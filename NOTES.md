# Astal decomp notes (names + notes only; no game data)

## Disc (2026-10-17)
- US release MK-81019 V1.003, own copy, 2 tracks (track 1 data, track 2 CDDA). Extracted with a 2352-byte-sector ISO reader: 267 files.
- IP header: first read address 0x060b0000, IP size 0x8000. Boot program = A0SYS.BIN (285,616 bytes).
- Per-round overlays R<nn>.BIN (R11..R14, R19, R21..R24, R29, R31, R33, R39, R41..R43, R49, R51, R53, R64, R91, R94..R97; 230-372 KB each) + R14BOSS.BIN, R64BOSS.BIN. R19 / R29 / R39 / R49 are the same 234,086-byte demo stub (one program, R19, stands for all four). Data per round: R<nn>ASS.SCL, NBG<n>.SCL, RBG0.SCL, SCLMP.BIN, ENECG.BIN (enemy graphics), SE.SND / SEQ.SND. Other code: APT.BIN, BPT.BIN, CPT.BIN, TIT.BIN.
- Load bases (`tools/basefind.py` + `tools/basechk.py`, big-endian pointer histograms with prologue scoring): A0SYS.BIN at 0x060b0000 (284 pointer entries / 595 hits, next best 44); every R<nn>.BIN at 0x06002000 (157-262 entries each; R11: 226 / 756, next best 51); APT / BPT / CPT also at 0x06002000 (49-54 entries, small code). So the round overlays load below the resident system module.

## Ghidra (12.1.4)
- BinaryLoader, SuperH:BE:32:SH2; `FindSh2FunctionsMem.java` prologue scan + `CreateAt.java`, then `CsDumpAll.java` for the decompile dump. A0SYS 744 functions; the R overlays 198-312 each; APT 169, BPT 133. 25 programs in all (A0SYS, APT, BPT, 22 R overlays with R19 standing for the four demo stubs).

## Naming round 1 (2026-10-17)
- A0SYS: `decprep.py` slices, one naming agent per slice with `ghidra/naming/prompt_A0SYS.txt` (every name from reading the code and strings, never from a script), `decmerge.py` merge: 736 named, 3 leftovers named in a second small pass.
- Round overlays share most of their code (the per-round engine is linked into each overlay). R11 was named first (`ghidra/naming/prompt_R.txt`, 260 names), then `tools/dectransfer.py` carried names to identical functions in the other overlays (matched by code bytes with the call targets masked); the leftovers of R14 / R51 / R95 / R53 were named by hand and transferred again; the last four shared functions that every overlay gained after the apply (sizes 520 / 692 / 6 / 118) were named once and transferred with MASK=1. APT / BPT: small passes of their own.
- Result (applied + re-exported): all 25 programs, 0 FUN_ anywhere; 5,213 hand-name lines, 6,422 functions; provisional A0SYS 209, R overlays 79-144 each, APT 7, BPT 5.

## Review round 1 (2026-10-17 .. 10-18)
- `tools/ckprovctx.py` writes one context per provisional function (its decompile plus up to three callers); `lrown.py` / `lrdedupe.py` collapse the overlays' shared functions so each is reviewed once, `inheritverdicts.py` copies a verdict to the same function in the other overlays. A local model answers one verdict line each with `ghidra/review/prompt_r1_astal.txt`: `<PROG> 0x<addr> <old> CONFIRM|RENAME|UNSURE <new> <reason>`.
- A0SYS done and applied (`tools/srprovapply.py`): confirmed 178, renamed 23, unsure 8; re-applied and re-exported: 744 functions, 0 FUN_, 8 provisional.
- The overlay review (R11 plus the two shared-function groups) is queued; its verdicts will be inherited by all overlays and pushed as round 2.

## Next
- Round 2: apply the overlay verdicts (R11 and the shared groups, inherited to R12..R97), re-export, push. Then CPT.BIN / TIT.BIN (title and credits), R14BOSS / R64BOSS, and the A0SYS to overlay call table (how the system module enters a round).
