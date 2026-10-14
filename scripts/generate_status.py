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


def packed_regions(entries, bounds, preserve_order=False):
    """Area is proportional ONLY to the number of real functions in each group."""
    entries = [item for item in entries if item[3]]
    if not preserve_order:
        entries.sort(key=lambda item: (-len(item[3]), item[0]))
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



def hierarchy_rows(rows, mapping):
    """Build and validate the nested inventory independently of review status."""
    by_address = {row['address']: row for row in rows}
    paths = {}
    def build(nodes, prefix=()):
        result = []
        seen = set()
        for node in nodes:
            key, label = node['id'], node['label']
            if key in seen or not re.fullmatch(r'[a-z0-9-]+', key):
                raise ValueError('Hierarchy node IDs must be unique within their parent')
            seen.add(key)
            path = prefix + (key,)
            paths[path] = node
            children = build(node['children'], path)
            selected = [dict(by_address[a],code_role=item.get('code_role','role-unresolved')) for a,item in mapping['assignments'].items()
                        if tuple(item['component_path'][:len(path)]) == path]
            direct = [by_address[a] for a,item in mapping['assignments'].items()
                      if tuple(item['component_path']) == path]
            if direct and children:
                raise ValueError('Functions must have a leaf component path')
            result.append({'id':key,'label':label,'path':path,'children':children,
                           'rows':sorted(selected,key=lambda r:int(r['address'],16))})
        return result
    tree = build(mapping['hierarchy'])
    for addr,item in mapping['assignments'].items():
        path = tuple(item['component_path'])
        if addr not in by_address or path not in paths or path[0] != item['system']:
            raise ValueError('Invalid component path or system ownership')
        if paths[path]['children']:
            raise ValueError('Assigned component must be a leaf')
    if {node['id']:node['label'] for node in tree} != mapping['systems']:
        raise ValueError('Hierarchy roots must match the major systems')
    return tree


