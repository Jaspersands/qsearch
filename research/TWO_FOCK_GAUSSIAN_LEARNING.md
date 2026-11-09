# Two Fock branches in an unknown Gaussian basis

REVIEWED WRITTEN POLYNOMIAL-COPY/BIT LEARNER (7 November2026).
No execution, novelty, sample optimality or quantum/classical separation claim.

## Question and selection

Can every parity-definite pure state supported on at most TWO occupation
strings in an unknown fermionic Gaussian basis be learned efficiently, with
no branch-weight or spectral-gap promise? This is a native special case of
Sen's explicit unknown-Gaussian-Fock learning question, not a source made
from a residual decoding obstruction. It targets a preparation description
for experimentally supplied states rather than a classical search speedup.

The independent comparison considered the random-F3 subset-sum threshold,
explicit central-simple-algebra isomorphism, scalar OPI, lattice Gaussian
cooling, and Jones evaluation. Corpus and actual-source checks found the
first two already extensively treated here; actual Amitsur v2 removes the
abstract's old irreducibility heuristic. The other three supplied no new
paid operation beyond their recorded baselines. Clifford-scrambled Gaussian
learning supplies a Bell-shell constraint but no paid frame extractor.
Here a concrete spectral operation supplies both frame and phase recovery.

The screened alternatives retain their native contracts:

| Direction | Input/output, operation and resource target | Baseline, proof obligation and cheapest falsifier |
|---|---|---|
| Random F3 zero sum | Explicit IID n-by-m matrix, return nonempty Boolean kernel vector; published CLZ/quotient-decoder Fourier filtering targets polynomial time at every fixed m/n²>0. | Published classical n²/3 threshold and Wagner tradeoff; announced0.1022 constant lacks a complete proof in the checked source. No new paid decoding operation emerged; existing ternary/SDE audits already cover this threshold. |
| Split central-simple algebra | Structure constants of A isomorphic to M_d(K), return compact splitting map; Amitsur cocycle/S-unit arithmetic targets polynomial quantum BIT time. | Actual2307.00261v2 already supplies the composition, unlike stale abstract metadata. The old irreducibility heuristic is not a new blocker; existing local audit pays the output interface. |
| Scalar OPI | Full random half-set tables, return degree<k polynomial at the DQI target score; affine-flat constraints and RS linear solving are polynomial. | Classical systematic-basis annealing is stronger; forcing rank and flat dimensions must beat the Prange ceiling. Existing every-table bounds already cap this proposed operation. |
| Native lattice cooling | Explicit lattice basis, prepare narrow coherent discrete Gaussian for a decoder; simulate warm-start Metropolis parent with charged time and accuracy. | LLL/Babai and wide classical Gaussian samplers; existing exponentially small native coupling rejects this operation without a paid nonlocal move. No general DGS lower bound. |
| Jones observable | Explicit braid, estimate a specified normalized invariant; known path-model quantum circuit costs polynomial in length and inverse additive error. | Bounded-width tensor contraction; useful unnormalized accuracy can require exponentially fine normalized error. No new normalized observable/search endpoint emerged. |
| Clifford-scrambled Gaussian | Exact copies of a Clifford-transformed Gaussian state, output preparation; ordinary Bell measurement reveals a hidden balanced Majorana shell. | No paid shell-frame extraction or uniform support gap near stabilizers. The two-Fock mechanism below uses known physical Majoranas and does not solve this different problem. |

These are admission screens, not new impossibility claims. The old anyonic
note's blanket claim that #P-hardness excludes polynomial quantum algorithms
was NOT used as evidence. Corpus baseline lookups and the actual primary
sections preceded admission of the two-Fock operation.

## Native contract and classical attacks

Input: positive integer n, epsilon,eta in (0,1), and independent copies of one exact pure
state

    psi = G(alpha|x> + beta|y>),   |alpha|²+|beta|²=1,

where G is an unknown even Gaussian unitary on known physical Majoranas,
x,y are distinct unknown Fock strings of equal parity (one coefficient may
vanish); a single distinct branch is included.
The computational/Jordan-Wigner encoding and ordinary polynomial qubit
circuits are available. Copies, Pauli measurements, Gaussian rotations and
finite precision are charged. G, its inverse, branch strings and moments
are NOT supplied. Output a polynomial-size preparation circuit at trace
distance <=epsilon, with probability >=1-eta. This does not cover unknown
physical Majoranas, arbitrary Clifford scrambling, general sparsity,
mixed/noisy copies or general superpositions of nonorthogonal Gaussians.

