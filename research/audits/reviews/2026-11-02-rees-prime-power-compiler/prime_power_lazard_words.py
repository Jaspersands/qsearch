"""Inverse-BCH word evaluation modulo an annihilating prime power p^e, any fixed class c<p.

Item 6 of research/REES_FULL_CAMPAIGN.md. The straight-line certificates of
theorems/universal_lazard_words.py are rational identities over Z[1/c!] and do
not depend on p. Only that file's evaluator reduces exponents modulo p. This
module reuses the certificates unchanged and evaluates them modulo M=p^e.

Also here: an exact model of the free class-c Lie ring F_{s,c}(Z/M) (Lyndon
basis inside the truncated free associative algebra), its BCH group law, and
the free pullback Phi:(F,*)->G evaluated by group words only. Ground truth for
tests is the unitriangular group UT_{n}(Z/M), whose Lie ring is computed
directly by matrix log/exp, independently of BCH words.

Run: /opt/anaconda3/bin/python -B prime_power_lazard_words.py  (writes the .json report)
"""
from __future__ import annotations

import json
import random
import sys
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.universal_lazard_words import compile_lazard_word  # noqa: E402


def _prime_power(modulus, p):
    if p < 2 or any(p % q == 0 for q in range(2, int(p**0.5)+1)):
        raise ValueError("p must be prime")
    e, m = 0, modulus
    while m % p == 0:
        m //= p
        e += 1
    if m != 1 or e < 1:
        raise ValueError("modulus must be p^e with e>=1")
    return e


# ---------------------------------------------------------------- evaluator

class PrimePowerLazardWords:
    """Opaque evaluator of the certified ADD/BRACKET words, exponents mod M=p^e.

    M is any power of p annihilating G (exact exponent not needed; M=p^b is a
    valid loose bound for b-bit encodings). Class and exponent promises are
    external. Every branch depends only on public certificate data and public
    coefficients, never on element values.
    """

    def __init__(self, p, modulus, class_bound, identity, multiply):
        self.e = _prime_power(modulus, p)
        if type(class_bound) is not int or not 1 <= class_bound < p or not callable(multiply):
            raise ValueError("1<=c<p and public multiplication required")
        self.p, self.modulus, self.class_bound, self.identity = p, modulus, class_bound, identity
        self._multiply, self.multiplication_calls = multiply, 0
        self.certificates = {op: compile_lazard_word(class_bound, op) for op in ("add", "bracket")}

    def multiply(self, left, right):
        self.multiplication_calls += 1
        return self._multiply(left, right)

    def power(self, element, exponent):
        if type(exponent) is not int:
            raise ValueError("integer exponent required")
        exponent %= self.modulus          # the ONLY change from the exponent-p evaluator
        result = self.identity
        while exponent:
            if exponent & 1:
                result = self.multiply(result, element)
            exponent //= 2
            if exponent:
                element = self.multiply(element, element)
        return result

    def scalar(self, numerator, denominator):
        # denominator has prime factors <= c < p (certificate-checked), so it is a unit mod p^e
        return numerator*pow(denominator, -1, self.modulus) % self.modulus

    def _evaluate(self, operation, left, right):
        certificate = self.certificates[operation]
        values = [self.identity, left, right]
        for instruction in certificate.instructions:
            if instruction[0] == "mul":
                values.append(self.multiply(values[instruction[1]], values[instruction[2]]))
            else:
                _, i, numerator, denominator = instruction
                values.append(self.power(values[i], self.scalar(numerator, denominator)))
        return values[certificate.output]

    def lie_add(self, left, right):
        return self._evaluate("add", left, right)

    def lie_bracket(self, left, right):
        return self._evaluate("bracket", left, right)

    def operation_caps(self):
        """Worst-case group multiplications per operation (square-and-multiply, 2*bitlen(M))."""
        pw = 2*self.modulus.bit_length()
        cap = {op: sum(1 if i[0] == "mul" else pw for i in cert.instructions)
               for op, cert in self.certificates.items()}
        return {"power": pw, "lie_add": cap["add"], "lie_bracket": cap["bracket"]}


# ------------------------------------------- truncated free associative algebra mod M

def t_mul(a, b, degree, modulus):
    out = {}
    for u, x in a.items():
        for v, y in b.items():
            if len(u)+len(v) <= degree:
                w = u+v
                out[w] = (out.get(w, 0)+x*y) % modulus
    return {w: x for w, x in out.items() if x}


