# DCP Walsh Feedforward: A Constructive Alternative And Its Classical Test

Status: LOCAL DERIVATION / REVIEW PENDING, 2026-09-23. No independent review,
formal verification, novelty claim, efficient new decoder, or speedup. This
is a theory note and implementation contract, not a completed subsystem.

## 1. Research Decision

The preceding purification construction needs normalized coherent subset-sum
fiber aggregation. That is a sufficient architecture, not a necessary one.
Here is a different actual circuit architecture: retain every Hadamard outcome,
correct an outcome-dependent sign on the sum register, and Fourier-measure it.
An ideal sign correction has constant natural-label decoding probability at
m=n+O(log n), without amplitude normalization or rare-outcome postselection.

The attempted escape has an important qualification. If its sign correction
is uniformly computable CLASSICALLY, useful decoding success implies an
efficient CLASSICAL average subset-sum witness algorithm, through chosen-query
Goldreich-Levin learning. This remains true for arbitrary nonlinear dependence
on the measured outcome. It is not just a low-degree or linear-correction test.

Consequently:

- Do not reject this architecture merely because the direct normalized-fiber
  block has exponentially small singular scale. It does not implement that
  block by generic amplification.
- Do not call an exact signed-count table a cheap phase oracle. Its computation
  is the unresolved arithmetic, and ordinary dynamic programming is exponential
  in n. Training, advice, precision, and per-label preprocessing are charged.
- A fast classical sign corrector would itself be important, but it must face
  the classical witness extractor below. It is not evidence that arithmetic
  has been bypassed by a Fourier transform.
- Next main-model work should construct an actual arithmetic algorithm, or a
  quantum operation outside the classically evaluable diagonal-feedforward
  interface. Do not spend the next pass fitting uncharged sign tables.

## 2. Exact Circuit And Physical Outcome Law

Let N=2^n, M=2^m, lambda=M/N, and f_a(b)=sum_i a_i*b_i mod N. For public a,
the clean input is

    |psi_d> = M^(-1/2) sum_b omega^(d*f_a(b)) |b>.

Compute f_a(b) reversibly into an n-qubit register. Apply H to all m input
qubits and measure them, obtaining e. Define the INTEGER response

    A_t(e) = sum_(b:f_a(b)=t) (-1)^(e dot b).

The unnormalized remaining branch is

    |v_(d,e)> = (1/M) sum_t A_t(e)*omega^(d*t) |t>.       (1)

Its probability is sum_t A_t(e)^2/M^2, not uniform in e. Retain every branch.
Apply a diagonal correction sigma_a(e,t) in {-1,+1}, then inverse QFT and
measure j. All correction scratch must be uncomputed. Correct-output
probability is, for EVERY secret d,

    P_sigma(a) = 1/(M^2*N) sum_e [sum_t sigma_a(e,t)*A_t(e)]^2.  (2)

No physical postselection or hidden success denominator appears in (2).
An ordinary polynomial-time Boolean evaluator for sigma supplies its phase
gate by reversible compute/phase/uncompute, with the evaluator cost charged.
The existence of the function does not supply that evaluator.

### The Uncorrected Circuit Is Exactly A Local Readout

With sigma=1, the COMPLETE joint distribution is

    Pr[e,j | a,d] = (1/N) product_i
        (1 + (-1)^e_i*cos(2*pi*a_i*(d-j)/N))/2.          (3)

Thus it can be implemented by choosing uniform j, applying the public phase
offset -j to each source qubit, and locally X-measuring those qubits. This is
an equivalence to local QUANTUM measurements, not a classical source-state
simulator. Classical processing of (a,e,j) still has the random-design
decoding problem. If the circuit simply reports j, success is exactly 1/N.

Derivation: the joint amplitude factors as

    1/(M*sqrt(N)) product_i [1+(-1)^e_i*omega^(a_i*(d-j))].

Outcome-dependent nontrivial correction is exactly what prevents commuting
the final Fourier measurement to the beginning. Equation (3) does not cover
that correction, nor another collective measurement.

## 3. Sign Rectification Has Constant Natural-Source Success

For an ideal evaluator set sigma_a(e,t)=sign(A_t(e)), assigning either sign
at zeros. Triangle inequality shows this is optimal among diagonal phase
corrections for the declared circuit, including arbitrary complex unit phases.
It need not be an optimal measurement on the original DCP states.

    P_rect(a) = 1/(M^2*N) sum_e [sum_t |A_t(e)|]^2.       (4)