The proposed advantage is polynomial copy/time over unrestricted tomography
of an exponential-dimensional state. It is NOT a classical-input exponential
speedup: all reconstruction processing below is classical. Given G,x,y,
Gaussian/Pfaffian methods already compute this two-branch state's amplitudes
and number-measurement probabilities efficiently, including interference.
Fixed-small Gaussian compression is a stronger applicable learning baseline
than treating the state as an arbitrary tensor network. It closes the small
Hamming-distance cases and is reused, not reimplemented.

Cheapest falsifiers: incorrect four-point signs; a coherent cross term at
large branch distance; a missing/degenerate top eigenvalue; a growing cat
already covered by fixed-cap learning; exponentially unstable rounding;
unpaid phase readout or an inverse of the UNKNOWN G; finite tests promoted
to a theorem. Exact finite controls are only falsifiers.

## Exact moment identity and paid spectral operation

For distinct a,b define C_ab=i<gamma_a gamma_b>, antisymmetric with zero
diagonal. For four distinct indices define T_abcd=-<gamma_a gamma_b gamma_c
gamma_d>, extended alternatingly and zero on repeated indices. Put

    W(C)_abcd = C_ab C_cd - C_ac C_bd + C_ad C_bc,
    K = T-W(C).

Let k=Hamming(x,y). k is even. For k>=6, any Majorana monomial of degree
at most4 changes at most4 occupations before G, so its branch cross term
is zero. Gaussian conjugation preserves degree. The two branch covariance
matrices J0,J1 commute, square to -I, agree on a common subspace and have
opposite signs on the active 2k-dimensional subspace. Write

    J=(J0-J1)/2, P=-J², B=(J0+J1)/2, p=|alpha|², a=4p(1-p).
    BJ=0, B²=-(I-P), C=B+(2p-1)J, K=a W(J).

The last identity is the quadratic polarization identity
p W(J0)+(1-p)W(J1)-W(pJ0+(1-p)J1)=p(1-p)W(J0-J1).
It is independent of the unknown relative phase, which is recovered later.
DO NOT use the mixture covariance formula at k=2: quadratic cross terms
can survive. That case is handled by Gaussian/compressible learning.

Flatten K on pairs a<b,c<d. Antisymmetric matrices have inner product
<X,Y>=Tr(X^T Y)/2. Direct index contraction gives

    L_J(X)=<J,X>J+J X J.

On active pairs, L_J has eigenvalue k-1 on J, eigenvalue -1 on commuting
skew matrices orthogonal to J, and eigenvalue +1 on anticommuting skew
matrices. All matrices with an inactive index have eigenvalue0. The
multiplicities are 1,k²-1,k(k-1), and binom(2n,2)-binom(2k,2).
These spaces exhaust all pairs. Thus K has unique largest eigenvalue
a(k-1), top vector J/sqrt(k), and gap a(k-2), for a>0 and k>=3.

The operation is ordinary diagonalization of a binom(2n,2)-square REAL
symmetric matrix assembled from O(n^4) measured Pauli expectations. It
does not require tensor decomposition, branch enumeration, a hidden basis
oracle or a quantum linear-system solver.

## Uniform completion, without promised minimum weights

Take n>=6; for n<6 use constant-dimensional tomography. For clarity set

    tau=epsilon²/10000,
    delta=epsilon^10/[10^20 (n+1)^10].

Estimate all two/four-point means to additive delta simultaneously, clip
individual real estimates to [-1,1], and form Chat,Khat. Hoeffding with a
union bound costs O(n^4 delta^-2 log(n/eta)) copies. Each Pauli measurement
uses O(n) elementary gates; no joint measurement or state inverse is needed.
Let c=||Chat-C||_F<=2n delta. Entrywise K error is <=7delta, hence

    e=||Khat-K||op <=14 n² delta.

Construct a constant/small polynomial list of candidates, validating their
fidelity on NEW copies only after construction:

1. A pure Gaussian candidate from polar rounding Chat. If k>=6 and
   min(p,1-p)<=tau, all singular values of C are >=1-2tau. Its polar is
   exactly the dominant branch covariance. Stable rounding therefore gives
   a candidate at distance <=sqrt(tau)+O(c) from psi. The estimate need not
   identify that branch, and there is no small-weight division.
2. The known fixed-4 Gaussian-compressible learner, at error epsilon/20.
   Every k<=4 two-Fock input has this form: after known parity convention
   and a Gaussian frame, at most4 modes carry non-Gaussian information.
   On other inputs this routine is capped and only supplies a candidate;
   its success guarantee is invoked exclusively under its source promise.
