# Rees extension C: black-box free-Lie pullback, proof check

Date: 2026-11-02. AI session (Claude Code), item C of `research/REES_EXTENSIONS_CHECK_BRIEF.md`.
This is not a human review. Nothing here changes a claim gate, the manuscript or a registry.

**Checked:** `docs/papers/rees-hsp/main.tex:589–602` (the Sylow paragraph and Prop
`prop:black-box`), together with the outer-envelope sentence at `main.tex:531`.

**Read:** the brief; `research/STATE.md`; `research/TRAPS.md`; core report
`research/audits/reviews/2026-11-01-rees-core-proof-check.md` §4, §8.2 and §9;
`research/FREE_LAZARD_PULLBACK.md` §§1–5; `research/CLASS_FOUR_PRIME_POWER_INPUT.md` §§1–5;
the `large_prime_outer_envelope` and `copy_only_outer_envelope` blocks of
`research/reductions/rees_hsp_reduction.json`. Anchored greps only: `REES_WHOLE_PROOF_SCOPE_AUDIT.md:225–290`,
`CLASS_THREE_HSP_THEOREM_DRAFT.md:755–792`, `UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md:110–135`,
`UNIVERSAL_LAZARD_WORD_COMPILER.md:1–80`. Full text of Imran–Ivanyos, arXiv:2304.08376v1
(17 Apr 2023), fetched and read: Thm 1, §2.1–2.4, Prop 1 with Algorithm 1, Props 2–3, Thm 2, §6.

**Assumed, and under check elsewhere:** Thm `thm:ring-to-field`, used only for e > 1. Item B
is checking it in a parallel session. Cor `cor:fpt-r` (item A) is **not** used by any conclusion
here. Prop (ii) uses Thm `thm:main` on each F_p section, and needs only class ≤ c for that, not
the rank bound. The core (Thm `thm:main`, steps 1–5) is taken as proved, per the core report §9.

**Scripts:** all in `research/audits/reviews/2026-11-02-rees-extensions/C/`, with each output saved
next to its script as `.out`.

- `metacyclic_cover_check.py`: exact, pure Python, p = 3, 5, 7. Run it with
  `/opt/anaconda3/bin/python research/audits/reviews/2026-11-02-rees-extensions/C/metacyclic_cover_check.py`.
- `omega_agemo_sweep.g`: GAP 4.15, SmallGroups. Run it with
  `printf 'Read("research/audits/reviews/2026-11-02-rees-extensions/C/omega_agemo_sweep.g");\nQUIT;\n' | /opt/anaconda3/envs/qsearch-cas/bin/gap -q`.
- `rank_and_envelope_check.py`: Sage 10.9. Run it with
  `/opt/anaconda3/envs/qsearch-cas/bin/python research/audits/reviews/2026-11-02-rees-extensions/C/rank_and_envelope_check.py`.

No test suite was run. The only files written are this one and `.../C/`.

**Bottom line.** No counterexample. The chain holds for exponent p (e = 1), given Thm main.
For e > 1 it holds conditionally on Thm ring-to-field (iii). Five text gaps remain:

- (C5) The proposition never says how ker Φ is obtained, or what the e > 1 recursion runs on.
  Both are closable at polynomial cost.
- (C5) Part (iii)'s "correct local object" sentence points the reader at an object that the
  valid recursion does not need.
- (C6) The b(b+1) / exponent-147 "black-box outer envelope" is for the acquired-chart route. It
  does not bound the free-pullback route the proposition describes.
- (C1) The Sylow sentence overstates its inputs: |G| is not needed.
- (C2) The p ≤ c Sylows can be covered by Imran–Ivanyos Thm 1, but the text says nothing about them.

---

## C1. Sylow split

**Verdict: Holds**, with a weaker hypothesis than the text: |G| is not needed. The cost is not
charged in the paper.

**Evidence: proof.** For II's matching recipe, see the full text, §2.2 and Prop 1.

- **Decomposition.** A finite nilpotent G is the direct product of its Sylow subgroups G_p,
  each normal and unique. Every subgroup H is nilpotent, so H = ∏_p H_p, where H_p is the unique
  Sylow p-subgroup of H. Since H_p ≤ G_p and H ∩ G_p is a p-group containing H_p, we get
  H_p = H ∩ G_p.
