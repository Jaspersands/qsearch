# Rees SDE solver below Schedule 2, and the linear-arity question

2 November 2026. Item 5 of `research/REES_FULL_CAMPAIGN_2.md`. AI-only pass: one
session plus one literature helper. This is not human review, a Lean proof or a
priority claim. AI-checked, pending human review. Labels: **[proved]** (written
proof here or a cited theorem), **[exact]** (complete finite computation, script
named), **[float]** (heuristic computation), **[argued]**. Scripts, outputs and
fetched texts are in `2026-11-02-rees-linear-arity/`; the interpreter is
`/opt/anaconda3/bin/python`. Only this file and that folder were written.

Problem (from `2026-11-02-rees-small-prime-arity.md` §0, §6, §9). The columns
λ_1..λ_M ∈ F_p^a are arbitrary, κ = gcd(d, p−1) ≥ 2, H = (F_p^*)^κ and
P = H ∪ {0}. Find x ∈ P^M with x ≠ 0 and Σ x_i λ_i = 0. Then s_i = x_i^{1/κ}
and a Bezout exponent give Σ s_i^d λ_i = 0. Q_m = g^m H and A_m = Q_m ∪ {0}.
E_2(κ) is the set of primes with no universal two-level contraction, as in the
paper's Proposition `prop:decoupled-sde`.

## 0. Answers

1. **The target is not reached [argued + literature].** No polynomial-time
   algorithm was found at arity o(a²) for any fixed κ ≥ 2, and none at O(a)
   for any fixed p. The literature agrees: Kothari–Metger–O'Donnell–Shutty–Wu
   (arXiv:2609.40321, Sep 2026) say that at m = Θ(n) every known attack on
   F_q^n-subset-sum is still exponential, even on average. Proposition C below
   shows that no scheme in the collision-tensor family used here can go below
   quadratic.
2. **Schedule 2 shrinks by a factor of about 2(κ−1) at every κ [proved + exact].**
   For every p ∉ E_2(κ), with the paper's decoupled contraction (α, β), a
   deterministic solver finds a witness from M^tri(a) = (a+1)(a+2)/2 arbitrary
   columns (Theorem A). This replaces (a+1)((κ−1)a+1). A non-triangular
   variant uses (a+1)². With sparse dependencies (the Kothari–O'Donnell–Wu
   lemma) it uses (1−1/p)a²/2 + O(a log a). The key fact is that the
   second-level dependency needs a linear conditions, not (κ−1)a.
   - **Not new at κ = 2.** This is Ivanyos–Sanselme–Santha Claim 1 (diagonal
     quadratic forms). At p = 3 it is their F_3 subset-sum bound, and the
     sparse variant at p = 3 is KOW Theorem 1.2.
   - **κ ≥ 3** is, as far as this pass found, not stated in the literature. It
     is a short combination of ISS's dimension reduction with the repo's coset
     contraction. **No priority claim.**
   - **Class-9 profile:** 63.6 → 43.6 bits of lifted sources per terminal
     sample, wherever p ∉ E_2(κ_d) for every grade.
3. **The L-level fallback has a reduced form [proved + exact].** With any
   universal L-level contraction, level t needs only r_t·a + 1 lower objects,
   where r_t = rank of a canonical flattening and r_t ≤ min((κ−1)^{t−1}, κ^{L−t}).
   The first and last levels have r = 1 (Theorem B).
   - **Worst-case all-prime fallback (L = L_CW):** the class-9 profile drops
     from 1392 to 739 bits.
   - **Exact ranks at the exceptional primes:** r = [1,3,1] at (13,4), (17,4)
     and (29,4); [1,2,1] at (11,5); [1,3,4,1] at (5,4) with L = 4.
   - **BIS_5:** the triangular count is Σ_{q≤m}(q+1)(3q+1)(4q+1) + 1 ≈ 3m⁴,
     against KMOSW Theorem 1.11's 5^{25}(m+1)⁴. Same exponent, smaller constant.
4. **There is a barrier for this method class [proved].** Every universal
   contraction has at least two levels with r_t ≥ 1 (Proposition C). So every
   product scheme in this family needs (a+1)² columns, and every triangular one
   needs about a²/2 (or (1−1/p)a²/2 with sparse dependencies) [argued for the
   triangular count]. Going below quadratic needs a different idea.
5. **Hardness evidence, only when κ grows [proved, conditional].** Take
   h = (p−1)/κ ∈ {1, 2}, so P ⊆ {0, ±1}, and p ≥ ω(a² log a) polynomial in a.
   Then witness finding on uniformly random columns at the Chevalley–Warning
   arity κa + 1 is as hard as worst-case SIVP_{Õ(a√p)}, by GPV Proposition 5.7
   (Proposition D).
   - So no algorithm can be uniform in κ at near-linear arity unless standard
     lattice assumptions fail.
   - This says nothing about fixed κ or fixed p. There no hardness is known,
     and no reduction from a known-hard problem was found.
