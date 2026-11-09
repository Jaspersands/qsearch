# General Selmer admission: complete wild local images

Date: 2026-11-07. Status: admission PARKED; exact source falsifiers reviewed.
General algorithm NOT admitted.
No speedup, novelty, hardness or quantum execution claim.

## 1. Native question and independent selection

Input: explicit monic separable f in Z[X], odd d=2g+1, growing g and
coefficient bits; C:y^2=f with rational infinity. Output the integer
F2-dimension of Sel^2(J/Q), NOT Mordell-Weil rank, rational points or covers.
Target: bounded-error quantum polynomial BIT time under explicit GRH. Global
compact S-unit/class-support algorithms are reusable candidates, but no full
composition is asserted here. The missing operation is a COMPLETE local
Kummer image at EVERY bad/small/wild/dyadic prime, from f alone. No supplied
regular model, cluster picture, local generators, field closure or class/unit
advice. Charge all local extension degrees, precision, charts, source rejection,
linear algebra and global compact evaluation. Expected possible advantage is
replacement of general classical class/unit arithmetic by known quantum
arithmetic; no classical lower bound or separation is known.

Independent comparison with isogeny torsor inversion found no new paid
class-group action/phase decoder there. This Selmer endpoint has external
arithmetic value, but is admitted only if the complete wild local operation
can be paid. Prior good2 and p>d local results do NOT cover this contract.
Corpus been-tried preceded primary literature; baselines returned an
inapplicable LLL lead. The actual matched baseline is Stoll's classical
two-descent with class/unit computation, complete extension/disc generation,
and its explicitly warned random polynomial-divisor alternative. Sources
and exact falsifiers below are classical; no quantum circuit is built.

## 2. Exact native falsifier: all unramified point traces can vanish

Let p=3, h=X^2-3, k=X^3-9, f=hk. This is a smooth genus2 curve over Q3.
Write alpha^2=3, beta^3=9. Both h and k are irreducible over Q3 and over
EVERY finite unramified extension F: root valuations are 1/2 and 2/3.
Stoll Lemma4.4 therefore gives dim J(Q3)/2J(Q3)=2-1=1.

For any P=(x,y) in C(F), normalize v(3)=1. The value group of F is Z.
If v(x)>=1 (including x=0), v(h(x))=1, v(k(x))=2, hence v(f(x))=3:
no such point exists. If v(x)<=0, both factors of
f(x)/x^5=(1-3/x^2)(1-9/x^3) are principal units, hence squares in F.
Thus x^5, and therefore x, is a square in F. In each root extension,
x-alpha=x(1-alpha/x) and x-beta=x(1-beta/x) are squares, because the
parenthesized terms are principal units in odd residue characteristic.
There are no finite branchpoints in F, and infinity has trivial label.
Consequently EVERY curve point over EVERY finite unramified extension has
trivial Kummer label. By norm/corestriction compatibility, ALL their traces
to J(Q3)/2 also vanish, even if arbitrarily many unramified fields are used.

The missing direction has an explicit ramified source. For the degree2
branch divisor D_h=sum_{h(a)=0}(a,0)-2 infinity, Stoll §6 gives
  delta(D_h)=( -k(alpha), h(beta) )=(9-3 alpha, beta^2-3).
Both coordinates have normalized field valuation3 (odd). Their field norms
are EACH54, so total norm54^2 is square as required. This nonzero label spans
the one-dimensional image. It is the trace of (sqrt3,0)-infinity from the
ramified quadratic field. The minus sign in the first coordinate is essential.

This refutes complete generation by unramified curve-point traces, including
a strategy that only lifts curve points from smooth multiplicity1 loci over
unramified extensions. It does NOT
refute regular-model methods with ramified horizontal divisors, tame-field
methods (this witness is tame), general local-image algorithms or quantum
algorithms. It does not assert hardness. Parent derivation and independent
mathematical check agree. The targeted Sage/PARI algebra control confirms
norms54, valuations3, ramification indices2/3 and local factor degrees2/3.

The same proof supplies an unbounded-genus counterfamily: for EVERY g>=2
and EVERY odd prime p, take h=X^(2g-2)-p, k=X^3-p^2, f=hk. Eisenstein
and the slope2/3 Newton polygon give irreducibility over every unramified
extension. For v(x)>=1, v(f(x))=3; for v(x)<=0, f(x)/x^(2g+1) is a
principal unit. Hence all unramified point labels still vanish. The local
image has dimension1 and delta(D_h)=(-k(alpha),h(beta)) has normalized
valuation3 in BOTH fields (2(2g-2)>3). Norms agree by the resultant identity
since deg(h) is even. This includes p dividing2g-2 and p=3: only odd residue
characteristic is needed for principal units to be squares. For g>=3 the
complementary degree3 branch divisor represents the same mod2 class; for
g=2 use degree2. No large extension or divisor is needed for the witness.

## 3. Exact density falsifier for the known unstratified sampler

At p=3,g=2, for any integer N>=1, put
  f_N=(X-1) product_{j=1}^4 (X-3^N j).
All five roots are rational, hence dim local image=4. For a nonbranch
prime-divisor point over E with v_3(x)<N, the four clustered quantities
x-3^N j have the same squareclass in E. Their norms consequently have one
common class u in Q3*/Q3*^2; the square total-norm condition forces the fifth
class1. Such labels lie in {(u,u,u,u,1)}, dimension at most2. The remaining
branchpoint x=1 also has trivial label: all differences from the cluster and
their product are principal units. Thus a complete source MUST produce a
point/divisor involving x of valuation>=N.

