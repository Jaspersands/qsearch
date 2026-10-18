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

## Rediscovery audit (`rediscovery.py`)

How many retained negatives restate barriers the literature already has? The registry
cites arXiv in only 2 of 976 records, so the audit searches for the barriers itself.

```bash
python tools/audit/rediscovery.py export --out DIR                   # 60 clusters in 6 judge batches
python tools/audit/rediscovery.py search 'abs:"hidden subgroup"' --who NAME   # judges search through this
python tools/audit/rediscovery.py import DIR/out/*.jsonl
python tools/audit/rediscovery.py spot-export --out FILE --n 30
python tools/audit/rediscovery.py import --spot-check REVIEW.jsonl
python tools/audit/rediscovery.py report
```

How it works:

- Negatives are clustered by their reasoning, with arXiv ids stripped first, into 60
  clusters.
- A judge reads up to 6 members per cluster, states the shared barrier in standard terms
  and searches arXiv. Searches are paced to one request every 3 seconds across processes,
  cached and logged in `rediscovery_queries.jsonl`.
- The judge labels the cluster published, adjacent, not-found or unclear, and can
  override the label for single members.
- A "published" label, for a cluster or for one member, needs a citation whose quote of
  at least 6 words appears verbatim in the cited abstract. Anything else is downgraded
  to unclear on import.
- Ten records that restate textbook barriers were fixed as ground truth before judging.

Measured on 2026-10-19 with 6 judges and 190 arXiv searches:

| Label | Records | Read by a judge | Inherited from the cluster |
|---|---|---|---|
| published | 309 (32%) | 138 | 171 |
| adjacent | 452 (46%) | 169 | 283 |
| not-found | 2 (0%) | 2 | 0 |
| unclear | 213 (22%) | 57 | 156 |

| Check | Result |
|---|---|
| Ground-truth records labelled published | 7 of 10 |
| Fresh reviewer agrees with the label, 30 random records | 27 of 30 (Wilson 95% interval 74% to 97%) |
| Reviewer agreement, records read by a judge | 11 of 12 |
| Reviewer agreement, inherited labels | 16 of 18 |

How to read it:

- Almost nothing came back not-found. The registry's barriers are mostly instances of
  published ones (32%) or known techniques in a new setting (46%). The highest published
  share is in coset observables / nonabelian HSP (48%) and code equivalence (37%). The
  lowest is in the dihedral coset track (7%), where most records are adjacent.
- Unclear is mostly templated records ("Falsified or refined by exact theorem
  evaluation") and mixed clusters.
- Labels are cluster-level. The reviewer found records whose own barrier differs from
  their cluster's, including one that was mis-clustered. Before citing a single record's
  label, check its row in `rediscovery_audit.json` and the review queue in the report.
- Three ground-truth misses (lossy boson sampling, Gaussian CV, QAOA locality) sit in a
  mixed cluster labelled unclear. One ground-truth hit, quantum-walk blindness on
  strongly regular graphs, carries its cluster's citation on symmetric-group Fourier
  sampling rather than the walk papers.
