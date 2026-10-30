# Verification Checkpoint

2026-10-23. Two completed isolated passes: exact kernel-to-module/order
postprocessing, and the uniform elementary-lift/trace/denominator bound.

## Executed

- New bundle: 47 tests PASS (36 kernel-output controls, 11 uniform-source
  controls). Final complete run: 7.44 seconds.
- All twelve isolated bundles rerun separately: 438 tests PASS.
- Python py_compile for both modules, both test files and the replay: PASS.
- Live replay: five odd-characteristic cases, six checks each, all PASS.
- Eight source SHA-256 hashes in kernel_output_receipt.json independently
  rechecked against the final source files: all match.
- No owned subprocess or test session was left running.

Commands used /opt/anaconda3/bin/python with external cache path
/tmp/qsearch-rees-pycache. Pytest ran with plugin autoload disabled and
`-p no:cacheprovider`. Bundles were separate processes to avoid unrelated
replay.py import-name collisions.

| Bundle | Passed |
| --- | ---: |
| normalizer | 68 |
| inverse-trace-residual | 30 |
| spectral-source | 42 |
| central-rank | 32 |
| terminal-fpt | 55 |
| rees-channel | 12 |
| prior-art | 19 |
| interacting-readout | 24 |
| bell-readout | 16 |
| ppav-source | 37 |
| smooth-repolarization | 56 |
| kernel-output | 47 |
| Total | 438 |

## Concrete Controls

The order obtained from prime-square block congruences equals the order
computed independently from the full module. Norm-13 quaternion isogenies
give an additional exact reference with known transported lattices. The
tests exercise characteristic 2 algebra and odd characteristic 3,7,11,19
orders, a 127-bit secret prime, non-Lagrangian failure, insufficient
divisibility, lift independence, and weak-mask cancellation failures.
The characteristic-2 fixture is not a geometric backend for the odd-p
source. All fixtures are algebraic; no torsion points were constructed.

The first test run exposed SymPy retaining a QQ matrix domain despite
integral entries in the independent reference lattice. Explicit validated
integer-matrix construction fixes the HNF call without rounding rationals.
A subsequent self-review added a composite auxiliary-level regression for
invertible matrices whose first column has no unit pivot.

For the p=11, ell=13 uniform-bound replay:

- Maximum physical/quaternion word lengths: 39/156.
- Public trace bound: 1587 bits.
- Shared squarefree smooth denominator: 1594 bits.
- Auxiliary primes: 188, largest 1151, omitting p and ell.

These conservative numbers are NOT a practical resource estimate. The
dimension-16 geometric quotient still has very large polynomial costs.

## Not Executed Or Claimed

No quantum HPGP learner, coherent source circuit, theta canonicalizer,
geometric repolarization, classical secret-kernel recovery, protocol break,
or quantum speedup. No independent external proof review or novelty review.

No repository-wide test run, qsearch validate, node syntax check, registry
refresh, commit, or push. Those would test or alter a different moving
checkout, not this isolated research bundle. No source/staging files were
edited. The migration coordinator PID 4829 was still running at the final
check; the verified destination quantum algorithm search still did not
exist. HANDOFF.md gives the integration tasks for a stable checkout.
