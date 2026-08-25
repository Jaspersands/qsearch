# Research Agent Handoff

Last updated: 2026-08-24

## Antigravity Mechanical Wiring Completion Note (2026-08-24 - Pass 6)

- **Mechanical Wiring Status**: **100% COMPLETE**. All **22 newly generated theorem modules** in `self_dual_wreath_*` families (including branch-character cyclic polar compilers, quadrant overlaps, equivariant multiplier normal forms, GPE dilation separations, label-coherent power-map boundaries, Naimark Fourier bridges, and Schur dilated multiplicity access boundaries) have been fully wired into:
  - `core/research_registry.py` (all 22 `ExperimentRecord` blocks registered under `CODE-COSET-COLLECTIVE` in `seed_candidate_records()`)
  - `core/experiment_runner.py` (imports, runner dispatchers, priority maps, supported experiment sets, and safe result upsert fallbacks)
  - `qsearch.py` (CLI subparser commands and execution handlers)
  - `README.md` & `repomap.html` & `docs/REPOSITORY_MAP.md` (CLI command documentation & 745 module updates)
  - `tests/test_experiment_runner.py` (full clean-registry unit test dispatch coverage for all 22 experiments)
- **Repository Milestones**: The research registry now tracks **746 registered experiments**, **729 experiment results**, **1,212 dequantization findings** (1,208 blocking), and **809 negative result records**.
- **Validation**: Full workspace validation (`python3 qsearch.py dequantize && python3 qsearch.py validate`), `python3 tools/build_progress_snapshot.py`, `python3 -m compileall -q .`, `node --check site/progress.js`, and `git diff --check` all passed cleanly with **0 issues (`valid: true`)** and **22 newly added dispatch tests passed (100% OK)**.
- **Claim Gates & Integrity**: All mathematical contracts, constants, formulas, falsifiers, negative result claims, and `speedup_claim_allowed=False` gates remain 100% intact.

## Antigravity Mechanical Wiring Completion Note (2026-08-21 - Pass 5)

- **Mechanical Wiring Status**: **100% COMPLETE**. All **64 newly generated theorem modules** in `coset_hidden_involution_*` and `self_dual_wreath_*` families (including adaptive Walsh routing, regular-master Walsh flatness no-go, MRS identification escape theorem, and shared-conjugation QSVT lower bounds) have been fully wired into:
  - `research_registry.py` (all 64 `ExperimentRecord` blocks registered under `CODE-COSET-COLLECTIVE` in `seed_candidate_records()`)
  - `experiment_runner.py` (imports, runner dispatchers, priority maps, supported experiment sets, and safe result upsert fallbacks)
  - `qsearch.py` (CLI subparser commands and execution handlers)
  - `README.md` (CLI command documentation)
  - `tests/test_experiment_runner.py` (full clean-registry unit test dispatch coverage for all 64 experiments)
- **Repository Milestones**: The research registry now tracks **723 registered experiments**, **727 experiment results**, **1210 dequantization findings** (1206 blocking), and **806 negative result records**.
- **Validation**: Full workspace validation (`python3 qsearch.py dequantize && python3 qsearch.py validate`), `python3 tools/build_progress_snapshot.py`, `python3 -m compileall -q .`, `node --check site/progress.js`, and `git diff --check` all passed cleanly with **0 issues (`valid: true`)** and **64 newly added dispatch tests passed (100% OK)**.
- **Claim Gates & Integrity**: All mathematical contracts, constants, formulas, falsifiers, negative result claims, and `speedup_claim_allowed=False` gates remain 100% intact.

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

This model-allocation policy is part of the research goal, not an optional
workflow preference. Codex should continue choosing the highest-value hard
reasoning problem until its usage is exhausted, leave exact assumptions,
falsifiers, claim gates, and acceptance tests, and treat exhaustion as a
handoff to Gemini rather than completion of the research objective.

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

## Current High-Reasoning Result: Schur Branch Merger Is the Orientation Polar in Encoded Coordinates (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_schur_branch_merger_polar_equivalence.py
tests/test_self_dual_wreath_schur_branch_merger_polar_equivalence.py
research/representation/self_dual_wreath_schur_branch_merger_polar_equivalence.json
EXP-CODE-SELF-DUAL-WREATH-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE
```

Let `J_e:M_e->X` include the physical invariant range
`M_e=ran(E_e)`, let `S=[J_e]_e`, and let `B=direct_sum_e B_e` be the
orthogonal Schur companion encoding. The natural encoded merger
`S_B=S B^*` obeys

```text
S_B S_B^* = sum_e E_e = A,
S_B^* S_B = B(S^*S)B^*,
polar(S_B) = polar(S)B^*.
```

The retained-character factor has the parallel identity
`polar(L C^*)=polar(L)C^*`, with its Gram equal to an isometric conjugate of
`I tensor H_nu`. Thus Schur encoding preserves every nonzero singular value
and does not remove either `A^(-1/2)` or `H_nu^(-1/2)`.

The physical-to-companion interface is nevertheless positive: after source
Schur decomposition, `Inv(V_nu^* tensor sigma_e)` factors exactly as the
canonical Bell invariant `|Omega_nu>` tensored with the opaque multiplicity
state. Bell unpreparation enters or leaves the companion without exposing a
standard Kronecker basis. Therefore physical and encoded polar compilers are
polynomially interreducible. The carrier interface is solved; the polar is
not.

A branch-faithful deterministic Stinespring map must retain orthogonal
environment tags whenever `J_e^*J_f` is nonzero. This rejects free unitary
which-path erasure, but not a structured direct polar, multi-round companion
transform, or decoder retaining branch characters. Three exact `S_3/S_4`
controls and eight focused tests pass. No physical PGM, decoder, classical
separation, algorithm, or speedup is claimed.

## Current High-Reasoning Result: Schur-Dilated Fixed-Source Multiplicity Access Boundary (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_schur_dilated_multiplicity_access.py
tests/test_self_dual_wreath_schur_dilated_multiplicity_access.py
research/representation/self_dual_wreath_schur_dilated_multiplicity_access.json
EXP-CODE-SELF-DUAL-WREATH-SCHUR-DILATED-MULTIPLICITY-ACCESS
```

The blanket claim that no efficient internal symmetric-group multiplicity
carrier is known is too strong. For fixed source Specht labels, append fixed
Schur--Weyl companion basis states and apply

```text
T = Schur_(n,d^k) R_site (Schur_(n,d)^dagger)^tensor-k.
```

Diagonal `S_n` equivariance gives

```text
T = direct_sum_nu I_(P_nu) tensor B_nu,
```

where `B_nu` coherently embeds the generalized Kronecker multiplicity into an
opaque joint companion subspace. With `d=n` and polynomial `k`, the corrected
high-dimensional Schur transform makes this global isotypic router
polynomial. Exact `S_3`, `S_4`, and `S_5` controls verify the
`GL(d_A d_B)` branching identity, diagonal isotypic projector ranks, at least
three active branch sectors per target, and the genuine multiplicity-two case
`g((3,2),(3,1,1),(3,1,1))=2`.

The important correction is that different source-label tuples occupy
orthogonal `U(d)^k` subgroup-branch sectors of the joint companion. A
source-controlled Schur router therefore retains orientation which-path
information and does **not** realize the physical cross-orientation kernel
`H_nu`. A separate coherent branch-mixing/erasure intertwiner is required
before `H_nu` appears. If one instead assumes a common output-coordinate
isometry on the orientation analysis map `L_nu`, it preserves
`L_nu^*L_nu=H_nu` and cannot whiten it. These are distinct statements and must
not be conflated.

Claim boundary:

```text
fixed-source encoded Kronecker carrier:             PROVED POLYNOMIAL
global fixed-source isotypic routing:                PROVED POLYNOMIAL
standard multiplicity coordinates:                  NOT EXPOSED
cross-orientation branch intertwiner:                OPEN
controlled Schur router realizes H_nu:               FALSE
common coordinate isometry improves H_nu:            FALSE
Racah associator / orientation polar / decoder:      OPEN
physical PGM / classical separation / speedup:       OPEN
```

The next high-judgment task is to characterize the minimum branch intertwiner
needed to map the orthogonal source sectors into a common orientation carrier.
Derive its equivariance constraints and normalization before attempting a
circuit. A useful positive result must compile the intertwiner with polynomial
normalization and then implement or bypass the `H_nu^(-1/2)` polar. A useful
negative result must prove that every allowed branch-erasure implementation
inherits factorial normalization, vanishing physical support, or a classical
simulation; dimension counting or opacity of the companion basis is not
enough. Do not claim that the Schur construction itself preserves the
cross-orientation Gram: only a common coordinate isometry would do that.

## Current High-Reasoning Result: Coherent Source Labels Do Not Cancel Power-Map Normalization (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_label_coherent_power_map_boundary.py
tests/test_self_dual_wreath_branch_character_label_coherent_power_map_boundary.py
research/representation/self_dual_wreath_branch_character_label_coherent_power_map_boundary.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-LABEL-COHERENT-POWER-MAP-BOUNDARY
```

The apparent escape from the termwise power-map normalization is now sharply
rejected. A mixed hidden-subgroup coset state is

```text
rho_H = |G|^-1 sum_(h in H) R_h.
```

Under the group QFT it is exactly block diagonal in inequivalent irrep labels.
Not measuring weak Fourier labels therefore does not supply cross-label
amplitudes: it retains a classical direct-sum block. The branch field also
preserves every fixed source tuple `Lambda`, so the global desired convolution
is `direct_sum_Lambda C_Lambda`. Wrong output-irrep blocks of the full
power-map isometry are orthogonal leakage, not paths to the same physical
output.

For the predecessor normalization

```text
alpha_(nu,Lambda)=|G|^k/sqrt(d_nu D_Lambda),
S_3=sum_lambda d_lambda^3,
```

independent Plancherel averaging gives the exact squared inverse coefficient

```text
E[alpha^-2] = S_3^(2k+1)/|G|^(4k+1)
              <= |G|^(-k+1/2).
```

Conditioning on global source distinctness changes this by at most the inverse
conditioning probability, which is `1+o(1)` at the natural copy scale. Cyclic
controls make the mechanism explicit: the norm-one transformed paired power
map spreads one input character over `m^(2k-1)` output tuples, but the mean
mass in the matching physical source block remains exactly `m^(-2k)`. Seven
focused tests pass, including an exact `S_3` coset-state QFT block-diagonality
control and nonabelian Plancherel enumeration.

Claim boundary:

```text
mixed-coset irrep-label superselection:             PROVED
source tuple conservation by the branch field:      PROVED
Plancherel label average cancels normalization:      FALSE
all output label blocks are useful target paths:     FALSE
whole-quadrant FFT-like factorization:                OPEN
arbitrary label-mixing direct polar/compiler:         OPEN
physical decoder / classical separation / speedup:   OPEN
```

This is not a no-go for a circuit that combines the complete quadrant
coefficient sum before labels are exposed, mixes and later restores labels, or
implements the direct polar by another representation-specific mechanism.

## Predecessor High-Reasoning Result: Power-Map Fourier Primitive Has Fatal Termwise Normalization (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_power_map_fourier_access_boundary.py
tests/test_self_dual_wreath_branch_character_power_map_fourier_access_boundary.py
research/representation/self_dual_wreath_branch_character_power_map_fourier_access_boundary.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-POWER-MAP-FOURIER-ACCESS-BOUNDARY
```

For a fixed exponent tuple `r`, the paired power map

```text
Phi_r(h)=(h^(1-r_1),h^r_1,...,h^(1-r_k),h^r_k)
```

is injective because either adjacent pair multiplies to `h`. It is efficiently
reversible, and QFT conjugation makes it a normalization-one nonlinear Fourier
isometry. The desired representation monomial is an exact selected block, but

```text
M_(nu,r) = alpha_(nu,Lambda) block(V_r),
alpha_(nu,Lambda)=|G|^k/sqrt(d_nu D_Lambda)
                 >= |G|^(k/2-1/4).
```

At `k=Theta(log|G|)`, extracting exponent terms independently is therefore
superpolynomial. Eight cyclic controls verify injectivity, the transformed
isometry, nonzero selection blocks, zero selection blocks, and exact scale.
The theorem deliberately does not reject coherent summation of all exponent
tuples before block selection.

### Next Codex Work After This Pause

Do not revisit source-label coherence. The two live theorem-level questions
are:

1. Derive or falsify a normalization-one whole-quadrant recursion. Work with
   the controlled field `|h>|psi> -> |h>J_h|psi>` and the complete cyclic
   coefficient tensor, not isolated power-map monomials. A positive result
   must erase the path/exponent workspace coherently, preserve the physical
   source tuple, and avoid any `sqrt(|G|)` or `|G|^(Omega(k))` postselection.
   A negative result must state an explicit architecture class, such as
   prepare-exponent/power-map/unprepare circuits of bounded recursion width;
   do not claim an arbitrary circuit lower bound.
2. Identify the exact native input density for the candidate convolution and
   compare it with the maximally mixed domain used by the Frobenius theorem.
   Prove the transfer if covariance makes it exact, or produce the missing
   Radon-Nikodym/operator-domination quantity if it does not. Do not infer this
   from average dimensions alone.

The physical relative element `h=s^-1g` is a summation path, not a native
register. Merely making `Phi_r(h)` reversible leaves the path-erasure problem
untouched. No implementation of either next theorem has been started.

### Gemini / Antigravity Boundary

Gemini 3.6 Flash should wire both new experiments, run broad validation, and
refresh registry/UI artifacts from the mechanical plan. It must preserve the
distinction between a termwise no-go, a label-coherence no-go, and the still
open whole-sum transform. It must not describe either theorem as a general
circuit lower bound or algorithmic speedup.

## Current High-Reasoning Result: Equivariant Multiplier Normal Form and Covariance-Only Insufficiency (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_equivariant_multiplier_normal_form.py
tests/test_self_dual_wreath_branch_character_equivariant_multiplier_normal_form.py
research/representation/self_dual_wreath_branch_character_equivariant_multiplier_normal_form.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-EQUIVARIANT-MULTIPLIER-NORMAL-FORM
```

For input source representation `P_x`, branch-completed output representation
`Q_x`, and Fourier irrep `rho_nu`, the exact field covariance and multiplier
equation are

```text
J_(x h x^-1) = Q_x J_h P_x^*,
(rho_nu(x) tensor Q_x) Jhat_nu
  = Jhat_nu (rho_nu(x) tensor P_x).
```

Thus `Jhat_nu` is an intertwiner. If

```text
rho_nu tensor P = direct_sum_tau rho_tau tensor C^(m_tau),
```

then Schur/Wigner-Eckart gives the exact normal form

```text
Jhat_nu = direct_sum_tau I_(d_tau) tensor R_(nu,tau),
R_(nu,tau): C^(m_tau) -> C^(2^k) tensor C^(m_tau).
```

Every reduced singular value is repeated `d_tau` times. The new Frobenius
contraction theorem controls their dimension-weighted spectral tail but does
not determine or synthesize their multiplicity-space singular vectors.

Conjugacy compression is also exact but does not solve access. For a class
representative `c`, the left-right representation twirl `T_c` equals the
average Fourier kernel over that class, and

```text
Jhat_nu = |G|^-1/2 sum_classes |class(c)| T_c.
```

The direct class-LCU coefficient one-norm is still `sqrt(|G|)`.

The reduced intertwiner algebra has complex dimension

```text
2^k sum_tau m_tau^2,
sum_tau m_tau^2 >= (d_nu dim(P))^2/|G|.
```

For the regular Plancherel master `P=Reg(G)^(tensor 2k)`, the bound is exact:

```text
m_tau = |G|^(2k-1) d_nu d_tau,
sum_tau m_tau^2 = |G|^(4k-1) d_nu^2.
```

Therefore covariance, an efficient `S_n` QFT, and state-weighted near-isometry
do not by themselves imply an efficient transform. They leave arbitrary huge
reduced maps. This is a structural underdetermination theorem, not a circuit
lower bound for the explicit quadrant field. Eight focused tests directly
verify covariance, intertwining, class twirls, character multiplicities, and
the Cauchy pressure; all 33 tests in the current theorem chain pass.

Claim boundary:

```text
field conjugation covariance:                       PROVED
equivariant/Wigner-Eckart multiplier normal form:   PROVED
class-twirl reconstruction:                         PROVED
direct class-LCU normalization bypass:              REJECTED
covariance plus near-isometry sufficient to compile: FALSE
specific quadrant reduced-map factorization:        OPEN
direct multiplier compiler / decoder / speedup:     OPEN
```

### Next Codex Work

Analyze the explicit reduced maps rather than their symmetry envelope. Expand
the local quadrant symbol into cyclic power-map coefficients, substitute that
expansion into `Jhat_nu`, and determine whether the reduced maps factor through
polynomially many Young-tower/Jucys-Murphy/centralizer-induction primitives.
The first decisive theorem should either:

1. exhibit a sequential reduced-map factorization with polynomial ancilla and
   normalization; or
2. prove that the power-map Fourier tensors have high operator Schmidt rank,
   high recoupling width, or a query lower bound on natural high-mass sectors.

Do not count a formal Wigner-Eckart decomposition as algorithmic progress.

### Gemini / Antigravity Boundary

Gemini 3.6 Flash should wire this theorem, regenerate its artifact, and run
broad validation without converting covariance-only underdetermination into a
universal circuit lower bound.

## Current High-Reasoning Result: Raw GPE Dilation Is Asymptotically Orthogonal to the Polar Transform (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_gpe_dilation_separation.py
tests/test_self_dual_wreath_branch_character_gpe_dilation_separation.py
research/representation/self_dual_wreath_branch_character_gpe_dilation_separation.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-GPE-DILATION-SEPARATION
```

The raw full-character Kraus field has an exact representation dilation. For
one source pair,

```text
K_h = [M_+(h);M_-(h)]
    = (H tensor I)(|0><0| tensor A_h + |1><1| tensor B_h)(|+> tensor I).
```

The controlled middle family is a genuine representation, so this raw field
is the obvious generalized-phase-estimation access substitute for the polar
field `J_h`. The substitute is now rejected asymptotically.

On an order-`m` cyclic eigenphase, the raw/polar branch overlap is one at the
`+/-1` axes and otherwise

```text
(|cos(pi t/m)|+|sin(pi t/m)|)/sqrt(2).
```

Uniform regular spectral multiplicity gives a closed-form local average
`a_m`. It equals one only for `m in {1,2,4}`. For every other order,

```text
a_m <= gamma = a_3 = a_6
               = [1+(1+sqrt(3))/sqrt(2)]/3
               = 0.9772838841927122...
```

Two independent Plancherel labels exactly reproduce the normalized
`Reg(S_n) tensor Reg(S_n)` trace. Therefore `k` independent source pairs have
annealed normalized global convolution overlap

```text
E_Lambda overlap(C_raw,C_polar)
  = (1/n!) sum_(h in S_n) a_ord(h)^k.
```

An order-dividing-four permutation has at least `n/4` cycles. The exact cycle
moment `E[2^cycles]=n+1` gives

```text
Pr[ord(h) divides 4] <= (n+1)2^(-n/4),
E overlap <= (n+1)2^(-n/4)+gamma^k.
```

At `k=ceil(3log2(n!))+2` this vanishes. Nonnegativity and the existing
`Pr(global distinct)=1-o(1)` theorem transfer it to physical collision-free
source portfolios. Markov then gives

```text
||C_raw-C_polar||_F^2/(n! D) -> 2
```

for typical natural portfolios. Eight focused tests pass, including the exact
two-Plancherel-to-regular reduction at `S_3`, cyclic closed forms through
order 1024, and direct low-order permutation controls.

The canonical pair of controlled-`J_h` PREPARE isometries exposes
`C_polar/sqrt(n!)`. The new quadrant theorem says `C_polar` has order-one
singular values on almost all normalized domain mass, so bounded uniform QSVT
still requires `Omega(sqrt(n!))` degree on that good sector. State-weighted
conditioning does not repair the generic subnormalization.

Claim boundary:

```text
raw representation dilation:                         PROVED
raw-to-polar natural convolution overlap vanishes:   PROVED
raw GPE substitution:                                REJECTED
generic controlled-field LCU/QSVT:                   SUPERPOLYNOMIAL
direct conjugation-equivariant multiplier normal form: OPEN
direct representation-specific multiplier compiler: OPEN
physical decoder / classical separation / speedup:   OPEN
```

### Next Codex Work

Derive the conjugation-equivariant Fourier multiplier normal form. From

```text
J_(x h x^-1) = (I_character tensor P_x) J_h P_x^*,
Jhat_nu = |G|^-1/2 sum_h rho_nu(h^-1) tensor J_h,
```

show exactly which irreducible and multiplicity blocks `Jhat_nu` couples,
which reduced matrices must be synthesized, and whether generalized phase
estimation plus symmetric-group QFT/CG primitives can implement them without
`sqrt(n!)` or `sqrt(d_nu)` normalization. Try to prove a reduced-matrix rank,
entropy, or query obstruction before assuming this is a positive route.

### Gemini / Antigravity Boundary

Gemini 3.6 Flash should wire and validate this module mechanically. It must
not rewrite an access-model QSVT lower bound as an arbitrary-circuit lower
bound, and it must leave direct equivariant synthesis explicitly open.

## Current High-Reasoning Result: All-Order Quadrant Overlap and Natural Frobenius Contraction (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_cyclic_quadrant_overlap.py
tests/test_self_dual_wreath_branch_character_cyclic_quadrant_overlap.py
research/representation/self_dual_wreath_branch_character_cyclic_quadrant_overlap.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-CYCLIC-QUADRANT-OVERLAP
```

This pass closes the all-order lemma left open by the natural Frobenius
word-map reduction. For the four-ray branch-polar symbol `s_m`, if `H<C_m`
has index `q`, its group-algebra coefficient mass on `H` is exactly zero for
even `q` and `1/q^2` for odd `q`. The proof is the quotient-fiber identity

```text
sum_(l=0)^(q-1) s_(dq)(a+ld) = 0       q even
                              = s_d(a) q odd,
```

followed by quotient Parseval. Therefore two elements generating different
cyclic subgroups have branch-symbol correlation at most `1/3` and Naimark
range overlap at most `2/3`.

If two distinct elements generate the same order-`m` cyclic subgroup, write
the second generator as the `u`th power of the first. The exact correlation
numerator is

```text
T_m(u) = m - 4 d_m(u),
```

where `d_m(u)` counts positive open-half residues mapped to the negative open
half. Alternating preimage intervals of length `m/(2 min(u,m-u))`, with
separate exact cases for even multipliers, odd multipliers, `a=3`, and the
antipodal multiplier, prove `d_m(u)>=m/8`. Hence `T_m(u)<=m/2` and every
distinct pair in every finite group obeys

```text
Tr(P_a P_b)/|G|^2 <= 3/4.
```

The bound is sharp at cyclic order eight with multiplier three. The direct
symbol identity, quotient identity, proper-subgroup Fourier mass, and every
nonidentity unit through order 512 were checked; `S_3` and `S_4` regular
controls also pass. These checks are falsifiers, not the proof.

Combining the theorem with the exact regular word-moment identity proves

```text
E R <= (|G|-1)(3/4)^k.
```

For `k=ceil(3 log2 |G|)+2`, the exponent is
`1+3 log2(3/4)=-0.245112...`. For `G=S_n`, the existing global-distinct
source theorem has `Pr(D)=1-o(1)` at this scale, and positivity gives
`E[R|D]<=E[R]/Pr(D)=o(1)`. Markov plus the Frobenius tail inequality proves
source-typical normalized-Frobenius contraction and vanishing bad spectral
mass for a maximally mixed domain.

Claim boundary:

```text
all finite-group q<=3/4 range overlap:              PROVED
all-n natural collision-free Frobenius contraction: PROVED
maximally mixed domain bad spectral mass vanishes:  PROVED
uniform minimum singular value:                     NOT PROVED
physical input Fourier domination:                  NOT PROVED
normalization-one dense transform access:           NOT COMPILED
physical decoder:                                    NOT COMPILED
classical separation / speedup:                      NOT PROVED
```

The predecessor
`self_dual_wreath_branch_character_natural_frobenius_word_map.py` and its
artifact now reflect the closed all-order gate. Seventeen focused tests pass.

### Next Codex Work

Do not spend high-capability usage on registry wiring. The bottleneck has
moved to structured coherent access. Derive or kill a factorization of the
dense relative convolution `C` (or an equivalent block encoding) using the
nonabelian Fourier multiplier decomposition, cyclic branch-symbol support,
and Young/Racah transforms. The decisive target is a normalization-one or
polynomial-normalization block encoding whose preparation and selection costs
are polynomial in `n` and `k`, on the proven state-weighted good sector. Try
to prove lower bounds against generic LCU/QSVT constructions before treating
any factorization as progress. Physical input domination and decoding remain
separate proof obligations.

### Gemini / Antigravity Boundary

Gemini 3.6 Flash should wire the new experiment ID through the registry,
runner, `qsearch.py`, README command table, and dispatch tests, regenerate the
new and predecessor artifacts, run broad validation, and preserve every gate
above exactly. It must not rewrite normalized-Frobenius contraction as a
minimum-singular-value theorem or algorithmic speedup. Exact commands and
acceptance checks are in `research/MECHANICAL_FOLLOW_UP_PLAN.md`.

## Current High-Reasoning Result: Autocorrelation Is a Fourier-Tail Problem, Not a Pointwise-Norm Problem (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary.py
tests/test_self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary.py
research/representation/self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-NAIMARK-AUTOCORRELATION-FOURIER-BOUNDARY
```

