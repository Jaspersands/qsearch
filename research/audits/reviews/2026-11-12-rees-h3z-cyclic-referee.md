# Hostile referee of Theorem C′ (cyclic case of HSP(H_3(Z))) (2026-11-12)

**Status: AI-checked by one hostile-referee Claude Code helper session, pending human review.**
No API agents, no git, no network. No existing file was edited; the proof note is unchanged.
Claim gates (`speedup_claim_allowed`, `novelty_established`) stay false. No novelty, priority
or speedup claim is made.

* Target: `2026-11-12-rees-h3z-cyclic-proof.md` (the "proof note") and its folder.
* Background read:
  * `2026-11-12-rees-h3z-infinite-index.md` §§0–4 (the "II note");
  * `2026-11-12-rees-h3z-qzs-attack.md`;
  * `2026-11-12-rees-h3z-qzs-referee.md` (fixes G1–G3).
* My checks are in `2026-11-12-rees-h3z-cyclic-referee/`. They run with
  `nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python`. Every finite check can only falsify
  (TRAPS 7).

## Verdict

**Theorem C′: CORRECT WITH FIXES. It is PROVED given cited theorems, and I found no GAP.**

I re-derived every lemma of §§2–5 line by line. I also checked the group-law algebra in sympy
and checked the physical-state Gram law against brute-force group-element lookups.

* **No step fails, and no hidden average-case assumption was found.** The only randomness the
  proof uses is the algorithm's own: ρ is exactly uniform for every coset of every H, plus the
  coset law and the measurement outcomes. Lemma D holds for every X in its box and every
  offset sequence α, and C1(iii) holds for every α.
* The design change, decoding only the direction and then going abelian in A_v, removes the
  anti-concentration problem completely. Nothing is circular: no step needs h before it is
  found.
* **Six fixes, all presentational or bookkeeping.** None changes an algorithm parameter.
  * F1: the derivation of the c-bound in §0 is false for negative k. The bound itself still
    holds.
  * F2: the "repeat until success" loops need explicit caps.
  * F3: "certified generator" needs Shor factoring as a required import, not an optional one.
  * F4: one line of the b₂ step in Lemma D's proof is misstated. The conclusion holds.
  * F5: the period-finding constant needs an explicit run count.
  * F6: the power-of-2 rounding is inconsistent with `common.params`.
* The QZS referee's fixes are all incorporated:
  * G1, the window drift: it is the 2P|μ|Mb term in D_i.
  * G2, primitivity: it holds automatically for prime q, and Lemma 2.3 uses it.
  * G3, generation: the prime-by-prime certification handles it.
  * C4′, two-interval segments: the square-box preparation avoids it.
* **What stays open before any STATE row moves:**
  * a human read of C1(ii) and Lemma D;
  * a source check of Rosser–Schoenfeld (RS) and LLL (recalled, not re-read, TRAPS 10);
  * a **prior-art search** (not done by the note or by me; no network);
  * a check that ePrint 2026/2678 §10 problem 5 is posed in this access model (signed box,
    known b). Theorem A also carries uncomputed Kuperberg constants (B = poly(b)).

## Table

