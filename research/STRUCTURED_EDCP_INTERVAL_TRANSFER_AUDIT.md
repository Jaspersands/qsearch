# Structured EDCP: Long-Interval Transfer Is Not Free

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

This is a scoped state-conversion obstruction, not a hardness theorem for
structured EDCP, LWE, or all quantum measurements. It closes a specific
tempting shortcut: treating exponentially many coefficient labels as the
long interval required by a known efficient hidden-shift algorithm. No
novelty, independent proof review, efficient decoder, or speedup is claimed.

## 1. Research Decision And Literature Contract

Do not implement a purported Childs--van Dam solver by replacing its interval
length with the cardinality of the structured coefficient support.
[Childs and van Dam](https://arxiv.org/pdf/quant-ph/0507190), sections 3--4,
solve generalized hidden shift for interval length M >= N^epsilon with fixed
positive epsilon. Their measurement uses fixed-dimensional convex integer
programming to prepare bounded-size solution fibers. This is a geometric
requirement, not just an entropy threshold.

For L structured blocks, a scalar fiber variable lives in a nonconvex digit
set. Expanding those variables gives L*d coefficient variables. Constant L
does not make that integer-programming dimension constant. A bijection that
packs the support into an interval generally changes the secret-dependent
phases and is not a valid algorithm transfer.

The local results below are stronger than a failed relabeling: even an
arbitrarily expensive secret-independent SINGLE-BLOCK operation cannot make
a long uniform interval state with both constant fidelity and nonnegligible
success in the specified growing regime, averaged over the full phase orbit.
The bound permits all heralded unit label multipliers and arbitrary ancillary
systems independent of the secret.

The phase-conversion framework is established prior art. In particular,
[Marvian and Spekkens](https://arxiv.org/pdf/1104.0018), Theorem 26 and
Corollary 27, characterize stochastic covariant pure-state transformations
through positive-definite characteristic functions. We derive the finite
cyclic specialization and the approximate-output bound directly below.
For additive geometry we use Freiman's dimension lemma in its standard form,
as stated in equation (1.3) of
[Jing and Mudgal](https://arxiv.org/pdf/2307.03066).

Next targets remain genuinely JOINT Gaussian-fiber processing and efficient
prior-aware decoding of local readouts. This result does not make either easy.
See `STRUCTURED_EDCP_GAUSSIAN_FIBERS.md`,
`STRUCTURED_EDCP_INFORMATION_THRESHOLD.md`, and
`STRUCTURED_EDCP_PRIOR_CVP_BASELINE.md` in this directory.

## 2. Input And Output Contracts

Let q >= 3, d >= 2, Q=q^d+1, and

    E(c) = sum_(i=0)^(d-1) q^i*c_i mod Q,
    D_R = E({-R,...,R}^d),   B=2R+1,
    R >= 1,                 4R <= q-1.                 (1)

Unlike the information-threshold divisor lemma, the geometric statements
here do not require power-of-two d or R <= d. Their stronger digit-width
condition (1) MUST be checked independently.

Compress the input's character sectors abstractly:

    |psi_z> = sum_(u in Z_Q) sqrt(p_u) omega_Q^(z*u) |u>.

For the coefficient-register source, p is the pushforward of its coefficient
probability law under E. Several coefficient strings in one sector are
combined into their normalized known fiber vector, not summed as probability
amplitudes across unrelated sectors. Compression need not be efficient for
this upper bound: allowing it only gives a converter more power.

The successful output, with a heralded unit beta in Z_Q, is compared against

    |I_z^(beta)> = M^(-1/2) sum_(b=0)^(M-1)
                       omega_Q^(z*beta*b) |b>,  1 <= M <= Q.       (2)

All operations are independent of the unknown z. They may depend on public
source parameters. The success p_suc and squared fidelity F are averaged
over uniform z, with F conditioned on success and weighted by branch success.
In particular,

    p_suc*F = (1/Q) sum_(z,beta)
       <I_z^(beta)| E_beta(|psi_z><psi_z|) |I_z^(beta)>.

This is not an arbitrary-secret-prior claim. To apply it to z=<a,s>, establish
the required phase-orbit distribution or an all-z guarantee; a nonprimitive
public label can instead give a smaller orbit. Unknown-center sources do not
silently inherit this known-amplitude contract.

## 3. Exact Additive Geometry

Evaluation is injective on [-2R,2R]^d under (1). Indeed, a difference has
coordinates at most 4R in absolute value and integer evaluation magnitude
at most 4R*(q^d-1)/(q-1) <= q^d-1 < Q. Equality modulo Q is therefore
integer equality. Reducing successively modulo q forces every difference
digit to vanish, because each lies in [-(q-1),q-1]. Consequently

    |D_R| = B^d,                  |D_R+D_R| = (4R+1)^d.          (3)

If three successive points of a modular arithmetic progression lie in D_R,
their coefficient lifts satisfy c_0-2c_1+c_2=0 by the same argument. Thus a
progression wholly inside D_R lifts to a straight coefficient progression.
A nonzero step changes an integer coordinate by at least one per step:

    longest nonconstant progression inside D_R has B terms.       (4)

The bound is attained by varying one digit. In particular every B+1
consecutive positions of a unit-step progression contain a missing point.
The condition is essential: q=3,d=2,R=1 violates (1), and its nine-point
support contains a unit-step progression of length nine, not three.

Equation (4) alone is insufficient to obstruct constant-error conversion
when B grows. The stronger intersection bound is the important next step.

Let P={gamma+beta*b: 0<=b<M} with beta a unit, and let C be the coefficient
lifts of P intersect D_R. Write N=|C| and r=dim_aff(C). For N>0:

* Projection onto some r coordinate axes is injective on aff(C), so N<=B^r.
* Freiman's dimension lemma gives |C+C| >= (r+1)N-r(r+1)/2.
* Injectivity on the doubled box and P's interval parametrization give
  |C+C|=|E(C)+E(C)| <= 2M-1, including when interval sums wrap modulo Q.

Hence an exact integer upper bound on ALL such intersections is

    U_dim = max_(0<=r<=d) min(B^r,
                    floor((2M-1+r(r+1)/2)/(r+1))),
    U = min(B^d, M-floor(M/(B+1)), U_dim),
    |P intersect D_R| <= U,          alpha=U/M.                  (5)

Empty intersections satisfy this trivially. The formula uses the ordinary
affine dimension of coefficient lifts, not the dimension of residues as
points on a scalar number line. It costs O(d) big-integer arithmetic
operations, not Q-sized enumeration. Floors and powers can be exact.

A useful asymptotic relaxation follows by separating N<sqrt(M). Otherwise
r>=log_B(M)/2 and N<=(2M-1)/(r+1)+r/2, whence

    alpha <= max(M^(-1/2), 2/(1+log_B(M)/2)+d/(2M)).             (6)

Thus for q and R polynomial in d and M=Q^epsilon with fixed epsilon>0,
the maximum interval occupancy tends to zero, not to one. Formula (5),
rather than floating-point logarithms, should generate finite certificates.

## 4. Exact Pure-Output Conversion: A Packing LP

Twirling any successful converter over the known phase action preserves
its average success and target fidelity under uniform z. For outcome beta,
apply the inverse output phase after a random input phase. The resulting
instrument is covariant. This is a mathematical reduction for a bound, not
an assumption that the original physical converter respects a symmetry.

Its Kraus operators can be refined into character modes gamma. In a mode,
input frequency u=gamma+beta*b maps to output b. An exactly pure successful
branch of mass r_(beta,gamma) must have coefficients proportional to

    K_(beta,gamma)|gamma+beta*b>
        = sqrt(r_(beta,gamma)/(M*p_(gamma+beta*b))) |b>.

The condition for such branches to be jointly trace-nonincreasing is

    sum_(beta,gamma,b: u=gamma+beta*b) r_(beta,gamma)/M <= p_u
        for every u,             r_(beta,gamma)>=0.             (7)

Conversely these inequalities construct the Kraus operators, with failure
completing the channel; zero-mass entries prohibit any positive branch that
uses them. Maximize sum r to obtain the optimal exact success probability.
This is a bounded-reference LP, NOT an efficient large-Q algorithm.
It includes all offsets and all heralded unit beta, so choosing a clever
different label multiplier does not evade the bound.

For input supported in D_R and M>B, every branch encounters a zero, hence
the exact success is zero. For full support, put

    eta = sum_(u not in D_R) p_u.

Every target branch spends at least 1-alpha of its mass outside D_R.
Summing (7) there gives the all-branches bound

    p_suc <= min(1, eta/(1-alpha)),  when alpha<1.               (8)

There is NO multiplication by the number of branches. The crude alternative
using (4) is eta/[floor(M/(B+1))/M]; (5) is much stronger asymptotically.

## 5. Approximate Outputs: A Robust Bound

Exact-state obstructions alone would not exclude an approximate algorithm.
For each refined covariant Kraus mode j=(beta,gamma,auxiliary index), write
x_j=K_j|psi_0>. Let P_j project onto output b whose input frequency
gamma+beta*b is OUTSIDE D_R. From (5),

    ||(I-P_j)|I_0^(beta)>|| <= sqrt(alpha).

Let a_j=<I_0^(beta)|x_j>. By the triangle and Cauchy--Schwarz inequalities,

    |a_j| <= sqrt(alpha)*||x_j|| + ||P_j*x_j||.

The character-mode relation gives P_j*K_j=K_j*P_out, with P_out the input
projector outside D_R. Trace-nonincreasingness therefore implies

    sum_j ||P_j*x_j||^2 <= ||P_out*psi_0||^2 = eta.

Taking the Euclidean norm across modes proves

    sqrt(p_suc*F) <= sqrt(alpha*p_suc)+sqrt(eta).

In particular,

    p_suc <= min(1, eta/(sqrt(F)-sqrt(alpha))^2),  if F>alpha.    (9)

This includes mixed successful outputs, discarded internal records, and
success-weighted heralded multipliers. For a successful target trace-distance
error at most epsilon, F>=1-epsilon; substitute this LOWER bound for F only
when it exceeds alpha. The distance convention is (1/2)||rho-sigma||_1.
If eta=0, any positive-success converter has F<=alpha, regardless of cost.

This corrects the initially weak exact-only argument. Since alpha tends to
zero, a fixed positive target fidelity is enough for a meaningful bound.
If F<=alpha, report the bound as VACUOUS, not a division error or rejection.

## 6. Full Gaussian Source And Growing Parameters

Take independent coefficient probabilities proportional to
exp(-2*pi*c_i^2/sigma^2), with sigma the AMPLITUDE width used in the native
fiber note. Evaluation outside D_R implies at least one coefficient outside
[-R,R], even with modular aliases. A Gaussian integral bound and normalization
at least one give

    eta <= min(1, d*sigma^2/(2*pi*R)
                       * exp(-2*pi*R^2/sigma^2)).               (10)

This is a charge on the actual untruncated source, not an added support
promise. Set q=d^(a+o(1)), sigma=d^(b+o(1)), with fixed a>b>0, and
R=ceil(sigma*ln(d)). Then (1) holds eventually, eta is superpolynomially
small, and for fixed 0<epsilon<=1 and M of order Q^epsilon, alpha=O(1/d).
Equation (9) makes the success of constant-positive-fidelity SINGLE-BLOCK
interval conversion superpolynomially small. This holds for an average
all-phase-orbit guarantee, not automatically the reduction's secret prior.

Analytic bound evaluations, NOT simulations or cryptographic parameters:
q=d^2, sigma=sqrt(d), R=ceil(sigma*ln(d)), M=q^(d/4), target F>=0.9.

| d | R | alpha upper bound | log10 tail upper bound | log10 success upper bound |
|---|---|---|---|---|
| 64 | 34 | 0.0625000000 | -48.0053946200 | -47.6939553432 |
| 256 | 89 | 0.0144927536 | -82.3625360286 | -82.1989086720 |
| 1024 | 222 | 0.0034305317 | -128.4558161771 | -128.3547060324 |

Keep logs to avoid silently rounding a positive Gaussian tail to zero.

## 7. Bounded Verification And Countercontrols

These were direct mathematical reference computations, not production tests.
No module, CLI, candidate, registry, or full-suite status was changed.

Exact support checks used (q,d,R)=(5,2,1),(7,2,1),(9,2,2),(5,4,1).
Their support sizes are 9,9,25,81, sumset sizes 25,25,81,625, and maximum
nonconstant supported progression lengths 3,3,5,3. Unit-step intervals
were exhausted at lengths {1,B,B+1,2B,floor(Q/2),Q}, totaling 1,199,424
intervals. Every occupancy satisfied (5). All 511 nonempty subsets of
[-1,1]^2 passed exact rational affine-rank, projection-cardinality, and
Freiman sumset checks. These validate implementation identities, not replace
the cited lemma or a proof review.

Ten SciPy/HiGHS packing LPs checked primal feasibility, dual feasibility and
matching objectives. All positive Kraus branches were reconstructed and
checked against EVERY z for their modulus (1,496 branch/phase checks).
Representative exact-output optimum successes:

| q,d,R | M | probability outside D_R | optimum success |
|---|---|---|---|
| 5,2,1 | 3 | 0 | 1 |
| 5,2,1 | 4 | 0 | 0 |
| 7,2,1 | 4 | 0 | 0 |
| 9,2,2 | 5 | 0 | 1 |
| 9,2,2 | 6 | 0 | 0 |
| 3,2,1 | 4 | 0 | 8/9 (premise deliberately false) |
| 5,2,1 | 4 | 0.01 | 0.030588235294 |
| 5,2,1 | 8 | 0.01 | 0.024470588235 |
| 5,2,1 | 13 | 0.01 | 0.015294117647 |
| 5,2,1 | 26 | 0.01 | 0.015294117647 |

The LP inputs were uniform on D_R at zero tail, or a mixture of uniform on
D_R and uniform on its complement at the displayed tail. They are algebraic
transformation controls, NOT new oracle-problem candidates. Numeric LP output
was checked at tolerance 1e-8 and phase identities at 1e-10. Fraction labels
in the table also have direct elementary constructions.

192 approximate covariant instruments passed (9), all in its nonvacuous
regime: Q=26, R=1, M in {4,8,13,26}, branch counts in {1,8,32}, tail masses
in {0.001,0.1}, eight trials each, NumPy seed 20260925. Output directions
were near the uniform interval vector, with complex Gaussian perturbations
of size 0.05 or 0.001. Every mode used a random unit beta and random gamma;
one common rescaling enforced total squared Kraus load <=1 per input label.
Checks included the actual outside-output mass, simultaneous contraction,
aggregate fidelity and the inequality BEFORE division by its denominator.

Another 24 dense NONCOVARIANT instrument controls verified that twirling
preserves average success and success-weighted target fidelity. They used
Q=26, M in {4,8,13}, tails in {0,0.01}, four trials each and three heralded
multipliers {1,3,5}, NumPy seed 20260925. Dense complex Gaussian Kraus
matrices were jointly rescaled by the largest eigenvalue of their total
K-dagger-K load. Masking entries by u-beta*b=gamma implemented the exact
character-mode decomposition; all original-versus-twirled averages and
outside-mass bounds agreed within 1e-12. This checks that the no-go is not
silently restricted to a hand-selected symmetric family of filters.

The failed-premise control q=3,d=2,R=1 has a unit-step progression of length
nine. Nonunit steps can cycle inside that support; do not report repeated
visits as the length of a distinct-point interval.

## 8. Red Team: What This Does Not Rule Out

1. JOINT blocks: their frequency distribution is a convolution of differently
   multiplied digit laws. It need not retain this support geometry. Apply a
   new bound to that distribution or implement a genuine joint operation.
2. A prior-adapted decoder: uniform twirling changes a narrow prior. The
   balanced Gaussian secret prior in the source reduction is a real escape,
   not permission to claim an all-secret converter works.
3. A different output task: recovering a function of z, supplying short phase
   states, or directly decoding local data need not create (2).
4. A genuinely different source: wide digits, secret-dependent reference
   states, extra independent samples, or a smaller character orbit change
   the contract. Charge those resources and rederive the claim.
5. Gaussian widths comparable to q: condition (1) may not permit a low-tail
   truncation. No conclusion follows just from substituting a bad R.
6. Very small target fidelity: (9) is vacuous below alpha. An independently
   justified decoder tolerating that output would need a fresh analysis.

The most important attempted falsification was approximate conversion:
the elementary progression-length argument did NOT settle it. The
dimension/occupancy argument and Kraus-norm bound supply the stronger scoped
result. A counterexample to (5) under (1), or to (9) for a legal covariant
instrument, would invalidate this note. A fast multi-block algorithm would
not contradict it and remains desirable.

## 9. Gemini Implementation Handoff

Create `theorems/structured_edcp_interval_transfer.py` only as a mathematical
checker, not as a new algorithm-search pipeline. Keep integration secondary
to testing a real joint decoder.

* Implement exact premise checking and O(d) integer cap (5); return a
  not-applicable result when digit width, unit multiplier, phase orbit, or
  target length conditions are missing. Do not factor Q to evaluate (5).
* Implement log-domain Gaussian tail and exact/approximate success bounds.
  Distinguish squared fidelity, trace distance, conditional success, and
  vacuous inequalities. Retain the amplitude-width convention.
* Add bounded support/LP references with explicit Q caps, all offsets and
  units, primal/dual checks and reconstructed Kraus operators. Never label
  Q-sized enumeration as scalable source preparation or conversion.
* Preserve the supported short-interval positive controls, failed-width
  control, low-fidelity/vacuous case, multi-branch contraction checks and
  full-Gaussian nonzero-tail accounting. Add independent checks of the
  coefficient lift and dimension cap before trusting a report.
* Record a negative result ONLY for single-block long-interval transfer
  under its full-phase-orbit contract. Do not mark structured EDCP or its
  source candidate globally dequantized, solved, or refuted.

Main-model follow-up: examine compact joint measurement representations,
including group-covariant quantum message passing, and identify an actual
poly(log Q) operation rather than hiding an exponential eigenvalue table,
coherent fiber sampler, or generic CVP oracle behind an abstraction.

## 10. Follow-Up Audit: What Quantum Message Passing Actually Supplies

[Mandal and Pfister](https://arxiv.org/pdf/2604.12186), Lemma 17 and
Theorem 22, give equality-node compression and closure of group-covariant
messages on trees. Their explicit equality operation uses a controlled
Householder reflection built from a normalized conditional eigenvector.
Closure does not itself provide a poly(log |G|) implementation of that
reflection. This is an applicability audit, not a criticism of a claim the
paper does not make.

There is also a genuine efficiency result to distinguish from abstract
closure: [Piveteau and Renes](https://arxiv.org/pdf/2509.19441), Proposition
4.1 and Theorem 1.2, give BPQM complexity exponential in the maximum variable
dimension and an optimal binary-code trellis decoder with runtime O(n*k*S^4)
for trellis state-space size S. Their section 5.2 explicitly requires small
internal alphabet sizes for efficient tree descriptions. A tree with edges
indexed by Z_Q is not sufficient when Q grows exponentially. Nor do native
integer carries automatically form the binary linear code that theorem uses.

Here is the exact local specialization for two canonical phase messages:

    |psi_z^(1)> = sum_u sqrt(p_1(u))*omega^(z*u)|u>,
    |psi_z^(2)> = sum_v sqrt(p_2(v))*omega^(z*v)|v>,
    r(w) = sum_u p_1(u)*p_2(w-u).

For a public unit multiplier a, absorb it into p_2(v)=p(a^(-1)*v), NOT into
a newly chosen independent coefficient distribution. The equality-node
Gram eigenvalues are lambda(w)=Q*r(w). Modular addition turns the product
state into

    sum_w sqrt(r(w))*omega^(z*w)|w>|zeta_w>,
    |zeta_w> = sum_u sqrt(p_1(u)*p_2(w-u)/r(w)) |u>.             (11)

The missing operation is controlled erasure of zeta_w. Its inverse is
controlled coherent preparation of the same conditional weighted fiber.
This is exactly the joint-fiber target already identified in this project,
not an independent efficient decoder delivered by a new name.

Even without assuming a controlled construction, an exact unitary taking
the product family to the canonical family with the stated phase convention
for EVERY z must map each normalized total-frequency fiber to |w>|0>.
Multiply that vector identity by omega^(-z*w) and sum over z; character
orthogonality isolates the fiber, whose positive sqrt(r(w)) cancels. Its
inverse prepares that fiber. Empty fibers impose no constraint. This exact
claim concerns the specified coherent vector identity, not unconstrained
z-dependent global phases or a prior-specific approximate discrimination task.

### A Less Wasteful Approximation Contract

Do not demand exponentially precise treatment of every rare fiber unless
the proposed algorithm actually needs it. Suppose a frequency-preserving
controlled unitary uses an approximate erasure U_w, and put

    e_w = ||U_w|zeta_w> - |0>||,
    Delta^2 = sum_w r(w)*e_w^2.                               (12)

Orthogonal w registers make the full output vector error EXACTLY Delta for
every z, not merely on average. This also holds for any prior on z. Thus
the absolute loss in the probability of any subsequent measurement event
is at most min(1,Delta). For a tree of such operations, a hybrid argument
bounds total error by the sum of node errors, evaluated on their ideal input
messages. A rare bad region of mass delta contributes at most 4*delta to
Delta^2, since unit vectors differ in norm by at most two.

Without frequency preservation, Parseval still gives the average identity

    (1/Q) sum_z ||V|input_z> - |ideal_z>|0>||^2
      = sum_w r(w)*||V|fiber_w> - |w>|0>||^2.                (13)

That average does NOT automatically transfer to a narrow prior. The basis
vectors and ideal output phases must be fixed consistently before using
(12) or (13); independently optimizing a global phase per fiber is invalid
unless the phase correction is coherently computable and applied.

These are implementation specifications with an explicit error budget, not
a supplied oracle for r or zeta. Identifying a low-mass bad region, estimating
its mass, computing good conditional amplitudes, and implementing the
controlled erasure remain charged tasks. A flat or easily evaluated r alone
does not determine the conditional fibers. For example, uniform p_1 makes
r uniform for both point-mass and uniform p_2, while their fibers differ.

Bounded references tested 12 native two-block merges at
(q,d,R)=(3,2,1),(5,2,1),(7,2,1), amplitude width 2.3, using the first four
unit multipliers at each modulus. All 344 phase/compression identities and
344 controlled weighted-error identities passed at tolerance 1e-12.
Twelve additional non-frequency-preserving unitary perturbations passed
(13), using NumPy seed 20260925. These used explicit small matrices and
are NOT scalable implementations or quantum circuit compilations.

REVISED NEXT TASK: find a compact approximation to (11) for naturally random
public multipliers and an information-sufficient number of blocks. Measure
the WEIGHTED coherent error (12), success, bit complexity and source coverage;
compare the same instances with prior-aware classical local-readout decoding.
A small classical eigenvalue table, an abstract Householder formula, a
low-dimensional-looking graph with Q-sized alphabets, or a source with
specially selected multipliers is not a solution. Do not spend a main-model
pass wiring generic BPQM before this operation has a credible implementation.
