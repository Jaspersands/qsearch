# Native Rank-One Phase Synchronization Is Not Character Recovery

LOCAL DERIVATION / REVIEW PENDING. A concrete failed spectral relaxation and
a polynomial exact character validator, not a noisy decoder or global lower
bound. This replaces redundant identifiability work: the existing
`ternary_covariant_noise.py` already has the full paired noise law,
polynomial-sample identifiability and signed-combination gates.

## Test A Real Optimizer Representation

Original even native level2r gives IID uniform a_i,c_i in Z_q^n, q=3^r.
The existing covariant measurement retains every outcome

    y_i1=a_i.s+e_i1, y_i2=c_i.s+e_i2,
    nu(e1,e2)=|1+chi_q(e1)+chi_q(e2)|^2/(3*q^2).

No chosen-query or coherent-LWE sample access is granted. Classical calibration
uses the exact physical law, not a simulator that can infer an unknown secret.
Original qutrits are charged once; their two errors are correlated.

A natural spectral relaxation uses frequency nodes

    V={0} union_i {+/-a_i,+/-c_i,+/-(a_i-c_i)}.

Use a moment matrix M on these nodes, PSD with diagonal1, and impose ALL
translation equalities M_uv=M_wz whenever u-v=w-z as actual group frequencies.
A genuine secret gives M_uv=chi_q((u-v).s). The objective rewards the three
paired phase features at their observed values. Each source contributes at
most3; the apparent optimum is3 times the number of qutrits.

The module constructs, without the hidden secret, a rank-one alternative:
assign each original a_i exponent y_i1, each c_i exponent y_i2, and each local
sum/difference the corresponding sum/difference of these exponents. Take
M=vv*, v_u=chi_q(h_u). It has EXACT rank1, diagonal1, PSD, qth-root phases
and perfect observed local fit. Yet it generally is not one group character.
This is stronger than a fractional or high-rank SDP counterexample.

## Exact Formal-Difference Certificate

Each node has a formal coefficient vector in Z_q^(2m) specifying its expression
in the independent original public frequencies. Equal FORMAL differences
automatically have equal fake phases. If the actual frequency map introduces
no new difference equality among these nodes, EVERY moment constraint is
satisfied by this perfect rank-one fake, for EVERY observed outcome.

The complete audit compares all K^2 differences, K=6m+1, using exact modular
arithmetic and hash maps. A whole-table preflight cap yields an error, never
a partial successful certificate. It distinguishes an actual frequency
resonance from a phase violation: a resonance could happen to have compatible
outcomes, and neither count is silently identified with the other.

For fixed preregistered templates, any nonzero formal difference residual has
at least one nonzero original-label coefficient. An IID uniform linear
combination is uniform on its coefficient-generated subgroup. For q=3^r,
its zero probability is at most3^-n. For this local A2 vocabulary each raw
residual coefficient has absolute value<=4, so the sharper maximum is
q^-n at q3 and(3/q)^n at r>=2. Union over at most binomial(K^2,2) comparisons
bounds the chance of ANY accidental difference resonance. Polynomially many
fixed nodes therefore usually introduce no global constraints in growing n.

This statement explicitly EXCLUDES label-adaptive template construction.
Gaussian elimination can intentionally build real public relations; their
formal coefficients depend on the labels, so the independence bound no longer
applies. A native-valid resonance countercontrol demonstrates this failure
of scope, rather than promoting the fixed-template result to a global SOS
or synchronization impossibility theorem.

## Character Consistency Is Compact But Nonconvex

Collect all2m frequency rows A. If rank(A mod3)=n, select n independent rows
B. Its determinant is a unit, so B has an inverse over Z_q. The validator
computes B^-1 through a PRIME-field inverse followed by Newton/Hensel lifting

    X <- X*(2I-BX) mod3^(2k).

Do not invoke a prime-only matrix inverse at composite q. That FLINT call
was observed to abort even on an invertible matrix during this investigation.

Interpolate s_trial=B^-1*y_basis. For each public row f_j, set
lambda_j=f_j*B^-1 and derive the EXACT native frequency relation

    f_j-sum_k lambda_jk*B_k=0 modq.

A fake phase fit lifts to a shared character iff

    y_j-sum_k lambda_jk*y_basis_k=0 modq for EVERY j.

The validator retains a nonzero relation and residual as an exact falsifier.
It uses only public rows and outcomes; the calibrated true secret is not
an input. Full unit-rank failure is UNKNOWN, not a false inconsistency proof.
Noise-free honest characters pass. This is not a decoder for noisy records:
interpolating noisy basis outcomes generally produces a wrong candidate.

All character constraints can be written as qth-root multiplicative power
relations using a polynomial-size arithmetic circuit (repeated squaring).
They do not become linear constraints in the SAME small moment matrix.
A dense monomial/SOS expansion can still be exponential. The next section
implements a circuit lift that avoids that expansion, but a solver still
needs a tightness or optimization argument. A polynomial circuit does not
solve itself.

## Constructive Repair: A Polynomial Rank-One-Sound Lift

The module also compiles the label-adaptive public relations into a PSD
representation with polynomially many frequency nodes. It starts with0 and
all native frequency rows, adds repeated-doubling/accumulation nodes to
compute each lambda-weighted basis sum, and identifies the endpoint with its
native target. It separately closes the q-multiple loop for each unit-basis
frequency. Negative nodes are included when needed.

For each addition z=u+v impose the LINEAR moment equality

    M_(z,0)=M_(u,-v),

