# DHSP Domain-Retaining Collision Walk

Status: **LOCAL DERIVATION / REVIEW PENDING**. Physical calibration and scoped
obstructions, not a new algorithm, independent proof review or speedup claim.
No candidate has been accepted. No general DHSP lower bound is asserted.

## Why This Test Exists

The binary domain-erasure architecture in `DHSP_CODOMAIN_SAMPLE_SIMULATION.md`
can be simulated using classical label samples followed by quantum processing.
This test instead retains the domain through known left-group/Fourier hopping
and oracle-dependent phase kicks. That earlier simulation does not cover it.
The question is whether interference can funnel amplitude into two distinct
members of the same hidden coset at a cost below known algorithms.

This is an actual full-function-oracle interface, not supplied phase/coset
states, an inverse-function oracle, or an unknown coset-support reflection.
The small tables calibrate that interface; they are not efficiently generated
natural instances and do not establish a consequential problem reduction.

## Source And Public Driver

Write the dihedral group as `(b,x)(c,y)=(b xor c,x+(-1)^b y)` over Z_N,
N=2^n. Hide `h_s=(1,s)` with `f_s(b,x)=pi(x-b*s)`, one fixed output permutation
for the whole experiment. The partner of g is g*h_s. Verifying distinct
g,g' with equal function values proves g'=g*h_s; known arithmetic gives
`s=(-1)^b*(y-x)` from g=(b,x), g'=(1-b,y).

Each step is `U=C_tau D_f`. D_f applies exp(-i*gamma*v(f(g))) using two
evaluation queries: compute and uncompute. Potentials are public parity hash
or full-label cosine. The public driver has norm-one Hamiltonian
`K=(K_rot+L_0)/2`, with known left reflection L_0:(b,x)->(1-b,-x).
K_rot is diagonalized by the KNOWN cyclic QFT with even multiplier kappa(k):

| Family | Multiplier | Scope |
| --- | --- | --- |
| Local | cos(2*pi*k/N) | Nearest-rotation/reflection hops; path obstruction below |
| Dyadic | Mean of cos(2*pi*k*2^j/N), j<n | Public long-range shortcuts |
| Chirp | cos(2*pi*(k^2 mod N)/N) | Exact parity trap for odd hidden shifts |
| Lifted chirp | cos(2*pi*(k^2 mod 2N)/(2N)) | Removes that trap, not a speedup |

Since K_rot commutes with L_0,
`C_tau=exp(-i*tau*K_rot/2)*(cos(tau/2)I-i*sin(tau/2)L_0)`.
QFT, multiplier arithmetic, rotations, controls and approximation errors must
all be charged. Dense matrices here are exponential verification machinery,
not the proposed implementation. No oracle eigenbasis is given.

## Physical Two-Register Protocol

Preparation A retains two power-of-two clocks of size Q and two domains:

1. Prepare uniform clocks t_1,t_2 and a uniform first domain.
2. Apply controlled U^t_1 to the first domain.
3. CNOT its computational index into the second, initially zero, domain.
4. Apply controlled U^t_2 to the second domain.
5. Mark unequal domain inputs with equal evaluated labels; retain every branch.

Computational-index copying entangles the domains. It does NOT clone an unknown
walk eigenstate. The full A is reversible from the same oracle and public gates.
With `w_g=mean_t |(U^t |uniform>)_g|^2` and
`T_{g',g}=mean_t |(U^t)_{g',g}|^2`, unconditional success is
`p=sum_g w_g T_{g*h_s,g}`. Neither localization IPR nor a favorable conditional
energy outcome substitutes for this quantity.

For gamma!=0, binary controlled powers use at most Q-1 steps per walk. The
explicit implementation costs:

- A or A inverse: 4(Q-1) function evaluations.
- Good phase reflection: 4 evaluations, including label uncomputation.
- Each ordinary amplification iteration: 8(Q-1)+4 evaluations.
- Measured-pair verification: 2 evaluations.
- j-iteration run: 4(Q-1)+j*(8(Q-1)+4)+2 evaluations.