We now average over independent uniform a_i, uniform e, and uniform t. Walsh
orthogonality gives E[A^2]=lambda. The exact fourth moment is

    E[A^4] = lambda*B,
    B = 1 + 3*(M-1)/N
          + 3*(3^m-2*M+1)/N^2
          + 2*(4^m-3*3^m+3*M-1)/N^3.                  (5)

This is a signed-response fourth moment, not the fourth factorial moment of
the unsigned fiber count. The Boolean quadruple classification is the same
one already used in `theorems/dcp_subset_sum_fourth_moment_obstruction.py`.

Proof of (5): after averaging e, surviving ordered quadruples have XOR zero.
Write them b, b xor u, b xor v, b xor u xor v. There are respectively

    1,
    3*(2^m-1),
    3*(3^m-2*2^m+1),
    4^m-3*3^m+3*2^m-1

direction pairs with zero, one, two, or three nonempty coordinate categories
among (u_i,v_i)=(1,0),(0,1),(1,1). Summing the signed labels in these disjoint
categories gives independent uniform X,Y,Z when the categories are nonempty.
The equal-frequency conditions are X+Z=Y+Z=X+Y=0. Their probabilities are
1, 1/N, 1/N^2, and 2/N^3 respectively. The factor two in the last case is
the two solutions of 2Z=0 over Z_(2^n), including N=2. Average the forced
target t at cost 1/N and sum the M choices of b. This proves (5).

Interpolation between the first, second, and fourth moments yields

    E|A| >= (E A^2)^(3/2)/(E A^4)^(1/2).

Using Jensen on (4) therefore gives

    E_a P_rect(a) >= lambda/B.                          (6)

If m=n+O(log n) and lambda tends to infinity, B/lambda tends to 3, so (6)
tends to 1/3. At m=n it tends to 1/4. These are lower bounds, not asserted
limiting success probabilities. They concern the natural source, not a chosen
easy family. A numerical control with m much larger than n need not be in
this asymptotic regime.

Analytic examples for m=n+ceil(log2(n^2)):

| n | m | lambda | Lower Bound In (6) |
| --- | --- | --- | --- |
| 16 | 24 | 256 | .2643958235 |
| 32 | 42 | 1024 | .3313063111 |
| 64 | 76 | 4096 | .3333057725 |
| 128 | 142 | 16384 | .3333265518 |
| 256 | 272 | 65536 | .3333316379 |

These are formula evaluations, NOT executions of large phase corrections.
For a noisy source with a clean component of weight p0, the same measurement's
correct-output probability is at least p0 times its clean success, simply by
positivity. This supplies no constant-noise decoding or purification theorem.

### Approximation Must Be Measured In The Right Distribution

Let L_e=sum_t |A_t(e)| and, when L_e>0,

    C_e = sum_t sigma(e,t)*A_t(e)/L_e.

Equation (2) is exactly the sum of the ideal branch contributions in (4)
weighted by C_e^2. A branch-global sign has no effect. Ordinary unweighted
classification accuracy on (e,t), or accuracy only on e=0, is not the metric.

Alternatively, define the physical squared-amplitude sign-error mass

    epsilon = (1/M^2) sum_(e,t with wrong sign) A_t(e)^2.

The purified corrected states differ in norm by 2*sqrt(epsilon). Projection
onto the correct Fourier outcome gives the robust lower bound

    P_sigma >= max(0, sqrt(P_rect)-2*sqrt(epsilon))^2.    (7)

The same argument works with label averages by retaining the label as a
classical flag in a purification. Sign errors at A=0 cost zero. This is a
sufficient error bound; the branch correlation identity is sharper.

## 4. The Classical Goldreich-Levin Reduction

This is the main adversarial test of the apparent positive construction.
Assume sigma_a(e,t) has a uniform deterministic CLASSICAL evaluator of charged
cost C_sigma on arbitrary chosen e,t. Public random coins may be fixed for an
attempt and included in the source law. No oracle for the unknown secret is
assumed or created.

Fix a. Choose a reference assignment b uniformly, set s=f_a(b), and let t be
the INDEPENDENT uniform subset-sum challenge in Z_N. Define

    g_(s,t)(e) = sigma_a(e,s)*sigma_a(e,t),
    ghat_(s,t)(v) = E_e g_(s,t)(e)*(-1)^(e dot v),
    H(b,t) = sum_(c:f_a(c)=t) ghat_(s,t)(b xor c).

Expanding (2) gives the exact identity

    E_(b,t) H(b,t) = P_sigma(a).                        (8)

