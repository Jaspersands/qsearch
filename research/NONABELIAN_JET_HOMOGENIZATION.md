# Nonabelian Polynomial-Jet Homogenization

2026-10-22. Status: PROVISIONAL constructive reduction, exact public algebra
and falsifiers. Not an independently reviewed theorem, executed quantum
receiver, novelty certificate, useful application, or Shor-level result.

SUBSEQUENT AUDIT: JET_ORACLE_HOMOGENIZATION.md replaces the initial
random source alignment by a deterministic tuple oracle when the input
is an ordinary coherent hiding FUNCTION. That is now the preferred
ordinary-oracle route and needs p>c. The state-only route and its random
rank schedule below remain separately labelled and retain p>2c. Public
polynomial-group algebra itself now admits the full p>c Lazard range.

## 1. Why This Is The Next Question

The preceding filtered induced receiver reduced its phase weight from kc
to c, but retained two enormous erasure trees and required N=L' to be
metabelian. This pass asks whether we can keep the whole nonabelian normal
register, convert it into an ordinary hidden-subgroup state in a larger
PUBLIC group, and obtain automorphisms that preserve the hidden subgroup.
It does not Fourier-scalarize N or compile unknown polynomial coefficients.

The old GRADED_HSP_PHASE_DESCENT.md correctly rejects direct dilation of
a generic H: cancelling scalar phases does not restore lost coset support.
The proposed escape is to construct a DIFFERENT group and hidden subgroup
for which preservation is an identity, not an extra input promise.

Target input: an explicitly presented finite-dimensional nilpotent Lie
algebra L/F_p of fixed class c, p>2c, unique coordinates, and an ordinary
coherent deterministic-label function hiding left cosets of H in exp(L).
Initially H intersects exp(N), N=L', trivially. No hidden polynomial
evaluator, nonlinear advice, new hiding-function oracle, or inverse of a
mixed-state preparation channel is available. Abelian inputs bypass this
construction. Growing c, small p and arbitrary black-box encodings are
outside the proposed uniform bound.

Conditional target: polynomial quantum time in dim(L) and log(p) for
each FIXED c. This would enlarge the preceding scope if correct and new.
No classical-hard external application has been identified.

## 2. The Ordinary Source And Its Filtered Potential

Write V=L/N. Transversality makes H abelian, with a linear image U in V.
The existing proof-only section word P(q) is

```
P(q) = exp(X(q)) exp(Y(q)+Z(q)) exp(-X(q)-Y(q)),
X=s(q-pi(q)), Y=s(pi(q)), Z=a(pi(q)).
```

Choose a public basis e_i of N adapted to the ACTUAL ambient lower-central
flag, with weight w_i>=2. AMBIENT_SECTION_POTENTIAL.md and the subsequent
filtered refinement give deg(log(P)_i)<=w_i. This degree argument does
not require N to be metabelian. Unknown pi, a, P and their coefficients
are proof witnesses, not inputs to any public operation below.

After tracing the original function output and inverting the normal
coordinate, the full regular source has matrix entries

```
rho[(q,x),(q',x')] = 1/(|V||N|)
    * [q'-q in U] * [P(q)*x = P(q')*x'].
```

The orientation follows the normal-first chart x^-1*s(q). It is already
supported by CosetMatrixSource's section-word/coset-relation lemmas; no
normal-subgroup QFT or preferred representation sector is used here.

## 3. Public Polynomial Group And Normalized Curve

Introduce formal variables u=(u_1,...,u_m) and t. Let A be the Lie algebra
of N-valued polynomials whose e_i coordinate has TOTAL degree<=w_i.
Pointwise bracket closes: [e_i,e_j] only has coordinates of weight
at least w_i+w_j, while polynomial degrees add. This is an exact
finite-dimensional algebra, not truncation of nonzero bracket terms.

Let J_lie be its ideal of polynomials divisible by t and J=exp(J_lie).
A public basis is e_i*u^alpha*t^d with d>=1 and |alpha|+d<=w_i. Thus

```
dim J = sum_i binom(m+w_i,m+1).
```

The following PUBLIC substitutions are automorphisms:

```
alpha_q R(u,t) = R(u+t*q,t),
S_s R(u,t) = R(u,s*t),  s != 0,
S_s alpha_q = alpha_(s*q) S_s.
```

Define the public semidirect group K=J semidirect V by
(x,q)(y,r)=(x*alpha_q(y),q+r). Give V degree one and J degree equal to
t-degree. Translation's derivation t*q.partial_u raises degree by one,
and brackets add degrees. No positive grade exceeds c. Consequently K
has class at most c and polynomial-size coordinates for fixed c.

ONLY IN THE PROOF, define

```
F(q)(u,t) = P(u)^-1 * P(u+t*q).
```

BCH respects the filtered total-degree caps, and F(q) vanishes at t=0,
so F(q) belongs to J. Crucially the normalization is on the LEFT.
Associativity and cancellation give the formal identities

```
F(q+r) = F(q) * alpha_q(F(r)),
F(Y+s*q) = F(Y) * [F(q) evaluated at (u+t*Y,s*t)],
F(s*q) = S_s(F(q)).
```

Replacing P(u)^-1*P(u+tq) with the opposite product fails the first
identity in a nonabelian N; a negative test catches that mistake.

## 4. Preparing The Lift Without Evaluating F

Take B fresh original regular sources, fresh independent nonzero s_i,
and a fresh uniform q register. Reversibly subtract s_i*q from each old
quotient register and measure Y_i. Every Y tuple has probability |V|^-B.
The common off-diagonal support remains q'-q in U, because U is linear
and each s_i is nonzero. Conditional on the complete record, the carrier
increment is exactly E(F(q')^-1 F(q)), where the PUBLIC homomorphism is

```
E: J -> N^B,  E(j)_i = j(Y_i,s_i).
```

Indeed P(Y_i+s_i*q)=P(Y_i)*F(q)(Y_i,s_i); the left constant cancels in
P(Y_i+s_i*q')^-1 P(Y_i+s_i*q). It is not an unknown conjugation.

Injectivity is tested by ordinary linear algebra in log coordinates.
Each coordinate uses monomials s^d Y^alpha with d>=1, |alpha|+d<=w_i.
Full rank of the largest scalar design, of dimension
ell=binom(m+c,m+1), suffices for every coordinate. After division by s,
a nonzero relation has degree<=c-1. Schwartz-Zippel on
F_p^m times F_p^* bounds its zero probability by (c-1)/(p-1)<1/2.
Union over fewer than p^ell relations gives rank-failure probability
at most (p^ell-1)*((c-1)/(p-1))^B. Taking
B=(ell+1)*bit_length(p)+2 makes this less than 1/(4p).
Failed batches are consumed and charged, never silently postselected.

Now E(J) need NOT be normal in N^B. Do not use a group quotient by it.
Choose a linear complement C in log(N^B), separately in each normal
coordinate, using evaluation columns followed by independent unit columns.
Both linear projections preserve the actual ambient filtration. The map

```
(j,k) -> E(j) * exp(k),  k in C,
```

is a bijection. To prove and compute this, write z=E(j)+k. Its logarithm
is z+T(z), with T starting at brackets. If a change in z lies in ambient
depth r, the change in T lies in depth at least r+2, because both inputs
have depth at least two and the projections preserve filtration. Iterate
z <- x-T(z) to invert; after at most c corrections the result is exact.
Uniqueness follows from the lowest nonzero depth of a hypothetical pair
of preimages. C need not be a subalgebra. A generic unfiltered complement
does not justify this argument.

Left multiplication by E(a) changes j to a*j and leaves k fixed. Perform
this public bijection reversibly, uncompute its scratch space, and measure
k, retaining EVERY outcome. Every k has mass |N|^-B |J|. The normalized
retained state is exactly

```
rho_F[(q,j),(q',j')] = 1/(|V||J|)
    * [q'-q in U] * [F(q)*j = F(q')*j'].
```

This is the SAME J and SAME F for every successful evaluation transcript,
not a new unrelated potential for each copy. Invert j publicly and
interpret the register as (j^-1,q) in K. The cocycle identity shows this
is the ordinary coset mixture for

```
H_F = {(F(u),u): u in U} <= K.
```

Only coset-state preparation has been obtained, NOT a new hiding function.

## 5. Exact Preservation And Central-Character Descent

Delta_s(x,q)=(S_s(x),s*q) is a PUBLIC automorphism of K. The scaling
identity gives Delta_s(H_F)=H_F for every s!=0. Also H_F intersects J
trivially. Both properties persist after quotienting any invariant
subgroup contained in J. No promise that original H is homogeneous is
being smuggled in, and no Vandermonde reconstruction of log(H_F) is
needed for this argument.

Remove the top remaining grade d=c,c-1,...,2. Its subgroup Z_d is central
elementary abelian, of dimension

```
r_d = sum_(i:w_i>=d) binom(m+w_i-d,m).
```

It lies in the remaining image of J, so H intersects Z_d trivially.
Central Fourier measurement on each fresh coset mixture produces every
label lambda in Z_d^* with probability 1/|Z_d|. Retain them all.
For the normalized projected density rho_lambda and the right action
R_g|x>=|x*g^-1>, direct contraction of the coset projector gives

```
Tr(rho_lambda R_g) = 0                    if g not in H Z_d,
                  = omega^(lambda.z)     if g=h*z, h in H, z in Z_d.
```

The z is unique. This holds for mixed coset sources, not just an unknown
selected pure coset. Apply the published fixed-degree diagonal-equation
solver to the PUBLIC labels to obtain a nonzero vector (s_i) satisfying
sum_i lambda_i*s_i^d=0. Consume and discard zero-scale inputs. All
remaining scales preserve H exactly and scale Z_d by s_i^d.

Prepare a uniform register over a public transversal of Z_d. Controlled
on representative g, apply tensor_i R_(Delta_si(g)) to the projected
source registers and then discard those registers. The Gram factor for
g,g' is the product of the displayed correlations at Delta_si(g'^-1*g).
It equals ONE on H Z_d and ZERO outside it: cancellation removes the
central character, while exact subgroup preservation keeps its support.
The new register is therefore precisely the coset mixture for H Z_d/Z_d.
No reverse source channel, hidden eigenstate, or label rejection occurs.

Repeat with fresh disjoint preparations at every child. Complete-record
conditioning is essential; matching marginals alone is insufficient, as
the earlier composition counterexample demonstrates. Ideal outputs here
are transcript-independent. At the final grade-one abelian quotient,
ordinary Fourier samples determine the image of H_F; projecting to the
original V recovers U. The abelian dimension is m+r_1, not merely m.

## 6. Scope Extension And Resource Cost

No part of this construction assumes N''=0. An actual scope witness is
N=gamma_2(ut_9), with
[[E13,E35],[E57,E79]]=E19 != 0. Its ambient class is eight. The new
ambient_jet_certificate constructs and verifies the real filtered chart,
without the preceding certificate's abelian-N' guard.

For arbitrary H, the following is a WRITTEN continuation, not a new
executable recursion: solve the restriction to N recursively to learn
K0=H intersect N, compute M=normalizer_L(log(K0)), and work in M/K0.
Here H/K0 intersects the derived subgroup trivially because M' is
contained in N. Run the transverse image routine; restrict to the
preimage T of the returned image. In the proof T=h+S' with h abelian,
so T' is contained in gamma_3(S), giving a strict class drop unless
already abelian. Transversality persists under these restrictions.
The initial N has class at most floor(c/2), so recursion terminates.
Canonical quotient representatives and workspace cleanup must be explicit
before claiming an executable oracle reduction. Never assume N is
contained in M, and take Lie closure if an inner solver returns generators.

For each FIXED c, J has polynomial dimension, there are at most c-1
central stages, and the published SDE arity is polynomial in r_d with
degree depending on d. Their product is thus polynomial in dim(L), not
in c. BCH coefficient precomputation exponential in c is charged as a
fixed-class constant, not hidden from a growing-class claim.

The live resource artifact uses the previous actual c9, m2, dim(N)=17
weight multiset. The new J has dimension994, K dimension996, and
(r_1,...,r_9)=(344,249,171,110,65,34,15,5,1). At p43, one initial batch
costs998 original sources. Eight SDE stages replace the two symbolic
erasure trees. A conservative sufficient original-query CEIL-log2 bound
for one transverse call is1776, versus4496 in the preceding filtered
scheme; at p=2^127-1 the new bound is1781. Both are astronomically large
UPPER bounds, not measured runtimes, lower bounds, or practical speedups.

The schedule charges failed alignment batches with capped fresh retries
and enough final abelian samples. In the ideal exact SDE/gate model its
alignment-abort and rank-failure bounds are each below1/(4p). Approximate
gate synthesis, the general SDE implementation, and all arbitrary-H
recursive calls are not represented by this single-call count.

## 7. Attempts To Disprove It And Remaining Blockers

- Wrong normalization order: falsified by a noncommuting control.
- E(J) assumed normal: false in an exact test; the filtered coset chart
  works without normality. Its bijection, not a quotient, is required.
- Bracket-compatible integers mistaken for actual ambient weights:
  rejected by the embedding certificate and a deliberately mixed basis.
- Abstract Lie formulas drifting from real groups: BCH agrees with
  independent matrix exp/log, including nonmetabelian N and a127-bit prime.
- Direct dilation assumed safe: a nonhomogeneous UT4 hidden subgroup
  loses support. Its actual section potential passes the lifted identity,
  and original group cosets agree with the aligned register relation.
- Phase cancellation alone called descent: the finite central instrument
  succeeds on preserved H and fails on nonpreserved H with the SAME
  cancelling cubic labels. These are falsifiers, not algorithm benchmarks.
- Pure-state checks mistaken for mixed-channel composition: a separate
  complete125-by-125 density test retains all central labels and verifies
  every entry of the resulting25-by-25 quotient state. This is still only
  a bounded control; the general channel claim rests on the trace argument.
- Branch normalization omitted: exhaustive small register permutation
  checks retain all spectator outcomes; the general count rests on the
  triangular bijection proof, not finite statistics.
- Input advice leaked into operations: only functions explicitly named
  fixture accept P. Public chart/factorization never receives P or U.
- Source independence assumed from marginals: still forbidden. All
  children must be fresh conditional tensor factors, consumed once.
- General quantum program inferred from exact classical checks: forbidden.
  No physical preparation, SDE backend, controller or complete extracted
  program is implemented in this pass. No new Lean theorem was added.
- Novelty inferred from a search miss: forbidden. Independent review of
  the entire ordinary-source-to-graded-state bridge is the next priority.
- A black-box query separation mistaken for an application: forbidden.
  Public-circuit interpolation, low-degree and orbit-module classical
  filters remain live. Enlarging HSP scope does not establish a useful
  hard explicit-object problem, a DCP algorithm, or a Shor-level result.

The sharpest outstanding mathematical audit is the complete physical
composition: actual section degree -> public coherent factorization ->
same normalized lifted coset mixture on every record -> mixed-state
central descent -> correct original image. A counterexample to ANY arrow
invalidates the proposed uniform result, regardless of the local tests.

## 8. Prior Art And Reproduction

The [nil-2 algorithm](https://arxiv.org/abs/0707.1260) already uses
automorphism-twisted character cancellation. The
[constant-class bounded-prime result](https://arxiv.org/abs/2304.08376)
uses central subgroup-state conversion and explains why generic higher
class lacks the needed automorphisms. This draft proposes constructing
a different polynomial group where the relevant hidden subgroup is
preserved; it does not contradict the obstruction for the original group.
The [fixed-degree SDE theorem](https://arxiv.org/abs/1503.09016) supplies
the cited all-input cancellation algorithm, not new work here.
Polynomial graph/semidirect-product algorithms are essential comparison
targets. Targeted searches do not establish novelty or supersede them.

```
python -m pytest -q tests/test_nonabelian_jet_homogenization.py -W error::RuntimeWarning
python -m theorems.nonabelian_jet_homogenization --write
```

The implementation is an exact mathematical control and certificate
module. It deliberately does not edit qsearch, UI, central candidate
admission or the general-purpose search registry.

Twenty new tests pass; the final connected suite passes179 tests in26.65s
with RuntimeWarning fatal. Syntax, qsearch validation and existing
site checks pass. No full-repository Python run or new Lean proof is
claimed. The ambient input contract remains a genuine Lie algebra; an
arbitrary Python callable is not thereby certified bilinear on all inputs.
