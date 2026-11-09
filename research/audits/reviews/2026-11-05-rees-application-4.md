# Rees application search, fourth pass: Problem S1

2026-11-05. Claude Code session, AI only, not human review. No claim gate
changes: `speedup_claim_allowed` and `novelty_established` stay false.
`main.tex`, the registry JSON, `STATE.md` and the handoff were not touched.
Code and outputs are in `2026-11-05-rees-application-4/`. Literature is
cited from memory, with no network access; every citation not already in
`main.tex` is marked NEEDS HUMAN VERIFICATION.

Rees wording, as the scope guard requires: "proposed fixed-class,
growing-prime polynomial-time composition, pending independent correctness
and priority review".

Tags: [proved] means a full proof is given here. [computed] means an exact
finite check in the code directory; such checks can falsify, not prove
(TRAPS 7). [cited] means imported. [argued] means a sketch, not a proof.
[conjecture] means unproved.

## 0. Verdict

**No family X was found. One barrier theorem is proved, and it moves the
residual.** Problem S1 is §4.1 of the third-pass report. The residual is
the part of S1 not yet known to be classical.

1. **Theorem W (Weil-restriction Lie filter) [proved; computed].** Write
   δ(F) for the *p-weight degree* of F. This is the largest base-p digit
   sum Σ_i s_p(α_i) over the exponent vectors α in the support of F. Let ν
   be the nilpotency index of L on the variables (ν ≤ D ≤ p). Assume
   p > max((ν−1)δ̂, 2δ̂), with a known bound δ(F) ≤ δ̂. Then H = Stab_G(F) is computed
   by a randomized classical algorithm. It uses only evaluations of F at
   points of E^D, where E = F_{p^K} and p^K > Δ. The number of evaluations
   is O(d(d + log 1/ε)(δ̂+1)), with d = dim L, which is polynomial when δ̂
   is polynomially bounded. Here Δ is the formal degree,
   which may be 2^{O(s)}. The algorithm does not use how the circuit is
   built. Part (b): for fixed δ̂ and any p > δ̂, H is computed in time
   polynomial for each fixed δ̂, given Luks's vector-stabilizer theorem.
   - Theorem W covers the following filters in one presentation-independent
     statement: the audit's Frobenius-lift filter, Artin–Schreier and trace
     forms, Hermitian and twisted-sesquilinear forms, linearized (additive)
     polynomials, and twisted classical-group invariants.
   - It also covers Moore forms of r rows when p > max((ν−1)r, 2r).
   - It removes the restriction to matrices over F_p that the audit's
     identical-block lift needed (the Hermitian row of the §2.4 table).
2. **Consequence.** An S1 instance outside known classical reach, and
   outside pre-Rees quantum algorithms, must satisfy all of the following:
   - **p-weight.** The p-weight must be unbounded, and either at least
     p/max(ν−1, 2) or superpolynomial in the input size. Theorem W(a)
     costs (δ̂+1) evaluations per basis element per sample. So for
     superpolynomial p it is polynomial only for polynomially bounded δ̂.
     When p is polynomially bounded, the first condition alone suffices.
   - **D grows.** For D fixed and p polynomial, |G| ≤ p^{D(D−1)/2} is
     polynomial, so brute force over G with a membership test by PIT works.
   - **p grows.** For bounded p the quantum algorithm of FIMSS applies:
     `main.tex` already notes that p must grow for this reason.

   Multivariate public-key maps and IP instances are tuples of polynomials
   of degree ≤ 3. Rees needs c ≥ 3, so p ≥ 5 > 3, and these maps lie
   outside the degree-≥p residual. They are also explicit tensors, so
   `rem:filters`(0) applies for every p (Section 4, X3).
3. **Candidates [computed].** The high-weight families tested were:
   - generic invariants of non-normal pattern (Nakajima) subgroups, X1a and
     X1b, conjugated by a random element of G;
   - single cyclic norms, X1c.

   X1c dies to factorization, to anchored jets at p = 5 and to the orbit
   rank. At D = 4, X1a survives (p = 5 and 7) and X1b survives (p = 5 only;
   skipped at p = 7 for cost) against:
   - the naive Lie method;
   - Theorem W;
   - anchored jets of order ≤ 3 at E- and F_p-anchors;
   - the gradient span;
   - factorization.

   Their H is non-normal and does not contain [G,G]. At D = 4 they die to
   the orbit-module cap (rank 36 and 75). At D = 6 only the orbit rank was
   computed for X1a, at least 600 and unconjugated. So no single instance
   has been shown to pass every filter. X1a and X1b also die in their
   natural presentation, because the circuit exposes the norms, which are
   Moore ratios, and so exposes K. Only an unstructured presentation is
   left. Any hardness it has would be obfuscation-type, none is known, and
   it has no independent motivation.
4. **The abelian-quotient restriction (Lemma Z) [lemma proved; computed].**
   For central Z, H is the kernel of a homomorphism φ: HZ → Z/(Z∩H).
   Evaluating φ(g) means solving g·F = n·F, an abelian transporter in Z.
   So H follows from HZ by one abelian step. But HZ is the stabilizer of
   the Z-orbit of F, an S1-type instance with no succinct circuit known.
   So the restriction is a quantum step inside Rees, and no classical way
   to apply it is known [argued].

Status of S1: **UNKNOWN, unmotivated, not an application**. The residual is
narrowed to unbounded p-weight that is ≥ p/max(ν−1, 2) or superpolynomial.
TRAPS 9 holds: nothing here shows hardness.

## 1. Inputs and contract

Read:
- the third-pass report in full, together with its code;
- `STATE.md` (Rees rows) and `TRAPS.md`;
- `main.tex`: `rem:filters`, the application-3 paragraph, `thm:main`,
  `tab:main-regimes` and the related-work paragraph (FIMSS);
