# Product-Output Obstruction And Correlated-Block Escape

Date: 2026-09-23

Status: LOCAL DERIVATION / REVIEW PENDING. Not an independently reviewed
theorem, novelty claim, DCP lower bound, or quantum speedup. This theory pass
does not integrate code, run bulk workflows, or promote proof gates.

## Research Decision

The recursive edge construction discards most of a batch to produce one
clean phase qubit. Can an arbitrary collective operation instead retain many
independent clean phase qubits while cancelling the same low label bits?

For a natural, pre-grouped batch of m=2r random phase labels, the derivation
below obstructs nine such output qubits with high joint fidelity and useful
success probability when n>=6r and r grows faster than log(n). The operation
can be arbitrarily complicated: this is not a restriction to permutations,
linear circuits, basis sampling, or the current edge algorithm.

However, a polynomial-size low-bit measurement retains a CORRELATED phase
block with at least r bits of Holevo quantity on a collision-free source.
Independent inverse-n dephasing changes this by only O(r log(n)/n). Holevo
quantity is NOT a lower bound on accessible information, an efficient
measurement, or a decoding algorithm. This positive control prevents the
product-output obstruction from being promoted to a general no-go claim.

Priority: investigate operations on implicit correlated phase blocks, or
explicitly charged adaptive pooling. Do not build a fresh-batch many-product-
output interface on the assumption that physical implementability is free.
One through eight outputs are not excluded by the stated asymptotic bound.

## 1. Model And Charged Success

Let N=2^n, M=2^m and omega=exp(2*pi*i/N). Labels a_i are independent uniform
elements of Z_N. The batch is fixed before inspecting its labels. Its state is

    |psi_d> = M^(-1/2) sum_b omega^(d*f(b)) |b>,
    f(b) = sum_i a_i*b_i mod N,       b in {0,1}^m.

The unknown secret d is uniform in Z_N. All operations are independent of d
except through these m input states. Arbitrary known ancillas, classical
computation, measurements, coherent workspaces, feedforward and postselection
are allowed. Additional unknown-secret states or oracle calls are NOT free.

An accepted outcome names B labels delta_j, each nonzero modulo N and divisible
by 2^r, where 1<=r<n. Its target, on D=2^B basis states, is

    |Phi_(d,delta)> = D^(-1/2) sum_z omega^(d*t(z)) |z>,
    t(z) = sum_j delta_j*z_j mod N.

Labels delta may depend on a and the classical outcome, even when that
outcome's probability depends on d. No independence or uniformity assumption
on the output labels is imposed. Unobserved workspace is traced, not erased.

Let s be total accepted probability averaged over natural labels and uniform
d, and h the correspondingly averaged UNNORMALIZED fidelity numerator.
The accepted joint fidelity is h/s. Averaging conditionally normalized
fidelities uniformly over d is a different, inappropriate success metric.

## 2. Frequency-Support Fidelity Lemma

Fix a, delta and one Kraus operator K from the input batch to the output.
Further Kraus indices can account for discarded workspaces. Let F={f(b)}.
For each gamma in Z_N define

    u_(z,gamma) = M^(-1/2) sum_(b: f(b)=gamma+t(z)) K_(z,b).

The sum within a source-frequency fiber is coherent. Replacing it by a sum
of squared entries is wrong when f has collisions.

Finite Fourier orthogonality gives EXACT identities

    s_K = E_d ||K psi_d||^2 = sum_(z,gamma) |u_(z,gamma)|^2,
    h_K = E_d |<Phi_(d,delta)|K|psi_d>|^2
        = D^(-1) sum_gamma |sum_z u_(z,gamma)|^2.

Define L_gamma = #{z: gamma+t(z) is in F}, counting output BITSTRINGS,
including multiplicities when different z have the same target frequency.
Cauchy-Schwarz, separately for each gamma, proves

    h_K <= (max_gamma L_gamma / D) * s_K.                 (1)

This proof allows dense complex K with arbitrary interference and
secret-dependent success probability. Summing (1) over outcomes is valid
when the support bound holds for every eligible output-label tuple.

If no translate of the complete target cube lies in F, then

    h_K <= (1 - 1/D) * s_K.                              (2)

For fixed F and target labels, max_gamma L_gamma/D is also the optimal
conditional fidelity if arbitrarily small positive acceptance is allowed:
choose one maximizing gamma, map one input basis element for each supported
frequency to all matching output rows with equal amplitudes, and scale the
operator to a contraction. The output's supported rows have the correct
relative phases. Repeated rows sharing an input require this scaling.
This existence argument says nothing about implementation cost or useful
acceptance probability.

In particular, exact positive-probability conversion requires AND, without
efficiency restrictions, is possible whenever a full translated cube exists.

## 3. Generic Full-Modulus Labels Force Disjoint Supports

