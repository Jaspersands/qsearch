# Rees native application search (campaign item 12)

2026-11-02. Claude Code session, AI only, with two independent automated
reviewers (Section 7). This is not human review. No claim gate changes,
and `speedup_claim_allowed` stays false.

## 0. Verdict

**No native application survives.** This is a negative result, built from
five pieces:

1. **Classical-input families fail (Section 3).** Every family examined
   presents the hidden subgroup through one of four channels:
   - an explicit linear representation (Lemma A, proved; Luks above the
     Lie range);
   - a field-valued polynomial of degree below p/D_c
     (`NIL3_POLYNOMIAL_HIDING_ATTACK.md`, cited);
   - conjugation inside the group itself (Lemma B, proved);
   - an isomorphism or transporter question (Remark C). That question is
     not an HSP over the p-group, because the standard reduction needs
     G wr Z_2, which is not a p-group for odd p.
   The first three channels have polynomial classical algorithms. The
   classical residual is succinct objects of degree at least p, or opaque
   labels. No motivated family of that kind was found. Cryptographic
   platforms on class-2/3 p-groups fall into the same four channels.
2. **The most natural quantum-input family is already handled by
   published methods (Section 4).** That family is ray stabilizers of
   unknown states under the shift-and-phase groups
   G_e = F_p^n ⋉ Pol_{<=e}. These are the qudit translation and diagonal
   Clifford-hierarchy groups, of class e+1. For phase states they reduce
   to the published Ivanyos–Santha elimination (Section 5 of arXiv
   1503.09016v2). The repo already recorded this kill
   (`POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md`, 10-22 and 10-28), so I
   confirm it rather than claim it.
   New here:
   - (a) the Rees Schedule-1 per-sample arity product on this family equals
     the known fixed-axis IS bound term by term, since
     g_r = dim γ_r = K_r = binom(n+d-r, d-r);
   - (b) a sharper Weil gap, at most (d-2)/sqrt(p) instead of a constant
     2^-r bound;
   - (c) exact state-vector checks of the copy-only line step.
   So Rees gives no advantage here, not even in sufficient bounds. The
   reviewer found a real gap in the line step as first written: a fixed
   direction stalls. The smallest instance is n = 2, d = 2, v = (1,1),
   P = (x_1−x_2)². It is repaired by random directions (Section 4.2).
3. **The reviewer's surviving candidate is also killed (Section 4.4).**
   The candidate is the twisted translation code
   ρ_{U,P} = D_P Π_U D_P†/p^{n−k}. Its hidden data U and P (mod
   U-periodic terms) make it a non-Pauli abelian stabilizer code for
   d ≥ 3, and the line route provably outputs I/p on it. Rees applies,
   with gap ≥ 1 − (d−2)/√p. But the same IS elimination run in an
   n-dimensional register keeps the U^⊥ noise as a linear phase (Lemma D,
   proved), removes P for every η, and leaves Π_U/p^{n−k}. Fourier
   sampling that gives U. Exact checks: (n,p,d) = (2,7,3), (3,7,3),
   (2,13,4).
4. **A tempting general shortcut is false (Section 5).** The idea was:
   "metabelian (so every class ≤ 3) implies known methods, via an abelian
   quotient plus IS Cor 8 on lines". It fails at the quotient step. Tracing
   out the kernel register does not give the coset state of HN/N.
   Fourier-sampling the characters has success probability |H∩G'|/|G'|.
   So class-3 Rees is not reduced to published results by this route.
5. **One residual is left open (Section 6).** It is learning the symmetry
   group, inside a non-Pauli unipotent group, of an unknown quantum state
   that has no further learnable structure. The nearest untested case is
   the code states of subgroups H̃ ≤ G_e that mix diagonal (level-set)
   and twisted-translation parts, or are nonabelian. Its status is
   UNKNOWN, and no motivated family was identified for it. A decoder is
   not the obstacle; the missing piece is a native source of such states.

The STATE row "Rees applications: none survived" stays as it is. Its
reason can be sharpened (Section 8).

## 1. Inputs read, and corpus checks

I read:

- `REES_FULL_CAMPAIGN.md`, `STATE.md`, `TRAPS.md`;
- `2026-10-30-rees-application-selection.md`, whose rejected candidates I
  did not redo;
- `main.tex` §§ `sec:intro` (input contract, lines 156–213),
  `sec:subspace` (603–630) and `sec:classical-landscape` (632–665);
- the notes `NIL3_POLYNOMIAL_HIDING_ATTACK.md`,
  `CLASS_THREE_APPLICATION_AUDIT.md`, `REES_PROJECTIVE_STATE_SOURCE.md`,
  `EXTERIOR_NOISY_PHASE_LEARNING.md`,
  `POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md`,
  `HPGP_COSET_INTERFACE_AUDIT.md`, `BOUNDED_CLASS_METABELIAN_HSP.md` (the
  sections cited), and `2026-10-30-noisy-phase-native-scope.md`.

Primary literature, read as full text:

- Ivanyos–Santha arXiv:1503.09016v2, Def 4, HPGP′, Thm 5, Cor 6, Prop 7,
  Cor 8 and §§4.1, 5 (pdftotext);
- Decker–Ivanyos–Santha–Wocjan arXiv:1107.2189v2, the HPP/HPGP
  definitions, Thm 4, Cor 2, Thm 5, §5.3;
