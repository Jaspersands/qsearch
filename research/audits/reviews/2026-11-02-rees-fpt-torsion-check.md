# Rees extensions A and B: Cor `cor:fpt-r` and Thm `thm:ring-to-field`

Date: 2026-11-02. Reviewer: Claude Code (Opus 5.5), side session, AI only. **No human
review.** Brief: `research/REES_EXTENSIONS_CHECK_BRIEF.md`, items A and B. The core (steps 1–5
of Thm `thm:main`) is taken as proved, per `2026-11-01-rees-core-proof-check.md` §4 and §5.1.
I edited no other file. `git status --short` before and after the runs differs only by
untracked files of the parallel sessions (`2026-11-02-rees-black-box-check.md`,
`2026-11-02-rees-combined-schedule.md`, `2026-11-02-rees-schedules/`) and this review's own
directory.

Text read: `docs/papers/rees-hsp/main.tex` lines 88–92, 165–200, 425–456, 520–580;
`research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md` §§1–5 (lines 1–213);
`research/UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md` lines 1–233 (§§1–3);
`research/CLASS_THREE_HSP_THEOREM_DRAFT.md` lines 105–130 (the frozen-normalizer warning);
the three claim-gate JSONs named in §5. Primary source: Ivanyos–Magniez–Santha,
arXiv:quant-ph/0102014v1 (fetched from arxiv.org, full text via `pdftotext`, 12 pages), read in
§2 (model, p. 3), §3 (Thm 4, Cor 5, pp. 4–6), §4 (Thms 6–8, pp. 6–7) and §5 (Thm 11, p. 9).

Scripts (new, import nothing from the repo), in `research/audits/reviews/2026-11-02-rees-extensions/`:

| Script | Checks | Output |
|---|---|---|
| `A/a1_uniformity.py` | exact-integer Schedule 3 bounds at c = u = r+1, r ≤ 300; filiform profile; IMS-size bound | `A/a1_uniformity_out.txt` |
| `A/a1_banks.py` | per-bank witness counts, filiform profiles r = 1, 2, 3 at the smallest admissible p | `A/a1_banks_out.txt` |
| `B/b_recursion.py` (Sage/FLINT lattices) | (i)–(iii) of Thm ring-to-field on six mixed-order Lie rings, 293 (ring, H) pairs, brute-force group checks | `B/b_recursion_out.txt` |

Reproduce (about 10 s, 90 s and 55 s):

```bash
cd research/audits/reviews/2026-11-02-rees-extensions/A && /opt/anaconda3/bin/python a1_uniformity.py
```
```bash
cd research/audits/reviews/2026-11-02-rees-extensions/A && /opt/anaconda3/bin/python -u a1_banks.py
```
```bash
cd research/audits/reviews/2026-11-02-rees-extensions/B && /opt/anaconda3/envs/qsearch-cas/bin/python -u b_recursion.py
```

## 0. Verdicts

| Q | Verdict | Evidence |
|---|---|---|
| A1 uniformity in c | **Holds**, with constants independent of c | written derivation; exact integer check (`a1_uniformity.py`) |
| A2 hypotheses, label law | **Holds** | proof; filiform family attains c = r+1 |
| A3 IMS fallback | **Holds with a stronger hypothesis/extra step**: IMS gives constant bounded error; reaching ε needs an amplification step the paper does not state (given below, elementary) | full-text citation + argued |
| A4 gap p ≤ c | **Holds** (nothing claimed for c ≥ p); wording "all-prime" is loose | text check |
| B1 socle facts | **Holds** | proof + exact checks |
| B2 restriction + core | **Holds, conditional on A** | proof |
| B3 outer recursion | **Holds**, given two unstated stop rules (no call on a trivial section; reject a returned subspace that is not a strictly larger subalgebra) | proof + exact simulation with a truth core |
| B4 note vs paper | The paper's (iii) is **a different and stronger algorithm** than the note's (≤ b calls vs b(b+1)/2); it survives, but its proof is the paper's own | text comparison |

No gap that breaks either bound, and no counterexample. Nothing here is verified by a human.

---

## A. Cor `cor:fpt-r` (`main.tex:540–550`)

### A1. Uniformity in c

