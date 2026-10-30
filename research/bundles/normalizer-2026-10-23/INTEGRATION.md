# Research Handoff: Abelian-Action Normalizer

2026-10-23. This bundle is LOCAL and outside the actively migrating repository.
It is not a second repository checkout. No source or staging file was edited.

## Completed Work

- ABELIAN_ACTION_NORMALIZER.md: proposed bounded-index p-group HSP reduction.
  The general route now imports known all-prime normalizer algorithms with
  PAID quantum collection; the original large-prime arithmetic remains an
  independent transparent backend, not a new general normalizer discovery.
- abelian_action_normalizer.py: exact log/exp, joint augmentation-nilpotence
  certification, additive/bracket closure, saturated integer-congruence
  stabilizer, and native subgroup-preservation checks.
- test_abelian_action_normalizer.py:44 tests, including noncommutative groups,
  unequal/equal prime-power cyclic factors, changed basis, a nonnormal
  stabilizer, rejected non-p actions, classes4/8/12 and a127-bit prime.
- QUOTIENT_BRIDGE_AUDIT.md: original-group quotient coordinates, known
  normalizer interface, retained-input coherent compiler, exact distinction
  between fresh and arbitrary quantum targets, and physical falsifier.
- quotient_bridge_controls.py and test_quotient_bridge_controls.py:24 tests
  of full finite Fourier learning/normalization/quotient/pullback, oracle
  fibers, nonhomomorphic sections, coherent garbage cleanup and failure
  without a retained input. The fixture's numeric labels are classically
  easy; this is not a hard family or a scalable quantum implementation.
- replay.py and normalizer_receipt.json: public arithmetic and finite Fourier
  receipts, separate simulation/device/scalability flags, a symbolic
  coherent-compilation counterexample, and SHA256 source hashes.

Latest verification:68 tests PASS in13.83s; py_compile PASS for all five
Python files; updated live replay and source-hash/claim-scope checks PASS.
The class8, p11 action control leaves an
order1331 class2 semidirect quotient after a SUPPLIED intersection. The
mixed-module runs at p5 and p=2^127-1 compute action order p^3 and stabilizer
order p^2. The new class3, p7 finite simulation learns its intersections
from oracle labels and recovers all four conjugate control subgroups.
There is no black-box acquisition or scalable quantum HSP execution.

## Main-Model Review Still Needed

The quotient bridge has now received a local audit, NOT independent review.
Review the precise IMS nice-map and quotient interfaces and the Eick/Luks
normalizer import with quantum collection. No Eick/Luks implementation is
supplied. The compiler's arbitrary-target error is 2*sqrt(delta), not the
fresh-zero-target sqrt(2*delta). The no-retained-input counterexample has
orthogonal outputs on a balanced witness; uniform input alone mostly
shows a harmless global phase and is not an adequate physical witness.

Do not expand the matrix backend or run more size sweeps. The next valuable
work is an independent interface/proof audit or a useful native source.
The all-prime terminal parameter dependence has not been audited to an FPT
bound. No novelty claim follows from a search that found no exact match.

For fixed k>2 the terminal solver depends on the repository's still-unreviewed
Rees theorem. For k<=2 published nil-2 HSP suffices, but that does NOT remove
the new reduction's own proof-review obligation. No natural hard source or
speedup is established. Do not admit a candidate from these finite controls.

The inverse-trace and isogeny triage in this pass produced no new solver or
native source. Existing classical attacks retain their original scopes.

## Mechanical Integration After Migration Verification

First verify that the copy has completed, the new repository is readable,
and its authoritative path is established. A running ditto process, a staging
directory, or a successful download request is NOT verification. Do not stop
or modify the migration worker from this handoff.

Then integrate these specific files, preserving any intervening edits:

1. Move the public module into theorems/abelian_action_normalizer.py.
2. Put both tests in tests/. Move quotient_bridge_controls.py into an
   explicitly bounded research-control location, not the candidate factory.
   Adjust imports without weakening or promoting the controls.
3. Put both proof/audit notes in research/. Update local replay paths to
   final locations without upgrading claim status.
4. Integrate replay.py as a small standalone research replay using the
   new module path. Write its receipt to research/reductions/ rather than
   the central candidate registry. Update source-hash paths and regenerate.
5. Add a concise dated entry at the top of RESEARCH_PRIORITY_DECISION.md,
   AGENT_HANDOFF.md and MECHANICAL_FOLLOW_UP_PLAN.md. State the exact scope,
   validation, independent-review status and missing native application.
6. Run these68 tests plus the existing bounded-codimension and connected
   Rees algebra suites, syntax checks and the appropriate repository
   validation. Report actual counts; no full-repository pass was run here.

No qsearch.py/UI expansion, central candidate admission, commits, pushes,
new agents, or automated campaign is requested by this handoff. Gemini can
perform the mechanical integration once the copy is verified. Main-model
effort should remain on proof scrutiny and useful source reductions.

## Replay Now

From this standalone directory:

    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile abelian_action_normalizer.py test_abelian_action_normalizer.py quotient_bridge_controls.py test_quotient_bridge_controls.py replay.py

Full-repository tests and qsearch.py validation were NOT run during migration.
No migration worker was started, stopped or modified by this pass.
