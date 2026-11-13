# Growing quadratic towers: support and conic recurrence

2026-11-13. CLOSED WRITTEN at the stated ERH/factoring scope. The final
380-line independent batch proof and 240-line witness proof have been fully
parent-read and checked, together with the actual maximal-order source and
fixed-rank quaternion wrappers. This current conclusion supersedes the
historical open gates retained below. It is a written algorithm, not code,
a novelty claim, an unconditional classical polynomial algorithm, or a
quantum advantage.

## Final native theorem and proof chain

For EVERY supplied explicit quadratic tower Q=F0<...<Fh of degree N=2^h,
with expanded maximal-order tables/bases and tower maps charged as input,
and factored rational support containing2 and all tower ramification,
there is a bounded-error classical polynomial-BIT reduction that returns
an expanded independent complete basis of Fh(S_h,2) and stored coordinates.
It assumes full relevant-Hecke ERH for the small split-prime theorem and
makes polynomially many integer-factorization calls of polynomial TOTAL
query bit mass. Requested error eta has logarithmic overhead. No conic,
unit, class-group, principalization, point, supplied-prime or coordinate
oracle remains. Coordinate queries pay their own expanded input sizes.
Outside-S valuations are EVEN; these representatives need not be S-units.

The same coupled proof constructs promised isotropic ternary/quaternary
points on ORIGINAL tower fields. Its auxiliary quadratic extensions only
serve known-witness shortening; no recursive problem is solved over them.
The finite schedule is six strictly lower-field batches. For total payload
M_d at depth d,

    M_(d+1)<=9M_d+(3Pmax+2A)*6^d,
    M_d<=9^d*M0+(3Pmax+2A)*(9^d-6^d)/3.

Shortened conics have height <=64*(Hcoeff+logDelta+n²). Fixed-rank wrappers
and sparse one-tag gluing therefore give H_child<=C_*(H_parent+W), with
absolute nonrecursive C_* and original-field polynomial W. Since h=log2N,
Hmax=2*C_*^(h+1)*(H0+W) and Pmax=O(N*(Hmax+W)^2) are original-input
polynomials. Stored coordinate queries visit only two tagged children;
all kernel-coordinate construction visits are bounded by O(12^h).
All dense products, numerical prime enumeration, auxiliary maximal orders,
exact LLL, embeddings, root extraction and finite-field work are charged.

Material repairs to the paid proposal are mandatory:

- retain every formal tag and its normalization scalar, including pure tags;
- extract original-target views by explicit binary matrices; inverse-map,
  sparsify in ORIGINAL tags, then reset before conic input/return;
- use EXACT nonzero coefficient-prime-ideal support, not every prime above
  a rational support cover;
- mask every form's pool by its OWN norm cutoff X_q as well as splitting;
- use two Hilbert CHARACTER rows per finite place in the support bound;
- retain rational point coordinates, including at rational leaves;
- obtain maximal orders from the full radical of the CONSTRUCTED ORDER
  discriminant through actual Buchmann--Lenstra, including even exponents.

For arbitrary large original targets, the restored output height is not
field-only: Q,S={2},J=(p) forces height>=logp in tag1. This is a scoped
counterexample to an overbroad intermediate claim, not this root endpoint
(which has no target tags). The older Q(sqrt(-14)) rank6 example continues
to refute unrestricted norm-image surjectivity. No finite control proves
the asymptotic algorithm; the proof is the displayed recurrence plus the
independently checked exact algebra and bit interfaces.

Proofs: `audits/reviews/2026-11-13-native-tower-batch-audit.md`,
`audits/reviews/2026-11-13-native-tower-witness-shortening.md`,
`audits/reviews/2026-11-13-maximal-order-source-check.md`, and their referenced
stable tagged/reset/gluing proofs. Parent also checked actual Kutas
Propositions12/15, Corollary19, Theorem20 and Remarks21/22; the four-dimensional
restriction improvement is a separate proved algebraic deduction, not an
attribution to Kutas. Exact quaternion zero-divisor exits are retained.

