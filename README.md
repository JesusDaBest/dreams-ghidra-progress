<div align="center">

# DREAMS
### Reverse engineering progress

Working out how Dreams works, one piece of code at a time

[Research findings](ANALYSIS.md) Â· [Progress log](PROGRESS.md) Â· [Mapping evidence](MAPPING.md) Â· [Function review](analysis/function-review.json) Â· [Status data](analysis/status.json)

</div>

## Status

![Analysis status](assets/status-badges.svg?v=6ade5d09bdb5)

<!-- status-summary:start -->
**27 of 9,551 functions named and checked.** A function is one piece of the game's code.
<!-- status-summary:end -->

![Dreams code extraction and name checking by system](assets/status.svg?v=91f0395de753)

**Left: code extracted. Right: names checked.** Both maps show the same functions grouped by the part of Dreams they support. Blue means computer-generated code is available to study; green means a descriptive name has been checked. Amber needs follow-up; gray means that step is unfinished.

**Section size counts code identified so far, not the full size of that Dreams system.** Sculpting may look small because much of its code has not been identified yet. Neither map measures a finished or rebuilt game.

<!-- area-status:start -->
| Part of Dreams | Functions mapped | Code extracted | Names checked |
| --- | ---: | ---: | ---: |
| Sculpting & painting | 117 | 117 / 117 | 0 / 117 (0.0%) |
| Gadgets & logic | 450 | 450 / 450 | 22 / 450 (4.9%) |
| Physics & collision | 60 | 60 / 60 | 0 / 60 (0.0%) |
| Sound & music | 62 | 62 / 62 | 0 / 62 (0.0%) |
| Animation & puppets | 47 | 46 / 47 | 0 / 47 (0.0%) |
| Rendering & lighting | 275 | 274 / 275 | 0 / 275 (0.0%) |
| Editor & interface | 313 | 313 / 313 | 0 / 313 (0.0%) |
| Dreamiverse & networking | 103 | 100 / 103 | 0 / 103 (0.0%) |
| Shared engine & object data | 113 | 108 / 113 | 5 / 113 (4.4%) |

**1,540 of 9,551 discovered functions are mapped; 8,011 still need a system assignment.** Percentages measure checked names among the functions mapped to that section. The complete size of each system is still unknown; these are not whole-game completion percentages.
<!-- area-status:end -->

<sub>Automatic extraction has produced code for 9,508 functions in the previous analysis snapshot; 43 still need fixes. This is preparation for research, not verified or rebuilt game code. See the [progress log](PROGRESS.md).</sub>

## What we know so far

**The full written findings are in [Dreams: decompilation results and findings](ANALYSIS.md).** They cover the executable and calling convention, shared property types, gadget field matches, object dispatch, saved signature corrections, proposed names, and extraction experiments. The [supporting research data](analysis/research-details.json) includes all 43 failed addresses and 77 matched property fields.

The map connects code to sculpting and painting, gadgets, physics, audio, animation, rendering, the editor, the Dreamiverse, and shared engine data. Assignments come from references in the machine code, registered types, and the game's object-type dispatcher. Every assignment has an address and supporting evidence in the [system map](analysis/system-map.json).

So far, checked names cover gadget property readers and registrations plus shared object helpers. Mapping a function to a system is a separate step from understanding its behavior and checking its name. See [how the mapping is established](MAPPING.md).

## Latest progress

- **27 functions named and checked.** Another 4 have been reviewed but remain unclear.
- **9,508 functions have computer-generated code ready to study.** Generating that code is preparation; it does not mean we understand it yet.
- **43 functions need extraction fixes.** Every one of the 9,551 functions found so far received an attempt.
- **Six field-registration signatures were corrected, saved, and verified through native reopen checks.** A newer snapshot preserves those corrections and all 27 names; its extraction cache has not been started. Separate live MCP verification remains pending.
- **Three ReporterTelemetry names have supporting reviews but have not been applied.** A copy-only flow-limit experiment also produced pseudocode, then was rolled back because its switch domain still needs proof. These outcomes are documented separately from completed work in the [findings](ANALYSIS.md).

Next: extend the system mapping and review the functions within each section. The [progress log](PROGRESS.md) holds the technical evidence and limitations.

## Repository scope

This public repository contains sanitized progress, review metadata, and status graphics. Game binaries, Ghidra databases, decompiled game code, local paths, credentials, and logs remain outside it. The analysis is incomplete; full source reconstruction is not claimed.
