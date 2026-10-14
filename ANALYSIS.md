# Dreams: decompilation results and findings

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