6. **Göös et al. Open Problem 6 [literature, full texts read].** At κ = p−1
   our problem is exactly BIS_p (Definition 6.1), with m = a equations and
   n = M columns.
   - OP 6 asks only whether BIS_q has a non-trivial polynomial-time regime.
     That is already answered positively for prime q: ISS (q = 3), Imran–Ivanyos
     2024 Theorem 2, KOW 2026 Theorem 1.2, KMOSW 2026 Theorem 1.11, and the
     repo's L-level Theorem 4.
   - The linear regime n = O(m) (n ≥ (m+1)(p−1) is their threshold) is open
     for every prime p ≥ 3. "Linear arity at fixed small p" is that open
     problem when κ = p−1. For κ < p−1 it is a weighted version, and for
     h = 2 it is SIS_p (Definition 6.2).
7. **Small p [proved].** For p ≤ f(κ), brute force over the witness costs
   (h+1)^M, which is exponential in a; this is unchanged from round 1.
   Theorems A and B make every fixed p polynomial at quadratic (p ∉ E_2) or
   O(a^{L*}) arity. Nothing found makes small p linear.
8. **Lattice reduction, random columns only [float].** BKZ-20 finds {0,±1}
   witnesses on random columns at the Chevalley–Warning arity for p = 5
   (a ≤ 40), p = 7 (a ≤ 30, 14/15 runs) and p = 13 (a ≤ 20). At p = 13,
   a = 30 it found none (0/5). This is average-case heuristics in small
   dimension. It gives no worst-case statement, and it does not apply when κ
   is fixed and p is large (P has no geometry there).

## 1. Unnormalised coordinates

Write each dependency coefficient as an element of F_p^* with coset label
m = coset(γ) ∈ Z_κ (γ ∈ Q_m). A level-t object is a list of entries
(column, coef, m ∈ Z_κ^t). Here coef is the product of the coefficients on the
path to the column, and m lists their cosets. Its cells are T_m = Σ coef·λ over
the entries labelled m. The paper's normalised contraction C relates to the
function used here by F(m) = C_m / Π_t z_{m_t}. The conditions translate as
follows:

- C_m ∈ P becomes F(m) ∈ A_{−|m|}, with |m| = Σ_t m_t. Then coef·F(m) ∈ P,
  since coef ∈ Q_{|m|}.
- C annihilates W^{⊗L} exactly when Π_t (1 − π_t) F = 0, where π_t averages
  over axis t (κ is invertible mod p). Multiplying by Π z sends W^{⊗L} to
  (ker 1^T)^{⊗L}. The annihilator of the latter is the sum of the kernels of
  the commuting projectors 1 − π_t.
- At L = 2 the decoupled form becomes F(m_1, m_2) = α_{m_2} + β_{m_1}, with the
  condition α_j + β_i ∈ A_{−(i+j)} of the paper.

## 2. Theorem A: triangular two-level solver

**Lemma 1 (flexible vector) [proved].** Let U ≤ F_p^a. Let d ∈ F_p^S, d ≠ 0, on
a column set S satisfy e := Σ_{i∈S} d_i λ_i ∈ U. Put
v := Σ_{i∈S} β_{coset(d_i)} d_i λ_i. Take c ∈ F_p^* with coset n, and the
weights x_i = c d_i (α_n + β_{coset(d_i)}) (and 0 where d_i = 0). Then
x_i ∈ P and Σ x_i λ_i = c α_n e + c v ∈ c v + U.
*Proof.* c d_i ∈ Q_{n+m} with m = coset(d_i), and α_n + β_m ∈ A_{−(n+m)}, so
x_i ∈ P. The sum is c α_n Σ d_i λ_i + c Σ β_{m(i)} d_i λ_i. ∎

**Algorithm.** Normalise every d so that its first nonzero entry is 1. Start
with U_0 = 0. In round k (k = 0, 1, …), let q = a − dim U_k:

- Take the next q + 1 unused columns. Their images in F_p^a/U_k are dependent,
  so solve for d ≠ 0 with e ∈ U_k, and form v.
- If v ∈ U_k (this always holds when q = 0, and then the "dependency" is one
  column with d = 1), stop. Set R := the weights of Lemma 1 with c = 1
  (n = 0); R lies in U_k.
- Otherwise put U_{k+1} = U_k ⊕ F_p v_{k+1} and continue.

**Back-substitution.** Set τ = −ΣR. For l = k, …, 1, let c_l be the
v_l-coordinate of τ ∈ U_l = U_{l−1} ⊕ F_p v_l. If c_l ≠ 0, add object l's
Lemma-1 weights for c_l and replace τ by τ − c_l(α_n e_l + v_l) ∈ U_{l−1}.

