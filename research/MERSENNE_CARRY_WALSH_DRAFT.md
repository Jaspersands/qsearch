# Mersenne Carry Walsh Evaluation: Reviewed Local Construction

Date: 2026-10-29.

**STATUS: REVIEWED LOCAL WRITTEN ALGORITHM WITH A BOUNDED REFERENCE
IMPLEMENTATION.** Jason independently reviewed the full construction,
the static DP argument, and the time/space exponents 45/21. This is
AUTOMATED review, not human peer review, formal verification, or a novelty
claim. Dalton supplied the construction and this proof; a separate
implementation and finite controls check the arithmetic and DP identities.

The [bounded reference module](../theorems/mersenne_carry_walsh.py)
and [test file](../tests/test_mersenne_carry_walsh.py) include completed
small full-precision DP
controls and a native n=17,s=3,a=1 run at precision 5, using 6,608,260
charged transitions and returning residue 16 modulo 32. This agrees with
-848 modulo 32; it is NOT full signed Walsh evaluation or a controlled
real-valued approximation. No full-precision native execution is reported.

The implementation chooses the smaller available width. Its canonical
multiplier-4 reorder first activates at n=43; no completed canonical
multiplier-4 DP run is reported. Synthetic reordered and overlapping-boundary
controls are distinct from that missing execution. Section 12 separates
these implementation results from the earlier exponential reference
controls, which remain useful but are not compressed DP execution.

The live report and exact-oracle adapter are replayable with:

    python -m theorems.mersenne_carry_walsh --native-mod32 --output research/classical_baselines/mersenne_carry_walsh.json

`exact_walsh_oracle` raises `CarryWorkCap` on incomplete evaluation. This
is distinct from the clipped sampler's probabilistic ABORT: its success
bound assumes completed exact oracle calls. Setting the transition cap to
None explicitly selects the complete, potentially impractical algorithm.
There is no full-table fallback. The executable API currently bounds field
degrees at 127; the uniform asymptotic claim is the written algorithm, not
an assertion that this reference interface accepts arbitrarily large input.

## 1. Fixed Problem And Scope

Preserve the family from `MERSENNE_RECIPROCAL_RESEARCH_TARGET.md`:

    n is an odd prime, n >= 17;
    q = 2^n, Q = q - 1;
    s = floor((n - 3)/4), d = 2^s - 1;
    r = n - 4s in {3,5};
    F(0) = 0, F(x) = inv0(x)^d = x^(1 - 2^s) for x != 0;
    W(a) = sum_(x in F_q) (-1)^Tr(F(x) + a*x).

The coefficient a is an arbitrary public element of F_q. The output is the
SIGNED INTEGER W(a), not merely its square, magnitude, divisibility, spectrum,
or a moment averaged over a. There is no supplied Walsh oracle, field-sized
table, factorization of Q, discrete logarithm, or primitive-element oracle.

Write

    e = 1 - 2^s, M = n + 2, w = r + 4 in {7,9}.

Here e is a negative Laurent exponent on nonzero elements. It is NOT the root
parameterization exponent denoted e in the earlier target note. M is the
2-adic precision in this draft, not a residual coordinate count from the
access audit. Q is the integer q-1, not a sampling distribution.

The native relation, when relevant to interpretation, still has N=n^2,
K=floor(N/8), arbitrary distinct public evaluation points, the original
Vandermonde parity constraints, and the original target bits. This draft
does not transform those constraints, construct native witnesses, or sample
the native fiber. It addresses the local coefficient evaluation problem.

### Reviewed Written Algorithmic Claim

Given the stated n, a public valid polynomial-basis representation of F_q,
and a in that representation, the specified procedure computes W(a) exactly
by finite arithmetic modulo 2^M. Its conservative bounds are

    time:  O(n^(4w+9)) arithmetic bit operations;
    space: O(n^(2w+3)) bits.

Thus the uniform bounds are O(n^45) time and O(n^21) space. For r=3 they
become O(n^37) time and O(n^17) space. These are deliberately loose
theoretical bounds, not a proposed practical performance estimate.

The proof obligations are supplied below rather than hidden in a specialized
point-counting primitive. The parent reports their independent automated
validation by Jason. The bounded implementation and execution evidence have
the narrower scope stated in Section 12; no practical-runtime claim follows.

## 2. Explicit Field And Ring Representation

### 2.1 Input And Finite Representation

The input field is

    F_q = F_2[T]/(h_bar(T)),

where h_bar is a supplied monic irreducible polynomial of degree n. A field
element is its n binary coefficients in this basis. Let h(T) in Z[T] be the
monic coefficientwise 0/1 lift of h_bar. Define

    O = Z_2[T]/(h(T)),
    R_M = (Z/2^M Z)[T]/(h(T)).

Because h_bar is irreducible over a finite field, it is separable. O is the
ring of integers of the unramified degree-n extension of Q_2, and R_M is its
quotient by 2^M. No claim that the chosen h is a Teichmuller modulus is needed.
An arbitrary monic lift of the irreducible residue polynomial suffices.

An element of R_M is stored as n coefficients modulo 2^M, using O(nM) bits.
Convolution followed by reduction modulo the monic h uses O(n^2) coefficient
operations. With schoolbook M-bit integer multiplication, a ring
multiplication costs O(n^2 M^2) bit operations. Ring addition costs O(nM).
Reduction modulo 2^M is performed throughout; no growing integer numerators
are retained inside the dynamic program.

Input validation is charged. Primality of the integer n can even be checked
by trial division in polynomial time in n. Irreducibility of h_bar can be
checked using repeated squaring and polynomial gcds over F_2, in polynomial
time in n. These validation costs are below the conservative final bound.
If an input uses another explicit basis, a verified polynomial-time basis
conversion must be supplied and charged; this draft does not assume a free
conversion from an unspecified black-box field.

### 2.2 Teichmuller Lifts Without An Exponential Search

For each x in F_q there is a unique lift [x] in O satisfying

    [x] mod 2 = x, [x]^q = [x].

For x != 0, [x] is a Q-th root of unity. Existence and uniqueness follow
from Hensel lifting X^q-X, whose derivative is -1 modulo 2. The nonzero lifts
form a cyclic group of order Q. This group is used in the proof, not listed
by the algorithm.

Only A=[a] modulo 2^M is needed computationally. Set A=0 if a=0. Otherwise
let B in O be the coefficientwise 0/1 lift of a. Choose

    L = n*ceil(M/n).

