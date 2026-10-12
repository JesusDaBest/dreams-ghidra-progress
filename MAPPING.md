# Code-to-system mapping

The front-page map groups actual function addresses by the part of Dreams they support. Its input is [system-map.json](analysis/system-map.json). The map currently contains 1,560 functions across nine systems; another 7,991 discovered functions still need classification and are counted below the map.

Mapping establishes a function's association with a system. The independent [review ledger](analysis/function-review.json) determines whether its name has been checked. The mapping pass itself added no checked names. Subsequent naming reviews bring the total to 63 checked names, of which 57 are in this map; 4 remain reviewed but unresolved.

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

- Each function appears once in its evidenced system and component. A single 64-column square lattice holds all 1,560 mapped functions without empty slots. All cells have identical width and height. Hierarchical sections partition those cells in proportion to their actual counts; boundaries can be stepped rather than stretching cells. Main system names overlay cells at 15 pixels, component names at 14 pixels, and counts at 12 pixels. Contiguous recursive partitions keep sibling components together on the lattice. Small internal units share their labeled parent when a readable label would not fit; the evidence hierarchy is unchanged.
- Sculpting and painting includes CSG, sprites, and sculpt property code. Rendering includes draw routines, lighting, and graphics infrastructure. Physics includes collision and ray-query code.
- Gadget object schemas and their related property routines stay in Gadgets & logic, including motion, camera, signal, and sound gadget settings. Core audio and animation data have separate sections.
- Editor & interface covers editing tools, UI, and interaction data. Dreamiverse & networking covers creation browsing and multiplayer/network data. Shared engine & object data covers common objects, serialization, and support routines.
- Green identifies reviewed behavior/helpers; blue identifies reviewed property/type registration. Both require independently checked names from the review ledger. Amber means reviewed but unresolved; gray means not yet reviewed. Cached pseudocode does not make a cell green.
- Section labels show checked names divided by identified functions. The adjacent table separately counts runtime/helper review and property/type review; no subsystem completion percentage is displayed. The total code size of each system is still unknown. Counts can grow or assignments can be corrected as research finds more evidence.

These are research classifications, not a recovered source-module layout or a measure of game-system complexity. Unclassified functions remain in the full inventory and are reported separately below the map.

## Components within each system

The map now retains the code-unit boundaries inside each system rather than combining every function into one system-wide grid. Components use exact registered type identities and implementation-file evidence already supporting those functions. Type identities are grouped under readable categories such as logic and signals, sensors, sculpt geometry, paint strokes, and collision queries. These category names are research organization, not recovered original source directories.

Every assignment records its `component_path` and `component_basis`. The hierarchy is system → subsystem → native component → code role: a component appears once, with runtime and property code grouped beneath it rather than repeating the component under separate analysis stages. A function supported by multiple components stays in their common parent; it is not duplicated or forced into one child. Shared property helpers retain their shared ownership. The graph retains the major system and component hierarchy. Readable internal units such as Sculpt bricks, Chunk, Sun Shadow, and Spot Shadow remain nested inside their parent components. Small units remain within a labeled parent section rather than receiving tiny abbreviated labels or separate unlabeled outlines. The expanded tree retains every full component and code-unit name and its exact checked/identified count. There are no display-only Other categories.

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

### CSG record rebuilding and shared page finalization

Four descriptive names now survive saving and reopening: `InitializePackedCSGRecordWriter`, `RebuildPackedCSGRecordsWithMetadataOffset`, `FinalizePackedResourceTreeWriter`, and `ReleasePackedResourcePage`. The initializer explicitly selects native storage category 1, labeled CSG by allocator diagnostics. This supports mapping the initializer, rebuilding, append/delta helpers and category-specific summary to Sculpt geometry / CSG record storage. Shared finalization and page release remain under Shared engine / Resource pages. Seven previously unmapped functions now have supported associations; no address is counted twice.