def t_add(a, b, scalar, modulus):
    out = dict(a)
    for w, x in b.items():
        out[w] = (out.get(w, 0)+scalar*x) % modulus
    return {w: x for w, x in out.items() if x}


def t_exp(n, degree, modulus):
    """exp(n), n without constant term; 1/k! for k<=degree<p is a unit mod M."""
    result, power = {(): 1}, {(): 1}
    for k in range(1, degree+1):
        power = t_mul(power, n, degree, modulus)
        result = t_add(result, power, pow(factorial(k), -1, modulus), modulus)
    return result


def t_log(g, degree, modulus):
    n = dict(g)
    if n.pop((), 0) % modulus != 1:
        raise ValueError("constant term must be 1")
    result, power = {}, {(): 1}
    for k in range(1, degree+1):
        power = t_mul(power, n, degree, modulus)
        result = t_add(result, power, (-1)**(k+1)*pow(k, -1, modulus), modulus)
    return result


# ------------------------------------------------- free class-c Lie ring F_{s,c}(Z/M)

def lyndon_words(s, c):
    """Duval's algorithm: all Lyndon words over range(s) of length <= c, lex order."""
    words, w = [], [-1]
    while w:
        w[-1] += 1
        words.append(tuple(w))
        m = len(w)
        while len(w) < c:
            w.append(w[len(w)-m])
        while w and w[-1] == s-1:
            w.pop()
    return words


def standard_factor(w):
    """w=uv with v the longest proper Lyndon suffix."""
    for i in range(1, len(w)):
        v = w[i:]
        if all(v < v[j:]+v[:j] for j in range(1, len(v))) and all(v < v[j:] for j in range(1, len(v))):
            return w[:i], v
    raise ValueError("not a Lyndon word of length >= 2")


class FreeNilpotentLieRing:
    """F_{s,c}(Z/M) with Lyndon basis; coordinates are tuples in (Z/M)^d."""

    def __init__(self, s, c, p, modulus):
        _prime_power(modulus, p)
        if not 1 <= c < p:
            raise ValueError("c<p required")
        self.s, self.c, self.p, self.modulus = s, c, p, modulus
        self.basis = [w for w in lyndon_words(s, c)]
        self.index = {w: i for i, w in enumerate(self.basis)}
        self.tree = {w: (None if len(w) == 1 else standard_factor(w)) for w in self.basis}
        self.expansion = {}
        for w in sorted(self.basis, key=len):
            if len(w) == 1:
                self.expansion[w] = {w: 1}
            else:
                u, v = self.tree[w]
                a, b = self.expansion[u], self.expansion[v]
                self.expansion[w] = t_add(t_mul(a, b, c, modulus), t_mul(b, a, c, modulus), -1, modulus)
            if self.expansion[w].get(w) != 1 or any(x < w for x in self.expansion[w] if len(x) == len(w)):
                raise ArithmeticError("Lyndon triangularity failed")
        self.dimension = len(self.basis)

    def to_tensor(self, coords):
        out = {}
        for w, a in zip(self.basis, coords):
            if a % self.modulus:
                out = t_add(out, self.expansion[w], a, self.modulus)
        return out

    def from_tensor(self, z):
        z, coords = dict(z), [0]*self.dimension
        for i, w in enumerate(self.basis):          # increasing lex order
            a = z.get(w, 0) % self.modulus
            coords[i] = a
            if a:
                z = t_add(z, self.expansion[w], -a, self.modulus)
        if z:
            raise ArithmeticError("element is not in the Lie span")
        return tuple(coords)

    def bch(self, u, v):
        """Group law u*v = log(exp u exp v) on F."""
        c, M = self.c, self.modulus
        return self.from_tensor(t_log(t_mul(t_exp(self.to_tensor(u), c, M), t_exp(self.to_tensor(v), c, M), c, M), c, M))

    def generator(self, i):
        return tuple(1 if w == (i,) else 0 for w in self.basis)

    def random(self, rng):
        return tuple(rng.randrange(self.modulus) for _ in self.basis)


