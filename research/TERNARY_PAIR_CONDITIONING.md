# Constructive Local Conditioning And Quotient Sampling

2026-10-20. LOCAL DERIVATION / INDEPENDENT REVIEW PENDING. Known Fourier,
conditioning and BPQM primitives; no new quantum speedup or novelty claim.

Producer: `python theorems/ternary_pair_conditioning.py --write`.
Artifact: `research/reductions/ternary_pair_conditioning.json`.
Tests: `tests/test_ternary_pair_conditioning.py`.

## Decision Question And Alternatives

Can the sampler avoid decoding the nuisance short-codeword directions found
in the preceding sparse-reduction audit? Yes: impose their constraints during
KNOWN source preparation, then coherently decode the remaining quotient.
This removes the full-word obstruction for that new construction, but does
not supply a good residual decoder or a classical separation.

Before extending this direction, the existing polar alternative was checked.
POLAR_SOURCE_DESIGN.md already constructs a matching classical source-shaping
sampler for its certified binary family. Rebuilding the same polar receiver
would not address the objective. This is a local source-aware reduction,
not another claim that code/channel duality itself is new; see
[Renes](https://arxiv.org/abs/1701.05583). The coherent sampling paradigm
remains related to [DQI Gibbs sampling](https://arxiv.org/html/2609.40345v1#S3).

## Public Input And Exact Target

Let H have V rows and N columns over F3, with independent public local
probability spectra mu_e and original public offsets J. The target is

    P_J(x) proportional to product_e mu_e(J_e + H_e^T x).

The native spectra are(0,1/2,1/2), giving uniform satisfying assignments.
Choose g DISJOINT pairs(p,q) of equal nonzero columns of H. Selection must
be fixed from H, not chosen after inspecting favorable residual offsets.
All dependent spin rows and their uniform gauge lifts remain.

On every original affine word y=J+H^T x, the pair difference is already fixed:

    t = J_p-J_q,   y_q=y_p-t.

Compute the THREE known weights and their exact local normalization:

    w_t(a)=mu_p(a) mu_q(a-t),
    m_t=sum_a w_t(a),   nu_t(a)=w_t(a)/m_t.

If m_t=0, the original supported target is empty. Return ABSTAIN with a local
support-contradiction certificate; do not renormalize a zero vector. Otherwise
delete column q, retain offset J_p and replace spectrum mu_p by nu_t. Repeat
for the disjoint pairs. Call the resulting matrix, spectra and offsets
Hbar, nubar, Jbar. For EVERY spin x,

    original_weight(x) = (product_pairs m_t) contracted_weight(x).

Thus normalized spin laws agree exactly. The contracted affine word expands
uniquely by y_q=y_p-t. Rank(Hbar)=rank(H), while the residual decoding dimension
is r=N-g-rank(H), compared with k=N-rank(H) before conditioning. This is a
real reduction of the required decoding task, not a claim that C=ker H can
be decoded accurately despite its short words.

## Actual Source Circuit, Not Postselection

Prepare each retained coordinate with amplitudes sqrt(nubar_e). This takes
known one-qutrit rotations. To expand a pair, append a blank qutrit q,
apply SUM from p to q, then shift q by -t. The implemented total unitary is

    |a,b> -> |a,b+a-t>.

It is defined on every basis state, including dirty inputs. Arbitrary complex
superpositions and entanglement with other registers survive; no branch is
measured or discarded. For native trines, t=0 leaves a trine on the retained
coordinate, while t=1 or2 produces a known point spectrum.

Although product_pairs m_t can be exponentially small, the construction does
NOT wait for that event. It calculates local three-entry vectors and prepares
their tensor product directly. This is legitimate because the public input
gives all local probabilities and the constraints factor over disjoint pairs.
It would NOT be a legitimate transformation of arbitrary unknown physical
DCP/coset inputs: those cannot simply be replaced with re-prepared unknown
phases. The current DQI source is constructed using public label-controlled
phases, not received from an unknown-state oracle.

Local probability arithmetic uses O(g) constant-alphabet operations and
polynomial bit lengths. Pair expansion uses O(g) exact SUM/shift gates. The
reference uses floating local rotations and does NOT supply finite gate-set
synthesis or a useful large-instance residual decoder. Those costs remain.

## Conditional Error Argument

Let Gbar be a basis of ker Hbar. For each fixed local-difference vector t,
write p_t for the normalized contracted product law and define

    psi_u^t = sum_z sqrt(p_t(z)) omega^((u Gbar).z) |z>.

Let A_t be a known coherent decoder for these states with mean word error
delta_t, including all retained records and work registers. A_t and p_t may
depend on H, the public spectra and t, but NOT on the residual syndrome
s=Gbar Jbar. The sampler prepares

    3^(-r/2) sum_u omega^(-u.s) |u> |0> |psi_u^t>,

applies A_t, subtracts its estimate from the label, and applies the adjoint
of that SAME circuit. It then expands the physical pairs, measures and uses
the original Gaussian lift H^T x=y-J with uniform gauge coins. Failures are
ABSTAIN, not free retries or an UNSAT oracle.

For fixed t and UNIFORM s, the existing Parseval proof now applies to the
quotient labels. If a_(s,t) is actual and b_(s,t) the unnormalized comparison,

    E_s ||a_(s,t)-b_(s,t)||^2 = 2 delta_t,
    E_s TV(output,target_extended) <= min(1,2 sqrt(2 delta_t)).

The comparison restricts p_t to Gbar z=s. Pair expansion and Gaussian lift
give exactly the original spin target. Empty residual fibers remain in the
average. For local-empty t, the automatic abstention already matches the
extended target. Source/decoder/gate approximation must still be budgeted.

Uniform original J makes t uniform and Jbar independent uniform conditional
on t, because (J_p,J_q)<->(J_p,J_p-J_q) is invertible. More generally it
suffices that s is uniform conditional on t and the fixed public source data.
An arbitrary correlated-offset distribution does NOT inherit the guarantee
without proving that condition. This is the explicit repair to the prior
IID-offset gap, not a silent reuse of its unconditioned proof.

IMPORTANT: t is an INPUT syndrome. Its law is not the Born probability m_t
of a hypothetical quantum check measurement. Natively these are respectively
(1/3,1/3,1/3) and(1/2,1/4,1/4). Averaging the new receiver with the latter
weights is incorrect. The executed BPQM controls give mean word errors
0.5654352164 versus the incorrectly weighted0.5333380098.

## Complete Bounded Implementation And Falsifiers

The module actually prepares the contracted source from blank registers,
runs the existing modular estimate/uncompute instrument with nonidentical
local spectra, expands the physical pairs by the listed gates and performs
the ORIGINAL affine postprocessing. Its heterogeneous three-wire BPQM root
uses known [q-ary node operations](https://arxiv.org/html/2601.21330v1), with
total dark-space completions and retained herald phases. It is a bounded
reference, not an efficient generic codeword measurement oracle.

For each t, the SAME decoder is built before enumerating all27 remaining
offsets. Correct-adjoint Parseval residuals are below9e-16. Source preparation
is independently compared to its formula; raw expansion is checked on
arbitrary complex inputs, not only valid codewords.

| Receiver | Average TV at t=0 | Average TV at t=1 or2 |
|---|---|---|
| BPQM |0.19444444|0.07407407|
| Product Fourier receiver |0.33333333|numerically zero|
| No decoder |0.66666667|0.33333333|

These controls are repeated affine forms, deliberately classically trivial.
They calibrate the construction, not a new oracle problem or advantage. In
particular, a more accurate codeword decoder need not be the better sampler.
The generic word-error TV bound is vacuous for these imperfect receivers.

A wrong adjoint preserves norm but breaks the identity by0.98093635. Another
countercontrol chooses BPQM only when the remaining offsets all agree and
uses identity otherwise: the identity fails by0.08291454. Merely reporting
average decoding error cannot justify residual-offset adaptivity.

## Matched Classical Proposal And Native Scope

The same local conditioning is available classically. Draw the retained
coordinates independently from nubar, expand the pairs, and attempt the
original Gaussian lift. Accepted samples have exactly the target law.
For each nonempty t, average acceptance over uniform residual s is3^-r.
This improves plain product-source rejection by3^g but is exponential for
growing r. It is not the strongest known competitor: the rank-conditioned
and hash-isolation samplers from the preceding pass remain relevant.
No quantum advantage may be inferred by comparing with unconditioned rejection.

The unchanged saved16-spin input has one disjoint duplicate pair, removing
one of16 decoding coordinates;15 remain. The saved32-spin input has no such
pair; all32 remain. The inventory executes local exact conditioning but NOT
a native quantum receiver. This does not resolve the enormous extrinsic-tree
cost or provide a finite-N quantum sampling guarantee.

For the earlier equality-gadget reduction, pair conditioning makes the local
addition constraints known point-spectrum factors. Eliminating those exact
linear additions recovers the original dense problem and its decoding code.
The construction therefore avoids the full-word short-subcode obstruction,
but does not turn arbitrary dense instances into certified random LDPC codes.

## Revised Priority

Keep this as a source-aware constructive reduction, not a breakthrough
candidate. Reject claims that it is postselection, that full original
codeword recovery is necessary, or that it supplies a generic residual
decoder. Also reject any use of measurement-herald weights for input-syndrome
averages, or of a J-adaptive decoder inside the fixed-decoder proof.

Do not extend duplicate-pair scans or build UI around this calibration. A
larger locally tractable subcode could be conditioned analogously only with
a PAID classical and coherent preparation procedure and a new residual
decoder. Such a proposal must beat the same classical preprocessing. Since
this mechanism does not materially simplify the retained native instances,
the next main-model pass should compare genuinely different source/decoder
families, not keep expanding this local construction by inertia. No central
candidate/proof/negative promotion or Git operation follows from these tests.
