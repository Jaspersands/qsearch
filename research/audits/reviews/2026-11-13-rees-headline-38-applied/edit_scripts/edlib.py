import sys
class Ed:
    def __init__(self, path):
        self.path = path; self.s = open(path).read(); self.log = []
    def r(self, tag, old, new):
        n = self.s.count(old)
        if n != 1:
            print('FAIL', tag, 'count', n); sys.exit(1)
        self.s = self.s.replace(old, new); self.log.append(tag)
    def save(self):
        open(self.path, 'w').write(self.s); print('applied', len(self.log), self.log)