| # | Item | Verdict | Fix / evidence |
|---|---|---|---|
| 1 | Lemma 2.1: exact preparation, ρ uniform and independent of the coset, chirp state | CORRECT | Distinct π-points give P(ρ) = 1/N₀ exactly, on good *and* bad cosets. Part 2 checks this: an explicit QFT on 7 h gives max \|P(ρ) − 1/N₀\| = 3e-19 and chirp phase error 8e-16. |
| 1 | Lemma 2.1(1): V and P(bad) ≤ V/R | CORRECT (wording) | "per coset" should read "per factor". The variation is ≤ Δc + C(Δ,2)ab + pΔb ≤ V. Part 2: 0/3000 violations of spread ≤ V. |
| 1 | Lemma 2.2: exact Gram law with absolute-window drift; 0 off K | CORRECT | sympy: yk⁻¹ = gh^{t−τ}z^{s−σ}, and the increment is τc + C(τ,2)ab + p₁τb (Part 1). Brute-force lookups agree with the closed form to 7e-14 on 210 (τ,σ) pairs, and k ∉ K gives exactly 0 (Part 2). 1 − A ≤ \|τ\|/\|I\| + max\|δ\|/N: 0 violations. |
| 1 | Lemma 2.3 and support = Zw iff gcd(μ₁,μ₂)=1 | CORRECT | sympy: the σ identity and the δ_μ endomorphism hold as polynomial identities (Part 1). The control μ = (2,2) for w = (2,2) gives a cross-line overlap of 0.90; primitive μ gives exactly 0 (Part 3). |
| 1 | Theorem C1(ii): TV ≤ η + 2V/R | CORRECT | The reference state, the line-wise orthogonality, ‖Ψ−Ψ*‖² ≤ 2Σ(1−A_i) + 4π²Θ′²S², Jensen, and TV ≤ ‖Φ−Φ*‖ all re-derived. The S, σ, δ bounds are re-derived, including D_i = 4.5μ²Mb² + 2P\|μ\|Mb. E[1/\|I\|] is checked by exact line counts for 9 adversarial w: ratio ≤ 0.875 against the 1.1 used (Part 4). Part 3 runs 7 toy instances from explicit physical states: TV ≤ ‖Φ−Φ*‖ ≤ √(pointwise analytic bound) in all of them. |
| 1 | C1(iii): strip mass ≤ 2^{-7} + 2^{-14}; fiber uniformity | CORRECT | The Fejér tail sum, the fiber count Mb·g, L_r ≤ Mb/g, and #lines ≤ 2^{b+1}Mb are re-derived, and Σ_y P* = 1 is checked. The bound holds for every α. |
| 1 | α known exactly; N₀ ≥ 2R; Mb \| N₀ | CORRECT | α = (Σρ_iC(μ_i,2) mod N₀)/N₀ is integer arithmetic. The inequalities hold for b = 1..200 (Part 4). |
| 2 | Lemma P′ ≥ 0.22 (Parseval overlap, second moment) | CORRECT | P(E_q), λ(A_q∩A_q′) ≤ 4ε² + 1/(3qq′), the discretisation 3q/N₀ and the 4.03 ratio are re-derived. Worst case over b = 1..200 is 0.228. |
| 2 | Rosser–Schoenfeld usage | CORRECT, recalled | The inequalities used are π(x) > x/ln x (x ≥ 17) and π(x) < 1.25506x/ln x (x > 1), RS 1962 Cor. 1 (3.5), (3.6). These are the right ones for π(2Q) − π(Q), and they give 0.732 at the worst b. **Robust:** RS Cor. 3 [recalled], π(2x) − π(x) > 3x/(5 ln x), still gives 0.224. A human should confirm against the source. |
| 2 | θ_i exactly uniform and independent; enumeration cost; Markov cap | CORRECT | E#(Λ∩B) ≤ 1 + 41.8 ln ε^{-2}. The box/count ratio ≤ 20³ is re-derived (LLL Prop 1.6). After the cap the success is 0.178 ≥ 0.17. Conditioning on SDA success conditions only on ρ, so the coset law is unbiased. |
| 3 | Lemma D (direction decoder) | CORRECT WITH FIX (F4) | Proof re-derived. The b₂ line "λ₂ ≤ 2^{(n−1)/2}R_t" is not what is needed. Apply LLL Prop 1.12 to {b₁, true vector}: this gives ‖b₂‖ ≤ 2^{(n−1)/2}·max(‖b₁‖, R_t) ≤ 2^{n−1}R_t = ρ_max, which is the stated conclusion. \|ω(w,w′)\| < F holds at both stages, and the bound is vacuous-safe anyway. |
| 3 | "0.875 < 1" no-wrap | CORRECT for **all** b | 2^{12}·7·2^{-2b-19}·2^{2b+4} = 7/8 exactly; b cancels. B₃ = 2^{2b+3} is a valid bound, since the true \|X₃\| ≤ 2^{2b} + 2^{b+1} (Part 1, exhaustive at b ≤ 4), so there is slack. |
| 3 | Union terms ≤ 2^{-18} and ≤ 2^{-43}; p_bad | CORRECT | Analytically monotone in b: (c + 2^{-b})²(8c + 2^{-2b})(1 + 2^{7−b})⁴·const. Numerically the maximum is −18.08 at b = 1. The float log flattens near b ≥ 54; this is rounding, not a non-monotonicity. Stage-2 p_bad = 0.0044 at b = 1 (Part 4). |
| 3 | Stage 2: ι homomorphism, exact P*_0, wrong-v soundness | CORRECT | sympy: ι is a homomorphism. A wrong v gives H ∩ A_v = 1, so no r ≥ 1 is accepted. |
| 3 | Certification "output generates H" | CORRECT WITH FIX (F3) | If some r passes, then H ⊆ A_v and ℓ ∈ Zℓ̂ (ℓ̂ primitive), so prime-by-prime reduction ends at g and h_out = h^{±1}. This needs the factorisation of ĝ < 2^{2b+2}, i.e. **Shor factoring as a required import**. Without it the output is only "in H, a generator w.h.p." |
| 3 | Period-finding constant "≥ 0.99 after O(log log 2^b) runs" | CORRECT WITH FIX (F5) | The constant is not derived. The fix uses a constant number of runs: per lcm pair, P(both good, gcd(j₁,j₂,g)=1) ≥ (4/π²)²·6/π² ≥ 0.097, so 48 disjoint pairs (96 runs) give ≥ 0.99. |
| 3 | H = 1 detection; circularity | CORRECT | For H = 1, no r is ever accepted, so the output is "H = 1" with certainty. ρ is uniform for single-point cosets too, so stage 1 still terminates. No parameter or step uses h. |
| 4 | Parameters explicit, O(b) bits; box; gates | CORRECT WITH FIX (F2, F6) | 0 failures of 13 inequalities over b = 1..200, and max TV/η_s = 1.86 ≤ 2 (Part 4). B(b) is linear (278, 369, 441, 1163 at b = 1, 6, 10, 50). F2: "repeat until SDA succeeds" and Tonelli–Shanks need caps. F6: P, N, R are not rounded to powers of 2 in the code; round P up first, then compute R, N, N₀. |
| 4 | Total error | CORRECT WITH FIX | ε/2 (statement) and ε/4 (proof) are inconsistent but harmless. With caps, per-batch ≥ 0.93 − 4·0.83^{C_s}. |
| 5 | Quantifiers: every H, worst case | CORRECT | See the verdict. decode_sim's random h is evidence only. My adversarial runs (Part 5, `adv_pipeline.py`) all pass. |
| 0 | §0 "\|c\| < 2^b + 2^{2b−1}" | WRONG (derivation), conclusion OK (F1) | Counterexample: b = 3, h = (−7, −7, 56) with generator h^{-1} = (7, 7, −7) gives \|c\| = 56 > 40. The true bound is \|c\| < 2^{2b} + 2^b < 2^{2b+1}, so the stated promise \|c\| < 2^{2b+1} holds. |
| 6 | decode_sim rerun | reproduced | b = 6, seed 4242: 200/200, control 0/100. b = 10, seed 4243: 200/200, control 0/100. Run times 87 s and 112 s. |
| 6 | Adversarial tests (mine) | no failure | See §2 below. |

