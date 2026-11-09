# Rees diagonal SDE, worst case: how much of p ≥ poly(a) is essential? Lookahead steering, control fan-in, bounded-p obstructions

AI-only pass, 8 November 2026, one Claude Code session; not human-reviewed, no novelty claim.
Scripts and outputs: `2026-11-08-rees-sde-uniform-p/` (interpreter `/opt/anaconda3/bin/python`).
Only this file and that folder were written. `subquad.py` was copied to `subquad_u.py` (only
`leaf()` changed) and not edited. No git, no network, `make_numbers.py` not run.

Labels: **[proved]** (full proof here), **[exact]** (complete finite computation, script named),
**[sampled]**, **[argued]**, **[conjecture]**, **[literature]**. Notation is that of
`2026-11-07-rees-sde-subquad-A.md` (Theorem A): flag rounds 1..L, blocks, offsets β, defects
e_l ∈ U_{l−1}, steering functionals φ_{j,bb′}, sources Src, ρ = number of cross-class block pairs,
E = 3J − 2, G*_E(p) = least |Good| over ≤ E distinct offsets and arbitrary classes, and
LW_E(p) = min_{e≤E} κ^{−e}(p − e − (κ^e−1)(e−1)√p) ≤ G*_E(p) (Lemma W).

## 0. Verdict

1. **(1) No for ALG-T's leaves; the linear term has an exact, leaf-computable replacement.** A
   failure (cross-class coincidence at level j) is detected at once but cannot be repaired at
   level j (its offsets do not depend on s_j); only at the pair's *controlling variable*, the
   last-drawn variable with nonzero coefficient in the offset difference.
   - **Theorem L [proved, §2]:** lookahead back substitution (forbid, at each controlling variable,
     the one value zeroing each pair it controls) *never fails* if G*_E(p) ≥ N*_lev + 1 and
     (p−1)/κ ≥ N*_src + 1, N* = the leaf's **control fan-in** (polynomial-time computable).
   - **Corollary L1 [proved]:** Theorem A holds with zero-error back substitution at every prime
     p ≡ 1 (mod κ), p ≥ max(C_old(κ,J), κ^E(Er+2)): linear term halved, not removed.
   - **The linear term is real for ALG-T [proved structure + exact + sampled, §3].** On the
     exact-circuit banks EC, ALG-T returns a leaf where every s_l is irrelevant and all ρ = r
     pairs are source-controlled; for *every* source order the last source controls
     #{π : C_{π,last} ≠ 0} (= ρ generically; measured ≈ ρ(1−1/p)) pairs. Completion is the
     nowhere-zero problem t ∈ P^r, Ct ∈ (F_p^*)^r, whose pass success decays in r: exact at p = 5,
     0.875 → 0.175 (r = 4 → 20); sampled lookahead 0.005 (p = 11, r = 120), 0.035 (p = 29, r = 200).
2. **Constant thresholds under bounded fan-in [proved, conditional].** If every leaf had
   N* ≤ N_loc(E,κ) (max cross pairs in one round), Theorem A would hold, zero-error, at every prime
   p ≡ 1 (mod κ), p ≥ C_loc(κ,J), no a-dependence. Exact least primes: C_loc(2,3) = 583,991,
   C_loc(2,4) = 84,822,113, C_loc(3,3) = 172,103,821, C_loc(3,4) = 282,423,985,969. ALG-T violates
   bounded fan-in (EC; also design_mix, N*_lev = 29 at r = 40). A random scan order restores it on
   EC (N_lev ≤ 4, N_src ≤ 2; look 1.000 vs plain 0.49 at p = 29, r = 40) [sampled]. Whether some
   forward rule has N* = O_J(1) on every bank is **open** (Q-loc, §3.4).
3. **Tradeoff.** [proved] F(a,p) = O(a²/J(a,p)), J the largest admissible under
   p ≥ max(C_old, κ^E(Ea+2)); o(a²) iff log(p/a) → ∞. [conditional on Q-loc]
   F = O(a²/min(log a, log p)), and ⌊(a+2)²/4⌋ + 2a at every p ≥ C_loc(κ,3). For a ≤ 10⁴ the
   a-free Weil constant usually decides J (§4).
