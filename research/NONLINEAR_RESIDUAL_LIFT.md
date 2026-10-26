# Quadratic Lifting Creates A False Advantage

2026-10-20. Local elementary derivation REVIEW PENDING. No novelty, quantum
speedup or general classical lower bound is claimed. This follows
`NONLINEAR_FILTER_PINNING.md`; it tests an actual code-aware arithmetic attack,
not another source-tail certificate.

Producer: `theorems/nonlinear_residual_lift.py`.
Artifact: `research/classical_baselines/nonlinear_residual_lift.json` (schema v2).

## The Question

For public prime-field points alpha_i, nonzero a_i and explicit half-size
sets F_i, the published task is to choose deg(P)<n maximizing

    P(alpha_(i+1)) + a_i P(alpha_i)^2 in F_i.

The [known relative-DQI construction](https://arxiv.org/abs/2609.35101) is
already a quantum algorithm; it is not ours. Its tested classical competitors
do not settle the complexity of this explicit task. We asked whether the
substitution Q=P^2 makes a useful classical linear optimization problem.

It makes a linear RELAXATION, but the first obvious completion fails badly.
The result blocks a concrete false-positive mechanism, not the whole route.

## Exact Lift And Feasibility

Write c for n coefficients of P and q for 2n-1 coefficients of Q. Define

    B_i = [1, alpha_(i+1), ..., alpha_(i+1)^(n-1),
           a_i, a_i alpha_i, ..., a_i alpha_i^(2n-2)],
    r = B (c,q).

The degree bounds are formal polynomial bounds. They do not permit reducing
Q modulo an evaluation vanishing polynomial before checking Q=P^2. The
producer checks every convolution coefficient, including the leading ones.
Q being the square of SOME polynomial is insufficient: it must equal the
square of THE SAME P in the linear block.

If B has a verified nonsingular (3n-1)-row submatrix, then a complete residual
vector has at most one lifted preimage. Solve those rows, replay EVERY other
row, and check Q=P^2. This gives a polynomial-time exact inverse/image test,
not an optimization algorithm for the unknown residuals. An invalid square
in that unique preimage proves that no other P produces that entire residual.
It does not rule out another P with the same or higher SCORE.

Rank is not optional. For constant a and the natural order, all lifted
residuals lie in a polynomial space of degree at most 2n-2, of dimension
2n-1, rather than 3n-1. At p7,n2,a=1, original P=0 and P=-1 both give zero
residual. The invalid pair P=X,Q=-X-1 ALSO gives zero residual. Rejecting that
representative as proof of infeasibility would be wrong. The inverse refuses
rank-deficient input; the collision is a permanent countercontrol.

For odd characteristic, the linear span of the ORIGINAL residual image is
the full column space of B. Indeed R(P)-R(-P) isolates the linear P block;
R(P)+R(-P) isolates P^2, and squares span all polynomials of degree <=2n-2
by polarization. Thus full rank is not simply an artifact of taking the
linear span of an unnecessarily large auxiliary family. This is a dimension
statement only, not an algorithmic hardness statement.

## The Native False Positive

Inspected Zhong-Xia Shang and Daniel Stilck Franca's frozen
[RDQINumerics v1.0.0](https://github.com/dsfranca/RDQINumerics/tree/v1.0.0),
commit d9de27218b594925fcd60d8b6c6115a1c74397c7. Data are CC BY 4.0; code is
MIT. We read data with NumPy and independently evaluate modular arithmetic;
no author search kernels were imported or executed.

The first indexed instance, selected before scoring, is
`residual-p2053-n205-281cdca8d31c880a`. Its points are 1,...,2052 in natural
order, but its multipliers are the saved nonconstant public vector. The
first 614 rows have EXACT rank 614. A shifted-polynomial identity does not
remove this rank or turn the lift into an ordinary 409-dimensional RS code.

Procedure: independently pick one allowed residual on each of these 614
rows, solve the linear system, and evaluate both the lifted residuals and the
actual P. One fixed seed48211, no rerolls or instance selection:

| Quantity | Exact native result |
| --- | --- |
| Relaxed score, NOT an original witness | 1353/2051 = 0.659678... |
| Score of the actual P from the same solve | 1011/2051 = 0.492930... |
| Nonzero coefficients of Q-P^2 | 409 of 409 |
| Full-rank forced passing rows | 614 |

The relaxed number exceeds the published ideal quantum mean. It is NOT a
classical falsification of that algorithm: its residual vector has no native
polynomial preimage. The artifact retains c, q, the entire square defect,
both residual vectors, forced values, public structure and source hashes so
that the discrepancy can be independently reproduced.

## Independent Verification Of All 880 Frozen Witnesses And 22 Classical Attacks (Schema v2)

`verify_frozen_witnesses_and_attack_inventory` in `theorems/nonlinear_residual_lift.py`
independently verifies all 880 final polynomial witnesses across all 20 frozen
instances (22 classical methods $\times$ 40 runs) from the versioned archive
([Zenodo 17619922](https://zenodo.org/records/17619922),
[RDQINumerics v1.0.0](https://github.com/dsfranca/RDQINumerics/tree/v1.0.0)):

- **Cryptographic & Structural Integrity**: Checks SHA-256 digests in `SHA256SUMS`
  for `index.json`, `witnesses.json`, `tasks.json`, `tables/runs.csv`, and all 20
  instance metadata and `.npz` array files, and confirms every witness has $n=205$
  canonical coefficients in $\mathbb{F}_{2053}$.
- **Direct Polynomial Evaluation & Ledger Match**: Evaluates $P(\alpha_i)$ on the
  instance's actual evaluation order, computes $(P(\alpha_{i+1}) + a_i P(\alpha_i)^2) \bmod 2053$,
  and confirms the half-set passing count matches `w["score"]`, `runs.csv` `best_score`,
  `witness_digest`, and `satisfaction` on all $880/880$ runs (`0` mismatches).
- **Raw-Batch Coverage Caveat Preserved**: Retains `available_raw_batches: 116` out
  of `expected_raw_batches: 120` (`complete_raw_archive: False`,
  `authenticated_accepted_campaign: 800`, `earlier_attempt_matching_final_table_witness_only: 80`),
  without rerunning or inventing the 4 missing raw batches (`missing_raw_batches_rerun_or_invented: False`).
- **Classical Attack Cost-Ledger Inventory**: Inventories all 22 classical methods
  (from `uniform` and `prefix` to `warm-relax-project-from-moving`,
  `warm-coordinate-from-moving`, and `belief-propagation-guided-decimation`),
  charging full-table lookups (`setup_graph_table_lookups` + `graph_table_lookups`),
  candidate/objective evaluations including warm starts, and CPU time, while recording
  that folded-oracle lower bounds ([arXiv:2610.02145](https://arxiv.org/abs/2610.02145))
  do not apply to explicit public scalar tables. The top verified classical witness across
  all 880 runs scores `1252/2051` (`0.610434`, on `residual-p2053-n205-281cdca8d31c880a`
  by `warm-relax-project-from-moving`), below the ideal quantum threshold `1299/2051`.

## Why This Failure Is Predictable

Here is a narrowly scoped exact ENSEMBLE calculation. Fix public structure
and a full-rank basis of k=3n-1 rows, independently choose each F_i uniformly
among h=(p-1)/2 element sets, and use ideal independent uniform member choices
on the basis rows. Do not optimize those choices or inspect the other tables
when selecting the lifted polynomial.

Each selected residual r_i is uniform in F_p before conditioning on F_i.
The invertible solve makes (c,q) uniform over F_p^k. Therefore

    relaxed score = k + Binomial(M-k, h/p),
    Pr[Q=P^2] = p^(-(2n-1)).

The second statement is an exact counting ratio, not a lower bound on an
optimizer. It cannot be applied to a distribution designed to satisfy the
square relation. At the native parameters it is 2053^-409; unconditional
uniform-lift rejection alone would need about 2^4500.44 trials on average.

More importantly, simply keeping c does not inherit the forced successes.
Conditional on c, q(alpha_i)-P(alpha_i)^2 is uniform, so the repaired native
residual equals the forced residual with probability 1/p. Conditional on
the entire selected residual vector, F_i is a uniform set containing r_i.
If the repaired residual is different, its membership probability is
(h-1)/(p-1). Thus on EVERY forced row the projected passing probability is

    1/p + (1-1/p)(h-1)/(p-1) = h/p.

The other rows have that probability by input independence. Hence the
original projected score has mean M h/p, while the relaxed mean is
k+(M-k)h/p. At the native parameters these means are 1025.000487... and
1332.150024... (fraction0.649512...). This is a built-in relaxation bonus,
not a structural quantum advantage being classically reproduced.
The relaxed probability of at least1299 passing tests is >0.96210 under
these ensemble assumptions; the artifact computes its exact binomial tail
and rounds down. That probability is emphatically NOT a native success rate.

The full native score law has NOT been derived. The ensemble theorem is NOT
a statement about every frozen input, a fixed PRNG seed, every choice of
allowed symbols, correlated lift search or a different repair map. The exact
p5,n1 control enumerates all4000 input/member-choice combinations and checks
both means and the square-consistency probability without the producer's
linear solver. Small examples are validation controls, not research targets.

## Decision And Next Constructive Question

Do not fund a campaign optimizing the unconstrained lift and reporting its
score. No square-blind projection has earned further experiments. The exact
image test is reusable for a proposal that actually specifies a new repair.
Any future such attack must pay for feasibility throughout, retain all failed
reconstructions, and score a verifiable original P on the same public tables.

## Reproduction

Use the frozen author release in a separate directory, then run:

```sh
python theorems/nonlinear_residual_lift.py --reference /path/to/RDQINumerics/data/reference --write
python -m pytest -q tests/test_nonlinear_residual_lift.py -W error::RuntimeWarning
```
