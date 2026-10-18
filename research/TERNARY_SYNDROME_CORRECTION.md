# Nonlinear Syndrome Correction: Two Concrete Attempts Tested

LOCAL DERIVATION / REVIEW PENDING. No novelty, accepted algorithm, independent
theorem review, general quadratic-circuit no-go, or native DCP decoder.

## Problem And Proposed Algorithm

Given explicit IID A in F3^(n by m), find c in {1,2}^m with A*c=0. The known
IID-preserving last-column shear converts this to a nonempty Boolean zero sum.
Allowing zeros in c changes the problem to ordinary nullspace elimination.
The [CLZ framework](https://arxiv.org/abs/2108.11015) and
[Kothari et al., Section3](https://arxiv.org/html/2609.40321v1) motivate replacing
the hard decoder in coherent filtering. They do not supply our tested receiver.

Try public d(b)=R^T*b+Q(H*b), with A*R=I_n, H*A^T=0, r independent rows in H,
and n homogeneous quadratic components in Q. A useful efficient public rule
at a genuinely new density could matter; no such scaling advantage is proved.
We test a fixed low-rank cross term, and random full-syndrome quadratic Q.
Neither survives as a quantum advantage. Structured optimized Q is not excluded.

The actual known preparation is

    1/sqrt(3^n*2^m) sum_(s,e) sigma(e)|A^T*s+e>|s>,
    s in F3^n, e in {1,2}^m, sigma(e)=(-1)^(number of e_j=2).

s is coherently prepared uniformly, NOT an unknown fixed native DCP secret
available as an oracle. Subtract d(b) from s by a complete permutation and
apply the existing local trine readout to b. Keep every residual and failed
output; no projection onto correct decoding is used. Finite source,
subtraction and tensor readout execute, not just a probability formula.

The filter rebuilds `SyndromeQuadratic` from validated PUBLIC matrices and
coefficients, checking A*R=I, H*A^T=0, H independence and exact source binding.
It never invokes an injected decoder callback. Reversible gate export,
finite-gate approximation certification and asymptotic success remain absent.

## Exact Classical Sampler For Low Rank

Put W=rowspan(H), N=3^r, P=I-R*A. Fourier-measuring the residual for ANALYSIS
gives z=-A*e. Q(H*b) only shifts word frequencies inside W, so different
affine W blocks cannot interfere in the final word measurement. This is not
an extra unknown-input measurement or oracle granted to a receiver.

1. Draw uniform sign coins e0, paying m random bits. Set z=-A*e0 and c0=P*e0.
2. Enumerate u in F3^r and e(u)=e0+H^T*u. Retain signed amplitude sigma(e(u))
   if all coordinates are nonzero, otherwise zero. Let B count occupied vertices.
3. On those N coordinates apply unitary convolution

       g_z(v)=(1/N) sum_x omega_3^(v.x-z.Q(x)).

   Amplitude at v is sum_u sigma(e(u))*g_z(v-u)/sqrt(B). Final diagonal
   readout phases do not change probabilities.
4. Sample ALL weights and return c0+H^T*v, including zero-coordinate failures.

Drawing e0 chooses an occupied block with Born mass B/2^m. Another occupied
anchor only changes its coordinates. Tests check the JOINT word/residual-
Fourier law, not merely success. Both DFT sums use exact Z[omega_3] integer
counts. For numerator a+b*omega_3 the squared norm is a^2-a*b+b^2. Weights sum
EXACTLY to N^2*B; no clipping, postselection or approximate renormalization.

Cost is O(poly(n,m,r)*9^r), with polynomial-size integer weights and public
construction/validation charged. Thus r=O(log(n+m)) is classically samplable.
The cap returns UNKNOWN before larger enumeration, not a larger-rank no-go.
Complete 2^m sign censuses are only audit references. This samples the measured
WORD law, not a reusable coherent output channel. General coherent composition
is not covered. Nor does a conditional Clifford description make arbitrary-
rank evolution with nonstabilizer inputs easy; see the scoped discussion of
[Veitch et al.](https://doi.org/10.1088/1367-2630/14/11/113011).

## Positive Finite Signal, Then Falsification

At A=(1,1,1), H rows (1,2,0),(1,0,2), Q=x1*x2 gives actual unheralded witness
success7/12 versus1/2 for systematic linear subtraction. The classical sampler
reproduces ALL the gain. Also c=(1,1,1) is a deterministic classical solution.
All27 quadratic policies are retained, spanning success1/4 through7/12; policy
optimization is not free. The fixed public cross-term rule on ALL27 IID
one-row width3 matrices, including the actual zero-rank fallback, averages
41/81 versus17/27 for linear subtraction. Losing/no-solution labels remain.
These controls establish instrument behavior, not hard instances.

## Random Dense Quadratics: Asymptotic Falsifier

Increasing rank defeats that block simulator, but does it yield an algorithm?
Fix public A,R,H BEFORE choosing every Q coefficient independently uniformly.
At z!=0 the scalar coefficients of z.Q are IID uniform. Averaging a phase
pair x,y pinches exactly when x_i*x_j=y_i*y_j for every i<=j, equivalently
y=x or y=-x. A nonzero coordinate of x fixes a common sign via the cross terms;
zero x forces zero y. No generic random-phase/rank heuristic is assumed.

For normalized block amplitudes a_u=sigma(e(u))/sqrt(B), with zeros included,
the exact coefficient-averaged probability at v is

    1/N + (1/N) sum_u a_u*conj(a_(2v-u)) - |sum_u a_u|^2/N^2.

The reflection term is real and <=1 by Cauchy-Schwarz. Thus every point has
mean mass <=2/N. Integer weights have numerator
`N*B+N*sum_u sigma_u*sigma_(2v-u)-(sum_u sigma_u)^2`, denominator N^2*B.
The exceptional z=0 branch is UNCHANGED by Q; its total mass V_A/2^m is
retained separately. V_A counts all-nonzero words in ker(A).

For FULL H spanning ker(A), N=3^(m-n). Each block contains at most V_A valid
words, so

    E_Q[success | A] <= V_A/2^m + 2*V_A/3^(m-n).

For IID A, every fixed sign word has A*c=0 with probability3^-n. Hence
E_A V_A=2^m/3^n exactly. The union over (3^n-1)/2 projective left-kernel
vectors bounds rank failure by (3^n-1)/(2*3^m). Full-rank probability >1/2
for m>=n. Even arbitrary success on rank-deficient inputs gives

    E_A,Q success <= 3^-n + 2*(2/3)^m + (3^n-1)/(2*3^m).

For S random candidate draws and up to R repetitions of a selected candidate,
pay T=S*R by max<=sum and the success union bound. Multiply the first two
terms by T; rank failure is paid once for the FIXED A. Receiver calls alone
do not pay for best-of-many program selection. Conditioned on full rank, use
the conservative cap min(1,2*T*(3^-n+2*(2/3)^m)). Coherent composition or
amplification is NOT covered, nor are deliberately optimized/structured Q.

At n64,m128,T4096, unconditional success is <=2^-61, including arbitrary
rank-failure fallback. This is an exact source-average local derivation, not
a large quantum execution or a bound on every individual matrix/program.
Polynomially many random trials do not turn this candidate into a polynomial-
success solver. Merely increasing syndrome rank is not progress.

## Verification, Costs And Decision

Tests cover actual joint states, all small source labels, every output word,
anchor independence, exact categorical draws including failures, vector/dense
inverses, program covariance, forged callbacks, source/cap rejection, all27
coefficient twirls, and exact IID sign-count/rank moments. An n32/width96
CLASSICAL sampler runs with quantum/exhaustive references forbidden.

The existing independent Node replay's --syndrome-correction mode rebuilds
preparation, quadratic subtraction and tensor readout on four saved controls,
compares every word to the exact classical distribution, and rejects forged
output/program/speedup records. This is not independent mathematical review.

REJECT low-rank correction as a quantum advantage and random dense homogeneous
quadratics as a useful one-pass algorithm. There is no uniform structured
extensive-rank rule here. Do not automatically launch another coefficient
scan or random scaling plot. Compare independent constructive mechanisms
again before extending this track. Strong classical baselines must include
Gaussian free-sign assignment, generalized-birthday methods, algebraic/
syndrome decoding and the published finite-field subset-sum tradeoffs.

    PYTHONPATH=theorems python -m pytest -q tests/test_ternary_syndrome_correction_physics.py
    python theorems/ternary_syndrome_correction.py --write
    node research/certificates/ternary_decoder_filter_crosscheck.js --syndrome-correction