- **Restriction.** For x, y ∈ G_p, we have x⁻¹y ∈ G_p. So f(x) = f(y) ⟺ x⁻¹y ∈ H ⟺
  x⁻¹y ∈ H ∩ G_p, and f restricted to G_p hides H ∩ G_p. Generators of H are then the union of
  generators of the H ∩ G_p. This needs no query beyond f on G_p.
- **Generators of G_p.** Quantum order finding gives o_i = ord(g_i), using the bound 2^ℓ on any
  order. Shor factoring of each o_i follows. Write o_i = p^{α} o_i′; then g_i^{(p)} := g_i^{o_i′}
  (II §2.2), or the CRT idempotent power, is the G_p-component of g_i. The g_i^{(p)} generate G_p,
  because projection onto a direct factor is a homomorphism. If p | |G| then G_p ≠ 1, so some
  g_i^{(p)} ≠ 1 and p | o_i. Hence **the primes of |G| are exactly the primes of the o_i, and
  |G| itself is never needed.** The text at `main.tex:591` ("needs |G| and its factorization")
  asks for more than this.
- **Exponent of G_p.** This is needed to choose Z/p^e in Prop (i). For p > c, G_p has class < p
  and so is regular (P. Hall). In a regular p-group, {x : x^{p^k} = 1} is a subgroup. So
  exp G_p = max_i |g_i^{(p)}|, the largest generator order. This step is argued from a standard
  theorem, not machine-checked. As a consistency check, Ω_1 was a subgroup in all 58 groups of
  the GAP sweep (`omega_agemo_sweep.out`, last column). A loose bound M = p^{⌊ℓ/log₂p⌋} also
  works (`CLASS_FOUR_PRIME_POWER_INPUT.md:13–15`), at the price of a larger cover.
- **Cost.** s order-finding runs and s factorizations of numbers below 2^ℓ, plus O(s·ℓ)
  multiplications for the projections: poly(s, ℓ, log 1/ε), with error charged to a preprocessing
  share. Neither the paper nor the JSON envelope charges this
  (`covers_group_preprocessing_cost = false`). `CLASS_FOUR_PRIME_POWER_INPUT.md` §5 does
  describe it, and allocates a quarter of ε.

**Human check:** confirm the regularity citation, or use the loose M instead.

## C2. Primes p ≤ c: does Imran–Ivanyos Thm 1 cover them?

**Verdict: Holds as a composition**, for the coherent-oracle input of Def `def:input-contract`
(iii). It gives an all-prime, bounded-class, black-box nilpotent HSP algorithm: exact on the
small-prime part, bounded-error overall. It is conditional on the large-prime route (C4/C5).
**Could not decide** for copy-only input: the exact II Thm 1 needs the inverse of the
state-creating oracle. The forward-only copy route (II Prop 3 plus
`REES_COPY_ONLY_OUTER_REDUCTION.md`) is out of scope here.

**Evidence: full-text citation** (arXiv:2304.08376v1).

- **Thm 1, verbatim hypotheses (p. 3–4).** "G is a nilpotent group of class bounded by a
  constant and … the prime factors of |G| are also bounded by a constant", and G is "a
  black-box group with unique encoding of elements by ℓ-bit strings". The conclusion is an exact
  algorithm using poly(ℓ) operations and poly(log|G|) calls to "the subgroup state creating
  oracle and its inverse".
- **Applies to the small-prime part.** Apply it to G_{≤c} := ∏_{p≤c} G_p, or to each G_p
  separately. These are black-box subgroups with the same ℓ-bit unique encoding, generated by
  the projected generators of C1. Their class is ≤ c, a constant, and their primes are ≤ c, a
  constant. Prop 1 (p. 9) also asks for "the prime factors of |G| … given as part of the input";
  C1 supplies them.