**Theorem A [proved].** Let κ ≥ 2 and p ∉ E_2(κ), with (α, β) a universal
two-level contraction (α_0 = 1, β_0 = 0). For every λ_1..λ_M ∈ F_p^a with
M ≥ (a+1)(a+2)/2, the algorithm returns a nonzero x ∈ P^M with Σ x_i λ_i = 0.
It makes at most a + 1 Gaussian eliminations of size ≤ a × (2a+1), plus O(a²)
coset evaluations x ↦ x^{(p−1)/κ}. It is deterministic given (α, β), and runs
in time poly(a, log p).

*Proof.*
- **Column count.** Round k uses a − k + 1 columns and the last round uses 1, so
  at most Σ_{k=0}^{a}(a − k + 1) = (a+1)(a+2)/2 columns are used.
- **Supports.** Object supports are disjoint, so the weights simply add.
- **Back-substitution.** τ ∈ U_l, and τ − c_l v_l ∈ U_{l−1} by the choice of
  c_l. Also c_l α_n e_l ∈ U_{l−1}, since object l was built modulo U_{l−1}.
  At the end τ ∈ U_0 = 0, so the total sum is −τ = 0.
- **Nonzero.** The normalised d of the last object has an entry 1 ∈ Q_0. Its
  weight is 1·(α_0 + β_0) = 1. ∎

**Variants [proved].**
- *Product.* Use a + 1 objects of a + 1 columns each with U = 0, and one
  dependency c among v_1..v_{a+1}. That gives (a+1)². Equivalently: Schedule 2's
  second level needs Σ_j c_j v_j = 0 (a conditions), not the full tensor
  relation ((κ−1)a conditions). The α term is killed by the first-level
  relation, as in the normal form C = z a^T + b z^T.
- *Sparse.* In a q-dim quotient, take q + r columns with p^r ≥ q + 1. Use a
  minimum-weight dependency from the r-dim space; brute force over p^r ≤ p(q+1)
  combinations, or derandomise as in KOW Lemma 3.6. Unused columns go back to
  the pool. The recursion
  m_l = max(l + r_l, m_{l−1} + ⌊(1−1/p)l/(1−p^{−r_l})⌋ + r_l)
  gives (1−1/p)a²/2 + O(a log_p a). This is the KOW Theorem 3.7 shape. It helps
  only at small p, and the time is poly(a, p).

**Priority.** This was checked against the full text of
Kothari–O'Donnell–Wu (arXiv:2510.07515v3, §§2–3 and §5.2):
- **κ = 2:** Theorem A is Ivanyos–Sanselme–Santha Claim 1 (diagonal
  quadratic equations, worst case, (n+1)(n+2)/2; paper's
  `IvanyosSanselmeSantha2012`), as KOW §5.2 describes it.
- **p = 3:** it is KOW Theorem 2.2, and the sparse variant is KOW Theorem 1.2.
- **κ = (p−1)/2, p ∈ {5, 7}** (P = {0,±1}): the sparse variant matches KOW
  Theorem 3.7.
- **κ ≥ 3 in general:** KOW's reducible-vector lemma (Lemma 3.3) is about
  intervals {−s..s} and does not cover P = κ-th powers. Ivanyos–Santha 2017
  is at arity ≈ d^{d log d}·n^{d log d}.
- **Repo:** the Schedule 2 count (a+1)((κ−1)a+1) comes from the repo's own
  note.

**Exact checks [exact; `reduced_sde.py two|sparse`, outputs `sweep_two_level.out`].**
Every run checks x_i ∈ P (x_i^{(p−1)/κ} = 1), x ≠ 0 and Σ x_i λ_i = 0 mod p.
For p < 5000 it also checks the converted SDE witness s^κ = x. Families:
random, repeated basis vectors, scaled basis pairs, rank-one, sparse.

| p | κ | a | triangular arity / used | product | Schedule 2 | witnesses |
|---|---|---|---|---|---|---|
| 3 | 2 | 6 | 28 / ≤ 27 | 49 | 49 | 30/30 + 30/30 |
| 5, 7 | 2 | 6 | 28 | 49 | 49 | 60/60 each |
| 7 | 3 | 6 | 28 | 49 | 91 | 60/60 |
| 13 | 2, 3 | 5 | 21 | 36 | 36, 66 | 60/60 each |
| 41 | 4 | 5 | 21 | 36 | 96 | 60/60 |
| 191 | 5 | 4 | 15 | 25 | 85 | 40/40 |
| 1009 | 3, 4 | 8, 6 | 45, 28 | 81, 49 | 153, 133 | 40/40 each |
| 3001 | 5 | 4 | 15 | 25 | 85 | 30/30 |
| 2^61−1 | 2, 3 | 8 | 45 | 81 | 81, 153 | 15/15 each |
| 2^61−1 | 5 | 6 | 28 | 49 | 175 | 10/10 |