4. **(2) Bounded p: no route below the triangular count in the worst case [proved obstructions,
   argued conclusion, §5].** Pigeonhole identity Σ_c |Good(β,c)| = p + E(κ−1), so G*_E(p) = 0 for
   p < κ^E − E(κ−1) (p < 121 at (κ,J) = (2,3), p < 2173 at (3,3)) [proved]. Every ≥ 3-block,
   ≥ 2-class round has an offset vector (a cross-class coincidence) with empty Good [proved], so
   Θ(a) unsteered such rounds succeed jointly only with probability e^{−Θ(a/p)} and steering-free
   schemes gain one direction per round [argued]. Forced parallel columns save O(log_p² M). κ = 2, two classes: exact
   G*_3(p) = 1 for p ≤ 13, 2 for 17 ≤ p ≤ 23, so even N* = 2 steering is guaranteed only from
   p = 29; κ = 3: G*_3(p) = 0 at every p ≤ 97 [exact].
5. **Weakest step.** The EC decay *rate* e^{−Θ(r/p)} is exact/sampled, not proved; EC defeats only
   ALG-T's fixed scan order, not every algorithm.

## 1. Where the linear term enters

Lemma 2 (Q1 report) bounds the first-coincidence probability of each of the ρ ≤ Er/2 cross pairs
by 1/G*_E or κ/(p−1), and sums them. The per-pass failure is then ≤ ρ·2κ^E/p ≤ 1/2, which forces
p ≥ 2Erκ^E.

For a pair π = (j,b,b′), write F_π = −Σ_σ t_σ φ_π(σ) − Σ_{l>j} s_l φ_π(e_l). This is the offset
difference that must be nonzero. **Control:**
- ctrl(π) = m, the least l > j with φ_π(e_l) ≠ 0, if one exists;
- else ctrl(π) = (src,i), the last source σ_i (in a fixed order) with φ_π(σ_i) ≠ 0. It exists
  by (S).

In the draw order t_1, …, t_k, s_L, …, s_1 the controlling variable is the last-drawn variable
with nonzero coefficient in F_π (s_{j+1}, …, s_{m−1} have coefficient 0). Fan-in:
N_m = #{π : ctrl = m}, N_{src,i} = #{π : ctrl = (src,i)}, N*_lev = max N_m, N*_src = max N_{src,i}.

## 2. Theorem L (lookahead back substitution) [proved]

**Algorithm** (`lookahead.py: Ctl.backward`).
- *Sources.* For i = 1..k, draw t_i uniformly from P ∖ Bad_i, where
  Bad_i = {A_π/φ_π(σ_i) : ctrl(π) = (src,i)} and A_π = −Σ_{i′<i} t_{i′}φ_π(σ_{i′}).
- *Levels.* For l = L..1, compute β from τ_l. Draw s_l uniformly from Good_l(β) ∖ Bad_l, where
  Bad_l = {φ_π(τ_l)/φ_π(e_l) : ctrl(π) = l}. Set x on round l as in Lemma 2, and update
  τ_{l−1} = Π_{l−1}(τ_l) − s_l e_l.
- *Fallback (recorded).* If an allowed set is empty, draw from the full set. (Good is enumerated
  exactly for p ≤ 3·10⁵, drawn by rejection above.)

**Theorem L.** Assume the flag satisfies the hypotheses of Lemma 2: (F1), (F2), blocks inside
classes, ≤ E blocks per round, Src ≠ ∅ outside the rounds with span(Src) ⊆ U_L, and (S). Assume
also G*_E(p) ≥ N*_lev + 1 and (p−1)/κ ≥ N*_src + 1. Then the lookahead pass never uses the
fallback, and it returns a nonzero x ∈ (P ∪ {0})^M with Σ x_iλ_i = 0.

*Proof.*
- *One bad value per pair.* Fix π with control v.
  - Every other variable with a nonzero coefficient in F_π is drawn before v. When v is drawn,
    F_π = A − v·f with A already determined and f ≠ 0, where f = φ_π(e_m) if v = s_m and
    f = φ_π(σ_i) if v = t_i.
  - For v = s_m, A = φ_π(τ_m). Indeed τ_{m−1} = Π_{m−1}(τ_m) − s_m e_m. Also φ_π vanishes on Ω_m,
    because m > j and φ_π reads only round-j coordinates. And φ_π(e_l) = 0 for j < l < m. Hence
    F_π = φ_π(τ_j) = φ_π(τ_{m−1}) = φ_π(τ_m) − s_mφ_π(e_m).
  - Exactly one value of v zeroes F_π, and that value is in Bad. After v is drawn F_π is final,
    since every later variable has coefficient 0.
