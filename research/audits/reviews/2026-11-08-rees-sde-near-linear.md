# Diagonal SDE, near-linear arity: the promise problem is Legendre-PRF-hard up to M = 2a − log_κ p + 4; only the total band [2a − log_κ p, κa + 1] is open

AI-only pass, 8 November 2026, one Claude Code session. Not human-reviewed, not in Lean, no
novelty or priority claim. Scripts and outputs: `2026-11-08-rees-sde-near-linear/`, interpreter
`/opt/anaconda3/bin/python`. Only this file and that folder were written: no `.tex`, no git, no
STATE/handoff edit, `make_numbers.py` not run. Inputs read: `main.tex` prop:triangular-sde and
rem:triangular-scope, `appendix-sde-side.tex` rem:sde-worst-case(b) (the a+2 reduction), the
7 November reports A (§0, §10), B (§0–§4, §6–§9) and lit, `STATE.md` ("Now"), `TRAPS.md`.

Labels: **[proved]** (complete proof here), **[exact]** (complete finite computation, script
named), **[sampled]** (exact arithmetic on random samples), **[argued]**, **[conjecture]**,
**[literature]** (from the cited repository file or from memory, marked which).

Notation. κ ≥ 2, p ≡ 1 (mod κ) prime, g a generator of F_p^×, P = (F_p^×)^κ, P₀ = P ∪ {0},
cos : F_p^× → Z_κ the coset index (cos(y) = e iff y ∈ g^e P). A bank is λ₁..λ_M ∈ F_p^a; a
solution is x ∈ P₀^M ∖ {0} with Σ x_i λ_i = 0. SDE(a, M) is the search problem "given a bank
with a solution, return one"; it is total when M ≥ κa + 1 (Chevalley–Warning, CW). For κ = 2,
cos = (1 − χ)/2 with χ the Legendre symbol, and P₀ = Sq.

## 0. Verdict

**Negative on the goal, with a hardness theorem that locates the obstruction.** No Las Vegas
poly(a, log p) algorithm at arity o(a²/log a) was found, and none should be expected below the
total regime:

1. **Theorem H [proved, reduction; hardness conditional on the power-residue PRF].** For every
   κ ≥ 2, every prime p ≡ 1 (mod κ), every a, and every M with a + 2 ≤ M ≤ 2a + 4 − ⌈log_κ p⌉ − λ,
   an algorithm that solves every solvable bank at (a, M) in time T recovers the key θ of the
   power-residue PRF c ↦ cos(θ + c) (κ = 2: the Legendre PRF) from m = 2a − M + 4 queries at
   uniformly random points, in time T + poly(a, M, log p), with failure probability
   ≤ 2κ^{1−λ} for p ≥ 4κm. The instances are the a+2 instances of rem:sde-worst-case(b) padded
   with k = M − a − 2 **dead pairs** (two proportional columns (μ, cμ) in a fresh dimension with
   −c ∉ P, which no solution can use). The case k = 0 is the paper's remark (b).