The sparse variant (`reduced_sde.py sparse`) used at most
- 56 columns at (3, 2, a = 12), within a budget of 80 (dense count 91);
- 51 at (5, 2, 10) and 55–56 at (7, 2 or 3, 10), all within a budget of 64
  (dense count 66).

Every run passed. Exceptional primes are detected (5, 13 for κ = 4; 11, 31 for
κ = 5; 7, 13, 61 for κ = 6; 53 for κ = 4). The test file `test_reduced_sde.py`
passes (4 tests). The κ = 7 runs at 2^61−1 were stopped while still sampling α with
Python `pow` (the per-j search needs about 7^7 trials). They are not counted, and
`run_sweeps.sh` still lists them.

## 3. Theorem B: reduced L-level schemes (exceptional primes)

Let F : Z_κ^L → F_p with F(m) ∈ A_{−|m|}, F(0) ≠ 0 and Π_t(1−π_t)F = 0. By
round-1 Theorem 4, such an F exists at every prime once κ^L > κ(κ−1)^L.

- Define H_t := π_t Π_{s<t}(1 − π_s) F. Telescoping gives F = Σ_{t=1}^{L} H_t,
  and H_t does not depend on m_t.
- Let r_t be the rank of the matrix (H_t(m_{<t}, ·, m_{>t})), with rows
  m_{<t} and columns m_{>t}. Its rows are killed by every π_s with s < t, so
  r_t ≤ min((κ−1)^{t−1}, κ^{L−t}); in particular r_1, r_L ≤ 1.
- Choose r_t independent columns φ_{t,1..r_t} of that matrix.

**Scheme.**
- A level-0 object is one column.
- A level-t object takes r_t q + 1 level-(t−1) objects k, where q =
  dim F_p^a/U. It solves for γ ≠ 0 with Σ_k γ_k φ_{t,j}(T^k) ∈ U for every j,
  where φ(T) := Σ_{m_{<t}} φ(m_{<t}) T_{m_{<t}}. It normalises the first
  nonzero γ to 1 and appends coset labels.
- The final weight is x = coef·F(m).

**Theorem B [proved].** In the product form (U = 0) the scheme returns a
witness from Π_{t=1}^{L}(r_t a + 1) columns. In the triangular form the top
level is replaced by the back-substitution of Theorem A, using the flexible
vectors v_K = Σ_{m_{<L}} H_L(m_{<L}) T^K_{m_{<L}}. That form needs
1 + Σ_{q=1}^{a} Π_{t<L}(r_t q + 1) columns.

*Proof.*
- **Splitting the sum.** Σ_m F(m) T_m = Σ_t Σ_m H_t(m) T_m. In the t-th term,
  group the top cells by the level-t objects K beneath them:
  Σ_m H_t(m) T_m = Σ_{m_{>t}} Σ_K coef_{>t}(K, m_{>t})·Σ_{m_{<t}} H_t(m_{<t}, m_{>t}) R^K_{m_{<t}},
  where R^K_{m_{<t}} = Σ_{m_t} T^K_{(m_{<t}, m_t)} = Σ_k γ_k T^k_{m_{<t}}.
- **Each term vanishes.** Each H_t(·, m_{>t}) lies in the span of the chosen
  φ_{t,j}, so the inner sum is in U. In the product form it is 0.
- **Triangular form.** The realisation with top coefficient c, coset n, is
  c Σ_{m_{<L}} F(m_{<L}, n) T^K = c v_K + (element of U). Then Theorem A's
  back-substitution applies verbatim.
- **Nonzero.** The all-first-children path has coefficient 1 and label 0, so
  its weight is F(0) ≠ 0. ∎

At L = 2 the ranks are r = (1, 1), which recovers Theorem A. The round-1
scheme corresponds to imposing full relations, i.e. r_t = (κ−1)^{t−1}.

**Exact ranks and witnesses [exact; `reduced_sde.py ranks|llev`, `sweep_llevel.out`; contractions from round-1 `llevel.py sat`, re-verified].**

| (p, κ, L) | r | a | triangular / product / round-1 arity | witnesses |
|---|---|---|---|---|
| (13,4,3), (17,4,3), (29,4,3) | [1,3,1] | 2 | 30 / 63 / 399 | all pass (15+15, 15+15, 10+10) |
| (13,4,3) | [1,3,1] | 3 | 70 / 160 / 1120 | 5+5 |
| (11,5,3) | [1,2,1] | 1; 2 | 7 / 12 / 170; 22 / 45 / 891 | 15+15; 10+10 |
| (5,4,4) | [1,3,4,1] | 1; 2 | 41 / 80 / 2240; 230 / – / 21945 | 15+15; 5 |
| (41,5,3), (7,3,3) | [1,4,1], [1,2,1] | – | ranks only (`ranks`); (31,5,3) SAT timed out at 600 s | – |

