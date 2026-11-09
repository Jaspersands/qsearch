# Rees HSP paper: unanchored adversarial check of the core (§§2–4, `thm:main`)

Item 6 of `research/REES_FULL_CAMPAIGN_4.md`. Text checked: `docs/papers/rees-hsp/main.tex` as
of 2 Nov 2026 late (integrated versions 3–4, with rows I49–I54 of the integration log), lines
233–568: §2 (Rees cover, evaluations, dilations, tuple oracle, coset copies), §3 (complete central
instrument), §4.1–4.2 (`prop:descent`, recursion, error budget, `lem:hybrid`, "Proof of Theorem
`thm:main`") and the Schedule 1 paragraph of §4.3, together with the Schedule 1 count displayed
after `thm:main` (l. 186–195). I read this text cold, wrote my own checks, and only then read
`2026-11-01-rees-core-proof-check.md` and `2026-11-02-rees-referee.md` (§7 below).

Status of everything here: **AI-checked, pending human review.** Labels: *proved* (written
argument, checked line by line), *exact* (integer or rational computation), *float* (complex
matrices compared to tolerance 1e-9), *cited* (read in the source, not re-derived).

Scripts and outputs, in `2026-11-03-rees-check-core/`:

| File | What |
|---|---|
| `check_core.py` | independent checks C1–C10. It imports nothing from the project: algebras, cover, BCH, regular representation, instrument and merge are rebuilt from the paper's definitions |
| `core_quick.json`, `core_full.json` | outputs (`--quick` skips the p = 5 dense descent) |
| `c8_flag.py`, `c8_flag.json` | Dixmier–Lister flag check (every derivation lowers the flag) |
| `sim_run.json`, `sim_run.log` | `theorems/rees_end_to_end_sim.py` (read-only), default run |
| `ext_heis.json`, `ext_heis.log` | `theorems/rees_end_to_end_ext.py heis3 heis5` (read-only), charged-arity run |

## 0. Verdict

**No counterexample.** Every statement of §§2–4 that `thm:main` uses holds, for every subgroup
H, normal or not, including H ∩ Z(G) = 1, and for every label tuple and every nonzero witness.
I tried three attacks: the quantifiers over H, the query count, and error accumulation. Only
the third found anything, and neither finding is a counterexample:

- **G1 (gap, minor to moderate: a hypothesis mismatch).** `lem:hybrid`, added as I50, assumes
  that each implemented instrument is within η_j of the ideal one in **diamond norm**, that is,
  on every input. The proof of `thm:main` gets its per-instrument error from
  `thm:uniform-compilation`(iii). That theorem only gives operator-norm error *on the canonical
  subspace* (registers holding field elements below p, with clean workspace), and it then cites
  a "restricted-domain hybrid of the note" from outside the paper. A restricted-domain bound does
  not imply the diamond-norm hypothesis. Example: V = QFT_3 ⊕ (−1) and U = QFT_3 ⊕ 1 on two
  qubits agree exactly on span{|0⟩,|1⟩,|2⟩}, but ½‖V·V† − U·U†‖_◇ = 1. So the chain
  "Thm uniform-compilation ⇒ lem:hybrid ⇒ ε/3" has a hole as written. The fix costs nothing:
  the telescoping proof only ever applies Φ̃_j − Φ_j to *ideal* intermediate states, and those
  stay canonical. So the lemma holds with a restricted-domain hypothesis, and the same proof
  also covers the note's restricted QFT hybrid. Proposed text P1–P3. This is what is left of
  referee item M3, which asked for the restricted-domain hybrid. The lemma inserted for M3 has
  the full-domain hypothesis instead.
- **G2 (gap, minor: undefined quantity).** The body never defines N_instr, and it uses
  "complete instrument" in two senses. In §3 it means one central measurement. In the budget it
  has to mean a lifted-source preparation, a whole merge node, or a final readout, because that
  is what q_max = max(n, m, max_d(2M_d g_d + D_{d−1})) in `thm:uniform-compilation`(iii) counts.
  The allocation ε/(3N_instr) needs N_instr fixed in advance. Under Schedule 1 it is fixed:
  N_instr = S(P + Σ_{d=2}^c Π_{d'=2}^{d−1} M_{d'} + 1), with S = m + t and P = Π M_d. This
  matches the count in the 11-01 envelope and in Appendix `app:free-coordinate`. Proposed
  text P2.

With P1–P3 applied, this statement holds as a written proof (AI-checked, pending human review):

> For fixed c, every prime p > c, every Lazard Lie algebra L ≅ F_p^m of class c given by
> structure constants, every subgroup H ≤ G = (L, ∗), and every ε ∈ (0,1), the Schedule-1
> procedure makes exactly c(m+t)∏_{d=2}^c B_d(g_d) oracle queries (or uses that many copies of
> ρ_H), with t = ⌈log_p(3/ε)⌉, and returns a basis of log H with probability ≥ 1 − 2ε/3. Its
> running time is polynomial in m, log p, the label width and log(1/ε). The only cited
> non-elementary ingredients are IS17 (Theorem 11 and §3.3, with van de Woestijne's solver
> inside it) and the QFT compilation of `thm:uniform-compilation`(iii).

## 1. Per-statement verdicts (§2)

| Statement | Verdict | Evidence | Smallest counterexample / fix |
|---|---|---|---|
| `thm:rees-cover`(i) cover is a graded nilpotent algebra of class exactly c, A_c central, n ≤ cm | holds | proved; C10 exact | — |
| (ii) E_s is a Lie hom, onto for s ≠ 0; δ_λ is an automorphism; E_s∘δ_λ = E_{λs} | holds | proved; C10 exact: Lie hom on all basis pairs, and E_s∘δ_λ = E_{λs} as matrices for all s, λ (Heis F_3, F_5; n4 F_5, F_7) | — |
| (iii) BCH groups; E_s and δ_λ are group homs | holds | proved (Dynkin denominators divide products of integers ≤ N ≤ c; identities in the free class-c Lie ring over ℤ[1/c!], which embeds in its ℚ-form); C10 exact: all 6561 / 390625 pairs on the Heis F_3 / F_5 covers, 4000 random pairs on the n4 covers, plus associativity | — |
| `lem:homogeneous`: fibres of f̂ = left cosets of exp(h̃), h̃ = ⊕t^k(h∩γ_k) = ∩_{s≠0}E_s^{-1}(h); subalgebra; δ-stable | holds | proved: Vandermonde times diag(s_i), with determinant ∏s_i∏(s_j−s_i) ≠ 0. h is an F_p-subspace because an additive subgroup of an F_p-space is one. C1 exact, every subalgebra: Heis F_3 19/19, Heis F_5 39/39 at points (1,2) and (2,4), n4 F_5 220/220 at (1,2,3) and (2,3,4). Each check verifies that the fibres are unions of cosets of ⟨basis of h̃⟩, that their number equals the index p^{n−dim h̃}, and that h̃ is δ-stable | **The point count c is needed**: with c−1 points the lemma fails for 13/19 subalgebras of Heis F_3 and 181/220 of n4 F_5. Smallest case: Heis F_3, H = 1, point 1 only, gives 27 fibres against index 81 |
| operational paragraph (uncompute evaluations, keep address and labels) | holds | proved | — |
| `prop:single-evaluation` | holds | proved, using u = s·tz − t²z; C2 exact: all (H, s, λ ≠ 1), 38 + 468 + 2640 cases, every one agrees with "γ_2 ⊆ h" | — |
| Heisenberg F_3 example after it | holds | δ_2(t²z) = 4t²z = t²z mod 3, and E_1(δ_2 u) = z | — |
| Dixmier–Lister paragraph (§2.3) | holds for 5 ≤ p ≤ 23; the "every p > 3" part is cited | exact (C8, `c8_flag.py`): Jacobi holds; LCS dims (8,4,2); cover dim 14; derivation space of dim 12 with system rank 52 = 64 − 12 mod each p ∈ {5,7,11,13,17,19,23}; every basis derivation maps L → [L,L] → span(e7,e8) → 0, so D³ = 0 for every derivation by linearity. The "divide by the gcd of degrees" step is proved | the 32 integer row certificates for all p > 3 are in an artifact; I did not re-run them |
| `lem:copy-lift` | holds | proved, with tr(ρ_H R_g) = 1_H(g); C4 float: all 19 subalgebras of Heis F_3, every entry of the 81×81 output | — |
| `prop:refresh` and its C_p counterexample | holds | proved (twirling); C5 float, p = 5: both marginals I/p, invariant under twirls, and the two-target lift gives the all-1/p matrix, not I/p | — |

## 2. Per-statement verdicts (§3)

| Statement | Verdict | Evidence | Note |
|---|---|---|---|
| Π_λ are orthogonal projectors summing to I | holds | C3 float | — |
| `lem:central`: label law |K|/|Z| on K^⊥, 0 off it; ρ_λ formula; tr(ρ_λR_g) = χ_λ(z) for g = hz, independent of the decomposition | holds | proved: (hz)g = 1 forces g^{-1} ∈ HZ, and the |K| decompositions all carry the same character because λ ⊥ K. C3 float, on the Heis F_3 cover (81-dim), every subalgebra (19/19): law, Πρ_HΠ/pr = ρ_Hπ/pr = the printed formula, and the trace formula for all 81 g. C3 on the Heis F_5 cover (625-dim): 39/39 for law, state and trace formula | no transversality, no normality and no basis of K are used: confirmed. The trace value is χ_λ(z) with g = hz, which is the sign the descent proof needs |
| "H ⊇ Z ⇒ only λ = 0" | holds | follows from the law | — |

## 3. Per-statement verdicts (§4)

| Statement | Verdict | Evidence | Smallest counterexample / fix |
|---|---|---|---|
| setting of §4.1 (uniform *superposition* on Q; s_i = 0 consumed; δ_0 never applied) | holds | — | the 11-01 wording fix (superposition, not maximally mixed) is in the text |
| `prop:descent`: for every positive-probability label tuple and every nonzero witness, the output is exactly ρ_{HZ/Z} | holds | proved: the entry is (1/|Q|)∏_i tr(ρ_{λ_i}R_{δ_{s_i}(g)}) with g = σ(r)^{-1}σ(q); δ(HZ) = HZ, δ_s(hz) = δ_s(h)·s^d z, and the product of the χ_{λ_i}(s_i^d z) is χ_{Σs_i^dλ_i}(z) = 1. C3 float, Heis F_3 cover, every subalgebra, every label triple in (K^⊥)³, every nonzero s ∈ F_3³ with Σs_i²λ_i = 0: **3198/3198 exact**. On the Heis F_5 cover with M = 2 it is **3912/3912 exact** for all 39 subalgebras. Non-witnesses: 5616 of 6084 give a wrong output. The other 468 are all from H = 1, where HZ = Z and the g that occur are trivial, so any s works; that count is exactly 702 − 234 | — |
| the hypothesis "δ_s preserves H" is necessary (why the cover is needed) | confirmed | C3b float: descending on Heis F_3 *itself* with its grading dilation (s, s, s²), for the non-homogeneous H = ⟨x+z⟩, gives a wrong output for 72 of 234 witness tuples | — |
| "output does not depend on the record ⇒ conditioning on record events keeps i.i.d. copies; correlated banks excluded" | holds | proved: the joint state of all (record, output) pairs factorizes because the output is the same for every record | — |
| `rem:product-channel` | holds | SUM(χ_a ⊗ χ_b) = χ_{a−b} ⊗ χ_b checked by hand; at p = 5, a = 1, b = 4 the output character is 4 | — |
| recursion (§4.2): A^{(d)} is δ-stable; Z_d is central of rank g_d; δ_s acts on it by s^d; H_d is homogeneous; K_d = t^d(h∩γ_d); a_d ≤ g_d; H_dZ_d/Z_d = H_{d−1}; terminal group tL with hidden subgroup th | holds | proved. A^{(d)} kills grades > d, so [A_i, A_d] ⊆ A_{i+d} = 0. log(H_dZ_d) = h_d + Z_d because Z_d is central; its image is the sum of the grades below d. The project's exact sim confirms every intermediate state on n4 F_5 (below) | — |
| "basis of h gives generators of H" | holds | proved (Lazard, subgroup form; I54 now says so) | — |
| rank bullet: Pr[fail] ≤ 1/((p−1)p^t) ≤ ε/3 | holds | exact (C6): 880 cases, p ≤ 11, m ≤ 8, four values of ε, every e = dim h^⊥ ≤ m, all within the bound; the largest ratio is 0.9999994, so the bound is tight | — |
| solver bullet (Markov cap) | holds; unused by Schedule 1 | proved; it needs T to bound the expected time on every instance, with fresh coins per attempt | — |
| approximation bullet | **gap G1 + G2** | see §0 | P2 |
| `lem:hybrid` | holds as stated (standard telescoping), but its hypothesis is stronger than what `thm:uniform-compilation`(iii) supplies | proved; the example V = QFT_3 ⊕ (−1) in §0 | P1 (restricted-domain form, same proof) |
| Schedule 1 paragraph: arity B_d(a) = G(d,a)^{⌈log₂(d+1)⌉}, deterministic for every column tuple, the κ_d reduction, B_κ ≤ B_d | holds (cited + exact) | cited: read in `2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`. The κ_d reduction by a positive t with td ≡ d′ mod (q−1) is IS17 §3, start. Theorem 11 is G(d,m) = d^{d(d−1)/2}(m+1)^d vectors in deterministic polynomial time. §3.3 iterates it ⌈log₂(d+1)⌉ times and ends with van de Woestijne's z_1^d+…+z_{d+1}^d = 0. Unused columns get weight 0, so M ≥ B_d is enough. Exact (C7): B_k(a) ≤ B_d(a) for all k ≤ d ≤ 12 and a < 60, with B_1 = a+1 | — |
| query count after `thm:main`: c(m+t)∏B_d(g_d) ≤ C_c c(m+t)(m+1)^{Σd⌈log₂(d+1)⌉}; exponent 145 at c = 9 | holds | exact (C7): no violation for c ≤ 7, all nonincreasing profiles with g_d < m ≤ 11, t ∈ {1,2,5}; exponent at c = 9 is 145 = `\ReesClassNineQueryExp`. The ext run charges and spends exactly c·S·M_2 = 2·7·64 = 896 queries per run on Heis F_5 (S = m + 4 there, M_2 = B_2(1) = 64), 14/14 runs | — |
| "Proof of Theorem `thm:main`" (I51) | holds modulo G1, G2 | each sentence checked against the lemmas above; the total is 2ε/3 | P3 |

## 4. The three requested attacks

**(a) Quantifiers over H.** Nothing in §§2–4 uses normality of H, a basis of K = H ∩ Z, or
transversality. My checks enumerate *every* subalgebra: 19 (Heis F_3), 39 (Heis F_5) and 220
(n4 F_5), most of them non-normal, many with H ∩ Z(G) = 1 (for example ⟨x⟩, ⟨x+z⟩ and
⟨e2+e4⟩). Others have H ∩ Z(G) = 1 while K_d ≠ 0 on the cover, such as ⟨e3⟩ in n4, where
e3 ∈ γ_2 is not central. One subtlety is real but harmless. The descent hypotheses concern the
*cover's* centers Z_d = t^dγ_d, not Z(G), so K_d can be nonzero even when H ∩ Z(G) = 1. The
paper states everything in terms of K_d, which is correct. Edge cases H = 1 and H = G: H = 1
gives labels uniform on all of F_p^{g_d}, and descent is then exact for *every* nonzero s, which
explains the 468 cases above. H = G gives only λ = 0, any nonzero s is a witness, and the
terminal samples are all 0, so the nullspace is L. Both are correct.

**(b) Query count.** S = m + t samples, each from P = ∏_{d≥2} M_d lifted sources at c queries
each. Under Schedule 1 there are no retries: the solver is deterministic and total, and retries
in any case reuse saved labels. The count is therefore exact, not just an upper bound, for the
procedure as written with M_d = B_d(g_d). The (m+1)-power bound, C_c and the exponent 145 are
exact computations. One wording point needs no change: the Schedule 1 paragraph says the
reduced solver uses only B_{κ_d}(g_d) columns. The proof feeds B_d(g_d) and gives the rest weight
0, so the displayed count is what is spent. The ext artifact runs the combined rule, which
spends B_{κ_d}, so it is not a check of the B_d count. It does check that queries = charged
arity × c × S.

**(c) Error accumulation.** The rank third holds and is tight (C6). The solver third is zero.
The approximation third has the gaps G1 and G2. I checked the other assumptions of the budget:
- no division by small branch probabilities, because exactness holds branch by branch;
- no retries consume quantum sources;
- the oracle is exact;
- the classical records are diagonal, since measurements write them, so dephasing in
  `lem:hybrid` costs nothing;
- the controlled right actions are exact reversible permutations (Toffoli arithmetic), so a
  merge node's only approximate parts are its 2M_dg_d transforms and its D_{d−1}-coordinate
  address preparation, which is what q_max counts;
- 2ε/3 ≤ ε.

## 5. Finite checks (summary)

| Check | Instance | Result | Label |
|---|---|---|---|
| C10 homomorphisms and associativity | Heis F_3, F_5 (exhaustive pairs); n4 F_5, F_7 (4000 random pairs) | all true | exact |
| C1 homogenization | 19 + 39 + 39 + 220 + 220 subgroup-point cases | all exact; c − 1 points fail (13/19, 181/220) | exact |
| C2 single evaluation | 3146 cases | all agree | exact |
| C3 instrument and descent, Heis F_3 cover, M = 3 | 19 H; 3198 witness cases | all exact; 5616/6084 non-witnesses wrong (468 = H = 1) | float |
| C3 instrument and descent, Heis F_5 cover, M = 2 | 39 H; 3912 witness cases | all exact; law, state and trace formula 39/39; 14400/14880 non-witnesses wrong (the other 480 = H = 1, which is 600 − 120) | float |
| C3b base-group control | Heis F_3, H = ⟨x+z⟩ | 72/234 witness outputs wrong, as predicted | float |
| C4 copy lift | Heis F_3, 19 H | 19/19 | float |
| C5 refresh counterexample | C_5 | as printed | float |
| C6 rank bound | 880 cases | no violation; tight | exact |
| C7 counts | c ≤ 7, m ≤ 11; c = 9 exponent | no violation; 145 | exact |
| C8 Dixmier–Lister | 5 ≤ p ≤ 23 | as printed | exact |
| project sim, default | 37 runs, 23 (G,H) instances (Heis F_3, F_5; n4 F_5), exact and dense backends | all recovered; laws uniform on K_d^⊥; every stage state equals ρ_{H_d}; negative controls as predicted | exact (sim) |
| project ext | heis3, heis5, 14 runs at charged arity | all recovered; queries = charged | exact (sim) |

The paper's §3 paragraph says the sim covers "32 hidden subgroups". The default command covers
23 instances. The remaining 9 come from the class-three group over F_7 (`--f7`), which I did not
run. That is not a core-proof issue.

## 6. Minor, non-blocking

- m1 of the referee is still open. λ is the dilation scalar in `thm:rees-cover`(ii),
  `lem:homogeneous` and `prop:single-evaluation`, and the central label in §§3–4. No proof
  confuses them, because §4 writes the dilation as δ_s, but a reader can. The editorial fix is
  to rename the §2 scalar u. I give no LaTeX for this, since it touches the introduction too.
- `prop:descent` says "a nonzero vector (s_1,…,s_M) ∈ F_p^M". Its proof uses only that the
  active set is nonempty, which is the same thing. Fine.
- §4 "Rank" bullet: the bound uses only e = dim h^⊥ ≤ m. Fine.

## 7. Comparison with earlier reviews (read after my pass)

- **2026-11-01 core proof check.** It agrees on every verdict. Its steps 1–2 found no gap. Its
  envelope (§6.2) defines N_instr = S·P + N_merge + S, the same as mine, but the paper never
  took it up (G2). Its §6.3 says "these errors add over a sequential composition" without
  addressing the restricted domain (G1 not noticed). Its text fixes 1–6 are in the current text.
- **2026-11-02 referee.** Its M3 asked for a hybrid lemma and for the restricted-domain hybrid
  of `thm:uniform-compilation`(iii). I50 inserted P4 with the *full-domain* hypothesis, and
  (iii) still cites the note, so M3 is half done. G1 is its remainder, made precise. Its S1 ran
  the descent at p = 3 only, and its p = 5 run timed out. My C3 at p = 5 (vectorized) closes that
  independently of the project (39/39 subgroups, 3912/3912 witness cases exact). m1 (notation) is still open. m15 is fixed (I54).
- Nothing in either review contradicts a verdict here.

## 8. Exact statement that now holds; what is missing; claim gates

**Holds (AI-checked, pending human review):** the statement quoted in §0, conditional on
applying P1–P3. Without them, the same statement holds with "AI-checked" replaced by "proof has
a stated hypothesis mismatch in the approximation step (G1)". The mathematics is unaffected,
because the fix uses the same proof.

**Still missing.**
- A human reading of §§2–4.
- The Dixmier–Lister row certificates for every p > 3 (re-checked here only for p ≤ 23).
- The IS17 internals: Theorem 11 is cited, not re-derived.
- The QFT compilation constants of `thm:uniform-compilation`(iii) (outside this item).
- An exact rerun of `prop:descent` above class two outside the project's sim. My dense checks
  are class two; the class-three descents rest on the written proof and the project's exact sim
  on n4 F_5.

**Claim gates that must stay false.** `independent_review`, `novelty_established`,
`speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented` and
`formal_compiler_checked`.

## 9. Proposed paper text

All three targets are in `main.tex` §4.2. Status label for each: AI-checked, pending human
review.

### P1. Replace `lem:hybrid` and its proof

Target: the whole `lem:hybrid` environment and its proof.

```latex
\begin{lemma}[Sequential hybrid]
\label{lem:hybrid}
Let an ideal procedure apply quantum instruments $\mathcal{I}_1,\dots,\mathcal{I}_N$ in sequence, each possibly chosen from the earlier classical records, and let the implemented procedure apply $\widetilde{\mathcal{I}}_j$ in place of $\mathcal{I}_j$. View each instrument as a channel whose output is its quantum output together with a classical record register, extended by the identity on the registers it does not touch. Let $\mathcal{S}$ be a set of states of the joint system that contains the initial state, is closed under conditioning on values of classical registers, and is mapped into itself by every ideal step. Suppose $\frac12\|(\widetilde{\mathcal{I}}_j - \mathcal{I}_j)(\omega)\|_1 \le \eta_j$ for every possible choice and every $\omega \in \mathcal{S}$. Then the joint distributions of all classical records, including abort flags and the final output, of the two procedures differ by at most $\sum_{j=1}^N \eta_j$ in total variation distance. If $\mathcal{S}$ is the set of all states, the hypothesis is $\frac12\|\widetilde{\mathcal{I}}_j - \mathcal{I}_j\|_\diamond \le \eta_j$.
\end{lemma}

\begin{proof}
Let $\Phi_j$ and $\widetilde\Phi_j$ be the $j$-th steps on the joint quantum--classical system: each dephases the classical registers it reads and applies the instrument selected by their values. Let $\rho_0$ be the initial state and $\rho_j = \Phi_j\cdots\Phi_1(\rho_0)$, so that every $\rho_j \in \mathcal{S}$. Then
\[
  \widetilde\Phi_N\cdots\widetilde\Phi_1(\rho_0) - \rho_N = \sum_{j=1}^N \widetilde\Phi_N\cdots\widetilde\Phi_{j+1}\bigl((\widetilde\Phi_j - \Phi_j)(\rho_{j-1})\bigr).
\]
After dephasing, $\rho_{j-1} = \sum_r q_r\,\omega_r$, where $\omega_r \in \mathcal{S}$ is the state conditioned on the value $r$ of the registers that step $j$ reads. Hence $(\widetilde\Phi_j - \Phi_j)(\rho_{j-1}) = \sum_r q_r\,(\widetilde{\mathcal{I}}_{j,r} - \mathcal{I}_{j,r})(\omega_r)$ has trace norm at most $2\eta_j$. Channels do not increase the trace norm, so the two final states are within $\sum_j \eta_j$ in trace distance. Measuring the classical registers is a channel, and on diagonal states the trace distance equals the total variation distance.
\end{proof}
```

### P2. Replace the "Approximation" bullet

Target: the third item of the error-budget list in §4.2.

```latex
  \item \emph{Approximation.} Count as one instrument each lifted-source preparation, each merge node (its $M_d$ complete central instruments, the preparation of its quotient address register and its controlled right actions) and each final Fourier readout. With $S = m+t$ terminal samples and $P = \prod_{d=2}^c M_d$, there are
  \[
    N_{\mathrm{instr}} = S\Bigl(P + \sum_{d=2}^{c}\,\prod_{d'=2}^{d-1} M_{d'} + 1\Bigr)
  \]
  of them, a number fixed before the run under Schedule~1, whose arities are fixed and which has no restarts. Call a state \emph{canonical} if every register holds field elements below $p$ and every workspace is clean; the ideal instruments map canonical states to canonical states. Each instrument receives approximation error $\eps/(3N_{\mathrm{instr}})$ on canonical inputs, with any reference system adjoined. Trace distance is $\frac12\|\cdot\|_1$ throughout, so an isometry error $\|(V-U)\Pi\| \le \eta$ in operator norm, where $\Pi$ projects onto the canonical subspace, gives trace distance at most $\eta$ on those inputs.
```

### P3. One sentence in "Proof of Theorem `thm:main`"

Target: replace the sentence that begins "Implementing each of the $N_{\mathrm{instr}}$
instruments".

```latex
Implementing each of the $N_{\mathrm{instr}}$ instruments of the approximation item to error $\eps/(3N_{\mathrm{instr}})$ on canonical inputs (Theorem~\ref{thm:uniform-compilation}(iii), which allots each of its at most $q_{\max}$ transforms the error $\eta = \eps/(3N_{\mathrm{instr}}q_{\max})$) changes the output distribution by at most $\eps/3$, by Lemma~\ref{lem:hybrid} with $\mathcal{S}$ the canonical states.
```

Optional companion, outside this item's sections. In `thm:uniform-compilation`(iii), replace
"By the restricted-domain hybrid of the note, $N_{\mathrm{QFT}}$ calls add at most
$N_{\mathrm{QFT}}\,\eta$ to the error." with "By Lemma~\ref{lem:hybrid}, with $\mathcal{S}$ the
canonical states and each transform as one step, $N_{\mathrm{QFT}}$ calls add at most
$N_{\mathrm{QFT}}\,\eta$ to the error." This makes (iii) self-contained, which is referee M3's
remaining request.
