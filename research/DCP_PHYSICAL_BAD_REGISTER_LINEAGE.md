# DCP Bad Registers: Physical Merge And Lineage Audit

Local density derivation, primary-theorem source checked, external review
pending. No general DCP, DHSP or lattice no-go is asserted. This addresses
the real bad-register promise missing from the existing ideal sample sieve.
Additional state-preparation and physical gate errors are not certified here.

## The Source Is Not An Ideal Phase Evaluator

This complements the existing tagged dcp_bad_register_audit, dcp_contamination_witness, dcp_clifford_contamination
and dcp_physical_phase_noise rather than claiming those capabilities were
absent. The new objects are normalized CNOT density branches and lineage
budgets under a legal real-source subclass, with independence/clean-flag
countercontrols and explicit reduction-parameter costs.

The repository's Regev contract (cs/0304005, cached quantum_average.tex)
permits a register to be an arbitrary basis state |b,x> instead of a coset,
with bad probability at most1/(log N)^f. Both good and bad position-register
Fourier readouts yield UNIFORM measured labels. A bad qubit becomes |b>,
not a smaller perfect phase state. The simulator's hidden slope is used
ONLY to validate literal quantum matrices; no evaluator, chosen label or
bad-status flag is delivered to an algorithm. An actual lattice-to-coset
generator and a full bad-register receiver remain unimplemented.

For a measured label k, compact audit density parameters are

    rho_k = [[a, v*exp(-2*pi*i*k*s/N)/2],
             [v*exp(2*pi*i*k*s/N)/2, 1-a]].

With bad rate p and bad-basis zero probability b, a=(1-p)/2+p*b and v=1-p.
These parameters are PRIVATE audit information, not extra source access.
They must satisfy v^2 <= 4*a*(1-a). Original receipt IDs are disjoint; an
output cannot be paired with an overlapping ancestor as if it were a copy.
Disjoint IDs are not sufficient: the merge API additionally requires an
explicit conditional product-source assumption. Independence is conditioned
on the COMMON unknown secret, not a separate secret twirl for each register.

## Exact CNOT Branches

For control density(a,v), target density(b,w), and target readout0:

    probability = a*b+(1-a)*(1-b),
    output_population = a*b/probability,
    output_visibility = v*w/(2*probability), label = k+l.

For readout1 replace b by1-b in the population/probability formulas,
keep the visibility formula, and use label k-l. An impossible branch has
NO normalized output and cannot be selected for free. Literal4x4 CNOT
and projected target blocks independently verify all six original cases.

Good+good produces the usual two half-probability phase branches. Any basis
bad input destroys output coherence in this two-state combiner. Bad0+bad0
has a deterministic branch0, disproving a universal branch-probability1/2
assumption. Biased allowed contamination also changes branch probabilities.
None of this rules out a different collective measurement or fault handling.

A correlated bad-status countercontrol has the SAME balanced marginal densities
and distinct receipt IDs, but chooses all good with probability1-p and bad00
or bad11 with probability p/2 each. Its branch1 has probability(1-p)/2
and is perfectly coherent, unlike the marginal-product prediction. This
demonstrates why IDs and marginal rates cannot certify the product law.
It is a scope countercontrol, not a claim about every published source.

Pure bad cases in the literal controls are components of a mixture, not
claims that an always-bad distribution satisfies the small-bad-rate promise.

## Labels Can Improve While Phase Information Disappears

A BALANCED equal bad0/bad1 mixture is a legal subclass of the full theorem
promise. It gives a=1/2 and v=1-p. Under disjoint CNOT merge trees, both
branches have probability1/2 and visibility MULTIPLIES, independent of labels:

    v_out = product_i(1-p_i).

For common p and a balanced depth-d tree, L=2^d original leaves give
v_out=(1-p)^L. This is an exact density statement, not a simulation fit,
and not a claim that every possible sieve requires a balanced depth-d tree.
The actual original leaf count is the relevant variable.

The profiles use the LEGAL MAXIMUM-rate balanced subclass. They are not
visibility upper bounds for every smaller bad rate; a perfect source still
has visibility1. This adversarial allowed subclass tests full-family claims.

