# Repair By Complete Cyclic Fourier Positivity

CONSTRUCTIVE NUMERICAL EXPERIMENT / NO POPULATION RECOVERY OR SPEEDUP.
This tests a specific polynomial-description repair suggested by the exact
native SDP counterexamples. It does not add a rank oracle, chosen samples,
full secret enumeration or another fixed toy-circuit menu.

## The Missing Necessary Constraint

An exact group-character mixture has moments f(d)=E_s chi_q(d.s). The
full-difference circuit SDP certifies PSD only on its finite node set V.
Even when EVERY multiple of a vector d appears among V-V, it need not
contain the full cyclic subgroup as actual matrix nodes. Its PSD constraint
therefore need not make the cyclic Fourier law positive.

The additive order of d in Z_q^n is m=q/gcd(q,d1,...,dn), not automatically
q. For q=3^r it is an odd power of3. If all m vectors k*d are represented
differences, every true character satisfies

    p_(d,t) = (1/m) sum_(k=0)^(m-1) chi_m(-k*t) f(k*d) >= 0,
    sum_t p_(d,t) = 1.

For one secret p is a delta distribution: d=(q/m)*d' and the sector is
d'.s modm. A mixture gives ordinary nonnegative marginal probabilities.
These are LINEAR inequalities on the existing moment entries. They are
also equivalent to PSD of the complete cyclic circulant matrix, without
adding a new m-by-m cone. Positivity on all represented cycles is still
NOT global realizability across different cycles.

## Why This Repair Is Not A First-Moment Support Check

The previous exact dyadic witnesses satisfy EVERY one-dimensional root
polygon constraint for all represented differences, with their correct
orders including3. Each individual moment belongs to the convex hull of
the allowed roots. Yet some COMPLETE cyclic laws have negative probabilities.
The producer certifies these violations using rational root intervals;
floating Fourier transforms only suggest which violations to examine.

For odd m the regular polygon inequalities can use existing mth roots:
the outward normal exp(-i*(2t+1)*pi/m) equals
-chi_m((m-1)/2-t). The exact slack is

    -cos(2*pi*((m-1)/2)/m)
      + Re[chi_m(((m-1)/2-t))*f(d)].

Endpoint-aware dyadic interval arithmetic proves every such slack nonnegative
for the saved witnesses. This eliminates the weaker proposed repair, rather
than silently treating an order-q polygon as adequate for divisible vectors.
The full cyclic constraints use higher moments and really reject the points.

## Compiled Experiment

Start from the SAME public polynomial circuit node set. Hash all V-V
differences; canonicalize generators under unit multiples modulo their
ACTUAL additive order. Keep only cycles whose EVERY member is represented.
Do not fill missing moments with0 or grant their values. Scan all complete
cycles, with whole-order/whole-constraint caps returning declared failures.
Every frequency, cycle and constraint depends only on original public labels,
not measurement outcomes, planted truth, a previous decoder output or holdout.

The real nonnegative sparse operator is added to the existing Hermitian
SDP solver. Its feasibility audit checks every new probability, including
the imaginary residue. Secret-blind rounding and training-only coordinate
refinement are unchanged. Solver precision and recovery remain unproved.

Predeclared cohorts: source seeds93013 (n3/r2/M48),93017 (n5/r2/M32),93018
(n6/r2/M32). The first is a positive calibration; the latter two generated
the original exact gap witnesses. All classical TRAINING records can be
reused: that is not reuse or cloning of unknown quantum inputs. Freeze the
new candidate and all old training-selected comparison candidates BEFORE
generating NEW independent256-record validation cohorts at source seed+100
and noise seed+101. Old holdout data is not reused for validation. Distinct
IDs and PRNG streams remain evidence of implementation discipline, not a
certificate of physical IID input supply.

Compare the new candidate with the old SDP,14-start refinement and the
256-start portfolio containing the14-start seeds. All receive the same
counterfactual fresh CLASSICAL validation records. Their errors are not
independent; use the union bound4*exp(-2*256/81) when interpreting all four
threshold tests together. Classical recovery from these measurements does
not simulate the original quantum input.

## Costs And What Could Still Fail

There are at most K^2 represented differences. Generator canonicalization
costs polynomial work in n,K,q. Each retained group contributes m<=q
inequalities with m entries, so O(q^2*K^2) is a conservative operator-size
bound. This is polynomial in q, NOT logq; a growing-root theorem must
justify the upstream q regime. The finite implementation caps q at81.
It never enumerates all q^n characters to compile cuts or choose a candidate.

The old certificates' exponential censuses remain previous research evidence,
not an input to the repair. Discovery of violated cycle probabilities needs
only the polynomial represented-difference set and q-sized Fourier laws.
The decoder uses all those laws, not just a handpicked violation tailored to
the old numerical solution. This preserves the true-character feasible set.

Falsifiers and failure modes:

- A true character fails a compiled cyclic inequality: reject the compiler.
- Wrong subgroup order, missing multiple or bad Fourier sign invalidates a law.
- A saved witness's alleged negative law has a nonnegative certified upper.
- The solver finds new high-score pseudo-moments satisfying EVERY cycle.
- Rounding fails, classical comparison explains success, or fresh prediction
  fails despite a high training objective.
- The missing constraints involve relations across many independent cycles;
  this local repair may then have little leverage at growing n or q.

If stronger false solutions survive, do not infer all convex or quantum
methods impossible. Seek a new exact certificate and identify the missing
cross-cycle realization condition. Nor does rejecting the old witness prove
tightness: the optimizer can move to another feasible pseudo-moment point.

## Exact Survivor Certificates

`ternary_character_cyclic_gap_certificate.py` reuses the existing dyadic PSD
factor/residual method on the STRENGTHENED numerical points. Identity mixing
preserves every cyclic law: it gives the uniform cyclic distribution1/m.
The exact quantized point must pass EVERY new law with a rational lower bound,
not only PSD or the earlier finite-character score bound. A positive gap
against the previously certified all-secret upper therefore disproves
universal tightness AFTER this repair. This identifies an actual cross-cycle
realizability failure, not mere rounding or a numerical cutoff artifact.

The original complete character census can be reused only under unchanged
pinned training records. The new independent verifier replays it again. No
expensive numerical optimizer needs to be repeated to certify a saved point.
The `--replay-saved-matrices` mode verifies the unchanged compiled node/cycle
model and numerical feasibility, then reruns rounding and SAME seeded
validation bookkeeping. It is not a new independent experiment, new source
acquisition or a claim that SCS was reexecuted. It also prevents JSON list
versus tuple conventions from corrupting post-hoc calibration flags.

Independent replay now certifies strengthened feasible score gaps per training
record of at least approximately0.6145898192 and1.2775982183 for seeds93017
and93018. It checks21,534 cyclic probabilities exactly,135,578 moment entries
and590,490 full-root secrets. Both new dyadic points have a strictly positive
minimum cyclic probability lower bound (about1/288). These are finite native
counterexamples to universal tightness, not growing-sample failure theorems.

```
python theorems/ternary_character_cyclic_decoder.py --write
python theorems/ternary_character_cyclic_decoder.py --replay-saved-matrices --write
node research/certificates/ternary_character_cyclic_decoder_crosscheck.js
python theorems/ternary_character_cyclic_gap_certificate.py --write
node research/certificates/ternary_character_cyclic_gap_certificate_crosscheck.js
python -m pytest -q tests/test_ternary_character_cyclic_decoder.py
```

Gemini owns CLI/registry/UI integration and full production validation.
Import the old-point rejection as exact scoped evidence and the new decoder
as numerical research, not an accepted speedup candidate.