- *Allowed sets are nonempty (downward induction).*
  - Sources: |P ∖ Bad_i| ≥ (p−1)/κ − N_{src,i} ≥ 1.
  - Level l: every cross pair of round l is controlled by a source or by some s_m with m > l, so
    it is already drawn. By the first bullet each has F ≠ 0, so level l has no cross-class
    coincidence.
  - Equal offsets then lie in one class and merge, leaving e ≤ E pairwise distinct offsets. Hence
    |Good_l| ≥ G*_E(p) ≥ N*_lev + 1 > |Bad_l|.
- *Values.* These are the values of Lemma 2. Each x_i = δ_i(β_{b(i)} + s_l) ∈ P ∪ {0}, the sum
  telescopes to 0, and x ≠ 0 because t ∈ P^k. ∎

**Cost.** ctrl takes O(ρL) evaluations of φ; each level costs N_l evaluations plus one Good draw
(O(Ep) by enumeration, or expected p/(|Good| − N_l) rejection trials). Runs assert residual 0.

**Corollary L1 [proved].** Theorem A holds with zero-error back substitution at every prime
p ≡ 1 (mod κ) with p ≥ C_old(κ,J) and p ≥ κ^E(Er+2).

*Proof.* For p ≥ C_old, Lemma W gives G*_E ≥ p/(2κ^E) ≥ Er/2 + 1 ≥ ρ + 1 ≥ N* + 1, and
(p−1)/κ ≥ N* + 1 is trivial. ∎ (Against Theorem A's p ≥ 2Erκ^E: linear term halved, failure
probability ≤ 1/2 → 0. The sharp leaf-dependent condition is LW_E(p) ≥ N*_lev + 1 and
(p−1)/κ ≥ N*_src + 1.)

**Corollary L2 [proved, conditional].** Let N_loc(E,κ) be the largest number of cross pairs among
E blocks: 12 and 25 for κ = 2 (E = 7, 10), and 16 and 33 for κ = 3. Suppose a forward pass meets
Theorem A's budget F(r) and always yields leaves with N* ≤ N_loc. Then Theorem A holds at every
prime p ≡ 1 (mod κ) with p ≥ C_loc(κ,J), defined as the least p with LW_E(p) ≥ N_loc + 1 and
(p−1)/κ ≥ N_loc + 1.

Thresholds [exact] (`thresholds.py`, same search and spot checks as `weil_thresholds.py`;
least integer / least admissible prime):

| κ | J | E | N_loc | C0: LW > 0 | C_loc | C_old (Thm A constant) | Thm A linear |
|---|---|---|---|---|---|---|---|
| 2 | 3 | 7 | 12 | 580,658 / 580,663 | 583,982 / **583,991** | 2,322,604 | p ≥ 1792 r |
| 2 | 4 | 10 | 25 | 84,768,869 / 84,768,877 | 84,822,109 / **84,822,113** | 339,075,436 | p ≥ 20480 r |
| 3 | 3 | 7 | 16 | 172,029,470 / 172,029,493 | 172,103,820 / **172,103,821** | 688,117,852 | p ≥ 30618 r |
| 3 | 4 | 10 | 33 | 282,419,970,645 / …727 | 282,423,985,962 / **282,423,985,969** | 1,129,679,882,536 | p ≥ 1,180,980 r |

C_loc ≈ C_old/4. What the fan-in hypothesis buys is a-independence, not a much smaller constant.

## 3. Why the linear term survives: the exact-circuit family EC

### 3.1 Family and leaf [proved]

**EC(J,L)** (`families_u.py: ec_bank`), with r = (J−1)L:
- A random invertible matrix splits V = F_p^r = Π_1 ⊕ … ⊕ Π_L, with dim Π_l = J − 1.
- Circuit l consists of a basis u_1..u_{J−1} of Π_l and w = Σc_iu_i, where
  δ = (−c_1, …, −c_{J−1}, 1) is not monochromatic.
- Bank order: a random basis B (r columns), then the L circuits, then random padding up to F(r).

