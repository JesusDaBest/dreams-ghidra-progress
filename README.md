<div align="center">

# DREAMS
### Reverse engineering progress

Function discovery · Decompilation · Verified naming

![Analysis status](assets/status-badges.svg?v=015f859d7b4c)

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Dreams verified function names by address region](assets/status.svg?v=37a4b32760b0)

Each tile represents **one of the 9,551 discovered functions**. Green means its descriptive name is supported by evidence and verified after reopening; amber means a reviewed function remains unresolved; gray means unreviewed. Generating pseudocode does **not** turn a tile green.

Blocks group fixed **1 MiB address ranges**, with area proportional to function count. Labels such as `1404xxxxx` mean `0x140400000–0x1404fffff`; these are address regions, not identified game subsystems. Verified and deferred tiles come first within each region, followed by unreviewed addresses. The layout follows the [AnyPS5 progress-map approach](https://github.com/boykopovar/AnyPS5/blob/main/tools/progress.py), with an independently written generator and counting rules for this analysis.

The percentage measures verified naming among discovered functions. It does not measure whole-game completion, recovered original source, or complete behavioral understanding.

## Latest checkpoint

- **12 names verified** after saving and reopening. The documented batches cover property visitors and type/field registration routines. 4 other reviewed functions remain unresolved.
- **PS4 calling conventions:** 9,486 direct assignments plus 19 inherited thunk conventions, validated on a copy before updating the working project. Existing explicit signatures and the Windows wrapper are preserved.
- **Coverage pass:** 9,508 cached, 43 failed, and 0 pending out of 9,551 discovered functions. Extraction runs against an immutable snapshot; generated code remains local.

The cache retains its frozen analysis revision and original snapshot names. Verified naming reflects the saved working project. These are separate checkpoints; the status does not imply cached pseudocode contains every later rename.

Every discovered function received an extraction attempt. Bounded retries recovered 26 additional functions; remaining failures are 41 timeouts, 1 flow-limit failure, and 1 forced-merge failure. Successful cached outputs were not reprocessed, and all cached file hashes were checked.

## What comes next

Resolve remaining extraction failures, review coherent function clusters, and check signature and type questions against assembly. Existing annotations and decompiler output still require validation.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
