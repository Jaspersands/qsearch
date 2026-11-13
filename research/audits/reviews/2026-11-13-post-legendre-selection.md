# Post-Legendre independent selection

**Recommendation: none of the three mechanisms below merits a new paid batch.**
This is a selection outcome, not a claim that these problems have no quantum
algorithm. Each has substantial external value, but the proposed operation
either reaches an already audited endpoint or retains a concrete exponential
cost. No nearby Legendre/Hahn, Gram, purity, community, or arithmetic variant
is selected to keep work moving. The Legendre scalar review is unchanged.

Read current STATE, TRAPS and GOAL. Ran both `been-tried` and `baselines`
with `/opt/anaconda3/bin/python tools/corpus/cli.py` on these exact queries:

1. `nonmetabelian nilpotent class four HSP Heisenberg Fourier central character Bell Clifford instrument Rees`
2. `lattice isomorphism coherent discrete Gaussian cooling hidden orthogonal symmetry`
3. `quantum Metropolis Gibbs sampler interacting fermion Hubbard local update spectral gap`

These are discovery leads, not proof labels. The HSP search returned several
QUARANTINED overbroad exclusions; none is used as an impossibility theorem.
The baseline catalog found no HSP keyword match, LLL/Babai for the lattice
query, and stochastic-localization/source-shaping/Gibbs comparators for the
thermal query. A missing catalog match is not absence of a classical method.
Only the relevant topic sections listed below were subsequently read.

## A. Non-metabelian class-four HSP via matrix-phase cancellation

**Native task.** An explicit F_p Lie algebra of fixed class four, p>4, with
BCH group operations and a standard coherent coset-function oracle hiding
an arbitrary subgroup H. Output generators of H with bounded error in
poly(dim L,log p) gates and oracle calls. This is an important algebraic
oracle problem; it is not yet a supplied classical-input cryptanalytic task.

**Specific candidate operation.** After valid intersection/normalizer
reduction, H is transverse to N=G', but N is now class two rather than
abelian. Fourier analysis on N produces Heisenberg/Weyl matrix phases.
Use fixed-degree diagonal-equation cancellation across distinct observed
central labels and Bell/Clifford instruments to turn these into scalar
polynomial phases on unknown affine supports. Public controls must use only
the labels and group data, never H, its graph potential, or its support.
If this complete source instrument existed with polynomial success and
clock, the already paid scalar phase learner could provide the output.

**First falsifier.** Merely pairing opposite labels in an r-dimensional
center has match probability p^-r. With M independent labels, the union
bound for any matched pair is at most M^2/p^r. A Bell contraction whose
accepted rank factor hides the same loss is equally insufficient. The
actual obligation would be a pointwise complete-instrument identity and
its unconditioned output law for every nonzero-probability record, not a
formal cancellation of scalar central characters alone.

**Why not select it.** `AFFINE_VS_MIXED_PHASE_AND_NONMETABELIAN_GAP_AUDIT.md`
LF15–17 marks only the old derived-abelian boundary. More decisively,
`REES_WHOLE_PROOF_SCOPE_AUDIT.md` LF30–35 already targets all fixed-class,
growing-prime nilpotent HSP. Its LF74–126 explicitly treats central
conditioning, all label tuples, dilations, retained registers and the
fresh-copy tree, without requiring metabelianity. Thus the proposed
Heisenberg compiler would presently be an alternative proof of an existing
repository endpoint. This does not promote the Rees human-review gates or
assert publication priority. No explicit cost failure in that construction,
better asymptotic regime, or new native application has been identified.

The classical comparator is standard subgroup reconstruction in the SAME
oracle model, including generic collision search and easy subgroup families;
an oracle separation would not itself solve a classical-input application.
A generic class-four source audit would duplicate work rather than change
the scientific decision. Source checks on nil-2 and bounded-prime results
can clarify scope, but do not supply the missing external endpoint.

## B. Lattice isomorphism by coherent Gaussian canonicalization

**Native task.** Explicit positive-definite integer Gram matrices A,B of
rank d and B-bit entries, promised integrally isometric. Output an integer
unimodular T with T^T A T=B. The intended quantum target is poly(d,B), with
verification and output-coordinate length charged. No reduced basis,
short-vector list, Gaussian sampler below smoothing, or isometry oracle is
supplied. This would have independent value for lattice symmetry and
cryptographic structure problems; no reverse reduction to code equivalence
is assumed.

**Candidate operation.** Prepare basis-independent discrete-Gaussian lattice
states, cool them to a scale resolving lattice geometry, and use coherent
Gram fingerprints of sampled tuples to align the two lattices. The useful
operation must construct new output positions or transport amplitudes;
simply filtering a broad Gaussian is not sufficient. Recovering T from the
fingerprints is another explicit obligation, not free tomography.

