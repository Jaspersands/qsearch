# Rees item 6: prime-power word compiler for class c ≥ 5 (2026-11-02)

AI session only; human review still required. Campaign: `research/REES_FULL_CAMPAIGN.md`, item 6.
Scripts, data and outputs: `research/audits/reviews/2026-11-02-rees-prime-power-compiler/`.

**Verdict.** The gap closes. The class ≤ 4 boundary for exponent p^e was never mathematical. The
general-class certificates already in the repo, evaluated with exponents mod p^e instead of mod p,
compute the Lazard addition and bracket in **every** finite p-group of class ≤ c < p, for every
e ≥ 1. A short proof is in §2. There is no obstruction anywhere in c < p, so there is no
"smallest failing (c, p, e)". Exact checks at p = 7, 11, e = 2, c = 5, 6 (plus wider controls)
agree with Φ computed directly, and the negative controls fail as they should.

## 1. Why the construction stopped at c ≤ 4 for p^e (exact diagnosis)

- **Certificates are characteristic-free.** `compile_lazard_word(c, op)`
  (`theorems/universal_lazard_words.py`) builds a straight-line program of multiplications and
  rational powers x^{a/b}. Its verifier checks the identity exactly in Q⟨X,Y⟩/(deg > c), and it
  checks that every denominator has prime support ≤ c. Neither step mentions p.
  (Exact computation, from the existing verifier.)
- **Only the evaluator assumes exponent p.** `UniversalLazardWords` uses p in exactly three places:
  - line 196, `exponent %= self.p` in `power`. This also makes x^{-1} into x^{p-1}.
  - line 213, `pow(denominator, -1, self.p)`: each a/b becomes a·b^{-1} **mod p**.
  - line 225: `linear_combination` coefficients are restricted to [0, p).

  In a group of exponent p^2 all three are wrong.
- **Smallest exhibited failure.** Class 2, p = 3, e = 2, in UT_3(Z/9), with x = 1+E_12 and
  y = 1+E_23. The true value exp(log x + log y) has corner entry 5 (= 1/2 mod 9). The mod-p
  evaluator returns 8, the mod-9 evaluator returns 5, and x^{p-1} ≠ x^{-1}. (Exact computation,
  `exponent_p_evaluator_failure`.) At (p, e, c) = (7, 2, 5) the mod-p evaluator fails ADD on 10 of
  10 random pairs and breaks the pullback homomorphism. In GAP it fails the homomorphism test on
  all four relatively free groups of §4.
- **No identity or denominator fails mod p^e.** The largest certificate denominators are:

  | c | ADD (mul, pow, max den) | BRACKET (mul, pow, max den) |
  |---|---|---|
  | 5 | 118, 44, 3600 = 2^4 3^2 5^2 | 116, 42, 60 |
  | 6 | 230, 88, 8640 | 228, 86, 720 |
  | 7 | 498, 184, 2116800 = 2^6 3^3 5^2 7^2 | 496, 182, 5040 |
  | 8 | 978, 368, 14515200 | 976, 366, 40320 |

  Every prime involved is ≤ c < p, so all of them are units mod p^e.
- **Why c ≤ 4 was covered.** It was covered only because `ClassFourGroupWords`
  (`CLASS_FOUR_PRIME_POWER_INPUT.md` §1) was written with an annihilating modulus M. The universal
  compiler's contract (`UNIVERSAL_LAZARD_WORD_COMPILER.md:9`, "exponent-p group") and its evaluator
  were not.
- **p = 3.** The black-box check (§C3(d)) also listed p = 3, c = 2, e > 1 as uncovered. That case
  is covered too, since c = 2 < 3. It is tested below.

## 2. Theorem and proof

**Lemma (prime-power evaluation; proved).** Fix c ≥ 1, a prime p > c, and a power M of p. Let Π be
any straight-line program accepted by the certificate verifier for class c, with target
T ∈ {X+Y, [X,Y]}. Let G be a finite p-group of nilpotency class ≤ c whose exponent divides M, and
let x, y ∈ G. Evaluate Π in G, with each rational power a/b taken as the integer power
a·b^{-1} mod M. The result is x +_L y, respectively [x, y]_L, where (G, +_L, [·,·]_L) is the
Lazard Lie ring of G.

