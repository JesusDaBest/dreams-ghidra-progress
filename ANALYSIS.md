# Dreams: decompilation results and findings

This is the written account behind the status map. The [research data](analysis/research-details.json) records failure addresses, saved signature corrections, proposed names, and matched property fields. [PROGRESS.md](PROGRESS.md) contains the applied naming ledger; [MAPPING.md](MAPPING.md) explains the system assignments.

## Current results

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

## Remaining work

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