def render_hierarchy(nodes, bounds, depth=0):
    """Partition a single square lattice: no stretched cells or empty slots."""
    x0,y0,width,height=bounds
    count=sum(len(n['rows']) for n in nodes)
    columns=52
    # Preserve equal squares for arbitrary evidence-backed inventory sizes.
    # A partial final row contains no fake functions or completion padding.
    grid_rows=math.ceil(count/columns)
    side=min(width/columns,height/grid_rows)
    cells={(i%columns,i//columns) for i in range(count)}
    regions=[];out=[]
    def divide(items,positions):
        # Keep child inventories in contiguous horizontal strips so each part
        # has room for a readable name and count.
        if len(items)==1:return [(items[0],positions)]
        width=max(x for x,y in positions)-min(x for x,y in positions)+1
        height=max(y for x,y in positions)-min(y for x,y in positions)+1
        total=len(positions);running=0;choices=[]
        for cut in range(1,len(items)):
            running+=len(items[cut-1]['rows'])
            choices.append((abs(total-2*running),cut,running))
        _,cut,amount=min(choices)
        vertical=width>height
        ordered=sorted(positions,key=(lambda p:(p[0],p[1])) if vertical else (lambda p:(p[1],p[0])))
        first=set(ordered[:amount]);second=positions-first
        return divide(items[:cut],first)+divide(items[cut:],second)
    def draw(items,positions,level):
        items=sorted((n for n in items if n['rows']),key=lambda n:(-len(n['rows']),n['id']))
        partitions=divide(items,positions)
        for node,owned in partitions:
            regions.append((node,owned,level))
            attr=f'data-area="{node["id"]}"' if level==0 else f'data-component="{"/".join(node["path"])}"'
            out.append(f'<g {attr} data-depth="{level}" data-count="{len(owned)}"><title>{escape(node["label"])}</title>')
            # Keep small code units in their named component; the full tree remains below.
            children=[c for c in node['children'] if c['rows']]
            if children and (level==0 or (len(owned)>=60 and any(len(c['rows'])>=15 for c in children))):
                draw(children,owned,level+1)
            else:
                priority={'verified_name':0,'deferred':1,'unreviewed':2}
                colors={'verified_name':'green','deferred':'amber','unreviewed':'gray'}
                rows=sorted(node['rows'],key=lambda r:(priority[r['review']],int(r['address'],16)))
                for row,(gx,gy) in zip(rows,sorted(owned,key=lambda p:(p[1],p[0]))):
                    scope=row.get('reviewed_scope','unreviewed')
                    color=colors[row['review']]
                    out.append(f'<rect data-function="{row["address"]}" data-status="{row["review"]}" data-reviewed-scope="{scope}" x="{x0+gx*side:.6f}" y="{y0+gy*side:.6f}" width="{side:.6f}" height="{side:.6f}" fill="{COLORS[color]}" stroke="#0d1117" stroke-width="0.6"/>')
            out.append('</g>')
    draw(nodes,cells,depth)
    # Draw section outlines along lattice edges, including stepped boundaries.
    borders=[]
    for node,owned,level in reversed(regions):
        edges=[]
        for gx,gy in owned:
            x=x0+gx*side;y=y0+gy*side
            for neighbor,edge in [((gx-1,gy),(x,y,x,y+side)),((gx+1,gy),(x+side,y,x+side,y+side)),((gx,gy-1),(x,y,x+side,y)),((gx,gy+1),(x,y+side,x+side,y+side))]:
                if neighbor not in owned:
                    ax,ay,bx,by=edge;edges.append(f'M{ax:.4f},{ay:.4f}L{bx:.4f},{by:.4f}')
        borders.append((node['path'],f'<path data-region-border="true" d="{" ".join(edges)}" fill="none" stroke="{"#c9d1d9" if level==0 else "#97a8bc"}" stroke-width="{2.8 if level==0 else 1.4}"/>'))
    labels=[];labeled=set();occupied=[]
    def overlaps(a,b):
        return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
    # Preserve existing placements, then retry missing labels against stepped
    # line footprints without moving a heading that already fits.
    pending=[(*region,False) for region in sorted(regions,key=lambda r:(r[2],-len(r[1]),r[0]['path']))]
    for node,owned,level,stepped in pending:
        if node['id'] in {'properties-types','runtime-implementation','role-unresolved'}:continue
        if level>0 and len(owned)<5:continue
        checked=sum(r['review']=='verified_name' for r in node['rows'])
        size=15 if level==0 else 14
        placed=None;root_placements=[]
        # Major headings belong at the start of their own section. Children
        # find room below them rather than displacing the parent into the middle.
        for wrap in range(32,8,-1):
            lines=textwrap.wrap(f"{node['label']}  {checked}/{len(owned)}",width=wrap,break_long_words=False)
            values=lines; sizes=[size]*len(lines)
            bw=max(len(line)*fs*.58 for line,fs in zip(values,sizes))+4
            bh=sum(fs+2 for fs in sizes)
            candidates=[]
            for gx,gy in sorted(owned,key=lambda p:(p[1],p[0])):
                tx=x0+gx*side+2;ty=y0+gy*side+1
                box=(tx,ty,bw,bh)
                if not stepped:
                    covered={(cx,cy) for cy in range(gy,math.ceil((ty+bh-y0)/side)) for cx in range(gx,math.ceil((tx+bw-x0)/side))}
                    if not covered<=owned or any(overlaps(box,b) for b in occupied):continue
                # A short line can fit the narrower part of a stepped section.
                # Check each line's footprint instead of the widest line's box.
                line_boxes=[];line_y=ty
                for line,fs in zip(values,sizes):
                    line_box=(tx,line_y,len(line)*fs*.58+4,fs+2)
                    covered={(cx,cy) for cy in range(math.floor((line_y-y0)/side),math.ceil((line_y+fs+2-y0)/side)) for cx in range(gx,math.ceil((tx+line_box[2]-x0)/side))}
                    if not covered<=owned or any(overlaps(line_box,b) for b in occupied):break
                    line_boxes.append(line_box);line_y+=fs+2
                if len(line_boxes)==len(values):
                    candidates.append((0,box,line_boxes))
            if candidates:
                _,box,line_boxes=min(candidates,key=lambda item:item[0])
                placed=(box,values,sizes,line_boxes)
                if level==0:root_placements.append(placed)
            if placed and level>0:break
        if root_placements:
            placed=min(root_placements,key=lambda p:(p[0][1],p[0][0],p[0][3]))
        if placed is None:
            if not stepped:pending.append((node,owned,level,True))
            continue
        (tx,ty,bw,bh),values,sizes,line_boxes=placed
        occupied.extend(line_boxes if stepped else [(tx,ty,bw,bh)]);labeled.add(node['path'])
        labels.append(f'<g data-label="{"/".join(node["path"])}" data-label-box="{tx:.6f},{ty:.6f},{bw:.6f},{bh:.6f}">')
        baseline=ty
        for label,size,line_box in zip(values,sizes,line_boxes):
            baseline+=size
            footprint=','.join(f'{v:.6f}' for v in line_box)
            labels.append(text(round(tx,3),round(baseline,3),label,size,weight=600,extra=f' data-label-line-box="{footprint}" stroke="#0d1117" stroke-width="3" paint-order="stroke" stroke-linejoin="round"'))
            baseline+=2
        labels.append('</g>')
    out.extend(border for path,border in borders if path in labeled)
    out.extend(labels)
    return out,y0+grid_rows*side


def progress_data(status, applied, mapping):
    """Export measured done/todo groups with the same semantics as the map.

    Done means verified descriptive naming here; it does not mean implemented,
    recovered original source, or a complete game feature.
    """
    names = {row['address']: row['applied_name'] for row in applied}
    scopes = {row['address']: row['reviewed_scope'] for row in applied}
    def group(node):
        done = sorted(r['address'] for r in node['rows'] if r['review']=='verified_name')
        todo = sorted(r['address'] for r in node['rows'] if r['review']!='verified_name')
        total = len(done)+len(todo)
        return {'name':'/'.join(node['path']), 'label':node['label'],
                'done':len(done), 'todo':len(todo), 'total':total,
                'behavior_or_helpers_reviewed':sum(scopes.get(a)=='behavior_or_helper' for a in done),
                'properties_or_types_reviewed':sum(scopes.get(a)=='properties_or_type_registration' for a in done),
                'runtime_functions_identified':sum(r.get('code_role')=='runtime-implementation' for r in node['rows']),
                'property_type_functions_identified':sum(r.get('code_role')=='properties-types' for r in node['rows']),
                'code_role_unresolved':sum(r.get('code_role')=='role-unresolved' for r in node['rows']),
                'whole_feature_completion':None,
                'done_names':[names[a] for a in done],
                'todo_names':['0x'+a for a in todo],
                'done_addresses':done, 'todo_addresses':todo,
                'unresolved_addresses':sorted(r['address'] for r in node['rows'] if r['review']=='deferred'),
                'groups':[group(c) for c in sorted(node['children'],key=lambda c:(-len(c['rows']),c['id'])) if c['rows']]}
    groups=[group(n) for n in sorted(hierarchy_rows(status['rows'],mapping),key=lambda n:(-len(n['rows']),n['id'])) if n['rows']]
    done=sum(g['done'] for g in groups)
    total=sum(g['total'] for g in groups)
    return {'schema_version':1, 'snapshot_date':status['snapshot_date'],
            'meaning':'Done = function role and descriptive name checked. Totals include only functions with evidenced system assignments; full system sizes are unknown.',
            'systems':{'done':done,'todo':total-done,'total':total,
                       'behavior_or_helpers_reviewed':sum(scopes.get(a)=='behavior_or_helper' for a in mapping['assignments']),
                       'properties_or_types_reviewed':sum(scopes.get(a)=='properties_or_type_registration' for a in mapping['assignments']),
                       'whole_feature_completion':None,'groups':groups},
            'unmapped':status['inventory_total']-total}


def render(status, applied, mapping):
    total = status["inventory_total"]
    review = status["metrics"]["review"]
    assert len(applied) == review["verified_names"]
    assert {r["address"] for r in applied} == {r["address"] for r in status["rows"] if r["review"] == "verified_name"}
    scopes={r['address']:r['reviewed_scope'] for r in applied}
    rows = [dict(r,reviewed_scope=scopes.get(r['address'],'unreviewed')) for r in status["rows"]]
    assert len(rows) == total and len({row["address"] for row in rows}) == total
    areas = research_area_rows(rows, mapping)
    mapped = sum(len(items) for _, _, _, items in areas)
    unassigned = total - mapped
    mapped_review = Counter(row['review'] for _, _, _, items in areas for row in items)
    description = (f'{review["verified_names"]} of {total} function names checked. '
                   f'{mapped} functions have evidence-backed system assignments; {unassigned} functions do not. '
                   'Sections show evidence-backed associations with parts of Dreams. '
                   'Every square is a real function. All function squares share one continuous lattice. Nested section outlines identify ownership. Labels overlay their own cells; only the final row may be incomplete. '
                   'Green means an evidence-supported descriptive name checked against static code; amber means reviewed but unclear; gray means not reviewed. This does not measure runtime testing or feature completion. '
                   'Assignments are incomplete; full system totals and completion are unknown.')
    hierarchy, bottom = render_hierarchy(hierarchy_rows(rows,mapping),(0,34,1000,600))
    canvas_height=bottom+58
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{canvas_height}" viewBox="0 0 1000 {canvas_height}" role="img" aria-labelledby="status-title status-desc">',
           '<title id="status-title">Dreams function review by game system</title>',
           f'<desc id="status-desc">{escape(description)}</desc>',
           '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
           rect(0, 0, 1000, canvas_height, "background"),
           text(4, 21, f'Dreams code review | {mapped:,} mapped functions', 16),
           text(996, 21, 'Section counts = checked names / identified functions', 12, 'muted', extra=' text-anchor="end"'),
           '<g data-panel="review">']
    out.extend(hierarchy)
    out.extend(['</g>',
                legend(4, bottom+20, 'green', f'{mapped_review["verified_name"]:,} names checked against code'),
                legend(360, bottom+20, 'amber', f'{mapped_review["deferred"]:,} reviewed, still unclear'),
                legend(700, bottom+20, 'gray', f'{mapped_review["unreviewed"]:,} not reviewed')])
    out.append(text(4, bottom+45, f'Static code review only: no in-game verification claimed. {unassigned:,} functions still unmapped.', 12, 'muted'))
    out.append('</g></svg>')
    return "\n".join(out) + "\n"


def render_area_table(status, mapping):
    areas = research_area_rows(status['rows'], mapping)
    applied=read_json(Path(__file__).resolve().parent.parent/'analysis/function-review.json')['applied']
    scopes={r['address']:r['reviewed_scope'] for r in applied}
    lines = ['| Part of Dreams | Functions mapped | Runtime reviewed/identified | Properties/types reviewed/identified |',
             '| --- | ---: | ---: | ---: |']
    for area_id, title, _, rows in areas:
        checked = sum(row['review'] == 'verified_name' for row in rows)
        progress = f'{checked:,}' if rows else 'No functions mapped yet'
        behavior=sum(scopes.get(r['address'])=='behavior_or_helper' for r in rows)
        properties=sum(scopes.get(r['address'])=='properties_or_type_registration' for r in rows)
        runtime_total=sum(mapping['assignments'][r['address']].get('code_role')=='runtime-implementation' for r in rows)
        property_total=sum(mapping['assignments'][r['address']].get('code_role')=='properties-types' for r in rows)
        runtime_count=f'{behavior}/{runtime_total}' if runtime_total else 'None mapped'
        property_count=f'{properties}/{property_total}' if property_total else 'None mapped'
        lines.append(f'| {title} | {len(rows):,} | {runtime_count} | {property_count} |')
    mapped = sum(len(rows) for _,_,_,rows in areas)
    unassigned = status['inventory_total'] - mapped
    lines.extend(['', f'**{mapped:,} of {status["inventory_total"]:,} discovered functions are mapped; {unassigned:,} still need a system assignment.** '
                  'Section area counts mapped functions. Property/type reviews do not count as behavior reviews. '
                  'Whole-system coverage and completion remain unknown.'])
    lines.extend(['','<details>','<summary>Explore the systems and their components</summary>',''])
    def list_nodes(nodes,depth=0):
        for node in sorted(nodes,key=lambda n:(-len(n['rows']),n['id'])):
            if not node['rows']:
                continue
            checked=sum(r['review']=='verified_name' for r in node['rows'])
            behavior=sum(scopes.get(r['address'])=='behavior_or_helper' for r in node['rows'])
            properties=sum(scopes.get(r['address'])=='properties_or_type_registration' for r in node['rows'])
            lines.append('  '*depth+f'- **{node["label"]}** - {len(node["rows"]):,} functions identified; {behavior} behavior/helper reviews; {properties} property/type reviews')
            list_nodes(node['children'],depth+1)
    list_nodes(hierarchy_rows(status['rows'],mapping))
    lines.extend(['','</details>'])
    return '\n'.join(lines)


def render_badges(status):
    total = status["inventory_total"]
    metrics = status["metrics"]
    coverage = json.loads((Path(__file__).resolve().parent.parent / "analysis/reverse-engineering-coverage.json").read_text())
    assert coverage["understood_bytes"] == sum(r["bytes"] for r in coverage["counted_functions"])
    assert coverage["percent"] == 100 * coverage["understood_bytes"] / coverage["executable_bytes"]
    badges = [
        ("RE coverage (minimum)", f"{coverage['percent']:.4f}%", "green"),
        ("names checked", f"{100 * metrics['review']['verified_names'] / total:.2f}%", "green"),
    ]
    widths = [(round(len(label) * 6.5 + 20), round(len(value) * 6.5 + 20)) for label, value, _ in badges]
    width = sum(left + right for left, right in widths) + 10 * (len(badges)-1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" viewBox="0 0 {width} 20" role="img" aria-labelledby="badges-title badges-desc">',
           '<title id="badges-title">Dreams analysis status badges</title>',
           '<desc id="badges-desc">Minimum audited static behavior coverage of imported executable bytes, followed by separate function-name review coverage.</desc>',
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
    applied = read_json(repo / 'analysis' / 'function-review.json')['applied']
    allowed_scopes = {'behavior_or_helper', 'properties_or_type_registration'}
    invalid_scopes = [(row['address'], row.get('reviewed_scope')) for row in applied
                      if row.get('reviewed_scope') not in allowed_scopes]
    if invalid_scopes:
        raise ValueError(f'Unrecognized review scopes would omit subtotal credit: {invalid_scopes}')
    progress_path = repo / 'progress.json'
    progress_content = json.dumps(progress_data(status, applied, mapping), indent=2) + '\n'
    svg = render(status, applied, mapping)
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
                or readme != expected_readme
                or not progress_path.is_file() or progress_path.read_text(encoding="utf-8") != progress_content):
            raise SystemExit("Status assets are valid but not current; regenerate them")
        print("Status assets are valid and current")
    else:
        write_atomic(progress_path, progress_content)
        write_atomic(args.status, content)
        write_atomic(args.output, svg)
        write_atomic(args.badges_output, badges_svg)
        write_atomic(readme_path, expected_readme)
        print(f"Generated public status for {len(rows):,} discovered functions")


if __name__ == "__main__":
    main()



