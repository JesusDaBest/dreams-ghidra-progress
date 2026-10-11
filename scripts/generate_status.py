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
import textwrap


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
    "green": "#3fb950", "blue": "#58a6ff", "gray": "#484f58",
    "amber": "#d29922",
}

# Mapping is independently evidenced in analysis/system-map.json. Discovering
# ownership never changes a function's semantic-review state.

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


def research_area_rows(rows, mapping):
    """Group mapped functions; unknown ownership is reported outside the map."""
    by_address = {row["address"]: row for row in rows}
    if len(by_address) != len(rows):
        raise ValueError("Research-area input contains duplicate addresses")
    if mapping['schema_version'] != 1:
        raise ValueError('Unsupported system-map schema')
    systems = mapping['systems']
    if not systems or 'unassigned' in systems:
        raise ValueError('The map must contain evidenced systems')
    grouped = {system: [] for system in systems}
    for addr, assignment in mapping['assignments'].items():
        if address(addr) != addr or addr not in by_address:
            raise ValueError('Mapped address is missing from the inventory')
        if assignment['system'] not in systems or not assignment['evidence']:
            raise ValueError('Every system assignment requires evidence')
        grouped[assignment['system']].append(by_address[addr])
    return [(system, label, '', sorted(grouped[system], key=lambda row: int(row['address'],16)))
            for system, label in systems.items()]


def packed_regions(entries, bounds):
    """Area is proportional ONLY to the number of real functions in each group."""
    entries = sorted((item for item in entries if item[3]), key=lambda item: (-len(item[3]), item[0]))
    if not entries:
        raise ValueError("A status map needs a nonempty function inventory")
    x, y, width, height = bounds
    scale = width * height / sum(len(item[3]) for item in entries)
    areas = [len(item[3]) * scale for item in entries]
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


def function_cells(rows, bounds, metric="review"):
    """One equal-area cell per address. No texture or placeholder cells."""
    x, y, width, height = bounds
    count = len(rows)
    grid_rows = max(1, min(count, round(math.sqrt(count * height / width))))
    priority = {'verified_name': 0, 'deferred': 1, 'unreviewed': 2}
    colors = {'verified_name': 'green', 'deferred': 'amber', 'unreviewed': 'gray'}
    if metric == "decompilation":
        colors = {state: ('blue' if state == 'complete' else 'amber' if state in {'failed', 'truncated', 'blocked_abi'} else 'gray') for state in DECOMPILATION}
        priority = {state: (0 if colors[state] == 'blue' else 1 if colors[state] == 'amber' else 2) for state in DECOMPILATION}
    ordered = sorted(rows, key=lambda row: (priority[row[metric]], int(row['address'], 16)))
    out, cursor, offset_y = [], 0, 0
    for line in range(grid_rows):
        columns = count // grid_rows + (line < count % grid_rows)
        cell_width, cell_height = width / columns, height * columns / count
        for column in range(columns):
            row = ordered[cursor]
            out.append(f'<rect data-function="{row["address"]}" data-status="{row[metric]}" '
                       f'x="{x + column * cell_width:.6f}" y="{y + offset_y:.6f}" '
                       f'width="{cell_width:.6f}" height="{cell_height:.6f}" '
                       f'fill="{COLORS[colors[row[metric]]]}" stroke="#0d1117" stroke-width="0.5"/>')
            cursor += 1
        offset_y += cell_height
    return out