**Lemma E2.** On EC, ALG-T (`solve_T`, scan in bank order) returns the thm2 leaf with flag = the L
circuits and Src = B. Every e_l = 0, every round has J singleton blocks, and Ω_l = Π_l.

*Proof.*
- `init_state` reserves the first r independent columns, which are B.
- Suppose rounds < l realized U = Π_1 ⊕ … ⊕ Π_{l−1}. The scan of unused columns starts at
  circuit l, whose u's are independent mod U because the sum is direct. Then w closes a circuit
  of size J with relation δ.
- The defect is e = w − Σc_iu_i = 0. Since δ is not monochromatic, the round is not direct.
- `split_blocks` (E = J, |S| = J) gives J singleton blocks. Any J − 1 of the δ_iλ_i span Π_l,
  so U becomes U ⊕ Π_l.
- After L rounds U = V, and the pass returns "ok" before any padding column is scanned. ∎

**Lemma E1.** If every e_l = 0, then τ_{l−1} = Π_{l−1}(τ_l). So all offsets are functions of
τ_L = −Σ t_σσ, every pair is source-controlled (no φ(e_l) ≠ 0), and a pass succeeds iff every
Good_l(β_l(t)) ≠ ∅. Resampling the s_l cannot help.

*Proof.* (F2) gives τ_{l−1} = Π_{l−1}(τ_l) − s_l e_l, and e_l = 0. ∎

**Lemma E3 (κ = 2, J = 3).** Each round has class pattern (c,c,c′), with exactly 2 cross pairs;
their functionals are two independent differences of the Π_l coordinates, and the levels form a
direct sum, so the r = 2L pair functionals are a basis of V* and F = −Ct with C ∈ GL_r(F_p),
C_{π,σ} = φ_π(σ). Two-class G*_3(p) ≥ 1 for every p ≥ 5 (exact for p ≤ 61, `good_small.out`; all p
by E_cg(3,2) = ∅, two-relation report §4), so a pass succeeds whenever Ct is nowhere zero. For any
source order the last source σ_k controls exactly #{π : C_{π,k} ≠ 0} pairs (ρ for generic B).
Completing the leaf is thus exactly: find t ∈ P^r with Ct ∈ (F_p^*)^r, a nowhere-zero-point
problem of Alon–Jaeger–Tarsi type with coordinates in a coset [literature, recalled, not checked];
existence proofs there use the polynomial method and are not algorithmic. ∎

### 3.2 Data (κ = 2, J = 3; `ec_k2_J3.out`, `ec_k2_J3_large.out`, `ec_exact_small.out`)

Per-pass rates; "exact" = probability over all t ∈ P^r. Padded banks (r ≤ 40) also ran end to end
through ALG-T (leaf thm2, solved within 30 lookahead passes). N*_lev = 0 on every EC leaf.

| p | r (= ρ) | N*_src | plain | lookahead | exact |
|---|---|---|---|---|---|
| 5 | 4/8/12/16/20 | 4/5/9/13/19 | .88/.47/.37/.24/.22 | 1/.62/.50/.32/.23 | .875/.461/.352/.240/.175 |
| 7 | 4/8/12 | 4/8/12 | .78/.58/.49 | 1/.82/.62 | .778/.602/.456 |
| 11 | 20/40/80/120 | 20/33/74/110 | .45/.19/.015/.005 | .71/.33/.045/.005 | — |
| 29 | 40/100/200 | 40/94/193 | .46/.16/.02 | 1.00/.565/.035 | — |
| 101 | 40 | 40 | .80 | 1.00 | — |

- [sampled] N*_src tracks ρ(1 − 1/p) (p = 29: 96.5, 193 predicted; 94, 193 measured). The plain
  rate tracks (1 − 1/(2p))^r (p = 11, r = 40: 0.16 vs 0.19; p = 29, r = 200: 0.03 vs 0.02): each
  pair coincides with probability ≈ 1/p and about half of the coincidences are fatal.
- [argued, consistent with the data] Lookahead is perfect while N*_src ≲ p and collapses once the
  last source's bad values cover most of P (coupon collector). Repetition then costs e^{Θ(r/p)}
  passes, so polynomial time on these leaves needs p = Ω(r/log r): for Lemma-2-type completion of
  ALG-T leaves the linear term of L1 is necessary up to a log factor.

### 3.3 Under a random scan order EC becomes local [sampled; `ec_shuffle.out`]