The rebuilding function copies each decoded record, offsets its signed metadata byte, applies a signed lower bound and caps at 127 before appending. The metadata's gameplay meaning is unresolved. Finalization canonicalizes the active tree path from leaf to root, refreshes CSG summaries, updates parent child links and returns the root index; an empty leaf is released and returns the invalid-index sentinel. Page release clears 512 bytes, atomically clears allocation/reference bitmap bits and removes its fingerprint entry with backward shifting. Synchronization helper semantics, fingerprint collisions, invalid inputs and allocation-failure behavior remain unresolved.

All four complete native bodies were read and matched against live bytes before naming. The reopened full inventory matches the baseline plus journaled changes; original archive hashes remain unchanged. There are 116 checked descriptive names among 9,552 discovered functions. This adds no full-behavior completion credit and does not establish a whole-game completion percentage. Raw code and private project data remain local.

### Resource roots and page collection

Three more descriptive names are saved and verified after reopening: `MarkObjectPackedResourceRoots`, `MarkContainerPackedResourceRoots`, and `MarkPackedResourceTreeReachable`. These shared helpers mark resource-page IDs from object-kind-specific fields, visit container roots serially or through jobs of up to 256 objects, and recursively mark tree children. Object-kind names remain unresolved; field offsets alone are not treated as semantic type names.

The collector body has been read but remains an undefined function region in the project. It clears a reachability bitmap, marks referenced trees, and sweeps allocated unmarked pages after rechecking allocation and current references under the resource mutex. Its completion word is a participant bitmask: the inspected coordinator publishes roots and atomically sets bits; collection waits for the combined mask `0x7fff`. The wait import is confirmed as `scePthreadCondWait` by exact symbol-ID calculation and loader binding. Mutex lock, unlock and thread-ID imports are also confirmed. Canonicalization unlocks before calling page release; that path does not require recursive locking.

These findings do not prove root completeness, runtime synchronization, allocation-failure handling or collector correctness. Other completion-mask participants, imported implementations and sound-data references still need tracing. There are 119 checked descriptive names among 9,552 discovered functions. Full-behavior coverage is unchanged. Raw native code and detailed local evidence are not published.

### Keyed-resource lookup and eviction

Four descriptive names now persist after reopening: `TouchKeyedResourceLastUseCounter`, `CopyKeyedResourceDescriptorOrDefault`, `QueryKeyedResourceMetadataWithFallback`, and `EvictOldestEligibleKeyedResource`. Complete native bodies were reviewed and matched to live bytes before the name-only edits. Initialization confirms that fixed descriptor storage and the lookup table pointer refer to the same 8,192-slot table.

The touch helper refreshes an existing key's last-use counter under a separate mutex. Descriptor lookup refreshes the counter and returns a descriptor or an initialized default. Metadata lookup can use a fallback key; the packed fields' gameplay meanings remain unresolved. Eviction selects the strictly oldest occupied entry and rejects it if its timestamp is newer than the previous resource-collection cycle. It clears associated allocation records, removes the table entry with backward shifting, invokes an optional callback and decrements the used count. The eviction helper has no mutex calls of its own; caller protection must be established.

Sound resource leaves use the touch helper, but that does not establish audio-exclusive ownership. Payload meaning, callback effects, counter wrap, malformed descriptors and runtime synchronization remain unresolved. The saved-project inventory matches the recorded edits and original archives remain unchanged. There are 123 checked descriptive names among 9,552 discovered functions; full-behavior coverage is unchanged. Raw code and private project data remain local.

### Keyed-resource block allocation

Three further descriptive names are verified after reopening: `FindBestFitKeyedResourceBlockRun`, `AllocateKeyedResourceBlocksWithEviction`, and `AllocateKeyedResourceBlocks`. The finder selects the smallest suitable contiguous free run in a 16,384-block bitmap. The allocator retries after eligible-resource eviction, marks the allocated range and initializes its 16-byte auxiliary records. The wrapper supplies mutex protection.

Native review of the paired serialization callbacks confirms that each block has 16-byte and 128-byte auxiliary records. All three discovered registration call sites transfer a 56-byte descriptor by value on the stack, although registration copies only 49 meaningful bytes into a new table entry. This distinction prevents an incorrect pointer prototype or argument size. Auxiliary record contents and several descriptor fields remain unresolved; no speculative type changes were applied.

