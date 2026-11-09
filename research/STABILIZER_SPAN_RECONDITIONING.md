# Stabilizer-span reconditioning: an exact obstruction with an easy escape

7 November 2026. Reviewed all-n derivation and minimum-rank strengthening;
exact classical controls complete. No new learner, novelty, quantum execution, general
learning impossibility or exponential UNRESTRICTED extent claim.

## Selection and native algorithmic question

Start from STATE/TRAPS after Reduced Norm Prescribed Field; the preceding
turn made progress. Corpus been-tried/baselines preceded literature. Compare
three independent directions: arbitrary constant-rank stabilizer learning is
already covered by actual2610.03658 and the stronger2610.06819; finite-field
tensor isomorphism has no new paid receiver from the screened arithmetic/
Levi routes; the full classical sparse-function-field relation counterpart
still lacks a paid constants operation (GENERAL_SPARSE_CONSTANTS_ATTACK.md).
Do not import a numerical-degree Puiseux clock or implicit-determinant sparse
support bound to reopen that route.

Selected high-value question: can EVERY n-qubit pure state of stabilizer rank
at most k be learned from fresh IID copies in poly(n,k,1/epsilon,log1/eta)
time/copies, outputting a classical stabilizer combination within trace
distance epsilon? Unknown components/coefficients, no state-preparation
unitary, conjugate-state oracle, overlap gap, stabilizer frame or branch advice.
This would extend known structured-state tomography to polynomial rank; no
classical input/output speedup is inferred from a quantum-copy input model.

Known mechanism: the bounded-extent learner consumes a bound on the
UNSQUARED minimum coefficient norm Lambda. A polynomial relation
Lambda(psi)<=poly(k) for normalized rank-k states would close the endpoint.
Actual2610.06819 uses SQUARED extent xi=Lambda^2 and proves
xi<=2^{O(sqrt(k log(k+1)))}; its Sections3/8 already contain code merging,
averaged Pauli block elimination and the resulting copy-only learner. The
weaker2610.03658 calls its UNSQUARED norm xi. Preserve this distinction.
Actual2609.20771 Cor8.11 supplies polynomial bounded-extent tomography;
no replacement of ordinary copies by free preparation/reflection is allowed.

Candidate stronger operation: given a k-dimensional subspace V spanned by
known stabilizer rays, replace/augment its dictionary using stabilizer rays
that remain IN V until the normalized positive frame operator has condition
poly(k). If such a frame existed, its lower bound would give polynomial
coefficient norm for every unit vector in V, so the existing learner would
need no supplied dictionary. Finding a frame efficiently would be a further
obligation. The all-n family below DISPROVES EVEN EXISTENCE for this in-span
route. No quantum implementation is justified.

Strong baselines: exact classical stabilizer/tableau and affine-support
simulation for supplied states; explicit computational-basis decomposition;
known rank/extent tomography; and tensor-network contraction under its actual
bond-dimension cost. An exponentially bad SUPPLIED Gram matrix alone would
not disprove reconditioning or optimized extent: the simple prefix family
can be repaired by adding its missing computational-basis tail. The result
below quantifies over ALL in-span stabilizer rays and ALL positive weights.

## 1. Explicit span and its original Gram matrix

For every n>=2, let E={0,e_1,...,e_n} subset F_2^n and m=n+1. Let C_ij be
strings whose first two one positions are i<j. Each C_ij is an affine
subspace of dimension n-j, and these binom(n,2) disjoint cells partition the
complement of E. Write |C_ij> for their normalized uniform stabilizer states,
|p>=|+>^n, and

    V_n = span(|p>, {|C_ij>:i<j}),
    K = dim V_n = binom(n,2)+1,
    |u_E> = m^(-1/2) sum_(x in E)|x>,  r=m/2^n.

The cells are orthonormal and p has a nonzero E component, proving dimension
K. Moreover V_n consists exactly of vectors constant on E and separately on
each C_ij. Its input stabilizer descriptions have polynomial(n) size.
The root-to-cell overlaps are a_ij=2^(-j/2), with

    sum_(i<j) a_ij^2 = 1-r,
    |p> - sum_(i<j) a_ij |C_ij> = sqrt(r)|u_E>.

