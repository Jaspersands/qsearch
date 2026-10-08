# Native Prefix Integrality And Certified Linear Pruning

LOCAL DERIVATIONS / REVIEW PENDING. No novelty, polynomial native pair finder,
population hardness or quantum speedup is claimed. This closes the experiment
specified in `NATIVE_TERNARY_PREFIX_INTEGRALITY_TARGET.md`.

## Decision

The current failure has TWO causes. Many visited prefixes are linearly
infeasible, so exact separator search can help locally. Others have genuine
fractional continuations despite having no native integer continuation. Better
linear separation cannot eliminate the latter in the same representation.
The matched certified-LP decoder does not improve larger-root pair recovery.
Generic LP/cap inflation is therefore deprioritized, not declared impossible.

## Exact Model

For the original scalar nuisance problem, each digit has coordinates
`z_j=(u_j,v_j)` in `{(0,0),(1,0),(0,1)}`. The full congruence kernel has verified
integer rows `K_i`, whose native embedded rows are `R_i=3*E(K_i)`.
The fixed target representative is `z0`, and the native error is
`T-sum_i c_i R_i`, where `T=E(ones)-3*E(z0)`.

At a real passed parent checkpoint, rows `i>=b` have assigned integer
coefficients. The unassigned `i<b` are canonically zero in the saved record.
An exact Babai completion supplies a numerically moderate integer anchor
`z_anchor=z0+sum_i anchor_i K_i`; EVERY assigned coefficient is unchanged.
The continuous prefix is exactly

```text
z = z_anchor + sum_(i<b) eta_i K_i, eta_i real;
u_j >= 0, v_j >= 0, u_j+v_j <= 1.
```

Every digit forbidden by the actual prefix-projector energy test has EXACT
zero probability in its block triangle. These are necessary correlated-block
conditions; their energies are not summed. Affine span membership retains all
assigned projections, not just the original scalar modular congruence.

For a true native word, `A.z=t+Q*k` for an integer winding `k`. The real prefix
alone need not satisfy this. Therefore the report also checks the complete
allowed winding schedule, with

```text
k_anchor = (A.z_anchor-t)/Q;
w_i = (A.K_i)/Q;
k = k_anchor + sum_i w_i eta_i;
k in [0, floor((sum_j max(a_j,c_j)-t)/Q)].
```

Native integer coefficients additionally force `k-k_anchor` divisible by
`gcd(w_i)`; when that gcd is zero, only `k=k_anchor` is possible. No favorable
winding branch is selected while ignoring the rest.

## Proof Authority

SciPy/HiGHS only PROPOSES a point or a nonnegative dual combination.
FLINT exact rational elimination reconstructs an active face, including
guessed rational free coordinates when needed. All original triangle,
forbidden-digit and winding constraints are independently checked. The
recovered point need not be a vertex. A float feasible/infeasible flag, solver
timeout or failed rational reconstruction is never a mathematical conclusion.

Infeasibility is certified by explicit rational multipliers `y>=0` with
`y*A_constraints=0` and `y*B_constraints<0`. Equality constraints occur as both
signed inequalities. Every multiplier is retained. A certificate for one
fixed winding cannot certify the unrestricted prefix; the independent checker
now enforces the enclosing model identity as well as the arithmetic.

Native truth is obtained separately by complete original-digit MITM and exact
prefix-span membership. ALL collision buckets are retained, not only two
words. Preflight/match-budget failures mean UNKNOWN, not an empty prefix.
These exponential truth tables are never supplied to LP proposal or decoding.

## Live Evidence

The audit uses 72 passed cap256 parent prefixes from nine frozen label sets
and the same independent-uniform-target fixtures. Targets within a label
batch are conditional observations, not new population samples.

| Root digits | Exact feasible prefixes | Exact linear obstructions | Fixed-winding false prefixes |
| --- | ---: | ---: | ---: |
| 16 | 9 | 15 | 8 |
| 24 | 8 | 16 | 8 |
| 32 | 9 | 15 | Native truth unknown |

One additional root16 prefix has a prefix-only integrality gap, but all its
allowed integer windings are exactly obstructed. It must NOT be counted as a
fixed-winding gap. All 26 feasible and 46 obstructed classifications have exact
certificates. The 1,034 winding branches contain 104 primal and 930 dual proofs;
including the parent models gives 130 primal and 976 audit dual proofs.
The native reference checks 48 original target fibers using 1,076,004 half
assignments. Root32 references exceed their explicit budget.

The matched runtime pilot retains every Farkas prune and charges 16 LP attempts
per target, with a 2,048-coefficient-node cap. It uses only unrestricted-prefix
cuts, not an uncharged loop over windings.

| Root digits | Verified pairs / targets | LP decoder nodes | Projector baseline nodes |
| --- | ---: | ---: | ---: |
| 16 | 1 / 24 | 14,290 | 15,184 |
| 24 | 0 / 24 | 49,152 | 49,152 |
| 32 | 0 / 24 | 49,152 | 49,152 |

The root16 nonpair fibers all complete; all 48 larger-root targets hit caps
without witnesses. The pilot records 1,152 LP attempts and 536 exact prunes.
A roughly 6% small-root node reduction is NOT a wall-time improvement: LP
work, original LLL preparation and physical source costs cannot be omitted.

## Attempted Refutations And Limits

- Huge coset coordinates can corrupt float faces: the LP is now recentered at
  an exact integer anchor, and the final certificate checks original coordinates.
- Under-ranked faces can be genuine: exact free-coordinate proposals are allowed
  only after all equalities and inequalities verify; they are not called vertices.
- Fractional winding can create fake gaps: the complete integer winding/gcd
  schedule resolves one apparent gap and leaves 16 genuine fixed-winding cases.
- A whole fiber may be nonempty while this prefix is empty: exact native truth
  checks assigned projections, rather than merely whole-target emptiness.
- Selected prefixes may be atypical: these finite conditional observations prove
  no average-case obstruction, source success exponent or universal lower bound.
- Another basis/order, integer cut, higher-degree relaxation or collective quantum
  receiver can evade this result. Linear feasibility does not force its visitation.

The follow-up `TERNARY_PREFIX_MODULAR.md` now audits one discrete escape route.
The next question is `NATIVE_TERNARY_COUPLED_MOMENTS_TARGET.md`, not more generic
LP iterations or another conditional quantum receiver wrapper.

## Reproduction

```sh
python theorems/ternary_prefix_integrality.py --write
python theorems/ternary_prefix_integrality.py --decoder --write
python -m pytest -q tests/test_ternary_prefix_integrality.py
node research/certificates/ternary_prefix_integrality_crosscheck.js
```

The independent BigInt checker verifies original integer kernel completeness,
actual GS prefix spans, projector domains, all rational proofs and budgeted
native truth, as well as runtime words and retained prune certificates. It
does NOT replay the full enumeration tree or prove population coverage.
Gemini/Antigravity owns routine CLI/registry/UI and full production validation.
