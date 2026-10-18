# Joint Block Readout, Local Blindness And A Product-Measurement Baseline

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty, efficient decoder,
natural-source certificate or quantum speedup is claimed.
Run `python qsearch.py dcp-correlated-block-observables`.

## Research Decision

Do not compress the retained block into a list of one-qubit marginals. The
full syndrome/X outcome can contain secret information while every low-order
X correlator vanishes. Conversely, discarding the syndrome gives an exactly
reproducible product-measurement mixture; that is not evidence of collective
measurement advantage. Keep BOTH the syndrome and the joint outcome, account
for their correlated law, and charge the inference problem.

This pass implements bounded complete likelihoods to falsify readout ideas,
not a scalable likelihood oracle. Native asymptotic statements below are
analytic bounds, never extrapolations from these selected small controls.

## 1. Complete Physically Defined Readout

Start from the correlated-block gate primitive: measure
y=A*x mod4 componentwise, retaining all m original quantum wires. Then apply
H to every retained wire and measure the COMPLETE X string z. No syndrome
is selected/rejected and no original Boolean address is erased.

For the clean input, the joint Born law is

    P(y,z|s)=2^(-2m)*|sum_(x: A*x=y mod4)
              exp(2pi*i*s.(A*x)/2^t)*(-1)^(z.x)|^2.       (1)

This includes the syndrome probability D_y/2^m; using1/D_y instead would be
an uncharged conditioning error. Empty fibers have probability zero.
Only s modulo2^(t-2) affects probabilities: the syndrome contributes a global
phase. This is why the calibration enumerates residual, not full secrets.

Independent original Z-error probabilityp=(1-v)/2 commutes with the diagonal
syndrome measurement. Final H readout turns it into independent bit flips:

    P_noisy(y,z|s)=sum_e p^|e|*(1-p)^(m-|e|)*P_clean(y,z XOR e|s).

The implementation uses SciPy's Hadamard transform and the Walsh eigenvalues
v^|u| of this binary-symmetric channel. Direct density/gate tests and a
separate straightforward JavaScript complex-sum/convolution replay check it.
All secrets, syndromes, addresses and full likelihood entries enumerated in
the finite calibration are reported. Larger instances return UNKNOWN.

Uniform-prior mutual information and optimal one-copy Bayes success are
properties of the resulting CLASSICAL observation channel. Computing their
full tables is exponential. They neither implement an unknown-secret decoder
nor show that a compact or polynomial-time likelihood representation exists.

## 2. Exact Baseline When The Syndrome Is Discarded

Pinching in coarse syndrome sectors is equivalent to averaging conjugation by

    D_k|x>=exp(2pi*i*k.(A*x)/4)|x>, k uniform in Z4^n.

Each D_k factors into single-qubit Z rotations. Therefore sum_y P(y,z|s)
is reproduced by choosing a uniform PUBLIC k, rotating each raw phase qubit
by its known coarse phase and measuring every qubit in X. Conditional on k,
the z bits have a product distribution with means

    v*cos(2pi*(s.A_i)/2^t + 2pi*(k.A_i)/4).

There is no entangling syndrome circuit in this baseline. It REQUIRES access
to the individual raw phase qubits (or the corresponding phase-measurement
sampler); known s is used only to calibrate the likelihood here. It is NOT
a classical simulator/solver for unknown-secret DCP.

This twirl reproduces z after forgetting y, NOT the joint (y,z) source.
The Fourier-dual random variable k must not be relabeled as the measured y.
Adding their likelihoods as independent observations is equally invalid.

## 3. Why Low-Order Observables Can Be Exactly Blind

Suppose public coarse A has NO nonzero v in{-1,0,1}^m of support<=k with
A*v=0 mod4. Any two Boolean addresses differing on at mostk coordinates
have different coarse syndromes. Thus in EVERY measured fiber, every
off-diagonal element of every at-most-k-qubit reduced density matrix is zero.
Its diagonal is independent of s because the original diagonal is flat.
Consequently all such reduced states are SECRET-INDEPENDENT, even with no
noise. Every nonempty X parity of degree<=k has zero expectation conditional
on each nonempty syndrome, so the X readout is k-wise uniform.