**Verdict: Holds.** Every c-dependent quantity of Thm `thm:random-column` is bounded using
only c ≤ u, κ_d ≤ d ≤ c ≤ u and a_d ≤ u−1, so the constants are absolute once u = r+1.

Derivation (u = r+1, M = 4u, p ≥ 16u², c ≤ u; κ = κ_d = gcd(d, p−1), h = (p−1)/κ):

1. *Per bank.* μ_d = ((h+1)^M − 1)/(h p^{a_d}) ≥ h^{M−1}/p^{a} ≥ p^{M−1−a}/(2κ)^{M−1}
   ≥ (16u²)^{3u}/(2u)^{4u−1} = 2^{8u+1}u^{2u+1}. This uses κ ≤ u and a ≤ u−1 only, not c.
   Acceptance N_0/(2p^M) ≥ 1/(4κ^M) needs h+1 ≥ p/κ and p ≥ 2κ, both true.
2. *Tree.* Merge nodes T ≤ M^{c−1} ≤ (4u)^{u−1}, so the bank events sum to
   ≤ (4u)^{u−1}(4/μ + 2p^{a−M}) ≤ 2^{−6u−1}u^{−u−2} + 2^{−10u−5}u^{−5u−3} ≤ 1/64.
   B = ⌈log₂(64 M^{c−1})⌉ ≤ 7 + (u−1)log₂(4u) = O(u log u); arithmetic caps add 3·2^{−B}·T ≤ 3/64.
   One tree aborts with probability ≤ 1/16, for every c ≤ u.
3. *Restart and error.* 4m' trees, m' = m + ⌈log₂(3/ε)⌉; fewer than m' successes with
   probability ≤ 2^{4m'}(1/4)^{3m'} = 2^{−2m'} ≤ ε/3; rank failure ≤ ε/3; approximation ε/3 over all
   N_instr ≤ 4m'(M^{c−1} + T + 1) instruments. None of these depends on c except through
   M^{c−1} ≤ (4u)^{u−1}.
4. *Charged cost.* Original queries ≤ 4m'·c·M^{c−1} ≤ 4m'(r+1)(4r+4)^r. Classical trials per node
   4κ^M B ≤ 4u^{4u}B, over ≤ 4m'·T nodes. Each controlled right action costs 4 BCH evaluations of
   (c−1)c(c+1)(c+2)/6 ≤ (r+1)^4 brackets at O(n³) field operations, n ≤ cm ≤ (r+1)m. A lifted
   source needs c ≤ r+1 distinct nonzero points (p−1 ≥ c holds) and a c×c Vandermonde solve.
   QFT precision bits O(log N_instr + log q_max + log(1/ε)) = O(r log r + log(m/ε)). Total:
   2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)) + Q·T_f, absolute constants.
5. *Steps 1–2.* The core check proved them for every c < p (core §1–2, §4); their costs are
   polynomial in c. Nothing there assumes fixed c.

Machine check (`a1_uniformity.py`, exact integers and `Fraction`): 92 cases, r = 1..40 and
60..300, worst case c = u and a_d = u−1 at **every** grade, p = least prime ≥ 16u² and
p = 2^61−1. Zero failures of the μ bound, the acceptance bound, bank sum ≤ 1/64 and tree abort
≤ 1/16 (the bank sum also stays ≤ 1/64 with the looser leaf count M^{c−1}).
log₂(queries per tree)/(r log₂(r+2)) is at most 2.53 and falls to 1.25 at r = 300;
log₂(classical trials per tree)/(r log₂(r+2)) is at most 8.31 (r = 1) and stays ≤ 7.14 for r ≥ 2.

Reviewer must still check: the gate constants of Thm `thm:uniform-compilation` (taken from the
paper, not re-derived), and Thm `thm:random-column` itself, which has an AI proof check only
(core §5.5).

### A2. Hypotheses and the label law

**Verdict: Holds.**

- *c ≤ r+1.* In a nilpotent algebra γ_{d+1} = γ_d ≠ 0 would never reach 0, so
  g_2 > g_3 > … > g_c ≥ 1 with g_2 = r, giving c−1 ≤ r. The filiform algebra
  (x, e_1..e_{r+1}, [x, e_i] = e_{i+1}) attains c = r+1 (`a1_uniformity.py`, r ≤ 20).