At a parity target label N/2, the even/odd states have trace distance v,
so optimal SINGLE-copy success is at most(1+v)/2. When v<=1/2, Pinsker and
D(rho_even||rho_odd)=v*log((1+v)/(1-v))<=4*v^2 imply that success3/4
needs at least1/(8*v^2) INDEPENDENT target copies. Correlated targets or
reused ancestors cannot inherit that tensor-product copy bound. Parity is
only one bit, not full hidden-slope recovery.

Large rational powers are not expanded past a whole-work cap. Reciprocal
Bernoulli gives (1-p)^ceil(1/p)<=1/2 and a certified upper bound
2^-floor(L/ceil(1/p)), conservatively capped at192 bits. A cap returns an
unknown exact power, not a fake zero visibility or a failed source claim.

The illustrative depthceil(sqrt(log2 N)) profiles are tests of one familiar
merger shape, NOT lower bounds on all Kuperberg/Regev implementations.
For any FIXED f, exponential-in-sqrt(log N) lineage width eventually
overwhelms polynomially small bad probability. A label-only sieve score
that ignores this visibility cannot certify transfer to the noisy source.

## Bridge To Existing Physical-Z Packet Audits

For an equatorial GOOD phase qubit, independent balanced bad-basis rate p
has exactly the same density as a physical Z flip at rate p/2:

    (1-p)*rho_good + p*I/2 = (1-p/2)*rho_good + (p/2)*Z*rho_good*Z.

The bridge uses the existing IndependentPhysicalZ packet implementation and
checks all four logical Fourier masks on two actual compiled public charts.
Their contrast factors are (1-p)^physical_support. The biased bad-basis
countercontrol has a different diagonal and does NOT match this channel.
This reuses existing noise tools on an admissible balanced independent
subclass, NOT the full arbitrary bad-register theorem promise. Existing
source/chart/secret-independence assumptions still need checking for every
packet result. Unknown coset phases do not become classically known through
this density identity; no known-phase simulator is transferred to them.

## Raising f Is Not A Free Repair Of The Reduction

The cached primary construction uses M=2^(4n), log2 N=n*(4n+1),
prime p>n^(2+2f), and unique-SVP approximation order n^(1/2+2f).
For the illustrative merger width, the audit computes the minimum integer f
satisfying (log2 N)^f>=2L, which SUFFICIENTLY retains visibility at least1/2
by Bernoulli. It records the resulting approximation exponent and prime
growth. This sufficient f need not be necessary or optimal.

Substituting an f that grows with dimension is NOT the paper's fixed-f
polynomial-time theorem. Its prime/guessing cost can cease to be polynomial,
and the required uniqueness can become weaker than the usual LLL baseline.
Constants and the full variable-f reduction are not silently assumed uniform.
Different source adapters, robust sieves and polynomial-copy collective
decoders remain open and should be searched, not excluded by this audit.

## A Single-Register Clean Flag Is Not A Free Repair

For any nonzero measured label, averaging the good phase qubit over a uniform
unknown cyclic secret gives I/2, identical to the balanced bad ensemble.
Every fixed one-copy effect therefore has the SAME mean good/bad acceptance.
An effect rejecting BOTH bad basis states exactly must be zero by positivity.
The complete32-secret control checks Z, X, Y and identity effects. Label0
has a known phase but carries no hidden-secret information. Collective
instruments, prior information from other registers and partial-secret
conditioning are not excluded. No clean-register flag is granted.

## Next Research Target

Preserve actual quantum-state input rather than transferring known-phase
classical simulation to opaque coset states. Develop a collective decoder
or explicitly costed error-handling mechanism whose useful outputs survive
the source's bad-register law. Also implement the actual lattice producer:
a formal theorem contract is not a source preparation experiment.

    python theorems/dcp_physical_bad_register_lineage.py --write
    node research/certificates/dcp_physical_bad_register_lineage_crosscheck.js
    python -m pytest -q tests/test_dcp_physical_bad_register_lineage.py
