# Known Phase Tags: Measured-Witness Sieves Have A Classical Simulation

Date: 2026-09-29. LOCAL DERIVATION / REVIEW PENDING.

No novelty, independent proof verification, general quantum simulation, or
lower bound for DHSP is claimed. This is an exact comparator for a specified
decoder family on the project's ACTUAL classically prepared phase sources.
Routine implementation and registry integration are assigned to Gemini.

## 1. Research Decision And Scope

Do not prioritize generic measured-pair extraction, Kuperberg-style qubit
merges, or explicitly listed collimation packets as the missing quantum
decoder for the native/classical-tag source. Under the access and operation
premises below, their full output transcript has a classical sampler with
polynomial overhead. It includes failure, weighting, postselection and retries.
Improved classical merge rules may still be useful classical attacks.

The reason is NOT that the quantum input has a classical description; that
would be far too broad. The simulator uses BOTH its sampleable coefficient
probabilities and computable relative phases, and the restricted locations
where interference occurs. Genuine HSP phase states have unknown phases and
do not satisfy this access contract. General coherent operations on the large
input registers are also outside the result.

The relevant framework is established prior art:
[Van den Nest, Definition 1 and Section 4.2](https://arxiv.org/pdf/0911.1624)
studies states with classically sampleable basis probabilities and computable
amplitudes, including efficiently invertible basis-preserving operations.
Here the explicit latent-sample argument also avoids computing the normalizer
of a measured fiber. It is a local application to this source, not a claim
to have introduced that framework.

## 2. Source Access Must Be The Actual One

Let X be the original classical input and public preparation randomness.
Consider a finite pure source

    |Psi_X>=sum_(c in C) A_X(c)|c>,
    A_X(c)=sqrt(mu_X(c))*exp(i*phi_X(c)).                       (1)

The comparator may use X, but NOT the hidden secret or original noise.
Require an efficient sampler for mu_X and efficient evaluation of relative
amplitudes on an explicitly listed set of basis points, to charged precision.
Additive amplitude access alone does not automatically give efficient
relative accuracy on an arbitrarily rare postselected branch.

The native finite source in NATIVE_RLWE_PHASE_DECODER_TARGET satisfies this:

    mu(c) proportional to exp(-2*pi*||c||^2/sigma^2),
    phi_X(c)=2*pi*<b,c>/q mod 2*pi,
    log |A(u)/A(v)|=-pi*(||u||^2-||v||^2)/sigma^2.              (2)

Coordinates are sampled independently in their actual cutoff intervals.
Log weights avoid underflow; relative phase is public modular arithmetic.
The scalar direct source similarly has known tags t_l=u_l^T*b and phase
2*pi*sum_l t_l*E(c_l)/Q. Its simulator samples the SAME public selectors
and tags. It never substitutes the unknown ideal phase <a,s> for t_l.

If the quantum decoder voluntarily discards b or fresh tags, the classical
baseline may still retain what it computed from the same original input.
This is an algorithm comparison on classical Ring-LWE input, not an assertion
that a solver supplied ONLY unknown quantum states receives extra records.
The source's hidden covariance does not matter here: its actual preparation
uses the public envelope and observed b, not the hidden error shape.

## 3. Weighted Measured-Witness Extraction Without A Fiber Counter

Measure a publicly computable syndrome h(c), obtaining y. Let

    F_y={c:h(c)=y}, p_y=sum_(c in F_y) mu(c).

Given only X,y and its own randomness, a CLASSICAL witness finder returns
distinct u,v in F_y, or declares failure. It must not depend on an unobserved
source assignment. Project the retained register onto span{|u>,|v>}.
On acceptance, compress these two known basis strings into a qubit. The
normalized state is

    [ A(u)|0>+A(v)|1> ] / sqrt(mu(u)+mu(v)),                  (3)

and the conditional acceptance probability is (mu(u)+mu(v))/p_y.
This probability may be hard to compute directly. It is not needed by the
following exact weak simulator:

    draw latent c_star from mu;
    y=h(c_star);
    (u,v)=Finder(X,y,ordinary independent randomness);
    accept exactly when c_star is u or v;
    if accepted, store the known two-component vector (3);
    do NOT reveal c_star to Finder or the simulated protocol.

For fixed y,u,v, summing the latent probability over the two endpoints gives
exactly the quantum acceptance mass. The accepted pure qubit depends on the
pair, not on which latent endpoint passed the test. Store/simulate that
coherent vector; returning the sampled endpoint as the qubit would be wrong.
Every syndrome, finder failure, rejection and success has the correct weight.
There is no conditional fiber sampler, approximate counter or 1/p_y oracle.

The standard measured-pair construction is prior art, not a new algorithm:
[Regev, Section 3](https://arxiv.org/pdf/quant-ph/0406151)
measures a low subset sum, finds a bounded fiber, and compresses two surviving
members. `DCP_MEASURED_FIBER_COLLIMATION.md` discusses a more general witness
interface for UNKNOWN DCP phases. This comparator applies when that interface
is instead used with the known tags in (2).

### Unequal Weights, Failed Projections And Filters

To equalize the amplitudes, let m=min(mu(u),mu(v)) and apply the heralded
diagonal filter with entries sqrt(m/mu(u)), sqrt(m/mu(v)). The TOTAL mass
of balanced success, conditional on y and the chosen pair, is 2*m/p_y,
not 2/|F_y| and not (mu(u)+mu(v))/p_y. In the simulator, after endpoint
acceptance use the latent endpoint to sample that filter's success coin;
then store the equal-magnitude vector with the known relative phase.

If a failed pair projection is followed by another pair attempt on the SAME
register, retain c_star. It already has the correct distribution conditioned
on every failure. The amplitude evaluator must also mask out the rejected
endpoints. Resampling c_star from the original unconditioned mu would be wrong.
Finder sees the rejection transcript, never c_star. A fresh source preparation
instead gets a fresh latent sample and counts as a new preparation.

Known diagonal instruments also admit this treatment. For a refined outcome j
with Kraus multiplier d_j(c), sample j at the latent point using |d_j(c_star)|^2
and multiply each later endpoint amplitude by d_j(c). Require efficient
outcome sampling, multiplier evaluation and relative-precision accounting.
Products of known multipliers and masks retain their full transcript history.
No destructive interference has occurred between different coefficient points.

An efficiently invertible public permutation can update the latent point
and pull endpoint amplitudes back through its inverse. Public diagonal
phases, even nonlinear ones, only update the known relative phases. These
extensions do not include an unmeasured Fourier/Hadamard transform on the
large register, or coherent feedback from a small packet into that register.

## 4. Phase-Qubit Merges Are Explicit Classical Arithmetic

Conditional on the transcript, let two independent retained qubits have
KNOWN normalized vectors u=(u0,u1), v=(v0,v1). Apply CNOT from the first
to the second and measure the second in the computational basis. Outcome t
has unnormalized surviving vector

    w_t=(u0*v_t, u1*v_(1 xor t)),
    Pr[t]=||w_t||^2.                                        (4)

The simulator samples this probability and retains w_t/||w_t||. For
equatorial states with relative phases theta and phi, each t has probability
1/2 and the new relative phase is theta+(-1)^t*phi. Thus sum/difference
label combining, adaptive buckets, family-specific merge rules and final
single-qubit measurements are all simulated, including discarded branches.

For native endpoints, the putative ideal phase label is

    lambda=C_a^T*(v-u) mod q,

but the ACTUAL relative phase is the already known

    theta=2*pi*<b,v-u>/q
         =2*pi*(<s,lambda>+<e,v-u>)/q mod 2*pi.              (5)

The simulator evaluates the first expression. It is never given s or e.
If a merge rule cancels noise and recovers the secret within this family,
the same classical sampler has that recovery probability. This is stronger
than merely showing that an ideal-source approximation budget is inadequate.

More generally, arbitrary known one-qubit operations and a known two-qubit
unitary followed immediately by rank-one measurement of one output also
preserve this simulation. Conditional on each outcome, the remaining qubit
is an explicitly known pure state and stays independent of all other packets.
Induction proves the entire adaptive transcript law. Unrecorded outcomes
can be retained privately by the simulator, not exposed to the controller.
Keeping both outputs coherently and building an unbounded entangled component
is a different operation family.

## 5. Explicit Packet Collimation And Resource Accounting

The same argument handles an explicitly listed packet
sum_(j=1)^K alpha_j |z_j>, with known alpha_j and basis labels z_j.
For two independent packets, measure a public function h(z_i,z_j): sample
latent indices from |alpha_i|^2 and |beta_j|^2 to get the outcome, then retain
the listed matching amplitudes alpha_i*beta_j with their known normalization.
For bounded list sizes one may enumerate the product table. Alternatively,
reuse the algorithm's already-computed matching list and fill its amplitudes.
Subsequent explicitly represented operations on that packet are ordinary
matrix-vector calculations.

[Kuperberg, Algorithm 4.1 and Proposition 4.2](https://arxiv.org/pdf/1112.3333)
explicitly account for classical phase-multiplier tables and their indexing
in collimation. In genuine HSP those multipliers do not reveal the unknown
phase. On the actual known-tag source, endpoint histories or amplitude tables
supply it, so this comparator must be included.

Let T include source preparations, witness finding, adaptive classical work,
and all explicitly generated list entries. With polynomial-size listed
packets and charged relative-amplitude precision, the simulator costs
poly(T,input size,precision), not polynomial in a secretly exponential
Hilbert-space table supplied for free. For qubit-only destructive merging
it stores O(1) complex amplitudes per retained qubit.

Large IMPLICIT fibers alone do not escape Section 3: no enumeration is needed
before a classically selected explicit pair is accepted. Large coherent
interference before that pair is identified can escape. An implicit packet
which is processed without listing its exponentially many entries needs a
separate analysis; simply asserting a polynomial classical table size does
not cover it. This is a polynomial-overhead comparator, not a statement that
every exponential-time sieve has a polynomial-time classical implementation.

## 6. Scope Tests And Attempts To Break The Claim

**Unknown phases.** |+> and |-> have identical computational probabilities,
but opposite deterministic X outcomes. A simulator given only mu cannot
reconstruct both. Actual HSP oracle phases fail the known-phase premise.
Do not attach this result as a universal negative result for DHSP or HSP.

**Leaking the latent draw.** For a uniform four-point source and constant
syndrome, a fixed pair accepts with probability 1/2. A finder illegally
given c_star can always choose a pair containing it and accept with probability
one. The simulator must isolate its private latent state from solver inputs.

**Dropping rejection costs.** Repeating until success must execute the same
attempts, or sample the same fully justified waiting-time law with costs
recorded. Conditioning on a rare successful pair is not free in either model.
Every fixed input X has the same output law in the ideal arithmetic argument,
so averaging over secret/shape distributions does not weaken that guarantee.

**Quantum witness finders.** Section 3 assumes Finder is classical. A quantum
algorithm solving its ordinary classical witness instance may be valuable,
but this proof does not simulate it. Its useful operation and complexity must
be supplied explicitly, rather than credited to the measured source phase.

**General quantum processing.** Arbitrary known-input quantum computation is
not simulated. Examples outside the proof include coherent mixing across a
large fiber, retaining growing entangled packets, and transformations whose
output relative amplitudes are unavailable. Exiting this simulation class
is only an eligibility condition; it does not establish useful recovery.

**Untracked coherent registers.** In (3), u and v specify FULL basis states
of the source's entire coherent component. The accepted packet must not stay
entangled with an omitted register. For example, the Bell state on labels
00,11 is a perfectly valid TWO-entry packet, but its first qubit alone is
I/2, not a pure |+> packet inferred from its diagonal. That replacement has
trace distance 1/2 and wrong X statistics. A local two-dimensional projector
inside a large entangled register is not the full two-witness compression
assumed here. Packet independence or explicit retention of the whole
correlated component is an applicability premise, not a bookkeeping detail.

**Numerics.** The exact statement treats probabilities/amplitudes exactly.
For implementation, charge source-sampler error and each adaptive transition's
certified TV error; conditional kernels with a uniform error budget compose
by the usual sequential coupling bound. Native Gaussian relative weights
should be computed in log form. A claimed accuracy for a normalized rare
branch must be justified, not inferred from small absolute amplitude errors.
Real-device noise and other state-preparation inaccuracies require their own
comparison; this is not a simulator for arbitrary noisy hardware channels.

## 7. Checks Actually Run

Targeted finite mathematical controls, not candidate-circuit search:

- 48 full weighted extraction transcript comparisons on d=2 coefficient
  registers at q=3,5,7, using Gaussian weights, known linear/nonlinear
  phases, different syndrome functions, two-outcome complex diagonal
  instruments, two pair attempts and final non-diagonal readout. Maximum
  transcript TV discrepancy was 2.50e-16. No fiber counter was used in the
  simulator formula; small enumeration was only the reference comparison.
- 480 unequal-weight balancing controls preserved total success weight.
- 60 overlapping second-pair attempts after first-pair rejection checked
  the required support mask; maximum error was 8.33e-17. An unmasked second
  pair gave a TV contribution as large as 0.294521. A retained balancing-
  failure control with original weights (0.9,0.1) had weights (0.8,0),
  rather than resetting to the original law.
- 120 arbitrary complex-qubit CNOT merges and 240 equatorial sum/difference
  branches checked (4), including their outcome probabilities.
- 24 adaptive four/five-qubit destructive-merge protocols with general
  two-qubit unitaries, 528 projected branches and full tensor-state references.
  Maximum unnormalized density error was 2.23e-16; maximum final-probability
  error was 2.23e-16. These test the induction beyond equatorial qubits.
- 60 explicit packet controls with sizes (2,3),(3,5),(7,9), measured label
  sums and arbitrary listed-space readout. Maximum error was 3.34e-16.
- The unknown-phase, illegal latent-to-finder and untracked coherent-register
  controls above were run. The latter's erroneous pure-qubit replacement
  changes the X distribution by TV 1/2.

Floating controls do not replace proof review or establish novelty. No full
test suite, production wiring, live registry runs or commits were performed.

## 8. Gemini Contract And Remaining Research Target

Add a SCOPED comparator for candidates combining these ACTUAL classical-tag
sources with measured-witness extraction and known-qubit/list sieves. Do not
globally reject all sieve candidates or every use of the HSP workbench.

Record source provenance, access to classical tags, envelope/relative-phase
evaluation, witness-finder type, maximum explicitly listed packet size,
operations before extraction, merge instrument, retained entanglement, and
every success/failure cost. Endpoints must specify the whole coherent source
component, and conditional independence between packets must be justified
or their joint amplitudes retained. The applicability checker must fail closed when
any premise is unproved: classify it as OUTSIDE THIS COMPARATOR, not automatically
as a quantum advantage or as a dequantized algorithm.

Keep c_star private in a separate simulator component. Compare whole joint
transcripts, including rejected attempts and final bits, against small exact
quantum references. Include unequal Gaussian weights, repeated attempts on
the same register, known nonlinear phases, general destructive merges, and
the three mandatory premise-breaking controls. Use actual b/tags, never a*s.
Wire negative results only to candidates whose operations satisfy the contract.

Main-model priority remains an explicit prior-aware decoder outside this
class, or a strong original-data classical attack. Merely generating better
classical witnesses, varying collimation buckets, or adding a public diagonal
phase before measured-pair extraction does not supply a quantum contribution.
