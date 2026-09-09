# Classical Value Access and Cost Audit

## Decision

The canonical quadratic hidden-shift controls are easy with known-form,
classical value access. They remain rejection/calibration controls, not search
candidates. This pass makes the advertised attacks actually execute within
their query budgets. It does not discover a new classical or quantum algorithm.

The previous Boolean attack computed a full Walsh transform and labelled it
`2(n+1)` queries. The finite-field attack computed a full two-dimensional FFT
and labelled that a polynomial-query certificate. Neither implementation
enforced its advertised access budget. They now read only named points.

## Exact Reconstruction

For the canonical Boolean form
`Q(x) = sum_j x_(2j) x_(2j+1)`, with an additional last linear bit for odd n,
classical value queries return `Q(x)` and `Q(x+s)` as bits. Define
`d(x) = Q(x+s) + Q(x)` over F2. The values `d(e_j)+d(0)` reveal the
paired polar coefficients, hence all paired shift bits. For odd n the last
polar coefficient is zero; the last shift bit is instead
`d(0) + sum_j s_(2j)s_(2j+1)`. Total cost: `2(n+1)` value calls, separately
charging f and g, and a conservative `O(n^3)` bit-work bound for the actual
Python loops. No transform, full table, or exhaustive shift search occurs.

For `Q(x,y)=x^2+xy+c*y^2` over an odd prime field, query both functions at
`(0,0), (1,0), (0,1)`. Subtract the derivative's origin value to obtain
`a=2s_x+s_y`, `b=s_x+2c*s_y`. If `4c-1` is invertible,
`s_x=(2c*a-b)/(4c-1)` and `s_y=(-a+2b)/(4c-1)`. This is six value calls
and polynomial bit work in log p. The default c=5 is singular at p=19;
the attack declines that case rather than claiming success.

Both algorithms assume the *known canonical form*, not an arbitrary unknown
bent/quadratic function. Queried-value consistency does not certify that a
black-box function satisfies a global promise. `true_shift` is used only to
score the independently computed prediction. Tests deliberately change it.

## Access and Precision Boundaries

- `ExactPhaseEvaluator` returns an integer exponent modulo the phase modulus.
  Its output has `ceil(log2(p))` bits; the caller supplies actual value access.
  It does not simulate extracting that exponent from a quantum state.
- Numerical inputs are read one point at a time. Each complex value must be
  within `min(1e-8, sin(pi/p)/16)` of its promised root. Nearest-root residuals
  are checked. That check cannot establish the error relative to an unknown
  true value. For p above `2^32`, the numerical path rejects and requires exact
  residues instead of assuming unbounded phase resolution.
- For odd Boolean n, shifts differing in the last bit give vectors differing
  only by a global minus sign. Classical signs distinguish these value tables;
  an uncontrolled phase oracle or an isolated phase state does not supply
  that distinction. The tests explicitly preserve this counterexample.
- A coherent *value* oracle can be queried on basis inputs to obtain values.
  A coherent *phase* oracle, controlled phase oracle, and supplied DHSP states
  are different interfaces. The old undifferentiated `coherent_oracle` label
  remains unresolved, not evidence of classical hardness. These attacks are
  not registered as legal state-only attacks.
- Generating the finite diagnostic tables and searching for primes are not
  part of the polynomial reconstruction algorithm. Table-free regression
  controls use fixed known primes and lazy exact evaluators.