For the candidate-relative convolution and its autocorrelations,

```text
C[g,s]=|G|^-1/2 J_(s^-1 g),
A_x=|G|^-1 sum_h J_h^*J_(xh),
```

the exact nonabelian Fourier multipliers are

```text
Jhat_nu=|G|^-1/2 sum_h rho_nu(h^-1) tensor J_h,
C ~= direct_sum_nu I_(d_nu) tensor Jhat_nu.
```

Thus the convolution singular spectrum is the union of each multiplier
spectrum repeated `d_nu` times. Uniform conditioning is an extreme-block
problem, not a bound on one autocorrelation at a time. Matrix-valued Parseval
gives the exact identity

```text
||C^*C-I||_F^2/(|G| dim H)
 = sum_x ||A_x-delta_(x,e)I||_F^2/dim H
 = sum_nu d_nu||Jhat_nu^*Jhat_nu-I||_F^2/(|G|dim H).
```

The decisive counterexample is the completed Legendre phase on `Z_p`, for
prime `p=3 mod 4`. Every pointwise value is an isometry and every nonidentity
autocorrelation is exactly `-1/p`, but the convolution singular values are
`1/sqrt(p)` once and `sqrt(1+1/p)` otherwise. Its condition number is
`sqrt(p+1)` and its Gram operator-norm error is `1-1/p`. This refutes the
planned implication that maximum nonidentity autocorrelation `O(1/|G|)` gives
a uniform constant gap.

The counterexample also shows why uniform conditioning is too strong as the
only target. Its normalized Frobenius error is `(p-1)/p^2`, and the bad
Fourier sector has normalized regular-input mass exactly `1/p`. In general,
normalized Gram Frobenius error `R` bounds maximally mixed mass outside an
`epsilon` Gram window by `R/epsilon^2`. State-weighted trimming can therefore
remain viable even when the minimum singular value vanishes asymptotically.

Exact `S3` controls reproduce the complete direct convolution spectrum from
the Fourier blocks. The three-pair threshold control still has condition
`1.4950900031928052` and normalized Gram Frobenius residual
`0.10763888888888895`. Eight focused tests and 42 adjacent tests pass, the live
artifact is generated, and `git diff --check` is clean.

Strict false gates:

- no all-`n` natural state-weighted Fourier-tail theorem;
- no proof that the physical input is maximally mixed or suitably dominated;
- no uniform natural branch Fourier gap;
- no normalization-one dense multiplier compiler;
- no physical PGM decoder, classical separation, algorithm, or speedup.

### Refined Next High-Reasoning Task

1. Derive the exact annealed formula for the natural-source normalized Gram
   Frobenius residual. Expand `||A_x||_F^2` over shared `h,h'` and factor only
   across independent source labels, never across the shared group average.
2. Condition on unequal/global-distinct Plancherel pairs and quantify the
   total-variation perturbation.
3. Identify the actual physical input density in the group Fourier sectors;
   prove maximally mixed input or a domination bound before applying the tail
   lemma.
4. If the residual is `o(1)` at `k=ceil(log2(n!))+O(1)`, retain the
   state-weighted route and attack structured access separately. If it stays
   constant, close this Naimark-convolution route.
5. Do not return to a maximum-per-offset operator-norm target; the Legendre
   family has falsified that proof strategy.

## Current High-Reasoning Result: Exact Known-Relative Polar Naimark Completion (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_polar_naimark_completion.py
tests/test_self_dual_wreath_branch_character_polar_naimark_completion.py
research/representation/self_dual_wreath_branch_character_polar_naimark_completion.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-POLAR-NAIMARK-COMPLETION
```

For one unequal pair and known relative permutation `h`, let

```text
V_s(h)=polar((A(h)+sB(h))/2), P_s=V_s^*V_s, F=P_+ + P_-.
```

On every eigenphase of `U=A^*B`, `F` is one at `+/-1` and two otherwise.
Hence `I<=F<=2I` and

```text
J_h=(|0>V_+ + |1>V_-)F^-1/2
```

is an exact isometry. The cyclic phase register applies the extra factor, so
no inverse minimum singular value is used. Tensoring over `k` source pairs
gives the full `2^k` coefficient-output isometry with `k` local cyclic
compilers. An `S4` mixed-phase witness attains the sharp frame condition two.
Eight focused tests pass, 19 local controls and six tensor controls have zero
failures, and the artifact is generated.

This is only a known-relative dense primitive. Pointwise isometries do not
automatically assemble the unknown-relative convolution, and neither the
physical orientation polar nor a decoder follows.

## Current High-Reasoning Result: Almost All Natural Joint-Target Mass Has Factorial-Scale Row Dimension (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_joint_character_natural_sector_mass.py
tests/test_self_dual_wreath_joint_character_natural_sector_mass.py
research/representation/self_dual_wreath_joint_character_natural_sector_mass.json
EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-NATURAL-SECTOR-MASS
```

For fixed source pairs `Lambda=((lambda_i,mu_i))`, orientation `e` selects one
partition `alpha_i(e)` per pair. The exact target-sector law is

```text
p_nu(Lambda)=Tr(D_nu)
 =2^-k sum_e d_nu g(alpha_1(e),...,alpha_k(e);nu)
              /product_i d_(alpha_i(e)).
```

The unselected carrier dimensions cancel. Each orientation is therefore the
dimension-weighted Kronecker transition from the existing Plancherel
recoupling theorem. With all `2k` source partitions independent Plancherel,
the annealed target law is exactly Plancherel for every `k>=1`:

```text
E_Lambda p_nu(Lambda)=d_nu^2/n!.
```

Conditioning all sources globally distinct changes the source law in total
variation by exactly the collision probability. Data processing gives the
same upper bound on the target-law perturbation. The existing collision-free
mass theorem makes this `o(1)` at `k=ceil(log2(n!))+O(1)`.

Let `p(n)` be the partition number and
`R_n=floor(sqrt(n!)/p(n))`. Counting irreps gives the exact tail bound

```text
Plancherel[d_nu<=R_n] <= 1/p(n).
```

Hence the collision-conditioned annealed low-row mass is
`delta_n<=1/p(n)+Pr(collision)=exp(-Theta(sqrt(n)))`. Markov then gives
low-row mass at most `sqrt(delta_n)` for at least `1-sqrt(delta_n)` of natural
source tuples. Thus `1-o(1)` physical sector mass lies on
`d_nu>sqrt(n!)/p(n)`. At `n=512`, the exact threshold has log2
`1865.6676...`, and the canonical direct-analysis generic degree lower bound
on that mass has log2 `932.8046...`.

This closes the mass loophole in the previous theorem: the
`sqrt(d_nu)` canonical normalization is not confined to an arbitrary balanced
witness. It occurs on almost all natural sector mass, so rare low-dimensional
sectors cannot provide an inverse-polynomial-mass decoder for that
architecture.

The target irrep marginal is hidden-label independent. High-dimensional mass
does **not** prove extensive hidden information inside `D_nu`, nor does it
rule out a fused direct polar. Those gates remain false. Fifty-one adjacent
tests pass, the live artifact is generated, and `git diff --check` is clean.

### Refined Next High-Reasoning Task

1. Decompose joint Holevo information or PGM success by the high-dimensional
   target sectors and prove an all-`n` lower bound, or produce a dequantizing
   upper bound.
2. Use the exact source-conditioned `D_nu` projection-Gram formula; target
   Plancherel mass alone is not information.
3. If extensive information survives, attack `polar(A_nu)` directly through
   the orientation kernel, multi-round branch relocation, or a fused
   covariant transform. Generic density/direct amplification is now closed on
   typical mass.
4. If the high-row blocks carry only `o(log n!)` Holevo information, close the
   retained-character route and redirect to a different nonabelian mechanism.

