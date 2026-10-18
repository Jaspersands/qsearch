# Campaign Negative Claims: Five General Conclusions Retracted

Reviewed2026-10-13; extended2026-10-16. This is a scoped integrity correction, NOT a positive
quantum speedup, a comprehensive audit of61 investigations, or a rejection
of the underlying literature. The original records and numerical checks are
preserved. Five broad negatives are removed from active search guidance:

- `NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER`
- `NEG-QUANTUM-SIMULATION-TENSOR-NETWORK-HORIZON`
- `NEG-QUANTUM-WALKS-SPATIAL-TOPOLOGY-BARRIER`
- `NEG-EASTIN-KNILL-NON-CLIFFORD-FAULT-TOLERANT-BARRIER`
- `NEG-QUANTUM-ERGODICITY-ETH-LOCAL-OBSERVABLE-BARRIER`

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

## Fixed-Code Transversal Limits Are Not A Distillation Mandate

The [Eastin-Knill theorem](https://arxiv.org/abs/0811.4262) restricts universal
transversal encoded gates for a fixed error-detecting code (modulo physically
irrelevant global phases). It does not require magic state distillation in
every fault-tolerant implementation. [Paetznick-Reichardt](https://arxiv.org/abs/1304.3709)
give a universal construction using transversal operations AND fault-tolerant
error correction without state distillation. This does not contradict the
fixed-code transversal-only theorem or eliminate the cost of error correction.
The campaign record's narrowly stated transversal-only obstruction can be
retained in a properly scoped replacement; its architectural mandate cannot.

Its Steane example also checks the WRONG stabilizer type. Transversal diagonal
T commutes with every Z stabilizer, so their expectations cannot change. In
the eight-word simplex support of logical zero, T^7 assigns phase+1 to zero
and-1 to each nonzero weight-four word. A nonzero simplex X stabilizer pairs
zero with its weight-four partner, giving expectation(6-2)/8=1/2 instead of1.
Z expectations remain1. The conclusion that T^7 fails on THIS code is valid;
the claimed Z-stabilizer proof was not.

The 15-to-1 small-error expansion is not an exact threshold equation. For the
ideal independent phase-fault/check model, enumerate all2^15 error masks,
accept those with XOR of their nonzero four-bit positions zero, and count
odd accepted weight as logical error. The exact map, with v=1-2p, is

    p_out=(1+15v^8-15v^7-v^15)/(2(1+15v^8)).

At p=3/20, the cubic approximation35p^3=189/1600<p predicts purification,
but the exact output624658088490057/3729440300000000>p does NOT purify.
This directly refutes treating1/sqrt(35) as the exact threshold. The
[Bravyi-Kitaev protocol](https://arxiv.org/abs/quant-ph/0403025) is context;
the enumerator and exact counterexample are reconstructed locally. No
hardware threshold or universal lower bound is inferred.

Finally polylogarithmic overhead is not exponential overhead. For search
size N=2^(2n), a stipulated per-query overhead n^3 changes sqrt(N) to
n^3*sqrt(N), leaving classical/quantum work ratio2^n/n^3 unbounded. This
conditional accounting example does not certify a hardware crossover or
assume every architecture has that overhead. It refutes the universal
asymptotic-erasure inference, not the importance of fault-tolerant costs.

## ETH Premises And Measurement Access Must Be Named

Nonintegrability does not establish strong ETH for EVERY eigenstate.
[Shiraishi-Mori](https://arxiv.org/abs/1702.08227) construct local Hamiltonians
with no local conserved quantities but embedded nonthermal eigenstates.
This does not refute conditional ETH predictions for models/states satisfying
their premises. Six-qubit Ising comparisons are not proofs of a universal
thermodynamic or computational bound.

A small mean difference alone does not imply an inverse-square sample lower
bound. Bernoulli(0) versus Bernoulli(delta), delta=2^-n, can be distinguished
by asking whether ANY positive event appears in T=2^n independent samples.
Equal-prior success is1-(1-delta)^T/2>=1-1/(2e), despite T being only1/delta,
not1/delta^2. The missing variance-away-from-zero/likelihood premise matters.
Hoeffding gives a sufficient sample bound, not a universal necessary bound.
This counterexample does not itself make thermal eigenstate inference easy.

Local indistinguishability also does not block arbitrary joint records or
controlled-evolution phase estimation. GHZ+ and GHZ- have identical reduced
density matrices on EVERY proper subsystem, but H on each wire followed by
all Z measurements and one classical parity distinguishes them in one shot.
They are eigenstates of the efficiently measurable Pauli product X^n with
eigenvalues+1,-1. This is a counterexample to the access implication, NOT a
counterexample to ETH in a local chaotic Hamiltonian and not a new algorithm.
The general ETH-to-QPE impossibility inference in the active record is invalid.

The normalized full identity is the infinite-temperature ensemble, not an
arbitrary energy-window microcanonical state. Computing its Pauli trace does
not solve general thermal expectation estimation. A defensible local-measurement
lower bound needs an explicit state family, promises on its density operators,
permitted sequential/collective channels, and a controlled relative-entropy or
trace-distance calculation. None of these broad exclusions are reinstated.

## Evidence And Next Work

The producer `theorems/campaign_negative_claim_audit.py --write` checks exact
matrix identities, preserves original-record hashes, and emits25 structural
countercontrols. These are calibration counterexamples, never toy algorithm
candidates. Tests cover the counterexamples and deny reintroduction of the
quarantined IDs into search guidance.

For the two2026-10-16 extensions, run
`python theorems/campaign_negative_claim_audit.py --quarantine-reviewed --write`.
The writer preserves complete originals in the existing quarantine, rejects
changed originals, checks for concurrent changes and excludes the IDs from
active loading before removing their raw active copies. Re-running is safe.
Ordinary registry upserts continue to reject quarantined IDs. This is a
specific mathematical review, not blanket removal of unreviewed negatives.

Next, audit the remaining campaign claims individually: identify quantifiers,
input size, access model, approximation norm, source theorem and its actual
hypotheses. Distinguish conditional upper bounds, particular-algorithm
limitations, heuristic evidence, and genuine impossibility theorems. Do not
blanket-quarantine unreviewed work or count numerical PASS outputs as new
mathematical discoveries. Resume constructive receiver research with these
false general barriers removed.
