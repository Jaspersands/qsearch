# Evenly spaced Gaudin eigenstate preparation

2026-11-12. CLOSED scoped attempt; full-interval candidate remains OPEN and
is parked pending a new proof mechanism. No quantum implementation.

## Selection from independent directions

Start STATE/TRAPS after the closed surface source audit. Corpus lookups first:
modular-form Hecke coefficients, integral module isomorphism and Gaudin gaps;
focused saved lookups are audits/selection/2026-11-12/gaudin_picket/.
The baselines catalog returns tensor networks, not a matched sampler theorem.
Actual sources then checked: Bruin, Computing coefficients of modular forms,
Theorem1.1 (https://pub.math.leidenuniv.nl/~bruinpj/coefficients.pdf), already
pays classical polynomial coefficient evaluation under GRH for fixed n0 and
squarefree variable n1, with factored index and explicitly specified eigenform.
Adding Shor factoring there is a known arithmetic composition, no new mechanism.
BHJ's retained primary paper, introduction hypothesis(H)/Theorem, covers split
semisimple quotients for lattice isomorphism. The general division-component
extension needs an unpaid noncommutative principal-ideal algorithm; no concrete
new endpoint was identified. Neither rejection asserts a general impossibility.

The selected question is instead the quantitative JOINT spectrum of an
explicit interacting family: a bound would complete an already paid quantum
preparation mechanism, not create another subsystem. This has external value
for highly excited integrable states. Latest arXiv2503.21741 remains v3
(March12,2026), checked Nov12. Actual local v3 Eq12/13, sections7/8 and AppendixH
still leave the finite-coupling same-sector bound open; numerics and small Smale
bounds do not answer it. The prior nonuniform two-cluster counterexample does
not satisfy this pass's evenly spaced geometry.

## Native candidate and obligations

Even N; initial bit label b of weight N/2; rational target t in[0,1]; desired
trace distance eta. Sites eps_i=i/N and physical coupling g=t/N, so

    Q_i(t)=n_i+(t/2) sum_{j!=i}(SWAP_ij-I)/(i-j), n_i=(I+Z_i)/2.

Output: the joint eigenstate continuously followed from b. No charge values,
Bethe roots, eigenvector, conditional norms, branch oracle or target-dependent
parent Hamiltonian are supplied. Mechanism: GAUDIN_JOINT_CHARGE_TRAVERSAL.md's
random evolution under all commuting charges and fine eigenpath projection.
Individual Pauli norms/derivatives are O(logN), total O(NlogN); input/precision
and all random-time simulation costs remain charged as in that theorem.

Single decisive obligation: absolute c>0 and finite C such that EVERY pair of
distinct half-filled joint branches and EVERY t in[0,1] has

    sum_i (q_i(t)-q'_i(t))² >= c*N^(-C).

This would give poly(N,1/eta) preparation. Expected upside is efficient quantum
access to arbitrary interacting eigenstates for a fully specified family;
there is NO established classical lower bound or separation. Classical
baselines: binomial(N,N/2)-dimensional diagonalization, eigenvalue-based Bethe
continuation, MPS with charged bond dimension, and determinant prefix sampling
only where every conditional norm is paid. Efficient roots or single amplitudes
do not by themselves yield a full quantum state or a classical sampler.
Falsifiers: an exact same-sector collision, superpolynomial true JOINT spacing,
unpaid coefficient/precision/branch resources, or a matching classical sampler.
A violation of the old1/N conjecture alone does not falsify this weaker target.
No all-N claim may follow from finite diagonalization or solver convergence.

## Cheapest analytic control: a rigorous perturbative interval

Let H=H_(N-1) and h_i=H_(i-1)+H_(N-i)<=2H. Since ||SWAP-I||=2,
||Q_i(t)-n_i||<=t*h_i. For 0<=t<=1/(8H), each spectrum lies in two disjoint
intervals [b_i-1/4,b_i+1/4]. Its two spectral projectors vary continuously.
Because all Q_i commute, their products give continuous joint projectors;
at t=0 each bit product has rank one, so its integer rank remains one on the
whole interval. Each branch is uniquely labelled by its bit string there.
Two distinct labels in the same weight sector differ in at least two positions;
each such charge differs by at least1/2. Thus the squared SAME-sector joint
gap is at least1/2 throughout this interval. This is a direct Weyl/continuous-
projector argument, not finite evidence; the existing traversal pays it.

For a classical small-t control, the traversal's derivative estimate gives
||v'(t)||<=L/kappa<=2*sqrt(2N)*H in parallel gauge. Hence the unchanged product
state has trace distance <=2*sqrt(2N)*H*t; computational samples are matched
by outputting b when t<=min{1/(8H), eta/(2*sqrt(2N)*H)}. More sharply, the
sampling TV error is exactly 1-|<b|v(t)>|², hence at most8NH²t². Thus deterministic
output b pays sampling error eta for t<=min{1/(8H),sqrt(eta)/(2*sqrt(2N)*H)}.
These are sufficient regimes, not optimality claims. They must not be extended
to t=1. The independent classical review checked both bounds; neither resolves
the full candidate.

## Checked classical sampler audit and exact prefix falsifier

Independent review audits/reviews/2026-11-12-gaudin-picket-classical.md is
complete and parent-read, including its actual source sections. Native charge
tracking still lacks uniform step/conditioning/branch guarantees. Even granting
it, determinant formulas for specified amplitudes, full on-shell norms and
local observables do not supply all conditional Born probabilities. The literal
root-subset MPS/Gram construction is exponential at M=N/2; this is not a lower
bound on every representation or sampler.

The norm-deletion shortcut fails INSIDE this exact family. Let two real on-shell
rapidities be v1,v2, d=v2-v1, a_i=1/(v1-eps_i), b_i=1/(v2-eps_i). For a site
set U, let A=sum a_i², B=sum b_i², K=sum a_i*b_i. Directly summing the physical
two-particle amplitudes gives Z_U=AB+K²-2(A+B-2K)/d², while the proposed
deleted Gaudin determinant is AB-2(A+B)/d². Full on-shell equations imply
K_full=-4/d². Deleting one site e therefore gives the exact discrepancy

    Z_U-detG_U=(v1+v2-2e)²/[d²(v1-e)²(v2-e)²].

For N4, occupation label0101, eps_i=i/4 and g=t/4, the real implicit-function
branch has v1=1/2+t/8+O(t²),v2=1+t/8+O(t²). Deleting FIRST site e=1/4 is the
empty-prefix event; discrepancy tends to1024/9 and is positive for all sufficiently
small t>0. Root existence follows by scaling displacements u=(v-eps)/g: at
g=0 each equation is1/u=2 with invertible Jacobian. This is an actual native
on-shell branch, not arbitrary off-shell data. Parent independently derived
the norm identity and checked the limit. Relative error can vanish as t->0;
this disproves exact determinant reuse, not approximate sampling or hardness.

## Independent work and next test

Two distinct paid obligations under audits/api_inputs/2026-11-12-gaudin-picket/:
OpenAI constructive full-interval inequality; Claude asymptotic counterfamily.
Both have the exact native contract and actual v3 excerpts; no archives or
credentials. Claude terminated max_tokens with an EMPTY report,32768 output
tokens, estimatedUSD0.715176; no result and no retry. OpenAI also terminated
max_output_tokens with an EMPTY report:48000 reasoning/output tokens,
estimatedUSD2.503510. Its process is gone; no report or retry. Combined runner
estimateUSD3.218686, not an invoice/balance. Neither supplies mathematical
evidence. The independently reviewed weak-window theorem and SAME-family
prefix falsifier are the actual results of this pass.
The separate internal classical review is complete as recorded above.
No full-interval proof or counterfamily was obtained. Reopen only with a new
quantitative mechanism, not larger retries or another nearby gap constant.
No generic optimizer, gap sweep or quantum circuit is queued. All full-algorithm,
novelty, separation and execution gates remain false. In response to the owner's
explicit acceleration request, the next round compares three INDEPENDENT
constructive endpoints in ACCELERATED_ENDPOINT_SELECTION.md; six distinct API
obligations are dispatched concurrently, with no Gaudin retry.
