# Retained Source Labels and Full Walsh Transcripts

Status: derived, review pending. Novelty is NOT established. This is a
restricted information obstruction, not an algorithm, an efficient classical
sampler, or an all-measurement/all-copy no-go theorem.

## Question and Result

The previous corrected-weight calculation discarded source labels after a
phase-dependent bit correction. Keeping them genuinely changes the law. This
pass implements exact paired category/bit histograms, the coarser joint law
of negative-source count m and corrected weight w, and executable decisions
w=m, w<m, w>m. No decision orientation is fitted.

A separate argument now bounds ALL source irrep labels paired with ALL raw
Walsh bits, even for complex common central unitary phases:

    T <= min(1, sqrt((2^k-1)/(4M)),
             2k sqrt(r/M) + D min(1,1/2+3/sqrt(L))^k),
    D=n!, M=(n-1)!!, L=n(n-1)/2, even n>=8.

Here r is the number of retained irrep categories. For every irrep retained,
use r=p(n)<=2^(n-1). The category count DOES NOT enter the remainder radius.
At S1024, k=17528, exact outward dyadic rounding gives T<=2^-1663 with ALL
irrep labels. At S4096, k=86488, it gives T<=2^-8745. These are upper bounds
on distinguishability, not measured exponentially tiny probabilities.

For polynomial k>=(1+epsilon)log2(D), fixed epsilon>0, the bound is
superpolynomially small. The raw-copy bound separately covers
k<=(1-epsilon)log2(M). The INTERMEDIATE WINDOW IS NOT CLOSED. k means the
number of participating mask positions, not the available copy budget: an
algorithm can ignore additional copies and operate in that window.

## Exact Scope

- G=S_n, n even, and the uniform fixed-point-free involution class C of size M.
- Standard mixed coset inputs: rho_0=I/D and rho_h=(I+R_h)/D, with the SAME
  hidden h in every copy. Average h only after forming joint probabilities.
- Measure source irrep labels, or a common partition of irreps, keeping their
  complete unconditioned natural distribution.
- Choose a COMMON central unitary U=sum_lambda phi_lambda P_lambda before
  observing sources, |phi_lambda|=1. The irrep partition is also fixed before
  sources and is the same at every position.
- Uniform coherent control of every subset S, INCLUDING the empty mask,
  applies U_S=sum_g a_g tensor_i R_g^(1[i in S]). This includes the correct
  empty-mask scalar; it is not silently replaced by an unrelated identity.
- Walsh-measure every control bit, retain every paired category label and
  bit, and discard all physical inputs. Any classical processing of that
  transcript is covered. Category-known bit flips do not change its distance.

The common central unitary may have complex phases. For RAW Walsh readout,
the phase need not be constant inside a category. A matching reflection
correction requires the category to determine the sign; all irrep labels do.
The finite sign-category evaluator implements the negative-character
reflection. It is a specialization, not a restriction of the new theorem.

Multiple queries, nonuniform masks, phases selected from the observed source
tuple, noncentral operations, retained physical inputs, and coherent final
selector measurements are NOT covered. Nor does the bound certify a natural
graph/code reduction to this precise binary promise.

## Paired Outcome Law

For category j let its central projector have real S_n coefficients

    p_j(g) = (1/D) sum_(lambda in j) d_lambda chi_lambda(g),
    q_j=p_j(e),  sum_j q_j=1,  sum_g p_j(g)^2=q_j.

Write U=sum_g a_g R_g. Centrality and unitarity give

    sum_g |a_g|^2=1,  sum_g conjugate(a_g) a_(hg)=0  (h!=e).

Set p_j0(g)=p_j(g), p_jh(g)=p_j(g)+p_j(hg), and q_jeta=p_jeta(e).
Each q_jeta is a nonnegative natural source probability, including zeros.
Tracing the local controlled group action gives the RAW bit factor

    L_(j,z,eta)(u,v) = [q_jeta + p_jeta(u^-1 v)
       + (-1)^z (p_jeta(u^-1)+p_jeta(v))]/4.

The full paired transcript law is

    P_eta((j_1,z_1),...,(j_k,z_k))
      = sum_(u,v) conjugate(a_u) a_v product_i L_(j_i,z_i,eta)(u,v).

For known source bit flips, multiply the last parenthesis by the declared
category sign. Joint histograms of the 2r paired outcomes are sufficient by
exchangeability; (m,w) alone generally is NOT sufficient. Individual factors
and pair weights can be signed. This expression is not a classical sampler.

## Positive Coset-Diagonal Comparison

Let H_0={e}, H_h={e,h}. Restrict the sum to u^-1 v in H_eta. Define the
normalized positive categorical probability vector

    F_(eta,g)(j,z) = [q_jeta + (-1)^z p_jeta(g)]/2.

Positivity follows because p_jeta is a positive-definite functional:
|p_jeta(g)|<=q_jeta. Its components sum to one. The retained diagonal is

    Q_0 = sum_g |a_g|^2 F_(0,g)^tensor k,
    Q_h = (1/2) sum_g |a_g+a_(hg)|^2 F_(h,g)^tensor k.

