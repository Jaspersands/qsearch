# arXiv watch: reviewed triage of flagged papers

Reviewed 2026-10-21. This covers every paper that `research/audits/arxiv_collisions.json`
labels `possible-kill` (7) or `possible-scoop` (15), across all tracks, as of the 2026-10-19
backfill run in the main checkout.

**Method.** Each abstract was read against the project documents it matched. I also grepped the
notes, the registry, the preprint and the outreach drafts for each paper's key objects. I read
the full text only for 2610.06753, Proposition 8. For 2610.03566 I read only the full abstract.
These are the reviewer's verdicts, not the authors', and they are not independent proofs.

**Result.** No paper invalidates a project claim, and no paper scoops a result the project
presents as new.

- Nine call for a citation or a narrower sentence.
- Eight overlap in topic only.
- Five are keyword false alarms.

Verdicts used below:

- **should cite**: no conflict, but a named document should mention the paper or narrow a
  sentence.
- **related only**: shared topic, nothing to do.
- **false alarm**: the cue or the corpus match is spurious.

**Stale labels.** Five of the 22 are already cited in research notes: 2609.35101, 2610.00502,
2610.01902, 2610.06753 and 2610.16827. The watch ran on 2026-10-19, before those notes were
indexed. Against today's corpus index, all five would be `already-cited`.

## Public-facing documents (preprint and outreach)

The preprint and outreach actions in this section were applied on 2026-10-21. The
note-level actions in the next section are left to the agents.

### 2610.06753, Mazumder and Niroula, *Discovering New Problems for DQI*

Flagged kill. Verdict: **should cite**. It does not weaken Result A.

**The cap (Proposition 8).** The proposition assumes:

- the objective counts satisfied constraints;
- decoding is worst-case Hamming with 2ℓ+1 < d;
- the code rate is 0 < α < 1.

Under those assumptions, DQI's satisfied fraction exceeds Prange completion, ρ + (1−ρ)α, by at
most κ(α) = √(u(1−u)) − u, where u = α/2. Over all α the maximum is (√2−1)/2 ≈ 0.207.

**Our low-rate input against the cap.**

- At N = 127 and K = 39, α ≈ 0.307 and ρ ≈ 1/2. Prange completion gives 0.654, so the cap is
  about 0.861, or 109.4/127 asymptotically.
- The classical witness of 109/127 already sits at that cap.
- The project's certificate at ℓ = 19, which is inside half the distance, is 0.8168
  (`research/PRIME_CHARACTER_FINITE_READOUT.md:152`). That is below both.
- The only radius that beats the witness is ℓ = 32 (0.9028). It lies outside the cap's
  hypothesis. The preprint already makes it conditional on "an exact unique decoder beyond half
  the minimum distance" (`docs/papers/classical-competitors/main.tex:142`).

**Multiplicative polynomial intersection.** This is the paper's discrete-log candidate. It is a
different problem from power-character OPI. The agents already credit it as their starting
point (`research/BALANCED_SIGNED_MPI.md:12-18`).

**Actions.**

- Preprint: cite the cap at `main.tex:142` and in the Relation paragraph. Under worst-case
  Hamming decoding, a DQI edge at this rate needs decoding beyond the cap's regime.
- Outreach draft `docs/outreach/01-dqi-opi.md`: reword question 2 (lines 72-73), which the
  paper partly answers. Ask instead whether decoding beyond half the distance is plausible for
  explicit characters.
- Consider adding Mazumder and Niroula as recipients of that draft.

### 2610.03566, Piveteau, Quek and Franco Garrido, *Gibbs state preparation through quantum decoding*

Flagged scoop. Verdict: **should cite**. This is the highest priority among the Gibbs papers.

**What the paper does.** It replaces HDQI's classical decoder with quantum decoders over
pure-state classical-quantum channels, for uniformly random signs.

- Its unambiguous-discrimination decoder is "dequantized" into a classical rejection sampler
  that matches the decoder's temperature threshold.
- Its BPQM decoder exceeds the classical Shannon limit on dilute spin glasses.

**Why this does not undercut the project.**

- The rejection sampler appears to be per-symbol USD plus Prange; the abstract alone does not
  settle it. The project's matched sampler eliminates the inner spin per block and beats the
  independent-clause baseline (`research/PARITY_BLOCK_USD_PRANGE.md:117-121`).
  `NEG-PARITY-BLOCK-USD-MATCHED-CLASSICAL-PRANGE` stands.
- The square-root temperature law is already the project's pure-state channel
  parameterization.
- The finding that BPQM goes beyond the ceiling is already labelled "KNOWN MECHANISM"
  (`research/BPQM_GIBBS_FRONTIER.md:3`).
- The polar bound, E_J TV ≤ 0.010221, is a classical bound at fixed c, so no quantum improvement
  can invalidate it.

**Actions.**

- Preprint: cite it near `main.tex:206` and at the product-USD/Prange ceiling sentence.
- Outreach draft `docs/outreach/02-polar-gibbs.md`: acknowledge the paper. Piveteau is a likely
  recipient; the preprint cites Piveteau and Renes. The paper's BPQM threshold partly answers
  question 2 (lines 78-79).

## Research notes and registry (agent-owned; corrections for the agents)

