# Referee report: Rees linear arity note (2026-11-13), Lemmas K, D, W and the reductions

AI only (one Claude Code referee subagent), pending human review. Hostile reading of
`research/audits/reviews/2026-11-13-rees-linear-arity.md` (the "note"). Compared against the core
`docs/papers/rees-hsp/core/main-core.tex`: sec:schedule1, sec:halving, lem:two-term,
def:schedule1h, thm:halving, cor:hcd, rem:kappa-two and lem:halved-exponent. Also compared against
the full version: `main.tex` prop:decoupled-sde, prop:triangular-sde and rem:triangular-scope at
lines 851–885, and `appendix-schedule2.tex` cor:app-s2-small at line 370.

No existing file was edited. No Git, no network. Every run used `nice -n 19`, one at a time, RSS
< 0.1 GB, and the longest run took 61 s. Scripts and outputs are in
`research/audits/reviews/2026-11-13-rees-linear-arity-referee/`, run with `/opt/anaconda3/bin/python`.

## 0. Verdicts

| item | verdict |
|---|---|
| §4 Lemma K(ii), κ = 3 contraction + existence of b | **PROVED** |
| §4 Lemma K(i), κ = 2 | **PROVED** (trivial) |
| §4 "consequence for the core" | **PROVED WITH FIXES**: it rests on prop:triangular-sde, which is **not in the core**, and the note under-claims the effect on the core (E_H(9) 38 → 36, §3 below) |
| §5 Lemma D (coset-doubling tower) | **PROVED given lem:two-term**. The exceptions table was reproduced exactly by independent code |
| §1 reductions, §2 Lemma C | **PROVED**, with two small notational fixes |
| §6 Lemma W | **PROVED WITH FIXES** (one counting line) |

No REFUTED or GAP verdicts.

## 1. Lemma K

**The coset conditions in the paper's exact sense.** Take the notation of prop:triangular-sde
(main.tex:865): z_m = ξ^m, Q_m = ξ^m P, and a decoupled contraction C_ij = z_i z_j(α_j + β_i) ∈ Q_0°.
This is the same condition as α_j + β_i ∈ g^{−(i+j)}P ∪ {0}, with α_0 = 1 and β_0 = 0. That is the
note's condition C_{−(i+j)} ∪ {0}, with C_ν = g^ν P.

I recomputed all nine entries for α = (1,0,−b), β = (0,b,−1), reading the indices as (i,j) with i
the β index and j the α index:
- (0,0) gives 1 ∈ C_0.
- (0,2) gives −b ∈ C_1.
- (1,0) gives 1+b ∈ C_2.
- (1,1) gives b ∈ C_1.
- (2,1) gives −1 ∈ C_0.
- (2,2) gives −1−b ∈ C_2.
- (0,1), (1,2) and (2,0) give 0.

Only −1 = (−1)³ ∈ P is used. The table in the note is correct, and so is the zero-diagonal
description β_i = −α_{i+1}.

**The count of b.** The character expansion is right. 9N is p − 2, plus four unit terms (χ^s(−1) =
1), plus two terms of the form J(χ^s, χ^{−s}) equal to −1, plus two terms ±χ(−1)J(χ,χ) of modulus
√p. So 9N ≥ p − 8 − 2√p, which is positive iff √p > 4, that is p ≥ 19. A cleaner closing step
needs no small-p cases. With N = (p+1+L)/9 (Gauss) and 4p = L² + 27M² with M ≠ 0, we have
|L| < 2√p, so 9N > (√p − 1)² > 0 for every p ≡ 1 (mod 3).

Independent check (`ref_counts_tower.py`, part 1) over all 3014 primes p ≡ 1 (mod 3) up to 60000,
for **both** choices of the coset generator (C_1 ↔ C_2): the count equals (p+1+L)/9 every time.
The minimum of N/(p−1) is 1/12, at p = 13. At p = 7 and 13, N = 1. At κ = 2, the least non-residue
ν always has ν − 1 a nonzero square (6056 odd primes ≤ 60000).

**The solver it plugs into, and where it lives.** prop:triangular-sde is stated and proved only in
the full version (main.tex:863–880, "AI-checked, pending human review"). Lean checks its algebra
from a supplied contraction (main.tex:1724, ReesSdeTriangular). **The core has no triangular solver.**
Its κ = 3 grade runs candidate (a) of def:schedule1h, arity G(3,a) = 27(a+1)³ with t = 2 and L = 1.
That matches the note.

