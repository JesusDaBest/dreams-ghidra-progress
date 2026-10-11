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
from collections import Counter, defaultdict
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
# Labels are navigation hints inherited from the analysis, never review evidence.
# Specific named types precede broad property/helper roles. Unnamed functions
# are never assigned to a topic based on address proximity or a guessed subsystem.
TOPIC_RULES = (
    ("Logic tools", ("Calculator", "Splitter", "Combiner", "SignalInspector", "SignalGenerator")),
    ("Puppets", ("Puppet", "Limb")),
    ("Health", ("Health",)),
    ("Rotation", ("Rotator", "Gyroscope")),
    ("Movement", ("Mover", "Follower")),
    ("Variables / scores", ("Variable", "Score")),
    ("Emitters", ("Emitter",)),
    ("Sculpts", ("Sculpt",)),
    ("Sprites", ("Sprite",)),
    ("Physics", ("Physics", "Joint", "Raycast", "Shapecast")),
    ("Impact", ("Impact",)),
    ("Sound", ("AudioNumber", "SoundCategory")),
    ("Settings", ("GlobalSettings",)),
    ("Graphics", ("Shader",)),
    ("Fog", ("Fog",)),
    ("Guides", ("AutoGuides",)),
    ("Doorways", ("MagicDoor",)),
    ("Data fields", ("Properties", "FieldOffset", "TypeDescriptor", "RegisterEnumValue")),
    ("Object updates", ("Thing", "GameUpdate")),
)
GROUPS = {label for label, _ in TOPIC_RULES} | {"Startup", "Other labels", "Unidentified"}
COLORS = {
    "background": "#0d1117", "panel": "#131b26", "border": "#263344",
    "text": "#f0f6fc", "muted": "#97a8bc", "dim": "#6e829a",
    "green": "#3fb950", "cyan": "#39d5ff", "blue": "#58a6ff", "gray": "#283747",
    "amber": "#d29922", "accounted": "#687c94",
}


def group_for_name(name):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,119}", name):
        return "Unidentified"
    if re.fullmatch(r"(?:thunk_)*FUN_[0-9a-fA-F]+", name):
        return "Unidentified"
    if name in {"entry", "RunRuntimeCallbackTables"}:
        return "Startup"
    for label, tokens in TOPIC_RULES:
        if any(token in name for token in tokens):
            return label
    return "Other labels"


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
            "group": item.get("group", "Unidentified"),
        }
        for key, allowed in (("convention", CONVENTION), ("decompilation", DECOMPILATION), ("review", REVIEW), ("group", GROUPS)):
            if row[key] not in allowed:
                raise ValueError(f"Unknown {key} status at {addr}")
        existing[addr] = row
    addresses = inventory_addresses(inventory) if inventory else sorted(existing, key=lambda item: int(item, 16))
    if not addresses:
        raise ValueError("A nonempty discovered-function inventory is required")
    rows = [existing.get(addr, {"address": addr, "convention": "unknown",
                               "decompilation": "not_reported", "review": "unreviewed", "group": "Unidentified"}) for addr in addresses]
    declared_total = raw.get("inventory_total")
    if inventory is None and declared_total != len(rows):
        raise ValueError("inventory_total does not match the complete status row inventory")
    by_address = {row["address"]: row for row in rows}
    if inventory:
        for item in read_list(inventory):
            if isinstance(item, dict) and item.get("present", 1):
                by_address[address(item["address"])]["group"] = group_for_name(item.get("name"))
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
        "grouping_basis": "Presentation groups inferred from existing function labels, not verified subsystem boundaries. Unnamed code remains unidentified. Review states are independent of labels.",
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


def legend(x, y, color, label):
    return rect(x, y-9, 8, 8, color, 1) + text(x+15, y, label, 11, "muted")