## 1. Re-derivations (the parts that carry the theorem)

**C1.** Write ψ(gh^tz^s) = e(−θs)/√(|I|N) on its support s ∈ [−c_t, N − c_t). Then
⟨ψ|R_kψ⟩ for k = h^τz^σ equals e(θσ)·#{(t,r) : t, t−τ ∈ I, r, r−δ_t ∈ [0,N)}/(|I|N), with
δ_t = σ + τc + C(τ,2)ab + p_{t−τ,1}τb. This is exactly Lemma 2.2, including the drift term the
QZS referee called G1.

* With x_i(u) = δ_{μ_i}(σ(u)) and u′ = u + tw, one gets
  x′x⁻¹ = h^{μ_it}z^{−μ_i²S + C(μ_i,2)tX₃} (sympy), so Σθ_iσ_i = −ΘS + αtX₃ exactly.
* If u′ − u ∉ Zw, then gcd(μ₁,μ₂) = 1 makes some x′x⁻¹ fall outside K, and the overlap is
  exactly 0.
* So Φ* (the line-wise phase-corrected copy of Φ) has the Fejér law P*_α exactly, and
  ‖Φ−Φ*‖² = Mb^{-2}Σ_u(2 − 2ΠA_i cos 2πΘ′S). Everything after that is bounding, and each bound
  checks:
  * |S| ≤ 2.5Mb²;
  * |σ_i| ≤ 3.5μ²Mb², using Mb ≥ 2^{2b+3};
  * max|δ| ≤ D_i;
  * E[1/|I|] ≤ #lines·(2R+2V)/(8P²R(1−V/R)) ≤ 1.1|w|_∞/P.
