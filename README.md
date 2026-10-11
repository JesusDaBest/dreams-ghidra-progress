<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Analysis status](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/e8c7643d6b0be52c9cf4d2d8deaf633d83d6fb8a/assets/status-badges.svg)

**12 of 9,551 functions named and checked.** A function is one piece of the game's code.

![Dreams progress: identified functions and work still to review](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/e8c7643d6b0be52c9cf4d2d8deaf633d83d6fb8a/assets/status.svg)

**Green:** name checked. **Amber:** reviewed, still unclear. **Gray:** not reviewed yet.

The left map groups code by the labels already in the analysis project. Those labels still need checking. The right map contains code without descriptive labels. Every discovered function appears once; the two maps use different scales.

Code extraction produces computer-generated code to study. It does not mean that code has been understood or rebuilt.

## What we know so far

We have identified parts of the calculator, splitter and combiner tools, fog effects, object placement guides, and shared object data. These are early findings; the systems are still being investigated.

## Latest progress

- **12 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.

Next: study related functions together, identify their roles, and investigate the extraction failures. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
