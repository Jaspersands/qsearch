# Inverse-Trace Completion: A Sampling-Preserving Restriction

2026-10-23. Local mathematical deduction, REVIEW PENDING. This extends the
independent review's [search restriction](independent_review_2026_10_22/CLASSICAL_RESTRICTION.md)
to approximate uniform sampling. It supplies neither the missing residual
sampler nor a new quantum algorithm. The independent review is closed;
this follow-on has not been independently reviewed.

## Decision

The residual problem is sufficient to attack BOTH remaining tasks, but
under different contracts. A verified residual witness solves search.
Sampling the residual nearly uniformly for typical uniform syndromes
would also approximately sample the full native fiber. The latter does
not require exact completion counts, a Markov-chain mixing assertion, or
rejection of the sampled prefix with an uncharged acceptance probability.

The useful next implementation is a capped residual solver/sampler on the
original public points. Keep its search and distributional results separate.
More field-size sweeps of already dequantized subfield instances would not
resolve this obligation. Prime extension degree remains unresolved, not hard.

## 1. Original Input And Proposed Composition

Keep q=2^n, N=n^2, K=floor(N/8), arbitrary distinct supplied alpha_i, the
K-by-N Vandermonde matrix H, and bits b_i. Define

    A_i = {x in F_q : Tr(inv0(x))=b_i},    |A_i|=q/2.

All zeros, field arithmetic and target bits have their original meaning.
Allow an arbitrary fixed syndrome s; the native problem has s=0. Fix a
residual coordinate set U of size m=K+ceil(4K/n), before sampling. Let T
be its complement and ell=|T|. The algorithm is:

1. Independently sample x_T uniformly from the corresponding A_i. Sampling
   a trace-hyperplane value and applying inv0 is an exact paid method.
2. Compute h=s-H_T*x_T.
3. With fresh independent randomness, sample the accepted residual fiber
   H_U*x_U=h. An empty fiber produces ABORT. The sampler has a fixed
   polynomial clock, including on exceptional syndromes.
4. Independently verify the original Hx=s and every original predicate.
   Invalid output becomes ABORT; it is never counted as a solution.

Step 3 is MISSING. Gaussian elimination exposes ceil(4K/n) free field
variables, not that many Boolean variables. Neither an exact conditional
sampler nor its source probability is granted as an oracle.

## 2. Exact Distribution Identity

Let Q=q^K, a_U=(q/2)^m, a_T=(q/2)^ell, and let Z_U(h), Z_T(t) be the
accepted assignment counts of the two blocks at those syndromes. Put

    g(h)=Q*Z_U(h)/a_U,
    f(h)=Q*Z_T(s-h)/a_T,
    c=E_uniform_h[f(h)*g(h)].

Both f and g have uniform mean one. The full accepted fiber has size
a_U*a_T*c/Q. Assume c>0. Its prefix distribution has density

    target_prefix(x_T) / product_prefix(x_T) = g(h)/c.       (1)

If Step 3 samples its fiber exactly, the conditional output law given a
nonempty prefix is the same under the proposed algorithm and the target.
Therefore the TOTAL variation distance, including the ABORT output, is

    TV = (1/2) E_uniform_h [ f(h)*|1-g(h)/c| ].              (2)

This is not a claim that the prefix itself is exactly uniform under the
target. Empty residual fibers have g=0 and contribute to (2). Merging all
their prefix labels into ABORT preserves the total variation identity,
since the target assigns zero mass to every such prefix and to ABORT.
No success conditioning or restart is implicit.

## 3. Transfer Bound Without A Small-Normalizer Division

Write v_U=E(g-1)^2 and v_T=E(f-1)^2. Then

    |c-1| <= sqrt(v_U*v_T).                                (3)

In particular sqrt(v_U*v_T)<1 certifies c>0. By Cauchy--Schwarz,

    E[f*|g-1|] <= sqrt(v_U) + sqrt(v_U*v_T).

Compare the probability prefix law P with the UNNORMALIZED law gP,
then compare gP with its normalization gP/c. The second L1 distance is
exactly |c-1|, not |c-1|/c. Equations (2)--(3) give

    TV <= min(1, sqrt(v_U)/2 + sqrt(v_U*v_T)).               (4)

Thus a near-flat residual count distribution suffices even though it is
not evaluated by the algorithm. Dividing every error bound by 1-c_error
is unnecessary here. This argument does not assume independent f and g;
they can be adversarially correlated through the public input.

The review's exact MDS Fourier second moment gives, uniformly in the points
and bits, v_U<=V_m and v_T<=V_ell, where

    V_j=9^j*q^(K-j).

Consequently the original restriction has full sampling error at most

    sqrt(V_m)/2 + sqrt(V_m*V_ell),                          (5)

whenever V_m*V_ell<1. At the specified native parameters, (5) is
2^-Omega(n^2). This is an asymptotic implication with a missing sampler,
not an executed native-size sampling result.

