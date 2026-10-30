# Six-Agent Constructive Direction Challenge

30 October 2026. Status: reviewed mathematical progress and scoped negative
results; no new accepted quantum candidate, speedup, or native application.
The active research goal remains open. All six agents completed and were
closed. These are automated independent checks, not human peer review.

## Assignments And Outcomes

| Agent | Focus | Result after challenge |
| --- | --- | --- |
| James the 2nd | Classical succinct-stabilizer literature and constructive residuals | An all-fixed-anchor extension-field procedure; an orbit-sum residual family, not evidence of hardness. |
| Lagrange the 2nd | New power-sum geometry versus actual Rees SDE | The equation family, geometric promises, and rank-dependent cost do not transfer automatically. |
| Carson the 2nd | Native application of the residual orbit-sum stabilizer | Terminal-cost symmetry need not be a recurrence symmetry or useful dynamical quotient. Several explicit classical structures remain. |
| Dewey the 2nd | Quaternion direct quotient/Fourier receiver | Exact source-specific direct-success bound; corrected coefficient-state access and unit-bound attribution. Independently verified the parent's general cardinality proof. |
| Rawls the 2nd | Independent native direction and diffusion comparison | Gaussian-LCHS suggested as a pivot; independent review supports the parent's polynomial classical baseline in a specified window, with essential observable and precision repairs. |
| Kepler the 2nd | Adversarial review of power-sum and all-anchor arguments | Corrected a false extra nonzero-output blocker; confirmed the all-anchor argument with randomness, field, and acceptance qualifications. |

Agent IDs, in the same order:

```
01a18b05-cd08-7aa3-8bb2-3c6c67073af6
01a18b05-cd9a-7142-881e-6afbb131b8aa
01a18b09-ba1d-7632-b2b4-f0de76f9a036
01a18b09-bab0-7921-ba07-18ca30d23fdc
01a18b09-bb25-7110-8ee5-2a768f2b9a6c
01a18b0d-c08c-78a2-8fc4-1b13e06acf2e
```

## What Survived

1. [All fixed anchors](../../ITERATED_QUADRATIC_JET_FILTER.md): d extension
   anchors recover the universal F_p jet kernel with a charged error
   probability; fresh generator PIT can certify equality with the true
   stabilizer. Every sampled upper group is sound even on unlucky probes.
   This is a proof-level classical algorithm, not an implemented extension
   backend. The residual orbit-sum question remains mathematically open,
   but its natural application and classical resistance are unestablished.
2. [Diffusion baseline](../../FOKKER_PLANCK_CLASSICAL_BASELINE.md): an
   explicit Euler/Girsanov/Pinsker bound removes an exponential Gronwall
   dependence for bounded smooth-periodic drift. A rounded-history
   comparison pays finite precision. Reversibility reduces the normalized
   overlap to sqrt(p_RP*p_PR) when BOTH restricted-Gibbs samplers are
   supplied. This is a scoped use of standard methods, not a new stochastic
   algorithm or a refutation of every quantum diffusion advantage.
3. [Quaternion unit bound](../../QUATERNION_COMPACT_ORBIT_SOURCE.md): the
   general |O^1|<=max(120,16d^2) statement survives by a direct deduction
   from finite SU(2) classification and cyclotomic degree, rather than
   the earlier overbroad attribution to Hawk.

## What Did Not Survive

- [Power-sum transfer](../../POWER_SUM_GEOMETRY_TRANSFER_AUDIT.md): no new
  solver improvement follows for arbitrary vector-weighted same-degree
  Rees equations. Nonradical examples violate the geometric premise;
  even regular examples can have degree g^r. This is not a lower bound
  on SDE. IMPORTANT correction: when Cafure--Matera's actual geometric
  promises hold, its smooth-output construction already excludes zero
  in the homogeneous degree>=2 case. The initial extra blocker was
  withdrawn, not silently retained.
- [Direct quaternion quotient](../../QUATERNION_DIRECT_QUOTIENT_FILTER.md):
  Parseval gives p_good<=|H|*max(P_I), which is N^(-Omega(N)) for the
  specified broad finite coefficient laws. Ordinary amplification of
  that marked event loses to the named exponential-time/space SVP
  comparator. This is not a full-record decoder lower bound. Approximate
  preparation adds its trace-distance error to the probability bound.
