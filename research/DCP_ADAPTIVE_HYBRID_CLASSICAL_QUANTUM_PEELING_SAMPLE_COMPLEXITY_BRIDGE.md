# DCP Adaptive Hybrid Classical-Quantum Witness Peeling and Sample-Complexity Bridge

## V1 Dominance And Sample-Ratio Claims Retracted (2026-10-17)

V1 assigned classical bias gamma^h and quantum bias p_match*gamma^h, then
compared their squared inverses. It supplied no classical measurement with
that first bias and discarded the quantum acceptance flag. That algebra is
not an access-matched receiver comparison or a DCP sample-complexity theorem.

## Native Input And Actual Competitors

Public A over Z/(2^t), nonzero binary witness v, h selected phase qubits:
`rho_i=(I+gamma*(cos(theta_i)X+sin(theta_i)Y))/2`, with unknown
`theta_i=2*pi*<a_i,s>/q` and independent original Z noise. Finding v,
acquiring the pool and other reduction costs are NOT provided for free.

Independent X measurements followed by parity have mean
`gamma^h*product_i cos(theta_i)`, not `gamma^h*cos(sum_i theta_i)`.
For two pi/2 phases the former is0 and the latter-1. Classical modular samples
with first characteristic gamma*exp(i*theta_i) WOULD multiply that way, but
the native qubit input does not supply those samples.

A legal single-copy separable protocol chooses uniformly among product X/Y
measurements with an even number of Y axes, then multiplies its outcome by
`(-1)^(#Y/2)`. Its mean is
`2^(1-h)*gamma^h*cos(sum_i theta_i)`, by expanding the real part of
`product_i(cos(theta_i)+i*sin(theta_i))`. Every packet consumes h source
qubits. This is one competitor, NOT a lower bound on all separable/adaptive
measurements or on classical processing of the full raw data.

## Public Coherent Circuit And Full Native Law

The module now exports AND executes a fixed star-CNOT readout: CX(0,j) for
j>0, H on0, then Z measurement on all wires. It does not know s, invert the
source, or synthesize a secret-dependent rotation. A measured syndrome d
has probability2^(1-h) and effective label

    a_eff = a_0 + sum_{j>0}(1-2*d_j)*a_j mod q.

The retained target's conditional X mean is `gamma^h*cos(2*pi*<a_eff,s>/q)`.
All labels, syndromes and X outcomes are retained. Computing the realized
label costs O(n*h); the circuit costs h-1 CX and one H. Its small reference
law enumerates2^(h-1) branches, NOT all2^K anchors including unused wires.
That exhaustive count is NOT needed to execute the circuit.

Keeping only labels a_eff=+/-A*v gives p_match, but other branches are not
proved useless. This filter is a deliberate coarsening, not the full receiver.
V1's mod8 all-ones h3 count p_match=1/4 is correct; its claimed16x universal
penalty is not. Mod2 remains a genuine classical-X control because all phases
are0 or pi. That equality does not transfer to growing two-power moduli.

## Retaining Erasures Changes The Cost

For a COARSENED target-cosine parameter mu, let g=gamma^h. The flag law is
`P(+,keep)=p*(1+g*mu)/2`, `P(-,keep)=p*(1-g*mu)/2`, `P(erase)=1-p`.
Its local Fisher information is `p*g^2/(1-g^2*mu^2)`.
Replacing erasures by fair coins instead gives `p^2*g^2/(1-p^2*g^2*mu^2)`.
At mu=0 the acceptance penalties are1/p and1/p^2, respectively. At p=1/4
these are4 and16, not an unavoidable16 for flagged observations.

This is a local statistical experiment, NOT a complexity theorem for the
discrete DCP secret, full multi-frequency data, adaptive protocols or optimal
measurements. For zero target the matched cosine is constant and the module
does not attach a fictitious secret-information proxy. Zero visibility gives
zero signal and null inverse-information fields, not JSON infinity.

## Verification And Scientific Decision

Twenty-two checks include independent native density matrices and actual
CX/H matrices for every secret in the selected one/two-component fixtures,
all Born outcomes, exact rational derivatives of the flag/coin laws, explicit
product-Pauli operators, mod2 equality, ignored-wire accounting and a64-wire
linear gate-plan check. JS independently checks the counterexample and
three-outcome information law. These are numerical finite calibrations, not
an asymptotic theorem or scalable decoder. No general negative is registered.

Portfolio rechecked: [rank-metric DQI](https://arxiv.org/html/2606.04843) does
not claim an advantage for its Gabidulin construction, and the
[quadratic-DQI preparation theorem](https://arxiv.org/html/2510.08061) carries
an explicit author correction invalidating Algorithm1/Theorem1. Neither is
an automatic implementation target. DCP remains a reserve until an actual
finder/recovery method, not this readout alone, supplies an end-to-end path.
