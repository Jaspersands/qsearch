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
- `failure_mode_judgements.json` holds the judge labels, one verbatim quote per judged
  group (records in a group share it), and a second judge's labels on a random sample of
  150 groups. The second judge was the same model in a fresh context, so the agreement
  below measures how repeatable one model's labels are, not agreement between experts.
- The trend table dates each record by its first appearance in the registry's git history.

Measured on 2026-10-19:

| Check | Result |
|---|---|
| Second judge vs first judge, 150 groups (214 records) | 84% same primary mode (91% counting a secondary mode), kappa 0.81 |
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
- Labels spread from the members a judge read to the rest of the cluster only under a
  guard. An unread member inherits the cluster label only if at least half of the read
  members kept that label (no member override), and one of those members is on the same
  research track. Otherwise its label is withheld and counted as unclear.

Measured on 2026-10-19 with 6 judges and 190 arXiv searches:

| Label | Records | Read by a judge | Inherited from the cluster | Withheld |
|---|---|---|---|---|
| published | 275 (28%) | 138 | 137 | – |
| adjacent | 436 (45%) | 169 | 267 | – |
| not-found | 2 (0%) | 2 | 0 | – |
| unclear | 263 (27%) | 57 | 137 | 69 |

Of the 366 records a judge read, 138 (38%) are published. Of the 713 records with a label
other than unclear, 39% are published.

| Check | Result |
|---|---|
| Ground-truth records labelled published | 7 of 10 (see the caveat below) |
| Fresh reviewer agrees with the label, 27 random records whose label is unchanged since review | 25 of 27 (Wilson 95% interval 77% to 98%) |
| Reviewer agreement, records read by a judge | 11 of 12 |
| Reviewer agreement, inherited labels | 14 of 15 |

The reviewer sampled 30 records before the guard existed. The guard has since withheld the
inherited labels of 3 of them; the reviewer had agreed with 2 of those 3 labels.

How to read it:

- Almost nothing came back not-found. The registry's barriers are mostly instances of
  published ones (28%) or known techniques in a new setting (45%). Among the three
  largest tracks, the published share is highest in coset observables / nonabelian HSP
  (111 of 255, 44%; 48 of 90 read records) and code equivalence (157 of 457, 34%; 83 of
  185 read), and lowest in the dihedral coset track (1 of 154), where most records are
  adjacent. The small applied-QC track, barriers taken from the literature, has 4 of 10
  published.
- Earlier versions of this audit reported 309 published (32%). That figure let every
  unread member inherit its cluster's label, including members of clusters where the
  judge had overridden most of the members it read. The guard above removed 34 published
  labels that rested only on inheritance.
- Unclear is mostly templated records ("Falsified or refined by exact theorem
  evaluation"), mixed clusters and withheld labels.
- Labels are cluster-level. The reviewer found records whose own barrier differs from
  their cluster's, including one that was mis-clustered. Before citing a single record's
  label, check its row in `rediscovery_audit.json` (its `basis` says whether a judge read
  it) and the review queue in the report.
- **The ground-truth check is weaker than it looks.** The judge instructions used the
  barren-plateau topic for their example query and example citation (arXiv 1803.11173,
  McClean et al.). Only arXiv ids were stripped from the records, so author-year
  references such as "McClean et al. (2018)" stayed visible to the judges. Four of the
  seven hits are single-record overrides inside one mixed cluster (C14), barren plateaus
  among them. Read 7 of 10 as a check that the pipeline can find a known barrier
  when pointed at it, not as a recall estimate.
- Three ground-truth misses (lossy boson sampling, Gaussian CV, QAOA locality) sit in a
  mixed cluster labelled unclear. One ground-truth hit, quantum-walk blindness on
  strongly regular graphs, carries its cluster's citation on symmetric-group Fourier
  sampling rather than the walk papers.
