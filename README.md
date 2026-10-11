# Dreams reverse engineering progress

This private repository records sanitized progress from a local Ghidra analysis of Dreams. Setup is verified and analysis is partial. The game has not been fully decompiled or reconstructed.

The imported starting analysis contains **9,551 functions**: **9,395** have default `FUN_` names and **156** have other names. These are baseline inventory counts, not a measure of verified understanding.

- [Progress and limitations](PROGRESS.md)
- [Function review and rename record](analysis/function-review.json)

The current naming batch contains two applied descriptive renames and six deferred functions. Both names were verified immediately through MCP and again after a clean stop and reopening of the saved project. A refreshed inventory contains 9,551 functions, including 9,393 default `FUN_` names. Existing meaningful names are preserved.

The input uses a PE wrapper around embedded PS4 code. The current Windows calling convention produces misleading parameter recovery for that code. Correct ABI handling must be established before broad signature, type, or interpretation changes.

This repository contains progress notes and analyst reasoning only. Game binaries, Ghidra databases, decompiled game code, raw dumps, private paths, personal identifiers, credentials, and authentication configuration remain outside it. The local MCP is restricted to loopback. Assistant-assisted analysis still involves model processing and is not described as fully offline.

Future updates should distinguish proposed changes from applied and verified changes, refresh coverage counts from the working project, and retain evidence and uncertainty for each conclusion.
