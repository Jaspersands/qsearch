# Learning one correlated rotation beyond a Clifford product

2026-11-06. REVIEWED WRITTEN copy-based polynomial-time learner for the
exact native family below. Independent source, all-n algebra, Bell-law/gap
and end-to-end error/resource reviews complete. No full learner execution,
novelty, classical separation or quantum hardware claim. Review dispositions:
`audits/reviews/2026-11-06-one-rotation-learning.md`.

## Question and native contract

Input: fresh exact copies of

    psi = C exp(-i*pi*Z^(tensor n)/8) |H>^(tensor n),

n>=4 grows, C is an unknown n-qubit Clifford, and |H> is the real +1
Hadamard eigenstate with Bloch X=Z=1/sqrt2,Y=0. No classical circuit,
chosen-state query, inverse preparation, supplied axes or conjugate source.
Output a polynomial-size preparation circuit within trace distance epsilon
of the same pure state, with failure<=eta and target
poly(n,1/epsilon,log1/eta) resources. Constant n is standard tomography.
This is the usual approximate state-learning contract. Exact preparation
on the correct internal branch does NOT certify exact selection among
other branches; a final independent known-preparation inverse test pays the requested epsilon.

This is structured quantum-device/resource-state learning, not a classical
input speedup. Before the unknown Clifford the state is a bond2 MPS (a sum
of two product states); the Clifford hides its simple coordinates. A single
collective Pauli interaction couples an extensive magic-state product.
Recovering its physical Pauli direction would remove that coupling and let
an existing product learner finish. Full tomography has exponential size;
this is not a lower bound for this promised family.

Independent comparison rejected extending Selmer merely by inertia.
Scalar-OPI exact-symbol Gibbs clusters reproduce the existing affine-cluster
sampler and have an MDS freezing issue; no new first-witness guarantee.
Gaussian correction is classically sampled in its proved regime. Exterior
streaming and fixed-format tensors supply no fresh native receiver. The
present operation is selected because it gives a concrete end-to-end
learning route beyond the product-cut mechanism.

Corpus been-tried and baseline lookups preceded primary-source selection;
no exact catalog match is not hardness. Haug arXiv2609.27128 and Aguilar et
al.2609.27565 supply current Clifford-product/Bell-symmetry learners. Their
qubit product results already defeat naive rare-single-plane Bell detection
as a reason to reject ordinary C|H>^n learning. The full-copy quadratic
algorithm, not that naive test, is the applicable baseline. The source does
not automatically supply a learner for arbitrary Clifford-hidden bond2 MPS.

## Concrete mechanism and cheapest falsifiers

Let v=(x,z) in F2^(2n), q(v)=sum x_i z_i, p=(0,1^n), ell(v)=sum x_i.
The base product Bell law mu has local probabilities

    I:1/2, X:1/4, Z:1/4, Y:0.

Write B=supp(mu). For the one-rotation state before C, direct identical-copy
Bell expansion gives the proposed exact law

    nu(v)=mu(v)                         if ell(v)=1;
    nu(v)=(mu(v)+mu(v+p))/2             if ell(v)=0.

Indeed U^T W_v U=W_v when P anticommutes with W_v and equals
W_v(cos(pi/4)-i sin(pi/4)P) when they commute. Here P=Z^n is real, and
the real base Bell amplitudes have no cross term in the second case.
Normalization follows because ell(v+p)=ell(v). Unknown C applies an
invertible affine symplectic relabeling preserving q.

Consequently

    S=supp(nu)=(B union(B+p)) intersect {q=0}.

The universal full-swap condition q=0 is essential. S is NOT translation-
periodic by p; a naive Simon oracle for S would therefore be wrong.
For i<j the Boolean cubics

    E_ij=x_i*x_j*(z_i+z_j)

vanish. Together with q, they cut S exactly over F2: on the active x
positions, z must be all0 or all1, and q excludes all1 for odd active count.
This set-theoretic assertion does NOT prove that q and E_ij span the entire
low-degree vanishing space. Boolean x_i^2=x_i identities must be retained.

