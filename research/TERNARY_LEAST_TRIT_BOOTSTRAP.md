# Native Least-Trit Target And Conditional Full Recovery

LOCAL DERIVATIONS / REVIEW PENDING. No higher-root weak learner, full native
secret search, accepted candidate, novelty or speedup is claimed. The research
target is now narrower: an inverse-polynomial advantage for ONE least trit
would suffice, subject to the precise source and cost obligations below.

This follows [covariant noise accounting](TERNARY_COVARIANT_NOISE.md), which
established polynomial-sample identifiability without efficient search.
The current implementation is an exact reduction/source bridge, a receiver
copy gate, and an actual final-field decoder GIVEN an external correct prefix.
It is not an assumed ML or secret oracle masquerading as an algorithm.

## Source And Missing Learner

At even native level2r, q=3^r, the original source supplies independent

    (|0>+chi_q(a.s)|1>+chi_q(c.s)|2>)/sqrt3,
    a,c IID uniform Z_q^n, shared unknown s in Z_q^n.

Wanted: a polynomial-cost learner W that, averaged over ALL uniformly random
secrets, fresh native labels, physical measurements and its own randomness,
outputs s_0 mod3 with probability at least1/3+epsilon. Epsilon must be inverse
polynomial and this guarantee must hold at every lower root needed in the
reduction. The learner may use full public labels and collective quantum
control. It may instead process the covariant classical records, but the
records must come from the stated source; chosen evaluations are not granted.
At a FIXED root, a known random shift can also be applied to fresh classical
covariant records by subtracting a.u,c.u from the outcomes and relabeling
the frequencies. This retains the same paired noise. It does not permit
reuse for independent amplification or the subsequent pure-source modulus
bridge, which requires correcting fresh states before their readout.

W IS MISSING. A success rate in a finite control does not prove this promise.
Primitive-secret success alone is insufficient: at n1 the primitive fraction
is2/3, so success2/5 only implies4/15 average success if nothing is known about
nonprimitive inputs. Assigning chance success to the missing cases is invalid.
The contract rejects primitive-only and chosen-label guarantees.

## Exact Known-Prefix Bridge

Assume a CORRECT known lower prefix p=s mod3^d, componentwise, d<r. On a fresh
original qutrit apply the public diagonal

    diag(1, chi_q(-a.p), chi_q(-c.p)).

With t=(s-p)/3^d and Q=q/3^d, this produces EXACTLY

    (|0>+chi_Q((a modQ).t)|1>+chi_Q((c modQ).t)|2>)/sqrt3.

Every lower frequency pair has3^(2nd) original preimages. Thus two independent
uniform frequency rows remain independent uniform rows, without selecting
labels, losing outcomes, cloning, unknown inversion or frequency-fiber erasure.
The actual even native ring chart at level2(r-d) is checked, not just a formal
phase expression. No secret is used to construct the transformation.

Correctness of p is CONDITIONAL, not checked from planted truth by a decoder.
Wrong p generally leaves non-root-Q phases; the lower-source promise fails.
For adaptive recovery, condition on no previous digit error and use fresh
original states. The earliest-error union argument avoids claiming a valid
source after an erroneous prefix.

Correction is BEFORE measurement. Reducing old covariant records to Q does
not implement this pure source: every proper projection of their paired noise
is uniform. Classical collimation instead has arbitrary noise-phase tags and
attenuated visibility. The two data types cannot be interchanged.

## Average-To-Worst Transfer And Error Symmetry

At a current modulus Q choose a uniformly random known shift u in Z_Q^n,
an independent sign lambda=+/-1, and swap coordinate j with0 using permutation
P. Correct the supplied state by known phases chi_Q(-a.u),chi_Q(-c.u), then
give W ONLY the transformed source with

    a' = lambda * P(a), c' = lambda * P(c),
    t' = lambda * P(t-u).

Here P denotes the same coordinate swap on both rows and secrets, and
lambda^-1=lambda. The physical phase is unchanged by these relabelings.
For any fixed t, t' is uniform over ALL Z_Q^n. Transformed labels are uniform
independently of t'; their joint promised distribution is independent of
lambda. The randomizer's metadata/original labels are NOT added to W's view.