- Qi–Xu–Feng–Li arXiv:2607.15559v1, introduction and related work.

Luks, FOCS 1992, "Computing in solvable matrix groups": the full text
could not be fetched, because the author page's certificate has expired.
Only the abstract was seen, so it is used only where `main.tex` already
imports it, and is labelled *imported*.

Corpus `been-tried` queries were run for these candidates, among others:

- "cubic phase state learning qudit"
- "Clifford hierarchy stabilizer group learning"
- "phase polynomial state symmetry nilpotent group"
- "qudit hypergraph state learning"
- "conjugacy search p-group cryptography"
- "semidirect product key exchange p-group"
- "code equivalence unipotent automorphism"
- "polynomial symmetry unipotent action"
- "phase state learning from copies HPGP Ivanyos Santha"
- "level set states hidden polynomial graph phase states"
- "subspace stabilizer unipotent linear representation Luks"

The registry had no direct hits; the relevant prior work is in the notes
above, which grep found. Literature search (standard and extended) found no
copy-only learner for degree ≥ 3 phase states over F_p^n other than the IS
route below. Qi et al. learn qudit *stabilizer* states, at a cost
exponential in p², which is irrelevant for p growing.

## 2. What a Rees application must supply

By Definition `def:input-contract` and the TRAPS scope guard, a candidate
needs all four of the following:

- **(R1)** An explicit Lazard algebra of fixed class c, with 3 ≤ c < p and
  p growing. Class 2 is handled by Ivanyos–Sanselme–Santha.
- **(R2)** A hidden subgroup H that is not normal, does not contain
  [G,G], and is not of a family covered by IS Cor 8 or DHIS.
- **(R3)** A coherent hiding function, or fresh coset or state copies, that
  is paid and natural.
- **(R4)** No classical algorithm for the original native input, and no
  simpler known quantum algorithm for that input.

Every candidate below fails (R4), or fails (R3) on naturalness.

## 3. Classical-input families

### 3.1 Lemma A: linear representations in the Lie range (proved)

**Lemma A.** Let G = exp(L) be an explicit Lazard group. Let
ρ: G → GL_N(F_p) be a representation with ρ(G) ≤ UT_N(F_p), N ≤ p, given
by the images of a basis. Let W ≤ F_p^N be a subspace; a vector is the
case dim W = 1 with an affine fixed-point condition, given below. Then

```
Stab_G(W) = exp( dρ^{-1}{ y in M : yW ⊆ W } ),   M = log ρ(G),
Stab_G(v) = exp( dρ^{-1}{ y in M : yv = 0 } ),
```

where dρ = log∘ρ∘exp : L → M is F_p-linear and a Lie map. Both stabilizers
are computable by linear algebra in poly(N, m, log p).

*Proof.*

1. N ≤ p gives x^N = 0 for x in n_N(F_p). So the truncated exp and log are
   inverse bijections between n_N(F_p) and UT_N(F_p) (`prop:conjugation`).
   Moreover x lies in F_p[exp x − I] and conversely, with no constant term.
2. Hence for every subspace W: exp(x)W = W ⟺ (exp x − I)W ⊆ W ⟺ xW ⊆ W.
   For a vector: exp(x)v = v ⟺ xv = 0, because exp x − I = x·u(x) with
   u(x) a unipotent polynomial that commutes with x.
3. ρ(G) is a p-subgroup of UT_N with N ≤ p, hence a Lazard group itself.
   Let M be the Lie algebra generated by log ρ(exp e_i). By the Lazard
   correspondence, the subgroup generated by the exp(x_i) is exp of the
   subalgebra generated by the x_i, so M = log ρ(G).
4. A homomorphism of Lazard groups is a Lie homomorphism in log
   coordinates (Lazard 1954; Khukhro, *p-Automorphisms of Finite
   p-Groups*, Ch. 10). So dρ is linear and is determined by its values on
   a basis.
5. Stab_G(W) = ρ^{-1}(Stab_{ρG}(W)), and its log is the preimage of the
   linear space {y : yW ⊆ W}. ∎

Tuples, flags and intersections of finitely many such conditions are
handled the same way. *Exact check:* exhaustive over exp(n_4(F_5)) and a
proper subalgebra, three random W each. `{x : xW ⊆ W}` matched the true
stabilizer pointwise (part 4 of `phase_state_checks.out`).

Above the Lie range (nilpotency index > p), vector and subspace stabilizers
in a p-subgroup of GL_N(F_q) are still polynomial in N and log q. This is
by Luks (FOCS 1992), which `rem:filters` already uses. The present report
labels this *imported* (abstract only), not verified.

**Consequence.** Codes over F_p with a unipotent linear automorphism group
are subspace stabilizers, so Lemma A or Luks applies. The same holds for
flag, vector and module data, and for orbit modules of polynomial
dimension (`rem:filters`(i)). Codes under a p-group of coordinate
permutations are set or subspace stabilizers, handled by Luks and
Kantor's Sylow theorem (`CLASS_THREE_APPLICATION_AUDIT.md`). Integral
lattices: mod-p^k reductions are handled by the ring-to-field theorem plus
Lemma A, and the global step fails by the local–global example in the
10-30 review. None of these satisfies (R4).

