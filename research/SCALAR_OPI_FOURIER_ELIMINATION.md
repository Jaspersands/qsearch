# Scalar OPI through exact weighted-parity elimination

5 November 2026. Classical falsifier on the original full-table input.
Known Algorithm H, not a new quantum mechanism or a separation claim.

## Question, model and prior work

Can a polynomial-time classical algorithm match the known DQI approximation
score on scalar OPI with complete explicit random accepted sets? The input
is exactly that of `SCALAR_OPI_NATIVE_PRIORITY.md`: q=2^t, m=q-1 nonzero
field points, degree<k, independently uniform q/2-element accepted sets,
and the explicit field basis. Output native polynomial coefficients and
verify every evaluation. No planted secret, compact predicate, folded
oracle, free QRAM, or changed source distribution is supplied.

The corpus been-tried and baselines lookups preceded implementation in the
interrupted October pass; the been-tried lookup was repeated on 5 November.
No matching retained implementation was found. This is not novelty evidence.
The primary mathematical method is already in
[Crowston et al., arXiv:1104.1135v3, Section 2](https://arxiv.org/pdf/1104.1135):
Remark 2 identifies Fourier polynomials with weighted parity excess;
Reduction Rule 1 combines equal supports with their signs; Algorithm H
eliminates a pivot by imposing a selected parity equation. We run that
operation to exhaustion, choosing a largest absolute current coefficient.
The source's general excess results do not establish the native DQI score.

The quantum comparator remains published balanced DQI, with all table
loading, reversible RS decoding and precision costs paid as in the priority
note. At fixed rate R its ideal mean tends to
1/2+sqrt((R/2)(1-R/2)). The classical baseline is Prange, and published
systematic-basis line search/annealing is stronger than the small Prange
control. The present experiment is not a matched runtime comparison against
either quantum circuits or the published long classical runs.

## Exact operation and cost

Write the coefficient bits as z in F2^N, N=kt. Let E_i be the binary matrix
of monomial evaluation at a_i in the supplied field basis. For table
indicator h_i define its unnormalized integer Walsh transform

    c_i(u) = sum_y h_i(y) (-1)^(u.y).
    q F(z) = sum_(i,u) c_i(u) (-1)^((E_i^T u).z),

where F counts satisfied native coordinates. Aggregate signed coefficients
of equal masks. There are at most mq terms before aggregation. On an
affine section z=z0+Bv, replace each mask a by B^T a and multiply its
coefficient by (-1)^(a.z0), retaining every collision, including those
between different evaluation rows. The constant term divided by q is the
EXACT uniform-section mean.

Select a nonzero current mask a with maximum absolute coefficient C_a;
impose a.v=b with (-1)^b C_a positive. Substitute its least significant
pivot bit into every term and sum signed collisions. The constant term
increases by exactly |C_a|. Each step removes one free bit, hence at most N
steps occur. On termination the total score is constant on the remaining
section. Set free bits to zero, back-substitute and verify the polynomial.
For every such full-table input the output score is at least m/2. No
stronger all-input or distributional approximation guarantee is proved.

The Walsh transforms take O(mqt) integer additions. The elimination takes
O(Nmq) dictionary visits, each with O(N)-bit masks and polynomial-time
integer arithmetic. Coefficient absolute sums never increase under signed
merging and are initially at most mq^2, so O(log(mq^2))-bit coefficients
suffice. Field arithmetic, construction of evaluation transposes, and
native verification are polynomial in the explicit input length. This is
not polynomial in log q for succinct inputs. The implementation also
charges its original field/basis preprocessing; no 2^N objective table is
constructed except in the separately labelled four-bit control.

## An early-stage restriction, not a full-algorithm bound

Let V_i=im(E_i^T). Evaluation surjectivity at any <=k RS coordinates implies
that any <=k distinct V_i form a direct sum. Suppose the accumulated
restriction space has the form S=direct_sum_(i in T) S_i with S_i<=V_i,
and r=|T|. If r<=k-2, the images of any two different row spaces modulo S
have no common nonzero vector: a putative collision would be a relation
on at most r+2<=k rows, and directness forces both vectors into S. Thus
until this regime ends, each nonzero frequency still has a unique row
owner and each new restriction preserves the stated direct-sum form.

If r<=k-1, every untouched E_j remains surjective on the section: its dual
intersection with S is zero. Its table mean is exactly 1/2, even when T
and the restrictions were chosen adaptively using all tables. Therefore
the current section mean is at most m/2+r/2. This is a deterministic
identity about uniform averaging of a fixed section, not an independence
assumption about the adaptive choices. It does NOT bound the completed
algorithm after cross-row aliases can form. Greedy restriction need not
finish one row before touching another.

## Precommitted six-case probe

`classical_baselines/scalar_opi_fourier_elimination.py` reuses the exact six
saved tables and field moduli in `scalar_opi_fft_probe.json`; no rerolls,
parameter tuning or new random cases. Integer arithmetic, signed merging,
the trajectory, work counters and native coefficients are retained in
`scalar_opi_fourier_elimination.json`.

| q | k | Seed | Algorithm H | Prange32 best | DQI mean lower bound |
|---|---|---|---|---|---|
| 16 | 4 | 3101 | 13 | 13 | 9.436 |
| 16 | 4 | 3102 | 14 | 13 | 9.436 |
| 64 | 16 | 3101 | 57 | 45 | 47.326 |
| 64 | 16 | 3102 | 56 | 45 | 47.326 |
| 256 | 64 | 3101 | 206 | 171 | 203.636 |
| 256 | 64 | 3102 | 203 | 172 | 203.636 |

The q256 pair straddles a LOWER bound on the mean of the retained rational
DQI filter. Exceeding that lower bound is not proof of exceeding its exact
mean, or the optimal DQI mean over all filters.
The run therefore admits a serious finite classical competitor but proves
neither an asymptotic match nor an advantage. Independent review found no
invalidating error; see `audits/reviews/2026-11-05-scalar-opi-algorithm-h-review.md`.
The separate Sage checker imported no Algorithm H code: all six native
witnesses (666 evaluations), all 1244 saved parity/gain identities, and 56
exact section means passed. Means were computed from native affine images,
using 4296 row-image enumerations. Every q16 step and the preselected
q64/q256 checkpoints were covered; this was not an independent check of
every individual selected Fourier coefficient. Source hashes are saved in
`classical_baselines/scalar_opi_fourier_sage_check.json`.

Internal exact controls covered all 16 assignments and all 307 affine
sections of a degree<2/F4 instance, 1530 signed restriction transitions,
352 negative-weight cases, and constructive/destructive aliases between
different native rows. They verify the algebraic operation, not scaling.

## Mechanistic diagnosis on the same cases

Replaying the saved constraints with separate row contributions shows the
first nonzero cross-row SUPPORT aliases at steps479/485 of512 for q256.
The first selected multiple-row coefficient occurs at steps490/488. The
total gains on selected single-row frequencies are61.3828125/61.625, and
on multiple-row frequencies17.1171875/13.875, respectively. This diagnostic
is `scalar_opi_fourier_provenance.py/json`, uses the original Fourier lift,
and is not independent correctness evidence. Support collisions are not
the same as intersections of the full row spaces. A selected single-row
frequency after earlier aliases need not satisfy the early lemma.

Sage's native affine images identify the useful finite mechanism. At step256,
51/48 rows are already identically accepted on rank-4 images. At step504,
the fully accepted row rank histograms are {4:110,3:6} and {4:113,3:4}.
Thus large accepted affine flats supply much of the preterminal gain on
these instances. Their dimension4 is a substantial fraction of t=8. The
old random-flat counting restriction is relevant asymptotically, but its
full-row-rank prefix certificate does not upper-bound this adaptive attack.

Another tempting shortcut is false: the maximum INITIAL Walsh coefficient
does not bound later selected coefficients. For any one balanced indicator,
favorable-parity elimination ends with the indicator identically1 after
at most t steps (the terminal constant is Boolean and its mean has risen
from1/2). Its total numerator gain is q/2, so some step gains at least
q/(2t), even when all initial coefficients are O(sqrt(q log q)). This
single-table argument refutes that proposed bound, not the full OPI attack.

An explicit low-spectrum family makes the warning deterministic: t=2s+1,
q=2^t, h(x,y)=1[x+sum_j y_(2j-1)y_(2j)=0]. It is balanced, and factoring
its Walsh sum into two-bit quadratic sums gives every nonconstant
coefficient in {0,+2^s,-2^s}. The same terminal argument forces a later
coefficient >=q/(2t). No performance conclusion about random RS tables
follows. Independent review supplied and checked this counterexample.

## Obligations and cheapest next falsifier

The live question is the score law of this SPECIFIED algorithm for growing
q at fixed R, including adaptive signed collisions. Analyze the retained
gain trajectory and the onset of cross-row collisions before commissioning
any larger sweep. A valid asymptotic claim needs a source-correct bound on
those adaptive operations and a paid runtime/quality comparison. An early
no-alias bound alone cannot establish a final Prange ceiling.

Keep false: novelty, quantum speedup, classical hardness, asymptotic DQI
match, matched runtime advantage, and any statement that finite success
or failure settles the native question. No registry or manuscript promotion.

### Predeclared next-size test (before execution)

The rank-4 diagnostic justifies ONE q512,k128,seed3101 case, retaining the
original IID half-set generator, nonzero field points, greedy tie rule,
and Prange32 comparator. This tests the finite persistence hypothesis:
the unchanged method still reaches the rational-filter DQI mean lower
bound at the next field size. Failing it stops a claim of persistence on
this sequence; succeeding still proves no asymptotic match. No tuning,
extra seeds or replacements. Save all tables and the field modulus before
running; retain the complete trajectory and verify the native witness
independently with Sage. Core cost is <=1152*512*511 dictionary visits plus
selection and field preprocessing; no matched runtime claim. Analyze
accepted-image ranks at checkpoints if the score changes materially.

### Next-size result

The one unchanged-algorithm q512 case returned396/511; Prange32 returned347.
The rational filter's certified mean enclosure rounds to414.0369687457006.
Thus the predeclared finite persistence criterion FAILED. The q256 first-seed
quality206/255=0.80784 fell to396/511=0.77495, while the quantum reference
quality increased. This is one retained continuation, not a distributional
estimate, asymptotic upper bound, hardness result or quantum circuit run.
The complete run, including original field preprocessing and Prange, took
250.17 seconds on this host. No matched runtime advantage is claimed.

Operational correction: the first execution reached score computation but
terminated during comparison because its NumPy integer score overflowed
inside an exact Fraction cross product. Its unsaved witness was lost.
The comparison failure was separately reproduced; converting the score to
a Python int fixed it. A tiny list-versus-NumPy native instance produced
identical witnesses and passed exact comparison/JSON serialization. The
same saved q512 input was rerun, with an assertion that all input data
matched. The driver now saves the witness before the comparison. No
selection rule or source changed, and the original six-case outputs remain
unchanged. Independent next-size Sage verification passed: both native
Algorithm H and Prange witnesses, all1152 saved parities/gain identities,
and six exact section means from3066 row-image enumerations. The report is
`classical_baselines/scalar_opi_fourier_next_size_sage.json`, with source
hashes and an exact replay command. At the halfway checkpoint75 rows are
identically accepted on rank-4 images. Before the last9 restrictions,
the fully accepted ranks are {4:157,3:4,5:1}; the exact mean is96381/256.
This confirms the same finite flat mechanism, without proving its scaling.

Decision: stop further sweeps and retain Algorithm H as a finite classical
baseline. The native full-input OPI question and this method's asymptotic
score remain UNKNOWN. A future pass must offer a source-correct theorem or
new constructive operation; another tie rule, parameter sweep, initial-
spectrum ceiling or early-alias barrier does not justify continued work.
Compare other independently motivated directions before extending this one.

Milestone validation: owned-path `git diff --check`, saved-score/source-hash
checks, STATE/handoff title consistency and owned-file whitespace passed.
Only the scoped mathematical controls described above were run; no full
repository test-suite claim. No Git commit, push or external submission.
