"""Turn the warnings of a compile of formal/Formal/BCHClassSevenSubgroups.lean
(`lake env lean` or `lake build` output) into lint7.json for gen_subgroups7.py:
which NeZero instances a lemma must `omit`, which lemmas `simp` closes alone
('closes'), and which need no final `ring` ('noring'). Usage: lint7.py LOG"""
import json, re, sys, os
LEAN = '/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassSevenSubgroups.lean'
lines = open(LEAN).read().split('\n')
def owner(ln):
    for i in range(ln - 1, -1, -1):
        m = re.match(r'theorem (\S+)', lines[i])
        if m:
            return m.group(1)
log = open(sys.argv[1]).read()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lint7.json')
lint = {}
pat = re.compile(r'(?:warning: )?Formal/BCHClassSevenSubgroups\.lean:(\d+):\d+: warning: (.*?)(?=\n(?:warning: )?Formal/|\n\t|\Z)', re.S)
for m in pat.finditer(log):
    ln, msg = int(m.group(1)), m.group(2)
    if 'automatically included section variable' in msg:
        name = re.search(r'QSearch\.BCHClassSevenSubgroups\.([A-Za-z0-9_]+)', msg).group(1)
        qs = re.findall(r'^\s*\[NeZero \(?(\d)', msg, re.M)
        e = lint.setdefault(name, {})
        e['omit'] = sorted(set(e.get('omit', [])) | set(qs))
    elif '`all_goals match_scalars` does nothing' in msg:
        lint.setdefault(owner(ln), {})['closes'] = True
    elif '`all_goals ring` does nothing' in msg:
        lint.setdefault(owner(ln), {})['noring'] = True
    elif 'does nothing' in msg or 'never executed' in msg:
        pass  # companions of the two cases above
    else:
        print('UNHANDLED', ln, msg[:200])
for e in lint.values():
    if e.get('closes'):
        e.pop('noring', None)
json.dump(lint, open(path, 'w'), indent=1, sort_keys=True)
print(len(lint), 'entries', sum(1 for e in lint.values() if e.get('closes')), 'closes',
      sum(1 for e in lint.values() if e.get('noring')), 'noring')
