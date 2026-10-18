# Circuit search

Empirical search over small readout circuits, next to the theory loop. Outputs go to
`research/audits/`. Nothing here writes to the registry. Results are notes for the
research agents to evaluate.

## DCP readout (`dcp_readout.py`)

```bash
python tools/circuit_search/dcp_readout.py                          # all instances
python tools/circuit_search/dcp_readout.py --instances mod64 --restarts 20
```

The script writes `research/audits/circuit_search_dcp_readout.json` and
`CIRCUIT_SEARCH_DCP_READOUT.md`.

**Setting.** Each packet is one qubit, rho(theta, gamma) = (I + gamma cos(theta) X + gamma
sin(theta) Y) / 2. This matches
`theorems/dcp_multi_packet_collective_helstrom_product_likelihood_bridge.py`. The task is
binary: secret 0 against secret s*. The secret is either known, or its sign is unknown and
the hypothesis averages s* and -s*. Scores are total-variation distances between outcome
laws, and success = (1 + TV) / 2.

**Search spaces.** Every receiver uses one single-qubit rotation per wire, a Z measurement
and classical feed-forward, with no entangling gate:

- Product: each wire is measured along its own direction.
- Adaptive: wires are measured in sequence, and each direction depends on the earlier
  outcomes. All wire orders are tried.

Both are optimized with Nelder-Mead and Powell from 12 seeded restarts. Each two-packet
instance and setting evaluates about 45,000 circuits, and each three-packet one about
480,000. Two bounds come from SDPs (semidefinite programs)
rather than search:

- **Collective** is the Helstrom optimum over all joint measurements.
- **PPT bound** is the best measurement whose effects stay positive under partial
  transpose across every cut. Every local protocol is such a measurement, including
  two-way, multi-round and POVM-based ones. So this is an upper bound on all of them. The
  bound is certified: the solver's dual is repaired into a feasible dual solution and
  the residual eigenvalue is added, so it rests on floating-point eigenvalue accuracy,
  not on solver tolerance. The test suite checks the certificate against the primal
  value. The reported PPT bound is the smaller of this certificate and the collective
  value, which is itself an upper bound on every measurement.

### Findings (seed 0, 12 restarts)

**Known secret, the recorded mod-64 instance (headers 16 and 17, secret 1, pure packets).**
A two-step adaptive local circuit reaches 0.8801, the collective optimum. It measures wire
0 in the XY plane, then wire 1 in a direction chosen by the first outcome. So for this
instance the collective advantage over the X-basis product disappears once one bit of
classical feed-forward is allowed. This is the known theorem that LOCC (local operations
and classical communication) reaches the Helstrom bound for any two pure multipartite
states (Virmani, Sacchi, Plenio, Markham, Phys. Lett. A 288, 62 (2001)). The bridge note
says it "does not compare against the optimal adaptive/separable receiver". This run
supplies that comparison.

| Comparison | Score |
|---|---|
| X-basis product | 0.7745 |
| Product of local Helstrom readouts | 0.7410 |
| Best product with free local directions | 0.8483 |
| Best one-way adaptive | 0.8801 |
| Collective | 0.8801 |

**Mixed packets show a certified local gap.** The known-secret three-packet instance has
gammas 0.85, 0.8 and 0.75. Its collective optimum is 0.6993, and no local protocol of any
kind exceeds 0.6895, a certified gap of 0.0098. The one-way adaptive search reaches 0.6868.

**Unknown sign.** Sign symmetrization makes H1 a mixture.

| Instance | Best adaptive | PPT bound | Collective | Status |
|---|---|---|---|---|
| three_packet | 0.6263 | 0.6263 | 0.6369 | Adaptive search is optimal among local protocols to within 4e-6. Certified gap 0.0106. |
| two_packet | 0.4967 | 0.5122 | 0.5143 | Certified gap 0.0022, with an open window of 0.0155. |
| mod64 | 0.7745 | 0.8305 | 0.8305 | Open. The PPT program's primal solution, a PPT and so (on two qubits) separable measurement, comes within 1e-7 of the collective score. That rests on solver precision, not on a certificate. Whether LOCC reaches it is undecided: the search found nothing above the X basis. |

### Scope

- The instances are small, with at most three packets. The gaps are 0.002 to 0.011 in TV.
  Nothing here is asymptotic.
- "Best adaptive" is a search result, so it is a lower bound on the one-way adaptive
  optimum. Only the PPT column and the collective column are bounds.
- An open window is the range that a richer local protocol could still gain: multi-outcome
  POVMs per wire, or two-way rounds.

## Tests

```bash
python -m pytest -q tests/tools/test_circuit_search.py
```

The tests do the following:

- Reproduce the three recorded mod-64 scores to 1e-12.
- Check the analytic outcome law against a density-matrix circuit simulation.
- Check that adaptive search reaches Helstrom on random pairs of pure product states.
- Check the PPT certificate.

The PPT tests need `cvxpy`, and are skipped without it.