- **Oracle interface.** The input is a unitary preparing a purification of Ξ_{G,H} (§2.3,
  Lemma 1: any |ψ⟩ = |G|^{-1/2} Σ_x |x⟩|v(x)⟩ with v constant on left cosets and orthogonal
  across them), plus its inverse.
  - From a coherent U_f: prepare the uniform superposition over G_p, using the exact version
    [II22] of Watrous's method (II §2.2), then apply U_f. The result Σ|x⟩|f(x)⟩ is a
    purification with v(x) = f(x).
  - The inverse is U_f again (an XOR oracle) followed by the inverse preparation.
  - Restriction from G to a Sylow subgroup is II §2.4, though with an f oracle one simply
    queries f on G_p. So each II call costs one f query.
  - This matches `CLASS_FOUR_PRIME_POWER_INPUT.md:195–201`.
- **Exactness and gates (§2.1).** The exact model needs exact QFTs mod the primes. For bounded
  primes, "a constant number of gates are sufficient". Inside a bounded-error composition, the
  exact sub-algorithm is simply used as is. Any approximate gate synthesis is charged to the
  small-prime error share.
- **Cost.** poly(ℓ) with an exponent depending on c: Prop 2 uses T(p,n)^{O(c)}, and Thm 2 gives
  S(p,n) = p^{O(p log² p)} n^{O(p log² p)} with p ≤ c. This is polynomial at fixed c, with
  astronomical constants. Prop 1 makes at most n² HSMC calls for |G_p| = p^n.
- **Composition.** H = ∏_p (H ∩ G_p). The small-prime parts come from II; the p > c parts come
  from Prop `prop:black-box`. A first-error union bound covers the adaptive calls. Nothing in II
  requires the large-prime Sylows to be absent: Thm 1 is simply not invoked on them.
- **Consistency with the core report §8.2.** II for growing primes is conditional on a zero-sum
  method. That is irrelevant here, because only p ≤ c is sent to II.

**Consequence for the text.** The restriction "when every prime divisor of |G| exceeds c"
(`main.tex:591`) can be dropped for coherent-oracle input. The bounded-prime part is then
imported, not new. Gate `covers_small_prime_queries` stays false regardless: the JSON envelope
does not count II's queries or time.

**Human check:** confirm that II's Prop 1 recursion (Kantor–Luks normalizers, §2.2) runs on
G_{≤c} as a black-box subgroup of a larger black box G. I read it as requiring only that the
subgroup's primes be small, which holds.

## C3. The pullback Φ

**(a) Lazard functoriality, surjectivity. Verdict: Holds. Evidence: proof, plus an exact check
(class 2, exponent p²).**

G_p has class c′ ≤ c < p and exponent p^e. So L = log G_p is a Lie ring of class c′ annihilated
by p^e: exp(nx) = exp(x)^n, so additive and group orders agree. F_{s,c} over Z/p^e is free in the
variety of class-≤ c Lie rings annihilated by p^e, so x_i ↦ log g_i extends to a Lie-ring
homomorphism π.

- **Group homomorphism.** BCH is natural under Lie-ring homomorphisms, and c < p. So
  Φ = exp∘π∘log : (F,∗) → G_p is a group homomorphism.
- **Surjectivity.** π(F) is a Lie subring, hence a subgroup by Lazard, and it contains every
  g_i.
- **f∘Φ hides Φ⁻¹(H).** f(Φ(u)) = f(Φ(v)) ⟺ Φ(u)⁻¹Φ(v) = Φ(u⁻¹∗v) ∈ H.
- **Exact check.** The metacyclic group is built from normal forms, not from a Lie chart, and Φ
  is evaluated only through the black-box words `ADD_2(g,h) = g h (g,h)^{-1/2}` and
  `BRACKET_2 = (g,h)`, with ½ inverted mod p². Results: Φ is a homomorphism (exhaustive at
  p = 3, 531441 pairs; 3·10⁵ random pairs at p = 5, 7) and Φ is surjective
  (`metacyclic_cover_check.out`, items 1).

**(b) Rank. Verdict: Holds. Evidence: proof, plus exact comparison with Sage.**

The free Lie ring over Z has a Hall basis whose degree-k part has Witt rank
W(s,k) = (1/k)Σ_{d|k}μ(d)s^{k/d}. Tensoring with Z/p^e gives a free Z/p^e-module of rank
d = Σ_{k≤c} W(s,k) ≤ Σ_{k≤c} s^k = O(s^c). Sage's `LieAlgebra(QQ, s, step=c)` agrees on 7
(s,c) pairs (`rank_and_envelope_check.out`).