**Class-9 profile [exact arithmetic; `profile_bits.py`, `profile_bits.out`].**
The grade dimensions are a_d = 17, 16, 14, 12, 9, 6, 3, 1 for d = 2..9, with
κ_d = d. Total bits:

| scheme | bits |
|---|---|
| Schedule 2 | 63.6 |
| (a+1)² | 50.0 |
| (a+1)(a+2)/2 | 43.6 |
| worst-case fallback at L_CW, round 1 | 1392.2 |
| worst-case fallback at L_CW, reduced product (rank upper bounds) | 754.6 |
| worst-case fallback at L_CW, reduced triangular (rank upper bounds) | 739.1 |

The worst-case exponent of a at L_CW is unchanged (it is still L_CW). Only
the constants change.

## 4. Proposition C: the barrier for universal-contraction schemes

**Proposition C [proved].** For κ ≥ 2, every universal contraction F has
r_t ≥ 1 for at least two levels t.
*Proof.* Suppose H_t = 0 for all t ≠ t_0. Then F = H_{t_0} does not depend on
m_{t_0}. But F(m) ∈ A_{−|m|} for all κ values of m_{t_0}, and
A_j ∩ A_{j'} = {0} for j ≠ j'. So F ≡ 0, contradicting F(0) ≠ 0. ∎

Consequences:
- **Product form [proved].** Two nested dependency stages, each over a-dim
  vectors, need at least (a+1)² columns on generic inputs.
- **Triangular form [argued].** Each new flexible direction in a q-dim
  quotient costs a dependency, i.e. q + 1 columns, or about (1 − 1/p)q with
  sparse dependencies. So the total is Θ(a²).
- **Scope.** Linear or o(a²) arity would need instance-adaptive (non-universal)
  contractions, or a non-linear-algebraic method. Counting does not forbid
  it: for large p a full "flexible quotient" of dimension q needs only about
  q(1 + log κ/log p) columns. The obstacle is computational: realising a
  given target is the inhomogeneous problem itself.

## 5. Göös et al. Open Problem 6, exactly

Source: arXiv:1912.04467v2 (CCC 2020), full text in `lit/gksz_1912.04467.txt`.

- **Definition 6.1, BIS_q.** The input is A ∈ Z_q^{m×n} and the condition is
  n ≥ (m+1)^{N(q)}(q−1); for a prime q this is n ≥ (m+1)(q−1). The output is
  x ∈ {0,1}^n with x ≠ 0 and Ax ≡ 0.
- **Definition 6.2, SIS_q.** The condition is n ≥ ((m+1)/2)^{N(q)}(q−1) and
  the output is x ∈ {−1,0,1}^n.
- **Theorem 10.** For prime p, BIS_p and SIS_p reduce to Chevalley_p.
  BIS_q and SIS_q are in FP^{PPA_q}. BIS_{2^k} and SIS_{2^k3^l} are in FP.
- **Open Problem 6:** "For all q, is there a non-trivial regime of parameters
  n, m where BIS_q is solvable in polynomial time?"

Exact connection:
- Our instance at κ = p−1 (P = {0,1}) **is** BIS_p, with m = a and n = M.
  Their threshold (m+1)(p−1) sits just above Olson's
  D(C_p^m) = m(p−1) + 1 = κa + 1.
- At h = 2 (κ = (p−1)/2) our instance is SIS_p, with threshold ((m+1)/2)(p−1)
  ≥ κa + 1.
- For 1 < h, κ < p−1, our problem is the A-CIS of KOW (Definition 1.10) with
  A = P, of size (p−1)/κ + 1, in the worst case. It is a weighted Davenport
  search.

For prime q, OP 6 as worded is answered positively in the literature:
- ISS Claim 1 for q = 3: n ≥ (m+1)(m+2)/2.
- Ivanyos–Santha 2017 with d = q−1.
- Imran–Ivanyos 2024, Theorem 2: q^{O(q log² q)}·m^{O(q log q)}.
- KOW 2026, Theorem 1.2: q = 3 at m²/3 + Cm log m.
- KMOSW 2026, Theorem 1.11: q^{q²}(m+1)^{q−1}.
- Round-1 Theorem 4 here, and Theorem B: BIS_5 at about 3m⁴.

The repo's "linear arity at fixed small p" is the stronger, still open question
of whether BIS_p (or SIS_p) is in FP at n = O(m). KMOSW §1.3: "none ... reaches
that range". Göös et al. Open Problems 4 and 5 (the average case of SIS_q, and
Chevalley_p ≤ BIS_p) are untouched by this pass for fixed q. For growing q see
Proposition D.

