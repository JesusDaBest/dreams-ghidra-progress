<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

![Analysis status](assets/status-badges.svg?v=ba5973a02e75)

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Dreams progress: identified functions and work still to review](assets/status.svg?v=97df6acfb290)

**Green means we have identified what a function does, given it a descriptive name, and checked that the saved name is correct.** Amber means we have reviewed it but still have questions. Gray means it has not been reviewed. A function is one piece of the game's code.

The square-based display takes inspiration from [AnyPS5's progress map](https://github.com/boykopovar/AnyPS5/blob/main/tools/progress.py). Our figures measure work on the functions found so far—not how much of the entire game has been rebuilt.

## What we know so far

We have identified parts of the calculator, splitter and combiner tools, fog effects, object placement guides, and shared object data. These are early findings; the systems are still being investigated.

## Latest progress

- **12 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.

Next: study related functions together, identify their roles, and investigate the extraction failures. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
