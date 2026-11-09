# fb: proof check of the classical-filter and circuit-backend appendices

Checker `fb`, 9 November 2026. AI-only check (Claude Code), not human review, not Lean.

## Header

**Scope.** Every line of `T/appendix-filters.tex` (lines 1-49: `prop:conjugation`, the Luks paragraph, `rem:filters`, the filter paragraph, `app:filters-applications`) and of `T/appendix-backends.tex` (lines 1-47: `app:backends-control`, `-arith`, `-coherent`, `-instances`, `-scope`).

Cited material I read: `T/main.tex` 66-80 (status convention), 161-388, 730 (header of `prop:triangular-sde`), 794-1034 by label (`thm:uniform-compilation`, `lem:qft-mod`, the three coherent witness lemmas, the backend paragraph l. 858, `tab:backends`), and 1413 and 1490 (grep); `T/appendix-provenance.tex` 90-171 and 237; `T/appendix-schedule2.tex` 78-84 (definition of `E_2`) and 370; `T/references.bib` 138 and 306.

Code, read only: `theorems/rees_coherent_sde_kappa.py` 120-300, `theorems/rees_circuit_coherent_k3.py` 1-182, `theorems/rees_circuit_general.py` 251-300, `theorems/rees_circuit_arith.py` 910-950, `formal/Formal/ReesMergeReduction.lean`.

One `grep` over `T/*.tex` printed a single label line of `T/main-full-draft.tex`. I did not read that file or use the line.

| file | shasum |
|---|---|
| `T/appendix-filters.tex` | `fc8a2ac43259e4b763ee85c5e421e8e930b56159` |
| `T/appendix-backends.tex` | `020a873804d10f895c46de144c15f2f7b042a968` |
| `T/main.tex` | `0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4` |
| `T/appendix-provenance.tex` | `2545e44aeb3ff7f97a204932c46f20ac8c77ec62` |
| `T/appendix-schedule2.tex` | `8abf0e08ebeb059ba862bf7b0c905e38b1ae3624` |
| `T/references.bib` | `25bcc17522c9c7d9a976d221b9398e5aad21511d` |

**9 November changes.** `O/diffs/patch9nov-main.tex.diff` changes neither file, and it changes no statement they cite. Lines 95, 107, 217 and 312 of the diff mention `lem:qft-mod` or `app:backends-arith`, but only as context lines.

**Verdict: MINOR ONLY.** No stated result is affected.
- Finding 1 is at the ERROR level: a scope sentence gives an incomplete list of conditions.
- Findings 2-12 are MINOR.
- No counterexample to any proposition, cost claim or count was found.

**Compute.** About 4 core-minutes, at `nice -n 19` with a timeout, one job at a time. Scripts and outputs are in `O/fb/`. Every script imports the repository read-only.

## Findings

### 1. ERROR: the scope sentence lists too few conditions (`appendix-backends.tex:47`, `app:backends-scope`)

The text says:

> "Apart from the programs of rees_circuit_coherent_k3.py described in the preceding paragraph, whose output law is uniform on hh^⊥ conditionally on Lemmas homogeneous and central, Proposition descent and exact transforms, …"

In the paper's convention, "conditionally on X" means proved assuming X. The proof that the preceding paragraph (l. 45) gives also assumes three further things:
- **Unproved macro and comparator correctness.** The two written witness-circuit arguments assume that the two arithmetic macros and the comparator are correct on canonical words. This is checked exhaustively only for `p ≤ 127` (for κ = 2 the text cites `p ≤ 13`) and `b ≤ 12`. The sentence covers every emitted program, `p ≤ 2·10^6` included.
- **Argued structure.** The shape, footprint and wiring properties are argued: they are read off the generator code.
- **Prop `triangular-sde`.** The witness lemmas `lem:coherent-quadratic-sde` and `lem:coherent-power-sde` are labelled "conditional on Proposition triangular-sde" in their headers.

Referee 5 (I11) flagged this same pattern, conditionality dropped in a summary sentence, at other places. If the macros are in fact correct for every `p`, the sentence is true, but it is not proved as stated.

Proposed replacement for the clause:

