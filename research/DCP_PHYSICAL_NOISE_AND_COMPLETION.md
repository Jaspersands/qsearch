# Physical Phase Noise And Noisy DCP Completion

LOCAL DERIVATION / REVIEW PENDING. No independently reviewed theorem, novelty,
full residue decoder, native-noise reduction or speedup claim. This is a source
audit and conditional interface, not a new accepted algorithm candidate.

## Research Decision

Do not promote the previous IID logical-output noise obstruction to a native
DCP obstruction. Physical error location, source dependence and register
correlations matter. The correct next algorithmic target remains constructive
unknown-residue inference at growing modulus, not more constant-noise plots.
The conditional completion/verifier results below can close the final step
of a future decoder; they do not supply its hard first step.

Read `DCP_BELL_INFERENCE_KERNEL.md` and `DCP_FULL_BELL_SOURCE_MOMENTS.md` for the
ideal source/measurement definitions. Here q is a power of two >=8, Q=q/2,
n is vector dimension, and k=2n for native n-by-3n systematic packets.

## Original Physical Errors, Not Logical IID Errors

A public affine parity chart writes the original binary variables as x0+Kz.
A physical Z mask e multiplies the branch amplitude by (-1)^(e.x0+e.Kz).
Its global factor disappears, leaving logical mask K^T e. For a Bell pair,
eta=K1^T e1+K2^T e2, over F2. All original syndrome outcomes remain uniform
under this phase-only channel. A bit flip, arbitrary basis failure or other
channel does not automatically inherit this statement.

For independent physical bits with rates epsilon_i, the logical error
Fourier coefficient is

    phi(h) = product over both packets, rows i with (Ki h)i=1 of (1-2 epsilon_i).

For a declared classical joint physical-mask distribution, instead use
phi(h)=E_e[(-1)^(eta.h)]. `IndependentPhysicalZ` supports scalable Fourier
evaluation without enumerating 2^(m1+m2) masks. `SparsePhysicalZ` supports
explicit correlated distributions, including across packets, with cost
polynomial in the supplied support. Dense mask enumeration is bounded
calibration only. No arbitrary quantum channel is represented by these types.

For a fixed public low chart and effective secret character order >=4, with
native higher labels independent of the error law, the exact source mean is

    E_high [2^k sum_v p_noisy(v)^2] = sum_h phi(h)^2 2^(-R(h)),

where R(h) is the binary rank of physical rows selected by Ki h in both
packets. This follows by the source-character fourth-moment calculation and
the Fourier multiplier of the classical XOR channel on Bell output v.
The rank sum remains exponential in k; it is not an efficient decoder.
The source independence declaration is not programmatically proven.

Two countercontrols are mandatory:

- IID original physical errors generally produce nonindependent logical bits.
  The complete 64-mask example records joint error != product of marginals.
- On identical charts, shared physical errors e1=e2 cancel in eta. A two-point
  joint mask law with first-bit marginal 1/2 retains the clean Bell collision.
  Marginal noise rates alone cannot imply the IID obstruction. This is a
  correlated-source counterexample, not a tensor-product native promise.

## Native Weighted Source Mean

Condition each native low n-by-3n matrix on its first n columns being
invertible. Charge the pair prefix probability

    p_prefix = [product_(j=1..n)(1-2^-j)]^2.

The two systematic charts each have k free unit rows and n independent uniform
pivot rows. Put a=(1-2 epsilon)^2 and N=2^k. Disjoint physical directions h,j
give the exact IID original-phase-error source mean

    Cbar = [N + ((1+a^2)^k-1)((1+a)/2)^k
              + ((2+a^2)^k-N-(1+a^2)^k+1)((2+a)/4)^k] / N.

Explanation: h=0 contributes N; j=0,h!=0 contributes the second term. For
nonzero disjoint h,j the free-coordinate weighted triple sum is 2+a^2 per
coordinate. Each pivot permits (0,0),(0,1),(1,0), with total expectation
(2+a)/4. Remove h=0 and j=0 before applying that independent-direction law.

Leading bases are (2+a^2)(2+a)/8 and (1+a^2)(1+a)/4. Constant epsilon=1/16
puts both below one. Vanishing epsilon=1/n^2 need not: it is deliberately
retained as a control, not ruled out by a constant-rate calculation.

