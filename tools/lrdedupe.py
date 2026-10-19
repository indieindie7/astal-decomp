# lrdedupe.py <lr dir> <out dir>: keep one review entry per identical function body (name + decompile text with
# addresses masked); writes <out>/<file> with unique entries and <out>/dups.tsv (PROG addr name -> canonical PROG addr).
import os, re, sys, hashlib
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
seen = {}; dups = []; total = kept = 0
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.txt'): continue
    text = open(os.path.join(src, fn), encoding='utf-8', errors='replace').read()
    parts = re.split(r'(?m)^(?=#### )', text); head = parts[0]; keep = [head]
    for e in parts[1:]:
        m = re.match(r'#### (\S+) (0x[0-9a-fA-F]+) (\S+)', e); total += 1
        body = e.split('---- callers', 1)[0]; body = body[body.find(chr(10)) + 1:]
        key = hashlib.md5((m.group(3) + re.sub(r'0x0?6[0-9a-fA-F]{6}|_0?6[0-9a-fA-F]{6}|FUN_[0-9a-fA-F]+', '@', body)).encode()).hexdigest()
        if key in seen: dups.append((m.group(1), m.group(2), m.group(3)) + seen[key]); continue
        seen[key] = (m.group(1), m.group(2)); keep.append(e); kept += 1
    if len(keep) > 1: open(os.path.join(out, fn), 'w', encoding='utf-8').write(''.join(keep))
open(os.path.join(out, 'dups.tsv'), 'w').write(''.join('%s %s %s %s %s\n' % d for d in dups))
print('entries', total, 'unique', kept, 'dups', len(dups))