If W outputs v, pull it back as u_j+lambda*v mod3. Let e=v-t'_0 mod3.
The distribution of e is independent of lambda, so the pulled-back error is
lambda*e. If W is correct with probability p>=1/3+epsilon, the two wrong
classes each have probability(1-p)/2. The correct-vs-wrong margin is therefore

    p-(1-p)/2 >= 3*epsilon/2.

The sign is essential. A predictor with errors(2/5,3/5,0) has better-than-
chance correctness but the wrong class wins raw plurality. Symmetrization
changes this to(2/5,3/10,3/10). Random shifts alone do not repair that bias.

For R INDEPENDENT fresh calls, each correct-minus-fixed-wrong vote lies in
[-1,1]. Hoeffding gives exp(-9*R*epsilon^2/8) for that competitor, and twice
this for the trit decision. No amplification guarantee from repeatedly
randomizing the same state/record pool is provided. Record IDs reject shared
ancestors; that check does not by itself prove uniform labels or IID sampling.
Use reset learner workspaces and independent internal randomness per call;
do not retain adaptive quantum memory or expose randomizer metadata to W.

`plurality` only reports empirical counts/ties. It does not certify the
missing learner's guarantee, and no black-box truthful learner is implemented.

## Conditional Full Recovery And Charged Cost

Starting with p=0,d=0, obtain every coordinate's next trit through the above
fresh transformations and amplified W calls. Update p by3^d times that trit
vector, then increment d. All calls for a digit use the prefix BEFORE that
digit; do not mix partially updated coordinates into an inconsistent prefix.
There are nr coordinate-digit decisions. With B fresh qutrits per W call,

    failure <= 2*n*r*exp(-9*R*epsilon^2/8),
original qutrit cost <= n*r*R*B.

The implementation chooses an exact conservative integer

    R = ceil(8*(ceil(log2(2*n*r))+kappa)/(9*epsilon^2))

to obtain failure<=2^-kappa. B and epsilon must bound ALL lower-root calls;
using the worst such bounds overcharges rather than silently ignoring them.
The reduction is polynomial only if W's runtime, B and epsilon^-1 are
polynomial in n,r. Original native-source acquisition is additional. Each
qutrit requires two known root phase rotations and O(n) modular arithmetic
on O(r)-trit values. Charge finite-precision synthesis and aggregate channel
error tau; the complete failure bound then includes tau. No exact physical
phase gate is supplied merely because its numerator is known.
B is a maximum fresh-copy budget per call, not an uncharged conditional
expectation following postselection. The ledger rejects weak contracts that
violate the full-label information copy gate below. Passing that necessary
gate neither implements W nor certifies its promise.

