# Campaign Negative Claims: Three General Conclusions Retracted

Reviewed2026-10-13. This is a scoped integrity correction, NOT a positive
quantum speedup, a comprehensive audit of61 investigations, or a rejection
of the underlying literature. The original records and numerical checks are
preserved. Three broad negatives are removed from active search guidance:

- `NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER`
- `NEG-QUANTUM-SIMULATION-TENSOR-NETWORK-HORIZON`
- `NEG-QUANTUM-WALKS-SPATIAL-TOPOLOGY-BARRIER`

Their full original records live in
`registry/quarantined_campaign_negatives.json`. Ordinary registry loading
excludes those IDs; upsert refuses reinstatement; validation catches raw-file
restoration. A reviewed, narrower replacement needs its own claim and evidence.
The remainder of the campaign is UNREVIEWED, not implicitly endorsed.

## Why This Takes Priority

The campaign's latest checks evaluate some finite matrices and assumed
formulas. Its JS walk checker, for example, compares a hardcoded localization
number and assigns the asserted1D speedup ratio to1. These checks do not prove
infinite-volume localization, all-graph complexity bounds or impossibility of
other algorithms. Setting `speedup_claim_allowed=False` prevents a positive
overclaim but does not make a negative overclaim correct. Incorrect negatives
can suppress exactly the high-upside directions the project should investigate.

## Annealing And Stoquasticity

The general implication "no sign problem => polynomial PIMC/QMC simulation"
is false. [Hastings and Freedman](https://arxiv.org/abs/1302.5733) construct
no-sign-problem systems where QMC equilibration fails despite a polynomial
quantum spectral gap. This refutes that particular simulation argument; it
does not prove hardness against every classical algorithm.

[Bravyi and Terhal](https://arxiv.org/abs/0806.1746) give restricted efficient
simulation results and establish MA-completeness for stoquastic6SAT. They do
not establish the campaign's general BPP classification for finding arbitrary
stoquastic frustration-free ground states. Precise promise and path conditions
matter; MA-completeness alone is not an unconditional BPP separation.

The campaign also turns a sufficient adiabatic error estimate into a necessary
runtime bound. An exact counterfamily is

    epsilon=3^-n, H(s)=diag(-epsilon*(1+s), epsilon*(1+s)),
    P0=diag(1,0), 0<=s<=1.

The minimum gap is2*epsilon and ||Hprime||=epsilon. A misused gap-squared
proxy is1/(4*epsilon), exponentially large. But [H(s),P0]=0 identically and
the ground projector never changes. Starting in|0> gives ZERO leakage for
every positive runtime. This does not invalidate correctly stated adiabatic
upper bounds or model-specific avoided-crossing analyses; it invalidates a
universal necessity inference.

For a transparent positivity-versus-mixing control, consider the reversible
two-state transition matrix with off-diagonal epsilon=2^-n and stationary
weights(1/2,1/2). All weights are positive, but its gap is2*epsilon. At
t=2^(n-3), TV from a point start is(1-2*epsilon)^t/2 >=3/8 by Bernoulli's
inequality. Thus THIS update rule mixes exponentially slowly. The stationary
distribution is trivially sampled directly; do not promote this example to
hardness of the distribution or all samplers. The published QMC examples
provide the nontrivial physical counterpoint.

## Simulation And Precision

An upper bound ||U-S_r||<=C/r licenses a sufficient r for a requested error;
it cannot be inverted into a universal necessary r. An exact noncommuting
countercontrol takes one cell A=3Z, B=4X, runtime t=2*pi:

    A^2=9I, B^2=16I, (A+B)^2=25I,
    exp(-itA)=exp(-itB)=exp(-it(A+B))=I.

One Trotter step has error0 despite ||[A,B]||=24. For n independent cells,
the commutator norm is24n and the first-order upper proxy is48*pi^2*n, yet
one complete step still has error0. This special periodic family refutes the
claimed universal inference, NOT generic simulation hardness or typical-time
gate costs.

Likewise, a small target fidelity does not imply white noise. Applying Z to
|+> gives|->: target fidelity0, output purity1, and squared Hilbert-Schmidt
distance1/2 from I/2. This is a coherent unitary error, not a claim that all
stochastic noise is harmless. A physical noise conclusion needs an explicit
channel and task metric.

The area-law discussion also omits approximation and algorithmic conditions.
MPS approximation for gapped1D systems is valuable, but does not by itself
prove constant bond dimension at machine precision, convergence of practical
DMRG, or dequantization of arbitrary long-time simulation. See the precise
[Hastings area-law statement](https://arxiv.org/abs/0705.2024).

## Walks And Input Models

For glued-tree depth n, explicit vertex count is N=2^(n+2)-2. An O(N)
adjacency-list BFS remains exponential in n. It is not a polynomial-depth
classical solution in the compact neighbor-oracle model. A dense adjacency
matrix also has a different scan cost from an adjacency list. A valid
comparison must charge representation construction/access on both sides.

The dimension4 threshold refers to a PARTICULAR continuous-time lattice
search Hamiltonian, not every spatial quantum search algorithm. The
[Dirac/coin variant](https://arxiv.org/abs/quant-ph/0405120) gives improved
dimension dependence. This is a known algorithm, not our discovery or an
argument for superpolynomial advantage.

A finite41-site disordered-chain calculation at one time supports only that
calculation. It does not prove all-time/infinite-volume localization or extend
to arbitrary graph dimensions, disorder laws and correlations. Localization
results require their actual hypotheses. A constant diagonal shift alone
changes only a global phase, illustrating why "nonzero potential" is not a
sufficient disorder premise.

Fast classical mixing on an expander also does not erase a quadratic target-
search advantage: a target fraction1/N still takes orderN random samples,
versus a square-root quantum query scale in the appropriate model. Both
being polynomial is not a proof that their complexities match.

## Evidence And Next Work

The producer `theorems/campaign_negative_claim_audit.py --write` checks exact
matrix identities, preserves original-record hashes, and emits14 structural
countercontrols. These are calibration counterexamples, never toy algorithm
candidates. Tests cover the counterexamples and deny reintroduction of the
quarantined IDs into search guidance.

Next, audit the remaining campaign claims individually: identify quantifiers,
input size, access model, approximation norm, source theorem and its actual
hypotheses. Distinguish conditional upper bounds, particular-algorithm
limitations, heuristic evidence, and genuine impossibility theorems. Do not
blanket-quarantine unreviewed work or count numerical PASS outputs as new
mathematical discoveries. Resume constructive receiver research with these
false general barriers removed.
