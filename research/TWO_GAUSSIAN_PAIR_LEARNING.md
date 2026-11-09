# Learning two arbitrary fermionic Gaussians from copies

REVIEWED WRITTEN POLYNOMIAL-COPY/BIT LEARNER, 7 November2026.
Independent AI exact/core/composition and source reviews, plus checked Claude
proof audits, support the derivation below. No human peer-review, formal
verification, novelty, quantum execution, classical-input speedup or general
Gaussian-rank claim.

## Selection and native contract

The question is whether every normalized coherent sum of TWO unknown pure even
fermionic Gaussian states can be learned from IID copies in polynomial(n,
1/epsilon,log1/eta) copy and BIT cost. Physical Majoranas/Jordan-Wigner encoding
and ordinary circuits are known. No branch description, inverse, overlap,
minimum amplitude or eigengap is supplied. Output a preparation circuit within
trace distance epsilon with failure at most eta. Both coefficients complex;
near-cancellation is allowed. This strictly differs from a promise of two
occupation strings in a shared Gaussian basis. We currently restrict the
statement to EVEN input; no uncharged parity/frame advice is used.

Independent selection: audits/reviews/2026-11-07-two-gaussian-selection.md.
Corpus been-tried and baselines preceded actual primary reads. The algebraic
screens (rational quadratic-form equivalence and finite-algebra decomposition)
already have factoring-based or randomized polynomial classical algorithms;
general finite-algebra automorphism is NOT thereby solved. The high-impact
Legendre/OPI/DCP alternatives currently lack a new paid operation. Here the
covariance/pairing operation is concrete, and Boutin--Bauer2105.01088 SecII.C
and Bravyi--Gosset1609.00735 motivate Gaussian superpositions independently.
This does NOT prepare impurity ground states or prove they have rank two.

Expected benefit: polynomial reconstruction of this succinct quantum-state
class, rather than unrestricted exponential-dimensional tomography. Supplied
Gaussian descriptions already permit classical Pfaffian/overlap calculations;
the parameter reconstruction processing is classical; copy measurements and coherent sequential compression are quantum operations. Fixed-small-mode
Gaussian compression and supplied-frame bounded-bond tomography are required
baselines. There is no classical-input quantum computational separation.

Resources proposed: O(n4) degree2/4 Majorana means, polynomial spectral linear
algebra and Gaussian rotations, followed by bounded-memory sequential
measurements on fresh copies. Falsifiers: nonzero cross-pair covariance,
incorrect parity/normal form, degenerate quartic data far from a usable
fallback, exponentially unstable normalized branching, or unpaid sequential
postselection. No implementation is admitted before uniform composition.

## Exact paired form and covariance

By an analysis-only inverse of the first Gaussian and Bloch--Messiah for the
second, there is a hidden even Gaussian frame with

 psi = [alpha |0...0> + beta tensor_j(c_j|00>+s_j|11>)] / sqrt(N),
 c_j,s_j>=0, c_j²+s_j²=1,
 N=|alpha|²+|beta|²+2Re(alpha* beta) product_j c_j >0.

Any remaining unpaired mode is vacuum; fully occupied pairs are allowed.
This is a proof normal form, not an available circuit. See primary pairing
0810.4772, SecII.C equations13--15. Opposite branch parities are not covered.
Define x_j=c_j², P_j=product_{l!=j}x_l and A=|alpha beta|/N.
Logical pair j has density matrix rho_j, with

 det rho_j = A²(1-x_j)(1-P_j),  nu_j²=1-4det rho_j.

Every cross-pair Majorana bilinear has zero expectation by pair parity.
Its real4D covariance block has eigenvalues +i nu_j and -i nu_j each twice;
all four singularvalues equal nu_j. Common pure modes have nu=1. For j!=k,

 nu_j²-nu_k² = 4 A² (x_j-x_k)(1-R_jk),
 R_jk=product_{l!=j,k}x_l.

