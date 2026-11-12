# 2026-11-12 Harsh referee: core Sections 4, 5, 7 (measured central descent, Schedule 1, proof of thm:main) and the "Shorter zero sums" Outlook paragraph

**AI-run hostile referee report, pending human review.** Target:
`docs/papers/rees-hsp/core/main-core.tex` §4 (ll. 408–509), §5 (ll. 514–562), §6.2 as used
(ll. 604–627), §7 (ll. 629–655), the parts of §1.4 and §§2–3 they invoke (thm:main, rem:main-solver,
lem:fourier, lem:homogeneous, lem:lifted-source, lem:copy-lift), and the Outlook paragraph
"Shorter zero sums in Schedule 1" (l. 911). I edited no paper, STATE, handoff or reductions file.
No git, no network, no API calls. Scripts and outputs are in `2026-11-12-rees-harsh-sec4/`
(run with `nice -n 19 /opt/anaconda3/bin/python`). Finite checks only falsify.

**Order of work.** I re-derived every statement of §4, the conversion lemma of §5 and the proof of
§7 from the definitions, and wrote the checks, before I opened any earlier referee report. Only
afterwards did I read `2026-11-12-rees-exponent-discharge-referee.md`, `2026-11-05-rees-referee-17-core.md`,
`-18-core.md`, `2026-11-04-rees-referee-9-core.md`, `2026-11-03-rees-referee-2.md` and
`2026-11-02-rees-referee.md` (grep plus the relevant sections). §6 says what is new.

## 0. Overall verdict

**§4, §5 (as used) and §7: CORRECT.** I found no mathematical error in lem:instrument,
lem:central, prop:descent, rem:product-channel, the §4.3 recursion, lem:bezout, the Schedule 1
paragraph, rem:is-import(d), lem:hybrid as applied, cor:approx or the §7 proof. The query count
Q_q = c(m+τ)∏B_d(g_d), its explicit bound and the class-nine exponent **145** are correct from the
paper's own definitions. There is one presentational GAP-level item, which is cosmetic in substance:
the letter s_i is used both for the evaluation points and for the witness scalars in the same §7
paragraph. There are a few small wording fixes (§5).

**Outlook "Shorter zero sums" (145 → 53): CORRECT WITH FIXES**, as an Outlook (argued,
unclaimed) statement. The number 53 is right, and so are the J = ∅ rule, the publicity of the
arity, the Weil-bound threshold and the Las Vegas charging. But the paragraph has four defects, all
new to this report. Two of them matter if the owner moves the headline:

1. It cites the wrong IS result (the rounds are in the proof of IS **Theorem 3**, §3.3, not
   Theorem 11).
2. "⌈log₂ t_d⌉ = 2 once …" is false as written when t_d = 2.
3. It never says that the arity is G(**κ_d**, g_d)^{⌈log₂ t_d⌉}. A reader who charges "Schedule 1
   with L rounds" in the theorem's own way, base d as in B_d, gets **71**, not 53.
4. A length-2 zero sum at even κ_d (when (p−1)/κ_d is even) also needs a 2κ_d-th root of unity,
   which is again a Las Vegas step (or a deterministic step via Pila's algorithm, which I have
   not checked). The paragraph says only that lengths 3 and 4 are Las Vegas. The Las Vegas step
   also needs an explicit per-trial success bound.