| arXiv | Title (short) | Flag | Verdict | Reason and action |
|---|---|---|---|---|
| 2610.00502 | OPI variants beyond locality | scoop | should cite | The ternary notes already build on it. The abstract says the m = Ω(n²) regime of Chen, Liu and Zhandry is "now covered by classical algorithms". `research/DCP_BINARY_ERROR_SOURCE_BRIDGE.md:15-16` still calls m = εn² "a potential ... exponential classical separation". Add the paper to that note's Literature Update and check which ε the classical result covers. |
| 2610.03645 | Random-order streaming space advantage | scoop | should cite | A second streaming-DQI result for OPI: low rate, O(d log n) qubits against Ω(n) bits. Not the Hermite half-rate decoder. Add it to "Novelty And Attempts To Disprove It" in `research/HERMITE_STREAMING_COMPOSITION.md`. |
| 2609.40036 | Cycle codes and DQI | kill | should cite | The corpus match (the QAOA and LPN notes) is spurious. The real overlap is `research/TERNARY_COLORING_BPQM.md` (q = 3 cycle codes), which claims no speedup. The paper's LP decoder is a classical baseline that note lacks. Cite it next to Mandal and Pfister, and run the LP decoder before continuing that line. |
| 2610.03697 | Redundancy-free Hamiltonians | scoop | should cite | "Redundancy-free" is the independent-label condition of `research/HDQI_PREDECESSOR_UNIFORM.md:55-57`. Its NP-hardness at large β²d does not contradict the note's exact solver, which is restricted to predecessor-uniform orders. Add it to the note's prior-art comparison. If the paper contains the radius recurrence, record a rediscovery. |
| 2610.01141 | Classical hardness of Hamiltonian-function learning | scoop | should cite | No theorem breaks. But the QML registry lesson ("cannot achieve scalable super-polynomial quantum advantage", `research/registry/negative_results.json:68483`) is broader than its evidence, which covers kernel concentration, projected kernels, QTK and HHL. A factoring-based learning separation contradicts the universal wording. Scope the lesson to kernel and variational QML. |
| 2609.37636 | Resonance breaking in noisy Shor | scoop | should cite | Supports the project's fault-tolerance notes, e.g. `QUANTUM_ERROR_MITIGATION_EXPONENTIAL_BARRIER.md:22`. Framed as "we argue". Cite it as supporting evidence there. |
| 2610.16827 | Quantum character transform | scoop | should cite | Already cited in two notes. The project's S_n class-sum block encodings are special cases of its generic construction, and the project disclaims novelty for them. Cite it wherever those encodings are presented. |
| 2610.01902 | Streaming DQI, Hermite OPI | scoop | related only | Already the base of the Hermite line and credited as prior art (`research/HERMITE_DECODER_PRIOR_ART.md:37`). |
| 2609.35101 | Homomorphic polynomial transduction | scoop | related only | Already cited as the source framework (`research/CHAIN_SUPPORT_BUDGET.md:12` and two others). |
| 2609.40250 | Classical Gibbs sampling, quantum p-spin | kill | related only | Noncommuting p-spin; the project claims no Gibbs advantage there. Optional: add algorithmic stochastic localization to the classical baselines in `AFFINE_CLUSTER_NATIVE_PROBE.md`. |
| 2610.02079 | Transverse-field Ising phase diagram | kill | related only | Strengthens the classical side that the annealing note already argues. Optional baseline for `RELATIVE_GIBBS_WORLDLINE.md`. |
| 2609.40260 | Minimum generating set | scoop | related only | No project claim on generating sets or chief series of black-box groups. |
| 2610.04597 | State identity testing | scoop | related only | Uses Jucys–Murphy elements for Schur sampling in fidelity testing, a different task from the coset JM label work. |
| 2610.05752 | S_n character-state preparation | scoop | related only | The project never claims character-state preparation. |
| 2610.08714 | Multivariable polynomial transformations | scoop | related only | No project theorem says multivariable synthesis needs bad normalization. The project's normalization no-gos are univariate degree bounds and are explicitly scoped (`DCP_PGM_PROJECTED_ENCODING.md:3-4`). |
| 2609.40302 | Sublinear sparse SDPs | kill | false alarm | "SDP" matched a note on an LWE-style SDP decoder. The project has no quantum SDP speedup claim. |
| 2609.35239 | Clifford template compilation | kill | false alarm | The cue "classically simulable" refers to forward Clifford dynamics, which the paper concedes is easy. |
| 2609.36480 | Black-box abelian group decomposition | scoop | false alarm | The project's "Regev" is the 2004 DCP reduction, not Regev factoring. The project makes no group-decomposition claim. |
| 2610.06781 | Pretty good shadow tomography | scoop | false alarm | Shares only the phrase "pretty good measurement" with the coset copy-count ledger. |
| 2610.06812 | Protecting quantum computers from untrusted users | kill | false alarm | The project makes no claim about one-bit readout, DQC1 or factoring simulability. |

## For the watch itself

- **Kill flags.** 0 of 7 were real kills. Two were weaker relatives worth citing but not
  damaging: 2609.40036 and 2610.06753. Five were related-only or false alarms.
- **Scoop flags.** 0 of 15 were real scoops. Five were already cited by the time of review.
- **Rerunning the labels.** Labelling against the current index would turn those five into
  `already-cited`.