- `SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md` in full;
- the heads of `MOORE_GRADIENT_CLASSICAL_FILTER.md` and
  `POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md`.

The corpus `been-tried` returned nothing relevant for Weil restriction or
p-weight degree, Nakajima or generic invariants, or orbit-product
stabilizers.

S1 is used as stated in the third pass.
- **Input:** an explicit G = exp(L) ≤ UT_D(F_p) with D ≤ p, and a circuit
  for F of formal degree Δ, possibly with Δ ≥ p.
- **Output:** H = {g : F(g^{−1}x) = F(x) formally}.

The scripts act by x ↦ gx. That gives the same stabilizer, since H is a
group. Contract (R1)–(R4) of 11-02 §2 is unchanged:
- (R1) 3 ≤ c < p;
- (R2) H is non-normal, does not contain [G,G], and is not in IS Cor 8 or
  DHIS;
- (R3) the source is paid;
- (R4) no classical algorithm and no simpler quantum one is known.

## 2. Theorem W: Weil-restriction Lie filter

### 2.1 Statement

Let q = p^r, and let L be an F_p-Lie subalgebra of n_D(F_q), given by an
F_p-basis A_1..A_d. Let ν be the nilpotency index of L on F_q^D, so
A^ν = 0 for every A ∈ L. Assume ν ≤ p. Then L has class ≤ ν−1 < p, so
G = exp(L) is a group (Lazard), and every g ∈ G is exp(A) for a unique
A ∈ L. Let F ∈ F_q[x_1..x_D]
have formal degree ≤ Δ, and suppose it can be evaluated at points of any
extension field E ⊇ F_q, for example by a division-free circuit of size s.
Put H = Stab_G(F). (The S1 case is r = 1.)

**Theorem W.**
- **(a) [proved]** Suppose δ(F) ≤ δ̂ and p > max((ν−1)δ̂, 2δ̂), with ν ≤ p. Then
  log H is the kernel of an explicit F_p-linear map on L. A randomized
  classical algorithm outputs an F_p-basis of log H with error ≤ ε. It
  uses (4d + 16 ln(1/ε)) · d · (δ̂+1) evaluations of F at points of E^D,
  where E = F_{p^K} ⊇ F_q and p^K > Δ, plus poly(d, K, D, δ̂, log p)
  arithmetic. This is polynomial when δ̂ is polynomially bounded. It needs no structure of the circuit.
- **(b) [proved, given Luks]** Suppose δ(F) ≤ δ̂ < p with δ̂ fixed. Then H
  is computable in time poly_δ̂(s, D, r, log p, log Δ). This uses Luks's
  vector stabilizer in matrix p-groups [cited: Luks 1992, Thm 3.2(5), as in
  `rem:filters`(0)], and holds for every p > δ̂.

### 2.2 Proof of (a)

**Step 0: coordinates.** Fix E = F_{p^K} ⊇ F_q with p^K > Δ, and an
F_p-basis β_1..β_K of E. Write N = DK, and for u ∈ F_p^{D×K} put
z(u)_i = Σ_j u_{ij}β_j. The map u ↦ z(u) is an F_p-linear bijection
F_p^N → E^D. Every A ∈ Mat_D(F_q) acts F_p-linearly on E^D. Let ρ(A) be the
matrix in Mat_N(F_p) with z(ρ(A)u) = A z(u). Then ρ is an injective
F_p-algebra homomorphism. So ρ(A)^ν = ρ(A^ν) = 0 and
ρ(exp A) = exp ρ(A). For A over F_p, ρ(A) = A ⊗ I_K.

**Step 1: Weil restriction.** For u ∈ F_p^N and e ≥ 0, write
λ_{i,e}(u) = Σ_j u_{ij}β_j^{p^e}. Then

  z(u)_i^{p^e} = Σ_j u_{ij}^{p^e}β_j^{p^e} = λ_{i,e}(u),

because u_{ij} ∈ F_p, and λ_{i,e} is an E-linear form in u. Write
F = Σ_α c_α x^α, and write each exponent in base p as
α_i = Σ_e α_{i,e}p^e with 0 ≤ α_{i,e} < p. Define

  R_F(u) = Σ_α c_α Π_{i,e} λ_{i,e}(u)^{α_{i,e}} ∈ E[u].

Then deg R_F ≤ max_α Σ_{i,e} α_{i,e} = δ(F), and R_F(u) = F(z(u)) for every
u ∈ F_p^N.

**Step 2: reduced polynomials.** A polynomial of total degree < p is
reduced, meaning all its exponents are < p. A reduced polynomial over E that
vanishes on F_p^N is zero. (Induct on the variables: a univariate of degree
< p with p roots is zero.) So two polynomials of degree < p agree as
functions on F_p^N exactly when they are equal formally.

**Step 3: equivariance.** For g ∈ G,
(g·F)(z(u)) = F(g^{−1}z(u)) = R_F(ρ(g)^{−1}u). We claim that g ∈ H if and
only if R_F∘ρ(g)^{−1} = R_F formally.
- g·F − F has degree ≤ Δ < |E| and coefficients in E. So it is zero
  formally if and only if it vanishes on E^D. This is Schwartz–Zippel with
  the full grid E^D.
- That holds if and only if R_F(ρ(g)^{−1}u) = R_F(u) for all u ∈ F_p^N.
- Both sides have degree ≤ δ < p, since composing with a linear map does
  not raise degree. By Step 2 they agree on F_p^N if and only if they are
  equal formally.