*Proof.*

1. **Free object.** Let Λ be the free nilpotent class-c Lie ring on X, Y over Z_(p), that is,
   L_Z(X,Y)/γ_{c+1} ⊗ Z_(p). The free Lie ring is a free Z-module, with a Hall basis in each
   degree. So Λ is a free Z_(p)-module and embeds in Λ_Q.

   Λ_Q is the space of Lie elements of degree ≤ c in T_Q = Q⟨X,Y⟩/(deg > c). This holds because
   the free Lie algebra embeds in the free associative algebra and both are graded.
2. **The verifier computes in exp(Λ).** On the Lie elements of T_Q, exp is injective, with
   exp(u)·exp(v) = exp(BCH(u,v)) and, by definition, exp(u)^r = exp(r·u). The verifier's `pow` is
   exactly exp(r·log v).

   By induction, every intermediate value is exp(ℓ_i) with ℓ_i ∈ Λ. The degree-k BCH coefficients
   have denominators supported on primes ≤ k ≤ c < p, so BCH(Λ, Λ) ⊆ Λ. Every exponent
   r ∈ Z[1/c!] lies in Z_(p). Acceptance means ℓ_out = T in Λ.
3. **Transport to L.** By the Lazard correspondence, L = Laz⁻¹(G) is a Lie ring on the set G. Its
   filtration is γ_i(G), so it has class ≤ c, and Laz(L) = (L, BCH) = G as groups. This is
   Trappeniers, arXiv:2406.02475v3, Example 2.1 and Theorem 2.3. That theorem restates Lazard 1954
   and Khukhro, *p-Automorphisms of Finite p-Groups*, Ch. 9–10.

   Integer multiples are group powers: BCH(nx, x) = (n+1)x, since nx and x commute. So M·L = 0, L
   is a Z_(p)-module, and Λ is free in the variety of class-≤ c Z_(p)-Lie rings. There is
   therefore a unique Lie homomorphism ψ: Λ → L with X ↦ x and Y ↦ y. Truncated BCH is a Lie
   polynomial with Z_(p) coefficients, so ψ commutes with it and with scalar multiplication by
   r ∈ Z_(p).
4. **Back to group words.** In Laz(L) = G, BCH is the group product. For r = a/b ∈ Z_(p), r·z equals
   (a·b^{-1} mod M)·z, because M·z = 0, and that integer multiple is the group power
   z^{a·b^{-1} mod M}.

   So evaluating Π on (x, y) in G with integer powers produces ψ(ℓ_i) at every step, and the output
   is ψ(T) = x +_L y, respectively [x, y]_L. ∎

This is what the black-box check (§C3, "Human check") left open: there, only the class-2 case had
been checked. The Lemma reduces it to Lazard's correspondence, which the paper already imports,
plus the Hall-basis freeness of free Lie rings. The exactness of the inverse-BCH words for
3 ≤ c < p is no longer an extra assumption.

**Corollary (general-class prime-power compiler; proved, costs counted).**

- **Input.** A black-box p-group G = ⟨g_1, …, g_s⟩ with unique encodings, a multiplication oracle
  and the identity. The class bound c < p is promised, and M = p^a is any known multiple of the
  exponent; M = p^b works for b-bit encodings, at cost log M = b log p. No inverse oracle is needed,
  since x^{-1} = x^{M-1}.
- **Words.** Let (m_+, q_+) and (m_[], q_[]) be the (mul, pow) counts of the class-c certificates
  in the table of §1. They depend only on c.
- **Power, ADD and BRACKET.** One integer power costs ≤ 2·bitlen(M) multiplications. One ADD costs
  ≤ m_+ + 2·bitlen(M)·q_+, and one BRACKET costs ≤ m_[] + 2·bitlen(M)·q_[].
- **Pullback precomputation (classical, once).** Let F = F_{s,c}(Z/M) with its Lyndon (Hall)
  basis, of rank d = Σ_{k≤c} (1/k)Σ_{j|k} μ(j) s^{k/j} ≤ Σ_{k≤c} s^k. Following the standard
  bracketing, the images h_w = π(P_w) need exactly d − s BRACKET words, one per non-generator
  basis element. That is ≤ (d−s)·(m_[] + 2·bitlen(M)·q_[]) multiplications.