These denominator-free products cover zero overlaps. With A>0, equality
means x_j=x_k or R_jk=1 (at most two active pairs). Thus exact covariance
identifies different pair-angle groups except a <=4physical-mode case.

## Uniform collision lemma, including cancellation

Let a=|alpha|²/N,b=|beta|²/N and m=min(a,b), so m<=A. Changing the branch
with smaller normalized coefficient from v to v' changes the normalized
state by at most 2sqrt(m)||v-v'|| (when the new vector is nonzero; a bound
<1 guarantees that). Swapping which branch is the reference preserves the
physical pair spaces and relative angles; it need not preserve the original
choice of vacuum. Therefore "merge" means relative-angle merge, not keeping
the original vacuum coefficients/frame fixed.

For theta_j in[0,pi/2], x_j=cos²theta_j,
 (theta_j-theta_k)² <= (pi²/4)|x_j-x_k|.
Changing one angle to the other therefore has squared Euclidean state error
at most pi² A |x_j-x_k|. Making every pair outside{j,k} inactive has squared
error at most 8 A(1-R_jk). Their product is at most

 2 pi² |nu_j²-nu_k²|.

These bounds remain uniform as N tends to zero: A also enters the observed
gap quadratically. They are statements about the native normalized state,
not bounded individual coefficients. Either small-gap states are close to
an angle merge, or they are close to the <=4mode Gaussian-compressible class.

For simultaneous merging, suppose the state is farther than a0 from EVERY
<=4mode Gaussian-compressible state. Then A(1-R_jk)>a0²/8 for EVERY pair.
Consequently A|x_j-x_k| <= 2|nu_j²-nu_k²|/a0². If each spectral cluster
has squared-covariance width w, change every angle in it to one representative.
The tensor-product branch error squared is bounded by the SUM of squared
angle changes; use the same smaller branch throughout. Total squared state
error is <=2 pi² n w/a0². This removes the alternating-dichotomy/chain issue.
The complementary case must be handled by an independently constructed and
validated small-core candidate; a gap alone cannot select the right branch.

## Equal-angle group: exact positive pairing signal

Consider k>=2 identical-angle logical pairs in one true covariance group.
They are permutation-symmetric, including after tracing outside pairs.
Apply the SAME logical SU2 rotation within every pair so its one-pair density
matrix becomes diagonal. This is an even Gaussian operation in each pair.
Then the group covariance is nu Jstandard. For nu>0 this complex structure
is determined by the covariance; remaining changes are passive U(2k).
In that complex basis put p=<n_j>, q=<n_i n_j>, i!=j, and
 z=<sigma_i^+ sigma_j^->. The logical two-pair density has no antisymmetric
component, hence z=p-q>=0 (real). On physical Lambda² C^(2k), the ordinary
number-conserving two-particle RDM is

 R2 = q I + z |Omega><Omega|,
 Omega=sum_j |2j-1,2j>,  ||Omega||²=k.

Reason: an unpaired two-particle diagonal has value q; a true paired
diagonal has p; pair-to-pair entries are z; other entries vanish by pair
parity. So the isolated eigenvalue gap is k z, and the top eigenvector
recovers the skew pairing form up to phase whenever z>0. Normalize and
polar-round the skew form, then unitary skew-Takagi gives a physical pair
basis. Its compact symplectic ambiguity preserves BOTH Gaussian branches.
No unknown Gaussian inverse or Lie-algebra decomposition is supplied.

If z=0, the group is supported on vacuum/full occupation: E[L(k-L)]
=k(k-1)z and L(k-L)>=k-1 outside{0,k}. More generally the probability
outside that cat subspace is <=kz. Thus small signal permits a quantified
cat projection; every passive basis preserves its two endpoint states.
A small quartic gap is not automatically an algorithmic obstruction.

## Near-zero covariance orientation

