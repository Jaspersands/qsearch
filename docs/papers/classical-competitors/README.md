# Classical competitors and local measurements (draft preprint)

A draft, not for circulation. It covers three results:

- **A.** A classical competitor for explicit prime-character OPI.
- **B.** Local readout of multi-packet DCP phase packets, against certified PPT bounds.
- **C.** A classical sampler for the uniform-sign polar Gibbs source.

It also summarizes the rediscovery audit of the negative-results registry.

## Build

```bash
python docs/papers/classical-competitors/make_numbers.py --check
latexmk -pdf -cd -outdir=/tmp/paper docs/papers/classical-competitors/main.tex
```

- `make_numbers.py` writes `numbers.tex` from `numbers_map.json`. Each macro names a
  committed JSON report, a path into it, and optionally an exact conversion:
  - `up:N` or `down:N` rounds a decimal in a fixed direction, so an upper bound is never
    printed too low and an achieved score or lower bound never too high.
  - `bits` gives a bit length, and `bits_ge` the least bit length at which every integer
    reaches the value (a sufficient field size).
  - `pi` gives an angle as a fraction of π.
  - `sci` gives scientific notation; `sci:up` and `sci:down` round it in a fixed direction.
- A path that no longer resolves stops `make_numbers.py`. The one exception is an entry
  with `"absent"`: when only its last key is missing (the audit report omits zero counts),
  it prints that text, a dash.
- A value that changes does not stop the build by itself. `numbers.tex` stays stale until
  `make_numbers.py` is rerun, and `tests/tools/test_paper_numbers.py` fails while the
  committed `numbers.tex` differs from what the script would generate. The same test fails
  if `main.tex` uses a command that is neither a generated number nor a known command.
- `--check` also lists any LaTeX command that is neither a generated number nor a known
  command.

Keep build output out of this directory. The `-outdir` flag above does that.

## Reproduce

```bash
docs/papers/classical-competitors/reproduce.sh OUT
```

This reruns the eight prime-character and polar modules of `qsearch-classical` and the
DCP circuit search into `OUT`, then compares each macro with its committed value. It does
not run the two Jacobi modules, which no number in the paper uses. It runs the vendored
source from the checkout (it puts `packages/qsearch_classical/src` on `PYTHONPATH`), so
`pip install -e packages/qsearch_classical` is not needed and is not what it tests. It
needs python-flint, sympy, numpy, scipy and cvxpy, and stops at once if one is missing;
the package's own dependencies are only the first three.

A run on 2026-10-19, after the revision check, took 690 s. It matched 183 numbers
exactly, with 0 differences. The other 55 came from the bridge note and the two audits,
which the script does not regenerate. The second referee pass then added and re-rounded
macros without rerunning the script: formatted from the reports that run regenerated,
all 192 regenerated macros match the committed values, with 0 differences, and the other
76 come from the bridge note and the two audits.

## Review history

- **Draft.** Written by a drafting subagent from the source notes. Every scope sentence
  is quoted verbatim.
- **Referee pass, 2026-10-19.** A fresh referee checked all 205 numbers against the
  reports, confirmed all 23 references, and raised 7 must-fix, 14 should-fix and 15 minor
  issues. The must-fix issues were:
  - an omitted conditioning on the syndrome in Result C;
  - "PPT bound equals collective" read as attainment;
  - the fixed-input guarantee in Result A stated more broadly than the notes allow;
  - a wrong reason for the zero bounds in the original field;
  - a mis-scoped "best classical witness";
  - a false "highest share" sentence about the audit.

  All 7 must-fix and 14 should-fix items were addressed, and every minor issue except
  one.
- **Revision check, 2026-10-19.** A second fresh reviewer checked the revision against
  the report. One must-fix sentence was still too strong ("only above" a threshold), and
  one new citation needed another clause. The reviewer also found nine new problems,
  none serious:
  - the Korada–Urbanke lemma covers only the joint-law step of the hybrid bound;
  - two sentences ignored the N = 15 controls, which do have positive bounds;
  - three Result B bounds were rounded the wrong way;
  - smaller items: the conventions paragraph, solver tolerance, the r = 4 prime, an
    implicit angle formula, comma spacing in math mode, and three bibliography details.

  All were addressed, and the outreach drafts were brought in line. The Result B
  rounding, however, was only disclosed (the table caption said values were rounded to
  nearest), not fixed; the second referee pass fixed it.
- **Second referee pass, 2026-10-19.** A fresh referee found these, all now fixed:
  - Result A claimed perfect witnesses on every saved high-rate input; the N = 31,
    K = 16 mixed seed-71 input stops at 30 of 31. The claim now covers the N = 127,
    K = 77 inputs, and Limitations lists the N = 31 input.
  - Result B printed achieved scores and bounds rounded to nearest. Every Result B number
    is now directed: achieved scores, collective values and certified gaps down; PPT
    bounds and open windows up.
  - The sufficient field sizes in Result A were the thresholds' bit lengths (169 and 756
    bits); a prime of that length can lie below its threshold. The text now states
    p ≥ threshold and gives 170 and 757 bits as sufficient.
  - The polar certificate was presented as unconditional. It now names the two
    review-pending derivations it rests on: the magnitude-to-pure-state-channel
    correspondence and the degradation argument.
  - "Lemma 2" of Korada and Urbanke appears in no source note and was dropped; the paper
    is still cited. Virmani et al.'s pages are now 62–68.
  - The Reproducibility section said a regenerated report cannot leave a stale number in
    the text. It now says what is true: a missing path stops the script, and the numbers
    test fails while `numbers.tex` is stale.
  - The audit section was updated to the regenerated reports: the propagation guard and
    withheld records, the published count among records a judge read, the spot check
    restricted to labels unchanged since review, a ground-truth caveat, and the
    failure-mode second opinion described as one model's repeatability over sampled
    groups.
  - This README said `reproduce.sh` reruns every package module; it skips the two Jacobi
    modules. `reproduce.sh` now stops if a dependency is missing.