Compute B^(2^L) in R_M by L repeated squarings. This equals A modulo 2^M.
Indeed, B=[a]*(1+2u) for some u in O. Since L is a multiple of n,
[a]^(2^L)=[a]. Repeated squaring gives

    (1+2u)^(2^L) = 1 mod 2^(L+1),

by the elementary implication v_2(v)>=h>=1 =>
v_2((1+v)^2-1)>=h+1. Since L>=M, the desired precision follows.
For M=n+2 and n>=17, L=2n. This computation is polynomial and requires
neither a primitive field element nor a discrete logarithm.

Precompute

    A_i = A^(2^i) mod 2^M, 0 <= i < n,
    A_i^v mod 2^M, 0 <= v < M.

This costs O(nM) ring operations. Set A_i^0=1 also when a=0. The latter
convention makes zero coefficients harmless in the moment formula.

The exact unramified extension has a Frobenius automorphism sigma with
sigma([x])=[x]^2 and fixed ring Z_2. The algorithm never computes sigma on
arbitrary elements by incorrectly treating ordinary squaring as additive:
it only squares Teichmuller elements to obtain their conjugates.

**FROBENIUS WARNING: ordinary squaring implements sigma ONLY on individual
Teichmuller monomials, not on their sum or on the accumulated trace S.**
To form the trace, advance X^e and A*X separately by ordinary squaring,
and add their successive conjugates. Do NOT advance X^e+A*X or S by
ordinary squaring: in characteristic 2^M, the cross term 2*(X^e)*(A*X)
does not generally vanish, and sigma fixes S in Z_2 whereas S^2 need not
equal S. The repeated squaring of an arbitrary lift B in Section 2.2 is
ordinary exponentiation to construct a Teichmuller element, not a claim
that squaring B is Frobenius. Ordinary powers S^k in the moment argument
likewise mean ring multiplication, not a Frobenius operation.

## 3. An Integral Polynomial For The Sign Character

For an indeterminate Z define

    H_M(Z) = sum_(j=0)^(M-1) (-2)^j * binom(Z,j)
           = sum_(k=0)^(M-1) h_k*Z^k.

### Lemma 1: Coefficient Integrality And Precision

Every h_k is in Z_2, and for every z in Z_2,

    H_M(z) = (-1)^(z mod 2) mod 2^M.

Proof. Write the j-th term as

    ((-2)^j/j!) * product_(ell=0)^(j-1) (Z-ell).

For j>=1, v_2(j!)<=j-1, so (-2)^j/j! is 2-adically integral. The j=0
term is 1. Thus the polynomial coefficients are integral.

For a nonnegative integer t, the finite binomial theorem gives

    (-1)^t = sum_(j=0)^t (-2)^j*binom(t,j).

Every omitted term with j>=M is divisible by 2^M. Hence the claimed
congruence holds for all nonnegative integers. For arbitrary z in Z_2,
choose the nonnegative integer t representing z modulo 2^M. Integrality
of H_M implies H_M(z)=H_M(t) modulo 2^M, and t has the same parity as z.
This proves the statement without an unquantified analytic approximation.

To compute h_k, write j!=2^v*u with u odd. Compute

    (-2)^j/j! = (-1)^j * 2^(j-v) * u^(-1) mod 2^M,

and multiply by the falling-factorial polynomial, using its integral
coefficient recurrence. Only the odd unit u is inverted. One must NOT
try to invert j! in R_M. Exact cancellation of its power of 2 occurs before
the modular inverse, and no additional precision is lost. O(M^2) scalar
coefficient operations suffice, plus polynomial-time odd-unit inversions.

### Lemma 2: The Lifted Trace Has The Required Parity

For a nonzero Teichmuller element X=[x], put

    S(X) = sum_(i=0)^(n-1) (X^(e*2^i) + A_i*X^(2^i)).

This is the unramified trace of X^e+A*X, so S(X) is in Z_2. Reduction
modulo 2 is compatible with the trace, and therefore

    S(X) mod 2 = Tr_Fq/F2(x^e + a*x).

In particular, H_M(S(X)) is the desired sign modulo 2^M. Notice that
X^e+A*X need not be the Teichmuller lift of x^e+a*x. No additivity of
Teichmuller lifting is assumed or required: only reduction of the trace
is used.

## 4. Exact Recovery From Moment Coefficients

Regard S(X) temporarily as a formal Laurent polynomial over O. For k>=0
let C_k be the sum of the coefficients in S(X)^k whose exponents are
multiples of Q. Equivalently it is the coefficient of the residue class
0 in the group ring obtained by imposing X^Q=1. This definition does NOT
instruct the algorithm to build that Q-dimensional group ring.

For the group T_q^* of nonzero Teichmuller elements, character orthogonality
gives, for every integer ell including negative integers,

    sum_(X in T_q^*) X^ell = Q if Q divides ell, and 0 otherwise.

For completeness, if Q does not divide ell, choose a generator zeta of
this cyclic group. Its ell-th power has residue different from 1, so
zeta^ell-1 is a unit in O. Multiplying the sum by zeta^ell permutes its
terms and forces the sum to vanish. Existence of zeta in this proof is
not an algorithmic primitive or a computation of zeta.

It follows that

    sum_(X in T_q^*) S(X)^k = Q*C_k,
    W(a) = 1 + Q*sum_(k=0)^(M-1) h_k*C_k mod 2^M.             (1)

The initial 1 is exactly the x=0 term of W(a), since F(0)=0 and a*0=0.
It is not an arbitrary normalization or a point-at-infinity correction.
C_0=1. Since each S(X) is in Z_2 and Q is odd, each C_k is also in Z_2,
although its computation can be performed in R_M. Correct computed C_k
therefore have zero nonconstant polynomial-basis coordinates modulo 2^M.

An explicit expansion is

    C_k = sum [ k! / product_i(u_i!*v_i!) * product_i A_i^(v_i) ],   (2)

where the sum is over nonnegative integer arrays u,v satisfying

    sum_i(u_i+v_i)=k,
    sum_i(e*u_i+v_i)*2^i = 0 mod Q.

The multinomial coefficient in (2) is an INTEGER. The algorithm below
computes it through binomial increments, not factorial division in R_M.

Finally |W(a)|<=q. Since 2^M=4q, (1) identifies a unique integer in
[-q,q]. Extract the scalar residue modulo 2^M and take its centered
representative in [-2q,2q). It must lie in [-q,q] and is signed W(a).
This is exact reconstruction, with no numerical or probabilistic error.
The optional a=0 fast path may return 0 by balance: gcd(s,n)=1 implies
gcd(d,Q)=1, so F permutes F_q. The general formula also covers a=0.

