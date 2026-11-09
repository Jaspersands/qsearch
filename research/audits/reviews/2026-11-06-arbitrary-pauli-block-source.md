# Arbitrary-Pauli active-block learner: source and branching audit

2026-11-06. Independent actual-text/source/resource audit. No Git, network,
API call, broad source generalization or quantum execution. Repository Python:
`/opt/anaconda3/bin/python`. STATE/TRAPS and the current one-rotation note were
read. This review is CONDITIONAL on the parent's separate uniform arbitrary-
Pauli Bell-kernel/support-gap and active-axis proofs; it does not prove them.

## Verdict and exact source use

ACCEPT the following two-branch composition at the source/resource boundary:
recover the exact irreducible Clifford-product blocks using the constant-gap
quadratic learner; directly learn bounded blocks approximately if their maximum
size is below 25; otherwise apply the new cubic-axis operation to the one large
block and finish using exact finite-H product learning and the original fresh-
copy verifier. The two branches have different completeness arguments.

Primary local texts and exact locators:

- `../sources/one_rotation_learning/haug.txt`, lines174--183: Theorem1's
  irreducible symplectic decomposition; lines188--212: Theorem2 recovers the
  exact decoder/blocks with O(gamma_2^-1*(n^2+log(1/delta))) Bell samples and
  polynomial classical time. Structure recovery itself has NO exponential
  dependence on the largest recovered block size.
- The same text, lines973--1012: the uniform false-equation union bound and
  LemmaS5 justify reuse of the learned samples under adaptive decoding.
  Lines1018--1084: AlgorithmS1 explicitly removes stabilizers, chooses each
  block's symplectic basis, returns a known Clifford decoder, and optionally
  reads all stabilized-qubit signs from one fresh decoded copy. Lines1102--1118
  bound its finite-field processing and sample count.
- Lines211--227 and1120--1145: exact decoded blocks are pure; subsequent full
  block tomography has GLOBAL trace error epsilon, with copy bound
  O(r*2^k*epsilon^-2*log(r/delta)). AppendixE explicitly uses dimension-weighted
  infidelity budgets and the product-fidelity inequality.
- Lines1401--1424: PropositionS9 gives constant quadratic gap 1/16 for a
  Clifford-scrambled H product (H is single-qubit Clifford equivalent to T).
  Lines1514--1536 give width-one capping and exact finite-orbit identification
  with O(n^2+log(1/delta)) copies and polynomial processing.
- `../sources/one_rotation_learning/aguilar.txt`, lines380--411: Theorem4
  distinguishes disentangler recovery from Corollary2's full block learning.
  It is a compatible fallback, not needed to strengthen Haug's stated result.

No theorem here asserts learning arbitrary unknown-Clifford bond2 MPSs.

## Large-block gauge and legal access

Assume the new proof establishes, above the fixed threshold25, one
stabilizer-free indecomposable active w-block and inactive H singletons, with
a uniform constant quadratic support gap for the WHOLE input state. Haug's
Theorem2 then recovers that block in poly(n,log(1/eta)) resources. Its unique
symplectic block subspace is independent of decoder choices. The remaining
choices are block order, symplectic coordinates and Pauli phases, hence an
arbitrary LOCAL Clifford within each recovered block. There is no supplied
or known original hidden frame. In particular, the active state remains in
the proposed arbitrary-Pauli family with an unknown local Clifford.

Apply the known decoder to fresh original copies and retain its active
register. The exact decomposition makes this a fresh PURE block copy; discarding
the other product factors needs neither postselection nor an unknown inverse.
For small weights the active component may acquire stabilizers or split into
smaller irreducibles. AlgorithmS1 handles these cases, and only the recovered
maximum block size is used for the branch decision. Weight0 is simply a
Clifford-H product.

After a correct physical-axis correction within the decoded large block,
the ENTIRE corrected n-qubit state is C' H^n, including the inactive singletons.
Either sign of the Hermitian Pauli works: the corrections differ by a Pauli
pi/4 rotation, which is Clifford. Run the finite-H learner on this full state.
Its successful correct branch returns an exact known unitary preparation;
undoing the chosen correction and the known decoder returns a preparation of
the original state. Validate all returned Clifford tableaux and finite-H labels
on wrong branches, and cap their clocks. The inverse verifier uses only these
constructed circuits, never the unknown preparation's inverse.

## Bounded-block branch: approximate output without verification

On the exact-structure event, if maxblock<25, the true Clifford-product width
is at most24. Source AppendixE therefore supplies direct global tomography in
O(n*2^24*epsilon^-2*log(n/eta)) copies, a polynomial bound with a potentially
very large FIXED constant. No practical-efficiency claim follows.

Give structure recovery failure allowance eta/4 and full tomography allowance
eta/4. Run tomography to global trace target epsilon/2; do not assign epsilon/2
independently to every block. AppendixE's allocation

    infidelity_alpha = (epsilon/2)^2 * d_alpha / sum_beta d_beta

implies that the product state's total infidelity is at most(epsilon/2)^2.
Use per-block confidence eta/(4r). Pure block descriptions of constant
dimension can be normalized and converted to preparation unitaries with
polynomial bit work. Reserve the remaining epsilon/2 for finite-description
and gate-synthesis errors: e.g. allocate vector-norm error epsilon/(2r) per
block, whose telescoping sum is at most epsilon/2. The known exact Clifford
decoder does not increase trace error. If an ideal Clifford+T output is
required, approximate these known constant-block unitaries to that tolerance;
only polynomially many gates and polynomial precision are required.

Output this preparation directly. There is NO candidate-selection test on
this branch. It succeeds to the requested epsilon with failure at most eta/2.
This is approximate learning, not an exact finite-copy state equality claim.

## Large-block budget and the avoided verifier pitfall

Allocate eta/4 to initial quadratic structure, eta/4 to active cubic-kernel
recovery, eta/(4R) to each capped product learner, where R<=n+1, and eta/4 to
the union of false candidate acceptances. Only the true product branch needs
its promised learner guarantee. Conditional on success it is EXACT, so the
original all-zero known-preparation-inverse test has completeness 1. Its

    m=ceil(epsilon^-2*ln(4R/eta))

tests per candidate have soundness eta/(4R) against every preparation farther
than epsilon. With fresh copies this remains valid conditionally on all prior
adaptive choices. Total large-branch failure is at most

    eta/4 + eta/4 + eta/(4R) + eta/4 < eta.

Do NOT apply this all-zero verifier unchanged to a merely epsilon/4-close
tomographic candidate: F^m can decrease with log(1/eta), so its completeness
would be unpaid. The direct-output bounded-block branch avoids that problem.
The same issue does not affect exact finite-H candidates in the large branch.

This closes source applicability, decoder gauge, block-error accumulation and
branching resources conditional on the new uniform Bell/algebraic proofs. No
arbitrary-angle, noisy-copy, unknown-Clifford MPS, uniqueness or speedup result
is established by this audit.
