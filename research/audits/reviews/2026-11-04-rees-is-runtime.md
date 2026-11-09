# Rees Schedule 1: an explicit running-time bound for the Ivanyos–Santha solver

4 November 2026. AI-only pass (one session). No human review. Labels: **[proved]** (written
argument here), **[source]** (stated in a cited paper, not re-proved here), **[argued]**
(standard but not written out in full), **[exact]** (complete finite computation).

Target: `docs/papers/rees-hsp/main.tex`, Theorem `thm:is-import`, Remark `rem:is-import`(b) and
Proposition `prop:coherent-receiver`. That proposition takes as given a multitape-TM time bound
T^IS_d for the Schedule 1 solve and says no explicit polynomial is known. This note gives one.
No `.tex`, `.bib` or code was edited. Nothing was committed. No network was used.

## 0. Answer

Notation: κ = κ_d = gcd(d, p−1), a = g_d (the column dimension; the rank is enough), b = ⌈log₂ p⌉,
G = G(κ, a) = κ^{κ(κ−1)/2}(a+1)^κ, ℓ ≤ κ+1 the number of terms of the computed zero sum of κ-th
powers, L = ⌈log₂ ℓ⌉, and N = G^L ≤ B_κ(a) ≤ B_d(a) = M_d (the columns the run consumes). Let
n_π be the largest divisor of p−1 whose prime factors all divide κ. Put ν = Ω(n_π) ≤ b−1 (the
number of prime factors of n_π, with multiplicity) and ω = the number of distinct primes dividing κ.

1. **Field-operation count [proved].** For κ ≥ 2 the solver (IS §§3.1–3.3), its zero-sum step
   and the Bezout step use at most

   F ≤ 40 κ³ · N · b · (a² + b²)  (+ a g M + a for the optional row reduction)

   field multiplications and inversions. Exponentiation is charged at 2·bitlen(exponent)
   multiplications. The solver also uses at most twice as many additions. For κ = 1 the count is
   F ≤ a²(a+1) + 2a + 2b(a+1) (+ agM + a). The explicit form behind this, term by term, is in
   §3 (equation (F)). The constant 40 is a crude estimate. The worst ratio on a grid of
   p ≤ 2¹²⁷, κ ≤ 8 and a ≤ 1000 is 5.74.
2. **Bit operations and multitape TM steps.** With schoolbook arithmetic, every counted
   operation costs O(b²) bit operations. A multitape TM runs the algorithm with constant-factor
   overhead **[argued, §5]**. Hence

   **T^IS_d ≤ C₁ · d³ · M_d · b³ · (g_d² + b²)**

   multitape TM steps on every list of M_d columns. C₁ is an absolute constant fixed by the
   machine. For fixed d this is O(M_d · b³ · (g_d² + b²)). The refined form is
   O_d(M_d · b² · [(ν+1)(g_d² + (ν+1)b) + b]). So when ν = O(1) (for example d = 2 and
   p ≡ 3 mod 4) it is O_d(M_d b²(g_d² + b)).
3. **Why b³(a² + b²) and not a²b².** The extra factors come from two places. The §3.1 restarts
   give up to ν+1 ≤ b whole runs. Each classification is a Pohlig–Hellman logarithm costing
   O((ν+ω)b) multiplications. In the worst case (n_π ≈ p, for example p = 2^k + 1 with d even)
   that is b⁵ per column. A linear-algebra-only count of O(M a² b²) bit operations would be
   wrong by these factors.
4. **The van de Woestijne step.** It does not depend on M or a, and for fixed κ it is
   O(κ³ log κ · b² + κ² log κ · b³) field operations **[proved for the implemented variant, §4]**.
   For odd κ it costs nothing (1^κ + (−1)^κ = 0). The source states Õ(κ² log p) field operations
   for its own algorithm (ISSAC 2005, Theorem 6.2). That bound is soft-O, and its proof is
   deferred to the thesis, which was not obtained **[source]**.
