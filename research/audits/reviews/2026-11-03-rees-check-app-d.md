# Rees round 4, item 4: unanchored proof check of Appendix D (torsion, black box)

**AI-checked, pending human review.** No human has read this. Nothing here changes the paper,
a registry, a claim gate or `STATE.md`. Campaign row: `research/REES_FULL_CAMPAIGN_4.md`,
item 4.

**Scope.** `docs/papers/rees-hsp/appendix-torsion-blackbox.tex` (875 lines) in full, and the
body statements it proves or feeds: `thm:ring-to-field`, `prop:black-box` and
`thm:bb-envelope` in `main.tex`, plus the parts of `def:input-contract`, `thm:main` and
`cor:fpt-r` that the appendix uses. Not in scope: the core query bound per field call
(`c(m+t)∏M_d ≤ cK_c(m+t)(m+1)^{E_W−1}`, Appendices A/B) and the Imran–Ivanyos paper itself.

**Method.** I read the appendix and the `\ref` targets first and wrote a verdict for every
statement before opening any project report. Then I ran six exact scripts (folder
`2026-11-03-rees-check-app-d/`, Python `/opt/anaconda3/bin/python`, read-only use of
`theorems/universal_lazard_words.py`). Only then did I compare with the three 11-02 reviews
(§5). Labels: **proved** (written argument checked here), **exact** (script), **argued**,
**imported**.

## 0. Verdicts

| # | Statement | Verdict | Smallest counterexample, or fix |
|---|---|---|---|
| 1 | `lem:tb-integral`, (eq:tb-commutator), (eq:tb-conjugation) | **Holds** (proved) | — |
| 2 | `lem:tb-words` | **Holds** (proved) | — |
| 3 | `lem:tb-evaluation` | **Holds** (proved; exact on UT_{c+1}(Z/p^e), 8 cases with c ≤ 6) | M must be a multiple of the exponent: with M = p and e = 2 the words give wrong answers (exact negative control) |
| 4 | `cor:tb-correspondence` (a)–(c) | **Holds** (proved; exact brute force on 5 rings) | — |
| 5 | (M1)–(M3) public arithmetic | **Holds** (proved) | — |
| 6 | `thm:ring-to-field` (i) | **Holds** (proved) | — |
| 7 | `thm:ring-to-field` (ii) | **Holds, conditional on `cor:fpt-r`** | the abelian branch r_loc = 0 has no stated error; one clause (P7) |
| 8 | `lem:tb-quotient-oracle`, `lem:tb-section-rank` | **Holds** (proved; exact) | — |
| 9 | `prop:tb-recursion` (≤ b calls on every branch, error ≤ ε, time-out) | **Holds** (proved; exact simulation incl. adversarial solver) | — |
| 9a | its sentence "there are then log_p\|H\| enlarging calls plus one final call when H ≠ G" | **False as an equality** (the bound ≤ b is unaffected) | L = (Z/p)², H = G: one call, the sentence says two. Fix P1 |
| 10 | Access model ("no group inverse oracle is used") | **Gap, closable** | order finding (Lemma tb-sylow(d)) runs before any exponent multiple is known, so x^{M−1} is unavailable there; out-of-place Bennett evaluation fixes it (P2) |
| 11 | `lem:tb-sylow` (a)–(c) | **Holds** (proved; exact) | (c) is sharp in p > c: D_8 (p = c = 2) and C_3 ≀ C_3 (p = c = 3) have generators of order p and exponent p² |
| 12 | `lem:tb-sylow` (d) | **Holds as stated (poly)**, but it does not give the body's O(sℓ² + sℓ log(s/ε)) | fix P2 |
| 13 | `lem:tb-small-primes` | **Holds as an import** (II Thm 1 not re-read) | — |
| 14 | `prop:black-box` (i) proof (Φ surjective hom, evaluation counts) | **Holds** (proved; exact on C_{p²}⋊C_p, p = 3, 5, 7) | — |
| 15 | `lem:tb-kernel` | **Holds** (proved; span bound exact) | — |
| 16 | `prop:black-box` (ii): e = 1, (R1), (R2) | **Holds** (proved, conditional as stated) | e = 1 via the chart (used by `thm:bb-envelope`) is not spelled out; one sentence (P6) |
| 17 | `prop:black-box` (iii) | **Holds** (proved; exact, every subgroup at p = 3, 5, 7) | — |
| 18 | `prop:black-box` (iv) chart cost O_c(s^cℓ³ + ℓ⁴), 4n(2b_M + A_c) per use | **Not proved in the paper.** The appendix's own (R2) route goes through (M1) with S = F, a d × d Smith form, which is only poly(d) | P4 gives a proof at O_c(dk² + k⁴). The 11-02 argued step it came from is **false** as written (§5, C_9 × C_3) |
| 19 | Table `tab:tb-steps`, `rem:tb-scope` | **Holds** (d(4,9) = 40584 exact) | — |
| 20 | `thm:bb-envelope` (i), queries for p > c | **Holds, conditional** (on the per-call core bound and `thm:ring-to-field`(iii)) | — |
| 20a | `thm:bb-envelope` final paragraph: total queries O_c(N^{E_W+1}); "query exponent is E_W(c)" when all e_p = 1 | **Not proved**: both include the II queries, whose exponent contains α_22, which the 11-02 review left UNKNOWN | fix P5: state the large-prime count and the II term separately |
| 20b | `thm:bb-envelope` (ii) | **Two gaps**: preprocessing count not proved (row 12); chart acquisition omits evaluating Φ on the chart basis | P2, P3 |
| 20c | `thm:bb-envelope` (iii) classical chart time | **Argued only** | P4 |
| 20d | `thm:bb-envelope` (iv), error split | **Holds** | — |
| 21 | Field-solver hypothesis "class at most c" vs `def:input-contract` "class c" | **Wording gap** | socles can have class below c; P7 |

