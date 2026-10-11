<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Analysis status](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/3bac5130ebed0df3b5bb34ea62fe2e82ba31bf1a/assets/status-badges.svg)

**27 of 9,551 functions named and checked.** A function is one piece of the game's code.

![Dreams research by game system](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/3bac5130ebed0df3b5bb34ea62fe2e82ba31bf1a/assets/status.svg)

**Green square = one checked function name. Gray grid = unmapped research space.** All gadget families stay together in the right-hand map. Checked names currently describe properties and registration; no whole gadget or system is marked finished.

**9,524 functions still need an area assignment.** System totals are unknown, so the maps show checked counts, not completion percentages. Section sizes are layout choices; gray squares do not stand for a measured number of remaining functions.

<sub>Automatic extraction has produced code for 9,508 functions in the previous analysis snapshot; 43 still need fixes. This is preparation for research, not verified or rebuilt game code. See the [progress log](PROGRESS.md).</sub>

## What we know so far

We have identified routines that describe and read properties for calculator, splitter, combiner and signal gadgets, doorways, camera shake, controller rumble, fog, placement guides, and shared object data. The code that drives these systems is still being investigated.

## Latest progress

- **27 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.

Next: study related functions together, identify their roles, and investigate the extraction failures. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