### 3.2 Field-valued polynomial hiding functions (cited, not redone)

Suppose f has field values that are polynomials of degree e in the Lie
coordinates, with p > max(c, e·D_c, 2E). Then the right-invariant vector
fields make log H the kernel of a linear system
(`NIL3_POLYNOMIAL_HIDING_ATTACK.md`, Fixed-Class Extension). This covers
any explicit object of polynomial size under an action that is polynomial
of degree below p/D_c. Examples are polynomials, tensors and bilinear
maps under unipotent substitutions, with formal degree in the group
parameter below p/D_c.

### 3.3 Lemma B: conjugation inside the group (proved)

**Lemma B.** For a Lazard group of class c < p, the centralizer is
C_G(exp X) = exp(C_L(X)). Conjugacy search, that is finding y with
y∗X∗(−y) = Y, is solvable in poly(m, log p) by central-series lifting.

*Proof.*

1. In the BCH group, y∗X∗(−y) = e^{ad y}X. This is a Lie identity with
   p-integral coefficients in class < p, and ad_y^c = 0.
2. As in Lemma A, e^{ad y} − 1 = ad_y·u(ad_y) with u invertible and
   commuting. So e^{ad y}X = X ⟺ [y, X] = 0, which is linear in y.
3. For the search, put φ(y) = e^{ad y}X. Suppose y_k satisfies
   φ(y_k) ≡ Y mod γ_{k+1}. Then for z in γ_{k}... more precisely, z
   in L with [z, X] in γ_{k+1}:
   φ(y_k ∗ z) ≡ φ(y_k) + [z, φ(y_k)] mod γ_{k+2}.
   So the correction modulo γ_{k+2} is one linear system in z modulo
   centralizer terms.
4. After c steps either a solution is found, or a linear system is
   inconsistent and no conjugator exists. ∎

**Consequence.** A key-exchange or identification scheme whose hardness is
conjugacy search, or centralizer computation, in an explicitly given
Lazard group of class < p is classically broken. Its HSP content is
C_G(x), a linear subalgebra. This is elementary. It is standard
central-series practice for polycyclic groups, but I do not cite a
theorem number for it.

### 3.4 Remark C: isomorphism questions are not HSPs over the p-group (argued)

The HSP formulation of an orbit or isomorphism question "is w ∈ G·v,
and by which g" uses the group G wr Z_2 = (G×G) ⋊ Z_2, of order 2|G|².
For odd p this is not a p-group, so it lies outside Rees and outside every
p-group HSP method. Within G alone, HSP returns Stab(v), an automorphism
group, never a transporter. A p-group reduction would need a public cyclic
p-orbit of objects v_0, …, v_{p−1}, which no native problem examined here
supplies. This does not rule out an unknown reduction.

### 3.5 Cryptographic constructions on class-2/3 p-groups (argued)

| Platform | What the hidden structure is | Verdict |
|---|---|---|
| Conjugacy and decomposition search in explicit p-groups (Ko–Lee style) | Transporter; its HSP part is the centralizer | Lemma B: classical |
| Automorphism-based schemes (MOR-type) on p-groups | Discrete log in an abelian group, or a linear action on a class-2 group | Abelian HSP (Shor); not Rees |
| Semidirect-product key exchange over p-groups | Linear or affine dynamics, no hidden subgroup | Not an HSP |
| Class-2 p-group isomorphism, i.e. alternating-bilinear-map isometry (ALTEQ/MEDS-type) | Transporter in GL×GL | Remark C: not a p-group HSP. The unipotent-part stabilizer is Lemma A |
| p-group-valued hash or PRF used as f | Opaque labels | Oracle problem, not native (R3) |

The MOR-type and key-exchange rows are summary judgements. I did not read
those specific papers' full texts this pass. They are recorded only as
"no HSP of Rees type found", not as attacks.

### 3.6 What is left on classical input

The classical residual is a succinct object whose orbit map has degree at
least p in the group parameter, and whose orbit module has no polynomial
cap. Examples are iterated maps with T ≥ log₂ p, Legendre-symbol
compositions χ∘Q, and inverses x^{p−2}. When the object is public, the
classical solver reads the structure. For example, Stab(χ∘Q) = Stab(Q) for
unipotent g and non-square Q, by Weil, and Stab(Q) is linear. When it is
hidden, the problem is an oracle problem. The iterated-map p = T residual
of the 10-30 review is the only such case known here, and it lacks
motivation. No new candidate was found.

## 4. Quantum-input family: shift-and-phase groups and phase states

### 4.1 The Rees formulation (proved; overlaps with the 10-22 note §6)

Take G_e = F_p^n ⋉ Pol_{≤e}(F_p^n), with constants included. It has
elements (a, Q), acting by R(a,Q) = D_Q X_a with
(X_a ψ)(x) = ψ(x−a) and (D_Q ψ)(x) = ω^{Q(x)}ψ(x). Its Lie algebra is
F_p^n ⊕ Pol_{≤e} with [a, Q] = ∂_a Q. It has class e+1, exponent p for
p > e+1, and γ_r = Pol_{≤e+1−r}. Note that G_e is **metabelian**.

For |ψ_P⟩ = p^{−n/2}Σ_x ω^{P(x)}|x⟩ with deg P = d = e+1 < p:

- **Ray stabilizer.** H̃ = {(a, Q) : Q(y) = P(y+a) − P(y) + const}. It
  is abelian, contains the scalar centre γ_{e+1}, is non-normal (for
  d ≥ 3 it is not normalized by D_M with M of degree e), and does not
  contain [G,G].
- **Gap.** For g ∉ H̃ the overlap is p^{−n}|Σ_x ω^{R(x)}|, with R
  nonconstant of degree ≤ e. Choose u with R_top(u) ≠ 0. Every line
  x + tu then restricts R to degree exactly deg R. Weil's bound for
  additive character sums (Lidl–Niederreiter, Thm 5.38) gives
  |Σ| ≤ (deg R − 1)p^{n−1/2}, and the sum is 0 when deg R = 1. So
  |overlap| ≤ (d−2)/√p, and γ ≥ 1 − (d−2)/√p. This is sharper than the
  10-22 note's constant bound (1 − (r−1)/p)/2^r.
  *Exact check:* n = 2, p = 7, random cubic P. Exhaustive over G_2 modulo
  scalars found exactly p^n = 49 unit overlaps, one per shift, and the
  largest other overlap was 0.377964 = 7^{−1/2} (part 3).
- **Rees cost.** The projective-state source with the zero-moment design
  (`REES_PROJECTIVE_STATE_SOURCE.md`) plus Schedule 1 gives
  ∏_{r=2}^{d} B_r(g_r) lifted sources per terminal sample, with
  g_r = dim γ_r = binom(n+d−r, d−r). For d = 3 that is
  B_2(n+1)·B_3(1) = 4(n+2)⁴·46656. The total is polynomial in n and log p.

### 4.2 The published competitor (argued; the repo's 10-22/10-28 note, confirmed)

IS §5 (proof of Thm 5) learns hidden η from univariate states
Σ_t ω^{Σ_j t^j (Y_j·η)}|t⟩ with *known*, arbitrary coefficient matrices Y.
The steps are: solve the diagonal equation, shift registers by δ_i t,
measure, recurse on degree, then Fourier-measure to get one linear
equation and substitute. The copy-only multivariate front end is:

1. Take k copies of ψ_P and δ with Σ δ_i^d = 0. Use δ = (1, −1) for odd d;
   in general a Fermat solution with k ≤ d+1 exists by Chevalley–Warning
   and is found by IS Fact 2. Take a direction v; a fixed v is not enough
   (see the stall below). A single copy restricted to a line is already an
   IS degree-d state, so the δ-trick is optional at the first step
   (reviewer).
2. Append |+_t⟩, map |x_i⟩ ↦ |x_i − δ_i t v⟩, and measure z.
3. The outcome z is uniform, and the post-state is the univariate phase
   state with phase r_z(t) = Σ_i P(z_i + δ_i t v). It has no t^d term; its
   coefficients are known linear forms in η; and its t^{d−1} row depends
   on the top form.

This is exactly IS's |ψ_Y⟩ input. IS use the randomness of their y only
to discard |φ_0⟩, so fixed or z-dependent public Y is fine (reviewer,
proved by reading IS §5).

**A fixed direction v stalls (proved; reviewer).** With one v, every
learned functional lies in the span of the D_vP data, so any part of P
that is constant along v is invisible. Smallest instance: n = 2, d = 2,
v = (1,1), P = (x_1 − x_2)². Then P(z + tv) is constant in t, and the
output is the same as for P = 0. **Repair (argued; reviewer):**
- draw a fresh random v for each copy;
- run the recursion modulo the span W of the equations already learned,
  re-reading the top degree each time;
- while W is not everything, some t^j coefficient (j ≥ 1) is a nonzero
  polynomial in (v, z) mod W, so Schwartz–Zippel gives progress with
  probability at least 1 − d/p;
- failures are detectable (the result lies in W), so discard and retry.
  This needs only p > d.

With the repair, IS's recursion recovers P modulo constants. The ray
stabilizer H̃ is unchanged by P ↦ P + (linear), so Rees learns only P
modulo affine terms. IS returns strictly more.

The repo's `EXTERIOR_NOISY_PHASE_LEARNING.md` (r = 1 case, lines 88–137)
already gives this kill. It uses the map x_i = t + u_i and measures all
but one axis j. That is the same mechanism, and it proves the rank
invariant W_{j,r} ⊆ span{b_α : α_j ≥ r} with dim ≤ K_r = binom(n+d−r, d−r).
Its axis map does not suffer the counterexample above for the axes it
uses. But a single axis j is blind to the part of P that does not depend
on x_j, so the axes must vary across trees; the note keeps frame and axis
fixed only within each tree. Read from the note, not re-proved: its sharper
fixed-axis count for D = 3 is B_2(n+1)·B_3(1).

**Arity (proved, IS Thm 3; reviewer).** IS need
N > d^{d² log d}(ℓ+1)^{d log d} variables per diagonal system. With
ℓ = binom(n+d,d) − 1 = Θ(n^d), the plain IS count is about
ℓ·N^{d−1} = n^{O(d³ log d)} copies. That is polynomial for fixed d, and
the fixed-axis count above is far smaller. IS also assume d | p − 1,
without loss of generality.

*Exact checks* (parts 1–2 of `phase_state_checks.out`):

- The line-step identity held in 20/20 random cases for each of
  (n,d,p) = (2,3,7), (3,3,11), (2,4,13), (3,4,13), (2,5,11).
