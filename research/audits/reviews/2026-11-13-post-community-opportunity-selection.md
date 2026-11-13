# Post-community opportunity comparison — 2026-11-13

**Disposition: no candidate extension is admitted.** The named next lead is a
single PRIMARY-SOURCE gate on loss-conditioned bosonic transport (section 2).
Three externally
valuable native endpoints are compared below, with specific compiler operations
rather than a generic simulation/QPE proposal. Each tested operation fails a
cheap exact check. This is a recommendation to pause candidate EXTENSION pending
a materially different operation, not to mark the research goal blocked, claim
hardness, or create more barrier infrastructure.

Current STATE/TRAPS and the prior post-tower comparison were read. The community
source repair and its new classical challenger are not treated as a new
Shor-scale mechanism. Tower arithmetic, compact wave sampling, and the prior
near-join Euler match remain closed; no nearby variant is reopened.

## 1. Rigid graph isomorphism: global permutation-coherence compression

Native input: two explicit rigid N-vertex adjacency matrices. Output: an
isomorphism permutation, or distinguish isomorphic from nonisomorphic pairs
with bounded error. This is an externally significant combinatorial endpoint;
a polynomial native quantum algorithm would be substantially stronger than the
known quartic-scale mechanisms investigated recently.

Proposed operation: efficiently prepare the usual hidden-permutation coset
states, then replace their N! dimensional register by polynomially many small
assignment-density matrices, preserving enough information to decode the
permutation. Uniform permutations, graph relabeling and verifying an output
permutation have polynomial native cost. If a sufficiently informative compressed
receiver existed with inverse-polynomial conditioning and polynomial copies,
the intended total clock would be poly(N,log(1/eta)); this is a hypothesis,
not supplied access to an optimal measurement.

Cheapest exact falsifier for the low-coordinate receiver: for rigid isomorphic
inputs the states have the form
  (|0>|pi>+|1>|pi sigma>)/sqrt(2), pi uniform in S_N.
Encode pi by its N images. Retain the branch qubit and positions I, and trace
the other image registers. The off-diagonal survives only if sigma fixes every
position outside I, since pi is injective. For an N-cycle sigma it vanishes
for EVERY proper I. After averaging pi, both diagonal branches are the same
uniform distribution on injective I-tuples. Thus this receiver's output is
exactly independent of sigma. Randomly choosing/recording I does not fix it.
This excludes the proposed discard-before-readout operation, not collective
measurements preserving global coherence or graph isomorphism algorithms.

Strong classical comparison: Babai's quasipolynomial method, individualization/
refinement and canonical-labeling solvers; bounded-degree and other easy
subfamilies must be separated. The corpus already contains extensive native
code/GI coset work and warns that its broad commutant no-go was quarantined.
No assertion from that quarantined note is used here.

Primary checks needed for a different receiver: Babai, *Graph Isomorphism in
Quasipolynomial Time*; Moore--Russell--Schulman, *The Symmetric Group Defies
Strong Fourier Sampling*; Hallgren--Moore--Rotteler--Russell--Sen, *Limitations
of Quantum Coset States for Graph Isomorphism*. Their exact scope must be read,
not converted into a no-go for all receivers. No new global receiver is
specified here, so this is NOT selected as another coset/phase campaign.

## 2. Loss-conditioned bosonic transport: a many-particle normalization compiler

Native input: an explicit rational complex contraction A on N modes, with
singular values in [1/2,1], and one photon in each input mode. Output: a sample,
to TV error epsilon, from the occupation law of the normalized state
  Gamma(A)|1,...,1> / ||Gamma(A)|1,...,1>||.
Gamma is the bosonic lift of the one-particle linear map. This is a concrete
loss-conditioned optical transport/matching-amplitude problem; it does not
ask for exponentially many amplitudes or supply an unknown state.

Proposed operation: use the explicit one-particle polar decomposition/unitary
dilation to compile the NORMALIZED many-particle map with polynomial overhead
in N, input bits and 1/epsilon. A successful uniform compiler would remove a
real postselection bottleneck. The hoped-for separation is polynomial quantum sampling against the general
exponential permanent-based classical route, under the actual sampling-hardness
assumptions; it is not an established lower bound. It would still need a
same-input classical comparison. Unitary A already reduces to known boson
sampling, so that special
case alone would be a known sampling mechanism, not a new Shor-level algorithm.

Cheapest falsifier: take even N and
  A=diag(1,...,1,1/2,...,1/2)
with N/2 entries of each kind. Its one-particle condition number is 2 and its
operator norm is 1. In the direct passive dilation, all photons survive with
probability (1/4)^(N/2)=2^(-N). Plain conditioning therefore has exponential
cost, and amplitude amplification of that dilation costs order 2^(N/2).
One-particle conditioning does NOT pay the proposed many-particle normalization.
The conditional state in this example is itself an easy basis state: this is
a falsifier of the compiler argument, not hardness of the native problem.

