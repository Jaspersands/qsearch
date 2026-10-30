# Verification: 2026-10-25

25 focused tests PASS. Combined with the preceding hidden-mode bundle:
69 tests PASS. Three Python syntax checks PASS. Exact write/check replay
PASS, including five sampling cases up to m=64,R=7,L=2, optional X-basis
output, and a signed-path control.

Commands, from this directory:

    /opt/anaconda3/bin/python -m pytest -q
    /opt/anaconda3/bin/python -m pytest -q ../hdqi-hidden-mode-access-2026-10-25/test_mode_access.py test_word_sampler.py
    /opt/anaconda3/bin/python -m py_compile word_sampler.py test_word_sampler.py replay.py
    /opt/anaconda3/bin/python replay.py write
    /opt/anaconda3/bin/python replay.py check

Receipt SHA256:
33704f98675d2e685b2eb49536126f3afc339a35fb0c3fdd137c1abada1a3341

The backend, normalization, conditional masses and random rational coins
use exact arithmetic. Every conditional mass is separately compared with
exhaustive suffix sums on bounded fixtures; dense Pauli controls compare
all signed amplitudes, not just probabilities or spectra. Zero-vector
products are rejected. Thermal approximation uses the separate written
repeated-transfer bound; arbitrary transfer products are not called thermal.

No complex-parameter/rational-compression compiler is implemented here.
The quasipolynomial extension in the note is conditional and unreviewed.
No advantage or general polynomial thermal sampler is claimed. No main,
staging, CLI/UI, registry, Git, migration or automation edits. Main tests
and qsearch validation were not run. No subprocess remains for this bundle.