**Step 4: Lie criterion.** For A ∈ L put P_A(t,u) = R_F(exp(tρ(A))u). The
matrix exp(tρ(A)) has t-degree ≤ ν−1, so deg_t P_A ≤ (ν−1)δ < p. Put

  R_A(u) := ∂_t P_A(0,u) = ∇R_F(u)·ρ(A)u.

The map A ↦ R_A is F_p-linear. We claim exp(A) ∈ H if and only if R_A = 0.

- (⇒) For s, t ∈ F_p we have exp(sA)exp(tA) = exp((s+t)A). Terms of
  degree ≥ ν vanish, and for n < ν ≤ p,
  Σ_{i+j=n} s^i t^j/(i! j!) = (s+t)^n/n!. So exp(tA) = exp(A)^t ∈ H for
  every t ∈ F_p. By Step 3, applied to g = exp(tA)^{−1},
  P_A(t,u) = R_F(u) formally in u for each t ∈ F_p. Each E[u]-coefficient
  of P_A(t,u) − R_F(u) is a polynomial in t of degree < p with p roots, so
  it is zero. Hence P_A is constant in t, and R_A = 0.
- (⇐) Since ρ(A) commutes with exp(tρ(A)),
  ∂_t P_A(t,u) = R_A(exp(tρ(A))u) = 0. A polynomial in t of degree < p with
  zero derivative is constant, because n·a_n = 0 forces a_n = 0 for
  0 < n < p. So R_F(exp(ρ(A))u) = R_F(u). By Step 3, applied to
  g = exp(A)^{−1}, this gives exp(A)^{−1} ∈ H, hence exp(A) ∈ H.

Every element of G is exp(A) for a unique A ∈ L. Hence
log H = {A ∈ L : R_A = 0}, an F_p-subspace.

**Step 5: evaluation-only access to R_A.** Fix u ∈ F_p^N and put
w = ρ(A)u ∈ F_p^N. The univariate r(σ) := R_F(u + σw) ∈ E[σ] has degree
≤ δ̂. For σ ∈ F_p, Step 1 gives r(σ) = F(z(u) + σ·A z(u)). The nodes
0, 1, …, δ̂ are distinct in F_p because δ̂ < p. So Lagrange interpolation
gives

  R_A(u) = r′(0) = Σ_{σ=0}^{δ̂} c_σ F(z + σAz),

with fixed weights c_σ ∈ F_p and z = z(u). In particular
R_{Σ a_j A_j}(u) = Σ_j a_j R_{A_j}(u). Each R_{A_j}(u) costs δ̂+1
evaluations of F.

**Step 6: sampling.** Draw z uniformly from E^D, which is the same as u
uniform in F_p^N. Each sample gives the E-linear equation
Σ_j a_j R_{A_j}(u) = 0 in the unknowns a ∈ F_p^d, that is, K F_p-linear
equations. Let V_t be the solution space after t samples.
- V_t ⊇ log H always.
- Suppose V_t ≠ log H, and pick a ∈ V_t \ log H. Then R_A is nonzero of
  degree ≤ δ̂.
- Schwartz–Zippel over the subset F_p ⊂ E gives
  Pr_u[R_A(u) ≠ 0] ≥ 1 − δ̂/p ≥ 1/2. When that happens, a ∉ V_{t+1}, so the
  dimension drops.
- d drops suffice. Until V_t = log H, the number of drops stochastically
  dominates Bin(T, 1/2). With T = 4d + 16 ln(1/ε), the Chernoff lower tail
  gives Pr[fewer than d drops] ≤ exp(−(d+8L)²/(4(d+4L))) ≤ ε², where
  L = ln(1/ε).

**Step 7: output.** Return a basis of V_T = log H. By the subgroup form
of the Lazard correspondence, log H is a Lie subalgebra, and the
exponentials of a basis of it generate H. Step 4 alone gives
H = exp(log H) only as a set. ∎

*Remarks.*
- **The promise.** If δ(F) > δ̂, nothing is guaranteed: the conjugated X1a
  and X1b controls return dimension 0, while the true value is 2 or 3.
  Containment of the output in H can always be checked by PIT. The
  promise can be met syntactically:
  - weight(f+g) ≤ max;
  - weight(fg) ≤ weight f + weight g;
  - weight(f^{p^e}) = weight f, even with F_q coefficients, because
    p^e·α_i has the same digit sum as α_i;
  - weight(f^n) ≤ s_p(n)·weight f.

  So a circuit whose power gates are marked gives δ̂ gate by gate. The
  weight is G-invariant, since g acts on each x_i^{p^e} by a weight-1
  form and carries only lower digit sums.
- **Only ν matters.** The hypothesis uses the nilpotency index ν, not the
  number of variables. Block-diagonal actions on many variables keep ν
  small.
- **Where the Lie guard went.** This is the audit's §3 Lie method applied
  to R_F instead of F. The guard p > (D−1)Δ, on the formal degree, becomes
  p > (ν−1)δ, on the p-weight. The Frobenius behaviour that breaks the
  naive method (x^p is F_p-linear) is absorbed by the Weil restriction.

### 2.3 Proof of (b)

Since δ̂ < p, R_F is reduced. Its coefficients come from the values of
u ↦ F(z(u)) on the simplex grid
S = {u ∈ {0..δ̂}^N : Σu ≤ δ̂}. This grid is unisolvent for degree ≤ δ̂
when the nodes are distinct [standard: Newton interpolation on the
principal lattice]. That costs C(N+δ̂, δ̂) evaluations, which is polynomial
for fixed δ̂.

G acts on E[u]_{≤δ̂} by π(g): P ↦ P∘ρ(g)^{−1}. This is an explicit
F_p-representation of dimension K·C(N+δ̂, δ̂), and it is faithful for
δ̂ ≥ 1, since its degree-1 part is the dual of ρ. By Step 3,
H = Stab_{π(G)}(R_F), a vector stabilizer in a matrix p-group, which Luks
computes in polynomial time [cited]. ∎