- *u ≥ c, u > max a_d.* a_d = g_d − dim(h ∩ γ_d) ≤ g_d ≤ r < u. u = r+1 is public (dim [L,L] by
  linear algebra), so no hidden quantity is used. u ≥ 2 needs r ≥ 1, the corollary's hypothesis.
- *Label law at every grade.* Induct from the leaves. A grade-d node consumes M children. Each
  child is a whole subtree, and by core (2d) its output is ρ_{H_d} for every value of its own
  record. The children use disjoint fresh sources, so conditional on any event about all
  earlier records (in particular "all M children succeeded"), their outputs are ρ_{H_d}^{⊗M}.
  Measuring Z_d then gives i.i.d. uniform labels on K_d^⊥, independent of every earlier record.
  The node's acceptance does depend on its own labels, so those labels are not i.i.d. given
  acceptance (source note §4 says so). That does not matter: nothing later reads them, and by
  (2c) the node's output is ρ_{H_{d−1}} for every accepted record. The union bound is taken in
  execution order, Pr[some node fails] ≤ Σ_v Pr[v fails | predecessors succeeded], and each
  conditional bank law is exactly i.i.d. uniform. This holds at every grade d = c, …, 2. The
  approximation error is charged once, by the whole-algorithm hybrid (Thm random-column (ii)).

Exact falsifier runs (`a1_banks.py`; DP exact for a = 1, exact main term plus float64 character
sum for a ≥ 2), filiform profile with H = 1 (so a_d = g_d), smallest admissible prime:

```text
r=1 p=67  d=2 kappa=2 a=1 M=8:  200/200 banks have a witness; min acceptance 4.4e-03 vs bound 9.8e-04
r=2 p=149 d=2 kappa=2 a=2 M=12:  60/60;  min 2.6e-04 vs 6.1e-05
r=3 p=257 d=2 kappa=2 a=3 M=16:  20/20;  min 1.6e-05 vs 3.8e-06
r=3 p=257 d=4 kappa=4 a=1 M=16: 200/200; min 2.8e-10 vs 5.8e-11
```

No bank fell below 1/(4κ^M); the ratio was 4.3–4.8 throughout. (κ = 1 grades are linear and are
skipped.) These samples cannot see events below about 10^{−2}; the bound is the written proof.

Reviewer must still check: the (2c)/(2d) factorization when a subtree is aborted midway (it
is charged as a failed tree, and its partial outputs are never used).

### A3. The IMS fallback (p < 16(r+1)²)

**Verdict: Holds, with an extra step for ε.** Full-text citation of arXiv:quant-ph/0102014v1.

What IMS states and assumes:

- *Model* (§2, p. 3). Black-box group: elements are n-bit strings, the group is given by
  generators, and the input size is the encoding length times the number of generators. Oracles
  U_G|g⟩|h⟩ = |g⟩|gh⟩ and U_G^{−1}|g⟩|h⟩ = |g⟩|g^{−1}h⟩. Strings that encode no element may behave
  arbitrarily. The hiding function f: {0,1}^n → {0,1}^m is constant on **left** cosets and
  distinct on distinct cosets, with m given in unary. Errors are "bounded by some fixed
  constant 0 < ε < 1/2" (p. 3), not by an input ε.
- *Theorem 11* (§5, p. 9): "Let G be a black-box group with unique encoding of elements. The
  hidden subgroup problem in G can be solved by a quantum algorithm in time polynomial in the
  input size + |G′|." H is **arbitrary**. Neither |G′| nor generators of G′ are inputs: the proof
  enumerates G′ from conjugates of commutators of the generators. It hides HG′ (normal, since
  G/G′ is abelian) by F(x) = {f(xg) : g ∈ G′}, using |G′| queries of f per F evaluation. It finds
  HG′ by Thm 8 (p. 7), which rests on Beals–Babai (Thm 4, Cor 5) with ν(G/HG′) = 1 and on Shor
  order finding (Thm 6–7). Finally it selects an element of xG′ ∩ H for each generator x by
  enumeration.

Does the explicit Lazard chart meet them? Yes:

- unique encoding: canonical coordinate vectors in F_p^m (non-canonical strings, i.e.
  coordinates ≥ p, may behave arbitrarily, which IMS allows);
- generators: the basis vectors; the subgroup they generate has log equal to the Lie subring
  they generate, which is L (Lazard, c < p); input size m·m⌈log₂ p⌉;