No counterexample to any theorem-level claim of the appendix. One false sentence (9a), one
false argued step in the source review (18), and four cost statements in `thm:bb-envelope`
that the paper does not prove (12, 18, 20a, 20b).

## 1. Lazard toolkit (`app:tb-lazard`)

**Integrality (`lem:tb-integral`). Proved.** For a homogeneous Lie element u_n of degree n,
Dynkin–Specht–Wever gives θ(u_n) = n·u_n, and θ maps T_{R_c} into Λ_{R_c}. For n ≤ c the
integer n is a unit of R_c. The identification of Λ_{R_c} with R_c ⊗ Λ_Z inside T_Q uses
that R_c is a localization of Z, hence flat; the text leaves this implicit, which is fine.

**(eq:tb-commutator), (eq:tb-conjugation). Proved.** The degree-n part of
log(e^{−U}e^{−V}e^Ue^V) has denominators that are products of integers ≤ n, so by the lemma
it lies in Λ_{R_c}. Its bidegree-(n,0) and (0,n) parts vanish, since the commutator is 1
when either argument is 0. So κ consists of monomials containing both u and v. The
conjugation sum stops at c − 1 because ad_x^c = 0 in class c.

**Words (`lem:tb-words`). Proved.** I checked the degree bookkeeping: a bracket monomial
with i ≥ 1 entries u ∈ b + Λ^{(k+1)} and j ≥ 1 entries X_j, i + j ≥ 3, has degree
≥ ik + j ≥ k + 2. The correction step is right because BCH_c(u,v) ∈ u + v + Λ^{(2k)} for
u, v ∈ Λ^{(k)}, and 2k ≥ k + 1. The implemented compiler uses the opposite commutator
convention xyx^{−1}y^{−1}; both have leading term [X,Y], so nothing changes.

**Prime-power evaluation (`lem:tb-evaluation`). Proved; exact.** The only nontrivial step
is the power instruction: bn ≡ a (mod M) and Mψ(ℓ) = 0 give b·nψ(ℓ) = aψ(ℓ), and b is a
unit on log G. This needs M to be a multiple of the exponent, not merely a power of p.
`check_lazard_eval.py` evaluates the project's certified words with modulus p^e on
UT_{c+1}(Z/p^e) (class exactly c). It compares them with exp(log x + log y) and
exp([log x, log y]), computed by matrix series mod p^e, at
(p,c,e) ∈ {(3,2,2), (3,2,3), (5,3,2), (5,4,2), (5,4,3), (7,3,3), (7,5,2), (7,6,2)}. All
agree, including the largest class c = p − 1. With modulus p at e = 2 the words fail at
(5,3), (7,5) and (5,4), which is the old compiler defect and shows the hypothesis is
needed. The evaluator rejects p ≤ c.

**Correspondence (`cor:tb-correspondence`). Proved; exact.** (b), converse direction: from
e^{ad x}K = K, N = e^{ad x} − 1 preserves K and N^c = 0 (because N = ad_x·(unit
polynomial)). So ad_x = log(1 + N), a polynomial in N with denominators below c, preserves
K. (c): |x ∗ K| = |K| = |x + K| together with the inclusion gives equality.
`check_correspondence.py` checks, on (Z/9)² with [x,y] = 3y, Heis(Z/9),
Z/25 ⊕ Z/5 with [e1,e2] = 5e1, a class-3 mixed ring Z/25 ⊕ Z/5 ⊕ Z/5 (Jacobi and class
verified), and the filiform F_5⁴: (a) BCH group closure equals Lie closure for 80 random
generating sets each; (b) normalizer in (S,∗) equals the idealizer for 202 pairs (K,S),
with S = L and S a proper subring; (c) x ∗ K = x + K for 81 ideal pairs.

## 2. Ring-to-field (`app:tb-ring`)

**(M1)–(M3). Proved.** In (M1), C = B_S^{−1}B_K is integral because Λ_K ⊆ Λ_S, and
B_K = B_S P^{−1} diag(δ) Q^{−1} gives Λ_K = W diag(δ) Z^m and Λ_S = W Z^m. The δ_i are powers
of p because DZ^m ⊆ Λ_K. In (M3), x = Σ t_k u_k ∈ (S/K)[p] forces p t_k ≡ 0 (mod p^{a_k}),
so dividing by p^{a_k−1} is exact on residues mod p^{a_k} and well defined mod p.

