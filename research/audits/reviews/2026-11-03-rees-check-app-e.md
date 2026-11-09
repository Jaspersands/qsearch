# Rees round 4, item 5: unanchored proof check of Appendix E (hidden codimension)

Date: 2026-11-03 (night of 11-02). Reviewer: Claude Code (Opus 5.5), side session, AI only.
**No human review. AI-checked, pending human review** applies to every verdict below.
Brief: item 5 of `research/REES_FULL_CAMPAIGN_4.md`, under that file's shared rules.

Target: `docs/papers/rees-hsp/appendix-codimension.tex` (all 328 lines), plus `cor:codim` and
`rem:codim` in `main.tex` (lines 685–703). The statements they use, read in `main.tex`:
`def:input-contract`, `thm:main`, `thm:rees-cover`, `lem:homogeneous`, `lem:central`,
`prop:descent`, §`sec:recursion` with `lem:hybrid`, `thm:random-column`,
`thm:uniform-compilation` and `cor:fpt-r`.

Order of work. I read the appendix and those statements first, formed a verdict on every
step by hand, and wrote and ran my own scripts (below). Only after that did I read the 11-02
review `2026-11-02-rees-codimension.md` (§0, §2, §§7–9) and the round-2 hand-over note in the
shared notes folder. I did not open the 11-02 scripts. The comparison is in §4.

Files written: this report and `research/audits/reviews/2026-11-03-rees-check-app-e/`, nothing
else. Nothing committed and no claim gate changed.

## 0. Bottom line

**No step of the appendix fails, and no gap breaks Theorem `thm:app-codim` or Corollary
`cor:codim`.** Every lemma has a complete, elementary proof, apart from the two cited
conditional dependencies (`thm:main` and `thm:random-column`) and the Lazard correspondence.
I found one false sentence and four places where the wording should be tightened:

1. **The open question after Prop `prop:app-codim-size` is settled, and the answer is no.**
   "We do not know whether class at most b always holds" has a five-dimensional counterexample:
   class 4 with b = 3. Both bounds of the proposition are **attained at b = 3 by a single
   algebra**: dimension 6 = b(b+1)/2 and class 5 = 2b−1. That algebra is a k = 3 terminal of
   class 5 = 2k−1, so the bound c_J ≤ 2k−1 of Prop `prop:app-codim-complete`(iii) is sharp at
   k = 3. In general (at k = 3), Theorem `thm:random-column` cannot be run at the terminal with
   any u < 2k−1. Class 2b−1 also occurred at b = 4, in a seeded random algebra. *Exact
   computation*; the identities are proved below. The appendix itself only uses 2b−1, so
   nothing downstream changes.
2. **The unwinding formula in the proof of `cor:codim` (main.tex) needs a linear section.** The
   sketch allows "any section σ ..., even a nonlinear one" and then unwinds with
   h = σ(h/K) + K. That formula is false for a nonlinear σ, since σ(h/K) need not be a subspace.
   The appendix gets this right: it transports through any τ but runs and unwinds with the
   linear σ. Fix in §5.
3. The Heisenberg no-splitting remark skips one step: why a normal subgroup of order p² must
   contain the centre. It is true, and I checked it exhaustively for p = 3, 5, 7. Fix in §5.
4. The parenthetical "or a promise on codim h as in Corollary `cor:codim`" in
   `thm:random-column` reads as if the codimension promise alone gave the hypotheses. It
   bounds only a_d. The hypothesis c ≤ u holds only at the terminal of the reduction. Fix in §5.
5. The birthday branch cites `thm:uniform-compilation`(i), which is stated for the stage
   quotients G_d of the cover, for a BCH product on 𝓛 itself. The same recurrence applies to 𝓛
   verbatim, so this is a citation fix only. Fix in §5.

## 1. Scripts and reproduction

All scripts are in `research/audits/reviews/2026-11-03-rees-check-app-e/`. They import nothing
from the repository except the folder's own `lie_fp.py`, and they use exact arithmetic mod p
unless a check is marked "float". Interpreter: `/opt/anaconda3/bin/python`. Each script was run
niced on a loaded machine, and the wall times below are from that machine.

