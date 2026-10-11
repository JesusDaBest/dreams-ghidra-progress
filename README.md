<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Progress log](PROGRESS.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Analysis status](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/3bac5130ebed0df3b5bb34ea62fe2e82ba31bf1a/assets/status-badges.svg)

<!-- status-summary:start -->
**27 of 9,551 functions named and checked.** A function is one piece of the game's code.
<!-- status-summary:end -->

![Dreams function review by verified system assignment](assets/status.svg?v=e55b3a4cf236)

**Each cell represents one discovered function.** Green means its name has been checked; amber means reviewed but unresolved; gray means not reviewed. Every section's area comes from the number of functions assigned to it. Functions without an established system belong to **Unassigned**.

<!-- area-status:start -->
| Part of Dreams | Functions assigned so far | Names checked | System completion |
| --- | ---: | ---: | --- |
| Sculpting & creation | 0 | 0 | Unknown |
| Gadgets & logic | 22 | 22 | Unknown |
| Rendering & lighting | 0 | 0 | Unknown |
| Physics & movement | 0 | 0 | Unknown |
| Sound & music | 0 | 0 | Unknown |
| Puppets & animation | 0 | 0 | Unknown |
| Interface & controls | 0 | 0 | Unknown |
| Shared object data | 5 | 5 | Unknown |

**9,524 of 9,551 functions have no verified system assignment yet.** A zero above means none assigned so far; the system's actual function count is unknown.
<!-- area-status:end -->

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
