# Audits of the research record

Read-only audits over `research/registry/`. They never write to the registry; outputs go
to `research/audits/`. Judging is done by in-session subagents. The tools export batches
for the subagents, then import and check what comes back. The stored judgements make
every report rebuildable without re-judging.

## Failure-mode meta-analysis (`failure_modes.py`)

Where do proposals die? Each retained negative gets one primary failure mode: classical
competitor, no signal, readout, state preparation, resource blow-up, finite-size
evidence, proof gap, hidden advice or oracle, overbroad claim, or unclear.

```bash
python tools/audit/failure_modes.py                                   # rebuild the report
python tools/audit/failure_modes.py --export-batches DIR --batches 8  # judge inputs
python tools/audit/failure_modes.py --import DIR/out/*.jsonl --judge NAME
python tools/audit/failure_modes.py --import DIR/second/*.jsonl --judge NAME --second-opinion
```

- Records that share their reasoning are judged once: 976 records form 685 groups.
- A keyword rule pass labels every record. Judge labels override the rule labels, and
  records without one fall back to the rules (for example, records added since the last
  judging).
- `failure_mode_judgements.json` holds the judge labels, a verbatim quote for each, and a
  second, independent judge's labels on a random sample of 150 groups.
- The trend table dates each record by its first appearance in the registry's git history.

Measured on 2026-10-19:

| Check | Result |
|---|---|
| Second judge vs first judge, 214 records | 89% same primary mode, kappa 0.86 |
| Keyword rules vs judges, 976 records | 49% same primary mode, kappa 0.40 |
| Rules on classical competitor | 87% precision, 85% recall |
| Rules on hidden advice or oracle | 85% precision, 89% recall |

The rules fell short of the 85% target, so every reported label comes from the judges.
Trust the rules alone only for the two modes in the table.