Strongest comparator is now this factoring reduction itself. Quantum
factoring could replace its charged queries but creates no advantage beyond
factoring, and removes neither ERH nor the explicitly charged native field
input. General number fields without a supplied quadratic tower remain
outside this theorem. Novelty/priority remains UNKNOWN. The broad corpus
refresh returned mostly lexical matches; the actual Kutas, Koprowski,
Wesolowski and Buchmann--Lenstra sources delimit the imported results.
No nearby field variant, solver implementation or new infrastructure is
selected. The next pass must compare a new concrete native quantum mechanism
against these stronger classical baselines.

## Native problem and expected value

Input an explicit tower Q=F0 subset ... subset Fh, Fi=F(i-1)(sqrt(di)),
N=2^h, with charged expanded field/order coordinates and embeddings. For this
proof attack, maximal-order tables may be supplied and their full size is
charged. S_Q contains2 and all ramification primes; S_i contains all primes
above S_Q. Output a complete independent basis of Fh(S_h,2), with expanded
polynomial-bit representatives and coordinate maps. Target bounded-error
poly(N,B,log1/eta) time using integer factorization of polynomial-bit
intermediates. Supplying complete class groups, units or norm solutions is
forbidden. General compact outputs require a separate support interface.

Mechanism: relative Hilbert-symbol norm spaces, bounded-rank quaternion/conic
descent, and the support-obstruction kernel below. The established ERH-conditional factoring
reduction closes the explicit native arithmetic scope. It would simultaneously establish a classical
factoring comparator; no advantage beyond factoring, novelty or hardness is
claimed. The repo already has general growing-degree quantum compact
isotropy and Selmer compositions under explicit GRH. Renaming those does not
answer this question.

Strong classical baselines: the proved quadratic and promised-quartic
factoring algorithms; general S-unit/class arithmetic; local Hilbert-symbol
linear algebra; lattice reduction. Corpus been-tried and baselines were run
before actual primary checks. Kutas1606.01053v2 Remark22 and
Koprowski2111.08569v2 Algorithms1/2/4 and AppendixA were inspected, with exact
excerpts in `audits/api_inputs/2026-11-13-tower-recurrence/`.

## Exact support-obstruction operation

Let L=F(sqrt d), and include all dyadic and relative ramification primes in S.
Assume, for this algebraic reduction, complete F(T,2) presentations and conic
witnesses are available at the charged supports. Let

    V = F(S,2) intersect N_(L/F)(L*).

For a basis a_i, obtain beta_i with N(beta_i)=a_i c_i². Include numerator AND
denominator support in E outside S. At a split prime the two beta_i valuation
parities agree; at an inert prime its single parity counts. Since outside S
is unramified, each parity divisor is the pullback of J_i in F2^E. Let

    W = image(F(S union E,2) -> F2^E),
    C = kernel(c -> sum_i c_i J_i mod W).

For c in C, solve for gamma in the enlarged base presentation with parity
sum c_i J_i. Then product beta_i^c_i times gamma has even outside-S support
and the desired norm squareclass. Conversely, if alpha is an even-supported
lift of that norm class, beta/alpha has square norm. The identity

    (x+t)² = (Tr(x)+2t)x, when N(x)=t²,

with x=-t handled separately, expresses its squareclass by an element of F.
Unramified outside-S valuations put that element in F(S union E,2) with
exactly parity sum c_i J_i. Hence c belongs to C. The norm kernel is
F(S,2)/<d>, yielding the exact sequence

    0 -> F(S,2)/<d> -> L(S_L,2) -> C -> 0.