## 6. Proposition D: conditional hardness when κ grows

**Proposition D [proved, conditional on the cited theorem].** Let p be prime,
h = (p−1)/κ ∈ {1, 2}, and P ⊆ {0, ±1} viewed as integers. Suppose an algorithm
finds, with non-negligible probability over uniform random columns in F_p^a, a
witness from M ≤ poly(a) columns. Suppose also 2a⌈log₂ p⌉ ≤ M and
√M ≤ p/ω(√(a log a)). Then worst-case SIVP_γ on a-dimensional lattices, with
γ = √M·Õ(√a), has a probabilistic polynomial-time algorithm.
*Proof.* A witness is a nonzero integer vector with ‖x‖_2 ≤ √M and
Λx ≡ 0 mod p, i.e. a solution of average-case SIS_{p,M,β=√M}. Apply
Gentry–Peikert–Vaikuntanathan (STOC 2008, author copy of 25 Aug 2008),
Proposition 5.7: m = poly(n), β = poly(n), prime q ≥ β·ω(√(n log n)),
γ = β·Õ(√n), with n = a, m = M, q = p. ∎

At the Chevalley–Warning arity M = κa + 1 ≈ pa/h, the hypothesis holds once
p ≥ ω(a² log a). In words: finding SDE witnesses at the existence threshold,
uniformly in κ, is as hard as approximate SIVP in dimension a (factor Õ(a√p)).
This explains why every known efficient scheme has a κ-dependence that is
exponential in some form: T_W ≈ κ^{2κ}, E_2(κ), L_CW ≈ κ ln κ, IS's
a^{κ log κ}. It does not apply to fixed κ, to fixed p, or to worst-case
statements beyond the average case. The same parameters appear in KOW
footnote 7 (s = O(1), q = Θ(n² log n), m = Θ(n log n)).

## 7. Lattice probe (random columns only)

[float; `lattice_probe.py` under `/opt/anaconda3/envs/qsearch-cas/bin/python`,
output `lattice_probe.out`]. The probe uses the q-ary kernel lattice and
BKZ-20, then scans basis vectors and their pairwise sums and differences. Each
reported success was re-checked exactly mod p.

| p | h | κ | a | M | successes |
|---|---|---|---|---|---|
| 5 | 2 | 2 | 10, 20, 30, 40 | 2a+1 (CW) | 5/5 each |
| 5 | 2 | 2 | 10, 20, 30, 40 | 4a+1 | 5/5 each |
| 7 | 2 | 3 | 10, 20 | 3a+1 (CW) | 5/5 each |
| 7 | 2 | 3 | 30 | 3a+1 (CW) | 4/5 |
| 13 | 2 | 6 | 10, 20 | 6a+1 | 5/5 each |
| 13 | 2 | 6 | 30 | 6a+1 | 0/5 |
| 5 | 1 | 4 | 10, 20, 30 | 4a+1 | 2/5, 0/5, 5/5 |

Random instances at linear arity are easy at these sizes, consistent with
average-case results such as KMOSW Theorem 1.7. Nothing here bears on
worst-case inputs, or on fixed κ with large p.

## 8. Artifacts

| file | content |
|---|---|
| `reduced_sde.py` | Theorems A and B (product, triangular, sparse), contraction search, instance families, exact witness checks |
| `test_reduced_sde.py` | 4 pytest checks (passes) |
| `run_sweeps.sh` → `sweep_two_level.out`; `run_llevel.sh` → `sweep_llevel.out` | §2 and §3 tables |
| `profile_bits.py` → `profile_bits.out` | class-9 bit counts |
| `lattice_probe.py` → `lattice_probe.out` | §7 |
| `lit/` | full texts (GKSZ, IS, II24, KOW, KMOSW, GPV, MP13, DEL25) and the helper's `LITERATURE_SUMMARY.md` |