class FreePullback:
    """Phi:(F_{s,c}(Z/M),*) -> G, x_i -> g_i, computed with group words only."""

    def __init__(self, ring, words, generators):
        if len(generators) != ring.s or words.modulus != ring.modulus or words.class_bound < ring.c:
            raise ValueError("inconsistent pullback data")
        self.ring, self.words = ring, words
        start = words.multiplication_calls
        self.images = {}
        for w in sorted(ring.basis, key=len):        # classical precomputation, h_w = pi(P(w))
            if len(w) == 1:
                self.images[w] = generators[w[0]]
            else:
                u, v = ring.tree[w]
                self.images[w] = words.lie_bracket(self.images[u], self.images[v])
        self.precomputation_multiplications = words.multiplication_calls-start

    def __call__(self, coords):
        result = self.words.identity
        for w, a in zip(self.ring.basis, coords):
            if a % self.ring.modulus:
                result = self.words.lie_add(result, self.words.power(self.images[w], a))
        return result

    def evaluation_cap(self):
        caps = self.words.operation_caps()
        return self.ring.dimension*(caps["power"]+caps["lie_add"])


# ------------------------------------------------- ground-truth target UT_n(Z/M)

def mat_mul(a, b, M):
    n = len(a)
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(i, j+1)) % M for j in range(n)) for i in range(n))


def mat_identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def mat_lin(terms, n, M):
    return tuple(tuple(sum(c*m[i][j] for c, m in terms) % M for j in range(n)) for i in range(n))


def mat_exp(a, M):
    """exp of strictly upper triangular a; a^n=0 and n-1<p so 1/k! is a unit mod M."""
    n = len(a)
    result, power = mat_identity(n), mat_identity(n)
    for k in range(1, n):
        power = mat_mul(power, a, M)
        result = mat_lin([(1, result), (pow(factorial(k), -1, M), power)], n, M)
    return result


def mat_log(g, M):
    n = len(g)
    nil = mat_lin([(1, g), (-1, mat_identity(n))], n, M)
    result, power = tuple(tuple(0 for _ in range(n)) for _ in range(n)), mat_identity(n)
    for k in range(1, n):
        power = mat_mul(power, nil, M)
        result = mat_lin([(1, result), ((-1)**(k+1)*pow(k, -1, M), power)], n, M)
    return result


def mat_bracket(a, b, M):
    return mat_lin([(1, mat_mul(a, b, M)), (-1, mat_mul(b, a, M))], len(a), M)


def random_nilpotent(n, M, rng):
    return tuple(tuple(rng.randrange(M) if j > i else 0 for j in range(n)) for i in range(n))


def direct_pullback(ring, logs, coords):
    """Phi computed through the target's own Lie ring: exp(sum c_w pi(P(w)))."""
    M, n = ring.modulus, len(logs[0])
    lie = {}
    for w in sorted(ring.basis, key=len):
        lie[w] = logs[w[0]] if len(w) == 1 else mat_bracket(lie[ring.tree[w][0]], lie[ring.tree[w][1]], M)
    return mat_exp(mat_lin([(a, lie[w]) for w, a in zip(ring.basis, coords)], n, M), M)


# ------------------------------------------------- checks and report

def check_ut_operations(p, e, c, trials, seed):
    """ADD/BRACKET words on opaque UT_{c+1}(Z/p^e) elements vs direct matrix log/exp."""
    M, n, rng = p**e, c+1, random.Random(seed)
    words = PrimePowerLazardWords(p, M, c, mat_identity(n), lambda a, b: mat_mul(a, b, M))
    corner_nonzero = 0
    for _ in range(trials):
        a, b = random_nilpotent(n, M, rng), random_nilpotent(n, M, rng)
        x, y = mat_exp(a, M), mat_exp(b, M)
        if words.lie_add(x, y) != mat_exp(mat_lin([(1, a), (1, b)], n, M), M):
            return {"ok": False, "failed": "add", "a": a, "b": b}
        br = mat_bracket(a, b, M)
        if words.lie_bracket(x, y) != mat_exp(br, M):
            return {"ok": False, "failed": "bracket", "a": a, "b": b}
        corner_nonzero += bool(mat_log(words.lie_add(x, y), M)[0][n-1])
    return {"ok": True, "p": p, "e": e, "c": c, "trials": trials, "group": f"UT_{n}(Z/{M})",
            "caps": words.operation_caps(), "add_results_with_nonzero_corner": corner_nonzero}