Call a label tuple exceptional if a nonzero v in {-2,-1,0,1,2}^m obeys

    sum_i a_i*v_i = 0 mod N.

There are 5^m-3^m vectors with an odd entry, each vanishing with probability
1/N, and 3^m-1 nonzero all-even vectors, each with probability 2/N. Thus

    Pr(exceptional) <= (5^m + 3^m - 2) / 2^n.             (3)

This bound can be vacuous. In particular, do not apply it in the dense
m approximately n or m approximately 2n regimes.

Suppose a is nonexceptional and a complete translated output cube exists.
For every z choose b_z satisfying f(b_z)=gamma+t(z). Every two-dimensional
face satisfies

    a dot (b_00 + b_11 - b_01 - b_10) = 0 mod N.

The coefficient vector has entries between -2 and 2, so it must be zero
AS AN INTEGER VECTOR. Hence every coordinate function z -> (b_z)_i has all
mixed second differences zero. It is an integer-affine Boolean function.
Such a function is only a constant, z_j, or 1-z_j: two nonzero affine
coefficients would give a range wider than {0,1}.

Consequently every nonzero delta_j is a signed sum of input labels on a
nonempty support S_j, and these B supports are PAIRWISE DISJOINT. This is a
deduction from output frequencies, not an assumption that K acts on bases.
For B=1 the coordinate classification holds without any two-dimensional
faces. Zero output labels are excluded because fresh |+> states are free.

## 4. Natural-Source Bound

For fixed disjoint nonempty signed supports, the B sums modulo 2^r are
independent uniform residues. All vanish with probability 2^(-r*B).
Each input coordinate is unused, or assigned with either sign to one of B
groups. There are at most (2B+1)^m assignments. Empty groups are omitted
BEFORE applying the probability 2^(-r*B); counting them would be invalid.
The larger cardinality is used only as an upper bound on nonempty assignments.

Combining this union bound with (3), with probability at least 1-epsilon
over natural input labels there is NO eligible translated B-cube, where

    epsilon = min(1, (5^m+3^m-2)/2^n + (2B+1)^m/2^(r*B)). (4)

On ordinary label tuples (2) applies to the entire accepted instrument.
On exceptional tuples use only h_a<=s_a<=1. Therefore

    h <= (1-2^(-B))*s + 2^(-B)*epsilon.

If h/s >= 1-eta and eta < 2^(-B), then

    s <= epsilon / (1 - 2^B*eta).                         (5)

For m=2r, B=9 and n>=6r, epsilon=2^(-Omega(r)); the second term has
exponent -[9-2*log2(19)]*r, approximately -0.50416026*r. With joint
infidelity eta<=1/1024, acceptance is at most 2*epsilon. Inverse-polynomial
infidelity eventually satisfies this constant threshold.

For r=omega(log n), inverse-polynomial success is therefore impossible in
this FRESH-BATCH PRODUCT-TARGET model. More than nine eligible outputs are
also covered by retaining nine: fidelity with the corresponding pure target
cannot decrease under partial trace.

Analytic examples, NOT executions of large quantum circuits:

| n | r | m | B | log2(epsilon) |
|---|---|---|---|---|
| 48 | 8 | 16 | 9 | -4.020408 |
| 96 | 16 | 32 | 9 | -8.066206 |
| 192 | 32 | 64 | 9 | -16.132639 |
| 384 | 64 | 128 | 9 | -32.265278 |
| 768 | 128 | 256 | 9 | -64.530557 |

Fresh independent retries must charge their failed batches. Selecting m
labels adaptively from a larger pool changes the input distribution and is
NOT covered by substituting the original epsilon. A polynomial-size pool
can contain exponentially many m-subsets; do not union-bound only over its
number of labels. This is a genuine open escape, not a proved obstruction.

## 5. Exact Finite Conversion Benchmark

For fixed a and delta define frequency distributions

    p_t = #{b:f(b)=t}/M,     q_t = #{z:t(z)=t}/D.

The best exact accepted probability among unrestricted physical instruments
is the linear-program optimum

    maximize sum_gamma w_gamma
    subject to w_gamma >= 0,
               sum_gamma w_gamma*q_(t-gamma) <= p_t
               for EVERY t in Z_N.                       (6)

Sketch: average an instrument over known input/output phase rotations.
Uniform-secret success and fidelity are preserved. Fourier-decomposing its
Kraus operators isolates frequency shifts gamma. On the normalized source
fiber state |chi_t>, an exact successful shift maps

    |chi_t> -> sqrt(w_gamma*q_(t-gamma)/p_t) |tau_(t-gamma)>,

where |tau_s> is the normalized uniform target-frequency fiber state.
The completeness inequality is precisely (6). Conversely its feasible
weights give a trace-nonincreasing map on the occupied source span, completed
with failure elsewhere. Multiple Kraus operators with the same shift add
their weights. Because the original accepted state is exactly pure, each
successful Kraus term must be aligned with that target.