### 2.4 What Theorem W subsumes (weights) [proved by inspection]

Every product of k forms ℓ^{p^e} has p-weight ≤ k. So:

| Family | δ(F) | Covered by |
|---|---|---|
| Moore form of r rows | r | W(a) if p > max((ν−1)r, 2r); the Moore gradient filter has no guard |
| Mixed Frobenius lift of the audit (§4), syntactic lifted degree δ_syn | ≤ δ_syn | W(a), with no exposed Frobenius gates needed |
| Hermitian / twisted sesquilinear Σ a_ij x_i^{p^k} x_j, coefficients in F_q | 2 | W(a) over F_q (closes the audit's "identical-block" gap) |
| Artin–Schreier / trace Q(ℓ^p − ℓ, Tr ℓ, …) | ≤ deg Q | W(a) or W(b) |
| Linearized (additive) polynomials and products of k of them | ≤ k | W |
| Twisted classical-group invariants B(x, x^{p^k}) (Carlisle–Kropholler type) | 2 | W |
| Quadratic or cubic maps (HFE, UOV, Rainbow, IP) | ≤ 3 | W(b) or `rem:filters`(0) |
| Orbit products N_K(ℓ) with \|Kℓ\| = p^a | a(p−1)+1 when Kℓ is an affine subspace; can be larger otherwise (referee: 13 for a non-affine orbit of size 25 at p = 5) | **not** covered |
| Dickson invariants c_{D,i} | D(p−1) (referee, checked for D = 2, 3 at p = 3, 5) | not covered (but GL_D(F_p)-invariant) |
| Generic invariants Q(N_1, …) of a non-normal Nakajima group | ≥ p | **not** covered |

### 2.5 Exact checks [computed]

`weil_lie_filter.py` produces `weil_lie_filter.out` (≈4 min). It compares
the naive Lie method, Theorem W and brute force over all of G, using
evaluation at 3 random points of E^D. The cases are:
- the two audit controls, F = x_1^p x_2 − x_1x_2^p (D = 2) and
  F = x^p z + x z^p − 2y y^p (UT_3), at p = 5 and 7;
- 10 planted families F = Q(x, x^p), with Q invariant under a non-normal
  subgroup K of the 4-dimensional class-3 group
  L = ⟨E12+E34, E23, E13−E24, E14⟩ ≤ UT_4, for p = 7, 11, 13 and
  δ = 2, 3, 4. The formal degree is up to 52.

Results:
- **Inside the hypothesis: W is correct in 14 of 14 cases, and naive Lie in
  0 of 14.**
- Outside it, on the audit's UT_4(F_5) cubic (degree 3 < p, but
  3·3 ≥ 5), both are wrong. Brute force gives H = 1, while W and naive
  Lie each give dimension 1.

`weil_lie_filter.py` takes d + 6 sample points (the other scripts take
10–12). Each gives K F_p-equations, which is
more than the proof's bound requires in practice; the proof's T is not
what was run.

`weil_lie_twisted.py` produces `weil_lie_twisted.out`. It covers:
- **F_q coefficients:** G = UT_3(F_25) and UT_3(F_49) as F_p-groups of
  dimension 6, with F = a_0 M(x_0,x_2) + a_1 M(x_1,x_2) + a_2 x_2^{p+1}
  and a_i ∈ F_{p^2}, where M(u,v) = u^p v − u v^p. Its symmetries exist
  only for F_p-multiples.
- **Moore forms:** r = 3 rows under the 4-dimensional L, at p = 11 and 13.

Results:
- F_q coefficients: brute force gives |H| = 25 at p = 5 and |H| = 49 at
  p = 7, in each case the 2-dimensional F_p-subspace ⟨E02, E12⟩. W matches
  both.
- Moore forms: brute force gives |H| = 11^3 and 13^3, the stabilizer of
  W = ⟨x_0, x_2, x_3⟩. W matches both.

Coverage caveats from the referee: the planted cases in
`weil_lie_filter.py` use the coordinate basis and an unconjugated K, and
only ⟨a+b⟩ is not aligned with it. The referee's own test was
independent: random bases, F_q coefficients and planted Moore-type
invariants at p = 5, 7 and 25, 9 cases in all. W matched brute force in all
9, with a proper nontrivial H in 3 of them.

## 3. Where the residual lies

Combining Theorem W with the known filters, an S1 instance can be outside
known classical reach, and outside pre-Rees quantum algorithms (the
"p grows" item uses FIMSS, which is quantum), only if every item below
holds.

- **p grows.** For bounded p the group has bounded exponent and bounded
  derived length, so the quantum algorithm of FIMSS solves the HSP. `main.tex` already notes, in
  its related work, that its exponent p grows for this reason [cited in
  `main.tex`].
- **p-weight.** δ(F) is unbounded (Theorem W(b)), and either
  δ(F) ≥ p/max(ν−1, 2) or δ(F) is superpolynomial in the input size
  (Theorem W(a) costs δ̂+1 evaluations per basis element per sample).
- **D grows.** For D fixed and p polynomially bounded,
  |G| ≤ p^{D(D−1)/2} is polynomial, so brute force over G with a
  membership test by PIT works. The case of D fixed and p superpolynomial
  is open. There m is fixed, and it is UNKNOWN whether pre-Rees quantum
  algorithms already cover fixed-dimension Lazard groups.
- **H.** It is non-normal and does not contain [G,G], by (R2).
- **The other filters.** Anchored jets, orbit-module rank, the Moore
  recognizer, tensor trains and factorization must all fail.
