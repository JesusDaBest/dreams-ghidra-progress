# Progress

Status snapshot: 2026-10-11. Setup is verified; reverse engineering remains partial.

See [decompilation results and findings](ANALYSIS.md) for the consolidated analysis, including the later six-function signature promotion, the verified v2 snapshot and its completed, audited extraction, ReporterTelemetry's three applied and reopen-verified names, and the copy-only extraction experiments. The [research data](analysis/research-details.json) lists their recorded states, matched fields, and all 43 frozen-cache failure addresses. The older extraction and ABI counts below describe their specified v1 snapshot.

## Verified setup

- GhidraMCP 2.0 is available through a local, loopback-only MCP endpoint.
- The supplied Ghidra packed-program archive was imported into a persistent working project with auto-analysis disabled to preserve existing analysis.
- Function inventory, decompilation, and cross-reference queries were verified.
- Original inputs and a separate preexisting project are retained outside this progress repository.
- All applied names persisted after a clean service stop and reopening of the saved project. The supplied original archive and its imported input copy retained their original hashes.

## Baseline inventory

| Category | Count |
| --- | ---: |
| Functions in starting inventory | 9,551 |
| Default `FUN_` names | 9,395 |
| Other names | 156 |

The 156 other names include existing annotations or symbols; they are not 156 independently verified findings from this work. Inventory size does not establish complete function discovery or decompilation coverage.

After a clean stop and reopening, a fresh complete paginated inventory confirmed 9,551 functions, 9,365 default `FUN_` names, and 186 other names. Every address and name matches the baseline plus the journaled renames. The baseline above remains unchanged.

## Documented naming batches

34 previously unnamed functions have documented review outcomes: 30 descriptive names applied and verified after reopening, and 4 deferred. The local journal retains each original name and supporting evidence.

| Address | Original name | Applied name | Recorded state |
| --- | --- | --- | --- |
| `1404d7ef0` | `FUN_1404d7ef0` | `VisitCalculatorProperties` | Verified after reopening |
| `1404d6660` | `FUN_1404d6660` | `VisitFogProperties` | Verified after reopening |
| `1404f68b0` | `FUN_1404f68b0` | `VisitPosProperties` | Verified after reopening |
| `1404f7a20` | `FUN_1404f7a20` | `VisitCanvasProperties` | Verified after reopening |
| `1404f70b0` | `FUN_1404f70b0` | `VisitVariantProperties` | Verified after reopening |
| `1404f8350` | `FUN_1404f8350` | `VisitGadgetNameProperties` | Verified after reopening |
| `140cfda40` | `FUN_140cfda40` | `RegisterVariantFieldOffset` | Verified after reopening |
| `1404d7480` | `FUN_1404d7480` | `VisitAutoGuidesGadgetProperties` | Verified after reopening |
| `1404d83d0` | `FUN_1404d83d0` | `VisitSplitterProperties` | Verified after reopening |
| `1404d87a0` | `FUN_1404d87a0` | `VisitCombinerProperties` | Verified after reopening |
| `140d6e850` | `FUN_140d6e850` | `RegisterCombinerFieldOffsets` | Verified after reopening |
| `140d57980` | `FUN_140d57980` | `RegisterCombinerTypeDescriptor` | Verified after reopening |
| `1404d8bf0` | `FUN_1404d8bf0` | `VisitMagicDoorProperties` | Verified after reopening |
| `140d6e570` | `FUN_140d6e570` | `RegisterMagicDoorFieldOffsets` | Verified after reopening |
| `140d57a50` | `FUN_140d57a50` | `RegisterMagicDoorTypeDescriptor` | Verified after reopening |
| `1404d9c10` | `FUN_1404d9c10` | `VisitSignalInspectorProperties` | Verified after reopening |
| `140d6e2b0` | `FUN_140d6e2b0` | `RegisterSignalInspectorFieldOffsets` | Verified after reopening |
| `140d57b20` | `FUN_140d57b20` | `RegisterSignalInspectorTypeDescriptor` | Verified after reopening |
| `1404da460` | `FUN_1404da460` | `VisitSignalGeneratorProperties` | Verified after reopening |
| `140d6e010` | `FUN_140d6e010` | `RegisterSignalGeneratorFieldOffsets` | Verified after reopening |
| `140d57bf0` | `FUN_140d57bf0` | `RegisterSignalGeneratorTypeDescriptor` | Verified after reopening |
| `1404dabe0` | `FUN_1404dabe0` | `VisitCameraShakerProperties` | Verified after reopening |
| `140d6ddf0` | `FUN_140d6ddf0` | `RegisterCameraShakerFieldOffsets` | Verified after reopening |
| `140d57cc0` | `FUN_140d57cc0` | `RegisterCameraShakerTypeDescriptor` | Verified after reopening |
| `1404db190` | `FUN_1404db190` | `VisitPadRumbleProperties` | Verified after reopening |
| `140d6dbd0` | `FUN_140d6dbd0` | `RegisterPadRumbleFieldOffsets` | Verified after reopening |
| `140d57d90` | `FUN_140d57d90` | `RegisterPadRumbleTypeDescriptor` | Verified after reopening |

The shared visitors are identified by matching caller offsets with field registrations, explicit type literals, and body behavior. In particular, Calculator OperandA/OperandB register as Variant and its Name field registers as GadgetName. The Combiner cluster has matching FatWireType, Name and RotationRepresentation offsets across its visitor and registration routines. The MagicDoor, SignalInspector and SignalGenerator clusters add nine names supported by explicit registered type names and 53 matching field labels and offsets. Their initializers link the Thing base descriptor; this does not mean each visitor directly visits all inherited Thing properties. CameraShaker and PadRumble add six names supported by their registered type literals and matching visitor/registration offsets. These identify property and registration routines, not the algorithms that drive camera motion or controller motors. These are analyst-assigned function names; original function symbols and complete type layouts are not claimed.

The initial eight-function review used the starting convention. The later shared-property review uses the validated PS4_SYSV correction and assembly evidence. Names, reasons, and caveats are recorded in `analysis/function-review.json`; unrelated signatures and data types were not changed in these batches.

The status data contains all 9,551 discovered addresses, with decompilation and semantic-review states tracked separately. Unreviewed functions are explicitly distinguished from reviewed-but-deferred functions.

## ReporterTelemetry naming checkpoint

Three additional descriptive names were applied with a cold project backup and reversible before/after journal records, then checked after a clean save, stop, and reopening. All 30 applied names and the complete 9,551-address inventory matched the baseline plus journaled changes. The three functions retained their prior signatures, conventions, body sizes, and namespaces.

| Address | Original name | Applied name | Recorded state |
| --- | --- | --- | --- |
| `1404de8c0` | `FUN_1404de8c0` | `VisitReporterTelemetryProperties` | Verified after reopening |
| `140d6c700` | `FUN_140d6c700` | `RegisterReporterTelemetryFieldOffsets` | Verified after reopening |
| `140d580d0` | `FUN_140d580d0` | `RegisterReporterTelemetryTypeDescriptor` | Verified after reopening |

The names identify property and metadata roles; they do not establish telemetry transmission behavior or the meaning of the unusually high visitor-state threshold. The frozen v2 extraction retains its own earlier 27-name snapshot identity.

## ABI and mapping limitation

The supplied analysis reports a Windows PE wrapper containing `.elf` sections. A sample of 1,664 code bytes matched the PS4 SELF reference with a PE address mapping offset of `0x140010000`. This is sampled evidence, not a full-binary equivalence proof.

The starting Windows calling convention was unsuitable for the embedded PS4 functions. An additive `PS4_SYSV` model was validated on a saved project copy, then applied to 9,486 game functions with unknown conventions and no saved parameters. Another 19 thunks inherit their targets' convention, giving 9,505 functions with that effective model. The 45 existing explicit signatures and the Windows wrapper were not directly reassigned.

All function names, body sizes, saved parameter names/types/storage, the symbol and datatype inventories, and memory contents were preserved. Five representative decompilations matched the validation copy after the working project reopened. Registry, label, and offset inputs now recover from RDI, RSI, and EDX where observed in assembly.

This is a calling-convention improvement, not completed signature recovery. SIMD inputs and indirect callbacks still need work. The global Windows data organization remains unchanged, so native PS4 type sizes and layouts must be independently checked. Verified descriptive names rely on explicit labels, registrations, and control-flow relationships.

## Decompilation snapshot

The immutable, validated snapshot currently records:

| Cache state | Functions |
| --- | ---: |
| Complete pseudocode cached | 9,508 |
| Decompilation failures | 43 |
| Pending | 0 |
| Total discovered | 9,551 |