Thus u_E belongs to V_n. The original arrowhead Gram matrix is
[[1,a*],[a,I]], with eigenvalues 1+sqrt(1-r), 1-sqrt(1-r), and1 of
multiplicity K-2; its determinant is r. These are exact all-n identities,
not an asymptotic inference from a scan.

## 2. Every in-span stabilizer frame remains badly conditioned

A normalized stabilizer state has affine computational support and constant
amplitude modulus on that support. To see this directly, its pure-Z
stabilizers impose affine support equations; the X components of the full
maximal stabilizer group act transitively on that affine solution space.
Their unit-modulus Pauli phases equate the amplitude magnitudes. If |s> belongs to V_n, its coordinates on
E are equal. Either they are zero, or its affine support contains ALL E.
Because E affinely spans F_2^n, the latter support is the whole cube. Its
amplitude modulus is then2^(-n/2), and the equal coordinates on E also have
equal phase. Therefore EVERY normalized stabilizer ray in V_n satisfies

    |<u_E|s>|^2 in {0,r},
    max_(s stabilizer in V_n) |<u_E|s>|^2 = r.

The maximum is attained by p. Let F=sum_l w_l |s_l><s_l| for ANY finite
family of such rays with w_l>=0 and total weight W>0. If it does not span V,
its smallest eigenvalue on V is zero. Otherwise

    lambda_min(F|V) <= <u_E|F|u_E> <= r W,
    lambda_max(F|V) >= Tr(F|V)/K = W/K,
    condition(F|V) >= 1/(K r) = 2^n/[K(n+1)].

The inequality holds for all n>=2; its lower bound exceeds1 from n=9 onward.
It is the all-n asymptotic family, not a small-n condition number, that
falsifies a uniform polynomial bound. This holds regardless of dictionary
size and arbitrary positive reweighting.
It rules out inverse-polynomial conditioning in K=Theta(n^2), even after
unlimited in-span augmentation. It does not lower-bound arbitrary quantum
measurements, signed-LCU constructions, or frames with atoms OUTSIDE V.
A normalization or inverse cannot be declared free to evade this statement.

## 3. Restricted extent is exponential; actual extent is only linear

Let Lambda_V minimize the coefficient l1 norm using only stabilizer rays
in V. Taking inner product with u_E in any such decomposition gives

    1 <= sqrt(r) sum_l |c_l|,
    xi_V(u_E)=Lambda_V(u_E)^2 >= 1/r = 2^n/(n+1).

The displayed root/cell representation gives the matching scale:

    Lambda_V(u_E)
      <= [2^(n/2)+sum_(j=2)^n (j-1)2^((n-j)/2)]/sqrt(n+1)
      <= (4+2sqrt(2))*sqrt(2^n/(n+1)).

So xi_V=Theta(2^n/n). In contrast the obvious computational-basis
representation gives chi(u_E)<=n+1 and UNRESTRICTED xi(u_E)<=n+1. Each
individual basis ray |x>, x in E, lies OUTSIDE V for n>=2, since it is not
constant on E. Their sum lies in V. This is a constructive, polynomial-size
escape from the obstruction, not a hardness example for the native learner.

The actual unrestricted fidelity is exactly

    F_S(u_E) = 9/[4(n+1)]  for every n>=2.

Indeed a d-dimensional affine subspace contains at most d+1 points of the
affinely independent set E. Flat stabilizer amplitudes and the triangle
inequality bound the squared overlap by (d+1)^2/[(n+1)2^d]. The maximum of
(d+1)^2/2^d over integers d>=0 is9/4, at d=2. The uniform stabilizer on
span(e_1,e_2), with other coordinates0, attains the bound. Thus

    4(n+1)/9 <= xi(u_E) <= n+1.

This exact linear scale strengthens the guard against confusing fixed-span
conditioning with global magic. It does NOT prove exact minimal rank,
optimal extent, or a general rank-to-extent polynomial bound.

## 4. A unique minimum-rank span with exponential coefficient cost

