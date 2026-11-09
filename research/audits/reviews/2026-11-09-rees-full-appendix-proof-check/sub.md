# Proof check: flat subspace symmetry sources (checker `sub`), 9 Nov 2026

An AI session (Claude) did this check; no human has reviewed it. The paper was read-only. All outputs are in `O/sub/` and in this file.

**Scope.**
- `T/appendix-subspace.tex`, all 426 lines (Appendix `app:subspace`). This covers Definitions `def:app-sub-instance` and `def:app-sub-core`; Lemmas `lem:app-sub-gram`, `-angles`, `-character`, `-antisym`, `-growth`, `-lcu`, `-design` and `-lift`; Propositions `prop:app-sub-ray` and `-stream`; Corollaries `cor:app-sub-cancel` and `-two-lifts`; Theorem `thm:app-sub-hsp`; and Remarks `rem:app-sub-multiple-p`, `-profile`, `-sharper` and `-scope`.
- `T/main.tex` lines 1341-1402 (Section `sec:subspace`). This covers Theorem `thm:subspace-source` and its proof, the four steps, Corollary `cor:subspace-hsp`, Remark `rem:mixed-source` with the paragraph after it, and the budget paragraph.
- Read where cited:
  - main.tex 103-160, 161-388 and 397-431 (`thm:rees-cover`, `lem:homogeneous`);
  - main.tex 495-507 (`lem:copy-lift`), 609-642 (`sec:recursion`, `lem:hybrid`) and 654-657 (`thm:is-import`);
  - main.tex 1128 (the profile row of the query table, for the dimensions g_d);
  - numbers.tex 135-149;
  - the provenance items `prov:bb-subspace`, `prov:bb-mixed`, `prov:bb-subspace-profile`, `prov:sub-main` and `prov:sub-profile`.

**shasum.**

| File | shasum |
|---|---|
| `appendix-subspace.tex` | `f8553ee2c6474d9daa36b12716a9d8ac46d3ad35` |
| `main.tex` | `0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4` |
| `numbers.tex` | `c7e587fbc60d3c4a24b95db17c69f8537aefef92` |
| `appendix-provenance.tex` (named items only) | `2545e44aeb3ff7f97a204932c46f20ac8c77ec62` |

**Diffs.** `O/diffs/appendix-subspace.diff` changes wording in four places: the status line, "float check" becoming "finite computation" twice, and the provenance pointer in Remark profile. None of them changes a statement. The 9 Nov `main.tex` patch does not touch lines 1341-1402.

**Verdict: GAPS (fixable; statements survive).** There is one GAP, F1. One complexity sentence is false for a design that the corollary itself offers, and a one-phrase fix repairs it. Everything else is MINOR. I found no counterexample to any lemma, proposition or proof step. Every number I recomputed reproduces: the leak values, the falsifiers 1.732 and 1.902, the tail bounds and the whole profile.

**Compute.** About 10 core-minutes. Two early runs of `check_stream_profile.py` were stopped because their exact loops were too slow, then rerun with smaller exact loops. Only the final output is used. The finite checks can only falsify; none is offered as proof.

**Scripts.** All in `O/sub/`, each with a matching `.out`:
- `check_lcu_leak.py`: antisymmetrizers, growth, the LCU branches, the off-domain distance, and the leak without recovery.
- `check_lift_heis.py`: the ray stabilizer, the character, the cancellation and the lift on Heis(F_3) and Heis(F_5).
- `check_designs_chars.py`: Lemma design (a)-(c), with exhaustive row choices, and Lemma character on filiform groups. Exact arithmetic.
- `check_stream_profile.py`: tails of the streaming preparer, the profile numbers, Remark sharper, and the rounding identities of Remark mixed-source(i).

## Findings

### F1. GAP: polynomiality needs a design of polynomial size, but the corollary offers S = F_p^× with M = p-1