For a group of k>=3 equal-angle pairs c, let r in[0,1] be the overlap of
all outside pairs. Since A<=1/[2(1-r c^k)], the determinant identity gives

 nu >= c(1-r c^(k-2))/(1-r c^k) >= c(k-2)/k >= c/3.

The first inequality follows by subtracting the maximal determinant from1:
its numerator is (c-r c^(k-1))². The second uses monotonicity in r and
(1-c^(k-2))/(1-c^k)>=(k-2)/k. If c=r=1 the state is a single Gaussian and nu=1; the zero-normalization
case is excluded. Other endpoint lower bounds follow by continuity.
Thus small nu implies small c. Replace those c's by0: overlap of the two
full branches was already <=c^k, so normalized coefficients are bounded
and state error is O(sqrt(k)c). The reduced group becomes a vacuum/full
cat mixture. For 2k>=6 modes its connectedquartic is 4p(1-p)W(J), as in
the reviewed two-Fock note; small covariance makes p close to1/2, giving a
constant nonzero top gap. Recover J using that quartic even when C alone
cannot orient it. Groups of k<=2 have at most4physical modes and can remain
as constant-dimensional blocks in the final tomography.

## Uniform composition and precision hierarchy

The exact and composition reviews cover the full written learner below. All branch-dependent objects below are analysis witnesses;
the algorithm only uses measured moments, matrix operations and fresh copies.
Let 0<epsilon,eta<1, n>=5 (n<5 uses constant tomography), and put

 t=epsilon²/[10^8(n+1)²],  B=10^6(n+1)^20,
 a0=(t/B)², h=t/B, tau=(t/B)²,
 b=t*h*tau/B^6, w=(a0*b/B)², delta=b*w/B².

Every quantity is an explicit polynomial precision. Estimate all degree2/4
Majorana means to entry error delta, with aggregate failure eta/10, using
O(n4 delta^-2 log(n/eta)) independent bounded measurements. Matrix arithmetic
and orthogonal gates use smaller polynomial rounding error. There is no
unknown amplitude, overlap, eigengap, or exact-real input in this prescription.

Construct TWO candidates with capped clocks. Outside its guaranteed case,
each branch may return a fixed trivial preparation; fresh final validation
selects a successful candidate without requiring a structural decision.

### Candidate 1: small Gaussian core

Diagonalize measured C, keep its four most impure canonical modes, and project
the other modes onto their more likely occupations after the learned Gaussian
rotation. Tomograph the remaining four-mode pure conditional state, charging
every failed projection, then output the inverse-rotation preparation. If the
original state is a0-close to ANY four-mode Gaussian-compressible pure state,
Weyl and ||Cpsi-Cphi||op<=2n a0 give discarded expected excitations
O(n² a0+n² delta). Markov/union gives projection failure at most that value,
and pure-state disturbance O(n sqrt(a0)+n sqrt(delta))<=t. The conditional
state needs no promised branch description. Conditional sampling succeeds
with probability >=1/2 in this case; cap requests and ABORT otherwise.
Approximate tomography and compiled-gate errors can be set <=epsilon/100.

### Candidate 2: covariance groups and model perturbation

Assume the input is farther than a0 from EVERY such four-mode state. Form
H=-Ctilde². Cluster its sorted real eigenvalues by joining adjacent gaps<=w,
including a sentinel at1; discard the sentinel cluster as almost-pure modes.
Under entry error delta, a true fourfold pair value cannot split. Between
retained clusters the true spectral gap is >=w/2; each cluster has width
O(nw). The sentinel cluster has purity defect O(nw), so Gaussian projection
there costs O(n sqrt(w)). Retained block dimensions are multiples of4.