I re-read the proof line by line:
- The weights are x_i = ζ δ_i(α_n + β_{cos δ_i}), and they lie in P0 because the cosets cancel.
- The value is ζ α_n e + ζ v.
- Round k uses a − k + 1 columns, so at most (a+1)(a+2)/2 columns in total.
- The back substitution keeps τ ∈ U_{l−1} and ends at τ = 0.
- The output is nonzero because the stop-round realisation has weight α_0 + β_0 = 1 on its
  normalised column, and no other round touches that column.

I found no gap. The output is a genuine κ-solution in the core's sense (w ∈ P0^M, w ≠ 0, roots r):
every nonzero weight lies in P, and its cube root exists.

**Re-implementation** (`ref_triangular.py`, written from the proposition, not from the note's
`sdelib.py`). It covers κ = 3 at every p ≡ 1 (mod 3) with p ≤ 103, both coset generators, and
random valid b, plus κ = 2 at every odd p ≤ 103, for a = 1..6. The banks are of 11 kinds: random,
zero, sparse, rank-1 with C_1 multipliers, rank-1, dead-pair cycles e_j·g^ν, C_1-unit columns,
repeated columns, {0,±1} entries, rank-2 with coset coefficients, and echelon. Every output was
checked for: weights in P0, nonzero, sum zero, at most (a+1)(a+2)/2 columns used, and an explicit
κ-th root for each weight.

| run | runs | failures |
|---|---|---|
| random and adversarial banks | 9900 | 0 |
| every valid b, both generators, p ≤ 103, a ∈ {2,4} | 288 | 0 |
| exhaustive a = 1: all p³ banks at κ = 3 (p ≤ 43) and κ = 2 (p ≤ 23) | 700282 | 0 |
| exhaustive a = 2, p = 7: all 9⁶ six-tuples from a fixed 9-element column set | 531441 | 0 |
| random a = 2, p ∈ {7, 13} | 40000 | 0 |
| **negative control** (invalid b) | 1590 | 1231 detected |

The negative control shows that the harness does detect wrong contractions. The note's own check
used only the first b and one generator; mine covers both. These are finite checks only.

**Las Vegas and determinism.** The claims in the note are correct, but conservative. Given g and b,
the solver is deterministic. A uniform draw gives b with probability N/(p−1) ≥ 1/12, and g with
probability 2/3. Given a cubic non-residue g, cube roots can also be taken deterministically by the
Adleman–Manders–Miller / Tonelli–Shanks method (standard, not re-derived here). So "Las Vegas
cube roots" is not forced.

**Fixes needed:**
- (K1) State in the note's §0 and §4 that the core contains no triangular solver. Using Lemma K
  there means importing prop:triangular-sde with its one-paragraph proof. It also means adding a
  candidate "(T) triangular, κ = 3, degree 2" to def:schedule1h, updating thm:halving(ii)–(iii)
  (constant K_3 ≤ 1), and adding the (g, b) draws to the Las Vegas preprocessing count n_pre of
  rem:is-import(d).
- (K2) In §0 item 1, "three exhaustive searches" means the three separately written programs of
  cor:app-s2-small, which search ten primes 7..79. Say so.

## 2. Lemma D

I re-derived the induction:
- The K_{j+1} → K_j split works because K_{j+1} ∖ K_j ⊆ g^{e_j}K_j.
- Weights that lie in both K_j and g^{e_j}K_j are sent to I, which is harmless.
- The object has type (1, c_j) with c_j = −g^{−e_j}, since Σ_J x_i λ_i = −u.
- The F1 finish needs y_1, y_2 ∈ P0, not K_j. That is the hypothesis P0 + c_j P0 ⊇ F_p^×, and it
  is correct, because K_j is not closed under multiplication.
- The arities multiply, giving N_1 = (a+1)^{m+1}.

lem:two-term (core, line 691) gives the hypothesis for every c at p ≥ 4κ⁴, with success
probability ≥ 1/(2κ) per draw. With e_j = 2^{j−1}, A_{m+1} = Z_κ at m = ⌈log₂κ⌉. The degree row
(3,3,4,4,4,4,5,5 for κ = 3,…,9,16) and the comparison with the core's ê(κ) row (core
lem:halved-exponent proof) are both correct.

**Exceptions table, reproduced independently** (`ref_counts_tower.py`, part 2: my own good-shift
test and my own BFS). Every row for κ = 2..12 matches the note's table exactly:
- κ = 8: no tower plan at 17, 41, 73, 89, 97, 137; degree 5 at 233 and 761.
- κ = 10: 8 primes with no plan, degree 10 at 131, degree 6 at 191, 211, 251, 281, 331.
- The largest exceptions are 29, 11, 43, 71, 761, 163, 331, 419, 541 for κ = 4..12.

At two primes ≥ 4κ⁴ for each κ, every shift is good, which is consistent with lem:two-term.