> whose output law is uniform on $\hh^\perp$ conditionally on Lemmas~\ref{lem:homogeneous} and~\ref{lem:central}, Propositions~\ref{prop:descent} and~\ref{prop:triangular-sde}, exact transforms and the assumptions of that paragraph (the written witness-circuit arguments, the correctness of the arithmetic macros and of the comparator on canonical words, checked exhaustively only for $p\le127$ and $b\le12$, and the argued shape, footprint and wiring properties),

### 2. MINOR: the generator's running time is understated (`appendix-backends.tex:45`, `app:backends-scope`)

The text says "its classical generator, including the search for its constants, is not shown to run in time polynomial in $\log p$". As implemented, it is known not to:
- Every backend `Config` builds `Encoding(p)` (`theorems/rees_circuit_general.py:251-264`, l. 292), whose minimal-test tables cost about `p^3` operations.
- I re-measured this: 0.06 s at p = 61, 0.59 s at p = 127, 4.77 s at p = 251. Each step's time ratio (8.9, 10.0, 8.1) matches the cube of the p ratio (7.6, 9.0, 7.7). Script `O/fb/encoding_time.py`, output `O/fb/encoding_time.out`. The gh-check measured 49 s at p = 509.
- Extrapolated, the sentence "For $p\le2\cdot10^6$ it emits one for every Lie algebra …" describes runs of about 10^12 s each. It is a statement about the generator's output, not about runs that were made.

Proposed replacement:

> and its classical generator is not polynomial in $\log p$: its encoding tables alone take about $p^3$ operations, so the coverage statement for $p\le2\cdot10^6$ describes the programs it would emit, not runs that were made.

### 3. MINOR: status labels and ranges disagree with the convention (`main.tex:74`: "argued" means the proof is given only in a source)

- **(a) `appendix-backends.tex:45`.** The correctness proofs of the κ = 2 and κ ≥ 3 witness circuits are given only in source reports. The provenance items `prov:gc-kappa2-proof` and `prov:gc-kappa-proof` call them "argued". The text says "the proof is written from …" and "proves", with no "argued". Fix: insert "argued;" after the item reference in both parentheses.
- **(b) `appendix-filters.tex:49`.** The text tags "A randomized classical algorithm computes it … (proved)" and "item (0) … applies (proved, given [Luks])". Their proofs are only in the source: `prov:cl-app4` says "proved in the source". Line 9 says the application searches are "argued, not proved here". Fix: write "(argued; proof in the source of item~\ref{prov:cl-app4})". Alternatively, add the short proof, which I re-derived:
  - s ↦ F(u+sAu) has degree at most δ̂, so δ̂+1 values give (A·R_F)(u).
  - A nonzero A·R_F vanishes at a uniform point with probability at most δ̂/p < 1/2.
  - O(d + log 1/ε) points then give the kernel with error at most ε.
- **(c) `appendix-backends.tex:4`.** The status line points to "items prov:gc-control–prov:gc-kappa2-proof". It omits `prov:gc-kappa-proof`, cited at l. 45, and `prov:gc-qft-mod`, cited at l. 16. Fix: "items~\ref{prov:gc-control}--\ref{prov:gc-kappa-proof}; Lemma~\ref{lem:qft-mod}: item~\ref{prov:gc-qft-mod}".
- **(d) `appendix-backends.tex:45`.** The same two macros are said to be checked exhaustively "for $p\le13$" (κ = 2 sentence) and "for $p\le127$" (κ ≥ 3 sentence). State one range, assuming they are the same `add_product` and `add_scaled` macros (`MACRO_KINDS` in `rees_circuit_coherent_k3.py`).

### 4. MINOR: the example variable is indexed wrongly (`appendix-filters.tex:36`, `rem:filters`(i))

The text says "for $F = x_{D-2}$ under $\UT_D(\Fp)$, $\dim W = 2$ and $\ker\rho_W$ has index $p$". This holds only if the variables are numbered from 0. The paper numbers them $x_1,\dots,x_D$ (l. 49), with the action $F\mapsto F(g^{-1}x)$ and $g$ upper unitriangular:
- With 1-based indexing, $x_{D-2}$ gives $\dim W = 3$ and index $p^3$.
- $x_{D-1}$ gives $\dim W = 2$ and index $p$.