Grouped Davis--Kahan plus orthogonal subspace alignment provides an analysis
rotation taking the true groups to the estimated groups with Frobenius error
O(n^3 delta/w). Its Gaussian lift changes any state by another polynomial
factor (generator norm<=sqrt(n) times its skew-matrix Frobenius norm).
Align the exact model and merge all relative angles within each retained
cluster BEFORE projecting the almost-pure sentinel group. This keeps the
collision bound on the original coefficients; the later high-success
projection only changes the comparison state by its measured disturbance. The simultaneous collision bound gives state error
O(n sqrt(w)/a0). Including almost-pure projection and finite arithmetic,
all this is <=b, using the padded factor B above. Thus in the LEARNED
cluster spaces there exists a rank-two paired model within b of the input.
The algorithm never computes its angles or branches.

The square root/polar decompositions below need only polynomial accuracy.
An entrywise error e in degree<=4 moments gives operator error O(n² e) in
any pair-index matrix; orthogonal basis changes and comparison to a b-close
state add at most fixed polynomial factors. A deliberately loose bound B
covers each of the matrix assembly, grouped subspace alignment, Gaussian
lift and polar-rounding estimates used here. The complete high-nu chain
below is bounded by B^4 b/(h tau); low-nu cost by B h. The independent composition review explicitly traces these powers;
they are not inferred from a numerical stability test.

For a group of k<=2 pairs, choose any SO basis and retain the entire <=4mode
quantum block. Do NOT tomograph its reduced state independently.
For k>=3, estimate its covariance norm nu. Use threshold2h:

- Low-nu branch: true nu<=3h. The lemma gives c<=9h. Replacing that group
  by its orthogonal-branch cat changes the state by O(sqrt(k)h), with bounded
  normalized coefficients. Its reduced covariance has |2p-1|=O(sqrt(k)h),
  so 4p(1-p)>=1/2. The connectedquartic on 2k physical modes is aW(J),
  with top gap a(2k-2)>=k-1. Recover its top skew vector, normalize/polar-round
  to J, and choose any canonical basis of J. Moment contamination, lift and
  all such group errors together are <=B h. No phase was measured by this
  operation; global phase recovery is deferred to coherent tomography.
- High-nu branch: true nu>=h. Polar-round the measured covariance to its
  complex structure J and take any compatible complex basis. The nearest
  true complex structure is transported to it by an SO rotation with error
  O(poly(n)b/h). In that basis assemble the number-conserving R2. If its
  measured top-to-next gap is <=2tau, the true gap is <=3tau, and projecting
  this group to vacuum/full occupation loses probability <=3tau. If the
  measured gap exceeds2tau, the true gap is >=tau. Recover the top skew
  pairing form, polar-round it to skew-unitary, and pair v with Z conjugate(v)
  by orthogonal recursion. This is matrix multiplication/Gram--Schmidt of
  polynomial size. The aggregate high-nu orientation/pairing error is
  <=B^4 b/(h tau), smaller than t. All cat projections commute; total failure
  <=3n tau, so their total pure-state disturbance is <=sqrt(3n tau)<=t.

Proof order for the comparison state: first apply high-gap basis transports
on their disjoint groups (including covariance orientation). Then perform
the commuting small-gap cat projections. Their failure remains <=3n tau;
the hierarchy leaves slack for the orientation error. Make low-nu branch
replacements afterward. Projection of OTHER groups changes coefficients,
but not a low group's relative angle c. Its two outside branch factors can
be normalized even when they are local GHZ superpositions; their overlap
has modulus<=1, so the full branch overlap is still<=c^k. The coefficient
bound and O(sqrt(k)c) replacement remain valid. Its branch-defined complex
structure J is unchanged by those outside projections. No recursive group
error or square-root loss is hidden in this ordering.