Parent checked this algebra and an independent review agrees. This removes
the old odd S-class premise algebraically. Parent fully read the296-line independent kernel/coordinate proof and
reproduced its exact Sage/PARI control. The fixed-quartic composition is now
closed written for EVERY quartic with a quadratic subfield. The control
F=Q(sqrt(-14)), L=F(sqrt2), S_Q={2,7} has a genuine rank-one obstruction:
dim V=4, dim C=3 and dim L(S_L,2)=6. The uncorrected full-V shortcut would
predict7. The odd inert denominator prime over3 is explicitly checked.
No growing-degree clock follows from the sequence. A basis of V alone is not enough when C is proper.

## Paid proof gates

Dispatch: `audits/api_inputs/2026-11-13-tower-recurrence/dispatch.json`.
The first four requests are terminal/read/reaped: three completed and
one EMPTY truncation (support-growth), with no retry. No request has tools
or credential context.
Two OpenAI/max and now two Claude/high; local ceilings20USD are not charges.

1. Fixed-rank descent: I_j(3) reduces to boundedly many I_(j-1)(3,4,6).
   Pay the 4/6 solvers instead of calling the same conic oracle circularly.
2. Aggregate support: A_j needs A_(j-1)(S), one conic lift per norm-basis
   vector, and A_(j-1)(S union E). Bound the full adaptive dependency DAG.
3. Quaternary gluing: replace the unpaid auxiliary-prime search in
   Koprowski Algorithm1. Its AppendixA inverse product of prime norms is
   not polynomial in prime bit length. This refutes that inference, not
   every possible prime-selection algorithm.

A fourth task tests a NEW parent operation: U_K(S;J_i), the complete space
of pairs ([x],c) with outside-S parity(x)=sum c_i J_i. It retains coefficient
labels even if x=1. Push target parities by relative norm, compute the lower
U, intersect norm conditions, lift a basis, then call the lower U on the
residual pulled-back parities. Multiplying those correction witnesses by
the beta products gives the upper U; the restriction kernel should be
exactly ([d],0). This replaces a full enlarged-support basis by a constrained
divisor problem. The completed Claude report and independent review confirm the exact
algebra. The94-line independent tagged control passes26exact checks,
including equality of the full seven-dimensional constrained space and
kernel([d],0). Keeping a pure coefficient tag is essential. No asymptotic
conclusion comes from that control. Full coordinate-query BIT composition is
under independent review; actual conic batching remains open.
Exact new construction: `tower-parity-constrained-descent.md` in the packet.

Constant branching over h=log2 N would be polynomial. Degree-polynomial
branching at every level only proves a quasipolynomial recurrence; repeated
polynomial height composition may be worse. Neither is a lower bound on
all methods. The stop rule is to park this line if no complete finite clock
emerges, rather than continue with nearby fixed-degree variations.

## Expanded squareclass height compression: closed written

Parent fully checked the270-line independent proof in
`audits/reviews/2026-11-13-squareclass-weighted-lll-compression.md`.
This operation closes the stated expanded representative-height gate. For expanded
alpha in F(S,2), factor its principal fractional ideal and set
v_P(I)=-floor(v_P(alpha)/2). Then alpha I²=J, with J squarefree integral
and supported in S. On the ideal lattice I use the positive archimedean norm

    q(gamma)=sum_real |sigma(alpha)| sigma(gamma)²
             +2 sum_complex |sigma(alpha)| |sigma(gamma)|².

Its Gram determinant is |disc(F)| N(J). A short vector supplied by LLL gives
beta=alpha gamma² integral, in the same squareclass, with every absolute
embedding bounded by q(gamma). Thus its height can depend on field data and
support instead of the incoming unit size. All finite-BIT details are paid: ideal HNF, a prescribed dyadic rational
Gram precision from det(Q)>=1 and an explicit lambda_max bound, exact
Gram-only LLL with bounded transformation coefficients, native primitive
roots and trace-dual output conversion. For degree N,

    max_sigma |sigma(beta)| <=3*2^((N-1)/2)(|disc(F)|N(J))^(1/N).

