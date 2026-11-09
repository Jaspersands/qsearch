# Unanchored proof check of Appendix C (flat subspace source), 2026-11-03

Campaign 4, item 3 (`research/REES_FULL_CAMPAIGN_4.md`). AI session only; **pending human
review**. No paper file was edited, nothing was committed, and no claim gate was changed.

**Scope.** `docs/papers/rees-hsp/appendix-subspace.tex` (422 lines) and the main.tex statements
it proves: Theorem `thm:subspace-source` (i)–(ii), the four-step composition and Corollary
`cor:subspace-hsp` of §`sec:subspace`. I also read what the appendix imports: Lemma
`lem:homogeneous`, Lemma `lem:copy-lift`, Definition `def:input-contract`, Theorem
`thm:rees-cover`(iii) and the Schedule 1 assembly at the end of §`sec:recursion`.

**Order.** I read the appendix and those statements first and wrote my verdict on every lemma
before running anything. I then wrote the scripts. Only after that did I open
`2026-11-02-rees-subspace-source.md` and the sibling note on item 16. The comparison is at the end.

**Scripts** (folder `2026-11-03-rees-check-app-c/`; each `.py` has a matching `.out`; all
run under `nice`, in about 3 minutes in total, with `/opt/anaconda3/bin/python`):

| Script | What it checks | Kind |
|---|---|---|
| `check_linear_algebra.py` | Lemma gram (a)–(c), Lemma angles (all 3 identities), Prop. ray (a)–(c), and φ(g) = det(Y†UY); 78 random complex cases, d ≤ 5, r ≤ d | float check, mpmath at 40 digits, error ≤ 4e-38 |
| `check_growth.py` | Lemma antisym (a)–(c); Lemma lcu on 54 inputs with 3 completions of J; a growth tree of every accept/reject history to depth 4 | exact (Fractions) for antisym; complex128 and mpmath at 30 digits (3e-31) for lcu |
| `check_norecovery.py` | what happens without the recovery W†, over 20 completions of J and 20 inputs | float check |
| `check_lcu_offsubspace.py` | the gap between the LCU realization and the Lüders instrument outside range(P_k⊗I) | float check |
| `check_character.py` | Lemma character on 7 Lazard groups of class 2–4 over F_3, F_5, F_7, with 3–5 subalgebras each, some nonabelian: group axioms, the conjugation identity, [K,K] = [k,k] as sets, and x∗y − (x+y) ∈ [k,k] | exact over F_p |
| `check_designs.py` | Lemma design (a), (b), (c) and the profile design; a smaller variant | exact over F_p; (c) exhaustive for p ≤ 7 |
| `check_lift.py` | Lemma lift, Cor. cancel, Remark multiple-p on Heis(F_3), Heis(F_5) (3 subgroups H each) and the class-3 filiform group over F_5 (H nonabelian, and H nonnormal); full σ and exact TD for Heis | complex128 |
| `check_accounting.py` | exact tails of Prop. stream; every number in Theorem app-sub-hsp and Remark profile, from integers; Remark multiple-p | exact |

## Verdict

**No counterexample to any proof step.** Every lemma, proposition and corollary is correct as
stated, and so is Theorem `thm:app-sub-hsp` relative to Definition `def:app-sub-core`, with one
fix to how its precision clause is stated (F1 below). The main.tex Theorem `thm:subspace-source`
(i)–(ii) follows. Corollary `cor:subspace-hsp` follows as Theorem `thm:app-sub-hsp`.

Findings, most important first:

- **F1 (precision clause; wording, but it is load-bearing).** Theorem app-sub-hsp says
  "implement each growth instrument within ε/(8TN) in diamond norm". The growth instrument G_k is
  defined as the Lüders instrument on the whole space. Its LCU realization (Lemma lcu) equals
  G_k only on range(P_k⊗I). Off that range, the accept Kraus operator (1/L)(I − Σ_j SWAP_{j,k+1})
  differs from P_{k+1} by exactly k/(k+1) in operator norm: 0.6667 at k = 2 and 0.7500 at
  k = 3 (`check_lcu_offsubspace.out`). So a compiled LCU circuit, which is what part (ii)
  charges, cannot meet the stated target if the target is G_k. The proof is correct once the
  reference is the exact circuit of Lemma lcu. The hybrid then compares compiled circuits with
  exact circuits, and in Run 2 the exact circuits act only on inputs in range(P_k⊗I), where they
  equal G_k. Fix: proposed text P2.
