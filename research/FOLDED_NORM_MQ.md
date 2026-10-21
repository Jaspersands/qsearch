# Native Global Square Completion

## Scientific Question

Can a genuine global algebraic attack find a native polynomial at the score
thresholds that the existing interpolation/repair/norm-line attacks miss?
This is an ACTUAL classical solver experiment, not another quantum candidate,
generic MQ hardness assertion or a fixed-subset feasibility proxy.

`theorems/folded_norm_mq.py` takes the exact public inputs from the saved
folded-norm attack report. Its targets are25/58/114 for n25/65/127. The first
is a fresh recovery of an already known perfect instance; the second is above
the old57 witness; the last is the old conditional quantum mean's integer
threshold. No known polynomial, root witness or selected subset is given to
the solver. Public shifts/signs/field and original F_p dimension K are fixed.

Expected asymptotic improvement: NONE established. A generic Groebner-based
solver may be exponential, time out or run out of memory. Its purpose is a
stronger classical falsifier and an exact native algebraic representation for
further mathematical attacks. It does not establish a Shor-level result.

## Exact Quadratic Reduction

Let E=F_(p^m) with the same verified public monic irreducible polynomial and
power basis as the source. Let P(X)=sum_(j<K)c_j X^j, all c_j in F_p.
At block i, the acceptance condition is

```text
z_i = pack(P(a_i,0),...,P(a_i,m-1))-t_i,
chi_E(z_i)=sigma_i, or z_i=0 when including-zero is enabled.
```

Choose a VERIFIED base-field nonsquare nu. Since m is odd it is also a
nonsquare in E. Put d_i=1 for sigma_i=+1 and d_i=nu otherwise. Introduce
roots w_i in E through their m ORIGINAL F_p coordinates, not an extension
solver sort. Then selected block i accepts exactly when z_i=d_i*w_i^2,
with w_i!=0 in strict mode.

For beta the stated field generator, compile the square by convolution

```text
raw_h = sum_(r<=s,r+s=h) (1 if r=s else2)*w_r*w_s,
sq_r = sum_h coefficient_r(beta^h)*raw_h.
```

The2m-1 basis powers are actually computed. Independent tests compare the
manual polynomial-modulus square with extension arithmetic on ALL343 roots
of F_(7^3); native pinned-polynomial SMT controls check the generated equations.
No multiplication, trace or square-root oracle is supplied to the solver.

Use field idempotents b_i^2=b_i for block selection. A FIELD element satisfying
this equation is exactly0 or1. Introduce separate square-coordinate variables
sq_i,r and assert the quadratic square equations. Then the score guards are

```text
b_i * [sum_(j<K)c_j*a_i,r^j - t_i,r - d_i*sq_i,r] = 0.
```

These are QUADRATIC, not cubic: sq is a declared auxiliary variable with its
own quadratic defining equation. Every polynomial coefficient and every
root/auxiliary/selector coordinate belongs to F_p. Replacing this by an
E-coefficient polynomial is a different, invalidly relaxed problem.

For target T, add n-T idempotent slack bits e_j and the linear equation

```text
sum_i b_i - sum_j e_j = T  in F_p.
```

The native distinct-point geometry gives p>n. The corresponding integer
residual lies in[-n,n-T], strictly between-p and p. Thus there is NO modular
wrap: this equation is satisfiable exactly when sum_i b_i>=T. The compiler
uses no bitvector/integer-theory cardinality interface. For T=n, b_i=1 follows
exactly and is explicitly added for preprocessing; this is not a guessed mask.

In strict mode introduce v_i in E, again as F_p coordinates, and assert
w_i*v_i=b_i. These are bilinear equations. If b_i=1 they ensure w_i!=0; if
b_i=0, choosing v_i=0 permits any w_i. No high-degree norm/nonzero equation
or disjunctive field test is needed.

**Forward:** any native P with at least T accepted blocks yields a model:
select those blocks, choose square roots of z_i/d_i, set sq=w^2, choose
inverses when strict, and fill slack bits. The Q=3mod4 square-root exponent
(Q+1)/4 can verify such calibration witnesses, but no roots are supplied in
the actual search. **Reverse:** any model gives an original degree<K
polynomial, at least T selected blocks, and actual square witnesses for each.
Thus this is the optimization objective, not a promise about a prescribed
subset. Failure on one fixed subset would not test this objective.

## Witnesses And Unresolved Outcomes

A SAT flag alone is never accepted. The implementation checks canonical
coefficients and all selector values, replays the ORIGINAL polynomial with
independent Horner evaluation on every scalar point, compares native norm
predicates, and manually squares/reduces every selected root. Every selected
block must accept and the actual total score must meet T. A complete valid
witness remains useful even if a solver process is subsequently terminated;
a truncated or wrong-prime model is rejected.

UNSAT is retained as `SOLVER_UNSAT_NOT_INDEPENDENTLY_CERTIFIED`, not a proof
or automatic negative. Time, memory, parser/backend failure and UNKNOWN are
unresolved. Even a VERIFIED finite witness does not prove a uniform classical
algorithm, dequantization of the family or refutation of a quantum mean LOWER
bound. UNSAT at114 on the127-block instance would require an independent
encoding/proof audit before drawing any contradiction with that finite mean.
UNSAT at58 on the65-block instance would not contradict its56.6987 mean floor.
These old small inputs are NOT the different n>=3200 uniform-family theorem.