Gamma=0 makes preparation oracle-free, so only marker/final verification
queries remain. These counts describe this implementation, not lower bounds
against all alternative implementations. The report's `cost/sqrt(p)` fields
are diagnostic proxies using calibration success, not certified runtimes.
Unknown-success scheduling, total gate complexity and precision remain debt.

## Seeded-Walk Identity: Localization Is Not Partner Transport

Right multiplication by h_s commutes with both the public left driver and D_f.
Let `c_t^+/-=(|0,t> +/- |1,t+s>)/sqrt(2)` be hidden calibration bases and U_+,
U_- the corresponding blocks. Then, for every walk time,

`<g*h_s|U^t|g> = ((U_+^t)_{t_g,t_g}-(U_-^t)_{t_g,t_g})/2`.

For the SEEDED second-walk protocol, an eigenstate concentrated near a hidden
pair is insufficient. Its two sector return amplitudes must differ at an
accessible time. This is NOT a requirement for every two-domain strategy.
The unknown sector
transform is used ONLY to verify this identity, never as an algorithmic gate.
Small or exponentially split levels may defeat a proposed spectral readout;
this is a warning, not a universal localization theorem. In particular, an
adiabatic state constrained to the plus sector need not pay a minus-sector gap.

Finite-time phase estimation has filters
`F_k=Q^-1 sum_t exp(-2*pi*i*k*t/Q) U^t` and `sum_k F_k^dagger F_k=I`.
The workbench retains all outcomes and verifies that selecting identical first
and second energy records cannot improve UNCONDITIONAL partner probability
over retaining every second outcome. Free exact eigenprojections, duplicated
eigenstates and normalized-away postselection are excluded. This comparison
does not cover a redesigned outcome-controlled driver.

## Counterdirection: Two Fresh Preparations

Instead of copying the first domain's computational index, initialize the
second domain uniformly and run the same clocked preparation independently.
Each preparation's averaged position law w obeys w_g=w_{g*h_s}, since the input
and operations preserve right hidden symmetry. Actual collision probability is
then `sum_g w_g*w_{g*h_s}=sum_g w_g^2`, the IPR of the UNCONDITIONAL law. The
two preparations are actually executed and inverted; no unknown-state copy is
granted. Their oracle cost is the same 4(Q-1) as the seeded protocol.

This is a genuine limitation of the sector-return framing: reproducible
concentration into the same hidden pair could work without partner transport.
The odd-shift chirp has ZERO seeded transport but POSITIVE fresh-preparation
collision yield. The parity trap is not a no-go for independently seeded
preparations. All pilot fresh-preparation yields still lose the matched birthday
baseline. The local path proof below also gives `p_fresh<=max_g w_g`; it therefore
screens this alternative for polynomial-time LOCAL preparation.

Random conditional localization does not suffice. A uniform-domain evaluation
and measured function label already gives an exact coset state with one query.
Its conditional position IPR is1/2. Two fresh executions produce independently
chosen labels: records match with probability1/N and partners appear with
UNCONDITIONAL probability1/(2N), not1/2. Averaging conditional IPRs before
accounting for record alignment introduces a spurious factorN. All three exact
countercontrols retain this distinction. A mechanism targeting the SAME outcome
must pay its conditional preparation or matching cost.

A charged benchmark prepares a PUBLIC desired label y=0 by known uniform-state
Grover diffusion and a two-query label marker. Two fresh preparations can then
recover a partner with probability near1/2, but require O(sqrt(N)) queries. No
inverse-function or coset-state cloning primitive was supplied.

Its alternative interpolating Hamiltonian is
`H(t)=I-(1-t)|uniform><uniform|-t P_{f=0}`. In the symmetry-protected plus sector,
the active two-dimensional gap is
`sqrt(1-4(1-1/N)t(1-t))`, with minimum1/sqrt(N). At t=1 the full-space gap is
zero while the protected plus-sector gap is one: a minus-sector degeneracy is
not automatically an adiabatic obstruction. However symmetry protection does
not eliminate the Grover-scale gap at t=1/2. The workbench checks these spectra;
it does NOT implement or certify an adiabatic schedule. Nor is this a lower
bound for other full-function algorithms using more than this label marker.

## Two Scoped Cuts

### Exact Naive-Chirp Parity Trap

