"""Instrument theorems/rees_is_sde_solver.py (unchanged) and compare its
operation counts with the analytic bounds of
research/audits/reviews/2026-11-04-rees-is-runtime.md.

Run with  /opt/anaconda3/bin/python -O is_count.py  (-O strips the solver's
assert-only checks; the remaining verification work, theorem11's identity
(12) loop and the final verify(), is attributed by function and excluded).
"""
import random
import sys
from collections import Counter, defaultdict
from math import gcd

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
import theorems.rees_is_sde_solver as S  # noqa: E402

if __debug__:
    raise SystemExit("run with python -O")

MUL = Counter()        # field multiplications by function
ADD = Counter()        # field additions/subtractions by function
POWS = defaultdict(list)   # (function) -> list of (exponent bitlen, negative)
OTHERPOW = Counter()   # pow() with modulus != p (exponent arithmetic)
KERNELS = []           # (R, E, mults inside) per _kernel_vector call
CLASSIFY = [0]
P = [None]

EXCLUDE = {"theorem11", "verify"}   # verification-only work


def _named(f):
    while f.f_code.co_name.startswith("<"):
        f = f.f_back
    return f.f_code.co_name


def _caller():
    return _named(sys._getframe(2))


class F(int):
    """int in [0, p) that counts the arithmetic done on it."""
    def _wrap(self, v):
        return F(v)

    def __mul__(self, o):
        MUL[_caller()] += 1
        return F(int(self) * int(o))
    __rmul__ = __mul__

    def __add__(self, o):
        ADD[_caller()] += 1
        return F(int(self) + int(o))
    __radd__ = __add__

    def __sub__(self, o):
        ADD[_caller()] += 1
        return F(int(self) - int(o))

    def __rsub__(self, o):
        ADD[_caller()] += 1
        return F(int(o) - int(self))

    def __neg__(self):
        return F(-int(self))

    def __mod__(self, o):
        return F(int(self) % int(o))

    def __pow__(self, e, m=None):
        return counting_pow(self, e, m, depth=2)


_builtin_pow = pow


def counting_pow(x, e, m=None, depth=1):
    if m is None:
        return _builtin_pow(int(x), e)
    if m == P[0]:
        fn = _named(sys._getframe(depth))
        POWS[fn].append((abs(int(e)).bit_length(), int(e) < 0))
        return F(_builtin_pow(int(x), int(e), m))
    OTHERPOW[_named(sys._getframe(depth))] += 1
    return _builtin_pow(int(x), int(e), int(m))


S.pow = counting_pow   # module-global shadow of builtins.pow

_orig_kernel = S._kernel_vector


def kernel_wrapper(prime, vectors, spread=False):
    before = MUL["_kernel_vector"]
    out = _orig_kernel(prime, [[F(x) for x in v] for v in vectors], spread)
    KERNELS.append((len(vectors[0]), len(vectors), MUL["_kernel_vector"] - before))
    return out


S._kernel_vector = kernel_wrapper

_orig_classify = S.Classifier.classify


def classify_wrapper(self, alpha):
    CLASSIFY[0] += 1
    return _orig_classify(self, F(alpha))


S.Classifier.classify = classify_wrapper


def reset():
    for c in (MUL, ADD, OTHERPOW):
        c.clear()
    POWS.clear()
    KERNELS.clear()
    CLASSIFY[0] = 0


def pow_mults(lst):
    """Square-and-multiply cost bound 2*bitlen per exponentiation (+1 inversion if e<0)."""
    return sum(0 if (neg and bl == 1) else 2 * bl for bl, neg in lst), sum(1 for _, neg in lst if neg)


# ---------------- analytic predictions ----------------