- **One evaluation of Φ: (F, ∗) → G.** On coordinates u ∈ (Z/M)^d, Φ(u) = ADD-fold of h_w^{u_w}.
  This costs ≤ d·(2·bitlen(M) + m_+ + 2·bitlen(M)·q_+) = O_c(s^c · log M) multiplications. That is
  polynomial in s and log M at fixed c, and it is the bound O(d·W_c·e log p) of the black-box
  check, §C3(c).
- **Charged extras.**
  - Coefficient arithmetic: the q_+ + q_[] scalars a·b^{-1} mod M are computed once.
  - Compilation is symbolic and depends only on c (≈ 12 s at c = 8 here). There is still no
    uniform-in-c bound.
  - Coherent evaluation: every branch depends only on public data, so Φ is a reversible
    straight-line program. Powers with a quantum exponent u_w are controlled multiplications by
    the classical constants h_w^{2^i}, which is d·bitlen(M) further classical squarings. Bennett
    uncomputation at most doubles the multiplications and needs O(instructions) group registers
    of workspace.
  - No circuit is synthesized here.
- **Conclusion.** Φ is a surjective homomorphism (black-box check §C3(a)), so f∘Φ hides Φ⁻¹(H).

## 3. Exact checks: unitriangular targets

Script `prime_power_lazard_words.py`, output `.json`/`.out`. All checks use exact integer
arithmetic.

- **Ground truth.** Ground truth comes from G ≤ UT_{c+1}(Z/p^e). Its Lie ring is the matrix Lie
  ring: log and exp are truncated series with 1/k! for k ≤ c < p, and the bracket is AB − BA.
  None of this uses BCH words. The words see the matrices only through multiplication.
- **ADD/BRACKET vs matrix exp(A+B), exp([A,B]).** 25 random pairs each at (p,e,c) = (3,2,2),
  (5,2,3), (5,3,4), **(7,2,5), (7,2,6), (11,2,5), (11,2,6)**, (7,3,6), (11,3,6) and (13,2,7). All
  pass, and the top-corner coordinate is nonzero in 24–25 of 25 pairs.
- **Pullback Φ by words vs Φ direct = exp(Σ u_w π(P_w)).** The test also checks Φ(x_i) = g_i and
  Φ(u∗v) = Φ(u)Φ(v), with ∗ computed by BCH in a separate exact model of F_{s,c}(Z/M): the Lyndon
  basis inside the truncated free associative algebra mod M, with triangular coordinate
  extraction. All pass at:

  | (p, e, c, s) | d | multiplications per Φ (mean) | cap |
  |---|---|---|---|
  | (3,2,2,3) | 6 | 148 | 288 |
  | (7,2,5,2) | 14 | 5 964 | 9 212 |
  | (7,2,5,3) | 80 | 33 554 | 52 640 |
  | (7,2,6,2) | 23 | 18 574 | 29 854 |
  | (11,2,5,2) | 14 | 7 270 | 10 472 |
  | (11,2,6,2) | 23 | 23 528 | 33 948 |
  | (11,2,5,3) | 80 | 41 490 | 59 840 |
  | (7,2,5,2), loose M = 7^4 | 14 | 11 072 | 16 772 |

- **Negative controls (must fail, and do).**
  - The mod-p evaluator fails ADD on 10 of 10 pairs at (7,2,5) and breaks the homomorphism.
  - Class-4 words on a class-5 target UT_6(Z/49) fail on 9 of 10 pairs. One random pair has a
    vanishing degree-5 error.
  - The evaluator rejects M not a power of p, c ≥ p, and composite p.

## 4. Exact checks: relatively free GAP groups

`gap_relatively_free_check.g` with `pp_data_p*_c*.g`; outputs in `gap_check_p*_c*.out`.

- **Construction.** G is the largest class-c quotient of C_M ∗ C_M, with M = p^2, built by GAP
  4.15's p-quotient (`EpimorphismPGroup`). The run was taken to stabilization; the p-class bound
  is c+e−1. This group is not given by a Lie chart.
