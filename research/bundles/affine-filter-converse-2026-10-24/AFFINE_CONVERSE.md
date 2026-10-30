# Affine Filtering Is Not Outside The Existing Positive-Mixture Comparator

Status: LOCAL UNREVIEWED synthesis and proof-control implementation. The
measurement characterization is established prior art, not a claimed new quantum
algorithm. The new repository conclusion is that the existing classical affine
sampler covers a larger proposed escape route than its documentation stated.

## Decision And Exact Scope

Do not launch an affine-filter LP optimization campaign as an escape from
LINEAR_ERASURE_PRANGE_DUALITY. For a canonical binary group-covariant pure-state
channel, every covariant error-free affine filtering POVM has a positive affine
frequency-mixture description, with exactly the same unresolved subspaces and
branch probabilities. Thus the earlier positive-mixture construction is not
merely one arbitrary subclass of these covariant affine measurements.

For disjoint local blocks, public product factors, nonadaptive measurements and
global Gaussian reconstruction, the SAME branchwise rank condition feeds the
existing matched classical sampler. Efficiency, sign-distribution and partition
normalization assumptions remain essential. This is not a universal classical
simulation of quantum receivers, nor an arbitrary-fixed-instance Gibbs theorem.

This supersedes the immediately preceding tree-duality note's suggestion to
investigate this particular affine-filter escape before implementing it. The
literature and prior repository comparator already close it under these promises.

## Prior Art And Repository Context