| Script | Checks | Output | Wall |
|---|---|---|---|
| `lie_fp.py` | library: F_p linear algebra, Lie algebras from structure constants, the construction of Lemma `lem:app-codim-ideal` with random admissible choices, normalizer, quotient with a random complement, random nilpotent algebras built by iterated central extensions by random 2-cocycles | — | — |
| `ideal_bounds.py` | Lemmas `lem:app-codim-ideal` and `lem:app-codim-selfcentral` and Prop `prop:app-codim-size` on 981 algebras (4,010 construction runs): filiform m ≤ 9, n_N for N ≤ 5, random central extensions of dim ≤ 9 at p = 3, 5, 7, random subalgebras of n_4 and n_5. Also the two hand examples of §2.3 | `ideal_bounds_out.txt` | 25 s |
| `filiform_e.py` | Prop `prop:app-codim-filiform`(iii) and the subalgebra remark, m = 4..10, p ∈ {5, 7, 11, 13}, 20 random construction runs each | `filiform_e_out.txt` | 3 s |
| `reduction_lie.py` | (R1)–(R4), Props `prop:app-codim-complete`(i)–(iv), Lemmas `lem:app-codim-normalizer`, `lem:app-codim-unwind` and `lem:app-codim-ad` at the Lie level. **All** subalgebras of codimension ≤ 3 (≤ 2 or ≤ 1 for the larger p = 5 cases) of Heis₃, Heis₅, filiform 4/5/6, the two hand examples and n_4, over F_3 and F_5, found by enumerating every subspace; plus random (𝔤, 𝔥) at p = 3, 5, 7. 6,209 pairs, each run with k = codim + 0, 1, 2 (18,627 runs) | `reduction_lie_out.txt` | ≈ 25 min |
| `reduction_group.py` | The same steps at the group level, using the oracle alone: BCH of class ≤ 4 (associativity checked), p = 5, 7; coset-labelling oracles; the restricted oracle's fibres; the exact Fourier law (float, b ≤ 4); transport through 57 sections that are neither linear nor homomorphic (11,051 parent queries); recovery after unwinding; the birthday uniformity step for 107 nonnormal H; the Heisenberg remark for p = 3, 5, 7 | `reduction_group_out.txt` | ≈ 4 min |
| `bounds_check.py` | the spanning bound p^{r−t}, the birthday batch inequalities (exact rationals), the small-prime bound log₂B ≤ k(3+log₂k)+2 for k ≤ 300, the error-budget arithmetic | `bounds_check_out.txt` | 20 s |

```bash
cd research/audits/reviews/2026-11-03-rees-check-app-e && /opt/anaconda3/bin/python ideal_bounds.py
```
```bash
cd research/audits/reviews/2026-11-03-rees-check-app-e && /opt/anaconda3/bin/python reduction_lie.py
```
```bash
cd research/audits/reviews/2026-11-03-rees-check-app-e && /opt/anaconda3/bin/python reduction_group.py
```
```bash
cd research/audits/reviews/2026-11-03-rees-check-app-e && /opt/anaconda3/bin/python bounds_check.py && /opt/anaconda3/bin/python filiform_e.py
```

Headline numbers. There were 0 failures in every script, and every recovery returned 𝔥.
Lie-level end states: 370 at (R1), 6,741 at (R2) and 11,516 nonabelian terminals. The largest
terminals by k, as (dim, class):

| k | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| (dim, class) | (3, 2) | **(6, 5)** | (9, 6) | (9, 7) | (9, 8) | (9, 8) |

The largest Σ_d a_d at a terminal was 5 at k = 3 and 7 at k = 4. So the total really does
exceed k, as the text after Lemma `lem:app-codim-ad` says, and only the per-grade bound holds.
The largest class seen for each b was {1: 1, 2: 2, 3: 5, 4: 7, 5: 8, 6: 8}, against the bound
2b−1. These finite checks can only falsify; the verdicts rest on the proofs (TRAPS 7).

