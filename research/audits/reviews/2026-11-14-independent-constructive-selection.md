# Independent constructive selection after the BCS match

Scope: local corpus and topic-note screen on 2026-11-14. No network, paid
call, experiment, or shared-status edit. STATE now records the BCS ground
Born sampler as classically matched under its supplied final sector gap.
This note does not reopen that gap or the completed ternary decision proof.

**Disposition: no new proof batch is justified yet.** The most concrete
remaining source-screen candidate is full spin-resolved *factorized*
scattering. Its quantum circuit is explicit, but its prior-art/classical
status must be checked before calling it a new opportunity. The other two
independent domains below fail this selection pass for precise reasons.

## 1. Product-spin rational-R scattering: source screen only

**Native target.** N spin-1/2 particles in the repulsive one-dimensional
delta gas; explicit distinct rational rapidities, positive rational
coupling, and an initial spin bitstring in momentum order. Output the
asymptotic outgoing spin bitstring in a specified momentum order, within
TV epsilon. All input bits and N are charged. Take an extensive number
of each spin, rather than a fixed number of spin excitations.
There are TWO internal colors, not N distinct ball labels. The proposed
endpoint is the complete reversal of initially decreasing rapidities:
every pair crosses once, not an arbitrary selectable partial collision
schedule or a general circuit of independently parameterized exchanges.

**Concrete operation.** Factorized two-body scattering suggests a reversal
network with at most N(N-1)/2 two-spin rational partial-SWAP gates. For the
algebraic circuit, the unitary

    R(u) = (u I + i c SWAP)/(u + i c)

is completely explicit for real rational u and c>0. The checked/braid
version exchanges I and SWAP; which version and wire ordering implement
the physical scattering map must be fixed from the actual source.
This is a material convention, not an asserted identification here.

For either convention, the *given circuit* is executable in
poly(N,B,log(1/epsilon)) gates: sort the rational rapidities, retain their
labels through crossings, compute each rational two-qubit matrix, and
compile each gate to error O(epsilon/N^2). No inverse rapidity-gap clock
is needed merely to compute these bounded rational unitaries. Product
spin preparation and final spin measurement are native. There is no
Bethe-eigenvector preparation or many-body spectral-gap oracle.

This differs from the rejected inelastic scalar-field proposal in
DCP_SIMON_OCTOBER_REVISION_AUDIT.md:250-256: dressing and interacting-vacuum
preparation are not the proposed operation. It also differs from asking
for an excited Gaudin eigenstate or a new Bethe transform. Nevertheless,
an explicit known scattering circuit is not by itself a new algorithm.

**Scientific output and possible gain.** Correlated spin transport in a
finite integrable cold-atom scattering experiment, including the complete
spin-counting law. A polynomial quantum versus superpolynomial classical
full-sampling separation is the desired target, not established here.
Finite-width wave packets and a finite experimental duration would require
an additional quantitative reduction to the asymptotic S-matrix law;
they are not silently included in the circuit clock above.

**Classical attacks.** Exact state propagation stays inside the conserved
magnetization sector, of dimension binomial(N,w); fixed w is already
polynomial. MPS contraction, coordinate Bethe-ansatz formulas, determinant
identities for special boundaries, and stochastic six-vertex/interchange
representations are the relevant competitors. None was verified to give
the arbitrary extensive-spin full law in this pass. Conversely, failure
of a naive stochastic replacement of each gate would prove no hardness.

**Cheapest next discriminator.** Read the actual integrable/velocity-
constrained model in Aaronson--Bouland--Kuperberg--Mehraban, *The
Computational Complexity of Ball Permutations*, before any paid proof.
Then check current integrable-circuit sampling literature for this exact
spin-1/2, fixed-rapidity, reversal-network law. If already covered by a
polynomial classical sampler, or if the quantum endpoint is already the
same published algorithm with no new application reduction, stop.
If not, the narrow question is whether its full Born law admits a positive
polynomial sampler despite interfering spin-exchange histories. A single
mixed-spin exact comparison can reject the simplest Markov replacement,
but cannot establish a speedup or justify broad simulation infrastructure.

**Source requests.** Actual Yang spinful delta-gas S-matrix/factorization;
the ball-permutation paper; current classical full-output integrable
circuit results. These are requests, not theorem imports from abstracts.
The parent has now retained the ball-permutation PDF/text under
audits/sources/ballistic_scattering_selection/; its source audit remains
separate from this selection note.