All 19 thunks are included; 15 external functions are recorded separately. Cache completion does not mark a function as semantically reviewed. Failures and attempts are retained locally for deliberate retries. [The front-page status](README.md#status) is generated from sanitized address/status rows.

The completed extraction audit matched every baseline address and verified all 9,508 cached file hashes, exported metadata and final attempt states. There were 9,551 initial 20-second attempts and 67 bounded 60-second retries; 26 retries recovered output. No successful function was decompiled again in this revision. The 43 unresolved failures consist of 41 timeouts, 1 flow-limit failure, and 1 forced-merge failure; each address and attempt is retained locally.

The extraction revision is a frozen snapshot from before the latest naming batches. The working project has the verified names listed above; cached pseudocode retains its own coherent snapshot names. Coverage accounting does not imply updated pseudocode or complete function discovery.

The supplied packed-program archive and its input copy still match their pre-analysis hashes. A current whole-file hash was also recorded for the original SELF reference; no pre-analysis whole-SELF hash was available, so historical whole-file invariance is not claimed for that file.

## Next work

The first code-to-system mapping pass associated 1,540 functions with nine Dreams systems using native source-string references, registered type descriptors, field and enum builders, and the object-type dispatcher. All 120 dispatcher branches were resolved; 119 received system assignments. Four typed wrappers were linked to their exact descriptor schemas. Conflicting ownership was excluded. The remaining 8,011 functions are reported outside the system map. That mapping checkpoint added no semantic-review credit: at the time, 27 names were checked and 4 reviews remained deferred. See [mapping evidence](MAPPING.md) and the per-address [system map](analysis/system-map.json).

1. Investigate the recorded extraction failures with targeted assembly and metadata checks.
2. Review coherent clusters, beginning with calculator registration and shared property visitors.
3. Reconcile preserved explicit signatures, SIMD inputs, and indirect-call arguments with assembly evidence.
4. Journal and verify further justified changes, save checkpoints, and recheck original input hashes.

Setup, a small naming batch, and generated pseudocode do not satisfy the full reverse engineering goal.

## Final v2 extraction checkpoint

All 9,551 discovered functions are accounted for: 9,513 complete cached outputs and 38 failures (36 timeouts, one flow-limit failure, one forced-merge failure). The immutable snapshot has 9,532 code functions and 19 thunks; 15 external functions are recorded outside that denominator. All 59 initial timeouts received one 60-second retry. The audit checked all 9,513 cache hashes and all 9,610 attempt records; no previously successful output was re-decompiled.

All cached outputs also received a mechanical quality scan with a per-address local result and next step. This grants no semantic-review credit: 30 names are checked, 4 naming reviews are deferred, and 9,517 functions await semantic naming review. The 39 preserved explicit signatures and all final extraction failures have address-specific unresolved records. Original binary inputs, both caches, checkpoints, and raw evidence remain local.

## Continued semantic review: wireless and variables

Eleven more descriptive names were applied and survived a clean saved-project reopening: **41 names checked; 4 deferred; 9,506 still unreviewed**. The original archive and input copy hashes remain unchanged. This is ongoing reverse engineering; successful extraction does not complete it.

- WirelessReceiver and WirelessTransmitter: their literal type names identify separate descriptors. Each initializer links the Thing base descriptor and invokes its own field registrar. The visitors match all 16 receiver and 12 transmitter object offsets. Receiver-specific ZoneSize, ZoneOffset, FalloffSize, FalloffOffset and DetectName distinguish it from the transmitter, which has DetectScope. These are property visitors, not identified wireless signal-processing algorithms.
- VariableGadget: the descriptor, registrar and visitor agree on 20 field offsets. Explicit fields include InitialValue (+0xe8), IsMultiplayer (+0x108), IsPersistentInMap (+0x109), ForceResetVariable (+0x10a), VariableValueShouldBePreserved (+0x10f), and RestoreVariableOnLevelRewind (+0x110). Three nested fields use shared helpers without outer labels; their exact helper roles remain unresolved. The last two flags are gated by visitor state +0x1c >= 0x5ff. Actual variable update, persistence and rewind behavior still need tracing.
- ReporterSculpt: only its type-descriptor initializer and six-field registrar were named. The generic neighboring visitor is still unassigned because the type identity is not proven by adjacency.

Every new function was read as cached v2 C and checked against complete assembly and direct literal reads. Changes are names only, journaled with old names, backed up before application and verified against the complete 9,551-function inventory after reopening. No new extraction run or prototype changes were needed.

### Developer coding streams: research leads

[Media Molecule's programming-stream announcement](https://www.mediamolecule.com/blog/article/this_weeks_live_stream_the_tech_behind_the_magic) identifies Alex Evans and Mark Zarb-Adami demonstrating live code and particle features in April 2016. The official recording is [Dreams PS4 - The Tech Behind The Magic](https://www.youtube.com/watch?v=yZM_Ij9aeOA), whose description identifies wave-shader work. The recording has been located, but its frames and transcript have not yet been analyzed; it supports no function rename in this batch. Pre-release examples must be matched against this executable before treating them as implementation evidence.

Next: inspect source visible in the developer recordings, trace the wireless/variable runtime callers and nested helpers, and continue mapping verified functions to Dreams systems. Metadata registration and property visitation are only part of those systems.

## Player values and boolean player masks

Four additional descriptive names persisted after clean saved-project reopening: **45 verified names, 4 deferred, 9,502 unreviewed**. The full address/name inventory matches the baseline plus the durable rename journal; original input archive hashes are unchanged. Names-only edits were made after a cold project backup.

- `1404f9650` â€” `VisitPlayerValueProperties`: matches the explicit PlayerValue descriptor's `non_player` float at +0 and `values` at +4. Assembly visits four player floats at +4, +8, +0xc and +0x10. Modern state >=0x4ef enters a nested values scope and restores the caller's path state. The older branch instead emits legacy indexed callbacks and `valid_bits=0`. The observed state fields are not yet a recovered version enum.
- `1404f9b20` â€” `VisitPlayerValueBoolProperties`: consumes the caller's low input byte and visits `PlayerBits` through vtable+0x848. Under state +0x18 ==0 and +0x1c <=0x4ee it can also emit `valid_bits=0`. The final indirect jump is a tail callback; the decompiler's switch-table warning is not evidence of an actual switch table.
- `140d68880` â€” `RegisterPlayerValueBoolFieldOffset`: appends a field record and installs the PlayerValueBool descriptor, preserving registry/property-key/object-offset inputs from RDI/RSI/EDX.
- `140d1b1c0` â€” `RegisterPlayerValueBoolTypeDescriptor`: explicitly installs the `PlayerValueBool` literal on descriptor14586d650 and registers `PlayerBits` at byte offset0.

VariableGadget uses these helpers for VariableValue+0xf4 and its increase/decrease bytes at +0x10b/+0x10c. This establishes their property representation; the runtime update algorithms remain to be traced. Full assembly, direct NUL-terminated literal reads, cached C hashes, caller references and after-reopen names are recorded locally. No parameter or type guesses were applied.

### Coding-stream evidence now inspected

The official [Liam Live Codes Dreams recording](https://www.youtube.com/watch?v=IvGbhvZsTa8&t=1240s) was identified from Media Molecule channel metadata. Auto-captions were searched and a full-resolution source frame around 20:41 was inspected. It shows `physics_tool.cpp`, the signature `PhysicsTool::Update(SController* controller)`, a local `ThingPtr`, and a call to `GetHoveredThing(controller)`. These provide search leads for editor tools and object handles, not proven names for this later executable. The inclusion of `twitch_livecoding.h` also shows that some helpers belong to the demonstration setup. No names in this batch depend on the video. Next, cross-check relevant type and string references before claiming a binary match.

## Editor tool-name lookup

**46 names verified after reopening, 4 deferred, 9,501 unreviewed.** A cold backup preceded the names-only edit; the complete address/name inventory matches the baseline plus the rename journal, and original input archive hashes are unchanged.

`140646860` is now `GetToolTagName`. Its complete 687-instruction assembly and five directly read relative jump tables establish an integer-to-static-name lookup. Static interpretation covers all 837 IDs from 0 through 0x344: 326 named entries and 511 `notag` results. Two out-of-range representatives also return `notag`. A direct caller uses the resulting string under `tool_tag`; another compares it against input text. This establishes editor tag naming, not how the tools execute during gameplay. Object-type IDs and inventory tool-tag IDs are separate enums and must not be confused when tracing gadgets.

REA 6.4.0 was installed in an isolated local folder and tested. Its Ghidra prerequisites pass, but actual inspect requests reject both the Dreams Ghidra archive and original PS4 executable as unsupported formats. Its current Windows provider cannot attach to this saved analysis. Existing Ghidra analysis continues; no REA-generated semantic findings or extra review credit are claimed.

## Variable Gadget defaults

**47 names verified after reopening, 4 deferred, 9,500 unreviewed.** The names-only edit followed a cold backup. The complete inventory matches the baseline plus the durable rename journal; original archives remain unchanged.

`140944f20` is now `InitializeVariableGadgetDefaults`. Two independent caller jump tables route object type 0x58 (VariableGadget) to zero-fill branches followed by this initializer. Complete assembly establishes InitialValue=0, MinLength=-1000, MaxLength=1000, preservation=false and rewind restoration=true, matched to the independently reviewed field registrar. Callers zero the object first; this helper alone does not overwrite every byte.

Runtime investigation also located a value-update function that gates initialization on the preservation flag, consumes linked Variable Modifier objects, clamps values, and constructs increase/decrease masks. That function remains under review: its context gates and caller dispatch need further validation. The extraction count is unchanged and does not represent semantic completion.

## Variable Gadget value update

**48 names verified after reopening, 4 deferred, 9,499 unreviewed.** The names-only edit followed a cold backup and complete function metadata was checked after reopening.

`1408e4bb0` is now `UpdateVariableGadgetValues`. Complete assembly and the caller's directly read jump table confirm type 0x58 dispatch. It gates initialization on the preservation flag, processes linked Variable Modifiers, clamps the five stored values, and produces increase/decrease masks. The modifier's independently registered OperationType enum matches the arithmetic: Set=0, Get=1, Add=2, Reset=3. Get performs no value write in these branches.

Mask bits0..3 correspond to the four player slots and bit4 to the non-player slot; comparisons are strict and ordered. Missing comparison objects leave the masks unchanged. The context double, mode gates, snapshot timing and external player numbering remain unresolved. No guessed types or prototypes were applied, and static analysis is not a claim that gameplay was observed.

## Variable lookup sorting and preservation

**49 names verified after reopening, 4 deferred, 9,498 unreviewed.** `1409af070` is now `SortU64I16Entries`: complete C and assembly review shows lexicographic sorting of 16-byte records by unsigned 64-bit key and signed 16-bit index. Its only non-recursive direct caller builds a Variable Gadget lookup table. The key's semantic identity and original library provenance remain unresolved.

A separately reviewed caller path skips value copying when RestoreVariableOnLevelRewind is enabled. Otherwise it matches Variable Gadgets, copies values, and sets the preservation flag before simulation preparation. Multiplayer values follow player mappings; absent mappings use the destination InitialValue. Raw-byte decoding resolved an incorrect instruction boundary in that caller without altering the project listing. The larger caller is not counted as fully reviewed or newly named.

The name-only change followed a cold backup and full metadata verification after reopening. No guessed types or prototypes were applied. The progress map counts mapped functions only; this generic helper remains unassigned pending system ownership evidence.

## Verified status map update

Mapped seven independently reviewed functions to their confirmed gadget types: Reporter Sculpt, Reporter Telemetry, Wireless Receiver, Wireless Transmitter and Variable Gadget. The map now contains 1,547 functions, with 43 checked, 4 unresolved and 1,500 awaiting review. Six other checked functions remain outside the map pending supported ownership. Equal square cells now support arbitrary mapped counts; no invented functions pad the last row. Counts measure identified code, not full subsystem completion.

## Game-pool context lifecycle

**51 names verified after reopening, 4 deferred, 9,496 unreviewed.** `140904120` is now `InitializeGamePoolContext`; `14090e110` is `AcquireUnusedGamePoolContext`. Complete assembly and the pool-creation sequence establish seven fixed-size contexts, usage counters, exclusion of the current context, and initialization before reuse. The creation code registers the label main game pool and stores the pool in the same global used by acquisition.

Initialization establishes defaults, arena pointers, list anchors and counters; it does more than zero memory. Acquisition waits/retries until a context is available and returns the initialized context through its output pointer. Exact synchronization import identities and full context types remain unresolved. Both edits changed names only, followed a cold backup and were verified with full metadata after reopening.

## Game-pool reference lifetime

**53 names verified after reopening, 4 deferred, 9,494 unreviewed.** `14090e280` is now `RetainCurrentGamePoolContext`; `14090e300` is `ReleaseGamePoolContextReference`. Complete assembly confirms increment/decrement of the seven pool usage counters; the counter-offset arithmetic was checked for every pool slot. A caller retains one handle, uses its context if present and releases that same handle on both branches.

Release triggers the retry mechanism when the count becomes zero; it does not clear the handle or directly free its context. Exact synchronization imports and the copied metadata fields remain unknown. Another equivalent release body remains unnamed pending its caller review. Name-only edits followed a cold backup and were checked with full metadata after reopening.

## Merge lookup helper

**54 names verified after reopening, 4 deferred, 9,493 unreviewed.** `140913a90` is now `LookupU32HashTableValue`. All 324 assembly instructions and the complete cached C were reviewed. The helper reads 32-bit key/value entries, performs at most 16 repeated hash probes, and returns the stored value on a match or `0xffffffff` for an empty entry or exhaustion. It does not modify the table. Branch targets, contiguous instruction coverage and probe count were audited.

Its callers in the game-merging code translate endpoint values before emitting a relationship. The larger merge routine is only partly reviewed and retains its original name. This name-only edit followed a cold project backup; full metadata and the complete function inventory were verified after reopening. Original archives remain unchanged.

## Merge index sorting

**55 names verified after reopening, 4 deferred, 9,492 unreviewed.** `140912670` is now `SortU16IndicesByDescendingI32Keys`. All 478 assembly instructions and the cached body were reviewed: it rearranges 16-bit indices using descending signed 32-bit keys, with partitioning, a heap fallback, and insertion for small ranges. Both external callers are in the game merge routine.

The insertion helper was traced through the executable loader's import slot and symbol identifier to `memmove`, corroborated by [shadPS4's import registration](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/libc_internal/libc_internal_memory.cpp). All 84 direct branch targets were checked. This is a descriptive analyst name; original source identity, sort stability and native runtime behavior are not claimed. The edit followed a cold backup and was verified after reopening, including full function metadata and the complete inventory. Original archive hashes remain unchanged.

## Filtered object graph traversal

**56 names verified after reopening, 4 deferred, 9,491 unreviewed.** `140769150` is now `AdvanceFilteredObjectGraphIterator`. Its complete cached body and 212 assembly instructions establish an explicit traversal stack, node visited sets, packed links and category filters. The emitter transform dispatcher consumes its object indices and separately deduplicates corresponding physics bodies. Another caller checks whether a requested object is among the yielded indices.

Caller assembly confirms inline initialization that the cached pseudocode omitted. All 57 direct branch targets were checked. The descriptive name does not claim recovered native class names or edge enums. The edit followed a cold backup; reopening verified all 56 names and the complete function inventory. Original archive hashes remain unchanged. Emitter velocity assignment and its separate object/body callback channels are under analysis and have not yet received verified names.

### Status measurement correction

Separated property/type code from runtime/implementation within the existing feature hierarchy. System ownership and all 1,554 mapped addresses remain unchanged. The graph and component breakdown report behavior/helper reviews separately from property/type reviews; progress data no longer exports checked-name percentages as feature completion. There are 9 mapped behavior/helper reviews and 41 mapped property/type reviews. Full feature completion is unknown. No new functions were named in this correction.

### Graph readability and denominators

Anchored main system headings at section starts and increased the packed lattice height so labels can fit without shrinking text. Labels now show separate reviewed/identified counts for runtime/helpers and properties/types. Missing role mappings are shown as a dash, rather than a zero completion claim. Exported component counts and the README table use the same denominators. Function colors, ownership, evidence and review states are unchanged.

## Object hierarchy transform name verified

`140903590` is now `ComputeObjectHierarchyTransform`. All 210 assembly instructions and the complete cached body establish parent-chain traversal and composition of a 32-byte position/scale plus quaternion result. An independent caller's complete 136-instruction body confirms its input/output use. Symbolic evaluation checks quaternion multiplication order, and the loader import ID plus recomputed hash identifies its infinity guard.

The name is descriptive. Native category meanings, cache invariants, external handedness and runtime validation remain unresolved; NaN sanitization is not established. A cold project backup preceded the edit. A clean restart verified all 57 names, the full 9,551-function inventory, unchanged metadata for this routine, and unchanged original archive hashes. No datatype, signature, calling convention, bytes or boundaries were edited. There are 57 verified names, 4 deferred reviews and 9,490 unreviewed functions. The map now contains 1,555 assigned functions, including 10 runtime/helper reviews and 41 property/type reviews.

## Teleporter runtime ownership

Native object tag `31` is Teleporter, confirmed from the enum's literal registration. A guarded call in the general property dispatcher passes that exact object to `1408f1dc0`; its offset reads match the Teleporter descriptor's `PosOffset` field at `+f0`. Its full 136-instruction body is now named `ComputeTeleporterTransformWithOffset`. It composes the object hierarchy transform with that offset; zero offset xyz uses active physics-body or cached object translation.

`140d78870` is now `RegisterTeleporterFieldOffsets`: its full 71 instructions bind 15 literal fields plus base position to descriptor `1458a7770`. Its full 42-instruction initializer, `140d55830`, is named `RegisterTeleporterTypeDescriptor`. Both survive reopening. These are descriptive names; no types, prototypes, conventions, bytes or boundaries were changed.

The map now places two runtime functions under Gadgets & logic / Movement & possession / Teleporter. The second, `1408f2180`, independently checks tag31 and computes an offset before a property operation; its 121-instruction body was read, but the property-write helper and context-mapping semantics remain unresolved, so it remains unnamed and incomplete. The general multi-type dispatcher is not assigned wholesale to Teleporter. Teleport execution, priority arbitration and fade behavior are still unreviewed.

There are 60 verified names, 4 deferred reviews and 9,487 unreviewed functions. Reopening verified the complete 9,551-function inventory and unchanged original archive hashes. The map contains 1,558 assigned functions, with 11 runtime/helper names and 43 property/type names checked. Whole-feature completion remains unknown.

## Packed status label verification

The system → subsystem → component → code-role hierarchy keeps each native component together instead of repeating it beneath analysis stages. Section names are 14 pixels, with compact checked-name/identified-function counts at 12 pixels. The inspected render has all nine main system headings and 48 nonoverlapping section labels, compared with 29 in the previous published render. All 1,558 function cells retain identical square dimensions. The table separates behavior/helper review from property/type review. Small components remain in the expanded breakdown; the graph does not claim full-system completion.

## Contiguous subsystem layout

Replaced the strip-quantization layout with recursive contiguous partitions of the shared square lattice. The inspected result moves the main systems and their nested components into new regions; it preserves all function assignments and review states. Main system labels use 16 pixels, component labels 14 pixels, and counts 12 pixels. All nine system labels must appear, each system must remain connected, and label boxes must remain inside the graph without overlap. This corrects the layout; full system mapping and completion remain incomplete.

## Compact front-page map

After inspecting the actual GitHub page in the browser, reduced the graph from 914 to 484 pixels high. The 64-column lattice preserves all 1,558 real, equal-square cells and all review states. Narrow sections prefer a horizontal split to accommodate readable words. No code mapping or semantic-review count increased in this layout change.

## Shared transform-property command path

`140705a90` is now `FindPackedObjectPropertyPayload`. Its full 22-instruction, 68-byte body searches the list at object `+18`, compares 16-bit identifiers, advances by a two-byte header plus the per-identifier payload size, and returns a payload pointer or null at the `ffff` terminator.

`140ad5f90` is now `TransferTransformPropertyPayload`. Its full 62-instruction, 267-byte body copies a 32-byte stream payload into a destination in mode 0. Mode 1 writes the destination's first float4 and normalized quaternion to the stream. Other modes only advance the cursor; every mode advances it by 32 bytes. All 13 direct branch targets across both helpers were checked. Both names survived reopening; no types, prototypes, conventions, bytes or boundaries changed.

The native command `10a` record contains a six-byte header and 32-byte payload. Its exact jump-table entry resolves to `140ae49d3`, which looks for a packed property payload, falls back to a positive type-specific inline offset, and reaches the transfer helper. With an existing payload, the write path synchronizes the inline copy only when the previous packed and inline values match. This is a bounded review of that branch, not the whole large dispatcher.

The Teleporter caller constructs a translation/scale plus identity-quaternion payload; an exact zero xyz result is replaced by the smallest positive normal float in those lanes. The sentinel's intent remains unproved. The archived type-offset table slot is zero, so command `10a` has not yet been proved to target Teleporter's registered `PosOffset`. No name is applied to that larger routine on this evidence.

There are 62 verified names, four deferred reviews and 9,485 unreviewed functions. The map has 1,560 assignments: 13 reviewed behavior/helpers, 43 reviewed property/type functions, four unresolved and 1,500 unreviewed. These shared helpers are not counted as completed Teleporter behavior. Whole-system completion remains unknown.

## Teleporter position-offset command identified

The compiled initializer contains a direct two-byte write at `140a83034` assigning `f0` to table slot `149f4f6e2`. Independently calculating the slot as `149f39f90 + 1f * b02 + 10a * 2` reaches that exact address. Teleporter's reviewed field registrar labels inline offset `f0` as `PosOffset`. This establishes the command-to-field link that was previously unresolved; the archived table's zero value was not the initialized binding.

Fourteen table entries also match named Teleporter fields and their registered offsets, including Power, Halfsize, Name, DetectName, TeleportPosition, TeleportOrientation, FadeIn, FadeOut, Priority and DetectScope. The neighboring `TeleportedLastFrame` field was not assigned a command by this comparison.

This is a bounded review of the initialization stores. The full large initializer was captured locally but has not been semantically reviewed or named, and startup ordering has not been tested in a running game. The caller's transform helper receives the caller's third argument as its object index; the evidence does not justify treating that index as the Teleporter itself. Editing intent and the tiny nonzero offset sentinel still need tracing. `1408f2180` is now `SubmitTeleporterPositionOffsetCommand`. Its full 121-instruction, 513-byte body and all ten direct branch targets were reviewed. The name survived saving and reopening; the full inventory matches the recorded renames. No types, signatures, conventions, bytes or boundaries changed. Verified naming is now 63 of 9,551 functions; four reviews remain deferred and 9,484 functions remain unreviewed.


### Shared position reader: 64 verified names

`1408f2110` is now `ReadObjectPhysicsOrCachedPosition`. Its complete 22-instruction, 97-byte body and all four direct branch destinations were checked. It reads the active physics-body position vector when available, otherwise the cached position; an ordered-zero cached w returns a zero vector. Native assembly returns 16 bytes in XMM0, whereas the cached pseudocode understates the return width. The caller consumes all four lanes and subtracts the independently reviewed hierarchy translation for the same object index.

A cold backup preceded the rename. Saving and reopening verified all 64 names and the full 9,551-function inventory; original archive hashes are unchanged. No prototype or datatype changes were made. The helper is shared, so it remains outside the subsystem map pending ownership evidence. There are 4 deferred reviews and 9,483 unreviewed functions. The mapped graph retains 1,560 functions and 57 checked names.

Further bounded assembly review follows a Teleporter-related pair queue into context flag propagation and shared physics-record/transform preparation. These findings do not yet locate the final teleport movement or establish complete Teleporter behavior.


### Object transform composition: 65 verified names

`1408f9b50` is now `ComputeObjectTransformWithPositionOffset`. Its complete 168-instruction, 766-byte body and all 13 direct branch targets were reviewed. Exact polynomial evaluation of 37 assembly instructions supports composition of the base and offset quaternions, rotated/scaled offset translation, and multiplication of scales. The original object's optional offset is combined with the resolved base transform; missing-offset paths preserve the base transform.

A cold backup preceded the rename. Saving and reopening verified all 65 names and the complete inventory. Original archive hashes remain unchanged. No prototypes, types or function boundaries changed. This shared helper remains unmapped pending subsystem ownership evidence. There are 4 deferred reviews and 9,482 unreviewed functions; mapped counts remain 1,560 functions and 57 checked names.

Bounded native analysis now traces the Teleporter pair queue through priority filtering, target selection and position/orientation flags into a shared application helper's physics-record writes. This advances the earlier queue-only trace. The enclosing large update routine and shared application helper are not yet fully reviewed or renamed. Runtime behavior, malformed-chain safety and floating-point equivalence remain unverified.



### Teleporter callback and movement-helper follow-up

The object path in shared helper `1408fa380` has an exact symbolic check of 41 assembly instructions: the delta quaternion multiplies the original quaternion; delta rotation, scale and translation transform the original position and scale. This proof covers ideal polynomial identities, not floating-point rounding, normalization or runtime execution. The complete 658-instruction body was read and all 53 direct branch targets checked. Additional vectors are transformed, preserved or cleared according to the mode; their meanings remain unresolved.

Teleporter callback vtable `141c2a1d8` slot `10` targets adapter `1408f20d0`. Its four instructions unwrap the game pointer and object index and tail-call the captured callback. The captured `1408f2040` entry resolves the object and sets flag bit 15 in its packed header; both paths of its 16-instruction body were checked. The caller installs this callback when accumulator `+4c` is zero; bounded earlier evidence connects that accumulator to prior TeleportedLastFrame values. The flag's meaning and downstream effects remain unknown. These are static findings, with no new names or runtime-validation claims.


### Teleporter target and scope analysis: 67 checked names

Candidate type 3 is independently registered as `Key`. Its field registrar and visitor confirm Power `+40`, position `+50`, Name `+f8`, and PosOffset `+110`, matching the target-selection reads. The complete 43-instruction field registrar and 42-instruction descriptor initializer now have descriptive names `RegisterKeyFieldOffsets` and `RegisterKeyTypeDescriptor`. A cold backup preceded the changes; reopening verified all 67 names and the complete inventory, with original archive hashes unchanged. These registration names do not establish complete gadget behavior.

The DetectScope enum independently supplies All=0, Me=1, Others=2. All bypasses ancestry filtering. Me accepts candidates whose ancestry reaches the selected scope anchor; Others accepts those whose ancestry does not. Parentless candidates pass only Others when filtering is active. The 96-instruction scope-anchor helper was read and its nine direct branches checked. Its optional extra parent step uses property slot `0x686`: compiled initialization for Key maps this to `+100`, independently registered and visited as IsGluedGadget. Cached ancestry type IDs 13, 14 and 15 independently map to Microchip, Timeline and Sound.

Nearest-target selection uses xyz distance and updates only for an ordered strictly smaller distance; equal finite distances retain the earlier candidate in linked-list order. The Power test rejects ordered nonpositive values but permits NaN through its native unordered comparison. Input validity and runtime behavior remain untested. Object `+2e`, cached/uncached ancestry equivalence, and the initial distance bound remain open.

Media Molecule's [Movers & Output guide](https://docs.indreams.me/en-US/create/resources/edit-mode-guide/assembly/gadgets/movers-and-output) describes named-tag targets and continuous following while powered. Its [v2.32 notes](https://docs.indreams.me/en/whats-happening/updates/release-notes/dreams/v232) describe configurable Teleporter ordering. These corroborate the observed behavior; they do not prove this binary's exact version or independently establish the internal Key-to-UI-Tag binding.

Additional exact polynomial checks cover physics-transform composition and four mode-dependent vector rotations in the shared application helper. The parent-relative position formula was checked with separately read sign-mask and scalar constants. Exceptional division, normalization, field meanings and running-game validation remain unresolved. No additional functions were counted toward audited-byte coverage in this batch.

### Physics motion pair provenance

The Emitter callback `140957f80` independently establishes linear and angular motion vectors at physics-record offsets `+70` and `+80`. An exact polynomial check of its twelve SIMD instructions confirms linear motion equals captured linear motion plus captured angular motion crossed with displacement from the captured origin. The fourth linear lane is preserved; the angular vector is copied.

A bounded 145-instruction section of `1409e67d0`, with 17 direct branch targets checked, selects `+90/+a0` in place of `+70/+80` when body flag `+ec` bit 3 is set. Both alternatives feed the same position and orientation integration. The selected xyz vectors are divided by 30; the constant's fourth lane is zero, so no exception-free four-lane arithmetic is claimed.

In `140bc1aa0`, one path copies the primary 32-byte motion pair into the alternate pair for every body. Another path stages the primary pair in separate arrays. A further 319-instruction review, with 21 direct branch targets checked, traces common writeback into both pairs and a conditional path deriving linear motion from a position difference. Intervening array processing, flag meanings, the difference multiplier and running-game validation remain open. These findings establish alternate linear/angular motion provenance without claiming a specific engine name for that storage. No new names, types or complete-function byte coverage were counted in this batch.

### Sculpt GPU transform preparation

The embedded label MakeBigListOfSDFTransformsForGPUJob is passed alongside callback `1415056b0`. Its 565-instruction return-bounded body was read and all 55 direct branch destinations checked. It builds packed object metadata, 48-byte forward transforms, fallback inverse transforms, scale data and an additional object/body-index table. The enclosing routine also stages motion buffers; it cannot be identified as a pure motion integrator from that subsection alone.

Exact polynomial checks of 64 object-path instructions and 58 physics/property-path instructions establish the same twelve-lane forward layout: three xyz basis columns followed by xyz translation. The linear part is object scale times resource scale times quaternion rotation; translation includes the rotated, scaled resource offset. A separate 42-instruction inverse check verifies the determinant denominator, inverse basis and negative inverse-basis-times-translation. The inverse requires a nonzero determinant. Floating-point rounding, invalid inputs, resource conversion and downstream GPU consumers remain unresolved; no whole-function completion credit or speculative name was added.

The 218-instruction working-buffer initializer was also read through its return. All 103 pointer assignments and the entry's position, quaternion, orientation-matrix, linear-motion and angular-motion buffer bindings were checked. This supports tracing the subsequent processing, but does not establish complete subsystem behavior. The separately read position-difference multiplier is 120 and motion integration divisor is 30; those constants alone do not establish the game's frame rate.


### Sculpt buffer setup and two verified shared helper names

The complete native bodies of `14001eb20` (17 instructions, 51 bytes) and `14001d7e0` (18 instructions, 54 bytes) support the analyst names `PackMaskedFormatFields` and `SetPackedBufferDescriptorFlags`. The first packs six masked integer fields into 24 bits. The second replaces selected fields in two descriptor words while preserving other bits. Neither body calls another function or branches. These names describe checked operations, not recovered original symbols or a proven GPU API.

A verified cold backup preceded the edits. Saving and reopening verified all 69 descriptive names against the complete 9,551-function inventory, with original and input archive hashes unchanged. There are 4 deferred reviews and 9,478 functions without naming review. Both helpers remain outside the subsystem map because their shared ownership is unresolved. No prototype, type, boundary or byte edits were made, and no whole-function behavior coverage credit was added automatically.

Bounded sculpt buffer setup requests three 786,432-byte allocations, then constructs views with a 48-byte stride. The descriptor's `0x3fff` argument is stored unchanged; it is not yet established whether the field denotes a count, limit or something else. The allocator's reviewed failure path performs maintenance and returns failure without retrying the allocation. The complete allocator contract and downstream GPU consumers remain unresolved.

The sculpt transform callback's resource scale conversion was traced through a one-instruction import thunk, its loader write and the imported NID `kn0yiYeExgA`. The [shadPS4 symbol database](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/aerolib/aerolib.inl) identifies that NID as `ldexpf`. The caller reconstructs scale as `ldexpf(1 + 0.25 * (word & 3), signed_word >> 2)` and scales a signed integer offset vector. This resolves the static conversion path, not floating-point corner cases or running-game behavior. Forward and inverse matrix proofs remain algebraic checks; singular transforms, exact GPU consumption and runtime validation remain open.


### Physics contact compute shaders: dispatch and compiled resources

Three bounded paths copy the SDF transform descriptors into downstream blocks. One reviewed path reserves a 448-byte scratch block and copies descriptors at offsets `+0x70` and `+0x80`. It then reaches a command writer and a dispatch helper. The dispatch helper and two wrappers were read completely, including their direct branches. Loader/import tracing resolves the final command-building import to `sceGnmDispatchDirect`, independently corroborated by [shadPS4's registration](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/gnmdriver/gnmdriver.cpp). This establishes static command construction, not execution in the running game.

The command writer's 17-entry jump table was checked against the native copy instructions. Its six-word case copies 24 bytes and advances the command cursor by 40 bytes. The immediate caller writes a block pointer and count; the other words occupy reused stack storage. Their complete reaching definitions and shader use remain unresolved. This is not evidence of an uninitialized-data bug.

Two complete 206-instruction resource getter bodies identify `RefreshContact.cs.pssl` and `RefreshContact_OldBetaVersion.cs.pssl`, tied to the embedded source path `src/physics/mankini_contact.cpp`. The reviewed caller selects between them using an internal flag whose product-facing meaning remains unknown. This places this use of the SDF transforms in physics contact processing, without claiming complete sculpt rendering or collision behavior.

The executable's hash routine was read and compared structurally with [MurmurHash3 x64-128](https://github.com/aappleby/smhasher/blob/master/src/MurmurHash3.cpp), including all 15 tail switch entries. The reconstructed normalized paths match two distinct entries in the supplied shader archive: 2,960-byte regular and 3,192-byte old-beta payloads. The archive's 604-entry candidate index was checked for sorted keys, bounds and nonoverlap. The native parser independently places both code pointers at payload offset 96. Its copied-region lengths are 2,804 and 3,036 bytes; those are not asserted to be instruction-only lengths.

A small bounded decoder, checked against [shadPS4's frontend decoder](https://github.com/shadps4-emu/shadPS4/blob/main/src/shader_recompiler/frontend/decode.cpp) and scalar-memory translation, reads the opening scalar operations and first two buffer reads. Both prefixes load through scalar registers s0:s1. Their scalar-load ranges include CPU-staged descriptor offsets; however, the first actual buffer reads use the separate descriptor at block `+0x100`. Later transform accesses, register bindings, vector arithmetic, all control-flow paths and runtime behavior remain to be established. The decoder stops on unsupported forms and is not presented as a complete disassembly.

Raw shader payloads, instruction captures and local paths remain private. This batch adds behavioral evidence but no names, type edits or automatic completion credit: 69 verified descriptive names, 4 deferred reviews, and the existing conservative whole-function coverage minimum remain unchanged.


### Shader parser and dispatch wrappers: 72 verified names

Three complete native bodies now have descriptive analyst names: `140011fb0` → `ExtractShaderBinarySections` (13 instructions, 43 bytes), `14003ade0` → `AppendGnmDispatchDirect` (39 instructions, 111 bytes), and `14003ae50` → `AppendGnmDispatchDirectWithMode` (45 instructions, 125 bytes). The parser computes metadata/code pointers and copy size, checked against both matched contact shader payloads. Both wrappers construct direct-dispatch commands through the resolved import and advance the command cursor only on success; the second incorporates a mode input into the flags. Growth-callback behavior and runtime execution remain separate unresolved contracts.

A cold backup was verified before editing. After saving and reopening, all 72 names and the complete 9,551-function inventory matched the baseline plus journaled changes, and original/input archive hashes were unchanged. Only names changed. The shared helpers remain outside the subsystem map pending ownership evidence; there are 4 deferred reviews and 9,475 functions without naming review. No automatic whole-function behavior coverage credit was added.

### Contact shader transforms and texture setup

The regular contact shader reads four three-dword chunks at offsets 0, 12, 24 and 36 through the descriptor loaded from block `+0x80`. The old-beta variant reads this same 48-byte layout through both `+0x70` and `+0x80`. All twelve read sites were checked against payload bytes. These layouts match the previously traced CPU transform records. An exact symbolic check of twelve arithmetic instructions on one regular-shader path produces `A*x + B*y + C*z + T - P`, where A/B/C/T are those four chunks. Input coordinate frames, masked execution and floating-point corner cases remain unresolved.

Physical linear decoding now reaches the first `S_ENDPGM` in both payloads: 495 instructions in the regular variant and 540 in the old-beta variant. All 18 and 21 decoded scalar branch targets land on decoded instruction boundaries. Both contain two `IMAGE_GATHER4_LZ` instructions. The reviewed region immediately before those operations loads an eight-word image descriptor from block `+0x00` and a four-word sampler descriptor from `+0x40`; the CPU staging code copies matching sizes into those offsets. This custom decoder is not an independent hardware disassembler, and aligned targets do not prove complete control-flow or lane semantics. A scalar-immediate encoding classification was corrected during review; the boundary and binding checks still pass.

Tracing the image descriptor's enclosing resource reaches creation routine `1413c3620`. Its complete 146-instruction body was read and all eleven direct branch targets checked. The descriptor is stored at resource `+0x2c`, initialized before backing-memory allocation, and updated with the allocated address. The earlier global descriptor write is zero initialization, not evidence of live image contents.

The creation template requests a **2048 x 2048 x 128 3D texture**. The descriptor type's relative jump table, dimension packing and type-specific depth selection establish this distinction from a 2D array. Creation format selector 45 maps through the game's table to packed value `0x204001`; the format setter produces GPU data format 1 and number format 0, meaning **single-channel 8-bit UNORM**. Field meanings were checked against shadPS4's [image descriptor](https://github.com/shadps4-emu/shadPS4/blob/main/src/video_core/amdgpu/resource.h) and [format definitions](https://github.com/shadps4-emu/shadPS4/blob/main/src/video_core/amdgpu/pixel_format.h).

These are static setup and arithmetic findings. Uploaded texels, component swizzle, later aliased updates, full shader-pointer binding, all execution paths and runtime contact behavior remain unverified. The format alone does not establish signed-distance encoding. No new function names, types, subsystem completion or audited whole-function coverage are credited in this batch. Raw payloads and assembly remain local.


### Contact sampling and conditional volume-index output

A bounded arithmetic review of the regular contact shader verifies that its two four-value image gathers are combined as two bilinear samples, then blended along a third coordinate. The checked corner order is 3, 2, 0, 1. A later checked expression converts the sample to `(4*sample - 2) * 2^exponent`, with the exponent obtained from a packed record. This establishes the static arithmetic expression; it does not yet establish a complete signed-distance contract, lane behavior or running-game correctness. Three further checked expressions subtract opposite face sums from the eight gathered values. They are not claimed to be the exact derivative of trilinear interpolation.

Native routine `1412776e0` copies a 288-byte CPU resource record and constructs 168-byte packed records in two arrays. The source word at offset `+0xd8` is copied unchanged to packed offset `+0x50`, which the contact shader reads. Its separate scale field uses the previously resolved `ldexpf` conversion. The packed GPU buffer setup requests 16,384 records at a 168-byte stride. Complete meanings of the remaining record fields and full caller behavior remain open; no speculative function name was applied.

Tracing another input index array reaches the volume evaluation pass in `14127f740`. The caller's descriptor is copied into staging block `+0x80` before selecting `Bricker2WriteKidIndices` or `Bricker2WriteKidIndicesMulti`. Both embedded shader/source names were matched to entries in the original shader archive using the reviewed path hash. In the Multi variant, a checked conditional path loads that descriptor and writes a dword through it. The stored expression ORs a vector value with one staging value shifted by 24 and another scalar value shifted by 28. This is a conditional write, not a complete shader contract. Earlier divergent definitions, input ranges and the meaning of the overlapping upper bits still need review.

The same evaluation routine also selects `Bricker2ClearAtlas`, `Bricker2MakeTreeIndexAtlas` and `Bricker2ClearTreeCounters`, all matched to compiled resources. The small MakeTreeIndexAtlas body extracts three 10-bit coordinates from an input word and stores a linear index with its high bit set into an image. That image lookup is distinct from the conditional output-array write above. Names alone were not used to classify either output.

These findings add checked behavior, not automatic completion credit. The verified naming total remains **72**. Raw code, shader payloads and local paths remain private.


### Volume resource packing: 73 verified names

The complete 141-instruction, 730-byte body at `1412776e0` now has the descriptive analyst name `CopyAndPackGpuVolumeResource`. It copies a 288-byte CPU resource record and constructs matching 168-byte records in CPU and GPU-backed arrays. The name describes the checked copy/packing operation; individual field semantics, input ranges and floating-point exceptional behavior remain unresolved.

A verified cold backup preceded the name-only edit. Saving and reopening verified all 73 names and the full 9,551-function inventory against the baseline plus journaled edits. Original/input archive hashes are unchanged. No prototypes, types, boundaries or bytes changed, and no automatic complete-function behavior coverage was added. This helper remains outside the displayed subsystem map pending an evidenced ownership assignment.


### Resource bounds and alternate contact bounds

The two packed output records of `CopyAndPackGpuVolumeResource` each receive 18 stores covering exactly 168 bytes, without gaps or overlapping writes. Corresponding fields use matching sources. Checked native arithmetic and constants identify the resource-adjusted center at `+0x28`, half-extents at `+0x34`, normalization scale at `+0x60` and normalization bias at `+0x6c`. In real arithmetic, the latter scale/bias map the transformed lower and upper bounds to 0 and 1; 108 rational endpoint cross-checks passed. Floating-point exceptional cases and runtime behavior remain unresolved.

The regular contact shader reads the center and half-extents fields. A checked seven-instruction block forms `abs(point-center)-half_extent` and its maximum component. Raw absolute-value and negate modifier bits were checked. This is a box-related calculation, not yet a complete collision-distance contract.

Six checked shader selections use alternate bounds when their first extent is positive; otherwise they use the packed resource bounds. The alternate descriptor reaches a CPU-produced array of 24-byte center/extents records. A checked producer path copies these from a separate 128-byte record array only when its word at `+0x6e` is nonzero and dword at `+0x70` equals 1. Otherwise that write path uses minus-one extent sentinels, triggering the shader fallback. Other paths can skip the write and still require review.

The upstream array writer selects a candidate record and copies its bounds and both gate fields. Candidate kinds are initially 0, 1 and 2, but the constructor can overwrite a kind on an early-success path; initial values are not treated as final type identities. A separately checked constructor path sums absolute extent vectors, applies resource offset/scale conversion, and writes the resulting midpoint and half-difference. Upstream vector construction, final kind definitions and exact coordinate spaces remain unresolved. The full captured constructor body has not been semantically reviewed.

These findings add evidence without new names, speculative types or automatic completion credit. The verified descriptive-name total remains 73; raw captures stay local.


### Transformed box samples: 74 verified names

`1414f3e20` is now named `AppendTransformedBoxSamples`. The native body constructs a grid of sample positions from extents, can add edge samples and eight corner samples, transforms coordinates through three axes and a translation, and appends 16-byte records to a shared array. Remaining per-call and shared-array capacity gates precede generation.

The primary fourth value is 1.5 times the smallest extent divided by its axis count, calculated before optional count doubling. Edge and corner paths use one half and one quarter of that value. These calculations are verified; the scalar's downstream meaning remains unresolved. The edge count identity was checked against 125 positive dimension combinations, without claiming invalid-input or floating-point correctness.

A cold backup preceded the name-only change. Reopening verified all 74 applied names, the complete inventory against baseline plus journaled changes, and unchanged original/input archive hashes. No types or code bytes changed. This is partial semantic progress, with no new complete-behavior coverage credit. The helper is not added to a displayed subsystem until ownership is supported.


### Box samples and weighted body centers

The downstream consumer at `140bc0d80` reads each object's sample count and starting index from a 128-byte record and accesses 16-byte samples. The position follows a quaternion-style transform, scale and translation. The fourth sample value is multiplied by absolute transform scale; another body-dependent factor can affect the complete record. Its final magnitude weights the position contribution, and the consumer accumulates both weighted xyz and total weight.

The caller at `140bc1aa0` then divides the accumulated xyz by that same total weight for selected bodies, writing a weighted center back to the body record. Exact pointer/offset arithmetic ties the accumulation and normalization to the same fields. Earlier guarded paths clear those accumulators. This establishes a weighted-center calculation, without asserting original type names, center-of-mass semantics or an exclusive meaning for the sample's fourth value. The selected-body flags, zero-weight cases and other paths remain under review.

These bounded findings do not add verified names or complete-function behavior coverage. All 74 previously applied names remain the saved and reopened naming baseline.


### Sphere-sample filtering and transform updates: 77 verified names

Read the complete native bodies of two shader loaders (205 instructions each) and their 435-instruction caller. Applied descriptive names `GetTestSpheresAgainstSdfComputeShader` (`1414f2fd0`), `GetSphereVsSphereCheckComputeShader` (`1414f3370`), and `FilterSphereSamplesWithGpuTests` (`1414f3710`). Embedded source/shader identifiers and matching entries in the local shader archive corroborate the identities. The caller uploads 16-byte samples, invokes the SDF test and five sphere-versus-sphere passes, then compacts records with a positive fourth value into the caller array and updates its count. Shader rejection rules and graphics synchronization contracts are not yet fully decoded.

The body transform staging path was also traced: each 304-byte body record contributes a 32-byte position/rotation pair to a working array. Checked downstream loops write paired vectors back, retaining the first vector's fourth lane. A later body-update branch subtracts the rotated weighted center from its target position to compensate the body origin. Per-body accepted sample counts gate center normalization; a nonzero count alone has not been proven to guarantee nonzero total weight.

One verified cold backup preceded the three name-only edits. Reopening verified all 77 applied names and the complete inventory against baseline plus journaled changes; original/input archive hashes are unchanged. No types or code bytes changed, and these partial findings add no complete-function behavior coverage. Shader identities establish a sphere-test pipeline, without proving that every use of the fourth sample scalar has identical semantics.


### Compute binding and sphere bounds fallback: 78 verified names

Named `14003b210` `AppendGnmComputeShaderBinding` after checking its complete 30-instruction body and resolved import. It requires 25 command-buffer DWORDs, requests growth when needed, calls `sceGnmSetCsShaderWithModifier` with modifier zero, and advances the cursor by 100 bytes only on API success. The capacity comparison uses a truncated 32-bit value; valid ordered buffer pointers are a precondition. Growth-callback behavior and GPU execution remain unverified. A verified cold backup preceded the name-only change; reopening verified all 78 names, the complete inventory and unchanged original/input archive hashes.

The sphere shader's bounds fallback was traced separately. It computes each absolute center-subtracted coordinate minus its packed half extent, selects every axis tied for the largest component, and copies coordinate sign bits onto zero/one axis magnitudes. Ties can therefore retain multiple axes. Its nonnegative fallback magnitude is the largest positive bounds excess, rather than Euclidean distance to the box. Nineteen instruction sites and 216 finite-input cases were checked, including 96 multi-axis ties; these are static arithmetic checks, not GPU execution tests.

The fallback and sampled-field paths feed the previously documented maximum-component direction scaling and fitting decisions. Exceptional floating behavior, runtime ordering and the complete shader contract remain unresolved. This batch adds one supported descriptive name and no complete-behavior coverage. The generic binding helper is not assigned to a Dreams subsystem solely because the physics caller uses it; displayed subsystem ownership remains evidence-based. Raw code and captures remain local.


### Sphere pipeline: fitting decisions and synchronization

For finite full-group sampled values, the checked reductions give a minimum and maximum across 64 lanes. The prospective stored radius is the previous radius minus the maximum when that maximum is positive, or the previous radius otherwise. At counter 24, a positive minimum selects a minus-one rejection value; otherwise the prospective radius is stored. Earlier iterations choose direct correction when the minimum is positive; the alternative mean-fit path continues only when its clamped candidate exceeds the prospective radius. An exit stores the prospective radius, not that candidate. The counter comparison survives the intervening 39 instructions without a scalar condition overwrite. These bounded checks do not establish convergence or exceptional-input correctness.

Between shader passes, `1412989d0` reserves and zeroes an eight-byte temporary token in command-stream storage, emits a 64-bit immediate-one release command, calls the resolved `sceGnmComputeWaitOnAddress` wrapper, then appends an acquire-memory command. The primary implementation maps selector 3 to a masked equality wait, here with reference one and mask `0xffffffff`. This is a GPU command-stream barrier, distinct from the CPU completion wait. [Primary API implementation](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/libraries/gnmdriver/gnmdriver.cpp#L162), [packet definitions](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/video_core/amdgpu/pm4_cmds.h#L661).

Before CPU compaction, a separate wrapper submits a completion-sequence command and calls `sceKernelWaitEqueue` repeatedly. It checks the completion memory against the expected sequence after each return; the event alone does not terminate the loop. The completion packet writes 32 bits, while the CPU compares 64 bits. The context constructor allocates 32 bytes and zeroes all of them before the first wait, establishing the required upper-word initial state. Preservation across every later aliased writer remains unproven.

These findings join the shader decisions to native submission and wait paths. Real GPU cache visibility, complete failure recovery, reuse invariants and in-place peer races within one dispatch remain unresolved. No additional names, types or complete-behavior coverage are credited; the saved verified-name total remains 78. Raw code and captures stay local.


### Saved dispatch synchronization names: 81 verified names

Applied `AppendGnmComputeWaitOnAddress` (`14003c0a0`), `AppendAcquireMemoryPacket` (`14003c1e0`) and `AppendComputeDispatchBarrier` (`1412989d0`). Their complete bodies contain 43, 42 and 51 instructions respectively. The names describe the previously traced command construction and call chain; they do not assert successful execution, complete cache coherency or recovery from growth/API failure.

A verified cold backup preceded these name-only edits. Reopening verified all 81 recorded names, exact metadata for this batch, the full inventory against baseline plus journaled renames, and unchanged original/input archive hashes. No types, boundaries, calling conventions or code bytes changed. These shared command helpers remain outside displayed Dreams subsystem ownership pending evidence; no complete-behavior coverage is added.


### Sphere samples: downstream occupancy grid

The native consumer `1407338a0` takes the filtered center/radius samples and builds a bit grid. Each bit here represents a grid cell, not a sphere or a completed reverse-engineering task. The function's full 2,686-instruction capture is available locally; the findings below cover connected portions of it, not a complete behavior audit.

* **Grid sizing:** three selected base vectors give cell budgets of 512, 4,096 or 32,768. Bounds aspect ratios determine the dimensions; a `powf` scale and rounding are followed by decrementing a largest dimension until the product fits the budget. The import is identified through its loader binding and NID `1D0H2KNjshE`, matched against the pinned [primary symbol table](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/libraries/aerolib/aerolib.inl). A total-cell budget does not impose a per-axis limit below 64.
* **Sphere bounds:** the consumer transforms all eight corners of the center-plus/minus-radius box, takes their coordinate bounds, rounds outward and clips against grid limits. This is an enclosing-box calculation, not an exact transformed-sphere bound.
* **Cell traversal:** the small-span path sets a single cell bit. The larger-span path visits X/Y rows and solves a line/sphere quadratic for Z endpoints. The X/Y loop upper bounds are exclusive. Z storage and iteration use complete 64-cell words, including a padded final word. The inspected transforms initialize as identity bases; grid coordinates and normalized bounds are checked separately.
* **Unresolved mask edge case:** the native 64-bit shift sequence produces a zero mask when a chunk's local upper endpoint is 63. An isolated model using a sphere fully contained in its bounds reaches that case: dimensions 5 × 5 × 163, half-extents 0.5 × 0.5 × 32, radius 0.2, and a center on grid row (2, 2, 63) give rounded Z roots 62 and 64. Solving the actual line/sphere polynomial reproduces those endpoints. This is static arithmetic evidence, **not a reproduced game bug**: valid object construction, complete aliasing invariants and real floating-point/runtime behavior remain to be established.

The saved checks include exact instruction assertions, all eight box corners, 2,080 ordered within-word mask intervals, and 112 ideal coordinate round trips. Those checks cover the stated calculations; they do not prove the enclosing function or subsystem complete. No new names, types, mapped functions or whole-function behavior credit are added by this report. Raw game code, shader binaries and local captures remain private.


### Sphere candidates: selection, fallback and inertia data

The occupied-cell grid feeds a comparison between three candidate sphere sets. On the inspected normal path, a candidate qualifies only when its occupied-cell count strictly exceeds both the smallest positive candidate count and half the largest count (rounded down), and its sample count is 1–65,535. Among qualifying candidates, fewer samples win; ties prefer the earlier candidate. If none qualifies, a separate index-based fallback applies. Two manually derived models agree on 15,625 nonnegative cases; this is not native execution. Equal nonzero occupancy counts produce no qualifying candidate under the strict comparison.

That comparison is not the only selection path. The first two candidates use `140736f20` with strategy arguments zero and one. A nonzero low-byte return accepts the corresponding candidate immediately, bypassing occupancy comparison. A zero return can still leave generated samples. The strategy-one geometric branch checks a small-vector threshold near 0.001, a relative vector difference below 10%, a clear flag, and a scalar difference below 1%. Passing all four skips the final GPU sphere filter. UI meanings of the modes remain unresolved.

Later fallback can replace the chosen samples. Mode one can copy one supplied sphere; the other inspected path requests 50 samples for mode two or 100 otherwise, subject to capacity. These samples are emitted in opposite pairs. Before the minimum-radius clamp, their radius is `0.333f * R` and their center distance is `max(0, R - sample_radius)`. Direction generation uses a base-two radical inverse and a sine/cosine angle. The final radius floor near 0.01 can expand very small samples beyond the ideal enclosing sphere. The ideal geometric checks cover 600 generated sample cases, not runtime floating-point behavior.

The compared scalar and vector pair were traced through the resource-pool copy and GPU resource packer to writer `141292230`. Six signed 64-bit accumulated terms are converted to float and scaled by the fifth power of resource scale before reaching the vector pair. A weighted count, with an independently captured weight of exactly 0.5, is scaled by the cube of that scale before reaching the scalar. The writer dispatches `ComputeVoxelSolidInertia` and `ComputeFullChildSolidInertia`; native source-path/suffix construction corroborates both shader entries in the local archive. Together with the downstream box calculation, this supports an inertia-tensor interpretation for the vector pair and volume-like units for the scalar. Exact component normalization, voxel accumulation, units and runtime behavior still require shader verification; the scalar is not established as mass.

These are connected static behavior findings. No new function names, types, mapped-function counts or complete-function coverage are credited in this update. Raw code, shader binaries and captures remain local.


### Voxel inertia: inputs, six terms and GPU accumulation

The inspected `ComputeVoxelSolidInertia` shader reads three packed 10-bit coordinates from one word and counts set bits in two other words. Its arithmetic uses positions `4*coordinate + 2 - origin` and a weight between 0 and 64. It produces the three diagonal inertia terms and three negative cross products. Each diagonal also includes `4 * weight * 0.6666666865`. The arithmetic was checked against the encoded source-negation and output-scale modifiers; omitting those modifiers changes the result.

All six terms pass through a mantissa/exponent conversion into signed 64-bit pairs. The inspected reference decoder implements the conversion's rounding operation as floor of a float32 addition of 0.5. Hardware edge cases remain open. This block does not contain an explicit constant fixed-point multiplier, so the earlier suggestion that these particular outputs were fixed-point is not established.

Register tracing follows all 72 additions, 60 swizzles and 24 lane reads through to six GPU shared-data-store additions. The output order is **XX, YY, ZZ, YZ, ZX, XY**, at eight-byte intervals. Every traced add combines the same component. This proves component routing; complete active-lane behavior still needs review.

Native dispatch parameters place these terms at GPU shared-data-store byte offset `0xc68`. The native readback helper dispatches `ReadGDSCounters` with start offset `0xc00` and 45 dwords. A matching archive shader reads a dword at `start + 4*index` and stores it through its output buffer descriptor. The offset difference is `0x68`, consistent with the previously traced CPU six-term reads at `0x68` through `0x90`. Final descriptor-to-CPU pointer identity still needs independent confirmation before this is treated as a closed end-to-end proof.

These findings connect voxel inputs, tensor arithmetic, integer conversion and output routing. They do not establish physical normalization, exceptional-input handling, full shader completion or a working reconstruction of Dreams. No completion percentage, function-name count or subsystem size is increased. Raw instruction streams and shader payloads remain local.


### Inertia follow-up: shared buffer, tail lanes and full children

The output-buffer pointer connection is now established on the inspected successful setup path. Native setup constructs the readback descriptor from the same allocation pointer later loaded by the CPU, with four-byte elements and 45 entries. The descriptor encodes 44 address bits. This closes the earlier static pointer-provenance gap; it does not prove runtime synchronization or allocation/lifetime safety.

The voxel shader zeroes all six inertia inputs before masking out invalid record indices, then restores the saved execution mask before conversion and reduction. Under full 64-lane entry participation and ordinary finite conversion, out-of-range tail lanes therefore contribute zero. A modular-integer butterfly model passed all tail counts from zero through 64 with five signed-value patterns. Its auxiliary radius uses a separate origin and the formula `sqrt(sum((abs(position-origin)+k)^2))`, with `k=3.464101791381836`. Symbolic lane tracing verifies the finite-value maximum reduction across both 32-lane halves. That maximum is read at CPU offset `0x98` and multiplied by resource scale. The actual geometric reason for this constant remains unresolved.

The companion `ComputeFullChildSolidInertia` shader consumes selected bits from `mask_at_16 & ~mask_at_8`, least-significant first. Its bit-coordinate mapping enumerates a 4×4×4 grid. For the two observed level arguments, each bit contributes a cube-volume weight and diagonal/cross inertia terms at a level-dependent position. A bounded instruction-driven rational model matched the independent formulas in 384 cases covering every child bit, both levels and three base-coordinate tuples. This checks algebra and bit operations, not native float32 rounding or complete loop execution.

Tracing another 72 additions and 60 swizzles establishes that the full-child shader writes **XX, YY, ZZ, YZ, ZX, XY** to the same six slots used by the voxel shader. Their intermediate cross-term registers differ, but their final component order agrees. Input-mask producer semantics, physical normalization, exceptional values and hardware execution remain open. These findings add no complete-function credit or percentage increase.

### Correction: voxel inline constant and inertia term

The earlier voxel center offset and intrinsic diagonal term were incorrect. Encoded inline operand 244 is **2.0**, not 0.5, as defined in [LLVM’s AMDGPU disassembler](https://github.com/llvm/llvm-project/blob/main/llvm/lib/Target/AMDGPU/Disassembler/AMDGPUDisassembler.cpp). The center is `4*coordinate + 2`; the multiply-by-two output modifier makes the intermediate `4*weight`, so each diagonal includes `4*weight*0.6666666865`. The auxiliary radius uses the corrected center too. A decoded-instruction rational model checks 625 input combinations, including the encoded source modifiers and output scale. This verifies bounded algebra, not hardware float rounding or complete shader behavior. No additional completion credit or Ghidra renames were assigned for this correction.

### GPU radius: native storage and resource copy

The CPU writer scales the GPU auxiliary-radius readback, saves it temporarily, inserts it into the fourth float lane of a resource vector, and stores that vector at pool offset `0x20260`. The radius therefore occupies `0x2026c`. Assembly in resource-copy function `141295780` confirms a 32-byte copy from pool `+0x20260` to destination `+0x80`, preserving the radius at destination `+0x8c`. This destination uses a different layout from the fallback resource at `+0x4c`; the alternate construction traced below establishes a shared origin. Consumers of the copied radius, allocation lifetime and full runtime behavior remain under investigation. This bounded data-flow finding adds no whole-function completion credit.

### GPU radius connected to fallback sphere resources

An alternate branch of `1412993c0` copies the same pool vector into a temporary resource at `+0x40`, placing its radius in the fourth lane at `+0x4c`. It passes that temporary to `CopyAndPackGpuVolumeResource`, whose assembly copies `0x120` bytes into the indexed resource array. Fallback sphere code in `1407338a0` reads its radius at `+0x4c` and center vector at `+0x40` from that same array with the same `0x120` stride. This establishes the static data route from the GPU auxiliary radius to fallback sphere construction. It does not prove scheduling/lifetime, absence of intervening writes, or that the bound covers every resource type. The earlier unresolved relationship between the two layouts is now narrowed by this evidence; whole-function completion remains unchanged.

### Fallback sphere: radius origin and coordinate transform

The shader radius-origin parameters are the three lanes of a CPU center vector. After readback, the CPU adds translation metadata from the same selected pool entry (`+0x201f0`), shifting each signed integer coordinate left six bits before conversion to float. It then scales the translated center. Register and stack lineage confirms that the radius readback and center use the **same decoded scale value**. Together with the resource-array trace, this connects the radius measured about the shader origin to the center/radius pair supplied to fallback sphere construction. Integer wrapping, float rounding, object lifetime, all branch conditions and conservative coverage of every shape remain unverified. No additional whole-function completion credit is assigned.

### Extra CPU inertia: selected cells and cube constants

The CPU additionally accumulates inertia from a packed coordinate list. Captured constants and assembly give centers `64*(coordinate+0.5)-origin`, weight `64^3`, and a diagonal constant equal to float32(`64^3*64^2/6`), consistent with uniform side-64 cubes under this weight convention. The builder appends a coordinate when its cell-table entry equals `-2`. One verified writer of that state uses operation mode 1 and an interval upper endpoint below a negative threshold of approximately `-32.51*resource_scale`; the threshold comes from captured `0.5`, `64`, and `0.51` constants. Scalar/extent origins and the operation enum still need verification before assigning a source-level geometric meaning.

The inspected CPU loop updates six inertia terms, not the auxiliary radius. The full-child GPU shader likewise has six inertia accumulator writes and no radius maximum. This narrows which code computes the radius; it does **not** establish a game bug or prove that interior contributions need a separate radius update. Coverage of all shapes remains unresolved. No whole-function completion credit is added.

### Cell classifier: verified box-field dispatch

Captured jump-table bytes independently confirm that shape value `1`, extracted from flag bits 2–6, selects the inspected box-field branch. With optional hollowing disabled, its scalar is `max(abs(x)-a, abs(y)-b, abs(z)-c)` before per-record scaling: negative inside positive box extents, zero on the boundary, positive outside. This is an implicit box field, not Euclidean distance outside corners. The common cell-classification tail consumes that scalar interval. Original enum names, the full input transform, scale/extent validity and other shape branches remain unresolved; this evidence does not complete the enclosing function.

### Ellipsoid helper: candidate geometry and SIMD arguments

Helper `140e86000`, called by encoded shape 2 and other classifier branches, receives a point vector in `XMM0` and an axis vector in `XMM1`, returning its result through `XMM0`. The cached integer-only pseudocode prototype is misleading. Its initial quadratic intersects an ellipsoid with a line in direction `(1,1,1)` from the absolute point; later blocks consider coordinate planes and axes. A reproducible finite-real candidate model agrees with an independent maximum-coordinate-distance bisection model over 3,000 deterministic positive-axis cases (largest absolute difference about `2.15e-13`). This supports signed ellipsoid distance in the maximum-coordinate metric, not ordinary Euclidean distance. Native float32 execution, degenerate axes, full caller transforms and a backed-up custom-storage type change remain pending. No whole-function completion credit is assigned.

### Persisted ellipsoid helper name: 82 verified names

`140e86000` now has the descriptive analyst name `EvaluateEllipsoidLInfField`. A cold project backup was copied after graceful shutdown and verified file-by-file by SHA-256 before this name-only edit. A subsequent clean restart verified all 82 journaled names and the full inventory against the baseline plus recorded renames; original/input archive hashes remain unchanged. The helper’s misleading cached prototype has not been changed. Its full runtime behavior remains unverified, so complete-behavior coverage is unchanged. Subsystem ownership remains separate from this naming review.

### Paired primitive fields: dispatch and consumer evidence

Native dispatch-table bytes for `140e852e0` establish selectors 0 (box), 1 (sphere), 2 (cylinder field), and 4 (paired ellipsoid helper calls). The two point/dimension pairs arrive in SIMD registers; the results occupy the first two lanes of the returned vector. Sphere lane routing was checked in 500 deterministic real-arithmetic cases. Both native consumers compare these results to thresholds and form their difference on the inspected paths; their broader runtime purposes remain unresolved.

For selector 2, the unequal-axis XY candidate agrees with independent signed L-infinity ellipse-distance bisection in 2,000 finite positive-axis cases (largest difference about `1.39e-13`). The equal-axis shortcut instead uses Euclidean radial distance. The native branch combines its radial field with `abs(z)-height`, taking the maximum inside and the length of positive terms outside. This mixed metric must not be described as an exact Euclidean distance for every cylinder. Selector 3, invalid inputs, native float32 exceptional behavior, calling-convention types and full consumer semantics remain open. These checks add no whole-function completion credit or new applied name.


### Paired primitive evaluator: 83 persisted descriptive names

`140e852e0` is now named `EvaluatePairedPrimitiveFields`. The reversible name-only change followed a cold backup verified by file hashes. After a clean restart, all 83 recorded names and the full inventory matched the baseline plus the rename journal; original/input archive hashes were unchanged. The SIMD prototype remains unresolved and complete-behavior coverage has not increased.

The remaining selector 3 starts with an elliptic-cone quadratic, selects its negative-Z side, and combines a cap over `[-height,0]`. Its initial quadratic identity passed 500 exact rational checks. Reduced quadratic paths switch to a duplicated linear root `-C/B` when the leading coefficient is small relative to the other coefficients (float32 tolerance approximately `1e-5`). Exact zero-leading-coefficient examples were checked; near-linear approximations, zero denominators and native exceptional values still need analysis.

[Alex Evans’s 2015 developer slides](https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf), pages 27–29, explain the use of max-norm primitive fields and quadratic solutions. This corroborates the mathematical approach observed in the executable; prototype-era slides do not establish final symbol names, subsystem ownership or complete runtime behavior.

### Persisted SIMD signatures for primitive fields

The main Ghidra project now records explicit custom register storage for `EvaluateEllipsoidLInfField` (point and axes vectors in XMM0/XMM1, scalar float result in low XMM0) and `EvaluatePairedPrimitiveFields` (four vectors in XMM0–XMM3, selector in EDI, two float results in low XMM0). Analyst structures describe the observed lanes; they are not recovered original source types or alignment declarations.

Before promotion, both helpers and two callers decompiled successfully in an isolated project copy. Native call-site and control-flow checks distinguished scalar field uses from unrelated upper-register accesses. Promotion followed a fresh cold backup verified by file hashes. Independent reopening verified both signatures, storage and instruction-byte hashes; function names and boundaries were unchanged. All 83 names and the original/input archive hashes also passed verification after service restart. The historical notes above describe the prototypes before this correction. No semantic completion percentage is increased by this type change; exceptional inputs, further caller semantics and complete behavior remain unresolved.


### Force-gadget direction and field blending: 86 persisted names

Native string bytes, descriptor initialization and field registrations identify `ForceRepulseGadget`, including `ForcePushPull` at `+0x158` and `ForceType` at `+0x159` with Radial/Directional values. The runtime helper reads those same offsets, selects a radial position difference or a direction-property path, normalizes non-tiny vectors and optionally reverses the result. Its normalization uses a squared-length threshold of `2^-46` and one inverse-square-root refinement. The generic direction-property lookup and transform helper still need fuller analysis.

Applied descriptive names are `ComputeForceGadgetDirection`, `RegisterForceRepulseGadgetFieldOffsets` and `RegisterForceRepulseGadgetTypeDescriptor`. A fresh verified cold backup preceded these name-only edits. Restart verification confirmed all 86 recorded names, the full inventory and unchanged original/input archive hashes. Their signatures are unchanged; complete-behavior coverage remains unchanged.

One consumer turns paired primitive field values into a blending weight. For ordered finite values it chooses zero when the first field is at or above the threshold, one when both fields are below it, and otherwise interpolates the threshold crossing between them. The real-arithmetic crossing model passed 2,000 deterministic cases. Assembly then broadcasts this weight and multiplies the direction-helper result. This is field-based blending, not proof of an exact geometric intersection or the consumer’s entire behavior.

### Transform composition and Light bounds: further native analysis

The force-direction transform helper `141112450` combines an incoming transform with an optional property transform. Native lane tracing establishes quaternion multiplication in the order incoming × optional, and position composition as incoming position plus incoming scale times the optional position rotated by the incoming quaternion. Scale multiplies separately. Each algebraic identity passed 1,000 deterministic exact rational cases; these checks do not execute the original instructions. Quaternion normalization, property-table population and shape-specific output adjustments remain under review.

The local-bounds helper `1411129d0` produces two minimum/maximum vector pairs. Its ordinary vector path uses center ± half-size. A scalar fallback represents an inner radius and an additional nonnegative outer-radius extension. It also has a separate Light path. Native enum registration assigns 2 to Light; a construction branch independently selects type 2 with the Light descriptor, and its dispatch calls the constructor matching the registered light fields. The final object type-field write remains to be traced.

Light properties match Intensity at `+0xa0`, LightType at `+0xa8`, Range at `+0xac` and Angle at `+0xb0`; enum values are Spot=0 and Point=1. The angle call's loader import ID resolves to `tanf` in [shadPS4's import database](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/aerolib/aerolib.inl). For a spot light below 45 degrees, the symmetric bounds have extents `(Range*tan(Angle), Range*tan(Angle), Range)`; above the split they use `(Range, Range, Range*tan(pi/2-Angle))`. The point-light extent is `2*sqrt(100*Intensity)`. The secondary pair is zero in these branches. A 1,000-case finite-real check confirmed the complementary-angle identity, not native float32 behavior.

No new function names, whole-function completion credit or progress-percentage increase is claimed for these partial findings. Exceptional inputs and the surrounding runtime behavior remain unresolved. Raw native captures and executable data remain local.


### Light registration and object references: 89 persisted descriptive names

Applied `RegisterLightTypeDescriptor` (`140d54090`), `RegisterLightFieldOffsets` (`140d88a00`) and `DeserializeObjectReference` (`141601ca0`). The names describe observed roles rather than recovered original symbols. A fresh cold backup preceded the changes; clean reopening verified all 89 recorded names, the entire function inventory and unchanged original/input archive hashes. Signatures and instruction boundaries were unchanged.

The reference helper decodes a compact token, uses its upper bits as a reference ID, reuses existing object-table entries or creates an object through descriptor callbacks, and caches the object pointer alongside its descriptor. Native analysis established a 24-byte table-entry stride and a concrete-type factory callback at descriptor offset `+0x250`. Base-property registration copies this callback into derived descriptors, explaining why callers cannot be found using only the original global slot's direct references. Valid 32-bit encoding identities passed 1,000 deterministic model cases; malformed and overlength input behavior remains unresolved.

The Light factory branch and its native constructor were traced through a larger factory whose entry is not defined as a function in the captured snapshot. This exposes code outside the current discovered-function inventory; 9,551 must not be interpreted as proof of a complete function count. Establishing factory boundaries and tracing the final object type-field write remain open work. No complete-behavior coverage increase is claimed for this naming batch.


### Newly defined Light allocator

`AllocateDefaultLight` at `140d88850` was previously executable code without a defined Ghidra function. An isolated experiment established its 401-byte, 58-instruction body through its return, no overlap with existing functions, successful decompilation and a justified `void *` return in RAX. The routine calls C++ `operator new` for 400 bytes and initializes Light defaults, including spot mode, range 100, angle approximately 20 degrees, intensity 0.5 and shadows enabled. Its runtime type field initially remains zero; later restoration is unresolved.

Promotion followed a new verified cold backup. Reopening verified the new definition and all 89 prior renames; live MCP memory matched the pre-definition code-byte hash, and original/input archive hashes were unchanged. The discovered inventory is now 9,552 functions. There are 90 verified descriptive function names, comprising 89 renames and one newly defined function. The map includes the new allocator under the existing Light component. Complete-behavior coverage remains unchanged because the allocation-failure contract and surrounding runtime lifecycle are still under review.


### Force-position property and serialization

Assembly tracing connects packed property tag `0x27f`, used by the force-direction helper, to a `float3` reader. Its destination descriptor registers X/Y/Z at offsets 0/4/8 and declares 12 bytes. Both the allocation callback and packed-property slot reserve 16 bytes; that storage does not establish a fourth coordinate or the serialized byte count.

The typed reader resolves a stream schema identifier before loading composite fields. Saved fields are matched to current fields by 32-bit identifiers, including alternate identifiers and inherited fields with accumulated byte offsets. The complete 78-instruction lookup body supports the descriptive name `FindTypeFieldByIdentifier` (`141607680`). That name has been applied and read back locally after a verified backup; all 247 function bytes remain unchanged. Independent reopening verified all 90 recorded renames and the newly defined Light allocator against the full 9,552-function inventory. Original/input archive hashes are unchanged. The verified descriptive-name total is 91; this is not a count of fully understood functions.

The ordinary writer visits registered fields in order and applies flag/mask filters. The primitive decoder supports direct four-byte float reads when the schema category and destination stride match. Its short-read check is verified. The primitive float writer does not check its returned byte count locally; error propagation elsewhere is unresolved. These findings establish parts of the serialization path, not a complete file-format decoder or full behavior verification. No complete-behavior coverage credit is added.


### Creator category decoding and persona titles

`ParseCreatorCategoryCode` (`1402da320`) maps recognized creator-category token identifiers to compact byte codes. Assembly and executable string comparisons support General, Explorer, Creator, Artist, Animator, Maestro and Curator, with explicit case variants. Recognized input writes a code and returns success; unknown input leaves the destination unchanged and returns failure. A caller initializes that destination to zero and ignores the return value. The 270-byte body remained unchanged after the rename and an independent project reopening.

A separate registration identifies `EPersonaTitle` with 15 values: None, Tastemaker, Curator, Crafter, Artisan, Influencer, AudioSupreme, MasterBuilder, Puppeteer, Player, MajorGamer, Storyteller, Polymath, Animator and Artist. These enum values differ from the parser's compact code representation; their direct relationship is not yet established.

The surrounding structured parser builds 12-byte records containing two code bytes, an integer and a float. The integer branch matches the `points` identifier; the float branch has a hash-derived `time` candidate whose units and independent name linkage remain unresolved. The larger parser has not been named or counted as fully understood. The identifier formula has corroborating constants but is not yet verified across all input lengths.

Independent reopening verified 91 existing-function renames and one newly defined function, for 92 descriptive names across 9,552 discovered functions. Original/input archive hashes are unchanged. Complete-behavior coverage is unchanged, and no speculative subsystem placement was added to the map.


### Creator queries and player-identity records

Two shared query helpers now have evidence-supported descriptive names: `AppendQueryClauseText` (`140633f00`) and `AppendUnquotedQueryField` (`140634120`). The first appends field/operator/value text and joins clauses with `AND`; the second records a field-name hash and requests unquoted formatting. The creator-category decoder's caller uses this path for clauses such as `persona=ARTIST`. Query construction is distinct from player-identity serialization. If hash-list allocation fails, text construction still proceeds; this pair of updates is not proven atomic.

Player-identity serialization independently links `persona` and `subpersona` to byte fields at offsets `0xC` and `0xD`, and `level` and `recent` to array headers at `0x20` and `0x30`. Each level record has a 12-byte stride: two code bytes, a 32-bit integer at offset 4, and a float at offset 8. Native scalar argument loads corroborate the parser's record stores. One concrete writer emits creator codes as quoted letters, the integer with unsigned decimal formatting, and the float through a text formatter. Other serializer modes, second-code meanings, float units, import identity, and malformed-input behavior remain under review. An unrelated `Persona` menu label does not establish a data type.

The project was cold-backed-up before these two name-only edits. Independent reopening verified all 93 renames and the previously defined allocator; all 596 bytes of the two helpers match the immutable baseline. Original archive hashes remain unchanged. There are now 94 verified descriptive names across 9,552 discovered functions. These findings add no complete-behavior coverage credit. The new shared query helpers remain outside the subsystem map until their ownership is established, so the map's reviewed count does not rise for them.


### Level-record parser and serializer

`ParseCreatorLevelRecords` (`140412a70`) and `SerializeCreatorLevelRecords` (`140413970`) now have verified descriptive names. Both handle the creator-category records used by player identity's `level` and `recent` fields. Direct field-label callers and matching record loads/stores support mapping these two functions under **Dreamiverse & networking → Player identity → Level & recent records**. This identifies two pieces of implementation, not the full feature or its completion percentage.

The parser has distinct positional-array and keyed-object paths. The keyed path rejects integer `-1`, rejects ordered negative floats, and requires an ordered positive float when the integer is zero. With other nonzero integers, its comparison gate permits unordered values. That gate does not apply to the separate positional append continuation. Full four-field arity validation and error recovery remain unresolved.

Both inspected float-conversion branches accept spans up to 127 bytes containing digits and `+ - . E e`, copy and NUL-terminate them, call `strtod` with no end-pointer, and narrow the result to float32. Literal `NaN` and `inf` do not pass this filter. The filter does not validate full numeric grammar or conversion consumption. Exponent overflow is a nonfinite-value lead: host CRT conversion of `1e39` narrows to positive infinity, but this is not target-runtime reproduction. The concrete writer's classification import resolves to `__isfinitef`: finite values use unquoted `%f`, nonfinite values quoted `%f`. Exact nonfinite spelling is formatter-dependent.

The subcategory writer preserves 19 lowercase letter codes and emits `"0"` for unsupported codes. Static parser-table correspondence, conditional on the checked one-byte hash model, maps that sentinel to NUL. This is not an end-to-end runtime round-trip test, and most letter meanings remain unresolved.

A verified cold backup preceded the name-only edits. Independent reopening checked all 95 renames and the previously defined allocator. The two new functions' complete 4,798-byte spans match the immutable baseline; original archive hashes are unchanged. There are now 96 checked descriptive names among 9,552 discovered functions. No complete-behavior coverage credit was added.


### Creator records and Dreamstone identifiers

Three more descriptive names are verified after reopening: `AppendExpandedCreatorLevelRecords` (`140209490`), `GetDreamstoneTypeName` (`140252190`), and `RegisterDreamstoneTypeValues` (`140c841a0`). The expansion converts 12-byte category records into 16-byte records, mapping category bytes to numeric values and copying the integer and float bits. The destination capacity contract remains unresolved.

All 125 registered nonzero Dreamstone identifiers match the lookup's returned name pointers in a static instruction model. Registration includes zero as Invalid, while the lookup returns an empty name for zero. These are descriptive analyst names, not recovered source symbols.

The expanded level and recent records feed the player-identity update encoder. Its native calls target `/puserver.v1.IdentityService/UpdatePlayerIdentity`. Each record carries category, subcategory, a sign-extended integer varint, and raw float32 bits. Independent length calculations passed 343 boundary-value combinations; this is a static model, not game execution or proof of server acceptance.

Connection/shutdown and client-rate-limit statuses map to numeric 503. The queued-error consumer reaches a concrete identity callback, which forwards the special zero/-1 pending key. For the inspected constructor-installed owner vtable, failure processing proceeds only when state is neither zero nor finished state six. The handler retains an earlier nonzero/non-200 result. Subclass overrides, full retry behavior, and all finalization side effects remain unresolved.

There are now 99 checked descriptive names among 9,552 discovered functions. All three new names persisted after a clean save and reopening; their combined 5,608-byte spans and the original archives are unchanged. No complete-behavior coverage credit was added.


### Keyed object cache analysis

`AdjustObjectCacheKeyReferenceCount` (`1403a49a0`) is now verified after reopening. Its two observed callers add a reference on cache insertion and remove one on cache deletion. The helper tracks a 64-bit/32-bit key pair in 16-byte records, removes zero-count records, and grows its backing array when needed. This is an analyst descriptive name, not an original source symbol.

Related assembly analysis identifies 80-byte cache entries, 4,096 hash slots, payload blocks with 24-byte headers, and a deadline checked during payload-space reclamation. A caller supplies a deadline 600 seconds ahead. Counter and frequency import identifiers match the process-time APIs in [pinned shadPS4 source](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/libraries/kernel/time.cpp). This is static evidence, not runtime validation.

Eviction samples eight occupied entries and compares normalized age; samples need not be distinct. A synthetic model of hash removal found a wraparound case needing further investigation. Accepted key-domain reachability and game-runtime reproduction have not been established, so this is not reported as a confirmed game defect.

There are now 100 checked descriptive names among 9,552 discovered functions. The new name's 436-byte span, complete inventory, and original archives passed persistence verification. Its precise game-system assignment remains unresolved, so it is not placed into an invented subsystem. No complete-behavior coverage credit was added.


### Comment record cache analysis

`CacheCommentRecord` (`1403b2710`) now has a checked descriptive name, verified after saving and reopening the project. The complete native body and three observed caller sites support its role: it accepts a K/k identifier and caches either the complete record with status 2 or an empty payload with status 7, depending on a record flag. Both paths pass a deadline 600 seconds ahead. The parser's hashed `comment` key matches the dispatch value; this supports the association but does not recover an original source symbol.

Before caching, it computes a predominant right-to-left text flag. Native character tables distinguish left-to-right and right-to-left classes; the routine compares their counts after formatting/token filtering. This is a direction heuristic, not a complete Unicode bidirectional algorithm. The formatting helpers, fallback direction source, and meaning of the flag selecting status 7 remain under investigation.

Related response analysis distinguishes status handling, deferred parsing and cache consumption. Static evidence identifies a queue whose worker publishes parsed records and whose consumer matches them against requested identifiers. A zero parsed-record count also serves as a readiness condition; whether an empty parse can remain queued requires further investigation. No runtime failure is claimed.

There are now 101 checked descriptive names among 9,552 discovered functions. Original archives, function bytes, calling conventions and the complete inventory passed persistence checks. No complete-behavior coverage credit was added; the precise subsystem assignment of this cache helper remains unresolved.


### Version record and resource summaries

`ResolveAndCacheVersionRecord` (`1403b2030`) now has a descriptive name verified after saving and reopening. When handling a root version record, it resolves selected creation references through the cache. A missing dependency triggers a waiting cache status rather than normal payload storage. Normal records store a payload or status 7 according to a record flag; its precise meaning remains unresolved.

Startup assembly reconstructs 59 resource-metric entries whose stored table is initially zero. Member names support three summary categories: gameplay resources, graphics resources and audio resources. A producer examines indices 0 through 57 and admits 17 metrics from those categories, multiplies their values by 255, stores floats without clamping, and computes category maxima. These are internal game-resource summaries, not reverse-engineering completion percentages. Upstream metric calculations remain under review.

Zero identifiers in another record array receive eight random bytes through an import matched to `sceRandomGetRandomNumber` in [pinned shadPS4 source](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/libraries/random/random.cpp). The native caller ignores its result and does not retry zero identifiers. This is static analysis, not an observed runtime failure or a claim about console random quality.

The dispatcher consumes two output registers from the version helper; saved pseudocode omits one. That contract is documented locally, with no speculative prototype change. There are now 102 checked descriptive names among 9,552 discovered functions. The 1,159-byte function span, complete inventory and original archives passed persistence checks. No complete-behavior coverage credit or provisional subsystem assignment was added.


### Resource traversal and thermometer accounting

`AdvanceResourceTreeLeafIterator` (`1410607f0`) is now a checked descriptive name. Its complete native body advances through resource-tree leaves, popping exhausted parents and descending the next child. Shared callers support this general role. The 162-byte span and name were verified after saving and reopening; no prototype or type changes were made.

Native code connects a worker callback to the internal label `Thermometer`. Its sculpt-cost path deduplicates resource identifiers across two object lists before accumulating model, brick and ball costs. Another path uses a four-bit membership filter for resource pairs; this is not an exact set and its runtime collision frequency has not been measured.

The resource-count helper returns two distinct values: accepted iterator entries and a sum derived from record lengths divided by 40. Both the thermometer's current `SculptsSprites` contribution and a separate candidate-budget path use the length-derived second output. The candidate path scales it by 1/524,288 and adds it to the current normalized sprite metric before a limit comparison. The first output feeds a separate conditional worker counter whose final metric remains unresolved. Correction: an earlier explanation reversed the thermometer's output pointers; tracing the native call arguments and accumulation instructions resolved that error. This is static code evidence, not a claim that every counted entry is a rendered sprite or that a game defect has been demonstrated.

There are now 103 checked descriptive names among 9,552 discovered functions. This batch adds no complete-behavior credit or provisional subsystem mapping. Internal game-resource budgets are separate from progress in understanding Dreams.


### Packed resource records and sculpt accounting

Three descriptive names are now verified after reopening: `InitializePackedResourceRecordIterator`, `AdvancePackedResourceRecordIterator` and `DecodePackedResourceRecordDelta`. Their complete native bodies total 261 instructions and 895 bytes, all unchanged by the name-only edits. The iterator traverses resource-tree leaves; the decoder updates selected fields while retaining others. State is carried between records within a leaf and reset when advancing to another leaf. Original record type names remain unresolved.

The thermometer's `ScopeSculptPrimitives` metric sums weights from the effective decoded state, divides by 120,000 and caps the result at 1 before later filtering. Its `ThingWires` metric counts records subject to endpoint filters and divides by 16,383. Both divisors were checked against executable memory. These are game resource measurements, not reverse-engineering percentages.

Another worker branch maps to physics joints, collectabubbles, prizes and portals. The prize path compares 128-bit identifiers but retains at most 150 distinct identifiers for comparison. Repeats of identifiers first encountered after that capacity can count again in the translated algorithm. Runtime occurrence and producer constraints remain unverified; this is not an observed game bug.

There are now 106 checked descriptive names among 9,552 discovered functions. No full-behavior completion credit or new subsystem assignment is claimed for this batch. Raw code and detailed native traces remain local.

### Decoded resource transforms and compressed rotation

`TransformDecodedPackedResourceRecord` is now a checked descriptive name, verified after saving and reopening. Its 504-instruction body transforms four- and five-point records, applies scale to associated scalar fields, and combines and repacks compressed rotations on other paths. Four native call sites establish the mutable decoded record and the 32-byte transform argument. All 2,397 function bytes remain unchanged.

The rotation format stores three 15-bit components and a two-bit omitted-component index. The encoder chooses the largest absolute component, canonicalizes its sign, and the decoder reconstructs it from the remaining squared length. A deterministic scalar float32 model exercised 10,010 finite unit inputs, covering all four layouts; the largest observed rotation error was approximately 0.0081 degrees. This is a model result, not native execution or an error bound for every input. The normalization helper import resolves to `__isinff`; it must not be described as general NaN rejection. Actual linked-library behavior and exceptional inputs remain unverified.

There are now 107 checked descriptive names among 9,552 discovered functions. This adds a verified naming review, not whole-function behavior completion credit. Precise subsystem placement remains under investigation, so no new graph assignment is guessed. Raw code and detailed traces remain local.

### Expanded geometry records and bounds

`ExpandDecodedResourceRecord` and `AccumulateExpandedResourceRecordBounds` are now verified descriptive names after saving and reopening. Their complete native bodies contain 742 and 336 instructions respectively, with all 4,817 bytes unchanged. The first expands decoded resource state into 96-byte geometric records; the second consumes those records to expand or intersect bounds and independently accumulate signed metadata. No datatype or prototype edits were made.

Native callers establish different scratch capacities: one allows 64 expanded records, matching up to 32 repetitions with two mirror variants; another allows only two records and checks the end before each write. Why the latter path keeps this smaller subset remains unresolved. An earlier local note incorrectly summarized the expansion repetition field as bits 5–6; native caller instructions extract bits 2–6. The separately traced thermometer weighting must not be substituted for expansion counts.

The expanded layout depends on its variant. One offset holds a reciprocal basis norm on a basis path and a radius-like extent on a point path, so it cannot be assigned a universal field meaning. The reciprocal calculation is compatible with max-norm change-of-basis correction discussed in Alex Evans's [2015 Media Molecule presentation](https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf), but its evaluator consumers still need tracing. Historical material is a lead, not proof of this build's original shape names or exact behavior.

There are now 109 checked descriptive names among 9,552 discovered functions. Complete behavior coverage remains unchanged. No new subsystem assignment is guessed; raw code, native traces and project backups remain local.

### Packed record writing and resource-page summaries

Three more descriptive names are verified after saving and reopening: `AppendPackedResourceRecord`, `TryAppendPackedResourceRecordDelta`, and `RecomputePackedResourceNodeSummary`. Their complete native bodies contain 506 instructions and 1,874 bytes, unchanged by the name-only edits. The append wrapper handles resource-tree continuation and restores the delta baseline by replaying the selected leaf. The summary helper computes metadata ranges and counts; it does not normalize geometry.

The delta writer's presence masks and payload sizes match the decoder. It updates the published leaf length and cached state on success. A failed attempt may leave tentative bytes beyond the previously published length, so the operation must not be described as rolling back all writes. A local scalar format model passed 8,224 round-trip cases across variant and optional-field combinations, but does not execute the native implementation or validate capacity failures. The compared floating-point field treats signed zeros as equal, so bitwise preservation is not promised.

The resource-page allocator's native diagnostics identify categories for CSG, animation, light and sprite strokes, sound, JPEG images, and script data. This supports shared storage infrastructure rather than a sculpt-only allocator. Allocation exhaustion, tree-depth bounds, hash collisions, concurrency and actual runtime behavior remain unverified.

There are now 112 checked descriptive names among 9,552 discovered functions. Full-behavior coverage remains unchanged, and no subsystem assignment is guessed for these helpers. Raw code and detailed evidence remain local.

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

### Sound playback trace and time-bounds signature correction

Traced Power comparisons through registered trigger-state fields and Playhead writes. Corrected `GetThingTimeBounds` to four arguments with the verified calling convention after reviewing 50 direct call setups, running an isolated trial, and checking persistence after reopening. Original archives and instruction bytes were preserved. Previous-frame context identity and complete Sound update behavior remain unresolved. Counts and full-behavior coverage are unchanged; see [research findings](ANALYSIS.md#sound-power-triggering-and-playhead).

### Shared timeline timing helpers

`GetThingTimeBounds`, `ComputeThingTimelineInterval`, and the newly named `ComputeThingTimelineIntervalFromTimeBounds` are mapped to shared runtime code. They handle timing across object kinds, rather than belonging exclusively to sound or one gadget family.

The interval helper now has a corrected six-argument PS4 calling convention: object, context, two output pointers, and two floating-point bounds. All 18 discovered direct call argument setups were inspected. A cold-copy trial preceded the live correction; reopening confirmed persistence and unchanged instruction bytes. The context term uses the Timeline CanvasProps origin and zoom field, not the Playhead field. Concrete context types and complete caller behavior remain unresolved.

The wrapper's complete 38-instruction body obtains time bounds and forwards them to the interval helper. All three direct callers were inspected. Its descriptive name was verified after reopening; its prototype remains unchanged. There are now 141 checked descriptive names among 9,553 discovered functions. These changes add no full-behavior completion credit.

### Sound forced-playhead branch

A further 49 current native instructions were matched against the executable in the later Sound update branch. `ForceRvPlayhead` is cleared when an upstream flags byte lacks bit 2 or SoundType equals 1. Otherwise it depends on an indexed flags word's bit 5 being clear and object mode differing from 4.

When forced-playhead handling is enabled, the updated Sound's Power and the paired Sound object's force flag affect the playing candidate. A nonzero or unordered Power comparison can force both that candidate and the trigger discriminator to one when the paired force flag is clear. The common downstream stores have additional gates; this does not establish that the final playing byte always changes.

The upstream flags' meanings and the paired object's temporal role remain unresolved. Stack storage is reused across branches, so no global stack-slot types are inferred. This adds bounded behavior evidence, with no new checked names, runtime validation, or full-function completion credit.

### Timeline flags linked to Sound playback

Live instruction review now links the Sound playback gates to their context flags array: two-byte entries at context offset `+0x210c54`. Sound `ForcePreview` receives bit 0 of a selected entry. Live field registration also confirms `UseLiveNoteData`; one update path clears that field before joining the forced-playhead branch. The provenance review matched 566 native instructions and both field-name literals.

A further 98 native instructions establish one producer path. The main update loop follows object references through Timeline objects, calculates intervals, and sets bits 3 and 5 on each working object. This supplies a concrete producer for the bit-5 gate used by Sound forced-playhead handling. After a successful traversal, it appends a record containing two object identifiers and an accumulated timing float, increments the record count, and sets bit 4. The playback consumer's bit-4 path scans these records for a matching identifier and reads the timing float.

These are bounded static findings. Other producers, flag resets, selection gates and the temporal relationship between paired object contexts remain unresolved. No original enum names, new checked-function credit, runtime verification, or whole-function completion credit are claimed.

### Animation keyframe and input predicate

`HasAnimationKeyframeMaskOrEligibleInput` is now named and verified after reopening. Its complete 58-instruction body returns false for null or non-Animation objects. For keyframes it tests object mask bits excluded by a referenced object's mask, then scans input records that can set the boolean result. All six discovered direct argument/result neighborhoods were inspected, spanning update, dependency marking and animation evaluation. Live enum/type registration identifies Animation kind 9, and live field registration identifies `IsKeyframe` at `+0x134`.

Only the descriptive name changed. Mask enum meanings, input-record mode semantics, concrete types and complete caller behavior remain unresolved. There are 142 checked descriptive names among 9,553 discovered functions; no full-behavior completion credit was added.

The earlier Timeline-chain divisor is now linked through live offset initializers and field registration to `PlaybackSpeed` for Sound and Timeline. A second chain producer and an adjacent bit-6/7 producer were also checked against 111 native instructions. Surrounding record selection, flag resets and other object-kind bindings remain unresolved.

### Animation predicate prototype and mask inheritance

The predicate now has a verified boolean return and three native arguments: two opaque context pointers in RDI/RSI and a packed integer identifier in EDX. A cold-copy trial preceded the live correction. Only this signature changed among 9,553 functions, its 58 native instructions remained unchanged, and reopening confirmed the saved signature. The trial caller now expresses the result as a boolean; concrete context structures remain unresolved.

Simulation preparation builds the mask array from each object's byte at `+0x22`. Mode-0 objects with a valid `+4` reference also inherit that referenced entry's mask. The keyframe predicate tests for bits absent from the referenced mask, connecting its test to the inheritance mechanism. The reviewed loop initializes entry zero and processes the remaining entries in ascending order. The original meaning of the mask bits and a guarantee that referenced entries precede dependents remain unproven. Other mask producers still need review.

This adds a justified prototype and bounded behavior evidence, with no new checked names, runtime validation or full-function completion credit.

### Main-loop mask update and developer-source lead

A further 102 live native instructions verify the main loop's mask inheritance path. It reads object byte `+0x22`, optionally combines the referenced mask for mode-0 objects, and stores the resulting context mask separately. A later gate can clear the object's byte before storing the already computed context mask. The neighboring byte `+0x23` uses a different owner array and separate combination logic; it is not treated as the Animation predicate's mask. Gate meanings, entry conditions and runtime consequences remain unresolved.

The source frame at 20:41 of Media Molecule's [Liam coding stream](https://www.youtube.com/watch?v=IvGbhvZsTa8&t=1241s) was visually inspected. It shows an unfinished physics-tool update body and a hovered-object helper. Searches of cached decompilation found no matching source labels. This is a research lead, not a verified function match: the cache and historical stream cannot establish the current executable's source identity. No streamed names or additional completion credit were applied.

### Animation mask reference validation

The mask-clearing gate is now linked to its prepared reference lookup: 80 current consumer instructions and 55 producer instructions were reviewed. A nonzero object mask is retained for mode 0; other modes require a valid referenced identifier and a matching prepared entry. Mode 1 uses a presence field, while other modes use a one-based record index and verify that record's mode byte. References outside the lookup-table range fall back to a scan matching the full identifier and mode; exhaustion clears the object byte.

Simulation preparation builds that table from the same records, with separate index fields for mode-1 and other records. Another record byte controls two packed flags; it is not conflated with the mode byte. Original mode/record names, index-capacity invariants and runtime implications remain unresolved. This is bounded static behavior evidence, with no new checked names or full-function completion credit.

### Indexed resource records used by Animation

`GetResourceTreeRecord72ByOrdinal` is named and verified after reopening. Its full 100-instruction, 339-byte native body walks resource-tree leaves and selects a 72-byte record by ordinal. All three direct caller argument/result neighborhoods were reviewed; they use an object resource index and a descriptor ordinal, then inspect record type, flags or timing data. The leaf-count arithmetic was checked for every possible 16-bit header value.

The name describes verified mechanics, not a recovered source symbol. Negative-ordinal, resource-capacity and iterator-depth assumptions remain unresolved. The record's full layout and source type are unproven, so no concrete types or full-behavior completion credit were added. There are 143 checked descriptive names among 9,553 discovered functions. This helper remains outside the subsystem map until its broader ownership is established.

A separate 76-instruction review of the Animation evaluation entry verified predicate bypasses for power and time-window gates. Native unordered floating-point comparisons can pass these gates where an ordinary pseudocode comparison would suggest otherwise. Later evaluation paths remain under investigation.

### Animation playback modes linked to runtime gates

Live field registration now identifies 33 Animation properties used to interpret the evaluation path, including `HeaderAndDataPages`, `Playhead`, `PlaybackMode`, `Reverse`, `Relative`, `PlayheadDelta`, and `LoopOverlapFraction`. The playback enum registration links values 0–3 to `PLAYONCE`, `SUSTAIN`, `LOOP`, and `PINGPONG`.

This resolves previously unnamed branches: PLAYONCE with `PlayingInternally` overrides effective power to 1; PINGPONG expands the upper playback window to twice the maximum minus the minimum. In the reviewed later branch, an ordered playhead beyond the maximum is reflected about that maximum when the input and object identifiers differ. `Reverse` can then reflect the position about the interval midpoint under the identifier condition. Native floating-point branch behavior remains authoritative, including unordered comparisons.

These are property-registration and bounded runtime findings, not full Animation completion. Record types, producer invariants and the remaining evaluation branches still need review. No additional names, concrete structure types or full-behavior completion credit were added.

### Animation delta helper named and saved

`EvaluateAnimationDeltaOnBaseValue` now describes the helper that samples a record twice, computes a type-dependent difference, and applies it to a supplied base value. The scalar, two-, three-, and four-component paths and the quaternion path were reviewed in native code. Both direct call sites are in the Animation property evaluator; a conditional first result can become the base input to the second call. Its route uses `PlayheadDelta` and a successful base-property read. Complete loop-boundary behavior and remaining conversions are still unresolved.

The descriptive name survived a clean reopening, all 1,663 native instructions and both direct references were unchanged, and the full name inventory matched the baseline plus recorded changes. The prototype remains uncorrected. This adds one checked name and one evidence-supported Animation mapping: 144 checked descriptive names overall, with 1,601 mapped functions and 7,952 still unmapped. It adds no full-function behavior completion credit.

### Shared tagged-value conversion named

`ConvertTaggedValueToTwoFloat4Blocks` is now named after reviewing its complete 32-instruction body and all 13 direct caller argument/result neighborhoods. Callers copy its 32-byte output, use both blocks in Animation sampling and blend math, compare them with reference values, or unpack eight components for a callback. The name describes the observed conversion; original structure names and complete caller behavior remain unresolved.

After a cold backup, only the name changed. A clean reopening verified that name, all native instructions, and the full direct-reference list. The prototype remains unchanged. The function is mapped to shared property data rather than credited exclusively to Animation. There are now 145 checked descriptive names and 1,602 mapped functions; no full-behavior completion credit was added.

### Animation strength interpolation helper named

`InterpolateTaggedValueFromBase` now names the shared strength helper at `1411dd230`. Its 302-instruction body and all 26 direct argument/result neighborhoods across 21 sampler functions support this role. The strength input was traced to the registered `AnimStrength` field, including nine predecessor paths outside the original inspection windows. Quaternion and Position paths have dedicated rotation interpolation; other tags delegate to weighted tagged-value blending and restore the target metadata.

The change affects only the name. A cold backup preceded it, and a clean reopening verified the name, unchanged instructions, all direct references, and unchanged prototype. The complete function-name inventory and both original archive hashes were also checked. There are now 146 checked descriptive names and 1,603 mapped functions. Mixed-type conversions, input ranges, and complete sampler behavior remain unresolved; no full-behavior completion credit was added.

### Animation registration names and property IDs

The 42-instruction `RegisterAnimationTypeDescriptor` and 307-instruction `RegisterAnimationFieldOffsets` now have checked descriptive names. The initializer binds the executable's `Animation` literal to its descriptor, installs callbacks, links its base, and invokes the field registrar. The registrar supplies the named field offsets and constructs its blend-type field record. Both changes are names only, backed up before application and verified after a clean reopening; native instructions, prototypes and reference addresses are unchanged.

The startup property-offset matrix independently links 27 Animation property IDs to registered field names. For example, `0x238` maps to AnimStrength at object offset `0x14c`, `0x2e4` and `0x2e5` map to Reverse and Relative, and `0x4b` through `0x4e` map to Playhead, StartTime, EndTime and PlaybackSpeed. The last four share a packed constant store whose register provenance was traced through an uninterrupted native sequence.

The three easing-strength properties (`0x32d` through `0x32f`) use class 23 in the shared property metadata table. That connects their registered fields to the scaled signed-byte storage selector audited above. It does not prove that every property has animation records or that every sampler route is understood. IsKeyframe, PlayheadDelta and remaining property links still need tracing.

There are now 148 checked descriptive names, with 107 among the 1,603 mapped functions. Original archive hashes and the complete function-name inventory passed verification. No full-behavior completion credit was added.

### Shared interpolation enum corrected

The executable registers `EBlendType` as None (0), Linear (1), EaseIn (2), EaseOut (3), EaseBoth (4), and LAST (5). Animation's BlendType field at offset `0x148` binds this descriptor; its adjacent boolean at `0x149` is a separate field. The descriptor is also referenced by shared Thing property registration.

Reading the three complete enum registration/append bodies and their descriptor references exposed an earlier classification error: the type name had placed these three functions under rendering. They now sit under shared property data as interpolation modes. This corrects ownership only; none is newly counted as understood or named. The relationship between these enum values, Animation's runtime reads and packed sample curve bits remains unproven.

### Animation easing curve helper named

`EvaluateAnimationEasingCurve` now names the complete 66-instruction helper at `140705ae0`. It reads Animation's BlendType and three easing-strength fields. Linear returns its input; None and values outside the four recognized modes return zero. EaseIn returns `x^p`, EaseOut returns `1-(1-x)^p`, and EaseBoth uses the corresponding two-sided curve, where `p = 1 + 7 * strength^2.807354927` and the stored signed-byte strength is scaled by approximately 0.01.

Both direct calls occur in the same runtime routine. Their reviewed neighborhoods compute timeline fractions, clamp them to 0…1, and select an object checked against Animation kind 9; one complements the curve result afterward. This connects the curve to timeline weighting, but earlier object-validity invariants and the complete enclosing routine remain unresolved. Matching the packed-record sampler formulas does not prove direct copying of the enum into sample bits.

A cold backup preceded the name-only change. Clean reopening verified all 332 body bytes, reference addresses and the unchanged prototype. The complete function-name inventory and original archive hashes also passed verification. There are now 149 checked descriptive names, with 108 among 1,604 mapped functions. No full-behavior completion credit was added.

### Animation easing signature corrected

`EvaluateAnimationEasingCurve` now has the verified signature `float (void * animation, float fraction)` using PS4 System V register storage: the object pointer is in RDI, the fraction and result use the low float lane of XMM0. The pointer remains opaque because a complete Animation structure has not been reconstructed.

An isolated project trial compared the helper and its enclosing caller before and after the correction. Both direct call sites now pass the object pointer and scalar fraction correctly, removing misleading integer argument and result casts. A fresh cold backup preceded promotion. Only this function's signature changed; all 332 native body bytes remained unchanged, and clean reopening verified the saved signature. Checked-name counts and full-behavior coverage are unchanged. Runtime validation and the settings-to-packed-sample producer connection remain unresolved.

### Animation serialization and shared buffer service traced

Animation's serializer transfers BlendType and all three easing-strength fields as raw bytes, under internal format-version checks: BlendType at version 255 or later, strengths at 1081 or later. Native kind 9 dispatch links the routine to Animation. These field transfers do not establish how the runtime 12/24-byte sample controls are generated.

`ServiceSerializerBuffer` now names the complete 81-instruction shared buffer helper. It services exhausted read buffers or pending writes through a callback receiving context, callback data and an operation flag. Success resets cursor/checkpoint state; failure retains an error, invokes cleanup and clears callback resources. The original callback types, individual error-code meanings and secondary-context path remain unresolved.

A cold backup preceded the name-only change. Reopening verified its 343 body bytes, references and unchanged prototype; the complete name inventory and original archives also passed checks. There are now 150 checked descriptive names, 109 among 1,605 mapped functions. No runtime-validation or full-behavior completion credit was added.

### Shared block lifetime and serializer block callback traced

`ReleaseRefCountedBlockHandle` now names the 23-instruction shared block-handle cleanup helper. It clears a null handle normally; otherwise it atomically decrements the block reference count and, when that reaches zero, releases a nested handle, adjusts allocation counters and calls the final release routine. Original symbols and complete ownership/concurrency invariants remain unresolved.

The serializer callback was read through its two read paths and write path. External reads require a four-byte length and an exact payload read; block-list reads fetch a recorded entry. Positive decode results establish the readable buffer end. Native checks and nine observed status paths are documented locally. The codec implementation and original error-enum names are not fully recovered.

The allocator import was independently identified as calloc through its calculated PS4 NID, loader assignment and thunk. Under the explicit condition that the callback allocation returns null, native control flow reaches an unguarded low-address read after cleanup. This is a conditional static finding; no runtime crash was reproduced and no game code was patched.

A cold backup preceded the cleanup helper's name-only change. Reopening verified its body bytes, all 105 reference addresses and unchanged prototype. All 151 descriptive names and the original archives passed verification. There are 110 checked names among 1,606 mapped functions; no full-behavior completion credit was added.

### Serialized-block LZ4 decoder identified

`DecodeLz4Block` now names the 556-instruction decoder used by the serializer block callback. Its token nibbles, extended lengths, 16-bit backward offsets and match lengths agree with the upstream [LZ4 block format](https://github.com/lz4/lz4/blob/dev/doc/lz4_Block_format.md). This identifies a format and descriptive role, not an exact original symbol or library version.

Animation loading selects the input-sized checked mode, supplying the output base and no earlier external dictionary. The two short-offset tables were verified against native constants; symbolic comparison with independent byte-by-byte expansion passed for offsets 1–7 and lengths 4–256. Remaining vector and byte-copy paths were read, with conditional buffer-slack reasoning recorded locally. These model checks do not execute the binary or prove safety for all malformed inputs. Zero offsets, alternative dictionary/mode variants and arithmetic extremes remain unresolved.

A cold backup preceded the name-only change. Clean reopening verified all 2,254 body bytes, nine reference addresses and the unchanged prototype; all 152 descriptive names and original archive hashes passed verification. There are 111 checked names among 1,607 mapped functions. Full-behavior coverage is unchanged. This serialized-block decoder does not identify how Animation's packed sample controls are generated.

### Animation property metadata lookup and registration

Native review verified all 98 instructions of a shared property lookup and 89 instructions of its table-registration callback. The lookup includes Animation blend mode in its hash, along with the object kind and property identifier. The same mixer addresses 8,192 records of 12 bytes each; static sentinel records were independently read back. These are executable-image observations, not a runtime table snapshot.

Registration matches the property, kind and variant byte, while lookup compares property and kind after hashing the variant. Table population and collision invariants remain unresolved, so this difference is not presented as a defect. The callback entry is referenced by a function pointer but has no defined function in the current project; it has not been created or named from a guessed boundary.

A separate property visitor reads the three signed easing-strength bytes and forwards converted values through an indirect visitor call. Neither path establishes how packed Animation sample controls are generated. No names, subsystem mapping counts or full-behavior coverage were increased for this investigation. Raw native evidence remains local.

### Shared property lookup named after native review

`FindThingPropertyMetadata` now describes the 98-instruction lookup reviewed in the preceding checkpoint. Its complete native body, all six specialized object-kind dispatch paths and static sentinel records were verified. Related registration code establishes the shared key and record layout. The name identifies its descriptive role; it does not assert an original symbol, full table-population correctness or a packed Animation sample writer.

A cold backup preceded this name-only change. Clean reopening verified the unchanged 324 body bytes, 17 reference addresses and prototype. The full inventory now contains 153 checked descriptive names, including 112 among 1,608 mapped functions. Original archive hashes are unchanged. No full-behavior completion credit was added; the variant matching difference and sample-control producer remain unresolved.

### Animation timed-record merge path traced

Native caller and jump-table review now ties a 12-byte timed-record writer to Animation descriptors. The parent selects Animation objects, walks their descriptor resource tree and dispatches four record-type cases to this writer. Reviewed write paths copy timestamp, payload and control data into resource pages while applying a time offset and updating used-byte counts.

At one near-equal timestamp boundary (strictly less than approximately 1/60 second), native masks preserve the existing record's easing-strength bits while conditionally combining lower control flags with the incoming record. A separate boundary path can select control nibble 9 or clear the low nibble under reviewed flag conditions. This establishes control modification during merging; it does not yet identify where the incoming controls were originally generated.

The full 194-instruction parent and selected writer regions were read. The writer's captured 1,081 instructions are not counted as fully understood. Remaining prefix/suffix paths, ownership, failure behavior and the source-buffer producer are unresolved. No speculative name, mapping increase, runtime validation claim or full-behavior credit was added.

### Signed-byte Animation sample controls traced to conversion

The upstream buffer builder and numeric dispatch now identify a signed-byte sample conversion path feeding Animation record merging. Native jump-table reads connect numeric representation class 23 to the converter. Its packed branch forms 12-byte timestamp/payload/control records; the separate flag-zero path keeps an 8-byte source representation. Reviewed comparisons use signed-byte values scaled by approximately 0.01.

Packed controls start with `0x700`, supplying strength nibble 7 in bits 8-11. Recording configuration adds low control flags; the single-sample branch also adds a mode-dependent bit 5. This identifies a source of the previously observed default strength, rather than treating it as recovered from the Animation gadget's separate easing-strength properties. It does not establish identical behavior across every recording representation.

Several branch and helper bodies were absent from Ghidra's defined-function output. Temporary disassembly in an isolated project copy recovered their native instructions; the transaction was rolled back and bytes were checked against live program memory. The converter and 12-byte append helper were read, including duplicate filtering and capacity checks. Capacity exhaustion can leave a partial append; caller capacity guarantees and the intended output-time contract remain unresolved.

No new function definitions, names, types, mapping counts or full-behavior credit were added. Raw code and detailed branch evidence remain local.

### Timed byte recording writer named

`RecordTimedByteProperty` now describes a reviewed 170-instruction recording helper. It initializes the recording header, appends timestamp-plus-byte records, replaces matching records in selected modes, and marks the recording slot when its capacity guard rejects an append. Two checked callers supply Boolean values. This name does not assert that the helper produces signed strength samples.

A hash-verified cold backup preceded the name-only change. Clean reopening verified all 737 body bytes, 16 references and the unchanged signature. The inventory now contains 154 checked descriptive names, including 113 among 1,609 mapped functions. Original archives are unchanged; no full-behavior completion credit was added.

Related local analysis recovered signed-byte conversion and eight-/twelve-byte append helpers in an isolated copy. Correct PS4 argument storage restores control writes omitted by default pseudocode. Raw recording headers consume ten bytes per sample: under a valid 512 KiB extent, at most 29,126 eight-byte samples produce 349,512 converted bytes. This is conditional arithmetic, not proof of every producer invariant. The separately reviewed generic producer's sole direct caller records property 0x231 with a 36-byte payload; it is not evidence for the signed-strength writer. Producer-wide limits, gate helpers, time conversion details and runtime validation remain open.

### Recording eligibility, timing and byte filtering verified

The recording gate now has an evidence-supported Boolean return and four arguments using the executable's PS4 calling convention. All six direct callers test the returned low byte. The gate checks selected recording modes and state, prepares timing for an empty recording slot, and can issue a notice. It is not merely a predicate. A cold backup preceded the type correction; clean reopening verified all 160 instructions, six references and successful caller decompilation. Its original name and several state meanings remain unresolved.

Native timing instructions show that the byte writer separately quantizes the current clock and recording origin on an approximately 30 Hz grid, subtracts their integer ticks, then converts the difference to seconds. Mode 2 instead writes a zero timestamp. Floating-point rounding at boundaries and exceptional values still need investigation; this local conversion does not establish the update rate of the entire engine.

Jump-table reads also show that the byte writer's filter type 255 and the three easing-strength properties' representation class 23 select a zero-return path without reading or modifying the payload, after an instrumentation call. This does not prove that every producer accepts unrestricted values or that the instrumentation has no side effects. The actual signed-strength recording producer remains unidentified.

These findings improve the recording model without adding completed behavior. Counts remain 154 checked descriptive names, 113 checked among 1,609 mapped functions, and 7,944 functions awaiting subsystem mapping. Raw code, local paths and detailed native evidence remain local.

### Float recording arguments and channel selection verified

The neighboring timed-property writer now has a corrected seven-argument signature, including its float value in the first floating-point argument register. All ten direct caller windows were checked against live bytes. The complete 167-instruction writer stores an 18-byte record containing the object handle, property, timestamp and four-byte value. It shares the separately quantized 30 Hz clock conversion previously verified for byte recording.

Two callers first use a fully reviewed 26-instruction helper to select the signed value with greatest absolute magnitude from five consecutive float channels. Strict comparisons retain the earlier candidate on ties. The initial ordered comparison masks an initial NaN or zero to positive zero; later NaN candidates do not win. The five channels' original meaning and the property names remain unresolved.

An isolated signature trial preceded the working-project change. A hash-verified cold backup and clean reopening confirmed that the corrected signature persisted, all 726 body bytes and ten references remained unchanged, and decompilation succeeded. The complete name inventory and original-file checks passed. No additional descriptive names, subsystem assignments, runtime validation or completed-behavior credit were added.

### Five float recording value selector named

`SelectGreatestMagnitudeOfFiveFloats` describes a fully reviewed 26-instruction helper used by two timed float recording callers. It preserves the sign of the strongest input, visits channels in the order 1, 2, 3, 4, 0, and retains the earlier candidate on equal magnitudes. The native audit records the initial zero and NaN handling and the ordered comparisons. The meanings of the five channels remain unresolved; this is a descriptive name, not an original symbol.

A hash-verified cold backup preceded this name-only change. Clean reopening verified the unchanged 122 body bytes, two references and signature. The full inventory and both original archive hashes passed verification. There are now 155 checked descriptive names, including 114 among 1,610 mapped functions; 7,943 functions remain unmapped. This helper review adds no whole-game behavior completion credit.

### Float property recording and persistence audit

`RecordTimedFloatProperty` now names the reviewed float recording writer. Its complete 167-instruction body and all ten direct call sites were checked against current native bytes. It writes 18-byte records containing an object handle, property identifier, payload length, timestamp and float value. Mode 2 replaces the first matching record at time zero; mode 5 replaces using calculated time; other permitted modes append. Capacity checks occur before replacement. Buffer extent integrity and compatible record widths are assumed. Mode meanings, gate side effects, property meanings and numeric edge cases remain unresolved; the `0xff` sanitizer path does not validate the float payload.

`SelectGreatestMagnitudeOfFiveFloats` also now has the supported `float (float * values)` signature under PS4_SYSV: input pointer in RDI, float return in XMM0. An isolated trial was rolled back before promotion. Both metadata changes were made together after a hash-verified cold backup. Fresh-process readback verified 848 unchanged native instruction bytes and all 12 references. All 9,553 inventory entries and both original archive hashes passed verification.

The persistence checks now require an observed stopped process, closed service listeners, a newly created process with a distinct run ID, the expected loaded program hash, and matching process/listener identity before and after the metadata reads. Without this evidence the general verifier reports current metadata only. Nine focused failure-path tests passed. This addresses a provenance gap in the prior verifier, whose clean-reopen assertion relied on separate external observations.

There are now 156 checked descriptive names, including 115 among 1,611 mapped functions; 7,942 functions remain unmapped. These changes add no whole-game behavior completion credit or runtime validation.

### Recording modes, eligibility and stored Animation data

The executable's `ERecordMode` registration identifies 0 None, 1 Animation, 2 Keyframe, 3 Microphone, 4 Sound, 5 AutoKeyframe, 6 Possess, 7 Simulation and 8 LAST. Native field registrations bind this enum to `Machine.record_mode` and `Player.last_used_record_mode`. The reviewed caller carries that exact Machine field into the byte and float writers. This resolves the earlier unknown names for numeric modes 2 and 5; it does not establish every mode transition or caller.

| Mode in the reviewed property-recording path | Established behavior |
| --- | --- |
| Keyframe | Replace the first matching object/property record at timestamp zero, or append if no match exists. |
| AutoKeyframe | Replace the first match using the calculated recording timestamp, or append if absent. |
| Animation, Possess, Simulation | Use the stateful eligibility gate and append when the writer permits it. |

These results concern the reviewed writers and caller path. Their buffer header value 2 is a separate format discriminator, not the Keyframe mode number. Microphone and Sound processing are outside this traced property-recording path.

`PreparePropertyRecordingIfEligible` names the 160-instruction gate. Its threshold field corresponds to the game's `AnimPageData` thermometer category, and its timer is registered as `possess_countin`. The gate can request `force_tick_sim_next_frame_due_to_recording`, clear a flag that suppresses audio-ring processing, and initialize `recording_start_time` from the Animation playhead or parent timeline. All six direct callers immediately test AL and skip recording on zero. Native floating-point comparisons retain their ordered/unordered distinction; threshold calculation, translated notification text, tick-flag lifecycle and the physical audio source remain unresolved.

The downstream trace follows the reviewed sample merge into page types explicitly labeled `ANIMATION` and `ANIMATION_HEADER`. It finalizes both resource trees, returns their updated roots and a descriptor ordinal, and reaches submission of the two resource identities through property `0x2fe`. The existing `FinalizePackedResourceTreeWriter` name is retained. The follow-up below traces selected float source conversions, property installation and resource serialization; complete merge correctness, the outer scene-save path and runtime behavior remain unresolved.

`RegisterRecordModeFieldOffset` and `AddRecordModeEnumValue` name the two fully reviewed registration helpers. The map places these shared recording controls under Editor & interface / Editing & tools, preserving their Properties & type definitions role. This classification follows the Machine and Player field uses; it does not claim that the helpers draw UI or run exclusively in the editor.

The three names were applied in one backed-up batch. Fresh-process verification checked 1,997 unchanged native instruction bytes, 26 references, unchanged signatures apart from the names, the complete 9,553-function inventory and both archive hashes. There are now 159 checked descriptive names, including 118 among 1,612 mapped functions; 7,941 functions remain unmapped. No whole-game completion or runtime-validation credit was added.


### Float samples, property installation and resource serialization

The float path is now traced independently of byte recording. Seven reviewed property IDs reach the native float converter through their recorded type and numeric-class tables on the ordinary conversion branch. An earlier special conversion branch remains untraced. The reviewed converter consumes timestamp/float pairs, preserves the stored float bits, and can produce either 8-byte samples or 12-byte samples with control data. Equal intermediate values can be suppressed while endpoints and unordered NaN comparisons follow the native branches. This is not a claim that every float buffer reaches the same merge routine: the resource router selects among several writers according to descriptor and mode flags.

A later filter applies to properties `0xbc` and `0xc5`. It inspects float words at offsets `4 + 8*i` and can clear the output length when every inspected value compares equal to zero. Since conversion also supports 12-byte records, the eight-byte scan must not be described as a universal test of every converted sample without proving the format invariant.

The resource-pair command is connected to property storage. Its `0x2fe` dispatch-table entry leads to native code omitted from Ghidra's recovered function body. That branch transfers two 64-bit resource fingerprints into two local 32-bit page handles. With an explicit stored property, it updates the inline object field only when its value before conversion equals the old stored pair; a differing inline value is preserved. Without an explicit property payload, the offset-mapped inline field is the destination. The transfer helper assumes valid pointers, initialized resource tables, and sufficient buffer capacity; it is not a checked parser for arbitrary input.

Native initialization binds Animation property `0x2fe` to `HeaderAndDataPages` at offset `0x110`. The registered pair type identifies `Header` at relative offset zero and `Data` at four. For serialization versions at least `0x3a7`, the reviewed binary serializer processes Header and then Data through the same resource helper, with error checks between operations.

The output path writes the root fingerprint, visits resource pages while avoiding repeats, writes children before their parent, and ends a nonempty resource sequence with a zero byte. Leaf pages contribute 512 bytes; internal pages contribute their header and child fingerprints. Calls into stream servicing remain part of this path, so these observations are not a complete contiguous file grammar. The input path interns pages and resolves the root fingerprint to a local handle. A zero input fingerprint returns without assigning that handle. The follow-up below establishes its initial value on the reviewed construction path, with remaining preservation limits. Historical-format migration, outer scene containers, framing, compression and runtime round trips remain incomplete.

[Media Molecule's audio-tools talk](https://www.youtube.com/watch?v=-UyiXUJcIQ0&t=2963s) supplies a separate lead about animation-driven parameters participating in dependency ordering. It does not identify this binary's resource representation. The installation branch reviewed here does not establish how those dependency links are created or updated.

These are additional static data-flow findings. No additional function names, whole-behavior completion credit or runtime-validation credit were added in this follow-up.
### Eight-byte sample merging and serializer checkpoints

The alternate existing-track path is now traced for compatible eight-byte scalar samples. It preserves old samples before the incoming range, emits the incoming timestamp/value pairs, removes covered old samples, and retains the old suffix. It rebases timestamps to a common origin while preserving value bits. The boundary tolerance is approximately 1/60 second; this does not establish the engine's update rate. Native equality and unordered-comparison branches are recorded separately in the local evidence.

The writer finalizes both resource roots, appends a 72-byte descriptor, and returns its ordinal. Its input-count calculation can select a 12-byte divisor while its incoming loads still use an eight-byte stride, so compatibility of mixed-format calls remains an upstream invariant to prove. The follow-up below traces the scalar alternate-mode writer; new-track paths remain incomplete.

The generic binary object's Animation input branch clears newly allocated object storage and calls its initializer before selecting the Animation serializer. Two independently decoded type-table entries establish that route. The initializer explicitly sets both Header and Data handles to `0xffffffff`; the type factory uses the same empty pair. This establishes initialization at construction. Preservation across every intervening common-field helper and every reload path remains unverified, so it does not establish a universal result for zero fingerprints applied to arbitrary existing objects.

Resource serialization also has optional checksum checkpoints. For eligible spans from 4,096 through 720,896 bytes, the reviewed helper computes a zero-seed XXH32 hash and increments a counter. Versions at least `0x3d8` transfer a 16-bit checkpoint word; versions below `0x59a` mix the counter into that word. From version `0x649`, the next checksum span starts after the checkpoint word. A mismatching input checkpoint reports an error. These conditional words can occur between resource page transfers and must be accounted for in any reconstruction of the stream.

The generic byte-transfer helper copies across buffer boundaries. Its optional secondary transfer uses the signed low 32 bits of the original requested length, so bounded nonnegative lengths are a caller requirement. It adds no framing of its own; the service callbacks may do so. The follow-up below establishes scene input checkpoint setup and its callback route. Save-side policy, the secondary context's purpose, complete outer containers and runtime round trips remain unresolved.

This follow-up adds native behavior evidence without applying additional names or increasing whole-game completion credit. That trace follow-up left 159 checked descriptive names; no in-game verification is claimed.

### Animation initialization and serializer helper names

Three additional descriptive names are saved and verified: `InitializeAnimationObjectDefaults` (`14093f9d0`), `ProcessSerializerChecksumCheckpoint` (`140d92160`), and `TransferSerializerBytes` (`140d923e0`). Their complete native bodies establish the roles described above. The first initializes Animation object fields, including the empty resource-handle pair; the others process versioned checksum checkpoints and move bytes through serializer buffers.

These are name-only changes. Existing prototypes are preserved; a guessed shared prototype could affect many callers. A hash-verified cold backup preceded promotion. After a clean stop and fresh-process reopening, checks confirmed 1,280 unchanged native bytes, all 3,835 enumerated references, unchanged function metadata apart from names, the complete 9,553-function inventory, and unchanged original archive hashes. Enumerating references for preservation does not mean all those callers were semantically reviewed.

There are now 162 checked descriptive names, including 121 among 1,615 mapped functions; 7,938 functions remain unmapped. The initializer belongs to Animation and the two serializer helpers to shared engine serialization. No whole-game completion or runtime-validation credit was added.

### AutoKeyframe conversion and scene input policy

The alternate scalar writer now has a native trace showing eight-byte old samples becoming twelve-byte records with control data. Caller flags connect that route to AutoKeyframe in the reviewed ordinary conversion branch. Separate slot flags, special conversion paths, one timestamp-origin assumption and runtime playback remain unresolved.

The reviewed binary scene-input branch explicitly enables checksum checkpoints and selects the block-descriptor-list callback route. The same context is forwarded through the object list to the generic loader and established Animation path. This extends earlier callback and LZ4 findings; it does not count repeated analysis as new completion. Output setup, the complete container and runtime round trips remain open.

See [the detailed route table and conditions](ANALYSIS.md#autokeyframe-conversion-and-scene-input-policy). Checked names remain 162. No further naming or whole-behavior credit was added for these traces.

### Recording flags and serialization policy narrowed

Native review identified the builder's extra slot byte as `recording_possession`. The reviewed runtime writers constrain it to 0 or 1; raw-byte deserialization prevents extending that guarantee to all restored state. Twelve Animation constructor defaults were matched to registered fields.

The checksum-enabled scene input context is now restricted to its actual non-99999 format branch. A different output context explicitly disables checksums, but its connection to main scene saving remains unproved. This corrects the scope of the earlier policy finding without changing completion counts.

[Defaults, branch conditions and remaining work](ANALYSIS.md#recording-flags-construction-defaults-and-serializer-selection). Totals remain 162 checked names and 1,615 mapped functions; no runtime validation or additional completion credit.

### Four serializer names and a complete initializer contract

Saved four descriptive serializer-helper names and corrected the Animation initializer's opaque-pointer signature after native/caller review and an isolated trial. One cold backup covered the batch; fresh reopening preserved all 2,876 affected instruction bytes and 329 enumerated references. The original archives and full function inventory were checked.

The initializer's complete static contract adds 411 audited bytes independently of naming: conservative coverage is now **0.0052% (1,495 / 28,940,288 executable bytes)**. Totals are **166 checked names, 1,618 mapped functions and 7,935 unmapped functions**. No running-game or complete scene-save validation is claimed.

[Contract scope, names and evidence](ANALYSIS.md#animation-initialization-contract-and-serializer-helper-review).



### Version-record and alternate-stream trace

Traced the checksum-disabled inner payload to a version record, distinguished it from the associated Dream record and followed its copy into save/publish preparation. Separately identified the 99999-format branch's matching input/output streams and selected binary metadata operations. The nearby reference collector is now distinguished from the byte-stream writer.

[Evidence, corrected marker semantics and remaining format gaps](ANALYSIS.md#version-record-ownership-and-the-alternate-scene-stream). No runtime validation or extra whole-behavior coverage was added for these partial traces.


### Descriptor block helpers named and typed

Read the complete block-loader and block-flush bodies, checked their method-table ownership and caller register usage, and saved `LoadDescriptorInputBlock` / `FlushDescriptorOutputBlock` with tested working signatures. Fresh reopening preserved 1,185 native bytes and seven recorded references. The reader's low-byte success result and writer's capacity return are now distinguished explicitly.

[Findings, error-path limits and verification](ANALYSIS.md#descriptor-block-reading-flushing-and-return-values). Totals: 168 checked names, 1,620 mapped functions and 7,933 unmapped functions. Audited-byte coverage remains about 0.0052%; no runtime validation or additional completion credit.


### Reflected output helpers and array events

Saved four descriptive output-helper names and the primitive writer's low-byte status signature after complete owned-body review and an isolated trial. Native dispatch establishes unsigned/signed compact encodings and raw-width cases. The two output boundary callbacks are now tied to specific completed array/container traversals. Earlier float and composite-filter findings were reconciled rather than counted again.

Fresh reopening preserved 3,900 instruction bytes and 13 recorded references. Totals: 172 checked names, 1,624 mapped functions and 7,929 unmapped functions. [Encoding table, callback conditions and limits](ANALYSIS.md#reflected-value-encodings-and-array-boundary-events). Audited-byte coverage remains about 0.0052%; no runtime round trip is claimed.


### Reflected readers and conversion rules

Saved three reader-helper names and the primitive reader's tested six-argument, low-byte-status signature. Native tables and code establish integer range checks, numeric conversion families, Boolean normalization, checked reads and a float64 destination binding. Selected conversion models pass 3,565 cases under nearest-even rounding; target runtime state remains unverified. Overlong integer framing, stride/count guarantees and custom callbacks remain explicit gaps.

Fresh reopening preserved 3,565 instruction bytes and 207 recorded references. Totals: 175 checked names, 1,627 mapped functions and 7,926 unmapped functions. [Reader paths, models and limits](ANALYSIS.md#reflected-primitive-reading-and-conversion). Audited-byte coverage remains about 0.0052%; no runtime scene round trip is claimed.

### Composite loading and skipping

Seven descriptive names saved and verified after clean reopening. Field matching, inherited offsets, auxiliary objects, callback order and unknown-data consumption traced. Totals:182 checked names,1,634 mapped functions,7,919 unmapped. Types and native bytes preserved; audited-byte coverage unchanged. [Findings and open contracts](ANALYSIS.md#reflected-field-loading-and-unknown-data-consumption).

### Composite-reader signature verified

Applied the native-supported four-pointer, byte-status working signature after an isolated trial. The loader and three caller functions decompile successfully. Fresh reopening, full name inventory, native bytes, references and original archives checked. No additional names or completion credit. [Signature evidence and limits](ANALYSIS.md#composite-reader-working-signature).

### Chunk-stream callbacks defined

Three native callbacks now have verified function definitions and descriptive names. The span reader and skip adapters share chunk refill and actual-byte-count handling. Fresh reopening preserved489 native bytes,3 references and the full existing inventory. Totals:185 checked names across9,556 functions;1,637 mapped. [Behavior and limits](ANALYSIS.md#inline-chunk-stream-callbacks). Audited-byte coverage remains unchanged.

### Schema metadata helpers named

Five verified descriptive names added for schema allocation, raw name bytes, compact integers and read-hook cleanup. Native tracing distinguishes object registration from later field population and corrects schema reuse assumptions. Totals:190 checked names,1,642 mapped functions. [Evidence and remaining format contracts](ANALYSIS.md#schema-metadata-and-object-population). Byte coverage is unchanged.

### Outer record reader named

Saved and freshly verified `ReadReflectedStreamRecords` after full native role review. Totals: 191 checked names and 1,643 mapped functions. [Scope and open format contracts](ANALYSIS.md#outer-reflected-record-reader-named). No runtime or additional audited-byte credit.

### Read-resource cleanup named

Two cleanup roles saved and freshly verified, preserving types, code and references. Totals: 193 checked names and 1,645 mapped functions. [Resource lifecycle and remaining ownership contracts](ANALYSIS.md#reflected-read-resource-teardown). Audited-byte coverage remains unchanged.

### Name hash named

Saved and verified the shared name-ID helper after 970 arithmetic-model cases covering lengths 0–96. Totals: 194 checked names and 1,646 mapped functions. [Algorithm and validation limits](ANALYSIS.md#name-identifier-hash). No runtime or audited-byte credit added.

### Six helper signatures verified

Applied and freshly verified native-supported types for name spans, compact integers and chunk read/skip callbacks. All six helpers and three callers decompile successfully. [Contracts and limits](ANALYSIS.md#reflected-helper-signatures-verified). No new names or completion credit.

### Schema writer roles named

Two verified names added for dependency collection and object-record writing. Traced emitted schema order, field filters, metadata and object payload records. Totals: 196 checked names and 1,648 mapped functions. [Evidence and remaining format contracts](ANALYSIS.md#schema-collection-and-object-record-writing-named). Audited-byte coverage remains unchanged.

### Descriptor map helpers named

Three verified roles added for descriptor lookup, growth and ID insertion. Traced exact-pointer traversal suppression and shared probe rules. Totals: 199 checked names and 1,651 mapped functions. [Evidence and limits](ANALYSIS.md#descriptor-map-roles-named). Audited-byte coverage is unchanged.

### Descriptor map emulation checked

Captured lookup/insertion instructions passed 4,629 calls with reference-dictionary comparisons. Native growth/rehash preserved 300 entries across capacities 16–1,024 and 6,621 lookup checks with controlled allocation/free stubs. [Validation scope and limits](ANALYSIS.md#descriptor-map-instruction-emulation). This is instruction emulation, not running-game validation; no names or audited-byte credit added.

### Native reader emulation checked

Compact readers passed284 value/range and2,568 truncation cases. Connected native compact/chunk readers passed512 chunk cases and14 short/marker cases. Span/skip paths passed728 cases, including248 partial results. [Dependencies and validation limits](ANALYSIS.md#compact-and-chunk-reader-instruction-emulation). No running-game validation, new names or audited-byte credit claimed.

### Boolean reader failure behavior checked

The native scalar Boolean path passed 48 complete-read and 360 short-read cases for counts below 16. Short reads leave the transferred prefix unnormalized. Live code and constants were rechecked; vector execution remains unverified because of an isolated emulator mismatch. [Evidence scope and limits](ANALYSIS.md#boolean-primitive-conversion-and-short-reads). No completion credit added.

### Array and container control flow checked

Reviewed the complete field writer and passed 60 controlled orchestration cases across arrays and contiguous containers. Confirmed empty-value behavior, callback timing and failure propagation, and traced the concrete scene-input observer. [Findings and dependencies](ANALYSIS.md#reflected-array-and-container-event-contracts). Counts and completion coverage are unchanged.

### Native primitive writer connected to reader

Passed 1,199 connected native value cases and checked 1,871 short writes. Integer wire encodings matched an independent reference; Boolean normalization and selected float-bit preservation were confirmed. The writer ignores returned byte counts; caller-level error handling remains open. [Scope and limits](ANALYSIS.md#connected-primitive-writer-and-reader-validation). No whole-scene or game-runtime completion claimed.

### Composite field decoding connected

Passed 83 matching-array cases, 430 schema-mismatch/unmapped cases, 980 truncation checks, and 132 optional-mask checks with captured native writer/reader instructions and synthetic schemas. A following field verified alignment. Retained a separate noncanonical-Boolean skip limitation. [Evidence scope and remaining gaps](ANALYSIS.md#connected-composite-fields-schema-mismatches-and-optional-masks). Completion counts are unchanged.

### Native schema matching connected

Passed 1,548 connected writer/field-mapping/reader cases, plus 84 identifier-lookup cases and a 14-field load-plan fixture. Mappings now come from captured native lookup/build code in this test, including aliases and unknown fields. [Scope and remaining gaps](ANALYSIS.md#native-field-matching-connected-to-decoding). Real root schema parsing remains open; completion counts are unchanged.

### Concrete output stream errors traced

Checked 252 native encoder/buffered-stream cases, including 52 modeled flush failures, and live-verified selected save return paths. Stream errors and serializer status are separate; complete higher-level propagation remains open. [Verified behavior and limits](ANALYSIS.md#concrete-buffered-output-failure-contract). No game defect or added completion credit claimed.

### Two schema predicates saved

Two previously undefined source-schema predicates now have verified names and working signatures. Fresh reopening preserved their 152 bytes and the complete inventory; 504 synthetic predicate checks passed. Totals: 201 checked names across 9,558 functions; 1,653 mapped. [Behavior and limits](ANALYSIS.md#source-schema-predicates-defined). Audited-byte coverage is unchanged.

### Game container callbacks

Twelve previously undefined routines now have checked names and working signatures for storage, count, resize and append operations on Game Thing-reference, Wire and Body containers. Their complete native bodies contain 130 instructions in 661 bytes. Property registrations connect them to the generic scene serializer: loading calls resize before reading elements; saving calls count and storage. Wire entries occupy 64 bytes and Body entries 304 bytes. Initialization leaves some trailing bytes untouched; their meaning and caller-side bounds remain unresolved.

A cold backup and isolated definition/decompilation trial preceded promotion. A clean reopening verified all twelve names, signatures and native bodies, the full 9,570-function inventory and original archive hashes. Totals are 213 checked names and 1,665 mapped functions; 7,905 remain unmapped. This is storage and serialization progress, not proof that an actual scene round trip or the game works. AVX execution remains unverified. Audited-byte coverage is unchanged.

### Wire header representations and registration

Five registration helpers now have evidence-backed names: WireHeader fields, EProp fields, EditOp fields, signed32 fields and the wire blend-operation field. A separate prototype repair gives the existing Thing-reference registrar its actual descriptor, name and offset arguments, fixing misleading caller output. Cold backup, isolated trial and fresh reopening verified the changes; original archives and native bytes remain unchanged. The large Game registration caller exceeded the decompiler timeout; the six changed functions and smaller caller decompiled successfully.

WireHeader selects between overlapping source representations: flag bit0 selects a signed32 source port (mask16), otherwise an EProp source property (mask1). All256 synthetic native-selector cases passed, and the generic writer applies that mask to registered fields. The blend enum registers MaxAndModulateBase, MaxAndOverwriteBase and BlendAndBlendBase. Actual signal evaluation, blending math and a real-scene round trip remain unverified. Totals:218 checked names,9,570 discovered functions,1,667 mapped and7,903 unmapped. These are static review findings; audited-byte coverage is unchanged.

### Wire runtime lookups and sorting wrapper

Named and typed three Wire lookups and `SortGameWires` after connected native review. The destination-run lookup stops at a changed destination and requires matching source, property and source-port flag;1280 synthetic native cases passed. Two index lookups distinguish source-port matching from destination/property-only matching;4000 synthetic unsorted-path cases passed. The sorting wrapper passes the full64-byte Wire range to its implementation and then sets `wires_sorted`.

All four changes passed an isolated trial and fresh-reopen inventory, byte and archive checks. Sorted paths use AVX and remain unexecuted; partition/heap comparisons, packed-reference generations and caller grouping invariants remain open. This is lookup/storage behavior, not proof of signal evaluation or blending. Totals:222 checked names,9,570 functions,1,670 mapped and7,900 unmapped. Audited-byte coverage is unchanged.

### Wire normalization and cycle marking

Three connected routines now have checked descriptive names and working types: blend-mode normalization, Game/linked-Game wire preparation and logic-cycle edge marking. Normalization passed2048 synthetic native cases: the first non-blend mode in an eligible destination/property group wins. Update preparation sorts and normalizes wires and conditionally invokes cycle marking; primary and linked Games use different gates.

The isolated native DFS block passed2048 cases covering all512 directed graphs on three vertices, two traversal orders and premarked-edge handling. It marks Wire flag0x04 on back edges to active vertices. These cases supply prebuilt adjacency and do not validate graph construction, vertex ordering, allocation or the flag's effect on signal evaluation. Full runtime signal arithmetic remains untraced.

Cold backup, isolated trial and fresh reopening verified all three names/types with unchanged native bytes and original archives. Totals:225 checked names,9,570 discovered functions,1,671 mapped and7,899 unmapped. Audited-byte coverage is unchanged.

### Typed signal reduction and Wire blend accumulator

Named `ReduceTypedSignalToScalar` and `AccumulateWireSignalByBlendMode` with conservative working types. The reducer returns a float in XMM0; correcting its inferred integer return removes misleading casts in the connected caller.1360 captured native direct-scalar/default-zero cases passed, including arbitrary NaN, infinity, signed-zero and subnormal payload bits. This does not validate other reductions or broad SIMD behavior.

The property updater supplies Wire blend-mode byte+0x31 to the accumulator for property-source wires. Its mode branches scale/reduce typed inputs and delegate maximum/weighted combination to other helpers; those helpers and base-property application remain incomplete. One weighted helper still needs its stack-passed value arguments reconstructed. No running-game signal correctness is claimed. Cold backup, isolated trial and clean reopening preserved native bytes and original archives. Totals:227 checked names,9,570 discovered functions,1,673 mapped and7,897 unmapped. Audited-byte coverage is unchanged.

### Connected typed signal conversion and combination

Named `ConvertTypedSignalInPlace`, `MergeTypedSignalsByMaximumMagnitude` and `BlendTypedSignalsByWeight` after native body/caller review, cold backup, isolated trial and independent project reopening. The weighted helper now receives both40-byte value inputs correctly in the decompiler. All9,570 function entries were checked; only the three intended name/signature entries changed, and original archives remain unchanged.

511 full-entry/return synthetic native conversion cases establish same-tag preservation and conversion to numeric tag23. Separately,1,352 isolated signed64 maximum-branch cases establish greater-magnitude selection, second-on-tie selection and clamping a negative winner to zero. These checks do not cover all conversions, generic SIMD selection or the running game. Weighted normalization control flow is traced statically; its rotation-like helper uses an approximately−0.01 sign-flip threshold and identity fallback, with special-value behavior still unresolved.

Totals:230 checked descriptive names,1,676 mapped functions and7,894 unmapped. These are naming/mapping counts. Audited-byte coverage and game-runtime verification remain unchanged.

### Original Variant types and Impact decoding

Recovered all 32 original `EVariantType` labels and connected their enum descriptor to the Variant type byte at offset 36. The float at offset 32 is registered as `alpha`. [Recovered values and conservative layout](analysis/variant-types.json) now identify Quaternion, Impact, PlayerValue, Timestamp and other previously anonymous numeric paths.

Installed a conservative 40-byte Variant layout and 20-byte Impact decoder output layout, preserving opaque payloads, padding and unknown subfield meanings. Six working signatures retain their verified argument locations, including both stack-passed Variant values. Named the Impact decoder and three enum registration helpers. Independent reopening confirms all 9,570 entries, only the intended nine name/signature entries changed, unchanged native instructions and intact original archives. A misleading raw-copy numeric float cast in the pseudocode is annotated with the assembly behavior; generated C is not a faithful source reconstruction.

Both maximum and weighted type-selection prefixes agree for every 256 × 256 byte-tag pair (131,072 scoped native prefix checks). Another 125 prepared-branch cases establish that equal identifier-like tags produce a Bool signal from payload truthiness. These checks stop before downstream conversion and do not establish valid runtime inputs or complete function behavior. The generic floating-point selection remains unverified: both emulator versions reject its blend instruction, and a comparison probe disagrees for a subnormal value even with an explicit floating-point control setting. No instruction shims were counted as native evidence.

Totals: 234 checked descriptive names, 1,677 mapped functions and 7,893 unmapped. Audited-byte coverage and game-runtime verification remain unchanged.

### Connected Variant vector and quaternion extraction

Named `ExtractVariantVectorComponents`, `ExtractVariantFloat4Components` and `ExtractVariantQuaternionComponents`, replacing misleading inferred integer returns with conservative 128-bit XMM0 working return layouts. The connected conversion, weighted blending and vector-operation callers now consume explicit vector results. The layouts preserve the source-dependent fourth lane and do not claim original C++ declarations.

3,072 scoped native entry-to-return cases validate selected direct-copy paths and input preservation across these helpers. The generic XYZ helper has 24 captured direct call sites, the four-component helper has 12, and the quaternion helper has one. Full callers, scalar fallbacks and nonlinear conversion math remain incomplete. The quaternion-oriented Float3 path uses +Y basis constants; its familiar rotation interpretation requires finite unit input, which this helper does not enforce. Arbitrary inputs need not yield normalized quaternions.

Cold backups, isolated trials and independent reopening verify the repaired register returns, unchanged native code, all 9,570 function entries and intact original archives. A Media Molecule coding-stream lead, [The Tech Behind The Magic](https://www.youtube.com/watch?v=yZM_Ij9aeOA), is recorded separately: only official metadata was accessible; no visible source or binary match is claimed.

Totals: 237 checked descriptive names, 1,680 mapped functions and 7,890 unmapped. Audited-byte coverage and game-runtime verification remain unchanged.

### Splitter and Combiner output behavior

Named `ReadSplitterOutputVariant` and `BuildCombinerOutputVariant` after matching original gadget field registrations to their native reads and the connected property-output dispatcher. These are gadget output helpers, beyond property registration. Splitter reads its InputA Variant; Combiner uses its FatWireType selector and input properties. Both use the original RotationRepresentation enum: YawPitchRoll or AxisAngle.

2,816 full native entry-to-return Combiner cases establish selected component assembly from Number inputs: first matching input wins, missing inputs become zero, and unused output bytes remain unchanged. Another 4,608 Splitter cases establish generic vector component extraction, missing-component zeros, Signal output type and alpha 1. Inputs remain unchanged in these synthetic cases. These checks do not establish valid gameplay reachability of every synthetic fixture.

Rotation conversions, Position/Impact/PlayerValue/Timestamp special paths and complete running-game behavior remain unresolved. The Number/Signal difference branch is traced statically. Reused stack storage caused Impact field names to appear in a Timestamp path; the project now annotates that decompiler artifact. Cold backup, isolated trial and independent reopening verify both names and working arguments, unchanged native code and original archives, and all 9,570 function entries.

Totals: 239 checked descriptive names, 1,682 mapped functions and 7,888 unmapped. Audited-byte coverage and game-runtime verification remain unchanged.
### Calculator native behavior checkpoint

Named and typed the shared normalization helper after reviewing its complete native body and five calls from Calculator. Its unordered length branch handles NaN using the same equal-component fallback as zero/small vectors; the decompiler condition omitted that case.

179 isolated original-instruction hardware cases passed:23 Number cases,128 vector component arithmetic cases,21 direct normalization helper cases and7 special Float3 cases. The result check uses the original supplied library implementation, rather than a replacement stub. Tested comparisons scale and round inputs before comparing. These are selected synthetic cases, not full Calculator completion or a running-game test. Angle-between-vectors, exceptional special inputs, other value types, timestamp and revision-sensitive math remain unresolved.

240 descriptive names checked;1,683 functions mapped,7,887 unmapped. Audited-byte coverage is unchanged.
### Calculator output wrappers and timestamp behavior

Named and independently reopened both Calculator output wrappers, matching their registered fields and property-dispatch callers. Wide Calculator folds available inputs in port order; the standard wrapper returns zero for operation IDs 33–38, including NotEqual despite its core branch. UI reachability remains unresolved.

The expanded isolated native suite passes 2,928 cases: 23 Number cases, 128 vector arithmetic cases, 21 normalization helper cases, 10 special Float3 cases, 1,053 Timestamp cases, 1,533 Wide Calculator wrapper cases and 160 standard wrapper cases. Original acosf code handles the tested axis angles. Native timestamp comparisons use signed 64-bit ordering; addition wraps and subtraction clamps according to the wrapped signed result. The unsigned-looking pseudocode is misleading.

These tests use selected synthetic inputs and original instructions, not a running game. Other value types, exceptional inputs, mixed conversions, revision-sensitive Power and remaining math branches are incomplete. No audited-byte credit added. Totals: 242 checked names; 1,685 mapped functions; 7,885 unmapped.
### Shared Calculator core and compatibility behavior

Named the shared evaluator called by both Calculator wrappers, preserving its established six-argument working ABI and by-value Variant inputs. Independent reopening verifies the descriptive role name and unchanged native instructions. This is role identification, not a claim that every operator/type combination is fully understood.

The native suite now passes 3,272 scoped cases. Forty Power cases use original powf instructions and constants: signed zero bases raised to 0.4 return 1 before last_edited_revision 1672 and 0 afterward. Another 256 mixed-type cases establish Number broadcasting into Colour/Float2/Float3/Float4, preserving operand order and caller inputs. Thirty-six unary and twelve ACos cases check selected rounding, clamping, NaN and unit-conversion behavior.

Remaining type/operator pairs, exceptional inputs, library error/scaling branches and game execution remain incomplete. No audited-byte credit added. Totals: 243 checked names; 1,686 mapped functions; 7,884 unmapped.
### Counter output and input-transition behavior

Named and typed Counter output/update helpers after matching original fields, native callers and the kind-specific runtime offset initializer. Independent reopening verifies both changes and unchanged original instructions/archives.

11,756 isolated native cases passed: 2,268 output cases, 1,296 inactive update cases with null previous state and 8,192 selected active input/reset cases. Output ratio and full threshold use unsigned values; update clamps use signed ordering. Selected sign-class transitions step the count, held classes do not retrigger, NaN inputs do not count, and reset rising edges clear current and wrap the reset byte.

The update harness supplies two offsets verified from original initializer writes; the initializer itself was not executed. The matching-previous caller path passes a Counter pointer through a shared-tail entry that bypasses nulling. Initial-state gating, mode/gate meanings and actual integration remain unresolved. Other active extremes and output property labels also remain incomplete. No game-runtime or audited-byte credit added. Totals: 245 checked names; 1,688 mapped functions; 7,882 unmapped.
### Selector output and input-transition behavior

Named and independently reopened Selector output/update helpers after matching original descriptor fields, the kind-specific offset initializer and dispatcher calls. The output reader returns zero for inactive ports, one for an active port without a matching passthrough input, or copies the first matching input Variant.

14,952 isolated native cases passed: 4,416 output, 5,120 inactive normalization, 24 inactive property-bag effects, 4,096 active wrapping and 1,296 direct-port cases. Selected sign-class input transitions wrap once by combined direction. In the tested four-port setup, the highest newly rising port wins; held inputs do not override. Inactive clearing preserves unrelated records and Variant tail bytes.

Synthetic Power metadata matches original initializer writes; the initializer was not executed. Concrete Game gate meanings, real-caller reachability, other exceptional/mixed inputs, active zero ports and malformed bags remain incomplete. No game-runtime or audited-byte credit added. Totals: 247 checked names; 1,690 mapped functions; 7,880 unmapped.
### Timer outputs and control-input modes

Named and independently reopened Timer output/update helpers, matching original time/state fields and mode enum descriptors. The output ratio is unclamped. CountDown done output requires zero current time and Active state; other modes compare current and target exactly.

18,286 scoped native cases passed: 9,720 output, 7,776 inactive update, 768 inactive property-bag and only 22 hand-picked active mode/boundary cases. Those active cases cover start/restart, speed signs, movement toward a position target, countdown, completion and reset at target 1. Original constants provide a step factor about 1/30 and crossing tolerance 0.005; selected SetSpeed cases can emit TimerDone before current reaches target. The large total does not represent exhaustive active-mode coverage.

Synthetic Power metadata matches the original initializer; the initializer was not executed. Other active values/targets, simultaneous conditions, Game gate meanings, input labels and real-caller reachability remain incomplete. No game-runtime or audited-byte credit added. Totals: 249 checked names; 1,692 mapped functions; 7,878 unmapped.
### Shared Thing update gate

Named and independently reopened PassesThingUpdateStateAndPowerGate. Complete native control flow and four call sites distinguish mode/session/index gating, optional bypass, Power lookup and stored object state. The bypass leaves Power and object checks in place. The stored state comes from an update-mode argument and game mode, separately from Power. Original field and enum labels remain unresolved.

4,862 scoped original-instruction hardware cases passed with synthetic metadata and selected flags, gates, offsets and Power values. This verifies selected predicate behavior, not running-game integration or full subsystem completion. Totals: 250 checked names; 1,693 mapped functions; 7,877 unmapped.
### Selected Thing runtime reset

Named and independently reopened ResetThingSelectedRuntimeState. The helper clears stored state bits18/19, then dispatches on Thing kind to reset selected fields. Selector ActivePort becomes255; Timer State becomes0 while CurrentTime remains unchanged. This is not a reset of every gadget setting or runtime value.

2,048 original-instruction hardware cases passed across every low-byte dispatch value, four flag patterns and two fill patterns. Every object byte and guard was compared. Synthetic padded objects include unregistered kinds; game reachability and complete caller behavior remain unverified. Totals: 251 checked names; 1,694 mapped functions; 7,876 unmapped.
### Reset, inactive update and output sequences

Composed original helpers on hardware: 480 Selector sequences and 720 Timer sequences passed full object/output byte and guard checks. Selector reset installs ActivePort255, then an inactive update normalizes it to0 for a positive port count, even with zero Power. Timer reset clears State while preserving CurrentTime and TimerDone storage. Modes0/1/2 can still report done after reset when current equals target; CountDown3 instead requires Active state. Selected inactive Timer clamps can also make done output true.

These are synthetic helper compositions with Game mode0, null previous state and null property bags. They do not establish real-game scheduling or complete gadget behavior. No verified-name or completion increment.
### Randomiser weighted port selection

Named and independently reopened ChooseRandomiserWeightedPort. Original fields bind NumPorts and WeightA through WeightJ to native reads. A zero eligible total returns sentinel10 without advancing the seed; otherwise a30-bit seed update chooses an eligible cumulative weight interval.

147,456 synthetic native cases passed for port counts2..10, four weight profiles, four seeds and all10-bit exclusion masks. Exact seed writes and object/guard bytes were checked. Original mode labels are NoRepeat, Shuffle and TrueRandom; the full mode-update behavior and real-game integration remain unresolved. No whole-gadget completion credit. Totals: 252 checked names; 1,695 mapped functions; 7,875 unmapped.
### Randomiser mode-update trace

12,960 controlled native updater cases compare NoRepeat, Shuffle, TrueRandom and a synthetic invalid mode, including initialization, trigger transitions, exact seed changes and16-bit counter boundaries. Shuffle advances a deterministic weighted ordering from ShuffleSeed. Initialization can run without a trigger, updates the thread seed again for ShuffleSeed and does not increment RandomIndex. An out-of-range Shuffle port may remain until the final clamp.

The updater, weighted picker and import thunk retain their original instructions. The operating-system TLS boundary is explicitly modeled to return worker seed index1; this is not execution of the PS4 OS implementation. Tests use synthetic non-null previous state. The matching-previous worker path passes the previous Randomiser through a shared-tail entry; initial-state gating and actual scheduling remain unresolved. No names or completion metrics added.
### Randomiser trigger-edge updater name

Applied and independently reopened UpdateRandomiserFromTriggerEdges with working Game, previous Randomiser, current Randomiser and object-index arguments. Original fields, mode labels, complete native control flow and12,960 controlled native cases support the descriptive role. Initialization can run without a trigger; initialized zero-to-nonzero input advances selection and16-bit RandomIndex.

The synthetic TLS boundary and non-null previous-state fixture remain explicit limitations. The matching-previous worker path passes the previous Randomiser through a shared-tail entry; initial-state gating and actual game scheduling remain unresolved. Neither this name nor the tests establish whole-gadget completion. Totals: 253 checked names; 1,696 mapped functions; 7,874 unmapped.
### Randomiser output routing

Applied and independently reopened ReadRandomiserOutputVariant. Sentinel10 silences every output. A selected output forwards the first matching common input at property122 as37 bytes, preserving the last3 output bytes; without that input it returns Signal1. Unselected outputs return Signal0.

30,720 scoped original-instruction cases check low-byte property aliases, selected/sentinel ports, six well-formed bags, two tags and two port counts. Synthetic invalid configurations do not prove UI validity or real-game scheduling. No whole-gadget completion credit. Totals: 254 checked names; 1,697 mapped functions; 7,873 unmapped.
### Randomiser reset and initialization sequences

576 controlled compositions of original reset, update, picker and output helpers passed full byte/guard checks. Reset installs ActivePort255 and clears stored state bits18/19. With those bits cleared, valid Game gates alone do not allow initialization. After the fixture restores bit18, initialization selects a weighted port independently of a trigger and leaves RandomIndex unchanged. All-zero weights produce sentinel10 and silence all ten tested outputs.

The full worker was not executed: its bit18 restoration is modeled explicitly. TLS index1 and non-null previous state are also synthetic boundaries. These sequences do not establish actual game scheduling. Wider incoming-edge inspection confirms the matching-previous worker path bypasses the nulling instruction; initial-state gating remains unresolved. No naming or completion increment.
### Remapper unsmoothed curve paths

Repaired the working evaluator signature from native register/stack evidence: two40-byte Variants pass by value. Independent reopening confirms the saved types and unchanged original instructions/archives, without naming credit. Original fields and enum labels identify range configuration, smoothing, edge modes and curve choices.

840 finite Number/Signal cases verify seven unsmoothed curves, three range configurations and bypass within1e-6; unused output bytes, inputs and guards are checked exactly. Sixteen separate bypass cases show selected quiet/signaling NaNs become positive zero, while infinities and subnormals preserve their bits. The fixture executes the original libc NaN predicate rather than a substitute normal-value filter.

Smoothing, edge-state behavior, vector/player components and real-game integration remain unverified. No new checked-name or completion credit.
### Remapper edge state and smoothing

46,080 controlled native cases check all256 prior scalar state-flag bytes across six edge modes, five finite inputs, three prior outputs and Number/Signal tags. Pulse modes emit their selected edge and clear the latch in these unsmoothed cases. ToggleOnEnter/Leave invert the latch on their selected threshold entry. ToggleOnBoth instead sets it at an upper entry and clears it at a lower entry. Upper state bits are preserved.

576 separate native smoothing cases use the original libc exp2f body and indexed table/constants. Selected rise/fall coefficients follow1-exp2(-6*(1/30)/smoothTime), alongside a separate linear increment. Results match the float32 model within1e-6; other bytes and guards are exact. The external exp2f error helper is deliberately unmapped and selected exponents avoid that path.

These cover ordered0..1 ranges and selected scalar inputs. Reversed thresholds, vector/player lanes, combined edge-plus-smoothing behavior and game scheduling remain unverified. No naming or completion increment.
### Remapper evaluator name

Applied and independently reopened EvaluateRemapperSignal, with four register arguments and two40-byte Variants passed by value. Original fields and enums identify range mapping, curves, edge state, smoothing, presets and component bypass. The descriptive role is supported by native control-flow review and47,512 scoped cases across separately tested paths.

This is not a full Remapper completion claim. Combined edge/smoothing, vector/player lanes, reversed thresholds, other presets and running-game integration remain unresolved. Original instructions and archives remain unchanged. Totals: 255 checked names; 1,698 mapped functions; 7,872 unmapped.
### Remapper components and player edge history

10,240 original-instruction cases verify independent bypass bits and selected affine range mapping for Float2/3/4/8 and PlayerValue. They preserve untouched payload, alpha, type, tail, configuration and input bytes. Scope: Custom preset, curveOff, no smoothing or edges, matching prior type/shape and selected finite values.

1,800 separate PlayerValue edge/smoothing cases use differing previous lane values. All1,800 distinguish a shared scalar reduction of previous PlayerValue from lane-local history. Current lanes and their state flags remain separate, while smoothing uses that shared previous scalar. The selected nonnegative profiles reduce to their common maximum. Original evaluator, reducer, math bodies and tables execute without substitutes.

These are synthetic helper findings, not a gameplay bug or impact claim. Other prior-value classes, presets, longer sequences and real-game scheduling remain unverified. No naming or completion increment.
### Remapper runtime wrapper

Applied and independently reopened UpdateRemapperOutputFromInput with four native working arguments.972 controlled wrapper cases verify freeze transitions and write boundaries: both prior and current FreezeOutput must be nonzero to reuse stored prior output. Current-only freeze and leaving freeze still evaluate input in the tested configurations. The stored-output route copies37 bytes and preserves the final3 output bytes.

Original initializer writes verify Power and OutputA offsets supplied to the fixture. These tests cover inactive Game mode0, selected Number/Signal values, Custom preset, no smoothing/edges and well-formed/null input bags. Active/network behavior and real-game scheduling remain unresolved. Totals: 256 checked names; 1,699 mapped functions; 7,871 unmapped.
### Local Remapper signal history

Applied and independently reopened AppendRemapperSignalHistory with history/input/output pointers. The helper records paired input/output samples in a256-slot ring and maintains input extrema.7,680 scoped Timestamp native cases verify wrap, count cap256, signed extrema and equal-value retention. Copies update37 bytes of each40-byte Variant slot, preserving padding3.

Original Game initialization corroborates two local history records and head255/count0.48 native initializer cases verify37-byte logical clears per slot. This follows the Remapper wrapper locally; it is not evidence of network transmission. Other type/component extrema, cache expiry/locking, consumers and actual game scheduling remain unresolved. Totals: 257 checked names; 1,700 mapped functions; 7,870 unmapped.
### Remapper signal-history cache

Applied and independently reopened FindOrInitializeRemapperSignalHistory with Game/key arguments and pointer return.784 controlled cases verify key hits, expiry boundaries including unordered ages, replacement and timestamp refresh. Matching unflagged keys bypass expiry; on a miss, a second eligible record overrides first. The original threshold is0.06666667014360428; its clock unit is not independently established.

Original cache and initializer instructions, constant and import thunks execute with explicit modeled mutex, thread-id, copy and fill contracts. Actual PS4 synchronization/memory implementations and concurrency are not validated. Consumers and game scheduling remain unresolved. Totals: 258 checked names; 1,701 mapped functions; 7,869 unmapped.
### Signal-history typed extrema

420 finite component cases and72 selected special-value pairs extend history validation beyond Timestamp. Sampled scalar/vector extrema are component-wise, retain current input metadata/unused payload, and preserve slot padding. Native min/max select stored operand bits on equal or unordered comparisons in these tests, including signed-zero and NaN patterns; no NaN cleanup occurs here.

220 mixed Timestamp cases show type priority: incoming Timestamp replaces sampled non-Timestamp extrema, while existing Timestamp extrema survive non-Timestamp inputs. Both Timestamp values use signed64 comparisons. Ring sampling still records incoming input/output values.

Non-Timestamp payloads in mixed-tag cases are synthetic opaque patterns, not assumed valid numeric values. Broader mixed-type/shape behavior, consumers and game scheduling remain unverified. No names or completion metrics added.
### Inverter and XOR output helpers

Applied and independently reopened ReadInverterOutputVariant and ReadXorOutputVariant. Original kind-table entries and property branches bind both helpers to their gadgets. Inverter passed44 selected numeric and identifier cases. Its numeric path clamps to[-1,1] then subtracts from a sign-selected endpoint; zero maps to1 and both endpoints to0.

XOR passed130,520 uniform and mixed selected-input cases. Exactly one active input forwards its original value; a second active input writes zero and stops. No active input leaves the caller-provided output untouched. This is exactly-one behavior, not parity XOR. Identifier-like tags use raw nonzero64-bit payloads, including all-ones; Number/Signal inputs use ordered scalar>0. Full output bytes, padding, input objects and guards were compared.

These tests execute original instructions in controlled local fixtures. Other variant reductions and running-game behavior remain unverified. Totals:260 checked names;1,703 mapped functions;7,867 unmapped. This adds no whole-game completion or audited-byte credit.
### AND and OR typed output helpers

Applied and independently reopened ReadAndOutputVariant, ReadOrOutputVariant and MergeTypedSignalsByMinimumMagnitude. Original kind-table entries and output-property branches bind the wrappers. AND picks the smaller-magnitude signed component; OR picks the larger. Equal or unordered component comparisons select the second input bits. Numeric weights use SSE minimum/maximum, also taking the second operand on equal or unordered comparisons.

21,168 original-instruction numeric pair checks,5,292 identifier/Timestamp pair checks,4,704 mixed Number/Signal pair checks and12,152 multi-port wrapper checks passed. Identifier-like values combine raw-nonzero truth into Bool with zero alpha. Timestamp branches compare signed64 magnitudes, clamp a selected negative timestamp to zero, and use absolute min/max alpha. The wrappers always combine two embedded inputs, then fold extra sparse properties in port order. Missing extra inputs become NONE/zero. Tests compare exact input/output/guard bytes, including NaN payloads, signed zero and padding.

Broader mixed-type promotion and actual running-game behavior remain unverified. Totals:263 checked names;1,706 mapped functions;7,864 unmapped. No whole-subsystem completion or audited-byte credit is added.
### Mixed scalar, vector and PlayerValue promotion

19,404 additional original-instruction checks cover AND/OR mixed-type combination:14,112 scalar/vector cases and5,292 PlayerValue/vector cases, with both input orders and exact byte/guard comparisons. Number and Signal broadcast across Float2, Float3, Float4, or five-lane PlayerValue before component comparison. PlayerValue uses a separate promotion table; when paired with Float2/3/4, selected nonnegative five-lane profiles reduce to their maximum then broadcast to the vector.

The ordinary promotion rule chooses higher rank, breaking equal ranks by higher tag. PlayerValue overrides that rule through its special map. This explains why mixed inputs can change both output type and component meaning. Signed or exceptional PlayerValue reductions and broader conversions remain unresolved; context-dependent, quaternion and default-fill paths are outside this checkpoint. No new names or whole-game progress credit are added.
### Signal Generator random ranges and inactive output

Applied and independently reopened UpdateSignalGeneratorOutputAndRandomRanges after inspecting its complete132-instruction body,130-instruction evaluator, registered fields and worker call. The wrapper refreshes out-of-range RandomTime and two RandomMag endpoints using a worker-local30-bit LCG before checking Power. Signed-zero Power leaves phase/output untouched. Nonzero Power enters an evaluator whose phase encodes rise, high hold, fall and low hold, using Game-gated step and magnitude values passed in floating-point registers.

864 original-instruction cases compare the whole gadget object and worker seed across selected ranges, cache values, seeds, zero/nonzero/NaN Power and sweep values. These use inactive Game state, phase1.25 high hold and explicit modeled TLS worker index1; original OS TLS is not executed. Active transitions, cosine path, invalid ranges and running-game behavior remain unverified. The evaluator pseudocode has unresolved floating-register arguments; it is not renamed or treated as a reliable working signature yet.

Totals:264 checked names;1,707 mapped functions;7,863 unmapped. No whole-subsystem completion or audited-byte credit is added.
### Signal Generator active phase evaluation

576 additional original-instruction checks validate selected no-boundary active and inactive phases. Exact loader binding identifies the cosine import as cosf; tests execute the original local libc implementation and constants. Stage0 rises with cosine easing, stage1 holds high, stage2 falls with cosine easing, and stage3 holds low. The captured timestep is1/30 only when Game mode3, either activity flag set, and pause flag zero; otherwise it is zero. Phase fraction advances by timestep divided by sweep or cached pause duration.

Whole gadget bytes and worker seed are checked, with output compared to an independent cosine model at tolerance2e-7; these selected cases had zero observed output error. TLS worker index and guard pointers are explicit fixtures. Stage crossings, their random draws, malformed durations, exceptional/large cosine inputs and actual game scheduling remain unverified. The evaluator receives timestep in XMM0, magnitude limits in XMM1 and five GP pointer arguments; its saved working signature still needs repair. No new names or whole-game completion credit are added.
### Signal Generator stage crossings and random draws

432 original-instruction cases validate selected positive-duration boundary crossings, including steps that cross more than one boundary. Leaving rise or fall draws a new pause. Entering fall draws the low magnitude endpoint; entering rise draws the high endpoint. The unused portion of the timestep continues into subsequent stages. Exact final phase, random cache, worker seed and all other gadget bytes match an independent stage/LCG model; selected output values match with zero observed error.

Assembly and execution establish an additional pause bound:when sweep duration is at most the captured1/30 constant, the new pause lower bound is max(configured low,1/30); otherwise it is max(configured low,0). The first model assumed only the configured bound and failed; correcting it from the original comparison makes all selected cases pass. This was a model correction, not a change to game instructions.

Tests retain original evaluator and local libc cosine code with explicit modeled TLS index and guard pointers. Selected finite ranges, three positive sweep/pause durations and four seeds are covered. Zero, negative or NaN durations, larger timesteps, evaluator signature repair and real-game validation remain unresolved. No new function names or whole-game completion credit are added.
### Signal Generator evaluator signature

Applied and independently reopened EvaluateSignalGeneratorPhase with an explicit register signature: timestep in XMM0, four-float magnitude bounds in XMM1, five pointer arguments in RDI/RSI/RDX/RCX/R8, and float return in XMM0. A small analyst-defined register container preserves all four magnitude limits. Original caller assembly proves the assignments; reopened evaluator pseudocode now exposes the named timestep and magnitude inputs instead of undefined incoming ZMM values. The connected wrapper also decompiles successfully. Opaque upper SIMD-register bytes still appear in decompiler temporaries; this repair identifies the scalar lane actually used and the16-byte magnitude argument.

The evaluator name is supported by the complete body,576 selected no-boundary cases and432 selected crossing cases using original libc cosf. Original instructions and input archives remain unchanged after backed-up trial, promotion and independent reopening. Invalid durations, broader edge cases and actual running-game integration remain unresolved. This working ABI does not claim the original C++ declaration. Totals:265 checked names;1,708 mapped functions;7,862 unmapped.
### Signal Generator output into the signal path

The original startup writer maps SignalGenerator property0x11d to OutputNormalised. The wire consumer first tries the generic property reader, then calls special gadget dispatch only if that read fails. Original type/property jump tables lead the generic reader to a Signal-producing scalar branch.84 original-instruction cases verify success return, exact float payload bits, Signal type and weight1, while preserving other output bytes. Default reads use the embedded field. Forced sparse reads prefer a matching override and otherwise fall back to the embedded field. Signed zero, subnormals, infinities and selected NaN payloads are retained as bits.

The saved offset table is initially zero, so the fixture reconstructs this one entry from its original startup store; full startup is not executed. Ghidra has not defined the selected indirect-jump blocks as part of the reader body. Their raw original bytes were independently captured, inspected and executed without changing project code or claiming the whole generic reader is understood. Full wire scheduling and other properties/types remain unverified. No function-name or whole-game completion credit is added.
### Signal Inspector change counters

Applied and independently reopened UpdateSignalInspectorChangeCounters after inspecting its complete40-instruction body, registered fields and native worker call. Ordered positive Power enables comparison of reduced previous/current InputA scalars. A changed or unordered scalar resets TimeSinceChange and subtracts8 from BrightnessOnChange with floor0. Equal scalars increment both byte counters with saturation255. Changes to unused Number/Signal payload or alpha do not count as scalar changes in the selected cases.

34,800 original-instruction checks compare complete previous/current object bytes across selected Number/Signal values, Power bits and counter states. Signed-zero/negative/selected NaN Power leaves counters untouched; selected NaN input scalars count as changed. Incoming edges show that a matching previous Inspector pointer is passed; absent or mismatched previous objects select null. The helper tests use synthetic objects, so initial-state gating, actual scheduling and display interpretation remain unverified. No whole-Inspector completion or audited-byte credit is added. Totals:266 checked names;1,709 mapped functions;7,861 unmapped.
### Signal Inspector caller correction

A wider control-flow trace corrects the earlier unconditional-null description. The absent-previous path clears the pointer, while the matching-Inspector path selects the previous object and enters the shared call tail after that clearing instruction.32 incoming-edge instruction spans match the original unencrypted PS4 executable exactly; the40-instruction helper and selected call tail also match. The nulling instruction is real, but is bypassed on the matching path.

The Ghidra annotation was corrected in a backed-up trial, promoted and independently reopened. Function names, signatures, native instructions and archives are unchanged. Earlier bounded-window evidence omitted this incoming edge. Initial/mismatched-object Power gating and actual in-game scheduling remain unverified. Name totals remain266.
### Stateful gadget caller audit correction

Counter, Selector, Timer and Randomiser use the same shared-tail pattern found in Signal Inspector. Each matching-previous path selects a correctly typed previous pointer in RSI, then enters the call tail after its nulling instruction. Only absent/mismatched paths select null.204 instruction spans across these incoming edges and call tails match the original unencrypted PS4 executable. Earlier unconditional-null caveats based on short tail windows were incomplete and are corrected here and in current function reviews.

All four saved Ghidra annotations were corrected through a cold backup, isolated trial, promotion and independent reopen. Names, signatures, instructions and archives remain unchanged. Existing synthetic helper tests still do not establish actual scheduling, initial-state gating or full gadget integration. No name or completion increment;266 functions remain checked.
### Gate activation requests

Applied and independently reopened UpdateGateActivationRequests after inspecting its complete91-instruction body, original Gate descriptor, field registration and worker call. It always clears want_to_activate. Nonzero Power enables typed input truth and previous-state comparisons, reset waiting and synchronization. Automatic reset mode with false input, or a rising Reset, sets reset waiting. Waiting plus GateSync clears active state and updates forget_queue. An inactive gate combines input requests with a nonzero QueueFrame and marks a Game flag when work is requested. This helper requests activation; it does not choose a winning gate.

50,176 original-instruction cases compare complete previous/current objects and a33-byte Game flag window. Selected Number/Signal and identifier-like values, Power bits, ResetMode0/1, queue markers and boolean flags are covered. Request1 versus3 distinguishes powered prior truth; identifiers use raw nonzero64 payloads while other selected inputs use scalar>0. Negative and selected NaN Power enter the nonzero path. Queue arbitration, Queue reset mode2, null previous/reset edges and actual game runtime remain unresolved.

Names, saved signature and native bytes were independently reopened after backed-up trial/promotion; archives are unchanged. No whole-gadget completion or audited-byte credit added. Totals:267 checked names;1,710 mapped functions;7,860 unmapped.
### Inline Gate arbitration and output path

A bounded assembly trace locates Gate processing inside the main update routine. A256-byte claimed-group scratch array is zeroed, and gates use group indices from a parallel array. An already-claimed group clears a later gate's active state. On a requested input, GateSync with an unclaimed group can set the gate active. Active gates copy37 bytes of InputA to OutputA, clear QueueFrame/QueueLevel and mark the group claimed. Inactive outputs become NONE with weight1; the branch retains their old payload bytes.

Queue initialization stores the Game counter plus1 and the reduced input level; an existing queue level uses MAXSS with current input. forget_queue clears the queue fields and itself.524 instruction spans in the captured window match the original unencrypted PS4 executable. These findings come from static native/data-flow inspection, not execution of the inline loop.

The surrounding priority/order rules, group construction and request-flag-to-loop scheduling remain unresolved. Nearby-storage and raw-byte cluster searches were treated only as leads; unrelated candidates were rejected. No new name, mapping or whole-game completion credit is added.
### Gate activation ordering comparator

Applied and independently reopened GatePrecedesInActivationOrder with two pointer arguments and boolean AL return. The main update calls the Gate pointer sorter before inline group arbitration. The comparator first uses unsigned raw64 Name key ascending and signed Priority descending. It then compares interrupt-related level, activation score, input scalar, reset-mode byte and queue level descending; queue-frame key and final signed integer tie-breaker ascend. The raw Name key is not claimed to be display-string lexical order, and the final integer field remains unnamed.

12,000 original-instruction checks cover all nine decision levels and compare full input bytes. Interrupt level is zero without GateInterrupt; otherwise it is queued level when QueueFrame is nonzero, or current input scalar. Inactive interruptible gates can use request bit2 as activation score. Native SETA implements ordered float greater-than; selected NaNs return false at the reached float comparison. Full-sort behavior with NaNs is not validated.

The83-instruction comparator and its scalar reducer are tested; the1,500-instruction sorting helper and surrounding group construction are not execution-validated. Names/signature, instruction bytes and archives were independently reopened after backed-up trial/promotion. Totals:268 checked names;1,711 mapped functions;7,859 unmapped. No whole-subsystem completion or audited-byte credit added.
### Gate pointer-range sorting

Applied and independently reopened SortGatePointersByActivationOrder with begin/end pointer range and signed64 depth budget.180 original-instruction cases validate sizes0 through256, including32/33 boundaries and depth budgets0/1/16, across random, sorted, reversed, equal-key and duplicate-pointer inputs. Tests check sorted key sequences, exact pointer multiplicity, buffer guards and unchanged Gate objects. Both small-range and larger/fallback paths are exercised.

The original1,500-instruction sort,83-instruction comparator and scalar reducer execute locally. The remaining import resolves exactly to memmove; its original thunk targets an explicit modeled overlap-safe copy fixture, separately checked in96 overlap/zero-length cases. The PS4 library copy implementation is not validated by these tests.1,583 sort/comparator instruction spans match the original unencrypted executable.

Selected finite Number keys are covered. NaNs, other reductions, group construction, inline arbitration composition and actual game scheduling remain unverified. This deepens the sort contract without claiming whole-Gate completion. Names/signatures and archives were independently reopened after backed-up trial/promotion. Totals:269 checked names;1,712 mapped functions;7,858 unmapped. No audited-byte credit added.
### Parent scope reference resolution

Applied and independently reopened ResolveParentScopeReference with Game/encoded-reference arguments and a32-bit reference return. Gate grouping calls this shared helper; it also has callers outside the Gate path. Cache-count match traverses a ushort parent map while skipping cached codes13..15. A count mismatch follows object parent pointers while the current object mode byte is nonzero. After traversal, a glued object can skip one additional parent. A root/no-parent can return the current reference. Raw codes and mode bytes are not assigned unsupported semantic names.

24,576 original-instruction cases validate both modes separately on valid eight-object acyclic chains, with selected cache/mode patterns, glued flags and encoded high bits. Return values, complete objects and selected Game lookup ranges are checked. The glued offset fixture is reconstructed from an original startup store; startup and cache construction are not executed, and mode equivalence is not established. Invalid references, cycles, absent objects, other object kinds, complete Gate grouping and actual scheduling remain unverified.

Backed-up trial, promotion and independent reopening confirm the name/signature and unchanged instructions/archives. Totals:270 checked names;1,713 mapped functions;7,857 unmapped. No whole-subsystem completion or audited-byte credit added.
### Parent cache writer and container types

Fresh native inspection of a runtime object-registration path shows the parent cache receiving the object parent's low16 bits and the type cache receiving Thing kind low7 bits. Object count and cache count are both set to the inserted index plus1. The original Thing enum registers13 as Microchip,14 as Timeline and15 as Sound. This establishes the previously unnamed cached types skipped by ResolveParentScopeReference as those three containers.

219 writer/enum instruction spans and the enum string bytes match the original unencrypted PS4 executable. This is static data-flow evidence; object registration and full cache rebuild were not execution-tested. The fallback object-mode byte, cache invalidation, complete grouping and actual game scheduling remain unresolved. No function-name or completion increment;270 functions remain checked.

### Gate scope grouping

The original grouping loop partitions sorted Gates by their raw Name identity. Matching nonzero scope references share a group index. Gates whose initial scope key is zero walk their resolved parent and cached ancestors to find a matching scope within that same-name group. That ancestor search includes later entries as well as earlier ones; a first interpretation restricted it to earlier entries and failed an exact group-index check, so it was corrected from the native branches before publication.

432 original-instruction cases pass across sizes1 through256, equal/distinct/mixed names and nested parent trees. Exact scope keys, group indices, scratch-array guards and unused tails, plus complete Gate and parent-object bytes, are checked. All552 captured instruction spans match the original PS4 executable. The fixture explicitly supplies the stack/register boundary and cached acyclic parent trees; allocation, sorting and arbitration are not composed here. Glued/container combinations, fallback traversal in this loop and running-game behavior remain unverified. No new name or completion credit;270 names remain checked.

### Gate activation arbitration

1,344 original-instruction cases pass for the inline arbitration loop, with groups of1 to256 Gates and finite Number inputs. An active Gate claims its group; later Gates in that group lose GateActive. A synchronized request activates only when unclaimed. Blocked synchronized Gates retain a waiting request only in Queue reset mode; unsynchronized requests can also queue. Active output copies37 Variant bytes and clears queue state. Inactive output receives NONE and alpha1 without payload clearing.

Queue initialization stores the current frame counter plus1 with uint32 wrap and the input level. Existing queues retain the maximum level. Initializing a queue clears the forget flag before final forget processing. Tests check complete Gate objects, the complete Game fixture, unchanged pointer/group arrays, claimed-group bytes and scratch guards. Every modeled branch family was exercised. Original reducer/constants run, while allocation and stack setup are explicit boundary fixtures. Other Variant inputs, NaN queue levels, sorting/grouping/update composition and actual game scheduling remain unverified.270 names remain checked; no subsystem completion credit.

### Gate grouping and arbitration composition

288 cases execute the original grouping and arbitration loops continuously, with an explicit adapter supplying the scratch allocation between them. Same-name, distinct-name, mixed-name and nested-parent fixtures cover1 to256 Gates. Original parent resolution and scalar reduction run. Exact scope/group/claimed arrays, guards and unused tails, complete Gate and parent objects, unchanged pointer arrays and the full Game allocation match the independent composition model.

This closes the previously separate grouping-to-arbitration check for the selected fixtures. Sorting and initial request generation are still outside this composition; parents are valid cached acyclic trees with no glued/container combinations and inputs are finite Numbers. Allocation/free and game scheduling are not executed. No additional name, whole-subsystem completion or running-game validation is claimed;270 names remain checked.

### Gate request-to-output pipeline

The original request updater, priority sorter/comparator, parent-scope grouping and activation/output arbitration now execute in sequence on the same Gate objects.288 cases pass across1 to256 Gates, shuffled pointer inputs, same/distinct/mixed names, nested cached parent trees and sorter depth budgets0,1,16. A separate288-case sorting/grouping/arbitration composition also passes. The tests compare independently modeled ordering, exact group/claim arrays and their guards/tails, complete previous/current Gate and parent objects, and the full Game allocation including the expected request-dirty flag.

This validates the connected sequence for selected finite Number inputs and nonnull snapshots, beyond the previous individual helpers. The library memmove import uses an explicit overlap-safe model with96 boundary checks; allocator/free calls use boundary adapters. Glued/container parent combinations, fallback traversal in the connected sequence, other Variant inputs, NaN keys, cross-frame scheduling and actual game execution remain unresolved. This is bounded native pipeline evidence, not whole-Gate or whole-game completion;270 function names remain checked.

### Gate reflection registration names

Applied InitializeGateTypeDescriptor and RegisterGateProperties. The initializer binds the original Gate label, base properties, descriptor callbacks and property registrar. The registrar defines the reflected input/output, priority, queue, reset and scope fields and their enum metadata.374 native instruction spans match the original PS4 executable; runtime traces corroborate selected offsets.

Cold backup, isolated trial, promotion and independent reopening verify both names and void/no-argument signatures with unchanged instructions and original archives. Registration allocation/static guards and callbacks remain unexecuted. Totals:272 checked names;1,714 mapped functions;7,856 unmapped. No whole-subsystem completion credit.

### Gate creation and cleanup callback boundaries

The Gate descriptor points to two callbacks that are not yet defined as functions in the saved project. Complete bounded decoding identifies a50-instruction creation path and a4-instruction cleanup path; all callback bytes match the original PS4 executable. Creation requests352 bytes and sets Power1, Priority10, no active/queued request, empty input/output Variants, GateSync1 and ScopeType1. Cleanup returns for null and otherwise tail-jumps to a deallocation import.

Creation also reads a runtime colour global. A native initialization window loads original file-backed colour components and stores them to that global; this trace avoids assuming uninitialized memory is its runtime value. Initializer execution, later indirect writers, exact allocation/deallocation import symbols, allocation failure and actual lifecycle execution remain unverified. No functions were created or named in this checkpoint;272 checked names remain.

### Gate callback initialization execution

Original creation instructions pass256 cases, one for every initial fill byte. All352 object bytes, surrounding guards, requested allocation size and returned pointer match the independent initialization model. The original cleanup callback passes256 null cases without calling deallocation and256 nonnull cases forwarding the exact pointer once. Complete object bytes remain unchanged during cleanup.

Original import thunks run against explicit heap-boundary substitutes; these tests do not execute the actual allocator or deallocator. The colour value is supplied from the original static initialization writer and file-backed constant; that startup writer is not executed. Allocation failure, runtime descriptor dispatch and in-game lifecycle remain unverified. No function definitions or names were added in this checkpoint;272 checked names remain.

### Saved Gate lifecycle callback definitions

Defined AllocateDefaultGate and FreeGateStorage at the original descriptor callback targets, with pointer return/no arguments and void/pointer argument respectively. The full nonoverlapping50- and4-instruction bodies retain original bytes. Existing functions are unchanged. Cold backup, isolated trial, promotion and independent reopening confirm the definitions, ABI storage and saved decompilation. Original archives remain unchanged.

The definitions are supported by256 full-object initialization cases and512 cleanup cases using explicit heap-boundary models. Actual heap implementation, allocation failure, startup execution and in-game lifecycle remain unverified. Totals:274 checked names among9,572 discovered functions;1,716 mapped and7,856 unmapped. This adds two previously undefined functions, not extraction or whole-subsystem completion credit.

### Gate pipeline with glued and fallback parents

The connected original request/sort/group/arbitration sequence passes another288 cases with valid acyclic Gate-kind parent trees:144 cached traversal and144 fallback traversal cases, with parent-mode and glued flags varied. Cached type entries match the parent objects' Gate kind. Original parent resolution runs in the connected sequence. Exact scope/group/claim arrays, full Gate and parent objects and the full Game allocation are checked alongside sorting and output/queue behavior.

The independent model initially represented a no-parent reference as signed-1 in an unsigned output array; that fixture encoding was corrected before the successful run. The fallback mode byte remains semantically unnamed. Container-kind combinations, invalid/cyclic references, other Variant inputs and real game scheduling remain unverified. Heap/copy boundaries remain explicit models. No names or completion credit are added;274 names remain checked.

### Unsigned32 field registration

Applied RegisterUnsigned32FieldOffset with descriptor/name/32-bit byte-offset inputs and an opaque property-record pointer return. The original u32 label binds the field type; numeric metadata4 is not established as a byte width. The complete139-instruction body appends a144-byte property record, stores the name/hash/offset and attaches type/default metadata. Gate QueueFrame uses this shared helper.

Original bytes match the PS4 executable. Backed-up trial, promotion and independent reopening verify the saved name/signature and unchanged archives. Reflection allocation/static guards and serialization remain unexecuted. Totals:275 checked names among9,572 functions;1,717 mapped and7,855 unmapped. No whole-subsystem completion credit.

### Gate property visitor

Applied VisitGateProperties with opaque visitor and Gate pointer inputs. Original kind84 dispatch, reflected fields and complete763-instruction body bind the role. Native branches filter property paths and format versions: ParentFromModel from729, QueueFrame replacing legacy Queuing from1049, QueueLevel from1085, forget/reset-waiting/sync fields from1131, IsGluedGadget from1139, and ScopeType from1673. A separate scope compatibility branch covers1673 through1850 inclusive. These are numeric format thresholds, not dates.

Backed-up trial, promotion and independent reopening verify the name/signature and unchanged original instructions/archives. Virtual callbacks and full serialization direction remain unexecuted. Totals:276 checked names among9,572 functions;1,717 mapped and7,855 unmapped. No whole-subsystem completion credit.

### Filtered property visitor entry

Applied BeginFilteredPropertyVisit. It rejects suppressed visits and explicit names beginning#, generates signed decimal names for unnamed fields only in mode1, and accepts filters matching the complete name or a slash-delimited descendant. Accepted mode0 calls the first virtual callback with the name; mode1 calls the second only when a prior field was visited. Success sets the prior-field flag and returns1. Modes remain numeric contracts without inferred read/write direction.

2112 original-instruction cases compare return, callback sequence and every visitor-context byte using explicit string/format and virtual callback models.73 instruction spans and the original format literal match the PS4 executable. Backed-up trial, promotion and independent reopening verify the saved name/signature and unchanged archives. Real serialization recursion remains unverified. Totals:277 checked names among9,572 functions;1,718 mapped and7,854 unmapped.

### Signed field registrar ABI and metadata correction

Corrected RegisterSigned32FieldOffset to descriptor/name/32-bit offset inputs and an opaque property-record pointer return.139 original instructions and the s32 type literal support the role and ABI. Backed-up trial, promotion and independent reopening verify the saved signature; names and original bytes/archives are unchanged.

Corrected an unsupported earlier interpretation of unsigned metadata4 as a byte width, including the saved Ghidra comment and current public evidence. Signed registration has metadata8; the meaning of these numeric values remains unresolved. Original u32/s32 labels establish the field types. No new checked-name or completion credit;277 names remain checked.

### Developer rendering material comparison

Reviewed Alex Evans’ [SIGGRAPH2015 slides](https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf), including the specific Hilbert-order/point-cluster description on page112. The talk covers historical rendering experiments; it does not establish this executable’s implementation.

Fresh inspection of a local candidate instead finds Morton/Leaves/Links/Bounds job labels,2n-1 records and a64-bit sorter.583 captured instruction spans match the original executable. A256-element job batch is insufficient evidence of the slides’ point-cluster storage. Four worker callbacks are identified for further tracing; their ownership and data layout remain unresolved. No source/binary function match, new name or completion credit is claimed.277 names remain checked.

### Morton binary bounding-volume tree workers

The four native workers generate Morton keys, initialize leaves, link a binary tree and propagate bounds/flags.36 connected array cases pass across sizes1 through513, including duplicate and reversed centres and256-item job boundaries. Independent bit interleaving checks the keys; recursive invariants verify every node is reached exactly once, parent/child consistency, complete bound unions and flag propagation. Input/context bytes and scratch guards remain unchanged.

The tested layout has2n-1 nodes of32 bytes and16-bit indices, with root2n-2. Keys combine16 coordinate bits per axis with a16-bit original index.256 is the job batch size; this does not establish the earlier talk’s point-cluster implementation. Original sorter/workers run with an explicit overlap-safe copy model and origin0/scale1 finite integer fixtures. Native normalization, degenerate/NaN bounds, concurrent scheduling and scene/render/physics ownership remain unverified. No new definitions, names or completion credit;277 names remain checked.

### Saved Morton tree worker definitions

Defined GenerateMortonBvhKeysJob, InitializeMortonBvhLeavesJob, LinkMortonBvhNodesJob and PropagateMortonBvhBoundsJob with opaque context and32-bit batch-index inputs. Backed-up trial, promotion and independent reopening confirm nonoverlapping bodies, unchanged instructions/existing functions and original archive hashes.

Both tree-builder calls come from a routine scheduling the original CalculateSculptBoundsAndWakeUpBodies job and collecting transformed object bounds. This connects the work to sculpt/physics processing without establishing every consumer. The worker definitions are recorded under shared spatial helpers.36 connected tree cases support their roles; normalization, concurrency and complete consumers remain unresolved. Totals:281 checked names among9,576 discovered functions;1,722 mapped and7,854 unmapped. No whole-subsystem completion claim.

### Morton tree normalization and scheduling wrapper

30 connected cases now execute the original normalization/scheduling wrapper together with the four workers and sorter. Sizes0 through513 include flat axes and identical centres. Independent float32 calculations match normalized keys; tests also verify job labels/counts, complete tree invariants, forward/inverse identifier permutations, unchanged input records and scratch guards. Empty input returns0 without jobs. Nonempty input returns2n-1.

A failed first model assumed flat-axis conversion contributed zero; original instruction execution instead produces the equivalent of coordinate32768 in the interleaved key. The model was corrected before publication. Sequential scheduler/fence substitutes and an overlap-safe copy model are explicit boundaries; concurrency, explicit nonfinite input bounds, index overflow and real consumers remain unverified. No new names or completion credit;281 names remain checked.

### Saved Morton tree wrapper name

Applied BuildMortonBvhForBounds with five opaque pointer inputs and a32-bit node-count return. Original157-instruction wrapper, four job targets and30 connected cases support its role. Empty input returns0; nonempty input produces2n-1 nodes and forward/inverse identifier permutations. The first caller-supplied context pointer remains opaque; actual jobs use a global scheduler.

Cold backup, isolated ABI trial, promotion and independent reopening verify the saved name/signature and unchanged original bytes/archives. Sequential scheduler/fence and copy models remain explicit limits; concurrency and complete real-game consumers are unresolved. Totals:282 checked names among9,576 functions;1,723 mapped and7,853 unmapped. No whole-subsystem completion credit.

### Unsigned64 range sorter

Applied SortUnsigned64Values with unsigned64 begin/end pointers and a64-bit partition budget. The complete426-instruction routine sorts ascending with unsigned comparisons, partition/insertion paths and a larger-range heap fallback.375 native array cases across sizes0..1024, high-bit/extreme/duplicate/random/reverse data and budgets-1/0/1/16/1024 match independent unsigned ordering and exact value multiplicity; both guards remain intact.

Backed-up trial, promotion and independent reopening verify the name/signature, original instructions and unchanged archives. The original copy import resolves to an explicit overlap-safe model; malformed ranges, concurrent mutation and actual library copy remain unverified. Totals:283 checked names among9,576 functions;1,724 mapped and7,852 unmapped. No whole-subsystem completion claim.

### Sculpt bounds flag construction

The sculpt-bound/body-wakeup worker calls a helper that constructs the flags stored beside each bound.57,600 original-instruction cases compare its complete32-bit return with an independent bit model, including11,520 skipped-player-query and46,080 mode-zero player-query cases.187 instructions across the flag helper and filter match the original executable. Complete object/body-table bytes and selected context/state windows remain unchanged.

The tests cover per-object bitset mask4, player-filter contribution16, category-byte shifting, ordered positive level mask8, object/auxiliary masks1/2 and selected body/extra metadata contributions. Native NaN comparison leaves mask8 clear. These establish numeric mechanics, not complete gameplay names for the bits. Other parent/filter modes, full large state allocations, the worker’s wakeup behavior and in-game execution remain unresolved. No new names or completion credit;283 names remain checked.

### Saved sculpt-bound flag helper name

Applied BuildSculptBoundsFlags with opaque Game/current-state/sculpt pointers, signed body index and32-bit flag return.93 original instructions and57,600 scoped hardware cases support its role. Cold backup, isolated trial, promotion and independent reopening verify the name/signature, unchanged original instructions and archive hashes.

Bit mechanics remain numeric where gameplay meaning is unresolved. Other player/parent filter modes, full large state allocations and parent worker wakeup behavior remain unverified. Totals:284 checked names among9,576 functions;1,725 mapped and7,851 unmapped. Current status snapshot is dated2026-10-15. No whole-subsystem completion credit.

### Object/player mask and parent-mode filter

Applied PassesObjectPlayerMaskAndParentModeFilter with encoded object reference, opaque player/state pointers, player index and boolean AL return.7104 original-instruction cases cover direct masks, early rejection, cached high/low record indices and fallback scans. Mode1 uses high7 cached bits; other nonzero modes use low7 bits with a record-mode check. Scans compare the full encoded parent, while cached lookup normalizes its index. Nonzero modes accept when no record resolves.

Full object/player/record tables and cached map remain unchanged. Backed-up trial, promotion and independent reopening verify the saved signature and original bytes/archives. Gameplay mode meanings, cache construction/invariants and invalid/null object lookups remain unresolved. Totals:285 checked names among9,576 functions;1,726 mapped and7,850 unmapped. No whole-subsystem completion credit.

### Sculpt worker wake-state branch

An inspection-only function definition in an isolated project exposes the complete1732-byte worker without changing the main project.768 original-instruction cases validate the comparison/wake bookkeeping branch with valid sculpt/resource/body fixtures and the bounds-active header flag clear. Checks cover the complete job context, full prior/current objects and the wake flag window.160 cases take the wake write and384 mark notifications.

The wake-state write requires a previous counterpart and body, then selected object-byte or state changes. It updates low16 flags to(initial&0xf0fb)|4 while preserving the adjacent upper16 bits. A change only to the vector’s fourth component is ignored; selected xyz/scalar NaNs count as changes. The job’s atomic counter and notification behavior also match the independent model. Bounds-active geometry calculations, full large state buffers, concurrent scheduling and actual gameplay wake effects remain unverified. No new main-project definitions or names;285 names remain checked.