If S lies over S_Q, log N(J)<=N sum_(p in S_Q)log p. Thus output
coordinate height is affine in this rational support bit-mass plus a
polynomial in the charged field/basis input. Runtime still charges alpha's
EXPANDED incoming size. No compact expansion, small conic discovery or total
support-growth bound follows. No unit basis or principalization is supplied.
The actual LLL scan was inspected on PDF pages3,7,8,9; its text file is empty.
The rational-Gram extension is proved in the note. The actual Mehlhorn–
Sagraloff–Wang1301.4870v2 Corollary1 and preceding scaling derivation were
read for the finite root-approximation compiler.

The exact Q(sqrt2) control uses alpha=3(1+sqrt2)^(2k)/5^(2k), k=1,10,100,1000.
I has basis5^k(1,sqrt2); its weighted trace Gram determinant is72 for every k.
The real CAS control checks integrality, identical squareclass and bounded
output coefficients. It is a finite falsifier only, not a proof of the
uniform theorem. Artifacts: `audits/controls/tower_recurrence/weighted_lll_control.*`.
Even a proved compression does not by itself bound the growing support E.

## Returned findings and their dispositions

All three nonempty reports in the first four-job round were fully parent-read.

- `tower-fixed-rank-descent`: accepted the promised-split six-form transfer
  is3H, so every four-dimensional restriction is isotropic. The first such
  restriction reduces the six-variable step to a quaternary. The middle
  Pfister step is a base ternary; total is two embedding quaternaries and
  one ternary over the smaller field. Accepted the exact cycle when a final
  embedding four-form is solved by adjoining its discriminant and calling
  the same conic. The Hamilton/sqrt(-3) family has a small explicit solution
  while all coordinate ternaries are anisotropic; it falsifies that shortcut,
  not a general algorithm. No uniform conic compiler was obtained.
- `tower-support-growth`: EMPTY truncation, no findings or retry.
- `tower-parity-constrained-descent`: accepted exact pair-space descent and
  kernel. New generic divisor reset: for residual ideal R, ordinary LLL in
  R^-1 finds w so M=(w)R is integral of lognorm O(n²+logdisc). Multiplying
  beta by w changes its residual to odd(M) and preserves its norm tag. Parent fully checked the243-line independent divisor-reset proof:
  `audits/reviews/2026-11-13-conic-content-support-normalization.md`.
  This bounds new target mass independently of the conic witness. The report's
  alternate squareclass reset is superseded by the fully checked stronger
  weighted-LLL proof above. Its unread regulator citation is not used; a
  crude Minkowski/HNF count suffices. Its recurrence bounds are not runtime
  lower bounds. The U-only basis support/height clock is proved conditional on a uniform
  expanded conic primitive; arbitrary coordinate-query BIT composition is now closed after full
  parent check of the332-line independent proof below.
- `tower-local-gluing`: accepted the collective small-splitting-prime idea,
  with its unverified analytic estimate REPLACED by actual Wesolowski2019
  Theorem1.2 and the stronger explicit relevant-Hecke ERH assumption below.

## Isolated ERH auxiliary-prime gluing: closed written

Parent fully checked the232-line independent source/control review:
`audits/reviews/2026-11-13-tower-gluing-source-check.md`.
For q=<a1,a2,a3,a4> over K, include2 and coefficient numerator/denominator
support in S. Set d1=-a1a2,d2=-a3a4, M=K(sqrt d1,sqrt d2), and ray modulus
m0=product_(P in S) P^(2v_P(2)+1), with all real places. The full ray Artin
kernel H0 has index <=4. Under FULL ERH for the relevant Hecke characters,
Wesolowski's actual theorem generates H0 by small degree-one split primes.
With L=2+[K:Q]+bitlength|discK|+bitlengthNm0, the safe explicit cutoff is

    X=(32L)².

