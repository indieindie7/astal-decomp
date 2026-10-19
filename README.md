# Astal (Sega Saturn, Sega 1995) reverse-engineering notes and symbols

Hand-named function maps, review inputs and tools for **Astal** (MK-81019, US release, SH-2), the 2D
platformer with the big grab-and-throw hero. Round 1 (one naming pass over every function in all 25 programs,
then a review of the system module's provisional names with their callers):

| Program | Functions | Hand-named | Still `provisional` |
|---|---|---|---|
| A0SYS.BIN (system module at 0x060b0000) | 744 | 739 (5 are shared stubs) | 8 |
| 23 round overlays R11..R97 (at 0x06002000, one per round / boss) | 5,383 | 4,172 (names transferred between overlays that share code) | 2,074 |
| APT.BIN, BPT.BIN (small helpers at 0x06002000) | 295 | 302 lines (169 + 133) | 12 |

Totals: 6,422 functions, 5,213 hand-name lines, 0 placeholders left, 2,094 still marked provisional
(the overlay review with callers is queued and will be pushed as round 2).

Subsystems named so far, system module: Sega GFS / CDC file system and streaming (`gfs_`, `cd_`, `cdc_`,
`cdbuf_`, `stream_`, `tilestream_`, `mapstream_`), VDP1 / VDP2 / SCU setup and DMA (`vdp1_`, `vdp2_`, `scu_`),
sound (`snd_`), splines and maths (`spline_`, `math_`), palette fades (`palfade_`), pad (`pad_`), actors, objects
and collision (`actor_`, `obj_`, `collide_`, `map_`), GCC runtime (`gcc_`). Round overlays: scene scripts and
round flow (`scene_`, `round_`), enemies and bosses (`enemy_`, `boss_`), the player (`player_`, `leda_`),
objects, items and effects (`obj_`, `item_`, `effect_`, `sprite_`), collision (`collide_`), menus and debug
(`menu_`, `debug_`).

Same method as [threedirtydwarves-decomp](https://github.com/indieindie7/threedirtydwarves-decomp) and
[clockworkknight-decomp](https://github.com/indieindie7/clockworkknight-decomp): load bases by pointer
histogram, functions by SH-2 prologue scan, a decompile dump cut into slices, each slice named from its code
and strings (prompts in `ghidra/naming/`), names deduplicated and transferred to the overlays that share the same
code (`tools/dectransfer.py`), applied as USER_DEFINED labels, then every provisional name re-read with its
callers by a local model (prompt in `ghidra/review/`, verdicts applied with `tools/srprovapply.py`).
Non-commercial, done for study and preservation (platformer / grab-and-throw design reference).

**No game data is included**: no disc image, no executables, no overlays, no decompiled C, no game text,
no Ghidra database. You need your own copy of the game to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | disc layout, load bases, Ghidra setup, the naming round, the review round, what comes next |
| `ghidra/hand_<prog>.txt` | hand names per program: `0x<addr> func <name> hand <comment>` (A0SYS, APT, BPT, R11..R97; apply with ApplyNames.java from the Scorcher / AMOK repos, hand mode) |
| `ghidra/funcinfo_<prog>.tsv` | per-function export: `F` address name source size, `C` callees (string rows removed) |
| `ghidra/naming/` | the round-1 naming prompts (system module, round overlays) |
| `ghidra/review/prompt_r1_astal.txt` | the provisional-review prompt |
| `ghidra/scripts/` | `FindSh2FunctionsMem.java` (SH-2 prologue scan in a raw image), `CreateAt.java`, `CsDumpAll.java` (decompile dump with headers) |
| `tools/` | `basefind.py` + `basechk.py` (load bases), `decprep.py` / `decmerge.py` (slice and merge), `dectransfer.py` (carry names between overlays with identical code), `ckprovctx.py` (review contexts with callers), `lrown.py` / `lrdedupe.py` / `inheritverdicts.py` (review bookkeeping across overlays), `srprovapply.py` (apply verdicts), `pubfuncinfo.py` |

## Licence

Notes, names and tools: MIT (see `LICENSE`). Astal belongs to Sega; nothing from the game is distributed here.
