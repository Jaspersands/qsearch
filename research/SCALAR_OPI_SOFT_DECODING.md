# Scalar OPI: Soft Interpolation And Additive-FFT Cancellation

31 October 2026. Reviewed scoped deductions and a completed classical falsifier.
Same explicit F_(2^t), m=q-1, degree<k, IID half-table source as
SCALAR_OPI_NATIVE_PRIORITY.md. No quantum implementation, classical hardness
or new speedup claim. Corpus been-tried/baselines preceded the source audit.

## 1. Dense-List Multiplicities Cannot Supply The Root Certificate

The standard soft-interpolation mechanism chooses a polynomial Q(X,Y)
with multiplicity M_(i,y) at each supplied point (a_i,y). Its numerical
constraint cost is sum binom(M_(i,y)+1,2), not the bit length of these
multiplicities. If P has degree<k, the substitution Q(X,P(X)) has degree
at most the (1,k-1)-weighted degree D of Q. Thus the strict score condition

    sum_i M_(i,P(a_i)) > D

forces Q(X,P(X))=0 and permits polynomial-root extraction. This is the
published GS/KV mechanism, not a new decoder. The primary original KV PDF
timed out; the formal interface was checked in
[El-Khamy--McEliece cs/0509097, SectionIII](https://arxiv.org/html/cs/0509097).
Their iterative/reliability schemes are competitors, not automatically
covered by the following restriction.

Give every y in F_i the SAME INTEGER multiplicity s_i>=0, with no weight outside
F_i. The s_i may be chosen adaptively from the entire public input. Write
L=|F_i| and j=deg_Y Q. For v_i the exact (X-a_i)-adic valuation of Q,
the nonzero specialization of Q/(X-a_i)^v_i at X=a_i has all L distinct
roots with multiplicity at least s_i-v_i if that is positive. Its Y-degree
is at most j. Therefore

    v_i >= max(0,s_i-floor(j/L)).

The product of these powers divides Q. Weighted degree is additive under
nonzero multiplication over the field, and the residual Y-degree is j, so

    D >= sum_i max(0,s_i-floor(j/L))+(k-1)j
      >= sum_i s_i - m floor(j/L)+(k-1)j
      >= sum_i s_i                  if L(k-1)>=m.

But every P has multiplicity score at most sum_i s_i. Thus the strict
certificate is impossible. For L=q/2 and m=q-1, this holds for every k>=3.
It covers dependent interpolation equations and coordinate reweighting,
not just a generic monomial-count estimate. Unequal weights WITHIN each
accepted list, or polynomial factors occurring without this certificate,
are not ruled out. The valuation argument is a local deduction; no novelty
or general lower bound is claimed. Multiplicity means Hasse/ideal
multiplicity, including in characteristic two. Two independent automated
reviews accepted this deduction. The bound is sharp: the X-only polynomial
prod_i(X-a_i)^s_i attains D=sum_i s_i.

## 2. A Specific Additive-FFT SC Schedule Equals A Prange-Type Baseline

Use the published degree-ordered subspace-polynomial basis
[Lin--Chung--Han1404.3458, SectionII](https://arxiv.org/pdf/1404.3458).
Let V_r=span_F2(1,z,...,z^(r-1)), W_r(X)=prod_(v in V_r)(X-v), and
S_r(X)=W_r(X)/W_r(z^r). Basis element X_j is the product of S_r for
the nonzero binary digits of j, so deg X_j=j. Degree<k is exactly the
condition that coefficients of numerical indices >=k vanish.

At a node of size 2n, offset beta and n=2^r, split coefficients into c,v.
The two child polynomials have coefficient pairs

    a_j=c_j+s*v_j, b_j=c_j+(s+1)*v_j, s=S_r(beta).

Their child evaluation transforms generally DIFFER. A valid synthesized
channel recursion nevertheless exists if all unprocessed coefficients,
INCLUDING future frozen ones, are averaged uniformly: child futures are
independent because the above pair transform is invertible. Decode (c_j,v_j)
in the common recursively interleaved child order (bit reversal). Child
likelihood vectors L,R give low likelihood sum_v L(c+s*v)R(c+(s+1)*v).
Then impose the required frozen high coefficient when its turn arrives.
Use positive weights, for example 2^(indicator), to avoid zero channels.

At beta=0, s=0, so the low likelihood is exactly

    L(c) sum_v R(c+v) = L(c) sum_b R(b).

If k<=n, every high v_j is frozen zero. By induction the chosen c vector
depends only on the left tables and independent coins. Right prefixes
contribute only a candidate-independent factor, never decision feedback.
The left child has offset zero and the same degree restriction. If k=2^s,
recursion stops at V_s, whose coefficients are all free.

Keep the original m=q-1 problem by adding a NEUTRAL weight at point0, not a
new random constraint. Only k-1 actual tables then influence the output P.
Conditioned on them and the coins, the remaining m-k+1 hits are independent
Bernoulli(1/2). Thus

    E[number satisfied] <= (m+k-1)/2.

This is at best the Prange limit at fixed dyadic rate. Polynomially many
precommitted/independently seeded such candidates followed by full-score
selection cannot close a fixed DQI gap (Hoeffding and union bound).
Adaptive feedback from ignored tables is excluded from that statement.
Independent review accepted the recursion and the no-feedback induction.

This rejects THIS unrestricted-future SC schedule, not every FFT, BP,
freeze-aware recursion, variable order, or classical scalar-OPI algorithm.
Published RS polarization kernels [Mori--Tanaka1001.2662](https://arxiv.org/pdf/1001.2662)
do not let one replace the prescribed degree prefix by a good polar code.

## 3. The Concrete Repair Tested And Stopped

At a low decision whose paired high coefficient is known zero, replace
the unrestricted sum over that coefficient by the actual v=0 contribution
L(c)R(c). Propagate individual child degree cutoffs where justified. This
uses full-table information that the rejected schedule discards. It is a
CLASSICAL HEURISTIC: future frozen pairs create cross-child correlations,
so these scalar messages are not asserted to be exact constrained marginals.

Indeed at k=n the exact relation between left and right evaluation vectors
is dense Cauchy mixing: T_xy=W_r(beta)/(W_r'(0)*(beta+x-y)). Every entry
is nonzero. An independent Sage F4 control with V={0,1}, beta=z and both
right accepted sets {0,1} permits exactly (x,x^2); each unary marginal is
full, and multiplying those marginals falsely permits all16 pairs.

The repair is worth one bounded experiment because it directly removes
the proved data-discarding step while retaining the native code and paid
input. A fixed table alphabet q makes q-symbol message updates polynomial
in the explicit O(q^2)-bit input. Freeze coefficients by numerical DEGREE,
not their SC position, and verify every final word by native-field Horner
evaluation of an actual degree-<k polynomial. Compare to real Prange
restarts on the identical tables and the retained rational DQI mean bound.
No belief-propagation correctness, quantum execution or asymptotic success
may be inferred from a finite score. Stop rather than expand a failed test.

The bounded experiment is complete. `classical_baselines/scalar_opi_fft_probe.py`
uses FLINT field arithmetic, integer max-sum messages, native polynomial
conversion and Horner verification, and 32 actual Prange restarts on each
identical instance. Its JSON retains all input tables, field moduli, seeds,
witnesses and charged message work. DQI entries are rational lower bounds
on the published ideal mean, not measured quantum outputs.

| q,k | seed | ordinary SC | freeze-aware | best Prange32 | DQI mean lower bound |
|---|---|---|---|---|---|
| 16,4 | 3101 | 12 | 12 | 13 | 9.436 |
| 16,4 | 3102 | 4 | 11 | 13 | 9.436 |
| 64,16 | 3101 | 39 | 42 | 45 | 47.326 |
| 64,16 | 3102 | 47 | 46 | 45 | 47.326 |
| 256,64 | 3101 | 148 | 165 | 171 | 203.636 |
| 256,64 | 3102 | 158 | 155 | 172 | 203.636 |

Independent Sage verification checked all 18 returned native witnesses.
Exact F4 controls gave interpolation kernel dimensions 0 at weighted degree3
and 1 at degree4 for row weights (1,2,1); unequal symbol weights escape via
Q=Y-X, score3>degree2. The dense-Cauchy guard has 4 allowed joint pairs but
16 pairs in the product of unary supports. Results are in
`classical_baselines/scalar_opi_soft_decoder_controls.json`. Script controls
also check full-code decoding, the best-constant aware decoder, and ten
ordinary-SC ignored-suffix invariances. Independent review found no
invalidating implementation error.

Decision: stop this repair after the precommitted six cases. It did not
reach the comparator on the larger tested cases. This is neither an
asymptotic failure theorem nor classical hardness, and the Prange comparison
is not matched wall-clock complexity. No broader decoder campaign follows
without a new operation that addresses the retained joint correlations.

A separate quantum list-decoding extension was checked before implementation
and demoted as existing machinery. [Jo2607.16541, Sections4-7](https://arxiv.org/html/2607.16541)
already gives complete syndrome-fiber lists, canonical globally padded
index erasure and a uniform-index projection with success Z_I/(L Z_0).
Its algorithmic theorem pays normalization under a specified exponent
condition and Johnson-radius margin. Theorem5.2's coherent sum is exactly
the proposed mechanism; a small list alone does not pay success. This audit
does not transfer the paper's prime-field score theorem to the current
binary-field experiment or claim that the old DQI comparator is optimal.