Why polar/basis ambiguity is harmless: if two real complex structures are
close, a near-identity orthogonal transporter exists by polar decomposition
of their intertwiner I-Jhat J. For unitary skew forms Z,Zhat close in
Frobenius norm, their quaternionic structures similarly admit a close
unitary transporter. After that transporter, ALL choices of exact pairing
basis differ by the compact symplectic stabilizer, which preserves both
identical-pair Gaussian branches. The proof needs closeness of a transporter,
not continuity of a particular degenerate eigensolver's eigenvectors.
The normalized top R2 vector reshapes to Z/sqrt(k); multiply by sqrt(k)
before polar rounding. This polynomial factor is charged.
More explicitly, for either real complex structures or antiunitary quaternionic
structures, M=I-Jhat J (respectively I-Zhat conjugate(Z)) is near2I and
intertwines the two structures. Its polar unitary/orthogonal V also
intertwines, with ||V-I||F=O(||Jhat-J||F) or O(||Zhat-Z||F).
A skew matrix's nonsingular polar factor remains skew by its unitary
skew-Takagi form. These are finite matrix operations with singular values
bounded away from0 in the admitted branch.

Track basis orientation: if an O frame has determinant-1, implement its SO
part and a KNOWN Majorana Pauli reflection, permitted by the ordinary qubit
circuit input model, and undo it in the output preparation. Occupations and
parities are tracked; no branch parity is silently changed or supplied.
This is not a claim restricted to parity-preserving physical gates only.


Order each recovered pair adjacently and each constant-size or cat block
contiguously, using charged fermionic swaps. Ordering learned modes this way
leaves the target within O(t) of an
MPS of bond dimension at most8. A recovered pair has fixed local dimension;
a <=4mode group is kept whole. A projected large group contributes a local
vacuum/full GHZ factor in each of the two global product branches, raising
bond rank by at most a factor2. A cut inside a four-mode block has rank at
most4 per branch. Hence8 is a safe bound; no branch parameters are advice.

### Paid known sequential endpoint, including global phase

This is the known local-unitary tomography mechanism of Landon-Cardinal,
Liu and Poulin, arXiv1002.4632, actual method steps1--4, Accuracy section,
and Local measurements degeneracy discussion (retained txt60--180).
That primary explicitly retains final-memory GHZ phase and postselection.
We specialize it to bond8 and give the quantitative gap-free/capped-sampling
interface below. This endpoint is reused machinery, not a novelty claim.

Given fresh copies of a state within d0=O(t) of an unknown pure qubit MPS
with bond<=8 in the learned order, keep a three-qubit coherent memory.
Tomograph memory plus next qubit (four qubits); choose a unitary mapping
the largest eight-dimensional density support into |0> times the memory.
Repeat, then tomograph the final memory. Earlier disentangling gates are
reapplied to each fresh copy; measure and CONDITION on the earlier discarded
qubits being zero. This is charged conditional sampling, not free postselection.

For the reference MPS, conditioning any earlier prefix preserves Schmidt
rank<=8 at every remaining cut. If actual prefix success is >=1/2, its
normalized conditional state is O(d0)-close to the reference's conditional
state (contractivity on unnormalized vectors and normalization). Thus the
conditional four-qubit density has rank8 tail <=O(d0). Tomography to trace
error t makes each chosen projection fail with probability O(d0+t).
Inductively the total failure is O(n(d0+t))<1/2. Obtain each tomography
sample using a capped geometric schedule (success>=1/2); Chernoff and a
union bound charge all copies and give failure<=eta/10. If a cap or a
measured success check fails, return the trivial candidate.

Quantitative endpoint bounds (independently audited, with compilation repair):
phase-align the reference so ||psi-phi||<=sqrt(2)d0. For every ACTUALLY
applied prefix W_j and zero-projector Pi_j,
 ||Pi_j W_j psi - Pi_j W_j phi|| <= sqrt(2)d0.
If actual success>=1/2, normalized conditional states have distance<=4d0;
the reference is nonzero when d0<1/2. This comparison is to the original
reference through actual gates, not to a recursively fitted state.
If rhohat is Hermitian trace1 with ||rhohat-rho||1<=Delta, Ky Fan gives
 tr[(I-Phat8)rho] <= tail8(rho)+Delta <=4d0+Delta,