## 2. Per-statement verdicts

The labels are: **proved**, meaning I checked the written proof line by line; **exact**, an
exact computation; and **float**, a floating-point check. "Smallest counterexample: none"
means that none exists, because the statement is proved; the entry then gives the sharpest
instance I found.

### 2.1 Statement and Lazard facts

**Thm `thm:app-codim` (i)–(iii): holds** (proved, conditional exactly as stated). Assembly
checked in §2.6. There is no counterexample. The sharp instances are the filiform family for
the direct descent and the six-dimensional algebra of §2.3 at k = 3.

**Lemma `lem:app-codim-lazard` (a)–(d): holds** (proved; (d) is cited Lazard). On (c), the
truncation degree on the two sides may differ. Truncation at any N ≥ class gives the same
value, and φ(𝔤) has class ≤ c′, so the two products agree. The proof says this. BCH
associativity and inverses were checked exactly on every group of `reduction_group.py`.

### 2.2 Filiform example

**Prop `prop:app-codim-filiform` (i): holds** (proved by hand; exact for m = 4..10). Jacobi on
basis triples and γ_d = Span(e_d, …, e_{m−1}) are correct.

**(ii): holds** (proved). a_d = 1 for d = 2..m−1, grade one adds 2, and the total is m. With
M_d = 1 the single label is uniform on a line, and s^dλ = 0 with s ≠ 0 forces λ = 0, which has
probability 1/p. The conclusion ∏M_d ≥ 2^{m−2} is about the descent only, and the text says so.

**(iii): holds** (proved by hand; exact, 28 (m, p) cases × 20 random runs). The induction
I_j = Span(e_{m−j}, …, e_{m−1}) is right, including the boundary case j = m−2, where the
constraint [y, e_2] = αe_3 needs m ≥ 4. N(𝔥) = 𝓘 and 𝓘/𝔥 ≅ F_p. Two abelian calls are made:
one on exp 𝓘, which returns 𝔨 = 𝔥, and one on the remainder. `rem:codim` now reads "one
abelian call on exp 𝓘, leaving a one-dimensional abelian remainder", which is accurate. The
integrator note in the appendix's header comment (lines 31–33) is therefore stale.

### 2.3 The abelian ideal

**Lemma `lem:app-codim-ideal`: holds** (proved; exact on 4,010 runs). V_j is cut out by
O(n²) linear conditions and contains 𝓘_j. Adjoining any x ∈ V_j \ 𝓘_j keeps the space abelian
and an ideal, and the flag property is the defining condition. A deterministic choice (a basis
vector of V_j outside 𝓘_j) gives poly(n, log p). For 𝔤 ≠ 0, V_0 = Z(𝔤) ≠ 0, so b ≥ 1.

**Lemma `lem:app-codim-selfcentral`: holds** (proved; exact, 4,010/4,010). C = C_𝔤(𝓘) is an
ideal by the derivation identity. Take the last index i with [𝔤, …, [𝔤, C]] ⊄ 𝓘; any x in that
term outside 𝓘 lies in V at termination, which is a contradiction. Corollary, not stated in the
text: self-centralizing implies maximal among abelian ideals, because an abelian ideal
J ⊋ 𝓘 would lie in C(𝓘) = 𝓘. So the word "maximal" in the `cor:codim` sketch is correct.

**Prop `prop:app-codim-size`: holds, and both bounds are sharp at b = 3** (proved; exact).
The map ρ is faithful on 𝔤/𝓘 and lands in 𝔫_b in the flag basis; γ_b(𝔫_b) = 0, so
γ_b(𝔤) ⊆ 𝓘_b and γ_{b+j}(𝔤) ⊆ 𝓘_{b−j}, which gives γ_{2b} = 0.