With shuffled column order (p = 29, r = 16, 24, 40, two banks each) the forward pass builds mixed
circuits (only 1–2 exact rounds), N*_lev ≤ 4, N*_src ≤ 2, and lookahead succeeds in 200/200 passes
on every bank (plain 0.80 → 0.49). So EC refutes bounded fan-in for ALG-T's fixed rule only. Two
attempts to make EC shuffle-robust failed: padding by proportional copies creates size-2
monochromatic relations and ALG-T returns direct solutions (`ec_shuffle_copies.out`, 6/6; κ + 1
columns on a line always force one, Chevalley–Warning in dimension 1); large exact pieces force
monochromatic triples for κ = 2 by R(3,3) = 6 [argued].

### 3.4 Open structural question

**(Q-loc)** Is there a polynomial-time forward rule meeting budget F(r) + O(r) whose leaves have
N* ≤ N(J), independent of r, on every bank? A yes gives Theorem A at all p ≥ C_loc(κ,J)
(Corollary L2) and §4(b). The obstacle is exact or near-exact rounds (φ(e_{j+1}) = 0), which push
control up to sources in U_L. A source σ ∈ U_j could be injected at level j (add −t_σσ to τ_j and
draw t_σ there), making its control local, but an adversary can keep free columns out of low U_j
[argued]. Status: **open**, not a conjecture: the random-order evidence covers only EC and the §6
families.

## 4. Tradeoff F(a,p)

(a) **Unconditional [proved: Theorem A + Corollary L1].** Let J(a,p) be the largest J with
max(κ,3) ≤ J ≤ max(max(κ,3), ⌈log_κ a⌉) (so κ^E = poly(a)), p ≥ C_old(κ,J) and p ≥ κ^E(Ea+2).
Then F(a,p) = D_J(a) + max(2,2J−4)a ≤ a²/(2(J−1)) + O(Ja). For p = a^γ, γ > 1 fixed,
J ≈ ((γ−1)/3)log_κ a and F ≈ (3/(2(γ−1)))·a²/log_κ a; in general F = O(a²/log(p/a)) once
p ≥ a^{1+Ω(1)}. J → ∞ iff log(p/a) → ∞; if p < κ^7(7a+2) no J ≥ 3 is admissible and only the
triangular count (a+1)(a+2)/2 remains.

(b) **Under bounded fan-in [conditional on Q-loc].** Let J be the largest with p ≥ C_loc(κ,J);
C_loc grows like κ^{6J} up to poly(J) factors. Then J ≈ (1/6)log_κ p, capped at ⌈log_κ a⌉, and
F(a,p) = O(a²/min(log_κ a, log_κ p)) + O(a log a). This is o(a²) whenever p → ∞ with a, at any
rate. At J = 3 it is ⌊(a+2)²/4⌋ + 2a at every p ≥ C_loc(κ,3).

(c) **Numbers** (`tradeoff.out`; entries J / F; tri = (a+1)(a+2)/2):

| κ, a, rule | p = 10⁶ | 10⁷ | 10⁸ | 10¹⁰ | 10¹² |
|---|---|---|---|---|---|
| 2, 1000 (tri 501,501), (a) | — | 3 / 253,001 | 3 / 253,001 | 4 / 171,502 | 5 / 131,753 |
| 2, 1000, (b) | 3 / 253,001 | 3 / 253,001 | 4 / 171,502 | 5 / 131,753 | 6 / 108,704 |
| 2, 10⁴, (a) [Theorem A alone] | — | 3 / 2.503·10⁷ [—] | 3 / 2.503·10⁷ | 4 / 1.67·10⁷ | 5 / 1.26·10⁷ |
| 3, 1000, (a) | — | — | — | 3 / 253,001 | 3 / 253,001 |
| 3, 1000, (b) | — | — | — | 3 / 253,001 | 4 / 171,502 |

For a ≤ 10⁴ Theorem A and L1 differ only at (κ,a,p) = (2,10⁴,10⁷); everywhere else the a-free
constant limits J. The conditional rule (b) gains about one J step.

## 5. Bounded p (question 2)

