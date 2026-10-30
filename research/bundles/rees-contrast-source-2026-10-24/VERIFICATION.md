# Verification, 2026-10-24

Executed in the external research-work directory, not the migrating repo:

```
/opt/anaconda3/bin/python -m pytest -q -W error \
  rees-contrast-source-2026-10-24/test_contrast_source.py \
  rees-coarse-spectrum-2026-10-24/test_coarse_spectrum.py \
  rees-code-support-2026-10-24/test_code_support.py \
  rees-spectral-mixture-2026-10-24/test_spectral_mixture.py
```

108 PASS in 0.42s: 31 new and 77 predecessor tests, no skips. Warnings are
errors. `py_compile` passes for all three new Python files.

`python run_audit.py --output receipt.json` executed. A fresh in-memory
replay matches the saved JSON exactly. All nine new/local dependency
hashes and all eleven hashes in the preceding coarse-source receipt match.
Receipt SHA256:

    a8ea071e922ff92e711df8d3d08cfe4138f2e89b5029d7edadf8dad29c6ad0fe

The symbolic diagonal full-rank control has D=2^256 and 80% uniform
background mass. No D-dimensional matrix or sample table was allocated.
The noncommuting control uses a literal 27-dimensional active block and
an implicit scalar complement, D=2^40. Its contrast residual is
0.0001953125 (allowed 0.000390625), coarsening error 0.0010416984579932963
(bound 0.003515625), and minimum outside trace distance
0.19996745586977815 (promised 0.1). The retained rank is three and the
original, packet and expected nonnormal subgroup agree. This is an easy
finite control, not a native-scale quantum computation or hard application.

The conservative copy ledger has 102 decimal digits. It was COMPUTED,
not executed. The classical sample bound and count classifier are present;
the Luks stabilizer backend remains cited and unimplemented.

Not done: independent review of this extension, novelty certification,
formal verification of this extension, a full quantum implementation,
main-repository test/CLI/UI/registry checks, Git edits/commits/pushes, or
migration repair. The verified local checkout was still absent. All owned
processes finished. No additional sub-agent was used.
