# Adversarial Review: Rank-Bounded Mixed Spectral Source

30 October 2026. Scope: `REES_MIXED_SPECTRAL_SOURCE.md`,
`theorems/mixed_spectral_source.py`, and `tests/test_mixed_spectral_source.py`.
Read `AGENTS.md` and the superseding ring-to-field note. No direct mixed-order
receiver review, flat-state proof replay, code edits, installs, commits,
network writes, outreach, or subagents. This note is the only created file.

## Result

**No fatal counterexample found within the stated supplied-copy model.**
The written spectral compression, upper-bound-only rank acquisition, and
capped complete-run error argument survive the attacks below. This is a
checked mathematical construction, not a verified implementation or a new
speedup. The source reduction does not require the Rees receiver to be correct;
subsequent nonabelian recovery still requires an applicable pure-ray learner.
The ordinary-label-oracle ring-to-field reduction does not automatically
provide that learner in this different, supplied-state model.

Precise surviving claim: fix an IID source rho *before* choosing the public
grid, with a correct numeric upper rank bound R and a correct global orbit
trace gap delta. Use the least permitted power-of-two grid size M. Conditional
on the grid a, the ideal output is T copies of ONE pure flag-product ray
Psi_a, with exact stabilizer H and overlap gap at least delta^2/8. The
complete physical run, including all rejection and abort branches, has source
substitution error at most 5 beta under the stated primitive-error budgets.
The comparison is joint receiver-state trace distance, not an assertion that
conditioning an arbitrary noisy success branch preserves this error bound.

The remaining implementation premise is a uniformly compiled, fresh-copy
factory realizing these instruments and clocks. The three scoped files do
not implement it. No classical hardness or practical resource advantage was
established.

## Mathematical Attacks

### Coherent Thresholding

The claimed complete instrument in the source note, lines 128-160, survives
the cleanup objection. Let A be ideal coherent phase estimation with uniformly
bounded wrong-classification probability p on each eigenspace. Copy the
classification bit and apply A inverse. Comparing with the exact sector-bit
isometry gives operator-norm error at most sqrt(2p): the incorrect-bit part
has squared norm p and changing its bit contributes a factor two. Orthogonal
target eigenspaces make this a maximum over eigenvalues, not a sum over
ambient dimension. The bound therefore also holds with an entangled reference.
Taking p=O(eta^2) and separately paying simulation error gives the claimed
O(eta) complete-instrument error.