- **Note on size.** d is in no way bounded by log_p|G|. For example, d = 40584 at (s,c) = (4,9),
  against the profile's b = 104 bits.

**(c) Coherent evaluation. Verdict: Holds for fixed c. Evidence: argued; exact for c = 2. The
cost is charged in the source note for e = 1, but not in the paper.**

- **Words.** The inverse-BCH words for + and [·,·] are straight-line programs with
  Z[1/c!]-rational powers (`UNIVERSAL_LAZARD_WORD_COMPILER.md:49–53`).
- **Rational powers.** In a finite p-group of class c < p, x ↦ x^n is a bijection for p ∤ n.
  So x^{a/b} = x^{a·b⁻¹ mod M} for any multiple M of the exponent, and the words are valid mod
  p^e.
- **Evaluation.** Precompute the d basis images h_j = Φ(w_j) classically. Each costs at most c−1
  BRACKET_c words. Then Φ(Σc_j w_j) is an ADD_c-fold of h_j^{c_j}.
- **Cost per evaluation:** O(d · W_c · e log p) group multiplications, where W_c, the word length,
  depends only on c ("potentially very badly", per the source). Bennett cleanup of the workspace
  is required. This matches `FREE_LAZARD_PULLBACK.md` §5 at e = 1. The paper's Prop (i) states no
  cost.

**(d) Compiler coverage. Verdict: Holds, with a precise exception.**

- `CLASS_FOUR_PRIME_POWER_INPUT.md:11–19` covers p^e for class ≤ 4 **and p > 4**.
- `UNIVERSAL_LAZARD_WORD_COMPILER.md:9` covers general fixed c only for **exponent p**.
- **The exact regime the project compilers leave uncovered** is e > 1 together with either
  c ≥ 5, or p = 3 (c = 2). This is a limit of the compilers' contracts, not a mathematical gap:
  by (c), the same certificates evaluated mod p^e are valid for all c < p. But no mod-p^e
  universal compiler is implemented or certified. The paper's "only for c ≤ 4" omits p > 4.

**Human check:** the statement that the Z[1/c!] inverse-BCH identities hold in every finite
p-group of class < p. This is standard (Lazard 1954; Khukhro, *p-Automorphisms of Finite
p-Groups*, Ch. 9–10). It was checked here only at class 2.

## C4. Exponent p (e = 1)

**Verdict: Holds**, conditional only on Thm `thm:main`. It uses neither item A nor item B.
**Evidence: proof**, plus the exact check of the pullback identities in C3(a).

- **Input contract.** F = F_{s,c}(F_p) is an explicit Lazard algebra of class c < p (exactly c
  when s ≥ 2), with public structure constants. f∘Φ is a coherent hiding oracle for
  K = Φ⁻¹(H) on (F,∗). So Def `def:input-contract` holds with m = d.
- **Output.** Thm main returns a basis v_1, …, v_k of log K. The exp(v_i) generate K (Lazard,
  as in the core report §7). Φ surjective gives Φ(K) = Φ(Φ⁻¹(H)) = H. So the Φ(exp v_i)
  generate H.
- **Cost:**
  - Thm main at dimension d = Σ_{k≤c} W(s,k), with the label width of f and log(1/ε). The Rees
    cover of F has dimension Σ_k dim γ_k(F) ≤ c·d.
  - Each lifted source uses c queries to f∘Φ, each one f query plus one coherent Φ evaluation
    (C3(c), O(d·W_c·log p) multiplications) and its uncomputation.
  - Total: poly(s^c, log p, label width, log 1/ε) · poly(W_c) at fixed c.
  - The copy-only variant (`FREE_LAZARD_PULLBACK.md` §3) was not re-audited here.
- **Remark.** Acquiring the chart by one abelian HSP (C5) would cut the working dimension from d
  to log_p|G_p| ≤ ℓ. That is a cost choice, not a correctness issue.

## C5. Exponent p^e (e > 1): ker Φ, Φ⁻¹(Ω_1(G)), and the metacyclic example

