# Adaptive Pilot Policies At The Receiver Boundary

29 October 2026. A conditional mathematical composition and a checked
classical transcript compiler, not an executed quantum receiver, a new
hardness result, or an established quantum speedup.

## Scientific Question

Does selecting a cancellation witness after measuring pilots and banks
bias the surviving quantum state, or omit the mass and cost of rejected
sources? The preceding [pilot compiler](PILOT_SUBMODULE_COORDINATES.md)
verified original mixed-modulus equations, but its callback supplied only
classical labels. A successful arithmetic transcript is not a quantum
source or an implementation of the receiver.

The constructive answer is conditional: embed the bounded policy in a
fixed, fully charged independent tensor, prove the output for each full
record, and only then average. Adaptive selection does not require witness
randomness to be independent of measured labels. Source independence and
valid subgroup-preserving actions, however, cannot be dropped.

This removes a composition gap in the proposed Rees central descent.
There is no independent asymptotic advantage claim for this wrapper.
Its significance depends on an end-to-end native problem and on supplying
the promised source, actions, coordinates, runtime and final recovery.
The existing classical stabilizer filters remain applicable to their
stated families; surviving this receiver check does not evade them.

## Fixed Source Bank And Operational Promises

Fix an ambient central character module with cyclic exponents a_j,
rank R, prime p and degree d<p. Let B_R be the ambient per-episode
envelope already derived by the spanning-block construction. For at most
t episodes, allocate N=t*B_R sources in the joint state rho_H tensor N.
Every source has the same explicit ambient group G, central subgroup Z,
quotient Q=G/Z and hidden subgroup H. No new source depends on an unobserved
quantum state or on changing the ambient group during this invocation.

Perform each local central-character measurement. Its full measured
record is y=(y_1,...,y_N), including labels never requested by the
controller. Reveal only the sequential prefix requested by the existing
policy. Fresh pilot and bank requests consume distinct positions. Unused
suffix labels cannot affect its choices. Measuring these suffixes and
then forgetting them has no effect on the used slots of the independent
tensor. The equivalence would not follow from matching marginals alone.

For an accepted record, retain a nonempty set A of original, nonpilot
bank slots with unit scales s_i. For all central coordinates j require

```text
sum_(i in A) s_i^d * y_ij = 0 mod p^a_j.
```

The corresponding group automorphisms must preserve H and restrict on
Z to z -> s_i^d*z. In a Rees application this is a property of the lifted
hidden subgroup, not permission to assume arbitrary dilations preserve
an arbitrary hidden subgroup. Public representatives of Q and reversible
group actions must be supplied efficiently without H advice.

Apply the appropriate controlled translation to each active target.
Every other slot has identity group action and is eventually traced out.
In particular, zero coefficient means discard/identity, NEVER dilation
by zero. Rejected episodes, pilots, rejected blocks and padding remain
part of the charged source tensor. An all-abort outcome discards all
sources and returns a fixed orthogonal abort flag.

This preallocated implementation costs N sources, not the number of
callback labels observed. It may retain O(N log|G|) target qubits plus
measurement/control workspaces. A streaming memory improvement would
need a separate lifetime argument. There are at most N central
measurements and N nontrivial controlled translations; their gate costs,
uniform control preparation, source production, coordinate arithmetic and
classical solver time must also be paid. None is measured by the Python
transcript replay.

## Pointwise Output Before Averaging

Write P_y for the tensor of unnormalized measured source branches and
p_y=Tr(P_y). The tensor factorization uses JOINT independence. Let u
encode a finite randomized controller outcome, with conditional law
K(u|y)>=0 and sum_u K(u|y)=1. The controller is LABEL-ONLY classical
processing with source-independent private randomness: conditional on y,
its choice cannot steer the residual quantum state. An arbitrary table
K(u|y) alone does not establish this Markov condition. The law may depend
on labels. A bounded random-bit implementation supplies a finite outcome space; an
uncapped expected-time solver has not thereby acquired a hard clock.

For every accepted (y,u), active-slot character cancellation gives

```text
output(y,u) = p_y * K(u|y) * rho_(HZ/Z).
```

