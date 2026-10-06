# Native DCP Projective Codes: Preserve The Target, Beat The Baseline

**LOCAL DERIVATION / REVIEW PENDING.** No new algorithm, accepted candidate,
full classical simulation, generic DCP no-go or independent theorem review.
This studies the existing native DCP source, not a new toy oracle problem.

## What Changed The Research Decision

Recent projective symmetry learning is a real technique, but applying its
stabilizer-output theorem to native phase packets does not itself recover a
DHSP shift. Many secrets have exactly the same output subgroup. Full coded
measurement records DO retain information, so discarding that route outright
would also be wrong. This workbench separates those two claims.

For a broad fixed binary self-orthogonal CSS measurement family, the complete
source-averaged chi-squared signal has an exact code-shortening formula. It is
bounded above by ordinary Bell pairs with the same number of logical rows and
no more consumed source states. Searching for a "better" fixed code by that
metric alone therefore has a ceiling already achieved by a known primitive.
This is a signal-metric comparison, NOT Blackwell dominance, sample-complexity
dominance, efficient likelihood inference or complete classical dequantization.

The surviving research question is narrower and more consequential: can a
RETAINED-REGISTER decoder, public-label-adaptive code or raw-transcript decoder exploit
structure that this fixed-source moment calculation does not capture, with a
uniform compiler and better total costs than sieving/classical inference?

## Literature Ingredient And Its Limits