For N divisible by four, `(k+N/2)^2=k^2 mod N`. The chirp multiplier has period
N/2, so its Fourier hopping preserves x parity. L_0 and diagonal oracle phases
also preserve it. An odd hidden shift has its partner in the opposite parity
class: SEEDED second-walk success is EXACTLY ZERO for any time or potential in
this architecture, not for the fresh-preparation alternative above.
The report preserves the tiny roundoff residual but records exact zero rather
than treating it as evidence. Lifting the chirp modulus removes this invariant
only; it supplies no efficiency theorem.

### Local-Driver Path Obstruction

Only for the LOCAL nearest-rotation/reflection driver, take tau<=1 and at most
a=Q-1 steps. Arbitrary diagonal kicks change phases, not hop support. In the
interaction picture, truncate the Dyson series at R=8(Q+n) hops. Norm(K)<=1
gives remainder at most

`sum_{r>R} a^r/r! <= (3a/(R+1))^(R+1)/(1-a/(R+2)) < 2^-R <= epsilon`,

where epsilon=2^-(n+8), using e<3. The truncated operator has norm <=1+epsilon.
Known left words of length<=R lie in a ball of at most V=min(2N,4R+2) elements.
Acting on uniform input, Cauchy-Schwarz and `(x+y)^2<=2x^2+2y^2` give
`w_g <= 2(1+epsilon)^2 V/(2N)+2epsilon^2`.

The relative left word connecting g to g*h_s is
`g*h_s*g^-1=(1,2x+(-1)^b s)`. Its length is cycle_distance(2x+(-1)^b s)+1.
At most min(2N,8R+4) domain points have a partner within the ball; the rest
have transition probability <=epsilon^2. Therefore

`p <= min(1,min(2N,8R+4)*w_max+epsilon^2)`.

For the two-fresh-preparation alternative, `p_fresh=sum_g w_g^2<=w_max`,
so the same polynomial-time local driver is also inadequate there.

This is POINTWISE in hidden shift, labeling and diagonal potential; no random
permutation average is needed. For polynomial Q it decays as poly(n)/2^n.
j ordinary amplification iterations have success <=min(1,(2j+1)^2*p).
The exact ledgers use Q=j=n^2. Total composed implementation trace error must
be ADDED. An error budget of 10^-6, for example, prevents claiming an
exponentially tiny physical probability from the ideal bound alone.

This proof requires independent review. It does not cover dyadic/chirp drivers,
other initial states/protocols, nonlocal domain operations, or general DHSP.

## Oracle-Free Preparation Is A Restricted Grover Route

For any oracle/secret-independent A, including arbitrary entangled ancillas,
the N collision predicates partition cross-layer domain pairs. Each cross-layer
pair determines exactly one value `s=(-1)^b*(y-x)`; same-layer distinct pairs
never collide. Consequently `sum_s p_s<=1` and uniform-shift mean success
is <=1/N. Ordinary A/marker amplification obeys
`mean_s success_j <= min(1,(2j+1)^2/N)`.

Equivalently, the clean collision marker is equality testing against one
unknown key s after a known reversible arithmetic change of basis. This cuts
oracle-independent preparation plus ordinary amplification, not algorithms
that retain information from other full-function evaluations. In particular,
it says nothing against standard DHSP coset-state processing.

For these phase-free drivers specifically, shift-averaged success is exactly
`mean_{t<Q} sin^2(t*tau/2)/N`, independent of kappa. All hidden shifts are
enumerated in 12 finite controls. A good individual shift can therefore conceal
a poor source-average; filtered instances are not an acceptable scaling claim.

## Results And Attempts To Falsify The Direction

Pilot: N=8,16,32; two fixed seeds per N; four drivers; two potentials; Q=8,
tau=.75, gamma=1.2 committed before drawing the source. Same fixed permutation
is used across calls. All 48 controls lose to an exact classical birthday
attack at the same unamplified evaluation budget. That attack draws r distinct
uniform inputs independently in each group half and has success
`1-binomial(N-r,r)/binomial(N,r)` (or one when 2r>N), for ANY fixed shift.
Several small controls are already cheaper to solve by querying the full table.

