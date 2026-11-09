# Referee report: draft Corollary cor:black-box and input-model paragraph (9 Nov 2026)

Object: `research/audits/reviews/2026-11-08-rees-blackbox-corollary-draft.tex`, parts (A) and (B).
Checked against `docs/papers/rees-hsp/core/main-core.tex` (Definition def:input-contract,
Theorem thm:main, Theorem thm:is-import, Lemma lem:fourier, Section sec:uniform-compilation,
Section sec:proof-main), `docs/papers/rees-hsp/appendix-torsion-blackbox.tex` (lem:tb-words,
lem:tb-evaluation, lem:tb-kernel, the e = 1 "Alternatively" route, lem:tb-chart) and
`docs/papers/rees-hsp/main.tex` (prop:black-box, thm:bb-envelope). This is an independent AI
referee report. It is not human review, and no label in the draft was taken on trust.

## Verdict: MINOR

The mathematics of Corollary cor:black-box is correct. The free pullback, the kernel step, the
chart and the reduction to Theorem thm:main all hold, and the error and cost claims follow,
except that `log p` is missing from the cost (finding 3). Nothing found breaks the result. The
problems are precision and scope: the algorithm's behaviour off the good event is not
specified, the explanation of the public checks points at the wrong failure mode, two
sentences of the scope remark are inaccurate, and the matrix-group paragraph (A)(a) is
narrower than the core's own related-work claim and skips one justification. There is also a
structural issue the draft already flags: the proof depends on lemmas proved only in the full
version.

## What was checked and holds