def B(k, a, l):
    return k ** (l * (l - 1) // 2) * (a + 1) ** l


def Lam(k, a):
    """Per-input Gaussian-elimination mults of Lemma 12: sum_l R_l^2 E_l / B_l."""
    return sum((k ** (l - 1) * a) ** 2 * k ** (l - 1) * (a + 1) / B(k, a, l)
               for l in range(1, k + 1))


def nodes_per_t11(k, a):
    return {l: B(k, a, k) // B(k, a, l) for l in range(1, k + 1)}


def predicted(k, a, L):
    G = S.collision_arity(k, a)
    calls = sum(G ** j for j in range(L))
    nodes = nodes_per_t11(k, a)
    kern = {l: calls * n for l, n in nodes.items()}
    la = sum(kern[l] * (k ** (l - 1) * a) ** 2 * k ** (l - 1) * (a + 1) for l in kern)
    cls_bound = sum(kern[l] * k ** (l - 1) * (a + 1) for l in kern)
    inputs = calls * G
    return dict(G=G, t11=calls, kernels=sum(kern.values()), kern_by_level=kern,
                la_bound=la, la_formula=inputs * Lam(k, a), cls_bound=cls_bound,
                inputs=inputs)


def nu(p, k):
    n, out = p - 1, 0
    for ell in S._prime_divisors(k):
        while n % ell == 0:
            n //= ell
            out += 1
    return out


def run(p, d, a, M=None, early_exit=False, spread=False, seed=0, cols=None):
    k, t = S.reduced_degree(p, d)
    need = S.columns_required(p, d, a)
    M = M or need
    rnd = random.Random(seed)
    if cols is None:
        cols = [tuple(rnd.randrange(p) for _ in range(a)) for _ in range(M)]
    reset()
    P[0] = p
    w = S.is_sde_solve(p, d, cols, early_exit=early_exit, spread=spread)
    assert S.verify(p, d, cols, w.s)
    mult_alg = sum(v for f, v in MUL.items() if f not in EXCLUDE)
    pm_alg = sum(pow_mults(v)[0] for f, v in POWS.items() if f not in EXCLUDE)
    inv_alg = sum(pow_mults(v)[1] for f, v in POWS.items() if f not in EXCLUDE)
    return dict(p=p, d=d, kappa=k, t=t, a=a, M=M, L=w.levels, zs=len(w.zero_sum),
                restarts=w.restarts, nu=nu(p, k) if k > 1 else 0,
                classify=CLASSIFY[0], kernels=len(KERNELS),
                kernel_max_ratio=max((m / (R * R * E) for R, E, m in KERNELS), default=0),
                kernel_mults=sum(m for *_, m in KERNELS),
                kernel_bound=sum(R * R * E + R for R, E, _ in KERNELS),
                mul_by_fn=dict(MUL), pows_by_fn={f: (len(v), pow_mults(v)) for f, v in POWS.items()},
                mult_alg=mult_alg, pow_mult_alg=pm_alg, inv_alg=inv_alg,
                excluded=sum(v for f, v in MUL.items() if f in EXCLUDE) +
                sum(pow_mults(v)[0] for f, v in POWS.items() if f in EXCLUDE),
                early=w.early_zero, t11=w.theorem11_calls, kernel_calls_reported=w.kernel_calls,
                sizes=Counter((R, E) for R, E, _ in KERNELS))


def report(r):
    k, a, L = r["kappa"], r["a"], r["L"]
    line = (f"p={r['p']:>6} d={r['d']} k={k} t={r['t']} a={a} N={r['M']:>4} L={L} zs={r['zs']} "
            f"nu={r['nu']} restarts={r['restarts']} early={r['early']}")
    print(line)
    print(f"   kernels={r['kernels']} sizes={dict(r['sizes'])} GE mults={r['kernel_mults']} "
          f"<= sum(R^2E+R)={r['kernel_bound']} (max ratio {r['kernel_max_ratio']:.3f})")
    print(f"   classify calls={r['classify']} | field mults (alg)={r['mult_alg']} "
          f"+ pow-mults<= {r['pow_mult_alg']} + inversions {r['inv_alg']} | verification-only={r['excluded']}")
    print(f"   mults by fn: { {f: v for f, v in sorted(r['mul_by_fn'].items())} }")
    print(f"   pows by fn (count, (mult bound, inversions)): {r['pows_by_fn']}")
    if k > 1:
        pr = predicted(k, a, L)
        runs = r["restarts"] + 1
        print(f"   predicted per run: t11={pr['t11']} kernels={pr['kernels']} by level={pr['kern_by_level']} "
              f"GE bound={pr['la_bound']} (= inputs*Lambda {pr['la_formula']:.0f}) classify<= {pr['cls_bound']}")
        print(f"   x runs={runs}: kernels<= {runs*pr['kernels']} GE<= {runs*pr['la_bound']} "
              f"classify<= {runs*pr['cls_bound']}; reported last-run t11={r['t11']} kernels={r['kernel_calls_reported']}")
    print()


if __name__ == "__main__":
    print("Lambda(k,a) values:")
    for k in (2, 3, 4, 5):
        print("  k=%d:" % k, ", ".join(f"a={a}: {Lam(k,a):.2f} (bound a^2+k^2a+2k^3+1={a*a+k*k*a+2*k**3+1})"
                                         for a in (1, 2, 5, 20, 100)))
    print()
    cases = [
        # (p, d, a, early_exit)
        (5, 2, 1, False), (7, 2, 1, False), (13, 2, 1, False), (97, 2, 1, False),
        (257, 2, 1, False), (65537, 2, 1, False), (7, 2, 2, False), (97, 2, 2, False),
        (65537, 2, 2, False), (536870951, 2, 2, False),
        (7, 3, 1, False), (13, 3, 1, False), (163, 3, 1, False), (163, 3, 2, False),
        (19, 3, 2, False), (5, 3, 2, False), (11, 3, 2, False), (536871001 if (536871001 - 1) % 3 == 0 else 7, 3, 2, False),
        (97, 2, 2, True), (163, 3, 2, True),
    ]
    for p, d, a, ee in cases:
        report(run(p, d, a, early_exit=ee))
    # adversarial order to force restarts: columns whose kernel coefficients have growing pi-parts
    print("restart stress (spread kernel, several seeds) at p=65537,d=2,a=1 and p=163,d=3,a=1:")
    for p, d, a in ((65537, 2, 1), (163, 3, 1), (257, 2, 2)):
        best = max((run(p, d, a, seed=s, spread=True) for s in range(6)), key=lambda r: r["restarts"])
        report(best)