**Location.**
- `main.tex:1380`, Corollary `cor:subspace-hsp`.
- `appendix-subspace.tex:360` and `:380`, the preamble and part (iii) of Theorem `thm:app-sub-hsp`. The proof of (iii) is at `:402`.

**Problem.** The corollary takes "a public certified zero-moment design S of M points". In its parenthesis it says "for p ≥ c+2, Lemma (a) gives S = F_p^× deterministically". It then sets T = MℓB_leaf and says: "For fixed c this is polynomial in m, log p, r, q, 1/δ and log(1/ε)". For S = F_p^×, M = p-1. The raw-copy count T(N+1) ≥ T ≥ p-1 is then exponential in log p.

Theorem `thm:app-sub-hsp`(iii) makes the same claim for every certified design S of size M. Its proof covers less: "take the design of Lemma (b), so that M ≤ (c+1)! is constant". The statement survives when M ≤ (c+1)! (Lemma (b)). More generally it survives for any design whose size M is polynomial in the listed parameters, since every count is polynomial in M (T is linear in M, and N grows like log M).

**How it arose.** check-app-c P5 (3 Nov) fixed only the proof of (iii). Referee 11, item I5 (4 Nov), then added the F_p^× option to the corollary's parenthesis.

**Fix.**
- In `main.tex:1380`, replace the last sentence of the corollary with: "For fixed $c$ and $M \le (c+1)!$ (the design of Lemma~\ref{lem:app-sub-design}(b)), this is polynomial in $m$, $\log p$, $r$, $q$, $1/\delta$ and $\log(1/\eps)$, plus $rT$ times the gate cost of one controlled-$R$ call at precision $\eps/(16rT)$; it is not polynomial when $r$ is exponential in $q$. For a general design the counts are also polynomial in $M$; with $S = \Fp^\times$, $M = p-1$, they are not polynomial in $\log p$."
- In `appendix-subspace.tex:380`, replace "The number of copies and the gate count are therefore polynomial in" with "With the design of Lemma~\ref{lem:app-sub-design}(b), the number of copies and the gate count are therefore polynomial in". After "$\log(1/\eps)$" add "(for a general design, also in $M$)".

### F2. MINOR: in the main proof of (i), the phase is undefined for g ∉ H

**Location.** `main.tex:1363`.

**Problem.** The proof says "$R(g)^{\otimes r}\Omega_V$ is $\Omega_{R(g)V}$ up to the phase $\det(R(g)|_V)$". For g ∉ H, R(g)|_V maps V onto a different subspace. So det(R(g)|_V) is not defined, and the phase depends on the frame chosen for R(g)V. Proposition `prop:app-sub-ray`(a) in the appendix states this correctly.

**Fix.** Replace the clause with "$R(g)^{\otimes r}\Omega_V$ is $\Omega_{R(g)V}$ up to a phase, and equals $\det(R(g)|_V)\,\Omega_V$ for $g \in H$".

### F3. MINOR: "the inverse of the instrument's ... preparation" names the wrong operator

**Location.** `main.tex:1363`.

**Problem.** The text says "On rejection, the procedure applies the inverse of the instrument's linear-combination-of-unitaries preparation". The recovery in Lemma `lem:app-sub-lcu` is W^†. That is the inverse of the whole circuit W = (J^†⊗I) Sel (J⊗I), not of the PREPARE map J, which is what "preparation" usually means in LCU terms. Applying only J or J^† does not give the Lüders complement.

**Fix.** "applies $W^\dagger$, the inverse of the whole linear-combination-of-unitaries circuit $W$ of Lemma~\ref{lem:app-sub-lcu}, before the fresh register is discarded".

### F4. MINOR: Theorem `thm:subspace-source`(ii) uses T and β before introducing them, and says "added here"

**Location.** `main.tex:1358`.