Enumerate/decompose primes up to X and keep those for which both d_i are
residue squares. No ray class group, class field or hidden principal generator
is computed. The unknown feasible common value has outside-S odd primes
splitting in M; the ray-class square quotient moves them to this small-prime
support without changing local squareclasses at S or signs. Thus the complete
K(T,2) basis and local Hilbert/sign linear system yield a feasible b. Those
complete-basis and subsequent ternary backends remain charged assumptions.
The source theorem/definitions and final proofs were actually read; the
narrower quadratic-only GRH claim in the paid report is not imported.

Exact q=<1,1,-3,-7> has solution(1,3,1,1) and commonvalue10, but no initial
S={2,3,7} supported commonvalue class. Adding split prime5 works. Multiplying
10 by1177=11*107 preserves its S/local-real classes yet creates an obstruction
(-1,11770)_11=-1. This falsifies local-only approximation, not an asymptotic
algorithm. Rank-only arbitrary-prime additions also have no finite clock.

Two NEW completion tasks run in `api_inputs/2026-11-13-tower-native-composition/`:
one OpenAI/max end-to-end batched compiler and one Claude/high sparse-support
height construction. Their local ceilings9USD are not charges. These tasks
use the returned operations and actual primary cutoff; they are not retries.

## Claim gates and next acceptance test

False: general tower polynomial clock; general classical Selmer solution;
new quantum isotropy theorem; classical hardness; novelty; useful advantage.
No quantum implementation or infrastructure was selected.
Next: finish the independent generic-divisor and conditional tagged-U BIT
composition, then inspect both new completion reports. All previous terminal
reports and the weighted-LLL/obstruction proofs have been fully checked. Acceptance requires one
uniform polynomial in original N,B and requested failure bits for all
supports, witness sizes, prime searches, basis/coordinate operations and
calls. A compact certificate, per-level polynomial, or numerical experiment
fails this acceptance test.

## Generic divisor reset and the conditional U basis clock

CLOSED WRITTEN after parent full243LF proof check. For any integral ideal R
of degree-n field F, compute an ordinary short vector w in R^-1 with
M=(w)R integral and

    N(M)<=3^(n/2)*2^(n(n-1)/4)*sqrt(|discF|).

Use m=N(R), the integral lattice m R^-1, prescribed rational Gram precision
and exact LLL; all ideal arithmetic and expanded w are paid. Factor only
N(M) to expose the new residual support, a polynomial-bit integer. M may
remain nonprincipal. Replace each conic norm lift beta by w beta and its
residual R by odd(M); this preserves the norm TAG, and changes the upper
squareclass in precisely the way the residual records. A subsequent
weighted squareclass reset preserves that changed class while bounding its
expanded representative.

At every U-only node, individual target norms are bounded by the original
target norms or field discriminants. Target COUNT grows only additively by
dimF_j(S). An elementary HNF count of small ideals bounds logclassnumber;
no regulator theorem, class computation or enumeration is used. Thus all
node support/height inputs are bounded in ORIGINAL data, and there are at
most2N−1 nodes, with polynomially many conic calls each. This is a polynomial
basis reduction to a UNIFORM polynomial EXPANDED relative-conic interface.
It does not supply that interface or the coupled Kutas/I4/U recurrence.

The optional content-ideal version was also checked, but the generic reset
is simpler. Dyadic exclusion is essential: x=y=1,d=17,a=-1,c=4 has contentZ
while both split2-adic beta valuations are odd. All intended S contain2.
No algorithm or speedup follows from a finite control.

## Full tagged-U reduction, including coordinates: closed at oracle scope

Parent fully checked `audits/reviews/2026-11-13-tagged-tower-conditional-composition.md`
(332LF). For arbitrary initial r0 parity targets, the exact tagged presentation
and stored coordinate routines are polynomial reductions to integer factoring
AND a uniform polynomial EXPANDED relative-conic primitive. Field tables,
maximal orders, original support and initial target sizes are charged.