Inactive normalized factors have trace one, and their unnormalized
branch masses remain in p_y. If any source branch has zero mass, its
projected matrix is zero, so the identity still holds without dividing
by that mass. A nonempty active set is essential: without it there is
no factor forcing zero correlation outside HZ.

In the explicit mixed-modulus character pairing,

```text
chi_y(z) = exp(2*pi*i * sum_j y_j*z_j/p^a_j),
```

the displayed native congruences imply that
sum_(i,j) s_i^d*y_ij*z_j/p^a_j is an integer for every z. Hence the
active character product is one. This pairing calculation is a written
derivation with exact rational controls, not a Lean compiler from the
Python transcript to its Witness.Valid hypothesis.

The complete output, retaining records, is

```text
sum_accept p_y*K(u|y) |y,u,accept><y,u,accept| tensor rho_(HZ/Z)
 + sum_abort p_y*K(u|y) |y,u,abort><y,u,abort| tensor |abort><abort|.
```

Record distributions may depend on H; the normalized successful target
does not depend on which successful record occurred. The success and
abort weights sum to one when the measured input ensemble is complete.
No branch is promoted by postselection and no acceptance probability is
divided out. Correctness for accepted incomplete pilot frames remains
valid, but their availability cannot be inferred from one transcript.
The earlier bound (3/16)^t applies only under its IID-uniform label and
supported solver assumptions, before observing the pilots.

## Lean Scope

`formal/Formal/CentralDescentPolicy.lean` contains the 16 policy theorems
and eight full-dual measurement bridge theorems, with local and global
axiom guards. It reuses existing character-correlation and
controlled-action identities, generalizing inactive-slot padding from
field scalars to automorphisms of an arbitrary finite central abelian
group. The substantive steps are:

- `normalized_padded_correlation`, `normalized_padded_output`: active
  automorphisms cancel the central character, inactive targets trace out.
- `all_record_output`: multiply back every branch mass, including zero.
- `accepted_output_factorization`, `accepted_output_trace`: derive the
  selected matrix and trace from actual actionOutput, not an assumed
  desired output.
- `abort_output_factorization`, `accepted_abort_trace_conservation`:
  discarded packet traces retain the complementary mass.
- `ChoicePolicy` and the randomized conservation theorems: weights may
  depend on labels and are nonnegative and normalized per label.

The abstract relation to an arbitrary supplied input matrix assumes
explicitly that the sum of measured packets equals that input. This is
an INPUT ensemble completeness premise, not a proof that arbitrary labels
are physical measurement outcomes.

The subsequent full-dual bridge removes that extra premise for the actual
central-ancilla measurement on an independent coset tensor:

- `measuredBank` is the literal product ancilla-Kraus action on supplied
  copies; it is not a map that clones an unknown single input.
- `measured_bank_eq_packet` derives every unnormalized record from those
  operators, using the existing two-sided measurement theorem.
- `projected_sum`, `packet_sum`, `measured_bank_sum` sum the FULL dual.
  Centrality is required for the physical two-sided source identity.
  The one-sided algebraic sum alone is not a physical branch assertion.
- `independent_source_trace`, `measured_bank_mass_sum` derive total mass
  one from the actual coset source.
- `measured_accepted_output_factorization` expresses the accepted output
  using actual measured branch traces.
- `measured_randomized_output_trace_conservation` derives total accepted
  plus abort trace one without a supplied completeness premise.

These statements cover any finite additive abelian center, including
mixed prime-power centers. They do not give an efficient enumeration of
its full dual. The explicit-coordinate implementation argument below is
separate from the Lean refinement of the Python controller.

The module proves matrix-entry and trace identities. It does not extract
typed positivity/CPTP certificates, a quantum circuit, a terminating policy,
an efficient mixed-ring character compiler or a source-ownership proof.
The user-supplied policy validity and input-ensemble premises must remain
visible at every later specialization.

## Complete-Channel Error Accounting

### Explicit Cyclic Coordinates Do Not Require A Hidden Dual Basis

