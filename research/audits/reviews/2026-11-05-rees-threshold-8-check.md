# Threshold-8: independent adversarial check and integration

5 November 2026 (overnight pass). AI-only check, not a human review, not a Lean proof, not a
priority claim. **"AI-checked, pending human review" applies to everything below.**

Object: `2026-11-05-rees-threshold-8.md` (§2 proofs, §3 computations, §4 heuristic, §6 proposed
text, §9 its own checker) and the folder `2026-11-05-rees-threshold-8/`. Own code and outputs:
`2026-11-05-rees-threshold-8-check/` (interpreter `/opt/anaconda3/bin/python`; every run under
`nice -n 10`, at most two processes, each under 30 min and well under 1 GB). No code is shared
with dfs2b, rcdfs.c, the threshold-8 folder or its `check/` subfolder.

## 0. Verdict

**No Error.** One Gap and six Imprecisions, all fixed in the integrated text.

- **Gap G1 (duplication, weaker than known).** Lemma 5 (E_2(D) ⊆ E_2(κ) on p ≡ 1 mod κ for
  D | κ with gcd(D, κ/D) = 1) is correct, but it is the coprime special case of Consequence 1
  of threshold-7 Proposition 4.6 (E_2(κ) ⊆ E_2(D') for κ | D', no gcd condition). The report's
  "Check. The case gcd > 1 is not covered" is true only of its own map j ↦ (κ/D)j. The plain
  restriction to the indices 0..D−1 with the same ξ works for every divisor (§1.4). The paper
  now states the general lemma with that three-line proof and credits threshold-7 Prop. 4.6;
  the coprime hypothesis is dropped everywhere (appendix and main.tex).
- **Imprecisions** (fixed in the inserted text):
  - I1. "not explained by two-row obstructions for any κ ≤ 9": E_2(2) = E_2(3) = ∅, so
    4 ≤ κ ≤ 9, and the comparison is with the largest *known* member (κ = 8, 9 are not exact).
  - I2. The scope remark omitted r ≤ κ, p ≡ 1 (mod κ) and the column version of Prop. 6.
  - I3. "two separately written programs" for the E2row lists, 3 ≤ κ ≤ 16: in the report
    only κ = 4..9 had two codes (`tworow.py`, `tworow_np.py`) and §9's checker went to κ = 12.
    Now true: own `cyclo_check.py` reproduces every list for κ = 3..16 (§2.1).
  - I4. The proposed status line dropped what the report itself says: lower bounds only,
    square gap not narrowed, two-row argument "likely classical", no priority. Added.
  - I5. §6.2's "for fixed r they cannot reach the square gap" mixes a threshold gap with
    certificates. Now: r-row obstructions are void above ((r−1)κ^r+2)², so for fixed r they
    cannot certify primes near κ^{(κ+1)/2} once κ is large; the square gap stays open.
  - I6. Prop. 3(iii) in LaTeX gave only the inequality. The explicit range p ≥
    ((κ−1)(κ−2)+2)² for κ ≥ 4 (report §2.2, stated as a fact about W_2) now has its two-line
    proof in the text.
- Proofs re-derived line by line (§1): Lemma 0, Theorem 2, Corollary 3(1)–(3) including |𝒫|,
  the pigeonhole bound and the Weil expansion, Lemma 5 and the general projection, Prop. 6,
  Theorem 1 (not integrated).
- Computations (§2): own cyclotomic code (κ = 3..16, two generators, direct difference-set
  test); own complete E_2 solver (Python + C port, agreeing) reproducing every exact list in
  the paper for κ = 4..7 and the κ = 8, 9 counts below 2442 / 3584; independent exact E_2 for
  κ = 10 and 12 (κ = 10 every prime ≤ 8191, κ = 12 every prime ≤ 10453, 0 disagreements with dfs2b on 565 primes); divisor inclusion on all witnesses.
- Heuristic §4: labelled [conjecture] throughout; `heuristic2.py` has no fitted parameter.
  Not proposed for and not inserted into the paper.

## 1. Proofs re-derived

### 1.1 Lemma 0, Theorem 2 (two rows)

Correct. Lemma 0: β_i = β_k forces α_j = −β_i for all j (cell in Q°_{−(i+j)} ∩ Q°_{−(k+j)}
= {0}), then the row-0 value β_0 − β_i lies in every Q°_{−j}, hence 0, against α_0 + β_0 ≠ 0.
Theorem 2: d = β_i − β_k ∈ ξ^{−j}(Q°_{−i} − Q°_{−k}) for every j, using
Q°_{m−j} = ξ^{−j}Q°_m; the set S is Q_0-stable, so S ⊇ ⋃_j ξ^j dQ_0 = F_p^×. Uses all κ
columns and two rows; the column version uses α_j − α_l.

### 1.2 Corollary 3 (cyclotomic criterion)

- (1) The three representations of z ∈ Q_c as x − y (x = 0 iff c = b − ε; y = 0 iff c = 0;
  x = zw, y = z(w−1) iff A(−c, b−c) ≥ 1) are right. The map (b, c) ↦ (−c, b−c) is a bijection
  {b ≠ 0} → {u ≠ v}, with c ≠ 0 ⟺ u ≠ 0 and c ≠ b − ε ⟺ v ≠ ε (since b − ε = v − u − ε and
  c = −u). The step to rows: Q°_0 − Q°_b ⊉ F_p^× times ξ^{−i} is Q°_{−i} − Q°_{−(i−b)}, i.e.
  rows i and i − b. Independent of ξ.
- (2) Σ_{u,v} A = p − 2. The three lines u = 0, v = ε, u = v meet in (0, ε), (0, 0), (ε, ε):
  one point if ε = 0 (union 3κ − 2), three otherwise (union 3κ − 3). So |𝒫| = (κ−1)(κ−2) or
  κ² − 3κ + 3, and all A ≥ 1 on 𝒫 forces p ≥ (κ−1)(κ−2) + 2 = κ² − 3κ + 4.
- (3) K′(s,0) = −1, K′(0,t) = −χ^t(−1), K′(s,−s) = −1 (w ↦ w/(w−1) permutes F_p∖{0,1}),
  |K′| ≤ √p on the (κ−1)(κ−2) generic pairs (f = X^s(X−1)^t, two roots, exponents in
  [1, κ−1], so not a κ-th power; same input as `lem:app-s2-cyclo`). Boundary total ≤ 3(κ−1).
  The added range claim: with c = (κ−1)(κ−2) and √p ≥ c + 2, p − c√p ≥ 2c + 4 > 3(κ−1) + 2
  iff (κ−1)(2κ−7) + 2 > 0, true for κ ≥ 4 and false (= 0) at κ = 3, matching W_2(3) = 17 > 16.
- Small κ by own code (§2.1): every prime p ≡ 1 (mod κ), p ≤ κ² − 3κ + 3, κ = 3..16, has a
  zero on 𝒫, and the solver of §2.2 puts each of them in E_2(κ).

### 1.3 Remark (exactness), Lemma 4

Correct (not integrated). Rows {0, b} with β_0 = 0, β_b = −d: column j needs
d ∈ ξ^{−j}S_{−b}; column 0 with α_0 = d ≠ 0 when d ∈ Q_0. Lemma 4 is the h = 1 case.

### 1.4 Lemma 5 versus threshold-7 Proposition 4.6 (Gap G1)

Lemma 5's proof is correct: ξ^{m(p−1)/D} = ζ^{m²} has order κ/gcd(κ, m²) = mD/(m·gcd(D, m))
= D; x ∈ Q_e lies in ξ^{mt}P_D iff mt ≡ e (mod D); the cell index −m(i′+j′) gives
t ≡ −(i′+j′). But the hypothesis gcd(D, κ/D) = 1 is not needed for the inclusion:

> Restrict a contraction at (p, κ) for ξ to 0 ≤ i, j < D. ξ is a coset generator for D
> (ξ^{(p−1)/D} = ζ^{κ/D} has order D; the appendix says this at the start of `app:s2-tower`),
> and Q_m ⊆ ξ^m P_D = Q^{(D)}_{m mod D}. So α_j + β_i ∈ Q^{(D)}_{−(i+j)} ∪ {0} and
> α_0 + β_0 ≠ 0: a contraction at (p, D) for ξ.

This is threshold-7 Prop. 4.6, Consequence 1 (R = Z_{D'}, K = {0}), proved there and
checked in `2026-11-05-rees-threshold-7-check.md`, but not yet in the paper. So the integrated
lemma is the general one, with the threshold-7 credit; nothing of Lemma 5 is lost.
Consequences corrected: §5 "max E_2(κ) ≥ max E_2(D) for coprime-cofactor divisors" holds for
every divisor D whose maximal member is ≡ 1 (mod κ) (the report's example 18181 ≡ 1 mod 18 is
unaffected). Tested on witnesses, including non-coprime pairs (§2.3).

### 1.5 Proposition 6 (locality barrier)

Correct. β_i = ξ^{−i} − 1 (i ∈ R), α_0 = 1 give column 0 the values ξ^{−i} ∈ Q_{−i}; roots
1 − ξ^{−i} distinct; `lem:app-s2-weil-count` with ℓ = r ≤ κ gives
κ^r|X_j| ≥ p − r − κ^r − (r−1)κ^r√p; with s = √p ≥ (r−1)κ^r + 2,
s² − (r−1)κ^r s ≥ 2s ≥ 2(r−1)κ^r + 4 > κ^r + r. Needs r ≤ κ (for E_κ(ℓ,p) ≤ (ℓ−1)√p + 1)
and p ≡ 1 (mod κ); R need not contain 0. Columns by the i ↔ j symmetry of the cell rule.

### 1.6 Theorem 1 (zero cells; not integrated)

Correct as written. f(i) − f(k) ≡ ε for all ordered pairs, swap gives 2ε ≡ 0, three
distinct indices (κ ≥ 3) give ε ≡ 0; f ≡ c ≠ 0; (3) the y_m computation checks
(numerator and denominator both in Q_{−m−m′−c}). The optional main.tex replacement sentence
is not used (one sentence only was allowed).

## 2. Own computations

### 2.1 Cyclotomic criterion (`cyclo_check.py` → `cyclo_check.out`)

From a discrete-log table, for every κ = 3..16 and every prime p ≡ 1 (mod κ) below W_2(κ):
A(u, v) for two coset generators (g and g^{u_0}, same verdict), Σ A = p − 2, |𝒫|, the
deviation bound of Cor. 3(3) on all κ² pairs, pigeonhole zeros, and (p ≤ 1500) a direct
difference-set test Q°_0 − Q°_b ⊇ F_p^× agreeing with the A test. W_2(κ) recomputed (17, 56,
171, 434, 940, 1810, 3188, 5242, 8164, 12170, 17500, 24418, 33212, 44194 for κ = 3..16). Every
E2row list of the report's §3.2 is reproduced exactly; max/κ² ≤ 14.93 (κ = 14, 2927). 10 s.

### 2.2 Exact E_2 (`e2dfs.py`, C port `e2dfs_c.c`)

Normal form β_0 = 0, α_0 = 1; DFS over β_1..β_{κ−1} with exact forward checking (domain of an
unassigned row = values compatible with the current column sets; smallest domain first). A
prime is FEASIBLE iff all column sets stay nonempty; every witness is re-checked on all κ²
cells with modpow. The Python and C versions give identical verdicts and node counts on the 95
primes κ = 10, p ≤ 2671 (`e2dfs_py_k10_partial.out`). Build: `cc -O2 -o e2dfs_c e2dfs_c.c`
(binary not kept); `run_small.sh` reruns κ = 4..9.

| κ | range | own result | reference |
|---|---|---|---|
| 4 | ≤ 997 | {5, 13, 17, 29, 37, 53} | paper, exact (T_A(4) = 869) |
| 5 | ≤ 12721 | {11, 31, 41, 61, 71, 101, 131, 151, 181} | paper, exact |
| 6 | ≤ 1999 | 53 primes, max 859 | paper; list of TH7-check `e2six.out` |
| 7 | ≤ 3389 | 56 primes = Theorem 6 list of threshold-2, max 3221 | paper |
| 8 | ≤ 2441 | 82 of 83, only 1553 feasible | paper: 82 of 83 below 2442 |
| 9 | ≤ 3583 | 82 of 83, only 3529 feasible | paper: 82 of 83 below 3584 |
| 10 | ≤ 8191 (253 primes) | all in E_2 except 3361, 3761, 5821 | dfs2b: 253/253 agree; rcdfs ≤ 3800 |
| 12 | ≤ 10453 (312 primes) | all 312 in E_2 | dfs2b: 312/312 agree; rcdfs ≤ 4000 |

### 2.3 Inclusions (`compare.py` → `compare.out`, `divisor_check.py` → `divisor_check.out`)

- E2row(κ) ⊆ own E_2(κ) on every decided range (κ = 4..10, 12).
- Exact-list inclusions: E_2(4) ∩ {1 mod 8} = {17} ⊆ E_2(8) (gcd(4, 2) = 2, outside Lemma 5,
  inside the general lemma); E_2(4) ∩ {1 mod 12} = {13, 37} ⊆ E_2(12); E_2(6) ∩ {1 mod 12}
  (20 primes, gcd(6, 2) = 2) ⊆ E_2(12); E_2(5) ⊆ E_2(10). The paper's κ ≤ 9 data contain no
  other nontrivial instance (E_2(2) = E_2(3) = ∅, and every feasible κ = 8, 9 prime exceeds
  max E_2(4) and max E_2(3)).
- `divisor_check.py`: all 563 own witnesses (κ = 4..10) re-checked by modpow with a
  separate generator test; each restricted to 0..D−1 for every divisor 2 ≤ D < κ (273
  projections, 77 of them with gcd(D, κ/D) > 1: κ = 4 → 2, 8 → 2, 4, 9 → 3) is a
  D-contraction for the same ξ; the report's map with ξ^{κ/D} also works on all 196 coprime
  cases.
- κ = 10 run stopped at its 30 min cap after 8191 (8221..8311 left to dfs2b alone); the
  sentence in the paper says 8191. Every prime p ≡ 1 (mod κ) up to the last printed one has a
  verdict (gap check in `compare.py`).

### 2.4 Report tables

§3.3 (κ = 10, 12 rows) and §3.5 (f(κ) for κ = 4..10) agree with own data on the own ranges.
§3.2 agrees exactly (§2.1). Not re-checked: κ = 11, 13..16 E_2 ranges (dfs2b + rcdfs only),
§3.1 clique counts, §3.4 statistics (none of these enter the paper).

## 3. Heuristic (§4)

Labelled [conjecture] in §0 and §4; `heuristic2.py` uses Pr[p ∈ E_2] = exp(−μ_G/(2κ²)) with
μ_G = p^{2κ−2}q^{κ²−1}, q = (h+1)/p, orbit size 2κ² from the recentring × transposition
symmetry, and the median-of-tail rule; there is no fitted parameter (the earlier `heuristic.py`
with a fitted c is marked superseded). The sketch p* ≈ κ^{(κ+1)/2}(2κ²L)^{1/(2κ−2)} follows
from μ_G = (p/κ^{(κ+1)/2})^{2κ−2}(1 + (κ−1)/p)^{κ²−1}, re-derived. Modelling choices (orbit
size, independence, median rule) are assumptions, not fits; the report says the model is wrong
per prime below about κ^4 (consistent with f(10) = 3361 being a non-member where the model gives
probability ≈ 1 of membership). Nothing of §4 is in the paper.

## 4. Integration

- `appendix-schedule2.tex`: new subsection `app:s2-local` ("Local obstructions and small
  exceptional primes") after `rem:app-s2-chains-scope`, directly before `app:s2-scope`:
  status line, `lem:app-s2-two-rows`, `prop:app-s2-cyclotomic` (i)–(iii), `lem:app-s2-divisor`
  (general D | κ, threshold-7 credit), `rem:app-s2-local-scope`. Statuses: proved / finite
  computation; "AI-checked, pending human review"; no square-gap claim.
- `main.tex` `rem:two-level-threshold-size`: one sentence before "A sub-family of the
  problem is a coloured-clique question ...".
- Not changed: `tab:app-s2-thresholds`, main tables, `numbers.tex`, claim gates, registry.
- Build (scratch copy in $TMPDIR, `latexmk -g -pdf`): exit 0, 171 pp., 0 Overfull, no
  undefined refs/cites, no "Float too large" (a transient one at main.tex l. 233 seen in a first
  build came from a concurrent edit by another pass and was gone in the final build). Numbers
  test: 2 passed. `make_numbers.py` not run. Nothing committed.
- Concurrency: `main.tex` and `appendix-schedule2.tex` were edited by other passes during this
  check (date line, `Section` → `Appendix`, notation sentence in `app:s2-tower`); the edits were
  applied by exact-string replacement on the current files (each anchor count 1), backups in the
  session scratchpad (`backup/*.pre-edit`).
- `REES_FULL_CONTINUATION.md` item 2: one paragraph added.

## 5. Claim gates that stay false

Threshold of order κ^{(κ+1)/2} proved; square gap closed or narrowed; E_2(κ) known for κ ≥ 8;
max E_2(κ) determined for κ ≥ 8; the §4 model proved; any priority claim (the two-row argument
may be classical; no literature search was possible). `rees_hsp_reduction.json` and registry
gates untouched.

## 6. Next

Next hard question unchanged (report §7): certify one prime in (Cκ^{(κ+1)/2}, κ^κ/2] for one
κ ≥ 8 without enumeration. Cheap next command: `./e2dfs_c 10 8312 12000` in this folder
(about 1 h at current load; expected: members throughout, by the model), re-decided on a
sample by dfs2b.
