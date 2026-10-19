# inheritverdicts.py <ghidra dir> <verdict files>...: transferred names (hand comment "=SRC ...", SRC != own program)
# inherit the verdict given to the same name in SRC: CONFIRM clears "provisional", RENAME renames (plain new name if
# free in that file, else _2...). Own entries are applied by address with Pandemonium/tools/srprovapply.py first.
import sys, os, re, glob
g = sys.argv[1]; v = {}
for rf in sys.argv[2:]:
    for l in open(rf, encoding='utf-8', errors='replace'):
        f = l.split(None, 5)
        if len(f) >= 5 and f[3] in ('CONFIRM', 'RENAME') and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', f[4]):
            v[(f[0], f[2])] = (f[3], f[4])
for hf in sorted(glob.glob(os.path.join(g, 'hand_*.txt'))):
    prog = os.path.basename(hf)[5:-4]; lines = open(hf, encoding='utf-8').read().splitlines()
    used = set(l.split()[2] for l in lines if len(l.split()) > 2); out = []; c = r = 0
    for l in lines:
        f = l.split(' ', 4); m = re.match(r'=(\S+) ', f[4]) if len(f) > 4 else None
        a = v.get((m.group(1), f[2])) if m and m.group(1) != prog and 'provisional' in l else None
        if not a: out.append(l); continue
        rest = re.sub(r'\bprovisional\b:?\s*', '', f[4]).strip(); nn = f[2]
        if a[0] == 'RENAME' and a[1] != f[2]:
            nn = a[1]; k = 2
            while nn in used: nn = '%s_%d' % (a[1], k); k += 1
            used.discard(f[2]); used.add(nn); rest += ' (was %s)' % f[2]; r += 1
        else: c += 1
        out.append(' '.join([f[0], f[1], nn, f[3], rest]))
    open(hf, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    if c or r: print(prog, 'inherited confirm', c, 'rename', r)
