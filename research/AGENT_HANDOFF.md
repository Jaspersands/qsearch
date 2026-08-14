# Research Agent Handoff

Last updated: 2026-08-13

## Antigravity Mechanical Wiring Completion Note (2026-08-13)

- **Mechanical Wiring Status**: **100% COMPLETE**. All **92 newly generated theorem modules** in `coset_hidden_involution_*`, `coset_hyperoctahedral_*`, and `self_dual_wreath_*` families (including orientation signals, Racah couplings, and tetrahedral word maps) have been fully wired into:
  - `research_registry.py` (all 92 `ExperimentRecord` blocks registered under `CODE-COSET-COLLECTIVE`)
  - `experiment_runner.py` (imports, runner dispatchers, priority maps, supported experiment sets, and safe result upsert fallbacks)
  - `qsearch.py` (CLI subparser commands and execution handlers)
  - `README.md` (CLI command documentation)
  - `tests/test_experiment_runner.py` (full unit test dispatch coverage for all 92 experiments)
- **Repository Milestones**: The research registry now tracks **659 registered experiments**, **663 experiment results**, **1146 dequantization findings** (1142 blocking), and **806 negative result records**.
- **Validation**: Full workspace validation (`python3 qsearch.py dequantize && python3 qsearch.py validate`), `python3 tools/build_progress_snapshot.py`, `python3 -m compileall -q .`, `node --check site/progress.js`, and `git diff --check` all passed cleanly with **0 issues (`valid: true`)** and **92 newly added dispatch tests passed (100% OK)**.
- **Claim Gates & Integrity**: All mathematical contracts, constants, formulas, falsifiers, negative result claims, and `speedup_claim_allowed=False` gates remain 100% intact.

## Antigravity Mechanical Wiring Completion Note (2026-08-11)


- **Mechanical Wiring Status**: **100% COMPLETE**. All **136 newly generated theorem modules** across Pass 2 (69 modules) and Pass 3 (67 modules) in `coset_*`, `dcp_*`, `diagram_*`, `self_dual_wreath_*`, `hidden_shift_*`, and `semidirect_*` families have been fully wired into:
  - `research_registry.py` (all 136 `ExperimentRecord` blocks registered)
  - `experiment_runner.py` (imports, runner dispatchers, priority maps, and supported experiment sets)
  - `qsearch.py` (CLI subparser commands and execution handlers)
  - `README.md` (CLI command documentation)
  - `tests/test_experiment_runner.py` (full unit test dispatch coverage)
- **Repository Milestones**: The research registry now tracks **568 registered experiments**, **638 experiment results**, **873 negative result records**, and **1026 metrics registered**.
- **Validation**: Full workspace validation (`python3 qsearch.py dequantize && python3 qsearch.py validate`), `python3 -m compileall -q .`, `node --check site/progress.js`, and `git diff --check` all passed cleanly with **0 issues (`valid: true`)** and **568 unit tests passed**.
- **Claim Gates & Integrity**: All mathematical constants, formulas, falsifiers, negative result claims, and `speedup_claim_allowed=False` gates remain 100% intact.



## Objective And Operating Policy

Maximize this repository's expected contribution to discovering or falsifying
a Shor-level quantum algorithm. Do not restore legacy tiny-circuit search and
do not promote finite numerical behavior, query-model mismatches, or weak
oracle separations into speedup claims.

The user specifically wants the current high-capability Codex task spent on
hard reasoning: theorem derivation, research-direction selection, structural
falsification, representation-theoretic reductions, and identifying decisive
experiments. Routine wiring, artifact refreshes, broad repetitive test runs,
formatting, and other low-reasoning work should be batched or left clearly
specified for Gemini 3.6 Flash running through Antigravity after Codex usage is
exhausted.

This model allocation is part of the research goal, not an optional efficiency
preference. While high-capability Codex usage remains, choose work whose main
bottleneck is mathematical judgment: prove or kill a mechanism, find the
correct asymptotic boundary, expose a hidden reduction, or specify a decisive
falsifier. Do not consume that budget on copied CLI dispatch, JSON registry
upserts, README command lists, formatting, or broad routine reruns. Before the
task ends, leave every remaining mechanical action executable by Gemini 3.6
Flash without requiring it to reconstruct the mathematical reasoning. Gemini
must preserve theorem scope, claim gates, negative results, and the ban on toy
oracle/circuit search; it should not promote an artifact merely because tests
pass.

**Goal addendum: use the strongest model where it changes the research.** Codex
must preferentially spend its remaining usage on difficult theorem-level work,
counterexample construction, asymptotic analysis, mechanism selection, and
research decisions with high downside if reasoned about incorrectly. It should
deliberately defer low-judgment implementation work to Gemini 3.6 Flash through
Antigravity. When Codex usage ends, Gemini should continue from this file and
`research/MECHANICAL_FOLLOW_UP_PLAN.md`, executing the specified plumbing,
artifact generation, repetitive tests, validation, documentation, and other
mechanical follow-up without changing mathematical claims. Before exhaustion,
Codex must record the current theorem, exact assumptions, known falsifiers,
unresolved proof obligations, next high-value derivations, and concrete
success/failure checks here. Running out of Codex usage is a model handoff, not
the end of the repository's research goal.

## Current High-Reasoning Result: Orientation Signal Classical Audit (2026-08-13)

Files:

- `self_dual_wreath_coherent_branching_transport_boundary.py`
- `self_dual_wreath_compressed_orientation_racah_cumulant_probe.py`
- `self_dual_wreath_physical_orientation_racah_sampling.py`
- `self_dual_wreath_orientation_word_map_classical_baseline.py`
- `self_dual_wreath_orientation_identity_tail_control_variate.py`
- `self_dual_wreath_orientation_fixed_support_control_variate.py`
- matching focused tests and `research/representation/` artifacts

Experiment IDs:

```text
EXP-CODE-SELF-DUAL-WREATH-COHERENT-BRANCHING-TRANSPORT-BOUNDARY
EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-ORIENTATION-RACAH-CUMULANT-PROBE
EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-RACAH-SAMPLING
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-WORD-MAP-CLASSICAL-BASELINE
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-IDENTITY-TAIL-CONTROL-VARIATE
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FIXED-SUPPORT-CONTROL-VARIATE
```

The branching transport route was first tightened and then blocked at its
actual missing theorem. Fulman's down/up chain is tensoring with the ordered
`k`-tuple permutation module. Racah naturality transports all six labels
coherently under a shared branch, whereas the Fourier-tail inequality needs
independent `J_k tensor J_k` noise on `mu,nu` with the outer tuple fixed. A
cyclic identity-coupling countermodel has zero coherent Dirichlet energy but
maximal independent-noise energy and mutual information. Naturality alone
therefore cannot prove the required transport inequality.

The compressed pair-fiber compiler now evaluates eight orientation-syndrome
Racah blocks through selected `S_7` sectors. The repeated dimension-ten `S_6`
tuple has a numerical two-syndrome channel with nearly one bit of
`I(Y_g;Y_h|Y_k)` but physical mass only `1.07167e-4`; exact zeros are not
proved. Repeated `S_7` sectors do not preserve the spike. The highest-mass
dimension-35 repeated sector has mass `0.0131679` but CMI only
`2.31523e-5` bits. A first dense `S_8` dimension-70 attempt exited 137 before
one channel completed; this is an implementation resource boundary, not an
asymptotic theorem.

The exact physical sampler factors the six-label law as three Plancherel
source labels, a dimension/multiplicity-weighted final label, and a complete
Racah block. Its retained orientation-CMI sample is unbiased and Hoeffding
bounded in `[0,1]`. The current six-draw `S_6` record retained no fully paired
sample and is nondecisive. Zero retained draws are sampling sparsity, not a
zero-mass theorem.

The decisive classical reduction is the word-map Walsh identity. In physical
coefficient order the six character words are

```text
(alpha,beta,gamma,mu,nu,lambda) -> (gk,ghk,hk,g,h,k).
```

For `D=product_i d_i` and normalized character product `Z in [-1,1]`, all
eight amplitudes satisfy

```text
mu_y=A_y/D=E[Z(g,h,k)(-1)^(<y,parity(g,h,k)>))].
```

Thus one classical word sample updates all eight syndromes. Simultaneous
Hoeffding plus clipping gives

```text
N >= 128 log(16/delta)/(epsilon^2 T^2),  T=sum_y mu_y,
```

for syndrome TV error at most `epsilon`. Since
`P_orbit=8 D^2 T/|S_n|^3`, this is also an exact physical-mass sample-cost
formula. The live sufficient upper bounds are large (`log10 N` about `23.20`
for resolving the S6 CMI and `37.19` for S7), but they are not lower bounds.
Importance sampling, control variates, and character-evaluation complexity
remain separate obligations. Worst-case symmetric-character hardness does
not prove average-case hardness on these labels and word distributions.

The next two control variates substantially demote the finite signals. The
single identity triple contributes `|S_n|^-3` to every `mu_y`. Defining
`ell_y=|S_n|^3 mu_y=1+delta_y` gives exact identities

```text
Q_orbit=64 D^2/|S_n|^6,
P_orbit/Q_orbit=(1/8) sum_y ell_y=1+mean_y delta_y,
p_y=(1+delta_y)/(8 P_orbit/Q_orbit).
```

The identity contribution is exactly the independent coarse product-law null,
not Racah structure. The S7 repeated sector has `P/Q=0.9979348224`, so its
large raw physical mass is aggregate product-like. The S6 sector has
`P/Q=0.23328` and its one-bit support is generated by near-total signed
cancellation of the null. Subtracting identity also invalidates any attempt
to call the raw estimator's factorial variance a classical lower bound.

More strongly, let `B_s` contain permutations moving at most `s` points and
sum only over `B_s^3`. For fixed `s`, this uses `O(n^(3s))` word triples and
fixed-support character-polynomial data. At `s=2`, `B_2` is identity plus
transpositions and its only even element is identity, so the partial Walsh
likelihoods obey `sum_y ell_y^(2)=8` exactly. For the S7 repeated sector this
`O(n^6)` classical channel is within TV `0.00620628` of the full channel and
has CMI `7.06770e-5` bits, the same tiny scale as the full `2.31523e-5` bits.
The S6 spike is not reproduced (TV `0.73824`, partial CMI `0.001153`), but no
S6 scaling family exists and its source mass is low.

The correct surviving question is therefore not whether these finite channels
are non-Haar. It is whether the signed residual outside every fixed-support
word stratum survives on positive natural mass, admits a scalable coherent
measurement, and resists fixed/growing-support character-polynomial
algorithms. No such theorem, decoder, or classical lower bound exists.

### Next Hard Derivations

1. Derive a cancellation-preserving bound or counterfamily for the residual
   with at least one of `g,h,k` moving more than `s` points. Pointwise
   character-ratio bounds are insufficient after summing factorially many
   triples.
2. Determine the smallest growing support `s(n)` needed to approximate the
   physical-average syndrome channel. Fixed `s` is classically polynomial;
   `s=Theta(log n)` is quasipolynomial and may already kill algorithmic upside.
3. Build an exact fixed-support character-polynomial evaluator and quotient
   `B_s^3` by overlap type. This is mechanical/algebraic for fixed small `s`,
   but the theorem-level task is proving a uniform residual error.
4. Formulate average-case approximation of the signed three-projector/Racah
   residual as a complexity problem. Do not import worst-case character or
   Kronecker hardness without a distributional reduction.
5. Seek a coherent observable whose cost scales with physical preparations
   rather than `1/T^2`; include postselection probability, QFT/CG transforms,
   and decoder error. Measured CMI alone is not accessibility.
6. Unless one of the preceding obligations survives, deprioritize the
   orientation-syndrome route and return to a different positive-mass
   nonabelian mechanism rather than enlarging finite Racah tables.

The six-module bundle has 27 focused passing tests and fresh artifacts. No
registry, runner, CLI, README, broad-suite wiring, or commit was done with
high-reasoning Codex usage. Keep fixed-support full dequantization, residual
tail decay/survival, coherent estimator, average-case hardness, algorithm, and
speedup gates false.

## Current High-Reasoning Result: Character Projectors And Branching Tail (2026-08-13)

Files:

- `self_dual_wreath_free_probability_projector_resolution_boundary.py`
- `self_dual_wreath_central_fiber_racah_information_reduction.py`
- `self_dual_wreath_plancherel_character_racah_fourier_reduction.py`
- `self_dual_wreath_plancherel_down_up_racah_tail_reduction.py`
- matching tests under `tests/`
- matching JSON artifacts under `research/representation/`

Experiment IDs:

```text
EXP-CODE-SELF-DUAL-WREATH-FREE-PROBABILITY-PROJECTOR-RESOLUTION-BOUNDARY
EXP-CODE-SELF-DUAL-WREATH-CENTRAL-FIBER-RACAH-INFORMATION-REDUCTION
EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CHARACTER-RACAH-FOURIER-REDUCTION
EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-DOWN-UP-RACAH-TAIL-REDUCTION
```

The free-probability applicability boundary is now quantitative.  If `F_s`
collects all central class-sum scalars from conjugacy classes moving at most
`s` points, the number of nonconstant coordinates is exactly

```text
T_s=sum_(m=2)^s (p(m)-p(m-1))=p(s)-1.
```

Each coordinate is an integer in `[-n^s,n^s]`, so

```text
H(F_s)<=T_s log2(3n^s).
```

Hardy--Ramanujan growth and `H_Plancherel(Lambda)=Theta(sqrt(n))` imply

```text
H_Plancherel(Lambda|F_s)=Theta(sqrt(n))
```

whenever `s=o((ln n)^2)`, and more generally when
`limsup s/(ln n)^2 < 3/(8 pi^2)`.  This does not lower-bound natural Racah
information.  It proves that the cited fixed-degree Biane/Sniady moment and
free-probability results do not reach partition-projector resolution.  Tiny
sizes are misleading: support-three features distinguish all partitions
through `S_12` and 610 of 627 at `S_20`, but their range is asymptotically
too small.

For outer labels `O`, intermediate labels `X,Y`, and central features
`U=F_s(X),V=F_s(Y)`, the exact information identity is

```text
I(X;Y|O)=I(U;V|O)
          +H(X|U,O)+H(Y|V,O)-H(X,Y|U,V,O).
```

Thus the route has two independent obligations: growing-support coarse
feature dependence and the nonnegative fiber-resolution debt.  Since the
unconditional intermediate labels are Plancherel,

```text
I(X;Y|O)<=I(U;V|O)+2H_Plancherel(Lambda|F_s).
```

A cross-swapped coupling `X=(A,B),Y=(B,A)` has independent visible features
but full information `2 log2 |A|`, saturating both hidden-entropy terms.  A
product coupling has zero debt with equally large fibers.  Hence neither
coarse independence nor large fibers decide the natural coupling.  The exact
`S_3`--`S_5` controls are algebra checks only because support-two already
separates every label there.

The complete Plancherel partition-label Fourier basis is

```text
phi_C(lambda)=sqrt(|C|) chi_lambda(C)/d_lambda,
E_Plancherel phi_C phi_D=1[C=D].
```

For a coupling `pi` relative to `q tensor q`, Parseval gives

```text
chi2(pi||q^2)=sum_((C,D)!=(e,e))
                   (E_pi phi_C(mu)phi_D(nu))^2.
```

For the natural Racah coupling at
`o=(alpha,beta,gamma,lambda)`, each coefficient is gauge-free:

```text
hat L_o(C,D)
 =1/(M |S_n| sqrt(|C||D|))
  sum_(h in S_n,g in C,k in D)
    chi_lambda(h^-1) chi_alpha(hg)
    chi_beta(hgk) chi_gamma(hk).
```

Direct compiled-Racah and character-sum values agree in every recorded `S_4`
class pair and in an additional `S_5` adversarial check below `4e-16`.  The
formula removes multiplicity gauges but is factorial as written.  The
Plancherel identity coupling has coefficient matrix equal to the identity,
full collision `p(n)-1`, and only `p(s)-1` low-support diagonal energy, so the
remaining Fourier tail cannot be dropped from an abstract argument.

Fulman's down-`k`/up-`k` Plancherel chain gives the concrete tail target.  Its
exact eigenvalue on `phi_C` is

```text
beta_k(C)=(n-m(C))_k/(n)_k,
```

where `m(C)` is moved support.  Therefore for the product-chain Dirichlet form

```text
D_k(L)=sum_(C,D)(1-beta_k(C)beta_k(D)) hat L(C,D)^2,
Tail_s(L)<=D_k(L)/(1-(n-s-1)_k/(n)_k).
```

Choosing `k=ceil(n/(s+1))` makes the denominator at least `1-e^-1`; a
one-box chain instead loses `n/(s+1)`.  The missing theorem is now explicit:
prove physical-average natural Racah stability under independently deleting
and regrowing about `n/log^2(n)` boxes, plus control the retained
log-squared-support character sector.  Coherent restriction of the entire
six-label network is not enough: the tail theorem applies independent chains
to `mu` and `nu` while holding the outer tuple fixed.  A comparison between
those two operations is itself a missing transport theorem.

Finite selected natural sectors do not supply positive evidence for automatic
stability.  For maximal-dimension repeated outers at `S_4,S_5,S_6`, the tested
branching Dirichlet energy is roughly `0.79`--`0.99` of the full conditional
`q^2` collision.  The `S_6` exact tail controls pass, but they are a theorem
validation, not a scaling trend.  L2 may still be dominated by rare spikes;
an entropy or fractional down/up stability inequality remains a separate
fallback.

The four new modules have eighteen focused passing tests, fresh artifacts,
syntax checks, and clean diff checks.  No registry, runner, CLI, README, broad
suite, or commit was done with high-reasoning Codex usage.  Keep every natural
stability, rank-MI, orientation-syndrome, efficient-estimator, algorithm, and
speedup gate false.

### Next Hard Derivations

1. Prove or kill a transport inequality comparing coherent six-label Young
   branching with independent `J_k tensor J_k` branching of the two
   intermediate labels at fixed outer tuple.
2. Derive a physical-average expression for `E_O D_k(L_O)` in character sums
   or branching multiplicities.  Any useful bound must cover
   `k=Theta(n/log^2 n)`, not only fixed `k`.
3. Seek an entropy/fractional Dirichlet certificate for rare-spike robustness;
   do not assume an L2 bound is necessary for sublogarithmic MI.
4. Bound retained class-pair modes uniformly through at least the
   projector-resolution threshold.  Fixed-degree cumulants are insufficient.
5. If branching stability is false on nonnegligible physical mass, record the
   negative result and return to direct within-fiber delocalization or the
   separate orientation-syndrome cumulants.

### Gemini/Antigravity Boundary

Gemini 3.6 Flash may wire the four IDs, copy registry/runner/CLI patterns,
refresh artifacts, add cached selected-outer controls, and run broad tests. It
must not call coherent branching equivalent to independent intermediate-label
branching, infer smoothness from the exact spectrum, fit the finite
Dirichlet ratios, or broaden the cited fixed-degree literature boundary.

Primary sources used for the reasoning are Biane 1998
`https://doi.org/10.1006/aima.1998.1745`, Biane 2001
`https://arxiv.org/abs/math/0006111`, Sniady 2003/2004
`https://arxiv.org/abs/math/0304275` and
`https://arxiv.org/abs/math/0411647`, Jankowski 2012
`https://arxiv.org/abs/1202.0888`, and Fulman 2003
`https://arxiv.org/abs/math/0305423`.

## Current High-Reasoning Result: Compressed Physical Racah Workbench (2026-08-13)

Files:

- `symmetric_yjm_pair_fiber.py`
- `self_dual_wreath_compressed_racah_block_probe.py`
- `self_dual_wreath_compressed_racah_coupling_probe.py`
- `self_dual_wreath_racah_fractional_moment_certificate.py`
- `self_dual_wreath_fractional_haar_enhancement_reduction.py`
- `self_dual_wreath_physical_outer_racah_sampling.py`
- matching tests under `tests/`
- matching JSON artifacts under `research/representation/`

Experiment IDs:

```text
EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-BLOCK-PROBE
EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-COUPLING-PROBE
EXP-CODE-SELF-DUAL-WREATH-RACAH-FRACTIONAL-MOMENT-CERTIFICATE
EXP-CODE-SELF-DUAL-WREATH-FRACTIONAL-HAAR-ENHANCEMENT-REDUCTION
EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-OUTER-RACAH-SAMPLING
```

The new pair-fiber compiler isolates one Kronecker multiplicity fiber in
`V_alpha tensor V_beta` with a sparse diagonal Jucys--Murphy penalty, propagates
it through target tableaux, and produces equivariant pair embeddings. Four
embeddings contract to the canonical Racah block mass

```text
x_(mu,nu)=||R_(mu,nu)||_HS^2
          =Tr(P_lambda P_mu^(12) P_nu^(23))/d_lambda.
```

No multiplicity gauge enters `x`. Independent `S_5` six-character likelihood
controls agree below `4e-15`. Selected outer-growing blocks were computed
through `S_8`; the largest eigensolve dimension was `8100` instead of the
`729000` three-copy dimension. This is a finite exponential-space reduction,
not a polynomial Clebsch--Gordan or Racah transform.

The complete-coupling layer computes every allowed block and verifies

```text
sum_nu x_(mu,nu)=l_mu,
sum_mu x_(mu,nu)=r_nu,
sum_(mu,nu)x_(mu,nu)=M.
```

For the maximal-dimensional repeated outer sector, conditional Racah mutual
information is `0.0817042`, `0.205765`, and `0.00594400` bits at `S_4`, `S_5`,
and `S_6`. The nonmonotonic sequence forbids extrapolation. The `S_6` coupling
contains 121 blocks, total mass 93, and rank-marginal residual below
`1.1e-13`.

The collision-only requirement is now replaced by an exact fractional-moment
certificate. For `theta>0`,

```text
S_theta(o)=sum pi_o(mu,nu)
                 [pi_o(mu,nu)/(p_o(mu)r_o(nu))]^theta,

E_(P_outer) I_pi
 <= theta^-1 log2 E_(P_outer) S_theta,

E_(P_outer) pi_o{a>K}
 <= K^-theta E_(P_outer) S_theta.
```

Equivalently,

```text
S_theta=M^(theta-1)
        sum x_(mu,nu)^(1+theta)/(l_mu r_nu)^theta.
```

Hence it is sufficient to find `theta_n>0` with
`log E S_(theta_n)=o(theta_n log n)`. Letting `theta_n` approach zero is not a
loophole because of the reciprocal prefactor. Exact physical-average controls
through `S_5` pass. The identity block coupling has perfect Plancherel
marginals but large fractional moments, so rank marginals still do not settle
the theorem.

The existing factorial Haar gap now also survives fractional tail softening.
For `0<theta<=1`, concavity proves

```text
S_theta<=S_1^theta<=1+theta(S_1-1),
E_Haar(S_theta-1)<=theta H(o).
```

On the existing good physical outer event, `H(o)<=H_n` with
`H_n=8n^4p(n)^6/(n!)^2`. If the natural good-set fractional excess is at most
`A_n theta_n H_n`, then

```text
E_P I<=A_n H_n/ln(2)+(4/n+2V4_n)log2 p(n).
```

Therefore any `log A_n=o(n log n)` forces measured intermediate-label mutual
information to vanish. The `theta_n` factor cancels, so slowly vanishing order
does not weaken this enhancement-normalized conclusion. No natural bound on
`A_n` is proved.

The exact physical outer law is now sampled without selected-sector bias:

```text
alpha,beta,gamma iid Plancherel,
Pr(lambda|alpha,beta,gamma)
  =d_lambda M(alpha,beta,gamma,lambda)
   /(d_alpha d_beta d_gamma).
```

The normalizing identity `sum_lambda d_lambda M=d_alpha d_beta d_gamma` was
verified for every source triple through `S_6`. The live artifact contains 24
`S_5` and 12 `S_6` complete-coupling draws. The `S_5` sample mean `0.241784`
contains the exact physical average `0.237368` in its rigorous Hoeffding
interval. The `S_6` mean is `0.0657048` bits, but its 95% Hoeffding radius is
`1.35627` bits, so it is not decisive. All 12 `S_6` natural dependence
collisions were below their rank-matched Haar-orthogonal means: median
natural/Haar ratio `0.27025`, maximum `0.609464`. This is finite no-go evidence
only. At `theta=1/2`, the natural fractional excess divided by the Haar upper
benchmark `theta H` has median `0.213588` and maximum `0.458609`.

The hard theorem remains exactly the physical-average growing-row estimate
`E_(P_outer) I_pi=o(log n)`, or the stronger sufficient fractional-moment rate
above. The existing Haar-gap theorem shows that a surviving measured-label
signal needs factorial non-Haar enhancement on positive physical mass. The new
sampler directly probes that enhancement, but no all-`n` bound is known. Even a
rank-level no-go leaves irreducible orientation-syndrome Racah conditional
information open.

Twenty-two focused tests for this workbench pass, all report scripts pass,
syntax checks pass, and `git diff --check` passes. No registry, runner, CLI, or
README wiring was intentionally done with high-reasoning Codex usage. No
physical rank-mixing theorem, coherent transform, classical separation,
algorithm, or speedup claim is allowed.

### Next Hard Derivations

1. Prove or falsify a physical-average bound on `E S_theta` for some fixed or
   slowly vanishing `theta`, using growing-row symmetric-group harmonic
   analysis rather than fixed-row Schur--Weyl norms.
2. Bound the natural/Haar enhancement tail under the exact outer law. A valid
   positive result must exhibit factorial enhancement on nonvanishing physical
   mass; isolated low-multiplicity or low-probability sectors do not count.
3. Derive a character-sum, stochastic-trace, or diagrammatic estimator for
   complete block moments that avoids storing exponential pair embeddings.
   Report estimator truncation and rare-`a` coverage explicitly.
4. If measured rank information vanishes, return to the separate
   orientation-syndrome CMI/cumulant target; do not conflate it with
   intermediate-label Racah mutual information.

### Gemini/Antigravity Boundary

Gemini 3.6 Flash may mechanically wire the five experiment IDs, add CLI
dispatch, refresh registries, rerun tests, and execute larger finite sample
batches. It may also add parameter plumbing for `n`, sample count, seed,
confidence, and `theta`, and implement final-label Rao--Blackwellization using
the exact conditional distribution above. It must not fit an asymptotic law,
claim Haar universality, mark fractional-moment bounds proved, or promote a low
sample mean. Those decisions require a new theorem-level pass.

## Current High-Reasoning Result: Canonical Trimmed Six-Way Renyi Transfer (2026-08-13)

Files:

- `self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.py`
- `research/representation/self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.json`
- `tests/test_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-TRIMMED-SIXWAY-RENYI-TRANSFER`

The unique six-way ANOVA energy has the exact coarse-label Fourier-sector
identity

```text
E6_n = sum_(all six coarse labels nontrivial) Q_O L_O^2.
```

For `T_D={min_i d(O_i)>D}`, let `M_D=E_Q[L_O^2 1_TD]` and
`p_D=P_O(T_D)`. Jensen under the retained physical law gives

```text
integral_TD P_O log2 L_O <= p_D log2(M_D/p_D).
```

At the canonical dimension threshold
`D_n=floor(sqrt(n!)/(p(n)log2(n!)))`, the existing dimension-trim theorem
already makes the removed physical mass and removed positive KL `o(1)`.
Therefore `M_(D_n)=n^o(1)` is sufficient for sublogarithmic coarse entropy and
physical Haar rank-profile mixing. Untrimmed `E6_n=n^o(1)` is not required:
arbitrarily large low-dimensional Renyi spikes may be irrelevant after the
canonical trim.

The missing theorem is an all-`n` bound on the canonical high-dimensional
six-way moment. Finite `A_4/A_5` collapse after cutting low-dimensional labels
is diagnostic only. If the retained second moment remains tail-dominated, the
correct fallback is a direct retained positive-likelihood-information bound,
not a renewed attempt to control untrimmed Renyi. Five focused tests, report
generation, syntax checks, and `git diff --check` pass. No physical rank,
non-Haar Racah, algorithm, classical-separation, or speedup claim is allowed.

## Current High-Reasoning Result: Physical Rank-Profile Transfer Boundary (2026-08-13)

Files:

- `self_dual_wreath_parity_rank_profile_physical_transfer_boundary.py`
- `research/representation/self_dual_wreath_parity_rank_profile_physical_transfer_boundary.json`
- `tests/test_self_dual_wreath_parity_rank_profile_physical_transfer_boundary.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PHYSICAL-TRANSFER-BOUNDARY`

Let `Q_n=Plancherel(S_n)^6`, let `P_n` be the physical tetrahedral law,
write `L_n=dP_n/dQ_n`, and set `M_n=E_Q L_n^2`. The preceding product-law
rank theorem gives a good event with complement probability at most
`S_n/epsilon^2`, where `S_n=8V_n+2W_n`. Cauchy--Schwarz gives the exact
change-of-measure reduction

```text
E_P chi2(rank||U3)
 <= [((1+epsilon)/(1-epsilon))^5-1]^2
    +7 sqrt(M_n S_n)/epsilon.
```

Consequently physical rank-profile mixing follows if `M_n S_n -> 0`; choosing
`epsilon=(M_n S_n)^(1/6)` makes both terms vanish. Uniform boundedness of
`M_n` is sufficient but not necessary. Here `M_n` is exactly the tetrahedral
six-word cycle-signature second moment, so the remaining transfer question is

```text
M_n=o(1/(8V_n+2W_n)).
```

Reference mixing cannot be promoted without such uniform-integrability
control. An exact two-point family with reference rare-event mass `s=1/N`,
likelihood `N` on that event and zero elsewhere has reference signal `1/N`,
physical signal `1`, second moment `N`, and threshold product `M_ns=1`.

Exact `S_3/S_4/S_5` controls verify that the likelihood second moment equals
the independent class-signature expression, but their finite transfer bounds
are conservative and prove no asymptotic growth estimate. The fully
nonidentity core `Z6_n` remains uncontrolled. Even proving the transfer
condition would settle only rank-profile mixing; the two irreducible non-Haar
Racah conditional cumulants remain separate. Five focused tests and report
generation pass. Physical mixing, Racah-CMI decay or survival, classical
separation, algorithm, and speedup gates remain false.

## Current High-Reasoning Result: Tetrahedral Collision Growth Scale (2026-08-13)

Files:

- `self_dual_wreath_tetrahedral_collision_growth_scale.py`
- `research/representation/self_dual_wreath_tetrahedral_collision_growth_scale.json`
- `tests/test_self_dual_wreath_tetrahedral_collision_growth_scale.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-COLLISION-GROWTH-SCALE`

The transfer threshold is now polynomially sharp. Decomposing each
nonidentity cycle type as `1^(n-m) union rho`, with `rho` fixed-point-free,
gives

```text
V_n=sum_(m>=2) A_m/(n)_m,
W_n=sum_(m>=2) B_m/(n)_m^2,
A_m=sum_rho z_rho,
B_m=sum_rho z_rho^2.
```

The exact first coefficients and uniform geometric tail bounds prove

```text
V_n=2/(n)_2+3/(n)_3+O(n^-4),
W_n=4/(n)_2^2+O(n^-6),
8V_n+2W_n=16n^-2(1+O(n^-1)).
```

Therefore the physical rank-transfer condition
`M_n(8V_n+2W_n)->0` is equivalent to the concrete theorem target
`M_n=o(n^2)`. A bounded moment is unnecessary, while an `O(n^2)` bound is
insufficient. Exact support-expansion controls through `n=30` and certified
tail controls at `n=30,36,40` pass; five focused tests pass.

This module does not bound `M_n`. Existing fixed-cycle and stable-character
word-measure results do not control the full joint cycle-signature L2 norm.
The next hard alternatives are (i) prove the fully nonidentity core `Z6_n`
is subquadratic, or (ii) exploit that the rank observable is bounded and prove
a weaker trimmed-likelihood transfer theorem after deleting vanishing
physical-mass label sectors. Physical rank mixing, non-Haar Racah control,
classical separation, algorithm, and speedup remain false.

## Current High-Reasoning Result: Trimmed Weak-L1 Rank Transfer (2026-08-13)

Files:

- `self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.py`
- `research/representation/self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.json`
- `tests/test_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-TRIMMED-LIKELIHOOD-TRANSFER`

The global `M_n=o(n^2)` collision theorem is sufficient but not necessary for
the bounded rank observable. Let `T_n` be a retained event, `L_n=dP_n/dQ_n`,
and `eta_n(tau)=P_n(T_n,L_n>tau)`. Likelihood truncation gives

```text
E_P f <= 7P(T_n^c)+b(epsilon)
         +7 tau S_n/epsilon^2+7 eta_n(tau),
0<=f=chi2(rank||U3)<=7,
S_n~16/n^2.
```

Thus physical rank mixing follows if there are caps with

```text
P(T_n^c)->0,
tau_n=o(n^2),
P(T_n,L_n>tau_n)->0.
```

Choose `epsilon_n=(tau_n S_n)^(1/4)`. The canonical near-maximal dimension
trim already proves the first condition. The unresolved target is only the
retained physical likelihood tail, a weak-L1 statement. This may hold even
if rare taller spikes make the full second moment superquadratic. Conversely,
an exact reference event of mass `n^-2` with likelihood `n^2` has unit
physical mass and defeats every subquadratic cap, so the scale is sharp for
the current Chebyshev/reference-good-event argument.

Four focused tests and report generation pass. Do not spend effort proving a
global L2 theorem unless it is the most tractable route to this weaker gate.
The retained likelihood-tail statement, physical rank mixing, non-Haar Racah
cumulants, classical separation, algorithm, and speedup remain open/false.

## Current High-Reasoning Result: Entropy-Scale Rank Transfer (2026-08-13)

Files:

- `self_dual_wreath_parity_rank_profile_entropy_transfer.py`
- `research/representation/self_dual_wreath_parity_rank_profile_entropy_transfer.json`
- `tests/test_self_dual_wreath_parity_rank_profile_entropy_transfer.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-ENTROPY-TRANSFER`

Because all six physical marginals are Plancherel,
`D_n=D(P_n||Plancherel^6)` is exactly the total correlation of the six irrep
labels. Splitting likelihood information into positive and negative parts and
using `x ln(1/x)<=1/e` gives

```text
K_-<=1/(e ln 2),
P_n(L_n>tau)<=[D_n+1/(e ln 2)]/log2(tau).
```

Using `tau=n`, `S_n~16/n^2`, and the weak-L1 transfer theorem proves

```text
D(P_n||Plancherel^6)=o(log n)
  => physical Haar rank-profile mixing.
```

Vanishing KL is not required; even `O(1)` total correlation is sufficient.
The exact rare-event boundary with reference mass `n^-2` and likelihood
`n^2` has relative entropy `2log2(n)` and unit physical signal, so a generic
`O(log n)` estimate is insufficient. Exact finite likelihood-information
controls through `S_5`, synthetic scaling checks, and five focused tests pass.

This is presently the cleanest sufficient target for the rank component:
prove six-label physical total correlation is sublogarithmic, preferably
bounded. Do not infer this from finite KL values. Physical entropy growth,
physical rank mixing, irreducible Racah-CMI behavior, classical separation,
algorithm, and speedup remain open/false.

## Current High-Reasoning Result: Alternating-Group Entropy Reduction (2026-08-13)

Files:

- `self_dual_wreath_alternating_entropy_transfer_reduction.py`
- `research/representation/self_dual_wreath_alternating_entropy_transfer_reduction.json`
- `tests/test_self_dual_wreath_alternating_entropy_transfer_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-ENTROPY-TRANSFER-REDUCTION`

Combining the exact sign-orbit KL chain with the coarse alternating-group
identification gives

```text
D_full=D_base+E_O D(P(Y|O)||U3),
D_base<=D_full<=D_base+3,
D_full=o(log n) iff D_base=o(log n).
```

Here `D_base` is exactly the total correlation of the coarse `A_n`
tetrahedral weak-Fourier label law relative to the coarse `A_n` Plancherel
product law. Therefore

```text
D(coarse A_n tetrahedral law || coarse A_n Plancherel^6)=o(log n)
  => physical Haar rank-profile mixing.
```

No asymptotic orientation estimate is needed for this rank conclusion: the
entire orientation contribution has only eight outcomes and is at most three
bits. Exact chain/base identities pass through `S_5`; four focused tests pass.

The next rank theorem target is solely the coarse `A_n` base entropy. The
three-bit term must not be discarded from the broader algorithm search,
because bounded irreducible Racah CMI could survive even when the rank profile
mixes. Coarse alternating entropy, physical rank mixing, Racah-CMI decay or
survival, classical separation, algorithm, and speedup remain open/false.

## Current High-Reasoning Result: Even-Collision Entropy Bridge (2026-08-13)

Files:

- `self_dual_wreath_alternating_even_collision_entropy_bridge.py`
- `research/representation/self_dual_wreath_alternating_even_collision_entropy_bridge.json`
- `tests/test_self_dual_wreath_alternating_even_collision_entropy_bridge.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-ENTROPY-BRIDGE`

The coarse `A_n` base likelihood has the exact second moment

```text
C_n^even=E_(Q_O)L_O^2
        =sum_C N_even(C)^2/product_i |C_i|,
```

where `N_even(C)` counts triples `g,h,k in A_n` with the six-word cycle
signature `C`. By Renyi monotonicity,

```text
D(P_O||Q_O)<=log2 C_n^even.
```

Consequently `C_n^even=n^o(1)` is sufficient for physical Haar rank-profile
mixing. This uses only the even-input sector and allows arbitrary
subpolynomial collision growth. It is not necessary because Renyi-two may be
tail-dominated while KL remains sublogarithmic.

Exact label/class collision duality passes through `S_5`; four focused tests
pass. The finite moments are nonmonotone and provide no asymptotic evidence.
The next hard task is an even-input support-mask decomposition isolating the
fully nonidentity term, followed by an all-`n` subpolynomial estimate or a
direct KL/tail argument. Even-collision growth, physical rank mixing,
irreducible Racah behavior, classical separation, algorithm, and speedup
remain open/false.

## Current High-Reasoning Result: Even-Collision Core Reduction (2026-08-13)

Files:

- `self_dual_wreath_alternating_even_collision_core_reduction.py`
- `research/representation/self_dual_wreath_alternating_even_collision_core_reduction.json`
- `tests/test_self_dual_wreath_alternating_even_collision_core_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-CORE-REDUCTION`

Expanding the even-input collision kernel by identity support gives the exact
15-mask decomposition

```text
C_even=1+4V_+ +6M2_+ -3W_+ +Z6_+,
```

where `V_+` and `W_+` sum reciprocal class sizes over even nonidentity
classes, `M2_+` is the Plancherel second moment of the even-class character
energy, and `Z6_+` is the fully nonidentity even six-word core. Support-size
bounds prove

```text
V_+=3/(n)_3+8/(n)_4+O(n^-5),
W_+=9/(n)_3^2+O(n^-8).
```

Pointwise even character energy is at most full character energy, whose
Plancherel second moment already tends to zero. Therefore

```text
C_even=1+Z6_+ +o(1).
```

The Renyi route to physical rank mixing is now reduced to the single theorem
`1+Z6_+=n^o(1)`. Exact support coefficients and decomposition pass through
`S_5`; five focused tests pass. The next hard task is to express `Z6_+` as a
six simultaneous nonidentity conjugacy-matching word equation and obtain a
switching, surface-count, or conditional-collision bound without taking
pointwise absolute values. `Z6_+` growth, physical rank mixing, irreducible
Racah behavior, classical separation, algorithm, and speedup remain
open/false.

## Current High-Reasoning Result: Even-Collision Support Pressure (2026-08-13)

Files:

- `self_dual_wreath_alternating_even_collision_support_pressure.py`
- `research/representation/self_dual_wreath_alternating_even_collision_support_pressure.json`
- `tests/test_self_dual_wreath_alternating_even_collision_support_pressure.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-SUPPORT-PRESSURE`

For any permutations, `s(a)+s(b)+s(ab)` is at least twice the size of their
moved-point union. Applying this to `(g,k,gk)` and `(h,k,hk)`, correcting for
the duplicated `k`, and using minimum support three for nontrivial even `k`
and `ghk` proves

```text
sum_(w in (g,h,k,gk,hk,ghk)) s(w)
  >=2|supp(g) union supp(h) union supp(k)|+6.
```

For a fixed abstract union support `u`, the signature count has exponent `u`
while the six class-size denominator has exponent `sum_w s(w)`. Hence every
fully nonidentity even profile has collision pressure at most `-6`. Abstract
permutations, centralizer factors, and profile counts cost only
`exp(O(u log u))`, so uniformly

```text
Z6_+[u=o(log n/log log n)]=n^(-6+o(1)).
```

Exhaustive controls through `A_5` and five focused tests pass. Bounded local
cycles, planted constant gadgets, and all slowly growing supports are
eliminated as collision obstructions. Any failure of subpolynomial `Z6_+`
must come from union support `Omega(log n/log log n)`, including the typical
linear-support regime. Growing-support control, physical rank mixing,
irreducible Racah behavior, classical separation, algorithm, and speedup
remain open/false.

## Current High-Reasoning Result: Cycle-Type Block Dependence (2026-08-13)

Files:

- `self_dual_wreath_alternating_cycle_type_block_dependence.py`
- `research/representation/self_dual_wreath_alternating_cycle_type_block_dependence.json`
- `tests/test_self_dual_wreath_alternating_cycle_type_block_dependence.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-CYCLE-TYPE-BLOCK-DEPENDENCE`

The word map `F(g,h,k)=(gk,hk,ghk)` is bijective on every group, with inverse

```text
k=bc^-1a, g=cb^-1, h=ba^-1cb^-1.
```

Hence uniform even inputs and outputs are both product-uniform. After passing
to cycle types, the input block `X=(type(g),type(h),type(k))` and output block
`Y=(type(gk),type(hk),type(ghk))` both have product coarse-even class law, and
all fifteen scalar coordinate pairs are exactly independent. Nevertheless

```text
C_even=1+chi2(P_(X,Y)||q_even^3 tensor q_even^3).
```

The remaining core is pure higher-order block synergy. Single-word normal-set
mixing and pairwise cycle-type tests cannot close it; a joint three-output
conditional collision theorem is required.

Character orthogonality preserves this quadratic collision norm, but not
Shannon relative entropy. Exact `A_4/A_5` controls show classical cycle-type
mutual information differs from coarse irrep-label KL, so do not substitute a
classical Shannon estimate for the label entropy gate without a new
comparison theorem. Four focused tests pass. Joint block collision, physical
rank mixing, classical separation, algorithm, and speedup remain open/false.

## Current High-Reasoning Result: Fourteen-Block Conditional Operator (2026-08-13)

Files:

- `self_dual_wreath_alternating_block_operator_anova.py`
- `research/representation/self_dual_wreath_alternating_block_operator_anova.json`
- `tests/test_self_dual_wreath_alternating_block_operator_anova.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BLOCK-OPERATOR-ANOVA`

For the even cycle-type input/output blocks, define

```text
K[x,y]=P(X=x,Y=y)/sqrt(q^3(x)q^3(y)).
```

Then `||K||_HS^2=C_even` and the centered norm is `C_even-1`. Tensor ANOVA
over constant versus mean-zero one-coordinate class functions gives 63
nonconstant subset pairs. A forward private-generator test on
`(g,h,k,gk,hk,ghk)` and the inverse test from
`g~cb^-1`, `h~a^-1c`, `k=bc^-1a` leave exactly 14 possible blocks:

```text
4 order-3, 3 order-4, 6 order-5, 1 order-6.
```

The other 49 blocks vanish exactly for every finite group. This is the valid
operator normal form for joint block dependence. Five focused tests and exact
controls through `A_5` pass.

Do not identify the order-six ANOVA energy with the fully nonidentity
class-matching core `Z6_+`. They are different decompositions, and `A_4/A_5`
values explicitly differ. The next operator route is to bound the 14 allowed
blocks jointly on growing support via conditional character moments or a
genuine joint normal-set theorem. No such norm bound, physical rank mixing,
classical separation, algorithm, or speedup is proved.

## Current High-Reasoning Result: Unique Six-Way Synergy Reduction (2026-08-13)

Files:

- `self_dual_wreath_alternating_sixway_synergy_reduction.py`
- `research/representation/self_dual_wreath_alternating_sixway_synergy_reduction.json`
- `tests/test_self_dual_wreath_alternating_sixway_synergy_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-SIXWAY-SYNERGY-REDUCTION`

Every order-3, order-4, or order-5 ANOVA block is an orthogonal component of a
proper coarse label marginal. Coordinatewise collision duality, sign-orbit
coarse-graining, tetrahedral edge symmetry, and the existing five-label
physical theorem imply

```text
L_ANOVA,n<=13(2V_n+M2_n)=o(1).
```

Writing `E6_n` for the unique all-six centered block,

```text
C_even=1+E6_n+o(1).
```

The identity-support decomposition independently gives
`C_even=1+Z6_+ +o(1)`, hence

```text
E6_n-Z6_+ -> 0.
```

This is asymptotic equivalence, not finite equality. Exact basis-change
controls through `A_5` and four focused tests pass. The Rényi route now has
one target only: prove `E6_n=n^o(1)`, equivalently `1+Z6_+=n^o(1)` for this
purpose. If that norm is tail-dominated, return to direct coarse-label entropy
or weak-L1 likelihood tails. Six-way growth, physical rank mixing,
irreducible Racah behavior, classical separation, algorithm, and speedup
remain open/false.

## Current High-Reasoning Result: Racah Rank/Arithmetic/Alignment Split (2026-08-13)

Files:

- `self_dual_wreath_parity_racah_rank_residual_decomposition.py`
- `research/representation/self_dual_wreath_parity_racah_rank_residual_decomposition.json`
- `tests/test_self_dual_wreath_parity_racah_rank_residual_decomposition.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-RANK-RESIDUAL-DECOMPOSITION`

The coefficient-axis convention is now settled rather than inferred from a
tetrahedron drawing. The implemented physical order is

```text
(alpha,beta,gamma,mu,nu,lambda)=(gk,ghk,hk,g,h,k).
```

Its fusion triples are `(alpha,beta,mu)`, `(mu,gamma,lambda)`,
`(beta,gamma,nu)`, and `(alpha,nu,lambda)`. Every positive exact likelihood
entry through the exhaustive `S_3/S_4` controls obeys those four support
conditions. The tempting tetrahedral-dual mapping
`(h,k,g,hk,gk,ghk)` is wrong for these array axes: it assigns positive
likelihood to forbidden blocks (20 violations at `S_3`, 264 at `S_4`, and
3076 in the separate `S_5` audit). Do not reintroduce that mapping.

For each syndrome orientation, the positive projector amplitude is exactly

```text
A_y=||R_(mu,nu)||_HS^2/(d_mu d_nu).
```

Writing

```text
l_y=g(alpha,beta,mu)g(mu,gamma,lambda),
r_y=g(beta,gamma,nu)g(alpha,nu,lambda),
M_y=sum_eta g(alpha,beta,eta)g(eta,gamma,lambda),
H_y=l_y r_y/(M_y d_mu d_nu),
E_y=A_y-H_y,
```

gives the exact split into the Haar block-rank mean `H`, deterministic
non-Haar Racah arithmetic `E`, and their centered alignment. For
`N(v)^2=8 sum_y(v_y-mean(v))^2`,

```text
N(A)^2=N(H)^2+N(E)^2+16<CH,CE>,
|N(H)-N(E)|<=N(A)<=N(H)+N(E).
```

This kills rank-profile reasoning in both directions. The all-dimension-three
`S_4` control has `N(A)^2=0` but
`N(H)^2=N(E)^2=0.00137174211` and centered cosine `-1`: deterministic Racah
arithmetic exactly cancels the nonuniform Haar rank profile. An `S_5`
dimension-five control instead has residual energy `0.00314153086` versus
rank-profile energy `0.00002844444`, so a nearly flat rank profile does not
imply a flat natural channel. Two additional `S_5` controls have material
contributions from both terms.

The real-Haar block variance

```text
2lr(M-l)(M-r)/[M^2(M-1)(M+2)]
```

is recorded only as a null benchmark. There is no theorem that natural
symmetric-group recoupling matrices are Haar. The next hard task is to bound
the source-weighted relative rank term `N(H)/T0`, the deterministic arithmetic
term `N(E)/T0`, and their alignment on the canonical high-dimensional physical
sector. For decoupling, upper bounds on both component norms suffice. For
survival, one must additionally prevent cancellation. No canonical mixing or
survival result, algorithm, classical separation, or speedup is claimed.

Seven focused tests pass. The generated report has zero control failures,
maximum orientation-fiber amplitude residual `8.33e-17`, and maximum variance
decomposition residual `1.74e-18`. All canonical and algorithmic gates remain
false.

## Current High-Reasoning Result: Racah Toric Obstruction (2026-08-13)

Files:

- `self_dual_wreath_parity_racah_toric_obstruction.py`
- `research/representation/self_dual_wreath_parity_racah_toric_obstruction.json`
- `tests/test_self_dual_wreath_parity_racah_toric_obstruction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-TORIC-OBSTRUCTION`

Young-diagram transpose is sign tensoring, so every Kronecker coefficient
depends on three orientation bits only through their XOR:

```text
g(a^u,b^v,c^w)=g_(u xor v xor w)(a,b,c).
```

Applying this to the Haar rank benchmark gives the exact factorization

```text
H_(g,h,k)=a_g b_(g xor k)c_h d_(h xor k)/(M_k d_mu d_nu).
```

Consequently every normalized rank-profile channel is a three-node Markov
model `G--K--H`: `G` and `H` are conditionally independent given `K`. Both
conditional `2x2` minors vanish exactly, as does the even-versus-odd cube
binomial (the three-factor log-linear interaction). This is an all-`n`
algebraic restriction, not a finite numerical pattern. The transpose-XOR law
was exhaustively checked through `S_5` with zero mismatches.

Natural Racah arithmetic can escape this toric variety. The exact positive
`S_5` orbit tuple `(1,2,1,2,2,2)` has amplitudes

```text
(1/64,1/64,1/64,9/1600,1/64,9/1600,1/14400,1/64).
```

Its conditional minors are exactly `-7/28800` and `17/80000`, its cube defect
is `-61/1024000000`, and its normalized `I(G;H|K)` is
`0.204898071955...` bits. The matching rank benchmark has both minors, cube
defect, and conditional mutual information exactly zero. This is a strict,
all-positive certificate that deterministic non-Haar symmetric-group `6j`
arithmetic creates genuine tetrahedral dependence erased by Haar rank
averaging.

This is still finite and low-dimensional. The next valid target is an
asymptotic positive-physical-mass lower bound for one toric minor or conditional
mutual information on canonical labels, or a theorem that it vanishes. The
same statistic must then be tested under matched classical word-map sampling,
explicit representation access, and coherent coset access. Measured-label CMI
alone is not a coherent decoder or complexity separation. Five focused tests
pass; combined with the preceding module, `12 passed`. The exact-character to
signed-projector implementation residual is `1.04e-17`. All asymptotic,
classical-separation, algorithm, and speedup gates remain false.

## Current High-Reasoning Result: Racah Information Projection (2026-08-13)

Files:

- `self_dual_wreath_parity_racah_information_projection.py`
- `research/representation/self_dual_wreath_parity_racah_information_projection.json`
- `tests/test_self_dual_wreath_parity_racah_information_projection.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-INFORMATION-PROJECTION`

The rank/arithmetic amplitude split can cancel, so this module replaces it
with a positive information-geometric split. Let `P_O(g,h,k)` be the natural
syndrome law for a paired base orbit and let `M` be the entire Markov family
`G independent of H conditional on K`. Every rank-profile channel belongs to
`M` by the toric theorem. The information projection is explicit:

```text
Pi_M(P)(g,h,k)=P(g|k)P(h|k)P(k),
min_(Q in M) D(P||Q)=D(P||Pi_M(P))=I_P(G;H|K).
```

Since the uniform law is in `M`, the exact Pythagorean split is

```text
D(P||U3)=I_P(G;H|K)+D(Pi_M(P)||U3).
```

The first nonnegative term is irreducible Racah arithmetic outside every
rank-only model, not merely outside one chosen Haar benchmark. The second is
rank-compatible syndrome bias. For any compatible rank benchmark `R in M`,
`D(P||R)=I_P(G;H|K)+D(Pi_M(P)||R)` as well. This completely removes
rank/arithmetic cancellation from the research target.

Finite physical aggregation over every positive dimension-`>1` paired orbit
tuple gives zero irreducible term at `S_4`. At `S_5`, retained physical mass is
`0.103548611111...`; its adaptive KL contribution is `0.115252621827` bits,
of which `0.002843022070` bits (about `2.4668%`) is irreducible Racah CMI and
`0.112409599756` bits is rank-compatible. The maximum single-orbit CMI is
`0.204898071955` bits. These are finite controls, not scaling evidence.

The next hard theorem is exactly `E_phys I(Y_g;Y_h|Y_k,O)`: prove it vanishes
or lower-bound it on a canonical positive-mass sector. If it survives, compare
its estimation complexity under classical word-map samples, explicit
representation access, and coherent coset access. Six focused tests pass;
maximum KL Pythagorean residual is `1.39e-17`. All asymptotic, coherent-access,
classical-separation, algorithm, and speedup gates remain false.

## Current High-Reasoning Result: Conditional Racah Cumulants (2026-08-13)

Files:

- `self_dual_wreath_parity_racah_conditional_cumulant.py`
- `research/representation/self_dual_wreath_parity_racah_conditional_cumulant.json`
- `tests/test_self_dual_wreath_parity_racah_conditional_cumulant.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-CONDITIONAL-CUMULANT`

For a normalized syndrome channel `p(g,h,k)`, define the two conditional
slice determinants

```text
delta_k=p(0,0,k)p(1,1,k)-p(0,1,k)p(1,0,k).
```

They vanish exactly iff the channel belongs to the rank-compatible Markov
family `G--K--H`. If `r_abc` are the seven nontrivial Walsh coefficients,
equivalently the parity-coset ratios `F_x/F_0`, and `s=(-1)^k`, then

```text
16 delta_k=(1+s r_001)(r_110+s r_111)
             -(r_100+s r_101)(r_010+s r_011).
```

Thus irreducible Racah information is controlled by two explicit quadratic
cumulants, not by seven unrelated linear modes. If `q=Pi_M(p)`, then

```text
p(g,h,k)-q(g,h,k)=(-1)^(g+h) delta_k/P(K=k),
TV(p,q)=2 sum_k |delta_k|/P(K=k),
chi2(p||q)=sum_k delta_k^2 P(K=k)/
  [P(G=0,k)P(G=1,k)P(H=0,k)P(H=1,k)].
```

Together with `D_bits(p||q)=I(G;H|K)`, these give exact proof interfaces and
the two-sided bounds `2TV^2/ln2 <= CMI <= log2(1+chi2)`. They also show why
raw determinant decay is insufficient: lower tails of all conditional
marginals must be controlled.

The even/odd cube binomial is strictly weaker. A positive exact rational
eight-channel counterexample has zero cube defect but two nonzero conditional
minors and positive CMI. Do not use the cube identity as a substitute for
Markov control. Six focused tests pass; maximum Walsh/determinant residual is
`3.47e-18`. The next asymptotic target is both quadratic cumulants plus their
conditional marginal denominators on physical mass. All asymptotic,
coherent-access, classical-separation, algorithm, and speedup gates remain
false.

## Current High-Reasoning Result: Product-Plancherel Rank Mixing (2026-08-13)

Files:

- `self_dual_wreath_parity_rank_profile_plancherel_mixing.py`
- `research/representation/self_dual_wreath_parity_rank_profile_plancherel_mixing.json`
- `tests/test_self_dual_wreath_parity_rank_profile_plancherel_mixing.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PLANCHEREL-MIXING`

For `m` independent Plancherel irreps, the normalized tensor-multiplicity
density

```text
Y_m=n! <chi_1...chi_(m-1),chi_m>/product_i d_i
```

has exact mean one and variance
`sum_(C!=e)|C|^(2-m)`. Its sign-twist difference has exact second moment
`4 sum_(C odd)|C|^(2-m)`. These identities follow from column orthogonality
and were checked exactly for tensor orders three and four through `S_5`.

After cancelling one common dimension factor, every Haar rank-profile
amplitude has the exact density factorization

```text
R_(g,h,k)=Y1_g Y2_(g xor k) Y3_h Y4_(h xor k)/Z_k,
```

where the four `Y` pairs are three-character fusion densities and the `Z`
pair is a four-character total-multiplicity density. Put
`V_n=sum_(C!=e)|C|^-1` and `W_n=sum_(C!=e)|C|^-2`. Under six independent
Plancherel labels, all eight `Y` variables and two `Z` variables are within
`epsilon` of one except with probability at most
`(8V_n+2W_n)/epsilon^2`. On that event the normalized eight-channel rank law
is uniformly close to fair. On the complement its chi-square is at most seven.
Taking `epsilon=(8V_n+2W_n)^(1/4)`, with `W_n<=V_n=o(1)`, proves

```text
E_(Plancherel^6) chi2(P_rank||U3) -> 0,
```

and therefore expected rank-profile TV and KL also vanish. Absent
total-multiplicity sectors are assigned uniform reference channels; they are
outside the good event and do not change the proof.

This closes multiplicity geometry only under the independent product
reference. The physical six-label law reweights by a correlated tetrahedral
likelihood that is not known to be uniformly integrable on the canonical
trim. Non-Haar Racah CMI is also untouched. Six focused tests pass; maximum
density-factorization residual is `3.47e-18`. The next hard gate is a
change-of-measure theorem transferring rank mixing to physical mass, followed
by the two conditional Racah cumulants. All physical, adaptive, algorithm,
classical-separation, and speedup gates remain false.

## Current High-Reasoning Result: Signed Tetrahedral Projector Reduction (2026-08-13)

Files:

- `self_dual_wreath_parity_projector_tetrahedral_reduction.py`
- `research/representation/self_dual_wreath_parity_projector_tetrahedral_reduction.json`
- `tests/test_self_dual_wreath_parity_projector_tetrahedral_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-TETRAHEDRAL-REDUCTION`

For six `S_n` irreps in the physical coefficient-axis order
`(gk,ghk,hk,g,h,k)`, the three input variables act diagonally on the
overlapping factor sets `(1,2,4)`, `(2,3,5)`, and `(1,2,3,6)`. If `P_a^+`
and `P_a^-` are the trivial and sign isotypic
projectors of one such action and `J_a(x)=P_a^++(-1)^xP_a^-`, then the exact
parity-coset partition function is

```text
F_x=(n!/2)^3 Tr(J_g(x_g)J_h(x_h)J_k(x_k))/product_i d_i.
```

This is the cancellation-preserving representation-theoretic normal form
missing from the projected class-kernel module. It identifies each face or
opposite-complement energy as an `L2` average of a signed three-projector
angle, equivalently a tetrahedral `6j` contraction.

On the fully transpose-paired sector, the six coarse Plancherel factors cancel
the squared partition-function normalization tuple by tuple:

```text
Q(O_1,...,O_6) F_x(O_1,...,O_6)^2
  = Tr(J_g(x_g)J_h(x_h)J_k(x_k))^2.
```

The canonical paired-sector target is therefore an unweighted sum of squared
signed `6j`-type traces. At `S_5`, retaining only the two nonself orbits of
dimensions four and five gives face energy `0.031116743827...` and opposite
energy `0.017794521604...`; all 64 orbit tuples have nonzero traces in both
representative sectors. `S_4` is exactly zero after the analogous trim, so
neither finite behavior is extrapolated.

The same theorem kills rank-only estimates. If all six dimensions exceed
`D`, each signed projector support has normalized rank at most `2/D^2`.
At the canonical `D*=sqrt(n!)/(p(n)log2(n!))`, the resulting seven-sector
energy bound grows rather than decays; its `n=100` log2 value is
`2244.0324`. Even the exact full-Plancherel expected trivial-plus-sign support
fraction, `2/n!`, supplies only marginal rank information and misses two
factorial powers in the unnormalized partition function.

Seven focused tests pass. They validate Young-matrix characters, orthogonal
trivial/sign projectors, all eight `S_3` parity cosets, the four-factor rank
bound, the exact `2/n!` Plancherel identity through `S_5`, the existing array
axis convention, and tuplewise outer-weight cancellation. The next valid
analytic target is an `L2` relative-angle estimate at `o((n!)^-3)` for one
face and one opposite-complement signed overlap. Projector ranks, dimensions,
marginal MP/Plancherel laws, and pointwise character triangle bounds are now
explicitly forbidden substitutes. Canonical decay/survival, adaptive
information, classical separation, algorithm, and speedup gates remain false.

## Current High-Reasoning Result: Adaptive Syndrome Is Positive Channel Variance (2026-08-13)

Files:

- `self_dual_wreath_parity_projector_orbit_variance.py`
- `research/representation/self_dual_wreath_parity_projector_orbit_variance.json`
- `tests/test_self_dual_wreath_parity_projector_orbit_variance.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-ORBIT-VARIANCE`

For every fully transpose-paired coarse orbit tuple, define

```text
A_y=Tr(P_g^(y_g) P_h^(y_h) P_k^(y_k)), y in F_2^3.
```

These traces are nonnegative here for a representation-specific reason, not
because arbitrary triple projection traces are positive: each `A_y` is
`product_i(d_i)/(n!)^3` times one physical oriented likelihood. The signed
projector traces are their Walsh transform. Consequently

```text
P(Y=y|O)=A_y/sum_z A_z,
sum_(x!=0) Q(O)F_x(O)^2=8 sum_y(A_y-mean(A))^2,
chi2(P_(Y|O)||U3)=8 sum_y(A_y/sum_z A_z-1/8)^2.
```

Thus the cancellation target is equivalently equidistribution of eight
positive tetrahedral channels. This formulation is stronger and safer than
trying to bound the signed sums term by term.

The module also gives a decisive proof-strategy falsifier. On four coordinate
atoms indexed by the even-parity subset of `F_2^3`, the six binary projectors
all have rank two and every cross-coordinate pair intersection has trace one,
exactly matching independent fair bits. Nevertheless the eight triple traces
are supported only on even parity, the `(1,1,1)` Walsh mode survives, and the
conditional chi-square is exactly one. Therefore marginal ranks, pairwise
angles, and all pairwise measured-label decoupling cannot prove the needed
tetrahedral mixing. A genuine three-projector cumulant/`6j` estimate is
mandatory.

Five focused tests for this module and seven for its signed-projector
predecessor pass together (`12 passed`). Five natural `S_4/S_5` orbit controls
obey positivity and both Parseval identities; four have positive finite
chi-square. Those controls are not asymptotic evidence. Keep canonical
equidistribution/variance, survival, classical separation, algorithm, and
speedup false.

## Current High-Reasoning Result: Disjoint Grid Recoupling Falsifier (2026-08-13)

Files:

- `self_dual_wreath_disjoint_grid_recoupling_falsifier.py`
- `research/representation/self_dual_wreath_disjoint_grid_recoupling_falsifier.json`
- `tests/test_self_dual_wreath_disjoint_grid_recoupling_falsifier.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-DISJOINT-GRID-RECOUPLING-FALSIFIER`

The earlier disjoint-pair waist theorem is an upper bound, not an equality.
A broader `S_6`, four-label screen found 32 strict controls among the first
250. The materialized primary witness is especially clean: target `(6,)`,
first pair `(0,15)`, second pair `(5,6)`, nine occupied membership-grid cells,
and every cell has isotypic multiplicity at most one. Nevertheless,

```text
first core rank = 1
second core rank = 81
best one-waist bound = 1/5
observed product norm = 1/15
observed squared norm = 1/225
```

The margin is more than `10^8` times the declared numerical error budget. A
second crossing on the same grid has bound `1/9` and the same observed norm
`1/15`. This falsifies both exact waist saturation and any formula determined
only by the best waist dimension. It also proves that local
multiplicity-freeness does not scalarize the row/column recoupling network.

Scope is deliberately narrow. `1/15` is a stable finite rational
reconstruction, not yet a symbolic all-`n` formula. Strict contraction helps
rather than hurts conditioning, so this is not an algorithm no-go. The next
high-reasoning task is to derive the exact symmetric-group 9j/grid contraction
with multiplicity indices and then determine its source-weighted asymptotic
norm. Any coherent compiler must retain this recoupling tensor; carrier
dimensions and pairwise angles alone are insufficient. All algorithm,
uniform-gap, compiler, classical-separation, and speedup gates remain false.

Focused plus adjacent validation: 16 tests passed.

## Current High-Reasoning Result: Grid Quantum-Marginal Boundary (2026-08-13)

Files:

- `self_dual_wreath_grid_quantum_marginal_boundary.py`
- `research/representation/self_dual_wreath_grid_quantum_marginal_boundary.json`
- `tests/test_self_dual_wreath_grid_quantum_marginal_boundary.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-GRID-QUANTUM-MARGINAL-BOUNDARY`

The disjoint pair-core product now has a precise representation-theoretic
identity. Row-first and column-first parity-intertwiner bases are two coupling
schemes for the same membership-pattern grid, so `B_row^* B_column` is a
generalized symmetric-group recoupling (`3nj`) block and

`||P_row P_column|| = ||B_row^* B_column||`.

Both materialized `S_6` controls verify the basis/projector norm identity; the
primary recoupling norm is `1/15`. This identifies the object that an exact
formula and coherent compiler must manipulate.

Primary literature:

- Christandl, Sahinoglu, Walter, *Recoupling coefficients and quantum
  entropies*, `https://arxiv.org/abs/1210.0463`.
- Keyl, Werner, *Estimating the spectrum of a density operator*,
  `https://arxiv.org/abs/quant-ph/0102027`.

The first paper connects bounded-row symmetric-group recoupling asymptotics to
quantum-marginal compatibility and explicitly generalizes to `3nj` blocks.
That theorem does **not** directly cover the natural source here. Its
`poly(n)` constants depend on the maximum row count `d`; Weyl's dimension
formula already contributes at most

`(n+d)^(d(d-1)/2)`.

Consequently its log prefactor is `Theta(d^2 log n)`. Constant-distance
spectrum-estimation suppression is only `Theta(n)`. The proof remains
exponentially informative for `d=o(sqrt(n/log n))`, is borderline at
`d=Theta(sqrt(n/log n))`, and loses exponential control at the natural
Plancherel scale `d=Theta(sqrt n)`. At `n=4096`, the recorded Weyl-bound ratio
to the strongest constant-distance suppression is `0.0122` for four rows and
`16.57` for `2 sqrt(n)` rows.

This is a proof-scope audit, not evidence that natural coefficients are large.
The next theorem target is a dimension-uniform or source-weighted Plancherel
recoupling bound, paired with a classification of whether naturally weighted
grid spectra are compatible quantum marginals. A magnitude theorem still
would not provide a coherent `3nj` compiler. All natural-source,
uniform-gap, compiler, algorithm, and speedup gates remain false.

Focused plus adjacent validation: 22 tests passed.

## Current High-Reasoning Result: Dimension-Uniform 6j Certificate (2026-08-13)

Files:

- `self_dual_wreath_recoupling_dimension_certificate.py`
- `research/representation/self_dual_wreath_recoupling_dimension_certificate.json`
- `tests/test_self_dual_wreath_recoupling_dimension_certificate.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-DIMENSION-CERTIFICATE`

The exact tetrahedral Hilbert--Schmidt symmetry from
`arXiv:1210.0463` can be made dimension-uniform by retaining exact swapped
block ranks instead of replacing them by a fixed-row polynomial. For

`R=[alpha beta mu; gamma lambda nu]`

write

```text
g1=g(mu,gamma,lambda), g2=g(alpha,beta,mu),
g3=g(alpha,nu,lambda), g4=g(beta,gamma,nu).
```

Then

```text
||R||_op^2 <= min(
  1,
  (d_mu d_nu)/(d_beta d_lambda) min(g2 g4,g1 g3),
  (d_mu d_nu)/(d_alpha d_gamma) min(g2 g3,g1 g4)).
```

The proof uses only exact tetrahedral symmetry and
`||X||_HS^2<=rank(X)||X||_op^2<=rank(X)` for the two swapped blocks. It has no
row-count assumption. All 51 blocks in the complete finite `S_6` Racah
controls respect the bound; 24 receive a strict upper bound below one. A clean
selected block has actual norm `1/3` and certified bound `5/9`, with exact
squared certificate `25/81`.

This is a local 6j theorem, not a natural-source 3nj theorem. The decisive next
quantity is the joint pressure of Specht-dimension ratios and swapped
Kronecker ranks under the natural Plancherel source, followed by control of the
number and interference of intermediate paths in a full grid. A local norm
certificate does not compile the recoupling transform. All natural-rank,
generalized-grid, compiler, uniform-gap, algorithm, and speedup gates remain
false.

Focused tests: 5 passed. An adjacent pre-existing integration test fails
because `write_complete_racah_control_report` accepts registry arguments but
does not write the result that `experiment_runner` expects. This is mechanical
registry plumbing assigned below, not a failure of the new theorem controls.

## Current High-Reasoning Result: Plancherel 6j Rank-Pressure No-Gos (2026-08-13)

Files:

- `self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.py`
- `self_dual_wreath_physical_recoupling_rank_pressure_no_go.py`
- matching artifacts under `research/representation/` and focused tests

Experiment IDs:

- `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-RANK-PRESSURE-NO-GO`
- `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-RECOUPLING-RANK-PRESSURE-NO-GO`

The dimension-uniform certificate is now closed as a typical-mass tool. Put
`G=n!`, let `q_rho=d_rho^2/G` be a Plancherel atom, `p=p(n)`, and
`V_n=sum_(C!=1)1/|C|`. Atom counting and the exact normalized-Kronecker
variance show that, for six independent Plancherel labels, both raw squared
rank bounds are at least

`G/(4 n^(7/2) p^(7/2))`

except with probability at most `6/n+16V_n`. The lower bound diverges and the
failure probability vanishes.

The stronger theorem handles the actual correlated physical path. If a 6j
block is sampled by sequential projective-measurement trace mass, then

`P(alpha,beta,gamma,mu,nu,lambda)=d_alpha d_beta d_gamma d_lambda ||R_mu,nu||_HS^2/G^3`.

Recoupling unitarity proves every edge marginal is exactly Plancherel and each
of the four local Kronecker triples has density `1+X` relative to three
independent Plancherel labels. On the only bad event, `X < -1/2`, that density
is at most `1/2`; all four lower-tail failures therefore cost at most `8V_n`.
Consequently blocks on which the rank-aware certificate proves contraction
carry physical mass at most `6/n+8V_n=o(1)`. Exact size-biased local controls
pass through `S_7`; the `n=30` finite theorem bound has good-event probability
at least `0.78047` and a raw-bound margin of `2^44.95`.

This does **not** say the true 6j norm is one. It says this upper certificate is
uninformative on typical physical mass. Coherent 3nj interference remains
open. Focused plus adjacent theorem validation: 19 tests passed.

## Current High-Reasoning Result: Plancherel Marginal Compatibility (2026-08-13)

Files:

- `self_dual_wreath_plancherel_marginal_compatibility_no_go.py`
- `research/representation/self_dual_wreath_plancherel_marginal_compatibility_no_go.json`
- `tests/test_self_dual_wreath_plancherel_marginal_compatibility_no_go.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-MARGINAL-COMPATIBILITY-NO-GO`

For normalized row spectra `s(rho)=rho/n`,

`||s(rho)-s(sigma)||_1=|Young(rho) triangle Young(sigma)|/n`.

The Logan--Shepp--Vershik--Kerov limit-shape theorem therefore makes any fixed
number of Plancherel-marginal spectra mutually `o(1)` in `L1`; label
independence is unnecessary. For every probability vector `r`, the diagonal
state `sum_i r_i |iii><iii|` has spectrum `r` on
`A,B,C,AB,BC,ABC`. Combining this witness with the physical six-edge
Plancherel marginal theorem proves that the physical six-spectrum tuple lies
`o(1)` from the tripartite quantum-marginal compatibility set.

Thus a constant incompatibility gap cannot occur on positive physical mass.
This does not bound the shrinking-gap rate: `n D_n^2` may still diverge, and
the published compatible-side lower theorem is fixed-dimensional. Exact-law
two-sample `L1` controls decrease from `0.39236` at `n=4` to `0.22590` at
`n=30`; they are diagnostics, not a rate proof. Thirteen focused plus adjacent
tests passed.

## Current High-Reasoning Result: Recoupling Channel Information (2026-08-13)

Files:

- `self_dual_wreath_recoupling_channel_flatness_boundary.py`
- `research/representation/self_dual_wreath_recoupling_channel_flatness_boundary.json`
- `tests/test_self_dual_wreath_recoupling_channel_flatness_boundary.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-CHANNEL-FLATNESS-BOUNDARY`

For fixed source/final labels, channel dimensions `L_mu,R_nu`, and total
multiplicity `M`, the two sequential intermediate-label measurements obey

```text
p(mu,nu)=||R_(nu,mu)||_HS^2/M,
q(mu,nu)=p(mu)p(nu)=L_mu R_nu/M^2,
p/q=M||R_(nu,mu)||_HS^2/(L_mu R_nu).
```

Hence `D_KL(p||q)` is exactly channel mutual information and

`chi^2(p||q)=sum ||R_(nu,mu)||_HS^4/(L_mu R_nu)-1`.

The complete `S_6` controls falsify exact Haar-flat channel mass: four of five
sectors are nonflat, maximum TV is `1/8`, maximum mutual information is
`0.156425` bits, and two sectors assign product mass `1/16` to a physically
forbidden cross channel. These are finite arithmetic correlations, not an
asymptotic signal. The decisive next theorem is the physical
Plancherel/source-weighted fourth moment: prove TV/mutual information vanishes,
or exhibit a uniform positive-mass outlier family and attack it classically.
Eight focused theorem tests passed; the known Racah registry integration test
still fails for the separate writer-upsert defect described above.

## Current High-Reasoning Result: Haar Gap And Tetrahedral Synergy (2026-08-13)

Files:

- `self_dual_wreath_recoupling_haar_gap_reduction.py`
- `self_dual_wreath_physical_recoupling_tetrahedral_synergy.py`
- matching artifacts under `research/representation/` and focused tests

Experiment IDs:

- `EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-HAAR-GAP-REDUCTION`
- `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-RECOUPLING-TETRAHEDRAL-SYNERGY`

For Haar orthogonal recoupling with total multiplicity `M` and `a,b` channel
blocks, the exact benchmark is

`E chi^2=2(a-1)(b-1)/((M-1)(M+2))`.

Under physical source/final trace mass, the multiplicity density relative to
four independent Plancherel labels has exact chi-square
`V4_n=sum_(C!=1)|C|^-2`. Outside physical mass `4/n+2V4_n`, the total
multiplicity is at least `n!/(2n^2p(n)^2)`. Thus the orthogonal-Haar channel
benchmark is at most `8n^4p(n)^6/(n!)^2`; any nonvanishing measured-label
signal on positive mass requires factorial-scale enhancement over Haar. This
is a conditional reduction, not a proof that natural Racah blocks are Haar.

The physical six labels have stronger exact low-order structure: all 15 label
pairs are independent Plancherel, while each of the four fusion-face triples
has chi-square `V_n=sum_(C!=1)|C|^-1=o(1)` from product Plancherel. Therefore
one-edge, pairwise, and one-face classical label statistics are dead. Any
surviving signal must be high-order tetrahedral synergy, final/source-
conditioned channel information, or coherent multiplicity phase. At `n=50`,
the face TV upper bound is `0.0145263` and the face information bound is
`0.0012172` bits. These theorems do not control the full six-label law or
coherent phases. The affected focused chains passed 12 and 13 tests.

## Current High-Reasoning Result: Final-Label Necessity For Measured Channels (2026-08-13)

Files:

- `self_dual_wreath_source_conditioned_channel_decoupling.py`
- `research/representation/self_dual_wreath_source_conditioned_channel_decoupling.json`
- `tests/test_self_dual_wreath_source_conditioned_channel_decoupling.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-SOURCE-CONDITIONED-CHANNEL-DECOUPLING`

Fix independent Plancherel source labels `alpha,beta,gamma`, measure the two
overlapping intermediate channels `mu,nu`, and sum out the final Racah label.
Relative to independent Plancherel outputs, the exact conditional likelihood
is a five-character sum. Its source-averaged chi-square is

```text
V5_n = 2 V_n + E_Pl[T_lambda^2],
T_lambda = sum_(C!=1) r_lambda(C)^2,
V_n = sum_(C!=1) 1/|C|.
```

The fourth moment has the exact finite-group convolution identity

`E_Pl[T_lambda^2]=sum_(A,B!=1)||u_A*u_B||_2^2`.

Young contraction bounds it by
`H_n^2`, where `H_n=sum_(C!=1)|C|^-1/2`. A moved-support decomposition,
`z_rho<=m^(m/2)`, and at most `2^m` fixed-point-free cycle types prove
`H_n=o(1)`. Explicitly, for `n>=237`, set
`a_n=2(2/n)^(1/4)` and `b_n=2(2e^2/n)^(1/4)`; then

`H_n <= a_n^2/(1-a_n) + b_n^(floor(n/2)+1)/(1-b_n)`.

Therefore `V5_n<=3H_n^2=o(1)`: the joint physical law of
`alpha,beta,gamma,mu,nu` tends in TV to five independent Plancherel labels,
and average source-conditioned channel mutual information vanishes. Direct
five-character enumeration at `S_3,S_4`, direct class convolution through
`S_6`, and exact character controls through `S_14` verify every identity.
The focused/adjacent chain passes 20 tests before the added direct controls.

This is the sharp scope boundary: it sums out `lambda`. The finite `S_6`
nonflat sectors condition on `lambda`, so they do not contradict the theorem.
The next high-judgment target is the conditional information
`I(mu:nu | alpha,beta,gamma,lambda)`, equivalently the genuinely tetrahedral
six-label interaction. Prove its physical expectation vanishes, or construct
a positive-mass family where revealing `lambda` unlocks nonvanishing
correlation. Then attack any survivor with classical character/Kronecker
sampling before treating it as quantum leverage. Coherent multiplicity phases
remain a separate open route. Keep full-six-label, final-conditioned,
coherent-phase, algorithm, and speedup gates false.

## Current High-Reasoning Result: Tetrahedral Chi-Square Tail No-Go (2026-08-13)

Files:

- `self_dual_wreath_tetrahedral_chi_square_tail_no_go.py`
- `research/representation/self_dual_wreath_tetrahedral_chi_square_tail_no_go.json`
- `tests/test_self_dual_wreath_tetrahedral_chi_square_tail_no_go.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-CHI-SQUARE-TAIL-NO-GO`

The full physical six-label chi-square has an exact classical dual. For three
independent uniform permutations, form
`W=(g,h,k,gk,hk,ghk)`. The physical irrep-label chi-square from
`Plancherel^6` equals the chi-square of the joint six cycle types from the
product of their marginals. If `N_C` counts six-class signatures, the common
second moment is `sum_C N_C^2/product_i|C_i|`.

There are exactly 15 nonzero identity/nonidentity support masks for `n>=3`.
Writing `V=sum_(C!=1)|C|^-1`, `V4=sum_(C!=1)|C|^-2`, and
`M2=E_Pl[T_lambda^2]`, the exact decomposition is

`chi^2=4V+6M2-3V4+Z6`,

where `Z6` is the fully nonidentity six-word core. All displayed lower-support
terms vanish by the preceding convolution theorem.

Raw chi-square nevertheless cannot vanish. Restrict all six irrep labels to
trivial/sign bits. Eight of 64 patterns satisfy the three exact parity
equations

```text
a+b+mu = b+c+nu = a+b+c+lambda = 0 mod 2.
```

They have likelihood `(n!)^3`; the other 56 have likelihood zero. This tiny
sector contributes exactly `8-16/(n!)^3+64/(n!)^6` to chi-square, tending to
eight, while its physical mass is only `8/(n!)^3`. The entire event that any
of six labels is one-dimensional has physical mass at most `12/n!`.

Therefore untrimmed chi-square and maximum likelihood are rejected as
positive-mass research metrics. Exact class signatures through `S_5`, direct
physical character transforms through `S_5`, and the adjacent theorem chain
pass 22 tests. This does not prove typical-mass TV/KL decay or survival.

## Current High-Reasoning Result: Near-Maximal Dimension Information Trim (2026-08-13)

Files:

- `self_dual_wreath_tetrahedral_dimension_trim.py`
- `research/representation/self_dual_wreath_tetrahedral_dimension_trim.json`
- `tests/test_self_dual_wreath_tetrahedral_dimension_trim.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-DIMENSION-TRIM`

The parity-tail repair extends to all low-dimensional irreps. For either the
physical law or `Plancherel^6`, the event that any label dimension is at most
`D` has mass at most `delta_D=6p(n)D^2/n!`. Its TV contribution is at most
`delta_D`. Since every tuple has likelihood at most `(n!)^6`, its positive KL
contribution is at most `6 delta_D log2(n!)`.

With

`D_n=floor(sqrt(n!)/(p(n)log2(n!)))`,

the removed TV is at most `6/[p(n)log2(n!)^2]` and removed positive KL is at
most `36/[p(n)log2(n!)]`; both vanish. At `n=50`, `log2 D_n=81.7214`, removed
mass is at most `6.403e-10`, and removed positive KL is at most
`8.229e-7` bits. Thus every polynomial- and subexponential-dimensional tail
is irrelevant: any genuine measured signal must live on a retained
near-maximal-dimensional bulk. Five focused tests pass. The theorem is
information-theoretic and does not compile a coherent trim.

## Current High-Reasoning Result: Projected Tetrahedral Word Map (2026-08-13)

Files:

- `self_dual_wreath_projected_tetrahedral_word_map.py`
- `research/representation/self_dual_wreath_projected_tetrahedral_word_map.json`
- `tests/test_self_dual_wreath_projected_tetrahedral_word_map.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PROJECTED-TETRAHEDRAL-WORD-MAP`

For a retained irrep set `R`, define

```text
m_R(x)=|G|^-1 sum_(rho in R) d_rho chi_rho(x),
K_R(x,y)=|G|^-1 sum_(rho in R) chi_rho(x)chi_rho(y),
q_R=|G|^-1 sum_(rho in R)d_rho^2.
```

The retained sub-probability chi-square is exactly

```text
C_R = sum_(t,u in G^3) product_i K_R(W_i(t),W_i(u))
      -2 sum_(t in G^3) product_i m_R(W_i(t)) + q_R^6,
W(t)=(g,h,k,gk,hk,ghk).
```

Moreover `TV_R<=(q_R^3/2)sqrt(C_R)`. This converts the retained Racah problem
into one six-fold high-dimensional central Fourier projection of a classical
word map. Exact projected-kernel controls after several trims pass through
`S_4`; label-space controls pass through `S_5`. At `S_5`, deleting only the
one-dimensional irreps drops chi-square from `15.5459` to `0.92637`, but
retained unnormalized TV remains `0.35092`. No asymptotic conclusion follows.

The literature audit matters. Féray--Sniady is strongest for short
permutations; the six word values are typically long. Lifshitz--Marmor gives
powerful level/norm and normal-set mixing bounds, but not this correlated
six-edge high-level projection. Benaych-Georges controls fixed small cycles of
one word, and Hanany--Puder controls stable class functions; the canonical
dimension trim removes precisely those low-level Fourier modes. The next
hard theorem is therefore explicit: prove `C_R=o(1)` for
`R={rho:d_rho>D_n}`, or identify retained modes and signatures with
nonvanishing direct L1/positive-KL mass. A nonzero projected chi-square alone
is insufficient because a second high-dimensional L2 tail may exist.
Classical word-map sampling and character/Kronecker baselines are mandatory
for any survivor. Coherent multiplicity phases remain outside this reduction.
Six focused tests pass. All asymptotic-survival, classical-separation,
compiler, algorithm, and speedup gates remain false.

## Current High-Reasoning Result: Sign-Orbit Syndrome Reduction (2026-08-13)

Files:

- `self_dual_wreath_sign_orbit_syndrome_reduction.py`
- `research/representation/self_dual_wreath_sign_orbit_syndrome_reduction.json`
- `tests/test_self_dual_wreath_sign_orbit_syndrome_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-SYNDROME-REDUCTION`

Deleting the trivial and sign representations does not delete the sign action:
`V_(rho^T)=V_rho tensor sign` for every Young diagram. On a six-tuple of
non-self-conjugate sign orbits, encode transpose choices by
`z=(z_alpha,z_beta,z_gamma,z_mu,z_nu,z_lambda)`. The tetrahedral word tuple
maps input permutation parities `x=(x_g,x_h,x_k)` to

```text
A x=(x_g+x_k,x_g+x_h+x_k,x_h+x_k,x_g,x_h,x_k).
```

The exact 64-point orientation likelihood depends only on the three-bit
syndrome

```text
A^T z=(z_alpha+z_beta+z_mu,
       z_beta+z_gamma+z_nu,
       z_alpha+z_beta+z_gamma+z_lambda).
```

Equivalently its Walsh support is the eight-element image of `A`, and each
syndrome has exactly eight transpose choices. On every retained nonself sector,
the product Plancherel orientation is uniform and KL splits exactly as

`D(P||Q)=D(P_orbit||Q_orbit)+E_P D(P_syndrome||Uniform(F_2^3))`.

Thus sign-orbit orientation carries at most three measured-label bits. It is a
classically readable statistic once the six partitions are measured. It is not
a coherent decoder or an algorithm.

The theorem also kills a tempting no-go shortcut. The repeated `S_4` standard
sign pair has orientation KL zero, but the repeated `S_5` `(3,2)/(2,2,1)` pair
has exact finite conditional TV `8/17` and KL about `0.9471` bits after all
one-dimensional labels are excluded. Therefore “remove sign labels and all
parity disappears” is false. This finite row is not asymptotic evidence: the
canonical near-maximal-dimension sector and positive retained mass remain
uncontrolled.

The KL chain residual is below `9e-16` on all live controls and six focused
tests pass. Finite self-conjugate Plancherel mass is recorded through `n=50`
without claiming a limit. Borodin--Okounkov--Olshanski
`arXiv:math/9905032` supplies Airy edge asymptotics for Plancherel diagrams,
but the audited statement does not directly provide the joint opposite-edge
anti-concentration needed to conclude `P(lambda=lambda^T)->0`; keep that gate
false unless a precise primary theorem or proof is added.

Next hard target: bound the three nonlocal parity-sector character moments on
the canonical dimension trim, or exhibit a positive-mass sign-orbit family.
Any survivor must then be compared with a classical six-partition syndrome
calculation under the same access model. Keep self-conjugate-mass decay,
canonical syndrome decay/survival, coherent signal, classical separation,
algorithm, and speedup gates false.

## Current High-Reasoning Result: Unconditional Sign Syndrome Decouples (2026-08-13)

Files:

- `self_dual_wreath_sign_syndrome_unconditional_decoupling.py`
- `research/representation/self_dual_wreath_sign_syndrome_unconditional_decoupling.json`
- `tests/test_self_dual_wreath_sign_syndrome_unconditional_decoupling.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-SIGN-SYNDROME-UNCONDITIONAL-DECOUPLING`

The raw three-bit sign syndrome is now proved asymptotically useless without
assuming that self-conjugate Plancherel mass vanishes. Choose an antisymmetric
section `eta(lambda^T)=-eta(lambda)` and set `eta=0` on self-conjugate
partitions; equivalently attach an independent fair orientation bit there.

The seven nonzero syndrome Walsh frequencies have exact tetrahedral geometry:
four are fusion faces and three are the four-edge complements of opposite
pairs. If `V_n` is the exact face chi-square and `V5_n` is the five-label
chi-square from the source-conditioned theorem, then

```text
chi2(P_Y || Uniform(F_2^3)) <= 4 V_n + 3 V5_n,
TV(P_Y,Uniform) <= 0.5 sqrt(4 V_n + 3 V5_n),
KL_bits <= log2(1+4 V_n+3 V5_n).
```

All bounds tend to zero. Tetrahedral symmetry transfers the representative
five-label estimate to all three opposite-pair complements. The fair fixed-
orbit lift means no self-conjugate-mass assumption or conditioning is used.
At `n=50` the analytic upper bounds are TV `0.05559` and KL `0.01773` bits;
these are conservative asymptotic bounds, not measured residual signals.

Exact fair-lifted syndrome distributions through `S_5` pass five focused
tests. The raw `S_5` syndrome TV is `0.07079`, much smaller than the `8/17`
conditional TV in one high-dimensional sign pair. This is not a contradiction:
conditional biases cancel across base orbits.

Let `O` be the six unoriented sign-orbit identities. The exact identity

`E_O D(P(Y|O)||U)=I_P(O:Y)+D(P_Y||U)`

shows what remains. Since the last term vanishes, any surviving orientation
information must be orbit-adaptive mutual information `I(O:Y)`. The next hard
target is to bound this quantity on the canonical high-dimensional trim or
construct a positive-mass orbit family. It remains a deterministic statistic
of measured labels and needs a same-access classical baseline. Keep
orbit-adaptive decay/survival, base-orbit product law, coherent signal,
classical separation, algorithm, and speedup gates false.

## Current High-Reasoning Result: Lossless Sign-Orbit KL Chain (2026-08-13)

Files:

- `self_dual_wreath_sign_orbit_kl_chain_reduction.py`
- `research/representation/self_dual_wreath_sign_orbit_kl_chain_reduction.json`
- `tests/test_self_dual_wreath_sign_orbit_kl_chain_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-KL-CHAIN-REDUCTION`

The full measured six-label information problem now has an exact lossless
two-term decomposition. Append fair bits on self-conjugate partitions, let
`O` be the six unordered transpose-orbit labels, let `Z in F_2^6` be the
orientation bits, and let `Y=A^T Z in F_2^3`. Product Plancherel satisfies
`Q(O,Z)=Q_O(O)/64`, while the physical likelihood is constant on every
eight-point kernel fiber of `A^T`. Therefore

```text
D(P_six || Plancherel^6)
 = D(P_O || Q_O) + E_O D(P(Y|O) || Uniform(F_2^3)).
```

No information is lost: the three kernel orientation bits are exactly
ancillary. Also

`E_O D(P(Y|O)||U)=I_P(O:Y)+D(P_Y||U)`.

The preceding theorem makes `D(P_Y||U)=o(1)`. Thus every asymptotic measured
survivor is now localized to one of two explicit quantities:

1. dependence among the six **unoriented sign-orbit labels**;
2. orbit-adaptive mutual information `I(O:Y)`.

Exact controls through `S_5` pass five tests with maximum KL-chain residual
`3.4e-15`. At `S_5`, full KL `1.13255` bits splits into base-orbit KL
`0.50667` and conditional syndrome KL `0.62587`; the latter splits into raw
syndrome KL `0.04062` and orbit-syndrome MI `0.58526`. These finite values are
diagnostics, not asymptotic evidence.

The next hard theorem should separately project the canonical high-dimensional
word map onto (a) transpose-even central functions for base-orbit KL and (b)
the seven sign-twisted kernels for `I(O:Y)`. Prove both vanish or identify a
positive-mass retained mode. Both are classical functions of measured Young
diagrams, so any survivor still needs same-access dequantization. Keep both
asymptotic term gates, coherent signal, classical separation, algorithm, and
speedup false.

## Current High-Reasoning Result: Base Orbits Are Coarse A_n Fourier Data (2026-08-13)

Files:

- `self_dual_wreath_alternating_base_orbit_reduction.py`
- `research/representation/self_dual_wreath_alternating_base_orbit_reduction.json`
- `tests/test_self_dual_wreath_alternating_base_orbit_reduction.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BASE-ORBIT-REDUCTION`

The base sign-orbit term is now a standard group object. For every nonself
pair,

`(r_lambda(w)+r_(lambda^T)(w))/2 = 1[w in A_n] r_lambda(w)`.

A self-conjugate character already vanishes on odd permutations. In the six
tetrahedral words, all values are even exactly when the independent inputs
`g,h,k` lie in `A_n`. Hence the orientation-averaged likelihood is

`L_O=sum_(g,h,k in A_n) product_i r_(O_i)(W_i(g,h,k))`.

The orbit labels and weights are exactly coarse `A_n` weak-Fourier labels:
nonself `S_n` pairs restrict to one `A_n` irrep, while each self-conjugate
irrep splits into two dimension-`d/2` irreps that are merged. Their combined
`A_n` Plancherel mass equals the original `S_n` orbit mass. Therefore the
base KL in the preceding chain is exactly coarse alternating-group
tetrahedral KL.

Direct even-permutation word-map transforms agree with aggregated `S_n`
likelihoods through `S_5` (maximum residual `1.14e-12`); five focused tests
pass. At `S_5`, this term is `0.50667` bits, `44.74%` of full finite KL. No
asymptotic conclusion follows.

The merged trivial/sign orbit becomes the single trivial `A_n` label and
still gives physical all-six mass `|A_n|^-3` with likelihood `|A_n|^3`.
Thus raw coarse `A_n` chi-square still has a rare tail; apply the canonical
dimension trim and direct L1/KL metrics.

Next hard target: prove dimension-trimmed six-word mixing for this coarse
`A_n` law, or find positive retained mass. The exact classical dual samples
three uniform even permutations and their six word values, so any survivor
must be evaluated under the natural-input access model before it has quantum
value. Keep coarse-`A_n` decay/survival, classical separation, coherent
signal, algorithm, and speedup gates false.

## Current High-Reasoning Result: Adaptive Syndrome Is a Twisted A_n Channel (2026-08-13)

Files:

- `self_dual_wreath_alternating_parity_coset_channel.py`
- `research/representation/self_dual_wreath_alternating_parity_coset_channel.json`
- `tests/test_self_dual_wreath_alternating_parity_coset_channel.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-PARITY-COSET-CHANNEL`

The remaining orbit-adaptive syndrome term is now an exact finite-group
partition-function problem.  For a six-tuple of unoriented sign orbits `O`
and input parity `x=(parity(g),parity(h),parity(k))`, define

```text
F_x(O)=sum_(input parity=x) product_i r_(O_i)(W_i(g,h,k)).
```

If `z` records the six transpose orientations, then

```text
L_O(z)=sum_x (-1)^(x dot A^T z) F_x(O),
P(Y=y|O)=1/8 [1+sum_(x!=0)(-1)^(x dot y)F_x(O)/F_0(O)].
```

Here `F_0` is exactly the coarse `A_n` tetrahedral likelihood from the base-
orbit theorem.  Consequently the seven conditional-syndrome Walsh
coefficients are the parity-coset ratios `F_x/F_0`, and

```text
E chi2(P(Y|O)||U_3)
  = sum_O Q_O sum_(x!=0) F_x(O)^2/F_0(O).
```

Choosing an odd coset representative identifies every nonzero sector with an
outer-automorphism-twisted `A_n` word map. Tetrahedral symmetry reduces the
seven sectors to two asymptotic problems: four face twists and three
opposite-complement twists. Exact controls through `S_5` verify the Fourier
reconstruction, probability law, KL-chain identity, and within-type annealed
moment symmetry; five focused tests pass. At `S_5`, the total conditional
chi-square is `0.88270`, with one face contribution `0.15465` and one
opposite-complement contribution `0.08804`. These are finite diagnostics.

This is a reduction, not a mixing theorem. Raw `F_x^2/F_0` moments can be
dominated by low-dimensional base sectors. The next hard task is to define
the canonical dimension-trimmed coarse `A_n` law and prove direct retained
KL/TV decay for both twist types, or exhibit a positive-mass retained
counterfamily. Any survivor is still a classical statistic of measured
partitions and needs a natural-input classical baseline. Keep both trimmed
twist gates, adaptive survival, coherent signal, classical separation,
algorithm, and speedup false.

## Current High-Reasoning Result: Denominator-Free Adaptive Trim Transfer (2026-08-13)

Files:

- `self_dual_wreath_adaptive_syndrome_trim_transfer.py`
- `research/representation/self_dual_wreath_adaptive_syndrome_trim_transfer.json`
- `tests/test_self_dual_wreath_adaptive_syndrome_trim_transfer.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-ADAPTIVE-SYNDROME-TRIM-TRANSFER`

The apparent `F_x/F_0` small-denominator problem is now removed exactly. For
any retained coarse-orbit set `B`, physical weighting by `P_O=Q_OF_0`, Walsh
Parseval, and Cauchy--Schwarz give

```text
E_P[1_B TV(P(Y|O),U_3)] <= (1/2)sqrt(Q(B) S_B),
S_B = sum_(O in B) Q(O) sum_(x!=0) F_x(O)^2.
```

For the dimension trim `B_D`, the existing marginal theorem gives
`P(B_D^c),Q(B_D^c)<=delta_D=6p(n)D^2/n!`, hence

```text
E_P TV(P(Y|O),U_3) <= delta_D+(1/2)sqrt(Q(B_D)S_(B_D)).
```

Entropy continuity transfers this to expected conditional KL and `I(O:Y)`:
if the right side is `epsilon<=7/8`, both are at most
`h_2(epsilon)+epsilon log2(7)`. No likelihood floor is required.

There is also an exact matched-projection identity:

```text
S_B = M_full(B)-M_base(B) = C_full(B)-C_base(B),
```

where `M` is retained likelihood second moment and `C` is retained
subprobability chi-square. Thus adaptive information is precisely the excess
of the full projected `S_n` tetrahedral word-map energy over its coarse `A_n`
base projection. Use the manifestly nonnegative seven-coset sum for analysis,
not numerical subtraction of two potentially large moments.

Seven finite controls pass five focused tests with maximum identity residual
`5.33e-15`. At `S_5`, deleting one-dimensional labels leaves adaptive energy
`0.68460` and retained conditional TV `0.25373`. These are finite diagnostics,
not evidence for either asymptotic decay or survival.

The hard target is now exactly `S_(B_(D_n))=o(1)` for the canonical threshold,
or positive retained direct L1/KL mass. It splits into one face and one
opposite-complement parity-coset energy by tetrahedral symmetry. Even if this
term vanishes, coarse `A_n` base KL remains independently open. Keep all
asymptotic, coherent, classical-separation, algorithm, and speedup gates false.

## Current High-Reasoning Result: Pointwise Character Triangle Route Is Vacuous (2026-08-13)

Files:

- `self_dual_wreath_character_triangle_barrier.py`
- `research/representation/self_dual_wreath_character_triangle_barrier.json`
- `tests/test_self_dual_wreath_character_triangle_barrier.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-CHARACTER-TRIANGLE-BARRIER`

Do not try to close the projected parity-coset target by improving pointwise
character constants and then summing absolute values over input triples. Even
under the unrealistically strong assumption `|chi_lambda(w)|<=1` on every
retained nonidentity word,

```text
|F_x| <= |S_n|^3 D_n^-6.
```

At the continuous canonical threshold
`D*=sqrt(n!)/(p(n)log2(n!))`, this is exactly
`(p(n)log2(n!))^6`, which diverges. The corresponding seven-sector energy
bound is `7(p(n)log2(n!))^12`. Flooring `D*` only weakens the estimate.

Teyssier--Thevenin `arXiv:2411.04347`, Theorem 1.6, bounds ordinary
characters by a positive dimension exponent determined by orbit growth;
their cycle-count corollary and the Lifschitz--Marmor bounds are therefore
weaker than the ideal assumption used in this barrier once triangle
inequality is applied. They remain potentially useful only inside a
cancellation-preserving argument. Five tests pass; at `n=100` the already
idealized energy upper bound has log2 size `441.30`.

This eliminates a proof strategy, not either asymptotic outcome. A viable
proof must preserve cancellation through projected class kernels, exact
Plancherel orthogonality, collision geometry, or a genuinely multilinear norm
estimate before taking absolute values. Keep adaptive decay, survival,
classical separation, algorithm, and speedup false.

## Current High-Reasoning Result: Projected Parity-Coset Collision Kernels (2026-08-13)

Files:

- `self_dual_wreath_projected_parity_coset_kernel.py`
- `research/representation/self_dual_wreath_projected_parity_coset_kernel.json`
- `tests/test_self_dual_wreath_projected_parity_coset_kernel.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-PROJECTED-PARITY-COSET-KERNEL`

The two adaptive-energy targets now have an exact cancellation-preserving
class-kernel form. For a sign-invariant retained irrep set `R`, put

```text
K_R(a,b)=|S_n|^-1 sum_(lambda in R) chi_lambda(a)chi_lambda(b).
```

If two input triples `t,u` lie in the same parity coset `T_x`, corresponding
word signs agree. Therefore each transpose pair contributes identically and
the coarse sign-orbit Plancherel sum reconstructs the ordinary `S_n` kernel:

```text
S_x(R)=sum_(t,u in T_x) product_i K_R(W_i(t),W_i(u)).
```

Writing `N_x(C)` for parity-restricted six-word class-signature counts gives

```text
S_x(R)=sum_(C,D)N_x(C)N_x(D)product_i K_R(C_i,D_i).
```

For all irreps, column orthogonality diagonalizes the kernel and yields
`S_x(all)=sum_C N_x(C)^2/product_i|C_i|`. These are positive Gram energies
despite signed projected kernels. Tetrahedral symmetry again leaves one face
and one opposite-complement contraction.

Six exact projected controls through `S_4` pass five focused tests. Maximum
direct/kernel residual is `8.89e-16`; full-kernel collision formulas agree
exactly. The zero energies in the strongest tiny `S_4` trim are finite rank
annihilations and carry no asymptotic meaning.

The next valid analytic task is a canonical-`R_n` bound on one representative
of each type using collision switching, projected-kernel operator estimates,
trace moments, or another multilinear orthogonality argument before absolute
values. Pointwise triangle bounds are forbidden by the preceding theorem.
Keep canonical decay/survival, classical separation, algorithm, and speedup
false.

## Current High-Reasoning Result: Dense Automaton Dyadic Boundary (2026-08-13)

Files:

- `self_dual_wreath_dense_automaton_fiber_dyadic_boundary.py`
- `research/representation/self_dual_wreath_dense_automaton_fiber_dyadic_boundary.json`
- `tests/test_self_dual_wreath_dense_automaton_fiber_dyadic_boundary.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-DENSE-AUTOMATON-FIBER-DYADIC-BOUNDARY`

The previous “dense constant-state ordered-subword automaton” question is now
closed exactly. For every support fiber `U subset F_2^u` of density
`delta=|U|/2^u`, the suffix-branch entropy theorem gives an anchor leaving at
most

`floor(u-log2|U|)=floor(log2(1/delta))`

frame generators over every finite group. No automaton assumption is needed.
Consequently every fiber whose density is bounded below has `O(1)` rank,
independent of frame width.

For same/different fibers of codimensions `c_S,c_D`, selecting the denser
fiber gives scalar crossing-pressure margin at least

`(c_S+c_D)/2-floor(min(c_S,c_D))`.

If both fibers mix uniformly on a constant class of size `C`, this tends to
`log2(C)-floor(log2(C))`. Every non-power-of-two class therefore has a
constant unsigned-mass loss that a normalized target character cannot repair.
Only dyadic effective class sizes can saturate the density theorem. The exact
mixed-frame target theorem closes balanced full fibers too: if
`|S|=|D|=2^k` and `0 in S`, the residual target is itself a relation; if
`0 notin S`, adjoining zero gives size `2^k+1` and one full scalar exponent of
loss. Thus no exactly balanced dyadic full fiber survives. **Do not** broaden
this to near-uniform fibers just below a power of two.

The imported periodic `S_3` transfer has an 18-state leading class, exact
limiting density `1/18+O(2^-k)`, generic generator bound four, and limiting
generic scalar margin `log2(18)-4=0.169925...`. This already kills the
periodic escape without the stronger family-specific three-generator
certificate. Six focused tests pass and the live artifact is generated.

The next high-reasoning target is now sharply reduced to **near-uniform**
dyadic fibers: counts just below a power of two can have vanishing generic
margin without exact saturation. Prove a structural torsion/surface gap for
all fixed-state automata in that regime, or construct a mixed-frame fiber with
matching `S_n` homomorphism mass and a nonvanishing normalized
high-dimensional character. Growing-state automata and interleaved leaves are
separate routes. Keep all survival, `M4`, algorithm, and speedup gates false.

## Current High-Reasoning Result: Cyclic Dyadic Torsion No-Go (2026-08-13)

Files:

- `self_dual_wreath_dyadic_modular_fiber_torsion_no_go.py`
- `research/representation/self_dual_wreath_dyadic_modular_fiber_torsion_no_go.json`
- `tests/test_self_dual_wreath_dyadic_modular_fiber_torsion_no_go.py`

Experiment ID:

`EXP-CODE-SELF-DUAL-WREATH-DYADIC-MODULAR-FIBER-TORSION-NO-GO`

The simplest dyadic boundary is now killed all-width. For
`U_(m,u)={v:|v|=0 mod m}` and `u>=m+1`, every `m`-subset is an ordered-subword
relation. Comparing the two `m`-subsets obtained by exchanging adjacent
coordinates gives `x_i=x_(i+1)`. Hence all frame generators are one generator
`x`, an `m`-subset gives `x^m=1`, and every other fiber relation follows:

`P(U_(m,u)) ~= C_m`.

This is a symbolic proof, not an extrapolation from Tietze controls. The
roots-of-unity filter gives

`||U|/2^u-1/m| <= ((m-1)/m) cos(pi/m)^u`.

The cycle index for permutations with all cycle lengths dividing `m` gives
`#Hom(C_m,S_n)=|S_n|^(1-1/m+o(1))`. Thus for fixed `m=2^r`, the true limiting
scalar margin is `r-1+1/m`, strictly positive even though the generic entropy
rank can sit at the dyadic boundary. The minimum is `1/2` at `m=2`. A
normalized target character cannot restore this unsigned mass. Five focused
tests pass and the live artifact is generated.

This theorem covers cyclic Hamming-modulus automata only. It does not classify
nonabelian `2`-group automata, near-uniform dyadic fibers, a modulus growing
with frame width, or interleaved leaves. Those are the only automaton variants
still worth high-reasoning attention; do not resume generic modular searches.
Keep natural `M4`, algorithm, and speedup gates false.

## Current High-Reasoning Frontier: Subgroup-Stratified Orbit Synthesis (2026-08-13)

The binary hidden-involution orbit-synthesis route has advanced beyond the
generic polar and hyperoctahedral-CG formulations. No algorithm or speedup has
been obtained. The newest theorem chain is:

1. `coset_hidden_involution_incidence_walk_boundary.py` gives the exact
   biregular incidence normal form. A generic normalized Szegedy/QSVT polar has
   degree `Omega(sqrt(M))`; only a structured row/Fourier escape remains.
2. `coset_hidden_involution_common_factor_trim.py` removes every tensor
   component containing a global trivial/sign common factor with exact retained
   candidate mass `(1-2a/n!)^k`. The corrected normalized pair overlap is
   strictly below `1/2`, proved by integer arithmetic; floating telemetry may
   round it to `1/2`. This trim does not bound the residual norm.
3. `coset_hidden_involution_subgroup_outlier_hierarchy.py` proves the residual
   norm is in fact superpolynomial. For `K=C_2 wr S_m`, the number of incident
   fixed-point-free involutions is
   `L_m=sum_j m!/(j!(m-2j)!) >= ceil(m/2)^ceil(m/2)`, and nontrivial right-`K`
   invariants witness frame norm at least `L_m` at every copy count.
4. `coset_hidden_involution_spherical_outlier_deflation.py` then proves this
   particular obstruction is not terminal. The full conjugate witness span is
   exactly the nontrivial even-row Thrall support, is QFT-label flaggable, and
   its all-register alternative mass vanishes at the orbit-flatness width.
5. `coset_hidden_involution_subgroup_support_dichotomy.py` generalizes the
   span identity: for arbitrary `L<=G`, the conjugate invariant span is the
   support of `Ind_L^G(1)`, with Plancherel dimension at most
   `[G:L]sqrt(|G|)`. Low-index subgroups are therefore information-
   theoretically negligible after an all-register support trim, but efficient
   support membership is not automatic.
6. `coset_hidden_involution_imprimitive_plethysm_boundary.py` exhibits the
   important high-index survivor `S_b wr S_a`, `b>=3`. It proves the exact
   fixed-point-free incidence formula and resolves all two-row constituents by
   subset-orbit differences. Odd two-row sectors survive the even-row trim but
   their full label union is again negligible and directly deflatable.
7. `coset_hidden_involution_foulkes_support_mass_probe.py` compiles the entire
   Foulkes character `h_a[h_b]` in the power-sum basis without enumerating the
   subgroup. It computes exact constituent support, Plancherel mass, and the
   actual common-trimmed candidate probability `w`. For `h_a[h_3]`, `w` is
   `0.1060, 0.1934, 0.3810, 0.6136` at `a=4,6,8,10`; nevertheless `w^k` remains
   below `2^-41` in these controls. This is not an asymptotic theorem. The
   decisive quantity is `k(1-w)`.
8. `coset_hidden_involution_foulkes_support_projector_no_go.py` proves that a
   generic conjugate-twirl QSVT support test is exponentially conditioned. On
   `lambda=(2a+1,a-1)`, the twirl eigenvalue is at most `6a/3^a`; Markov's
   inequality forces exponential polynomial degree. This does not rule out a
   direct label predicate or structured coherent restriction transform.

The active research target is now sharply defined: determine the asymptotic
Plancherel/candidate support deficit of `h_a[h_b]`, especially fixed `b=3`, and
either compile or rule out a structured higher-row support projector. The
correct falsifier is whether `k(1-w_(a,b))` diverges. If it stays bounded, the
all-register deflation architecture fails and the higher-row support needs a
structured polar. If it diverges, prove that fact and then classify the next
high-index subgroup stratum. General plethysm NP/#P hardness is relevant
evidence but is not a quantum lower bound and must not close the gate.

The exact `h_12[h_3]` support-mass calculation completed in 2400.73 seconds
and is preserved separately in
`research/representation/coset_hidden_involution_foulkes_support_mass_h12_diagnostic.json`.
It gives `w=0.8030040889256911`, `k=74`, `k(1-w)=14.5776974195`, and
`w^k=8.894345546e-8=2^-23.4225`.  The finite all-register mass is still small,
but `k(1-w)` fell from `22.7992` at `a=10`; no monotone trend or asymptotic
deficit theorem follows.  Do not rerun this in routine validation.  The
reusable module's default live artifact intentionally stops at `h_10[h_3]`.

All algorithm, residual-norm, decoder, natural-input classical separation, and
speedup gates remain false. Gemini/Antigravity should wire these reports but
must not infer asymptotic behavior from the finite sequence.

**Priority correction after the support analysis.**
`coset_hidden_involution_bulk_conditioning_normalization_no_go.py` proves that
outlier classification is not the primary compiler bottleneck. If `X` is the
uniform-source eigenvalue law of unnormalized synthesis, then
`E[X]=1`, `Var(X)=(M-1)/2^k`, and the alternative law is the exact `X`-size
bias. With a modest copy overhead, all but vanishing alternative mass lies in
`X in [1-delta,1+delta]`, where the unnormalized polar has constant condition
number. However, inherited incidence access is `D=S/sqrt(M)`, so the useful
singular values are still `Theta(M^-1/2)` and Bernstein forces
`Omega(sqrt(M))` odd-QSVT degree. Canonicalization, QFTs, and coherent unitary
trims preserve that scale unless they expose a genuinely different access
normalization.

This supersedes the previous priority sentence: the first target is now a
`poly(n)`-normalization block encoding, direct orbit-row polar, or structured
fast-forward of the matrix group-convolution row walk. Continue Foulkes
support-deficit work only when it can produce such a primitive or a rigorous
no-go for one. A support classification by itself is no longer sufficient
progress. Keep the exact `h_12[h_3]` run as diagnostic evidence, not as the
main architecture.

`coset_hidden_involution_branch_erasure_normalization_no_go.py` closes the
first apparent normalization shortcut.  Candidate-controlled preparation is
the exact isometry

`V(direct_sum_h x_h)=sum_h |h>B_h x_h`.

Any normalized one-row operation on the candidate label has coefficients
`c_h`; agreeing with a common multiple `S/alpha` of the unlabelled synthesis on
every branch forces `c_h=1/alpha`, hence `alpha>=sqrt(M)`.  The uniform
homogeneous-space Fourier row attains equality and has success operator
`S^*S/M`.  Consequently its success remains `Theta(1/M)` even on the
constant-conditioned alternative bulk, and ordinary amplitude amplification
still costs `Theta(sqrt(M))`.  Nonuniform label preparation, candidate phases,
and a branch QFT followed by one clean output row are closed.

Do not broaden this result into an arbitrary-circuit lower bound.  A joint
candidate/physical multiplicity transform, a decoder retaining a large
homogeneous-space Fourier sector, multi-round candidate relocation, and a
direct orbit-row polar remain open.  In particular, counting retained irrep
*labels* is not enough: one `S_n` sector can have large carrier dimension.  The
next hard question is whether the full `C[G/K]` Fourier coordinate can couple
to the physical `S_n` multiplicities through an efficiently implementable
matrix-Hecke/recoupling transform whose normalization is not inherited from
one-row erasure.

`coset_hidden_involution_fourier_coefficient_normalization_no_go.py` closes
the next generic variant.  In the regular row normal form, Schur orthogonality
gives the exact block identity

`W_nu=sqrt(|G|/d_nu) I_(d_nu) tensor A_nu`,

where `A_nu` is the raw physical Fourier-coefficient matrix of the canonical
representatives.  A useful constant singular value of `W_nu` occurs at scale
`sqrt(d_nu/|G|)` in normalization-one access to `A_nu`.  Since
`d_nu<=sqrt(|G|)`, generic bounded-polynomial polar amplification costs at
least `|G|^(1/4)` in every sector, the same factorial leading scale as
`sqrt(M)` for perfect matchings.  Exact `S_3` controls verify all carrier,
multiplicity, and singular-value factors for one through three copies.

This still is not a recoupling lower bound.  A direct sector block encoding
already normalized at `sqrt(d_nu/|G|)`, a structured matrix-Hecke
fast-forward, or a non-QSVT row polar remains open.  The next positive attempt
must explicitly construct one of those; “prepare `v_o`, apply the physical
QFT, then run generic QSVT on its coefficients” is now closed.

`coset_hidden_involution_binary_identification_self_reduction.py` materially
raises the value of the binary compiler target.  Left-coset dephasing for
`L<=G` obeys `Delta_L(R_h)=R_h` when `h in L` and zero otherwise.  For a
proposed matching edge `e`, taking `L=S_e x S_(complement(e))` therefore emits
an exact smaller hidden instance iff `e` is present, and an exact maximally
mixed null instance otherwise.  Factoring all already-known edge swaps as
`C_2^t` and retaining every Fourier character positive on their product has
probability exactly `1/2`; the loss does not compound with recursion depth.
Testing partners of one remaining vertex at each level needs `m^2-1` binary
membership tests.  Candidate verification supplies the converse reduction.

Thus, in the explicit fresh-coset-state model, a polynomial worst-case binary
detector for all smaller perfect-matching instances yields a polynomial hidden
matching identifier.  This is consistent with and narrower than the published
Fenner--Zhang decision/search equivalence for permutation-group HSP
(`arXiv:cs/0610086`); do not claim novelty for the general equivalence.  The
artifact's value is the exact state-channel recursion and its no-compounding
ledger.  No efficient detector, graph-isomorphism reduction, or speedup has
been obtained.

`coset_hidden_involution_rigid_gi_bridge.py` restores the natural-problem
stakes without inventing a new reduction.  The primary Moore--Russell--Schulman
construction (`arXiv:quant-ph/0501056`) maps two rigid `n`-vertex graphs to a
trivial subgroup when nonisomorphic and to `{1,m_alpha}` when isomorphic,
where `m_alpha` swaps the two vertex blocks and is a fixed-point-free
involution in `S_(2n)`.  The possible `m_alpha` form a structured
`S_n wr C_2` class of size `n!` inside the full `(2n-1)!!` matching class.

The same source explicitly observes, and the new finite controls verify as a
density-matrix identity, that sampling over `S_n wr C_2` or over `S_(2n)` only
adds a maximally mixed left-transversal register.  Moreover, random full-group
conjugation turns any fixed structured `m_alpha` into the uniform full
perfect-matching class while leaving the null invariant.  Therefore a
polynomial full-class binary detector decides rigid GI; the binary-to-search
self-reduction would identify `m_alpha` and recover the unique isomorphism.

This bridge is prior art plus an explicit compatibility audit, not a new GI
algorithm.  It does not handle nonrigid graphs or general GI, and the binary
detector remains blocked by normalization/recoupling.  It does establish that
solving the active compiler problem would matter on a natural input family,
rather than only in an opaque oracle benchmark.

## Newest High-Reasoning Frontier: Binary Hidden Involutions

The newest pass separates information-theoretic binary detection from hidden-
element identification for a conjugacy class `C` of `M` nonidentity
involutions. No new algorithm or speedup has been found. The completed theorem
chain is:

- `coset_hidden_involution_binary_decision_reduction.py`: the centered mixed
  alternatives are Hilbert--Schmidt orthogonal and
  `chi^2(rho_C^k || I/d)=(2^k-1)/M`. One-copy weak Fourier labels and the
  two-copy `(lambda,mu;nu)` coupling label are exactly Helstrom-optimal in
  their stated regimes. Hayashi--Kawachi--Kobayashi already imply the
  `Theta(log M)` sample scale, so it is not novel.
- `coset_hidden_involution_fourth_moment_threshold.py`: an exact fourth-moment
  identity in `(M,c,T,E)` gives a constant trace-distance lower bound at
  `k=ceil(log2 M)`. This is an explicit certificate, not a new sample theorem.
- `coset_hidden_involution_query_separation_boundary.py`: opaque-label
  classical access needs `Omega(sqrt(M))` queries by a collision-transcript
  bound, while standard coset states give an unbounded-processing quantum
  upper bound `O(log M)`. Do not claim a matching arbitrary-quantum lower
  bound. Ettinger--Hoyer--Knill already give polynomial finite-HSP queries.
- `coset_hidden_involution_threshold_compiler_boundary.py`: the natural
  normalization-one average-projector encoding exists, but generic scalar
  thresholding at scale `2^-k` has exponential degree. Its central class-sum
  dilation is exact, while measuring only the dilation label is suboptimal.
- `coset_hidden_involution_support_span_reduction.py`: the Hayashi support test
  is `T=supp(A_k)`, accepts every alternative, and has null acceptance at most
  `M/2^k`. Its polar/range synthesis remains computationally unimplemented.
- `coset_hidden_involution_orbit_hull_twirl_reduction.py`: Schur twirling gives
  `A_k=direct_sum_nu I_(V_nu)/d_nu tensor Q_nu` and
  `T=direct_sum_nu I_(V_nu) tensor supp(Q_nu)`. Binary detection removes the
  carrier-orientation output; multiplicity support is the missing object.
- `coset_hidden_involution_multiplicity_support_obstruction.py`: diagonal group
  and stabilizer actions are identity on global multiplicity, so they cannot
  implement `T` when a `supp(Q_nu)` is proper nonzero. Exact `S_3/S_4`
  controls verify proper support; no all-`n` proper-support theorem is claimed.
- `coset_hidden_involution_support_filter_no_go.py`: the generic support-filter
  obstruction is distributional, not a negligible hard edge. Exactly,
  `Tr(A_k)/d=2^-k`,
  `Tr(A_k^2)/d=4^-k[1+(2^k-1)/M]`, and the alternative mean eigenvalue is
  `mu=2^-k+(1-2^-k)/M`. At `k=ceil(log2(4M))`, at least `3/4` of alternative
  mass lies below `4mu<=5/M`. Any globally `[0,1]`-bounded polynomial effect
  with null acceptance at most `1/3` and alternative acceptance at least
  `2/3` has degree at least `1/sqrt(72mu)=Omega(sqrt(M))`. This refutes generic
  normalization-one QSVT filtering, not arbitrary circuits.

The latest affected chain passed **52 tests** in 6.89 seconds. The newest
support-filter report contributes **8 focused passing tests** and a live
artifact. Artifacts use matching basenames under `research/representation/`,
except the query-boundary artifact under `research/classical_baselines/`.

**Current high-judgment target.** The surviving binary route is a structured
fused transform that deflates exceptional large-eigenvalue sectors and
directly rescales or projects naturally occupied multiplicity blocks without
paying the raw `Theta(1/M)` frame scale. Require both constant retained natural
source mass and coherent polynomial normalization/support access. Existing
standalone whitening results already impose an `exp(Omega(sqrt(n)))` burden;
renaming the inverse as a branching transform is not progress. The decisive
falsifier is that every proposed deflation still leaves constant alternative
mass at exponentially small normalized singular values. Any survivor must
also pass a classical query-limited comparison.

### Weak-source deflation is closed (2026-08-13)

`coset_hidden_involution_source_deflation_no_go.py` proves that weak Fourier
source labels cannot supply the missing structured deflation.  If `p` is the
Plancherel source law, `q(lambda)=p(lambda)(1+r_lambda)`, and `M` is the
involution-class size, character-column orthogonality gives exactly

`chi^2(q^k || p^k)=(1+1/M)^k-1`.

At `k=Theta(log M)` this is `o(1)`, even though the full quantum chi-square is
`(2^k-1)/M=Theta(1)`.  For the conditioned normalized frame

`B_s=E_h tensor_i(I+rho_(lambda_i)(h))/2`,

the exact trace law is `Tr(B_s)/D_s=2^-k ell(s)`.  Markov plus the existing
global spectral theorem leaves at least one half of alternative mass
simultaneously in ordinary source blocks and at `A_k` eigenvalue `O(1/M)`.
The exact block chi-square chain rule

`sum_s p_s ell_s^2 chi^2(sigma_s||I/D_s)`
`=(2^k-1)/M-[(1+1/M)^k-1]`

shows that essentially all threshold signal is internal to conditional
multiplicity blocks, not in the source transcript.  This closes source-only
testing and deletion of exceptional source labels.  It does **not** close a
coherent source-controlled transform acting inside each block.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-SOURCE-DEFLATION-NO-GO`.  The same-stem artifact
is under `research/representation/`; four exact finite controls pass.

### Proper multiplicity support is now an all-n theorem (2026-08-13)

`coset_hidden_involution_isotypic_support_no_go.py` upgrades the old `S_3/S_4`
finite witness.  For simultaneous conjugation `U_g`, a direct fixed-point
count gives

`Tr(U_g rho_h)=|g^G|^-1(1+1[gh is conjugate to g])`.

Writing `s_K=|K|` and
`z_K=|{h in C:g_K h is conjugate to g_K}|`, the exact diagonal-isotypic laws
are

`p_nu=d_nu/|G| sum_K chi_nu(K)/s_K^(k-1)`,

`q_nu=d_nu/|G| sum_K chi_nu(K)/s_K^(k-1)`
`      *[1+(2^k-1)z_K/M]`.

Character bounds imply

`TV(p,q)<=(2^k-1)(p(n)-1)/(2 s_min^(k-1))`.

For fixed-point-free involutions in `S_n`, every even `n>=6`, and
`k=ceil(log2(4M))`, the elementary inequalities `k>=n`, `2^k<=8M`,
`M<=n^(n/2)`, `p(n)<=2^(n-1)`, and `s_min>=n(n-1)/2>=n^2/3` give

`TV(p,q)<=4/n^((n-2)/2)<=1/9`.

If the support projector were a union of whole diagonal isotypic sectors,
perfect alternative acceptance and null acceptance at most `1/4` would force
label TV at least `3/4`, a contradiction.  Therefore at least one diagonal
sector has proper nonzero multiplicity support for every even `n>=6`.  This
proves the scalable proper-support gate that the previous module explicitly
left open.  It rules out diagonal group/subgroup actions and whole-isotypic
GPE as support compilers, but not commutant-side recoupling or a fused
multiplicity transform.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-ISOTYPIC-SUPPORT-NO-GO`.  Four exact controls
compare the class formula with direct regular-basis fixed-point traces; the
`S_4` fixed-point-free value is exactly `1/6`.  For the odd fixed-point-free
class in `S_6`, parity makes every `z_K` zero and the isotypic laws identical.

### The proper low-spectrum obstruction has constant mass (2026-08-13)

`coset_hidden_involution_multiplicity_hard_mass.py` rules out the possibility
that the all-n proper block is negligible.  Put
`t_nu=rank(S_nu)/dim(M_nu)`.  The support-rank bound and the new isotypic TV
theorem imply

`E_p[t_nu]<=1/4`,  `E_q[t_nu]<=1/4+epsilon`,  `epsilon<=1/9`.

Markov gives `q{t_nu<=1/2}>=5/18`.  Intersecting this event with the existing
`3/4` alternative low-spectrum event yields the uniform theorem

`Pr_q[t_nu<=1/2 and lambda(A_k)<=5/M] >= 1/36`.

Thus constant natural mass simultaneously requires a genuinely internal
multiplicity projector and lives at exponentially small normalization-one
spectral scale.  Deleting exceptional proper sectors cannot rescue generic
filtering.  The theorem still does **not** lower-bound a fused support/polar
isometry.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-HARD-MASS`.  Three finite sector-law
controls pass.  Across the stored all-n scaling rows, the sharper certified
intersection lower bound is at least `0.2667`; `1/36` is the uniform theorem,
not a finite extrapolation.

The focused/adjacent chain for these three modules and the prior multiplicity,
support-filter, and orbit-hull modules passes 39 tests in 3.25 seconds.  The
two broader new-module/adjacent runs passed 21 and 38 tests respectively.

### Orbit synthesis is relatively flat on most alternative mass (2026-08-13)

`coset_hidden_involution_orbit_synthesis_flatness.py` studies the unnormalized
range-synthesis operator

`S: direct_sum_(h in C) ran(P_h) -> H`,  `S((v_h))=sum_h v_h`.

It satisfies `SS*=M A_k`.  If `R=D/2^k` and the eigenvalues of `S*S` are
normalized over its `MR`-dimensional source (including its kernel), then

`E[x]=1`,  `E[(x-1)^2]=(M-1)/2^k=:eta`.

The alternative state is exactly the size-biased law of `x`.  Consequently

`Pr_alt(|x-1|>delta) <= eta(delta^-2+delta^-1)`.

At `k=ceil(log2(64M))` and `delta=1/2`, at least `29/32` of alternative mass
has `x in [1/2,3/2]`.  Thus most natural signal is well conditioned after the
correct relative rescaling.  This defeats any argument that the absolute
`Theta(1/M)` eigenvalue scale alone is a computational no-go.  It does not
provide standard-access implementation of the unnormalized `S`, erase the
branch label, or compile the polar.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-ORBIT-SYNTHESIS-FLATNESS`.  Four finite controls
pass; the six-copy-overhead scaling rows retain at least `0.9093` alternative
mass in the stated relative window.

### The exact common top outlier is removable but negligible (2026-08-13)

`coset_hidden_involution_common_outlier_deflation.py` proves

`intersection_(h in C) ran(P_h)=C[S_n/<C>]^tensor k`.

For the fixed-point-free involution class in even `n>=6`, its normal closure is
`S_n` when `n/2` is odd and `A_n` when `n/2` is even.  The common dimension is
therefore `a^k`, with `a=1` or `2`.  This is exactly the top `SS*` eigenspace
with eigenvalue `M`, and it can be coherently flagged using the trivial sector,
or trivial plus sign sectors, of the per-register `S_n` Fourier transform.

Its alternative mass is `(2a/n!)^k`, and its share of centered synthesis
variance is `((M-1)/M)(4a/n!)^k`.  Both are super-exponentially negligible at
the flatness threshold.  Deflating this explicit outlier does not prove any
operator-norm bound for the remainder; pair and higher intersections remain.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-COMMON-OUTLIER-DEFLATION`.  Three exact normal-
closure controls pass.  The stored common-mass and variance-share logarithms
are already below `-75` on the tested scaling family.

### Every pair polar has a structured phase compiler (2026-08-13)

`coset_hidden_involution_pair_polar_phase_compiler.py` gives the first positive
compiler primitive on this frontier.  For right-regular involutions `H,G`,
`P=(I+H)/2`, `Q=(I+G)/2`, and `U=HG`, the exact partial polar is

`polar(QP)=U^(-1/2) supp(PQP)`.

If `r=ord(HG)`, then on every regular dihedral copy

`spec(PQP|ran(P))={cos^2(pi ell/r):0<=ell<r}`.

The phase-`pi` sector is exactly the kernel.  A generic gap-dependent bounded-
polynomial polar can pay the inverse minimum cosine `Theta(r)`, but phase
estimation of the explicit permutation `U` resolves the phase and applies the
half rotation using `O(log r+log(1/epsilon))` controlled powers.  For `S_n`,
`log r<=log(n!)=O(n log n)`.  The pair polar tensorizes exactly, so the `k`-
copy pair compiler is polynomial.  This proves that tiny pair singular values
are not themselves a computational obstruction.  It does not compile the
full `M`-branch synthesis polar.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-PHASE-COMPILER`.  Five exact dihedral
controls and five scaling rows pass; the focused/adjacent chain passed 28
tests after tightening the finite-vs-asymptotic generic-gap claim.

### Canonical pair transport has extensive nontrivial holonomy (2026-08-13)

`coset_hidden_involution_pair_polar_holonomy_no_go.py` proves that efficient
pair polars do not form a path-independent global alignment.  For the three
transpositions in the regular representation of `S_3`, every pair product has
order three, while the canonical pair-polar triangle restricted to the
starting plus space has exact spectrum

`{1,-1,-1}`.

Its distance from identity is two, and the direct edge differs from the two-
edge path by norm two.  Vertex gauge changes only conjugate this loop, so the
spectrum cannot be gauged away.  The regular `S_3` action embeds the witness as
three fixed-point-free involutions in every even `S_n`, `n>=6`; common
disjoint swaps extend it without changing the generated `S_3` or pair-product
orders.  On `k` copies the negative holonomy multiplicity is

`(3^k-(-1)^k)/2`,

so the defect occupies asymptotically one half of the pair-aligned source
space.  This closes blind spanning-tree composition of canonical pair polars.
It does not close a path-register architecture, coherent holonomy correction,
connection-Laplacian quotient, or direct multiplicity/global polar.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-HOLONOMY-NO-GO`.  The exact `S_3`
control and embeddings through `n=64` pass; the phase-compiler plus holonomy
chain passes 17 tests.  Keep all algorithm, MRS-escape, global-polar, and
speedup gates false.

### The nonflat S3 chart nevertheless has a constant-conditioned polar (2026-08-13)

`coset_hidden_involution_s3_chart_gram_compiler.py` proves that pair holonomy
is not itself a conditioning no-go.  Split each three-dimensional plus fiber
of the regular `S_3` chart as a common invariant line `T` and a two-dimensional
standard space `W`.  Pair-overlap magnitude is one on `T` and one half on `W`;
triangle holonomy is `+1` on `T` and `-1` on `W`.  A `k`-copy sector with `m`
standard factors has multiplicity `binom(k,m)2^m`, overlap `a=2^-m`, and exact
three-branch Gram spectrum

`m even: (1+2a,1-a,1-a)`,

`m odd:  (1+a,1+a,1-2a)`.

Only two `m=0` modes and one mode across each of the `2k` internal `m=1`
directions vanish.  Therefore

`rank(G_k)=3^(k+1)-2(k+1)`.

For every `k>=2`, the nonzero Gram spectrum is contained in `[3/4,3]`, so the
source-synthesis condition number is at most two.  The Gram commutes with the
triangle connection Laplacian, but the parallel-section kernel is only one
connection sector, not the full synthesis support.  A controlled `T/W`
decomposition, defect-weight counter, parity-dependent three-branch transform,
and bounded rescaling compile this constant-size chart polar in polynomial
`k`.  This is a positive local mechanism, not an algorithm: no compatible
cover, spherical transform, branch-label erasure, or full-class normalization
has been constructed.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-S3-CHART-GRAM-COMPILER`.  Four exact matrix
controls and five formula-only scaling rows pass; the compiler/holonomy chain
passes 24 tests.  This result revises any interpretation that nonflatness alone
closes holonomy-aware synthesis.  It leaves every full-class and speedup gate
false.

### Global branch covariance is an induced bundle, not pair-polar gluing (2026-08-13)

`coset_hidden_involution_induced_source_bundle_reduction.py` identifies the
full branch-labeled orbit source exactly.  For `K=Stab(P_0)` and
`R=ran(P_0)`,

`E=direct_sum_(xK in G/K) ran(U_x P_0 U_x^*) ~= Ind_K^G R`.

The synthesis `S:E->H`, `S((v_x))=sum_x v_x`, is a `G` intertwiner.  Hence
Frobenius reciprocity gives

`E=direct_sum_nu V_nu tensor Hom_K(V_nu,R)`,

`S=direct_sum_nu I_(V_nu) tensor S_nu`.

This absorbs branch permutation and stabilizer cocycles without composing
canonical pair polars.  Those pair polars define a different connection: on
the one-copy regular `S_3` fiber, the stabilizer cocycle has spectrum
`{1,1,-1}`, whereas the pair-polar triangle has `{1,-1,-1}`.  Pair-polar path
gluing should therefore be deprioritized as a route to global covariance.

For `k` copies of the exact `S_3` chart, induced-source multiplicities are

`mult(1)=(3^k+1)/2`, `mult(sgn)=(3^k-1)/2`, `mult(std)=3^k`.

Synthesis is injective on the trivial/sign blocks and has standard
multiplicity rank `3^k-(k+1)`, so its entire kernel is `k+1` standard copies.
The branch-labeled induced transform can be organized from coherent coset
factorization, uniform `K` preparation, controlled `K` action, and the `G`
QFT.  For the symmetric/hyperoctahedral pair those covariance primitives are
available.  This still starts with a branch-labeled source; it does not compile
the physical analysis map `S*`, the multiplicity support/polar, or full-class
normalization.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-INDUCED-SOURCE-BUNDLE-REDUCTION`.  Three exact
equivariance/character/block-rank controls pass; the induced/chart/holonomy
chain passes 21 tests.  Keep all physical-lift, multiplicity-polar, algorithm,
and speedup gates false.

### The remaining transfer is matrix-valued Hecke, not scalar spherical (2026-08-13)

`coset_hidden_involution_matrix_hecke_transfer_reduction.py` gives the exact
operator on the induced multiplicity spaces.  For
`T in Hom_K(V_nu,R)`, `R=ran(P_0)`, define

`F_nu(T)=|G:K|^-1/2 sum_(xK) U_x T rho_nu(x)^*`.

Then `F_nu(T) in Hom_G(V_nu,H)` and

`<F_nu(T),F_nu(T')>`
`=|K|^-1 sum_(g in G) Tr[T^* P_0 U_g P_0 T' rho_nu(g)^*]`.

This is a positive matrix-valued Hecke transfer on
`Hom_K(V_nu,R)`.  It is not the commutative scalar Hecke algebra of `G/K`
unless the stabilizer fiber is trivial and one-dimensional.  On the regular
`S_3` chart, the scalar three-branch Hecke algebra has dimension two, while

`dim End_G(Ind_K^G R^tensor k)=(3*9^k+1)/2`.

The standard source multiplicity alone is `3^k`.  Direct normalized coset
transfer matrices and the group-sum Gram formula agree to about `1e-15` in
every tested sector, and reproduce the exact induced-source synthesis ranks.
This proves that outcome-side perfect-matching spherical eigenvalues cannot
compile the natural physical transfer.  Large matrix dimension is not a
hardness proof; a succinct centralizer/recoupling transform may still exist.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-TRANSFER-REDUCTION`.  Two exact
sector families pass; the matrix-Hecke/induced/chart chain passes 18 tests.
Keep the uniform matrix-Hecke basis, structured polar, physical source lift,
algorithm, and speedup gates false.

### Generic hyperoctahedral fusion contains symmetric Kronecker (2026-08-13)

`coset_hyperoctahedral_cg_kronecker_reduction.py` proves that a generic
`C_2 wr S_m` Clebsch--Gordan transform is not supplied by its efficient QFT.
The wreath irreps `(lambda,empty)` are inflations of `S_m` Specht modules, so

`(lambda,empty) tensor (mu,empty)`
`=direct_sum_nu g(lambda,mu,nu)(nu,empty)`.

Thus a uniform wreath CG transform contains the internal symmetric-group
Kronecker transform on the trivial-color sector.  Five exact character-inner-
product controls through `m=6` pass.  This is not a quantum lower bound.  Under
regular `K_m` Plancherel the sector has mass `2^-m`, or `2^(1-m)` conditioned
on even central parity, so its relevance to the natural source required a
separate mass theorem.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-CG-KRONECKER-REDUCTION`.  The focused/adjacent
chain passes 19 tests.  Keep natural hard-sector mass, generic/source-specific
fusion hardness, a uniform CG compiler, algorithm, and speedup gates false.

### The embedded Kronecker sector is negligible under the natural source (2026-08-13)

`coset_hyperoctahedral_trivial_color_mass_no_go.py` supplies the required
self-critique.  Let `N=(C_2)^m` be the base subgroup of
`K=C_2 wr S_m`.  The one-copy source fiber is the `K` permutation module
`C[S_(2m)/<h>]`, and the sum of all `(lambda,empty)` sectors is exactly its
`N`-invariant subspace.  For a base element flipping `t` matching pairs,

`chi_R(a)=|C_G(a)|/2 (1+1[2t=m])`,

`|C_G(a)|=2^t t!(2m-2t)!`.

Burnside projection gives the exact `k`-copy source fraction

`w_(m,k)=2^-m sum_t binom(m,t)`
` [2^t t!(2m-2t)!/(2m)! (1+1[2t=m])]^k`.

Every nonidentity normalized character is at most `1/3` for `m>=2`, so at
`k>=m`, `w_(m,k)<=2^(1-m)`.  Source fraction alone does not control the
alternative size-biased law, so the theorem additionally uses the exact frame
moment `E[x^2]=1+(M-1)/2^k`: Cauchy--Schwarz bounds alternative contribution
by `sqrt((1+eta)w)`.  At the six-copy flatness overhead this vanishes as
`2^((1-m)/2)`.  Hence the ordinary-Kronecker embedded sector is not the
natural compiler bottleneck; source-heavy colored sectors are.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-TRIVIAL-COLOR-MASS-NO-GO`.  Five direct coset-
fixed-point/Burnside controls pass; the mass/CG/matrix-Hecke chain passes 21
tests.  Keep colored-sector classification/fusion, full matrix-Hecke polar,
algorithm, and speedup gates false.

### Natural base colors concentrate in balanced bands (2026-08-13)

`coset_hyperoctahedral_color_weight_concentration.py` Fourier-inverts the full
base group `N=(C_2)^m`.  If `q_t` is the normalized source character at a base
element of weight `t`, the exact `k`-copy color-weight law is

`p_(m,k)(r)=binom(m,r)2^-m sum_t K_t(r)q_t^k`,

with binary Krawtchouk polynomial `K_t`.  Since every nonidentity `q_t<=1/3`,

`TV(p_color,Uniform(F_2^m))<=((2^m-1)/2)3^-k`.

At `k>=m`, source color weight is exponentially close to
`Binomial(m,1/2)`.  Hoeffding plus the global frame second moment transfers
this to alternative contribution: asymptotically all signal has color size in
`[m/4,3m/4]`.  The next target is residual `S_r times S_(m-r)` multiplicity on
balanced colors, not the all-trivial sector.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-COLOR-WEIGHT-CONCENTRATION`.  Five exact integral
Fourier controls pass; the color/trivial/CG chain passes 24 tests.  Keep
balanced residual fusion, matrix-Hecke polar, algorithm, and speedup false.

### The complete K-irrep source law is wreath-Plancherel typical (2026-08-13)

`coset_hyperoctahedral_source_plancherel_typicality.py` upgrades color
concentration to every bipartition.  For `x in K=C_2 wr S_m`,

`q_x=chi_R(x)/dim(R)=(1+1[xh~x])/|x^{S_(2m)}|`.

For `m>=3`, nonidentity `q_x<=4/((2m)(2m-1))`.  The `k`-copy source irrep law
satisfies

`TV(p_k,Plancherel(K))<=((|K|-1)/2)q_max^k`.

Wreath Plancherel has an explicit hierarchy: draw
`r~Binomial(m,1/2)`, then independently draw `alpha` and `beta` from ordinary
Plancherel on `S_(m-r)` and `S_r`.  The actual source is therefore not confined
to an exceptional easy family.  Frame-second-moment transfer gives the same
typical-set conclusion for alternative contribution, but QFT labels still do
not resolve repeated multiplicity copies.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-SOURCE-PLANCHEREL-TYPICALITY`.  Three exact
character/dimension/factorization controls pass; the typicality/color/mass
chain passes 22 tests.  Keep typical multiplicity transfer/polar, algorithm,
and speedup false.

### Typical source basis tuples form exact free K orbits (2026-08-13)

`coset_hyperoctahedral_free_orbit_canonicalization_boundary.py` gives the
concrete module behind Plancherel typicality.  The plus fiber has permutation
basis `X=S_(2m)/<h>` under `K` conjugation, and the `k`-copy source is
`C[X^k]`.  Its nonfree tuple fraction is bounded by

`sum_(x!=e)q_x^k <= (|K|-1)q_max^k`.

Hence asymptotically all source basis tuples lie in free `K` orbits and

`C[X^k_free] ~= C[K] tensor C[O_free]`.

The same frame moment proves asymptotically full alternative contribution on
this exact regular module.  This converts the abstract multiplicity-basis
question into coherent orbit representative/transporter computation.  It does
not assume such a canonicalizer is efficient.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-FREE-ORBIT-CANONICALIZATION-BOUNDARY`.  Five exact
free-tuple/orbit controls pass; the free/Plancherel/color chain passes 22 tests.

### A polynomial canonicalizer resolves the trimmed source basis (2026-08-13)

`coset_hyperoctahedral_trimmed_orbit_canonicalizer.py` constructs the missing
canonicalizer on asymptotically full mass.  For a coordinate pair, enumerate
the four right-`<h>` orientations.  If the ordered permutation action generated
by `(h,p,q)` is transitive, an ordered breadth-first traversal from one of
`2m` roots gives a unique labeling.  Normalize the transformed matching back
to canonical `h`, transform the full tuple, and take the lexicographic minimum
over polynomially many seed pairs/orientations/roots.  On free tuples the
transporter is unique and obeys the exact covariance law.

For independent uniformly oriented seed cosets, `p,q` are independent uniform
permutations.  A common-invariant-subset union bound gives

`delta_n<=sum_(s<=n/2)1/binom(n,s)`

for one pair to be intransitive.  Disjoint seed pairs amplify to `delta_n^L`.
Combining this with the nonfree bound and frame second moment proves polynomial
canonicalization on `1-o(1)` source and alternative contribution.  A
deterministic polynomial map has a reversible polynomial implementation on
the coherently flagged good set; a gate-level workspace/error ledger is still
owed.

Experiment ID:
`EXP-COSET-HYPEROCTAHEDRAL-TRIMMED-ORBIT-CANONICALIZER`.  Three exact
reconstruction/covariance/uniqueness controls pass; the canonicalizer/free/
Plancherel chain passes 20 tests.  This is a positive source-basis compiler,
not the physical transfer polar or an algorithm.

### Trimmed induction yields regular S_n row frames (2026-08-13)

`coset_hidden_involution_regular_orbit_row_reduction.py` removes generic
hyperoctahedral fusion from the active architecture.  On the canonicalized
source,

`Ind_K^G(C[K] tensor C[O]) ~= C[G] tensor C[O]`.

For canonical orbit representative vectors `v_o`, synthesis becomes

`W|g,o>=U_g|v_o>`,

and its Gram is matrix group convolution

`<g,o|W^*W|g',o'>=<v_o|U_(g^-1 g')|v_o'>`.

The `S_n` QFT removes the regular carrier coordinate, leaving only a
source-specific row-frame operator in each physical multiplicity block.
Generic `C_2 wr S_m` Clebsch--Gordan fusion and a separate subduction basis are
therefore unnecessary on trimmed high mass.  The exact regular `S_3` two-copy
control has source dimension 24, rank 20, 12 nonzero cross-orbit blocks, and
maximum cross overlap `1/4`; canonicalization is not itself the polar.

Experiment ID:
`EXP-COSET-HIDDEN-INVOLUTION-REGULAR-ORBIT-ROW-REDUCTION`.  The regular-row/
canonicalizer/matrix-Hecke chain passes 14 tests.  Keep row polar, group/orbit
label erasure, full synthesis polar, algorithm, and speedup false.

**Revised current high-judgment target.** Source weighting, whole-isotypic
routing, negligible proper sectors, absolute-scale filtering, and blind
pairwise alignment are closed.  The geometry is nevertheless relatively flat
after natural rescaling, the common top outlier is explicitly removable, and
every local pair polar is efficiently compilable.  The exact `S_3` chart shows
that defect weight plus holonomy parity can compile a nonflat local Gram with
constant conditioning, while the induced-bundle theorem removes pairwise chart
gluing as a separate covariance problem.  The surviving question is now
strictly the **orbit-representative row-frame polar** after the regular
`S_n` coordinate has been Fourier transformed.  Source basis, stabilizer
fusion, and branch covariance are solved on asymptotically full natural mass.
The next decisive theorem should derive a succinct block encoding and spectral
normal form for the matrix kernels
`<v_o|U_g|v_o'>`, including the exact normalization inherited after carrier
transfer.  Try to prove a post-common-deflation operator-norm/condition bound
on constant alternative mass; otherwise reduce structured label erasure to a
matched index-erasure/adversary problem without importing black-box lower
bounds into the natural model.  Any positive compiler must specify physical
analysis access, orbit-copy handling, phase precision, garbage uncomputation,
and how it avoids measured-sieve restrictions.  It must still face a matched
classical query/sample model.

## DCP Adaptive-Linear Affine-Flat Boundary

`dcp_linear_reparameterization_affine_flat_no_go.py` closes one concrete
non-coordinate escape for density-one low-bit subset-sum fibers. Let
`N=2^q`, `m=2q+O(1)`, and
`F_(a,s)={x in F_2^m: sum_i a_i x_i=s mod N}`. For an affine `r`-flat,
group the generator matrix's repeated nonzero columns into `t` distinct parity
features. Their aggregate coefficients remain independent uniform residues,
and the parity-evaluation matrix has rational rank `t`. Smith normal form plus
Hadamard gives fixed-flat probability at most `t^(t/2)/N^(t+1)`. Counting all
generator matrices modulo `GL(r,2)`, all affine cosets, and all `t`, then
union-bounding proves that no affine flat of dimension at least
`8 ceil(log2 q)` is contained in the fiber except with probability
`2^-Omega(q log q)`.

The full fiber has `2^(q+O(1))` points with overwhelming probability, so every
support-contained cancellation-free affine/stabilizer cover needs
`2^(q-O(log q))` pieces. The union is already over every affine flat, so the
transform may be chosen after seeing all labels and the target. Three exact
modular-kernel controls and four scaling records pass; the affected
affine-flat/adaptive-layout/fiber-moment chain passed **29 tests** in 11.71
seconds. The live artifact is
`research/phase_workbench/dcp_linear_reparameterization_affine_flat_no_go.json`.

Do not broaden this result. It does **not** prove high Schmidt rank across all
linear splits, stabilizer rank when amplitudes may cancel, a nonlinear-
tensorization no-go, or a general circuit lower bound. The next hard target is
an approximate linear-split Schmidt bound that permits matrix cancellation, or
a constructive efficiently computable nonlinear coordinate map. Merely finding
another affine patch is closed.

### Compact CNOT Linear-Split Entanglement Boundary

`dcp_cnot_linear_split_entanglement_no_go.py` now supplies the missing
cancellation-aware extension for compact binary linear preprocessing. On any
row or column affine restriction, grouping equal parity features and choosing
an independent feature basis gives

`h(z)=sum_i b_i z_i+g(z) mod 2^q`,

with independent uniform `b_i` after conditioning on the arbitrary offset
function `g`. For each ordered distinct tuple, the equations over `(b,t)` are
an inhomogeneous linear system with the same homogeneous kernel as ordinary
subset sum. It is therefore either empty or a kernel coset, so the ordinary
growing factorial-moment bound dominates it term by term after target
averaging. For a side with `q+d` variables the corrected envelope is
`E[(X)_k] <= 2^(dk+1)`, not the unit-density shorthand `<=2` when `d>0`.

Unioning over every at-most-`G` CNOT sequence, every output-coordinate
bipartition, every row/column coset, and every target yields
`log_2 T=d+O((G log q+q)/k)`. The indicator amplitude matrix then obeys
`||M||^2 <= ||M||_1||M||_infinity <= T^2`, so retaining fixed Schmidt mass
`eta` needs rank at least `eta|F|/T^2`. Choosing an admissible
`k=o((q/log q)^(1/3))` closes every
`G=o(q^(4/3)/(log q)^(4/3))` family asymptotically, including matrix
cancellation and label/target-adaptive selection. Independent-target failure
`2^-3q` absorbs the planted likelihood ratio `<=2^q`.

The live artifact is
`research/phase_workbench/dcp_cnot_linear_split_entanglement_no_go.json`.
Its two exact offset controls, two exact Schmidt controls, and four asymptotic
records have zero failures; the focused/adjacent theorem chain passed **35
tests** in 9.30 seconds. The minimum instantiated Schmidt-rank exponent was
`0.56265` for the conservative `G=q`, `k=(q/log q)^(1/4)` schedule.

Do not broaden this theorem. Dense `Theta(q^2)` CNOT/`GL(m,2)` transforms,
nonlinear coordinate maps, unbalanced tensor-network contractions, general
circuits, and polynomial subset-sum decoding remain open. This is a
state-preparation/tensor-factorization obstruction, not a DCP time lower bound
or an algorithm. The next hard DCP question is whether dense all-`GL` splits
admit an explicit low-rank counterexample or a stronger uniform max-load/rank
theorem that avoids a `2^Theta(q^2)` family union bound.

## Authoritative Current State

- Branch: `main`.
- Do not commit frequently. The last known pushed commit before the current
  large research pass was `37915e74bb7ec9f69504381cbdab94f0e557323b`.
- The worktree contains a large coherent uncommitted research pass. Do not
  discard, reset, or rewrite it wholesale.
- User-owned deletions under `ag-remote/` must remain untouched.
- Latest registry validation: 8 candidates, 266 experiments, 391 results,
  639 negative results, 782 dequantization checks, and no registry issues.
- Latest theorem-focused physical-transfer/flag check: 20 tests passed in
  18.85 seconds.
- Latest equal-Gram/polar-chain check: 26 tests passed in 19.61 seconds.
- Latest shorted-metric/coefficient/transport theorem chain: 35 tests passed
  in 29.71 seconds.
- Latest common-core atomization plus dependency-homology check: 14 tests
  passed in 29.70 seconds.
- Latest pair-core recoupling-boundary check: 5 tests passed in 12.07 seconds.
- Latest sparse-parity/relative-Cech/augmented-Cech focused check: 18 tests
  passed in 17.17 seconds. The broader affected theorem check passed 31 of 32
  tests; its sole failure was a comparator that incorrectly allowed sign on
  empty patterns and was corrected before the 18-test rerun.
- Latest recursive pair-generation check: 4 tests passed in 46.73 seconds,
  including the complete 11,025-node S5 exhaustive boundary.
- Latest pair-quotient overlap check: 4 tests passed in 6.39 seconds.
- Expanded pair-quotient overlap check: 5 tests passed in 20.87 seconds after
  adding the 693-merge S6 Gram-factor screen.
- Latest carrier-factorization check: 10 tests passed in 2.72 seconds.
- Latest multistar-degree check: 8 tests passed in 16.37 seconds.
- Latest orientation-Laplacian-gap check: 10 tests passed in 14.92 seconds.
- Latest global-source mass/kernel check: 16 tests passed in 17.23 seconds.
- Latest vertex trivialization/groupoid check: 14 tests passed in 3.17
  seconds; the broader vertex/Laplacian/carrier regression passed 28 tests in
  23.21 seconds.
- Latest graded flat-transport obstruction/rescue check: 20 tests passed in
  0.19 seconds; the combined vertex/graded focused chain passed 22 tests in
  3.13 seconds before the rescue module was added.
- Latest relation-cokernel/augmented-H0/hierarchical-cokernel/graded-trim
  regression: 25 tests passed in 68.80 seconds.
- Latest sibling-frame/word-map/event-transfer/trace-burden regression: 26
  tests passed in 14.67 seconds. The new trace-burden artifact was then
  generated successfully with zero exact-control failures.
- Latest regular-master/trace-burden regression: 11 tests passed in 5.16
  seconds. The regular-master artifact has maximum spectral residual
  `1.34e-15` and zero finite-control failures.
- Latest final-root natural common-span theorem check: 6 tests passed in 3.85
  seconds. The live artifact proves asymptotic common relative rank
  `19/128-o(1)` on globally distinct conditional mass `1/9-o(1)`, child
  fiber aspect `19/520-o(1)`, and component block ratio at most
  `(520/19+o(1))/q`. The natural positive component edge remains open.
- Latest component-defect rank/mass theorem check: 6 tests passed in 1.05
  seconds. The live artifact proves the nonscalarity defect has relative
  common-fiber rank `1-(520/19+o(1))/q` on the same source event and
  conditioned expected physical support mass at least `19/1152-o(1)`, without
  assuming a positive component eigenvalue edge.
- Latest component-POVM spectral-trim check: 5 tests passed in 1.07 seconds.
  The live artifact proves failure at most `kappa tau B/r` for input flatness
  `kappa=r||rho||_infinity` and component rank budget `B`, while a concentrated
  finite control has unit loss. Natural polynomial input flatness and coherent
  threshold/support access remain open.
- Latest component-effect algebra boundary check: 4 tests passed in 1.11
  seconds. An orthogonal PVM has full-rank nonscalarity defect but zero
  commutator defect, while the trine POVM generates the full qubit algebra.
  Natural noncommutative effect-algebra source and physical mass are unproved.
- Latest natural leaf-commutator theorem check: 8 tests passed in 1.18
  seconds. Density-one balanced natural orientation pairs have commutator norm
  at least `sqrt(1-(n-1)^-2)/(n-1)` after global-distinct transfer. Transfer
  through canonical frame whitening/common-span compression remains open.
- Latest leaf-whitening commutator no-go check: 8 tests passed in 0.40
  seconds. An exact duplicate-free rank-two projection-frame family has frame
  condition number below three, constant total-rank aspect, full-rank
  nonscalarity with edge tending to `1/2`, and density-one inverse-linear leaf
  commutators, yet all canonical whitened effects commute. The exact commuting
  full-support criterion is an integer-degree independent-set cover in a
  simultaneous effect eigenbasis; every nonzero commuting-effect eigenvalue
  is reciprocal to a positive integer. Proper sibling common-span compression
  is outside that criterion.
- Latest common-span component universality no-go check: 9 tests passed in
  1.06 seconds. Naimark dilation proves every POVM is realizable by the actual
  compressed canonical formula. A structured family simultaneously has common
  relative rank `1/3`, total-rank aspect four, relative leaf rank `4/k`, frame
  condition below four, density-one inverse-linear leaf commutators, component
  edge `1/3`, and nonscalarity edge tending to `5/9`, yet its compressed
  components commute and contain the non-reciprocal eigenvalue `2/3`. This is
  a generic no-go, not a natural wreath commutativity theorem.
- Latest component commutator trace-mass bridge check: 10 tests passed in
  0.24 seconds. For one child POVM,
  `Tr(D_com)=Tr((sum_e H_e^2)^2)-sum_(e,f)Tr(H_eH_fH_eH_f)` exactly,
  `Tr(D_com)<=r`, and `D_com<=2I`. Hence a physically normalized regular-
  master scalar fourth-moment mass `M_4` implies both physical commutator-
  support mass and source-block noncommutativity probability at least `M_4/2`,
  without a component edge or center-valued rank law. Positivity of natural
  compressed `M_4` remains unproved.
- Latest component commutator Haar benchmark check: 10 tests passed in 0.13
  seconds. The complete `S_4` unitary-Weingarten contraction gives
  `E Tr(D_com)/r=(N-b)(N-2b)(N-r)(r^2-1)/[N(N-2)(N-1)(N+1)(N+2)]`.
  At `r/N->alpha` and sparse `b/N->0`, this tends to
  `alpha^2(1-alpha)`. At `alpha=19/520` the benchmark is about `0.0012863`;
  after the proved event/common-rank constants it suggests physical support
  around `1.06e-5`. This is explicitly Haar/Jacobi surrogate scale, not
  natural wreath evidence.
- Latest central-support/rank-bridge chain: 17 tests passed in 8.18 seconds;
  both live artifacts regenerated with zero finite-control failures.
- Latest subgroup-walk/affine-outlier/pair-angle/central-support chain: 31 tests
  passed in 8.98 seconds. The subgroup-walk Fourier spectrum matches its full
  `S_3` regular control, all 2,592 gauge transitions pass, and both new affine
  subgroup artifacts have zero finite-control failures.
- Latest local-transversality/Kronecker/Hamming-rank chain: 25 tests passed in
  13.81 seconds. It proves the independent-Plancherel Hamming-three support
  transition and fixed-pair rank scale, while leaving coherent incidence and
  the complete node-frame edge explicitly open.
- Latest natural pair-carrier law check: 5 tests passed in 1.03 seconds. The
  exact annealed carrier law, all even overlap moments, weighted-L1 quenched
  concentration argument, and low-dimensional mass bounds pass; the live
  artifact's `n=32` quadratic-dimension mass is about `2^-188.75`. The simple
  three-factor Markov/TV bound remains numerically loose at `n=32`, so it is
  an asymptotic theorem rather than a strong finite guarantee.
- Latest pair-carrier/return-walk chain: 10 tests passed in 1.37 seconds. The
  all-order two-color count is now an exact convolution return probability,
  the source-only generated-subgroup formula passes complete `S_2/S_3`
  controls, and the regular `S_3,K=2` walk has a verified nonstationary
  eigenvalue `3/4`, explicitly falsifying a coarse-global-gap route.
- Latest pair-support/carrier/return/hierarchy-rank theorem chain: 41 tests
  passed in 18.83 seconds. The new hierarchy exact-common rank module passed
  its 5 focused tests in 4.90 seconds.
- Latest hierarchy low-carrier trim check: 5 tests passed in 10.16 seconds.
  At `n=48` it trims all pair carriers through dimension about `2^33.57`
  with conditioned all-target rank budget about `2^-16.91`; surviving pair
  correlations are at most `2^-33.57`.
- Latest complete low-dimensional S6 vertex-channel audit: 3 tests passed in
  17.39 seconds. It exhausts 1,155 globally distinct portfolios and 64
  high-degree vertices; all 16 nonorthogonal components are positive flat
  affine triangles.
- Latest scalar affine-plane holonomy check: 3 tests passed in 0.13 seconds.
  Latest affine-plane support-pressure no-go check: 4 tests passed in 5.29
  seconds. At `n=48` the exact support-demand/capacity ratio is about
  `2^179.13`, so orthogonal plane atomization is asymptotically impossible.
- Latest signed-Steiner theorem chain: 31 focused tests passed across the
  incidence boundary, gauge homology, random-gauge surrogate, sharp nullity,
  deterministic scalar bulk edge, operator bulk reduction, and coverage
  Welch-pressure modules. Individual checks passed 4, 4, 5, 4, 5, 4, and 5
  tests respectively.
- Latest physical trace-weighted PGM bridge/access-boundary chain: 18 focused
  tests passed in 0.85 seconds. The physical sector average is exactly the
  rescaled orientation-frame trace state; raw PGM eigenvalues are smaller by
  the orientation width, so a cutoff `tau` on the orientation frame means
  `tau/2^k` on the raw physical frame. The flat-frame control proves generic
  normalized analysis still costs `Theta(sqrt(2^k))` even with no hard edge.
- Latest conditional native pair-mass check: 5 tests passed in 5.93 seconds;
  the broader pair/access regression passed 21 tests. The natural `d_alpha^4`
  multiplicity law is exactly conditional active pair-frame trace mass, but
  normalized cross-overlap QSVT remains superpolynomial on that mass.
- Latest GPE direct pair-polar and holonomy reduction check: 15 focused tests
  passed in 6.04 seconds. Coherent generalized phase estimation exports the
  canonical carrier row while preserving unknown Kronecker multiplicities,
  giving a polynomial exact pair-polar transport. Fundamental-cycle products
  are therefore executable without dense Racah matrices; a natural
  inverse-polynomial holonomy gap and recursive child-span coverage remain
  open.
- Latest recursive-node GPE compiler check: 28 focused tests passed in 13.45
  seconds. The normalized parent relation now has an exact two-part circuit
  normal form: normalized minimum-energy child embeddings plus a short-metric
  endpoint mixer. Equal child short metrics make the mixer exactly a signed
  Hadamard. Flat affine child embeddings prepare in affine dimension many GPE
  transport stages with no square-root width penalty. All three selected
  W3/W5 affine controls compile through the finite pair-path/GPE chain, while
  a noncommuting metric control requires a genuine matrix-valued mixer and a
  metric-ratio counterfamily keeps an exponentially small endpoint gap even
  when pair GPE is available.
- Latest partial-support child-embedding check: 27 affected focused tests
  passed in 47.41 seconds. A sparse leaf-Gram reconstruction exposes a
  globally source-distinct S6 affine plane with a 34-dimensional common span
  but nonscalar component effects. The left child splits into rank-9 and
  rank-25 projector channels; the right has a rank-9 `1/178` effect and a
  full-rank complement. Cross-child effect commutator norm is exactly
  `1/356`, and endpoint spectra are `81/170,1/2,9/17` versus
  `8/17,1/2,89/170`. This falsifies universal scalar affine fibers. The
  surviving recursive target is a matrix-valued partial-support sheaf, whose
  coherent GPE compiler and positive native-mass theorem are open.
- Latest partial-support source-mass check: 13 focused tests passed in 21.31
  seconds. The direct S6 conjugate-chain mechanism requires both trivial and
  sign source irreps. For `m=2 ceil(log2 n!)` independent Plancherel sources,
  its probability is at most `m(m-1)/(n!)^2`; any source of dimension at most
  `L` has union mass at most `m p(n)L^2/n!`. Global-distinct conditioning only
  divides by a probability tending to one. At `n=48`, the conditioned direct
  S6 bound is about `2^-362.06`, and the bound for any `n^4`-dimensional anchor
  is about `2^-105.93`. The known S6 mechanism is physically negligible; only
  high-dimensional-source matrix partial supports remain relevant.
- Latest matrix-POVM recursive compiler check: 18 focused tests passed in
  21.50 seconds. Every normalized child embedding factors exactly as a
  component POVM Naimark dilation `sum_e |e>sqrt(H_e)` followed by component
  partial isometries. The parent relation is an endpoint two-outcome POVM,
  then the child POVM, then GPE-compatible support transport. Noncommuting
  trine effects pass exactly, and no intrinsic square-root outcome-count loss
  appears. Generic bounded-polynomial access to `sqrt(H_e)` has degree
  `Omega(delta^-1/4)` at minimum effect eigenvalue `delta`; at `delta=2^-512`
  the recorded lower-bound log degree is `127.21`. This premise cannot be
  inferred from a small component trace: the sparse-support companion below
  gives rare low-rank effects with a constant positive edge. Natural effect-
  POVM dilation, all-depth GPE support compatibility, and high-dimensional
  native mass remain open.
- Latest component-POVM sparse-support boundary: 5 focused tests passed in
  0.15 seconds. For a Haar isometry `W:C^r->C^N` and coordinate block of
  aspect `beta`, the exact generic zero/one atoms and free-Jacobi edges show
  that as `beta->0` at fixed `alpha=r/N`, positive eigenvalues converge to
  `alpha` while support-rank and trace fractions are `beta/alpha` and `beta`.
  Therefore rare outcomes do not by themselves trigger the generic square-
  root-QSVT obstruction. Natural Jacobi universality and coherent support
  SELECT remain unproved.
- Latest component-effect regular-master reduction: 4 focused tests passed in
  0.70 seconds. Canonical child effects are spectral-calculus expressions in
  regular-master orientation projectors. Matrix-effect source probability is
  a source-center support trace; physical common-span mass is its common-space
  cutdown; ordinary defect trace can be smaller still. The S3 control gives
  exact masses `16/81`, `5/81`, and `2/81`, respectively, but has repeated
  sources and no asymptotic force. A high-dimensional center-valued local law
  is now the precise missing mass theorem.
- Latest corrected MRS model-scope check: 5 focused tests passed in 0.11
  seconds. `M=Delta(M)` characterizes only invariance under early projective
  transcript measurement. Classical use of a projective transcript requires
  the stronger block-scalar condition `M=C(M)`. A four-dimensional control is
  dephasing invariant but violates the latter, proving that off-diagonal
  coherence is sufficient but not necessary for transcript-only separation.
  The full adaptive MRS transcript is a sequential POVM `{E_t}`; a physical
  separation must put the PGM effect outside `{sum_t f_t E_t: 0<=f_t<=1}` on
  nonnegligible accepted mass. No such separation is proved, so the MRS gate
  remains closed.
- Latest MRS transcript-POVM separation check: 5 focused tests passed in 0.65
  seconds. For any specified adaptive transcript POVM `{E_t}`, transcript-only
  binary effects form the zonotope `{sum_t f_t E_t:0<=f_t<=1}`. Box-constrained
  projection gives an exact membership test and its normalized residual gives
  a dual separation witness. A two-stage adaptive Kraus control compiles
  exactly. The physical PGM effect, its transcript POVM, and separation from
  every allowed MRS policy are still absent.
- Latest weighted affine-relation bulk check: 7 focused tests passed in 6.44
  seconds, including exact comparison with the physical star-spectrum engine.
  The combined weighted-bulk/relation-cokernel regression passed 12 tests.
  Five finite collision-free rows certify beginning at `n=32`; at `n=48`
  the conditioned burden/capacity ratio is below `2^-170.97` and the fixed
  relation-window coefficient outlier-rank bound is below `7.4e-26`.
- The relation-cokernel theorem resolves the old state-mass-transfer gate:
  every pair-relation direction has exactly zero ideal PGM polar amplitude.
- Direct pair-common Cech completeness is asymptotically falsified, but
  recursive child-span relations are information-theoretically complete. An
  exact constant-arity polar chain now bypasses pairwise pseudoinverse-frame
  comparability as a mandatory identity. The active gates are a natural
  independent-source all-depth node-frame spectral event and tightly
  normalized coherent node-frame/root access.
- The carrier-factorization and multistar-degree modules are now fully wired
  (registry seed, `qsearch.py` subcommand, runner dispatch, clean-registry
  dispatch tests, README, Sellke literature record). The Laplacian-gap module
  below is **not** wired yet; that is queued mechanical work.
- Latest affected-theorem regression (recoupling boundary, atomization, pair
  angles, triple range, pair-quotient overlap): 30 tests passed in 35.82
  seconds.
- `python -m compileall -q .`, `node --check site/progress.js`, and
  `git diff --check` are clean as of this pass.
- The newest theorem artifacts contain one globally distinct S6 full-merge
  counterexample to universal half-balance. Any older summary saying all
  collision-free S6 merges were neutral is superseded by the sections below.
- The registry counts above predate the newest theorem-only modules. Routine
  registry/CLI refresh is intentionally queued for Gemini rather than charged
  to the high-reasoning pass.
- Root `index.js` no longer exists; the active UI script is
  `site/progress.js`, and `node --check site/progress.js` passes.

## Latest Mathematical Results

### Physical PGM Bridge, Generic Access Boundary, And Direct GPE Escape

Files:

- `self_dual_wreath_trace_weighted_pgm_bridge.py`
- `self_dual_wreath_native_frame_access_boundary.py`
- `self_dual_wreath_pair_transport_native_mass_boundary.py`
- `self_dual_wreath_gpe_pair_polar_transport.py`
- `self_dual_wreath_gpe_holonomy_resolver_reduction.py`
- matching JSON artifacts and focused tests.

For one physical Fourier sector, let `R` be the stacked orientation analysis,
`S=R^*R`, `w=2^k`, and let `C` be the row-copy intertwiner. The physical
analysis is `A=w^-1/2 R^* C` and `CC^*R=R`, hence

`AA^*=S/w`.

The exact physical PGM coisometry is `Q^*C`, where `Q=R S^-1/2`. Truncating
the rescaled orientation frame at `tau` gives physical average failure exactly

`tr[S 1_(0,tau)(S)]/tr(S)`.

This closes the old state-mass-transfer caveat: normalized trace weighting is
the physical PGM sector average, not an abstract surrogate. It also enforces a
scale correction that must not be lost: the corresponding raw PGM cutoff is
`tau/w`, not `tau`.

The bridge does not supply tight access. For retained frame eigenvalues
`lambda_i`, generic normalized analysis has good probability

`a^2=sum_i lambda_i^2/(w sum_i lambda_i)`.

Ozols--Roetteler--Roland water filling gives exact-fidelity conversion scale
`sqrt(w/lambda_min)`, while the variable-time RMS inverse-singular scale is
`sqrt(w rank(S)/tr(S))`. The flat control `S=I` has no low mode to trim but
still costs `Theta(sqrt(w))`. Therefore hard-edge control and trace truncation
cannot make generic PREPARE/SELECT/QSVT access polynomial. This is an access-
model boundary, not an arbitrary-circuit lower bound.

For two orientation projectors `E,F`, each active Jordan channel has
`tr((E+F)|channel)=2`, including a common channel. Conditional active
pair-frame trace mass is therefore exactly principal-angle multiplicity mass.
The natural law transfers to `q4(alpha)=d_alpha^4/Z4`, and

`q4[d_alpha<=L] <= p(n)^2 L^4/(n!)^2`.

Since the pair correlation is `1/d_alpha`, normalized cross-overlap QSVT has
superpolynomial branchwise degree on natural active mass. This obstruction is
real but not fundamental.

The direct polar is entanglement reassociation. In a carrier `alpha`,

`E F = (1/d_alpha) U_alpha`,

where `U_alpha` maps
`|i>_a |Omega_alpha>_(0,b)` to
`|Omega_alpha>_(0,a) |i>_b` and preserves every multiplicity label.
Coherent generalized nonabelian phase estimation acts as

`|alpha,j,i> -> d_alpha^-1/2 sum_t |alpha,i,t> |alpha,j,t>`.

Apply this GPE to blocks `0,a,b`, equality-control on their irrep labels, swap
the exported row registers of `a,b`, and uncompute. Beals' `S_n` QFT plus
sparse Young-orthogonal adjacent-transposition actions makes the circuit
polynomial with no `1/d_alpha` amplification and no full Kronecker transform.
Pair transport is therefore resolved and must not be listed as the main
bottleneck again.

Different pair edges regroup tensor factors differently, so GPE does not kill
Racah holonomy. It makes it executable. On one flat equal-rank channel, choose
a spanning tree with root transports `T_v`; each non-tree edge gives

`H_e=T_v^* U_(v<-u) T_u`.

The connection-Laplacian kernel is exactly the simultaneous `+1` fixed space
of these fundamental holonomies. Hence a coherently selectable generator
family with inverse-polynomial frustration gap would yield a polynomial
fixed-space resolver. A succinct near-identity rotation has exponentially
small gap, so efficient edge circuits alone do not prove this. Partial
supports, emergent child-span dependencies, and complete relative-frame
whitening remain outside the theorem. No decoder or speedup is claimed.

### Recursive Child-Span Compiler Normal Form

Files:

- `self_dual_wreath_gpe_recursive_node_compiler.py`
- `research/representation/self_dual_wreath_gpe_recursive_node_compiler.json`
- `tests/test_self_dual_wreath_gpe_recursive_node_compiler.py`

For a parent common-span isometry `X`, child syntheses `S_L,S_R`, and

`A_s=X^*(S_sS_s^*)^+X`, `M=A_L+A_R`,

define the normalized minimum-energy child embeddings

`W_s=S_s^+X A_s^-1/2`.

The normalized recursive relation is exactly

`[W_L A_L^1/2 M^-1/2; -W_R A_R^1/2 M^-1/2]`.

This separates child-fiber preparation from endpoint conditioning. If
`A_L=A_R`, the endpoint mixer is exactly `I/sqrt(2)` on each side. If the
metrics do not commute, even constant spectral comparability can require a
matrix-valued rotation. Pair GPE does not remove that operation. If the
normalized child embedding instead has a flat affine form

`|A|^-1/2 sum_(x in A)|x>V_x`,

affine Hadamards plus the transports `V_(x+g)V_x^*` prepare it in `dim(A)`
transport stages. The companion direct-GPE theorem compiles compatible pair
polar edges without inverse carrier-dimension amplification. This closes the
finite W3/W5 generator-transport objection, not the all-n theorem: structured
child fibers, compact reversible generator SELECT, matrix holonomy, and a
natural endpoint gap on positive PGM mass remain open.

### Natural Scalar-Affine Falsifier And Partial Supports

Files:

- `self_dual_wreath_partial_support_child_embedding.py`
- `research/representation/self_dual_wreath_partial_support_child_embedding.json`
- `tests/test_self_dual_wreath_partial_support_child_embedding.py`

The child embeddings can be reconstructed from the sparse leaf block Gram.
If `Z=(Z_L,Z_R)` is an orthonormal cross-dependency basis, orthonormalize the
common physical image and form the normalized minimum-energy embeddings
`W_L,W_R`. Their mask effects

`H_(s,e)=W_(s,e)^*W_(s,e)`

are positive and sum to identity for each child. The scalar affine compiler
requires each active `H_(s,e)=w_e I` on the full common fiber.

The globally source-distinct S6 node with masks `{2,5,11,12}` falsifies this
condition while retaining affine mask support. Its 34-dimensional left child
effects are complementary rank-9/rank-25 projections. The right mask-11
effect is `1/178` on a rank-9 support; mask 12 is full rank with eigenvalues
`177/178` and `1`. A cross-child effect commutator has norm `1/356`. The short
metrics themselves commute, proving that endpoint diagonalization does not
remove mask-resolved matrix traffic.

Do not pursue a universal scalar coefficient-affine theorem again. The live
target is a matrix partial-support sheaf: coherent support/eigenchannel SELECT,
compatible GPE transports, the matrix endpoint mixer, and holonomy filtering.
The finite S6 obstruction is not yet known to carry positive asymptotic native
PGM mass, so it does not kill the collective route.

### Low-Dimensional Partial-Support Source Mass Is Negligible

Files:

- `self_dual_wreath_partial_support_source_mass_boundary.py`
- `research/representation/self_dual_wreath_partial_support_source_mass_boundary.json`
- `tests/test_self_dual_wreath_partial_support_source_mass_boundary.py`

For `m` independent Plancherel source partitions,

`Pr[min_i d_(lambda_i)<=L] <= m p(n)L^2/n!`.

The direct S6 conjugate-chain construction specifically needs both trivial and
sign, so its probability is at most

`m(m-1)/(n!)^2`.

After conditioning on global distinctness, divide by `P_cf`; the exact
collision-free theorem has `P_cf->1` at information-threshold copy count.
Stirling plus Hardy--Ramanujan therefore makes every polynomial-dimensional
anchor event `n^-omega(1)`. The direct S6 mechanism cannot have positive
natural source mass despite being a valid universal counterexample.

This does not establish scalar affine behavior on the physical bulk. The only
relevant unresolved obstruction is a nonscalar component POVM generated
entirely by typical high-dimensional source irreps. Future screens or theorems
must exclude low-dimensional anchors before being treated as evidence.

### Matrix-POVM Recursive Compiler Normal Form

Files:

- `self_dual_wreath_matrix_povm_recursive_compiler.py`
- `research/representation/self_dual_wreath_matrix_povm_recursive_compiler.json`
- `tests/test_self_dual_wreath_matrix_povm_recursive_compiler.py`

For any normalized child embedding `W` with components `W_e`, define

`H_e=W_e^*W_e`, so `sum_e H_e=I`.

Component polar decomposition gives `W_e=V_e sqrt(H_e)`. Therefore the exact
child compiler is a coherent POVM Naimark dilation

`|psi> -> sum_e |e>sqrt(H_e)|psi>`

followed by controlled partial isometries `V_e`. The recursive endpoint mixer
is itself a two-outcome POVM with Kraus operators
`C_s=A_s^1/2(A_L+A_R)^-1/2`. An arbitrary parent relation is therefore:

1. endpoint POVM dilation;
2. selected child component-POVM dilation;
3. controlled support polar, using GPE when the support channel is compatible.

This works algebraically for noncommuting effects and has no intrinsic
`sqrt(number of outcomes)` loss. It does not give a generic circuit. If a
bounded polynomial approximates `sqrt(x)` down to effect edge `delta`, the
mean-value theorem plus Markov inequality gives degree
`Omega(delta^-1/4)`. Thus a representation-specific direct Naimark transform
or inverse-polynomial natural effect edge is required only if the positive
edge is actually small. Component trace and outcome probability do not prove
that premise. Pair GPE solves only step 3.

### Sparse-Support Component-POVM Boundary

Files:

- `self_dual_wreath_component_povm_sparse_support_boundary.py`
- `research/representation/self_dual_wreath_component_povm_sparse_support_boundary.json`
- `tests/test_self_dual_wreath_component_povm_sparse_support_boundary.py`

For a Haar isometry `W:C^r->C^N`, coordinate projector `P_e` of rank `b`,
`alpha=r/N`, and `beta=b/N`, the component effect `H_e=W^*P_eW` has generic
atom multiplicities

`mult_0=max(r-b,0)`, `mult_1=max(r+b-N,0)`

and free-Jacobi fractional edges

`lambda_+-=(sqrt((1-alpha)beta) +- sqrt(alpha(1-beta)))^2`.

As `beta->0` at fixed `alpha`, both edges converge to `alpha`, their width is
exactly `4sqrt(alpha(1-alpha)beta(1-beta))`, support-rank fraction is
`beta/alpha`, and trace fraction is `beta`. Thus a many-outcome effect may be
approximately `alpha` times a tiny-rank support projector. The plausible
natural compiler target is coherent support-projector SELECT plus GPE support
transport, not generic approximation of `sqrt(x)` at an assumed exponentially
small positive eigenvalue.

This is a Haar benchmark only. The natural Plancherel/Racah child embedding
may have arithmetic outliers, non-Haar alignment, or hard edges. Required
theorems are natural block-aspect identification, mixed trace/Jacobi
universality, operator-norm edge rigidity on positive accepted mass, and
all-depth error composition.

### Component-Effect Regular-Master Reduction

Files:

- `self_dual_wreath_component_povm_regular_master_reduction.py`
- `research/representation/self_dual_wreath_component_povm_regular_master_reduction.json`
- `tests/test_self_dual_wreath_component_povm_regular_master_reduction.py`

The canonical full-domain synthesis gives, on a common-span isometry `X`,

`A_s=X^*F_s^+X`,

`H_(s,e)=A_s^-1/2 X^*F_s^+ E_e F_s^+ X A_s^-1/2`.

This equals the leaf-coefficient effect and is built entirely from sums,
products, support/intersection spectral projections, pseudoinverses, and
compressed inverse square roots. It therefore preserves the regular-master
source decomposition. For the positive nonscalarity defect

`D_Lambda=sum_(s,e)(H_(s,e)-tr(H_(s,e))/r_Lambda I)^2`,

three measures are different: source-center support probability, its physical
common-span cutdown, and ordinary normalized defect trace. The exact repeated-
source S3 control gives `16/81`, `5/81`, and `2/81`. Consequently scalar
moments cannot prove negligible matrix-effect block probability without a
relative-rank theorem or center-valued local law.

Do not infer that removing low-dimensional source labels removes low-
dimensional internal carriers; tensor products of high-dimensional sources
can contain trivial/sign sectors. The required asymptotic cut and estimate
must occur in the master center/internal-carrier decomposition itself.

### Exact MRS Transcript Criteria

Files:

- `self_dual_wreath_mrs_coherence_escape_criterion.py`
- `research/representation/self_dual_wreath_mrs_coherence_escape_criterion.json`
- `tests/test_self_dual_wreath_mrs_coherence_escape_criterion.py`

Primary source: Moore, Russell, and Sniady,
`https://arxiv.org/abs/quant-ph/0612089`, especially Section 3.

Their sieve weakly Fourier samples every source and repeatedly measures an
irrep in a selected pair's tensor-product decomposition. Inputs are destroyed,
and the classical irrep-labeled forest transcript is the algorithm's usable
information. For transcript projectors `{P_t}`, define

`Delta(X)=sum_t P_t X P_t`.

For final decision effect `M` and state `rho`,

`tr(M rho)-tr(M Delta(rho))=tr((M-Delta(M))rho)`.

Thus deferring measurements changes nothing for every input iff
`M=Delta(M)`. This is not the criterion for simulation from the classical
transcript. Define the block-scalar conditional expectation

`C(M)=sum_t tr(P_t M)/tr(P_t) P_t`.

For a projective transcript, the output depends only on the classical block
probabilities for every input iff `M=C(M)`. Hence an off-diagonal block is a
sufficient but not necessary separation witness: a block-diagonal effect that
is nonscalar within one isotypic block also uses information absent from the
classical label. The exact finite control has `M=Delta(M)` but
`||M-C(M)||=1/2` and changes the transcript-only probability by `1/2`.

The adaptive MRS process is more general than one fixed projective transcript.
If `{E_t}` is its complete sequential transcript POVM, every binary decision
obtainable by classical transcript postprocessing has effect
`sum_t f_t E_t`, `0<=f_t<=1`. A formal physical escape must separate the PGM
decision effect from this entire set on nonnegligible accepted-state mass.
Pair GPE alone is carrier-label block diagonal and proves neither an
off-diagonal nor a within-block/full-POVM witness.

The companion files
`self_dual_wreath_mrs_transcript_povm_separation.py` and
`research/representation/self_dual_wreath_mrs_transcript_povm_separation.json`
make this criterion executable for any specified `{E_t}`. The effect set is a
box-constrained zonotope; Hilbert--Schmidt projection supplies exact membership
and the normalized residual supplies a support-function dual witness. The
module also compiles two-stage adaptive Kraus trees into terminal transcript
effects. It does not optimize over all allowed MRS policies.

Do not claim the architecture is outside MRS merely because it is described as
globally coherent. Either produce the transcript-dephasing witness after the
complete circuit is specified, produce a within-block witness, or directly
separate the decision effect from all classical postprocessings of the adaptive
transcript POVM. Otherwise prove a simulation into the measured sieve class.
Even a valid separation would avoid only this lower-bound model; it would not
prove efficiency, correctness, classical hardness, or speedup.

### Sibling Frames, Mixed-Arity Polar Schedule, And Trace Burden

Files:

- `self_dual_wreath_sibling_frame_mp_moments.py`
- `self_dual_wreath_sibling_frame_jacobi_surrogate.py`
- `self_dual_wreath_sibling_frame_joint_freeness.py`
- `self_dual_wreath_sibling_frame_joint_conditioning_surrogate.py`
- `self_dual_wreath_sibling_word_map_normal_form.py`
- `self_dual_wreath_multiscale_polar_schedule.py`
- `self_dual_wreath_trace_polynomial_edge_burden.py`
- matching JSON artifacts and focused tests.

For independent Plancherel source labels, the sibling child frame
`A=sum_(e:e_j=0) E_e` has exact normalized moments through order four. They
converge to the first four Marchenko--Pastur moments at aspect
`alpha=2^(K-1)/|G|`. The exact identities also falsify scalar concentration:

`E||A-alpha I||_F^2/D=alpha(1-1/|G|)` and
`E||A-B||_F^2/D=2alpha(1-1/|G|)`.

Sibling exchangeability therefore does not make the frames samplewise equal.
Exact mixed moments prove independent-source freeness through total degree
four, uniformly in the target dimension. More generally, every mixed binary
word `w` has the exact normal form

`E tr(w(A,B))/D = |G|^-p sum_x I_w(x)[chi_nu(prod x)/d_nu]q_p(x)^(K-1)`.

The two split constraints reduce exact enumeration from `|G|^p` to
`|G|^(p-2)`. This is the right growing-word object, but finite screens through
degree six are not asymptotic evidence.

For the Gaussian benchmark `A=XX*`, `B=YY*`, with `X,Y` of size `D x m` and
`alpha=m/D>1/2`, the finite row-projector reduction is exact. When
`alpha<1`, there are `D-m` zero eigenvalues, `D-m` one eigenvalues, and
`2m-D` fractional eigenvalues. Passing to the row-space complement gives the
effective full-rank Jacobi parameter `alpha/(2alpha-1)`. In both singular and
full-rank regimes the limiting fractional support is

`lambda_+-=(1+-sqrt(2alpha-1))^2/(4alpha)`.

This corrects the tempting but wrong direct substitution of `alpha<1` into a
full-rank MANOVA law. The adaptive `K/K+1` schedule gives only a relative
top-split Jacobi gap, uniformly at least

`(3-2sqrt(2))/6 = 0.0285954792...`.

It does not control the parent hard edge. `K+2` copies put the selected top
split at child aspect `[2,4)`, but a binary all-depth tree still crosses the MP
hard edge. The exact multiway polar identity

`Q_T=(direct_sum_i Q_i) col_i(S_i^(1/2)) S_T^(-1/2)`

allows a mixed schedule: binary levels through `K-2`, one eight-way merge to
`K+1`, and one final binary merge to `K+2`. Its Gaussian-surrogate aspects are
`<=1/2`, `[2,4)`, and `[4,8)`, giving all-depth nonzero edge floor
`3/2-sqrt(2)` and support condition upper `17+12sqrt(2)`. This proves neither
the natural edge nor coherent access; naive width-normalized LCU can erase the
physical gap.

The normalized-trace route is much harder than the old handoff stated. With
probability at least one half, the natural target carrier obeys
`log D = Theta((log |G|)^2)` by an elementary Plancherel dimension tail.
Chebyshev extremality therefore forces interval-uniform trace-polynomial
degree `Theta((log |G|)^2)` to detect one outlier. At `n=48`, `K=205`, and 25
percent slack, the typical-carrier burden is at least 13,094 degrees for the
upper edge and 72,449 for the lower edge, even optimistically assuming the
positive support is known. Fixed words and `O(log |G|)` words are cut as
generic edge-proof strategies. This is not a natural-frame no-go: a
law-specific local law, operator-valued concentration, deterministic
no-outlier theorem, or exact multiplicity reduction could bypass the
interval-uniform trace penalty.

### Regular Master Lift And Central-Support Local-Law Target

Files:

- `self_dual_wreath_regular_master_central_support.py`
- matching JSON artifact and focused tests.

Replace every source slot by the left regular representation and define the
same orientation invariant projectors. Fourier decomposition gives the exact
block identity

`A_reg = direct_sum_Lambda A_Lambda tensor I_(product_j d_Lambda_j)`.

Therefore normalized regular trace is exactly product-Plancherel expectation
of normalized physical-block trace for every polynomial. This is a fixed
group-register operator, not another surrogate.

The desired edge event is not its ordinary bad spectral mass. If
`Q_B=1_B(A_reg)` and `c_Z` is central support in the source-label block center,
then

`Pr_Lambda[spec(A_Lambda) intersects B] = tr_reg c_Z(Q_B)`.

Ordinary moments see only
`tr_reg Q_B=E rank(Q_(B,Lambda))/dim(H_Lambda)`. The exact `S_3`
standard-target control has bad-block probability `4/9` but scalar bad
spectral mass `1/9`. More importantly, dilution survives the physical source
condition: an exact globally distinct `S_4`, two-copy root control has
conditional bad-block probability `54/89`, scalar mass `10/267`, and ratio
`81/5`.
This makes the missing theorem precise: prove a center-valued local law, bound
the Plancherel trace of bad central support directly, or prove every bad
projection has nonnegligible relative rank. The regular master norm itself is
a worst-block norm and can be set by negligible sectors. The lift does not
provide tightly normalized coherent access to a width-`w` node sum.

### Relative-Rank Bridge And Symmetry No-Go

Files:

- `self_dual_wreath_central_support_rank_bridge.py`
- matching JSON artifact and focused tests.

If every nonzero bad block projection has relative rank at least `r_min`, then

`Pr[bad block] <= scalar bad spectral mass/r_min`.

This is the highest-leverage possible bypass currently visible. A natural
bound `r_min>=|G|^-c` for fixed `c` changes the interval-uniform polynomial
degree from `Theta((log |G|)^2)` to `O(log |G|)`. At `n=48`, `c=1`, the
upper/lower burdens become 167/921 instead of 13,094/72,449.

The premise is not proved. Every node frame commutes with the global diagonal
`S_n` action, but Schur form is only

`A=direct_sum_alpha I_(d_alpha) tensor M_alpha`.

Trivial and sign sectors have `d_alpha=1`, while their multiplicity operators
can be large. A globally distinct `S_4` control has trivial and sign
multiplicity two and admits rank-one commutant projections of relative rank
`1/54<1/24`. Thus global covariance cannot prove even a `1/|G|` floor.
Pursue a natural relative-rank theorem only through the specific
subgroup-projector sum or source typicality; otherwise attack central support
directly.

### Subgroup-Projection Walk And Affine Common-Outlier Exclusion

Files:

- `self_dual_wreath_subgroup_projection_walk.py`
- `self_dual_wreath_affine_node_common_outlier.py`
- matching JSON artifacts and focused tests.

After lifting target and sources to regular representations, every orientation
projector is uniform averaging over a diagonal subgroup `H_e` of
`S_n^(2K+1)`. A normalized node frame is therefore the exact
subgroup-projection Markov operator

`M_T=|T|^-1 sum_(e in T) P_(H_e)`.

Product Fourier decomposition yields every physical target/source node frame
divided by `|T|`, with regular multiplicity. In gauge coordinates
`a_i=t^-1x_i`, `b_i=t^-1y_i`, one common uniform multiplier updates every
unselected relative coordinate while each selected coordinate is fixed. The
complete `S_3`, one-pair control matches all 216 regular eigenvalues to the
physical Fourier blocks and verifies all 2,592 gauge transitions.

For a coordinate-aligned affine node of dimension `d`, the orientation
membership system has exactly `2d+1` distinct nonempty patterns and binary
incidence rank `d+1`. For `n>=5`, subdirect-product simplicity of `A_n` and
the sign quotient give the exact generated subgroup order

`|L_T|=|S_n|^(2d+1)/2^d`.

The regular walk's eigenvalue one has scalar mass `1/|L_T|`. More importantly,
a physical frame can have eigenvalue `|T|` only if all `2d` source irreps on
the varying coordinates are trivial or sign. Independent Plancherel failure
at a fixed node is at most `(2/|S_n|)^(2d)`. Under global source distinctness,
the event is impossible for every `d>=2`; over every bottom node its
unconditioned numerator is exactly bounded by

`2^K/|S_n|^2 < 2/|S_n|`.

After conditioning, divide by `P_cf(n,K)=1-o(1)`. Thus exact width-sized
outliers disappear simultaneously over the natural hierarchy with factorially
small failure probability. This is not a near-outlier or natural-edge theorem:
eigenvalues below but close to `|T|` remain uncontrolled, and the required
normalized edge is `Theta(1/|S_n|)` rather than merely a gap below one.

### Full-Regular Pairwise Subgroup-Angle Route Is Refuted

Files:

- `self_dual_wreath_subgroup_pair_angle_no_go.py`
- matching JSON artifact and focused tests.

For any two distinct orientations, their generated subgroup has three
nonempty membership patterns, parity rank two, and exact order

`|<H_e,H_f>|=|S_n|^3/2`.

For every affine node with `d>=2`, this is strictly smaller than `|L_T|`.
Consequently, in the full regular representation, pair-common invariants
strictly contain all-node invariants. After removing only the all-node common
space, **every pairwise cosine is exactly one**. The complete cosine matrix
has spectral radius `|T|-1`. The dense `S_2` two-cube control verifies all six
pairs exactly: ambient dimension 32, pair-common dimension eight,
all-node-common dimension four, and cosine residual below `1e-12`.

This cuts unrefined pairwise subspace-arrangement/Kazhdan-angle proofs on the
regular master. It does not refute a physical typical-block theorem: the
extra pair-common sectors may be carried by atypical Fourier blocks. A viable
angle route must prove a source-center quotient, show pair-common central
support is negligible on the relevant physical blocks, or use genuinely
higher-order incidence information. Do not cite the small noncommon
two-projector angle after quotienting each pair's own intersection as a
full-family expansion bound; those are different quotients.

### Sharp Pair-Support And Rank Transition

Files:

- `self_dual_wreath_local_pair_transversality.py`
- `self_dual_wreath_pair_common_covering_transition.py`
- `self_dual_wreath_fixed_family_common_rank_dilution.py`
- `self_dual_wreath_plancherel_kronecker_positivity.py`
- `self_dual_wreath_extended_kronecker_threshold.py`
- `self_dual_wreath_hamming_stratum_rank_transition.py`
- matching JSON artifacts and focused tests.

For three independent Plancherel irreps of `S_n`, character column
orthogonality gives the exact identity

`g(lambda,mu,nu)/(d_lambda d_mu d_nu)=(1+X)/|S_n|`,

`E[X]=0`, and

`E[X^2]=sum_(nonidentity conjugacy classes C) 1/|C|=o(1)`.

Nonnegativity of the Kronecker coefficient therefore proves
`Pr[g(lambda,mu,nu)=0]=o(1)`. The same calculation with fixed target `tau`
and `q>=3` independent Plancherel factors proves the stronger normalized
multiplicity law

`|S_n| m_tau/(d_tau product_j d_(lambda_j)) -> 1`

in probability, uniformly for each fixed target. This is an
**independent-Plancherel pointwise theorem**. It does not prove arbitrary
couplings, uniform-partition positivity, or simultaneous covering of every
target irrep.

Consequently the natural pair geometry has a sharp rank-density transition.
Hamming-one and Hamming-two orientation pairs are simultaneously transverse
with probability `1-o(1)` under global source distinctness. For every fixed
`h>=3` with `K-h>=3`, a density `1-o(1)` of the Hamming-`h` stratum is live,
and each fixed pair has relative common rank

`R_(e,f)=(2+o(1))/|S_n|^3`.

The density conclusion uses an average bad-pair indicator and Markov, not an
invalid union bound over the exponential Hamming stratum. Fixed orientation
families also show a decisive support/rank separation: all target supports
may be present while their scalar common rank is factorially tiny. These
results settle pair support and pointwise pair rank; they do **not** settle
the alignment of noncommon carrier directions around triples/cycles or the
complete node-frame spectral edge. The next mathematical object is the
multiplicity-weighted natural carrier law and its coherent higher-order
incidence, not another support screen.

### Natural Pair-Carrier Law Is Solved

Files:

- `self_dual_wreath_natural_pair_carrier_law.py`
- `research/representation/self_dual_wreath_natural_pair_carrier_law.json`
- `tests/test_self_dual_wreath_natural_pair_carrier_law.py`

For a fixed orientation pair, let `alpha` be the exact pair-angle carrier and
let the shared, left-only, and right-only source blocks be independent
Plancherel tensors. The shared block may contain any fixed target. Exact
character orthogonality and block independence give

`E[A_alpha]=d_alpha^4/|S_n|^3`.

After rank normalization the annealed carrier distribution is exactly

`q4(alpha)=d_alpha^4/Z4`, `Z4=sum_alpha d_alpha^4`.

Every even overlap moment follows:

`E[Tr |B_e^*B_f|^(2p)]/D`
`=|S_n|^-3 sum_alpha d_alpha^(4-2p)`.

In particular, active pair rank is `Z4/|S_n|^3`, Hilbert--Schmidt overlap is
`1/|S_n|^2`, and the fourth moment is `p(n)/|S_n|^3`. If all three random
blocks have at least three factors, the fixed-target variance theorem can be
averaged under `q4`; this proves quenched total-variation convergence without
unioning over all irreps. Also

`q4[d_alpha<=L] <= p(n)^2 L^4/|S_n|^2`

and the `q4` RMS pair correlation is at most `sqrt(p(n)/|S_n|)`. Thus the
worst-case `1/(n-1)` pair correlation and the mere presence of low-dimensional
carriers are radically unrepresentative of natural multiplicity mass.

This is still not a node-frame edge. The unresolved object is coherent
alignment of the overwhelmingly high-dimensional carrier multiplicity spaces
around orientation triangles and longer closed walks. Existing exact
sibling-frame moments through degree four and the all-word normal form remain
the correct bridge. A useful reformulation found during this pass is that the
`K`th moment of the two-color identity count is a return probability for the
fixed subgroup measure on `G^(2K)` obtained by choosing an orientation and one
uniform common multiplier. Coarse global gaps are insufficient because rare
Fourier blocks survive; seek a collision-free central-support or
operator-valued return bound. Small regular controls have nontrivial global
eigenvalues `3/4` for `S_3,K=2,3` and `S_4,K=2`, while the complete globally
distinct physical `S_4,K=2` screen has no nontrivial normalized-frame
eigenvalue above `1/2`. This is a target-selection clue, not a theorem.

### Two-Color Moments Are One Return Walk

Files:

- `self_dual_wreath_two_color_return_walk.py`
- `research/representation/self_dual_wreath_two_color_return_walk.json`
- `tests/test_self_dual_wreath_two_color_return_walk.py`

For `q_p(x)` equal to the number of two-colorings whose two ordered subwords
both multiply to identity, transpose the `K` coloring rows into `p`
orientation columns. If `mu_K` is the probability measure on `G^(2K)` that
chooses an orientation `e`, a uniform common multiplier `x`, and applies `x`
to the selected slot of every pair, then exactly

`E_(x in G^p) (q_p(x)/2^p)^K = mu_K^(*p)(1)`.

Thus the exponential `2^(pK)` coloring sum is not intrinsic: the growing-word
problem is a convolution-power/return problem for the source-only version of
the subgroup walk. For `S_n`, `n>=5`, its generated subgroup contains
`A_n^(2K)` and has sign-incidence rank `K+1`, hence

`|L_K|=|S_n|^(2K)/2^(K-1)`.

This does not make the global return probability sufficient. Complete dense
controls give largest nonstationary eigenvalue `1/2` for `S_2,K=2` and `3/4`
for `S_3,K=2`, while the natural scale is `1/|S_n|`. Those eigenvalues live in
atypical Fourier support. The precise successor is a growing-order return
bound after collision-free central projection, or an operator-valued return
bound that tracks physical source blocks. Do not spend time proving only a
constant global gap.

There is an exact regular-moment obstruction. For the unnormalized
source-only frame `F_K=2^K M_K`, stationarity forces

`tr_reg(F_K^p) >= 2^(Kp)/|L_K|`.

At information threshold this reaches one at `p=(2+o(1))K` and then grows
exponentially. Thus unconditioned regular growing moments are dominated by
rare common-invariant Fourier blocks long before the generic trace-method
degree. Global source distinctness removes exact stationary support for
`K>=2`, but growing moments cannot be transferred by ordinary total
variation. A collision-free central/injective return theorem is mandatory.

### All Pair-Common Hierarchy Directions Have Factorially Small Rank

Files:

- `self_dual_wreath_hierarchy_pair_common_rank_budget.py`
- `research/representation/self_dual_wreath_hierarchy_pair_common_rank_budget.json`
- `tests/test_self_dual_wreath_hierarchy_pair_common_rank_budget.py`

For the coordinate dyadic hierarchy on `F_2^K`, write `N=2^K`. Direct level
counting gives exactly

`N(2N-K-3)/2`

non-antipodal pair incidences and `N/2` root antipodal pairs. For every
non-antipodal pair, all three source blocks are nonempty, so the exact natural
pair-carrier law gives expected ambient-relative common rank `2/|S_n|^3`.
The span of pair-common ranges has rank at most their rank sum regardless of
triangle/cycle coherence. At a root antipodal pair the shared block contains
only the target, contributing `1/|S_n|^2` exactly for a trivial or sign target
and zero for a higher-dimensional target. Therefore the fixed-target bound is

`N(2N-K-3)/|S_n|^3 + 1[dim(tau)=1]N/(2|S_n|^2)`.

The unweighted sum over all targets, used only for a simultaneous Markov
bound, is

`p(n)N(2N-K-3)/|S_n|^3 + N/|S_n|^2`.

With `K=ceil(log2 |S_n|)+2`, this is `O(p(n)/|S_n|)`. Conditioning on all
source labels being distinct divides by `P_cf(n,K)=1-o(1)`, so all exact
pair-common hierarchy sectors occupy factorially small relative rank with
high probability. The finite conditioned bound is pre-asymptotically
vacuous at `n=20,24`, becomes nonvacuous at `n=28`, and is about `2^-153.66`
at `n=48`.

This resolves the scalar-rank trimming of singular-value-one pair-common
directions, including arbitrary coherent alignment among them. It does not
bound their exceptional eigenvalues, near-common carriers, noncommon
recoupling traffic, the complete node-frame edge, PGM state mass, or any
algorithm. The active object is now the collision-free noncommon return
operator after this exact-common sector is removed.

### Low Carriers Admit A Quarter-Factorial Hierarchy Trim

Files:

- `self_dual_wreath_hierarchy_low_carrier_trim.py`
- `research/representation/self_dual_wreath_hierarchy_low_carrier_trim.json`
- `tests/test_self_dual_wreath_hierarchy_low_carrier_trim.py`

The exact-common rank theorem extends to every pair carrier below a dimension
cutoff. Let `Z4(L)=sum_[d_alpha<=L] d_alpha^4`, let
`C_non=N(2N-K-3)/2`, and let `C_anti=N/2`. Trimming both endpoint singular
spaces for all carriers with `d_alpha<=L` costs expected unweighted
all-target relative rank at most

`B_L=2p(n)C_non Z4(L)/|S_n|^3`
`    +2C_anti sum_[d_tau<=L] d_tau^2/|S_n|^2`.

The second term is the root-antipodal target exception. Rank subadditivity
makes this valid for arbitrary coherent alignment and repeated incidence
across hierarchy levels. On the surviving leaf subspaces, the exact
pair-angle theorem gives every pair cross-map norm at most `1/(L+1)`.

The canonical choice

`L=floor(|S_n|^(1/4)/p(n))`

gives

`B_L <= 128/p(n)^2 + 8/(p(n)sqrt(|S_n|)) = o(1)`

before conditioning, and residual pair correlation
`O(p(n)/|S_n|^(1/4))`. Global-distinct conditioning divides by
`P_cf(n,K)=1-o(1)`. The exact finite bound becomes nonvacuous at `n=44`; at
`n=48`, `L` is about `2^33.57`, 130 low carriers are removed, the conditioned
all-target trim budget is about `2^-16.91`, and the residual pair bound is
about `2^-33.57`.

This kills the idea that polynomial-size worst-case carriers are the active
edge obstruction. It still does not prove an edge: multiplying the residual
pair magnitude by `Theta(|S_n|)` leaves a divergent row-sum bound. The
remaining task is signed/phase-sensitive Racah traffic or a center-valued
return theorem on the high-carrier complement. The quarter exponent comes
from the elementary fourth-power tail bound and is not known optimal.

### Finite Vertex Channels Are Positive Affine Triangles

Files:

- `self_dual_wreath_complete_s6_vertex_channel_audit.py`
- `research/representation/self_dual_wreath_complete_s6_vertex_channel_audit.json`
- `tests/test_self_dual_wreath_complete_s6_vertex_channel_audit.py`
- `self_dual_wreath_affine_plane_scalar_holonomy.py`
- `research/representation/self_dual_wreath_affine_plane_scalar_holonomy.json`
- `tests/test_self_dual_wreath_affine_plane_scalar_holonomy.py`

The complete S6 boundary uses all eight irreps of dimension at most nine, all
105 perfect matchings, and all eleven targets: 1,155 globally distinct
physical portfolios. Every one of the 64 vertices incident to at least three
live pair cores was audited after exact common directions were removed.
Sixteen have nonorthogonal traffic. Each has exactly one three-core connected
component; all sixteen are cliques, and their three opposite endpoints close
with the shared vertex to one affine plane. Normalized Grams have spectrum
`{0,1,3}` and no path/holonomy residual above `1.1e-14`.

An adversarial S6 stress search then included dimension-10 and dimension-16
source irreps under an ambient cap: 55 source sets, 5,775 matchings, 14,700
target portfolios, 1,208 high-degree vertices, and 236 nonorthogonal controls.
No violation appeared; worst holonomy residual was `2.14e-14`. A first dense
S7 control at ambient dimension 1,382,976 also produced one positive affine
triangle, with residual below `1e-13`. These two stress searches are recorded
here as live research observations, not default test artifacts.

The local algebraic explanation is exact. For a real carrier `V` of dimension
`d`, the three canonical pairings of four copies have diagonal Gram one and
positive off-diagonal Gram `1/d`. Tensoring cluster and companion carriers
gives `gamma=1/(d_beta d_p)`. Any multiplicity-scalar affine-plane channel
therefore normalizes to `J_3 tensor I`, has identity path maps, and positive
triangle holonomy. Negative-simplex phase is impossible inside one such
channel. This does not control matrix-valued recoupling or simultaneous
supports from different affine planes.

### Orthogonal Affine-Plane Atomization Is Falsified

Files:

- `self_dual_wreath_affine_plane_support_pressure_no_go.py`
- `research/representation/self_dual_wreath_affine_plane_support_pressure_no_go.json`
- `tests/test_self_dual_wreath_affine_plane_support_pressure_no_go.py`

The finite disjoint-triangle pattern cannot persist at threshold width. The
exact number of pattern-rich affine planes through one vertex is

`R_K=(4^K-4*3^K+6*2^K-4)/6`.

One rich vertex-plane star overlap has independent-Plancherel expected
noncommon support rank

`4(Z4^2-4)/|S_n|^7`

relative to ambient. Across all `N R_K` vertex-planes this is the support
demand. The worst-target expected total incident pair-core capacity is at
most

`2N(N-2)/|S_n|^3 + N/|S_n|^2`.

Their exact ratio is

`4R_K(Z4^2-4) / [|S_n|^4(2(N-2)+|S_n|)]`.

Since `Z4/|S_n|^2>=1/p(n)` and `N=Theta(|S_n|)`, this is
`Omega(|S_n|/p(n)^2)` and diverges factorially. Existing star multiplicity
relative concentration supplies a density-one lower demand after
global-distinct conditioning; a one-sided conditional Markov bound controls
capacity. Square-root pressure slack still diverges. Thus supports assigned
to distinct affine planes must overlap extensively with probability tending
to one in the natural collision-free law.

This is a no-go for disjoint clique atoms, not for the algorithmic direction.
Overlapping positive planes could form a well-conditioned association scheme,
expander, or approximately free traffic law. The active object is now the
matrix-valued incidence algebra of those overlapping channels.

### Signed Steiner Geometry: Local Positivity Is Not A Global Gauge

Files:

- `self_dual_wreath_signed_steiner_incidence_boundary.py`
- `self_dual_wreath_interplane_gauge_homology.py`
- corresponding JSON artifacts and focused tests.

At one orientation vertex, nonzero displacements are the `v=2^K-1` points of
`PG(K-1,2)` and affine planes are Steiner triples `{x,y,x xor y}`. The
unsigned point-line incidence matrix has

`C_+ C_+^T=((2^K-4)/2)I+J`,

so its condition number tends to three. Local positive line holonomy does not
force this gauge. Two independent binary functionals give legal signed line
columns with product `+1` and an exact two-dimensional kernel at every depth.
This is adversarial and does not assert that natural `S_n` recoupling realizes
the signing.

The remaining scalar gauges are classified by the first cohomology of the
bipartite point-line incidence graph. For all lines its dimension is

`beta_1=(2^K-2)(2^K-4)/3`.

For the pattern-rich lines used in the pressure theorem, a weight-`w` point,
`1<=w<=K-1`, has degree

`(2^w-2)(2^(K-w)-2)/2`,

the all-ones point has degree zero, exactly `2K+1` point vertices are
isolated, and all weights `2,...,K-2` form one giant component. Hence

`beta_1^rich=2R_K-2^K+2K+3=Theta(4^K)`.

The quotient signing has a negative six-cycle already on an embedded
four-coordinate rich subsystem. Single-plane positive-holonomy audits
therefore leave a quadratic-dimensional longer-cycle gauge debt.

### Scalar Gauge Singularities Are Rank-Rigid

Files:

- `self_dual_wreath_signed_steiner_nullity_theorem.py`
- `self_dual_wreath_signed_steiner_bulk_edge.py`
- `self_dual_wreath_random_steiner_gauge_edge.py`
- corresponding JSON artifacts and focused tests.

The adversarial kernel cannot become extensive in one full scalar channel.
Every real signed incidence matrix of `PG(K-1,2)` has left nullity at most
two for every `K>=3`, and the quotient construction attains two. The proof is
an exact Fano restriction: three independent kernel evaluations force the
seven signed Fano relations to imply both `cef=-abd` and `cef=abd`.
Exhausting all `4^7=16,384` positive-gauge Fano signings gives nullity
histogram `{0:5632,1:8960,2:1792}` and universal third-eigenvalue floor
`3-sqrt(5)`.

More strongly, every signing has a deterministic bulk edge. For the full
line family, with point degree `r=(v-1)/2`,

`||CC^T-rI||_F^2=v(v-1)`.

Thus at relative window `delta`, at most

`4v/[delta^2(v-1)]`

eigenvalues lie outside `r[1-delta,1+delta]`; the trimmed rank fraction is
`O(1/v)`. On the active pattern-rich component, degree normalization gives

`||D^-1/2 CC^T D^-1/2-I||_F^2 <= 6R_K/d_min^2 -> 16`,

so it also has only constantly many relative outliers for every signing.
No gauge randomness is needed. The independent balanced-gauge matrix
Bernstein theorem remains a stronger untrimmed surrogate, with condition
tending one, but its independence hypothesis is not natural and is no longer
needed for scalar bulk rank control.

These are per equal-weight scalar-channel theorems. They do not justify
adding the constant trims over all natural carrier sectors, and rank is not
yet PGM state mass.

### Matrix Holonomy Reduces To Diagonal Coverage

Files:

- `self_dual_wreath_operator_steiner_bulk_reduction.py`
- `self_dual_wreath_coverage_welch_pressure.py`
- corresponding JSON artifacts and focused tests.

Let a line `L` carry coefficient fiber `E_L` and let
`W_(x,L):E_L -> H_x` be arbitrary isometries at its three points. For the
global operator incidence map, set

`D_x=sum_(L contains x) W_(x,L)W_(x,L)^*`.

Unique-line incidence gives the exact holonomy-blind identity

`||CC^*-D||_F^2=6 sum_L dim(E_L)`.

If `D>=d_0 I` on a retained fiber, whitening gives

`||D^-1/2 CC^*D^-1/2-I||_F^2`
` <=6 sum_L dim(E_L)/d_0^2`.

For uniform `m`-dimensional unitary fibers the relative outlier trim is
`4/[delta^2(v-1)]`, independent of `m` and all nonabelian holonomy. Matrix
multiplicity and cycle transport are therefore not intrinsically fatal; the
active representation-theoretic object is the natural diagonal coverage
operator.

Support pressure does not prove coverage. If `P_a` are the incident support
projectors, `D=sum_a P_a`, `Q` is capacity, `T=tr D`, and `R=T/Q`, the fusion
Welch inequality gives

`tr(D^2)>=T^2/Q=RT`,
`sum_(a!=b)tr(P_aP_b)>=(R-1)T`.

So the divergent collision-free pressure forces enormous inter-plane
overlap; treating it as a perturbation is impossible. Define the normalized
excess fusion potential

`epsilon=Q tr(D^2)/T^2-1`.

The fraction of coverage eigenvalues below `(1-delta)R` is at most
`epsilon/delta^2`, and `epsilon=0` exactly for tight coverage `D=RI`. At
`n=48`, even the square-root-slack redundancy lower bound has log2 about
`84.46`, so raw overlap is necessarily nonperturbative. Pressure gives no
bound on `epsilon`.

This unweighted coverage target has now been bypassed for the actual weighted
pair-relation Gram. The natural collision-free four-orientation coverage
second moment

`sum_(a,b) tr(P_a P_b)`

in carrier/multiplicity variables remains open and relevant only if a
normalized support-incidence implementation specifically requires it. It is
no longer the leading spectral gate for the true relation coefficients.

### Exact Weighted Pair-Relation Bulk Edge

Files:

- `self_dual_wreath_affine_relation_weighted_bulk.py`
- `research/representation/self_dual_wreath_affine_relation_weighted_bulk.json`
- `tests/test_self_dual_wreath_affine_relation_weighted_bulk.py`

For an orientation star with coordinate-signature support `S`, exact
Plancherel averaging of the carrier-factorized physical overlap gives

`E ||B_ex^*B_ey||_F^2/dim(H_phys)=4/|S_n|^5`

whenever `|S|=3` or `4`. The only two-signature exception is
`2/|S_n|^4` for one-dimensional targets and zero otherwise. This was checked
both symbolically over all valid supports through `S_7` and directly against
the exact physical star-spectrum engine by summing every `S_5` Plancherel
label assignment.

Writing `g=|S_n|`, `N=2^K`, the exact ordered-pair counts at one orientation
vertex are `A_K=N^2-6N+8` for three/four signatures and `3(N-2)` for two
signatures. For the complete pair-common boundary `D_1`, its coefficient Gram
`G=D_1^*D_1` has diagonal `2I` and

`E ||G-2I||_F^2/dim(H_phys)=N[4A_K/g^5`
` + 6(N-2)1_(d_nu=1)/g^4]`.

Uniform balanced pair-core rank concentration lower-bounds the global domain
by `N B_K(1-eta)^3/g^3` times physical ambient dimension. Applying Markov
once to the whole relation Gram after exact collision-free conditioning gives
a burden/capacity ratio `O(1/g)`. With square-root slack, both conditional
failure and fixed-window relative outlier rank are `O(g^-1/2)` uniformly in
the target. This proves a collision-free **coefficient-rank bulk edge** despite
the factorially divergent unweighted support pressure.

The exact relation-cokernel identity `D_0D_1=0` means every trimmed relation
image has zero ideal PGM polar amplitude. Do not describe PGM state-mass
transfer as open for this trim; it is exactly resolved. The real open gate is
whether retained pair relations plus recursive child-span constraints compile
the full synthesis-cokernel projector without leaving spurious H0, and whether
that projector and the subsequent polar chain have efficient coherent access.
No untrimmed minimum edge, full cokernel projector, decoder, or speedup is
proved.

### Global Collision-Free Mass And Injective Source Kernel

Files:

- `self_dual_wreath_global_collision_free_mass.py`
- `self_dual_wreath_global_distinct_joint_kernel.py`
- matching JSON artifacts and focused tests.

The exact natural mass of globally distinct source partitions is

`P_cf=(2k)! e_(2k)({d_lambda^2/n!})`.

At threshold it is zero for small `n` and still about `2^-26.51` at `n=48`,
but this is pre-asymptotic. Aggarwal--Elboim's maximal-dimension theorem gives
`C_n<=max p_lambda=exp(-Theta(sqrt(n)))`; with `k=Theta(n log n)`, the birthday
bound proves `P_cf=1-o(1)`. The physical-mass gate is resolved. No spectral
claim follows merely from that typicality.

Global distinctness destroys independence. The correct `2k`-slot source law
is the injective Plancherel transform

`I_n(f_1,...,f_r)=sum_(nu_1,...,nu_r distinct) prod_j p_(nu_j)f_j(nu_j)`.

Unequal characters and projector words have exact rank-one slot expansions,
so their joint conditioned kernel is `I_n/P_cf`. Direct and subset-DP values
match exactly; `n=4,5` controls have nonzero rational factorization defects.
Moreover

`TV(pairwise-unequal, globally-distinct)=1-P_cf/(1-C_n)^k`

is `exp(-Theta(sqrt(n)))`, much larger than the required
`exp(-Theta(n log n))` PGM moment scale. Generic total-variation transfer from
the independent all-unequal kernel is inadequate for transferring the large
moment observable directly. It is not mandatory for event transfer. If each
independent-source node event fails with probability `delta`, conditioning and
a union bound give full hierarchy failure at most `M delta/P_cf`, with
`M<16 n! p(n)`. Thus the active independent per-node target is
`delta=o(1/(n!p(n)))`; the signed injective observable is only an optional
direct-moment route.

### Vertex Trivialization Criterion And Flat Carrier Groupoid

Files:

- `self_dual_wreath_vertex_trivialization_criterion.py`
- `self_dual_wreath_vertex_channel_groupoid.py`
- matching JSON artifacts and focused tests.

After exact common directions are removed, let `G` be the block Gram of all
residual cores incident to one vertex and let `gamma` bound their cross maps.
The missing vertex isometries exist exactly when

`T_gamma=I+(G-I)/gamma >= 0`, equivalently `lambda_min(G)>=1-gamma`.

This is constructive: any Gram factor of `T_gamma` supplies the isometries.
A regular simplex is the decisive abstract counterfamily. At width `p`, every
pair correlation has the uniform reciprocal magnitude `1/(p-1)`, but the
normalized Gram has minimum eigenvalue `2-p`; its signed triangle holonomy is
`-1`. Therefore the old observation of a single residual correlation value
is not evidence for vertex trivialization.

The natural W6 controls satisfy a stronger flat partial-isometry groupoid. For
normalized maps `A_ef`, their support projections commute and

`A_ef A_fg = A_eg P_gf`.

This splits the normalized Gram into positive clique atoms `J_|S|`. Three
selected controls, including a five-edge residual vertex, pass below `1e-14`
with spectra `{0,1,3}`. The simplex fails the path law by exactly two. The
all-depth theorem is now precise: derive this path law from arbitrary natural
Kronecker/Racah multiplicity indices, or find a natural negative cycle.

### Graded Flat-Transport Boundary And Internal-Closure Rescue

Files:

- `self_dual_wreath_graded_flat_transport_no_go.py`
- `self_dual_wreath_internal_closure_graded_rescue.py`
- matching JSON artifacts and focused tests.

Vertex groupoids and a constant metric floor are still insufficient for the
relative polar. On a flat crossing-only `K_(p,p)` channel,

`M=2(1-gamma)I+gamma(A+B)`, `J=gamma(A-B)`,

and the exact defect is

`gamma p/[2(1-gamma)+gamma p]`.

It tends to one, so the endpoint gap is `Theta(1/p)` and is exponentially
small at natural width. This kills any inference from the Laplacian metric to
the graded endpoint gap without internal quotienting.

The full internal closure changes the answer. Add every same-child pair edge
on both sides and take the exact graded Schur quotient. The defect becomes

`gamma p/[2(1-gamma)+2 gamma p] <= 1/2`,

so every endpoint gap is at least `1/4`, independent of width. Ten exact
controls pass for `gamma=1/5,1/9`, and natural-width scaling tends to the
quarter gap.

This channel theorem remains valid, but it is no longer the complete polar
mechanism. Direct leaf pair relations fail to span the natural synthesis
kernel asymptotically. Its endpoint gap applies to a signal-free subset of
known constraints, not to every hierarchical constraint.

### Natural Rank, Residual Energy, And Graded Trim

Files:

- `self_dual_wreath_uniform_orientation_rank_concentration.py`
- `self_dual_wreath_pair_core_rank_concentration.py`
- `self_dual_wreath_star_channel_mass_typicality.py`
- `self_dual_wreath_residual_frobenius_typicality.py`
- `self_dual_wreath_graded_frobenius_trim.py`
- matching artifacts and focused tests.

For independent Plancherel factors and target `nu`, normalized multiplicity
`X_nu` obeys

`E X_nu=d_nu/G`,

`Var(X_nu)/E[X_nu]^2=sum_(K!=1) r_nu(K)^2 |K|^(2-C)`.

At natural copy depth, every orientation rank and every balanced pair-core
rank concentrates simultaneously after global-distinct conditioning. The
finite W6 sparse star graph is pre-asymptotic: natural live pair-core density
is `1-o(1)`. Exact pair rank relative to the full target carrier has mean
`2/G^3`.

On typical seven-pattern star channels, rank-normalized carrier law is
`q(alpha)=d_alpha^4/Z_4`, and high-correlation low-dimensional carriers have
factorially small rank mass. More generally, all 16 complement-pattern
occupancy strata satisfy expected residual squared overlap at most `4/G^5`
per centered star. This gives full relation-Gram off-diagonal Frobenius
density `O(G^-1/2)` with failure `O(G^-1/2)`.

Pinching `K=O^2+O_J^2` into left-internal, right-internal, and crossing sectors
and retaining eigenvalues at most `epsilon^2/3` deletes at most
`6 delta/epsilon^2` coefficient fraction while preserving the grading. At
`epsilon=1/4`, the retained pair-relation quotient has endpoint gap at least
`0.392857...`; the n48 removed fraction bound is `6.35e-25`. This is an
information-theoretic conditioning theorem. The low-energy projector still
has no coherent polynomial implementation.

### Relation Cokernel, Augmented H0, And Recursive Resolution

Files:

- `self_dual_wreath_relation_cokernel_transfer.py`
- `self_dual_wreath_augmented_h0_dimension_obstruction.py`
- `self_dual_wreath_hierarchical_cokernel_resolution.py`
- updated augmented-Cech and graded-trim modules, artifacts, and tests.

For leaf isometries `Q_e`, let `D_0=[Q_1 ... Q_N]` and let `T` embed each
coefficient fiber into its own physical leaf copy. The orientation PGM
analysis and polar satisfy

`R=T D_0^*`,

`range(polar)=T range(D_0^*)=T ker(D_0)^perp`.

Every pair boundary obeys `D_0 D_1=0`. Therefore every retained or deleted
pair-relation mode is exactly orthogonal to the ideal PGM output. The old
coefficient-to-state-mass comparison was misposed: relation trimming has
exactly zero ideal state loss. The complement of pair relations equals the
polar support iff augmented

`H_0=ker(D_0)/im(D_1)`

vanishes. Three lines in a plane are the generic counterexample; the physical
W3 control has H0 dimension two, while the selected W5 control is exact.

Pair completeness fails asymptotically. Put `G=n!`,
`K=ceil(log2 G)`, `N=2^K`, `c=N/G`, and `g=c-1`. Uniform leaf-rank
concentration gives `dim ker D_0 >= 3gD/4` at relative tolerance `g/(4c)`.
The expected total pair-core budget is at most

`D [N(N-2)/G^3 + N/(2G^2)]`.

Since `g>=(2^v2(n!))/n!`, Markov plus the rank theorem proves with conditioned
probability `1-o(1)` that `dim H0>=gD/2>0`. With one extra copy,
`dim H0>=D/2`. At n48 the finite conditioned bounds certify relative H0 at
least `0.017786` at minimal copies and `0.535572` with one extra copy, with
failure upper bounds about `2^-168.96` and `2^-171.87` respectively.

This does **not** kill hierarchical polar sampling. For every binary node
`T=L union R`, with child syntheses `S_L,S_R` and common child span `K`,

`ker[S_L S_R] = ker S_L direct_sum ker S_R direct_sum`

`{S_L^+x direct_sum -S_R^+x : x in K}`.

Recursing this identity exactly resolves the full synthesis cokernel for any
finite subspace family, including the three-lines control. The remaining
node metric and grading on an orthonormal basis `X` of `K` are exactly

`M=X^*(F_L^+ + F_R^+)X`,

`J=X^*(F_L^+ - F_R^+)X`, where `F_s=S_s S_s^*`.

Binary common-span synthesis would require natural pseudoinverse-frame
comparability. A complete abstract hierarchy with `p` repeated left copies
and one matching right copy has endpoint gap `1/(p+1)`, so exact completeness
alone gives no conditioning. However, the later constant-arity polar identity
shows this binary shorted-metric route is one implementation, not a mandatory
mathematical gate. The mixed-arity frame-root chain is exact; its natural
spectral edges and coherent implementation remain open.

### Revised Highest-Value Derivations

1. Prove or refute **positive natural mass of a genuinely noncommutative final
   component-effect algebra**. The exact diagnostic is
   `D_com=sum_[e<f][H_e,H_f]^*[H_e,H_f]`, whose central support is the source-
   block noncommutativity event. Full-rank nonscalarity `D_ns` does not imply
   this: an orthogonal PVM is the exact counterexample. Either prove positive
   central and common-span support of `D_com` on high-dimensional globally
   distinct blocks, or prove asymptotic commutativity and target a coherent
   simultaneous eigenbasis/conditional-probability compiler. Finite S6
   noncommutativity uses negligible low-dimensional anchors and is not enough.
   The original leaves are now known to be noncommuting on a density-one set of
   balanced pairs with inverse-polynomial norm, but generic transfer through
   the canonical child frame inverse is now refuted even for distinct
   high-rank leaves, condition number below three, constant aspect, and a
   full-rank nonscalarity defect. Do not pursue another condition-number-only
   transfer. The full-support reciprocal-integer criterion is also invalid
   after proper sibling common-span compression: every POVM can arise there,
   and the structured counterfamily matches all currently proved coarse
   natural analogues while commuting. Directly analyze `D_com` from the
   compressed regular-master formula on natural source/common mass. The exact
   scalar target is now
   `M_4=E[Tr((sum H_e^2)^2)-sum_(e,f)Tr(H_eH_fH_eH_f)]/D_phys`.
   Any lower bound `M_4>=eta` gives physical and source support at least
   `eta/2`; no center-valued local law or positive edge is needed. Compute
   this first under independent Plancherel sources, then transfer it to the
   globally distinct law. The exact Haar benchmark predicts the blockwise
   normalized scale `alpha^2(1-alpha)` in the sparse-outcome limit; use it as a
   falsifier, not as an assumption. If the natural gap vanishes, derive the simultaneous
   eigenbasis; if it is positive, compile the noncommuting component branch.
2. Compile or kill the **natural final component-POVM dilation**. Its dimension
   and center-valued mass gates are solved: on `1/9-o(1)` globally distinct
   natural mass, `r/D>=19/128-o(1)`, `r/N>=19/520-o(1)`,
   `b_max/r<=(520/19+o(1))/q`, and the nonscalarity defect has relative rank
   `1-o(1)` with expected physical support mass at least `19/1152-o(1)`.
   What remains is coherent square-root/support access. The state-weighted
   spectral trim is now exact: threshold `tau` loses at most
   `kappa tau N/r` for `kappa=r||rho||_infinity`. Therefore the next theorem is
   the actual incoming common-fiber density and either
   `kappa=poly(n)` or a sharper state-specific weighted-loss bound. A natural
   edge `delta>=kappa_0 r/N` is another sufficient route, and a direct
   representation-specific dilation is a third. Derive any edge from the exact regular-master component formula,
   not Haar/Jacobi analogy. A natural exponentially small edge only kills the
   untrimmed generic-QSVT route, not every average-success implementation.
3. Extend the **positive-mass common-span/component-aspect theorem to every
   relation-bearing multiscale node**, or prove that only the final sibling
   component measurement is needed by a complete decoder. The final theorem
   uses exact sibling second moments and does not provide earlier eight-way or
   binary-node dimensions. Classify those nodes before attempting a global
   recursive claim.
4. Compile the **natural sparse-support component-POVM dilation** after items 1--2.
   If positive-edge rigidity survives, build coherent support-projector SELECT,
   tightly normalized child pseudoinverse access, and GPE transport. Generic
   square-root QSVT is relevant only on sectors with an actually small
   positive edge. A compact coherent support SELECT, not another formal polar
   decomposition, is the target.
5. Establish or refute a **physical MRS transcript-POVM separation**. Construct
   the sequential transcript POVM `{E_t}` for a fixed adaptive sieve policy and
   separate the pulled-back PGM effect from
   `{sum_t f_t E_t:0<=f_t<=1}` on positive accepted-state mass. For one fixed
   projective tree, test both `||M-Delta(M)||` and the stronger
   `||M-C(M)||`; vanishing of the first does not imply classical transcript-only
   simulation when blocks have dimension greater than one. Use the implemented
   zonotope projection/dual-witness engine once the effects exist, then prove a
   policy-independent obstruction or exhibit an allowed simulation. Do not use
   “globally coherent” as a substitute for this calculation.
6. Build a **uniform coherent GPE generator and holonomy theorem**. Give a
   polynomial reversible SELECT for partial-support transports,
   including path and gauge data, rather than an exponential classical table.
   Then give a polynomial-depth spanning structure for the fundamental
   GPE/Racah cycle operators on positive native PGM mass and prove an
   inverse-polynomial frustration gap, or find a natural near-flat
   counterfamily. Abstract efficient edge transport is insufficient.
7. Prove a **natural short-metric endpoint theorem** for the recursive normal
   form. Equal metrics give an exact Hadamard, proportional metrics give a
   scalar rotation, and noncommuting metrics require an operator-valued mixer.
   Bound the grading defect on positive native mass or construct a natural
   exponentially imbalanced/noncommuting counterfamily. Pair GPE availability
   alone says nothing about this gap.
8. Use the **collision-free weighted pair-relation bulk edge** only as input to
   the recursive resolver in item 6. Relation directions have exactly zero
   ideal PGM amplitude. The risk is incomplete removal of emergent relations,
   partial support normalization, or a small holonomy gap, not pair carrier
   dimension. Do not spend more work on low-carrier pair trimming as an access
   strategy; GPE bypasses that barrier directly.
9. In parallel, prove or falsify an **independent-Plancherel all-depth
   noncommon node-frame spectral event** for the mixed-arity schedule with
   per-node failure `o(1/(n!p(n)))`. This remains necessary if the recursive
   GPE/holonomy route still uses frame-root whitening.
10. Work on the exact subgroup-projection regular master and bound the
   **central support of bad spectral projections**, not ordinary scalar
   spectral mass. Seek a center-valued local law or deterministic no-outlier
   theorem. The interval-uniform scalar route needs
   `Theta((log n!)^2)` degree and is not competitive.
11. Use the exact word-map normal form only if it can prove item 9 at growing
   word length or derive a resolvent/gap identity for item 6. More fixed-degree
   moment screens are cut.
12. Apply event-level global-distinct conditioning only after an independent
   node/holonomy event is proved. `o(1)` total variation is too weak for the
   required exponentially small union-bound scale.
13. Once items 1--10 yield a complete polar, compose the physical row-copy,
    GPE/relative polar, and inverse `S_n` QFT. Audit total copies, gates,
    memory, approximation error, and classical dequantization.
14. Only after the transcript criterion in item 5 and a complete circuit,
    state precisely whether the architecture lies outside MRS and make any
    end-to-end decoder claim.

Do not revert to the old priority “observe one gamma and assume a common
isometry.” Do not use an ungraded Laplacian floor as a polar endpoint gap. Do
not use `o(1)` total-variation closeness to transfer an exponentially small
moment. Do not use fixed normalized moments as a spectral edge theorem. Do not
claim direct pair-common completeness; it is falsified. Do not treat augmented
H0 as a no-go for recursion; hierarchical span relations resolve it exactly.
Do not restore binary pseudoinverse comparability as a mandatory gate after
the exact mixed-arity polar factorization. Do not list inverse carrier
dimension, pair-polar QSVT degree, or a full Kronecker transform as the active
pair-transport bottleneck: coherent GPE now bypasses all three. The unresolved
objects are higher-order support coverage, holonomy gap, and complete
relative-frame composition.
Do not revive universal scalar coefficient-affine fibers: the globally
source-distinct S6 partial-support control falsifies them while preserving
affine masks. Any bulk scalar approximation must first prove that matrix
partial-support channels have vanishing physical frame weight.
Do not claim an MRS escape from deferred measurement, unmeasured GPE labels,
or generic noncommutativity. The required object is a positive-mass separation
of the pulled-back physical decision effect from the classical postprocessing
set of the full adaptive transcript POVM. Off-diagonal blocks are only one
sufficient fixed-projective witness; within-block nonscalarity is another.

### Orientation Fourier Reduction

Files:

- `self_dual_wreath_orientation_fourier_reduction.py`
- `research/representation/self_dual_wreath_orientation_fourier_reduction.json`
- `tests/test_self_dual_wreath_orientation_fourier_reduction.py`

For unequal labels `(lambda_i,mu_i)`, the compressed overlap is

`K_i(s) = [rho_lambda_i(s) tensor I + I tensor rho_mu_i(s)] / 2`.

The collision-free orbit-Gram Fourier block in target irrep `nu` is exactly

`F_nu = 2^-k sum_epsilon E_(nu,epsilon)`,

where every `E_(nu,epsilon)` is an invariant-subspace projector. All 15
collision-free `W_4` controls pass with maximum spectrum residual below
`4.5e-16`.

The cheap support-sparsity proof route is falsified. Every tested portfolio
from `n=6` through `n=12` has full orientation support. At `n=12,k=29`, every
target supports all `2^29` orientations, with full support reached after the
third label.

### Orientation Fusion-Frame Second Moment

Files:

- `self_dual_wreath_orientation_fusion_moment.py`
- `research/representation/self_dual_wreath_orientation_fusion_moment.json`
- `tests/test_self_dual_wreath_orientation_fusion_moment.py`

For orientation projectors `E_a,E_b`, pair overlap has the exact
representation-ring formula

`Tr(E_a E_b) = d_companion sum_tau m_A(tau)m_B(tau)m_D(tau)/d_tau`.

It passes 48 active pair-overlap controls and 300 rank controls over all 15
collision-free `W_4` tuples. The maximum nontrivial canonical correlation is
`0.5`; two finite pairs have nonzero common range.

The complete orientation-averaged second moment is evaluated without
enumerating `4^k` pairs by reconstructing symmetric-group class-product
constants for the cycle types of `s`, `t`, and `st`. Through `n=12,k=29`, the
largest collision lower bound is only `1.060406...` times the target
`2^(1-k)` scale, and maximum effective-rank log2 is `639.9058`. No
second-moment superquartic obstruction appears.

This is nonobstructing structural evidence, not a norm theorem:
`Tr(F^2)/Tr(F)` is a lower bound on `lambda_max(F)` and cannot exclude a thin
high-eigenvalue sector.

### Orientation Common-Range Theorem

Files:

- `self_dual_wreath_orientation_common_range.py`
- `tests/test_self_dual_wreath_orientation_common_range.py`

For two orientations, split the representation into the shared tensor
`R_0`, factors selected only by each orientation `R_a,R_b`, and companion
space `H_c`. The commutator of the two diagonal actions acts only on `R_0`.
Because `[S_n,S_n]=A_n`, the exact intersection formula is

`dim(Ran E_a intersect Ran E_b) = dim(H_c) sum_delta m_0(delta)m_a(delta)m_b(delta)`

for `delta` equal to the trivial or sign representation. The formula passes
all 750 `W_4` matrix controls with zero residual.

An exact Kronecker-support dynamic program counts all `4^k` ordered pairs
without enumeration. Pairwise common ranges proliferate rather than vanish:
at `n=10,k=21` every target exceeds 99.8% common-range incidence; at
`n=12,k=29` the minimum and maximum over all 77 targets are
`0.9999977811` and `0.9999986789`. Pairwise transversality is therefore
falsified. This does not prove a large norm because different pairs can share
different directions.

### Fixed-Family Common-Range Depth

Files:

- `self_dual_wreath_orientation_triple_range.py`
- `research/representation/self_dual_wreath_orientation_triple_range.json`
- `tests/test_self_dual_wreath_orientation_triple_range.py`

For any fixed family of orientations and `n>=5`, group factors by the subset
of orientations selecting them. Simplicity of `A_n` makes its actions
independent on distinct membership patterns. Each pattern tensor must occupy
a trivial/sign sector, and the sign choices solve a linear parity system over
`F_2`. This gives an exact fixed-family intersection multiplicity formula.
It passes all 140 `S_5` matrix controls with zero residual.

The naive exact seven-support dynamic program is not scalable: 18,784 states
at `n=6`, 508,186 at `n=7`, and a 600,000-state cap before completing `n=8`.
Deterministic uniform sampling with exact per-family multiplicity tests shows
a sharp incidence-depth transition at `n=12,k=29`:

- three-way incidence: at least 93.1% estimated on every declared target;
- four-way incidence: at most 5.1% estimated;
- five- and six-way incidence: zero successes in 2,048 samples per target,
  with Wilson upper bounds recorded in the artifact.

Thus exact common cores are dispersed by family size five. This does not
control near-common directions or the frame norm.

### Exact Pair Principal-Angle Spectrum

Files:

- `self_dual_wreath_orientation_pair_angle_spectrum.py`
- `research/representation/self_dual_wreath_orientation_pair_angle_spectrum.json`
- `tests/test_self_dual_wreath_orientation_pair_angle_spectrum.py`

Decompose the shared, left-only, and right-only pair tensor products into
`S_n` irreps. Every nonzero principal correlation between two orientation
ranges is exactly `1/d_alpha`, with multiplicity

`dim(H_c) d_alpha m_0(alpha)m_a(alpha)m_b(alpha)`.

The `d_alpha=1` terms are exactly the trivial/sign common ranges. For `n>=5`,
all non-common correlations are at most `1/(n-1)`. The complete spectrum
formula passes 56 active finite controls: all collision-free `W_4` tuples and
three `W_5` controls, with maximum residual below `4.5e-16`. The observed
largest non-common correlations are `1/2` at `n=4` and `1/4` at `n=5`.

This proves dimension-driven pair contraction off the common ranges. The
remaining problem is the Gram operator carried by the trivial/sign incidence
channels across many orientations.

### Structured Block Common Cores

Files:

- `self_dual_wreath_orientation_block_common_core.py`
- `research/representation/self_dual_wreath_orientation_block_common_core.json`
- `tests/test_self_dual_wreath_orientation_block_common_core.py`

Partition the source labels into blocks whose left and right tensor products
contain the same one-dimensional character. Replicate one orientation bit
across every label in a block. For `r` parity-compatible blocks, all `2^r`
resulting orientation projectors have an exact common vector, so

`||sum_e E_e|| >= 2^r` and `||F_nu|| >= 2^(r-k)`.

The exact deterministic portfolio search finds witnesses for all six rows
`n=7,...,12`. At `n=12,k=29`, nine blocks give a family of 512 projectors,
projector-sum norm at least 512, averaged Fourier norm at least `2^-20`, and a
factor 256 violation of the bare `2^(1-k)` target. The common-core dimension
lower bound has log2 `107.7938`. These finite portfolios by themselves do not
establish natural asymptotic mass.

### Typical Plancherel Block Obstruction

Files:

- `self_dual_wreath_plancherel_block_obstruction.py`
- `research/representation/self_dual_wreath_plancherel_block_obstruction.json`
- `tests/test_self_dual_wreath_plancherel_block_obstruction.py`

Primary literature dependency:

- Mark Sellke, *Covering Irrep(S_n) With Tensor Products and Powers*, Theorem
  1.2, `https://arxiv.org/abs/2004.05283`.

Sellke proves that a fixed absolute number `C` of arbitrarily coupled
Plancherel irreps tensor together to cover every `S_n` irrep with probability
`1-o(1)`. Divide the natural `k=ceil(log2(n!))` labels into `C`-sized blocks.
Both the left and right block products cover every irrep except on an
`o(1)` fraction of blocks with high probability. This density statement needs
no convergence rate: Markov applied to the expected bad-block fraction is
enough.

Freeze bad blocks and the bounded leftover. Select a target constituent of
their chosen residual tensor; self-duality of `S_n` irreps makes the target
times residual contain the trivial irrep. Every good block uses its trivial
left/right sectors. The exact fixed-family theorem then yields

`r=(1-o(1))k/C` independent block bits and `2^r` projectors with a common
vector. Intersecting this event with the existing global-distinctness event
shows, for typical natural globally collision-free tuples,

`max_nu ||F_nu|| >= 2^(r-k)`.

Therefore every proposed uniform `poly(n)2^-k` upper bound is asymptotically
false: the ratio is `2^r/poly(n)=2^Omega(k)/poly(n)`. This closes the uniform
orientation-frame norm route as a negative result. It does **not** rule out
whitening, quotienting the common channels, non-projector measurements,
fixed-target behavior, efficient decoders, or quantum advantage. Seven
focused tests pass, all six proof steps are gated true, and three unresolved
scope objections are preserved in the artifact's adversarial audit.

### Spectrally Trimmed Constant-Success Sub-POVM

Files:

- `self_dual_wreath_spectral_trimmed_subpovm.py`
- `research/representation/self_dual_wreath_spectral_trimmed_subpovm.json`
- `tests/test_self_dual_wreath_spectral_trimmed_subpovm.py`

For any `M` equal-rank-`r` projectors, put `B=M^-1 sum_s P_s` and
`mu=Tr(B^2)/r`. For fixed `c>1`, let `R=1[B<=c mu]` and define

`E_s=R P_s R/(M c mu)`.

These effects form a valid sub-POVM. The second-moment Markov bound retains
average projector trace fraction at least `1-1/c`. Rank Cauchy plus Jensen,
without any covariance assumption, proves average exact-label success

`p_correct >= (1-1/c)^2/(M c mu)`.

For the wreath bridge ensemble,

`mu=(2^k+M-1)/(M 2^k)`.

At `M=n!`, `k=ceil(log2 M)`, and `c=2`, `M mu<=2`, hence
`p_correct>=1/16` for every `n`. Three finite covariant-projector controls
pass exactly; one control removes two genuine high-frame eigenvectors. This
proves that the common-core norm spike is not an information-theoretic no-go.
It does not implement the sharp cutoff or the `n!` outcomes.

### Generic Spectral-Filter Degree Obstruction

Files:

- `self_dual_wreath_spectral_filter_degree_obstruction.py`
- `research/representation/self_dual_wreath_spectral_filter_degree_obstruction.json`
- `tests/test_self_dual_wreath_spectral_filter_degree_obstruction.py`

The clipping threshold is `tau=Theta(1/n!)`. A bounded polynomial uniformly
approximating the low-pass must change by a constant between `tau` and
`2tau`. The original Markov estimate was valid but loose. Because QSVT
polynomials are bounded on `[-1,1]` and the transition lies near the interior
point zero, Bernstein's inequality forces degree `Omega(n!)` on eigenvalue
access. Singular-value access widens the transition to
`Theta(1/sqrt(n!))` but still needs degree `Omega(sqrt(n!))`.

This closes generic polynomial/QSVT filtering of the normalization-one frame
encoding. It is not an all-circuit lower bound: a spectral gap, better-scaled
encoding, exact representation transform, or intrinsic quotient remains a
valid bypass target. Scaling is stored in log space to avoid factorial
underflow.

### Black-Box Spectral-Trim Query Lower Bound

Files:

- `self_dual_wreath_spectral_filter_query_lower_bound.py`
- `research/representation/self_dual_wreath_spectral_filter_query_lower_bound.json`
- `tests/test_self_dual_wreath_spectral_filter_query_lower_bound.py`

For search bits `x_j`, the equal-rank projectors `P_j=|x_j><x_j|` have
average `diag(1-|x|/M,|x|/M)` and reflections
`2P_j-I=(-1)^x_j Z`. A generic low-pass that separates zero from a fixed
positive multiple of `1/M` therefore solves promised unstructured search.
BBBV gives `Omega(sqrt(M))` controlled-projector queries, hence
`Omega(sqrt(n!))` at `M=n!`. This closes every generic indexed-projector or
PREPARE/SELECT implementation. It does not cover extra symmetric-group
structure.

### Exact Plancherel Tensor Stationarity

Files:

- `self_dual_wreath_plancherel_block_mass.py`
- `research/representation/self_dual_wreath_plancherel_block_mass.json`
- `tests/test_self_dual_wreath_plancherel_block_mass.py`

For any fixed block size `C>=1` of iid Plancherel irreps and target `nu`,

`E[m_nu/product_i d_lambda_i]=d_nu/n!`,

so the expected normalized `nu`-isotypic mass is exactly `d_nu^2/n!`, the
Plancherel probability of `nu`. This follows because
`E[chi_lambda(g)/d_lambda]` is the regular character divided by `n!`.

Trivial and sign block sectors therefore each have expected normalized mass
`1/n!`, independent of `C`; independent left/right matched one-dimensional
mass is `2/(n!)^2`. Markov gives an `n^a/n!` typical upper bound with failure
`n^-a`. All 540 exact class-sum controls through `n=10` and block sizes
`1,2,3,8` pass.

This explains the coexistence of Sellke-typical support, a large frame-norm
spike, and successful spectral trimming. It kills direct postselection onto
the common-core sectors. Efficiently rejecting or quotienting those thin
sectors remains open.

### Quotient And Local-Filter No-Go Chain

Files:

- `self_dual_wreath_block_common_core_quotient.py`
- `self_dual_wreath_orientation_covariant_quotient_obstruction.py`
- `self_dual_wreath_branch_controlled_invariant_filter.py`
- `self_dual_wreath_paired_block_filter_bypass.py`
- `self_dual_wreath_local_isotypic_filter_no_go.py`
- matching artifacts under `research/representation/`
- matching focused tests under `tests/`

The algebraic quotient that removes trivial/sign sectors from every left and
right block kills the finite common vector with negligible expected dimension
loss, but its naive branchwise physical lift fails: it commutes with the two
uniform orientation actions and has mixed-orientation commutator norm one.
For non-self-conjugate source labels, all orientation signatures generate
independent `A_n` actions. Schur's lemma makes the branchwise commutant scalar,
so a nontrivial branch-independent projector cannot implement that quotient.

An orientation-controlled physical filter does commute with hidden
conjugation and removes the selected one-dimensional block sectors. It is not
enough. Pair two Sellke-good blocks and retain any common nontrivial irrep
`alpha`; self-duality puts trivial inside `alpha tensor alpha`, recreating one
common orientation bit per pair. At `n=12,k=29`, the exact portfolio retains a
16-projector common family after the local filter.

The paired witness generalizes by Plancherel incidence. For arbitrary retained
sets `S_j` of mass at least `q`, double counting forces one irrep to occur in
at least `qb` blocks. Pairing those blocks leaves `floor(qb/2)` common bits.
Thus every constant-mass block-local isotypic filter is asymptotically
bypassed. Nine focused tests across the local and cluster-local modules pass.

### Quantitative Cluster-Locality Lower Bound

Files:

- `self_dual_wreath_cluster_locality_no_go.py`
- `research/representation/self_dual_wreath_cluster_locality_no_go.json`
- `tests/test_self_dual_wreath_cluster_locality_no_go.py`

Treat disjoint clusters of at most `L_n` Sellke-good base blocks as
superblocks. If each cluster retains common left/right Plancherel support mass
`q_n`, incidence and self-dual pairing leave

`r_n = Omega(q_n k_n/L_n)`

exact common bits. Because `k_n=Theta(n log n)`, the residual norm ratio is
superpolynomial whenever `q_n n/L_n -> infinity`. At constant retained mass,
**every disjoint product isotypic filter acting on `o(n)` source labels per
cluster is ruled out**. A viable high-retention filter must coordinate
`Omega(n)` labels, use overlapping/global structure, leave the isotypic
support-filter model, or change the spectral access model.

This is not a general circuit lower bound. It does not cover overlapping
bounded-depth filters, globally coordinated support decisions, non-isotypic
coherent transforms, or the abstract spectral-trimmed sub-POVM. The report
contains 12 conservative scaling rows, nine finite degree/locality thresholds,
and an explicit unresolved-scope audit.

### Orientation-Character Filter And Circuit Schema

Files:

- `self_dual_wreath_orientation_subspace_filter.py`
- `self_dual_wreath_invariant_projector_circuit.py`
- their artifacts under `research/representation/`
- their focused tests under `tests/`

For a selected orientation subspace `H=F_2^r`, let
`F_H=|H|^-1 sum_h E_h`. Coherently control `E_h`, Fourier transform the
orientation register, and accept a nontrivial character. Character
orthogonality gives the exact effect

`D_H=F_H-F_H^2`.

It is positive, has spectrum at most `1/4`, and annihilates
`intersection_h Ran(E_h)` exactly. This is the first nonlocal filter in the
repository that attacks a selected common core at unit scale rather than
resolving its `|H|/2^k` weight inside the full frame. Seventy-six finite
controls, including all 75 collision-free `W_4` target blocks, validate the
Kraus/Parseval identity.

The internal controlled projector is polynomial. Uniformly prepare
`s in S_n`, apply the target plus orientation-selected source irrep actions,
and unprepare. The top block is exactly
`E_h=(1/n!)sum_s U_h(s)`. Beals' efficient `S_n` QFT implements each irrep
action by conjugating reversible left multiplication. Two complete QFT
intertwining controls and 20 physical projected-block controls pass. No
factorial amplitude amplification or factorial precision is needed *once the
orbit-Gram carrier is available*.

### Physical-Access Obstruction For The Dual Filter

Files:

- `self_dual_wreath_orientation_filter_physical_access.py`
- `research/representation/self_dual_wreath_orientation_filter_physical_access.json`
- `tests/test_self_dual_wreath_orientation_filter_physical_access.py`

This is the required adversarial correction to the preceding positive result.
The orientation Fourier blocks live on the orbit-Gram domain. With synthesis
`T`, physical frame `B=TT^*`, and Gram operator `G=T^*T`, every direct
physical-to-dual filter of the form `D^(1/2)T^*`, `0<=D<=I`, has average
conclusive probability

`Tr(DG^2)/r <= Tr(B^2)/r`.

For the natural wreath ensemble this is `Theta(1/n!)`. Three exact finite
factorization controls pass; at `n=512` the direct-access success upper bound
has log2 `-3874.52`, and generic amplification costs log2 `1937.26`.

Therefore the dual circuit alone is **not** a physical algorithm: reaching
that domain through the obvious synthesis adjoint restores the factorial
barrier. The next subsection records the direct physical branch-interference
circuit that bypasses this specific factorization.

### Direct Physical Orientation Interference

Files:

- `self_dual_wreath_physical_orientation_interference.py`
- `research/representation/self_dual_wreath_physical_orientation_interference.json`
- `tests/test_self_dual_wreath_physical_orientation_interference.py`

The second escape in the preceding paragraph is now constructed. An unequal
wreath irrep has a physical induced-branch qubit. Known rectangular flips
align the two summands, exposing an `F_2^k` orientation register. For a chosen
subspace `H`, the circuit:

1. coherently resolves the diagonal `S_n` isotypic label;
2. applies a reversible binary basis change into `H` plus quotient bits;
3. Hadamard-transforms the `H` bits;
4. accepts a nontrivial `H` character.

This acts directly on the physical carrier and never invokes `T^*`. For every
target `nu`, it obeys the exact trace-transfer identity

`Tr(K_nu,H B K_nu,H^*) = d_nu |H|/2^k sum_q Tr(F_nu,q-F_nu,q^2)`.

Uniform random conjugation makes acceptance independent of the hidden
permutation. All 30 complete collision-free `W_4` controls, using both the
full orientation space and the diagonal block direction, pass. Retained trace
ranges from `0.4444` to `0.75`; covariance spread is below `2.3e-16`, and the
trace-transfer residual is below `2.3e-15`.

The earlier physical-access no-go remains correct **only** for filters that
factor through the direct synthesis adjoint. This direct branch circuit is an
explicit bypass, not a contradiction.

### Natural Information Retention Theorem

Files:

- `self_dual_wreath_orientation_retention_theorem.py`
- `research/representation/self_dual_wreath_orientation_retention_theorem.json`
- `tests/test_self_dual_wreath_orientation_retention_theorem.py`

For source pairs `(lambda_i,mu_i)`, the rejected fraction is exactly

`L_H=|H|^-1 sum_(u in H) (1/n!) sum_s product_(i:u_i=1) r_lambda_i(s)r_mu_i(s^-1)`.

Plancherel normalized-character orthogonality gives

`E[L_H]=1/|H|+(1-1/|H|)/n!`.

For `dim H=Omega(k)` at `k=ceil(log2(n!))`, Markov makes `L_H` smaller than
every fixed inverse polynomial with probability `1-o(1)`. Intersecting with
the existing all-distinct source event transfers this to the natural
collision-free unequal sector. Covariantization equalizes acceptance over
hidden labels, and a coherent implementation plus the gentle measurement
lemma preserves identification success up to `sqrt(L_H)`. Therefore the
existing information-theoretic `1/16` success remains constant after the
physical filter on typical natural tuples.

Thirty exact physical/character controls and eight exact Plancherel controls
through `n=10` pass. At `n=512`, expected rejection has log2 `-484` and the
Markov failure bound for rejection above `n^-10` has log2 `-394`.

This is the strongest positive result in the current pass. It proves a
polynomial direct filter and natural information retention. It does **not**
prove a polynomial postfilter frame norm, an efficient final POVM, a hidden
permutation decoder, or a classical separation.

### Exact Postfilter Frame Compression And Finite No-Gain Result

Files:

- `self_dual_wreath_postfilter_frame_compression.py`
- `research/representation/self_dual_wreath_postfilter_frame_compression.json`
- `tests/test_self_dual_wreath_postfilter_frame_compression.py`

Let `B` be the hidden-label average frame and let the direct filter Kraus
operators be `K_nu=Z_H U_H Pi_nu`. Because `B` commutes with every diagonal
`S_n` isotypic projector, **discarding** the isotypic label gives

`sum_nu K_nu B K_nu^* = Z_H U_H B U_H^* Z_H`.

This is an exact theorem, not a finite ansatz. But the intended circuit says
to retain the label coherently. Its average frame is instead

`direct_sum_nu Z_H U_H Pi_nu B Pi_nu U_H^* Z_H`.

Cross-label average blocks vanish, and the tagged norm is the maximum sector
norm. It can be strictly smaller than the discarded-label principal
compression. This distinction is essential because later decoding may
interfere the coherent label with the carrier.

If `q=rank(I-Z_H)`, Cauchy interlacing gives

`||Z_H U_H B U_H^* Z_H|| >= lambda_(q+1)(B)`.

For `dim(H)=r`, `q/D=2^-r`: a near-unit-retention filter can remove only that
fraction of spectral directions. The raw top norm is preserved exactly iff
the pulled-back accepted subspace `Ran(U_H^*Z_H)` intersects the top
eigenspace of `B`.

Thirty dense complete `W_4` controls verify both output-channel identities,
commutation, equality criterion, and interlacing. Matrix-free Lanczos covers
all 21 current collision-free `W_5` portfolios for the discarded-label
channel. Raw discarded-label top norm is preserved in 45 of 51 controls and
reduced in six. After normalization, none of those 51 improves.

The corrected coherent-tagged result is less negative. At `W_4`, 2 of 30
controls strictly improve conditioned norm, six more are unchanged, and 22
worsen. Complete matrix-free tagged-sector Lanczos over all 21 `W_5`
portfolios finds nine improvements and 12 regressions. The best `W_5` ratio is
`0.8592911`; the worst is `1.1627907`. Across both sizes, 11 of 51 improve.
This is a mixed finite signal, not an asymptotic sector theorem.

This kills the interpretation that discarding the isotypic label can help and
shows that common-core rejection alone is not uniformly useful. It does not
kill coherent tagging: the two finite gains are a real but sparse signal. The
decisive missing theorem is now sectorwise and quantitative: bound the maximum
tagged-sector norm on typical natural tuples while preserving cross-sector
coherence for the decoder.

### Logarithmic Orientation Rank-Retention Regime

Files:

- `self_dual_wreath_orientation_rank_budget.py`
- `research/representation/self_dual_wreath_orientation_rank_budget.json`
- `tests/test_self_dual_wreath_orientation_rank_budget.py`

For physical dimension `D=2^k C`, the exact trace identity is
`Tr(B)/D=2^-k`. Therefore, for every `A>=1`,

`rank(1[B>A 2^-k]) < D/A`.

An orientation subspace of dimension `r` rejects exactly `D/2^r` Hilbert
dimensions. Setting `A=2^r` matches the filter's rejection rank to the entire
high-spectrum count permitted by trace. This is a capacity theorem, not an
alignment theorem.

The correct calibrated regime is now

`r=ceil(a log2 n)`, `A=2^r in [n^a,2n^a)`.

For a retention threshold `n^-b`, `0<b<a`, the exact Plancherel expectation
and Markov give failure `O(n^(b-a))`; gentle information loss is
`O(n^-b/2)`. Thus logarithmic `r` gives all three necessary resources at once:

- a polynomial cutoff `A 2^-k`;
- enough rejection rank to cover the universal trace-allowed tail;
- acceptance `1-o(1)` and vanishing loss of the known constant information.

This replaces `r=Omega(k)` as the default design. Linear `r` proves far more
retention than necessary but rejects exponentially fewer Hilbert dimensions
than trace alone can justify. At `n=512`, the calibrated example uses `r=72`
instead of the old illustrative `r≈484`; its Markov failure bound is below
`2^-36` at rejection threshold `n^-4`.

The decisive missing result is **structured alignment**: prove that a selected
`Theta(log n)` subset of the available source-adapted block directions spans
the actual high-spectrum subspace, not merely the already-known common vector.

### Isotypic Dephasing Identification No-Go

Files:

- `self_dual_wreath_isotypic_dephasing_no_go.py`
- `research/representation/self_dual_wreath_isotypic_dephasing_no_go.json`
- `tests/test_self_dual_wreath_isotypic_dephasing_no_go.py`

For a uniform covariant ensemble under
`R(g)=direct_sum_nu rho_nu(g) tensor I_(M_nu)`, dephasing the irrep label makes
every state block diagonal. Covariant POVM symmetrization and Schur averaging
force the seed effect in sector `nu` to satisfy

`Tr_(V_nu)(E_nu)=d_nu/|G| I_(M_nu)`.

The positive-operator inequality

`X <= d I_d tensor Tr_(C^d)(X)`

then gives the exact decoder bound

`p_success <= sum_nu p_nu d_nu^2/|G| <= max_nu d_nu^2/|G|`.

For `G=S_n`, this is the largest Plancherel atom. Aggarwal--Elboim's maximal
dimension theorem makes it `exp(-(2d+o(1))sqrt(n))`, `d>0`. Data processing
extends the bound through every later filter, unitary, ancilla, and decoder.
Multiplicity spaces do not evade it.

Therefore **any architecture that classically samples `nu` or runs independent
sector decoders is asymptotically dead for constant-success exact hidden-
permutation recovery**. The isotypic transform must remain coherent, and the
final decoder must exploit cross-`nu` coherences. The average tagged frame is
block diagonal, but individual hidden states retain cross-sector terms in the
label/carrier system; those terms are now a proved necessary resource.

The theorem does not rule out coherent cross-sector decoding or a coarser
trivial-vs-nontrivial decision problem.

### Coherent Fourier Decoder Criterion

Files:

- `self_dual_wreath_coherent_fourier_decoder.py`
- `research/representation/self_dual_wreath_coherent_fourier_decoder.json`
- `tests/test_self_dual_wreath_coherent_fourier_decoder.py`

The surviving decoder architecture is now an exact mathematical target. For
any finite group,

`|F_g> = direct_sum_nu sqrt(d_nu/|G|) vec(rho_nu(g))`

is the nonabelian Fourier image of `|g>`. Consider a coherent covariant state

`|psi_g> = direct_sum_nu sqrt(p_nu) (rho_nu(g) tensor I)|phi_nu>`.

If the row/multiplicity Schmidt probabilities in sector `nu` are
`lambda_nu,i`, define

`f_nu=d_nu^-1/2 sum_i sqrt(lambda_nu,i)`.

The exact correct-label probability after inverse group QFT is

`P=[sum_nu d_nu sqrt(p_nu/|G|) f_nu]^2`.

Therefore perfect decoding occurs when:

- `p_nu=d_nu^2/|G|` coherently (Plancherel amplitudes);
- every sector exposes an aligned dual row/column register with a flat Schmidt
  spectrum (`f_nu=1`).

Four exact `S_3`/`S_4` Young-matrix controls verify Fourier unitarity and the
success formula for ideal, weight-mismatched, Schmidt-mismatched, and rank-one
states. The ideal control decodes with probability one.

For `S_n`, Beals makes the final inverse QFT polynomial. This removes “there
are `n!` outcomes” as the conceptual decoder bottleneck: a permutation is only
`O(n log n)` bits and Fourier synthesis outputs it directly. The hard core is
now **coherent carrier normalization**:

1. extract an aligned dual row register from the physical multiplicity carrier;
2. flatten its sector Schmidt spectrum;
3. reweight coherent sector amplitudes to Plancherel;
4. preserve cross-sector phase throughout;
5. apply inverse `S_n` QFT.

No physical extraction, flattening, or polynomial reweighting theorem exists
yet, so this is a research architecture, not an algorithm claim.

### Constant-Success PGM And Quantum-Sampling Normal Form

Files:

- `self_dual_wreath_pgm_success_theorem.py`
- `self_dual_wreath_covariant_pgm_factorization.py`
- `self_dual_wreath_pgm_truncation_robustness.py`
- `self_dual_wreath_pgm_spectral_window.py`
- `self_dual_wreath_pgm_quantum_sampling_reduction.py`

The full covariant projector ensemble has all-n PGM success

`p_PGM >= 1/[1+(n!-1)2^-k]`.

At `k=ceil(log2 n!)` this is constant. Covariance removes the explicit
`sqrt(n!)` Petz environment charge and reduces the PGM to controlled carrier
polars. In an isotypic sector,

`A_nu|m> = sum_j |j> tensor P|nu,j,m>`, `A_nu^*A_nu=D_nu`,

so the required carrier isometry is `A_nu D_nu^-1/2`. The orientation factor
has the equivalent nonorthogonal quantum-sampling form

`R_nu|x> = sum_epsilon |epsilon> E_(nu,epsilon)|x>`.

Truncation removes dependence on the actual minimum eigenvalue, and a fixed
condition-number window of `n! B` retains constant PGM success. Neither result
makes generic QSVT polynomial: raw access still sees a `Theta(1/n!)` scale.
The surviving route must implement the structured polar of `R_nu`, not a
black-box inverse.

### Hierarchical Orientation Polar Chain

Files:

- `self_dual_wreath_pair_polar_sampler.py`
- `self_dual_wreath_hierarchical_polar_tree.py`
- `self_dual_wreath_relative_effect_intersection.py`
- `self_dual_wreath_common_core_polar_bypass.py`
- `self_dual_wreath_early_level_overlap_localization.py`

For a subtree `T=L union R`, put `S_T=sum_(epsilon in T)E_epsilon`. The exact
chain rule is

`Q_T=(Q_L direct_sum Q_R)[S_L^1/2;S_R^1/2]S_T^-1/2`.

The left relative effect is

`C=S_T^-1/2 S_L S_T^-1/2`.

The pair level is polynomial: every noncommon principal correlation is at most
`1/(n-1)`, so the two-projector polar has constant condition. The number of
strictly fractional eigenvalues of `C` is exactly

`dim(range(S_L) intersect range(S_R))`.

This localizes every weighted conditional channel to a child-span
intersection. Exponential block-common cores are not an obstruction to an
aligned tree: each balanced split acts as exactly `C=I/2` on the core. This
explicitly supersedes the old interpretation that recurring-irrep incidence
closed every overlapping transform. Off exact common ranges, child spans are
provably disjoint through `O(log n)` early levels; the theorem does not reach
the full `Theta(n log n)` depth.

### Physical PGM Transfer Is Compiled

Files:

- `self_dual_wreath_polar_factor_transfer.py`
- `self_dual_wreath_physical_pgm_intertwiner.py`
- `tests/test_self_dual_wreath_physical_pgm_intertwiner.py`

Equal Gram factors do not generically expose their output intertwiner. The
wreath factor has additional covariant structure that closes this gate. After
the explicit induced-branch alignment, generalized coherent `S_n` Fourier
sampling gives the row-copy isometry

`C_U|nu,a,m> = d_nu^-1/2 sum_b |nu,a,b>|nu,b,m>`.

Its branch-`epsilon` residual lies exactly in
`range(E_(nu,epsilon))`, and for every coherent Fourier row

`A_(nu,a)=2^(-k/2) R_nu^* C_(U,nu,a)`.

Therefore the physical PGM coisometry is exactly

`(A A^*)^-1/2 A = Q_R^* C_(U,nu,a)`.

This uses a uniform permutation register, controlled diagonal restriction
action, and the Beals `S_n` QFT. It does not compute a Kronecker multiplicity
basis, use the factorially weak synthesis adjoint, or dephase `nu`. Three
physical W3/W4 controls pass. **The physical-output transfer gate is closed.**
The all-n orientation polar `Q_R` is now the sole PGM implementation gate.

### Level-Three Linear-Flag Audit

Files:

- `self_dual_wreath_level_three_flag_audit.py`
- `research/representation/self_dual_wreath_level_three_flag_audit.json`
- `tests/test_self_dual_wreath_level_three_flag_audit.py`

Every ordered basis of `F_2^3` was enumerated: 168 linear flags and seven
merges per flag. Across selected collision-free W5 sectors and the
pairwise-distinct W3 triangle control, every fractional relative eigenvalue is
exactly `1/2`. The current artifact contains 4,704 merge occurrences and 2,520
fractional eigenvalue occurrences.

This is structural, not generic. A fully repeated unequal label produces 648
nonhalf occurrences with exact values including `1/3`, `4/9`, `5/9`, and
`2/3`. Any all-n theorem must use collision-free or stronger label structure.

The old carrier-core explanation for this pattern is now falsified and must
not be used as the all-n conjecture. The replacement results follow.

### Affine Carrier Cores Are Sufficient But Not Necessary

Files:

- `self_dual_wreath_affine_core_flag_theorem.py`
- `research/representation/self_dual_wreath_affine_core_flag_theorem.json`
- `tests/test_self_dual_wreath_affine_core_flag_theorem.py`

An affine leaf-incidence core is routed by every linear flag with weights only
`0,1/2,1`; a nonaffine three-point core gives `1/3` and `2/3`. This theorem is
exact. However, actual label-distinct W3 overlaps are pairwise-emergent and do
not reduce the leaves, while remaining exactly half-balanced. Selected W5
overlaps also fail leaf reduction. Therefore **exhaustion by reducing affine
carrier cores is not the governing mechanism**.

### Exact Shorted-Overlap Balance Criterion

Files:

- `self_dual_wreath_shorted_overlap_balance.py`
- `research/representation/self_dual_wreath_shorted_overlap_balance.json`
- `tests/test_self_dual_wreath_shorted_overlap_balance.py`

For `A,B>=0`, `K=range(A) intersect range(B)`, and isometry `U` onto `K`, set

`G_A=U^*A^+U`, `G_B=U^*B^+U`.

The fractional spectrum of `(A+B)^-1/2 A (A+B)^-1/2` is exactly the
generalized spectrum of `(G_B,G_A+G_B)`. Hence every fractional channel is
`1/2` iff `G_A=G_B`, equivalently iff the shorted operators of `A` and `B` to
`K` agree. This is now the exact all-n target. It predicts every repeated-
label nonhalf value and has zero finite validation failures.

### Canonical Coefficient-Space Affine Normal Form

Files:

- `self_dual_wreath_canonical_coefficient_affine.py`
- `research/representation/self_dual_wreath_canonical_coefficient_affine.json`
- `tests/test_self_dual_wreath_canonical_coefficient_affine.py`

For child frame `A=sum_e E_e`, the minimum-norm leaf maps
`D_e=E_e A^+U` obey `sum_e D_e=U` and
`sum_e D_e^*D_e=G_A`. All 20 label-simple fractional merges tested have
`G_A=G_B=gI`, scalar equal component effects, and affine active mask support.
W3 uses the affine plane `{0,2,5,7}`; W5 uses the affine line `{3,6}`.
Repeated labels fail ten certificates. The affine structure therefore lives
in the canonical coefficient register, not in reducing carrier cores.

The maps still contain `A^+`. They are a structural normal form, not a
circuit.

### Isolated Single-Anchor Shorting

Files:

- `self_dual_wreath_single_anchor_shorting.py`
- `research/representation/self_dual_wreath_single_anchor_shorting.json`
- `tests/test_self_dual_wreath_single_anchor_shorting.py`

If `K` lies in anchor leaf `E_a` and is orthogonal to
`range(E_a) intersect span(other child leaves)`, minimum-energy synthesis uses
only the anchor and the shorted child operator is exactly `P_K`. A duplicate-
core leaf falsifies the premise and changes the metric. All 11 selected W5
fractional merges are explained exactly by the unique anchor pair `{3,6}` and
a five-dimensional core. No all-n isolated-anchor decomposition is proved.

### Flat Affine Recoupling Bundle

Files:

- `self_dual_wreath_affine_recoupling_bundle.py`
- `research/representation/self_dual_wreath_affine_recoupling_bundle.json`
- `tests/test_self_dual_wreath_affine_recoupling_bundle.py`

Uniform scalar coefficient maps define isometric fibers `V_e`; their
transports `T_(f,e)=V_fV_e^*` are exact flat partial isometries. An affine
support can therefore be prepared by affine Hadamards plus controlled
generator transports if those transports have explicit circuits. W5's line
transport is identity. W3's plane transports are nontrivial, with generator
fiber-map difference as large as `sqrt(3)`. A repeated-label balanced control
has equal child metrics but nonscalar fibers on a nonaffine six-mask support.

### Pair-Polar Transport Network And Degree Gate

Files:

- `self_dual_wreath_pair_polar_transport_network.py`
- `self_dual_wreath_pair_transport_degree_obstruction.py`
- `research/representation/self_dual_wreath_pair_polar_transport_network.json`
- `research/representation/self_dual_wreath_pair_transport_degree_obstruction.json`
- corresponding tests under `tests/`

Every finite W3 fiber transport is a path of at most two leaf-pair polar maps;
the overlap graph is `K_(2,2)` and endpoint gauges are `+I` or `-I`. W5 uses
one direct common-range edge. This is a finite compilation, not an asymptotic
one.

For carrier `alpha`, pair correlation is `c=1/d_alpha`. Any bounded QSVT
polynomial implementing the polar sign on the normalized cross-overlap needs
degree at least

`(1-epsilon)sqrt(1-c^2)/c = Omega(d_alpha)`.

This does not contradict the constant-conditioned stacked pair sampler based
on `E+F`; the two access problems are different. It also does not rule out an
explicit Racah transform outside the cross-overlap QSVT model.

### Transport Carrier-Mass Falsifier

Files:

- `self_dual_wreath_transport_carrier_mass.py`
- `research/representation/self_dual_wreath_transport_carrier_mass.json`
- `tests/test_self_dual_wreath_transport_carrier_mass.py`

Exact representation-ring probes on deterministic natural high-dimension
portfolios show that low-dimensional pair carriers are not typical by
multiplicity. At `n=12,k=29`, sampled intermediate distances have weighted
median carrier dimension `5775`; at most `5.9e-8` of pair-overlap multiplicity
lies in dimensions at most `n^2`, and RMS correlation is at most `2.1e-4`.
This falsifies a generic typical-mass argument for cheap transports. It is not
an algorithm lower bound because the candidate affine fiber may align with an
exceptional low-dimensional sector.

Literature scope warning:

- Moore, Russell, and Sniady, *On the Impossibility of a Quantum Sieve
  Algorithm for Graph Isomorphism*, `https://arxiv.org/abs/quant-ph/0612089`.

Their lower bound rules out Kuperberg-style adaptive tensor-product sieves on
the wreath-product GI reduction in less than `exp(Omega(sqrt(n)))` time. Do
not mutate this filter into a pairwise/small-register Clebsch-Gordan sieve.
The current circuit is outside that stated model only because it performs a
single globally entangled `Theta(n log n)`-register isotypic measurement and
orientation transform. Any claim that it lies outside the theorem must be
checked against the paper's formal algorithm class, not inferred from naming.

## Superseding Dependency And Recoupling Results

The following results replace the earlier conjecture that every
collision-free affine merge is exactly half-balanced.

### Cross-Dependency Normal Form And Cayley Boundary

Files:

- `self_dual_wreath_cross_dependency_neutrality.py`
- `self_dual_wreath_cayley_fiber_reduction.py`
- `self_dual_wreath_matrix_cayley_boundary.py`
- matching artifacts and tests under `research/representation/` and `tests/`

For child syntheses `R_L,R_R`, the canonical cross-dependency space is

`W=ker[R_L,-R_R] intersect (ker R_L direct_sum ker R_R)^perp`.

If `J=diag(I,-I)`, every fractional relative eigenvalue is
`lambda=(1-delta)/2` for `delta in spec(P_W J P_W|_W)`. Exact half-balance is
therefore equivalent to total grading neutrality of `W`.

Scalar XOR-Cayley fibers Fourier-reduce to `[[c,d],[d,c]] tensor I` and are
half-balanced. Matrix-valued Cayley kernels are balanced exactly when their
opposite saturation spaces are orthogonal. A two-dimensional positive
counterfamily gives channels `(1 +/- 1/sqrt(2))/2`; XOR covariance alone is
not a proof.

### Sparse Invariant Dependencies And Weighted Exclusion

Files:

- `self_dual_wreath_sparse_invariant_dependency.py`
- `self_dual_wreath_weighted_overlap_exclusion.py`
- matching artifacts and tests

Invariant leaf ranges are extracted from representation multiplicities and
small coefficient Grams, avoiding dense ambient projectors. S6 controls reach
ambient dimension 22,500, multiplicity five, and seven active orientations.

For common-free leaves with weights `w_ij=||U_i^*U_j||`, the exact comparison
bound is

`||P_LP_R|| <= ||W_LR|| / sqrt((1-rho(W_LL))(1-rho(W_RR)))`.

It strictly excludes all 1,920 screened common-free S6 affine merges. W3 is
the sharp norm-one boundary. This does not handle exact pair-common sectors.

### Pair-Common Homology

Files:

- `self_dual_wreath_dependency_homology.py`
- `research/representation/self_dual_wreath_dependency_homology.json`
- `tests/test_self_dual_wreath_dependency_homology.py`

Let `W_pair` be the span in `W` of exact two-leaf common relations and
`H_em=W/W_pair`. W3 has genuine neutral emergent homology. Earlier W5/S6
controls are pair-generated, but this is not a neutrality theorem.

The new globally distinct S6 control
`W6-COLLISION-FREE-NONCOMMUTING-CORE` has a 34-dimensional child intersection,
is entirely pair-generated, and has grading defect `1/17`. Its channels are:

- nine at `8/17`;
- sixteen at `1/2`;
- nine at `89/170`.

This is a full affine-merge counterexample, not merely a reduced pair model.
Universal collision-free half-balance is false.

### Affine Common Supports And Noncommuting Core Counterexample

Files:

- `self_dual_wreath_common_core_atomization.py`
- `research/representation/self_dual_wreath_common_core_atomization.json`
- `tests/test_self_dual_wreath_common_core_atomization.py`

The fixed-family parity formula is now realized by explicit orthonormal
trivial/sign intertwiners. There is also an all-`n>=5` support theorem:

`intersection(U_a,U_b,U_c) subset U_(a xor b xor c)`.

Summing the three parity equations gives the fourth orientation's invariance
equation. Hence every exact common vector has affine orientation support, and
any support crossing affine sibling cosets meets them equally. Unequal support
counts are not the source of the S6 defect.

The actual obstruction is noncommuting recoupling. In the counterexample,
balanced affine line cores have principal correlation `1/9` but nonzero
commutator norm `0.110423...`. A direct relative Cech quotient reproduces the
nonhalf spectrum above. This falsifies both universal pair-core commutativity
and the claim that affine support balance alone implies half-balance.

### Pair-Core Recoupling Boundary

Files:

- `self_dual_wreath_pair_core_recoupling_boundary.py`
- `research/representation/self_dual_wreath_pair_core_recoupling_boundary.json`
- `tests/test_self_dual_wreath_pair_core_recoupling_boundary.py`

Two local scalar recoupling laws are exact. With carrier correlation
`gamma=1/d`, an open two-cross-edge star has channels

`(1-gamma)/(2-gamma)` and `(1+gamma)/(2+gamma)`.

After quotienting an equicorrelated internal edge, the high channel becomes

`(1+gamma-gamma^2)/(2+gamma-gamma^2)`.

Selected S6 controls realize `d=5,9,10` exactly. A deterministic screen of 180
controls and 560 pair-core stars found 393 fractional correlations, all equal
to `1/5`, `1/9`, or `1/10`; none exceed `1/(n-1)`. This is finite evidence,
not an all-n carrier-factorization theorem.

If `gamma<=1/(n-1)` and `n>=5`, every isolated scalar star lies in
`[3/7,5/9]`. Nonhalf local blocks are therefore not automatically hard. A
weighted Schur-comparison theorem certifies all three selected endpoint gaps.
However, a broader 100-control, 6,766-merge audit left 33 cases uncertified by
the sign-blind absolute-weight bound even though the exact maximum defect was
only `1/9`. Cech-cycle cancellations and recoupling phases are essential.

### Relative Common-Core Cech Laplacian

Files:

- `self_dual_wreath_common_core_cech_laplacian.py`
- `research/representation/self_dual_wreath_common_core_cech_laplacian.json`
- `tests/test_self_dual_wreath_common_core_cech_laplacian.py`

The phase-sensitive chain groups are

`C_p = direct_sum_(|F|=p+1) intersection_(e in F) U_e`,

with alternating inclusion boundaries. The pair-relation Gram is
`G_1=D_1^*D_1`, so `G_1D_2=0`; `H_1=ker D_1/im D_2` is the pair-cycle
homology not generated by higher common cores.

Three hard S6 affine planes and one eight-orientation affine cube pass. In the
four-way-core controls, the pair
kernel has dimension three and the four triple cells have boundary rank three;
the quadruple cell gives the one relation among those triples. All positive-
degree homology vanishes. The dense control that defeats the sign-blind bound
has exact pair-Laplacian positive spectrum `[2,4]` after the Cech cycle
quotient. The eight-orientation cube has 12 pair cores, the same exact
three-dimensional higher-cell cycle, positive spectrum `[17/9,4]`, and a real
grading defect `1/17`; its sign-blind comparison bound is infinite. This is a
finite pair-cycle prototype only and does not test the augmented leaf-
dependency quotient.

### Sparse Parity Kernel And Augmented Common-Core Cech

Files:

- `self_dual_wreath_orientation_triple_range.py`
- `self_dual_wreath_common_core_atomization.py`
- `self_dual_wreath_augmented_common_core_cech.py`
- `research/representation/self_dual_wreath_augmented_common_core_cech.json`
- `tests/test_self_dual_wreath_augmented_common_core_cech.py`

The old fixed-family implementation enumerated all `2^(2^m-1)` formal parity
assignments, including empty membership patterns forced into the trivial
isotype. It is now an exact sparse XOR dynamic program over at most `2k+1`
occupied patterns for `k` labels. A separate compact enumeration constructs
only viable occupied-pattern intertwiners. This makes eight-orientation cells
exactly computable without changing the theorem.

The Cech complex is now augmented by leaf synthesis:

`... -> C_2 -> C_1 -> C_0 -> V`,

so `H_0=ker(D_0)/im(D_1)` measures many-leaf dependencies not generated by
pair common cores. This is logically independent of the prior `H_1` pair-cycle
audit. The direct W3 distinct plane has `H_0=2` and no pair cores. The repeated
W3 plane has four raw leaf dependencies, pair-boundary rank three, and
`H_0=1`. These exactly reproduce the independent dependency-homology audit.
They are adversarial controls outside the `n>=5` parity theorem, not an all-n
counterexample.

A selected W5 plane is augmented-exact: raw dependency dimension five and
pair-boundary rank five. A low-ambient (`625`) full depth-three W6 cube has all
simplex cells through degree seven, zero homology in every degree, and Hodge
spectrum bounded between `2` and `8`. It is deliberately labeled factorized:
it tests the sparse all-depth machinery but not noncommuting multicarrier
holonomy. Universal pair generation for natural `n>=5` portfolios remains a
separate theorem gate.

### Recursive Pair Generation And Complete S5 Boundary

Files:

- `self_dual_wreath_recursive_pair_generation.py`
- `research/representation/self_dual_wreath_recursive_pair_generation.json`
- `tests/test_self_dual_wreath_recursive_pair_generation.py`

There is an exact short sequence at every sibling merge. If `W/W_pair` is the
cross-dependency quotient after all internal child syzygies are removed, then

`dim H0(parent) = dim H0(left) + dim H0(right) + dim(W/W_pair)`.

The identity recovers the distinct W3 root `H0=2` and repeated W3 root `H0=1`
entirely in the cross quotient, while the selected globally distinct W5 plane
has zero at every node.

The optimized exact screen covers all 105 perfect-match portfolios formed from
six distinct S5 partitions, all seven targets, all 14 affine planes, and the
full orientation cube: 11,025 affine nodes total. Every node has `H0=0`; raw
dependency dimension reaches eight, and the maximum direct `D0D1` residual is
below `2e-15`. This is the complete globally distinct, three-label S5
boundary, not an all-n theorem. A separate live S6 low-dimensional screen
checked all 15 pairings of the six degree-at-most-five-dimensional source
partitions over all 11 targets (165 controls) with no emergent H0; it is not
yet a dedicated artifact.

### Pair-Core Quotient Overlap Criterion

Files:

- `self_dual_wreath_pair_quotient_overlap.py`
- `research/representation/self_dual_wreath_pair_quotient_overlap.json`
- `tests/test_self_dual_wreath_pair_quotient_overlap.py`

For child spans `A,B`, let `K` be the physical span of all crossing leaf-pair
common cores. Crossing pair relations generate exactly `K` after internal
dependencies are quotiented. Therefore the local emergent quotient vanishes
exactly when

`||P_(A minus K) P_(B minus K)|| < 1`.

This isolates the exact phase-sensitive all-n norm target. W3 reaches one and
recovers emergent dimensions two/one. A pair-rich W5 node has `dim K=5`, no
emergent quotient, and exact residual gap `0.659504...`.

The residual absolute-weight graph is not generally adequate. A screen of 539
affine merges for one complete S5 portfolio found 12 phase-only certificates.
The promoted control has exact residual gap `0.591089...`, but the sign-blind
bound is infinite because one child's internal weight radius reaches one.
Thus even common-free pair generation may require signed/Racah block control;
scalar weighted graphs cannot be the all-depth proof.

The canonical Gram-factor screen for the selected globally distinct S6
portfolio covers nine active targets and 693 affine merges. No emergent cross
quotient appears; the minimum exact residual gap is `0.7375`, the minimum
pair-rich gap is `0.8`, and 12 merges are phase-only. These larger finite gaps
are encouraging but do not imply monotonicity or an asymptotic lower bound.

## Exact Pair-Core Carrier Factorization

Files:

- `self_dual_wreath_pair_core_carrier_factorization.py`
- `research/representation/self_dual_wreath_pair_core_carrier_factorization.json`
- `tests/test_self_dual_wreath_pair_core_carrier_factorization.py`

This closes the former open derivation 1. Grade every tensor factor of a
three-orientation family `{a,b,c}` by its membership pattern and write
`m_P(alpha)` for the isotypic multiplicities of block `T_P`. The blocks split
into cluster one `{T_a,T_ab,T_ac,T_abc}`, cluster two `{T_b,T_c,T_bc}`, and the
spectator `T_empty`. Because both pair cores are one-dimensional isotypes on
their groups, both are graded by every block's isotypic label, so the overlap
operator is block diagonal in that grading and never needs the ambient space.
Inside a block the carriers are forced to one irrep per cluster, and
contracting the four (respectively three) maximally entangled carrier pairs
gives the exact closed form

`B_ab^* B_ac = direct_sum (1/(d_beta d_p)) W`, `W` a partial isometry,

with exact multiplicity

`m_a(b) m_ab(b^d') m_ac(b^d) m_abc(b^{d xor d'}) * d_p m_b(p) m_bc(p^d) m_c(p^{d xor d'}) * dim T_empty`,

where `alpha^0=alpha` and `alpha^1` is the conjugate partition.

Three consequences matter.

1. The conjectured single-reciprocal `1/d_alpha` law is **false in general**.
   The exact value is a two-carrier product. Every earlier finite screen saw
   single reciprocals only because its membership blocks were singletons,
   which forces the second carrier to be one dimensional.
2. There is **no nontrivial multiplicity-space Racah/6j block** for a
   shared-vertex star. Two pairings of four self-dual carriers into invariants
   contract to the scalar `1/d`. Genuine Kronecker content first appears for
   vertex-disjoint pair cores, where a waist bound replaces the scalar law.
3. A correlation equals one exactly when both carriers are one dimensional.
   Two isotype channels can meet in one carrier sector only when both carriers
   are self-conjugate, hence of dimension at least `n-1`, and the collision
   term `4/(n-1)^2` is dominated for `n>=5`. Therefore **every off-common star
   correlation is at most `1/(n-1)` for all `n>=5`**, which upgrades the
   180-control reciprocal screen to a theorem.

Validation: 168 screened controls plus the three named `d=5,9,10` controls
reproduce every dense ambient singular value, rank, and multiplicity with
maximum residual `5.83e-16`. Forty vertex-disjoint controls respect the waist
bound and are exactly tight on all forty. Forty repeated-source-label controls
outside the collision-free sector obey the same closed form, so the theorem
does not depend on global distinctness. Ten focused tests pass.

## Sign-Blind Multistar Route Is Dead At Natural Depth

Files:

- `self_dual_wreath_multistar_degree_obstruction.py`
- `research/representation/self_dual_wreath_multistar_degree_obstruction.json`
- `tests/test_self_dual_wreath_multistar_degree_obstruction.py`

This settles former open derivation 4 in the negative for the technique the
repository was using. Block Gershgorin on the crossing relation Gram needs

`max_e sum_{f adjacent to e} ||G_ef|| < 2`.

The carrier factorization makes every term exact, and a sibling merge has a
complete bipartite crossing graph, so each live edge has exactly
`2(2^(j-1)-1)` adjacent crossing edges at merge depth `j`. Deterministic
sampling on the natural high-dimension collision-free threshold portfolios
gives:

| `n` | `k` | live stars | mean off-common weight | projected degree (log2) |
| --- | --- | --- | --- | --- |
| 7 | 7 | 14/40 | `2^-10.86` | `-3.88` |
| 8 | 11 | 29/40 | `2^-8.81` | `2.19` |
| 9 | 15 | 39/40 | `2^-4.93` | `10.07` |
| 10 | 21 | 40/40 | `2^-3.66` | `17.34` |
| 11 | 26 | 40/40 | `2^-3.61` | `22.39` |
| 12 | 29 | 40/40 | `2^-3.57` | `25.50` |

The mechanism is visible in the data. At `n=7` no sampled star has a
one-dimensional carrier and every weight is a small two-carrier product. By
`n=12` thirty-seven of forty sampled stars have a one-dimensional carrier in
one cluster and the mean weight has reached `0.975` times `1/(n-1)`. That is
Sellke covering saturating the membership blocks, the same mechanism already
used by the Plancherel block obstruction. Weighted degree therefore grows like
`2^(j-1)/(n-1)`, which is `Theta(n!/n)` at `j=k=ceil(log2 n!)`.

Conclusion: **no absolute-weight comparison can certify the residual quotient
at natural depth.** The 33 of 6,766 finite planes the sign-blind bound failed
to certify were not an edge case; they were the leading edge of the asymptotic
regime. The certificate is already vacuous at `n=8`.

The surviving object is identified. Let `C` be the signed subspace incidence
map sending an edge coefficient in `K_e` to `+` its vector at one endpoint and
`-` at the other. Then `C^*C` is exactly the relation Gram the Cech modules
already use, and `CC^*` is the projector-weighted orientation Laplacian

`Delta = D - A`, `D_uu = sum_{e containing u} P_{K_e}`, `A_uv = P_{K_uv}`.

Their positive spectra coincide; two finite controls verify this with maximum
residual `4.2e-14`. All-depth conditioning is therefore a **subspace
connectivity** question about projector-weighted orientation graphs, not a
weighted-degree question. No Laplacian gap is proved. Eight focused tests pass.

## Model-Scope Analysis For The Two Literature Lower Bounds

These are reasoning notes, not resolved obligations. They exist so the next
pass does not have to re-derive the scope question.

### Moore--Russell--Sniady

`https://arxiv.org/abs/quant-ph/0612089` rules out Kuperberg-style adaptive
sieves on the wreath-product graph-isomorphism reduction below
`exp(Omega(sqrt n))`. Their algorithm class combines a bounded number of coset
registers at a time, applies Clebsch-Gordan, and measures or discards between
combination steps.

The hierarchical polar tree superficially looks like such a sieve because it
recurses on sibling merges. Complete-bipartite crossing structure and a
globally coherent `Theta(n log n)`-register description suggest a mismatch
with locally measured pairwise combination, but they do not prove one. Early
measurement can preserve a decision effect, and a sequential transcript POVM
can encode more than one fixed projective block decomposition.

Before any speedup claim, the complete polar tree must be written in MRS's own
formal algorithm model and its physical decision effect must be separated from
all classical postprocessings of the allowed adaptive transcript POVM, or a
simulation must be given. The existing degree obstruction is not that
separation.
Do not infer the separation from naming, and do not mutate the current filter
into a pairwise or small-register Clebsch-Gordan sieve.

### Ozols--Roetteler--Roland

The rejection-sampling lower bound is a *state conversion* bound, and the
repository currently holds an *information* bound (`1/16` PGM success) and a
*filter retention* bound. These are not comparable as stated. The decisive
missing computation is explicit: take the coherent Fourier decoder criterion's
sector Schmidt probabilities `lambda_{nu,i}`, form the source amplitude vector
of the physical post-filter frame state and the target amplitude vector
required by `p_nu=d_nu^2/|G|` with flat `f_nu=1`, and evaluate the
water-filling cost of that conversion. Until that vector pair is written down,
no claim that representation labels evade the oracle model is admissible.

## Width-Independent Metric Floor: The Sign-Blind Pessimism Is Withdrawn

Files:

- `self_dual_wreath_orientation_laplacian_gap.py`
- `research/representation/self_dual_wreath_orientation_laplacian_gap.json`
- `tests/test_self_dual_wreath_orientation_laplacian_gap.py`

The previous pass proved that absolute-weight comparison is vacuous at natural
depth and left the impression that the hierarchy is badly conditioned. **That
reading was wrong, and this section supersedes it.** Keeping the incidence
signs shows the relation metric does not degrade with merge width at all.

**Dirichlet form.** For the signed subspace incidence map `C` and
`Delta = CC^*`,

`<x, Delta x> = sum_e ||P_(K_e)(x_a - x_b)||^2`,

so `ker Delta` is exactly the set of vertex assignments whose edge differences
avoid every live pair core.

**Commuting case, solved exactly.** When the live pair-core projectors commute
they have Boolean atoms `A_S` and

`M = direct_sum_S L_S tensor I_(A_S)`,

with `L_S` the scalar graph Laplacian of the atom's edge set. The affine-
support theorem forces each atom's orientation set to be an affine subspace,
so `S` is a **complete** graph and `lambda_2(L_S) = |F_S| >= 2`. Hence
`lambda_min+(M) >= 2` **regardless of how many pair cores meet one
orientation**. Both commuting controls reproduce the atom prediction exactly,
with every atom support affine.

**Exact p-star law.** For a star of `p` edges at one vertex with residual
correlation `gamma`,

`spec(M) = {2-gamma} with multiplicity p-1, together with 2+(p-1)gamma`.

The smallest eigenvalue **does not move as `p` grows**. This reproduces the
known S6 noncommuting counterexample exactly: `gamma=1/9`, `p=3`, spectrum
`17/9` and `20/9`, residual `2.7e-15`. The `d=5` plane gives `gamma=1/5`,
`p=2`, spectrum `9/5` and `11/5`.

**Uniform-transport floor.** If the residual overlaps factor through vertex
isometries `W_(e,v)` with one common `gamma`, then

`M = 2(1-gamma)I + gamma C~^* C~`,

so `spec(M) = 2(1-gamma) + gamma spec(L~)` for the twisted graph Laplacian.
Since `C~^*C~` is positive semidefinite **for any holonomy**,

`lambda_min(M) >= 2 - 2 gamma >= 2 - 2/(n-1)`,

independent of merge width. At `n=12` that floor is `1.8182`; the sign-blind
estimate for the same merge was `-4.88e7`.

**Evidence.** 270 full-live-graph controls, zero violations of the
`2-2gamma_max` floor. On natural threshold portfolios the number of distinct
off-common correlations per sampled star collapses monotonically as the label
count grows — 16, 13, 8, 2, 1 for `n = 8,9,10,11,12` — reaching a **single**
value `1/(n-1)` at `n=12`. The same Sellke saturation that killed the
sign-blind bound is exactly what makes the transport uniform.

**Two traps recorded.** First, the floor is a statement about the **full live
graph**; evaluating the same form on a star subgraph deletes edges and drops
the minimum to `lambda_2` of a star, which is one. A screen that restricted to
star subgraphs produced 20 spurious "violations". Second, disjoint pair cores
overlap geometrically but contribute **nothing** to the relation Gram, whose
off-diagonal blocks are indexed by shared vertices only.

**Scope.** The vertex trivialization is a hypothesis. Only its
single-correlation half is measured; no isometry factorization is constructed
and the holonomy of the residual transport bundle is untested. Nothing here
bounds the graded form, so endpoint gaps for the relative polar are still
open, and no circuit follows.

## Natural Final-Root Common Span And Component Aspects

Files:

- `self_dual_wreath_final_root_natural_common_span.py`
- `research/representation/self_dual_wreath_final_root_natural_common_span.json`
- `tests/test_self_dual_wreath_final_root_natural_common_span.py`

This theorem removes the dimension/mass half of the final component-POVM
problem without assuming full support or Haar universality. Let
`g=|S_n|`, `K=ceil(log2 g)`, use the existing `C=K+2` source pairs, and split
the final orientation bit. Each child has `q=2^(C-1)` leaves and aspect
`a=q/g in [2,4)`. On the simultaneous leaf-rank event,

`(1-epsilon)D/g <= rank(E_e) <= (1+epsilon)D/g`

for the full target-carrier dimension `D`. The target factor `d_nu` cancels:
it multiplies both `D` and each physical leaf block. Do not reintroduce it as
an extra aspect penalty.

The exact sibling second moment gives

`E[Tr(A^2)+Tr(B^2)]/D = 2[a(1-g^-1)+a^2]`.

If `p_cf` is the all-`2C`-sources-distinct probability, positivity and
conditional Markov give, for `c>1`, an event of conditioned probability at
least `1-1/c` on which the left side is at most its expectation times
`c/p_cf`. This is not a total-variation argument and does not require a
bounded observable. Cauchy rank and
`dim(range A intersect range B)>=rank A+rank B-D` then give

`r/D >= 2(1-epsilon)^2 a p_cf/[c(a+1-g^-1)] - 1`.

Since `p_cf=1-o(1)` and the simultaneous rank failure is `o(1)`, choosing
`epsilon=1/64`, `c=9/8` proves

`Pr_cf[r/D >= 19/128-o(1)] >= 1/9-o(1)`.

On the same positive-mass event, child coefficient dimension `N` and maximum
leaf block `b_max` obey

`r/N >= 19/520-o(1)`,

`b_max/r <= (520/19+o(1))/q`.

Therefore the coordinate-defect bridge would give a full-rank asymptotic gap
at least `19/1040-o(1)` if every retained nonzero component eigenvalue obeyed
the still-unproved relative edge `delta>=(r/N)/2`. More generally a constant
factor `kappa` gives limiting gap `19 kappa/520`.

**What is now solved:** positive natural source mass, positive physical common-
span mass, constant final component fiber aspect, and `O(1/q)` block/fiber
ratio. A full-support theorem is unnecessary for these conclusions.

**What remains open:** the natural positive component eigenvalue edge (or a
mass-preserving tiny-edge trim), tightly normalized child pseudoinverse access,
coherent component-support SELECT, earlier relation-bearing node aspects,
recursive transport, and decoding. The old final-root leverage module is a
Haar/Gaussian edge theorem only; its schedule claim has been renamed explicitly
as a surrogate claim. Do not use the new dimension theorem to transfer the
Haar edge.

Finite artifacts through `S_48` deliberately leave the common-span lower bound
vacuous because exact global-distinct mass is still tiny there. That does not
contradict the asymptotic theorem, and those finite rows are not evidence for
the natural edge.

## Component Defect Has Constant Natural Support Mass

Files:

- `self_dual_wreath_component_defect_rank_mass.py`
- `research/representation/self_dual_wreath_component_defect_rank_mass.json`
- `tests/test_self_dual_wreath_component_defect_rank_mass.py`

For a component POVM `{H_e}` on an `r`-dimensional common fiber, define

`h_e=Tr(H_e)/r`,

`D_def=sum_e(H_e-h_e I)^2`.

Because this is a sum of squares,

`ker D_def = intersection_e ker(H_e-h_e I)`.

For every positive-trace component, `h_e>0`, so every vector in the defect
kernel is a nonzero-eigenvalue vector of `H_e` and lies in `range(H_e)`. Hence

`nullity(D_def) <= min_(h_e>0) rank(H_e)`.

Natural component effects are coordinate compressions, so
`rank(H_e)<=b_e` and therefore

`rank(D_def)/r >= 1-b_max/r`.

Combining this deterministic bridge with the final-root theorem above proves,
on globally distinct conditional source mass `1/9-o(1)`,

`rank(D_def)/r >= 1-(520/19+o(1))/q = 1-o(1)`.

Since `r/D_phys>=19/128-o(1)` on the same event, the conditioned expected
physical defect-support mass is at least

`(1/9)(19/128)-o(1)=19/1152-o(1)`.

This resolves the center-valued source/support-mass problem that the regular-
master reduction left open. It does so blockwise and rank-theoretically; it
does not infer source probability from an ordinary scalar defect trace.

**Do not overclaim the result.** Relative rank gives no lower bound on nonzero
defect or component eigenvalues. Coherent square-root preparation, support
SELECT, child pseudoinverses, and MRS separation remain open. In particular,
positive component nonscalarity on constant mass is only a structural input to
an MRS witness, not separation from every adaptive transcript policy.

## Component Hard Edge Replaced By An Input-Flatness Gate

Files:

- `self_dual_wreath_component_povm_spectral_trim.py`
- `research/representation/self_dual_wreath_component_povm_spectral_trim.json`
- `tests/test_self_dual_wreath_component_povm_spectral_trim.py`

For component POVM `{H_e}`, retain

`K_e=H_e 1_[tau,1](H_e)`

and reject the positive remainder

`L=I-sum_e K_e=sum_e H_e 1_(0,tau)(H_e)`.

If `B=sum_e rank(H_e)` and the incoming common-fiber density has flatness
`kappa=r||rho||_infinity`, then

`Tr L <= tau B`,

`Pr_rho[reject]=Tr(rho L) <= kappa tau B/r`.

The rejection probability is also exactly the mean-square error between the
ideal component Naimark map `stack_e sqrt(H_e)` and its accepted trimmed map
`stack_e sqrt(K_e)` on `rho`. Every retained nonzero effect eigenvalue is at
least `tau`.

At the natural final root, `B<=N` and `r/N>=19/520-o(1)`. Thus

`tau=eta(19/520)/kappa`

gives rejection at most `eta+o(1)`. Polynomial `kappa` produces an inverse-
polynomial cutoff; exact isotropy gives a constant cutoff. Consequently a
uniform natural component edge is not necessary for average-state dilation.

The flatness premise is real. An eight-outcome four-dimensional control has a
one-dimensional sector on which every effect eigenvalue is `1/8`. Trimming at
`tau=1/5` loses only `1/4` on the maximally mixed input but loses probability
one on the state concentrated in that sector. Do not use uniform trace loss as
a worst-case state claim.

**Next high-reasoning object:** derive the actual density entering each child
component dilation after the endpoint mixer. Prove polynomial flatness, prove a
state-specific weighted trim directly, or exhibit a natural concentration
counterfamily. Even a good cutoff still needs coherent effect access,
thresholding, failure flagging, support SELECT, and recursive error composition.

## Nonscalarity Is Not Noncommutative Effect Algebra

Files:

- `self_dual_wreath_component_effect_algebra_boundary.py`
- `research/representation/self_dual_wreath_component_effect_algebra_boundary.json`
- `tests/test_self_dual_wreath_component_effect_algebra_boundary.py`

The newly proved natural support mass concerns

`D_ns=sum_e(H_e-h_eI)^2`.

This detects failure of one global scalar distribution but does not detect
genuinely nonabelian measurement structure. The exact diagnostic is

`D_com=sum_(e<f)[H_e,H_f]^*[H_e,H_f]`.

`D_com=0` iff every pair of effects commutes, equivalently iff the generated
finite-dimensional C-star algebra is commutative. The regular-master lift
preserves this defect blockwise, so its central support is exactly the natural
source-block noncommutativity event.

The boundary is strict. A four-outcome orthogonal coordinate PVM has full-rank
`D_ns`, zero `D_com`, and generated algebra dimension four. The trine qubit
POVM has nonzero full-rank `D_com` and generates all of `M_2`. Therefore the
constant natural mass and asymptotically full rank proved for `D_ns` cannot be
reported as natural noncommutative component mass.

This correction changes the top research question. Prove positive central and
physical support of `D_com` for high-dimensional globally distinct final-root
blocks, or prove the effects asymptotically commute and exploit a coherently
accessible simultaneous eigenbasis. The finite S6 noncommuting effect remains
low-dimensional, asymptotically negligible evidence. Neither branch is yet
compiled, and no MRS conclusion follows.

## Natural Leaf Algebra Is Robustly Noncommutative

Files:

- `self_dual_wreath_natural_leaf_commutator_mass.py`
- `research/representation/self_dual_wreath_natural_leaf_commutator_mass.json`
- `tests/test_self_dual_wreath_natural_leaf_commutator_mass.py`

For a balanced orientation pair, the shared, left-only, and right-only source
patterns each contain `Theta(K)` independent Plancherel factors. Sellke's
constant-block covering theorem puts the standard irrep `(n-1,1)` into all
three pattern products with probability `1-o(1)`. A fixed target in the shared
pattern does not obstruct this: select a constituent `beta` of
`(n-1,1) tensor target^*` and use Frobenius reciprocity after the random product
covers `beta`.

The exact pair-angle theorem then supplies principal cosine `c=1/(n-1)`. On
that principal plane,

`||[E_a,E_b]|| = c sqrt(1-c^2)`.

Thus every fixed balanced pair has commutator norm at least

`sqrt(1-(n-1)^-2)/(n-1)`

with probability `1-o(1)`. Markov on the average bad-pair indicator upgrades
this to a density-one fraction of balanced pairs without requiring a Sellke
convergence rate. Balanced Hamming distances have density one, and global
distinctness also has probability `1-o(1)`.

This proves positive natural mass and an inverse-polynomial norm witness for
the **original leaf projector algebra**. It does not close the top component-
algebra gate. Canonical effects contain frame-inverse congruence and common-
span compression. The companion whitening no-go proves that frame condition
number, aspect, relative leaf rank, distinctness, and full-rank nonscalarity do
not transfer this commutator. Proper common-span compression is moreover
POVM-universal. The next proof must analyze the natural compressed effects
directly, not infer them from uncompressed leaf data.

## Generic Leaf-To-Canonical Transfer Is False

Files:

- `self_dual_wreath_leaf_whitening_commutator_no_go.py`
- `research/representation/self_dual_wreath_leaf_whitening_commutator_no_go.json`
- `tests/test_self_dual_wreath_leaf_whitening_commutator_no_go.py`

For a full-support projection frame `F=sum_e E_e` and canonical effects

`H_e=F^(-1/2) E_e F^(-1/2)`,

commuting `H_e` have an exact simultaneous-basis characterization. Projection
idempotence is `H_e F H_e=H_e`. Hence every positive diagonal effect entry is
`1/F_ii`, every `F_ii` is the positive integer counting effects incident on
coordinate `i`, and every effect support is an independent set in the graph
of nonzero off-diagonal entries of `F`. These conditions are also sufficient.
In particular, every nonzero eigenvalue of a commuting **full-support**
canonical effect is one of `1,1/2,...,1/q`.

The exact counterfamily partitions an `r=sp` dimensional fiber into `s`
parts of size `p`, uses all cyclic length-`b` intervals within each part, and
sets `H_e=(1/b)P_e`. Its leaves `E_e=F^(1/2)H_eF^(1/2)` are pairwise distinct
rank-`b` projections. Cross-part pairs, whose density tends to one, have

`||[E_e,E_f]||=(b/r)sqrt(1-(b/r)^2)`.

Nevertheless, the canonical effects are diagonal and commute exactly. The
frame condition number is `(2-1/s)/(1-1/s)<3`, total-rank aspect is `b`,
relative leaf rank is `b/r`, and

`D_ns=(1/b-1/r)I`.

Thus leaf commutators and full-support frame controls alone are compatible
with zero canonical commutator defect. This is not a natural wreath
counterexample. The reciprocal-integer corollary does not apply after the
proper common-span compression used by the final-root components; the next
section gives the exact no-go. Conditioning alone is no longer viable.

## Common-Span Compression Is POVM-Universal

Files:

- `self_dual_wreath_common_span_component_universality_no_go.py`
- `research/representation/self_dual_wreath_common_span_component_universality_no_go.json`
- `tests/test_self_dual_wreath_common_span_component_universality_no_go.py`

For the actual child formula

`A=X^*F^+X`,

`H_e=A^(-1/2)X^*F^+E_eF^+XA^(-1/2)`,

every finite-dimensional POVM is possible. Given `{H_e}`, its Naimark
isometry `V psi=direct_sum_e sqrt(H_e)psi` and coordinate projections `E_e`
give `F=I` and `V^*E_eV=H_e`. A sibling projection onto `Ran(V)` makes that
space the exact child-span intersection. Therefore neither reciprocal-integer
spectra nor any other generic POVM invariant follows from compression.

The stronger structured counterfamily combines cyclic rank-two commuting
effects with the duplicate-free leaf-whitening frame. It has common relative
rank `1/3`, total leaf-rank/common-rank aspect four, maximum leaf rank ratio
`4/k`, first-frame condition below four, density-one leaf commutators of
inverse-linear norm, component edge `1/3`, and

`D_ns=(5/9-1/k)I`.

Its compressed component effects nevertheless commute exactly and have
spectrum `{0,1/3,2/3}`. This simultaneously refutes the proposed
non-reciprocal-spectrum shortcut and every inference from the currently proved
coarse quantities. It does not prove natural wreath effects commute. The only
valid leading gate is now direct natural analysis of compressed `D_com` or an
explicit natural simultaneous-eigenbasis construction.

## Commutator Mass Is A Scalar Fourth-Moment Problem

Files:

- `self_dual_wreath_component_commutator_trace_mass_bridge.py`
- `research/representation/self_dual_wreath_component_commutator_trace_mass_bridge.json`
- `tests/test_self_dual_wreath_component_commutator_trace_mass_bridge.py`

For one child component POVM `{H_e}`, write `S_2=sum_e H_e^2`. The exact
identity

`Tr(D_com)=Tr(S_2^2)-sum_(e,f)Tr(H_eH_fH_eH_f)`

turns noncommutative support into a noncrossing-versus-crossing degree-four
moment gap. Every POVM obeys

`0<=Tr(D_com)<=r`, `0<=D_com<=2I`.

If `Q=supp(D_com)`, then `D_com<=2Q`; for every input state,
`Tr(rho Q)>=Tr(rho D_com)/2`. In the regular master, define

`M_4=E_Plancherel Tr(D_com,Lambda)/D_Lambda`.

Then both physical support mass and source-block noncommutativity probability
are at least `M_4/2`. Ordinary scalar trace is sufficient in this lower-bound
direction because the commutator defect has a universal operator upper bound.
No component edge, relative-rank theorem, or center-valued local law is needed.

The module does not prove natural `M_4>0`. Existing independent-Plancherel
sibling-frame degree-four moments concern uncompressed frames and cannot be
substituted for this calculation. The next theorem must evaluate the same two
moments after common-span pseudoinverse normalization, with physical carrier
normalization and globally distinct conditioning kept explicit.

## Exact Haar Scale For The Missing Moment

Files:

- `self_dual_wreath_component_commutator_haar_benchmark.py`
- `research/representation/self_dual_wreath_component_commutator_haar_benchmark.json`
- `tests/test_self_dual_wreath_component_commutator_haar_benchmark.py`

For a complex-Haar isometry `W:C^r -> C^N`, split into `q=N/b` coordinate
blocks and set `H_e=W^*P_eW`. A complete fourth-order unitary-Weingarten
contraction proves

`E Tr(D_com)/r`

`=(N-b)(N-2b)(N-r)(r^2-1)`

` / [N(N-2)(N-1)(N+1)(N+2)]`.

The factors `r^2-1` and `N-2b` correctly force zero for one-dimensional and
two-outcome POVMs. If `r/N->alpha` and `b/N->beta`, the limit is

`alpha^2(1-alpha)(1-beta)(1-2beta)`.

For sparse blocks `beta=1/q->0`, this remains
`alpha^2(1-alpha)`: a superpolynomial outcome count and vanishing block-rank
fraction do not suppress the Haar commutator signal. At the proved natural
aspect lower bound `19/520`, the blockwise benchmark is about `0.0012863`.
Combining it only as a scale estimate with source event `1/9` and common
physical rank `19/128` gives `M_4≈2.12e-5` and support `≈1.06e-5`.

This is not a natural theorem. The sibling-generated common span and
representation-theoretic dependencies may collapse the crossing gap. A
natural result must reproduce a positive scale or exhibit the exact
recoupling identity responsible for a zero/smaller gap.

## Natural Component-Commutator Gate Is Now A Pinned Growing-Word Problem

Newest files:

- `self_dual_wreath_component_commutator_collision_free_transfer.py`
- `self_dual_wreath_component_green_ridge_stability.py`
- `self_dual_wreath_component_hamming_orbit_reduction.py`
- `self_dual_wreath_natural_leaf_commutator_trace_profile.py`
- `self_dual_wreath_leaf_marked_green_word_normal_form.py`
- matching tests under `tests/`
- matching live artifacts under `research/representation/`

The collision-free conditioning issue is solved sharply for this observable.
For `Z=Tr(D_com,Lambda)/D_phys,Lambda in [0,1]` and conditioning event `C`
of mass `p`,

`E[Z|C] >= max(0,(E Z-(1-p))/p)` and
`|E[Z|C]-E Z| <= 1-p`.

Both inequalities are sharp. At the information-threshold schedule,
`1-p_cf=n^{-omega(1)}`, so any constant or inverse-polynomial independent
component `M4` survives global source distinctness. Finite rows through
`n=48` are deliberately reported as preasymptotic and vacuous for the
illustrative `1e-3` signal; do not reinterpret them as contrary evidence.

The Green/ridge transfer is also outcome-count free. For two `r`-dimensional
POVMs `{H_e},{J_e}`,

`|M4(H)-M4(J)| <= 4 sqrt(2 sum_e ||H_e-J_e||_F^2/r)`.

For the exact and ridge syntheses, the trace-weighted polar ratio

`R_eta=||U-U_eta||_F^2/[r(sigma_min(U)+sigma_min(U_eta))^2]`

gives `|M4-M4_eta|<=16 sqrt(2 R_eta)`. Thus an average ridge gap `zeta`
transfers if `E R_eta=o(zeta^2)`, without a leaf-count factor or uniform frame
edge. That natural average ratio and a positive natural ridge gap remain
unproved.

Source-pair flips and permutations reduce the annealed final-child pair sum
to `K-1` Hamming strata exactly:

`M4=(1/2) E_[W~Bin(K-1,1/2)] [q^2 c_W]`.

It is enough to lower-bound one typical-Hamming `q^2`-rescaled pair gap; the
exponential pair enumeration is no longer the bottleneck.

The natural uncompressed pair trace is now exact and quenched. For every
nonzero final-child orientation difference under independent Plancherel,

`E Tr([E_e,E_f]^*[E_e,E_f])/D_phys`

`=2(|S_n|-p(n))/|S_n|^3=Theta(q^-2)`.

Uniform relative multiplicity variance gives this scale on a density-one
fraction of balanced pairs with high probability, and collision-free
conditioning preserves the event. Hence one child has constant aggregate
**uncompressed** leaf commutator trace. This result does not imply component
`M4`; the generic whitening and common-span universality counterfamilies
remain valid.

The newest normal form removes the common span as an external random object.
For sibling frames `A,B`, support projections `P_A,P_B`, and common projection
`P`,

`P=s-lim_t (P_A P_B P_A)^t`,

`K=A^+ P (P A^+ P)^+ P A^+`.

Therefore the exact left-child Green kernel lies in `W*(A,B)`. Every
polynomial/ridge approximation to its pair moment is a linear combination of
words in frame tokens `A,B` and marked leaves `E,F`. Under independent
Plancherel, an exact word of length `p` at child Hamming distance `w` is

`g^-p sum_x I_split(x) [chi_nu(prod x)/d_nu]`

`    Q_0(x)^(K-1-w) Q_1(x)^w`,

where `Q_0,Q_1` are partially pinned two-color identity counts. If no `B`
token occurs, `I_split` forces `prod x=1`, so the target character cancels
exactly. The `EEFF-EFEF` specialization recovers the uncompressed trace above
for every target and tested distance.

This is the current highest-value theorem target:

1. Prove or refute a growing-degree rigidity/genus theorem for the signed
   `Q_0,Q_1` strata generated by polynomial approximants to `P` and `K`.
2. The theorem must cover degree growing with `n` (at least the degree needed
   for trace-weighted spectral approximation), typical
   `w=K/2+O(sqrt(K))`, and mixed `A/B` terms.
3. Bound arbitrary target characters in the mixed terms, or prove a
   cancellation that removes them. All-left target cancellation alone is not
   enough for the sibling common projection.
4. Show the signed AABB-minus-ABAB functional retains a constant or
   inverse-polynomial `q^2`-rescaled gap, or exhibit the exact natural
   recoupling identity that cancels it.

Primary-literature audit on 2026-08-09 found no theorem covering this regime.
Cassidy's new `arXiv:2608.02210` treats fixed surface relations and stable
characters. Hanany--Puder `arXiv:2009.00897` and Magee--Puder
`arXiv:1902.04873` are also fixed-word/stable-character inputs. Schneider--
Thom `arXiv:2206.11956` gives metric image results for words with constants,
not the required signed moment. These are useful structural tools, but none
allows the growing-degree gate to be marked resolved.

Latest focused checks before this handoff:

- collision-free transfer: 13 tests passed;
- Green/ridge stability: 6 tests passed;
- Hamming-orbit reduction: 5 tests passed;
- exact natural leaf trace profile: 9 tests passed after the exact-rational
  and cancellation-stable variance patch;
- leaf-marked Green word normal form: 7 tests passed;
- all five scripts generated live artifacts with zero focused-control
  failures.

No natural positive Green pair gap, component `M4`, component compiler,
decoder, MRS separation, or speedup is proved. The sole natural trace-mass
gate is now the growing marked-word theorem above.

## Marked Relation Pressure Is Closed Through Degree Two

Newest files:

- `self_dual_wreath_marked_relation_topology.py`
- `tests/test_self_dual_wreath_marked_relation_topology.py`
- `research/representation/self_dual_wreath_marked_relation_topology.json`

Experiment ID:
`EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY`.

The copy-depth part of the pinned-word expansion is now exact. For an
assignment alphabet `Omega={0,1}^u`,

`Q(x)^r = sum_(S subset Omega) onto(r,|S|) 1[all constraints in S hold]`.

Thus a fixed `u` needs support subsets, not ordered source-coordinate
assignment sequences. This removes all dependence on copy depth `K` at fixed
word degree, but leaves `2^(2^(u+1))` profile pairs as `u` grows.

Each support pair gives an exact finite-group presentation. Single-occurrence
Tietze elimination is solution preserving over every finite group. For the
uncompressed controls, `EEFF` reduces to a free rank-two group (`g^2`
solutions) and `EFEF` to one commutator (`g p(n)` solutions). S3 gives 36 and
18 exactly.

The leading typical-Hamming pressure certificate for a profile is

`d + 0.5 log2|S0| + 0.5 log2|S1| - p + 2`,

where `d` is an upper bound on the leading `log_|S_n|` solution exponent.
Dropping all but one residual relator gives a rigorous upper bound. The
certificate engine now recognizes:

- orientable quadratic surface words: loss one group exponent;
- nonorientable quadratic words: loss one half for crosscap one and one for
  higher crosscap;
- explicit commutators whose two factors extend to a verified free basis:
  loss one;
- primitive powers `x^k`: loss `1/k`, by the cycle-index count of
  permutations whose cycle lengths divide `k`;
- hidden surface or power words reached by a recorded chain of elementary
  Nielsen automorphisms.

Every one of the 4,500 support profiles with exactly two frame tokens now has
certified noncrossing pressure at most zero and crossing pressure at most
minus one. Full residual group topology remains unclassified for 116 of those
profiles, but that classification is not needed for the pressure upper bound.
The finite theorem is exact at the leading `log_|S_n|` exponent; partition,
Witten-zeta, and involution prefactors are `|S_n|^o(1)` and must not be silently
treated as uniform constants.

A deterministic degree-three probe found four entropy-heavy profiles that
defeated literal surface recognition. All four are now killed by exact
certificates:

- two become orientable genus-two relators after the Nielsen move
  `x4 -> x4 x6^-1`;
- one is an explicit free-basis commutator;
- one contains `x5^3`, whose one-third exponent loss moves pressure from
  `-0.7075...` to `-1.04085...`.

These four controls are **not** an exhaustive degree-three theorem. The next
high-reasoning task is to replace degree-by-degree enumeration with an
entropy-versus-relator theorem: for every support pair generated by a crossing
marked word, prove enough independent surface/torsion/word-map loss to offset
`0.5 log2(|S0||S1|)`, uniformly for growing `u`; or construct a profile family
whose presentation solution exponent violates that balance. After that,
mixed target-character observables still require a separate signed bound.

The counterexample-directed continuation is now implemented in:

- `self_dual_wreath_marked_pressure_obstruction_search.py`;
- `tests/test_self_dual_wreath_marked_pressure_obstruction_search.py`;
- `research/representation/self_dual_wreath_marked_pressure_obstruction_search.json`.

Experiment ID:
`EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH`.

Best-first support mutation ranks profiles by literal pressure proof debt,
then reserves Whitehead, Nielsen, and free-basis searches for finalists. The
live deterministic run now visits more than 7,500 profiles: all-`A` beams
through frame degree six plus mixed `A/B` beams at degrees three and four.
Every current scalar-pressure finalist receives an upper-bound certificate,
but this is not exhaustive coverage and the growing-degree theorem flag
remains false.

Two new exact certificate families emerged from the search.

First, a relator `y x^a y^-1 x^b` with `min(|a|,|b|)=1` says that a permutation
is conjugate to a fixed nonzero power of itself. Equality of cycle type forces
every cycle length to be coprime to the nonunit power. Every admissible
conjugacy class contributes exactly `|S_n|` pairs, so the pair count is
`|S_n| p_allowed(n)=|S_n|^(1+o(1))`; this removes one group exponent. This
killed the degree-three power-conjugacy survivors.

Second, a full Whitehead automorphism search reduces the hardest degree-four
relator from length seven to one basis generator in four moves. Every move
stores generator images and a verified two-sided inverse basis. A primitive
relator removes exactly one free variable over every finite group. This killed
the last degree-four survivor and its degree-five lifts.

Whitehead minimization now retains nonprimitive minima as well. It reduces a
balanced rank-six length-16 relator to an orientable genus-two word of length
eight in three verified moves. This closes the all-`A` degree-five scalar row
that the earlier bounded Nielsen search missed.

Most importantly, degree growth itself is now proved not to dilute hard
cores. Append a trailing frame token `z` whose assignment bit is zero on both
supports. The first marked `E` generator `x1` and `z` occur in exactly the same
split/color-zero relators, at the first and last positions, and neither occurs
in color-one relators. The basis change

`y1 = z x1`  (equivalently `x1 = z^-1 y1`)

turns every lifted relator into the old relator and leaves `z` free. Therefore
the lifted group is the old presentation free-product `<z>`, `d` and word
length both increase by one, and pressure is exactly invariant at every
degree. All 2,287 profiles through degree two plus the 14 live degree-four
finalists passed the exact relation-isomorphism/free-generator controls.

This changes the next proof target. Do not argue that large degree suppresses
fixed obstructions. Quotient constant-zero trailing coordinates first, then
classify **irreducible support cores**: coordinates that cannot be removed by
a free-product/Nielsen gauge. Prove an entropy-versus-word-measure bound for
those cores, or find an irreducible family with a matching asymptotic lower
bound above the crossing threshold. Constant-one and interior-coordinate
lifts are not covered by the theorem. Mixed target characters remain a
separate gate even after scalar pressure is controlled.

The search now enforces this quotient rule at degrees five and six. Every
reported finalist there has zero constant-zero lift depth. Degree six found
no positive literal pressure debt at all; its worst visited row is exactly at
the crossing threshold under the trivial assignment bound. This is finite
search evidence only, not a universal irreducible-core theorem.

The critical new frontier is mixed `A/B` words. Their split relations do not
alone force `prod(x)=1`, so the normalized target character cannot be dropped
from the Green-word normal form. Separate mixed beams currently have no
unresolved **scalar** pressure finalists. The runner transports the full
product through every Tietze replacement, reconstructs exact `S3` solutions,
and records sign and standard normalized-character averages.

Most visited mixed finalists cancel symbolically: the transported target is
freely trivial or is itself a residual relator. The retained adversarial
presentation from pattern `EFAEFBBB` is now resolved exactly. Its fourth
residual relator is

`r4 = (-8,-7,4,-8,-7,8,-5,-4,-8,-7,8,5)`.

Set `q=(-5,-8,7,8,4,5)`. The inverse relator factors as `r4^-1=q s`, and
the retained target is the cyclic shift `s q`. Therefore

`target = q^-1 r4^-1 q`.

This is a one-relator normal-closure certificate valid over every group. The
previous finite-residual interpretation was a false lead. The finite screens
remain useful exact regression fingerprints:

- 66 solutions in `S3`, all with identity target;
- 960 solutions in `S4`, all with identity target;
- 11,040 solutions in `S5`, all with identity target.

KBMAG independently reduced the target to identity using a valid but
nonconfluent completion; inspecting the words exposed the much shorter cyclic
certificate above. Do not retain a finite-residual conjecture for this row.

The old mixed beam was nevertheless searching the wrong boundary: it ranked
scalar pressure without preferring a surviving target, so it repeatedly chose
genus-zero or support-killed rows. This has been corrected by the exact
split-target theorem in
`self_dual_wreath_mixed_split_target_genus.py`. If the B positions form `r`
cyclic runs, imposing only the two split relations turns the full product into
an orientable quadratic boundary of genus `r-1`. For an irrep of dimension
`d_nu`, its exact split-only normalized character average is
`d_nu^(-2(r-1))`. The proof Nielsen-collapses each monochromatic run to one
block and applies the surface commutator formula. All 8,190 binary patterns
through length 12 and exact `S3` genus-one/two character controls pass. Extra
support relations condition the surface variables, so this is not yet the
needed relative theorem.

Mixed beams through frame degree six now require positive split genus and
prioritize support-uncancelled boundaries. They find genuine surviving target
words rather than cancellations. Every current finalist nevertheless has a
surface/free-basis certificate at least one full `|S_n|` exponent stronger
than the crossing threshold. This is finite counterexample-directed evidence,
not a growing-degree theorem.

The leading degree-three row has an exact stronger certificate in
`self_dual_wreath_relative_surface_factorization.py`. For pattern `EFBEBFB`,
write the residual generators as `a,b,c,d` and set

`A=a, H=bcda, C=c, K=da`.

The stored two-sided free-basis map sends the sole relation to
`A[K,C]A^-1` and the target to `H^-1 A H A^-1`; the relation and target use
disjoint generator pairs. Hence over every finite group `G` the exact solution
count is `|G|^3 k(G)` and the normalized target-character average is
`d_nu^-2`. For `S_n`, this is `|S_n|^(3+o(1))`, one exponent below the old
early-stopped bound. The exact `S3` controls are 648 solutions and standard
character average `1/4`.

The repeated surface certificates now have a uniform topological source in
`self_dual_wreath_two_partition_ribbon_surface.py`. Pair the split partition
with any one support assignment, invert the support color relators, and glue
equally labelled polygon edges. The components are closed orientable ribbon
surfaces. If component `j` has genus `g_j` and `f_j` ribbon faces, the original
one-vertex presentation is exactly

`(*_j pi_1(Sigma_{g_j})) * F_(sum_j(f_j-1))`.

Consequently its leading `S_n` solution exponent is

`sum_j(f_j-1) + sum_(g_j>0)(2g_j-1)`.

This replaces bounded Tietze/Nielsen discovery for every two-partition pair
with a direct face-permutation calculation. All 87,380 binary partition pairs
through length eight have valid orientable topology, and all 340 pairs through
length four match exact `S3` solution counts. The exponent is now used in
pressure beam scoring. It is only a one-support-cell upper bound: dropping all
other support relations can leave large support entropy unpaid.

The support-entropy side now has an exact abelian theorem in
`self_dual_wreath_support_affine_rank_entropy.py`. For nonempty cube supports
`S,D subset {0,1}^u`, the rational exponent-sum relation rank satisfies

`R >= 2 + 0.5 log2|S| + 0.5 log2|D|`.

A real affine `d`-plane contains at most `2^d` cube vertices; support
differences supply the larger affine-direction space, while the differing-leaf
offset and all-ones row supply two independent directions. Exhaustive `u=1,2`
controls cover 918 support profiles with zero failures. Thus abelian rank pays
all support entropy except at most one crossing exponent. **Do not convert this
to an `S_n` homomorphism-count theorem.** Nonprimitive and power relators show
that rational rank need not cost one permutation exponent per row. The missing
rank-to-nonabelian lift and final crossing surface loss remain the decisive
obligations.

The degree-three primitive-cube adversarial row has also been sharpened, after
falsifying an incorrect coprime-collapse interpretation. Its exact residual
relations are equivalent to

`<x,y,z | x^3, [x,z], [y,z]> = (C_3 * Z) x Z`.

Nonidentity 3-cycles survive; the exact `S3` solution count is 42, not 36. For
every finite group `G`, the solution count is `|G|` times the sum over
conjugacy classes `[z]` of the number of cube roots of identity in `C_G(z)`.
For `S_n`, comparison with the identity centralizer and the subexponential
partition count gives leading exponent `2-1/3=5/3`. The certificate uses an
exact alternating normal form in `(C_3 x Z) * F`, and the focused topology and
pressure suites pass. Never restore the discarded claim that these relations
force `x=1`; its derivation misread the sign of the fourth relator.

A separate coprime statement is valid and now has a deliberately narrow
certificate: literal pure-power relators `x^a=1` with degree gcd one force
`x=1` by Bezout. The topology classifier applies this only when every selected
relator is a one-generator pure power, for example `x^2=x^3=1`. It must never
be generalized back to equal-context or sign-sensitive relations.

A first genuine growing-degree subclass is now closed in
`self_dual_wreath_linear_code_support_pressure.py`. For the contiguous
crossing family

`E A^u F E F`

with same and different supports binary linear codes `S,D <= F_2^u`, let
`s=dim S`, `d=dim D`, and `r=max(s,d)`. The all-A split plus the zero cell of
`D` is exactly `F_u * Z^2`: eliminate the last E/F leaves and use the free
basis change `A=a(x_1...x_u)`. An RREF basis of the larger code is contained
in that support and supplies `r` actual relators, each with one unique pivot
frame generator. Selecting those relators gives

`F_(u-r) * Z^2`.

Hence the full presentation has at most `|G|^(u-r+1) k(G)` solutions over
every finite group. For `S_n`, the support-weighted crossing pressure is at
most

`-1 - |s-d|/2`.

This is symbolic and uniform in `u`, not a finite-beam extrapolation. All
4,774 linear-code pairs through width four and two exact `S3` full-presentation
controls pass. The theorem does **not** cover affine cosets, arbitrary
supports, interleaved leaves, B frames, or mixed target characters. Affine
cosets through width three showed no finite pressure violation, but they do
not contain the RREF combinations used by this proof; no affine claim is
allowed without a new relative-partition basis theorem.

The all-A zero-based problem has since been solved in
`self_dual_wreath_frame_subword_entropy.py`. For arbitrary supports in the
same contiguous family, assume `0 in D`, put `U=S union D`, and define

`P(U)=<x_1,...,x_u | product_(i:v_i=1) x_i=1, v in U>`.

The split and zero different cell make the selected full presentation exactly
`P(U) * Z^2`. If `e(U)` is a certified leading `S_n` solution exponent for
`P(U)`, the crossing pressure is at most

`e(U) + H(S,D) - u - 1`,  `H=(log2|S|+log2|D|)/2`.

Because `H<=log2|U|`, the single-support inequality

`e(U)+log2|U| <= u`

closes every pair with union `U`. This inequality is now an exact all-width
theorem. For `a in U`, the triangular automorphism

`x_i -> A_i x_i^((-1)^a_i) A_i^-1`,
`A_i=product_(j<i) x_j^a_j`,

sends `w_b` to `w_(a xor b) w_a^-1`, so `P(U)` is invariant under re-rooting
at `a`. Re-root at an element of the larger last-coordinate half. If the one
half is empty the last generator is free; otherwise a one-half relation
determines it and leaves a quotient of the zero-half presentation. Induction
proves for every finite group `G`

`#Hom(P(U),G) <= |G|^(u-log2|U|)`.

All 32,906 width-at-most-four supports, 16,948 width-five stress supports,
every re-rooting base through width eight, 20,000 random induction controls
through width ten, and exact `S3` counts through width three agree. These are
code controls; the displayed automorphism and induction are the proof.
Nonabelian Littlewood-Offord bounds do not supply this result: Tiep--Vu treats
`{A_i,A_i^-1}` products and polynomial concentration regimes, whereas these
lazy `{1,g_i}` fibers can be exponentially small.

The frame-subword result is now strictly stronger. For uniform `X in U`, let
a coordinate branch when both bit values occur conditional on the strict
suffix of `X`. The entropy chain rule gives

`log2|U| <= E[number of branching coordinates]`.

Hence some anchor has at most `floor(u-log2|U|)` suffix-forced coordinates.
After XOR re-rooting at that anchor, every branching-coordinate witness is a
triangular relator that eliminates its generator. Therefore, for every
nonempty support (zero is no longer required for this strengthening),

`#Hom(P(U),G) <= |G|^floor(u-log2|U|)`.

`frame_subword_suffix_branch_certificate` stores the anchor, every witness,
the entropy-chain audit, and the integer generator bound. This supersedes the
real entropy exponent whenever `|U|` is not a power of two.

`self_dual_wreath_contiguous_all_a_support_pressure.py` removes the zero-base
and linear-support restrictions entirely. Same-coordinate color-one cells
form `P(S union {0})`; choosing `q in D`, different-coordinate color-one cells
form the re-rooted presentation `P(D xor q)`. The stronger fiber pays

`max(log2|S union {0}|, log2|D|) >= H(S,D)`.

The integer theorem further improves the frame exponent to
`u-ceil(log2 max(|S union {0}|,|D|))`.

For fixed frame values, the split and base-cell equations reduce the four
outer variables to `A(bT)A^-1=w_q b`. Summing possible conjugators gives at
most `sum_g |C_G(g)|=|G|k(G)` outer assignments. Hence every nonempty
arbitrary support pair for `E A^u F E F` has scalar `S_n` crossing pressure at
most `-1`, uniformly in `u`. Structural controls cover all 65,259 support
pairs through width three and exact full `S3` controls pass. This is an
unsigned obstruction, not a component signal.

`self_dual_wreath_contiguous_frame_target_factorization.py` extends the same
scalar theorem to every contiguous A/B frame pattern `E T_1...T_u F E F`.
Put `w_A` for the A-frame subword, `X=x_1...x_u`, and `R=w_A^-1 X`. Exact
elimination gives the same outer conjugacy equation and reduces the full
target on every solution to `A R A^-1`. Thus its normalized character is
exactly `chi(R)/d`; the unresolved measure on frames carries the explicit
weight

`sum_b 1[bT conjugate w_q b] |C_G(bT)|`.

All 87,380 frame-type/base pairs through width eight pass the symbolic outer
and target factorizations. Restoring both colors of every support cell yields
a sharp fixed-width tradeoff. Under the integer strengthening, scalar pressure
saturates exactly when `0 in S` and `|S|=|D|` is a power of two; the zero same
cell contributes `R` itself as a relator, so every saturating profile forces
target identity.

The old real entropy certificate did **not** have a uniform gap. An
exact `S3` seed with frame types `BABA`, nonidentity target, `|S|=1`, and
`|D|=2` has an identity-A-frame lift of every depth `k`. Its supports have
sizes `2^k` and `2^k+1`, every full marked relation remains satisfied, the
target stays nonidentity, and the old real entropy margin is exactly
`0.5 log2(1+2^-k) -> 0`.

This no longer falsifies the strongest certificate. Because `2^k+1` crosses a
power-of-two boundary, the integer suffix-branch margin tends to `1`, and the
lift is uniformly subleading already at the scalar level. A genuine global
uniform-gap counterexample would need a target-surviving profile near the
opposite side of a power-of-two boundary. That question remains open.

That opposite-side generic counterexample now exists but also collapses.
Delete one same row and one different row, giving support sizes `2^k-1` and
`2^k`. The integer suffix-branch certificate margin becomes
`0.5 log2(2^k/(2^k-1)) -> 0`, and the same nonidentity `S3` assignment remains
a solution. Exact Tietze reduction at every depth gives five generators and
one genus-two relator. A Nielsen change identifies the group as the genus-two
surface group free-product one free generator; the target modulo the relator
is one handle commutator. Exact `S3` count is `2916`, sign average `1`, and
standard normalized average `1/2`. The true `S_n` solution exponent is `4`,
so its scalar pressure margin is
`1+0.5 log2(2^k/(2^k-1))>1`. This falsifies the strongest *generic
certificate* gap, not the actual-presentation gap.

Independently, that exact lift is classified in
`self_dual_wreath_target_survival_surface_seed.py`. Paired same-support rows
force every appended A-frame generator to identity, so every lift is
Tietze-equivalent to the width-four seed. The seed is a four-generator,
genus-two surface presentation with `S_n` solution exponent `3`; the target is
one handle commutator. Exact `S3` fingerprints are 486 solutions, sign average
`1`, and normalized standard average `1/2` at every stored lift depth.

For `Z_n=sum_(lambda|-n)d_lambda^-2` and
`C_alpha=sum_(lambda covers alpha)d_lambda^-1`, standard Ind--Res gives the
exact normalized handle average

`(sum_(alpha|-n-1) C_alpha^2 - Z_n) / ((n-1) Z_n)`.

The Witten-zeta bounds `zeta_Sn(1)=2+O(n^-1)` and
`zeta_Sn(2)=2+O(n^-2)`, plus the `O(sqrt n)` removable-corner bound, give

`2/(n-1)^2 + O(n^-5/2)`.

More generally, write the commutator density as `1+sgn+h`. Orthogonality gives
`E|h|^2=zeta_Sn(2)-2=O(n^-2)`, so the genus-two handle law is `O(1/n)` in total
variation from uniform measure on `A_n`. Every normalized irreducible target
except trivial/sign therefore vanishes uniformly; trivial and sign equal one.
The degree-30 exact partition sum gives `n^2`-scaled standard average
`2.1860`, approaching the proved constant `2`.

The next high-value theorem is either a global target-survival gap across the
remaining power-of-two boundary profiles or a centralizer-weighted `S_n` frame-character
upper/lower bound for target-surviving presentations **not** equivalent to
this identity-frame genus-two seed, coupled to the growing-degree partially
pinned `Q_0,Q_1` regime. A valid positive result needs matching leading
homomorphism mass and nonvanishing normalized character. Interleaved leaves
remain a separate multi-boundary problem.

Latest focused validation: the linear-code and topology suites pass 25 tests
in 28.54 seconds; the topology and pressure-obstruction suites pass
25 tests in 91.62 seconds after the centralized-torsion correction; the
split-target genus and relative-surface suites each passed 4 tests, in 0.86
and 0.55 seconds respectively; the ribbon-surface suite passed 4 tests in 3.11
seconds, and the affine-rank suite passed 5 tests in 0.16 seconds. Their live
artifacts have zero
split-genus, finite-character, relative-factorization, ribbon-topology,
residual-target, lift, or adversarial-pressure control failures. No exhaustive
degree-three theorem,
growing-degree pressure theorem, universal mixed-character cancellation,
asymptotic counterexample, positive Green pair gap, component `M4`, or speedup
is claimed.

## Superseded Pre-2026-08-08 Priority List

This list is retained only as provenance. The vertex PSD criterion, simplex
holonomy counterfamily, flat carrier groupoid, graded crossing no-go, and
internal-closure quarter-gap theorem above supersede its ordering. Follow
`Revised Highest-Value Derivations`, not this section.

The PGM still has constant information-theoretic success and physical
transfer. The pair-core overlap operator is now exact, and the sign-blind
route to all-depth conditioning is dead. Work in this revised order:

1. Construct or refute the **vertex trivialization of the residual transport**
   at natural depth. This is now the single decisive statement. The
   single-correlation half of the hypothesis is measured and holds at `n=12`;
   what is missing is the isometry factorization
   `B_e^* B_f = gamma W_(e,v)^* W_(f,v)` for adjacent live cores. Build the
   `W_(e,v)` from the carrier factorization's explicit index bijection, or
   exhibit a natural adjacent pair whose normalized overlap is not a
   restriction of a common vertex isometry.
   Note holonomy does **not** need to vanish: `C~^*C~ >= 0` for any
   connection, so the floor `2-2gamma` survives arbitrary holonomy. Only the
   factorization itself is at stake.
   Falsifier: a natural full live graph with `lambda_min+(M) < 2 - 2gamma_max`.
2. Bound the **graded defect**, not just the metric. The metric floor says
   nothing about `||M^(-1/2) J M^(-1/2)||`, which is what endpoint gaps for
   the relative polar actually require. Redo the star and commuting-atom
   calculations with the `J` grading in place and determine whether the
   defect is also width independent.
3. Prove or falsify the **uniform residual pair-quotient gap**: an all-n bound
   below one on `||P_(A minus K)P_(B minus K)||`. This is a *geometric*
   statement about child spans, and unlike the relation Gram it **does** see
   vertex-disjoint core overlaps, which are nonzero at natural depth. Absolute
   weights are proved inadequate; the Laplacian floor does not transfer here
   automatically.
4. Derive the **exact vertex-disjoint pair-core overlap**. The shared-vertex
   case is a scalar; the disjoint case is a grid contraction with genuine
   Kronecker content, currently controlled only by the waist upper bound. That
   bound is exactly tight on all forty screened controls, so either prove
   equality or exhibit a strictly smaller grid. This feeds item 3, not the
   relation Gram.
5. Extend the finite **phase-sensitive relative Cech/Laplacian prototype** to
   all depth. Prove exactness or classify `H_p`, `p>=1`, for the noncommuting
   multiplicity sheaf. Use the `C^*C`/`CC^*` duality so that homology is
   computed on the vertex side, and reuse the commuting-atom splitting: under
   commutativity the whole complex is a direct sum of scalar complete-graph
   complexes on affine supports.
6. Determine the **physical PGM mass** of the noncommuting blocks. A finite
   S6 defect does not establish asymptotic relevance. Compute frame-weighted,
   not raw multiplicity-weighted, mass on natural threshold portfolios. The
   carrier factorization now supplies exact per-sector weights for this.
7. Compile or kill a coherent **Racah/common-core transform**. The scalar
   shared-vertex result removes one imagined obstruction: there is no
   nontrivial 6j block to compile at the star level. The compilation target is
   therefore the Cech quotient and the disjoint-pair grid blocks, in
   polynomial gates, with multiplicity spaces kept in quantum registers.
8. Extend the weighted common-free exclusion to the residual after exact
   affine common supports and noncommuting pair cores are removed. Note the
   same asymptotic caution as item 3: any successor must not be sign blind.
9. Write the hierarchical polar tree in the **Moore--Russell--Sniady** formal
   algorithm model and either prove simulation (killing the route) or isolate
   the coherent operation that escapes it. See the scope analysis above; the
   degree obstruction is evidence, not a separation.
10. Compute the **Ozols--Roetteler--Roland** water-filling cost for the
    explicit source/target amplitude pair named in the scope analysis above.
11. Only after 1--7, compose
    `physical row-copy -> Q_R^* -> inverse S_n QFT` and audit total gates,
    copies, memory, and approximation error.
12. Maintain the falsification route: a residual quotient gap closing on
    positive natural mass, a superpolynomial Racah transform, or an
    extended-sieve simulation is a reason to abandon this PGM architecture.

Do not resume claims of universal exact half-balance. Do not use pair
generation, affine support balance, XOR covariance, or finite reciprocal
spectra as substitutes for the missing Laplacian-gap and conditioning
theorems. In particular, do not reintroduce any absolute-weight or block
Gershgorin certificate as an all-depth argument: it is now proved vacuous at
natural depth. Additional finite work is justified only when it attacks one of
those statements with a declared counterfamily.

Two corrections that must not be re-broken. The metric floor is about the
**full live graph**: a star-subgraph evaluation is not evidence about a merge.
And the relation Gram has **no vertex-disjoint off-diagonal blocks**; disjoint
core overlaps matter for the child-span geometry in item 3, not for `M`.

## Mechanical Follow-Up For Antigravity / Gemini 3.6 Flash

These tasks are useful but should not consume the scarce high-reasoning pass:

0. Wire
   `EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN` with suggested
   CLI name `code-wreath-final-root-natural-common-span`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS` with suggested CLI
   `code-wreath-component-defect-rank-mass`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM` with suggested CLI
   `code-wreath-component-povm-spectral-trim`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY` with suggested
   CLI `code-wreath-component-effect-algebra-boundary`,
   `EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS` with suggested CLI
   `code-wreath-natural-leaf-commutator`, and
   `EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO` with suggested
   CLI `code-wreath-leaf-whitening-no-go`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO` with
   suggested CLI `code-wreath-common-span-component-universality`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE` with
   suggested CLI `code-wreath-component-commutator-trace-mass`, and
   `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK` with
   suggested CLI `code-wreath-component-commutator-haar`. Copy the existing
   theorem-module registry/runner/CLI pattern; do not alter the mathematics.
   Preserve these gates exactly: positive natural common-span mass and final
   block/fiber aspects are true; natural positive component edge, coherent
   pseudoinverse access, component-support SELECT, recursive polar, and speedup
   are false. The defect-rank module proves center-valued support mass and
   asymptotically full relative rank, not a nonzero spectral gap. The spectral-
   trim module proves a conditional state-weighted hard-edge bypass, not
   natural input flatness or a coherent filter. The effect-algebra boundary
   keeps natural commutator support mass false; full-rank nonscalarity is not
   noncommutativity. The leaf theorem proves density-one inverse-polynomial
   commutators only before whitening. The whitening no-go proves that bounded
   conditioning, distinct high-rank leaves, constant aspect, and full-rank
   nonscalarity still do not transfer them; its reciprocal-integer criterion
   is full-support only. The common-span universality module proves arbitrary
   POVMs, including commuting non-reciprocal spectra, arise after proper
   compression and gives a stronger all-coarse-data counterfamily. It does not
   prove natural wreath commutativity. Keep direct natural compressed
   commutator mass, simultaneous-basis/compiler, MRS, decoder, and speedup
   claims false. The trace-mass bridge makes a scalar natural `M_4` lower
   bound sufficient for support, but proves no such lower bound; do not report
   uncompressed sibling moments as that missing result. The exact Haar formula
   is also surrogate-only and must never be presented as natural transfer.
   Add clean dispatch
   tests, regenerate downstream registry
   workflows, and include the artifact in the progress summary without calling
   the finite `S_48` rows evidence for the asymptotic edge.
1. Re-run and record the standard downstream workflows after any new module:
   `dequantize`, `proofs`, `query-models`, `frontiers`, `conjectures`,
   `mutate`, and `validate`.
2. Add routine CLI/experiment-runner/registry plumbing by copying the pattern
   used for `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT`.
   The common-range experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE`, and its intended CLI
   name is `code-wreath-orientation-common-ranges`.
   The fixed-family experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE`, and its intended CLI
   name is `code-wreath-orientation-family-ranges`.
   The pair-angle experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES`, and its intended CLI
   name is `code-wreath-orientation-pair-angles`.
   The finite block-core experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE`, and its intended
   CLI name is `code-wreath-orientation-block-core`.
   The asymptotic obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION`, and its intended
   CLI name is `code-wreath-plancherel-block-obstruction`.
   The trimmed measurement experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM`, with intended CLI
   `code-wreath-spectral-trim`.
   The generic degree obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION`, with
   intended CLI `code-wreath-spectral-filter-degree`.
   The Plancherel mass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS`, with intended CLI
   `code-wreath-plancherel-block-mass`.
   The algebraic quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT`.
   The branchwise commutant experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION`.
   The physical branch-filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER`.
   The paired-filter bypass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS`.
   The all-local-filter no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO`.
   The cluster-locality lower-bound experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO`.
   The black-box spectral query lower-bound experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND`.
   The orientation-character filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER`.
   The invariant-projector circuit experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT`.
   The physical-access audit experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS`.
   The direct physical filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE`.
   The natural retention theorem experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM`.
   The exact postfilter-compression experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION`.
   The logarithmic rank-retention experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET`.
   The isotypic-dephasing no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO`.
   The coherent Fourier decoder experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER`.
   The quantum-sampling normal-form experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION`.
   The pair-polar experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER`.
   The hierarchical-chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE`.
   The relative-intersection experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION`.
   The common-core bypass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS`.
   The early-overlap experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION`.
   The generic equal-Gram transfer-gate experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER`.
   The resolved physical transfer experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER`.
   The exhaustive three-bit flag experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT`.
   The canonical cross-dependency experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY`.
   The scalar Cayley reduction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION`.
   The matrix Cayley failure-boundary experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY`.
   The sparse invariant dependency experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY`.
   The common-free weighted exclusion experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION`.
   The pair/emergent quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY`.
   The affine-support/noncommuting-core experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION`, with suggested CLI
   `code-wreath-common-core-atomization`.
   The local recoupling-conditioning experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY`, with suggested
   CLI `code-wreath-pair-core-recoupling`.
   The phase-sensitive common-core chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN`, with suggested CLI
   `code-wreath-common-core-cech`.
   The augmented leaf-dependency chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH`, with suggested CLI
   `code-wreath-augmented-common-core-cech`.
   The recursive H0 experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION`, with suggested CLI
   `code-wreath-recursive-pair-generation`.
   The exact residual quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP`, with suggested CLI
   `code-wreath-pair-quotient-overlap`.
   The pair-core carrier factorization experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION`, with suggested
   CLI `code-wreath-pair-core-carrier-factorization`.
   The multistar degree obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION`, with suggested
   CLI `code-wreath-multistar-degree`.
   The orientation Laplacian gap experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP`, with suggested CLI
   `code-wreath-orientation-laplacian-gap`. This one is not wired yet.
   The exact global collision-free mass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS`.
   The injective conditioned source-kernel experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL`.
   The exact vertex PSD criterion experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION`.
   The flat carrier-groupoid experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID`.
   The graded crossing-only no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO`.
   The complete internal-closure rescue experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE`.
   The exact relation-cokernel transfer experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER`.
   The augmented-H0 dimension obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION`.
   The hierarchical cokernel resolution experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION`.
   The exact independent-Plancherel sibling moment experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS`.
   The Gaussian Jacobi benchmark experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE`.
   The exact degree-four joint-freeness experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS`.
   The Gaussian top-split conditioning experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE`.
   The exact arbitrary-word normal-form experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM`.
   The event-level conditioning bypass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER`.
   The exact mixed-arity polar schedule experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE`.
   The interval-uniform trace-polynomial burden experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN`.
   The regular master/central-support experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT`.
   The relative-rank bridge/symmetry-boundary experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE`.
   The exact subgroup-projection walk experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK`.
   The affine-node exact common-outlier experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER`.
   The full-regular pairwise-angle no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO`.
   The physical trace-weighted PGM bridge experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE`.
   The generic native-frame access-boundary experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY`.
   The conditional native pair-mass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY`.
   The direct generalized-phase-estimation pair-polar experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT`.
   The executable holonomy fixed-space reduction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION`.
3. Add Sellke's paper to `research/literature_index.json` and
   `research/literature_records.json`, preserving the precise mechanism,
   theorem, reuse, and no-overclaim fields.
4. Add clean-registry dispatch tests and update README command examples.
   The step-by-step version of items 1-6 with exact commands, acceptance
   checks, and forbidden actions is in
   `research/MECHANICAL_FOLLOW_UP_PLAN.md`. Work from that file, not from
   this summary.
5. Run focused tests first, then `python -m compileall -q .`,
   `node --check site/progress.js`, `git diff --check`, and
   `python qsearch.py validate`.
6. Do not run the multi-hour full suite after every narrow change. The last
   complete repository suite before these two modules was 1,494 tests passed;
   use affected tests unless a shared contract changes.
7. Do not commit or push each subsystem. Make one intentional checkpoint only
   after several coherent research passes or when the user requests it.

## Periodic Frame Rank Collapse (2026-08-09)

`self_dual_wreath_periodic_frame_fiber_counterfamily.py` constructs an exact
nonidentity `S3` frame family with exponentially vanishing old real-entropy margin.
That family is now **falsified as an asymptotic channel**, not left open.

`self_dual_wreath_periodic_frame_rank_collapse.py` proves the missing all-period
statement. Let

```text
P = 001110100010111010000011101000
Q = 10011
```

for the repeated `BAABB` frame values. Both selected/complement products of
`P` and of the all-zero six-period block are identity; `Q` reaches the same
fiber state. The exact suffix-branch lemma says that a support row agreeing
with an anchor after coordinate `i` and flipping bit `i` gives, after XOR
re-rooting, a relator that determines `x_i` from lower generators. The finite
witness catalog proves:

- first `P`: every coordinate branches except `1,2,5`;
- every later `P`: all coordinates branch using a `PP` witness;
- terminal `Q`: all coordinates branch using a `PQ` witness;
- the single `Q` case separately leaves at most three generators.

Therefore every `k=6m+1` same-fiber frame presentation has at most three
generators over every finite group. The exact fiber size is

```text
S_m = (16*2^(30m) + 8*2^(24m) - 4*2^(6m) - 2)/9,
D_m = S_m + 1.
```

The existing mixed-frame outer conjugacy theorem contributes at most
`|G| k(G)`, so the full presentation has at most `|G|^4 k(G)` solutions. For
`S_n`, the scalar pressure margin is uniformly at least
`1-0.5*log2(3/2) = 0.707518...`. A target character cannot rescue this missing
unsigned mass. Keep every speedup/positive-M4 gate false.

The four materialized controls now have remaining generator counts `4,5,4,3`
and exact `S3` counts `324,396,342,126`; they are regressions, not the proof.
The all-period proof is the suffix-witness/neutral-concatenation certificate.

**Next high-reasoning task:** determine whether every dense constant-state
ordered-subword automaton fiber admits an `O(1)` suffix-branch generator bound.
A positive theorem would eliminate a broad class of finite-group frame-fiber
escapes and redirect search toward growing-state algebra or interleaved leaves.
A useful counterexample must have growing suffix-branch dimension and survive
the outer conjugacy pressure accounting. Do not spend Codex reasoning on CLI,
registry, or README plumbing for these modules; that is explicitly assigned to
Gemini 3.6 Flash through Antigravity in
`research/MECHANICAL_FOLLOW_UP_PLAN.md`.

## Resume Commands

```bash
python qsearch.py code-wreath-orientation-fourier
python qsearch.py code-wreath-orientation-moments
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT
python self_dual_wreath_physical_pgm_intertwiner.py
python self_dual_wreath_level_three_flag_audit.py
python self_dual_wreath_common_core_atomization.py
python self_dual_wreath_dependency_homology.py
python self_dual_wreath_pair_core_recoupling_boundary.py
python self_dual_wreath_common_core_cech_laplacian.py
python self_dual_wreath_augmented_common_core_cech.py
python self_dual_wreath_recursive_pair_generation.py
python self_dual_wreath_pair_quotient_overlap.py
python self_dual_wreath_pair_core_carrier_factorization.py
python self_dual_wreath_multistar_degree_obstruction.py
python self_dual_wreath_orientation_laplacian_gap.py
python self_dual_wreath_global_collision_free_mass.py
python self_dual_wreath_global_distinct_joint_kernel.py
python self_dual_wreath_vertex_trivialization_criterion.py
python self_dual_wreath_vertex_channel_groupoid.py
python self_dual_wreath_graded_flat_transport_no_go.py
python self_dual_wreath_internal_closure_graded_rescue.py
python self_dual_wreath_sibling_frame_joint_freeness.py
python self_dual_wreath_sibling_frame_joint_conditioning_surrogate.py
python self_dual_wreath_sibling_word_map_normal_form.py
python self_dual_wreath_collision_free_event_transfer.py
python self_dual_wreath_multiscale_polar_schedule.py
python self_dual_wreath_trace_polynomial_edge_burden.py
python self_dual_wreath_regular_master_central_support.py
python self_dual_wreath_central_support_rank_bridge.py
python self_dual_wreath_subgroup_projection_walk.py
python self_dual_wreath_affine_node_common_outlier.py
python self_dual_wreath_subgroup_pair_angle_no_go.py
python self_dual_wreath_local_pair_transversality.py
python self_dual_wreath_pair_common_covering_transition.py
python self_dual_wreath_fixed_family_common_rank_dilution.py
python self_dual_wreath_plancherel_kronecker_positivity.py
python self_dual_wreath_extended_kronecker_threshold.py
python self_dual_wreath_hamming_stratum_rank_transition.py
python self_dual_wreath_natural_pair_carrier_law.py
python self_dual_wreath_two_color_return_walk.py
python self_dual_wreath_hierarchy_pair_common_rank_budget.py
python self_dual_wreath_hierarchy_low_carrier_trim.py
python self_dual_wreath_complete_s6_vertex_channel_audit.py
python self_dual_wreath_affine_plane_scalar_holonomy.py
python self_dual_wreath_affine_plane_support_pressure_no_go.py
python self_dual_wreath_trace_weighted_pgm_bridge.py
python self_dual_wreath_native_frame_access_boundary.py
python self_dual_wreath_pair_transport_native_mass_boundary.py
python self_dual_wreath_gpe_pair_polar_transport.py
python self_dual_wreath_gpe_holonomy_resolver_reduction.py
python self_dual_wreath_final_root_natural_common_span.py
python self_dual_wreath_component_defect_rank_mass.py
python self_dual_wreath_component_povm_spectral_trim.py
python self_dual_wreath_component_effect_algebra_boundary.py
python self_dual_wreath_natural_leaf_commutator_mass.py
python self_dual_wreath_leaf_whitening_commutator_no_go.py
python self_dual_wreath_common_span_component_universality_no_go.py
python self_dual_wreath_component_commutator_trace_mass_bridge.py
python self_dual_wreath_component_commutator_haar_benchmark.py
python qsearch.py code-wreath-subpovm-moments
python qsearch.py validate
```

Before claiming progress, inspect the current artifact and verify that every
claimed theorem has a proof gate and every finite experiment has an explicit
falsifier. Keep `speedup_claim_allowed` false until the asymptotic norm,
coherent measurement, decoder, end-to-end complexity, and classical-baseline
obligations are all resolved.
