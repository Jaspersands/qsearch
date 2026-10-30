# Response To The Dilation-Source Review

2026-10-25. The SAME single authorized independent AI reviewer checked the
new source lemma. Its unmodified report is REVIEW.md. This is an additional
assignment to that reviewer, not a second reviewer or a human peer review.

## Finding And Correction

No fatal mathematical counterexample was found within the reconstructed
scope, relative to the explicitly imported ingredients. Finding F1 is a
valid resource qualification: a polynomial native-copy count does not imply
a gate bound independent of native register width and action complexity.

The reviewer's family is decisive. Fix p=131, dim L=1 and delta=1/2. For
arbitrarily large q=1 mod p, take the q-qubit GHZ state and the transversal
action diag(1,omega^t) on each qubit. Its nontrivial cyclic twirl has trace
distance 1/2, so the listed promise parameters stay fixed. A sufficiently
accurate implementation of the SUPPLIED controlled action must still act
on every native qubit. It costs Omega(q) in a bounded-arity gate model.
This refutes the overbroad gate-accounting interpretation, not the source
lemma or every possible algorithm on those inputs.

The revised proof states UNIFORM coherent SELECT(U), not mere pointwise
availability of classical-g circuits. With Q=B*k*M, it separately charges
Q native copies and Q SELECT calls. Per-query half-diamond error epsilon/(8Q)
costs at most epsilon/8 in the complete adaptive-channel hybrid. Total
action gates are Q*C_U(epsilon/(8Q)); acquisition, native width, arithmetic,
public sampling, moment design and receiver costs remain explicit. The
source amplification keeps its original epsilon/4 allocation, leaving
5epsilon/8 for the separately charged operations and receiver errors.

The integer planner now exposes that query count and error allocation,
sets total_gate_cost_certified=False, and lists unpriced resources. A new
test prevents promoting this copy/query plan into a full gate certificate.
It still cannot certify the robustness promise, design, or receiver cap.

## Frozen Review Target

reviewed_snapshot/ preserves the exact proof, three original Python files,
and original receipt. Archived Python files have .py.txt extensions to avoid
pytest collecting duplicate historical tests. Their bytes match all four
reviewed proof/code hashes in REVIEW.md. The archived receipt retains SHA256
9a6f31f65bafa3d9a4fc90e5917245819b2320cfff422f9b9727890c9b96a590.
The original report's line references refer to this frozen version, not
the revised live note. Nothing in the review was rewritten by the parent.

## Independent And Parent Checks

The reviewer separately constructed symbolic matrix/Jacobian controls and
an exact nonnormal Heisenberg source at p=131. The latter catches the wrong
kernel orientation (overlap 7/32 instead of 1) and shared-scale correlation
(1/131 instead of 1/17161 for two packets). It imports none of our proof
diagnostics and did not use the parent controls as evidence. The parent
reran its script successfully. These finite controls supplement, not prove,
the reconstructed general argument.

The parent's separate SOURCE_INDEPENDENCE.md derives a complete address
state counterexample to reusing one scale. The eight parent tests and new
resource-contract test are distinct from the reviewer's checks.

## Limits And Handoff

Keep the original pure-state, prime-field, class<=3, p>=131, fresh IID copy,
discarded-record and subgroup-robustness assumptions. The review imports
Weil, standard representation theory, Lazard and the older Rees receiver.
It supplies an independent sufficient scalar moment-design argument but
does not certify the older design implementation. It is not a formal proof,
end-to-end circuit, native physical-source validation, novelty assessment,
classical hardness result or useful application.

Gemini should retain these source/query/gate distinctions when integrating
after migration. No central registry, CLI, UI, staging or main-checkout edits
are authorized by this isolated handoff; integration awaits verified local
migration. See VERIFICATION.md for the current checked execution scope.