def check_ut_pullback(p, e, c, s, trials, seed, modulus=None):
    """Phi by words vs Phi direct, plus Phi(u*v)=Phi(u)Phi(v), on G=<g_1..g_s> <= UT_{c+1}(Z/p^e).

    modulus may be a loose multiple p^b of the exponent; F is then F_{s,c}(Z/p^b).
    """
    M_group = p**e
    M = modulus or M_group
    n, rng = c+1, random.Random(seed)
    ring = FreeNilpotentLieRing(s, c, p, M)
    words = PrimePowerLazardWords(p, M, c, mat_identity(n), lambda a, b: mat_mul(a, b, M_group))
    logs = [random_nilpotent(n, M_group, rng) for _ in range(s)]
    gens = [mat_exp(a, M_group) for a in logs]
    phi = FreePullback(ring, words, gens)
    ringG = FreeNilpotentLieRing(s, c, p, M_group)
    for i in range(s):
        if phi(ring.generator(i)) != gens[i]:
            return {"ok": False, "failed": "generator"}
    before = words.multiplication_calls
    for _ in range(trials):
        u, v = ring.random(rng), ring.random(rng)
        pu = phi(u)
        if pu != direct_pullback(ringG, logs, tuple(x % M_group for x in u)):
            return {"ok": False, "failed": "direct", "u": u}
        if phi(ring.bch(u, v)) != mat_mul(pu, phi(v), M_group):
            return {"ok": False, "failed": "homomorphism", "u": u, "v": v}
    per_eval = (words.multiplication_calls-before)/(3*trials)
    return {"ok": True, "p": p, "e": e, "c": c, "s": s, "modulus_used": M, "free_rank_d": ring.dimension,
            "trials": trials, "precomputation_multiplications": phi.precomputation_multiplications,
            "mean_multiplications_per_Phi": round(per_eval, 1), "Phi_evaluation_cap": phi.evaluation_cap()}


def exponent_p_evaluator_failure(p=3, e=2):
    """Smallest exhibited failure of the mod-p evaluator: class 2, UT_3(Z/p^e)."""
    from theorems.universal_lazard_words import UniversalLazardWords
    M = p**e
    x = mat_exp(((0, 1, 0), (0, 0, 0), (0, 0, 0)), M)
    y = mat_exp(((0, 0, 0), (0, 0, 1), (0, 0, 0)), M)
    true_add = mat_exp(((0, 1, 0), (0, 0, 1), (0, 0, 0)), M)
    old = UniversalLazardWords(p, 2, mat_identity(3), lambda a, b: mat_mul(a, b, M))
    new = PrimePowerLazardWords(p, M, 2, mat_identity(3), lambda a, b: mat_mul(a, b, M))
    return {"p": p, "e": e, "x": x, "y": y, "true_exp_logx_plus_logy": true_add,
            "mod_p_evaluator": old.lie_add(x, y), "mod_p_correct": old.lie_add(x, y) == true_add,
            "mod_p^e_evaluator": new.lie_add(x, y), "mod_p^e_correct": new.lie_add(x, y) == true_add,
            "mod_p_inverse_of_x_correct": old.power(x, -1) == mat_exp(((0, M-1, 0), (0, 0, 0), (0, 0, 0)), M)}


def negative_controls(seed=5):
    """Each must FAIL: mod-p evaluation on exponent p^2, and class-(c-1) words on a class-c target."""
    from theorems.universal_lazard_words import UniversalLazardWords
    rng, out = random.Random(seed), {}
    p, e, c = 7, 2, 5
    M, n = p**e, c+1
    old = UniversalLazardWords(p, c, mat_identity(n), lambda a, b: mat_mul(a, b, M))
    short = PrimePowerLazardWords(p, M, c-1, mat_identity(n), lambda a, b: mat_mul(a, b, M))
    fails_old = fails_short = 0
    for _ in range(10):
        a, b = random_nilpotent(n, M, rng), random_nilpotent(n, M, rng)
        target = mat_exp(mat_lin([(1, a), (1, b)], n, M), M)
        x, y = mat_exp(a, M), mat_exp(b, M)
        fails_old += old.lie_add(x, y) != target
        fails_short += short.lie_add(x, y) != target
    out["mod_p_evaluator_add_failures_of_10_at_p7_e2_c5"] = fails_old
    out["class4_words_add_failures_of_10_on_UT6_Z49"] = fails_short
    # The mod-p evaluator also breaks the free pullback homomorphism at (7,2,5), s=2.
    ring = FreeNilpotentLieRing(2, c, p, M)
    logs = [random_nilpotent(n, M, rng) for _ in range(2)]
    gens = [mat_exp(a, M) for a in logs]
    class _ModP(UniversalLazardWords):
        modulus = M
    phi_old = FreePullback(ring, _ModP(p, c, mat_identity(n), lambda a, b: mat_mul(a, b, M)), gens)
    u, v = ring.random(rng), ring.random(rng)
    out["mod_p_pullback_homomorphism_holds"] = phi_old(ring.bch(u, v)) == mat_mul(phi_old(u), phi_old(v), M)
    return out


