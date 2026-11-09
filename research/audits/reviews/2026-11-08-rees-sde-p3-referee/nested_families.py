"""NEST vs KOW on structured (non-uniform) instance families, n = 60, unlimited supply drawn from
the family; reports columns pulled.  Sampled evidence only: no worst-case claim."""
import numpy as np
from nested_sampler import Run

class FamRun(Run):
    def __init__(self, n, rng, mode, gen):
        super().__init__(n, rng, mode); self.gen = gen
    def pull(self, k):
        while len(self.pool) < k:
            self.stream.append(self.gen(len(self.stream)) % 3); self.pool.append(len(self.stream) - 1)

def families(n, rng):
    Bk = [rng.integers(0, 3, n) for _ in range(n // 2)]
    pool = [rng.integers(0, 3, n) for _ in range(2 * n + 1)]
    eye = np.eye(n, dtype=np.int64)
    def lowrank(i): return sum(int(c) * b for c, b in zip(rng.integers(0, 3, len(Bk)), Bk))
    def fewdistinct(i): return pool[i] if i < len(pool) else pool[rng.integers(0, len(pool))]
    def davenport(i): return eye[i // 2] if i < 2 * n else rng.integers(0, 3, n)
    def sparse(i):
        v = np.zeros(n, dtype=np.int64); pos = rng.choice(n, 2, replace=False); v[pos] = rng.integers(1, 3, 2); return v
    def signed(i): return eye[i // 3] * (1, 1, 2)[i % 3] if i < 3 * n else rng.integers(0, 3, n)
    def weight_n3(i):  # random vectors of weight n/3
        v = np.zeros(n, dtype=np.int64); pos = rng.choice(n, n // 3, replace=False); v[pos] = rng.integers(1, 3, n // 3); return v
    return dict(lowrank=lowrank, fewdistinct=fewdistinct, davenport_pad=davenport, sparse2=sparse,
                signed_blocks=signed, weight_n_over_3=weight_n3)

if __name__ == "__main__":
    rng = np.random.default_rng(3)
    n = 60
    for name in families(n, rng):
        out = {}
        for mode in ("kow", "nest"):
            ms = []
            for rep in range(3):
                fam = families(n, np.random.default_rng(100 + rep))[name]
                R = FamRun(n, np.random.default_rng(rep), mode, fam); R.run(); ms.append(len(R.stream))
            out[mode] = ms
        print(f"{name:16s} KOW {out['kow']}  NEST {out['nest']}   (n^2/4={n*n//4}, n^2/3={n*n//3})")
