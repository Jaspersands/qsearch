# Full-Jet Adaptive Resource Theorem And Source-Support Refinement

2026-10-22. A conditional resource/error argument for the existing proposal,
not a complete quantum implementation, a new HSP scope, or a novelty claim.
The new support refinement is proved below in ordinary mathematics and
checked against symbolic implementations. It is NOT a new Lean theorem.

## Question And Outcome

Does the class-three-normal construction hide an exponential-in-log(p)
selection, precision or diagonal-solving cost? No such cost was found under
its stated promises. The audit did find (1) rounded clocks that can be one
too small, (2) an incomplete executable error ledger, and (3) a much larger
SDE equation envelope than the actual source requires. The third is a
structural improvement: the source has three invariant polynomial blocks.
It does not reduce the maximum erasure degree or eliminate either tree.

Input: an explicit prime-field Lie algebra L, fixed ambient class c>=4,
class(L')<=3, p>max(c,3(c-2)), and an ordinary coherent hiding-function
oracle. For one transverse image call put m=dim(L/L'), and r,s,z for the
existing A,B,C dimensions, with C=FULL Z(L'). Let D=c-2, e=max(c,3D).
The scalar-derived branch and arbitrary-H recursion remain separate.

## Three Invariant Blocks

Fix the proof-only polynomial potential and its ordered coefficient basis
once per image call. Write theta_A, theta_B, theta_C for its three groups
of coefficients. These are never inputs to the controller. The actual
phase -sum Phi(g(Y_i+s_i*q), L^-1(t,zeta)_i) is a sum of the following:

| Hidden coefficient type | Total q degree | Total jet-register degree |
| --- | ---: | ---: |
| linear theta_C | <=c | 0 |
| linear theta_A or theta_B | <=D | <=2 |
| theta_A*theta_A or theta_A*theta_B | <=2D | <=1 |

There are no theta_B*theta_B, central cross-products, or higher parameter
products. Optional public terms of q degree <=c and no jet dependence can
be allowed without invalidating the bound; the original source needs none.

Proof from the actual phase formula: c0 is central and linear; gamma(a,x)
and delta(x,b) are linear in the hidden coefficients and in the carrier;
delta(x,beta(a,x)) and mu.beta(a,x) are linear in a and quadratic in the
carrier. The remaining terms delta(a,beta(a,x)), ell(a).b and
ell(a).beta(a,x) have hidden types A*A or A*B and carrier degree <=1.
The noncentral potentials have q degree <=D, and the central potential
has degree <=c. Public affine carrier alignment and fixed spectators do
not increase carrier degree or introduce hidden parameters.

The ACTUAL erasure map is

```
(q,t) -> (Y+s*q, Z+A(Y,s)*t).
```

It has no q-to-t or t-to-q block. Substitution preserves each separate
q-degree and jet-degree bound and does not change the hidden coefficient
type. Sums of such pullbacks preserve them too. Induction therefore
applies at every adaptive weighted node and every outcome. No source
coefficient is multiplied by another source's phase coefficient: phases
ADD, rather than multiplying as polynomials.

This is stronger than generic weighted-degree preservation. In particular,
the otherwise legal lower-weight map t_2 <- t_2+q sends
theta_A^2*q^(2D)*t_2 to a term theta_A^2*q^(2D+1). It preserves the broad
weight bound but breaks this source envelope. Do not apply the refinement
to arbitrary maps accepted by WeightedPhaseErasure's generic theorem.

## Exact SDE Equation Counts

Let

```
hA = r*binom(m+D,m), hB = s*binom(m+D,m), hC = z*binom(m+c,m),
H2 = hA*(hA+1)/2 + hA*hB,
n_k = r*binom(m+D-k,m), 1<=k<=D,
J = sum_k n_k.
```

n_k counts jet variables of weight k. Define H_m(u)=binom(m+u-1,u)
for u>=0 and zero otherwise. Let C_j(Q,T) count monomials of EXACT
weight j, q degree at most Q, and jet degree at most T, for T=0,1,2.
Start with H_m(j) if 0<=j<=Q. For T>=1 add
sum_k n_k*H_m(j-k), retaining only 0<=j-k<=Q. For T=2 also add

```
sum_(k<l) n_k*n_l*H_m(j-k-l)
  + sum_k binom(n_k+1,2)*H_m(j-2k),
```

again imposing the q-degree cutoff. A sufficient number of public
coefficient equations at weighted stage j is now

```
Ew_j = (1+hC)*C_j(c,0)
       + (hA+hB)*C_j(D,2)
       + H2*C_j(2D,1).
```

This counts every permitted parameter-monomial/physical-monomial pair.
It need not assume that the potential coefficients are independent.
Counting impossible pairs only overestimates the required arity.

After the phase is erased, negative jet Fourier readout yields eta.F(q).
This is linear in theta_A ALONE and has q degree <=D. Ordinary affine
erasure preserves that linearity, so at ordinary stage j a safe bound is

```
Eo_j = (1+hA)*H_m(j), 1<=j<=D.
```

Use these stage-specific counts, not just their maximum. The broader
Hlift*binom(m+J+e,e) bound remains a valid comparison, not the preferred
schedule. Existing leading-column extraction already uses actual sparse
coefficient keys, so no change to the cancellation identity is needed.

For fixed c, all these counts are polynomial in dim(L). This observation
does NOT imply useful constants or a small polynomial exponent.

## Published Solver Dependency

[Ivanyos--Santha, Theorem 11 and Section 3.3](https://arxiv.org/pdf/1503.09016)
give the deterministic all-input collision construction used here. With
G(j,E)=j^(j(j-1)/2)*(E+1)^j, use a_j(E)=G(j,E)^ceil(log2(j+1));
use a_1(E)=E+1. For j not dividing p-1, reduce to g=gcd(j,p-1).
Choose u inverse to j/g modulo (p-1)/g and lift y to y^u. When that
modulus is one use u=1; zero maps to zero. Then (y^u)^j=y^g.
The original j-based arity safely dominates the g-based one. Only j is
fixed; the number of equations may grow. No factorization of p-1 or
nonresidue oracle is assumed by that published deterministic construction.

2026-10-22: CUBIC_DIAGONAL_SOLVER.md adds the published g=3 construction
and integrates it with the Bezout adapter. The g=2 implementation still
requires p=3 mod4. This remains NOT the general solver; in particular
some stages at p=19 require g>3. All general fixed-degree polynomial-time
SDE claims here remain a cited dependency, not measured implementation
performance. Verifying a returned witness alone cannot certify a partial
solver's all-input success or its runtime.

## Adaptive Freshness And Rank

For a fixed original instance retain the complete classical record R:
labels, random draws, solver outputs, all measured coordinates, rejection
decisions and consumed-input history. Trace discarded hiding outputs;
do not condition on inaccessible purifications. At each ideal program
boundary the accessible state is

```
sum_R mu(R) |R><R| tensor product_(a in live(R)) sigma_a(R).
```

A fresh ordinary query on fresh registers supplies an independent factor.
Public classical processing only reads R. A local instrument consuming a
disjoint set of factors replaces that set by its one conditional output;
untouched factors remain a product. Every used input, even a zero-scale
discard, is removed. A rejected matrix batch is fully discarded before
starting a fresh attempt. This proves the invariant by program induction.

The record law mu need NOT factor. Forgetting a shared random record can
destroy the product statement, and a repeated bad seed is not a fresh
trial. The argument applies to the ideal process; the approximate device
is compared with that whole process later, not assumed to retain exact
product form itself.

For a fresh attempted matrix leaf, all central labels, including zero,
are retained. Conditional on labels and nonzero scales, the complete Y
tuple is uniform: the independent source diagonals are uniform and the
fresh-q shear is a bijection of the computational addresses. This holds
conditional on ANY PRIOR valid history, not after selection on new Y.

Divide the scalar feature row (s^k Y^alpha) by s!=0. It contains exactly
all monomials in (s,Y) of total degree <=D-1. For ell=binom(m+D,m+1), a
nonzero row dependence is a nonzero polynomial of that degree. The
product-domain root bound on F_p^* x F_p^m is (D-1)/(p-1). For b rows,

```
Pr[rank deficient] <= (p^ell-1)*((D-1)/(p-1))^b.
b=(ell+1)*bit_length(p)+2  => this is <=1/(4p).
```

The rank lift uses an identity A block and is uniform in EVERY central
label. Neither nonzero-character selection nor a source-level SDE is
needed. Acceptance may correlate the new public records; the exact
source formula holds record by record and does not need accepted records
to be IID.

## One Finite Schedule And Joint Error

Take t=m+ceil(log_p(4/epsilon)) final roots. The bottom-up stages are
weighted e,...,1 followed by ordinary D,...,1, with the above arities.
Let M=t*product(all arities). The number of nodes at stage i is t times
the product of arities AFTER i. In particular

```
sum_i nodes_i*(arity_i-1) = M-t,
merge_calls <= M-t.
```

Set a=ceil(log_p(8b)) for nonzero-scale draws, and
R=ceil(log_2(4M/epsilon)) matrix attempts per leaf. Each ideal attempt
fails with conditional probability <=b*p^-a+1/(4p)<1/2. Conditional
failure multiplication along one retry history and then a union bound
give leaf exhaustion <=M*2^-R<=epsilon/4. This does NOT assume IID trial
failures. It does require the uniform conditional bound and fresh inputs.

Successful terminal roots have exactly the same phase-free density,
independent of their successful records. Thus fresh quotient Fourier
rows are uniform on U-perp even conditional on earlier output rows. The
spanning union bound is (p^m-1)/((p-1)*p^t)<=epsilon/4.

The raw-query cap is Q=M*R*b. There are at most S=Q*a classical uniform
field draws. Binary rejection sampling uses bit_length(p) bits per trial
and fails each trial with probability <1/2. Cap it at
B=ceil(log_2(8S/epsilon)); total sampler exhaustion is <=epsilon/8.
Accepted field elements are exactly uniform. Count ABORT as an outcome;
never renormalize it away.

Let C=t*product(ordinary arities) be the curve Fourier readouts. One safe
count of complete instrument calls is

```
I = Q + M*R + merge_calls + C + t.
```

These are source, matrix alignment, merge, curve readout and final Fourier
instruments. Require half-diamond distance <=epsilon/(8I) for EACH
complete history-controlled instrument, uniformly including classical
outcomes and ABORT. CPTP contractivity and a telescoping hybrid bound the
whole output distance by epsilon/8. There is NO division by an outcome
probability. Gate-level synthesis must meet this complete-instrument
contract; this document does not extract those circuits.

Adding the four errors gives <=3*epsilon/4. Remaining slack is not a
license to omit a solver, arithmetic, or implementation failure term.
At constant target error, the required precision-bit count is logarithmic
in this polynomial schedule. Arbitrary-H calls use the separate first-
error union bound and additive original-oracle costs from Section 7 of
CLASS_THREE_MONOMIAL_FULL_JET.md, not products across reductions.

For depth-first evaluation, a conservative logical-register envelope is
(m+J)*(1+sum_i(arity_i-1)) + b*(m+r+s+z) + m. Oracle, reversible arithmetic
and synthesis ancillas are ADDITIONAL. Final roots can be measured and
released one at a time. Stored classical transcripts, coefficient tables
and solver workspace are also additional; keeping the entire record can
use polynomial space comparable to the total schedule. This is not a
gate-level or total-memory space certificate.

## Executable Evidence And Limits

Run `python -m theorems.full_jet_resource_certificate --write`.
The resulting standalone artifact contains exact counts in hexadecimal,
integer/rational clocks, node counts and the failure allocation. Decimal
logarithms are not used to choose a clock. The frontend's historical
comparison now also uses exact caps and explicitly retains its GENERIC
support envelope; the new standalone certificate defaults to source
structure.

For (c,m,r,s,z)=(6,6,9,2,4), epsilon=1/8:

| Prime | Generic query cap floor(log2) | Structured cap floor(log2) |
| --- | ---: | ---: |
| 19 | 36555 | 14641 |
| 2^127-1 | 36559 | 14645 |

These are floors of logarithms of enormous SUFFICIENT upper caps, not
lower bounds, achieved runtimes, or evidence of practical speedup. Do not
attempt the full tree as a numerical experiment. Better SDE algorithms,
rank/phase structure, or a different receiver would be needed for useful
resources.

Falsifiers exercised: exact clocks just above an integer-log threshold;
independent enumeration of weighted monomial counts; actual source
compiler and repeated Taylor pullbacks; a leading-degree merge; impossible
parameter products and carrier degrees; cross-block maps that preserve
weight but break the refinement; correlated retries with good marginals;
forgotten records; and global-small/conditional-large approximation error.
Finite tests do not prove the source, CPTP hybrid, or all-input SDE theorem.

Still blocked: one machine-checked end-to-end input/controller theorem,
general executable SDE, uniform physical synthesis, independent novelty
review and an access-matched useful hard application. The existing local
source theorems are reused, not promoted into those missing results.