For uniform packet residue, order<=2 exception mass rho=(2/Q)^n, and T
supplied independent pairs fixed BEFORE their higher labels, discard all
quantum data on failed prefixes and retain every noisy Bell v on success.
An exact conservative joint public-source/output information certificate is

    KL_bits <= T p_prefix [2(1-rho)(Cbar-1)+rho k],
    P(recover negation orbit) <= min(1,2/Q^n+sqrt(KL_bits/2)).

The reference retains public higher labels; they are not averaged away from
the learner. This uses the source mean to bound expected conditional KL,
then a joint KL bound and Pinsker. It charges 6nT original states. At
n=q=256, T=n^2, epsilon=1/16 the certified success is below 1/100. This
closes only that fixed noisy measured protocol, not adaptive matching,
quantum memory, encoded inputs, arbitrary measurements or native basis noise.

## Noisy Candidate Completeness

The old noiseless all-zero packet test is NOT perfectly complete with physical
Z errors. For a known correct residue, its native systematic mean acceptance
is the probability K^T e=0:

    (1-epsilon)^(3n) + 2^(-2n)[1-(1-epsilon)^n].

To derive it: zero pivot mask requires every free error zero; any nonzero
pivot mask yields a uniform logical syndrome when averaging the IID pivot
rows. A wrong residue committed before independent higher labels still has
source mean acceptance 2^(-2n). Do not turn either source mean into a uniform
per-instance guarantee or reuse ideal completeness at constant noise.

## Actual Reduction Promise

