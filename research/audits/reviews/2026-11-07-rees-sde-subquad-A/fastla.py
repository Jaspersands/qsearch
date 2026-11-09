"""Small exact linear algebra over F_p with an incremental reduced echelon basis.
Used only for speed; forward_fast in subquad.py is cross-checked against q1core.forward."""


class Ech:
    """Reduced row echelon basis of a subspace of F_p^a.  Each row carries a tag vector
    (dict index -> coefficient) recording it as a combination of tagged generators."""

    def __init__(self, p, a):
        self.p, self.a = p, a
        self.rows = []      # (pivot, vec, tag)

    def copy(self):
        e = Ech(self.p, self.a)
        e.rows = [(pv, list(v), dict(t)) for pv, v, t in self.rows]
        return e

    def __len__(self):
        return len(self.rows)

    def reduce(self, v, track=False):
        p = self.p
        v = [x % p for x in v]
        co = {}
        for pv, row, tag in self.rows:
            f = v[pv]
            if f:
                for t in range(self.a):
                    if row[t]:
                        v[t] = (v[t] - f * row[t]) % p
                if track:
                    for k, x in tag.items():
                        co[k] = (co.get(k, 0) + f * x) % p
        return v, co

    def contains(self, v):
        r, _ = self.reduce(v)
        return not any(r)

    def add(self, v, tag=None):
        """Add v (with tag = its expression in generators); returns False if dependent."""
        p = self.p
        r, co = self.reduce(v, track=tag is not None)
        if not any(r):
            return False
        pv = next(t for t in range(self.a) if r[t])
        iv = pow(r[pv], p - 2, p)
        r = [x * iv % p for x in r]
        if tag is not None:
            # row = (v - sum co) / r[pv]  as a combination of generators
            nt = {k: x for k, x in tag.items()}
            for k, x in co.items():
                nt[k] = (nt.get(k, 0) - x) % p
            nt = {k: x * iv % p for k, x in nt.items() if x * iv % p}
        else:
            nt = {}
        # eliminate pv from existing rows
        new = []
        for q, row, tg in self.rows:
            f = row[pv]
            if f:
                row = [(x - f * y) % p for x, y in zip(row, r)]
                tg = dict(tg)
                for k, x in nt.items():
                    tg[k] = (tg.get(k, 0) - f * x) % p
            new.append((q, row, tg))
        new.append((pv, r, nt))
        self.rows = new
        return True


def rank_vecs(vecs, p, a):
    e = Ech(p, a)
    return sum(1 for v in vecs if e.add(v))
