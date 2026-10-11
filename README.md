<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Progress log](PROGRESS.md) · [Mapping evidence](MAPPING.md) · [Function review](analysis/function-review.json) · [Status data](analysis/status.json)

</div>

## Status

![Analysis status](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/3217cde4c680cf7e9b321b123ccd8fd9c269a5e0/assets/status-badges.svg)

<!-- status-summary:start -->
**27 of 9,551 functions named and checked.** A function is one piece of the game's code.
<!-- status-summary:end -->

![Dreams function review by verified system assignment](https://raw.githubusercontent.com/JesusDaBest/dreams-ghidra-progress/3217cde4c680cf7e9b321b123ccd8fd9c269a5e0/assets/status.svg)

**Each cell is one function mapped to that part of Dreams.** Green means its name has been checked; amber means reviewed but unresolved; gray means not reviewed. Section sizes come from actual mapped function counts. More complex systems may still have fewer mapped functions while their code is being identified.

<!-- area-status:start -->
| Part of Dreams | Functions mapped | Names checked |
| --- | ---: | ---: |
| Sculpting & painting | 117 | 0 / 117 (0.0%) |
| Gadgets & logic | 450 | 22 / 450 (4.9%) |
| Physics & collision | 60 | 0 / 60 (0.0%) |
| Sound & music | 62 | 0 / 62 (0.0%) |
| Animation & puppets | 47 | 0 / 47 (0.0%) |
| Rendering & lighting | 275 | 0 / 275 (0.0%) |
| Editor & interface | 313 | 0 / 313 (0.0%) |
| Dreamiverse & networking | 103 | 0 / 103 (0.0%) |
| Shared engine & object data | 113 | 5 / 113 (4.4%) |

**1,540 of 9,551 discovered functions are mapped; 8,011 still need a system assignment.** Percentages measure checked names among the functions mapped to that section. The complete size of each system is still unknown; these are not whole-game completion percentages.
<!-- area-status:end -->

<sub>Automatic extraction has produced code for 9,508 functions in the previous analysis snapshot; 43 still need fixes. This is preparation for research, not verified or rebuilt game code. See the [progress log](PROGRESS.md).</sub>

## What we know so far

The map connects code to sculpting and painting, gadgets, physics, audio, animation, rendering, the editor, the Dreamiverse, and shared engine data. Assignments come from references in the machine code, registered types, and the game's object-type dispatcher. Every assignment has an address and supporting evidence in the [system map](analysis/system-map.json).

So far, checked names cover gadget property readers and registrations plus shared object helpers. Mapping a function to a system is a separate step from understanding its behavior and checking its name. See [how the mapping is established](MAPPING.md).

## Latest progress

- **27 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.

Next: extend the system mapping and review the functions within each section. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