This statement is about reduced states/low-degree statistics, NOT all
protocols with local measurement gates. Measuring all qubits locally and
computing a HIGH-DEGREE parity can reveal a correlation. The finite control
with columns(1,0),(0,1),(5,1),(1,2) has minimum signed coarse relation weight3.
Its one- and two-bit X marginals are uniform for every syndrome, yet its
complete joint outcome contains secret information. This is a required scope
counterexample, not a new algorithm or native advantage estimate.

## 4. Native Probability And Simultaneous Information

For each fixed nonzero signed relation, a unit coefficient makes all n coarse
components uniform, so its zero probability is4^-n. A union bound gives

    Pr[exists signed relation of support<=k]
       <=4^-n * sum_(w=1)^k binom(m,w)*2^w.              (2)

Opposite signs name the same event and could tighten this bound, but are
deliberately overcounted here. Mask events need NOT be independent.

For m4n and k=floor(n/4), bound the coefficient sum using z=1/32:

    sum_(w=1)^k binom(m,w)*2^w
       <=32^k*(1+2/32)^(4n)
       <=2^(5k+ceil(n/2)), since (17/16)^8<2.

Hence (2) is at most2^(-[2n-ceil(n/2)-5floor(n/4)]), at most2^(-n/4)
when n is divisible by4. This is exact integer rounding, not a fitted entropy
exponent. The bound is a native probability statement, not pointwise in A.

The companion source-information result at t=n+8,v=1-1/n gives retained
Holevo>=max(0,2n-2ceil(log2 n)-6), outside probability2^(-n^2). A union bound
therefore yields BOTH linear retained Holevo AND complete blindness of all
at-most-n/4 local reduced states, except the explicitly charged sum of these
exceptions. The full classical X readout need NOT attain that Holevo value.

This is the concrete research challenge: exploit global information without
granting a fiber inverse/normalizer or mistaking low-degree blindness for a
general quantum-measurement lower bound. It also gives a clear falsifier for
local-observable/low-degree-feature searches that report a spurious signal.

## What Is Likely To Fail Next

1. Full likelihood evaluation may remain exponentially hard. Knowing that a
   channel is informative does not provide a statistical or computational
   inference algorithm. Enumerated Bayes/MI are calibration ceilings only.
2. The observed information in selected small cases may vanish or change
   structure under growing modulus and native labels. No scaling claim uses it.
3. Dropping y is exactly matched by the product-measurement baseline. Keep a
   syndrome-aware likelihood or abandon that route as a collective advantage.
4. One-body and low-degree metrics are typically blind; a positive numerical
   result should first be checked for a short signed relation, conditioning,
   sampling error or data leakage. Conversely their failure does not kill
   the full outcome, as the weight-three countercontrol demonstrates.
5. A classical inference algorithm for these quantum-produced observations
   would not classically simulate the raw source, but must still be compared
   to direct product readout on the same paid phase-state budget.

Next high-judgment target: identify a compact syndrome-aware sufficient
statistic or structured full-output inference method that survives the native
local-blindness bound, then test an actual growing-modulus cost claim. A bank
of independently treated parity likelihoods is not such a method.

## 5. Exact Native Fourth Moment Of This Full Readout

The complete outcome is informative in finite controls, but how much of the
block's native information does it actually extract? There is an exact
source-average calculation, stronger evidence than scaling those controls.
Let G=4^n,M=2^m and Q(y,z)=1/(G*M), with all possible syndromes including
empty ones. Assume t>=4 and FIX a residual secret with an odd component.
For independent original visibilityv in[0,1], define

    kappa = G*M * E_A sum_(y,z) P(y,z|s)^2.

Then exactly

    B=(1+v^2)^m, C=(2+v^2)^m,
    kappa = G/M + (M+B-2)/M + (C-M-B+1)/(G*M).           (3)

Proof sketch with every source dependence charged: expand the squared Born
probability using four Boolean addressesx1,x2,x3,x4. Summing over z forces
x1 XOR x2 XOR x3 XOR x4=0. Write original labelsA=A0+4H and average over
the independent higher lifts. Because the residual secret has an odd
component and residual modulus>=4, each column's character average forces

    x1-x2+x3-x4=0 AS AN INTEGER VECTOR.

Its possible coordinates are0,+/-2 after the XOR condition; nonzero2 does
not vanish in residual modulus>=4. Thus the surviving quadruples are Boolean
parallelograms. Write x3=x1 XOR u, x2=x1 XOR w, x4=x3 XOR w with w subsetu.
The noise weight isv^(2|w|).

