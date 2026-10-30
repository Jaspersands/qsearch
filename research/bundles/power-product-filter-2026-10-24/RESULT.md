# Exposed Power Products Do Not Manufacture Hard Symmetry

2026-10-24. Local written reduction plus an implemented exact classical
solver for UT_D(F_p). No independent review, Lean proof, general circuit
factorization algorithm, quantum algorithm, or novelty claim.

## Research Decision

The preceding pass closed a normalized central-instrument proof gap. This
pass first checked the current Rees scope against published HSP results:
the [nil-2 algorithm](https://arxiv.org/abs/0707.1260), the
[bounded-prime fixed-class result](https://arxiv.org/abs/2304.08376), and
[restricted semidirect/quasi-Hamiltonian families](https://arxiv.org/abs/2608.05321).
The inspected scopes do not establish that the proposed all-prime,
fixed-class theorem is already covered. This targeted refresh does NOT
certify novelty or independently validate the complete theorem.

Inspection also found that the natural graph/code/tensor and
cross-characteristic routes, and the hidden-codimension resource bounds,
already have substantial filters in the repository. Repeating those is
not progress. The remaining succinct-polynomial application suggested a
specific missing attack: enormous formal degree arising from exposed
products of powers, even when the raw derivative and mixed-Frobenius
guards fail. The old orbit-module note has a single-power warning, but
does not provide this multi-atom reduction or its sharp factor-count gate.

The result below excludes that entire construction pattern when its
factor support is too small. It is an application of elementary unique
factorization and p-group actions, not a claimed new invariant-theory theorem.

## Exact Native Problem

Let Gamma be a supplied finite p-subgroup of GL_D(K), where K has
characteristic p. The native task is to compute the FORMAL stabilizer

```
Stab_Gamma(F) = {g : F(g^{-1} x) = F(x) as polynomials}.
F = c product_i P_i(x)^{e_i},       c != 0, e_i > 0.
```

The nonzero polynomials P_i and the binary exponents e_i are exposed
input. They need not be irreducible, distinct, squarefree or coprime.
The exponents may be arbitrarily large and divisible by p. A zero atom
with positive exponent makes F zero and the answer the whole group.
An exponent zero removes that atom; negative exponents are not allowed.

This is the SAME public polynomial and group action as the proposed Rees
application. It is not a newly relabeled oracle problem or an assumption
that the classical competitor can inspect a hidden subgroup.

## Small-Factor-Support Reduction

**Claim.** If F has R distinct nonassociate irreducible factors and R<p,
then

```
Stab_Gamma(F) = intersection_i Stab_Gamma(P_i).
```

**Proof.** Put H=Stab_Gamma(F). Unique factorization implies that H
permutes the R irreducible factor classes, preserving their multiplicities.
The image of this action is a p-group contained in S_R. Since p does not
divide R! when R<p, the image is trivial. Thus for each irreducible factor
f_j and each h in H, substitution sends f_j to a_j(h) f_j with
a_j(h) in K^*. The element h has order p^b for some b, so
a_j(h)^{p^b}=1. In characteristic p,
X^{p^b}-1=(X-1)^{p^b}; a field has no nontrivial such root of unity.
Therefore a_j(h)=1. Every factor is fixed EXACTLY, not just projectively.
Consequently every P_i is fixed. The reverse containment follows by
multiplying the identities. No hidden factorization is computed. QED.

A publicly computable sufficient bound is

```
R <= degree(rad(product_i P_i)) <= sum_i degree(P_i) = B.
```

Thus B<p is a conservative certificate. The huge e_i do not appear in
it. Shared factors and multiplicities only reduce R. The argument concerns
the stabilizer H, not an incorrect assumption that the whole ambient
Gamma preserves the exposed atom set.

Useful stronger variants, not needed by the implemented conservative gate:

- It suffices that every irreducible-factor class of a fixed degree and
  multiplicity has fewer than p members, since the action preserves both.
- A single exposed power P^e always has the same p-group stabilizer as P:
  the ratio of its transforms is a scalar root of unity and p-power order
  kills that scalar. No R<p assumption is needed for that special case.

The general gate does not silently assume either stronger certificate.

## Obtaining The Stabilizer, Not Just Testing Elements

The reduction can use any costed classical simultaneous atom stabilizer
algorithm. Two routes already available in the repository are:

1. Small atom orbit modules. Learn each atom module with the existing
   capped extension-field/PIT method. Direct sums and the original faithful
   block turn simultaneous stabilization into vector stabilization.
   [Luks, Theorem 3.2(5)](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
   gives the relevant published solvable-matrix-group backend. For a
   defining-characteristic p-group its noncharacteristic-prime parameter
   is bounded. That general backend is not reimplemented here.
2. Low atom degree. With Gamma in GL_D(F_p), p>D, and
   `(D-1) max_i degree(P_i) < p`, the existing finite/infinitesimal
   proof applies to EACH atom. Learn the common kernel of
   `gradient(P_i)(x)^T A x` for A in log Gamma and exponentiate its basis.
   Public low-degree circuits can use the existing charged PIT argument;
   explicit polynomial atoms permit exact coefficient linear algebra.

`power_product.py` implements the second route for the full public
UT_D(F_p), so its Lie basis is explicit and unambiguous. SymPy's polynomial
arithmetic and finite-field DomainMatrix nullspace perform the symbolic
and linear computations. All returned generators are substituted back
into EVERY active atom and checked as formal polynomials.

Completeness is not inferred from those generator checks: it follows from
the factor-support proof and the finite/infinitesimal equivalence. For the
latter, P_i(exp(tA)x) has t-degree at most (D-1) degree(P_i)<p.
An invariant exp(A) gives all p values of t and hence a constant polynomial;
conversely its zero derivative forces a constant under the same degree bound.
The learned kernel is therefore exactly log H. Its basis generates H by
the Lazard correspondence for strictly upper triangular matrices with p>D.

The implementation cost is polynomial in the EXPANDED atom input size,
D, log p, and binary exponent lengths, not in degree(F). It never expands
the enormous outer powers. Passing an arbitrary compact SymPy expression
as an atom may incur expansion in `Poly`; this is NOT a polynomial-time
claim for arbitrary small circuits. Primality is a mathematical input
promise. The built-in screen rejects ordinary composites but is not a
general primality certificate. The live 127-bit field has a separate
Lucas-Lehmer certificate.

## A Family Eliminated Before Quantum Work

For p>max(D,2(D-1),3), take

```
Gamma = UT_D(F_p),
P_1 = x_0,             e_1 = p^8-1,
P_2 = x_0+x_1^2,       e_2 = p^9+2.
```

B=3<p. Stabilizing P_1 fixes the first row. Stabilizing P_2 then fixes
the second row, because the coefficient of x_1 x_j is twice that row's
off-diagonal entry. The exact hidden subgroup is the embedded UT_(D-2)
on the remaining coordinates, of Lie dimension (D-2)(D-3)/2.

At D=4 this is a class-three ambient group, within the proposed Rees core;
at larger D it also illustrates that the classical attack needs no fixed
class bound. The live D=4,6,10 controls at p=2^127-1 return dimensions
1,6,28 and verify every finite generator. The full formal degree has more
than 1,100 bits. The raw-degree guard fails. Even an exposed base-p
Frobenius expansion gives relaxed degree

```
digit_sum_p(e_1) + 2 digit_sum_p(e_2) = 8(p-1)+6 = 8p-2,
```

so that particular mixed no-carry guard fails as well. This is NOT a claim
that every prior classical attack fails, or that its orbit rank was proved
large. The new reduction suffices to solve the original task regardless.
These controls are deliberately easy counterfamilies, not candidates.

## Attempts To Break The Claim

**The threshold must be strict.** For the shear x -> x+t y in F_p,

```
product_(a in F_p) (x+a y) = x^p-x y^(p-1)
```

is invariant under ALL shears, while no nonzero shear fixes the first
linear atom. There are exactly p distinct factors. At B=p the implemented
gate returns OUT_OF_SCOPE rather than incorrectly intersecting the atom
stabilizers. This also shows why one must bound irreducible factors, not
merely count syntactic multiplication gates or named atoms.

**The p-group premise matters.** Over F_5 the order-two variable swap
preserves xy without fixing x or y, although two factors are fewer than p.
Likewise x -> -x preserves x^2 but not x: scalar semi-invariants cannot be
discarded for arbitrary groups. Both are exact test controls.

**The derivative guard is separate.** B<p does not imply
`(D-1) max degree(P_i)<p`. When the second condition fails the factor
reduction can remain mathematically valid, but this particular solver
returns OUT_OF_SCOPE. It does not label the family hard.

**Finite functions are not formal polynomials.** Tests compare formal
coefficient dictionaries, not evaluation tables over F_p. The norm
counterexample's behavior cannot license a change of the native problem.

**Input access is not free factorization.** The product structure is the
actual input. For a separate unstructured circuit, a proposed decomposition
requires a charged identity certificate and access to its atoms. General
circuit factor results have degree-dependent bounds; they do not grant a
poly(log degree) factorization algorithm here. See the precise scope in
[Chou--Kumar--Solomon](https://eccc.weizmann.ac.il/report/2019/037/).

**Tests are not the universal proof.** Small fields exhaustively compare
the entire generated output subgroup with the stabilizer of the EXPANDED
original product, including shared/reducible atoms. Large-field controls
check the stated closed-form subfamily without enumerating its group or
expanding its outer powers. The universal reduction is the written proof
above, still pending independent review.

## Consequence For The Search

Do not promote exponential formal degree, failed raw derivative guards,
failed mixed-Frobenius guards, or orbit-rank caps as hardness. Add the
small-factor-support gate before investing in a quantum receiver.

An exposed power-product construction must either contain intrinsically
hard atoms or permit nontrivial factor permutations. For a large prime,
the latter requires at least p equal-degree/equal-multiplicity irreducible
factors in some orbit. Encoding such a large orbit succinctly is a specific
structural requirement, not evidence of hardness. Simple additive norms
and Moore forms already have existing classical filters.

The next useful experiment is on a genuinely specified compressed
norm/resultant family or another native input, with its OWN same-input
classical attack. Do not generate an arbitrary planted factor orbit and
call it a hard application. This pass narrows the application search;
it neither solves the remaining succinct-circuit case nor establishes a
Shor-level algorithm.
