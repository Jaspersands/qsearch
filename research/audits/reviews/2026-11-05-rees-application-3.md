# Rees application search, third pass

2026-11-05. Claude Code session, AI only, not human review. No claim gate
changes; `speedup_claim_allowed` stays false; `rees_hsp_reduction.json`,
`main.tex`, `STATE.md` and the handoff were not touched. Exact checks are in
`2026-11-05-rees-application-3/` (`lie_linear_checks.py`, `.out`).

Rees wording, as the scope guard requires: "proposed fixed-class,
growing-prime polynomial-time composition, pending independent correctness
and priority review".

## 0. Verdict

**No application survives. The negative result is sharpened in three
places, and one residual is restated as a precise, paid, but unmotivated
problem.**

1. **Black-box p-groups (Section 2).** For black-box Lazard p-groups with
   unique encoding, the following tasks are quantum polynomial using
   abelian quantum subroutines only: centralizers, normalizers,
   intersections, automorphism fixed points, homomorphism kernels and
   conjugacy search. Quantum constructive membership (IMS 2003, Thm 6, via
   Beals–Babai) and the paper's abelian chart step make the group
   explicit. After that, Lemma E (proved, with exact checks) turns every
   one of these tasks into linear algebra in the Lie algebra. The known
   classical routes are blocked by abelian constructive membership
   (Babai–Szemerédi; Shoup for cyclic DLP). No per-task classical lower
   bound is proved here, and some instances are classically easy: in a
   black-box Heisenberg group, C(h) = ⟨h, [x,y]⟩ needs no DLP. So any
   separation is the abelian one, or none, and Rees adds nothing.
   Isomorphism of black-box p-groups is an orbit problem under a group that
   is not a p-group, so it is not an HSP over the p-group (11-02,
   Remark C). Status: **killed**.
2. **Cryptography over nilpotent platforms (Section 3).** Every scheme
   examined rests on one of four problems:
   - a cyclic or abelian discrete log, solved by Shor. In an explicit
     Lazard group it is linear anyway, since log h = a·log g; KS 2023
     Example 5.1 is one instance of this;
   - conjugacy or centralizer problems, solved classically (11-02 Lemma B
     and Lemma E);
   - the semidirect discrete log, which is quantum polynomial for solvable
     platforms by Imran–Ivanyos (DCC 2024);
   - an isomorphism or transporter problem, which is not an HSP over the
     p-group.

   No scheme reduces to an HSP with an arbitrary hidden subgroup in a
   fixed-class Lazard group. Status: **killed**.
3. **Lattices and codes (Section 5).** The natural nilpotent HSP from
   lattice cryptography is the Cyclotomic Coset Problem of
   Boucher–Fouque–Shen (arXiv:2609.34996). Its group R_q^n ⋊ F_p has class
   L = t(p−1).
   - For q = p^t with t ≥ 2 the class is at least p, outside Lazard.
   - For q = p the class is p − 1. That is fixed only when p is fixed, and
     there the BFS sieve is already polynomial in n.
   - Any fixed-class truncation is F_p^M ⋊ F_p of constant class, which is
     Ivanyos–Santha Cor 8.
   - The hidden subgroup is cyclic of order p, which is special.

   Lattice automorphism groups have p ≤ n+1, and q-ary lattices and codes
   are subspace stabilizers. Status: **killed**.
4. **Linear actions over every finite field (Section 6, Lemma F).** The
   dichotomy N ≥ p is proved. The classical branch imports Luks (abstract
   only) and an argued pull-back. Characteristic 0 is not written out. The
   11-02 kill of the "explicit linear representation" channel covered only
   the defining characteristic. Here is the cross-characteristic case.
   If ρ(G) is nonabelian then N ≥ p, so every prime is polynomially bounded
   and Luks applies. If ρ(G) is abelian then the stabilizer contains
   [G,G], and the problem is an abelian HSP (Shor-type). So linear actions
   never need Rees, in any characteristic.