## 4. Paying For An Approximate Or Exceptional Residual Sampler

For each h, define an ideal kernel: uniform on the accepted residual
fiber if nonempty, and ABORT if empty. Let e(h) in [0,1] be the TOTAL
variation error of the capped, verified actual residual sampler relative
to that kernel, including failures. Require that this kernel depends on
the public residual instance and h, with fresh coins, not hidden details
of the randomly selected prefix. Suppose

    E_uniform_h e(h) <= epsilon.

The prefix-generated syndrome has density f, and its distance from
uniform is at most sqrt(v_T)/2. Therefore

    E_prefix e(h) <= epsilon + sqrt(v_T)/2.

The complete algorithm, with aborts retained, satisfies

    TV(actual, uniform full fiber)
      <= min(1, sqrt(V_m)/2 + sqrt(V_m*V_ell)
                  + epsilon + sqrt(V_ell)/2).              (6)

For example, error at most eta outside a uniform-syndrome exceptional
set of measure delta implies epsilon<=eta+delta. Runtime must still be
capped on that set. An average over a convenient planted-syndrome source
is NOT the stated hypothesis. If the sampler is chosen adaptively from
x_T, a single fixed-kernel uniform-syndrome bound is insufficient.

## 5. Attempts To Falsify The Composition

- A deterministic residual witness is not a residual uniform sampler.
  Even f=g=1 can have arbitrarily bad completion bias: two completions
  per syndrome and a fixed choice give full TV=1/2, while (4) is zero
  for the exact uniform-completion kernel. The missing error is e(h).
- Omitting empty fibers silently changes the algorithm. For uniform
  f=(1,1) and g=(2,0), the unconditioned algorithm aborts with probability
  1/2 and has TV=1/2. Conditioning away the abort instead has TV=0, but
  incurs a retry cost and is a different law.
- Uniform-syndrome error does not transfer for free. A prefix concentrated
  on the one bad syndrome can turn an average error 1/Q into error one.
  The sqrt(v_T)/2 term pays for this mismatch; native MDS mixing makes
  it small, not an informal claim that the syndrome looks random.
- Solving only a planted, zero, or favorable syndrome does not meet (6).
  No claim of hardness follows if an attempted residual solver times out.
- The small finite checks below verify the probability identities, not
  polynomial runtime, native asymptotic sampler existence, or a separation.

## 6. Literature And Other Routes Checked This Pass

[Cheng, 2610.06445v1](https://arxiv.org/html/2610.06445v1) counts subspaces
with SUM_(x!=0 in E) 1/x=0. That is not the pointwise requirement
Tr(1/x)=0 for every x in E, nor a polynomial-time construction of a useful
native correction space. It does not close Step 3.

The existing prime-character norm solver addresses a different odd-field
predicate and degree budget. Its population/fixed-input guarantees cannot
be imported into inverse trace. Affine inverse-coordinate parametrizations
and low-degree multipliers were already audited in the independent review;
no new solver follows merely by rewriting their coupled equations.

The Rees receiver remains a separate proposed theorem needing independent
whole-proof validation and a useful source. Its Lean dependency artifacts
were still offloaded when checked; no hydration or cache repair was attempted.

## 7. Exact Controls And Mechanical Follow-Up

`tests/test_inverse_trace_completion_transfer.py` uses exact rational
arithmetic. It checks the identity and bound over finite histograms,
empty-fiber/biased-completion countercontrols, approximate-kernel error
transfer, and genuine F16 inverse-trace/Vandermonde histograms obtained by
bounded syndrome convolution. The latter is EXPONENTIAL in nK, used only
as an independent control, never a proposed scalable sampler.

Gemini follow-up, only when assigned: implement a capped residual attack
on original prime-degree inputs, record public U, prefix randomness, h,
all failures, native witness verification and runtime. Use search status
unless the output-distribution contract in Section 4 is established.
On bounded calibration instances compare against exact residual fibers;
do not treat distinct-looking answers as evidence of uniformity. Keep
the fixed polynomial clock and the uniform-syndrome vs induced-syndrome
distinction. No registry admission is licensed by this reduction alone.

Verification:38 new controls and65 selected tests PASS in1.32s; new-file
py_compile PASS. The expanded output-law test initially included a disjoint
support pair with no full target; it now explicitly checks c=0/ABORT rather
than attempting normalization. The earlier exhaustive bound test already
handled this case. This is not a whole-repository or quantum-execution run.

The native F16 control has v_U=53/2048. For all-zero, all-one and alternating
targets at syndrome zero it obtains nonzero prefix-transfer TV (about
0.057,0.064,0.059 respectively), confirming that the composition is not
silently EXACT uniform sampling. At n17/31/61, the main term sqrt(V_m)/2
has base-two logarithm -6.177/-33.445/-160.359; cross terms are much smaller.
Those large-n values are theorem-bound evaluations, not sampler executions.