- **Pullback (item 1).** Exponent p and class below p give p·log G = 0, since x^{*n} = nx. So
  log G is an F_p-Lie algebra of class at most c, and F_{s,c} ⊗ F_p is relatively free in that
  variety. φ is therefore well defined. Its image is a Lie subalgebra containing every log g_i,
  so it is a subgroup containing every g_i, and φ is onto. Φ(u) = Π_+(…, h_d^{u_d}) equals
  exp(Σ u_j φ(w_j)) = exp φ(u) by Lemma tb-evaluation with M = p. Lyndon standard
  factorisation gives h_j = Π_[](h_{j'}, h_{j''}). Inverses are z^{p-1}. Since exp is a
  bijection and encodings are unique, u ↦ enc Φ(u) is constant exactly on the cosets u + K.
- **Samples and error (item 2).** The rank of K^⊥ is m. Unique encodings give p^m ≤ 2^ℓ, so
  m ≤ min(d, ⌊ℓ/log₂ p⌋). Lemma tb-kernel at δ = ε/4 gives sampling failure at most
  p^{m-t} ≤ ε/8 and an approximation error of ε/8, and ⌈log_p(2/δ)⌉ = ⌈log_p(8/ε)⌉. The
  arithmetic is right.
- **Chart (item 3).** The span of the non-pivot standard vectors of an RREF basis of K is a
  complement of K: a vector in the intersection has every pivot coordinate equal to its own
  row coefficient, hence 0. Reducing a bracket by the RREF rows clears the pivot coordinates
  and gives the quotient structure constants. y ↦ φ(ιy) is then a Lie isomorphism
  F_p^m → log G, hence a BCH-group isomorphism, and it equals log E. Since ι(e_a) = w_a, the
  "m precomputed images" are just the h_a, so E costs O_c(m log p) multiplications.
- **Accounting (item 4).** d = Σ W(s,k) ≤ Σ s^k ≤ c·s^c and m log₂ p ≤ ℓ both hold. f is not
  queried before the chart. Each query of f∘E costs one f-query and two coherent
  E-evaluations (compute, query, uncompute). On the good event the chart is the RREF chart of
  K, a deterministic function of K, so applying Theorem thm:main conditionally is legitimate.
  The union bound gives ε/4 + ε/2 < ε.
- **Hypotheses (item 5).** Fixed c, c < p (so p > c), exponent p, p given and unique encoding
  are exactly what Definition def:input-contract and Theorem thm:main need for the acquired
  chart, with oracle model (a).
- **Matrix groups (item 6).** For n ≤ p: (I+N)^p = I + N^p = I; the class is n−1 < p; the log
  series has denominators k ≤ n−1; and the Lie closure equals log G. F_p ⋉ F_p^m embeds for
  p > m: an action A with A^p = I has (A−I)^p = 0, so A is unipotent and is conjugate to an
  upper unitriangular matrix, and (a,v) ↦ [[A^a, v],[0,1]] does the rest.
- **Finite control.** The four runs in `research/audits/reviews/2026-11-08-rees-blackbox-e2e/`
  (heis5_s3, affine5, affine7, free23_5) match the remark's description: three unitriangular
  groups and one free group of class 3 and exponent 5 with hidden coordinates.

## Findings

### 1. MINOR. Scope remark, first sentence: the conditionality statement is wrong

*Location:* rem:black-box-scope, "so it is conditional only on Theorem~\ref{thm:main}, as every
result of this paper is."

*Problem:* Theorem thm:main is proved in the paper, not assumed. The condition is Theorem
thm:is-import (the corollary's own statement says "assume Theorem~\ref{thm:is-import}"). And
not every result of the paper is conditional: Proposition prop:classical-query is
unconditional. The sentence also leaves out that the proof uses Lemmas tb-words,
tb-evaluation and tb-kernel, which the core does not prove (see finding 7).

*Fix:* "so, like Theorem~\ref{thm:main}, it is conditional only on Theorem~\ref{thm:is-import}."
If the full-version lemmas stay, add "and it uses Lemmas … of \fullv".

### 2. MINOR. Kernel step: behaviour on failure is unspecified, and the explanation of the checks is misleading

*Location:* proof, paragraph "Kernel", last two sentences; and the statement's "On the event …
that the chart is correct".

*Problems:*
1. The proof says the two checks "reject" some outputs K′ but never says what the algorithm
   then does: abort, retry or fall back. The finite control retries up to 20 times
   (`kernel_step` in `theorems/rees_blackbox_end_to_end.py`). The proof is one-shot.
2. The statement bounds the queries only on the good event, so no worst-case query bound is
   given. If the algorithm continues on a wrong K′, Theorem thm:main may run on an invalid
   instance, for example when K′ is not an ideal.
3. "They do not detect K′ ⊊ K, so they do not remove the error term ε/4" misidentifies the
   failure modes. With exact transforms every sample lies in K^⊥, so the null space always
   contains K: every ideal-procedure failure is a K′ ⊋ K, and check 1 always detects it.
   K′ ⊊ K, or a K′ incomparable with K, can arise only from the ε/8 approximation error.
   Moreover, a K′ ⊊ K that passes the ideal check is harmless for correctness. F/K′ is then a
   Lie algebra of class at most c, E′ = Φ∘ι′ is a surjective homomorphism onto G,
   f∘E′ hides E′^{-1}(H), and Theorem thm:main still returns a basis whose E′-images generate
   H. Only the dimension, and so the query count, grows.

*Fix:* Specify: if a check fails, or if d − dim K′ > L := ⌊ℓ/log₂ p⌋, then abort (or retry a
fixed number of times). Then state:

- the output is correct with probability at least 1 − ε;
- on every branch the queries number at most c(L+τ)∏_{d=2}^c B_d(L), polynomial in ℓ and
  independent of s (B_d is monotone and g′_d ≤ L);
- on the event K′ = K, the queries number at most Q_q at (m, g_d).

Replace the last sentence of the paragraph by the correct account: the checks detect every
ideal sampling failure; an undetected deviation (K′ ⊊ K) can only come from approximation and
affects only the query count. If the proof keeps no retry, say that the artifact's retry loop
is not part of the analysed algorithm.

### 3. MINOR. Cost claim omits log p

*Location:* statement, "Its other cost is \poly_c(s,\ell,w,\log(1/\eps))"; proof, last
sentence.

*Problem:* The bound log₂ p ≤ ℓ needs G ≠ 1. If every g_i encodes the identity, p is arbitrary
relative to ℓ, while F_p arithmetic, the exponent p−1, and QFT_{F_p} on F_p^d cost poly(log p).
Theorem thm:main's own gate bound also contains log p. Some cost items are also never
mentioned, although each is poly_c(s, log p):

- the Lyndon-basis bracket table of F (Hall rewriting, or the table T_c of Lemma tb-chart,
  Step 0);
- the ideal check (dim K′·d brackets);
- the push-forward of the output basis.

*Fix:* Add log p to the argument list of poly_c, or say "for G ≠ 1, where log₂ p ≤ ℓ" and treat
G = 1 separately: test g_i·g_i = g_i, the unique-encoding identity test. List the three items.

### 4. MINOR. (A)(a): "with p > m" is narrower than needed and than the core's related work

*Location:* (A)(a), last sentence.

*Problem:* The core's related-work paragraph (main-core.tex, around l.182) says the
F_p ⋉ F_p^m instances are covered once p exceeds the class. (A)(a) gives coverage only for
p > m, which excludes most of the range of [IS2015, Cor. 8]: constant class, m unbounded.

*Counterexample:* p = 3, m = 4, A = I + E_{12} + E_{34}. The class is 2 < p but p ≤ m. This
group sits in UT_5(F_3) with n = 5 > p, so (A)(a) does not apply as written. Still, the
truncated matrix log X = M − M²/2 (M = g − I) is a bijection onto a Lie algebra with
exp X · exp Y = exp(X + Y + [X,Y]/2) on the whole group. Exact check (order 243):
`research/audits/reviews/2026-11-08-rees-blackbox-e2e/semidirect_check.py`.

*Fix:* State (a) under the condition that the non-unital associative algebra 𝒜 generated by
the g_i − I satisfies 𝒜^p = 0, with n ≤ p as a sufficient case. This condition can be checked
by linear algebra in poly(n, s, log p). Then G ⊆ I + 𝒜, exp and log truncated below degree p
are inverse bijections, and the BCH identity holds. For F_p ⋉ F_p^m of class c,
𝒜^{c+1} = 0, since (g−I)-products of length k have block form [[P_1⋯P_k, P_1⋯P_{k−1}v],[0,0]].
So the condition covers every p > c. Also say that the unipotent A must first be conjugated
to upper unitriangular form: a flag of kernels of powers of A − I, computable in polynomial
time.

### 5. MINOR. (A)(a): "is the Lazard logarithm" is asserted without argument

*Location:* (A)(a), third sentence.

*Fix:* One sentence suffices. In ℤ_(p)⟨X,Y⟩ modulo degree ≥ n, the truncated exp, log and BCH
series have denominators whose prime factors are at most n−1 < p. Products of n strictly upper
triangular matrices vanish. Hence exp X · exp Y = exp BCH(X,Y) on 𝔫_n(F_p), and by uniqueness
of the Lazard ring structure [Lazard1954; Khukhro Ch. 9–10] the restriction to log G is the
Lazard ring of G. The same argument proves the generalisation in finding 4.

### 6. MINOR. Scope remark: route identification and item (iii)

*Location:* rem:black-box-scope, first sentence and item (iii).

*Problems:*
1. Item (iii) says the full-version composition is "conditional on Schedule~2". But
   thm:bb-envelope (main.tex, the paragraph after its items) and the core's own outlook
   (main-core.tex l.697: "on Schedule~2 (or on Schedule~1 alone, at a larger exponent)") both
   say that with Schedule 1 alone the dependence on Theorem power-sde(ii) disappears. What
   keeps the nilpotent case unclaimed, when every Sylow subgroup for p > c has exponent p, is
   that the core does not treat the Sylow preprocessing (order finding, factoring, AKS) or
   the imported exact algorithm of [II23, Thm 1]. It is not Schedule 2.
2. "The corollary is the e = 1 chart route in the proof of Proposition black-box(ii)" is
   loose. That route uses the chart of (R2), Lemma tb-chart, which is a Y-matrix/Howell-form
   construction with hypothesis k ≥ ⌊ℓ/log₂ p⌋. The draft's t = min(d, ⌊ℓ/log₂ p⌋) + ⌈log_p(8/ε)⌉
   can be smaller: s = 2, c = 2, p = 5, ℓ = 100 gives t = 5 against ⌊ℓ/log₂ p⌋ = 43. The
   draft's own RREF chart needs no such hypothesis and is correct, so this is a description
   problem only.
3. Theorem thm:main also covers coset-copy input (b). The corollary does not, because E^{-1}
   is never computed, and the remark should say so.

*Fix:* For (iii): "with Schedule~1 alone and exponent-p Sylow subgroups it needs, beyond
Theorem~\ref{thm:main}, only the Sylow split and the imported algorithm of
\cite[Theorem~1]{ImranIvanyos2023}; with the combined rule it is also conditional on
Schedule~2; …". For route 1: "a field form of the e = 1 chart route (with an RREF complement
in place of Lemma tb-chart)". Add a restriction (iv): oracle input only.

### 7. MINOR (structural). The core proof depends on full-version lemmas; header label convention

*Location:* proof, "Evaluating Φ" and "Kernel"; corollary header.

*Problem:* The core says no proof depends on the full version, and its Section sec:outlook
says the paper's results are Theorem thm:main and Proposition prop:classical-query. The draft
acknowledges this in its comments, but leaves it unresolved. Lemma tb-kernel also cites Lemma
qft-mod "for odd p", while c = 1, p = 2 is allowed by the hypotheses; there QFT_{F_2} is the
exact Hadamard, so nothing breaks. Separately, the header "[…; AI-checked, pending human
review]" goes against the core convention in Section sec:status that proved statements carry
no label. Only imported Theorem thm:is-import carries one.

*Fix:*
- For e = 1, replace Lemma tb-kernel by four lines from the core: the hiding function gives
  coset states ρ_K; Lemma lem:fourier with the hyperplane count at rank m ≤ min(d, ⌊ℓ/log₂ p⌋)
  bounds the sampling failure; Corollary cor:approx and Lemma lem:hybrid, with Theorem
  uniform-compilation(iii) (any modulus), bound the approximation.
- Either include the short proofs of tb-words and tb-evaluation, about 20 lines at M = p, or
  cite the inverse Hausdorff formulas with a checked locator. The NEEDS-HUMAN-VERIFICATION tag
  on Khukhro stands.
- Drop the header label, or explain why this corollary differs from the convention.

### 8. NIT. Coherence sentence and oracle conventions

*Location:* proof, end of "Evaluating Φ".

*Problem:* "With unique encodings, Φ is computed coherently and its workspace cleaned up by
uncomputation." Bennett cleanup does not need unique encodings. Uniqueness is needed so that
enc∘Φ is constant on cosets, which is the hiding property. Three conventions are also left
unstated: the multiplication oracle's action on strings that are not encodings, which should
be some unitary agreeing on encodings, as the core assumes for U_f before Lemma lem:hybrid;
how the identity encoding used by check 1 is obtained (g_1^p under the promise); and how a
multiplication by a classical constant is controlled (select enc(h) or enc(1) into the y
register). The last two are routine.

*Fix:* Reword the sentence, and add one sentence stating the three conventions.

### 9. NIT and suggestion. The exponent-p promise is checkable given class < p

*Location:* statement, "promised to be a $p$-group of class at most $c<p$ and exponent $p$".

*Observation:* If the class is below p, then G has exponent p if and only if every g_i^p = 1.
The reason: p·log g_i = 0 implies that p kills every bracket monomial, so it kills the Lie
subring they generate, which is log G. With unique encodings this is the test
(g_i^p)·(g_i^p) = g_i^p, at O(s log p) multiplications. The promise could be stated as
"class at most c < p, with exponent p verified by the algorithm (abort otherwise)". This is
optional.

### 10. NIT. (A)(c) power-commutator presentations

The hedge "whenever normal forms can be multiplied in polynomial time" is honest. Two small
additions would help: here s = n is the number of pc generators and ℓ = n⌈log₂ p⌉, so
d = O(n^c); and fixed-class collection, via Hall polynomials or Deep Thought, is the relevant
literature if a cost is ever claimed. No change is required.

## Summary of required changes before the paper pass

The required changes are findings 1, 2, 3 and 6 (wording, specifying failure behaviour, and
log p), and findings 4 and 5 for (A)(a). Finding 7 needs an owner decision: make the core
self-contained for e = 1, or accept a full-version dependence. None of these changes the
corollary's truth. With finding 2 adopted, the statement gets stronger: the probability of a
correct output is unchanged, and the query bound becomes a worst-case bound polynomial in ℓ
and independent of s, with Q_q holding on the good event.