2. **Corollary H1 [proved given 1].** For every ε ∈ (0, 1]: if some algorithm solves every
   solvable bank with M = ⌊(2 − ε)a⌋ columns in poly(a, log p) time for all primes p ≥ P₀(a)
   with P₀ polynomial, then the power-residue PRF has a poly(log p) key-recovery attack from
   O(log p) random queries, for all large p. In particular M = O(a^{1+ε'}), O(a polylog a) and
   every M ≤ (2 − ε)a are excluded for the promise problem at primes p ≤ κ^{εa − O(1)}, under
   the assumption already used in the paper (rem:sde-worst-case(b)). Not uniform in p: a solver
   that only works at p ≥ 2^{a²} is untouched, because the hard block needs log_κ p ≤ a + 2.
3. **Corollary H2 [conditional on Assumption LP of report B §4].** The same construction with
   m = ω(log a) queries gives: for every p ≥ m²κ^{2m}, including p ≥ 2^{poly(a)}, no
   poly(a, log p) algorithm solves every solvable bank at arity 2a − m + 4 = 2a − ω(log a).
4. **Limit of the technique (Proposition L) [proved for κ = 2; argued for κ ≥ 3].** Dead weight
   has at most 2 columns per dimension (κ = 2: by CW; κ ≥ 3: exhaustive at a = 1, exact counts
   at a = 2, Weil heuristic in general), and a one-parameter hard block with m conditions has
   deficiency 2a − M = m − 4 ≥ log_κ p − 4. So no reduction of the form "dead padding + hard
   block with a unique solution" reaches arity 2a + 1. For κ = 2, Theorem H stops
   log₂ p − 3 columns short of the CW threshold 2a + 1, and that is where totality starts.
5. **What this says about the open algorithmic question.** Every candidate near-linear
   algorithm must use totality in an essential way: it cannot be a "find a solution if one
   exists" procedure that happens to be run at arity ≥ 2a + 1, because such a procedure at
   arity 2a − log p would break the PRF. Directions (a) and (b) of the brief do not use
   totality: (a) returns to the piece schemes of report B (its Proposition E: isotropic
   subspaces presuppose the quotient problem; §6 below adds that the pencil's rational singular
   members give exactly the composite/realized-subspace structure), and (b) at p ≥ 2^{poly(a)}
   produces either SIS^∞-type problems (ternary kernel vectors at M ≥ a log₂ p + 1, a PPP-type
   total problem with no known poly algorithm [literature, lit §3]) or the same residuosity
   conditions. Neither was pursued to an algorithm; §6 records the two dead ends in one
   paragraph each.
6. **Computations [exact, sampled].** `reduction_check.py`: exhaustive enumeration of the
   whole kernel on 14 tiny instances (κ ∈ {2, 3, 4}, p ≤ 43, kernel dimension 4, up to
   3.4·10⁶ vectors each): every nonzero kernel vector in P₀^M has all dead-pair parameters zero
   and gives a key whose pattern is a constant shift of θ's pattern; brute-force solving of 12
   instances at p ≈ 10⁶–2·10⁶ (a up to 225, M up to 427, 2a − M = 9..23) recovered θ every
   time, every witness verified. `density_check.py`: at a = 1 every bank of three nonzero
   columns is solvable for κ ∈ {2, 3, 4, 6} and p ∈ {101, 103, 109} (exhaustive over banks), the
   dead pairs are exactly the (κ−1)(p−1)/κ predicted; at a = 2, κ = 3, p ∈ {1009, 1033}, the
   dead-pair bank with M = 4 has no solution and every tested bank with M = 5 = 2a + 1 < κa + 1
   has one (§7). Finite computations prove nothing about scaling.

## 1. Reformulation [proved, elementary]

Let Λ ∈ F_p^{a×M} have the bank as columns, rank a, kernel K of dimension k = M − a, and let
Φ : F_p^k → K be a basis. The coordinates x_i = ℓ_i(t) of Φ(t) are M linear forms in k
variables, and SDE(a, M) is: find t ≠ 0 with cos(ℓ_i(t)) ∈ {0, ⊥} for all i, i.e. every
ℓ_i(t) ∈ P₀. For k = 2 and t = (s, t₀) this is the one-parameter pattern problem
"find s with cos(s + c_i) = ε_i for i = 1..M, up to a common shift" (Proposition B′ of report B,
and (b) of rem:sde-worst-case): a + 2 columns ⟺ a + 2 residuosity conditions on one parameter.
For general k it is the k-parameter version. The number of solutions, heuristically
p^{k−1}/κ^{M} projectively, is ≥ 1 for M ≤ (k − 1)log_κ p; with k = M − a this is
M ≥ a(1 + 1/(log_κ p − 1)), far below CW, so "solvable" and "total" are different regimes
whenever p is large. All results below are about the promise problem SDE(a, M) at M < κa + 1.

## 2. Dead pairs and the density bound

**Lemma D (dead pair) [proved].** Let μ ∈ F_p^a ∖ {0} and c ∈ F_p^× with −c ∉ P. In any bank
containing the two columns μ, cμ, with μ outside the span of the other columns, every solution
has x = 0 on both. *Proof.* Σ x_i λ_i = 0 and μ ∉ span(others) force x_μ + c x_{cμ} = 0. If
x_{cμ} ≠ 0 then x_{cμ} ∈ P and x_μ = −c x_{cμ} ∈ P₀ ∖ {0} = P, so −c ∈ P, contradiction. ∎
In kernel coordinates (x_μ, x_{cμ}) = (t, dt) with d = −1/c, so the condition reads d ∉ P.

**Lemma CW₂ (density ≤ 2 for κ = 2) [proved].** A set of n columns in F_p^d with no nonzero
P₀-solution has n ≤ 2d: CW at degree 2. So dead weight costs at least one dimension per two
columns, and the pairs of Lemma D attain this.

**Remark (κ ≥ 3) [exact at a ≤ 2, argued in general].** CW only gives n ≤ κd. But three
nonzero columns in F_p¹ always have a solution for the tested (κ, p) (§7), and for a = 2 every
tested 5-column bank at κ = 3 has one. The Weil count N = p^{−a}Σ_y Π_i S(⟨y, λ_i⟩) with
|S(c)| ≤ (κ−1)√p for c ≠ 0 gives N > 0 for columns in general position once n ≥ 2a + 1 and
p ≫ κ^{2n}; adversarial banks need a recursion into hyperplanes carrying many columns, not
written out here. If this holds, dead weight has density ≤ 2 for every κ at p ≥ κ^{O(a)}, and
the "total" threshold at such primes is 2a + 1 rather than κa + 1. Nothing below depends on it.

## 3. Theorem H

**Setting.** Oracle O_θ(c) = cos(θ + c) for c ≠ −θ, and ⊥ at c = −θ. Parameters m ≥ 2
(queries), k ≥ 0 (dead pairs), a = m + k − 2, M = m + 2k, so that

M − a = k + 2,  2a − M = m − 4,  m = 2a − M + 4,  k = M − a − 2.

**Construction R(θ; m, k).** Draw c₁..c_m i.i.d. uniform in F_p; if any O(c_i) = ⊥ output
−c_i; redraw if all c_i are equal. Put ε_i = O(c_i), η_i = g^{−ε_i} (so η_i(θ + c_i) ∈ P), and
fix d ∉ P (d = g). Define Φ : F_p^{k+2} → F_p^M by

Φ(s, t₀, t₁..t_k) = ( η_i(s + c_i t₀) )_{i≤m} ⊕ ( t_j )_{j≤k} ⊕ ( d t_j )_{j≤k}.

Φ is injective (the first block has rank 2 since the c_i are not all equal; the pair blocks
have rank k on disjoint coordinates). Let Λ ∈ F_p^{a×M} have row space (im Φ)^⊥; then
ker Λ = im Φ and rank Λ = M − k − 2 = a. The bank is the columns of Λ. (In column language the
last 2k columns are k pairs (μ_j, −d^{−1}μ_j) in k fresh dimensions, dead by Lemma D since
−(−d^{−1}) = d^{−1} ∉ P; the first m columns are the a+2 instance of rem:sde-worst-case(b) in
m − 2 dimensions.) Cost: one Gaussian elimination, poly(M, log p).

**Theorem H [proved].** Let A return, in time T, a solution for every bank at (a, M) that has
one. Then the following procedure recovers θ: build R(θ; m, k), run A, get x ∈ P₀^M ∖ {0} with
Λx = 0, solve x = Φ(s, t₀, t) by linear algebra, output K = s/t₀ if t₀ ≠ 0, and check K on λ
fresh queries. It uses m + λ queries at uniform points, time T + poly(a, M, log p), and fails
with probability at most κ^{1−m}(1 + κ/(p−1))^m + κ^{1−m}p(1 + κ/(p−1))^m, which is
≤ 2κ^{1−λ} when m ≥ ⌈log_κ p⌉ + λ and p ≥ 4κm.

*Proof.* (i) *The instance is solvable:* x* = Φ(θ, 1, 0) has x*_i = η_i(θ + c_i) ∈ P for
i ≤ m and zeros elsewhere, and Λx* = 0. (ii) *Dead pairs are unused:* for any solution
x = Φ(s, t₀, t), the coordinates t_j and d t_j both lie in P₀; if t_j ≠ 0 then t_j, d t_j ∈ P
and d ∈ P, contradiction. So t = 0 and x is supported on the first m coordinates. (iii) *t₀ ≠ 0
unless the pattern is constant:* if t₀ = 0 then x_i = η_i s with s ≠ 0 and cos(x_i) =
cos(s) − ε_i = 0 for all i, so all ε_i equal cos(s). Over the draw of the c_i, the values
θ + c_i are i.i.d. uniform on F_p ∖ {0} (we are in the branch with no ⊥), so
Pr[all ε_i equal] ≤ κ(1/κ + 1/(p−1))^m... more precisely ≤ κ·(1/κ + 1/(p−1))^m ≤
κ^{1−m}(1 + κ/(p−1))^m. (iv) *Shifted pattern:* if t₀ ≠ 0, put K = s/t₀ and σ = cos(t₀).
Then x_i = η_i t₀(K + c_i), so for each i either K = −c_i (x_i = 0) or
cos(K + c_i) − cos(θ + c_i) = −σ. If K = θ then σ = 0 and the output is correct. (v) *Wrong keys
are rare:* fix K ≠ θ and σ. For c uniform on F_p ∖ {−θ}, the map c ↦ (K + c)/(θ + c) is a
bijection onto F_p ∖ {1}, and cos(K + c) − cos(θ + c) = cos((K + c)/(θ + c)) for c ≠ −K; so
Pr_c[c = −K or cos(K + c) − cos(θ + c) = −σ] ≤ 1/(p−1) + 1/κ, independently over i. A union
bound over K ∈ F_p ∖ {θ} and σ ∈ Z_κ gives probability ≤ κ p (1/κ + 1/(p−1))^m that some wrong
K is consistent with every i; only such K can be output by (iv). (vi) Adding (iii) and (v) and
using (1 + κ/(p−1))^m ≤ e^{κm/(p−1)} ≤ 2 for p ≥ 4κm gives the bound; the λ fresh checks
make the failure one-sided (the procedure never outputs a wrong key it could detect). ∎

**Corollary H1 [proved given Theorem H].** Fix ε ∈ (0, 1], a polynomial P₀, and suppose A
solves every solvable bank at (a, ⌊(2−ε)a⌋) for all a ≥ a₀ and all primes p ≥ P₀(a), in time
poly(a, log p). Given a PRF prime p, set a = ⌈(⌈log_κ p⌉ + λ − 4)/ε⌉ (so a = O(log p) for fixed
ε, λ), M = ⌊(2 − ε)a⌋, m = 2a − M + 4 ≥ ⌈log_κ p⌉ + λ, k = M − a − 2 ≥ 0 (as M ≥ a + 2 once
a ≥ 2/(1−ε), and for ε = 1, M = a, we instead take M = a + 2 ≤ (2 − ε)a + 2; the statement
then concerns arity a + 2, the paper's case). For large p, p ≥ P₀(a) = polylog(p) holds, so A
applies, and Theorem H recovers θ from O(log p) queries in time poly(log p) with failure
≤ 2κ^{1−λ}. ∎ The hypothesis "for all p ≥ P₀(a)" is used only to know that A works at the one
prime p = κ^{Θ(εa)} the PRF hands us; any solver whose prime range contains some
p ≤ κ^{εa − λ + 4} is covered. A solver that needs p ≥ κ^{a+3} is not (then log_κ p > a + 2
and the hard block does not fit; §4).

**Scope.** Theorem H is about the promise problem: the instances have M = 2a − m + 4 < κa + 1
and an algorithm for the total regime M ≥ κa + 1 is never run on them. The assumption is the
one in rem:sde-worst-case(b): key recovery for the power-residue PRF from O(log p) random
queries takes classical time superpolynomial in log p. It is a cryptographic conjecture, not
a standard complexity assumption [literature: appendix-sde-side.tex (b);
2026-11-05-rees-sde-subquadratic-check.md §1.5 for the Damgård / Beullens et al. citations;
nothing fetched here]. For κ = 2 it is the Legendre PRF.

## 4. Larger primes: Corollary H2 and the limit of the technique

**Corollary H2 [proved reduction; hardness conditional on Assumption LP, report B §4].**
Assumption LP says: random one-parameter instances of size m ("find s with cos(s + c_i) = ε_i,
i ≤ m") need time κ^{Ω(m)} at p ≥ κ^{2m}poly(m). Run R with the LP instance in place of the
PRF pattern (no key; the ε_i are the given pattern) and any k ≥ 0. By (ii)–(iv) every solution
of the padded bank is supported on the LP block and returns K with a shifted pattern; a shift
σ ≠ 0 is itself an LP solution for the shifted pattern, which is a random instance of the same
size, so an LP solver that handles all patterns is obtained with one extra loop over σ ∈ Z_κ.
Hence, under LP, no poly(a, log p) algorithm solves every solvable bank at (a, 2a − m + 4)
with m = ω(log a), for any prime p ≥ m²κ^{2m}, in particular for p ≥ 2^{poly(a)}. The prime
range is now unbounded above, at the price of the non-standard assumption.

**Proposition L (limit) [proved for κ = 2].** Consider any reduction whose instance is a bank
whose solutions all lie on a block of n columns in n − r − 1 dimensions (an r-parameter
projective family) together with dead weight. For κ = 2 the dead weight has ≤ 2 columns per
dimension (Lemma CW₂), so the arity satisfies M ≤ 2a − (2(n − r − 1) − n) = 2a − n + 2r + 2.
A block with a unique projective solution recoverable from a PRF needs n ≥ r log_κ p − O(1)
(a random point of P^r matches n conditions with probability κ^{−n}, and there are p^r
points), so 2a − M ≥ r log_κ p − 2r − O(1) ≥ log_κ p − O(1). Theorem H attains this at r = 1.
So reductions of this shape stop log_κ p − O(1) columns short of 2a + 1 = the CW threshold
for κ = 2, and cannot reach the total problem. ∎ For κ ≥ 3 the same holds if the density
remark of §2 holds [argued].

Between 2a + 4 − log_κ p and κa + 1 (κ = 2: a band of log₂ p − 3 columns ending at the CW
bound) nothing is known either way. For p = poly(a) the band is O(log a) columns wide. Any
algorithm there must use totality: it has no promise-problem counterpart one column below.

## 5. Relation to reports A and B and to the paper

- Report A (Theorem A, O(a²/log a) at p ≥ poly(a)) and report B (Theorem B: piece schemes need
  Ω(a²/log a) on random banks at p ≥ 2^{Õ(M)}) concern algorithms at arities where every bank
  (A) or every random bank (B) is solvable. Theorem H concerns adversarial solvable banks at
  arity below 2a and primes p ≤ κ^{a+O(1)} (H1) or any p (H2). The three are consistent and
  disjoint: A's algorithm is never asked to solve an H instance (its arity is a²/log a), and
  H's instances are far from random (k proportional pairs).
- B's Assumption LP is the k = 0 case of H2's hardness source; B's Proposition B′ (circuit
  pieces solve LP) is the converse direction at a single piece. H adds only the padding, which
  turns "arity a + 2" into "arity 2a − log_κ p + 4" at no cost in the assumption.
- The paper's rem:sde-worst-case(b) is Theorem H with k = 0 (its union bound is reused in (v)).
  Integrating H would change one sentence there: "no classical algorithm solves every solvable
  instance with M = a + 2 columns" becomes "... with any a + 2 ≤ M ≤ 2a + 4 − ⌈log_κ p⌉ − λ
  columns, hence with M = (2 − ε)a columns at primes p ≤ κ^{εa − λ + 4}". The sentence "It says
  nothing about arities at which every instance is solvable" stays, now with the quantitative
  gap of §4. Owner decision; not done here.
- B's claim gate "Ω(a²) barrier — false for the class" is untouched: H is not a lower bound
  for total arities.

## 6. Directions (a) and (b): why they were not pursued [argued]

**(a) Geometry of the pencil (κ = 2).** The a forms Q_j(y) = Σ_i λ_{ij} y_i² span a pencil
whose members Q_c = Σ_j c_j Q_j have diagonal matrix ⟨c, λ_i⟩. Killing a − 1 variables
(c ⊥ λ_i for i ∈ T, |T| = a − 1) gives a cone with vertex span(e_i : i ∈ T) over the diagonal
quadric Q_c in the other M − a + 1 variables. For a point y of that quadric, the a-dimensional
space span(y, e_T) lies on Q_c and the remaining a − 1 forms restrict to the diagonal system
s²Q_j(y) + Σ_{i∈T} λ_{ji} u_i² = 0: an SDE at (a − 1, a) whose extra column Q(y) = Σ y_i² λ_i
is exactly a composite of report B (§6, direction 1), constrained to the hyperplane c^⊥. The
lines through intersection points of the arrangement {ℓ_i = 0} ⊂ P^{k−1} (two forms through
one point become proportional on the line, merging two conditions) reduce arity a + k to a
one-parameter problem with a − k + 4 conditions plus two monochromaticity conditions on
(k − 1)-subsets, each of probability κ^{−(k−2)}: these are B's coset-oblivious stop pieces.
Every route tried re-created a realized-subspace scheme, as B's Proposition E predicts.
Not pursued further; no new mechanism.

**(b) Large p.** (i) Lifting to Z: s_i small integers makes Σ s_i² λ_i ≡ 0 a vector of the
kernel lattice (det p^a, dimension M) whose entries are perfect squares; LLL controls norms,
not squareness. (ii) Ternary vectors: at p ≡ 1 (mod 4), {−1, 0, 1} ⊂ Sq, so by pigeonhole
every bank with M ≥ a log₂ p + 1 has a {−1, 0, 1}-solution (collision of two 0/1 vectors) —
a second total regime at near-linear arity M = O(a log p). Finding it is SIS^∞ with ternary
solutions at m = n log q, a PPP-type total problem (GKSZ; lit §3) with no known poly
algorithm; KOW's worst-case SIS^∞ algorithm needs m ≥ Cn^k with s = ⌊q/(2k)⌋, useless at
s = 1 [literature, lit §1.1]. (iii) Polynomial parametrizations s_i = f_i(u) with
Σ f_i(u)² λ_i ≡ 0 as a polynomial identity give a system with the same variables/equations
ratio M/(2a); and f + c_i = h_i² for all i forces h_i constant (the curve y_i² = s + c_i,
i ≤ m, has genus 2^{m−2}(m − 3) + 1 by Riemann–Hurwitz, so no rational parametrization for
m ≥ 4). None of these breaks B's cost model; (ii) is the only one that is total, and it is
believed hard.

## 7. Computations

All in `2026-11-08-rees-sde-near-linear/`, exact integer arithmetic, interpreter
`/opt/anaconda3/bin/python -B`.

`reduction_check.py` → `reduction_check.out`.
- Exhaustive kernel enumeration [exact]: (κ, p, m, k) ∈ {(2, 29, 6, 2), (2, 37, 7, 2),
  (3, 31, 5, 2), (3, 43, 6, 2), (4, 29, 6, 2)}, three keys each (one run hit the oracle zero
  and returned the key directly). All p^{k+2} kernel vectors (up to 43⁴ = 3.4·10⁶) were
  enumerated; every nonzero one in P₀^M had t = 0 and t₀ ≠ 0, and every extracted key K had a
  pattern equal to θ's pattern shifted by one constant class (the `shift-classes` field has one
  element per key). Spurious keys with a nonzero shift appear at these tiny p (e.g. K = 27 with
  shift 1 at p = 29), as the union bound allows at λ ≈ 1–2; θ was always among the keys. The
  run with κ = 4, p = 29 ≡ 5 (mod 8), where −1 ∉ P, exercises the dead-pair criterion d ∉ P
  (a first version used −d ∉ P, which is the column-ratio criterion, and would have let pairs
  with −1 ∉ P live; corrected before the recorded run).
- Brute-force end-to-end [sampled]: (κ, p, λ, k) ∈ {(2, 1000003, 4, 40), (2, 2000003, 6, 200),
  (3, 1000033, 4, 60), (4, 1000037, 3, 30)}, m = ⌈log_κ p⌉ + λ, three keys each. The "solver" is
  the only one available at these arities: enumerate the one-parameter family (s, t₀ ∈ coset
  representatives) and test x ∈ P₀^M. Instances: a = 62, M = 104 (2a − M = 20); a = 225,
  M = 427 (23); a = 75, M = 137 (13); a = 41, M = 73 (9). Every returned x was verified
  (Λx = 0, x ∈ P₀^M, x ≠ 0) and θ was recovered in all 12 runs; two runs returned one extra
  key (consistent with the bound 2κ^{1−λ}). Runtime about 3 minutes.

`density_check.py` → `density_check.out`.
- [exact] a = 1: for κ ∈ {2, 3, 4, 6} and p ∈ {101, 103, 109}, every bank (1, c₂, c₃) of
  nonzero columns (all (p−1)p/2 up to scaling and order) has a nonzero P₀-solution; the number
  of dead pairs (1, c) equals (κ−1)(p−1)/κ exactly.
- [exact] a = 2, κ = 3, p ∈ {1009, 1033}: the bank of two dead pairs has 0 solutions at M = 4;
  60 random banks with M = 5 = 2a + 1 have between 4.22·10⁶ and 4.80·10⁶ solutions (the
  script's printed heuristic p³/27 is a slip; the right figure is |P₀|⁵/p² ≈ p³/243 ≈ 4.2·10⁶,
  which the counts match); the structured banks (two dead pairs plus a fifth column in each
  coset combination, a proportional triple, four proportional columns) all have ≥ 3.8·10⁶
  solutions. Consistent with the density remark of §2 (dead weight ≤ 2 per dimension at
  κ = 3), not a proof of it. Runtime about 6 minutes.

## 8. Weakest step, and what a referee should attack

1. The hardness is conditional on the power-residue PRF (H1) or on Assumption LP (H2). Both
   are cryptographic conjectures. A referee should ask whether a key-recovery attack from
   O(log p) random queries in time polylog(p) is excluded by the published cryptanalysis; the
   repository cites Beullens–Beyne–Udovenko–Vitto 2020 (cost ≈ p polylog p / M²) for "none
   known"; nothing was fetched in this pass. The reduction itself (Theorem H) is unconditional.
2. Step (v) assumes the c_i i.i.d. uniform; the paper's remark says "independent uniform" too.
   If the PRF model only allows distinct queries, draw i.i.d. and discard collisions (probability
   ≤ m²/p), which changes the bound by that amount.
3. The density remark for κ ≥ 3 (§2) is [argued]; Proposition L is proved only for κ = 2.
   Theorem H itself does not need it.
4. Corollary H1 needs a prime p ≡ 1 (mod κ) of size κ^{Θ(εa)}; the PRF is defined for every
   such prime, so this is only a statement about which primes the solver must handle.
5. Nothing here is an algorithm. The verdict "every near-linear algorithm must use totality"
   is a consequence of H1, not a lower bound for the total problem; the band
   [2a + 4 − log_κ p, κa + 1] is open in both directions.

## 9. Claim gates (must stay false), next question, next command

Gates:
- "The total problem at M ≥ κa + 1 (or 2a + 1) is hard": not shown; Proposition L says this
  technique cannot show it.
- "Theorem H is unconditional hardness": it is a reduction to a cryptographic conjecture.
- "Uniform in p": H1 needs log_κ p ≤ a + 2 − λ; H2 needs Assumption LP.
- "o(a²) algorithm found", "a²/log a optimal", any novelty or priority claim: none.
- "The paper's arity or any table changed": no; one sentence of rem:sde-worst-case(b) could be
  strengthened (§5), owner decision.

Next hard question. Is SDE(a, 2a + 1) for κ = 2 at p ≥ poly(a) hard under any assumption, or
in any class? It is in a growing-p analogue of PPA_p (the CW proof is a mod-p count); the
natural targets are (i) a reduction from a total problem believed hard (pigeonhole SIS^∞ at
m = n log q, PPP-type, §6(b)(ii)) and (ii) the converse: an algorithm that uses the mod-p count
constructively. The band [2a + 4 − log₂ p, 2a + 1] is O(log a) wide at p = poly(a), so the
first question to settle is whether the promise problem is already hard at 2a + 1 − O(1) for
banks that are solvable but not forced to be; Lemma CW₂ says no reduction with dead weight can
show it, so a hard block of density > 1 is needed.

Next command. `cd research/audits/reviews/2026-11-08-rees-sde-near-linear &&
/opt/anaconda3/bin/python -B reduction_check.py` reproduces both tables (about 3 minutes);
acceptance: every `exh` line has `with_t_nonzero_or_t0_zero=0` and one shift class per key,
and every `bf` line has `ok=True`.

## 10. Files

- `2026-11-08-rees-sde-near-linear/reduction_check.py`, `reduction_check.out`: construction R,
  exact kernel enumeration, brute-force extraction.
- `2026-11-08-rees-sde-near-linear/density_check.py`, `density_check.out`: dead-weight density
  at a = 1 (exhaustive) and a = 2 (exact counts).
