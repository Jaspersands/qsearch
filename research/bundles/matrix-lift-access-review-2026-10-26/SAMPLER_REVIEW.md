# Independent Review: Prime-Class Sampling For Exact Halving

Date: 2026-10-26. Verdict: **ACCEPT CONDITIONALLY**, with a sample-accounting
clarification. This is a reasoning audit, not a backend implementation.

## 1. Findings And Scope

The replacement in `../prime-sampler-halving-2026-10-26/SAMPLING.md` is sound:
fresh samples with the stated mod-two character bound suffice for verified
relation detection and generation of the entire rational 2-primary group.
Uniformity inside that group is unnecessary. Full zeta input is removed
**for this sampling role**, conditional on the separately supplied exact
order and arithmetic contracts. No circular torsion-basis input is needed.

Three qualifications should accompany the claim:

1. **`4s` counts outer generation proposals, not all sampler calls.** Each
   relation-lattice computation also consumes fresh samples. The note's
   lines 74-84 are correct read this way, but `4s` is not a total-cost bound.
2. Freshness must hold **conditional on the entire prior adaptive history**.
   Marginal Fourier bounds, a cached sample bank, or repeatedly using one
   sample do not suffice. Exact verification protects correctness but not
   termination under such substitutes.
3. A represented prime is not itself a represented degree-zero class.
   Section 6 below supplies a bounded conversion, including its sign. It
   needs no labels, halving oracle, or torsion basis, but its cost remains.

This report does not revisit the multi-list auxiliary-divisor search or its
degree budget. It supersedes only the sampling prerequisite of Section 5
of the auxiliary review, not that review's exact-order or pairing premises.
The existing `REVIEW.md` in this directory is unchanged.

## 2. Exact Input Contract

Let C/F_q be smooth, projective and geometrically connected, with g >= 1,
q odd, and a known rational point O. Put J = J_C(F_q), Q = J/2J, and
H = J[2^infinity]. Assume:

- The **true exact** order h = 2^s M, with M odd, is supplied.
- Exact equality, addition, scalar multiplication, and bounded class
  representations have charged polynomial cost.
- An effective perfect pairing e: J[2] x Q -> {+1,-1} is available on
  supplied represented arguments, with the correct normalization. The
  alternating Weil pairing restricted to rational torsion is not a substitute.
- Each new sample X obeys, conditional on the previously revealed history,
  `|E chi(X)| <= 1/2` for every nontrivial character chi of Q. Fresh independent
  calls to the same sampler meet this condition. For the prime construction,
  the degree n is fixed independently of its random outputs.

These are promises, not properties certified by `sampler_contract.py`.
Its booleans about exact verification and access are declarations. Its
integer and rational calculations check consequences of the promises.

Only the one-sided bound `E chi(X) <= 1/2` is needed below; the absolute
bound is a convenient stronger hypothesis.

## 3. Relations, Independence And Las Vegas Stopping

For supplied T_1,...,T_t in J[2], let phi: F_2^t -> J[2] send coefficients
to their group sum, and put U = im(phi), r = dim(U). The sign matrix formed
from b sample rows always satisfies `ker(phi) subseteq ker(A)`.

For each nonzero T in U, perfection makes e(T,.) a nontrivial character.
Thus its one-row probability of being missed is at most 3/4. Conditional
freshness gives a b-row miss probability at most `(3/4)^b`. Union bounding
over the **nonzero elements of U**, not over independent test events, gives

```text
Pr(ker(A) != ker(phi)) <= (2^r - 1)(3/4)^b.
```

No independence between different T's within one row is being assumed.
For t >= 1, b = 4(t+1) makes this bound less than 1/4, since

```text
(2^r-1)(3/4)^(4(t+1)) < (81/256)(81/128)^t < 1/4.
```

Evaluate a basis of ker(A) by exact group addition. If all basis vectors
map to zero, then ker(A) is contained in ker(phi), proving equality by the
reverse inclusion already known. This certifies **all** relations, even
when the T_i are dependent, zero, or not part of a known torsion basis.
For t = 0 return the zero relation space without sampling.