* No step needs a property of h beyond |a|, |b| < 2^b and |c| < 2^{2b+1}.

**C3.** Lemma Q is three lines and exact. In Lemma P′ the only external input is the prime
count.
* The Parseval overlap is λ(A_q∩A_{q′}) = Σ_j ĝ(jq′)ĝ(jq) ≤ 4ε² + 1/(3qq′).
* Discretisation costs ≤ 3q/N₀, since each A_q-interval meets at most 3 A_{q′}-intervals.
* With S₁ ≥ 2·0.68·1.89 = 2.57 and E Z² ≤ S₁ + 4.03S₁², we get P(Z > 0) ≥ 0.226.
* The prime-q primitivity argument (q ∤ k ⇒ ν = μ/k ∈ Λ and is shorter; q | k ⇒ |μ| ≥ q) is
  correct.

**C2.** Lemma D's E-event argument is sound.
* Conditioned on α_k and on the fiber value, ⟨y_k,w′⟩ mod F is uniform on a coset of a subgroup
  containing ω(w,w′) ≢ 0. So each sample passes w.p. ≤ 2γ′ + |ω|/F, and samples are independent
  given α.
* Under E, every vector of norm ≤ ρ_max has X′ ∈ Qw × Z. b₁ ≠ 0 in X′ because ρ_max < Den.
* The b₂ case closes by the no-wrap inequality, which is 7/8 for every b.
* Only the direction is read, so wrong candidates (λw, X′₃) are harmless. That is why no
  anti-concentration of α is needed.
* Stage 2 is the exact abelian law, and its soundness is set-theoretic: H ∩ A_v ≠ 1 ⇒ H ⊆ A_v
  for primitive v, since H is cyclic.

## 2. Computations (falsification only)

| Part | What | Result |
|---|---|---|
| 1 (`part1.out`) | sympy identities: power formula, δ_μ endomorphism, Lemma 2.3, Lemma 2.2 increment, yk⁻¹, ι, kX₃ = 2c_k − k²ab. Exhaustive c- and X₃-bounds at b = 2..4 | all differences 0. The §0 claim fails at b = 3, 4 (F1); max \|X₃\| = 15, 63, 255 ≤ 2^{2b} + 2^{b+1} |
| 2 (`part2.out`) | physical preparation by explicit QFT; brute-force Gram against Lemma 2.2 | errors 3e-19, 8e-16, 7e-14; 0 violations; off-K overlap 0; V bound 0/3000 |
| 3 (`part3.out`) | toy end-to-end physical Φ (Mb = 4) with brute-force Gram, 7 h including a = 0, b = 0, w = (2,2), plus a non-primitive control | all inequalities hold; cross-line 0; the control's cross-line overlap is 0.90 |
| 4 (`part4.out`) | constants: no-wrap, union terms b ≤ 400, p_bad, Lemma P′, enumeration, 13 parameter inequalities and TV budget b ≤ 200, E[1/\|I\|] geometry | all as claimed (table above) |
| 5 (`part5.out`) | real sizes b = 6, 10; 12 adversarial h × 5 α modes (SDA, 0, 1/2, 1/N₀, uniform) × 20; stage-1 decoder vs my independent Lemma-D implementation; stage-2 extremes | 1200/1200 correct directions at each b. Proof decoder and mine never disagree. Stage 2: 120/120 at each b. The sampler is exact at fiber gcd 16 and 32. |
| `adv_pipeline.py` (`adv_pipeline_b10.out`) | the full decode_sim.trial pipeline on 10 prescribed worst-case h at b = 10, among them g = 512, g = 1023 (composite, which exercises certification), \|c\| ≈ 2^{2b}, X₃ = 0, v = (1023, −1022) | 100/100, all at the first batch |
| reruns | `decode_sim.py 200 4242 6 6`, `200 4243 10 10` | 200/200 each; controls 0/100 |