[Regev, Quantum Computation and Lattice Problems](https://cims.nyu.edu/~regev/papers/quantum_average.pdf),
Definition 2.1 and Theorem 1.1, permits rare arbitrary computational-basis
registers instead of cosets, with a failure parameter. Position Fourier
measurement then gives a uniform public label but a basis qubit on a failed
register. Such failures need not be unbiased, equatorial or independent of
source/history. They can change subsequent chart syndrome probabilities.
The paper's lattice approximation and failure parameters must be mapped
explicitly; no standard LWE or automatically robust decoder claim follows.

Important refinement: the EXISTING prelabel X/sign gauge can legally balance
basis failures if their mask/bad bits precede uniform Fourier labels and old
labels/coins are discarded. Independent fault statuses then transfer to
physical phase flips at HALF the basis-failure rate; correlated faults retain
a fault-avoidance Fourier law. See `DCP_PRELABEL_GAUGE_SOURCE_MOMENTS.md` for
the source-linked extension and the exact correlated native formula. This is
preprocessing, not a lossless equivalence of arbitrary basis noise. Do not
interpret the raw-channel rejection gate below as forbidding that transfer.

`noise_promise_gate` rejects substituting arbitrary basis contamination for
IID physical Z errors. Passing it means declarations are internally adequate
for a named transfer, NOT that the source promises have been proven.

## Known-Residue Binary Experiment

If the CORRECT r=s mod(q/2) is known, correct fresh ORIGINAL states by r.
The remaining secret is a binary vector b, and pure phase-flip noise yields

    rho_b(A) = [I+(1-2 epsilon)(-1)^((A mod2).b) X]/2.

All states commute in the PUBLIC X basis. Measure H then Z to obtain classical
samples a uniform in F2^n, y=a.b+Bernoulli(epsilon). Conversely, given a,y,
prepare H|y> and preserve a: this exactly recreates the quantum experiment.
For classically correlated masks the joint experiment is still diagonal,
but its classical errors are correlated and are not automatically IID LPN.
This proves neither a polynomial classical LPN solver nor a ban on quantum
computation on classical LPN samples. Wrong r, only retained carry packets,
nonphase channels and an unavailable fresh-original-state source do not pass.

Quantum-example algorithms have a different input model:
[Cross, Smith and Smolin](https://arxiv.org/abs/1407.5088) study noisy quantum
learning access; [Grilo, Kerenidis and Zijlstra](https://arxiv.org/abs/1702.08255)
study quantum samples for LWE. Neither supplies a coherent example oracle
from these classically tagged one-qubit samples. Such a source transfer is a
new proof obligation, not a literature shortcut.

## Basis Bias: Counterexample And Constructive Filter

After correct r, take contamination probability gamma and a fixed bad basis
bit j: rho_p=(1-gamma)|X_p><X_p|+gamma|j><j|. The opposite-parity states have
commutator Frobenius norm squared 2 gamma^2(1-gamma)^2. Thus X measurement
need not be lossless. Random I/X twirling AFTER correction legally removes
the bias, giving flip rate gamma/2; this is degradation, not full equivalence.

Critique of that obstruction: if gamma<1 is a PUBLIC CONSTANT and j is PUBLIC,
there is a better heralded filter. Attenuate amplitude of |j> by
a=sqrt((1-gamma)/(1+gamma)), preserving the other basis amplitude. Success
probability is 1-gamma, independent of parity, and the conditional state is
[I+(-1)^p a X]/2. Failure is a secret-independent basis branch. H measurement
gives LPN flip rate (1-a)/2, strictly better than gamma/2 for 0<gamma<1.
Expected fresh inputs per success are 1/(1-gamma); charge discarded inputs.

An unerased sample y at this adjusted LPN rate can recreate the original rho
by preparing sqrt((1+gamma)/2)|j>+(-1)^y sqrt((1-gamma)/2)|1-j>.
This is a two-direction SAMPLE-CONVERSION interface with heralded loss in
the forward direction, not lossless one-copy equivalence. Unknown or
label-dependent bias, wrong r and arbitrary hidden Regev bad bits do not
inherit it. Symbolic 2-by-2 checks prove these identities locally; a physical
filter compiler, approximation error and source transfer remain unverified.

## Classical Clean Blocks And Robust Full Verification

For known correct r, L=n+lambda original binary samples have rank-failure
bound f=(2^n-1)2^-L. Binary elimination gives correct completion whenever the
block is clean and full rank. IID label-independent flips give lower success
(1-epsilon)^L(1-f). Only marginal flip bounds, even with correlations and
label dependence, give max(0,1-L epsilon-f), provided the native label-rank
law itself holds. Verify any resulting full candidate on fresh states.
At n=128, epsilon=1/n^2, lambda=40 both lower bounds exceed .98. At constant
epsilon=1/8 the IID bound is tiny. This is a useful low-noise classical
baseline, not a constant-rate LPN solution. The actual reduction's gamma(n)
must be derived; log N cannot silently be replaced by n.

A fixed FULL candidate committed before fresh uniform native labels admits
robust verification against arbitrary bad states. Require the bad probability
<=gamma<1/4 conditioned on EACH fixed secret and prior history, not only
unconditional register marginals. Ideal correction/projection has correct
zero-vote probability >=1-gamma; wrong probability <=1/2+gamma. Accept at
ceil(3M/4) zero votes. Conditional bounds imply binomial stochastic envelopes:

    FPR <= Bin(M,1/2+gamma) upper tail,
    FNR <= Bin(M,1-gamma) lower tail.

At M=256,gamma=1/16 the exact bounds are FPR<1e-7,FNR<1e-20. Arbitrary bad
states may depend on secret, label and history within that conditional budget.
Merely marginal bounds cannot amplify: a shared bad-block event can retain
error gamma at every M. This certificate assumes ideal gates and corrections;
precision/hardware error is NOT yet included. It verifies, never discovers.

## Artifacts And Falsifiers

Theory modules: `theorems/dcp_physical_phase_noise.py` and
`theorems/dcp_noisy_completion.py`; generators accept `--save`. Reports live
under `research/phase_workbench/` with matching names. Tests check physical
transport, full-source convolution, native weighted formulas, correlated
cancellation, 64-logical-bit nonenumerative interfaces, promise rejection,
binary reverse channels, symbolic public-bias filters and exact tail bounds.
The independent Node certificate redoes bounded physical/source counts and
large exact rational arithmetic, not independent theorem review.

Reject any use that assumes IID logical errors, ignores source-dependent
corruption, imports free coherent examples, applies correction before knowing
the correct residue, silently drops failed inputs, claims uniform completeness
from a source mean or calls a verifier a decoder. Reassess the next decoding
proposal against ideal growing-q sources first; then compose its ACTUAL
noise promise and natural-problem reduction. No accepted candidate is created
by this audit. Routine CLI/registry wiring remains Gemini work.