## 5. Cyclic Carries: Existence, Uniqueness, And Bounds

All indices in this section are residues modulo n. Define integer digits

    b_i = u_i + v_i - u_(i-s).

Since 2^n=1 modulo Q, shifting exponents cyclically gives

    sum_i(e*u_i+v_i)*2^i = sum_i b_i*2^i mod Q.              (3)

The b_i are signed integers, not necessarily binary digits.

### Lemma 3: Elementary Cyclic-Carry Criterion

For any integer array b, the congruence on the right of (3) is zero if
and only if there is an integer array c with

    b_i+c_(i-1)=2*c_i, for all i mod n.                    (4)

When it exists, the array c is unique. If |b_i|<=k for all i, then
|c_i|<=k for all i.

Proof. Define the n cyclically rotated weighted sums

    B_j = sum_(h=0)^(n-1) b_(j+h)*2^h.

Directly rotating the terms gives

    2*B_(j+1) = B_j + Q*b_j.                              (5)

If Q divides B_0, then (5) and the fact that Q is odd show that Q divides
every B_j. Set c_(j-1)=B_j/Q. Equation (5) becomes (4), proving existence
and cyclic closure. Conversely, multiply (4) by 2^i and sum for
0<=i<n. The shifted carry terms telescope to give

    B_0 = Q*c_(n-1),

