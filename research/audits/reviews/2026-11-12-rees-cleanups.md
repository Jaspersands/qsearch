# 2026-11-12 Rees cleanups (four small items)

**AI-run, pending human review.** No Git, no network, no paper/STATE/handoff/reductions file edited.
The only existing file edited is `2026-11-12-rees-exponent-discharge.md` (item 1, permitted).
Folder: `2026-11-12-rees-cleanups/` (pre-edit copy of that note).

## 1. Exponent-discharge note fixed per its referee

Pre-edit copy: `2026-11-12-rees-cleanups/exponent-discharge-pre-cleanup.md`. Every edit is listed at the
end of the note under "## Cleanup (2026-11-12)". Numbers I verified myself (not just copied):

| claim | check | result |
|---|---|---|
| E_2(9) members for p ≤ 20000 | `E2_k9_le20000.json`: members/nonmembers/undecided | 342 / 30 / 0, so 372 primes ≡ 1 mod 9 (sympy count 372 agrees); max 19963. The note's 414 is wrong for 20000 |
| E_2(8) | same, k = 8 | 293 members, max 14281 |
| 2521 ∈ E_2(8), E_2(9) | json membership | TRUE for both |
| rule values at p = 2521 | `exponents.e_grade`, c = 9 | R2 81, R3 38, R5 20 (R4 26, R1t/S1t 53): matches the referee |
| 414 for ≤ 25000; 1373 exceptions, 78 decided (72 members, 6 non), 1295 open to 424549 | copied from `2026-11-10-rees-dfs2b-queue-final.md` l. 90–91 and `2026-11-04-rees-k9-sweep.md` | NOT recomputed |
| tower thresholds 1.347e5 / 135000 / 2125764 | appendix-schedule2.tex l. 563 and 645; 2125764 = 4·3^12 is the note's own closed form | not re-derived |
| T_A, E_S1t, Weil tail | referee_checks.out | not recomputed |

Main corrections: 342 for 414; 2521 ∈ E_2 and the "artefact" paragraph restated; T2, T3 (and T4, T5)
relabelled CONDITIONAL; T1 gets the J = ∅ sentence, the public-arity rule and the Las Vegas charge; the
O_κ(1) search-cost caveat; the undecided κ = 9 set restated; tower status; the 37 / 19 / 53 labels; gate
bound replacing "UNKNOWN" (2c+2 = 20 at c = 9); pool-lemma core-procedure caveat; the §1 Conclusion
heading no longer says "only human review". Not changed: §7, §8, the exponent tables.

## 2. `hpgp_free23.py` (exit (ii) of the entangled-twist impossibility note)

Files: `2026-11-12-rees-entangled-twist-impossibility/hpgp_free23.py`, `.../hpgp_free23.out`
(`nice -n 19 /opt/anaconda3/bin/python hpgp_free23.py 5 7`, p = 5 in 7 s, p = 7 in 67 s, under 100 MB).
The note names the script but never defines "IS's HPGP′ measurement". IS's HPGP′ input is the
phase-free level-set state Σ_x |x⟩|u+Q(x)⟩, whereas our register carries a quadratic phase, so there is no
literal IS algorithm to apply. I therefore computed something stronger that covers every single-copy
measurement.

