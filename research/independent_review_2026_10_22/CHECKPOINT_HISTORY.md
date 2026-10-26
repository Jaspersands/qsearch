# Independent adversarial review — 22 October 2026

Started 2026-10-22 10:29:22 UTC (21:29:22 Sydney). Deadline 16:29:22 UTC
(03:29:22 Sydney, 23 October), subject to actual tool/usage limits.
All review edits are confined to this new directory. No agents, other-chat
messages, automations, Git changes, or cloud-file repair are authorized.

## Current assessment

**Proved deduction, independently reconstructed:** the balanced-source
support-mask estimate and singleton-erasure state identity are consistent.
They give the advertised ideal quantum success bound when combined with a
complete bounded GS decoder. See `QUANTUM_AUDIT.md`. This is mathematical
review, not a compiled-circuit or hardware verification.

The later full-list projection variant also survives independent review.
The strongest deduction is now the EXACT native success identity
lambda_b*(1-delta)^2/P, with P the fixed padded list size and lambda_b the
native solution count relative to its balanced baseline. Conditional on
native success its output is exactly uniform. This avoids the separate
coherent-tail and rare-ambiguity premises for this variant. See
EXACT_PATTERN_CHANNEL.md. It is an ideal algorithmic theorem, not evidence
of classical difficulty or certified novelty.

**Verified prior art:** Jo (July 2026), Theorem 5.2, already gives the paid
fixed-length full-list operation. Horinaga–Yamakawa (July 2026), Theorem 5.1,
already implies polynomial quantum success after substituting the native
tail and fiber-count estimates. Their generic theorem allows characteristic
two, although their main OPI specialization requires growing characteristic.
The candidate contribution is therefore the explicit native specialization,
not a new quantum decoding/interference mechanism. See LITERATURE.md.

**Strongest finding — proved classical algorithms on broad native slices:**
for every sufficiently large even n, ANY supplied distinct public points
and any target with at least 2K zero bits have a polynomial classical
solver. For n divisible by three, the same holds with at least 3K zeros.
The first uses a subfield, matroid union and paid coset sampling; the second
uses random accepted subfield lines, an independent-transversal argument,
and a nonzero-determinant sampling bound. Neither assumes random points
or a supplied witness. Uniform targets meet the respective thresholds
except with probabilities at most exp(-N/8) and exp(-N/32). See
SUBFIELD_EXTENSION_ATTACK.md for the proofs and explicit failure costs.
These attacks supersede the initial rank-conditional even-degree result.

**Open:** no polynomial classical solver or hardness result has been
established for the entire worst-case native relation. The new attack
does not cover prime n>3 or arbitrary targets with too few zero bits.
The earlier n=17,31 flat witnesses also pass independent verification,
but certify only those instances. Source access and stationary Gibbs
success do not resolve the remaining classical search question.

## Ranked unresolved obligations

1. Extend or decisively delimit the new subfield attack on the *given*
   points and bits: prime n>3 and too few zero targets remain unresolved
   at N=n², K=floor(N/8). Rank-deficient evaluation sets are now handled
   in the proved subfield-enabled families. Any claimed hard distribution
   must account for these classical algorithms; prime n is not an existing
   input promise.
   CLASSICAL_RESTRICTION.md gives a polynomial randomized reduction to
   an affine residual system with only Theta(n) free field variables;
   solving that system remains the concrete missing step.
2. Determine whether uniform-start search is fast for a stronger classical
   proposal. Worst-start Gibbs obstruction begins at solutions and alone
   says nothing about first hitting.
3. Establish novelty of the explicit inverse-trace specialization beyond
   the primary results in LITERATURE.md. Both the full-list mechanism and
   a generic theorem implying native success are now verified prior art.
4. Stress-test the quantum derivation at its actual interfaces, including
   the entire reversible decoder and input-size conventions. A practical
   gate count is separate from polynomial-time existence.

## Evidence and availability

Read the five requested notes, using only recent sections of the large
priority file. Relevant source modules are locally resident.
`research/PRIME_CHARACTER_NORM_ATTACK.md` is marked `compressed,dataless`;
it was skipped without opening or repairing it. The shared field backend
is reported unavailable by the source notes; imports will be avoided unless
its residency is checked. No source test suite has been run.

## Checkpoints

- Initial reconstruction: no missing q^K factor was found. The tail requires
  signed support-cell cancellation; ambiguity requires the separate list-size
  estimate. Neither argument can be replaced by ordinary decoding error alone.
