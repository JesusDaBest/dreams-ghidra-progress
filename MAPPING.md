# Code-to-system mapping

The front-page map groups actual function addresses by the part of Dreams they support. Its input is [system-map.json](analysis/system-map.json). The map currently contains 1,540 functions across nine systems; another 8,011 discovered functions still need classification and are counted below the map.

Mapping establishes a function's association with a system. The independent [review ledger](analysis/function-review.json) determines whether its name has been checked. This mapping pass added no checked names: 27 remain checked and 4 remain reviewed but unresolved.

## Evidence used

| Evidence | What connects the function to a system |
| --- | --- |
| Source reference | An instruction in the function refers to an embedded implementation-file string from a known source family, such as CSG, sprite processing, drawing, collision, UI, or Dreamiverse. Generic header references are excluded. |
| Type registration | The function writes an explicit type-name literal and size into a specific type descriptor. Both the string reference and descriptor write are confirmed in the native instruction references. |
| Field or enum registration | The function appends to that descriptor's own field or enum array. The exact counter offset, increment, and native write are checked. Nearby globals alone are insufficient. |
| Enum registration bridge | A type initializer directly calls a wrapper which directly calls that same descriptor's enum-value builder. Both native call edges are required. |
| Object-type dispatch | Numeric values registered in the game's object-type enum are matched to the native jump table and the direct call in each branch. All 120 switch entries were resolved; 119 have a system assignment. The legacy `Key` case is left unclassified. |
| Typed wrapper | A small, directly dispatched wrapper calls a visitor whose field labels match the exact same registered type, including several labels unique to that descriptor. Field similarity alone is insufficient. |
| Recorded function review | Existing checked property clusters and the four deferred shared helpers retain the ownership supported by their review records. |

For example, object tag `1` identifies Sculpt and dispatches to `140491730`; that wrapper calls `1405160d0`, whose fields match the Sculpt descriptor. Tag `0x4a` dispatches Signal Inspector to `1404d9c10`, and tag `0x57` dispatches Puppet Controls to `1404e1cc0`. Shared field names do not override these exact type links.

Assignments are joined by function address. Function names, address proximity, a generic serialization header, and unrestricted propagation through callers or callees are not used to guess ownership. Two functions with conflicting system evidence were excluded.

## How sections are counted

- Each function appears in one section and occupies one cell. Section area is proportional to its mapped function count.
- Sculpting and painting includes CSG, sprites, and sculpt property code. Rendering includes draw routines, lighting, and graphics infrastructure. Physics includes collision and ray-query code.
- Gadget object schemas and their related property routines stay in Gadgets & logic, including motion, camera, signal, and sound gadget settings. Core audio and animation data have separate sections.
- Editor & interface covers editing tools, UI, and interaction data. Dreamiverse & networking covers creation browsing and multiplayer/network data. Shared engine & object data covers common objects, serialization, and support routines.
- Both maps use the same system layout and addresses. The extraction map uses blue for cached pseudocode, amber for extraction failures, and gray for unavailable output. The name-checking map uses green for checked names, amber for unresolved reviews, and gray for unreviewed functions. Cached pseudocode does not make a name checked.
- A percentage is checked names divided by mapped functions in that section. The total code size of each system is still unknown. Counts can grow or assignments can be corrected as research finds more evidence.

These are research classifications, not a recovered source-module layout or a measure of game-system complexity. Unclassified functions remain in the full inventory and are reported separately below the map.

## Verification and reproduction

The mapping used an immutable program snapshot. All 9,551 function addresses and body sizes were matched to its exported native references, and all 9,508 available pseudocode files passed their recorded SHA-256 checks. The snapshot's modification time was unchanged. The program identity, evidence digests, instruction addresses, descriptor addresses, and applicable cache hashes are recorded in the public mapping metadata. Evidence JSON digests use UTF-8 text with LF newlines.

Public evidence contains identifiers and structural links; local paths, raw strings from source-file diagnostics, game code, binaries, and Ghidra databases remain outside the repository. A researcher with the same program can follow the recorded addresses. The private source evidence is required to independently re-establish the mapping; rendering the existing map requires only the public JSON files.

Regenerate the front-page assets with `python scripts/generate_status.py`, then validate them with `python scripts/generate_status.py --check`. Ownership comes from the mapping file; review colors come from the status rows. Changing a review state cannot move a function into a different system.