Exact check at p = 3, D = 4, 5, with both actions: `O/fb/orbit_kernel_check.py`, output `O/fb/orbit_kernel_check.out`. The source note's example (`x_2` under `UT_4(F_3)`, cited-notes report l. 346) is right with 0-based indexing. With 1-based indexing it holds only for the transposed action, and only at D = 4.

Fix: "for $F = x_{D-1}$ under $\UT_D(\Fp)$ acting by $F\mapsto F(g^{-1}x)$".

### 5. MINOR: the merge identity is attributed to the wrong section (`main.tex:1413`, `main.tex:1490`, `appendix-provenance.tex:237`)

All three places say "the merge identity … of Section~\ref{sec:uniform-compilation}". The identity and `ReesMergeReduction` are stated in `app:backends-instances` (`appendix-backends.tex:38`). The section `sec:uniform-compilation` (`main.tex` 794-1034) mentions only "merges via the Schur-product channel" in `tab:backends`.

Fix: "of Appendix~\ref{app:backends-instances}" in all three places.

### 6. MINOR: the hypothesis of the general symmetry statement is too weak (`appendix-backends.tex:25`, "Two symmetry lemmas")

The text says "… segments that act on it, on the states reached, as right translations by values held on other wires". The proof compares two runs: the original and the left-translated one. So the translation property is needed on the states reached from the translated input too, not only on the states of the original run.

The application is unaffected, because the text checks the instruments and merges as translations "on every input". The general statement should still say so. Fix: "on every state reached from any left translate of its input".

### 7. MINOR: one control-only claim omits the final transform (`appendix-backends.tex:23`, "Monolithic simulation")

The text says "After the preparation of $Q$ the labels and $Q$ are used only as controls". This is false for the final readout transform on $Q$. The next sentences treat that transform through the Gram matrices, and l. 25 does say "up to the final transform". Fix: "After the preparation of $Q$ and up to the final transform, the labels and $Q$ are used only as controls".

### 8. MINOR: one sentence names the wrong backend (`appendix-backends.tex:45`)

The text says "Consequently the deferred-measurement proof applies to every grade-two label tuple of the fifth backend, and the exhaustive run on all $5^{12}$ tuples over $\mathbb{F}_5$ … are controls". The $5^{12}$ run belongs to the fourth backend (`rees_circuit_coherent.py`, F_3(5), l. 25). The fifth backend is over $\mathbb{F}_7$ and has only sampled grade-two runs.

Fix: "applies to every grade-two label tuple of the fourth and fifth backends, and the exhaustive run on all $5^{12}$ tuples over $\mathbb{F}_5$ and the sampled runs over $\mathbb{F}_7$ are controls, not the proof."

### 9. MINOR: `u` is undefined, and the values of `R_F` are not stated (`appendix-filters.tex:49`)

"$t\mapsto R_F(\exp(tA)u)$" uses a $u$ that is never introduced. Also, $R_F$ takes values in $\mathbb{F}_{p^K}$: it is a $K$-tuple of polynomials over $\Fp$.

Fix: "for every $A\in\mathcal{L}$ and every $u\in\Fp^{KD}$, with $\exp(tA)$ acting on each of the $K$ coordinate blocks", and "($R_F$ is $\mathbb{F}_{p^K}$-valued, a $K$-tuple of polynomials over $\Fp$)".

### 10. MINOR: a citation is missing (`appendix-filters.tex:47`)

"The cyclotomic coset problem of Boucher, Fouque and Shen (an arXiv preprint, not checked offline)" has no `\cite`. The key `BoucherFouqueShen2026` exists (`references.bib:306`) and is cited at `main.tex:120`. Fix: "… Shen~\cite{BoucherFouqueShen2026} (an arXiv preprint, not checked offline)".

### 11. MINOR: the scope of "matrix p-group" (`appendix-filters.tex:29`)

"for every matrix $p$-group acting by conjugation, for every $N$ and $p$". The context is $N\times N$ matrices over $\Fp$, so the intended groups are the $p$-subgroups of $\mathrm{GL}_N(\Fp)$, which are unipotent. Fix: "for every $p$-subgroup of $\mathrm{GL}_N(\Fp)$ acting by conjugation". The scope of Luks's theorem beyond characteristic $p$ is left to the expert (see below).