The proof gives explicit original-input bounds T,A,r*,G,Z: individual target
norms are bounded by original targets or field discriminants; counts grow
additively by A; weighted output normalization prevents composing the conic
output polynomial at each level. There are <=2N−1 U nodes and <=(N−1)G
conic calls. Kernel-coordinate routines invoke existing child presentations,
not new U constructions, and give O(N logN) coordinate-node visits during
construction.

The coordinate height argument uses a common integral denominator. For
L(x)=log m(x)+log max(1,max|sigma x|), relative norm doubles L. Stored beta
are integral; if x'=x product beta^u and sigma²=Nx', then m(x)*sigma is
integral because its square is integral. Hence the trace-identity gamma
shares that denominator and L(gamma)<=L(x)+G*Z_arch+2. Each recursive child
has L<=2L_parent+fixed polynomial, giving ORIGINAL-input polynomial bits.
Exact square roots use a supplied-tower recursion with at most three smaller
calls: norm, then (A+sqrtNorm)/2 and (A-sqrtNorm)/2; B=0 uses z and z/d.
Its finite count <=N² and common-denominator bounds avoid an extra global
root/factorization oracle. Dyadic norm rows use the already checked local
squareclass generators and their norms, not residue-unit enumeration.

This is a complete CONDITIONAL reduction, not an implementation of Conic.
The actual conic/I4/U schedule remains the single missing end-to-end gate.

## Sparse gluing output, independent of the empty paid report

Parent fully checked156LF `audits/reviews/2026-11-13-sparse-gluing-support.md`.
For a complete K(S union Q,2) source and ell feasible original linear local
conditions, form its image Z under (Q-parity, local profile). The parity image
has codimension c_Q<=dimCl(O_K,S)/2. The annihilator gives an affine binary
system for q with computed row rank rho<=c_Q+ell. Selecting pivot columns
produces a solution supported on at most rho primes, and a source lift.
No class group or minimum-weight decoder is computed. Weighted normalization
preserves all profiles and gives

 log2 max|sigma b| <= log2(3)+(n−1)/2+log2|discK|/n
                    +[log2N(radS)+rho log2X]/n.

The actual source/pool construction still costs polynomial in its full size;
only the output-height bound avoids pool cardinality. ERH splitting remains
the reason new-prime Hilbert equations are automatic. The residual H logH
height possibility is not an affine global clock. The Claude sparse-height
request was EMPTY/truncated/reaped with no findings and no retry; this is
parent derivation plus internal proof. One OpenAI whole-composition report
is still running.

## Concrete native compiler returned; independent proof review open

The final OpenAI tower-batched-native-compiler report is completed, fully
parent-read and reaped. It proposes an actual mutually recursive U/C/E
algorithm, not another oracle interface. All end-to-end claim gates remain
FALSE pending verification. Its new mechanisms are:

- normalize every parity target by a recorded scalar; sparse tag-image bases
  have weight at most class-codimension plus local rows plus one;
- choose one coefficient-parity target per quaternary, and share one bounded
  small-prime pool across the ready batch;
- shorten an EXISTING conic witness using ideal reset over K and weighted
  squareclass reset over K(sqrt(d)), with no recursive calls over that field;
- execute three U preparation batches and adaptive E/C/E batches over the
  strictly smaller ORIGINAL tower field. Proposed count is <=6 children,
  total payload nextdepth <=9*current+6^depth*(3Pmax+2Dmax).

The proposed witness output has extensive absolute height O(Hcoeff+W) with
an absolute constant, and sparse gluing claims the same bound. These would
pay Hchild<=C*(Hparent+W), hence C^h=poly(N), before any full polynomial
workspace bounds are used. Auxiliary maximal-order construction must be
paid from factored discriminants; no unit/class/principalization oracle.
Full relevant Hecke ERH and charged integer factoring remain assumptions.