- Orbit-sum application: S composed with R minus S equals r composed
  with R^p minus r. S is not generally a dynamical invariant. Commuting
  recurrence symmetries, low-degree coboundaries and additive flows must
  be checked before promoting a native interpretation.
- Diffusion pivot: PDE grid dimension, a loose exponential classical
  upper bound, or avoided postselection do not establish a major
  separation. Periodic wrapping need not be smooth; restricted initial
  sampling is not free; small additive error is not relative rare-event
  accuracy. No new quantum subsystem is justified by this comparison.

## Review Repairs Worth Preserving

The all-anchor acceptance guarantee is unconditional Monte Carlo error,
not posterior confidence after PASS. An infrastructure abort does not
prove strict subgroup containment. Extension-field coefficients must be
expanded over F_p; computing an E-linear kernel changes the problem.

The diffusion endpoint probability and normalized overlap have different
normalizations. Bidirectional sampling repairs the comparison without a
partition-ratio oracle. Polynomial precision BIT LENGTH is the contract;
tiny time can require exponentially fine spacing. Region grids refine
the fixed input rather than changing it. Radial Hessian bounds include
tangential curvature, and walls incur their own costs.

The quaternion states in the quotient test are independent pure
coefficient states, not coefficients magically stripped from overlapping
packets. The gamma marginal is classically reproducible, not the whole
Fourier record. General unit finiteness uses all real places before
injecting the already finite group into one SU(2).

## Changed Files And Verification

New research notes: POWER_SUM_GEOMETRY_TRANSFER_AUDIT.md,
FOKKER_PLANCK_CLASSICAL_BASELINE.md, QUATERNION_DIRECT_QUOTIENT_FILTER.md,
and this review. Extended ITERATED_QUADRATIC_JET_FILTER.md and
QUATERNION_COMPACT_ORBIT_SOURCE.md. Updated AGENT_HANDOFF.md,
RESEARCH_PRIORITY_DECISION.md, and MECHANICAL_FOLLOW_UP_PLAN.md.

New tests: test_power_sum_transfer_scope.py (11),
test_fixed_anchor_scope.py (4), test_diffusion_classical_budget.py (14).
Extended test_quaternion_pip_scope.py with three controls: numerical
cyclotomic bound, exact native quotient/complete Fourier marginal,
and the preparation-error caveat. Total: 32 new bounded controls.

Final selected replay:

```
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -B -m pytest -q -W error -p no:cacheprovider \
  tests/test_power_sum_transfer_scope.py tests/test_fixed_anchor_scope.py \
  tests/test_diffusion_classical_budget.py tests/test_iterated_quadratic_jet.py \
  tests/test_power_sde.py tests/test_power_sde_budget.py \
  tests/test_rees_full_grade_budget.py tests/test_random_column_power_sde.py \
  tests/test_random_column_rees_budget.py tests/test_quaternion_pip_scope.py
```

Result: 392 passed in 6.50s. Four touched test files passed py_compile;
all 12 site JavaScript files passed node --check. qsearch.py validate:
valid=true, issues=[], eight candidates. Not a full repository suite,
Lean replay, production solver execution, or quantum experiment.

The 13 registry JSON files retain aggregate SHA256
79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd
(sorted filenames, then each filename's bytes followed by file bytes).
No production CLI, UI, registry admission, commit, or push was initiated
by this pass. Concurrent checkpoints 9232b813 and 561f341e were observed
and preserved; the latter already contains some earlier work in this
round. An empty diff for those files does not mean this work disappeared.

## Next Research Gate

Do not turn this collection of scoped filters into another generic
barrier engine. A next constructive pass should start with one actual
native task and a proposed decoder or reduction that solves it. For the
existing Rees residual, demonstrate why recovering the orbit-sum
stabilizer solves that task before extending its backend. For quaternion
records, give a specified weighted-sum contraction AND reconstruction
step, not only a measurement. A diffusion exception must identify which
paid hypothesis of the classical baseline fails and why the quantum
method still has polynomial resources. Failure to find such a route is
an unresolved research choice, not a reason to fabricate a candidate.