The adversarial α modes matter for Lemma D's claim "α_k arbitrary". α = 0 forces the b₂ branch,
since (0,0,1)·ω₃ is then a short vector, and that branch was exercised without failure. Two rows
of Part 5 go *outside* the true promise (|c| up to 2^{2b+1} + 2^{2b}, so |X₃| ≈ 2^{2b+2.6}) and
still pass. This is consistent with the slack in B₃.

None of these tests touches C1 at real sizes. C1 is tested only at toy size (Part 3 and the
note's c1_explicit), where the analytic bounds are loose. The real-size simulation samples the
ideal law P*_α. C1 at real sizes rests on the analytic proof alone.

## 3. Replacement text (do not apply without the integrator; the proof note is unchanged)

* **F1 (§0, line 36–37).** Replace the parenthesis with: "re-derived: H = ⟨h⟩ has a generator
  set element h^k (k ≠ 0) with entries < 2^b. Then |a|, |b| < 2^b, and kX₃ = 2c_k − k²ab gives
  |X₃| < 2^{b+1} + 2^{2b}. Applying this to whichever of h^{±1} has k > 0 gives
  |c| ≤ 2^b + 2^{2b−1}, hence |c| < 2^{2b} + 2^b < 2^{2b+1} for both h and h^{-1}.
  (Counterexample to the bound for the other sign: b = 3, h = (−7,−7,56).)"
* **F2 (§1 Stage 1, line 56; §3).**
  * Replace "Repeat (a)–(c) until SDA-ISO′ succeeds" with "Repeat (a)–(c) at most
    C_s = ⌈ln(64T/ε)/ln(1/0.83)⌉ times; if none succeeds, abort the batch".
  * Add: "Tonelli–Shanks is run with at most ⌈log₂(64T/ε)⌉ non-residue trials; failure aborts
    the batch."
  * Per batch the success is then ≥ 0.93 − ε/(16T), and the cost is worst-case polynomial.
* **F3 (§1 line 78, §4 lines 342–347, §6 lines 416 and 426–427).** Make Shor factoring a
  required import:
  * "For each prime p | ĝ (ĝ < 2^{2b+2}, factored by Shor's algorithm) …";
  * in the cited list, "Shor factoring (required for the certified-generator guarantee)".
  * Keep "without factoring, h_out ∈ H always, and it is a generator with probability ≥ 1 − ε"
    as a remark.
* **F4 (§4 Lemma D proof, line 316).** Replace "The true vector is independent of b₁, so
  λ₂ ≤ 2^{(n−1)/2}R_t and ‖b₂‖ ≤ ρ_max" with "b₁ and the true vector are linearly independent,
  since their X′ projections are (0,0,D₁) and (w, X₃). LLL Prop 1.12 gives
  ‖b₂‖ ≤ 2^{(n−1)/2}max(‖b₁‖, R_t) ≤ 2^{n−1}R_t = ρ_max".
* **F5 (§4 lines 340–341, §6 line 434–435).** Replace the period-finding sentence with: "Run 96
  period-finding instances in 48 disjoint pairs. Each pair yields lcm(r₁, r₂) = g with
  probability ≥ (4/π²)²·(6/π²) ≥ 0.097 (Shor; Mosca–Ekert), so g is accepted with probability
  ≥ 0.99."
* **F6 (§0 line 44, §5 lines 404–405).** "Round P up to a power of 2 first. Then set
  R = 2^{⌈log₂(10P²/η_s)⌉}, N = 2^{⌈log₂(16D/η_s²)⌉} with D computed from the rounded P, and N₀
  last. Rounding up only shrinks every error term." `common.params` does not round P, N or R.
  Its bit sizes are unaffected to within one bit.
* **Error constants (§6 line 418 vs 436).** Use one budget:
  * stage 0: ε/4;
  * batches: 0.07^T ≤ ε/4;
  * caps: ε/16.
* **Lemma 2.1 (line 89).** "per coset" → "for each factor".

## 4. What still needs a human

1. Rosser–Schoenfeld 1962 Cor. 1 (3.5), (3.6), or Cor. 3, against the paper (recalled; the
   proof survives with 0.6).
2. LLL 1982 Props 1.6 and 1.12 as used (standard; recalled).
3. A line-by-line read of Theorem C1(ii), especially the size-biased E[1/|I|] and the
   reference-state step, and of Lemma D.
4. **Prior art.** Search for quantum HSP algorithms for the discrete Heisenberg group /
   UT_3(Z) with infinite cyclic hidden subgroups, and for "auxiliary modulus" solutions of
   θ₁μ₁² + θ₂μ₂² ≈ 0. Neither the note nor I searched (no network).
5. Whether ePrint 2026/2678 §10 problem 5 is stated in this access model: a signed coherent box
   of exponent B = poly(b), b known, left cosets. The "all subgroups" claim also inherits
   Theorem A's imports: Kuperberg Thm 1.5/7.1 with uncomputed P_K, and Lemmas 7.6/7.16 not
   verified line by line.

## 5. Adversarial self-check

* **Did I just accept the note?** I tried to break it in the places most likely to hide an
  error:
  * the physical state versus the ideal law (Parts 2–3: brute-force group-element lookups, not
    the note's closed-form r-sum);
  * the Gram sign conventions (sympy);
  * worst-case h (Part 5 and the pipeline);
  * adversarial α (Lemma D claims arbitrary α);
  * the c-bound (exhaustive).

  The only false statement I found is the §0 derivation (F1), and its conclusion survives.
* **Is it too good?** The decisive ideas are Lemma Q (an auxiliary prime modulus) and decoding
  only the direction. Both are short and exact. I could not construct an h, an α or a parameter
  regime inside the promise where a step fails. That is not proof (TRAPS 7). The proof is the
  analytic chain, and I re-derived each link.
* **Where I could be wrong.**
  * C1 at real sizes is checked only analytically. My toy checks have Mb = 4 and |μ| ≤ 3, so
    they test algebra, not asymptotics.
  * The E[1/|I|] counting uses "≤ 2R + 2V cosets per line". I re-derived it but did not
    brute-force the size-biased law at a nontrivial R.
  * Lemma D's conditioning on fiber values assumes the ideal law is applied after α is fixed.
    That is right for this algorithm, since ρ is measured first, but the TV transfer then needs
    the 4 samples to be conditionally independent given all ρ's. They are, because they use
    fresh cosets.
  * The RS and LLL statements are recalled.
* **Model risk.** The signed box and the known b are inherited from the II note. Theorem C′ says
  nothing outside that model.
* **Not claimed:** that the survey problem is solved; novelty; a speedup. Theorem C′ is
  "PROVED given cited theorems, CORRECT WITH FIXES by one AI referee, pending human review and a
  prior-art search". Claim gates stay false.

## Files

All in `2026-11-12-rees-h3z-cyclic-referee/`:
* `referee_checks.py` (Parts 1–5);
* `part1.out` … `part5.out`;
* `adv_pipeline.py`, `adv_pipeline_b10.out`;
* `rerun_b6_seed4242.out`, `rerun_b10_seed4243.out`, `rerun_times.txt`.
