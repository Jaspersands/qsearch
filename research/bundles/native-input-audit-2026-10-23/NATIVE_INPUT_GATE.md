# Native Input Gate: Local Pairings Do Not Manufacture An Isogeny

2026-10-23. COUNTING FALSIFIER; INDEPENDENT REVIEW PENDING.

## Research Decision

The current surface chain starts with a genuine weak evaluator for ONE
ell-polarized isogeny phi:E^2->B and a known full source order. It proposes
kernel recovery and downstream endomorphism-ring transport FROM that input.
It does not start with a bare target B, and it does not find an arbitrary
isogeny between two given varieties.

This distinction now matters more than adding another receiver variant.
The direct surface chirp receiver and conditional source construction make
a concrete theorem candidate, but do not by themselves establish a new
general isogeny algorithm, a cryptographic break, or Shor-level significance.
Do not promote the proposed input model while trying to obtain the input.

One tempting source-acquisition strategy is demonstrably inadequate:
construct random small-torsion maps which pass the required pairings, then
treat them as weak samples of one isogeny. The bound below makes the gap
quantitative. It rejects that sampling strategy, not every conceivable
algorithm for constructing a weak evaluator.

## 1. Precise Experiment Being Falsified

Fix principally polarized surfaces A and B over an algebraic closure of
characteristic p>3. Fix an odd prime ell != p. The eventual source has
A=E^2, but the counting argument does not require that extra structure.

Choose distinct odd auxiliary primes r, all coprime to p*ell. At each
level, fix ordered symplectic bases for A[r] and B[r]. Independently sample
a uniformly random projective class of linear maps W_r which are
compatible with a common-unit weak image of a multiplier-ell isogeny:

    W_r^t J W_r = a_r^2 * ell * J

for some a_r != 0, identifying W_r with b_r W_r for any b_r != 0.
These maps pass ALL the full-basis Weil-pairing constraints, not just one
entry. The question is whether there exists a SINGLE global polarized
ell-isogeny inducing the entire tuple of weak classes.

The source and target must be fixed before this random sampling. This
experiment is not the distribution of honest samples from a supplied phi.

## 2. Local Count

After rescaling a_r away, the multiplier is exactly ell. Fixing one
multiplier-ell similitude identifies the possibilities with Sp_4(F_r).
Exactly the two scalars +/-1 preserve this fixed multiplier. Therefore the
number of weak projective classes at one level is

    N_r = |Sp_4(F_r)|/2
        = r^4 (r^2-1)(r^4-1)/2.

For clarity, the group count follows by selecting a symplectic basis:
v1 has r^4-1 choices, w1 with <v1,w1>=1 has r^3 choices, v2 in their
symplectic orthogonal complement has r^2-1 nonzero choices, and w2 in
that complement with <v2,w2>=1 has r choices.

The independent sample space at all levels has size product_r N_r. A
repeated prime is not another independent constraint and the code rejects it.

## 3. Global Count

An ell-polarized isogeny out of a principally polarized surface has a
Lagrangian kernel in A[ell]. The number of such planes is

    L_ell = (ell+1)(ell^2+1).

One derivation counts ordered isotropic independent pairs:
(ell^4-1)(ell^3-ell), divided by the number
(ell^2-1)(ell^2-ell) of ordered bases of a two-dimensional plane.

For each kernel, the polarized quotient is determined up to polarized
isomorphism. If it is isomorphic to the fixed B, the maps with that kernel
form a torsor for Aut(B,lambda_B); otherwise there are no such maps.

Here is a conservative uniform bound which does NOT grant a target order
or compute any secret torsion. Polarized automorphisms form a finite group:
their Rosati norm is fixed and they lie in a positive-definite integral
endomorphism lattice. They act faithfully on B[3]. Indeed, the Tate-module
action is faithful and 1+3*M_4(Z_3) is torsion-free. To see the latter,
if U=1+3^s C with s>=1 and C nonzero mod 3, powering by a prime other than
3 preserves the minimal 3-adic valuation of U-1; cubing increases it by
exactly one, by binomial expansion. No nonidentity such U can have finite
order. A polarized automorphism also preserves the Weil pairing. Hence

    |Aut(B,lambda_B)| <= |Sp_4(F_3)| = 51840.

Since phi and -phi always induce the SAME tuple of weak projective classes,
the number of globally realizable tuples is at most

    M_ell = 25920 * (ell+1)(ell^2+1).

There may be further coincidences or far fewer quotients isomorphic to B.
Both make this upper bound more conservative. No projective rigidity
theorem is needed for this direction of the count.

## 4. Probability Bound

For the independent uniform sampling experiment of Section 1,

    Pr[one global phi exists]
      <= min(1, M_ell / product_r N_r).

For T independent attempts, a union bound is T times the single-attempt
bound, capped at 1. The implementation uses exact integers and rational
arithmetic, and rounds the reported base-two exponent UP conservatively.
It does not run a geometric consistency test or estimate probability from
small samples.

Write R=product r and s=number of levels. Then

    product N_r = R^10 * 2^(-s)
                   * product (1-r^-2)(1-r^-4).

The final product is bounded below by an absolute positive constant over
distinct odd primes. Consequently the probability is

    O(ell^3 * 2^s / R^10).

Taking successive small primes until R>8*ell gives s=O(log ell/log log ell)
and the bound ell^(-7+o(1)). Excluding p and ell does not change that
asymptotic estimate. The finite arithmetic receipts use the exact expression,
not an asymptotic approximation. The threshold R>8*ell is merely a useful
public example plan; no geometry or successful interpolation is implied.

## 5. Attempts To Overstate Or Evade The Result

- Honest weak evaluations already satisfy the global promise. The bound
  says NOTHING negative about their consistency and cannot reject them.