**Independent tower solver** (part 3): 12 pairs (κ,p), including p = 2521 and 9661 above 4κ⁴,
a ≤ 2, four bank families. That is 96 runs with 0 failures, and every output was re-verified.

There is no gap. Lemma D is an improvement *for the core* at odd κ ≥ 5 and p ≥ 4κ⁴ (5 → 4,
7 → 4, 9 → 5), but the class-9 maximum comes from small primes, so it does not move E_H(9). That
agrees with the note.

## 3. Under-claim: Lemma K lowers the core's own E_H

The note says "no headline claim is made", and it defers to the R8 calculus, which is not in the
paper. I recomputed the core's degree recursion (def:schedule1h) with one extra candidate:
degree 2 at κ = 3 (Lemma K + prop:triangular-sde), which also feeds the κ = 6 plans that halve over
κ = 3. The script is `eh_with_lemmaK.py`. It reuses, read-only, Field, t_len and T_sequence from
`2026-11-13-rees-headline-38-applied/halved_schedule.py`. It covers every prime 9 < p < 26244,
plus one prime ≥ 26244 in each unit class mod 5040.

| | E_H(c), c = 2..9 |
|---|---|
| control (no extra candidate) | 3, 6, 10, 14, 20, 25, 29, **38** (matches lem:halved-exponent(ii)) |
| with Lemma K | 3, 5, 9, 13, 17, 23, 27, **36** |

At c = 9 the maximum is still attained at p = 2521, 7561, 12601, 15121, … (p ≡ 1 mod 2520):
the grade degrees go from 2,3,3,5,4,7,4,9 to 2,2,3,5,3,7,4,9. This is a **core-only** improvement
of the headline, from 38 to 36. It depends only on lem:two-term, Lemma K and an imported
prop:triangular-sde, with no R8, Lemma S/F or chain material. Labels: the degree computation is a
finite computation (exact below 26244; above it, the core's own residue-class argument). The
improvement is CONDITIONAL on importing prop:triangular-sde into the core, which is AI-checked and
pending human review. Another agent's untracked `2026-11-13-rees-headline-below-38/` may already
cover this; I did not read it.

## 4. Reductions (§1–2) and Lemma W (§6)

- (1b) κ_d = p−1 means p−1 | d ≤ c < p, so d = c = p−1. This is correct. Note that (κ,p) = (2,3)
  arises only at class c = 2. For c ≥ 3, κ = 2 grades have p ≥ 5, so barrier B2 at κ = 2 concerns
  c = 2 alone. The note says "(c = 2)", but B2 in §7 does not.
- (1c) vs (1e) notation: (1c) defines N as the existence threshold, in [2a+1, κa+1], but (1e)
  writes "N(2,a,p) = 2a exactly". Fix: the maximum unsolvable size is 2a, so the threshold is
  N(2,a,p) = 2a+1. The dead-pair argument and Chevalley–Warning are correct.
- (1d) "BIS_p needs n > a log₂ p to exist" is true but weak. The worst-case BIS_p threshold is
  the Davenport constant a(p−1)+1 (Olson, as in rem:zero-sum).
- Lemma C: correct. −P ∪ P = P_{κ/2} when h is odd, with q = −1 and (−1)^h = −1.
- Lemma W: correct, but the line "fewer than |W|^n candidates", and the bound (|W|^n − 1)/p^a,
  need 0 ∈ W. In general the candidates number at most |W|^n, and the fraction is at most
  |W|^n/p^a. The conclusion is unchanged. The SIVP and MP13 citations were not checked here.
- The KOW, KOMSW and KMOSW claims rest on the repo's 11-07 literature note. I did not check them
  (no network).

## 5. Adversarial self-check

- Did I just confirm the note's own code? No. All three scripts were written from the paper text
  (prop:triangular-sde, lem:two-term, def:schedule1h) before I looked at `sdelib.py`. The only
  shared code is the read-only 1H calculator in §3, and its control row reproduces the published
  38.
- The E_H = 36 figure is a degree count. It assumes that adding a candidate to def:schedule1h
  leaves the rest of the paper's argument intact (arity tie rules, the C^H_c constants, and the
  Las Vegas budget). I checked that the triangular constant is ≤ 1, but I did not re-run the
  arity tables or Table tab:query-crossover. Treat 36 as CONDITIONAL until an integrator re-runs
  `lem:halved-exponent`'s full computation with the new candidate.
- Finite checks only falsify. The PROVED labels for Lemmas K and D rest on the arguments re-derived
  above, not on the runs.
- Everything here is AI-checked, pending human review. prop:triangular-sde itself has had no human
  review.