Let D_t be the target fiber size. Parseval implies |H(b,t)|<=sqrt(D_t) and
E_t D_t=lambda. These hold for every public tuple; no occupancy or natural-
label concentration assumption is needed.

Suppose the label-averaged decoder success is at least p_*>0, and put

    tau = p_*/(2*lambda).

Separate the terms in H with Fourier coefficient magnitude below tau. Their
sum is at most tau*D_t. Averaging, the contribution of the remaining terms
is at least p_*/2. If E is the event that at least one valid c has a remaining
coefficient, their sum is bounded above by sqrt(D_t)*1_E. Cauchy-Schwarz gives

    Pr_(a,b,t)[E] >= p_*^2/(4*lambda).                  (9)

Apply Goldreich-Levin to the CLASSICALLY chosen-query function g_(s,t), with
threshold tau and failure probability at most 1/2 on every fixed input. It
returns a list containing every Fourier index v with |ghat(v)|>=tau. For each
returned v, test the Boolean assignment c=b xor v by computing f_a(c).
Accept only a verified witness for the supplied t. The resulting classical
procedure has average success at least

    p_*^2/(8*lambda),                                  (10)

in time polynomial in m, n, lambda/p_*, and C_sigma. The target was not planted:
only the auxiliary reference s was generated from b. Illegal challenges fail.
Known p_* is an inverse-polynomial lower-bound promise, not a success estimate
that can be obtained for free. A declared threshold schedule could be charged
instead; that is not needed for this statement.

When lambda=poly(n), inverse-polynomial quantum decoding through this circuit
therefore supplies a classical average witness solver. This is NOT a classical
simulation of arbitrary DCP measurements, a DCP hardness proof, or a claim that
such a classical subset-sum algorithm is impossible. At exponentially large
lambda, the reduction does not establish polynomial runtime or useful success.
It also does not supply classical membership access to a correction computed
only by a genuinely quantum procedure or one using uncharged quantum advice.

### A Self-Contained Polynomial Membership-Query Procedure

