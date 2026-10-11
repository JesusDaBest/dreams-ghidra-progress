#!/usr/bin/env python3
"""Build a public, path-free status document and deterministic SVG using stdlib only.

Normal use: python scripts/generate_status.py
Optional local inputs: --inventory PRIVATE_INVENTORY.json --cache-index PRIVATE_INDEX.json
Only addresses and allowlisted status fields are retained from local inputs. Names,
paths, signatures, decompiled text, metadata, and errors are never copied.
"""
from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import date
from html import escape
import json
import math
from pathlib import Path
import re
import subprocess


SCHEMA_VERSION = 1
DECOMPILATION = {
    "complete", "pending", "running", "failed", "truncated", "blocked_abi",
    "known_thunk", "known_external", "not_reported",
}
REVIEW = {"unreviewed", "verified_name", "deferred"}
CONVENTION = {"direct_sysv", "inherited_sysv", "other", "unknown"}
COLORS = {
    "background": "#0d1117", "panel": "#131b26", "border": "#263344",
    "text": "#f0f6fc", "muted": "#97a8bc",
    "green": "#3fb950", "blue": "#58a6ff", "gray": "#687c94",
    "amber": "#d29922",
}

# Explicit, reviewed research-area assignments. These are not recovered modules,
# and future verified names remain unassigned until their evidence is reviewed.
RESEARCH_AREAS = (
    ("sculpting-creation", "Sculpting & creation", "", ()),
    ("gadgets-logic", "Gadgets & logic", "Property and registration routines", (
        "1404d6660", "1404d7480", "1404d7ef0", "1404d83d0", "1404d87a0",
        "1404d8bf0", "1404d9c10", "1404da460", "1404dabe0", "1404db190",
        "140d57980", "140d57a50", "140d57b20", "140d57bf0", "140d57cc0",
        "140d57d90", "140d6dbd0", "140d6ddf0", "140d6e010", "140d6e2b0",
        "140d6e570", "140d6e850",
    )),
    ("rendering-lighting", "Rendering & lighting", "", ()),
    ("physics-movement", "Physics & movement", "", ()),
    ("sound-music", "Sound & music", "", ()),
    ("puppets-animation", "Puppets & animation", "", ()),
    ("interface-controls", "Interface & controls", "", ()),
    ("shared-object-data", "Shared object data", "Shared property helpers", (
        "1404f68b0", "1404f7a20", "1404f70b0", "1404f8350", "140cfda40",
    )),
)

# Display weights create readable, packed sections. They are deliberately separate
# from function counts: the number of functions in each system is still unknown.
SYSTEM_LAYOUT = (
    ("sculpting-creation", 38), ("rendering-lighting", 24),
    ("sound-music", 16), ("physics-movement", 14),
    ("puppets-animation", 12), ("interface-controls", 10),
    ("shared-object-data", 8),
)

# Families stay inside Gadgets & logic. Membership uses reviewed addresses,
# never a keyword match against a name or a guess about a routine's callers.
GADGET_LAYOUT = (
    ("signals", "Signals & calculation", 40, (
        ("combiner", "Combiner", 3, ("1404d87a0", "140d57980", "140d6e850")),
        ("signal-generator", "Signal generator", 3, ("1404da460", "140d57bf0", "140d6e010")),
        ("signal-inspector", "Signal inspector", 3, ("1404d9c10", "140d57b20", "140d6e2b0")),
        ("calculator", "Calculator", 2, ("1404d7ef0",)),
        ("splitter", "Splitter", 2, ("1404d83d0",)),
    )),
    ("effects", "Camera & effects", 20, (
        ("camera-shake", "Camera shake", 3, ("1404dabe0", "140d57cc0", "140d6ddf0")),
        ("fog", "Fog", 2, ("1404d6660",)),
    )),
    ("other-gadgets", "Other gadgets", 18, ()),
    ("doorway", "Doorways", 14, ("1404d8bf0", "140d57a50", "140d6e570")),
    ("rumble", "Controller rumble", 12, ("1404db190", "140d57d90", "140d6dbd0")),
    ("guides", "Placement guides", 10, ("1404d7480",)),
)