[Mandal, Shutty, Pfister and Jordan, Sections3.3-3.5](https://arxiv.org/html/2606.07852v2#S3)
characterize affine filtering by a character-based linear program. In their
notation, Gram eigenvalues are kappa_y=N*q_y and an LP variable theta_(V,L)
is constant on a coset L of the annihilator of V. Substituting
w_(V,L)=|L|*theta_(V,L)/N turns their feasibility constraints into positive
affine-mixture mass budgets. Their Section3.8 treats zero eigenvalues through a
limiting LP. The direct Gram proof below does not divide by q and handles zeros.
No novelty of the general equivalence is asserted.

The resident LINEAR_ERASURE_PRANGE_DUALITY.md already constructs instruments
FROM positive affine mixtures and a matched classical Gibbs sampler. It leaves
necessity of that representation open. PARITY_BLOCK_USD_PRANGE.md already
supplies sign-average normalization bounds and a planted-sign counterexample.
Their captured hashes are in source_context.json; neither file was modified.

## A Direct Gram Proof Of Necessity

Let C=F2^r, N=2^r and q_y>=0 with sum_y q_y=1. Define

    |psi_d> = sum_y sqrt(q_y) (-1)^(d.y) |y>,
    G(d,e) = sum_y q_y (-1)^((d+e).y).

A measurement outcome names a coset s+V containing d, where V<C is a linear
subspace. Its positive effect E_(V,s) satisfies unambiguity:
E_(V,s)|psi_d>=0 if d is outside s+V. The usual statement about a zero outcome
probability implies this vector statement because the effect is positive.
Covariance means translating d translates s, with V unchanged.

Put E_V=sum_s E_(V,s) and define its contribution Gram matrix

    K_V(d,e)=<psi_d|E_V|psi_e>.

It has three properties:

1. K_V is positive semidefinite.
2. K_V(d,e)=f_V(d+e) by covariance.
3. f_V(w)=0 whenever w is outside V. Indeed d,e then lie in different
   V-cosets, and for each outcome at least one of its two state vectors is killed.

Define the normalized Fourier coefficients

    h_V(y) = (1/N) sum_w f_V(w) (-1)^(w.y).

The circulant eigenvalues are N*h_V(y), hence h_V(y)>=0. Property3 implies
h_V(y+z)=h_V(y) for all z in V^perp. Thus h_V is constant on every affine
coset L=a+V^perp. For each such coset set

    w_(V,L)=|L| h_V(a).

The erasure contribution K_e=G-sum_V K_V is also positive semidefinite and
circulant, so q_e(y)=q_y-sum_V h_V(y)>=0. Regard each nonzero q_e(y) as a
point-mass affine branch. This gives the exact normalized decomposition

    q_y = sum_(V,L) w_(V,L) 1[y in L]/|L| + q_e(y).

The total weight for direction V is sum_L w_(V,L)=f_V(0), exactly the original
probability of observing direction V for EVERY classical codeword. A frequency
coset has dimension r-dim(V), so it reveals exactly r-dim(V) linear bits and
leaves dim(V) unresolved. Residual points reveal none. The entire direction law,
not merely expected information, is preserved.

No inverse Gram matrix was used. If q_y=0, all nonnegative components at y
must vanish. A positive-weight frequency coset cannot include that y. This
handles singular physical channels without pretending tiny regularizers are free.

## Sufficiency, Phases And What Is Actually Equivalent

Conversely, any normalized positive affine mixture supplies the branch isometry
already derived in the repository. For L=a+W it sends a codeword state into

    sqrt(w_L) (-1)^(a.d) |W-basis-transpose*d, L>.

Its Gram contribution is w_L*(-1)^(a.(d+e))*1[d+e in W^perp]. Summing these
contributions returns G. Equal Grams define an isometry on the input span,
including singular spans. The source-preparation and gate-compilation cost of
implementing this isometry are NOT supplied by the existence argument.

The refinement by L preserves the outcome effects/coarse direction law and
the relevant Gram contributions. It need not preserve arbitrary subsequent
processing of the original postmeasurement quantum states. For a decoder that
discards the quantum residuals and uses only the affine equations, it preserves
the information used by Gaussian reconstruction. A later coherent use of the
residual is an additional algorithmic mechanism and lies outside that comparison.

Affine offsets contribute real signs and cannot be dropped. Negative input
overlaps do NOT imply negative mixture weights or escape this theorem.

An arbitrary noncovariant affine measurement can be twirled over C for a
UNIFORM classical codeword prior, preserving any direction-only expected reward.
Therefore local mean-dimension optima may be restricted to covariant effects.
This does not preserve arbitrary global adaptive behavior or a nonuniform
coherent prior. The code rejects noncovariant inputs rather than silently twirling.

## Consequences For The Two Existing Controls

For four parity-constrained binary PSC messages with overlap c, the resident
six-branch mixture has mean unresolved dimension 4*c^2-c^4. Its exact dual
witness on the eight characters is

    z0=3, z_y=1 for odd weight, z_y=-7/3 for weight2.

For every affine frequency space L, average_L z <=3-dim(L). All51 such
spaces are checked exactly; the inequality also has the original fixed finite
certificate. Multiplying by mixture weights proves the lower bound. Necessity
above upgrades the conclusion to optimal mean unresolved dimension among ALL
affine filtering POVMs with uniform classical codeword prior, not all quantum
measurements. No minimum-error or coherent-superposition optimality follows.

Similarly q=(1/10,3/10,3/10,3/10), with negative nontrivial overlaps -1/5,
has optimum unresolved dimension3/5 for affine filtering. The witness
z=(-3,1,1,1) is checked against all11 affine spaces. Off-origin frequency
lines are essential. Both examples were already dequantized at the public
Gibbs-factor level; their improvements over product USD are not revived.

## Matched Classical Rank And Its Normalization Debt

For the unchanged public factor model with x in F2^h,

    G(x)=product_i [2^r_i q_i(A_i*x+b_i)],

draw a local branch L_i=a_i+V_i^perp with its weight. A basis U_i of V_i gives
the affine equations U_i A_i*x=U_i(a_i+b_i). The quantum unresolved codeword
differences are exactly V_i, so its Gaussian reconstruction matrix concatenates
A_i^T U_i^T. It is the TRANSPOSE of the stacked classical equation matrix.
Thus full quantum column rank and full classical row rank coincide branchwise,
not only at a fitted average threshold. This does not require IID dense labels.

Let d be the total number of selected independent local equations, Z_l the
number of their solutions and nu(l) the product branch proposal. The target
branch law is tilted by T_l=2^(d-h) Z_l. Full row rank gives T_l=1; a dependent
system has T_l=0 or 2^(d-rank), which can be exponentially large. The exact
Gibbs branch law is nu(l) T_l / E_nu T, NOT nu(l).

If all signs b_i are independent uniform and independent of the fixed local
mixture choices, the earlier positive-part argument gives expected output
TV <=min(1,3*epsilon), where epsilon is branch rank-failure probability.
This transfers to these covariant affine filters because their complete branch
rank law is identical. It is still a sign-averaged theorem. For a fixed signed
instance one must control the tilt or prove every proposed branch has full rank.
Strictly positive factors ensure a nonempty target; singular q needs a separate
positivity check. No partition normalization is inferred by this module.

A new exact fixed-sign countercontrol uses r=4, q_y=(63/64)/16+(1/64)*1[y=0]
and the public map A*x=(x,x,x,x) for one outer bit. The point branch has four
equations but rank one; its proposal probability is epsilon=1/64. With b=0,
the target zero probability is79/142 while the rank-failure-zero-fallback sampler
has zero probability65/128. Their TV is441/9088, STRICTLY GREATER than3/64.
Thus the sign-averaged3*epsilon statement is false for this fixed sign. The full
16-sign census obeys the average bound. This is a finite scope counterexample,
not a hard computational instance; exact sampling of one bit is trivial.

In particular, a classical-codeword branch law cannot be substituted into a
coherent quantum input: for q=(3/4,1/4), the half-weight full-frequency USD
branch has probability1/2 on either codeword but1/3 on the normalized sum of
the two codeword states. The DQI reduction keeps its own input and error debt.

## Resource Boundary

For constant local dimension and explicit rational coefficients, extracting the
mixture costs bounded local Fourier arithmetic and produces finitely many
branches; global affine sampling then uses polynomial binary linear algebra.
For growing blocks one needs a polynomial-size listed collection of effects,
efficient character coefficients and efficient sampling of the extracted
branches. Enumeration of all subspaces costs 2^Theta(r^2), so the mere existence
of an LP or mixture is not a polynomial-time classical algorithm. Even a succinct
quantum instrument does not automatically grant those classical coefficients.

The executable verifier is deliberately capped at16 codewords and consumes
explicit exact contribution Grams. It is a conformance and falsification tool,
not a claimed scalable measurement compiler. It checks positive semidefiniteness
by exact Schur pivots, support, covariance, spectral budgets and reconstruction.
The physical POVM tests use independent inverse-square-root formulas only on
strictly positive finite fixtures; the main certificate uses no square roots.

## Attempts To Break The Claim And The Next Decision

- Zero eigenvalues: supported cosets still decompose; forbidden support receives
  zero mass. Singular controls require no limiting numerical inverse.
- Negative overlaps: affine offsets reproduce the signs with positive weights.
- Noncovariant USD: an explicitly physical asymmetric example is rejected by
  the covariance contract. Its twirl preserves the uniform local reward only.
- Minimum-error measurement: an explicit physical two-outcome POVM has nonzero
  wrong-label probability. It fails unambiguity and is not declared dequantized.
- Coherent codeword superpositions: retain the explicit1/2 versus1/3 counterexample.
- Global rank: test all512 binary3x3 maps and16 residual subspaces (8192 cases)
  independently as row and column ranks. No average equation count substitutes.
- Fixed signs: retain the earlier planted-sign failure and normalization debt.

Do not spend the next pass on affine LP sweeps, more parity blocks, or merely
negative overlaps. A useful new receiver must add something genuinely outside
these promises: retained coherent residuals with charged reuse, a minimum-error
collective decoder with full outer error correction, or a succinct growing-block
instrument whose coefficient-access bottleneck is essential and whose quantum
implementation is efficient. These are targets, not evidence of hardness.

Before choosing one, inspect NONLINEAR_FILTER_PINNING and the existing coherent
BPQM work: changing the name of the measurement does not remove a decoder or
normalization obstruction. If no concrete outside-class construction survives,
pivot away from local binary Gibbs decoding rather than adding another baseline.
