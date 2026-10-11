<div align="center">

# DREAMS
### Reverse engineering progress

Function discovery · Decompilation · Verified naming

![Analysis status](assets/status-badges.svg?v=6dd0adde6dd8)

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Dreams function coverage: cached pseudocode, semantic review, and calling conventions](assets/status.svg?v=c2984731fbf3)

Each square represents **one of the 9,551 functions currently discovered**. Squares with the same status sit together in labeled blocks, with an exact count above each block. The grids show a measured snapshot of this analysis, not a percentage of the entire game recovered. Cached pseudocode and verified understanding are counted separately.

## Latest checkpoint

- **9 names verified** after saving and reopening, including Calculator, Fog, Pos, CanvasProperties, Variant, GadgetName visitors, and Variant field registration. 4 other reviewed functions remain unresolved.
- **PS4 calling conventions:** 9,486 direct assignments plus 19 inherited thunk conventions, validated on a copy before updating the working project. Existing explicit signatures and the Windows wrapper are preserved.
- **Coverage pass:** 9,482 cached, 69 failed, and 0 pending out of 9,551 discovered functions. Extraction runs against an immutable snapshot; generated code remains local.

The cache retains its frozen analysis revision and original snapshot names. Verified naming reflects the saved working project. These are separate checkpoints; the status does not imply cached pseudocode contains every later rename.

## What comes next

Resolve remaining extraction failures, review coherent function clusters, and check signature and type questions against assembly. Existing annotations and decompiler output still require validation.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