- **The circuit.** It must not expose H (Section 6).

## 4. Candidate families

Setup: G = UT_4(F_p) with x ↦ gx. Each instance is conjugated by a random
g_0 ∈ G, so H = g_0^{−1}Kg_0 is not aligned with coordinates. The Lie-type
filters use a random basis of L. A first, superseded run without the
conjugation had W(δ̂ = 1) "succeed" spuriously on X1a and X1b, and that
output was overwritten. The basis was aligned with the pattern group, and
the finite difference F((I+A)z) − F(z) vanishes there. The artifact is
now removed. In the same run the random ℓ of X1c happened to have
ℓ_0 = ℓ_1 = 0, which made F G-invariant; the script now forces ℓ_0 ≠ 0.

`candidate_filters.py` writes `candidate_filters_p5.out`,
`candidate_filters_p7.out` and `candidate_filters_blocks.out`.

**X1a: generic invariant of a pattern group.**
K = ⟨x_0 ↦ x_0 + a x_1, x_2 ↦ x_2 + b x_3⟩ ≅ F_p^2. Its invariant ring is
F_p[N_0, x_1, N_2, x_3] (Nakajima), with N_0 = x_0^p − x_0x_1^{p−1}, and
F = Q(N_0, x_1, N_2, x_3) with Q random quadratic.

*Motivation.* "Recover the group from a generic invariant" is an inverse
problem of modular invariant theory. It is weak: we know of no source that
produces such F without the norms.

**X1b: UT_3 block.** K = UT_3 pattern on (x_0, x_1, x_2), of order p^3,
with F = Q(N_0, N_1, x_2, x_3), where N_0 = Π_{a,b}(x_0 + a x_1 + b x_2) is
a Moore ratio of degree p^2.

**X1c: single cyclic norm.**
F = Π_{t∈F_p} ℓ(exp(tA)x), with A = E01 + E12 + E23 and ℓ_0 ≠ 0.

Results at p = 5 [computed]:

| Filter | X1a | X1b | X1c |
|---|---|---|---|
| \|H\|, H = K? | 25, yes | 125, yes | 5, yes |
| H normal / H ⊇ [G,G] | no / no | no / no | no / no |
| formal degree, p-weight | 10, 10 | 50, 10 | 5, 5 |
| naive Lie | wrong (dim 0) | wrong (0) | wrong (0) |
| Theorem W, δ̂ = 1 (outside hypothesis) | wrong (0) | wrong (0) | wrong (0) |
| gradient span dim W_F | 4 (full) | 4 | 4 |
| anchored jets ≤ 3, \|K_jet\| at α ∈ E / α ∈ F_p | 625 / 625 | 3125 / 3125 | **5 / 5 (= H)** |
| factorization | irreducible | irreducible | **5 linear factors** |
| orbit-module rank (cap filter) | **36** | **75** | 42 (rank of 700 sampled orbit points) |
| Lemma Z: \|H∩Z\|, \|HZ\| = \|H\|\|Z\|/\|H∩Z\| | 1, 125 ✓ | 1, 625 ✓ | 1, 25 ✓ |

At p = 7 [computed; X1b skipped for cost, orbit rank not computed;
membership labels use 2 points]: the two-point labels collide slightly,
since the reported X1c orbit size is 16805 and not |G|/|H| = 16807. So the
p = 7 numbers come from a marginal identity test. |H| and the filter
verdicts are consistent with p = 5.
- **X1a.** |H| = 49 = |K|, non-normal, H ⊉ [G,G], weight 14.
  - Naive Lie and W (δ̂ = 2) are wrong (dimension 0).
  - Anchored jets give |K_jet| = 2401 at both anchors.
  - F is irreducible.
  - Lemma Z: |HZ| = 343 ✓.
- **X1c.** |H| = 7 = |K|.
  - Naive Lie and W are wrong.
  - **Anchored jets give only |K_jet| = 49, so they do not determine H at
    p = 7.**
  - F has 7 linear factors.
  - Lemma Z ✓.

**Orbit-rank scaling for X1a with more blocks** (pattern blocks
{(2i, 2i+1)} in UT_{2b}, p = 5, rank from random g):
- b = 2 (D = 4): 36;
- b = 3 (D = 6): ≥ 600, saturating all 600 sampled rows.

So the rank cap fails as D grows. This is evidence at two sizes, not a
growth law.

**How each candidate died.**
- **X1c.** It dies in several ways:
  - factorization gives the p linear factors, at both primes;
  - anchored 2- and 3-jets give H exactly at p = 5, but only an upper
    bound of index 7 at p = 7;
  - the orbit rank is small at p = 5.
  - [argued] For p > (ν−1)^2, the factor set lies on the polynomial curve
    t ↦ ℓexp(tA). A unipotent g that preserves the set preserves the
    curve, and reparametrizes it by t ↦ t + β. So H = ⟨exp A⟩·C_G, where
    C_G is the pointwise stabilizer of span{ℓA^j}, computable by linear
    algebra.
  - For p superpolynomial the natural circuit is a resultant
    Res_t(t^p − t, ℓ(exp(tA)x)), which exposes ℓ and A.
- **X1a, X1b.** At D = 4 they die only to the orbit-module cap. That is
  expected: fixed D is dense-polynomial anyway. At D = 6 X1a passes every
  filter computed here at D = 6, but only the orbit rank was computed
  there. The other filters and H itself were computed only at D = 4. Both die in
  their natural presentation. The circuit computes the norms N_i as Moore
  ratios M(V_i ∪ x_i)/M(V_i). That exposes the subspaces V_i. Then
  - K = ∩_i Stab(x_i + V_i) is a set of subspace and affine-subspace
    stabilizers, solved by linear algebra (Lemma E style);
  - and H = K for generic Q (computed at D = 4).

  Only an unstructured circuit for the same F survives. That is an
  obfuscation hypothesis, not a natural input (TRAPS 3, and the audit's
  "reject hidden-H-generated invariant circuits").