Strong classical attacks: exact permanent-based sequential samplers, low-rank/
small-photon methods and special positive/free cases. The actual cost on the
NORMALIZED contraction law must be compared, not the cost of evaluating a
single generic permanent. The corpus's blanket physical-loss/boson-sampling
negative is not a theorem used here. Required primary checks: Aaronson--Arkhipov,
*The Computational Complexity of Linear Optics*; Clifford--Clifford, *The
Classical Complexity of Boson Sampling*; and, if a proposed reduction becomes
nonnegative matching sampling, Jerrum--Sinclair--Vigoda's nonnegative-permanent
approximation theorem. None is imported as a new algorithm in this screen.

ONE first primary gate: Brod--Oszmaniec, *Classical simulation of linear optics
subject to nonuniform losses* (Quantum 4, 267, 2020). Check the actual theorem's
input/output law: does it cover the normalized ALL-N-photon conditional law
above, or only unconditional loss statistics/few-survivor regimes? This source
is named for fetching, not claimed read. A positive matched theorem disposes
of the lead; a scope mismatch alone does not make it hard or quantum-efficient.
Before any extension, a replacement quantum compiler must construct the
normalized map from A with a particle-number-uniform cost. A supplied normalized
map, one-particle dilation or bounded singular-value ratio fails that test.

## 3. Ground-state observables from local fragment certificates

Native input: a bounded-degree local Hamiltonian with rational bounded local
terms, an explicit product/fragment starting state, and fixed-size fragment
spectra computable from those terms. Desired output: a local ground-state
observable to additive epsilon. The proposed NEW operation would turn those
native fragment data into a certified global preparation path and clock;
ordinary simulation/QPE AFTER an unprovided ground state is not the proposal.

The hoped-for resource would be poly(N,input bits,1/epsilon), enabling a useful
interacting many-body task where classical tensor contraction is costly. No
classical lower bound or uniform quantum clock follows from that hope; even a
positive source theorem would leave the asymptotic advantage UNKNOWN until
strong tensor/positive-measure methods are compared on the same family. In
particular the gap, source overlap and finite cutoff cannot be advice.

Cheapest exact falsifier for a local-gap certificate: on an open chain take
  H=-sum_(j<N) Z_j Z_(j+1) - g*sum_j X_j, with g=1/2.
All terms and every fixed-size fragment have size-independent spectral data.
Set
  Psi=c*sum_(j=1)^N g^(j-1)*(product_(i<j) X_i)*Z_j,
  c=sqrt((1-g^2)/(1-g^(2N))).
Its summands anticommute, so Psi^2=I; it anticommutes with global parity
product X_i. Direct telescoping gives ||[H,Psi]||=2c*g^N<=2g^N. Applying Psi
to a parity ground state produces an orthogonal unit vector with energy at
most E0+2g^N. Thus the global gap is at most 2^(1-N), despite all bounded
fragment information. Local gaps alone cannot certify the proposed clock.
This does NOT preclude a different preparation algorithm or additive-energy
method; this particular free-fermion chain is classically solvable.

Strong classical attacks: exact free-fermion reductions, MPS/DMRG or other
tensor networks on the actual geometry, and positive path-integral/cluster
methods where their hypotheses hold. A new family must escape an actual
matched algorithm, not merely have noncommuting terms. Primary checks for a
materially stronger criterion: Pfeuty, *The One-Dimensional Ising Model with
a Transverse Field*; Schwarz--Temme--Verstraete, *Preparing Projected Entangled
Pair States on a Quantum Computer*; and the precise gap assumptions in any
claimed constructive PEPS/Gibbs-preparation theorem. No global-gap theorem
was inspected/imported here, and none is assumed from a title or abstract.

## Evidence, ranking and what would change the decision

Corpus `been-tried` and `baselines` were run for each concrete screen above.
Preliminary LWE quantum-example and quadratic Gauss-sum proposals returned to
existing noisy-phase/source-access lines and were not promoted as fresh
candidates. No handoff/archive was opened. Only the retained compendium TOC
was used to orient comparison, not as a primary theorem. Listed external
primary papers are CHECK TARGETS; none was fetched through an external service.

Ranked by a specific next operation, bosonic normalization is the least vague,
then a genuinely global permutation receiver, then a native many-body path
certificate. Ranked by currently justified expected return, NONE clears the
extension gate: all three displayed cheap compilers fail, and no replacement
has been specified. A new source/result would change this decision only by
providing that missing constructive operation with native inputs, uniform
normalization/gap/copy bounds, and a verifiable output; merely improving a
known simulation or Fourier subroutine would not.

Recommendation: perform only the named nonuniform-loss PRIMARY gate, then
pause candidate extensions unless it reveals a genuinely different paid
operation. No exhaustive source survey, barrier project, implementation or
nearby parameter variant is selected. Retain the exact failed tests above.
