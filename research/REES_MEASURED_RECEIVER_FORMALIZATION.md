# Measured Class-Three Rees Descent

27 October 2026. Machine-checked ideal measurement and source-composition
identities. Not a novelty certificate, a compiled quantum circuit, a
polynomial-time solver implementation, or a demonstrated quantum speedup.

## Scientific Decision

The previous pass was PROGRESS: it constructed actual central quotients
and derived the class-three branchwise receiver identities. Its remaining
normalized-source premise was not yet connected to a complete physical
measurement. The question here is whether that connection survives all
records, including zero-probability labels, inactive targets and arbitrary
nonnormal hidden subgroups.

Before choosing this pass, the current native codeword and norm-sampler
notes were compared with the receiver gap. The randomly punctured
Reed--Muller full-support problem is not covered merely by the complete-AG
classical filters. However, its two-fold quantum decoder is already in
[Ragavan--Shutty, v2](https://arxiv.org/html/2610.00502v2); importing it or
repeating parameter sweeps would not constitute a new mechanism. No new
constructive native sampler was established in this comparison. This is
not evidence of classical hardness. The existing bounded-prime receiver
comparator remains [Imran--Ivanyos](https://arxiv.org/abs/2304.08376).

A focused theorem audit found that linear-character completeness ALREADY
exists in `RetainedFourier.linearCharacter_bijective`. A redundant temporary
draft was removed before integration. The genuinely missing bridge was
the full-register two-sided spectral measurement, not another Fourier
bijection or a new research framework.

## Input And Mechanism

The concrete result concerns finite L over the prime field F_p, p>3, with
nilpotency class at most three, and arbitrary H in its BCH group. The
initial source in this pass is the exact coset density of the actual
lifted subgroup in the degree-three Rees group. Preparing that source
from the original coherent oracle is a separate obligation; this pass
does not replace its cost by a supplied witness or hidden subspace.

The public operation measures the central character on the FULL group
register. A classical policy returns a nonzero SDE witness from the
measured label tuple. Zero scales receive identity controls; their target
registers are still consumed and traced out. Cubic descent is followed by
quadratic descent on disjoint fresh banks. The terminal source retains
all log(H), not just an abelianized image.

The policies are supplied total functions satisfying exact witness laws
for every label tuple. Their existence at the chosen batch size, efficient
construction, finite-time failure handling, and gate complexity are not
proved here. No classical lower bound or useful native hard application
is added. The proposed asymptotic claim is unchanged.

## New Proof Coverage

### Full-Register Spectral Measurement

`formal/Formal/CentralSpectralProjector.lean` defines the actual central
ancilla permutation and its Fourier-measurement Kraus amplitudes. The
target is never compressed to a quotient-transversal register.

The module proves equality with the full-register character projector,
self-adjointness, idempotence, orthogonality, the complete projector sum
and Kraus completeness over ALL additive characters. It reuses the
existing dual orthogonality theorem. Centrality then proves commutation
with the arbitrary-H coset density and the exact identity

    P_chi rho_H P_chi^dagger = projectedEntry(H, embed, chi).

This discharges the old one-sided versus two-sided source gap. No hidden
normality or trivial central intersection is required. The identity also
covers zero branches. A nontrivial base character is required when the
full character family is reindexed by linear labels; zero LABELS remain
valid and must not be confused with a trivial BASE character.

### Every Record And Every Consumed Target

`formal/Formal/CentralDescentRecords.lean` proves the actual two-sided
tensor-Kraus identity on an independent source bank. It then proves

    output(lambda, s) = (product_i p(lambda_i)) rho_(H image in Q)

for every valid nonzero SDE witness, without assuming each label has
positive probability. Here p is the actual projected-source trace.
Impossible records give the zero matrix without normalization. Inactive
targets use identity controls inside the SAME full input bank; they
contribute their trace factors rather than disappearing.

The relation is pointwise in labels and witnesses. Consequently the
normalized quotient source does not depend on a retained valid record.
This does not license sharing a correlated source bank or replacing its
joint state with an unjustified tensor of its marginals.

### Concrete Measured Rees Composition

`formal/Formal/ReesMeasuredReceiver.lean` reuses the existing character
equivalence, proves linear-label measurement completeness and total branch
mass one, and identifies literal product-Kraus branches with the sources
consumed by the all-record theorem.

`measured_step_output` instantiates the actual Rees centers, weights,
dilations, hidden images and quotient maps. `averaged_step_output` sums
ALL measured labels for a label-dependent valid witness policy. The
cubic and quadratic corollaries use the previously constructed canonical
sections, not a supplied homomorphic-section premise.

`convertStep` is an H-independent expression for this operation.
`two_stage_source` substitutes the cubic output into the quadratic stage,
and `measured_terminal_source` identifies the resulting matrix with

    rho(x,y) = 1/|L| if BCH.mk(y-x) belongs to H, else 0.

Tensoring a matrix rho in this expression denotes fresh supplied copies.
It is NOT a physical cloning channel on one unknown input. With cubic
bank size M3 and quadratic bank size M2, one terminal output consumes
M2*M3 lifted source copies, including all inactive targets. Original
source preparation costs are additional and unchanged. The definitions
are noncomputable finite mathematical matrices, not efficient dense
matrix implementations or extracted quantum programs.

## Decisive Controls

Two new tests extend `tests/test_central_quotient_receiver.py`:

* Exhaust all 9^5 = 59,049 five-label records for UT3(F_3) x F_3 with
  the same nonnormal H and proper nontrivial central intersection as the
  previous pass. All 3^5 = 243 positive records and all impossible records
  satisfy the unnormalized output law. Their outputs sum to the quotient
  coset density with trace one. The witness depends on the full record
  and may use zero scales.
* Omitting four inactive branch masses makes the selected branch trace
  too large by 81. Accepting an all-zero witness produces the uniform
  pure address state rather than the required quotient coset density.

The bounded F_3^2 subset finder is only a finite test control. It is not
the proposed general diagonal-system solver. This fixture tests the
generic channel theorem, not the p>3 cubic BCH construction. Existing
class-three source controls remain in the connected regression run.

## Independent Review

An independent read-only reasoning reviewer inspected the spectral,
all-record and concrete-composition modules and found no algebraic defect.
It confirmed the signs, arbitrary-H normalization, actual tensor branches,
inactive factors, nontrivial-base-character condition and full log(H)
retention. It also emphasized that `convertStep` is nonlinear as a function
of a SINGLE rho matrix: the physical channel is linear on the supplied
whole bank. The M2*M3 consumption above is of LIFTED source copies, not
free original-oracle queries. Automated review is not human validation.

The reviewer noted that total witness policies cannot simply be assumed
at any batch size: a singleton nonzero linear label has no nonzero scalar
witness over a field. The statements quantify over valid total policies;
they do not manufacture one or certify that an arbitrary chosen arity works.

## Verification And Provenance

The default Lean build passed with warnings fatal: 3497 jobs including
cached dependencies. Independent strict checks of all three new modules
and `Formal/Audit.lean` passed with implicit variables disabled. The
31 new local headline axiom guards are repeated in the global audit and
allow only `propext`, `Classical.choice`, and `Quot.sound`.

From `formal/`, using the installed pinned Lean 4.35.0 toolchain:

```text
lake --no-cache build --wfail
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/CentralSpectralProjector.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/CentralDescentRecords.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesMeasuredReceiver.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/Audit.lean
```

Eight selected Python files: **130 tests passed in 10.08 seconds**, with
warnings fatal and external pytest plugins disabled. The modified file
alone has six cases and passed in 2.59 seconds. This is not the entire
repository Python suite. From the repository root:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-measured-receiver-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_central_quotient_receiver.py tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-measured-receiver-pycache /opt/anaconda3/bin/python -m py_compile tests/test_central_quotient_receiver.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-measured-receiver-pycache /opt/anaconda3/bin/python qsearch.py validate
git diff --check
```

Syntax, registry validation (`valid=true`, `issues=[]`) and whitespace
checks passed. No JavaScript changed and no JavaScript check is claimed.
No registry promotion, CLI/UI change, dependency installation, migration,
commit, push or external outreach occurred. Both agents were closed.

Changed code: the three new Lean files, default imports in
`formal/Formal.lean`, global guards in `formal/Formal/Audit.lean`, and two
new tests plus their bounded witness helper in the existing control file.
Documentation: this note, `formal/README.md`, `research/AGENT_HANDOFF.md`,
the current formal-status paragraph in `research/REES_HSP_REDUCTION.md`,
a follow-up pointer in `research/REES_CENTRAL_QUOTIENT_FORMALIZATION.md`,
and the external working checkpoint. Earlier dirty work is preserved.

Source SHA-256 values:

```text
2cdb6e1ea0e7589539ffd34f47f08c0ca230a8851e1428d8c12d4bd61de2bc3b  formal/Formal/CentralSpectralProjector.lean
5c222def81081004fbc07c3a07b5feb015381cdead01103121ab3bde4702cdc0  formal/Formal/CentralDescentRecords.lean
33e9e6b56c8532c7945692b9a2732c13cade35209b3b1f9b2a6bc66fb429a0ee  formal/Formal/ReesMeasuredReceiver.lean
ec5d4c8206a17286a72b751de29a02e139ea5f5e6a1994259397af4b1887d2cc  formal/Formal.lean
0e36b69b70c66696bb3144b19e69c748cb1df0c0fcfb6cc73146d2cd1d3de26a  formal/Formal/Audit.lean
17ba0b649b0eb0cf9a3f1ecc498d6765c729ac8877622b6dddeb28ec33fe4c0f  tests/test_central_quotient_receiver.py
```

## Remaining Obligations

This closes the complete central-measurement/source identification and
the displayed exact two-stage fresh-bank composition, conditional on valid
total SDE policies and the initial lifted coset supply. It does not prove:

* An executable bounded-time SDE policy, its parameter guarantee or abort
  probability, or formal extraction of its classical arithmetic.
* The full original-oracle preparation, terminal Fourier learning and
  probability-of-recovery theorem in one formal end-to-end development.
* Approximate gate synthesis, diamond-norm error hybrids, finite runtime
  caps, noise tolerance or resource bounds for an extracted circuit.
* General nilpotency-class or prime-power-ring BCH transport.
* A useful natural application, novelty, peer review or classical hardness.

The next scientific decision should compare a genuinely new native-source
mechanism with the remaining constructive solver and whole-algorithm
dependencies. Do not reprove character completeness, the physical branch
bridge, the inactive-target law or this two-stage identity as new progress.
No further finite group-size sweep is justified by these results alone.