Reproduce:
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider test_reduced_sde.py`
and `./run_sweeps.sh` (about 20 min), `./run_llevel.sh` (about 30 min).

## 9. Status

**Exact statement that now holds.**

- *Theorem A [proved; AI-checked, pending human review].* For every κ ≥ 2 and
  every prime p ∉ E_2(κ) (in particular p > T_W(κ), all p for κ ≤ 3, and all
  but the listed primes for κ = 4, 5), any (a+1)(a+2)/2 columns in F_p^a admit
  a deterministic poly(a, log p) witness computation, given the precomputed
  (α, β).
- *Theorem B [proved].* With a universal L-level contraction, the arity is
  Π_t(r_t a + 1), or the triangular sum, with r_t ≤ min((κ−1)^{t−1}, κ^{L−t}).
- *Proposition C [proved].* Universal-contraction schemes are at least
  quadratic.
- *Proposition D [proved, conditional].* For h ≤ 2 and p ≥ ω(a² log a),
  witness finding at the CW arity is average-case SIS-hard.
- Linear or o(a²) efficient arity is **open**. It is open in the literature
  for every fixed p ≥ 3 at κ = p−1.

**Still missing.**
- Any o(a²) algorithm, or any hardness, for fixed κ or fixed p.
- Contractions minimising r_t (a rank-constrained SAT search was not run).
- A κ = 7 large-prime run (needs a faster α sampler, e.g. `scan2.c` from round 1).
- Literature not read in full: Ducas–Espitau–Postlethwaite (abstract only),
  and Bai–Galbraith–Li–Sheffield and Kirchner–Fouque (not fetched).

**Claim gates that must stay false.**
- "An efficient linear-arity (or o(a²)) SDE solver exists".
- "BIS_p/SIS_p or the diagonal SDE search is hard for fixed p or κ".
- "Schedule 2 is optimal".
- Any priority or novelty claim for Theorem A (κ = 2 is ISS; κ ≥ 3 is a
  short combination) or for Theorem B.
- "The L-level fallback is practical".
- Proposition D is about growing κ and random columns only. It must not be
  quoted as hardness for the paper's fixed-class regime.

**Next hard question.** Is there an instance-adaptive contraction, chosen after
seeing the cosets of the first-level dependencies, that gives flexibility in
two or more directions per object? With κ − 1 directions per object the
triangular count would fall by a factor of κ − 1. The universal version is
impossible **[proved]**. With two directions T_1, T_2 from one object, a target
(0, t_2) forces the pivot weight w_0 to satisfy w_0 z_1 ∈ P, hence w_0 = 0.
Then t_2 ∈ P is required, which fails for t_2 ∉ P. Next command:
`python reduced_sde.py ranks p k L` with a rank-constrained SAT variant (to be
written). Expected artifact: contractions at (13,4,3) with r_2 < 3.
Acceptance test: exact witnesses at the reduced arity.

## Proposed paper text

**Target 1.** Insert after Proposition `prop:decoupled-sde` (Section `sec:sde`).
Status: proved, AI-checked, pending human review.

```latex
\begin{proposition}[Triangular two-level solver; AI-checked only]
\label{prop:triangular-sde}
Let $\kappa=\kappa_d\ge 2$, $p\notin E_2(\kappa)$, and let $(\alpha,\beta)$ be a
universal two-level contraction as in Proposition~\ref{prop:decoupled-sde},
normalised by $\alpha_0=1$, $\beta_0=0$, so that $\alpha_j+\beta_i\in
g^{-(i+j)}H\cup\{0\}$ for all $i,j\in\mathbb{Z}_\kappa$, where $H=(\Fp^\times)^\kappa$.
Then from any
\[
  M_d^{\mathrm{tri}}=\tfrac{(a+1)(a+2)}{2}
\]
columns $\lambda_1,\dots,\lambda_M\in\Fp^{a}$ a deterministic algorithm with
$O(a)$ Gaussian eliminations and $O(a^2)$ evaluations of $y\mapsto
y^{(p-1)/\kappa}$ returns a nonzero solution of~\eqref{eq:sde-target}.
\end{proposition}

\begin{proof}
Write $\mathrm{cos}(y)=m$ when $y\in g^mH$. For a column set $S$, a vector
$\delta\in\Fp^S\setminus\{0\}$ and a subspace $U\le\Fp^a$ with
$e=\sum_{i\in S}\delta_i\lambda_i\in U$, put
$v=\sum_{i\in S}\beta_{\mathrm{cos}(\delta_i)}\delta_i\lambda_i$. For
$c\in\Fp^\times$ with $\mathrm{cos}(c)=n$, the weights
$x_i=c\,\delta_i(\alpha_n+\beta_{\mathrm{cos}(\delta_i)})$ lie in $H\cup\{0\}$,
because $c\delta_i\in g^{n+\mathrm{cos}(\delta_i)}H$; and
$\sum_i x_i\lambda_i=c\alpha_n e+cv\in cv+U$.

Start with $U_0=0$. In round $k$ take the next $a-\dim U_k+1$ unused columns,
choose $\delta\ne 0$ with $e_{k+1}=\sum\delta_i\lambda_i\in U_k$, scale it so that
its first nonzero entry is $1$, and form $v_{k+1}$. If $v_{k+1}\in U_k$ (always
the case once $U_k=\Fp^a$, when one column is taken with $\delta=1$), stop and
let $R$ be the realisation with $c=1$; it lies in $U_k$ and has the weight
$\alpha_0+\beta_0=1$ on one column. Otherwise set
$U_{k+1}=U_k\oplus\Fp v_{k+1}$. At most
$\sum_{k=0}^{a}(a-k+1)=(a+1)(a+2)/2$ columns are used.

