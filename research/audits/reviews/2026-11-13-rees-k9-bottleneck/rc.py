"""ctypes wrapper for rcdfs.c and a pow()-based checker of RC(D; R -> K) witnesses.

Independent of the threshold-7 scripts.  Interpreter: /opt/anaconda3/bin/python.
"""
import ctypes, os, subprocess, random

HERE = os.path.dirname(os.path.abspath(__file__))
SO = os.path.join(HERE, 'librcdfs.so')
if not os.path.exists(SO) or os.path.getmtime(SO) < os.path.getmtime(os.path.join(HERE, 'rcdfs.c')):
    subprocess.check_call(['cc', '-O2', '-shared', '-fPIC', '-o', SO, os.path.join(HERE, 'rcdfs.c')])
_lib = ctypes.CDLL(SO)
_lib.rc_feasible.restype = ctypes.c_int
_lib.rc_feasible.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                             ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                             ctypes.c_longlong, ctypes.c_uint,
                             ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                             ctypes.POINTER(ctypes.c_longlong)]


def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


def factor_set(n):
    s, d = set(), 2
    while d * d <= n:
        while n % d == 0: s.add(d); n //= d
        d += 1
    if n > 1: s.add(n)
    return s


def primitive_root(p):
    fs = factor_set(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs): return g
    raise ValueError


def cls_pow(x, p, g, D):
    """class of x != 0 modulo D w.r.t. generator g, by exponentiation only"""
    z = pow(g, (p - 1) // D, p)
    y = pow(x, (p - 1) // D, p)
    t = 1
    for c in range(D):
        if t == y: return c
        t = t * z % p
    raise ValueError('not found')


def check(p, g, D, R, K, alpha, beta):
    """beta: dict i -> value. Normal form alpha_0+beta_0 in Q_0 checked as a cell condition."""
    Ks = {k % D for k in K}
    if (alpha[0] + beta[0]) % p == 0 or cls_pow((alpha[0] + beta[0]) % p, p, g, D) != 0: return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0: continue
            if (cls_pow(v, p, g, D) + i + j) % D not in Ks: return False
    return True


def feasible(p, D, R, K, g=None, limit=10**12, seed=0):
    """complete search; returns (status, alpha, beta_dict, nodes).  status 1/0/-1."""
    if g is None: g = primitive_root(p)
    R = [0] + [i % D for i in R if i % D != 0]
    Ra = (ctypes.c_int * len(R))(*R)
    Ka = (ctypes.c_int * len(K))(*K)
    al = (ctypes.c_int * D)(); be = (ctypes.c_int * len(R))(); nd = ctypes.c_longlong()
    st = _lib.rc_feasible(p, g, D, Ra, len(R), Ka, len(K), limit, seed, al, be, ctypes.byref(nd))
    if st == 1:
        alpha = list(al); beta = dict(zip(R, list(be)))
        assert check(p, g, D, R, K, alpha, beta), ('witness rejected', p, D, R, K)
        return 1, alpha, beta, nd.value
    return st, None, None, nd.value