- Full state vectors at (2,3,7) with k = 2, (1,4,13) with k = 3, and
  (1,3,11) with k = 2: outcome probabilities were uniform to 3e−18, and
  the post-measurement states had fidelity 1.000000000000 to the
  predicted univariate states, for every z.

**Cost coincidence (proved, by counting).** The fixed-axis IS envelope is
(N/a)∏_{r=2}^{d} B_r(K_r) with N = binom(n+d,d) − 1. Rees Schedule 1 on
G_{d−1} has ∏ B_r(g_r) per terminal sample, with
g_r = dim Pol_{≤d−r} = K_r. The SDE factors are identical term by term.
The outer factors (N/a rounds, against about dim A terminal samples times
the design and amplification factors) are both polynomial and of the
same order. Rees therefore gives no advantage on this family, not even in
sufficient bounds. These are sufficient counts, not lower bounds.

### 4.3 Verdict for the family

Phase states fail (R4) against a published quantum method plus a
one-step front end. All copy-only learnable states whose symmetry lies in
G_e fail in the same way: once the state is learned, its symmetry group
is a classical explicit-object computation, handled by Section 3. Other
learnable classes are stabilizer states (Allcock et al.; GNW), MPS and
low-degree phase states.

### 4.4 The reviewer's candidate: twisted translation codes ρ_{U,P}

The independent reviewer (Section 7) proposed this family as the natural
Rees target in place of plain ψ_P. It is killed below by a known-method
route. The route is my derivation; its second independent check is in
Section 7.

**Input model.** p odd prime, d fixed with 3 ≤ d < p, a hidden
k-dimensional U ≤ F_p^n, and an unknown P of degree d. The input is IID
copies of

```
ρ_{U,P} = E_{λ ∈ U^⊥} |ψ_{P+λ·x}⟩⟨ψ_{P+λ·x}| = D_P Π_U D_P† / p^{n−k},
```

with Π_U the projector onto U-periodic functions. There is no oracle, no
conjugate copy and no inverse preparation. Equivalently, ρ is the uniform
mixture over cosets c + U of the phase-twisted coset states
p^{−k/2} Σ_{u∈U} ω^{P(c+u)}|c+u⟩ (proved: Π_U is the sum of the coset
projectors). It is the maximally mixed code state of the abelian,
non-Pauli (for d ≥ 3) stabilizer code with stabilizers
X_u-type elements R(u, P(x) − P(x−u)), u ∈ U. Motivation is thin. It is
the simplest non-Pauli twisted stabilizer code. Non-Pauli topological
codes from twisted quantum doubles exist (de la Fuente, Tarantino and
Eisert, Quantum 5, 398 (2021)), but I saw only a search snippet, so no
link to that paper is claimed.

**Stabilizer, identifiable data and gap (proved).**
- The scalar-support stabilizer in G_{d−1} is
  H̃_{U,P} = {(u, P(x) − P(x−u) + c) : u ∈ U}. It is abelian of order
  p^{k+1}, non-normal, and does not contain [G,G]. Proof: D_Q X_u D_P f =
  D_{Q + P(·−u)} f for U-periodic f, and a diagonal unitary acts as a
  scalar on all U-periodic functions only if its phase is constant.
- ρ_{U,P} = ρ_{U,P+R} for every U-periodic R, because D_R commutes with
  Π_U. So the learnable data are U and P modulo U-periodic polynomials,
  which is the same information as H̃.
- For a ∉ U, Tr(ρ R(a,Q)) = 0. For a = u ∈ U, X_u fixes Π_U and
  |Tr(ρ R(u,Q))| = |E_x ω^{R(x)}| with R = Q − P + P(·−u). The Weil
  argument of Section 4.1 then gives γ ≥ 1 − (d−2)/√p.
- *Float check* (part 5 of `phase_state_checks.out`, n = 2, p = 7, d = 3,
  k = 1): exactly p = 7 unit elements over a ∈ U, the largest other value
  0.377964 = 7^{−1/2}, and at most 5.6e−17 for a ∉ U.

So Rees with the projective source applies, at the Section 4.1 cost.

**Routes that fail (proved or float check).**
- Computational-basis outcomes are uniform.
- *Line route.* For a line direction v ∉ U, λ·v is uniform on F_p, and
  the line output of any number of copies is exactly I/p (reviewer,
  proved). Float check, part 5: distance to I/p 2.8e−17 for v ∉ U, and
  purity 1 for v ∈ U. A random v lies in U with probability about
  p^{−(n−k)}.
- *Pauli methods.* The Weyl characteristic function vanishes off a ∈ U.
  On a ∈ U it is an exponential sum of degree d − 1, of order p^{−n/2}
  for generic P (1/7 at n = 2, part 5). Bell difference sampling on
  ρ^{⊗4} gives an exactly uniform a-marginal: float check, mass on U
  0.142857 = 1/p at n = 2, p = 7 (`bell_difference_check.out`).
- *Exterior route.* `EXTERIOR_NOISY_PHASE_LEARNING.md` needs polynomial
  rank r; here r = |U^⊥| = p^{n−k}.

**Route that works.**