- **Order test.** Lazard predicts that G is the relatively free class-c, exponent-M group, so
  |G| = M^d.
- **Homomorphism test.** GAP evaluates Φ by words only. For 8 sample pairs, it checks
  Φ(u)Φ(v) = Φ(u∗v) and Φ(x_i) = g_i, with u∗v computed in Python. It repeats this on a non-free
  quotient G/N, where N is the normal closure of [g_1,[g_1,g_2]]^p·[g_2,[g_1,g_2]].
- **Results.**

  | (p, c) | d | \|G\| = M^d | class, exponent | hom mod p^e | hom on G/N | mod-p control |
  |---|---|---|---|---|---|---|
  | (7, 5) | 14 | 7^28 ✓ | 5, 49 | true | true (\|G/N\| = 7^14) | false |
  | (11, 5) | 14 | 11^28 ✓ | 5, 121 | true | true | false |
  | (7, 6) | 23 | 7^46 ✓ | 6, 49 | true | true (7^18) | false |
  | (11, 6) | 23 | 11^46 ✓ | 6, 121 | true | true | false |

- **Interpretation.** The relatively free group's order matches Lazard's prediction, and Φ is
  surjective (Lazard). So on these groups Φ is an isomorphism, and the sampled homomorphism test
  checks it. These are finite exact computations. They falsify, they do not prove; the general
  claim rests on §2.

Tests: `test_prime_power_lazard_words.py` gives 21 passed in 13 s (`pytest.out`). It covers Witt
ranks, all the above at reduced sizes, the controls, parameter rejection, and parsing of the
recorded GAP results.

## 5. What now holds, what is missing, gates, text fixes

**Exact statement now holding (proved + exact checks).** For every fixed c, every prime p > c and
every e ≥ 1, take a black-box p-group G of class ≤ c and exponent dividing a known M = p^a. It must
have unique encodings, a multiplication oracle, the identity and s generators. Then the free
pullback Φ: (F_{s,c}(Z/M), ∗) → G can be evaluated by public group words alone:

- precomputation ≤ (d−s)·B_c(M) multiplications;
- per evaluation ≤ d·(2·bitlen(M) + A_c(M)) multiplications;
- A_c(M) = m_+ + 2·bitlen(M)·q_+ and B_c(M) = m_[] + 2·bitlen(M)·q_[], where m and q depend only on c;
- d ≤ Σ_{k≤c} s^k.

So the cost is poly(s, log M) at fixed c. There are zero hiding-oracle queries, no target
coordinates, and no inverse or root oracle.

**Still missing.**
- The reversible circuit is counted, not synthesized.
- The integration into `theorems/universal_lazard_words.py` is not done (the campaign forbids
  editing it here). It is a three-line change: replace `self.p` with an annihilating modulus at
  lines 196, 213 and 225, and widen the contract text.
- The e > 1 route of Prop black-box (ii) still depends on Thm ring-to-field (iii), namely the
  idealizer, the quotient oracle and termination. That belongs to another item.
- The Lemma imports the Lazard correspondence and Hall-basis freeness. It has no Lean proof.
- Costs are not uniform in c.

**Claim gates that must stay false.**
- No speedup, novelty or "Shor-like" claim. This is known Lazard/inverse-BCH machinery;
  Cicalò–de Graaf–Vaughan-Lee compute it effectively.
- No quantum circuit synthesized, and no registry admission.
- All Rees gates stay false: `covers_small_prime_queries` and the human-review items.