### 12. MINOR: typos

- `appendix-backends.tex:9` says "read off its gate list exactly, by evaluating the gate list exactly, as integer coefficient vectors". Fix: "read off its gate list by exact evaluation, as integer coefficient vectors".
- `appendix-filters.tex:49` has "non-normal pattern subgroups", while the paper elsewhere uses "nonnormal" (referee 5, S3).

## Checked and correct

`appendix-filters.tex`
- **l. 11, exp(ad_x) against conjugation.** Checked:
  - The series exp(ad_x) is defined, since ad_x^p = ad_{x^p} (L_x and R_x commute in characteristic p) and x^p = 0.
  - It differs from conjugation exactly when N ≤ p ≤ 2N−2. The cross terms x^i M (−x)^j/(i!j!) with i, j ≤ N−1 and i+j ≥ p are distinct matrix units for the witness J_N, E_{N1}.
  - `O/fb/conj_check.py` part (c): p ∈ {2,3,5,7}, all N ≤ p, the witness predicted correctly in every case, exhaustive over n_N where |n_N| ≤ 2·10^4. 0 mismatches.
- **`prop:conjugation`, statement and proof, line by line.** Checked:
  - p-integrality of exp and BCH below degree N; exp is a bijection onto UT_N with inverse the truncated log; exp(L) is a group.
  - exp(x) − I ∈ F_p[x] and x ∈ F_p[exp x], so x and exp x have the same commutant.
  - The transporter for L = n_N is the stated linear system. It is correctly claimed only for n_N: every element of UT_N is I+X.
  - Edge cases: p = 2; N = p; proper subalgebras.
  - `conj_check.py` parts (a) and (b): brute force over G for n_N at (N,p) ∈ {(2,2),(2,3),(3,3),(3,5),(4,5),(3,7)}, 15 runs on proper subalgebras (dimension 1 to 4, p ≤ 7), and transporters at four (N,p). 0 mismatches.
- **l. 29, Luks paragraph.** Conjugation on k-tuples is a linear action of dimension kN², so a vector stabilizer in a p-group gives the stabilizer. Logic correct given the citation.
- **`rem:filters`(0).** Reduction of ρ(g)v, or of a subspace stabilizer, to Luks: logic correct given the citation.
- **`rem:filters`(i).** diag(g, ρ_W(g)) is faithful and fixes (0, e_F) iff g·F = F. Correct. For the example see finding 4.
- **`rem:filters`(ii), the 2-jet facts.** At a G-fixed anchor, H preserves every homogeneous part of the Taylor expansion, so K ⊇ H and K = 1 implies H = 1. Proved here, correct.
- **`rem:filters`(ii), first-order linearization.** Sufficiency of p > max(D, (D−1)Δ) re-derived:
  - deg_t F(exp(tA)x) ≤ (ν−1)Δ < p;
  - exp(sA)exp(tA) = exp((s+t)A);
  - d/dt exp(tA) = A exp(tA) when A^p = 0;
  - f′ ≡ 0 with deg f < p forces f to be constant.
- **`rem:filters`(ii), "Δ < p is not enough".** Confirmed with explicit instances for G = exp(F_p J_D). At p = 5, D = 4, Δ = 3, Fix and Ker both have dimension 4 but meet in dimension 3. So there are F fixed by G with A·F ≠ 0 (the method returns too small a group) and F with A·F = 0 not fixed (too large). The same happens at p = 5, D = 5, Δ = 3, 4 and at p = 7, D = 4, Δ = 5, 6. Script `O/fb/linearization_check.py`, outputs `.out` and `linearization_jets.out`. Linear and quadratic forms under J_D (D = 5..7 at p = 7; D = 5, 6 at p = 11) showed no failure; this corroborates the "UT_5 blocks" tests but proves nothing.
- **`rem:filters`(iii).** F_p has isotropic vectors, for example (1,2) over F_5. Correct.
- **l. 47.** (Z_{p^t}[ζ_p])^n ⋊ F_p has class t(p−1), because (ζ−1)^{p−1} = p·unit. This is at least p iff t ≥ 2.
- **l. 49, app:filters-applications second paragraph.** Checked:
  - R_F has degree at most δ(F), by Frobenius linearity of x^{p^e} on F_{p^K}.
  - Stab_G(F) = Stab_G(R_F) when p^K > deg F and δ̂ < p.
  - The first-order method is exact when p > max((ν−1)δ̂, δ̂).
  - The evaluation count O(d(d+log 1/ε)(δ̂+1)).
  - δ̂ = ⌊(p−1)/max(ν−1,2)⌋ satisfies the hypothesis.
  - Moore forms of r rows have p-weight r.
  - The fixed-δ̂ representation has dimension at most K·C(KD+δ̂, δ̂).
  - |UT_D(F_p)| = p^{D(D−1)/2}.
  - The "computed" p = 5 failures are reproduced independently (rows above).
  - `O/fb/pweight_check.py`: [A] 12 configurations of 4 algebras at p = 5 × 12 cases each (144) and [B] 3 × 60 random cases at p = 5, D = 3: the method equals the brute-force H in every case.
