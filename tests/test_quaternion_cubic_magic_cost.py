"""Independent cubic-magic cost controls; no decoder or rank lower bound.

Proof contract: p >= 5 is prime, a != 0 in F_p, omega = exp(2*pi*i/p),
and every stabilizer in a decomposition is normalized. A one-qudit stabilizer
is either |j> or p**(-1/2) sum_x omega**(u*x*x+v*x)|x>. Its overlap with
the normalized cubic seed is respectively 1/sqrt(p) in modulus, or a
degree-three additive character sum divided by p, NOT by sqrt(p).
The additive Weil theorem gives |sum_x omega**f(x)| <= (deg(f)-1)*sqrt(p)
when 0 < deg(f) < p. Here deg(f)=3 and p does not divide 3, so F_stab <= 4/p.

For ANY n, computational postselection of a pure stabilizer is zero or an
unnormalized stabilizer sqrt(q)*|s>, 0 < q <= 1. Equivalently, restrict its
quadratic phase on affine support to a computational slice. Hence adjoining
fixed computational ancillas preserves F_stab exactly: the upper bound is
q*F_stab, and tensoring a maximizing |s> proves the converse. Clifford
unitaries permute stabilizer rays, so arbitrary full Cliffords preserve it.

For a normalized target psi and ANY vector v=sum_j c_j*s_j,
  1-eps <= |<psi|v>| <= sqrt(F_stab(psi))*sum_j |c_j|
follows from reverse triangle and Cauchy--Schwarz when ||psi-v|| <= eps.
Thus sum|c_j| >= sqrt(p)/2 * max(0,1-eps), including unnormalized v.
Its square lower-bounds the homogeneous squared coefficient norm; if v is
normalized this is the usual extent. Squaring 1-eps without eps <= 1 is
invalid. For k vectors from ONE orthonormal stabilizer basis, orthogonal
projection gives eps**2 >= 1-sum_selected |<s_j|psi>|**2 >= 1-4*k/p.
Neither argument gives chi >= 1/F_stab or an Omega(p) arbitrary-rank bound.
They also give no lower bound on nonlinear arithmetic score algorithms or
Born-weighted average score approximation, and are not general runtime bounds.

Primary sources (checked 2026-10-30):
* Howard, arXiv:1501.05319, Eqs. (3)-(5), (32), cubic/Alltop states and Weil.
  https://arxiv.org/pdf/1501.05319
* Bajpai--Bhakta--Garcia, Eq. (13), explicit additive Weil hypotheses.
  https://doi.org/10.1007/s40993-022-00310-3
* Bravyi et al., arXiv:1808.00128, Sec. 6.1, Eq. (127), xi >= 1/F.
  That paper states the qubit version; its witness proof is dimension-free.
  https://arxiv.org/pdf/1808.00128
* Mao--Yi--Zhu, arXiv:2410.13572v2, Appendix B and S4, Eqs. (S39)-(S42).
  For U=(F*T on qudit 1)*C, U^dagger|r,z> =
  C^dagger((p**(-1/2) sum_x omega**(-f(x)-r*x)|x>) tensor |z>).
  Its cubic coefficient is -a != 0; the result applies to every record.
  Their p=3 magic gate uses ninth roots, not omega_3**(a*x**3+b*x*x+c*x).
  https://arxiv.org/html/2410.13572v2

These are consequences of established results, not a new simulation lower
bound. The tests below are finite exact/safe-analytic controls, not a proof
of Weil or an exhaustive check of all primes and all register counts.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import factorial

import pytest
import sympy as sp


PRIMES = (5, 7, 11, 13, 17, 19)
SCALE = 2**80


def _phase(p, a, b=0, c=0):
    return tuple((a*x**3 + b*x*x + c*x) % p for x in range(p))


def _atan_interval(inverse, terms=20):
    partial = sum((Fraction((-1)**j, (2*j + 1)*inverse**(2*j + 1))
                   for j in range(terms)), Fraction(0))
    next_term = Fraction((-1)**terms, (2*terms + 1)*inverse**(2*terms + 1))
    return min(partial, partial + next_term), max(partial, partial + next_term)


@lru_cache(None)
def _cos_intervals(modulus):
    """Outward dyadic bounds, with no floating-point transcendental calls."""
    a_lo, a_hi = _atan_interval(5)
    b_lo, b_hi = _atan_interval(239)
    # Machin's identity and alternating arctan remainders enclose pi.
    pi_lo, pi_hi = 16*a_lo - 4*b_hi, 16*a_hi - 4*b_lo
    result = []
    for residue in range(modulus):
        ratio = Fraction(2*min(residue, modulus-residue), modulus)
        midpoint = ratio*(pi_lo + pi_hi)/2
        radius = ratio*(pi_hi - pi_lo)/2
        terms = 24
        value = sum(((-1)**j * midpoint**(2*j) / factorial(2*j)
                     for j in range(terms)), Fraction(0))
        # Taylor through degree 2*terms-1 (odd coefficient zero), followed
        # by |cos(x)-cos(midpoint)| <= |x-midpoint| for the input interval.
        error = midpoint**(2*terms)/factorial(2*terms) + radius
        lower = max(Fraction(-1), value-error)*SCALE
        upper = min(Fraction(1), value+error)*SCALE
        result.append((lower.numerator // lower.denominator,
                       -((-upper.numerator) // upper.denominator)))
    return tuple(result)


def _squared_sum_polynomial(phases, p):
    """Exact |sum omega**phase|^2 in Q[z]/(1+z+...+z**(p-1))."""
    counts = Counter(phase % p for phase in phases)
    differences = [0]*p
    for left, left_count in counts.items():
        for right, right_count in counts.items():
            differences[(left-right) % p] += left_count*right_count
    return tuple(Fraction(value-differences[-1]) for value in differences[:-1])


@lru_cache(None)
def _real_interval(polynomial, p):
    assert len(polynomial) == p-1
    lower = upper = Fraction(0)
    for coefficient, (lo, hi) in zip(polynomial, _cos_intervals(p)):
        if coefficient < 0:
            lo, hi = hi, lo
        lower += coefficient*lo/SCALE
        upper += coefficient*hi/SCALE
    return lower, upper


def _overlap_polynomial(left, right, p):
    """States are dictionaries support -> phase, each normalized on support."""
    numerator = _squared_sum_polynomial(
        (left[x]-right[x] for x in left.keys() & right.keys()), p
    )
    return tuple(value/(len(left)*len(right)) for value in numerator)


def _two_qudit_stabilizers(p):
    """All rays, via affine support and quadratic phase (odd-prime normal form)."""
    for point in product(range(p), repeat=2):
        yield {point: 0}
    # Nonvertical lines (t,m*t+d), and vertical lines (d,t).
    for slope in (*range(p), None):
        for offset, a, b in product(range(p), repeat=3):
            yield {
                ((offset, t) if slope is None else (t, (slope*t+offset) % p)):
                (a*t*t+b*t) % p for t in range(p)
            }
    for a, b, c, d, e in product(range(p), repeat=5):
        yield {(x, y): (a*x*x+b*x*y+c*y*y+d*x+e*y) % p
               for x, y in product(range(p), repeat=2)}


def test_rational_trigonometric_enclosures_contain_exact_values():
    for modulus, residue, exact in ((3, 1, Fraction(-1, 2)), (4, 1, 0),
                                    (4, 2, -1), (6, 1, Fraction(1, 2))):
        lo, hi = _cos_intervals(modulus)[residue]
        assert Fraction(lo, SCALE) <= exact <= Fraction(hi, SCALE)
        assert hi-lo <= 4
    for p in PRIMES:
        assert _cos_intervals(p)[0] == (SCALE, SCALE)
        assert _squared_sum_polynomial([0]*p, p) == (p*p,) + (0,)*(p-2)
        assert _squared_sum_polynomial(range(p), p) == (0,)*(p-1)


@pytest.mark.parametrize("p", PRIMES)
def test_exact_translation_reduces_every_cubic_to_depressed_cubic(p):
    # This checks ALL nonzero cubic, quadratic and linear coefficients.
    # Translation and the resulting constant phase preserve the sum's modulus.
    for a in range(1, p):
        for b, c in product(range(p), repeat=2):
            shift = -b*pow(3*a, -1, p) % p
            linear = (c-b*b*pow(3*a, -1, p)) % p
            constant = (a*shift**3+b*shift**2+c*shift) % p
            original = _phase(p, a, b, c)
            assert tuple(original[(x+shift) % p] for x in range(p)) == tuple(
                (a*x**3+linear*x+constant) % p for x in range(p)
            )


@pytest.mark.parametrize("p", PRIMES)
def test_all_cubic_stabilizer_overlaps_have_certified_weil_bound(p):
    # A chirp overlap subtracts an arbitrary quadratic and linear term.
    # The preceding exact reduction therefore makes these representatives
    # exhaustive for all (a,b,c,u,v), without floating-point tolerances.
    for a, c in product(range(1, p), range(p)):
        polynomial = _squared_sum_polynomial(_phase(p, a, c=c), p)
        lo, hi = _real_interval(polynomial, p)
        assert hi-lo < Fraction(1, 10**18)
        assert hi <= 4*p, (p, a, c, hi)
        assert hi/(p*p) <= Fraction(4, p)
    assert Fraction(1, p) <= Fraction(4, p)  # Computational basis overlaps.


@pytest.mark.parametrize("p", PRIMES)
def test_chirp_bases_are_exactly_orthonormal_and_mutually_unbiased(p):
    for quadratic, linear in product(range(p), repeat=2):
        squared_sum = _squared_sum_polynomial(_phase(p, 0, quadratic, linear), p)
        expected = p if quadratic else (0 if linear else p*p)
        assert squared_sum == (expected,) + (0,)*(p-2)
    # Completeness is the prime-qudit Pauli classification, not an assumption
    # that arbitrary multi-qudit stabilizers are products of these states.
    assert p+p*p == p*(p+1)


def test_zero_cubic_coefficient_is_not_a_magic_state():
    p = 7
    for b, c in product(range(p), repeat=2):
        seed = dict(enumerate(_phase(p, 0, b, c)))
        assert _overlap_polynomial(seed, seed, p) == (1,) + (0,)*(p-2)
    assert 1 > Fraction(4, p)


def test_characteristic_three_collapse_is_not_the_ninth_root_magic_gate():
    p = 3
    for a, b, c in product(range(1, p), range(p), range(p)):
        assert _phase(p, a, b, c) == _phase(p, 0, b, (c+a) % p)
    # The naive omega_3 cubic is a stabilizer: 4/3 is merely vacuous.
    assert all(x**3 % 3 == x for x in range(3))
    # Mao--Yi--Zhu instead use exp(2*pi*i*x^3/9). At x=1 its phase
    # relative to x=0 is a primitive ninth root, never a cubic root.
    ninth_root_phases = tuple(x**3 % 9 for x in range(3))
    for a, b in product(range(3), repeat=2):
        assert ninth_root_phases != tuple(3*(a*x*x+b*x) % 9 for x in range(3))


@pytest.mark.parametrize("p", (3, 5))
def test_all_two_qudit_stabilizers_postselect_to_zero_or_a_stabilizer(p):
    seen = set()
    branch_sizes = set()
    for state in _two_qudit_stabilizers(p):
        signature = tuple(sorted(state.items()))
        assert signature not in seen
        seen.add(signature)
        total_probability = Fraction(0)
        for ancilla in range(p):
            branch = {x: state[x, ancilla] for x in range(p) if (x, ancilla) in state}
            branch_sizes.add(len(branch))
            probability = Fraction(len(branch), len(state))
            assert 0 <= probability <= 1
            total_probability += probability
            if len(branch) == p:
                a = (branch[2]-2*branch[1]+branch[0])*pow(2, -1, p) % p
                b = (branch[1]-branch[0]-a) % p
                assert all(branch[x] == (a*x*x+b*x+branch[0]) % p for x in range(p))
            else:
                assert len(branch) in (0, 1)
        assert total_probability == 1
    assert branch_sizes == {0, 1, p}
    assert len(seen) == p**2*(p+1)*(p*p+1)


def test_entangled_projection_must_keep_its_probability_factor():
    p = 5
    bell = {(x, x): 0 for x in range(p)}
    seed = {(x, 0): x**3 % p for x in range(p)}
    assert _overlap_polynomial(seed, bell, p) == (Fraction(1, p*p), 0, 0, 0)
    # Postselecting the Bell state's second qudit onto 0 has probability 1/p;
    # renormalizing the branch and discarding that probability loses a factor p.
    assert Fraction(1, p*p) == Fraction(1, p)*Fraction(1, p)


def test_entangling_clifford_preserves_the_exact_full_overlap_distribution():
    p = 5
    seed = {(x, 0): x**3 % p for x in range(p)}
    # C=(F tensor I)*SUM: |x,0> -> sum_u omega**(u*x)|u,x>/sqrt(p).
    # This is not merely a product or computational-basis permutation control.
    encoded = {(u, x): (x**3+u*x) % p for u, x in product(range(p), repeat=2)}
    before, after = Counter(), Counter()
    for state in _two_qudit_stabilizers(p):
        overlap = _overlap_polynomial(seed, state, p)
        before[overlap] += 1
        after[_overlap_polynomial(encoded, state, p)] += 1
        assert _real_interval(overlap, p)[1] <= Fraction(4, p)
    assert sum(before.values()) == 3900
    assert before == after


@pytest.mark.parametrize("p", PRIMES)
def test_every_mao_yi_zhu_outcome_retains_a_nonzero_cubic_coefficient(p):
    for a in range(1, p):
        for b, c, outcome in product(range(p), repeat=3):
            # <x|T^dagger F^dagger|outcome>, with F_xy=omega**(x*y)/sqrt(p).
            direct = tuple((-phase-outcome*x) % p
                           for x, phase in enumerate(_phase(p, a, b, c)))
            assert direct == _phase(p, -a, -b, -c-outcome)
            assert (-a) % p != 0


def test_approximation_triangle_allows_unnormalized_vectors_and_clips_at_zero():
    eps = sp.Symbol("eps", real=True, nonnegative=True)
    # v=(1-eps)*psi makes the reverse-triangle step sharp for 0<=eps<=1.
    assert sp.expand((1-(1-eps))**2) == eps**2
    for error in (sp.Rational(0), sp.Rational(1, 4), sp.Rational(3, 4), sp.Rational(1)):
        overlap = 1-error
        assert overlap >= 0
        assert sp.Abs(overlap) == 1-error
        # Its computational stabilizer decomposition has squared l1 cost
        # p*(1-error)^2, consistent with (not proving) the universal p/4 bound.
        assert 7*overlap**2 >= sp.Rational(7, 4)*(1-error)**2
    assert 1-sp.Rational(1, 4) < 1-sp.Rational(1, 4)**2
    # v=0 has error 1 and zero cost, hence is feasible also at eps=2.
    # Squaring the negative lower bound 1-eps would give a false positive cost.
    assert sp.Rational(7, 4)*(1-2)**2 > 0
    assert sp.Rational(7, 4)*max(0, 1-2)**2 == 0


@pytest.mark.parametrize("p", (5, 7))
def test_all_single_basis_subsets_obey_exact_projection_error_bound(p):
    seed = dict(enumerate(_phase(p, 1)))
    bases = [[{x: 0} for x in range(p)]]
    bases.extend([[dict(enumerate(_phase(p, 0, a, b))) for b in range(p)]
                  for a in range(p)])
    for basis in bases:
        probabilities = [_overlap_polynomial(seed, vector, p) for vector in basis]
        assert tuple(map(sum, zip(*probabilities))) == (1,) + (0,)*(p-2)
        for mask in range(1 << p):
            selected = [probabilities[j] for j in range(p) if mask & (1 << j)]
            mass = tuple(sum((row[k] for row in selected), Fraction(0))
                         for k in range(p-1))
            error_squared = tuple((1 if k == 0 else 0)-value for k, value in enumerate(mass))
            lower, _ = _real_interval(error_squared, p)
            assert lower >= 1-Fraction(4*len(selected), p)
            # Pythagoras makes this the minimum error over ALL coefficients
            # on the selected orthonormal vectors, normalized or otherwise.


def test_rank_two_cancellation_refutes_inverse_fidelity_rank_inference():
    p = 7
    # psi=(|0>-|+>)/sqrt(2-2/sqrt(7)) has an exact two-term decomposition.
    # For |0> and |+>, fidelity=(1-1/sqrt(p))/2 < 1/2. For all other
    # computational/linear-chirp states it is 1/(2*p-2*sqrt(p)) < 1/2.
    # For each genuine quadratic chirp, the exact Gauss sum below has
    # modulus sqrt(p). Triangle bounds the numerator by 2/sqrt(p), giving
    # fidelity <= 2/(p-sqrt(p)) < 1/2 since sqrt(7) < 3 = p-4.
    root = sp.sqrt(p)
    for a, b in product(range(1, p), range(p)):
        assert _squared_sum_polynomial(_phase(p, 0, a, b), p) == (p,) + (0,)*(p-2)
    bounds = ((1-1/root)/2, 1/(2*p-2*root), 2/(p-root))
    assert p < (p-4)**2
    assert all(bound < sp.Rational(1, 2) for bound in bounds)
    # The exhaustive prime-qudit classification covers ALL stabilizers, so
    # F_stab < 1/2, while chi=2 (it cannot be 1 since F_stab<1).
    gram = sp.Matrix([[1, 1/root], [1/root, 1]])
    coefficients = sp.Matrix([1, -1])/sp.sqrt(2-2/root)
    assert sp.simplify((coefficients.T*gram*coefficients)[0]) == 1
    coefficient_l2_squared = sp.simplify((coefficients.T*coefficients)[0])
    assert coefficient_l2_squared > 1
    coefficient_l1_squared = sp.simplify(4/(2-2/root))
    assert coefficient_l1_squared > 2
    # Cauchy gives ||c||_1^2 <= k*||c||_2^2, NOT <= k for nonorthogonal terms.
    assert sp.simplify(coefficient_l1_squared-2*coefficient_l2_squared) == 0