**Text fixes for `main.tex`** (listed, not applied):
1. **Prop `prop:black-box`(i).** Replace "The project's word compiler covers exponent $p$ in general
   class, and prime-power exponents only for $c \le 4$ (\file{…CLASS_FOUR_PRIME_POWER_INPUT.md})"
   with:

   "The certified inverse-BCH words of \file{research/UNIVERSAL_LAZARD_WORD_COMPILER.md} are
   identities over $\mathbb{Z}[1/c!]$. Evaluated with each rational power $a/b$ taken as
   $a b^{-1} \bmod p^e$ (or modulo any known power of $p$ annihilating $G$), they compute the
   Lazard addition and bracket in every finite $p$-group of class $\le c<p$, for every $e$: the
   free class-$c$ Lie ring over $\mathbb{Z}_{(p)}$ is free as a module, and Lazard's
   correspondence is functorial (\cite[Thm.~2.3]{Trappeniers2024}). After $d-s$ bracket words of
   precomputation, one evaluation of $\Phi$ costs at most $d(2\lceil\log_2 p^e\rceil + A_c)$ group
   multiplications, where $A_c$ depends only on $c$ and $d \le \sum_{k\le c}s^k$."

   Add the bib entry: S. Trappeniers, *A Lazard correspondence for post-Lie rings and skew braces*,
   arXiv:2406.02475.
2. Optionally state the Lemma of §2, with its four-step proof, as a lemma in Section
   `sec:black-box-groups`.
3. Cite this report and its folder as the exact checks (p = 7, 11; e = 2, 3; c = 5, 6; GAP
   relatively free groups).

## Sources

- S. Trappeniers, [arXiv:2406.02475v3](https://arxiv.org/pdf/2406.02475), §2: Example 2.1,
  Theorem 2.3, and the BCH denominator statement on p. 4. Full text read.
- Cicalò–de Graaf–Vaughan-Lee, *An effective version of the Lazard correspondence*, J. Algebra 352
  (2012), [doi:10.1016/j.jalgebra.2011.11.031](https://doi.org/10.1016/j.jalgebra.2011.11.031).
  Full text not obtained (the repository copy at iris.unitn.it is behind a Cloudflare challenge),
  so it is cited only as prior effective machinery and no detail is imported.

## 6. Fold-in: evaluator fix in `theorems/universal_lazard_words.py` (applied at the parent's request)

The parent session authorized this change. Nothing was committed.

**Diff (summary).** `UniversalLazardWords.__init__` gains `modulus=None`, which defaults to p. It
rejects anything that is not an int power p^e with e ≥ 1; `bool` and float are rejected too. The
module uses `self.modulus` instead of `self.p` in four places:

- `power`: `exponent %= self.modulus`;
- `_evaluate`: `pow(denominator, -1, self.modulus)`;
- `linear_combination`: the coefficient range;
- `operation_caps`: `bitlen(modulus)`.

The class and module docstrings now state the prime-power contract and point to §2. With the
default `modulus=None` the behaviour is identical to before, so no existing caller changes.
`theorems/free_lazard_pullback.py` (exponent-p domain) is untouched.

**New tests** (new file only): `tests/test_universal_lazard_words_prime_power.py`, 17 test cases.
- Matrix ground truth: ADD and BRACKET agree with UT_{c+1}(Z/p^e) matrix log/exp, and stay within
  `operation_caps`, at (p,e,c) = (3,2,2), (5,3,4), (7,2,5), (11,2,5), (7,2,6) and (11,2,6).
- `linear_combination` with coefficients mod 49 is correct.
- A loose annihilator 7^4 works.
- The default modulus gives identical values, caps and call counts.
- The default mod-p evaluation fails on UT_3(Z/9); this is the documented smallest failure.
- Seven bad moduli are rejected.

**Commands and results.**

```
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/test_universal_lazard_words.py tests/test_free_lazard_pullback.py      # before: 41 passed
  ... same + tests/test_universal_lazard_words_prime_power.py                    # after: 58 passed (41 + 17 incl. parametrized)
/opt/anaconda3/bin/python -B -m theorems.universal_lazard_words | cmp - research/reductions/universal_lazard_words.json   # identical
```

These are all the tests that import `universal_lazard_words`. `git status --short` before and
after differs only by ` M theorems/universal_lazard_words.py` and
`?? tests/test_universal_lazard_words_prime_power.py`. No existing test failed or changed
behaviour, so nothing was reverted.

**Still to update elsewhere (not done here).**
- `UNIVERSAL_LAZARD_WORD_COMPILER.md:9` still says "exponent-p group".
- The `main.tex` Prop black-box (i) sentence: see text fix 1 of §5.