- **The sentence after the proposition fails.** "We do not know whether class at most b always
  holds" has this answer. Take 𝔤₅ with basis e₁..e₅, [e₁,e_i] = e_{i+1} (i = 2, 3, 4),
  [e₂,e₃] = e₅, and all other brackets of basis vectors zero. Jacobi at (e₁,e₂,e₃) forces
  [e₂,e₄] = 0, and that holds. Every run of the construction returns
  𝓘 = Span(e₃, e₄, e₅). By hand: Z = F_p e₅, then ζ₂ ∩ C(e₅) = Span(e₄, e₅), then
  Span(e₃, e₄, e₅). C(𝓘) = 𝓘 because [ae₁ + be₂, e₃] = ae₄ + be₅. So b = 3 while the class
  is 4. This is the **smallest** instance found: no algebra of dimension ≤ 4 can have
  class > b, since dim ≤ 4 with b ≤ 2 gives dim ≤ 3 and class ≤ 2.
- **Both bounds attained.** Take 𝔤₆ with basis e₁..e₆, [e₁,e_i] = e_{i+1} (2 ≤ i ≤ 5),
  [e₂,e₃] = e₅, [e₂,e₄] = e₆, [e₂,e₅] = −e₆, [e₃,e₄] = e₆, and all other brackets of basis
  vectors zero. Jacobi holds over ℤ; it was checked exactly at p = 3, 5, 7, 11 and 10007, and
  the Jacobi sums are integers of absolute value at most 3. The algebra is filiform of class 5.
  Every run of the construction returns 𝓘 = Span(e₄, e₅, e₆). By hand,
  [y, e₄] = y₁e₅ + (y₂ + y₃)e₆ and [y, e₅] = (y₁ − y₂)e₆, so C(𝓘) = 𝓘. Hence b = 3,
  dim = 6 = b(b+1)/2 and class = 5 = 2b−1.
- Consequence for the reduction. Every subalgebra of 𝔤₆ of codimension ≤ 3 (103 of
  codimension exactly 3 over F_3) gives, at k = 3, an immediate terminal with b = 3 ≤ k and
  class 5 = 2k−1. So Prop `prop:app-codim-complete`(iii) is attained at k = 3, and
  `reduction_lie.py` found exactly this (6, 5) terminal. With p > 5, Theorem
  `thm:random-column` needs u ≥ c_J = 5 = 2k−1 there. The paper's u = 2k is fine, and the
  remark that u = 2k−1 also works is the best possible in general (at k = 3).

**Remark "an abelian subalgebra cannot replace the ideal": holds** (exact, m = 4..10).
Span(x, e_{m−1}) is abelian, self-centralizing and not an ideal.

### 2.4 Learning the intersection

**Lemma `lem:app-codim-restrict`: holds** (proved; exact on every R4 step of
`reduction_group.py`, where the fibres of F = f∘ι are exactly the cosets of W, and W read from
the oracle equals ι^{-1}(𝔥 ∩ 𝓘)). dim 𝔨 ≥ b − k uses only codim 𝔥 ≤ k. The oracle F needs no
group product on 𝓘, because 𝓘 is abelian.

**Lemma `lem:app-codim-sample`: holds** (proved; float check of the exact Fourier law in 38
cases, uniform on W^⊥ to 10⁻⁹; exact rational check of the spanning bound in 420 cases).
Acceptance holds iff Ŵ = W, because the exact classical basis test enforces Ŵ ⊆ W, and Ŵ ⊇ W
holds whenever the samples lie in W^⊥. Smallest instance where the dimension test matters: none
in the ideal process. The text says so, and it is needed only after an approximation error.

**Remark on the incomplete intersection: holds** (proved by hand). The subspace
B = Span(e₂, …, e_{m−2}) of dimension b − k passes every membership test and is not normalized
by x ∈ 𝔥. It shows why the whole of 𝔥 ∩ 𝓘 must be learned.

### 2.5 Normalizer, transport, unwinding, reduction

**Lemma `lem:app-codim-normalizer`: holds** (proved; exact, every R4 step). The key line is
[𝔥, 𝔨] ⊆ 𝔥 ∩ 𝓘, using that 𝔥 is a subalgebra and 𝓘 an ideal. The codimension identity
codim_{𝔰/𝔨}(𝔥/𝔨) = dim 𝔰 − dim 𝔥 is correct.

