# Diagonal SDE, total regime at near-linear arity: existence threshold (2 + O(log(κa)/log p))·a, a reduction to strictly sub-critical banks, PWPP membership by pigeonhole; complexity still open

AI-only pass, 11 November 2026, one Claude Code session plus one paid Claude API audit (§8).
Not human-reviewed, not in Lean, no novelty or priority claim. Scripts and outputs:
`2026-11-11-rees-sde-near-linear-total/`, interpreter `/opt/anaconda3/bin/python -I`. Only this
file and that folder were written: no `.tex`, no git, no STATE/handoff/plan edits.
Inputs read: `STATE.md` (Now; Rees SDE rows), `TRAPS.md`, the 8 Nov near-linear report and its
referee, report A of 7 Nov (§0, §1, §6–§8, §10), the literature notes of 7 and 8 Nov.

Labels: **[proved]** complete proof here; **[proved given X]** complete modulo a named earlier
repo result; **[known: …]** standard or from the repo's literature notes (as cited there; not
re-fetched); **[argued]**; **[conjecture]**; **[exact]**/**[search]** for computations (finite
computations only falsify; trap 7).

Notation as in the 8 Nov report: κ ≥ 2, p ≡ 1 (mod κ) prime, P = (F_p^×)^κ, P₀ = P ∪ {0}. A
bank is λ_1..λ_n ∈ F_p^a (worst case: arbitrary columns, repetitions allowed); a solution is
x ∈ P₀^n ∖ {0} with Σ x_i λ_i = 0; a bank is *dead* if it has none. cone(B) = {Σ x_iλ_i : x ∈ P₀^n}.
N(κ, a, p) = least n such that every bank of n columns in F_p^a has a solution. Input size
poly(a, n, log p). "Total regime" = n ≥ N(κ, a, p).

## 0. Verdict

The total regime is now located for every κ, not only κ = 2, but its complexity is unchanged:
no algorithm, no hardness, and no TFNP class at near-linear arity for large p.

1. **Existence threshold (Theorem E) [proved].** For every κ ≥ 2, prime p ≡ 1 (mod κ), a ≥ 1 and
   η > 0 with p^{η/(2(2+η))} ≥ 2(κ−1)((2+η)a + 1), every bank of more than (2+η)a columns in F_p^a
   has a solution. Consequences:
   - (E1) With η = 1: every bank of 3a + 1 columns is solvable once p ≥ (2(κ−1)(3a+1))⁶. This beats
     Chevalley–Warning (κa + 1) for every κ ≥ 4 at polynomial primes.
   - (E2) For η ≤ 1 it suffices that η ≥ 6 ln(2(κ−1)(3a+1))/ln p, so
     N(κ, a, p) ≤ (2 + 6 ln(2(κ−1)(3a+1))/ln p)·a + 1. At p = a^C this is (2 + O(1/C))a; at
     p = a^{ω(1)} it is (2 + o(1))a.
   - (E3) Exact: N(κ, a, p) = 2a + 1 when p > (2κ−2)^{4a+2}. The lower bound is the a dead pairs.
     This proves the 8 Nov report's "density remark", which was [argued].
   - (E4) N(κ, 2, p) = 5 for p ≥ 4κ⁶ (via Lemma R below). N(κ, 1, p) = 3 for p ≥ κ⁴.
2. **Structure (Lemmas DC, R) [proved].**
   - DC: if N(κ, u, p) = 2u + 1, every dead bank of 2u columns in F_p^u has cone = F_p^u.
   - R: for p ≥ κ⁴, worst-case SDE at (a, 2a + 1) Turing-reduces in poly(a, log p) time, with at most
     a oracle calls, to *strictly sub-critical* (s.s.c.) banks. An s.s.c. bank has 2d + 1 columns in
     F_p^d, and every proper subspace U holds at most 2 dim U − 1 of them. The reduction is correct
     whenever N(κ, d, p) = 2d + 1 for all d ≤ a; for κ = 2 this is Chevalley–Warning, so the κ = 2
     reduction is unconditional.
   - Hence every worst-case difficulty at 2a + 1 lives in s.s.c. banks. These are exactly the banks
     where the Weil count is weakest. Dead s.s.c. banks exist at small p: a 7-column dead s.s.c.
     bank in F_13³ for κ = 3 [exact], so N(3, 3, 13) ≥ 8 although N(3, 2, 13) = 5. The threshold
     at fixed p does depend on a.
3. **TFNP placement.**
   - (P1) [proved] If −1 ∈ P and n ≥ a log₂ p + 1, every bank has a {0, ±1}-solution, and the search
     problem is in PWPP: a Karp reduction to COLLISION.
   - (P2) [proved + known: MP13 via lit2 §3] For κ = (p−1)/2, P₀ = {0, ±1} and SDE *is* homogeneous
     ternary SIS^∞. It is total at n ≥ ⌊a log₂ p⌋ + 1, and for uniformly random banks it is as hard
     as worst-case approximate SIVP at p ≥ √n·a^δ. This is genuine total-regime hardness at
     near-linear arity, but only with |P| = 2 (κ growing with p). Nothing transfers to fixed κ.
   - (P3) [known: GKSZ via lit §3, input model not rechecked] At a *fixed* prime the CW instance is
     a Chevalley_p instance, hence in PPA_p.
   - For superpolynomial p and 2a + 1 ≤ n < a log₂ p, no standard TFNP class is known to contain the
     problem [argued]. Totality there comes from a mod-p count with exponential p (CW) or from
     Weil counting (Theorem E), and neither is a polynomial-size local parity or pigeonhole argument.
4. **Barrier for hardness (Prop. L*) [proved].** Assume N(κ, d, p) = 2d + 1 for all d ≤ a. Pad a
   bank B with columns G that no solution of B ∪ G uses. If |G| = 2 dim span(G), the projected
   bank B̄ in F_p^a/span(G) is already total, and its solutions are solutions of B. So unused
   padding cannot turn a promise instance into a total one. This generalizes the 8 Nov
   Proposition L (dead pairs) from κ = 2 to every κ in the range of (E3). The κ = 2 case is
   unconditional.
5. **Algorithms.**
   - (A0) [proved] Under Theorem E's hypothesis, Las Vegas expected time κ^{(2+η)a+1}·poly. Sample the
     kernel of a densest sub-bank, found by submodular minimization. The heuristic baseline on
     random banks is κ^{a(1+o(1))} [argued].
   - (A1) [proved given Theorem A of report A, which is stated for every J ≥ max(κ, 2)] Taking
     J ≈ √a/2 instead of log a: every bank with 2a^{1.5} + O(a) columns is solved in expected time
     κ^{1.5√a+O(1)}·poly at primes p ≥ κ^{3√a+O(1)}. More generally, arity a²/(2s) + 2sa + O(a)
     costs time κ^{3s+O(1)}; exact optima are in `tradeoff.out`. This is subexponential below
     a²/log a, but it does not reach near-linear arity.
   - No algorithm beating κ^{Θ(a)} at n = O(a polylog a) was found.
6. **Combined picture at one prime [proved given Theorem H of 8 Nov (PRF-conditional)].** Take
   ln p = √(6a ln κ · ln(2(κ−1)(3a+1))). Then:
   - every bank with ≥ 2a + w columns is solvable;
   - the promise problem with ≤ 2a − w columns is Legendre/power-residue-PRF hard;
   - here w = 2√(6a ln(2(κ−1)(3a+1))/ln κ) + O(1) = O(√(a log a)).

   The open band, total but of unknown complexity at fixed κ, is O(√(a log a)) columns wide at that
   prime size, for every κ.

## 1. Regimes and access model

- Worst case over banks unless stated (P2's hardness is average case over uniform banks, which
  implies worst case). κ fixed, p → ∞ with p ≥ poly(a) unless stated. The output must be
  verifiable: membership in P₀ is Euler's criterion, x^{(p−1)/κ} = 1.
- Promise regime: n < N(κ, a, p). Theorem H (8 Nov) gives PRF-hardness for a + 2 ≤ n ≤
  2a + 4 − ⌈log_κ p⌉ − λ, at primes with a ≤ (log p)^{O(1)} (the referee's corrected scope).
- Total regime: n ≥ N(κ, a, p). Before this pass: N ≤ κa + 1 (CW), and N = 2a + 1 for κ = 2
  (CW plus dead pairs). After this pass, Theorem E gives (2 + o(1))a at superpolynomial primes
  for every κ.

## 2. Cheapest classical baselines (stated first)

- **CW [known]:** N(κ, a, p) ≤ κa + 1 for every p. **Dead pairs [proved, 8 Nov Lemma D]:**
  N ≥ 2a + 1 for every κ ≥ 2 and every p.
- **Small p [known: Olson / van Emde Boas–Kruyswijk, lit §2]:** at p = κ + 1, P₀ = {0, 1} and
  N = D(C_p^a) = a(p − 1) + 1 = κa + 1. So CW is tight at the smallest prime, and the
  threshold must depend on p.
- **Signed Davenport constant [proved here, elementary; literature on the "plus-minus weighted
  Davenport constant" not consulted]:** let D_±(p, a) be the least n such that every n columns
  have a nonzero {0, ±1}-combination equal to 0. Then a⌊log₂ p⌋ + 1 ≤ D_±(p, a) ≤ ⌊a log₂ p⌋ + 1.
  - Upper bound: 2^n > p^a forces two 0/1 combinations to collide.
  - Lower bound: the a⌊log₂ p⌋ columns 2^i e_j have no signed relation. A signed sum of distinct
    powers of 2 below p is nonzero over Z (look at the lowest term) and has absolute value < p.
  - If −1 ∈ P then {0, ±1} ⊆ P₀ and N ≤ D_±. If P = {±1} (κ = (p−1)/2) then N = D_±.
- **Random banks [argued, first moment]:** a uniform bank of n columns has about |P₀|^n/p^a
  solutions. So random banks are solvable w.h.p. from n ≈ a(1 + ln κ/ln(p/κ)), far below 2a.
  Ternary solutions of random banks appear from n ≈ a log₃ p (3^n vs p^a): the "c·a log p/log 3"
  scale of the brief. Totality (worst case) needs 2a + 1 to (2 + o(1))a for P₀-solutions, and
  about a log₂ p for ternary ones.
- **Brute force [argued]:**
  - Random kernel vectors succeed with probability ≈ κ^{−n}.
  - Restricting to a j-dimensional subspace of the kernel on which n − a − j coordinates vanish
    leaves a + j coordinates to land in P, at cost ≈ κ^{a+j} with j ≈ 1 + a ln κ/ln p. So the
    heuristic baseline is κ^{a(1+o(1))}·poly.
  - The provable worst-case baseline is (A0), κ^{(2+η)a+1}.
- **Best poly-time arity [proved, report A]:** O(a²/log a) at p ≥ poly(a); (a+1)(a+2)/2 uniformly
  in p (ISS). KOW's worst-case SIS^∞ algorithm needs m ≥ Cn^k with s = ⌊q/(2k)⌋, which is useless at
  s = 1 [known: lit §1.1].
- **SIS hardness [known: lit2 §3, MP13 Thm 1.1]:** SIS with ℓ∞ bound β needs q ≥ β·n^δ. Every
  proved SIS/LWE hardness needs q ≥ poly(n). The only constant-modulus completeness result (SZZ,
  q = 4) puts the hardness in extra constraint rows.

## 3. Existence thresholds

**Tools.**
- (Gauss) [known: standard Gauss-sum bound] S(c) := Σ_{y∈F_p} e_p(c y^κ) has S(0) = p and
  |S(c)| ≤ (κ − 1)√p for c ≠ 0.
- (Lemma W) [proved in report A §2, Weil] For e distinct offsets β_b and any classes ε_b,
  #{s : s + β_b ∈ g^{ε_b}P ∀ b} ≥ κ^{−e}(p − e − (κ^e − 1)(e − 1)√p).
- (Count) [proved, orthogonality] For a bank T of n columns spanning F_p^D,
  N_T := #{y ∈ F_p^n : Σ y_i^κ λ_i = 0} = p^{−D} Σ_{u∈F_p^D} Π_i S(⟨u, λ_i⟩).
  Each solution x has κ^{|supp x|} preimages y. So T has a solution iff N_T ≥ 2, and the number
  of solutions is at least (N_T − 1)κ^{−n}. The identity was verified exactly on 98 banks
  (`count_check.out`).

**Theorem E [proved].** Let η > 0 and let B have n₀ columns in F_p^a with (2+η)a < n₀ ≤
⌊(2+η)a⌋ + 1 (extra columns can be deleted). If p^{η/(2(2+η))} ≥ 2(κ − 1)n₀, B has a solution.

*Proof.*
1. If B has a zero column, that column alone is a solution.
2. Let T ⊆ B maximize |T|/rk T (a densest sub-bank). Put δ = |T|/rk T ≥ n₀/a > 2 + η, n = |T| ≤ n₀
   and D = rk T, and identify span T with F_p^D. Every T′ ⊆ T has |T′| ≤ δ rk T′.
3. In (Count), the term u = 0 is p^{n−D}. For u ≠ 0 let z(u) = #{i ∈ T : ⟨u, λ_i⟩ = 0}. Then
   |Π_i S| ≤ p^z ((κ−1)√p)^{n−z} = ((κ−1)√p)^n A^z with A = √p/(κ−1) ≥ 1.
4. Expand A^{z(u)} = Σ_{T′ ⊆ Z(u)} (A−1)^{|T′|} and swap the sums:
   Σ_{u≠0} A^{z(u)} = Σ_{T′} (A−1)^{|T′|}(p^{D−rk T′} − 1) ≤ Σ_{T′: rk T′ < D} A^{|T′|} p^{D−rk T′}.
5. Put m = n − |T′| and c = D − rk T′. Then
   |N_T − p^{n−D}|/p^{n−D} ≤ Σ_{T′: rk T′<D} (κ−1)^m p^{c−m/2}.
6. Densest gives m ≥ δc, so m − 2c ≥ (1 − 2/δ)m ≥ (η/(2+η))m. Each term is ≤ x^m with
   x = (κ−1)p^{−η/(2(2+η))} ≤ 1/(2n). Every T′ with rk T′ < D has m ≥ 1, so the sum is
   ≤ (1 + x)^n − 1 ≤ e^{1/2} − 1 < 0.65.
7. Hence N_T ≥ 0.35 p^{n−D} ≥ 0.35p > 1, and N_T ≥ 2. Some y ≠ 0 exists; x = y^κ, extended by zeros,
   solves B. ∎

*Corollaries.*
- (E1): put η = 1.
- (E2): for η ≤ 1, η/(2(2+η)) ≥ η/6.
- (A0): the proof also shows that a uniform kernel vector of T is a solution with probability
  ≥ (N_T − 1)/(κ^n p^{n−D}) ≥ 0.35κ^{−n} − κ^{−n}p^{−1}. A densest sub-bank is found in
  polynomial time by parametric submodular minimization of δ·rk(T) − |T| with a Gaussian-elimination
  rank oracle. This gives a Las Vegas algorithm with expected κ^{(2+η)a+1}·poly time.

**Theorem E′ (E3) [proved].** If p > (2κ − 2)^{4a+2}, every bank of 2a + 1 columns in F_p^a has a
solution.

*Proof.*
1. Take T densest as before, with n ≤ 2a + 1 and n > 2D.
2. Group the u ≠ 0 by the proper flat W(u) = span{λ_i ∈ T : ⟨u, λ_i⟩ = 0}. W has dimension w and
   holds exactly the n_W = z(u) columns orthogonal to u, and there are ≤ p^{D−w} such u.
3. Densest gives n − n_W ≥ δ(D − w) > 2(D − w), so n − n_W ≥ 2(D − w) + 1. With √p ≥ κ − 1:
   relative error ≤ Σ_W p^{D−w}((κ−1)/√p)^{n−n_W} ≤ Σ_W (κ−1)^{2(D−w)+1}p^{−1/2}
   ≤ (2^n − 1)(κ−1)^n p^{−1/2}.
4. This is < 1 − 2^{−n} once √p ≥ (2(κ−1))^n, and then N_T > p^{n−D}2^{−n} > 1. ∎

The subset bound beats the flat bound once η is a constant. The flat bound is better for the
exact threshold, because it avoids the factor n^{4a}.

**Lemma DC (dead ⇒ covering) [proved].** If N(κ, u, p) = 2u + 1, every dead bank D of 2u columns
in F_p^u has cone(D) = F_p^u. *Proof.* For v ≠ 0, D ∪ {−v} has a solution. D is dead, so the
coefficient of −v lies in P; dividing by it gives v ∈ cone(D) (P₀ is closed under division by
P). ∎

**Lemma R (reduction to strictly sub-critical banks) [proved].** Let p ≥ κ⁴. Call a bank of
2d + 1 columns spanning F_p^d *s.s.c.* if every subspace U with 1 ≤ dim U ≤ d − 1 contains at
most 2 dim U − 1 of its columns.
- (a) If every s.s.c. bank in F_p^{d′} has a solution for every 2 ≤ d′ ≤ a, then N(κ, d, p) = 2d + 1
  for all d ≤ a. The case d′ = 1 holds unconditionally at p ≥ κ⁴; the audit in §8 noted that it
  is the only use of p ≥ κ⁴.
- (b) Given N(κ, d, p) = 2d + 1 for all d ≤ a, a solution of any bank of ≥ 2a + 1 columns is
  computed in time poly(a, n, log p) with at most a calls to an s.s.c. solver. The time is Las
  Vegas because of the d = 1 sampling.

*Proof* (strong induction on d; B has exactly 2d + 1 columns after deletion).
- d = 1, columns c₁, c₂, c₃ ≠ 0: set x₃ = 1 and seek x₁ ∈ P with x₁ + c₃/c₁ ∈ −(c₂/c₁)P. Lemma W
  with e = 2 and offsets 0, c₃/c₁ gives ≥ κ^{−2}(p − 2 − (κ² − 1)√p) > 0 choices for p ≥ κ⁴; a
  random x₁ works with probability ≈ κ^{−2}.
- d ≥ 2. Zero column, or B not spanning: trivial, or induction in span B.
- (A) Some proper U holds ≥ 2 dim U + 1 columns: induction in U.
- (B) Otherwise, suppose some proper U with u = dim U ≥ 1 holds exactly 2u columns (tight; a
  proportional pair is the case u = 1). Let D = B ∩ U.
  - The other 2(d − u) + 1 columns project to nonzero vectors of F_p^d/U: a column in U would
    put 2u + 1 columns in U.
  - Induction in the quotient gives x̄ ≠ 0 with w := Σ_{B∖D} x̄_i λ_i ∈ U.
  - Induction in U on D ∪ {w} gives (y_D, y_w) ≠ 0. If y_w = 0, y_D solves D. Otherwise
    x_D = y_D/y_w gives Σ x_D λ = −w, and (x_D, x̄) is a solution of B.
- (C) Otherwise B is s.s.c.

Detection [proved, standard tools]:
- Every proper flat misses some column e, and |B ∖ e| = 2d. So (A) holds iff
  min_{T⊆B∖e}(2 rk T − |T|) < 0 for some e: one submodular minimization per e.
- When (A) fails, a tight proper flat containing a column g and avoiding e exists iff the minimal
  minimizer over {T ⊆ B∖e : g ∈ T} has value 0 and rank < d.
- The recursion splits the dimension, so it has ≤ d leaves (1-dimensional or s.s.c.).

In the proof of (a), (B) uses only the induction hypothesis at dimensions u, d − u < d. ∎

**Corollary E4 [proved].** N(κ, 2, p) = 5 for p ≥ 4κ⁶.

*Proof.* By Lemma R(a), only s.s.c. banks in F_p² remain. Such a bank has no two proportional
columns, so any four of its columns t₁..t₄ are pairwise independent. After a change of
coordinates t₁ = e₁, t₂ = e₂, t₃ = (α, β), t₄ = (γ, δ). Put x₄ = 1. We need x₃ ∈ P with
x₃ + γ/α ∈ −α^{−1}P and x₃ + δ/β ∈ −β^{−1}P. The three offsets 0, γ/α, δ/β are distinct, and
Lemma W (e = 3) gives a solution once √p ≥ 2κ³. ∎

Data agree (`dead_w2.out`, [exact]): for κ = 3, N(3, 2, p) = 5 for every tested p ∈ [13, 67],
far below 4κ⁶ = 2916. The cases N(3, 2, 7) = 6, N(4, 2, 13) = 7 and N(4, 2, 17) = 6 lie below the
range.

**Does the threshold become 2a + 1 at an a-independent prime? [conjecture; open; evidence mixed].**
- The termwise Weil bound cannot give this. Even for banks in general position, the u's with
  z(u) = 0 contribute (κ−1)^{2a+1}p^{−1/2} relative error, because the bound has no cancellation
  across u.
- The natural route is Deligne's bound for smooth complete intersections. A diagonal system is
  smooth iff the columns are in general position, with error B·p^{a/2} and B = c(κ)^a against main
  term p^a. That would give p ≥ c(κ)² in general position. Hooley–Katz would cover singular
  configurations. Both are [known, standard; not checked against sources here]; this pass does
  not carry the route out.
- By Lemma R only s.s.c. banks matter, and they are not all smooth (planes may hold 3 columns).
- Evidence against an a-independent prime: the dead s.s.c. 7-column bank in F_13³ (κ = 3, §6),
  while every 5-column bank in F_13² is solvable. The first-moment count predicts
  5⁷/13³/4 ≈ 9 projective solutions there, so such banks are atypical rather than impossible.
- Refined conjecture: for each κ there is c(κ) such that N(κ, a, p) = 2a + 1 whenever p ≥ κ^{c(κ)}·
  poly(a). It is consistent with all data. Theorem E gives only p ≥ exp(O(a)) for exactly 2a + 1,
  or (2 + o(1))a at p = a^{ω(1)}.

## 4. TFNP placement and hardness

**(P1) PWPP [proved].** Let −1 ∈ P (κ | (p−1)/2) and n ≥ a log₂ p + 1.
- C(x) = Λx ∈ F_p^a, for x ∈ {0,1}^n, written in base p as an integer < p^a ≤ 2^{n−1}, is a
  poly-size circuit {0,1}^n → {0,1}^{n−1}.
- Any collision x ≠ x′ gives x − x′ ∈ {0, ±1}^n ∖ 0 ⊆ P₀^n with Λ(x − x′) = 0.
- So total SDE at these parameters Karp-reduces to the PWPP-complete COLLISION problem. The
  direction is SDE ≤ ternary SIS^∞ ≤ COLLISION; nothing goes back.
- For −1 ∉ P (e.g. κ = 2, p ≡ 3 mod 4) the collision argument fails outright: a set S with
  S − S ⊆ P₀ and |S| ≥ 2 forces −1 ∈ P. Paley-clique sets S with S − S ⊆ P₀ improve the
  pigeonhole bound only to a log_{|S|} p.

**(P2) Hardness at |P| = 2 [proved identity + known hardness].** For κ = (p−1)/2, P = {±1}. A
solution is then exactly a nonzero x ∈ {0, ±1}^n with Λx = 0 over F_p, i.e. homogeneous SIS^∞
with β = 1.
- It is total from n = ⌊a log₂ p⌋ + 1, which is near-linear when p = poly(a).
- For uniform Λ it is as hard as worst-case SIVP_γ with γ = Õ(√(an)) at p ≥ √n·a^δ [known: MP13
  Thm 1.1 as recorded in lit2 §3; ℓ₂ norm √n, ℓ∞ norm 1]. It is in PPA_p at fixed p [known: GKSZ,
  lit §3].
- This is the only total-regime hardness found, and it is at the opposite end from the target:
  there |P| is constant, while at fixed κ, |P| ≈ p/κ.
- Shortness has no counterpart at fixed κ [argued]. Every ternary-SIS instance with n > (2+η)a
  columns is an SDE instance (when −1 ∈ P) whose densest sub-bank already has
  ≥ 0.35p^{n−D}κ^{−n} SDE solutions (Theorem E). Almost all of them are not ternary, so the
  reduction SIS → SDE would need a gadget forcing small coefficients. P₀-membership of linear
  forms defines only Legendre-pattern sets, never intervals (the 8 Nov §6(b) dead ends).

**(P3) Fixed p [known: GKSZ via lit §3; that their Chevalley_p takes this explicit diagonal
input model is my reading, not rechecked].** For fixed p and n ≥ κa + 1 the system
Σ λ_{ji}y_i^κ = 0 is a Chevalley–Warning instance of total degree κa < n. GKSZ put Chevalley_p in
PPA_p. This needs p fixed: the PPA_p certificate uses p-element hyperedges.

**Prop. L* (unused padding) [proved].** Assume N(κ, d, p) = 2d + 1 for every d ≤ a (κ = 2: always;
every κ: p > (2κ−2)^{4a+2}). Let B ∪ G be a bank in F_p^a with ≥ 2a + 1 columns such that every
solution has x_G = 0. Let U = span G and u = dim U.
- G is dead (a solution of G would use G), so |G| ≤ 2u. Hence B has ≥ 2(a − u) + 1 columns and its
  projection B̄ to F_p^a/U is a total instance.
- If |G| = 2u:
  - No nonzero column of B lies in U: it would make G ∪ {b} solvable with x_G ≠ 0.
  - Every solution x̄ of B̄ satisfies Σ x̄_i λ_i = 0. Otherwise its lift w ∈ U is nonzero, and Lemma
    DC gives −w ∈ cone(G), hence a solution with x_G ≠ 0.
  - So B̄'s solutions are solutions of B: the padded total instance is no harder than the total
    instance B̄ in a − u dimensions.

This is the dead-pair Proposition L of 8 Nov (U ∩ span B = 0) made general. Its message is the
same: a hardness proof for the total regime needs a hard block of total arity, not padding.

**Remaining hardness options [argued].**
- A reduction from a believed-hard total problem into s.s.c. banks. By Lemma R, s.s.c. banks are
  the only place one can live.
- A fixed-κ analogue of the PWPP membership in the CW band 2a + 1 ≤ n < a log₂ p, which would need
  a pigeonhole on a set with differences in P₀. That is impossible for −1 ∉ P, and for −1 ∈ P
  only sets of size up to a Paley-type clique, about log p, are cheaply available.
- Neither is in hand.

## 5. Algorithms

- (A0) [proved, §3] Las Vegas κ^{(2+η)a+1}·poly at Theorem E's primes. With (E3)'s primes:
  (2κ)^{2a+1}·poly, since the relative error is < 1 − 2^{−n} and the success probability is
  ≥ (2κ)^{−n}·(1 − o(1)).
- (A1) [proved given report A Theorem A]
  - Theorem A holds for every J ≥ max(κ, 2) at arity F_J(a) = D_J(a) + max(2, 2J−4)a, with
    expected time κ^{3J−2}·poly at p ≥ max(8κ^{2E}E², 2Eaκ^E), E = 3J − 2.
  - Corollary A chose J = ⌈log_κ a⌉. The bound F_J(a) ≤ a²/(2(J−1)) + O(Ja) is minimized at
    J − 1 ≈ √a/2, giving F ≈ 2a^{1.5}. Exact values (`tradeoff.out`): a = 1024: J* = 17,
    F = 64,079, time exponent 49; a = 16384: J* = 65, F/a^{1.5} = 1.988.
  - For arity a^{1+α} with α ∈ [1/2, 1), take J ≈ a^{1−α}: time κ^{O(a^{1−α})}.
  - The additive (2J − 4)a absorption term blocks α < 1/2, and it is the only obstruction to a
    near-linear tradeoff in this family. D_J(a) alone tends to 2a as J → ∞.
  - Reducing the absorption load from 2(J − 1) to O(1) per round would give arity ≈ a²/(2J) + O(a)
    at time κ^{O(J)}, hence near-linear arity Ca in time κ^{O(a/C)}. Report A §10 shows that load
    O(1) fails without the Rado flat. Whether a cheaper Rado step exists is open.
- No algorithm at n = O(a polylog a) beats κ^{Θ(a)} [none found; trap 8: this is not hardness].

## 6. Computations

All in `2026-11-11-rees-sde-near-linear-total/`, exact integer arithmetic (the character check
uses complex floats only to compare with exact counts), `nice -n 19`, at most 2 processes.

- `sdecore.py`: coset tables, nullspace mod p, projective kernel enumeration and deadness test.
- `count_check.py` → `count_check.out` [exact]: the identity N_T = p^{−D}Σ_uΠS matches the
  kernel count on all 98 banks (κ ∈ {3, 4, 6}, p ≤ 61, d ∈ {1, 2}, random, dead-pair-plus and
  repeated-direction banks). The relative error always lies below Theorem E's sum, though the
  sum is vacuous (> 1) at these p. This is a sign/identity check only.
- `dead_w2.py` → `dead_w2.out` [exact, exhaustive up to GL₂ and P-scaling]: the largest dead bank
  in F_p¹ (m1) and in F_p² spanning (m2). Results:
  - κ = 3: m2 = 5 at p = 7, then 4 for p = 13, 19, 31, 37, 43, 61, 67.
  - κ = 4: m1 = 3, m2 = 6 at p = 13; m1 = 2, m2 = 5 at p = 17.
  - The run was stopped by hand during κ = 4, p = 29 (the DFS was too slow). κ = 4 at p ≥ 29,
    κ = 5 and κ = 6 were not computed.
- `dead_w3_search.py` → `dead_w3_search.out` [search, falsification only]: local search for dead
  (2d+1)-column banks.
  - Control κ = 3, p = 7, d = 3: found.
  - κ = 3, p = 13, d = 3: found a 7-column dead bank, verified by `verify_dead.py` (brute force over
    all 5⁷ vectors of P₀⁷: rank 3, 0 solutions). `analyze_bank.py` classifies it as s.s.c.: lines
    hold ≤ 1 column and two planes hold 3.
  - κ = 3, p = 19, d = 3 (600 s): not found; the best bank had 2 projective solutions.
  - κ = 3, p = 13, d = 4, n = 9 (600 s): not found; best 1. `found False` proves nothing.
  - κ = 4, p = 29, d = 3: found a 7-column dead bank, verified (`verify_k4p29.out`: rank 3,
    0 solutions). It is *tight*, not s.s.c. This is consistent with Lemma R:
    `lemmaR_trace_k4p29.out` shows 28 dead triples (1, a, b) in F_29. So N(4, 1, 29) ≥ 4, the
    hypothesis of R fails at d = 1, and p = 29 < κ⁴ = 256 lies below the range of the d = 1 case.
    The κ = 3, p = 13 bank is s.s.c., as Lemma R predicts from N(3,1,13) = 3 and N(3,2,13) = 5
    (the audit's prediction, §8). Both are passed falsification tests of Lemma R.
  - Saved checks: `verify_k3p13.out`, `analyze_k3p13.out`, `verify_k4p29.out`,
    `lemmaR_trace_k4p29.out`.
- `tradeoff.py` → `tradeoff.out` [exact]: the D_J recursion of report A at general J. It reproduces
  report A's F(64) = 970, F(256) = 7924 and F(1024) = 75272 at J = 6, 8, 10.

## 7. Weakest points

1. Theorem E is a direct Weil/Gauss count. It is very plausibly folklore for systems of additive
   forms over F_p, and no novelty is claimed. The prime conditions are not optimized.
2. Lemma R's algorithmic version relies on submodular minimization for the case detection. The
   existence version does not need it.
3. (A1) inherits Theorem A at J ~ √a. Report A asserts general J and checked the counting lemma
   exactly for J ≤ 20; the J ~ √a instance was not run.
4. P3 depends on the input model of GKSZ's Chevalley_p (not re-read).
5. The a-independent threshold is a conjecture with one piece of contrary small-p evidence.

## 8. Claude API audit (advisory)

One adversarial request: `claude-opus-5-5`, effort high, 32768 tokens, under $2. Prompt and
context are in `2026-11-11-rees-sde-near-linear-total/claude/`, the run bundle in `claude/run1/`.
Each finding's disposition is recorded below. No label above was promoted on the agent's
verdict.

Run: stop reason end_turn, 4,550 input and 21,670 output tokens, usage estimate USD 0.45 (an
estimate, not an invoice). The agent saw the claims file only (`claude/context_claims.md`), with
no code and no notes.

| Agent finding | Disposition |
|---|---|
| Claims 1, 2, 3, 5, 6 correct as written | Re-checked here line by line. Labels unchanged ([proved] was assigned before the audit, on my own derivation). |
| Claim 4 (Lemma R) mathematics correct; the p ≥ κ⁴ hypothesis is logically redundant in part (a), because a 1-dim s.s.c. bank is any 3-column bank | **Accepted.** p ≥ κ⁴ is what makes the d = 1 case hold unconditionally, so part (a)'s hypothesis is needed only for d′ ≥ 2. |
| Algorithmic Lemma R: a plain minimum of 2rk − \|·\| over B∖e detects only (A); (B) needs minimal minimizers over ordered pairs (e, g) | **Accepted.** This is the procedure already written in §3 (O(n²) SFM calls). |
| Corollary (b) positivity should be explicit | **Accepted.** §3 states ≥ 0.35κ^{−n} − κ^{−n}p^{−1} > 0 for p > 3. |
| Consistency prediction: given N(3,1,13) = 3 and N(3,2,13) = 5, Lemma R forces every dead 7-bank in F_13³ to be s.s.c. | **Accepted, and checked:** the found bank is s.s.c. (`analyze_bank.py`). This is a falsification test of Lemma R, and it passed. |
| Known-results question: N is a weighted Davenport constant D_A(F_p^d) with A = P (weighted Davenport literature recalled vaguely, nothing confident); the "≤ 2 dim U per subspace" condition is the Edmonds/Nash-Williams 2-covering criterion | **Open (priority).** No citation adopted (trap 10). The covering-criterion remark is correct and is a standard tool. |
| Remaining obligations: verify Lemma W independently | Lemma W is report A's (refereed there). Not re-derived here. |

## 9. Claim gates (must stay false), next question, next command

Gates:
- "Total SDE at near-linear arity is hard (fixed κ)": nothing shown. (P2) is |P| = 2 only.
- "In PPP/PWPP/PPA for large p at 2a + 1 ≤ n < a log₂ p": not shown.
- "N(κ, a, p) = 2a + 1 at an a-independent prime": conjecture, with contrary small-p data.
- "o(a²/log a) poly-time algorithm": none. (A1) is subexponential, not polynomial.
- Any novelty or priority claim, or any change to the paper's arity or tables: none.

Next hard question: decide N(κ, a, p) for s.s.c. banks at p = poly(a), κ = 3. Either prove a
c(κ)·poly(a) prime bound through Deligne/Hooley–Katz on the diagonal complete intersection
restricted to s.s.c. configurations, or construct dead s.s.c. families of growing dimension at
p ≥ κ^{2+ε}. This decides whether the total band at polynomial primes starts at 2a + 1 or at
(2 + c)a. Separately: does a cheaper Rado step (absorption load O(1)) exist? That is the only
visible route to a near-linear tradeoff.

Next command: `cd research/audits/reviews/2026-11-11-rees-sde-near-linear-total && nice -n 19
/opt/anaconda3/bin/python -I dead_w3_search.py`, extended to κ = 3, d ∈ {3, 4, 5} and
p ∈ {19, 31, 37}, with a structured s.s.c. seed. Expected artifact: `dead_w3_search.out` rows.
Acceptance test: every `found True` row is re-verified by `verify_dead.py` (0 solutions) and
classified by `analyze_bank.py`. A dead s.s.c. bank at p = 31, d = 4 would refute the refined
conjecture's "p ≥ κ^{c}·poly(a)" for small c. Failure to find proves nothing.