On failed verification, use fresh batches. The conditional success
probability is greater than 3/4 at every retry, so expected batches are
less than 4/3 and termination is almost sure. False acceptance is zero
under exact arithmetic. Consequently an unbounded sequence of adaptive
calls needs no accumulated Monte Carlo error budget. A fixed retry cap
must instead return an inconclusive result, never an unverified answer.

This is the same verification mechanism as
[Bruin, Algorithm 3.10](https://arxiv.org/html/1003.2563); the new argument
replaces its uniform-row rank estimate.

**Failure control.** One random sample repeated b times retains its one-row
miss probability. With two independent torsion directions it can never
give two independent rows. Verification may reject forever. Likewise,
rows already conditioned on generation success cannot automatically be
reused as fresh relation tests.

## 4. Generation Under Highly Nonuniform Laws

Multiplication by M kills J's odd component and is an automorphism on H.
It induces an isomorphism from Q to H/2H. Every proper subgroup H' of the
finite abelian 2-group H is contained in an index-two subgroup K. Pulling
the nontrivial character of H/K back along multiplication by M gives a
nontrivial character of Q. Therefore, conditional on the current H',

```text
Pr(MX notin H') >= Pr(MX notin K) >= 1/4.
```

This proof makes no assumption about masses within parity classes or
about how closely the distribution resembles uniform H. Its support can
be tiny compared with |H|.

The reviewed saturation algorithm gives the exact relation lattice of
the retained generators and each candidate, hence the exact order of the
generated subgroup. Keep a candidate only after a certified strict order
increase. Each such increase multiplies the order by at least two, so
there are at most s increases. The conditional waiting time for each is
at most four proposals in expectation. Thus `E N_outer <= 4s`, with
almost-sure termination; for s = 0 no H-generation samples are needed.
Stop at the supplied order 2^s, not after a quiet period or a guessed rank.

For completeness, the saturation invariant is `L subseteq ker(phi)` for
phi: Z^t -> H, starting from `L = 2^s Z^t`. Integral halves of suitable
vectors of L represent all order-two elements of Z^t/L. Their images are
supplied order-two points, so Section 3 applies before any torsion basis
exists. Adjoining their verified zero-image relations reduces the lattice
index. If no further relation exists, a nontrivial remaining 2-group
kernel would have an order-two element, a contradiction. This proves exact
saturation without a group discrete-log oracle.

After full H is obtained, its integer presentation supplies H[2] and the
reviewed doubling congruence. For a target x, solving `2u = Mx` in H gives
`y = u - ((M-1)/2)x`, with `2y = x`. Nonsolvability is also certified after
full H has been generated. No odd-component discrete logarithm is needed.

**Explicit accounting qualification.** For s >= 1, retained lists have
at most s generators and candidate lists at most s+1. A saturation call
on t generators has at most st strict index reductions plus a terminal
round. Each relation round uses at most `16(t+1)/3` expected fresh sample
rows by Section 3. Thus a loose bound is O(s^3) row draws per saturation
call and O(s^4) row draws during generation, in addition to O(s) outer
proposals. Each row can require O(s) pairings. These are nonoptimized
polynomial counts, not an implementation or a practical runtime estimate.
All prime-generation, representation, scalar-multiplication and pairing
costs must be multiplied in. Conditional bounds justify this accounting
despite adaptive stopping.

An inaccurate h is not repaired by these certificates: it can invalidate
the starting annihilator, the projection by M, or the final completeness
test. Only the subgroup order is certified internally.

## 5. Prime Degree, Equality And The Sampling Source

Write B_n for the number of degree-n closed prime divisors and
`C_n = (g+1)(n+6)`. The earlier character estimate gives

```text
|n sum_(deg P=n) chi([P-nO])| <= C_n q^(n/2),  chi nontrivial,
|n B_n - q^n| <= C_n q^(n/2).
```

The estimates use degree-zero classes. Analytically, a character gives an
unramified quadratic cover with O split; this excludes the constant-field
cover and its degree-parity obstruction. The cover has genus 2g-1.
Comparing point counts and removing proper-divisor contributions gives
the constants in the earlier review: `(6g-2)+n(g+1) <= C_n` for a nontrivial
character and `2g+1+n(g+1) <= C_n` for the prime count. This is a proof
using covers, not an instruction to construct their equations or first
find all characters. The point-count/prime-count identity and Weil-bound
method are also given in
[Elkies et al., Lemma 2.1](https://arxiv.org/html/math/0208060).

Set z = q^(n/2). Under `q^n >= 16 C_n^2`, we have z >= 4C_n, so

```text
B_n >= 3q^n/(4n) > 0,
|E chi([P-nO])| <= C_n/(z-C_n) <= 1/3 < 1/2.
```

This includes equality, proves nonemptiness, and is stronger than needed.
There is no factor |Q| in a bound for a single character. The character
argument is analytical and does not provide or require a class-label oracle.

For q = 100003, n = g+1 already satisfies the inequality at g = 1. Its
left/right ratio increases at successive g by

```text
q * ((g+1)/(g+2))^2 * ((g+7)/(g+8))^2 > q/16 > 1.
```

Hence the smallest sufficient n is at most g+1. It is O(log(g+1)) for
this fixed q. This conclusion is not asserted uniformly for all small q.
For g = 41,81,161,321,641 the smallest sufficient n is 2.

**Primary-source contract.**
[Bruin, Algorithm 3.2](https://arxiv.org/html/1003.2563) takes
`n <= i*ell-2g` and truncation `S^(2i+2)`, returning a uniform degree-n
prime represented by `H^0(L^i(-P))`; no zeta polynomial is input. Its
component-count rejection correction is essential.
[Algorithm 3.8](https://arxiv.org/html/1003.2563) uses `S^(7)` for supplied
classes and a pairing order dividing q-1. Sections 3.3-3.5 and Algorithm
3.11 retain zeta/Frobenius inputs for their respective constructions.

With ell = 2g+2 and i = 2, `n <= g+1 <= 2ell-2g`, so truncation 6
suffices for prime sampling and 7 covers the order-two pairing. The output
law is uniform on **closed primes**, not uniformly chosen extension-field
points or an uncorrected choice of a factor of a random section. It is
also not a divisor sampled inside one fixed degree-n linear equivalence
class. Exact independent calls must retain these distinctions.

For an explicit cost check, let k = 2ell+1-g and N = floor(2ell/n).
For each degree-n prime, exactly `q^(k-n)-1` of the `q^k-1` nonzero
sections vanish on it. With the corrected factor selection, the
per-trial probability of returning some prime is

```text
p = (B_n/N) * (q^(k-n)-1)/(q^k-1)
  >= 3(1-q^(-g-1))/(8ell).
```

Thus expected section trials are at most `8ell/[3(1-q^(-g-1))]` under
our stronger numerical condition. Neither B_n nor the zeta polynomial
must be computed to run the rejection rule; B_n appears only in this
analysis. Finite-algebra decomposition and finite-field factorization
still cost work. They are not being replaced by generic polynomial solving.

## 6. A Noncircular Conversion To [P-nO]

Here is an explicit deduction from the recovered graded algebra. Let L
be the embedding line bundle, ell = deg(L) = 2g+2, and set
`R_j = H^0(L^j)`, `W_D = H^0(L^2(-D))`.
The sampler returns W_P. The recovered rational point O supplies W_O as
the kernel of evaluation on R_2; its projective coordinate scaling does
not affect this kernel.

For effective D,E with `deg(D+E) <= ell`, compute

```text
U = span(W_D W_E) subset R_4,
W_(D+E) = {z in R_2 : z R_2 subset U}.
```

Both residual line bundles L^2(-D), L^2(-E) have degree at least
ell >= 2g+1, so their product fills `H^0(L^4(-D-E))`. Since L^2 is
globally generated, dividing by all R_2 imposes exactly vanishing along
D+E. These are finite linear systems, not a support-disjointness argument;
repeated copies of O and the case P=O when n=1 are allowed.
The multiplication and division criteria are
[Khuri-Makdisi, Lemmas 2.2-2.3](https://arxiv.org/html/math/0105182).

Construct, with at most O(ell) such operations,

```text
A = P + (ell-n)O,     B = ell O,
deg A = deg B = ell,  A-B = P-nO.
```

W_B and the padding spaces for multiples of O may be precomputed. In
Bruin's convention W_D represents `c_D = [L(-D)]`; hence the desired
class is **c_B - c_A**, not c_A - c_B. Khuri-Makdisi's divisor convention
has the opposite sign, so an adapter must choose one convention consistently.
Medium-model subtraction uses products through degree 5; see
[Khuri-Makdisi, Section 5, Proposition/Algorithm 5.1](https://arxiv.org/html/math/0105182).
Thus padding through degree 4 followed by bounded subtraction fits within
the available truncation 7.

This provides a represented class for every sampled prime without first
knowing a torsion basis, solving a halving problem, evaluating a class
label, or finding a canonical divisor. No rejection based on class or
support is required. Deterministic changes of representatives do not
alter the class law. An arbitrary nonzero section of L supplies an
effective representative of its class when needed by the group model.
The rational base point O and the embedding L need not satisfy L = ell O.

This closes the normalization *existence and polynomial-operation* gap
for the internal sampler, not an implementation gap. Correct norm and
trivialization handling in the pairing remains part of the arithmetic
contract. Adapters back to the original native divisor/evaluation task
are separate from producing these internal samples.

## 7. Controls And Remaining Access

Read-only execution of the parent sampler tests: **19 passed**. The new
`sampler_independent_controls.py` uses only exact rational finite-group
enumeration; its output is `sampler_control_results.json`.

- It computes relation-batch failure probabilities by dynamic programming
  on binary subspaces for ranks 1,2,3. Each is below the claimed bound.
- For T = (e1,e2,e1+e2), all 16 two-row sequences were checked: 6 certify
  exactly the true relation space, and 10 are rejected by basis verification.
- On C8 x C4, a law supported on 4 of 32 elements has maximum nontrivial
  mod-two bias 1/2 and total-variation distance 7/8 from uniform. Exact
  subgroup-state recursion gives expected generation time 20/3 proposals,
  compared with the bound 4s = 20. Its minimum reachable proper-subgroup
  escape probability is exactly 1/4. Three other groups pass the same checks.
- Correlated-reuse controls retain one-row failure, or rank deficiency
  forever, despite acceptable single-sample marginals.
- Exact integer degree checks include genera up to 10^16. They verify the
  inequality, not a curve sampler or the analytic character theorem.

These controls do not implement finite-field divisor decomposition,
pairings, or the recovered curve's Jacobian. The parent finite-group
halving test is useful, but its fixed seed and shared lattice code are
not independent proof of the geometric access contract.

The resulting dependency chain is now:

```text
complete AG matrix promise -> recovered curve, L, O -> fixed truncation 7
    -> corrected prime sampler -> represented [P-nO]
    + exact h + normalized perfect pairing + bounded exact arithmetic
    -> certified H presentation -> rational halving
```

Full zeta data are not a necessary input to the sampling branch of this
chain. They may still be how h is obtained. The relaxation does not turn
Bruin's general exact-uniform-J sampler or Frobenius-based torsion
algorithm into zeta-free algorithms; it replaces their sampling role in
this particular construction by a different proof.

**Sharp next step:** isolate acquisition and certification of the true h
for the recovered curve, with explicit input representation and bit cost.
If h is promised, the sampling objection is resolved at the theorem level;
source-matched finite-field decomposition, class conversion and pairing
costs still need to be charged in any end-to-end bound. If h is not promised,
state its computation as the remaining gate rather than claiming a zeta-free
native solver. No generic polynomial-system solver or native-search
complexity conclusion follows from this audit.