**Part (i). Proved.** The class bound uses the strict decrease of γ_j of a nilpotent
F_p-algebra: the chain γ_2 ⊋ ⋯ ⊋ γ_{k+1} = 0 has k − 1 strict steps.

**Part (ii). Holds, conditional on `cor:fpt-r`.** The restriction argument, the isomorphism
ι and the one-query-per-query accounting are correct. `cor:fpt-r` needs r ≥ 1, and the text
correctly sends r_loc = 0 to abelian Fourier sampling. That branch's error and sample count
are not stated. They are standard, but Prop `tb-recursion` needs every call to have error
≤ ε/b, so one clause is worth adding (P7).

**Quotient oracle, section rank. Proved.** The key step is that h ⊇ K is a union of
K-cosets, so g ∈ h ⟺ q(g) ∈ h/K. This needs K ⊆ h; the lemma assumes it, and the error
analysis only uses the lemma on the event that the earlier calls were correct.

**`prop:tb-recursion`. Proved; exact.** I tried to break it as follows.

- *Call count on every branch.* |K_j| ≥ p^j holds because every accepted U is nonzero, so
  K strictly grows, whatever the solver returned. A call in round j needs S_j ≠ K_j, so
  |K_j| ≤ p^{b−1} and j ≤ b − 1.
- *Edge L = Z/p^b, H = G.* S = L throughout, K_j = p^{b−j}L, and the socle of L/K_j is
  one-dimensional and fully hidden. After b calls K = L = S, and stop rule 1 fires. Without that rule a (b+1)st call on S/K = 0 would occur, as the text says.
  Exact (`Z/27`).
- *Invariant.* K' = q^{−1}((h/K) ∩ M[p]) = h ∩ P, and h ⊆ I_S(K') because P is an ideal of
  S. Exact on every truth-solver run.
- *Error.* The first-error decomposition is right: a wrong output forces a first incorrect
  call j, and conditioned on the earlier calls being correct the j-th input is a fixed valid
  instance with fresh coins. This needs a per-instance error guarantee from Solve, which is
  how "field solver" is defined.
- *Time-out.* It needs T_Solve to be computable from (dimension, log p, w, η). Theorem main
  gives an explicit bound, so this holds.

**The one false sentence (9a).** The proof says "there are then log_p|H| enlarging calls
plus one final call when H ≠ G". An enlarging call adds U = (h/K) ∩ M[p], which can have
dimension above one, so the count of enlarging calls is at most log_p|H|, not equal to it.
Smallest instance: L = (Z/p)² (any p > c = 1), H = G. One call returns all of L; the
sentence predicts two. `check_rtf_recursion.py` reports how often the equality fails (§2.1).
The conclusion "at most b in all" still holds, by the call-count paragraph. Fix P1.

### 2.1 Exact simulation of RtF

`check_rtf_recursion.py` (exact; output `check_rtf_recursion.out`) uses eight rings, each
checked for Jacobi on basis triples and for its declared class (< p):

- Z/27 and Z/25 ⊕ Z/5, both abelian;
- (Z/9)² with [x,y] = 3y;
- Z/9 ⊕ Z/3 ⊕ Z/3 with [e2,e3] = 3e1;
- Heis(Z/9), with b = 6;
- Z/25 ⊕ Z/5 with [e1,e2] = 5e1;
- a class-3 mixed ring Z/25 ⊕ Z/5 ⊕ Z/5 with [e0,e1] = e2, [e0,e2] = 5e0 (R = 2);
- (Z/25)² with [x,y] = 5y.

Each ring was run on 0, L and random Lie closures of 1–2 elements, 171 hidden subrings in
all.

- *Truth solver.* RtF returned h in all 171 cases within b calls. The invariant
  K ⊆ h ⊆ S held at every round, every section had derived cyclic rank ≤ R, and every
  socle had class ≤ min(c, R+1).
- *Adversarial solver*, 15 branches per case (2565 branches). It returns the truth, or K,
  or a random additive subgroup between K and the socle preimage, which need not be a
  subalgebra or contain the truth. On every branch the call count stayed ≤ b, and stop rule
  2 rejected the non-subalgebras.
- *Sentence 9a.* In 43 of the 171 truth cases the call count differs from
  "log_p|H| + [H ≠ G]". The smallest ring is (Z/9)² with [x,y] = 3y and |H| = 27: 3 calls
  (2 enlarging), against 4 predicted. The hand example L = (Z/p)², H = G is smaller still.
- *Socle dimensions.* Summed over one run they reach 2b: on Z/9 ⊕ Z/3 ⊕ Z/3 with |H| = 9,
  the socle dimensions are 3, 3, 2 against b = 4. This is harmless for the call cap, and §4
  shows that `thm:bb-envelope` does not rely on the opposite.

