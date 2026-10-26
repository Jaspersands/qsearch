# Stronger Classical Sampling On The Exact Ternary Inputs

2026-10-20. Actual mature classical backends, bijective encoding and native
witness replay. No asymptotic dequantization, independent backend proof audit,
or quantum speedup claim. The count/planting consequence is a LOCAL DERIVATION,
REVIEW PENDING, conditional on the preceding decoder/error premise.

## Research Question And Decision

Does the signed-trine sampler route survive stronger classical methods than
random rejection or the old one-second Z3 search? On the two saved finite
inputs, there is now an EXACT classical uniform sampler: complete SAT-model
enumeration followed by uniform index selection. The old timeout must not
serve as evidence of hardness. This does not settle growing-instance sampling.

The inputs are unchanged dv3/dc6 signed-socket constraints

    J_e+sum_i H_(i,e)*x_i !=0 mod3,  x_i in F3.

Original matrices, offsets and source seeds come directly from the prior
source-bound artifact. No SAT conditioning, planted witness, offset reroll,
gauge fixing or removal of parallel-socket cancellations is used.

## Why The CNF Samples The Correct Distribution

For each ORIGINAL spin i, introduce three Boolean flags b_(i,0..2) with
exactly one true. Each forbidden assignment to an aggregated native form's
at most three variables gets one clause. A zero form with offset zero yields
an empty clause; a vacuous form does not acquire a fabricated constraint.

There are no auxiliary variables. Complete CNF models and native solutions
are in BIJECTION, not just equisatisfiable. To reduce hashing support, sample
the first TWO flags of EVERY spin:10 maps to0,01 to1,00 to2. The third flag
is uniquely forced. Thus projected Boolean solutions are still in bijection
with ALL original spins. Unused/gauge spins retain all three values; sampling
a quotient without a uniform lift would be a different distribution.

Tests exhaust every Boolean assignment for every two-spin affine predicate,
plus a multi-constraint three-spin control, checking native counts and
projection multiplicity independently. Every actual backend sample replays
the unchanged ternary constraints inside the worker AND again in the parent.

## Two Existing Classical Methods, Not A New Sampler Invention