*Lemma D (vector-register shift; proved).* Take copies of
ρ_{U,P_1}, …, ρ_{U,P_M} (same U, any P_m) and public δ ∈ F_p^M, not all
zero. Append w ∈ F_p^n in uniform superposition, apply
|x_1, …, x_M, w⟩ ↦ |x_1 − δ_1 w, …, x_M − δ_M w, w⟩, and measure the x
registers, getting z. Then z is uniform, and the post-state is exactly
ρ_{U,P_z} with P_z(w) = Σ_m P_m(z_m + δ_m w).

*Proof.*
1. Fix a pure component, with linear terms λ_m ∈ U^⊥. Its amplitude at
   (z, w) is p^{−n(M+1)/2} ω^{Σ_m (P_m + λ_m·x)(z_m + δ_m w)}.
2. The modulus is the same for every (z, w) and every component, so z is
   uniform and independent of the component.
3. The phase is P_z(w) + μ·w plus a term depending only on (z, λ). That
   term is a global phase of the component and drops out of its
   projector. Here μ = Σ_m δ_m λ_m.
4. Since the λ_m are independent and uniform on U^⊥ and some δ_m ≠ 0, μ
   is uniform on U^⊥. So the mixture is ρ_{U,P_z}. ∎

*Float check* (part 1 of `twisted_code_kill.out`): full state vectors
with the permutation applied literally, at n = 2 for p = 5 and p = 7, for
two copies of one cubic, and for two different quadratics with
δ = (1, 3). The largest deviation was 4.3e−17. Part 4 chains two
stages on state vectors. It runs two cubic → quadratic stages, then
feeds their simulated mixed outputs (spectrally decomposed) into a
second shift with δ′ = (1, 2). At n = 2, p = 5 and p = 7 the largest
deviation from the twice-predicted ρ_{U,P″} was 1.0e−16.

The line route fails because the noise λ·v fills its whole register.
In an n-dimensional register the noise μ·w only covers the U^⊥
directions, and it is exactly the structure that reveals U.

*Elimination (argued from IS §5 and Thm 3; exact bookkeeping check).*
1. Write each intermediate state as ρ_{U, Yη}, where η is the unknown
   coefficient vector of P and Y is a public matrix (Y = I for a fresh
   copy). By Lemma D, a combination gives Y_new = Σ_m T(z_m, δ_m) Y_m,
   with T the public substitution w ↦ z + δw.
2. For j = d, d−1, …, 1, kill degree j for every η. Take children of
   degree ≤ j and choose δ with Σ_m δ_m^j Y_m^{(j)} = 0, where Y^{(j)}
   are the degree-j rows. This is a system of diagonal equations of
   degree j, IS's Section 3 object. At j = d all children equal I, and
   δ = (1, −1) works for odd d. At j = 1 it is linear algebra.
3. The final phase is constant for every η, so the final state is
   Π_U/p^{n−k}. Its Fourier samples are uniform in U^⊥, and O(n) samples
   give U.
4. With U known, measuring x mod U on a fresh copy gives a uniform coset
   c and the pure k-variate phase state of y ↦ P(c, y), whose
   coefficients are public linear forms in η. IS's known-Y elimination
   then recovers P modulo U-periodic polynomials, which gives H̃
   (argued). It must use the random-direction repair of Section 4.2 and
   IS's *adaptive* peeling: learn a part, apply D_{−estimate} to fresh
   copies, and recurse (end of IS §5). D_R commutes with Π_U for
   U-periodic R, so peeling is legitimate here.
   *Non-adaptive collection fails* (second reviewer; exact computation).
   At n = 2, p = 5, d = 3, k = 1, eliminating to degree 1 and
   Fourier-sampling reached rank 5 against the identifiable count
   binom(5,3) − binom(4,3) = 6. The cause is the forced top-level choice
   δ = (s, −s) for odd d: P(z_1 + sw) + P(z_2 − sw) cancels every odd
   homogeneous part, the linear term included. Learning U in step 3 is
   unaffected, because there the goal is to remove η, not to read it.

No nonvanishing condition is needed in step 2: the goal there is to
remove η entirely, not to read it.