If the headline moves to 53, the theorem statement, rem:main-solver, §7 ("deterministic … no solver
failure to budget"), rem:oblivious ("no restarts"), the explicit bound (4) and rem:is-printed must
all change, and the variant needs an in-core lemma with a proof (§4.5 below).

## 1. Table of verdicts

| # | Statement (core line) | Verdict | Note |
|---|---|---|---|
| 1 | Π_λ projectors, R_zΠ_λ = χ_λ(z)Π_λ (l. 419) | CORRECT | needs only Z abelian; centrality is used later |
| 2 | lem:instrument (l. 422) | CORRECT | Kraus operator is exactly Π_λ; a Lüders instrument; trace preserving (checked as matrices) |
| 3 | lem:central (l. 437) | CORRECT | uniform on K^⊥; ρ_λ = ρ_HΠ_λ/(|K|/|Z|); trace formula with sign g = hz checked; no normality or transversality |
| 4 | prop:descent (l. 477) | CORRECT | every positive-probability tuple and every nonzero witness: zeros, repeated labels, labels in a proper subspace, κ_d = p−1 |
| 5 | Independence paragraph (l. 485) | CORRECT | |
| 6 | rem:product-channel (l. 487) | CORRECT | SUM identity checked |
| 7 | §4.3 recursion (l. 496–509) | CORRECT | H_d graded, K_d, a_d, zero-insertion section, G_1 = tL, final h including [L,L] coordinates; generator paragraph correct (symbol K reused, cosmetic) |
| 8 | Tree counts P = ∏M_d, N_d = ∏_{d'<d}M_{d'} (l. 511, 640) | CORRECT | |
| 9 | thm:is-import as used (l. 519) | CORRECT as an import | arity C(d,a) ≤ G^{⌈log₂(d+1)⌉} matches IS §3.3 (re-read in `is_1503.09016.txt` ll. 577–594) |
| 10 | rem:is-import(a)–(e) (l. 529) | CORRECT | (d): Markov 1/4 + 1/4, union bound ε/3, N_solver = (m+τ)Σ_d N_d correct |
| 11 | lem:bezout (l. 549) | CORRECT | u = 0 (κ = p−1) is handled by the s_i = 0 convention |
| 12 | rem:zero-sum (l. 557) | CORRECT | B_4(2) = 3.65·10¹⁶ |
| 13 | Schedule 1 paragraph (l. 562) | CORRECT | |
| 14 | lem:hybrid + application (l. 608–622) | CORRECT | |
| 15 | cor:approx (l. 624) | CORRECT | |
| 16 | §7 procedure + correctness (l. 633–637) | CORRECT (one notation GAP) | s_i = i (points) vs s_i (witness scalars) in the same paragraph |
| 17 | §7 N_QFT (l. 639) | CORRECT | n per leaf, 2g_d per instrument, D_{d−1} per merge, m per terminal sample |
| 18 | §7 query count, explicit bound, C_c (l. 644) | CORRECT | |
| 19 | Exponent 145 at c = 9 (numbers.tex) | CORRECT | 1 + (4+6+12+15+18+21+32+36) |
| 20 | §7 running time (l. 649) | CORRECT | |
| 21 | rem:oblivious (l. 654) | CORRECT for Schedule 1; FALSE as worded for the 53-variant ("no restarts", deterministic time) | only matters if the headline moves |
| 22 | Examples: B_2(1) = 64, B_2(3) = 1024, B_3(2) = 531441, log₂Q = 33.19; the p = 7 five-label cubic and six-label quadratic counterexamples; Heisenberg "three labels suffice" | CORRECT (exact computation) | |
| 23 | Outlook "Shorter zero sums" (l. 911) | CORRECT WITH FIXES | four defects, §4 |

## 2. Re-derivations (independent of earlier reports)

**Projectors.** Using R_aR_b = R_{ab} (right regular representation) and character orthogonality:
Π_λΠ_μ = δ_{λμ}Π_λ, ΣΠ_λ = R_0 = I, Π_λ^† = Π_λ, and R_zΠ_λ = χ_λ(z)Π_λ. These need only that Z is
an abelian subgroup. Centrality is used for [Π_λ, R_h] = 0 with h ∈ H, which makes
Π_λρ_HΠ_λ = ρ_HΠ_λ.

**lem:instrument.** The Kraus operator of outcome λ is ⟨λ|F^†·CR·F|0⟩ = |Z|^{-1}Σ_zω^{−λ·z}R_z = Π_λ.
So the instrument is the Lüders instrument of {Π_λ}. It is valid, the post-measurement states are
as stated, and it uses 2g transforms. The remark "x∗(−z) = x−z" uses centrality of z in G_d; it
belongs to the application, as referee 17 noted.

**lem:central.** tr(ρ_HΠ_λ) = (|G||Z|)^{-1}Σ_{h,z}χ_λ(−z)tr R_{hz}. A term survives only if
hz = 1, that is z = h^{-1} ∈ K, and the sum is |Z|^{-1}Σ_{z∈K}χ_λ(−z) = (|K|/|Z|)[λ ∈ K^⊥]. This is
uniform on K^⊥, because |K^⊥| = |Z|/|K|. For the trace formula: tr(R_{hz}R_g) ≠ 0 iff hzg = 1 iff
g = h^{-1}(−z), so g = h'z' with h' = h^{-1} and z' = −z, and χ_λ(−z) = χ_λ(z'). There are |K| such
decompositions with one common value, which gives χ_λ(z') for g ∈ HZ. The sign is consistent. No
property of H beyond being a subgroup is used.

**prop:descent.** Address state |Q|^{-1}Σ|q⟩⟨r|. A controlled-U_q on a target followed by a partial
trace multiplies entry (q,r) by tr(U_qρU_r^†). Here U_q = R_{δ_s(σ(q))} and
tr(R_aρR_b^†) = tr(ρR_{b^{-1}a}). So the entry is |Q|^{-1}∏_{s_i≠0}tr(ρ_{λ_i}R_{δ_{s_i}(g)}) with
g = σ(r)^{-1}σ(q).

- If g ∉ HZ, then δ_{s_i}(g) ∉ HZ, because δ is bijective with δ(HZ) = HZ. Every active factor is
  0, and the active set is nonempty.
- If g = hz, then δ_{s_i}(g) = δ_{s_i}(h)·(s_i^d z), and the product is ω^{(Σ s_i^dλ_i)·z} = 1.
- g ∈ HZ iff r^{-1}q ∈ HZ/Z.

The output is exactly ρ_{HZ/Z}. The equation is used only through Σ_{i active}s_i^dλ_i = 0, which
the zero entries do not affect, so all of the following are covered:

- witnesses with zeros, repeated labels and labels in a proper subspace (a_d < g_d);
- κ_d = p−1, where s^d ∈ {0,1} and the equation is a zero-sum subset problem.

The witness may depend arbitrarily on the record, since the identity holds pointwise.

**§4.3.** ⊕_{k>d}A_k is a δ-stable ideal, and Z_d = A_d is central in A^{(d)}. H_d is the image of
the graded subalgebra h̃, so it is graded and δ-stable. Also K_d = H_d ∩ Z_d = t^d(h∩γ_d), and
H_dZ_d/Z_d = H_{d−1}. G_1 = A_1 = tL carries the zero bracket. So H_1 = th, and lem:fourier gives
h, including its [L,L] coordinates. The generator paragraph is correct; it reuses the symbol K,
already H∩Z, which is cosmetic.

**Counts.** Stage 2 has one merge, and stage d has N_d = ∏_{d'=2}^{d−1}M_{d'} merges. The leaves
number N_cM_c = P. The per-tree QFT count is Pn + Σ_dN_d(M_d·2g_d + D_{d−1}) + m. This matches l. 639.

**lem:bezout.** Take ud ≡ κ (mod p−1) with u ≥ 0. For x ≠ 0, s^d = x^{ud} = x^κ, and the support is
preserved. If u = 0 then κ = p−1 and s = 1 = x^{p−1}. Checked on 4320 random instances (`misc_checks.out` §1).

**§6/§7 error.** The chain is: Fourier failure ≤ 1/((p−1)p^τ) ≤ ε/3, since p^τ ≥ 3/ε; then
approximation ≤ N_QFT·η = ε/3; total 2ε/3. Under rem:is-import(d), the third ε/3 covers solver
aborts. lem:hybrid's telescoping uses the ideal prefix only, and the implemented suffix is a
channel. Classical steps (the solver, the null space) are total functions on bit strings, so they
are channels.

**Nothing assumed about H.** §4.1 is stated for an arbitrary subgroup of an arbitrary finite group.
§4.2 needs only that δ_s preserves H. §4.3 supplies this through gradedness of H_d, which is true by
lem:homogeneous for every H. Neither normality nor H ∩ Z = 1 is used anywhere.

## 3. The query count and the class-nine exponent

From eq. (Bd): B_d(g) = [d^{d(d−1)/2}(g+1)^d]^{L_d} with L_d = ⌈log₂(d+1)⌉. Each tree consumes
∏_{d=2}^c B_d(g_d) leaves, and each leaf costs c queries (or c copies), so
Q_q = c(m+τ)∏B_d(g_d). With g_d ≤ m this gives
Q_q ≤ C_c·c·(m+τ)(m+1)^{Σ_d dL_d}, where C_c = ∏_d d^{d(d−1)L_d/2}. I checked the inequality
B_d(g) ≤ d^{d(d−1)L_d/2}(m+1)^{dL_d} for d ≤ 9, m ∈ {1,5,19,50} and all g ≤ m.

At c = 9 the values of L_d are 2,2,3,3,3,3,4,4 for d = 2..9, so Σ dL_d = 144 and the exponent of m
is **145**. This equals `\ReesClassNineQueryExp`. The exponent is a polynomial degree in m, so it is
not inflated by the slack g_d ≤ m: under Σg_d ≤ m the product ∏(g_d+1)^{e_d} is still Θ(m^{Σe_d}).
The degree is therefore the right one for the stated bound. It is not a lower bound on the
algorithm's cost.

Two remarks:

- 145 is also the worst case over primes when Schedule 1 is charged B_{κ_d} instead of B_d. It is
  attained at p ≡ 1 mod 2520 (`misc_checks.out` §4). So the uniform B_d costs nothing in the
  worst-case exponent.
- C_9 ≈ 2^{1202.8}.

## 4. The "Shorter zero sums" paragraph (headline 145 → 53)

**4.1 The mechanism (CORRECT).** I re-read IS §3.3. After ℓ rounds of Theorem 11 applied to G^ℓ
columns, either some round's J was empty, or one vector u has 2^ℓ representations with pairwise
disjoint, *nonempty* supports and explicit d-th-power coefficients.

- **Induction.** Round ℓ+1 applies Theorem 11 to G vectors w_k. If J' = ∅, then
  Σ_{k∈I'}γ_k^d(any representation of w_k) is a nonzero zero representation, and we stop.
  Otherwise the representations Σ_{k∈I'}γ_k^dR_k^r and Σ_{k∈J'}γ_k^dR_k^r, for r ≤ 2^ℓ, are
  2^{ℓ+1} disjoint nonempty representations.
- **Finish.** Take a nontrivial z_1^κ + … + z_t^κ = 0 with t ≤ 2^L. Weight representation r by
  z_r^κ and give the rest weight 0. The sum is (Σz_r^κ)u = 0, and it is nonzero because some
  z_r ≠ 0 and the supports are disjoint.
- **Scalars.** They are explicit products, so prop:descent gets s_i and not only s_i^κ.

So L = ⌈log₂ t_d⌉ rounds suffice. The J = ∅ rule is needed for nonemptiness in rounds ≥ 2. The
paper's sentence covers it.

**4.2 Publicity (CORRECT, one wording error).**

- t_d = 2 iff −1 is a κ-th power iff (p−1)/κ_d is even. This includes every odd κ.
- If (p−1)/κ is odd, the Fermat curve x^κ + y^κ + z^κ = 0 has no point with a zero coordinate.
  The Weil bound gives N ≥ p+1−(κ−1)(κ−2)√p, so t = 3 as soon as this is positive. The paper's
  "> 3κ" also covers the even-quotient case, where the zero-coordinate points number at most 3κ.
- Brute force for all primes < 6000 and κ ≤ 9 confirms both rules, with no violations
  (`exponents.out` §3). Explicit point counts for κ ∈ {2,4,6,8} and p < 400 confirm the Weil bound
  and the zero-coordinate count (`misc_checks.out` §5).
- **Error:** "⌈log₂ t_d⌉ = 2 once p+1−… > 3κ_d" is false when t_d = 2, where the value is 1. It
  should read "t_d ≤ 3, so ⌈log₂ t_d⌉ ≤ 2".
- Weil thresholds: 6, 56, 434 and 1810 for κ = 2, 4, 6, 8. Below them t_d can exceed 4:
  t(5,4) = 5, t(7,6) = 7, t(31,6) = 5 and t(41,8) = 5, all with L = 3. They are settled by
  exhaustive search at O_c(1) cost.

**4.3 The number 53 (CORRECT, needs explicit base).** The variant charges grade d with arity
G(κ_d, g_d)^{L_d}, since Schedule 1 runs IS at degree κ_d (κ_d = 1: arity g_d+1). The exponent is
1 + Σ_d κ_dL_d.

- Exhaustive search over all primes 11 ≤ p < 6000 and all unit residues mod 5040 gives a maximum of
  **53** at c = 9, at p ≡ 2521 (mod 5040). There κ_d = d for every d, and L_8 = 2 because
  (p−1)/8 is odd (`exponents.out` §2).
- The paper's text does not state the base. "Charging Schedule 1 with L rounds" in the way the
  theorem charges Schedule 1 (B_d, base d) gives 1 + Σ dL_d, whose maximum is **71** (at p = 31,
  where t_6 = 5; `misc_checks.out` §4). The base κ_d must be written out.
- Other classes, for the record: c = 2..8 give 5, 8, 16, 19, 35, 36, 44. The small-prime maximum
  can exceed the large-prime one (c = 4 at p = 5, c = 6 at p = 31).

**4.4 Las Vegas and the error and gate bounds (CORRECT WITH FIXES).** The zero sum depends only on
(p, κ_d), so it can be found once per grade, before any quantum step.

- **Length 2, κ odd.** z = (1, −1), deterministic.
- **Length 2, κ even with (p−1)/κ even.** This needs z with z^κ = −1. Random y gives
  w = y^{(p−1)/(2κ)} with w^κ = (y|p) = −1 with probability exactly 1/2. This is Las Vegas.
  (Deterministic alternatives: Schoof's algorithm for κ ∈ {2,4,6} via √−1, √2, √−3, or Pila's
  roots-of-unity algorithm. Not checked here; not needed.) **The paragraph omits this case.**
- **Length 3** (p above the threshold, (p−1)/κ odd). A random pair (z_1,z_2) ∈ (F_p^×)² extends with
  probability N/(κ(p−1)), where N is the projective point count. This is ≥ 1/(2κ) once
  (κ−1)(κ−2)√p ≤ (p+3)/2, roughly p ≥ 4(κ−1)²(κ−2)² (7056 at κ = 8). Then a κ-th root is
  extracted by Las Vegas root finding. Below that bound, near the Weil threshold, N can be tiny
  and random trials are slow. Use exhaustive search there, at O_c(1) cost. The paragraph needs
  this explicit success bound, because rem:is-import(d) assumes "fails with probability ≤ 1/4 in
  expected time T".
- **Error budget.** Run ⌈log₂(3(c−1)/ε)⌉ capped attempts per grade, or use rem:is-import(d) per
  merge as the paper says; either works. Aborts cost ≤ ε/3, which is the third left unused by §7.
  No quantum source is consumed by a retry. N_QFT stays public (an upper bound if an abort comes
  early). The gate count gains only poly(log(1/ε)).
- **Conclusion.** The theorem's error ε and gate bound poly_c(m, log p, w, log 1/ε) are preserved.
  "Deterministic" and "no restarts" are not.

**4.5 What a 53 headline would require (owner decision).**

1. Theorem: replace (3)–(4) by arity G(κ_d,g_d)^{⌈log₂t_d⌉} (g_d+1 at κ_d = 1). The explicit bound
   becomes C'_c·c(m+τ)(m+1)^{E_c(p)} with E_c(p) = Σκ_dL_d ≤ 52 at c = 9. C'_c changes too.
2. Add an in-core lemma with the §4.1 proof, since thm:is-import as stated (deterministic, arity
   B_d) does not cover the variant.
3. Item (5) and §7: "deterministic … no solver failure to budget" becomes the ε/3 Las Vegas charge.
4. rem:main-solver: "it is deterministic" becomes Las Vegas.
5. rem:oblivious: "there are no restarts" becomes "classical retries only; queries and N_QFT
   bounded before the run".
6. rem:is-printed: the sentence that the exponent rests on Ivanyos' confirmed bound must say that
   the variant is an AI reading not covered by that confirmation.
7. The macro, the abstract and the class-three example figures (B_3(2), B_2(3), 2^{33.19}) change.

## 5. Replacement text

**R1 (§7 l. 633, notation; GAP-level presentation).** Replace "Fix the points $s_i = i$, $i =
1,\dots,c$," by "Fix the evaluation points $1,\dots,c$ of Lemma~\ref{lem:lifted-source}," and in
Lemma~\ref{lem:homogeneous}/\ref{lem:lifted-source} keep $s_i$; or, cheaper, add after "with the
returned witness": "(the witness scalars of~\eqref{eq:sde-target}, not the evaluation points)".

**R2 (l. 509, cosmetic).** "the subgroup $K = \langle\exp b_1,\dots\rangle$" →
"the subgroup $H' = \langle \exp b_1,\dots,\exp b_k\rangle \le H$ has $\log H'$ …, so $H' = H$".

**R3 (Outlook l. 911), replace the paragraph by:**

> \paragraph{Shorter zero sums in Schedule~1.} The proof of~\cite[Theorem~3]{IvanyosSantha2015}
> (Section~3.3 there) iterates~\cite[Theorem~11]{IvanyosSantha2015} $L$ times on $G(\kappa_d,a)^L$
> columns and obtains one vector with $2^L$ representations of pairwise disjoint support; if in
> some round the set $J$ of Theorem~11 is empty, a nonzero solution has already been found and
> the procedure stops, so otherwise all $2^L$ representations are nonempty. Any nontrivial zero
> sum $z_1^{\kappa_d}+\cdots+z_t^{\kappa_d}=0$ with $t \le 2^L$ then finishes, not only one of
> length $\kappa_d+1$. Let $t_d$ be the least such $t$ and charge grade $d$ with arity
> $G(\kappa_d,g_d)^{\lceil\log_2 t_d\rceil}$ (and $g_d+1$ when $\kappa_d = 1$). The arity is
> public: $t_d = 2$ exactly when $(p-1)/\kappa_d$ is even, $t_d \le 3$ once
> $p+1-(\kappa_d-1)(\kappa_d-2)\sqrt p > 3\kappa_d$ by the Weil bound, and an exhaustive search
> settles the finitely many smaller primes. The zero sum depends only on $(p,\kappa_d)$; for even
> $\kappa_d$ with $t_d = 2$ it needs an element $z$ with $z^{\kappa_d} = -1$, and for $t_d = 3$ a
> random pair extends with probability at least $1/(2\kappa_d)$ above an explicit bound on $p$;
> both are Las Vegas and are charged as in Remark~\ref{rem:is-import}(d), within its $\eps/3$. At
> $c = 9$ the exponent $1+\sum_d\kappa_d\lceil\log_2 t_d\rceil$ of $m$ is at most $53$ over all
> primes $p > 9$, attained for $p \equiv 2521 \pmod{5040}$ (finite computation below the Weil
> thresholds, residue classes above), against $\ReesClassNineQueryExp$ for the arity $B_d(g_d)$
> of Theorem~\ref{thm:main}. Status: AI-checked and refereed by AI, pending human review;
> G.~Ivanyos confirmed the $\lceil\log_2(d+1)\rceil$ bound, not this variant. The theorem and its
> numbers above use the published depth.

**R4 (optional, l. 562).** After "every prime $p > c$" add "(the remaining $M_d - B_{\kappa_d}(g_d)$
targets are consumed and discarded, as in Proposition~\ref{prop:descent})". This states explicitly
that the zero-weight columns cost sources.

## 6. What is new versus earlier referee reports

Earlier reports (referee 2, 9, 17, 18; 11-12 exponent-discharge referee) already found §4/§7
correct, checked N_QFT, 145, and (11-12) the 53 mechanism, the J = ∅ sentence, the publicity
rule and the Las Vegas charge. Referee 2 ran full Heisenberg descents over F_3 and F_5. **New here:**

1. Mis-citation in the Outlook: the rounds are in the proof of IS **Theorem 3** (§3.3), not
   Theorem 11.
2. "⌈log₂ t_d⌉ = 2 once …" is false when t_d = 2. The earlier referee wrote "*otherwise*
   ⌈log₂ t⌉ = 2 once …", which is correct. The paper dropped the word "otherwise".
3. The base G(κ_d, ·) is not stated. With the theorem's base d the same rule gives **71**, not 53.
   This was computed here for the first time.
4. Length-2 zero sums at even κ_d with t_d = 2 are not deterministic as described. The earlier
   referee's "Only finding the length-3 or length-4 zero sum is Las Vegas" is incomplete. Also new:
   an explicit per-trial success bound, and exhaustive search near the Weil threshold, which
   rem:is-import(d)'s hypothesis needs.
5. A list of what changes if the headline moves (§4.5). rem:oblivious and rem:main-solver claim
   determinism and no restarts, which would become false.
6. The s_i notation clash in §7. Referee 2 flagged λ/dilation clashes, not this one.
7. Exact class-3 checks on a Rees cover built from an actual oracle tuple (filiform algebra over
   F_5 and F_7, cover orders 5⁷ and 7⁷). They include κ_3 = 3 at p = 7, K_d ≠ 0 cases, witnesses
   with zeros and repeated labels, and teeth (wrong witnesses, non-invariant two-point pullback).
   The p = 3 Heisenberg run exercises κ_d = p−1 with explicit unitaries and partial traces.
8. 145 is also the worst case of B_{κ_d} (so the uniform B_d is free), and the variant maxima for
   c = 2..8.

## 7. Exact checks run

All checks are in `2026-11-12-rees-harsh-sec4/`. All are exact finite computations (float
tolerance 1e-8 on complex entries) and can only falsify.

| Script → output | What it checks | Result |
|---|---|---|
| `sim_heis_full.py` → `sim_heis_full.out` | Heisenberg, p = 3, full matrices. Lifted source from the oracle tuple; the instrument as explicit Kraus operators (trace preservation checked); the label law; lem:central's trace formula for every g; merges as explicit address⊗target unitaries with sequential partial traces; all 19 subgroups, a sample of label tuples at M = 2, 3, up to 2 random witnesses plus a witness with a zero entry. d = 2 = p−1, so this is the κ_d = p−1 zero-sum case. Final Fourier law uniform on h^⊥. | 308/308 merges exact; labels uniform on K^⊥ for 19/19 |
| same, p = 5 | 39 subgroups, 25 label triples each, ≤ 4 witnesses plus one with a zero entry; merge via the exact Schur-multiplier form tr(U_qρU_r^†), with ρ_λ computed as matrices | 3234/3234 merges exact; 39/39 label laws |
| same, teeth | Wrong witnesses (Σs²λ ≠ 0). Of these, 134/145 (p = 3) and 742/766 (p = 5) give a wrong output. The 11 + 24 that pass are all for H = 1, where ρ_{H_1} is maximally mixed and only diagonal entries survive, so any witness gives it. Single-evaluation pullback source (non-invariant): the output is not a coset state in 4/12 (p = 3) and 48/80 (p = 5) merges | the checks can detect errors |
| `sim_filiform.py 5` → `sim_filiform_p5.out` | Class 3: filiform ⟨x,y,z,u⟩, cover order 5⁷. Stage-3 source from the actual oracle tuple (lem:homogeneous checked on 4000 random pairs; dilation invariance of h̃); stage-2 source ρ_{H_2} built directly. Nine subgroups, including K_3 ≠ 0, K_2 of dimension 1 and 2, non-normal lines, derived lines and H = 1. Per stage: 6 merges with random witnesses, witnesses with zeros and repeated labels, 16 (q,r) entries each, biased to r^{-1}q ∈ H_{d−1} and near misses. All entries computed from definitions, not from lem:central | 0 bad entries among the 864 valid-witness entries per stage (54 merges per stage); label support = K_d^⊥ and uniform in 18/18 stage cases |
| same, teeth | Wrong witnesses fail whenever [r, h] has a nonzero Z_d-component modulo K_d. They pass, as they must, when it does not (H = 1; and H = ⟨u⟩ at stage 2, u central). The weak 0/1-pattern teeth line in the output is superseded by the next row | |
| `teeth_twopoint.py` → `teeth_twopoint.out` | Two-point pullback source (not dilation-invariant, contains ξ_u) at p = 5: the merge kills the ξ_u direction | 16/16 entries differ from the would-be correct value 1 |
| `sim_filiform.py 7` → `sim_filiform_p7.out` | Same at p = 7 (cover order 7⁷ = 823543), where κ_3 = 3 (genuinely cubic weights) and κ_2 = 2; two subgroups (⟨x+z+u⟩, ⟨z+u⟩ with K_2 ≠ 0), arity 4 at stage 3 and 5 at stage 2, 8 entries per merge. The third subgroup was stopped for time and is NOT computed | 0 bad entries among 64 valid-witness entries per stage (8 merges per stage). Wrong witnesses failed in 7 of 8 merges. The pass is one stage-3 wrong witness for ⟨z+u⟩ whose 8 sampled entries missed every pair with a nonzero Z_3-component |
| `exponents.py` → `exponents.out` | 145 and the B_d facts; t_d by brute force for all primes < 6000 and κ ≤ 9 (parity rule and Weil rule); thresholds; the variant maximum over primes for c = 2..9 | 145 confirmed; no rule violation; 53 at c = 9 |
| `misc_checks.py` → `misc_checks.out` | lem:bezout conversion (4320 cases); class-3 example counterexamples (p = 7 five labels; six quadratic labels at p = 5, 7, 11); Heisenberg "three labels suffice" (p ≤ 11); the SUM remark; base-d variant (71); B_{κ_d} at full depth (145); Fermat-curve counts vs Weil (κ ∈ {2,4,6,8}, p < 400) | all as stated in §§2–4 |


## 8. Adversarial self-check

- **Did I anchor?** I wrote the §2 derivations and the checks before reading the earlier reports.
  My conclusions on §4/§7 agree with theirs. Agreement between AI readers is not independent
  evidence of correctness, and a shared blind spot is possible. The most likely one is in
  thm:is-import itself: determinism of IS §3.1 and the restart count. That is outside this brief
  and rests on the source checks.
- **Simulations prove nothing in general.** They use small p (3, 5, 7), one class-3 algebra and
  random (q,r) entries for class 3. The class-3 checks compute ρ_λ and the merge traces from
  definitions (oracle tuple, R_g by BCH, Π_λ as a sum of translations), not from lem:central's
  formula. But they share my reading of the conventions: R_g|x⟩ = |xg^{-1}⟩ and
  ⟨x|ρ|y⟩ ∝ 1_H(x^{-1}y). If the paper and I shared a sign error, a consistent convention would
  hide it. The teeth tests (wrong witnesses fail, non-invariant sources fail) show only that the
  checks can detect some errors.
- **53 rests on finite computation plus a residue argument.** The residue argument assumes t_d ∈
  {2,3} for every p ≥ 6000, which follows from the Weil bound since all thresholds are ≤ 1810 for
  even κ ≤ 8. It also assumes Dirichlet for every unit class, and this affects only attainment, not
  the upper bound. The brute-force t_min uses coset classes of k-th powers. It agrees with the
  parity rule and Weil everywhere, but it is my code.
- **The Las Vegas success bound** 1/(2κ) above p ≈ 4(κ−1)²(κ−2)² is derived, not computed. The
  claim that N/(κ(p−1)) is the extension probability assumes each extendable pair has exactly κ
  third coordinates, which holds because z_3 ≠ 0 and κ | p−1. The Schoof/Pila alternative is
  quoted from memory and marked unchecked.
- **Could 53 be beaten or broken by a prime I missed?** Primes in [6000, ∞) are covered by the
  residue table under the Weil rule. If some t_d were 4 above the threshold, the exponent would not
  change (L = 2 either way), so the only risk is t_d ≥ 5 above 1810, which Weil excludes.
- **Is "CORRECT" for prop:descent too strong?** The proof is a three-line character computation that
  I re-derived twice, once with the sign of the decomposition made explicit. It holds for every
  finite group with a central elementary abelian Z and automorphisms scaling Z, and the hypotheses
  are met in §4.3. I see no residual gap. All of this is AI-checked, pending human review.