**Lemma P (pigeonhole identity) [proved; asserted on every β in `good_small.py`].**
- (a) For pairwise distinct offsets β_0 = 0, β_1, …, β_{E−1}:
  Σ_{c∈Z_κ^E} |Good(β,c)| = p + E(κ−1). Hence G*_E(p) ≤ (p + E(κ−1))/κ^E, and G*_E(p) = 0 when
  p < κ^E − E(κ−1).
- (b) For fixed c and β_1, …, β_{E−1} i.i.d. uniform on F_p: E|Good| = |Q°|^E/p^{E−1} with
  |Q°| = (p+κ−1)/κ. So Pr[Good ≠ ∅] ≤ p((1 + (κ−1)/p)/κ)^E.

Here Q°_c = Q_c ∪ {0}, and Good(β,c) = {s : β_b + s ∈ Q°_{−c_b} ∀b}.

*Proof.*
- (a) Fix s.
  - If s ∉ {−β_b}, every β_b + s is nonzero, and exactly one c works: c_b = −cls(β_b + s).
  - If s = −β_{b₀}, which is a single b₀ because the offsets are distinct, then c_{b₀} is free
    and the rest are forced: κ assignments.
  - Summing over s gives (p − E) + Eκ.
- (b) |Good| = Σ_s 1[s ∈ Q°_{−c_0}]·Π_{b≥1} 1[β_b + s ∈ Q°_{−c_b}]. The factors for b ≥ 1 are
  independent, each with probability |Q°|/p, and the s-sum has |Q°| terms. Markov's inequality
  finishes. ∎

*Consequences.* Theorem A's absorbed rounds (E = 7, J = 3) have classes with empty Good at every
p < 121 (κ = 2) and p < 2173 (κ = 3); at J = 4, p < 1014 and p < 59,029. Rounds with spread
targets realize E blocks only with probability ≲ p/κ^E, so a round realizes ≈ log_κ p directions
at bounded p and the count stays ≳ a²/(2 log_κ p) [argued; "spread targets" is heuristic].

**Lemma R (robustness) [proved].** If a round has n ≥ 3 blocks whose classes are not all equal,
then some offset vector β (β_0 = 0) has Good(β) = ∅.

*Proof.*
- Pick blocks b, b′ with c_b ≠ c_{b′} and a third block b″. Give every block except b″ the offset
  y and give b″ the offset y + z, with y = 0 if b″ ≠ 0 and y = −z if b″ = 0 (so β_0 = 0).
- Any s ∈ Good has y + s ∈ Q°_{−c_b} ∩ Q°_{−c_{b′}} = {0}, so s = −y. The other blocks at offset y
  then read 0, which lies in every Q°.
- Block b″ needs z ∈ Q°_{−c_{b″}}. Choose z ≠ 0 outside that coset (possible since κ ≥ 2). ∎

The construction uses a cross-class coincidence (β_b = β_{b′}); with pairwise distinct offsets a
two-class 3-block round always has Good ≠ ∅ for p ≥ 5. So Lemma R says: a round realizes every
target without steering only if it has ≤ 2 blocks or is monochromatic. Unsteered, each such round
hits a fatal coincidence with probability ≳ 1/p, so Θ(a) of them succeed jointly with probability
e^{−Θ(a/p)} [argued, assuming roughly independent offsets across rounds]. With 2 blocks, the coincidence β_1 = 0 is the zero target, realized by x = 0 on the round; this
is why the triangular solver needs no steering. A monochromatic multi-block round still needs
G^mono_E(p) ≥ 1, which already fails at p = 5 and 7 for E = 3 (`good_small.out`).

Steering-free flag schemes therefore gain one direction per round. On banks all of whose
circuits mod U_{l−1} have size q_l + 1, they cost Σ_q (q+1), the triangular regime [proved for
such banks].

**Forced parallel columns [proved accounting].** If N > κ(p^d − 1)/(p − 1) columns lie in V/U,
d = dim V/U, then κ + 1 of them share a projective point; by Cauchy–Davenport
|Q°c_1 + … + Q°c_κ| ≥ min(p, κ|Q°| − κ + 1) = p, so κ of them realize every multiple of that
direction mod U. Forcing needs d ≤ log_p M + 1, so even counting every such round the saving is
≤ Σ_{q ≤ log_p M+1}(q−1) = O(log_p² M) against a²/2. Birthday collisions in random banks give
d ≲ 2 log_p M + 1, still O(log² M) [argued]. BKW-type pairing (differences of columns colliding
mod U; Sq coefficients survive because supports are disjoint) halves the column supply per level
and, composed with any quadratic solver, is worse [argued].

