"""Wrapper around rcsearch (C) plus an independent certificate checker (pure Python,
classes by x^{(p-1)/D} against powers of xi^{(p-1)/D}, not by log tables)."""
import subprocess, json, os
from fp import least_primitive_root
HERE = os.path.dirname(os.path.abspath(__file__))

class ClassOracle:
    def __init__(self, p, D):
        self.p, self.D = p, D
        xi = least_primitive_root(p)
        z = pow(xi, (p - 1) // D, p)
        self.tab = {pow(z, i, p): i for i in range(D)}
        assert len(self.tab) == D
    def cl(self, x):
        return self.tab[pow(x % self.p, (self.p - 1) // self.D, self.p)]

def check_rc(p, D, R, K, alpha, beta):
    """beta: dict i -> value for i in R. Returns (ok, msg). Def. def:rc verbatim."""
    O = ClassOracle(p, D); K = set(k % D for k in K)
    if 0 not in R or 0 not in K: return False, "0 not in R or K"
    s = (alpha[0] + beta[0]) % p
    if s == 0 or O.cl(s) != 0: return False, "alpha0+beta0 not in P_D"
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0: continue
            if (O.cl(v) + i + j) % D not in K: return False, f"entry ({i},{j})"
    return True, "ok"

class RCSearch:
    def __init__(self, cache_path=None):
        self.proc = subprocess.Popen([os.path.join(HERE, "rcsearch")], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True, bufsize=1)
        self.cache_path = cache_path
        self.cache = {}
        if cache_path and os.path.exists(cache_path):
            with open(cache_path) as f: self.cache = json.load(f)
    def save(self):
        if self.cache_path:
            with open(self.cache_path, "w") as f: json.dump(self.cache, f)
    def query(self, p, D, R, K, mode, budget, seed=1):
        R = sorted(set(R)); K = sorted(set(K))
        self.proc.stdin.write(f"{p} {D} {mode} {budget} {seed} {len(R)} {' '.join(map(str,R))} {len(K)} {' '.join(map(str,K))}\n")
        line = self.proc.stdout.readline().strip()
        if line.startswith("FOUND"):
            a, b, _ = line[5:].split("|")
            alpha = list(map(int, a.split())); bl = list(map(int, b.split()))
            beta = dict(zip(R, bl))
            ok, msg = check_rc(p, D, R, K, alpha, beta)
            assert ok, (p, D, R, K, alpha, beta, msg)
            return "FOUND", (alpha, [beta[i] for i in R])
        if line.startswith("NONE"): return "NONE", None
        return "UNKNOWN", None
    def status(self, p, D, R, K, rtrials=200, ecap=2 * 10**7, exhaustive=True):
        """'FOUND'/'NONE'/'UNKNOWN' with caching; random first, then exhaustive."""
        key = f"{p}|{D}|{','.join(map(str,sorted(set(R))))}|{','.join(map(str,sorted(set(K))))}"
        c = self.cache.get(key)
        if c and (c[0] != "UNKNOWN" or not exhaustive): return c[0], c[1]
        st, cert = self.query(p, D, R, K, "r", rtrials, seed=p)
        if st != "FOUND": st, cert = self.query(p, D, R, K, "r", 300 * rtrials, seed=p + 7)
        if st != "FOUND" and exhaustive:
            st, cert = self.query(p, D, R, K, "e", ecap)
        self.cache[key] = [st, cert]
        return st, cert
