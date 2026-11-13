# Referee: Theorem F23, cover-free HSP for hard cyclic H in free23 (2026-11-13)

**Status: AI-checked, pending human review.** One hostile AI referee (Claude). Target:
`2026-11-13-rees-free23-theorem.md` and its folder. Context read: the two-copy report §1–2, the pair-measurement
report §2 and §9, the triples referee, the 11-12 impossibility note §1 and §8, core `main-core.tex` ll. 222–228 and
865–895, provenance l. 366, and greps of `CLASS_THREE_HSP_THEOREM_DRAFT.md`. The referee's code is in
`2026-11-13-rees-free23-theorem-referee/`. It was written from the definitions and imports nothing from the audited
folders. No other file was edited. Finite checks only falsify (TRAPS 7).

## Verdict: PROVED WITH FIXES (Route A, given cited theorems)

I found no gap in Route A. Theorem F23 (§5 of the target) holds as stated for p ≥ 5000, with the brute-force branch
below that, given the standard results listed in §6. None of the fixes below changes the statement or a constant
materially.

**Fixes.**
1. **Lemma 0's provenance.** It is no longer only inherited. §1 below proves the structure. The closed form is a
   rational-function identity, verified symbolically (`symbolic_lemma0.out`). Note that δ = n identically, because
   det(g_0, x') = λ·x', so A_3 = −(n²/6)h(e).
2. **The η_c step needs a written transversal.** K̂ = exp(F_p η̂_V)γ_3 is **not normal** in G: [X_0, η_V] has
   Z-coefficient e_1. The step therefore has to be done on left cosets, through an explicit section.
   * Take i_0 with ê_{i_0} ≠ 0 and t = g_{i_0}/ê_{i_0}. Then g = r·k, with r = g·exp(−tη̂_V) stripped of its γ_3 part,
     and k ∈ K̂.
   * K̂ is abelian, so the left factor gives only a global phase.
   * This is the only H-dependent subgroup in F23. It is used after ε has been learned, through left cosets only, and
     no quotient by it is formed. So it is not the frozen-normalizer error (§3). A wrong ε̂ is caught by the
     verification step.
   * The target says only "restrict to cosets of K".
3. **Arithmetic label (§4, "p = 5003 (p ≡ 1 mod 3)").** 5003 ≡ 2 mod 3. The value 0.548 is the worst-case bound
   (N_T = 432) evaluated at 5003. The first prime ≡ 1 mod 3 above 5000 is 5011, where the bound is 0.5489. The bound
   first reaches 0.5 at p = 4441.
4. **"With certainty" assumes an exact QFT_p and exact phase oracles.** With approximate gates, each certainty
   becomes 1 − O(N_op·ε) by the hybrid argument, so ε = 1/(100·N_op) suffices. This adds a log(1/ε) factor to the
   "O(log² p) gates" per operation. Say so, and cite the source; it is from memory here too.
5. **A missing output file.** `structure_check.out`, cited in §2, is not in the folder. I re-ran `structure_check.py`
   (stdout only): 30 configurations, 0 mismatches.
6. **Scope wording.** F23 is a **promise** result: H is hard cyclic (η ∉ γ_2). The labelled-copy input follows exactly
   from the standard oracle (§5), but arbitrary H in free23 is not covered. Every summary should say "hard cyclic".
   That includes the brief's phrase "a cover-free algorithm for the HSP in free23".
7. **Lemma C, minor.** "Such a u′ exists unless some D_l = 0" is a sufficient condition, not a characterization: for
   a smooth conic, D ≠ 0 suffices. The bound 3/p is unaffected.

## 1. Lemma 0: structure and closed form (PROVED)

**Structure.**
1. Let λ ≠ 0 and f(e) ≠ 0. In fil4_λ = G/ker λ, put N_λ = exp(F_p g_0 + γ_2)/ker λ.
   * N_λ is normal, because it contains [G,G].
   * N_λ is abelian, because λ([g_0, Z]) = 0.
2. exp(x x′)·H·exp(−x x′) is a complement of N_λ. Hence every coset gH equals n·H for some n ∈ N_λ.
3. Write exp(xη′) = exp(ν(x))·exp(x x′) with ν(x) ∈ log N_λ. Then the copy is
   Σ_x ω^{(twist)}|n·exp(ν(x)), x⟩.
4. The QFT over N_λ, with outcome y, gives ω^{−ỹ(ν(x))}, up to a global phase that depends on the base point.
5. Only one l-sector carries weight. My code finds l = +1 in every one of 662 non-spoiled copies. This is the
   target's l = −1, with the opposite orientation of ω.

**Closed form.** `symbolic_lemma0.py` checks f(e)·(−jν_{g_0} − kν_z + λ(ν_{γ_3})) = A_1x + A_2x² + A_3x³ over
Q(λ, x′, η, j, k, x), using the exact class-3 BCH. The difference is 0.

**True-state checks** (`check_lemma0.py`, `check_lemma0.out`). Each copy is built as follows:
* a coset state on ℂ[G] with a uniform base point;
* the label sampled from its exact law;
* for half the copies, a random automorphism σ applied as a permutation of ℂ[G];
* my own front end.

| p | non-spoiled copies matching the closed form | sign conventions that fit all copies | base-point independence (fixed H) |
|---|---|---|---|
| 5 | 82/82 | 1 of 8 | 76/76 |
| 7 | 168/168 | 1 of 8 | 166/166 |
| 11 | 275/275 | 1 of 8 | 284/284 |
| 13 | 137/137 | 1 of 8 | 140/140 |

The fitting convention is (global sign −1, (j,k) → −(j,k)). That is the FFT orientation, and it was then asserted on
every non-spoiled copy of the end-to-end runs (§4).

**New observation: spoiled copies (f(e) = 0).** In 78/78 spoiled copies across p = 5–13:
* the x-state is a single delta at a point x_0;
* x_0 is a critical point of the cleared phase: A_1 + 2A_2x_0 + 3A_3x_0² = 0.

Consequence (sketch, **CONDITIONAL**):
* A spoiled copy's along-e expansion in Lemma L is cs·q′(x_0) = 0 at order τ, and 0 at orders τ², τ³. This is the
  truth: the copy does not move.
* The level-2 state is supported on a line parallel to e.
* So spoiled copies appear harmless. The end-to-end runs agree: all 113 spoiled runs that reached the QFT gave correct
  equations (§4).
* To prove this, Lemma C's uniformity of r would also need redoing for spoiled triples. There, r and the level-2 coset
  outcome are correlated.
* If it were proved, the |B|/(p+1) term would disappear, and p_0 would fall from 5000 to a small constant. F23 does
  not need this.

## 2. Lemmas W, B, E, C, R and L (re-derived; checked)

**Lemma W, Claim 1 (PROVED; re-derived by hand and symbolically).**
1. Per copy, the (S)-tensor is t(a; b, c) = 3A_3(a)f(b)f(c), which is a multiple of ℓ(a)m(b)m(c), with ℓ = det(x′,·)/n
   and m = λ·.
2. Its part outside Sym³ is (2/3)[t(e;w,w) − t(w;e,w)]. Using ℓ∧m = −det, this equals −(1/3)·det(e,w)·(λ·w).
3. The constant −1/3 is universal: it is independent of λ and of the chart x′ (`symbolic_lemmaW.out`).
4. Summing with the weights u_j³s_{ji}³ gives the obstruction −(1/3)det(e,w)·(Σ_j u_j³P_3(T_j))·w.
5. This is zero iff Σu³P_3 = 0. Q_3 is then unique, because a symmetric trilinear form is determined by its values
   e·∇q(w) (p > 3).

**Lemma W, Claim 2 (PROVED).** The e_3-part of A_2 is (n/2)e_3. It contributes
(e_3/2)Σu²s²n·f(w) = (e_3/2)(Σu²P_2)·w.

**Lemma W, numerical check** (`check_lemmaW_B.py`, `check_lemmaW_B.out`).
* Both "iff"s were tested in 180 configurations at p = 101, 1009 and 10007, with m = 6 and 36. The weights were
  random, cubic-only solutions, or quadratic-only solutions, so both directions occurred. There were 0 failures.
* With Lemma-B weights at p = 101, 103, 1009 and 1013 (both residues mod 3), Q_3 existed and was unique, and E3 held,
  in 40/40 cases.

**Lemma B (PROVED; re-derived).**
* **One equation.**
  * Pigeonhole on F_p^*/F_p^{*3}, using that −1 is a cube.
  * For d = 2: the affine conic c_1x² + c_2y² = −c_3 has p ± 1 points, and each x carries at most 2 of them, so a
    random x succeeds with probability ≥ (p−1)/(2p).
* **Two equations.** If Σ_{i∈b}(w_i^{(b)})^d c_{i,0} = 0 and Σ_b e_b^d C_b = 0, then v_i = e_b w_i^{(b)} gives
  Σv^d c = 0. v ≠ 0 because the supports are disjoint.
* **Level 2.** u = Σ_k c_k v^{(k)} has disjoint blocks, so Σu²P_2 = Σc_k²·0 and Σu³P_3 = Σc_k³A_k = 0.
* **Genericity.** Lemma B uses none: every case, including zero columns, is handled.
* **Checks.** My own solver was run on 2700 adversarial column sets (all zero, constant, one-sided, ±1 entries,
  random) at p ∈ {5, 7, 11, 13, 19, 31, 37, 101, 103}, with 0 failures. The worst case for d = 3 at p ≡ 1 mod 3
  (three cube classes plus one) is solved.
* **Attribution.** This is IS's "(d+1)^m" recursion (IS intro, l. 123 of the local text). IS make it deterministic
  through van de Woestijne; the Las Vegas version here is weaker but sufficient.

**Lemma L, Lemma E and the level-3 algebra (PROVED; my derivation agrees).**
* B_l(w,e) = Σu²s²f(w)(A_2 + 3A_3X) is the polar form of the e-dependent quadratic part, evaluated at (w,e). Its
  e_3-part vanishes by E3.
* The level-3 condition is Σu′²B_l + R̃ ≡ 0, with R̃ symmetric. That is one antisymmetric condition, the conic.
* The cubic terms of the offsets are killed by T(d,·,·) = 0. The quadratic terms of the offsets give 2u′B_l(w_l, e),
  which is public and linear in e.
* The η_c-part of μ is Σu·P_1(η_c) = 0.

**Lemma C0 and Lemma C (PROVED).**
* D_l depends on r_j through u_js_{j1}r_j. For non-spoiled triples, r_j is uniform and independent of the coset
  outcomes, because the plane states have flat modulus.
* So Pr[D_l = 0] = 1/p, given non-spoiled copies. This is all that s(p) uses.
* The closed form of C0, in my convention −Σu s(nX + k), matched in every level-2 state of §4 (0 failures).

**Lemma R (PROVED).**
* Since L is free, the automorphisms are exactly the pairs (y_0, y_1) that are independent mod γ_2, which gives
  |GL_2|·p⁶ of them.
* σ(η)'s γ_3-part depends on the γ_3-parts c_0, c_1 of y_0, y_1 through e_0c_0 + e_1c_1. That map is linear and onto
  F_p², so each α has exactly p² completions.
* Given (σ(H), A), α is therefore uniform on α_0 + F_p(−e_1, e_0).
* ℓ′ = (Aᵀℓ_e + ℓ_3α, det(A)ℓ_3) sweeps an affine line in ε^⊥ that misses 0 when ℓ_3 ≠ 0. Projectively it is
  uniform on p points.
* U_σ maps a labelled copy of H to a labelled copy of σ(H) whose label is λ∘σ^{−1}. In my code this label was
  asserted to be deterministic after the permutation, on every copy.
* λ′ is uniform and independent of σ. Since A is uniform, e′ = Ae is uniform on F_p² \ 0 given λ′. This gives (a)
  exactly.

## 3. Hidden H-dependence and the frozen-normalizer check (none found)

**Quotients and subgroups.**
* G/ker λ: ker λ ≤ γ_3 = Z(G), so it is normal.
* N_λ ⊇ γ_2 ⊇ [G,G]: normal and abelian. It depends on λ only.
* There is no normalizer, no G/K and no quotient by an H-dependent group anywhere.
* The level-2 and level-3 coset measurements act on F_p-vector registers, not on group frames.
* The η_c step uses K̂, after ε is learned, through left cosets only (fix 2).
* So F23 does not make the CLASS_THREE draft's error ("Do not form G/K if K is not normal in G", draft l. 121).

**Public choices.**

| choice | depends on |
|---|---|
| charts x′, g_0 | λ′ (plus public coins; my code uses random charts) |
| weights u | P_2, P_3 of λ′ |
| M | I |
| Q_3 | λ′, s, the outcomes y |
| B_l, c_l, D_l, R | λ′, y, r, the coset outcomes |
| u′ | c, D |
| σ | uniform and independent |
| the set B | λ′ of the level-2 supports |

* In my simulation, the truth enters only through assertions and diagnostics.
* Labels are not conditioned. Unlike `theorem_pipeline.py` (which conditions labels on H's special line; documented
  there), spoiled copies occur freely: 721 of them in §4.

**Theorem R.** F23 lies in exit (ii) of the 11-12 note §8, through the non-central QFT over N_λ, so it is outside
SOT(Aut). There is no conflict, as the triples referee already found.

## 4. End-to-end exact simulation (falsification only; `e2e.py`)

**What is simulated: the full Algorithm A, unconditioned.**
* One fixed hard H per experiment. All copies come from H, with independent uniform base points.
* Per run:
  * a fresh uniform σ, applied to every dense copy;
  * 3 level-2 states with m = 9g_3² triples, Lemma-B weights, true front ends, exact S and coset sampling, Q_3, the
    Lemma-C choice of u′, R;
  * a QFT over F_p², with z sampled from |FFT|² of the true state;
  * the pullback.
* Per attempt:
  * two runs and the cross product;
  * the η_c step on true copies, with Fourier over K̂ through the transversal of fix 2;
  * verification by exact phase-estimation pass probabilities on 2 fresh copies.

| p (m) | attempts | **success** | wrong output | no output: C forced 0 / proportional | equations correct | runs with a spoiled copy in the supports | mass on the predicted line (unspoiled runs) | copies per attempt |
|---|---|---|---|---|---|---|---|---|
| 11 (36) | 40 | **37/40 = 0.925** | 0 | 2 runs / 1 pair | 78/78 | 79/80 (602 spoiled copies) | ≥ 1 − 3e−16 | 867 (formula 18m/q_adm + 4 ≈ 874) |
| 7 (144) | 15 | **9/15 = 0.60** | 0 | 6 runs / 0 | 24/24 | 23/30 (60 spoiled copies) | ≥ 1 − 2e−16 | 4217 |
| 13 (144) | 10 | **9/10 = 0.90** | 0 | 0 runs / 1 pair | 20/20 | 17/20 (59 spoiled copies) | ≥ 1 − 1e−16 | 3327 |

**Reading.**
* Every failure is a "C forced 0" run or a proportional pair. Both are accounted for in s(p).
* No wrong equation, and no wrong candidate, ever occurred.
* At p = 7, C was forced to 0 in 6/30 runs, against the bound 3/p = 0.43.
* The p = 11 rate is far above the theorem's bound, which is vacuous at p = 11: |B| = 12 = p + 1. That is because
  spoiled copies did no harm (§1).
* Lemma 0 was asserted on every non-spoiled front end of these runs (an assertion failure would abort the run).

**Verification and brute force** (`check_verify.py`, `check_verify.out`; exact pass probabilities on true copies).

| candidate | pass probability |
|---|---|
| correct ĥ | exactly 1 (200/200 at p = 5 and at p = 7) |
| ĥ ∉ K | exactly 1/p |
| ĥ ∈ K \ H | 0 or 1 depending on λ, mean 1/p over λ (observed 0.160 at p = 5 and 0.130 at p = 7) |

At p = 5, all p³(p+1) = 750 hard cyclic candidates were tested:
* the unique correct one passes with probability 1;
* the wrong ones average 0.2016, with 1/p = 0.2;
* the union bound with v = 6 copies is (p+1)/p³ ≤ 2/p².

## 5. Probability and copy accounting (PROVED; numbers recomputed)

**Input model.** From the standard oracle, a coset state followed by the γ_3 character measurement gives
ρ_{Hγ_3, χ_λ}, with λ uniform because H ∩ γ_3 = 1. That is the target's input exactly: χ_λ(exp(tη_V)c) =
ω^{λ(c) − tλ(η_c)}.

**Success per attempt.** s(p) ≥ (1 − 3N_T/(p+1))²(1 − 3/p)²(1 − 1/p).
* The product form is legitimate for three reasons:
  * the two runs use independent σ and independent copies;
  * the C ≠ 0 event is bounded conditionally on non-spoiled labels, as Lemma C requires;
  * the proportionality event is bounded conditionally on both runs having ℓ_3 ≠ 0, with α uniform and independent
    of everything else.
* Recomputed values: 0.5483 at 5003 (N_T = 432) and 0.8735 (N_T = 108). So 0.452 = 1 − 0.548 is a valid failure
  rate for every p ≥ 5000.

**Final error.** Pr[no correct candidate in R attempts] ≤ 0.452^R, and Pr[some wrong candidate passes] ≤ R/p², since
a wrong candidate passes 2 independent copies with probability ≤ p^{−2}. Hence the error is ≤ 0.452^R + R/p².

**Copies.**

| p | q_adm | 18·144/q_adm | 18·36/q_adm |
|---|---|---|---|
| 5003 | 0.99940 | 2593.6 | 648.4 |
| 11 | 0.745 | | 870 (observed 867 per attempt) |

The target's "≤ 2600 + 4" and "≤ 650 + 4" are right.

**Brute force (p < 5000).**
* There are p³(p+1) candidates, each tested on 6 fresh copies.
* The error is ≤ (p+1)/p³ ≤ 2/p².
* The cost is 6p³(p+1) = 3.75·10¹⁵ copies at p = 4999, the largest prime below 5000.
* It is cover-free and "useless in practice", as the target says.

## 6. Citations from memory and what Route A avoids

| citation | used by | Route A? |
|---|---|---|
| Heintz's Bézout inequality and "linear images do not raise degree" | Lemma G3 | **avoided** |
| Hartshorne III Ex. 5.5 (complete intersections of positive dimension are connected) | Lemma G1(5), and hence geometric irreducibility | **avoided** |
| Weil bound (genus 73), Lang–Weil, zero-dimensional solving | Lemma G4 | **avoided** |
| Approximate QFT over Z_p for prime p (Kitaev, Hales–Hallgren, Mosca–Zalka), and the hybrid argument that errors add (Bernstein–Vazirani; Nielsen–Chuang §4.4) | both routes | **not avoided**. Every HSP algorithm over F_p needs it. Standard, but write it down (fix 4) |
| Las Vegas square and cube roots (Tonelli–Shanks, Adleman–Manders–Miller, or Cantor–Zassenhaus) | Lemma B, and the level-3 conic point | not avoided. Textbook (e.g. Bach–Shallit) |
| Lemma 0 | both | now proved here (§1) |

**Route B (not needed for F23).** I checked G1's incidence count: the rank is |J| + 3, with exactly one Euler
dependency, and the dimensions are 23 < 24. I also checked the genus, 73 (K = O(4), 2g − 2 = 144), and G4's
fibre-counting constants: (1 − 146/10⁴)/36 ≈ 0.0274. They are consistent. Its proved constants rest on the
memory citations above, so Route B stays **PROVED given cited theorems (memory)**.

## 7. Claim gates and next question

**Gates.** These stay false until human review: "exit (ii) closed", "the cover is unnecessary for free23 (hard cyclic
H)", and novelty or priority. Internal drafts `BOUNDED_CLASS_METABELIAN_HSP.md` and `CLASS_THREE_HSP_THEOREM_DRAFT.md`
remain unadjudicated. I read only greps of the second. It uses a different mechanism (the full γ_2 label, then DHIS
phase linearization), and its relation to F23 is UNKNOWN.