- Strongest falsifier of that reconstruction: an exact support-only mask
  violating the correlation bound, or a retained coset with two admissible
  errors despite a genuinely complete singleton list. Both are concrete
  algebraic claims rather than finite-success heuristics.
- Constructive classical result: systematic accepted-root proposals have
  success exactly (1+e_b)2^-K, |e_b|<=eta. A latent-constraint mixture gives
  a direct polynomial sampler for moderate-temperature native Gibbs laws
  (fixed M<15 at rate 1/8), but does not reach the M>=N search regime.
  See `CLASSICAL_SAMPLING.md`, including the rare-event/TV self-attack.
- The support-mask method extends to nonbalanced root sets with an explicit
  density factor. An unchanged-bound counterexample at density 3/4 is
  computed algebraically in `MASK_GENERALIZATION.md`. The balanced theorem
  survives this adversarial check; exact balance is not the most general
  sufficient condition.
- Independent checkpoint: the existing n=17,31 witnesses satisfy every
  original equation, and exact rational arithmetic reproduces the n=17,31,61
  quantum failure budgets. These are witness checks and mathematical bounds,
  not large quantum executions. See checkpoint_verification.json.
- Rational-attack falsifier: minimum-support scaling can fail even in odd
  field degree. An explicit F_32 odd linear dependency contradicts the
  required all-one trace equations. See CLASSICAL_ALGEBRA.md. Larger adaptive
  families remain open; the counterexample does not imply classical hardness.
- The Gibbs worst-start argument survives review, but begins with a full
  solution. GIBBS_AUDIT.md separates it from the still-open uniform-start
  first-witness question and records the constructive moderate-temperature
  sampler's exact limitation.
- The shared priority note changed during the review. Its new full-list
  projection was read and independently reconstructed; the paid 1/P factor
  and clean workspace are valid, and a sharper success bound is recorded
  in QUANTUM_AUDIT.md. The older singleton audit remains valid as a separate
  protocol, not as the only route to an efficient quantum solver.
- Stronger subsequent deduction: the support-subspace Gram spectrum is
  exactly the vector of relative native fiber counts. The full-list success
  formula and exact conditional uniformity follow from an N-bit Hadamard
  change of basis; no coherent-tail inequality is needed for that success
  calculation. The formula reproduces 605/2048 in the saved F_8 fixture.
- Literature self-attack found a direct antecedent for the full-list
  operation and a generic worst-case theorem. The quantum reconstruction
  survives, but the initial candidate novelty statement has been narrowed.
- A stronger classical deduction now samples the exact coalesced
  Fourier-side probability law using signed Walsh queries, the complete
  decoder and rejection with acceptance at least (1-eta)/P. The final
  inverse-Fourier witness readout remains unresolved; source access and
  erasure-side sampling alone are not the quantum advantage. See
  CLASSICAL_FOURIER_BRANCH.md.
- The full-list proof also includes the limiting check rate K/N=1/4,
  paying P=O(N) and Omega(1/N) native success. The separate negligible-tail
  argument does not cover that boundary. See BOUNDARY_AND_DENSITY.md.
- A one-quadratic-per-coordinate reformulation is exact only after
  excluding x_i=0 at target-one coordinates. Without that condition it
  returns the invalid all-zero word for every nonzero target. Its apparent
  binary linear solve has exactly the original trace compatibility defect.
  See CONIC_REFORMULATION.md; this is an attack formulation and a concrete
  false-solver counterexample, not a classical lower bound.
- Classical sampler self-correction: rare rejection of active sets is
  avoidable by direct truncated-binomial sampling, even at M>=N. Its
  failure there is approximation quality. An exact tilted-binomial
  calculation now gives this sampler's native hitting probability and
  the witness-blind interval 8<M<15; extra rejection-conditioned
  constraints preserve the paid systematic-root success product.
- A useful algebraic simplification is proved: for every sufficiently
  large native instance, the fraction of valid witnesses with any zero
  coordinate is at most (2N/q)*(1+eta_(N-1))/(1-eta_N). Thus a classical
  solver may target the all-nonzero stratum without adding an input
  promise. It must still enforce nonzero coordinates; arbitrary zeros
  of the unsaturated quadratic system remain false answers. See
  CONIC_REFORMULATION.md.