The easy u_E example has a smaller decomposition outside V. A tiny algebraic
perturbation removes that qualification. Put B=Q(zeta_8), and enumerate the
K original normalized stabilizer states as s_0,...,s_(K-1). They and
R=sum_(x in E)|x> have coordinates in B. Choose an odd prime p>K of sizeO(K),
let theta=2^(1/p)>0 and set

    epsilon0=2^(-2n)/(8K),
    z=R+epsilon0*sum_(j=0)^(K-1) theta^(j+1) s_j,
    v=z/||z||.

By Eisenstein, [Q(theta):Q]=p; since p is coprime to[B:Q]=4, the tower
law gives [B(theta):B]=p. Suppose a subspace W spanned by stabilizer rays
contains z but not V. Every stabilizer ray has a representative with B
coordinates, so an ordinary B-linear functional ell can vanish on W
without vanishing on V. Then

    ell(R)+epsilon0*sum_j theta^(j+1) ell(s_j)=0

is a polynomial over B of degree at mostK<p. All coefficients must vanish,
forcing ell(V)=0, a contradiction. Normalization does not affect complex
linear-span membership. Thus EVERY stabilizer-spanned W containing v also
contains V. In particular chi(v)=K, and every minimum-rank decomposition
spans exactly V. Global phases of the chosen rays do not change this argument.

Because theta^K<2, q=||z-R||<=2K*epsilon0=2^(-2n)/4. The normalized vector
obeys ||v-u_E||<=2q/sqrt(n+1)<=sqrt(r). Hence every stabilizer s in V has
|<v|s>|<=2sqrt(r). For EVERY minimum-rank decomposition of v,

    (sum |c_j|)^2 >= 1/(4r) = 2^n/[4(n+1)].

On the other hand its displayed outside-V representation through the m=n+1
computational basis atoms and K original atoms has coefficient norm at most

    (m+2K*epsilon0)/(sqrt(m)-2K*epsilon0) <= 2sqrt(m).

Therefore the globally optimized squared extent is <=4(n+1), with at most
K+n+1 terms. A small additive increase in term count removes an exponential
coefficient cost. This disproves polynomial coefficient-cost guarantees for
rank-minimizing decompositions themselves, not just for an unlucky supplied
frame: the cost is exponential in n and superpolynomial in K=Theta(n^2).
It does not prove the exact optimized extent or a learning lower bound.
The tagging is an EXACT-rank statement and is fragile to approximation:
v is exponentially close to u_E, which already has rank at most n+1. No
approximate-rank separation or sample-complexity lower bound follows.

The family has polynomial-size algebraic coefficient descriptions: p=O(K),
B(theta) has degree4p, theta powers have exponent at mostK, epsilon0 has
O(n+logK) bits, and the squared norm is computed from the explicit K-square
stabilizer Gram matrix. Adjoining its positive square root increases degree
by at most2. More explicitly, all original Gram entries have O(n)-bit
coordinates in B. Before reduction, squared-norm theta powers have degree
at most2K<2p; one replacement theta^p=2 suffices. Summing O(K^2) terms
gives coefficient heights O(n+logK) in the B/theta basis. The norm square
root and normalized coefficients consequently have polynomial degree/height
descriptions, without printing 2^n amplitudes. The known outside-span
decomposition has polynomial coefficient
norm and prepares this explicit family to requested precision with charged polynomial
LCU overhead;
no unknown-state preparation oracle or hidden decomposition is granted to
the proposed native learner. The independent field/annihilator/normalization check is complete; the
separate Claude attack and exact coefficient-extraction control also closed.

## 5. What the falsifier changes

A local exchange rule that projects one supplied stabilizer by a Pauli from
another's stabilizer group and retains the result only if it remains in V
cannot have a universal polynomial-conditioning guarantee. Neither can an
arbitrary in-span optimizer, even with unlimited computation. The published
code/projection proof explicitly permits atoms outside the original span;
this is a material resource, not optional cosmetic freedom.

The full polynomial-rank learner and polynomial optimized extent remain OPEN.
This pass closes one concrete stronger mechanism; it does not replace that
native question by an easy supplied-frame problem or claim a general no-go.
Next scientific action must compare independent mechanisms. Do not build a
span-preconditioning backend, projection sweep or dictionary enumerator from
this falsified premise.