**What it computes (exact, free23 BCH group over F_p, p = 5, 7).** One copy
φ_λ(a) = p^{-1/2} Σ_t ω^{-λ·C_a(t)} |π(a·exp(tη))⟩ on G/γ_3 = F_p^3, λ = measured γ_3-label (known),
base point a uniform (unknown), H = ⟨exp η⟩ hard, η = (e1,e2,e3,eu,ew). For each hypothesis h it forms the
exact nuisance-averaged density matrix ρ_h and reports the Holevo quantity χ = S(avg ρ_h) − avg S(ρ_h)
(an upper bound on the information of ANY measurement of one copy), the information of abelian Fourier
sampling in the exp chart, and controls. Hypotheses: HYP1 = the line (e1:e2) of V/D (p+1 of them, "the
line of v_1"); HYP2 = the line ⟨(e1,e2,e3)⟩ of V (p²+p).

**Results** (bits; `hpgp_free23.out`; p = 5 | p = 7):

| case | χ (any measurement) | Fourier-chart MI |
|---|---|---|
| λ ≠ 0, HYP1, all nuisance (a, e3, eu, ew) uniform | 0.0000 | 0.0000 |
| λ ≠ 0, HYP2, all nuisance uniform | 0.0000 | 0.0000 |
| λ ≠ 0, HYP1, a fixed (control; must be informative) | 2.07 \| 2.57 | 0.0000 |
| λ ≠ 0, HYP1, central part (eu,ew) = 0 known | 0.636 \| 0.711 | 0.0134 \| 0.0079 |
| λ ≠ 0, HYP1, (e3,eu,ew) = 0 known | 1.787 \| 2.207 | 0.117 \| 0.098 |
| λ ≠ 0, HYP2, (eu,ew) = 0 known | 2.214 \| 2.718 | 0.130 \| 0.106 |
| λ = 0, HYP1 | 0.4136 \| 0.3673 | equal to χ |

(log2 of the number of hypotheses: HYP1 2.585 | 3.000; HYP2 4.907 | 5.807.) The nonzero λ
(1,0), (0,1), (1,1) agree at p = 5; at p = 7 only λ = (0,0) and (1,0) were run (GL_2 symmetry). Trace of ρ_h = 1 asserted in the code.

**What it shows (finite computation; it can only falsify).**
1. For every λ ≠ 0 (probability 1 − 1/p²) and uniform hard H, **every** ρ_h equals I/p³ (mean S(ρ_h) =
   log2 p³ = 6.966 | 8.422 bits), so χ = 0 for any single-copy measurement. Two-line proof, so this is
   PROVED, not only observed: the linear coefficient of λ∘C_a(t) is λ(η_c) + (terms in a, η̄), and uniform
   η_c makes it uniform and independent; averaging ω^{ct} over c kills every off-diagonal term t ≠ t′,
   leaving the uniform mixture over the points a·exp(tη̄), and uniform a makes that I/p³.
2. Hence the simple version of exit (ii), "measure one label-carrying copy on a non-abelian frame, with
   copies independent", is **REFUTED**: it carries zero information about the line of v_1 or K/γ_3
   whenever λ ≠ 0. This holds because η_c is unknown. If η_c were known, one copy would carry up to
   χ = 1.8 | 2.2 of 2.6 | 3.0 bits, but plain Fourier sampling extracts only about 0.1 bit (Fourier
   chart), so the concrete measurement is weak even then.
3. **Not closed:** η_c (and e3) is shared by all copies of the same H while λ_i differ, so the joint state
   of several copies is not the product of the marginals computed here, and joint measurements
   (these are the zero-sum structure) are untouched. The λ = 0 copies (probability 1/p²) carry 0.37–0.41
   bits each, as a plain coset-state of a line in heis_3. Only p = 5, 7 were run; no scaling in p is
   claimed.

**Proposed text for the impossibility note (§8 (ii), and "Next hard question").** Replace the last two
sentences of (ii) by:

> Single-copy marginals carry nothing. For λ ≠ 0 and uniform hard H, the a- and η_c-averaged state of
> φ_λ(a) on G/γ_3 is I/p³ for every hypothesis (averaging ω^{λ(η_c)t} over η_c kills the t ≠ t′ terms;
> averaging a makes the point uniform). So no measurement of a single label-carrying copy reveals the line
> of v_1 or K/γ_3 (exact check p = 5, 7: `hpgp_free23.out`, Holevo χ = 0). Any exit-(ii) algorithm must
> measure several copies jointly, using that η_c is shared. **UNKNOWN** whether such a measurement exists.

Next question: the same Holevo computation for two copies with labels λ_1, λ_2 and shared η (state space
p^6 = 15625 at p = 5; not done). Acceptance test: χ_2 > 0 would show joint information; χ_2 = 0 for all
λ_1, λ_2 would extend the refutation.

## 4. H_3(Z) referee reruns

In `2026-11-12-rees-h3z-referee/`, with `nice -n 19 /opt/anaconda3/bin/python`, new files only:
`step1_sim_b1.rerun.out` (`step1_sim.py 1`), `step1_sim_b2.rerun.out` (`step1_sim.py 2`),
`struct_referee.rerun.out` (`struct_referee.py 3 3000 7`). Each ran in seconds.

| rerun | diff against committed | verdict |
|---|---|---|
| `step1_sim_b1.rerun.out` vs `step1_sim_b1.out` | empty (byte-identical, 14 lines) | MATCH |
| `step1_sim_b2.rerun.out` vs `step1_sim_b2.out` | empty (byte-identical, 14 lines) | MATCH |
| `struct_referee.rerun.out` vs `struct_referee.out` | empty (byte-identical, 25 lines) | MATCH |

Which lines are deterministic: `step1_sim.py` has no random numbers (it is an exact distribution computed
in floating point), so all lines are deterministic, and the equality shows the floating-point output is
reproducible on this machine at the printed precision. `struct_referee.py` uses `random.Random(7)`
(seeded by the third argument) for the random-instance block (3) and `random.seed(1)`, so even those lines
are deterministic for fixed seeds and they match; the exact-integer blocks (1), (2) are deterministic by
construction. Caveat: identical output is evidence of reproducibility, not of correctness of the
referee's claims; the checks can only falsify.

## 3. DL_11.g (p = 11 Aut(DL))

- Files: `2026-11-12-rees-entangled-twist-impossibility/gap/DL_11.g` (written 17:25), `dl_aut_11.out`
  (0 bytes, 17:25). There is no `gap/DL_11.gout` and no `DL_11.json`. **The earlier job never wrote any
  output**: `dl_aut.py` only keeps `.gout` data from `AutomorphismGroup(G)`, which never returned.
  Result: NOT computed.
- For scale, `DL_5.gout` and `DL_7.gout` were produced about 1 s after launch (17:19:50 → 17:19:51
  and 17:19:58 → 17:19:59), so p = 11 is far slower, not a 1-s job (group of order 11^8).
- I reran it once: `nice -n 19 timeout 1800 gap -q gap/DL_11.g` (21:11 → killed by the 30-minute
  timeout at about 21:41, RSS 118 MB, no `.gout` written; `gap/DL_11.stdout` holds only the harmless
  "packagemanager not available" notice). So it did not finish within a 30-minute cap, and its
  growth rate is unknown. NOT computed.
- Rerun fits the 2-hour cap only if allowed to run up to ~2 h, with no evidence it would finish; I
  did not spend that. The note's §7 DL table (p = 5, 7) is unaffected, and nothing claims p = 11.
  The note's line 313 ("still running at writing") should now read "did not finish in 30 min; NOT
  computed".

## Adversarial self-check

- Item 1: I verified the 342/293/2521 numbers and the p = 2521 rule values by recomputation; the 414,
  1373/78/1295, tower thresholds and T_A values are quoted. Relabelling T4/T5 CONDITIONAL goes slightly
  beyond the referee's explicit list (T2, T3); I think it follows from the paper's status convention, but
  the owner may want T5 kept at "refereed".
- Item 2: the proof that ρ_h = I/p³ uses a uniform η_c, i.e. a uniformly random hard H; it says nothing
  for a structured H or for several copies. My "HPGP′" is a Holevo bound plus Fourier sampling, not IS's
  algorithm (which targets phase-free states); the result refutes only single-copy measurements.
- Item 3: absence of output is all I can say; a bug in DL_11.g (e.g. wrong relations at p = 11) is
  not excluded because it was never confluence-checked at p = 11 here.
- Item 4: matching output shows reproducibility only.
