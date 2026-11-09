# Rees cloud harvest: dfs2_k89_1102

- Session: `session_01B1JoCg16BhN1KPQkX1ez3V` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-02 10:27 UTC; final message: 2026-11-02 20:09 UTC (last event 20:39)
- Asked: Rees cloud: dfs2 exceptional-prime scans κ=8 (from 4058) and κ=9 (from 5690), κ=7 sanity checks; plain dfs2 (no symmetry pruning) with a 50M node limit.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 69.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 0 distinct primes, 0 bad.
- Against `k8dec.txt` / `k9dec.txt`: 68 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=7 p=3221 nodes=16430862
INFEASIBLE k=8 p=4049 nodes=5267869
INFEASIBLE k=8 p=4057 nodes=5273471
INFEASIBLE k=8 p=4073 nodes=5682924
INFEASIBLE k=8 p=4129 nodes=6082404
INFEASIBLE k=8 p=4153 nodes=6136216
INFEASIBLE k=8 p=4201 nodes=6620653
INFEASIBLE k=8 p=4217 nodes=6706519
INFEASIBLE k=8 p=4273 nodes=8126623
INFEASIBLE k=8 p=4337 nodes=8141793
INFEASIBLE k=8 p=4409 nodes=8371907
INFEASIBLE k=8 p=4457 nodes=9612340
INFEASIBLE k=8 p=4561 nodes=11994875
LIMIT k=8 p=4649 DONE k=8 range=[4649,4649] feasible=0 infeasible=0 limit=1  34.567246242 s
INFEASIBLE k=8 p=4649 nodes=13593816
INFEASIBLE k=8 p=4721 nodes=15564908
INFEASIBLE k=8 p=4793 nodes=17517831
INFEASIBLE k=8 p=4801 nodes=15779143
INFEASIBLE k=8 p=4889 nodes=18553504
LIMIT k=8 p=5009 DONE k=8 range=[5009,5009] feasible=0 infeasible=0 limit=1  38.865756042 s
INFEASIBLE k=8 p=5209 nodes=27765762
INFEASIBLE k=8 p=5393 nodes=34756987
INFEASIBLE k=8 p=5417 nodes=36898232
INFEASIBLE k=8 p=5441 nodes=35721950
LIMIT k=8 p=5521 DONE k=8 range=[5521,5521] feasible=0 infeasible=0 limit=1  46.901990828 s
INFEASIBLE k=9 p=5743 nodes=3729359
INFEASIBLE k=9 p=5779 nodes=3910175
INFEASIBLE k=9 p=5851 nodes=4896658
INFEASIBLE k=9 p=5869 nodes=4757491
INFEASIBLE k=9 p=5923 nodes=4742199
INFEASIBLE k=9 p=6067 nodes=6407153
LIMIT k=8 p=6073 DONE k=8 range=[6073,6073] feasible=0 infeasible=0 limit=1  56.848995442 s
INFEASIBLE k=9 p=6121 nodes=5739504
INFEASIBLE k=9 p=6211 nodes=6670060
INFEASIBLE k=9 p=6229 nodes=7322040
INFEASIBLE k=9 p=6247 nodes=7138954
INFEASIBLE k=9 p=6661 nodes=11515163
INFEASIBLE k=9 p=6733 nodes=13081875
INFEASIBLE k=9 p=6949 nodes=14198964
LIMIT k=8 p=8009 DONE k=8 range=[8009,8009] feasible=0 infeasible=0 limit=1  104.044755692 s
LIMIT k=8 p=12041 DONE k=8 range=[12041,12041] feasible=0 infeasible=0 limit=1  240.699040450 s
```

## Result messages (all 53, verbatim; the session never wrote a final report)

--- result 1 (2026-11-02T10:49Z)
The monitor is armed. I'm waiting for events.
--- result 2 (2026-11-02T10:49Z)
Event recorded: κ=8, p=4073 is INFEASIBLE with 5,682,924 nodes. The local run had reported LIMIT for 4073; it now completes. Still waiting.
--- result 3 (2026-11-02T10:50Z)
Event recorded: κ=8, p=4201 is INFEASIBLE with 6,620,653 nodes. Still waiting.
--- result 4 (2026-11-02T10:53Z)
Event recorded: κ=8, p=4273 is INFEASIBLE with 8,126,623 nodes. That is a new exceptional prime beyond 4057. Still waiting.
--- result 5 (2026-11-02T10:54Z)
Event recorded: κ=8, p=4409 is INFEASIBLE with 8,371,907 nodes. The exceptional set keeps extending past 4057, and each INFEASIBLE prime costs roughly 10–15 CPU-minutes. Still waiting.
--- result 6 (2026-11-02T10:58Z)
Event recorded: κ=8, p=4129 is INFEASIBLE with 6,082,404 nodes. The local run had reported LIMIT for 4129. Still waiting.
--- result 7 (2026-11-02T11:01Z)
Event recorded: κ=8, p=4217 is INFEASIBLE with 6,706,519 nodes. Still waiting.
--- result 8 (2026-11-02T11:03Z)
Six κ=8 primes are INFEASIBLE so far: 4073, 4129, 4201, 4217, 4273 and 4409. No chunk has finished yet after 25 minutes, so this will take a while. Still waiting.
--- result 9 (2026-11-02T11:06Z)
Event recorded: κ=8, p=4289 is INFEASIBLE with 8,015,020 nodes. Still waiting.
--- result 10 (2026-11-02T11:07Z)
Event recorded: κ=8, p=4153 is INFEASIBLE with 6,136,216 nodes. The local run had reported LIMIT for 4153. Still waiting.
--- result 11 (2026-11-02T11:11Z)
The first chunk finished: `DONE k=8 range=[4058,4157] feasible=0 infeasible=3 limit=0`. Every κ=8 prime ≡ 1 mod 8 from 4073 to 4441 has come back INFEASIBLE so far. The full job covers 424 primes for κ=8 and 250 for κ=9. If most turn out INFEASIBLE or LIMIT, the run will be very long. I'll keep it running and judge the rate once later chunks report.
--- result 12 (2026-11-02T11:12Z)
Event recorded: κ=8, p=4241 is INFEASIBLE with 6,838,330 nodes. Still waiting.
--- result 13 (2026-11-02T11:19Z)
I re-armed the monitor. It now also reports chunk DONE lines.
--- result 14 (2026-11-02T11:20Z)
Event recorded: κ=8, p=4297 is INFEASIBLE with 8,089,839 nodes. Still waiting.
--- result 15 (2026-11-02T11:37Z)
Here's where things stand. Every κ=8 prime from 4073 to 4481 has come back INFEASIBLE, so E_2(8) does not end at 4057. Short probes with a 300k-node limit at 4649, 5009, 5521, 6073, 8009 and 12041 found no witness. Per-node cost rises steeply with p: about 1.2k nodes/s at p=12041, against 11k/s at p=4049. At that rate a single 50M-node run near p=12000 takes about 11 hours, and the full job as specified would take months on 4 cores.

So I reorganised the queue so it gives the most useful partial answer. The κ=7 sanity checks run first. After them, κ=8 (from 4858) and κ=9 (from 5690) chunks alternate in ascending order, so each κ extends a contiguous checked range. The 4 κ=8 chunks already running keep going, and the new queue ramps up to 4 cores as they finish. The run will stop at a fixed time budget, and I'll report exactly which ranges were covered.
--- result 16 (2026-11-02T11:50Z)
Chunk done: `DONE k=8 range=[4458,4557] feasible=0 infeasible=2 limit=0`. Still waiting.
--- result 17 (2026-11-02T11:55Z)
All three sanity checks pass:
- `./dfs2 7 3221 3221 100000000` printed `INFEASIBLE k=7 p=3221 nodes=16430862`, taking 1093 s.
- `./dfs2 7 3229 3500 100000000` printed no INFEASIBLE line. All 4 primes in the range (3319, 3347, 3361, 3389) are FEASIBLE, and the DONE line reads `feasible=4 infeasible=0 limit=0`.
- κ=8 4049 and 4057 were already confirmed INFEASIBLE earlier.

The ramp-up is behaving correctly: 3 old κ=8 chunks plus the first κ=9 chunk keep all 4 cores busy.
--- result 18 (2026-11-02T12:05Z)
This is the first FEASIBLE κ=8 prime above 4057: p=4657, with a witness re-checked internally. In the same chunk, 4561 (11,994,875 nodes) and 4649 (13,593,816 nodes) are INFEASIBLE. Continuing.
--- result 19 (2026-11-02T12:07Z)
I re-armed the monitor and am waiting on the next chunks.
--- result 20 (2026-11-02T12:14Z)
κ=9 chunk done: 5743 is INFEASIBLE (3,729,359 nodes), which confirms the earlier finding, and 5779 is a new INFEASIBLE prime (3,910,175 nodes). Continuing.
--- result 21 (2026-11-02T12:37Z)
Progress at 12:37 UTC, two hours in:
- **κ=8:** contiguous coverage is complete through 4657. INFEASIBLE primes found further up include 4721 (15.6M nodes) and 4793 (17.5M nodes).
- **κ=9:** contiguous coverage is complete through 5789. 5851 is INFEASIBLE (4.9M nodes).

The number of nodes per prime is rising quickly, so I expect κ=8 runs to start hitting the 50M limit somewhere around p≈5300. Continuing.
--- result 22 (2026-11-02T12:41Z)
Chunk done: `DONE k=9 range=[5790,5889] feasible=0 infeasible=2 limit=0`. Continuing.
--- result 23 (2026-11-02T12:57Z)
Chunk done: `DONE k=8 range=[4658,4757] feasible=0 infeasible=3 limit=0`. Continuing.
--- result 24 (2026-11-02T13:08Z)
My ramp-up script had a bug: its pattern also matched one of the new chunks. One core sat idle from about 12:40 to 13:08 UTC. I fixed it by hand and all 4 cores are busy again. The idle time cost wall time only; no results were affected.
--- result 25 (2026-11-02T13:21Z)
Chunks done:
- `DONE k=8 range=[4758,4857] feasible=0 infeasible=3 limit=0`
- `DONE k=9 range=[5890,5989] feasible=0 infeasible=1 limit=0`

The queue is now running at full 4-way parallelism.
--- result 26 (2026-11-02T13:25Z)
Chunk done: `DONE k=8 range=[4858,4957] feasible=0 infeasible=2 limit=0`. Continuing.
--- result 27 (2026-11-02T13:38Z)
I re-armed the monitor. Still waiting.
--- result 28 (2026-11-02T13:39Z)
Chunk done: `DONE k=9 range=[5990,6089] feasible=0 infeasible=1 limit=0`. Continuing.
--- result 29 (2026-11-02T13:56Z)
Chunk done: `DONE k=9 range=[6090,6189] feasible=0 infeasible=1 limit=0`. Continuing.
--- result 30 (2026-11-02T14:08Z)
Progress at 14:08 UTC:
- **κ=8:** 26 INFEASIBLE primes so far, from 4073 to 4969. The only FEASIBLE prime above 4057 is 4657. Node counts have reached about 21M at p=4969.
- **κ=9:** INFEASIBLE so far: 5743, 5779, 5851, 5869, 5923, 6067 and 6121.

I plan to stop starting new chunks at about 16:30 UTC, let the running chunks finish, and then report exact coverage.
--- result 31 (2026-11-02T14:33Z)
Chunk done: `DONE k=8 range=[5158,5257] feasible=1 infeasible=1 limit=0`. 5209 is INFEASIBLE (27,765,762 nodes) and 5233 is FEASIBLE. Continuing.
--- result 32 (2026-11-02T14:38Z)
I re-armed the monitor. Still waiting.
--- result 33 (2026-11-02T15:00Z)
Chunk done: `DONE k=8 range=[4958,5057] feasible=0 infeasible=3 limit=0`. Continuing.
--- result 34 (2026-11-02T15:08Z)
Status at 15:08 UTC: 4 chunks are running (κ=8 5058–5157, 5258–5357, 5358–5457 and κ=9 6190–6289). Still waiting.
--- result 35 (2026-11-02T15:35Z)
Chunk done: `DONE k=9 range=[6190,6289] feasible=0 infeasible=3 limit=0`. Continuing.
--- result 36 (2026-11-02T15:39Z)
κ=9 has added 6211, 6229 and 6247 as INFEASIBLE, with node counts of 6.7M–7.3M. Still waiting.
--- result 37 (2026-11-02T16:09Z)
Here is the end-phase plan:
- **κ=8:** contiguous coverage is complete through 5257. Chunks 5258–5357, 5358–5457 and 5458–5557 are still running, and I won't start any more κ=8 chunks.
- **κ=9:** contiguous coverage is complete through 6289, and 6290–6389 is running. A new feeder keeps the cores full with κ=9 chunks, which are faster, ascending from 6390. It stops launching at 18:00 UTC.
- **Finish:** everything still in flight runs to completion, then I write the final report.
--- result 38 (2026-11-02T16:28Z)
Chunk done: `DONE k=8 range=[5258,5357] feasible=1 infeasible=2 limit=0`. κ=8 contiguous coverage now runs through 5357, and κ=9 chunk 6390–6489 has been launched.
--- result 39 (2026-11-02T16:39Z)
I re-armed the monitor. Still waiting.
--- result 40 (2026-11-02T16:52Z)
Chunk done: `DONE k=9 range=[6290,6389] feasible=0 infeasible=3 limit=0`. κ=9 contiguous coverage now runs through 6389. Continuing.
--- result 41 (2026-11-02T17:09Z)
I re-armed the monitor. Still waiting.
--- result 42 (2026-11-02T17:29Z)
Chunk done: `DONE k=9 range=[6390,6489] feasible=0 infeasible=2 limit=0`. κ=9 contiguous coverage now runs through 6489. Continuing.
--- result 43 (2026-11-02T17:39Z)
Status at 17:39 UTC: running are κ=8 chunks 5358–5457 and 5458–5557, and κ=9 chunks 6490–6589 and 6590–6689. Still waiting.
--- result 44 (2026-11-02T17:55Z)
Chunk done: `DONE k=8 range=[5458,5557] feasible=0 infeasible=1 limit=0`. κ=8 5358–5457 is still running. The feeder launched κ=9 6690–6789 at 17:55, which will be its last launch before the 18:00 cutoff.
--- result 45 (2026-11-02T17:59Z)
Chunk done: `DONE k=9 range=[6490,6589] feasible=0 infeasible=2 limit=0`. The feeder made one last launch at 17:59 (κ=9 6790–6889), just before the 18:00 cutoff. Still running: κ=8 5358–5457 and κ=9 6590–6689, 6690–6789 and 6790–6889.
--- result 46 (2026-11-02T18:01Z)
The feeder has stopped. The first κ=9 chunk not launched starts at 6890. I'm waiting for the 4 chunks still running to finish.
--- result 47 (2026-11-02T18:10Z)
I re-armed the monitor and am waiting for the last 4 chunks.
--- result 48 (2026-11-02T18:40Z)
Results from the last chunks:
- **κ=8, chunk 5358–5457:** 5393 is INFEASIBLE (34,756,987 nodes) and 5417 is INFEASIBLE (36,898,232 nodes). 5441 and 5449 are still to run.
- **κ=9, chunk 6590–6689:** 6661 is INFEASIBLE (11,515,163 nodes).
- **κ=9, chunk 6690–6789:** 6733 is INFEASIBLE (13,081,875 nodes). The chunk is done with `feasible=0 infeasible=1 limit=0`.

Three chunks are still running.
--- result 49 (2026-11-02T18:44Z)
Chunk done: `DONE k=9 range=[6590,6689] feasible=1 infeasible=2 limit=0`. κ=9 contiguous coverage now runs through 6789. κ=8 5358–5457 and κ=9 6790–6889 are still running.
--- result 50 (2026-11-02T19:10Z)
I re-armed the monitor. Two chunks are still running.
--- result 51 (2026-11-02T19:39Z)
κ=9 6790–6889 is done (`infeasible=2`), and 5441 is INFEASIBLE (35,721,950 nodes). Only the κ=8 chunk 5358–5457 was still running, with 5449 left in it. I put the 3 idle cores on κ=9 chunks 6890–6989, 6990–7089 and 7090–7189 while it finishes.
--- result 52 (2026-11-02T19:40Z)
The older monitor has expired. The newer one is still watching. Waiting.
--- result 53 (2026-11-02T20:09Z)
I re-armed the monitor. Waiting on the last κ=8 chunk and 3 κ=9 chunks.