[Holt--Subramanian, section9](https://arxiv.org/html/2609.38085v1) linearises
an abelian projective action using a code matrix M. The checked conditions
include MM^T=0, target-preserving rank, and extra phase-neutrality conditions
when Bose rather than anyonic sampling is used. An efficiently implemented
gauge is assumed. Theorem9.17 learns a symmetry subgroup of a state from
copies; it is not a hidden-element decoder for arbitrary phase packets.
Lemmas9.2-9.5 and the adjacent theorem/proof were inspected. Full number-theoretic
code constructions and the complete paper have not been audited.

The calculations below are local source-specific derivations, not attributed
paper theorems or novelty claims. The prior [StateHSP scope screen](STATE_HSP_DHSP_SCOPE.md)
already separates normal-core recovery from full nonnormal target recovery.

## Native Source And Exact Stabilizer Loss

Let N=2^n>=8. A consumed native sample has a public independent uniform label
k in Z_N and one qubit

`|phi_(k,s)> = (|0> + exp(2*pi*i*k*s/N)|1>)/sqrt(2)`.

The standard full DHSP oracle-to-phase-state bridge uses one oracle query per
sample and records its measured label. This workbench takes those samples as
inputs; it does not supply reusable phase oracles, inverse sample preparation,
unknown-state cloning or selected identical labels for free.

For theta=2*pi*k*s/N, the Pauli expectations for P(a,b)=Z^a X^b are

`<I>=1, <Z>=0, <X>=cos(theta), <ZX>=-i*sin(theta)`.

The nonidentity anyonic stabilizer is X if 2ks=0 mod N, ZX if 4ks=0 mod N
but 2ks!=0, and absent otherwise. On a product packet, a tensor Pauli has
unit expectation modulus only when every nontrivial local factor stabilizes
its corresponding qubit. Thus the full phaseless stabilizer is the direct
product of these local groups.

For fixed public labels, ALL ODD secrets have exactly the SAME group: the
condition is determined by the label's valuation, and eligible labels are
0,N/4,N/2,3N/4. Even revealing that group perfectly cannot identify the odd
part of s. More generally it reveals only a coarse valuation class; eigenvalue
phases and the full measurement distribution are different data and must not
be silently substituted for a phaseless subgroup.

For a single nonstabilizer equatorial qubit the gap is
1-max(|cos(theta)|,|sin(theta)|). A worst-case label k=1,s=1 gives
1-cos(2*pi/N)<=20/N^2. This is a WORST CASE, not a typical-packet claim.
Typical independent polynomial-size packets can have inverse-polynomial
gaps and still share a target-independent stabilizer. Missing target data,
not necessarily an exponentially small typical gap, is the direct problem.

## A Dihedral Action Is Not Automatically An Abelian Projective Action

At a fixed irrep label k the known rotation and reflection actions include

`R_k=diag(exp(2*pi*i*k/N), exp(-2*pi*i*k/N)), X`.

Their commutator is diag(exp(4*pi*i*k/N),exp(-4*pi*i*k/N)). It is scalar
IFF 4k=0 mod N. A projective action of an abelian group has only SCALAR
commutators. Cancelling a scalar cocycle therefore cannot repair this generic
noncentral dihedral commutator. Only four of N labels meet this particular
criterion, and their coarse action does not encode the full shift.

This excludes that direct reinterpretation, not every encoded subspace or
new representation. A tensor product of these same actions remains noncentral
unless every factor is scalar, on the FULL tensor Hilbert space. Restricting
to a special encoded subspace can escape; its source preparation, selection
cost and retained target information then require a new reduction. Known
label-combining sieves are a baseline for precisely such escapes.

## Source-Faithful Coded Measurement

Take r independently supplied native registers; repeated label values are allowed.
Fix a full-rank
h-by-r binary matrix M BEFORE these labels are drawn, with MM^T=0 over F_2.
Let C=row(M). The known commuting Pauli action is

`R_M(a,b)=Z^(aM) X^(bM)`, a,b in F_2^h.

It is a genuine linear representation of F_2^(2h). A uniform control register,
controlled known Paulis and Boolean Fourier readout give 2h classical output
bits. Equivalently measure the 2h commuting X/Z row generators. Known Clifford
cost is at most 2*sum(row weights) two-qubit gates plus4h Hadamards in the
purified construction. State generation consumes r full-oracle queries via
the usual bridge. No postselection or secret-dependent rotation is used.

This is NOT an invocation of the literature's rho^tensor(r) stabilizer guarantee:
the physical qubits can have different measured labels and different states.
The known commuting measurement is still legal. Claiming identical conditional
states would require obtaining repeated labels or a new paid conversion.
Conversely, repeated-label copies are not needed merely to execute this raw
joint measurement on native inputs. Both distinctions are retained.

For u=aM,v=bM, expectation is zero unless support(u) is contained in support(v).
Otherwise it is

`F_(u,v)=(-i)^wt(u) product_(i in u) sin(theta_i)
                         product_(i in v\u) cos(theta_i)`.

Self-orthogonality makes wt(u) even in this case, so F is real. The COMPLETE
probability law is its normalized Boolean Fourier transform over (a,b), with
every output retained. The purified statevector executes that same law.

Two-copy M=[1,1] is linear but not generally Bose phase-neutral: on two +Y
states (ZX)^tensor2 has eigenvalue -1. Four-copy M=[1,1,1,1] changes it to +1.
The latter satisfies the extra doubly-even condition; replacing it with two
copies without using phase-aware/difference sampling changes the theorem
output. This is not a reason to reject ordinary Bell RAW records.

## Exact Native Cross-Secret Kernel

Use the reference D0 with the SAME public uniform labels and a uniform 2h-bit
output. For a secret of order>=4 define f_s=4^h*p_s and g_s=f_s-1. Let
K(s,t)=E_labels[4^h sum_y p_s(y)p_t(y)].

Parseval and independent cyclic-character averages give

`K(s,t)=1`, t not equal to s or -s mod N,
`K(s,s)=K(s,-s)=sum_(v in C) 2^(dim(C_v)-wt(v))`,

where C_v={u in C:support(u) contained in support(v)} is the shortened code.
To see the first identity, every nontrivial coefficient contains at least one
cosine/cosine or sine/sine character product; its average vanishes outside
the negation orbit. At t=s the squared moment is 2^-wt(v). At t=-s the sine
sign is (-1)^wt(u)=1. The number of eligible u is2^dim(C_v). Order-one/two
secrets have different diagonal moments and are not included in this formula.

Public labels are retained in the joint-record comparison; this is NOT the
uninformative marginal obtained by hiding them from the learner. Orthogonality
establishes an identifiable statistical family, not an efficient decoder.
The raw likelihoods can differ even when every odd secret has the same Pauli
stabilizer. Literal controls exhibit this distinction.

## Bell-Pair Signal Ceiling: A Short Exact Proof

Row-reduce and permute columns to write M=[I_h|A]. Self-orthogonality gives
AA^T=I_h, hence rank(A)=h and r>=2h. For b in F_2^h let v=(b,bA).
Any u in C_v has first h coordinates supported on b, so dim(C_v)<=wt(b).
Therefore

`2^(dim(C_v)-wt(v)) <= 2^-wt(bA)`.

Choose h independent columns A_P. The map b->bA_P is a bijection, and
wt(bA)>=wt(bA_P). Summing,

`K(s,s) <= sum_b 2^-wt(bA_P) = (3/2)^h`.

Disjoint Bell pairs M=[I_h|I_h] attain equality with r=2h input states.
Disjoint four-copy rows have K=(9/8)^h. Extended Hamming[8,4] gives
K=45/16, centered signal29/16, compared with Bell's K=81/16 and65/16.
The statement covers EVERY full-rank binary self-orthogonal code in this
family, not only those named examples or a numerical search.

An even stronger outcome-signal comparator is INDIVIDUAL X readout of2h native
qubits: with the same2h classical output bits and no entangling measurement,
its kernel is(3/2)^(2h). A proposed-secret likelihood is a product of2h cosine
factors and is classically evaluable in O(h) arithmetic, but efficient full
secret SEARCH does not follow. This is classical processing of legitimate
quantum measurements, not a classical phase-state preparation simulator.

Do not optimize fixed-code distance/rate solely to enlarge this already-bounded
moment. A claim of greater research leverage needs another metric and an actual
decoder/source reduction. No theorem here orders TV, mutual information,
likelihood computability, noise robustness or higher moments. Non-CSS actions,
public rotations and current-label-adaptive codes are not covered automatically.

## Retained Registers Refute A Broader Interpretation

The preceding ceiling concerns CLASSICAL outcomes ONLY. Projecting on 2h
commuting checks leaves r-2h encoded qubits when r>2h. The complete instrument
has blocks rho_(s,y)=Pi_y|psi_s><psi_s|Pi_y; it is not just a draw from p_s(y).
With the SAME public labels retained, the source-averaged quantum collision
relative to a maximally mixed input reference is

`J_quantum = 2^r E_labels sum_y Tr(rho_(s,y)^2)
           = 2^(r-2h) K(s,s)`.

This includes the true unnormalized branch weights. It can exceed Bell's
classical score because quantum registers remain, NOT because new information
was created. The untouched r-qubit pure source has collision2^r; the measured
instrument is a channel and cannot improve pairwise distinguishability. The
report includes the original-input trace distance to prevent that overclaim.

An attempted counterexample with a disjoint four-copy row FAILED: the all-one
codeword is present. For equatorial product states X_all maps s to -s up to a
global phase. If all-ones lies in C, X_all is one of the measured stabilizers;
each branch then has identical density for s and -s, even with remaining
qubits. Bell pairs have that property too. This is retained as a negative
control, not hidden by choosing a different successful example.

A genuine counterexample uses overlapping rows

`M = [[1,1,1,1,0,0], [0,0,1,1,1,1]]`.

They are full-rank, mutually orthogonal and doubly even, but all-ones is NOT
in their code. The instrument leaves two encoded qubits. Across EIGHT
unfiltered native-label seeds43011-43018, all classical outcome laws for s1
and s31 at N32 agree, while seven retained quantum outputs differ. Their
trace distances range approximately .351-.897 in those seven cases; the
remaining degenerate source gives zero and is also retained. None exceeds
the original input trace distance. Independent replay verifies the FULL
unnormalized branch differences, not averaged normalized branch fidelities.

### Concrete Nonlinear Logical State

For this overlapping code, consider the branch where all four generator
measurements are zero. Its probability remains charged; other branches are
kept in the parent instrument. Define theta_i=2*pi*k_i*s/N, and for p in{0,1}

`C_p=product_(j=0..2) cos((theta_(2j)+(-1)^p theta_(2j+1))/2)`,
`S_p=product_(j=0..2) sin((theta_(2j)+(-1)^p theta_(2j+1))/2)`.

In a PUBLIC Clifford logical basis, its unnormalized state is

`exp(i sum_i theta_i/2)/4 * sum_(p,a) (C_p+(-1)^a i S_p)|p,a>`.

The measured Z relations set all three pair parities equal to p, without
measuring p individually. Within each pair write bits(r_j,p XOR r_j); the
remaining logical a is r_1 XOR r_2 XOR r_3. Averaging the four known X-code
translations gives the displayed cosine/sine products. Each logical basis
vector is the normalized four-element orbit with fixed p,a. This is a known
linear Clifford decoding, not an unknown phase inverse.

All eight branch controls execute that physical orbit projection and compare
every complex logical amplitude with the formula. Branch probability is
`(C_0^2+S_0^2+C_1^2+S_1^2)/8`, not one; its IID source average is1/16 for
nonzero secrets by the mean-zero character expansion. No per-instance lower
bound, flat envelope, reusable unknown-phase unitary or new decoder is claimed.

This supplies a concrete next target: nonlinear phase/amplitude transport with
coherent pair-parity information retained. It may still be a repackaging of
known partial stabilizer/phase-fusion primitives; compare a sequential
label-combining construction before claiming novelty. A signal or tangent
product is not a Shor-level algorithm. The fixed-outcome SQ gate below does
NOT exclude using these encoded quantum registers in subsequent operations.

## Scoped Statistical-Query Screen, And Its Escape

Representatives of the order>=4 negation orbits have orthogonal centered
densities with norm d=K-1<=(3/2)^h-1. For a bounded ONE-RECORD expectation query,
Bessel gives sum_orbits |E_Ds(phi)-E_D0(phi)|^2<=d. At tolerance tau, at most
floor(d/tau^2) secrets force a response outside the reference tolerance.
Following an adaptive reference-answer path, T such queries have uniform-orbit
identification success at most

`min(1,(T*floor(d/tau^2)+1)/((N-2)/2))`.

The reasoning is the same scoped expectation-query idea as the prior
[Bell inference audit](DCP_BELL_INFERENCE_KERNEL.md), applied to this different
uncollimated native-code interface. Raw records, symbolic equation solvers,
joint multirecord queries or current-label-dependent measurement selection are
NOT excluded. Nor can this bound be advertised for arbitrary growing h: when
h is proportional to logN, d can grow exponentially and the bound becomes
VACUOUS. The report preserves that countercontrol. Query count alone is not
a classical time bound, and no classical phase-state simulator is supplied.

## Attempts To Kill The Conclusion

- **Bell dominates complete protocols:** false. The bound is outcome-only.
  Overlapping-code quantum remainders distinguish secrets with identical raw
  outcome laws; full register protocols and costs must be audited separately.
- **The stabilizer is trivial, so all records are useless:** false. Full native
  coded laws for odd s1 and s3 differ. Preserve their known labels and outputs.
- **A clever fixed code beats Bell:** it cannot beat the derived chi-squared
  ceiling under these premises. It could improve another inferential/resource
  property; demonstrate it against matched Bell and individual-qubit baselines.
- **Choose M after reading the labels:** that escapes the averaging premise.
  It is a substantive direction, not a candidate automatically ruled out.
  Charge selection/search complexity and compare to classical subset-sum,
  meet-in-the-middle and Kuperberg/Regev label-combining baselines.
- **Use more rows:** the SQ bound may become vacuous. That does not produce
  a decoder; a product of Bell blocks already realizes the signal growth.
  Full likelihood/information/computational criteria remain separate.
- **The theorem uses copies, so native implementation is impossible:** false
  for the raw commuting measurement. Its native distinct-state execution is
  explicitly simulated. Only transferring SAME-STATE stabilizer guarantees
  without their premise is blocked.
- **Poor gap is the reason:** not generally. Worst-case small gap and typical
  polynomial gap coexist with target-independent subgroup output.

## Evidence And Next Work

FOLLOW-UP: `DCP_PATH_CODE_FUSION.md` now derives EVERY syndrome of the concrete
overlapping primitive, supplies its explicit linear-cost Clifford compiler,
and proves the measured-p comparator is ordinary pair fusion plus Fourier
parity checks. The sign signal also survives that comparator; do not cite it
as requiring common-parity coherence. Coherence can improve the statistic,
but no new decoder follows. Prefer the follow-up's revised next-work decision.

Twelve purified controls cover disjoint Bell and quartic codes plus the extended
Hamming code, unfiltered seeded native labels, two odd secrets, and every output.
An independent JavaScript checker enumerates72 shortened-code terms, replays
720 full probabilities,512 exact odd-secret signatures,148 retained-register
branches,32 unnormalized complex logical amplitudes and five growing ledgers.
Ten quantum-remainder controls retain two
failed all-ones examples and ALL eight overlapping-code source draws. Eight
native logical branch formulas retain charged probabilities and complex amplitudes.
Tests also exhaust ALL small two-row self-orthogonal codes at width6, actual
scalar-commutator conditions, native label-averaged cross kernels and the
two-copy/four-copy Bose-phase counterexample.

Verified:24 new focused tests; combined five-file mathematical regression:
87 passed in2.83s. Python/JS syntax, strict JSON and
scoped whitespace checks pass. No full repository suite or CLI validation is
claimed; production integration remains delegated.

New module/tests `dcp_projective_code_admission`; report under phase_workbench,
independent checker under certificates, matching hypothesis/source-audit
records. Exact code moment enumeration is capped; the symbolic Bell bound
scales without enumerating all outcomes. Physical compiler export, full
production CLI/registry validation and independent theorem review are pending.

Gemini: integrate as target-preservation/known-baseline admission, NOT an
accepted algorithm or complete dequantization. Expose both useful raw records
and failed stabilizer-output transfer. GPT: target the concrete overlapping
encoded-state transport, a label-adaptive mechanism or structured raw decoder, with a proved
natural source law and costs. Another fixed-code benchmark is not the next
high-impact step.