def render(status, applied, mapping):
    total = status['inventory_total']
    review = status['metrics']['review']
    assert {r['address'] for r in applied} == {r['address'] for r in status['rows'] if r['review'] == 'verified_name'}
    areas = research_area_rows(status['rows'], mapping)
    mapped = sum(len(items) for _, _, _, items in areas)
    selected_rows = [row for _, _, _, items in areas for row in items]
    short = {
        'Sculpting & painting': 'Sculpting', 'Gadgets & logic': 'Gadgets & logic',
        'Physics & collision': 'Physics', 'Sound & music': 'Audio',
        'Animation & puppets': 'Animation', 'Rendering & lighting': 'Rendering',
        'Editor & interface': 'Editor', 'Dreamiverse & networking': 'Dreamiverse',
        'Shared engine & object data': 'Shared engine',
    }
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="398" viewBox="0 0 1000 398" role="img" aria-labelledby="status-title status-desc">',
           '<title id="status-title">Dreams: code extraction and name checking by system</title>',
           '<desc id="status-desc">Two maps of the same mapped functions. Blue means decompiled output exists; green means name checked. Gray means unfinished; amber needs follow-up. System sizes represent only identified functions, not complete system sizes.</desc>',
           '<g font-family="Segoe UI,Arial,sans-serif">', rect(0,0,1000,398,'background')]
    outline = ' stroke="#0d1117" stroke-width="3" paint-order="stroke"'
    for metric, left, heading, state in [('decompilation',0,'Code extracted','complete'), ('review',505,'Names checked','verified_name')]:
        done = sum(row[metric] == state for row in selected_rows)
        out.append(text(left+4,20,f'{heading}: {done:,}/{mapped:,} ({100*done/mapped:.1f}%)',15))
        out.append(f'<g data-panel="{metric}">')
        for (area_id,title,_,selected), bounds in packed_regions(areas,(left,32,495,280)):
            x,y,w,h = bounds
            count = sum(row[metric] == state for row in selected)
            out.append(f'<g data-area="{area_id}" data-count="{len(selected)}"><title>{escape(title)}: {heading.lower()} {count}/{len(selected)} mapped functions. Whole-system completion unknown.</title>')
            out.extend(function_cells(selected,bounds,metric))
            out.append(f'<rect data-region-border="true" x="{x:.6f}" y="{y:.6f}" width="{w:.6f}" height="{h:.6f}" fill="none" stroke="#0d1117" stroke-width="2"/>')
            label = short.get(title,title)
            # Keep narrow labels readable without crossing into another system.
            for line,label_line in enumerate(textwrap.wrap(label,width=max(6,int((w-10)/6.4)),break_long_words=False)):
                out.append(text(round(x+4,3),round(y+14+13*line,3),label_line,11,weight=600,extra=outline))
            out.append('</g>')
        out.append('</g>')
    out.extend([legend(4,334,'blue','Decompiler output available'),legend(505,334,'green','Name checked'),
                legend(4,354,'amber','Extraction needs follow-up'),legend(505,354,'amber','Reviewed, still unclear'),
                legend(260,334,'gray','No output yet'),legend(765,334,'gray','Not reviewed'),
                text(4,378,f'Same {mapped:,} functions in both maps. One square = one function; {total-mapped:,} still need a system assignment.',12,'muted'),
                text(4,394,'Section sizes count identified code only. Full system sizes and completion are unknown.',12,'muted'),'</g></svg>'])
    return '\n'.join(out)+'\n'


def render_area_table(status, mapping):
    areas = research_area_rows(status['rows'], mapping)
    lines = ['| Part of Dreams | Functions mapped | Code extracted | Names checked |',
             '| --- | ---: | ---: | ---: |']
    for area_id, title, _, rows in areas:
        checked = sum(row['review'] == 'verified_name' for row in rows)
        progress = f'{checked:,} / {len(rows):,} ({100*checked/len(rows):.1f}%)' if rows else 'No functions mapped yet'
        extracted = sum(row['decompilation'] == 'complete' for row in rows)
        lines.append(f'| {title} | {len(rows):,} | {extracted:,} / {len(rows):,} | {progress} |')
    mapped = sum(len(rows) for _,_,_,rows in areas)
    unassigned = status['inventory_total'] - mapped
    lines.extend(['', f'**{mapped:,} of {status["inventory_total"]:,} discovered functions are mapped; {unassigned:,} still need a system assignment.** '
                  'Percentages measure checked names among the functions mapped to that section. '
                  'The complete size of each system is still unknown; these are not whole-game completion percentages.'])
    return '\n'.join(lines)


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    badges = [
        ("code extracted", f"{100 * metrics['decompilation']['complete'] / total:.2f}%", "blue"),
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
    parser.add_argument("--system-map", type=Path, default=repo / "analysis" / "system-map.json", help="Evidenced code-to-system assignments")
    parser.add_argument("--output", type=Path, default=repo / "assets" / "status.svg")
    parser.add_argument("--badges-output", type=Path, default=repo / "assets" / "status-badges.svg")
    parser.add_argument("--inventory", type=Path, help="Local inventory: copies only addresses; names and all other fields discarded")
    parser.add_argument("--cache-index", type=Path, help="Optional local cache function-index.json; copies only address/status")
    parser.add_argument("--check", action="store_true", help="Validate canonical JSON and SVG without writing")
    parser.add_argument("--asset-revision", help="Pin README images to a committed revision containing the generated assets")
    args = parser.parse_args(argv)
    status = sanitize(read_json(args.status), args.inventory, args.cache_index)
    mapping = read_json(args.system_map)
    # Compact rows keep the public inventory small and reviewable; the header is pretty printed.
    header = dict(status)
    rows = header.pop("rows")
    content = json.dumps(header, indent=2)[:-2] + ',\n  "rows": [\n'
    content += ",\n".join("    " + json.dumps(row, separators=(",", ":")) for row in rows)
    content += "\n  ]\n}\n"
    svg = render(status, read_json(repo / "analysis" / "function-review.json")["applied"], mapping)
    badges_svg = render_badges(status)
    readme_path = repo / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    expected_readme = readme
    summary = (f'**{status["metrics"]["review"]["verified_names"]:,} of {status["inventory_total"]:,} '
               'functions named and checked.** A function is one piece of the game\'s code.')
    for marker, replacement in (('status-summary', summary), ('area-status', render_area_table(status, mapping))):
        pattern = rf'(<!-- {marker}:start -->).*?(<!-- {marker}:end -->)'
        expected_readme, count = re.subn(pattern, lambda m: m[1] + '\n' + replacement + '\n' + m[2],
                                        expected_readme, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected exactly one generated README block for {marker}')
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
