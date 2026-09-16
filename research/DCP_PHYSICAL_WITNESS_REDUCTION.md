# Physical DCP Measurements Yield Witnesses, Not Necessarily Uniform Fibers

Status: corrected derivation and executable adversarial controls; REVIEW PENDING.
No new DCP decoder, speedup, independent review, formal proof or novelty claim.

## The Proof Error

The previous arbitrary-measurement reduction worked in the span of normalized
uniform subset-sum fibers. Physical input states lie in that span, but an
arbitrary measurement effect need not preserve it. Compressing its effects
preserves forward outcome probabilities on the ensemble. It does NOT provide
a circuit implementing the compressed effects' inverse.

Consequently, the earlier inference to *uniform* fiber preparation was false.
The witness-finding reduction survives in the full assignment space, and can
be simplified to avoid matching-garbage normalization entirely.

## Full-Space Statement

Fix public labels a=(a_1,...,a_m) modulo N. On the M=2^m Boolean assignments,
let f(b)=a.b mod N, P_s project onto ALL assignments of residue s, and

    |psi_d> = M^(-1/2) sum_b omega^(d f(b)) |b> = U_d |psi_0>.

Write c_s=rank(P_s), pi_s=c_s/M, S={s:c_s>0}, L=|S|. The uniform fiber F_s
is one vector in the generally larger range of P_s.

Assume a supplied, efficient, reversible STATE-ONLY decoder circuit. Its
workspace and inverse are accessible; any classical randomness or deferred
measurements are retained coherently. It does not call an additional unknown
hiding-function oracle or request fresh unknown states inside the decoder.

Coherently choose uniform r, apply U_r, run the decoder, and subtract r from
its computational output. Keep r as workspace. The resulting effects obey

    E_d = U_d E_0 U_d^dagger,
    <psi_d|E_d|psi_d> = p,

where p is the original success averaged over the hidden shift, for THIS
public label tuple. The same circuit remains uniformly efficient over labels.
This construction does not assume the optimal PGM, rank-one effects or a
known positive lower bound on p.

The original decoder need not first measure or preserve its Fourier-label
registers. For the inversion reduction, the label tuple is a classical input:
initialize those registers to its known value and include them in the retained
workspace. Their initialization can be reversed and its success flag charged.
This defines an accessible input isometry V_a on the assignment register,
even if the supplied decoder subsequently mixes the quantum labels. Unlike
the uniform-fiber compression, this input restriction has an explicitly
efficient preparation. A full-unitary control below checks this distinction.

## Two-Call Unamplified Wrapper

Let V be the accessible symmetrized decoder dilation, with outcome d and
arbitrary retained workspace. The following circuit has a well-defined block:

1. Compute V on an arbitrary input and clean workspace.
2. Copy its computational outcome into a separate retained register D.
3. Uncompute V, retaining D. This copies an orthogonal label, not an unknown state.
4. Controlled by D=d, unprepare the PUBLIC known-shift state psi_d on the input.
5. Select the all-zero input/workspace block, retaining D.

Known-shift preparation uses Hadamards and public modular phase arithmetic;
it does not use a hidden shift or a subset-sum fiber table. Directly inserting
the copied-outcome projectors shows that this block is

    K0 = sum_d |d><psi_d| E_d.

Its construction uses one decoder call and one inverse call. There is no
amplitude amplification or success estimation. The all-zero selection is a
heralded branch whose probability MUST be charged, not free postselection.

Put zeta=E_0 psi_0 and zeta_s=P_s zeta. Covariance and Fourier orthogonality give

    QFT_N K0 = sqrt(N) sum_s |s><zeta_s|,
    (QFT_N K0)^dagger |s> = sqrt(N) zeta_s.

Invert the block after inverse QFT on a supplied target. The branch probability
is q_s=N||zeta_s||^2 <=1. Conditional on that branch, computational measurement
returns a valid witness b with f(b)=s. If zeta_s=0 it simply fails. No claim
about uniformity within a fiber is made.

## Success Without Occupancy Or Good-Label Selection

For the uniform-legal target law, Cauchy--Schwarz gives

    p^2 = |<psi_0|zeta>|^2 <= sum_s ||zeta_s||^2,
    E_uniform-legal q_s >= (N/L)p^2 >= p^2.

For the PLANTED target law pi_s=c_s/M, use a different inequality:

    p <= sum_s sqrt(pi_s)||zeta_s||,
    p^2 <= L sum_s pi_s ||zeta_s||^2,
    E_planted q_s >= (N/L)p^2 >= p^2.

Both statements hold at every density, for every fixed public label tuple,
and also at p=0. No Poisson approximation, typical-source theorem, multiplicity
lower bound, or occupancy loss is needed. Neither L nor c_s is computed by
the wrapper; L<=N is used only in its proof.

There is also a bound for targets uniform on ALL of Z_N, without needing a
sampler for legal targets:

    E_uniform-Z_N q_s = sum_s ||zeta_s||^2 >= p^2.

Illegal targets have q_s=0. For a label law Q, conditioning the JOINT
uniform-residue challenge law on legality changes its label marginal. Its
success is the unconditioned success divided by Z=E_Q L/N<=1, and hence is
still at least pbar^2. This argument must not replace the conditional label
marginal by Q while keeping the same decoder average without justification.