def word_size_table(max_class=8):
    rows = []
    for c in range(1, max_class+1):
        for op in ("add", "bracket"):
            cert = compile_lazard_word(c, op)
            muls = sum(1 for i in cert.instructions if i[0] == "mul")
            dens = [i[3] for i in cert.instructions if i[0] == "pow"]
            rows.append({"c": c, "op": op, "mul": muls, "pow": len(cert.instructions)-muls,
                         "max_denominator": max(dens+[1])})
    return rows


def build_report():
    ops = [check_ut_operations(p, e, c, 25, 1000*p+10*e+c)
           for p, e, c in [(3, 2, 2), (5, 2, 3), (5, 3, 4), (7, 2, 5), (7, 2, 6), (11, 2, 5), (11, 2, 6),
                           (7, 3, 6), (11, 3, 6), (13, 2, 7)]]
    pulls = [check_ut_pullback(p, e, c, s, 6, 7*p+e+c+s)
             for p, e, c, s in [(3, 2, 2, 3), (7, 2, 5, 2), (7, 2, 5, 3), (7, 2, 6, 2), (11, 2, 5, 2), (11, 2, 6, 2),
                                (11, 2, 5, 3)]]
    pulls.append(check_ut_pullback(7, 2, 5, 2, 4, 99, modulus=7**4))
    return {"status": "PRIME_POWER_EVALUATION_OF_UNIVERSAL_LAZARD_CERTIFICATES",
            "exponent_p_evaluator_failure": exponent_p_evaluator_failure(),
            "ut_operation_checks": ops, "ut_pullback_checks": pulls,
            "negative_controls": negative_controls(),
            "word_sizes": word_size_table(8),
            "all_ok": all(r["ok"] for r in ops+pulls)}


if __name__ == "__main__":
    report = build_report()
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(report, indent=1, default=str)+"\n")
    print(json.dumps({k: report[k] for k in ("all_ok", "exponent_p_evaluator_failure", "negative_controls")}, default=str))
    for r in report["ut_operation_checks"]+report["ut_pullback_checks"]:
        print({k: v for k, v in r.items() if k not in ("caps",)})


# ------------------------------------------------- export for the independent GAP check

def gap_data(p, e, c, trials, seed, s=2):
    """GAP source: certificates with exponents reduced mod p^e (and mod p, for the control),
    Lyndon tree, and sample triples (u, v, u*v) computed in F_{s,c}(Z/p^e) by this module."""
    M, rng = p**e, random.Random(seed)
    ring = FreeNilpotentLieRing(s, c, p, M)

    def program(op, modulus):
        out = []
        for i in compile_lazard_word(c, op).instructions:
            out.append([1, i[1]+1, i[2]+1] if i[0] == "mul"
                       else [2, i[1]+1, i[2]*pow(i[3], -1, modulus) % modulus])
        return out, compile_lazard_word(c, op).output+1

    tree = [[w[0]+1, 0] if len(w) == 1 else [ring.index[ring.tree[w][0]]+1, ring.index[ring.tree[w][1]]+1]
            for w in ring.basis]
    triples = []
    for _ in range(trials):
        u, v = ring.random(rng), ring.random(rng)
        triples.append([list(u), list(v), list(ring.bch(u, v))])
    lines = [f"PP_p:={p};; PP_e:={e};; PP_c:={c};; PP_s:={s};; PP_M:={M};; PP_d:={ring.dimension};;",
             f"PP_tree:={json.dumps(tree)};;",
             f"PP_order:={json.dumps([ring.index[w]+1 for w in sorted(ring.basis, key=len)])};;",
             f"PP_triples:={json.dumps(triples)};;"]
    for name, modulus in (("", M), ("_modp", p)):
        for op in ("add", "bracket"):
            prog, out = program(op, modulus)
            lines.append(f"PP_{op}{name}:=rec(prog:={json.dumps(prog)}, out:={out});;")
    return "\n".join(lines)+"\n"