Three focused independent checks: batch/dependencies, witness shortening,
and primary maximal-order source; two new Claude attacks cover local-choice
one-tag gluing/linear support height and coordinate/basis rebasing. These
are distinct new proof obligations, not retries of the empty sparse report.
Exact packets: audits/api_inputs/2026-11-13-tower-compiler-audit/dispatch.json.
The completed two-job composition round is frozen at
controls/tower_native_composition_round: 31 unique hashes verified once,
round3.468914USD, cumulative273.575724/209priced (Anth157.997014,
OpenAI115.578710), five UNKNOWN bills excluded. Estimates are not invoices
or balances; owner-reported SPENT155.99/101.71 stays separate.

The independent147LF post-tower comparison was fully parent-read. Its
near-join TDA candidate is classically matched by an Euler estimator under
homology concentration and constant ambient-face/Betti ratio. Hypergraph
one-body readout has only a binary population identity; actual multi-community
source remains unread/unverified and quartic scaling alone is not selected.
Convex-boson source lacks a distinct paid output and primary comparison.
No replacement direction or broad impossibility claim is promoted.

Coordinate paid audit disposition: Claude tower-coordinate-rebasing-audit
truncated with1435bytes, fully parent-read/reaped. It gives only an introductory
verdict and stops immediately before naming its claimed amendments. Neither
its acceptance language nor its unnamed false-statement claim is an auditable
proof/counterexample. No findings imported and no retry. The independent
full coordinate/batch proof remains the decision gate. Cost at next milestone.

## Known conic witnesses admit absolute-slope shortening

CLOSED WRITTEN at the explicit factoring interface: parent fully checked240LF
independent proof (one subsequent wording clarification of prime BIT size),
`audits/reviews/2026-11-13-native-tower-witness-shortening.md`, and complete
maximal-order source review. Given an already expanded nonzero witness of a
nonsingular diagonal ternary over original degree-n tower field K, output
another with summed extensive absolute height at most

    64*(H_coeff+log|disc K|+n^2).

The slope64 is independent of degree. Runtime pays the OLD witness, coefficients,
all factorizations and every expanded field table. No first witness is discovered.
For x²-dy²=a z² with d nonsquare, beta=(x+y sqrt(d))/z has norm a. Reset its
outside-coefficient-support parity using a short vector of a base inverse ideal;
then square-reset beta in the explicitly constructed auxiliary quadratic field.
Output x0,y0 and z0=w*N(gamma) or an exact ORIGINAL-field square root. No
conic/U/class/unit call is made over the auxiliary field.

The stronger native order is A=O_K direct-sum D_d^-1 sqrt(d), where
D_d=product P^floor(v_P(d)/2) and J_d=(d)D_d^-2 is integral squarefree.
It need not be principal. Its exact discriminant is4^n*disc(K)^2*N(J_d).
Factor its radical and apply actual Buchmann--Lenstra Theorem1.2/proof1.3;
this pays maximal orders uniformly in expanded degree. Weighted reset then
gives H_L(beta0)<=4H(a)+6H(d)+3logDelta+7n². Trace and root extraction give
the stated64bound. This applies at rational leaves too.

KEEP rational expanded output: arbitrary integer denominator clearing can
spoil the absolute height slope. Total encoded coordinate length has an
extra degree factor, charged only as workspace/runtime. The reset changes
the old point and may change its upper squareclass; it preserves the required
normclass and valid isotropy. No prescribed congruence is promised. This
closes the witness lemma only; coupled U/C/E batch proof is still under review.

One-tag gluing paid audit disposition: Fable ReadTimeout, EMPTY/reaped,
final billing UNKNOWN. Streaming0.126700USD is partial and excluded from
priced totals. No retry and no findings. Thus neither of the two new paid
stress tests is a completed audit. The parent and independent internal full
proofs, not their labels or absence of findings, determine the compiler gate.
The global UNKNOWN-bill count becomes SIX at the next ledger milestone.
