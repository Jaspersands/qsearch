# Original-Data Ceiling For The Noisy Phase Input Bridge

Status: LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This is a statistical
comparison and exact finite quantum-discrimination dual, NOT an efficient
classical solver, a computational lower bound, or a general dequantization.

## The Baseline Must Start Before Phase Preparation

The new input bridge takes classical noisy values C and prepares a known
state sigma_C. Given secret s and public original labels A, the conditional
output is rho_s=sum_C p(C|s,A)*sigma_C. Any subsequent quantum receiver,
including adaptive processing, induces conditional decision probabilities
T(guess|C,A) independent of s. Therefore original classical C statistically
dominates the entire prepared-state experiment. Quantum computation can
still accelerate finding a good decision; the inequality is NOT an efficient
classical simulation of T, an efficient MAP implementation, or dequantization.

Let the prior be pi_s (uniform for the live controls). Define

    w(C)=max_s pi_s*p(C|s,A),
    Gamma=sum_C w(C)*sigma_C.

Then Gamma-pi_s*rho_s is a nonnegative combination of PSD states for EVERY s.
It is an explicit feasible minimum-error quantum-discrimination dual. For
any POVM {E_s},

    P_quantum=sum_s pi_s*Tr(E_s*rho_s)
             <=Tr(Gamma)=sum_C max_s pi_s*p(C|s,A)=P_MAP_original.

This is general: mixed preparations, hidden reduction-side randomness and
complete abort channels can be included in sigma_C. For an unobserved random
mask, average sigma_C over that mask; its law must be independent of s.
If the reduction retains the original classical records as well as quantum
states, their statistical advantage is still bounded by the same data.
Different source access, coherent original oracles, or secret-dependent
preparation not determined by C require a separate analysis.

## Why This Changes Evaluation

A collective native PGM can beat a native local Fourier readout and still
lose to classical MAP on the ORIGINAL noisy-linear values. Calling that gap
an information-theoretic separation for LWE would compare different data.
For any claimed computational advantage the relevant baseline starts with
the same2M original records, their modulus, noise law, time and sample budget.
Classical noisy-linear/lattice/learning attacks must get those original values,
not only the intentionally degraded native measured transcript.

The exact Bayes ceiling may itself take exponential time to compute. A quantum
receiver below it can still constitute a groundbreaking computational speedup
if it is efficient and no comparably efficient classical method is known.
Nor does poor performance of an implemented attack establish hardness.

## Finite Exact Controls, Not Invented Oracle Problems

Use the SAME native input bridge calibration chi(0)=1/2,chi(+/-1)=1/4,
uniform original labels and shared integer secrets. The calibration is NOT
an LWE-hardness source. Precommitted controls are(n,q,M)=(1,3,1),(2,3,1),
(1,9,1),(1,3,2),(2,3,2). Labels are drawn BEFORE evaluation, without rank or
success filtering. Complete source likelihoods sum all3^(2M) original error
vectors per secret, retaining collisions at the modulus.

For each nonzero complete original transcript, store ALL conditional secret
probabilities, its maximum joint weight, the exact native densities and
Gamma over Q(omega_q). Zero-likelihood transcripts contribute zero implicitly;
the ambient q^(2M) space and cap are charged. Each sigma_C is the true product
of known three-branch phase preparations, not a planted-state guess.
The independent checker reconstructs the entire law, exact matrices,
normalization and nonnegative decomposition of EVERY dual difference.

The module also computes exact native F3 outcome likelihoods. Numerical MAP
and PGM success are separately labeled DIAGNOSTICS, not numerical certificates
of quantum optimality. A positive PGM-minus-F3 gap is not promoted as source
advantage. Dense source/reference enumeration is capped and returns UNKNOWN
rather than promoting a truncated law. It is never a scalable decoder.

## Input Quality And Decoder Sample Count Must Be Jointly Chosen

For the continuous Gaussian adapter, V<=q^2*alpha^2/3+1/2. The new bridge's
noise contribution is at most

    M*min(1,(20/3)*alpha^2+10/q^2).

Gate and source-rounding losses are ADDITIONAL. An ideal receiver's success
lower bound epsilon survives this certificate only if ALL losses are smaller
than epsilon. Failure of that sufficient transfer inequality does NOT prove
the noisy receiver impossible: a direct robustness argument could improve it.

At fixed inverse-polynomial alpha, a superpolynomial sample count generally
makes this generic ledger vacuous. Lowering alpha enough to compensate changes
the upstream lattice approximation factor tilde-O(n/alpha); it cannot be
held fixed while advertising a different decoder. The two exact live profiles
use identical n64,q3^64,alpha1/1048576,epsilon1/2 and M512 versus2^40:
the first pre-rounding transfer is positive, the second is vacuous. No receiver
is supplied, and these are pre-rounding profiles, not admitted hardness.

[Boucher, Fouque and Shen](https://arxiv.org/html/2609.34996v1), Proposition5,
already relate binary and cyclotomic coset sources; the repository implements
that known constant-overhead conversion. Their Section6.2 distinguishes a
Gaussian quantum-input result from classical LWE, explicitly warning about
sample supply. Our approximate known-value input route is a DIFFERENT source
adapter, not a license to import their ideal solver without its sample and
noise requirements. No new binary/native equivalence is claimed.

## Falsifiers And Next Constructive Task

Reject a source-advantage claim if it uses the weaker native readout as the
only classical baseline, ignores original records, erases a source cap, or
mistakes statistical domination for efficient simulation. Falsify the dual
by any wrong conditional likelihood, negative coefficient, wrong matrix or
trace. Falsify transfer by missing gate/rounding cost or changed noise/source
parameters. Do not turn a vacuous certificate into a general no-go theorem.

The next useful ALGORITHM task remains an efficient full-label, noncharacter,
collective native receiver or a rigorous original-data classical attack. Its
contract must state growing-root runtime, original samples, workspace,
robustness and receiver success together. Further source wrappers, encoding
renamings and favorable small PGM plots do not resolve that missing mechanism.