*Exact computation* (part 2 of `twisted_code_kill.out`; the
diagonal-equation step uses a capped random search in the null space,
not IS's deterministic solver). For (n, p, d) = (2, 7, 3), (3, 7, 3) and
(2, 13, 4), three runs each, the final Y had zero rows in every degree
≥ 1 exactly over F_p, and the U^⊥ noise survived. Copies per Fourier
sample were 56–70, 140–142 and 1593–1785. Part 3 recovered U exactly from
3n Fourier samples at (n, p, k) = (4, 7, 1) and (5, 11, 2).

**Arity (argued).** Each level-j system has
dim span{Y_m^{(j)}} ≤ N·binom(n+j−1, j) equations, so IS Thm 3 bounds
the children per level by a polynomial for fixed d. The total is
n^{O(d³ log d)} copies per Fourier sample, the same order as Section 4.2.
For d = 3 that is roughly n^{14} (second reviewer; IS Thm 3 needs more than
d^{d log d}(m+1)^{d log d} variables for m equations). That is a sufficient
count, not a lower bound. The script's random null-space search is a check
only. Its cost is exponential in the number of children in general.

**Verdict.** ρ_{U,P} fails (R4): it has a polynomial-copy solution for
fixed d by published elimination plus Lemma D, with no nonabelian HSP.
The smallest instance where the line route fails and this route works is
n = 2, k = 1, d = 3, p = 7. The first reviewer's proposal is refuted as a
candidate. The second review confirmed Lemma D and the bookkeeping, and
added the adaptive-peeling requirement of step 4.

## 5. A false shortcut, recorded so it is not retried

**Tempting claim.** Every metabelian Lazard group (in particular every
class ≤ 3 group, since [γ_2, γ_2] ⊆ γ_4) has a published HSP solution.
The proposed route:

1. get π(H) ≤ G/G' by abelian Fourier sampling of the quotient coset state;
2. get K = H ∩ G' by restricting the oracle;
3. finish each basis line v of π(H) with IS Cor 8 on
   ⟨g_v⟩G'/K ≅ F_p ⋉ F_p^m, where the hidden subgroup has order p and is
   not in the normal factor.

**Failure (proved).** Step 1 does not work. Write g = s(ḡ)·n and trace out
n. The reduced state keeps coherences only between elements with equal
n-coordinate, so it is not ρ_{HG'/G'} (`HPGP_COSET_INTERFACE_AUDIT.md`
§1). Weak Fourier sampling of ρ_H returns a one-dimensional character of
G/G' that is trivial on H with total probability

```
|G/HG'|·|H|/|G| = |H ∩ G'|/|G'|,
```

which is exponentially small when H ∩ G' is small. Steps 2–3 are valid:
restriction to a normal subgroup, and quotient by a known normal K ⊆ H,
preserve coset states, and the line groups meet Cor 8's promise. The open
part is step 1, and that is exactly where the project's unknown-support
instrument and the Rees central descent do their work. This failure says
nothing against Rees, and nothing about the novelty of class 3.

## 6. The residual (UNKNOWN)

The input is fresh copies of an unknown state ρ, possibly mixed and flat,
whose scalar-support stabilizer H̃ is an arbitrary subgroup of an explicit
Lazard group under a linear unitary representation, with a gap γ, and
where ρ has no further structure that a known learner exploits.

The code states of subgroups H̃ ≤ G_e map out what is now known (argued):
- *Twisted translations only* (H̃ a graph over a subspace U): Section
  4.4 kills these.
- *Diagonal only* (H̃ = {D_Q : Q ∈ V}, with a character): the code state
  is the uniform mixture of the basis states of a level set, unchanged
  by D_P. Basis measurements give uniform points of the level set, and V
  is found classically by linear algebra on monomials.
- *Mixed:* translations along U inside a level set Z of V. The shift
  x ↦ x − δw of Lemma D leaves Z, so z is no longer uniform and Lemma D
  does not apply. This case is untested.
- *Nonabelian H̃:* scalar action on the support forces the commutators to
  act trivially there. Those commutators are diagonal, so every
  nonabelian H̃ falls under the mixed case.

So the nearest open targets are the mixed level-set twisted codes, and
generic H̃-invariant states that are not code states. Two facts hold:

- The Section 5 failure means known pieces do not obviously solve this.
- The 10-30 noisy-phase review shows the known-coefficient framework does
  extend to some mixed phase-type sources.

No motivated family was found. Physical symmetric Hamiltonians over qudits
of large prime dimension, with a non-Pauli unipotent symmetry and a gap
promise, would be the natural source, but none was identified. This is
the only direction with an open, non-oracle quantum input. The missing
piece is a native source, not a decoder.

## 7. Independent review

There were two independent automated reviews: AI agents, not human review,
read-only, with no repo writes.

**Review 1: the phase-state kill (Section 4).** Verdict: it holds with
repairs.
1. Fixed or z-dependent public Y is fine in IS §5 (proved by reading the
   section).
2. A fixed line direction stalls. Smallest instance: n = 2, d = 2,
   v = (1,1), P = (x_1−x_2)² (proved). The repair is random directions,
   recursion modulo the learned span, and detectable retries (argued).
   This is now in Section 4.2.
3. Arity is n^{O(d³ log d)} by IS Thm 3 (proved).
4. The Weil gap is correct and tight for the cubic case (proved). Rees
   learns P only modulo affine terms.
5. For d = 2, Gross–Nezami–Walter Bell sampling is the simpler learner.
6. The reviewer proposed ρ_{U,P} as the natural Rees target. That is
   refuted in Section 4.4.

A follow-up question went to this reviewer: does the r = 1 case of
`EXTERIOR_NOISY_PHASE_LEARNING.md` already cover the kill? It got no
answer. I answered it from the note itself: yes, with the fixed-axis
count B_2(n+1)·B_3(1) for D = 3 (Section 4.2).

**Review 2: the twisted-code kill (Section 4.4).** It used its own
scripts, outside the repo. Verdict: ρ_{U,P} fails (R4), subject to one
fix.
1. Lemma D is correct, also for different P_m and some δ_m = 0 (proved).
   The reviewer's own pointwise prediction, which does not use the
   script's substitution matrix, matched to about 1e−16 for mixed degrees
   with δ = (0,1,2), (2,0,0) and (1,4,0). With every δ = 0 the claim
   fails, as it should (distance 0.04).
2. The "for every η" bookkeeping is right, and `subst_matrix` agrees
   with pointwise evaluation (exact).
3. The arity is polynomial for fixed d, about n^{14} for d = 3 (argued,
   IS Thm 3).
4. **The gap it found:** recovering P after U needs IS's adaptive
   peeling. Non-adaptive collection misses the linear term for
   δ = (s, −s); the smallest instance is n = 2, p = 5, d = 3, k = 1
   (exact computation, rank 5 against 6). Section 4.4 step 4 now says
   this. Learning U is unaffected.
5. Identifiability (proved): ρ_{U,P} = ρ_{U,P′} if and only if P − P′ is
   U-periodic.

## 8. Closing statement

**What now holds.**

- *Classical input* (Lemmas A, B proved; Remark C argued; NIL3 cited;
  Luks imported). Suppose an explicit Lazard group of class c < p acts on
  an explicit object through:
  - (i) a linear representation of dimension N ≤ p, or
  - (ii) field-valued polynomials of degree below p/D_c, or
  - (iii) conjugation in G.

  Then the hidden stabilizer is computable classically in time
  polynomial in m, N, the circuit size and log p. Under (i) with N > p
  the same follows from Luks (imported). Orbit and isomorphism questions
  are not p-group HSPs. These are worst-case statements for every
  instance in the stated access model.
- *Quantum input* (argued, relying on IS §5, which is itself a proof
  sketch; exact finite checks only). Copies of ψ_P, deg P ≤ d < p fixed,
  can be learned with n^{O(d³ log d)} copies and poly(n^d, log p) other
  work, with no conjugate copies, oracle or nonabelian HSP. This uses
  random line directions; a fixed direction stalls. The Rees route on
  G_{d−1} has the same SDE arity factors, and it learns less: P modulo
  affine terms.
- *Twisted translation codes* (Lemma D proved; elimination argued from
  IS §5 and Thm 3; exact bookkeeping checks). Take copies of
  ρ_{U,P} = D_P Π_U D_P†/p^{n−k}, with U ≤ F_p^n hidden of any dimension
  k and deg P ≤ d < p fixed. Then U and P modulo U-periodic polynomials,
  and hence the scalar-support stabilizer H̃_{U,P}, are learnable with
  n^{O(d³ log d)} copies per sample and no nonabelian HSP. This holds
  even though every IS line restriction off U outputs I/p.
- So the natural shift-and-phase symmetry families need no Rees. These
  are sufficient upper bounds; no lower bound is claimed.

**Still missing.**
- A motivated native source of unknown states whose symmetry is a
  non-normal subgroup of a fixed-class Lazard group, with the state not
  otherwise learnable. The mixed level-set twisted codes of Section 6
  are the next family to test, first with Lemma D's failure mode
  (z non-uniform off the level set).
- A full-text check of Luks 1992.
- An independent proof that IS §5's sketch is complete for fixed-Y
  inputs.
- A run of Section 4.4's elimination with IS's deterministic Thm 3
  solver in place of the random null-space search. Item 9's solver is
  the natural tool.
- A state-vector run of a full elimination down to Π_U. Two
  consecutive Lemma D stages were simulated (part 4). The full chain
  was checked at the matrix level only.

**Claim gates that must stay false.** `speedup_claim_allowed`, every Rees
novelty, application and outreach gate, and any registry promotion.

**Text fixes for `main.tex`** (listed, not applied):

1. `main.tex:663`. After "No application of the Rees composition is
   known.", add: "The natural quantum-input candidate, the ray stabilizer
   of a degree-d phase state under the shift-and-phase group
   F_p^n ⋉ Pol_{≤d−1}, is learned by the diagonal-equation elimination of
   [IS, §5] after a one-step copy-only front end, with the same SDE arity
   factors. The same holds for the maximally mixed states of twisted
   translation codes D_P Π_U D_P†, with the elimination run in an
   n-dimensional register."
2. `main.tex:638`. Add Lemma A as a one-line statement: "for an explicit
   representation into UT_N(F_p) with N ≤ p, stabilizers of subspaces
   and vectors are exp of linear preimages". It is the representation
   form of `prop:conjugation`.
3. `main.tex:627` (`sec:subspace`, "Two limits apply"). Add: "copy-only
   phase-state families, the first natural instance of this source, are
   already learnable without the Rees receiver
   (POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md)."

**STATE row suggestion** (for the parent to apply): "Rees applications:
none survived. Classical-input families are linear, low-degree,
conjugation, or not p-group HSPs. Phase-state symmetry has a published IS
§5 route with equal SDE factors. Twisted translation codes D_P Π_U D_P†
fall to the same elimination in an n-dimensional register (2026-11-02
application review, §4.4). Open: mixed level-set twisted codes and
unstructured symmetric states, with no motivated family."

## Artifacts

- `2026-11-02-rees-application/phase_state_checks.py`: run with
  `/opt/anaconda3/bin/python -I phase_state_checks.py`, about one minute.
- `2026-11-02-rees-application/phase_state_checks.out`: its output.
  Parts 1–4 cover phase states and Lemma A; part 5 covers ρ_{U,P}.
- `2026-11-02-rees-application/twisted_code_kill.py` and `.out`: the
  Lemma D state-vector check, the exact elimination bookkeeping and the
  recovery of U. Runs in about a minute.
- `2026-11-02-rees-application/bell_difference_check.py` and `.out`:
  Bell difference sampling and the Weyl support of ρ_{U,P} at n = 2,
  p = 7.