**Verdict: Gap in the text, closable. No counterexample.** For e > 1 the conclusions depend
on Thm `thm:ring-to-field` (iii) (item B): the normalizer step, the quotient oracle and
termination. They do not depend on its rank bound or on Cor `cor:fpt-r`. **Evidence: proof,
plus exact computation.**

**What the text leaves open.**

- Part (ii) says to run the outer recursion of Thm ring-to-field (iii), but not on which group.
- Part (iii) then says "the correct local object is Φ⁻¹(Ω_1(G)), which needs the relation
  lattice of ker Φ". It does not say how ker Φ is obtained, and charges nothing for it.

**How ker Φ is obtained.** It is an abelian HSP, not a nonabelian one.

- π is Z/p^e-linear, so the map x ↦ Φ(x), viewed on the additive group (F,+) ≅ (Z/p^e)^d, has
  fibres that are exactly the additive cosets of ker π, given unique encoding.
- Standard abelian Fourier sampling over (Z/p^e)^d therefore returns generators of ker π, with
  O(d + log 1/ε) samples. Hermite form then gives the full relation lattice.
- Cost: poly(d, e log p, log 1/ε) coherent Φ evaluations, plus integer normal forms. **Zero f
  queries.** This is the kernel method of `CLASS_FOUR_PRIME_POWER_INPUT.md` §2, applied to the
  free domain.
- Exact check (`metacyclic_cover_check.out`, items 2): ker π is an additive subgroup of order p³,
  and Φ(u) = Φ(v) ⟺ u − v ∈ ker π.

**Two valid e > 1 routes.** Both are conditional on Thm ring-to-field (iii).

- **(R1) Recursion on the cover.** Run Thm ring-to-field (iii) on the explicit ring
  F_{s,c}(Z/p^e) with hidden K = Φ⁻¹(H). Each local problem is the socle of a section of F: an
  F_p Lie algebra of class ≤ c. Thm main applies to it, so Cor fpt-r is not needed. There are at
  most log_p|F| = e·d nontrivial calls, and Φ pushes K forward to H. **Neither ker Φ nor
  Ω_1(G) is ever needed.** The kernel sits inside K and is recovered with it.
- **(R2) Acquire the chart, then drop the cover (recommended).** Find ker π as above, then form
  F/ker π ≅ L(G_p) by Smith form. The brackets are inherited from F's public brackets, so no
  separate bracket acquisition is needed. Run Thm ring-to-field on G_p itself, with
  b = log_p|G_p| ≤ ℓ and local dimensions ≤ ℓ. In this route Ω_1(G) = exp L[p] is public, and
  Φ⁻¹(Ω_1(G)) = {x : px ∈ ker π} is computable but not needed.

**Exact checks on C_{p²} ⋊ C_p**, ⟨a,b | a^{p²} = b^p = 1, bab⁻¹ = a^{1+p}⟩, at p = 3, 5, 7.
GAP identifies the group as SmallGroup(p³, 4) at all three primes, with class 2.

| Claim in `main.tex:600` | Result |
|---|---|
| Ω_1(G) = ⟨a^p, b⟩, order p² | true: 9, 25, 49 |
| Φ(Ω_1(F_{2,2})) = ⟨a^p⟩ | true. It equals ℧_1(G), order p |
| every preimage of b has order p² | true |
| Φ(p x_1) = a^p | true (the earlier claim was correctly withdrawn) |
| Φ⁻¹(Ω_1(G)) = {x : px ∈ log ker Φ} | true, order p⁵ |
| (R1) recovers K and Φ(K) = H for **every** subgroup H | true: 10, 14 and 18 subgroups. At most 3 local calls, counting the final trivial one (bound e·d = 6). K ≤ N always holds, and every socle section is bracket-closed |
| naive Φ(K ∩ F[p]) = H ∩ Ω_1(G) | **fails** for p+2 subgroups (5, 7, 9), as (iii) warns |
| F/ker π has order \|G\|, x_1 and x_2 have orders p² and p | true |

