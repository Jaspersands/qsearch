# One-rotation magic-learning audit dispositions

2026-11-06. Exact input copies; proper output within pure-state trace distance
epsilon, failure eta. No noisy-source guarantee, original-Clifford recovery,
axis uniqueness, full learner execution, novelty or classical separation.

## Primary sources and scope

Parent fetched the actual PDFs in audits/sources/one_rotation_learning/.
Source reviewer superlattice_source_scope checked Haug Theorem2 (text188--227),
AppendixI (1967--1977), PropositionS9 (1401--1424), and finite-orbit exact
identification (1514--1536). Unknown Clifford-product BLOCK learning is not
arbitrary unknown-Clifford bond2 MPS learning. The CAMPS classical sampler
assumes a supplied representation with known Clifford.
Aguilar Theorem4/Corollary2 (380--411), Theorem7 (2604--2617) and Lemma14
(2807--2812) distinguish product-block recovery, full block tomography and
CHOI/unitary access. Copies of one output state supply no unknown channel.
The corrected C'|H>^n branch IS covered by an exact finite-H preparation
learner in O(n^2+log1/delta) copies and polynomial computation. This uses
the product theorem directly, not the random-circuit corollary.

## Bell source and support gap

The parent derived the exact two-copy Bell law using the TRANSPOSE
bilinear amplitude U^T W U, not U^dagger W U. For the real diagonal Z^n
axis and real H product, the mixed branch amplitudes are in quadrature.
Full-swap q=0 remains enforced. S is NOT periodic under p, so the first
translation/Simon shortcut is false.
The independent Opus report proved the same law and the product-transfer
bound gamma_D>=2^(-2D-3). Parent rechecked its induction on the three-letter
local support and the degree-D+1 shift-and-multiply function. This yields
an explicit polynomial sample clock for the COMPLETE K3, not a few valid
constraints or a hard-to-detect rare sector.
Phase conventions must be consistent: tensor-product and global-parity
Hermitian conventions can differ by signs, irrelevant to the probability
law. The antisymmetric bilinear identity also holds for complex vectors.
The report's suggestion that ANY nearby angle destroys the gap is too
broad: both weights can remain bounded away from zero. No extension to
angles/noise is claimed or needed here.

## Uniform algebraic extraction

Derivation: growing_degree_mechanism, CLOSED
2026-11-06-one-rotation-cubic-axis.md. Parent independently rederived:

- Exact K3=q*Aff_1+span Eij from coordinate slice coefficients; unique
  overlap sum Eij=q*ell+q. K2=<q>, K1=0; no assumed ideal-generation step.
- Top exterior3-form covariance removes affine shifts. Lie matrices act
  by D_M f(v)=df_v(Mv), so W'=(F^-1)^*W implies L'=F L F^-1. This is
  PHYSICAL F covariance, not F^-T Pauli labels.
- For all n>=4, pure-x, xz^2 and x^2z coefficients force the uniform
  classification aI+N_D, D=diag(c)+b11^t. The B-block needs two outside
  indices; they exist at n4. No parity-dependent matrix inverse is used.
- The Lie algebra is ABELIAN, falsifying the proposed commutator shortcut.
  Squaring is linear on this commuting promise space. Its kernel contains
  the desired square-zero maps. The intrinsic symplectic diagonal lambda
  transforms as F lambda and gives explicit rank-one quadratic equations.
- Degree3 Macaulay rows yield ALL degree<=2 relations: in hidden canonical
  variables v_i v_j=b implies b v_i=b. The n+2 affine-independent solutions
  give the complete quotient algebra; simultaneous idempotent eigensplitting
  lists all points with polynomial work. No matrix/assignment search, generic
  MQ solver or algebraic-closure multiplicity assumption is imported.

Independent adversarial reviewer independent_direction_selection rederived
these steps, their n>=4 hypotheses, covariance and degree3 closure. Its final
review is retained in the pass record; no finite rank table substitutes for
this symbolic proof.

## Endpoint, error allocation and scope distinction

Source reviewer independently audited the complete main-note procedure.
For r=n+1 axes, cap every finite-H learner and validate its returned Clifford
plus finite-H labels. Every returned candidate is thus a known unitary
preparation circuit, including on a wrong unpromised branch.
One sign per true physical axis suffices: sign ambiguity changes correction
by a Pauli pi/4 Clifford. The correct branch returns exact preparation on
its success event. Returned known circuit inversion, not unknown source
inversion, tests fresh copies. ALL-zero acceptance m=ceil(epsilon^-2
ln(4r/eta)) bounds each epsilon-inaccurate candidate by eta/(4r).
Earlier wording said SWAP; repaired to the actual projector test, whose
constant is different. Total failure <=eta/4+eta/(4r)+eta/4<eta.
Accepted wrong branches need only be epsilon-close; no exact certification.

K2=<q> and the actual quadratic-cut source imply Clifford-product width n.
The degree2 gap bounds every nontrivial Clifford-cut purity by63/64 and
PURE-product trace distance by at least sqrt(1-sqrt(63/64))>0.088.
The independent reviewer checked this scope; it is not a mixed-product
approximation theorem or a general learning lower bound.

## Claude run dispositions

Exact saved requests under audits/claude_runs/2026-11-06-:

- one-rotation-algebra-fable: truncated max_tokens, empty report;
  1504 input/32768 output tokens, estimated USD1.65344. No findings/retry.
- one-rotation-gap-opus: completed;3276 input/15046 output tokens,
  estimated USD0.314024. Main law/gap proof verified above.
- one-rotation-rank-one-opus: provider refusal, empty report;
  1490 input/772 output tokens, estimated USD0.0214. No findings/retry.
  This was a distinct explicit Macaulay proof audit after the broad search;
  it supplied no independent endorsement.

Total estimated USD1.988864, not an invoice or exact remaining balance.

## Exact finite falsifiers

All controls used /opt/anaconda3/envs/qsearch-cas/bin/python.

- bell_control.py: n4, exact Q(zeta16), all256 labels in canonical and
  nontrivially scrambled frames. Offset32, support106, total mass1, exact
  law/cubic cuts/correcting Pauli verified. Naive p-period fails.
- lie_n4.py: canonical W dimension13 and Lie dimension6; commutator common
  kernel dimension8, falsifying the one-dimensional-kernel shortcut.
- macaulay_n4.py: all106 transformed support labels, no supplied cubic
  basis. K2=1,K3=14,W=13,L=6,N=5,U=4;10 quadratic relations, quotient
  dimension6, eigensplitting ranks0,1,1,1,1,1. Recovered axes
  [1,32,96,128,193] equal independent forward-Pauli conjugation. The
  F^-T countercontrol disagrees. ZERO coefficient assignments enumerated.

These are finite identity/covariance/implementation falsifiers, not a full
copy-sampling learner, asymptotic experimental evidence or quantum execution.
No larger backend or adjacent family extension is queued. Re-rank native
mechanisms independently before the next research experiment.
