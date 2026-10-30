# Scope And Mechanical Handoff

This bundle is outside the migrating checkout. Do not integrate until the
intended local repository copy is verified. No Git commit, UI/CLI change,
candidate admission or experiment campaign is needed for this result.

## What Changed Scientifically

The full native HDQI word distribution does not inherit the flux chain's
small-influence proof. The exact three-generator path has C_13=C_31=1
and influence spectral radius >1 at every beta>0, despite the unconditional
small-occupation bounds. This defeats uniform weighted Dobrushin criteria,
not the underlying chain, other samplers, or the existing flux theorem.
The same fixture and all its tensor products are classically easy.

The written extension applies to any graph with an induced three-vertex
path and nonzero path couplings, at all positive temperatures outside a
locally finite exceptional set. This includes connected extensive-cycle
line graphs. Its worst-boundary conditioning can be rare and does not
imply slow mixing. A separate L(K_4) integer-power control checks the
extension's first nonzero coefficients and exact parity zeros.

The written all-temperature proof is in OUTPUT_PINNING.md. The Python
files are finite EXACT controls, not production samplers or a proof
assistant certificate. No use of a dense eigensolver or zero tolerance
establishes a theorem here. The three-point temperature list is fixed
regression coverage, not a parameter-search recommendation.

## Reproduce

In this directory with /opt/anaconda3/bin/python:

    python -m pytest -q -W error test_pinning_control.py
    python -m py_compile pinning_control.py test_pinning_control.py replay.py
    python replay.py --write
    python replay.py --check

replay.py hashes five source files and three external context notes. It
does not read or modify the migration-sensitive checkout. Main repository
tests, qsearch.py validate and node --check were not run for this bundle.

## Next Gate, Not A Wiring Queue

Any future output-bit coupling must explicitly handle positive pins and
exact zero amplitudes. Do not use the unconditional inclusion theorem as
a conditional domination statement. If using amplitude-only simulation,
price amplitude evaluation and check the actual algorithm's hypotheses;
the Gaussian flux expression is not a polynomial amplitude oracle at
extensive cycle rank. The known easy six-atom family must remain a
negative control against claiming hardness from failed Dobrushin bounds.

Do not build more three-site tests or a new general-purpose workbench.
The next research task remains constructive full-output sampling on the
same connected extensive-cycle inputs, or a useful native task surviving
the existing classical readout comparisons. Neither was solved here.