**Families examined without new code, and how they died.**
- **X3: multivariate public-key maps (HFE, UOV, Rainbow) and IP
  (Patarin).**
  - Their components have degree 2 (3 for some variants) over the base
    field; HFE's degree q^i + q^j is in the extension-field variable. They
    are tuples of polynomials, not a single F.
  - Rees needs c ≥ 3, hence p ≥ 5 > 3. So these maps lie outside the
    degree-≥p residual of S1 (S1 itself allows any Δ).
  - They are also explicit tensors of dimension O(D^3), so
    `rem:filters`(0) applies for every p.
  - Their known attacks target a transporter (IP), a MinRank problem
    (Kipnis–Shamir) or a rank structure (Beullens), not a stabilizer in a
    unipotent group. Their stabilizers lie in GL × GL. [proved for the
    degree argument; attack descriptions cited from memory, NEEDS HUMAN
    VERIFICATION]
- **X4: Deligne–Lusztig, Hermitian, Suzuki and Ree curves, and
  Artin–Schreier big actions.** For these the Sylow p-subgroups of the
  automorphism groups are as follows:
  - Hermitian curve (odd q): class 2, so ISS [cited from memory, NEEDS
    HUMAN VERIFICATION, as are the next three items];
  - Suzuki (p = 2): violates c < p;
  - Ree (p = 3, class 3): violates c < p;
  - Lehr–Matignon big actions: class ≤ 2 as recalled [cited from memory,
    NEEDS HUMAN VERIFICATION];
  - p fixed in each family: FIMSS.

  Hermitian hypersurfaces Σ x_i^{p+1} over F_{p^2} have unitary Sylow
  groups of class about n−1 < p [from memory, NEEDS HUMAN VERIFICATION],
  but the form has p-weight 2. So W(a) over
  F_{p^2} applies when p > 2(n−1).
- **X5: codes.**
  - Explicit codes are subspace stabilizers (`rem:filters`(0), Luks).
  - Succinct codes built from linearized polynomials (Gabidulin), traces
    or subfield subcodes have weight-1 or weight-2 evaluation maps, so
    Theorem W applies at the polynomial level.
  - A Reed–Muller codeword is a reduced polynomial of degree r, so its
    weight is r, and W applies when p > (ν−1)r.
  - A random codeword has H = 1, which anchored jets can certify. We found
    no motivation for a codeword's unipotent symmetry.
- **X6: Lang-map polynomials.** The entries of adj(X)·c·X^{(p)} have
  p-weight D. Their stabilizer under left multiplication is a centralizer
  of c, given by Lemma E of the third pass, and W also applies.
- **X7: transfers Tr_K(f) = Σ_{k∈K} k·f.**
  Tr_K = Π_i(τ_i − 1)^{p−1} in F_p[K], so a circuit costs poly(p, a, s)
  and names the τ_i, which exposes K. For p superpolynomial even one level
  needs the coefficient [t^{p−1}] of a circuit polynomial in t. Extracting
  a coefficient of a univariate circuit of exponential degree is
  #P-hard-flavoured (subset-sum counting), so no natural succinct circuit
  is available. [argued]
- **X8: Dickson-padded composites F = Q(low-weight invariants, c_{D,i}).**
  The c_{D,i} are GL_D(F_p)-invariant, and they are constant (0 or −1) at
  points z ∈ F_{p^ℓ}^D whose coordinates span F_{p^ℓ}, for ℓ ≤ D. This is
  because Π_v(T − ⟨v, z⟩) = (T^{p^ℓ} − T)^{p^{D−ℓ}}. Restricting there
  replaces them by constants, so H ⊆ Stab(F′) for a low-weight F′, which
  Theorem W can treat if p^ℓ exceeds deg F′. This is an upper-bound
  filter only. [argued]

## 5. The abelian-quotient restriction

**Lemma Z [proved].** Let N ⊴ G, H = Stab_G(F), and let S be the setwise
stabilizer of the orbit N·F. Then:
- (i) S = HN, and H ∩ N = Stab_N(F).
- (ii) Suppose moreover that N is central. Then φ: S → N/(N∩H) is a
  well-defined homomorphism, where φ(g) is the class of the n with
  g·F = n·F. Its kernel is H. In particular H ⊴ HN.

*Proof.*
- (i) g ∈ S ⟺ g·F = n·F for some n ⟺ n^{−1}g ∈ H ⟺ g ∈ NH = HN.
- (ii) Well-defined: n·F = n′·F gives n^{−1}n′ ∈ N∩H. Homomorphism: if
  g·F = n·F and g′·F = n′·F, then gg′·F = g·(n′·F) = n′·(g·F) = n′n·F,
  because n′ is central. Kernel: φ(g) = 1 ⟺ g·F = F. ∎

Check [computed]: |HZ| = |H||Z|/|H∩Z| for Z = Z(UT_4) in all five
recorded instances (X1a, X1b and X1c at p = 5; X1a and X1c at p = 7).

What it means. Given HZ, H costs one abelian step per generator. That step
is quantumly an abelian HSP on Z × Z_p: f(z, t) = z·g^t·F hides
{(z,t) : z·n_g^t ∈ Z∩H}. Classically it is an abelian transporter, that is,
a hidden shift in Z.

HZ itself is the stabilizer of the Z-orbit of F. Representing that orbit by
a polynomial needs a norm or the symmetric functions over |Z : Z∩H|
conjugates. For a cyclic Z of order p:
- the resultant trick needs t-degree ≪ p;
- deg_t F(exp(tA)x) can be (ν−1)Δ ≥ p.