def region_tiles(items, bounds):
    x, y, width, height = bounds
    # Distribute exactly count cells across near-square rows, with no filler cells.
    count = len(items)
    if not count:
        return ""
    row_count = max(1, min(count, int(math.sqrt(count * height / width) + 0.5)))
    base, remainder = divmod(count, row_count)
    colors = {"verified_name": "green", "deferred": "amber", "unreviewed": "accounted"}
    out = []
    cursor = 0
    for row_index in range(row_count):
        columns = base + (1 if row_index < remainder else 0)
        for column in range(columns):
            item = items[cursor]
            px = x + width * column / columns
            py = y + height * row_index / row_count
            cell_width, cell_height = width / columns, height / row_count
            out.append(f'<rect data-function="{item["address"]}" x="{px:.3f}" y="{py:.3f}" '
                       f'width="{cell_width:.3f}" height="{cell_height:.3f}" '
                       f'fill="{COLORS[colors[item["review"]]]}" stroke="{COLORS["background"]}" stroke-width="0.65"/>')
            cursor += 1
    assert cursor == count
    return "".join(out)


def group_rectangles(groups, bounds):
    """Pack count-weighted areas into strips chosen for near-square rectangles."""
    if not groups:
        return []
    x, y, width, height = bounds
    area_per_function = width * height / sum(len(items) for _, items in groups)
    areas = [len(items) * area_per_function for _, items in groups]
    result, cursor = [], 0
    while cursor < len(groups):
        short_side = min(width, height)
        def distortion(end):
            values = areas[cursor:end]
            strip_width = sum(values) / short_side
            return max(max(value / (strip_width * strip_width),
                           strip_width * strip_width / value) for value in values)
        end = cursor + 1
        while end < len(groups) and distortion(end + 1) <= distortion(end):
            end += 1
        thickness = sum(areas[cursor:end]) / short_side
        offset = 0
        vertical = width >= height
        for index in range(cursor, end):
            length = areas[index] / thickness
            cell = ((x, y + offset, thickness, length) if vertical
                    else (x + offset, y, length, thickness))
            result.append((groups[index], cell))
            offset += length
        if vertical:
            x, width = x + thickness, width - thickness
        else:
            y, height = y + thickness, height - thickness
        cursor = end
    return result


def grouped_map(rows, bounds):
    groups = defaultdict(list)
    priority = {"verified_name": 0, "deferred": 1, "unreviewed": 2}
    for row in rows:
        groups[row["group"]].append(row)
    ordered = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    out = []
    for (label, items), (x, y, width, height) in group_rectangles(ordered, bounds):
        items = sorted(items, key=lambda row: (priority[row["review"]], int(row["address"], 16)))
        checked = sum(row["review"] == "verified_name" for row in items)
        out.extend([f'<g data-group="{escape(label)}"><title>{escape(label)}: {checked} checked / {len(items)} labeled functions</title>',
                    region_tiles(items, (x + 1, y + 1, width - 2, height - 2)),
                    rect(x, y, width, height, "none", stroke="background")])
        # Put each label on the group itself, like a map legend, with a dark outline.
        words, lines, line = label.split(), [], ""
        size = min(13, max(9, (width - 8) / (max(map(len, words)) * 0.57)))
        limit = max(3, int((width - 8) / (size * 0.57)))
        for word in words:
            if line and len(line) + 1 + len(word) > limit:
                lines.append(line)
                line = word
            else:
                line = (line + " " + word).strip()
        lines.append(line)
        label_count = 0
        for index, line in enumerate(lines):
            if len(line) <= limit and 20 + index * 15 < height:
                out.append(text(round(x + 4, 3), round(y + 16 + index * 15, 3), line, round(size, 2), "text", 500,
                                ' stroke="#0d1117" stroke-width="3" paint-order="stroke"'))
                label_count += 1
        if not label_count and height > width:
            size = min(12, (height - 8) / (len(label) * 0.57), width - 8)
            if size >= 9:
                cx, cy = round(x + width / 2, 3), round(y + height / 2, 3)
                out.append(text(cx, cy, label, round(size, 2), "text", 500,
                                f' text-anchor="middle" dominant-baseline="middle" transform="rotate(-90 {cx} {cy})"'
                                ' stroke="#0d1117" stroke-width="3" paint-order="stroke"'))
        out.append('</g>')
    return "\n".join(out)