3. For each even k in [6,n], use the top normalized eigenvector v of Khat,
   convert it to a skew matrix, and scale by sqrt(k). Round its largest k
   skew singular pairs to singular value1, the others to0, obtaining Jhat.
   This is a nearest rank2k orthogonal partial complex structure in
   Frobenius norm. Set Phat=-Jhat². On Phatperp, polar-round the compression
   of Chat to a full complex structure Bhat. Zero/ill-conditioned invalid
   trials use a fixed valid candidate; the correct trial has the bounds
   below. Bhat and Jhat act on orthogonal spaces by construction.

In case3 with the TRUE k and min(p,1-p)>tau, a>=2tau. Davis--Kahan and
e<gap/4 give, after an irrelevant sign choice,

    ||sqrt(k)v-J||_F <=d,    d=4 sqrt(n)e/tau.

Nearest rounding implies ||Jhat-J||_F<=2d and
||Phat-P||_F<=4d. Since their projector distance is <1, a rotation R mapping
P to Phat exists with ||R-I||_F<=2||Phat-P||_F. This rotation is used ONLY
in the proof, not supplied to the learner. Btilde=RBR^T is a feasible
complex structure on Phatperp with ||Btilde-B||_F<=16d. Therefore

    ||(I-Phat)Chat(I-Phat)-B||_F <=c+8d,
    ||Bhat-B||_F <=2c+64d,
    ||(Bhat +/- Jhat)-(B +/- J)||_F <=2c+66d.

For pure Gaussian branches with covariances Gamma,Gamma', the expected
excitation count in one branch's vacuum frame is ||Gamma-Gamma'||_F²/8.
The probability outside that vacuum is at most the excitation count.
Consequently infidelity <=||Gamma-Gamma'||_F²/8. A particle-hole frame
used to prove this identity is not an input oracle. With the displayed
delta, branch distances, frame-rounding errors and the distance from psi
to the learned two-dimensional span can all be made <epsilon/1000.

The two rounded branches share a computable orthogonal normal-form frame
and differ exactly on the k active occupations. A determinant correction
can be absorbed into one known occupation sign so the actual Gaussian
rotation is even. Gaussian circuits use O(n²) plane rotations, each
specified to polynomial bit precision. The odd-parity sector is retained;
alternatively detect the exact total parity, conjugate all copies by fixed
X1, and restore X1 on output. O(2n) and SO(2n) are not silently identified.

Undo only this LEARNED frame on fresh copies. Estimate the unnormalized
2x2 density block on its two known occupation strings. Its diagonal
projectors and real/imaginary off-diagonal observables have norm1 and
O(n)-gate measurement circuits: a reversible affine bit map sends the
two strings to |0^n>,|10...0>, after which one measures the encoded qubit
and checks the remaining bits. A failed check contributes zero, not a
renormalized successful record. Project the estimated matrix to PSD and
return its top eigenvector. When the true state is near this span its
weight is near1 and its leading eigenvalue is separated by a constant;
additive O(epsilon²) entry accuracy is ample for error <=epsilon/20.
The relative cat phase is thus measured with polynomial resources, not
inferred from the low-degree tensor, which cannot contain it at large k.

Finally estimate each candidate's fidelity on fresh copies by applying
its explicitly learned inverse preparation and measuring all zero.
O(epsilon^-4 log(n/eta)) copies per candidate suffice for additive
epsilon²/100 accuracy. Select the largest estimate. At least one
candidate has distance <=epsilon/10, hence the selected pure state has
infidelity <=epsilon²/100+2epsilon²/100 <epsilon². Allocate eta among
moment acquisition, fixed4 learning, block tomography and validation.

All rounds, copy counts and numerical eigensolvers are capped. Wrong-k
or nonpromised candidates do not need to succeed. Numerical matrix
operations and O(n²)-rotation compilation use an additional inverse-
polynomial precision allowance, smaller than the displayed delta; the
true trial has the proved gaps. Skew singular-pair truncation needs only
the active/inactive gap, not a gap within equal singular values. The
common polar map has singular values bounded away from zero in the good
trial. Numerical normal forms may choose any within-block basis: these
choices preserve the two extremal Fock rays, up to phases measured later.
Round each of O(n²) plane-rotation angles to error O(delta/n²), so the
sum of unitary errors is O(delta). Standard finite universal-gate synthesis
to that same total accuracy costs polynomially many additional gates.
This supplies polynomial BIT time as well
as arithmetic time. The deliberately loose acquisition bound is
O(n^24 epsilon^-20 log(n/eta)), NOT a practical or optimal sample count.

## Sources and prior overlap

Actual PDFs/text/hashes: `audits/sources/two_fock_learning/source.json`.