5. **The residual, restated (Section 4).** Task: find the unipotent symmetry
   group of a polynomial of degree Δ ≥ p over F_p, given by an arithmetic
   circuit. This problem is now in Rees's input model with a paid
   reduction. Lemma G (proved) shows that the evaluation-graph source gives
   ε-approximate coset states once log q ≥ ½ m log p + log Δ + log(Q/ε).
   The first-order Lie method provably fails here (Part 3 control).
   Classical status is UNKNOWN. But no natural family is known, and the
   problem contains, as its abelian case, period finding for circuit
   polynomials. In that case abelian Fourier sampling already works, and
   classical hardness there looks obfuscation-like (a heuristic, not a
   result). So it is **not an
   application**: it satisfies (R1)–(R3) of the 11-02 contract but not the
   "motivated native input" requirement.

The best surviving candidate is item 5, and it is not a speedup claim.
Section 9 states what a human must check before it could become one.

## 1. Inputs and contract

Read:
- `main.tex`: abstract, §1 (contract `def:input-contract`, `thm:main`,
  `tab:main-regimes`), §`sec:black-box`, §`sec:classical-landscape`,
  `prop:classical-query`, `rem:query-separation`;
- `2026-10-30-rees-application-selection.md`;
- `2026-11-02-rees-application.md` (in full);
- the heads of the two 10-30 burst reviews;
- STATE row 156 and lines 80–125;
- TRAPS (rules 5, 7–11 and the scope guards).

The contract (R1)–(R4) of 11-02 §2 is used unchanged:
- (R1) fixed class 3 ≤ c < p;
- (R2) H non-normal, not containing [G,G], and not in IS Cor 8 or DHIS;
- (R3) a paid, natural hiding function or coset source;
- (R4) no classical algorithm and no simpler quantum one.

Primary sources opened as full text this pass:
- IMS 2003 (arXiv quant-ph/0102014, Thms 1–7, via pdftotext);
- Kahrobaei–Stanojkovski 2023 (§§1, 4.3, 5.1);
- Boucher–Fouque–Shen 2026 (arXiv HTML: the definitions, Lemmas 2, 5, 6
  and Thms 4.2, 4.3, via a summarizing fetch; specific statements are
  cited only as that fetch reported them).

Abstract only: Imran–Ivanyos SDLP, Tsaban 2015, Sun 2023. These are used
only for what their abstracts state (TRAPS 10).

## 2. Direction 1: black-box p-groups

### 2.1 Lemma E: Lie-linear group tasks (proved)

**Lemma E.** Let G = exp(L) be a Lazard group of class c < p. Let
K = exp k and K′ = exp k′ be subgroups, let α be an automorphism, and let
ψ: G → G′ be a homomorphism of Lazard groups. Then:

- (a) N_G(K) = exp N_L(k), where N_L(k) = {x : [x,k] ⊆ k};
- (b) C_G(K) = exp{x : [x,k] = 0};
- (c) K ∩ K′ = exp(k ∩ k′), and ⟨S⟩ = exp(Lie subalgebra generated by
  log S);
- (d) Fix(α) = exp ker(dα − 1);
- (e) ker ψ = exp ker dψ.

Every right-hand side is a linear-algebra computation over F_p, polynomial
in m and log p for fixed c. For prime-power exponent, replace F_p by
Z/p^e and subspaces by Howell forms (argued, not checked).

*Proof.*
1. Conjugation is exp(x) exp(y) exp(−x) = exp(e^{ad x} y), a BCH identity
   with p-integral coefficients in class < p.
2. Since ad_x maps γ_i into γ_{i+1}, we have ad_x^c = 0. So
   T = e^{ad x} − 1 satisfies T^c = 0, and
   ad_x = Σ_{1≤j<c} (−1)^{j+1} T^j / j. The denominators are below p, and
   log exp = id holds in Z_(p)[t]/(t^p).
3. Hence a subspace is preserved by e^{ad x} exactly when it is preserved
   by ad_x. Applied to k this gives (a); N_L(k) is a subalgebra by Jacobi.
   Applied to vectors y ∈ k with T y = 0 ⟺ ad_x y = 0, it gives (b).
4. (c) holds because exp is a bijection and by the subgroup form of the
   Lazard correspondence.
5. (d) and (e) follow because Lazard is functorial: α∘exp = exp∘dα with
   dα a linear Lie map, and similarly for ψ. ∎

