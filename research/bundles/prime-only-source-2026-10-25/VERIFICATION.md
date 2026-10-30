# Verification And Scope

2026-10-25. Run from /Users/jaspersands/Developer/qsearch-research-work with
/opt/anaconda3/bin/python. All paths below are relative to that workspace.

## Results

- New source suite: 26 PASS in 4.68s.
- New elliptic postprocessing suite: 15 PASS in 0.55s.
- Initial source/dependency regression: 120 PASS in 36.01s.
- Final combined regression: 171 PASS in 41.76s, no skips, warnings as errors.
- Six Python syntax checks PASS.
- Receipt --write --check PASS, followed by separate --check PASS.
- Receipt SHA256:
  98e5c7b2e077cdb33564bc77b16957a30fca9911aa2eb7fda8f24c205ff93bcb.

The final combined command was:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

Syntax-checked prime_source.py, controls_prime_source.py, elliptic_reduction.py,
test_prime_source.py, test_elliptic_reduction.py and replay_prime_source.py.
Replay: `/opt/anaconda3/bin/python prime-only-source-2026-10-25/replay_prime_source.py --check`.

## What The Controls Establish

The exact arithmetic covers integral inverses, the original mod-ell group
query, evenized factors, odd trace, the derived uniform trace bound, the
quadratic relation and the multiplier-N norm certificate. The integral
Gaussian realization verifies rank16 maximal-isotropic prime kernels at
seven levels, including the nonsemisimple discriminant-zero prime29.
It also checks common-mask cancellation and N^-1 marking transport.

Countercontrols reject even-trace odd-target equations, naive appending
of the parity shear, wrong N^-2 transport, corrupted coefficients and
promotion of repeated-prime formal certificates to prime-only access.

The elliptic checks recover a line and LEFT annihilator ideal from a
SUPPLIED doubled plane, with ideal index ell^2 and left-order closure.
Wrong image constraints, unequal factor masks, nondoubled planes and
rank-deficient inputs fail their respective tests.

The uniform example (ell5, characteristic11, basis norm sum8) has trace
bound1410 bits, multiplier2825 bits, 303 quotient primes and maximum weak
order2027. Its weak-query exponent is1. This is a deliberately conservative
uniform plan, not the resources of a practical quantum implementation.
Lists would still contain r^16 points. None was enumerated.

## What Was Not Verified

No elliptic/torsion point generation, PPAV quotient, canonical geometric
label, coherent circuit, secret-kernel recovery, IdealToIsogeny conversion
or target-order geometric evaluation ran. The split fixtures are small
enumerative examples, not a scalable splitting implementation. SymPy's
four-square routine supplies verified witnesses, not a certified uniform
polynomial-time implementation of the imported theoretical algorithm.

The algebra proofs and conditional elliptic corollary need independent
review. The previously authorized Rees reviewer did not inspect them.
Prior art already supplies quantum IsERP algorithms; novelty or an
unconditional assumption removal is NOT certified. Matched classical
hardness is NOT established. The search-indexed 2025 manuscript statements
were inspected, but its full proof could not be retrieved in this pass.

The entire new bundle and the shared checkpoint are isolated from the
unverified migrating repository. No main/staging/dependency source edit,
CLI/registry/UI integration, commit, push or migration change was made.
Main repository tests, qsearch.py validate and node --check were NOT run;
this was a theory/arithmetic pass, not a validated main-project release.

## Files

Created PRIME_ONLY_SOURCE.md, ELLIPTIC_COROLLARY.md, prime_source.py,
controls_prime_source.py, elliptic_reduction.py, test_prime_source.py,
test_elliptic_reduction.py, replay_prime_source.py, receipt.json, HANDOFF.md
and this VERIFICATION.md. Prepended one entry to the shared isolated
RESEARCH_CHECKPOINT_2026-10-23.md. Existing dependency sources were retained
unchanged, including the old prime-square path and its negative controls.