without any eigengap or minimum Schmidt weight. Padding an actual rank<8
causes no problem. A compiled four-qubit unitary at operator error kappa
adds at most2kappa to that failure bound. Thus
 total failure <=(n-3)(4d0+Delta+2kappa).
Choose Delta<=2t,kappa<=t and final-memory pure-state error<=epsilon/100.
The hierarchy leaves d0<=10t and therefore success>=1/2 and final error
well below epsilon/10. Fresh copies use at most4N+O(log(n/eta)) attempts
for N successful conditional measurements, by Chernoff. The output uses
exactly reversed adjoints of the compiled prefix; no uncharged preparation
inverse appears. Reusing those gates cancels output inverse mismatch but
DOES NOT erase their compression error, which is the2kappa term above.

All later gates act only on the memory/future and never on discarded qubits.
For the final fixed unitary U, the entire successful branch is therefore
just projection of U|psi> onto zeros on all discarded qubits. Its normalized
state differs by trace distance sqrt(total failure)=O(sqrt(n(d0+t))).
Final pure-memory tomography and U inverse give a deterministic preparation
with this error plus its tomography/compilation tolerance, <=epsilon/10.
No proper-marginal determination is assumed: GHZ+/GHZ- phases survive in
this memory and are measured at the end. Postselection is only in learning;
the output circuit prepares the fitted memory and runs the inverse gates.

### Selection and resources

Estimate both candidates' fidelities on fresh original copies by their KNOWN
inverse preparation circuits and all-zero measurement, to additive
O(epsilon²) at failure<=eta/10. Select the better. One candidate is within
epsilon/10 in every native case; suitably small constants then make the
selected output epsilon-close. No inverse of the unknown preparation is used.
Allocate remaining failure to all matrix/measurement/tomography caps by
union bound. Candidate generation has no unbounded search.

The precision hierarchy is polynomial: b=t4/B9, w=t12/B24 and
 delta=t16/B35. The dominant raw copy count is
 O(n4 B70 t^-32 log(n/eta)); polynomial-size matrix work per measured entry,
Gaussian Givens compilation, constant-window tomography and conditional
sampling add polynomial overhead. This deliberately loose expression is
NOT a practical bound or an optimality claim. Finite gate angles need only
log(1/delta) plus polynomial(n) bits. The composition review checks these precision/rounding powers. No full
learner or statistical resource experiment was executed.

## Sources, reviews and Claude disposition

Primary PDFs/text/hashes: audits/sources/two_gaussian_learning/source.json.
Actual reads: impurity SecII.C equations4--5; Bravyi--Gosset Sec2 Gaussian
rank/Wick definitions; pairing Bloch--Messiah equations13--15; quadratic
MFCS2020 intro classical factoring comparison; finite-algebra2608.30340
intro explicitly states randomized expected polynomial classical baseline.
No abstract-only novelty inference. Source/normalization review is complete; historical priority remains UNKNOWN.

Claude inputs: audits/claude_inputs/2026-11-07-two-gaussian/.
Covariance Fable/high report completed; direct identities and cancellation-
uniform branch modification/product bound checked and accepted. "Unchanged
other data" was repaired to allow swapping the reference branch; its
pairwise-to-algorithm sentence does not pay the fallback or simultaneous
merging. The simultaneous bound above is a separate parent derivation.
Quartic Fable/high request ended max_tokens with NO report; no findings or
retry. Parent derived the positive R2 signal independently. The final four-bundle usage estimate is USD5.559080; none of the bundles
is a provider balance measurement.

Core exact/source reviews: audits/reviews/2026-11-07-two-gaussian-core.md
and 2026-11-07-two-gaussian-sources.md. Accepted exact positive signal,
explicit antiunitary basis extraction, near-zero bound, and even normal-form
scope. Both explicitly left uniform composition unpaid. Bravyi--Gosset
Eq25/28 require nonzero branch overlap; Eq24/27 use a phase-aware reference.
Do not invoke the inverse formula at zero overlap or omit relative phase.
Classical simulation under supplied descriptions retains its precision and
cancellation cost; exact identity is not a uniform numerical complexity bound.