**Lemma `lem:app-codim-transport`: holds for every section τ** (proved; exact, 57 nonlinear,
non-homomorphic sections, each fibre equal to a left coset q₀∗π(H) computed with the BCH
product of 𝔰/𝔨). The step 𝔥 = π^{-1}(π(𝔥)) uses 𝔨 ⊆ 𝔥.

**Heisenberg remark: holds, but one step is unstated** (exact: no 2-dimensional subalgebra of
Heis(F_p) misses the centre, for p = 3, 5, 7). "is normal, and so contains the centre" needs
this: a nontrivial normal subgroup of a p-group meets the centre nontrivially, and here
|Z| = p. Fix in §5.

**Lemma `lem:app-codim-unwind`: holds** (proved; exact, 18,627 + 280 recoveries). It needs σ
linear, which the appendix uses. **The `cor:codim` sketch in main.tex does not say this**
(§0, item 2).

**Reduction (R1)–(R4) and Prop `prop:app-codim-complete` (i)–(iv): hold** (proved; exact, 0
violations).
- (i): the codimension decreases by exactly dim 𝓛_j − dim 𝔰_j, so k_{j+1} ≥ codim 𝔥_{j+1}.
- (ii): each R4 step drops the dimension by ≥ 1, which gives ≤ m levels and ≤ m calls.
- (iii): b_J ≤ k, so the dimension is ≤ k(k+1)/2 and the class is ≤ min(2k−1, c). For k ≤ 1
  the dimension is ≤ 1, so the terminal is abelian. For k = 2, a nonabelian nilpotent algebra
  of dim ≤ 3 is Heisenberg, with class 2. Exhaustive over all subalgebras of codim ≤ 3 (≤ 2 or ≤ 1 in the larger
  p = 5 cases) of the listed algebras: no nonabelian terminal at k ≤ 1, and every k = 2 terminal was (3, 2).
- (iv): proved.

**Recursion cost: holds** (proved). There are ≤ m levels. Each level needs one construction
(≤ n null spaces of O(n²) × n systems), a normalizer (≤ n² rows), and structure constants
(q² brackets). One f query plus a stored m × dim 𝓛_j matrix per transported query. Queries per
level: T + (b + 1). No BCH product is evaluated anywhere in the reduction; only linear maps and
abelian Fourier sampling are used. This is worth stating, because it makes Part (iii) for k ≤ 1
independent of the BCH compiler.

### 2.6 Terminal solvers and assembly

**Lemma `lem:app-codim-ad`: holds** (proved; exact, every terminal). The isomorphism
γ_d/(𝔥 ∩ γ_d) ≅ (γ_d + 𝔥)/𝔥 gives a_d ≤ codim 𝔥_J ≤ k. Σ a_d > k happens (5 at k = 3), so
the "only per grade" caution is necessary.

**Prop `prop:app-codim-rc`: holds, conditional on `thm:random-column`** (proved as an
application). The hypotheses are u = 2k ≥ 2, c_J ≤ 2k−1 ≤ u, a_d ≤ k ≤ u−1 and
p ≥ 64k² = 16u². κ_d ≤ d ≤ 2k−1 < p−1, so the case d = p−1 cannot arise. The costs are
(8k)^{2k−2} leaves per tree, κ^M ≤ (2k)^{8k} trials per node, and terminal dimension
≤ k(k+1)/2, all 2^{O(k log(k+2))}. The u = 2k−1 remark is correct, and by §2.3 it is the least
admissible u in general (at k = 3).

**Prop `prop:app-codim-birthday`: holds** (proved; exact rationals). The checks:
- B(B−1) > 2I for I ≤ 3000 and for selected prime powers.
- The no-repeat probability is < 1/2 for all J ≤ I < 400, and at J = I for the others.
- For every coset gH of 107 nonnormal subgroups, the multiset {x^{-1}∗y : x, y ∈ gH} covers H
  exactly |H| times each. This is the conditional-uniformity step.
