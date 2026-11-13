# Native matroid top-spectrum: a complete classical comparator

2026-11-13. REVIEWED WRITTEN application of published theorems; no novelty
claim. The full 145-line independent report
`audits/reviews/2026-11-13-native-input-selection.md` was parent read and
checked against the actual primary texts. No quantum code or paid call.

## Native question and selection

Input is an explicit matrix over Q or an explicitly represented finite field,
with all field and entry bits charged. Its independent column sets define a
matroid. Delete loops by rank tests; n now denotes the remaining ground size
and r the rank. The target is either (a) the full multiplicity-normalized
spectral law of its top reduced simplicial Laplacian, to TV error epsilon,
or (b) its top reduced Betti number divided by the number of bases, to
additive epsilon with failure at most eta. Rank zero returns the single
zero eigenvalue. No basis table, independence oracle, uniform state or
spectral advice is supplied.

This candidate was compared with Boolean Macaulay inversion and the earlier
sparse constant-map route. An implicit polynomial-sparse Laplacian and an
integer positive gap could make quantum filtering avoid the exponentially
large chain matrix. The requested advantage was a polynomial native-input
clock against explicit exponential matrix construction, not a proved
separation. The decisive question is whether the SAME normalized output has
a classical sampler. Corpus been-tried and baselines preceded the source
checks; the absence of a direct catalog entry is not absence of a baseline.

## Algorithm and proof of the same-output classical match

Fix the column order. Find a basis greedily using matrix rank. Use the
Anari-Liu-Oveis Gharan-Vinzant down-up chain: drop a uniformly random basis
element and enumerate all at most n completing elements, choosing uniformly
among those giving a basis. Corollary 1.3 of arXiv:1811.01816 supplies an
all-matroid mixing bound r*log(n^r/delta), with each independence query paid
by native rank computation. Run from the greedy basis for a fixed sufficient
number of steps. No chain-mixing assumption is inferred from finite data.

Given the sampled basis B, repeatedly compute V=cl(B1), initially B1=B,
and remove an internally active b of B1 in the restriction to V. An element
b is internally active precisely when no smaller e in V minus B1 gives
another basis B1-b+e of V. Stop when none is active, then output

    lambda = n - |cl(B1)|.

At most r removals occur. Each step uses at most O(n*r) rank tests, so the
whole deterministic map costs polynomial native BIT time.

Kook-Reiner-Stanton (KRS), Theorem 1, bijects bases with triples (V,B1,B2):
B1 has no internal activity in V; B2 has no external activity in M/V.
Their Corollary 13 and Theorems 14-15 identify orthogonal top-chain summands
E(V) of eigenvalue n-|V| and dimension

    dim E(V)=beta_top(IN(V))*|mu_(M/V)(0,1)|.

The two factors count the respective choices of B1 and B2. Therefore the
number of bases mapped to lambda equals its eigenvalue multiplicity. This
proves that the deterministic pushforward of the uniform basis law is the
normalized top spectrum. Approximate sampling contracts TV under the map.
This is an inference directly from the source decomposition, not a new
spectral theorem or an assertion about individual basis-state measures.

For Betti density alone, KRS's Euler-characteristic identity and shellability
give beta_top=T_M(0,1), while the number of bases is T_M(1,1). Thus one can
instead test whether the sampled original basis has zero internal activity.
Each test uses at most n*r rank queries. Use sampling bias <=epsilon/8 and
O(epsilon^-2 log(1/eta)) independent restarted trajectories; Hoeffding bounds
the remaining additive error. No exact count or relative approximation to
an arbitrarily small density follows.

## Finite clocks and scope

The spectral sampler has a polynomial(n,inputbits,log(1/epsilon)) BIT clock,
including reading the accuracy input. Allocate epsilon/2 to basis mixing
and epsilon/2 to finite random coins. Each draw is uniform from at most n
listed options via binary rejection. If H is the fixed total number of
draws, cap each at ceil(log2(2H/epsilon)) trials. Each trial succeeds with
probability at least 1/2; coupling with exact coins charges the union of cap
failures to TV. On a failure return any legal eigenvalue label in 0,...,n;
the mass is charged even if that fallback has zero exact probability. The
scalar estimator uses the same finite coupling with a separate eta budget,
so every branch has a polynomial clock. It does not condition on global
absence of failures or run an unbounded rejection loop.

The matched law is the spectral law of the MAXIMALLY MIXED TOP-chain state.
No statement is made about an arbitrary specified/coherent input state,
eigenvector preparation, coherent evolution, relative tiny-weight readout,
exact Betti computation, or general simplicial complexes. No quantum
hardness, novelty, speedup, practical implementation, or formal/human
verification claim is made.

## Primary sources and exact falsification control

Actual KRS author PDF:
https://www-users.cse.umn.edu/~stant001/PAPERS/laplacian.pdf .
Read Theorem 1, the internal-activity/Euler paragraphs, Corollary 13,
Theorems 14-15 and Corollary 17. Actual ALOV PDF:
https://arxiv.org/pdf/1811.01816 . Read the transition definition and
Corollary 1.3, including the independence-oracle scope. Retained PDFs,
extracted text and SHA256/URL metadata are in
`audits/sources/matroid_betti_screen/`. No abstract supplies a theorem.

One exact Sage run in `audits/controls/matroid_top_spectrum/` compared the
boundary-transpose-boundary characteristic polynomial with counts from the
actual greedy decomposition. U_2_4 gives multiplicities {0:3,4:3} on six
bases; the graphic K4 matroid gives {0:6,3:4,6:6} on sixteen bases. These
checks test the eigenvalue shift and normalization; the all-input theorem
comes from the source-backed argument above. No sweep or broad suite run.

The independent Macaulay screen supplies a separate operation falsifier:
for equations x_i=1 the grounded Boolean-cube incidence matrix has
sigma_min<=sqrt(n/(2^n-1)), although the original equations are classically
trivial. This repeats the known conditioning issue and earns no new quantum
preconditioner project. A different coordinate projection has success 2^-n;
this is not a no-go for all preconditioners or all Boolean solvers.

## Next action

Do not implement quantum trace filtering for this already matched output or
repeat a paid confirmation review. A new topology proposal must state an
unmatched native output, its preparation and normalization, and an applicable
classical comparator before admission. Independent many-body/tensor screens
are being completed; a missing mechanism is not a hardness claim.
