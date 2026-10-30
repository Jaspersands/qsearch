# Verification Boundary

Date: 2026-10-24. Interpreter: /opt/anaconda3/bin/python.

## Completed

```sh
python -m pytest -q -W error test_flux_gap.py ../hdqi-fermion-sampler-2026-10-24/test_fermion_sampler.py ../hdqi-parent-gap-2026-10-23/test_parent_gap.py ../hdqi-sign-sampler-2026-10-24/test_sign_sampler.py ../hdqi-paired-positivity-2026-10-24/test_paired_positivity.py
```

318 passed in 4.05s: 87 new and 231 predecessor tests. No skips, warnings
treated as errors. Four new Python files pass py_compile after the last
changes. Earlier 58-, 298- and 301-test runs preceded the additional controls.

`python replay.py --write` completed. A separate fresh
`python replay.py --check` passed with all eleven hashes: six local code/science/
handoff files and five frozen dependency files. The verification document,
checkpoint and receipt are excluded from that hash list. All seven source
hashes in the preceding fermion-sampler receipt remain intact.

Receipt SHA256:

    e0801165165d1d099401294b3c8c5568d919cb0e1adfc751527eabe7380fb507

The dense two-cycle adiabatic control has flux trace distance approximately
9.660e-6 and the same native pilot vector error after global-phase alignment.
This is a tiny classical dense simulation, NOT quantum execution. Its full
native state retains signed amplitudes, not just output probabilities.
Additional Gaussian controls prepare pairs and rotate their modes, then
compare signed vectors WITHOUT any global-phase alignment. Tests cover
signed couplings, zero modes, odd mode count and degenerate blocks. These
are dense finite Fock controls, not compiled quantum circuits.

The rational four-cycle sample used three heat-bath steps and 36 exact
determinants, with certified total TV upper bound 1/2. This is only a
classical FLUX sample. The native log-partition and conditional intervals
do not call a floating eigensolver or enumerate flux sectors.
The receipt's fixed seed is a reproducibility control; the mathematical
TV guarantee assumes independent random bits, not a fixed pseudorandom string.

The 256-vertex ladder has r=127, beta=1/32, and analytic gap lower bound
509/65024. No 2^127 table is constructed. The conservative coherent ledger
contains about 8.87e24 conditional rotations and 2.14e54 determinants;
these are symbolic upper counts, not executed work or elementary gate
estimates. Polynomial asymptotics are not a claim of practicality or hardness.

A four-cycle's flux probability differs from 1/2 by only about 3.97e-5.
The symbolic product of one billion independent copies amplifies the
uniform-amplitude replacement's trace distance to about 0.891. That large
product was NOT constructed and is classically factorable.

The follow-on same-output classical attack tested whether the earlier
paired-support positivity obstruction might disappear for line graphs.
It does not: the K_{2,3} root gives an exact symmetry zero with
W(full,Y)=-2A(t)^2 and leading coefficient -2t^12/2025. Three exact rational
Taylor-interval tests certify negativity at beta=1/32,1/64,1/128. This
falsifies that representation only; the witness itself is classically easy.

## Not Established

Independent proof review, formal verification, novelty, generic HDQI gap,
compiled coherent conditional arithmetic, compiled phase-consistent Gaussian
preparation, hardware execution, classical hardness, useful-task reduction,
or quantum speedup. Exact arithmetic establishes the stated interval claims;
the all-size gap and complexity arguments remain local deductions.

No Desktop/staging checkout, qsearch CLI, registry, UI, Git or migration
changes. No extra reviewer was spawned. Full-repository tests and qsearch
validation were not run against the unverified moving checkout. All owned
test and replay processes completed.
The intended /Users/jaspersands/Developer/quantum algorithm search checkout
was rechecked after the final replay and remains absent.
