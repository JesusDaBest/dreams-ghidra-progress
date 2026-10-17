# Dreams: decompilation results and findings

## Controlinator properties linked to transform selection — 2026-10-17

Original property registration now identifies four fields read by `ResolveObjectTransformForAuxiliaryContext` (`141046d40`). The field offsets, original strings, enum values and runtime instruction bytes were checked against the local executable and the saved Ghidra program. Four instruction annotations persisted after reopening the backed-up project.

| Original property | Offset | Verified use on this branch |
| --- | --- | --- |
| `CtrlMode` | `0x1a0` | Must equal `FollowController` (2). The original enum is spelled `EControllinatorMode`. |
| `InputDisableControls` | `0x1f7` | Must be zero. |
| `playeridx` | `0x122` | Registered through the `PlayerIdx` helper; 255 rejects this path, otherwise the index selects a record with stride `0x19c50`. |
| `FollowImpMode` | `0x1a1` | Compared with `Gun` (2), selecting between the already traced transform paths. |

The original `EFollowImpMode` registration maps 0 to `MaintainGrabOrientation`, 1 to `FaceDockToCamera`, 2 to `Gun`, and 3 to the `LAST` sentinel. The original `EControllinatorMode` registration maps 0 to `None`, 1 to `Possessable`, 2 to `FollowController`, 3 to `Remote`, 4 to `FollowRemoteController_Deprecated`, and 5 to `LAST`.

These names come from property and enum registrations, rather than inferred UI wording. Registration helpers preserve the property-name and object-offset arguments and write them into the same field descriptor. The runtime reads then match those offsets on the Controlinator kind branch. These conditions are necessary on this branch; additional state and flag gates remain. This trace does not establish every controller mode, all `PlayerIdx` values, or the complete property registrar's semantics. No function-name review credit or completion percentage was added for these annotations. Raw assembly and backup manifests remain local.

This is the written account behind the status map. The [research data](analysis/research-details.json) records failure addresses, saved signature corrections, proposed names, and matched property fields. [PROGRESS.md](PROGRESS.md) contains the applied naming ledger; [MAPPING.md](MAPPING.md) explains the system assignments.

## Initial extraction and naming snapshot

The table below records the early project baseline. For current totals, see the [latest progress](README.md#latest-progress); subsequent sections record the later reviews and corrections.

| Work | Recorded result |
| --- | --- |
| Function inventory | 9,551 discovered functions |
| Frozen v1 extraction | 9,508 functions with cached C-like pseudocode; 43 failures |
| Applied descriptive names | 30, verified after reopening the project |
| Deferred naming reviews | 4 |
| ReporterTelemetry names | Three applied and verified after reopening |
| System mapping | 1,540 functions associated with nine systems; 8,011 still unclassified |
| Saved signature corrections | Six field-registration helpers; native reopen checks passed |
| Frozen v2 extraction | 9,513 cached outputs; 38 failures; all 9,551 functions accounted for |

These are separate stages. Extracting pseudocode gives us code to inspect. Mapping establishes its association with a part of Dreams. Checking a descriptive name requires evidence for that function's particular role. The status map tracks the applied naming reviews within the mapped inventory.

The pseudocode is generated from machine code. Original source files, original local-variable names, complete class definitions, a complete build, and a working reconstruction of Dreams have not been recovered.

## Executable and calling convention

The supplied analysis is a Windows PE wrapper with embedded `.elf` sections. A sample of 1,664 code bytes matched the PS4 SELF reference using an address mapping offset of `0x140010000`. This establishes the sampled relationship; it is not a whole-binary equivalence proof.

The original Windows calling convention obscured PS4 arguments. A validated `PS4_SYSV` model was applied to 9,486 eligible functions, with 19 thunks inheriting their targets' convention. The frozen v1 snapshot therefore records 9,505 effective assignments. Its 45 existing explicit signatures were initially preserved.

Later work corrected the inputs of these six explicit field-registration helpers:

| Address | Existing function name |
| --- | --- |
| `14010fc00` | `RegisterFloatFieldOffset` |
| `140cd8b00` | `RegisterBooleanFieldOffset` |
| `140cdbb80` | `RegisterTransformFieldOffset` |
| `140cdca90` | `RegisterGadgetNameFieldOffset` |
| `140ceccc0` | `RegisterFloat2FieldOffset` |
| `140d5f6c0` | `RegisterCanvasPropertiesFieldOffset` |

Native instructions and callers establish a registry in RDI, a property key in RSI, and the object's field byte offset in EDX. The saved corrections recover the missing input while preserving the existing offset's meaningful name, width, and EDX storage. Return types were preserved; return contracts still need separate review.

The promotion was tested on a copy, saved to the working project, and checked after reopening through the native Ghidra API. Metadata and selected decompilations matched the recorded post-change state, and all 27 checked names were preserved. The live MCP readback now confirms all six corrected signatures, four caller signatures, body sizes, conventions, and all 27 applied names. All ten MCP decompilations match native Ghidra using the same default options. The other 39 explicit signatures remain deferred.

The newer verified snapshot contains these changes. Its separate v2 initial pass is complete and audited: all 9,551 functions were attempted, 9,490 complete output hashes were verified, and 61 failures were recorded (59 timeouts, one flow-limit failure, and one forced-merge failure). Every address and terminal attempt matched the inventory, and no successful output was re-decompiled. All 59 eligible timeouts received one additional 60-second attempt. The final audit verified 9,513 complete output hashes and 38 failures: 36 timeouts, one flow-limit failure, and one forced-merge failure. It checked all 9,551 inventory addresses, all 9,610 attempt records, and the absence of repeated successful extraction. Both the initial and final failure lists are retained separately. The older v1 cache remains intact. The per-address status now uses v2 extraction and convention data; current naming reviews are joined separately by address. The system-map evidence still comes from unchanged native code in v1. No code outputs from the two cache versions were mixed.

The MCP server uses a default DecompInterface, whereas native cache extraction loads the saved program's decompiler options. Seven of ten sampled outputs differed between these configurations, including whether constant data was folded into literal values. All ten outputs matched exactly when native Ghidra used the MCP defaults. This is an options comparison, not evidence of a program change or additional semantic-review progress. Original archive, imported-copy, and SELF-reference hashes were rechecked unchanged.

Global Windows data organization has not been replaced. SIMD arguments, indirect callbacks, return contracts, native type sizes, and complete layouts still need checking against instructions.

## How Dreams describes object properties

The inspected code contains explicit type descriptors, field-registration routines, and visitors that access the same fields at matching object offsets. Those links let us distinguish an object's properties from the algorithms that implement its behavior.

Several visitors are shared between many object types:

| Shared property type | Established observations |
| --- | --- |
| Pos | The helper visits transform and legacy physics data. Calculator uses it at `+0x40`; many other objects use it too. Its role is broader than a position vector. |
| CanvasProperties | Calculator's TweakProps at `+0x90` matches an explicitly named descriptor with a `0x40` field extent. The visitor handles canvas transforms, bounds, and packed data. |
| Variant | Calculator OperandA and OperandB at `+0xd8` and `+0x100` match an explicit Variant descriptor with a `0x28` extent. The visitor uses a tag at `+0x24` and alpha at `+0x20`. Tag meanings and the full union layout remain unresolved. |
| GadgetName | Calculator's Name at `+0x128` matches an explicit GadgetName descriptor with an eight-byte field extent. Its encoding remains unresolved; it is not established as a raw string pointer. |

The confirmed gadget clusters include:

| Cluster | Evidence and useful distinctions |
| --- | --- |
| Calculator | Distinct OperandA, OperandB, and Name fields link its visitor to the shared Variant and GadgetName registration helpers. |
| Splitter | InputA at `+0xd8`, Name at `+0x100`, and RotationRepresentation at `+0x108` distinguish its layout from Combiner. |
| Combiner | Nine field registrations match the visitor, including FatWireType at `+0xd1`, Name at `+0xd8`, and RotationRepresentation at `+0xe0`. Two labels are supplied by specialized helpers rather than direct literal arguments. |
| MagicDoor | All 23 registered fields match the visitor. Distinctive fields include MagicDoorType at `+0x119`, MagicDoorOpenUI at `+0x124`, and MagicDoorUseSpawnTrans at `+0x151`. |
| SignalInspector | All 16 fields match. InputA is at `+0x118`; TimeSinceChange and BrightnessOnChange use byte accesses at `+0x140` and `+0x141`. Their labels alone do not establish floating-point types or time units. |
| SignalGenerator | All 14 fields match, including SweepSeconds at `+0xd8`, PauseSeconds at `+0xe0`, OutputNormalised at `+0xec`, RandomTime at `+0x108`, and RandomMag at `+0x110`. |
| CameraShaker | Eleven field labels and offsets match between registration and visitation. |
| PadRumble | Thirteen field labels and offsets match between registration and visitation. |

The [research data](analysis/research-details.json) includes all 77 matched fields from the MagicDoor, SignalInspector, SignalGenerator, CameraShaker, and PadRumble reviews. These observations support the applied function names. They do not establish complete object layouts, serialization direction, version-gate meanings, or the runtime camera-shake and rumble algorithms.

## Object types and system mapping

The game's object-type enum registers numeric identities. Matching those values to the native 120-entry property-dispatch jump table resolved every branch. Of those branches, 119 have a system classification; the legacy Key case remains unclassified.

Examples include Sculpt at tag `1`, SignalInspector at `0x4a`, PuppetControls at `0x57`, and ReporterTelemetry at `0x51`. Exact dispatch links resolve cases where different object types share field names. Source-file references also associate code with CSG, sprite processing, rendering, collision, the editor UI, and Dreamiverse pages.

The complete per-address assignments and evidence are in [system-map.json](analysis/system-map.json). These associations are incomplete research classifications. They do not establish the complete size or complexity of each game system.

## ReporterTelemetry: applied descriptive names

| Address | Applied name | State |
| --- | --- | --- |
| `1404de8c0` | `VisitReporterTelemetryProperties` | Applied; verified after reopening |
| `140d6c700` | `RegisterReporterTelemetryFieldOffsets` | Applied; verified after reopening |
| `140d580d0` | `RegisterReporterTelemetryTypeDescriptor` | Applied; verified after reopening |

An exact ReporterTelemetry literal is installed on descriptor `1458afdd0`. The initializer links the Thing base descriptor and transfers to the field registrar. All 14 registered fields match the independently inspected visitor, including six TelemetryKey fields at `+0xe0` through `+0x108`, and TimeSinceSend at `+0x110`. Dispatcher tag `0x51` corroborates the identity.

The extension fields are guarded by a visitor-state value of at least `0x1869f` (99,999), with additional filtering conditions. The meaning and normal reachability of that threshold are unresolved. This review establishes property roles; it does not establish transmission behavior, recipients, payloads, or a reporting algorithm. The three descriptive names were applied with reversible journals and a cold backup, then verified after reopening. A subsequent immutable reopen audit compared all 9,551 functions against v2 plus those three approved name changes, including signatures, parameter/local metadata, bodies, and comments. Types, external functions, memory, block permissions, and symbols also matched; symbol names and sources were normalized only for the three approved renames. A closed checkpoint copy passed byte-for-byte verification. They bring the applied-name total to 30. The frozen v2 extraction still uses its earlier 27-name snapshot; no cached output or snapshot was rewritten.

## Extraction failures and experiments

The frozen cache has 41 timeouts, one flow-limit failure at `1401180e0`, and one forced-merge failure at `14146b220`. Every failed address, body size, and attempt count is listed in [research-details.json](analysis/research-details.json).

For `1401180e0`, a disposable-copy experiment expanded the analyzed body and supplied candidate switch references. It produced pseudocode successfully. Fifty table entries had local targets, but the byte selector permits values up to 255 and no explicit upper-bound guard was established. The legal selector domain therefore remains uncertain. The experiment was rolled back and was not promoted as a production fix; the frozen failure count remains 43.

For `14146b220`, normalization succeeded and exposed intermediate control-flow information. That mode does not produce extracted C. A separate full-decompilation attempt with array splitting disabled still failed with the forced-merge intersection error and produced no C output. Both experiments left the production cache unchanged.

The final v2 mechanical scan inspected all 9,513 cached outputs. It flagged 5,919 functions with decompiler warnings, 230 with unresolved register inputs, 367 with unresolved SIMD call outputs, 90 with invalid or unimplemented flow patterns, and 1,292 with an indirect-call pattern. These categories overlap; a flag is a review lead, and no flag does not prove correctness. Every discovered address has a local scan or failure record and a next step. This adds no semantic-review credit.

An earlier mechanical quality scan inspected 9,482 v1 outputs while extraction was still in progress. It flagged warnings, indirect calls, unresolved register inputs, and SIMD-call outputs as review leads. Its counts are not a final audit of all 9,508 cached outputs and are not semantic-review credit. The completed extraction integrity audit separately checked all 9,508 cached file hashes and the full 9,551-address inventory.

## Remaining work at the initial snapshot

Extraction and accounting for the current inventory are complete. Research remains partial: 38 extraction failures need targeted investigation, 39 explicit signatures remain deferred, 4 naming reviews remain unresolved, and 9,517 functions have no completed semantic naming review. The next research work is to investigate those failures, validate deferred signatures, extend the code-to-system map, and review the functions within those systems. Further proposed names must be applied and checked after reopening before they receive applied-name credit. Full signatures, layouts, and algorithms need their own evidence.

The public files contain findings and structural evidence. Raw pseudocode, binary inputs, Ghidra projects, and unfiltered local reports are retained separately. That separation does not reduce the extraction counts or mean the locally saved work was undone.

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

### Object hierarchy transform: floating-point guard

Static tracing of the transform helper at `140903590` resolves its imported guard at `141608170` through slot `141c66f00` and the loader's literal NID `rDMyAf1Jhug`. Recomputing the symbol hash for `__isinff` matches that NID; the pinned [GhidraOrbis symbol database](https://github.com/astrelsky/GhidraOrbis/blob/2d6e3fac23ae9830e941c32826e97100ed603311/data/nid_db.xml) independently records the same mapping. A known `memmove` NID serves as a hash-method control.

The assembly selects an identity quaternion for zero squared magnitude or an infinity reported by that guard. Near-unit finite products are retained; other finite nonzero products take reciprocal-square-root normalization with one refinement. A NaN magnitude reaches an unordered comparison whose branch retains the product, so this path does not establish NaN sanitization. This refines the earlier quaternion-composition analysis; it is static evidence, with floating-point exceptions and runtime behavior still untested. No new name or datatype was applied in this step.

## Object hierarchy transform name verified

`140903590` is now `ComputeObjectHierarchyTransform`. All 210 assembly instructions and the complete cached body establish parent-chain traversal and composition of a 32-byte position/scale plus quaternion result. An independent caller's complete 136-instruction body confirms its input/output use. Symbolic evaluation checks quaternion multiplication order, and the loader import ID plus recomputed hash identifies its infinity guard.

The name is descriptive. Native category meanings, cache invariants, external handedness and runtime validation remain unresolved; NaN sanitization is not established. A cold project backup preceded the edit. A clean restart verified all 57 names, the full 9,551-function inventory, unchanged metadata for this routine, and unchanged original archive hashes. No datatype, signature, calling convention, bytes or boundaries were edited. There are 57 verified names, 4 deferred reviews and 9,490 unreviewed functions. The map now contains 1,555 assigned functions, including 10 runtime/helper reviews and 41 property/type reviews.

## Teleporter runtime ownership

Native object tag `31` is Teleporter, confirmed from the enum's literal registration. A guarded call in the general property dispatcher passes that exact object to `1408f1dc0`; its offset reads match the Teleporter descriptor's `PosOffset` field at `+f0`. Its full 136-instruction body is now named `ComputeTeleporterTransformWithOffset`. It composes the object hierarchy transform with that offset; zero offset xyz uses active physics-body or cached object translation.

`140d78870` is now `RegisterTeleporterFieldOffsets`: its full 71 instructions bind 15 literal fields plus base position to descriptor `1458a7770`. Its full 42-instruction initializer, `140d55830`, is named `RegisterTeleporterTypeDescriptor`. Both survive reopening. These are descriptive names; no types, prototypes, conventions, bytes or boundaries were changed.

The map now places two runtime functions under Gadgets & logic / Movement & possession / Teleporter. The second, `1408f2180`, independently checks tag31 and computes an offset before a property operation; its 121-instruction body was read, but the property-write helper and context-mapping semantics remain unresolved, so it remains unnamed and incomplete. The general multi-type dispatcher is not assigned wholesale to Teleporter. Teleport execution, priority arbitration and fade behavior are still unreviewed.

There are 60 verified names, 4 deferred reviews and 9,487 unreviewed functions. Reopening verified the complete 9,551-function inventory and unchanged original archive hashes. The map contains 1,558 assigned functions, with 11 runtime/helper names and 43 property/type names checked. Whole-feature completion remains unknown.

## Shared transform-property command path

`140705a90` is now `FindPackedObjectPropertyPayload`. Its full 22-instruction, 68-byte body searches the list at object `+18`, compares 16-bit identifiers, advances by a two-byte header plus the per-identifier payload size, and returns a payload pointer or null at the `ffff` terminator.

`140ad5f90` is now `TransferTransformPropertyPayload`. Its full 62-instruction, 267-byte body copies a 32-byte stream payload into a destination in mode 0. Mode 1 writes the destination's first float4 and normalized quaternion to the stream. Other modes only advance the cursor; every mode advances it by 32 bytes. All 13 direct branch targets across both helpers were checked. Both names survived reopening; no types, prototypes, conventions, bytes or boundaries changed.

The native command `10a` record contains a six-byte header and 32-byte payload. Its exact jump-table entry resolves to `140ae49d3`, which looks for a packed property payload, falls back to a positive type-specific inline offset, and reaches the transfer helper. With an existing payload, the write path synchronizes the inline copy only when the previous packed and inline values match. This is a bounded review of that branch, not the whole large dispatcher.

The Teleporter caller constructs a translation/scale plus identity-quaternion payload; an exact zero xyz result is replaced by the smallest positive normal float in those lanes. The sentinel's intent remains unproved. The archived type-offset table slot is zero. The subsequent initializer review below resolves its compiled binding to Teleporter's registered `PosOffset`; the static zero alone did not reveal that binding.

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


### Sphere filtering: decoded rejection and fitting arithmetic

The small `SphereVsSphereCheck` shader was decoded through its first end instruction, with all five branch targets checked. Its checked arithmetic marks a sample's radius negative when it is contained by a positive-radius peer or has no overlapping peer. Containment compares center distance plus the absolute sample radius with the absolute peer radius. Overlap compares center distance with the sum of absolute radii. The shader reads and writes the same sample array; parallel ordering and determinism remain unresolved.

The larger `TestSpheresAgainstSDF` shader was physically decoded through its first end instruction: 485 instructions and 20 branch targets landing on instruction starts. This is decoding coverage, not complete behavioral understanding. Its two four-value gathers use the same eight-sample trilinear polynomial and corner order (3, 2, 0, 1) previously checked in the contact shader. The result is remapped to `4*sample - 2` and scaled by a power of two. The starting exponent comes from the top four bits of packed resource offset `+0x50`; each child descent decreases the current exponent used for sampling.

Separate lane and operator checks establish reductions across 64 lanes. The candidate-position calculation uses the current center plus a direction vector multiplied by the old radius minus a sampled lane value. Exact coefficient checks show that each candidate position contributes once to the mean position, and each distance from that mean contributes once to the mean distance. A subsequent loop limits the iterative radius candidate by distances to other sample centers, skips its own index, and advances per-lane indices by 64. This loop loads peer xyz, not peer radii.

The exit store writes the center and a distinct fourth-value register, rather than directly storing that iterative radius candidate. A checked path at iteration counter 24 can write a minus-one rejection value. The native caller later retains only records whose fourth value is positive. Direction normalization, coordinate provenance, exceptional paths, lane initialization, asynchronous execution, and the complete convergence contract remain open. No new names, types, or complete-behavior coverage are credited: the naming total remains **77**. Raw shader payloads and captures remain local.


### Sphere directions and packed-volume traversal

Native setup allocates 768 bytes for 64 three-component vectors, with a 12-byte descriptor stride. Its checked loop constructs a base-two radical-inverse vertical coordinate and an angular coordinate, then writes three floats per vector. The trigonometric thunk resolves through the converted executable's loader to the `sincosf` import identifier. The resulting construction has unit length in ideal arithmetic; all 64 reconstructed directions are distinct. Host reconstruction is not a measurement of original-library rounding or runtime GPU contents.

The SDF shader transforms the initial sample point through the packed resource scale and offset, with a decoded factor approximately 1/7 and the starting power-of-two level. Atlas setup multiplies local coordinates by 7, clamps them approximately to 0.01..6.99, and uses their fractional parts for the checked interpolation weights. Three packed atlas coordinates supply eight-unit bases; the two gathers use neighboring slices separated by exactly one unit.

Child traversal selects octant bits with strict half-coordinate comparisons, remaps coordinates into the selected child, and extracts little-endian three-byte entries from two adjacent words. The byte-alignment expression was checked against a pinned primary shader implementation and 1,024 packed-entry cases, including word crossings. Flagged entries remove lanes. At level zero a sentinel removes remaining lanes before decrementing, bounding this checked traversal path to at most 16 sampled levels. Importantly, the sample exponent is the **current traversal level**, not always the starting packed exponent.

Full shader masks, exceptional paths, GPU ordering and convergence remain unresolved. These findings add no names, types or complete-function coverage. The 77-name baseline and displayed status counts are unchanged.


### Sphere fitting: masks, replacement rules and compute binding

For finite inputs, the initial sampling mask selects nonnegative local coordinates; it does not itself impose an upper bound or establish finite-input safety. The shader saves the execution mask before narrowing it, initializes the sampled value to positive infinity, and later restores the saved mask. Lanes skipped by this initial mask select the earlier bounds-related fallback. The checked finite-class mask excludes infinities and NaNs; the negative-class mask distinguishes negative zero from positive zero. This is a static path finding, not a complete exceptional-input safety claim.

An exact polynomial check identifies three opposite-face differences of the eight gathered samples. These unweighted differences are not claimed to be the exact position-dependent derivative of trilinear interpolation. Before fitting, the components are divided by their maximum absolute component. Their resulting Euclidean length and the absolute resource scale then adjust the selected value. This is maximum-component scaling, not unit normalization; zero and nonfinite components remain open cases.

A separate packed four-bit threshold gates two replacement rules. Below the threshold, selected lanes retain the previous direction and may adopt a larger current magnitude. At or above it, selected lanes may adopt a smaller current magnitude and current face differences, subject to another checked cutoff. Both paths explicitly preserve the previous sign bit. The decoded Boolean predicate and replacement instructions were checked separately; original field names and complete exceptional behavior remain unresolved.

Native binding was traced from the shader loader's header pointer through the command helper and converted executable import table to `sceGnmSetCsShaderWithModifier`, with modifier zero. The register ordering matches a 64-by-1-by-1 compute group, seven user SGPRs and an enabled x workgroup ID. The primary compute prologue initializes vector register zero from the local x thread index. This supports the peer-index traversal and single-local-index-zero output interpretation without claiming measured GPU execution.

The direct correction path uses per-lane values, so a shared center cannot be assumed throughout fitting. The scalar counter and checked equality exit bound the outer loop to 25 evaluations. Runtime ordering, convergence, complete exceptional paths and the full shader contract remain unverified. No names, types or complete-behavior coverage are added; the verified name total remains **77**.


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

### Sound Power, triggering and Playhead

Native code links Sound's registered Power field to a comparison against a paired object. A nonzero/zero discriminator passes through additional gates into `newly_triggered`; related paths update `updatethings_counter_when_triggered`, clear `muted_by_speaker`, and update `PlayingInternally`. The destination object and paired Power object come from separate owner contexts. Their temporal ordering is still being investigated, so this is not yet labeled a confirmed previous-to-current frame edge.

The selected playback position reaches Sound's registered `Playhead` field. Normal advancement uses `CompositePlaybackSpeed` multiplied by approximately 1/30, with separate triggering, bounds and mode gates. Sound duration uses a 48,000-sample-per-second conversion for sample records, separate canvas handling, and an adjustment when granular playback is enabled. This does not establish the complete Sound subsystem or every branch of its large update routine.

`GetThingTimeBounds` had an incorrect two-argument calling convention and signature. Its native body and all 50 statically referenced direct call setups support four arguments: object, minimum float output, maximum float output, and trim flag. A cold backup and isolated trial preceded correction to `PS4_SYSV`; the corrected signature and function inventory were verified after reopening. Only that function's signature changed, and its instruction bytes and original archives were preserved. The trial also exposed downstream signatures that remain unresolved.

[Media Molecule developer Bogdan Vera’s 2020 audio presentation](https://www.youtube.com/watch?v=-UyiXUJcIQ0&t=3046s) describes Power as both a volume input and a trigger-edge input. The static trace supports that direction of investigation, but the presentation is a lead rather than proof of this executable's complete behavior. No additional checked names, runtime validation, full-function behavior credit or whole-game completion percentage was added for this partial trace.

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

### Animation sample differences applied to a base value

The two-time evaluator samples an Animation record at two times relative to its timestamp, computes a difference, and applies it to a supplied base value. Current native code confirms the same-type paths for internal tags 6 and 7: four float components for tag 6, and three components with the unused fourth lane cleared for tag 7. These paths subtract the first sample from the second, then add the result to the base. A separate float at payload offset `+0x20` has its sign bit cleared during base application; its source-level meaning is still unknown.

Four live secondary jump tables establish which branches these tags actually select. All table targets are instruction boundaries, and all 1,663 captured instructions still match the earlier native capture. That comparison checks staleness; it does not establish understanding of every branch. Other type conversions remain under investigation; the same-type tag-16 rotation path is described below. No new name, signature change, or completion percentage is credited for this bounded finding.

### Animation rotation difference and application order

The same-type tag-16 branch is now resolved as quaternion arithmetic. In scalar-last Hamilton notation, it computes and normalizes `second_sample * conjugate(first_sample)`. The application stage computes and normalizes `delta * base`, establishing the multiplication order in the reviewed path. Native lane equations were checked algebraically, and live jump-table entries confirm the selected branches.

Both stages compare the squared norm against approximately `1.42108547e-14`. At or below that threshold, or when the comparison is unordered, the branch selects `[0, 0, 0, 1]`. Above it, normalization uses a reciprocal-square-root estimate with a refinement step. The algebra establishes the operation, not bit-identical results under arbitrary floating-point reassociation or behavior for every nonfinite input. Original type names, coordinate handedness, other conversion paths, and full evaluator behavior remain unresolved. No new name or full-function completion credit is added.

### Animation delta helper named and saved

`EvaluateAnimationDeltaOnBaseValue` now describes the helper that samples a record twice, computes a type-dependent difference, and applies it to a supplied base value. The scalar, two-, three-, and four-component paths and the quaternion path were reviewed in native code. Both direct call sites are in the Animation property evaluator; a conditional first result can become the base input to the second call. Its route uses `PlayheadDelta` and a successful base-property read. Complete loop-boundary behavior and remaining conversions are still unresolved.

The descriptive name survived a clean reopening, all 1,663 native instructions and both direct references were unchanged, and the full name inventory matched the baseline plus recorded changes. The prototype remains uncorrected. This adds one checked name and one evidence-supported Animation mapping: 144 checked descriptive names overall, with 1,601 mapped functions and 7,952 still unmapped. It adds no full-function behavior completion credit.

### Animation sampler record layouts

Both discovered callers use bit 2 of record byte `+0x0a` to select between two sampler implementations. The reviewed common paths count 20-byte entries when the bit is clear and 24-byte entries when it is set. Their reciprocal multiply/shift count arithmetic was proved exact across the masked-header range. Both read a float-sized leading field and 16 payload bytes on the contiguous-leaf path; the 24-byte layout also reads another 32-bit word. The flag's original name remains unknown; decoded controls in the extra word are described below.

The second caller samples into a local value, converts it to two vector blocks, compares those blocks against reference data, and retains a running maximum of the measured difference. This supports a sampling-error interpretation, but does not establish the purpose of the complete caller. The conversion helper's complete 32-instruction body was reviewed: it copies two blocks for tag 4, extracts three components and inserts a fourth component of 1 for tags 7 and 20, and supplies default blocks for other tags. The remaining call sites are covered in the shared-helper review below.

These findings cover specific dispatch, layout, and comparison paths. The large sampler bodies, cross-leaf reconstruction, interpolation details, and original types remain incomplete. No names, prototypes, or full-behavior completion credit were added in this review.

### Shared tagged-value conversion named

`ConvertTaggedValueToTwoFloat4Blocks` is now named after reviewing its complete 32-instruction body and all 13 direct caller argument/result neighborhoods. Callers copy its 32-byte output, use both blocks in Animation sampling and blend math, compare them with reference values, or unpack eight components for a callback. The name describes the observed conversion; original structure names and complete caller behavior remain unresolved.

After a cold backup, only the name changed. A clean reopening verified that name, all native instructions, and the full direct-reference list. The prototype remains unchanged. The function is mapped to shared property data rather than credited exclusively to Animation. There are now 145 checked descriptive names and 1,602 mapped functions; no full-behavior completion credit was added.

### Animation time snapping and gap-dependent sampling

The common 20-byte sampler path snaps a query to nearby timestamps using a strict tolerance of approximately `0.0001`. Its interior search adjusts neighboring record indices using the midpoint timestamp minus that tolerance. The selected timestamps receive another snapping check before the payload operation.

The payload operation is not always interpolation. When the native comparison finds `lower_time + 0.05000000447 > upper_time`, it forms a linear blend of the four-component payloads. The alternative path chooses the lower or upper sample, switching on an ordered query greater than approximately `upper_time - 0.03333333507 + 0.0001`. Native unordered comparisons follow the selection branch; duplicate/unsorted timestamps and nonfinite inputs are not assumed valid.

A separate before-first branch reads the registered Animation field `AnimUseNewBehavior`. Under its ordered time conditions, that field can zero output metadata and set an optional flag. It is distinct from the record flag that selects 20-byte versus 24-byte layouts. These are bounded native findings; cross-leaf reconstruction, later blending, and complete sampler behavior remain unresolved. No additional names or completion credit were added.

### Animation per-sample interpolation controls

The extra word in the reviewed 24-byte path carries interpolation controls. Its low three bits select a mode; modes 1–4 respectively preserve linear alpha, ease in, ease out, or ease in/out. Four bits supply strength. Native calls were linked through the executable's loader to `powf`, supporting the decoded power-curve formulas. Nonzero bits 6–7 can quantize elapsed sample time downward in steps of approximately 2/30, 3/30, or 4/30 before alpha is calculated.

The 24-byte path also differs at larger time gaps: a nonzero curve mode can force interpolation depending on another control bit and the entry count. Endpoint bit 4 changes whether payloads blend or an endpoint is copied with adjusted output metadata. These are decoded mechanics, not recovered UI names or proof of which editor settings produced the records. Record producers, other type branches, resource reconstruction, and later blending remain unresolved. No additional names or full-behavior completion credit were added.

### Animation value types and intermediate representation

The executable's `EVariantType` registry explicitly names tag 6 `Float4`, tag 15 `AudioNumber`, and tag 16 `Quaternion`. Rechecking all 32 registered literals and 227 instructions against the live project confirms the earlier registry evidence; this is not counted as a new discovery of those names.

Tracing that registry into six reviewed output neighborhoods clarifies the common sampler path. Both formats save the input record's type byte, compare it with 16, and write a result tag of 16 when equal or 6 otherwise. Thus these Quaternion paths preserve their tag, while the AudioNumber common path produces a Float4-tagged intermediate. The representation change does not establish equivalent behavior for the two types.

The four-lane blends described above are not evidence of quaternion spherical interpolation or a complete AudioNumber implementation. Other dispatch branches, later processing, and record producers still require analysis. This checkpoint adds evidence and clarification, with no new names, prototype changes, or full-behavior completion credit.

### Conditional Quaternion blending after sampling

A later, optional stage in the 20-byte sampler calls shared helper `1411c1590`. An ordered zero control value bypasses this stage; nonzero or unordered values enter it. The caller supplies two tagged values and requests weight normalization, then copies the result back and restores earlier output metadata. This stage therefore does not normalize every sampler result.

For two Quaternion inputs, the helper preserves the type and loads both four-component payloads. It can flip every sign bit of the first input when their dot product is strictly below approximately `-0.01`, then forms a weighted sum. The threshold differs from the zero threshold often assumed for quaternion sign correction. The reviewed path uses normalized linear blending, not spherical interpolation.

The result is scaled using a refined reciprocal-square-root estimate when its squared norm is ordered greater than approximately `1.421e-14`. Smaller or unordered norms select the identity Quaternion `[0, 0, 0, 1]`. Earlier large-weight copy shortcuts can bypass this math. Mixed-type conversion, other value types, overflow behavior, and further sampler stages remain unresolved. The findings come from current native instructions, dispatch tables, constants, and the caller's argument/result flow; no new name or full-behavior completion credit was added.

### Animation strength uses a separate interpolation stage

The registered `AnimStrength` setting controls a later stage of the reviewed 20-byte sampler. A strength exactly equal to 1 bypasses it. Other values must also pass an integer gate and a value-type exclusion mask; the integer's provenance across all sampler routes remains unresolved. The caller supplies the sampled value, an endpoint-derived value, and strength to helper `1411dd230`.

For two Quaternion values, this helper uses strength to interpolate from the endpoint-derived value toward the sample. It corrects a negative dot product by reversing the base Quaternion's sign. When the absolute dot is greater than approximately `0.99999`, it uses a linear blend without an explicit normalization in that branch. Otherwise it uses the spherical formula with `acosf` and `sinf`; the executable's loader and import trampoline independently establish the `sinf` identity.

This is a separate stage from the normalized weighted blend above. Both can occur along the reviewed sampler route, so identifying one does not describe all rotation processing. Endpoint construction, valid input ranges, mixed-type behavior, and the complete sampler remain unresolved. No additional names or full-behavior completion credit were added.

### Strength base traced in both record formats

On the reviewed contiguous record routes, the strength blend's base comes from the initial 16-byte payload read. Both samplers save two eight-byte halves and later reassemble them as the second tagged argument to `1411dd230`; the sampled output is the first argument. This connects the blend to saved record data, rather than assuming its base is the current neighboring sample or the identity Quaternion.

The 24-byte format reaches the same strength helper with the same setting and type-exclusion mask as the 20-byte format. Its additional integer gate uses 48 where the 20-byte route uses 40. These thresholds match two entry sizes, but that correspondence alone does not prove the integer's meaning across every route.

Current memory checks cover 158 instructions across six bounded regions. Cross-leaf reconstruction and alternate paths still need tracing before this base interpretation can be generalized. No additional names or full-behavior completion credit were added.

### Animation strength interpolation helper named

`InterpolateTaggedValueFromBase` now names the shared strength helper at `1411dd230`. Its 302-instruction body and all 26 direct argument/result neighborhoods across 21 sampler functions support this role. The strength input was traced to the registered `AnimStrength` field, including nine predecessor paths outside the original inspection windows. Quaternion and Position paths have dedicated rotation interpolation; other tags delegate to weighted tagged-value blending and restore the target metadata.

The change affects only the name. A cold backup preceded it, and a clean reopening verified the name, unchanged instructions, all direct references, and unchanged prototype. The complete function-name inventory and both original archive hashes were also checked. There are now 146 checked descriptive names and 1,603 mapped functions. Mixed-type conversions, input ranges, and complete sampler behavior remain unresolved; no full-behavior completion credit was added.

### Numeric animation storage and quantization

The Number record dispatcher selects numeric samplers through property metadata. Six traced selectors lead to unsigned 8-, 16-, 32- and 64-bit storage, signed 32-bit storage, and scaled signed-byte storage. Enum records also reach the unsigned-byte sampler directly. Original selector names and descriptor-index bounds remain unresolved.

The reviewed contiguous entries use 12 bytes for the smaller formats: a float timestamp, a payload field, and a control word. Unsigned 64-bit entries use 24 bytes, with the payload at entry offset 8 and control word at 16. Padding and alternate resource-tree routes are not fully characterized.

These paths produce Number-tagged sampled values, but their quantization differs. The unsigned byte and word paths truncate the interpolated float and retain its low 8 or 16 bits. Unsigned 32-bit storage uses a wider conversion before retaining 32 bits. Signed 32-bit interpolation quantizes through signed integers. The scaled signed-byte path converts stored units by approximately 0.01, clamps the blend to −1…1, then rounds and stores hundredths. The unsigned 64-bit path uses separate handling for values with the high bit set; its conversion has not been exhaustively proved for all floating-point inputs.

In the reviewed byte path, endpoint control bit 4 governs contribution: two participating endpoints interpolate, one participating endpoint retains its value with a scaled contribution, and neither participating produces zero contribution metadata. This is more than a storage conversion and does not establish an original flag name.

Three local audits matched 1,138 native instruction observations against current memory, with overlapping regions counted separately. This evidence covers selected dispatch, storage and interpolation paths, not complete sampler bodies. Exceptional values, cross-leaf reconstruction and later blending remain under investigation. No new names or full-behavior completion credit were added.

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

The reviewed alternate scalar writer (`14108f690`) converts retained eight-byte timestamp/value samples into twelve-byte records with control data. It preserves the value bits and normally supplies control word `0x700`; incoming records already carry their own control data. Old-prefix, incoming-range and old-suffix processing follows the traced merge structure, with additional AutoKeyframe boundary-control changes. Both resource roots are finalized and a 72-byte track descriptor is appended.

Native caller flags establish these selected routes for scalar descriptor types 2, 5, 24 and 25:

| Existing samples | Recording mode | Selected writer | Output records |
| --- | --- | --- | --- |
| Eight bytes | Outside AutoKeyframe | `14108af70` | Eight bytes |
| Eight bytes | AutoKeyframe | `14108f690` | Twelve bytes |
| Twelve bytes | Either | `1410859b0` | Twelve bytes |

The table applies to the reviewed ordinary conversion branch with its earlier builder flag clear, consistent descriptor lookups, and descriptor flags matching the generated buffer. A separate per-slot byte also contributes flags; its lifecycle and the earlier special conversion branch remain unproved. The alternate writer reads incoming data at a twelve-byte stride, so the table does not establish that arbitrary mixed-format buffers are safe.

One AutoKeyframe boundary check compares an old stored timestamp with an already rebased incoming timestamp. The old origin adjustment is absent from that particular comparison; whether surrounding state always makes it zero remains unresolved. Empty-input safety, tree ownership and allocation contracts, other dispatcher types, new tracks and runtime playback also remain open. The complete writer body and selected dispatcher/caller regions were checked against current native bytes; not every dispatcher case was semantically reviewed.

The reviewed binary scene-input branch at `140d97090` explicitly enables checksum checkpoints, selects callback `140d91c30`, sets input direction, and passes null external data. That selects the callback's block-descriptor-list input route. Native argument forwarding reaches the object-list bridge (`140dc2a50`) and generic object loader, connecting this setup to the previously traced Animation construction and serialization path.

The object-list bridge transfers the count and objects, checks serializer errors and invokes the checksum helper after the list. A separate optional object marker is distinct from checksum policy. Earlier work identified the block decoder as LZ4; this follow-up establishes the scene input setup and context route rather than claiming the codec was newly identified. Save-side initialization, preservation of policy fields across every intervening helper, the complete outer container and runtime round trips remain unresolved.

These traces add no further names beyond the three above and no whole-behavior or runtime-validation credit. Raw native captures and local audit records remain outside the public repository.

### Recording flags, construction defaults, and serializer selection

The extra per-slot flag used by the recording builder is now tied to the reflected `recording_possession` byte. The reviewed slot initializer clears it, and the corresponding runtime start/stop paths write 1 or 0. Snapshot reset copies the initialized zero value; the copy import was independently bound to `memcpy`. Those values cannot set sample-format bit 2. However, the versioned serializer transfers this field as an unnormalized byte, and complete live-state-to-snapshot propagation remains untraced. Arbitrary restored values are not proven to be Boolean. This narrows the earlier format concern without asserting a universal buffer-format invariant.

The Animation initializer's native stores and registered field offsets establish these values at construction:

| Fields | Initial value |
| --- | --- |
| Playhead, StartTime | 0 |
| EndTime, PlaybackSpeed, Power, AnimStrength | 1 |
| PlaybackMode | LOOP (2) |
| Reverse, Relative | False |
| EaseInStrength, EaseOutStrength, EaseBothStrength | Stored byte 50, interpreted as 0.5 by the reviewed reader |

These are constructor outputs, not a claim about every editor-created or loaded object: later property copies and deserialization can overwrite them. The full 411-byte initializer and selected registration regions and literals were checked against current memory. The constructor does not initialize every byte of object storage.

Scene input also has a format-selection branch. The previously described checksum-enabled binary context is selected when the source record's discriminator is not 99999. Equality instead begins a different stream construction using table `141c37950`. This value is not established as a shipping build number, and the alternate stream grammar was still untraced at that stage; the later alternate-stream findings below narrow this gap.

A separate native output chain, `14039d770` to `140399260`, explicitly selects output mode and callback `140d91c30` with null external data, but disables checksum checkpoints. Thus the callback's presence alone does not determine checksum policy. This chain has not yet been attributed to the main scene-save operation. The follow-up below establishes version-record ownership and the counterpart alternate writer; complete buffer invariants and runtime round trips remain open.

These findings leave the totals at 162 checked names and 1,615 mapped functions. No whole-behavior completion or runtime-validation credit was added.

### Animation initialization contract and serializer helper review

The complete 411-byte body of `InitializeAnimationObjectDefaults` (`14093f9d0`) now has an independently checked static contract. All 53 instructions are accounted for: six global reads, 41 stores touching 408 distinct bytes within a 448-byte object span, and 40 bytes left unchanged. The 16-byte mutable global input remains symbolic. The contract explicitly requires accessible memory, nonoverlap with the source blocks/code/return slot, stable source data and the applicable AVX environment. It covers normal return, not faults, races, full object semantics or in-game behavior.

All four discovered calls clear the 448-byte destination before invoking this initializer. Their continuations overwrite `RAX` before using it. An isolated project trial therefore supported the working opaque-pointer signature `void InitializeAnimationObjectDefaults(void *animation)` with the existing `PS4_SYSV` calling convention. The saved signature was verified after a fresh process reopened the project; all 411 native bytes and four references remained unchanged. This is a supported working signature, not a recovered original declaration; the complete Animation structure remains unresolved.

This separately audited contract adds 411 bytes to the conservative static-coverage measure: **1,495 / 28,940,288 executable bytes (0.0052%)** across three complete function contracts. Name-only changes below add no coverage. Runtime validation remains separate and has not been performed.

| Address | Saved descriptive name | Native role |
| --- | --- | --- |
| `140d91c30` | `ServiceEncodedSerializerBlock` | Services input/output encoded blocks through the selected buffer or external-handle route. |
| `140d91900` | `PrepareEncodedSerializerBlock` | Prepares an encoded block, its descriptor and accounting. |
| `140dc2a50` | `SerializeSceneObjectList` | Transfers the counted object list through the generic object serializer, with status/checkpoint handling. |
| `14039b4a0` | `TransferSerializerByte` | Transfers one raw byte directly or delegates to the general byte-transfer helper; it does not normalize Boolean values. |

These four analyst names preserve their prior prototypes. A hash-verified cold backup preceded the changes. Fresh-reopen checks preserved 2,465 native bytes and all 325 enumerated references for the four names; the complete 9,553-function name inventory and original archive hashes also matched. Reference preservation is not an audit of every caller. There are now **166 checked descriptive names**, including 125 among 1,618 mapped functions; 7,935 functions remain unmapped.

### Version-record ownership and the alternate scene stream

The previously traced output serializer is now tied to a **version-record subpayload**. The producer selects the controller's current element and invokes the serializer for destination record `+0x120` when source `+0xa8` is nonzero; otherwise it clears that 16-byte pair. It checks the returned status and writes discriminator 99999 on its successful path. The downstream consumer `140469a90` pairs this record's leading value with the literal `version_id`; a separate record is paired with `dream_id`. Copy instructions carry the version record's `+0x120` pair into operation context `+0x620`, and `publish_type` supplies a save/publish-preparation connection. The exact subfield meaning, subsequent persistence, and source descriptor's original type name remain unresolved.

The inner subpayload serializer transfers marker `0x53637262` and explicitly disables the legacy checksum checkpoints. That fact belongs to this subpayload. It does not establish the policy or complete format of the main scene stream.

The scene loader's **99999 branch** has now been traced to its actual counterpart writer:

| Route | Native connection | Established behavior |
| --- | --- | --- |
| Alternate input | `140d97090` selects stream table `141c37950`, mode 0, then `140c74040` / `140c74670`. | Descriptor-backed blocks feed the already identified LZ4 decoder, then the stream supplies bytes to the reflected reader. |
| Alternate output | `140d94880` selects table `141c32cb8`, mode 1, then the same setup/engine. | Buffered output is encoded into blocks, given descriptors and handed to backing storage. |
| Reflected content | Output engine reaches `140116eb0`; input reaches `1415fea20`. | Selected output regions emit initial marker bytes, seven-bit continuation integers and descriptor-backed metadata/byte strings. The complete field grammar is still open. |
| Visitor callbacks | Two reviewed callbacks per visitor table reach stream method `+0x18`. | Input returns zero; output may request a block boundary based on span and hash conditions. The output events were still untraced at that stage; the later reflected-writer findings below identify two array/container paths. Input-event timing remains open. |

The nearby table `141c37930` is a separate reference collector. It gathers/deduplicates 16-byte reference entries; it is not the output byte-stream implementation. This distinction prevents mixing the reference list with serialized scene content.

Two native counter details remain important for future validation: one output multi-copy loop adds the original request length each iteration, and one input consume method may return the requested amount after an incomplete consume. Neither observation is a reproduced runtime defect; callers and interface contracts must be established first. The exact encoder implementation, full reader/writer grammar, descriptor algorithm, backing-store guarantees and runtime round trip remain open.

Independent naming review also corrected the object-list marker description: its low-word error check occurs **before** the optional sequence-marker transfer. The sequence counter increments afterward even if the fallback transfer sets an error, and this body does not compare the transferred marker for equality.

These bounded ownership and format findings add no complete-function coverage. Only the separately audited Animation initializer contract contributes the 411 new bytes reported above.

### Descriptor block reading, flushing and return values

Two more shared saving/loading helpers now have evidence-supported descriptive names and working signatures:

| Address | Name | Observed interface |
| --- | --- | --- |
| `140c73ef0` | `LoadDescriptorInputBlock` | Stream pointer, two 64-bit descriptor halves; Boolean result in `AL`. |
| `140c737c0` | `FlushDescriptorOutputBlock` | Stream pointer; 64-bit available-capacity result in `RAX`. |

The complete native bodies—305 instructions / 1,185 bytes—were read and matched to the current program. All three recorded reader calls load a 16-byte descriptor from the input list and immediately test `AL`. The body sets that low byte to zero or one; its other return bits are not consistently normalized. This supports a working Boolean return in the decompiler. The original source declaration and descriptor structure remain unrecovered, so the two observed descriptor halves and an opaque stream pointer are retained.

The reader acquires the descriptor-backed resource, invokes the already identified LZ4 decoder, and on positive output installs the decoded buffer's cursor and end. It updates separate encoded and decoded byte counters. Missing resources or nonpositive decoding record errors and clear cursor/end, with local resource ownership released afterward. Valid pointer extents, low-32-bit length arithmetic, lifetimes and decoder contracts still require validation.

The writer encodes pending input, builds a descriptor, attempts to append it and hands the encoded payload to backing storage. A failed descriptor-vector allocation can skip append while continuing to the handoff; encoded-byte accounting happens before storage success. These are conditional native findings, not proof that a save succeeds or a reproduced runtime defect.

**The writer's return is capacity, not a success flag.** Prior error or empty input returns zero. After a nonempty attempted flush, the reviewed paths reset the buffer and return its capacity even when they recorded an allocation, encoding or storage error. The buffered caller tests that capacity and can copy additional input after such an error before reaching another boundary. Complete enclosing error propagation, failure reachability and runtime effects remain open.

Both working signatures were tested in an isolated project copy before promotion. Only these two function signatures/names changed. A hash-verified cold backup and fresh-process reopening confirmed all 1,185 bytes and seven recorded references unchanged, plus the complete function-name inventory and original archives. The signatures express the checked machine interface; they are not recovered original declarations.

Totals are now **168 checked descriptive names**, with **127 checked among 1,620 mapped functions** and **7,933 functions still unmapped**. No new complete-function coverage was added: the conservative audited-byte measure remains **1,495 / 28,940,288 (about 0.0052%)**. Linked dependency contracts, complete scene-field grammar and runtime save/load validation remain unfinished.

### Reflected value encodings and array boundary events

Four output helpers now have saved descriptive names: `WriteReflectedPrimitiveValue` (`141603480`), `ResolveReflectedTypeId` (`141603710`), `WriteReflectedValue` (`141603860`), and `WriteReflectedFieldValue` (`141603fe0`). Their complete owned bodies total **1,068 instructions / 3,900 bytes**. The ten unowned bytes inside the value writer's address span are excluded from that total.

The primitive dispatch table establishes these payload operations:

| Descriptor kind | Payload encoding |
| --- | --- |
| 0 | No payload bytes |
| 1 | One raw byte, without Boolean normalization |
| 2–5 | Unsigned 8/16/32/64-bit value, using seven-bit groups with a continuation bit |
| 6–9 | Signed 8/16/32/64-bit value, sign-extended and transformed with `(x << 1) XOR (x >> 63)` before the same compact encoding |
| 10 | Four raw bytes; previously established float registration binds this kind to scalar float |
| 11 | Eight raw bytes; the subsequent reader review below establishes float64 interpretation |

These numbers are descriptor kinds used to choose an encoding. They are not assumed to be literal type tags in a saved file. The prior float-field registration was checked against current native stores, its `float` literal and four-byte stride; that existing result adds no repeat completion credit.

The primitive writer returns low-byte status zero for supported kinds and seven for an unsupported kind. Upper return bits are not consistently normalized on the unsupported path. Both recorded callers establish the stream/type-code/value register interface, so an isolated trial supported the working signature `uchar WriteReflectedPrimitiveValue(void *stream, uint type_code, void *value)`. The other three functions retain their previous prototypes. As already established for float output, supported primitive writes discard the stream's reported byte count; the extended dispatch review confirms the same local behavior across the other emitting cases. Complete enclosing error propagation remains unresolved.

The value writer handles custom callbacks, primitive values, filtered composite fields and object-reference IDs. The field writer delegates single fields and traverses fixed arrays or callback-provided containers. Fixed arrays use their descriptor count directly unless the optional count flag is set; that flag emits a selected count prefix after resolving/clamping its associated integer field. Container callbacks and mask meanings still need further tracing.

The output visitor callbacks previously left unexplained are now bound to concrete paths:

| Visitor slot | Verified writer event | Result |
| --- | --- | --- |
| `+0x38` | After the reviewed fixed-array traversal finishes, including zero-count arrays; an element error skips it | If its stream is present, calls the output boundary-request method with mode 1 |
| `+0x48` | After the reviewed nonempty contiguous container traversal with valid data; its error and iterator paths skip it | If its stream is present, calls the same boundary-request method with mode 1 |

Thus these callbacks request possible block boundaries at those array/container traversal points. They do not establish per-field checksum words or callbacks after every field. Complete input-event timing, the reader's conversion grammar, custom callbacks, reference-table invariants and a runtime save/load round trip remain unfinished.

A verified cold backup preceded promotion. The isolated trial and fresh-process reopening preserved all **3,900 owned instruction bytes and 13 recorded references**; the complete function-name inventory and original archives also matched. Totals are now **172 checked names**, **1,624 mapped functions**, and **7,929 unmapped functions**. The conservative audited-byte coverage remains **1,495 / 28,940,288 (about 0.0052%)**; no new complete-function coverage or runtime validation is claimed for these findings.

### Reflected primitive reading and conversion

Saved three more descriptive names: `ReadReflectedPrimitiveValues` (`1416003a0`), `ReadReflectedPairEntries` (`1416019f0`), and `ReadReflectedTypedValue` (`141602aa0`). Their complete owned bodies total **919 instructions / 3,565 bytes**. The primitive reader now has a tested six-argument working signature with opaque context/type/destination pointers, a source category, stride and count, and low-byte status. The pair and typed-entry helpers retain their previous prototypes.

The source category and destination kind serve different purposes:

| Generic source category | Verified reader path |
| --- | --- |
| 1 | Reads compact unsigned integers and checks destination bounds; destination kind 1 instead uses the Boolean bulk path below |
| 2 | Reads the compact integer, reverses the signed transform, then checks signed destination bounds |
| 3 | Reads binary32 values; matching float kind 10 with stride 4 uses a checked bulk read, otherwise scalar conversions |
| 4 | Reads binary64 values; matching kind 11 with stride 8 uses a checked bulk read, otherwise scalar conversions |
| 0 or 5 | Returns low-byte status 2 on the generic path |
| Above 5 | Returns low-byte status 7 on the generic path |

A custom descriptor reader overrides this generic dispatch. Its callbacks and optional interface processing remain dependencies. Source category numbers are not interchangeable with the output writer's destination-kind numbers.

The captured range tables establish the integer limits used before ordinary conversion: unsigned input must fit the configured maximum, and signed input must fit the configured minimum/maximum. Negative signed integer values cannot enter an unsigned destination through this path. The reader reports short reads with low-byte status 1 and range failures with status 2. It may have written earlier elements before a later failure; no transactional rollback is established.

The native conversion branches treat destination kind 11 as **64-bit floating point**, closing the writer-only pass's raw-eight-byte type question. Integer-to-float, float widening/narrowing and truncating float-to-integer paths are visible. Numerical models for the unsigned-64-to-float32 sticky-half algorithm and unsigned-64-to-float64 split algorithm matched **3,565 deterministic boundary/random cases** under round-to-nearest ties-to-even. These models do not execute the target instructions or establish the game's MXCSR rounding/exception state. NaNs, infinities, out-of-range float casts, traps and all floating side effects still need further validation.

For destination kind 1 with source category 1, the reader consumes `count` contiguous bytes, checks the returned count and converts every nonzero byte to one. Scalar, 16-byte and 128-byte normalization paths agree with that operation. This path does not check for stride 1 or honor an arbitrary larger stride; caller storage requirements remain important. Float/double bulk paths explicitly check their expected strides. Count-shift overflow and complete buffer/lifetime guarantees remain open.

Malformed integer framing remains an explicit gap. The observed varint loops continue until the continuation bit clears and do not reject the eleventh byte locally. They retain only the first ten bytes, while reconstruction uses the consumed count. The typed-entry helper has the same pattern for schema IDs. Caller/framing constraints and actual effects of overlong input are not validated; this is a conditional static observation, not a reproduced runtime defect.

The pair helper requires two source and two destination field records, obtains storage through an iterator and dispatches each side through primitive, composite or the already named object-reference reader. The typed-entry helper uses an expected primitive class directly or validates a compact composite schema ID, table entry and stored ID before delegation. Its 200 recorded references are preserved; they have not all been semantically audited. Original container classes, iterator ownership and complete schema construction remain unresolved.

A hash-verified cold backup and isolated signature trial preceded promotion. Fresh-process reopening preserved all **3,565 owned instruction bytes and 207 recorded references**, the complete function-name inventory and original archives. Totals are now **175 checked names**, **1,627 mapped functions**, and **7,926 unmapped functions**. Audited-byte coverage remains **1,495 / 28,940,288 (about 0.0052%)**. These findings add no complete-function coverage or runtime scene-round-trip claim.

### Reflected field loading and unknown-data consumption

Seven descriptive names now cover composite field reads, field-load plans, field-element and primitive/composite skipping, and two registered callback phases. All existing prototypes are preserved. Fresh reopening verifies the complete function inventory, unchanged native bytes and references, and unchanged original archives.

The load-plan builder matches saved field identifiers to current descriptor records, including inherited offsets and supplementary objects. It caches auxiliary instances and prepares two reverse-traversed callback lists. Related target descriptors can reuse a prior plan; this is observed cache behavior, not proof of general migration correctness.

The composite reader loads the portion fitting destination storage and consumes surplus or unmapped source elements afterward. Its array callbacks occur after the mapped portion but before surplus consumption. The standalone composite skipper instead runs its after-array callback after skipping the whole field. Reference skipping validates represented object IDs rather than creating new objects.

The primitive skip dispatch table was captured directly from the executable: categories1/2 consume compact integers,3/4 skip four/eight bytes per element, and5 consumes length-prefixed payloads. Category0 returns status2; categories above5 return7. These are source categories, not output destination-kind numbers.

Remaining gaps include indirect hook and stream contracts, allocation failure, related-type cache invariants, and malformed input. The composite skipper narrows its field-element count to32bits; not every count-decoding path has the same explicit bound check. A trailing-chunk path reaches zero status after a short header or payload read. Caller constraints and actual runtime consequences remain unproved; these are static observations, not reproduced defects.

Totals are182 checked names,1,634 mapped functions and7,919 unmapped functions. Audited-byte coverage remains1,495 /28,940,288 (about0.0052%); these role reviews do not add whole-function completion or runtime scene-round-trip credit.

### Composite-reader working signature

`ReadReflectedCompositeFields` now has a verified working signature returning an unsigned byte and accepting four opaque pointers: context, source schema, destination type descriptor and destination storage. The native body and all six recorded call locations support RDI/RSI/RDX/RCX arguments and AL status. Upper return-register bits are not consistently normalized.

An isolated project trial and the promoted project both decompiled the loader and its three containing caller functions successfully. Fresh reopening preserved the signature, native instructions and recorded references. The complete function-name inventory and original archive hashes also passed verification. This improves call reconstruction; it does not recover original declarations, prove undiscovered indirect callers, validate runtime behavior or increase audited-byte coverage. Totals remain 182 checked names and 1,634 mapped functions.

### Inline chunk stream callbacks

Defined and named three previously unrecognized functions: `ReadReflectedChunkSpans`, `SkipReflectedChunkBytes`, and `ForwardReflectedChunkSkip`. Their130 instructions occupy489 bytes, excluding trailing alignment. Native scene-reader initialization installs their table at context+0xe8; the table points to the reviewed entry addresses.

The span reader fills an array of destination-pointer/length spans from chunk-buffered data. A null destination consumes bytes without copying. Refills read a16-bit header, treat reserved values as markers, and load ordinary payload lengths. Short underlying reads or an empty payload return the accumulated byte count. The two skip adapters route a null-destination span through this same reader, retaining the actual-consumed-count result.

The earlier hook-cleanup helper reads another header/payload before restoring state. Its caller preserves the hook's status, while cleanup ignores its own payload-read count. This differs from callers that explicitly compare the stream callback's returned byte count. Full framing, caller invariants and malformed-input runtime effects remain open.

An isolated function-definition trial checked ownership, instruction boundaries and decompilation. Promotion followed a hash-verified cold backup. Fresh reopening preserved489 native bytes and3 recorded table references, all existing names, and original archive hashes. There are now185 checked names across9,556 discovered functions;1,637 are mapped and7,919 remain unmapped. Prototypes remain provisional. Audited-byte coverage is unchanged at about0.0052%; no runtime validation or original-source recovery is claimed.

### Schema metadata and object population

Five further descriptive names cover hook-scope cleanup, source-schema allocation, raw name-byte reading, and compact unsigned32/64-bit readers. All previous prototypes are preserved. Full native bodies and caller relationships support these roles; fresh reopening, the complete inventory and original archives were verified.

The name reader produces a raw begin/end byte span with no enforced terminator or encoding. The32-bit integer reader rejects decoded values above its range; its short-read code is1, while the64-bit reader uses2. Overlong continuation framing, allocation and ownership contracts remain unresolved.

The outer stream reader has a five-entry dispatch table. Its object-payload handler resolves a source schema and an already registered destination object, then delegates to primitive/composite readers or consumes the payload through skip helpers. Reference loading separately creates/registers missing objects; it does not populate their fields in that helper. Pointer stores may precede later marker-validation failure, so rollback is not established.

Schema fields derive identifiers from saved name bytes, carry type/flag/mask/count data and child schema pointers, and undergo normalization before destination mapping. The schema allocator always creates a new entry and writes its ID slot; it does not return an existing entry. Missing-entry placeholders are observed, but repeated IDs, replacement and child-pointer continuity remain open. No general forward/cyclic-schema correctness is claimed. A special field identifier and alternate field list still need semantic binding.

The outer reader also invokes descriptor callbacks on completion and several error paths. These are not yet established as destructors or success-only finalizers. A child status9 receives special zero conversion; its origin and meaning remain open.

Totals are190 checked names across9,556 functions,1,642 mapped and7,914 unmapped. Audited-byte coverage remains about0.0052%. These findings do not establish a complete scene decoder, recovered original source or runtime validation.

### Outer reflected record reader named

`ReadReflectedStreamRecords` now names the complete 1,157-instruction outer reader. Native selectors route to schema definitions, object payloads, parsing-state updates and terminal handling. The object path populates registered destinations or skips their source payloads. The parsing-state handler stores a checked 32-bit value; its original meaning is still unbound.

Full-body role review supports this descriptive name, while schema replacement, special-field initialization, factories, callback ownership, status9, malformed framing and a working runtime round trip remain open. Fresh reopening preserved the existing prototype, native bytes and references; full inventory and archive checks passed. Totals: 191 checked names, 1,643 mapped functions and 7,913 unmapped. Audited-byte coverage is unchanged.

### Reflected read-resource teardown

`ReleaseReflectedReadContextResources` and `ReleaseReflectedSourceSchemaResources` now name two fully reviewed cleanup roles, covering 274 native instructions. Context teardown may drain unread records in skip mode before terminal processing. It conditionally releases an owned stream, tracked raw-name allocations, current schema entries and table storage. Schema teardown separately destroys auxiliary instances and hook callables and releases its vectors; its caller releases the enclosing allocation.

Descriptor callbacks at outer-reader exit remain distinct from auxiliary-instance destruction. Only schema pointers currently in the table are visited here, so overwritten-slot ownership remains unresolved. Partial contexts, repeated teardown, indirect callback effects and allocator guarantees need more analysis. No runtime or audited-byte credit is added.

A hash-verified cold backup preceded naming. Fresh reopening preserved native bytes, types, references, full function inventory and original archives. Totals: 193 checked names, 1,645 mapped functions and 7,911 unmapped.

### Name identifier hash

`HashNameBytes32` names the shared 32-bit identifier helper used for reflected field names and other name/tag lookups. The reviewed model combines signed-byte polynomial-27 sums for two space-padded 32-byte blocks, multiplying the second by 0xdeadbeef, modulo 2^32. Input after the first 64 bytes does not enter the reviewed model. Hash matches do not uniquely recover names.

970 deterministic cases cover every length 0–96 and signed high-byte inputs, matching captured-instruction interpretation against an independent arithmetic model. They exercise 1,103 of 1,104 instructions; the remaining branch lies outside the reviewed valid-length partition. This is not target execution or complete ABI/invalid-length validation.

Fresh reopening preserved the name, existing prototype, native bytes and references; full inventory and archive checks passed. Totals: 194 checked names, 1,646 mapped functions and 7,910 unmapped. Audited-byte coverage remains unchanged.

### Reflected helper signatures verified

Six existing helpers now have native-supported working signatures. The raw-name reader takes context and output span pointers and returns byte status. The32-bit compact reader takes a stream and uint output pointer with byte status; the64-bit reader takes a stream and64-bit output pointer with32-bit status. The decoded value is stored through the output pointer rather than returned as status.

The chunk-span reader takes stream, span-begin and span-end pointers and returns a64-bit consumed-byte count. Both skip adapters take stream and64-bit count and preserve that full byte-count result. Opaque pointers avoid inventing original class declarations.

An isolated trial and promoted project decompiled all six helpers plus the outer record reader, composite loader and object-reference reader. Exact parameter/return register storage was checked. Fresh reopening preserved native bytes and references, and full inventory/archive checks passed. Virtual replacement tables, undiscovered callers and runtime behavior remain open. Counts remain194 checked names and1,646 mapped functions; audited-byte coverage is unchanged.

### Schema collection and object-record writing named

Saved `CollectReflectedSchemaDependencies` and `WriteReflectedObjectRecords` after reviewing their complete 939 native instructions. The collector registers IDs before dependency traversal but appends descriptors after recursion. The writer consumes that list forward, so ordinary acyclic dependencies precede their parent even though assigned IDs need not ascend. Recursive schemas, lookup internals and placeholder continuity remain open.

The writer emits schema headers, raw names, field metadata and object payload records. Observed field inclusion/exclusion masks match between collection and emission. Named-alternative metadata binds to the reader’s category-1/flag-0x20 list path. Original source-type semantics are not inferred solely from that shape. Stream writes generally check returned lengths; allocation failures, callbacks and full framing still require analysis.

Fresh reopening preserved both names, previous types, native bytes and references; full inventory and original archives passed checks. Totals: 196 checked names across 9,556 functions, 1,648 mapped and 7,908 unmapped. No runtime round trip or audited-byte credit was added.

### Descriptor map roles named

Saved `FindReflectedDescriptorSlot`, `EnsureReflectedDescriptorMapCapacity`, and `InsertReflectedDescriptorId` after reviewing all 361 native instructions. Lookup matches exact descriptor pointers and returns a map/index result with a capacity miss sentinel. Growth chooses power-of-two storage with minimum capacity 16 and reinserts old entries. Insertion updates existing IDs or displaces entries according to the same probe-distance rule used by lookup; the incoming pair can change during displacement.

The collector registers a new descriptor before recursing. Repeated lookup of that same pointer can therefore suppress repeated traversal. This establishes the observed collection mechanism, not complete recursive-schema correctness in the reader. Zero keys, invalid/full tables, overflow, allocation failures and full ownership contracts remain open.

Fresh reopening preserved names, previous types, native bytes and references; full inventory and original archives passed verification. Totals: 199 checked names, 1,651 mapped functions and 7,905 unmapped. No runtime or audited-byte credit was added.

### Descriptor map instruction emulation

Captured x86-64 lookup and insertion bytes ran under Unicorn 2.1.2 in isolated synthetic memory. Nine scenarios at capacities 16, 32 and 64 produced 4,629 native-function calls matching a reference dictionary, including deliberate collisions, wraparound and duplicate-ID updates. Stack balance and callee-saved registers were checked. Eight insertion cases changed the mutable incoming pair, confirming the observed displacement side effect.

The captured growth routine then ran with explicit successful allocation/free stubs. Across 300 inserted entries and 300 growth calls, capacities progressed from 16 to 1,024. All registered IDs survived 6,621 lookup checks; seven allocations and six old-allocation releases were observed. Stack and callee-saved register checks also passed.

These execute the captured instruction bytes rather than merely reimplementing the table algorithm, but still use synthetic valid tables and controlled dependencies. Real allocators, allocation failures, overflow, invalid/full tables, complete formal correctness and the running Dreams game remain unverified. Counts and audited-byte coverage are unchanged.

### Compact and chunk-reader instruction emulation

Captured compact unsigned32/64-bit reader instructions passed 284 value/range cases and 2,568 truncated-input cases with controlled byte-span stream callbacks. Boundary values through unsigned64 limits were checked. Failure paths in those cases preserved output storage, stack balance and callee-saved registers; the32-bit reader's short-read status1 and64-bit reader's status2 were confirmed.

The compact readers were then connected to the captured native chunk-span reader. Across chunk widths1,2,3 and10, with and without interspersed reserved markers, 512 value/range/chunk cases and14 short-input/marker cases passed. Underlying reads and memory copying remained explicit stubs.

Direct chunk-span and skip-adapter emulation passed728 cases, including248 partial-count cases. Checks covered multiple spans, zero lengths, null destinations, actual-consumed-byte results and untouched destination tails, plus stack/register preservation.

These tests execute captured instruction bytes in synthetic memory. They do not run Dreams or decode real scene files. Real stream/memory-copy implementations, overlapping buffers, overlarge counts, overlong compact encodings, malformed marker runs and full caller contracts remain open. Counts and audited-byte coverage are unchanged.

### Boolean primitive conversion and short reads

A fresh check matched the complete 623-instruction primitive reader and its Boolean vector constants to the expected executable. Static control flow shows zero/nonzero normalization through 128-byte blocks, 16-byte blocks, and a scalar tail.

For counts 0 through 15, 48 complete-read cases and 360 short-read cases passed with captured native instructions and a controlled stream callback. Complete reads convert zero to 0 and nonzero to 1. Short reads return status 1 before normalization: the copied prefix remains raw and the untouched destination tail retains its prior contents. This describes partial-write behavior, not a demonstrated game defect.

SIMD execution remains unverified. A minimal captured-instruction reproducer disagrees with explicit-source compare semantics under both Unicorn 2.1.2 and 2.1.4. Passing scalar checks do not validate vector paths. Dreams itself was not run; names and audited-byte coverage are unchanged.

### Reflected array and container event contracts

The complete 352-instruction field writer was reviewed against live memory, and the reader's corresponding event conditions were rechecked. Array callbacks bracket successful element writes, including an empty array. The contiguous-container path writes its compact count first, then obtains storage; zero count or null storage skips its callback pair. An absent count callback also returns without that pair. A separate pair-iterator route uses recursive pair-field writes and iterator cleanup.

Captured field-writer instructions passed 24 array and 36 contiguous-container orchestration cases with controlled dependencies. Checks covered empty values, element errors, short count writes, missing count callbacks and null storage. Checked element errors propagate and suppress the closing notification. Callback return values do not override the result. These tests stub element serialization and stream writes; they do not verify serialized scene contents.

On input, the closing array/container event occurs after mapped element reads and before surplus saved elements are skipped. The concrete scene-input observer's primitive opening/closing methods are no-ops. Its array/container closing methods forward to the supplied stream's control method; the identified input-stream implementation simply returns zero. Other supplied stream implementations remain separate dependencies.

No new names, audited-byte credit or game-runtime verification are claimed.

### Connected primitive writer and reader validation

Captured native primitive-writer and primitive-reader instructions were connected through controlled in-memory stream callbacks. All 1,199 value cases passed: unsigned compact integer encodings, signed zigzag encodings, all 256 raw Boolean input bytes, and selected matching-width floating-point bit patterns. Boolean writes preserve the raw byte while reads normalize zero/nonzero. Matching-width float checks preserved signed-zero, infinity and selected quiet/signaling NaN payload bits; this does not validate floating arithmetic or conversions.

Another 1,871 short-write cases confirmed that the primitive writer returns success even when the stream accepts fewer bytes, including zero. Its native code discards the returned count. This is a function-level contract observation; actual stream error flags and caller-level failure handling remain unresolved, so it is not a demonstrated game defect. Empty type and unsupported type behavior were also checked.

These are connected native value tests in synthetic memory, not a complete scene-file round trip or running-game validation. Custom serializers, scene framing, compression and storage remain separate dependencies. Names and audited-byte coverage are unchanged.

### Connected composite fields, schema mismatches and optional masks

The captured native field/value/primitive writer was connected to the composite reader and primitive/skip helpers using controlled memory streams and prebuilt matching schemas. All 83 matching-array cases passed, including packed and padded layouts. Another 62 zero-accepting-stream cases confirmed that the field/value writer chain does not detect that form of short write.

For canonical Boolean storage and the tested integer/float values, 430 schema-mismatch and unmapped-field cases preserved the expected destination prefix, padding and untouched tail. Surplus elements were consumed before a following scalar field, whose value confirmed stream alignment. Another 980 truncation checks returned errors without populating that following field.

Optional-mask checks passed 96 presence/mapping cases, 35 truncated-header cases and one unsupported-destination case. Zero per-field masks mean unconditional fields; nonzero masks require an intersecting bit. Omitted fields consume no value bytes and preserve storage. Checked truncated mask headers return status 2 before field writes; a destination without mask support returns status 7 before consuming the header.

A separate native reproducer retains a limit deliberately excluded from the canonical-Boolean mismatch cases: raw noncanonical Boolean bytes can contain compact-integer continuation bits, causing the skipped-field path to consume bytes from the following field. Real game reachability is unproven; this is not classified as a demonstrated game defect.

These tests supply schemas and load plans synthetically. Actual root schema parsing/matching, mask production, object references, hooks, nonempty postload callbacks, compression and storage are not validated. Boolean SIMD execution remains unproven. No real scene-file round trip, running-game verification or completion credit is claimed.

### Native field matching connected to decoding

The native field lookup passed 84 descriptor/alias/inheritance cases. It scans field records from a rotating cached index, accepts alias identifiers, and accumulates parent offsets. Primary hits advance the cursor; alias hits leave it unchanged. The native load-plan builder then mapped 12 primary/alias identifiers and left two unknown identifiers unmapped in a synthetic three-level descriptor hierarchy.

The composite reader was connected to that actual native load-plan builder and lookup, removing prefilled destination mappings from the test. All 1,548 connected writer/mapping/reader cases passed across primary IDs, aliases, unknown fields, two initial lookup cursor positions and destination capacities of 0, 2 and 16. Unknown and surplus values were skipped before the following field, whose expected value confirmed alignment. Element bytes, padding and untouched tails matched expectations.

Source schemas and destination descriptors are still synthetic. Root schema parsing, supplementary types, allocator paths, nonempty read/postload callbacks, object references, compression/storage and running-game behavior remain unverified. Boolean fixtures are canonical and avoid the unverified SIMD path. No new names or completion credit are claimed.

### Concrete buffered output failure contract

The captured primitive encoder was connected to the concrete buffered output-write method, with controlled memory-copy and block-flush dependencies. All 252 cases passed, including 52 reached flush-failure cases. The buffered method refuses writes with a preexisting error, stops copying on a zero flush result, and returns the copied prefix length. The primitive encoder still reports success in these checked error cases because it discards that count. The stream retains its error for possible higher-level handling.

Selected save return paths were checked against live memory. Serializer success combines its context error word and status byte. The concrete stream's error storage is separate in the captured caller. The selected common cleanup performs a final flush without directly replacing the saved return code with its result. This bounded trace does not prove that every helper omits propagation.

Actual compression/storage failure execution, propagation through other helpers and real save-operation reachability remain unresolved. No game defect, whole-save validation or completion credit is claimed.

### Source-schema predicates defined

Defined `HasReflectedSourceField` and `HasAuxiliaryMappedReflectedSourceField` from source-schema vtable entries. The first tests for a saved field identifier. The second requires the first matching field to have both a destination mapping and an auxiliary base. Their 45 native instructions occupy 152 bytes, including internal alignment and excluding trailing padding. Combined synthetic instruction checks passed 504 empty-list, present/absent ID and pointer-state cases.

Both now have working PS4_SYSV signatures with an opaque schema pointer, unsigned field ID and byte return. A hash-verified cold backup and isolated decompilation trial preceded promotion. Fresh reopening verified both definitions/signatures, unchanged native bytes, all 9,558 inventory entries and original archives. Totals: 201 checked names, 1,653 mapped functions and 7,905 unmapped. Duplicate-ID invariants, all caller usage and running-game behavior remain open. Audited-byte coverage is unchanged.

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

### Sculpt worker transformed bounds

840 no-body and2520 body-associated cases execute the original bounds-active worker path. Independent eight-corner quaternion/scale/translation calculations match XYZ bound envelopes across selected identity/90/180-degree rotations, positive/zero/negative scales, translations and zero/skewed resource axes. Maximum absolute differences are0.00000143 and0.00000197 respectively, within the stated0.00002 tolerance. Flags, identifiers, inclusion/body-index bookkeeping and counters are checked exactly; object/resource bytes remain unchanged.

The body path also executes the original flag helper and expands bounds by a stored body vector times the original0.13333334028720856 factor. The vector’s gameplay meaning and units remain unresolved; velocity is a lead rather than an adopted field name. The two output SIMD fourth lanes are not independently modeled, and nonfinite/unnormalized inputs, concurrent scheduling and complete game consumers remain unverified. No new names or completion credit;285 names remain checked.

### Saved sculpt bounds and wake-state worker

Defined CalculateSculptBoundsAndWakeBodiesJob with its complete1732-byte body and opaque job-context pointer input. The original job label, native dispatcher and4128 scoped worker cases support its bound-calculation, flag, notification and wake-state roles. Cold backup, isolated trial, promotion and independent reopening verify the saved definition, unchanged existing functions/instructions and original archives.

Recorded under physics simulation because it writes body wake-state flags and prepares sculpt bounds for spatial-tree construction. XYZ math is tolerance-checked; fourth SIMD lanes, body-vector meaning/units, nonfinite/unnormalized inputs, concurrency and actual gameplay wake effects remain unresolved. Totals:286 checked names among9,577 discovered functions;1,727 mapped and7,850 unmapped. No whole-subsystem completion claim.

### Saved spatial-tree query helper names

Applied CollectBvhLeavesIntersectingSegment and CollectBvhLeavesOverlappingBounds after reviewing all154 original instructions and running4,200 controlled native cases. Both traverse the sculpt bounding-volume tree, filter node flags and return a bounded list of leaf indices. Callers convert these indices to object identifiers. The segment helper checks the interval from0 to1; the overlap helper compares XYZ bounds and masks the fourth lane.

Tests check exact traversal order, output pointers, zero/small/full capacities, flag masks, untouched inputs and guards, plus two empty-root cases. They use finite synthetic trees and nonzero directions. The segment expansion constant was captured from the original executable file; runtime initialization remains unresolved. Exact SIMD signatures and complete caller behavior remain open, so existing signatures were retained. Backup, isolated trial and independent reopening verify the names and unchanged original archives.

Totals:288 checked descriptive names among9,577 discovered functions;1,729 mapped and7,848 unmapped. This is helper-level evidence, not a whole-game completion percentage or real-game validation.

### Saved region-query enqueue name

Applied EnqueueRegionQuery after reviewing all187 original instructions and running288 controlled native cases. It appends a112-byte record, returns a packed handle combining generation, a marker, phase bit and queue index, and rejects requests at capacity256 with an overflow flag. The connected consumer traverses the sculpt BVH before region sampling/refinement.

Tests cover192 accepted and96 rejected requests with exact handle/record/padding checks, independent local-centre and extent math, complete state-allocation preservation and unchanged inputs. Fixtures use cardinal unit rotations and positive power-of-two scales. The import loader NID and local libc symbol identify __isinff; these tests execute its original instructions through the retained original thunk. Arbitrary rotations, complete consumer semantics, concurrency and gameplay integration remain open. Existing SIMD/stack signature retained.

Cold backup, isolated trial and independent reopening verify the saved name and unchanged original archives. Totals:289 checked names among9,577 discovered functions;1,730 mapped and7,847 unmapped. No whole-subsystem completion claim.

### Spatial-query working types

Recovered explicit register/stack signatures for the two BVH query helpers and EnqueueRegionQuery. Both collectors return the output-end pointer in RAX, receive the root as16 bits in SI, and read two16-byte SIMD inputs in XMM0/XMM1. The enqueue function returns its32-bit packed handle in EAX, reads six SIMD inputs in XMM0..XMM5, and receives a second opaque 64-bit value at incoming stack offset8. Its former local_res8 was the incoming argument and is now represented as a parameter.

The working types expose the32-byte BVH node and6-byte query-mask record. They preserve unknown state and opaque values. Cold backup, isolated trial, promotion and independent reopening verify exactly three signature changes and unchanged original instructions/archives; both large query consumers still decompile. Displayed argument order and record names are analyst representations, not original C++ declarations. Existing controlled native evidence remains scoped; there is no new gameplay validation or name-count increase. Total stays289 checked names.

### Saved phase-filtered region-query processor

Applied ProcessQueuedRegionQueriesForPhase with an opaque game-context pointer and phase-byte input after reviewing all1,261 original instructions. The processor connects queued requests to sculpt BVH overlap candidates, GPU bootstrap/field sampling, ten refinement iterations and output copy, then appends positive weights/object identifiers and records each request result span. Original RegionQuery labels identify the GPU stages; subordinate shader math remains unresolved.

360 controlled native cases validate empty requests, empty trees, phase selection, selected null/unsupported candidates and newly initialized result headers while checking complete state/game preservation. The byte-fill import is explicitly modeled. These tests do not execute sculpt GPU work, positive result delivery, callbacks, actor-list paths or saturation; real-game behavior and concurrency remain open. Cold backup, isolated trial and independent reopening verify the saved name/signature and unchanged original archives.

Totals:290 checked descriptive names among9,577 discovered functions;1,731 mapped and7,846 unmapped. This broad processor role does not mean every called shader or the subsystem is understood.

### Positive Sprite region-query results

Validated the processor direct result path with408 additional original-instruction cases:192 single-leaf cases and216 cases using trees of1,3 or33 leaves. Original enum instructions independently identify object kind17 as Sprite. Admitted Sprite candidates append weight1.0 and their mapped object identifiers when the query auxiliary bit2 is set and phase/masks match. Tests check exact entry order, per-query count/start spans, total append count and complete state/game preservation.

The candidate scratch list holds1,024 entries shared across matching requests. The global result buffer stops appending at16,383 entries; subsequent direct-path requests receive empty spans. This establishes the selected direct Sprite path, not GPU sculpt output or exact geometry beyond BVH admission. Byte-fill import modeling, synthetic scenes, callbacks, actor-list fields, GPU saturation and in-game/concurrent validation remain explicit limits. The saved processor comment and current evidence were updated; checked-name total remains290.

### Saved CPU region-shape weight evaluator

Applied EvaluateRegionShapeWeight and recovered its float return in XMM0, shape byte in DIL, five16-byte SIMD inputs and two16-byte incoming stack transform containers. The connected region processor consumes its positive output as a query weight. All686 original instruction spans match the executable; working types expose storage without claiming original C++ declarations or source argument order.

1,833 controlled original-instruction cases validate selected identity/uniform-axis mode0/4 radial falloff, mode1 box-shell falloff and empty/constant/invalid guards. Independent reference error stays below0.00000017. The original box-intersection callee executes; mapped cylinder/cone callees are not exercised with nonempty geometry. General rotations, nonuniform extents, full shape enum, mode5 gameplay meaning and real-game/GPU behavior remain unresolved. Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature; connected processor still decompiles.

Totals:291 checked descriptive names among9,577 discovered functions;1,732 mapped and7,845 unmapped. Selected weight cases do not establish complete geometry or subsystem understanding.

### Transformed region-weight evidence and enum lead

1,350 additional original-instruction cases validate radial modes0/4 and box mode1 with randomized translations, unit rotations and positive uniform scales. Matching transform containers and uniform inner/outer extent triples remain explicit fixture limits. Independent references use actual float32 inputs; maximum error is below0.0000143. No imports are modeled, and inputs remain unchanged.

The original EGadgetZoneType registration declares0 Sphere,1 Box,2 Cylinder,3 Cone,4 Ellipsoid and5 EntireLevel. Its descriptor/value bodies match original executable bytes. These labels are consistent with the weight modes, but the direct property-field-to-evaluator trace remains open. Exploratory cylinder/cone axis probes are retained locally and provide no geometric validation credit. Nonuniform extents, unmatched transforms, nonempty modes2/3 and gameplay/GPU validation remain unresolved. The saved evidence comment was independently reopened; checked-name total stays291.

### HealthModifier zone-type binding

Traced the original EGadgetZoneType enum through HealthModifier zone queries: the reflected ZoneType field at object offset0x110 is read after the runtime HealthModifier kind check, passed to EnqueueRegionQuery, stored in query byte0 and passed by the region processor to EvaluateRegionShapeWeight. Values0..4 preserve Sphere/Box/Cylinder/Cone/Ellipsoid; this processor clamps values5 and above to EntireLevel. TriggerZone has a separate ZoneType field at0xf0 and was not substituted for HealthModifier.

Applied GadgetZoneTypeWorkingByte to the two shape parameters. Its one-byte working storage follows actual register/record loads and stores; descriptor metadata2 is not asserted to be a byte width. Cold backup, isolated trial, promotion and independent reopening verify exactly two signature changes, unchanged original archives and successful connected caller decompilation. The static trace cross-checks1,342 original instruction spans; full producer-to-gameplay execution, other consumers and nonempty cylinder/cone behavior remain open. Checked-name total stays291.

### Saved weighted HealthModifier delta helper

Applied AccumulateHealthModifierDelta with an opaque game/modifier context, object indices, player mask, float weight and bool acceptance return. The main HealthModifier query loop passes each result weight to this helper. Original HealthGadget property names bind current/max health, cooldown, damage multiplier and player handling; original modifier modes are PerSec and PerHit.

11,520 native arithmetic/player-routing cases and five target-rejection cases match independent references. PerSec uses the captured1/30 factor; PerHit/no-history uses1. Negative raw amounts use DamageMultiplier; proposed health is clamped before deriving the accumulator delta. Cooldown blocks nonpositive deltas while healing can accumulate. The bool return means target accepted, even if no counter changes. Full target/modifier/game bytes and selected state windows are checked each case, with complete state checked at the end. No imports are modeled.

PerHit previous-history suppression/cache writes, the special immediate-application path, nonfinite/malformed inputs, full caller/gameplay integration and concurrency remain unresolved. Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original archives. Totals:292 checked descriptive names among9,577 discovered functions;1,733 mapped and7,844 unmapped.

### HealthModifier history and immediate-application branches

14,544 additional original-instruction cases validate1,872 PerHit history/cache cases,10,800 immediate-state cases and1,872 combined cases. Previous-hit membership works across scalar,8-wide,16-wide and mixed-tail list lengths. Recorded contacts remain tracked while suppressing repeat changes; eligible new contacts are tracked and applied in the selected immediate state. No imports are modeled; current hit caches are preinitialized.

The immediate path updates current health and empty-health output bits. Eligible nonpositive deltas reset remaining cooldown from the configured duration, including selected zero-delta cases; healing leaves cooldown unchanged. Source state mode/control bytes identify the branch, but their gameplay meanings remain unresolved. Exact target/modifier/game bytes are checked every case; cache/control windows and sampled complete-state checks are recorded per fixture. Lazy initialization, cache limits, malformed/nonfinite inputs, complete main-update integration and concurrency remain open. Saved comments were independently reopened; checked-name total remains292.

### Lazy HealthModifier hit-cache initialization

2,880 additional cases execute the original health helper, import thunk and libc memset implementation/jump table. The first tracked contact initializes the cache count and clears exactly object_count×4 header bytes before appending. Selected object counts4,10,64 and257 exercise16..1,028-byte original fill paths with unchanged trailing headers/guards. Previously initialized caches avoid reset; blocked new contacts leave uninitialized caches untouched, while prior hits remain tracked. No fill/import model is used.

Exact health, cooldown, output, cache and preservation checks cover the selected combined PerHit/immediate-state fixtures. Cache capacity/wrap, malformed/nonfinite inputs, the gameplay meanings of state controls, complete game-loop integration and concurrency remain unresolved. Libc trap/error and very-large fill paths are outside scope. The saved comment was independently reopened; checked-name total remains292.

### Saved object player-mask helpers

Applied ReadResolvedObjectPlayerMask and GetPowerOrResolvedObjectPlayerMask with opaque state/object pointers and a caller-visible byte return in AL. All four recorded callers consume that low byte; upper return bits and original C++ return widths remain unclaimed. The Power helper uses four nonzero per-player lanes first, including the original unordered NaN behavior, then inherited/resolved-object routing. The direct reader prefers its current object metadata field before fallback.

3,809 native checks execute both original helpers and their original fallback resolver with direct/inherited/parent/link/cached-container fixtures, all16 lane masks and a NaN lane. Linear and sorted link paths select the tested first matching0x40f entry. All object buffers and selected state windows are checked each case, with sampled full-state preservation; no imports are modeled. Exact metadata property labels, complete link semantics, malformed/cyclic graphs, large tables and game integration remain unresolved. Cold backup, isolated trial and independent reopening verify the two saved names/signatures and unchanged original archives.

Totals:294 checked names among9,577 discovered functions;1,735 mapped and7,842 unmapped. Shared-object classification reflects generic routing support, not a claim that every caller is understood.

### Player-mask field identities from original registrations

Matched original offset-table initializer stores to native registration calls and original field-name literals. For Sculpt (kind 1), table slot 0x6a4 points to object offset 0x24c, registered as PlayerOwnership. For HealthGadget (kind 0x42) and HealthModifier (kind 0x43), fallback slot 0x686 points to offsets 0xd0 and 0xe0 respectively, both registered as IsGluedGadget. Fifteen original instruction spans and three literal references establish these links.

These links apply to the specified kinds; they do not establish the field for every Thing. The resolver follows the parent when the identified gadget glue flag is set. Its Microchip field and 0x40f link meaning remain unresolved. An unrelated registered field offset with the same numeric value was rejected as a label source. No new function-name credit is added; the checked total remains 294.

### Saved Microchip type and field registration

Applied InitializeMicrochipTypeDescriptor and RegisterMicrochipProperties. The original Microchip literal and descriptor connect the initializer, Thing base registration and 14 specialized field registrations. The registrar binds IsGluedGadget at object offset0x138; the original kind13 metadata initializer writes that offset to slot0x686. This resolves the Microchip field label used by the player-mask fallback resolver. The0x40f link meaning remains unresolved.

All104 original instruction spans match. Full cold backup, isolated trial, promotion and independent reopening verify two intended name/comment changes, unchanged signatures and unchanged original archives. Specialized registrar arguments, descriptor numeric meanings, imported guard behavior, allocation/cleanup bodies and game integration remain unresolved. No native gameplay test or original C++ prototype is claimed.

Totals:296 checked names among9,577 discovered functions;1,736 mapped and7,841 unmapped.

### Saved Microchip property visitor

Applied VisitMicrochipProperties after reviewing all752 original instructions and matching its named field offsets to the Microchip registrar. It visits version-gated fields, handles nested FirstChild traversal, retains unnamed legacy placeholders and updates a legacy canvas flag for selected older versions when a stored float is nonzero or NaN. The original calls and code establish these branches; virtual callbacks and full serializer traversal were not executed.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/comment, unchanged signature and unchanged original archives. Separately,110 original instruction spans establish that Microchip property0x40f has offset-table sentinel0xffff and an eligibility consumer rejects an existing matching wire. This narrows the connection role without proving its original label.

Totals:297 checked names among9,577 discovered functions;1,736 mapped and7,841 unmapped. No game integration or complete serializer reconstruction is claimed.

### Saved wire-property eligibility check

Applied CheckWirePropertyEligibility with a caller-visible unsigned byte return and opaque state/object-reference/property/mode inputs. It rejects invalid references and selected special properties, checks existing source or destination wire endpoints for two connection properties, and conditionally requires property metadata flagbit0. The special property0x359/kind0x59 or0x5b path returns mode XOR1; it is not universally a normalized Boolean.

12,960 native fixture cases execute the original109-instruction check plus the original94-instruction wire search and98-instruction metadata lookup, with no import models. Fixtures cover linear/sorted wires, selected kinds/properties, metadata flags and noncanonical mode bytes;240 results exceed1. Object, wire and metadata buffers are preserved each case, with full state preservation sampled every500 cases. Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original archives.

Editor caller paths use this result while considering connection interactions, but exact UI modes, property labels, collision/subtype lookup paths, malformed graphs and full game integration remain unresolved. The0x40f label is not inferred. Totals:298 checked names among9,577 discovered functions;1,737 mapped and7,840 unmapped.

### Saved glued-parent and Microchip-input reference resolver

Applied ResolveGluedOrMicrochipInputReference with opaque state, encoded object reference and a full uint reference return. It resolves container/inheritance ancestry, returns the parent when the identified IsGluedGadget field is set, or scans an unglued Microchip input connection with property0x40f and returns its opposite endpoint. The original0x40f label remains unclaimed. The glue field identity is established for Microchip, HealthGadget and HealthModifier; other kinds require separate registration evidence.

256 direct native cases execute the original164-instruction resolver, independently checking complete returned references and failure sentinel0xffffffff. Input/output upper10 bits vary across four values;96 successful results retain nonzero upper reference bits. Entire state and every object buffer are preserved each case. These supplement the3809 earlier mask fixtures; no import models or game integration are claimed. Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original archives.

Cache construction, malformed or cyclic graphs, large tables and full gameplay behavior remain unresolved. Totals:299 checked names among9,577 discovered functions;1,738 mapped and7,839 unmapped.

### Saved Microchip allocation and cleanup callbacks

Defined AllocateDefaultMicrochip and FreeMicrochipStorage at the original Microchip descriptor callback targets. Complete48- and4-instruction bodies have verified nonoverlapping boundaries and original bytes. The allocator requests336 bytes and initializes the full object; cleanup skips null and forwards the exact nonnull pointer. Defaults match registered fields, including Power1, Halfsize1/1, FirstChild0xffffffff and IsGluedGadget0. The descriptor value0x40 is not asserted as allocation size.

256 creation fills check every object byte, guards, requested size and returned pointer.256 null and256 nonnull cleanup cases check forwarding. Original callbacks and import thunks execute with explicit allocator/deallocator models; actual heap implementations, allocation failure, reconstructed colour startup execution and game callback dispatch remain unverified. Cold backup, isolated trial, promotion and independent reopening confirm both definitions and opaque pointer ABIs, unchanged existing functions and unchanged original archives.

Totals:301 checked names among9,579 discovered functions;1,740 mapped and7,839 unmapped. Two previously undefined callbacks were added; this is scoped lifecycle evidence, not whole-subsystem completion.

### Specialized registrar ABI corrections

Corrected Float3, SoundCategory and AudioNumber registrars from Windows two-argument annotations to native RDI registry / RSI property name / EDX offset contracts. Named RegisterNodeCustomIconFieldOffset, whose fixed original NodeCustomIcon label takes registry in RDI and offset in ESI. The Microchip caller now decompiles Colour, UserSoundCategory, Volume and NodeCustomIcon with the correct descriptor and offsets, without the previous phantom incomingRCX. Its stale uncertainty comment was updated.

All514 original instruction spans match. Cold backup, isolated ABI trial, promotion and independent reopening verify four intended name/signature entries, connected caller decompilation and unchanged archives. RAX pointer outputs are observed working outputs, not recovered original C++ return declarations; metadata tags do not prove byte widths. Reserve/hash/type initialization and game integration remain untested here.

Only the newly named icon registrar adds checked-name credit; the three existing-name ABI corrections add none. Totals:302 checked names among9,579 discovered functions;1,743 mapped and7,836 unmapped.

### Saved HealthModifier query and impact preparation

Applied PrepareHealthModifierZoneQueriesAndImpactTargets after reviewing the complete460-instruction body. It walks active HealthModifiers and clears OutputHealthModAffected, prepares zone queries in the zero phase, and builds impact target mappings in the nonzero phase. EntireLevel zones clear the cached query handle; other shapes route through the existing geometry/mask/enqueue chain. Impact targets retain low16 mapping bits, acquire a modifier tag and append label/filter flags to the first free of eight11-bit slots. Duplicate traversal targets and full records are skipped.

1,944 native impact cases cover all slot occupancies, selected label/filter flags, map/scratch gates and negative/zero/positive/NaN target Power.576 cases append a packed token,648 reject a tagged mapping and72 reach a full eight-slot record. The original producer and libc memset execute; TLS, scratch allocation/release and graph traversal are explicit models. Exact object/packed/map/scratch/receipt checks run each case, with full game/current/previous-state preservation checked every128th.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original archives. Zone execution, real graph traversal, multiple-modifier interactions, exact filter/property2d7 labels and complete game-loop integration remain unresolved. Totals:303 checked names among9,579 discovered functions;1,744 mapped and7,835 unmapped.

### Saved region-query mask builder and filter registrars

Applied BuildObjectRegionQueryMasks and registrars for LabelAnyOrAll, LabelVisible and LabelCollidable. Original values identify Any0/All1, Visible0/Invisible1/Ignore2 and Collidable0/NotCollidable1/Ignore2. HealthModifier offset-table writes bind these fields to0x162/0x163/0x164. The helper packs unsigned16 any/all/excluded masks into the low48 return bits. Visibility and collision settings require, exclude or ignore their corresponding query bits.

69,120 direct native helper cases use an independent mask oracle and no import models. They cover present/missing fields, selected label masks and mode bytes, optional filters, kinds0x40/0x43 and stored compatibility values0/1736/1737.4,608 cases exercise explicit zero-label All behavior: all-mask0x8008 through1736,0x0008 above it, before optional filter bits. Every object and metadata row is preserved each case; complete state is checked every1,024th. The original meaning of that stored value and a separate generic gate field remain unresolved.

All530 original instruction spans match across the four functions. Cold backup, isolated trial, promotion and independent reopening verify names/signatures and connected callers. Registrar initialization, negative offset sentinels, full metadata construction and complete producer/query/BVH/game integration remain untested. The saved producer comment and current evidence records now remove the resolved filter-enum uncertainty. Original C++ return declarations and enum storage widths are not asserted. Totals:307 checked names among9,579 discovered functions;1,745 mapped and7,834 unmapped.

### Saved object zone and falloff bound reader

Applied ComputeObjectZoneAndFalloffBounds with a nonnull object pointer and four typed16-byte vector outputs. Original HealthModifier registrations and offset initializer dataflow bind ZoneSize, ZoneOffset, FalloffSize and FalloffOffset. Zone and falloff vectors become centre plus/minus half XYZ size; missing falloff size enables scalar radius overrides. Type-dependent defaults and the observed fourth lane are retained without claiming original Float3 declarations or world-space bounds.

18,432 direct original-instruction cases check every output byte and guards, full object/metadata preservation, field presence, zero/0xffff missing offsets, selected nonLight kinds and finite vector/radius inputs.9,216 cover falloff vectors and4,608 cover radius overrides. No imports/models execute on tested paths. The original initializer linkage checks1,367 straightline instructions with unchanged RAX aliases,16 registrar instructions and four literal names. This is static initializer evidence, not in-game initialization.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/pointer ABI, connected geometry caller and unchanged original archives. Light-specific paths, null/aliased/nonfinite/malformed inputs, concurrent metadata changes and full transform/query/game integration remain unresolved. Totals:308 checked names among9,579 discovered functions;1,746 mapped and7,833 unmapped.

### Saved object region-query geometry preparation

Applied PrepareObjectRegionQueryGeometry with exact working storage for five GP pointers and two full16-byte SIMD transform inputs. It composes the optional object PosOffset with the incoming transform, handles combined-rotation normalization, reads named zone/falloff bounds, and constructs shape-dependent inner/outer transforms and extents. The HealthModifier caller now shows the object and four output pointers plus two SIMD values, instead of misleading inferred arguments. Transform output pointers each cover two16-byte vectors.

11,520 native cases execute original geometry296 instructions, bounds reader185 and original libc isinff/thunk, with current module/function bytes verified and no import models.1,920 cases per shape value0..5 cover five finite HealthModifier profiles, selected base rotations, positive scales and local unit/nonunit/zero rotations;2,160 use nonunit local rotations. An independent quaternion/matrix and centre/extent reference bounds maximum numeric error at0.00000330 with tolerance0.00004. Output guards and complete object/metadata/input-frame preservation are checked each case.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/custom GP-SIMD contract, connected caller and unchanged original archives. Light/kind0x30 paths, alternate shape metadata, nonfinite/malformed/aliased inputs and complete producer/queue/game integration remain untested. Source declarations/order and fourth-lane geometry meanings are not recovered. Totals:309 checked names among9,579 discovered functions;1,747 mapped and7,832 unmapped.

### Connected HealthModifier zone request validation

The original HealthModifier producer now runs through the original geometry preparer, bounds reader, mask builder and enqueue function in one fixture.15,552 cases produce8,640 accepted requests,4,320 capacity rejections and2,592 EntireLevel bypasses. Accepted requests preserve phase1/tag5, the modifier reference and conditional glued callback pointer. Cached handles, transform/local-centre/extents, masks, count/overflow effects and every queue byte including padding match independent expectations. Empty-label All requests cover both stored compatibility values1736 and1737, with720 accepted cases on each side. Maximum numeric error is0.000000174 at tolerance0.00004.

Connected request cases execute original code for all five functions and libc isinff/thunk; only TLS lookup and scratch allocation/release are modeled. The impact graph iterator is not invoked. Complete queue/object/metadata/scratch/receipt checks run each case; complete game/current/previous-state checks run every256th. One valid modifier, cardinal rotations and positive power-of-two scales bound this evidence. Inherited bases/cache ancestry, glued callback execution, query/GPU results, concurrency and the full game loop remain unverified.

The15,552 connected configurations and11,520 earlier geometry configurations were revalidated with NaN-poisoned floating outputs, so an unwritten expected-zero lane cannot pass the tolerance check. These are strengthened reruns, not additional unique cases. Five saved comments and current evidence records were reconciled and independently reopened, with1,235 original instruction spans, names/signatures and original archives unchanged. This adds connected validation, not new-name credit:309 names remain checked among9,579 discovered functions.

### Saved glued-source parent-subtree callback

Defined AcceptRegionQueryTargetOutsideSourceParentSubtree at the original callback address. Its19 instructions/74 bytes reject the source parent and any target whose ancestor chain reaches that parent, accepting chains that reach0xffff. A0xffff target returns true before pointer dereference. The source reference comes from request offset104 and uses signedlow22 normalization; the processor supplies a fourth target-object pointer that this body ignores. The original Sculpt candidate call consumes the Boolean result in AL.

46,400 finite chain/star/forest/random-tree cases and two sentinel/null-pointer cases execute the original callback with no imports/models.26,688 tree cases accept and19,712 reject. Complete131,072-byte parent cache and guards, request and Game inputs are preserved each case; full state is sampled every1,024th. Source upper bits, unused fourth-pointer values and bounded index extremes are covered. Cache construction, malformed/negative references and cycles remain untested.

Cold backup, isolated trial, promotion and independent reopening verify the new nonoverlapping definition and working callback ABI, unchanged existing function names/signatures and unchanged original archives. The producer now names the callback; this standalone/static-link evidence does not validate GPU/query execution or the complete game loop. Totals:310 checked names among9,580 discovered functions;1,748 mapped and7,832 unmapped.

### Saved sorted reference-pair search

Applied TestSortedReferencePairRecordMatch with begin/end pointers, two uint reference arguments and a Boolean result consumed in AL. The complete43-instruction helper performs a lower-bound search through12-byte records. It compares signed low22-bit indices, switching to the second word only when the first raw32-bit references are equal. The third record word is ignored here.

6,384 original native cases match independent tuple membership for consistently encoded sorted tables, including sizes0 through513, negative/boundary indices, duplicates and four upper-bit patterns. Another20 probes show that different upper bits with equal first index can accept regardless of the second reference. Table/frame bytes and guards are unchanged; no imports/models execute.17 original caller spans confirm the12-byte stride, two packed reference arguments, raw0xffffffff exclusions and Boolean result use.

Cold backup, isolated trial, main promotion and independent reopening verify persistence, connected caller decompilation and unchanged original archives. Table production/domain, mixed-encoding ordering, malformed lengths, unsorted records and full caller/game execution remain unresolved. No subsystem assignment is claimed before tracing the table producer. Totals:311 checked names among9,580 discovered functions;1,748 remain mapped and7,832 unmapped.

### Saved persistent object ID resolver and pair-table producer trace

Applied ResolvePersistentObjectIdToIndex. It rejects ID0xffffffff before reading state, looks up a bucket by the low16 ID bits, checks a signed upper-ID fingerprint in an18-bit descriptor, then compares the full ID at the candidate object. On a miss it follows the collision chain until an index is outside the current object count. Success returns the low14-bit current index; failure returns0xffffffff.

168 finite-chain configurations plus a null-state sentinel execute all28 original instructions without imports/models. Counts0 through513, high-bit IDs, first/middle/last/missing matches and fingerprint/full-ID mismatches are covered. Every case checks full state SHA256, object and input-frame preservation. Cyclic/malformed chains, invalid object pointers, counts beyond14-bit capacity and hash-table construction remain untested.

26 original producer spans show command case0x0e resolving persistent IDs from payload offsets2 and6, appending two current indices plus the byte at payload offset10 to the12-byte table, and incrementing its count up to capacity16,383. Valid resolver output has upper reference bits zero, explaining consistent encoding on this producer path. The byte flag, command name, sorting path and complete reader/game execution remain unresolved; the pair search itself remains without a subsystem assignment.

Cold backup, isolated trial, promotion and independent reopening verify the saved resolver ABI and connected producer decompilation with original archives unchanged. Totals:312 checked names among9,580 discovered functions;1,749 mapped and7,831 unmapped.

### Saved persistent object ID pair export and sort

Applied BuildSortedPersistentObjectIdPairRecords and SortPersistentObjectIdPairRecords. The exporter compacts input records whose raw endpoint references are not0xffffffff, resolves signed low22-bit indices through the current object array, and writes persistent IDs from object offset0. Invalid indices or null object pointers produce0xffffffff IDs without removing that pair. The connected sorter orders signed32-bit first/second IDs lexicographically, carrying the byte at offset8 while leaving padding9..11 in physical slots.

72 original native export/recursive-sort cases cover preallocated output, counts0 through129, empty and existing destination lengths, raw sentinels, invalid indices, null objects and signed IDs. Full state SHA256/objects are preserved. Vector headers, signed ordering, pair/flag multisets, output guards and padding are checked. No imports/models execute on this path.183 exporter and807 sorter instruction spans match the original executable.

The exporter does not copy source byte8: newly initialized destination slots have flag0, while existing flags remain associated with compacted destination positions before sorting. This is recorded behavior, not a recovered semantic meaning for the flag. Real allocator behavior, malformed or aliased input, depth-budget exhaustion and whole caller/game execution remain untested; modeled growth/failure results follow below. Sorting persistent-ID output does not establish the runtime index-pair table sorting path.

Cold backup, isolated trial, main promotion and independent reopening verify both saved names, working pointer/depth ABI, connected exporter decompilation and unchanged original archives. Totals:314 checked names among9,580 discovered functions;1,751 mapped and7,829 unmapped.

### Persistent pair exporter growth and conditional failure behavior

36 additional original exporter/sorter configurations test counts3,7,33 and129 with old length/capacity0,1 or2. The allocator and deallocator are explicit native boundary models: requested alignment, byte size, returned backing and freed pointer are recorded.12 first-allocation successes verify alignment16, capacity=max(2*oldcapacity,sourcecount),12-byte records, copying/freeing old storage, initialization and final sorted IDs.

24 conditional null-allocation probes show that a failed first allocation does not stop compaction into the old buffer. Pair writes exceed its logical capacity. The fixture deliberately reserves oversized guarded backing to observe this without touching outside physical storage. If a later retry succeeds, only old-length records are copied and remaining output slots become0xffffffff ID pairs with zero flags. If both attempts fail, old length/capacity remain although pair data was written beyond logical capacity. All cases check expected records/headers, allocator/free receipts, guards, full state SHA256 and object preservation.

These findings are conditional on an allocator returning null. The real allocator may terminate or throw instead; no live-game heap failure is demonstrated. Real heap behavior, concurrency, malformed/aliased inputs, depth-budget exhaustion and complete caller/game execution remain unresolved. The saved exporter comment was updated reversibly and independently reopened; names, signatures, original native bytes and archives are unchanged. No additional checked-name credit:314 of9,580 discovered functions.

### Original libc allocator forwarding and descriptor rejection

The original game loader NIDs resolve the pair exporter imports to memalign and free, and both NIDs match the local PS4 libc export table. ELF relative relocations bind the memalign forwarding slot to module offset0x27fd0 and the free slot to0x27f00. The memalign wrapper supplies a global heap descriptor to dispatcher0x31320.

96 original native cases execute the exported memalign wrapper, relocated forwarding target and descriptor dispatcher. With deliberately mismatching synthetic heap metadata, the dispatcher returns null before calling the internal allocator. Both cookie modes, three mismatching descriptor values, four alignments and four sizes are covered; the input frame and complete16KiB data window remain unchanged. No allocator/import call is reached.

This establishes an original null-return branch for descriptor rejection, not memory exhaustion on a valid initialized heap. Heap setup/validity, runtime dispatch-pointer replacement, the internal allocation implementation and live-game failure behavior remain unresolved. No additional checked-name credit:314 of9,580 discovered functions.

### Saved object-pair add/remove command builders

Applied SubmitAddPersistentObjectIdPairCommand and SubmitRemoveCurrentObjectPairCommand. Add builds an11-byte payload: ushort0xfdf6, two persistent uint IDs at offsets2 and6, and zero byte at10. Remove resolves a current pair record through the object array, writes persistent IDs or0xffffffff for invalid/null endpoints, and serializes record byte8&1 at offset10 with command0xfdf7. Both forward player and eligibility metadata.

32 add and24 remove cases execute the original70/107-instruction builders with a receipt-only dispatcher model. They verify payloads, command IDs, endpoint stack arguments, player and eligibility flags, full state SHA256 and object/record/frame preservation. Scope is null game context, selected player/count/actor-presence states and endpoint boundary cases; game-present GUI/global-override paths and actual command queue/application remain untested.

Original jump-table bytes map0xfdf6 to the append branch and0xfdf7 to the branch that invalidates the supplied current pair endpoints. A larger caller exports pair tables from two snapshots and emits these commands while comparing them. Its complete behavior, the pair flag meaning and full gameplay integration remain unresolved; it receives no full-function review credit.

Cold backup, isolated trial, main promotion and independent reopening verify both saved names, working byte/uint/pointer ABI and connected caller decompilation, with original archives unchanged. Totals:316 checked names among9,580 discovered functions;1,753 mapped and7,827 unmapped.

### Saved legacy object-pair to glued-parent conversion

Applied ConvertObjectPairToGluedParent. The source inheritance byte must be zero, its IsGluedGadget metadata offset positive, and its glue byte clear. The target must differ from the source and existing parent and belong to the accepted type set. Success writes the full target reference to source offset4 and sets its IsGluedGadget field to1. Optional branches convert a local transform and invalidate matching property0x231 wire records; scoped wire cleanup validation follows below, while transform conversion remains untested.

3,024 original-native cases with54 accepted conversions cover the previously identified Microchip, HealthGadget and HealthModifier glue offsets, missing0/0xffff metadata, inherited/already-glued sources, self/same-parent rejection, target-type gates and upper reference bits. No imports/models execute on this tested path; optional transform metadata is absent and wire count is zero. Complete guarded source/target/frame/metadata effects are checked, with full state SHA256 every64th case.

65 original versioned-caller instructions show the helper being used for compatible pair endpoints, its AL result accumulated and the old pair invalidated. This connects a legacy use of the table to glued-object relationships; it does not prove that every pair or flag means glue. Malformed/null inputs, cycles, optional transform branches and complete caller/game behavior remain unresolved; scoped wire cleanup validation follows below.

Cold backup, isolated trial, promotion and independent reopening verify the saved name and working state/object/reference ABI, unchanged existing functions and original archives. Totals:317 checked names among9,580 discovered functions;1,754 mapped and7,826 unmapped.

### Glue migration wire cleanup validation

48 additional cases execute the original glue-conversion helper through its wire cleanup path, with168 expected invalidations and wire counts1,2,17 and257. No imports/models execute; optional transform metadata remains absent. Each64-byte wire record must have flag byte48 bit0 set, property at40 equal0x231, and endpoint reference at36 resolving to the source object pointer. Matching record bytes32 through39 become0xffffffffffffffff. Property, flags, padding and count remain unchanged.

Tests cover three known glue-bearing object types, nonmatching flags/properties/endpoints, invalid references, upper reference bits, distinct indices resolving to the same source pointer and inherited-source rejection. Every case checks full expected state SHA256 and guarded source/target objects, frame and metadata, including expected parent/glue changes.

The saved comment was updated reversibly and independently reopened; names, signatures, original instructions and archives are unchanged. Optional local-transform conversion, malformed pointers/cycles, full-capacity arrays and complete versioned caller/game behavior remain unresolved. This is a wire-record flag, not identification of the separate pair-table flag. Checked-name count remains317 of9,580.

### Saved transform copy with normalized rotation and corrected stack input

Applied CopyTransformWithNormalizedRotation with a typed output pointer in RDI and a32-byte value at incoming stack offset8. The new RigidTransformWorking32 container contains two16-byte working vectors at offsets0 and16, representing position/scale and quaternion lanes. The caller previously omitted this stack input in decompilation; it now shows the complete copy call and typed output. This is an observed machine layout, not recovery of an original C++ declaration.

The first vector is copied bit-for-bit. Zero or infinite squared quaternion norms produce identity rotation. Norms within5e-7 of1 preserve the input quaternion bits; other tested norms use reciprocal-square-root refinement.511 original-native cases execute the49-instruction helper and actual22-byte libc isinff with no import models:3 identity fallbacks,5 near-unit preservation cases and503 normalizations. Maximum absolute error is1.17e-7 at tolerance3e-6. NaN-poison outputs, exact first-vector preservation, guards and input-frame checks are included.

Cold backup, isolated trial, main promotion and independent reopening verify the saved name, custom stack value storage, exact working type offsets and connected caller decompilation with unchanged original archives. Quaternion NaN payloads, subnormal/FTZ modes, aliasing and complete glue-migration transform composition remain unresolved. Totals:318 checked names among9,580 discovered functions;1,755 mapped and7,825 unmapped.

### Reviewed existing transform composition name and repaired input ABI

Retained the pre-existing descriptive name ComposeRigidTransform and reviewed its complete93-instruction body. Corrected its previously empty signature to a typed output pointer in RDI plus four working16-byte vectors in XMM0 throughXMM3: first position/scale, first rotation, second position/scale and second rotation. The migration caller now shows all inputs.

768 original-native cases execute the helper and actual libc isinff without import models. The independent oracle checks position=A.position+A.scale*Rotate(A.rotation,B.position), scale=A.scale*B.scale and normalized quaternion product.192 zero products use identity rotation. Maximum absolute error is6.98e-7 at5e-5 tolerance; NaN-poison outputs, guards and input frames are checked, and the bridge preserves Win64 XMM6 throughXMM15.

Cold backup, isolated trial, main promotion and independent reopening verify the corrected custom ABI, working types and connected caller decompilation, with unchanged original archives. First rotations are normalized and positions/scales use selected finite positive profiles; first-rotation nonunit/nonfinite behavior, subnormal/FTZ modes, aliasing and the complete glue conversion chain remain unresolved.

This is one newly checked existing name, not a new rename. Totals:319 checked names consist of289 existing-function renames,29 created functions and1 retained existing-name review, among9,580 discovered functions.1,756 functions are mapped and7,824 unmapped.

### Connected glue conversion, parent-relative transform and wire cleanup

1,536 scoped cases execute the original glue conversion, composition and normalization helpers together (312 instructions), plus the original22-byte libc isinff, with no function models. A Microchip source is converted to an allowed Sculpt parent. Original initializer stores bind Microchip position offset0x40, ParentFromModel0x60 and IsGluedGadget0x138; the Sculpt position field uses0x50. The ParentFromModel registration was also checked against original bytes. A Microchip parent is excluded by the original target-type mask and is not used in this fixture.

An independent inverse-parent/world transform oracle checks the resulting ParentFromModel position, scale and normalized rotation. The test also checks the parent reference, glue byte and1,536 expected wire-record endpoint invalidations. Maximum absolute transform error is3.14e-6 at tolerance1e-4. Guarded source/target objects, frame, both metadata rows and wire buffers are checked every case. Full expected state SHA256 is checked every31st case so samples cover zero and nonzero wire paths; the sampling audit rerun does not add duplicate case credit.

Coverage uses finite positions, selected positive scales, normalized parent rotations and unit/nonunit/zero source rotations. The versioned caller, old-pair invalidation, hierarchy caches, malformed/nonfinite transforms, cycles, aliasing and full game integration remain unresolved. This is scoped integration evidence, not completion of Dreams or the complete migration system.

All three saved comments were updated reversibly and independently reopened. Names/signatures, original instruction bytes and archives are unchanged. Checked-name count remains319 of9,580.

### Bounded serialized-game upgrade caller and old-pair retirement

The original caller references serialise_upgrade.cpp and receives its version value in ESI. The selected native region compares that value as signed and enters this glue-pair conversion loop for versions at or below0x17e. The tested0x17d and0x17e cases execute it;0x17f and0x220 skip it from this entry. Earlier upgrade branches and later continuations are excluded.

60 native cases execute the original bounded loop and the original migration/composition/normalization helpers with libc isinff. Explicit generated exit trampolines stop before other upgrades; this is not full-caller execution. Tests cover empty/small/mixed arrays, duplicate/reversed pairs, invalid endpoints, incompatible types and inherited/already-glued sources. An independent sequential oracle verifies full expected state SHA256, objects, frame, metadata and guards every case. Large Windows stack pages are pre-touched and nonvolatile GP/XMM registers preserved.

108 old pairs are invalidated. The caller selects the first endpoint with positive glue metadata, otherwise the second. After calling the helper, it invalidates the old pair even if conversion is rejected. Only successful conversions contribute1 to the local change accumulator. Retiring an old record therefore does not mean that a new glued-parent relationship was created.

The evidence comment was updated reversibly and independently reopened; names, signatures, original instructions and archives remain unchanged. The full15,647-instruction caller is not reviewed or given a function name/progress credit. Full loading/game behavior and other upgrade branches remain unresolved. Checked-name count stays319 of9,580.

### Saved EThingType registration and complete label map

Applied RegisterThingTypeEnumEntries and AppendThingTypeEnumEntry. The original initializer registers121 immediate value/name pairs: values0 through119 and LAST120 sentinel. The entry builder lazily configures metadata, computes name length/hash and appends a24-byte value/name-pointer/hash record, with a separate growth/failure path.

Four preallocated runs execute the original366-instruction initializer,91-instruction builder, original name hash and actual96-byte libc strlen without import models.484 appended records match an independent native-literal map and short-ASCII padded polynomial/hash oracle. Fresh/already initialized metadata and empty/prefixed arrays are covered; complete output guards/padding/prefix and64KiB descriptor page match expected bytes. The first oracle omitted an original fixed high-term hash constant; it was corrected from the original MOV instruction before these checks passed. No general hash-function review credit is claimed.

The [verified object type map](analysis/thing-types.json) includes Group0, Sculpt1, Key3, Joint5, PuppetHeart11, Microchip13, Timeline14 and Sound15. These are registered names in this executable, including deprecated/internal entries; they do not prove feature availability or an original enum declaration width. This identifies the next legacy pair-cleanup test for kind5 as Joint; the separate pair flag remains unresolved.

Cold backup, isolated trial, main promotion and independent reopening verify both names, the observed byte/string entry ABI, type-context caller decompilation and unchanged original archives. Allocation/growth/failure and callback invocation remain untested. Totals:321 checked names (291 renames,29 created functions,1 retained existing-name review) among9,580 discovered functions. Mapping totals remain1,756 mapped and7,824 unmapped because these two functions were already classified as type registration.

### Bounded legacy Joint-pair cleanup

The next selected upgrade stage is gated by a signed version comparison at or below0x220. Original EThingType registration identifies masked type5 as Joint. When both endpoint references resolve to nonnull objects and either endpoint is a Joint, the cleanup invalidates only the first8 bytes of the12-byte pair record. Flags, padding and table count are preserved. This region does not interpret the pair flag.

192 native cases cover versions0x17e,0x21f,0x220 and0x221; arrays of0,1,2,9,33 and257 records; null object slots; invalid/negative/upper-bit references; reversed and self pairs; and flags0,1,2 and255.3,060 expected pair retirements match an independent signed-low22/type oracle. Full expected state SHA256, guarded objects/pairs and input frames are checked every case.

The harness executes the original version gate and cleanup region with a generated trampoline skipping the intervening parent-upgrade block and exiting before later upgrades. Earlier glue conversion is excluded. This is bounded native-region evidence, not full-caller or game execution. Large Windows stack pages are pre-touched and nonvolatile GP/XMM registers preserved.

Both region comments explicitly mark partial review and were saved reversibly and independently reopened. Names/signatures, original instructions and archives are unchanged. The full15,647-instruction caller remains unreviewed; no additional name credit. Checked-name count stays321 of9,580.

### Connected Joint parent upgrade and pair cleanup

216 additional native cases execute the original version gate, intervening Joint parent-upgrade block and following pair cleanup consecutively. Only the exit before later upgrades is generated; the parent block is no longer skipped. Tested versions0x21f and0x220 run both blocks;0x221 skips them. The selected contiguous region has159 owned original instruction spans.

A Joint must have a parent resolving to a Sculpt. That Sculpt must have a parent resolving to an object whose own parent reference H is not0xffffffff. The code scans for any nonnull PuppetHeart with parent reference exactly equal to H. On a match, it copies H into the Joint parent field. The comparison uses the full32-bit reference: differing upper bits prevent a match even when the normalized index is the same. Group and Light grandparent kinds behave alike in the tested block. Original enum registrations bind all type names.

Nine graph schemas cover valid/missing/wrong-type/null chains, absent PuppetHeart and exact-reference mismatch, with encoded-reference variants and empty/populated pair tables.32 expected Joint-parent changes and488 pair retirements match independent parent-chain and cleanup oracles. Full expected state SHA256 and guarded objects/pairs/frame are checked every case; pair flags/padding/count remain intact.

All three region comments explicitly retain partial-review scope and were saved reversibly and independently reopened. Names/signatures, original instructions and archives remain unchanged. Grandparent lookup is valid/non-null in these fixtures; malformed grandparent chains, cycles, earlier/later upgrade stages and full15,647-instruction caller/game execution remain unverified. No new name credit:321 of9,580 checked names.

### Global gravity settings: verified accumulation branch

Traced the registered GlobalSettings gravity fields into a runtime consumer and cross-checked all 462 instructions against the original executable. A bounded native fixture passed 1,575 finite-value cases: when AdjustGravityStrength is nonzero, the branch adds Power times GravityMul to a sum and abs(Power) to its weight. With the option off, both values remain unchanged. Guarded output and unchanged input/field checks passed against an exact float32 oracle.

This tests five original instructions with generated setup and exit, without import models. It does not test the complete function, concurrent snapshot/retry behavior, reset handling, final normalization or application to physical bodies. One caller supplies a null previous-settings pointer; its reachability through the reset-edge test remains unresolved. No new function name or whole-function review credit is added.

The developer stream's per-object gravity-factor example remains a separate lead. Matching gravity terminology does not establish a source-code match. Reverse engineering is still incomplete; the checked-name total remains 321 of 9,580 discovered functions.

### Global gravity: resolved strength and direction

Followed the accumulated gravity sum and weight into the game update pass. A contiguous 30-instruction normalization window passed 1,715 native finite-value cases using the original constants. Positive strength weight produces (sum / weight) times 9.81; nonpositive weight defaults to 9.81. Direction uses its own weighted vector, defaults downward for nonpositive direction weight, and normalizes by XYZ length. A near-zero XYZ length produces zero direction.

The initial test oracle incorrectly counted the fourth lane in the squared length. Reading the original SIMD instructions corrected that assumption; fourth-lane-only and mixed-lane cases now pass. Maximum direction error was below 0.000000077. Guarded poisoned outputs and unchanged inputs passed. Generated setup/output boundaries exclude snapshot locking and subsequent physics execution.

A downstream object-loop consumer reads both resolved fields and multiplies strength by direction, but its full behavior remains under review. No full-function name or additional completion credit is claimed. The livestream's per-object gravity-factor implementation is still unmatched.

### Sculpt gravity flag and movement-gadget linkage

Mapped twelve Mover/Follower properties through their original metadata initializers and registrations, checking 347 instructions. Damping and per-axis damping amounts match the movement loop; Follower TargetPosition and ValidTarget identify its gadget outputs. This narrows the earlier downstream finding to movement-gadget processing, without claiming general gravity application for all physical bodies.

Separately traced Sculpt.IgnoreGravity into a packed physics-related attribute path. The current registrar and consumer total 1,345 instructions checked against the original executable. A contiguous 26-instruction window passed 252 native cases: any nonzero IgnoreGravity flag makes the fourth packed byte zero; otherwise a body coefficient is scaled by 255, rounded via truncation after adding 0.5, and saturated into a byte. Negative, zero, fractional and above-one coefficients, multiple body indices and flag values were covered with exact output and unchanged input checks.

Two adjacent runtime friction coefficients were explicit fixture inputs, not recovered initialization. Generated setup/exit boundaries exclude zero-count fallback, upload routing and the solver. The next trace must establish how the packed coefficient is consumed and where the body coefficient is produced. No extra function completion credit or match to the streamed per-object gravity-factor source is claimed.

### Sculpt particle coefficient distribution

Connected the original gravity-sensitive packing window to the original particle-array copy loop with an explicit generated boundary. The fixture passed 480 cases across particle counts 1, 2, 17, 33 and 129, multiple starting indices, body indices, friction values and gravity coefficients. Each of four arrays matched complete guarded expected bytes, totaling 17,472 checked particle entries per array. The first array receives the packed word, the second receives zero, and the remaining two receive a separate packed word. All bytes outside the object range remain unchanged.

The connection deliberately skips particle geometry, mass computation and range allocation; it is not a complete function execution. Runtime friction coefficients and array pointer bindings remain explicit fixture inputs. The first disposable run failed because the fixture template omitted code/constants loading; the corrected fixture passed before these results were recorded.

Separately checked the caller's original instructions: it prepares a gravity parameter with XYZ equal to direction times strength and a fourth lane equal to strength. How the coefficient arrays and gravity parameters reach the solver, and how the solver interprets them, still require tracing. No complete-function review or additional naming credit is claimed.

### Saved physics array pointer table helper

Applied PopulatePhysicsArrayPointerTable after reading the complete 218-instruction body and tracing its caller. It clears a 0x338-byte output table and fills 103 eight-byte entries from physics resource slots. The four particle arrays traced from Sculpt coefficient packing appear in table slots 10, 12, 13 and 14.

1,024 complete native tests execute the original function and actual original libc memset through its original import thunk, without import models. Sixty-four independent source patterns and output alignments 0 through 15 match exact output bytes, guards and the whole readonly source page. Global resource initialization, pointer validity for later dereference, overlap/malformed pointers and solver interpretation remain unresolved.

A full cold backup, isolated trial, promotion and independent reopening verify the saved name and working RDI output-pointer signature. Original instructions and archives are unchanged. Totals: 322 checked names (292 renames, 29 created functions and one retained-name review) among 9,580 discovered functions; 1,757 mapped and 7,823 unmapped. This does not mark the physics solver or Dreams complete.

### Located the compiled physics shader resources

The traced Predict stage submits a GPU compute dispatch with groups calculated from the particle count in batches of 64, followed by a compute barrier. Its program loader constructs a shader resource path and looks it up by hash. This establishes where CPU setup hands off to compiled shader code; CPU pseudocode alone does not establish the solver's gravity behavior.

Validated the local shader archive's 604 sorted unique entries and all resource bounds. Executing the original 148-instruction path hash routine with seed zero confirms four exact resources: Predict (556 bytes), GrabConstraint (2,632), ApplyConstraints (1,004) and Advance (1,524). Extracted binaries remain local. Predict and the neighboring GrabConstraint loaders were inspected individually; the remaining two resource paths are confirmed by native hashing, without claiming their full loader behavior.

Shader instruction decoding, buffer bindings and the gravity coefficient's solver interpretation remain unfinished. These are resource matches, not four completed shader decompilations, and add no function naming credit.

### Predict shader instruction trace

Decoded a 228-byte executable region containing 47 instructions from the confirmed Predict resource. Its first instruction's metadata pointer, footer code length and terminal instruction agree on the region. Reassembling the complete disassembly with CLRX reproduces every code byte exactly. The disassembler was obtained from its publisher and its archive checksum verified; extracted game code and disassembly remain local.

The instruction trace calculates each lane's particle index and exits for indices outside the count. A flag-word bit gates a three-component update. Enabled lanes combine the old value with a vector parameter times a step scalar and the fourth formatted component; disabled lanes store zero. Another four-component buffer then advances XYZ using the updated three-component value and the same step, preserving its fourth component.

These are symbolic instruction roles. CPU descriptor bindings, formatted component conversion and the original loader's code-boundary calculation still need corroboration before identifying the fields conclusively as velocity, position and gravity. Byte-exact reassembly is not GPU execution or proof of solver correctness. No new function completion credit is added.

Tool/format references: [CLRX disassembler documentation](https://github.com/CLRX/CLRX-mirror/wiki/ClrxDisasm) and [opengnm shader binary structures](https://ps4-opengnm.github.io/opengnm/reference/shaderbinary/).

### Predict: linked gravity coefficient and CPU bindings

Traced the original CPU descriptor copies into the parameter offsets used by Predict. Its formatted input comes from the same particle array that receives the Sculpt IgnoreGravity-sensitive packed word. The vector parameter comes from resolved global gravity, and the step scalar comes from the frame step divided by an integer divisor.

768 native cases execute the complete original descriptor constructor, original format-size helper/table and descriptor flag setter. The resulting descriptor has four-byte stride, four eight-bit components, unsigned normalized conversion and XYZW selection. Full descriptor bytes, guards and unchanged input frames match. The format identities are corroborated by [the pinned shadPS4 format definitions](https://github.com/shadps4-emu/shadPS4/blob/b2d7ec7d31f9ad9426db93afe079db8679b3e1e0/src/video_core/amdgpu/pixel_format.h). These tests verify descriptor generation, not GPU execution.

The resulting static integration trace is: for in-range particles with flag bit 13 set, the three-component value becomes its old value plus global gravity times the step times the packed fourth byte divided by 255. With the bit clear, the shader stores zero instead. The output XYZ then advances by the step times that value, preserving the input fourth component. This supports descriptive velocity/position roles. IgnoreGravity removes this shader's gravity contribution in enabled lanes by making the packed coefficient zero.

The flag bit's producer/meaning, exact shader floating-point rounding, original shader code-boundary parser and live-game behavior remain unresolved. No additional function completion credit is claimed.

### Predict flag packing and original shader section boundaries

1,536 native cases verify the CPU flag-packing expression. For body indices below 8,192, the shader's enabling bit 13 is the inverse of body metadata flag 0x20. Probes at indices 8,192 and 16,383 show that the unmasked index can force that bit on. These probes establish arithmetic behavior, not that such indices occur in a valid game state. The body's index bound and the meaning/producer of flag 0x20 remain unresolved; no sleeping/static interpretation is assigned.

The original ExtractShaderBinarySections helper also passed 64 native cases using all four confirmed shader resources at sixteen input alignments. It independently confirms the instruction start at resource offset 96. For Predict it returns a 404-byte section containing the 228-byte executable span plus metadata. Footer length, first-instruction metadata pointer and terminal instruction agree on the executable span, addressing the earlier section-start corroboration gap.

Exact output pointers/lengths, guards, padding and unchanged resource bytes passed. This does not validate malformed headers, execute the shaders or add naming/completion credit. The graph's checked-name count remains 322.

### Advance shader: final motion commit gate

Decoded Advance's 1,152-byte executable span and reassembled all 236 instructions to byte-identical code. Original CPU descriptor copies and dispatch instructions connect its particle flags and second per-particle word to the common parameter table. The shader explicitly masks body lookup indices to thirteen bits; the producer's valid index bound still requires verification.

The selected final write path keeps candidate velocity and commits candidate position when either the candidate XYZ squared length exceeds a threshold and particle flag bit 13 is set, or bit 0 in a second particle word is set. Otherwise it writes zero velocity and does not overwrite the primary position at that commit point. Thus Predict's earlier flag gate alone does not establish the final motion outcome.

The second bit's producer/meaning, threshold initialization and earlier correction/matrix paths remain unresolved. This is a selected static data-flow review plus full byte-exact instruction decoding, not execution or complete understanding of Advance. No shader/function completion credit is added; raw shader code remains local.

### GrabConstraint marker reaches Advance

Found a writer for the second particle word used by Advance's final commit gate. After checking the slot's particle range and activation mask, GrabConstraint reads that word, sets bit 0, and writes it back with an additional descriptor-count bounds check. The common CPU descriptor table links this write to the same array read by Advance. This establishes one path by which an active grab constraint can force the final commit independently of the motion threshold and particle bit 13.

The marker is set before later correction calculations, so it does not prove that a nonzero correction was produced. CPU instructions copy the slot mask into the parameter field read by the shader; an identified set site enables a slot when its state byte equals 2. The original state label and complete mask provenance remain unresolved.

GrabConstraint (475 instructions), ApplyConstraints (134) and ResetConstraints (285) now have byte-exact decode/reassembly checks. ResetConstraints was separately matched to the local archive with the original native path hash routine. These decoding results do not mark their complete behaviors understood. Only the selected marker writer/reader path is traced here; GPU execution, other writers and synchronization behavior remain unverified. No new naming credit is added, and binaries/disassembly stay local.

### Saved Predict and GrabConstraint shader getters

Applied GetPredictShader and GetGrabConstraintShader with working opaque pointer return types. Their complete bodies construct the corresponding shader resource paths, consult the packed resource table and support file-loading fallback. Each returns its static shader descriptor when its handle is present, otherwise null. Original native hashing independently confirms both archive resources.

256 original-native initialized cached-success cases verify the exact descriptor address and an unchanged readonly global page. No imported callees execute in those cases. Initialization, path construction, lookup/load/failure and concurrency were inspected statically but remain outside the native test coverage; no complete shader or solver execution is claimed.

Full cold backup, isolated trial, promotion and independent reopening verify both saved names/signatures and unchanged instructions/archives. Totals: 324 checked names (294 renames, 29 created functions, one retained-name review) among 9,580 discovered functions. Mapping remains 1,757 mapped and 7,823 unmapped because both wrappers were already classified under physics simulation.

### Shader file-open failure follow-up

Traced the shader file helper through resolved fopen, fseek, ftell, malloc, fread and fclose imports. Its failed-open branch returns false without initializing the caller's output pointer or size. 384 native helper cases with a failed-open boundary model verify that both sentinel outputs remain untouched.

256 further cases execute the complete original getters and file helper with explicit formatting, failed-open and recording-only free models. When both open attempts fail, each getter returns null but passes its preexisting scratch pointer value to modeled free. Seeded scratch values survive to that argument unchanged. This identifies a potentially unsafe cleanup path; it does not establish a live-game crash, exploit or actual deallocation. Real scratch contents depend on prior stack state.

The formatting model supplies only a terminated empty path, the open model returns null, and the free model records rather than frees. Actual formatting/filesystem behavior, successful loading, allocation failures, short reads and concurrency remain untested. Updated Ghidra comments survived independent reopening with unchanged names, signatures and all 409 getter instruction spans. The checked-name total remains 324.

### Saved shader file-buffer reader

Applied ReadShaderFileToAllocatedBuffer after reviewing its complete 44-instruction body and shader-loading callers. It opens the path, obtains a size truncated to 32 bits, allocates a buffer, requests the read and closes the file. Its Boolean result reports whether opening succeeded. Seek, tell, allocation, read and close errors do not change that result; true does not guarantee a complete usable buffer. Failed open leaves both output values untouched.

384 failed-open and 144 opened-file original-native cases verify call receipts, outputs and guards. Explicit I/O/allocator boundary models do not perform real filesystem access, payload transfer or allocation/deallocation. These checks establish helper control flow, not real backend reliability or complete shader loading.

Full cold backup, isolated trial, promotion and independent reopening verify the descriptive name and working signature without changing original instructions or archives. The generic helper is mapped under shared engine runtime support, rather than credited to an exclusive gameplay subsystem. Totals: 325 checked names (295 renames, 29 created functions and one retained-name review) among 9,580 discovered functions; 1,758 mapped and 7,822 unmapped. This is not a percentage of the entire game understood.

### Saved vertex-fetch shader helpers

Applied ComputeVertexFetchShaderSize and GenerateVertexFetchShaderInstructions after reading their complete bodies and shader construction callers. The first computes the auxiliary buffer size from a shader header. The second emits descriptor loads, formatted vertex-buffer loads, waits and a return instruction, followed by a metadata count. Both are mapped to the rendering graphics toolkit.

8,600 original-native size-wrapper/setup cases and 3,584 original-native generation cases verify synthetic inputs, exact outputs and guards without modeled imports. Independent CLRX decoding and reassembly reproduce a 72-byte generated program exactly; its trailing four-byte metadata count is excluded from executable decoding. Real shader compatibility, malformed inputs and GPU execution remain unverified. The surrounding resource initializer still has unresolved allocation-error handling; it receives no completion credit here.

Full cold backup, isolated trial, promotion and independent reopening verify both saved names and working signatures, unchanged original instructions and unchanged archives. Totals: 327 checked names (297 renames, 29 created functions and one retained-name review) among 9,580 discovered functions; 1,760 mapped and 7,820 unmapped. These counts do not measure whole-game completion.

### Saved header-to-vertex-fetch wrapper

Applied CreateVertexFetchShaderFromHeader with a working void return and instruction-output, modifier-output and opaque shader-header pointer arguments. Its complete body prepares the fetch descriptor from shader registers, points it at inline usage and vertex-semantic records, generates the auxiliary program and writes the register modifier. It is mapped under the rendering graphics toolkit.

2,560 connected original-native cases execute the size wrapper, generation wrapper, setup helper and generator together (362 instruction spans). Calculated size equals the exact emitted instructions plus trailing metadata. Output slack/guards, register modifier, complete inputs and canary match at four alignments without modeled callees/imports. Synthetic header acceptance does not establish real resource compatibility, malformed-header safety or GPU execution.

Full cold backup, isolated trial, promotion and independent reopening verify the saved name/signature, original instructions and archives. Totals: 328 checked names (298 renames, 29 created functions and one retained-name review), 1,761 mapped functions and 7,819 unmapped among 9,580 discovered functions. Whole-game completion is not claimed.

### Debug-text records and saved text-unit decoder

Applied DecodeTextUtf8UnitWithEscapes with working codepoint-output, cursor, end and escaped-flag arguments. 4,380 ordinary-unit and 2,992 escape original-native cases verify exact values, cursor advancement and guards; escape tests use the actual original libc memchr. The decoder is not a strict Unicode validator. Backslash-n produces linefeed while leaving the cursor at n and the escaped flag clear; its higher-parser effect remains unresolved.

The linked archived debug-text vertex shader directly reads 16-byte packed records and expands each into six vertices. CPU emission and draw callers confirm the record layout and pending-count times six. 8,192 tests of original packing windows verify half-float pairs, color and atlas row cutoff. Both inline character-normalization paths match across every 16-bit input and selected 32-bit boundaries. The 344-byte shader independently decodes/reassembles exactly. Selected windows do not validate the entire emitter; glyph decoding/lookup, graphics submission, resource lifetime and GPU execution remain unresolved.

Native resource-path hashing also matches 94 vertex-path candidates to local archived shaders. All have zero fetch-input count in the inspected layout; individual caller links remain leads except the directly traced examples. Construction checks cover 1,504 resource/alignment cases, not in-game rendering.

Full cold backup, isolated trial, promotion and independent reopening verify the new name/signature, original instructions and archives. Totals: 329 checked names (299 renames, 29 created functions and one retained-name review), 1,762 mapped and 7,818 unmapped among 9,580 discovered functions. No whole-game completion percentage is inferred.

### Saved emoji skin-tone suffix decoder

Applied TryDecodeEmojiSkinToneSuffix with a working Boolean return and tone-code output, base codepoint, cursor, end and variation-present output arguments. It checks the original 99-entry base-character table and recognizes U+1F3FB through U+1F3FF, directly or after U+FE0F. Success writes values 48 through 52 and consumes the suffix; failure preserves the caller outputs and cursor.

7,416 original-native helper/decoder cases cover every eligible base, four noneligible values, all five modifiers, optional variation selector and missing/malformed/truncated suffixes at four alignments. Exact values, guards, source and canary match without modeled callees. This executable-specific table does not establish current Unicode support, glyph availability or correct visible emoji rendering.

A separate connected check confirms that repeated calls to the complete base parser preserve the lower decoder behavior: backslash-n followed by Z yields linefeed, n and Z. Its effect in the final text wrapper and visible rendering remains unresolved.

Full cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 330 checked names (300 renames, 29 created functions and one retained-name review), 1,763 mapped and 7,817 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved emoji sequence matcher and plain unit decoder

Applied TryMatchTextEmojiSequence and DecodeUtf8Unit with working Boolean returns and bounded cursor/output arguments. The matcher checks the original 60-group, 379-sequence table, returns an executable-specific mapped value and commits only the matched prefix. Failure preserves cursor and output. Its optional mode supplies an implicit variation selector before the input. The plain decoder reads one UTF8-like unit without interpreting backslash escapes; it is not a strict Unicode validator.

12,528 complete original matcher cases cover every table entry, exact/extended/truncated/mismatch inputs, both insertion modes and four alignments. 4,392 complete original plain-decoder cases verify values, cursor and guards. Another 48 selected connected base-parser cases confirm that variation selectors are consumed only for eligible original character properties; accepted FE0E/FE0F set numeric style values one/two. These checks use original code/tables without modeled callees, and do not verify font availability, whole markup parsing or visible rendering.

Full cold backup, isolated trial, promotion and independent reopening verify both names/signatures and unchanged original instructions/archives. Totals: 332 checked names (302 renames, 29 created functions and one retained-name review), 1,765 mapped and 7,815 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved text color and size tag parsers

Applied TryParseTextColorTag and TryParseTextSizeTag with working Boolean returns and bounded byte-range/output arguments. Color parsing recognizes color/colour, 148 exact named colors, RGB and RGBA hex forms. RGB gains opaque alpha; packed bytes are reordered. All-zero RGBA returns false, and invalid hex can return false after writing a partial accumulator. Size parsing accepts size= with one to three ASCII digits, clamps successful values to 1 through 512 and writes default 32 on tested failures.

6,688 complete original color-parser cases and 7,388 complete original size-parser cases verify exact outputs, failure writes, guards and unchanged inputs. Tests execute actual original libc strncmp through the original thunk with original strings/table; no callees are modeled. Static caller linkage connects successful parses to color/size state tokens and closing tokens to their resets. A separate 10,240-case original control-state test verifies selected token transitions, packed state bits and unwinding. Full markup integration, font lookup and visible rendering remain unresolved.

Full cold backup, isolated trial, promotion and independent reopening verify both names/signatures and unchanged original instructions/archives. Totals: 334 checked names (304 renames, 29 created functions and one retained-name review), 1,767 mapped and 7,813 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved text control and bounded prefix helpers

Applied ApplyTextControlToken, UnwindTextStateMask and TryConsumeTextLiteralPrefix with working signatures. The control handler updates selected text-state fields and reports whether its caller should consume the token. The unwinding helper steps through a packed depth/mask until it finds a saved bit, clears that bit and returns. The prefix helper advances a bounded cursor only when the literal fits and matches; an empty literal succeeds without advancement.

10,240 complete original control/unwinding cases verify the entire state buffer, return values and guards across 160 tokens and 64 state profiles. 1,812 complete original prefix cases verify exact cursor/input/literal guards using actual libc strlen/strncmp through original thunks, without models. Original table names and native hashes link clue, term and pink to numeric styles 2, 1 and 3; their visual meanings remain unresolved. Color/size tag linkage identifies some fields, while others remain opaque. Whole markup parsing, font lookup and visible rendering are not verified.

Full cold backup, isolated trial, promotion and independent reopening verify all three names/signatures and unchanged original instructions/archives. Totals: 337 checked names (307 renames, 29 created functions and one retained-name review), 1,770 mapped and 7,810 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved initialized text icon and emoji lookup helpers

Applied SortTextNameHashRecords, GetTextIconCodepointByHash, GetTrenIconCodepointByHash and ResolveTextEmojiAlias. Original startup code builds sorted name-hash/source-record indices from immutable source tables. The general/Tren helpers resolve bounded hash queries to mapped values. The alias resolver supports primary/fallback/special tables and numeric or named skin-tone suffixes; failure may still update the tone and class outputs.

1,152 complete sorter cases verify unsigned order and full-record preservation using the actual original memmove implementation and jump table. The bounded original startup window rebuilds 3,513 records across nine groups in three fill-pattern runs. All 1,566 general/Tren source lookups, selected absent hashes and length limits pass on those constructed indices. The alias resolver passes 6,016 plain-name and 80,592 suffix cases with exact outputs and unchanged guarded inputs/tables. An additional original startup sorter is required to initialize the special tone-eligibility table before lookup. Original hash, sort, strings, tables and libc dependencies execute without modeled callees.

These checks verify CPU table construction and lookup. The huge startup owner, whole markup pipeline, font/glyph availability and visible rendering remain unverified. Equal-key sort stability and invalid-pointer safety are not claimed. The working 32-bit tone-output type preserves its all-ones sentinel; original source signedness is not recovered.

Full cold backup, isolated trial, promotion and independent reopening verify all four names/signatures and unchanged original instructions/archives. Totals: 341 checked names (311 renames, 29 created functions and one retained-name review), 1,774 mapped and 7,806 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved text flag-alias fallback and connected token checks

Applied TryResolveTextFlagAlias with working bounded start/end, output-pointer and Boolean return arguments. It searches the initialized flag-prefixed and short country-code tables, each with 254 original records and separate length limits. Success writes the executable-specific flag identifier; miss preserves the output. 2,300 original-native direct cases cover all 508 source names plus unknown, empty and overlength inputs. Another 2,032 complete original base-parser cases confirm the flag token, payload and cursor advancement.

The connected colon-alias path also passes 16,276 successful plain/toned cases with exact tokens, payload/style fields and guarded state. Selected unknown/empty/malformed-colon sequences pass 288 runs comprising 5,340 decoded units: they remain literal and advance character by character. These checks use original startup-built indices, original hash/sort/parser/helper bodies and actual library dependencies without models. They do not verify arbitrary markup, Unicode composition, glyph/font availability or visible rendering.

Full cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 342 checked names (312 renames, 29 created functions and one retained-name review), 1,775 mapped and 7,805 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved button-label span parser

Applied TryFindTextButtonLabelSpan with working byte-pointer start/end in/out arguments and Boolean return. It recognizes the exact button opening prefix, advances the label start, and scans with the original escaped text decoder until a raw closing quote/greater-than pair. A matched prefix still advances start if the closing delimiter is missing. Escaped or hex-decoded quotes do not close the span.

Original-native checks cover 48 basic and 88 selected escaped/malformed/NUL cases. Another 64 connected parser sequences comprising 352 calls verify the opening token, label characters, queued closing token, delimiter skipping, exact guarded state and control-handler return. These checks use original code, initialized tables and actual library dependencies. Selected color/size/named-style paths also passed 432 connected checks; closing size tags accept size-prefixed trailing text, while closing color tags require whole-name equality. Arbitrary nested markup and visible rendering remain unverified.

Cold backup, isolated trial, promotion and independent reopening verify the saved change and unchanged original instructions/archives. Totals: 343 checked names (313 renames, 29 created functions and one retained-name review), 1,776 mapped and 7,804 unmapped among 9,580 discovered functions. This is partial semantic analysis, not whole-game completion.

### Button labels through the higher-level text parser

The higher-level parser and all eight directly referenced direction/marker helpers were read alongside the existing base parser. Its 1,269 instruction spans match the original executable. Selected native checks now cover 128 ASCII button-label sequences (768 wrapper calls) and 32 mixed Hebrew-label/ASCII-suffix sequences (272 calls), with exact output tokens, cursor positions and guarded state before and after the original control handler. Original code, initialized lookup tables, Unicode data and actual library dependencies are used.

The wrapper can emit an initial direction token without consuming input. The caller must apply that token before requesting the next unit; the original text emitter does so and stores the previous token before handling it. The selected Hebrew label is preserved between the button tokens, then the following ASCII character receives direction-transition tokens. A preliminary fixture that omitted control application repeated the initial token; this was a fixture caller omission, not a game stall.

These are selected path checks. General bidirectional text, Arabic shaping, nested markup, markdown and visible rendering remain unverified. No additional function names or whole-function completion credit were added.

### Saved initial text-direction lookup

Applied FindInitialTextDirection with working current-unit, bounded next-byte/end, opaque parser-state arguments and unsigned-byte result. The original Unicode-property category selects left-to-right or right-to-left immediately for strong characters. Otherwise the helper copies 80 bytes of parser state and scans subsequent decoded units, applying controls to the copy. Exhaustion returns unknown; caller state remains unchanged. A special raw direction-control path is also present.

262,160 original-native cases cover every codepoint in the executable property-table range plus eight outside values across two state profiles. Another 72 selected lookahead cases cover neutral prefixes, ASCII, Hebrew, Arabic, tags, button labels and raw direction controls. Exact results, guarded caller state, inputs, initialized indices, source pages and canary were checked using original code/data and actual library dependencies. These checks do not establish modern Unicode conformance, arbitrary markup/escape/malformed behavior or visible bidirectional rendering.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 344 checked names (314 renames, 29 created functions and one retained-name review), 1,777 mapped and 7,803 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved packed text-direction and transition helpers

Applied ResolvePackedTextDirection, SelectTextDirectionTransitionToken and SelectTextDirectionExitToken with working scalar/state arguments. Packed current direction takes priority over fallback, with a supplied default used when both packed words are negative. The transition selector emits a token only when the requested direction differs. The exit selector chooses a token for the opposite effective direction. Both selectors update only the direction-category byte; the caller applies the returned control token.

The complete original bodies total 189 instructions. Native checks cover 40,896 guarded state profiles: 204,480 resolution calls, 204,480 transition calls and 40,896 exit calls. Profiles exercise depth boundaries, low masks, negative sentinels, fallback words, state masks, modes and pointer alignment. These synthetic combinations are not all proven reachable during gameplay. The first exit-token oracle incorrectly assumed same-direction restoration; the failing native case and original assembly corrected that interpretation before the full checks passed.

Cold backup, corrected isolated trial, promotion and independent reopening verify the saved names/signatures and unchanged original instructions/archives. Totals: 347 checked names (317 renames, 29 created functions and one retained-name review), 1,780 mapped and 7,800 unmapped among 9,580 discovered functions. Whole bidirectional parsing, visible rendering and whole-game completion remain unverified.

### Direction-class lookahead and percent-placeholder dependency

The 68-instruction direction-class lookahead uses an 80-byte copy of parser state and skips executable property category 7, which includes ASCII number/currency/percent terminators such as #, $ and %. Ordinary spaces are not skipped by this rule. It returns the next low-nibble property category, byte 255 on exhaustion, or zero for special queued output or decoded units outside its table range.

262,176 native cases compare it with direct traversal of the original base parser and original property data: all encoded codepoints in the table domain, two outside values, 14 selected strings and two alignments. Exact byte results, whole guarded caller state, input/index/source pages and canary were checked. This comparison shares the original parser/data and therefore is not independent Unicode-standard validation; supplied encodings may also be transformed by the decoder.

Expanding beyond the earlier selected button paths reached a percent-placeholder dependency missing from that fixture. The original 42-, 164- and 120-instruction helper chain was captured, read and byte-matched, then loaded with actual library dependencies and original constants. It recognizes percent tokens and parses placeholder/format options; it is not a Unicode-composition helper. No game defect is inferred from the incomplete-fixture failure. No additional checked-name or whole-parser completion credit is added.

### Saved placeholder token, format and span helpers

Applied ParseTextPlaceholderFormatOptions, TryParseTextPlaceholderToken and TryFindTextPlaceholderSpan with working bounded cursor/output arguments. The option parser recognizes flags once in the order #, +, 0, stores width and precision in bytes, and consumes supported type characters without storing them. Decimal width/precision wrap modulo 256; star stores 255. A dot without digits advances the cursor without setting precision.

Numbered placeholders begin with 1 through 9 and accumulate subsequent digits modulo 32 bits. Named bracket placeholders store a name hash, relative source offset and byte length, with optional colon-separated format options. Literal percent has its own record kind; the span checker accepts numbered, named and general-format kinds while excluding literal percent. Failure can change token-parser outputs, while the span checker preserves its output on failure.

The complete original bodies total 326 instructions. Native checks cover 63,168 option cases, 16,416 token cases and 16,416 span cases, with exact descriptors, cursor/span outputs and guards. Original code, hash, library dependencies and constants are used. Substitution values, final formatted output and visible localization/rendering remain unverified.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged original instructions/archives. Totals: 350 checked names (320 renames, 29 created functions and one retained-name review), 1,783 mapped and 7,797 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Placeholder spans through both text parsers

Connected checks now trace recognized placeholder spans through the complete original base and higher-level text parsers. The base parser records the span end in state and marks subsequent decoded units inside that span as special output. The higher parser returns those units without normal markup/direction interpretation. Selected angle-tag and colon-alias text inside placeholders therefore remains literal. At the recorded end, the span clears and a boundary byte marks the first following decoded unit.

552 base-parser sequences passed 3,032 calls; 2,176 higher-parser sequences passed 12,000 calls across four flag profiles and four alignments. Exact units, cursors, flags and whole guarded state were checked, along with original input/source/index pages and canary. The higher-parser fixture mirrors the original emitter previous-token store and control-handler ordering.

These checks cover selected ASCII forms, with higher-parser cases starting in left-to-right mode. Escaping, Unicode, right-to-left text, nested malformed placeholders, substitution values and final formatted rendering remain unresolved. No new checked-name or whole-parser completion credit was added.

### Placeholder consumers, direction estimation and locale fallback

Two additional callers were traced. One counts strong left-to-right and right-to-left text units while skipping recognized placeholders. Another stores/deduplicates text content and builds 16-byte literal/placeholder records in chunked buffers, adding mode and direction flags. This builder prepares records for later use; it is not the final substitution routine.

The complete original 150-instruction direction estimator passed 8,928 native cases covering 1,089 ASCII/Hebrew count combinations plus selected placeholders, tags and neutral text, two controlled locale values and four alignments. Right-to-left wins only when its strong-unit count exceeds left-to-right; ties choose left-to-right. Letters inside selected placeholder names do not count. Inputs, original source/index data and canary were checked, and the fixture locale global was restored.

For zero strong-unit counts, the estimator compares the active locale hash against the original native hash of ar. A bounded startup trace shows the language-code table containing ar, hashing the selected locale and its prefix before a hyphen, then checking localization files and assigning fallback locale hashes. This resolves the earlier unknown comparison as an Arabic-locale fallback in this executable; live locale selection was not tested.

1,240 original instruction spans were byte-matched across the two callers, slash-reference helper and bounded startup window. The 600-instruction record builder and 404-instruction slash helper remain statically traced, with allocator/dedup/reference dependencies unresolved. Final substitution, broad bidirectional behavior and rendering remain unverified. No checked-name or whole-function completion credit was added.

### Saved shared byte-hash helper used by text records

Applied HashBytesMurmur3X64_128 with working input pointer, 64-bit byte count, 32-bit seed and two-word output arguments. Its complete 148-instruction body, constants, block/tail rotations and final mix match the [primary MurmurHash3 x64/128 reference](https://github.com/aappleby/smhasher/blob/master/src/MurmurHash3.cpp). This is algorithm identification, not recovery of the game source declaration.

21,363 original-native cases match an independent arithmetic implementation for lengths 0 through 256 and selected block/page boundaries through 8,192 bytes, four patterns, five seeds, four alignments and three null-input/zero-length cases. Both output words, input/output guards and original source/index data were checked. The executable uses a 64-bit length argument, so it is not asserted to have the exact reference API.

There are 758 static call references. The text-record builder passes seed zero and stores the first 64-bit output word as its content deduplication key. This does not establish collision-free identity, complete builder behavior or final substitution. Its copy/allocation dependencies remain to be tested. Original import-loader bindings and libc export symbols resolve these as memcpy, bcmp and operator new; bcmp is a bounded byte comparison rather than a string comparison.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 351 checked names (321 renames, 29 created functions and one retained-name review), 1,784 mapped and 7,796 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Text-record builder: bounded native execution

The complete original 600-instruction builder now executes against preallocated guarded record/index/link arrays and content/token chunks, with original hash, parser/control and memcpy dependencies. 64 input profiles passed 248 calls covering insertion, repeated nonempty key/content, conflicting-key rejection, duplicate-content reuse and capacity-zero rejection. Exact raw content, hash/index records, 16-byte placeholder/literal tokens, link metadata, counters and whole guarded buffers were checked.

Different keys with identical content reuse stored text and token data while cloning the link with an updated placeholder-base count. Empty insertion behaves differently: it leaves the record hash word untouched. Another 40 profiles and 80 calls show repeated empty-key lookup succeeding when that preexisting word is zero and rejecting for the tested nonzero words, without further mutation. This corrects the initial test expectation that every repeated empty key would succeed. These are synthetic storage states; allocator initialization and in-game reachability remain unverified, so no observed game defect is claimed.

Allocation/chunk growth, external comparison-table and whitelist paths, hash collisions, broader formats, final substitution and rendering remain unresolved. The original byte-comparison import is resolved but its external-table caller path was not exercised here. No new checked-name or whole-function completion credit was added.

### Saved text and placeholder-record builder

Applied TryStoreTextAndPlaceholderRecords with working opaque builder-context, 64-bit key and bounded text arguments. Its complete 600-instruction body stores/reuses content and optional placeholder records, checks an optional whitelist and external key/offset/length table, and maintains hash/index/link metadata. The descriptive name identifies its role; it does not mean every execution path is verified.

In addition to the previous 248 bounded and 80 empty-storage calls, 4,800 cases now exercise the original external-table and whitelist branches with the actual bcmp routine. Existing external text requires matching key, length and every byte, including bytes after embedded zeroes; a match succeeds without local insertion even at capacity zero. A nonnull empty whitelist rejects, while an absent whitelist or matching entry permits lookup. Whole guarded context, local/external buffers, inputs and original source/index data were checked.

Allocation/chunk growth, virtual allocator, hash collisions, broader formats and final substitution/rendering remain unresolved. The preseeded empty-hash finding remains a synthetic-storage observation, not a verified in-game defect.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 352 checked names (322 renames, 29 created functions and one retained-name review), 1,785 mapped and 7,795 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Allocation boundary and the text-record caller

The builder grows content in 4,096-byte payload chunks and tokens in 256-record chunks. Both use 4,120-byte blocks including headers and counters, allocated through operator new or the allocator object first virtual entry. Original library windows trace operator new through a configurable allocation dispatch: zero-size requests normalize to one, failed allocations consult a new-handler and retry or enter an allocation-exception path. The default malloc dispatch reaches a heap delegate whose initialization remains unresolved. File-backed initial dispatch pointers are not proof of live runtime targets; this allocation path has not been executed.

A 150-instruction caller selects direct storage or text-representation conversion based on modes zero/one and a leading control byte. Forty-four native checks verify its direct/guard paths using original builder/hash/copy/strlen dependencies: null source and invalid modes leave the builder unchanged, automatic end stops at the first zero byte, and an explicit bounded range preserves embedded zeroes. Whole guarded caller/builder contexts, arrays/chunks, inputs and original source/index data were checked.

The conversion helpers, temporary heap allocation, chunk growth, virtual allocator and final substitution/rendering remain unresolved. No new checked-name or whole-function completion credit was added.

### Saved internal text-stream size and writer

Applied ComputeInternalTextStreamSize and WriteInternalTextStream with working bounded text/cursor arguments and opaque parser state. The forward writer emits an internal stream beginning with control byte 0x0E for nonempty output, then encoded text/control units, escape markers and payloads. It applies controls and commits cursors after complete units. The size helper follows the same parser/control pipeline without writing output.

840 native capacity checks cover 21 selected plain, Hebrew, tag, alias, placeholder and escaped inputs, every capacity from zero through required size plus two, and four alignments. Selected measured sizes match actual byte counts; known empty/ASCII/Hebrew byte vectors also match. Short buffers return failure without writing past the supplied end, but partial writes and state changes are possible, so failure is not claimed atomic.

Another 168 connected original-caller cases verify that mode-zero conversion stores the encoded bytes, length and hash through the record builder. They cover explicit/automatic input ends and the stack temporary-buffer path. Expected bytes come from prior direct-converter checks, not an independent full format specification. Optional marker insertion, broader control/Unicode/RTL cases, reverse conversion, heap temporaries, final substitution and rendering remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged original instructions/archives. Totals: 354 checked names (324 renames, 29 created functions and one retained-name review), 1,787 mapped and 7,793 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Internal stream decoding and packed payloads

The original 577-instruction internal decoder and its 211-instruction packed-payload reader were read and matched to original bytes. The payload reader reconstructs a 32-bit value from four encoded byte-plus-one units. It passed 16,384 valid cases spanning every byte value in each lane, plus 544 selected truncation cases. Earlier-unit truncation fails without changing caller output/cursor; a truncated fourth two-byte unit can instead succeed with a replacement-derived high byte. This is bounded native behavior, not a verified in-game defect.

Eighty-four stream comparisons across 21 previously encoded inputs and four alignments checked 308 units. Tokens, their defined payloads and escape flags match the original source parser. Full metadata equality does not hold: source lookahead can populate unused payload scratch fields early, and presentation metadata differs for some generated controls and literal placeholder characters. The checks record 20 unused-payload and 36 presentation-metadata differences rather than claiming full state or rendering equivalence. Initial broad-equality assertions were narrowed only after reviewing what the original writer actually encodes, with all differences retained as evidence.

The readable-markup reverse writer and its additional formatting/alias dependencies remain unverified. Malformed decoder inputs are not comprehensively covered, and final substitution/rendering remains unresolved. No additional checked-name or whole-function completion credit was added.

### Selected reverse conversion to readable markup

The original reverse writer and size calculator now execute selected paths with the original encoded decoder, packed-payload and glyph-expansion helpers, actual strlen/strncpy/memchr bodies and original data. 1,056 capacity checks cover 16 selected forward streams, two output flag settings, every capacity from zero through required size plus two, and four alignments. Selected measured sizes match written bytes; known empty/ASCII/Hebrew output vectors match. Named styles, buttons and emphasis reconstruct readable markup, and flag eight selects emphasis tags instead of asterisks. Short-buffer checks verify writes stay within the supplied end without claiming failure atomicity.

A separate 7,068-case check verifies the alias-format helper with three strings and optional tone suffix. It checks total capacity before writing, preserves cursor/output on the tested failures, and writes a raw low-byte tone character rather than validating a digit range. These checks use actual original strlen and strncpy.

The first named-style reverse test exposed a missing fixture pointer table. The original three style records and pointers were read and explicitly relocated, then the source baseline was updated before checks passed. This was an incomplete fixture dependency, not a game failure. Formatted color/size output and emoji/flag aliases still need additional formatting/table coverage. Exact original markup restoration, final rendering/substitution and whole reverse-converter completion are not claimed. No checked-name credit was added.

### Saved packed-payload reader and bounded alias appender

Applied TryReadInternalTextPackedPayload and AppendTextAliasWithOptionalTone with working bounded cursor/output arguments and signed tone code. The payload reader reconstructs four encoded byte-plus-one units into a 32-bit value; its documented fourth-unit truncation behavior remains explicit. The alias appender joins prefix/name/suffix with an optional tone suffix and checks total capacity before writing. It does not validate arbitrary nonnegative tone codes.

Evidence includes 16,384 valid packed-payload cases, 544 selected truncation cases and 7,068 alias-format cases with exact bytes, returns, cursors and guards, using original instructions/data and actual library dependencies. The original snprintf export and bounded-output callback were also traced into their formatting engine. That trace is static: color/size formatting coverage is not claimed, and no host-formatting substitute was used.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged original instructions/archives. Totals: 356 checked names (326 renames, 29 created functions and one retained-name review), 1,789 mapped and 7,791 unmapped among 9,580 discovered functions. Broader reverse conversion, rendering, final substitution and whole-game completion remain unresolved.

### Saved canonical and alternate emoji display lookup

Applied SortEmojiCanonicalNameIndex, SortEmojiAliasNameIndex and FindEmojiDisplayStringByName with working bounded index/name arguments. The lookup searches the canonical table for a display-string pointer, then searches the alternate table and resolves its canonical-name hash if needed. The alternate record own display pointer is not returned directly by this helper.

The original bounded startup window builds 2,553 canonical and 1,344 alternate records using the original strlen, name hash and two sort bodies. Three executions with different padding values verify all hash/source pairs, sorted keys, padding and preservation of older indices/source data. The two 571-instruction sort bodies match the previously reviewed name-hash sort after normalizing only local instruction addresses. No host-sorted replacement was used.

15,654 native lookup checks cover all 3,897 source names at four alignments plus unknown/empty cases, verifying exact returned pointers and guards. Arbitrary hash collisions, unbounded input, complete reverse formatting and rendering remain unverified.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged original instructions/archives. Totals: 359 checked names (329 renames, 29 created functions and one retained-name review), 1,792 mapped and 7,788 unmapped among 9,580 discovered functions. Whole-game completion is not inferred.

### Saved special emoji output helpers

Applied ComputeSpecialEmojiOutputSize and TryWriteSpecialEmojiOutput with working ID, mode, tone and bounded-output arguments. Missing display lookup returns success without output; unknown IDs fail and have size zero. Nonnegative tone uses the low byte of tone plus one.

All 135 source IDs and 14 selected signed tones were tested: 186,320 named/untone cases and 79,436 display cases across bounded capacities and four alignments. Exact bytes, cursors, guards, indices, source data and canary were checked. The original snprintf %s_tone%c path passed 2,548 separate cases, without a host formatter. Display expectations share the separately checked original lookup. Other formatting conversions and the full reverse text pipeline remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged original instructions/archives. Totals: 361 checked names (331 renames, 29 created functions and one retained-name review), 1,794 mapped and 7,786 unmapped among 9,580 discovered functions. This is not whole-game completion.

### Saved internal text to readable markup conversion

Applied ComputeReadableTextFromInternalSize and TryWriteReadableTextFromInternal with bounded input/output arguments and opaque parser state. The functions decode internal tokens, count or emit readable text and markup, and apply state controls. Their output can normalize the input; it is not guaranteed to reproduce original source markup.

Native checks cover 1,056 basic capacity cases, 440,264 special-emoji capacity cases (6,480 complete streams), and 5,584 cases across all 21 existing forward-generated streams and eight flag settings. The original integer formatter passed 49,032 separate cases. Successful bytes, sizes, cursors and state agree; buffer, input, source, index and canary checks pass. Most normalized-output expectations share a full-capacity native baseline or separately checked helper, rather than an independent complete specification.

Selected tests cover text, styles, buttons, placeholders, escapes, color, size and emoji/flag output. Malformed streams, all token/flag combinations, substitution and rendering remain unresolved. Short-buffer failures can leave partial writes or state changes; atomic failure is not claimed.

Cold backup, isolated trial, promotion and independent reopening verify saved names/signatures and unchanged instructions/archives. Totals: 363 checked names (333 renames, 29 created functions and one retained-name review), 1,796 mapped and 7,784 unmapped among 9,580 discovered functions. No whole-game completion percentage is inferred.

### Saved mode-selected text conversion and storage caller

Applied StoreTextRecordInSelectedRepresentation with an opaque mode context, record key and bounded text arguments. Mode zero stores internal text; mode one stores readable text. Matching input representation is stored directly, otherwise the appropriate size and writer helpers convert it before the record builder runs. Null end uses strlen; null source and unsupported modes return without storage. The function returns no success status and ignores the builder result.

Native checks cover 44 direct/guard cases, 168 forward cases, 168 reverse cases and 144 ASCII boundary cases through exactly 4,096 converted bytes. Whole guarded caller/context/record/index/content buffers, hashes, inputs, source indices and canary match expectations. Conversion expectations share earlier native converter vectors; boundary byte expectations are independent.

Both directions use the stack temporary through 4,096 bytes. The larger allocation/free branch was read but remains unexecuted. Chunk growth, placeholder parsing in the conversion integration, substitution and rendering remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 364 checked names (334 renames, 29 created functions and one retained-name review), 1,797 mapped and 7,783 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved keyed float-pair record storage

Applied StoreTextFloatPairRecords with mode, builder context, key, interleaved float-pair source and count arguments. The original caller stores these records alongside text. The helper filters keys, compares existing records, then stores a key/index/count record and copies eight bytes per pair into chunks of 256 entries. The application meaning of the pairs remains unresolved.

3,168 native storage/guard cases cover counts through 256, initial chunk usage, supported/unsupported modes, record capacities and four alignments. Another 1,920 cases cover existing records and key filters using an independent floating-point equality expectation. Positive and negative zero compare equal; identical quiet NaN bits do not. Whole guarded context, records, chunks, source and existing tables agree. Original memcpy is used.

Chunk growth and its allocator remain unexecuted. Malformed-table safety and floating-point exception flags are not claimed verified. Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives.

Totals: 365 checked names (335 renames, 29 created functions and one retained-name review), 1,798 mapped and 7,782 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved scratch arena allocation and connected chunk growth

Applied AllocateTextScratchBytes with an arena pointer, byte count and pointer return. When enough capacity remains, the original body returns the old cursor and advances it by exactly the request. Zero-sized requests and exact fits are accepted. This body does not round alignment or initialize the backing bytes. An out-of-space tail call exists but remains unexecuted.

3,192 native cases check requests through the text-builder object size, spare-capacity variations and four alignments, with exact return/cursor/whole guarded object and unchanged backing. Another 280 connected cases run the original float-pair storage helper and original arena allocator through virtual dispatch, growing through 1,024 pairs. Chunk links, logical base indices, used counts, pair bytes, record/context fields and allocator cursor agree exactly. The bounded backing storage supplies memory; no host allocator replaces the original arena method.

This supersedes the earlier untested-chunk-growth limitation for this arena-backed float-pair path. Original fallback/OS heap allocation, failure handling, malformed arenas and the application meaning of the pairs remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original instructions/archives. Totals: 366 checked names (336 renames, 29 created functions and one retained-name review), 1,799 mapped and 7,781 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Verified content and placeholder-token chunk growth

The original text builder now passes 104 content-growth cases through 16,384 bytes and 104 token-growth cases through 1,024 numbered placeholders. Both use the original arena method through virtual dispatch, original memcpy and original hash/parser bodies. Content chunks hold 4,096 bytes; token chunks hold 256 sixteen-byte descriptors. Exact guarded old/new chunks, links, logical offsets, used counts, record/index/link fields, hashes, parameter counts, arena cursor and inputs agree.

This supersedes earlier unexecuted-growth limitations for these arena-backed paths. The scratch allocator fallback import is identified as malloc by its loader NID and matching original libc export. Its deeper heap implementation and allocation failures remain unexecuted. Token-growth coverage uses repeated numbered placeholders; other token kinds, final substitution and rendering remain unresolved.

No new naming credit is added: 366 names checked among 9,580 discovered functions. These tests do not establish whole-game completion.

### Verified locale-aware float-pair lookup

Traced a 145-instruction runtime getter that searches linked records by masked key and locale. 9,240 native direct-lookup cases cover record counts through 127, empty leading blocks, every stored key and misses, pair flags, high key bits and locale choices. Exact returned begin/end pointers, record-use flag and whole guarded nodes/source/output agree. A direct record with pairs is marked used; a matching record without pairs returns an empty span.

396 additional cases verify the serialized locale fallback across empty and populated language views and key tables. When the requested locale has no direct record, the getter can use the default-locale record to reach the requested serialized view, match a secondary key, and compute an eight-byte-pair span. That path does not mark the direct registry record used. A matching direct record without pairs suppresses fallback.

The getter and ordered-boundary setters connect these pairs to editable ranges, but their units and application meaning remain unverified. Concurrency, malformed offsets and rendering are unresolved. The two-register aggregate return must be represented correctly in the saved ABI before applying a function name/type. No naming credit is added; the total remains 366 checked names.

### Saved locale-aware text float-pair span getter

Applied FindTextFloatPairSpan with a text key, locale hash and a reviewed sixteen-byte result containing begin/end float pointers. Explicit custom return storage represents the observed begin pointer in RAX and end pointer in RDX, with eight-byte fields at offsets zero and eight. Independent reopening verifies the structure layout, parameter registers, return registers and saved descriptive name. The decompiler now returns named span fields without introducing a hidden output argument.

The earlier 9,240 direct lookup cases and 396 serialized locale fallback cases support this role. Matching direct pair records are marked used; serialized fallback resolves secondary keys in locale views without that mark. Pair units/application meaning, concurrency, malformed tables, substitution and rendering remain unresolved. The explicit aggregate model is a working interpretation of the machine ABI, not a recovered original source declaration.

Cold backup, isolated trial, promotion and independent reopening verify unchanged original instructions and archives. Totals: 367 checked names (337 renames, 29 created functions and one retained-name review), 1,800 mapped and 7,780 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved text range copy and extension

Applied CopyOrExtendTextFloatRanges with a target extent, desired range count and record pointer. The helper copies existing eight-byte pairs, then fills missing ranges using a 0.25 gap and default width of 2, or an adjusted width based on the target extent. It redirects the record to pooled storage and updates its count and chunk bookkeeping.

960 native cases cover requested counts through 256, four existing counts, five initial chunk usages and six finite extents. An independent float32 oracle checks exact whole chunks, record, source, globals and guards, including walking existing linked chunks when the current chunk cannot fit the whole array. Pool reuse and new allocation remain unexecuted.

A higher consumer selects the first inclusive range containing an input value before selecting text. Its bounded caller converts an unsigned counter to float and divides it by the original constant 1,000. This supports a time-scaled interpretation but does not establish the source counter units or prove a specific caption/subtitle feature. The large owner did not decompile within the configured limit; a bounded 54-instruction caller window was captured and original-byte checked instead.

Cold backup, isolated trial, promotion and independent reopening verify the name, mixed float/integer arguments and unchanged instructions/archives. Totals: 368 checked names (338 renames, 29 created functions and one retained-name review), 1,801 mapped and 7,779 unmapped among 9,580 discovered functions. NaN/overflow/invalid counts, concurrency, substitution and rendering remain unresolved.

### Identified video playback clock behind text ranges

The previously opaque counter is populated from sceAvPlayerCurrentTime. Original worker instructions preserve that return value, store it in the current player object, and the captured text-selection caller reads the same field, converts the unsigned value to float, divides by 1,000, and calls the range-based text selector. Imports in the same worker identify sceAvPlayerInitEx, GetVideoDataEx, IsActive and source loading. 965 captured instruction spans across the relevant helpers and caller window match the original executable.

The [primary shadPS4 API implementation](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/avplayer/avplayer.cpp) corroborates the import NIDs. Its [source implementation](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/avplayer/avplayer_source.cpp) returns milliseconds for CurrentTime, supporting seconds after the native division. This is emulator-source corroboration of the game dataflow, not Sony source or a live Dreams playback test.

This advances the earlier unknown-counter finding to video playback timing used for text selection. It supports a video-timed text interpretation of this consumer; it does not prove all float-pair uses are captions or establish rendering correctness. The larger UI owner remains only partly captured. No new naming credit is added; 368 function names remain checked.

### Saved playback-time text range selection

Applied SelectTextRangeAtPlaybackTime with playback seconds, an opaque output context and text-key pointer. The caller clock is traced to AVPlayerCurrentTime divided by 1,000. The selector publishes the associated whole text span and a selected range index; it does not itself extract a substring for that range.

The corrected native fixture passes 4,608 cached-path cases across empty, adjacent and overlapping ranges, first/middle/last key positions, missing keys/text, high key bits, finite/NaN/infinite values and four actual buffer alignments. An independent first-inclusive-range expectation verifies whole output, input, tables, blobs and guards. Shared endpoints and overlaps choose the first matching range. A gap sets the index to FFFFFFFF without publishing text. Missing cached keys leave the index unchanged while setting the state field; a zero low-56-bit key leaves output unchanged. The initial fixture was superseded after its alignment/key-position coverage was corrected; only the corrected result is counted here.

Dynamic registry/lock/fallback branches and owned-buffer freeing remain unexecuted. This is not a live AV playback or caption-rendering test. Cold backup, isolated trial, promotion and independent reopening verify saved name/types and unchanged instructions/archives.

Totals: 369 checked names (339 renames, 29 created functions and one retained-name review), 1,802 mapped and 7,778 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved text selection context copy and span ownership

Applied CopyTextSelectionContext with destination/source context pointers. It copies the text key, range index, state, ready flag and C-string storage. If a ready span points to the source own string, it rebases that span to the destination copied string and computes its end. Otherwise it preserves the borrowed begin/end pointers. It does not extract a substring using the selected index.

1,536 native cases cover string lengths zero through 47, inline and borrowed external strings, ready/unready states, own/borrowed spans and four actual alignments. The original 80-instruction copy and 82-instruction string-storage helper run with actual strlen and memcpy. Exact whole guarded source, destination, backing string and canary match expectations. Destination heap freeing/new allocation and malformed pointers remain unexecuted.

The video UI copies the selected context before calling its display interface, whose implementation stores a copied context in the display object. This traces the handoff but does not verify live caption rendering. Cold backup, isolated trial, promotion and independent reopening verify saved name/types and unchanged instructions/archives.

Totals: 370 checked names (340 renames, 29 created functions and one retained-name review), 1,803 mapped and 7,777 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved attached-display text selection handoff

Applied SetAttachedTextSelection and ClearAttachedTextSelection with an opaque adapter and source-selection argument for the setter. The original file vtable and video UI calls identify these set/clear methods. An attached object receives a copied selection context; own ready spans rebase to its text storage. Clearing resets the key, span, state and ready flag, with FFFFFFFF as the range index. A null attached object makes both methods no-ops.

384 native calls execute the complete 46/36-instruction methods, original context copy/string-storage helpers and actual strlen/memcpy. Cases cover six string lengths through 47, ready/unready contexts, own/borrowed spans, attached/null objects and four actual alignments. Whole guarded object, adapter, source, text backing and canary match exactly.

Heap-owned destination freeing/new allocation, runtime vtable overrides, drawing, layout and substitution remain unverified. Cold backup, isolated trial, promotion and independent reopening verify saved names/types and unchanged instructions/archives. Totals: 372 checked names (342 renames, 29 created functions and one retained-name review), 1,805 mapped and 7,775 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Saved indexed nonempty text-segment extraction

Applied TryFindNonemptyTextSegment with begin/end outputs, bounded input, signed segment index, separator token and parser-state pointer. The seventh argument is verified on the SysV stack. The helper uses the higher or internal decoder, applies control tokens, skips empty segments and returns a raw byte span excluding the separator. Its body snapshots the state at a segment start and restores it for later layout on success.

1,008 native cases cover twelve plain UTF8 forms, three separators, seven signed indices and four alignments. An independent split/nonempty-segment expectation checks 160 successful byte spans; input, output and state guards pass. Negative and out-of-range indices fail for these finite inputs. Returned parser state is captured but not independently modeled; formatted/internal streams and failure atomicity remain unverified.

Traced the stored display selection into a 285-instruction consumer, then a large dispatch and a 161-instruction layout wrapper. That wrapper reads the selected index and invokes this segment extractor unless an alternate flag selects another path. The larger dispatch has 11,236 defined instructions and did not decompile within the configured limit; its native body was captured without treating extraction as understanding. Alternate extraction, actual layout and rendering remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify saved name/types and unchanged instructions/archives. Totals: 373 checked names (343 renames, 29 created functions and one retained-name review), 1,806 mapped and 7,774 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Verified formatting state at a selected segment start

Twenty native cases cover clue, term, pink, size and color markup spanning a newline, at four input alignments. Exact second-segment offsets and independently expected style/size/color fields agree. The returned span contains the selected text but excludes trailing closing tags that only change control state. The returned parser state retains formatting active before that selected text, even though the extractor subsequently encountered the closing tag.

This resolves the selected-field part of the earlier formatting-state question. It does not independently verify the entire parser state, nested or malformed tags, internal streams, alternate extraction, layout or rendering. No new naming credit is added; 373 names remain checked.

### Saved text-layout unit iterator

Applied AdvanceTextLayoutUnit with an opaque iterator pointer and Boolean result. It applies and skips formatting controls before returning the next decoded unit, tracks the previous unit and cursor, and stores a classification flag from the original property table. End-of-input clears the current unit and flag. A terminal soft hyphen becomes a dash; a middle soft hyphen is retained.

44 native profiles with 136 calls cover eleven known UTF8 forms at four alignments, including ASCII, newline, embedded NUL, Hebrew, emoji, soft hyphens and style/size/color markup. Expected codepoints are independent; classification expectations use original table bytes. Exact current/previous units, flag, selected formatting fields and input/iterator guards agree.

The alternate indexed extraction path uses this iterator and additional font/layout helpers. Its state-construction and metrics functions were read, but font metrics, shaping, alternate extraction, actual layout and rendering remain unexecuted. Internal streams, nesting and malformed UTF8 need further coverage.

Cold backup, isolated trial, promotion and independent reopening verify saved name/types and unchanged instructions/archives. Totals: 374 checked names (344 renames, 29 created functions and one retained-name review), 1,807 mapped and 7,773 unmapped among 9,580 discovered functions. No whole-game completion is inferred.

### Verified text-layout iterator initialization

384 native integration profiles run the original iterator initializer, direction probe and previously checked advance helper. Eight plain/internal forms, two locale settings, two flag settings, three optional-state profiles and four alignments agree with manually prepared iterator state followed by the original advance helper. Whole iterator, source, supplied-state guards and canary agree.

Initialization installs bounded input, preserves a supplied nonzero direction, applies the flag bit, chooses Arabic RTL or default LTR for unknown initial direction, and primes the first non-control unit. Without supplied state, eight padding bytes remain unwritten; the expected state retains their original poison values. The integration expectation shares original direction/advance helpers and is not an independent complete iterator specification. Font metrics, shaping, layout and rendering remain unexecuted. No new naming credit is added; 374 names remain checked.

### Saved font data loader

Applied LoadFontDataFromFile with opaque font-object and already-open file pointers. It retains the file handle, links the font into the runtime list, initializes glyph worker managers when needed, and loads packed FNTD font tables. The loader accepts versions 1 through 8. Version 7 uses a 48-byte header; packed 14-byte primary and 22-byte secondary records expand backwards into 48-byte runtime records with resolved record links.

All 540 original instruction spans match. Import resolution confirms fopen, fread and C++ operator new[]; the allocator is not malloc. All twelve local version-7 assets agree with the table read order and bounds, covering 137,235 primary and 6,415 secondary records. Checked same-array links and primary-to-secondary references are within bounds.

This is static loader and asset-structure evidence. The loader, worker threads, glyph payload decoding, shaping and rendering have not been executed. The inspected path does not check fread return counts; valid asset checks do not establish malformed-input safety. Raw assets and code remain local.

Cold backup, isolated trial, promotion and independent reopening verify the saved name and signature, unchanged instruction bytes and unchanged original archives. Totals: 375 checked names, 1,808 mapped and 7,772 unmapped functions among 9,580 discovered functions. These counts do not measure whole-game completion.

### Saved font glyph lookup

Applied FindFontGlyphRecord with a reviewed 16-byte return type containing the selected font pointer and glyph index. Assembly and native execution confirm the two fields return in RAX and RDX. This corrects the incomplete pointer-only interpretation of related callers; their other behavior remains under investigation.

The lookup uses each word's lower 16 bits as a presence mask and upper 16 bits as a base index, adding the rank of lower present bits. Mode zero selects the first font containing the codepoint, even without runtime records. Nonzero modes skip missing records: low mode byte 2 prefers the packed record class at or above 0x10000000, while other low bytes prefer below it. If no preferred match exists, the first eligible font is returned. No match returns both fields zero.

The original 105-instruction helper passed 1,245,220 mode-zero checks covering every codepoint in all twelve original asset lookup planes plus out-of-range sentinels. Another 21,868 calls cover 3,124 exhaustive ordered lists of zero through four fonts, five availability/record states, four object alignments and seven modes. Return fields, output guards and unchanged input objects/tables agree. These tests use synthesized runtime objects with original lookup data; they do not execute the original loader or rendering.

Cold backup, isolated trial, promotion and independent reopening verify the saved name, signature, aggregate field layout and custom register return storage. Original instruction bytes and archives remain unchanged. Totals: 376 checked names, 1,809 mapped and 7,771 unmapped functions among 9,580 discovered functions. Whole-game completion, malformed-input safety, shaping, metrics and rendering remain unproven.

### Saved codepoint remapping and glyph-record lookup

Applied RemapTextCodepointForFont and FindTextGlyphRecordData with reviewed SysV signatures. The remapper normalizes null, control 0x1A and nonbreaking space to space, maps selected internal tokens to glyph codepoints, and uses a property-gated 420-pair table when the low direction-flag byte is nonzero. Quote controls 2 and 3 combine that raw byte with the respective quote codepoint using OR and XOR. Property-gated results use sixteen bits.

The glyph helper resolves direction from the first nonnegative override at state offsets 0x48 and 0x14, otherwise from the fallback direction byte. It remaps the codepoint, then searches fonts using the bitmap/rank index. It returns a pointer 24 bytes into the selected 48-byte runtime record. Unlike the preference lookup, this helper stops at the first font containing the mapped codepoint: if that font has no runtime record array, it returns null rather than continuing to later fonts.

The original remapper passed 262,307 checks. The original glyph helper and remapper together passed 2,490,440 checks over all twelve original asset lookup planes in two fallback directions, plus 48,960 corrected checks across 6,120 direction/list/alignment profiles. Exact pointers, guards and unchanged inputs agree. The initial direction fixture incorrectly represented an empty list; its failure was preserved, corrected and excluded from passing counts.

All 159 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify both saved names and signatures, unchanged instructions and unchanged archives. Runtime arrays are synthesized and property expectations use original tables. Loader execution, glyph payloads, metrics, shaping and rendering remain unverified. Totals: 378 checked names, 1,811 mapped and 7,769 unmapped functions among 9,580 discovered functions; these are not whole-game completion percentages.

### Saved glyph advance calculation

Applied ComputeTextGlyphAdvance with a float return in XMM0 and three reviewed SysV pointer parameters: iterator, layout context and glyph record data. The iterator classification flag can force zero advance. Normal glyph width uses a signed 16-bit field divided by 64, multiplied by one plus a packed nine-bit field divided by 255, then by the layout scale. An optional multiplier excludes codepoints with property bit 0x40; tabs still use it.

Tabs look up the space glyph and multiply its advance by four. The fixed-width digit option uses 96; control 0x1A uses the exact stored float 41.60000228881836; internal token 0xFDDB has zero width. These are measured layout units, not screen pixels or an assertion about all text behavior.

All 92 original instruction spans match. The original function, original glyph lookup and original remapper passed 15,360 finite-input checks with bit-exact binary32 results and unchanged input buffers. The arithmetic oracle follows assembly operation order. Its first version rounded decimal 41.6 differently from the game's stored constant; that mismatch was documented, corrected and excluded from passing counts.

Cold backup, isolated trial, promotion and independent reopening verify saved name, parameter storage and float return, unchanged instructions and unchanged original archives. Synthetic records and original property tables support these checks; NaN, infinity, denormal behavior, original loader execution, full layout, shaping and rendering remain unverified. Totals: 379 checked names, 1,812 mapped and 7,768 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved text-unit font and glyph selector

Applied SelectFontGlyphForTextUnit with the reviewed two-field DreamsFontGlyphRecord return: font pointer in RAX and glyph index in RDX. Ordinary codepoints are remapped for direction and passed to the preference lookup using the parser's selection mode. A fresh decompilation of the position/selection caller now consumes explicit font and glyph_index fields before passing glyph data to ComputeTextGlyphAdvance.

All six special-token branches were read and exercised. FDD8 and FDDA search eight-byte key/index records; FDDA rejects keys at or above 676. FDD9 and FDE1 search 24-byte records containing a key and five indices, accepting variant values 0x30 through 0x34. FDD1 remaps a payload codepoint and searches the supplied font set; FDE9 searches the global font list. Both prefer the first record below the packed-class threshold 0x10000000, otherwise the first eligible record above it. Missing runtime record arrays are skipped in these two branches.

The original selector passed 1,800 ordinary-character checks over twelve original lookup tables, 46,080 auxiliary-key/variant checks and 4,992 payload routing/preference checks. Tests exercise the original selector, dispatch table, remapper and preference helper with exact font/index results and unchanged guarded inputs. Runtime objects are synthesized; this does not execute the original loader, full glyph payload decoding, complete layout, shaping or rendering.

All 380 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify the saved name, field layout, custom return registers and signature, with unchanged instructions and original archives. Totals: 380 checked names, 1,813 mapped and 7,767 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved layout style refresh and span selection step

Applied RefreshTextLayoutStyle and StepTextLayoutSpanSelection with reviewed SysV signatures. Style refresh derives scale, selects a font, and computes the current color. Style factors, explicit size, fixed color modes, font overrides and highlighting were checked in 80,640 cases with exact guarded context results. Another 7,168 packed-color cases execute the original libc powf: RGB bytes normalize and use exponent approximately 2.2, while alpha stays linear. Independent numerical expectations differ by at most two float ULP for RGB; alpha is exact.

The span step selects glyph data, calculates advance and updates cursor and indexed selection state. It saves the start token and first 80 parser-state bytes on entering the selected segment. Formfeed advances the segment immediately; newline and NEL count toward a configured limit. Reaching the next segment records the end token and returns true. Right-to-left cursor movement occurs before selection; left-to-right movement occurs afterward unless the span completes. Classified units do not move the cursor. These behaviors passed 5,760 exact whole-state checks.

An additional 4,096 integration cases force a formatting-cache mismatch through the original span caller. It copies twelve style bytes, runs the original refresh function, then uses the refreshed font and scale in original glyph selection and advance. Exact context, descriptor, cursor and parser snapshot results agree. Nonzero packed color is checked separately rather than in this integration; full iterator-loop behavior and rendering remain unverified.

All 278 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify names, signatures and unchanged instructions/archives. Synthetic bounded runtime objects support the tests; original loader execution, full glyph payloads, complete layout, shaping and rendering remain unfinished. Totals: 382 checked names, 1,815 mapped and 7,765 unmapped functions among 9,580 discovered functions. These are not whole-game completion percentages.

### Saved next-line layout driver

Applied TryLayoutNextTextLine with a float width limit, iterator/result/context pointers, an integer ellipsis policy and a Boolean result. It uses the original 31-class break transition table, refreshes formatting, selects glyph metrics, and saves parser/cursor/dimension checkpoints for rollback when a line exceeds the limit.

Independent fixed-width ASCII checks cover hard wrapping and explicit newlines (8,432 calls, 656 text/width cases), space-based rollback (4,744 calls, 568 cases), and ellipsis reservation (1,300 calls, 325 cases). Exact line widths, heights, counts, next codepoints and byte or null cursors agree at four actual input alignments, with guarded inputs/iterator/output and the original stack canary intact. The original driver executes the original decoder, iterator and linked font/layout helpers.

The driver accepts at least one ordinary character even at a zero limit. Trailing newline does not create an additional result. Space rollback can consume separating spaces while restoring dimensions from the preceding non-space checkpoint; a leading-space-only checkpoint can have zero height. Final-line ellipsis reservation can restore a prefix or default checkpoint without advancing input, so the caller controls continuation. This helper reports visible width and truncation; its caller handles the ellipsis contribution to aggregate dimensions.

Fixture and oracle corrections are recorded locally and failed attempts are excluded. All 794 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify the saved name, mixed float/integer SysV signature, Boolean return and unchanged instructions/archives. Synthetic fixed-width glyphs limit these results: Unicode breaking, variable metrics, direction mixing, markup integration, ellipsis-space interaction, full layout, shaping and rendering remain unfinished.

Totals: 383 checked names, 1,816 mapped and 7,764 unmapped functions among 9,580 discovered functions. These counts do not establish whole-game completion.

### Saved aggregate text dimension measurement

Applied MeasureTextLayoutDimensions with a reviewed DreamsTextDimensions return structure: width and height are two binary32 fields in the low 64 bits of XMM0. This replaces the earlier integer-return interpretation. Parameters cover width limit, input begin/end, layout context, unit limit, optional parser state and line limit, with reviewed SysV register storage.

The original function initializes an iterator and repeatedly invokes TryLayoutNextTextLine. It takes the maximum line width and sums heights with binary32 rounding and configured spacing. The unit limit is checked after an entire line and before the final ellipsis adjustment. When the last permitted line truncates, the ellipsis advance is added to the aggregate maximum width only if the restored iterator has a nonzero current codepoint. A default checkpoint can suppress that adjustment. Adding to an earlier wider line's aggregate maximum can produce a result wider than the requested width limit.

17,680 native calls across 4,420 fixed-width single-word profiles match independent exact dimension expectations for width, unit and line limits and a controlled positive ellipsis width. Four actual input alignments agree; guarded source, parser state and output remain intact, as does the original stack canary. Tests execute the original aggregate caller, iterator initializer, line driver and linked layout helpers. An initial oracle omitted the restored-codepoint gate; its correction is preserved locally and the failed attempt is excluded.

All 119 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify the saved name, eight-byte field layout, custom XMM0 return storage and all parameters, with unchanged instructions and original archives. Synthetic fixed-width glyphs limit the result: spaces/newline aggregation, spacing variants, optional null parser state, Unicode layout, mixed directions, shaping and rendering remain unfinished.

Totals: 384 checked names, 1,817 mapped and 7,763 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved directional text layout step

Applied TryStepDirectionalTextLayout with iterator, layout-context and unit-descriptor pointers, an outer-direction Boolean and a Boolean result. It copies the iterator, measures a directional run, then replays its snapshot through StepTextLayoutSpanSelection or a recursive call for a different direction. Early selected-span completion propagates true. Its recursive call now decompiles with an explicit Boolean result.

Native checks cover 80 fixed-width ASCII runs, 192 Latin/Hebrew runs and 256 newline-separated selected-span completion cases. They execute the original decoder, iterator, font/glyph selector, refresh, advance and span step. Independent cursor/EOF/snapshot or selected start/end expectations agree at four actual input alignments, with guards and the original stack canary intact. Iterator observations confirm that Latin units resolve left-to-right despite a right-to-left fallback; an early-completion oracle initially confused those and was corrected without crediting the failed attempt.

The mixed-text checks do not independently instrument exact recursive branch coverage. The descriptor includes a temporary local-iterator pointer, which tests do not dereference after return or treat as persistent output. Fixed-width synthetic glyphs limit these findings; complete layout, shaping and rendering remain unverified.

All 227 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify the saved name and signature, unchanged instructions and unchanged original archives. Totals: 385 checked names, 1,818 mapped and 7,762 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved text prefix scanner

Applied TryScanTextPrefixToStopUnit with a Boolean result and nine reviewed SysV arguments, including three stack parameters. It snapshots the first 80 parser-state bytes, decodes units and applies controls until a selected non-control stop unit or input end. The stop unit is excluded from the prefix but consumed from the cursor and optionally reported. Nonempty input can return an empty prefix at a leading stop; empty input returns false.

384 plain UTF8 checks cover twelve forms, four stop lists, four actual input alignments and optional stop output. Another 40 checks cover two consecutive scans of five known style/size/color forms across newline. Independent byte spans, cursor and stop values, exact entry snapshots and known active format fields agree with the original scanner/decoder/control helpers; guarded inputs/state and the original stack canary remain intact. Active formatting survives the consumed newline and enters the next snapshot. The following visible tail excludes trailing closing markup while the cursor consumes it to input end.

All 201 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify name, signature and unchanged instructions/archives. Nesting, malformed markup, internal streams, failure atomicity, the complete text processor, layout and rendering remain unverified. Totals: 386 checked names, 1,819 mapped and 7,761 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved string storage and insertion helpers

Applied PrepareTextStringStorage and InsertTextStringSpan with reviewed SysV signatures. These reusable string helpers are called by the text processor; this mapping does not imply they are exclusive to text layout. Storage preparation selects inline or existing external storage and writes the requested terminator. Negative signed lengths clamp to zero. Insertion reads the existing C-string length, shifts its suffix with memmove, copies the bounded payload and writes the new terminator.

The original storage helper passed 2,056 checks covering inline lengths 0–255, two negative patterns and borrowed external lengths 256–511 within capacity 512, at four actual alignments. The original insertion helper passed 17,112 checks using the original libc strlen, memmove and memcpy, with every insertion position in short strings and selected positions near larger inline boundaries. Bounded payloads include embedded NUL and later bytes. Returned pointers and whole guarded records/backing/input bytes match independent expectations.

Another 2,048 direct-copy integration checks execute the original record builder, storage helper and memcpy for every explicit length 0–255, two payload profiles and four alignments. Exact payload, terminator, record fields, input guards and stack canary agree. Owned-buffer release, heap growth/failure, extreme lengths, external insertion ownership, invalid positions and source aliasing remain untested. Complete text processing, layout and rendering remain unfinished.

All 177 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify both names/signatures and unchanged instructions/archives. Totals: 388 checked names, 1,821 mapped and 7,759 unmapped functions among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved text record construction and processing

Applied BuildTextLayoutRecord and ProcessTextLayoutTokens with independently reopened SysV signatures. The builder takes a floating width limit plus eleven integer/pointer arguments, initializes the layout record, and either copies an explicit byte span directly or processes text through the token scanner. It also contains auxiliary-record transfer/merge paths. The processor scans spans, dispatches selected tokens and inserts replacement text.

Original code passed 4,032 initialization checks, 2,048 explicit direct-copy checks, 128 plain-text builder integration checks and 88 plain processor checks. Whole guarded output records, inputs, optional parser states and argument buffers agree with independent expectations. Plain cases include ASCII, newlines, Hebrew and inline boundary lengths. These checks execute the original decoder, scanner and string/libc helpers where called; the token dispatcher is exercised only on its no-selected-token path.

Special substitutions, direction-marker replacement, auxiliary-record merging, heap growth and full game rendering remain unverified. All 859 original instruction spans match, both saved names/signatures survive independent reopening, and original archives remain unchanged. Totals: 390 checked names, 1,823 mapped and 7,757 unmapped among 9,580 discovered functions. This is bounded analysis progress, not whole-game completion.

### Saved text layout iterator initialization

Applied InitializeTextLayoutIterator with a reviewed five-argument SysV signature. It installs a bounded input span, uses either default parser state or a supplied 80-byte state, resolves direction when unset, optionally enables a parser flag, and primes the first visible unit while applying control tokens. Measurement initializes its iterator through this helper before laying out lines.

All 149 original instruction spans match. Assembly confirms destination,begin,end,byte flag and optional state arguments. Default-state stores leave eight padding bytes untouched; the observed behavior is preserved rather than treating the object as wholly zero-initialized. Nonzero supplied direction survives; unknown direction uses the original probe and locale fallback.

The original initializer passed 1152 bounded integration profiles covering eight plain/internal forms,three locale values,three flag values,four optional-state profiles including supplied zero direction and four alignments. Whole iterator bytes,input and supplied state,guards and stack canary agree. The oracle shares the separately checked original direction probe and advancement helpers,so this is not an independent specification of the entire iterator. Malformed streams,full shaping/rendering and in-game behavior remain unresolved.

Cold backup,isolated trial,promotion and independent reopening verify the saved name/signature and unchanged original archives. Totals: 391 checked names,1,824 mapped and7,756 unmapped among9,580 discovered functions;these are not whole-game completion percentages.

### Token processing: auxiliary records and replacement spans

Direct execution now covers selected branches beyond plain-text passthrough. Token 0xFDDF appends a 32-byte auxiliary record when the list has spare capacity: bytes 0–24 become zero, bytes 25–27 remain untouched, and the type field at byte 28 becomes 4. The list count increases, the dispatcher returns false, and the replacement span remains unchanged. Thirty-two checks cover eight insertion positions and four record alignments with exact whole-buffer, list, context, span and canary expectations. The meaning of type 4 remains unknown; allocation and full-capacity paths were not executed.

A separate 100-instruction helper replaces the context string and returns its begin/end span. A nonzero flag surrounds the input with the UTF-8 encodings of U+FDE2 and U+FDE3; zero copies plain text. All 3,000 checks passed for inline lengths 0–249, three flag values and four alignments, executing original string and libc dependencies. Whole guarded context, source and returned span agree with independent expectations. Release of owned old storage, external sources and heap growth remain untested. The internal markers' meaning has not yet been established.

These results do not verify the complete dispatcher, account-dependent substitutions, rendering or in-game behavior. No new names or completion credit are added for partially covered dispatcher behavior. Raw instructions and fixtures remain local.

### Saved replacement-span and auxiliary-record helpers

Applied SetTextReplacementSpan and AppendTextAuxiliaryRecord after inspecting their complete bodies and token dispatcher callers. Both use reviewed SysV signatures. The replacement helper resets the context string and returns its bounded span, optionally surrounding text with internal U+FDE2/U+FDE3 markers. The append helper copies one 32-byte auxiliary record and increases the vector count. Its growth path selects the larger of double capacity and count plus one, requests 16-byte-aligned storage, copies prior records and releases old backing unless it is inline. Allocation failure leaves the count unchanged; this path is static evidence only.

The original replacement helper passed 3,000 inline checks, and the original append helper passed 512 checks across sixteen insertion positions,four alignments and eight full-record payloads. Whole guarded backing,list,context,source and span expectations agree,with stack canaries preserved. Growth/free/failure,external replacement sources and owned old-string release remain unexecuted. Internal marker and auxiliary payload meanings remain partly unresolved.

All 176 original instruction spans match. Cold backup,isolated trial,promotion and independent reopening verify both saved names/signatures and unchanged original archives. Totals: 393 checked names,1,826 mapped and7,754 unmapped among9,580 discovered functions. These are descriptive-role checks rather than complete game behavior or whole-game completion.

### Token reader capacity and acceptance behavior

The 211-instruction reader decodes text, applies control state, asks a virtual predicate whether to accept each unit, and re-encodes accepted units as UTF-8. Its username-like predicate accepts ASCII letters, digits, hyphen and underscore. A separate hash-delimited predicate rejects hash and selected property-table classes. Original vtable entries resolve to local callback code; the callbacks currently lack Ghidra function definitions, so no recovered function boundary or saved name is claimed for them yet.

In 1,920 bounded native checks, 1,712 succeeded and 208 intentionally exceeded capacity. Success writes a terminator, returns the byte count and commits the accepted cursor/parser state. A rejected unit remains unconsumed. Capacity failure returns false and leaves the caller's length, cursor and state unchanged, while any already-written output prefix remains and receives no new terminator. This distinction matters when interpreting callers that retry or discard partial results.

Checks use twelve valid plain-text forms, both original callbacks, capacities 1–20 and four alignments, with guarded buffers and canaries. Prefix bytes, UTF-8 re-encoding, capacity and cursor/length commit expectations are independently calculated. Hash classification uses original tables. Selected committed direction/emoji state expectations were corrected using observed probes and are not independent decoder verification. Initial fixture encoding and state-oracle failures receive no passing credit. Zero capacity, malformed UTF-8, formatting/internal streams and null-predicate failure remain unexecuted. No new naming or whole-game completion credit is added.

### Saved predicate-driven token reader

Applied TryReadAcceptedTextToken with a reviewed Boolean SysV signature: UTF-8 output, in/out capacity or length, input cursor span, parser state and acceptance predicate. All 211 original instruction spans match, and all three dispatcher callers inspect the low-byte Boolean result. This corrects the previously inferred wide return value without claiming the complete dispatcher is verified.

Alongside the 1,920 plain checks already reported, 192 formatted checks cover clue, size and packed-color tags, both original predicates, capacities 1–8 and four alignments. Of these, 120 succeed and 72 intentionally fail capacity. Opening markup changes accepted state and advances the committed input cursor even though output contains only text. Closing controls encountered before a rejected hash are speculative: the returned cursor/state remain before the closing tag. Capacity failure discards even opening-tag state changes while preserving any partial output bytes. Whole guarded state, output and cursor match explicit expectations.

Only three known flat formatting tags are covered. Malformed or nested markup, internal streams, zero capacity and null-predicate failure remain unexecuted. Plain hash classification uses original tables, and selected direction/emoji state expectations came from probes rather than independent decoder verification.

Cold backup, isolated trial, promotion and independent reopening verify the name/signature and unchanged archives. Totals: 394 checked names, 1,827 mapped and 7,753 unmapped among 9,580 discovered functions. Full game behavior and whole-game completion remain unproven.

### Bracketed-name substitution suppression

The original dispatcher's left-bracket branch looks ahead for @ followed by 3–16 accepted ASCII name characters and a right bracket. It records recognition in a context flag without consuming the caller's input or producing replacement text. The following @ dispatch clears that flag and returns without substitution. This provides a one-use suppression path for bracketed names; it does not establish the meaning or correctness of every other substitution form.

A 336-call check includes 208 bracket-recognition cases and 128 following-@ suppression calls. These cover name lengths 0–19, delimiter and punctuation variants, four alignments and both prior flag states. Original reader, name predicate, virtual cleanup and decoder/control code execute. Whole guarded context, input span, parser state and replacement output remain as independently expected. The earlier standalone 208-case receipt overlaps this check and is not additional unique coverage.

Another 112 checks execute the original text processor with the dispatcher and its dependencies: valid bracketed names of lengths 3–16 remain literal with surrounding text, in both scanner-list modes and four alignments. Exact whole output, context and input agree; parser-state guards and canaries remain intact. Parser-state mutations are not independently modeled in full. Invalid-bracket integration, ordinary @ replacement, malformed/nested markup, external substitutions and rendering remain unverified. No new checked-name or whole-game completion credit is added.

### Ordinary at-name replacement boundaries

The original dispatcher now executes the ordinary @ replacement path with synthetic local text. Names of 3–16 accepted characters produce @name as the replacement span. With context flag 0x1000 clear, the helper surrounds it with internal U+FDE2/U+FDE3 markers; with that flag set, it returns the plain replacement. The semantic meaning of these markers remains unresolved.

Failure has two distinct cursor effects: accepted names shorter than three characters return false after consuming their accepted characters, while over-capacity names return false without committing cursor or parser state. This follows the reader's successful-read versus capacity-failure distinction and must be preserved when interpreting dispatcher callers.

All 160 bounded checks passed for lengths 0–19, two wrapper settings and four alignments, with exact whole context, cursor, parser state, replacement span, input guards and stack canary expectations. They execute the original dispatcher, reader, name predicate, virtual cleanup, replacement helper, insertion and libc functions. The bounded-length import was resolved through the original loader NID to strnlen and matched to the local libc's 34-byte export before execution.

This batch uses uppercase A names with an exclamation delimiter and disables the auxiliary list. It does not verify auxiliary append integration, all accepted name characters, the complete text processor, rendering or in-game behavior. No external service requests or account data are involved. No new names or whole-game completion credit are added.

### At-name processing with auxiliary records

Ordinary @name processing is now checked through the original text processor with auxiliary output enabled. It preserves surrounding text, inserts the replacement with optional U+FDE2/U+FDE3 wrappers, and appends one type-3 auxiliary record in both scanner modes. The record has a zero first eight-byte field, a 17-byte name area at offset 8 and type 3 at offset 28. Three intervening padding bytes are copied from a local stack record without an initialized-value guarantee in this branch; they are not treated as semantic payload.

The dispatcher/append combination passed 64 checks across boundary name lengths, wrapper settings, alignments and in-capacity list positions. Processor integration then passed 2,080 checks covering each of the 64 accepted ASCII characters repeated at lengths 3 and 16, plus two mixed names, both wrapper settings, both scanner modes and four alignments. The earlier 32-case processor receipt overlaps this expanded batch and is not additional unique coverage.

Independent expectations cover whole output, context, input and list state, plus auxiliary backing bytes except the three unspecified padding bytes. Parser-state guards and canaries remain intact; full parser-state mutations are not independently modeled. Auxiliary growth, arbitrary name combinations, malformed text, rendering and in-game behavior remain unverified. These are local synthetic-data checks with original code and dependencies; no external requests or account credentials are involved. No new checked names or whole-game completion credit is added.

### Hash-token substitution and scanner mode

The hash dispatcher branch accepts at least four bytes from its predicate-driven reader. It prefixes accepted text with the UTF-8 encoding of private-use glyph U+E474 and a space, then applies the optional U+FDE2/U+FDE3 wrapper policy. The private-use glyph's visual meaning remains unidentified. Short accepted text returns false after the reader advances, as distinct from reader capacity failure.

Original scanner tables explain a mode difference: the table selected by context flag 0x80 includes hash as a stop token, while the default table does not. Processor integration confirms that distinction. Default mode preserves the tested hash text literally; enabled mode inserts the glyph-prefixed replacement and appends a type-2 auxiliary record. The record zeroes bytes 0–24 and writes type 2 at offset 28; its three padding bytes remain outside semantic expectations.

The dispatcher passed 296 checks covering 37 accepted lengths from zero through selected inline boundaries up to 245, two wrapper settings and four alignments. Another 32 processor checks cover lengths 4 and 16, both wrapper settings, both scanner modes and four alignments, with auxiliary output enabled. Independent expectations cover complete output, context, cursor/list/input and defined auxiliary bytes. Parser-state guards and canaries remain intact; full processor parser-state mutations are not independently modeled.

These checks use repeated uppercase A text and bounded inline capacity. Other accepted characters, capacity growth, malformed text, rendering and game runtime remain unresolved. The complete dispatcher is still unfinished, so no new name or whole-game completion credit is added.

### Slash substitution key parsing

The slash branch calls a parser for a 15-character typed key: one allowed type letter followed by fourteen lowercase hexadecimal characters. The seven decoded bytes form a 56-bit numeric value packed above the type byte. An all-zero numeric value normalizes the complete key to zero. Static prefix-mask decoding identifies exactly thirty accepted letters: CDMOPTUVabcdeghijkmopqrstuvwxz. Their individual semantic meanings remain unresolved.

The original seven-byte hex decoder passed 15,360 checks: 256 payload patterns plus every possible byte at each of the fourteen input positions, in four alignments. Only digits and lowercase a–f are accepted. A bad pair returns false, retaining earlier completed output bytes and leaving the current and later output bytes untouched. There is no input-length parameter; this helper assumes fourteen readable bytes.

The enclosing 404-instruction parser passed 740 checks covering all 52 letter prefixes, three hex patterns, fourteen invalid-hex positions, fifteen truncated lengths and four alignments. Failure preserves the caller cursor and parser state. After collecting fifteen ASCII units it clears the output key before validating the prefix and hex; on truncation the output remains untouched. Success commits the parsed cursor and state. Packed-key, acceptance, cursor and guard expectations are independently calculated. One decoder-state byte for digits was corrected from observed probes, so these checks do not independently specify the complete decoder state.

Formatting, nesting, non-ASCII units, trailing input, type-specific substitutions and rendering remain unverified. No new saved names or whole-game completion credit is added. All fixtures and raw code remain local.

### Saved typed-key parsing helpers

Applied TryDecodeSevenBytesLowerHex and TryParseTextTypedKey with reviewed Boolean SysV signatures. All 583 original instruction spans match. The hex helper takes a seven-byte output and fourteen readable input characters; the parser takes a 64-bit key output, cursor span and opaque parser state. Complete bodies and the slash dispatcher caller were read at assembly level. The hex helper has nineteen entry references and is shared beyond text; its subsystem mapping records observed text use rather than exclusivity.

The saved comments preserve the independently tested behavior: lowercase-only hex, partial output on hex failure, thirty accepted type prefixes, packed 56-bit numeric value plus type byte, all-zero normalization and distinct output-versus-cursor effects on parser failure. Evidence includes 15,360 hex checks and 740 parser checks. The selected digit-state expectation came from a probe rather than an independent decoder specification; formatting, non-ASCII, trailing input and type-specific substitutions remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify both names/signatures, unchanged instructions and original archives. Totals: 396 checked names, 1,829 mapped and 7,751 unmapped among 9,580 discovered functions. No full dispatcher, rendering or whole-game completion is claimed.

### Typed-key formatting and trailing-input commit

Another 216 checks execute the original typed-key parser with clue, size and packed-color tags inserted before the key or at two positions within it. They cover a valid key, an invalid type prefix and invalid hex, with two trailing suffixes and four alignments. Seventy-two valid cases succeed; the other 144 are expected validation failures.

Success skips the opening formatting controls, commits their state effects and stops after exactly fifteen visible ASCII units. The closing tag and any trailing text remain unconsumed. Invalid prefix or hex clears the key output but rolls back the complete caller cursor and parser state, including speculative formatting changes. Exact packed key, cursor, whole guarded state/output/input and canary expectations agree.

These checks cover three known flat tags and selected insertion points, not nesting, malformed markup, non-ASCII input or full slash substitution. The previously saved comments' formatting limitation describes their earlier checkpoint; this later evidence extends it only to the cases listed here. No additional checked names or whole-game completion credit is added.

### Reference-aware text direction by majority

The inspected 150-instruction scanner counts two directional character classes and chooses the low-byte result from their majority. Latin/Hebrew checks confirm left-to-right on ties containing strong characters. Locale fallback is used only when neither directional class contributes. Successfully parsed slash typed keys are skipped; an invalid type prefix leaves its letters available to influence the result.

All 2,456 bounded checks passed across Latin/Hebrew counts 0–12 and selected boundaries 255, 256, 257 and 300, valid/invalid references, two locale values and four alignments. Full-register checks confirm that only the low byte carries the direction: upper EAX bits can retain count data above that byte. Treating the complete register as a clean direction enum would therefore be unjustified without checking the caller.

Another 40 checks cover selected percent forms after Hebrew: accepted string, numeric and named placeholder forms are skipped, while unknown percent-q contributes its literal q. These use original scanner, placeholder/key parsers and decoder/control dependencies. Input guards and canaries agree. A failed fixture transformation removed setup before native scanner execution; it was corrected, preserved locally and receives no passing credit.

Arabic and other scripts, formatting/nested or malformed streams, complete placeholder grammar and game rendering remain unverified. Caller interpretation and saved naming are still pending, so no new checked-name or whole-game completion credit is added.

### Saved reference-aware directional majority scanner

Applied ChooseTextDirectionByVisibleMajority with two bounded text pointers and an unsigned-byte SysV return. The comment-cache caller compares AL with 3 and stores the result as its RTL flag at record offset 0x3A. This confirms that upper EAX count bits are not part of the direction result and supports correcting the earlier wide inferred return type.

All 150 original instruction spans match. Evidence includes the complete scanner and 115-instruction caller, 2,456 majority/reference/locale checks and 40 selected placeholder checks. The saved comment records majority selection, ties, fallback only with no counted strong characters, skipped typed references and selected placeholder kinds. Arabic and other scripts, formatting or malformed streams and full placeholder grammar remain unresolved.

Cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged original archives. Totals: 397 checked names, 1,830 mapped and 7,750 unmapped among 9,580 discovered functions. No full rendering or whole-game completion is claimed.

### Directional majority counts decoded and shaped units

The majority scanner counts units returned by the higher text decoder, not raw Unicode input characters. The distinction is observable with Arabic lam-alef: in the tested isolated contexts, two input letters produce one U+FEFB presentation-form unit. One Latin A plus one lam-alef cluster therefore ties and selects left-to-right. Earlier references to character counts should be read as decoded-unit counts; they do not establish raw input-character weighting.

The original ligature table contains the lam/alef pair and U+FEFB/U+FEFC form alternatives. Twenty original iterator calls across eight profiles confirm U+FEFB for isolated lam-alef and Latin followed by lam-alef. This supports the expected unit count rather than deriving it solely from the majority result.

Another 1,960 checks cover left/right unit counts 0–6, clue/size/packed-color flat tags, Arabic alef and space-separated lam-alef clusters, two locale values and four alignments. Known formatting tags add no directional weight, and selected Arabic clusters follow the decoded-unit majority/tie rules. Input guards and canaries remain intact. The preliminary fourteen-call observation probe is exploratory and receives no additional verification credit.

Other Arabic joining contexts, comprehensive shaping, nested or malformed tags and rendered glyphs remain unresolved. This extends the evidence for the existing saved direction function; it adds no checked names or whole-game completion credit.

### Slash dispatcher key-list and disabling boundaries

The slash dispatcher checks context flag 0x2000 and a fixed sixteen-entry parsed-key list before invoking the typed-key parser. With the flag set, it returns without parsing or mutation. Count 15 accepts one final key and becomes 16; count 16 rejects without changing the cursor, state or key list.

All 144 checks passed across an unhandled lowercase-e key, an all-zero normalized key and an invalid prefix, list counts 0/15/16, four flag combinations and four alignments. Original dispatcher, key parser, hex/visible-unit helpers, decoder/control, replacement and libc code execute. Independent whole context, key-array, cursor, state, output-span, input-guard and canary expectations agree.

The selected unhandled-type and zero-key paths store the parsed key and succeed with an empty replacement, optionally surrounded by internal wrappers. This is not evidence about a failed object lookup: object-resolving branches were not executed. Auxiliary records are disabled in this batch. Full processor integration, handled key types, rendering and game behavior remain unresolved. No checked names or whole-game completion credit is added.

### Display-name cleanup and 64-byte string helpers

The inspected display-name builder uses a 64-byte string representation with metadata at offset 0x3C. Its storage helper passed 520 checks covering inline lengths 0–63, two negative length patterns and borrowed external lengths 64–127 within capacity 128, at four alignments. Its insertion helper passed 17,112 bounded inline checks with original strlen, memmove and memcpy. These are separate original functions from the earlier 256-byte text helpers.

The original display-name builder then passed 76 integration checks across nineteen nonempty source forms and four alignments. It removes exact lowercase br/nl tags, literal backslash-n, UTF-8 U+0085, LF and CR. Uppercase or incomplete tags remain literal in the tested cases. Nonempty input containing only removed forms becomes empty without entering the empty-source fallback branch.

Whole guarded output, source object and input agree with expectations. The output is a C string: bytes beyond its new terminator can retain previous source data. An initial oracle omitted the first source copy and therefore predicted the wrong unused bytes; it was corrected to model the observed preparation/copy sequence and receives no passing credit. The helper does not clear the entire inline buffer.

Owned-buffer release, heap growth, fallback/localization, current-object special cases, null objects, complete slash object resolution and rendering remain unverified. No new names or whole-game completion credit is added. Raw code and fixtures remain local.

### Display-name fallback differs from preferred-name cleanup

When the preferred name is empty and a nonempty fallback is supplied, the original builder copies that fallback verbatim. Twenty checks cover ordinary text, a br tag, LF, UTF-8 NEL and the 63-byte inline boundary at four alignments. The tags and line-break bytes remain in the output. Preferred-name cleanup must therefore not be generalized to all output branches.

Another 76 checks exercise relative preferred-name storage inside the object rather than a name pointer. The nineteen source forms use a positive relative offset from the name field and four alignments. Cleanup, empty-after-cleanup behavior, whole guarded output and unchanged source object agree with the earlier pointer-backed cases.

This extends the prior fallback limitation only to nonempty supplied fallback text. Null or empty fallback still enters unresolved localization branches. Current-object special cases, heap growth, null objects, complete object resolution and rendering remain unverified. No checked names or whole-game completion credit is added.

### Saved small-string and display-name helpers

Applied PrepareSmallStringStorage, InsertSmallStringSpan and BuildObjectDisplayName with reviewed SysV signatures. All 418 original instruction spans match. The storage helper returns its selected character buffer and takes a signed length; insertion takes a signed position and bounded source span; the display builder takes output, object and optional fallback pointers. Opaque pointers avoid inventing a complete source structure.

The comments preserve 64-byte representation details, metadata at 0x3C, negative-length clamping, tested insertion behavior, preferred-name cleanup and verbatim nonempty fallback copying. Evidence includes 520 storage checks, 17,112 insertion checks and 172 display-builder integration checks across pointer-backed and relative preferred names plus supplied fallback. Old bytes may remain beyond the output terminator. The string helpers are shared beyond text; mapping records their observed display-name use rather than exclusivity.

Owned-buffer release, heap growth/failure, invalid insertion positions, source aliasing, localization/current-object special cases and null objects remain unexecuted. Cold backup, isolated trial, promotion and independent reopening verify all names/signatures and unchanged archives. Totals: 400 checked names, 1,833 mapped and 7,747 unmapped among 9,580 discovered functions. Full object resolution, rendering and whole-game completion remain unproven.

### Saved typed-reference object resolver adapter

Applied ResolveTextReferenceObject and corrected its inferred void return to an opaque object pointer. The 64-instruction adapter selects lookup paths using ordered-tree membership. One path initializes optional scope output and calls a cache lookup with scope -2; the other builds a key/options descriptor and calls a resolver that searches multiple scopes. Both callees return an object pointer or null in RAX, which the adapter preserves through its epilogue. The slash dispatcher tests that value and passes a returned object to BuildObjectDisplayName.

Evidence includes the complete adapter assembly, the 368- and 550-instruction callee bodies and their return paths, and the dispatcher caller. The five SysV arguments are a 64-bit reference key, status output, scope output, opaque lookup context and request-permission byte. Context and scope structures remain opaque because their complete layouts are not established.

This is static ABI and descriptive-role evidence. Runtime cache timing, thread checks, request queuing, pending states and complete object resolution have not been executed or verified. No new native lookup test count is claimed. All 64 original adapter spans match; cold backup, isolated trial, promotion and independent reopening verify the saved name/signature and unchanged archives. Totals: 401 checked names, 1,834 mapped and 7,746 unmapped among 9,580 discovered functions. Whole-game completion remains unproven.

### Object cache lookup and deferred queue comparison

Assembly review identifies a 4,096-entry object lookup table with 80-byte records and linear probing. Lookup compares a five-field identity tuple, stops at an empty first key field and handles raw status values separately. Some statuses return a cached record's object payload; others return metadata or defer/retry. Access-time updates, locale discrimination and request permission affect these paths. This is a partial reader-side layout, not a verified complete cache or status specification.

The deferred request path has a 128-entry queue of 32-byte key tuples. Its comparison loop overwrites the match flag for every entry and tests it only after the loop. A native check of the original contiguous comparison/append fragment passed 212 cases: a match in the last record suppresses append, while an earlier match followed by a different final record permits a duplicate append. Count 128 skips insertion; count 127 can fill the final slot.

The fixture executes the original 36-instruction fragment with relative branches intact and an appended fixture return. It compares whole guarded queue and descriptor buffers across counts 0–8, 127 and 128, match positions and four alignments. It deliberately bypasses locks, thread-ID updates, caller status and routing. These results prove the bounded fragment behavior, not an in-game concurrency bug, the complete deferred queue or external request behavior.

Kernel clock/thread execution, cache writers/invalidation, request routing and whole object resolution remain unresolved. No new checked names or whole-game completion credit is added; no external service requests were made.

### Deferred request consumer order and processing handoff

References to the deferred key array locate its consumer inside a larger worker routine. The consumer decrements the count and reads the previous final 32-byte record, so this path processes the newest queued tuple first. It does not clear the removed slot; the lowered count determines which records remain active.

All 192 bounded native dequeue checks passed across counts 1, 2, 3, 16, 127 and 128, eight record payload profiles and four output alignments. The original twelve-instruction nonempty fragment runs with its bytes and relative branch intact, an appended fixture return and a bridge that captures its output registers. Whole guarded queue and output records match independent expectations. The empty branch is deliberately excluded.

Surrounding original assembly releases the queue lock, rebuilds the same 32-byte tuple on the stack and calls the producer's request handler with processing mode 1. It then reacquires the lock before taking another key. This links deferred insertion to processing; the handoff and locks were read statically rather than executed in the fragment fixture. Request routing, timing, concurrent behavior and full worker execution remain unverified.

The earlier duplicate-append result should be understood alongside this newest-first consumer. Neither fragment alone establishes an in-game defect or the intended coalescing policy. No new checked names or whole-game completion credit is added, and no external request was executed.

### Saved shared object-cache lookup and key structure

Applied LookupCachedObjectOrRequest with a pointer return and an explicitly stored 32-byte DreamsObjectLookupKey value on the stack at offset +8. The key contains three 64-bit fields followed by two signed 32-bit fields. Field offsets and stack storage are independently checked after reopening. These are reviewed descriptive field roles, not recovered source declarations.

The complete 368-instruction body establishes exact identity comparison, a 4,096-entry 80-byte-record table, linear probing and separate raw-status paths. The resolver and worker linkages place this function in shared object-cache behavior; the map adds an Object cache group under shared object data. A new shared category avoids treating the whole cache as exclusive text-decoding code.

This checkpoint verifies static role, ABI and saved types. It does not execute the complete cache, kernel clock/thread dependencies, invalidation, concurrency or request routing. The previously tested queue fragments remain separately bounded evidence. All 368 original spans match; cold backup, isolated trial, promotion and independent reopening verify unchanged instructions and archives. Totals: 402 checked names, 1,835 mapped and 7,745 unmapped among 9,580 discovered functions. Whole-game completion remains unproven.

### Saved immediate/deferred object lookup handler

Applied ProcessOrDeferObjectLookup with an integer processing-mode argument, optional status output and the same 32-byte DreamsObjectLookupKey passed by value at stack offset +8. The processing branch changes a field in its local stack key copy; the typed signature avoids representing that as a mutation of a caller-owned key object. The handler returns an opaque pointer where its local construction path supplies one, otherwise null.

All 308 original instruction spans match. The complete handler assembly/decompilation and lookup-to-worker handoff establish its deferred queue versus processing branches. Evidence includes the separately bounded 212 comparison/append and 192 nonempty dequeue fragment checks; these do not execute the full handler, locks, thread/clock calls, local asset construction or request routing.

Cold backup, isolated trial, promotion and independent reopening verify the name, custom stack key storage, exact field layout and unchanged archives. Totals: 403 checked names, 1,836 mapped and 7,744 unmapped among 9,580 discovered functions. Full runtime handler behavior, concurrency and whole-game completion remain unproven.

### Saved shared object cache writer

Applied StoreObjectLookupResult with numeric status, payload begin/end, retry-counter reset flag, auxiliary flag, deadline seconds and the 32-byte DreamsObjectLookupKey passed by value. It handles both payload replacement and status-only updates, returning the stored payload pointer or null.

Read all 577 original instructions and the typed trial decompilation. Five selected caller windows add 358 byte-matched instruction spans and confirm mixed register/stack arguments. Their decoded deadline constants are all 600 seconds, added to current time; this is not proof that every caller uses that duration or that every cache read enforces expiry.

Cold backup, isolated trial, promotion and independent reopening verify the saved name, signature, key layout and unchanged archives. Full runtime writer behavior, all caller paths, object-type side effects, concurrency and eviction safety remain unresolved. Numeric status enum names are not recovered.

Totals: 404 checked names and 1,837 mapped functions among 9,580 discovered functions; 7,743 still need system mapping.

### Saved response-code cache update

Applied UpdateObjectCacheFromResponseCode with an integer response code, 32-byte by-value lookup key and void return. Its caller routes code 200 to a separate payload handler. This helper maps 404 to cache status 4 and 423 to status 7. For 503 or 524, a nonnull cached payload with zero auxiliary flag selects status 2, preserving that payload; otherwise 503 selects status 8 and 524 selects status 3. Other codes select status 3.

The writer receives an empty span, false retry-reset flag and a deadline of current time plus 600 seconds. Numeric status names and the concrete response type remain unresolved. The 66-case assembly-derived truth table is a model, not runtime validation.

All 80 original instruction spans match. Cold backup, isolated trial, promotion and independent reopening verify the name, signature, key layout and unchanged archives. Totals: 405 checked names and 1,838 mapped functions among 9,580 discovered functions; 7,742 still need system mapping.

### Saved structured-text member reader

Applied ReadStructuredTextMemberName with an opaque parser-state pointer and void return. It reads quoted or unquoted object member names, requires a colon and computes their name hash. These hashes feed response payload dispatch; they are member-name identifiers, not proven intrinsic runtime type IDs.

The original parser, quote scanner, whitespace helper and hash routine passed 1,296 selected checks: nine names, unquoted and both quote styles, selected whitespace and 16 alignments. Complete parser state, input, guards, spans, cursor and hash were compared. Separately, 144 original-hash checks confirmed candidate matches for player_identity, playeridentity, impcfg, version, dream, user, edit_rights, comment and photo. Hashes can collide, so those matches do not uniquely recover original type names.

All 144 original reader instructions match. Trial, promotion and independent reopen verify the saved name/signature and unchanged archives. Escapes, comments, malformed input, stream refill, arrays and the full payload parser remain unexecuted. Totals: 406 checked names and 1,839 mapped functions among 9,580 discovered functions; 7,741 still need system mapping.

### Saved object-response processing chain

Applied HandleObjectLookupResponse, QueueObjectResponseForProcessing and DispatchParsedObjectMemberToCache. The callback queues nonempty successful responses and delegates other response codes to cache-status handling. The queue builder copies identity pairs, retains the response owner and signals a worker. The dispatcher routes 13 serialized-member identifiers to shared cache writes or specialized helpers.

All 465 original instruction spans match. Trial decompilations, saved custom SysV interfaces and an independent reopen agree with the assembly. Complete callback/queue/dispatcher runtime behavior, delegated helper signatures, allocation failures and concurrency remain unresolved. Original archives remain unchanged.

The member-reader fixtures now cover 3,472 selected cases: 432 unquoted names, 864 quoted names, 448 escape/error cases and 1,728 comment cases. They compare complete state, input and guards. The reader hashes raw escaped member-name bytes; missing colons set an error and zero discriminator. Comment tests use the refill helper only while sufficient input remains. Actual stream refill, truncated inputs, arrays and the complete payload parser remain unexecuted. These checks add no function-name credit.

Totals: 409 checked names and 1,842 mapped functions among 9,580 discovered functions; 7,738 still need system mapping.

### Saved Dream-record normalization and cache handler

Applied NormalizeAndCacheDreamRecord with scope key/index, a mutable payload-span descriptor and auxiliary flag, returning the record key or zero. The parsed dream member dispatch selects this helper. It can copy and rebuild a payload, remap selected integer-array values, update record flags, accumulate three category maxima and write either a payload cache entry or status-only entry with a 600-second deadline.

The original diagnostic identifies a missing field at offset 0xc0 as an author. Other field names, account-slot interpretation and category meanings remain provisional. Copy/serialization helper signatures, category-table safety, NaN behavior, allocation failures and concurrency remain unresolved.

All 307 original instruction spans and the typed trial decompilation were read. Trial, promotion and independent reopening verify the saved name/signature and unchanged archives. The full handler has not been executed. Totals: 410 checked names and 1,843 mapped functions among 9,580 discovered functions; 7,737 still need system mapping.

### Saved Dream-record copy and owned-array cleanup

Applied CopyDreamRecord and ReleaseDreamRecordOwnedArrays. The copy helper transfers fixed fields through an observed extent of 0x358 bytes and reconstructs 18 array descriptors through byte copies or delegated element-copy helpers. The cleanup helper releases negative-marker owned arrays, including nested owned storage in two 96-byte-element arrays. It leaves descriptors unchanged; repeated cleanup is not established as safe.

All 508 original instruction spans and both typed trial decompilations were read. Trial, promotion and independent reopen verify the saved names/signatures and unchanged archives. Full copying, delegated deep-copy semantics, allocation failure and actual deallocator behavior remain unverified.

The original integer-remapping fragment passed 192 checks with its original lookup table and full input/guard comparisons. Separately, the entire cleanup body passed 88 ownership/order checks with the deallocator explicitly replaced by a recording stub. Those cleanup checks verify which pointers are passed in what order, not real allocation or freeing. Neither fixture proves the complete normalization handler.

Totals: 412 checked names and 1,845 mapped functions among 9,580 discovered functions; 7,735 still need system mapping.

### Saved nested-record array copy and reserve helpers

Applied ReserveNestedByteArrayRecords96 and CopyNestedByteArrayRecords96 with assembly-supported SysV arguments and boolean/void returns. These helpers operate on 96-byte records containing a nested byte-array descriptor. The reserve helper grows storage and relocates existing records. The element helper chooses copy direction by address order, copies defined fields and reconstructs nested arrays. The names describe the observed layout, not recovered source type names.

All 242 original instruction spans and both typed trial decompilations were read. Trial, promotion and independent reopening verify the names/signatures and unchanged archives. The element helper passed 144 original-code overlap/self-copy checks with empty nested arrays, comparing the complete buffer and guards without substituted calls.

Actual allocation/growth, nonempty nested payload copying, failure rollback and complete Dream-record copying remain unverified. The element helper does not release destination nested storage first, so a general assignment contract is not established. Totals: 414 checked names and 1,847 mapped functions among 9,580 discovered functions; 7,733 still need system mapping.

### Saved thermometer materializers

Applied MaterializeLightThermometerData and MaterializeThermometerEntry with seven assembly-supported SysV arguments, including the stack byte controlling selection. The light record contains Gameplay, Graphics and Audio float bits at offsets 0, 4 and 8. Each detailed thermometer entry contains type at offset 0 and amount float bits at offset 4. Original literal hashes and serializer dataflow support these labels.

All 571 original instruction spans and both typed trial decompilations were read. Trial, promotion and independent reopen verify names/signatures and unchanged archives. Both original bodies passed 672 checks with preexisting output: field-selection subsets, empty selection, force flags, alignments and exact bit patterns including NaNs, infinities and signed zero. These materializers copy values; they do not compute category maxima or clamp amounts.

Output allocation/growth/failure, large relative offsets and the full 5,503-instruction parent serializer remain unverified. Selected parent branches identify author at 0xc0, head version at 0xd0, thermometer entries at 0x248 and light thermometer data at 0x258; the whole parent is not counted as reviewed. Totals: 416 checked names and 1,849 mapped functions among 9,580 discovered functions; 7,731 still need system mapping.

### Typed thermometer input/output records

Saved working structures DreamsLightThermometerData (12 bytes: gameplay, graphics and audio floats at offsets 0, 4 and 8) and DreamsThermometerEntry (8 bytes: unsigned type at offset 0 and amount float at offset 4). Both materializers now use these types for input and output pointers. The custom SysV register/stack storage remains unchanged.

Independent reopening verified every field offset, width, record size and saved signature; original instruction bytes and archives match. These are descriptive layouts supported by the traced field names and existing bounded checks, not recovered source declarations. No function-name or runtime-coverage credit was added.

### Saved portal metadata materializer

Applied MaterializePortalRecord after reading all 423 original instructions, tracing the parent portals array, and verifying the saved name and seven-argument SysV layout after independent reopening. Each 96-byte record contains a portal-type byte, a name with inline or relative storage, a gadget-sequence value and raw angle bits. Angle units and type values remain unresolved. This is metadata processing, not proof that portal gameplay has been reconstructed.

The original helper passed 816 scalar-selection checks with explicit output and empty descriptor names. The original hash routine passed 80 checks for the five associated member and parent names. Nonempty names, inline empty names, null output, allocation/growth/failure and the full parent serializer remain untested. Original archives and instruction bytes are unchanged. Totals: 417 checked names and 1,850 mapped functions among 9,580 discovered functions; 7,730 still need system mapping. These counts are not a percentage of a completed PC port or of all Dreams behavior understood.

### Saved edit-rights metadata materializer

Applied MaterializeEditRightsMetadata after reading all 356 original instructions, tracing the nested Dream record and two additional caller windows, and independently reopening the saved name and seven-argument SysV layout. The 88-byte structure contains two rights bit fields and a signature string. The helper copies stored metadata; it does not generate or verify the signature. Bit meanings remain unresolved.

The original helper passed 432 scalar-selection checks with explicit output and empty signature descriptors. The original hash routine passed 64 checks for four associated field and parent names. Nonempty signatures, inline empty strings, null output and allocation/growth/failure remain untested. Original archives and instructions are unchanged. Totals: 418 checked names and 1,851 mapped functions among 9,580 discovered functions; 7,729 still need system mapping. These are bounded code-review counts, not whole-game completion.

### Saved collection-icon and Dream-version materializers

Applied MaterializeCollectionIconRecord and MaterializeDreamVersionInfo after reading and matching all 1,009 original instructions, reviewing trial decompilations and independently reopening the saved names and seven-argument SysV layouts. Collection icons contain a hash, type, color data, manual-icon flag and thing type. The 104-byte version record contains portal and collection-icon arrays, cover/audio hashes, thermometer values, visibility and rights fields. These are metadata layouts; their rendering or gameplay meaning is not fully recovered.

The original collection-icon helper passed 1,188 explicit-output checks. Original version-info and light-thermometer helpers passed 648 checks with empty arrays and preallocated output; seven field/parent names passed 112 original hash checks. Nonempty arrays and strings, null output, allocation/growth/failure and large offsets remain untested. The full parent serializer has now been read and byte-matched, but has not been executed as a whole and is not counted as semantically complete.

Totals: 420 checked names and 1,853 mapped functions among 9,580 discovered functions; 7,727 still need system mapping. Original instructions and archives are unchanged.

### Nested arrays and string-storage follow-up

The original version-info, portal, collection-icon and light-thermometer helpers passed 672 integrated checks with actual nested arrays of zero, one or two entries. Tests cover pointer and relative input descriptors, distinct source counts, field selection, force flags, alignment, complete output buffers and guards. Portal names were empty in that integrated fixture.

Separately, original portal and edit-rights helpers passed 1,944 synthetic string checks using the original strlen and strncpy implementations. Their import slots were independently matched through original executable relocations and bundled libc exports. Checks cover inline, pointer and relative input strings and the 63/64-byte output-storage boundary. No account credentials or real signature material were used. Allocation/growth/failure, null output, malformed inputs, aliasing and integrated nonempty portal strings remain untested.

The previously unnamed byte at record offset 0x149 matches was_localised_from_content_field. Its 32-character name exceeded the earlier candidate index limit; the index was corrected and 16 original hash checks passed. The output byte is initialized to zero and copied late, after earlier text-gating checks. Its full runtime role remains under investigation. Counts stay at 420 checked names; these tests add evidence, not additional function-name or whole-game completion credit.

### Saved Dream-record materializer

Applied MaterializeDreamRecord with five assembly-supported SysV arguments: two input records, a range of selected field hashes and an output-buffer descriptor. All 5,503 original instructions were read and matched, nested helpers traced, and the saved name/signature independently reopened. Empty selection uses the second input; a nonempty selection chooses selected fields from the second input and other fields from the first. The output reserves a 16-byte-aligned fixed record and stores nested data using relative offsets.

The complete original serializer passed 60 aligned minimal-record checks and 1,008 checks with nonempty synthetic titles, descriptions and signature strings, using original helper and libc code with preallocated output. Tests check full output buffers, relative descriptors, selection, alignment gaps, input preservation and guards. The localisation flag is copied after text serialization in these cases. No real account or signature data was used.

An unaligned append-position test disagreed with the general record oracle. All seven known direct callers supply fresh empty output descriptors, consistent with the aligned path; no game bug is demonstrated. Nonempty parent arrays, allocation/growth/failure, malformed inputs, aliases and large offsets remain untested. Ghidra reports type-propagation and overlapping-global warnings; assembly remains primary evidence. Reading this body and testing bounded records does not recover all field semantics or complete Dreams.

Totals: 421 checked names and 1,854 mapped functions among 9,580 discovered functions; 7,726 still need system mapping.

### Complete serializer: nonempty array checks

The complete original Dream-record serializer passed 960 additional checks across all 15 array fields, tested one at a time with one or two entries. These include framing, collection icons, categories, portals, developer tags, awards, tags, themes, collaborators, tutorial fields, slideshow hashes, thermometer entries and the nested version record arrays. Original helpers, libc string routines and framing constants were used. Tests verify whole output buffers, selection between distinct source arrays, pointer and relative descriptors, counts, offsets, alignment gaps, padding and unchanged inputs. Portal names were empty; tag strings were synthetic.

This adds evidence to the existing function review and leaves the checked-name count at 421. Simultaneous nonempty arrays and strings, buffer growth/failure, malformed data, aliases, large offsets and real-game behavior remain untested.

### Saved metadata record types and combined-path checks

Saved descriptive Ghidra layouts for the 96-byte portal record, 88-byte edit-rights record, 64-byte collection-icon record and 104-byte version-info record. Their helpers now use typed input/output pointers. Shared types describe an 80-byte string container with 64 inline characters, a 16-byte array descriptor and a 24-byte data/used/capacity buffer descriptor. The main Dream-record materializer now uses the typed buffer pointer; its input record pointers remain untyped. Eight-byte pointer widths, field offsets, record sizes and existing SysV register/stack locations were independently verified after reopening. Original instructions and archives match. Unknown padding and opaque hash/color bytes remain explicit; these are working layouts, not recovered source declarations.

The complete original serializer also passed 384 combined-record checks with all 15 array fields populated together and nonempty main and nested portal strings. Checks cover lengths 3, 63, 64 and 127, field selection, pointer and relative input descriptors, input alignment, whole output buffers, counts, offsets, strings and guards. All data was synthetic and output preallocated. Allocation/growth/failure, malformed inputs, aliases, large offsets and real-game execution remain untested. Parent decompiler warnings remain. These type and test updates add no function-name credit; the count remains 421.

### Verified language-code lookup

Saved `LookupLanguageCodeByKey` with its assembly-supported 32-bit input and string-pointer result. Its complete 104-instruction body maps 22 recognized keys to language codes and returns null for other keys. Original code passed 4,205 standalone native checks covering every mapped key, nearby values, comparison boundaries, signed extremes and deterministic random inputs. The saved name and signature were independently reopened; original instructions and archives are unchanged.

Caller tracing shows localized titles, descriptions and portal names select a matching language entry, falling back to an `all` entry. The title copy helper uses inline storage for up to 63 bytes; description storage uses a dynamic descriptor. The source of the selected language, enum/hash generation, allocation failure behavior and full live-game flow remain unresolved. The naming is descriptive, not recovered original source.

Totals: 422 checked names and 1,855 mapped functions among 9,580 discovered functions; 7,725 still need system mapping. These counts measure documented work, not a percentage of the entire game recovered.

### Verified localized-text selection

Saved SelectLocalizedInlineText64 and SelectLocalizedDynamicText with two assembly-supported arguments and void returns. Both complete original bodies were read, caller and copy-helper paths traced, full trial pseudocode reviewed, and saved names/signatures independently reopened. Original instructions and archives are unchanged.

The complete original selectors, language lookup, copy helpers and original libc routines passed 1,620 synthetic checks. The first exact language match wins; otherwise the last all entry is used; with neither, the destination stays unchanged. Checks cover text lengths through 127 bytes, duplicate and reordered keys, three selected languages, alignment and input/outer guards. Buffers were preallocated: allocation, growth, free, failures, invalid counts, aliases and live-game behavior remain untested.

Static initialization tracing independently links six original imports and the 23-entry platform language table with its original relocations. The path checks DefaultLanguage, reads a platform parameter, and tests full and base localization-file paths before falling back. This path was not executed.

Totals: 424 checked names and 1,857 mapped functions among 9,580 discovered functions; 7,723 still need mapping. These are documented review counts, not whole-game completion.

### Verified tool-tag lookup signature

Preserved the existing reviewed name GetToolTagName and saved its one 32-bit index argument and string-pointer return. Independent reopening verified persistence and unchanged original instructions and archives. The complete original leaf function, five relative jump tables and original strings passed 5,123 checks across all 837 traced indexes, nearby values, signed extremes and deterministic random inputs. Unsupported values return notag. Names include tools, modes, menus and actions; this verifies the lookup, not those systems. No new naming credit: 424 checked names.

Further metadata tracing distinguishes category-name lookup from numeric parsing: the helper forms a kCategory name, hashes it and maps recognized hashes to category IDs. Award lookup recognizes a fixed set of 191 hashes and writes the recognized hash or zero. These two helpers have static body review but no new runtime or naming credit.

### Verified category-name lookup

Saved TryLookupCategoryIdByName with text begin/end pointers, a category-ID output pointer and a success/failure return. All 500 original instructions were read and matched; the saved name/signature was independently reopened without instruction or archive changes. This converts category names into metadata IDs, rather than parsing decimal numbers.

Seventy-five original category literals passed 1,200 checks with the original hash function. The complete original lookup, hash and successful libc dependencies then passed 4,880 checks covering recognized names, CATEGORY_ prefixes, trailing punctuation or spaces, unknown and wrong-case inputs, alignment and exact outputs/guards. Success writes the ID; failure leaves the output unchanged. Long suffix bounds, malformed prefixed all-punctuation inputs, libc error handling and live-game behavior remain untested.

Totals: 425 checked names and 1,858 mapped functions among 9,580 discovered functions; 7,722 still need mapping. This is documented semantic-review progress, not a whole-game completion percentage.

### Verified award-name resolution

Saved ResolveAwardHashByName with text begin/end pointers and an output-hash pointer. The helper clears the output, hashes the supplied text, and stores that hash only when it belongs to its 191 recognized values. The working return is void because the traced metadata caller ignores the return register. All 584 original instructions were read and matched; backup, isolated trial, promotion and independent reopening verified the saved name/signature and unchanged original instructions and archives.

All 191 recognized hashes now match original executable award-name strings, including four longer Impy 2022/2023 nominee names missed by the earlier short-string index. The complete original lookup and hash code passed 3,136 checks covering these names, unknown inputs, alignment and exact outputs/guards. Hash collisions, arbitrary input lengths, aliases and live-game behavior remain untested. This verifies award metadata resolution, not the award service or entire game.

Totals: 426 checked names and 1,859 mapped functions among 9,580 discovered functions; 7,721 still need mapping.

### Tagged metadata path validation

Read the complete 916-instruction tagged metadata helper and checked 13,752 cases through original code across flags, five enum fields, typed references, signed challenge rank, category/award appends and tutorial tool-tag appends. Arrays were preallocated; checks cover counts, existing entries, pointer/relative descriptors and whole output allocations. These are tested paths, not every branch or live-game behavior.

Execution corrected two static interpretations: lowercase h is accepted as the typed reference prefix while uppercase H is rejected; tool-tag index 836, ImportExportMode, is accepted. Both initial fixture mismatches were retained with their causes and corrected checks. Unknown categories leave arrays unchanged; unknown awards append zero.

Separately, the original tag hash matched an independent XXH64 specification model in 5,824 checks. Tag-record append passed 480 checks and string insertion with original libc shared copy code passed 1,888 checks. Full tag construction and percentile conversion remain untested, as do allocation/growth/failure, malformed counts and arbitrary aliases. No naming credit added: 426 checked names.

### Saved tag runtime helpers

Saved HashBytesXXH64, AppendTagRecord56 and InsertPackedSmallStringBytes with assembly-supported SysV arguments and returns. All three original bodies were read and matched, and the saved names/signatures independently reopened. Original instructions and archives are unchanged.

The original hash passed 5,824 checks against an independent XXH64 specification model, including four seeds, lengths through 1,024 bytes, binary inputs and alignment. The append helper passed 480 checks of all 56 copied bytes, count changes, pointer/relative storage and existing-element inputs. String insertion passed 1,888 checks using original libc shared copy code across inline and preallocated external storage. These are 8,192 scoped checks; allocation/growth/failure, invalid indexes/counts, arbitrary aliases, full tag construction and live-game behavior remain unverified.

Totals: 429 checked names and 1,862 mapped functions among 9,580 discovered functions; 7,718 still need mapping.

### Saved tagged Dream metadata helper

Saved ApplyTaggedDreamMetadata with a tagged-entry pointer and mutable Dream-record pointer. Its complete 916-instruction body and 14 discriminator cases were read and matched, and three record-building callers traced. Independent reopening verified the descriptive name and working SysV signature; original instructions and archives remain unchanged.

Its original tested paths passed 13,968 checks across flag/enum writes, typed references, challenge rank, category/award/tool-tag appends and inline TAG construction, using original dependencies and preallocated storage. The 216 TAG checks compare defined fields and buffers while excluding unspecified record padding at bytes 41 through 47. The tested paths do not cover the entire helper: percentile conversion, allocation/growth/failure, long-tag truncation, malformed counts, arbitrary aliases and live-game behavior remain unresolved. The decompiler still warns about overlapping globals; complete original assembly is the primary evidence.

Totals: 430 checked names and 1,863 mapped functions among 9,580 discovered functions; 7,717 still need mapping. This is documented semantic-review work, not a whole-game completion percentage.

### Saved unsigned integer decoder

Saved ReadUnsignedVarint64OrZero after reading its complete original body and running 2,296 independent-model checks of decoded values, cursor movement and full input/output guards. Independent reopening verified the descriptive name and working SysV signature. Original code and archives remain unchanged.

The reader accepts noncanonical encodings and returns zero for truncated or invalid continuation sequences. Zero therefore does not prove valid input. These are scoped original-helper tests, not whole-parser or live-game verification.

Totals: 431 checked names and 1,864 mapped functions among 9,580 discovered functions; 7,716 still need mapping. These counts do not measure whole-game completion.

### Saved transport decoding helpers

Defined DecodeBase64LikeText, FindRequestSlotByStreamId and ReadHpackPrefixInteger after reading their complete original bodies, auditing boundaries and testing original machine code. The scoped checks total 1,320, 828 and 6,912 respectively. Independent reopening verified all three saved definitions and working signatures; original code and archives remain unchanged.

The text decoder treats equals as zero-valued data and can write three bytes when its supplied capacity is below three. Tests used oversized guarded allocations; this is helper behavior, not an exploitability claim. The known status-details caller supplies 2,048 bytes. None of these tests verifies the whole parser, live service or game.

Totals: 434 checked names and 1,867 mapped functions among 9,583 discovered functions; 7,716 still need mapping. Three previously undefined functions were added; extraction is not semantic completion.

### Saved HPACK string and table helpers

Defined DecodeHpackStringTo1024Buffer, LookupHpackHeaderByIndex and SetHpackDynamicTableLimit after complete original-body review and 688, 2,208 and 820 scoped original-code checks respectively. Independent reopening verified the saved definitions and working signatures; original bytes and archives remain unchanged. The 61-entry static header table matches RFC 7541, and all 122 original table-pointer relocations were verified.

These checks do not establish whole-decoder or live-game correctness. Exhaustive Huffman padding/EOS handling, malformed table states, aliases and concurrency remain unresolved. The insertion helper remains undefined as a separate function because its code overlaps an existing Ghidra function body; ownership will be audited before changing that boundary.

Totals: 437 checked names and 1,870 mapped functions among 9,586 discovered functions; 7,716 still need mapping. This records scoped semantic review, not whole-game completion.

### Saved HPACK dynamic table insertion

Defined InsertHpackDynamicEntry after tracing both tail callers and correcting Ghidra ownership that had absorbed the callee into an encoder. The backed-up trial and independent reopen verified that only the audited insertion range left the encoder body; all other existing bodies, names and signatures stayed unchanged. Original bytes and archives are unchanged.

The original helper passed 5,760 scoped insertion-sequence checks of packed records, shifted indices, eviction and guards, with original hash and copy dependencies. Oversized entries can exceed the configured table limit; full HPACK conformance, malformed tables, aliases, concurrency and live-game behavior remain unresolved.

Totals: 438 checked names and 1,871 mapped functions among 9,587 discovered functions; 7,716 still need mapping.

### Saved HPACK header representation decoder

Defined DecodeNextHpackHeader after reading all 361 original instructions and auditing control flow, tail calls and boundaries. It handles indexed headers, literal names/values and table-size updates through the reviewed helpers. Independent reopening verified the saved name and working stream-descriptor signature; original bytes and archives remain unchanged.

The top-level decoder has not been executed. Supporting helpers passed scoped original-code tests and 384 combined pipeline steps; those do not establish whole-decoder correctness. The decompiler warns about overlapping globals. Original formatted-copy behavior, exhaustive Huffman padding/EOS handling, malformed tables, aliases, concurrency and live-game behavior remain unresolved.

Totals: 439 checked names and 1,872 mapped functions among 9,588 discovered functions; 7,716 still need mapping.

### Brick shader resource wrappers

Saved GetOrLoadBricker2TagBricksShader and GetOrLoadBricker2HashBricksShader after reading 410 original wrapper instructions and 369 loader-callee instructions. Original import relocations confirm guarded initialization, destructor registration and file loading. The wrappers obtain/cache shader resources through packed-blob or file paths and return an opaque resource pointer when its prepared-header pointer is present. They are CPU loading wrappers, not the GPU tagging or hashing algorithms. The file reader checks whether opening succeeded but does not independently check a complete fread.

Cold backup, isolated trial, promotion and independent reopening verify both names and working signatures; original instructions and archives are unchanged. GPU execution, concurrency, full sculpt behavior and exact correspondence to the 2015 rendering talk remain unverified. Totals: 441 reviewed names among 9,588 discovered functions; this does not measure whole-game completion.

### Compute completion and scoped sweep-grid validation

Saved SubmitComputeQueueAndWaitForFence and AppendComputeCompletionFence after complete original-body and caller review. The completion builder increments a fence number and emits its destination/value; the submission path notifies the compute queue and waits until the shared fence equals the expected value. Event wakeup alone does not permit continuation. Observed wrappers ignore platform return codes and have no overall timeout. 2,148 original packet-writer tests verify packing and cursor changes with existing capacity; GPU execution and memory ordering are unverified.

The existing ExtractShaderBinarySections name now has a tested two-argument signature, verified after reopening. 8,864 native checks cover pointer/size extraction and guards, not blob validity. Separately, 7,880 original coordinate-marking window tests and 1,131 neighbor-bit window tests match independent models of a 32-cubed byte grid. These selected windows do not validate the full sweep builder or GPU boundary results.

Totals: 443 reviewed names among 9,588 discovered functions; 1,875 mapped and 7,713 unmapped. New compute-support mappings describe shared graphics infrastructure, not full completion of rendering or sculpting.

### Saved sweep boundary routines

Saved BuildSweepBlockRanges and DispatchSweepHashBlocksRange after reading and matching 1,549 original instructions. The builder marks and propagates a 32-cubed byte grid, orchestrates block-index, cleanup and coarser processing stages, reads counters after compute completion waits, builds paired range boundaries, applies reverse range hashing and bias, then pads boundaries and marks them ready. The range dispatcher uses adjacent boundaries for SweepHashBlocks.

The 7,880 coordinate and 1,131 neighbor native checks cover selected CPU windows only. Whole-builder execution, GPU shader behavior, world scale and resource lifetime remain unverified. Early exits can leave partial boundaries with ready clear. Existing incomplete signatures were preserved; names are descriptive analyst labels. Backup, trial, saved promotion and independent reopening passed with original instructions and archives unchanged. Totals: 445 reviewed names, 1,877 mapped and 7,711 unmapped among 9,588 discovered functions.

### Brick shader binaries and hash-resource setup

Matched Bricker2TagBricks and Bricker2HashBricks to the immutable local shader archive using the original native path hash and section extractor. Their instruction prefixes through the first end-program marker decode and reassemble exactly: 306 instructions / 1,552 bytes and 102 instructions / 496 bytes. Trailing resource data was excluded from executable-code claims. This verifies byte-preserving analysis, not GPU execution.

The tagging shader contains coordinate interleaving and bounded atomic table operations. Its 40-instruction integer interleaving window matches an independent Morton-code model across 68,608 software cases; this is not a native GPU test. The hashing shader uses a bounded probe/displacement structure with atomic table updates. Full wave-mask, floating-point, resource-bound and concurrent behavior remain unresolved.

Saved InitializeGpuHashTableResources after a complete 121-instruction body and caller review. It selects a capacity and builds paired 8-byte/4-byte tables plus a shared parameter block. The observed startup request selects 367,001 entries. Parameters contain capacity, reciprocal, clamp and retry seeds; 868 original CPU-window checks cover all 217 capacity entries and four alignments with exact output guards. Full allocation failure behavior and GPU use remain unverified. Backup, trial, saved promotion and independent reopening passed; original instructions and archives are unchanged. Totals: 446 reviewed names, 1,878 mapped and 7,710 unmapped among 9,588 discovered functions.

### Resource storage and aligned pool allocation

Saved TryAllocateGraphicsResourceStorage and AllocateAlignedBlockFromPool after reading and matching all 278 original instructions. The resource wrapper checks allocation classes, fills storage metadata and reports failure. The underlying pool allocator selects an aligned free block, splits leading/trailing ranges and updates allocation records and statistics. General pool allocation is mapped to shared engine support; graphics resource storage is mapped to compute support.

616 original core-window tests verify alignment, splitting, records, statistics, no-fit behavior and guards with one free block and available bookkeeping nodes. Mutex entry/exit and high-water snapshots were bypassed; full allocator, concurrency, node exhaustion and live execution remain unverified. Ordinary null-return paths strengthen the static unchecked-allocation finding in hash-resource setup, but no live crash was reproduced. Backup, trial, saved promotion and independent reopening passed with original instructions and archives unchanged. Totals: 448 reviewed names; 1,880 mapped and 7,708 unmapped among 9,588 discovered functions.

### CSG hash-table clear dispatch and loader

Saved DispatchGpuHashTableClear and GetOrLoadHasherClearShader after reading and matching all 292 original CPU instructions. The dispatcher passes both hash-buffer descriptors and selected capacity to HasherClear. The loader uses the source-associated shader path, archive lookup and file fallback. It returns null without a loaded header, while this dispatcher has no local null check. The dispatcher does not wait internally. GPU clear values, completion and live runtime remain unverified. Backup, trial, promotion and independent reopening passed.

Allocator follow-up adds 512 multiblock/node-exhaustion and 1,920 snapshot core-window cases, for 3,048 total selected core checks. A first-fit split-node shortfall can return failure without trying a later exact-fit block; a high-water snapshot can contain only a prefix when nodes run out. Mutex entry/exit, concurrency, invalid metadata, overflow and full allocator behavior remain unverified. These checks add evidence, not reviewed-name counts.

Totals: 450 reviewed names; 1,881 mapped and 7,707 unmapped among 9,588 discovered functions. The larger brick pipeline remains under analysis and is not counted as reviewed.

### GPU buffer descriptors and format fields

Saved InitializeGpuBufferDescriptor and refined the signature of the existing PackMaskedFormatFields name. All77 original instructions were read and matched; 1,280 original packer executions and336 complete descriptor-construction executions passed, including guarded outputs. Eleven packer call/jump sites across seven owners establish its broader graphics use. Individual enum meanings remain unresolved, so field parameters stay neutral. This adds one reviewed name, not two.

HasherClear follow-up locates the archived shader using the original hash and section extractor. Its16-instruction program issues zero stores to both tables;80 decoded bytes reassemble exactly, with76 trailing bytes excluded. Successful descriptor construction supplies the same capacity to both bounds checks. This is static evidence, not GPU execution or hardware validation.

Totals:451 reviewed names;1,883 mapped and7,705 unmapped among9,588 discovered functions.

### Brick storage and cache lifetime

Saved ResizeBrickBlockChain,ReleaseMarkedObjectCacheReferences andQueueAgedCacheEntriesForRelease after complete original-body review andindependent reopening. Original CPU fixtures passed2,970 block-resize,288 direct-reference maintenance,1,848 state1 walker and3,696 collision/wrap state2 walker cases. Exact links,counts,guarded images andbudget/hash changes were checked within those scopes. The generic walker is mapped to shared support;sculpt block storage andmarked-object maintenance are mapped to sculpt geometry.

The static chain connects reference release,generation aging,queueing,pending-resource release andblock recycling. Original imports identify mutex operations,an untimed condition wait andgeneration broadcast. A zero initial walker budget can still move its first eligible entry. Auxiliary arrays,mixed hash homes,optional callbacks,concurrency,whole-program liveness andlivegame/GPU behavior remain unverified. Test counts do not represent game completion.

Totals:454 reviewed names;1,886 mapped and7,702 unmapped among9,588 discovered functions.

### Bricker2 build pipeline

Saved RunBricker2BuildPipeline after staged review andmatching of2,512 original CPU instructions,three caller traces andindependent reopening. It coordinates atlas/counter setup,ordinary ormulti-item tagging andcollection,block allocation,key sorting,voxel gathering or tree writing,compaction,hashing,open-face/corner work,child indices,surface counting,andfinal counter/output handling. Explicit readiness,capacity andallocation failure paths were traced.

This establishes a descriptive CPU orchestration role,not a recovered source implementation orvalidated GPU algorithm. The exact aggregate stack types remain unresolved;the existing unknown prototype was retained. Helper tests do not prove whole-pipeline geometry orruntime correctness. Raw code remains local.

Totals:455 reviewed names;1,887 mapped and7,701 unmapped among9,588 discovered functions.

### Bricker2 shader research: encoding and semantics remain separate

Read all 49 decoded tree-writer instructions and all 2,807 decoded gather instructions in staged reviews. The tree writer reassembled to its exact 260 original bytes. Gather reassembly failed at nine image-store constraints, so its complete encoding roundtrip remains unverified. Raw shaders and disassembly remain local.

The gather trace covers coordinate decoding, hash and sparse-tree lookup, sample filtering, weighted interpolation, gradient bounds, index reservation, compressed payload and final records. Exact algebra checks establish one trilinear output and its center-gradient coefficients. Software models checked 5,668 coordinate cases and 4,176 final payload-packing cases; the payload matches BC3 byte-field layout, but the bound resource format is unverified. A 512-address model resolves shared-memory restoration before metadata reads. These checks do not execute the GPU or prove whole-shader correctness.

AMD class documentation clarifies that mask 60 selects negative classes including negative zero; 8,242 software cases check that definition. The reference is GCN3, so exact PS4 GCN1.1 behavior remains a stated assumption. Channel meanings, scalar units, GPU floating behavior, memory visibility and runtime safety remain unresolved. Reviewed-name total stays 455.

Format reference: https://learn.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-block-compression
ISA reference: https://gpuopen.com/download/AMD_GCN3_Instruction_Set_Architecture_rev1.1.pdf

### Bricker2 gather and tree-writing shader loaders

Saved GetOrLoadBricker2GatherVoxelsChunkShader and GetOrLoadBricker2WriteTreeBricksShader after reading and matching all 411 original CPU instructions. Original source and shader literals link these loaders to the archived programs analyzed in the previous checkpoint. Both use guarded initialization, archive lookup and file fallback, and return an opaque resource only when its header is present. Backup, isolated trial, promotion and independent reopening passed. GPU execution and whole-shader correctness remain unverified.

Totals: 457 reviewed names; 1,887 mapped and 7,701 unmapped among 9,588 discovered functions.

### Gather output format and image descriptor flags

Traced the gather output descriptor from its shader load to the CPU constructor. The output view divides source width/height by four and uses data format 14 with numeric format 4: 32_32_32_32 UINT in AMD register definitions. The shader writes four raw unsigned DWORDs carrying its BC3-compatible packed payload; the write view itself is not BC3-typed. This resolves the earlier hardware-format uncertainty statically, without GPU execution.

Saved SetImageDescriptorControlFlags after matching all 18 instructions and passing 4,096 cases executing the complete original CPU body. The helper sets split control flags and does not set the data format. Backup, trial, promotion and independent reopening passed. The extra uploaded DWORD remains under investigation; the shader header indicates eleven user registers and a hardware group-index register, so an uninitialized shader input defect has not been established.

Primary definitions: https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux/+/master/drivers/gpu/drm/amd/include/asic_reg/gca/gfx_7_2_enum.h and https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux/+/master/drivers/gpu/drm/amd/include/asic_reg/gca/gfx_7_2_sh_mask.h .

Totals: 458 reviewed names; 1,888 mapped and 7,700 unmapped among 9,588 discovered functions.

### Compute shader input-register upload

Saved AppendComputeUserDataRegisters with a four-argument working signature after reading and matching all 83 original CPU instructions. The gather shader uses this helper to upload its input pointers, batch offset and selected buffer descriptor. In 2,432 cases executing the complete original helper, counts 0–16 copied the expected DWORDs, exact-capacity buffers worked, reservation failure preserved the cursor and buffers, and successful reservation could relocate the destination. Controlled callbacks substituted for the real allocator.

Counts 17 and 32 emitted a header and advanced the cursor without copying values. This is documented invalid-count behavior, not a reproduced game failure. GPU submission, concurrency, real allocator behavior and integer-overflow cases remain unverified. Backup, trial, promotion and independent reopening passed.

Totals: 459 reviewed names; 1,889 mapped and 7,699 unmapped among 9,588 discovered functions.

### Gather register binding and historical rendering leads

Traced the archived header through section extraction, CPU copying, code-address patching and compute-shader binding. The resource configuration selects eleven user registers and enables a hardware group-index register. The shader entry uses that group index plus the batch offset. Although the CPU uploader copies twelve DWORDs, the twelfth is outside the configured user-register range; this does not establish an uninitialized shader-input defect. This is a static trace, without GPU execution or execution of the platform driver.

Compared pages 110–115 of Alex Evans’s 2015 talk with the current gather trace. Eight-corner surface classification and bounds provide architectural leads. The slides describe DXT1 color for point clusters, while this shader emits a BC3-compatible payload; these are not established as the same representation. Hilbert ordering, cluster BVHs and stochastic LOD remain unmatched. Historical slides do not justify build-specific function names by themselves.

Source: https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf . Reviewed-name total remains 459.

### Image-format fields and channel selectors

Saved GetPackedFormatChannelSelector and SetImageDescriptorFormat with working argument and return types after reading and matching all 91 original instructions. The getter extracts one of four three-bit channel selectors and returns 2 for an out-of-range channel. The setter writes six data-format bits, four numeric-format bits and four channel selectors while preserving the other descriptor fields.

Complete original CPU execution passed 24,576 getter cases and 4,096 setter cases. These cover all 4,096 selector combinations, channels 0–3 and two out-of-range indices, sampled remaining format bits and randomized initial descriptor words, with surrounding-byte guards. The gather output literal selects channels [4, 5, 6, 7]. Stack-canary data was supplied locally; this does not execute GPU operations or validate the platform driver. Backup, trial, promotion and independent reopening passed.

Totals: 461 reviewed names; 1,891 mapped and 7,697 unmapped among 9,588 discovered functions.

### Image descriptors, surface layout and storage requirements

Saved InitializeImageDescriptorFromSpecification, CalculateGpuSurfaceLayout and CalculateImageDescriptorStorageRequirements after reading and matching all 1,874 original instructions. The constructor validates image specifications and builds descriptors. The surface-layout routine calculates padded dimensions, storage bytes and tile/alignment fields through several modes and fallback paths. The storage routine uses either a restricted table path or mip-by-mip calculations, accumulating size and maximum alignment.

Validation and failure paths are part of this review: late errors can leave a partially modified descriptor or accumulated size/alignment outputs. Exact input/output structures and some called layout-property helpers remain unresolved. These are descriptive name-only changes with existing unknown prototypes retained; neither whole-function CPU execution nor GPU behavior is claimed. Backup, isolated trial, promotion and independent reopening passed.

Totals: 464 reviewed names; 1,894 mapped and 7,694 unmapped among 9,588 discovered functions.

### Original surface-layout execution: linear modes

Read and matched another 458 instructions across the layout dependencies, including packed tile-property lookups and macro-layout selection. Executed the entire original CalculateGpuSurfaceLayout routine with its original helper code and tables in 320 ordinary-linear and 320 aligned-linear cases. Independent formulas checked dimensions and storage bytes for five pixel sizes across varied widths/heights; input and surrounding memory guards remained unchanged.

The first aligned model underpredicted padding for a 1×1 eight-bit surface. The original returns a 256-pixel pitch there. Correcting the slice-divisibility constraint resolved the mismatch, and all 320 aligned cases then passed. This failed prediction is recorded as a model correction, not counted as a passing case.

Coverage is limited to single-sample, depth-one, uncompressed linear surfaces. Tiled modes, compressed formats, mip chains, arrays, overflow, concurrency and GPU execution remain unvalidated. Other output fields have not all been independently modeled. No new names are counted; the total remains 464.

### Linked image constructor execution and working prototypes

Executed 64 linked scenarios through the complete original image constructor, storage-requirements routine, descriptor-to-layout conversion and packed-format getter: 256 successful original function calls. Checks cover dimensions, descriptor kind and format roundtrip, exact storage size/alignment, decoded layout values, unchanged input and surrounding memory guards. Four invalid constructor cases confirm that early mip validation preserves the descriptor while later kind/dimension errors leave partial changes. Coverage is restricted to kind9 linear128bit images, one mip/sample, depth1 and slice0.

Saved BuildSurfaceLayoutInputFromImageDescriptor and GetImageDescriptorPackedFormat. Also replaced unknown prototypes on the three previously named constructor/layout/storage routines with justified register arguments and status returns. Storage now has explicit 64-bit size and 32-bit alignment output pointers. Structures remain opaque. Backup, trial, promotion and independent reopening passed; other image kinds, tiled/compressed formats, overflow, concurrency and GPU execution remain unvalidated.

Totals: 466 reviewed names; 1,896 mapped and 7,692 unmapped among 9,588 discovered functions. Three prototype updates do not add name counts.

### Sculpting compressed-attribute atlas and image resource setup

The original game format table identifies the startup source texture as Bc3Unorm. Its dimensions are 2048×2048×128. The gather shader write view is 512×512×128 with four unsigned DWORDs per element, matching one sixteen-byte payload per 4×4 source block. Startup derives the write-view address from the source descriptor. Physical meanings of the payload channels remain unresolved.

Executed the original tile selector, descriptor constructor, storage calculator and packed-requirements helper for these actual dimensions/formats under both hardware-mode inputs. Source and write view each require 536,870,912 bytes (512 MiB), aligned to 256 bytes. These tests calculate descriptors and sizes; they do not allocate GPU memory, execute shaders or observe which hardware mode the running game selects.

Saved InitializeGpuImageResource and GetImageDescriptorPackedAllocationRequirements after matching all 180 instructions. The initializer builds a descriptor, attempts storage allocation, sets address/control flags and registers metadata; it was reviewed statically, without executing allocation or registration. The requirements wrapper packs alignment and size into one 64-bit result; its size-overflow branch remains untested. Backup, trial, promotion and independent reopening passed.

Totals: 468 reviewed names; 1,898 mapped and 7,690 unmapped among 9,588 discovered functions.

### Sculpting distance atlas: format, binding and addressing

The game’s original format table identifies the companion distance atlas as R8Unorm, with startup dimensions 2048×2048×128. Traced its descriptor through the brick pipeline’s local copy and control flags into the gather shader constant block and eight image stores. Each stored value uses the shader transform 0.25×distance+0.5, which algebraically maps −2 to 0, zero to 0.5 and +2 to 1. Physical units, GPU rounding and UNORM clamping/conversion remain unverified.

The complete original descriptor/size chain passed both hardware-mode inputs: 512 MiB storage, 256-byte alignment, with the format preserved after control-flag changes. No GPU allocation or rendering was performed.

An independent integer model checked all 1,048,576 possible twenty-bit indices. Their base coordinates map uniquely into 256×256×16 slots of size 8³ inside this atlas. This verifies the software base-address formula, not actual allocator capacity, every shader lane, hardware tiling or memory visibility. Reviewed-name total remains 468.

### Surface-voxel counting consumes packed metadata

Linked the actual Bricker2CountSurfaceVoxels shader through original loader literals, native archive hashing and section extraction. Read all 68 decoded instructions; reassembly reproduced the exact 344 program bytes. The shader reads 172 R8Uint metadata bytes per physical brick and counts nonzero nibbles. It does not sample the distance atlas directly. The gather producer explicitly zeros the final unused nibble, leaving 343 valid cell entries.

Software models passed 1,200 record-count cases and 224 counter-distribution cases. The shader always adds the count to its selected level counter. A separate per-brick DWORD’s high bit also enables weighted contributions to lower-index counters, using powers of four with 32-bit arithmetic. That flag’s meaning and the counters’ physical units remain unresolved; GPU atomics, memory visibility and runtime results are unverified.

Saved GetOrLoadBricker2CountSurfaceVoxelsShader after matching all 206 CPU instructions and independently reopening its working pointer-return signature. Backup, trial and promotion passed.

Totals: 469 reviewed names; 1,898 mapped and 7,690 unmapped among 9,588 discovered functions.

### Brick-key marker traced through collection and counting

Read all 162 decoded instructions of Bricker2HashChildAndTagParentBricks and all 903 of Bricker2CollectBricks. Reassembly reproduced their exact 804 and 4,408 program bytes. Traced bounded parent/child hash operations, sibling selection, collection reservation/capacity filtering and bit-population counters. Atomic concurrency and GPU behavior remain unvalidated.

The collection shader explicitly adds a high-bit marker when its iteration parameter is zero; the CPU supplies that parameter directly. The gather shader loads the key once and preserves it through the per-brick key write. The surface-count shader then tests that high bit for weighted counter contributions. This establishes a zero-iteration marker’s origin, rather than a distance or material flag. Its broader policy role and the counters’ physical units still need tracing.

Collection also contains an orientation/coordinate-bit transformation. Its precise curve convention, bit-width constraints and input meanings are not established yet. Counter readback and CPU consumption remain unfinished. No new names are counted; the total stays 469.

### Collection coordinate ordering and Media Molecule’s Hilbert lead

Interpreted the collection shader’s 41-instruction integer transform and exhaustively checked all 37,448 points at depths 1–5. Its outputs form a bijection, consecutive curve positions share a face, and recursive groups fill aligned cubes. Another 256 zero-depth inputs retain their values. These are independent geometric checks of Hilbert-style ordering; the exact orientation convention, larger depths and runtime parameter bounds remain unresolved. This is software interpretation, not GPU execution.

Page112 of Alex Evans’s 2015 talk describes Hilbert ordering of voxel bricks. The executable now has matching structural evidence for that technique. The historical slide’s stated block/cluster sizes and other rendering details are not established as identical to this build, and the talk does not supply original function names. Source: https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf .

Saved GetOrLoadBricker2HashChildAndTagParentBricksShader and GetOrLoadBricker2CollectBricksShader after reading and matching all 410 original CPU instructions. Both archive programs were already fully read and reassembled exactly. Backup, trial, promotion and independent reopening passed.

Totals: 471 reviewed names; 1,898 mapped and 7,690 unmapped among 9,588 discovered functions.

### Surface counters traced through readback into volume records

The ReadGDSCounters shader copies words from GDS into a destination buffer under both word-count and descriptor bounds. Read all 18 decoded instructions and reproduced the exact 92 program bytes. The CPU dispatcher prepares the destination, byte offset and count; it does not wait internally. The brick pipeline dispatches 69 words starting at GDS byte 256, then submits and waits for its fence before reading results.

Traced the same 512-byte allocation and its 69-element, four-byte-stride descriptor through the CPU buffer. Words 59–68 correspond exactly to the ten surface-count counters at GDS bytes 492–528 and CPU buffer bytes 236–272. The successful build path copies them into its volume result. CopyAndPackGpuVolumeResource then forwards all ten unchanged to offsets 128–167 of both 168-byte packed volume-record arrays. The relevant successful path was reviewed; the enclosing caller is not claimed fully understood.

Saved DispatchGdsCounterReadback and GetOrLoadGdsCounterReadbackShader after matching all 332 CPU instructions and independently reopening their working signatures. This establishes the counter data path, not rendering policy, physical units, GPU coherency, fence liveness or live readback correctness. Negative/overflow word counts remain unvalidated.

Totals: 473 reviewed names; 1,899 mapped and 7,689 unmapped among 9,588 discovered functions.

### Sculpt point queries traced into the GPU program

Saved DispatchPointQueriesAndWait and GetOrLoadPointQueryRunShader after reading and matching all 337 CPU instructions, backing up the project, testing an isolated copy and independently reopening both signatures. The dispatcher binds the sculpt distance atlas, sampler, packed tree, volume records, query records and output records. It dispatches groups of 64 and explicitly submits and waits for its fence. The unsigned group calculation wraps count+63 in 32 bits.

Read all 262 PointQueryRun GPU instructions and reproduced all 1,400 program bytes exactly; the remaining 84 bytes are metadata. A query selects a volume, uses its bounds and packed tree information, and traverses three-byte child references. Two image gathers feed interpolation of the sculpt distance atlas. The decoding 4*sample-2 is the algebraic inverse of the writer distance/4+0.5. Checked 576 exact rational interpolation cases and 4,096 adjacent-word child-reference extraction cases. These are software algebra checks, not GPU execution.

This consumer reads volume bytes 40–83; it does not read the surface counters at bytes 128–167. Rendering use of those counters remains unresolved. Physical distance units, all returned vector-component meanings, exceptional floating-point behavior and live GPU correctness are not established. A shader-load failure can return null and the dispatcher has no visible null check; no live crash is claimed.

Totals: 475 reviewed names; 1,900 mapped and 7,688 unmapped among 9,588 discovered functions.

### Occlusion voxel stages read beyond the shader names

Read four complete GPU programs linked to CPU descriptor bindings and original archive resources. OcclusionCopyInstances transforms per-instance data (248 instructions, 1,360 program bytes). OcclusionMakeInitialVoxels transforms/intersects bounds, reserves ordered output slots and emits parent records (178 instructions, 984 bytes). OcclusionMakeChildEmitMasks evaluates eight children per parent, samples the sculpt distance atlas, compares against a scale/orientation-dependent threshold and writes a 64-bit wave mask containing eight adjacent bits per parent (316 instructions, 1,740 bytes). All three programs reassembled exactly; trailing metadata was excluded.

OcclusionWriteAtomics (282 instructions, 1,592 program bytes) follows packed tree references, evaluates child occupancy and extracts each parent's eight-bit mask. One branch applies an image atomic minimum; another interleaves parent coordinates, adds a region offset and atomically ORs the mask into its byte within a DWORD. CLRX rejected the image atomic instruction because its unorm bit is not set. Kept the original encoding; this program has **no successful reassembly verification**.

Integer software checks passed 320 parent/child indexing cases, 4,162 wave masks, all 32,768 coordinates in a 32-cubed region and 1,024 byte-slot/mask combinations. These verify the stated packing models, not running GPU behavior. None of these four programs reads volume counter bytes 128–167. The child-emission flag at packed byte 124 comes from CPU record byte 24, zero-extended; its broader meaning remains unresolved.

No GPU execution, atomic-concurrency, hardware floating-point or full CPU-renderer validation is claimed. Runtime region bounds, all numeric output meanings and rendering use of the surface counters remain open. No new names or whole-executable behavior coverage were credited for this checkpoint.

### Occlusion refinement loop and buffer handoffs

Saved GetOrLoadOcclusionWriteChildVoxelsShader and GetOrLoadOcclusionUpdateDispatchArgsShader after matching all 412 loader instructions and independently reopening their no-argument pointer signatures. Read both GPU programs and reproduced all 244 and 100 program bytes exactly, excluding metadata. The child writer doubles packed coordinates, adds child bits and preserves region and instance IDs. Its ordered reservation precedes the 524,288-record output guard; the argument updater clamps the accumulated count to that capacity before preparing the next dispatch.

Traced five refinement rounds in the CPU renderer. They alternate resource IDs 45 and 46; each round reads the previous output, and the final atomic stage requests ID 46. Starting from zero spatial coordinates, five refinements generate parent coordinates 0–31; the last eight child bits therefore encode a 64-cubed occupancy region. Checked 37,448 coordinate-refinement cases. These are static binding requests and software models; backend binding and GPU synchronization are not validated.

The selected region count is unsigned min(requested, 6) when a control float equals zero, otherwise unsigned min(requested, 3). Both signed zeros select six; the comparison model sends NaN to three. Checked 2,331 selection cases. The setting meaning and live values remain unknown. Only selected paths of the enclosing renderer were reviewed.

The one-bit voxel packing structurally agrees with pages 136–139 of [Alex Evans SIGGRAPH 2015 talk](https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf), which describes cascaded binary occupancy and atomic OR. This does not establish build-identical code or current cascade count. Located the official [engine-code livestream](https://www.youtube.com/watch?v=yZM_Ij9aeOA); its footage and visible code remain uninspected and unmatched.

Totals: 477 reviewed names; mapping remains 1,900 of 9,588 discovered functions. No in-game validation or additional whole-executable behavior coverage is claimed.

### Deferred compute resource dependencies

Saved CollectDeferredResourceAccessesForJob with a void return, unsigned job ID and opaque resource-record pointer. Read all 39 original instructions and executed the complete original helper in 168 isolated graph cases, including duplicate/shared children and cycles. It appends a resource linked list of access entries before recursively traversing dependencies. A per-resource 16-bit job marker suppresses repeat visits. An initial marker of 65,535 skips matching job IDs; IDs compare by their low 16 bits. Real scheduler job bounds and whether these edge cases are reachable remain unresolved.

Read and matched 355 additional CPU instructions for deferred compute job construction, constant-data registration and dependency finalization. The builder records shader and argument data, tracks an indirect-argument resource when present, and queues the job. This is deferred scheduling evidence, not actual GPU command emission or synchronization validation. Native execution covers the 39-instruction walker only.

Backup, isolated trial, promotion and independent reopening passed. The constant-registration caller decompiled with both corrected arguments. Pending-access capacities, invalid resource IDs and full binding-backend behavior remain open.

Totals: 478 reviewed names; 1,901 mapped and 7,687 unmapped among 9,588 discovered functions.

### Deferred jobs reach indirect compute command writers

Saved FinalizeAndQueueDeferredGraphicsJob and both indirect-dispatch wrappers after matching all 238 original instructions and independently reopening their working signatures. The original finalizer passed 198 bounded fixtures across scalar/vector list-copy boundaries, two tracking modes and prior-job hazard states. The complete four-routine compute builder chain passed 144 cases with an explicit local byte-copy shim for its memcpy import. It retains shader, constants and arguments, registers backing resources and queues the job. These tests do not execute a real scheduler or GPU.

Traced 196 selected instructions in the 4,611-instruction executor. Compute jobs reach shader binding and constant upload. Direct dispatch is skipped when any group dimension is zero. Indirect dispatch resolves an argument resource and byte offset, then selects its command writer. The full executor and state-transition helper are not claimed understood.

Both indirect wrappers call sceGnmDispatchIndirectOnMec, identified through the original SELF import relocation and local NID database. They require eight DWORDs, call refill when needed, reload a relocated cursor, and advance 32 bytes only when the import returns zero. Explicit mode packs (contextflag & 1) + 8*mode with 32-bit wrapping. The original wrappers passed 480 fixtures using an argument-recording import spy and controlled refill. Actual GNM packet bytes, real allocation behavior and GPU synchronization remain unverified.

Fixture corrections are retained locally: fixed guard/end-pointer expectations in finalizer tests, initialized the argument tracking byte in chain tests, and corrected the synthetic refill branch. No original-code failure was inferred from those fixture errors. Queue capacities, invalid IDs, unusual copy sizes and concurrency still need work.

Totals: 481 reviewed names; 1,904 mapped and 7,684 unmapped among 9,588 discovered functions.

### Queue sequence waits and release-memory packet encoding

Saved ScheduleRequiredQueueSequenceWaits and AppendReleaseMemoryPacket after matching all 154 original CPU instructions and independently reopening their working signatures, including the release writer stack arguments. The wait helper passed 1,024 original-native fixtures with command spies. It schedules each wait only when the unsigned required sequence exceeds its cached value, selects the frame-parity address slot, updates the cached value and clears the pending requirements. Tested values include zero and unsigned boundary values; this does not prove safe runtime sequence rollover.

Read 588 instructions across state accumulation, flushing, sequence waits and post-job updates. State accumulation records sequence maxima and cache flags without emitting commands. The flush path reaches known wait and acquire-memory writers. Post-job code increments its queue sequence and targets the same address slots used by waits. Full cache semantics, alternate queue writers and live GPU visibility remain unresolved.

The original release writer passed 4,320 fixtures checking every emitted word, field masks, refill failure and relocation. It writes seven DWORDs headed c0054902 and advances 28 bytes. The opcode is RELEASE_MEM in the [AMD kernel definitions](https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux.git/%2B/1e43c377a79f9189fea8f2711b399d4e8b4e609b/drivers/gpu/drm/amd/amdgpu/cikd.h). The traced caller supplies event 47, cache flags zero, data selector one and the incremented sequence payload. Packet encoding was executed locally; no GPU ordering, coherence or liveness validation is claimed.

Totals: 483 reviewed names; 1,906 mapped and 7,682 unmapped among 9,588 discovered functions.

### EffectField initialization and wave properties

Saved InitializeEffectFieldDefaults with a working void return and one object-pointer parameter after a backed-up trial, independent trial reopen, promotion and independent main-project reopen. All 93 original initializer instructions and 277 instructions around five recorded direct callers were byte matched. Each caller clears 592 bytes before initialization. The registered EffectField descriptor identifies its creation callback, which calls this initializer.

Executed the original initializer across three controlled guard paths. Wave amount, scroll and time initialize to zero; wave position initializes to (1, 0). The one-time packed default is computed or reused from its cache. Guard imports were replaced by controlled stubs. These checks cover the wave fields, packed value and object boundary canaries; they do not validate every initialized field, real guard synchronization or concurrency.

Inspected visible wave source in Media Molecule’s [2016 technical livestream](https://www.youtube.com/watch?v=yZM_Ij9aeOA), including the splats_mega.cpp tab and octave-based deformation. Related wave properties exist in this executable, but their runtime consumers and shader upload remain unresolved. No equivalence to that footage, water-system identification or runtime deformation completion is claimed.

Totals: 484 reviewed names; 1,907 mapped and 7,681 unmapped among 9,588 discovered functions. Reviewed names measure supported descriptive roles, not overall game completion.

### Graphics user-data writer and EffectField shader trace

Saved AppendGraphicsUserDataRegisters with its five-argument working signature after backup, isolated trial, independent trial reopen, promotion and independent main-project reopen. All 95 original instructions were read and matched. The original function passed 1,296 packet fixtures covering register starts, stage indices, counts, capacity thresholds and controlled refill failure/relocation. Counts 1–16 copy the source DWORDs exactly. Count zero substitutes NOP words; count 17 advances without copying payload. Real caller limits remain unresolved, so count 17 is an observed boundary, not a supported-use claim. No GPU execution was tested.

Traced EffectField type checking and packing into 64-byte records, then into a parity-selected allocation with a GPU descriptor for 1,024 elements. The allocation requests 65,536 bytes with 256-byte alignment. A glass UI draw path places this descriptor in a parameter block; its deferred draw job stores the two shader pointers and copies an eight-byte pointer to that block into its constant payload. Selected executor code sends that pointer through the reviewed user-data writer. Complete hardware stage and shader root-pointer binding still need audit.

Matched the glass shader resources against the unchanged local archive using the original native hash and section parser. In PrimGlassIntoUILayerPS, the descriptor offset matches the CPU parameter block, and 87 selected shader instructions were checked against the archived bytes. The selected branch reads the traced amount, position, time and reverse fields, constructs a spatial phase, adds time and conditionally reverses it. Full modes, final output use and real GPU behavior remain unresolved. A separate PrimGadget lead used a different descriptor offset and was not treated as a confirmed wave consumer.

These are current-build EffectField findings. They do not establish equivalence to the 2016 livestream’s trochoidal water deformation. Raw code, shader binaries and local data remain outside the public repository.

Totals: 485 reviewed names; 1,908 mapped and 7,680 unmapped among 9,588 discovered functions. Naming and selected-path evidence do not measure overall game completion.

### Deferred draw construction and EffectField waveform follow-up

Saved CreateAndQueueDeferredDrawJob with a working nine-argument signature, including three explicitly verified stack arguments. All 416 original builder instructions were read and matched. A 735-instruction original builder, constant-registration, dependency and finalizer chain passed 108 synthetic cases covering copied draw state, both shader pointers, null pixel-shader fallback, two constant payloads, argument preservation and queue insertion. Imported memcpy and memset were replaced by local native shims. Render-target tracking branches, constant mode 2, capacity, concurrency and real GPU execution were not tested.

The fixtures clarified a precondition: pointer-tracking mode needs a registered resource covering the pointer target, not merely the address of the source payload. Invalid fixture inputs faulted in the dependency collector; corrected fixtures passed. This is not evidence of a failure with valid game inputs.

Traced both constant streams of the glass draw. Each contains the same eight-byte parameter-block pointer. The executor sends them to vertex and pixel user-data register pairs. Original register-table values match [LLVM’s primary AMDGPU register definitions](https://llvm.org/doxygen/AMDGPUPALMetadata_8cpp_source.html). This resolves the earlier stage-identity uncertainty on this selected path; it does not validate complete driver configuration or GPU execution.

Recovered the original ELFOShape names and numeric values: Sine, Sandcastle, Square, Ramp, RandomSmooth and RandomStep. They agree with the selected shader waveform branches, including smoothed and stepped hash samples. The waveform modulates a weight used for contributions derived from the original Colour property. Those contributions accumulate into later shading calculations. Final pixel-export dataflow, complete mode behavior under GPU arithmetic and the full glass shader remain unresolved. No equivalence to the 2016 livestream’s water algorithm is established.

Totals: 486 reviewed names; 1,909 mapped and 7,679 unmapped among 9,588 discovered functions. These are verified descriptive roles, not a whole-game completion percentage.

### Deferred draw resource and dependency validation

The original 735-instruction draw-building chain passed 96 additional resource-tracking fixtures across all nine draw-state handle slots and three argument handle slots. These checked first/last-job markers, retention of existing access kinds, write markers and branch-specific flags. Valid synthetic IDs and bounded contexts were used; invalid handles, capacity and concurrency remain untested.

A further 16 original-chain fixtures covered both constant streams in modes 1 and 2 with nonempty root access lists and a shared dependency child. Mode 1 retains its backing record; mode 2 creates a registered copy. The fixtures verified dependency order, shared-child suppression, queue insertion and resource marker updates. Local native memcpy/memset shims remain fixture boundaries. No actual GPU execution was performed.

This extends validation of the existing descriptive name; it adds no function names, mapping cells or whole-game completion credit. Earlier checkpoint limits describe the checks available at those checkpoints; these results supersede the former untested-mode-2 and empty-dependencies limitations for the specified fixture cases.

### Deferred shader constant registration

Saved RegisterDeferredShaderConstants after reading and matching all 110 original instructions, testing it inside the original compute and draw chains, and independently reopening its four-argument working signature and opaque backing-record pointer return. The packed argument contains a low 32-bit mode and high 32-bit byte count. The helper copies payload bytes to the arena and records their DWORD count.

Mode 1 finds a backing resource covering the pointer loaded from the source. Mode 2 finds the source address, creates a registered copy and inherits dependency links. The reviewed dependency collector then walks those links for the job. Modes 0 and unknown modes return no backing record. Synthetic chain tests cover these distinctions, including shared-child suppression; they do not establish invalid-input safety, real capacity, concurrency or GPU behavior. Imported copy/zero routines were local native shims in the fixtures.

Totals: 487 reviewed names; 1,910 mapped and 7,678 unmapped among 9,588 discovered functions. No whole-game completion credit is inferred.

### Shader-pair binding and pixel input controls

Saved BindGraphicsShaderPairIfChanged, AppendGnmVertexShaderBinding, AppendGnmPixelShaderBinding, BuildPixelInputControlWords and AppendPixelInputControlWords with evidence-supported working signatures. All 412 original instructions were read and matched. Backed-up trial, independent trial reopen, promotion and independent main-project reopen verified the five changes without changing executable bytes or archive inputs.

The original pair helper passed 64 cases with command-recording substitutes: unchanged pairs emit no binding calls, changed stages update their cache, null pixel shaders skip input linkage, and changing either stage rebuilds input controls when needed. The original binding wrappers passed 96 cases covering arguments, capacity thresholds, refill failure/relocation and import return status. Their imports independently resolve to sceGnmSetVsShader and sceGnmSetPsShader350. These tests do not execute those platform APIs or validate their generated GPU packets. Cache fields can update even if lower emission fails; full recovery invariants remain unresolved.

The original semantic mapper passed 192 cases covering 2,256 input words, including missing and duplicate semantics. It selects the first matching vertex semantic, uses a fallback for missing matches and packs metadata flags into control words. Its special path is gated by a cached Boolean sceKernelIsNeoMode result. The query was controlled in the fixture; no real console mode or GPU interpolation was tested. Exact compiler semantic names and all hardware bit meanings remain unresolved.

The original input-control writer passed 204 exact packet cases, including counts 0–33, refill failure and relocation. Counts 1–32 preserve every source word; count zero emits NOP words, while count 33 advances over unfilled payload. The latter is observed boundary behavior, not a supported-use claim. Real caller limits still need audit.

Totals: 492 reviewed names; 1,915 mapped and 7,673 unmapped among 9,588 discovered functions. No whole-game completion percentage is inferred.

### Integrated binding-chain validation and failure-path scope

Executed all 412 original instructions of the five-function shader-binding chain together across 192 controlled cases. Vertex/pixel binding wrappers, metadata mapping and input-control packet writing now connect in one fixture. Mapped input words reached the exact emitted packet payload, including the Neo-controlled branch. GNM imports, refill and the Neo query remained controlled substitutes; no real platform-generated binding packet or GPU interpolation was executed.

A targeted transition test first denied command space, then restored space while requesting the same shader pair. The first call still updated the pointer cache; the second skipped rebinding because the pair matched. This establishes helper-local behavior, not a whole-engine defect. The original initialization path selects a default refill callback returning false, and the executor clears its local shader cache at entry. Persistence across executor invocations is therefore not demonstrated. Capacity accounting, later callback changes and recovery within an execution pass still need review.

No new names or mapping cells were added. Totals remain 492 reviewed names, 1,915 mapped and 7,673 unmapped among 9,588 discovered functions.

### Color render-target command binding

Saved AppendColorRenderTargetBinding with an independently reopened working signature. It writes the selected color-target descriptor registers when the derived base word is nonzero; a null descriptor or zero derived word clears the target INFO register. Every packet word, cursor movement, refill failure and relocation was checked in 384 isolated cases and 8,704 connected cases using the original descriptor/format/tile helpers. The connected path covers 490 original instructions. The tile resolver separately passed 7,616 cases and the descriptor helper 25,648 cases. These counts overlap in code coverage and are not whole-game progress percentages.

Connected testing corrected an earlier local bit-field interpretation: one macro-table reader selects bits 6–7, rather than bits 2–3. Nested resolver failure cases remain excluded: the caller ignores its return status and may consume unwritten stack output. Valid descriptor constraints, base-word address units and real GPU behavior remain unresolved. Refill was controlled. No live game or GPU execution is claimed.

Totals: 493 reviewed names; 1,916 mapped and 7,672 unmapped among 9,588 discovered functions.

### Blend controls and depth/stencil target binding

Saved eight descriptive names with working signatures: ResetBlendControl, SetBlendControlEnabled, SetColorBlendFactorsAndOperation, SetSeparateAlphaBlendEnabled, SetAlphaBlendFactorsAndOperation, AppendColorBlendControl, AppendColorTargetWriteMask and AppendDepthStencilRenderTargetBinding. All 180 original instructions were read and byte matched. Backed-up trial, independent trial reopen, promotion and independent main reopen verified only the expected name/signature changes and unchanged original archives.

The five original field setters passed 2,090 exact packing cases, including oversized inputs and preservation masks. Primary gfx7.2 field definitions corroborate source/destination factors, operations, enable and separate-alpha roles. Enable inputs are shifted without Boolean normalization; the reviewed caller supplies zero or one. Hardware factor enum values and actual pixel output were not tested.

The original blend/target-mask writers passed 640 cases checking every packet word, capacity threshold, refill failure/relocation and cursor. Blend controls clear bits 13–15 before emission. The connected depth/stencil writer and descriptor helpers passed 6,400 cases over 501 original instructions, checking 24-word active packets and six-word disabled packets. Nested resolver failure cases remain excluded because their caller ignores status and may consume unwritten output. Valid descriptor constraints remain unresolved. Refill was controlled, with no real GPU or live-game validation. Test instruction scopes overlap and do not measure whole-game completion.

Totals: 501 reviewed names; 1,924 mapped and 7,664 unmapped among 9,588 discovered functions.

### Stencil surface layout and storage range

Saved BuildStencilSurfaceLayoutInput and ComputeStencilSurfaceSliceSize with independently reopened working signatures. Their complete 148 original instructions were read and byte matched. The existing CalculateGpuSurfaceLayout name and signature were retained; its 1,377-instruction body received additional review and tests, with no duplicate naming credit. Original instruction bytes and archive inputs remain unchanged.

The complete original query passed 432 linear-surface cases against independently calculated dimensions and byte counts. The connected original stencil builder, query, size wrapper, base helpers and depth/stencil range helper passed 1,440 cases: 378 accepted layouts and 1,062 rejected synthetic descriptors. The returned range matched the minimum base and maximum end, with descriptor base words converted in 256-byte units. Accepted stencil byte counts agreed with the returned padded dimensions and sample count. These tiled checks establish internal consistency; padding is not independently predicted. For example, a synthetic 128-by-64 surface with two samples needed 32,768 bytes rather than the unpadded 16,384 bytes.

The size wrapper ignores the builder status, queries again, and returns the low 32 bits of the 64-bit size on query success or zero on failure. No tested builder failure became a successful second query. The query can partially write output before returning an error. Exact constraints for all descriptors, overflow cases, other view indices and real GPU behavior remain unresolved. Layout pointers remain opaque.

Totals: 503 reviewed names; 1,926 mapped and 7,662 unmapped among 9,588 discovered functions.

### Viewport transform and clipping commands

Saved ConfigureViewportFromRectangle, AppendViewportTransformAndDepthRange, ResetViewportTransformControl, SetViewportTransformMode, AppendViewportTransformControl, AppendScreenScissor, AppendHardwareScreenOffset and AppendGuardbandAdjustments with independently reopened working signatures. All 361 original instructions were read and byte matched. Float parameters use the verified low four bytes of their XMM registers; scale and offset vectors have float-pointer working types. Backed-up trial and independent trial/main reopening verified only the expected changes and unchanged original archives.

The connected original composite and seven callees passed 96 finite rectangle cases checking all 28 packet words. It constructs viewport half-extents, center translations, screen scissor, rounded hardware screen offsets and guardband adjustments. A further 2,496 capacity/refill cases checked exact packet subsequences and every destination byte. Failed refill can skip a large packet while later smaller packets still fit: emission is not atomic. Successful refill relocation preserves earlier writes and redirects subsequent packets. The callback was controlled; real allocator behavior remains unresolved.

Six targeted edge observations found positive-infinity guardband values for zero extents under nontrapping floating-point control, signed scales for reversed rectangles, and exact preservation of a Z quiet-NaN payload and negative-zero offset. These observations do not establish supported hardware usage or exhaustive IEEE/integer behavior. No real GPU or live-game validation is claimed.

Totals: 511 reviewed names; 1,934 mapped and 7,654 unmapped among 9,588 discovered functions.

### Depth, stencil and raster controls

Saved 19 descriptive names with independently reopened working signatures for depth-test enable/write/compare settings, front/back stencil compare and operations, reference masks, face culling, polygon modes and polygon-offset settings, plus their command writers. All 248 original instructions were read and byte matched. Backed-up trial and independent trial/main reopenings verified only the expected name/signature changes and unchanged original instruction bytes and archives.

The fourteen original setters passed 5,852 exact packing/default/preservation cases. Primary gfx7.2 register fields corroborate the descriptive roles. Some flag setters do not normalize oversized inputs: depth-enable uses addition that can carry, while polygon mode-enable compares the full arguments against two before truncating their three-bit fields. The reviewed draw-state caller uses bounded or Boolean values; observed oversized behavior is not a supported-use claim. Original enum names remain unresolved.

Five original packet writers passed 350 cases checking register targets, masks, duplicated front/back stencil reference/mask words, every output-buffer byte, cursor movement, refill failure and successful relocation. The refill callback was controlled. These checks do not validate actual depth/stencil/raster output, real allocator behavior or live-game execution.

Totals: 530 reviewed names; 1,953 mapped and 7,635 unmapped among 9,588 discovered functions.

### Multisampling, sample patterns and polygon bias

Saved 13 descriptive names with independently reopened working signatures for EQAA fields, MSAA/scissor enable, default sample patterns, sample-location descriptors, centroid priorities, sample-count/distance configuration and front/back polygon offset. All 343 original instructions were read and byte matched. Backed-up trial and independent trial/main reopening verified only expected changes, including float and 64-bit argument storage, with original instruction bytes and archives unchanged.

The five original EQAA setters passed 2,090 exact packing/default cases. Four command writers passed 2,560 cases checking packet words, masks, cursor, all destination bytes, refill failure and relocation. Front/back float-bias packets preserved NaN, infinity and negative-zero argument bits even when the controlled refill callback overwrote volatile float registers. This does not establish supported hardware usage for those values.

The original default sample-pattern composite, descriptor constructor and two writers passed 128 connected cases against original pattern tables and centroid priorities. All 25 packet words, or capacity-dependent subsequences, were checked. Out-of-range sample codes produce zero locations while AA configuration still uses the code’s low three bits; this is observed behavior, not supported usage. Some flags also shift inputs without Boolean normalization. Refill was controlled. Actual GPU sample positions, real allocator behavior and live-game output remain unverified.

Totals: 543 reviewed names; 1,966 mapped and 7,622 unmapped among 9,588 discovered functions.

### Graphics draw-state binding and image-view offsets

Three descriptive names and working signatures were independently reopened: ApplyGraphicsDrawStateIfChanged, ResetGraphicsBindingState and CalculateImageViewOffsetAndSliceSize. All 1,247 original instructions were read and byte matched; original archives remained unchanged.

The draw-state updater connects color and depth targets, blend controls, viewport/scissor, multisampling, depth/stencil, raster state and polygon bias. Twenty-one connected scenarios checked normal binding, unchanged repeats, changes, removal and failed-capacity retry. Caches can advance when emission fails. Executor resets between invocations are established, but in-pass allocation policy and live-game consequences remain unresolved.

The baseline reset passed 40 capacity/refill/return/mode combinations and three failed-refill cache patterns. Its GNM shader call used an explicit controlled fixture: this does not validate real platform shader packets. The image-view helper passed 90 valid linear-image cases against independent mip-offset sums and one invalid-slice rejection. Tiled fast paths, optional metadata paths and the resource prologue still need investigation. The general offset path ignores nested errors, so successful return alone does not establish valid input or output. No GPU or live-game result is claimed.

Totals: 546 reviewed names; 1,969 mapped and 7,619 unmapped among 9,588 discovered functions.

### Render-target auxiliary layouts and packed requirements

Saved four descriptive names and working signatures for color/depth auxiliary-layout queries and their read-only size/alignment wrappers. All 363 original instructions were read and byte matched. Backed-up trial and independent trial/main reopening verified the expected names and parameter storage, successful decompilation, unchanged instruction bytes and unchanged original archives. Target descriptors remain opaque.

The color query matched independent padding/divisibility arithmetic in 4,572 cases, including 108 rejections preserving outputs. The depth query matched padding, slice scaling and alignment rounding in 576 cases. Thirty-two connected wrapper cases checked enable flags and packed returns, including two oversized results: low size becomes zero when it exceeds 32 bits, while high alignment is retained. These wrappers differ from descriptor-mutating preparation helpers that truncate queried sizes.

A separate layout-backed metadata query can write outputs while returning an error; callers must respect status. Unsupported fixed-path pipe configurations were excluded from execution because arithmetic validity is not established. Exact hardware metadata classification, actual allocation consumers and GPU/live-game behavior remain unresolved. The first color-query harness attempt had a pointer-width bug; it was corrected before the passing run and was not a Dreams fault.

Totals: 550 reviewed names; 1,973 mapped and 7,615 unmapped among 9,588 discovered functions.

### Auxiliary image descriptors from color targets

Saved InitializeAuxiliaryImageDescriptorFromColorTarget and SelectPackedAuxiliaryImageFormat with independently reopened signatures. All 262 original instructions were read and byte matched. Backed-up trial and independent trial/main reopening verified only expected name/signature changes, successful decompilation and unchanged original bytes and archives.

The selector matched independently decoded original jump-table constants for all 64 encoded sample/fragment combinations. The constructor passed 2,240 slice/gate cases: 1,248 successful output formats roundtripped to the expected packed format, and 992 rejections preserved the output. Logical width and slice count were checked. Auxiliary height can be padded: a tested 64 by 64 target produced height 128. Exact padded storage arithmetic remains unresolved.

The runtime executor builds the descriptor, reads the target auxiliary address, binds it and applies usage flags. This sequence passed 120 connected cases with source and boundary preservation. Address binding can clear additional tile bits; exact mask arithmetic is not independently proved. The executor ignores constructor status, but upstream validity constraints must be established before claiming a runtime defect. Specific GPU metadata identity, allocation behavior and live-game output remain unverified.

Totals: 552 reviewed names; 1,975 mapped and 7,613 unmapped among 9,588 discovered functions.

### Auxiliary address-binding evidence correction

The earlier 120-case connected binding fixture left the source-format field unset. Its nested resolver validity was therefore unproven, and that receipt has been superseded. The corrected fixture supplies a valid 128-bit source format and checks every enabled nested resolver input. All 120 cases matched the exact source-getter and image-binder masks derived from original tile tables; tile modes that bypass masking were also checked. These replace the earlier 120 cases rather than adding to their count.

Different source and auxiliary-image formats can select different table entries and clear different address bits. This explains the previously observed difference between the getter address and the final bound address. Exact padded storage, allocation behavior and GPU output remain unresolved. No function-review or completion count changed.

### Shared compute dispatch and cached controls

Saved DispatchComputeWithCachedControls and AppendComputeDispatchControl with independently reopened signatures. Both are shared graphics support, not completed sculpting algorithms. All 135 original instructions were read and byte matched. Backed-up trial and independent trial/main reopening verified expected name/signature changes, successful decompilation and unchanged original bytes and archives. Existing named platform dispatch writers were preserved.

The control writer matched exact packet words, masks and capacity behavior in 500 cases. The shared wrapper passed 40 default cases and 972 float-control cases, including 540 exceptional-input cases under an explicitly nontrapping floating-point environment. Its zero-grid gate uses the low 32 bits of the dimension product, so overflow to zero also skips work. The platform import was linked to sceGnmDispatchDirect using original relocation metadata. The API was replaced only in scratch test memory; real platform packets were not validated.

Thirty-two capacity/retry scenarios confirmed that cached controls can advance when their packet cannot be written; restoring capacity and retrying unchanged context does not restore that packet. Region counters count wrapper attempts even when no platform call occurs. Actual allocator recovery policy remains unresolved, so these findings do not establish a live-game defect. Exceptional arithmetic tests do not establish supported GPU settings.

Totals: 554 reviewed names; 1,977 mapped and 7,611 unmapped among 9,588 discovered functions.

### Compute profiling-region labels

Saved InternAndBeginComputeProfilingRegion with a working signature using an opaque context and character-pointer label. All 79 original instructions were read and byte matched, plus 70 downstream command-writer instructions. Original imports were linked to strcmp, strlen and memcpy. Backed-up trial and independent trial/main reopening verified persistence, successful decompilation and unchanged original code and archives.

Forty-two native calls across six scenarios checked NULL and duplicate labels, label interning, active-region changes, 64-label and 2,048-byte storage limits, region counters and exact seven-word commands. Scratch ABI shims called the host C runtime for string operations. Failed command emission still advances region state, so repeating the same label does not reemit that command. Overall region-array capacity, concurrency and exact GPU event semantics remain unresolved. Counters represent dispatch-wrapper attempts, not completed GPU work.

Totals: 555 reviewed names; 1,978 mapped and 7,610 unmapped among 9,588 discovered functions.

### Shared volume and item resource recycling

Saved DrainRetiredVolumeAndItemResources with an opaque caller-held mutex parameter and void return. All 206 original instructions were read and byte matched. Backed-up trial and independent trial/main reopening verified persistence, successful decompilation, unchanged instruction bytes and unchanged archives. The existing QueueAgedCacheEntriesForRelease name was preserved and is not counted again.

Six primary-pool scenarios checked exact volume resets, block-release arguments, list unlinking and bitmap clearing. Eight secondary-pool scenarios checked 16-byte item compaction, surviving offsets, total counts and bitmap/list state, including multiple releases in different orders. The drain temporarily unlocks for payload cleanup and relocks for list/bitmap changes. Block release and mutex/thread calls were controlled fixtures; actual integration and concurrency remain unverified.

Follow-up evidence for the existing retirement helper covers 288 generation/budget cases and 40 payload-hash cases, including wraparound and collision backshifts. A zero initial budget can still retire an eligible head before the budget check. Eighty callback/pending-list scenarios cover reference counts, allocation rollback and exact links. Pending IDs keep their bitmap bits until the retired drain clears them. This pool is shared with object-cache consumers and is not a sculpt-exclusive allocator. Producer constraints, pressure/wait recovery and malformed-pool behavior remain unresolved.

Totals: 556 reviewed names; 1,979 mapped and 7,609 unmapped among 9,588 discovered functions.

### Multi-item volume build and reuse slots

Saved BuildAndReuseVolumeResourcesForSlot with a uint slot, low-byte reuse flag, uint minimum level count and uint status return. All 2,109 original instructions were read and byte matched, with 347 direct branch targets checked. Both inbound calls, callback initialization, complete cleanup branches and the build-pipeline/output-packing calls were traced. Backed-up trial and independent trial/main reopening verified signature storage, successful decompilation and unchanged original bytes and archives.

Twelve original-code empty-input cases checked both slots and reuse modes, output sentinels and counter resets. Twenty populated reuse-only cases checked previous-slot lookup, duplicate reference retention, inactive-item sentinels, output order and preservation of the previous list. A missing constant page in the first reuse harness run was corrected by mapping original file-backed data; the passing run does not indicate a game fault. New-item GPU build paths received static review, but their resulting geometry has not been executed or verified.

The caller packs relative coordinates, selects build levels, invokes RunBricker2BuildPipeline for new items and transfers successful volume results through CopyAndPackGpuVolumeResource. Its scale uses a quarter-step mantissa with a power-of-two exponent through ldexpf. Failure cleanup and caller retry handling were traced; producer constraints, capacities, ownership, concurrency and retry termination remain unresolved.

A separate follow-up connected the original retired-resource drain to the original brick-block allocator in six scenarios, replacing the earlier block-release fixture. Exact free lists, metadata, links, volume resets and bitmap changes matched for these synthetic pools. Real concurrent integration and producer constraints remain unverified.

Totals: 557 reviewed names; 1,980 mapped and 7,608 unmapped among 9,588 discovered functions.

### Volume-slot build descriptors and allocation rollback

Saved BuildVolumeSlotDescriptor with a uint slot and opaque output pointer. All 116 original instructions were read and byte matched. Fifty-four original-code cases covered both slots, three sentinel patterns and counts around vector/scalar boundaries. All 268 output bytes, untouched holes, guards and source preservation matched. Backed-up trial and independent trial/main reopening verified persistence, signature storage, successful decompilation and unchanged original code and archives.

The builder counts item entries marked -2 and writes separate sentinel and other-item counts, then copies selected slot/global fields. Some source loads extend beyond the indexing stride; aggregate ownership remains unresolved. This is not evidence of an overflow defect. The output remains opaque rather than asserting an unproven full structure layout.

Follow-up tests entered the original multi-item caller’s new-item failure branch. Twelve zero-capacity cases checked relative 10-bit XYZ packing, status 2, output sentinels and cleanup. Eight partial-allocation cases allocated one ID before exhaustion: rollback left it zero-reference pending with its bitmap bit retained until retirement, while caller output and temporary counters were cleared. These tests used original allocation/release callbacks and controlled synchronization; they did not enter a successful GPU build. Producer constraints, real concurrency and new geometry remain unverified.

Totals: 558 reviewed names; 1,981 mapped and 7,607 unmapped among 9,588 discovered functions.

### Temporary volume build resources

Saved InitializeVolumeBuildTemporaryResources with an opaque context pointer after reviewing and byte matching all 322 original instructions. It initializes ten typed resources, calls the existing hash resource initializer, and requests seven further buffers. Backed-up trial and independent trial/main reopening verified the saved signature, unchanged original code and archives, and successful decompilation.

Original-code fixtures exercised all 512 combinations of nine optional allocation outcomes. They checked ten requests per scenario, selected hash capacity, all 84 hash parameter bytes, zero descriptors after failed allocations, element counts for the seven later successful descriptors, resource headers and boundary guards. Failed optional allocations did not prevent later requests.

The allocator was controlled and format globals were fixture values. The parameter allocation remained successful: the real allocator can return NULL, while subsequent hash setup dereferences the pointer unconditionally. Runtime capacity guarantees remain unresolved; no actual game fault is established. This does not verify actual GPU allocation, complete successful volume builds, resource destruction or concurrency.

Totals: 559 reviewed names; 1,982 mapped and 7,606 unmapped among 9,588 discovered functions.

### Volume and item capacity reclamation

Saved ReclaimVolumeAndItemCapacity with two unsigned request counts and a one-byte success result. All 154 original instructions were read and byte matched; two inbound sites support the units and return contract. It computes separate volume and item pressure, retires weighted aged candidates, waits for a generation change while candidates remain, then drains retired resources before unlocking. Empty candidates with remaining pressure produce failure.

Native checks covered 85 no-pressure cases, 80 weight callback cases, nine controlled pressure paths and nine repeated-wakeup cases. Unchanged generation after early wakeups keeps the loop waiting; a changed generation allows retry. An initial branch-offset defect in the scratch wait fixture was corrected before the passing rerun; it was not a game fault. Backed-up trial and independent trial/main reopening verified the saved name and signature and unchanged code and archives.

Pressure fixtures replace retirement, drain and synchronization callees. They establish control flow, not real concurrent execution or connected GPU builds. The volume weight subtractand, upstream bounds and runtime capacity guarantees remain unresolved.

Totals: 560 reviewed names; 1,983 mapped and 7,605 unmapped among 9,588 discovered functions.

### Connected capacity reclamation follow-up

The existing capacity-reclamation review now includes connected original-code checks: 16 cases through retirement and weight callbacks, six through the primary drain, six through original brick-block release, and eight through secondary item compaction. These are separate fixture groups, not 36 end-to-end game runs.

Primary checks verified resource bitmap clearing, retired queue removal, restored self-links and exact block-pool metadata and links. Secondary checks verified item bytes, surviving offsets, total counts, removed records and resource ID release. Insufficient capacity returns failure after reclaiming the available candidates. Synchronization remains controlled; real concurrent scheduling, runtime producer guarantees and GPU workloads remain unverified. No new function names or completion credit were added.

### Volume and item summary refresh

Saved RefreshVolumeAndItemSummaryRecords with an opaque persistent context and optional ID-filter pointer. All 368 original instructions were reviewed and byte matched; two bounded callers support the working signature. Backed-up trial and independent trial/main reopening verified the name, signature and unchanged original code and archives.

197 native refresh cases cover empty active sets, generation and filtering, valid/invalid volume IDs, existing matches, lower-bound edges and two-ID retained/regenerated merges. A separate 35-case original small-sort fixture verifies unsigned key/discriminator ordering and exact copied bytes. Empty active sets clear the logical count while preserving storage. Older-generation valid resources regenerate summary fields; current/newer entries retain lower-bound positions. Synthetic mismatched keys can therefore retain a different existing record; caller key-set invariants remain unresolved, and no reachable game defect is claimed.

Defined capacity, item-count and vector fields, source preservation, output bounds and guards matched. Generated bytes 9 through 11 were not asserted; the final four bytes stay at their array positions. Synchronization and memset are controlled scratch fixtures. A Windows stack-probing adaptation was needed for the original large stack frame. Larger sorting paths, full producer bounds and real concurrency remain unverified.

Totals: 561 reviewed names; 1,984 mapped and 7,604 unmapped among 9,588 discovered functions.

### Adaptive summary-record sorting

Saved AdaptiveStableSortSummaryRecords, BufferedStableSortSummaryRecords and AdaptiveMergeSummaryRecordRuns with register-verified working signatures and opaque scratch contexts. All 1,409 original instructions were reviewed and byte matched. The buffered helper sorts 32-record chunks then merges runs; the adaptive helper uses fitting-side scratch or split/search/three-reversal rotations when scratch is insufficient. Equality handling preserves stable order. Lazy allocation retries halve record capacity until success or zero.

323 native cases cover 35 small sorts, 30 buffered large sorts, 120 limited-scratch sorts, 30 controlled allocation failures and 108 direct uneven-run merges. Exact copied record bytes, unsigned key/discriminator order, stable duplicates, positional trailing bytes and input/scratch guards matched. Backed-up trial and independent trial/main reopening verified all three names and signatures, unchanged machine code and original archives.

Valid sorted adjacent runs, consistent counts and nonoverlapping scratch are preconditions. Allocation failure was controlled, not real allocator exhaustion. Runtime producer bounds, complete scratch ownership/types and concurrency remain unresolved.

Totals: 564 reviewed names; 1,987 mapped and 7,601 unmapped among 9,588 discovered functions.

### Metadata sequence and deferred cleanup follow-up

Registration assigns the next sequence to metadata and increments it. The summary generation is selected through a caller snapshot from a metadata-list head, or the sequence fallback when the sentinel is reached; a marked current entry can be skipped once. This is not a demonstrated frame number or whole-build completion percentage. List ordering, reset and wrap behavior still constrain interpretation.

54 cross-word refresh cases passed at IDs 31/32, 63/64 and 127/128. The already named ReleaseMarkedObjectCacheReferences received stronger evidence: 30 basic/current-entry cases, eight connected resource-release cases and 16 auxiliary occupancy cases. Current entries remain requested with a deferred flag; ordinary entries clear state, release volume/item references, queue zero-reference resources and unlink metadata. The existing name was preserved with no additional naming credit.

A 399-instruction preparation helper selects candidates absent from two exclusion bitmaps, removes hash entries and adds release requests. Twenty disjoint-buffer/empty-hash cases verified all bitmap bytes and guards. Its optional callback is initialized to NULL by overlapping stores that exact-address reference lookup missed; later indirect assignments remain unexcluded. Hash collision deletion, alias fallback and real concurrent cleanup remain unverified.

### Unselected build metadata release queue

Saved QueueUnselectedBuildMetadataForRelease after reviewing and byte matching all 399 original instructions and tracing both mutex-acquiring callers. It selects metadata absent from two exclusion bitmaps, removes corresponding hash entries, clears the selected active bits and adds release requests. Backed-up trial and independent trial/main reopening verified the no-argument working signature and unchanged original code and archives.

108 native cases cover 20 disjoint bitmap selections, 56 exact whole-buffer aliases and 32 three-slot collision/callback scenarios. Exact bitmap bytes, independent metadata hashes, backward shifts, slot values/padding, table counts and guards matched. Collision homes cover all eight positions, including wraparound. The optional recording callback observed the final vacated slot before its fields were cleared.

Observed startup initializes the optional callback to NULL through overlapping stores; later alias assignments remain unexcluded. Synthetic alias cases establish instruction behavior, not valid runtime layouts. Partial overlaps, mixed-home/full-table collisions, complete producer ownership and real concurrency remain unverified.

Totals: 565 reviewed names; 1,988 mapped and 7,600 unmapped among 9,588 discovered functions.

### Build metadata lookup and registration

Saved GetOrRegisterBuildMetadataEntry after reviewing and byte matching all 522 original instructions. Three bounded callers support a 16-bit ID result and three unsigned argument registers. The third argument stays uint in the working signature because hashing uses its full value, although observed callers zero-extend a byte or pass zero. Backed-up trial and independent trial/main reopening verified the name, signature and unchanged original code and archives.

217 native scenarios cover 128 lookup/exhausted-ID cases, 24 new registrations, eight append/relookup scenarios, nine resource revivals, 24 insertion-threshold cases and 24 collision insertions. Exact metadata bytes, sequence wrap, queue links, ID bitmaps, dirty flags and independently modeled hash displacement matched. Active cached resources gain references; pending resources revive and unlink before reuse.

At hash count equal to its mask, synthetic fixtures register metadata without inserting its hash entry. Actual runtime reachability remains unresolved; this is not a confirmed game defect. Optional insertion callback, deferred-request removal, complete caller constraints and real concurrency remain unverified.

Totals: 566 reviewed names; 1,989 mapped and 7,599 unmapped among 9,588 discovered functions.

### Connected registration lifecycle and source leads

Fourteen existing-entry cases verified removal of the first matching object index from the deferred list, including exact compaction and untouched tail bytes. Twenty-four insertion-callback cases verified one call with the selected slot and size 16 before the final fingerprint and ID are installed. Original SELF symbols and relocations resolve the relevant imports to memmove, memcpy and scePthreadCondBroadcast; identity resolution does not establish real platform synchronization.

Eight scenarios connected original registration, release preparation and marked cleanup with two metadata entries and all selection masks. Complete metadata bytes, surviving queue links, freed self-links, hash mappings/counts and allocated/active/request bitmaps matched. Sequence wrap persisted without cleanup incrementing the registration sequence. Cached payload release was tested separately; this combined fixture uses empty resource hashes and controlled synchronization.

Media Molecule's [SIGGRAPH 2015 presentation](https://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf), pages 21 and 110, supplies stage terminology and GPU block-sizing leads. Sweep/bricker terminology supports the independently traced pipeline structure. Its 64-thread GPU blocks do not establish the meaning of this executable's 64-unit CPU allocations. Earlier research material is not an exact source or build match. No new names or completion credit were added.

### Explicit build metadata resource release

Saved ReleaseBuildMetadataEntryResources after reviewing and byte matching all 148 original instructions. It releases auxiliary occupancy, optional volume-ID lists and direct volume/item references; zero-reference resources enter pending queues. It unlinks metadata and clears allocation/active/request bits. Two bounded caller windows pass a current metadata ID when its deferred flag is set, then reset current globals afterward. The helper itself has no mutex or current-ID deferral guard.

32 isolated native cases cover eight direct release cases, eight connected scanner-to-explicit-cleanup cases and sixteen auxiliary occupancy cases. Current-entry deferral preserves references until explicit cleanup releases them once. Backed-up trial and independent trial/main reopening verified the working void(uint metadata_id) signature, unchanged code and unchanged source archives.

Valid IDs and list links remain preconditions. Complete caller synchronization, lifetime constraints, malformed metadata and actual concurrent gameplay are unverified. This is descriptive semantic review, not proof of subsystem completion.

Totals: 567 reviewed names; 1,990 mapped and 7,598 unmapped among 9,588 discovered functions.

### Retirement of all aged pending cache entries

Saved RetireAllAgedPendingCacheEntries after reading and byte matching all 151 original instructions. It traverses the pending list at sentinel capacity+1, selects records whose unsigned generation age is at least two, clears their state and appends them to the retired list at capacity+2. It continues past younger records and has no retirement budget or weight callback. Selected state-two records also lose their hash entry through collision backshifting and an optional deletion callback.

88 isolated native cases cover 48 age/list cases and 40 hash/callback cases, including generation wrap, young entries preceding old entries, collision wraparound and missing hashes. Exact queue links, hash key/value slots, occupied counts and callback slot pointers matched the independent fixture model. Backed-up trial and independent trial/main reopening verified the saved working signature and unchanged original code and archives.

Valid lists and hash invariants remain preconditions. Full caller synchronization, malformed state and actual concurrent gameplay are unverified. Two metadata processing lists are now observed, but their higher-level phase names and transitions remain under investigation.

Totals: 568 reviewed names; 1,991 mapped and 7,597 unmapped among 9,588 discovered functions.

### Cache slot allocation with retirement

Saved AllocateCacheResourceSlotWithRetirement after reading and byte matching all 318 original instructions. It selects the first free bitmap ID below capacity and initializes a zero payload, one reference, active state and self-links while preserving generation. When full, it retires eligible pending entries, removes state-two hash entries and retries after draining. The capacity+1 pending list has priority; the capacity list is considered when the first list is empty. Young pending entries cause waits until shared generation changes. Empty candidate lists log and return UINT_MAX.

117 isolated native cases cover 22 immediate allocations, 15 pressure/wakeup/exhaustion cases and 80 hash/callback cases across both pending-list branches. Collision wraparound, missing hashes, exact callback slot pointers and repeated unchanged-generation wakeups were checked. Backed-up trial and independent trial/main reopening verified the name, working signature and unchanged original bytes and archives.

Drain, logging and condition wait were controlled in scratch. Actual resource destruction, real concurrency and complete caller constraints remain unverified. Valid bitmap, list and hash invariants are preconditions. An initial test-stub execute-permission error was corrected before the pressure cases passed; it was not a game defect.

Totals: 569 reviewed names; 1,992 mapped and 7,596 unmapped among 9,588 discovered functions.

### Older metadata lookup by descending discriminator

Saved FindOlderBuildMetadataByDescendingDiscriminator after reading and byte matching all 128 original instructions. Under the shared mutex it hashes the indexed object pointer with key variant zero and searches discriminator values from the supplied maximum down through zero. It returns the first matching metadata ID whose unsigned generation is below the snapshot threshold, or low-word FFFF. Two bounded callers supply a zero-extended discriminator byte and compare the returned AX to FFFF, supporting the saved ushort working result type.

1,280 isolated native cases matched the independent registration hash and descending selection model across missing variants, generation thresholds and consistent collision tables. Metadata and hash bytes remained unchanged. Backed-up trial and independent trial/main reopening verified the saved name, signature and unchanged original bytes and archives.

The discriminator remains a descriptive field name; its higher-level Dreams meaning is not established. Tests use four discriminator values, four pointers and controlled synchronization. Malformed state, complete caller constraints and actual concurrent gameplay remain unverified.

Totals: 570 reviewed names; 1,993 mapped and 7,595 unmapped among 9,588 discovered functions.

### Object replacement notification for metadata refresh

Saved QueueObjectReplacementForMetadataRefresh after reading and byte matching all 94 original instructions. Under the shared mutex it processes old then new object IDs, skipping FFFFFFFF and duplicates. The 16-entry deferred-request list evicts its oldest entry before appending when full. If the current-object ID equals the old ID, it changes to the new ID. This connects object replacement to deferred filtering already observed in registration and scheduling.

784 isolated native cases matched an independent bounded-list model for counts zero, one, fifteen and sixteen; sentinel IDs, duplicate ordering, eviction and current-object equality were checked against exact full list storage. Backed-up trial and independent trial/main reopening verified the name, signature and unchanged original code and archives. Host memmove was adapted to the original calling convention; synchronization was controlled. Valid list counts and object lifetimes remain preconditions, and actual concurrent mutation is unverified.

Related local followups also tested original registration followed by query in 48 registration scenarios and 432 queries, and metadata handle promotion in 101 base cases plus 72 dirty-bit/auxiliary cases. Later object replacement and re-registration branches remain under investigation; no additional name credit is assigned for these followups.

Totals: 571 reviewed names; 1,994 mapped and 7,594 unmapped among 9,588 discovered functions.

### Metadata promotion and object resource refresh

Saved PromoteBuildMetadataAndRefreshObjectResources after reading and byte matching all 171 original instructions. It promotes a generation-qualified candidate metadata handle to the stored handle, clears a bounded dirty bit and conditionally invalidates an auxiliary record. A later volume-field comparison can rebuild the CSG object, notify old/new replacement, propagate the replacement to a linked type-one object and re-register metadata with the previous key fields. Two bounded callers supply context/object pointers and a packed object index, and ignore a return value.

247 isolated cases cover 101 base promotions, 72 dirty-bit/auxiliary cases, 28 resource guards, six rebuild orchestration cases, 36 linked-object lookups and four registration-failure cases. Exact handles, relevant state buffers, controlled callee arguments, collision paths and deferred notifications were checked. Backed-up trial and independent trial/main reopening verified the saved name, signature and unchanged original bytes and archives.

Rebuild and registration were controlled in orchestration fixtures. Actual connected CSG execution, complete lifetime/synchronization constraints and source field meanings remain unverified. Valid pointers and the linked type-one object invariant are preconditions. Controlled registration failure preserves the previous stored metadata handle after object replacement; actual failure reachability is unresolved.

Totals: 572 reviewed names; 1,995 mapped and 7,593 unmapped among 9,588 discovered functions.

### Packed resource node allocation and copying

Saved AllocateOrCopyPackedResourceNode after reading and byte matching all 209 original instructions. Under the shared node-pool mutex it searches 4,096 bitmap words from a rotating cursor, allocates the first clear bit and marks both allocation and dirty bitmaps. Nodes are 512 bytes. A supplied source ID copies the node and replaces header category bits; a missing source creates a zeroed node with requested leaf/category flags. No reference-count operation appears in this body.

387 isolated cases cover 384 allocation/copy combinations and three exhausted-pool diagnostics. Exact node bytes, preserved source, complete bitmaps, cursor and thread-owner fields were checked, including final node ID 262143 and cursor wraparound. Exhaustion returns UINT_MAX, preserves allocation state and counts fourteen header categories plus other entries across the original diagnostic scan. Backed-up trial and independent trial/main reopening verified the name, working signature and unchanged original bytes and archives.

Host memcpy was ABI-adapted; synchronization and logging were controlled. Valid source IDs and lifetimes remain preconditions. Actual allocation races, complete caller flag bounds and end-to-end writer ownership remain unverified. Related local followups read writer initialization and finalization and tested multi-leaf rebuild traversal without additional name credit.

Totals: 573 reviewed names; 1,996 mapped and 7,592 unmapped among 9,588 discovered functions.

### Packed resource node interning

Saved InternPackedResourceNodeByFingerprint after reading and byte matching all 119 original instructions. It hashes complete leaf nodes or ordered child fingerprints, inserts a candidate into the shared fingerprint table, or selects an existing matching node. Existing selection marks the node dirty and releases a different candidate. The routine does not perform a full byte-equality check after a fingerprint match.

121 isolated scenarios cover 248 original interning calls: forty controlled hash/release cases, forty with original release, thirty-two connected original-hash/release scenarios and nine longer/mixed collision sequences. Full table state was compared against an independent Robin Hood model, including wraparound and displacement. The original XXH64 routine separately matched 600 independent reference cases. Backed-up trial and independent trial/main reopening verified the name, signature and unchanged original bytes and archives.

Valid IDs, table capacity and node lifetimes remain preconditions. Actual concurrency, full-table behavior and adversarial fingerprint collisions remain unverified. Writer append/finalization ownership is still being traced. These results support the descriptive role, not completion of the entire subsystem.

Totals: 574 reviewed names; 1,997 mapped and 7,591 unmapped among 9,588 discovered functions.

### Packed resource tree writer growth

Saved GrowPackedResourceTreeWriter after reading and byte matching all 96 original instructions. It finalizes an active node, updates its parent link, allocates a fresh path node and reserves room in the parent. Full 126-child parents cause growth to cascade upward. Growing beyond the root shifts the writer path and creates a two-child root.

Twelve connected growth cases verified a root leaf split, a parent with room and a full-parent cascade using original allocation, hashing, interning and release. Four full-pool cases checked first replacement allocation failure: the old node is finalized, the active slot becomes UINT_MAX and depth stays unchanged. Backed-up trial and independent trial/main reopening verified the name, signature and unchanged original code and archives.

The complete local CSG rebuild chain also passed 63 scenarios covering 1,305 records, including eighteen requiring growth. Original decoding, clamping, delta encoding, allocation, growth, summaries, hashing, finalization and release ran together. Independent output decoding, node summaries, fingerprints and exact reachable allocation/dirty sets matched; source blocks were unchanged. These cases cover kind-zero records and small valid trees.

Platform synchronization/logging were controlled and host memcpy/memmove ABI-adapted. Other record kinds, real concurrency/game integration, new-root allocation failure and depth-limit contracts remain unresolved. No whole-subsystem completion is claimed.

Totals: 575 reviewed names; 1,998 mapped and 7,590 unmapped among 9,588 discovered functions.

### CSG rebuild working signatures and mixed records

Refined three existing functions without new naming credit: RebuildPackedCSGRecordsWithMetadataOffset now has a uint root ID, two int working metadata arguments and a uint root result; InitializePackedCSGRecordWriter has writer/source-root arguments and a void working result; FinalizePackedResourceTreeWriter has a writer argument and uint root result. Rebuild arithmetic uses only the signed low byte of each int input. Backed-up trial and independent trial/main reopening verified all three signatures, unchanged names and unchanged original code and archives.

The complete original local rebuild chain additionally passed 36 mixed-kind scenarios covering 621 records of kinds 0, 7, 12 and 22. Primary payloads, kind-7 extensions, output order, metadata clamps, summaries, fingerprints and exact reachable allocation/dirty sets matched independent checks. Source blocks stayed unchanged. Together with the earlier kind-zero cases, this covers 99 complete-chain scenarios and 1,926 records.

These are analyst-supported working types and controlled local tests. Full payload field meanings, all optional combinations, real game integration, concurrency, allocation-failure recovery and depth-limit contracts remain unresolved. Reviewed-name total stays 575.

### Teleporter object callback integration and flag propagation

The original transform dispatcher, graph iterator, hierarchy helper, object callback adapter and object flag setter passed 80 connected native scenarios. All three supplied graph objects received flag bit 15 while the two shared runtime bodies retained their expected mode-specific transform and vector results. The separate body callback channel was disabled. These fixtures use controlled platform services, valid supplied graphs, finite unit rotations and positive scales; they are not live-game tests.

A separate seven-instruction block passed 120 native scenarios. It conditionally copies bit 15 from a nonnull source object's flags into destination flags using OR, preserving existing destination bits, unrelated bytes and source data. Static pointer setup links the source to a cached world object and the destination to incoming storage plus the flags offset. The enclosing 5,457-instruction routine has not been fully reviewed, so its role and the gameplay meaning/lifetime of bit 15 remain unresolved.

No additional function names or completion credit were added. Current totals remain 594 checked names and 2,010 mapped functions among 9,589 discovered functions.


### Object and runtime-body transform evaluation

Saved EvaluateObjectBodyTransform with a conservative four-input working signature after reading and byte matching all 290 original instructions. Without an associated body, it copies the object transform selected by kind metadata. With a body, it can interpolate transforms, apply translation and axis-angle corrections, then compose the association local transform. Zero translation correction skips angular correction even with nonzero angular inputs.

560 original entry-to-return scenarios matched independent equations: 192 baseline, 112 interpolation, 128 correction and 128 combined cases. Source buffers and output guards were preserved. Original __isinff ran; sinf/cosf were supplied by host UCRT after import resolution. A compressed project backup and independent reopening verified the saved name/signature and unchanged original game archives.

These are controlled finite inputs with valid references, unit rotations and positive scales. Exact PS4 trigonometric results, exceptional inputs, every world-gate combination, full callers, concurrency and live-game integration remain unverified. The related object flag still has no proven gameplay name.

Totals: 595 checked names; 2,011 mapped and 7,578 unmapped among 9,589 discovered functions. Naming and these scoped checks do not mean whole-game completion.

### Transform selection and indexed transform powers

224 connected selector cases establish supplied-transform, body fallback, cached-parent and recursively evaluated parent paths. In the tested parent paths the result is evaluated-parent times inverse stored-parent times supplied transform. A further 64 cases cover two auxiliary numeric kinds: cached transform is applied before the supplied transform when object flag 15 is clear, while a set flag bypasses that operation. These numeric kinds belong to the auxiliary record and are not automatically object-kind names.

The related 458-instruction helper was read and matched to original bytes. 272 cases establish repeated-transform and identity-return paths. Another 170 cases establish inverse fractional translation, scale and pure rotation. 144 coupled cases satisfy the independent matrix relation output^selector = inverse(input)^(selector-step), using matrix multiplication and Gauss-Jordan inversion. This supports the fractional-transform role within sampled branches; the relation alone does not uniquely choose every matrix root.

Tests use valid controlled records, finite transforms and positive scales. Host math adapters supply several imports, so exact PS4 math is unverified. Full selector branches, auxiliary field meanings, flag lifetime, exceptional inputs and real game execution remain unresolved. The selector fixtures were corrected to allocate the entire accessed context; the earlier 224 cases were rerun successfully and their receipts superseded. No new name or completion credit was added for these checkpoints.


### Indexed repeat transform helper

Saved ComputeIndexedRepeatTransform with a conservative custom-register working signature after reading and byte matching all 458 original instructions. Negative selectors at most -2 produce the supplied transform raised to step minus one for positive step. Small selector magnitudes and nonpositive steps produce identity. Positive selectors produce identity when step reaches the selector; interior steps produce an inverse fractional transform in the tested branches.

586 original entry-to-return cases cover repetition, identity, translation, scale, rotation and coupled transforms. Independent matrix arithmetic and inversion verify the coupled power relation; separate pure cases constrain the rotation branch. Two additional game-update/physics caller windows confirm signed selector, step and transform-register inputs. Backup and independent project reopening verified the saved name/signature; original game archives remain unchanged.

These are sampled finite positive-scale transforms. Host adapters supplied several math imports; exact PS4 library behavior, extreme integer selectors, exceptional or singular transforms, original field meanings and live-game behavior remain unresolved. No whole-subsystem completion is claimed.

Totals: 596 checked names; 2,012 mapped and 7,577 unmapped among 9,589 discovered functions.


### Existing object-transform getter ABI correction

Retained the existing GetThingTransform name and corrected its saved two-input fastcall declaration to a conservative four-pointer PS4_SYSV working signature: output transform, world, object and optional context. The original record wrapper supplies those inputs in RDI/RSI/RDX/RCX. 64 connected original wrapper/getter/composer cases match independent ordinary object/local-record transform composition with source and output guards preserved.

A verified compressed backup, unchanged original archive hashes, independent project reopening and fresh local decompilation confirm the correction. Special records, packed rotations, invalid inputs, exact source types and complete getter semantics remain unresolved. No naming or semantic-completion credit was added; checked-name total stays 596.


### Record transform resolution

Saved ResolveRecordTransform after reading and byte matching all 50 original wrapper instructions. It resolves the record object reference, obtains its transform, then calls the existing record-composition helper with an optional frame context. Ordinary records compose object and local transforms; record kind 3 with a frame context instead selects an indexed slot and composes it with the context transform.

208 connected original wrapper/getter/composer cases cover ordinary composition, indexed context selection and signed-scale handling. A negative ordinary product scale becomes positive and its quaternion is right-multiplied by a 180-degree X rotation. This is a specific convention, not equivalence to general negative-scale 3D transforms. Distinct source inputs and output guards were checked. A verified compressed backup, independent reopening and fresh decompilation confirm the saved name and conservative four-pointer working signature.

Special getter records, packed rotations, invalid references or slots, original record field meanings, full lifecycles and live-game integration remain unresolved. This names the wrapper without claiming completion of its callees or subsystem.

Totals: 597 checked names; 2,013 mapped and 7,576 unmapped among 9,589 discovered functions.


### Quaternion orientation snapping

Saved SnapQuaternionToOrientationSet after reading and byte matching all 279 original instructions. It chooses the closest quarter-turn orientation by absolute quaternion dot score and aligns the output sign with the input. Mode 8 also considers positive and negative 45-degree offsets about each axis.

128 original entry-to-return cases match an independently generated candidate set, nearest score and hemisphere, with guarded input/output. A verified compressed backup, independent reopening and fresh decompilation confirm the mode input and XMM0 quaternion input/return. The 16-byte register container is an analyst working type. Host sin/cos supplied the trigonometric import; exact PS4 math, ties, nonunit or exceptional inputs and real-game behavior remain unresolved.

Additional frame reconstruction evidence now binds original Animation, Microchip, Timeline, Sound and Scripter types to runtime record categories 6, 2, 3, 4 and 5. 200 connected cases verify category/ID matching and world fallback. Another 384 scoped cases examine nonzero extra-field coordinates, rotations, metadata dimensions, offsets and Timeline-specific scaling. These do not establish full frame-helper semantics or original field names. Timeline numerical checks use a documented vector-scale error bound; maximum observed relative vector error was approximately 0.000000505.

Totals: 598 checked names; 2,014 mapped and 7,575 unmapped among 9,589 discovered functions. Only the quaternion helper adds new naming credit here.


### Native test harness math ABI audit

An additional frame test exposed a harness error: Windows scalar math functions had been called directly from PS4 code without the Windows 32-byte shadow area. Some host calls could overwrite the PS4 caller scratch data. Scalar math adapters now reserve the required area and stack alignment before calling the host implementation.

All 924 affected cases were rerun successfully with corrected adapters, including body correction, indexed transform powers and transform snapping. The additional 64 translated/rotated/scaled-frame hysteresis cases also pass. The apparent nonidentity-frame counterexample and its old register traces are superseded as harness artifacts, not game behavior. Earlier naming credit is unchanged; these are revalidation checks, not additional reviewed functions. Exact PS4 math implementations and untested input domains remain unresolved.


### Relative transform snapping with hysteresis

Saved SnapRelativeTransformWithHysteresis after reading and byte matching all 690 original instructions. It converts the desired transform into the reference frame, rounds position to a power-of-two grid, rounds scalar scale to a signed power of two, and snaps rotation through the verified quaternion helper. A stack flag selects whether grid size uses the supplied source-frame scale or a fixed factor of four.

With a prior relative transform, the tested position retention window is 0.7 grid cells per axis, and the angular window is 0.9 times 360 divided by orientation mode in physical degrees. The desired scale supplies output scale. Both mutable buffers finish with the final transform.

372 original entry-to-return cases cover baseline, translated/rotated/scaled frames, both grid sources, and independent prior poses. Expected results use independent inverse/composition, grid and orientation-candidate calculations with source/output guards. Host math adapters include the corrected Windows shadow space. Backup, independent reopening and fresh decompilation confirm the working eight-input signature, including typed 32-byte transform pointers, SIMD scalar and stack flag. Exact PS4 math, threshold ties, exceptional inputs, aliasing and real-game integration remain unresolved.

Totals: 599 checked names; 2,015 mapped and 7,574 unmapped among 9,589 discovered functions. This does not establish whole-game or whole-subsystem completion.


### Object auxiliary-frame reconstruction

Saved ComputeObjectAuxiliaryFrameTransform after reading and byte matching all 669 original instructions. It selects an identity or stored object frame at initial gates, otherwise reconstructs an auxiliary-relative frame from parent/object data, runtime record lookup, metadata dimensions and offsets. Original type registration binds Animation, Microchip, Timeline, Sound and Scripter parents to record categories 6, 2, 3, 4 and 5. Matching current-world records take priority over alternate-world fallback.

992 scoped scenarios cover stored/repeat frames, category lookup, nonzero extra-field coordinates, rotations, metadata dimensions and offsets, Timeline scaling, snapping integration and 200 paired parent-override cases. The override cases use an invalid child parent reference with a valid explicit parent and match the normal lookup result. Connected snapping tests use the original relative-transform and orientation helpers. Source buffers and output guards were checked.

Backup, independent reopening and fresh decompilation confirm the descriptive name and seven-input working signature, including typed 32-byte output and a stack parent override. Selected auxiliary index zero, finite valid records and sampled positive scales are tested. Remaining type-specific modes, original field names, arbitrary indices, malformed or aliased inputs, full lifecycles, exact PS4 math and live-game integration remain unresolved. Timeline calculations retain their documented numerical bounds; host math uses corrected shadow-space adapters.

Totals: 600 checked names; 2,016 mapped and 7,573 unmapped among 9,589 discovered functions. These counts do not mean whole-game or whole-subsystem completion.


### Transform selection: cached frames and eligibility gates

368 additional scoped scenarios exercise the original transform selector from entry to return. In 144 cases, a one-based object frame slot selects one of three cached transforms and combines it with the supplied transform. A nonzero object mode or the excluded object kind bypasses that combination. These tests use distinct inputs and check source buffers and output guards.

Another 224 cases check the auxiliary-kind eligibility masks and the secondary record-field condition when the selector equals the repeat step. Nonzero group, global-slot or record gates each bypass cached-frame composition. Synthetic kind codes establish branch behavior, not recovered enum names or proof that every code is valid in-game.

These findings add no checked name and no whole-function completion claim. Tests cover valid object index zero, selected slots, finite unit rotations and positive scales. The body-linked branch, remaining selection modes, exact field meanings, malformed inputs and live-game lifecycle remain unresolved.


### Body-linked transform selection

64 isolated helper scenarios and 128 connected selector scenarios verify a stored-transform path using original code. The helper combines a stored transform with the linked object's local transform. The selector replaces the resulting scale with the parent scale, then applies the inverse reference transform and supplied transform.

The two tested object modes differ in that reference: mode 2 uses the parent transform; mode 1 substitutes the runtime body's XYZ position while retaining the parent's scale and rotation. Distinct random inputs, independent transform equations, unchanged source buffers and output guards were checked. The connected 128-case set supersedes the preliminary 64-case set; those preliminary cases are not counted again.

This is scoped behavior evidence, with no new checked name. The linked object kind, metadata offsets, auxiliary slot/group, association and stored-state gates were controlled. Finite unit rotations and positive scales were sampled. Other linked types, modes, original field meanings, full lifecycles, malformed inputs and live-game behavior remain unresolved.


### Linked-transform position factors

176 additional original-code scenarios verify two unstored transform paths. In 80 cases, position blends from the group position toward the state position, while scale and rotation come from the state transform. Sampled factors from -0.5 to 1.5 show extrapolation as well as interpolation. The resulting reference transform combines with the object's local transform.

In 96 cases, a present metadata field and nonzero object value replace that position factor with object value divided by group factor, the original float constant 0.4, and group scale. A deliberately different state factor confirms which source is selected. Independent transform equations, distinct inputs and source/output guards passed.

These paths were tested with controlled metadata, default group mode, identity auxiliary gates, finite unit rotations and positive scales. The metadata field's physical meaning and units, nondefault group rotation paths, other object types, zero/nonfinite denominators and live-game lifecycle remain unresolved. No checked-name credit is added.


### Linked-transform group offset

256 original-code scenarios verify the nondefault group path across four sampled state modes, two flag values and both signs of state scale. It shifts the state position along a rotated local Z direction, multiplied by the position factor and group scale. Negative state scale reverses that shift. State scale and rotation remain selected for the final local-transform composition.

The direction uses the state rotation followed by a local X-axis rotation: +45 degrees for sampled modes 0 and 1, -22.5 degrees for mode 2 with its flag clear, and zero for mode 2 with the flag set or mode 3. Independent quaternion/transform equations and source/output guards passed. This 256-case set supersedes the preliminary 128 cases, which are not counted again.

Controlled host sine/cosine uses the corrected calling-convention adapter; exact PS4 math is not claimed. Tests use absent metadata scaling and identity auxiliary gates. Other modes, combined metadata behavior, original field meanings and live-game lifecycle remain unresolved. No new checked-name credit is added.


### Auxiliary-gated transform sources

384 original-code scenarios verify the alternate path selected when either auxiliary vector differs from the identity vector. With a stored override, position, scale and rotation come from that stored transform. Without it, position comes from the group and scale/rotation from state. The selected rotation then right-multiplies the mode-dependent local X rotation before object-local composition.

Tests cross three auxiliary-gate patterns, four sampled modes, two flag values, both override states and both scale signs independently. Distinct random transforms, independent equations, unchanged source buffers and output guards passed. The final 384-case set supersedes preliminary sets, which are not counted again.

This establishes sampled branch and source selection, not the original names or types of the auxiliary fields. Default group mode, finite unit rotations and positive local scale were used. Nondefault group combinations, combined metadata behavior, exact PS4 trigonometry and live-game lifecycle remain unresolved. No new checked-name credit is added.


### Linked-transform target blending

288 original-code scenarios verify the direct target-transform blend and its gates. When enabled by the metadata boolean, matching state pointer and nonzero auxiliary factor, the helper clamps the factor to 0–1 and applies smoothstep. It blends all position/scale components and uses a normalized, hemisphere-aligned quaternion blend before composing the object-local transform.

Disabling the metadata boolean or mismatching the state pointer suppresses the blend across all sampled factors. Independent equations, distinct transforms, source buffers and output guards passed. Quaternion comparisons account for equivalent signs. This set supersedes the preliminary 96 cases, which are not counted again.

The tests use a stored override, default auxiliary kind/group mode, identity auxiliary gates and finite unit rotations with positive scales. Linked-reference kinds that invoke recursive selection remain unverified, as do original field names, invalid inputs and live-game lifecycle. No checked-name credit is added.


### Linked-reference target construction and recursion

256 original-code scenarios verify that the two tested linked-reference auxiliary kinds build the target from a referenced object's transform and an auxiliary offset. Missing transform metadata substitutes identity before offset composition. The target then feeds the verified smoothstep blend and local composition.

128 connected scenarios exercise the helper, transform selector and runtime body evaluator together. Distinct stored and runtime transforms show that recursion uses the runtime body result. A matching object-reference field bypasses recursion and uses the stored reference transform instead. Independent equations, source buffers and output guards passed. The final connected set supersedes its preliminary 64 cases.

Tests cover valid reference index one, controlled metadata, finite unit rotations, positive scales and one recursion level. Auxiliary lookup uses the empty-list fallback. Nonempty lookup matching, arbitrary depth, cycles, invalid references, original field meanings and live-game lifecycle remain unresolved. No new checked-name credit is added.


### Auxiliary lookup order and direction adjustment

128 connected lookup scenarios verify that auxiliary ID and group identity must both match. A mismatched first entry is skipped; when both entries match, the first wins. Distinct cached transforms prove which index reaches the selector. ID and group misses use the runtime-body fallback. Tests cover a controlled two-entry list and valid indices.

160 direction-mode scenarios verify a separate geometric path: it places the result a fixed distance from the group origin along the stored-position direction, and applies a shortest-arc rotation from the negative group-forward axis. Changing the object mode, state mode, state pointer or secondary-state gate individually suppresses that adjustment. Independent geometric equations, source buffers and output guards passed.

These final sets supersede their preliminary sets. Nonzero displacement, non-antipodal directions, positive scales and controlled default gates were used. Zero-displacement and antipodal fallbacks, signed group scale, metadata distance, arbitrary recursion and live-game lifecycle remain unresolved. No checked-name credit is added.


### Direction-mode degenerate inputs

64 original-code edge scenarios further bound the direction mode. In 32 near-antipodal cases, the routine uses a fixed world-X half-turn before the stored rotation. This fallback must not be described as a general shortest-axis solution. Both group-scale signs were sampled.

In 32 exact-zero-displacement calls, output XYZ became NaN while scale and rotation remained finite. Source buffers and output guards were preserved. This describes an isolated controlled path; it does not establish that live callers permit the input or that the game has a reachable defect.

Threshold-adjacent behavior, exception modes, live caller constraints and complete lifecycle remain unresolved. No function name or completion credit is added.


### Object auxiliary target-transform helper

Saved ComputeObjectAuxiliaryTargetTransform with a seven-input working signature after tracing original control flow, callers, metadata and transform equations. It builds an auxiliary target from stored or group/state sources, optional mode offsets, linked targets and recursive selection, then applies the object-local transform.

2032 scoped scenarios support the descriptive role, excluding superseded sets. Backup, independent reopening and fresh decompilation verify persistence. The output uses the existing working 32-byte transform type; context/state/object pointers remain opaque. Original Controlinator registration binds one selector caller, without establishing exclusive use.

Combined modes, exact field names, threshold-adjacent behavior, arbitrary recursion, invalid or aliased inputs, full lifecycles and exact PS4 math remain unresolved. Isolated zero-displacement NaN evidence does not establish a reachable game defect. This name does not mark full semantic or subsystem completion.

Totals: 601 checked names; 2,017 mapped and 7,572 unmapped among 9,589 discovered functions.


### Sculpt group rebasing

288 original-code scenarios verify a transform-selector path bound to the original Sculpt type registration. It converts a supplied pose between group frames using new group × inverse(old group) × supplied pose. Initial tests cover the active-reference condition, presence of both groups, a required object-field sentinel and type gating; disabling each condition selects the ordinary fallback in the tested context.

192 further cases use nonzero old/new group indices, four packed-reference high-bit patterns and all combinations of old/new scale signs. Distinct group frames, independent transform equations, source buffers and output guards passed.

The tests use valid object index zero, finite nonzero scales and unit rotations. Original meaning of the object-field sentinel, zero/nonfinite scales, mismatched packed-reference bits, caller lifecycle and malformed inputs remain unresolved. This behavior evidence adds no checked-name credit.


### Head and hand auxiliary lookup

Original type registrations bind the selector's remaining linked kinds to HeadGadget and HandGadget. 328 original-code head-lookup scenarios test every 8-bit mask plus twelve gate variations. The least-significant set bit selects the requested auxiliary slot, with empty masks and the reserved tested bit rejected. Duplicate matches choose the first record. Success writes the record pointer; failure preserves the caller's output pointer.

The hand lookup calls a separate state selector. 1536 original-code cases cover six selector codes, all pointer-presence combinations, four sampled state modes and both boolean inputs. Exact pointer identity and source preservation passed. The selectors differ in how they choose between two available non-mode-2 states; a sole first state is eligible only in mode 2 for the tested default/sole-state selectors. Original physical state/selector names remain unresolved.

These are bounded lookup semantics, without new checked-name credit. Connected hand output behavior, downstream transform construction, large-list behavior, arbitrary byte values, invalid pointers and live-game lifecycle remain under review.


### Verified head and hand lookup names

Saved TryResolveHeadAuxiliaryRecord, SelectAuxiliaryHandState and TryResolveHandAuxiliaryState with explicit working parameter and return storage. The first lookup returns a boolean and record output; the state selector returns a pointer; the hand lookup returns a boolean with separate record/state outputs. Context and state structures remain opaque.

Evidence includes 328 head-lookup scenarios, 1536 state-selection scenarios and 1653 connected hand-lookup/gate scenarios. The connected tests exercise the original resolver again; these counts describe test scopes, not separate implementation units. Original type registrations bind the caller kinds to HeadGadget and HandGadget. A verified compressed backup, independent reopening and fresh decompilation confirm all three names and signatures; only their intended inventory entries changed.

Large lists, arbitrary byte values, NaN activation, invalid or aliased pointers, original field names and full lifecycles remain unresolved. These names do not complete the head/hand transform subsystem. Totals: 604 checked names; 2,020 mapped and 7,569 unmapped among 9,589 discovered functions.


### Head transform construction and connected selection

112 positive-local-scale and 112 negative-local-scale scenarios verify the head constructor's selected group pose and optional auxiliary composition. In sampled finite unit rotations, its reconstructed local basis and inverse cancel. Negative local scale adds a local X half-turn to the selected output orientation. Final scale preserves the sign of local scale times factor and clamps magnitude to the original float 0.01, including signed-zero factors.

64 connected scenarios execute the original selector, head lookup, constructor and composition together. The result is head target × inverse(stored head transform) × supplied transform, with the target drawn from the alternate context's group and auxiliary state. Two groups, both local-scale signs, auxiliary enable states and signed scale factors pass independent equations and guarded source/output checks.

The final standalone sets exclude their superseded preliminary set. Degenerate bases, other modes, original field meanings, invalid references and live-game lifecycle remain unresolved. This behavior evidence adds no checked-name credit.


### Verified head target-transform name

Saved ComputeHeadGadgetTargetTransform with a four-input working signature after reading and byte verifying its 482 original instructions. It builds the head target from the selected group and optional auxiliary transform, reconstructs the local basis and combines the inverse local transform. The tested negative-local-scale path adds a local X half-turn; final scale preserves product sign and clamps magnitude to the original float 0.01.

288 scoped original-code scenarios support the role, including 64 connected selector/lookup/constructor cases. A verified compressed backup, independent reopening and fresh decompilation confirm persistence. Context/gadget/record pointers remain opaque; the output reuses the working 32-byte transform type.

Degenerate or nonunit inputs, other modes, original field names, aliasing and full lifecycle remain unresolved. This name does not claim full semantic or subsystem completion. Totals: 605 checked names; 2,021 mapped and 7,568 unmapped among 9,589 discovered functions.


### Hand constructor flag and scale wrapper

64 flag-clear and 64 flag-set original-code cases verify the stored-state path of the larger hand constructor. With the flag clear, stored state composes with gadget-local transform. With it set, position stays fixed, stored scale is negated and a local X half-turn is applied before local composition. All stored/local scale-sign combinations were tested.

128 connected wrapper/constructor cases establish scale behavior: a negative control value toggles the extra flag when optional state switching is disabled; negative zero does not. The wrapper keeps the constructor's output scale sign and replaces its magnitude with the control value's absolute magnitude. Original bit masks resolve that distinction. Independent equations, source buffers and output guards passed.

These counts describe separate test scopes, not separate recovered implementation units. Most of the larger constructor's branches remain under review, including unstored state, metadata scaling, auxiliary and linked targets. Other wrapper flag sources, original field meanings, malformed inputs and live-game lifecycle remain unresolved. No checked-name credit is added.


### Verified hand target-transform wrapper

Saved ComputeHandGadgetTargetTransform with a seven-input working signature after reading and byte verifying all 51 original wrapper instructions. It selects the auxiliary group, derives a constructor flag from optional hand-state switching and control sign, calls the larger constructor, then combines constructor scale sign with control-field magnitude.

512 connected original-code scenarios verify sampled selector/state/record gates, pointer availability, sign combinations and signed-zero control behavior. State-derived switching requires the enabled gate, selector 0 or 1, clear record flag, both pointers and both state modes non-2. Negative control toggles that flag. Verified backup, independent reopening and fresh decompilation confirm persistence.

This names the small wrapper; most branches of its larger callee remain unreviewed and that callee stays unnamed. Context and state types remain opaque. Arbitrary bytes, NaNs, invalid or aliased inputs, original field meanings and lifecycle remain unresolved. Totals: 606 checked names; 2,022 mapped and 7,567 unmapped among 9,589 discovered functions.


### Hand position factors and group offsets

252 additional scoped hand-constructor scenarios cover unstored position blending, metadata factors, nondefault group geometry and their combination. The default group path blends group XYZ toward state XYZ without clamping the sampled factor, while retaining state scale and rotation. A present, nonzero metadata field replaces that factor with object value divided by group factor, the original float 0.4 and group scale. Zero field value falls back to the state factor.

The nondefault group path offsets state position along a mode-rotated local Z direction, using the factor, group scale and state-scale sign. State scale and rotation remain selected for final local composition. Combined tests use a deliberately different state factor to verify metadata selection across the sampled modes, flags and scale signs. Independent equations, source buffers and output guards passed.

These are bounded paths of the still-unnamed larger hand constructor. Auxiliary, linked-target and direction paths, nonfinite inputs, original field meanings and full lifecycle remain unresolved. Host sine/cosine uses the corrected adapter; exact PS4 trigonometry is not claimed. No checked-name credit is added.


### Hand targets, flag-selected offsets and recursion

200 scoped original-code scenarios verify direct target blending, linked-reference targets and connected recursion. The direct path requires its metadata boolean and matching state pointer, clamps the factor and applies smoothstep to position/scale and a normalized hemisphere quaternion blend. Disabled gates preserve the ordinary reference path.

For the two tested linked-reference kinds, target composition uses a different auxiliary offset for each extra-flag state. Distinct offset slots prove that selection. The flag-set source is flipped before blending. Missing transform metadata substitutes identity. Connected tests execute the original selector/body evaluator and distinguish runtime body selection from stored-reference bypass.

Tests cover both flags, valid reference one, unit rotations, sampled finite scales and one recursion level. Nonempty lookup, cycles, invalid references, other constructor paths and original field meanings remain unresolved. These behavior scenarios add no checked-name credit.


### Hand auxiliary sources and direction adjustment

192 original-code scenarios verify the path selected by either nonidentity auxiliary vector. Stored override selects stored position, scale and rotation; otherwise position comes from the group and scale/rotation from state. A mode-dependent local X rotation modifies the selected orientation. The extra flag adds its half-turn and scale negation afterward. Gate patterns, modes, flags, overrides and scale signs were crossed independently.

160 direction scenarios verify its geometry and four bypasses across both group-scale signs and extra flags. The first auxiliary state's mode enables the direction path, but that pointer need not equal the constructor's selected state pointer. Distinct pointers confirm the difference. The path sets position along normalized group-to-stored displacement at the signed group-factor distance and adjusts stored orientation with a shortest-arc quaternion before the extra-flag operation.

Independent equations, source buffers and output guards passed. Tests use default group mode, unit rotations and finite inputs. Nonempty linked-reference lookup, zero-displacement and antipodal cases, original field names and full lifecycle remain unresolved. No checked-name credit is added.


### Verified hand auxiliary target constructor

Saved ComputeHandAuxiliaryTargetTransform with an eight-input working signature, including the stack object pointer and one-byte extra flag. The 1160-instruction body selects stored/group/state transforms, metadata factors, mode offsets, direction geometry, auxiliary gates and optional linked targets, then applies gadget-local composition. The extra flag flips its source frame and selects the linked-reference offset slot.

1028 direct original-code scenarios exclude superseded sets. Another 512 connected wrapper scenarios separately support the call boundary. The latest lookup cases verify ID/group matching and first-match order under both flags. Direction edge cases establish the fixed X-axis fallback and isolated zero-displacement NaN behavior; the latter is not proof of a reachable game defect. Backup, independent reopening and fresh decompilation confirm the name and signature.

This is a descriptive role, not full semantic or feature completion. Context/state types remain opaque. Arbitrary recursion, threshold-adjacent cases, nonfinite or invalid/aliased inputs, original field meanings, exact PS4 math and full lifecycles remain unresolved. Totals: 607 checked names; 2,023 mapped and 7,566 unmapped among 9,589 discovered functions.


### Connected HandGadget selector path

64 original-code scenarios connect the transform selector, hand auxiliary lookup, state resolver, hand wrapper and larger constructor through final composition. The world-side lookup identifies state index 0 or 1; the constructor reads the corresponding alternate-context state. Distinct world and alternate payloads verify the handoff rather than merely observing identical cached values.

The selector result matches hand target × inverse(stored hand transform) × supplied transform. Both selected indices, signed-zero and signed control values, and both local-scale signs pass independent equations. Source buffers and output guards remain unchanged.

Tests use valid auxiliary record/group zero, a body-linked hand at index one and stored-state override. Optional switching, target blending, arbitrary state indices, invalid references and caller lifecycle remain outside this connected scope. No checked-name credit is added.


### Verified auxiliary-context transform selector

Saved ResolveObjectTransformForAuxiliaryContext with a six-input working signature: five register inputs and a 32-byte supplied transform passed by value on the stack. Its 1024-instruction body resolves supplied, runtime-body, cached, parent-relative and repeated transforms; it can rebase Sculpt group frames or apply Controlinator, HeadGadget and HandGadget targets.

1344 scoped entry-to-return scenarios support the descriptive role, excluding superseded sets. They cover source and eligibility gates, cached and recursive parent paths, repeats, packed references, signed group rebasing and connected gadget targets. Verified backup, independent reopening and fresh decompilation confirm the name and signature.

The context remains opaque and the transform is an analyst working type. Original field names, unexplored state combinations, arbitrary recursion/cycles, nonfinite or invalid/aliased inputs and full lifecycles remain unresolved. This is not full semantic or feature completion. Totals: 608 checked names; 2,024 mapped and 7,565 unmapped among 9,589 discovered functions.


### Verified PlayerIdx type and lifecycle callbacks

Recovered `PlayerIdx` as a one-byte structure with original `u8 idx` at offset zero. Its original type registration installs two previously undefined callbacks, now saved as `AllocateDefaultPlayerIdx` and `FreePlayerIdxIfNonNull` with typed signatures. Independent reopening and fresh decompilation verify both definitions; all previously defined function names and signatures are unchanged.

513 isolated cases check the original callbacks using controlled allocation/free substitutes: creation requests one byte, initializes 255, returns the full pointer and preserves adjacent guards; release forwards a nonnull pointer once and skips null. Real library behavior, allocation failure and full player lifecycle remain unverified.

The original Controlinator enums are also saved as types. A connected 192-case mode set confirms the tested transform branch uses the parent reference for `Gun` and substitutes runtime-body position for `MaintainGrabOrientation` and `FaceDockToCamera`, retaining parent scale and rotation. This set supersedes the overlapping earlier 128 cases. Its metadata offsets, valid associations, positive scales and finite rotations are controlled fixture inputs, not a complete in-game mode test.

Totals: 610 checked names, 2,026 mapped and 7,565 unmapped among 9,591 discovered functions. Type recovery and annotation alone receive no additional name-review credit. These counts do not measure whole-game semantic completion.


### Verified shared auxiliary transform helpers

Saved and independently reopened `ComputeAuxiliaryStateTransform` (142 instructions, 288 scoped cases) and `RotateTransformForAuxiliaryMode` (107 instructions, 432 scoped cases), including explicit working register signatures and fresh decompilations. The former selects a stored pose, blends group/state position, or offsets state position along a mode-adjusted direction while retaining state scale and rotation. The latter preserves finite position and signed scale while applying and normalizing a mode-dependent local-X quaternion rotation. Both mode-helper callers use in-place output; exact alias cases pass. The 432-case set supersedes its overlapping 216-case set.

Original Controlinator property registration also identifies `tip_from_controlinator_for_follow` at `0x240` and `world_from_grip_for_transition` at `0x260`; the relevant reads are annotated in the saved project. A still-unnamed writer has 152 passing reset/skip scenarios: tested eligibility failures clear only the follow transform, while earlier world, activation, object-flag or frame gates preserve the object. Its successful update and transition behavior remain under investigation, so it receives no naming credit.

The shared state helper has22 direct call sites; only the writer's argument preparation was traced here. Exceptional normalization inputs, other overlaps, exact PS4 trigonometry and complete caller lifecycles remain unresolved. Host-adapted trigonometry is used in the isolated tests, not claimed equivalent to every PS4 result. Original code and private data remain local.

Totals: 612 checked names; 2,028 mapped and 7,563 unmapped among 9,591 discovered functions. These are scoped code-review results, not full-game completion.


### Verified Controlinator follow updater and runtime transform application

Saved and independently reopened `UpdateControlinatorFollowTransforms` (992 instructions, 802 scoped writer cases) and `ApplyObjectWorldTransformToRuntimeContext` (288 instructions, 524 scoped cases), including explicit register signatures and fresh decompilations. Only the verified updater is mapped into Controlinator runtime code; the application helper remains shared object code.

The updater resets ineligible follow offsets, initializes or transfers them from a prior referenced object, builds transition transforms for eligible categories, applies ordinary follow and direction-aligned Gun transforms, and expires eligible auxiliary timestamps. Tests establish the orientation-capture difference between `MaintainGrabOrientation` and `FaceDockToCamera`, the referenced-transform composition used for transitions, and the float32 comparison at the timer threshold. Timer clock units remain unresolved. Writer scenario totals exclude diagnostic probes, instrumented observations and helper-only tests.

The application helper converts a requested world transform to its parent-relative form, updates the metadata-selected object field and context pose cache, and conditionally forwards the supplied reference's low 16 bits to body status. Separate transform, early-rejection and scalar/SIMD/remainder status tests support that role. Metadata offsets in these fixtures are controlled inputs, not complete recovered object layouts.

An initial Gun comparison exceeded a fixed local-position tolerance. Input-capture instrumentation showed world-position error below 0.00005, amplified by conversion through parent scale -0.5. The final uninstrumented test propagates that world-space tolerance through inverse-parent rotation/scale while retaining 0.00005 quaternion/scale checks. The initial failure, diagnosis and explicit tolerance remain in local evidence; this is not exact numerical equivalence with every PS4 math result.

Untested hierarchy/cache paths, failed prior-reference lookup variants, auxiliary nonidentity gates, invalid/cyclic or nonfinite inputs and complete caller lifecycles remain open. Totals: 614 checked names; 2,030 mapped and 7,561 unmapped among 9,591 discovered functions. This is scoped reverse-engineering progress, not full Controlinator or game completion.


### Verified Key spatial collection and nearest lookup

Saved and independently reopened `CollectAndSortKeySpatialProjections` (163 instructions, 96 scoped cases) and `FindNearestKeyByName` (204 instructions, 768 scoped cases), with explicit working register signatures and fresh decompilations. These are shared spatial lookup routines for original kind3 `Key` objects. The original enum, dispatcher and serialization wrapper establish the internal type; its player-facing Dreams feature remains unidentified.

The collector clears Key working fields, filters activation/object flags, builds 16-byte pointer/projection records, and orders them by ascending projection. An initial four-lane dot-product assumption failed; assembly establishes dot3 over transformed XYZ, excluding W. The corrected independent equations pass with varied nonzero W inputs. A direct static initializer normalizes constant (13, 23, 7) for the projection vector; indirect writes and other startup paths are not ruled out.

The query matches the original `Name` field at offset 0xf8 and returns the nearest eligible object. With positive maximum distance and spatial context it searches the projection records and applies minimum/maximum distance bounds. Missing context or nonpositive maximum selects a full-list fallback that ignores those bounds in the tested paths. Ancestry filter 0 accepts all; 2 excludes descendants; tested other nonzero modes include descendants. Packed-reference high-bit handling and valid acyclic parent chains were checked across both query paths.

Name remains an opaque 64-bit token; its encoding is not recovered. Tests cover collection sizes 0–40 and finite inputs, not capacity exhaustion, duplicate/nonfinite ordering, cycles, malformed references or a complete gameplay lifecycle. Original code remains local. Totals: 616 checked names; 2,032 mapped and 7,559 unmapped among 9,591 discovered functions. These findings do not claim a completed Dreams feature.


### Verified radius getters and targeting-property bindings

Saved and independently reopened `GetObjectInnerRadiusOrDefault` and `GetObjectOuterRadiusOrDefault`, each a complete 28-instruction leaf with object input in RDI and float return in the low XMM0 lane. Fresh decompilations passed; 2,560 calls per getter cover all 128 low-bit kinds, high object flags, zero/negative/max-positive metadata offsets and distinct finite field values without object mutation.

A positive signed16 metadata offset selects the configured float. Otherwise defaults are inner 10 / outer 300 generally, Follower and LookAtRotator 0 / 1000, EffectField 4 / 10, and SpawnplaceGadget 24 / 32. An incorrect initial EffectField outer-default assumption was caught by execution and corrected against its original constant; the complete test set then passed.

Original initializer writes bind the adjacent radius metadata slots to Follower object offsets 0x108/0x10c and LookAtRotator 0x104/0x108, agreeing with the serialized `InnerRadius`/`OuterRadius` properties. The same initializer binds their `DetectName` fields. The traced LookAtRotator branch reads that metadata-selected token and passes it into `FindNearestKeyByName`, connecting the spatial lookup to gadget targeting. This establishes the traced fields and call path, not a complete Follower or LookAtRotator implementation.

Other kinds' real offset initialization, null/invalid pointers, nonfinite field values and complete targeting lifecycles remain unresolved. Totals: 618 checked names; 2,034 mapped and 7,557 unmapped among 9,591 discovered functions. Raw code and private data remain local.


### Object region-shape selector and TriggerZone output trace

`GetObjectRegionShapeMode` is saved with an explicit object-pointer input and byte return, independently reopened and freshly decompiled. Its original 119-byte body passed 65,537 controlled calls covering all 128 low-bit kinds, high flags, null input, signed metadata offsets, selected field values and second-field override precedence. Object inputs stayed unchanged. Original property names and whole-game integration remain unresolved.

The traced TriggerZone call passes this selector into the previously reviewed region-shape weight evaluator, whose result feeds Key output channels. The recovered 20-byte `PlayerValue` layout contains `non_player` and four `values` floats. Original `ConsiderPlayers` selects all-channel versus ownership-mask-controlled writes. The bounded all-channel block replaces ties; selected-channel instructions preserve ties. These findings do not constitute a complete TriggerZone review or add another checked function. User-facing player numbering and complete strength/lifecycle behavior remain unresolved.

Totals: 619 checked names; 2,035 mapped and 7,556 unmapped among 9,591 discovered functions. These are discovered-function review counts, not whole-game completion. Raw code and private data remain local.


### Bounded TriggerZone Key-detection and output checkpoint

Original registration identifies `DetectType` value 1 as `Key`, along with `ZoneType`, `DetectCnt`, `ConsiderPlayers` and `OutputPlayerValue`. The non-EntireLevel Key path uses the TriggerZone shape to evaluate candidate transforms under the recorded valid/stable world-lookup assumption. EntireLevel instead scans collected Keys, retains name/ancestry filtering and writes unit strength without the bounded shape evaluator. Original FogGadget `FogShapeType` is a separate override supported by the shared selector, not another TriggerZone field.

Isolated original-code blocks passed 768 EntireLevel channel-write cases, 20,736 weighted selected-channel cases, 588 final output-gate cases and 10,240 propagation-loop cases. These are separate block fixtures, not full TriggerZone execution. Exact output bits and surrounding buffers were checked. Ownership bits 0–3 select the four `values` channels; zero selects `non_player`. An initial reversed source-bit expectation failed execution and was corrected. Weighted selected-channel writes preserve ties and quiet-NaN unordered comparisons; the separately reviewed all-channel path selects the new value on ties. EntireLevel writes literal 1.0.

The final gate requires a positive accepted count and the original `DetectCnt` threshold. Its saved value is a snapshot of that same property; zero additionally enables a count-equality condition. Success copies the accumulated 20-byte PlayerValue, failure clears it. Optional propagation writes the accumulated output through candidate metadata; original initialization binds Key and TriggerZone to `OutputPlayerValue`. Record-count production, propagation enable policy, other detection modes, malformed graph behavior and complete lifecycle remain unresolved. Saved annotations were independently reopened. No new function completion credit: totals remain 619 checked names and 2,035 mapped functions.


### Connected TriggerZone Key-path validation

Full original processor entry-to-return fixtures passed 66 EntireLevel Key cases, 162 controlled ownership cases, 162 cases inheriting ownership from Sculpt parents through the original `PlayerOwnership` field, 66 bounded sphere cases, and 48 multi-Key sphere cases. Handle lookup, allocation and free are explicit fixture boundaries; reviewed original helpers and original `isinff` execute. These groups test different scopes and do not establish all processor behavior.

The sphere reference independently calculates linear falloff for unit transforms with inner radius 2 and outer radius 4 at translated centres. Multi-Key cases include name mismatches, out-of-range candidates, nonzero signed prior outputs and threshold failure. They confirm provisional Key outputs are restored on failure. The separate rollback loop also passed 10,240 cases with distinct saved values per object. Snapshot capacity derives from world object-table count times 32; allocator failure behavior remains unverified.

The traced Key success routes disable the separate success-propagation loop. Binding a candidate output field to that loop does not mean the Key path enables it. Zero `DetectCnt` uses an all-matching condition in the tested bounded cases: a matching Key outside the region can fail detection and trigger rollback. Source ownership selects Key channels; candidate ownership selects accumulated TriggerZone channels.

Saved annotations were independently reopened. The full 5,247-instruction function remains unnamed and only partially reviewed. Other detection modes, broader geometry and filter combinations, malformed graphs and live gameplay remain unresolved. No additional checked-name credit; total stays 619.


### Scope, box geometry and Imp detection checkpoint

The original `EDetectScope` registers All, Me and Others. Fifteen EntireLevel and fifteen bounded-sphere connected cases cover valid direct/deeper ancestry, other trees, rootless candidates and zero/positive thresholds. These are expanded scope sets; the earlier twelve positive-threshold cases overlap and are not added again. In these fixtures, zero `DetectCnt` succeeds with filtered matches for EntireLevel, while the bounded-sphere path fails when globally name-matching Keys are excluded by scope. This branch difference is not presented as a game bug.

Another 162 full-entry box cases cover diagonal points, translations and Z rotations against an independent box-shell reference, with maximum output error below 0.00000012. Unit scales and uniform extents remain explicit limits.

Imp detection now has 88 stored-position cases, 400 eligibility cases and 360 group-to-state interpolation cases. Tests cover four player channels, relevant pointer/category/flag gates, NaN rejection in the observed group-value condition, and successful/failing count thresholds. Original category/flag property names and broader offset modes remain unresolved.

The segment math import resolves to `logf`. Forty-two full-entry special-position cases execute its original local libc implementation and compare outputs to an independent logarithmic segment reference plus the subsequent category-dependent sample offset. An initial one-dimensional reference missed that offset and failed. A private diagnostic capture isolated it; the final cases were rerun without diagnostic instrumentation, with maximum output error below 0.00000009. The failed expectation and resolution remain in local evidence.

Original processor/helpers execute with explicit handle lookup and allocation/free fixture boundaries. Whole fixture buffers and cleanup are checked within each stated scope. These tests do not establish other detection modes, general rotations/scales, malformed graphs, math error paths or live gameplay. Ghidra notes were independently reopened; the full processor remains partially reviewed and unnamed. Checked-name total remains 619.


### EntireLevel Dream-mode checkpoint

Original `DetectObjectId` registration and the Dream dispatch lead to a 40-byte record scan. The observed first 64-bit ID comparison selects a record ordinal, which filters Sculpt word `0x2c`; complete identifier and field representation remain unresolved. Thirty-two full-entry cases cover missing/matching records, empty/populated lists, shared parent roots and thresholds.

Original fields `LabelUnlabelled`, `QueryLabelBitmask` and `LabelAnyOrAll` control filtering. In 324 connected Dream cases, Any accepts a label intersection or permitted unlabelled object; All checks query-bit inclusion and accepts all tested labels for an empty query. This is a mode-specific result.

Another 486 connected ownership cases show that reaching a positive count threshold stops further root/channel accumulation. Forty-eight child-first cases verify that root dedup keeps the first accepted representative's ownership: a child can supply channels while its later parent is skipped despite different ownership. Zero count short-circuits at the first accepted root in the tested EntireLevel Dream path.

Tests execute original processor/helpers and original local libc `isinff`/`memset`, with explicit handle lookup and allocation/free fixture boundaries. Object, world and context preservation and cleanup were checked. Saved Ghidra notes were independently reopened. Cached/bounded Dream detection, complete identifier semantics, broader root/filter combinations and live gameplay remain unresolved. The processor is still partially reviewed and unnamed; 619 checked names unchanged.


### EntireLevel Labels-mode checkpoint

Original Labels detection visits PuppetHeart and Group objects through separate world lists. Their original registrations identify `Name`, `LabelBitmask`, `OutputPlayerValue` and `PlayerOwnership` at type-specific offsets. Metadata initialization agrees with the output and ownership bindings. The mode name does not imply a separate label-gadget object type.

Twelve full-entry first-list cases verify wildcard/exact/missing names, inactive power, output writes and threshold rollback. Sixty-four mixed-list cases verify the shared accepted count and restoration of distinct prior outputs in both types. In the tested short lists, the second pass still runs when the first pass alone meets the count threshold; longer-list ordering is not established.

Another 135 connected ownership cases use the original candidate fields and TriggerZone ownership inherited from Sculpt parents. Source ownership selects provisional candidate output channels, while candidate ownership contributes to the gadget's accumulated output. Threshold failure restores both objects' complete prior values. Whole object/world/context and cleanup checks passed within these fixture scopes.

Original processor/helpers and `isinff` execute, with explicit handle lookup and allocation/free fixture boundaries. Ghidra annotations were independently reopened. Cached/bounded Labels detection and broader label/player/filter combinations remain unresolved. The processor remains partially reviewed and unnamed; 619 checked names unchanged.


### Verified shared six-transform composition

Saved and independently reopened `ComposeSixTransforms`, a complete 464-instruction helper used by the Camera detection branch and numerous other callers. Its working signature records a 32-byte output through RDI, eight 16-byte SIMD inputs, and four 16-byte incoming stack containers. These represent six ordered position/scale and quaternion pairs; the name and signature are analyst descriptions, not recovered source symbols.

Two hundred fifty-six complete original helper executions, using original local `isinff`, match an independent ordered transform reference with finite unit quaternions, translations and signed scales. Maximum absolute error was below 0.000025; input buffers and output guards were preserved. Five normalization stages were reviewed in the original body. Nonunit, zero and nonfinite quaternion behavior, aliasing, extreme scales and complete caller lifecycles remain unresolved. Camera detection itself is still under review.

Totals: 620 checked names; 2,036 mapped and 7,555 unmapped among 9,591 discovered functions. These are discovered-function review counts, not whole-game completion. Raw code remains local.


### Camera detection checkpoint

Camera detection now has 198 zero-offset and 576 nonzero-offset full-entry cases. The latter cover four off-axis positions, three small finite Euler rotations, three positive scales, four signed depths and passing/failing thresholds, with player consideration disabled and enabled. Original code constructs a rotated forward offset before calling the shared region evaluator. The independent quaternion and spherical-falloff reference agrees within 0.00000018.

With scope set to All, successful detection writes the weight to all five output components in these fixtures, including when player consideration is enabled. Failing the count threshold clears outputs while preserving the accepted count. Whole object, world and context buffers and cleanup were checked. The original processor, composition and region helpers, and local libc `sincosf`/`isinff` execute; handle lookup, allocation/free and the platform stack-canary pointer are explicit fixture boundaries.

Saved Ghidra annotations were independently reopened. Camera offset field names, scope filtering, invalid/group indices, other shapes, large/nonfinite angles and live gameplay remain unresolved. The enclosing processor is still partially reviewed and unnamed. Checked names remain 620; these cases do not increase whole-game coverage by themselves.


### Camera scope and blend-contribution checkpoint

Forty-five full-entry cases establish fallback camera ancestry behavior for All, Me and Others. Another 90 cases exercise the Controlinator candidate branch using original PlayerIdx values 0 and invalid 255; another 90 connect the original Camera candidate blend-contribution helper to scope filtering. Positive candidate contribution enables ancestry filtering; it does not multiply the region weight in these fixtures. Direct and transitive matching ancestry, other trees, rootless references and thresholds 0/1/2 were covered.

The complete 126-instruction contribution helper was read. In 3,584 original-code cases, the first eligible matching token contributes an eased weight, attenuated by one minus each later entry's eased weight. Counts 0..3, modes 0..6, four eligibility flag patterns and all eight combinations of three context flags were covered; input bytes stayed unchanged. This does not establish every weight, token type or list ordering.

Two incorrect reference assumptions were retained and corrected: zero threshold caps the stored accepted counter to zero, and observed curve mode 5 computes `3*x*x - 2*x`, rather than cubic smoothstep. Corrected references pass; original code was not changed. Ghidra scope annotations were saved and independently reopened. Multiple candidates/order, other groups, malformed ancestry and live gameplay remain unresolved. Processor and contribution helper remain unnamed; checked-name total stays 620.


### Named layered blend-token contribution helper

The contribution helper is now saved as `ComputeLayeredBlendTokenWeight`, with explicit pointer/token inputs and a float return. Its complete 126-instruction body and all three call sites were read at the relevant calls: token types 0 and 1 are observed, so the descriptive name does not imply a Camera-only token. Independent reopening and fresh decompilation verify persistence. The 3,584 helper checks and 90 connected Camera scope cases above support this role; exceptional weights, duplicates, larger counts and complete blend lifecycles remain unresolved.

Totals: 621 checked names, 2,037 mapped and 7,554 unmapped among 9,591 discovered functions. These counts do not establish whole-game completion.


### Original camera field names recovered

Original registrations identify `CameraBlender::CameraStatus.focus`, `eye`, `euler`, `scale` and `focus_scale`. Nested `cb_data`, `camera_space_list` and `camera_blend_result` offsets agree with the processor reads: this detection path uses **focus**, not the separate **eye** field. The previously tested forward offset is `0.4 * focus_scale * scale`, rotated by the observed Euler composition and added to focus. The earlier fixtures remain valid; their anonymous offset-field descriptions are now resolved.

`ActiveCameraData` registrations identify `id`, `transition_type`, `packed`, `status` and `blend_amount`; `CameraId` identifies `type` and `number`. These agree with the named contribution helper's matching, curve and weight reads. Original `vr_comfort_mode` and `vr_comfort_mode_force_off` fields explain two of its context gates; the third flag still lacks an original name. The fallback ancestry field is registered as `scope_thingref`.

Registration instruction bytes were checked against the original executable, and saved Ghidra annotations were independently reopened. These labels strengthen field semantics without establishing original C++ declarations, every field type, active-space switching or whole-camera behavior. Checked-name count remains 621.


### Camera transition enum and working types

Original `ECameraTransition` values are `Smooth=0`, `Cut=1`, `EasyIn=2`, `EasyOut=3`, `Linear=4`, `Crazy=5`, and `LAST=6`. The unusual quadratic observed earlier belongs to `Crazy`; it was not a mislabeled standard smoothstep. `Cut` passes the incoming blend amount in this helper, which does not establish caller-side cut timing.

The enum and partial blend-entry/context layouts are saved in Ghidra and independently reopened. The named helper now takes a typed working context pointer. A fresh decompilation displays blend amounts, the count and VR flags by name; some token and transition reads still use pointer casts. The eight-entry slot footprint is inferred from the next count field, not proven runtime capacity enforcement. Unknown bytes and flag meanings remain explicit. No original code changed and no extra name credit was added; total stays 621.


### EntireLevel Objects detection and graph labels

Objects detection gathers candidates from supplied query records before graph-label filtering. Forty-eight complete original entry cases cover zero/one/two records, two record-kind values, original Sculpt Power off/on and thresholds 0/1/2/3. Only tested record kind 0x115 contributes; its producer-side semantic name remains unresolved.

Another 720 complete entry cases connect the original label helper and graph iterator using a query root and child Sculpt. A child-only match can qualify the root. Any accepts a label intersection or permitted unlabelled visited Sculpt. All requires every requested bit on one visited Sculpt; labels are not combined across different nodes. Empty All queries accept a visited Sculpt. Threshold output and stored-counter behavior, complete fixture buffers and cleanup were checked.

The complete 104-instruction helper is saved as `ObjectGraphHasMatchingLabels`, with explicit root-reference/packed-query inputs and a boolean return. Independent reopening and fresh decompilation verify persistence. The physics/query producer and valid graph are supplied fixture boundaries; host stack pages are prepared for original large stack frames. An initial nested fixture omitted its candidate-reference field; correcting that setup allowed the full cases to run. No original code was changed. Other graph categories, malformed/cyclic graphs, cached/bounded Objects detection and running-game behavior remain unresolved. The enclosing processor is still partially reviewed and unnamed.

Totals: 622 checked names, 2,038 mapped and 7,553 unmapped among 9,591 discovered functions.


### Cached Objects results and root-output routing

Original Sculpt registrations distinguish `LabelBitmaskComposed` from `LabelBitmask`. The graph helper reads the composed field. Registrations and metadata initialization also identify `Name`, `OutputPlayerValue` and `PlayerOwnership`, allowing output tests to use actual field bindings.

Seventy-two full-entry cached-result cases show that a matching result child updates the **gathered query root's** output, leaving the child's prior output unchanged. With player consideration disabled, incoming magnitude ties replace old values. Count-threshold failure restores the complete prior root output from its snapshot. The initial reference incorrectly targeted the child and retained ties; both assumptions were corrected against original assembly before the final runs.

Another 54 cases use two distinct result children sharing one query root. The root counts once and its output uses the first encountered result weight; the gadget output still accumulates the strongest weight before root deduplication. Their outputs can therefore differ. A threshold of two fails because only one unique root was accepted, and restores the root's prior value.

Original consumer/helper bodies execute and whole fixture buffers plus allocation cleanup were checked. Physics/contact records and cached spatial results are supplied boundaries; upstream query production and geometry were not executed. Signed/nonfinite weights, multiple distinct roots, player channels and live gameplay remain unresolved. Ghidra annotations were saved and independently reopened. No new name credit: 622 checked names unchanged.


### Sculpt Power fixture correction

Further tracing found that Sculpt's original `Power` field is at `0x4c`; `0x40` is used as a resource handle in the spatial producer. The original property registration and packed metadata initializer independently confirm `Power=0x4c`. Earlier Dream/Objects fixtures supplied `0x40` as a synthetic Power location, so their claim to use the original Power field was incorrect.

All eight affected suites were corrected and rerun: 1,784 cases covering Dream labels/ownership/root ordering and Objects filtering/nested labels/cached output routing. All pass with the corrected original field and the same scoped outcomes. Original fixture scripts and receipts are retained as superseded; these reruns add no test or naming credit. Ghidra correction annotations were saved and independently reopened. Other documented fixture boundaries remain; upstream query production and live gameplay are still incomplete. Checked names remain 622.


### Region-query GPU result transfer

The Sculpt query producer invokes five named compute stages: `RegionQueryBootstrap`, `RegionQuerySampleField`, `RegionQueryRefineSetup`, `RegionQueryRefine`, and `RegionQueryCopyOutput`. Reconstructed paths from executable literals match all five entries in the retained local shader archive using the executable's original native resource hash and section extractor. Extracted code ranges are 724, 3,372, 292, 5,924 and 180 bytes respectively. A 64-bit hash-index match alone cannot exclude collisions. Raw shader data remains local.

The CPU transfer trace connects CopyOutput dispatch to a float result stream. Staged query-index/leaf-ordinal pairs map a positive result back to its query and object. Nonpositive and unordered float values are skipped; available slots append a weight/object pair up to the observed 0x3fff cap. Per-query count/start spans match the cached-result layout already tested in TriggerZone.

CopyOutput's bounded static decode reaches its first physical end instruction after 19 instructions: an index/count guard, two buffer reads, floating comparison/conditional selection, and one buffer write. Its conditional exit targets that end instruction. Full buffer meanings, other-stage algorithms, synchronization, positive Sculpt GPU execution and live gameplay are not verified. Static decode counts are not behavior-completion counts. Ghidra trace annotations were saved and independently reopened; checked names remain 622.


### CopyOutput bindings and static expression

The final stage receives a 52-byte record containing three buffer descriptors and a staged-pair count. CPU record writes agree with the shader's descriptor/count loads. Output allocation and descriptor construction link its destination to the float stream consumed by the CPU.

For an active index below the count, the static instruction trace yields `output[i] = inputA[i] < 1.0 ? 1.0 : inputB[i]`. This follows the actual operand order and conditional-selection bits, rather than the stage name. The earlier meanings of the two inputs are still unresolved; neither is labeled as a distance or confidence value without that provenance.

Ghidra binding annotations were saved and independently reopened. This is static shader/CPU binding analysis, with no GPU execution, synchronization validation or full scene test. Checked-name count remains 622.


### Region-query accumulator provenance

CopyOutput's inputs now link to earlier stage writes. Bootstrap initializes input A to the largest finite float bit pattern and input B to zero. SampleField updates B with unsigned atomic maximum after its positive-result reduction; Refine also updates B with unsigned atomic maximum. Refine updates A with unsigned atomic minimum after clamping the candidate value against zero.

RefineSetup copies A minus one into a separate buffer that Refine reads during iteration. These writes and CPU descriptor bindings establish accumulation roles, but do not yet establish the full metric or field-sampling formulas. The atomics compare unsigned bit patterns; interpreting their ordering as ordinary float min/max requires the appropriate finite nonnegative domain, which is not proven for every path.

The archive payload hashes and relevant CPU instruction bytes were rechecked, and Ghidra annotations were saved and independently reopened. GPU execution, synchronization and real-scene behavior remain unverified. No new name or whole-system completion credit was added.


### Named region-query shader accessors

Four accessors are now saved as `GetRegionQueryBootstrapShader`, `GetRegionQuerySampleFieldShader`, `GetRegionQueryRefineShader`, and `GetRegionQueryRefineSetupShader`, with opaque descriptor-pointer returns. Their complete 819 instructions were reviewed against the fully read CopyOutput accessor; internal branch targets and identical external call targets were checked, and stage-string copy differences retained. Exact stage literals also agree with the native-hash archive matches above.

Eight original cached-entry calls across the four newly named accessors returned the expected descriptors without changing global state. Two additional cached calls checked the already named CopyOutput accessor, which receives no new naming credit. Saved names and signatures were independently reopened and freshly decompiled. Cold loading, path construction, fallback/error handling, concurrency and GPU execution remain untested; these are accessor-role reviews, not full shader-behavior audits.

Totals: 626 checked names. All four functions were already mapped to region queries, so mapped/unmapped counts remain 2,038/7,553 among 9,591 discovered functions.


### Refine accessor correction and work scheduling

The preceding naming batch transposed two accessor identities: `0x141276670` is `GetRegionQueryRefineSetupShader`; `0x141276a10` is `GetRegionQueryRefineShader`. Each accessor's own embedded stage label and compiled shader filename proves the corrected mapping. All five accessor-to-literal mappings are now explicitly checked. Both corrected names were saved and independently reopened; this adds no naming credit.

The CPU compute path prepares Setup and Refine work in a ten-pass loop before CopyOutput. A three-word work buffer begins as `(0,1,1)`, and Setup writes its first element. For valid ordered counters, the static Setup trace advances a cursor by the previous batch, subtracts it from the capacity-clamped total, and computes the next group count as `(batch + 63) >> 6`. The observed capacity uniform is 2,097,152. Counter names are analyst descriptions; wrap prevention, shared-data ordering and GPU execution remain unverified. Ghidra scheduling annotations were saved and independently reopened. Checked names remain 626.


### Indirect compute dispatch preparation

The 91-instruction wrapper is saved as `DispatchComputeIndirectWithCachedControls`. It takes an argument-buffer pointer, a mode and a 32-bit byte offset, and uses the global compute context. Region-query refinement supplies the work-count buffer prepared by RefineSetup.

In 1,296 connected original-code cases, effective argument addressing is buffer plus zero-extended offset; any nonzero mode selects the underlying writer's fixed mode 1. Preparation emits a seven-DWORD acquire-memory packet. Stale controls add a three-DWORD update; the indirect writer reserves eight DWORDs and advances its cursor only on platform-call success. Optional profiling still records the attempt on the tested error returns. Whole context, command-buffer bytes and guards were checked. The initial reference omitted the acquire-memory packet; its original helper was read and the reference corrected before the final run.

The actual GNM indirect-dispatch import is replaced by an argument recorder, so its packet encoding and GPU execution are not verified. Tests use default float controls and ample capacity; other limits remain explicit. Saved name/signature were independently reopened and freshly decompiled. Totals: 627 checked names, 2,039 mapped and 7,552 unmapped among 9,591 discovered functions.


### Controlinator detection mode differences

Seven hundred twenty complete original TriggerZone entry cases distinguish its three uncached EntireLevel Controlinator settings. Normal Controlinator detection requires a valid player index and bypasses the tested Power/activation gates. ControlinatorPossessable detection accepts original CtrlMode 1 or 2 (Possessable or FollowController) and applies Power/activation gates; ControlinatorAll omits the CtrlMode restriction while retaining those gates. GameState 2 is rejected by all three in these fixtures. Original Controlinator Power is independently registered at 0x80; it is not Sculpt's Power offset.

Another 72 complete-entry cases cover all four player indices with a deliberately permuted auxiliary channel mapping, plus wildcard, matching and missing names. Output follows the mapping byte rather than the player-index ordinal. With a valid index only that player channel is set. Modes 7/8 also accept invalid index 255 under their tested gates and set all five outputs. Failing threshold cases clear gadget output while preserving the accepted count as previously observed.

Whole fixture buffers and cleanup were checked, and Ghidra annotations were saved and independently reopened. Tests use valid glued Sculpt roots; PuppetHeart root writes/rollback, cached/bounded detection and invalid channel domains remain unresolved. No live gameplay or complete processor review is claimed. Checked names stay 627.


### PuppetHeart output selection and query mask

`BuildPuppetHeartRegionQueryMask` is now saved and independently reopened with a working register signature. Its complete 67-instruction body and 2,688 controlled original-code calls establish the mask contributions from composed labels, collidability, status bits and power. The conditional local-user scope helper was skipped with selector 255 and remains untested.

Original property registration identifies PuppetHeart `IsImp` at 0x36c; this is not a generic activation flag. The tested Controlinator path uses the composed-label mask for IsImp roots and descendant Sculpt label matching otherwise. Both paths write PuppetHeart `OutputPlayerValue` at 0x30c. With ConsiderPlayers disabled, the selected path writes one to all five channels. With it enabled, inherited source ownership selects the non-player channel or player channels, preserving unselected values. Failed detection thresholds restore all 20 prior output bytes.

48 root-output cases and 120 inherited-ownership cases passed with the original field metadata installed. Initial fixture omissions in output metadata and parent transform setup were corrected before these passing runs; they were fixture faults, not game faults. These cases cover the stated uncached paths, not the whole processor, every reference invariant, local-user scope or a complete gameplay lifecycle.

628 function names are checked among 9,591 discovered functions; 2,040 functions are mapped to systems. This is evidence about specific code behavior, not a percentage of the entire game being reverse engineered. Raw code and execution fixtures remain local.


### PuppetHeart local-user scope follow-up

The earlier selector-255 limitation is now narrowed by 4,480 additional connected original-code cases. `BuildPuppetHeartRegionQueryMask` calls the already named `PassesObjectPlayerMaskAndParentModeFilter`; a false result adds mask bit 0x10. No additional function-name credit is claimed.

4,096 cases cover selectors 0..3, the user-record enable byte, state 0/13, and all pairs of four-bit object masks. For unglued objects, an enabled user outside state 13 passes only when its bit is absent from the union of object bytes 0x24/0x25. Disabled records and state 13 reject.

384 further cases cover parent modes 1/2/3, absent or in-range parents, compact lookup words and matching/mismatching record modes. Mode 1 uses the high seven lookup bits; the other tested modes use the low seven bits and require the resolved record mode to match. A resolved parent-mode record rejects the filter. Missing parents or missing compact records pass. PuppetHeart storage remained unchanged on every call.

The out-of-range parent fallback scan, other parent modes, malformed references, complete producer invariants, concurrency and live gameplay remain unverified. Earlier test receipts retain their original narrower scopes. Counts remain 628 checked names and 2,040 mapped functions.


### PuppetHeart ancestry, glued roots and parent-record fallback

Saved and independently reopened `ResolvePuppetOrGluedObjectRootReference`, with a working unsigned reference return and explicit register arguments. The complete 100-instruction function is used by Controlinator detection and other object/game-update paths. 3,584 connected original-code cases plus 72 zero-index cases support its descriptive role; the original 164-instruction callee executes in these fixtures.

A category-11 PuppetHeart on the 16-bit ancestor chain returns immediately. Otherwise the function follows cached category-13..15 ancestry or uncached glued-object links, then permits the original input-parent resolver to override the result. Categories 0/1/10/11/17/41/42/95/96 preserve the result; other categories use a nonzero cached parent. A cached chain reaching zero can preserve the original input while the uncached glued path follows links to zero. These are distinct supplied contracts, not proof that both caches represent equivalent game state.

The optional reflected-parent tests deliberately supply metadata offset 0x60. That offset is test data, not a recovered original field. Microchip link lookup, cache construction, reference/category producer invariants, malformed or cyclic ancestry, negative references, concurrency and gameplay remain unverified.

The previously open local-user parent fallback scan now has 1,152 connected original-code cases. It skips reference -1 tombstones and requires both the complete packed parent reference and exact mode to match. A match rejects the user filter and adds mask bit 0x10; a missing match passes. Counts 0..5, first/middle/last matches and wrong-mode/reference records were checked. Whole world and context buffers matched explicit fixture writes after each batch. Larger counts and real-game producer invariants remain open.

Totals are 629 checked names and 2,041 mapped functions among 9,591 discovered functions. No completed Dreams feature or in-game verification is claimed. Raw code, native fixtures and private data remain local.


### Microchip input routing with original field metadata

Original initialization and registration independently identify Microchip `IsGluedGadget` at offset 0x138. This replaces the synthetic parent-flag offset for this follow-up suite; earlier receipts keep their explicitly narrower scope.

6,144 scenarios each execute the original `ResolveGluedOrMicrochipInputReference` and the connected `ResolvePuppetOrGluedObjectRootReference`: 6,144 direct calls and 6,144 root calls. Tests vary cached/uncached ancestry, sorted/linear search, independent input/record/parent packed-reference bits, record counts 0/1/2/3/5/8, grouped destination placement, property patterns and the actual IsGluedGadget byte. Complete object storage remained unchanged per scenario; the whole world buffer matched explicit fixture writes after each batch.

A nonzero IsGluedGadget selects the full parent reference before searching wires. Otherwise Microchip wire destination property 0x40f selects the opposite endpoint. The property identifier is established; its original user-facing label remains unresolved. Within the supplied contiguous destination runs, both search paths select the first matching property. Missing links return the resolver sentinel and let the root caller use its category-dependent parent fallback.

The first test expectation missed a real distinction: cached ancestry can normalize the input reference before wire search, while the uncached path can retain high packed bits. Original execution rejected that expectation; the corrected model was checked with independently varied input and record bits. No claim of cached/uncached equivalence for arbitrary state is made.

Wire creation/sorting invariants, arbitrary mixed packed-reference runs, discontiguous destinations, counts above eight, malformed state, concurrency and gameplay remain unverified. No extra naming credit is added: totals remain 629 checked names and 2,041 mapped functions.


### Original wire sorting connected to Microchip input lookup

Saved and independently reopened `SortWireRangeByDestinationAndSource`, with an explicit opaque working signature. Its complete 336-instruction body was read. 1,584 direct cases cover zero through 32 records; 864 larger-range cases cover counts up to 257 with budgets zero, one and the record count. The original partition and heap helpers execute in those larger tests. The partition helper's internal algorithm is not yet fully semantically reviewed and receives no naming credit.

For the supplied consistent-reference fixtures, results match independent ordering by destination index, destination property, source-object sequence and source property. The comparator distinguishes full-reference equality from normalized indices, so this tuple description is not a claim about arbitrary mixed packed references or duplicate object sequences. Small-range equality order was checked; stability is not claimed for larger ranges.

The tests establish that the movable record portion is 52 bytes within each 64-byte slot. The trailing 12 bytes remain in their original slot on the tested paths; their original meaning is not assigned. Payload multisets, expected order, external guards, objects and whole world storage were checked. The positive sort budget updates as floor(budget/2) plus floor(budget/4), with heap fallback when the remaining budget is nonpositive.

320 additional scenarios execute the original `SortGameWires` wrapper, then original Microchip input-wire lookup and root resolution on the actual sorted output. The sort sets its sorted-state flag; the lookup selects the matching destination-property 0x40f endpoint or sentinel, and the root receives that endpoint or its fallback. Only the profiling callback is a counting spy. Sorting, partition, heap, lookup and root algorithms execute original bytes.

Wire creation, arbitrary packed-reference combinations, comparator overflow, malformed references, full partition semantics, production scene invariants and gameplay remain open. Totals are 630 checked names and 2,042 mapped functions among 9,591 discovered functions.


### Wire equal-key partition and paired return

Saved and independently reopened `PartitionWireRangeByEqualKey`. The complete decompiled body was reviewed; all 1,947 original instructions were byte verified, with pivot selection, comparator/scan and return assembly anchors checked. This advances the earlier unresolved partition checkpoint.

1,920 direct original-code cases verify an independently calculated pivot and exact less/equal element counts. `RAX` and `RDX` delimit a nonempty half-open equal-key range: preceding keys are smaller and following keys larger. All-equal inputs return the entire input range. Counts up to 41 use the median of first/middle/last keys; counts from 42 use the median of three sampled triplet medians, with sampling step floor(count/8). The suite covers ten specified sizes from 33 to 257, eight seeds, six input shapes, consistent packed-reference bits and guarded offset spans.

A working 16-byte return type now records `equal_begin` in RAX and `equal_end` in RDX. A fresh caller decompilation uses both named fields and shows that sorting skips the equal-key span, recurses on the smaller outside range and iterates over the larger. This is a supported working type, not a recovered source declaration.

The movable 52-byte payload multiset, per-slot trailing bytes and external guards were checked; whole world, object and stack-guard storage matched at suite end. Arbitrary mixed packed references, duplicate object sequence values, comparator overflow and ordering invariants, malformed state, production scheduling and live gameplay remain unverified. Totals are 631 checked names and 2,043 mapped functions among 9,591 discovered functions.


### Wire max-heap adjustment

Saved and independently reopened `AdjustWireMaxHeap`, with explicit working arguments for array base, hole index, record count, held record and world handle. Its complete 201-instruction assembly and decompiled body were reviewed. The original range sorter calls it while building and popping fallback heaps.

4,176 direct original-code cases cover 16 specified counts from 1 to 257, holes at the root and other tree levels, six comparator profiles, two seeds, consistent packed-reference bits and three held-key choices. Each fixture starts with a valid max heap and bounds the held key by the parent of the original hole. The helper replaces the removed 52-byte record with the held record and restores global heap order under those preconditions.

Independent checks verify the exact removed-plus-held payload multiset and unchanged records outside the original hole's subtree. Per-slot trailing bytes, array guards, immutable held storage and the state handle were checked per call; whole world, object and stack-guard storage matched at suite end. The code promotes larger children, handles a final single child, then moves the held record upward without crossing the original hole.

The range sorter, equal-key partition and heap adjustment now have supported descriptive names and working signatures. Wire creation, arbitrary reference combinations, duplicate object sequences, comparator overflow, malformed/precondition-breaking inputs, production scheduling and live gameplay remain unverified. Totals are 632 checked names and 2,044 mapped functions among 9,591 discovered functions.


### Wire storage callbacks and insertion-path lead

89 original-code cases now verify `AppendGameWireSlot` and `ResizeGameWireStorage`: eight append cases and 81 grow/shrink/no-change combinations, including counts near the fixed storage extent. Complete 1 MiB storage and external guards match the independent expected changes. Both callbacks initialize a 52-byte prefix with two (0,0,0,1) vectors, absent endpoint references, zero property words and packed flags 0x308. Trailing slot bytes remain untouched.

Append returns the previous-count slot and increments the count. Resize initializes newly grown slots, stores the requested count, and leaves old records intact when shrinking. The count field follows 16,383 slots of 64 bytes. That layout arithmetic is not evidence that these callbacks enforce capacity or establish the complete scene-editing contract. Neither callback fills real endpoints or invalidates the Game wire-order flag.

A bounded static trace found an actual insertion path at `1407069d0`. For an already bounded current count, it compares the incoming list count with 0x3fff minus the current wire count. It writes a full 64-byte slot, increments the count, and later clears the sorted-state flag while setting other work flags. The subtraction assumes a bounded current count; no global overflow or capacity guarantee is claimed. The full-slot write differs from the callbacks' 52-byte initialization; trailing-byte meaning remains unresolved.

This producer remains unnamed and only partially reviewed. Selection rules, transforms, special property handling, event calls, cleanup, its full ABI and complete runtime behavior still need tracing. No extra naming or feature-completion credit is added: totals remain 632 checked names and 2,044 mapped functions.


### Animation record dispatch during wire insertion

Saved and independently reopened `DispatchAnimationWireRecordUpdate`. Its complete 194-instruction body was reviewed, including the original insertion caller, wire lookup and resource traversal. Original registration identifies Animation `HeaderAndDataPages` at offset 0x110. An existing active wire's source-property index selects a flattened 72-byte header record from those resource pages.

2,368 controlled scenarios execute the original dispatcher, original wire lookup and original leaf iterator: 304 reach a record handler and 2,064 take fallback. Tests cover one- and two-leaf trees, empty leaves, record boundaries, absent handles, active/inactive wires, sorted/linear lookup, packed-reference bits and property-argument truncation. The override selects one handler; otherwise record flag 0x4 selects between two handlers. Missing usable wire/header records select the fallback resource-writer path.

The three update handlers and fallback are explicit recording probes. This suite verifies which handler is selected, its register/stack arguments, signed result propagation, the output wire index, and copying the handler-updated 32-byte wire transform to the caller. It does not verify the handlers' record editing or allocation algorithms. Descriptor, page-handle pair, auxiliary, resource, object and output guards were checked per scenario; the whole world matched supplied fixtures plus allowed probe writes after each batch.

A twelve-argument working ABI now replaces the misleading inferred void return. A fresh insertion-caller decompilation consumes the named integer result and typed output transform. Deeper resource trees, malformed/negative indices, races, the full insertion function and live gameplay remain unverified. The larger insertion function remains unnamed. Totals are 633 checked names and 2,045 mapped functions among 9,591 discovered functions.


### Original Animation header/payload append and logical offsets

Saved and independently reopened `AppendAnimationHeaderAndPayloadRecord` and `GetPackedResourceTreeLogicalByteExtent`, after reviewing their complete 265- and 115-instruction bodies. The append path now executes real resource writing rather than the earlier fallback probe.

168 direct cases and 168 through the original wire dispatcher/lookup execute the original allocator, writer growth, finalization, interning, release and hashing code. The tests cover empty, nonempty, full-header and branched trees, three supported type-code rows, both element-size table variants, zero/aligned/unaligned payload lengths and growth across pages. Mutex/thread callbacks remain controlled and memory imports use host ABI adapters. This does not verify concurrent allocation or gameplay.

Payload bytes append to category-2 resource pages. Descriptor bytes 8..79 form the 72-byte category-3 header: the input data pointer is omitted, and header offset 4 receives the previous logical payload extent. Valid nonzero element-aligned payloads append a header and payload; tested zero/unaligned payloads preserve logical content. The returned index is total header records minus one, including -1 for an empty header tree. Exact header/payload streams, source-node immutability, descriptor/payload guards and handle-pair guards were checked. Through-dispatch cases also preserve the world and output transform while reporting no existing wire.

649 separate read-only cases establish that logical extent is 504 bytes for every nonfinal leaf plus the final leaf's used bytes. It is not the sum of stored payload bytes. For example, an element-aligned page containing 480 bytes still contributes 504 once another page follows. This distinction explains the stored offsets when alignment leaves gaps.

The three existing-record mutation handlers, other type rows, exhaustion/depth failures, malformed state, editing schedule, full wire insertion and playback remain unverified. Totals are 635 checked names and 2,047 mapped functions among 9,591 discovered functions.


### Existing Animation record update: scoped format-1 trace

The existing-record handler at `141077240` remains unnamed. Its format-1 branch now has 300 direct original-code cases and 300 through the original Animation wire dispatcher and lookup, with no replacement handler probe. These cases execute the original resource allocation, growth, finalization, interning, release and hashing code. Memory imports use host ABI adapters; mutex/thread callbacks remain controlled.

In this branch, each tested record contains a float32 time and an opaque 32-bit word. Both streams are rebased to the minimum of their origin times. Old keys at or below the first incoming time minus the original float32 1/60 constant are retained; old keys above the last incoming time plus that constant are retained. Incoming keys replace the intervening window. The result is appended after the previous payload, with a new 72-byte header; the old streams remain intact. Header bytes 36 through 67 are preserved from the old header. These are observed branch semantics, not recovered original source declarations.

Fixtures cover 0, 1, 3, 5 and 63 old records, six origin combinations and ten finite ordered incoming patterns. Exact complete header/payload streams, immutable inputs/source nodes and guards were checked. The connected cases also check the returned new record index, existing-wire index, output transform and unchanged world/source object. The 63-record cases exercise output resource growth while reading a single original source leaf.

Other format branches, flag-4/mode-5 behavior, exact tolerance-edge rounding, nonfinite times, multilevel source reads, malformed state, races, full insertion and playback remain unresolved. Identifying all 6,588 instructions is not a full semantic review. This checkpoint adds no name or completion credit: totals remain 635 checked names and 2,047 mapped functions among 9,591 discovered functions.


### Neighboring 48-byte Animation records and tolerance samples

The neighboring format-0 branch of the same unnamed handler now passes 300 direct original-code cases and 300 through the original Animation wire dispatcher and lookup. With flag 0 and auxiliary mode 0, records consist of a first float32 time followed by 44 bytes preserved exactly in these fixtures. They follow the same tested window replacement and origin rebasing model as format 1. The remaining fields are intentionally opaque; no transform-field meaning is inferred from their size.

Fixtures use 0, 1, 3, 5 or 10 old records in one source leaf, six origin combinations and ten incoming patterns. Full stored streams, preserved old/source bytes, replacement headers, output growth, inputs and guards match the independent model. The connected cases additionally check unchanged world/source object, returned record/wire indices and output transform. Original resource operations execute with the same controlled synchronization and host memory-import adapters as the previous checkpoint. Static inspection identifies additional code gated by auxiliary byte 0xb4 equal to 5 together with descriptor flag 4; that mode remains unverified.

Separately, 420 direct format-1 cases sample four float32 threshold centres, their adjacent representable input values and two intervals around old keys at 0.5 and 1.0. Original results match the explicit float32 arithmetic model. This closes the selected sampled boundary cases, not every rounding case or nonfinite input.

Other branches, special modes, deeper original source trees, malformed state, concurrency, full insertion and playback remain open. These branch findings add no whole-function review credit or inferred feature-completion percentage. Totals remain 635 checked names and 2,047 mapped functions among 9,591 discovered functions.


### Animation format-1 special-mode flags and producer-layout gap

600 direct original-code cases and 600 through the original Animation wire dispatcher now exercise descriptor flag 4 with auxiliary modes 0 and 5. Static assembly confirms two low-byte AND-with-1 operations. In the supplied mode-5 fixtures, the last retained old prefix pair has bits 1 through 7 of its second word cleared. The first incoming pair receives the same mask when the absolute float32 difference between the next old stored time and incoming rebased time is below the original +1/60 constant. Higher bytes and bit 0 remain intact. No original meaning is assigned to these flag bits.

The tests check the complete masked output against a separate model, exact replacement headers, preserved source nodes/input buffers, guards and original resource growth/finalization/hash behavior. Connected cases also validate the existing-wire result, returned new record index, output transform and unchanged world/source object. Mutex/thread callbacks remain controlled; memory imports use host ABI adapters.

A remaining representation gap is now explicit: flag 4 selects a 12-byte divisor for the incoming count, while the format-1 loop reads 8-byte pairs. These synthetic fixtures supply 8N pair bytes followed by 4N sentinel padding, and the observed branch consumes the pair region. This verifies branch behavior, not the real producer's extended input representation. The next-old comparison also uses the stored time against the incoming rebased time; the producer's origin invariants need tracing before interpreting that as a user-visible timing rule.

Other record formats, special-mode behavior for the 48-byte branch, real recording input layout, deeper source trees, nonfinite inputs, malformed state, concurrency, full insertion and playback remain unresolved. No whole-function name or completion credit is added. Totals remain 635 checked names and 2,047 mapped functions among 9,591 discovered functions.


### Animation input zero-value filter and converter boundary

Saved and independently reopened `ClearAllZeroAnimationInputForSelectedProperties`, after reviewing its complete 97-instruction body and original Animation producer callers. For selected property IDs, it clears the input buffer's byte count when all complete records have zero values; payload bytes, pointer and capacity remain unchanged. Other properties leave the buffer unchanged. Record times do not determine this filtering.

5,968 original-code cases cover every property ID from 0 through 0x57f, selected/nonselected controls and high-bit aliases, record counts 0/1/2/5/17, length remainders, first/middle/last nonzero values, second float components, NaNs and negative zero. Selected byte-valued properties use 8-byte records; one-float properties use 8-byte records; two-float properties use 12-byte records. Negative zero compares equal to zero, while float NaNs preserve a nonempty length. Complete guarded buffer descriptors and immutable payloads were checked. Huge counts, invalid buffers, concurrency and the complete editor schedule remain unverified.

The caller at `1407af650` groups input by endpoint/property, calls a converter and then this filter before wire insertion. The converter at `14109e4e0` has an unresolved computed jump: its current 37-instruction function body omits branch implementations. It remains unnamed and semantically incomplete. The earlier 12-byte count versus 8-byte read observation is still a producer-layout question; this helper does not resolve it. No completion credit is assigned to either larger function.

Totals are 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Animation converter jump-table recovery

Repaired the analysis boundary of the unnamed converter at `14109e4e0`. Its previous 37-instruction body omitted the code reached through the original 30-entry type table. A secondary property-based table has 23 entries. Following both tables and ordinary control flow recovers 1,095 reachable instructions, with no further unresolved indirect branches in that bounded graph. Calls remain separate review targets.

Every recovered instruction was matched against original executable bytes. Previously unassigned code was disassembled, added to the existing function, and given explicit jump-table destination overrides. The prior body/reference state was saved locally. Independent reopening and fresh decompilation now expose both switches and the branch bodies. Function count, names and saved signatures remain unchanged; executable and original archive files were not modified.

The recovered type-1 branch distinguishes basic and extended output paths. Its producer routing conditions and delegated writers still need tracing. Earlier flag-4/base-handler tests establish synthetic branch behavior, not that the real producer uses that combination. This recovery enables semantic work; it does not complete the converter or add naming/progress credit. Totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Animation converter basic/extended type-1 records

1,200 controlled cases now execute the original recovered converter's type-1 branch and its original 8-byte and 12-byte append writers. The basic path preserves complete emitted input pairs and compares the full value byte; the extended path compares only bit 0 and writes a 12-byte record with additional metadata. Both retain the first key, value changes and the final key in the supplied fixtures. This establishes actual converter output sizes, not the complete producer-to-update routing contract.

Tests cover counts 0/1/2/3/7/17, source strides 8/16, constant/alternating/run/low-bit-equivalent values, reversed finite times, modes 0/5 and five auxiliary flag values. Exact output lengths, basic output bytes, defined extended fields, buffer/bounds guards, unchanged destination outside emitted records and source/auxiliary immutability were checked. Three extended bytes between the value byte and metadata are not asserted or assigned a field meaning. Tests use ample capacity; short buffers and nonfinite times remain unverified.

The empty type-1 path appends nothing and zeros both supplied time outputs. Basic records accumulate minimum/maximum emitted times. The tested extended path uses maximum for both outputs: 400 cases distinguish its first output from the minimum emitted time, matching the original VMAXSS instructions. This is recorded as observed behavior, without assuming either an intended minimum-bound contract or a game bug. Single-record extended metadata includes the mode-5 bit; the tested multi-record path omits it.

The converter's other branches/callees, producer routing, mixed-format update eligibility and live editing remain unresolved. No whole-function name or completion credit is added. Totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Producer routing separates mixed-format conversion from base updates

A scoped static assembly trace now follows the producer's final override argument through insertion into the Animation dispatcher. When the producer finds an existing basic header, mode 5 or its initial extended-input condition sets both the extended indicator and override low byte. An existing extended header takes extended=1 and override=0 in that selection block.

The override is saved in the producer's stack frame, loaded after allocating the outgoing argument area, and passed as the final insertion stack argument. Insertion forwards that argument to the dispatcher. The already reviewed dispatcher selects handler `1410705f0` for a nonzero override, ahead of its ordinary old-header flag selection.

This constrains the earlier experiments: forced flag-4/base-handler cases verify synthetic branch behavior, but do not establish this producer's real mixed-format update path. The converter's actual 12-byte extended output therefore needs to be traced through the override handler, rather than interpreted using only the base handler's 8-byte reads. The earlier representation gap is narrowed to that transition path; it is not evidence that the game stores malformed records.

Original bytes for the producer and insertion captures were rechecked while saving the scoped annotations. This is static data-flow evidence, not full producer execution. Repeated endpoint/property groups, missing records, alternate producer branches and override-handler mutation algorithms remain unresolved. No whole-function name or completion credit is added; totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Original type-1 basic-to-extended transition

The override handler's type-1 branch now has 300 cases through the original dispatcher/lookup and another 300 that first run the original converter and its byte writers. In the connected suite, actual 12-byte converter output is supplied to the original override path. This verifies the previously missing scoped connection without a replacement record-handler probe.

Retained old 8-byte pairs become 12-byte records with rebased time, the low value bit and metadata 0x700. Three intermediate bytes in converted old records remain unasserted. Incoming extended records are read at stride 12 and preserved exactly except for time rebasing. The merge retains old keys outside the tested tolerance window, appends replacement data after the old stream, and appends a 72-byte header with the new 12-byte record count and prior data extent. Complete headers and defined payload fields match an independent model.

Fixtures cover 0/1/3/5/63 old records in one source leaf, six origin combinations and ten finite incoming patterns with auxiliary mode 0 and zero auxiliary flags. Tests check original source-node/input immutability, output growth, existing-wire and new-record indices, output transform, unchanged world/source object and guards. Original allocation, growth, finalization, interning, release and hashing execute; memory imports use ABI adapters and mutex/thread callbacks remain controlled.

This resolves the 8-byte-versus-12-byte representation question for this bounded transition: the producer's override path converts retained basic records and consumes extended incoming records. Full producer/insertion execution, mode 5, other formats/flags, deeper source trees, malformed state, concurrency and playback remain unresolved. The 6,254-instruction override handler remains partially reviewed and unnamed. Totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Connected mode-5 transition metadata

2,400 additional cases execute the original type-1 converter, original byte writers, original wire dispatcher/lookup and actual override handler with eight specified auxiliary/dispatcher flag profiles. The tests vary modes 0/5, auxiliary flag values 0/1/255 and both dispatcher flags, alongside the prior five old-record counts, six origin combinations and ten finite incoming patterns.

In the tested mode-5 branch, the last retained prefix key receives metadata 0x709 when auxiliary flags are nonzero and both dispatcher flags are clear. Either dispatcher flag suppresses that change, leaving the ordinary 0x700 metadata in these fixtures. The first incoming key has a separate rule: when the next old stored time is within the original float32 tolerance of its rebased time, its metadata becomes 0x700 OR (metadata AND 0x3f). Original assembly and the independent field model agree. No user-facing flag names are inferred.

Checks cover exact complete headers, expected output length, rebased times, defined old-record fields and all incoming fields including the conditional metadata mask, original input/source-node/world immutability, guards, returned indices and output transform. Three padding bytes in converted old records remain unasserted. Real resource growth/finalization/interning/release/hash executes with controlled mutex/thread callbacks and host memory-import adapters.

This extends the connected transition to selected mode-5 flag combinations. Exhaustive rounding, other record formats/flags, deeper original source trees, full producer/insertion scheduling, malformed state, concurrency and playback remain unresolved. The handler remains unnamed and partially reviewed. Totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Updating existing extended type-1 records

The already-extended update path now has 300 connected mode-0 cases, 2,400 mode/flag-profile cases and 960 focused cases with varied old metadata. Each executes the original converter and byte writers, then original dispatcher/lookup with override 0 and old-header flag 4, reaching the real extended handler. No record-handler probe is used.

Mode 0 preserves complete retained and incoming 12-byte records except rebased times. Mode 5 applies different boundary rules from basic-to-extended conversion: the last retained prefix key preserves its low metadata nibble when auxiliary flags are nonzero and dispatcher flag A is clear, except that a zero low-three-bit pattern becomes 9. Otherwise that boundary update clears the low four bits. Dispatcher flag B suppresses the prefix modification. Existing metadata's upper 16 bits remain unchanged in these fixtures.

When the first incoming key lies within tolerance of the next old stored time, its metadata inherits old bits 6 through 15. Lower bits combine old/incoming state conditionally on the old low-three-bit pattern and auxiliary flags. The focused cases vary these old bits independently of incoming metadata, verifying inheritance rather than a shared constant. User-facing meanings of the bits remain unresolved.

Complete header and payload streams match independent models, including the conditional masks. Tests also check returned indices, output transform, world/source-object/input/source-node immutability and guards. Original source counts include 42 records filling a 504-byte leaf, exercising output growth. Original allocator, finalizer, interning, release and hashing execute with adapted memory imports and controlled mutex/thread callbacks.

Other types, exhaustive rounding/flag combinations, deeper original source trees, full producer/insertion execution, malformed inputs, concurrency and playback remain unverified. The 6,366-instruction extended handler is partially reviewed and unnamed. Totals remain 636 checked names and 2,048 mapped functions among 9,591 discovered functions.


### Working Animation record layouts and argument types

Saved and independently reopened three explicit working types: the 80-byte input descriptor, 72-byte stored header and 8-byte header/data page-root pair. Their sizes and member offsets follow original assembly and the preceding append, converter and update evidence. Input pointer, packed byte count, type code, record flags, origin and resource roots now appear as named fields in decompiled code. Unresolved spans stay opaque; the two range values retain neutral names because the observed converter behavior does not establish a min/max contract.

Append and dispatch now accept typed descriptor/root pointers. The three partially reviewed update handlers have working pointer/register/stack argument types consistent with the traced dispatcher and original-code suites, including the two extra byte arguments used by override/extended handlers. Their context pointers remain opaque. These are analyst working layouts and calling signatures, not recovered original source declarations.

Independent reopening checks every defined member offset/size, original instruction bytes and fresh decompilation for all five functions. Only the five expected signatures changed; all 9,591 function names remain intact. Prior signatures/comments were saved locally. The larger handlers remain unnamed and partially reviewed, with no extra review or feature-completion credit. Totals remain 636 checked names and 2,048 mapped functions.


### Bounded 8-byte and 12-byte input writers

Defined and independently reopened `AppendBytes8ToBoundedBuffer` and `AppendBytes12ToBoundedBuffer`, previously unassigned code called by the Animation input converter. Their complete 128- and 192-instruction bodies form closed routines. A working 24-byte buffer type exposes data pointer, byte length and capacity. Fresh decompilation uses these fields and both descriptive names.

8,118 direct original-code cases cover capacities 0 through 32, initial lengths 0 through 40 and three source byte patterns. Exact complete destination, source and guarded descriptor checks include 1,500 partial-capacity cases and 4,752 already-over-capacity cases. Each helper appends only the available source prefix, stops advancing length at capacity, and performs no allocation or growth. Partial append is not an atomic whole-record operation. Their caller's handling of short capacity still requires tracing.

The preceding connected converter/update suites already execute both original writers with ample capacity. Direct tests add their short/full/overfull-buffer behavior. Uint64 wraparound, pointer aliasing, invalid pointers, concurrency and the complete producer schedule remain unverified.

These new definitions expand the discovered inventory rather than renaming existing functions. All 9,591 previously defined names/signatures remain unchanged. Totals are 638 checked names and 2,050 mapped functions among 9,593 discovered functions. This remains helper review, not whole-game completion.


### Byte-valued Animation input conversion

Defined and independently reopened `ConvertByteValueAnimationInputKeys`, the complete 192-instruction helper selected by the top-level converter's type-11 branch. Both basic and extended paths compare the full value byte. This differs from type 1, whose extended path compares only bit 0. Both retain the first key, value changes and the final key in the tested fixtures. Basic output preserves complete 8-byte pairs; extended output adds metadata in 12-byte records. Three intermediate extended bytes remain unasserted.

1,200 original-code cases execute the actual top-level dispatch, this helper and its original writers. The writers are byte-for-byte copies of the two bounded helpers reviewed previously. Tests cover counts 0/1/2/3/7/17, strides 8/16, modes 0/5, five auxiliary flag values, repeated/changing/low-bit-equivalent values and reversed finite times. Defined output fields, exact basic pairs, lengths, guarded bounds/descriptor, immutable source/auxiliary state and untouched destination outside emitted records match the independent model.

Empty input zeros both time outputs. Basic time outputs accumulate minimum/maximum; tested extended outputs both accumulate maximum. Single-record extended metadata includes the mode-5 bit; the tested multi-record path omits it. These are observed native behaviors, not an assumed min/max contract or recovered source declaration. Short buffers, nonfinite times, huge counts, aliasing, concurrency and full producer/gameplay behavior remain unresolved.

The existing 9,593 names/signatures remain unchanged. The new function raises totals to 639 checked names and 2,051 mapped functions among 9,594 discovered functions. The top-level converter and its other formats remain incomplete.


### AutoKeyframe binding and external animation leads

Revalidated the original ERecordMode registration and Machine field binding against the executable bytes: 165 enum-registration instructions, 928 field-registration instructions and all nine enum labels. Mode 2 is Keyframe and mode 5 is AutoKeyframe. The Machine record_mode byte at offset 0xb4 is the same auxiliary field used by the recent producer/converter/update chain. Earlier checkpoints called this value simply mode 5; its native registered name is now connected to those findings.

Saved and independently reopened a working byte enum plus a partial Machine recording prefix. Fresh decompilation now displays AutoKeyframe comparisons by name in five typed functions. The prefix exposes only the verified mode field and the still-opaque byte at 0xd6; it is not a declaration of the complete 0x43e0-byte Machine. Names and review counts are unchanged, and the large handlers remain partially reviewed.

External leads were also checked. The [official v2.58 notes](https://docs.indreams.me/en/whats-happening/updates/release-notes/dreams/v258) date the animation-canvas update to June 2023 and describe its additional recording features. The [recording guide](https://docs.indreams.me/en/create/resources/recording-modes) provides user-visible behavior to investigate, but does not identify numeric enum values or metadata bits. [The animation developer's first-hand overview](https://tadcordle.github.io/projects/dreams.html) describes invisible animation wires and reduced gadget/wire usage, consistent with the architecture being traced; it does not prove a source/binary match. The [official stream index](https://docs.indreams.me/en-US/create/resources/mm-streams-create) provides animation VOD leads; those videos were located, not visually audited in this checkpoint.

Local package metadata contains APP_VER=01.00 and VERSION=02.64. Those fields alone do not establish the imported executable's exact release build, so neither newer documentation nor older coding streams are treated as an exact implementation match. The AutoKeyframe enum binding comes from original registration, not UI ordering or inference from the published videos. Metadata-bit meanings and complete mode transitions remain unresolved. Totals remain 639 checked names and 2,051 mapped functions among 9,594 discovered functions.


### 16-bit word-valued Animation input conversion

Defined and independently reopened `ConvertWordValueAnimationInputKeys`, the complete 192-instruction helper reached through seven property-specific routes in the converter's type-2 branch. It compares the full 16-bit value word in both basic and extended formats. Tests explicitly distinguish values with equal low bytes and different high bytes. This is a word-valued equality path; no floating-point or signed-value interpretation is inferred.

8,400 original-code cases execute all seven property routes, the actual helper and original writers. They cover counts 0/1/2/3/7/17, strides 8/16, basic/extended output, None/AutoKeyframe context modes, five auxiliary flag values, repeated/changing values and reversed finite times. First/change/last selection, exact basic 8-byte pairs, defined extended 12-byte fields, lengths, guarded bounds/descriptor and input/auxiliary immutability match the independent model. Two intermediate extended-record bytes remain unasserted.

Both writer bodies are byte-identical to the bounded 8-byte/12-byte helpers already reviewed. Empty input zeros both range outputs; basic output uses minimum/maximum emitted times, while the tested extended path uses maximum for both outputs. Single-key AutoKeyframe metadata and multi-key metadata follow the observed original rules. Short buffers, nonfinite times, huge counts, aliasing, concurrency and complete producer/playback remain unverified.

All 9,594 previously defined names/signatures remain unchanged. Totals are 640 checked names and 2,052 mapped functions among 9,595 discovered functions. Other converter formats remain incomplete.


### 32-bit and floating-point Animation input converters

Defined and independently reopened `ConvertDwordAnimationInputKeys`, `ConvertDwordPropertyAnimationInputKeys` and `ConvertFloatAnimationInputKeys`. Their complete 184/184/181-instruction bodies distinguish raw 32-bit equality from floating-point equality. The two integer routines have the same normalized instruction flow but different dispatch routes and writer copies.

53,760 original-code cases execute the actual primary/secondary dispatcher, helpers and byte writers: 1,920 for the primary integer path, 40,320 across all 21 integer property routes, and 11,520 for all three primary float routes plus three sampled property routes out of 393. Counts 0/1/2/3/7/17, strides 8/16, basic/extended formats, None/AutoKeyframe modes, five auxiliary flag values and eight patterns cover repeated/changing values, equal low words, signed zero, quiet NaN payloads and reversed finite times.

The integer paths distinguish positive/negative-zero bit patterns and collapse identical NaN bit patterns. The float path treats signed zeros as equal and emits repeated NaNs as changes. Complete 8-byte/12-byte output records, lengths, guarded descriptors/time outputs, untouched destination outside output and source/auxiliary immutability match independent models. Empty time outputs are zero; basic time accumulation is minimum/maximum, while the tested extended paths use maximum for both. Original writer copies are byte-identical to the bounded helpers already reviewed. Nonfinite times, signalling NaNs, huge counts, short buffers, aliasing, concurrency and full producer/playback remain unresolved.

Four already identified Animation routines—the large top-level converter and three update handlers—are now mapped to their subsystem while retaining unreviewed status. Their ownership follows original call chains and the registered Animation resource field; this adds gray squares, not name or completion credit. Including known unfinished code makes the subsystem denominator more honest.

The new definitions preserve all 9,595 existing names/signatures. Totals are 643 checked names and 2,059 mapped functions among 9,598 discovered functions; 7,539 remain unmapped. Other formats and the four large routines remain incomplete.


### Vector and 64-bit Animation input converters

Defined and independently reopened `ConvertFloat2AnimationInputKeys`, `ConvertFloat3AnimationInputKeys`, `ConvertFloat4AnimationInputKeys` and `ConvertQwordAnimationInputKeys`. Complete original bodies contain 233, 269, 268 and 253 instructions respectively.

31,200 original-code cases exercise all nine primary vector routes and the one 64-bit property route through the actual main/secondary dispatcher. Counts 0/1/2/3/7/17, two source strides, basic/extended formats, None/AutoKeyframe modes and five auxiliary flag values cover repeated/changing values, each individual vector component, signed zero, quiet NaNs, reversed finite times, high 64-bit changes and source-padding-only changes.

All retain first/change/last keys. Every vector component participates in floating comparisons: signed zeros compare equal and repeated quiet NaNs produce changes. The 64-bit path compares the entire value and ignores source padding when selecting keys. Basic vector records occupy 12/16/20 bytes; extended records occupy 16/20/24 bytes. The 64-bit records occupy 16/24 bytes. Vector records are checked completely. The 64-bit extended record has opaque padding at offsets 4..7 and 20..23; these bytes are deliberately excluded from assertions. Original source bits, metadata fields, bounded-buffer descriptors, destination guards and time outputs match independent models; source and auxiliary buffers remain unchanged. The float2 basic writer is byte-identical to the independently reviewed bounded 12-byte writer.

Tests use ample capacity and finite times. Invalid pointers, signalling NaNs, aliasing, concurrency, full producer behavior and playback remain unresolved. These are descriptive working signatures, not recovered source declarations. All 9,598 existing names/signatures are preserved. Totals are 647 checked names and 2,063 mapped functions among 9,602 discovered functions; 7,539 remain unmapped. The larger converter and update handlers remain partially reviewed.


### Signed-byte and Boolean Animation key selection

Defined and independently reopened `ConvertSignedByteAnimationInputKeys` after reviewing its complete 211-instruction original body. It compares sign-extended low bytes after conversion to float and multiplication by 0.01, but writes the original byte rather than a scaled float. All 19 property dispatch routes passed 45,600 original-code cases covering counts 0/1/2/3/7/17, two strides, basic/extended layouts, two recording modes and five auxiliary flag values. Signed-byte boundaries, changes confined to upper source bytes, repeated/changing values and reversed finite times are included. Both actual writer copies match the previously reviewed bounded writers byte for byte.

Separately, 2,400 original-code cases verify the large converter's inline Boolean branch. Basic keys compare the full low byte; extended keys compare only the lowest bit and store canonical 0/1. Thus source bytes 1 and 3 trigger different selection behavior between the formats. Both paths retain first/change/last keys. Defined time, value and metadata fields, guarded descriptors, destination guards and source/auxiliary immutability match independent models. Bytes 5..7 in the 8/12-byte records remain opaque and are excluded from assertions. Empty time outputs are zero; tested basic outputs accumulate minimum/maximum, while extended outputs use maximum for both.

These fixtures use ample output capacity and finite times. Invalid input, aliasing, concurrency, full producer behavior and playback remain unresolved. The Boolean result adds branch evidence, not a checked-name credit for the larger converter. All 9,602 existing names/signatures are preserved. Totals are 648 checked names and 2,064 mapped functions among 9,603 discovered functions; 7,539 remain unmapped. Transform and other inline converter branches still need review.


### Shared typed-value comparison and wider Animation formats

Reviewed and independently reopened `AreTypedValueRecordsEqual`, a shared 77-instruction comparison used by Animation conversion and other native callers. The recovered 22-entry dispatch table selects exact 4/8/12/16-byte comparisons or a table-selected number of floating-point components. A type byte at offset 36 and floating field at offset 32 must match first. The meaning of the floating field remains unresolved. Type 30 additionally compares only the float at offset 4 and byte at offset 8; types 0, 29 and byte codes above 30 ignore the payload after those common checks. These describe the executable's behavior, not a claim that every byte code is a valid game type.

40,192 original-code cases cover all 256 type-byte values, independent changes at every position of a 40-byte record, signed zeros, quiet NaNs and ordinary unequal floats. Inputs stay unchanged. The supported return contract is Boolean in AL; interpreting the untouched upper return-register bits as part of the result would be incorrect. The saved signature uses two opaque pointers; formal source layouts and field names are not claimed. All 9,602 other names/signatures are preserved.

Another 8,160 original-code cases exercise the larger converter's inline eight-component and 64-bit paths. Every one of the eight float components can trigger a new key; signed zeros compare equal and quiet NaNs trigger changes. Basic/extended widths are 36/40 bytes for eight floats and 16/24 bytes for the 64-bit path. First/change/last selection, defined output bytes, metadata, guarded descriptors, time outputs and source/auxiliary immutability match independent models. The 64-bit extended padding at offsets 4..7 and 20..23 remains deliberately unasserted. These branch findings do not give the larger converter a complete-review credit.

Tests use valid buffers, ample capacity and finite times. Full producer/playback, invalid pointers, aliasing and concurrency remain unresolved. Totals are 649 checked names and 2,065 mapped functions among 9,603 discovered functions; 7,538 remain unmapped. Generic typed-value conversion still requires further layout and connected-path review.


### Main Animation input conversion and key reduction

Reviewed the complete recovered 1,095-instruction main converter and saved `ConvertAndReduceAnimationInputKeys` with a supported ten-argument void signature. It chooses basic or extended recording formats, dispatches by type and property, and retains first/change/last keys according to the relevant value comparison. Original producer callers ignore the return register. Both dispatch tables and all delegated helper roles have now been read; naming the converter does not establish complete editing or playback behavior.

74,400 connected original-code cases exercise its generic typed-value branch with the actual shared comparison routine. Both formats read 48-byte strided source records: time at offset 0 and the typed value at offset 8. Basic output copies all 48 selected source bytes. Extended output occupies 56 bytes, preserves time and typed-value bytes 8..44, and adds metadata at 48..51. Padding at 4..7, 45..47 and 52..55 is deliberately excluded from assertions. Type changes, changes to the common floating field, payload changes that the selected type ignores, signed zeros, quiet NaNs, padding-only changes and reversed finite times match an independent selection model. Guarded descriptors, defined output bytes, time outputs and source/auxiliary immutability are checked.

16,824 additional original-code cases cover every primary type byte, all 1,408 in-range property IDs and two upper-bit aliases. Recognized empty formats clear both time outputs; unsupported routes leave them unchanged and emit nothing, including with count 1. Property dispatch uses the low 16 bits of the ID. Earlier Boolean, wider inline and delegated-helper suites cover the other conversion paths; float property routes were sampled, not exhaustively exercised with nonempty inputs.

The saved definition preserves all 9,602 other names/signatures and every original instruction byte, and was independently reopened and freshly decompiled. Tests use valid buffers, ample capacity and finite times. Invalid pointers, out-of-range property IDs, aliasing, concurrency, full producer integration and playback remain unresolved. The three large record-update handlers still need further review. Totals are 650 checked names and 2,065 mapped functions among 9,603 discovered functions; 7,538 remain unmapped.


### Basic Animation interval updates across recording formats

5,400 original-code cases cover eighteen basic recording format codes through the actual update handler and its scalar/vector delegates. The tested updates rebase both streams to the minimum origin, retain old keys at or below the first incoming time minus 1/60 second and strictly above the last incoming time plus 1/60 second, then insert the incoming interval. Complete header/data streams, input/source immutability and guards match an independent model. Each format includes a maximal one-leaf old payload to exercise original output-resource growth.

The remaining basic format contains transform arithmetic. Another 300 cases pass with valid identity frames, unit identity rotations and scale one, using the original local libc `__isinff` implementation. Frame data is consumed from stored-header bytes 36..67 and input-descriptor bytes 44..75; treating those fields as arbitrary opaque bytes is not a valid transform fixture. The scoped transform cases preserve the tested position/quaternion payloads while applying the same interval merge. Other frames, rotations and scales still need investigation.

All nineteen supported basic formats now have these scoped merge checks. This does not establish the full 6,588-instruction updater: special flags, other recording modes, deeper original-source trees, nonfinite times, full producer integration and playback remain unresolved. The four delegated scalar/vector helpers are newly mapped to Animation from the original call chain, but remain unnamed and unreviewed. This adds four gray squares, not semantic-review credit. Totals stay at 650 checked names, with 2,069 mapped functions among 9,603 discovered functions; 7,534 remain unmapped.


### Transform recording frames beyond identity

3,840 additional original-code cases verify the basic transform-update path with translated frames, unit rotations and positive uniform scales 0.5, 1 and 2. For the tested domain, incoming key transforms follow `inverse(H) * D * K * O * inverse(W)`, where H is the stored header frame, D the incoming descriptor frame, K the incoming key, and W/O the updater's third/fourth frame arguments. Multiplication means transform composition, so the order matters. These labels are analyst descriptions, not recovered source names.

The formula was fixed before running this fresh set of sixteen independently generated frame profiles. Tests include empty and retained old streams, different time origins, interval positions and output-resource growth. Old keys outside the replaced interval remain in their stored frame; incoming keys receive the frame corrections and time rebasing. Exact headers, old bytes, times and guards are checked. Incoming positions, scales and rotations match the independent composition model, allowing quaternion sign equivalence; maximum observed absolute error was 0.000004990 against a declared tolerance of 0.0005. Original transform arithmetic and the byte-verified local libc infinity classifier execute.

Saved and independently reopened `AnimationTransformFrameWorking32`, exposing position, uniform scale and quaternion components in stored-header bytes 36..67 and input-descriptor bytes 44..75. The field is explicitly named `reference_frame_format4`: interpretation in other formats remains unresolved. Every existing function name/signature and the original updater instruction bytes are unchanged. This adds working type information and branch evidence, not name or whole-handler completion credit. Singular/negative scales, nonunit/nonfinite rotations, special flags/modes, deeper source trees, complete producer integration and playback still need investigation. Checked names remain 650.


### Scalar Animation interval merge and parent-tree reads

Reviewed all 1,022 original instructions of `MergeScalarAnimationRecordInterval` and saved a supported five-pointer signature with a signed last-header-index return. The basic updater delegates type codes 2, 5, 24 and 25 to this routine. The complete body includes time-origin rebasing, old prefix/suffix selection, incoming insertion, header flag handling, parent-tree seeks, output growth and header-index calculation. AutoKeyframe/extended-input conditions were read statically; their production behavior is not claimed verified here.

3,744 additional original-code cases cover old streams of 63, 64, 126 and 127 keys with logical data offsets 0, 16 and 504 bytes. Old data spans one to four leaves, including parent nodes, exercising cross-leaf reads that the earlier one-leaf fixtures did not reach. Thirteen incoming time patterns and different origins match an independent interval model. Complete headers/data, original source nodes, immutable input/context buffers and guards are checked. Output resource growth, hashing and finalization execute original code. The resolved double-precision `pow` import uses an explicit host ABI adapter; this boundary is not claimed to execute the console libc implementation.

Together with the earlier 1,200 scalar cases from the basic-format family suite, these checks support the descriptive merge role. The saved name/signature persisted after independent reopening and fresh decompilation, preserving all 9,602 other names/signatures and the original instruction bytes. Deeper parent levels, other flags/modes, nonfinite or invalid inputs, concurrency, full producer integration and playback remain unresolved. Totals are 651 checked names among 9,603 discovered functions; system mappings remain 2,069, with 7,534 unmapped. The three vector delegates and larger mutation handlers still need review.


### Three-component Animation merges and page gaps

Reviewed all 1,050 original instructions of `MergeFloat3AnimationRecordInterval` and saved a supported five-pointer signature with a signed last-header-index return. The basic updater selects it for type codes 3, 7 and 17. Each key occupies 16 bytes: time plus three components. A full leaf holds 31 keys in 496 bytes, leaving eight bytes of its 504-byte payload capacity unused. The reader explicitly corrects for these gaps when seeking old records; the new header uses logical page extent rather than the flattened sum of used bytes.

2,808 additional original-code cases cover old streams of 31, 32, 62 and 63 keys, data offsets 0, 16 and 504, and one to four source leaves. Thirteen incoming interval patterns and different time origins match independent models for retained keys, incoming insertion and origin rebasing. Complete headers/data, source-node immutability, all input buffers and guards are checked. Original resource growth, hashing and finalization execute; the resolved power import uses the explicitly documented host double-precision adapter. The earlier basic-format suite supplies another 900 one-leaf cases across these three routes.

The name/signature persisted after independent reopening and fresh decompilation, with all 9,602 other names/signatures and original instruction bytes unchanged. AutoKeyframe/extended-input conditions were read statically but are not claimed production-verified. Deeper source trees, other flags/modes, nonfinite/invalid inputs, concurrency and full producer/playback remain unresolved. Checked names are now 652; mappings remain 2,069 of 9,603 discovered functions, with 7,534 unmapped. The two other vector delegates and larger mutation handlers remain unfinished.


### Two-component Animation interval merge

Reviewed all 1,042 original instructions of `MergeFloat2AnimationRecordInterval` and saved its supported five-pointer signature and signed last-header-index return. The basic updater selects this helper for type codes 8, 20 and 21. Each key stores time plus two components in 12 bytes; 42 keys fill a 504-byte leaf exactly, so no per-leaf record gap is required.

2,808 additional original-code cases cover old streams of 42, 43, 84 and 85 keys with offsets 0, 12 and 504 across one to four source leaves. Thirteen incoming interval patterns and differing time origins match independent models for retained keys, inserted keys and rebased times. Complete header/data streams, source nodes, input/context buffers and guards are checked. Original resource growth, hashing and finalization execute, with the resolved power import handled by the documented host double-precision ABI adapter. The earlier basic-format suite adds 900 one-leaf cases across these three routes.

The name/signature persisted after independent reopening and fresh decompilation. Every original instruction byte and all 9,602 other names/signatures remain unchanged. AutoKeyframe/extended-input conditions were read statically but are not claimed production-verified. Deeper trees, other flags/modes, nonfinite/invalid inputs, concurrency and full producer/playback remain unresolved. Totals are 653 checked names and 2,069 mapped functions among 9,603 discovered functions; 7,534 remain unmapped. The four-component delegate and larger mutation handlers remain unfinished.


### Four-component Animation interval merge

Reviewed all 1,011 original instructions of `MergeFloat4AnimationRecordInterval` and saved its supported five-pointer signature and signed last-header-index return. The basic updater selects it for type codes 6, 15 and 16. Each key occupies 20 bytes: time and four components. Twenty-five keys occupy 500 bytes of a 504-byte leaf, leaving four bytes unused. The reader explicitly adjusts for this gap when seeking retained old keys.

2,808 additional original-code cases cover old streams of 25, 26, 50 and 51 keys, offsets 0, 20 and 504, and one to four source leaves. Thirteen incoming interval patterns and differing origins match independent models for prefix/suffix retention, incoming insertion and time rebasing. Complete headers/data, source nodes, input/context buffers and guards are checked. New header offsets follow logical page extent, not the flattened sum of used bytes. Resource growth, hashing and finalization execute original code; the resolved power import uses the documented host double-precision ABI adapter. The earlier basic-format suite adds another 900 one-leaf cases across the three routes.

The name/signature persisted after independent reopening and fresh decompilation, preserving all 9,602 other names/signatures and original instruction bytes. AutoKeyframe/extended-input conditions were read statically but are not claimed production-verified. Deeper trees, other flags/modes, nonfinite/invalid inputs, concurrency and full producer/playback remain unresolved. All four scalar/vector delegates now have descriptive names and scoped evidence; this does not complete the larger mutation handlers. Totals are 654 checked names and 2,069 mapped functions among 9,603 discovered functions, with 7,534 unmapped.


### Basic Animation replacement boundaries and header flags

864 additional original-code cases check both replacement edges and their immediately adjacent float32 values across eighteen basic formats. Old and incoming times are rebased before the original float32 minus/plus 1/60-second margins are applied. Old keys at or below the left boundary survive. Old keys exactly at the right boundary are removed; only keys strictly above it survive. Negative, zero and positive incoming times, single-key intervals and differing origins are included. Complete header/data streams, value/time bits, source immutability and guards match independent models. This establishes stored-key replacement conditions, not UI snapping or playback interpolation.

Another 5,202 cases check how old and incoming 16-bit header flags combine. Every individual bit except bit 2, plus zero and all other bits set, is paired across both records in each of the eighteen formats. Under this tested basic-route condition, the saved flags equal `(incoming & 0xff01) | (old & 0x00f8) | ((old | incoming) & 0x0002)`: incoming supplies bit 0 and bits 8..15, old supplies bits 3..7, and bit 1 is the OR of both. No gameplay meanings are assigned to these bits. Bit 2 (value 4) is kept clear because it selects the separate extended-record path.

Tests use mode 0, valid one-leaf sources and finite ordered times. Transform format 4, other modes and extended-record flag behavior retain their separate scopes. These findings add branch evidence without naming or marking the larger updater complete. Checked names remain 654; the full reverse-engineering task is unfinished.


### Connected scalar/vector basic-to-extended recording updates

3,900 original-code cases connect the real main converter and byte writers to the real wire dispatcher, lookup, basic-to-extended handler and its four scalar/vector delegates. All thirteen scalar/vector type-code routes are included; type 2 samples one float property route. Existing basic keys and newly converted extended keys pass through the actual transition path rather than a replacement handler.

Under the tested mode-0, zero-auxiliary-flags conditions, retained basic keys expand by four bytes and receive metadata 0x700. Incoming extended records are preserved byte for byte apart from rebased times. Complete stored headers/data match an independent interval model. Original allocation, growth, hashing and finalization execute. Old source nodes, world/source objects, input/context/auxiliary buffers and guards remain unchanged; the dispatcher returns the expected new record index and prior wire index.

These are valid finite-value/time fixtures with one-leaf original sources. Other modes, properties, metadata flags, deeper source trees, full producer integration and playback remain unresolved. Memory imports are adapted and thread/mutex callbacks controlled. The four delegates are newly mapped to Animation by the original call chain and connected execution, but remain unnamed and unreviewed pending complete body review. This adds four gray squares, not checked-name credit. Totals remain 654 checked names, with 2,073 mapped functions among 9,603 discovered functions and 7,530 unmapped.


### Scalar basic-to-extended merge and AutoKeyframe metadata

Reviewed all 1,053 original instructions of `MergeScalarAnimationRecordIntervalAsExtended`. It expands retained basic time/value pairs from 8 to 12 bytes, merges incoming extended records, writes a new header and returns its signed index. The saved working signature has five pointers and two byte controls, with the final control passed on the stack. The controls retain neutral names because their original source meanings remain unknown.

9,600 connected original-code cases exercise the actual converter, dispatcher, transition handler and scalar delegate across type codes 2, 5, 24 and 25. Eight profiles cover mode 0, registered AutoKeyframe mode 5, zero/nonzero auxiliary flags and both control flags. In the tested AutoKeyframe cases, nonzero auxiliary flags change the last retained prefix key's metadata to 0x709 only when both controls are clear; either control suppresses the change. When the next old raw time lies within the original tolerance of the first incoming rebased time, the incoming metadata's low 16 bits become 0x700 OR its original low six bits. The comparison is documented as implemented, without assuming identical old/new time origins.

Complete headers/data, values, metadata, rebased times, original world/source objects, source nodes, input/context/auxiliary buffers and guards match independent models. Original allocation, growth, hashing and finalization execute. The name and seven-argument signature persisted after independent reopening and fresh decompilation, preserving all original instruction bytes and all 9,602 other names/signatures. Scope remains finite ordered times/values and one-leaf old sources, with one float property sampled for type 2. Other properties/modes, exhaustive boundary rounding, deeper trees, invalid inputs, concurrency and full producer/playback remain unresolved. Totals are 655 checked names and 2,073 mapped functions among 9,603 discovered functions; 7,530 remain unmapped. Three transition vector delegates and the larger handlers remain unfinished.


### Three-component basic-to-extended recording updates

Reviewed all 1,076 original instructions of `MergeFloat3AnimationRecordIntervalAsExtended` and saved its supported seven-argument signature. It expands retained 16-byte time/three-component keys into 20-byte records, merges incoming extended keys, writes the new header and returns its signed index. The original body includes source-page gap correction, metadata/control conditions and parent-tree seeks. Native checks below cover one-leaf old sources; deeper source traversal remains unverified for this helper.

7,200 connected original-code cases exercise the real converter, dispatcher, transition handler and helper across type codes 3, 7 and 17. Eight mode/auxiliary/control profiles verify ordinary mode 0 and registered AutoKeyframe mode 5. Nonzero auxiliary flags can set the last retained prefix metadata to 0x709 when both controls are clear; either control suppresses that change. The first incoming metadata's low 16 bits are masked to 0x700 OR its original low six bits when the next old raw time meets the original tolerance against the incoming rebased time. Component bits remain unchanged apart from record expansion and time rebasing.

Complete headers/data, original world/source objects, source nodes, input/context/auxiliary buffers and guards match independent models. Resource growth, hashing and finalization execute original code. The descriptive name and seven-argument signature persisted after independent reopening and fresh decompilation, preserving every original instruction byte and all 9,602 other names/signatures. Other modes, exhaustive boundary rounding, deeper trees, invalid inputs, concurrency and full producer/playback remain unresolved. Totals are 656 checked names and 2,073 mapped functions among 9,603 discovered functions, with 7,530 unmapped. Two vector transition delegates and the larger handlers remain unfinished.


### Two-component basic-to-extended recording updates

Reviewed all 1,040 original instructions of `MergeFloat2AnimationRecordIntervalAsExtended` and saved its supported seven-argument signature. It expands retained 12-byte time/two-component keys into 16-byte records, merges incoming extended keys, writes the new header and returns its signed index. The original body includes source-page gap correction, metadata/control conditions and parent-tree seeks. Native checks below cover one-leaf old sources; deeper source traversal remains unverified for this helper.

7,200 connected original-code cases exercise the real converter, dispatcher, transition handler and helper across type codes 8, 20 and 21. Eight mode/auxiliary/control profiles verify ordinary mode 0 and registered AutoKeyframe mode 5. Nonzero auxiliary flags can set the last retained prefix metadata to 0x709 when both controls are clear; either control suppresses that change. The first incoming metadata's low 16 bits are masked to 0x700 OR its original low six bits when the next old raw time meets the original tolerance against the incoming rebased time. Component bits remain unchanged apart from record expansion and time rebasing.

Complete headers/data, original world/source objects, source nodes, input/context/auxiliary buffers and guards match independent models. Resource growth, hashing and finalization execute original code. The descriptive name and seven-argument signature persisted after independent reopening and fresh decompilation, preserving every original instruction byte and all 9,602 other names/signatures. Other modes, exhaustive boundary rounding, deeper trees, invalid inputs, concurrency and full producer/playback remain unresolved. Totals are 657 checked names and 2,073 mapped functions among 9,603 discovered functions, with 7,530 unmapped. One vector transition delegate and the larger handlers remain unfinished.


### Four-component basic-to-extended recording updates

Reviewed all 1,083 original instructions of `MergeFloat4AnimationRecordIntervalAsExtended` and saved its supported seven-argument signature. It expands retained 20-byte time/four-component keys into 24-byte records, merges incoming extended keys, writes the new header and returns its signed index. The original body includes source-page gap correction, metadata/control conditions and parent-tree seeks. Native checks below cover one-leaf old sources; deeper source traversal remains unverified for this helper.

7,200 connected original-code cases exercise the real converter, dispatcher, transition handler and helper across type codes 6, 15 and 16. Eight mode/auxiliary/control profiles verify ordinary mode 0 and registered AutoKeyframe mode 5. Nonzero auxiliary flags can set the last retained prefix metadata to 0x709 when both controls are clear; either control suppresses that change. The first incoming metadata's low 16 bits are masked to 0x700 OR its original low six bits when the next old raw time meets the original tolerance against the incoming rebased time. Component bits remain unchanged apart from record expansion and time rebasing.

Complete headers/data, original world/source objects, source nodes, input/context/auxiliary buffers and guards match independent models. Resource growth, hashing and finalization execute original code. The descriptive name and seven-argument signature persisted after independent reopening and fresh decompilation, preserving every original instruction byte and all 9,602 other names/signatures. Other modes, exhaustive boundary rounding, deeper trees, invalid inputs, concurrency and full producer/playback remain unresolved. Totals are 658 checked names and 2,073 mapped functions among 9,603 discovered functions, with 7,530 unmapped. All four scalar/vector transition delegates now have scoped reviews; the larger handlers remain unfinished.


### Animation transition source-page traversal

14,040 additional connected native-code cases exercise all 13 scalar/vector format routes through the original converter, dispatcher, basic-to-extended handler and four reviewed delegates. Old source counts are one page's record capacity, that capacity plus one, twice that capacity, and twice that capacity plus one. Each runs at offsets zero, one record width, and 504 bytes, across six origin pairs, five incoming time patterns and three mode/control profiles.

The checks cover ordinary mode 0 and AutoKeyframe mode 5 with both controls clear or both set. Scalar and two-component source pages use all 504 payload bytes. Three-component pages hold 496 bytes of complete records and four-component pages hold 500; traversal skips the remaining gaps while preserving logical 504-byte page strides. Exact merged records, metadata, rebased times, complete headers and returned header indices match independent models. Complete source nodes, world data, input/context/auxiliary buffers and guards remain unchanged. Original resource growth, hashing and finalization execute; pow uses a host double-precision adapter, memory imports are adapted, and mutex/thread callbacks are controlled.

This extends the earlier one-leaf checks to one parent level. Deeper trees, exhaustive floating-point rounding, all mode/control combinations, invalid inputs, concurrency and complete producer/playback behavior remain unresolved. No additional function is marked reviewed: the total remains 658 checked names, with 2,073 mapped and 7,530 unmapped functions among 9,603 discovered functions. No Ghidra project changes are made by this test batch.


### Animation transition handler format selection

Audited the original 30-entry signed-relative jump table and the four complete scalar/vector forwarding blocks in the 6,254-instruction basic-to-extended handler. All captured instruction bytes match the original executable. The handler reads the old header's format byte at offset 8. Codes above 29, and unsupported entries within that range, reach the same default return path.

| Old format codes | Selected path | Review scope |
| --- | --- | --- |
| 2, 5, 24, 25 | Scalar interval transition helper | Helper reviewed; connected cases previously published |
| 3, 7, 17 | Three-component interval transition helper | Helper reviewed; connected cases previously published |
| 6, 15, 16 | Four-component interval transition helper | Helper reviewed; connected cases previously published |
| 8, 20, 21 | Two-component interval transition helper | Helper reviewed; connected cases previously published |
| 0 | Inline typed-value records | Full branch review unfinished |
| 1 | Inline Boolean records | Earlier scoped native evidence; full handler review unfinished |
| 4 | Inline transform records | Full transition-branch review unfinished |
| 11 | Inline byte records | Full branch review unfinished |
| 23 | Inline dword records | Full branch review unfinished |
| 29 | Inline qword records | Full branch review unfinished |
| Other byte values | Return sentinel | 5,688 original-code cases in this batch |

The four delegate blocks pass the old header and incoming descriptor through, split the page-root pair into pointers at offsets 0 and 4, restore the auxiliary-state pointer, and forward both byte controls unchanged. This connects the helper signatures to their caller in original assembly; it does not establish source-level names for the controls.

The default-path tests cover all 237 unsupported byte values, six packed-size fixtures and four control pairs. The original handler returns the zero-extended value 0xffffffff and preserves all supplied argument buffers, guards and the synthetic resource-node span. These are direct handler tests, not full producer or gameplay tests. The six inline supported formats are the remaining branch-review gap; neither the whole handler nor another function is marked reviewed. The total remains 658 checked names. No Ghidra project changes are made by this batch.


### Inline dword animation transition branch

Read the format-23 branch of the basic-to-extended handler, including its source-tree setup, prefix retention, incoming writes, metadata controls, suffix selection, data/header finalization and returned header index. This is a branch-level review, not a review of the entire 6,254-instruction handler.

7,680 connected original-code cases now cover this branch: 2,400 ordinary one-leaf fixtures, 2,880 source-page boundary fixtures, and 2,400 additional dword bit-pattern fixtures. Each executes the original converter, dispatcher and inline handler branch. Eight mode/auxiliary/control profiles cover ordinary mode 0 and registered AutoKeyframe mode 5. Source counts of 63, 64, 126 and 127 records at offsets 0, 8 and 504 exercise up to four leaves under one parent level.

Retained 8-byte time/dword keys expand to 12-byte records. Incoming dword bits are copied exactly, with time rebasing and metadata adjustment. The payload checks include zero, signed integer boundaries, all ones, and bit patterns that would represent infinities or NaNs if interpreted as floats; they remain raw dwords. Complete merged data, 72-byte headers, interval boundaries for the scoped time patterns and returned indices match independent models. The AutoKeyframe prefix and first-incoming metadata rules match the previously reviewed scalar/vector paths. Complete source nodes, world data, argument buffers and guards remain unchanged.

Resource allocation, growth, hashing and finalization execute original code. Host memory and double-precision pow adapters and controlled mutex/thread callbacks remain explicit harness boundaries. Deeper source trees, exhaustive time rounding, invalid inputs, concurrency and full producer/playback behavior remain unresolved. The five other inline format branches still need complete review, so the whole handler remains unnamed and unreviewed. No new function credit is added; the total remains 658 checked names.


### Inline qword animation transition branch

Read the format-29 setup, prefix/incoming/suffix merge paths, resource finalization, header append and index return. Original assembly confirms the meaningful retained-record stores: a four-byte time, an eight-byte qword value, and four metadata bytes. Retained 16-byte keys expand to 24-byte records. Alignment padding at offsets 4–7 and 20–23 is opaque temporary state; this review does not promise that retained output padding is zero or copied from the old key.

8,160 connected original-code cases exercise the converter, dispatcher and inline qword branch across eight mode/auxiliary/control profiles. The 2,400 one-leaf cases include zero, signed boundaries, all ones, high-bit payloads and floating-point-like 64-bit patterns interpreted strictly as qwords. Another 5,760 cases use 31, 32, 62 and 63 old records at offsets 0, 16 and 504. Source pages hold 496 bytes of complete records with an eight-byte gap under the logical 504-byte stride, across up to four leaves under one parent level.

Exact time/value/metadata fields, merged lengths, complete 72-byte headers and returned header indices match independent models. The page-crossing fixtures seed incoming padding after conversion with distinct per-record values and verify the handler copies those bytes unchanged. Retained output padding is deliberately excluded from equality assertions; no claim of complete byte-for-byte equality for those records is made. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged. AutoKeyframe metadata and interval selection match the reviewed dword/scalar/vector rules in the tested scope.

Resource operations execute original code; memory imports and double-precision pow use host adapters, while mutex/thread callbacks are controlled. Deeper source trees, exhaustive rounding, invalid inputs, concurrency and full producer/playback remain unresolved. Four other inline format branches still need full review. The whole handler remains unnamed and unreviewed, and the total stays at 658 checked names. This batch changes no Ghidra project data.


### Inline byte animation transition branch

Read the format-11 source setup, prefix/incoming/suffix paths, resource finalization, header append and index return. Original assembly confirms that retained keys load and store only the one-byte value at offset 4, alongside the four-byte time and four metadata bytes. Old 8-byte keys expand to 12-byte records. Bytes 5–7 are opaque padding; this review makes no zeroing or preservation promise for those bytes in retained output records.

5,280 connected original-code cases execute the converter, dispatcher and inline byte branch across eight mode/auxiliary/control profiles: 2,400 one-leaf fixtures and 2,880 source-page fixtures. The latter cover 63, 64, 126 and 127 old keys at offsets 0, 8 and 504, across up to four leaves under one parent level. Scoped payloads include 0, 1, 0x7f, 0x80, 0xfe, 0xff, 0x55 and 0xaa. Exact times, byte values, metadata, merged lengths, complete headers and returned indices match independent models. Interval selection and AutoKeyframe metadata agree with the reviewed dword/scalar/vector paths in this tested scope.

Incoming padding is seeded after conversion with per-record values and preserved by the handler. Equality assertions exclude retained-record padding; complete byte-for-byte equality is not claimed for those records. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged. Original resource operations execute with host memory adapters, a host double-precision pow adapter for parent traversal, and controlled mutex/thread callbacks.

Deeper source trees, exhaustive time rounding, invalid inputs, concurrency and full producer/playback remain unresolved. Typed-value, Boolean and transform inline branches still require full review. The whole handler remains unnamed and unreviewed; the count remains 658 checked names. This batch makes no Ghidra project changes.


### Inline Boolean animation transition branch

Completed the format-1 branch read, including source setup, prefix retention, incoming metadata, suffix selection, resource finalization, header append and returned index. Original instructions in both retained-prefix and retained-suffix paths load the stored value byte and explicitly AND it with 1 before writing the extended value. This is low-bit extraction, not nonzero-to-true normalization. Noncanonical fixture bytes such as 0x80 therefore yield a retained value of 0, while 0x7f yields 1; this describes record processing, not a claim about normal user-facing Boolean values.

5,280 connected original-code cases execute the converter, dispatcher and Boolean transition branch across eight mode/auxiliary/control profiles. The 2,400 one-leaf cases supplement the earlier Boolean evidence with varied byte patterns and seeded incoming padding. Another 2,880 cases exercise 63, 64, 126 and 127 old records at offsets 0, 8 and 504, across up to four source leaves under one parent level. Ordinary mode 0 and registered AutoKeyframe mode 5 match the scoped interval and metadata models, including both byte controls.

Old 8-byte records expand to 12-byte records. Exact time, extracted low-bit value, metadata, merged lengths, complete headers and returned indices match independent models. Incoming records supplied by the converter retain their value and seeded padding while time and the scoped first-record metadata may change. Padding bytes 5–7 in retained records remain opaque and excluded from equality assertions. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged.

Original resource operations execute with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Deeper source trees, exhaustive rounding, invalid inputs, concurrency and complete producer/playback remain unresolved. Typed-value and transform branches still require full review. The whole handler remains unnamed and unreviewed, with no extra function credit; the total remains 658 checked names. No Ghidra project data changes in this batch.


### Inline typed-value animation transition branch

Read the format-0 branch through prefix/incoming/suffix selection, source-page traversal, data/header finalization and returned header index. Basic 48-byte keys expand to 56-byte records. Original assembly confirms the retained value copy covers 37 bytes at offsets 8–44 using overlapping 32-byte and eight-byte loads/stores, while metadata is written at offset 48. Incoming records are copied in full before time rebasing and the scoped first-record metadata adjustment.

15,840 connected original-code cases exercise the actual converter, typed-value comparator, dispatcher and inline transition branch. The 7,200 one-leaf cases cover value tags 1, 9 and 30 across eight mode/auxiliary/control profiles. The 8,640 source-page cases use 10, 11, 20 and 21 old records at offsets 0, 48 and 504. Full source-record pages use 480 of 504 payload bytes; the reader skips 24-byte gaps while preserving logical page strides, across up to four leaves under one parent level. Fixtures vary the common float field to keep converter inputs distinct; this batch does not repeat exhaustive type-dependent equality coverage from the earlier comparator/converter studies.

Exact times, value bytes 8–44, metadata bytes 48–51, merged lengths, complete 72-byte headers and returned indices match independent models. Incoming padding at offsets 4–7, 45–47 and 52–55 is seeded after conversion and preserved by the handler. Retained-record padding is opaque and excluded from equality assertions, so complete byte-for-byte equality is not claimed for those records. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged. Ordinary mode 0 and registered AutoKeyframe mode 5 match the scoped interval and metadata models.

Resource operations execute original code with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Other value tags in the connected transition path, deeper trees, exhaustive rounding, invalid inputs, concurrency and full producer/playback remain unresolved. The transform inline branch is still unfinished, so the whole handler remains unnamed and unreviewed. No function credit is added; the total stays at 658 checked names. This batch makes no Ghidra project changes.


### Basic-to-extended animation handler reviewed and named

Completed the remaining transform branch and the full 6,254-instruction handler review. Saved the descriptive name `MergeAnimationRecordIntervalAsExtended` and its eight-argument working signature: old header, incoming descriptor, two transform frames, page-root pair, auxiliary state and two byte controls, returning a signed 32-bit record index. Independent reopening and fresh decompilation confirm persistence; all original instruction bytes and all 9,602 other function names/signatures remain unchanged.

The handler selects 19 format codes through the original jump table. Four reviewed delegates handle scalar/vector groups; six inline branches handle typed-value, Boolean, transform, byte, dword and qword records. Scoped tests cover interval retention, origin rebasing, extended metadata, resource/header updates and the unsupported-format sentinel. The recorded suites total 96,048 native executions across overlapping fixture families; this is neither a unique-input count nor whole-game verification.

The new transform suite contributes 2,880 original converter-plus-handler cases using eight fresh frame profiles and three mode/control profiles. It verifies 36-byte old keys become 40-byte records; retained transforms stay in stored coordinates, while incoming transforms follow `inverse(H) * D * K * O * inverse(W)`. H is the stored header frame, D the incoming descriptor frame, K the incoming key, and W/O the two supplied frames. Finite unit quaternions and positive uniform scales 0.5, 1 and 2 produce a maximum measured error of about 0.0000147, below the fixed 0.0005 tolerance. Time, metadata, complete headers, retained-key bytes and guards are checked exactly. This transform suite calls the original handler directly after conversion; dispatcher coverage comes from the separately recorded format suites.

The name describes the reviewed role, with explicit limits: transform source traversal is one-leaf only, other tested formats reach one parent level, and typed-value transition fixtures cover tags 1, 9 and 30. Opaque retained-record padding remains outside equality claims. Other modes, exhaustive rounding, deeper trees, singular/negative scales, nonunit/nonfinite rotations, invalid inputs, concurrency and full producer/playback remain unresolved. Host adapters and controlled callbacks remain documented. The basic and already-extended large update handlers still need full reviews. Totals are 659 checked names and 2,073 mapped functions among 9,603 discovered functions, with 7,530 unmapped.


### Already-extended scalar animation interval updates

Reviewed all 1,081 original instructions of `MergeExtendedScalarAnimationRecordInterval` and saved its seven-argument working signature with a signed 32-bit index return. This helper merges records that are already extended: old and incoming records are both 12 bytes. Unlike the basic-to-extended path, retained metadata is preserved except for explicit AutoKeyframe field adjustments.

19,200 connected native-code cases execute the actual converter, dispatcher, already-extended handler and scalar helper across format codes 2, 5, 24 and 25. Eight mode/auxiliary/control profiles and four old metadata patterns exercise zero/nonzero low-three-bit fields, different low nibbles and varying upper 16 bits. Complete headers and data, rebased times, values, metadata, returned indices, source nodes, world data, argument buffers and guards match independent models.

For the last retained prefix key in AutoKeyframe mode, a clear second control allows metadata changes. With nonzero auxiliary flags and a clear first control, a zero low-three-bit field gets low nibble 9; a nonzero low-three-bit field stays unchanged. Otherwise the low nibble is cleared. For a sufficiently close next old raw time and first incoming rebased time, the incoming low 16 metadata bits combine the next old high ten bits with selected low bits; nonzero auxiliary flags and a nonzero old low-three-bit field select the old low nibble plus incoming bits 4–5. Upper 16 bits remain those of their source record. These are scoped observed bit rules, not recovered source-level flag names.

Independent reopening and fresh decompilation confirm the name and signature persisted; original bytes and all 9,602 other names/signatures remain unchanged. Tests use one-leaf old sources, finite ordered times, valid buffers and four metadata patterns. Deeper source trees, exhaustive rounding, other modes/properties, invalid inputs, races and full producer/playback remain unresolved. Host memory adapters and controlled mutex/thread callbacks remain explicit. The larger already-extended handler and three vector delegates still need full reviews. Totals are 660 checked names, 2,074 mapped functions and 7,529 unmapped functions among 9,603 discovered functions.


### Already-extended float3 animation interval updates

Reviewed all 1,086 original instructions of `MergeExtendedFloat3AnimationRecordInterval` and saved its seven-argument working signature with a signed 32-bit index return. This helper merges records that are already extended: old and incoming records are both 20 bytes. Unlike the basic-to-extended path, retained metadata is preserved except for explicit AutoKeyframe field adjustments.

14,400 connected native-code cases execute the actual converter, dispatcher, already-extended handler and float3 helper across format codes 3, 7 and 17. Eight mode/auxiliary/control profiles and four old metadata patterns exercise zero/nonzero low-three-bit fields, different low nibbles and varying upper 16 bits. Complete headers and data, rebased times, values, metadata, returned indices, source nodes, world data, argument buffers and guards match independent models.

For the last retained prefix key in AutoKeyframe mode, a clear second control allows metadata changes. With nonzero auxiliary flags and a clear first control, a zero low-three-bit field gets low nibble 9; a nonzero low-three-bit field stays unchanged. Otherwise the low nibble is cleared. For a sufficiently close next old raw time and first incoming rebased time, the incoming low 16 metadata bits combine the next old high ten bits with selected low bits; nonzero auxiliary flags and a nonzero old low-three-bit field select the old low nibble plus incoming bits 4â€“5. Upper 16 bits remain those of their source record. These are scoped observed bit rules, not recovered source-level flag names.

Independent reopening and fresh decompilation confirm the name and signature persisted; original bytes and all 9,602 other names/signatures remain unchanged. Tests use one-leaf old sources, finite ordered times, valid buffers and four metadata patterns. Deeper source trees, exhaustive rounding, other modes/properties, invalid inputs, races and full producer/playback remain unresolved. Host memory adapters and controlled mutex/thread callbacks remain explicit. The larger already-extended handler and two vector delegates still need full reviews. Totals are 661 checked names, 2,075 mapped functions and 7,528 unmapped functions among 9,603 discovered functions.


### Already-extended float4 animation interval updates

Reviewed all 1,084 original instructions of `MergeExtendedFloat4AnimationRecordInterval` and saved its seven-argument working signature with a signed 32-bit index return. This helper merges records that are already extended: old and incoming records are both 24 bytes. Unlike the basic-to-extended path, retained metadata is preserved except for explicit AutoKeyframe field adjustments.

14,400 connected native-code cases execute the actual converter, dispatcher, already-extended handler and float4 helper across format codes 6, 15 and 16. Eight mode/auxiliary/control profiles and four old metadata patterns exercise zero/nonzero low-three-bit fields, different low nibbles and varying upper 16 bits. Complete headers and data, rebased times, values, metadata, returned indices, source nodes, world data, argument buffers and guards match independent models.

For the last retained prefix key in AutoKeyframe mode, a clear second control allows metadata changes. With nonzero auxiliary flags and a clear first control, a zero low-three-bit field gets low nibble 9; a nonzero low-three-bit field stays unchanged. Otherwise the low nibble is cleared. For a sufficiently close next old raw time and first incoming rebased time, the incoming low 16 metadata bits combine the next old high ten bits with selected low bits; nonzero auxiliary flags and a nonzero old low-three-bit field select the old low nibble plus incoming bits 4Ã¢â‚¬â€œ5. Upper 16 bits remain those of their source record. These are scoped observed bit rules, not recovered source-level flag names.

Independent reopening and fresh decompilation confirm the name and signature persisted; original bytes and all 9,602 other names/signatures remain unchanged. Tests use one-leaf old sources, finite ordered times, valid buffers and four metadata patterns. Deeper source trees, exhaustive rounding, other modes/properties, invalid inputs, races and full producer/playback remain unresolved. Host memory adapters and controlled mutex/thread callbacks remain explicit. The larger already-extended handler and one vector delegate still need full reviews. Totals are 662 checked names, 2,076 mapped functions and 7,527 unmapped functions among 9,603 discovered functions.


### Already-extended float2 animation interval updates

Reviewed all 1,077 original instructions of `MergeExtendedFloat2AnimationRecordInterval` and saved its seven-argument working signature with a signed 32-bit index return. This helper merges records that are already extended: old and incoming records are both 16 bytes. Unlike the basic-to-extended path, retained metadata is preserved except for explicit AutoKeyframe field adjustments.

14,400 connected native-code cases execute the actual converter, dispatcher, already-extended handler and float2 helper across format codes 8, 20 and 21. Eight mode/auxiliary/control profiles and four old metadata patterns exercise zero/nonzero low-three-bit fields, different low nibbles and varying upper 16 bits. Complete headers and data, rebased times, values, metadata, returned indices, source nodes, world data, argument buffers and guards match independent models.

For the last retained prefix key in AutoKeyframe mode, a clear second control allows metadata changes. With nonzero auxiliary flags and a clear first control, a zero low-three-bit field gets low nibble 9; a nonzero low-three-bit field stays unchanged. Otherwise the low nibble is cleared. For a sufficiently close next old raw time and first incoming rebased time, the incoming low 16 metadata bits combine the next old high ten bits with selected low bits; nonzero auxiliary flags and a nonzero old low-three-bit field select the old low nibble plus incoming bits 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5. Upper 16 bits remain those of their source record. These are scoped observed bit rules, not recovered source-level flag names.

Independent reopening and fresh decompilation confirm the name and signature persisted; original bytes and all 9,602 other names/signatures remain unchanged. Tests use one-leaf old sources, finite ordered times, valid buffers and four metadata patterns. Deeper source trees, exhaustive rounding, other modes/properties, invalid inputs, races and full producer/playback remain unresolved. Host memory adapters and controlled mutex/thread callbacks remain explicit. All four scalar/vector delegates now have scoped reviews; the larger already-extended handler still needs a full review. Totals are 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions.


### Already-extended animation source-page traversal

14,040 additional connected original-code cases cover all 13 scalar/vector routes through the converter, dispatcher, already-extended handler and four reviewed delegates. Each format uses old counts of one page's record capacity, that capacity plus one, twice that capacity, and twice that capacity plus one. Record starts at offsets zero, one extended-record width, and 504 bytes exercise up to four leaves under one parent level. Six origin pairs, five incoming time patterns and three mode/control profiles cover ordinary mode 0 and AutoKeyframe mode 5 with both controls clear or both set.

Old metadata patterns alternate between records and vary low nibbles, low-three-bit fields and upper 16 bits. Complete merged data and 72-byte headers, logical offsets, rebased times, metadata and returned indices match independent models. Twelve-byte scalar and 24-byte four-component records fill all 504 payload bytes per full source page. Twenty-byte three-component records use 500 bytes with a four-byte gap; 16-byte two-component records use 496 bytes with an eight-byte gap. The reader skips gaps while retaining logical 504-byte strides, and new headers use logical extents rather than flattened byte counts.

Complete original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged. Original resource growth, hashing and finalization execute; memory and double-precision pow imports use host adapters, while mutex/thread callbacks are controlled. This extends the earlier one-leaf evidence to one parent level. Deeper trees, exhaustive rounding, other mode/control combinations, invalid inputs, concurrency and full producer/playback remain unresolved.

No new function credit is added: totals remain 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions. The larger already-extended handler still needs a complete branch review. This batch makes no Ghidra project changes.


### Inline already-extended dword updates

Read the format-23 branch of the already-extended handler through source setup, prefix/incoming/suffix handling, resource finalization, header append and returned index. Old, incoming and output records are all 12 bytes. Retained dword values and metadata are copied directly except for time rebasing and the scoped AutoKeyframe metadata adjustments.

5,880 connected original-code cases execute the converter, dispatcher and this inline branch. The 4,800 one-leaf cases cover eight mode/auxiliary/control profiles and four old metadata patterns. The 1,080 page-crossing cases cover 42, 43, 84 and 85 old keys at offsets 0, 12 and 504, with interleaved metadata under three mode/control profiles. Full pages hold 504 bytes of complete records; the tested source trees reach one parent level and up to four leaves.

Payload fixtures include zero, signed boundaries, all ones, and NaN-like/infinity-like dword patterns; values remain raw bits. Complete headers and merged data, logical offsets, rebased times, metadata and returned indices match independent models. The AutoKeyframe prefix low-nibble rule and first-incoming transfer of next-old metadata fields match the reviewed scalar/vector delegates. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged.

Original resource operations execute with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Deeper trees, exhaustive rounding, other modes/flags, invalid inputs, concurrency and full producer/playback remain unresolved. The five other inline branches still need complete reviews, so the whole handler remains unnamed and unreviewed. No function credit is added; totals remain 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions. No Ghidra project data changes in this batch.


### Inline already-extended byte updates

Read the format-11 branch through source setup, prefix/incoming/suffix handling, resource finalization, header append and returned index. Already-extended byte records remain 12 bytes. The retained-key path copies the stored first eight bytes, including the value byte at offset 4 and padding at offsets 5–7, followed by metadata at offset 8. This differs from basic-to-extended byte conversion, whose retained output padding was deliberately left outside equality claims.

5,880 connected original-code cases execute the actual converter, dispatcher and inline byte branch. The 4,800 one-leaf cases use eight mode/auxiliary/control profiles and four old metadata patterns. The 1,080 source-page cases use 42, 43, 84 and 85 old keys at offsets 0, 12 and 504, with interleaved metadata and three mode/control profiles. Full source pages use all 504 payload bytes; tested trees reach one parent level and up to four leaves.

Old value/padding patterns vary together, with byte values including 0, 1, 0x7f, 0x80, 0xfe, 0xff, 0x55 and 0xaa. Incoming padding is seeded after conversion with distinct per-record values. Complete merged data equality confirms both retained and incoming padding are preserved, apart from the explicitly modeled time and metadata fields. Complete headers, logical offsets, rebased times, metadata and returned indices match independent models. AutoKeyframe adjustments match the reviewed extended dword/scalar/vector rules. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged.

Original resource operations execute with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Deeper trees, exhaustive rounding, other modes/flags, invalid inputs, concurrency and full producer/playback remain unresolved. Typed-value, Boolean, transform and qword inline branches still need complete review. The whole handler remains unnamed and unreviewed; totals stay at 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions. No Ghidra project data changes in this batch.


### Inline already-extended Boolean updates

Read the format-1 branch through source setup, prefix/incoming/suffix handling, resource finalization, header append and returned index. Already-extended Boolean records remain 12 bytes. Retained records copy the stored value byte and padding bytes 5–7 unchanged; this branch does not repeat the low-bit extraction performed when converting basic Boolean records into extended records.

5,880 connected original-code cases execute the actual converter, dispatcher and inline Boolean branch. The 4,800 one-leaf cases use eight mode/auxiliary/control profiles and four old metadata patterns. Another 1,080 source-page cases cover 42, 43, 84 and 85 old keys at offsets 0, 12 and 504, with interleaved metadata and three mode/control profiles. Tested source trees reach one parent level and up to four leaves.

Noncanonical old fixture bytes such as 0x7f, 0x80, 0xfe and 0xff remain unchanged when retained; this describes the handler's copy behavior and does not establish that normal gameplay stores those representations. Incoming values generated by the Boolean converter are checked against the input low bit. Incoming padding is seeded after conversion with distinct per-record values. Complete merged records, including retained/incoming padding, headers, logical offsets, rebased times, metadata and returned indices match independent models. AutoKeyframe field adjustments match the reviewed already-extended byte/dword/scalar/vector paths. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged.

Original resource operations execute with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Deeper trees, exhaustive rounding, other modes/flags, invalid inputs, concurrency and full producer/playback remain unresolved. Typed-value, transform and qword inline branches still need complete review. The whole handler remains unnamed and unreviewed; totals stay at 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions. No Ghidra project data changes in this batch.


### Inline already-extended qword updates

Read the format-29 branch through source setup, prefix/incoming/suffix handling, resource finalization, header append and returned index. Already-extended qword records remain 24 bytes. The branch copies the full stored record before time rebasing and the scoped metadata adjustments, preserving the eight-byte value and padding at offsets 4–7 and 20–23. This differs from basic-to-extended qword conversion, whose retained padding remained outside equality claims.

5,880 connected original-code cases execute the actual converter, dispatcher and inline qword branch. The 4,800 one-leaf cases use eight mode/auxiliary/control profiles and four old metadata patterns. Another 1,080 source-page cases use 21, 22, 42 and 43 old records at offsets 0, 24 and 504, with interleaved metadata and three mode/control profiles. Full pages hold all 504 payload bytes; tested trees reach one parent level and up to four leaves.

Qword fixtures include zero, signed 64-bit boundaries, all ones, high-bit patterns and representations that would be NaN-like or infinity-like if interpreted as doubles; values remain raw bits. Old padding is explicit and incoming padding is seeded after conversion with distinct per-record values. Complete merged records, headers, logical offsets, rebased times, metadata and returned indices match independent models. AutoKeyframe field adjustments match the reviewed already-extended Boolean/byte/dword/scalar/vector paths. Original stored data, source nodes, world state, input/context/auxiliary buffers and guards remain unchanged.

Original resource operations execute with host memory adapters, host double-precision pow for parent traversal, and controlled mutex/thread callbacks. Deeper trees, exhaustive rounding, other modes/flags, invalid inputs, concurrency and full producer/playback remain unresolved. Typed-value and transform inline branches still require complete review. The whole handler remains unnamed and unreviewed; totals stay at 663 checked names, 2,077 mapped functions and 7,526 unmapped functions among 9,603 discovered functions. No Ghidra project data changes in this batch.


### Already-extended typed animation values

Read the format-0 merge branch and its shared tail in `14107ea70`. Original converter, typed-value comparator, dispatcher, and inline updater passed 17,640 cases against an independent interval/metadata model: 14,400 one-leaf cases and 3,240 cases with one parent level.

The branch merges 56-byte records. Checks compare every output byte, including typed values, rebased times, metadata, and padding at bytes 4–7, 45–47, and 52–55. Retained records preserve those padding bytes; incoming padding was seeded after conversion. Complete headers, old data, source nodes, descriptor guards, and world/context preservation were also checked.

Coverage is limited to typed-value tags 1, 9, and 30, finite ordered times, valid buffers, and the documented mode/control profiles. Parent fixtures use 9/10/18/19 old keys and offsets 0/56/504. Memory, threading, and the parent-seek `pow` import use controlled host adapters. This does not establish deeper-tree, malformed-input, race, exhaustive rounding, producer, or playback behavior.

No new function name or completion credit: 663 checked names remains unchanged. The containing handler is still unfinished; its inline transform branch remains to be reviewed.


### Already-extended animation transforms

Read the format-4 branch and its shared tail in `14107ea70`. Original converter and direct original updater passed 11,520 cases: 2,880 one-leaf cases and 8,640 cases with one parent level. This batch does not execute the dispatcher.

Old and incoming keys are 40-byte extended records. Retained transforms stay in their stored coordinates. Incoming transforms match `inverse(H) * D * K * O * inverse(W)`, where H is the old header frame, D the incoming descriptor frame, K the key transform, O the output frame, and W the wire frame. Eight fresh frame profiles use finite unit quaternions and positive uniform scales 0.5/1/2. Maximum absolute error was 0.00001465 against tolerance 0.0005, allowing equivalent quaternion signs.

Checks cover exact times, metadata, complete headers, retained transform bytes, old data, source nodes, descriptor guards, and context preservation. Parent fixtures use 12/13/24/25 old keys at offsets 0/40/504, including the 24-byte logical gaps after 480-byte record pages. The original byte-verified libc infinity check executes; memory/thread boundaries and the parent-seek pow import use controlled host adapters.

No additional checked name or completion credit. All six inline formats now have scoped review evidence, but the whole handler still needs its entry dispatch, delegated routes, and unsupported-format exits audited. Deeper trees, other mode/control combinations, singular/negative scales, nonunit/nonfinite rotations, malformed inputs, races, full producer behavior, and playback remain unverified.


### Already-extended animation handler reviewed and named

Completed the 6,366-instruction body review and saved `MergeExtendedAnimationRecordInterval` with a working eight-argument signature and signed 32-bit index return. Independent reopening and fresh decompilation confirm persistence. Original bytes and all 9,602 other names/signatures are unchanged.

The original table selects 19 formats: four scalar/vector delegate groups and six inline branches (typed value, Boolean, transform, byte, dword, qword). All 237 unsupported byte values returned the invalid-index sentinel across six size fixtures and four control pairs without changing test arguments or resource nodes. Assembly confirms both byte controls are forwarded unchanged to the delegates.

Recorded suites total 134,808 scoped native executions, including overlapping fixture families. They cover interval retention, time-origin rebasing, recording metadata, retained record preservation, resource/header updates and one-parent traversal. Transform coverage contributes 11,520 direct converter-plus-handler cases; maximum coordinate-composition error was about 0.00001465 under tolerance 0.0005. Those transform batches do not execute the dispatcher. Connected typed-value fixtures cover tags 1, 9 and 30.

This is one reviewed function, not whole-game completion. Other modes, exhaustive rounding, deeper trees, malformed inputs, concurrency, singular/negative scales, nonunit/nonfinite rotations and full producer/playback behavior remain unresolved. Controlled host adapters remain documented. Totals: 664 checked names, 2,077 mapped functions among 9,603 discovered functions, and 7,526 still unmapped. The large basic-record updater still needs full review.


### Basic animation updater: dword pages and dispatch

Read the basic dword format-23 branch and its shared retention/header/index tail in `141077240`. A new 720-case direct-original-handler suite checks 63/64/126/127 old keys at offsets 0/8/504, crossing one parent level. The 8-byte records preserve every dword value bit, including signed boundaries and NaN-like bit patterns, while rebasing times and replacing the incoming interval. Complete headers/data, retained keys, source nodes, argument buffers and guards match the independent model. This suite uses finite ordered times, descriptor flag 0 and auxiliary mode 0; it does not execute converter or dispatcher. Parent seeks use the documented controlled host pow adapter.

The original table at `1416d5000` selects 19 formats through four scalar/vector delegate groups and six inline branches. Another 1,422 direct original-code cases cover all 237 unsupported byte values across six packed sizes. Each returned the zero-extended invalid-index sentinel without changing arguments, guards or resource nodes.

These are scoped additions to the earlier basic-merge evidence, not a whole-handler review. Mixed basic/extended input flags and their mode-specific paths still require separate validation. Other modes, exhaustive rounding, deeper trees, malformed inputs, races and full producer/playback behavior remain unresolved. No new name credit: 664 checked names remains unchanged; the basic updater is still unnamed.


### Basic animation updater: qword record preservation

Read the format-29 branch and its shared retention/header/index tail in `141077240`. A new 720-case direct-original-handler suite checks 31/32/62/63 old keys at offsets 0/16/504, crossing one parent level and the 8-byte logical gaps after 496-byte record pages.

The 16-byte keys contain a time, four padding bytes, and a qword value. Complete-byte comparisons preserve distinct old/incoming padding and all 64 value bits, including signed boundaries and NaN-like bit patterns. The independent interval model also matches rebased times, complete headers/data, returned index and retained records; source nodes, arguments, context and guards remain unchanged.

This batch uses finite ordered times, descriptor flag 0 and auxiliary mode 0, with controlled host memory/thread callbacks and the documented double-precision pow adapter. Converter and dispatcher are not executed in this batch. Mixed basic/extended flags, other modes, exhaustive rounding, deeper trees, malformed inputs, races and full producer/playback behavior remain unresolved. The whole basic updater remains unfinished and unnamed; checked names remain 664.


### Basic animation updater: byte and Boolean records

Read both inline branches and their shared retention/header/index tails in `141077240`. New direct-original-handler suites passed 720 cases per branch, checking 63/64/126/127 old keys at offsets 0/8/504 across one parent level. Independent models match exact complete headers/data, rebased times, returned index, retained records, source nodes, argument/context preservation and guards.

In ordinary descriptor-flag-0/auxiliary-mode-0 merging, both formats copy complete 8-byte records except for time rebasing. The value byte at offset 4 and padding at 5–7 remain intact. Boolean bytes other than 0 and 1 are preserved in this scope. Static review identifies low-bit normalization in particular AutoKeyframe/extended-input paths; those paths are not established by these ordinary-merge checks. The input width table changes from 8 to 12 bytes when the extended flag is set, so mixed-input behavior still needs separate tracing rather than assuming the ordinary record model applies.

These batches call the original handler directly; they do not execute converter or dispatcher. Host memory/thread callbacks and the double-precision parent-seek pow adapter remain controlled boundaries. Other mode/flag combinations, deeper trees, exhaustive rounding, malformed inputs, races and full producer/playback behavior remain unresolved. No new checked-function credit: the whole basic updater remains unfinished and unnamed; total checked names remains 664.


### Basic animation updater: typed-value record copying

Read the format-0 branch and its shared retention/header/index tail in `141077240`. A new direct-original-handler suite passed 23,040 cases across tags 0–30 and 255. Fixtures use 10/11/20/21 old keys at offsets 0/48/504, including one parent level and the 24-byte logical gaps after 480-byte record pages.

In ordinary descriptor-flag-0/auxiliary-mode-0 merging, the branch treats each 48-byte record as stored bytes: it preserves value bytes 8–44, tag byte 44, and padding 4–7/45–47 while rebasing time. Unknown-tag preservation does not establish that the tag is valid or that its payload has been semantically decoded. Complete headers/data, returned index, retained records, source nodes, arguments, context and guards match the independent interval model.

The batch calls the original handler directly without converter or dispatcher. Controlled host memory/thread callbacks and the double-precision parent-seek pow adapter remain explicit boundaries. Mixed basic/extended flags and their AutoKeyframe-specific value handling remain unresolved, alongside other modes, exhaustive rounding, deeper trees, malformed inputs, races and full producer/playback behavior. The basic updater is still unfinished and unnamed; checked names remains 664.


### Basic animation interval updater reviewed and named

Saved the descriptive name `MergeBasicAnimationRecordInterval` after reading its complete 6,588-instruction body. Its working signature takes the old header, incoming descriptor, wire/output frames, page roots and auxiliary state, returning a signed 32-bit index. Independent reopening and fresh decompilation verify persistence; original instruction bytes and all 9,602 other names/signatures remain unchanged.

The function selects 19 formats through the original table: four scalar/vector delegate groups and six inline branches. Recorded suites total 36,582 scoped native executions, including overlapping fixture families. Ordinary flag-0/mode-0 checks cover interval retention, time rebasing, full record preservation and one-parent source traversal. Unsupported-format checks cover all 237 unsupported bytes. This is a descriptive-role review with explicitly bounded execution evidence.

The new transform suites contribute 3,840 original converter-plus-handler cases, including 14/15/28/29 old keys at offsets 0/36/504. Basic keys remain 36 bytes. Retained transforms stay in stored coordinates; incoming transforms match `inverse(H) * D * K * O * inverse(W)` across eight fresh frame profiles. Maximum error was about 0.00001465 under tolerance 0.0005, allowing equivalent quaternion signs. Time, headers, retained bytes, source nodes and guards are checked exactly. These transform batches call the original handler directly after conversion, without dispatcher execution. Unit quaternions and positive uniform scales 0.5/1/2 bound this math evidence.

Mixed basic/extended input flags and AutoKeyframe-specific normalization/value rewriting remain statically identified but not dynamically established. Typed-value checks establish opaque copying, not semantic decoding. Other modes, exhaustive rounding, deeper trees, malformed inputs, nonfinite/singular transforms, concurrency and full producer/playback behavior remain unresolved; controlled host boundaries remain documented.

Totals: 665 checked names, 2,077 mapped functions among 9,603 discovered, with 7,526 unmapped. All three interval updaters now have descriptive names; this does not establish complete recording, playback or whole-game reverse engineering.


### Recording producer: derived format and override selection

Traced the fresh-lookup selection path in producer `1407af650` through converter setup, descriptor construction and insertion-wrapper forwarding. Original bytes were checked for 163 producer instructions plus the wrapper call window. A separate native bridge executes only the original straight-line selection block: all 256 record-mode bytes paired with inherited selection 0/1 passed 512 cases.

When the looked-up stored record is basic, both derived choices equal `(recordMode == AutoKeyframe) OR inheritedSelection`: one choice requests extended converter output, while the other requests the basic-to-extended transition handler. For an already-extended stored record, the inspected branch chooses extended output with override 0; the dispatcher selects the extended updater from the stored header flag. Assembly ties the converter choice to the first stack argument and the descriptor's derived bit 4, then traces the saved override byte through the insertion call to the dispatcher.

This is a partial caller-contract result, not proof that mixed-input basic paths are unreachable. Descriptor flags also inherit a separate base byte whose possible bit 4 still needs tracing; the duplicate-key path also needs review. Only the small selection block ran in this batch, not the full producer, insertion wrapper, converter or dispatcher. No function name or completion credit was added; checked names remains 665.


### Recording producer: duplicate shortcut and inherited flag boundary

Original duplicate-selection and processed-bitmap instruction fragments passed 514 scoped native checks: two inherited-choice cases and 512 bitmap fixtures covering indices 0–127. The shortcut clears override while retaining the inherited extended choice. The following bitmap calculation selects the indexed bit; the enclosing conditional jump skips processing when it is set. These fragment checks do not prove that every duplicate group has already set that bit.

An original executable search for the inherited flag displacement was validated against saved Ghidra instruction boundaries, excluding overlapping false decodes. Five true sites remain: two address computations in the recording producer and three reads/tests in `140a0baa0`. No direct writer was found by this exact-displacement search. That does not exclude indirect or wider stores, and the byte's possible extended-format bit remains unresolved.

The second owner has 46,227 saved instructions; decompilation did not complete within 60 seconds. Only local instruction windows were inspected, so no whole-owner role or name is claimed. Full producer execution, complete duplicate-group dataflow, inherited-flag origin and mixed-input reachability remain open. Checked names remains 665; no new name or completion credit was added.


### All-zero key filter: expanded selector coverage

The saved helper `ClearAllZeroAnimationInputForSelectedProperties` was already reviewed and named. New direct original-code checks expand its property-selector coverage across all 65,536 ushort values, using all-zero and nonzero three-key buffers: 131,072 selector cases. Another 770 fixtures cover the 14 selected properties, empty and 1/2/3/7-record buffers, signed zero, NaNs, infinities, byte values and nonzero positions. The new batch totals 131,842 scoped executions; it overlaps earlier evidence and adds no name credit.

The selected groups are float2 properties 184/185/202, scalar-float properties 188/197, and byte properties 186/187/198/199/200/201/961/962/999. Their buffers are logically cleared by setting length to zero only when every examined value is zero. Other selectors leave the descriptor unchanged. Float comparisons accept both signed zeros and retain NaNs/infinities; byte comparisons inspect only the low byte. Complete pointer/capacity/guards and payload bytes remain unchanged. Return-register contents are not interpreted because the producer ignores them. This batch does not execute the whole producer or converter chain; malformed lengths, huge counts, invalid pointers and concurrency remain outside its scope.

A separate original-executable search checked constant-displacement writes up to 64 bytes that could overlap the inherited flag byte. Its two candidates were both false decodes beginning inside existing MOVZX instructions, confirmed by saved listing boundaries. No matching direct or overlapping writer was established; indirect bases, bulk initialization and other expressions remain open. Checked names stays 665.


### Animation wire insertion: stored record and dirty flags

Read the complete saved pseudocode for the 938-instruction insertion function `1407069d0` and verified all original instruction bytes. The function includes destination filtering, special transform-property preparation, animation-record dispatch or lookup/reuse, wire insertion, event calls, dirty flags and cleanup of marked previous wires. Those paths are now statically located, but their complete semantics and execution are not all established.

A new 48-case native bridge executes two original fragments: the final 64-byte record copy/count increment and the later dirty-flag stores. Six valid wire counts (0/1/63/64/1023/16382) and eight opaque prepared record patterns match an independent memory model. Every byte of the synthetic world and context is compared, with immutable source-frame/config checks and a positive control for distant world corruption. Exactly one wire slot and count change, followed by the three modeled world flags and one context flag.

The bridge deliberately skips the intervening event/control paths. It does not execute transform preparation, dispatcher, capacity guard, target filtering or cleanup. Prepared opaque record bytes do not validate how their fields were computed. Full pseudocode review and byte provenance therefore add no new checked-function credit yet: the function remains unnamed pending ABI and remaining behavioral validation. Checked names remains 665.


### Animation wire insertion: recovered stack descriptor signature

Saved and independently reopened a working signature for `1407069d0`: six register arguments, an 80-byte animation input descriptor passed by value at stack offset 8, and byte controls at offsets 88/96/104. Original caller stack copies and callee accesses support this layout. The return type is working void because callers ignore the return and the function has no established return-value contract. Context, source-object and destination-list pointers remain opaque.

Fresh decompilation now passes `&incoming_record`, `flag_a`, `flag_b` and `override_mode` explicitly to `DispatchAnimationWireRecordUpdate`. This removes the misleading loose stack-variable presentation. The special transform-property path writes three floats to local descriptor bytes 32–43; their precise coordinate meaning remains unresolved. Because the descriptor is passed by value, these writes affect the callee's local copy.

All 938 original instruction bytes and all 9,602 other function names/signatures remain unchanged. Before-state and reopening receipts are preserved locally. This is a type correction, not a new descriptive name: the function remains unnamed while transform, event, filtering and cleanup behavior are investigated. Checked names remains 665.


### Animation insertion: full-entry empty-list boundary

The full original `1407069d0` entry and return path passed 48 empty-destination cases using the recovered six-register/by-value-record/three-control ABI. Fixtures cover wire counts 0/1/63/64/1023/16383, four player indices and two control profiles. Even the maximum valid wire count accepts zero destinations without entering overflow diagnostics.

The original memset thunk executes through a host memset adapter; its saved import binding and original thunk bytes were checked. A synthetic stack-cookie value is supplied. Entire world memory, context, source object, destination list, descriptor/configuration and guards remain unchanged. A positive control confirms that the full-world comparator detects a distant mutation.

This is full-function execution of one no-op control path, not validation of all 938 instructions' behavior. Nonempty target filtering, transform preparation, animation dispatch, events, storage and cleanup remain separate scopes. The existing 48-case store/dirty-fragment evidence is not promoted to end-to-end insertion coverage. No new name credit; checked names remains 665.


### Animation wire insertion coordinator named

Saved `InsertAnimationWiresForDestinationList` after complete static pseudocode review, original-byte verification and scoped full-entry coordination tests. Independent reopening and fresh decompilation confirm the name and recovered ten-argument working signature. Original bytes and all 9,602 other names/signatures remain unchanged.

The new nonempty suite runs the original insertion function for one, two and three destinations, eight supplied transforms and four control profiles: 96 cases. Original wire lookup and the original local-libc infinity classifier execute. Controlled native probes supply dispatcher results and record event/root-commit calls. The insertion coordinator reuses the returned record index, forwards controls, stores expected wire IDs/flags/transforms and passes updated roots to the commit boundary. Defined wire bytes 0–51 match the model; trailing bytes 52–63 remain opaque. Full world/context comparisons constrain mutations to inserted records, count and dirty flags; caller inputs remain unchanged. Transform error was zero in these finite unit-quaternion/positive-scale fixtures.

This validates coordination within the stated probe boundaries, not their algorithms. Special transform-property preparation, target filtering, old-wire cleanup, overflow diagnostics, concurrency and real-game behavior remain unverified. Separate empty-list and store-fragment receipts retain their original limits. The descriptive name does not claim all behavior is verified.

Totals: 666 checked names and 2,078 mapped functions among 9,603 discovered; 7,525 remain unmapped. The new mapping is grounded in the Animation producer, record dispatcher and type-9 wire construction.


### Shared Animation record retirement traced

Saved `RetireUnsharedAnimationRecordAndDispatchWireRemoval` after reviewing all 123 original instructions. Independent reopening and fresh decompilation confirm its four-argument working signature; original bytes and all 9,602 other names/signatures remain unchanged.

The coordinator protects an animation record while another active wire shares the same full packed source reference and record ordinal. Destination and property differences do not change that decision. When no peer protects it and the source is an Animation object, it copies the 72-byte header, sets packed-word bit 31, and commits the replacement header root while preserving the data root. It then dispatches the requested wire removal.

816 original-function cases cover active/inactive peers, different ordinals, sources and packed generations, source kinds, target positions, header patterns, root pairs and player indices. Resource access/update, root commit and removal are controlled native probes. These checks establish the coordinator's decisions and boundary arguments; they do not verify actual wire compaction, resource persistence, invalid targets, concurrency or gameplay. Downstream consumers of bit 31 still need tracing.

Totals: 667 checked names and 2,079 mapped functions among 9,603 discovered; 7,524 remain unmapped. These are identified-code counts, not a percentage of the entire game understood or reconstructed.


### Record replacement through packed resource trees

Saved `ReplaceResourceTreeRecord72ByOrdinal` after reviewing all 97 original instructions and independently reopening its name and three-argument working signature. The ordinal uses a signed integer, matching the native comparisons; valid nonnegative ordinals are the tested scope. Original code bytes and all 9,602 other function names/signatures remain unchanged.

328 connected native cases run record lookup, replacement selection, the copy-on-write tree writer, allocator, iterator, interning, hashing and candidate release. Category-3 fixtures include one and several leaves, trees with one, two, four and six internal levels, changed/identical replacements and beyond-end requests. Exact record contents match the independent model. Old source nodes and caller replacement buffers stay unchanged; identical replacements and beyond-end requests retain their root. The existing and newly traced accessor return identical pointers in these fixtures.

These are in-memory resource checks. Mutex/thread boundaries are controlled, host memory-copy adapters and a synthetic stack cookie are explicit. Disk persistence, gameplay, concurrency, maximum-depth failures, allocation exhaustion and category-1 summary updates remain unverified. No new completion credit is assigned to the already named comparison accessor or the unnamed tree writer.

Totals: 668 checked names, 2,080 mapped functions and 7,523 unmapped functions among 9,603 discovered. Counts describe identified code, not total game completion.


### Animation resource event reaches the registered field

Original metadata initialization confirms Animation property 766 is `HeaderAndDataPages` at object offset `0x110`. The event uses two resource fingerprints rather than assuming local node indices are portable. The original resolver converts incoming fingerprints into local roots and marks found resources dirty; 172 native cases cover both conversion directions, missing/zero fingerprints and collision chains wrapping around the hash table.

196 connected native branch cases cover the property-list and missing-property paths. With a property-list entry, the branch replaces its roots and updates the reflected field only when it still equals the entry's previous roots. A different reflected value remains unchanged. Without a property-list entry, the branch resolves directly into the reflected field. Exact object/property buffers, input stream, 16-byte cursor advance and dirty bitmap match the model.

The fixture metadata slot is populated from the verified original initializer instruction. These checks use original branch, lookup and resolver code, with controlled synchronization and explicit private-clone continuations. They do not execute the entire event dispatcher or establish other modes, null-object handling, disk persistence or gameplay behavior. No additional checked-name credit is claimed; totals remain 668 checked names and 2,080 mapped functions.


### Header/data page event builder named

Saved `DispatchHeaderAndDataPagesChangeEvent` with its five-argument working signature after reviewing all 197 original instructions. Independent reopening and fresh decompilation confirm the name and signature; all other 9,602 function names/signatures and original instruction bytes are unchanged.

300 full-entry native cases verify the exact 22-byte event: property 766, object ID and two resource fingerprints. Sentinel roots become zero fingerprints. The resource dirty bitmap matches the non-sentinel roots. A separate 68-case connected suite follows original retirement through header replacement, resource allocation/interning and event construction: updated header contents survive as resolvable fingerprints while the old header tree and data root remain unchanged.

688 downstream property-branch cases distinguish modes. Mode 1 serializes roots without changing object/property storage. Mode 0 resolves incoming fingerprints and updates a reflected value when it still agrees with the previous property-list value. Tested modes 2 and 255 update an existing property-list value without synchronizing the reflected field. Without a property-list entry, resolution targets the reflected field directly. These observations do not assign broader meanings to the modes.

The event dispatcher and wire removal remain probes in the connected retirement suite. Optional object/player tracking branches, non-default player-state gates, full dispatcher integration, wire compaction, concurrency, persistence and gameplay remain unverified. The separate downstream tests stop at explicit private-clone continuations and retain their own limits.

Totals: 669 checked names and 2,081 mapped functions among 9,603 discovered; 7,522 remain unmapped. This is code-review inventory, not whole-game completion.


### Resource-event tracking side effects checked

1,152 full-entry native cases check the event builder's per-player property notification queue. Across the tested recording-mode/editing/state combinations, property 766 is appended only when the native mode/flag gate allows it and it is not already present. Full world/context comparisons allow exactly the expected queue entry/count updates. These cases use a sentinel object ID to isolate notifications.

A separate 288-case suite exercises object/player dirty membership with valid object IDs. The lookup uses the world referenced by the context, which can differ from the event's world. Direct matches and generation/ID-mismatch chains find the expected object. Missing, out-of-range and sentinel IDs do not change membership. Tracking adds only the selected player's bit and preserves existing bits. Full context and both world buffers match the independent mutation model. This suite suppresses notifications using the previously checked mode/flag combination.

The dispatcher remains a native probe in these full-entry tests. Finite valid pointers and acyclic chains do not establish malformed/cyclic input handling, notification capacity, concurrency, complete dispatch, disk persistence or gameplay. No new checked-name credit is added; totals remain 669 checked names and 2,081 mapped functions.


### Game-wire serializers named and connected

Saved `SerializeGameWireVector` and `SerializeGameWireRecord` after reviewing their complete 158- and 308-instruction original bodies. Both two-pointer working signatures and names survived independent reopening and fresh decompilation. Original bytes and other function names/signatures remain unchanged.

36 connected original-code cases include the vector, wire record, property/flag and transform serializers. For tested format version `0x500`, the stream contains a 32-bit count and 50 bytes per wire: destination, source, property, record index, two flag bytes and 32-byte transform. Nonnegative endpoint references serialize as sign-extended 22-bit indices; negative 32-bit values remain unchanged. Write preserves source records. Read initializes newly exposed slots and preserves opaque trailing bytes. Full vector, serializer, stream and guards match independent expectations.

Scope is counts 0/1/3, unit quaternions and the fast-buffer path. Logging is controlled and the verified original local-libc infinity-classifier body is supplied at the import boundary. Legacy formats, nonunit normalization, slow/error/marker paths, full-world roundtrips, disk persistence, concurrency and gameplay remain unverified.

A separate 96-case original removal-branch check confirms endpoint invalidation and dirty flags without decreasing wire count. Later compaction remains unresolved; serializer/resize count writes are not credited as compaction evidence.

Totals: 671 checked names, 2,083 mapped functions and 7,520 unmapped functions among 9,603 discovered. Extraction and inventory counts do not establish whole-game completion.


### Transform serialization normalization verified

Saved `SerializeTransform32WithQuaternionNormalization` after complete review of its 126 original instructions. Independent reopening and fresh decompilation confirm its working two-pointer signature; original bytes and all other function names/signatures remain unchanged.

422 original-code cases cover read and write, 200 supplied random finite quaternions and explicit scaled, zero, infinite and NaN fixtures. Finite nonunit rotations normalize on both directions. The largest component error against the independent model was about 1.2e-7, below the 2e-6 tolerance. Tested zero or infinite squared lengths use the original identity quaternion; tested NaN rotations retain their input bits. Position/scale bytes, source immutability, stream/record guards and serializer cursor match exact expectations.

These are fast-buffer tests with the verified original local-libc classifier supplied at its import boundary. They do not exhaust subnormal values, normalization threshold boundaries, alternative floating-point control modes or slow/error paths, and do not establish full-world save/load, disk persistence or gameplay. The earlier connected wire test retains its unit-quaternion scope.

Totals: 672 checked names, 2,084 mapped functions and 7,519 unmapped functions among 9,603 discovered. Counts describe identified code, not whole-game completion.


### Wire property/index/flag version migration named

Saved `SerializeWirePropertyIndexAndFlags` after complete review of its 171 original instructions. Independent reopening and fresh decompilation confirm the name and working two-pointer signature; original bytes and all other names/signatures remain unchanged.

256 original-code cases cover both directions at versions `0xc5`, `0x10c`, `0x10d`, `0x3e4`, `0x3e5`, `0x449`, `0x44a` and `0x500`. Older reads unpack 12-bit property and ordinal fields, derive flag bit 0 and set the second flag byte to 1. Version `0x10d` introduces separate full-width property/index values and a flag byte; `0x3e5` adds the second flag byte. Loads before `0x44a` clear flag bit 1. Exact buffers, guards, untouched flag bytes and stream cursor match the independent model.

The tested oldest write branch emits a zero legacy word in this executable. That observation is not a guarantee of supported historical save output. Tests use valid fast buffers and do not establish the record-level pre-`0xc5` layout, slow/error paths, complete legacy record roundtrips, persistence, concurrency or gameplay.

Totals: 673 checked names, 2,085 mapped functions and 7,518 unmapped functions among 9,603 discovered. Counts describe reviewed code, not whole-game completion.


### Versioned wire serializers connected

288 native read/write cases connect the original vector, wire-record, property/flag and transform serializers across eight format versions. In the tested fixtures, record sizes are:

| Format versions tested | Bytes per record |
| --- | ---: |
| `0x10d`, `0x3e4` | 51 |
| `0x3e5`, `0x437` | 52 |
| `0x438`, `0x449`, `0x44a`, `0x500` | 50 |

The connected results confirm the added second flag byte, its preservation from existing/default storage when absent, and the pre-`0x44a` load-time clearing of flag bit 1. Endpoint conversion and all defined fields match the independent model. Below `0x438`, two obsolete bytes before the transform are consumed; their meaning remains unknown and their write values are excluded from byte-content assertions. Exact stream length/cursor, full vector/serializer buffers and guards remain checked.

Scope is counts 0/1/3, unit quaternions and fast buffers. Pre-`0x10d` records, the special `0x1c7`–`0x1cf` branches, slow/error/marker paths and complete historical save compatibility remain unresolved. Source logging is controlled and the verified local-libc classifier is supplied at its import boundary. These checks do not establish full-world disk persistence or gameplay. No additional checked-name credit is added.


### Retired Animation headers excluded from duplicate matching

Saved `FindActiveOrAppendAnimationHeaderRecord72` after complete review of 319 original instructions and pseudocode. Independent reopening and fresh decompilation confirm its working header-pointer/root-pointer/control arguments and signed ordinal return. Original bytes and all other names/signatures remain unchanged.

64 full-entry connected native cases establish a concrete consumer of the retirement marker: with duplicate matching enabled, the helper reuses the first byte-identical header whose first word has bit 31 clear. A bit-31-marked header is skipped even when byte-identical to the incoming record. Otherwise it appends the full 72-byte header and returns its new ordinal. Existing source nodes and caller input remain unchanged. Original iterator, copy-on-write allocator/growth/finalization, interning/hash and independently bound local-libc byte comparison execute together.

Fixtures cover empty and 1/7/9-header trees, first/last/no duplicate matches, retired duplicates, active/retired input and controls 0/1. Synchronization is controlled and memory-copy adapters are explicit. Exhaustion, maximum depth, concurrency, disk persistence and gameplay are unverified. This establishes exclusion from duplicate reuse, not sampler skipping, physical record deletion or wire compaction.

Separate 31,248 original count-fragment cases show that nine sampler count calculations exclude the high four header bits; they do not execute full sampling and receive no new-name credit. The larger basic/extended samplers remain only partially reviewed.

Totals: 674 checked names, 2,086 mapped functions and 7,517 unmapped functions among 9,603 discovered. Counts describe identified code, not whole-game completion.


### Boolean Animation sampling with retired-header flags

168 native cases enter the original basic and extended samplers: 84 per implementation. With `AnimStrength = 1`, both match an independent three-key boolean step model across six value patterns and seven query times, including queries before and after the key range. Toggling header bit 31 leaves the sampled output unchanged in these fixtures. This distinguishes sampling behavior from the duplicate-search helper, which excludes bit-31-marked headers.

The checks compare boolean value, alpha, type and padding, preserve output guards, and verify source, header and resource-leaf immutability. Extended fixtures supply valid interned header/data roots and the original typed-record comparison helper. An earlier invalid fixture omitted the header root and looped; that isolated run was stopped and corrected before the final passing run.

These results cover three-key boolean paths with one data leaf, one header leaf where required, zero extended metadata and null optional arguments. Other strengths, record formats, cross-leaf paths, wrapper behavior and gameplay remain unverified. Neither large sampler receives whole-function review or naming credit. Checked-name and mapping totals are unchanged.


### Animation sampling wrapper and parent lookup

168 basic-path and 168 extended-path native cases enter the original wrapper and sampler together. Header flag `8` forces output alpha to zero after sampling. On the tested extended path, it also sets an optional output byte to `1`; without the flag, that byte stays untouched. The retirement marker does not change the tested boolean results.

A further 168 cases exercise property `0x231` with boolean samples. The wrapper uses an identity transform fallback and composes the header and wire transforms. Forty-two seeded finite pose pairs with normalized rotations and positive scales match an independent quaternion, translation and scale model within `2e-5` absolute/relative tolerance, across both alpha-suppression and retirement flags. Source, header, data leaf and wire remain unchanged, with output guards and padding checked. Other Variant conversions, degenerate rotations, secondary output and the other special properties remain unresolved.

The related 85-instruction target lookup was fully read and matched to original bytes. In 120 native cases, it follows inheritance-marked ancestors using signed low-22-bit parent indices, then returns kind `11` immediately or follows at most two additional parents. The final returned parent need not be kind `11`. Invalid links in the tested non-inherited traversal return null; invalid inherited links are dereferenced before a null check and were not executed. Valid acyclic chains only; generation bits are ignored by this lookup. Its original type names and the original name of property `0x231` are not established here.

These are local original-code fixtures, not gameplay runs. No function name, type or whole-function completion credit was added.


### PuppetHeart or fallback ancestor lookup named

Saved `ResolvePuppetHeartOrFallbackAncestor` after full review of its 85 original instructions and pseudocode. Original enum registration identifies kind `11` as `PuppetHeart`; both its literal and registration instructions were independently matched to the original executable. This resolves the previously unnamed kind in the wrapper lookup findings.

The helper follows inheritance-marked ancestors, then returns PuppetHeart immediately or follows at most two additional parents. Its final fallback can be another type. 120 native cases validate valid acyclic inherited chains, early matches, fallback, ignored high reference bits and null results for invalid non-inherited links. Invalid inherited links are dereferenced before a null check and were not executed. Independent reopening and fresh decompilation verify the saved two-pointer working ABI, pointer return and unchanged original bytes; all other names/signatures remain unchanged.

Mapped under shared object references. Totals are 675 checked names and 2,087 mapped functions, with 7,516 still unmapped among 9,603 discovered. This does not establish complete object layouts, gameplay behavior or whole-game completion.


### Puppet-relative Animation vector adjustment

504 boolean and 336 typed-record native cases connect the original wrapper, basic sampler, scalar reducer and `ResolvePuppetHeartOrFallbackAncestor`. For properties `0xb8` and `0xb9`, the wrapper converts inputs to an X/zero/Y vector, rotates it by the resolved PuppetHeart quaternion and returns the rotated X/Z pair as Float2. Boolean and Number inputs replicate their scalar into X and Y. For property `0x25b`, the result is Float3: scalar inputs are replicated across three lanes, Float2 supplies X/Y/zero, and Float3/Float4 supply X/Y/Z before rotation.

The fixtures use the exact kind-11 property-zero offset `0x50`, independently verified from the original initializer instruction; the quaternion is read at property `+0x10`. Only this matrix entry is supplied, rather than executing the full runtime metadata constructor. The typed input tags match the existing registry, with their original name literals rechecked.

Typed tests contain a single 48-byte record, so they establish conversion and rotation, not typed interpolation. Both suites use `AnimStrength = 1`, finite inputs, normalized rotations and a valid inherited parent link. Alpha-suppression and retirement flags, full output/guards/padding, unused payload bytes and source/header/resource/object/world/wire immutability are checked against an independent model. The remaining conversions, Quaternion angle conversion, other parent chains, original property names and gameplay remain unresolved. No new naming or completion credit is added.


### Animation sample/property-transform wrapper named

Saved `SampleAnimationRecordWithPropertyTransforms` after full review of its 508 original instructions and pseudocode. It selects the basic or extended sampler, applies the alpha-suppression flag, converts sampled values for special wire properties and supplies an optional keyframe output. Independent reopening and fresh decompilation confirm the name and unchanged bytes; existing parameter/return metadata is preserved because floating-register and opaque auxiliary argument types still need caller tracing.

The combined evidence now contains 2,688 full-wrapper native cases across seven scoped suites. New Quaternion coverage adds 576 cases: property `0x25b` matches a principal axis-angle rotation vector in degrees before PuppetHeart-frame rotation, while `0xb8`/`0xb9` use raw X/Y quaternion lanes. The original local-libc `acosf` body and nine constant spans execute on in-domain inputs. Forty-eight finite unit-quaternion fixtures span eight angles, both signs and small/half-turn cases; the independent model tolerance is `0.001` degrees absolute and `0.0002` relative. This is not an exact trigonometric or out-of-domain guarantee.

Another 768 cases cover Position, Float3, Impact and Number inputs to property `0x231`. Position supplies a full transform; Float3/Impact supply translation with unit scale and identity rotation; Number falls back to identity. The result matches header × sample × wire transform composition. Original registration identifies source byte `+0x134` as `IsKeyframe`: when enabled, the optional secondary output receives the header three-vector, alpha with its sign cleared, and Float3 tag, preserving unused bytes. The fixture toggles this field, alpha-suppression and retirement flags while checking all guards and immutable inputs.

Typed suites use one key and `AnimStrength = 1`; general interpolation, cross-leaf traversal, other strengths, nonfinite/degenerate transforms and gameplay remain unverified. The two large samplers retain their partial-review status. Totals are 676 checked names, 2,088 mapped functions and 7,515 unmapped among 9,603 discovered.


### Number interpolation distinguishes key gaps

1,872 new native cases connect the named wrapper and original basic sampler: 936 use one data leaf and 936 use two leaves under a resource-tree branch. An independent three-key Number timeline model matches six key spacings, thirteen query fractions and both alpha-suppression/retirement flags. Value, type, alpha, unused payload, padding and guards are checked; source, header and resource nodes remain unchanged.

The initial assumption of universal linear interpolation was disproved. The reviewed native branch interpolates close keys, but when float32 left-time plus the original `0.05000000447` constant is no greater than right-time, it selects one recorded value instead. In the tested gaps, the switch occurs around right-time minus `0.033333335` plus `0.0001`; nearby endpoint snapping also applies. These constants and the actual interpolation/selection instructions were independently matched to original bytes. This is scoped evidence, not an exhaustive threshold-rounding guarantee.

The branched tests respect the writer layout: whole 48-byte records in 480-byte leaves, with 24-byte logical page gaps. The first key starts at offset 432; later keys occupy the next leaf. Resource traversal uses the original code with an explicit host CRT double-`pow` import adapter. These tests do not split individual records across padding gaps.

Scope is three Number keys starting at time zero, `AnimStrength = 1` and null wire/optional outputs. Other formats, strengths, easing, deeper trees, nonfinite values and gameplay remain unresolved. No additional names or completion credit are added.


### Extended Number easing and stepped timing

45,864 new native cases connect the wrapper and original extended sampler: 936 with zero extra metadata, 11,232 with explicit easing and 33,696 with quantized easing. Zero metadata preserves the tested gap-aware behavior. Explicit modes 1–4 instead match linear, ease-in, ease-out and symmetric power curves, including across larger key gaps. The four-bit strength field produces exponent `1 + 7 × (strength / 15)^2.807354927`; tested strengths are 0, 7 and 15.

Bits 6–7 select stepped timing: nonzero values 1/2/3 floor elapsed time into approximately 2/30, 3/30 or 4/30-second bins before curve shaping. The original mode/strength/quantization instructions were independently matched to executable bytes. The verified local-libc `powf` body and constants execute on finite in-domain inputs; the independent curve model matches within `0.00002` absolute/relative tolerance.

Media Molecule’s [Animation Canvas guide](https://docs.indreams.me/en/create/resources/recording-modes) describes blend/ease controls and every-second, third or fourth-frame stop-motion blending. That is consistent with these findings, but the editor control-to-metadata writes still need tracing. It does not establish a coding-livestream/source-code match or identify this executable’s exact build.

Scope is three 56-byte Number records, one data leaf plus a matching header leaf, six key spacings, thirteen query fractions and `AnimStrength = 1`. Alpha-suppression/retirement flags, full output/guards/padding and source/header/resource immutability are checked. Metadata linkage/omission bits, mixed modes, smoothing/springiness, other formats/strengths, library errors, deeper trees and gameplay remain unresolved. No naming or completion credit is added.


### Blend names checked against the executable

The original `EBlendType` registration explicitly maps 0–4 to None, Linear, EaseIn, EaseOut and EaseBoth; 5 is the `LAST` sentinel. These names agree with the independently tested extended-key mode behavior. The registration instructions and original literals were checked directly.

The shared editor-action table contains 836 names, including the Animation Canvas blend actions. Its consumer subtracts one from the action ID before a bounded lookup. This avoids treating the table’s zero-based indices as action IDs. The actual callback-to-key-metadata writes remain unresolved; the table alone does not establish that connection. No function was created, renamed or given completion credit in this trace.


### Unwind-boundary audit repairs missing colour branches

The original executable’s unwind header yields 20,887 sorted, non-overlapping regions and 78 checked CIE records. 8,951 starts match existing Ghidra function entries; 11,936 lack an exact existing entry. These are boundary records, not additional understood functions, and are kept separate from the project’s 9,603 defined-function inventory. They provide a firmer basis for investigating code that has no current function definition or lies beyond an imported body.

All 676 reviewed names match original unwind starts, with no saved body extending outside its matching region. Examining excluded bytes found 887 NOP regions, 246 `UD2` trap regions and two regions containing actual SIMD code. Those two regions belong to `EvaluateAnimationDeltaOnBaseValue`: five HSV-to-RGB sectors had been omitted from the imported Ghidra body.

The saved repair adds those 85 original bytes and records the exact six destinations from the original relative jump table. Independent reopening and fresh decompilation confirm 1,678 analyzed instructions, recovered switch targets and removal of the previous jump-table warning. All executable bytes, names, signatures and other function bodies remain unchanged. The mapping fingerprint was refreshed to include the restored instructions.

3,425 original-code fragment cases cover all six hue sectors and agree with an independent HSV-to-RGB model, with maximum RGB error below `0.00000047`. Inputs are finite periodic hues and saturation/value in 0–1, with a zero additive input and a private harness continuation. These are fragment tests, not full Animation delta evaluation or gameplay runs. The enclosing helper remains partially reviewed, and no name or completion credit is added.


### Sparse Animation records rebuilt and wires remapped

Saved `RebuildSparseAnimationRecordsAndRemapWires` after complete review of 315 original owned instructions and pseudocode. Both direct caller neighborhoods guard kind-9 Animation objects and pass the world and Animation pointers. Independent reopening verifies the name, working two-pointer SysV signature, unchanged original bytes and unchanged names/signatures elsewhere.

108 full-entry native cases connect the original helper, resource extraction, append and resource allocation/interning. Fifty-four cases rebuild sparse referenced ordinals into first-use order, copy their headers/data and update matching active wire indices. Duplicate references retain sharing. Fifty-four cases leave roots unchanged: dense ordinal sets, no matching references and trailing unused records alone do not trigger rebuilding. Old source nodes and unrelated world/source bytes remain unchanged.

The packed remap contains old/new 32-bit ordinals. The original `VPINSRD` inserts the new ordinal into its high half; the current pseudocode omits that insert. Assembly and independent duplicate-group fixtures verify the actual behavior, so the pseudocode should not be used as a faithful port of this operation.

Fixtures cover five one-key Bool headers in basic, extended and mixed layouts, internal holes, aliases, inactive/foreign wires and high reference bits. Host aligned heap/free/memset and controlled TLS boundaries are explicit. Large/deep resources, complex linked metadata, allocation failure, concurrency, persistence, event propagation and the retirement-to-compaction call chain remain unverified. Rebuilding resource contents does not establish physical cache or disk reclamation. The editor-to-key-metadata write path remains unresolved.

Totals: 677 checked names, 2,089 mapped functions and 7,514 unmapped among 9,603 currently defined. These counts do not include the separate unwind-region candidates and do not measure whole-game completion.


### Animation records rebuilt separately for each active wire

Saved `RebuildAnimationRecordsPerActiveWire` after reviewing all 151 owned instructions and complete pseudocode. Both original caller neighborhoods invoke it before the sparse-record compactor for kind-9 Animation objects. Independent reopening verifies the descriptive name and working two-pointer SysV signature, with original bytes and other names/signatures unchanged.

145 connected native cases cover the null-world and world-byte guards, wire ordering, duplicate references, empty matching sets, inactive/foreign/invalid-source wires, high source-reference bits, header flag stripping and two key-time ranges. In the tested basic Bool layout, each matching active wire receives its own appended record—even if several wires previously shared one. Payloads and reference frames remain intact, header time bounds are recomputed, only the low two header flag bits survive, roots are replaced and three Animation runtime fields reset. An empty matching set yields invalid roots. Old resource nodes remain unchanged.

This differs from the following sparse compactor, which preserves shared references and skips dense ordinal sets. The fixtures execute the original rebuild, copy, range, append and resource-interning paths, with explicit host allocator/free/memset, controlled TLS and two synthetic runtime defaults. Extended inputs, other formats, deep resources, failures, persistence, gameplay and the full enclosing workflows remain unverified. No UI-to-key-metadata connection is claimed.

Totals: 678 checked names, 2,090 mapped functions and 7,513 unmapped among 9,603 currently defined. These are code-review counts, not whole-game completion.


### Why the two Animation rebuild helpers run in sequence

The world-byte guard is now identified by original Boolean field registration as `anim_2_upgraded`. When it is clear, `RebuildAnimationRecordsPerActiveWire` produces dense records, one per matching active wire. In 72 connected basic Bool cases, the following `RebuildSparseAnimationRecordsAndRemapWires` changes no roots, Animation bytes or world/wire bytes.

When `anim_2_upgraded` is set, the first helper skips rebuilding. In 108 connected basic/extended/mixed Bool cases, the second helper alone handles sparse referenced ordinals, preserves shared references and retains the tested header flags and payload bytes. Fifty-four cases rebuild; fifty-four skip because referenced indices are dense, absent, or have only trailing unused records.

The original copy helper moves raw resource bytes. Its stride argument aligns capacity truncation; it does not convert each key. Together with the registered upgrade guard, this rules out treating the first helper as a general extended-to-basic converter. One original caller places the pair in a serialization-upgrade path, but the complete format migration and the second enclosing caller remain unresolved.

These are 180 connected pair cases with single-leaf Bool fixtures, explicit host allocator/free/memset and controlled TLS/runtime boundaries. They do not prove all formats, deep resources, persistence, whole-caller execution, UI metadata writes or gameplay. No new names or completion credit are added; totals remain 678 checked names and 2,090 mapped functions.


### Bounded record resource payload copy

Saved `CopyRecordResourcePayloadToBoundedBuffer` after reading its complete pseudocode and all 168 owned original instructions, verifying the bytes and matching the original unwind extent. Independent reopening verifies its descriptive name and working four-argument SysV signature; original bytes and other names/signatures remain unchanged.

10,200 native cases check exact output and buffer guards across one leaf and a branch over three full 504-byte leaves. They vary byte offsets, requested lengths, capacity, positive strides 1/8/12/48 and the high four length bits. The helper copies raw bytes using the low 28-bit count and offset. If capacity is too small, the copied total is rounded down to a stride multiple. It does not convert key formats. Header, source nodes, destination pointer and capacity remain unchanged in the fixtures; output length is updated.

The tested destination starts empty. Nonempty destinations, deeper trees, malformed inputs, zero-stride truncation, concurrency and gameplay remain unresolved. Host memmove and double pow boundaries are explicit. Two direct callers are the Animation rebuild helpers; a third caller remains unreviewed.

The newly inspected writers of `anim_2_upgraded` lead into larger serialization/world-building routines. Setting that flag alone does not prove these functions convert Animation keys. Their complete roles and the actual migration remain unresolved; no additional name credit is assigned to them.

Totals: 679 checked names, 2,091 mapped functions and 7,512 unmapped among 9,603 currently defined. These are review counts, not whole-game completion.


### AutoBlend action linked to recording input metadata

Original action-table and dispatch evidence identifies action 818 as `KeyframeModeAutoBlend`. Its case toggles the selected Machine byte at `+0xd6` with XOR 1. The recording input producer selects the same Machine, reads that byte and builds `0x720 | byte | (byte << 3)`: Boolean settings 0/1 produce `0x720`/`0x729`. A separate conditional path writes `0x730` for a later marker, advancing time by the original approximately 1/30-second constant. The marker's full semantics remain unresolved.

1,536 native fragment cases connect the original action dispatch, toggle case and metadata arithmetic across three Machine positions, all 256 initial byte patterns and two toggles. Only the selected byte changes in the world fixture, and the second toggle restores it. All byte patterns are arithmetic probes; only 0/1 are interpreted as Boolean settings. Prepared stack locals and private return continuations bound execution; the complete UI handler and recording commit were not run.

Renamed the working Machine prefix field from `opaque_flags_d6` to descriptive `keyframe_auto_blend`. Independent reopening and fresh typed-consumer decompilation confirm it. The byte datatype, partial prefix size, other fields, function names and signatures remain unchanged. This is a field identification, not a new reviewed-function count.

One input control now has a concrete action-to-input-metadata link. The broader Animation Canvas blend/strength controls, final stored-key conversion, complete producer behavior and gameplay remain unverified. Totals remain 679 checked names and 2,091 mapped functions.


### AutoBlend metadata through converter, filter and resource append

864 connected native cases now exercise the original AutoBlend dispatch/case fragment, complete `ConvertAndReduceAnimationInputKeys`, `ClearAllZeroAnimationInputForSelectedProperties` and the original append/resource interning. Fixtures use property `0xba`, whose original format table identifies Bool, Keyframe/AutoKeyframe recording modes, three Machine positions, input counts 0/1/2/3/7/17, constant/alternating values, two input strides and both high-header-bit states.

The converted extended Bool metadata is `0x700` with AutoBlend off or `0x709` with it on. A single-input AutoKeyframe adds `0x20`, producing `0x720`/`0x729`. All four words are independently read back from retained stored payloads. In 432 cases a nonempty payload reaches the resource tree byte-for-byte; 432 cases are empty or cleared by the zero filter. Header contents, source/Machine immutability and output guards are checked within the harness.

The zero filter examines basic 8-byte positions even when supplied the tested extended 12-byte records; its scoped output matches an independent byte-position model. This observation is not a game-bug claim. Actual producer routing and framing must be established before interpreting its effect on the game.

The host prepares UI stack locals, source records and the final 80-byte record descriptor, and starts append with empty roots. Original components run between those explicit boundaries. Thus the test proves component-level metadata preservation through append, while complete recording-event execution, original caller framing, wire insertion/notifications, other formats, disk persistence and gameplay remain unresolved. No additional names or whole-game completion credit are added; totals remain 679 checked names and 2,091 mapped functions.


### Animation wire record replacement and notifications

Saved `ReplaceAnimationWireRecordOrdinalAndNotify` after reviewing all 370 owned original instructions and complete pseudocode, verifying bytes and matching the original 1,556-byte unwind extent. Independent reopening verifies its descriptive name and working seven-argument SysV signature. Original bytes and all other names/signatures remain unchanged.

244 full-entry native cases cover 120 replacements, 120 removal dispatches and four queue-boundary cases. The helper dispatches event `fdf3` before writing the wire record ordinal and `fdf5` afterward. Eligible recording contexts queue inverse events in the opposite order. If the new ordinal or destination is absent, it dispatches removal instead. Alternate-world mode suppresses the owner and queued recording. Queue-capacity rejection sets an owner status flag while replacement and immediate notifications continue. Callback arguments, ordinal timing, source/destination identities, control flags, queue counters and unrelated bytes are checked.

The three event/removal callees are recording probes with controlled returns. Their original event effects and actual removal were not executed here. Global force-history mode, invalid references, full producer execution, resource append, disk persistence and gameplay remain unresolved. This identifies the caller's record-update helper without claiming the entire recording path is complete.

Totals: 680 checked names, 2,092 mapped functions and 7,511 unmapped among 9,603 currently defined. These are code-review counts, not whole-game completion.


### Property-event history routing connected to Animation replacement

Saved `RoutePropertyEventToEnabledHistoryStreams` after complete pseudocode review and verification of all 324 original owned instructions. Independent reopening verifies the descriptive name and working nine-argument SysV signature. Original bytes and all other function names/signatures remain unchanged.

216 connected cases execute the original Animation wire replacement, history router and packed-event writer. First, second or both enabled history streams receive exact 22-byte before/after snapshots, byte counts increase by 44 and corresponding pool active flags are set. Missing or disabled history suppresses stream writes while direct replacement and eligible owner inverse-queue writes still occur. The first stream's stable-ID source lookup executes against a controlled current world. This clarifies that the previously probed notification helper routes recording/history events; it did not by itself prove game-event application.

A separate 240-case suite executes the original inverse-queue writer. Wire snapshots contain a 16-bit event ID followed by five 32-bit words: source ID, destination ID, property, record ordinal and flags. Every one of 480 attempts adds 22 bytes, including 144 candidates matching existing snapshots. The original exclusion mask bypasses coalescing for `fdf3`/`fdf5`; the initial hypothesis that these wire events replace matches in place was disproved and corrected before publication.

The history-context resolver returns a fixture and final event application remains a recording probe. Non-wire prehandlers, revision refresh, context lookup, history reclamation/overflow, the full recording producer, disk persistence and gameplay remain unresolved. The generic packed-event writer is still only partially validated; it receives no new name credit.

Totals: 681 checked names, 2,093 mapped functions and 7,510 unmapped among 9,603 currently defined. These are review counts, not whole-game completion.


### Original player history context lookup connected

Saved `FindOrAssignPlayerPropertyHistoryContext` after reviewing complete pseudocode and all 194 owned original instructions, verifying bytes and matching the 862-byte unwind extent. Independent reopening verifies its descriptive name and working pointer-return SysV signature. Original bytes and all other function names/signatures remain unchanged.

306 direct native cases verify existing-key reuse, first-empty assignment, recycling in all four slot positions and world/player/type-key guards. The selected player's Machine must match the configured type key. An existing key returns its context unchanged; assigning an empty ID changes only the ID. Recycling chooses a slot not held by active matching players and resets specific history metadata, counters, scan offsets and the disabled flag. It does not wipe payload bytes. The whole slot arena and world are checked against an independent model.

The earlier 216-case history suite now executes this original lookup as well as the original wire replacement, history router and packed-event writer. First, second or both history streams receive the verified snapshots and counters; blocked lookup or disabled context suppresses stream writes while direct replacement remains active. This removes the substituted lookup return from that tested path.

Globals, the Machine type key, an existing keyed slot and stream pointers are prepared fixtures; final event application remains a recording probe. Empty/recycled slots are tested directly but their complete initialization/lifecycle is not connected. Context exhaustion, invalid Machine indices, concurrency, actual type-key initialization, full recording, disk persistence and gameplay remain unresolved.

Totals: 682 checked names, 2,094 mapped functions and 7,509 unmapped among 9,603 currently defined. These are review counts, not whole-game completion.


### History revision synchronization and future metadata trimming

Saved `SyncPropertyHistoryRevisionAndTrimFutureMetadata` after complete review and byte verification of its 33 owned original instructions. Independent reopening verifies the descriptive name and working two-argument SysV signature. Original bytes and all other function names/signatures remain unchanged.

600 direct cases execute the original context lookup and refresh helper. The helper copies the world revision into the selected history context and sets its end to the current cursor. When the cursor is below the old end, it clears specific future-entry metadata fields, leaving recorded payload and other metadata untouched. When the cursor is above the old end, it raises the end without clearing. A blocked lookup is a no-op. The context disabled flag does not guard this helper itself; the surrounding router checks that flag before invoking it.

The connected 216-case suite now uses a world revision change from 0 to 7 and two future metadata entries. Original replacement, lookup, history routing, packed-event writing and refresh execute together: enabled histories receive the verified snapshots, synchronize the revision and clear the future metadata. Missing or disabled history still suppresses routing. This removes the earlier matching-revision-only restriction for these fixtures.

Prepared globals, an existing keyed context, a matching Machine type key and bounded index fixtures remain explicit. Final event application is still a recording probe. Malformed indices, context initialization, concurrency, new history commit, reclamation, full recording producer execution, disk persistence and gameplay remain unresolved.

Totals: 683 checked names, 2,095 mapped functions and 7,508 unmapped among 9,603 currently defined. These are review counts, not whole-game completion.


### Full wire-event write packets include a normalized transform tail

The final dispatcher probe has now been removed from the tested write path. In 648 connected cases, original wire replacement, context lookup, history routing, packed-event writing, the dispatcher entry, transform-tail writing and revision trimming execute together. Complete `fdf3` packets contain a 22-byte snapshot plus a 32-byte transform tail, totaling **54 bytes**. `fdf5` remains **22 bytes**. Each complete before/after pair therefore adds **76 bytes**. Earlier 44-byte pair results measured only snapshot headers with the final dispatcher explicitly probed; they were not complete packet-size measurements.

Unit, scaled and zero source rotations produce the expected normalized tail while the source wire transform remains unchanged. Exact history/owner queue contents, byte counters, direct ordinal changes, missing/disabled context behavior and future metadata trimming are checked. Only the selected mode-1 wire paths of the 267,374-byte dispatcher execute; the entire dispatcher receives no semantic completion credit.

Saved `SerializeTransform32WithNormalizedWriteRotation` after reading and byte-verifying all 63 owned original instructions. Independent reopening verifies its name and working signature. 558 direct cases cover mode 0 raw reads, writes for nonzero modes whose low byte equals 1, and cursor-only modes. All advance 32 bytes. Writes preserve the first 16 bytes and normalize the last 16-byte quaternion; zero/infinite squared norms use identity, and tested NaN/near-unit values are preserved. Finite normalization error is below 0.00000012. Original verified local-libc classification executes. Original bytes and other names/signatures remain unchanged.

Prepared globals, type key, keyed context and stream pointers remain fixtures. Replay-mode wire creation/deletion, other event branches, full recording producer execution, concurrency, disk persistence and gameplay remain unresolved. This proves the selected original write path, not the complete recording subsystem.

Totals: 684 checked names, 2,096 mapped functions and 7,507 unmapped among 9,603 currently defined. These are review counts, not whole-game completion.


## Wire-event replay creation and removal checked

The complete original event dispatcher entry now executes both wire replay branches in isolated native checks: 60 creation cases and 24 removal cases. Its 267,374 original bytes remain unchanged; this is branch evidence, not semantic credit for the entire dispatcher.

For `fdf3`, replay resolves stored persistent object IDs through `ResolvePersistentObjectIdToIndex`, appends a 64-byte wire record, restores property, record ordinal and flags, copies the 32-byte transform unchanged and increments the wire count. Counts 0, 1, 17 and 16,382 append successfully. At 16,383, creation is skipped but the transform cursor still advances 32 bytes. Replay preserves the tested scaled quaternion; normalization belongs to the previously checked write path.

For `fdf5`, replay replaces the selected wire's two endpoint indices with invalid values and sets the world and optional owner dirty flags. The wire count, transform, remaining record fields and cursor stay unchanged. Every case checks the complete world and owner buffers against the expected changes.

The host supplies the decoded event ID, header descriptor and removal wire pointer. The upstream packet reader, removal target selection, complete undo/redo lifecycle, malformed chains, concurrency and gameplay remain unverified. No functions were newly named or marked complete. Checked names remain 684. [Sanitized check results](analysis/wire-replay-dispatcher-checks.json).


## Wire replay connected through the original range reader

The earlier host-decoded dispatcher checks now have an upstream connection: the original range reader (`140b1a750`), packet wrapper (`140b1b7b0`) and dispatcher execute together in 60 creation and 120 removal cases. All 949 reader instructions and 923 wrapper instructions were matched against original executable bytes. These counts describe checked native bodies, not whole-function semantic completion.

The reader identifies the event and supplies decoded inputs itself. Removal searches existing wires by source/destination persistent IDs, property, ordinal and flags bit 0. First/middle/last targets, missing targets and property/ordinal/flag mismatches were checked with complete world/owner buffer comparisons. Missing or mismatched targets leave the world unchanged; the tested higher flag bit does not affect matching.

A separate 120-case observation suite checks inverse notification after creation. It selects the first matching wire, so an older duplicate can be selected instead of the appended wire. Exact duplicates and duplicates differing only in flag bit 16 select the older entry; property, ordinal and bit 0 mismatches select the new entry. This is observed selection behavior, not a claim of a gameplay bug.

Allocation, free and thread-local access remain controlled test boundaries. History output is disabled in the connected reader suites; the inverse-selection suite uses an explicit history-router observation probe. Complete user undo/redo, malformed inputs, dependency cycles, concurrency and gameplay remain unresolved. No checked-name or completion credit was added. [Sanitized evidence](analysis/wire-replay-dispatcher-checks.json).


### Inverse event-code mapping named; mixed replay follows pass order

Saved `GetInverseRecordedEventCode` with a working `ushort` input and return type. The complete 37-instruction original body exchanges seven pairs: `fde8/fdf2`, `fdf3/fdf5`, `fdf6/fdf7`, `fe06/fe08`, `fe0b/fe0c`, `fe0e/fe0f`, and `fe13/fe15`. All other 16-bit values remain unchanged. 131,072 native cases exhaust the 16-bit input domain with two upper-half patterns; applying the mapping twice restores each value. Independent reopening confirms the name, signature and unchanged original bytes; all other 9,602 names/signatures are preserved. The caller uses the mapped code for inverse history notification. This does not prove full event semantics or undo/redo correctness.

Mixed wire streams now have 128 connected reader/wrapper/dispatcher checks. An initial input-order model failed on removal followed by creation. The original selection assembly explains why: creation runs in pass 2, removal in pass 3, even when removal appears first in the input bytes. The corrected model checks eight sequences with identical and alternating ordinals, full world/owner comparisons and input guards. Removal selects the first live match without decrementing the wire count; unmatched removals do nothing. Allocation/free/TLS remain controlled, history output is disabled and malformed/dependency-cycle/concurrent/gameplay behavior remains unresolved. This observation alone is not a game-bug claim.

Totals: 685 checked names, 2,097 mapped functions and 7,506 unmapped among 9,603 currently defined. Review counts are not whole-game completion.


## Recorded wire removal and inverse replay connected

The original wire-removal producer now connects to the previously checked wrapper and dispatcher. 32 recording-disabled cases preserve payload/count and invalidate the endpoints. Another 64 cases check player 0 with owner recording enabled/disabled: enabled recording appends the exact 22-byte removal snapshot to the owner queue, while disabled recording leaves the queue unchanged. Both tested quiet values preserve that queue distinction.

A 72-case connected suite enables the first history stream, second stream or both. Before the endpoints are invalidated, the original history machinery writes a 54-byte inverse creation event containing the pre-removal transform with normalized rotation. The test then feeds those actual generated bytes through the original range reader, wrapper and dispatcher. Replay appends a restored wire at the next slot, retains the old invalidated slot and increases the count from 3 to 4. Unit, scaled and zero source rotations produce the expected normalized restored rotation. Complete world, owner, history, source/destination objects and replay-input guards are compared.

The final suite byte-verifies all eight captured native bodies (producer, router, packet writer, context lookup, revision synchronization, transform writer, range reader and wrapper), plus the unchanged 267,374-byte dispatcher. Earlier suites overlap this final suite and are not additive semantic-coverage counts.

Prepared history contexts, stream buffers, Machine key and globals remain fixtures. Optional endpoint and parent cleanup are disabled; allocation/free/thread-local access are controlled during replay. Initial harness gaps in pool-global and destination-ID table setup were corrected before the passing suite. Capacity exhaustion, malformed references, concurrency, gameplay and the complete user-facing undo/redo lifecycle remain unverified. No function-completion or checked-name credit was added. [Sanitized receipts](analysis/wire-replay-dispatcher-checks.json).


### Context-filtered wire connection counting named

Saved `CountFilteredWireConnectionsForReference` after reading and byte-verifying its complete 146-instruction body. It compares full 32-bit packed endpoint references and counts each matching wire once, including self-connections. A generation-bit mismatch does not match merely because the underlying object index is the same.

Bit-0-clear wires count when either endpoint matches. With no valid selected Machine, bit-0-set matches are excluded. With a valid Machine, its byte at offset `bbd` suppresses flagged matches. Otherwise they count if an endpoint state byte at offset `22` is nonzero, or if the source matches the Machine reference at offset `b8` and a type-6 record resolves. Both direct mapping and fallback linear record lookup were checked. The meanings of those state bytes and record type remain unresolved.

1,584 native cases compare an independent predicate and verify complete world/object preservation. Coverage includes missing/non-type-6 records, Machine validity and suppression, endpoint states, high flags, packed generation bits, empty lists and source/destination/self/sentinel cases within the stated valid-pointer boundaries. Removal callers compare the count with 1 before optional endpoint cleanup; the function itself changes no world/object data. Independent reopening confirms the descriptive name and working `uint` return with world pointer and 32-bit reference inputs. Other names/signatures and original bytes are unchanged.

Malformed/null active-Machine object paths, record-table corruption, overflow and gameplay remain unverified. No visibility or keyframe-source meaning is assumed.

Totals: 686 checked names, 2,098 mapped functions and 7,505 unmapped among 9,603 currently defined. Review counts are not whole-game completion.


## Optional endpoint cleanup selection connected

256 connected native cases now execute the original removal producer and `CountFilteredWireConnectionsForReference` together. With optional cleanup enabled, the producer separately checks each endpoint: its kind must have a positive offset entry for property `41`, and its filtered connection count must equal 1. Only then does it request a property update with 32 zero bytes. The suite observes 64 such calls across single, duplicated, source-only-extra and destination-only-extra wire configurations and context-dependent flag filtering.

The positive table entry is a property offset in the per-kind property matrix. Byte-verified initializer stores directly establish property `41` offsets `a0` for kind 0, `180` for kind 1 and `110` for kind 17. This is a partial initializer reconstruction; it does not imply other kinds lack the property. The original size table gives this property a 38-byte packet: 6-byte property/object header plus 32-byte payload.

The property updater is an explicit observation boundary. All 32 payload bytes, object selection and property ID are checked; its actual application and field name remain unresolved. Original producer/counter bodies (401 and 146 instructions) are byte-verified, and complete world/owner/object comparisons show only the expected removal and dirty flags when the update is observed. Synthetic support entries, valid object pointers and endpoint class bytes that avoid parent cleanup remain fixtures. No new name or completion credit was added. [Sanitized evidence](analysis/wire-replay-dispatcher-checks.json).


## Sculpt cleanup field identified as GadgetConnector

For Sculpt (kind 1), property `41` is now linked to the registered field **GadgetConnector** at object offset `180`. The original property-matrix initializer assigns that offset to property `41`; the original `RegisterSculptProperties` sequence passes the literal `GadgetConnector` and the same offset to the field registration helper. All four registration instructions, initializer bytes and literal bytes were checked against the original executable. The packet-size table independently gives 38 bytes, including the 32-byte payload observed in removal cleanup.

This identifies the Sculpt field targeted by the earlier zero-payload update. It does not yet establish its members, the meanings of the 32 bytes, the effects of applying the update, or the field names for other object kinds. The property dispatcher has a separate `41` branch that checks packed property storage; its fallback/direct application and related side effects still need execution checks. No additional checked name or completion credit was added. [Sanitized linkage](analysis/wire-replay-dispatcher-checks.json).