One exact finite CAS control: audits/controls/two_gaussian_learning/control.py
and .json. Eight physical modes, three equal pairs plus one distinct pair:
R2 dimension15 has p=9/268,q=36/1675,z=81/6700, gap243/6700; the cat
failure243/6700 saturates the bound. After a nontrivial cross-group Gaussian
rotation, C² alone returns the rank12 projector (other multiplicity4).
Complex coefficients and rational near-cancellation verify the covariance
identity; zero-covariance cat gives scalar R2, and explicit coherent GHZ
compression preserves final-memory X=+/-1. The first test mistakenly asked
for nu>=1/3 in the cancellation case; exactnu=c/(1+c+c²)<1/3 refuted that
stronger test. The proved nu>=c/3 was unchanged and the corrected exact
identity passed. No fulllearner/noise/quantum execution or asymptotic inference.

Sequential Claude report: audits/claude_runs/2026-11-07-two-gaussian-sequential/.
Accepted the contraction/normalization, gap-free KyFan, prefix-success,
contiguous-block rank and final coherent-memory proof. Its statement that
same-gate reuse eliminates ALL compilation cost was repaired: actual prefix
compression failures still add2kappa; inverse mismatch cancels. Its small
window proper-marginal GHZ wording is only for proper windows; final-memory
phase acquisition is retained. No upstream-frame proof inferred from it.

Sixth primary source added: Landon-Cardinal/Liu/Poulin1002.4632,
audits/sources/two_gaussian_learning/mps_tomography.pdf/.txt. Its sequential
local-unitary method, final-memory GHZphase, postselection and polynomial
resources match this endpoint. Actual Accuracy discussion assumes subspace
estimation; the explicit KyFan/fresh-copy cap above pays the chosen uniform
interface. Do not count rediscovery of sequential MPS tomography as progress
beyond the new hidden-Gaussian-frame operation. Overall priority UNKNOWN.

Final composition review: audits/reviews/2026-11-07-two-gaussian-composition.md.
It bounds grouped alignment/lift by O(n^(7/2)delta/w), merge by
O(n sqrt(w)/a0), high-nu propagation by O(n8 b/(h tau)), and low-nu
replacement/quartic/lift by O(n6 h). These fit the displayed B bounds and
the cross-stage ordering above. Combined with the paid known MPS endpoint
and final candidate fidelity selection, this establishes the written
polynomial-copy/BIT algorithm for the EXACT EVEN rank-two input contract.
No arbitrary Gaussianrank, noisy/mixed source or physical parity-only-gate
extension is claimed. There is no minimum coefficient/gap/overlap promise.

Final Claude disposition: four terminal bundles, two substantive completed
reports (covariance USD1.611150; sequential USD0.568280), two empty max_tokens
requests (quartic USD1.657290; composition USD1.722360). Empty reports supply
NO findings and were not retried. Parent/internal independent derivations
supply the exact quartic and full frame review. Pass total USD5.559080;
aggregate41 reported estimates USD34.019700,20 completed reports, including
pre-owner-balance-anchor runs. No invoice or remaining balance is inferred.

Next question: compare independently motivated native algorithm mechanisms
again; this pass closes a concrete rank-two learning route, not the broad
Shor-level objective. Do not queue general-rank extensions or implementation
solely because this proof left them open. Any next experiment needs a new
native operation, prior/corpus baseline check and decisive falsifier.

Milestone verification PASS: current STATE fulltitle/Now/accountedrow matches
newest HANDOFF; mechanical entry present; all six primary PDF hashes verified;
all four scoped reviews read; four immutable Claude prompt/context snapshots,
terminal statuses and usage checked; exact control falsegates retained;
aggregate41/USD34.019700/20reports and scoped whitespace checks passed.
No fullsuite, unchanged-control rerun after final prose, Git commit or push.