**Problem.** B = ⌈log_2(rT/β)⌉ uses T and β, which appear only later in the sentence "Then T copies ... with probability at most β". Separately, "with the recovery step on rejection added here" asserts that the step is not in [BeneWatts2026]. The appendix (`:257`) says "whether or not [BeneWatts2026] states that recovery step", and the G1 comment says nobody has checked this.

**Fix.**
- Begin with "For $T \ge 1$ and $\beta \in (0,1)$, put ...".
- Write "made explicit here" instead of "added here" until a human reads Algorithms 1-2.

### F5. MINOR: the corollary's precision clause leaves out the growth attempts

**Location.** `main.tex:1380`.

**Problem.** The corollary says "at most $TN$ growth instruments, at most $rT$ controlled-$R$ calls, each implemented within $\eps/(16rT)$". Here "each" refers to the R calls. The precision for the growth attempts is ε/(8TN). It is measured against the exact circuit of Lemma lcu, not against G_k, which was the point of check-app-c P2. The corollary leaves this to Theorem `thm:app-sub-hsp`. That is acceptable, but a reader who applies ε/(16rT) to the growth attempts gets a total error of TN·ε/(16rT) = rBε/16, which is not small.

**Fix.** Insert "each growth attempt within $\eps/(8TN)$ of the exact circuit of Lemma~\ref{lem:app-sub-lcu}" before "and polynomial public arithmetic".

### F6. MINOR: the motivation "For r > 1 distinct cosets give non-orthogonal states" is inaccurate

**Location.** `main.tex:1344`.

**Problem.** Distinct cosets give non-orthogonal states at r = 1 as well, with overlap up to sqrt(1-δ²). What fails only when r > 1 is condition (L1) of Lemma lift for ρ itself. For h ∈ H, |tr(ρR(h))| = |tr(R(h)|_V)|/r, which is less than 1 unless R(h) acts on V as a scalar. So ρ carries no phase character on H, while Ω_V does.

**Fix.** "For $r > 1$ the copy $\rho$ is mixed: for $h \in H$, $|\tr(\rho R(h))| = |\tr(R(h)|_V)|/r < 1$ unless $R(h)$ acts on $V$ by a scalar, so one copy does not carry a phase character of $H$."

### F7. MINOR: the off-domain distance in Run 2 holds only for k ≥ 2

**Location.** `appendix-subspace.tex:395`.

**Problem.** The text says "the accept Kraus operator $\frac1{k+1}(I-\sum_j\mathrm{SWAP}_{j,k+1})$ is at operator-norm distance $k/(k+1)$ from $P_{k+1}$". This is true for k ≥ 2 (here d ≥ r > k). The computed values are 0.6667 at k = 2 and 0.7500 at k = 3 (`check_lcu_leak.out`).

Analytically, write A for the accept operator. Then A - P_{k+1} = A(I - P_k⊗I), and A commutes with P_k⊗I. On the Young basis, A has eigenvalues (1 - content of box k+1)/(k+1). Away from the sign isotypic part of S_k, the largest modulus is k/(k+1), reached at content -(k-1) with shape (2,1^{k-1}).

At k = 1, P_1 = I. The range of P_1⊗I is the whole space, the circuit equals G_1 everywhere, and the distance is 0.

**Fix.** Add "(for $k \ge 2$; at $k = 1$, $\operatorname{range}(P_1\otimes I)$ is the whole space)".

### F8. MINOR (a strengthening): the leak without recovery has a closed form

**Location.** `appendix-subspace.tex:257`; provenance item `prov:sub-main`.

**What the paper says.** It gives the values 1/2 (d = r = 3, k = 2) and 2/3 (d = r = 4, k = 3), each as a finite computation. Both are correct.

**Claim.** Both are instances of one identity. Take any 1 ≤ k < r ≤ d, any density ϱ supported in ∧^kV and any J with J|0⟩ = f. On the rejection branch without W^†, the kept k-register state has weight exactly (k-1)/k outside ∧^kV.