**Proof of `thm:ring-to-field`. Proved**, given the above. The (iii) sentence "a nontrivial
h of order p^j gives h^{p^{j−1}} ∈ H_1" is right, and H ≤ N because H_1 = H ∩ Ω_1(G) is
normal in H.

## 3. Black-box groups (`app:tb-blackbox`)

**Access model (row 10). Gap, closable.** The text derives every inverse as x^{M−1} once a
multiple M of the exponent is known. Lemma tb-sylow(d) runs Shor's order finding before any
such M is known. The usual circuit multiplies in place by the classical constants
g^{2^j}, which needs g^{−2^j}, and g^{−1} = g^{o−1} needs the unknown order. The fix is
standard: compute g^k out of place. Keep ⌈log₂ Q⌉ fresh registers z_{j+1} = z_j·(k_j ? g^{2^j}
: 1), using the XOR multiplication with a classically controlled constant, copy out the
last one, and run the chain backwards. This costs twice the multiplications and O(ℓ)
registers of ℓ bits, and it uses no inverse. `thm:bb-envelope` sidesteps the issue by
assuming "coherent multiplication and its inverse". The appendix should say which one it
means (P2).

**`lem:tb-sylow`. (a)–(c) proved; (d) holds as stated.** (c) is sharp:
`check_sylow_and_counts.py` gives D_8 = ⟨two reflections⟩ (class 2, p = 2, generator orders
2, 2, exponent 4) and C_3 ≀ C_3 = ⟨(012), (036)(147)(258)⟩ (order 81, class 3, generator
orders 3, 3, exponent 9). So the p > c hypothesis cannot be dropped, and the M chosen for
G_{≤c} in the access model (the loose ∏ p^{⌊ℓ/log₂p⌋}) is the right choice there. In (d) the
lemma claims success probability ≥ 1/poly(ℓ) per run and poly(ℓ)·log(s/ε) runs. That gives
poly(s, ℓ, log(1/ε)), as stated, but not the body's O(sℓ² + sℓ log(s/ε)) multiplications
(row 12). The sharper count is true, by the lcm-of-two-runs argument in P2.

**`lem:tb-small-primes`. Holds as an import.** The reduction steps are right. The
projection to G_{≤c} with n_i is correct. f restricted to G_{≤c} hides H ∩ G_{≤c}, the
Sylow factorization of H shows this. The purification Σ_x |x⟩|f(x)⟩ has the stated reduced
state. I did not re-read II's Theorem 1 or its Lemma 1.

