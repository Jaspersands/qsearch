# Rees HSP: exact end-to-end simulation on small groups (campaign item 10)

2 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
Labels: **[exact]** = complete finite computation in exact arithmetic; **[float]** = complex
floating point, tolerance 1e-9; **[argued]** = reasoning, not machine-checked.

Files written (and nothing else):
`theorems/rees_end_to_end_sim.py`, `tests/test_rees_end_to_end_sim.py`, this report.
Full-run output (5 seeds, includes F_7) is outside the repo because only these three paths are
in my row: `/Users/jaspersands/Library/Application Support/Claude/side-session-notes/local_82ea8e9d-f8c7-4b78-b5f6-291cbf4bed0b/rees_end_to_end/full_run.{json,out}`.

Reproduce:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_end_to_end_sim.py
```
```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_end_to_end_sim --f7 --seeds 5 --out full_run.json
```

The tests (41) passed in 162 s. The full run (230 runs plus 32 negative
controls) took 1044 s. `git status --short` changed only by my two new files; the other new
paths belong to sibling sessions.

## 1. What runs

`run_rees(cover, oracle, backend)` is the whole algorithm. Its inputs are the public cover and
an oracle. It never receives H, log H or K_d. The truth is used only afterwards, by
`grade_run` and `stage_outputs_correct`.

1. **Cover.** `make_cover` takes explicit structure constants of L over F_p and computes γ_k(L)
   by elimination. It builds A = ⊕_k t^kγ_k(L) with [t^ix, t^jy] = t^{i+j}[x,y], checks Jacobi on A,
   and checks that each E_s (s = 1..c) is a Lie homomorphism on every basis pair. The group law is
   the truncated BCH product (class ≤ 4). The tests check it against the repo's `bch_via_ode`,
   including a class-4 algebra, n5 over F_7. The cover dimensions agree with
   `rees_hsp_reduction.make_rees_cover`. The tests also check associativity, that E_s and δ_λ are
   group homomorphisms, and that G_d → G_{d−1} is a homomorphism, on random triples **[exact]**.
2. **Lifted source.** The oracle f is a table on G = (L, ∗) with f(x) = f(y) ⇔ x⁻¹y ∈ H, built
   from group generators by closure. The simulator evaluates f(E_{s_i}(a)) on the whole address
   register, one vectorized call per evaluation point. That is the superposition query, charged
   as c queries per source, and the test checks that exactly c calls occur. Tracing out the label
   registers gives the source.
3. **Grades d = c..2.** For each source, the simulator computes the exact law of the Z_d label
   and samples a label from it. A block has M_d sources. The SDE Σ s_i^d λ_i = 0 is then solved by
   **brute force over F_p^{M_d}**, and a uniformly random witness is chosen from all nonzero
   solutions. The controlled-right-action channel (uniform superposition on Q = G_{d−1},
   controlled R_{δ_{s_i}(σ(q))}, zero-weight targets discarded, all targets traced out) produces
   one source on G_{d−1}.
4. **Readout.** S = m + 4 grade-one sources, each from its own descent tree, are measured
   after an exact abelian QFT. The output is the F_p-nullspace of the S samples.

**Arity.** M_d = κ_d g_d + 1 with κ_d = gcd(d, p−1). This is the Chevalley–Warning existence
arity, at which a witness exists for every label tuple (core check §5.2; small-prime report
§0). It is **not** Schedule 1's B_d(g_d) (64, 324 and 46656 at (d, g_d) = (2,1), (2,2), (3,1)),
and the Ivanyos–Santha solver is not run. Item 9 implements that solver.

**Two backends.**

- `ExactBackend` (all instances): a state commuting with left translations is stored as
  ρ = |G|⁻¹ Σ_g c(g) R_g, with c(g) ∈ Z[ζ_p] as integer vectors times one exact rational. All
  arithmetic is exact: no floats, and probabilities are `Fraction`s. Faithfulness requires left
  invariance. This is checked, never assumed. (i) The source: the tuple-oracle fibres are
  checked exhaustively to be the left cosets of the identity fibre S, which is checked to be a
  subgroup. (ii) The instrument: its Kraus operators are combinations of central R_z, and the
  test checks that the top grade of G_d is central. Π_λρΠ_λ is formed by two explicit
  group-algebra products. (iii) The channel: entry (q, r) of the output is
  |Q|⁻¹ F(σ(r)⁻¹σ(q)), where F(g) = Π_i Tr(ρ_i R_{δ_{s_i}g}). The code checks that F is constant
  on every central fibre gZ_d of G_d, which makes the entry depend on r⁻¹q alone for **every**
  address pair. A failure raises.
- `DenseBackend` (Heis(F_3), Heis(F_5)): explicit density matrices in complex floats. The
  instrument runs as its circuit: Fourier-prepared Z ancilla, controlled R_z, inverse Fourier,
  then measure. The channel uses explicit permutation matrices U_q = R_{δ_s(σ(q))} and the
  partial trace σ(q,r) ← σ(q,r)·Tr(U_q ρ_i U_r†), one target at a time. A separate test checks
  this one-target-at-a-time update against the joint two-target circuit. The readout uses an
  explicit QFT matrix. No left invariance is used.

On the same label record and witness, the two backends give the same source, post-measurement
and channel-output states to 1e-12 (Heis(F_3), Heis(F_5), all seven H each) **[float]**.

Simulation shortcut (exact, stated): every top-grade source is the same density ρ_{exp(h̃)}, so
it is prepared once. Its post-measurement state is computed once per label value and reused.
The query count still charges c per source. Sources below the top grade are never shared or
cached.

## 2. Instances and results

| G (cover dims, \|G̃\|) | M_d (Schedule 1 B_d) | top sources / queries per run | H tested |
|---|---|---|---|
| Heis(F_3): (3,1), 81 | M_2 = 3 (64) | 21 / 42 | 1; ⟨x⟩, ⟨y+z⟩, ⟨x+2y+z⟩ (non-normal, H∩Z = 1); Z(G); ⟨x,z⟩ (normal, ⊇ Z); G |
| Heis(F_5): (3,1), 625 | M_2 = 3 (64) | 21 / 42 | same seven |
| n4(F_5), [e1,e2]=e3, [e1,e3]=e4: (4,2,1), 78125 | M_3 = 2, M_2 = 5 (46656, 324) | 80 / 240 | ⟨e2⟩, ⟨e1⟩, ⟨e1+e3⟩ (non-normal, H∩Z = 1); ⟨e2,e4⟩ (non-normal, ⊇ Z); ⟨e1+e2,e3⟩ (Lie closure, 3-dim, normal); γ_2; ⟨e2,e3,e4⟩; Z(G); 1 |
| n4(F_7): (4,2,1), 823543 | M_3 = 4 (κ_3 = 3), M_2 = 5 | 160 / 480 | same nine |

Results: 5 seeds per (G, H). The exact backend ran all 32 (G, H) and the dense backend the 14
Heisenberg ones, 230 runs in all.

- **Recovery [exact]:** all 230 runs return exactly h = log H. Every subgroup type above is
  covered, including non-normal H with H ∩ Z(G) = 1 and non-normal H ⊇ Z(G). H = 1 ran on all
  four groups, H = G on the two Heisenberg groups.
- **Intermediate states [exact]:** in every exact run, every source produced on G_{d−1} (per
  class-3 group across seeds: 1800 on G_2 and 360 on G_1; 245 on G_1 per Heisenberg group)
  equals ρ_{H_{d−1}} with
  H_{d−1} = exp(⊕_{k<d} t^k(h∩γ_k)). This holds for every sampled record and every randomly
  chosen witness, so H is never replaced by another subgroup.
- **Label laws [exact]:** for every measured source, the label law is exactly uniform on
  K_d^⊥, with K_d = h∩γ_d in γ_d coordinates, and zero off it. The top-grade law is one
  distinct computation per run. The 1800 grade-2 laws per class-3 group are separate exact
  computations on channel outputs. On grade one, every readout law is exactly uniform on
  (th)^⊥ (checked in the tests for the Heisenberg and n4(F_5) runs at seed 20261102). Every
  observed label in all 230 runs lies in K_d^⊥.
- **Label laws [chi-square, observed labels]:** applied only where every expected count is
  ≥ 5 (120 stage-run cases; the dense Heisenberg runs repeat the exact ones' draws). The smallest p-value is 0.005, on n4(F_7) among 40 tests, which is consistent
  with multiple testing. The other groups' minima are 0.066 and 0.199. This adds little beyond
  the exact laws.
- **Witnesses:** a witness existed in every block (no block lost), as Chevalley–Warning
  predicts at this arity.

## 3. Negative controls (`negative_controls`, Heis(F_5) and n4(F_5), every H)

These show that the checks can fail.

- **One evaluation point instead of c** (Prop. `prop:single-evaluation`). The run fails, by a
  wrong intermediate state, **exactly** when [G,G] ⊄ H: 11 of 16 cases. It succeeds exactly when
  γ_2 ⊆ h **[exact]**, matching the proposition. **Finding:** in all 11 failing runs the
  *final* nullspace was still log H. The wrong sources still contain the correct lifted
  subgroup, so their Fourier support lies in h^⊥ (checked in an ad-hoc run at seed 7, not in the
  tests) and the nullspace is
  always ⊇ h. Here the mixture of wrong states happened to span h^⊥ **[argued]**. So a test that
  checks only the final readout cannot detect this failure. The exact per-stage state check
  can. This does not show that one evaluation point suffices in general.
- **A nonzero non-witness s.** The fibre-constancy check raises ("does not descend") in every
  case with [G,G] ⊄ H. When γ_2 ⊆ h, K_d = Z_d at every stage, every label is 0, no non-witness
  exists, and the run correctly succeeds.

## 4. What this shows and what it does not

Shows **[exact, finite]**: on the 32 listed (G, H) over F_3, F_5 and F_7 (classes 2 and 3),
running the algorithm of main.tex §§`sec:rees-cover`, `sec:instrument` and `sec:recursion` from
oracle access alone recovers log H exactly. On these instances it confirms, by computation,
core-check claims 1(4) (tuple oracle ⇔ exp(h̃)), (2a) (branch law uniform on K^⊥, arbitrary K
including K = 1 and K = Z), (2c) (output ρ_{HZ/Z} for every record and witness), (2e) (stage
groups and H_d) and §7.2 (terminal group tL with hidden subgroup th, not L/[L,L]). It also
covers κ_3 = 3 at p = 7, where cubing is not a bijection. It extends the earlier fixed fixture
`rees_complete_instrument.py`, which used two hidden lines on n4(F_5) with selected label
tuples and float phases, to arbitrary input algebras, i.i.d. sampled labels, exact arithmetic,
four groups, 32 subgroups and an independent dense backend.

Does **not** show:

- anything for groups or primes not run. This is a finite falsifier (TRAPS 7);
- a coherent receiver or a gate-level circuit. The simulation is exponential-size classical
  linear algebra. `coherent_receiver_implemented` stays false;
- Schedule 1 (B_d arity, Ivanyos–Santha solver), Schedules 2–3, or any asymptotic query, time or
  error bound. Brute force over F_p^M is test-size only;
- the approximate-QFT/finite-gate-set error analysis (core check §6.3, §7.2). All instruments
  here are exact;
- the black-box, prime-power, or copy-only input models (only the ordinary oracle is run);
- priority or novelty.

## 5. Exact statement that now holds

**[exact]** For L ∈ {Heis(F_3), Heis(F_5), n4(F_5), n4(F_7)} and every listed H, with oracle
access to a left-coset hiding function f of H only, the procedure (c-point lifted sources, c
queries each; for d = c..2, exact central measurement, a brute-force SDE witness at arity
κ_d g_d + 1, and the controlled-right-action channel; S = m + 4 exact grade-one Fourier
samples) returned log H in each of 5 seeded runs per (G, H). Every intermediate source equaled
ρ_{H_d}, and every label law equaled the uniform law on K_d^⊥. Charged cost per run: 42 queries
(Heisenberg), 240 (n4(F_5)) or 480 (n4(F_7)).

Still missing (for the paper's general claim): an implementation of the Schedule 1 solver at its
arity (item 9), a gate-level coherent implementation, and every asymptotic statement. These
remain written proofs (core check §§5–7), not computations.

## 6. Claim gates that must stay false

In `research/reductions/rees_hsp_reduction.json`: `coherent_receiver_implemented`,
`general_sde_implemented`, `independent_review`, `novelty_established`,
`speedup_claim_allowed` and `formal_compiler_checked`. In
`research/reductions/rees_complete_instrument.json`: `quantum_receiver_implemented`,
`asymptotic_runtime_tested`, `independent_review` and `formal_verification`. This simulation
changes none of them. Its own report also sets `schedule_one_solver_tested` and
`asymptotic_cost_tested` to false.

## 7. Text fixes for main.tex (listed, not applied)

1. After the "Finite control" paragraph (`main.tex:348`), add a sentence:
   "\file{theorems/rees\_end\_to\_end\_sim.py} runs the whole algorithm from oracle access, in
   exact $\mathbb{Z}[\zeta_p]$ arithmetic, on the Heisenberg groups over $\mathbb{F}_3$ and
   $\mathbb{F}_5$ and the class-three filiform groups over $\mathbb{F}_5$ and $\mathbb{F}_7$, for
   32 hidden subgroups. These include nonnormal ones with $H \cap Z(G) = 1$, nonnormal ones
   containing $Z(G)$, $H = 1$ and $H = G$. It samples labels i.i.d., solves each diagonal system
   by exhaustive search at the Chevalley--Warning arity $\kappa_d g_d + 1$, and recovers
   $\log H$ in every run. Every intermediate source equals $\rho_{H_d}$, and every label law is
   exactly uniform on $K_d^\perp$. It is a finite control, not an implementation of
   Schedule~1 or of a coherent receiver."
2. After Prop. `prop:single-evaluation` (`main.tex:265`), optionally add: "With one evaluation
   point, the intermediate sources are wrong exactly when $[G,G] \not\le H$, but the final
   annihilator can still equal $\hh$. Tests that inspect only the final readout therefore
   cannot detect this failure." Source: §3 above.
3. No correction to the algorithm's statements is needed: no run contradicted Lemma
   `lem:homogeneous`, Lemma `lem:central`, Prop. `prop:descent` (core check (2c)) or the terminal
   readout.