Routine registry, runner, CLI, README, ledger, and broad repetitive validation
belongs to Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: The Canonical Joint Analysis Map Has Exact `sqrt(d_nu)` Dilution (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_joint_character_analysis_map_normalization.py
tests/test_self_dual_wreath_joint_character_analysis_map_normalization.py
research/representation/self_dual_wreath_joint_character_analysis_map_normalization.json
EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-ANALYSIS-MAP-NORMALIZATION
```

Let `r=d_nu`, `q=2^k`, `d=dim(C)`, let `G_nu=L_nu^*L_nu` be the exact
projection Gram, and let `W` be the branch Walsh transform. The rectangular
factor whose Gram is the joint multiplicity operator is

```text
A_nu=sqrt(r/(q d)) L_nu(I_r tensor W)^*,
A_nu^*A_nu=D_nu.
```

This is the correct direct-polar target. The canonical coherent circuit is
more weakly normalized: Walsh preparation, a maximally entangled carrier
pair, controlled invariant projection `E_e`, and selected-row Walsh erasure
produce

```text
N_nu=L_nu(I_r tensor W)^*/sqrt(q d)=A_nu/sqrt(r),
N_nu^*N_nu=D_nu/r.
```

Thus the direct canonical map and the global purification theorem expose the
same Schur-row Gram exactly. Direct rectangular access improves generic
rescaling from `Omega(r)` to `Omega(sqrt(r))`, but does not remove it. A
Bernstein argument proves that a single bounded singular-value polynomial
uniformly amplifying `A/sqrt(r)` to `A` has degree `Omega(sqrt(r))`. Balanced
two-row dimensions make this exponential; the live `n=512` witness has a
degree lower bound with log2 approximately `249.5548`.

Scalar dilution does not change the mathematical polar:
`polar(A/sqrt(r))=polar(A)`. Consequently this is not a circuit lower bound.
A representation-specific polar, multi-round branch relocation, or fused
covariant isometry could bypass generic amplification. Natural large-row
sector mass was not established by this module, and no decoder or speedup is
claimed. Sixty-six adjacent tests pass and the live artifact is generated.

### Refined Next High-Reasoning Task

1. Transfer the exact Plancherel recoupling stationarity theorem to the
   physical target law `p_nu=Tr(D_nu)`.
2. Under globally distinct source conditioning, use total-variation
   contraction and the collision-free mass theorem to prove or falsify that
   `d_nu` is superpolynomial on `1-o(1)` physical sector mass.
3. Keep target-sector mass separate from hidden-label information inside each
   multiplicity block.
4. If high-row natural mass is proved, the canonical-access no-go becomes
   operational on typical input mass, but direct structured polar synthesis
   remains the only legitimate escape.

Routine registry, runner, CLI, README, ledger, and broad repetitive validation
belongs to Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Global Joint Purification Access Is Easy, But It Exposes `D_nu/d_nu` (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_joint_character_purification_access_boundary.py
tests/test_self_dual_wreath_joint_character_purification_access_boundary.py
research/representation/self_dual_wreath_joint_character_purification_access_boundary.json
EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURIFICATION-ACCESS-BOUNDARY
```

The native retained group--orientation-character amplitudes give the exact
purification

```text
Psi_g[(s,z),a]=vec(K_z(s^-1 g))[a]/sqrt(|G| dim(C)),
tau_g=Psi_g Psi_g^*.
```

A uniform coherent hidden-label register and controlled left translation
therefore purify `bar(tau)=|G|^-1 sum_g tau_g`. Reusing the exact
purification--SWAP theorem gives a normalization-one block encoding of this
global average in polynomially many gates under the already assumed native
branch-character preparation and efficient `S_n` action. The old blanket
statement that coherent access to the average state was open is false.

This does **not** block-encode the multiplicity operator with normalization
one. After the `S_n` QFT,

```text
bar(tau)=direct_sum_nu I_(d_nu)/d_nu tensor D_nu.
```

Every fixed Fourier row exposes `D_nu/d_nu`. Conditioning on the whole `nu`
sector divides by `p_nu=Tr(D_nu)` but leaves
`I/d_nu tensor D_nu/p_nu`; selecting a row still has conditional probability
`1/d_nu`. Three exact `S3/S4` controls verify the native purification, coherent
twirl, Schur row blocks, zero cross-row blocks, and failure of sector
conditioning to remove the row factor.

There is also an exact generic polynomial-transform boundary. A bounded
polynomial that uniformly converts `D/d` to `D` at constant error has degree
`Omega(d)` by Bernstein's inequality. For the balanced two-row irrep
`nu=(m,m)` of `S_(2m)`, `d_nu=Catalan(m)=2^Theta(n)/poly(n)`. The generated
scaling witness reaches `log2 d_nu=499.1679...` at `n=512`.

Scope is strict. The theorem does not prove that a balanced two-row sector has
natural source mass or identification information. It is not a circuit lower
bound and does not rule out a normalization-one restriction map, a direct
representation-specific polar, or a fused covariant isometry that never
materializes `D_nu`. Normalization-one `D_nu` access, direct fused polar,
all-`n` information, classical separation, algorithm, and speedup gates remain
false. Forty-one adjacent tests pass and `git diff --check` is clean.

### Refined Next High-Reasoning Task

1. Stop treating global density access as an open problem or as a decoder.
2. Work in the stronger direct-analysis access model: identify the exact
   restriction/analysis map whose Gram is the joint-character `D_nu`, not
   `D_nu/d_nu`.
3. Determine whether the known-relative cyclic local polars can assemble its
   polar without learning `s^-1 g_hidden`, while respecting the exact norm-two
   `S3` cocycle defect.
4. If direct assembly still recreates an exponentially small normalized
   singular scale, prove that equivalence and close this restricted route.
5. Do not infer a natural obstruction from the balanced witness until a
   source-weighted large-row mass theorem is proved.

Routine registry, runner, CLI, README, ledger, and broad repetitive validation
belongs to Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Known-Relative Character Polars Compile, But Their Phase Field Has Maximal Holonomy (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_branch_character_cyclic_polar_compiler.py
tests/test_self_dual_wreath_branch_character_cyclic_polar_compiler.py
research/representation/self_dual_wreath_branch_character_cyclic_polar_compiler.json
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-CYCLIC-POLAR-COMPILER
```

For one unequal source pair and a **known** relative permutation `h`, the
orientation-character carrier factor is

```text
M_s(h)=(A(h)+sB(h))/2=A(h)(I+sU(h))/2,
U(h)=A(h)^*B(h), s in {+1,-1}.
```

If `m=ord(h)` and `U(h)` has eigenvalue `omega^j`, the exact partial-polar
phase is

```text
s=+1: exp(pi i j/m) sign(cos(pi j/m)), j != m/2;
s=-1: -i exp(pi i j/m),                j != 0,
```

with the excluded eigenphase sent to zero. Coherent phase estimation over
`Z_m`, followed by this phase and uncomputation, therefore implements
`polar(M_s(h))` directly. Controlled powers use representation actions of
`h^r` and `h^-r`; `log ord(h)<=log(n!)`, so the circuit is polynomial under
the same efficient Young-representation action assumptions already used by
GPE. It never amplifies a singular magnitude and has no inverse-minimum-
singular-value cost.

The complete character Kraus operator is a tensor product of the local
factors, and polar commutes exactly with tensor products, including
rank-deficient factors. Eighteen local and twenty-four threshold-copy `S3`
controls match direct SVD polars with zero failures. Seven focused tests pass.

This does **not** compile the physical hidden-label decoder. In the native
row-copy state the relative element is `h=s_time^-1 g_hidden`, so the circuit
does not know it. A one-pass correction based only on `s_time` would require
the local polar field to satisfy a cocycle law. The natural `S3`
`(trivial,standard)` plus-character channel gives an exact full-rank
counterexample: for a three-cycle `c`,

```text
||V(c)^2-V(c^2)||=2.
```

Both `V(c)` and `V(c^2)` are unitaries. This is a branch-cut/holonomy defect,
not a small singular-value effect. Known-relative local phase normalization is
now solved; hidden-relative covariant assembly, the joint `D_nu` multiplicity
inverse, complete orientation polar, classical separation, algorithm, and
speedup gates remain false.

### Refined Next High-Reasoning Task

1. Use the compiler only where the relative group element is coherently known.
   Do not claim it can condition on `s^-1 g_hidden`.
2. Determine whether a path/holonomy register can assemble the cyclic polars
   into the joint group-character multiplicity transform, including output
   gauge and physical success mass.
3. Alternatively derive a normalization-one block encoding of the Schur
   multiplicity operators `D_nu` whose positive part uses these local cyclic
   phase primitives and whose conditioning survives the native law.
4. Test any assembly against the exact norm-two `S3` cocycle counterexample,
   the arbitrary-basis sublinear-rank no-go, and the existing generic
   normalized-access lower bounds.
5. Keep all decoder and speedup gates false until the unknown-relative
   covariance problem is solved end to end.

Routine registry, runner, CLI, README, and ledger wiring is assigned to Gemini
3.6 Flash through Antigravity.

## Current High-Reasoning Result: Split Sectors Do Not Obstruct Natural Branch Regularity (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_split_sector_branch_regularity.py
tests/test_self_dual_wreath_split_sector_branch_regularity.py
research/representation/self_dual_wreath_split_sector_branch_regularity.json
EXP-CODE-SELF-DUAL-WREATH-SPLIT-SECTOR-BRANCH-REGULARITY
```

The connected-Clifford route no longer needs an unsupported theorem saying
that an `O(n log n)` Plancherel tuple contains no self-conjugate partitions.
Restriction gives an exact refined `A_n` Plancherel law:

- a nonself transpose pair restricts to one `A_n` irrep with weight twice
  either `S_n` atom;
- a self-conjugate `S_n` irrep splits into two constituents of half its
  dimension, each with half its `S_n` Plancherel weight.

If `C_S=sum_lambda p_lambda^2` and `C_A` is the refined alternating collision,
then exactly

```text
C_A=2 sum_(lambda nonself) p_lambda^2
    +(1/2) sum_(lambda self) p_lambda^2,
C_S/2 <= C_A <= 2 C_S,
max A_n atom <= 2 max S_n atom.
```

This is the physical native source law. In the regular master, partial trace
of every lifted diagonal subgroup projector over the target is the source
identity because `Tr(L_s)=|S_n| 1[s=1]`. Refining the trace-biased source
marginal therefore gives independent `A_n` Plancherel labels, not an auxiliary
sampling model.

The maximal-dimension theorem makes `C_A=exp(-Theta(sqrt(n)))`. At
`K=ceil(log2(n!))+2`, the probability that any source pair has equal refined
`A_n` labels is at most `K C_A=o(1)`. Whenever the labels in every pair differ,
every nonzero pair-swap mask changes an `A_n^(2K)` coordinate irrep. Hence the
branch group `C_2^K` acts freely with probability tending to one even if many
coordinates originate from self-conjugate `S_n` partitions.

Split diagonal action also has the exact index-two factorization

```text
E_e^(S_n)=((I+rho_e(t))/2) E_e^(A_n)
```

for any odd involution `t`. Reassembling this parity projection gives the same
branch cross Gram `F/2^K` and the same orientation analysis polar as before.
Thus split constituents add coherent parity bookkeeping but do not scalarize
or compile the dense matrix-CS multiplicity transform.

Fourteen exact Plancherel controls and actual `S3`/`S4` split-sector matrix
controls pass with zero failures; seven focused tests pass. Full connected-
group Clifford transform, dense CS polar, complete orientation polar,
classical separation, and speedup gates remain false.

### Refined Next High-Reasoning Task

1. Delete self-conjugate mass decay from the connected branch-orbit premise.
   Do not spend further theorem effort trying to prove tuple-level absence.
2. Treat the easy parity quotient and split projection as solved bookkeeping.
   The sole quantum gate remains the dense `A_n` multiplicity/subduction CS
   polar after those labels are exposed.
3. Seek a direct normalization-one recoupling or a recursive child-coefficient
   factorization that uses all `2^K` output dimensions but has polynomial gate
   complexity.
4. Test every candidate against the arbitrary-basis sublinear-rank no-go,
   generic normalized-access lower bounds, GPE subblock boundary, and existing
   pair/common-support no-gos.
5. Do not infer circuit hardness from full rank, split-sector parity, or QFT
   label exposure.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Physical Trace Bias Closes Every Sublinear-Rank Coefficient Router (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_trace_biased_coefficient_rank_no_go.py
tests/test_self_dual_wreath_trace_biased_coefficient_rank_no_go.py
research/representation/self_dual_wreath_trace_biased_coefficient_rank_no_go.json
EXP-CODE-SELF-DUAL-WREATH-TRACE-BIASED-COEFFICIENT-RANK-NO-GO
```

This result upgrades the adaptive Walsh no-go to an arbitrary-basis output-
rank theorem. For each active native Fourier block `beta`, with orientation
projectors `E_e` and `F_beta=sum_e E_e`, complete polar cancellation identifies
the exact reduced coefficient state

```text
rho_beta[e,f]=Tr(E_e E_f)/Tr(F_beta).
```

It is positive with trace one. If
`a_beta=max_e Tr(E_e)/Tr(F_beta)`, projector positivity gives the pointwise
bound

```text
Tr(rho_beta^2)
  <= a_beta Tr(F_beta^2)/Tr(F_beta).
```

The existing simultaneous orientation-rank concentration theorem implies,
outside a product-Plancherel source event of probability
`delta_n=o(2^-K)`,

```text
a_beta <= (1+epsilon)/(2^K(1-epsilon))
```

for every orientation and target. Under the physical trace-biased block law,
the source marginal is exactly product Plancherel and regular-master trace
cancellation gives

```text
E[Tr(F_beta^2)/Tr(F_beta)] = 1+(2^K-1)/|S_n| = O(1).
```

After conditioning all sources to be globally distinct, whose probability
tends to one at `K=ceil(log2(n!))+2`, the average output purity is `O(2^-K)`.
For every block-dependent effect `0<=A_beta<=I` with `Tr(A_beta)<=m`, in any
basis and depending arbitrarily on measured source and target labels,

```text
E Tr(A_beta rho_beta) <= sqrt(m E Tr(rho_beta^2)).
```

Therefore every `m=o(2^K)` coefficient-output router retains vanishing native
PGM mass; constant mass requires `Omega(2^K)` coefficient dimension. This
strictly subsumes sparse adaptive Walsh routing as an output-retention claim.

Exact `S3,K=1` and `S4,K=2` controls verify positivity, trace one, the
pointwise purity inequality, trace-biased normalization, product-Plancherel
source marginal, and the arbitrary-rank Hilbert--Schmidt bound. The `S3`
average total coherence is exactly `7/6`; the `S4,K=2` globally-distinct mass
is exactly `89/1536`. Seven focused tests pass, zero controls fail, and the
`n=128` `K^6`-rank retained-mass envelope is about `1.57e-99`.

Claim scope is intentionally narrow. This is an output-rank theorem, not a
gate lower bound. A tensor Hadamard, dense representation-specific recoupling,
direct rectangular-CS transform, or complete orientation polar can use all
`2^K` coefficient dimensions in a polynomial-size circuit. None is rejected
or compiled here. Classical separation, an end-to-end algorithm, and every
speedup gate remain false.

### Refined Next High-Reasoning Task

1. Stop searching for sparse coefficient bases: arbitrary-basis sublinear
   output rank is now closed under the physical source law.
2. Analyze only succinct dense mechanisms. Seek an exact recursive
   factorization of the restricted child coefficient map using representation-
   specific recoupling or a normalization-one block encoding.
3. Explicitly test every proposed factorization against the existing pair-
   GPE, common-support, latent-master, source-gauge, connected-Clifford, and
   generic-access no-go theorems.
4. If the positive route fails, prove a circuit lower bound only for a sharply
   specified representation-specific transform class. Do not infer gate
   complexity from output rank or dense support.
5. Preserve false complete-polar, classical-separation, algorithm, and speedup
   gates until a coherent compiler and independent classical lower bound both
   exist.

Routine registry, runner, CLI, README, artifact-ledger, and broad validation
work is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Physical Trace Bias Closes Adaptive Sparse Walsh Routing (2026-08-24)

Files and experiment ID:

```text
theorems/self_dual_wreath_trace_biased_adaptive_walsh_no_go.py
tests/test_self_dual_wreath_trace_biased_adaptive_walsh_no_go.py
research/representation/self_dual_wreath_trace_biased_adaptive_walsh_no_go.json
EXP-CODE-SELF-DUAL-WREATH-TRACE-BIASED-ADAPTIVE-WALSH-NO-GO
```

The open source-adaptive Walsh collision gate is resolved without a
blockwise character `L4` estimate. For block
`beta=(nu;lambda_1,mu_1,...,lambda_K,mu_K)`, define

```text
F_beta=sum_e E_(beta,e),
b_beta(z)=Tr(F_beta)^(-1) sum_e Tr(E_(beta,e) E_(beta,e+z)).
```

The physically relevant native sector law is trace biased:

```text
pi(beta)=m_beta Tr(F_beta)/(q |G|^(2K)),
m_beta=d_nu product_i d_lambda_i d_mu_i, q=2^K.
```

Target-dimension-weighted rank completeness gives exactly

```text
sum_nu d_nu Tr(F_(nu,Lambda))=q product_j d_(Lambda_j),
```

so the source marginal under `pi` is the product Plancherel law, despite the
fixed-target trace bias. For projectors, `0<=Tr(PQ)<=Tr(P)`, hence every
`b_beta(z)` lies in `[0,1]`. Regular-master decomposition and the exact Walsh
flatness theorem give

```text
E_pi b_beta(0)=1,
E_pi b_beta(z)=1/|G| for z!=0.
```

Thus `E b_beta(z)^2<=E b_beta(z)`. For any source event `D` of product-
Plancherel probability `P_D`, the exact collision reduction now yields

```text
E[C_beta|D] <= q^(-1)[1+(q-1)/(|G| P_D)].
```

Every block-dependent set of at most `m` Walsh modes therefore retains
average native mass at most `sqrt(m E[C_beta|D])`. For global distinctness,
`P_D->1`; at `K=ceil(log2(n!))+2`, `q=Theta(n!)`, so collision is `O(1/q)`.
Every source-and-target-label-adaptive `m=o(q)` Walsh set has vanishing mass,
and constant retention requires `Omega(q)` modes.

Exact `S3,K=1` and `S4,K=2` controls verify the complete regular block
normalization, first moments, source marginal, collision contraction, and
adaptive-set bound. In the latter control the direct trace-biased globally
distinct mass is exactly `89/1536`. Seven focused tests pass; the artifact has
zero control failures and tail `K^6` retention upper bound about `8.76e-100`.

Scope remains strict. This closes sparse Walsh-output retention, including
block-adaptive choices. It does not prove Walsh circuit hardness, reject a
dense Hadamard, reject non-Walsh recoupling, compile direct rectangular CS,
compile the complete orientation polar, prove classical hardness, or permit a
speedup claim.

### Refined Next High-Reasoning Task

1. Remove adaptive sparse Walsh routing from the positive-route queue. No
   further character-collision theorem is needed for this no-go.
2. Focus on dense structured recoupling or direct restricted rectangular-CS
   compilation. The output must use `Omega(2^K)` Walsh support, but that alone
   is not a circuit lower bound because tensor Hadamards are efficient.
3. Derive a normalization-one block encoding or exact recursive factorization
   of the restricted child coefficient map. Test it against the existing
   pair-GPE, common-support, latent-master, gauge, and connected-Clifford
   no-go theorems.
4. If no positive factorization exists, seek a representation-specific lower
   bound for the endpoint inverse-square-root/rectangular-CS map, not a generic
   dense-support argument.
5. Keep complete-polar, classical-separation, algorithm, and speedup gates
   false until an executable coherent compiler and an independent classical
   lower bound both exist.

Routine registry, runner, CLI, README, stale cross-reference, and broad
validation work is assigned to Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Adaptive Walsh Routing Reduces To Collision Strata (2026-08-21)

**Superseded open gate:** the blockwise collision identity below remains
correct, but its physical collision obligation is now resolved by the
trace-biased positivity theorem above. Do not continue the proposed character
`L4` route merely to close adaptive Walsh routing.

Files and experiment ID:

```text
self_dual_wreath_source_adaptive_walsh_collision_reduction.py
tests/test_self_dual_wreath_source_adaptive_walsh_collision_reduction.py
research/representation/self_dual_wreath_source_adaptive_walsh_collision_reduction.json
EXP-CODE-SELF-DUAL-WREATH-SOURCE-ADAPTIVE-WALSH-COLLISION-REDUCTION
```

For an arbitrary fixed source block with `q=2^K` orientation projectors
`{E_e}`, set `F=sum_e E_e` and let `p_S` be the ideal polar output
probability after a Walsh transform of the orientation register. Define

```text
b_z = Tr(F)^(-1) sum_e Tr(E_e E_(e+z)).
```

Scalar Walsh inversion and Parseval give the exact identities

```text
p_S = q^(-1) sum_z (-1)^(S.z) b_z,
C := sum_S p_S^2 = q^(-1) sum_z b_z^2.
```

Consequently, every source-label-dependent set of at most `m` Walsh modes
retains at most `sqrt(m C_Lambda)` ideal mass in block `Lambda`, and Jensen
gives average retained mass at most `sqrt(m E C_Lambda)`. This eliminates the
previous exponential union bound over adaptive mode choices. Under any
pair-exchangeable source law, `E b_z^2` depends only on `|z|`, so the entire
adaptive sparse-routing question reduces to `K+1` Hamming strata:

```text
E C = q^(-1) sum_(j=0)^K binom(K,j) E b_(z_j)^2.
```

The regular benchmark has `b_0=1`, `b_z=1/|G|` for `z!=0`, hence
`C=q^(-1)[1+(q-1)/|G|^2]`; polynomial adaptive mode budgets retain vanishing
mass on the factorial schedule. Five globally distinct physical controls
validate both exact formulas: maximum Parseval residual is `1.67e-16`, the
largest W4 single-mode probability is `0.30`, and the largest selected W5
single-mode probability is `0.127`. Seven focused tests pass.

The physical theorem is deliberately still open. Regular first-moment
flatness and finite W4/W5 controls do not prove
`E C_Lambda <= poly(K)/2^K` for globally distinct Plancherel source blocks.
The result therefore neither rejects nor compiles a source-adaptive sparse
router. Dense recoupling, complete orientation polar, classical separation,
algorithm, and speedup gates remain false.

### Refined Next High-Reasoning Task

1. Derive `b_z` as an exact character-convolution expression under independent
   Plancherel source pairs, stratified by `j=|z|`.
2. Compute or bound `E b_(z_j)^2` uniformly in `j`, including rare source
   blocks. Then transfer the independent law to globally distinct sources.
3. A sufficient no-go target is
   `q^(-1) sum_j binom(K,j) E b_(z_j)^2 <= poly(K)/q`.
4. If the bound fails, identify the heavy Hamming strata and source labels;
   then test whether their heavy Walsh modes are computable reversibly from
   the source labels. Collision concentration alone is not a compiler.
5. Do not infer an asymptotic theorem from the finite controls, and do not
   conflate sparse-output rejection with a dense-polar lower bound.

Routine registry, runner, CLI, README, and broad validation are assigned to
Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Native Polar Walsh Output Is Regular-Master Flat (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_regular_master_walsh_flatness_no_go.py
tests/test_self_dual_wreath_regular_master_walsh_flatness_no_go.py
research/representation/self_dual_wreath_regular_master_walsh_flatness_no_go.json
EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-WALSH-FLATNESS-NO-GO
```

For a finite group of order `d`, any target representation of dimension `t`,
and `K` regular source pairs, the branch-resolved invariant projectors `E_e`
have rank `r=t d^(2K-1)`. Their normalized Walsh modes obey exactly

```text
||Ehat_0||F^2 = t d^(2K-2) [1+(d-1)/2^K],
||Ehat_S||F^2 = t d^(2K-2) (d-1)/2^K,  S!=0.
```

The proof uses only the regular character in each source pair. More
importantly, for `R=[E_e]_e`, `F=R*R`, exact polar `Q=R F^(+/2)`, and native
input `rho=F/Tr(F)`, a Walsh transform of the orientation output has

```text
Pr[S]=||Ehat_S||F^2/r.
```

Thus at `d=n!`, `K=ceil(log2 d)+2`, ideal native output is asymptotically
flat over all `2^K` Walsh characters. A fixed set of `m` nonzero modes retains
at most

```text
1/d + (d-1)(m+1)/(d 2^K).
```

Every fixed polynomial mode set and every degree-`K/4` truncation loses
asymptotically all ideal native PGM mass. At `n=128`, the live scaling artifact
gives retained masses about `5.01e-200` for a `K^6` budget and `3.19e-43` for
the degree-`K/4` ball; 90 percent mass requires 90 percent of all modes.
Three exact controls have energy residual below `1.6e-13` and native
probability residual below `7.8e-16`; seven focused tests pass.

Scope is critical. `F=sum_e E_e` is itself only the zero Walsh mode, so this
is not a dense-storage lower bound for the frame. A dense Hadamard is easy.
The theorem rejects fixed sparse/low-degree branch-output truncation, not a
source-label-adaptive sparse set, dense structured recoupling, direct
rectangular CS, or arbitrary circuits. Complete-polar, classical-separation,
algorithm, and speedup gates remain false.

### Refined Next High-Reasoning Task

1. Reduce source-label-adaptive mode selection to the blockwise collision
   `C_Lambda=sum_S p_S(Lambda)^2`. A size-`m` adaptive set has retained mass
   at most `sqrt(m C_Lambda)`.
2. Express `C_Lambda` by Walsh Parseval through scalar orientation
   autocorrelations
   `c_z=q^-1 sum_e Tr(E_e E_(e+z))`, avoiding mode enumeration.
3. Under exchangeable independent Plancherel source pairs, reduce the
   annealed collision to `K+1` Hamming strata. Prove or falsify
   `E C_Lambda=2^(-K+o(K))` from exact character-convolution formulas.
4. Do not infer the asymptotic collision theorem from the nearly flat finite
   W4/W5 controls. If the collision is large, inspect which source labels and
   Hamming strata concentrate it and attempt a reversible adaptive router.
5. Dense structured transforms and the restricted orientation-polar compiler
   remain the positive route regardless of the collision result.

Routine wiring and broad validation are assigned to Gemini 3.6 Flash through
Antigravity.

## Current High-Reasoning Result: Target PGM Escapes Every MRS Transcript Sieve (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_mrs_identification_escape_theorem.py
tests/test_self_dual_wreath_mrs_identification_escape_theorem.py
research/representation/self_dual_wreath_mrs_identification_escape_theorem.json
EXP-CODE-SELF-DUAL-WREATH-MRS-IDENTIFICATION-ESCAPE-THEOREM
```

The separate all-policy transcript-zonotope gate was artificial. The primary
Moore--Russell--Sniady proof gives a statement for each fixed legal hidden
flip, not only for the hidden-label average. For every allowed adaptive sieve
using fewer than `exp(a sqrt(n))` coset states,

```text
TV(P_s,P_0) <= exp(-b sqrt(n))
```

for every hidden bridge `s`, with positive `a,b` below the theorem's
character-bound threshold and sufficiently large `n`. The sieve may choose
pairs from its entire classical history, but every merge measures an isotypic
label and the final answer is a classical transcript postprocessing.

For `M=n!` equiprobable bridges and any randomized transcript decoder
`D(s|t)`, summing the fixed-label TV expectation bounds gives

```text
p_id <= 1/M + M^(-1) sum_s TV(P_s,P_0)
     <= 1/n! + exp(-b sqrt(n)).
```

The physical hidden-bridge PGM has success at least `4/5` with
`K=ceil(log2(n!))+2` copies. Since
`K=Theta(n log n)=exp(o(sqrt(n)))`, this schedule lies below every fixed
positive MRS threshold `exp(a sqrt(n))` eventually. Therefore the target PGM
POVM is asymptotically outside the union of all adaptive MRS transcript
postprocessings. Any uniformly accurate constant-success implementation of
that PGM automatically escapes the MRS class. A separate explicit fixed-
policy zonotope witness is useful geometry but is no longer a prerequisite
for the algorithmic route.

This result relies on the proof's explicit transcript total-variation
conclusion, not the primary theorem statement's ambiguous printed phrase
about success probability. It supplies no explicit MRS constants or finite-n
crossover. It also does not compile the PGM, lower-bound arbitrary quantum
algorithms, prove classical hardness, or permit a speedup claim. Seven focused
tests pass; the exact identification-transfer control saturates its bound and
the generated artifact keeps all implementation and speedup gates false.

### Refined Next High-Reasoning Task

1. Remove all-policy MRS effect separation from the prerequisite list. Do not
   spend high-capability reasoning on enumerating transcript zonotopes unless
   needed to diagnose a concrete proposed circuit.
2. Concentrate the circuit route on the complete natural orientation polar.
   The surviving local question is a direct, normalization-one implementation
   of the restricted child coefficient map/support SELECT, including coherent
   gauges and endpoint rectangular-CS transforms.
3. Derive either a representation-specific recursive compiler using the
   known matrix-POVM/recoupling structure or a no-go that reduces every such
   compiler in the current access model to the unresolved inverse-square-root
   normalization.
4. Test any positive compiler against the existing pair-common-support,
   latent-master tradeoff, source-order gauge, and connected-Clifford no-go
   theorems. Do not reintroduce any of those closed shortcuts under new names.
5. Keep classical separation independent and false. MRS escape only says the
   target measurement is outside one restricted quantum algorithm class.

Routine registry, runner, CLI, README, stale cross-reference, and broad
validation work is assigned to Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Source-Order Sorting Quotients Only A Gauge (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_source_order_gauge_canonicalization.py
tests/test_self_dual_wreath_source_order_gauge_canonicalization.py
research/representation/self_dual_wreath_source_order_gauge_canonicalization.json
EXP-CODE-SELF-DUAL-WREATH-SOURCE-ORDER-GAUGE-CANONICALIZATION
```

The coherent source-block loophole is now reduced exactly. Canonically order
each unequal source pair, let `s_i` record whether the observed ordered block
is reversed, and let `e_i` record which observed member enters the diagonal
invariant. The canonically selected-label pattern is

```text
q=e+s in F_2^K.
```

A branch flip acts by `(s,e)->(s+t,e+t)`, so `q` is invariant. The `2^(2K)`
pairs `(s,e)` split into `2^K` free branch orbits of size `2^K`, with one
orbit for each `q`. Reversible partition comparison, controlled carrier
swaps, and XOR updates compile

```text
(s,e)->(0,q)
```

while retaining `s` as a reversible gauge record.

The exact leaf-rank identity is

```text
rank(E_e^(s Lambda))=rank(E_q^(Lambda_canonical)).
```

Thus sorting makes all order gauges agree but preserves the full selected-
pattern frame. Branch shifts and branch Fourier transforms act only inside a
fixed `q` orbit and cannot normalize across `q`. In the `S_6` control, the 16
selected patterns retain five distinct leaf ranks from zero to `2025`.

Four controls have zero order-gauge rank residual, zero orbit-invariance
residual, and nonuniform selected-pattern rank profiles. Seven focused tests
pass.

This is a positive polynomial gauge compiler but not a polar compiler. It is
consistent with the connected-Clifford theorem: quotienting redundant branch
order does not implement the remaining rectangular CS transform. Keep direct
matrix selected-pattern transforms open and every complete-polar, decoder,
classical-separation, algorithm, and speedup gate false.

### Refined Next High-Reasoning Task

1. Stop revisiting pair transport, source-order sorting, branch Hadamards, or
   ordinary connected-group Fourier labels as complete-polar shortcuts. Their
   exact scope is now closed.
2. For the circuit route, the only local survivor is the existing matrix-POVM
   recursive compiler: derive direct structured square-root/support SELECT or
   prove a natural state-weighted trim. Generic graph, pair, and gauge access
   no longer help.
3. In parallel, return to the independent necessity gate: positive natural
   component commutator/MRS separation. The current exact reduction is the
   growing mixed marked-word functional in the Green kernel.
4. Spend high-reasoning effort on a new target-survival or cancellation
   theorem, not more finite wiring. Use the existing pressure/topology modules
   and preserve their fixed-word versus growing-degree boundaries.
5. Any promising component signal must still be attacked by transcript-cone
   or classical simulation checks before promotion.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Branch Covariance Crosses Source Blocks And Gives No Fixed-Block Hadamard (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_source_block_branch_covariance_boundary.py
tests/test_self_dual_wreath_source_block_branch_covariance_boundary.py
research/representation/self_dual_wreath_source_block_branch_covariance_boundary.json
EXP-CODE-SELF-DUAL-WREATH-SOURCE-BLOCK-BRANCH-COVARIANCE-BOUNDARY
```

A tempting all-depth shortcut has been rejected with the correct covariance
scope. For an ordered source tuple `Lambda`, orientation `e`, and branch flip
`t`, canonical carrier-factor swaps give

```text
U_t E_e^Lambda U_t* = E_(e+t)^(t Lambda),
```

where `t Lambda` swaps the ordered source labels in every selected pair. This
is an exact unitary between different Fourier source blocks. It is not an
internal unitary from `E_e^Lambda` to `E_(e+t)^Lambda`.

Every nonzero branch flip changes an ordered tuple of unequal source pairs;
the branch stabilizer is trivial. Independent Plancherel sampling is invariant
under these swaps, but that gives equality in distribution, not blockwise
short-metric equality or a coherent Hadamard endpoint mixer after the source
block is fixed.

Four physical controls have zero cross-block covariance rank mismatches and a
within-block sibling rank mismatch. In the matrix partial-support `S_6` node,
the affine translation pairs leaf ranks

```text
(225,125) with (225,2025),
```

so the child leaf-coefficient dimensions are `350` and `2250`; the maximum
paired mismatch is `1900`. Seven focused tests pass.

This does not reject an induced orbit transform that coherently carries all
swapped source blocks. The connected-Clifford normal form already shows that
such an orbit transform still faces the rectangular fixed-space CS polar.
Keep matrix child POVM dilation and direct CS transforms open, and every
complete-polar, decoder, classical-separation, algorithm, and speedup gate
false.

### Refined Next High-Reasoning Task

1. Analyze coherent source-pair sorting. Define the source-order bit `s_i` and
   selected-label bit `z_i=e_i+s_i`; prove which combination is branch-gauge
   invariant and how leaf ranks depend on it.
2. Determine whether sorting merely canonicalizes `s` while leaving the hard
   `z`-indexed orientation frame unchanged. If so, close the coherent orbit-
   sorting shortcut without claiming arbitrary-circuit hardness.
3. Reconcile the result explicitly with the syndrome-component and connected-
   Clifford theorems; do not create a second independent component label.
4. If a nontrivial coherent transform does act on `z`, exhibit it on the S6
   rank-mismatched control before proposing an all-n endpoint mixer.
5. Otherwise return to the matrix child-POVM effect dilation or the natural
   component-commutator/MRS separation gate; pair and source-order symmetries
   are exhausted.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Exact Pair Relations Equal Literal Common Support (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_pair_relation_common_support_no_go.py
tests/test_self_dual_wreath_pair_relation_common_support_no_go.py
research/representation/self_dual_wreath_pair_relation_common_support_no_go.json
EXP-CODE-SELF-DUAL-WREATH-PAIR-RELATION-COMMON-SUPPORT-NO-GO
```

The operator-metric extension of the pair sheaf is now closed. Let
`B_v=E_vF^(+/2)` be the canonical coordinate maps. For the most general exact
two-vertex linear relation

```text
R_uB_u+R_vB_v=0,
```

put `T=R_uB_u=-R_vB_v`. Then

```text
Ran(T*) subset Ran(B_u*) intersect Ran(B_v*).
```

Since `F^(+/2)` is invertible on the frame support,

```text
Ran(B_v*)=F^(+/2)Ran(E_v),
dim(Ran(B_u*) intersect Ran(B_v*))
 =dim(Ran(E_u) intersect Ran(E_v)).
```

The rank bound is tight: pseudoinverse lifts of an orthonormal common-space
basis make both endpoint images equal to that basis. Therefore the maximum
rank of any exact pair relation is exactly the principal-angle-one
multiplicity. Arbitrary positive/operator endpoint weights cannot extend a
pair relation into any noncommon principal-angle channel.

This does not contradict pair GPE. Pair GPE transports a carrier between two
local subspaces; it does not make the two canonical global-polar coordinates
equal. Nor does it reject recursive child relations: those are higher-arity
relations between aggregate child syntheses, not original two-leaf relations.

Three physical noncommon controls leave all nine active channels uncovered;
one common control attains the exact rank-one relation. The constructed
maximal relation residual is at most `6.68e-16`, with zero rank-identity
residual. Seven focused tests pass.

Pair-only sheaves are now closed, including operator-valued pair metrics.
Keep genuinely higher-arity hierarchical cokernel relations and direct
rectangular CS transforms open. Every complete-polar, decoder, classical-
separation, algorithm, and speedup gate remains false.

### Refined Next High-Reasoning Task

1. Reuse, do not duplicate, `self_dual_wreath_hierarchical_cokernel_resolution.py`
   and `self_dual_wreath_gpe_recursive_node_compiler.py`. They already prove
   information-theoretic completeness of aggregate-child relations and give
   the exact normalized parent relation.
2. Reassess the physical sibling symmetry at each affine split. Determine
   whether the two shorted metrics are equal, efficiently unitarily conjugate,
   or merely isospectral. Equality gives a Hadamard endpoint mixer; known
   conjugacy plus coherent carrier access may give a direct matrix mixer.
3. If natural sibling metrics can be exponentially imbalanced despite branch
   symmetry, produce an explicit physical family rather than reusing the
   abstract repeated-line counterexample.
4. Prove whether recursive normalized child embeddings plus endpoint mixers
   compose to the same rectangular CS polar and output gauge identified by the
   homogeneous-space theorem. Do not accept kernel completeness alone.
5. Reserve a sparse higher-arity parity-check route only if its SELECT and gap
   can be proved on natural occupied mass; abstract exactness is already known.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Latent Master Fibers Conserve Generic Polar Normalization Cost (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_latent_master_polar_tradeoff.py
tests/test_self_dual_wreath_latent_master_polar_tradeoff.py
research/representation/self_dual_wreath_latent_master_polar_tradeoff.json
EXP-CODE-SELF-DUAL-WREATH-LATENT-MASTER-POLAR-TRADEOFF
```

The obvious latent-master repair of the failed pair sheaf is now resolved in
the normalized-analyzer access model. Put

```text
C=stack_v(E_v)/sqrt(m),  X=C*C=F/m,
G_(a,b)=[aI; bC].
```

On `supp(F)`, the graph polar and its orientation-branch probability are

```text
polar(G)=G(a^2I+b^2X)^(-1/2),
p(x)=b^2x/(a^2+b^2x).
```

The master identity can regularize the graph, but recovering the desired
orientation polar on a superposition of `X` eigenspaces requires spectral
gain

```text
q_flat(x)=sqrt(a^2+b^2x)/(b sqrt(x)).
```

For the flagged access normalization `alpha=sqrt(a^2+b^2)`, at the smallest
occupied eigenvalue `x_min`,

```text
q_graph q_flat
 = alpha/(b sqrt(x_min))
 >= 1/sqrt(x_min).
```

Thus `a=0` puts all cost in polarizing `C`; large `a` makes the graph polar
easy but moves the same cost into spectral flattening/postselection. No master
weight improves the generic inverse-singular exponent. Merely postselecting
the orientation flag is invalid on spectral superpositions because `p(x)` is
not constant.

Nine physical controls pass with maximum graph-polar residual `1.98e-15`,
flattened-polar residual `2.40e-15`, and product-identity residual `8.89e-16`.
The minimum combined/direct scale ratio is exactly one. Seven focused tests
pass.

This is an access-model theorem, not arbitrary-circuit hardness. Pair GPE is
already a local representation-specific bypass. Keep a direct rectangular CS
transform and other non-black-box use of the group action open. The factorial
flat scaling rows are benchmarks, not a newly proved natural `x_min` law.
Keep every complete-polar, decoder, classical-separation, algorithm, and
speedup gate false.

### Refined Next High-Reasoning Task

1. Prove the general pair-relation rank theorem. For canonical coordinate
   maps `B_v=E_vF^(+/2)`, show any exact two-vertex relation
   `R_uB_u+R_vB_v=0` has rank at most
   `dim(Ran(E_u) intersect Ran(E_v))`; hence operator-valued metrics cannot
   recover noncommon principal-angle channels either.
2. Quantify the common-channel pair-relation rank on physical controls and
   compare it to the full dependency codimension. If common channels do not
   span the dependency space, stop pursuing all pair-only sheaves.
3. Recast the surviving target as a sparse, coherently selectable higher-arity
   parity-check/preconditioner `D` with `ker D=Ran(stack E_v)`, inverse-
   polynomial nonzero singular gap, and normalization-one access.
4. Determine whether any such `D` derived from fusion-tree associativity has
   local arity and polynomial degree, or whether constructing it is equivalent
   to the original rectangular CS polar.
5. Continue to reserve direct representation-specific transforms; the graph
   theorem does not reject them.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: Noncommon Pair-GPE Edges Cannot Form The Unweighted Polar Sheaf (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_pair_sheaf_metric_incompatibility.py
tests/test_self_dual_wreath_pair_sheaf_metric_incompatibility.py
research/representation/self_dual_wreath_pair_sheaf_metric_incompatibility.json
EXP-CODE-SELF-DUAL-WREATH-PAIR-SHEAF-METRIC-INCOMPATIBILITY
```

The current partial-holonomy sheaf has been tested against the actual target,
not merely against abstract noncommuting POVMs. Let `E_v` be the orientation
projectors, `F=sum_v E_v`, and

```text
W_v=E_v F^(+/2)
```

the coordinate maps of the canonical global analysis polar. For a pair edge,
put

```text
U=polar(E_vE_u),  P=U*U,  Q=UU*.
```

The unweighted sheaf equation `Q x_v=U P x_u` can hold on the canonical polar
range only if its two endpoint Gram operators agree. Exactly,

```text
W_u* P W_u = W_v* Q W_v
iff F^(+/2)(P-Q)F^(+/2)=0
iff P=Q.
```

The final equivalence uses that `F^(+/2)` is injective on `supp(F)` and both
edge supports lie there. Thus only literal common channels are compatible.
Every noncommon principal-angle channel has `P!=Q`, including the exact
inverse-dimension channels for which pair GPE gives a polynomial direct polar.
Pair GPE aligns their principal vectors but cannot glue their global-polar
coordinate amplitudes by equality.

The obstruction survives arbitrary vertex-local output gauges: the local
isometries cancel from the pulled-back endpoint metrics. It also precedes any
gap question. A perfect coherent SELECT and an inverse-polynomial sheaf gap
would efficiently project onto the wrong section space.

Physical controls at correlations `1/2`, `1/3`, and `1/4` have endpoint metric
obstruction `1` and canonical section residual `sqrt(2)`; a genuine common
channel has zero residual. All four controls verify the exact metric identity
to at most `1.04e-15`. Seven focused tests pass; the joint newest suite has 14
passing tests.

This is a restricted architecture no-go, not an all-holonomy lower bound.
Operator-valued endpoint metrics, latent master fibers, higher-arity
relations, and a direct rectangular CS transform remain open. Keep every
complete-polar, decoder, classical-separation, algorithm, and speedup gate
false.

### Refined Next High-Reasoning Task

1. Analyze the latent-master incidence exactly. For
   `G_a=[aI; (b/sqrt(m)) stack_v(E_v)]`, derive its polar, condition number,
   output probability, and the minimum amplitude amplification cost required
   to recover `stack_v(E_v)F^(+/2)`.
2. Test whether any choice of `a,b` gives both constant-conditioned graph
   preparation and constant native output probability. Prove the tradeoff or
   exhibit a normalization-one bypass.
3. Formulate the most general operator-metric edge relation compatible with
   the canonical coordinate effects. Determine whether its positive endpoint
   factors are exactly another representation of `F^(+/2)`; if so, close that
   weighted local architecture as circular.
4. Leave higher-arity relations open unless their incidence can be block-
   encoded without a normalization or postselection cost exponential in
   `log|S_n|`.
5. Do not spend high-capability time proving a gap for the rejected unweighted
   pair connection.

Routine wiring is assigned to Gemini 3.6 Flash through Antigravity.

## Previous High-Reasoning Result: GPE Fusion Trees Compile Full Recoupling, Not The Rectangular CS Polar (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_gpe_fusion_tree_cs_boundary.py
tests/test_self_dual_wreath_gpe_fusion_tree_cs_boundary.py
research/representation/self_dual_wreath_gpe_fusion_tree_cs_boundary.json
EXP-CODE-SELF-DUAL-WREATH-GPE-FUSION-TREE-CS-BOUNDARY
```

Coherent generalized phase estimation is stronger than weak Fourier sampling
in the relevant sense. Given an efficient group QFT and controlled factor
actions, it exports an irrep/carrier row while preserving opaque multiplicity.
Repeating this operation along a binary association tree compiles a coherent
fusion-tree transform with one GPE call per internal node. Uncomputing one
tree and computing another therefore compiles the full Racah recoupling
unitary without naming a classical multiplicity basis.

This does not compile the orientation polar. If `U_T` is the full tree-change
unitary and `P,Q` select the branch-fixed and diagonal-fixed labels, the
physical overlap is the rectangular subblock

```text
C = Q U_T P.
```

The decoder needs `polar(C)`, not `U_T`. Pre- and post-composition by fusion-
tree unitaries preserves the singular values of `C`; it cannot turn a
non-isometric subblock into its polar. Pair GPE is the exceptional direct
case because every active pair block is `cU` with one scalar singular level
and a known reassociation `U`. The first two-pair `S_3` control already has
five active singular values on three levels, from `sqrt(1/8)` to
`sqrt(3/8)`. Its minimum one-crossing unitary-only distance to the polar is
`1-1/sqrt(2)=0.292893...`.

The exact finite identity

```text
polar(C) = stack_e(E_e) [sum_e E_e]^(+/2)
```

passes on all three controls. Two controls have scalar active spectra and one
is genuinely matrix-valued. Seven focused tests pass. Keep direct global
rectangular-CS polar, complete orientation polar, classical separation,
algorithm, and speedup gates false.

This is not an arbitrary-circuit lower bound. A GPE-derived direct CS basis,
a structured singular-vector pairing, or a partial-support holonomy/F-move
network may still implement the polar without generic inverse-angle
amplification.

### Refined Next High-Reasoning Task

1. Characterize products of exact pair-GPE polar transports on the induced
   branch carrier. Derive a necessary and sufficient flatness/holonomy
   condition for the product to equal the global rectangular-subblock polar,
   including the output gauge.
2. Reuse the existing partial-holonomy/sheaf and holonomy-resolver reductions;
   do not duplicate finite path enumeration. Determine whether their kernel
   projector is exactly the CS singular-vector pairing or merely another
   normalized frame requiring `F^(+/2)`.
3. Search for a polynomial natural generator set and an inverse-polynomial
   gap only after proving the target fixed space equals the global polar
   range. A gap for the wrong flat connection is not progress.
4. Audit self-conjugate split `A_n` sectors separately. The current fusion-
   tree boundary does not prove their natural mass negligible.
5. If every pair-transport/sheaf construction algebraically recreates the
   same frame inverse square root, close that restricted architecture and
   redirect high-reasoning effort to another nonabelian mechanism.

Routine registry/runner/CLI/README wiring is assigned to Gemini 3.6 Flash
through Antigravity in `research/MECHANICAL_FOLLOW_UP_PLAN.md`.

## Current High-Reasoning Result: Ordinary Connected-Group Clifford QFT Reconstructs The Original CS Gate (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_connected_clifford_normal_form.py
tests/test_self_dual_wreath_connected_clifford_normal_form.py
research/representation/self_dual_wreath_connected_clifford_normal_form.json
EXP-CODE-SELF-DUAL-WREATH-CONNECTED-CLIFFORD-NORMAL-FORM
```

The full connected-group Clifford-theory shortcut is now resolved in the
generic nonsplit orbit. Assume the `A_n^(2K+1)` coordinate constituents are
not self-conjugate and are distinct up to odd conjugation. Their inertia group
in `L` is

```text
H=A_n^(2K+1) semidirect C,
```

where `C` is the orientation sign code. The branch group acts freely, so the
corresponding Clifford carrier is

```text
Ind_H^L(alpha_tilde)=direct_sum_(e in B) V_alpha.
```

In this basis, `B` is regular translation and

```text
Fix_B={|+_B> tensor v : v in V_alpha}.
```

The zero diagonal `D` lies in the inertia group. On branch `e`, it acts as the
conjugate orientation diagonal `H_e`; if `E_e` is its invariant projector,

```text
P_D=direct_sum_e E_e,
Fix_D=direct_sum_e |e> tensor Ran(E_e).
```

For the uniform branch embedding `S_B`, the fixed-space CS problem is exactly

```text
S_B* P_D S_B = (1/2^K) sum_e E_e = F/2^K,
polar(P_D S_B) = stack_e E_e F^(+/2).
```

The second expression is the complete orientation analysis polar. Therefore
an ordinary coherent `L` QFT/Clifford transform that exposes orbit,
stabilizer, and subgroup-fixed labels has only reconstructed the original
matrix CS gate. It has not normalized it. The explicit uniform branch orbit
retains the inverse-width factor.

This is not an arbitrary-circuit lower bound. A connected-group transform
augmented with the actual fixed-space CS SVD would solve the gate by
definition, and a direct GPE/holonomy factorization may avoid conventional
Clifford labels. Self-conjugate split `A_n` sectors also remain unresolved;
the theorem does not assume their natural mass vanishes.

Three physical controls pass with zero failures. The cross Gram residual is at
most `1.12e-16`, the cross-polar/orientation-polar residual at most `3.14e-15`,
and all three normalized overlaps are non-isometric. The two-pair `S_3`
control has three positive cross-Gram levels from `1/8` to `3/8`. Seven
focused tests, syntax, and diff checks pass. Keep ordinary Clifford CS
compiler, direct matrix CS polar, complete orientation polar, classical
separation, algorithm, and speedup gates false.

### Refined Next High-Reasoning Task

1. Stop treating completion of an ordinary `L` QFT as progress unless it
   includes a normalization-one implementation of `polar(P_D S_B)`.
2. Attack the direct many-way `A_n`/`S_n` subduction polar. Try recursive GPE
   fusion trees as physical isometries, not as labels; prove whether their
   composition implements the CS SVD or just alternating projections.
3. Formulate the holonomy network on the induced branch carrier. Pair-GPE
   gives exact edge partial isometries; derive a polynomial generator set,
   active coverage, path independence or correctable loop gauge, and equality
   with the global polar.
4. Audit split self-conjugate sectors separately. They may alter inertia
   groups and cocycles, but cannot be discarded without a natural-mass theorem.
5. If GPE fusion and holonomy both reduce algebraically to `F^(+/2)`, record a
   restricted-architecture no-go and redirect to another nonabelian mechanism
   rather than generating more group-QFT labels.

Routine wiring remains queued for Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Connected Parity Quotient Solved, Alternating Recoupling Remains (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_connected_quotient_heisenberg_reduction.py
tests/test_self_dual_wreath_connected_quotient_heisenberg_reduction.py
research/representation/self_dual_wreath_connected_quotient_heisenberg_reduction.json
EXP-CODE-SELF-DUAL-WREATH-CONNECTED-QUOTIENT-HEISENBERG-REDUCTION
```

After syndrome canonicalization, put `A=A_n^(2K+1)` inside the connected group
`L=<B,D>`. The quotient `P_K=L/A` has generators `a` (the zero-orientation
sign), branch swaps `b_i`, and central pair signs `c_i`, with

```text
a^2=b_i^2=c_i^2=1,
[a,b_i]=c_i,
[b_i,b_j]=1,
all c_i central.
```

Therefore

```text
|P_K|=2^(2K+1),
Z(P_K)=[P_K,P_K]=<c_1,...,c_K> ~= C_2^K,
P_K/[P_K,P_K] ~= C_2^(K+1).
```

This class-two multi-center Heisenberg/dihedral quotient has a complete irrep
classification:

```text
2^(K+1) one-dimensional irreps,
(2^K-1)2^(K-1) two-dimensional irreps,
no larger irreps.
```

For each nonzero central character `theta`, the commutator form has rank two
and a `(K-1)`-dimensional radical; radical characters index the
`2^(K-1)` two-dimensional blocks. The square sum is exactly `|P_K|`.
Consequently the entire parity/branch quotient QFT is polynomial via binary
linear algebra and one-qubit Pauli/Hadamard blocks. It is not the missing
high-rank transform.

The native homogeneous theorem puts nearly all frame mass in occupied CS
blocks of rank at least `|S_n|^(K/4)`, while every `P_K` carrier has dimension
at most two. Thus the residual multiplicity necessarily sits in the
`A_n^(2K+1)` orbit/stabilizer and many-way subduction spaces. This localizes
the compiler gate but does not prove hardness. Non-self-conjugate `S_n`
partitions restrict irreducibly to `A_n` up to extension gauge;
self-conjugate partitions split and their constituents are exchanged by odd
conjugation. A coherent Clifford-theory transform for the full `L` may still
exist.

Exact controls for `K=1..4` have zero failures; the largest checked quotient
has order 512, center/derived order 16, 32 one-dimensional and 120
two-dimensional irreps, 152 conjugacy classes, and exact square sum 512.
Seven focused tests, syntax, and diff checks pass. Keep full `L` Clifford
transform, alternating subduction polar, complete orientation polar,
classical separation, algorithm, and speedup gates false.

### Refined Next High-Reasoning Task

1. Build the Clifford-theory normal form for `L=A_n^(2K+1) semidirect P_K`.
   Start with collision-free non-self-conjugate source labels, where branch
   swaps have free coordinate orbits and odd signs change extension gauges.
2. Derive the stabilizer cocycle and a coherent orbit basis. Determine whether
   its F-moves are only binary-linear/Pauli operations or whether many-way
   `A_n` Kronecker multiplicity reappears explicitly.
3. Add self-conjugate split sectors rather than assuming them negligible; no
   all-natural absence theorem is available.
4. Test whether the full `L` QFT plus fixed-space marking yields the CS polar
   at normalization one. Merely exposing irrep/stabilizer labels is not enough.
5. If Clifford theory only repackages equation `CC*`, prove the equivalence and
   stop treating group-QFT completion as progress. Return to a direct
   alternating-subduction polar or GPE holonomy network.

Routine wiring remains queued for Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Complete Polar Reduces To One Syndrome Component (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_orientation_syndrome_component_reduction.py
tests/test_self_dual_wreath_orientation_syndrome_component_reduction.py
research/representation/self_dual_wreath_orientation_syndrome_component_reduction.json
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SYNDROME-COMPONENT-REDUCTION
```

The homogeneous incidence has an exact `K`-bit conserved charge. For
`gamma=(t,x_1,y_1,...,x_K,y_K)`, define

```text
z_i(gamma)=sgn(t)+sgn(x_i)+sgn(y_i) mod 2.
```

Pair swaps preserve this vector, so `z:Omega->F_2^K` is a homomorphism. Both
the branch subgroup `B` and zero-orientation diagonal `D` lie in its kernel.
For `n>=5`, the affine generated-subgroup theorem plus `B` conjugacy gives

```text
L=<B,D>=ker(z),
|L|=|S_n|^(2K+1),
[Omega:L]=2^K.
```

The connected components of the `Omega/D` to `Omega/B` incidence are the
right `L` cosets. Consequently

```text
T ~= I_(2^K) tensor T_0,
polar(T) ~= I_(2^K) tensor polar(T_0),
T_0: L/D -> L/B.
```

The zero-component source and physical dimensions are
`|S_n|^(2K)` and `|S_n|^(2K+1)/2^K`. The syndrome is polynomially computable
from permutation parity. A transposition in the first coordinate of pair `i`
represents syndrome bit `i`; controlled multiplication maps every component
coherently to syndrome zero. Therefore the apparent `2^K` replicated
component cost is not an independent compiler barrier. Future work only needs
one connected `L/D -> L/B` CS polar.

This does not solve normalization. Branch-controlled translations, syndrome
Fourier transforms, and all other pre/post unitaries preserve the singular
values of `T_0/sqrt(2^K)`. They cannot turn it into a partial isometry. The
three finite controls remain at least `0.292893` away from their component
polar under any unitary-only correction; the nonabelian `S_3` control has
normalized singular values from `1/2` to `1`. In the natural flat benchmark
the amplitude is `Theta(|S_n|^-1/2)`.

The syndrome is a conserved gauge/component label, not hidden-permutation
information. Three exact controls have zero generated-kernel mismatch, zero
off-syndrome incidence, zero canonicalization failures, and component-spectrum
residual at most `4.45e-16`. Seven focused tests, syntax, and diff checks pass.
Keep connected-component CS polar, complete orientation polar, classical
separation, algorithm, and speedup gates false.

### Refined Next High-Reasoning Task

1. Replace `Omega` by the connected group `L=ker(z)` in the fixed-space
   recoupling analysis. Derive irreps or an efficient subgroup-chain transform
   for `L=N semidirect B`, where `N` is the parity-code preimage containing
   `A_n^(2K+1)`.
2. Determine whether the `L` Fourier transform exposes a smaller multiplicity
   algebra than the `Omega` fixed-space CS blocks. A global QFT alone is not
   enough; the test is a normalization-one polar in the physical `B` gauge.
3. Formulate and test global GPE row relocation inside the zero-syndrome block.
   Syndrome translations may be used only for canonicalization, not counted as
   progress on singular-value normalization.
4. Prove or kill a polynomial holonomy/F-move network on the connected block.
   Pair-GPE edges are available, but active coverage and higher-order gauge
   consistency remain mandatory.
5. If `L` recoupling is no simpler, record the exact equivalence and return to
   a direct many-way Kronecker CS transform. Do not infer arbitrary-circuit
   hardness from connectedness, huge rank, or worst-case Kronecker results.

Routine wiring remains queued for Gemini 3.6 Flash through Antigravity.

## Current High-Reasoning Result: Fixed Spaces Explicit, Global Kronecker CS Polar Open (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_orientation_fixed_space_recoupling.py
tests/test_self_dual_wreath_orientation_fixed_space_recoupling.py
research/representation/self_dual_wreath_orientation_fixed_space_recoupling.json
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FIXED-SPACE-RECOUPLING
```

The two fixed spaces in the homogeneous orientation polar are now explicit in
one common local gauge. For

```text
Omega = G x (((G x G) semidirect C_2)^K), G=S_n,
rho = tau tensor zeta_1 tensor ... tensor zeta_K,
```

irreps of a local two-factor wreath group have two forms. If `lambda!=mu`,
the induced carrier is

```text
(V_lambda tensor V_mu) direct_sum (V_mu tensor V_lambda),
```

its swap-fixed space is one `V_lambda tensor V_mu`, and its restriction to
the selected first `G` coordinate is

```text
d_mu V_lambda direct_sum d_lambda V_mu.
```

For equal `lambda` and extension sign `sigma`, the swap-fixed space is
`Sym^2(V_lambda)` for `sigma=+1` and `wedge^2(V_lambda)` for `sigma=-1`; the
selected restriction is `d_lambda V_lambda`. Therefore

```text
Fix_B(rho) = V_tau tensor_i Fix_C2(zeta_i),
Fix_D(rho) = Inv_G(V_tau tensor_i Res_selected(zeta_i)).
```

The `B`-fixed basis is polynomially coherent. Unequal blocks need one branch
Hadamard and controlled tensor swap. Equal blocks use a reversible index
comparison and symmetric/exterior pair basis. This local basis is not the
bottleneck.

Compressing selected-coordinate action to that basis gives

```text
K_(lambda,mu)(s)
  = [rho_lambda(s) tensor I + I tensor rho_mu(s)]/2,
CC* = |G|^-1 sum_s rho_tau(s) tensor_i K_i(s).
```

The equal-label formula is the same half-sum restricted to the symmetric or
exterior square. The second identity is exactly the orientation Fourier frame
in the flattened `B`-fixed gauge. Thus the remaining operation is sharply
identified as the polar of a high-rank, many-way symmetric-group Kronecker
subduction kernel.

Coherent GPE can mark `Fix_D`, and the companion pair-GPE theorem implements a
single canonical carrier reassociation while preserving opaque multiplicity.
Neither supplies the global matrix CS polar: their direct composition retains
the inverse-square-root-width principal angles. Two exact global `S_3`
controls have respectively three and two distinct positive principal-cosine
levels inside one outer-label block (`1/4` through `1/2`). This directly
falsifies scalar outer-label filtering and automatic composition of pair
carrier swaps.

The May 2026 semisimple-algebra QFT does not currently close this gate. Its
proved unitary approximation has error `(d^-1/2+epsilon)poly(|A|)`, while the
natural diagram order is `Theta(K)=Theta(n log n)`, the loop parameter is only
`d=n`, and the factors are arbitrary Plancherel `S_n` irreps rather than one
fixed low tensor power of the permutation module. This is an applicability
failure, not a hardness theorem.

Six local controls and two global controls pass with zero failures. Maximum
local compression residual is `2.60e-16`; maximum global kernel residual is
`2.22e-16`. Both global controls are matrix-valued. Seven focused tests,
syntax, and diff checks pass. Keep global CS compiler, complete orientation
polar, classical separation, algorithm, and speedup gates false.

### Refined Next High-Reasoning Task

1. Formulate a global GPE row-relocation ansatz for the matrix kernel `CC*`.
   It must act on the full many-way invariant multiplicity coherently and end
   in the explicit physical `B`-fixed gauge.
2. Determine whether recursive GPE fusion trees provide a direct CS basis
   change or merely alternate two projectors at principal angle `Theta(g^-1/2)`.
   A positive theorem needs normalization one; a negative theorem must state
   the restricted circuit/oracle model.
3. Search the subgroup chain generated by `B` and `D` for a multiplicity-space
   Fourier transform, association scheme, or partition/centralizer algebra
   whose F-moves are polynomial at `K=Theta(n log n)`. Reject fixed-degree or
   large-loop results that do not reach this regime.
4. Try to express the CS polar as a product of direct pair-GPE reassociations
   plus a polynomial set of holonomy corrections. Prove active coverage and
   gauge consistency; finite path connectivity is insufficient.
5. If all such direct transforms fail, derive a natural-mass obstruction for
   the restricted GPE/local-swap architecture. Do not promote worst-case
   Kronecker hardness or huge rank to an arbitrary-circuit lower bound.

Routine registry, runner, CLI, README, ledger, and broad validation remains a
Gemini 3.6 Flash/Antigravity task.

## Current High-Reasoning Result: One Homogeneous-Space Polar Replaces The Orientation List (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_orientation_homogeneous_space_polar.py
tests/test_self_dual_wreath_orientation_homogeneous_space_polar.py
research/representation/self_dual_wreath_orientation_homogeneous_space_polar.json
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-HOMOGENEOUS-SPACE-POLAR
```

The complete regular-master orientation polar now has one exact global group
model. Put `G=S_n`, `Gamma=G^(2K+1)`, let `B=C_2^K` swap the two entries in
each source pair, and form

```text
Omega = Gamma semidirect B
      = G x (((G x G) semidirect C_2)^K).
```

Let `D` be the zero-orientation diagonal copy of `G`, acting on the target and
the zero-selected coordinate of every pair. Conjugating `D` by the branch
group gives every orientation subgroup `H_e`. There are canonical quotient
identifications

```text
Omega/D = disjoint_union_e Gamma/H_e,
Omega/B = Gamma.
```

For normalized right-coset embeddings `J_D,J_B` into `C[Omega]`, the full
orientation synthesis is exactly

```text
T = sqrt(2^K) J_B* J_D,
TT* = 2^K J_B* P_D J_B,
T*T = 2^K J_D* P_B J_D.
```

Thus every natural orientation polar is one Fourier block of the polar of
this single homogeneous-space incidence. This is the first exact flattened
representation-specific target that does not describe the compiler as an
explicit factorial list or a recursively nested black-box QSVT.

The `Omega` Fourier transform only removes the outer row action. In each
irrep `rho`, the remaining block is the matrix overlap

```text
sqrt(2^K) [Fix_D(rho) -> Fix_B(rho)],
```

and the required operation is its Cosine-Sine/subduction polar. It is not a
scalar spherical filter. With `g=n!`, `p=p(n)`, and
`I_n=sum_lambda d_lambda` equal to the number of involutions in `S_n`, exact
dimension formulas are

```text
#Irr(Omega) = p [p(p+3)/2]^K,
#(B\Omega/B) = g [(g^2+g)/2]^K,
sum_rho d_rho = I_n (I_n^2+g)^K.
```

For `m_B(rho)=dim Fix_B(rho)`, the physical quotient dimension fraction in
blocks with `m_B<=L` is at most

```text
L I_n (I_n^2+g)^K / g^(2K+1).
```

The source quotient has the same numerator and denominator `2^K g^(2K)`.
At `K=ceil(log2 g)+2` and `L=g^(K/4)`, both bounds are already below `2^-24`
at `n=5` and then fall rapidly; the `n=128` physical log2 bound is below
`-367720`. Therefore low multiplicity and scalar outer-label filtering are
not the typical uniform-dimension regime on either quotient.

Uniform dimension alone is not the native frame law, but the exact incidence
moments close that gap at the regular-master level. For `F=TT*`,

```text
Tr(F)   = (2^K/g) dim(C[Gamma]),
Tr(F^2) = [1+(2^K-1)/g] Tr(F).
```

If `r_rho` is the occupied CS rank in block `rho`, blocks with `r_rho<=R`
have total ambient rank at most `R sum_rho d_rho`. Hilbert--Schmidt
Cauchy--Schwarz bounds their native frame mass by

```text
sqrt((gamma/c) R I_n(I_n^2+g)^K/g^(2K+1)),
c=2^K/g, gamma=1+(2^K-1)/g.
```

At `R=g^(K/4)` this is negligible. The weakest recorded high-rank native-mass
lower bound is `0.999752`. Therefore low occupied overlap rank is no longer a
viable typical-native escape. A stronger conditioned per-sector
central-support transfer is not proved.

This is still not a hardness theorem. Huge occupied QFT multiplicity can have
a succinct basis and fast transform. Generic alternating reflections still
see the inverse-factorial principal-angle normalization, while a direct
fixed-space CS transform could bypass that boundary.

Three exact controls (`S_2,K=1`, `S_2,K=2`, `S_3,K=1`) have zero incidence
and equivariance residual. The largest polar-support residual is `9.24e-15`
and the largest frame-moment residual is `7.11e-14`. Seven focused tests pass;
syntax and diff checks pass. Native regular-master huge occupied rank is true.
Keep conditioned physical-sector rank transfer, normalized CS compiler,
complete orientation polar, classical separation, MRS escape, algorithm, and
speedup gates false.

### Refined Next High-Reasoning Task

1. Write an explicit coherent basis for `Fix_B(rho)`. This side factors over
   the `K` local two-factor wreath irreps: unequal labels give one swap-fixed
   copy of `V_lambda tensor V_mu`, while equal labels give symmetric or
   exterior squares.
2. Express `Fix_D(rho)` in the same basis. Restriction to the selected source
   coordinate produces a many-way diagonal `S_n` invariant/Kronecker space.
3. Search for a subgroup-chain or partition-algebra factorization of the
   fixed-space CS polar whose query count is polynomial and whose output gauge
   is the physical `B`-fixed basis. Kill the route if unrestricted Kronecker
   subduction reappears on constant native mass without a succinct transform.
4. Decide whether an annealed native-mass compiler is sufficient for the PGM
   error budget or whether a conditioned central-support theorem is needed.
   Do not reopen occupied-rank work unless the circuit requires per-sector
   guarantees.
5. If a direct CS transform is found, compose it with the already compiled
   physical PGM row-copy. Do not create a separate decoder project.

Routine registry, runner, CLI, README, ledger, and broad test wiring belongs
to Gemini 3.6 Flash through Antigravity and is specified in the mechanical
plan.

## Current High-Reasoning Result: Complete Polar Already Closes The Physical Decoder (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_component_polar_physical_pgm_closure.py
tests/test_self_dual_wreath_component_polar_physical_pgm_closure.py
research/representation/self_dual_wreath_component_polar_physical_pgm_closure.json
EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POLAR-PHYSICAL-PGM-CLOSURE
```

This theorem removes another redundant research gate. For the complete
orientation analysis `R`, `S=R*R`, polar `Q=RS^(+/2)`, and generalized Fourier
row-copy isometry `C_U`, the exact physical intertwiner has

```text
C_U C_U* R = R,
A = q^(-1/2) R* C_U,
AA* = S/q,
(AA*)^(+/2) A = Q* C_U.
```

The final expression is the physical PGM coisometry. The coherent row-copy,
`S_n` Fourier transforms, and group-label output are already compiled by the
physical intertwiner theorem. Therefore a coherent implementation of the
**complete** natural orientation polar `Q` finishes the known constant-success
PGM. There is no independent post-polar hidden-permutation decoder to invent.

The component maps from the preceding direct-Naimark theorem are recursive
factors of this same `Q`. They must remain coherent. Measuring leaf/component
labels during recursion destroys the block gauges needed by the polar chain
unless a separate dephasing-invariance theorem is proved; no such theorem is
available and it is not the intended architecture.

Approximation is also settled at the correct level. If exact contraction
factors `T_L...T_1` are replaced by coherent approximations with operator
errors `epsilon_l`, telescoping gives

```text
||T_L...T_1-Ttilde_L...Ttilde_1|| <= sum_l epsilon_l.
```

Every final measurement distribution differs in total variation by at most
the same sum. At `k=ceil(log2 n!)`, ideal PGM success is at least `1/2`, so a
total coherent compiler budget `1/8` leaves success at least `3/8`. A uniform
per-level budget `1/(8k)` is sufficient; inverse-polynomial accuracy per level
does not itself destroy the algorithm.

Focused verification: seven tests pass, both theorem files compile, three
finite controls have zero failures, the largest exact PGM-coisometry identity
residual is `1.66e-15`, 12 scaling rows retain robust success above `0.375`,
and `git diff --check` is clean.

**Corrected sole quantum implementation gate:** compile the complete natural
orientation polar coherently. This includes restricted child routers,
endpoint mixers, all-level composition, and natural gauge preservation. Once
that succeeds, use the existing physical PGM intertwiner. Do not open a new
sectorwise or post-polar decoder project. The positive component `M4` is a
compiler-mechanism witness, not a hidden-label statistic.

After a complete circuit exists, the remaining independent research gates are
classical complexity separation and a valid MRS-model audit. Keep complete
polar, classical separation, MRS escape, algorithm, and speedup gates false.

## Current High-Reasoning Result: Component Dilation Is Restricted Orientation-Polar Access (2026-08-21)

Files and experiment ID:

```text
self_dual_wreath_component_direct_naimark_polar_equivalence.py
tests/test_self_dual_wreath_component_direct_naimark_polar_equivalence.py
research/representation/self_dual_wreath_component_direct_naimark_polar_equivalence.json
EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIRECT-NAIMARK-POLAR-EQUIVALENCE
```

This theorem removes a redundant compiler objective from the carrier-retaining
route. Let `R=[Q_e]_e` be one child leaf synthesis, `F=RR*`, and let
`X:K->H` be an isometry into `Ran(R)`. Define

```text
A = X*F^+X,
U = R*F^(+/2),
J = F^(+/2)X A^(-1/2),
B = R*F^+X A^(-1/2).
```

Then exactly

```text
U*U=supp(F),
UU*=supp(R*R),
J*J=I,
B=UJ,
UJJ*=BJ*.
```

Thus `B` is the orientation analysis polar restricted to `Ran(J)`. If `D_e`
is the coefficient coordinate projection, then

```text
H_e=B*D_eB,
sum_e H_e=I.
```

Applying `B` and reading the coefficient coordinate is already a simultaneous
Naimark dilation of the natural component POVM. The factorization
`D_eB=V_e sqrt(H_e)` recovers the usual minimal square-root dilation followed
by controlled block gauges. Therefore **effect-by-effect matrix square-root
synthesis is not an independent natural compiler gate**. The remaining access
operation is a normalization-one implementation of the restricted orientation
polar `UJ`, or an equivalent direct coefficient router preserving the natural
block gauges.

The coefficient image is also exactly

```text
BB*=supp(R*R)-supp(R*(I-XX*)R),
```

so this result identifies the earlier dependency-support projection with the
range of the direct Naimark map; it does not introduce a second support object.

Two adversarial boundaries are part of the theorem and must not be weakened:

1. Component effects do not determine coherent output. The exact two-leaf
   countercontrol has identical effects and coordinate probabilities but
   orthogonal coherent outputs after changing one block gauge. A classical
   leaf transcript or an arbitrary Naimark dilation cannot replace the natural
   coefficient gauge in a label-sensitive decoder.
2. For `E=B-B_tilde` and an actual fiber input `rho`,

   ```text
   Tr(rho E*E) <= kappa ||E||_F^2/r,
   kappa=r||rho||_infinity.
   ```

   The rank-one countercontrol has normalized Frobenius error `1/r`, uniform-
   input error `1/r`, and concentrated-input error one. Hence the existing
   trace-weighted support scalarization becomes operational only after proving
   node-state flatness or a sharper state-specific weighted estimate.

Focused verification: seven tests pass, both theorem files compile, the live
artifact has three finite controls and zero failures, the largest `B=UJ`
residual is `1.77e-15`, the largest dependency-projection residual is
`4.96e-15`, and `git diff --check` is clean.

### Correct Frontier After This Theorem

The positive natural component `M4`, constant trace-weighted effect edge, and
support noncommutativity are already proved. Do not spend high-reasoning work
on another scalar signal or on separate effect square roots. The next hard
questions, in order, are:

1. Construct or rule out a normalization-one implementation of `U` on
   `Ran(J)` using the natural nested orientation structure. Generic uniform
   GPE exposes only `R*/sqrt(q)` and pays the forbidden width normalization.
2. Determine whether the restricted domain `Ran(J)` has additional structure
   that makes it easier than the full orientation polar. A proof must retain
   the exact common-metric embedding, not replace it by a Haar surrogate.
3. Use the already-proved all-level native-state trim: the exact frame second
   moment and fixed coefficient-register rank budget give an inverse-polynomial
   threshold without input flatness, a lower root cutoff, or a root high cap.
   The unresolved operation is coherent threshold/support SELECT and natural
   partial-isometry gauge transport, not state-error accounting.
4. Preserve the outer `S_n` carrier row and natural block gauges through the
   router, then use the already-compiled physical PGM intertwiner. Do not
   design a separate post-polar sector decoder. Leaf probabilities and scalar
   `M4` are hidden-label blind, but the complete coherent polar is sufficient.
5. After the complete circuit exists, audit its decision effect against the full adaptive MRS
   transcript model. Merely remaining coherent or lying outside the paper's
   syntax is not a separation theorem.

Keep these gates false: natural restricted-polar circuit, coherent natural
block-gauge compiler, complete orientation polar, MRS escape, classical
separation, algorithm, and speedup. A separate post-polar decoder gate is not
open; it has been reduced away conditionally on the complete polar.

The companion `self_dual_wreath_all_level_component_trim.py` supersedes any
older statement in this file that lists natural input flatness, retained root
rank, a lower root spectral window, or a root high-cap filter as a prerequisite
for average-state component trimming. Those information-theoretic gates are
closed. The coherent selector/access gate is not.

## Current High-Reasoning Result: Carrier-Traced Point Route Closed Through Quintic Samples (2026-08-21)

Files and experiment IDs:

```text
self_dual_wreath_point_critical_identity_atom.py
EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-IDENTITY-ATOM

self_dual_wreath_point_centered_residual_no_go.py
EXP-CODE-SELF-DUAL-WREATH-POINT-CENTERED-RESIDUAL-NO-GO
```

This bundle resolves the critical `c=2` point question left by the copy-
threshold theorem. Let `N=n!`, `Q=2^k`, `D=NQ`, and for public iid
Plancherel source labels `L` put

```text
Delta_(j,L)=omega_(j,L)-B_L,
B_L=n^-1 sum_j omega_(j,L).
```

The diagonal event `z=0,s=g` has exact probability `1/N` for every source
tuple. In the point quotient it is a classical simplex atom with

```text
D||Delta_atom,j||_2^2=(n-1)Q/N^2,
Xi_atom=(n-1)/N,
P_atom=1/n+(n-1)/(nN).
```

At `k=ceil(2log2 N)`, this atom asymptotically explains all previously known
annealed ambient Hilbert--Schmidt energy. The energy transition was therefore
not evidence for an operational point decoder.

The stronger centered theorem removes the atom at operator-mean level. For
every nonidentity `h`, regular-character orthogonality gives

```text
E_L p_L(0|h)=2^-k,       p_L(0|e)=1.
```

The diagonal `z=0` projection of `E_L Delta_(j,L)` is an exact point simplex
`M_j` satisfying

```text
D||M_j||_2^2=(n-1)Q/N^2(1-Q^-1)^2,
||M_j||_1/2=(n-1)(1-Q^-1)/(nN).
```

Since this is an orthogonal Hilbert--Schmidt projection,

```text
E||Delta_(j,L)-M_j||_2^2
  =E||Delta_(j,L)||_2^2-||M_j||_2^2.
```

Subtracting from the positive copy-threshold upper bound yields an explicit
residual `R_(n,k)` with dominant scale

```text
R_(n,k) <= exp(O(sqrt(n))) k exp(O(k/n^4))/n!
```

up to smaller terms. Therefore, for an arbitrary point POVM selected after
seeing every public source label,

```text
E[P_point-1/n]
 <= (n-1)(1-2^-k)/(n n!) + sqrt(R_(n,k))/2.
```

This is superpolynomially small for every `k=O(n^5)`, including all fixed
multiples of `log2(n!)`. The squared residual is nonnegative, so conditioning
on globally distinct Plancherel source draws costs only `1/(1-o(1))` for any
polynomial number of draws. The result is information theoretic and covers
every public-label-adaptive POVM on the carrier-traced point quotient; it is
not merely a PGM, QSVT, or circuit lower bound.

The virtual iid calculation includes equal partition pairs only as an
algebraic regular-character extension. The physical statement is obtained by
conditioning onto the all-unequal/global-distinct event, where the source
state is the actual unequal-pair irrep state. Do not route equal pairs through
the unequal physical constructor.

Focused verification: the centered module has five passing tests, two exact
`S_3` regular-character/mean-projection controls with zero failures, and 15
scaling records. At `n=128`, the arbitrary-point-POVM excess has log2 upper
bounds `-334.33`, `-323.67`, and `-303.14` at the critical, quartic, and
`n^5/16` schedules. Artifact status is
`carrier-traced-point-route-closed-through-quintic-samples`.

Keep these gates false:

- carrier-retaining global decoder ruled out;
- non-point collective decoder ruled out;
- all polynomial sample schedules ruled out;
- classical separation proved;
- speedup claim allowed.

**Research-direction decision:** stop work on carrier-traced point decoding,
including child-star relative-spectrum compilation. The relative collision
of the full point state is already bounded by the arbitrary-POVM theorem in
the proved window. The highest-value code-equivalence frontier is now an
explicit carrier-retaining global transform or a proof that carrier/source
entanglement also has superpolynomially small accessible information. In
parallel, the independent DCP frontier remains the density-one subset-sum
witness solver. Do not spend high-capability reasoning on more point-channel
finite controls or CLI plumbing.

## Current High-Reasoning Result: Trimmed Regular-Row Architecture Correction (2026-08-21)

Files and experiment IDs:

```text
coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-NORMALIZED-LIKELIHOOD-CHARGE-COMMUTATOR-NO-GO

coset_hidden_involution_trimmed_row_kernel_succinctness.py
EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-KERNEL-SUCCINCTNESS

coset_hidden_involution_trimmed_row_block_encoding_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-BLOCK-ENCODING-NO-GO
```

This bundle corrects the active hidden-involution architecture. On the
asymptotically full free source fiber, the existing reversible canonicalizer
and exact induction identity

```text
Ind_K^G(C[K] tensor C[O]) ~= C[G] tensor C[O]
```

fuse the `K=C_2 wr S_m` regular coordinate into a regular `G=S_(2m)`
coordinate before the `G` QFT. Generic `S_(2m) down K_m` subduction is
therefore **not** the remaining high-mass compiler. The residual object is the
orbit-copy Fourier row kernel

```text
R_lambda(o,o') = sum_g kappa_(o,o')(g) rho_lambda(g).
```

For product plus-coset rows, two robustly transitive seed coordinates give 16
endpoint orientations. For each orientation, an ordered transitive pair
conjugator is determined by one root image, giving at most `2m` possibilities.
Rooted propagation constructs them, and later coordinates filter them. Hence
`support(kappa_(o,o')) <= 16(2m)` and every pairwise matrix Fourier entry is a
polynomial-size sum of efficiently computable representation matrices on
asymptotically full alternative mass. Exact `S_4` and `S_6` controls reproduce
the full-group support and Fourier sums. Pairwise row-kernel evaluation is
classically dequantized; factorial entry summation cannot be used as quantum
leverage.

Coherent access does not rescue the route. If `I` is the physical/source
incidence matrix, normalized row- and column-edge isometries overlap as

```text
D = I/sqrt(M 2^k),        D^*D = Z/M = A.
```

The canonicalizer, induction map, and `G` QFT are unitary and preserve this
normalization. On the proved flat bulk, singular values remain
`Theta(M^-1/2)`, so generic dense-kernel polar/QSVT processing costs
`Omega(sqrt(M))`. Polynomial pairwise entries and polynomial coherent row
preparation do not fast-forward the unnormalized likelihood.

The independent charge route closes at the same boundary. Under the source
trace, `tau(Z)=1`, `tau((Z-I)^2)=eta=(M-1)/2^k`, and complete source-local
likelihood independence gives `E_Alg(D_m)(Z)=I`. Thus for every source-local
contraction `S`,

```text
||[A,S]||_(2,tau)^2 <= 4 eta/M^2.
```

At natural copy count, inverse-polynomial normalized commutator energy can
only lie on factorially small mass. A finite conditioned covariance is not a
natural signal.

The only surviving hidden-involution mechanism in this architecture is a
**direct analytically normalized global orbit-row orthogonalizer/recoupling
transform** that factors `M` symbolically before amplitude normalization. The
current theorems do not rule such a transform out, but they close all of these
proxies:

- generic hyperoctahedral subduction as the trimmed bottleneck;
- factorial pairwise kernel evaluation;
- scalar or matrix pairwise kernel estimation as an advantage;
- normalized likelihood/charge commutator mass;
- generic block-encoding, QSVT, or polar processing of coherent row states.

Keep direct-transform, detector, classical-separation, and speedup gates
false. Do not return to fixed-rank subduction catalogs or pairwise kernel
benchmarks. A future positive proposal must give explicit local rotations or
an exact combinatorial factorization of the global orbit-copy transform and
must explain where the `M` normalization cancels before state preparation.

Focused verification on 2026-08-21: all three modules compile, all 18 focused
tests pass, and live artifacts have statuses
`normalized-likelihood-charge-commutator-natural-mass-no-go`,
`regular-row-pairwise-kernel-succinct-global-polar-open`, and
`trimmed-row-coherent-access-retains-Z-over-M-normalization`. The robust-mass
artifact carries log-domain failure bounds through `m=128`; its final
alternative failure has log2 upper bound below `-1266`, rather than an
unexplained floating-point zero.

**DCP audit correction:** do not resume the proposed global-robustness theorem.
The committed repository already contains
`dcp_contaminated_pgm_audit.py`, which proves constant all-good information
mass for `O(n)` registers at exact `f=1`, and
`dcp_arbitrary_measurement_witness_reduction.py`, which proves the stronger
statement that every useful accessible standard-circuit DCP measurement
reduces to average density-one subset-sum witness preparation. The remaining
DCP frontier is the subset-sum solver itself, not a PGM/noise loophole.

## Current High-Reasoning Result: Point Copy Threshold Is Exactly Two (2026-08-21)

File and experiment ID:

```text
self_dual_wreath_point_copy_threshold.py
EXP-CODE-SELF-DUAL-WREATH-POINT-COPY-THRESHOLD
```

This theorem closes the existing carrier-traced point program at its old copy
width and identifies the only critical window worth studying. Put `N=n!` and
let

```text
S_(n,k)=N 2^k E ||omega_0-bar(omega)||_2^2.
```

The exact Plancherel point-kernel formula can be written

```text
S_(n,k)=N^-2 sum_(u,s,t) chi_(n-1,1)(u)
        [a(s^-1t)+c_u(s)d_u(t)]^k.
```

For `n>=5`, every nonidentity conjugacy class has size at least
`n(n-1)/2`; set `q=2/[n(n-1)]`. Both incidence sums
`sum_s c_u(s)` and `sum_t d_u(t)` equal the commutator density `A(u)`. The
second identity is non-obvious: products of two conjugates and commutators
have the same `S_n` law. Direct `S_3,S_4,S_5` counts verify it, while the
all-rank proof is the character calculation. Frobenius orthogonality gives

```text
N^-1 sum_u A(u)^2 = zeta_(S_n)(2).
```

After cancelling the `u`-independent zeroth binomial term, every `u!=e`
contribution is bounded in absolute value by

```text
B_non <= (n-1) zeta(2)/N * ((1+q^2)^k-1)/q^2.
```

The `u=e,s=t=e` term is exactly

```text
(n-1)(2^k-1)/N^2.
```

Separating equal nonidentity pairs, one-identity pairs, and distinct
nonidentity pairs gives a matching explicit upper bound. Therefore for every
fixed `c<2` and `k<=c log2(N)+O(1)`,

```text
S_(n,k) <= N^{-(2-c)+o(1)}.
```

This is an arbitrary-measurement no-go, not a QSVT no-go. For every point POVM
that may depend on all public source labels,

```text
P_point-1/n <= 0.5 E||omega_0-bar(omega)||_1
            <= 0.5 sqrt(S_(n,k)).
```

The point energy is nonnegative sourcewise, so conditioning all source
partitions to be globally distinct costs only `1/P_cf=1+o(1)` in this upper
bound. Thus **every fixed copy multiplier below two is closed** after carrier
trace. In particular, the old `k=ceil(log2 n!)` point PGM, linear POVM,
Young-star Naimark, and child-energy signals cannot have inverse-polynomial
average excess. Their finite positive controls are pre-asymptotic.

At the exact critical width `k=ceil(2log2 N)`, the same theorem reverses:

```text
S_(n,k) >= n-1-o(1).
```

This is a real normalized Hilbert--Schmidt energy phase transition, but it is
**not operational evidence**. It supplies no trace-distance lower bound,
relative child-star spectral window, Naimark circuit, full-permutation
decoder, or classical separation. The artifact keeps all such gates false.
The `n=128` scaling record has subcritical `c=1` log2 signal upper bound below
`-667` and critical `c=2` log2 lower bound above `7.66`.

Focused verification: six tests pass; all six exact `S_5/S_6` point signals
lie inside the theorem interval; exact nonidentity class bounds hold through
`S_12`; and the live artifact status is
`point-copy-threshold-two-proved-critical-harmonic-measurement-open`.

**Next high-reasoning task:** analyze the `c=2` relative operator, not ambient
energy. In the exact `S_(n-1)` Young-star decomposition, bound
`bar(omega)^(-1/2) Delta bar(omega)^(-1/2)` or the equivalent child-star PGM
seed on natural pairwise-unequal sources. Either prove an inverse-polynomial
operational spectral window and a direct harmonic Naimark route, or show that
the identity spike lies in factorially inaccessible relative eigenvalues.
Do not run more `c<2` point experiments and do not promote the critical
Hilbert--Schmidt lower bound by itself.

## Current High-Reasoning Result: Critical Energy Is Operationally Underdetermined (2026-08-21)

File and experiment ID:

```text
self_dual_wreath_point_critical_energy_separation.py
EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-ENERGY-SEPARATION
```

This theorem proves that the new `c=2` energy phase transition cannot by
itself support either a positive algorithm claim or a point-decoding no-go.
For a uniform point ensemble on an ambient `D`-dimensional register, put

```text
B=n^-1 sum_j rho_j,       Delta_j=rho_j-B.
```

The PGM has the exact relative-collision identity

```text
p_PGM = 1/n + n^-2 sum_j
  Tr(B^-1/2 Delta_j B^-1/2 Delta_j),
```

with Moore--Penrose inverses on `supp(B)`. For a covariant ensemble all `n`
relative-collision terms are equal. Ambient energy
`D||Delta_j||_2^2` does not determine this quantity.

The module constructs two exact commuting `S_n`-covariant ensembles whenever
`n` divides `D`. Both satisfy

```text
D||Delta_j||_2^2=n-1.
```

The flat-partition ensemble divides the basis into `n` disjoint blocks. It
has `B=I/D`, relative collision `n-1`, PGM success one, and optimal success
one. The spiky-simplex ensemble is supported on only `n` basis vectors:

```text
rho_j=I_n/n+sqrt(n/D)(|j><j|-I_n/n).
```

It has relative collision `n(n-1)/D`, PGM success
`1/n+(n-1)/D`, and exact optimal success

```text
1/n+(n-1)/sqrt(nD).
```

At the natural critical width
`D=n! 2^ceil(2log2(n!))`, that optimal excess is factorially small. The
`n=512` scaling record puts its log2 value below `-5808`, while the
same-energy flat family is still perfectly distinguishable. Therefore the
critical ambient-energy theorem is genuinely underdetermined, not merely
missing a loose norm inequality.

Focused verification: five tests pass, the two natural-width finite controls
have zero formula failures, the live artifact status is
`critical-energy-only-inference-falsified-relative-spectrum-open`, and every
natural-family measurement/speedup gate remains false.

**Refined next high-reasoning task:** derive the natural child-star formula
for

```text
Xi_j=Tr(B^-1/2 Delta_j B^-1/2 Delta_j)
```

at `k=ceil(2log2 n!)`, and control it on typical globally distinct public
labels. In the Young-star form this requires signal-weighted spectral
control relative to the parent-diagonal average blocks `D_nu/d_nu`; a global
top-eigenvalue or purity bound is not enough. Prove either
`Xi_j>=n^-O(1)` on sufficient mass (then point-PGM excess is `Xi_j/n` and a
harmonic Naimark compiler becomes meaningful) or a superpolynomial upper
bound. Do not infer either conclusion from ambient Hilbert--Schmidt energy.

## Current High-Reasoning Result: Relative Point Signal Has Positive Young Channels (2026-08-21)

File and experiment ID:

```text
self_dual_wreath_point_child_star_relative_collision.py
EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-RELATIVE-COLLISION
```

The relative quantity from the preceding falsifier now has an exact
representation-theoretic decomposition. Let `omega=T_H(tau)`,
`B=T_G(tau)`, and `Delta=omega-B`. Point covariance gives

```text
Xi=Tr(B^-1/2 Delta B^-1/2 Delta),
p_point_PGM=1/n+Xi/n.
```

In the `H=S_(n-1)` Young basis,

```text
omega=direct_sum_alpha I_(d_alpha) tensor Z^H_alpha,
B    =direct_sum_alpha I_(d_alpha) tensor Z^G_alpha,
Z^G_alpha=direct_sum_(nu covers alpha) D_nu/d_nu.
```

Therefore

```text
Xi=sum_alpha d_alpha
   ||(Z^G_alpha)^-1/4 (Z^H_alpha-Z^G_alpha)
     (Z^G_alpha)^-1/4||_F^2.
```

Because the average is parent diagonal, this refines into nonnegative
`(alpha,nu,mu)` terms

```text
d_alpha ||(D_nu/d_nu)^-1/4 Delta_(alpha;nu,mu)
          (D_mu/d_mu)^-1/4||_F^2.
```

Thus relative point signal cannot cancel between child stars or parent pairs.
The orientation projection-Gram theorem further gives

```text
D_nu/d_nu=(2^k dim(C))^-1
  [I_(d_nu) tensor W H_nu W^*].
```

Multiplying both `Z^H_alpha` and `Z^G_alpha` by `2^k dim(C)` leaves the PGM
child effect exactly unchanged. The common density normalization is therefore
**not** an intrinsic factorial scalar-amplification obstruction for the
mathematical point PGM. What remains is a wide, source-dependent,
dimensionless orientation-kernel transform and its signal-weighted relative
spectrum.

Focused verification: five tests pass; all three exact controls pass; 22
finite parent-pair channels are active, 16 off diagonal; the largest finite
relative collision is about `0.767`; rescaled effect residuals are numerical
zero; and artifact status is
`relative-child-star-channels-exact-critical-asymptotics-open`. Natural
critical mass, harmonic compilation, full recovery, and speedup remain false.

**Next high-reasoning task:** express each dimensionless relative parent-pair
channel directly in the orientation projector-Gram data `H_nu` and the
cross-parent native purification Gram. Then derive a Plancherel expectation
and concentration theorem at `k=ceil(2log2 n!)` after globally distinct
conditioning. The theorem must be signal weighted: existing global frame-norm
obstructions can be caused by common cores in sectors carrying little or no
`Delta` mass. Determine whether an inverse-polynomial fraction of `Xi` lies in
an efficiently describable spectral window, or prove that every such natural
window has superpolynomially small mass.

## Current High-Reasoning Result: Pair-Gaudin And K-Adapted Matching Charges (2026-08-20)

Files and experiment IDs:

```text
coset_hidden_involution_pair_gaudin_hierarchy.py
EXP-COSET-HIDDEN-INVOLUTION-PAIR-GAUDIN-HIERARCHY

coset_hidden_involution_pair_matching_charge_hierarchy.py
EXP-COSET-HIDDEN-INVOLUTION-PAIR-MATCHING-CHARGE-HIERARCHY
```

The first module proves an exact all-rank infinitesimal-braid hierarchy.  For
the eight-term pair interaction `c_ij`, disjoint interactions commute and
`[c_ij,c_ik+c_jk]=0`.  Therefore

```text
J_r=sum_(i<r)c_ir
```

commute and have only `8(r-1)` permutation terms.  Their aggregate is the
natural support-three charge `C_m`.  Individual `J_r` are not `K_m` adapted,
and every repeated `S_8` and `S_10` control retains joint-spectrum degeneracy.
This is an intermediate Gaudin basis, not a hyperoctahedral subduction basis.

The second module derives the first terminal `K_m`-adapted commuting extension:

```text
C_m = sum_(i<j)c_ij,
D_m = sum_{{ i,j } disjoint { k,l }} c_ij c_kl.
```

`C_m` is central in the algebra generated by all `c_ij`, so `[C_m,D_m]=0`
at every rank.  Both charges commute with `K_m` and have exactly
`8*binomial(m,2)` and `192*binomial(m,4)` distinct terms.  The obvious edge
power sum is provably redundant:

```text
c_ij^2=4c_ij+8z_ij,
sum c_ij^2=4C_m+8Z_m,  Z_m in Z(C[K_m]).
```

Finite branch-resolved controls show genuine but incomplete progress.  At
`m=5`, adjoining `D_m` changes the copy-label counts from `25` to `26` for
`lambda=(6,3,1)` (the exact target is `26`) and from `34` to `35` for
`lambda=(5,3,2)` (target `37`).  It leaves the worst controlled
`lambda=(4,3,2,1)` sector at `50` of `62` labels.  At `m=6`, it closes the
stable `lambda=(8,4)` and the tested `(9,2,1)` and `(8,2,2)` restrictions.

More strongly, occupancy-channel interpolation proves that normalized `D_m`
resolves the all-rank stable branch

```text
lambda_m=(2m-4,4), mu_m=((m-2,2),empty), b(lambda_m,mu_m)=2
```

with exact squared gap

```text
4(m^4-14m^3+75m^2-166m+129)
 / [m^2(m-3)^2(m-2)^2(m-1)^2]
```

and `gap(D_m)>=2/(5m^2)`.  This is `16/25` of the previously proved
support-five squared gap.  The stable branch has factorially negligible
natural source mass, so this is not a speedup mechanism by itself.

The naive third matching charge `M_3` fails: at `m=6`, an explicit coefficient
of `[D_m,M_3]` is `-1`.  An exact degree-three motif search found corrected
commuting combinations, but the strongest six-label correction adds no label
after `C_m,D_m` on the tested `m=5` and `m=6` sectors.  Do not promote it to a
third independent charge.  The next high-reasoning obligations are:

1. Prove or falsify that `D_m` contributes copy information beyond `C_m` and
   the `K_m` center on inverse-polynomial hidden-source mass.
2. Classify the low-degree `K_m`-invariant centralizer of `D_m`, separating
   true new charges from polynomials in `C_m,D_m` and `K_m`-center elements.
3. Find a third charge that splits a controlled residual sector before seeking
   an all-rank hierarchy.
4. Prove conditional gap and source-CS likelihood correlation.  Stable gaps,
   finite copy splits, and exact commutation do not imply either.

Focused verification currently reports six passing pair-Gaudin tests and
eight passing pair-matching tests.  The pair-matching artifact status is
`K-adapted-commuting-pair-proved-partial-copy-resolution`.  All natural-mass
completion, conditional-gap, source-correlation, coherent-transform,
detector, and speedup gates remain false.

### Natural-mass independence of `D_m`

The next theorem closes the natural-relevance part of that list, but not the
algorithmic gates:

```text
coset_hidden_involution_matching_charge_natural_independence.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-NATURAL-INDEPENDENCE
```

Define `T_m` as the normalized Hermitian average of all six orders of
`c_ij c_ik c_jk` over pair-label triples.  `T_m` commutes with `C_m` and
centralizes `K_m`, but it does not commute with `D_m`.  Exact local expansion
proves

```text
delta_m = ||[D_m,T_m]||^2_reg
        = 9(m-4)/[1024 m^3(m-3)(m-2)^3(m-1)^3]
        = Theta(m^-9).
```

The commutator vanishes on four pair labels.  Every five-label set contributes
exactly 122,880 terms, split evenly between coefficients `+12` and `-12`;
the unnormalized squared norm is 17,694,720.  The complete six-label
commutator is exactly the sum of its six embedded five-label copies, proving
that all overlap-one contributions cancel.  Disjoint seven-label words
commute termwise.  This is an all-rank local decomposition, not interpolation.

Because `T_m` commutes with `Alg(C_m,Z(C[K_m]))`, blockwise

```text
dist_F(D_m,Alg(C_m,Z(C[K_m])))^2/d
  >= ||[D_m,T_m]||_F^2/(4d).
```

Thus Plancherel mass at least `delta_m/(8-delta_m)` has commutator energy at
least `delta_m/2` and squared distance at least `delta_m/8`.  Every commutator
term moves at most ten points, so `coefficient_h(X^*X)=0` for `m>=11`; the
same mean and mass are present in the occupied h-even source space.  A
factorial tail comparison proves that for every `m>=13`, positive certified
mass remains after excluding all row/column defect-four partitions.  This
falsifies the hypothesis that `D_m` supplies only stable-family or
`C_m`/K-center information.

Six focused tests pass and the artifact status is
`matching-charge-natural-independence-proved-hierarchy-open`.  The result does
not provide a third commuting charge, conditional joint gaps, source-CS
likelihood correlation, a normalized subduction transform, a detector, or a
speedup.  Those gates remain false.  In particular, one- and two-copy tests
cannot validate the needed correlation because their exact Helstrom normal
forms are already scalar/target-label sufficient; the next correlation
experiment must use a genuinely matrix-valued three-or-more-copy A/B block.

### Matching-charge correlation and exact collective no-go boundary

Files and experiment IDs:

```text
coset_hidden_involution_matching_charge_cs_correlation.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-CS-CORRELATION

coset_hidden_involution_source_local_likelihood_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-SOURCE-LOCAL-LIKELIHOOD-NO-GO

coset_hidden_involution_diagonal_charge_bias_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-DIAGONAL-CHARGE-BIAS-NO-GO

coset_hidden_involution_cross_transposition_hecke_moment_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-CROSS-TRANSPOSITION-HECKE-MOMENT-NO-GO
```

The first module constructs the smallest honest matrix-valued conditioned
block found so far.  In `S_10`, with sources
`(6,2,2),(6,2,2),(9,1)` and target `(9,1)`, exact `S_9/S_8` restriction
matrix units and the exact `K_5` Reynolds projector give a six-dimensional
occupied A/B block.  Its squared principal cosines range from
`0.0956617478` to `0.2375409059`.  Compressed `D_5` has six distinct
eigenvalues, centered CS correlation `0.2397314804`, and raises regression
`R^2` from `0.0704700319` to `0.0789366357`.  It also has occupied-range
leakage `0.1289254802` and CS commutator norm `0.0016776943`; it does not
diagonalize the likelihood.  This proves only that `D_5` is not pure nuisance
after conditioning on this target block.  The family is fixed-defect and
factorially negligible, so it is not natural scaling evidence.

The second module then proves the decisive all-group cancellation theorem.
For the exact double-coset normal form

```text
A={(r,...,r;r):r in G},
B={(eps_1 r,...,eps_k r;r):r in K=C_G(h), eps_i in H=<h>},
Z=[G:K] e_B e_A e_B,
```

the target-identity slice of `B A B` is exactly `H^k`, every element with
constant multiplicity `2^k|K|^2`.  Therefore, for every source-coordinate
group-algebra element `x`,

```text
tr_B(x Z)=tr_B(x).
```

For every B-compatible Hermitian `x`, this applies to all spectral
projectors, so the complete measurement distribution, not just its mean, is
likelihood independent.  It includes every joint per-source measurement of
`C_m,D_m` and any other K-centralizing charge hierarchy.

The stronger slice identity is

```text
b(eps,r) a_g b(eps',r')
  =(eps_1 t eps'_1,...,eps_k t eps'_k;t),  t=r g r'.
```

If an observable leaves any source coordinate untouched, identity there
forces `t in H`; hence every proper source-plus-target marginal has the same
factorization.  A sum of terms touching at most `s` source copies has all
likelihood-weighted moments through degree `d` identical whenever `sd<k`.
Any group-algebra escape must be genuinely target-coupled across all `k`
copies.  The positive finite `D_5` covariance therefore cancels across
omitted target/outer sectors and cannot be promoted into a source-only
detector.

The third module kills the simplest all-copy escape.  For
`a_t=(t,...,t;t)`, `X_t=e_B a_t e_B`, exact factorization gives

```text
tr_B(X_t)=1[t in K],
tr_B(X_t Z)=1       if t in K,
              2^-k if t not in K.
```

Thus a Hermitian diagonal LCU with coefficient `l1` norm at most one has bias
at most `2^-k`.  At `k=ceil(log2(64M))` this is at most `1/(64M)`; constant
linear bias requires LCU normalization at least `2^k` and merely recreates
the orbit-label normalization barrier.  This does not rule out interleaved
powers `e_B y e_B y e_B`, nonlinear spectral tests, or nondiagonal all-copy
recoupling charges.  Those are now the correct high-reasoning search space.

The fourth module evaluates the first interleaving exactly for the canonical
perfect-matching switch.  Let `t` transpose points in two different h-pairs
and `X=e_B a_t e_B`.  For every `m>=3`,

```text
|K intersect tKt|=2^m(m-2)!,
tr_B(X^2)=1/[2^k m(m-1)].
```

The likelihood-weighted binary return count has one universal branch and one
extra branch exactly on `K intersect tKt`; all other six binary patterns are
impossible.  Hence

```text
tr_B(X^2 Z)=4^-k[1+(2^k-1)/(m(m-1))],
tr_B(X^2 Z)-tr_B(X^2)=4^-k[1-1/(m(m-1))].
```

The next binary-return layer also closes exactly.  Put
`r=m(m-1)` and `a=3m^2-7m+5`.  Switching the distinguished four-point
matching gives one full-product branch and switching two unaffected pairs
gives `(m-2)(m-3)` more.  The resulting cubic moments are

```text
tr_B(X^3)=1/(4^k r^2),
tr_B(X^3 Z)=[r^2-a-1+a 2^k+4^k]/(8^k r^2).
```

The degree-four layer is now also closed exactly.  A three-switch path activates
at most six of the `n=m-2` unaffected base pairs.  Deleting inactive pairs is a
bijection for every even-cardinality identity subword, reducing all ranks to
seven exact support cores.  Their binomial lift gives

```text
N8 = 1,
N4 = 7 + 16n + 14*C(n,2),
N2 = 84n + 260*C(n,2) + 336*C(n,3) + 144*C(n,4),
N1 = r^3-N2-N4-N8.
```

These counts hold at `m=3` and every `m>=5`.  At `m=4`, exactly six paths gain
one odd-cardinality identity subword, moving six paths from `N1` to `N2`.
This exception list is itself all-rank: an odd identity subword cannot leave
an inactive common pair, while three switches activate at most six pairs; the
same exact core catalog through `m=8` finds only the `m=4` exception.

The independently enumerated baseline closure histogram is

```text
Q1=8n,  Q2=2+8n+6*C(n,2)=3m^2-7m+4,  Q4=1.
```

Writing `x=2^k`, the exact moments are

```text
tr_B(X^4)   = [Q1+Q2*x+x^2]/[x^3*r^3],
tr_B(X^4 Z) = [N1+N2*x+N4*x^2+x^3]/[x^4*r^3].
```

The unique alternative `N8` transporter branch and unique baseline `Q4`
closure branch contribute the same `x^3` term.  They cancel exactly in the
likelihood bias, leaving

```text
tr_B(X^4 Z)-tr_B(X^4)
 = [N1+(N2-Q1)x+(N4-Q2)x^2]/[x^4*r^3]
 = O(x^-2).
```

At natural `k`, the relative second-moment excess vanishes, the new
degree-four contribution is `O(M^-2)`, and every unit-coefficient quartic
filter in the single cross-transposition operator still has only
inverse-candidate total bias.  This is not a full-spectrum theorem: rare large
eigenvalues, degree five and higher, and mixtures of double cosets remain open.

An attempted all-degree proof by excluding subgroup transporters is false.
There is an explicit three-switch path on six points, lifting unchanged to
every `m>=3`, whose selected middle bits `(0,1,1)` give a word `x` with
`x h x^-1=t h t`.  Nevertheless the complete five-involution subword law has
support 28 of 32 and maximum multiplicity only two (`1/16`); its identity
multiplicity is one.  Exactly `12(m-2)` of the `[m(m-1)]^3` three-switch
paths realize this selected transporter, a fraction `Theta(m^-5)`.  A
transporter is therefore necessary for endpoint collision but not sufficient
for large concentration.  Any all-degree theorem must bound the total mass and
alignment of transporter subwords, not assert that they do not exist.

### Exact degree-five continuation and cancellation falsifier

Files and experiment ID:

```text
coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-CROSS-TRANSPOSITION-HECKE-DEGREE-FIVE-NO-GO
```

Four switches activate at most eight unaffected base pairs.  The new module
enumerates all nine canonical all-active support cores exactly, using
meet-in-the-middle identity-subword counting, and lifts them by the same
delete/insert bijection.  With `n=m-2`, the stable degree-five histogram is

```text
N16 = 1,
N8  = 15 + 24n + 30*C(n,2),
N4  = 252n + 822*C(n,2) + 1200*C(n,3) + 600*C(n,4),
N2  = 564n + 5212*C(n,2) + 18216*C(n,3) + 30240*C(n,4)
      + 24000*C(n,5) + 7200*C(n,6),
N1  = 440n + 12096*C(n,2) + 82248*C(n,3) + 258408*C(n,4)
      + 436800*C(n,5) + 410400*C(n,6) + 201600*C(n,7)
      + 40320*C(n,8).
```

It holds at `m=3` and every `m>=5`.  At `m=4`, exact odd-word accounting
moves 96 paths from `N1` to `N2` and 60 from `N2` to `N4`; there are 156
exceptional paths and 216 odd identity occurrences.  The independently
enumerated baseline closure histogram is

```text
Q1=48n,  Q2=20n+20*C(n,2),  Q4=5.
```

Therefore, for `x=2^k` and `r=m(m-1)`,

```text
tr_B(X^5)   = [Q1+Q2*x+Q4*x^2]/[x^4*r^4],
tr_B(X^5 Z) = [N1+N2*x+N4*x^2+N8*x^3+x^4]/[x^5*r^4].
```

The degree-four leading cancellation does **not** extend to degree five.  The
unique `c=16` branch has no baseline term of equal copy weight and survives as
`1/(x*r^4)`.  This is a useful falsifier, not a positive signal: at natural
`x>=64M` it retains the full inverse-candidate penalty and an additional
`r^-4` path-mass suppression; the remainder is at most `4/x^2`.  A normalized
quintic filter still cannot have constant bias.

Seven focused tests pass.  The live artifact status is
`cross-Hecke-quintic-no-go-leading-transporter-survives-sparsely`; theorem
verification is true while all full-spectrum, detector, algorithm, and speedup
gates remain false.

### All-degree single-Hecke moment and polynomial-LCU no-go

Files and experiment ID:

```text
coset_hidden_involution_single_hecke_all_degree_moment_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-SINGLE-HECKE-ALL-DEGREE-MOMENT-NO-GO
```

The fixed-degree catalogs are superseded for bounding purposes by a simple
all-degree injection.  In every nontrivial loopless orbital path, the first two
involutions `a,b` are distinct.  Fix all other subword bits.  The four products
obtained from the first two bits are, up to common factors,

```text
e, a, b, ab.
```

They are pairwise distinct because `a,b` are distinct nonidentity
involutions.  Every ordered-subword product fiber therefore meets each
four-bit block at most once and has at most one-quarter of the full cube,
independently of degree and even when degree grows with `m`.

In the exact binary path normal form, the alternative degree-`d` moment is an
average of `(c_path/2^d)^k`, so it is at most `2^-k`.  On a baseline closure
path the duplicated terminal involution pairs identity subwords, giving binary
count `c_path/2` with denominator `2^(d-1)` and the same bound.  Degree one
saturates the bound directly.  Thus for every `d>=1`,

```text
0 <= tr_B(X^d), tr_B(X^d Z) <= 2^-k,
|tr_B(X^d Z)-tr_B(X^d)| <= 2^-k.
```

For every finite or absolutely summable polynomial
`P(X)=sum_d alpha_d X^d` with `sum|alpha_d|<=1`, the likelihood bias is also
at most `2^-k<=1/(64M)` at natural copy count.  Transporters do not evade this
argument; it never attempts to exclude them.

Eight focused tests pass.  The live artifact status is
`single-Hecke-all-degree-moment-and-normalized-polynomial-no-go`.  This closes
all normalized moments and polynomial LCUs in one loopless Hecke operator.  It
does **not** close discontinuous spectral projectors, polynomial approximants
with large coefficient `l1` norm, adaptive postselection, or noncommuting
mixtures of multiple double cosets.  All detector, algorithm, and speedup gates
remain false.

### Bounded-polynomial/QSVT spectral no-go

Files and experiment ID:

```text
coset_hidden_involution_single_hecke_bounded_spectral_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-SINGLE-HECKE-BOUNDED-SPECTRAL-NO-GO
```

Large monomial coefficient norm does not rescue an efficiently bounded
single-operator filter.  For `r=m(m-1)` and `x=2^k`, the exact second moments
of the baseline and likelihood-weighted spectral laws are

```text
s0=1/(x*r),
s1=(x+r-1)/(x^2*r).
```

If a real degree-`D` polynomial satisfies `||p||_infinity<=1` on `[-1,1]`,
Markov's brothers inequality gives `||p'||_infinity<=D^2`.  The constant
`p(0)` cancels because both spectral laws have total mass one.  Applying
Cauchy--Schwarz separately to both laws gives the exact query-model bound

```text
|E_1 p(X)-E_0 p(X)| <= D^2*(sqrt(s0)+sqrt(s1)).
```

Bias at least `beta` therefore requires

```text
D >= sqrt(beta/(sqrt(s0)+sqrt(s1))).
```

At natural `x>=64M` and `x>=r`, this implies

```text
D >= sqrt(beta)*(x*r)^(1/4)/sqrt(1+sqrt(2))
  = Omega(M^(1/4)).
```

This is superpolynomial in `m`.  It rules out efficient bounded-polynomial
single-`X` spectral transformations, including the standard QSVT/block-query
route.  Six focused tests pass and the live artifact status is
`single-Hecke-bounded-spectral-QSVT-no-go`.

The scope is important: small moments alone do not bound unrestricted total
variation.  The theorem does not grant or analyze free exact eigenbasis access,
a stronger oracle than block access to `X`, unbounded postselection, or
noncommuting multi-operator algorithms.  Those gates remain open/false; no
detector or speedup is claimed.

Focused tests currently report five passing finite-correlation tests, six
passing collective-no-go tests, four passing diagonal-bias tests, and eleven
passing first-four-moment Hecke tests plus seven degree-five tests.  Artifact
statuses are
`finite-D-CS-correlation-proved-natural-scaling-open`,
`source-local-likelihood-independence-proved-target-recoupling-mandatory`, and
`normalized-diagonal-all-copy-charge-bias-no-go-proved`, and
`cross-Hecke-quartic-no-go-transporter-leading-term-cancelled`.  All transform,
decoder, detector, and speedup gates remain false.  The Hecke artifact was
regenerated after the degree-four proof and has seven exact support-core
controls and six all-rank branch controls.

The next theorem-level obligations are:

1. Do **not** continue fixed-degree moment catalogs merely by increasing the
   degree.  The adjacent-pair theorem closes normalized moments at every degree,
   including growing degree.  The Markov/Cauchy--Schwarz theorem also closes
   efficient bounded-polynomial/QSVT filtering of a single operator.  The next
   hard task is now multi-operator: determine whether a normalized family of
   different double-coset operators can create joint second-moment width or
   noncommuting signal without using exponentially large coefficient norm.
   First separate the commutative `(S_(2m),K_m)` orbital algebra from the
   source-lifted B-Hecke algebra and count the physically accessible dimension.
2. Search for B-compatible all-copy charges outside the diagonal A-convolution
   span, with an inverse-polynomial normalized likelihood signal.
3. Resolve conditioned-block cancellation by target sector and determine
   whether an efficiently computable sign/reweighting rule exists on natural
   mass.
4. Do not spend high-reasoning Codex usage on registry, CLI, README, or broad
   repetitive validation for these modules; those are mechanical handoff work.

The old `Periodic Frame Rank Collapse` footer says the dense constant-state
suffix-branch theorem is open.  That sentence is superseded by `Dense
Automaton Dyadic Boundary (2026-08-13)`, which proves the general entropy
bound.  Do not resume the stale footer task; the remaining automaton frontier
is only the near-uniform dyadic regime recorded in the newer section.

## Current High-Reasoning Result: Natural Hyperoctahedral Recoupling (2026-08-20)

Files and experiment IDs:

```text
coset_hidden_involution_natural_recoupling_boundary.py
EXP-COSET-HIDDEN-INVOLUTION-NATURAL-RECOUPLING-BOUNDARY

coset_hidden_involution_hyperoctahedral_branching_mass.py
EXP-COSET-HIDDEN-INVOLUTION-HYPEROCTAHEDRAL-BRANCHING-MASS
```

The first module derives the actual natural-block map. Every source coordinate
has exact `H=<h>`-spherical Fourier law

```text
p_H(lambda)=d_lambda(d_lambda+chi_lambda(h))/|S_(2m)|.
```

Its total variation from Plancherel is at most `1/(2 sqrt(M))`, where
`M=|h^G|`, and Plancherel character orthogonality gives
`Pr[|chi(h)|/d>=epsilon] <= 1/(M epsilon^2)`. Thus all logarithmically many
coordinate labels are jointly Plancherel-typical on overwhelming mass. The
exact matrix block is the restriction/recoupling overlap

```text
Hom_G(1, tensor_i lambda_i tensor tau)
  <--> Hom_K(1, tensor_i lambda_i^+ tensor Res_K(tau)),
lambda_i^+ = direct_sum_(|beta| even)
               b(lambda_i;alpha,beta)[alpha,beta].
```

Efficient symmetric and hyperoctahedral QFTs expose outer/isotypic labels but
do not supply the symmetric-group Kronecker multiplicity basis or the
branching-copy basis. Even granting arbitrary unitary basis changes,
projection retains exact average success `1/M`, hence generic
reflection/postselection cost `Omega(sqrt(M))`. Bacon-Chuang-Harrow
`quant-ph/0407082` provides a generic irrep-label projector, not a full `S_n`
Kronecker multiplicity transform. The 2026 diagram QFT's large-loop regime
does not match natural tensor order `Theta(n log n)` with loop parameter `n`.

The second module proves that this missing-label problem is present on natural
mass. Refining one source coordinate into a `K=C_2 wr S_m` irrep gives

```text
q(lambda,mu)=2 d_lambda d_mu b(lambda,mu)/(2m)!,  |beta(mu)| even.
```

For `I_N=sum_lambda d_lambda` and
`J_m^+=sum_(b even) binom(m,b) I_(m-b)I_b`,

```text
Pr_q[b(lambda,mu)<=T] <= 2 T I_(2m) J_m^+/(2m)!.
```

Taking `T=M^(1/4)` and union-bounding over the natural logarithmic copy width
puts every coordinate in superpolynomial branching multiplicity on
overwhelming mass. At degree 128 the missing-label commutant dimension lower
bound exceeds `2^178`. A `K` QFT cannot resolve these copies because every
`C[K]` operator acts as identity on the multiplicity factor. This is not a
circuit lower bound: a paired-tower path can still use polynomially many bits.

Eleven natural-recoupling tests and ten branching-mass tests pass. Artifacts
have statuses
`natural-recoupling-map-proved-known-basis-transforms-retain-sqrt-M-normalization`
and
`natural-huge-hyperoctahedral-branching-mass-proved-missing-label-recursion-open`.
All detector, normalized-transform, and speedup gates remain false.

## Current High-Reasoning Result: Paired-Tower Primitive Boundary (2026-08-20)

Files and experiment IDs:

```text
coset_hidden_involution_paired_tower_missing_label_boundary.py
EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-MISSING-LABEL-BOUNDARY

coset_hidden_involution_colour_resolved_paired_tower_boundary.py
EXP-COSET-HIDDEN-INVOLUTION-COLOUR-RESOLVED-PAIRED-TOWER-BOUNDARY
```

The first module proves the exact restriction recurrence

```text
sum_(mu covers nu) b_m(lambda,mu)
  = sum_gamma f^(lambda/gamma)b_(m-1)(gamma,nu).
```

For the bipartition down-incidence matrix `D_m`, the product Young lattice is
a 2-differential poset:

```text
D_m D_m^T-D_(m-1)^T D_(m-1)=2I.
```

Therefore the recurrence fixes only `D_m b_m` and leaves a fresh kernel of
dimension `p_2(m)-p_2(m-1)`. Exact power-sum plethysm controls have zero
recurrence or dimension failures, and all 38 controlled `S_(2m)` irreps for
`m=2,3,4` have nonzero harmonic residual. At `m=64`, the kernel dimension is
`421,360,145`.

The second module gives the strongest obvious local repair and falsifies it.
Resolving the last `K_1=C_2` label splits the recurrence into horizontal and
vertical two-strip equations `D_alpha b` and `D_beta b`. Their common kernel is

```text
ker D_alpha intersect ker D_beta
  = direct_sum_(a+b=m) ker D_a^Y tensor ker D_b^Y,
h_m=p_2(m)-2p_2(m-1)+p_2(m-2).
```

The exact asymptotic is `h_m/p_2(m)~pi^2/(3m)`: its fraction vanishes, but its
dimension remains `exp(Theta(sqrt(m)))`. Exact controls for `m=2,...,6` have
zero split-recurrence failures. The hidden-source mass on irreps with nonzero
joint-primitive component is respectively
`1,31/40,251/315,1,1901/1925`; this is finite evidence only, not an asymptotic
component-norm theorem. Nineteen focused tests pass for each module.

This kills lower-rank coefficient recursion, even with the complete last-pair
colour, as a self-contained compiler. It does not prove subduction hardness.
The follow-up work below sharpens this boundary and supersedes any reading of
the joint primitive kernel as a physical source subspace.

### Joint-primitive coefficient projector is diagnostic only

Files and experiment IDs:

```text
coset_hidden_involution_paired_tower_joint_primitive_projector.py
EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-JOINT-PRIMITIVE-PROJECTOR

coset_hidden_involution_joint_primitive_ambient_lift_obstruction.py
EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-AMBIENT-LIFT-OBSTRUCTION

coset_hidden_involution_joint_primitive_representation_cone_obstruction.py
EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-REPRESENTATION-CONE-OBSTRUCTION
```

Young-lattice differential-poset theory gives the exact auxiliary projector

```text
P_n^prim=product_(j=1)^n (I-D_n^T D_n/j),
P_m^joint=direct_sum_(a+b=m) P_a^prim tensor P_b^prim.
```

Its normalized zero gap is at least `1/n`, and add/remove-corner access is
polynomially sparse. This proves an efficient query reflection on the
Euclidean vector space of recurrence coefficients. It does **not** produce a
physical branching-copy reflection.

There are two exact all-rank obstructions. First, Schur's lemma gives

```text
Res_K V_lambda=direct_sum_mu C^b(lambda,mu) tensor V_mu,
End_K(Res_K V_lambda)
  =direct_sum_mu End(C^b(lambda,mu)) tensor I_(V_mu).
```

The primitive coefficient projector has off-diagonal entries between
inequivalent `mu`, so it has no `K`-centralizing ambient lift. This does not
rule out a deliberately non-`K`-equivariant full subduction circuit.

Second, the coefficient projector does not preserve the representation cone.
For every `n>=2`, the alternating hook vector

```text
h_n=sum_(r=0)^(n-1) (-1)^r e_(n-r,1^r)
```

lies in `ker D_n`, while
`U e_(n-1)=e_(n)+e_(n-1,1)`. Therefore

```text
P_n[(n-1,1),(n)] = -P_n[(n),(n)] < 0.
```

This has a physical restriction counterexample at every rank. The trivial
`S_(2m)` representation restricts to the single trivial `K_m` irrep
`((m),empty)`, with maximum branching multiplicity one and no repeated copy.
Nevertheless its joint-primitive coefficient residual is nonzero, signed,
and fractional. Thus nonzero primitive residual and its Euclidean norm do not
imply a physical missing-copy subspace or hidden-source mass. Earlier finite
statements about the fraction of `lambda` with nonzero residual are
coefficient-table diagnostics only.

The three focused suites pass 18 tests. Their statuses are
`paired-tower-joint-primitive-coefficient-projector-diagnostic-only`,
`joint-primitive-label-projector-K-commutant-lift-obstructed`, and
`joint-primitive-coefficient-projector-diagnostic-only`. Keep physical
primitive measurement, source primitive mass, normalized subduction,
detector, and speedup gates false.

The next high-reasoning task is no longer to lift this coefficient projector.
Use the existing bounded-support commutant, stable support-six, natural local
commutator, and matching-charge results to attack the actual spaces
`C^b(lambda,mu)`. The decisive positive theorem is a polynomially described
within-`mu` generator hierarchy with inverse-polynomial **conditional** gaps
on inverse-polynomial natural source mass and a coherent local diagonalization.
The decisive falsifier is that bounded-complexity generators leave growing
joint degeneracy on that mass, or that resolving it reconstructs unrestricted
plethysm/subduction data. Do not use coefficient-kernel dimension or norm as
a proxy for either condition.

### Natural matching charge is accessible, but every scalar/linear use is closed

Files and experiment IDs:

```text
coset_hidden_involution_matching_charge_conditional_diameter.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-CONDITIONAL-DIAMETER

coset_hidden_involution_matching_charge_coherent_label_compiler.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-COHERENT-LABEL-COMPILER

coset_hidden_involution_matching_charge_orbit_recoupling_reduction.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-ORBIT-RECOUPLING-REDUCTION

coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-PAIRWISE-KERNEL-DEQUANTIZATION

coset_hidden_involution_matching_charge_word_moment_dequantization.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-WORD-MOMENT-DEQUANTIZATION
```

The exact matching/triangle commutator energy does more than prove algebraic
independence. In each common `(lambda,mu,C_m-eigenvalue)` multiplicity block,

```text
e=||[D_m,T_m]||_F^2/q <= diam(D_m)^2.
```

Therefore hidden-source mass at least `delta_m/(8-delta_m)` contains two
`D_m` eigenvalues separated by at least `sqrt(delta_m/2)`, where

```text
delta_m=9(m-4)/[1024m^3(m-3)(m-2)^3(m-1)^3].
```

Explicitly, good mass is at least `9/(40960m^9)` and the conditional
diameter is at least `3/(sqrt(10240)m^(9/2))`. Some of this mass is outside
all row/column defect-four sectors for every `m>=13`. This is one separated
eigenvalue pair, not a minimum-gap or residual-multiplicity theorem.

The direction is coherently accessible. `D_m` is the uniform Hermitian orbit
sum over exactly

```text
192*C(m,4)=8m(m-1)(m-2)(m-3)
```

constant-support permutations. A combinadic four-subset index and one of 192
local terms give a bijective reversible PREP/SELECT specification with block
normalization one. Phase labeling to the proved precision costs
`O(m^(9/2)log(1/epsilon))` SELECT calls. Hyperoctahedral subduction is not
needed merely to obtain the `D_m` eigenvalue label. Measuring that label is
still exactly likelihood blind by the source-local theorem.

The conjugation stabilizer of `D_h` is exactly `K=C_G(h)` for every `m>=4`.
The proof combines one all-rank cross-transposition noncentral witness with
the elementary maximality theorem for the perfect-matching stabilizer. Hence

```text
tK -> D_(t h t^-1)=tD_ht^-1
```

is an injective orbit coordinate for all `M=(2m)!/(2^m m!)` candidates, and
the orbit has normalization-one coherent access when an **external** candidate
permutation is supplied. The physical quotient target is not that register;
the gauge theorem below closes the naive identification.

The orbit's scalar geometry is dequantized. For a nearest two-edge matching
switch,

```text
|O_h intersect O_h'|
 =80*C(m-2,2)+192*C(m-2,3)+192*C(m-2,4),
kappa(h,h')=(m^2-5m+9)/[m(m-1)].
```

For arbitrary explicit matchings, enumerate the `O(m^4)` orbit terms and use
the constant-time two-disjoint-3-cycle membership test. More generally, every
scalar word moment of any polynomial-length charge word is a classical return
probability `Pr[g_1...g_d=e]`; the h-even trace also accepts product `h`.
Hoeffding estimates every inverse-polynomial scalar signal in polynomial
time. Pairwise fidelity, commutator scalar moments, and growing-degree scalar
word heuristics are not quantum leverage. Conditioned matrix transitions
remain open.

### Exact all-copy LCU, negativity, gauge, and two-projector boundaries

Files and experiment IDs:

```text
coset_hidden_involution_all_copy_target_lcu_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-ALL-COPY-TARGET-LCU-NO-GO

coset_hidden_involution_target_interference_negativity_barrier.py
EXP-COSET-HIDDEN-INVOLUTION-TARGET-INTERFERENCE-NEGATIVITY-BARRIER

coset_hidden_involution_matching_charge_target_gauge_trivialization.py
EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-TARGET-GAUGE-TRIVIALIZATION

coset_hidden_involution_physical_target_convolution_normal_form.py
EXP-COSET-HIDDEN-INVOLUTION-PHYSICAL-TARGET-CONVOLUTION-NORMAL-FORM

coset_hidden_involution_shared_conjugation_QSVT_lower_bound.py
EXP-COSET-HIDDEN-INVOLUTION-SHARED-CONJUGATION-QSVT-LOWER-BOUND

coset_hidden_involution_two_subgroup_projector_algebra_no_go.py
EXP-COSET-HIDDEN-INVOLUTION-TWO-SUBGROUP-PROJECTOR-ALGEBRA-NO-GO
```

The exact `BAB` factorization now closes every normalized **linear**
all-copy target LCU, not just diagonal or Hecke terms. For a basis element
`ell=(g_1,...,g_k;t)` and

```text
c_H(g,t)=#{(eps,eps') in H^2:g=eps t eps'},
```

one has

```text
tr_B(ell Z)=2^-k product_i c_H(g_i^-1,t^-1),
tr_B(ell)=1[ell^-1 in B].
```

Inside `K` the traces agree. Outside `K`, every supported local multiplicity
is one, so each basis bias is exactly `2^-k`. Thus for arbitrary coefficients

```text
|tr_B(XZ)-tr_B(X)| <= 2^-k ||X||_(group-basis L1).
```

At natural copy count, unit-L1 bias is at most `1/(64M)`. Constant bias
requires L1 norm at least `beta*2^k>=64 beta M`, factorial in `m`. This is the
exact negativity/sign resource. Standard coefficient PREP/SELECT has that
normalization and raw success at most its inverse square. This is not a
general circuit lower bound: an implicit Fourier/QSVT/polar transform may
have huge group-basis L1 without preparing the coefficients.

The physical target coordinate is gauge. Under

```text
(g_i;t)~(g_i r;t r),   x_i=g_i t^-1,
```

representative-covariant target-diagonal charge control necessarily acts as
`g_j->g_j t^-1 d t`, which becomes `x_j->x_j d`. It is exactly source-local
and likelihood blind. A useful operation must change the target coordinate.
For genuine left convolution by `(a_1,...,a_k;s)`, quotient coordinates give

```text
x_i -> a_i x_i s^-1.
```

The full normalized likelihood has the exact shared-conjugation normal form

```text
Z = 1/(4^k|K|) sum_(s in G) sum_(eps,eps' in H^k)
      (eps_1 s eps'_1,...,eps_k s eps'_k;s)
  = 1/|K| sum_s Q_s
  = M E_(s uniform G) Q_s.
```

Each conditioned `Q_s` is a product twirl with positive L1 normalization one;
the full `Z` has positive L1 exactly `M`. Generic uniform PREP/SELECT gives
`Z/M`, not a fast-forward of `Z`.

Put `P=e_A`, `Q=e_B`, and `A=QPQ=Z/M`. At least `29/32` alternative mass has
`A` eigenvalues in `[1/(2M),3/(2M)]`. A bounded degree-`D` polynomial with
constant variation from zero to `1/(2M)` obeys Markov's inequality

```text
2D^2 >= ||p'|| >= 2M beta,
D >= sqrt(M beta).
```

This is not merely a single-operator QSVT boundary. Every source-compressed
word in the two subgroup projectors satisfies

```text
Q w(P,Q) Q = (QPQ)^r,
```

so the entire ancilla-controlled two-projector query algebra is univariate
and inherits the `Omega(sqrt(M))` cost. Alternating reflections, ordinary
amplitude amplification, and two-projector word LCUs are closed. A direct
non-black-box matrix-CS transform or a genuinely third physical operator
remains open.

The 11 focused suites in this charge/target bundle pass 66 tests; the full
primitive-plus-charge focused integration suite passes 84 tests in 8.29
seconds. All artifacts were regenerated. Keep minimum-gap, residual-copy,
physical target control, structured fast-forward, matrix-polar, detector, and
speedup gates false.

**Next high-reasoning derivation:** let `A=QPQ` on the physical `Q` space and
let `D` be the normalization-one source matching charge, which commutes with
`Q`. Determine the natural source-weighted matrix quantity

```text
||[A,D]||_F^2
```

after resolving actual `(lambda,mu)` multiplicity blocks and excluding scalar
return-moment information. A useful positive result needs inverse-polynomial
mass and singular/eigenvalue separation for the noncommutative algebra
`Alg(A,D)` in a **target-changing** quotient implementation. A decisive
falsifier is exact commutation, inverse-candidate/factorial total energy, or a
classical return/kernel representation for every conditioned matrix entry.
Do not count the fixed `S_10` covariance example, regular scalar commutator
moments, or external-candidate charge access as this theorem. If positive,
the next obligation is a matrix-valued signal-processing compiler with
normalization and classical baselines; if negative, abandon charge-assisted
polar fast-forward and return to an explicit non-black-box subduction basis.

## Current High-Reasoning Result: Standard-Block Matrix Recoupling (2026-08-20)

Files:

- `coset_hidden_involution_standard_block_recoupling.py`
- `tests/test_coset_hidden_involution_standard_block_recoupling.py`
- `research/representation/coset_hidden_involution_standard_block_recoupling.json`

Experiment ID:

```text
EXP-COSET-HIDDEN-INVOLUTION-STANDARD-BLOCK-RECOUPLING
```

This pass tested whether the exact double-coset Cosine-Sine reduction secretly
scalarizes inside every `L=S_n^(k+1)` irrep. It does not. Exact character
moments found 585 nonflat or rank-deficient matrix blocks among 665 blocks with
both multiplicities at least two for `S_5`, three copies. More importantly,
the perfect-matching family has a scalable exact witness and an adversarially
useful closed form.

Let `G=S_(2m)`, let `h` be fixed-point-free, use three copies, and put the
standard representation `V=Std(S_(2m))` in all four `L` factors. Then

```text
pi^A = Inv_(S_(2m))(V^tensor4).
```

Under `K=C_G(h)=C_2 wr S_m`, the `+1` eigenspace of `h` in `V` is the embedded
standard `S_m` module `U`; the complement is the signed pair-difference
module. The three `<h>` averages retain `U` in the source factors, and the
base-sign average kills the signed target summand. Hence

```text
pi^B = Inv_(S_m)(U^tensor4).
```

For `m>=4`, both spaces have dimension four. Each is spanned by the centered
simplex fourth moment and the three metric pairings. The exact Gram and
cross-Gram matrices split under tensor-leg permutations into a two-dimensional
pair-standard sector and a two-dimensional symmetric sector. The squared
principal cosines are

```text
p_m, p_m, lambda_-(m), lambda_+(m),
p_m = (m-2)/(2(2m-1)),
lambda_- + lambda_+
  = (6m^2-19m+18)/(4(2m-3)(2m-1)),
lambda_- lambda_+
  = (m-3)(m-2)(m-1)/(4(2m-3)(2m-1)^2).
```

They are positive and nonuniform for every `m>=4`, and converge to
`{1/8,1/4,1/4,1/4}`. Dense tensor controls for `m=4,5,6` agree with the exact
formula below `1e-14` and all eight focused tests pass.

This is also a no-go for a weak hardness argument. The multiplicity transform
in this scalable matrix block is succinct: two directions are scalar and only
one explicit `2x2` generalized eigensystem remains. Matrix multiplicity,
occupied rank, and nonuniform principal angles therefore do not imply a hard
transform. The block is not naturally useful either: at degree 128 its source
fraction is below `2^-2471` and its alternative mass below `2^-2117`.

The 2026 partition/Brauer-algebra QFT does not close the natural-block problem.
Its approximation requires the loop parameter much larger than a polynomial
in the diagram-algebra dimension. Here the natural copy/tensor order is
`Theta(n log n)` while the loop parameter is only `n`; moreover arbitrary
source irreps require generalized symmetric-group Kronecker spaces rather than
one fixed standard-tensor centralizer.

The next theorem-level target is not another fixed-row block. It is to derive
the natural overlap as an explicit restriction/recoupling map

```text
Hom_(S_n)(tau*, tensor_i lambda_i)
  --> Hom_(C_2 wr S_(n/2))(tau*|K, tensor_i lambda_i^+),
lambda_i^+ = ker(rho_lambda_i(h)-I),
```

and decide whether a subgroup-chain basis makes its polar local. The decisive
falsifier is reappearance of unrestricted Kronecker multiplicity transforms,
exponential branching width, or a required diagram-QFT parameter outside its
unitary regime on constant natural mass. A positive result needs a coherent
physical basis change and normalization, not just character moments or an
abstract block diagonalization. Every detector and speedup gate remains false.

## Current High-Reasoning Result: Natural Matrix Double-Coset Polar (2026-08-20)

Files:

- `coset_hidden_involution_double_coset_polar_reduction.py`
- `coset_hidden_involution_natural_matrix_multiplicity.py`
- `coset_hidden_involution_occupied_matrix_rank.py`
- matching focused tests and `research/representation/` artifacts

Experiment IDs:

```text
EXP-COSET-HIDDEN-INVOLUTION-DOUBLE-COSET-POLAR-REDUCTION
EXP-COSET-HIDDEN-INVOLUTION-NATURAL-MATRIX-MULTIPLICITY
EXP-COSET-HIDDEN-INVOLUTION-OCCUPIED-MATRIX-RANK
```

This pass replaces the informal orbit-representative row-frame problem by one
exact homogeneous-space operator. Let `G` be the candidate group, `h` the
reference involution, `H=<h>`, `K=C_G(h)`, `M=[G:K]`, and use `k` coset-state
copies. Put `L=G^k x G` and

```text
A={(r,...,r;r): r in G},
B={(eps_1 r,...,eps_k r;r): r in K, eps_i in H}.
```

The physical tuple basis is `L/A`; the full hidden-involution/coset-tuple
source basis is `L/B`. If `V_A,V_B` are normalized right-coset embeddings into
`C[L]`, then

```text
D = V_A^* V_B = I_incidence / sqrt(2^k M).
```

The source synthesis is `sqrt(M) D`, so it has the same polar. The missing
physical compiler is exactly the Cosine-Sine alignment between the right-`A`
and right-`B` invariant subspaces. Both subgroup factorizations/reflections are
efficient for the symmetric/perfect-matching family, but this alone does not
help: on at least `29/32` of alternative mass the principal cosines of `D` are
`Theta(M^-1/2)`, so generic alternating-reflection phase resolution still costs
`Omega(sqrt(M))`.

The transform is genuinely matrix-valued, not a scalar Gelfand/spherical
transform. In an `L` Fourier block its physical multiplicity is

```text
Inv_G(nu_1 tensor ... tensor nu_k tensor tau),
```

while its source multiplicity is the corresponding `B`-fixed space. Even four
standard `S_n` factors have diagonal invariant multiplicity four for `n>=4`.
That finite witness alone would be weak, so the next theorem proves natural
mass.

For `m_B(pi)=dim(pi^B)`, the fraction of `Ind_B^L(1)` in blocks with
`m_B<=T` is at most

```text
delta_low <= T (sum_(lambda|-n) d_lambda)^(k+1) / |L:B|.
```

Robinson--Schensted gives the exact identity `sum d_lambda=I_n`, the number of
involutions in `S_n`. At `k=ceil(log2(64M))`, choosing
`T=|S_n|^(k/4)` makes `delta_low` super-exponentially small. Alternative mass
is the exact size bias of the unnormalized synthesis eigenvalue `x`, so at
least `29/32-(3/2)delta_low` alternative mass reaches these huge source blocks.

They are not mostly kernel. The exact source moment

```text
E[(x-1)^2] = eta = (M-1)/2^k
```

bounds the total kernel fraction by `eta<=1/64`. Any block whose occupied CS
rank `r` is at most `m_B/2` contributes at least half its source dimension to
the kernel, so all such blocks occupy at most `2eta`. Therefore alternative
mass at least

```text
29/32 - (3/2)(delta_low + 2 eta)
```

lies in blocks with `r>|S_n|^(k/4)/2`. The stored minimum is
`0.86094`; the degree-128 rank threshold has log2 greater than `64990`.

Research consequence: scalar spherical labels, low-multiplicity trimming, and
the claim that large multiplicity is mostly kernel are all closed on constant
natural mass. This is still not a hardness theorem. QFTs routinely act on huge
rank spaces, and no lower bound is proved for a succinct partition-algebra,
recoupling, or matrix-CS basis change.

The next and only worthwhile positive compiler task on this chain is:

1. Derive an explicit basis and block formula for the occupied overlap between
   `Inv_G(nu_1 tensor ... tensor nu_k tensor tau)` and the `B`-fixed space.
2. Search for a recursive/partition-algebra CS transform or an exact
   fast-forward of the two subgroup reflections that preserves the physical
   normalization.
3. Kill it if every recursion reintroduces generic symmetric Kronecker data,
   factorial normalization, or exponential orbit-copy enumeration.
4. A positive result must include coherent input/output labels, precision,
   garbage uncomputation, and a matched classical access model. Large rank or
   passing finite controls alone is not progress.

No binary detector, rigid-GI algorithm, code-equivalence algorithm, or speedup
is claimed.

## Current High-Reasoning Result: All Simple Surface Targets Mix (2026-08-20)

Files:

- `self_dual_wreath_separating_surface_target_mixing.py`
- `tests/test_self_dual_wreath_separating_surface_target_mixing.py`
- `research/representation/self_dual_wreath_separating_surface_target_mixing.json`

Experiment ID:

```text
EXP-CODE-SELF-DUAL-WREATH-SEPARATING-SURFACE-TARGET-MIXING
```

The marked-word search had left open whether a target carried by a surface
relation could retain a high-dimensional `S_n` character bias. This pass proves
that every certified simple curve on a closed orientable surface is a classical
no-go, uniformly over growing genus.

For the product of `h` independent commutators, its density relative to uniform
measure is

```text
A_h(x) = sum_rho chi_rho(x) / d_rho^(2h-1).
```

For a separating simple curve splitting the surface into genera `a,b`, the
exact target density is

```text
f_ab(x) = A_a(x) A_b(x^-1) / zeta_G(2a+2b-2).
```

Writing `A_h=1+sgn+r_h` for `G=S_n` gives

```text
||r_h||_2^2 = zeta*_Sn(4h-2),
TV(f_ab, Uniform(A_n))
 <= [2 eps_a + 2 eps_b + eps_a eps_b + (Z-2)] / (2Z),
eps_h = sqrt(zeta*_Sn(4h-2)),  Z = zeta_Sn(2a+2b-2).
```

The worst genus is `a=b=1`; fixed-exponent Witten-zeta tails imply an
`O(1/n)` genus-uniform bound. For a nonseparating simple curve on genus
`g>=2`, summing over its conjugate handle gives the exact density

```text
f_nonsep,g(x)
 = [sum_rho |chi_rho(x)|^2 / d_rho^(2g-2)] / zeta_G(2g-2),
TV(f_nonsep,g, Uniform(S_n)) <= t/(2+t),
t = zeta*_Sn(2g-2).
```

This is `O(n^-2)` uniformly over growing genus. Every normalized nontrivial
character expectation is at most twice the corresponding TV distance. Exact
controls cover `S_3` through `S_8`, three genus choices in each class, plus a
direct Frobenius count check; all 54 density controls and the direct check pass.

Research consequence: certified contractible, separating, nonseparating, and
unconditioned surface-boundary targets cannot support the needed asymptotic
marked-character signal. This is a target-class cut theorem, not a proof about
all marked words. Self-intersecting curves, genuinely non-surface words, and
unclassified interleavings remain outside scope. There is no natural component
`M4` lower bound and no speedup claim.

Next high-reasoning task: classify pressure-saturating marked relators by
surface topology and isolate the first self-intersecting target family that is
not reducible to this theorem. Then derive or falsify a character-mixing bound
for that family. A useful positive result must exhibit a growing-word family
whose normalized target character survives after scalar pressure and all
known classical word-measure bounds; another finite small-`n` bias is not
progress.

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

## Branch-Polar Access And Concentration Boundary (2026-08-24)

Four linked theorem modules close the current branch-polar pass without
claiming an algorithm or a general decoder lower bound.

1. `self_dual_wreath_branch_character_whole_sum_path_erasure_boundary.py`
   proves that the local cyclic compiler can assemble the complete coefficient
   sum when the relative group element is explicit, but erasing that path by
   the canonical uniform coisometry exposes amplitudes
   `sigma_j(C)/sqrt(|G|)`. Alternating-reflection/QSVT unpreparation therefore
   costs `Omega(sqrt(|G|))` on order-one retained singular sectors. An exact
   orthogonal-range classifier bypass shows this is architecture-scoped. The
   remaining constructive escape is a coherent natural range classifier or an
   equivalent direct Fourier multiplier/polar.
2. `self_dual_wreath_branch_character_raw_polar_matched_filter_boundary.py`
   proves that the native raw field and locally polar-completed field have a
   positive-contraction cross map. The unwhitened matched-filter correct
   probability is bounded by the already-vanishing raw/polar overlap. For
   global polar whitening,
   `sqrt(P_Q)<=sqrt(P_match)+sqrt(kappa R)`, where
   `kappa=||C_K||^2` and `R` is the normalized polar Gram residual. Polynomial
   raw domination would kill this decoder; it is not a positive completion
   gate. The actual physical PGM remains outside scope.
3. `self_dual_wreath_branch_character_raw_concentration_central_fourier_bridge.py`
   corrects a tempting but false bridge. The existing noncentral orientation
   block `F_nu` does **not** control the actual right-convolution multiplier.
   With `Q_nu=E^*Pi_nu^(R)E`, the exact identity is

   ```text
   M_nu^*M_nu = |G|/d_nu^2 I_(d_nu) tensor Q_nu,
   ||C_K||^2 = max_nu |G| ||Q_nu||/d_nu^2.
   ```

   The surviving bridge is trace-only:
   `Tr(Q_nu)=d_nu Tr(F_nu)` and
   `Tr(Q_nu)/D=Tr(D_nu)`, exactly the native Fourier-sector mass. On the
   natural high-dimensional bulk `d_nu>sqrt(n!)/p(n)`, concentration is below
   `p(n)^2`; multiplying by the polar Gram residual tends to zero (the live
   `n=512` log2 upper bound is about `-807.06`). Thus the high-dimensional
   `1-o(1)` mass cannot supply the whitening rescue. At this stage coherent
   alignment with the low-dimensional tail was the sole remaining escape.
4. `self_dual_wreath_branch_character_sector_resolved_whitening_no_go.py`
   closes that escape without a global operator-norm assumption. Fourier
   inversion expresses each correct-label correction amplitude as a partial
   trace. The exact raw multiplier bound cancels the irrep dimension:

   ```text
   ||A_E,nu||_F^2/D <= r_nu,
   P_E <= p(n) sum_nu r_nu <= p(n) R.
   ```

   Therefore
   `P_polar<=(sqrt(raw/polar overlap)+sqrt(p(n)R))^2`. At
   `k=ceil(3log2(n!))+2`, both annealed terms vanish, global-distinct
   conditioning costs `1+o(1)`, and Markov gives source-typical failure. The
   live `n=512` partition-weighted correction has log2 upper bound about
   `-878.97`, and the final expected success upper bound is about `1.51e-36`.
   This terminates `polar(C_J)^*` on the native raw ensemble. It does not reject
   the actual joint-character multiplicity PGM.

The four experiment IDs are:

```text
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-WHOLE-SUM-PATH-ERASURE-BOUNDARY
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-RAW-POLAR-MATCHED-FILTER-BOUNDARY
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-RAW-CONCENTRATION-CENTRAL-FOURIER-BRIDGE
EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-SECTOR-RESOLVED-WHITENING-NO-GO
```

**Next high-reasoning task:** return to the genuinely different physical
joint-character PGM. Its Schur multiplicity blocks are
`D_nu=r/(qD) I_r tensor W H_nu W^*`, and the physical analysis polar is
`A_nu D_nu^-1/2`. Determine whether the scalar orientation kernel `H_nu`
admits a natural bulk inverse, a representation-ring transform, or a new
state-weighted no-go. Do not reuse `polar(C_J)` under another name, and do not
identify `Q_nu` with `F_nu`. Keep `actual_physical_pgm_rejected` and
`speedup_claim_allowed` false until this distinct multiplicity route is
resolved.

Focused validation at this checkpoint: the sector no-go has seven passing
tests across three finite controls and a live JSON artifact. The combined affected chain and repository
validation are listed in the final checkpoint notes for this session.

## Physical Orientation Hash Normalization Boundary (2026-08-24)

`self_dual_wreath_orientation_kernel_hash_normalization_no_go.py` charges the
normalization omitted by the existing orientation-kernel hash-thinning route.
In orientation coordinates, the canonical physical analysis map has

```text
N_nu^*N_nu = I_(d_nu) tensor H_nu/(q dim(C)).
```

For a full-rank affine fiber `S` of density `p` and size `s=pq`, even after
conditioning on successful hash acceptance,

```text
N_(nu,S)^*N_(nu,S) = I_(d_nu) tensor H_(nu,S)/(s dim(C)).
```

The kernel mean is exactly tied to physical target mass:
`m_nu=Tr(H_nu)/q=dim(C)Tr(D_nu)/d_nu^2`. Grant the hash proposal its ideal
premise `H_(nu,S)<=(1+epsilon)m_nu I`. On the natural high-row event
`d_nu>sqrt(n!)/p(n)` and at `q>=n!`, the canonical singular scale is at most

```text
sqrt(1+epsilon) p(n)/(n! sqrt(p)).
```

Generic bounded-polynomial scalar whitening therefore needs degree
`Omega(n! sqrt(p)/p(n))`, still factorial for every inverse-polynomial hash
density. At `n=512`, the live log2 singular upper bound is `-3766.9784...` and
the generic degree lower bound is `3766.9492...`.

Uniform full-rank affine hashes preserve each orientation's inclusion
probability exactly; because the hash projector commutes with diagonal
isotypic resolution, the conditioned target law is preserved in expectation.
Three finite `S3/S4` controls verify the conditioned Gram, polar scale
invariance, kernel-mean identity, and exact full-rank hash mass transfer.

This kills **hash thinning plus canonical scalar QSVT/amplitude whitening**.
It does not kill hash thinning as a preprocessing step for a genuinely
structured direct polar, nor the actual physical multiplicity PGM under a
different access architecture.

Experiment ID:

```text
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-NORMALIZATION-NO-GO
```

## Orientation-Kernel Character Tensor Boundary (2026-08-24)

`self_dual_wreath_orientation_kernel_character_tensor_boundary.py` derives
the exact representation-theoretic tensor network underlying the remaining
physical orientation kernel. For source pair `(lambda_i,mu_i)`, define

```text
Q_i(x,y) = [[d_mu chi_lambda(xy), chi_lambda(x)chi_mu(y)],
            [chi_lambda(y)chi_mu(x), d_lambda chi_mu(xy)]].
```

Then the physical scalar kernel is exactly

```text
H_nu[e,f] = 1/(d_nu |G|^2) sum_(x,y in G)
              chi_nu(xy) product_i Q_i(x,y)[e_i,f_i].
```

This identifies `H_nu` as a `|G|^2`-term sum of tensor-product operators on
the orientation qubits. The summand is invariant under simultaneous
conjugation, but the exact pair-orbit count is

```text
orb_2(G) = |G|^-1 sum_z |C_G(z)|^2.
```

For `S_n`, this is `sum_(alpha partition n) z_alpha >= n!`, so explicit
pair-orbit enumeration remains factorial even after exhausting this symmetry.
Exact `S3/S4` controls also falsify three universal shortcuts: `H_nu` is not
generally XOR-translation invariant, the Boolean Walsh transform does not
generally diagonalize it, operator-Schmidt ranks can be maximal across
orientation cuts, and the local `Q_i(x,y)` matrices do not share a fixed
one-qubit eigenbasis.

These controls are ansatz falsifiers, not asymptotic tensor-network lower
bounds. The remaining constructive target is a globally coherent contraction
of this `S_n x S_n` character network, equivalently an internal
Kronecker/Racah multiplicity transform. Efficient character evaluation, an
efficient symmetric-group QFT, and explicit simultaneous-conjugacy orbit
listing do not by themselves provide that transform.

Experiment ID:

```text
EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-CHARACTER-TENSOR-BOUNDARY
```

**Next high-reasoning task:** audit the exact capability boundary of known
Schur/Clebsch-Gordan transforms before deriving another compiler. In
particular, determine from the primary literature whether the finite-group
Clebsch-Gordan construction of Bacon-Chuang-Harrow, the high-dimensional
Schur transform, or the Kronecker-projector algorithms provide a coherent
multiplicity-basis transform for arbitrary `S_n` irrep tensor products in the
input model required here. Distinguish isotypic projection and normalized
Kronecker-coefficient estimation from multiplicity-basis resolution. If none
does, formulate the unresolved contraction as a precise oracle/compiler
problem and test a globally coherent Racah network without intermediate
measurements. Keep the physical PGM, arbitrary-circuit lower bound, classical
separation, algorithm, and speedup gates false.

Pause validation checkpoint: the new physical-PGM dependency chain passes 48
tests, repository compilation and JavaScript syntax checks pass, `qsearch.py
validate` reports zero issues, and `git diff --check` passes. A broad pytest
run was stopped after 88 tests because eight older clean-registry writer tests
had already failed. The first isolated defect is confirmed mechanical:
`write_character_decoder_search_report` returns immediately after writing its
artifact, leaving its imported `upsert_scaling_run` unreachable/unused. The
other failures have the same missing-upsert symptom and are enumerated in
`research/MECHANICAL_FOLLOW_UP_PLAN.md`. They predate and are outside this
character-tensor theorem pass; do not infer that the repository-wide suite is
green.

## Schur-Companion Known-Transform Scope Boundary (2026-08-24)

`self_dual_wreath_schur_companion_transform_scope_boundary.py` completes the
primary-literature capability audit requested above and falsifies the precise
hypothesis that the published Schur/QFT/CG plus invariant-projector stack
already contains the missing orientation-polar compiler.

In a fixed target sector, write the encoded joint-companion source space as

```text
K_nu = direct_sum_e K_(nu,e),   K_(nu,e)=B_(nu,e)M_(nu,e).
```

The cited results provide Schur coordinate changes, source/target labels, and
supplied-label invariant membership reflections. Their proved interface lies
in the branch-preserving algebra

```text
A_br = direct_sum_e End(K_(nu,e) tensor W).
```

This remains true under arbitrary coherent composition inside the access
model: products, adjoints, label control, workspace extension, and selected
workspace top blocks still commute with every branch projector `Z_e`. By
contrast, for

```text
H_nu[e,f] = Tr(E_(nu,e)E_(nu,f))/d_nu,
```

any cross entry forces `H_nu^(+/2)` outside `A_br`, because
`H_nu=((H_nu^(+/2))^+)^2`. Three exact `S3/S4` controls verify cross blocks in
both operators, the reconstruction identity, and branch-algebra closure. The
existing target-uniform Plancherel tensor-covering theorem makes cross overlaps
density one on balanced natural orientation pairs, and the joint-sector
theorem places `1-o(1)` natural mass on high-dimensional target rows.

The literature boundary is exact and deliberately narrow:

- BCH and the corrected high-dimensional algorithm implement Schur--Weyl
  transforms and GT/SYT or one-box Pieri `F`-moves, not arbitrary internal
  `S_n` Specht Kronecker/Racah transitions.
- The Kronecker and plethysm `#BQP` constructions identify dimensions of
  invariant-projector images; they do not expose a coherent multiplicity basis
  or state-dependent cross-branch transition amplitudes.
- The efficient `S_n` QFT supplies carrier coordinates, not an internal
  multiplicity multiplier.

Successor correction: the closure statement above applies only while the
computation stays inside `A_br`. The already-compiled physical-invariant
interface permits a detour

```text
decode branch e -> block-encode E_f -> encode branch f,
```

whose signal block is `J_f^*J_e` with LCU normalization one. Coherent GPE also
compiles each addressed pair polar directly. Thus the raw cross-map query is
not open; the companion-only algebra theorem still explains why it cannot be
obtained without leaving that algebra.

The surviving constructive target is global: assemble all operator-valued
cross metrics and pair phases into the positive address-transition kernel,
with polynomial full-kernel normalization and an inverse-polynomial useful
spectral window on natural mass.

No new entangling companion circuit, noncommuting Racah network, multi-round
branch relocation, or character-retaining decoder is ruled out. No approximate
arbitrary-circuit lower bound, high-dimensional hidden-label information
theorem, physical PGM, classical separation, algorithm, or speedup is claimed.
`speedup_claim_allowed` remains false.

Experiment ID reserved for mechanical wiring:

```text
EXP-CODE-SELF-DUAL-WREATH-SCHUR-COMPANION-TRANSFORM-SCOPE-BOUNDARY
```

The next section records the resulting oracle construction and global
phase-only falsifier.

## Addressed Cross Maps And Pair-Polar Gram Boundary (2026-08-25)

`self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.py` advances the
cross-branch frontier and corrects the raw-access part of the previous target.
For branch inclusions `J_e:M_e->X`, use the physical Schur/Bell interfaces and

```text
E_f = (I + (2E_f-I))/2.
```

One Hadamard-LCU ancilla around the supplied-label invariant reflection gives
the exact addressed signal block

```text
B_f J_f^* E_f E_e J_e B_e^* = B_f J_f^*J_e B_e^*
```

at normalization `alpha=1`. The coherent query masks `(e,f)` control which of
the `O(n log n)` factor registers participate in each diagonal `S_n` action;
the circuit never enumerates the `4^k` possible orientation pairs. The
existing GPE row-reassociation theorem then supplies the direct support polar
`U_(f<-e)=polar(J_f^*J_e)` without inverse-carrier amplification.

This does **not** normalize the full dense address-transition operator.
The tempting phase-only global kernel

```text
K_pol[e,e]=I,       K_pol[e,f]=U_(e<-f)
```

is a Gram operator only when the pair connection is flat. In any PSD Gram
factorization, a unitary off-diagonal overlap forces the corresponding branch
isometry ranges to coincide; consequently every loop product must be the
identity. Conversely, a flat family has a common-range Gram factorization.

The exact regular-`S3` transposition triangle has holonomy spectrum
`{1,-1,-1}`. Its physical overlap Gram retains the nonflat metric `1/2` and
has spectrum

```text
{0,0,0,0, 3/2,3/2,3/2,3/2, 3}.
```

Replacing all nonzero cross metrics by their pair polars gives

```text
{-1,-1, 0,0, 2,2,2,2, 3},
```

so the phase-only kernel is indefinite. Under `k` tensor copies the negative
eigenvalue multiplicity is `(3^k-(-1)^k)/2`, asymptotically one sixth of the
three-branch coefficient space. The witness embeds in fixed-point-free
involutions for every even `n>=6`, but no positive natural Plancherel mass for
this chart is claimed.

The corrected bottleneck is the **operator-valued positive metric assembly**:
retain `|J_f^*J_e|` together with the GPE pair phases, construct the full PSD
address kernel at polynomial normalization, and prove a useful natural
spectral window. Entry-query `alpha=1` is not full-matrix `alpha=1`.

No global polar, physical PGM, natural-mass holonomy obstruction, hidden-label
information theorem, decoder, classical separation, algorithm, or speedup is
proved. `speedup_claim_allowed` remains false.

Experiment ID reserved for mechanical wiring:

```text
EXP-CODE-SELF-DUAL-WREATH-ADDRESSED-CROSS-MAP-PAIR-POLAR-GRAM-BOUNDARY
```

**Next high-reasoning task:** construct or falsify a coherent global PSD metric
assembly from the addressed raw cross-map oracle. The construction must expose
the address-transition PREPARE/SELECT normalization, retain the positive
operator factors rather than only pair phases, resolve nonabelian holonomy,
prove an inverse-polynomial useful spectral window on positive natural PGM
mass, and state what information its output carries about the hidden
involution. A finite S3 chart or alpha-one entry query is not enough.

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
