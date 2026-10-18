# Complex-Axis Readout: Remove Aliases Without Inventing A Decoder

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty, sample-efficient
inference, classical source simulation, new negative or speedup is claimed.
Run `python qsearch.py dcp-complex-axis-readout`.

## 1. First Fix The Real-Circuit Alias

The syndrome/X circuit is REAL. Complex conjugation sends secret s to-s but
does not change any outcome probability. Its full-identification ceiling is
(1+(2/Q)^n)/2 for a uniform residual secret in Z_Q^n, Q=2^(t-2). The prior
Fano count was a necessary condition for an impossible full-secret target,
not a sufficient or useful identification guarantee. The parent workbench now
states the ceiling explicitly and targets NEGATION ORBITS instead. Under the
original uniform prior, orbit entropy>=n*log2(Q)-1; a conservative3/4-success
Fano condition is I>=3n*log2(Q)/4-2, with actual sample costs charged.
This symmetry was already recognized for Bell packets; it applies here too.

## 2. Physical Complex Measurement

After measuring coarse syndrome y, keep all original phase qubits. Optionally
apply known single-qubit phase offsets beta_i(A,y,history), then sample fresh
uniform bits r_i. Apply S-dagger on qubiti if r_i=1, apply H on every qubit,
and measure z. Keep ALL of(A,r,y,z). The source supplies one fresh packet;
enumerating all masks in calibration does not provide2^m experimental copies.

The basic circuit adds at mostm S-dagger andm H gates to the syndrome circuit.
An actual source/syndrome-dependent feedback policy is exported on the T grid:
beta_i=pi*b_i/4, b_i=(sum_l(y_l+1)(A_li mod8)+i) mod8. At most7m T gates
are needed. Compute coefficients only for the REALIZED syndrome in O(nm),
not an exponential table. Full tables exist only in bounded calibration.
No guessed secret, unknown inverse, same-state copy promise or fiber inverse
is used. Hardware transpilation/execution is still absent.

For no feedback, conjugation now gives

    P_-s(r,y,z)=P_s(r,y,z XOR r),

not equality at the SAME observed z. The selected positive controls test
actual sign separation; noninformative/degenerate sources can still have
aliases. Randomization is NOT guaranteed to increase per-attempt mutual
information or to make every fixed public matrix identifiable.

## 3. An Efficient Source-Matched Reference

Let M=2^m, G=4^n, F_y={x:A*x=y mod4}, D_y=|F_y|. The classical reference is

    Q_A(r,y,z)=(1/M)*(D_y/M)*(1/M).

It samples A from its declared native law, draws uniform original x to obtain
y, draws uniform r and uniform z. It does NOT compute D_y or an unknown
secret. Q_A is a comparison distribution, NOT a sampler for actual quantum
records, whose deviations remain nonzero. Empty fibers have zero measure.
Inverse D_y appears only in analytic likelihood inner products and explicitly
enumerated tiny controls, not in the quantum measurement or a free oracle.

## 4. Exact All-Secret Source Kernel

For any two residual secrets a,b, define

    K(a,b)=E_A sum_(r,y,z) P_a(r,y,z) P_b(r,y,z)/Q_A(r,y,z).

For EVERY distinct a,b, K(a,b)=1. This includes zero and order-two secrets;
there is no primitive-secret exception and no remaining negation quotient.
All diagonal values are the same C. Centered densities therefore have
orthogonal source-averaged L2 features, with common squared normd=C-1.
This is source-ensemble identifiability when d>0, not pointwise identifiability,
large TV distance, useful sample complexity or an efficient decoder.

Proof: expand the two Born probabilities in x1,x2,x3,x4. Summing z forces
x1 XOR x2 XOR x3 XOR x4=0, so the two differencesd12,d34 have the same flip
support and values0,+/-1. Averaging the uniform S-dagger mask contributes
zero on any coordinate withd12+d34=+/-2. Only d12=-d34 survives. Known local
feedback cancels EXACTLY in these terms, even when it depends on full A and
the measured y. Remaining higher-label characters contain(a-b)*d12. If a!=b,
every nonzero flip support is killed by a nontrivial character. The zero-flip
terms give sum_y D_y/M=1. No secret parity restriction is made. Because the
random mask forces INTEGER cancellation directly, residual modulus2 is also
included, unlike the earlier fixed-X fourth-moment formula.