The constraints on t OUTSIDE F are essential: they forbid any shift that
would demand unsupported target mass. One may eliminate these shifts first
and then solve only the remaining source-frequency constraints.

This is an abstract physical feasibility benchmark, NOT a scalable state
converter. Enumerating p and synthesizing maps on |chi_t> can require
exponential work and subset-sum inversion. Neither is free.

Focused LP controls using SciPy's existing solver:

| Input labels / N | Target labels | Exact optimum | Admissible shifts |
|---|---|---|---|
| (1,5,25,125) / 1024 | (1000,904) | 1/4 | 1 |
| (1,3,7) / 32 | (4,8) | 0 | 0 |
| (1,1,2) / 16 | (4,8) | 0 | 0 |
| (4,8,12) / 32 | (4,8) | 1 | 4 |
| (1,5,25) / 256 | (0,0,0) | 1 | 8 |

The last case deliberately violates the nonzero-output premise. The fourth
has strong arithmetic relations and shows why the generic-label premise is
not dispensable. A particular branch below succeeds with probability 1/2;
that is not its optimal physical conversion probability.

## 6. Correlated Blocks Retain Information

Compute f(b) modulo 2^r reversibly and measure only this low-bit register.
This takes polynomial arithmetic in m,n, has no rejected outcomes, and does
not require knowing fiber sizes. Let Y=y, F_y={b:f(b)=y mod 2^r}, D_y=|F_y|.
On the clean source the surviving state is

    |psi_(d,y)> = D_y^(-1/2) sum_(b in F_y) omega^(d*f(b)) |b>.

The outcome has probability D_y/M independent of d. Writing
f(b)=y+2^r*g_y(b) exhibits a phase vector over modulus 2^(n-r), up to an
irrelevant global phase. It is generally NOT a product of phase qubits.
Its index remains b with an implicit fiber predicate; no efficient compact
indexing is asserted.

Assume f is injective over the FULL modulus. This weaker event fails with
probability at most (3^m-1)/2^n, by the signed-difference union bound. Then
averaging each conditional state over d gives I_(F_y)/D_y. Consequently its
Holevo quantity is log2(D_y), and its outcome-weighted average is

    chi_clean = sum_y (D_y/M)*log2(D_y)
              = m - H(Y) >= m-r.                         (7)

For independent input dephasing of visibility nu in [0,1], the input entropy
is m*h2((1-nu)/2). The same low-bit probabilities and uniform-secret average
remain. An efficient projective measurement cannot increase average
conditional entropy: purify the input and apply entropy concavity to the
unchanged average reference marginal. Therefore

    chi_noisy >= m-H(Y)-m*h2((1-nu)/2)
              >= m-r-m*h2((1-nu)/2).                      (8)

Use max(0, right-hand side) as an informative numerical lower bound. With
m=2r and nu=1-1/n, the loss in this bound is O(r log(n)/n). Thus the earlier
fixed-weight recursive visibility collapse is NOT a proof that all useful
phase information has disappeared from these correlated blocks.

Operational blocker: Holevo quantity only upper-bounds accessible classical
information. It neither gives a measurement attaining that information nor
an efficient decoder. Computing f(b) into a second register and tracing out
b destroys all secret-dependent coherence in that register. Erasing b
requires an actual physical construction; injectivity does not give an
efficient inverse. Repeated low-bit measurement on the same small batch also
eventually isolates singletons and removes phase information. A larger
retained-state representation and useful recursive operation must be supplied.

## 7. Attempted Falsification And Executed Checks

Only short, inline mathematical diagnostics were run. No bulk tests, CLI
workflows, artifact refreshes, or new production modules were run/created.

1. Enumerated every Boolean coordinate function for B=1,2,3. Zero integer
   mixed second differences give exactly 4,6,8 functions, respectively:
   constants and signed coordinate projections. GF(2)-affinity is NOT enough.
2. Exhausted 5^4 coefficient vectors for a=(1,5,25,125), N=1024: no nonzero
   relation in [-2,2]^4. Selecting b=(12,9,6,3) gives an exact two-output
   phase product with labels (1000,904), acceptance 1/4. Both labels are
   divisible by four. This prevents the bound from rejecting ALL merging.
3. For a=(4,8,12), N=32, b=(0,1,2,4) gives an exact nonlinear two-output
   branch with acceptance 1/2, using the relation 4+8=12. With labels
   (4,20,100), N=256, the same row map and target (4,20) instead has joint
   accepted fidelity 5/8. That source still contains other complete target
   cubes: failure of this particular map is not an impossibility proof.