- An algorithm exploiting geometry to correlate levels is not covered by
  the independent sampling experiment. This is not a hardness lower bound.
- Choosing B after sampling, changing the isogeny multiplier, or allowing
  unrelated isogenies at different levels changes the problem. It cannot
  be inserted into the existing source theorem without a new reduction.
- Local symplectic compatibility is necessary but not sufficient even
  when every pairing entry is checked. More finite pairing tests do not
  supply the missing global promise.
- Interpolation is not a source generator. The relevant PPAV interpolation
  theorem requires modeled endpoints and evaluations of an existing
  polarized isogeny. A polynomial does not become an isogeny because an
  interpolator accepts an unchecked interface.
- The coarse automorphism bound is deliberately loose. Tightening it would
  change constants, not repair the independent-random-mark strategy.
- Neither high data redundancy nor the small number of possible global
  maps gives an efficient recovery algorithm. Enumeration of ell^3 kernels
  is exponential in log ell.
- A known full Hom-module, target endomorphism basis, or unpolarized
  splitting is NOT a harmless source convenience. The prior classical
  attacks explicitly exploit those stronger inputs.

## 6. Consequence For Research Priority

Keep the surface chain as a concrete conditional theorem candidate. The
next work must justify ONE of the following, rather than extend the table
of finite receiver controls:

1. An independently checked end-to-end source theorem with the existing
   genuine weak-evaluator input, plus an exact comparison with the known
   elliptic IsERP result. This could be a contribution, but is not by itself
   evidence of Shor-comparable significance.
2. A natural explicit representation or protocol which supplies that input
   and is not already eliminated by the full-order, explicit-product or
   supplied-mixing-map classical attacks. State the actual security or
   computational problem solved; do not infer a break from the framework.
3. A charged reduction from a materially broader problem to this weak-input
   problem. It must construct globally compatible data without assuming
   the kernel, a target order, or the desired isogeny. Random local marks
   do not provide this reduction.
4. A new same-input classical attack, which would falsify or sharply narrow
   the intended advantage and therefore still be useful research progress.

If none of these can be advanced concretely, pivot to an independent
algorithmic mechanism. Do not use source-parameter variants as a substitute
for a significant problem. The scope of the current claimed contribution
is a possible SURFACE weak-IsERP extension, not general isogeny pathfinding.

The known elliptic quantum IsERP algorithm of
[Chen, Imran, Ivanyos, Kutas, Leroux and Petit](https://arxiv.org/abs/2305.19897)
already takes an isogeny evaluation representation and obtains a polynomial
quantum algorithm in its stated degree regime, with a pSIDH application.
It is prior art, not a discovery of this project. The present counting
argument does not establish novelty of our surface extension.

## 7. Known-Factor Padding Does Not Recover A Missing Source Order

Another proposed bridge starts from E_known x E_unknown, with a known
endomorphism order on only the first factor, and adds known auxiliary
factors in an attempt to use the surface group's elementary lifts. This
does not automatically recover the original theorem's source promise.
There is an exact information obstruction for the resulting one-sided
hidden-stabilizer method.

### General one-sided lemma

Let V be the known factor's torsion space, U the untouched unknown space,
and K a subspace of V direct-sum U. Write

    L = K intersect V,       S = projection_V(K),
    U0 = projection_U(K).

Then K is described by a surjection f:U0 -> S/L, with
K={(v,u): u in U0, v mod L=f(u)}. If projection to U has extra kernel it
is exactly L; f need not be injective, but its image is all S/L.

For a group G acting on V and trivially on U,

    Stab_G(K) = {g in G : gL=L and (g-I)S is contained in L}.

Proof: preserving K first requires gL=L. For every (v,u) in K, its image
(gv,u) must have the SAME u coordinate. This is equivalent to gv-v in L
for every v in S. Conversely, those two conditions send K into itself,
and invertibility gives equality. No symplectic assumption is needed.

The stabilizer depends on L and S but not on the actual gluing map f.
Changing that gluing while keeping L,S gives exactly the SAME coset
partition of G. Standard coset-state preparation, which discards the
opaque output register, produces the same density operator in every case.
There is no measurement on those states which can recover the differing f.

### Original graph and padded graph

Without padding, a transverse Lagrangian in V direct-sum U, with both
spaces two-dimensional, is the graph of an anti-isometry f:U->V.
Here L=0 and S=V, so its stabilizer for ANY faithful one-sided linear
action is trivial. All such secret gluings give injective oracle fibers.

Add a known elliptic auxiliary factor with a known kernel line L. The known
space V now has dimension four; S is the original known two-dimensional
plane plus L. The new kernel is K_f={(f(u)+l,u)}. It is Lagrangian in the
six-dimensional symplectic ambient space. All ell*(ell^2-1) anti-isometries
f still give the SAME stabilizer under the larger Sp_4(F_ell) action.
The extra known factor does not restore the lost gluing information.

The finite control checks all 51,840 elements of Sp_4(F_3) against all 24
anti-isometric gluings. Their common stabilizer has 54 elements (index
960), with zero disagreement. It constructs no hiding function and does
not present these explicitly supplied subspaces as unknown search inputs.

### Scope of this exclusion

This rules out recovering the gluing from that one-sided hidden subgroup
or its coset states. It does not rule out using the CONTENT of geometric
labels, another action involving the unknown factor, a hidden-shift
comparison with an independently available reference source, or a different
quantum algorithm. Each needs a new, charged mechanism. In particular, do
not silently replace the absent unknown-source order by an abstract matrix
action whose geometric lifts are unavailable.

This is a reason to retain the full known-source-order obligation, not a
proof that acquiring it is impossible. It also prevents an unjustified
application of the current chain to representations whose domain contains
an unknown-order factor, as can happen in higher-dimensional constructions.
