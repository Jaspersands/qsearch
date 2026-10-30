"""Exact arithmetic record identities, not a receiver or candidate search.

Primary source checked: Mao--Yi--Zhu, arXiv:2410.13572v2, Fig. 2,
Eq. (7), Theorem 4, Appendix B, and SM Eqs. (S5), (S14)--(S17):
https://arxiv.org/html/2410.13572v2
The measurement is U = F_1 T_1 C, with the POSITIVE Fourier exponent.
For p >= 5, T|t> = omega**f(t)|t>, f(t) = alpha*t**3 + beta*t**2
+ gamma*t + delta, alpha != 0. Thus chi_b = C^dagger T_1^dagger
F_1^dagger|b>, not T_1^dagger C^dagger F_1^dagger|b>.

Arithmetic contract (derived here, not attributed to the paper):
Use position-then-momentum coordinates, the reverse of the paper's block
order. Write K = C^dagger = xi W(a,d) mu(S), S = [[A,B],[G,H]],
with W(a,d)|z> = omega**(d.(z+a/2))|z+a>. The unit-modulus scalar xi
fixes the chosen metaplectic representative and is irrelevant to scores.
Let r = rank(B). The kernel is zero unless x-a-A*y belongs to im(B).
For ANY v solving B*v = x-a-A*y, put

  Q(x,y) = ( (A*y).(G*y) + 2*(G*y).(B*v) + (B*v).(H*v) )/2
           + d.(x-a/2).
  <x|K|y> = xi * p**(-r/2) * omega**Q(x,y).

All arithmetic in Q is in F_p. Symplecticity makes Q independent of the
lift v, including singular B. A linear right inverse on im(B) makes Q a
quadratic polynomial on its support relation. These are grid-register
coordinates, NOT a claim that finite lattice coefficient weights, packet
membership, floors, or arbitrary grid encodings are quadratic.

Write y(t)=(t,b_tail), y0=(0,b_tail), u=A*e1, x0=a+A*y0. Exactly,

  chi_b(x) = xi*p**(-(r+1)/2)
             * sum_{t: x-x0-u*t in im(B)}
                 omega**(Q(x,y(t))-f(t)-b[0]*t).

Let s=rank([B,u]). The affine envelope is E=x0+im([B,u]). There are
only two cases; rank(B) alone does not distinguish them.

* s=r+1: on E there is a UNIQUE affine-linear t=t(x). The support is
  exactly E (size p**(r+1)), with flat modulus p**(-(r+1)/2). Its phase
  is quadratic minus alpha*t(x)**3: one rank-one cubic in source GRID
  coordinates. This includes r=0 and rank-deficient B with r=n-1.
* s=r: r>=1, E=x0+im(B), and every x in E retains all p values of t.
  The phase can be written q0(x)-alpha*t**3+c2*t**2+lambda(x)*t,
  with constant c2 and affine lambda. Lambda is nonconstant on E:
  otherwise distinct normalized columns K|t,b_tail> would be parallel,
  contradicting unitarity. Translating t removes its quadratic term,
  leaving q1(x)-alpha*t**3+L(x)*t with L affine and surjective on E.
  The ACTUAL support is {x in E: sum_t omega**(-alpha*t**3+L(x)*t)
  != 0}, not automatically affine, and the modulus is not generally flat.
  Full-rank B always falls in this case. One extra sum variable remains;
  replacing the sum by a rank-one cubic phase is invalid in general.

For completeness, the zero set here has an elementary exact description.
A p-term root sum vanishes iff its exponent histogram is uniform (the
minimal polynomial is 1+z+...+z**(p-1)), i.e. iff the cubic permutes F_p.
For g(t)=a*t**3+l*t, a!=0: when p=1 mod 3 the power sum of degree
(p-1)/3 rules out a permutation; when p=2 mod 3 the power sum of degree
(p+1)/3 forces l=0, and t**3 then is a permutation. Hence for p=1 mod 3
the actual support is E; for p=2 mod 3 it is E minus the affine hyperplane
L=0, of size (p-1)*p**(r-1), which is NOT an affine space.

Normalization is not an unspecified partition function. In the first
case p**(r+1) equal squared moduli sum to one. In the second, every L
value has p**(r-1) preimages and Fourier orthogonality gives
sum_L |sum_t omega**(-alpha*t**3+L*t)|**2 = p**2. The same prefactor
p**(-(r+1)/2) therefore gives norm one even at cancellation zeros.

For ANY normalized finite amplitudes a_g(x), including exactly the
specified nonuniform sequential-bin/full-cell lattice source, define

  Z_g = sum_{x,t: x-a-A*y(t) in im(B)}
          a_g(x)*omega**(-Q(x,y(t))+f(t)+b[0]*t).
  X_g(C,b) = (p**n+1)*p**(-(r+1))*|Z_g|**2 - 1.

Use the actual a_g(x)=sqrt(P_g(z)*p_{g,z}(k)) at an occupied encoded
cell x=enc(k), and zero elsewhere; disjoint packet membership identifies
z. An injective, fixed encoding and its finite padding are part of the
input. Field arithmetic wraps modulo p, but physical cells must not be
identified by wrap. No replacement by Gaussian point weights or a theta
normalizer is made here. Polynomial phase pullback to coefficient z is
licensed only if the specified enc(k(z,...)) is affine over F_p.

Genuine deterministic scoring subclasses for THESE amplitudes:
1. An enumerable polynomial number K of occupied labels, and s=r+1:
   K finite-amplitude queries and polynomial modular linear algebra.
2. The same support promise and polynomial p: at most K*p terms in
   either rank case. Polynomial K alone does not remove the extra sum.
3. An enumerable constrained pair set (x,t) of polynomial size, e.g.
   p**(r+1) polynomial: enumerate it and query the actual amplitudes,
   without needing the occupied source support to be small.
Membership/query access alone does not imply enumerable small support.
All bounds charge the amplitude evaluator's Gaussian integrals and bits.
For absolute score error eps<=1, overlap error eps/[3*(p**n+1)] suffices.
For an L-term contraction, absolute error eps/[3*(p**n+1)*L] per
normalized summand suffices. This needs O(log(D)+log(L)+log(1/eps))
extra precision bits, but does not make exponentially many terms cheap.

Statistical proxy allowance, separately from uniform record accuracy:
Theorem 4 gives E_Born[(X_phi-X_proxy)**2] <= (15/2)*Tr(Delta**2)
<= 15*||phi-proxy||**2 for normalized kets and Delta=P_phi-P_proxy.
This allows close, efficiently scored proxies; it supplies neither a
proxy construction nor an evaluator for a weighted Gaussian/theta sum.

Tests use exact cyclotomic quotient arithmetic, never float tolerances.
Fourier normalization is stored as p**(-m/2); all norm/projector/score
checks use its exact rational square. Independent gate replay fixes
sign and order conventions. Small dimensions are identity controls only.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import prod

import pytest
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.polyclasses import ANP


@lru_cache(maxsize=None)
def _roots(order):
    z = sp.Symbol("z")
    modulus = [QQ(int(c)) for c in sp.Poly(sp.cyclotomic_poly(order, z), z).all_coeffs()]
    root = ANP([QQ.one, QQ.zero], modulus, QQ)
    return tuple(root**j for j in range(order))


def _conjugate(value, roots):
    result = roots[0] * 0
    for coefficient in value.to_list():
        result = result * roots[-1] + coefficient
    return result


def _points(p, n):
    return product(range(p), repeat=n)


def _dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def _mv(matrix, vector):
    return tuple(_dot(row, vector) for row in matrix)


def _rows(matrix):
    return tuple(tuple(int(x) for x in row) for row in matrix.tolist())


def _solve(matrix, rhs, p):
    """Finite-field elimination; free variables are set to zero."""
    width = len(matrix[0])
    rows = [[x % p for x in row] + [value % p]
            for row, value in zip(matrix, rhs)]
    pivots = []
    for column in range(width):
        pivot = next((i for i in range(len(pivots), len(rows))
                      if rows[i][column]), None)
        if pivot is None:
            continue
        index = len(pivots)
        rows[index], rows[pivot] = rows[pivot], rows[index]
        inv = pow(rows[index][column], -1, p)
        rows[index] = [x*inv % p for x in rows[index]]
        for i in range(len(rows)):
            if i != index:
                scale = rows[i][column]
                rows[i] = [(x-scale*y) % p for x, y in zip(rows[i], rows[index])]
        pivots.append(column)
    if any(not any(row[:width]) and row[-1] for row in rows):
        return None, len(pivots)
    solution = [0] * width
    for i, column in enumerate(pivots):
        solution[column] = rows[i][-1]
    return tuple(solution), len(pivots)


@dataclass
class _Ket:
    coefficients: dict
    fourier_power: int = 0


def _basis(p, label):
    return _Ket({tuple(label): _roots(p)[0]})


def _apply(ket, gate, p):
    """Independent computational-basis replay of actual elementary gates."""
    roots = _roots(p)
    out = {}
    kind, *args = gate
    half = pow(2, -1, p)

    def add(label, value):
        out[label] = out.get(label, roots[0]*0) + value

    for x, amplitude in ket.coefficients.items():
        if kind == "F":
            index, sign = args
            for t in range(p):
                y = x[:index] + (t,) + x[index+1:]
                add(y, amplitude*roots[sign*t*x[index] % p])
        elif kind == "Q":
            add(x, amplitude*roots[half*_dot(x, _mv(args[0], x)) % p])
        elif kind == "L":
            add(tuple(t % p for t in _mv(args[0], x)), amplitude)
        elif kind == "W":
            a, d = args
            y = tuple((t+shift) % p for t, shift in zip(x, a))
            exponent = _dot(d, tuple(t+half*shift for t, shift in zip(x, a)))
            add(y, amplitude*roots[exponent % p])
        elif kind == "T":
            coefficients, sign = args
            exponent = sum(c*x[0]**j for j, c in enumerate(coefficients))
            add(x, amplitude*roots[sign*exponent % p])
        else:
            raise AssertionError(kind)
    return _Ket({x: value for x, value in out.items() if value},
                ket.fourier_power + (kind == "F"))


def _run(ket, gates, p):
    for gate in gates:
        ket = _apply(ket, gate, p)
    return ket


def _inverse(gate, p):
    kind, *args = gate
    if kind == "F":
        return (kind, args[0], -args[1])
    if kind == "Q":
        return (kind, tuple(tuple(-x for x in row) for row in args[0]))
    if kind == "L":
        return (kind, _rows(sp.Matrix(args[0]).inv_mod(p)))
    if kind == "W":
        return (kind, tuple(-x for x in args[0]), tuple(-x for x in args[1]))
    raise AssertionError(kind)


@dataclass
class _Chart:
    p: int
    n: int
    A: tuple
    B: tuple
    G: tuple
    H: tuple
    a: tuple
    d: tuple
    rank: int

    def phase_with_lift(self, x, y, v):
        ay, gy = _mv(self.A, y), _mv(self.G, y)
        bv, hv = _mv(self.B, v), _mv(self.H, v)
        half = pow(2, -1, self.p)
        return (half*(_dot(ay, gy)+2*_dot(gy, bv)+_dot(bv, hv))
                + _dot(self.d, tuple(t-half*a for t, a in zip(x, self.a)))) % self.p

    def phase(self, x, y):
        ay = _mv(self.A, y)
        v, _ = _solve(self.B, tuple(t-a-b for t, a, b in zip(x, self.a, ay)), self.p)
        return None if v is None else self.phase_with_lift(x, y, v)

    def envelope(self, b):
        u = tuple(row[0] for row in self.A)
        x0 = tuple((a+t) % self.p for a, t in zip(self.a, _mv(self.A, (0,)+b[1:])))
        matrix = tuple(row+(t,) for row, t in zip(self.B, u))
        _, rank = _solve(matrix, (0,)*self.n, self.p)
        points = {x for x in _points(self.p, self.n)
                  if _solve(matrix, tuple(t-a for t, a in zip(x, x0)), self.p)[0]
                  is not None}
        return points, rank


def _chart(p, n, gates):
    S = sp.eye(2*n)
    displacement = sp.zeros(2*n, 1)
    for kind, *args in gates:
        step = sp.eye(2*n)
        shift = sp.zeros(2*n, 1)
        if kind == "F":
            j, sign = args
            step[j, j] = step[n+j, n+j] = 0
            step[j, n+j], step[n+j, j] = -sign, sign
        elif kind == "Q":
            step[n:, :n] = sp.Matrix(args[0])
        elif kind == "L":
            linear = sp.Matrix(args[0])
            step[:n, :n] = linear
            step[n:, n:] = linear.inv_mod(p).T
        elif kind == "W":
            shift = sp.Matrix(args[0]+args[1])
        else:
            raise AssertionError(kind)
        S = (step*S) % p
        displacement = (step*displacement+shift) % p
    J = sp.zeros(2*n)
    J[:n, n:], J[n:, :n] = sp.eye(n), -sp.eye(n)
    assert (S.T*J*S-J) % p == sp.zeros(2*n)
    A, B, G, H = (_rows(block) for block in (S[:n, :n], S[:n, n:], S[n:, :n], S[n:, n:]))
    _, rank = _solve(B, (0,)*n, p)
    return _Chart(p, n, A, B, G, H, tuple(map(int, displacement[:n])),
                  tuple(map(int, displacement[n:])), rank)


def _column(chart, y):
    roots = _roots(chart.p)
    return _Ket({x: roots[q] for x in _points(chart.p, chart.n)
                 if (q := chart.phase(x, y)) is not None}, chart.rank)


def _record(chart, b, polynomial):
    p, roots = chart.p, _roots(chart.p)
    coefficients = {}
    for x in _points(p, chart.n):
        value = roots[0]*0
        for t in range(p):
            q = chart.phase(x, (t,)+b[1:])
            if q is not None:
                f = sum(c*t**j for j, c in enumerate(polynomial))
                value += roots[(q-f-b[0]*t) % p]
        if value:
            coefficients[x] = value
    return _Ket(coefficients, chart.rank+1)


def _norm(ket, p):
    roots = _roots(p)
    return sum((a*_conjugate(a, roots) for a in ket.coefficients.values()),
               roots[0]*0) / p**ket.fourier_power


def _same_record(left, right, p):
    assert _norm(left, p) == _norm(right, p) == _roots(p)[0]
    assert left.coefficients.keys() == right.coefficients.keys()
    pivot = next(iter(left.coefficients))
    for x in left.coefficients:
        assert (left.coefficients[x]*right.coefficients[pivot]
                == right.coefficients[x]*left.coefficients[pivot])


def _circuit(case):
    middle = {"rank_zero": [], "transverse": [("F", 1, 1)],
              "summed": [("F", 0, 1)], "full": [("F", 0, 1), ("F", 1, -1)]}[case]
    return [("L", ((1, 1), (0, 1))), ("Q", ((2, 1), (1, 3)))] + middle + [
        ("L", ((1, 1), (1, 2))), ("Q", ((1, 2), (2, 1))),
        ("W", (1, 2), (2, 1))]


@pytest.mark.parametrize("p", [5, 7])
def test_every_single_qudit_symplectic_kernel_has_exact_weyl_covariance(p):
    roots = _roots(p)
    count = 0
    for a, b, g, h in product(range(p), repeat=4):
        if (a*h-b*g) % p != 1:
            continue
        count += 1
        chart = _Chart(p, 1, ((a,),), ((b,),), ((g,),), ((h,),),
                       (0,), (0,), int(b != 0))
        columns = [_column(chart, (y,)) for y in range(p)]
        for y, column in enumerate(columns):
            assert _norm(column, p) == roots[0]
            image_x = _apply(column, ("W", (a,), (g,)), p)
            image_z = _apply(column, ("W", (b,), (h,)), p)
            assert image_x.coefficients == columns[(y+1) % p].coefficients
            assert image_z.coefficients == {
                x: value*roots[y] for x, value in column.coefficients.items()}
    assert count == p*(p*p-1)


@pytest.mark.parametrize("p", [5, 7])
@pytest.mark.parametrize("case,r,s", [
    ("rank_zero", 0, 1), ("transverse", 1, 2), ("summed", 1, 1), ("full", 2, 2)])
def test_general_affine_record_matches_independent_gate_replay(p, case, r, s):
    gates = _circuit(case)
    chart = _chart(p, 2, gates)
    assert chart.rank == r
    polynomial = (2, 3, 1, 2)
    for b in [(0, 0), (1, 2), (p-1, 1)]:
        _same_record(_column(chart, b), _run(_basis(p, b), gates, p), p)
        record = _record(chart, b, polynomial)
        direct = _run(_basis(p, b), [("F", 0, -1), ("T", polynomial, -1)] + gates, p)
        _same_record(record, direct, p)
        envelope, actual_s = chart.envelope(b)
        assert actual_s == s
        assert len(envelope) == p**s
        assert set(record.coefficients) <= envelope
        if s == r+1:
            assert set(record.coefficients) == envelope
            assert all(v*_conjugate(v, _roots(p)) == _roots(p)[0]
                       for v in record.coefficients.values())
        else:
            expected = p**r if p % 3 == 1 else (p-1)*p**(r-1)
            assert len(record.coefficients) == expected


def test_rank_deficient_kernel_is_independent_of_the_solution_lift():
    p = 5
    chart = _chart(p, 2, _circuit("transverse"))
    assert chart.rank == 1
    y = (2, 3)
    for x in _points(p, 2):
        lifts = [v for v in _points(p, 2)
                 if all((a+b+c-t) % p == 0 for a, b, c, t in
                        zip(chart.a, _mv(chart.A, y), _mv(chart.B, v), x))]
        if lifts:
            assert len(lifts) == p
            assert {chart.phase_with_lift(x, y, v) for v in lifts} == {chart.phase(x, y)}
        else:
            assert chart.phase(x, y) is None


@pytest.mark.parametrize("p", [5, 7])
def test_transverse_cubic_is_rank_one_not_a_quadratic_pullback(p):
    chart = _chart(p, 2, _circuit("transverse"))
    b, polynomial = (2, 1), (1, 2, 3, 1)
    envelope, s = chart.envelope(b)
    assert s == chart.rank+1
    phases = {}
    t_values = {}
    for x in envelope:
        valid = [(t, chart.phase(x, (t,)+b[1:])) for t in range(p)
                 if chart.phase(x, (t,)+b[1:]) is not None]
        assert len(valid) == 1
        t, q = valid[0]
        phases[x] = (q-sum(c*t**j for j, c in enumerate(polynomial))-b[0]*t) % p
        t_values[x] = t
    x = next(iter(envelope))
    u = tuple(row[0] for row in chart.A)
    for direction in _points(p, 2):
        shifted = [tuple((a+j*d) % p for a, d in zip(x, direction)) for j in range(4)]
        values = [phases[y] for y in shifted]
        slope = (t_values[shifted[1]]-t_values[x]) % p
        third = (values[3]-3*values[2]+3*values[1]-values[0]) % p
        assert third == -6*polynomial[3]*slope**3 % p
    assert (t_values[tuple((a+d) % p for a, d in zip(x, u))]-t_values[x]) % p == 1
    assert -6*polynomial[3] % p != 0


@pytest.mark.parametrize("p", [5, 7, 11, 13])
def test_cubic_cancellation_support_and_parseval_are_exact(p):
    roots = _roots(p)
    for alpha in range(1, p):
        sums = [sum((roots[(-alpha*t**3+ell*t) % p] for t in range(p)), roots[0]*0)
                for ell in range(p)]
        zero_set = {ell for ell, value in enumerate(sums) if not value}
        assert zero_set == ({0} if p % 3 == 2 else set())
        norms = [value*_conjugate(value, roots) for value in sums]
        assert sum(norms, roots[0]*0) == p**2*roots[0]
        assert any(value != norms[0] for value in norms[1:])
        # A nonflat ket cannot be one constant-modulus polynomial phase.
        if zero_set:
            assert (p-len(zero_set)) not in (1, p)


@pytest.mark.parametrize("p", [5, 7])
def test_summed_case_quadratic_shift_and_affine_zero_hyperplane(p):
    chart = _chart(p, 2, _circuit("full"))
    polynomial, b = (2, 1, 3, 2), (3, 2)
    record = _record(chart, b, polynomial)
    roots, alpha = _roots(p), polynomial[3]
    linear_values = {}
    c2_values = set()
    for x in _points(p, 2):
        def residual(t):
            q = chart.phase(x, (t,)+b[1:])
            return (q-polynomial[0]-polynomial[1]*t-polynomial[2]*t*t-b[0]*t) % p

        c0 = residual(0)
        c2 = (residual(2)-2*residual(1)+c0)*pow(2, -1, p) % p
        c1 = (residual(1)-c0-c2) % p
        c2_values.add(c2)
        shift = c2*pow(3*alpha, -1, p) % p
        ell = (c1+2*c2*shift-3*alpha*shift**2) % p
        constant = (c0+c1*shift+c2*shift**2-alpha*shift**3) % p
        linear_values[x] = ell
        depressed = roots[constant]*sum(
            (roots[(-alpha*t**3+ell*t) % p] for t in range(p)), roots[0]*0)
        assert record.coefficients.get(x, roots[0]*0) == depressed
    assert len(c2_values) == 1
    assert all(list(linear_values.values()).count(ell) == p for ell in range(p))
    for x in _points(p, 2):
        for y in _points(p, 2):
            xy = tuple((a+b) % p for a, b in zip(x, y))
            assert (linear_values[xy]-linear_values[x]-linear_values[y]
                    + linear_values[(0, 0)]) % p == 0
    if p % 3 == 2:
        assert set(record.coefficients) == {x for x, ell in linear_values.items() if ell}


def test_gate_order_wrong_control_changes_the_record_projector():
    p, polynomial, b = 5, (0, 0, 0, 1), (1,)
    gates = [("F", 0, 1)]  # K=C^dagger=F.
    correct = _run(_basis(p, b), [("F", 0, -1), ("T", polynomial, -1)] + gates, p)
    wrong = _run(_basis(p, b), [("F", 0, -1)] + gates + [("T", polynomial, -1)], p)
    _same_record(correct, _record(_chart(p, 1, gates), b, polynomial), p)
    assert _norm(wrong, p) == _roots(p)[0]
    assert len(wrong.coefficients) == 1
    assert len(correct.coefficients) == p-1
    assert correct.coefficients.keys() != wrong.coefficients.keys()


@pytest.mark.parametrize("p", [5, 7])
def test_nonzero_cubic_hypothesis_is_essential_for_support_classification(p):
    chart, b = _chart(p, 1, [("F", 0, 1)]), (2,)
    no_cubic = _record(chart, b, (0, 0, 0, 0))
    _same_record(no_cubic, _basis(p, b), p)
    assert chart.rank == 1
    assert len(no_cubic.coefficients) == 1
    with_cubic = _record(chart, b, (0, 0, 0, 1))
    assert len(with_cubic.coefficients) == (p if p % 3 == 1 else p-1)


@pytest.mark.parametrize("case", ["rank_zero", "transverse"])
def test_transverse_label_queries_do_not_enumerate_the_magic_variable(case):
    p, b, polynomial = 7, (3, 1), (2, 1, 3, 2)
    chart = _chart(p, 2, _circuit(case))
    record = _record(chart, b, polynomial)
    roots = _roots(p)
    u = tuple(row[0] for row in chart.A)
    matrix = tuple(row+(a,) for row, a in zip(chart.B, u))
    x0 = tuple(a+t for a, t in zip(chart.a, _mv(chart.A, (0,)+b[1:])))
    _, rank = _solve(matrix, (0, 0), p)
    assert rank == chart.rank+1
    for x in _points(p, 2):
        solution, _ = _solve(matrix, tuple(t-a for t, a in zip(x, x0)), p)
        if solution is None:
            assert x not in record.coefficients
            continue
        t = solution[-1]
        q = chart.phase_with_lift(x, (t,)+b[1:], solution[:-1])
        exponent = (q-sum(c*t**j for j, c in enumerate(polynomial))-b[0]*t) % p
        assert record.coefficients[x] == roots[exponent]
    # Multiplying these queried values by arbitrary actual finite amplitudes
    # and summing an enumerable K-label support costs K solves, not K*p.


def test_fourier_and_cubic_signs_with_identity_clifford():
    p, polynomial, b = 7, (1, 2, 3, 4), (2, 5)
    record = _record(_chart(p, 2, []), b, polynomial)
    roots = _roots(p)
    assert record.fourier_power == 1
    assert set(record.coefficients) == {(t, b[1]) for t in range(p)}
    assert all(record.coefficients[(t, b[1])] == roots[
        (-sum(c*t**j for j, c in enumerate(polynomial))-b[0]*t) % p]
        for t in range(p))


def test_qutrit_field_cubic_is_not_the_papers_magic_gate():
    roots3, roots9 = _roots(3), _roots(9)
    assert all(roots3[t**3 % 3] == roots3[t] for t in range(3))
    assert roots9[3] != roots9[0]
    # Canonical qutrit T uses omega_9**(t**3), t=0,1,2, not omega_3.
    assert roots9[1]**3 == roots9[3]
    assert roots9[8]**3 == roots9[6]
    assert sum((roots9[(-t**3) % 9] for t in range(3)), roots9[0]*0)


@pytest.mark.parametrize("case", ["rank_zero", "transverse", "summed", "full"])
def test_score_identity_coefficientwise_for_arbitrary_nonuniform_amplitudes(case):
    # Each coefficient multiplies a_g(x)*conjugate(a_g(y)). Equality for
    # every pair proves the identity for the actual finite lattice weights,
    # without replacing them by a uniform, Gaussian, or quadratic law.
    p, n, b, polynomial = 5, 2, (2, 1), (1, 3, 2, 1)
    gates = _circuit(case)
    record = _record(_chart(p, n, gates), b, polynomial)
    roots = _roots(p)
    forward = [_inverse(gate, p) for gate in reversed(gates)] + [
        ("T", polynomial, 1), ("F", 0, 1)]
    row = {}
    powers = set()
    for x in _points(p, n):
        output = _run(_basis(p, x), forward, p)
        row[x] = output.coefficients.get(b, roots[0]*0)
        powers.add(output.fourier_power)
    assert len(powers) == 1
    direct_power = powers.pop()
    for x in _points(p, n):
        for y in _points(p, n):
            cx = record.coefficients.get(x, roots[0]*0)
            cy = record.coefficients.get(y, roots[0]*0)
            score_coefficient = (p**n+1)*_conjugate(cx, roots)*cy / p**record.fourier_power
            direct = (p**n+1)*row[x]*_conjugate(row[y], roots) / p**direct_power
            assert score_coefficient == direct
    # The '-1' term is exact only for a normalized rank-one target.
    assert _norm(record, p) == roots[0]


def test_proxy_bound_is_mean_square_not_uniform_score_accuracy():
    re, im = sp.symbols("re im", real=True)
    distance_squared = 2-2*re
    fidelity = re**2+im**2
    hs_squared = 2*(1-fidelity)
    assert sp.expand(15*distance_squared-sp.Rational(15, 2)*hs_squared) == (
        15*re**2-30*re+15+15*im**2)
    assert sp.expand(distance_squared-(1-fidelity)-((1-re)**2+im**2)) == 0
    dimension, error = sp.symbols("D error", positive=True)
    overlap_error = error/(3*(dimension+1))
    score_error = (dimension+1)*(2*overlap_error+overlap_error**2)
    assert sp.simplify(score_error/error-sp.Rational(2, 3)-error/(9*(dimension+1))) == 0


def _q_choose(n, k, p):
    if not 0 <= k <= n:
        return 0
    numerator = prod(p**(n-i)-1 for i in range(k))
    denominator = prod(p**(k-i)-1 for i in range(k))
    assert numerator % denominator == 0
    return numerator // denominator


def _subspace_bases(p, ambient, dimension):
    """Enumerate each subspace once by its unique row-reduced basis."""
    for pivots in combinations(range(ambient), dimension):
        free = [(i, j) for i, pivot in enumerate(pivots)
                for j in range(pivot+1, ambient) if j not in pivots]
        for entries in product(range(p), repeat=len(free)):
            rows = [[int(j == pivot) for j in range(ambient)] for pivot in pivots]
            for (i, j), value in zip(free, entries):
                rows[i][j] = value
            yield tuple(tuple(row) for row in rows)


def _symplectic_pair(x, y, p):
    m = len(x) // 2
    return (_dot(x[:m], y[m:])-_dot(x[m:], y[:m])) % p


@pytest.mark.parametrize("p,m", [(5, 1), (7, 1), (3, 2), (5, 2), (3, 3)])
def test_lagrangian_projection_rank_counts_by_exact_subspace_enumeration(p, m):
    # For a fixed position projection W of dimension r, L intersect vertical
    # is W^perp. The remaining choice is a symmetric form on W, giving
    # p**(r*(r+1)/2) Lagrangians for each of [m choose r]_p choices of W.
    counts = [0]*(m+1)
    for basis in _subspace_bases(p, 2*m, m):
        if any(_symplectic_pair(x, y, p) for x, y in combinations(basis, 2)):
            continue
        _, r = _solve(tuple(row[:m] for row in basis), (0,)*m, p)
        counts[r] += 1
    expected = [_q_choose(m, r, p)*p**(r*(r+1)//2) for r in range(m+1)]
    assert counts == expected
    assert sum(counts) == prod(1+p**i for i in range(1, m+1))
    mean_p_rank = Fraction(sum(count*p**r for r, count in enumerate(counts)), sum(counts))
    assert mean_p_rank == Fraction(1+p**(m+1), 1+p)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_conditional_kernel_subspace_count_including_extreme_ranks(p):
    # Ae1 is in im(B) iff ker(B) is contained in e1^perp. Conditional on
    # L=S(vertical), right multiplication by its domain parabolic leaves L
    # fixed and acts transitively on these (m-r)-dimensional pullbacks.
    for m in range(1, 5):
        for r in range(m+1):
            k = m-r
            total = contained = 0
            for basis in _subspace_bases(p, m, k):
                total += 1
                contained += all(row[0] == 0 for row in basis)
            assert total == _q_choose(m, k, p)
            assert contained == _q_choose(m-1, k, p)
            assert Fraction(contained, total) == Fraction(p**r-1, p**m-1)
            assert Fraction(total-contained, total) == Fraction(p**m-p**r, p**m-1)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_q_binomial_rank_generating_function_gives_dimension_independent_probability(p):
    for m in range(1, 9):
        coefficients = [1]
        for i in range(1, m+1):
            updated = [0]*(len(coefficients)+1)
            for r, value in enumerate(coefficients):
                updated[r] += value
                updated[r+1] += p**i*value
            coefficients = updated
        ranks = [_q_choose(m, r, p)*p**(r*(r+1)//2) for r in range(m+1)]
        assert coefficients == ranks
        # F(z)=product_i(1+z*p**i); E[p**r]=F(p)/F(1) telescopes.
        mean = Fraction(sum(value*p**r for r, value in enumerate(ranks)), sum(ranks))
        assert mean == Fraction(1+p**(m+1), 1+p)
        assert (p**m-mean)/(p**m-1) == Fraction(1, p+1)


def test_full_sp4_f3_count_and_inverse_distribution():
    # Enumerate all symplectic bases, not random samples or just a subgroup.
    # The two momentum vectors form an ordered isotropic independent pair;
    # the position vectors are all compatible symplectic complements.
    p, m = 3, 2
    vectors = list(_points(p, 2*m))
    nonzero = vectors[1:]
    counts = [0]*(m+1)
    transverse_counts = [0]*(m+1)
    inverse_counts = [0]*(m+1)
    changed_by_inversion = 0
    for w1 in nonzero:
        line = {tuple(c*x % p for x in w1) for c in range(p)}
        for w2 in nonzero:
            if w2 in line or _symplectic_pair(w1, w2, p):
                continue
            B = tuple((w1[j], w2[j]) for j in range(m))
            _, r = _solve(B, (0,)*m, p)
            row_membership = _solve(tuple(zip(*B)), (1, 0), p)[0] is not None
            # S^-1 has A'=H^T and B'=-B^T in this block convention.
            inverse_B = tuple(tuple(-x % p for x in w[:m]) for w in (w1, w2))
            inverse_u = (w1[m], w2[m])
            _, inverse_s = _solve(tuple(row+(u,) for row, u in zip(inverse_B, inverse_u)),
                                  (0,)*m, p)
            inverse_transverse = inverse_s == r+1
            first = [v for v in vectors if _symplectic_pair(v, w1, p) == 1
                     and _symplectic_pair(v, w2, p) == 0]
            second = [v for v in vectors if _symplectic_pair(v, w1, p) == 0
                      and _symplectic_pair(v, w2, p) == 1]
            for v1 in first:
                _, s = _solve(tuple(row+(u,) for row, u in zip(B, v1[:m])), (0,)*m, p)
                transverse = s == r+1
                assert transverse == (not row_membership)
                for v2 in second:
                    if _symplectic_pair(v1, v2, p):
                        continue
                    counts[r] += 1
                    transverse_counts[r] += transverse
                    inverse_counts[r] += inverse_transverse
                    changed_by_inversion += transverse != inverse_transverse
    assert counts == [1296, 15552, 34992]
    assert sum(counts) == p**(m*m)*prod(p**(2*i)-1 for i in range(1, m+1)) == 51840
    assert transverse_counts == inverse_counts == [1296, 11664, 0]
    assert Fraction(sum(transverse_counts), sum(counts)) == Fraction(1, p+1)
    for r in range(m+1):
        assert Fraction(transverse_counts[r], counts[r]) == Fraction(p**m-p**r, p**m-1)
    # Inversion preserves the uniform distribution, not necessarily the event
    # for an individual S. Clifford displacement never enters this event.
    assert changed_by_inversion > 0


@pytest.mark.parametrize("p", [5, 7])
def test_single_qudit_transverse_measurements_are_complete_but_diagonally_blind(p):
    # For m=1, transverse means B=0, A!=0: every record is flat over F_p.
    # Test every such symplectic matrix and representative displacements.
    # The result concerns this conditioned ensemble only, not m>1 or every
    # modified measurement ensemble. Its failure is bias/nonidentifiability,
    # not a claim that the variance of the old (biased) score diverges.
    roots = _roots(p)
    polynomial = (2, 1, 3, 1)
    for A, G in product(range(1, p), range(p)):
        for a, d in [(0, 0), (1, 2), (p-1, p-2)]:
            chart = _Chart(p, 1, ((A,),), ((0,),), ((G,),), ((pow(A, -1, p),),),
                           (a,), (d,), 0)
            records = [_record(chart, (b,), polynomial) for b in range(p)]
            for record in records:
                assert _norm(record, p) == roots[0]
                assert set(record.coefficients) == {(x,) for x in range(p)}
                probabilities = [value*_conjugate(value, roots)/p
                                 for value in record.coefficients.values()]
                assert all(value == roots[0]/p for value in probabilities)
                # The response to |0><0|-|1><1| is exactly zero, for each
                # individual recorded setting and outcome, before averaging.
                assert probabilities[0]-probabilities[1] == roots[0]*0
                old_score = (p+1)*probabilities[0]-roots[0]
                assert old_score == roots[0]/p
                assert old_score != roots[0]  # True fidelity of |0> with itself.
                assert old_score != roots[0]*0  # True fidelity of |0> with |1>.
            for x, y in product(range(p), repeat=2):
                frame_entry = sum((record.coefficients[(x,)]
                                   *_conjugate(record.coefficients[(y,)], roots)/p
                                   for record in records), roots[0]*0)
                assert frame_entry == int(x == y)*roots[0]
                # On any diagonal density matrix M(rho)=I/p. Applying the
                # original full-ensemble inverse still returns I/p, not rho.
                reconstructed = (p+1)*frame_entry/p-int(x == y)*roots[0]
                assert reconstructed == int(x == y)*roots[0]/p
