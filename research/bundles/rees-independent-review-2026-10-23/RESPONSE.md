# Response To The Independent Rees Review

2026-10-23. The explicitly authorized reviewer completed a fresh-context
adversarial mathematical review. Its unmodified report is REVIEW.md.

## Finding And Disposition

The reviewer found no fatal counterexample or unresolved core proof
obligation within its checked scope, relative to the stated imported
theorems. It identified one repairable parameter-convention problem:
the variable-class corollary used c<=r+1 although the input c could be a
loose upper bound. This is a real cost issue, not just terminology.

The parent checked the cited manuscript passages and accepted the finding.
For Heisenberg(F_p), r=1 and actual class=2, while a supplied c=p-1 is
permitted by c<p. Literal use of c evaluations per lifted input destroys
the claimed uniform dependence on log p when r is fixed.

The corrected copy rees_hsp_review_revised.tex changes only the introduction
to the derived-dimension section. It explicitly computes the actual class
by public lower-central linear algebra BEFORE building the cover or any
source bank. This uses at most n strict decreases and no hidden-source
calls. All evaluation counts, BCH truncations and copy counts then use the
actual class. The zero algebra is handled directly. The original source/
snapshot and the reviewer's report remain unchanged.

The correction is the reviewer's proposed local repair, checked and applied
by the parent. The reviewer was closed after completing its assignment and
did not independently review this exact revised file. No additional reviewer
was spawned.

## Parent Verification

- Reran the independent exact_controls.py successfully. Both exact
  cyclotomic controls reproduce the reported counts, including all 27
  positive label triples and all 234 valid scale witnesses in EACH control.
- The independent control code passes py_compile.
- Diff against the frozen source confirms a single localized manuscript
  change in the variable-class section.
- The revised manuscript compiled successfully with the desktop LaTeX
  compiler. Compilation is not mathematical verification.

## Status And Integration

Status: proposed theorem with ONE completed independent AI adversarial
review and one local correction. This is not a peer-reviewed, formally
verified, novel, practical, or naturally applicable quantum algorithm.
The report's unverified imported internals and implementation scope remain.
Do not describe the entire research program as independently validated.

After migration is fully verified, Gemini should port only the localized
normalization paragraph into the live manuscript and record the exact
reviewed-source hashes and correction. Check any resource-planning code
that accepts a class upper bound: it must compute the actual class or charge
the supplied bound honestly; unused zero grades alone do not justify
dropping charged evaluations. Keep review status separate from proof and
novelty status. Run repository validation after integration.

The orthogonal proposal and its new classical bounds were NOT part of
this review. They still lack independent review.