Both are positive normalized mixtures. For the second equality, pair g and
hg; centrality gives a_(gh)=a_(hg) and F_(h,hg)=F_(h,g). Complex interference
is retained through Re(conjugate(a_g)a_(hg)). Q is generally NOT P for small
k. The off-coset remainder must be paid in full.

## Mixed Overlap Bounds the Mixture Separation

For f(g)=|a_g|^2 define

    B_j(h)=sum_g f(g) p_j(hg)^2.

It is nonnegative and constant on each conjugacy class, and
sum_h B_j(h)=q_j. Hence B_j(h)<=q_j/M for h in C. Likewise
|p_j(h)|<=sqrt(q_j/M), by class invariance and projector normalization.
Cauchy-Schwarz and the substitution g -> hg give

    S_j=sum_g |a_g|^2 |p_j(hg)| <= sqrt(q_j/M),
    R_j=sum_g |a_g a_(hg) p_j(g)| <= sqrt(q_j/M).

For any event E of the entire paired transcript, use
TV(F^tensor k,G^tensor k)<=k TV(F,G). Expand

    Q_h-Q_0 = sum_g Re(conjugate(a_g)a_(hg)) F_(h,g)^tensor k
             + sum_g |a_g|^2 [F_(h,g)^tensor k-F_(0,g)^tensor k].

The cross coefficient sums to zero. Subtract the valid reference product
R_h^tensor k, where R_h(j,z)=q_jh/2, from its first term.

- TV(F_(h,g),R_h)<=sum_j |p_j(g)+p_j(hg)|/2. The cross contribution is at
  most k sum_j R_j, using the h-translation symmetry of |a_g a_(hg)|.
- TV(F_(h,g),F_(0,g))<=sum_j (|p_j(h)|+|p_j(hg)|)/2. Its contribution is
  at most (k/2) sum_j (|p_j(h)|+S_j).

Taking the supremum over E gives

    TV(Q_0,Q_h) <= 2k sum_j sqrt(q_j/M) <= 2k sqrt(r/M).

No interpolation through negative probabilities, conditioning on rare source
labels, or efficient access to the mixture is used.

## Column Orthogonality Removes the Category-Count Penalty

For any nonidentity g, character column orthogonality and Cauchy-Schwarz give

    sum_j |p_j(g)| <= (1/D) sum_lambda d_lambda |chi_lambda(g)|
                   <= 1/sqrt(|class(g)|).

This bounds every partition of the irreps at once, including singleton
categories. Bounding each projector separately would introduce an unnecessary
sqrt(r) factor and lose the full-source conclusion.

For an off-coset pair u^-1 v not in H_eta:

- If u,v are both outside H_eta, start with the nonnegative q_jeta/4 term.
  Its sum over (j,z) is 1/2. Each of the three remaining projector sums has
  magnitude at most 2/sqrt(L) in the alternative, at most 1/sqrt(L) in the
  null. Triangle inequality yields sum_(j,z)|L|<=1/2+3/sqrt(L).
- If one endpoint is in H_eta, the other cannot be. One bit per category has
  zero factor, the other equals (q_jeta+p_jeta(v))/2 up to translation and
  known bit flips. It is nonnegative and sums to exactly 1/2.
- Always sum_(j,z)|L(u,v)|<=1: each local outcome kernel is a positive Gram
  kernel, so sum |L(u,v)|<=sqrt(sum L(u,u) sum L(v,v))=1.

Thus rho=min(1,1/2+3/sqrt(L)) bounds every off-coset paired-outcome l1 radius.
Since (sum_g |a_g|)^2<=D,

    TV(P_eta,Q_eta) <= (D/2) rho^k.

Two such errors plus the mixture distance prove the displayed theorem. The
hidden-class invariance of the complete law permits working with one h; it
does not permit independent h per copy or averaging factors before products.

### Elementary Minimum Class Size

For even n>=8 every nonidentity conjugacy class has size at least C(n,2).
If its moved support s lies in [2,n-2], choosing the support already gives
C(n,s)>=C(n,2). On s moved points with r cycles, no cycle has length one and

    centralizer <= 2^(s-r) r!,  r<=floor(s/2),

using j<=2^(j-1) and product_j m_j!<=r!. The displayed bound is nondecreasing
in r>=1. For s=n=2m it is at most 2^m m!, giving class size at least M.
For s=n-1 it is at most 2^m(m-1)!, giving at least mM. Finally M>=C(n,2)
for even n>=6 by induction. The code conservatively requires n>=8.

Since irreps correspond to integer partitions and partitions are a subset
of compositions, p(n)<=2^(n-1). This crude bound already suffices: log M is
Theta(n log n), whereas log r=O(n). No partition enumeration is needed for
the asymptotic contract. Outward rounding uses integer square roots and exact
integer powers, not floating-point underflow.