4. For a=(1,3,7), N=32 and target (4,8), selecting b=(0,3,5) into the first
   three output rows attains the GLOBAL support bound 3/4, with acceptance
   3/8. No translated complete target square exists. This checks tightness
   of (1) independently of the full-modulus generic-label argument.
5. Six dense complex Kraus operators, normalized together in three two-
   outcome instruments, were tested by explicit averaging over every d.
   Cases included colliding source frequencies and repeated target labels.
   Direct s,h matched the Fourier formulas within 1e-12. Success varied
   with d (ranges approximately 0.19 to 0.43); all support bounds held.
6. Exhausted the 64 low-label tuples for m=3,r=2,B=2 and all 72 nonempty
   ordered disjoint signed assignments. The relation event is 25/64; the
   simple union bound is vacuous here. No finite-size separation is claimed.
7. Solved the five finite LP controls above. These use ordinary numerical
   optimization, not certified rational duals or scalable implementations.
8. For a=(1,5,25,125), N=1024,r=2, fiber sizes are (2,4,6,4). Explicitly
   averaged conditional density matrices over all 1024 secrets and checked
   (7)-(8) for nu=1,.99,.9,.5,0. Clean chi=2.09436094; at .99 it is
   1.94422979 and at .9 it is 1.21426232; at zero it vanishes. The lower
   bound at .5 is negative and uninformative, as it should be.

Still unreviewed: the arbitrary-instrument quantifiers, cube-to-disjoint-
support reduction, exact LP optimality, and extension decisions need an
independent mathematical reviewer. Numerical checks do not certify them.

## 8. Scope And Prior Art

The obstruction does NOT cover adaptively regrouped large input pools,
correlated non-product outputs, large m where (3) is vacuous, supplied oracle
access, known-secret inputs, nonuniform secret priors, or output joint error
above the stated threshold. It does not bound arbitrary DCP running time,
direct secret measurement, or classical subset-sum algorithms. It does not
show that a different product sieve cannot improve known constants.

The exact spectral-support conversion principle is prior art in asymmetry
theory. Gour and Spekkens, Theorem 4, characterize stochastic U(1) pure-state
conversion by translated spectral containment. The present finite-cyclic
Fourier proof and random subset-sum application should be reviewed against
that literature, not marketed as a new physical principle:
https://arxiv.org/html/0711.0043v2#S3.SS4

Chefles gives general pure-state transformation criteria:
https://arxiv.org/abs/quant-ph/0109060

Probabilistic clock superreplication is also established; its fidelity and
success tradeoffs warn against invoking ordinary no-cloning to dismiss all
postselected transformations:
https://arxiv.org/abs/1304.2910

Retaining phase vectors is not a new DCP architecture by itself. Compare
Regev's recursive sieve and Kuperberg's collimation sieve before any novelty
claim:
https://arxiv.org/abs/quant-ph/0406151
https://arxiv.org/abs/1112.3333

## 9. Gemini Implementation Contract

Keep work in the existing DCP state-conversion/research reporting flow, not
a new candidate/experiment for every lemma. Main-model work remains theory.

1. Implement a small-instance frequency-fiber certificate that coherently
   sums K entries within fibers, counts target multiplicity, and reports
   direct Born-weighted s,h separately from h/s. Include dense Kraus and
   secret-dependent-success cases, not just basis selectors.
2. Implement (3)-(5) as analytic exact-integer/rational bounds with explicit
   model premises. Flag vacuous bounds, zero target labels, dense input
   regimes, regrouped pools and missing raw-sample accounting. NEVER apply
   the natural-label bound to a selected-label distribution automatically.
3. Add the finite LP (6) only as an unrestricted physical upper benchmark.
   Include constraints for absent source frequencies or eliminate invalid
   shifts first. Label enumeration/storage and fiber-state synthesis as
   unimplemented scalable costs. Rational certificates are preferable for
   claims of exact optimality; floating solver status alone is insufficient.
4. Reproduce the positive, negative and saturation controls in section 7.
   Include free zero-label |+> outputs and the nonlinear relation example
   as deliberate out-of-scope controls, not malformed data to ignore.
5. Add the implicit low-bit projection and clean/noisy Holevo checks as a
   countercontrol. Do not label chi as recovered bits or algorithm success.
   Keep b and all measured outcomes in the physical-state simulation.
6. Report the new obstruction and its correlated-block escape together.
   Do not broaden existing affine-only no-go modules or treat this as a
   universal barrier. No speedup gate should be enabled.
7. Independent review target: try adaptive pool selection, large joint
   error, repeated output labels, degeneracy and dense-source regimes first.
   A counterexample within all stated premises must block theorem promotion.

Next high-reasoning question: find a physically executable operation on an
implicit correlated phase block whose useful measurement statistics and
total cost can be bounded without a subset-sum inverse, exponentially long
search, or free reflection about an unknown input. Information retention
alone does not satisfy this requirement.