For ANY public-label distribution, write pbar=E_a p(a). Jensen then yields

    E_a E_target q >= E_a p(a)^2 >= pbar^2.

Thus inverse-polynomial label-averaged decoder success implies nonnegligible
average witness success at two decoder/inverse calls per attempt. Bad label
tuples may have success zero. The wrapper neither identifies nor discards them.
This is a weak average-case inverter, not a bounded-error guarantee on each
target or label tuple. Repeating on one impossible target cannot repair zero
success, and resampling a different challenge is not allowed for free.

For whole-wrapper operator-norm synthesis error epsilon, the success change
is at most 2 epsilon. Epsilon<=pbar^2/8 therefore preserves at least
3 pbar^2/4 average success. Public arithmetic and QFT errors must be included
in that total. No error is assigned to an imagined ideal measurement: the
implemented reversible decoder defines the actual E_d and actual pbar.

## Optional Normalized Variant

If a positive inverse-polynomial fixed-label success lower bound is supplied,
matching-garbage amplification can normalize zeta by sqrt(p). It gives
q_s=N||zeta_s||^2/p and both target averages >=(N/L)p. That variant incurs its
bootstrap cost and tighter accuracy requirements. It is NOT necessary for
the label-averaged reduction above. The report keeps these contracts separate.

## Exact Counterexample

Take N=2, labels=(1,1), basis order 00,01,10,11. Let

    F0=(|00>+|11>)/sqrt(2), G0=(|00>-|11>)/sqrt(2),
    F1=(|01>+|10>)/sqrt(2), U=diag(1,-1,-1,1),
    E0=(I+|G0><F1|+|F1><G0|)/2, E1=U E0 U.

E0 has eigenvalues 0,1/2,1/2,1; E0+E1=I. These are exact rational matrices.
On psi_0=(F0+F1)/sqrt(2), p=1/2 and

    zeta = E0 psi_0 = (1/2,1/4,1/4,0),
    q_0=1/2, q_1=1/4, E_planted q=3/8 >=p^2=1/4.

The target-zero conditional witness is ALWAYS 00, not the uniform 00/11
superposition. Its unamplified uniform-span leakage squared is 1/8, or 1/4
after matching-branch normalization. This refutes the old inference but not
the repaired witness-support statement. It is a proof counterexample, not a
new toy oracle problem or algorithm candidate.

## Attempts To Break The Repair

- Full-space complex noncovariant POVMs test symmetrization and all residue
  degeneracies. Abstract one-coordinate-per-fiber controls are insufficient.
- An independent complete unitary dilation is explicitly computed, its label
  copied, then uncomputed. Its actual selected block matches the predicted
  probabilities without dividing by p or granting free inverse compression.
- A complex decoder that actually mixes a quantum label register is wrapped
  in a coherent random-shift register. The complete 32-dimensional unitary
  copy/uncompute circuit checks the known-label initialization, all success
  flags, residue support and the averaged squared-success inequality.
- A zero-success covariant decoder checks that normalization is not hidden.
- Highly colliding, singleton-support and low-density labels test the lack
  of an occupancy premise; they are calibration controls, not candidates.
- Exact rational eigenvalues and probabilities verify the counterexample
  independently of the numerical square-root implementation.
- Heterogeneous label-success laws check Jensen including zero/rare successes.
- The separate per-target stratum counterexample remains valid: covariance
  and average success do not imply nonzero success on every target.

The repair would fail if circuit inversion or public-state unpreparation were
unavailable, the decoder used an unprovided unknown-input oracle, some discarded
workspace could not be retained, or the specified target/label laws changed.
No uniform witness-sampling theorem, quantum hardness theorem, or DCP speedup
follows from these checks.

## Research Consequence And Literature Boundary

Do not exclude arbitrary physical measurement architectures merely because
uniform subset-sum fiber states have high entanglement in a chosen layout.
The inverse state can be nonuniform; a single valid witness is itself a product
basis state. Finding that witness efficiently is still unresolved.

The canonical-PGM/uniform-fiber connection is established prior work, not a
discovery here: see Bacon, Childs and van Dam,
[Section 8](https://arxiv.org/html/quant-ph/0501044#S8). Chia and Hallgren study
related basis-mapping and coset-subspace decision restrictions in
[TQC 2016](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2016.6).
Neither a small literature search nor these controls establishes novelty of
the corrected reduction; broader comparison and independent review remain.

The next hard task is to audit whether ANY exclusion in the registry imported
uniform-fiber complexity through the arbitrary-measurement reduction. Repair
only genuinely affected dependency routes, keeping valid canonical-PGM and
explicit uniform-state results. Separately assess constructive nonuniform
witness routes against the appropriate subset-sum and DHSP resource baselines.

## Reproduce

    python qsearch.py dcp-arbitrary-measurement-witness-reduction
    python qsearch.py run EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION

The existing report now contains physical-space controls, the counterexample,
both wrapper contracts and scoped false claim gates. It writes a retraction
record, not a new DCP impossibility claim. All derivations remain review-pending.