Every nonzero pilot also loses on the amplification QUERY proxy to the same
phase-free public driver. This comparison is not a total gate-time bound or a
classical simulation: phase-free preparation and repeated drivers still cost
gates. Likewise a measured/dephased driver is a legal quantum baseline, not
automatically an efficient classical sampler for every dense Fourier kernel.

Four explicit coherent amplification controls execute A, A inverse, the
label-only marker and the all-zero reflection, rather than inserting the
amplification formula. One reaches approximately .927 success after two
iterations, but costs more than full-table classical recovery. It is a
physical correctness control, not a promising algorithmic result.

The fixed-Q mean pilot probabilities decrease roughly with 1/N, but three tiny
sizes and six sources are NOT an asymptotic fit or a typical-source theorem.
There is no evidence of a useful random-disorder funnel. Deprioritize generic
parameter tuning and nearest-neighbor localization. The remaining high-variance
target is a justified, public, nonlocal mechanism that creates polynomial-time
sector return contrast OR reproducible unconditional pair concentration, with
verified collision yield on unfiltered sources.

## Next Research Gates

1. Independently review the Dyson/word-ball argument and disjoint-marker bound.
   A legal phase kick changing hop support, a larger required word ball, or an
   allowed ancillary procedure invalidating the preparation assumptions falsifies
   the corresponding claim. Do not repair a failed bound by broadening its scope.
2. Specify a structured nonlocal driver or adaptive interference mechanism and
   derive sector return contrast or reproducible unconditional pair concentration
   BEFORE commissioning wide parameter searches. Conditional records must align
   with charged cost; independently regenerating a random coset does not align them.
   Hidden-shift-dependent gates or unknown support reflections kill the proposal.
3. Prove unfiltered success and total preparation/amplification costs as n grows,
   including unknown-success scheduling, rotations and error accumulation.
   An exponential clock, rare normalized acceptance or selected shifts kills it.
4. Compare against exact birthday recovery, phase-free marker search, available
   classical reconstruction, and Kuperberg/Regev-style baselines under identical
   access promises. Beating a tiny classical table does not qualify.
5. Give a consequential natural reduction with input-generation and error costs.
   Arbitrary random table promises remain calibration, not a breakthrough target.

Gemini owns CLI/registry integration, large held-out sweeps and full production
validation. GPT should pursue the mathematical nonlocal mechanism or move to a
better justified source/reduction, not spend its budget wiring this prototype.

The separate [Singer source audit](SINGER_RESIDUAL_HARDNESS.md) now examines a
natural finite-geometry alternative: classical normal extraction leaves a known
Shor/quasi-polynomial DLog residual, while growing-field membership access has
its own query/offset costs. It is not a decoder for this random-label walk source
and supplies no transfer of its bounds to generic DHSP.

## Artifacts And Sources

Prototype: `theorems/dhsp_domain_collision_walk.py`; focused tests:
`tests/test_dhsp_domain_collision_walk.py`; report:
`research/phase_workbench/dhsp_domain_collision_walk.json`; independent numerical
and rational checker: `research/certificates/dhsp_domain_collision_walk_crosscheck.js`.
Contract and source inspection scope are recorded in their matching hypothesis
and literature-audit files. The independent checker is not independent human
theorem review.

Focused tests:29 passed; related five-suite regression:165 passed in1.51s.
Python/JS syntax and four strict JSON records verified. Full production tests,
CLI integration and qsearch validation are deliberately delegated, not claimed
green; the prior writer omissions are not repaired by this pass.

[BHMT amplitude amplification](https://arxiv.org/abs/quant-ph/0005055) motivates
charging A and A inverse; [BBHT searching](https://arxiv.org/abs/quant-ph/9605034)
is a search comparator, not a general DHSP lower bound.
[Kuperberg DHSP](https://arxiv.org/abs/quant-ph/0302112) supplies the established
subexponential comparison target. [MNRS](https://arxiv.org/abs/quant-ph/0608026)
requires a costed walk/reflection interface; this Floquet protocol has NOT been
shown to satisfy its algorithmic framework.
[Dihedral walk localization](https://arxiv.org/abs/2006.08992) concerns a different
walk's position statistics and does not establish hidden-reflection recovery.
These sources were inspected at abstract level in this pass; the local
identities and bounds above are local derivations, not quoted paper theorems.