**Derivation.**
1. The f-identity on line 257 shows that the kept state on all k+1 registers is X = (1/L)Σ_{j=0}^{k} S_j ν S_j^† - P_{k+1}νP_{k+1}. Here ν = ϱ⊗Π_V/r, S_0 = I and S_j = SWAP_{j,k+1}.
2. The j = 0 term and P_{k+1}νP_{k+1} both lie in ∧^kV⊗V, so they contribute nothing outside ∧^kV.
3. For j ≥ 1 and ϱ = |e_I⟩⟨e_I|, tr[(P_k⊗I) S_j ν S_j] = (1/r)[(r-k)/k + k/k²] = (r-k+1)/(rk).
4. The construction is U(V)-invariant and ∧^kV is irreducible, so the same value holds for every ϱ.
5. Hence the unnormalized weight outside ∧^kV is (k/(k+1))(1 - (r-k+1)/(rk)) = (r+1)(k-1)/(r(k+1)).
6. The rejection probability is 1 - p_k = k(r+1)/(r(k+1)). The normalized weight is the ratio, (k-1)/k, independent of r and d.

**Numerical check.** All eight (d,r,k) cases with 3 random completions of J each (`check_lcu_leak.out`).

**Optional text.** "...has weight exactly $(k-1)/k$ outside $\wedge^kV$, for every $r > k$ and every retained density ($1/2$ at $k = 2$, $2/3$ at $k = 3$)".

### F9. MINOR: Remark `rem:mixed-source` has undefined symbols and two notation clashes

**Location.** `main.tex:1391-1398`.

**Problem.** β (in M_0 ≥ 8r̄/β and "≤ β/8") and ε (in "polynomial in ... 1/ε") are not defined in the remark. The one-body density γ_ψ (line 1398) clashes with γ = δ²/8 used a few lines later. J = ⌈1/w⌉ clashes with the LCU unitary J of Lemma lcu.

**Fix.** Write "for a failure budget $\beta \in (0,1)$ and a target error $\eps$", and rename γ_ψ and J.

### F10. MINOR: one sentence is duplicated

**Location.** `main.tex:1385` repeats what `main.tex:1383` already says ("Appendix ... proves a completed form ... AI-checked only").

**Fix.** Delete one of them.

### F11. MINOR (slack, not an error): b over-provisions by p^{n/2}

**Location.** `appendix-subspace.tex:364` and `:393`; `main.tex:1400`.

**Problem.** Run 1 needs only ½B_leaf p^{n/2}(1-γ)^ℓ ≤ ε/16. But b contains ⌊n log_2 p⌋, and the proof ends with "εp^{-n/2}/16 ≤ ε/16", which throws away a factor p^{-n/2} (2^{-263} at the profile). With ⌊(n/2)log_2 p⌋ in b, the same proof gives b = 1839 and ℓ = 367,800 at the profile. Keeping e^{-γℓ} as well gives about 254,700 blocks. The main text's "step (3) alone would allow about ℓ ln 2 blocks" (about 291,400) counts only the slack between e and 2. No stated count is wrong: all are sufficient bounds. This is optional.

### F12. MINOR: the gate count for Lemma lcu leaves out the sign

**Location.** `appendix-subspace.tex:244` and `:254`.

**Problem.** Sel applies -SWAP on ancilla levels 1..k. The sign costs one diagonal ancilla phase per use of Sel, or it can be folded into J. The count "2k controlled swaps" is right for the swaps themselves. This is negligible.

## Checked and correct

