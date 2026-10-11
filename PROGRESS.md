# Progress

Status snapshot: 2026-10-10. Setup is verified; reverse engineering remains partial.

## Verified setup

- GhidraMCP 2.0 is available through a local, loopback-only MCP endpoint.
- The supplied Ghidra packed-program archive was imported into a persistent working project with auto-analysis disabled to preserve existing analysis.
- Function inventory, decompilation, and cross-reference queries were verified.
- A goal prompt defines the intended analysis and completion criteria.
- Original inputs and a separate preexisting project are retained outside this progress repository.
- Both applied names persisted after a clean service stop and reopening of the saved project. The supplied original archive and its imported input copy retained their original hashes.

## Baseline inventory

| Category | Count |
| --- | ---: |
| Functions in starting inventory | 9,551 |
| Default `FUN_` names | 9,395 |
| Other names | 156 |

The 156 other names include existing annotations or symbols; they are not 156 independently verified findings from this work. Inventory size does not establish complete function discovery or decompilation coverage.

After a clean stop and reopening, a fresh complete paginated inventory confirmed 9,551 functions, 9,393 default `FUN_` names, and 158 other names. The baseline above remains unchanged.

## Documented naming batch

Eight previously unnamed functions were inspected in and around the property-visitor cluster. Two descriptive renames were applied through MCP and verified by read-back both immediately and after reopening; six functions remain deferred because their precise roles are not sufficiently established.

| Address | Original name | Applied name | Recorded state |
| --- | --- | --- | --- |
| `1404d7ef0` | `FUN_1404d7ef0` | `VisitCalculatorProperties` | Applied; verified immediately and after reopening |
| `1404d6660` | `FUN_1404d6660` | `VisitFogProperties` | Applied; verified immediately and after reopening |

The calculator visitor references `CalculatorOp`, `CalculatorUnits`, `OperandA`, and `OperandB`. The fog visitor references `FogShapeType`. Both are called by the existing Thing property dispatcher and follow its property-callback pattern. These are analyst-assigned behavior names, not recovered original source names. Detailed evidence, original names, and verification status are in `analysis/function-review.json`.

For this documented batch: 8 reviewed, 2 renamed and verified after reopening, 6 deferred, and 0 decompilation failures observed. The eight saved candidate decompilations were untruncated. A complete per-address coverage report does not yet exist; global reviewed, unresolved, failed, and pending totals must not be inferred from these batch counts.

## ABI and mapping limitation

The supplied analysis reports a Windows PE wrapper containing `.elf` sections. A sample of 1,664 code bytes matched the PS4 SELF reference with a PE address mapping offset of `0x140010000`. This is sampled evidence, not a full-binary equivalence proof.

The active Windows ABI is unsuitable for the embedded PS4 functions: decompilation shows unrecovered `RDI`/`RSI` inputs. This can distort parameter lists, return values, call arguments, and inferred types. No broad prototype or calling-convention correction is claimed here. The two applied names rely on explicit labels and control-flow relationships instead of inferred signatures.

## Next work

1. Establish and validate ABI treatment for representative embedded PS4 functions while distinguishing wrapper code.
2. Build an address-based coverage index and process coherent function clusters with cached evidence.
3. Journal and verify further justified changes, save checkpoints, and recheck original input hashes.

Setup, a small naming batch, and generated pseudocode do not satisfy the full reverse engineering goal.