*Exact check* (Part 1 of `lie_linear_checks.out`). In UT_4(F_5) (class 3,
order 5^6) the check is exhaustive over all 15625 elements. The test cases
were six random subgroups with dim k between 1 and 4, six intersections,
and three automorphisms (conjugation by random invertible upper-triangular
b). Brute-force normalizers, centralizers, intersections and fixed-point
sets equal the exponentials of the linear answers in every case, with
0 failures.

### 2.2 Black-box reduction (argued from cited theorems)

Let G be a black-box Lazard p-group of class c < p with unique encoding.

1. **Constructive membership.** IMS 2003, Theorem 6 (read): for black-box
   groups with unique encoding, constructive membership (straight-line
   programs), order, a presentation, the centre, a composition series and
   Sylow subgroups are quantum polynomial in the input size + ν(G), and
   ν(G) = 1 for solvable G. The only quantum steps are order finding and
   abelian HSP instances. The quantum part is the constructive test in
   *abelian* subgroups, the abelian HSP φ(α, α_0) = ∏ h_i^{α_i} g^{−α_0}
   (hypothesis (b) of IMS Cor 5). Constructive membership in G itself is
   Beals–Babai's classical machinery calling that test.
2. **Chart.** The paper's chart step, `prop:black-box`(ii) route (R2),
   recovers ker Φ for the free-Lie pullback Φ: F_{s,c} → G by one abelian
   HSP on (F_{s,c},+). This gives the explicit chart F_{s,c}/ker Φ ≅ log G.
3. **Translation.**
   - Chart to box: Lazard words evaluate Φ.
   - Box to chart: take the straight-line program from step 1 and evaluate
     it in the chart.
4. **Linear algebra.** With both directions available, Lemma E answers
   every task listed in Lemma E, and 11-02 Lemma B answers conjugacy
   search, by linear algebra.

So each task is quantum polynomial with abelian quantum subroutines only.

**Classical side.** Constructive membership in abelian black-box subgroups
is not classically polynomial under group-operation oracles. This is
Babai–Szemerédi 1984, as quoted by IMS §3. For cyclic Z_p it is the
generic DLP, Ω(√p) by Shoup 1997. These bounds are for constructive
membership, not for the tasks themselves. No per-task classical lower bound
is claimed. Some instances are classically easy: in a black-box Heisenberg
group with generators x, y, every noncentral h has
C(h) = ⟨h, [x,y]⟩. Where a separation exists, it is the abelian one.

Natural black-box hiding functions are built from group operations, for
example
- f(g) = g h g^{−1} for a centralizer;
- the Watrous-type subgroup-state label |gKg^{−1}⟩ for a normalizer;
- g ↦ g α(g)^{−1} for fixed points. Under the paper's convention
  f(x) = f(y) ⟺ x^{−1}y ∈ H, this gives left cosets; g^{−1}α(g) would
  hide right cosets.

All of these land in Lemma E. The black-box Theorem `thm:bb-envelope` is
needed only for an opaque hiding function, which is the oracle model
again.

### 2.3 Candidate table

| Candidate | Reduction to HSP | H | Best classical, and the quantum route without Rees | Status |
|---|---|---|---|---|
| Centralizer C_G(h), C_G(K) | f(g)=g h g^{−1} | arbitrary centralizer | IMS Thm 6 + chart + Lemma E(b); classically blocked only by abelian constructive membership | killed (abelian) |
| Normalizer N_G(K) | label of gKg^{−1} | arbitrary | Lemma E(a) after chart | killed (abelian) |
| Intersection K ∩ K′ | f(g) = (gK, gK′) labels | arbitrary | Lemma E(c) after chart | killed (abelian) |
| Fixed points of a black-box automorphism | g ↦ gα(g)^{−1} | arbitrary | Lemma E(d); dα from α on a basis plus logs | killed (abelian) |
| Kernel of a black-box homomorphism | g ↦ ψ(g) | normal | Hallgren–Russell–Ta-Shma / IMS Thm 7; Lemma E(e) | killed (normal) |
| Conjugacy search | transporter; its HSP part is the centralizer | — | 11-02 Lemma B after chart | killed |
| Isomorphism of black-box p-groups | orbit problem under GL, not a p-group | — | not an HSP over G (11-02 Remark C); best classical for class 2, exponent p, Cayley tables: N^{Õ((log N)^{1/2})} (Ivanyos–Mendoza–Qiao–Sun–Zhang, FOCS 2024, improving Sun 2023) | not Rees-type |
| Subgroup conjugacy, transporters | orbit coset (FIMSS 2003) | — | contains the hidden shift over Z_p, i.e. dihedral-type, for growing p | not Rees-type |
| Extraspecial p-groups, any H | HSP | arbitrary | IMS 2003, Cor 12 | already known |