- log₂B ≤ k(3 + log₂k) + 2 for k ≤ 300 at the largest prime < 64k², with
  max log₂B/(k log₂(k+2)) = 2.335.

One citation fix (§0, item 5): the BCH evaluation on 𝓛 is the recurrence of
`thm:uniform-compilation`(i) applied to 𝓛 itself, at poly(m, c) brackets.

**Error budget and proof of Thm `thm:app-codim`: hold** (proved; exact arithmetic for
m < 60 and four values of ε).
- m · 2^{m−T} ≤ ε/4 and 2mN_sη = ε/4.
- The budget ε/4 + ε/4 + ε/2 is assembled correctly by `lem:hybrid`.
- The "caps on every branch" argument is right. The dimension test forces dim 𝔨̂ ≥ 1 even after
  an approximation error. 𝔨̂ ⊆ 𝓘 is abelian, so N(𝔨̂)/𝔨̂ is again a nilpotent Lie algebra of
  class < p, and the terminal solver always receives a well-formed algebra.

Part-by-part:
- Part (i): `thm:main` is applied at each class c′ ≤ 2k−1, finitely many.
- Part (ii): the branch on p ≷ 64k² uses public data.
- Part (iii): k ≤ 1 uses only abelian sampling; k = 2 uses `thm:main` at c = 2.

### 2.7 main.tex: `cor:codim` and `rem:codim`

**`cor:codim` (i), (ii): hold**, with the appendix as proof.
- The statement of (i) does not repeat "conditional on Theorem `thm:main`", although the title
  says "conditional". Suggested in §5; optional.
- The proof sketch has the unwinding error of §0 item 2, and it uses the letter a for dim 𝓘,
  which clashes with a_d.
- (ii)'s query count poly(m, w, log(1/ε)) is weaker than the appendix's poly(m, log(1/ε)), and
  it is consistent with it.

**`rem:codim`: holds** (proved; exact). It is accurate as written, including "leaving a
one-dimensional abelian remainder".

## 3. Small k, explicitly

| k | What happens | Status |
|---|---|---|
| 0 | 𝔥 = 𝓛, no query | proved |
| 1 | The reduction ends at (R1) or (R2) for every p > c. Smallest run that needs two abelian calls: Heis₃ with 𝔥 = Span(x, z), where every choice gives b = 2 > k, one call on exp 𝓘 and one on an abelian remainder. No BCH evaluation, no Rees step | proved; exact (exhaustive codim ≤ 1 and the slack runs) |
| 2 | Every nonabelian terminal is the Heisenberg algebra (dim 3, class 2), and `thm:main` at c = 2 solves it for every p > 2 | proved; exact (all k = 2 terminals were (3, 2)) |
| 3 | Terminal class up to 5 = 2k−1 occurs (𝔤₆, any 𝔥 of codim ≤ 3) | exact + proved |

## 4. Comparison with the 11-02 review (read after §§1–3)

- **Agreement.** The 11-02 review and I reach the same verdict on every step (R1–R4, S6,
  S6′). It was also unable to break the bound.
- **New here.**
  - The 11-02 review lists "a proof of class ≤ a for self-centralizing abelian ideals" as open
    and optional (§9). The statement is **false**: 𝔤₅ has class 4 > 3 = b, and 𝔤₆ has class 5
    = 2b−1. The improvement in constants it hoped for therefore does not exist in general.
  - It records (6, 3) as the extremal terminal at k = 3. The extremal one is (6, 5).
  - Its proposed proof text, now in main.tex, contains the nonlinear-section/unwinding mismatch
    (§0 item 2). The appendix, written later, already avoids it.
- **Differences of method.**
  - My Lie-level check is exhaustive over every subalgebra of codim ≤ 3 (or ≤ 2) of 16 named
    algebras over F_3 and F_5; the 11-02 check used random subalgebras of n_N at p ≥ 7.
  - My random algebras come from iterated central extensions by random cocycles, a family that
    reaches every nilpotent algebra in principle. This is how class 2b−1 showed up at b = 3, 4.
    Subalgebras of n_N reach it less easily.
  - My group check is smaller (280 instances against their 400 groups) but adds the exact
    Fourier law and the birthday uniformity.