**Corpus result.** `been-tried` for “Yang Baxter rational R matrix spinful
delta gas scattering full spin Born sampling rapidities” found only
unrelated compact-group/HSP and Slater hits. Targeted Markdown search found
only an old anyonic braid relation. `baselines` returned tensor-network
simulation with no exact keyword match. These weak catalog results do not
establish novelty or absence of a classical algorithm.

## 2. Growing-genus curve zeta reconstruction: reject as rediscovery

**Native target.** An explicit smooth hyperelliptic curve over F_q, with
growing genus g, and its full zeta numerator as classical output. The
natural constructive operation is quantum Jacobian order computation
over a controlled collection of extensions, followed by exact Weil-bound
reconstruction. Its intended clock is polynomial in g and log q and the
explicit equation length; no point-count oracle is supplied.

This has clear arithmetic/cryptographic value, but it is already the
published primitive identified in JACOBI_SURFACE_RECONSTRUCTION.md:24-37
(Kedlaya, math/0411623). The repo explicitly rejected the Fermat-curve
instance as rediscovery and used the primitive in later surface work.
It does not meet the request for a new operation beyond existing abelian
order-finding. Classical point-counting and finite-field cohomology are
the real comparators; this pass does not assert a uniform classical match
at simultaneously growing characteristic and genus.

`been-tried` returned the existing surface/curve material; `baselines`
misranked generic arithmetic entries. The exact topic admission above is
stronger evidence than that search score. No new source or proof batch.
The separate normalized Kloosterman idea is also already screened in
KLOOSTERMAN_SPECTRAL_ADMISSION.md: whole-curve zeta loses the marked
character sector and its genus grows with p. Do not relabel it rank two.

## 3. Diagram-native Khovanov readout: reject this receiver

**Native target/mechanism.** Given a knot diagram with n crossings, encode
its enhanced-resolution chain complex, implement its sparse differential
Dirac operator, and read zero modes to detect the unknot or a homological
invariant. An attractive proposed clock is polynomial in n and requested
accuracy, with no pre-supplied cycle or harmonic-state oracle. Quantum
phase estimation alone does not pay the relevant output normalization.

**Exact cheap falsifier of the uniform-trace version.** Put n independent
Reidemeister-I kinks on an unknot. Ignoring gradings, the enhanced chain
space has dimension 2*3^n, while its homology has dimension 2. One can
verify this locally without a spectral assumption: for
A=Q[x]/(x^2), the kink complex is A tensor A --multiplication--> A.
Multiplication has the A-linear section a -> a tensor 1 (using the first
factor action), and its kernel is free of rank one over A, generated by
x tensor 1 - 1 tensor x. Thus this complex splits as a shifted A plus a
contractible free pair. Tensoring n local complexes over A gives the
stated dimension and homology. Orientation changes grading, not this count.

The Laplacian kernel therefore has normalized trace 3^(-n), even if its
nonzero spectral gap were perfect. Purify the uniform chain state and
filter its kernel: the success probability is 3^(-n), and ordinary
amplitude amplification of this receiver costs order 3^(n/2). This is
not a lower bound for arbitrary quantum topology algorithms. Classical
Reidemeister-I simplification removes this family directly.

A uniform constructive chain contraction or an input-dependent source
with a proved useful harmonic overlap would change that conclusion; none
was derived here. Naming “Lee deformation” or “Morse preconditioning”
without its complete native construction would just replace the missing
operation by advice. General classical diagram simplification, normal-
surface recognition, and width-sensitive chain contraction must also be
checked against any more specific surviving target.

Corpus `been-tried` returned unrelated code-homology and the already
classically matched matroid top-spectrum note, not this exact target;
`baselines` had no keyword match. Primary sources for a later genuinely
constructive proposal would be Khovanov/Bar-Natan's chain definitions and
unknot-detection literature. No such proposal survives the present screen.

## Next action

Do not spend a paid retry on any of these as presently formulated. The
only short discriminator worth doing first is the actual ball-permutation
source/current-classical screen for the exact extensive-spin scattering
law. A positive result would specify an externally motivated endpoint
whose quantum source is already explicit; a match or prior identical
algorithm would end this candidate. No novelty, hardness, speedup, or new
end-to-end quantum theorem is admitted by this selection note.