- **l. 49, "An instance beyond these filters therefore needs …".** I first suspected a gap for bounded p-weight δ(F) ≥ p, where the interpolation route is stated only for p > δ̂. It is covered after all: then p ≤ δ(F) = O(1), so D ≤ p is bounded and exhaustive search applies.

`appendix-backends.tex`
- **l. 9.** Checked:
  - 3 sources × c = 2 gives 6 oracle calls; 3 children × 4 passes give 12 BCH passes.
  - Heis(F_3) has 1+13+4+1 = 19 subgroups, 6 of them normal subgroups containing the centre.
  - Chevalley–Warning arity κ_d g_d + 1; the coherent arities follow `coherent_arity_k`.
- **l. 14.** 40b²+2b Toffoli gates (independent of γ) and at most 158b²+46b gates per multiply-accumulate. The closed form 134b²+50b−4+(20b−4)w+4H with w ≤ b and H ≤ b² gives 158b²+46b−4. The repository's counting mode, re-run at 11 primes up to 2^61−1, gives these Toffoli and gate bounds and 3b+5 ancillas. Script `O/fb/arith_counts.py`, outputs `.out` and `.json`.
- **l. 16.** Checked (`O/fb/backend_numbers.py`):
  - (t,r,τ) = (26,19,15) and (32,22,18) from the formulas of `lem:qft-mod`, at η = 1.5e-3 and 1.488e-3, and at 2.8e-4, 2.799e-4 and 2.5e-4.
  - 3π2^{−15} = 2.876e-4 < 2.9e-4 ≤ η/(b+3), and 3π2^{−18} = 3.595e-5 < 3.6e-5.
  - Transforms 24/6 and 148/24 from the q_max counting of `thm:uniform-compilation`(iii).
  - Per terminal sample 0.014177 and 0.011178; per run 0.09924 < 0.0993 and 0.08942 < 0.0895.
  - The coupling sentence: TV = min over couplings of the mismatch probability.
  - Qubits 154 = 82+11+61 and 835 = 744+14+77; gates per transform 7873 ≤ 8405 and 13303 ≤ 14948, the bounds of the lemma.
  - The hybrid argument with deferred measurement, and the zero-input charge, are logically correct.
- **l. 21.** κ_d ≤ 2 on both instances; arities 3 (equal to the Chevalley–Warning 3) and 6 (against 5).
- **l. 23.** 574 = 82 × 7; 729 = 3^3 · 3^3; 3^18 ≈ 3.9·10^8. Deferred-measurement use is correct; see finding 7.
- **l. 25.** Checked:
  - Both symmetry lemmas re-derived. Left translations commute with right and central translations. Untouched oracle outputs turn the address state into a mixture of coset states. Subtrees are independent until the root merge.
  - 390625 = 25·5^6; 5^12 label tuples and 25 label pairs; 5^6 or 25^6 tuples.
  - The deferred-measurement argument for every label tuple of positive probability is correct, given the stated checks.