def render(status, applied):
    total = status["inventory_total"]
    review = status["metrics"]["review"]
    assert len(applied) == review["verified_names"]
    assert {r["address"] for r in applied} == {r["address"] for r in status["rows"] if r["review"] == "verified_name"}
    labeled = [row for row in status["rows"] if row["group"] != "Unidentified"]
    unknown = sorted((row for row in status["rows"] if row["group"] == "Unidentified"),
                     key=lambda row: (row["review"] != "deferred", int(row["address"], 16)))
    checked_labeled = sum(row["review"] == "verified_name" for row in labeled)
    description = (f'{review["verified_names"]} of {total} functions named and checked. '
                   f'{len(labeled)} functions grouped by existing labels; {len(unknown)} still unidentified. '
                   'Each square is one function. Panels use different scales. Existing labels remain gray until checked.')
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="424" viewBox="0 0 1120 424" role="img" aria-labelledby="status-title status-desc">',
           '<title id="status-title">Dreams function review progress</title>',
           f'<desc id="status-desc">{escape(description)}</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
           rect(0, 0, 1120, 424, "background"),
           text(4, 21, f'Labeled code: {checked_labeled:,} checked / {len(labeled):,}', 17),
           text(574, 21, f'Code still to identify: {len(unknown):,}', 17),
           text(4, 43, 'Grouped by existing labels', 13, "muted"),
           text(574, 43, 'The purpose of this code is still being investigated', 13, "muted"),
           grouped_map(labeled, (0, 54, 550, 310)),
           region_tiles(unknown, (571, 55, 548, 308)),
           rect(570, 54, 550, 310, "none", stroke="background"),
           legend(4, 386, "green", f'Name checked: {review["verified_names"]:,}'),
           legend(234, 386, "amber", f'Still unclear: {review["deferred"]:,}'),
           legend(453, 386, "accounted", f'Not reviewed: {review["unreviewed"]:,}'),
           text(4, 411, 'One square = one function. Panels use different scales. Existing labels stay gray until checked.', 13, "muted"),
           '</g></svg>']
    return "\n".join(out) + "\n"


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    decomp = metrics["decompilation"]
    badges = [
        ("names checked", f"{100 * metrics['review']['verified_names'] / total:.2f}%", "green"),
        ("code extracted", f"{100 * decomp['complete'] / total:.2f}%", "blue"),
    ]
    widths = [(round(len(label) * 6.5 + 20), round(len(value) * 6.5 + 20)) for label, value, _ in badges]
    width = sum(left + right for left, right in widths) + 10 * (len(badges)-1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="26" viewBox="0 0 {width} 26" role="img" aria-labelledby="badges-title badges-desc">',
           '<title id="badges-title">Dreams analysis status badges</title>',
           '<desc id="badges-desc">Counts cover discovered functions. Generated pseudocode still needs review; verified names do not imply complete behavioral understanding. Analysis is in progress.</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" font-size="11">']
    x = 0
    for (label, value, color), (left, right) in zip(badges, widths):
        out.extend([rect(x, 1, left+right, 24, "panel", 4, "border"),
                    rect(x+left, 1, right, 24, color, 4), rect(x+left, 1, 4, 24, color),
                    text(x+left/2, 17, label, 11, "muted", 550, ' text-anchor="middle"'),
                    text(x+left+right/2, 17, value, 11, "background", 700, ' text-anchor="middle"')])
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
    parser.add_argument("--inventory", type=Path, help="Local inventory: copy addresses and derive allowlisted groups from names; names and all other fields discarded")
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