**Next hard question.** Prove that spoiled copies are harmless (Lemma 0′ plus a spoiled-triple Lemma C). That would
give F23 with p_0 = O(1).
* Next command: `python check_lemma0.py 17 400 6`, extended with an exact analytic statement of the spoiled block.
* Acceptance test: a written proof that y(Ad_{exp(x_0x′)}η′) = 0 ⇔ q′(x_0) = 0, and, in e2e, 0 wrong equations over
  ≥ 200 spoiled runs.

## 8. Adversarial self-check

* **Shared code with the target?** None. My group code, front end, Lemma-B solver, Q_3 and B solves, conic and
  η_c step were written from the definitions. The sign convention was fitted (1 of 8 conventions), not assumed, and
  only one fits.
* **Could the end-to-end run pass vacuously?**
  * Mass on the predicted line, computed with the true θ, was 1 to 1e−15. Every pulled-back equation was tested
    against the true ε.
  * The verification probabilities are exact.
  * A wrong Q_3 sends the mass to ≈ 1/p: this is the triples referee's negative control, not re-run here.
* **Small primes.** p ≤ 13, so this is falsification only. The theorem's proved regime, p ≥ 5000, was not simulated.
  The lemmas are polynomial identities whose proofs do not depend on p beyond p > 3.
* **Spoiled-copy harmlessness** is an observation with a sketch only. I do not promote it. F23's bound does not use
  it.
