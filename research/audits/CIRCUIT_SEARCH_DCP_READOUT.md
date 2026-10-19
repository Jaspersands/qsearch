# Local Readout Search on DCP Phase Packets

Generated 2026-10-19 by `tools/circuit_search/dcp_readout.py` (seed 0, 12 restarts per search). Not a registry entry; for the research agents to evaluate.

Scores are total-variation distances between the outcome laws under H0 and H1 (success = (1 + TV) / 2).
Product and adaptive receivers use one single-qubit rotation per wire, a Z measurement and classical
feed-forward. No entangling gate is used. Collective is the Helstrom optimum over all joint measurements.

PPT bound is a certified upper bound on every local protocol, including two-way and multi-round ones:
the best measurement whose effects stay positive under partial transpose across every cut, solved as an
SDP and certified by a repaired dual solution. Certified gap = collective - PPT bound: no local protocol
of any kind gets closer to the collective score. Open window = PPT bound - best adaptive: the range a
richer local protocol than this search covers could still gain.

## Known secret

| Instance | X basis | Local Helstrom product | Best product | Best adaptive | PPT bound | Collective | Certified gap | Open window |
|---|---|---|---|---|---|---|---|---|
| mod64 | 0.7745 | 0.7410 | 0.8483 | 0.8801 | 0.8801 | 0.8801 | 0.0e+00 | 0.0e+00 |
| single | 0.2125 | 0.4250 | 0.4250 | 0.4250 | 0.4250 | 0.4250 | 0.0e+00 | 0.0e+00 |
| two_packet | 0.4763 | 0.5657 | 0.5895 | 0.6147 | 0.6147 | 0.6147 | 0.0e+00 | 0.0e+00 |
| three_packet | 0.5746 | 0.6495 | 0.6698 | 0.6868 | 0.6895 | 0.6993 | 9.8e-03 | 2.7e-03 |

## Unknown sign of the secret

| Instance | X basis | Local Helstrom product | Best product | Best adaptive | PPT bound | Collective | Certified gap | Open window |
|---|---|---|---|---|---|---|---|---|
| mod64 | 0.7745 | - | 0.7745 | 0.7745 | 0.8305 | 0.8305 | 0.0e+00 | 5.6e-02 |
| single | 0.2125 | - | 0.2125 | 0.2125 | 0.2125 | 0.2125 | 0.0e+00 | 0.0e+00 |
| two_packet | 0.4763 | - | 0.4763 | 0.4967 | 0.5122 | 0.5143 | 2.2e-03 | 1.5e-02 |
| three_packet | 0.5746 | - | 0.5783 | 0.6263 | 0.6263 | 0.6369 | 1.1e-02 | 4.0e-06 |