**`prop:black-box` (i). Proved; exact.** The Hall-basis recursion
w_j = [w_{j'}, w_{j''}] with j', j'' < j is the defining property of basic commutators, so
h_j = π(w_j). Counts: an integer power with n < M costs at most 2⌈log₂M⌉ multiplications,
and the compiler's cap is exactly 2·bitlength(M). `check_metacyclic_pullback.py` builds
Φ: F_{2,2}(Z/p²) → C_{p²} ⋊ C_p only through black-box multiplication, the certified words
and the Hall basis X1, X2, [X1,X2], at p = 3, 5, 7. Φ is surjective, and Φ(u ∗ v) = Φ(u)Φ(v)
holds for all 729² pairs at p = 3 and 4000 sampled pairs at p = 5, 7. ker π has order p³ and
is an ideal.

**`lem:tb-kernel`. Proved; exact bound.** Uniform samples on A = (ker π)^⊥ have uniform
images in A/pA ≅ F_p^k, and generating A is equivalent to spanning A/pA (Nakayama, as the
proof says). The bound k ≤ min(d, ⌊ℓ/log₂p⌋) is right: A ≅ F/ker π, and |F/ker π| = |G| ≤ 2^ℓ.
The script computes the exact failure probability 1 − ∏_{i<k}(1 − p^{i−t}) for
p ∈ {2,3,5,7,11}, k ≤ 8 and t ≤ k + 11. It is always ≤ (#hyperplanes)·p^{−t} ≤ p^{k−t}, and
t = k + ⌈log_p(2/δ)⌉ gives ≤ δ/2 at δ ∈ {1/2, 1/10, 1/1000}.

**(ii). Holds.** (R1): b_F = ed, socles of sections of F have class ≤ c and dimension ≤ d.
(R2): Φ̄ = Φ∘σ̃ = π̄ is right, because q∘σ̃ = id. One accounting point is correct but easy to
misread. Table `tab:tb-steps` charges 2E_Φ per query, while the body charges 4n_p(2b_M + A_c).
Both are valid upper bounds. Compute Φ with garbage, apply U_f to the output register, and
run the computation backwards: that is 2E_Φ and needs no separate copy. The body's 4 counts
a Bennett-cleaned evaluation twice. e = 1 through the chart, which `thm:bb-envelope`(i)
uses, is (R2) without the recursion: F/ker π is then an F_p-algebra and Theorem main applies
to it directly. The appendix says this only as "optionally" (P6).

**(iii). Proved; exact.** F[p] = p^{e−1}F holds because F is free over Z/p^e. Then
Φ(F[p]) = p^{e−1} log G = ℧_{e−1}(G) ⊆ Ω_1(G). The exact script checks, at p = 3, 5, 7:
℧_1(G) has order p and Ω_1(G) has order p²; b has no order-p preimage; Φ(pX1) = a^p;
Φ^{−1}(Ω_1(G)) = {x : px ∈ ker π}; and Φ(K ∩ F[p]) = H ∩ ℧_1(G) for every subgroup H
(10, 14, 18 subgroups).

**Composition. Holds.** H = ∏_p (H ∩ G_p), and the steps run in sequence with fresh coins,
so the first-error union bound applies. `rem:tb-scope`: d(4,9) = Σ_k W(4,k) = 40584 (exact).

## 4. Body statement `thm:bb-envelope`

**(i), large primes. Holds, conditional.** The proof sketch bounds each Sylow by n_p calls
of dimension ≤ n_p. Each call costs ≤ cK_c(n_p + t)(n_p + 1)^{E_W−1}, imported from
Appendices A/B. Superadditivity of x ↦ x(x + t)(x + 1)^{E−1} then gives
Σ_p ≤ cK_c(L + t)(L + 1)^{E_W}. Superadditivity holds because x ↦ (x + t)(x + 1)^{E−1} is
increasing; the script also checks it on 0..59. The factor x is the number of calls; it is
not a sum of socle dimensions. That matters, because the socle dimensions summed over a run
can exceed n_p. The simulation of §2.1 shows this, and on Z/p^a ⊕ (Z/p)^k with H the cyclic
factor the sum is (a+1)(k+1) against n_p = a + k. The sketch's per-call bound does not need
it. L ≤ ℓ/log₂(c+1) holds because p ≥ c + 1. t = ⌈log₂(12ℓ/ε)⌉ ≥ ⌈log_p(3·4ℓ/ε)⌉, the core
error term at error ε/(4ℓ). The quoted numbers also check (`check_sylow_and_counts.py`):
9·143 = 1287, the Schedule-1 exponent at c = 9 is 145, and log₂(9K_9) = 1206.0.

**Final paragraph, total query exponent (20a). Not proved.** "The number of queries to f is
O_c(N^{E_W(c)+1})" counts all queries, and (i) says the primes p ≤ c "add the queries of
[II23, Thm 1], poly(log|G|)". The comparison remark gives II's exponent as
2 + (c−1)σ_p + α_22. The 11-02 envelope review (§0) states that α_22, the query exponent of
II's exact abelian subroutine, "was not read, so it stays UNKNOWN". So the total exponent
is proved only for the primes p > c. Smallest case where it matters: c = 2. There the
statement needs 3 + α_22 ≤ E_W(2) + 1 = 6, i.e. α_22 ≤ 3, and for the exponent-p sentence
(E_W(2) = 5) α_22 ≤ 2. Neither is established. The same applies to the gate exponent
E_W + 4 + o(1), whose (iii) explicitly adds II's gates and those of order finding. Fix P5:
state the p > c count, and the II term as a separate additive term with its own (imported)
exponent.

**(ii) (20b). Two gaps.**
- *Preprocessing.* O(sℓ² + sℓ log(s/ε)) multiplications is not what Lemma tb-sylow(d)
  proves (row 12). P2 proves it.
- *Chart acquisition.* (R2) needs the chart-to-group words, and these need E_i = Φ(σ̃(ε_i))
  for the n'_p ≤ n_p chart basis elements. The count
  (d − s)(m_[] + 2b_M q_[]) + 2kd(2b_M + A_c) leaves out these classical evaluations. Through
  the appendix's (M1) section they cost ≤ n_p·d(2b_M + A_c). Through the column-selection
  section of P4 they cost ≤ n_p²(2b_M + A_c). The 11-02 envelope review (§2.4) had this term;
  it was lost in the theorem. Since n_p ≤ k, adding it changes the constant 2 to 3 at most.
  Fix P3.

**(iii) (20c). Argued only.** The classical chart time O_c(s^cℓ⁵ + ℓ⁶) bit operations rests
on `prop:black-box`(iv)'s O_c(s^cℓ³ + ℓ⁴) ring operations. The paper does not prove that.
The appendix's (R2) uses (M1) with S = F and K = ker π, which as written is a Smith form of a
d × d basis matrix, O(d³) = O(s^{3c}). It also uses the full Hall structure tensor of F,
whose cost the appendix states only as poly(s, e log p). The cheap route needs three facts.
First, the chart is im Y for the k × d sample matrix Y. Second, generators are chosen by
greedy membership, not by rank mod p. Third, the Hall structure constants are sparse by
multidegree. P4 writes this out. Its total is O_c(dk² + k⁴) ring operations, within the
claimed bound.

**(iv). Holds.** Four shares of ε/4: preprocessing, II (gate synthesis only), chart
acquisition (ε/(4ℓ) per prime, ≤ ℓ primes), and core calls (ε/(4ℓ) each, ≤ L ≤ ℓ calls).

**Hypothesis wording.** "Coherent multiplication and its inverse" is stronger than what the
appendix uses. Either keep it (then row 10 is moot for the theorem) or drop it and add P2's
out-of-place sentence. Optional.

## 5. Comparison with the 11-02 reviews (read after §§1–4)

- **`2026-11-02-rees-fpt-torsion-check.md` §B.** It agrees with every verdict above on
  ring-to-field. Its B3 states the count correctly, "≤ log_p|H| nontrivial steps, plus one
  final trivial call when H ≠ S". The appendix turned this into an equality (row 9a), so the
  error was introduced in drafting. Its simulation covered 293 (ring, H) pairs with a truth
  core; mine adds an adversarial core, which tests the "every branch" claim directly.
- **`2026-11-02-rees-black-box-check.md` C1, C5.** It agrees on the Sylow split, Φ, ker Φ
  as an abelian HSP, (R1)/(R2) and the metacyclic identities; my exact run reproduces C5's
  table. C1 argues (c) from regularity. My D_8 and C_3 ≀ C_3 examples confirm that the
  hypothesis p > c is needed. C1 counts preprocessing only as poly. C5's sample count
  "O(d + log 1/ε)" was already corrected by the envelope review, and the appendix's count is
  the corrected one.
- **`2026-11-02-rees-bb-envelope.md`.** Three points.
  - *(a) §2.4 "Structure constants [argued]" is false as written.* "Choose ≤ r Hall
    (Lyndon) basis elements whose Y-columns span im Y mod p. By Nakayama, they generate
    L(G_p)." Spanning im Y modulo p(Z/M)^k is not spanning im Y/p·im Y.
    `check_chart_selection.py` gives the smallest instance: G = C_9 × C_3 (p = 3, c = 1,
    exact exponent 9), generators (1,0), (0,1). Every sample lies in
    (ker π)^⊥ = {(x, 3y)}, so column 2 of Y vanishes mod 3. The mod-3 rule selects column 1
    only, which generates a subgroup of order 9 of the order-27 chart. With the review's
    own "loose M" option (§2.1), G = C_p and M = p² already break it, since every column
    vanishes mod p. Greedy membership selection (P4) fixes this, at the same cost.
  - *(b)* It flags α_22 as UNKNOWN, but the theorem's headline exponent drops the caveat
    (row 20a).
  - *(c)* Its preprocessing count assumes O(log(s/ε)) runs per generator, i.e. constant
    success per run, which the appendix does not prove (row 12). It also included the
    chart-basis images that the theorem omits (row 20b).
- Nothing in the three reviews contradicts a verdict here. The points above that the
  reviews do not contain are rows 9a, 10, 12, 18 (counterexample), 20a (as a defect of the
  theorem's text) and 21.

## 6. What now holds, what is missing, gates

**Exact statement that now holds** (AI-checked, pending human review). Fix c. Theorem
`thm:ring-to-field` (i)–(iii) and Proposition `tb-recursion` hold as stated. In particular,
on every branch RtF makes at most b field calls, none on a trivial section, and with error
ε/b per call it returns h with probability ≥ 1 − ε. Part (ii) is conditional on
`cor:fpt-r`. Proposition `prop:black-box` (i)–(iii) hold as stated, with (ii) for e > 1
conditional on Theorem main and `thm:ring-to-field`(iii). For `prop:black-box`(iv) and
`thm:bb-envelope`, what holds is the following. Black-box queries for the primes p > c
number at most cK_c(L + t)(L + 1)^{E_W(c)}, conditional on the per-call core bound of
Appendices A/B. Chart acquisition costs at most
(d − s)(m_[] + 2b_M q_[]) + 3kd(2b_M + A_c) multiplications per prime. Preprocessing costs
O(sℓ² + sℓ log(s/ε)) multiplications, with the P2 argument. The primes p ≤ c add II's query
count, with an exponent not bounded here.

**Still missing.**
- α_22, or any bound on II's total query and gate exponent at c < 9, needed for the
  all-prime exponents.
- A written proof of the chart cost (P4 is the proposal; it is argued, not machine-checked).
- Human review of everything.
- The copy-only variant, which is not covered.

**Claim gates that must stay false** (`research/reductions/rees_hsp_reduction.json`):
`independent_review`, `novelty_established`, `speedup_claim_allowed`,
`coherent_receiver_implemented`, `general_sde_implemented`, `formal_compiler_checked`. Also
`large_prime_outer_envelope.{outer_reduction_implemented, covers_small_prime_queries,
covers_group_preprocessing_cost, is_total_gate_bound}`, and every false flag of
`copy_only_outer_envelope`.

## 7. Proposed paper text

All targets are for the integrator (`rees-r2-01-integrator`). Status label for every item:
**AI-checked, pending human review**.

**P1** (target: `appendix-torsion-blackbox.tex`, proof of `prop:tb-recursion`, end of
"Correctness of a round"; status: proved). Replace

```latex
The invariant holds initially ($0 \subseteq \hh \subseteq \mathcal{L}$), so on the
event that every call made returns the correct answer, the output is $\hh$; there are
then $\log_p|H|$ enlarging calls plus one final call when $H \ne G$, at most $b$ in all
(when $H = G$, stop rule~1 removes the final call).
```

with

```latex
The invariant holds initially ($0 \subseteq \hh \subseteq \mathcal{L}$), so on the
event that every call made returns the correct answer, the output is $\hh$. Each
enlarging call multiplies $|K|$ by at least $p$, so there are at most $\log_p|H|$
enlarging calls and at most one final call; by the call count above there are at most
$b$ calls in all. (For $\mathcal{L} = \Fp^2$ and $H = G$ a single call suffices.)
```

**P2** (target: `appendix-torsion-blackbox.tex`, `lem:tb-sylow`(d) statement and proof, and
one sentence of the access model; status: argued, standard). In the statement of (d)
replace "in time $\poly(s,\ell,\log(1/\eps_{\mathrm{pre}}))$" with

```latex
using $O(s\ell^2 + s\ell\log(s/\eps_{\mathrm{pre}}))$ group multiplications and
$\poly(s,\ell,\log(1/\eps_{\mathrm{pre}}))$ further gates
```

and replace the proof of (d) with

```latex
(d) No inverse is available yet, so $k \mapsto g_i^k$ is computed out of place: with
precomputed constants $g_i^{2^j}$, put $z_0 = 1$ and
$z_{j+1} = z_j\cdot(k_j\,?\,g_i^{2^j} : 1)$ in fresh registers using the coherent
multiplication, copy the last register, and run the chain backwards. This costs
$O(\ell)$ multiplications and $O(\ell)$ registers per run and needs no inverse. One run of
Shor's order-finding circuit (\arxivid{quant-ph/9508027}) with $2\ell+1$ control qubits
returns, with probability at least $4/\pi^2$, the reduced fraction of $k/o_i$ for some $k$,
each $k \in \{0,\dots,o_i-1\}$ having probability at least $4/(\pi^2 o_i)$. For two
independent runs, the lcm $v$ of the two denominators equals $o_i$ whenever
$\gcd(k_1,k_2,o_i) = 1$, so $\Pr[v = o_i] \ge (4/\pi^2)^2\prod_{q \mid o_i}(1-q^{-2})
\ge (4/\pi^2)^2\cdot 6/\pi^2 > 1/11$. Repeat pairs until $g_i^{v} = 1$, at most
$\lceil 11\ln(s/\eps_{\mathrm{pre}})\rceil$ times; each test costs $O(\ell)$
multiplications, and any $v$ with $g_i^v = 1$ is a multiple of $o_i$. Factor $v$ with
Shor's algorithm and certify its prime factors deterministically (Agrawal, Kayal and
Saxena, Ann.\ of Math.\ 2004); this uses no group multiplication. Then strip primes:
while $q \mid v$ and $g_i^{v/q} = 1$, replace $v$ by $v/q$. This ends at $o_i$ after at most
$\log_2 v \le 2\ell$ tests of $O(\ell)$ multiplications each (only denominators below
$2^\ell$ are kept). A generator fails only if no
pair succeeds, with probability at most $\eps_{\mathrm{pre}}/s$, and the failure is
detected. The generators $g_i^{o_i'}$ cost $O(s\ell)$ multiplications per prime, and there
are at most $\ell$ primes.
```

In the access model, after "No group inverse oracle is used:", insert "the order finding of
Lemma~\ref{lem:tb-sylow}(d) runs out of place and needs none, and". If the integrator keeps
`thm:bb-envelope`'s hypothesis "and its inverse", add "(the appendix does not use it)".

**P3** (target: `main.tex`, `thm:bb-envelope`(ii); status: proved, given P4 or the
appendix's (M1) route). Replace

```latex
Chart acquisition costs $(d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 2k\,d\,(2b_M + A_c)$ multiplications per prime $p > c$.
```

with

```latex
Chart acquisition costs $(d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 2k\,d\,(2b_M + A_c) + n_p^2(2b_M + A_c) \le (d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 3k\,d\,(2b_M + A_c)$ multiplications per prime $p > c$; the last term evaluates $\Phi$ on the chart basis.
```

**P4** (target: `appendix-torsion-blackbox.tex`, new paragraph at the end of (R2); status:
argued). Insert

```latex
\emph{Chart arithmetic at cost linear in $d$.} Use a Lyndon basis, a Hall basis that is
multihomogeneous and invariant under order-preserving relabelling of the generators. The
expansion of $[w_a,w_b]$ then lies in the span of the basis elements of multidegree
$\mu(a)+\mu(b)$, at most $c!$ of them, and is read from a table depending only on $c$.
Let $Y$ be the $k \times d$ matrix of the samples of Lemma~\ref{lem:tb-kernel}. Then
$u \mapsto Yu$ induces $F/\ker\pi \cong A \coloneqq YF \subseteq (\mathbb{Z}/p^e)^k$. Scan
the columns $Yw_j$ and keep $j$ exactly when $Yw_j$ lies outside the span of the columns
kept so far, which is tested against a Howell form in $O(k^2)$ ring operations. Each kept
column multiplies the span's order by at least $p$, so at most $n = \log_p|G|$ columns are
kept, and they generate $A$. Testing the residues of the columns modulo $p$ is not enough:
for $G = C_9 \times C_3$ every sample lies in $\{(x,3y)\}$, and the second column vanishes
modulo $3$. A Smith form of the $k \times n$ matrix of kept columns presents
$\mathcal{L}_G$ with a basis $\varepsilon_i = \sum_{j} \alpha_{ij} w_j$ supported on kept
indices. Its structure constants come from the $O_c(n^2)$ products $Y[w_a,w_b]$ and two
contractions, and the images $\Phi(\varepsilon_i)$ cost at most $n(2b_e + m_+ + 2b_eq_+)$
multiplications each from the precomputed $h_j$. In all this is $O_c(dk^2 + k^4)$ ring
operations modulo $p^e$ and $n^2(2b_e + m_+ + 2b_eq_+)$ multiplications, with no query to
$f$.
```

**P5** (target: `main.tex`, `thm:bb-envelope`, final paragraph; status: proved for p > c).
Replace

```latex
For fixed $c$ and input size $N = s\ell + w + \log(1/\eps)$, the number of queries to $f$ is $O_c(N^{E_W(c)+1})$, and it does not depend on $s$. The number of gates is $O_c(N^{E_W(c)+4+o(1)})$, and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$.
```

with

```latex
For fixed $c$ and input size $N = s\ell + w + \log(1/\eps)$, the number of queries to $f$ for the primes $p > c$ is $O_c(N^{E_W(c)+1})$, and it does not depend on $s$; the primes $p \le c$ add the $\poly(\log|G|)$ queries of~\cite[Theorem~1]{ImranIvanyos2023}, whose exponent includes that of their exact abelian subroutine and is not bounded here. For the primes $p > c$, and for order finding, factoring and the charts, the number of gates is $O_c(N^{E_W(c)+4+o(1)})$ and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$; the gates and time of~\cite{ImranIvanyos2023} are added separately.
```

and replace "If every Sylow subgroup for $p > c$ has exponent $p$, the query exponent is
$E_W(c)$." with "If every Sylow subgroup for $p > c$ has exponent $p$, the large-prime
query exponent is $E_W(c)$."

**P6** (target: `appendix-torsion-blackbox.tex`, proof of `prop:black-box`(ii), end of
"Exponent $p$"; status: proved). Replace "Optionally, Lemma~\ref{lem:tb-kernel} with $e = 1$
followed by the chart construction below reduces it to $\log_p|G| \le \ell$." with

```latex
Alternatively, Lemma~\ref{lem:tb-kernel} with $e = 1$ and the chart of route~(R2) below give
an explicit $\Fp$-Lie algebra $\mathcal{L}_G = F/\ker\pi$ of dimension
$\log_p|G| \le \ell$ and an oracle $f\circ\bar\Phi$ hiding $\bar\Phi^{-1}(H)$; one call of
Theorem~\ref{thm:main} on it, with no recursion, recovers $H$. This is the route of
Theorem~\ref{thm:bb-envelope}(i) for $e_p = 1$.
```

**P7** (target: `appendix-torsion-blackbox.tex`, the paragraph defining a field solver, and
part (ii); status: proved). After "so a field solver for class at most $c$ suffices." insert

```latex
Theorem~\ref{thm:main} is stated for class $c$; a socle of class $c' < c$, read off from its
structure constants, is processed by Theorem~\ref{thm:main} at $c'$, whose bounds are at
most those at $c$ because each factor $B_d(g_d)$ is at least one.
```

and in part (ii) replace "abelian Fourier sampling over $\Fp^m$ returns $\iota^{-1}(H_1)$" with

```latex
abelian Fourier sampling over $\Fp^m$ with $m + \lceil\log_p(2/\eta)\rceil$ samples and
approximate transforms of total precision $\eta/2$ returns $\iota^{-1}(H_1)$ with error at
most $\eta$, as in Lemma~\ref{lem:tb-kernel}
```

## Scripts (folder `2026-11-03-rees-check-app-d/`)

| Script | Checks | Output |
|---|---|---|
| `lazard_small.py` | helper: mixed-order Lazard rings, BCH through class 3 | — |
| `check_lazard_eval.py` | Lemma tb-evaluation on UT_{c+1}(Z/p^e); M = p negative control; p ≤ c rejected | `.out` |
| `check_correspondence.py` | Cor tb-correspondence (a)–(c) by brute force | `.out` |
| `check_rtf_recursion.py` | RtF with truth and adversarial solvers; call cap, invariants, socle class, sentence 9a | `.out` |
| `check_metacyclic_pullback.py` | Prop black-box (i), (iii), Lemma tb-kernel on C_{p²}⋊C_p, p = 3, 5, 7 | `.out` |
| `check_sylow_and_counts.py` | Lemma tb-sylow(c) sharpness, span bound, Witt and exponent numbers | `.out` |
| `check_chart_selection.py` | mod-p column selection fails on C_9 × C_3; greedy selection works | `.out` |