## 5. Exact statement, what is missing, gates, proposed paper text

**Exact statement that now holds** (AI-checked, pending human review). Theorem `thm:app-codim`
as printed, with the same hypotheses: an ordinary coherent left-coset oracle, k given, c < p,
the class not fixed. Its conditions are unchanged: (i) on `thm:main`; (ii) on
`thm:random-column` and the Rees composition; (iii) unconditional for k ≤ 1; for k = 2 only on
`thm:main`. The supporting bounds hold as stated. Two of them are now known to be sharp at
k = b = 3: dim 𝓛_J ≤ k(k+1)/2 and c_J ≤ 2k−1.

**Still missing.**
- Human review.
- An independent check of `thm:random-column` (Appendix B, item 2 of this round), on which
  Part (ii) rests.
- A priority assessment of the composite, which neither review did.

**Claim gates that must stay false** (I read them, and every one is false now):
- `research/reductions/codimension_hybrid_budget.json`: `proof_promotion`,
  `candidate_promotion`, `quantum_receiver_implemented`, `native_application_established`,
  `speedup_claim_allowed`, `hidden_intersection_completeness_certified`, `solver_implemented`,
  `novelty_established`, `growing_class_pointwise_correctness_certified`.
- `research/reductions/random_column_rees.json`: `whole_rees_correctness_certified`,
  `joint_source_law_verified`, `fixed_bank_success_guaranteed`,
  `intrinsic_rank_promise_verified`, `quantum_receiver_implemented`, `novelty_established`,
  `speedup_claim_allowed`.