- **F2 (a false illustrative number).** The appendix (line 255, and header lines 33–35) and the
  11-02 review give the leak without recovery as 0.093 "with another completion of J", and say
  that the size depends on the completion. It does not. With the two-outcome measurement
  {|0⟩⟨0|, I−|0⟩⟨0|}, the kept state depends on J only through f = J|0⟩, because
  tr_anc[((I−|0⟩⟨0|)J†⊗I) Y (J⊗I)] = tr_anc[((I−|f⟩⟨f|)⊗I) Y], and the post-Sel state Y itself
  depends on J only through f. Over 20 completions and 20 inputs of rank 1–3 the leak is
  **0.5000** at (d,r,k) = (3,3,2) and (4,3,2), and **0.6667** at (4,4,3), every time
  (`check_norecovery.out`). I cannot reproduce 0.093 with any valid J. It probably came from a
  J with J|0⟩ ≠ f, or from measuring the ancilla in its full basis; the per-outcome leak then
  ranges over 0.500–0.978. The point the remark makes, that recovery is necessary, still stands.
  The smallest falsifier of the no-recovery shortcut is d = r = 3, k = 2, leak 1/2. Fix: P1.
- **F3 (who aborts when making the design).** Main.tex Cor. `cor:subspace-hsp` says design
  generation "has its own abort". Lemma design(b) is deterministic, given the cited solver.
  Lemma design(a) proves only that μ_e is a design. Finding a generator of μ_e needs a Las Vegas
  search, since no deterministic polynomial-time method is known in general. The lemma's title
  "constructible" holds for (b), and for (a) only with that search. Fix: P6.
- **F4 (cost of one evaluation).** Theorem (ii) charges O(n) operations in F_p per evaluation
  a ↦ E_s(a). E_s takes the cover's coordinates (bases of the γ_k) to the given coordinates of
  L, which R expects. That is a linear map F_p^n → F_p^m with Σ_k m·g_k = mn coefficients. So the
  cost is O(mn); O(n) holds only in a filtration-adapted basis. Polynomiality is unaffected.
  Fix: P4.
