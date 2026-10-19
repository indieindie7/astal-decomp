# lrown.py <lr dir> <out dir>: keep only the review entries a program owns: header comment without a =SRC tag,
# or whose =SRC tag names the program itself (transferred copies inherit the verdict of their source).
import os, re, sys
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); tot = kept = 0
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.txt'): continue
    parts = re.split(r'(?m)^(?=#### )', open(os.path.join(src, fn), encoding='utf-8', errors='replace').read())
    keep = [parts[0]]
    for e in parts[1:]:
        m = re.match(r'#### (\S+) 0x[0-9a-fA-F]+ \S+ \| (?:=(\S+) )?', e); tot += 1
        if m.group(2) is None or m.group(2) == m.group(1): keep.append(e); kept += 1
    if len(keep) > 1: open(os.path.join(out, fn), 'w', encoding='utf-8', newline='\n').write(''.join(keep))
    print(fn, len(keep) - 1)
print('total', tot, 'kept', kept)