A nonpositive allocation request can reach eviction before failure, so it must not be assumed side-effect free. Malformed sizes, runtime concurrency and the remaining allocation caller need further review. There are now 126 checked descriptive names among 9,552 discovered functions. Full-behavior coverage is unchanged; original archives remain unchanged and raw code stays local.

### Audio file import

Two descriptive names are verified after reopening: `InitializeAudioFileImportContext` and `ProcessAudioFileImportContext`. Native review traces RIFF/WAVE parsing, accepted PCM restrictions, buffered processing, peak-envelope generation, keyed-resource registration and cleanup. The encoder thunk is identified as `sceAt9EncEncode` by its exact symbol-name NID and loader binding.

The peak data also has scalar-evaluation and selection/normalization consumer leads; those cached-code findings still require native and caller verification. The alternate input format, several context fields and runtime behavior remain unresolved. No speculative prototypes were applied. These are checked function roles, not completed audio features or recovered original source.

There are 128 checked descriptive names among 9,552 discovered functions. Original archives remain unchanged; raw code stays local. Full-behavior coverage is unchanged.

### Audio playback positioning

`ComputeAudioPlaybackSamplePosition` is verified after reopening. All 113 native instructions were reviewed and matched to current project bytes. The function converts signed playback rate and time to a sample position at a 48,000-sample scale, handles reversed selection, and applies wrapping or alternating-direction loops. Exact loader bindings identify `exp2f` and `log2f`; the gated pitch conversion clamps semitones to -72 through 72 before converting to a rate multiplier.

The associated 110-instruction control wrapper was also read, but has not been renamed. Object-field names, caller invariants and the positive-domain invariant for the logarithm remain unresolved. No parameter types or calling conventions were changed, and runtime correctness is not claimed. There are now 129 checked descriptive names among 9,552 discovered functions; full-behavior coverage is unchanged.

### Sound controls and playback modes

`EvaluateSoundPlaybackPositionFromControls` is verified after reopening. Its complete 110-instruction native body normalizes packed controls and tail-calls the verified sample-position helper. Native caller tracing resolves a 16-byte object-base adjustment. Field registration and current string bytes confirm `PlaybackSpeed`, `EnableSoundGranular` and `SlicePlaybackMode` in the Sound layout.

The registered playback enum is `PLAYONCE=0`, `SUSTAIN=1`, `LOOP=2`, `PINGPONG=3`, with `LAST=4` as a sentinel. The sample-position helper wraps LOOP and alternates direction for PINGPONG. Its unsigned mode comparison also permits the sentinel and higher malformed values into wrapping; enum validation and whole-system mode behavior have not been established. Remaining packed-control names and caller range invariants are unresolved. No speculative prototypes were applied.

There are 130 checked descriptive names among 9,552 discovered functions. These static role checks do not establish complete audio features or runtime correctness. Full-behavior coverage remains unchanged.

### Sound playback-envelope amplitude

`ComputeSoundPlaybackEnvelopeAmplitude` is verified after reopening. Its complete 218-instruction native body was read and matched to current project bytes. Registered Sound labels identify Volume, Power, Spiciness and VolumeADSR01. The function obtains playback position through the verified control wrapper, returns zero outside selection bounds, and combines signed Volume, conditionally squared Power, envelope timing and squared interpolated resource peak data. The direct caller uses its returned scalar.

The result can be signed; it is not simply a nonnegative magnitude. Packed event semantics, conditional Power gates and caller range invariants remain unresolved. No speculative prototypes or runtime correctness claims were added. There are now 131 checked descriptive names among 9,552 discovered functions; full-behavior coverage is unchanged.

### Sound sample-record selection

`SelectSoundSampleRecordByPlaybackExtent` and `SelectSoundSampleRecordByTag` are verified after reopening. Their complete native bodies (131 and 132 instructions) were read and compared with current program bytes. Both traverse packed resource-tree leaves containing 40-byte sample records. The registered Sound field SausagePage supplies the root. The caller uses the tag selector when LocalisedSound is enabled and the extent selector otherwise; both paths converge before playback-envelope evaluation.