**Definitions and setting.**
- Definition `app-sub-instance`, and the sentence after it: H = stab V = stab ρ, and δ ≤ 1.
- Definition `app-sub-core`:
  - B_leaf = (m+t)ΠM_{d'} matches Section `sec:recursion`.
  - Under Schedule 1 the core error is at most ε_0/3 + ε_0/3.
  - The remark on other schedules (any deterministic cap on the sources consumed) is right for the hybrid.
- `eq:app-sub-interp` follows from the coefficientwise criterion in the proof of `lem:homogeneous`.

**Wedge products, angles and the ray stabilizer.**
- Lemma gram (a)-(c), re-derived: Leibniz after reindexing; X^{⊗k} commutes with P_π; the alternating multilinear expansion.
- Lemma angles, re-derived: frames adapted to the SVD, mutually orthogonal S_i, eigenvalues ±sin θ_i.
- Proposition ray (a)-(c), re-derived:
  - the converse in (a), and χ^p = 1;
  - μ ≥ TD² by Cauchy-Schwarz;
  - AM-GM and the chain down to 1-δ²/2.
  - Float checks on 6 Heisenberg instances show violations ≤ 4e-15 (`check_lift_heis.out`).

**The determinant character and cancellation.**
- Lemma character, Steps 1-4, re-derived:
  - Step 1: the subgroup form of Lazard;
  - Step 2: the e^{ad x} identity over Z[1/c'!], and the Vandermonde step with c' < p;
  - Step 3: the polynomial has degree ≤ c' ≤ p-1 in each variable, and its st coefficient is [x,y];
  - Step 4: an additive character.
  - Exact checks on filiform groups with (p,c) = (5,3), (5,4) and (7,3): associativity, the Step 2 identity, [G,G] = [L,L] as sets, and a∗b - a - b ∈ [L,L].
- Corollary cancel, and the counterexample on Heis(F_3):
  - χ = ψ_0², and χ^{1+4} = χ² ≠ 1;
  - |F-1| = √3 = 1.732 reproduced;
  - 1.902 at p = 5 reproduced, for both H = Z and H = ⟨x⟩.

**Streaming preparation.**
- Lemma antisym (a)-(c), re-derived by the coset decomposition by π(k+1). Residuals ≤ 2.2e-16 over 9 (d,r,k) cases.
- The growth instrument and Lemma growth (a)-(c), re-derived. p_k does not depend on the retained state (to 8e-17), the supports are right, and k+1 = r gives Ω_V.
- Lemma lcu, re-derived:
  - W(|0⟩⊗φ) = |0⟩⊗φ by norm saturation;
  - W^†(I-|0⟩⟨0|)W gives (I-P_{k+1}).
  - Both branches checked on random inputs in range(P_k⊗I), not only in ∧^kV⊗V, with 3 random completions of J. Residuals ≤ 1.4e-16.
  - The cost of 2k swaps, two J and two J^† is right.
- The remark on leaving out recovery: the values and their independence from the completion of J are correct (F8 gives the closed form).
- Proposition stream (a)-(c):
  - the law of the attempt count is exact;
  - it is dominated by collecting r coupons of probability 1/r²;
  - r(1-r^{-2})^N ≤ r e^{-B} ≤ r 2^{-B}, then a union bound over T;
  - the outputs are a product state on the no-abort branch;
  - the copy and instrument counts and the live memory are right;
  - the one-shot probability r^{-r} = Πp_k holds exactly for r ≤ 11.
  - Tails for r = 2..10 and B = 1..8 are all below r2^{-B}, exactly for r, B ≤ 4 and in float otherwise. The largest ratio is 0.3378, at (r,B) = (3,1).

**Zero-moment designs.**
- The design definition.
- Lemma design (a):
  - the geometric sum;
  - "a suitable e exists iff p ≥ c+2", exact for p ≤ 43;
  - the Las Vegas test: 18/42 = φ(14)/14 at p = 43.
- Lemma design (b):
  - the moments factor, M ≤ (c+1)!, and both coverage cases hold;
  - exhaustive over all row choices for p ∈ {3,5,7} and c ≤ 4, and sampled at (p,c) = (7,4);
  - at the edge case p = 7, c = 6 = p-1, one witness design has M = 5040 = 7!, p | M and 6 distinct points.
- Lemma design (c), by Vandermonde: no violation among 1602 random multisets.

**The lift.**
- Lemma lift:
  - the character part, by equality in the triangle and Cauchy-Schwarz inequalities;
  - the slot factor φ(E(b^{-1}∗a)), since E_s is a homomorphism;
  - Φ = 1 on H̃ under (D1) or (D2), and |Φ| ≤ 1-γ off H̃;
  - the passage from Frobenius norm to trace norm.
  - Checked on Heis(F_3) with H = Z, the nonnormal ⟨x⟩ and ⟨x,z⟩, at r = 2 and 3, and on Heis(F_5) with H = Z and ⟨x⟩:
    - stab(V) = H, and χ is linear;
    - |Φ-1| ≤ 7e-15 on H̃ with the designs (1,1,1,2,2,2) and (1,2,3,4);
    - σ is PSD with trace 1;
    - the exact TD lies below the bound. This last test is weak, since the bound exceeds 1 in these small cases.
- Corollary two-lifts (a) and (b).
- Remark multiple-p:
  - Φ ∈ μ_p on H̃;
  - the numbers 420411, 3,783,699 and 5,885,600;
  - the crossover p > Mℓ/c.

**Composition with the core.**
- Theorem app-sub-hsp (i):
  - The hybrid over four runs, re-derived.
  - Run 1: b > n log_2 p + log_2(8B_leaf/ε) gives εp^{-n/2}/16.
  - Run 2: the exact circuits equal G_k on the reachable domain, with the ancilla in |0⟩; β = ε/8; producing outputs just in time changes nothing.
  - Run 3: the diamond-norm hybrid with padding gives ε/8 + ε/16 + ε/16 = ε/4.
  - The total is 11ε/16 < ε.
  - Each precision clause is stated relative to the right object: the exact LCU circuit for growth, the ideal controlled R, and the ideal address state.
- Theorem app-sub-hsp (ii): the counts are right.
  - at most T(N+1) copies;
  - at most TN attempts, each with ≤ 2(r-1) swaps, 4 uses of J^{±1} and ≤ r levels;
  - at most rT controlled calls of R;
  - 2T evaluations of O(mn) operations each.
- Theorem app-sub-hsp (iii): correct with the design of Lemma (b); see F1.

**Remarks.**
- Remark profile and `main.tex:1400`, recomputed with exact integers from the formulas and g_d = (17,16,14,12,9,6,3,1):
  - t = 1, log_2 B_leaf = 1569.49, and log_2 Q_q = 1572.66, which matches the table;
  - b = 2102, ℓ = 420400, log_2 T = 1591.98;
  - B = 1598, 1600, 1602 and N = 6392, 102400, 1640448;
  - raw copies 2^1604.62, 2^1608.62, 2^1612.62.
  - The numbers.tex macros match.
- Remark sharper: no violation of its inequalities on a grid, and the factor min{r/2, 1/δ²} is right.
- Remark scope: each bullet re-derived.
  - In the diag(3/4,1/4,0) example the swap fixes the support but not the state.
  - Too large an r gives p_r = 0, hence an abort.
  - A v⊗v bank stalls at level one.
  - A projective R breaks (b).

**Main text.**
- Theorem `thm:subspace-source`(i)-(ii) and its proof, apart from F2-F4.
- Steps (1)-(4).
- Corollary `cor:subspace-hsp`, apart from F1 and F5.
- Remark `rem:mixed-source`(i) and the argued paragraph after it:
  - the rounding lands in (λ-2w, λ], and tr(ρ-ρ̃) < δ/8;
  - K ≤ r̄, and Σr_l ≤ min{r̄(r̄+1)/2, 16r̄/δ};
  - a move of more than 7δ/8 passes to one factor, and 1-(7δ/8)²/2 ≤ 1-δ²/8;
  - the number of bad offsets is at most the number of eigenvalues (exact on 60 random spectra, δ ≥ 1/4);
  - the acceptance probability is (1-k tr(ργ_ψ))/(k+1) ≥ w(r-k)/(k+1);
  - the coupon timeout bound holds.
- The four diff hunks.

## Not checked / UNKNOWN
- [BeneWatts2026], Algorithms 1-2 and Theorem 5 / Remark 6: whether they contain the recovery W^†. There is no offline copy, and network use was not allowed.
- [IvanyosSantha2015, Fact 2] (van de Woestijne): that a nonzero solution of Σ_{i ≤ j+1} x_i^j = 0 is found deterministically in time poly(j, log p).
- The core guarantee of Definition `app-sub-core`. It is inherited from Theorem `thm:main`, which the other checkers cover.
- Remark `rem:mixed-source`(ii): the threshold instrument built from density-matrix exponentiation, the rank learning, and the 78-run simulation (not rerun).
- `research/reductions/rees_subspace_source.json`: not opened. I recomputed its numbers from the paper's formulas instead.
- The status sentences "no explicit family ..." and "no quantum implementation ...".

## For the human expert
1. Bene Watts et al., Algorithms 1-2: does their growth step already apply W^† on rejection? The phrase "added here" (`main.tex:1358`, `appendix-subspace.tex:257`) depends on the answer.
2. IS15 Fact 2 / van de Woestijne, on which the deterministic design of Lemma (b) rests.
3. Definition `app-sub-core` makes every result here conditional on the core of Theorem `thm:main`. Please confirm that the core consumes a fixed number B_leaf of sources and touches them only through public operations.
4. Modelling choices: δ is a promise and is not certified; the copies are i.i.d.; r is supplied; R is linear, not projective.
5. Remark `rem:mixed-source` is argued, not proved.

## Comparison with the earlier reports
**check-app-c (3 Nov), fixes P1-P10.**

| Fix | Present now? | Right? |
|---|---|---|
| P1 (leak without recovery) | Yes, at `:257`; the header comment is updated and 0.093 is withdrawn. | Yes. F8 adds the closed form. |
| P2 (precision relative to the exact circuit) | Yes, at `:376` and `:395`. | Yes. F7 limits "k/(k+1)" to k ≥ 2. |
| P3 (outputs just in time) | Yes. | Yes. |
| P4 (O(mn) per evaluation) | Yes. | Yes. |
| P5 (design of Lemma (b) in (iii)) | Only in the proof (`:402`). | The statement of (iii) and the corollary still claim polynomiality for any design. After referee 11's I5, the corollary even offers F_p^×. This is F1. |
| P6 (Las Vegas generator for (a)) | Yes, in the appendix and main text. | Yes. |
| P7 (Remark sharper) | Yes. | Yes. |
| P8 (one-shot r^{-r}) | Yes. | Yes. |
| P9 (smaller product design, M ≤ 2Π_{j even ≤ c}(j+1) = 1890 at c = 9) | No; it was optional. | I re-derived it, including the even case c = p-1, and it is correct. Optional. |
| P10 (wording of step (4)) | Yes, through referee 11's I6. | Yes. |

**Referee 11 (4 Nov), subspace items.**
- G1 was modified and remains open; see F4 and expert item 1.
- I1 was applied; see F5.
- I2, I3, I4, I5, I6, I7, I13, S1 and S2 are applied and correct.
- Referee 11's number "⌈b ln2/γ⌉ = 291,384" is slightly off: the value is 291,400, since b ln2/γ = 291,399.07. The paper says only "about ℓ ln 2", which is right.
- Their statement that the .tex files contain "no false statement" missed F1, which their own I5 created.

**Missed by both reports:** F1, F2, F3, F6, F7, the closed form in F8, F9, F10, F11 and F12.

**Outside scope, noticed.** In `appendix-provenance.tex:338`, item `prov:sub-main` ends with "(the flat subspace source).." (a double period).