- [Sen2609.12219v1, Section1.4](https://arxiv.org/html/2609.12219v1#S1.SS4)
  explicitly asks the general unknown-Gaussian sparse-Fock question. Its
  computational-basis sparse theorem does not supply the hidden rotation.
- [Mele--Herasymenko, PRX Quantum6,010319](https://ir.cwi.nl/pub/34997/34997.pdf)
  supplies the fixed-compressibility learner. The exact t=4 promise is
  used here; its approximate theorem's mixed output is not silently
  substituted for a pure preparation.
- [Amidi--Asadian--Moosavian2610.08723v1, Theorem1](https://arxiv.org/html/2610.08723v1)
  already uses connected quartic tensors for unknown Gaussian block
  recovery, with a FIXED particle cap per branch. Its theorem2 learns
  the orbit of fixed four-mode paired-magic blocks. No priority claim
  is made for cumulant methods or this spectral specialization.

The growing balanced k-mode cat cannot evade the fixed-cap distinction
by a different decomposition of the source's stated block family. Its
covariance is zero and K=W(J) is invertible on all active bivectors for
k>=6. In a covariance-zero source block representation there are no core
modes and each branch weight is1/2, hence exactly two disjoint branches
per block. Two blocks would make K zero on their cross-block bivectors,
contradicting invertibility. One block needs k/2 particles per branch.
Thus the particle cap must grow. This is a covariance/cumulant invariant
argument for that precise family, not exclusion of other published learners.

## Review, controls and continuation

Actual-source scope review: `audits/reviews/2026-11-07-two-fock-sources.md`.
The parent inspected the primary fixed4 theorem/output and fixedparticlecap
contract directly. Core/end-to-end review is `audits/reviews/2026-11-07-two-fock-core.md`, accepted after checking the complete uniform bounds. The
source review's covariance-zero/full-rank invariant is a deduction checked
above; it is not a quoted novelty or lower-bound theorem.

Two independent Claude reports completed on immutable packets under
`audits/claude_inputs/2026-11-07-two-fock-learning/`:

- `audits/claude_runs/2026-11-07-two-fock-spectrum/`: Opus5.5/high,
  estimate USD0.254508. Accepted after checking: exact signs, complete
  spectrum/multiplicities, unordered branch reconstruction, k4 cross-term
  counterexample. The suggestion to infer k by exact rank is unnecessary
  and NOT used under noise; the polynomial k-loop remains.
- `audits/claude_runs/2026-11-07-two-fock-stability/`: Fable5.1/high,
  estimate USD1.395840. Accepted: small-weight exact polar identity,
  sequential rounding, learned-span phase readout and fresh-copy selection.
  Its compressed B-rounding inequality compares across unequal subspaces;
  the main proof explicitly transports B with R before nearest rounding.
  Its tighter sample exponent is NOT adopted. Numerical bit costs and
  small-core/parity/source obligations were completed separately above.
  The suggested largest-absolute-eigenvalue convention workaround is NOT
  used: the raw T sign is fixed and verified, since a wrong Wick subtraction
  is not generally repaired by changing the eigenvalue selector.

Total estimated usage USD1.650348, both terminal reports; no retry,
invoice or remaining-balance inference. Reviews support the checked proof,
not an automatic theorem or separation promotion.

Exact CAS control: `audits/controls/two_fock_learning/control.py` and `.json`.
Seven physical modes, six active, four rational Gaussian rotations mixing
active/common modes, and a nonreal cat phase. All raw two/four-point means
are computed exactly. The observed pair matrix has spectrum
5^1,1^30,(-1)^35,0^25, and its measured top eigenspace recovers J exactly.
The Gaussian branch Wick baseline reproduces every low-order mean; two
different cat phases have identical such data. A common frame computed
ONLY from these moments compiles to56 numerical Givens rotations, then
two-dimensional phase readout/preparation gives fidelity >1-2e-15.
No generating-G inverse or branch advice enters that decoder. Exact k4
and k2 controls reject the inappropriate mixture identities. This is a
finite source/spectral/phase control, NOT full noisy learner execution,
statistical validation, asymptotic evidence or quantum hardware execution.

The unresolved high-level question remains general sparse-Fock learning;
this pass claims at most the two-branch endpoint. No implementation of a
general moment backend or adjacent extension is authorized by this result.

Milestone: current STATE title/Now/boundary row, three primary PDF hashes,
immutable Claude context snapshots, both terminal reports/usage, review
presence and scoped control gates verified. Scoped whitespace check passed.
No full-suite run, commit, push or unaffected experiment rerun. The final
control derives its largest eigenvalue from measured K and projects C onto
the recovered common space; the generating frame is never decoder advice.