- **F5 (gaps of one sentence each).** (a) Step (1) produces outputs "just in time" interleaved
  with the lift and the core. Run 2 compares against producing all T outputs first. That this
  changes nothing (the operations act on disjoint registers, and the abort depends only on the
  preparer's own record) is true but unstated: P3. (b) Theorem (iii) says "M ≤ (c+1)! is
  constant" while the theorem allows any certified design: P5. (c) Main.tex Theorem (ii)'s
  one-shot probability r^{−r} is not proved in the appendix. It is Π_k p_k = r^{−r}, exact for
  r ≤ 10 in `check_accounting.out`: P8.
- **F6 (Remark sharper).** "Divides ℓ by about r/2." With γ_r itself the factor is about r when
  rδ² is small. With the stated lower bound min{rδ²/4, 1/2} it is at least min{r/2, 1/δ²}.
  Fix: P7.
- **F7 (an optional improvement, not an error).** The single factor {1, −1} kills every odd
  moment, so Lemma design(b) needs rows only for even j. Then M ≤ 2·Π_{j even ≤ c}(j+1), which
  is 1890 at c = 9 against (c+1)! = 3,628,800. This is proved below and checked on 68 designs,
  including c = p−1: P9.

## Per-statement verdicts

Labels: **proved** means I re-derived it; **exact** means an exact computation; **float** means a
floating-point check. "Smallest counterexample or fix" names the smallest instance that breaks
it, or the fix, or says that there is none.

| Statement | Verdict | Checks | Smallest counterexample or fix |
|---|---|---|---|
| Def. app-sub-instance | sound | — | none. Minor: R acts on C^d inside a q-qubit register (2^q ≥ d), extended by the identity; nothing depends on this, since V ⊆ C^d |
| Def. app-sub-core | sound as an interface; inherits the status of Thm `thm:main` | B_leaf = (m+t)ΠM_d matches the Schedule 1 assembly in §recursion | none |
| Lemma gram (a)–(c) | **proved** | float, 40 digits, 78 cases, error ≤ 4e-38 | none |
| Lemma angles (3 identities) | **proved**. The S_i are orthogonal because all four cross inner products vanish after the SVD | float, 40 digits, error ≤ 2e-40 (sin θ computed from (I−Π_V)Y′ to avoid cancellation) | none |
| Prop. ray (a), (b), (c) = Thm subspace-source(i) | **proved**; every inequality in the chain Π cos ≤ (1−μ)^{r/2} ≤ √(1−TD²) ≤ 1−TD²/2 checked; μ ≥ TD² | float, 40 digits; the stabilizer phase equals det(Y†UY) = det A for block unitaries | none |
| Lemma character | **proved**. Step 2 uses Vandermonde with c′ < p; Step 3 is a polynomial of degree < p in each variable vanishing on F_p², whose st-coefficient is [x,y]; edge case p = 2, c = 1 is trivial | exact on Heis(F_3), Heis(F_5), filiform4(F_5), filiform4(F_7), free(2,3)(F_5), filiform5(F_5), filiform5(F_7): [K,K] = [k,k] in all 23 (group, subalgebra-shape) cases, (dim k, dim [k,k]) up to (5,3) | none |
| Cor. cancel | **proved** | in `check_lift.out`: Φ = 1 on H~ to 5e-14 | without the moment condition: Heis(F_3), H = Z(G), r = 2, S = (1,2), \|Φ−1\| = 1.732 (reproduced) |
| Lemma antisym (a), (b), (c) | **proved** | **exact** for 6 (d,k) and 15 (d,k,r) rational subspaces | none |
| Lemma growth (a)–(c) | **proved**; p_k does not depend on ϱ | growth tree, 80 nodes: \|P(acc) − p_k\| ≤ 2e-15; support leak ≤ 7e-15 | none |
| Lemma lcu | **proved**. Since W(\|0⟩⊗φ) = \|0⟩⊗φ, the recovery W† is exact | 54 inputs × 3 completions, error ≤ 4e-16; mpmath at 30 digits, 3e-31 | none for the lemma. Its remark's number 0.093 is false (F2): P1 |
| Prop. stream = Thm subspace-source(ii) | **proved**: coupon-collector domination with r coupons of probability 1/r² (valid since r·r⁻² ≤ 1); union bounds | **exact** tails for r = 2..10, B = 1..8: P(timeout) ≤ r2^{−B}, largest ratio 0.338 | none. One-shot r^{−r} not proved in the appendix (trivial): P8 |
| Lemma design (a) | existence **proved** | **exact**: 254 triples (p,e,c) | construction is Las Vegas (F3): P6 |
| Lemma design (b) | **proved**, given that the cited solver is deterministic (I did not reread Ivanyos–Santha Fact 2; the item-16 note says it checked arXiv v2) | **exact**: 2050 designs, p ≤ 31, c ≤ 7, rows minimal, maximal, repetitive and random; c = p−1 for p = 3, 5, 7; coverage ≥ c+1 when c ≤ p−2 and ≥ c when c = p−1 | none. Optional smaller variant: P9 |
| Lemma design (c) | **proved** | **exact**, exhaustive: 118,280 multiplicity vectors mod p for p ∈ {3,5,7} | none |
| Lemma lift | **proved**. The slot factor is tr(U(E(a))ξU(E(b))†) = φ(E(b⁻¹∗a)); Frobenius to trace norm via p^{n/2} | Heis(F_3), Heis(F_5) for H = Z(G), ⟨exp X⟩ (nonnormal), ⟨exp X, exp Z⟩: stab(V) = H, χ = ψ0², Φ = 1 on H~, \|Φ\| ≤ (1−δ²)^{r/2} off H~; σ has trace 1 and is PSD; exact TD ≤ bound for ℓ = 1, 2, 3, 5. Filiform4(F_5), H = ⟨e0,e2,e3⟩ (nonabelian, class 2 inside class 3) and H = ⟨e1⟩: Φ = 1 on all 15,625 elements of H~ | none |
| Cor. two lifts (a), (b) | **proved** | (a) is exact (Φ = 0 off H~) | none |
| Remark multiple-p | **proved** | \|Φ^p − 1\| ≤ 2e-13 on H~ for non-design points; 420411, 3,783,699 and 5,885,600 exact | none |
| Thm app-sub-hsp (i) | **proved** relative to Def. app-sub-core: ledger ε/4 + ε/16 + ε/8 + ε/4 = 11ε/16 < ε; b > n log₂ p + log₂(8B_leaf/ε) gives ε p^{−n/2}/16 | parameters re-derived exactly | precision clause F1 (P2); interleaving F5(a) (P3) |
| Thm app-sub-hsp (ii) | **proved** count: ≤ T(N+1) copies, ≤ TN growth steps (≤ 2k ≤ 2(r−1) swaps, ≤ 4 uses of J^{±1}, L ≤ r levels), exactly rT controlled R, 2T evaluations | — | O(n) should be O(mn) (F4, P4) |
| Thm app-sub-hsp (iii) | **proved**; B_leaf uses log_p(12/ε) = log_p(3/(ε/4)) | — | "M ≤ (c+1)!" assumes Lemma design(b) (P5) |
| Remark profile | **exact**: t = 1, log₂ B_leaf = 1569.49, b = 2102, ℓ = 420400, M = 14, log₂ T = 1591.98; B = 1598/1600/1602; N = 6392/102400/1640448; T(N+1) = 2^1604.619, 2^1608.621, 2^1612.623; every value equals the JSON integer (raw_copy_cap, tail_bits, per-output cap, growth cap = TN) | `check_accounting.out` | none |
| Remark sharper | correct inequality | — | factor wording (F6, P7) |
| Remark scope | correct. Spot checks: a supplied rank above r gives p_r = 0, so an abort; the pure-copies bank v⊗v always rejects at level 1 | — | none |
| main.tex Thm subspace-source (i), (ii) | follow from Prop. ray and Prop. stream (+P8) | — | none |
| main.tex §subspace steps (1)–(4) | follow from Lemma lift, Cor. cancel and Thm app-sub-hsp. Step (4)'s mention of Schedule 3 goes beyond the appendix, which needs a deterministic cap on the number of sources consumed | — | optional P10 |
| main.tex Cor. subspace-hsp | follows as Thm app-sub-hsp | — | abort wording (F3, P6) |

## Comparison with `2026-11-02-rees-subspace-source.md` (read after my pass)

- **Agreement.** Every mathematical step it checks, I also find correct: the CS decomposition,
  AM–GM, state-independent p_k, the necessity of W†, the coupon clock, the four-step composition,
  the falsifiers 1.732 and 1.902, and the profile table. Its numbers match mine exactly.
- **Disagreement.** It gives the no-recovery falsifier as "weight 0.093" at d = r = 3, k = 2. For
  any valid J and the two-outcome measurement, the weight is exactly 1/2 (F2). The appendix
  carries both numbers and calls the difference completion-dependent. That explanation is wrong.
- **New here.** F1 (the precision reference) and F4 (O(mn)) concern text written after that
  review. F3 is inherited from it ("its own abort"). F7 is new. The review also says "about
  r/2" (F6).
- The review's Lemma copy-lift-style composition is now Lemma lift, which covers both lifts and
  needs a design only when χ ≠ 1. I checked it independently, on more groups than the review:
  class 3 and a nonabelian H.

## Exact statement that now holds

**Theorem (flat subspace HSP, conditional on the core; proved here, AI-checked, pending human
review).** Assume Definition `def:app-sub-instance`: an explicit Lazard algebra L over F_p of
class c < p; fresh i.i.d. copies of Π_V/r with r supplied; a linear controlled R; the promised
gap δ. Assume also Definition `def:app-sub-core`: the Schedule 1 core of Thm `thm:main`, or any
schedule that consumes at most a fixed number of sources. Let S be a certified zero-moment
design of size M, and set the parameters as in Theorem `thm:app-sub-hsp`. Implement each growth
attempt by the circuit of Lemma `lem:app-sub-lcu` within ε/(8TN), each controlled R within
ε/(16rT), and each address preparation within ε/(16B_leaf), all in diamond norm *of the
respective ideal circuit*.

Then the output is a basis of log H with probability ≥ 1−ε, an abort counting as failure. It
uses ≤ T(N+1) raw copies, ≤ TN growth attempts, exactly rT controlled R calls and 2T
evaluations of O(mn) F_p-operations each, plus the core's own work at ε/4. With the design of
Lemma design(b), M ≤ (c+1)!; with merged odd rows, M ≤ 2Π_{j even ≤ c}(j+1).

Design (b) is deterministic, given van de Woestijne's solver. Design (a) is Las Vegas.

## Still missing

- Human review of the whole appendix, and of Theorem `thm:main`, on which everything here is
  conditional.
- Rereading Ivanyos–Santha Fact 2 / van de Woestijne for the exact statement "a nonzero solution
  of Σ_{i ≤ j+1} x_i^j = 0 in deterministic poly(j, log p)". I relied on the item-16 note's
  check; I did not open the source (no network use in this session).
- No explicit family with polynomial r, a proved gap and a nontrivial nonnormal H. No quantum
  implementation of the preparer or the core. The gap δ is a promise.
- No end-to-end simulation of the lift composed with a core. Item 9 covers the mixed-source
  analogue; I checked the lift's output density only.

## Claim gates that must stay false

`speedup_claim_allowed`, `novel_antisymmetrization_primitive`, `novelty_established`,
`nonflat_conjugation_symmetry_covered`, `preparer_quantum_backend_implemented`,
`quantum_receiver_implemented`, `natural_hard_state_family_established`, `quantum_execution_performed`,
and every Rees candidate or proof promotion.

## Proposed paper text

For the integrator only. Every item is AI-checked and pending human review. Each one gives its
target, its status, and exact LaTeX.

**P1** (target: `appendix-subspace.tex` line 255, the second and third sentences of the
paragraph after Lemma `lem:app-sub-lcu`; also fix header comment lines 33–35 to match).
Status: float check (`check_norecovery.out`) plus a one-line proof.

```latex
The recovery $W^\dagger$ is necessary. Without it, discarding the ancilla and the fresh register can leave the retained registers outside $\wedge^kV$. At $d = r = 3$ and $k = 2$ the retained state on the rejection branch has weight $1/2$ outside $\wedge^2V$ (float check; $2/3$ at $d = r = 4$, $k = 3$). This does not depend on the completion of $J$: the post-measurement state depends on $J$ only through $f = J|0\rangle$, since $\tr_{\mathrm{anc}}\bigl[((I-|0\rangle\langle0|)J^\dagger\otimes I)\,Y\,(J\otimes I)\bigr] = \tr_{\mathrm{anc}}\bigl[((I-|f\rangle\langle f|)\otimes I)\,Y\bigr]$ and $Y = \mathrm{Sel}\,(J\otimes I)(|0\rangle\langle0|\otimes\nu)(J^\dagger\otimes I)\,\mathrm{Sel}^\dagger$.
```

**P2** (target: Theorem `thm:app-sub-hsp`, the sentence after the three steps, line 372; and
Run 2 of its proof, line 391). Status: proved.

```latex
Implement each growth attempt (if $r \ge 2$) by the circuit of Lemma~\ref{lem:app-sub-lcu}, within $\eps/(8TN)$ in diamond norm of that circuit with exact $J$, $\mathrm{Sel}$ and measurement; implement each controlled call of $R$ within $\eps/(16rT)$, and each address preparation within $\eps/(16B_{\mathrm{leaf}})$.
```

In Run 2, replace "with the exterior states from $\mathcal{P}_T$, which has exact instruments." by:

```latex
with the exterior states from $\mathcal{P}_T$, run with the exact circuits of Lemma~\ref{lem:app-sub-lcu}. These circuits receive only inputs supported in $\wedge^kV\otimes V \subseteq \operatorname{range}(P_k\otimes I)$ (Lemma~\ref{lem:app-sub-growth}), where they equal $\mathcal{G}_k$. Off $\operatorname{range}(P_k\otimes I)$ they differ from $\mathcal{G}_k$: the accept Kraus operator $\frac1{k+1}(I-\sum_j\mathrm{SWAP}_{j,k+1})$ is at operator-norm distance $k/(k+1)$ from $P_{k+1}$. This is why the precision above is measured against the circuit, not against $\mathcal{G}_k$.
```

**P3** (target: end of Run 2, after "$|\Pr_2(\mathsf{F})-\Pr_1(\mathsf{F})| \le \eps/8$."). Status: proved.

```latex
Producing the outputs just in time does not change this: the preparer acts only on its own registers, its abort rule depends only on its own record, and operations on disjoint registers commute, so the interleaved run has the same output law as the run that first prepares all $T$ outputs.
```

**P4** (target: Theorem `thm:app-sub-hsp`(ii), line 375). Status: proved.
Replace "each with $O(n)$ operations in $\Fp$" by:

```latex
each a public $\Fp$-linear map $\Fp^n \to \Fp^m$ with $O(mn)$ operations in $\Fp$
```

**P5** (target: proof of Theorem `thm:app-sub-hsp`, line 398, "For~(iii), $M \le (c+1)!$ is
constant."). Status: proved.

```latex
For~(iii), take the design of Lemma~\ref{lem:app-sub-design}(b), so that $M \le (c+1)!$ is constant.
```

**P6** (target: Lemma `lem:app-sub-design`(a), line 282; and main.tex Cor.
`cor:subspace-hsp`, line 813, "(its generation has its own abort, charged separately)").
Status: proved (standard).

Append to (a):

```latex
A generator of $\mu_e$ is found by a Las Vegas search: for uniform $x \in \Fp^\times$, the element $y = x^{(p-1)/e}$ generates $\mu_e$ if and only if $y^{e/q} \ne 1$ for every prime $q \mid e$, which happens with probability $\varphi(e)/e$.
```

In main.tex replace the parenthesis by:

```latex
(Lemma~\ref{lem:app-sub-design}(b) constructs one deterministically, with $M \le (c+1)!$; the cyclic design of Lemma~\ref{lem:app-sub-design}(a) needs a Las Vegas search for a generator)
```

**P7** (target: Remark `rem:app-sub-sharper`, line 408). Status: proved.
Replace "Using $\gamma_r$ instead of $\delta^2/2$ divides $\ell$ by about $r/2$ when $r\delta^2$
is small." by:

```latex
Using $\gamma_r$ instead of $\delta^2/2$ divides $\ell$ by about $r$ when $r\delta^2$ is small, and by at least $\min\{r/2,\,1/\delta^2\}$ in general, by the lower bound above.
```

**P8** (target: end of the proof of Proposition `prop:app-sub-stream`, line 272). Status: proved;
exact for r ≤ 10.

```latex
For comparison, projecting $r$ raw copies at once onto $\wedge^r\mathbb{C}^d$ succeeds with probability $\tr(P^V_r)/r^r = r^{-r} = \prod_{k=1}^{r-1}p_k$, the probability that the first $r-1$ attempts all succeed.
```

**P9** (optional; target: after the proof of Lemma `lem:app-sub-design`, before "A design is
public preprocessing"). Status: proved; exact check on 68 designs, p ≤ 31, c ≤ 8, including
c = p−1 for p = 3, 5, 7.

```latex
\begin{remark}[Smaller product designs]
Since $\sum_{x\in\{1,-1\}}x^j = 0$ for every odd $j$, the single factor $X = \{1,-1\}$ kills every odd moment. Hence the rows of Lemma~\ref{lem:app-sub-design}(b) are needed only for even $j$, and $S = \{\epsilon\,x_2x_4\cdots x_{2\lfloor c/2\rfloor} : \epsilon \in \{1,-1\},\ x_j \in X_j\}$ is a design with $M \le 2\prod_{2\le j\le c,\ j\text{ even}}(j+1)$; at $c = 9$ this is $1890$. The coverage argument is unchanged. If $c \le p-2$, then $p \nmid M$. If $c = p-1$, then $c$ is even, and the product without the row $j = c$ has size prime to $p$ and kills the moments $1,\dots,p-2$.
\end{remark}
```

**P10** (optional; target: main.tex §`sec:subspace`, step (4), line 808). Status: argued.
Replace "its label law, including the uniform law used by Schedule~3, is covered by the
complete-instrument hybrid." by:

```latex
its label law is covered by the complete-instrument hybrid for any schedule that consumes at most a fixed number of sources (Definition~\ref{def:app-sub-core}); Theorem~\ref{thm:app-sub-hsp} is stated for Schedule~1.
```
