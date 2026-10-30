# Simon DCP: October Revision Does Not Change The Decoder

2026-10-30. Version-scoped source audit and mathematical checks. Six focused
agents contributed source-history, theorem-scope, postselection, Lemma 3,
constructive-DCP and alternative-direction reviews. This is automated
research review, not human peer review, a new quantum algorithm, or a fresh
Lean verification of either external paper.

## Decision

Do not reopen this decoder on the strength of its October response. Its
actual operations are unchanged from the August version. The published
label-information theorem still applies through an explicit simulation of
those operations. Adaptive selection of zero-Hadamard groups does not
remove the information bound when the whole instrument, including failures,
is retained. This conclusion does NOT rule out a different DCP algorithm.

This pass fills a provenance gap: the September repository audit did not
read the October revision, and its generic digest tests did not independently
implement Simon's full asymptotic circuit. Neither fact should be rewritten.

## Sources And Exact Delta

Daniel R. Simon, *A Polynomial-Time Quantum Algorithm for the Dihedral
Coset Problem*, ePrint 2026/1591, CC BY 4.0. Official archived versions:

- [August 11 archive](https://eprint.iacr.org/archive/2026/1591/20260811:220210),
  [PDF](https://eprint.iacr.org/archive/2026/1591/1786485730.pdf), 16 pages.
  Local `literature_cache/eprint_2026_1591_20260811.pdf` SHA256:
  `e84834fb205d00e87facbcee67310b17251b496e3547874d239d8fe679efbaec`.
- [October 8 archive](https://eprint.iacr.org/archive/2026/1591/20261008:003009),
  internal document date October 7, 18 pages. Retrieved from the official
  current PDF on October 30, not inferred from its abstract.
  Local `literature_cache/eprint_2026_1591_20261008.pdf` SHA256:
  `5e827802a7cd2351ce8561f4fbd55b44df2c79aae12fa6b176bcd85eda6714ed`.

The source text from `In Step 1` to immediately before `Lemma 3.` is
identical after deleting whitespace and page-number-only lines: 7,837
characters, SHA256
`9345666fdb53203f2693dbcbfc4b527fb5c486827fe6e126d078f9d7b39ee8ea`.
This includes Steps 1-7 and Lemmas 1-2. The concluding Hadamard readout is
also unchanged. The new material alters Lemma 3's justification and some
exponent bookkeeping, and adds Section 3's postselection response. It adds
no full-label-dependent operation. Relevant mathematical pages were read
in text and the response/lemma pages were also visually inspected.

The applicable primary result is Gupte, Ragavan and Zhandry,
[*A Fourier-Label Information-Loss Barrier for Dihedral Coset Algorithms*,
arXiv:2609.40062v1](https://arxiv.org/html/2609.40062v1), Theorem 2.1 and
Sections 2.4/4.2. Its stated target is the August version. The transfer to
October below uses the verified operational equality, not an assumption
that an old refutation automatically covers every revision.

## Transfer Certificate

Write N=2^n, m=kn^(c+1), w=c*log2(n), and r=log2(n), with integral block
parameters as in the manuscript. Constants k,c are fixed. Work first with
ideal DCP inputs, a case covered by its at-least clean-source promise.

1. Move measurement of the Fourier labels Y immediately after the initial
   Fourier transforms. All intervening operations control on Y in its
   computational basis; they do not mix it. Conditional source-position
   phases are global. The resulting labels are independent and uniform.
2. Compute the complete subset sum with FULL labels and measure its low
   n-1 bits EXACTLY. Keep the measured z with its Born probability. Do not
   approximate this operation or normalize and uniformly average branches.
3. Only the next group-summary computation uses numerical label values.
   Subsequent group selection depends on measured D, not a new query to Y.
   Permuting a subsequently unused Y register is not a useful new access.
   Analytical symbols for subset-sum fibers are not extra circuit queries.
4. Round each label down to its top n-ell bits, ell=floor(2n/3). For each
   fixed nonempty block string, the exact block sum is uniform modulo N.
   Rounding changes its integer sum by less than w*2^ell. A changed r-bit
   summary requires a bucket-boundary crossing, of probability at most
   w*2^(r+ell-n), capped at one. Modular wrap is another such boundary.
5. Union over all block strings and blocks. With bad-label probability

       delta <= min(1, m*2^(w+r+ell-n)),

   the entire summary table fails to agree somewhere. Outside that event
   the whole coherent computation agrees, not just the selected entries.
   Thus later adaptive selection is already covered. The averaged states
   differ by at most delta for either secret, with all later branches kept.
6. In the rounded implementation, discard unused full labels and retain
   only their fixed coordinatewise digests. The primary digest theorem
   bounds parity trace distance by m*2^(-ell/2). Data processing therefore
   gives the complete one-run distribution, including restart, the bound

       TV(P_0,P_1) <= Delta
          := min(1, m*2^(-ell/2) + 2*m*2^(w+r+ell-n))
           = poly(n)*2^(-n/3).

Here T(rho,sigma)=||rho-sigma||_1/2. Equal-prior guessing advantage is half
the trace distance, not the trace distance itself. The polynomial factor
can make this estimate vacuous at small n; no finite-size practical attack
or concrete cryptosystem parameter claim follows.

The theorem concerns a label-averaged classical-quantum ensemble after
specified information has become inaccessible. It does not claim that
each pure state at a fixed full Y is close to its dephasing. Computational
dephasing retains the b register; literal deletion of b is a different map.
Use the precise theorem rather than Section 3's shorthand about tracing.

## Why Adaptive Postselection Does Not Repair It

Let rho_0,rho_1 have trace distance at most epsilon. Represent the complete
adaptive algorithm by a quantum instrument {E_t}, where t records its
transcript, selected A, and abort/accept flag. The maps may depend on earlier
outcomes, but their sum is trace preserving. Then

    (1/2) sum_t ||E_t(rho_0)-E_t(rho_1)||_1 <= epsilon.       (1)

This is one global budget, not epsilon independently available to each
possible A. Coarse-graining or conditionally processing transcripts is a
further channel. Exponentially many possible transcripts do not multiply
the budget of the actual instrument.

For an accepted event, retain its transcript and call the two unnormalized
accepted states X,Y, with p=Tr X and q=Tr Y. Merge every rejected outcome
into one orthogonal abort symbol. Contractivity gives

    (||X-Y||_1 + |p-q|)/2 <= epsilon.                       (2)

For positive p,q, normalization and triangle inequality imply

    max(p,q) * T(X/p,Y/q) <= epsilon.                      (3)

For example, when p>=q, multiply the normalized difference by p and bound
||X-(p/q)Y||_1 by ||X-Y||_1+p-q. Equation (2) completes the proof; exchange
the states otherwise. The independent reviewer strengthened the parent's
initial valid but weaker min(p,q) bound to this sharp form.
When p=q, conditional guessing advantage is at most epsilon/(2p).
For unequal acceptance, conditioning also changes the secret prior:
it becomes p/(p+q), not 1/2. Reporting conditional correctness without
acceptance and priors can report information that came from selection.

Perfect decoding on an exponentially rare event is entirely compatible
with (1). The valid rare-event observation does not imply that selecting
A after seeing D creates a high-success decoder. Such selection changes
the transcript law and belongs inside the same instrument (1). Likewise,
small unconditional disturbance from dephasing B cannot be used as a small
conditional disturbance after imposing an exponentially rare A event
without the factor in (3).

Two scope checks are essential. First, the comparison must include every
label register accessible to the continuation. With uniform classical y,
the states Z^y|+> and I/2 have identical averages when y is discarded, but
distance 1/2 with y retained; a controlled Z^y extracts that difference
without rare conditioning. Second, (1) needs a common pair of states.
Comparing a state separately to many different A-dependent dephasings and
splicing their selected branches need not preserve any common small
budget. Here the actual/rounded channel transfer and the fixed-digest
theorem supply the common comparison before the adaptive instrument.

For R fresh repetitions, including retries and later postprocessing,
output distance is at most R*Delta. For a stopping rule tau, truncation at
R adds at most Pr_0[tau>R]+Pr_1[tau>R]. A polynomial expected runtime and
inverse-polynomial advantage contradict the exponentially small bound by
choosing a sufficiently large polynomial cutoff and using Markov's
inequality. One cannot count only successful runs.

## A Direct Born-Weighted Rounding Check

There is also a simpler, weaker comparison that avoids enumerating every
block string. This is a local derivation/check of the simulation argument,
not a novelty claim or a replacement for the published theorem.

Retain k bits of each label, where r<=k<=n. For a fixed Y, let eta_Y be
the fraction of Boolean strings on which at least one group summary
changes. Before the low-sum measurement the b amplitudes have equal
magnitude. The exact and rounded summary isometries retain b, so their
pure-state overlap is exactly 1-eta_Y. Both can be computed before the
low-sum measurement, since they commute with its diagonal projectors.
Their trace distance, before any subsequent processing, is

    sqrt(2*eta_Y-eta_Y^2) <= sqrt(2*eta_Y).

Average the same bucket-crossing bound over b and then Y. For disjoint
blocks totaling m samples,

    E_Y eta_Y <= min(1, m*2^(r-k)).

Jensen's inequality, the exact low-sum measurement, and later channels give
an averaged simulation error at most min(1,sqrt(2*m*2^(r-k))). Together
with the digest theorem the complete output distance is bounded by

    min(1, m*2^((k-n)/2) + 2*sqrt(2*m*2^(r-k))).           (4)

Taking k=ceil(n/2), r=O(log n), m=poly(n) yields poly(n)*2^(-n/4).
Unlike the uniform-table argument, this check does not pay 2^w. It still
requires fixed blocks, the stated flat premeasurement source, exact
prefix, rounding-only label use, no retained useful low-label workspace,
and full Born weighting. It is not a uniform conditional-on-Y or
conditional-on-acceptance guarantee, nor a general low-precision theorem.

## The Revised Lemma 3 Still Needs A Different Moment Argument

An independent reviewer checked the actual new pages 11-12 without relying
on the older repair notes. Fixing original-order Y and varying D changes
which groups enter A, hence which fibers the fixed summary transcript
describes. Fixing the relabeled coordinates instead enforces D_A=0.
Distinct compatible paths sharing their B string then have identical
phases, not pairwise-independent signs. Randomizing Y in the subsequent
paragraph does not establish the missing selection-conditioned moments.

For fixed selected first-a groups and unrestricted uniform D_B, if m_v
counts A-completions of B-string v, the correct Walsh identity is

    E_D [sum_v m_v*(-1)^(v dot D_B)]^2 = sum_v m_v^2.

It is completion-collision energy, not sum_v m_v. For other selection
patterns, skipped groups before the a-th zero are constrained nonzero;
a nontrivial character on a width-w skipped group has conditional mean
-1/(2^w-1), not zero. A later unconditioned group has mean zero.

An exact calibration uses n=16, five width-4 groups, four selected groups,
Y=(1,...,20), and z'=22. These are reduced parameters, NOT the theorem's
sample schedule. All top-four-bit summaries and the carry guard are zero.
Take D=(0,0,0,0,u) in group notation. The paths with one-based supports
{1,4,17} and {2,3,17} have z*=5 and the same B string. Their joint signs
over uniform u have (++,+-,-+,--) counts (8,0,0,8), not (4,4,4,4).
The nonzero completion multiplicities for total sum 22 are (79,3,2,2,1).
Consequently the sum of squared signed branch counts is 100144, whereas
16 times the number of paths is 1392. Every such D branch has positive
Born mass; zero-probability events and the zero subset-sum exception are
not responsible for this discrepancy.

The general equal-phase identity persists upon zero-padding paths into
larger blocks. The finite probabilities above are not an asymptotic
failure bound. This witness rejects the claimed independence/normalization
step; the algorithm-level conclusion comes from the separate information
argument. Also, the revised printed Lemma 3 states a 2^n threshold while
its proof and later use employ 2^(n/2). Fixing that typo alone is not a
repair of the conditional moments.

## Constructive Disposition

The DCP reviewer found the already documented full-label Walsh feedforward
route still information-theoretically viable, but with no efficient sign
evaluator. Quantum counting remains exponential; an efficient classical
chosen-query evaluator must face the existing classical witness extractor.
Do not promote ideal signed-count tables to an algorithm.

The independent pivot review proposed inelastic scalar-field scattering
using existing dressing, simulation and detector algorithms. It is a
different native application, but supplied neither a new algorithmic
mechanism nor a parameter family with a proved preparation gap and
nontrivial output distribution beyond strong classical truncation methods.
It is therefore not automatically elevated above the open arithmetic
tasks. More simulation infrastructure is not the missing theorem.

Re-entry for this particular DCP line requires a changed physical
operation that breaks the simulation above, or a precise error in its
premises/proof. A rewritten analysis of the identical decoder is not such
a change. Independent low-label-sensitive operations might evade the
bound; mere sensitivity or failure of this filter does not prove speedup.

## Verification Boundary

`tests/test_dcp_revision_postselection.py` pins both source hashes and the
unchanged operational text. Its bounded controls check bucket crossings,
the actual summary-isometry overlap, the exact low-sum measurement, a
first-zero adaptive instrument on existing physical DCP density counts,
rare-event success costs, unequal acceptance priors, and the difference
between averaged and labelwise claims. They do not simulate the paper at
its enormous asymptotic sample schedule or prove the general theorem by
finite enumeration. No production solver, candidate, registry promotion,
CLI or UI implementation is introduced.

Verified: 168 selected tests passed in 37.40 seconds under `-W error`,
including the initial 28 tests in the new file. Selection: the revision controls,
label digest, arbitrary-measurement witness reduction, approximate erasure,
disjoint kernel pairing, registry I/O and CLI parser tests. This is not
the whole repository suite. Python compilation, all 12 site JavaScript
syntax checks, `git diff --check`, and `python qsearch.py validate` passed;
validation returned `valid: true` and no issues.

After independent postselection review, the final control file was extended
to 30 tests and the acceptance bound strengthened from min(p,q) to max(p,q).
All 30 final tests passed in 0.92 seconds under the same strict settings;
Python syntax, registry validation and diff checks were replayed. All six
agents completed and were closed. No inference relies on an untested
last-minute change.

The 13 registry JSON files retain aggregate SHA256
`79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd`
(sorted filenames followed by their bytes). The existing approximate-
erasure integration test also replayed its real report twice during the
two combined runs, appending history runs 00598/00599 and refreshing its
trend/report timestamps. Those unchanged-metric replays are NOT new
scientific evidence or progress. No Git commit or push was performed.