- U_G is x, y ↦ x ∗ y by reversible BCH; U_G^{−1} uses (−x) ∗ y. Each call costs
  poly(m, c, log p) with c ≤ r+1. IMS counts oracle calls as unit time, so this factor must be
  charged;
- f is the Rees oracle (left cosets, label width w);
- |G′| = |exp[L, L]| = p^r, since γ_2(G) = exp γ_2(L) for c < p (core §1.1).

*Time.* poly(ℓ + |G′|) ≤ 2^k ℓ^k |G′|^k with IMS's unspecified absolute exponent k, so the
branch costs poly(m, log p, w)·p^{O(r)} (oracle calls times BCH cost). For p < 16(r+1)², p^r is
2^{O(r log(r+2))}: `a1_uniformity.py` gives log₂(p^r)/(r log₂(r+2)) ≤ 3.74 for r ≤ 300, and in
general log₂ p < 4 + 2 log₂(r+1). So "poly(input) + poly(|G′|)" versus "poly(input)·|G′|^{O(1)}"
does not matter here: both are 2^{O(r log(r+2))}·poly.

*Missing step: error ε.* The corollary claims poly(log(1/ε)), but IMS gives a fixed constant
error. Amplification is elementary and should be stated: run IMS k = O(log(1/ε)) times; for each
output H′ check f(x) = f(1) on its returned generators (one query each), which certifies H′ ≤ H;
compute |H′| (the log of ⟨H′⟩ is the Lie subalgebra its logs generate: linear algebra); output the
largest certified H′. If any run is correct it has order |H|, and a certified H′ ≤ H with
|H′| = |H| equals H. Failure ≤ ε_0^k. Cost: a factor O(log(1/ε)).

Reviewer must still check: the IMS proof of Thm 8 via Beals–Babai (a published result read here,
not re-derived); that the canonical set-valued F (sorted list of |G′| labels, width |G′|·w) is
a valid input to Thm 8 (it is, since m is part of the input in unary and |G′|w is polynomial in
input + |G′|).

### A4. The gap 1 < p ≤ c

**Verdict: Holds.** The corollary's statement has c < p, and Table row `main.tex:195` says
"all p > c". The proof's IMS branch, though it would also run on groups of class ≥ p, is used
only under the Lazard input contract, which requires c < p. Primes p ≤ r+1 are covered only for
algebras whose actual class is below p, consistently. Nothing is silently claimed for c ≥ p.
Two loose phrasings: the corollary's title ("All-prime bound", `main.tex:540`) and the abstract
("an all-prime bound", `main.tex:92`) omit "p > c". The source note's "for ALL primes with c<p"
is correct.

---

## B. Thm `thm:ring-to-field` (`main.tex:563–580`)

Setting: L ≅ ⊕_{i=1}^m Z/p^{e_i} with explicit structure constants, class c < p, G = (L, ∗)
by BCH over Z[1/c!], b = Σe_i, R = dim_{F_p}([L,L]/p[L,L]) = d_add([L,L]).

### B1. Part (i)

**Verdict: Holds.** Proof: p[x,y] = [px,y] = 0 for x ∈ L[p], so L[p] is an ideal, with basis
p^{e_i−1}ε_i. Since g^k = exp(kx), g^p = 1 ⇔ px = 0, so exp L[p] = {g : g^p = 1}, a normal
subgroup. Also [L[p], L[p]] ⊆ [L,L][p], and dim A[p] = d_add(A) for a finite abelian p-group A,
so dim [L[p], L[p]] ≤ R. Strict decrease of the lower central dimensions gives class ≤ R+1, and
class ≤ c because L[p] is a subring. The class of L[p] is < p because c < p, not because
R+1 < p (that need not hold; the note says so).

Exact checks (`b_recursion.py`): on all six rings the socle is an ideal with class and derived
dimension within min(c, R+1) and R. Brute force under the BCH product (|G| = 729, 15625, 3125)
gives {g : g^p = 1} = L[p].

### B2. Part (ii)