Learn the full degree<=3 Boolean vanishing space K3 by sample evaluations
and linear algebra. The proposed uniform support-gap proof is short:
if a degree-D function f is nonzero on B, nu>=mu/2 there gives probability
at least4^-D/2 by finite-product anti-concentration. Otherwise
(1+ell(u))*f(u+p), of degree<=D+1, is nonzero on B and gives at least
4^-(D+1)/2. Thus gamma_D>=2^(-2D-3); for D3, >=1/512. This would pay
O(n^3+log1/eta) Bell samples. The independent Opus audit and exact cyclotomic control support the
parent proof; no sampling inference is used as the proof.

The algebra has a complete independently reviewed uniform proof, retained in
`audits/reviews/2026-11-06-one-rotation-cubic-axis.md`. Its essential steps are:

1. The EXACT Boolean kernel is K3=q*Aff_1+span(E_ij), with one overlap
   sum E_ij=q*ell+q. Its dimension is2n+binom(n,2), and K2=<q>.
   This is proved from coefficients on one- and two-active-x slices,
   not inferred from the set-theoretic generators or a finite nullspace.
2. Its top exterior3-form space W is affine-translation invariant. Compute
   L={M in sp(2n,2):D_M W subset W} by linear equations. For every n>=4,

       L={a I + [0 0; D 0]: D=diag(c)+b*11^t}.

   The proof separates the pure-x, xz^2 and x^2z terms; the two
   outside indices in the B-block argument require n>=4. The first
   commutator shortcut is FALSIFIED: this Lie algebra is abelian.
3. Squaring is LINEAR on this commuting algebra. Its kernel N consists of
   the square-zero matrices and has dimension n+1. Their common kernel is
   a Lagrangian. Intrinsically define lambda(N) by
   omega(v,lambda(N))=omega(v,Nv). Rank<=1 is equivalent to
   N(v)=omega(v,lambda(N))*lambda(N), giving explicit Boolean quadratics.
4. A degree3 Macaulay computation, followed by simultaneous eigensplitting,
   returns ALL n+1 nonzero rank-one matrices. In hidden canonical variables
   the equations are v_i*v_j=b; their degree3 multiples yield b*v_i=b.
   The complete quotient algebra has dimension n+2 and affine-linear basis.
   This proves polynomial extraction, not an assumed generic MQ solver.
5. Covariance gives the candidate list {Fz_1,...,Fz_n,Fp} in the PHYSICAL
   label space. There is no unique-axis claim. Unknown affine Bell shifts
   affect no top cubic. No supplied hidden coordinate frame is used.

## Complete candidate learner and error budget

Let D3=1+2n+binom(2n,2)+binom(2n,3). Take

    M=ceil(512*(D3*ln2+ln(4/eta)))

Bell samples, each using two exact copies. The learned K3 is complete with
probability>=1-eta/4. Apply the polynomial algebra above. Dimension,
commutativity, algebra and returned-rank consistency checks are capped;
incorrect learned inputs never trigger an unbounded symbolic search.

For r=n+1 candidate axes, apply one fixed sign of its Pauli pi/8 correction
to fresh copies and run the existing finite-H product learner with its
polynomial promise clock and failure parameter eta/(4r). An arbitrary
wrong branch may fail or return an arbitrary finite-H preparation; do not
trust its product assertion. Validate its Clifford tableau and n finite-H
orbit labels, or return ABORT, so EVERY returned preparation is a known
unitary circuit that can be inverted even on an unpromised wrong branch. On the correct axis, either rotation sign
works because their difference is a Pauli pi/4 Clifford. Thus at least one
branch returns an EXACT preparation of the corrected state on its success
event. Undo that candidate correction in the returned circuit.

VERIFY each returned preparation V using fresh ORIGINAL copies: apply the
KNOWN circuit V inverse and measure all qubits, accepting only if all tests
return zero. This is an inverse of our constructed circuit, not an inverse
oracle for the unknown source. The zero probability is fidelity
F=|<0|V^dagger|psi>|^2. Take

    m=ceil(epsilon^(-2)*ln(4r/eta))

fresh tests per candidate. A circuit farther than epsilon in pure-state
trace distance has F<1-epsilon^2 and passes all m tests with probability
at most eta/(4r). Correct exact preparations pass certainly in the ideal
gate model. Union bounds over K3, the correct product branch and false
acceptances give total failure below eta; no exact equality certificate is
claimed for the accepted wrong branch. Return ABORT if none passes.