**The phenomenon in (iii) is generic, and has a clean form.** F is a free Z/p^e-module, so
F[p] = p^{e−1}F. Hence Φ(Ω_1(F)) = {Φ(v)^{p^{e−1}}} = ℧_{e−1}(G), the set of p^{e−1}-th powers
(proof). The GAP sweep (`omega_agemo_sweep.out`) covers every group of order 3³–3⁵ and 5³–5⁴
with class < p and exponent > p, 58 groups in all. In 49 of them ℧_{e−1}(G) is strictly smaller
than Ω_1(G), and Ω_1(G) is a subgroup in all 58. So (iii) is correct, but its last two sentences
steer the reader toward an object that route (R1) avoids. As written, they also suggest that ker Φ
is an unpriced obstacle, which it is not.

**§4 falsifier for C.** None found. Both ker Φ and Φ⁻¹(Ω_1(G)) are obtainable at
poly(d, e log p, log 1/ε) cost with no f queries, and route (R1) needs neither. The smallest
instances, at p = 3, 5, 7, were checked exhaustively.

**Human check:** the B3 items that (R1) and (R2) inherit. These are: the idealizer as a linear
congruence over Z/p^e; a coherent quotient oracle on N/K_1, with public Smith-form sections; and
the termination count. That work is item B. My script checks them only on the 42 metacyclic
instances.

## C6. Call cap b(b+1) and outer exponent 3 + Σ d⌈log₂(d+1)⌉

**Verdict: the arithmetic holds; the scope is a gap.** The envelope belongs to a different
route than Prop `prop:black-box`. **Evidence: exact computation, plus a source reading.**

- **Arithmetic** (`rank_and_envelope_check.out`):
  - b(b+1) = 104·105 = 10920, which equals the JSON's `large_prime_call_cap`.
  - 3 + Σ_{d=2}^{9} d⌈log₂(d+1)⌉ = 3 + 144 = 147, which equals
    `large_prime_query_dimension_exponent`. The core's own exponent is 1 + 144 = 145.
  - The derivation is in `REES_WHOLE_PROOF_SCOPE_AUDIT.md:253–285`:
    Q_large ≤ B·c(b+t)∏B_d(b) with B = b(b+1). That is b² from the call cap, b from (b+t), and
    b^{Σ d⌈log₂(d+1)⌉} from the arities, with every local rank replaced by b.
- **Recursion behind b(b+1).** It is the chain-pass scan of `CLASS_THREE_HSP_THEOREM_DRAFT.md:779–784`:
  at most r+1 passes of at most r calls in a Sylow of composition length r. Summing over Sylows
  with Σr_i ≤ b gives Σr_i(r_i+1) ≤ b(b+1) (convexity; checked exhaustively for b ≤ 12 and up to
  4 Sylows). This is a valid, conservative cap. It is consistent with, though looser than:
  - the paper's Thm ring-to-field (iii), "at most b calls" (whole-socle recursion);
  - the artifact's b(b+1)/2 (central-flag scan, `UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md:128–129`).

  The paper uses all three counts, and should name the recursion each one belongs to.
- **Scope gap.** The envelope assumes "all correct local Lie dimensions and lower-central ranks
  are ≤ b" ("acquired-target-chart route", `REES_WHOLE_PROOF_SCOPE_AUDIT.md:271–272`).
  `FREE_LAZARD_PULLBACK.md:146–150` says explicitly that such envelopes "are not bounds for this
  free route".
  - Under Prop `prop:black-box` as written, local dimensions are up to d = Σ W(s,k), and the
    cover has composition length e·d. Neither is bounded by b (e.g. d = 40584 at (s,c) = (4,9)).
  - `main.tex:531` calls it "the separate conditional black-box outer envelope" without naming
    the route.
  - Under route (R2) of C5, local dimensions are again ≤ log_p|G_p|, and the envelope's
    form applies to the large-prime core calls. It does not cover chart acquisition, Φ
    evaluation, preprocessing or the small-prime calls.
- **Flags.** The envelope's own false flags are accurate, and must stay false:
  `covers_small_prime_queries`, `covers_group_preprocessing_cost`, `is_total_gate_bound`,
  `outer_reduction_implemented`.

---

## Surviving statement

**Proposition (black-box nilpotent HSP at fixed class; conditional).**