**Verdict: Holds, conditional on item A.** For x, y ∈ Ω_1(G), f(x) = f(y) ⇔ x^{−1}∗y ∈ H ∩ Ω_1(G),
so the restriction hides H_1. The F_p-structure tensor of L[p] is obtained by dividing the
coordinates of brackets of the basis p^{e_i−1}ε_i by p^{e_k−1}, in poly(B); no inversion of p in
a torsion ring is needed. The embedding into L is a public linear map, so each local query costs
one query of f. The input has dimension m, class ≤ min(c, R+1) < p and derived dimension
r_loc ≤ R, so Cor `cor:fpt-r` gives 2^{O(R log(R+2))}·poly(B, w, log(1/ε)) (the function
2^{O(r log(r+2))} is monotone in r). If r_loc = 0, abelian Fourier sampling suffices. Everything
here inherits A's conditional status (Thm random-column and IMS).

### B3. Part (iii), the outer recursion

**Verdict: Holds**, given two stop rules the text leaves implicit (fix 2 in §6).

- *H ≤ N_G(H_1), and log N is the idealizer.* H normalizes H and the normal subgroup Ω_1(G), so
  it normalizes H_1. Conjugation by exp x is exp(ad_x), with ad_x^c = 0. Conversely,
  ad_x = log(1 + (e^{ad_x} − 1)) has denominators < c < p. So exp x normalizes exp(log H_1) iff
  [x, log H_1] ⊆ log H_1. This is the kernel of the Z-linear map x ↦ ([x, k_j] mod log H_1)_j,
  computable by HNF/SNF (or Howell form mod p^{max e_i}) with transformation matrices, in
  poly(B). Exact: the idealizer equals the brute-force group normalizer for 36 (ring, H)
  pairs (`b_recursion.py`).
- *Quotient oracle.* For an ideal k = log H_1 of log N, every BCH term beyond x + y contains a
  bracket with an entry of k, so x ∗ k = x + k. Left cosets are additive cosets (checked by brute
  force on samples). Hence f_loc(t) = f(σ(t)) with an additive normal-form section σ hides H/H_1:
  σ(t)^{−1}∗σ(t′) ∈ H ⇔ t^{−1}t′ ∈ H/H_1, because H ⊇ H_1 is a union of H_1-cosets. That is one
  query per query, and σ is computed and uncomputed reversibly from public lattice data. The
  section log N / log H_1, with SNF coordinates, is an explicit Lie ring of class ≤ c < p
  (Lazard for normal subgroups).
- *Rank and class of every section.* Every nested section is S/K with S a Lie subring of L and K
  an ideal of S, since preimages compose. Its derived ring ([S,S]+K)/K ≅ [S,S]/([S,S] ∩ K) is a
  quotient of a subgroup of [L,L]. For finite abelian p-groups, U ≤ A gives U[p] ↪ A[p], and a
  quotient A/W is generated by images, so d_add cannot increase. Hence the derived additive rank
  is ≤ R, and the class is ≤ class(S) ≤ c < p.
- *Termination and error.* If the current section S/K is nontrivial and H ≠ K, then H/K ≤ S/K
  (H ≤ S by induction) is a nontrivial p-group, so it meets Ω_1(S/K) nontrivially, and the new
  known part H_1′ ⊋ K. Each nontrivial step multiplies |K| by ≥ p, so there are ≤ log_p|H|
  nontrivial steps, plus one final trivial call when H ≠ S. That is ≤ b calls **provided no
  call is made on a trivial section** (H = G otherwise costs b+1). On erroneous branches a
  wrong core answer may not be a subalgebra strictly containing K; the procedure must reject it
  and stop (or impose the cap b), so the call count holds on every branch. The error is ε/b per
  call by a first-error union bound over adaptive calls. Public arithmetic is deterministic.
- *Readout over mixed orders.* The recursion never Fourier-samples a mixed-order group. Each core
  call reads out over F_p (Ω_1 of a section), and the final log H is the lattice K assembled by
  sums and preimages. The Z/3 × Z/9 annihilator failure (`main.tex:561`) does not arise.
- *Frozen normalizer.* `CLASS_THREE_HSP_THEOREM_DRAFT.md:117–121` warns against quotienting by a
  known K ≤ H that is not normal in H, or forming G/K for non-normal K. Here each H_1′ is
  H ∩ (a normal subgroup of the section), so it is normal in H, and the recursion forms only
  N/H_1′ with N its recomputed normalizer inside the current section. The warning does not apply.

