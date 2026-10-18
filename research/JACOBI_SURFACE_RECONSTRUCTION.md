# Exact Surface Counts: CM Reconstruction And A Real Classical Attack

2026-10-17. Local mathematical derivations, review pending. No novelty claim.

**Superseding classical comparison:** the [known-norm reduction](JACOBI_KNOWN_NORM_REDUCTION.md)
identifies a published deterministic polynomial-time classical recovery
theorem that applies to the public ideal AND known relative norm. Under the
stated Jacobi/primary identities this removes the prime-conductor asymptotic
quantum opening, without needing a uniform LLL success theorem. Its actual
theorem inputs are constructed and checked; the imported recovery algorithm
is not implemented here. This page retains the original experiment and real
LLL results, not a current claim that quantum PIP is needed.

## Research Decision

The preceding HDQI source remained unresolved. We compared independent routes:

- The new [lattice Gaussian sampler](https://arxiv.org/abs/2605.20133) offers a
  quadratic improvement, not an identified polynomial lattice breakthrough.
- Curve point counting is NOT a new opening:
  [Kedlaya](https://arxiv.org/abs/math/0411623) already gives quantum polynomial time
  in genus and log field size. We rejected a proposed Fermat-curve application
  as rediscovery before implementation.
- Exact Jacobi reconstruction from compact number-field data is a different
  mechanism from preparing a hard interference source. [Tal's modular
  factorial preprint](https://arxiv.org/abs/2607.29453) uses known quantum
  principal-ideal/unit methods and phase disambiguation for repeated-character
  sums. [Biasse and Song](https://arxiv.org/abs/2510.02280) provide the underlying
  S-unit framework. These are external research results, not repo routines.

Selected question: can that arithmetic yield a charged exact point-count
reduction for split Fermat SURFACES, and what can a serious classical attack
already reconstruct? This is a candidate reduction experiment, not a new
end-to-end quantum implementation or a refutation of the cited papers.

## Problem, Input And Intended Advantage

Count projective solutions over F_p of

    X^d + Y^d + Z^d = W^d,      p prime, d>=3, d|(p-1).

p and d are public binary integers. A verified order-d root eta in F_p is
public, not a hidden function. The character is defined by
chi(x)=zeta_d^j when x^((p-1)/d)=eta^j; a table of size d, not p, implements
this evaluator. The EXHAUSTIVE native reference additionally makes a size-p
table, explicitly charged and never used by the public-ideal attack.

The proposed quantum target is polynomial in d and log p, NOT polynomial
in log d. To get a polynomial succinct-input algorithm, require an explicit
growth promise d=poly(log p). Fixed d already has strong classical arithmetic
methods and cannot establish an asymptotic separation. No classical lower
bound or best-known-algorithm separation is claimed for growing d here.

The prospective mechanism is a carry-described cyclotomic ideal, a real
principal-ideal/unit reconstruction, exact local residues and an integer
point-count lift. No coherent hidden oracle, source preparation assumption
or free full-field sum is part of that proposed pipeline. The quantum
principal-ideal/unit routines and generic three-character extension have
NOT been implemented or independently reviewed by this pass.

## Exact Reduction

Let J(a,b,c)=sum_(x+y+z=1) chi^a(x)chi^b(y)chi^c(z), extending ALL characters
by zero at0. For a,b,c in1..d-1 with a+b+c !=0 mod d,

    #surface = p^2+p+1 + C,
    C = sum_(admissible ordered triples) J(a,b,c).

Character orthogonality gives this projective formula. The number of terms is
B=(d-1)(d^2-3d+3), and each has absolute value p. Thus |C|<=Bp. C is an
integer, not an approximate complex number. If p>2B, C mod p^2 has a unique
lift in [-Bp,Bp]. If p<=2B=O(d^3), a full-field classical convolution count
costs polynomial time in d. The prototype rejects ambiguous residues rather
than silently using centered rounding. It explicitly counts the projective
boundary, not just the affine chart.

All triple sums are computed by exact two-character sums and a convolution
identity. When a+b=0, the missing zero-convolution mass matters:
J(a,-a,c)=p*chi^a(-1). Dropping it changes the norm and the point count.

## Ideal And Valuation Conventions

Use K=Q(zeta_d), the monic cyclotomic integral basis, and POSITIVE reductions
zeta_d -> eta^t, t in(Z/dZ)^*. The generalized Stickelberger carry profile is

    e_t = 2-floor(((at mod d)+(bt mod d)+(ct mod d))/d).

It satisfies e_t+e_(-t)=2 and sum e_t=phi(d). The inverse-root convention
has complementary carries; copying its labels would be wrong. Every native
sum is checked at all split primes modulo p^3, including exact valuations2.
Teichmuller roots use eta_t^(p^(h-1)) mod p^h. The exact relative norm is
J*conjugate(J)=p^2 in the FIELD, not merely a floating magnitude at one place.

To reduce J/p^v to h unit digits requires h+v input digits. The native helper
demonstrates this and rejects inversion of p modulo p^h. It does NOT implement
valuation-aware division of arbitrary compact quantum outputs. That bit-cost
extension is still an explicit obligation; known repeated-character residue
theorems must not silently be treated as arbitrary three-character routines.

## Strong Classical Baseline: Public Ideal LLL

This deliberately instantiates established classical arithmetic rather than
claiming LLL/Jacobi reconstruction as new:
[Buhler and Koblitz (1998)](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/article/lattice-basis-reduction-jacobi-sums-and-hyperelliptic-cryptosystems/211979CB954028EF8899B3FB49930091)
gives a fixed-small-conductor algorithm polynomial in log p. Standard
[odd-prime Jacobi primary congruences](https://www.impan.pl/shop/en/publication/transaction/download/product/82645)
also predate this project; the three-character form below has a local proof.

We build the actual ideal lattice using ONLY public p,d,eta and carries:
coefficient rows satisfy A(eta_t)=0 mod p^e_t. Sequential modular kernels
have checked determinant p^phi(d). LLL returns rows which are tested for
A*conjugate(A)=p^2. Ideal membership plus that norm gives equality of
principal ideals. Kronecker's theorem then leaves only a root of unity.

All64 selected small-input ideals yield a balanced row. This is an actual
attack, not an assumed classical dominance theorem. No balanced row is ever
selected by comparing it to the true Jacobi sum. Failure to find such a row
returns UNKNOWN, not a negative result or evidence of quantum advantage.

## Prime Conductors Need No Phase Oracle

For odd prime conductor ell, lambda=1-zeta_ell, the THREE-character sum obeys

    J(a,b,c) = 1 mod lambda^2.

Elementary derivation: expand zeta^e=1-e*lambda modulo lambda^2. The number
of nonzero triples summing to1 is p^2-3p+3, congruent to1 mod ell. For any
one coordinate, fixing x!=1 leaves p-2 choices for the other two; at x=1
there are p-1, but log_chi(1)=0. The total linear coefficient is therefore
divisible by ell, since sum_(x!=0) log_chi(x) is divisible by ell for odd ell.
As ell is divisible by lambda^(ell-1), both required congruences follow.

In Z[zeta_ell]/lambda^2, test A(1)=1 and A'(1)=0 mod ell. The2ell roots of
unity have distinct residues in this quotient. Thus this primary condition
selects the correct root multiple of a balanced generator CLASSICALLY, with
no phase estimate or true character sum. It does not replace norm
normalization: multiplying by the non-root unit1+zeta_5 preserves the ideal
but fails the relative-norm test. Composite conductors are not covered by
this implemented primary-normalization proof.

## Live End-To-End Classical Result

LLL plus primary normalization reproduces all six prime-conductor native
surface controls. More importantly, at

    p=2305843009213693951, d=11,
    #surface=5316911983139663865501362488876572959.

The public computation uses51 distinct ideal profiles for200 symmetric
triple records. NO p-sized table, true Jacobi sum or phase oracle is used.
The tests independently replay norm, ideal membership, determinant/index,
primary congruences, complete multiplicities, rationality and the Weil bound
without rerunning LLL. This is a checkable algebraic certificate under the
stated local derivation, NOT an independently enumerated 61-bit field or
formal theorem proof. No worst-case growing-conductor LLL success theorem
has been established. In particular, a finite classical success is not a
general dequantization. Cubic controls are explicitly already classical:
#surface=p^2+7p+1 for the split primes, not a quantum benchmark.

Fourteen native small-field controls retain1032 symmetric triple records,
64 selected ideal attacks and246 synthetic coarse-phase checks. The latter
only calibrate root spacing; no quantum phase estimation was executed and
prime-conductor primary normalization makes those checks unnecessary for
the implemented public reconstruction.

## Reproduce And Next Scientific Work

Run `python theorems/jacobi_surface_reconstruction.py --write` and
`python -m pytest tests/test_jacobi_surface_reconstruction.py -q`.

That next question has now been answered at the appropriate theorem level:
known-norm recovery, not unproved uniform LLL success, is the classical
baseline. Read JACOBI_KNOWN_NORM_REDUCTION.md and run its separate producer.
Independent review of the local application is still needed. Do not spend
another pass scanning primes or implementing known quantum PIP for this
prime-conductor proposal. A broader arithmetic candidate must first specify
an output not already supplied by the known-ideal/known-norm theorem; unknown
norms and composite root ambiguities are not automatically quantum openings.
No central candidate/general negative or groundbreaking algorithm is claimed.