So no succinct circuit is known. The same holds for H[G,G], via the
[G,G]-orbit. **So the restriction is the quantum descent step inside Rees,
not a classical reduction, and it cannot be "always applied" classically**
[argued for the negative part]. What is always available is H ∩ A for
abelian A, as a sub-instance: quantumly by abelian Fourier sampling on the
same source. Classically that sub-instance is the abelian-period residual
(S1 with G abelian), whose status is UNKNOWN; any hardness it has would be
obfuscation-type.

## 6. Exposure and succinctness

**Lemma X (exposure) [proved, elementary].** Let π: G → GL(V) be an
explicit F_p-representation, let d ∈ V, and let Φ be a construction with
Φ(π(g)d) = g·Φ(d). Then Stab_G(d) ≤ Stab_G(Φ(d)), with equality if and
only if Φ is injective on the orbit π(G)d. Suppose equality holds, V is
explicit, and d is known or can be recovered from F. Then H is a vector
stabilizer: `rem:filters`(0), Luks.
- Moore forms (d is a Plücker vector) and twisted forms (d is the
  bilinear form B) are orbit-injective.
- Orbit products and transfers are not. Their fibres are the
  reparametrizations of an orbit (X1c) or the action of K itself (X1a,
  X1b). Their natural circuits name K or its norms anyway.

**Observation S (succinctness) [argued].** Natural constructions of a
polynomial with a large hidden p-group K among its symmetries are:
- orbit products and orbit sums over K;
- Nakajima norms, which are Moore ratios;
- Dickson and Mui invariants;
- compositions of the above.

Each one either names K or its invariant generators in the circuit, or has
size growing with |K| (or with p, for one cyclic level). Every high-weight
family found in four passes has this property. A natural X would need a
*semantic* source of high-weight invariants with no constructive access to
K. None is known.

## 7. Best survivor

**S1-hw (high-weight residual).** S1 with all of the following:
- p-weight δ(F) unbounded, and either ≥ p/max(ν−1, 2) or superpolynomial;
- D and p growing;
- H non-normal with H ⊉ [G,G];
- a circuit that does not expose H.

Most concrete instance: **X1a with b ≥ 3 blocks**. This is a generic
invariant of a non-normal pattern group, conjugated by a random element of
UT_D(F_p), and given by an unstructured circuit.
- At D = 4 (p = 5 and 7) it survives naive Lie, Theorem W, anchored jets
  ≤ 3, gradient span and factorization, and dies only to the orbit-rank
  cap. At D = 6 only the orbit rank was computed (≥ 600, unconjugated).
  So no single instance has been shown to pass every filter; running all
  filters at D ≥ 6 is open.
- Under Lemma G it is quantum polynomial at fixed class, conditional on
  `thm:main`(b).
- **It is not an application.** Any hardness would be obfuscation-type,
  none is known, and no independent motivation is known.

A classical attack worth testing [conjecture]. If τ = I + vφ^T is a
transvection in H, then (s − φ(x)) divides F(x + sv) − F(x) in F_p[x, s].
So, for polynomially bounded p, transvections in H appear as linear
factors of circuit polynomials (Kaltofen), provided the direction v can be
found. X1a's H is generated by transvections. A classical algorithm for
transvection-generated H would kill X1a outright. Not pursued here.

## 8. What a human must check

1. **Theorem W(a).** The proof in §2.2, in particular:
   - formal versus function identity on E^D (|E| > Δ);
   - the reducedness step (degree ≤ δ < p);
   - the two-direction Lie argument applied to R_F over E, using ν and
     exp(sA)exp(tA) = exp((s+t)A);
   - the interpolation identity of Step 5 at F_p-rational points only.
2. **Theorem W(b).** Unisolvence of the simplex grid, faithfulness of π,
   and the Luks import (abstract only so far, as in the third pass).
3. **Priority.** Two facts are classical in coding theory:
   - the F_p-algebraic degree of x ↦ x^a on F_{p^K} is s_p(a), the
     "algebraic degree" of power functions and Delsarte-type subfield
     arguments [NEEDS HUMAN VERIFICATION];
   - the Lie-algebra method for polynomial symmetries is Kayal's (2011)
     and the audit's [NEEDS HUMAN VERIFICATION].

   Their combination here may be known.
4. **Lemma Z.** The negative claim that no succinct circuit exists for the
   Z-orbit is argued, not proved.
5. **Candidates.** Whether X1a with an unstructured circuit has a classical
   algorithm. See the transvection-factor idea in §7.
6. **Regime.** Whether fixed-D, superpolynomial-p S1 (fixed m) is already
   covered by pre-Rees quantum algorithms (DHIS-type). UNKNOWN.
7. **Citations.** All literature below that is not in `main.tex`.

## 9. Proposed text

To sit after the application-3 paragraph of `main.tex` (not applied):