Exact simulation (`b_recursion.py`): the outer recursion with a **truth oracle** for the field
core (the core is taken as given; this tests only the outer algebra). Six rings: Heis₃(Z/9)
(p = 3); [x,y] = py on (Z/125)² and (Z/625)² (p = 5, class 3 and 4, R = 1); a mixed-order ring
Z/25·x ⊕ Z/5·y ⊕ Z/25·z with [x,y] = 5z, [x,z] = y (class 3, R = 2); n₄(Z/25) (class 3, R = 3);
a mixed Heisenberg of orders 27, 9, 9 (p = 3). There were 293 (ring, H) pairs, with H random Lie
closures of 1–3 elements biased to torsion, plus 0, L, L[p], [L,L] and the cyclic coordinate
subrings. Every step satisfied H ≤ N, H_1′ ideal in N, section class ≤ c, section derived rank
≤ R, core class ≤ min(c, R+1) and core derived dimension ≤ R. The output equalled log H every
time, with calls ≤ b (max 3, 4, 5, 3, 3, 4 against b = 6, 6, 8, 5, 12, 7). The note's
restart-in-original-L variant gave the same outputs. Brute force on the three small groups
confirmed that the group closure of the generators equals the Lie closure (Lazard on mixed
orders) for every tested H.

Reviewer must still check: the polynomial-time HNF/SNF-with-transforms claim (standard:
Kannan–Bachem, Storjohann; not re-derived), and the sizes of nested SNF coordinates (note §2
bounds HNF entries by p^b).

### B4. Paper vs source note

**Finding: the paper's (iii) is not the note's algorithm.**

| Point | Note §§1–3 | Paper `thm:ring-to-field` | Status |
|---|---|---|---|
| Outer loop | ascending central flag of the section, field call on I_i[p] with an order-≤p promise, one new element per success, restart in the original L | full socle intersection H ∩ Ω_1(section), recurse in the nested section N/H_1 | paper's own; checked here (B3) |
| Core calls | ≤ b(b+1)/2 | ≤ b | paper stronger; holds with the stop rules of B3 |
| Error per call | ε/[b(b+1)/2] | ε/b | each matches its own loop |
| Core selection | abelian / nil-2 / field bound by r_local | abelian / Cor fpt-r | equivalent for the bound |
| B | full bit length **including oracle label width** | "including the e_i log₂ p coordinate bits" | paper omits w (fix 4) |
| Oracle cost | Q·T_f charged separately | not stated in the theorem | fix 4 |
| Quotient oracle | normal-form section, one query per query (§2) | same, and the paper cites it | matches |

The paper's quotient-oracle paragraph (`main.tex:577`) says "This is the construction of the
source note, Section 2". That is true of the oracle, but the recursion of (iii) is different. The
artifact paragraph (`main.tex:579`) does say that the recorded caps b(b+1)/2 belong to the
note's flag scan and that (iii) needs only b. Nowhere is the paper's statement stronger than
what survives B3.

---

## 4. Falsifier hunt (brief §4)

- **A:** filiform, c = r+1, worst a_d at every grade, smallest admissible p. No bank below the
  acceptance bound, and no growth of the exact bank or abort sums with c (A1, A2). No
  counterexample.
- **B:** derived cyclic rank > R, class ≥ p, or a stalling recursion is impossible by B3's
  proof. None appeared in 293 exact runs, including mixed orders where sections reach class
  c = 4 (the (Z/625)² family) and core class R+1 = 3 (n₄(Z/25)).

## 5. Surviving statements, matching wording, gates

**A (surviving).** Let p be prime and L ≅ F_p^m an explicit F_p-Lie algebra of class c < p, with
c **not** fixed and r = dim[L,L] ≥ 1. Let G = (L, ∗), let H ≤ G be any subgroup, and let f be a
coherent left-coset hiding oracle of label width w and cost T_f. A quantum algorithm returns a
basis of log H with probability ≥ 1−ε in time 2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)), plus
Q·T_f with Q = 2^{O(r log(r+2))}·poly(m, w, log(1/ε)). The O(·) constants are absolute and
independent of c. Routes: for p ≥ 16(r+1)², Schedule 3 with u = r+1 (uses the i.i.d. label law of
fresh ideal sources; conditional on Thm random-column, AI-checked only); for p < 16(r+1)², IMS
Thm 11 on the Lazard chart, with constant error amplified by verified largest-order selection;
for r = 0, abelian HSP.