Fix c ≥ 1. The input is:

- a finite nilpotent group G of class ≤ c, as a black-box group with unique ℓ-bit encodings,
  coherent multiplication, identity, and generators g_1, …, g_s. Inverses are computed as powers.
  Nilpotence and class are promises;
- an arbitrary subgroup H ≤ G;
- access by a coherent oracle U_f with f(x) = f(y) ⟺ x⁻¹y ∈ H.

Then generators of H are found with probability ≥ 1 − ε by the following steps, split into four
error shares.

1. **Preprocessing.** Quantum order finding and factoring of the ord(g_i) give the primes of |G|
   and generators of each G_p by CRT powering. |G| is not needed. Cost poly(s, ℓ, log 1/ε).
   H = ∏_p (H ∩ G_p), and f restricted to G_p hides H ∩ G_p.
2. **Primes p ≤ c.** Use Imran–Ivanyos Thm 1 on ∏_{p≤c} G_p. This step is exact and imported:
   poly(ℓ) operations, with an exponent depending on c, and poly(log|G|) calls. Each call is one
   f query plus an exact uniform-superposition preparation, or its inverse.
3. **Primes p > c, exponent p.** Apply Thm `thm:main` to F_{s,c}(F_p), of dimension
   d = Σ_{k≤c} W(s,k) ≤ Σ_{k≤c} s^k, with oracle f∘Φ. Each query costs one f query plus
   O(d·W_c·log p) group multiplications, with reversible cleanup. Then push forward by Φ.
4. **Primes p > c, exponent p^e, e > 1. Conditional on Thm `thm:ring-to-field` (iii).** The
   evaluation words are taken mod p^e; they are valid for all c < p, but the project's compiler
   covers only c ≤ 4 with p > 4. Then use one of:
   - (R1) the outer recursion on F_{s,c}(Z/p^e), with hidden Φ⁻¹(H ∩ G_p), at most e·d local
     calls, and Thm main on each F_p socle section, of class ≤ c;
   - (R2) one abelian HSP on (F,+) for ker π, with zero f queries and poly(d, e log p, log 1/ε)
     Φ evaluations, then the Smith-form chart F/ker π, then Thm ring-to-field on G_p, with at
     most log_p|G_p| ≤ ℓ local calls of dimension ≤ ℓ.