When the PUBLIC center has coordinates Z=direct_sum_j Z/m_j with
m_j=p^a_j, use the pairing chi_y(z) displayed above. It enumerates every
character exactly once: evaluation at each public coordinate generator
distinguishes y_j modulo m_j, and a character on a cyclic factor is fixed
by an m_j-th root of unity. Products of these cyclic characters cover the
direct sum. This construction depends on the ambient module, not on
H intersect Z or on a basis of its annihilator. The hidden annihilator is
the distribution SUPPORT discovered by the measurement, not input advice.

Operationally, prepare a uniform ancilla on Z, perform the full-register
controlled right translation by the inverse of its embedded value, then
apply the negative-convention product QFT and measure that ancilla only.
The surviving target remains a G register. In the same convention as
`CentralSpectralProjector`, its Kraus operator is

```text
K_y = (1/|Z|) * sum_z conjugate(chi_y(z)) * R_(embed z),
R_g |x> = |x*g^(-1)>.
```

The uniform ancilla itself can be prepared by the positive QFT on zero.
This uses cyclic QFTs, not an exponentially enumerated character table or
a nonabelian QFT. For an explicit injective center embedding and efficient
reversible group arithmetic, the remaining prerequisite is a compiled
approximate cyclic QFT and its error allocation. The published
[Cleve--Watrous Theorem 5](https://cs.uwaterloo.ca/~watrous/Papers/ParallelCircuitsQFT.pdf)
gives circuits of size polynomial in log(m)+log(1/eta) for arbitrary m.
This is an imported quantum primitive, not an implementation in this repo.
Gate synthesis, workspaces and invalid binary encodings still require a
consistent reversible implementation.

If each cyclic QFT implementation, with cleaned workspace, approximates
its ideal isometry in operator norm by eta_j, its complete channel has
half-diamond error at most eta_j. Using it once for preparation and once
for readout costs at most 2*sum_j eta_j per central measurement, plus
the controlled-translation implementation error. This follows by a
unitary/isometry hybrid, including arbitrary references, then tracing out
workspace. Basis-vector tests or agreement of measured label frequencies
alone would not establish this operator-norm premise.

Thus an arbitrary mixed-order center is not an unknown Fourier primitive
in the EXPLICIT coordinate input model. What remains unimplemented is
the concrete compiler and its connection to the checked transcript and
source interfaces. An opaque group without supplied/obtained center
coordinates does not inherit this construction for free. No additional
scope or novelty claim follows from importing the standard cyclic QFT.

29 October implementation boundary: `mixed_modulus_receiver_compiler.py`
now supplies a DENSE finite numerical reference, not that scalable
compiler. It materializes matrices on ancilla times target and optionally
checks supplied central-intersection/density diagnostics. Those diagnostics
do not provide hidden subgroup advice to a real algorithm or certify an
arbitrary supplied density as rho_H. Gate synthesis, valid binary
encodings, workspace cleanup and the recursive source factory remain
unimplemented. The independent
[execution audit](audits/reviews/2026-10-29-gemini-execution-audit.md)
found malformed-input and error-allocation defects missed by its initial
tests; consult that audit's repair status, not the original blanket
completion statement.

### Unconditional Hybrid

Let the ACTUAL JOINT input be within delta_in trace distance of the ideal
independent tensor. Suppose complete measurement and controlled-action
channels have respective half-diamond error bounds eta_m and eta_a,
uniform over classical records and arbitrary reference systems. Include
uniform-control preparation and any other omitted operations in delta_c.
For at most M measurements and A actions the unconditional hybrid bound is

```text
delta_hybrid <= delta_in + M*eta_m + A*eta_a + delta_c.
```

For nonuniform stage tolerances this becomes
`delta_in + sum_t M_t*eta_(m,t) + A*eta_a + delta_c`.
The weighted average measurement tolerance is not itself a per-call
upper bound. The stage-aware calculator must retain the actual sum and
per-stage counts, with abort terms added once for the complete flagged
output. Neither formula verifies its source, channel-error or call-cap
premises.

This is the usual channel-composition inequality applied to complete
classical-quantum instruments, not a new theorem: see Watrous,
[The Theory of Quantum Information, Proposition 3.48](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf),
printed page 174. Keeping the classical transcript inside the channel
allows the same hybrid argument for adaptive control. Bounds on only
accepted subchannels or individual input marginals do not suffice.

If ideal abort probability is at most beta and a separate clock
truncation changes the full output by at most tau, the total unconditional
error/abort allowance is at most min(1,beta+delta_hybrid+tau).
`flagged_error_bound` performs this exact Fraction arithmetic; it does
NOT verify any of the premises, clocks, probabilities or call counts.
The reference is an unflagged ideal target with failures counted as
errors, not the actual conditional-on-success state.

## Decisive Falsifiers

**Matching marginals do not imply a valid receiver input.** Take G=Q=C3,
trivial central subgroup and H={0}. On two targets define

```text
rho[(x,y),(u,v)] = 1/9 if x-u = y-v mod3, and 0 otherwise.
```

This is the positive mixture (1/3)*sum_k
|Fourier(k),Fourier(-k)><Fourier(k),Fourier(-k)|. Both marginals are I3/3.
Their independent product gives receiver output I3/3; the correlated
state is invariant under simultaneous translation and gives J3/3,
trace distance 2/3 from the target. Character cancellation is trivial
and exact in both cases. Thus a marginal-only source contract is false.
The tiny negative numerical eigenvalue in the saved floating-point
control is rounding; positivity follows from the displayed decomposition.

**Accepted-only error can amplify.** With alpha=1/100 and delta=1/1000,
the normalized full diagonal states on abort/good/bad are
(1-alpha,alpha,0) and (1-alpha,alpha-delta,delta). Their distance is
delta, but conditioning on acceptance gives distance delta/alpha=1/10.
An unconditional budget cannot be relabeled as a conditional budget.

**Correct choice probabilities do not certify private randomness.** Let
G=Q=C3, Z and H trivial, and let a single source have marginal I3/3.
Supply forbidden auxiliary information k identifying its pure Fourier
component, uniformly distributed over k=0,1,2. Choose the automorphism
scale1 for k=0,1 and scale2 for k=2. All actions preserve H and the
central cancellation condition is trivial. The actual output has Fourier
weights (1/3,2/3,0), at distance 1/3 from I3/3. The SAME choice
probabilities (2/3,1/3), applied independently to the same marginal source,
give I3/3. Thus even a normalized label-conditioned table and a correct
source marginal do not justify multiplying K(u|y) by P_y. Private coins
or an equivalent conditional quantum independence statement are needed.

These finite controls falsify invalid assumptions. They are not oracle
problem proposals, algorithm discoveries or hardness evidence.

## Implementation And Live Replay

Run `python qsearch.py prime-power-sde --receiver-policy --write`.

`theorems/pilot_receiver_policy.py` checks fixed episode contracts,
canonical labels, charges, first-success stopping, distinct selected
nonpilot requests and the original ambient equations. It compiles sparse
active raw-slot positions against the fixed N-slot bank. It does not
reconstruct source probabilities or certify physical source handles.
Report flags for physical ownership, quantum execution, policy availability
and speedup remain false. The five deterministic fixtures currently have:

| Control | Fully charged N | Observed labels | Active slots |
| --- | ---: | ---: | ---: |
| ambient_mod_p_zero | 249 | 11 | 4 |
| oblique_mixed_order | 984 | 37 | 6 |
| cubic_embedded_support | 1632 | 49 | 15 |
| incomplete_pilot_retry_control | 166 | 15 | 6 |
| zero_support_control | 328 | 5 | 1 |

Saved artifact: `research/reductions/pilot_receiver_policy.json`.
Tests cover malformed transcripts, zero support, all-abort policies,
mixed-order phases, unused suffixes, all three falsifiers and exact budgets.

## Independent Review And Repair

One fresh independent automated reviewer found a real implementation
defect: a one-shot scale iterator was consumed by equation verification,
then appeared empty when constructing the active slot list. The compiler
could report acceptance with no active sources. Ordinary serialized
list/tuple histories were unaffected, but the callable interface violated
the mathematical nonempty-support premise.

The parent reproduced this before editing. Scales are now materialized
once, before both operations, and accepted plans explicitly require
nonempty support. A regression compares the iterator and list plans.
The review also prompted the private-randomness clarification and third
falsifier above. The reviewer found no further flaw in the scoped
preallocation, pointwise output, input-completeness or unconditional
hybrid arguments. This is automated adversarial review, not human
specialist validation or an originality assessment.

The reviewer subsequently verified the repair and both new targeted
tests. It also derived the source-steering example using exact symbolic
Kraus matrices, confirming weights (1/3,2/3,0) and distance 1/3 without
postselection. No remaining actionable defect was reported in that scope.

## Next Decision

Do not add more fixed-branch identities by inertia. The remaining
constructive question is whether a finite recursive source factory can
instantiate the mixed-order measurements/actions and bounded classical
policy with an honestly composed total copy, qubit and error budget.
Resolve that or expose a counterexample before claiming a full converter.
Compare its resulting resource dependence with known algorithms and
matched native classical attacks before promoting any application.
An explicit hard native reduction and human specialist assessment remain
missing. This receiver result supplies neither.

## Verification And Changed Files

The initial 602-test selection passed but missed the scale-iterator defect;
the independent review found it afterwards. After the repair and third
falsifier, **604 selected tests passed in 87.51 seconds**. This is the
22-file selection in PILOT_SUBMODULE_COORDINATES.md plus
`tests/test_pilot_receiver_policy.py`, not the entire repository suite.
The final CLI/policy-focused run passed 31 tests. Commands used the existing
Anaconda Python 3.13.5, disabled plugin autoload, external pycache prefix
`/tmp/qsearch-policy-pycache`, and `-q -p no:cacheprovider -W error`.

All eight touched/reused Python syntax checks, all 12 site JavaScript
syntax checks, `python qsearch.py validate`, and tracked/new-file whitespace
checks passed. Validation returned `valid:true, issues:[]`: 8 candidates,
796 experiments, 807 results and 973 negative results. No registry claim
was promoted. Five final saved plans were independently replayed without
the production plan/equation validators. The final artifact hash is
`7aa6d9acae49cbc183216278d0e29bfd1d7bae0fd4d30820fb0f452adf693234`.

The pinned Lean 4.35.0 worker build of `Formal.CentralDescentPolicy` and
`Formal.Audit` passed with `--no-cache` and `--wfail` (3,474 jobs including
cached dependencies). All 24 local and corresponding global axiom guards
permit only `propext`, `Classical.choice`, and `Quot.sound`. The parent
independently repeated the default `lake --no-cache build --wfail`:
exit 0, 3,498 jobs including cached dependencies. The parent read the full
eight-theorem measurement bridge; the independent reviewer
reviewed the preceding policy theorem and Python implementation, not
this later bridge. Do not describe the bridge as independently reviewed.

| File | Pass-specific change |
| --- | --- |
| `theorems/pilot_receiver_policy.py` | Checked padded raw-slot plans, exact error calculator, three source/conditioning falsifiers. |
| `tests/test_pilot_receiver_policy.py` | 23 policy tests, including the iterator regression. |
| `qsearch_cli/commands/sde.py`, `qsearch.py` | Mutually exclusive `--receiver-policy` mode, Fraction serialization and command documentation. |
| `tests/test_cli_parser_integrity.py` | Actual artifact-write workflow and mode-exclusion checks. |
| `formal/Formal/CentralDescentPolicy.lean` | 24 policy and full-dual measurement theorems. |
| `formal/Formal.lean`, `formal/Formal/Audit.lean` | Default-build import and matching axiom guards. |
| `research/reductions/pilot_receiver_policy.json` | Five fully charged plans and three falsifiers; no quantum-execution claim. |
| `README.md`, `formal/README.md`, `research/PILOT_SUBMODULE_COORDINATES.md` | Current scope, entry point and follow-up links. |
| `research/PILOT_RECEIVER_POLICY.md`, `research/AGENT_HANDOFF.md` | Mathematical argument, review repair, evidence and remaining obligations. |

Existing unrelated changes were preserved. Argon's received review remains
unchanged (SHA-256 `78a1ce07a17bf5bb2d6fdd0ddc72c2eaa3983dbe5f7d856da901094825b73aac`).
No commit, push, dependency installation, UI redesign or external contact
was performed.
