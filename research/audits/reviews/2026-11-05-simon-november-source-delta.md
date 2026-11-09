# Simon DCP November Source Delta

2026-11-05. Bounded independent source comparison for literature triage.
This is not a new DCP simulation, formal verification, or global no-go.

## Provenance and scope

The parent researcher reports that the official
[2026/1591 metadata](https://eprint.iacr.org/2026/1591) lists a November 3
revision, seventh of seven, described as clarity edits and reformatting;
official PDF/archive requests returned HTTP 403. The parent supplied a
PDF fetched with `curl` from the public
[mirror endpoint](https://eprint.iacr.asia/2026/1591.pdf). This reviewer made
no network, Git, service, or archive requests.

Independently inspected local sources:

- October official-source PDF:
  `research/literature_cache/eprint_2026_1591_20261008.pdf`, SHA256
  `5e827802a7cd2351ce8561f4fbd55b44df2c79aae12fa6b176bcd85eda6714ed`.
  Its text extraction is `eprint_2026_1591_20261008.txt`, SHA256
  `3491270aadc1ccc6d232e5ef563870cd7690948bf893170ff79b566f615418ca`.
  The prior audit records official retrieval and the October 8 archive
  date; the document itself says October 7 and has 18 pages.
- November mirror PDF:
  `research/literature_cache/eprint_2026_1591_20261103_mirror.pdf`, SHA256
  `7cbaba8ea7a2518dd6953b2e5e4c4c47da2e06c4d60f9f3bd722fd3eb31bffda`.
  Its text extraction is `eprint_2026_1591_20261103_mirror.txt`, SHA256
  `ef273e0b8f7708bb907779046a6054a601601555f670b7083c0147a45c688d46`.
  `pdfinfo` confirms 13 pages and creation November 3, 17:48:42 UTC;
  the internal publication date is November 2026. It uses an ACM template
  with placeholder DOI, which is not evidence of ACM publication.

The official metadata and access results above are parent-supplied, not
independently rechecked here. Official/mirror byte identity is UNKNOWN.
The operational verdict below applies to the actual retrieved mirror
document, whose bytes are pinned above. Unicode mathematical alphabets,
equation placement, hyphenation, and pagination prevent treating a raw
text difference as an algorithm change; no byte/text identity is claimed.

## Operational comparison

Manual comparison of October Section 2.2 (pp. 6–15) with the November
mirror Section 2.2 (pp. 4–10) finds the same specified operations:

| Step | Operation in both documents |
|---|---|
| 1 | Collect `Q=k*n^(c+1)` samples, Fourier transform their value registers, retain the Fourier labels `Y`. |
| 2 | Compute the exact full-label subset sum and measure its low `n-1` bits. |
| 3 | Use fixed width-`c log n` groups; compute each subset sum's top `log n` bits. |
| 4 | Hadamard and measure the sample bits, measure `Y`, and select the first `n/log n` all-zero groups as `A`. |
| 5 | Measure the group summaries in `B`; the displayed signed completion sums describe amplitudes rather than an extra label query or signed-count oracle. |
| 6 | Add summaries modulo `n`, erase one, compute the carry guard, and retain the specified zero-guard/zero-Hadamard-summary branches. |
| 7 | Compute/measure `h'=h XOR h*`, then erase `h`. |

Both conclusions then Hadamard and measure `h*` and propose polynomially
many repetitions. No additional low-label-sensitive computation, access
to a new Fourier label function, uncomputation from full labels, or
full-label feedforward is specified. Full labels are still used exactly
in Step 2 and only through coarse summaries in Step 3. The analytical
full-label fiber definitions after Step 4 are present in both versions;
they do not specify new physical computation.

## What changed in the response

November adds a Section 2.2 note referring to Guo–Yang,
[ePrint 2026/1714](https://eprint.iacr.org/2026/1714), for more formal
proofs. That external paper was not supplied or audited in this bounded
task; the citation does not itself validate any lemma. The November
Lemma 3 still asserts the selection-conditioned pairwise-independence
and moment step criticized in the October audit, and still prints a
`2^n` amplitude threshold while its proof uses `2^(n/2)`.

Section 3 (October pp. 15–17; November pp. 10–12) is substantively
rewritten. It now explicitly conditions the information-loss comparison
on averaging the untouched label portions, describes amplification of a
rare conditional difference, expands the preselected-`A` examples, and
argues that exponentially many candidate sets rescue total success.
These are changes to the explanation, not a specified new circuit or
full-label-dependent operation. The examples with preselected `A` and
unmeasured `B` already had counterparts in October.

There is an internal selection-description mismatch worth preserving:
November Section 3 describes `A` as chosen randomly among all-zero
groups, whereas its operational Step 4 still chooses the first qualifying
groups. Equality of those transcript laws is not established here. Either
selection rule depends only on the measured zero pattern, so the mismatch
does not supply a new full-label operation or evade the October audit's
uniform-summary-table transfer. A claimed conditional advantage must
still be charged with its acceptance probability in one common instrument;
counting many possible sets does not independently multiply that budget.

## Bounded disposition

For the inspected mirror document, no operational revision triggering DCP
re-entry was found. The existing October transfer argument remains
applicable under its stated ideal-source, fixed-group, label-access and
Born-weighted-instrument premises. This is a source-delta conclusion,
not a new independent proof of that transfer or a verdict on arbitrary
DCP algorithms. Direct official-November byte authentication remains
UNKNOWN; no novelty, speedup, solver, registry promotion, or new quantum
execution claim follows.

Next action only if needed for provenance: obtain the official November
PDF and compare its SHA256 and Sections 2.2–3 against the pinned mirror.
Acceptance requires the same operations or a precisely identified changed
operation; a new date, proof citation, or raw Unicode text diff is
insufficient. No new DCP implementation or simulation is requested.