For a=b all phase differences cancel without even averaging higher labels.
Thus C(A0), after averaging random axes, depends ONLY on coarse A0 and noise,
not secret, higher labels or feedback. It is the weighted Boolean-
parallelogram count divided byM*D_y in each fiber. The exact coarse census
computes this rationally. The independent full q16 census at n1,m2 gives
common diagonal87/64 at visibility1,1095/1024 at1/2, and1 at0, with EVERY
off-diagonal1. At zero visibility d=0 and all laws are unidentifiable; that
negative control prevents orthogonality being mistaken for information.

## 5. Native Norm And Feedback Bound

At m3n let lambda=M/G. Split fibers into D_y>=lambda/2 and the rest. On the
large fibers, 1/Q_A is at most twice the inverse UNIFORM-syndrome reference.
The previous exact uniform-reference collision mean kappa is now valid for
ALL secrets after random-axis averaging, with no even-secret exception.
Their total contribution is at most2*kappa.

For a small fiber, max_z P(y,z|s)<=D_y^2/M^2 even with phases/noise. Its
normalized collision contribution is at mostD_y^2/M. Since
D_y<lambda/2 implies D_y^2<=(D_y-lambda)^2, averaging all small fibers gives
at most Var(D)/lambda=1-1/G. Here the target-uniform native count has exactly
E[D]=lambda,Var(D)=lambda*(1-1/G), not an IID-fiber assumption.

Hence C<=2*kappa+1 and d<=2*kappa<=6 for n>=2,m3n, using
kappa<=2+2^-n+(27/32)^n<=3. Diagonal exchange terms also give

    d>=v^(2m)*(1-G/M).

At inverse-n noise this is a constant-scale positive bound; for arbitrary
smaller visibility it can be exponentially weak. Both distinctions matter.

Because C(A0) is independent of ANY local feedback phase, fresh random-mask
readout has per-batch source-mean KL at mostlog2(7)<3 bits, uniformly in the
secret and any prior history. Source-, syndrome- and history-dependent local
phase feedback cannot evade this bound IF the final mask remains fresh uniform
after choosing that feedback. T fresh attempts have information<=3T by KL
chain rule against the matched causal reference. This is a constrained readout
class, not a bound on deterministic adaptive bases or collective measurements.

## 6. What Learning Strategies Are Still Missing?

For bounded ONE-RECORD statistical queries, orthogonality and Bessel imply
sum_a |E_Pa phi-E_Q phi|^2<=d<=6. At absolute tolerance tau, one query can
separate at mostfloor(6/tau^2) secrets from the reference. Along an adaptive
reference-answer path, T such queries have uniform identification probability
at most(T*floor(6/tau^2)+1)/Q^n. This reuses the argument already developed
for Bell records; the native source and complex-mask kernel are different.
Query computation is unrestricted. Raw samples, multi-record algebra,
adaptively chosen non-dithered measurements and quantum memory are NOT ruled
out. Do not call all optimization or all classical inference an SQ algorithm.

A direct X/Y Pauli importance estimator is also charged: for weightw, keep
records whose mask matches the desired axes on the support, and return
2^w times the measured parity. It is unbiased for a fixed observable and
has EXACT second moment2^w. Native local blindness forces useful correlators
to high weight, so naive shadow-style feature estimates can be expensive.
The [classical-shadow framework](https://arxiv.org/abs/2002.08953) is relevant
context, not a transfer theorem for this varying-packet source. The estimator
here is derived explicitly; learning one fixed state is not assumed.

## Research Verdict And Falsifiers

Complex masks repair an identifiability defect with cheap actual gates, but
do not supply computational inference or more information per shot. A source-
aware feedback census checks the kernel, and a dephased control checks its
zero-norm failure. The next useful candidate must exploit raw-record algebra,
a more informative collective measurement, or a precisely named escape from
the dither/SQ class. Another expected-loss fit on one-record features is not
an evidence-backed replacement for that missing capability.
