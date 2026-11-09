# Oscillator pairing and mechanism triage review

2026-11-06. Narrow review sized to the scoped linear-algebra claim.

Parent checked actual2509.14443v2 Section6.3 universal pairing premise,
Claim44 and decoder discussion, and Section6.4's speculative scope. Parent
also checked Jo's actual fixed-padding theorem and the local native-source
composition; no list-decoding mechanism is new here. The character source
Theorem6/POVM and full-field classical distinction were reread in the saved
primary texts. No quantum execution or separation is claimed.

Independent helper growing_degree_mechanism accepted the exact proof from
the supplied source premise: pi=Mz, sigma=M^T y; square permutations have a
complete classical maximum and uniform-shell sampler. Parent reproduced
its algebra and incorporated these qualifications:

1. Basis queries recover M only UNDER THE PROMISE, not a circuit-identity
   test. Native classical evaluator cost is charged.
2. A y-dependent global phase permits pi(z)=Mz+b. Substituting z=0 proves
   this affine-only form; m+1 evaluations still pay the classical solver.
3. The result matches a classical output/position distribution, not a
   coherent quantum state. Rectangular Max-LINSAT remains outside it.

Independent direction-selection helper found no new paid decoder in its
bounded code-equivalence/isogeny comparison. Its observations are selection
decisions, not general simulations or hardness results. No external-source
claim was promoted solely from its response.

One Sage run of audits/controls/oscillator_pairing/exact_control.py passed:
invertible3-by-3 source recovered from basis queries, maximum score3,
all64 pairings exact; Toffoli permutation gave0 !=1. General proof is in
the note, not inferred from that control. No larger test is needed.

Claude run2026-11-06-character-factorial-opus is terminal empty_response /
refusal, zero report bytes, input12913/output612, estimated$0.063892.
No findings or review acceptance; no retry. Artifacts retained.

Milestone checks passed: matching STATE/handoff/queue title, retained note,
review, prompt and exact-control artifacts, JSON assertions, refusal/usage
metadata and whitespace. Scoped git diff --check also passed. No broad suite
was run; no repository runtime or API-runner code changed.