## Review, source and control status

Actual sources: audits/sources/stabilizer_rank_priority/{low_rank,extent}.*;
audits/sources/stabilizer_extent/{barnes_wall,mehraban_tahmasbi,marton}.*.
Barnes--Wall v3 Theorem31 gives a supplied-coefficient upper bound and
Problem55 asks for stronger eigenvalue relations. MT v2 Section4 proves a
positive fixed-k Gram gap by compactness. Neither opened source was found
to contain the prefix extremal construction; no such attribution is made.
Priority of the present explicit family is UNKNOWN. The universal polynomial
extent question is explicitly prior work, not a new conjecture here.

Independent review with minimum-rank addendum is CLOSED and fully read:
`audits/reviews/2026-11-07-stabilizer-extent-selection.md`. Parent independently
checked the affine-support quantifiers, weighted trace/Rayleigh bound, global
fidelity, B-linear annihilator, coprime degree and normalization/height ledger.

`audits/controls/stabilizer_span/control.py/.json` passed one exact Sage run.
For n=6, K=16, determinant/residual norm squared7/64 and the full Gram
characteristic polynomial agree. For n=3 all1080 distinct stabilizers are
enumerated over Q(zeta8): global fidelity max9/16; exactly11 in-span rays,
seven with overlap squared0 and four with1/2. This is supplied-description
CLASSICAL stabilizer simulation, not unknown-state tomography.

`audits/controls/stabilizer_span/tagged.py/.json` passed one separate exact
Sage run: n3,K4,p5,epsilon0=1/2048, x^5-2 irreducible overB, degree5/20
relative/absolute. The five theta-coefficient columns are exactly
[R,epsilon0*s0,...,epsilon0*s3], rank4, spanV; each original atom is recovered.
Exact algebraic-real comparisons check the chosen positive root bounds.
Neither control supplies the all-n proof or an exhaustive minimum-rank search.

Both narrow Opus/high reports completed and were fully read, estimates
USD0.286088 (base family) and USD0.220164 (tagging), totalUSD0.506252. No retry,
unknown charge or live call for this pass. Dispositions:

- Base report's support/complex-phase/frame/global-fidelity proofs accepted
  after checking. It notes the condition lower bound exceeds1 only at n>=9;
  the all-n inequality is valid also below that threshold. N2 identity
  u_E=(|++>+CZ|++>)/sqrt3 checks exact squared extent4/3. Loose constants are
  not errors. Its claim that a separation starts at n3 is not established
  by its bounds and is not used. Optional operator-frame extension is outside
  scope. The published extent bound is GLOBAL, as checked in the actual source.
- Tagging report's field/span/exact-rank proof and coefficient bounds accepted.
  Its approximation warning is essential and retained. Its sentence that
  polynomial BIT precision cannot resolve2^-2n is FALSE: O(n) precision bits
  suffice; distinguishing nearby unknown states concerns COPY cost instead.
  Its 'rank pinning only at error exactly0' is too strong: for any fixed n,
  the finitely many lower-rank stabilizer spans are closed, and v lies a
  positive distance away. We prove an easy approximation at the displayed
  exponentially small error, not a zero robust radius or an all-error claim.
  The packet did not include the separate arbitrary-frame condition proof;
  Section2 pays that gate independently. Blanket exact finite-gate preparation
  claims are unnecessary; our preparation statement is to requested precision.

The full polynomial-rank learner and polynomial optimized-extent conjecture
remain OPEN. Minimum-rank-first polynomial coefficient cost and universal
in-span frame conditioning are REFUTED. No full learner, quantum execution,
novelty, approximate-rank hardness, general learning no-go, or exponential
unrestricted extent claim. Independently pivot; no projection/backend sweep.


Milestone: final STATE/title/Now/closed row, five primary-source hashes,
closed review/addendum, both exact-control values/false gates, both completed
API prompt hashes/reports/costs and aggregate ledger checked. Scoped diff
and whitespace PASS. No control rerun, full suite, registry promotion or Git
checkpoint. The broad research goal remains active; independently choose the
next native mechanism rather than extend this closed conditioning route.