5. **Cross-check [exact].** I instrumented `theorems/rees_is_sde_solver.py` (unchanged) at
   d ≤ 3, a ≤ 2 on 20 instances in two exit modes, plus restart-stress runs. The predicted
   Theorem 11 calls, kernel calls per level and kernel shapes match exactly. Every measured
   count stays within its bound: Gaussian-elimination multiplications, classifications,
   restarts (≤ ν), total field operations and additions. Zero-sum rounds and cost were checked
   on 1373 pairs (p, κ). See §7.

## 1. Sources read

- IS arXiv:1503.09016v2 (`research/audits/reviews/2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`):
  Fact 2 and Theorem 3 (p. 2–3), §3 opening (gcd reduction), §3.1, Theorem 11, Lemma 12, the
  proof of (13), and §3.3. IS state every step as "time polynomial in B and log q". They give
  **no exponents**, so every count below is derived here from their description.
- van de Woestijne, ISSAC 2005. This is a local copy, SHA-1 `fec5a126…`, already fetched by an
  earlier session (another session's scratchpad, `…/92262358-…/scratchpad/is/issac2005.pdf`).
  It was converted with pdftotext into this session's scratchpad. I read §2 (soft-O convention),
  Theorem 5.1, §5.1–5.2, Theorems 6.1–6.2, §6.1, §6.2 and Theorem 7.1. The thesis was not
  available.
- `theorems/rees_is_sde_solver.py` and its report `2026-11-02-rees-is-solver.md` (recursion
  structure and the substitute Selective Root Extraction, proved correct there in §3).

## 2. The recursion, precisely

Input: p, d, columns λ_1..λ_M ∈ F_p^a with M ≥ N.

- **Step 0 (setup).**
  - Compute κ and t ≥ 1 with t·d/κ ≡ 1 mod (p−1)/κ (extended Euclid).
  - Compute n_π and the idempotent exponents of F_p^* = H_π × H_π′. This takes O(ω + ν)
    integer divisions and inversions of b-bit integers.
  - If κ = 1: one kernel vector of a+1 columns (an a × (a+1) elimination), then s_i = u_i^t.
    Done.
- **Step 1 (zero sum, once).** Compute z ∈ (F_p^*)^ℓ with Σ z_j^κ = 0 and 2 ≤ ℓ ≤ κ+1. This is
  van de Woestijne §6.1 applied to −1 = (p−1)·1^κ, with the terms stored as runs. Set
  L = ⌈log₂ ℓ⌉ and N = G^L. (§4.)
- **Step 2 (one run, classifier generator η).** This is §3.3 with L accumulation levels.
  - Level j = 1..L: G^{L−j} independent Theorem 11 calls. Each takes G consecutive vectors in
    F_p^a: the original columns at j = 1, the common vectors of level j−1 otherwise. So there
    are Σ_{j<L} G^j calls and I = G(G^L−1)/(G−1) ≤ (8/7)N input vectors in all.
  - **One Theorem 11 call is Lemma 12 at depth κ.** Write B_ℓ = κ^{ℓ(ℓ−1)/2}(a+1)^ℓ, so B_κ = G.
    A level-ℓ node (ℓ = 1..κ) has E_ℓ = κ^{ℓ−1}(a+1) children: input vectors at ℓ = 1,
    level-(ℓ−1) nodes otherwise.
  - Each node computes one kernel vector of an R_ℓ × E_ℓ matrix, with R_ℓ = κ^{ℓ−1}a (the
    concatenated w-vectors, κ^{ℓ−1} keys × a coordinates).
  - It classifies the at most E_ℓ nonzero kernel coefficients α = ζ_r γ^κ (§3.1), shifting them
    so that the target class is nonempty.
  - It forms the κ^ℓ new vectors w_{a′} = Σ_{k∈M_r} γ(k)^κ w_a(k) and the new coefficients
    β′ = γ(k)β.
  - A Theorem 11 call has G/B_ℓ nodes at level ℓ. Then the sign step sums ±w_a over a ∈ S_κ
    (κ!·a additions) and splits the supports into I and J.
  - §3.3 multiplies each original index's coefficient by its group's γ at every level. It exits
    early when a common vector is 0, which only shortens the run.
- **Step 3 (restarts, IS §3.1).** A classification whose π-part is not in ⟨η⟩ replaces η by a
  generator of ⟨η, γ⟩ and restarts Step 2. ⟨η⟩ strictly grows inside the cyclic group H_π of
  order n_π, so there are at most ν restarts and at most ν+1 runs **[proved]**.
- **Step 4 (finish).** Multiply the coefficients of the j-th representation by z_j: at most N
  multiplications. Then s_i = u_i^t for the at most N nonzero u_i (no work when κ = d), and
  s_i = 0 on unused columns.

## 3. Counting [proved]

**Cost model.**
- One modular multiplication or inversion costs at most c·b² bit operations (schoolbook, and
  extended Euclid), and an addition costs c·b.
- pow(x, e) is charged 2·bitlen(e) multiplications (square and multiply), plus one inversion
  when e < 0.
- Exponents are below p, so pow costs at most 2b multiplications.

**Gaussian elimination.** Gauss–Jordan on R × E (as in `_kernel_vector`) uses at most R²E + R
operations: per pivot one inversion, E normalizing multiplications and at most (R−1)E
eliminations.

**Per input vector of one Theorem 11 call.** Divide each level's cost by B_ℓ and sum over
ℓ = 1..κ:

- Λ(κ,a) = Σ_ℓ (R_ℓ²E_ℓ + R_ℓ)/B_ℓ ≤ a² + κ²a + 2κ³ + 2. The ℓ = 1 term is ≤ a² + 1. The ℓ = 2
  term is ≤ κ²a. For ℓ ≥ 3 the term is ≤ κ^{(ℓ−1)(6−ℓ)/2}·2^{3−ℓ}, which sums to ≤ 2κ³.
- Φ(κ,a) = Σ_ℓ [E_ℓ(κ^{ℓ−1}a + 6β_κ + 7) + B_ℓ]/B_ℓ ≤ a + 2.5κ + 10.5β_κ + 23, with
  β_κ = bitlen κ. This covers the w-vector combination, the γ^κ, the class shift (ζ powers,
  η^{±1}) and the support products.
- Θ(κ,a) = Σ_ℓ E_ℓ/B_ℓ ≤ 1 + 1/(a+1) + 1/8 + … ≤ 1.65 classifications.

The three closed bounds were also checked numerically for κ ≤ 12 and a ≤ 10⁵.

**One classification (§3.1).**
- Split α = γγ′: two pows, ≤ 4b.
- Pohlig–Hellman in ⟨η⟩: 2b for the order test; for each prime of κ, two cofactor pows, one
  base pow and a table of ℓ' ≤ κ powers, ≤ 6b + 2κβ_κ; for each of the ≤ ν digits, two pows,
  one multiplication and one inversion, ≤ 4b + 2; and ω+1 integer inversions for the CRT.
- The κ-th root in H_π′ and the factor η^f: ≤ 4b + 1.

In all: C_cls = (10 + 6ω + 4ν)b + 2ωκβ_κ + 2ν + ω + 2.

**Total (F).**

F ≤ (ν+1)·[ I·(Λ + Φ + Θ·C_cls) + (L+1)N ] + ν·[ ω(4b + 4b(ν+ω) + 1) + C_cls ] + Z(κ,b) + 2bN·[κ<d] (+ agM + a).

The four terms are, in order:
- the ν+1 runs;
- one join plus the aborted classification per restart;
- the zero sum (§4);
- the Bezout step.

The last bracket is the row reduction `_row_reduce`, which is optional: without it a = g.

**Simple form.** Use ν ≤ b−1, ω ≤ β_κ ≤ κ, b ≥ 2, κ ≥ 2, N ≥ G(κ,1) ≥ 8 and I ≤ (8/7)N. These
give:

| term | estimate |
|---|---|
| C_cls | ≤ 7κb² + 3κ³ |
| ν+1 runs | ≤ 16.6 κ³Nb(a²+b²) |
| restarts | ≤ 0.7 κ³Nb³ |
| Bezout | ≤ 0.05 κ³Nb(a²+b²) |
| Z | ≤ 18.3 κ³Nb³ (worst at κ = 2, b = 2; negligible for κ ≥ 4, where N ≥ 2¹⁶) |

The sum is below 40κ³Nb(a²+b²). Additions are at most F + (number of Theorem 11 calls)·κ!a ≤ 2F,
since κ!a ≤ G·a² ≤ the level-1 elimination cost of the call.

## 4. The van de Woestijne step

**[source]** ISSAC 2005:
- Theorem 6.2: a zero sum Σ_{i=0}^n x_i^n = 0 in Õ(n² log q) operations in F.
- Theorem 5.1 (Selective Root Extraction): Õ(n log q + log² q).
- Theorem 6.1 (b as a sum of n n-th powers): Õ(n² log q + n log² q).

§2 of the note says all its bounds are soft (log factors ignored). Full proofs are deferred to
the thesis. So the source gives an explicit exponent only up to log factors, and that bound is
not proved in the text we hold. IS §3.3 needs only this coefficient-1 case of Fact 2.

**[proved here, for the implemented variant]** This is the §6.1 reduction on −1 with the runs
representation, without the coefficient-size trick, and with the π-part Selective Root
Extraction of `selective_root` (correctness: 2026-11-02 report §3; κ+1 values always collide
modulo gcd(κ, ord η) ≤ κ).

- **Rounds.** While the number of terms T ≥ κ+1, the κ+1 blocks have size ≥ ⌊T/(κ+1)⌋ ≥ 1, and
  at least one block is dropped. So x = T − κ satisfies x′ ≤ xκ/(κ+1). That makes at most
  (κ+1) ln p + 1 rounds, plus at most κ rounds of `shorten` (each removes a term).
  - R_z ≤ ⌈(κ+1) b ln 2⌉ + κ + 2.
- **Runs.** Block cuts add at most κ runs per round, so there are ≤ 1 + κR_z runs.
- **Per round.** Block values cost (2β_κ + 4) per run. Selective Root Extraction costs
  (κ+1)·[split + join + logarithm + root] + 4b ≤ (κ+1)(6b + ω(4b + 4b(ν+ω)) + C_cls) + 4b.
- **Total.** Z ≤ R_z·[(1 + κR_z)(2β_κ + 4) + SRE] = O(κ³ log κ · b² + κ² log κ · b³) field
  operations.

**[exact]** On every prime p < 4000 and seven large primes (up to 29·2⁵⁷+1), with κ ∈ {2,4,6,8,12}
dividing p−1 (1373 pairs), measured rounds are ≤ 0.69 × R_z and measured field operations are
≤ 0.12 × Z. Odd κ needs no work.

## 5. From field operations to multitape TM steps [argued]

The proposition needs TM steps. Arithmetic on b-bit residues (multiplication, division with
remainder, extended Euclid) takes O(b²) steps on a multitape TM. The rest is data layout. Store
the columns, the per-index coefficient β_i and the per-index tag (a ∈ [κ]^ℓ, then I/J per
accumulation level) as arrays in input order. Evaluate breadth-first, one level at a time:

- Every level-ℓ node reads E_ℓ consecutive outputs of level ℓ−1, copies them to a work tape and
  eliminates there.
  - Pivot search scans the matrix, O(RE²b) ≤ O(R²Eb²) steps.
  - Row operations are sequential scans against a copied pivot row.
  - Its γ(k), class r(k) and new w-vectors are written sequentially.
- The coefficient and tag arrays are then updated in one synchronized pass. Children are
  contiguous index blocks, so the γ's are streamed in the same order.
- The sign step and the §3.3 updates are also single passes.

There are O((ν+1)Lκ) passes over arrays of O(N(b + κ log κ + L)) cells. That is O(κ² log κ · L · bN)
per run, which is absorbed into the bound. So TM steps ≤ C·(b²F + bN·polylog κ + Mgb) for an
absolute C. This is the standard argument, not a formal construction.

A generic log-cost-RAM-to-multitape-TM simulation would also give an explicit polynomial, but
it would multiply the exponent: at most cubic overhead (Papadimitriou, *Computational
Complexity*, Thm 2.5). That citation is from memory and was not checked in this pass.

## 6. The bound, assembled

κ_d ≤ d and N ≤ B_{κ_d}(g_d) ≤ M_d. Reading the input costs M_d g_d b and writing the output
costs M_d b; both are below M_d g_d² b³. So, for every grade d ≥ 2 and every prime p:

T^IS_d ≤ C₁ · d³ · M_d · b³ · (g_d² + b²),  with M_d = B_d(g_d) = d^{d(d−1)⌈log₂(d+1)⌉/2}(g_d+1)^{d⌈log₂(d+1)⌉}.

For fixed d this is O_d((g_d+1)^{d⌈log₂(d+1)⌉} · b³ · (g_d² + b²)). In prop:coherent-receiver(iv),
R_d ≤ C₀ T log T + M_d b. With this T, log T = O(log M_d + log b) = O_d(log(g_d+1) + log b).

What it does not say:
- It is a worst-case bound for this algorithm. It is not a lower bound, and it is not optimal.
- Avoiding whole-run restarts, using vdW's own SRE, or using fast multiplication would lower
  the b-exponents. None of this is claimed.

## 7. Cross-check against the implementation [exact]

**Method.** The scratch scripts are in
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/`:
`is_count.py`, `is_bound.py`, `is_table.py` and `is_zero.py`, with `.out` files. The module was
imported unchanged and monkeypatched.

- An `int` subclass counts multiplications and additions on field elements, attributed to the
  calling function.
- The module-global name `pow` is shadowed by a counting wrapper, which records exponent
  bit-lengths.
- `_kernel_vector` and `Classifier.classify` are wrapped to record matrix shapes and call counts.
- Runs use `python -O`, so the assert-only checks are stripped. The two remaining verification
  costs, the identity-(12) loop inside `theorem11` and the final `verify`, are excluded by
  function.
- Columns are random and nonzero (a zero column exits at once). Both `early_exit=False` (the full
  §3.3 and Fact 2 path) and the default were run.

**Structural check, full path** (`is_table.out`; "pred" is §2 per run):

| p | d | κ | a | N | L | T11 calls meas/pred | kernels (last run) meas/pred | kernel shapes (R,E) | GE mults ≤ Σ(R²E+R) | classifications ≤ (runs)·ΣE | restarts ≤ ν |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 2 | 2 | 1 | 64 | 2 | 9/9 | 45/45 | (1,2),(2,4) | 134 ≤ 279 | 82 ≤ 216 | 1 ≤ 1 |
| 65537 | 2 | 2 | 1 | 64 | 2 | 9/9 | 45/45 | (1,2),(2,4) | 124 ≤ 273 | 81 ≤ 216 | 1 ≤ 16 |
| 13 | 2 | 2 | 2 | 18 | 1 | 1/1 | 7/7 | (2,3),(4,6) | 102 ≤ 212 | 23 ≤ 72 | 2 ≤ 2 |
| 97 | 2 | 2 | 2 | 324 | 2 | 19/19 | 133/133 | (2,3),(4,6) | 2067 ≤ 3510 | 354 ≤ 912 | 1 ≤ 5 |
| 7 | 3 | 3 | 1 | 216 | 1 | 1/1 | 127/127 | (1,2),(3,6),(9,18) | 850 ≤ 2823 | 244 ≤ 684 | 1 ≤ 1 |
| 163 | 3 | 3 | 2 | 729 | 1 | 1/1 | 271/271 | (2,3),(6,9),(18,27) | 10941 ≤ 21106 | 809 ≤ 2997 | 2 ≤ 4 |
| 536871001 | 3 | 3 | 2 | 729 | 1 | 1/1 | 271/271 | (2,3),(6,9),(18,27) | 10683 ≤ 21092 | 796 ≤ 1998 | 1 ≤ 1 |

Four more rows are in the file, all OK. The node counts per level equal G/B_ℓ; for example,
κ = 3, a = 1 gives 108, 18, 1. The per-kernel ratio of measured multiplications to R²E reaches
1.00: the bound is attained on the 1×2 and 2×3 kernels.

**Totals vs (F)** (`is_bound.out`). There are 20 (p, d, a) instances in both exit modes:
- κ = 2 at p ∈ {7, 13, 97, 257, 65537, 536870951, 536871001};
- κ = 3 at p ∈ {7, 13, 19, 163, 536871001};
- κ = 1 at p ∈ {5, 11, 101} with d = 3.

Measured multiplications + pow-multiplications + inversions are between 0.006 and 0.22 of (F) for
κ ≥ 2. For κ = 1 they are 0.75–1.00 of the κ = 1 bound; it is attained at p = 11. Measured
additions are ≤ the multiplications in every case.

Restart stress (spread kernels, 8 seeds, at p = 65537, 257, 163 and 786433): at most 3 restarts
were observed, against ν = 16, 8, 4 and 18. All totals were within (F). Random inputs never
approach ν restarts, so the restart factor is not tested at its worst case. It is proved
(§2, Step 3), not measured.

**Not checked by this computation:**
- Any κ ≥ 4 run, which is too large to execute.
- The TM layout of §5.
- The worst-case restart count.

## 8. Status of each part

| Part | Status |
|---|---|
| Recursion structure (§2): calls, sizes, ≤ ν+1 runs | [proved] from IS §§3.1–3.3; matches the code [exact] |
| Field-operation count (F) and 40κ³ simple form | [proved] (elementary counting); grid sup 5.74 [exact] |
| Zero-sum step for the implemented variant | [proved] rounds/runs/SRE count; [exact] on 1373 pairs |
| vdW's own Õ(κ² log p) | [source], soft-O, proof in the thesis (not seen) |
| Correctness of the substitute SRE | 2026-11-02 report §3 (AI-checked) |
| O(b²) per field operation on a multitape TM | standard |
| Constant-factor TM overhead (§5) | [argued], not formalized |
| T^IS_d ≤ C₁ d³ M_d b³(g_d² + b²) | [proved] modulo §5 [argued]; C₁ absolute, not computed |

Claim gates that must stay false: `general_sde_implemented`, `coherent_receiver_implemented`,
`independent_review`, `formal_compiler_checked`, and every Rees novelty, priority or
receiver-execution gate. This pass bounds a classical solver's running time and implements
nothing.

## 9. Proposed LaTeX (not applied; AI-checked, pending human review)

A remark after Remark `rem:is-import`:

```latex
\begin{remark}[Explicit running time of Schedule~1; AI-checked, pending human review]
\label{rem:is-runtime}
Let $\kappa = \kappa_d \ge 2$, $a = g_d$, $b = \lceil\log_2 p\rceil$, $G = G(\kappa,a)$, and let
$\nu \le b-1$ be the number of prime factors, with multiplicity, of the largest divisor of $p-1$
all of whose prime factors divide $\kappa$. The algorithm of Theorem~\ref{thm:is-import} makes at
most $\nu+1$ runs, since each restart of \cite[Section~3.1]{IvanyosSantha2015} strictly enlarges a
subgroup of a cyclic group of order dividing $p-1$. Each run makes $\sum_{j<L}G^j$ calls of
\cite[Theorem~11]{IvanyosSantha2015}, with $L = \lceil\log_2 \ell_d\rceil$. One call runs
\cite[Lemma~12]{IvanyosSantha2015} with $G/B_\ell$ nodes at level $\ell$ (with
$B_\ell = \kappa^{\ell(\ell-1)/2}(a+1)^\ell$); each node is one kernel computation for a
$\kappa^{\ell-1}a\times\kappa^{\ell-1}(a+1)$ matrix and at most $\kappa^{\ell-1}(a+1)$
classifications, and each classification is a Pohlig--Hellman logarithm of
$O((\nu+\log\kappa)b+\kappa\log^2\kappa)$ multiplications. The zero sum of $\kappa$-th powers, computed by the
reduction of \cite[Section~6.1]{vandeWoestijne2005}, uses $O(\kappa^3 b^2\log\kappa +
\kappa^2 b^3\log\kappa)$ field operations, independently of $a$ and of the columns. Counting all of
this, together with the Bezout step of Remark~\ref{rem:is-import}(b), gives at most
$40\kappa^3 N b(a^2+b^2)$ multiplications and inversions in $\Fp$ and at most twice as many
additions, where $N = G^{L} \le B_{\kappa}(a) \le M_d$. With schoolbook arithmetic and a
level-by-level layout, a multitape Turing machine therefore computes the witness of Schedule~1
within
\[
  T^{\mathrm{IS}}_d = C_1\, d^3\, M_d\, b^3\,(g_d^2 + b^2)
\]
steps, for an absolute constant $C_1$. For fixed $d$ this is
$O\bigl((g_d+1)^{d\lceil\log_2(d+1)\rceil}\, b^3 (g_d^2+b^2)\bigr)$, and
$O\bigl(M_d b^2(g_d^2+b)\bigr)$ when $\nu$ is bounded. The derivation and an instrumented check
of the operation counts of \file{theorems/rees_is_sde_solver.py} at $\kappa_d\le 3$ are in
\file{research/audits/reviews/2026-11-04-rees-is-runtime.md}.
\end{remark}
```

For `prop:coherent-receiver`, append one sentence to item (iv):

```latex
By Remark~\ref{rem:is-runtime} one may take $T^{\mathrm{IS}}_d = C_1 d^3 M_d b^3(g_d^2+b^2)$,
so that $R_d = O\bigl(d^3 M_d b^3 (g_d^2+b^2)\log(M_d b)\bigr)$.
```

In the discussion after the proof, replace "and no explicit polynomial $T^{\mathrm{IS}}_d$,
exists" with:

```latex
and the explicit bound $T^{\mathrm{IS}}_d$ of Remark~\ref{rem:is-runtime} rests on a
standard Turing-machine layout argument that is not written out
```

Two notes for the integrator:

- **(v) needs the clock to be explicit.** The clock is C₁d³M_db³(g_d²+b²), and C₁ is fixed
  once the machine is fixed. If the referee wants a numerical C₁, that requires an actual TM
  construction, which nobody has done.
- **vdW's own bound must not be quoted as proved.** If the text cites
  \cite[Theorem~6.2]{vandeWoestijne2005} for the zero-sum cost instead, write
  "$\tilde O(\kappa^2\log p)$ field operations (soft-$O$; proof in the thesis)".

## 10. Next

- **Hard question.** Can the ν+1 whole-run restarts be avoided, for example by classifying with
  respect to a generator fixed in advance from the column data? Doing so would remove one
  factor of b.
- **Mechanical.** Apply §9 to main.tex; this is the integrator's call. Optionally, archive the
  four scratch scripts beside this note, so the cross-check survives the session.
  - Acceptance test: rerun `python -O is_bound.py`; it prints `simple-form failures: 0`, every
    row has ratio ≤ 1, and `is_table.py` prints OK on every row.