## 3. Direction 2: cryptography over nilpotent platforms

| Scheme family | What an attacker must solve | Reduction to the Rees input model | Classical or known attack | Status |
|---|---|---|---|---|
| DLP in UT_n(F_q), in p-groups, and the Kahrobaei–Tortora–Tota nilpotent multilinear NIKE | cyclic DLP g^a = h, or a commutator-power DLP | abelian HSP in Z × ⟨g⟩, not a nonabelian HSP | In an explicit Lazard group log h = a log g, which is linear. KS 2023 Example 5.1 computes the KTT key in Heis_{2m+1}(F_p) with O(log² p) group operations, because M(u,v,z)^a = M(au, av, …) is explicit. For opaque encodings: Shor. | killed |
| MOR / ElGamal over p-group automorphisms | DLP in ⟨φ⟩ ≤ Aut(G) | abelian | Shor; the 11-02 summary (Mahalanobis's papers not opened) | killed (abelian) |
| Conjugacy, decomposition and AAG key exchange in UT_n, polycyclic or nilpotent platforms | conjugacy or decomposition search | transporter; its HSP part is the centralizer | 11-02 Lemma B for Lazard groups; for X ∈ UT_n, XA = BX is linear (10-30 review); linear-algebra attacks of Tsaban (J. Cryptology 2015) and Myasnikov–Roman'kov (2015) for linear platforms (abstracts and context only) | killed |
| Semidirect-product key exchange, SPDH-Sign (SDLP) | semidirect discrete log | cyclic action, hidden shift; not a p-group HSP with arbitrary H | Imran–Ivanyos (DCC 92 (2024) 2825–2843): quantum polynomial when G is solvable, using Shor-type tools (abstract); before that, Kuperberg-type subexponential (Battarbee–Kahrobaei–Perret–Shahandashti) | killed |
| ALTEQ / MEDS / class-2 p-group isomorphism | isometry of alternating maps, i.e. a transporter under GL × GL | not a p-group HSP (Remark C) | best classical: Ivanyos–Mendoza–Qiao–Sun–Zhang 2024 for the group form | not Rees-type |
| A p-group hash or PRF used as f | opaque | the oracle model | — | not native (R3) |

No examined scheme has security equivalent to a fixed-class Lazard HSP
with an arbitrary non-normal H. The one scheme family whose attacks are
group-theoretic HSPs (the centralizers inside conjugacy schemes) is
classical by Lemma B and Lemma E.

## 4. Direction 3: succinct objects of degree ≥ p (the residual)

### 4.1 The problem

**Problem S1 (unipotent circuit symmetry in small characteristic).**

*Input:*
- a prime p;
- an explicit Lazard group G = exp(L) ≤ UT_D(F_p) with D ≤ p, acting by
  linear substitution;
- a division-free arithmetic circuit C of size s computing
  F ∈ F_p[x_1..x_D];
- a formal degree bound Δ, possibly ≥ p, possibly 2^{O(s)}.

*Output:* H = {g ∈ G : F(g^{−1}x) = F(x) as formal polynomials}.

### 4.2 Lemma G: Rees input model, paid (proved)

Let E = F_q, q = p^k ≥ 2Δ, and let |V_F⟩ = q^{−D/2} Σ_{x∈E^D} |x⟩|F(x)⟩.
The 10-30 succinct-source review shows two facts:
- R(g)|V_F⟩ = |V_{T_gF}⟩;
- ⟨V_F|V_{T_gF}⟩ = Pr_x[F(x) = T_gF(x)], which is 1 on H and at most Δ/q
  off H, by Schwartz–Zippel.

Prepare |G|^{−1/2} Σ_g |g⟩ R(g)|V_F⟩ by three steps:
1. a uniform superposition over the chart;
2. a circuit evaluation for F;
3. a controlled linear map x ↦ gx over E.

Trace out the second register and call the result ρ. Then
ρ − ρ_H = |G|^{−1} Σ_{g′^{−1}g∉H} ε(g,g′)|g⟩⟨g′| with |ε| ≤ Δ/q. This
gives

- ‖ρ − ρ_H‖_2 ≤ Δ/q;
- ‖ρ − ρ_H‖_1 ≤ √|G|·Δ/q.

Choose log q ≥ ½ m log p + log Δ + log(Q/ε). Then Q copies are ε-close
to ρ_H^{⊗Q}, at cost poly(s, D, m, log p, log Δ, log 1/ε).

So, conditional on `thm:main`(b), S1 is quantum polynomial at fixed class
for an arbitrary H.

### 4.3 Classical status

- **Membership.** Testing g ∈ H is randomized polynomial (PIT of T_gF − F
  over E). So S1 is a hidden-subgroup-with-membership problem.
- **First-order Lie method.** It is proved for p > max(D, (D−1)Δ)
  (`SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md`). It fails for Δ ≥ p.
  *Control* (Part 3): F = x_1^p x_2 − x_1 x_2^p, with g_t: x_1 ↦ x_1 + t x_2.
  Then F(g_t x) − F(x) = (t^p − t) x_2^{p+1}. This vanishes formally for
  every t ∈ F_p, so H ⊇ {g_t}, while the Lie derivative at t = 0 is
  −x_2^{p+1} ≠ 0 (checked at p = 5, 7). The symmetry exists only over F_p
  and not over E. So the first-order derivative test fails, and an
  extension-field stabilizer would be wrong.
- **Other filters.** This particular F is a Moore determinant, so the Moore
  gradient recognizer and factorization handle it. The filters of
  `rem:filters` stay in force: orbit-module rank, anchored jets, tensor
  trains, Frobenius recognizers, gradients and Moore forms.
- **Abelian subcase.** Translations x ↦ x + v, as affine maps in
  UT_{D+1}, make S1 into period finding for a circuit polynomial. That is
  solved by abelian Fourier sampling on the same source. Hardness there
  would be obfuscation-type ("hide a subspace in a circuit"), not natural.
  A Rees-specific application would need classical hardness that survives
  the restriction to the abelian quotient while H is non-normal and does
  not contain [G,G].
- **Natural degree-≥p families checked.** None survives:
  - Dickson and Mui invariants of UT_n(F_q): they factor into linear
    forms, so factorization applies;
  - Moore forms: the Moore filter;
  - Hermitian forms x^{q+1}: semilinear algebra;
  - Artin–Schreier and trace forms: Frobenius recognizers;
  - HFE-type public keys: low degree over the base field, and the symmetry
    group is GL × GL, not unipotent.

**Status: UNKNOWN, unmotivated, not an application.**

## 5. Direction 4: lattices and codes with unipotent symmetry

### 5.1 Cyclotomic Coset Problem (Boucher–Fouque–Shen 2026)

**Group.** G = R_q^n ⋊ F_p with R_q = Z_q[ζ_p], q = p^t, and
(x_1,j_1)(x_2,j_2) = (x_1 + ζ^{j_1}x_2, j_1+j_2).

**Hidden subgroup.** H_s = ⟨(s,1)⟩ with s ∈ Z_q^n, of order p.

**Samples.** The samples are (1/√p) Σ_j |j⟩|x + λ_j s⟩ with x uniform.
Each coset of H_s meets {j = 0} exactly once, so these are exact copies of
ρ_{H_s}. CCP therefore satisfies Rees input (b) whenever the Lazard
hypotheses hold.

**Class.** BFS Lemma 2: the class is L = t(p−1), with γ_k = π^{k−1}R^n.
Checked exactly (Part 2) for (p,L,n) = (5,4,1), (5,4,2), (7,6,1), (7,3,2)
and (11,4,2):
- the class equals L, with dim γ_k decreasing by n per step;
- λ_j s has π^k-coordinate C(j,k+1)s;
- H_s is not normal.

**Regimes.**
- t ≥ 2: the class is ≥ 2(p−1) ≥ p, outside Lazard and outside Rees
  (`thm:ring-to-field` also needs class < p).
- t = 1 (q = p): the class is c = p − 1 < p, so Lazard holds.
  - For fixed p this is a fixed-class Rees instance. But the group is
    F_p^{n(p−1)} ⋊ F_p with a unipotent Jordan action, and H_s has order p
    outside the normal part. So for fixed p it is exactly Ivanyos–Santha
    Cor 8, not just its truncation (independent referee).
    - BFS Thm 4.3 gives time 2^{O_p(log n log q)} = n^{O_p(1)}, already
      polynomial.
    - Imran–Ivanyos handles bounded primes exactly. BFS note that its
      state-preparation-unitary premise is missing in the sample model.
    - Rees's exponent at c = p − 1 is about c² log c.
  - For growing p (q = p = poly(n), the LWE-relevant case) the class
    grows. Rees's bound is not polynomial, and the derived-dimension and
    codimension corollaries are exponential, with r = n(p−2) and
    codim = n(p−1).
  - The BFS samples are in the group's semidirect coordinates. Passing to
    the BCH chart of `def:input-contract` is a public reversible map.
- **Fixed-class truncation.** R = F_p[π]/π^L with L fixed gives
  F_p^{nL} ⋊ F_p of constant class with H of order p not in the normal
  part. This is exactly Ivanyos–Santha Cor 8 (scope as recorded in
  `main.tex` §1).

**Classical counterpart.** CCP is a quantum-input problem. Its classical
cousin, cyclotomic LWE, is not an HSP.

Status: **killed** (special H; regime covered or outside Rees).

### 5.2 Other lattice and code symmetry

- **Lattice automorphism groups.** These are finite subgroups of GL_n(Z),
  so any element of prime order p forces p − 1 ≤ n. For a p-group P and a
  sublattice L ⊇ NZ^n, Stab_P(L) is the stabilizer of the submodule
  L/NZ^n of (Z/N)^n. With p ≤ n+1 polynomially bounded, this is a Luks /
  ring-to-field computation (argued).
- **q-ary lattices Λ_q(A) and codes.** Under a unipotent linear group
  these are subspace stabilizers, handled by Lemma A, Lemma F and Luks.
- **DCP.** The dihedral HSP (p = 2, class log N) is outside p > c.

Status: **killed**.

## 6. Sharpened negative result

### 6.1 Lemma F: cross characteristic over finite fields

The dichotomy is proved. Branch (b) is classical only via Luks (imported,
abstract only) and an argued pull-back.

**Lemma F.** Let G = exp(L) be explicit, with class c < p, and let
ρ: G → GL_N(F_ℓ) be given on generators, with ℓ ≠ p. Then exactly one of
the following holds.

- **(a) ρ(G) is abelian.** Then every vector or subspace stabilizer
  contains ker ρ ⊇ [G,G]. The HSP is the abelian HSP on G/[G,G], solved by
  Shor/Kitaev. The natural classical obstacle is DLP in
  μ_{p^e} ⊂ F_{ℓ^k}^*, with k = ord_{p^e}(ℓ) and p^e the exponent
  (e = 1 in the exponent-p case).
- **(b) ρ(G) is nonabelian.** Then N ≥ p.
  *Proof.* Since ℓ ∤ |G|, ρ ⊗ F̄_ℓ is semisimple (Maschke). Its
  irreducible constituents lift to characteristic 0, so their degrees
  divide |G| and are powers of p. If every constituent were linear, ρ(G)
  would be abelian. So some constituent has degree ≥ p, hence N ≥ p.
  Consequently every prime dividing |ρ(G)| is at most N. Luks 1992
  (imported, abstract only) then gives vector and subspace stabilizers,
  centralizers and intersections in ρ(G) in polynomial time. Pulling back
  through ρ uses the straight-line programs and a pc-presentation kernel
  computation (standard; argued). So the problem is classical.

In the defining characteristic, Luks's prime condition holds for every
p-group. So Luks alone covers it, and 11-02 Lemma A is a self-contained
special case for N ≤ p. Together these close the linear-representation
channel over every finite field, and its only hard part is abelian.
Characteristic 0 (number-field matrices) would need a reduction modulo a
suitable prime, which is not written out here.

### 6.2 Channels, updated

Native classical inputs reach a Lazard-group HSP only through:

- (i) linear representations over finite fields (Lemma A, Lemma F,
  Luks);
- (ii) polynomial actions of degree below p/D_c (NIL3 attack);
- (iii) group-internal operations, including black-box groups (Lemma B,
  Lemma E, IMS + chart);
- (iv) orbit or transporter questions, which are not p-group HSPs;
- (v) succinct objects of degree ≥ p (S1, UNKNOWN);
- (vi) opaque labels (the oracle model).

Channels (i)–(iii) are classical or abelian, and (iv) is out of scope. The
only residuals are (v) and (vi), together with the quantum-state residual
of 11-02 §6. Cryptographic platforms and lattice HSPs examined here all
fall in (i)–(iv), or have a special H outside the fixed-class regime
(CCP).

## 7. Independent review and checks

One independent AI referee (read-only; not human review) checked Lemmas E,
F and G, the IMS reading, the CCP section and the verdict wording.

- Lemma E: OK (exponent p).
- IMS reading: OK, with two slips that are now fixed: the abelian versus
  full constructive test, and the fixed-point label convention.
- Lemma F: OK, with the gaps now stated: μ_{p^e}, characteristic 0, and
  Luks and the pull-back.
- Lemma G: OK. Its ρ matches `main.tex`'s left-coset ρ_H, entries
  1_H(a^{−1}b)/|G|.
- CCP: OK. The referee fetched BFS and found that t = 1 with fixed p is
  IS Cor 8 directly.
- Verdict: one ERROR, now fixed. The draft claimed exponential separations
  for the black-box tasks; the Heisenberg centralizer is a counterexample
  to the per-task claim. The referee also flagged wording overclaims,
  fixed above.

### Checks

`/opt/anaconda3/bin/python -I lie_linear_checks.py` (about 1 minute, one
core) writes `lie_linear_checks.out`:

- Part 1: Lemma E, exhaustive, 0 failures.
- Part 2: CCP class, binomial λ_j and non-normality, 5 parameter sets.
- Part 3: the degree-≥p control.

These are finite checks. They can falsify, not prove (TRAPS 7).

## 8. Citations

Read in full text this pass:
- G. Ivanyos, F. Magniez, M. Santha. Efficient quantum algorithms for some
  instances of the non-Abelian hidden subgroup problem. Int. J. Found.
  Comput. Sci. 14(5):723–739, 2003; SPAA 2001; arXiv:quant-ph/0102014.
  Used: Thms 1–4, 6, 7 and Cor 12.
- D. Kahrobaei, M. Stanojkovski. Cryptographic multilinear maps using pro-p
  groups. Adv. Math. Commun. 17(5):1101–1114, 2023; arXiv:2102.04513.
  Used: §5.1, Example 5.1.
- M. Boucher, P.-A. Fouque, Y. Shen. Cyclotomic Cosets: Hidden Subgroup and
  Quantum Sieving Algorithm for Prime-Power Moduli. arXiv:2609.34996, 2026.
  Used: the definition of G_{n,q,p} and H_s, Lemma 2, Thm 4.2 (Imran–Ivanyos
  zero-sum) and Thm 4.3, as reported by a summarizing fetch of the arXiv
  HTML. Theorem numbers need a human check.

Abstract or metadata only:
- M. Imran, G. Ivanyos. Efficient quantum algorithms for some instances of
  the semidirect discrete logarithm problem. Des. Codes Cryptogr.
  92(10):2825–2843, 2024; arXiv:2312.14028; ePrint 2023/1953.
- B. Tsaban. Polynomial-time solutions of computational problems in
  noncommutative-algebraic cryptography. J. Cryptology 28:601–622, 2015;
  arXiv:1210.8114.
- X. Sun. Faster isomorphism for p-groups of class 2 and exponent p. STOC
  2023; arXiv:2303.15412.
- G. Ivanyos, E. Mendoza, Y. Qiao, X. Sun, C. Zhang. Faster isomorphism
  testing of p-groups of Frattini class 2. FOCS 2024.
- D. Kahrobaei, A. Tortora, M. Tota. Multilinear cryptography using
  nilpotent groups. In *Elementary Theory of Groups and Group Rings, and
  Related Topics*, De Gruyter, 2020; arXiv:1902.08777.
- E. M. Luks. Computing in solvable matrix groups. FOCS 1992, 111–120.

Cited through IMS or `main.tex`, not opened:
- L. Babai, E. Szemerédi. On the complexity of matrix group problems I.
  FOCS 1984, 229–240.
- R. Beals, L. Babai. Las Vegas algorithms for matrix groups. FOCS 1993,
  427–436.
- J. Watrous. Quantum algorithms for solvable groups. STOC 2001.
- K. Cheung, M. Mosca. Decomposing finite abelian groups. arXiv:quant-ph/0101004.
- G. Ivanyos, M. Santha. arXiv:1503.09016v2 (Cor 8; read in full by 11-02).
- G. Ivanyos, L. Sanselme, M. Santha. Algorithmica 62 (2012).
- M. Imran, G. Ivanyos. Zero sum subsequences and hidden subgroups. Quantum
  Inf. Process. 23, Article 14 (2024).
- K. Friedl, G. Ivanyos, F. Magniez, M. Santha, P. Sen. Hidden translation
  and orbit coset in quantum computing. STOC 2003; SIAM J. Comput. 2014;
  arXiv:quant-ph/0211091.

Standard results used:
- V. Shoup. Lower bounds for discrete logarithms and related problems.
  EUROCRYPT 1997.
- O. Regev. Quantum computation and lattice problems. SIAM J. Comput. 33(3),
  2004.
- G. Kuperberg. SIAM J. Comput. 35(1), 2005.
- M. Lazard. Ann. Sci. ENS 71, 1954.
- E. I. Khukhro. *p-Automorphisms of Finite p-Groups*, Ch. 10, 1998.
- J.-P. Serre. *Linear Representations of Finite Groups*, Part III
  (coprime characteristic), 1977.
- Schwartz (1980) and Zippel (1979).

Context, not opened:
- A. Myasnikov, V. Roman'kov. A linear decomposition attack. Groups Complex.
  Cryptol. 7 (2015).
- A. Battarbee, D. Kahrobaei, L. Perret, S. Shahandashti. The subexponential
  quantum SDLP algorithm (2022), cited by Imran–Ivanyos.

## 9. Survivor statement and what a human must check

**Candidate (best surviving, not an application).** S1 of Section 4.

**Claim it would allow, if every item below held.** "Conditional on
`thm:main`, the proposed Rees composition computes the formal unipotent
symmetry group of a degree-Δ circuit polynomial over F_p in time
poly_c(s, D, m, log p, log Δ). No classical polynomial algorithm is known
for the family X." That is a running-time statement for a named family X.
It is not a query separation and not a speedup claim. Even then, TRAPS 9
forbids the word "speedup" until hardness evidence exists.

**A human must check:**
1. Lemma G: the trace-norm bound, and the reduction to the left- or
   right-coset convention of `thm:main`(b).
2. A family X that is motivated independently of Rees. It must have a
   non-normal H not containing [G,G], and Δ ≥ p. It must also defeat the
   Lie method, the orbit-module, jet, Frobenius, gradient, Moore and
   factorization filters, and the abelian-quotient restriction of §4.3.
   None is known.
3. Lemma F(b): the pull-back step and Luks's full text (abstract only so
   far).
4. Lemma E for prime-power exponent (Howell forms).
5. The BFS theorem numbers, and whether CCP with t = 1 and fixed p is
   already polynomial in BFS's own accounting (Thm 4.3 as fetched says
   2^{O(log n log q)}).

**Suggested STATE row text** (not applied):

> Rees applications | None survived (11-05 third pass). Black-box Lazard
> p-groups: every group-theoretic HSP is abelian quantum + Lemma E linear
> algebra. Nilpotent-platform crypto: DLP, centralizer, SDLP or
> transporter. CCP (BFS 2026): class t(p−1), special H, covered or outside
> Rees. Linear actions over finite fields are closed (Lemma F).
> Residual: S1 (unipotent circuit symmetry, Δ ≥ p), paid via Lemma G,
> classical status UNKNOWN, no motivated family. |
> `audits/reviews/2026-11-05-rees-application-3.md`