For a monic integral polynomial h of degree<=g, all roots are integral. A
root of valuation>=N forces v_3(h(0))>=N. Under uniform independent integral
coefficient sampling (mod3^M with M>=N), this event has probability3^-N per
raw attempt. After T possibly adaptively stopped raw attempts the success
probability is at most T3^-N. Input coefficient bits are O(N). This rules out
a polynomial clock for that precise sampler, even with charged classical
rejection. Applying ordinary amplitude amplification to this same rare-event
source only square-roots the exponential scale. It is NOT a query lower bound
for arbitrary structured quantum algorithms. Disc/model stratification easily
handles this particular family; no general classical hardness follows.

## 4. Constructive route and source obligations

A plausible replacement: construct an explicit regular model; generate its
component/reduction contributions AND shallow formal contribution; lift to
explicit curve divisors and evaluate their Kummer labels. Every component
with relevant multiplicity, including multiplicity divisible byp, must be
handled. The unramified shortcut in §2 fails. A dual graph, abstract finite
group, or knowledge of J[2] alone is not a complete generating operation.

New source snapshot: audits/sources/wild_local_selmer/source.json.
Liu 2504.16808v3 gives an explicit double-cover desingularization algorithm,
including dyadic surfaces. Theorem1.1 is termination; Theorem4.6 bounds
weighted multiplicities after one normalized blowup; §5.3 iterates; §5.4
pays attention to chart representations. These statements must not be
silently read as a polynomial total BIT bound. Long lambda2 chains and
chart/precision growth require a separate argument. Liu2603.19065v2 Corollary1.27 (text899–914) DOES give the quantitative
bound n<=v(Delta_initial)/2 for a chain of singular WEIERSTRASS models.
Retain this genuine bound. Extended Tate Proposition2.4 (1472ff) requires
reduced special fiber and a rational point with delta<=3; Remark2.7 extends
specified nonreduced cases. These do not by themselves bound all arbitrary
wild regular charts or their BIT arithmetic. Double-cover Example4.8
(1279–1291) has long chains with lambda3/4, disproving a depth bound from
initial lambda alone; its growing exponent is NOT a counterexample to a
bound in expanded input bits.

Bosch–Liu Theorem1.1 (text109–135) supplies the geometric component-group
weighted intersection quotient; rational components require the corrections
in Corollary1.10/Theorem1.17. Corollary1.5 gives gcd(r_i d_i)=1 when there
is a rational curve point over finite residue field. Lemma2.1 (545–555)
gives surjectivity J(K)->J_k(k)->Phi(k) in this situation, using smoothness
and Lang. It is not an algorithm constructing divisor representatives.
An unramified section meets a multiplicity1 smooth component: in a strict
normal-crossings chart pi=u product t_i^d_i its valuation sum is1. The
explicit counterfamily above proves this restricted source can miss mod2
classes, rather than merely pointing at multiplicity>1 components.
Gehrunger-Pink2404.14214v2 uses marked branchpoints after field extension;
expanded closure cannot be supplied free. Muselli2206.10420v1 explicitly
excludes residue characteristic2. Earlier Liu1996 is a primary baseline,
not assumed to prove modern complexity.

Two distinct Claude obligations were submitted: actual Liu resolution BIT
cost (Fable/high) and complete Picard-to-divisor generation given a model
(Opus/high). BOTH ended at32768 output tokens with EMPTY reports. They supply
NO evidence and are not retried. Saved bundles:
- audits/claude_runs/2026-11-07-wild-local-resolution: estimated USD1.995190.
- audits/claude_runs/2026-11-07-wild-local-picard: estimated USD0.764120.
Total this pass USD2.759310. Aggregate46 reported estimates USD37.813650,
22 completed reports, includes pre-anchor usage; NOT invoice or remaining
balance. No pending call or unknown-cost retry.

The supplied model in the second prompt was only a conditional lemma
interface, never admitted as native free input. Initial local preflight
rejections were due to PDF form-feed characters, before any API call; cleaned
plain-text packets retain source URL/PDF hash. Large full-source contexts
(35679 and27190 input tokens) and difficult generation requests again yielded
no report. Future independent Claude tasks should isolate a short identity,
explicit proposed operation or actual source comparison; no automatic rerun
or larger-budget repetition of these unresolved searches.

Verification: parent read actual source statements and independent source
scope audit. Focused mathematical review is retained at
`audits/reviews/2026-11-07-wild-local-falsifiers.md`. One exact classical
control `audits/controls/wild_local_selmer/control.py/.json` checks norms,
valuations, a 32-digit Q3 factorization consistency check and f_N for
N=1,2,4,8. Exact local irreducibility follows from the separate valuation
proof, not finite-precision factoring. A Sage constructor typo in
the reporting fraction was corrected; no mathematical assertion failed.
The control is not a local-image solver, proof of uniform complexity or
quantum execution. No broad suite was run.

## 5. Claim gates and next decisive experiment

False gates: general Selmer algorithm, polynomial arbitrary-wild local source,
model construction clock, novelty/separation, general source impossibility,
MW-rank/points/covers, quantum execution. Unramified completeness and the
specified uniform-polynomial source clock are refuted, not general approaches.

Neither required constructive obligation closed: full regular-model BIT cost
and complete ramified divisor generation remain OPEN. Therefore the general
Selmer admission is PARKED. This is a missing algorithm, not impossibility.
Independently select the next native mechanism; do not queue a resolution
backend, adjacent source variant or another sampling sweep. Reopen this
route only upon an explicit paid construction for the remaining obligations.
Next command: `/opt/anaconda3/bin/python tools/corpus/cli.py been-tried
'native quantum algorithm constructive mechanism' -k 3`; expected artifact:
a selected native problem/input/mechanism/baseline contract and cheapest
classical falsifier, justified by value outside this repository.