- `research/reductions/rees_hsp_reduction.json`: `independent_review`, `novelty_established`,
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`,
  `formal_compiler_checked`.
- Note: `normalizer_recursion_required` in `rees_hsp_reduction.json` takes both the value true
  and the value false in different entries. It is not a gate for this item; I changed nothing,
  and Codex may want to look.

### Proposed paper text

Status label for all items: *AI-checked, pending human review.* The target is named in each
item. Only the integrator applies them.

**P1** (needed; `appendix-codimension.tex`, the paragraph after Prop `prop:app-codim-size`).
Replace the paragraph "The dimension bound is attained ... only $2b-1$ is used." with:

```latex
Both bounds are attained at $b = 3$, by a single algebra. Let $\mathfrak{g}_6$ have basis $e_1,\dots,e_6$ with $[e_1,e_i] = e_{i+1}$ for $2 \le i \le 5$, $[e_2,e_3] = e_5$, $[e_2,e_4] = e_6$, $[e_2,e_5] = -e_6$, $[e_3,e_4] = e_6$, and all other brackets of basis vectors zero up to antisymmetry. The Jacobi identity holds over $\mathbb{Z}$, the algebra is filiform of class $5$, and every run of Lemma~\ref{lem:app-codim-ideal} returns $\mathcal{I} = \Span(e_4,e_5,e_6)$: for $y = \sum_i y_ie_i$ one has $[y,e_4] = y_1e_5 + (y_2+y_3)e_6$ and $[y,e_5] = (y_1-y_2)e_6$, so $C_{\mathfrak{g}_6}(\mathcal{I}) = \mathcal{I}$. Thus $b = 3$, $\dim\mathfrak{g}_6 = 6 = b(b+1)/2$ and the class is $5 = 2b-1$. In particular the class can exceed $b$; five dimensions is the least in which this can happen (in dimension at most four, $\dim \le b(b+1)/2$ forces $b \ge \dim - 1$, which is at least the class), and it does happen there: the algebra with $[e_1,e_i] = e_{i+1}$ for $2 \le i \le 4$ and $[e_2,e_3] = e_5$ has $\mathcal{I} = \Span(e_3,e_4,e_5)$ and class $4 > b = 3$. Every subalgebra $\hh$ of $\mathfrak{g}_6$ of codimension at most three gives, at $k = 3$ and $p > 5$, a terminal instance of class $5 = 2k-1$, so the bound $c_J \le 2k-1$ of Proposition~\ref{prop:app-codim-complete}(iii) is attained, and Theorem~\ref{thm:random-column} cannot be applied to all terminals at $k = 3$ with $u < 2k-1$. (Exact checks: Section~\ref{app:codim-checks}.)
```

**P2** (needed; `main.tex`, proof of `cor:codim`). Replace
`and for any section $\sigma$ of $S \to S/K$, even a nonlinear one, $f \circ \exp \circ \sigma$ hides $\exp(\hh/K)$ in $\exp(S/K)$ at one query per query.`
with
`and for any section $\tau$ of $S \to S/K$, even a nonlinear one, $f \circ \exp \circ \tau$ hides $\exp(\hh/K)$ in $\exp(S/K)$ at one query per query; the algorithm uses a linear section $\sigma$.`
Then replace `Unwind with $\hh = \sigma(\hh/K) + K$.` with
`Unwind with $\hh = \sigma(\hh/K) + K$, which uses that $\sigma$ is linear and $K \subseteq \hh$.`
In the same proof, replace `with $a = \dim\mathcal{I}$ this gives $\dim\mathcal{L} \le a(a+1)/2$ and class at most $2a-1$. If $a > k$,` with
`with $b = \dim\mathcal{I}$ this gives $\dim\mathcal{L} \le b(b+1)/2$ and class at most $2b-1$, both attained at $b = 3$. If $b > k$,`

**P3** (recommended; `appendix-codimension.tex`, the remark after Lemma
`lem:app-codim-transport`). Replace
`but every subgroup of order $p^2$ has index $p$, is normal, and so contains the centre.`
with
`but every subgroup of order $p^2$ has index $p$, so it is normal, and a nontrivial normal subgroup of a $p$-group meets the centre nontrivially; since $|Z(\Heis(\Fp))| = p$, it contains the centre.`

**P4** (recommended; `main.tex`, the statement of `thm:random-column`). Replace
`(for example $g_d \le u-1$, or a promise on $\codim\hh$ as in Corollary~\ref{cor:codim})`
with
`(for example $g_d \le u-1$, or, at the terminal of the reduction of Corollary~\ref{cor:codim}, a promise on $\codim\hh$; on its own such a promise bounds $a_d$ but not $c$)`

**P5** (recommended; `appendix-codimension.tex`, proof of Prop `prop:app-codim-birthday`,
"Sampling and cost"). Replace
`by the BCH evaluation of Theorem~\ref{thm:uniform-compilation}`
with
`by the recurrence of Theorem~\ref{thm:uniform-compilation}(i) applied to $\mathcal{L}$ itself, a nilpotent algebra of class $c$, which uses $(c-1)c(c+1)(c+2)/6$ brackets and divides only by integers at most $c$,`

**P6** (optional; `appendix-codimension.tex`, end of Prop `prop:app-codim-complete`'s
proof). Add:
`No step of the reduction evaluates the BCH product: it uses only linear maps, the oracle and abelian Fourier sampling.`

**P7** (optional; `main.tex`, `cor:codim`(i)). Replace
`\item For each fixed $k$, the HSP` with
`\item Conditional on Theorem~\ref{thm:main}: for each fixed $k$, the HSP`

**P8** (optional, housekeeping; `appendix-codimension.tex`). Delete header comment lines
31–33 ("Note for the integrator: Remark rem:codim says ... in one abelian call"), because
`rem:codim` already reads "leaving a one-dimensional abelian remainder". In
§`app:codim-checks`, after "These checks can only falsify;", optionally add
`an independent check (\file{research/audits/reviews/2026-11-03-rees-check-app-e.md}) enumerated every subalgebra of codimension at most three of sixteen small algebras over $\mathbb{F}_3$ and $\mathbb{F}_5$ and found the extremal terminal $(\dim,\text{class}) = (6,5)$ at $k = 3$;`