Put $\tau=-R$. For $l=k,\dots,1$ let $c_l$ be the $v_l$-coordinate of
$\tau\in U_{l-1}\oplus\Fp v_l$; if $c_l\neq0$, add the weights of round $l$
for $c=c_l$ and replace $\tau$ by $\tau-c_l(\alpha_{\mathrm{cos}(c_l)}e_l+v_l)$,
which lies in $U_{l-1}$. Finally $\tau\in U_0=0$. The supports are disjoint,
so the weights sum to a nonzero solution of $\sum x_i\lambda_i=0$ with
$x_i\in H\cup\{0\}$. Taking $\kappa$-th roots and a Bezout exponent gives a
solution of~\eqref{eq:sde-target}.
\end{proof}

\begin{remark}[Scope and priority]
\label{rem:triangular-scope}
For $\kappa=2$ Proposition~\ref{prop:triangular-sde} is the dimension-reduction
bound of~\cite[Claim~1]{IvanyosSanselmeSantha2012} for diagonal quadratic
equations; at $p=3$ it is the $\mathbb{F}_3$ subset-sum bound recorded
in~\cite[Theorem~2.2]{KothariODonnellWu2026}. Using sparse dependencies
\cite[Lemma~3.6]{KothariODonnellWu2026} lowers the count to
$(1-1/p)a^2/2+O(a\log a)$. The same argument applied to Schedule~2 shows
that its second level needs only $a+1$ objects, giving $(a+1)^2$ columns in
place of $(a+1)((\kappa-1)a+1)$. Below $(a+1)^2$ and $(a+1)(a+2)/2$, no
scheme built from a universal contraction can go: every such contraction has
at least two levels with a nontrivial relation. No polynomial-time method at
arity $o(a^2)$ is known for any fixed $\kappa\ge2$; at $\kappa=p-1$ the
problem is the problem $\mathrm{BIS}_p$ of~\cite[Definition~6.1]{GoosKamathSotirakiZampetakis2020},
for which every known polynomial-time algorithm needs a number of columns
at least quadratic in $a$~\cite{KothariODonnellWu2026,KothariMetgerODonnellShuttyWu2026}.
\end{remark}
```

**Target 2.** In Remark `rem:combined-schedule`, replace
"if $\kappa_d \ge 2$ and $p \ge 16\,\kappa_d^{2\kappa_d+2}$, use Schedule~2 with
$M_d = (g_d+1)\bigl((\kappa_d-1)g_d+1\bigr)$" by the following. This is
conditional on the owner adopting Proposition `prop:decoupled-sde`'s hypothesis,
which is the owner's call:

```latex
if $\kappa_d\ge 2$ and $p\notin E_2(\kappa_d)$, use
Proposition~\ref{prop:triangular-sde} with $M_d=(g_d+1)(g_d+2)/2$
```

Status: conditional, AI-checked only. If the owner keeps the guard
$p \ge 16\kappa^{2\kappa+2}$, use the same arity under that guard; it is
implied, since that guard gives p ∉ E_2(κ).

**Target 3.** Bibliography entries for the integrator (`references.bib`):

```bibtex
@inproceedings{GoosKamathSotirakiZampetakis2020,
  author    = {G{\"o}{\"o}s, Mika and Kamath, Pritish and Sotiraki, Katerina and Zampetakis, Manolis},
  title     = {On the Complexity of Modulo-$q$ Arguments and the {Chevalley}--{Warning} Theorem},
  booktitle = {35th Computational Complexity Conference (CCC 2020)},
  series    = {LIPIcs}, volume = {169}, pages = {19:1--19:42}, year = {2020},
  note      = {arXiv:1912.04467}
}
@inproceedings{KothariODonnellWu2026,
  author    = {Kothari, Robin and O'Donnell, Ryan and Wu, Kewen},
  title     = {No Exponential Quantum Speedup for {SIS}$_\infty$ Anymore},
  booktitle = {Proceedings of STOC 2026}, year = {2026},
  note      = {arXiv:2510.07515}
}
@misc{KothariMetgerODonnellShuttyWu2026,
  author = {Kothari, Robin and Metger, Tony and O'Donnell, Ryan and Shutty, Noah and Wu, Kewen},
  title  = {Exponential Quantum Speedup for $\mathbb{F}_3^n$-Subset-Sum? {O}r, Rigorous Classical Algorithms for Binary-Error {LWE}},
  year   = {2026}, note = {arXiv:2609.40321}
}
```

(The LIPIcs volume and pages for GKSZ, and the STOC proceedings data for KOW,
were not checked against the publisher. The integrator should verify them or
cite only the arXiv numbers.)