- **l. 27.** 23×4 = 92 = 72+20 and 39 = 15+2·12 = 17+7+15.
- **l. 29.** κ_3 = 3 and κ_2 = 2 over F_7; arities 3 and 6 (against 4 and 5); 648 = 18·3·4·3; 230 transforms; 7^3·7^6 pairs.
- **l. 31.** κ = (2,3,2); arities (3,6,10) (against (3,7,7)); 10800 = 180·4·5·3; 3330 transforms; γ_2 = ⟨e3,e4,e5⟩.
- **l. 33.** 304234 − 115282 = 188952 = 24·7873 and 5035924 − 2694596 = 2341328 = 176·13303. TV 0.09924 < 0.0993 and 0.09857 < 0.0986. Same (t,r,τ) at η = 2.5e-4.
- **l. 38.** Checked:
  - Arities (2,5) and (5,3,7) are the Chevalley–Warning arities; |G_4| = 5^11.
  - 30 calls and 60 passes. 140 = 40·3 + 20·1 brackets: right-nested BCH_3 with [x,y] reused. 880 = 40·20 + 20·4 is the exact count of the unoptimised schedule of `thm:uniform-compilation`(i); its reuse bound would give 540.
  - Five of the nine subgroups are nonnormal (ideal check of referee 5's list).
  - (p^M−1)|K^⊥|^{M−1} is the exact number of pairs (λ, s) with s ≠ 0 that satisfy the witness equation; 2.98·10^17 at grade two.
  - The product identity re-derived. The Lean `merge_product_eq` has hypotheses E2 and E3 matching the described checks; slots with s_i = 0 drop out.
  - 16316 = 16302 + 14. The cubes of F_7 are {0, ±1}, so the search has 3^10 points instead of 7^10. 7^9 states for γ_2 of F_4(7) and for γ_4 of F_5(7).
- **l. 43.** No execution or speedup claim. Exact transforms are stated. The 7^7 source addresses follow from D_3 = 7. "It covers no other coherent-label circuit" is consistent.
- **l. 45.** Coverage and refusal re-run on the repository's own search (`O/fb/contraction_coverage.py`, `.out`):
  - The repository's exact search finds a normalised contraction at every p ≡ 1 (mod 3) below 3000, so E_2(3) = ∅ there. Among p ≡ 1 (mod 4) below 1100 it fails exactly at {5,13,17,29,37,53}; this is all of E_2(4), since 1100 > 4^5 = 1024.
  - κ = p−1 has none at p = 5, 7, 11, 13.
  - `ValueError` refusals at (13,4), (5,4), (17,4) and (7,6).
  - The E_2(5) and E_2(6) sets agree with the gh-check's.
  - Above 2·10^6 the α-scan cap of 10^5 raises instead of backtracking, consistent with "refuses some primes outside E_2". The gh-check observed this at κ = 6, 7.
  - The text correctly restricts the claim to p ≤ 2·10^6, cites `cor:app-s2-small`, and states "not the receiver of Theorem main".
- **l. 47.** The total-variation bounds are correctly limited to the third and seventh backends. `prop:coherent-receiver` is stated as existence only, with no generator.
- **Consistency of `tab:backends` and `main.tex:858` with the appendix.** Instances, qubits, gates, "simulated" and "counted only" columns all agree. The coherent_k3 row and the "apart from the written argument" exception are present.

## Not checked / UNKNOWN

- I did not re-run or simulate any gate list. This covers 5528 CNOTs, 231210 and 2997844 gates, 182/1198/1629/20566 qubits, every "simulated", "checked" and "agrees" statement, and the mutant outcomes. Only the arithmetic consistency of the printed numbers was checked.
- The proof of `lem:qft-mod`, its gate formula and the rotation range k ≤ max(r,τ). I used only its parameter formulas.
- The written witness-circuit proofs (κ = 2 and κ ≥ 3), the structural properties (S1)-(S6), (D1) and (D2c), and macro and comparator correctness for all p.
- That every two-level contraction can be normalised to α_0 = 1, β_0 = 0. "Refuses iff p ∈ E_2" depends on it; it belongs to Prop `triangular-sde` and Schedule 2, other checkers' parts.
- The floating-point rounding (`np.rint`) of the FFT counts in the exact search for p ≤ 2·10^6. My estimate puts the error near 10^-8, far below 0.5, but I did not write a proof.
- The source-only claims of `rem:filters`(ii) and (iii): the orbit-sum and tangent families, the p = 7 controls, the tensor-train implementation. Also the Moore gradient recognizer, the argued application search (l. 47), and the high-weight families.
- The Lean module: statements read, not built.

## For the human expert

- **Luks 1992, Theorem 3.2(5),(7).** Its numbering, its exact statement, and whether it is polynomial time with no number-theoretic oracle for the groups used. The appendix relies on it at l. 29, in `rem:filters` (0)-(iii) and at l. 49. The uses here concern p-subgroups of GL_N(F_p), which are unipotent. The expert should confirm the theorem covers them, and whether the l. 29 sentence needs that restriction.
- **Other citations.** `IvanyosSantha2015` Corollary 8 for the t = 1 cyclotomic case; `IvanyosMagniezSantha2001` for the Lazard-ring reductions in black-box p-groups; the content of the Boucher–Fouque–Shen preprint; priority of the p-weight / first-order combination (the text says "may be known").
- **The written arguments for coherent_k3.** The written proofs of the witness circuits and the "read off the code" structure of the coherent_k3 programs are the only non-finite claims of the backend appendix, and the scope sentence (finding 1) rests on them. A reviewer should decide whether macro and comparator correctness for all b should be proved; it is a standard Cuccaro-adder argument, which the gh-check sketched.
- **The coverage sentence.** Whether "For p ≤ 2·10^6 it emits one …" belongs in the paper at all, given that the generator cannot be run at such p (finding 2).

## Comparison with the earlier reports

**`2026-11-05-rees-companion-restructure.md`.** This is a structural record: it moved the backend prose and the classical filters into these appendices. It makes no mathematical claim about them. Its counts of labels and status words were not re-checked here. Nothing in these two files contradicts "no claim changed status".

**`2026-11-05-rees-receiver-general-gh-check.md`.**
- **Present and correct.** Its §6.1 and §6.2 replacement texts appear verbatim at `appendix-backends.tex:45` and `:47`. Its fixes are in:
  - the p ≤ 2·10^6 restriction and the `cor:app-s2-small` citation;
  - Adleman–Manders–Miller extractions counted with multiplicity, and the comparators;
  - "and the oracle calls";
  - "classical generator" rather than only the search;
  - the new item `prov:gc-kappa-proof`;
  - the consequential edits at `main.tex:858` and in the `tab:backends` row.

  I re-checked its E_2 sets, the refusals and the cap mechanism ("Checked and correct", l. 45), and its Encoding cost (finding 2).
- **Missed or weakened.**
  1. Its endorsed §6.2 text has the incomplete condition list of finding 1. It added `lem:homogeneous` but not the macro, comparator and wiring assumptions or Prop `triangular-sde`.
  2. Its Encoding finding (Θ(p^3), "polynomial in p, that is exponential in log p") was softened in the paper to "not shown to run in time polynomial in log p" (finding 2).
  3. It asked that the structural facts be labelled "argued"; that is done ("argued, same item"). The witness-circuit proofs themselves still carry no "argued" (finding 3a).
  4. Its note for the code owner is still open: the module STATUS of `theorems/rees_circuit_coherent_k3.py` (l. 66-73: `"scope": "n4(F_7) only"`, `"general_instances": False`) contradicts `appendix-backends.tex:45`. This is outside the paper, and I made no change.

**`2026-11-04-rees-referee-5-circuits.md`.**
- **Present and correct for these files.** E1 ("five of them nonnormal", l. 38; I re-checked the ideal structure of its list); I6 (l. 38); I7 (qubit conventions, l. 38); I12 (η rounding, l. 16); I15 (the label of the Instances paragraph, l. 38); S2 ("$z\leftarrow z+\gamma xy$", l. 14); S3 (no "non-normal" left in the backends file; one remains in the filters file, finding 12); and the splits L1, L4, L5, L8 and L9 (l. 16, 21, 29, 31).
- **Its numerical checks agree with mine.** One slip is in the report, not the paper: its formula "Σ_{j<d}(j+1)(j+2)/2 = d(d+1)(d+2)/6" lacks the factor (d−1) of `thm:uniform-compilation`(i). Its numbers 20 and 4 per pass, and 880, are right.
- **Not in its scope.** The filters appendix was outside its scope, so findings 3b, 4, 9, 10 and 11 are new. Findings 1-3a and 5-8 concern text added after it.
