# StateHSP Literature: DHSP Applicability Gate

**LOCAL DERIVATION / REVIEW PENDING.** No accepted candidate, new algorithm,
refutation of the papers, full StateHSP impossibility or independent human
theorem review. This audits transfer into the EXISTING full-function DHSP
source, not a new artificial oracle proposal. It is separate from sparse
Singer membership: do not transfer that source's query gate here.

## Primary Theorems Checked

[Holt--Subramanian, arXiv2609.38085v1](https://arxiv.org/html/2609.38085v1):
Theorem7.1 learns the normal core; section7.2.2 extends to groups with
polylogarithmic Baer-norm index, subject to subgroup QFT assumptions.
Definition8.11 uses CENTER index for poly-near abelian groups. It does not
mean merely possessing a low-index abelian subgroup. Lemma7.3 supplies the
graph-state reduction from HSP. These statements and adjacent proofs were
read, not the whole paper or its complete coding-theoretic development.

[Liu--Carrasco--Eisert--Bellante, arXiv2609.35656v1](https://arxiv.org/html/2609.35656v1):
Definitions1.2-1.3 distinguish copies from preparation/inverse access.
Theorems3.15-3.16 apply to finite ABELIAN ambient groups, with respective
1/sqrt(epsilon) and 1/epsilon dependence. Formal statements/access assumptions
were inspected; full lower-bound proofs were not audited. Neither statement
solves arbitrary nonabelian reflection HSP merely by granting an inverse.

These are promising reusable research primitives, but their assumptions and
output targets must be checked before mutating an existing candidate around
them. The remaining statements below are local calculations, not source quotes.

## Same Full DHSP Interface, Strong Access Already Present

Use D_N=<r,t | r^N=t^2=e, trt=r^-1>, order2N, N>=3. Write g=r^x*t^b.
Hidden H_s={e,r^s*t}. A full hiding function is

`f_s(b,x)=pi(x-b*s mod N)`

for an injective arbitrary label relabeling pi. It hides RIGHT cosets gH_s.
The normalized graph state is

`|Graph(f_s)> = (2N)^(-1/2) sum_g |g>|f_s(g)>`.

Uniform preparation followed by one XOR oracle evaluation gives A. Its inverse
uses the SAME self-inverse oracle followed by inverse uniform preparation.
This is a coherent unitary on the entire domain/label workspace, not reversal
of a measurement-conditioned coset state. The bounded workbench executes A
and A inverse, retaining the full XOR register including unused label values.
No free label inverse is provided.

The public right-regular representation R(h)|g,label>=|g*h^-1,label> is
implementable by group arithmetic, independent of s. Directly counting equal
labels gives

`<Graph(f_s)|R(h)|Graph(f_s)> = 1 if h in H_s, 0 otherwise`.

Thus the StateHSP gap is already ONE and coherent preparation/inverse access
already exists. The missing advantage is not a small promise gap or absent
inverse in this source. Repackaging its same oracle access cannot justify
applying an abelian theorem to a nonabelian ambient group.

## Normal Core Erases The Target

Conjugating r^s*t by r changes the reflection exponent to s+2. For N>=3 this
gives a different order-two subgroup. Distinct such subgroups intersect only
at e. Therefore

`core_(D_N)(H_s)={e}` for EVERY s.

The normal-core theorem does apply, but its correct output contains no shift
information. This is a theorem-output mismatch, not a false theorem. Restricting
the action to the abelian rotation subgroup also gives H_s intersect <r>={e}
for every s. The restricted symmetry subgroup again loses the target.

Abelian QUOTIENTS have a related local obstruction. The commutator subgroup
is <r^2>, so abelianization identifies all reflection shifts when N is odd
and preserves only shift parity when N is even. A fixed homomorphism to an
abelian group factors through this quotient. This excludes that reduction
recipe, not all nonlinear encodings or new quantum transformations.

## Correct Group-Class Check

For N>=3, the center is {e} for odd N and {e,r^(N/2)} for even N.
The normalizer of H_s has order2 for odd N and4 for even N: commuting with
its nonidentity reflection is necessary and sufficient.
Intersecting the normalizers of ALL reflection subgroups leaves exactly the
center. The Baer norm is contained in that intersection; conversely every
central element normalizes every subgroup. Hence

`Baer(D_N)=Z(D_N)`,
`[D_N:Baer(D_N)]=[D_N:Z(D_N)]=2N/gcd(N,2)`.

For N=2^n this index is 2^n, not polynomial in n. For growing odd N it is2N.
These families are neither poly-near Hamiltonian nor poly-near abelian under
the inspected definitions. The fact that <r> is abelian of index TWO is
irrelevant to these particular hypotheses. SymPy bounded subgroup enumeration
checks every subgroup, not only the reflection-normalizer upper bound.

## Exactly What Weak Labels Retain

For the graph state, weak irrep-label probabilities are

`p_lambda = d_lambda/(2N) * (d_lambda + chi_lambda(r^s*t))`.

Each two-dimensional irrep has character zero on reflections and probability
2/N, independent of s. A one-dimensional irrep with r->a,t->b has probability
(1+a^s*b)/(2N); a=1 always, and a=-1 also exists for even N.

For odd N the entire weak-label distribution is independent of the shift.
For even N the only informative label occurs with probability1/N and reveals
parity. Under a uniform shift prior its mutual information is exactly1/N BIT
per sample; opposite parity distributions have total variation1/N. The
remaining full shift cannot be reconstructed from these labels alone.

Do NOT declare the full irrep quantum blocks uninformative: their orientation
contains the familiar DHSP phases. Row/column basis changes, retained domain
registers, multi-register interference or a new state transformation are NOT
excluded by this label calculation. This pass is not a generic quantum lower
bound and does not revive earlier codomain-erasure restrictions here.

## Try To Falsify The Recommendation

- **New paper secretly solves reflection HSP:** its inspected output is the
  normal core, and its stronger group theorem requires a small Baer index.
  Find a different theorem satisfying this source's nonnormal/full-group
  promise before claiming it does more; the current source does not qualify.
- **Preparation inverse is enough:** it exists here, with gap1. The abelian
  sample/query comparison establishes no additional solver for this ambient
  group. A new nonabelian extraction method would be substantive progress.
- **Tensor linearisation removes the obstruction:** cancelling a KNOWN
  projective cocycle is not the same as decoding an UNKNOWN conjugated
  reflection. A usable reduction must specify an abelian projective action,
  physically prepared state, nontrivial stabilizer encoding s, inverse costs
  and promise gap; no such reduction is supplied by this audit.
- **Normality can be forced without losing s:** ordinary abelianization and
  rotation restriction lose it. A nonlinear or enlarged-space embedding might
  escape, but must retain distinguishable target data with a proved decoder.
  The local quotient obstruction is not a no-go against those embeddings.
- **All small examples work:** bounded examples certify exact group/source
  identities, not asymptotic extraction. The Baer/center formula and scope
  statements require independent review, not an extrapolated runtime fit.

## Experiments, Files And Next Target

All54 shifts at N3,4,5,6,8,12,16 are retained with a fixed injective relabeling.
Controls check graph overlaps, executed A inverse, trivial core, full subgroup
Baer norm, and exact/numerical character distributions. Growing N=2^n ledgers
at n8/16/32/64/128 retain exponential group indices and rare parity information.

Falsifiers: a nontrivial reflection core for N>=3, Baer element outside the
center, graph overlap violating subgroup membership, incorrect inverse return,
weak-label shift information beyond the stated parity law, or an inspected
theorem that actually supplies full nonnormal recovery under these promises.

New module/tests `state_hsp_dhsp_scope`, report under `research/reductions/`,
matching literature audit/contract. Group logic uses SymPy, not a new engine.
There is no implemented StateHSP learner or asymptotic group-QFT compiler.
Verified:23 new focused tests, combined five-file regression139 passed1.95s,
Python syntax, strict JSON and scoped whitespace checks. No full repository
suite, CLI/registry validation, commit or push is claimed.

Gemini should ingest exact theorem scopes and this failed TRANSFER into the
no-go/known-technique index, not mark the paper itself as a negative result.
No accepted candidate or general StateHSP rejection. GPT should examine a
concrete normality-changing/state-conversion reduction that preserves a useful
target, or investigate the new coding-based linearisation on a naturally
supplied projective abelian action. That requires inspecting the remaining
technical sections first; it is not completed by these scope checks.
