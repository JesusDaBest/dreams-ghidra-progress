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