**Exact small-p Good data** [exact; `good_small.out` for κ = 2, p ≤ 53; `good_small2.out` for
κ = 3 and for κ = 2, E = 4 at p = 53, 59, 61]. Values are minima over all distinct-offset data:

| κ | p | G*_2 | G*_3 (≥ 2 classes) | G*_3 (all) | G*_4 (all) | empty fraction |
|---|---|---|---|---|---|---|
| 2 | 5, 7 | 1, 2 | 1, 1 | 0, 0 | 0 | E=4/5: .44/.69, .35/.63 |
| 2 | 11, 13 | 3, 3 | 1, 1 | 1, 1 | 0 | .22/.52, .17/.48 |
| 2 | 17, 19, 23, 29 | 4, 5, 6, 7 | 2, 2, 2, 3 | 1, 1, 2, 2 | 0 | .11/.40, .08/.36, .05/.30, .02/.23 |
| 2 | 31 … 53 | 8 … 13 | 3, 4, 4, 4, 5, 5 | 3, 3, 4, 4, 4, 5 | 0 | E=4: .016 → .0003 |
| 3 | 7, 13, 19, 31, 37, 43, 61, 67, 73, 79 | 0, 1, 1, 2, 3, 4, 5, 6, 6, 7 | 0 | 0 | 0 | E=3: .54 → .010 |

κ = 2: G*_4(p) (all classes) = 0 at every p ≤ 61; two-class G*_4 = 1 at p = 53, 61 and 0 at 59,
consistent with E_cg(4,2) = {5, …, 59}. κ = 3: G*_3 = 0 also at p = 97. Lemma P(a) held on every β.

**Small-p ALG-T runs** [sampled; `run_k2_tiny.out`; κ = 2, J = 3; 3 banks/cell; per pass]:

| p | uniform r=40 plain / look | EC r=40 look | adapt_mix r=40 look | fallback events |
|---|---|---|---|---|
| 11 | .20 / .57 | .27 | .63 | in every cell (\|Good\| = 1 occurs) |
| 13 | .23 / .81 | .43 | .93 | in every cell |
| 23 | .46 / 1.00 | .91 | 1.00 | EC r=40: 13; uniform r=40: 1 |
| 29 | .56 / 1.00 | 1.00 | 1.00 | EC r=40: 1 |
| 53 | .68 / 1.00 | 1.00 | — (r=16: 1.00) | 0 |

All 90 banks were solved by repetition; these banks have local fan-in (N*_lev ≤ 5) and say
nothing about worst-case banks at these p.

**Conclusion for (2) [argued].** At bounded p the proven worst-case count stays triangular,
(a+1)(a+2)/2. Steering-free rounds give one direction each (Lemma R); multi-block rounds need
κ^E ≲ p (Lemma P); Theorem A's absorbed rounds are dead below p = 121 (κ = 2). The steered 3-block
route (⌊(a+2)²/4⌋, Theorem C) needs a fan-in bound (open even at large p, §3.4) and G*_3(p) > N*,
which for κ = 2 fails at p ≤ 23 already for N* = 2. No o(a²) and no constant-factor route is known
at bounded p in the worst case; within flag schemes Weil steering has no combinatorial
replacement, since what it needs (|Good| > fan-in ≥ 1 in ≥ 3-block rounds, κ^E ≲ p) is exactly
what is missing.

## 6. Computations

Exact arithmetic, every witness verified, ALG-T in strict mode (all count asserts on). Families:
uniform, EC, break-folder generators (planted, twist, adapt_rado, adapt_mix, design_mix); budget F(r).

