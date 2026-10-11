#!/usr/bin/env python3
"""Build a public, path-free status document and deterministic SVG using stdlib only.

Normal use: python scripts/generate_status.py
Optional local inputs: --inventory PRIVATE_INVENTORY.json --cache-index PRIVATE_INDEX.json
Only addresses and allowlisted status fields are retained from local inputs. Names,
paths, signatures, decompiled text, metadata, and errors are never copied.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from html import escape
import json
import math
from pathlib import Path
import re


SCHEMA_VERSION = 1
DECOMPILATION = {
    "complete", "pending", "running", "failed", "truncated", "blocked_abi",
    "known_thunk", "known_external", "not_reported",
}
REVIEW = {"unreviewed", "verified_name", "deferred"}
CONVENTION = {"direct_sysv", "inherited_sysv", "other", "unknown"}
COLORS = {
    "background": "#0d1117", "panel": "#131b26", "border": "#263344",
    "text": "#f0f6fc", "muted": "#97a8bc", "dim": "#6e829a",
    "green": "#3fb950", "cyan": "#39d5ff", "gray": "#283747",
    "amber": "#d29922", "accounted": "#687c94",
}


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


def progress(x, y, width, total, segments):
    parts = [rect(x, y, width, 5, "gray", 2)]
    cursor = x
    for count, color in segments:
        length = width * count / total
        if length:
            parts.append(rect(f"{cursor:.3f}", y, f"{length:.3f}", 5, color))
            cursor += length
    return "".join(parts)


def mosaic(rows, key, x, y, columns, color_for):
    # One 3x3 square per function, 1px separation. Grouping paths by color keeps
    # the SVG substantially smaller than thousands of separate rect/title nodes.
    paths = defaultdict(list)
    for index, row in enumerate(rows):
        px = x + (index % columns) * 4
        py = y + (index // columns) * 4
        paths[color_for(row[key])].append(f"M{px} {py}h3v3h-3z")
    return "".join(f'<path fill="{COLORS[color]}" d="{"".join(paths[color])}"/>' for color in sorted(paths))


def legend(x, y, color, label):
    return rect(x, y-9, 8, 8, color, 1) + text(x+15, y, label, 11, "muted")


def grouped_height(groups, columns):
    return sum(48 + math.ceil(len(items) / columns) * 4 for _, _, items in groups) + 12 * (len(groups)-1)


def grouped_mosaic(groups, key, x, y, columns):
    """Keep each status in its own labeled block; addresses order only within it."""
    out = []
    for label, color, items in groups:
        grid_height = math.ceil(len(items) / columns) * 4
        height = 48 + grid_height
        out.extend([rect(x-10, y, columns*4+20, height, "background", 6, "border"),
                    rect(x, y+13, 3, 13, color, 1),
                    text(x+12, y+24, label, 12, "muted", 600),
                    text(x+columns*4, y+24, f"{len(items):,}", 14, "text", 700, ' text-anchor="end"'),
                    mosaic(items, key, x, y+35, columns, lambda _: color)])
        y += height + 12
    return "".join(out)


def render(status):
    rows = status["rows"]
    total = len(rows)
    conv = status["metrics"]["convention"]
    decomp = status["metrics"]["decompilation"]
    review = status["metrics"]["review"]
    columns = 118
    decomp_groups = [
        ("Pseudocode cached", "green", [r for r in rows if r['decompilation'] == 'complete']),
        ("Needs follow-up", "amber", [r for r in rows if r['decompilation'] in {'failed', 'truncated', 'blocked_abi'}]),
        ("Waiting to decompile", "gray", [r for r in rows if r['decompilation'] in {'pending', 'not_reported'}]),
    ]
    running = [r for r in rows if r['decompilation'] == 'running']
    if running:
        decomp_groups.insert(2, ("Running", "cyan", running))
    separate = [r for r in rows if r['decompilation'] in {'known_thunk', 'known_external'}]
    if separate:
        decomp_groups.append(("Separately accounted", "accounted", separate))
    review_groups = [
        ("Names verified", "green", [r for r in rows if r['review'] == 'verified_name']),
        ("Reviewed, still unresolved", "amber", [r for r in rows if r['review'] == 'deferred']),
        ("Awaiting semantic review", "gray", [r for r in rows if r['review'] == 'unreviewed']),
    ]
    for groups in (decomp_groups, review_groups):
        grouped_addresses = [r['address'] for _, _, items in groups for r in items]
        if len(grouped_addresses) != total or set(grouped_addresses) != {r['address'] for r in rows}:
            raise ValueError('Grouped graphic must represent every discovered function exactly once')
    grid_height = max(grouped_height(decomp_groups, columns), grouped_height(review_groups, columns))
    panel_top = 280
    grid_top = panel_top + 82
    panel_height = 82 + grid_height + 20
    footer_top = panel_top + panel_height + 28
    height = footer_top + 72
    unresolved = decomp["failed"] + decomp["truncated"] + decomp["blocked_abi"]
    accounted = decomp["known_thunk"] + decomp["known_external"]
    n = lambda value: f"{value:,}"
    description = (f"Status for {n(total)} discovered functions. {n(conv['effective_sysv'])} have an effective SysV calling convention assigned. "
                   f"{n(decomp['complete'])} cached decompilations from {n(decomp['reported'])} reported cache states. "
                   f"{n(review['reviewed'])} reviewed: {n(review['verified_names'])} verified names and {n(review['deferred'])} deferred. "
                   "These counts do not measure full binary completeness.")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{height}" viewBox="0 0 1120 {height}" role="img" aria-labelledby="status-title status-desc">',
           '<title id="status-title">Dreams analysis status</title>', f'<desc id="status-desc">{escape(description)}</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
           rect(0, 0, 1120, height, "background", 18),
           rect(32, 32, 4, 44, "cyan", 2),
           text(50, 54, "DREAMS", 27, "text", 750), text(50, 77, "Reverse engineering progress", 16, "muted"),
           rect(883, 37, 205, 27, "panel", 13, "border"),
           text(900, 55, "FUNCTION STATUS BLOCKS", 10, "cyan", 650),
           text(32, 112, f"{n(total)} functions in the current inventory", 14, "muted"),
           text(1088, 112, f"Snapshot {status['snapshot_date']}", 12, "dim", extra=' text-anchor="end"')]
    card_y, card_h, card_w = 134, 118, 344
    for x in (32, 388, 744):
        out.append(rect(x, card_y, card_w, card_h, "panel", 10, "border"))
    out.extend([text(50, 158, "EFFECTIVE SYSV ASSIGNMENT", 11, "cyan", 650),
                text(50, 196, n(conv["effective_sysv"]), 32, "text", 700),
                text(172, 194, f"/ {n(total)}", 17, "muted"),
                text(50, 218, f"{n(conv['direct_sysv'])} direct + {n(conv['inherited_sysv'])} inherited", 12, "muted"),
                progress(50, 231, 308, total, [(conv["effective_sysv"], "cyan")]),
                text(406, 158, "DECOMPILATION CACHE", 11, "green", 650)])
    if decomp["reported"]:
        out.extend([text(406, 196, n(decomp["complete"]), 32, "text", 700),
                    text(528, 194, f"/ {n(total)}", 17, "muted"),
                    text(406, 218, f"{n(unresolved)} unresolved · {n(accounted)} separately accounted", 12, "muted")])
    else:
        out.extend([text(406, 194, "Awaiting data", 25, "text", 650),
                    text(406, 218, "No local cache snapshot reported yet", 12, "muted")])
    out.extend([progress(406, 231, 308, total, [(decomp["complete"], "green"), (decomp["running"], "cyan"), (unresolved, "amber"), (accounted, "accounted")]),
                text(762, 158, "REVIEWED FUNCTIONS", 11, "green", 650),
                text(762, 196, n(review["reviewed"]), 32, "text", 700),
                text(884, 194, f"/ {n(total)}", 17, "muted"),
                text(762, 218, f"{n(review['verified_names'])} names verified · {n(review['deferred'])} deferred", 12, "muted"),
                progress(762, 231, 308, total, [(review["verified_names"], "green"), (review["deferred"], "amber")])])
    for x in (32, 576):
        out.append(rect(x, panel_top, 512, panel_height, "panel", 10, "border"))
    out.extend([text(52, panel_top+29, "Decompilation coverage", 18, "text", 650),
                text(52, panel_top+52, "Cached output, independent of semantic review", 12, "muted"),
                text(596, panel_top+29, "Review coverage", 18, "text", 650),
                text(596, panel_top+52, "Verified naming and explicitly deferred reviews", 12, "muted")])
    out.extend([grouped_mosaic(decomp_groups, "decompilation", 52, grid_top, columns),
                grouped_mosaic(review_groups, "review", 596, grid_top, columns)])
    out.extend([
                text(32, footer_top, "ONE SQUARE = ONE DISCOVERED FUNCTION", 11, "cyan", 650),
                text(32, footer_top+20, "Squares are grouped by status, then ordered by address inside each labeled block.", 12, "muted"),
                text(32, footer_top+42, "Inventory coverage is not full binary completeness. Convention assignments and cached output are not correctness claims.", 11, "dim"),
                '</g></svg>'])
    return "\n".join(out) + "\n"


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    decomp = metrics["decompilation"]
    reviewed = metrics["review"]["reviewed"]
    pseudocode = f"{100 * decomp['complete'] / total:.1f}%" if decomp["reported"] else "awaiting data"
    badges = [
        ("pseudocode", pseudocode, "green"),
        ("reviewed", f"{100 * reviewed / total:.2f}%", "cyan"),
        ("verified names", str(metrics["review"]["verified_names"]), "green"),
        ("status", "in progress", "amber"),
    ]
    widths = [(round(len(label) * 6.5 + 20), round(len(value) * 6.5 + 20)) for label, value, _ in badges]
    width = sum(left + right for left, right in widths) + 10 * (len(badges)-1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="26" viewBox="0 0 {width} 26" role="img" aria-labelledby="badges-title badges-desc">',
           '<title id="badges-title">Dreams analysis status badges</title>',
           '<desc id="badges-desc">Percentages use discovered functions, not full binary completeness. Cached pseudocode is not verified source. Status is in progress.</desc>',
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


def main(argv=None):
    repo = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", type=Path, default=repo / "analysis" / "status.json", help="Public sanitized status input; rewritten canonically")
    parser.add_argument("--output", type=Path, default=repo / "assets" / "status.svg")
    parser.add_argument("--badges-output", type=Path, default=repo / "assets" / "status-badges.svg")
    parser.add_argument("--inventory", type=Path, help="Optional local inventory: list of addresses or address objects; other fields discarded")
    parser.add_argument("--cache-index", type=Path, help="Optional local cache function-index.json; copies only address/status")
    parser.add_argument("--check", action="store_true", help="Validate canonical JSON and SVG without writing")
    args = parser.parse_args(argv)
    status = sanitize(read_json(args.status), args.inventory, args.cache_index)
    # Compact rows keep the public inventory small and reviewable; the header is pretty printed.
    header = dict(status)
    rows = header.pop("rows")
    content = json.dumps(header, indent=2)[:-2] + ',\n  "rows": [\n'
    content += ",\n".join("    " + json.dumps(row, separators=(",", ":")) for row in rows)
    content += "\n  ]\n}\n"
    svg = render(status)
    badges_svg = render_badges(status)
    if args.check:
        if (args.status.read_text(encoding="utf-8") != content or not args.output.is_file()
                or args.output.read_text(encoding="utf-8") != svg or not args.badges_output.is_file()
                or args.badges_output.read_text(encoding="utf-8") != badges_svg):
            raise SystemExit("Status assets are valid but not current; regenerate them")
        print("Status assets are valid and current")
    else:
        write_atomic(args.status, content)
        write_atomic(args.output, svg)
        write_atomic(args.badges_output, badges_svg)
        print(f"Generated public status for {len(rows):,} discovered functions")


if __name__ == "__main__":
    main()