which proves the congruence. If c,c' are two solutions, their difference
satisfies 2*(c_i-c'_i)=c_(i-1)-c'_(i-1). Iterating n times yields
Q*(c_i-c'_i)=0 in the integers, so the two solutions are equal.
Finally, B_j/Q is a weighted average of the b_(j+h), because
sum_(h=0)^(n-1)2^h=Q. Thus |B_j/Q|<=max_i|b_i|<=k.

For an assignment contributing to C_k, the total of all u_i and v_i is
k. Hence |u_i+v_i-u_(i-s)|<=k. The lemma therefore bounds every carry
by k. Since only k<M is used, the following fixed domains suffice:

    0 <= u_i <= M-1,
    -(M-1) <= c_i <= M-1.

There are

    D = M*(2M-1)

possible paired states (u_i,c_i). Given the paired states at i,i-1,i-s,
the remaining local integer is forced:

    v_i = 2*c_i - c_(i-1) - u_i + u_(i-s).                (6)

Reject v_i outside [0,M-1], or local degree u_i+v_i>=M. Also reject any
transition taking the accumulated total degree to M or above.

Allowing the whole fixed carry domain before the final degree k is known
does not introduce spurious completed assignments. A completed assignment
obeys all n equations (4); uniqueness and the bound then hold for its
actual total degree. Conversely no contributing assignment is discarded.
In particular the all-zero u,v assignment has the unique all-zero carry
array; it is not counted D times or with an arbitrary initial carry.

## 6. Reindexing And The Exact Endpoint Factor

Since n is odd, multiplication by 4 permutes Z/nZ. Let gamma be its inverse
modulo n, computed by the extended Euclidean algorithm. Put j=4i mod n and
rename the paired state at original index i as

    z_j=(U_j,C_j)=(u_(gamma*j),c_(gamma*j)).

Because 4s=n-r,

    4*(i-1) = j-4 mod n,
    4*(i-s) = j+r mod n.

The factor from (6) thus uses z_j,z_(j-4),z_(j+r). Index the factor by
its cyclic right endpoint

    b = j+r mod n.

Its three variable labels are EXACTLY

    z_b, z_(b-r), z_(b-w), with w=4+r,                    (7)

with every label reduced modulo n. For this endpoint define

    i(b) = gamma*(b-r) mod n,
    V_b = 2*C_(b-r) - C_(b-w) - U_(b-r) + U_b,
    t_b = U_(b-r) + V_b,
    g_b = binom(t_b,U_(b-r)) * A_(i(b))^(V_b).            (8)

The factor is invalid unless 0<=V_b<M and 0<=t_b<M. Its degree is t_b
and its weight is g_b in R_M. The coefficient index is i(b), NOT b or
b-r in the original ordering. Every original site i is represented by
one endpoint b, and its u_i,v_i are counted once through t_b.

For w<=b<n, all three labels in (7) are ordinary nonnegative integers
in [b-w,b]. These are the sweep factors. For 0<=b<w the factor wraps
and is deferred until closure. This separation uses endpoint b, not
center j, avoiding an off-by-r closure rule.

## 7. Dynamic Program And Rigorous Closure

For all allowed n, w<n. Define sets of LABELS

    B = {0,...,w-1},
    E = {n-w,...,n-1}.

These are sets, not two independent copies of a list of variables.

### 7.1 Boundary Enumeration And Sweep

Enumerate each assignment eta of paired states to the labels in B exactly
once. This outer loop has at most D^w iterations and is processed
sequentially. Keep eta available as read-only boundary data during its pass.

For a fixed eta initialize the frontier to B with its assigned values.
Its degree array has entry 1 at degree 0 and zero elsewhere. No factors
have yet been evaluated, so the initial degree is 0 even if eta contains
nonzero U values. Degrees belong to factors, not to introduction events.

For b=w,w+1,...,n-1:

1. The old frontier is the label interval {b-w,...,b-1} of size w.
2. Introduce one state z_b, ranging over its D possibilities. This label
   has never been assigned before, since b>=w and all earlier introduced
   labels are smaller than b.
3. Evaluate endpoint factor b using z_b,z_(b-r),z_(b-w). Both old labels
   are in the frontier because 0<r<w.
4. If valid, update every degree k with k+t_b<M by

       new[k+t_b] += old[k] * binom(k+t_b,t_b) * g_b.      (9)

5. Forget label b-w from the active frontier, producing the new interval
   {b-w+1,...,b}. Merge paths with identical remaining labeled states and
   degree by addition in R_M.

For this pass, previously forgotten boundary labels are still accessible
through eta. Previously forgotten nonboundary labels are no longer needed:
all factors with endpoint at least w that involve such a label have already
been evaluated when it is forgotten, and Section 7.2 shows that no closure
factor requires a forgotten nonboundary label.

At the end the frontier is E. The invariant before closure is: every sweep
factor with endpoint in {w,...,n-1} has been evaluated exactly once; no
wrapping factor has been evaluated; each path gives a unique assignment
to all introduced labels extending eta; and its degree array is the sum
of precisely those paths with each given accumulated degree and frontier.

### 7.2 Support Of Every Wrapping Factor

Let 0<=b<w. In (7):

- b belongs to B;
- b-w mod n is n+b-w and belongs to E;
- if b-r>=0, then 0<=b-r<=w-1-r=3, so b-r belongs to B;
- if b-r<0, then b-r mod n is n+b-r, in {n-r,...,n-1}, a subset of E.

Thus every wrapping factor is supported on the union B union E. No
assumption that these sets are disjoint was made.

For each final frontier state of a pass, obtain one consistent assignment
on B union E. To look up a label ell, use eta[ell] when ell is in B and
the final frontier value otherwise. If ell is in both, the two stored
values MUST agree and refer to the same variable; one may assert this
agreement as an implementation check. There is no second sum over a new
value for that label.

Evaluate the wrapping factors in the fixed order b=0,...,w-1, using (8)
and the same degree update (9). Discard invalid assignments or degrees
>=M. Sum the resulting arrays over final frontiers and over eta. The
resulting entry of degree k is C_k.

### 7.3 The n=17 Overlap Is Not An Exception To The Proof

At n=17, s=3, r=5, w=9:

    B={0,...,8}, E={8,...,16}, B intersect E={8}.

Only labels 9,...,16 are introduced during the sweep. Label 8 was assigned
once in eta and remains in the frontier through the entire sweep. Its
final frontier value is therefore eta[8] automatically. Closure does NOT
enumerate a new z_8 and does NOT multiply by D for that overlap.

As explicit endpoint checks, the b=0 factor uses labels {0,12,8}; the
b=8 factor uses labels {8,3,16}. Both use the same previously assigned
label 8. This is the only canonical n<2w case, but the union-and-label
argument works whenever w<n even if B and E overlap more generally.

### 7.4 Why The Multinomial Increment Is Required

Suppose an already processed set of sites has total degree k and carries
the weight

    k! / product_processed(u_i!*v_i!) * product_processed A_i^(v_i).

For the next site, t=u+v and its local factor has weight

    binom(t,u)*A_i^v = t!/(u!*v!) * A_i^v.

Multiplication by binom(k+t,t) in (9) yields exactly

    (k+t)! / (product_processed(u_i!*v_i!)*u!*v!)
      * product_processed A_i^(v_i) * A_i^v.

Starting from degree 0 and processing all sites proves that the final
weight is the multinomial in (2), regardless of the sweep/closure order.
Omitting binom(k+t,t) would compute the wrong moments. The statement uses
ordinary integer binomial coefficients reduced modulo 2^M, not a formal
division by factorials in a ring with zero divisors.

### 7.5 Bijection With The Moment Sum

For each assignment u,v in (2), Lemma 3 supplies a unique carry array in
the allowed domains. Reindexing is bijective. Its values on B determine
one eta, every remaining label is introduced once, and every factor is
evaluated once. It survives all degree cutoffs because local degrees are
nonnegative and the final total is k<M. Equation (9) gives its correct
weight.

Conversely, a completed DP path gives one labeled paired-state assignment,
and (8) supplies a nonnegative v_i for each original i. All n carry
equations hold, including closure, and its degree equals sum_i(u_i+v_i).
Lemma 3 implies the exponent congruence. Thus it supplies exactly one
term of (2). This proves both correctness and absence of overcounting.

## 8. Algorithm Outline

The following is specification pseudocode, not an execution record. The
parent's [bounded implementation](../theorems/mersenne_carry_walsh.py)
implements the carry method with optional work caps and a smaller-width
layout selection; its actual execution scope is recorded in Section 12.3.

```text
validate n, s, r, h_bar, and the polynomial-basis coefficient a
M <- n+2; w <- r+4; D <- M*(2*M-1)
construct R_M using the monic 0/1 lift h
compute A, all A_i, and powers A_i^v for 0 <= v < M
compute integral coefficients h_k of H_M modulo 2^M
precompute integer binomial coefficients needed for degrees below M
C[0:M] <- 0
for each assignment eta to the distinct labels B={0,...,w-1}:
    frontier <- eta, degree-array [1,0,...,0]
    for b=w,...,n-1:
        introduce label b, evaluate endpoint b, apply (9), forget b-w
        combine equal remaining labeled states and degree
    for each final frontier on E={n-w,...,n-1}:
        form the consistent union of eta and this frontier by LABEL
        evaluate endpoints b=0,...,w-1, successively applying (9)
        add the remaining degree array to C
R <- 1 + Q * sum_(k=0)^(M-1) h_k*C[k] in R_M
check nonconstant coordinates of R are zero
W <- centered integer representative of the constant coordinate mod 2^M
check -q <= W <= q
return W
```

The coordinate and magnitude checks are necessary consistency checks, not
proof of an arbitrary implementation's correctness. For example an
incorrect scalar could pass both checks.

## 9. Complete Resource Accounting

### 9.1 Operation Model And Ring Work

The bounds here are conventional arithmetic bit-complexity bounds with
random-access tables and explicitly charged integer and ring arithmetic.
Ring elements use nM bits. Addresses and state/degree labels have O(log n)
bits because w is one of two fixed constants and M=Theta(n); their
arithmetic is dominated by the stated schoolbook ring multiplication
bound. These are not wall-clock estimates or tight multitape-machine
simulation bounds.

For each fixed eta, at most D^w frontier assignments are stored, each
with M coefficients. A sweep transition considers at most D possible new
states, and there are at most n stages. A local factor is a single degree
shift, so O(M) ring operations per transition would suffice with tables;
we conservatively charge O(M^2), including bookkeeping and closure.
The w closure factors per final frontier are covered by this bound,
since w<=9 is constant. Sequential enumeration of D^w boundary assignments
therefore gives

    O(n*M^2*D^(2w+1)) ring operations.                    (10)

This explicitly charges the boundary enumeration. Treating the cyclic
chain as an open chain and omitting that factor would understate the cost.

Polynomial preprocessing includes input validation, construction of h,
O(n) repeated squarings for A and its conjugates, O(nM) ring operations
for powers, O(M^2) binomial and falling-factorial coefficient work, and
the index permutation. It is dominated by (10). No exponent-dependent
dense polynomial of degree 2^s or table of size q is constructed.

### 9.2 Time Exponents

Multiplying (10) by the schoolbook ring-operation bound gives

    O(n*M^2*D^(2w+1) * n^2*M^2)
      = O(n^3*M^4*D^(2w+1)).

Since D=M*(2M-1)<=2*M^2 and w is fixed,

    O(n^3*M^4*D^(2w+1))
      = O(n^3*M^(4w+6))
      = O(n^(4w+9)), since M=n+2=Theta(n).

For w=9 this is exponent 45; for w=7 it is exponent 37. The constant
factor from 2^(2w+1) is independent of n and a. This bound is intentionally
conservative and not a claim that the construction is computationally
useful at existing parameter sizes.

### 9.3 Space Exponents

Only one boundary assignment's pass is kept at a time. Two frontier layers
need O(D^w*M) ring elements. Each element uses O(nM) bits, so

    O(D^w*M*nM) = O(n*M^2*D^w)
               = O(n*M^(2w+2))
               = O(n^(2w+3)) bits.

This is exponent 21 for w=9 and exponent 17 for w=7. Boundary data, output
arrays, ring moduli, index maps, binomial tables, and the nM table of
coefficient powers are smaller. There is no D^w multiplier in memory
for simultaneously retaining every boundary pass.

### 9.4 Precision And Failure Premises

All evaluator arithmetic is exact in R_M; the sign congruence needs only
M=n+2 bits. Teichmuller lifting and integral polynomial coefficients do
not require an uncharged precision increase. The bound |W|<=q suffices
for reconstruction; no Weil/genus bound is used for that step.

Subject to the proof and correct implementation, evaluation is
deterministic with zero error or failure probability for valid input.
Malformed field representations or invalid family parameters must be
rejected. Arithmetic software bugs are not an allowed probabilistic
failure premise. A bounded implementation may return WORK_CAP without
any coefficient; such an outcome is not successful evaluation. The
reported automated review and bounded controls must not be relabeled
as human certification, a completed full-precision native run, or a
practical runtime demonstration.

## 10. Consequence For The Existing Clipped Sampler

This section imports, rather than reproves, the fourth-moment and clipping
argument in `MERSENNE_CLASSICAL_ACCESS_AUDIT.md`, Section 2. In that notation
P(a)=W(a)^2/q^2 and delta<=14 or 30 according as r=3 or 5.

For rational 0<epsilon<=1/2, put T=ceil(delta/epsilon). Exact W(a) makes
the acceptance numerator min(W(a)^2,T*q) available using integers of
O(n+log T) bits. A uniform field proposal uses n random bits in the
public polynomial basis. The expected number of evaluator calls is
at most T/(1-epsilon). Thus the expected total evaluator work is

    O(n^45/epsilon),

with additional polynomial work in n, log T, and the representation size
of epsilon for exact integer probability sampling. With the audit's
proposal cap J=ceil(T*kappa/(1-epsilon)), there are at most J evaluator
calls, costing O(n^45*kappa/epsilon). The audit's distributional error
including proposal-cap ABORT is at most epsilon+2^(-kappa).

An exact uniform integer draw below T*q can use rejection from
ceil(log2(T*q)) independent bits. It has expected fewer than two attempts,
but unbounded worst-case random-bit consumption. Therefore the proposal
cap alone is NOT a strict worst-case bit-time bound for that implementation
of exact rational Bernoulli trials. If a strict clock is required, cap
each such integer draw at H attempts and retain an extra ABORT. Its
additional probability is at most J*2^(-H), so one may choose H to fit a
separately stated error allowance. No evaluator randomness is involved.

The resulting sampler is for the approximate measured local Fourier law,
not the exact law and not the native parity-conditioned fiber. Product
sources still require combined error budgets. Signed W values are
available, but that does not constitute a classical coherent simulation.

## 11. Relation To The Investigated Literature

The following primary sources were browsed during the originating
read-only research turn. Their ingredients should not be confused with
a previously published theorem asserting this complete construction.

- Blondeau, Canteaut, Charpin, *Differential properties of functions
  x -> x^(2^t-1)*, Theorem 1: linearized-polynomial differential counts.
  This is relevant local structure, not by itself arbitrary signed Walsh
  evaluation. <https://arxiv.org/html/1108.4753v2>
- Canteaut, Charpin, Dobbertin, *Binary m-sequences with three-valued
  crosscorrelation: a proof of Welch's conjecture*: results for the Welch
  decimation and weight methods, not a direct evaluator for the fixed
  exponent here.
  <https://www.rocq.inria.fr/secret/Anne.Canteaut/Publications/Canteaut_Charpin_Dobbertin00a.pdf>
- Nguyen, *On Weil Sums, Conjectures of Helleseth, and Niho Exponents*:
  the quadratic-extension Niho framework has hypotheses not supplied by
  this odd-prime-degree family. This does not assert that every result
  called Niho requires even absolute degree.
  <https://arxiv.org/pdf/2006.15726>
- Helleseth, Hollmann, Kholosha, Wang, Xiang, *Proofs of two conjectures
  on ternary weakly regular bent functions*, Lemma 4.2: the general
  integer cyclic-carry criterion. Section 5 above includes its elementary
  p=2 proof so that the transfer and uniqueness obligations are explicit.
  <https://arxiv.org/pdf/0803.2878>
- Hubrechts, *Point counting in families of hyperelliptic curves in
  characteristic 2*, Section 5.1: unramified/Teichmuller arithmetic and
  its complexity. Section 2 above supplies a simple schoolbook alternative
  adequate for this draft's deliberately loose bound.
  <https://arxiv.org/pdf/math/0607346>
- Lauder and Wan, *Counting points on varieties over finite fields of
  small characteristic*: point counting with degree/Newton-polytope
  dependence. Sparse input alone does not remove those parameters.
  <https://library.slmath.org/books/Book44/files/18lauder.pdf>
- Harvey, *Computing zeta functions of arithmetic schemes*: elementary
  finite-precision point-counting methods, with explicit dependence on
  the defining variety in its bounds. This is not a black-box guarantee
  polynomial in the logarithm of our growing ordinary degree.
  <https://arxiv.org/pdf/1402.3439>

The proposed use of full-precision moments, integral sign interpolation,
and bounded-width contraction is a derivation in this conversation. No
novelty claim is made. The relation 4s+r=n that also underlies the quartic
partial-norm identity instead makes the carry jumps constant after the
permutation j=4i. No assertion about hardness follows from the genus, and
no quotient of the curve or compressed cohomology oracle is assumed.

## 12. Reference Controls And Provenance

### 12.1 What Was Executed In The Originating Turn

The following in-memory controls were executed using `python -B -` from
the repository working directory. No control script or output file was
written. The outputs are part of the originating conversation's tool
record, not a separately signed or independent certificate.

1. The sign polynomial was checked for M=2,...,20 at every integer
   -100,...,100. All checks passed.
2. The cyclic-carry existence and bounds were checked exhaustively for
   b_i in {-1,0,1}, n=3,...,7. These are abstract lemma controls, NOT
   replacement research-family instances.
3. The index permutation and circular factor support were checked at
   canonical n in {17,19,23,29,31,61,101}. These check exact indexing,
   not runtime scaling or asymptotic correctness by extrapolation.
4. At n=17,s=3,a=1,M=19, an EXPONENTIAL group-ring convolution computed
   all required C_k and reconstructed W(1)=-848.
5. At n=17,s=3,a=12345,M=6, an EXPONENTIAL enumeration of monomial
   multisets checked the coefficient formula in
   (Z/64 Z)[T]/(T^17+T^3+1). It encountered 120 exponent-balanced terms
   across degrees 0 through 5, checked their cyclic carries, and returned
   residue 48. A separate full-field sum gave signed W(a)=-80, agreeing
   modulo 64.

The a=1 group-ring computation does not depend on a chosen field basis,
because its coefficients are all 1. The nontrivial-coefficient control
uses modulus T^17+T^3+1 and encodes a=12345 by its binary polynomial
coefficients. Its exponential reference builds power/log tables solely
for the reference sum; the proposed algorithm does not use those tables.

None of these checks executed the compressed weighted frontier DP.
That statement concerns the ORIGINAL checks listed above, not the
parent implementation results added in Section 12.3.
Appendix A gives exact self-contained replay commands. These commands
are not presented as a verbatim transcript of every original formatting
detail: they remove an inactive initialization expression and add explicit
label-introduction checks. Their algorithms, parameters, and expected
numeric results are stated here so that provenance is not obscured.

### 12.2 Save-Turn Environment And Source Snapshots

The environment was queried during the documentation turn with

```sh
python -B -c 'import sys, numpy; print(sys.version); print(sys.executable); print("numpy", numpy.__version__)'
shasum -a 256 research/MERSENNE_CLASSICAL_ACCESS_AUDIT.md research/MERSENNE_RECIPROCAL_RESEARCH_TARGET.md research/classical_baselines/mersenne_reciprocal_access.json
```

Observed interpreter: `/opt/anaconda3/bin/python`, Python 3.13.5,
packaged by Anaconda, Clang 14.0.6; NumPy 2.3.3. This is the save-turn
environment observation, not a retroactively captured environment log
from the first control execution.

Observed SHA-256 values:

```text
8d0fa317fa4489ea40ae87d81f8951b296ff7ab7061ce20e31524c7fcd0247d7  research/MERSENNE_CLASSICAL_ACCESS_AUDIT.md
806f05dd1b0a4f89a95c3050468a7b08888abbb55fd39f7566be629301b260ab  research/MERSENNE_RECIPROCAL_RESEARCH_TARGET.md
9dbd1ade2bcfc8b718d6bb2597acd31dc0669b6ff7618021a315a66ecde64eef  research/classical_baselines/mersenne_reciprocal_access.json
```

These are HISTORICAL snapshots of the context read by the documentation
agent, not the current sources after integration. Current hashes are in
`research/classical_baselines/mersenne_carry_walsh.json`. They are not hashes
of an implemented compressed evaluator. No claim is made about unrelated
dirty files elsewhere in the shared repository.

All three Appendix A commands were subsequently rerun from this saved draft
during the documentation turn and passed. The recorded results remained
W(1)=-848 at M=19 and residue 48, direct W=-80, and 120 balanced terms in
the nontrivial-coefficient control. This was still reference replay, not
execution of the compressed weighted DP.

### 12.3 Parent Implementation And Reported Execution Scope

The coordinating agent supplied the implementation report while this draft was being finalized:
Jason independently validated the complete written construction, static
DP, and bounds 45/21; the parent module passed 50 tests; the native
precision-5 run completed. The module and tests were then inspected
read-only in this session. Review validation and the native transition
count are attributed to that report, not to a fabricated local tool run.

The historical inspected source snapshots, before CLI/oracle integration, were:

```text
f7397168cf47564ddf69e2288e0f04111278f80d409c778051f7a04c6ee891fb  theorems/mersenne_carry_walsh.py
127e230b68e6d9da1b0279e83e30c589569a8aa933f21121bad8c25c8c3999df  tests/test_mersenne_carry_walsh.py
```

The bounded reference module uses python-flint and the repository's
public `field(bits)` modulus, reports that modulus in its result, and
currently limits its API to field degrees 3 through 127 and precision
1 through 10000. It does not expose the arbitrary supplied modulus input
of the general written algorithm. These are reference-interface limits,
not changes to the fixed research family or the mathematical input-size
claim. Its Teichmuller lifting uses a more conservative polynomial number
of squarings than the simple bound in Section 2.2. Its work cap counts
boundary visits and attempted transitions, not every bit operation or
wall-clock time. WORK_CAP returns neither a partial residue nor a signed
coefficient and does not fall back to a field-sized table.

The 50-test file covers all n=3,s=1 frequencies at full precision;
n=5,s=1 frequencies 0,1,2,7 at full precision; Teichmuller, lifted-trace,
sign-polynomial, and carry controls; guards and work caps; a synthetic
reordered control; and a synthetic n=3,width=2 overlapping-boundary
control. These small fields are implementation controls, not substituted
canonical research parameters. Static factor-index checks also cover
canonical inputs. In the lifted-trace test, the two Teichmuller monomials
are squared separately, consistently with the warning in Section 2.

The parent-reported native execution is precisely

    n=17, s=3, a=1, precision=5;
    EXACT_CONGRUENCE, modulus=32, walsh_residue=16;
    charged transitions=6,608,260;
    no signed walsh_value, no full-precision result.

The module's layout at this input is multiplier 1 and width 3. This is
actual canonical-family carry DP execution, but it is NOT the width-9
multiplier-4 layout used in the written uniform proof, and does not execute
that proof's n=17 overlapping boundary. The synthetic overlap test supplies
separate implementation evidence for shared-label handling.

The layout selects multiplier 4 only when the input is canonical and
r+4<s; ties retain the original ordering. For canonical primes below 43,
s<=r+4. At n=43,s=10,r=3, width 7 is strictly smaller than 10, so this is
the first canonical multiplier-4 selection. No completed canonical
multiplier-4 DP execution has been reported. A capped multiplier-4 run or
a static index check is not such an execution.

This is a reproducible command for the parent test file, with bytecode and
pytest-cache writes disabled:

```sh
python -B -m pytest tests/test_mersenne_carry_walsh.py -q -p no:cacheprovider -W error
```

This exact command was run in this documentation session and exited 0:

```text
..................................................                       [100%]
50 passed in 3.61s
```

This is fresh local verification of that bounded test file, not an
independent mathematical review, a whole-repository test result, or a
rerun of the 6,608,260-transition native control.

The native run can be requested from the inspected API using the following
command. This is a replay command derived from the API, not a claim about
the parent's verbatim original command; it was NOT run by this draft-only
session. Its cap is a transition cap, not a runtime guarantee.

```sh
python -B - <<'PY'
from theorems.mersenne_carry_walsh import carry_walsh
result = carry_walsh(17, 3, 1, precision=5, max_transitions=10_000_000)
print(result)
assert result['status'] == 'EXACT_CONGRUENCE'
assert result['walsh_residue'] == 16
assert result['transitions'] == 6_608_260
assert result['walsh_value'] is None
assert result['layout']['multiplier'] == 1
PY
```

Low 2-adic precision is only a congruence. It does not provide the signed
value or an error bound in ordinary absolute value, and by itself does
not instantiate the Fourier sampler's coefficient access. The reviewed
written algorithm supplies the full-precision theoretical route; completed
native full-precision execution remains absent from this evidence.

## 13. Review Disposition And Remaining Checks

The parent reports that independent automated reviewer Jason validated
the full construction, bounds, and static DP. This session has not read
Jason's raw review transcript. The following checklist records the proof
obligations for that review and for any subsequent review, rather than
marking the construction as wholly unreviewed:

1. The arbitrary monic lift defines the required unramified ring; the
   repeated-squaring Teichmuller construction uses only polynomial work.
2. S(X) lies in Z_2, although the summand is not an additive Teichmuller
   lift, and H_M has integral monomial coefficients at the stated precision.
3. The x=0 contribution, root-of-unity orthogonality, signed reconstruction,
   and all a including 0 are correct.
4. The signed-digit cyclic carry criterion is necessary and sufficient,
   has a UNIQUE integer solution, and bounds all relevant carries by k.
5. The endpoint factor uses labels b,b-r,b-w and coefficient A_(i(b)),
   with no accidental use of the reordered label as an original index.
6. Every wrap factor is deferred and evaluated once; shared labels in
   B intersect E are reused rather than independently enumerated.
7. The degree/multinomial increment is binom(k+t,t), and all factorial
   cancellation is legitimate without division by a nonunit.
8. Every valid term in C_k has exactly one completed DP path, including
   the degree-zero term and the n=17 overlap.
9. The D^w boundary-enumeration cost is charged in time but not repeated
   in peak memory; the exponents 4w+9 and 2w+3 follow as written.
10. The reference controls are not compressed execution, and the local
    sampler consequence is not promoted to native parity completion.

Completed scope, with provenance as above: reported independent automated
review of the local written algorithm; a parent bounded reference
implementation; small full-precision coefficient tests; synthetic reorder
and overlap controls; and a parent-reported low-precision native run.
Remaining scope: completed full-precision native evaluation, completed
canonical multiplier-4 DP execution, and any human or formal verification.
No novelty, practical runtime, coherent classical simulation, or native
parity-completion claim is made.

## Appendix A. Read-Only Replay Commands

Run from `/Users/jaspersands/Desktop/quantum algorithm search`. Each command
uses only standard-library modules except the explicitly exponential
NumPy group-ring control. `-B` prevents Python bytecode-cache writes.
There is no dependency installation and no output redirection to files.
The fenced commands are executable controls; the pseudocode in Section 8
is not one of them.

### A1. Sign, Carry, Index, And Shared-Label Controls

```sh
python -B - <<'PY'
from math import factorial
from itertools import product

for M in range(2, 21):
    mod = 1 << M
    p = [0] * M
    falling = [1]
    for j in range(M):
        f = factorial(j)
        v = (f & -f).bit_length() - 1
        scale = ((-1) ** j) * (1 << (j-v)) * pow(f >> v, -1, mod) % mod
        for k, c in enumerate(falling):
            p[k] = (p[k] + scale*c) % mod
        nxt = [0] * (len(falling)+1)
        for k, c in enumerate(falling):
            nxt[k] -= j*c
            nxt[k+1] += c
        falling = nxt
    for z in range(-100, 101):
        assert sum(c*pow(z, k, mod) for k, c in enumerate(p)) % mod == (
            1 if z % 2 == 0 else -1
        ) % mod
print('Parity polynomial: all M=2..20 and integers -100..100 passed.')

for n in range(3, 8):
    Q = (1 << n)-1
    for b in product(range(-1, 2), repeat=n):
        B0 = sum(x*(1 << i) for i, x in enumerate(b))
        if B0 % Q:
            continue
        carry = B0 // Q
        initial = carry
        for x in b:
            assert (x+carry) % 2 == 0
            carry = (x+carry) // 2
            assert abs(carry) <= 1
        assert carry == initial
print('Cyclic carry existence/bounds: exhaustive ternary digit controls passed.')

for n in [17, 19, 23, 29, 31, 61, 101]:
    s = (n-3) // 4
    r = n-4*s
    w = r+4
    gamma = pow(4, -1, n)
    B = set(range(w))
    E = set(range(n-w, n))
    introduced = set(B)
    frontier = set(B)
    evaluated = set()
    for i in range(n):
        j = 4*i % n
        b = (j+r) % n
        assert 4*((i-1) % n) % n == (j-4) % n
        assert 4*((i-s) % n) % n == (j+r) % n
        assert {j, (j-4) % n, (j+r) % n} == {
            b, (b-r) % n, (b-w) % n
        }
        assert gamma*((b-r) % n) % n == i
    for b in range(w, n):
        assert frontier == set(range(b-w, b))
        assert b not in introduced
        introduced.add(b)
        assert {b, b-r, b-w} <= frontier | {b}
        evaluated.add(b)
        frontier = (frontier | {b}) - {b-w}
    assert introduced == set(range(n))
    assert frontier == E
    for b in range(w):
        assert {b, (b-r) % n, (b-w) % n} <= B | E
        assert b not in evaluated
        evaluated.add(b)
    assert evaluated == set(range(n))
    if n == 17:
        assert B & E == {8}
    print({'n': n, 's': s, 'r': r, 'w': w,
           'shared_boundary_labels': sorted(B & E)})
print('Endpoint and single-introduction label controls passed; no weighted DP executed.')
PY
```

### A2. Full-Precision Exponential Group-Ring Control

Expected result: signed W(1)=-848 for n=17,s=3,M=19. This stores Q=131071
group-ring coefficients and is explicitly exponential in n.

```sh
python -B - <<'PY'
from math import factorial
import numpy as np

n = 17
s = (n-3) // 4
q = 1 << n
Q = q-1
M = n+2
mod = 1 << M
p = [0] * M
falling = [1]
for j in range(M):
    f = factorial(j)
    v = (f & -f).bit_length()-1
    scale = ((-1) ** j) * (1 << (j-v)) * pow(f >> v, -1, mod) % mod
    for k, c in enumerate(falling):
        p[k] = (p[k] + scale*c) % mod
    nxt = [0] * (len(falling)+1)
    for k, c in enumerate(falling):
        nxt[k] -= j*c
        nxt[k+1] += c
    falling = nxt
shifts = [((1-(1 << s))*(1 << i)) % Q for i in range(n)]
shifts += [(1 << i) % Q for i in range(n)]
v = np.zeros(Q, dtype=np.int64)
v[0] = 1
C = []
for k in range(M):
    C.append(int(v[0]))
    if k+1 < M:
        new = np.zeros_like(v)
        for shift in shifts:
            new += np.roll(v, shift)
        v = new % mod
residue = (1 + Q*sum(c*t for c, t in zip(p, C))) % mod
W = residue if residue < mod//2 else residue-mod
assert W == -848
print({'check': 'canonical n17,s3,a1 full-precision parity/moment formula',
       'precision_bits': M, 'W': W,
       'method': 'exponential group-ring correctness control, NOT compressed runtime validation'})
PY
```

The signed 64-bit arrays cannot overflow in this control: each update
sums 34 residues below 2^19 before reducing, far below 2^63. This argument
is for the stated control, not a general floating-point implementation.

### A3. Nontrivial Coefficient And Direct Field-Sum Control

Expected result: residue 48 modulo 64, direct signed W(12345)=-80,
120 balanced monomial terms. The moment side enumerates multisets; the
reference side builds full-field power/log tables. Neither is the DP.

```sh
python -B - <<'PY'
from math import factorial
from itertools import combinations_with_replacement
from collections import Counter

n = 17
s = 3
q = 1 << n
Q = q-1
M = 6
mod = 1 << M
a = 12345
zero = (0,) * n
one = (1,) + (0,) * (n-1)

def add(x, y):
    return tuple((u+v) % mod for u, v in zip(x, y))

def scale(x, c):
    return tuple(v*c % mod for v in x)

def mul(x, y):
    z = [0] * (2*n-1)
    for i, u in enumerate(x):
        if u:
            for j, v in enumerate(y):
                z[i+j] += u*v
    for k in range(2*n-2, n-1, -1):
        z[k-n] -= z[k]
        z[k-n+3] -= z[k]
    return tuple(v % mod for v in z[:n])

A = tuple((a >> i) & 1 for i in range(n))
for _ in range(n):
    A = mul(A, A)
Ais = []
t = A
for _ in range(n):
    Ais.append(t)
    t = mul(t, t)
assert t == A
powers = []
for Ai in Ais:
    values = [one]
    for _ in range(M-1):
        values.append(mul(values[-1], Ai))
    powers.append(values)
shifts = [((1-(1 << s))*(1 << i)) % Q for i in range(n)]
shifts += [(1 << i) % Q for i in range(n)]
C = []
hits = 0
for k in range(M):
    ans = zero
    for inds in combinations_with_replacement(range(2*n), k):
        if sum(shifts[i] for i in inds) % Q:
            continue
        counts = Counter(inds)
        weight = factorial(k)
        term = one
        u = [0] * n
        v = [0] * n
        for i, count in counts.items():
            weight //= factorial(count)
            if i >= n:
                v[i-n] = count
                term = mul(term, powers[i-n][count])
            else:
                u[i] = count
        digits = [u[i]+v[i]-u[(i-s) % n] for i in range(n)]
        carry = sum(digits[i]*(1 << i) for i in range(n)) // Q
        initial = carry
        for digit in digits:
            assert (digit+carry) % 2 == 0
            carry = (digit+carry) // 2
            assert abs(carry) <= k
        assert carry == initial
        ans = add(ans, scale(term, weight))
        hits += 1
    assert not any(ans[1:])
    C.append(ans[0])
p = [0] * M
falling = [1]
for j in range(M):
    f = factorial(j)
    v2 = (f & -f).bit_length()-1
    coefficient = ((-1) ** j) * (1 << (j-v2)) * pow(f >> v2, -1, mod) % mod
    for k, t in enumerate(falling):
        p[k] = (p[k]+coefficient*t) % mod
    nxt = [0] * (len(falling)+1)
    for k, t in enumerate(falling):
        nxt[k] -= j*t
        nxt[k+1] += t
    falling = nxt
answer = (1 + Q*sum(x*y for x, y in zip(p, C))) % mod

exp = [0] * Q
logs = [0] * q
t = 1
seen = set()
for i in range(Q):
    assert t not in seen
    seen.add(t)
    exp[i] = t
    logs[t] = i
    t <<= 1
    if t & q:
        t ^= q | 9
assert t == 1 and len(seen) == Q

def square(x):
    return 0 if x == 0 else exp[(2*logs[x]) % Q]

mask = 0
for j in range(n):
    t = 1 << j
    tr = 0
    for _ in range(n):
        tr ^= t
        t = square(t)
    assert tr in (0, 1)
    mask |= tr << j
loga = logs[a]
W = 1
for i in range(Q):
    bit = ((exp[(-7*i) % Q] ^ exp[(loga+i) % Q]) & mask).bit_count() % 2
    W += 1-2*bit
assert W == -80 and answer == 48 and hits == 120
assert W % mod == answer
print({'check': 'nontrivial coefficient in canonical field',
       'n': n, 's': s, 'a': a, 'precision_bits': M,
       'moment_residue': answer, 'direct_W': W,
       'balanced_terms_checked': hits,
       'note': 'correctness control only; moment enumeration is not the compressed DP'})
PY
```

The extra `seen` assertion checks that the particular full-field table
really traverses all nonzero elements. It is reference-only exponential
storage, not part of the algorithmic resource bound in Section 9.
