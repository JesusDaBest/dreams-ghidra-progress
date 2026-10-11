# Dreams: decompilation results and findings

This is the written account behind the status map. The [research data](analysis/research-details.json) records failure addresses, saved signature corrections, proposed names, and matched property fields. [PROGRESS.md](PROGRESS.md) contains the applied naming ledger; [MAPPING.md](MAPPING.md) explains the system assignments.

## Current results

| Work | Recorded result |
| --- | --- |
| Function inventory | 9,551 discovered functions |
| Frozen v1 extraction | 9,508 functions with cached C-like pseudocode; 43 failures |
| Applied descriptive names | 27, verified after reopening the project |
| Deferred naming reviews | 4 |
| Additional naming proposals | 3 ReporterTelemetry names; reviewed but not applied |
| System mapping | 1,540 functions associated with nine systems; 8,011 still unclassified |
| Saved signature corrections | Six field-registration helpers; native reopen checks passed |
| Newer v2 snapshot | Verified copy with the six corrections and all 27 names; separate extraction is in progress |

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

The newer verified snapshot contains these changes. Its separate v2 cache is now being extracted in resumable, read-only batches. The first completed batch recorded 2,994 complete outputs, 14 failures, and 6,543 pending functions; later batches are continuing. The 9,508 cached outputs and the system map still refer to the coherent older v1 snapshot, rather than mixing results from the two versions.

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

## ReporterTelemetry: reviewed proposals

| Address | Proposed name | State |
| --- | --- | --- |
| `1404de8c0` | `VisitReporterTelemetryProperties` | Not applied |
| `140d6c700` | `RegisterReporterTelemetryFieldOffsets` | Not applied |
| `140d580d0` | `RegisterReporterTelemetryTypeDescriptor` | Not applied |

An exact ReporterTelemetry literal is installed on descriptor `1458afdd0`. The initializer links the Thing base descriptor and transfers to the field registrar. All 14 registered fields match the independently inspected visitor, including six TelemetryKey fields at `+0xe0` through `+0x108`, and TimeSinceSend at `+0x110`. Dispatcher tag `0x51` corroborates the identity.

The extension fields are guarded by a visitor-state value of at least `0x1869f` (99,999), with additional filtering conditions. The meaning and normal reachability of that threshold are unresolved. This review establishes property roles; it does not establish transmission behavior, recipients, payloads, or a reporting algorithm. The three proposals are not counted among the 27 applied, reopen-verified names.

## Extraction failures and experiments

The frozen cache has 41 timeouts, one flow-limit failure at `1401180e0`, and one forced-merge failure at `14146b220`. Every failed address, body size, and attempt count is listed in [research-details.json](analysis/research-details.json).

For `1401180e0`, a disposable-copy experiment expanded the analyzed body and supplied candidate switch references. It produced pseudocode successfully. Fifty table entries had local targets, but the byte selector permits values up to 255 and no explicit upper-bound guard was established. The legal selector domain therefore remains uncertain. The experiment was rolled back and was not promoted as a production fix; the frozen failure count remains 43.

For `14146b220`, normalization succeeded and exposed intermediate control-flow information. That mode does not produce extracted C. A separate full-decompilation attempt with array splitting disabled still failed with the forced-merge intersection error and produced no C output. Both experiments left the production cache unchanged.

An earlier mechanical quality scan inspected 9,482 outputs while extraction was still in progress. It flagged warnings, indirect calls, unresolved register inputs, and SIMD-call outputs as review leads. Its counts are not a final audit of all 9,508 cached outputs and are not semantic-review credit. The completed extraction integrity audit separately checked all 9,508 cached file hashes and the full 9,551-address inventory.

## Remaining work

The main open work is to finish the coherent cache from the newer signature-corrected snapshot, resolve the recorded extraction failures, extend the code-to-system map, and review the functions within those systems. Proposed names must be applied and checked after reopening before they receive applied-name credit. Full signatures, layouts, and algorithms need their own evidence.

The public files contain findings and structural evidence. Raw pseudocode, binary inputs, Ghidra projects, and unfiltered local reports are retained separately. That separation does not reduce the extraction counts or mean the locally saved work was undone.