def address(value):
    text = str(value).lower().removeprefix("0x")
    if not re.fullmatch(r"[0-9a-f]{1,16}", text):
        raise ValueError("Inventory addresses must be hexadecimal, at most 64 bits")
    return format(int(text, 16), "x")


def natural(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer")
    return value


def safe_label(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value):
        raise ValueError(f"{label} must be a short public label, without paths or free text")
    return value


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def read_list(path):
    value = read_json(path)
    if isinstance(value, dict):
        value = value.get("items", value.get("rows"))
    if not isinstance(value, list):
        raise ValueError("Inventory/index input must be a list, or an object containing items/rows")
    return value


def inventory_addresses(path):
    result = []
    for row in read_list(path):
        if isinstance(row, dict):
            if row.get("present", 1) not in (0, 1):
                raise ValueError("Inventory present must be 0 or 1")
            if not row.get("present", 1):
                continue
            row = row["address"]
        result.append(address(row))
    if len(result) != len(set(result)):
        raise ValueError("Inventory contains duplicate addresses")
    return sorted(result, key=lambda item: int(item, 16))


def sanitize(raw, inventory=None, cache_index=None):
    """Construct an allowlisted document; never copy arbitrary source properties."""
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported status schema version")
    snapshot_date = raw["snapshot_date"]
    if not isinstance(snapshot_date, str) or date.fromisoformat(snapshot_date).isoformat() != snapshot_date:
        raise ValueError("snapshot_date must be YYYY-MM-DD")
    revision = safe_label(raw["analysis_revision"], "analysis_revision")
    existing = {}
    for item in raw.get("rows", []):
        if not isinstance(item, dict):
            raise ValueError("Status rows must be objects")
        addr = address(item["address"])
        if addr in existing:
            raise ValueError("Status contains duplicate addresses")
        row = {
            "address": addr,
            "convention": item.get("convention", "unknown"),
            "decompilation": item.get("decompilation", "not_reported"),
            "review": item.get("review", "unreviewed"),
        }
        for key, allowed in (("convention", CONVENTION), ("decompilation", DECOMPILATION), ("review", REVIEW)):
            if row[key] not in allowed:
                raise ValueError(f"Unknown {key} status at {addr}")
        existing[addr] = row
    addresses = inventory_addresses(inventory) if inventory else sorted(existing, key=lambda item: int(item, 16))
    if not addresses:
        raise ValueError("A nonempty discovered-function inventory is required")
    rows = [existing.get(addr, {"address": addr, "convention": "unknown",
                               "decompilation": "not_reported", "review": "unreviewed"}) for addr in addresses]
    declared_total = raw.get("inventory_total")
    if inventory is None and declared_total != len(rows):
        raise ValueError("inventory_total does not match the complete status row inventory")
    by_address = {row["address"]: row for row in rows}
    if cache_index:
        # A supplied snapshot replaces the old cache snapshot rather than mixing runs.
        for row in rows:
            row["decompilation"] = "not_reported"
        seen = set()
        for item in read_list(cache_index):
            if not isinstance(item, dict):
                raise ValueError("Cache index rows must be objects")
            if item.get("present", 1) not in (0, 1):
                raise ValueError("Cache present must be 0 or 1")
            if not item.get("present", 1):
                continue
            addr = address(item["address"])
            if addr not in by_address or addr in seen:
                raise ValueError("Cache index has an unknown or duplicate inventory address")
            seen.add(addr)
            state = item.get("status", item.get("decompilation"))
            if state not in DECOMPILATION:
                raise ValueError(f"Unknown cache status at {addr}")
            by_address[addr]["decompilation"] = state
    total = len(rows)
    declared_convention = raw.get("metrics", {}).get("convention", {})
    direct = natural(declared_convention.get("direct_sysv"), "direct_sysv")
    inherited = natural(declared_convention.get("inherited_sysv"), "inherited_sysv")
    if direct + inherited > total:
        raise ValueError("Effective SysV assignments exceed the discovered-function inventory")
    if declared_convention.get("effective_sysv", direct + inherited) != direct + inherited:
        raise ValueError("effective_sysv must equal direct_sysv plus inherited_sysv")
    convention_counts = Counter(row["convention"] for row in rows)
    for state, expected in (("direct_sysv", direct), ("inherited_sysv", inherited)):
        if convention_counts[state] > expected:
            raise ValueError("Per-address convention assignments exceed declared counts")
    if convention_counts["unknown"] == 0 and (convention_counts["direct_sysv"] != direct or convention_counts["inherited_sysv"] != inherited):
        raise ValueError("Complete convention rows disagree with declared convention totals")
    decomp = Counter(row["decompilation"] for row in rows)
    review = Counter(row["review"] for row in rows)
    reviewed = review["verified_name"] + review["deferred"]
    return {
        "schema_version": SCHEMA_VERSION,
        "snapshot_date": snapshot_date,
        "analysis_revision": revision,
        "inventory_total": total,
        "scope": "Currently discovered functions; not full binary completeness.",
        "metrics": {
            "convention": {
                "effective_sysv": direct + inherited, "direct_sysv": direct,
                "inherited_sysv": inherited, "other_or_unassigned": total - direct - inherited,
                "per_address_known": total - convention_counts["unknown"],
                "meaning": "Calling-convention assignment, not a correctness or completion percentage.",
            },
            "decompilation": {
                "reported": total - decomp["not_reported"], "complete": decomp["complete"],
                "pending": decomp["pending"], "running": decomp["running"],
                "failed": decomp["failed"], "truncated": decomp["truncated"],
                "blocked_abi": decomp["blocked_abi"], "known_thunk": decomp["known_thunk"],
                "known_external": decomp["known_external"], "not_reported": decomp["not_reported"],
                "meaning": "Cached decompiler output is not semantic review or recovered original source.",
            },
            "review": {
                "reviewed": reviewed, "verified_names": review["verified_name"],
                "deferred": review["deferred"], "unreviewed": review["unreviewed"],
                "meaning": "Recorded review outcomes; preexisting names do not count as verified.",
            },
        },
        "rows": rows,
    }


def text(x, y, content, size=14, color="text", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{COLORS.get(color, color)}"{extra}>{escape(str(content))}</text>'


def rect(x, y, width, height, fill, radius=0, stroke=None):
    border = f' stroke="{COLORS.get(stroke, stroke)}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{COLORS.get(fill, fill)}"{border}/>'


def legend(x, y, color, label, stroke=None):
    return rect(x, y-9, 8, 8, color, 1, stroke) + text(x+15, y, label, 11, "muted")


def research_area_rows(rows):
    """Assign verified rows by reviewed address allowlists, never by names."""
    by_address = {row["address"]: row for row in rows}
    if len(by_address) != len(rows):
        raise ValueError("Research-area input contains duplicate addresses")
    assigned = set()
    area_ids = set()
    result = []
    for area_id, title, role, known_addresses in RESEARCH_AREAS:
        if area_id in area_ids:
            raise ValueError("Research areas must have distinct IDs")
        area_ids.add(area_id)
        selected = []
        for addr in known_addresses:
            if address(addr) != addr or addr in assigned:
                raise ValueError("Research-area allowlists contain an invalid or repeated address")
            if addr not in by_address:
                raise ValueError("A reviewed research-area address is missing from the inventory")
            assigned.add(addr)
            row = by_address[addr]
            if row["review"] == "verified_name":
                selected.append(row)
        result.append((area_id, title, role, sorted(selected, key=lambda row: int(row["address"], 16))))
    return result


def packed_regions(entries, bounds):
    """Squarify positive display weights, independently of measured progress."""
    entries = sorted(entries, key=lambda item: -item[2])
    if not entries or any(item[2] <= 0 for item in entries):
        raise ValueError("A packed map needs positive layout weights")
    x, y, width, height = bounds
    scale = width * height / sum(item[2] for item in entries)
    areas = [item[2] * scale for item in entries]
    result, cursor = [], 0
    while cursor < len(entries):
        side = min(width, height)

        def distortion(end):
            strip = sum(areas[cursor:end]) / side
            return max(max(area / strip ** 2, strip ** 2 / area)
                       for area in areas[cursor:end])

        end = cursor + 1
        while end < len(entries) and distortion(end + 1) <= distortion(end):
            end += 1
        thickness = sum(areas[cursor:end]) / side
        offset = 0
        vertical = width >= height
        for index in range(cursor, end):
            length = areas[index] / thickness
            region = ((x, y + offset, thickness, length) if vertical
                      else (x + offset, y, length, thickness))
            result.append((entries[index], region))
            offset += length
        if vertical:
            x, width = x + thickness, width - thickness
        else:
            y, height = y + thickness, height - thickness
        cursor = end
    return result


def region_frame(bounds):
    x, y, width, height = bounds
    position = f'x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" height="{height:.3f}"'
    return [f'<rect data-unmapped-texture="true" {position} fill="url(#unmapped-grid)"/>',
            f'<rect data-region-border="true" {position} fill="none" stroke="#0d1117" stroke-width="3"/>']


def region_label(title, bounds, count=None):
    x, y, width, height = bounds
    limit = max(8, int((width - 10) / 6.4))
    lines, line = [], ""
    for word in title.split():
        if line and len(line) + len(word) + 1 > limit:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    lines.append(line)
    outline = ' stroke="#0d1117" stroke-width="3" stroke-linejoin="round" paint-order="stroke"'
    out = [text(round(x + 5, 3), round(y + 15 + 14 * i, 3), label, 12, extra=outline)
           for i, label in enumerate(lines)]
    if count is not None:
        label = f'{count} checked' if count else 'Unmapped'
        out.append(text(round(x + 5, 3), round(y + 16 + 14 * len(lines), 3),
                        label, 10, "muted", extra=outline))
    return out


def checked_tiles(rows, bounds):
    """Overlay exactly one green cell per checked name on the unknown texture."""
    x, y, width, height = bounds
    start_x = math.ceil((x + 4 - 0.5) / 7) * 7 + 0.5
    columns = max(1, int((x + width - 4 - start_x + 1) // 7))
    tile_rows = (len(rows) + columns - 1) // columns
    last_y = math.floor((y + height - 10 - 0.5) / 7) * 7 + 0.5
    start_y = last_y - (tile_rows - 1) * 7
    if tile_rows and start_y < y + 34:
        raise ValueError("Checked names need more display space in this region")
    out = []
    for index, row in enumerate(rows):
        if row["review"] != "verified_name":
            raise ValueError("Only verified names may appear in a research area")
        out.append(f'<rect data-function="{row["address"]}" data-status="verified_name" '
                   f'x="{start_x + (index % columns) * 7:.3f}" y="{start_y + (index // columns) * 7:.3f}" '
                   f'width="6" height="6" fill="{COLORS["green"]}"/>')
    return out


def gadget_regions(entries, bounds, by_address, assigned):
    out = []
    for (family_id, label, _, contents), region in packed_regions(entries, bounds):
        out.append(f'<g data-family="{family_id}">')
        out.extend(region_frame(region))
        if contents and isinstance(contents[0], tuple):
            out.extend(region_label(label, region))
            x, y, width, height = region
            out.extend(gadget_regions(contents, (x + 1, y + 23, width - 2, height - 24),
                                      by_address, assigned))
        else:
            selected = []
            for addr in contents:
                if addr in assigned or addr not in by_address:
                    raise ValueError("Gadget family assignments must be unique and reviewed")
                assigned.add(addr)
                selected.append(by_address[addr])
            out.append(f'<title>{escape(label)}: {len(selected)} checked property or registration names; total unknown.</title>')
            out.extend(region_label(label, region, len(selected)))
            out.extend(checked_tiles(selected, region))
        out.append('</g>')
    return out


def render(status, applied):
    total = status["inventory_total"]
    review = status["metrics"]["review"]
    assert len(applied) == review["verified_names"]
    assert {r["address"] for r in applied} == {r["address"] for r in status["rows"] if r["review"] == "verified_name"}
    rows = status["rows"]
    assert len(rows) == total and len({row["address"] for row in rows}) == total
    areas = research_area_rows(rows)
    mapped = sum(len(area_rows) for _, _, _, area_rows in areas)
    unassigned = total - mapped
    description = (f'{review["verified_names"]} of {total} function names checked. '
                   f'{mapped} verified names have explicit research-area assignments; {unassigned} functions do not. '
                   'These research areas are not proven module boundaries. '
                   'Green tiles show checked names only. Area totals are unknown. '
                   'The gray outline grid is an unmeasured background, not a function count. '
                   'Region sizes are layout choices, not code size or complexity.')
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="310" viewBox="0 0 1000 310" role="img" aria-labelledby="status-title status-desc">',
           '<title id="status-title">Dreams research areas and checked function names</title>',
           f'<desc id="status-desc">{escape(description)}</desc>',
           '<defs><pattern id="unmapped-grid" width="7" height="7" patternUnits="userSpaceOnUse">'
           '<rect width="7" height="7" fill="#0d1117"/>'
           '<rect x="0.5" y="0.5" width="6" height="6" fill="none" stroke="#414b57" stroke-width="0.7"/>'
           '</pattern></defs>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
           rect(0, 0, 1000, 310, "background")]
    area_by_id = {area[0]: area for area in areas}
    systems = [(area_id, area_by_id[area_id][1], weight, area_by_id[area_id][3])
               for area_id, weight in SYSTEM_LAYOUT]
    system_count = sum(len(entry[3]) for entry in systems)
    out.extend(['<g data-panel="systems">',
                text(4, 21, f'Dreams systems · {system_count} names checked', 16)])
    for (area_id, title, _, selected), bounds in packed_regions(systems, (0, 30, 495, 280)):
        out.append(f'<g data-area="{area_id}"><title>{escape(title)}: {len(selected)} checked names; total unknown.</title>')
        out.extend(region_frame(bounds))
        out.extend(region_label(title, bounds, len(selected)))
        out.extend(checked_tiles(selected, bounds))
        out.append('</g>')
    gadget_rows = area_by_id['gadgets-logic'][3]
    gadget_by_address = {row['address']: row for row in gadget_rows}
    out.extend(['</g><g data-panel="gadgets">',
                text(509, 21, f'Gadgets & logic · {len(gadget_rows)} names checked', 16),
                '<g data-area="gadgets-logic">'])
    out.extend(region_frame((505, 30, 495, 280)))
    assigned = set()
    out.extend(gadget_regions(GADGET_LAYOUT, (505, 30, 495, 280), gadget_by_address, assigned))
    if assigned != set(gadget_by_address):
        raise ValueError("Every reviewed gadget assignment must appear exactly once")
    out.extend(['</g></g></g></svg>'])
    return "\n".join(out) + "\n"


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    badges = [
        ("names checked", f"{100 * metrics['review']['verified_names'] / total:.2f}%", "green"),
    ]
    widths = [(round(len(label) * 6.5 + 20), round(len(value) * 6.5 + 20)) for label, value, _ in badges]
    width = sum(left + right for left, right in widths) + 10 * (len(badges)-1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" viewBox="0 0 {width} 20" role="img" aria-labelledby="badges-title badges-desc">',
           '<title id="badges-title">Dreams analysis status badges</title>',
           '<desc id="badges-desc">Share of discovered function names checked. Analysis is in progress.</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" font-size="11">']
    x = 0
    for (label, value, color), (left, right) in zip(badges, widths):
        out.extend([rect(x, 0, left, 20, "#555"),
                    rect(x+left, 0, right, 20, color),
                    text(x+left/2, 14, label, 11, "text", 500, ' text-anchor="middle"'),
                    text(x+left+right/2, 14, value, 11, "background", 700, ' text-anchor="middle"')])
        x += left+right+10
    out.append('</g></svg>')
    return "\n".join(out) + "\n"


def write_atomic(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(content.encode("utf-8"))
    temporary.replace(path)


def asset_link(repo, name, asset, readme, revision=None):
    """Pin committed images to immutable URLs; branch-based raw images can lag."""
    raw_base = 'https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/'
    requested = revision is not None
    if revision is not None and not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Asset revision must be a full Git commit ID')
    if revision is None:
        match = re.search(re.escape(raw_base) + r'([0-9a-f]{40})/assets/' + re.escape(name), readme)
        revision = match.group(1) if match else None
    if revision is not None:
        committed = subprocess.run(['git', '-C', str(repo), 'show', f'{revision}:assets/{name}'],
                                   capture_output=True, check=False)
        if committed.returncode == 0 and committed.stdout.replace(b'\r\n', b'\n') == asset.encode('utf-8'):
            return f'{raw_base}{revision}/assets/{name}'
        if requested:
            raise ValueError(f'Requested revision does not contain the current {name}; commit the generated assets first')
        # Never retain an immutable link to an older rendering after data changes.
    version = hashlib.sha256(asset.encode('utf-8')).hexdigest()[:12]
    return f'assets/{name}?v={version}'


def main(argv=None):
    repo = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", type=Path, default=repo / "analysis" / "status.json", help="Public sanitized status input; rewritten canonically")
    parser.add_argument("--output", type=Path, default=repo / "assets" / "status.svg")
    parser.add_argument("--badges-output", type=Path, default=repo / "assets" / "status-badges.svg")
    parser.add_argument("--inventory", type=Path, help="Local inventory: copies only addresses; names and all other fields discarded")
    parser.add_argument("--cache-index", type=Path, help="Optional local cache function-index.json; copies only address/status")
    parser.add_argument("--check", action="store_true", help="Validate canonical JSON and SVG without writing")
    parser.add_argument("--asset-revision", help="Pin README images to a committed revision containing the generated assets")
    args = parser.parse_args(argv)
    status = sanitize(read_json(args.status), args.inventory, args.cache_index)
    # Compact rows keep the public inventory small and reviewable; the header is pretty printed.
    header = dict(status)
    rows = header.pop("rows")
    content = json.dumps(header, indent=2)[:-2] + ',\n  "rows": [\n'
    content += ",\n".join("    " + json.dumps(row, separators=(",", ":")) for row in rows)
    content += "\n  ]\n}\n"
    svg = render(status, read_json(repo / "analysis" / "function-review.json")["applied"])
    badges_svg = render_badges(status)
    readme_path = repo / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    expected_readme = readme
    for name, asset in (('status.svg', svg), ('status-badges.svg', badges_svg)):
        link = asset_link(repo, name, asset, readme, args.asset_revision)
        pattern = (r'\]\((?:assets/|https://raw\.githubusercontent\.com/JesusDaBest/dreams-ghidra-progress/[0-9a-f]{40}/assets/)'
                   + re.escape(name) + r'(?:\?v=[a-zA-Z0-9_-]+)?\)')
        expected_readme, count = re.subn(pattern, f']({link})', expected_readme)
        if count != 1:
            raise ValueError(f'Expected exactly one README image link for {name}')
    if args.check:
        if (args.status.read_text(encoding="utf-8") != content or not args.output.is_file()
                or args.output.read_text(encoding="utf-8") != svg or not args.badges_output.is_file()
                or args.badges_output.read_text(encoding="utf-8") != badges_svg
                or readme != expected_readme):
            raise SystemExit("Status assets are valid but not current; regenerate them")
        print("Status assets are valid and current")
    else:
        write_atomic(args.status, content)
        write_atomic(args.output, svg)
        write_atomic(args.badges_output, badges_svg)
        write_atomic(readme_path, expected_readme)
        print(f"Generated public status for {len(rows):,} discovered functions")


if __name__ == "__main__":
    main()
