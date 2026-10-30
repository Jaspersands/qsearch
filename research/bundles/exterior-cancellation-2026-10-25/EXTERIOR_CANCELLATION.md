# Exterior Compression Of Public-Label Cancellation

2026-10-25. Status: local constructive deduction with exact arithmetic
controls. Not independently reviewed, formally verified, or novelty
certified. This is a CLASSICAL subroutine for a proposed quantum receiver,
not a new quantum algorithm or a claim of advantage on a native problem.

## Scientific Question And Prior Art

Can the public diagonal-equation step be implemented for genuine power
index greater than three, without full-field search or a hidden SDE oracle?
Can its collision construction retain the same witness guarantee using
less information than the full tensor representation?

The starting point is Ivanyos and Santha,
[Solving systems of diagonal polynomial equations over finite fields](https://arxiv.org/html/1503.09016v2),
especially Proposition 10 and Sections 3.2-3.3. Their method finds disjoint
power-weighted representations, then combines them. The existing repository
cubic backend implements that construction with tensor coordinates. This
pass changes its intermediate invariant to an exterior power and gives
the full derivation below. Do NOT attribute the underlying collision
method or fixed-degree polynomial-time SDE solvability to this project.

Targeted searches for diagonal equations, exterior/alternating compression,
and colliding representations found no matching variant. This limited
search does not establish novelty or exclude better known algorithms.
The local independent Rees review predates this argument and does not
validate it.

## Exact Input Contract

Given an odd prime p, degree 1 <= k < p, positive public equation width r,
and explicit columns v_i in F_p^r, output s != 0 such that

    sum_i s_i^k v_i = 0.

The columns are measured/public labels, not a supplied solution, hidden
subgroup, or extra coherent oracle. No assumption of randomness, full
rank, nonzero entries, or distinct columns is used. Zero scales are
allowed but are not invertible dilations: a receiver must discard their
registers while retaining their acquisition cost.

Set d=gcd(k,p-1), M=(p-1)/d. Choose u satisfying
u*(k/d)=1 mod M. A witness gamma for exponent d lifts by s_i=gamma_i^u,
because ku=d mod(p-1); zeros stay zero. The implementation verifies the
ORIGINAL k-moment on the original complete matrix after lifting.

The public bank is chosen from p,k,r BEFORE acquiring labels. The code
checks a canonical plan and rejects an insufficient bank, but cannot
prove a caller's chronology or absence of resampling. Those remain receiver
integration obligations. It charges every supplied column, including
unused suffixes and zero-scale slots. It does not lower the bank after
observing rank. A smaller width is legitimate only if a corresponding
public source subspace is certified in advance.

## Collision Lemma

Let d divide p-1. Define

    B_d(r) = product_{j=0}^{d-1} (r * binom(d-1,j) + 1).

From B_d(r) arbitrary columns, the algorithm constructs disjoint sets
P,N, with P nonempty, and nonzero gamma_i such that

    sum_{i in P} gamma_i^d v_i = sum_{i in N} gamma_i^d v_i.

The negative side may be empty; in that case the positive side already
represents zero. This is a signed collision, NOT automatically a zero sum
when d is even.

### Invariant And Coordinate Compression

Let E=F_p^d with ordered basis e_0,...,e_{d-1}. Choose one nonzero
representative zeta_a per dth-power class. Define lambda(e_a)=zeta_a and
W=ker(lambda). At level j, maintain

    T = sum_i epsilon_i gamma_i^d v_i tensor e_{I_i}
      in F_p^r tensor exterior^j E,
    contraction_lambda(T) = 0.

Each leaf i occurs at most once, epsilon_i is +1 or -1, gamma_i is
nonzero, and I_i is a sorted j-subset. A positive leaf occurs in the
distinguished cell {0,...,j-1}. This is a support invariant, not a claim
that the cell's VECTOR is nonzero.

Write E=W direct_sum span(e_{d-1}), possible since zeta_{d-1} != 0.
Every j-vector has a unique form A+B wedge e_{d-1}, with A in exterior^j W
and B in exterior^(j-1) W. Its contraction is
(-1)^(j-1) zeta_{d-1} B. Thus the kernel is exactly exterior^j W,
of dimension binom(d-1,j). No division by j or j! is needed.

More explicitly, a basis of W is
f_a=e_a-(zeta_a/zeta_{d-1})e_{d-1} for a<d-1. Expanding wedges of f_a
shows that projection onto the cells not containing d-1 is an isomorphism
from exterior^j W to that coordinate space. Consequently r*binom(d-1,j)
projected coordinates suffice for linear dependence; the other cells
need not be independently constrained.

### One Recursive Step

Level zero is a single v_i and its positive leaf. To form level j, take
r*binom(d-1,j-1)+1 disjoint level-(j-1) children T_a. Their projected
vectors are dependent. By injectivity, the resulting nonzero relation
sum_a alpha_a T_a=0 holds in the FULL exterior space.

Multiply the entire relation by a nonzero scalar so the first nonzero
alpha_a has power class j-1. Classify each nonzero coefficient as

    alpha_a = zeta_{t_a} rho_a^d.

Form

    T_new = sum_a rho_a^d T_a wedge e_{t_a}.

Since each child has zero contraction, the graded product rule gives

    contraction_lambda(T_new)
      = (-1)^(j-1) sum_a alpha_a T_a = 0.

Appending a repeated basis letter kills that leaf. Otherwise, sort the
letters and multiply epsilon by (-1)^(number of old letters > t_a).
Distinct children have disjoint original leaves, so no surviving leaf
can cancel another copy of itself. In the selected child, the positive
distinguished leaf has old letters {0,...,j-2}; appending j-1 preserves
its positive sign and creates the new distinguished cell. Hence the
support remains nonempty even when its aggregate vector is zero.

The recursive bank count is exactly B_d(r). At level d the contraction
kernel is exterior^d W=0, so T=0. Splitting its surviving leaves by sign
gives the promised collision. The code checks contraction, support
representation, and a positive distinguished leaf at every node, not
only the final sum.

## Turning The Collision Into A Zero Sum

If M=(p-1)/d is even, -1 is a dth power. Compute a checked root eta of -1
and multiply negative-side roots by eta. One collision suffices. This
includes every odd d, including d=1. Taking minus gamma instead is WRONG
for even d; there is an explicit rejecting test over F_13 at degree four.

Otherwise accumulate collisions on disjoint banks. At round a, either
a nonempty zero representation is found or a common NONZERO vector has
2^a nonempty, pairwise disjoint representations with positive dth-power
coefficients. To prove the induction, apply a collision to the child
common vectors; substitute each child's bth representation on each side,
for each b. Disjointness is preserved both across children and across b.
An empty side forces the common vector to zero and is an early valid
exit, not a request for another source bank.

Given a scalar row z != 0 with sum z_b^d=0 and at most 2^a entries,
multiply representation b's roots by z_b. Disjointness and one nonzero
scalar ensure a nonzero witness. Unused representations stay charged.

### Large-Field Scalar Row

For d>=2 and p>16(d-1)^4, sample x uniformly in F_p and test whether
-1-x^d is zero or a dth power. Extract a checked root y, giving (1,x,y).
No enumeration of F_p is performed.

Here is the quantitative justification. The smooth projective Fermat
curve X^d+Y^d+Z^d=0 has genus (d-1)(d-2)/2 (p does not divide d).
Hasse-Weil gives at least p+1-(d-1)(d-2)*sqrt(p) projective points.
There are at most d points at infinity. Under the stated guard, the
number of affine points is at least p/2: the square-root error is below
p/4 and d-1<p/4. Each x has at most d possible y, so a random x succeeds
with probability at least 1/(2d). The bound and standard plane-curve
genus formula are the only geometric imports; see Poonen,
[Rational points on varieties](https://math.mit.edu/~poonen/papers/Qpoints.pdf),
Corollary 7.2.1 for Hasse-Weil.

Two rounds supply four representations, of which only three are used.
The full bank is B_d(r)^2. With T independent uniform trials the scalar
sampling abort probability is at most (1-1/(2d))^T.

### Degree-Bounded Field

When p<=16(d-1)^4, enumerate the p field elements and retain one root per
dth-power value. Dynamic programming finds -1 as a sum of at most d such
values, yielding a normalized row starting with 1. Existence follows from
Chevalley-Warning applied to d+1 variables; normalize any nonzero entry
and permute it to the first position. The DP stores predecessor witnesses
and verifies the recovered row. Its field enumeration is polynomial in d,
NOT an unguarded exponential-in-log(p) escape hatch for arbitrary fields.

Use a=ceil(log2(d+1))=d.bit_length(), with bank B_d(r)^a. This is a
conservative public bound even if the discovered row is shorter. The
current implementation does not shrink it after acquisition. Small-field
planning and specialized quadratic routines could reduce this cost; they
are not needed for correctness and must not be confused with this bound.

## Resources, Not Just Existence

Power-class representatives need no discrete logarithm or factorization
of p-1. Factor the small integer d and sample a nonzero g satisfying
g^((p-1)/q)!=1 for every prime q dividing d. Then g^0,...,g^(d-1) represent
all classes. A uniform trial succeeds with probability phi(d)/d. Each
coefficient's class is identified by exponentiation and comparison with
d precomputed characters. FLINT factors degree-d polynomials to extract
roots; every root is checked. No unverified root is used as a witness.

With a cap T, a union bound for the two sampling loops is

    (1-phi(d)/d)^T + (1-1/(2d))^T,

omitting an unused loop and truncating at one. Seeded RNGs used by tests
are replay fixtures, not independently uniform sources establishing this
probability statement. The code exposes this as a SAMPLING abort bound.
FLINT root extraction, primality testing, RNG calls and linear algebra
are NOT locally wall-clock bounded by these caps. A bounded-time quantum
resource theorem must import a properly timed arithmetic implementation
or add a separate timeout/failure allocation. This pass does neither.

For fixed d, B_d(r) is a degree-d polynomial in r. The algorithm is
polynomial in its explicit acquired-bank size, d and log(p), under the
standard expected-time finite-field root primitive. Audit checks add
polynomial overhead. Coordinate size at a node is bounded by
r*binom(d-1,floor((d-1)/2)). Thus compression does not make growing d cheap:

    B_d(r) <= (r+1)^d * 2^(d*(d-1)),

and the conservative small-field accumulation exponent is still
ceil(log2(d+1)). For p>16(c-1)^4 and degrees at most c, at most two rounds
are needed at each degree. If every grade is erased once with public
width at most R, the illustrative product is at most
(R+1)^(c*(c+1)) * 2^(O(c^3)). This is only a conditional cancellation-bank
bound; it excludes Rees lifting, state preparation, repeated quotient
construction, terminal sampling, and gate synthesis. It is NOT a
polynomial-in-c algorithm, and does not solve DHSP or a native problem.

| Index d | Width r | Exterior collision B | Full tensor recurrence |
|---|---:|---:|---:|
| 2 | 3 | 16 | 28 |
| 3 | 3 | 112 | 1120 |
| 4 | 2 | 441 | 114939 |
| 5 | 2 | 9477 | 528463683 |

The last column is product_j(r*d^j+1), a comparison to the uncompressed
recursion, not a lower bound or a best-known algorithm claim. The existing
quadratic specialized bound is already (r+1)^2 for every odd prime and
can beat the GENERIC even-degree accumulation route. Keep that backend.
The cubic p=2 mod3 case is already linear; no improvement is claimed there.
The main higher-degree dispatcher currently declines genuine index>3;
this bundle supplies a standalone checked option, not a live integration.

## Adversarial Assessment And Falsifiers

- Projection could erase necessary information. The W basis above proves
  injectivity on the actual invariant, not arbitrary exterior tensors.
  Finite rank tests cover every exterior degree for d=2,...,6.
- Alternation could erase all leaves. The distinguished POSITIVE leaf
  proof tracks original indices, not aggregate values. Repeated/zero
  columns are explicit controls; every node checks its signed expansion.
- Even degree could turn equality into a false zero sum. The negative
  root test and full non-early accumulation controls check this boundary.
- Power-index reduction could solve the wrong moment. Bezout lifting is
  derived above and the original exponent is independently matrix-checked.
- The bank could hide exponential field search or adaptive resampling.
  Large-field controls include 128-bit primes; enumeration is permitted
  only by the public degree bound. All supplied labels remain charged.
- Arithmetic success could be mistaken for a receiver. There is no
  coherent implementation, measurement-channel certificate for this new
  backend, native reduction, or stronger classical hardness evidence here.

A single counterexample to the invariant induction, a valid input with
insufficient public bank, or an invalid accepted original witness falsifies
this construction. A better known equivalent method would remove a novelty
claim, not the value of implementing an available arithmetic dependency.
No novelty claim is currently made. Efficiency on a finite all-one bank
is a control of recursion, not a hard-instance benchmark.

## Next Decisive Step

Do not launch larger scalar controls. After review and safe integration,
substitute this backend into a genuinely grade-four/vector-center COMPLETE
instrument test, preserving zero branches, discarded slots, access costs,
and terminal measurement repetitions. If the purpose remains the Rees
native-application route, prioritize constructing/attacking that input
source over optimizing these constants. The unresolved native reduction
is more important than another cancellation-bank improvement.
