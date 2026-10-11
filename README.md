<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Analysis status](assets/status-badges.svg?v=10cd8d02b13d)

**27 of 9,551 functions named and checked.** A function is one piece of the game's code.

![Dreams progress: function names checked and code extraction](assets/status.svg?v=8cafc8a350e1)

**Left:** green means a function's name has been checked; amber means its role is still unclear. **Right:** blue means computer-generated code is available to study; amber means extraction needs work. Gray means that step is unfinished.

Both maps show all 9,551 discovered functions in the same order and at the same scale. Each square is one function. System boundaries are still being investigated, so these maps do not estimate the size, complexity, or completion of individual game systems.

Code extraction produces computer-generated code to study. It does not mean that code has been understood or rebuilt.

## What we know so far

We have identified routines that describe and read properties for calculator, splitter, combiner and signal gadgets, doorways, camera shake, controller rumble, fog, placement guides, and shared object data. The code that drives these systems is still being investigated.

## Latest progress

- **27 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.

Next: study related functions together, identify their roles, and investigate the extraction failures. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