* **Not done:**
  * exact gate counts;
  * a full reading of the two internal drafts;
  * any external literature search (no network);
  * only 10 attempts at p = 13 (18 min).
* **Overclaim risk.** "PROVED WITH FIXES" means a written AI proof, re-derived and checked by a second AI. It is not
  human-refereed, and it moves no STATE row by itself.

## Reproduce (folder `2026-11-13-rees-free23-theorem-referee/`; python = /opt/anaconda3/bin/python, all under nice -n 19)

```
python check_lemma0.py 5 100 2; python check_lemma0.py 7 200 3; python check_lemma0.py 11 300 4; python check_lemma0.py 13 150 5   > check_lemma0.out   # ~10 s
python symbolic_lemma0.py > symbolic_lemma0.out; python symbolic_lemmaW.py > symbolic_lemmaW.out         # ~2 s
python check_lemmaW_B.py > check_lemmaW_B.out                                                                                         # ~1 s
python check_verify.py 5 200 1; python check_verify.py 7 200 2   > check_verify.out                                                   # ~10 s
./queue.sh    # e2e.py 11 40 101 > e2e_11.out (8 min); e2e.py 7 15 202 > e2e_7.out (2 min); e2e.py 13 10 303 > e2e_13.out (18 min); < 0.35 GB RSS
```

Acceptance:
* every Lemma-0 line matches with exactly one convention;
* both symbolic outputs are 0 and −1/3;
* there are 0 Lemma-W/B failures;
* the SUMMARY lines show wrong_output = 0, C0_closed_form_fail = 0, verif_reject_correct = 0, and
  run_holds = run_ok.
