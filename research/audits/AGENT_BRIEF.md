# Agent brief

Generated 2026-11-14 by `python tools/brief/build_brief.py`; covers the 7 days since 2026-11-07 (00:00 local time, UTC+11:00). Do not edit by hand.
Read it before choosing a direction. "Not available" means the source could not be read, not that there is nothing to report.

## Registry

966 negative records in the working copy; 969 at commit df47b77f (2026-10-30), the registry's last change before 2026-11-07.

Added (0): none.
Removed (3, all now in the quarantine file): `NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER`, `NEG-ISOTROPIC-PARABOLIC-DEQUANTIZATION-BOUND`, `NEG-SINGER-CYCLE-TORAL-HSP-BARRIER`.

## arXiv watch

Possible kills and scoops with no person's verdict yet: 4. First seen since 2026-11-07 and already reviewed: 0. Labels are triage; verdicts are judgement.
Open backlog: 0 possible kills; 4 possible scoops (oldest first within each label).
Watch last saved a run on 2026-11-02.
- Track algorithm_discovery last covered through 2026-11-02.
- Track bpqm_gibbs last covered through 2026-11-02.
- Track code_equivalence last covered through 2026-11-02.
- Track dcp last covered through 2026-11-02.
- Track dequantization last covered through 2026-11-02.
- Track dqi_opi last covered through 2026-11-02.
- Track hidden_shift last covered through 2026-11-02.
- Track lattice last covered through 2026-11-02.
- Track nonabelian_hsp last covered through 2026-11-02.
- Track number_theory last covered through 2026-11-02.
- Track qsvt last covered through 2026-11-02.
- Track query_and_fourier last covered through 2026-11-02.
- Track representation last covered through 2026-11-02.
- Track state_discrimination last covered through 2026-11-02.
The watch has checkpoints older than this brief's window; refresh the watch before treating it as current.
Verdicts recorded since 2026-11-07: 0.

Open actions from verdicts (6; once one is done, run `python tools/arxiv_watch/watch.py --action-done ID`):

- `2609.37636` (human): Cite it as supporting evidence in the fault-tolerance notes, e.g. `research/QUANTUM_ERROR_MITIGATION_EXPONENTIAL_BARRIER.md`.
- `2609.40250` (human): Optional: add algorithmic stochastic localization to the classical baselines in `AFFINE_CLUSTER_NATIVE_PROBE.md`.
- `2610.00502` (human): Add the paper to the Literature Update of `research/DCP_BINARY_ERROR_SOURCE_BRIDGE.md` and check which ε the classical result covers.
- `2610.01141` (human): Scope the QML registry lesson to kernel and variational QML.
- `2610.03697` (human): Add it to the prior-art comparison in `research/HDQI_PREDECESSOR_UNIFORM.md`. If the paper contains the radius recurrence, record a rediscovery.
- `2610.16827` (human): Cite it wherever the project's S_n class-sum block encodings are presented.

Actions awaiting clarification (resolve the target before acting):

- `2609.40036`: Cite it in `research/TERNARY_COLORING_BPQM.md` next to Mandal and Pfister, and run the LP decoder before continuing that line. Pending: The reviewed target research/TERNARY_COLORING_BPQM.md is absent from this checkout. Ask the reviewer to identify or restore the intended note before carrying out the original action.
- `2610.02079`: Optional baseline for `RELATIVE_GIBBS_WORLDLINE.md`. Pending: The reviewed target research/RELATIVE_GIBBS_WORLDLINE.md is absent from this checkout. Ask the reviewer to identify or restore the intended note before carrying out the original action.
- `2610.03645`: Add it to "Novelty And Attempts To Disprove It" in `research/HERMITE_STREAMING_COMPOSITION.md`. Pending: The reviewed target research/HERMITE_STREAMING_COMPOSITION.md is absent from this checkout. Ask the reviewer to identify or restore the intended note before carrying out the original action.

| arXiv | Label | First seen | Verdict | Title |
|---|---|---|---|---|
| 2610.24719 | possible-scoop | 2026-10-26 | **open**: read it | Fast \(\ell_\infty\)-Reduction of Rank-2 Lattices in $\mathbb{R}^n$ via a New Reduced-Basis Notion |
| 2610.28737 | possible-scoop | 2026-10-26 | **open**: read it | Local Clifford equivalence to CSS codes: Polynomial-time classification and conversion |
| 2610.36731 | possible-scoop | 2026-11-02 | **open**: read it | Beyond LWE: Post-Quantum Assumptions under a Counterfactual Break of the Dihedral Coset Problem |
| 2610.40592 | possible-scoop | 2026-11-02 | **open**: read it | Toric codes all the way down: decoupling translation-invariant topological CSS codes in higher dimensions |

## Referee

34 notes reviewed; 0 flagged unsound or needs-work; 0 reviews stale (the note changed since). Queue: `research/audits/REFEREE_QUEUE.md`.


## Preflight

No problems from the static checks of `python tools/preflight/preflight.py`.

## Inertia

From `site/data/cockpit.json`, built 2026-11-12 (rebuild: `python tools/cockpit/build_cockpit.py`). A direction is flagged after 8 handoff sections with no registry gain in it.

- OPI / prime character (`opi`): 100 sections since the registry last gained a record here (never).
- BPQM / polar (`bpqm`): 31 sections since the registry last gained a record here (never).
- DCP / dihedral coset (`dcp`): 55 sections since the registry last gained a record here (2026-10-12).
- Carrier / PGM (`carrier_pgm`): 35 sections since the registry last gained a record here (2026-10-12).
- Ternary / lattice (`lattice`): 119 sections since the registry last gained a record here (2026-10-12).
- Code equivalence (`code_equivalence`): 14 sections since the registry last gained a record here (2026-10-11).

## Possible duplicates

No negative was added in the window, so there is nothing to compare.

## Commands

- **oracle**: `python tools/corpus/cli.py been-tried "<one paragraph describing the idea>"`. Before proposing or extending a direction: read the nearest retained negatives and say how the idea escapes them (MCP been_tried).
- **screener**: `python tools/dqi_screen/screen.py --params CANDIDATE.json`. Before any DQI claim: exit 1 means not viable under the Mazumder-Niroula soundness rules (MCP screen_dqi_candidate).
- **baselines**: `python tools/corpus/cli.py baselines "<one line describing the idea>"`. Before claiming an advantage: the classical algorithms the idea must be compared against (MCP classical_baselines).
- **preflight**: `python tools/preflight/preflight.py`. Before every commit: exit 1 lists JSON that does not parse under research/hypotheses/, research/registry/, research/audits/ and research/classical_baselines/, plus theorems/, core/ and qsearch_cli/ modules the CLI refers to that are missing or not tracked by git, and research/audits/cli_manifest.json subcommands missing from the CLI registry's ORDER or listed there under another module.
- **duplicates**: `python tools/corpus/cli.py check-new --file DRAFT_RECORD.json`. Before filing a negative: exit 2 means a retained or quarantined record is close (TF-IDF cosine 0.6 or above). A match is a record to read, not proof: extend it, say how the draft differs, or pass --allow ID for a sweep sibling you have read (MCP check_duplicate_negative).