There are three native coarse-rank classes:

- u=0: one choice ofw, rank zero, weighted count1 per anchor.
- u!=0 and w=0 oru: one coarse relation, weighted totalM+B-2 per anchor.
- 0<w<u: two distinct nested signed supports have a unit2x2 minor modulo4,
  so their sums are jointly uniform. Weighted countC-M-B+1 per anchor.

The coarse survival probabilities are1,1/G,1/G^2, respectively. Accounting
for M anchors and the Born/Walsh normalization gives (3). No IID fiber-entry
or independent-mask heuristic appears in this derivation.

The module independently enumerates ALL4096 original q16 label triples at
n1,m3. For odd secret1 it gets kappa21/8 at v1,201/128 at v1/2,11/8 at v0.
For EVEN secret2, v1 instead gives17/4. Consequently the primitive-secret
formula MUST NOT be averaged over the entire prior without charging that
exception. At residual modulus2 the character step also fails; t3 controls
remain legitimate finite likelihood tests but cannot use this fourth moment.

## 6. One-Bit Native Readout Frontier, Not A Decoder No-Go

At m3n and v<=1, noise is an L2 contraction for each public A. Thus (3) is
bounded by its clean value, which obeys

    kappa <=2+2^-n+(27/32)^n.

Relative entropy to Q is at mostlog2 of the collision multiplier. Jensen
therefore bounds mean KL, for EACH fixed primitive secret, by log2(kappa).
For a UNIFORM residual secret, the all-even class has probability2^-n.
Use the crude output-alphabet KL boundm+2n=5n on that class, NOT its collision
moment, which can be much larger. We obtain

    E_A I(S;Y,Z |A)
       <=log2(2+2^-n+(27/32)^n)+5n*2^-n.                 (4)

This tends to ONE bit per batch, even in the noiseless case. It is a source
AVERAGE, not an upper bound for every favorable public matrix. Public A is
included in the transcript and Q may have mass on impossible syndromes;
that only makes this divergence upper bound looser, not invalid.

For exact compact artifacts, (27/32)^5<1/2 and log2(1+x)<=2x imply

    (4) <=1+2^-h,
    h=min(floor(n/5)-1, n-ceil(log2(5n)))-1.

The saved n>=64 profiles use nonnegativeh. The all-even contribution is
explicit in this integer rounding, rather than hidden in a fitted exponent.

T independent fresh batches with this FIXED unrotated physical readout have
transcript information<=T*(1+2^-h). One may prove this via KL to the product
reference, averaging the fixed-secret bounds under the ORIGINAL prior;
resetting an adaptive posterior to uniform would be wrong. Arbitrary later
classical inference is permitted, but adaptively secret-aligned physical
bases, coherent inter-batch measurements, external side information and other
readout circuits are different protocols.

There is an additional identifiability defect: this circuit is real, so it
aliases s and-s exactly. Full identification is bounded by
(1+(2/Q)^n)/2, Q=2^(t-2), regardless of sample count. The original full-secret
sample target was therefore not a feasibility claim. The corrected benchmark
targets the NEGATION ORBIT under the original uniform-secret prior. Its
entropy is at least n*log2(Q)-1 and orbit alphabet at most Q^n, so Fano gives

    T >= ceil((3*n*(t-2)/4-2)/(1+2^-h)).                 (5)

Every batch consumes3n original phase qubits. This is only a POLYNOMIAL sample
lower bound, not a computational hardness claim or rejection of all efficient
algorithms. A good polynomial-time classical inference algorithm for enough
of these quantum-produced observations could still matter.

The retained block, at t=n+8,v=1-1/n,m3n, has Holevo at least
max(0,n-ceil(3*(ceil(log2 n)+3)/2)) except probability2^(-n^2-2n). Thus this
specific terminal measurement loses a linear factor of the raw information
in the native mean. That sharpens the research choice: improve the collective
readout OR solve the genuinely structured full-outcome inference problem;
do not confuse surviving Holevo with what this easy measurement extracts.
The public complex-axis successor in DCP_COMPLEX_AXIS_READOUT.md repairs
the conjugation alias but still does not provide efficient inference.
