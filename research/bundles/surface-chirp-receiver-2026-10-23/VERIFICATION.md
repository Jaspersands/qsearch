# Verification

2026-10-23. Isolated research bundle; source/staging were not modified.

- 18 receiver tests passed in 9.86 seconds.
- The 24-test classical baseline dependency was rerun separately.
- All four new Python files pass py_compile.
- Exact polynomial controls cover translation and quadratic cancellation
  at primes 3,5,7,11; public equation processing also passes at 2^127-1.
- Qiskit interference controls cover the full p=3 phase/compatible-weight
  family and additional padded-prime circuits through p=13.
- Dephasing reduces the equation-support probability to 1/3 at p=3.
- Native-oracle fiber replay recovers all five fixed control inputs, including
  top-coordinate input requiring rejection of three bad charts.
- Fake row answers cannot bypass the original-oracle certificate.

Replay ideal source-copy counts are 206,50,28,32,340, each below 1536.
Actual exponential classical fiber-table query counts are separately
324,162,1250,1250,405. Each successful replay uses three original-oracle
verification calls. These counts must NOT be conflated in comparisons.
The replay fingerprints six local files and three imported helper files.

What ran: finite post-query quantum state and measurement simulation in
Qiskit 2.3.0. What did not run: a coherent native-oracle circuit, geometric
source, scalable prime-Fourier gate synthesis or quantum hardware.

This pass has 42 targeted passing tests across two isolated suites. The
preceding 224-test milestone is historical; the unrelated suites were not
rerun here. No full-repository validation, commit, push or UI update occurred.
Independent proof/prior-art review and real-source checks remain open.