These boundaries are consistent with the separate repository public-evaluator
admission theorem. Do not confuse this known-form case with oracle-family
separations for [bent hidden shift](https://arxiv.org/abs/0811.3208), or claim
novelty for the [multiplicative-character hidden-shift mechanism](https://arxiv.org/abs/quant-ph/0211140).

## Resource Accounting

`ShiftAttackResult.resources` records calls to each function, classical time
class and bound, memory, table materialization, the input promise, and precision.
`sample_count` is now the **total f+g value calls** in this workbench. The random
collision probe separately labels its axis **samples per function**.

The random-sample attack reads q random values from each function, then scores
all shifts. Its work remains `O(q |G| poly(log|G|))`. A finite success is recorded
as `finite-random-sample-recovery-only`, never as a polynomial-time algorithm.
The chosen exhaustive attack caches values: it makes exactly `|G|+q` value
calls, stores the full base table, and still does `O(q |G|)` comparisons.
All value-correlation baselines score the real inner product, not its absolute
value, to avoid incorrectly identifying distinct signed value tables.

Missing resource records, tiny finite query counts, and prose such as `O(n)`
cannot pass the polynomial-value-recovery filter. That filter checks the
presence/consistency of a resource contract, not mathematical truth. The current
two admitted implementations have elementary derivations above and adversarial
access tests; no automatic complexity theorem prover is implied.

Nine table-free controls cover Boolean dimensions 16, 63, 128, 255 and prime
fields through `p=2^127-1`. Larger domain size here verifies lack of a hidden
table dependency, not stronger evidence for a quantum separation. All ordinary
Fourier diagnostics still explicitly incur full-table cost.

## Reproduce and Falsify

```sh
python qsearch.py hidden-shift --families bent_quadratic_f2,fp2_quadratic_form,quartic_character --min-bits 5 --max-bits 8
python qsearch.py baselines --families bent_quadratic_f2,fp2_quadratic_form,quartic_character --n-values 5,6,7,8 --sample-counts 4,8,16,32
python qsearch.py dequantize
python qsearch.py validate
```

The existing hidden-shift artifact includes `value_query_controls`; experiment
results expose their counts and state-access nonapplicability. Baseline writes
now update the scaling registry and scoped negative records. Tests forbid array
conversion/iteration and excess point reads, exhaust all shifts at small sizes,
check odd-dimensional sign recovery, corrupt residues/precision, reject singular
forms, and prevent finite/exhaustive or missing-cost claims from being promoted.

Remaining blockers: no worst-case success theorem for the sampled heuristic,
no end-to-end classical replacement of the binary-carrier quantum front end,
and no new natural hard-family quantum decoder. The nine controls do not resolve
any of those questions. More small-instance success counts would not do so.

## Follow-Up: Retraction of the Spectral Learner Claims

`fourier_compressibility_baselines.py` previously inferred evaluator recovery
and even random-sample recovery from spectra and a heuristic budget formula.
That function does not receive g(x)=f(x+s), an unknown shift, or any shifted
samples. It cannot have executed a shift-recovery algorithm. Its output is now
explicitly `full-table-spectrum-only`; all recovery and certified-query-bound
counters are zero, regardless of the requested sample budget. The finite
support threshold is no longer named "poly-sparse".

There are two independent missing implications. First, derivative access
requires pairs (x,x+a). A passive sample interface does not automatically let
a learner request those pairs. Second, learning a spectrum need not identify
a shift: over F2, exact Fourier phase ratios on frequencies spanning rank r
leave an annihilator of dimension n-r. All `2^(n-r)` corresponding shifts
give the same constraints. A one-sparse spectrum alone is not a complete
hidden-shift decoder. No new oracle problem or candidate is proposed by this
counterargument.

The runner, experiment seed, mutation protocols and family triage no longer
promote spectral concentration to learner success. Old positive recovery
counters are also distrusted by the dequantization reader. A future learner
needs actual permitted observations, counted queries, accuracy/failure bounds,
shift identifiability and charged classical decoding work.

Five historical `FOURIER-COMPRESSIBILITY-DEQUANTIZED-*` negatives were
unsupported by their stated evidence. The writer preserves the original
records and retraction reasons in
`research/quarantine/unsupported_fourier_recovery_claims.json`, removes them
from active negative evidence, and records one scoped failure of the inference
"concentration implies a decoder". Independent valid low-degree attacks are
not retracted. Withdrawal of a bad classical argument is not positive quantum
evidence. Repeated writes preserve the archive; `--no-registry` does not retire
or change any registry records.

```sh
python qsearch.py fourier-learnability
python qsearch.py run EXP-DHS-FOURIER-COMPRESSIBILITY
```