## Finite Falsification Results

Negative-character reflection at S6; total variation distances:

| Copies | Corrected Weight | Source Count Only | Full Paired Category/Bit | Full Disjoint-Pair Score |
| --- | --- | --- | --- | --- |
| 2 | 0.028889 | 0.136944 | 0.142396 | 0.176528 |
| 4 | 0.055828 | 0.162830 | 0.203076 | 0.257217 |
| 8 | 0.094424 | 0.237168 | 0.283812 | 0.365879 |

The paired histogram at 4 and 8 copies beats the older COARSE pair-event
count baseline but loses to the full pair likelihood. The latter has a
polynomial arithmetic decoder on observed pair labels; its quantum pair
front end is NOT classically replaced. This pass extends its finite exact
law evaluator to S6 through eight copies. Missing larger-copy full-score
comparisons are explicitly null, not silently assigned a weak baseline.

The ideal paired histogram is also not a compiled classifier: this evaluator
enumerates D^2 group pairs. Keeping a polynomial number of summary statistics
does not make their optimal likelihood table efficiently computable in n.
Declared comparisons w=m, w<m and w>m are executable without a fitted table;
none establishes scalable advantage. Source-only information is charged.

## Verification and Attempts to Break the Argument

- Exact signed category laws retain natural mass and pass independent
  category-prior and corrected-weight marginal checks.
- 36 separately matrix-derived histogram laws agree through S4; 40 exact
  coset-diagonal mixture laws include S6. The full-source column envelope is
  checked at all 750 elements of S3/S4/S6.
- 72 additional raw histogram/mixture laws include complex phases and
  categories whose irreps have different phases. These are floating-point
  consistency checks, not a proof for arbitrary complex phases.
- 1512 nonidentity cycle types at even degrees 8 through 20 satisfy the
  elementary minimum-class-size bound.
- Tests exercise every S4 k=3 histogram against the actual source-count
  decoder, opposite accepting orientations, zero source masses, nonexact
  small-k mixtures, access-scope exclusions and dyadic rounding.

The first validation exposed baseline fields inserted in the wrong function;
this was fixed before registry publication. A proposed zero-source-mass S4
test had a false premise: the double-transposition class has no such irrep.
The test now uses S3's transposition class, where the sign source has zero
alternative mass. These corrections are not evidence against the theorem,
but are reasons to require independent review rather than trust green tests.

Remaining attack points: audit the exact controlled-unitary convention, the
complex diagonal reduction, the event-norm constants and the common-source
partition assumption. Check whether known work already implies this
restricted obstruction. The tests do NOT provide independent mathematical
review. No theorem-prover certificate or natural-problem consequence is
claimed. Existing joint-coset lower bounds and measured-sieve no-go results
provide context, not a certification of this different access contract:
[Hallgren, Roetteler and Sen](https://arxiv.org/abs/quant-ph/0511148),
[Moore, Russell and Sniady](https://arxiv.org/abs/quant-ph/0612089).

## Next Research Decision

Do not keep adding source-derived scalar features in the already obstructed
large-copy regime. The best next falsification target is the INTERMEDIATE
copy window with growing degree. A simultaneous C(h)-conjugation orbit
contraction can reduce the finite cost while preserving the shared hidden
member; first reproduce full S6 sums exactly, then attempt S8. It remains a
finite verifier, not an efficient quantum or classical algorithm.

Alternative changes must leave an actual hypothesis of the bound: a
source-adaptive common phase, multiple coherent subset queries, or a final
measurement other than Walsh followed by classical processing. Each needs
its own normalized joint law and baseline, not just a declaration that a
no-go theorem no longer applies.

Run `python qsearch.py coset-binary-carrier-instruments`, then refresh
`dequantize`, `proofs`, `conjectures`, `mutate`, and `validate` through qsearch.
Refresh the website artifact with `python tools/build_progress_snapshot.py`.
The existing experiment and candidate are reused; this is not a candidate
promotion or an increase in the number of supposedly promising algorithms.

Current validation: 169 targeted research tests passed in 49.74 seconds;
the 18 new focused tests passed in 4.18 seconds. The old character-decoder
registry-write omission was fixed and all eight of its tests passed. Its
live default workflow completed 128 attempts without a polynomial-style
decoder success. The full-suite run progressed beyond that failure, then
stopped after 65 passes in 216.35 seconds at the separate missing scaling
write in `test_character_moment_obstruction.py:73`. It is NOT all-green.
All core/theorem/test Python syntax, site JS syntax and diff checks passed.

The next orbit-contraction feasibility check found 8, 34 and 182
C(h)-conjugation orbits on S4, S6 and S8, respectively. Enumerating one first
endpoint per orbit and every second endpoint uses 192, 24480 and 7338240
weighted pairs, versus 576, 518400 and 1625702400 full pairs. Orbits were
generated using within-pair swaps and adjacent-pair interchanges, without
enumerating the centralizer. These counts are not yet a verified probability
contraction or a new quantum algorithm.