```latex
A fourth AI-only pass (\file{research/audits/reviews/2026-11-05-rees-application-4.md}; AI-checked, pending human review) narrows that candidate further. Let $\delta(F)$ be the $p$-weight degree of $F$, the largest base-$p$ digit sum $\sum_i s_p(\alpha_i)$ of an exponent vector $\alpha$ in its support, and let $\nu \le p$ be the nilpotency index of $\mathcal{L}$ on the variables. On the points of $\mathbb{F}_{p^K}^D$, read as $\Fp^{KD}$, the polynomial $F$ agrees with a polynomial $R_F$ of degree at most $\delta(F)$, on which $G$ acts $\Fp$-linearly. Suppose a bound $\hat\delta \ge \delta(F)$ is known, $p > \max((\nu-1)\hat\delta, 2\hat\delta)$, and $p^K$ exceeds the formal degree. Then the first-order Lie method applied to $R_F$ recovers the stabilizer with high probability, from $\hat\delta+1$ evaluations of $F$ per basis element of $\mathcal{L}$ and per sample point, and uses nothing about how the circuit is built. This covers Frobenius lifts, Artin--Schreier, trace and Hermitian forms, and Moore forms of $r$ rows once $p > \max((\nu-1)r, 2r)$. For bounded $\hat\delta$ the restriction is an explicit representation, so~\cite[Theorem~3.2(5)]{Luks1992} applies for every $p > \hat\delta$. An instance beyond these filters therefore needs unbounded $p$-weight that is at least $p/\max(\nu-1,2)$ or superpolynomial in the input size. The high-weight families examined were generic invariants of non-normal pattern subgroups and orbit products. Each either exposes the hidden subgroup in its natural circuit or, at the sizes tested, falls to factorization, anchored jets or the orbit-module rank. Multivariate public-key maps have degree at most three, below $p \ge 5$, and are explicit tensors. No independently motivated family was found.
```

## 10. Citations

In `main.tex`:
- Luks 1992;
- FIMSS 2014;
- Ivanyos–Sanselme–Santha 2012;
- Ivanyos–Santha 2015;
- Ivanyos–Magniez–Santha 2001/2003.

From memory, not opened, all NEEDS HUMAN VERIFICATION:
- H. Nakajima, "Regular rings of invariants of unipotent groups",
  J. Algebra 85 (1983);
- H. E. A. Campbell, D. L. Wehlau, *Modular Invariant Theory*, Springer
  EMS 139 (2011);
- L. E. Dickson, Trans. AMS 12 (1911);
- H. Mui, J. Fac. Sci. Univ. Tokyo 22 (1975);
- D. Carlisle, P. Kropholler, on rational invariants of orthogonal and
  unitary groups, Bull. LMS (c. 1992);
- J. Patarin, Eurocrypt 1996 (HFE, IP);
- A. Kipnis, A. Shamir, Crypto 1999 (MinRank attack on HFE);
- A. Kipnis, J. Patarin, L. Goubin, Eurocrypt 1999 (UOV);
- J. Ding, D. Schmidt, ACNS 2005 (Rainbow);
- W. Beullens, Crypto 2022 (Rainbow);
- J.-C. Faugère, L. Perret, Eurocrypt 2006 (IP);
- N. Kayal, SODA 2011 (Lie-algebra method for polynomial equivalence);
- E. Kaltofen, "Factorization of polynomials given by straight-line
  programs" (1989);
- C. Lehr, M. Matignon, "Automorphism groups for p-cyclic covers of the
  affine line", Compositio Math. 141 (2005);
- P. Delsarte, IEEE Trans. IT 21 (1975) (subfield subcodes).

## 11. Independent adversarial check

One fresh general-purpose AI referee checked this report and its code. It
had read-only access, could rerun small checks, and had no access to this
session's reasoning. This is not human review. Its findings and how each
was handled:

- **Theorem W(a) [OK].** The referee checked each step: ρ for F_q
  matrices, the Weil identity using only u ∈ F_p^N, the degree bound with
  carries, formal versus function identity, both Lie directions with ν,
  interpolation at F_p nodes, and Chernoff (failure ≤ ε²). It found no
  counterexample inside the hypothesis. Its own independent test covered 9
  cases (random bases, F_q coefficients, p = 5, 7, 25), and W matched brute
  force in all 9.
- **Theorem W(b) [OK].** OK given the Luks import, which is already listed
  in §8.
- **Lemma Z [OK].** Correct.
- **Code [OK].** It tests what the report says, and every number matches
  the `.out` files.
- **ERROR, fixed.** The residual ignored that W(a) costs δ̂+1 evaluations.
  It now reads: "unbounded, and ≥ p/max(ν−1, 2) or superpolynomial"
  (§0, §3, §7, §9).
- **ERROR, fixed.** The orbit-product weight a(p−1)+1 holds only for affine
  orbits. The referee found weight 13 for a non-affine orbit of size 25 at
  p = 5. The table row is corrected, and the Dickson weight is sharpened to
  D(p−1).
- **GAP, fixed.** The "D grows" reason was wrong, because Δ may be
  exponential. It is replaced by brute force over |G| ≤ p^{D(D−1)/2} with
  PIT.
- **GAP, fixed.** Lazard/class < p is now stated in §2.1. Step 7 now uses
  only the subgroup form of the Lazard correspondence, and the hypothesis
  is weakened to ν ≤ p.
- **WORDING, all fixed.**
  - FIMSS is now called quantum.
  - X1b at p = 7 was not run, which is now stated.
  - No single X1a instance passes every filter, since D = 6 had only the
    orbit rank, which is now stated.
  - "Only hardness" became "any hardness would be … none is known".
  - The Lemma Z negative part is now marked [argued], and "explicit
    homomorphism" is removed.
  - The "H ∩ A always available classically" contradiction is removed.
  - S1 allows any Δ, so the X3 wording was changed.
  - The dangling "Remark 2.3" is removed.
  - Lemma X now requires that d be recoverable.
  - The X4 class claims are marked NEEDS HUMAN VERIFICATION.
  - The two-point labels at p = 7 are flagged as marginal.
  - The LaTeX now says "with high probability", "p > δ̂", "a known bound
    δ̂", and the Moore guard max((ν−1)r, 2r).

Referee's overall verdict: Theorem W(a) is correct, and W(b) is correct
given the Luks import. The report needed the revisions above before any
LaTeX goes in. All of them are applied here. The revised text was not
re-refereed.