The binary parity-to-full-secret bootstrap is already explicit in Section3
of [Kuperberg's original DHSP paper](https://arxiv.org/pdf/quant-ph/0302112).
This source-level ternary vector/weak-average formulation makes this repo's
access and error obligations precise; no claim that digit bootstrapping is new.

## A Full-Label Collective Copy Gate

There is a necessary copy condition even if W may implement ANY collective
POVM controlled by FULL labels. This is not the previous low-label-only gate.
Let D=3^M,G=q^n. For fixed labels, product words x have public frequency F(x).
Average over s with fixed s_0 mod3=t and all other secret coordinates/high
digits uniform. Matrix elements survive only when

    F(x)-F(z) lies in {0, +(q/3)e_0, -(q/3)e_0}.

The unconditional-secret average retains only difference0. Let Delta_t be
the difference of these two density matrices. For x!=z, F(x)-F(z) is uniform
in Z_q^n under original IID labels: at least one independent frequency row
has coefficient+/-1 or+/-2, all units in Z_q. Hence EXACTLY

    E_labels ||Delta_t||_F^2 = (2/G)*(1-1/D).

For any label-dependent ternary POVM, tracelessness and the positive-part
bound give mean advantage <=(1/6)*sum_t E||Delta_t||_1. Then
||Delta||_1<=sqrt(D)||Delta||_F and Cauchy-Schwarz yield

    mean_success <= min(1, 1/3 + sqrt((3^M-1)/(2*q^n))).

An advantage epsilon therefore requires3^M>=1+2*q^n*epsilon^2. For inverse-
polynomial epsilon this needs M>=nr-O(log(nr)); a few-copy digit shortcut
cannot meet the target. The bound permits polynomial-copy receivers and
does NOT establish computational hardness, fixed-source hardness, or a
per-secret bound. The exact rational ledger bounds the SQUARE OF MEAN
ADVANTAGE, not mean per-label squared advantage. Ancillas/processing cannot
improve this information-only optimum without additional source copies.
Postselected conditional success must include failure outcomes in its cost.

## Information-Only Least-Trit Optimum

A bounded exponential reference shows what W would need to access. Nuisance
fibers are indexed by

    (F_0 mod(q/3), F_1,...,F_(n-1)).

Let eta_(C,k) count words in fiber C with floor(F_0/(q/3))=k. The optimal
uniform-secret least-trit success, for those fixed full labels, is

    sum_C (sum_(k=0..2) sqrt(eta_(C,k)))^2 / (3*3^M).

Why this is an optimum, not merely a plotted POVM: each orthogonal nuisance
block is a three-character pure orbit. Its Fourier square-root frame attains
the expression. If S=sum_k sqrt(eta_k), the dual matrix
S*diag(sqrt(eta_k))/(3D) dominates each block state/3 by weighted Cauchy-
Schwarz, and its trace equals the attained success. Tests explicitly check
the native secret twirl, primal measurement and PSD dual inequalities.

The program enumerates3^M words and supplies NO efficient conditional fiber
state preparation, whitening, erasure, inverse or outcome estimator. A high
reference success is information sufficiency, not an implemented algorithm.
Its smaller nuisance quotient does not remove the fiber compiler obstacle.

## Actual Conditional Top-Digit Closure

For n1/r8,n2/r16,n4/r32, original full-ring random labels are sampled FIRST.
Given an externally supplied correct r-1-trit prefix, the known diagonal is
applied before the real root3 MUB readout. Raw original labels, correction
phases, Born probabilities and outcomes are retained. The existing streaming
cubic incidence decoder recovers the remaining vector without receiving
the unknown secret or enumerating3^n assignments. All fresh originals count.

These controls close the conditional last digit at genuinely growing original
roots. They do NOT discover the given prefix, solve a higher-root least trit,
or recover an unknown full secret. Planted secrets simulate and verify the
physical controls only. The exact field channel remains a classical positive
countercontrol, not a novel quantum advantage.

## Try To Kill This Direction

- The missing W could simply be the original decoding problem in disguise.
  The reduction narrows the output, not the computational difficulty.
- Arbitrary high reference success may require exponentially hard fiber
  preparation. No sampler-to-coherent-inverse assumption is allowed.
- Fresh-state cost, visibility losses or phase precision could remove an
  apparent polynomial advantage. An exponentially small epsilon is fatal.
- A primitive-only theorem or favorable planted-instance result does not
  establish the weak contract. Zero/nonprimitive secrets remain in scope.
- A classical joint inference attack could implement W just as well. Compare
  it before labeling an outcome quantum progress; scalar no-go gates do not
  exclude joint attacks.
- A least-trit receiver need not help a natural problem unless the original
  native source is efficiently obtainable from that problem. Charge and prove
  the original DHSP/EDCP/lattice reduction separately.

NEXT: specify an actual full-label collective least-trit operation and a
computable estimator using M=poly(nr) fresh originals. Prefer a structural
receiver or provable joint classical learner over another dense optimum
curve. Falsify all free nuisance-fiber inverses and preserve the source law.

## Verification And Ownership

Producer: `python theorems/ternary_least_trit_bootstrap.py --write`.
Focused tests: `python -m pytest -q tests/test_ternary_least_trit_bootstrap.py`.
Independent replay: `node research/certificates/ternary_least_trit_bootstrap_crosscheck.js`.
Report: `research/phase_workbench/ternary_least_trit_bootstrap.json`.

GPT owns these local derivations and targeted falsification. Gemini/Antigravity
owns routine CLI/registry/site wiring and full production validation; preserve
all claim gates. Suggested command: `qsearch.py ternary-least-trit-bootstrap`.