and conjugation M_(v,0)=M_(0,-v). Each is a genuine equal-frequency-difference
identity. For a rank-one PSD matrix with diagonal1, gauge v0=1; conjugation
gives v_-v=conjugate(v_v), and addition gives v_z=v_u*v_v. The q-loops force
each basis phase to be a qth root. Every native target is the prescribed
product of basis phases, hence is exactly one shared group character by the
unit-basis inverse. The same induction applies to every generated node.

Repeated squaring and relation reconstruction take O(m*n*log q) additions
and a comparable number of nodes; the dense PSD matrix has polynomially many
entries. No full q^n frequency group or dense monomial basis is materialized.
This explicitly REPAIRS rank-one certificate soundness. The old perfect fake
violates retained native-target constraints by its modular syzygy residual.

What it does NOT repair is convex tightness: a feasible higher-rank point
need not be a mixture of genuine group characters, an optimum need not be
rank1, and numerical near-rank1 extraction needs its own error/rounding law.
No SDP solver or efficient decoder is claimed here. Genuine characters pass
every compiled constraint; the counterfeit perfect fit fails. This is a
positive costed representation for the next optimizer experiment, not another
claim that a sparse synchronization eigenvector already found the secret.

## Self-Critique And Repair Beyond Rank One

Removing the rank-one fake alone could merely replace it by a perfect-fit
higher-rank fake. The circuit gives a stronger, quantitative certificate.
Represent ANY feasible PSD matrix with diagonal1 as the Gram matrix of unit
vectors g_v, with anchor g0. For an observed native phase h_j=chi_q(y_j),
write d_j=1-Re(conjugate(h_j)*M_(j,0)) and

    epsilon_j=||g_j-h_j*g0||=sqrt(2*d_j).

Conjugation preserves this error. The addition stencil equates anchored
deficit at z=u+v with half the squared distance between the two appropriately
phase-adjusted vectors at u and -v. Triangle inequality therefore gives

    epsilon_z<=epsilon_u+epsilon_v.

This is NOT a repeated square-root loss. Repeated squaring propagates the
integer coefficient weight. For target row j with public coefficients lambda,
the computed basis product has error<=sum_k lambda_jk*epsilon_basis_k.
The target equality ties its anchor moment to the original native row.
Consequently, if its modular outcome residual r_j is nonzero,

    |1-chi_q(r_j)| <= epsilon_j+sum_k lambda_jk*epsilon_basis_k.

Let Delta=3m-relaxed_score. Every objective feature has deficit>=0, and all
2m native anchor deficits are included. Cauchy--Schwarz and
|1-chi_q(r_j)|>=4/q for nonzero r_j yield

    Delta >= 8/[q^2*(1+sum_k lambda_jk^2)].

The module stores this exact RATIONAL lower bound and the relation producing
it, maximized over failures. Thus NO feasible PSD rank can perfectly fit
inconsistent native phases in this adaptive lift; at q=poly(n) the certified
gap is inverse polynomial. This is a gap to the IMPOSSIBLE perfect score,
NOT a guarantee that the optimum is rank1, that it identifies the planted
secret, or that noisy optimal character score is known. It also presumes
exact satisfaction of all selected stencils; solver residuals need separate
budgeting before using the certificate numerically.

## Source-Mean Integrality Gap And Its Limits

Condition on any fixed labels. The maximum paired noise probability is3/q^2.
Union over the q^n possible shared secrets gives

    Pr[any group character perfectly fits all observed phases]
        <=min(1,q^n*(3/q^2)^m).

This bound needs independent physical qutrit error pairs, not independent
errors WITHIN each pair. Together with the no-resonance bound, it exhibits
a source-mean regime where this sparse PSD relaxation perfectly fits data
while no real character does. This is not a quantitative gap to the optimum
noisy character score, a lower bound on all algorithms, or an LWE attack.
More samples make this false-fit representation problem worse, not better.

The2m independent frequency rows also fail to span mod3 with probability
at most(3^n-1)/(2*3^(2m)): union over the nonzero projective kernel directions.
Subtract all three failure bounds by a union bound to certify a regime where
the local fake is feasible, the character validator rejects perfect fit, and
the unit-basis adaptive compiler is available. Independence between these
three events is NOT required or claimed.

Controls start from actual original native ring labels at roots9/27 and sample
the existing exact readout law with prespecified seeds. The latent secret is
used only by the calibration producer. A planted noiseless countercontrol,
an explicit resonance violation and rank-deficient UNKNOWN case prevent
the validator from treating every apparent signal as failure. Source IDs and
seeds are not evidence for external physical IID supply.

## Revised Research Decision

Reject sparse phase-synchronization proposals that certify success from
perfect fit, PSD or rank1 alone. Require global character validation and
held-out native prediction. Focus any next spectral attempt on LABEL-ADAPTIVE
global relation constraints and a demonstrated tight, costed optimization
representation. The circuit lift now supplies rank-one soundness, so the
next real question is its planted native-source convex tightness and error
behavior; the fixed local vocabulary is already exhausted here.
Classical sample-learning and richer collective quantum receivers remain
open. Known quantum learning algorithms with
[quantum LWE samples](https://arxiv.org/abs/1702.08255) use a stronger input
model; this classical outcome registry does not supply that coherent state.
For context, [angular synchronization](https://arxiv.org/abs/0905.3174)
estimates phase offsets through spectral/SDP methods. Its success does not
automatically enforce the additional group-character relations audited here.

```
python theorems/ternary_character_synchronization.py --write
node research/certificates/ternary_character_synchronization_crosscheck.js
python -m pytest -q tests/test_ternary_character_synchronization.py
```
