"""Certificate search and independent checking for RC(D; R -> K) contractions.
AI-written 2026-11-13, pending human review.  Finite computation.

* search: rcrand.c (random beta, column scans; this folder) and, for p <= 12000, the complete DFS
  rcdfs.c of 2026-11-13-rees-k9-bottleneck (imported read-only through its rc.py wrapper);
* check: check_rc below, written from the definition, with classes computed by exponentiation
  x^((p-1)/D) compared with powers of g^((p-1)/D); no discrete-log table, no shared code with the
  search programs.  Every certificate used anywhere is passed through check_rc.
Classes are taken w.r.t. the least primitive root g of p (a coset generator for every D | p-1)."""
import ctypes, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
_lib = ctypes.CDLL(os.path.join(HERE, 'librcrand.so'))
_lib.rc_random.restype = ctypes.c_int
_lib.rc_random.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                           ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_longlong, ctypes.c_ulonglong,
                           ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
_rc = None


def rc_dfs():
    global _rc
    if _rc is None:
        sys.path.insert(0, os.path.join(HERE, '..', '2026-11-13-rees-k9-bottleneck'))
        import rc as _m
        _rc = _m
    return _rc


def factor_set(n):
    s, d = set(), 2
    while d * d <= n:
        while n % d == 0: s.add(d); n //= d
        d += 1
    if n > 1: s.add(n)
    return s


_PR = {}
def prim_root(p):
    if p in _PR: return _PR[p]
    fs = factor_set(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            _PR[p] = g; return g
    raise ValueError(p)


def cls_of(x, p, g, D):
    """class of x in F_p^* modulo D w.r.t. g: the c in [0,D) with x^((p-1)/D) = (g^((p-1)/D))^c."""
    assert x % p != 0 and (p - 1) % D == 0
    z = pow(g, (p - 1) // D, p); y = pow(x, (p - 1) // D, p); t = 1
    for c in range(D):
        if t == y: return c
        t = t * z % p
    raise AssertionError('class not found')


def check_rc(p, g, D, R, K, alpha, beta):
    """RC(D; R -> K): alpha_0+beta_0 nonzero of class 0; each cell alpha_j+beta_i (i in R, j in Z_D)
    zero or of class c with (c+i+j) mod D in K.  beta: dict i -> value with beta[0] = 0 allowed any."""
    Rs = sorted({i % D for i in R}); Ks = {k % D for k in K}
    if 0 not in Rs or 0 not in Ks or len(alpha) != D or set(beta) != set(Rs): return False
    v00 = (alpha[0] + beta[0]) % p
    if v00 == 0 or cls_of(v00, p, g, D) != 0: return False
    for i in Rs:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0: continue
            if (cls_of(v, p, g, D) + i + j) % D not in Ks: return False
    return True


def find_rc(p, D, R, K, trials=300, seed=1, dfs_max_p=12000, dfs_limit=2 * 10 ** 8):
    """returns (alpha, beta_dict, how) or None (not found; NOT a proof of non-existence)."""
    g = prim_root(p)
    Rl = [0] + sorted({i % D for i in R} - {0}); Kl = sorted({k % D for k in K})
    Ra = (ctypes.c_int * len(Rl))(*Rl); Ka = (ctypes.c_int * len(Kl))(*Kl)
    al = (ctypes.c_int * D)(); be = (ctypes.c_int * len(Rl))()
    st = _lib.rc_random(p, g, D, Ra, len(Rl), Ka, len(Kl), trials, seed, al, be)
    if st == 1:
        alpha, beta = list(al), dict(zip(Rl, list(be)))
        assert check_rc(p, g, D, Rl, Kl, alpha, beta), ('random witness rejected', p, D, Rl, Kl)
        return alpha, beta, 'random'
    if p <= dfs_max_p:
        st, alpha, beta, nodes = rc_dfs().feasible(p, D, Rl, Kl, g=g, limit=dfs_limit)
        if st == 1:
            beta = {int(i): int(v) for i, v in beta.items()}
            assert check_rc(p, g, D, Rl, Kl, alpha, beta), ('dfs witness rejected', p, D, Rl, Kl)
            return alpha, beta, 'dfs'
        return None if st == 0 else ('undecided', nodes)
    return None


def primes_upto(n):
    import numpy as np
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]
