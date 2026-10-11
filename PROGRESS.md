# Progress

Status snapshot: 2026-10-11. Setup is verified; reverse engineering remains partial.

See [decompilation results and findings](ANALYSIS.md) for the consolidated analysis, including the later six-function signature promotion, the verified v2 snapshot and its separate extraction in progress, ReporterTelemetry's three applied and reopen-verified names, and the copy-only extraction experiments. The [research data](analysis/research-details.json) lists their recorded states, matched fields, and all 43 frozen-cache failure addresses. The older extraction and ABI counts below describe their specified v1 snapshot.

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
