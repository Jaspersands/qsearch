# Unsent Expert-Review Request

Draft shown to the user on 27 October 2026. No recipient is selected.
The user requested a preview, not sending, posting or submission.
This file does not authorize any external action.

Subject: Request for correctness and prior-art assessment: fixed-class nilpotent HSP

Dear [Name],

I'm working on an AI-assisted quantum algorithms research project. We have
a proof draft that may extend known polynomial-time hidden-subgroup
algorithms, and I'm seeking an expert assessment before making any novelty
claim.

The core proposed result is a bounded-error algorithm for arbitrary hidden
subgroups of an explicitly presented nilpotent Lie/BCH group over F_p,
with fixed class c<p. Its claimed running time is polynomial in the
dimension and log p, allowing both to grow.

The mechanism constructs a positive lower-central Rees cover. Multiple
evaluations of the original hiding oracle make the lifted hidden subgroup
invariant under public dilations. Central-character cancellation then uses
the existing Ivanyos--Santha diagonal-system algorithm, eventually recovering
the entire original hidden Lie subalgebra.

The proposed contribution is this composition, not the diagonal solver or
central-state conversion themselves.

Could you help assess:
1. Whether the homogenization and recursive state-conversion argument has
   a mathematical flaw.
2. Whether an existing result already covers this precise growing-prime
   regime.
3. Whether the result, if correct and additional, warrants further development.

The work was developed with AI assistance and has received automated
adversarial review, but no human specialist validation. Finite computational
checks are supplementary, not evidence of the general theorem. No practical
advantage or cryptanalytic application is claimed.

I've attached the proof draft. Even a specific counterexample, prior-art
pointer, or referral would be valuable.

Best,
[Your name]

## Attachment Preparation

The intended mathematical attachment is `rees_hsp_review.tex`, with a PDF
alongside the source if successfully exported and checked. Compilation is
not a correctness certificate. Do not claim a PDF is attached unless one
actually exists in the eventual message. The brief and archived review
reports are supplementary reading, not a request to send the repository.
Primary diagonal-system reference: https://arxiv.org/html/1503.09016v2.