All Pauli corrections compile to O(n) Clifford operations and one T gate,
up to global phase. Returned circuits have polynomial size. Copy use is
O(n^3+n*log(n/eta)+n*epsilon^(-2)*log(n/eta)); all classical matrices have
polynomial dimensions, with fixed-degree Gaussian/Macaulay elimination.
No inverse of the unknown source, hidden advice, postselected rare sector,
or original-Clifford identification is needed. The uniform algebra and final error/resource reviews are complete. This is
a written algorithm under the exact input promise and ideal Clifford+T
gate model; no full learner has been run here.

## Why the product learner alone does not finish this family

The exact K3 classification gives K1=0 and K2=<q>. By Haug's actual
quadratic-cut theorem, the state has no Pauli stabilizers and its minimum
Clifford-product width is n: there is no nontrivial product cut in ANY
Clifford frame. This is a structural deduction, not a lower bound against
other learning algorithms.

There is also a constant approximation boundary. A nontrivial Clifford cut
has a quadratic swap equation different from0 and q, so the degree2 support
gap gives violation probability>=1/128. Its reduced purity is therefore
at most63/64. A PURE product across that cut has squared overlap at most the
largest Schmidt weight, at most sqrt(63/64). Hence its trace distance is
at least sqrt(1-sqrt(63/64))>0.088. This explains why an arbitrary small-error
claim cannot just invoke the existing product-block full-tomography step.
The new cubic algebra is a constructive way around that specific limitation.

The main falsifiers were a wrong Bell law, a vanishing support gap,
unrecoverable axes, incompatible candidate corrections, an uncharged Boolean
solver, or prior source coverage of the whole family. The direct proofs and
source review resolve those stated obligations. Two proposed shortcuts did
fail: p is not a support period, and the Lie commutator is uninformative.
No classical-input separation follows; all inference after Bell measurement
and the finite-H measurements is classical. Unknown-Clifford arbitrary MPS,
noisy sources, arbitrary local states and general Pauli/rotation families
remain outside this theorem.

## Sources, reviews and controls

Primary snapshots: audits/sources/one_rotation_learning/, hashes in source.json.
Actual Haug Theorem2 and AppendixI distinguish unknown product-block learning
from classical Bell sampling of a SUPPLIED known-Clifford MPS representation.
Aguilar Theorem4/Corollary2 and its Choi-state results do not provide unknown-
channel access from one output state's copies. Source reviewer checked these
scopes. After a correct correction, Haug PropositionS9 and finite-orbit
identification do provide exact C'|H>^n preparation with polynomial copies.

Claude packets: audits/claude_inputs/2026-11-06-one-rotation/.
The Fable extraction search terminated max_tokens with no report, estimated
USD1.65344; no findings or retry. Opus exact-law/gap audit completed, estimate
USD0.314024. Its main derivation is verified. Keep Pauli phase conventions consistent: tensor-product Hermitian phases
can differ by a sign from the report's global parity convention, with no
effect on the probability law. The antisymmetric bilinear identity holds
for complex vectors too. Reject its broader suggestion that any nearby
rotation angle destroys the gap: if both weights stay nonzero, that does
not follow. No noisy/approximate source extension is claimed here.
A distinct narrow rank-one Macaulay audit refused with an empty report,
estimated USD0.0214; no findings/retry. Total three-call usage estimate
USD1.988864, not an invoice or an exact remaining balance.

Exact n4 cyclotomic Bell control: audits/controls/one_rotation_learning/
bell_control.py checks256 labels in each of two frames, including a nonzero
affine Clifford offset, support size106, all cubic cuts and the physical
Pauli correction. The canonical Lie control falsifies the abelian-commutator shortcut.
`macaulay_n4.py` starts with all106 scrambled support labels, obtains
K2/K3/W/L/N dimensions1/14/13/6/5, then a6-dimensional quotient and five
nonzero rank-one axes by eigensplitting. It enumerates ZERO coefficient
assignments. Axes[1,32,96,128,193] match independent forward-Pauli conjugation;
the inverse-transpose countercontrol fails. Independent all-n and complete
error/resource reviews are finished. No full learner or quantum execution
is claimed. No larger simulator, adjacent extension or infrastructure queued;
independently rank native mechanisms before the next experiment.