[UniGen](https://github.com/meelgroup/unigen) supplies an established
hashing-based almost-uniform method. The
[Python binding](https://pysathq.github.io/docs/html/api/allies/unigen.html)
allows a projection set. The test uses the actual native library, not a
unit-cost SAT oracle. Counting epsilon, counting confidence delta and sampling
kappa are recorded separately. Counting epsilon is NOT output TV accuracy.
The pass does not assert arbitrary-TV or joint-IID guarantees for this binary.

[PicoSAT through pycosat](https://pypi.org/project/pycosat/) independently
enumerates complete CNF models. Only after FULL iterator exhaustion is its
pool used for exact uniform index selection. All models are natively checked
and uniqueness is enforced. Its cost includes solving, verifying and storing
EVERY solution; this is generally exponential, not a scalable-count oracle.

The pycosat documentation explicitly warns that a propagation-limited
iterator may stop before exhausting models. Therefore this implementation
does NOT set a propagation limit. A model cap or outer wall timeout returns
UNKNOWN with NO samples from the visited prefix. A partial SAT enumeration
is not a uniform pool. A completed empty pool is solver-reported UNSAT, not
an independently checked proof certificate.

Both backends run in isolated child processes with charged outer wall time.
Native C++ exits, unavailable runtimes, malformed protocol and timeouts remain
UNKNOWN; partial sample batches are never salvaged as successful experiments.
Solver output cannot change the original input or admit a candidate.

## Live Same-Input Results

| Original input | UniGen | Complete PicoSAT pool |
|---|---|---|
| V16,M32,seed711 |128 valid samples; reported count67; ~0.30s outer wall |67 solutions;128 exact-pool samples; ~0.073s |
| V32,M64,seed712 |30s timeout; UNKNOWN |10,092 solutions;128 exact-pool samples; ~8.60s |

These are one-run timings, not asymptotic fits or hardware-normalized quantum
comparisons. UniGen ran under the machine's existing x86_64 Python/Rosetta;
PicoSAT ran in the existing native research Python. No quantum receiver was
run on these inputs. Versions, binary hashes, encoding sizes, requested
samples, seeds, complete counts, pool storage and unknown outcomes are saved.

The exact-pool statement is conditional on solver correctness, full completion
and independent uniform index coins. The live seed gives a reproducible PRNG
transcript, not a proof of physical randomness. Unconditional runtime-capped
algorithms also have an ABSTAIN outcome. UniGen's empirical sample histograms
would not certify its output law; the report explicitly separates those.

At V32 the exact pool occupies322944 native trits before runtime overhead.
The expected count grows as(4/3)^V. Enumerating that many outputs cannot be
called an asymptotic polynomial algorithm. Finite success cuts weak benchmark
claims, not the conditional large-instance quantum mechanism.

## A Stronger Theoretical Classical Counting Consequence

For fixed H, let Z_J be the NUMBER of valid native spin assignments and let

    Zbar=E_uniform_J Z_J=3^V*(2/3)^M,    R_J=Z_J/Zbar.

This mean is independent of H, including dependencies and parallel sockets.
The preceding unconditional reduction's unnormalized comparison vector has
squared norm EXACTLY R_J. Its normalized actual state a_J therefore obeys

    (sqrt(R_J)-1)^2 <= ||a_J-b_J||^2.
    E_J (sqrt(R_J)-1)^2 <=2*delta.                       (1)

Here delta is the SAME offset-INDEPENDENT coherent decoder's mean word error on that actual code,
not a SAT timeout, a tree support rank or a fitted finite-size number.
For0<eta<=1, a relative deviation |R_J-1|>eta requires
|sqrt(R_J)-1|>=sqrt(1+eta)-1. Consequently

    Pr_uniform_J[|Z_J/Zbar-1|>eta]
        <= min(1,2*delta/(sqrt(1+eta)-1)^2).              (2)

Thus IF the known random-code decoder theorem and the local convergence/
reduction derivations give E_H delta_H->0, outputting the simple ANNEALED MEAN
is already a polynomial classical relative-count estimator on most ORIGINAL
inputs for every fixed eta>0. Rounding its rational output to an integer has
vanishing relative effect here. No quantum algorithm is needed to compute
that predictor. Do NOT promote approximate-count estimation itself as a
quantum advantage in this certified asymptotic regime.

This is conditional mathematical inference, not a new finite-N error bound,
an all-instance counter, a prefix-conditional model counter or a novelty claim.
The saved16/32 exact counts are two fixed inputs, NOT evidence proving (2).

## Quiet Planting Is Not A Prescribed-Input Sampler

Generate x uniformly, generate y uniformly from{1,2}^M, then set
J=y-H^T x. The resulting JOINT generator has

    P_planted(J)/P_uniform(J)=R_J,

and conditional x given J is indeed uniform on its solutions. Equation(1)
and Cauchy--Schwarz give

    TV(P_planted(J),P_uniform(J))
       =E_uniform |R_J-1|/2 <= min(1,sqrt(2*delta)).

This does not provide x for a GIVEN independent J. Sampling the right joint
distribution does not give its conditional sampler for free. Gauge-adjusting
a planted offset to a prescribed one first requires matching its syndrome;
that is precisely the missing conditioning problem, not ordinary row solving.
An independent finite joint census verifies the planting/count identity.

Nor does count concentration make spins IID. The complete pools provide
exact prefix marginals: for the32-spin input the first four spins are at TV
18607/136242 (about0.137) from flat IID, despite its total count being near
the annealed mean. At16 spins the first four have TV17/27. A self-reduction
must count the actual PREFIX-conditioned problems, whose ensemble and arities
have changed; it cannot reuse the unconditioned mean at every step.

## Scope Audit And Falsifiers

- The earlier native-frequency block-walk no-go is a DIFFERENT sample model.
  It does not kill these classical CSP samplers.
- Locked-CSP hardness results do not automatically apply: fixing the other
  variables in ONE ternary affine-exclusion predicate leaves TWO legal values
  for a remaining variable. The predicate itself is not locked. Whole-instance
  freezing or shattering needs a separate, scope-matched proof.
- Sampling-LLL sufficient conditions do not follow just from sparsity at
  violation probability1/3 and this dependency degree. Failure to meet a
  sufficient condition is not evidence of hardness either.
- Inspecting [upstream UniGen source](https://raw.githubusercontent.com/meelgroup/unigen/master/src/sampler.cpp)
  is not an independent audit of the wheel. Upstream master uses an
  integer0..1000/cutoff500 hash-bit generator rather
  than literal fair-bit sampling. This pass has NOT established whether that
  matches this wheel or changes its theoretical guarantees. No quantified
  wheel-TV claim is made. The exact-pool method is independent of that issue.
- The Boolean encoding must remain BIJECTIVE. Added auxiliary variables,
  dropped original spins, incomplete models or repeated native models would
  invalidate an unweighted uniform-sampling comparison.
- Small exact pools or successful near-uniform outputs do not prove a
  polynomial large-instance method. Conversely, a timeout does not prove a
  quantum advantage or justify retaining a weak baseline as the only test.

## Next Decision

2026-10-20 follow-up: [TERNARY_CONDITIONED_SAMPLING.md](TERNARY_CONDITIONED_SAMPLING.md)
now supplies rank-conditioned exact rejection and native F3 hash isolation.
Hashing can use the GLOBAL count window without prefix counters; its paid
bottleneck is solving and proving uniqueness of hashed cells. Both saved
inputs produced samples without complete-pool construction. The earlier
prefix warning still applies to prefix decimation, not to every sampler.
Runtime-capped isolation has an extra unknown failure mass and cannot inherit
the uncapped output-law bound from one completed trace.

Retain the conditional signed-trine quantum sampler as an ASYMPTOTIC research
route, not an advantage claim on these saved finite inputs. The global count
observable is now classically predicted under that same premise. Useful work
must address uniform conditional sampling, its solution geometry, or a
precision-paid coherent receiver, not another count/entropy signal plot.

The strongest next classical test is a count-to-sample self-reduction with
controlled error on ACTUAL conditioned prefixes, or a scope-matched native
sampler beyond complete enumeration. Any approximate-counter/SAT costs and
failure probability must be paid. Do not assume constant-factor UniGen
uniformity equals arbitrarily small target TV, or that a truncated pool can
be corrected without its missing mass. No automatic registry/proof promotion.

## Reproduce

The default Python already supplies pycosat0.6.6. pyunigen2.5.8 has no native
ARM64/CPython3.13 wheel. It was installed ONLY into git-ignored tmp/unigen-venv,
using the existing x86_64 Python3.12; the main research environment is unchanged.

    arch -x86_64 /usr/local/bin/python3.12 -m venv tmp/unigen-venv
    arch -x86_64 tmp/unigen-venv/bin/python -m pip install --only-binary=:all: pyunigen==2.5.8
    python theorems/ternary_classical_sampling.py --backend-python tmp/unigen-venv/bin/python --backend-arch x86_64 --samples 128 --timeout 30 --write
    python -m pytest -q tests/test_ternary_classical_sampling.py

Other platforms may use a supported backend Python without the architecture
override. Missing tools remain UNKNOWN. Optional dependencies are separated
in requirements-research-sampling.txt. No giant SDK or service is installed.