**Total time.** poly(s^c, ℓ, log p, label width, log 1/ε) at fixed c, with constants that are
astronomical (W_c, the B_d arities and II's S(p,n)). It is bounded-error, not exact.

**Not covered:**

- copy-only input (fresh ρ_H), which needs `REES_COPY_ONLY_OUTER_REDUCTION.md` and II Prop 3,
  and was not checked here;
- growing c;
- non-unique encodings;
- any gate-level total.

## Matching wording

Sylow paragraph (`main.tex:591`), suggested:

> Decomposing G into Sylow subgroups needs only the orders of the generators and their prime
> factorizations (quantum order finding and factoring, charged as preprocessing); |G| itself is
> not needed. The Sylow subgroups for primes p ≤ c are covered by the exact bounded-prime
> algorithm of Imran and Ivanyos [Theorem 1], given the subgroup-state unitary built from f
> and its inverse. The proposition below treats p > c.

Prop `prop:black-box`, suggested changes:

- **(i)** Add the cost "Each evaluation of Φ costs O(d·W_c·e log p) group multiplications
  with reversible cleanup, where d = rank F_{s,c} and W_c depends only on c". Replace the
  compiler sentence with "The project's word compilers cover exponent p in general class, and
  prime-power exponents only for c ≤ 4 and p > 4. The same Z[1/c!] identities hold modulo p^e
  for every c < p, but no mod-p^e compiler is implemented."
- **(ii) for e > 1** "Conditional on Theorem ring-to-field (iii) (not on Corollary fpt-r), either
  run its outer recursion on the explicit ring F_{s,c} over Z/p^e with hidden subgroup
  Φ⁻¹(H), using Theorem main on each F_p socle section (class ≤ c, at most e·d local calls), or
  first recover ker Φ by one abelian hidden-subgroup computation on (F_{s,c}, +) (the map
  x ↦ Φ(x) is constant exactly on additive cosets of ker Φ; no queries to f), form the explicit
  chart F_{s,c}/ker Φ ≅ log G, and apply Theorem ring-to-field to G directly."
- **(iii)** Replace the last two sentences with "In general Φ(Ω_1(F_{s,c})) = ℧_{e−1}(G),
  which can be a proper subgroup of Ω_1(G). Neither route above restricts to Ω_1 of the cover
  and pushes forward. Where Ω_1(G) is wanted, Φ⁻¹(Ω_1(G)) = {x : px ∈ ker Φ} is computable from
  the abelian kernel computation in (ii)."

Line 531: "The separate conditional black-box outer envelope is for the acquired-chart route,
whose local Lie dimensions are at most b; it does not bound the free pullback of
Proposition black-box, whose local dimension is rank F_{s,c}."

No row of Table `tab:main-regimes` should be added for black-box input. If one is wanted, it would
read: "Black-box, unique encoding, coherent f | all primes (p ≤ c via [II, Thm 1]) | as fixed
class, on rank F_{s,c} or on an acquired chart | poly(s^c, ℓ, log p, log 1/ε) total, conditional
on Thm ring-to-field for e > 1".

## Claim gates that must stay false

These are in `research/reductions/rees_hsp_reduction.json`.

- **Top level:** `independent_review` (this is an AI check), `novelty_established` (the
  black-box conversions are standard: Sylow split, II, abelian kernel, Lazard/inverse BCH),
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`,
  `formal_compiler_checked`.
- **`large_prime_outer_envelope`:** `outer_reduction_implemented`, `covers_small_prime_queries`
  (II is valid, but its cost is not counted), `covers_group_preprocessing_cost`,
  `is_total_gate_bound`.
- **`copy_only_outer_envelope`:** `outer_reduction_implemented`, `quantum_receiver_implemented`,
  `general_diagonal_solver_implemented`, `is_total_gate_bound`, `speedup_claim_allowed`.

## Ranked text fixes (listed, not applied)

1. **Prop (ii)–(iii), e > 1** (`main.tex:598–600`). Say what the recursion runs on, either (R1)
   or (R2). Say how ker Φ is obtained (abelian HSP on (F,+), zero f queries) and charge it.
   Replace "the correct local object is Φ⁻¹(Ω_1(G))…" with the identity
   Φ(Ω_1(F)) = ℧_{e−1}(G), and say that neither route needs a socle push-forward. State that
   e > 1 is conditional on Thm ring-to-field (iii) and not on Cor fpt-r.
2. **Line 531.** Tie the b(b+1) / 147 envelope to the acquired-chart route, with local
   dimensions ≤ b. It is not the free pullback: there, d = Σ W(s,k) and the composition length is
   e·d. Name the recursion behind each of the three call counts (b, b(b+1)/2 and b(b+1)).
3. **Line 591, Sylow sentence.** "needs |G| and its factorization" should read "needs the
   generator orders and their factorizations". Add the II Thm 1 composition for p ≤ c, which
   needs the state unitary and its inverse, built from f. Say that the cost is imported and not
   in the envelope.
4. **Prop (i), compiler coverage.** "only for c ≤ 4" should read "only for c ≤ 4 and p > 4".
   Add that this is a limit of the compilers' contracts, not a mathematical one.
5. **Prop (i), cost.** State the Φ-evaluation cost O(d·W_c·e log p) and the bound
   d ≤ Σ_{k≤c} s^k.
6. **Prop (ii), e = 1, optional.** Note that the working dimension is d = rank F_{s,c}, not
   log_p|G|, and that the chart acquisition of fix 1 would reduce it.
7. **Optional.** The exponent of G_p is the largest p-part of the generator orders, because
   groups of class < p are regular.

## What a human reviewer must still check

- **The Lazard / inverse-BCH validity mod p^e for class 3 ≤ c < p** (C3(c)). It was checked
  exactly here only at class 2.
- **The B3 items inherited by e > 1** (C5): the idealizer, the quotient oracle and termination.
  The parallel item-B session is checking them.
- **The II §2.2 normalizer step on a black-box subgroup** (C2).
- **The copy-only variants**, which were not checked here.