**B (surviving).** Let L ≅ ⊕_{i=1}^m Z/p^{e_i} be an explicit Lie ring of class c < p, with
b = Σe_i, B the full input length including the label width, and R = d_add([L,L]). With the
same oracle and any H, the recursion of (iii) returns log H with probability ≥ 1−ε. It makes at
most b calls to (ii), none on a trivial section, each with error ε/b and one original query per
local query. Time: b·2^{O(R log(R+2))}·poly(B, log(b/ε)) + poly(B) public HNF/SNF arithmetic +
Q·T_f. Conditional on A.

**Matching table rows** (`main.tex:195–196`):

| Regime | Prime condition | SDE schedule | Total time |
|---|---|---|---|
| Derived dim. r (class not fixed) | all p > c | random column (p ≥ 16(r+1)²) / IMS Thm 11 (p < 16(r+1)²) | 2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)) (Cor. fpt-r) |
| Torsion rank R | all p > c | socle core via Cor. fpt-r, ≤ b normalizer rounds (Thm. ring-to-field) | 2^{O(R log(R+2))}·poly(B, log(1/ε)) |

The current rows are correct; the class-not-fixed note and the branch thresholds are optional
additions.

**Claim gates that must stay false.**
- `research/reductions/rees_hsp_reduction.json`: `independent_review`, `novelty_established`,
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`,
  `formal_compiler_checked`.
- `research/reductions/random_column_rees.json`: `whole_rees_correctness_certified`,
  `joint_source_law_verified`, `fixed_bank_success_guaranteed`, `intrinsic_rank_promise_verified`,
  `arithmetic_controls_certify_iid_source`, `quantum_receiver_implemented`,
  `novelty_established`, `proof_promotion`, `candidate_promotion`, `speedup_claim_allowed`.
- `research/reductions/ring_to_field_rank_reduction.json`: `full_outer_reduction_implemented`,
  `field_core_newly_proved`, `quantum_receiver_implemented`, every control's
  `original_hidden_subgroup_recovered` and `hidden_subgroup_recovery_certified` (this review's
  simulation uses a truth core and recovers nothing quantumly), `proof_promotion`,
  `candidate_promotion`, `speedup_claim_allowed`.

## 6. Text fixes (ranked; listed, not applied)

1. **`main.tex:546` (Cor fpt-r proof, IMS branch).** IMS gives a fixed constant error (IMS §2,
   p. 3). Add the amplification: O(log(1/ε)) runs, certify H′ ≤ H by f(x) = f(1) on the returned
   generators, and output the largest certified H′. Also say that IMS's time counts group-oracle
   calls as unit cost, so each call is charged one reversible BCH evaluation, poly(m, r, log p).
   Cite "Theorem 11, Section 5" of the arXiv version.
2. **`main.tex:569` (Thm ring-to-field (iii)).** State the stop rules: make no call on a trivial
   section; reject (and stop on) a returned subspace that is not a Lie subalgebra strictly
   containing the known part. "At most b calls" is then true on every branch. Without the first
   rule, H = G costs b+1.
3. **`main.tex:577`.** "This is the construction of the source note, Section 2" applies to the
   quotient oracle only. Say that the recursion of (iii), with full socle intersections in nested
   sections, is this paper's, and that the note's central-flag scan uses up to b(b+1)/2 calls.
4. **`main.tex:559` and `:568`.** Include the oracle label width in B (as the note does), and
   charge Q·T_f separately in (ii)/(iii).
5. **`main.tex:540` and `:92`.** Replace "All-prime bound" / "an all-prime bound" with "for every
   prime p > c, class not fixed".
6. **`main.tex:546`.** Optionally say that the large-p branch inherits Thm random-column's
   dependence on the i.i.d. label law (AI-checked only), so the corollary stays conditional for
   that reason too, not only through the core.
7. **`main.tex:449` (Thm random-column (ii)).** The cost line lists poly(m, log p, log(1/ε)). Add
   the label width w, as the corollary does.
8. **`main.tex:574` (proof of (i)–(iii)).** Optionally add one line: every nested section is
   S/K with S a subring and K an ideal of S, so the rank argument covers all depths.