For a Boolean sign function g on m bits and a length-k Fourier-index prefix u,
the sum of squared Fourier coefficients extending u is

    W(u) = E_(x,x',y) g(x,y)*g(x',y)*(-1)^(u dot (x xor x')),

where x,x' are independent k-bit strings and y is a SHARED (m-k)-bit string.
This identity follows by summing the suffix characters. Estimate W(u) to
additive tau^2/4 and retain prefixes whose estimate is >=3*tau^2/4. Every
coefficient of magnitude >=tau survives; every retained prefix has mass
>=tau^2/2. There are at most 2/tau^2 such prefixes at a level.

Cap the retained list at ceil(2/tau^2), aborting an attempt if exceeded. At
most Q=2*m*ceil(2/tau^2) prefix estimates are then requested. Fresh independent
samples per estimate and

    L = ceil(32*tau^(-4)*ln(2*Q/delta))

samples suffice by Hoeffding and a conditional union bound. Each sample uses
two g evaluations, hence four sigma evaluations. The intentionally conservative
total is 4*Q*L sigma calls, polynomial but potentially large. This is a proof
of an implementable baseline, not a recommendation to run that loose budget
on every registry refresh. More efficient standard GL implementations exist.
Finite Walsh enumeration is NOT an execution of this chosen-query algorithm.

The established learning ingredient is Goldreich-Levin, not a new algorithm
here. Its heavy-coefficient membership formulation is stated in Feldman,
section 2.4, Theorem 4: https://eccc.weizmann.ac.il/report/2008/091/download .
The original work is Goldreich and Levin, STOC 1989,
https://doi.org/10.1145/73007.73010 . This pass read the Feldman statement;
retrieval of the original ACM page failed. Novelty of this DCP application
has NOT been established by the limited literature search.

## 5. Cheap Correction Classes And A Faster Exact Classical Control

Two exact bounds eliminate misleading small correction dictionaries:

1. For a public dictionary of K phase functions of t, fixed before e but
   allowed to depend arbitrarily on a, choosing the best member after seeing
   e has P<=K/N. For each fixed member, Walsh Parseval gives total squared
   overlap M^2; a pointwise maximum is at most the sum over the K members.
2. Let h_a(t) be a fixed partition into R cells, independent of e. Even if
   sigma chooses an arbitrary sign per cell after seeing e, P<=R/N. Sum A
   within each cell, apply Cauchy-Schwarz over the R cells, then Parseval over
   e; every assignment belongs to exactly one cell. This includes low-bit
   and other polynomial-size hash tables. A choice among K such partitions
   has the looser bound KR/N. An arbitrary e-dependent partition is NOT
   covered; treating the ideal sign function as a two-cell fixed partition
   would be an invalid proof.

For corrections linear in e, sigma(e,t)=(-1)^(e dot w_a(t)), there is a much
cheaper exact baseline than GL. The proposed w need not be a valid witness.
Set r(b)=b xor w_a(f_a(b)), and let L_u=|{b:r(b)=u}|. Parseval gives

    P_sigma(a) = sum_u L_u^2/(M*N).                    (11)

Classically choose uniform b, compute u=r(b), and on independent challenge t
return c=u xor w_a(t) only if f_a(c)=t. For each u there are exactly L_u
successful targets, so its average witness success is EXACTLY (11). This
uses two w evaluations and elementary arithmetic, no Fourier table.

A valid chosen witness on each of J distinct target residues puts at least
J assignments into r=0 and gives P>=J^2/(M*N). At near-linear sample count
this can be useful; reciprocal matching is not required by this architecture.
Producing those witnesses efficiently remains the task, not a free primitive.

## 6. Executed Mathematical Checks

Only bounded research-critical probes ran, not production workflows or the
test suite. Tables used here are explicitly exponential reference objects.

- Complete natural-label ensembles at (n,m)=(1,1),(1,3),(2,2),(2,3),(2,4),
  (3,3), totaling 858 label tuples, matched (5) using exact integers/Fractions.
  Fourth moments were 5/2, 88, 29/8, 139/8, 94, 539/128. Exact mean rectified
  successes were 3/4, 15/16, 41/64, 193/256, 833/1024, 2349/4096, each above (6).
- Five physical instances at N=4,4,8,8,16, with labels (0,0,0), (1,1,2),
  (1,2,4), (1,3,5,6), (1,2,3,5,7), used four corrections each: exact sign,
  none, seeded arbitrary signs, and a branch-global sign change of exact sign.
  All secrets were run through the full sum/Hadamard/correction/QFT state.
  Maximum normalization or success residual was 7.78e-16. Equation (3) matched
  the entire uncorrected joint law, not just its success probability.
- Those twenty cases also matched (8) exactly and satisfied (9), using full
  integer Walsh coefficient enumeration. This checked the ideal heavy-event
  lemma, NOT the runtime or success of a randomized GL implementation.
- A deliberately easy scope control, a=(1,2,4), N=8, with half the branch
  signs flipped, has zero global signed correlation but decoder success one.
  The pair-product g cancels this gauge and preserves the witness extraction.
  Thus a proof assuming positive global correlation for every good corrector
  would be false. This calibration is not a research input family/candidate.
- Twenty-one fixed-partition, finite-dictionary and linear-correction checks
  passed on three instances. The linear-correction probabilities 3/8, 17/64,
  47/256 matched independent exhaustive classical witness trials exactly.
- Another 208 exact prefix-mass checks on sixteen sign functions in dimensions
  one through four verified the correlated-query identity used by the GL
  procedure. They did not execute its randomized estimation schedule.
- Sixty seeded sign-perturbation controls verified (7); on the same five
  physical instances, four small-response thresholds each satisfied the
  weighted bound used in section 8. These are inequality checks, not physical
  executions of coherent amplitude estimation.
- An initial physical-check command had a bracket typo and did not execute;
  the corrected command produced the twenty successful checks reported above.

## 7. Gemini Handoff And Remaining Falsifiers

Extend an existing DCP readout/arithmetic diagnostic, not a new breakthrough
candidate or unbounded autonomous experiment:

1. Encode (1)-(6) with exact integer/Fraction moment controls; reuse the existing
   affine-quadruple classifier where useful. Distinguish signed fourth moments
   from unsigned factorial moments and analytic scaling from executed circuits.
2. Verify all-secret full-state circuits, the local-measurement equivalence,
   completeness, branch weights, zeros, repeated labels and the global-sign
   countercontrol. Include direct Born-error checks for (7).
3. Report the EXACT sigma access contract: classical chosen-query evaluator,
   quantum-only evaluator, enumerated table, or unsupported. Charge preprocessing
   and inverses. Only the first supports the classical consequence (10).
4. Implement a bounded GL membership adapter with query counts and independent
   sample batches if an actual efficient corrector is supplied. Keep full Walsh
   enumeration as an explicitly exponential reference, not that adapter.
5. Validate proposed witnesses against the original independent challenge.
   Implement the faster exact baseline (11) for e-linear corrections. Report
   useful source-average success, not the rate conditioned on legal targets.
6. Preserve both outcomes of this audit: ideal phase correction is physically
   useful, but a cheap classical implementation is already a classical average
   subset-sum breakthrough. The reduction does NOT eliminate all diagonal
   quantum operations, all densities, or the original DCP problem.

No actual fast corrector was found. A dense sign table, a small-instance neural
fit, or a phase circuit synthesized from that table does not fill the gap.
The next useful theory pass must either produce and analyze a compact evaluator,
or explain how a different quantum operation supplies useful coherence without
this evaluator or a free normalized-fiber inverse. Another moment bound alone
would not address the implementation bottleneck.

For prior measurement/subset-sum context, see Bacon, Childs and van Dam,
https://arxiv.org/abs/quant-ph/0501044 . The general association is established
prior work; this note claims neither to originate it nor to settle its complexity.

## 8. A Charged Quantum Implementation, Still Exponential

Added 2026-09-24. LOCAL DERIVATION / REVIEW PENDING. A quantum-only evaluator
escapes the CLASSICAL membership premise in section 4. That is not by itself
an efficient implementation. The following explicit baseline shows both what
can be implemented and where its exponential work remains.

For fixed e and a quantum-controlled target t, count

    D_+(e,t) = |{b:f_a(b)=t, e dot b=0}|,
    D_-(e,t) = |{b:f_a(b)=t, e dot b=1}|.

Their difference is A_t(e) and sum is D_t. Prepare fresh UNIFORM assignment
registers and use the two reversible predicates in standard amplitude
estimation. No reflection about the unknown source state is used. The BHMT
counting bound, Theorem 13, is

    |Dhat-D| <= 2*pi*sqrt(M*D)/T + pi^2*M/T^2

with constant probability above 1/2. Its sharper version has D*(M-D) under
the square root. Repeat coherently and compute a median so both count
estimates satisfy their bounds with probability at least 1-delta, for EACH
fixed e,t. Retain the work registers, apply the sign of their difference as
a phase, and reverse the entire estimation/median computation. Measuring or
discarding those registers midway is not a valid coherent correction.

Choose a power-of-two query scale C*sqrt(M)<=T<2*C*sqrt(M), C>=1. With each
reversible numerical count evaluation accurate to 1/C^2, the total difference
error, on the successful estimate event, is at most r_C*sqrt(D_t) for D_t>=1,
where

    r_C = 2*sqrt(2)*pi/C + (2*pi^2+2)/C^2.

This follows from sqrt(D_+)+sqrt(D_-)<=sqrt(2*D_t); the final 2/C^2 pays the
two numerical errors. D_t=0 has no physical branch weight. No promise that
all fibers have similar size is used.

The small-response set |A_t(e)|<=r_C*sqrt(D_t) has total PHYSICAL mass at most
r_C^2, for every a:

    (1/M^2) sum_small A_t(e)^2
        <= (r_C^2/M^2) sum_(e,t) D_t = r_C^2.

Outside it, only an estimation failure can give a wrong sign. After coherent
compute/phase/uncompute the state-norm error against ideal rectification is
therefore at most 2*sqrt(r_C^2+delta), plus charged gate-synthesis error xi.
The resulting natural-label success is at least

    max(0, sqrt(lambda/B)-2*sqrt(r_C^2+delta)-xi)^2.      (12)

For example C=128, delta=10^-4 and negligible xi give a limiting lower bound
about .1887 when lambda/B tends to 1/3. This is an analytic baseline, not an
executed amplitude-estimation circuit or a novel complexity improvement.

The two counts, coherent repetitions, numerical evaluation and uncomputation
use O(C*2^(m/2)*log(1/delta)) reversible predicate queries and polynomial
workspace. The predicates and each known-state reflection cost polynomial
gates in m,n. Numerical precision and gate synthesis remain charged; uniform
per-gate errors can be set to O(xi/query_count), requiring O(m+log(1/xi))
precision bits for fixed C,delta. There is no QRAM table or extra supply of
unknown DCP states hidden in this baseline. It is exponential for m near n
and is not competitive with the established subexponential DCP sieves.

This derivation supplies an UPPER bound for this generic counting route,
not a lower bound on structured sign computation. An improved arithmetic
procedure, a different quantum-only correction, or a different measurement
is not ruled out. Do not report the absence of a classical evaluator as an
advantage until the quantum evaluator has a better charged construction.

Primary counting source, Theorems 12-13, inspected in this pass:
https://arxiv.org/pdf/quant-ph/0005055 . The counting primitive is established
prior work; the weighted error application above is the local derivation.