| artifact | setting | result |
|---|---|---|
| `thresholds.out` | exact least Lemma-W thresholds | §2 table |
| `good_small.out`, `good_small2.out` | exact G*_E(p), empty fractions, Lemma P(a) | §5 table; identity on every β |
| `ec_exact_small.out`, `ec_k2_J3*.out` | EC fan-in, rates, exact over P^r (the p = 29, r = 300 run was stopped) | §3.2 |
| `ec_shuffle.out`, `ec_shuffle_copies.out` | EC under random scan order; copy padding | §3.3 |
| `run_k2_small.out` | κ=2, J=3, p ∈ {101, 1009, 10007}, r ∈ {8,…,40}, 3 banks per cell | 315/315 solved; look = 1.000 and no fallback in every cell at p = 1009, 10007; p = 101 below; N*_lev ≤ 12 |
| `run_k2_tiny.out` | κ=2, J=3, p ∈ {11,13,23,29,53}, r ∈ {16,40}, uniform/EC/adapt_mix | §5 table; 90/90 solved |
| `run_k2_Cloc.out` | κ=2, J=3, p = 583,991 (C_loc ≤ p < C_old), r ∈ {8,…,40}, 2 banks per cell | 70/70 solved; plain = look = 1.000; no fallback |
| `run_k3_Cloc.out` | κ=3, J=3, p = 172,103,821 (C_loc ≤ p < C_old), 2 banks per cell; **partial**: stopped after r = 8, 16 (all 7 families) and r = 24 (uniform, EC, planted) | 34/34 solved; plain = look = 1.000; no fallback; N*_lev ≤ 16 (planted, r = 16) |
| `run_k2J4_Cloc_par.out` | κ=2, J=4, p = 84,822,113 (C_loc ≤ p < C_old), r ∈ {12, 24}, uniform/EC/twist/adapt_mix/design_mix, 2 banks per cell (the planned r = 36 run was not made) | 20/20 solved; plain = look = 1.000; no fallback; EC N*_src = ρ; N*_lev ≤ 10 (twist) |
| `tradeoff.out` | admissible J and F(a) | §4 |

Remarks. (i) At p = 101 (< 121, the E = 7 pigeonhole bound) lookahead met empty Good sets on
leaves with absorbed rounds (≤ 7 blocks): planted r = 16 (look .863), twist r = 24, 32 (.992,
.858), design_mix r = 24 (.967); every other p = 101 cell has look 1.000. (ii) **Non-local fan-in
occurs in a break family too:** at p = 583,991, design_mix r = 40 has N*_lev = 29 > N_loc = 12
(twist reaches 9), so "ALG-T leaves have N* ≤ N_loc except on EC" is false; lookahead still
succeeded because actual |Good| ≈ p/2^7 ≫ 29. (iii) The C_loc runs test the constant part only:
for r ≤ 40, p = 583,991 > 1792r, so Theorem A's linear condition holds but C_old = 2,322,604 fails.

## 7. Claim gates, weakest steps, next

**Gates that must stay false.** "Theorem A holds at all p ≥ C(κ,J)" (proved only under Q-loc,
which ALG-T violates: EC, design_mix). "The linear term is necessary for every algorithm" (shown
only for Lemma-2-type completion of ALG-T fixed-order leaves, up to a log factor, sampled rate).
"o(a²) is impossible at bounded p" (argued for flag schemes only). Anything at p = 3 or
κ = p − 1; the paper's arity statement is unchanged.

**Weakest steps.** (i) The EC decay rate: exact for r ≤ 20, sampled beyond, no proof of
e^{−Θ(r/p)}; a proof needs a lower bound on the zero coordinates of Ct for t uniform on P^r.
(ii) The "spread targets" premise behind a²/(2 log_κ p). (iii) The Alon–Jaeger–Tarsi
identification (recalled, unchecked).

**A referee should attack** Theorem L's claim that the control variable is the last-drawn nonzero
coefficient (it uses φ_π|Ω_m = 0 for m > j and φ_π(e_l) = 0 for j < l < m), and Lemma E2's claim
that ALG-T returns exactly the EC leaf (it depends on `init_state` reserving B first and on the
scan order).

**Next hard question.** Settle Q-loc: a forward rule (random order, source injection at level j,
re-splitting below exact rounds) with N* = O_J(1) at budget F(r) + O(r), or a bank family on which
every rule's leaves have N* = Θ(r).

**Next command.** After adding an adaptive family that keeps rounds exact under a random order:
`cd research/audits/reviews/2026-11-08-rees-sde-uniform-p && nice -n 10 /opt/anaconda3/bin/python -B ec_shuffle.py 2 3 29 8,12,20 3 200 9`.
Expected artifact `qloc_adapt.out`. Acceptance: N*_src/ρ → 1 along r ∈ {16, 24, 40} under the
random order (Q-loc fails for that rule), or N* ≤ 6 on every bank.