The extent selector compares selection end minus selection start, using a different end field for LOOP/PINGPONG. This is not simply loop length. The tag selector returns an exact match first, then a preferred-tag match, then a zero-tag match, then the first record, with a default record when none is available. Preferred tag 3 is remapped to 1. Tag meanings remain unresolved; the LocalisedSound label alone does not establish language or channel semantics. No speculative types or runtime correctness claims were added.

There are now 133 checked descriptive names among 9,552 discovered functions. Full-behavior coverage is unchanged.

### Sound sample records and hue initialization

`CopySoundSampleRecordsFromResourceTree` and `ComputeSoundHueFromSampleKey` are verified after reopening. Their complete native bodies (159 and 32 instructions) were read and checked against current program bytes. The copier writes 40-byte records either in traversal order with a 64-record limit, or into slots selected by six bits in each record. Indexed mode counts encountered records; repeated slots can overwrite earlier records. A game-update caller uses indexed mode with a preinitialized 64-record destination.

The hue helper derives a byte from the selected sample's key using floating-point scaling and fractional extraction, then clamps it to 1–254. Both direct callers fill the registered SoundHue field only when it is zero. This is sound appearance initialization, not additional playback or runtime-correctness verification. Slot meanings and all caller invariants remain unresolved; no speculative types were added.

There are now 135 checked descriptive names among 9,552 discovered functions. Full-behavior coverage is unchanged.

### Playback sample index selection

`SelectSoundPlaybackSampleIndex` is verified after reopening. All 791 native instructions were read and matched against current program bytes. The routine filters nonzero sample records by Slice slot range and tag preference, compares two record control bytes, applies registered solo/disabled sample masks, and selects a record index using cumulative distance weights. Optional availability checks use resource metadata under the resource mutex. With history enabled, a hash table tracks prior choices and can exclude a recent candidate.

All three direct caller neighborhoods were inspected. The recorded count sources come from sequential sample-record copying, which caps output at 64 records. One call supplies a zero selection fraction and bypasses history; two generate a fraction from PRNG state. Floating-point rounding can reach 1.0, so the native index-zero fallback remains relevant. Complete caller invariants, some control-field meanings, hash collisions and concurrent history access remain unresolved. No runtime correctness, speculative type or full-behavior credit was added.

There are now 136 checked descriptive names among 9,552 discovered functions. Full-behavior coverage is unchanged.

### Main game-update worker

`ProcessMainThingUpdateWorker` is now defined and verified after reopening. All 382 native instructions were inspected. The callback is dispatched by the main update loop; it atomically claims object work, checks dependency completion, calls the per-object update routine, and marks completed work. Its thread-local getter and setter imports were identified through exact symbol-name hashes and executable loader references.

An isolated project trial established the nonoverlapping boundary and the two input registers before the backed-up main project was changed. The complete function inventory matches the change journal, and original archive hashes remain unchanged. Concrete context types, the return contract, concurrency invariants and old/new state ownership remain unresolved. No full-behavior completion credit was added.

There are now 137 checked descriptive names among 9,553 discovered functions. Defining this previously unrecognized function increases the discovered inventory by one; it does not enlarge the executable or mean the game is fully understood.

### Update buffer lanes and tagged records

Three helpers are verified after reopening: `AcquireLeastUsedThreadBufferLane`, `GetCurrentThreadBufferWritePointer`, and `AppendSizedRecordToThreadBuffer`. Their complete native bodies contain 82, 19 and 103 instructions respectively, all matched against current executable bytes before naming.

The buffer arena has a shared mode and six contiguous thread lanes. The selector atomically claims the least-used available lane and records its index in thread-local storage. The pointer helper returns that lane's base plus used bytes. The append helper reserves a tagged, size-table-driven payload and writes a terminating sentinel, enforcing the selected mode's capacity. Descriptor initialization and the main worker's release path were inspected, together with all 15 direct append call neighborhoods.

Exhaustion, nested caller behavior and concurrency invariants remain unresolved. These are descriptive analyst names; no additional types, runtime validation or full-behavior completion credit were added. There are now 140 checked descriptive names among 9,553 discovered functions.
