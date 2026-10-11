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
    "green": "#3fb950", "cyan": "#39d5ff", "blue": "#58a6ff", "gray": "#283747",
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


def legend(x, y, color, label):
    return rect(x, y-9, 8, 8, color, 1) + text(x+15, y, label, 11, "muted")


def region_tiles(items, bounds):
    x, y, width, height = bounds
    # Distribute exactly count cells across near-square rows, with no filler cells.
    count = len(items)
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


def identified_topics(applied):
    topics = defaultdict(int)
    for row in applied:
        name = row["applied_name"]
        if any(part in name for part in ("Calculator", "Splitter", "Combiner", "SignalInspector", "SignalGenerator")):
            topic = "Math and logic tools"
        elif "Fog" in name:
            topic = "Fog effects"
        elif "AutoGuides" in name:
            topic = "Object placement guides"
        elif "MagicDoor" in name:
            topic = "Doorways"
        elif any(part in name for part in ("Variant", "GadgetName", "CanvasProperties", "PosProperties")):
            topic = "Shared object data"
        else:
            topic = "Other code"
        topics[topic] += 1
    return sorted(topics.items(), key=lambda item: (-item[1], item[0]))


def render(status, applied):
    total = status["inventory_total"]
    review = status["metrics"]["review"]
    assert len(applied) == review["verified_names"]
    assert {r["address"] for r in applied} == {r["address"] for r in status["rows"] if r["review"] == "verified_name"}
    priority = {"verified_name": 0, "deferred": 1, "unreviewed": 2}
    rows = sorted(status["rows"], key=lambda r: (priority[r["review"]], int(r["address"], 16)))
    topics = identified_topics(applied)
    percent = 100 * review["verified_names"] / total
    title = f'{review["verified_names"]:,} functions named and checked'
    description = (f'Early-stage Dreams research. {title} out of {total:,} code functions found so far. '
                   f'{review["deferred"]:,} reviewed functions still need an explanation; {review["unreviewed"]:,} have not been reviewed. '
                   'Each square is one piece of code. Computer-generated code does not count as identified.')
    height = max(485, 175 + len(topics) * 55)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{height}" viewBox="0 0 1120 {height}" role="img" aria-labelledby="status-title status-desc">',
           f'<title id="status-title">Dreams: {escape(title)}</title>',
           f'<desc id="status-desc">{escape(description)}</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
           rect(0, 0, 1120, height, "background"),
           text(12, 31, title, 25, "text", 650),
           text(1108, 30, "EARLY STAGE", 13, "amber", 650, ' text-anchor="end"'),
           text(12, 56, f'{percent:.2f}% of the {total:,} code functions found so far', 15, "muted"),
           text(12, 94, "Most code still needs review", 17, "text", 600),
           region_tiles(rows, (12, 111, 732, 300)),
           text(774, 94, "What we have identified", 17, "text", 600),
           text(774, 115, "Parts of these systems — work is ongoing", 12, "muted")]
    for index, (topic, count) in enumerate(topics):
        y = 135 + index * 55
        out.extend([rect(774, y, 334, 46, "panel", 5, "border"),
                    text(786, y + 19, topic, 14, "text", 600),
                    text(786, y + 37, f'{count} function' + ('s' if count != 1 else '') + ' named and checked', 12, "muted")])
    out.extend([legend(12, 436, "green", f'Named and checked: {review["verified_names"]:,}'),
                legend(256, 436, "amber", f'Still unclear: {review["deferred"]:,}'),
                legend(460, 436, "accounted", f'Not reviewed: {review["unreviewed"]:,}'),
                text(12, 460, 'Each square is one function (a piece of code). Generated code still needs someone to work out what it does.', 12, "muted"),
                text(12, 479, 'This tracks the functions found so far. It is not a percentage of the whole game rebuilt or fully understood.', 11, "dim"),
                '</g></svg>'])
    return "\n".join(out) + "\n"


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    decomp = metrics["decompilation"]
    reviewed = metrics["review"]["reviewed"]
    badges = [
        ("checked", f"{reviewed:,} / {total:,}", "accounted"),
        ("identified", str(metrics["review"]["verified_names"]), "green"),
        ("ready to review", f"{decomp['complete']:,}", "blue"),
        ("status", "in progress", "amber"),
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
    svg = render(status, read_json(repo / "analysis" / "function-review.json")["applied"])
    badges_svg = render_badges(status)
    readme_path = repo / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    expected_readme = readme
    for name, asset in (('status.svg', svg), ('status-badges.svg', badges_svg)):
        version = hashlib.sha256(asset.encode('utf-8')).hexdigest()[:12]
        pattern = r'\]\(assets/' + re.escape(name) + r'(?:\?v=[a-zA-Z0-9_-]+)?\)'
        expected_readme, count = re.subn(pattern, f'](assets/{name}?v={version})', expected_readme)
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