Fresh negative-time simulations approximate the inverse *ideal unitary*;
they need not invert consumed noisy programs. The source's distinction is
correct. Controlled sample-based evolution is explicitly supplied by
[Kimmel et al., Appendix C/Theorem 20](https://arxiv.org/pdf/1608.00281).
The normalized diamond bound in
[Go et al., Theorem 2](https://arxiv.org/html/2412.02134v3#S4), applied also
to the program state |1><1| tensor rho, supports reference-safe simulation.
With total absolute evolution time S=O(Delta^-1 log(2/eta)), allocation
eta_i proportional to |t_i| gives sum_i O(t_i^2/eta_i)=O(S^2/eta).
Gate synthesis errors must be included in these allowances, not added free.
This derives the stated copy scaling; no pairwise eigengap is used.

**Falsifier for an implementation shortcut:** use rho=diag(1/2,1/4,1/4,0),
t=1/5, and target/reference state (|0,0>+|1,1>)/sqrt(2). Both target
eigenvalues pass. Measuring the detailed eigenvalue label dephases this state
and has trace error 1/2, even with perfect label probabilities. Coherent
cleanup preserves it. This falsifies a claimed complete-instrument
implementation, although dephasing a fresh diagonal input rho alone would
not by itself falsify the narrower source-preparation task.

### Rank Learning Under Only An Upper Bound

The estimator learns threshold ranks, NOT the exact original rank. For a
fixed good grid, h<=Delta/2 prevents classification changes on good estimates.
The reciprocal, tail, and implementation biases are bounded together by

    2h/w^2 + (kappa+zeta)/w <= 1/32.

The additional classical arithmetic allowance is 1/32. Hoeffding at deviation
1/8 and the stated m are more than sufficient for all J thresholds; sample
reuse across thresholds needs a union bound, not independence between them.
Fresh IID acquisitions give independence between the training samples.
The 1/w cap is justified by t_j>=w, including on bad estimates. A loose R
therefore increases cost without introducing a minimum-eigenvalue premise.

**Boundary falsifier:** rho_0=diag(1,0) and
rho_x=diag(1-x,x), both with supplied R=2, have n-copy trace distance
1-(1-x)^n<=nx. Exact original rank cannot be learned uniformly at cost
polynomial in R alone as x tends to zero. The proposed threshold-rank
algorithm does not make this impossible claim: its smallest threshold is w.
The source note's rejection of impossible rank sequences and fixed runtime
caps is necessary even when training returns a plausible but wrong answer.

### Fixed Random Grid

The grid argument is valid for a fixed source: all candidate thresholds are
4 Delta apart, so a positive eigenvalue lies strictly within Delta of a
candidate for at most one offset. Hence at most rank(rho)<=R offsets are
bad. This is a once-per-run error, not a fresh beta charge for each output,
and is not a heralded certificate. Conditioning on a good offset does not
change the independent fresh-copy preparation model.

**Legal counterexample to redrawing per output:** take R=3, delta=1/4,
beta=1/8, w=1/192, M=256 and

    rho = diag(97/192, 4751/19200, 1583/6400).

Let C3 cyclically permute these levels (embed with a zero fourth level for
two qubits). Both nonidentity elements have trace displacement
4951/19200 > 1/4. Offsets 128 and 148 are both good. The former retains ranks
(3,2,1), using six registers; the latter retains (3,1), using four. Thus even
good grids need not produce the same ray or register layout. The proper ideal
object is a classical mixture over a of T identical copies of Psi_a, with a
retained, NOT T copies of the grid-averaged state. The written construction
already imposes this requirement.

### Normalization And Error Composition

After an ideal filter, p_l=Tr(Q_l rho)>=w and every retained eigenvalue of
rho_l is at least w because p_l<=1. The nonflat streaming theorem and its
known-rank stopping modification really do apply:
[Bene Watts et al., Theorem 5 and Remark 6](https://arxiv.org/html/2610.06737v1#S3)
give the required exponential tail and allow failed new copies to be
discarded while retaining the smaller antisymmetric register. Initial
filtered inputs, growth failures, and all filter retries are counted here.

With at most A filter calls, the complete-channel hybrid costs A eta,
including adaptive calls entangled with previously prepared registers.
Setting eta=beta/(2A) pays beta/2; growth-gate approximation pays the other
half. Bad grid, rank error, growth timeout, filter timeout, and this hybrid
sum to less than 5 beta. This does not assert exact rank or purity of any
noisy intermediate state.

**Normalization falsifier:** change an ideal accepted branch p sigma to
p sigma + u tau, moving probability u from rejection. Complete-output trace
error can be u, while orthogonal sigma,tau give conditional accepted-state
error u/(p+u). At p=u this is 1/2. The draft correctly avoids this division
by comparing complete capped runs; success-only validation would not suffice.

## Paid Complexity And Matched Access

The polynomial statement survives explicit substitution. Writing soft-O for
logarithmic factors in R, 1/delta, 1/beta and T, the existing formulas imply

    Delta^-1 = O(R^2/(beta delta)),
    h^-1 = O(R^2/(beta delta) + R^2/delta^2),
    training programs = soft-O(R^7/(beta^2 delta^5) + R^7/delta^7),
    A = soft-O(T R^3/delta^3),
    preparation programs = soft-O(T^2 R^10/(beta^3 delta^8)).

For A, use sum_l r_l<=1/w, F=soft-O(T/w^2), and C=soft-O(1/w).
Add m training targets and A preparation targets, plus polynomial(q) gates
per program interaction and paid synthesis. These are conservative upper
bounds, not optimal exponents. Polynomial in numeric R is not polynomial
in log R, and the bound is not independent of the supplied-copy acquisition
cost if that cost is later included in an application.

For the legal three-level example above with T=1 and offset 128, the actual
calculator reports m=56,623,104 training targets, F=6,723 filtered requests,
C=3,072 trials per request, A=20,653,056 filter targets, and
eta=1/330,448,896. Those numbers exclude the far larger DME program budget.
The report explicitly marks total raw-copy budgeting and quantum preparation
as unimplemented (`mixed_spectral_source.py`, lines 228-242).

The input contains physical copies and controlled U, not a spectrum table,
purification, inverse preparation circuit, conjugate copies, or uniform
eigenvector sampler. The finite tests' spectrum tables grant strictly more
classical information and cannot be a matched classical lower bound.
[Holt--Subramanian, Sections 10.2 and 10.4](https://arxiv.org/html/2609.38085v2#S10.SS4)
use evolution access for the Hamiltonian route and separately formulate
mixed-copy conjugation learning. Their normalized Frobenius promise cannot
simply replace this trace-gap promise. For example, rho=|0><0| and a swap
of |0>,|1> have trace gap one but normalized Frobenius gap sqrt(2/2^q),
even at rank one. This is only a norm-conversion falsifier, not an oracle
separation or an application claim.

A same-input benchmark is per-element testing using two-copy SWAP
measurements. Set D_g=Tr(rho^2)-Tr(rho U_g rho U_g^dagger). Since the
difference of these states has rank at most 2R, a nonsymmetry has
D_g>=delta^2/R, whereas a symmetry has D_g=0. Estimating the two overlaps
therefore costs O(R^2 delta^-4 log(1/xi)) copies per g at failure xi.
Enumeration gives a |G|-scaled benchmark, not an efficient general learner.
This is a quantum measurement baseline; calling it classical would conceal
the measurement-access distinction. No unrestricted classical time lower
bound follows without specifying the classical measurement and input model.

## Verification And Next Action

Experiments performed, with no report regeneration or persistent test files:

- All 27 scoped pytest tests passed in 1.55 seconds using
  `PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
  /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error
  tests/test_mixed_spectral_source.py`.
- Supplemental in-memory exact-rational checks covered four spectra,
  including a 2^-100 tail/internal gap, with upper bounds 4, 9, and 17:
  48 profiles and 69,120 weighted-rank bias checks passed. Maximum bias
  including both contamination allowances was approximately 0.01562977,
  below 1/32. Exact bad-offset enumeration also satisfied its bound.
- Ideal finite-QPE cleanup preserved the entangled dyadic control above to
  floating-point error below 3e-16; measuring the label gave error 1/2.
  For spectrum (0.46,0.34,0.20,0), threshold 0.30 and a maximally entangled
  target/reference, 6/8/10/12 phase bits gave complete-output trace errors
  0.078727/0.018665/0.001621/0.000467, all below sqrt(2p_max).
  These are known-matrix reference simulations, NOT a DME-based filter,
  experimental quantum execution, or certification of diamond norm.

Snapshot SHA-256 of the scoped inputs:

    research/REES_MIXED_SPECTRAL_SOURCE.md
    376c47b3468aa7bcdda1494f3296c442c58c13d7cfa108f51b070af1bf8060a5
    theorems/mixed_spectral_source.py
    761e1716ffd8bd1613bcc2af9057163ca11157e99e3d316801692f654ecaf81e
    tests/test_mixed_spectral_source.py
    161ded47d5fe4e649d10bae4329027c29b2461bc55f26a69016a316dee187751

**Next action:** compile and independently test one complete copies-only
threshold/rank/factory path with fresh traced-out program states, retaining
accept, reject, and abort outputs and the entangled-reference cleanup
falsifier. Make the grid identity immutable across requests and record every
raw target/program copy. Do not regenerate more supplied-spectrum profiles
and count them as that verification. Until then, retain the written
source-reduction conclusion and its explicit primitive/receiver premises;
make no implementation, novelty, or speedup promotion.