**Cheapest decisive test already rejects the proposed cooling step.** For
Z^d let Z_d(s)=sum_z exp(-pi||z||^2/s^2) and theta(s)=Z_1(s).
The norm-one diagonal filter from
width 2s to s succeeds with probability Z_d(s)/Z_d(2s). Poisson summation
gives Z_d(s)=s^d theta(1/s)^d, hence for s>=2 this ratio is at most
(0.501)^d. One can check the constant from
theta(1/s)<=1+2exp(-pi s^2)/(1-exp(-3pi s^2)) and theta(1/(2s))>=1.
Generic amplitude amplification still costs exponentially in d. This is
already true on the classically trivial lattice Z^d, so it is a falsifier
of that filter, not evidence for lattice-isomorphism hardness.

The corpus led to `NATIVE_RLWE_GAUSSIAN_COOLING_AUDIT.md` LF161–197:
normalizer-ratio rejection, approximate filtering, and the cost of recursive
reflections were already isolated there. Changing the final task to lattice
isomorphism does not create the missing transport operation. Classical
competitors to audit are exact lattice-isometry algorithms, short-vector
and Voronoi methods, and reduction-assisted canonicalization. LLL/Babai
alone is not an isomorphism algorithm, despite the catalog match. No current
worst-case advantage or efficient small-width source is admitted.

## C. Interacting thermal sampling through coherent Metropolis updates

**Native task.** An explicit polynomial list of rational two-local spin
terms (or explicitly encoded fermionic hopping/density interactions), a
numerical inverse temperature beta<=poly(d), and epsilon. Output a full
computational/Fock-basis sample from the Gibbs state within TV epsilon.
Hamiltonian simulation, energy resolution, proposal preparation and inverses
must all be paid. A poly(d,B,beta,1/epsilon) all-input sampler would be a
major statistical-mechanics algorithm; a sign problem is not a hardness proof.

**Candidate operation.** Resolve energies coherently, implement reversible
local Metropolis updates, and use a quantum walk/reflection to accelerate
thermalization. A genuinely new version would need a specified nonlocal
proposal or a state-specific preparation argument that bypasses the actual
slow modes, rather than replacing a spectral gap by its square root.

**Cheap legal falsifier for a universal local-gap certificate.** The
commuting subfamily H=-(sum_i Z_i)^2/(2d), even d and beta=2, has weights
exp(M^2/d), M=sum_i Z_i. Its partition function is at least 2exp(d), so
the total probability of the single-flip boundary M=-2 is at most
(1/2)exp(4/d)*(2/e)^d. The two magnetization halves each have constant
stationary mass. Thus any bounded-rate, single-spin reversible proposal
has exponentially small conductance and gap. Square-root phase-gap
amplification remains exponential. The SAME Gibbs output is classically
easy here: sample one of d+1 magnetizations with binomial weights, then a
uniform subset of that size.

This does not rule out a different proposal, a suitable symmetric-start
protocol, or a noncommuting annealing path. It does reject the stated
uniform local-gap rationale. `GIBBS_ORBIT_PARENT.md` LF138–190 already
shows an exact quantum-parent/classical-heat-bath spectral correspondence
for its own code-sector model; that result is not generalized to arbitrary
Hubbard systems here. Free-fermion algorithms, tensor-network methods,
classical cluster updates and stochastic-localization results must be
compared under their actual parameter assumptions. No new nonlocal update
with a full sampling guarantee emerged in this pass.

## Source follow-up and decision-changing evidence

No new primary theorem was imported from an abstract or metadata. If a
specific new operation is found, parent should inspect the relevant actual
primaries before spending: for A, nil-2 arXiv0707.1260 and bounded-prime
arXiv2304.08376 against the existing Rees contract; for B, Plesken–Souvignier,
*Computing isometries of lattices*, and Gentry–Peikert–Vaikuntanathan,
*Trapdoors for Hard Lattices and New Cryptographic Constructions*; for C,
Temme et al., *Quantum Metropolis sampling*, the quantum simulated-annealing
gap theorem, and the current stochastic-localization paper cited by the
corpus (arXiv2609.40250). Their exact present scopes remain to be read; no
blanket classical match or absence-of-prior-art conclusion follows here.

A would reopen only with a demonstrated failure/cost improvement in the
existing receiver or a new native application. B requires an actual
small-width transport and a costed isometry readout. C requires an explicit
proposal/preparation operation that survives its legal commuting subfamily.
Without one of those, there is no defensible next proof dispatch among
these three. DQI/inverse-trace full-list operations and Gaudin gap wishes
are also rejected as already extensively tried, per their current topic
scope; neither is renamed as a fourth candidate. Preserve the remaining
paid budget instead of commissioning another generic barrier review.
