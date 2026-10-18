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
    printed too low.
  - `bits` gives a bit length.
  - `pi` gives an angle as a fraction of π.
  - `sci` gives scientific notation.
- A path that no longer resolves stops the build.
- `--check` also lists any LaTeX command that is neither a generated number nor a known
  command.
- `tests/tools/test_paper_numbers.py` checks that the committed `numbers.tex` matches
  the reports.

Keep build output out of this directory. The `-outdir` flag above does that.

## Reproduce

```bash
docs/papers/classical-competitors/reproduce.sh OUT
```

This reruns every `qsearch-classical` module and the DCP circuit search into `OUT`, then
compares each macro with its committed value. A run on 2026-10-19, after the revision
check, took 690 s. It matched 183 numbers exactly, with 0 differences. The other 55
come from the bridge note and the two audits, which the script does not regenerate.

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

  All were fixed, and the outreach drafts were brought in line.
