# Code-to-system mapping

The front-page map groups actual function addresses by the part of Dreams they support. Its input is [system-map.json](analysis/system-map.json). The map currently contains 1,554 functions across nine systems; another 7,997 discovered functions still need classification and are counted below the map.

Mapping establishes a function's association with a system. The independent [review ledger](analysis/function-review.json) determines whether its name has been checked. The mapping pass itself added no checked names. Subsequent naming reviews bring the total to 56 checked names, of which 50 are in this map; 4 remain reviewed but unresolved.

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

- Each function appears once in its evidenced system and component. A single 50-column square lattice holds all 1,554 mapped functions without empty slots. All cells have identical width and height. Hierarchical sections partition those cells in proportion to their actual counts; boundaries can be stepped rather than stretching cells. Labels overlay cells at 12 pixels or larger. Small internal units share their labeled parent when a readable label would not fit; the evidence hierarchy is unchanged.
- Sculpting and painting includes CSG, sprites, and sculpt property code. Rendering includes draw routines, lighting, and graphics infrastructure. Physics includes collision and ray-query code.
- Gadget object schemas and their related property routines stay in Gadgets & logic, including motion, camera, signal, and sound gadget settings. Core audio and animation data have separate sections.
- Editor & interface covers editing tools, UI, and interaction data. Dreamiverse & networking covers creation browsing and multiplayer/network data. Shared engine & object data covers common objects, serialization, and support routines.
- Green identifies reviewed behavior/helpers; blue identifies reviewed property/type registration. Both require independently checked names from the review ledger. Amber means reviewed but unresolved; gray means not yet reviewed. Cached pseudocode does not make a cell green.
- Section labels show checked names divided by mapped functions; no subsystem completion percentage is displayed. The total code size of each system is still unknown. Counts can grow or assignments can be corrected as research finds more evidence.

These are research classifications, not a recovered source-module layout or a measure of game-system complexity. Unclassified functions remain in the full inventory and are reported separately below the map.

## Components within each system

The map now retains the code-unit boundaries inside each system rather than combining every function into one system-wide grid. Components use exact registered type identities and implementation-file evidence already supporting those functions. Type identities are grouped under readable categories such as logic and signals, sensors, sculpt geometry, paint strokes, and collision queries. These category names are research organization, not recovered original source directories.

Every assignment records its `component_path` and `component_basis`. A function supported by multiple components stays in their common parent; it is not duplicated or forced into one child. Shared property helpers retain their shared ownership. The graph retains the major system and component hierarchy. Readable internal units such as Sculpt bricks, Chunk, Sun Shadow, and Spot Shadow remain nested inside their parent components. Small units remain within a labeled parent section rather than receiving tiny abbreviated labels or separate unlabeled outlines. The expanded tree retains every full component and code-unit name and its exact checked/identified count. There are no display-only Other categories.

Green is assigned to the checked functions inside their own units and totals are then added to the parent components and systems. Discovering a type, matching a source reference, or generating pseudocode does not turn its functions green. No new reviewed functions or larger system totals were invented for this change.

## Verification and reproduction

The mapping used an immutable program snapshot. Its native memory, body boundaries, and type evidence remain unchanged in v2; the latest saved-project audit confirms that continuity. Current extraction status now comes from the separately audited v2 cache. All 9,551 function addresses and body sizes were matched to its exported native references, and all 9,508 available pseudocode files passed their recorded SHA-256 checks. The snapshot's modification time was unchanged. The program identity, evidence digests, instruction addresses, descriptor addresses, and applicable cache hashes are recorded in the public mapping metadata. Evidence JSON digests use UTF-8 text with LF newlines.

Public evidence contains identifiers and structural links; local paths, raw strings from source-file diagnostics, game code, binaries, and Ghidra databases remain outside the repository. A researcher with the same program can follow the recorded addresses. The private source evidence is required to independently re-establish the mapping; rendering the existing map requires only the public JSON files.

Regenerate the front-page assets with `python scripts/generate_status.py`, then validate them with `python scripts/generate_status.py --check`. Ownership comes from the mapping file; review colors come from the status rows. Changing a review state cannot move a function into a different system.

## Verified status map update

Mapped seven independently reviewed functions to their confirmed gadget types: Reporter Sculpt, Reporter Telemetry, Wireless Receiver, Wireless Transmitter and Variable Gadget. The map now contains 1,547 functions, with 43 checked, 4 unresolved and 1,500 awaiting review. Six other checked functions remain outside the map pending supported ownership. Equal square cells now support arbitrary mapped counts; no invented functions pad the last row. Counts measure identified code, not full subsystem completion.

## One feature, one progress group

Timeline definition and playback-associated code share one Timeline group; Grade definition and color-processing-associated code share one Grade group. Source associations remain recorded per function. These presentation groups do not claim exclusive engine ownership. Each function address occurs once in the map, and parent totals include their children rather than adding another copy.



The hierarchy separates property/type definitions, runtime/implementation, and unresolved code roles inside existing feature associations. This split does not change system ownership. Review counts distinguish behavior/helpers from property/type handling. Neither count establishes whole-feature completion; no such percentage is exported.
