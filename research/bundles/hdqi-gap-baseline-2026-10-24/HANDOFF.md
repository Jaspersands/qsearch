# Handoff: Do Not Rediscover The Easy Mass Regime

Read GAP_AND_BASELINE.md. The preceding filtered parent now has an explicit
all-orders gap bound in a TOTAL-MASS regime:

    r=(sqrt(5)/2) exp(1/8) beta sqrt(sum_i J_i^2),
    gap >= (1-r)^2 when r<1.

For disconnected graphs use the largest component mass. At r>=1 the
answer is inconclusive, not a positive square and not a slow-mixing claim.
The local proof is unreviewed; numerical values are not interval certificates.

A direct clipped spectral filter gives a stronger algorithmic comparator:
polynomial pilot preparation when beta^2 sum_i J_i^2=O(log(m/epsilon)),
with explicit cutoff, success lower bound and approximation precision.
This is a construction using standard quantum primitives, not an executed
quantum circuit or a novelty-certified algorithm. Classical-output advantage
still has no proof. The commuting 64-term control is intentionally easy.

## Next High-Reasoning Task

For unit couplings and connected graphs, focus beyond
m/(d+1)=O(log(m/epsilon)) at fixed small beta^2(d+1). The direct comparator
already covers that dense regime. Seek a genuinely global degree/local-mass
gap bound, or a full-parent small-gap family, for growing intermediate
degree and large connected mass. A larger upper cost bound for the direct
algorithm is not a lower bound against other quantum or classical methods.

The new SYK fast-mixing paper 2610.05953 is relevant technique-wise but its
Majorana/even-Hamiltonian/disorder premises were not transferred. Our Z_i
jumps commute. Do not quote its spectral gap as a theorem for this input.

If a gap proof succeeds, still supply a useful physical target/decoder or
operational measurement task and matched classical algorithms. Preparing
a quantum state alone is not a classical-task separation.

## Routine Work For Gemini

After migration and destination verification only, integrate this bundle
with both prior HDQI parent bundles. Reproduce the receipts and hashes.
Do not edit moving/staging sources, auto-admit a candidate, update speedup
status from a finite spectrum, or launch the parameter ledgers as jobs.

Derive M and Lambda from the SAME validated canonical coefficients if
wiring an input adapter. Do not accept arbitrary optimistic scalar budgets
as evidence about a physical Hamiltonian with dependent labels.

Commands from this directory:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-hdqi-baseline-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider -W error test_gap_baseline.py \
      ../hdqi-filtered-parent-2026-10-24/test_filtered_parent.py \
      ../hdqi-parent-gap-2026-10-23/test_parent_gap.py

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-hdqi-baseline-pycache \
      /opt/anaconda3/bin/python gap_baseline.py --output receipt.json

No new independent reviewer has been authorized or used for these results.
The earlier Rees review does not cover this proof or comparator.