- A constructive second-moment reduction now samples accepted values on
  all but K+ceil(4K/n) coordinates. The prefix has a full native extension
  with probability 1-2^-Omega(n²), uniformly in the public points and bits.
  The residual affine system has only ceil(4K/n) free field variables, but
  finding its extension is still open. This is a paid classical reduction,
  not a witness-finding algorithm or a substitution of input promises. See
  CLASSICAL_RESTRICTION.md.
- Reciprocal elimination has an exact ordinary-degree obstruction: its
  first nonzero code identities have degree N-K (also over finite native
  points once q>N*(N-K)). More decisively for correctness, the complete
  reciprocal closure contains sparse points satisfying some target bits
  whose totalized inverses fail Hx=0. An attack must enforce the open
  nonzero stratum. These are algebraic deductions, not a classical
  complexity lower bound; trace/Frobenius methods remain open. See
  RECIPROCAL_ELIMINATION.md.
- A stronger classical attack now solves a natural even-degree native
  distribution in polynomial time. It uses the actual subfield, checks
  the full required rank, handles odd target parity with a paid buffer
  sampler, and never substitutes a witness or changes input points.
  The n=20, N=400, K=50 control produced valid witnesses at binary rank
  990 for both even and odd numbers of one targets. A subfield-point
  one-hot input correctly returned UNKNOWN at rank 500 and an inconsistent
  affine correction. See SUBFIELD_CLASSICAL_ATTACK.md and
  subfield_attack_receipt.json. The probability theorem, not these finite
  controls, establishes the average-case result.
- Arbitrary-point strengthening: matroid union repairs the even-degree
  rank obstruction with multiple buffers; relative-trace-zero inverse
  directions give a separate degree-three extension algorithm. The old
  n=20 one-hot counterexample is now solved, and an n=21, N=441, K=55
  fixed-point input is solved at full binary rank 1155 on the first
  direction trial. Both saved witnesses satisfy every original parity
  equation and inverse-trace bit. The finite controls test the interfaces;
  the rank and sampling proofs establish the asymptotic guarantees.
  See SUBFIELD_EXTENSION_ATTACK.md and subfield_extension_receipt.json.

## Final adversarial pass on the central deductions

The concise FINDINGS.md and current subject proofs supersede earlier
scope statements in this historical checkpoint. This pass checked the
following mathematical failure modes without repeating the test suite.

- **Subfield attack:** MDS independence is over the supplied full field;
  the matroid ranks are over the explicit subfield. Scalar-orbit expansion
  makes binary rank exactly m times subfield rank. The even-degree union
  inequality produces disjoint COMPLETE bases, not merely many independent
  columns. Each sampled coset changes only a syndrome component already
  spanned by the free zero coordinates. Both the rank proof and the paid
  sampling bound remain necessary.
- **Degree-three determinism:** independent a,b in the relative-trace
  kernel have a/b of degree three, which proves independence of the three
  inverse directions. The Rado inequalities hold for every public point
  set. The n=6 exchange fixture demonstrates why one may not replace
  matroid intersection by a claim that greedy assignment always works.
- **Quantum normalization:** the original untruncated attempt has success
  lambda_b*tau^2/P. Direct normalized ball-source preparation instead has
  lambda_b*tau/P and costs polynomial work by reversible integer unranking.
  These refer to different source protocols. All retained source, message
  and index labels must be erased as stated. No free normalized coalescence
  or variable list-length projection was assumed.
- **Classical reductions:** syndrome second moments are averages and are
  transferred to the actual sampled prefix only through the proved TV
  bound. Low-degree multiples retain the false zero point at bit one;
  reciprocal closures retain false boundary points. Neither a generic
  low-degree solver nor an extension oracle has been silently supplied.
- **Sampling versus search:** the rare-subfield event bounds uniform native
  sampling by counting ALL choices of correction positions. Consequently
  randomizing those positions does not remove the specific solvers' bias.
  This is not a lower bound on different classical samplers.
- **Scope:** composite degrees coprime to six are not silently counted as
  covered. The strongest main guarantees concern even degrees or degrees
  divisible by three with their stated zero counts; method B adds only
  its explicitly charged zero-rich cases. A broad easy subfamily does not
  refute a possible worst-case advantage on a remaining subfamily.

No new fatal quantum proof error was found in this pass. The decisive
remaining investigation is a constructive solver for the residual affine
inverse-trace problem on uncovered inputs, especially prime degrees, or a
classical sampler that escapes the subfield restriction while controlling
its output law. More successful finite fixtures would not settle either.