The small known-answer calibration deliberately includes a trap: the first
two blocks are infeasible together, but a different selected pair is feasible.
The solver recovers a verified polynomial without a witness hint. Some
six-block known-SAT/known-UNSAT cases remain unresolved within their budgets;
those failures are retained rather than replacing them with easier success
claims. Tests separately prove idempotence/cardinality by full finite
enumeration and compare the extension equations with native evaluation.

## Backend And Resource Contract

The backend is [cvc5's prime-field solver](https://cvc5.github.io/docs/latest/theories/finite_field.html),
which uses CoCoA/Groebner machinery. The ordinary cvc5 Python wheel tested here
cannot solve field problems: it reports that it was not configured with CoCoA.
The actual experiment uses the official cvc5-1.4.2 macOS arm64 static GPL
executable. Its downloaded archive matches the release API SHA256:

```text
82d06b330c68938739b28adb84d3f352ee058bc594efc25f32a7eebc2b507c74
```

The executable/licenses are OUTSIDE the repository. Only the small optional
SMT-LIB parser/serializer dependency is specified in requirements-research-mq.txt.
Model output is parsed structurally, not executed as code.

At the main parameters, including-zero variable counts are1885/4908/9564.
The dense original Vandermonde frontend evaluates240250/1624090/6102350
coefficient powers. Raw quadratic square products number496 per block at
m31. All these expression counts, script sizes/hashes and assembly times
are recorded. They are NOT complete bit-operation counts or a fast frontend.
Keeping auxiliary squares preserves the native sparse quadratic structure,
but the backend may densify it or spend its entire budget parsing/preprocessing.

Each real attempt has a60-second solver budget and a sampled3072MiB child RSS
budget. The outer process allows5 seconds for timeout handling, then kills
and WAITS for its OWN child if needed. Memory polling is sampled, not a hard
OS limit, and may overshoot. Null peak memory means no sample was obtained,
not zero memory. Frontend assembly time is separately paid; solver parsing
and algebra time are not separated. An observation-tool timeout never starts
another solver job. Source, dependencies, input and binary are hashed BEFORE
the run and checked again before writing a report.

Current-machine replay:

```sh
PYTHONPATH=/tmp/qsearch-cvc5 python theorems/folded_norm_mq.py \
  --solver /tmp/qsearch-cvc5-gpl/cvc5-macOS-arm64-static-gpl/bin/cvc5 \
  --seconds 60 --memory-mb 3072 --write
```

Large SMT files and raw stdout/stderr live under ignored tmp/folded_norm_mq/,
NOT the tracked research registry. The compact report contains the exact input
binding, all outcomes/costs, backend hash and any independently verified native
witnesses. No candidate/proof/negative is automatically promoted.

## Executed Outcomes: 2026-10-19

The saved producer report is `research/classical_baselines/folded_norm_mq.json`.
All three processes are terminal; each reported its internal time budget,
not UNSAT. No witness was returned and no input was rerolled.

| Blocks | Target | Frontend Seconds | SMT Bytes | Solver Seconds | Sampled Peak KiB | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| 25 | 25 | 6.000 | 12222408 | 60.055 | 1031968 | UNKNOWN: time budget |
| 65 | 58 | 27.001 | 75309591 | 60.128 | 1895888 | UNKNOWN: time budget |
| 127 | 114 | 99.653 | 276866814 | 60.110 | 1011744 | UNKNOWN: time budget |

The three-block strict known-answer calibration recovered the genuine native
polynomial P=2, selecting blocks1/2 although blocks0/1 cannot jointly satisfy
the target. The six-block known-SAT calibration timed out within2 seconds.
Thus the backend does not even reliably resolve these small calibration
systems within the declared budget. In particular, its failure on the25-block
instance cannot be treated as difficulty evidence: the existing native
norm-pencil report already contains a perfect classical witness on that SAME
input. The larger outcomes provide no stronger hardness evidence.

The exact quadratic representation and independent witness checker are useful
reusable outputs. The bounded generic solver did NOT improve any classical
score or resolve the scientific question. Source/input/dependency and backend
hashes are bound in the report; raw scripts/logs remain in ignored `tmp/`.
Do not promote these UNKNOWN outcomes to negatives or proof-status changes.

Verification at this milestone:462 connected tests pass177.58s, including all
13 MQ tests with the real optional backend. This is not the full repository
suite. Source/input/dependency hashes replay; four strict finite JSON artifacts
parse, compilation/site checks pass, and actual registry validation returns
`valid: true`, `issues: []`. The concurrent bridge ledger still has a separate
known failing test and is not mathematically endorsed by these checks.

## Stop Rule

If this bounded generic backend gives no new witness, do not respond by adding
more backend names, timeout/seed meshes or a hardness label. The next useful
step must exploit the shared algebra/code structure, produce a meaningful
natural reduction, or pivot to another concrete constructive direction.
