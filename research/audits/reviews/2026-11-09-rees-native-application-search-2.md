# Rees native application search, second deep pass (search 2)

2026-11-09. Claude Code session, AI only, not human review. No claim gate
changed; `speedup_claim_allowed` and `novelty_established` stay false.
`main.tex`, the registry and `STATE.md` were not touched; no git commands.
Scripts and outputs are in `2026-11-09-rees-native-application-search-2/`.

Rees wording, as the scope guard requires: "proposed fixed-class,
growing-prime polynomial-time composition, pending independent correctness
and priority review". Everything below is conditional on that theorem.

Tags: [proved] full argument here; [computed] exact finite check (can only
falsify, TRAPS 7); [cited] primary source read, locator given; [abstract]
only an abstract was read (TRAPS 10: no theorem is inferred from it);
[argued] sketch.

## 0. Bottom line

**No independently motivated application was found. The negative result
stands, but this pass found the first Rees-native problem whose
ingredients all come from published work, and it fixes the exact regime
where Rees is the only polynomial route we know of.**

1. **Best candidate (L1): the unipotent symmetry group of a hidden
   multivariate Legendre function.**
   - The secret is a squarefree Q in F_p[x_1..x_n] of degree d, n >= 3.
     The only access is coherent queries to x -> chi(Q(x)) on F_p-points,
     the generalized Legendre-PRF oracle of Russell–Shparlinski,
     Beullens et al. and KKK. The goal is H = Stab_U(Q), with
     U = UT_{n+1}(F_p) acting by affine substitutions (class n < p).
   - Paid reductions: Stab_U(chi∘Q) = Stab_U(Q) (Weil). A public
     random-point fingerprint f(g) = (chi(Q(g x_j)))_{j<=t}, with
     t = O(n^2 log p), is a coherent classical hiding function for the
     right cosets Hg [proved, modulo the multivariate Weil constant;
     computed].
   - Exact checks in UT_4(F_5) and UT_4(F_7), d = 3, 4: H is non-normal,
     of order p or p^2, not inside the translations, and about 20 points
     separate all cosets.
   - **Fixed d: killed.** The repo's own quantum Legendre learners
     recover Q in poly(log p) for each fixed d. They are AI-reviewed and
     unpublished. Use the squarefree readout on line restrictions and
     stitch the scalars. Stab_U(Q) is then linear algebra once p > nd
     (reviewer: for p <= nd, Fix(g) and ker D_X can differ).
   - **Circuit input: killed classically**, by a new Frobenius-root
     identity, Q(z)F(z)^2 = Q^[p](z) with F = Q^((p-1)/2) (Lemma 4,
     proved and computed). This answers the 11-05 S1 question: the
     natural high-p-weight F that pass was missing exists, but it is
     classical in the circuit model.
   - **Survivor regime:** F_p-point oracle only; d log d = omega(log log p)
     and p >= 64 d^2; p superpolynomial; n >= 4 fixed. For n = 3, UT_4 is
     metabelian, and the repo's own unreviewed metabelian HSP drafts would
     also apply. Here the best known learner of Q costs
     exp(O(d log d)) poly(d^n, log p), from the repo's Hankel receiver
     plus stitching. Russell–Shparlinski give only O(d) queries, with no
     efficient measurement. The Rees route costs poly(n, log p),
     independent of d apart from the prime threshold.
   - The reviewer's decomposition attack pins the missing piece. Known
     tools give H ∩ T (abelian HSP) and the lift of any known linear part
     (Ivanyos–Santha Cor 8). Normal H is also handled. What remains open
     without Rees is the linear-part image π(H) = HT/T in UT_n. Its
     natural route needs a translation-invariant fingerprint of
     lambda∘Q, a degree >= 2 Legendre hidden shift. That is not solved,
     and it is not shown hard.
   - **Why it is not an application:** nobody needs Stab_U(Q).
     Multivariate Legendre PRFs are not a published primitive. For
     random keys H is trivial. KKK's stabilizers of univariate keys
     (under PGL_2) are cyclic of order prime to p. A nontrivial H needs a
     planted symmetry, Q = R∘g0 with R public. Recovering H then recovers
     g0 only modulo N_U(K). Status: **constructed, natural
     ingredients.** This is the strongest survivor so far, and it is not
     an application.
2. **Second (A1): unipotent self-equivalences E∘A = B∘E of
   arithmetization-oriented permutations over F_p.** Examples are Rescue,
   whose x^(1/alpha) layers have degree about p, Anemoi and Griffin. They
   sit in the open S1 branch "D fixed, p superpolynomial, high p-weight".
   **Killed as an application.**
   - H is trivial by design. In the exact toy check (p = 11, state F_11^3,
     all 1,771,561 elements of UT_4) only the identity survives.
   - Published commutative cryptanalysis (Baudrin et al., ToSC 2023) works
     over F_2, where p = 2 is outside the Lazard range.
   - Coset-label injectivity is not guaranteed for maps of degree >= p.
3. All other new sources fall into channels already closed. These are
   Grochow–Qiao isomorphism problems, the unipotent part of Aut(G),
   tensor and semifield autotopisms, code automorphisms and equivalence,
   transversal qudit gates and unitary symmetries (table, Section 2).

The STATE row "Rees applications: none survived" stays. The reason can be
sharpened to name L1 as the best constructed survivor and to state its
regime (Section 7).

## 1. Scope and what was excluded

Read: `STATE.md`, `TRAPS.md`, cloud-batch section G (19 candidates, shortlist
Imran–Ivanyos / S1 circuit residual / C9 / qudit phase states), and the four
earlier searches, whose candidates are not repeated:
`2026-10-30-rees-application-selection.md`, `2026-11-02-rees-application.md`
(channels: linear reps, low-degree polynomials, conjugation, isomorphism;
phase states; twisted codes), `2026-11-05-rees-application-3.md` (black-box
p-groups, nilpotent-platform crypto, CCP, lattices, Lemma F) and
`2026-11-05-rees-application-4.md` with its check (Theorem W; S1 residual
"high p-weight, D and p growing", plus the branch "D fixed, p
superpolynomial" restored by the check). The 11-02 note (Section 3.6) already noted
Stab(chi∘Q) = Stab(Q) and set the hidden case aside as "an oracle problem".
What is new here is that the hidden case is a specific published oracle
family, not an arbitrary one. Its fixed-degree part is now killed by
quantum learners the repo wrote after 11-02. Its growing-degree part
survives.

## 2. Ranked candidate table

Columns: reduction to a Lazard HSP; class < p and access match; classical
status; earlier quantum coverage; verdict.

| # | Candidate | Reduction | Class / access | Classical | Earlier quantum | Verdict |
|---|---|---|---|---|---|---|
| L1 | Stab_U(Q) from chi∘Q, Q squarefree of degree d, U = UT_{n+1}(F_p), n >= 4 (n = 3 is metabelian) | fingerprint f(g) = (chi(Q(g x_j)))_j (Lemma 2) | class n < p; coherent F_p-point oracle, same Q2 promise as van Dam–Hallgren–Ip | best known exponential in log p (KKK, Beullens et al., Russell–Shparlinski O(d^2 p^{d+eps})); full-data O(p) per line; none poly known; no lower bound | fixed d (and d log d = O(log log p)): repo learners recover Q, then linear algebra (KILL). Otherwise only exp(O(d log d)); RS query-only; the reduction is DISW's strong-base idea, but the DISW orbit promise fails; known tools give H∩T and the lifts, not π(H) | **Survives in the regime "d log d = ω(log log p), n >= 4, F_p-oracle". Constructed target, no consumer.** |
| L1′ | Planted variant: Q = R∘g0, R public with known stabilizer K | H = g0^{-1} K g0 from L1; then conjugacy search (11-02 Lemma B) gives g0 mod N_U(K) | same | as L1 | as L1 | partial key recovery only; constructed |
| L1″ | Same with a k-th power-residue character, k \| p−1 | same, using Weil for chi_k | same | same | repo learners are quadratic-only; UNKNOWN for k > 2 | same as L1, untested |
| L1c | L1 with F = Q^((p-1)/2) given as a circuit (S1 model) | — | — | **classical poly** (Lemma 4, Frobenius root) | — | **killed** |
| A1 | Self-equivalences E∘A = B∘E of AO permutations over F_p (Rescue, Anemoi, Griffin) under unipotent affine A, B | labels B^{-1}∘E∘A (graph states or fingerprints) | class n < p; D fixed, p superpolynomial (open S1 branch) | UNKNOWN in general | none | **killed as an application**: H trivial by design (toy check: identity only); label injectivity unpaid for degree >= p; published commutative cryptanalysis is over F_2 |
| G1 | Group/tensor/cubic-form isomorphism, Grochow–Qiao | orbit problem under GL | not a p-group HSP (11-02 Remark C) | GQ reduce exponent-p class c < p GpI to class 2 [abstract] | — | **killed** (not Rees-type) |
| G2 | Unipotent part of Aut(G) for an explicit Lazard G; autotopisms of semifields; stabilizer of a tensor in an explicit unipotent U ≤ GL | Stab of the bracket tensor under a linear p-group action on a poly-dimensional space | class < p fine; explicit | Luks p-group stabilizer / 11-02 Lemma A; Eick–Leedham-Green–O'Brien lifting is the practical method [bibliographic] | — | **killed** (channel i) |
| C1 | Code automorphisms inside a permutation or monomial p-group; code equivalence (LESS-type) | set or subspace stabilizer; equivalence is an orbit problem under the monomial group | equivalence is not a p-group | Luks (bounded composition factors) for automorphisms | — | **killed** |
| Q1 | Transversal diagonal logical gates of qudit stabilizer codes, inside G_e = Paulis ⋉ diagonal level-e gates (class e+1) | stabilizer of an explicit code space | explicit succinct code | linear in the phase-polynomial coefficients [argued]; Webster–Quintavalle–Bartlett give efficient algorithms for qubit CSS codes [abstract] | — | **killed** (classical; qubit case is p = 2) |
| Q2 | Centralizer in G_e of a black-box unitary (Choi-state labels) | quantum labels | overlaps unbounded: unitaries that differ on a small subspace have Choi overlap near 1 | — | diagonal unitaries are learnable as phase states (IS15 §5; 11-02) | **killed** (no label promise) |
| K1 | Further group-based crypto: Stickel / UT_n, Cayley hashes on UT_3 and Heisenberg groups, nilpotent multilinear maps (arXiv 2102.04120) | linear conjugacy, word/relation finding, or DLP | — | linear algebra; collisions come from abelianization | Shor for DLP | **killed** (falls into the four primitives of the 11-05 table) |
| F1 | DISW hidden symmetry subgroups (HSSP) as a framework | Lemma 1 strong base | — | — | DISW solve affine/Frobenius cases and HQPP in constant characteristic | not an application; DISW's promise (level sets = H-orbits) fails for chi∘Q, so DISW does not cover L1; Lemma 2 below reuses their base idea |

Not repeated (earlier passes): black-box p-group tasks, MOR/SDLP/AAG,
CCP, lattices, phase-state learning, twisted codes, Theorem W families, C9,
the Imran–Ivanyos open problem.

## 3. L1 in detail

### 3.1 Problem

- Public: an odd prime p, n >= 3, d with 2 <= d and p >= max(64 d^2, nd + 1).
  The "only known route" claim below needs n >= 4.
- Secret: a squarefree Q in F_p[x_1..x_n] of degree d.
- Access: a coherent (bit or phase) oracle for lambda(Q(x)), x in F_p^n,
  with lambda the quadratic character and lambda(0) = 0. There are no field
  values of Q, no extension-field queries and no circuit.
- G = U = UT_{n+1}(F_p), acting on x in F_p^n by (x,1) -> M(x,1). Its
  class is n < p for p > n, and it is a Lazard group with its explicit
  matrix logarithm.
- Output: H = Stab_U(Q) = {g : Q∘g = Q}.

### 3.2 Lemmas

**Lemma 1 (non-proportionality) [proved].** If g in U and Q∘g = c·Q
with c in F_p^*, then c = 1.

*Proof.* U has exponent p, since n < p. So Q = Q∘g^p = c^p Q, hence
c^p = 1 and c = 1 in F_p.

**Lemma 2 (symmetries and fingerprint) [proved, modulo the constant in
the Weil bound (W)].**

(W) is the bound, for S squarefree of degree D < p (by restriction to
lines in a direction b with S_D(b) ≠ 0, Weil on each line, and
Schwartz–Zippel on the disc_t locus; reviewer item (d), with the measured
ratio to the bound <= 0.13):
|Σ_{x in F_p^n} chi(S(x))| <= (D−1) p^{n−1/2} + D(D−1) p^{n−1}.

Claims:

- (a) Stab_U(lambda∘Q) = Stab_U(Q) once p >= 64 d^2.
- (b) Fix t public uniform points x_1..x_t, with
  t >= (n(n+1) log_2 p + log_2(1/eta)) / log_2(4/3). Then, except with
  probability eta, the map g -> (lambda(Q(g x_j)))_j is constant exactly
  on the right cosets Hg. The per-point agreement of two distinct
  translates is at most rho = 1/2 + (2d−1)/(2√p) + (4d²+d)/(2p), and
  rho <= 3/4 for p >= 64 d^2.

*Proof.*

- Q∘(hg) = Q∘g for h in H, so the map is constant on right cosets.
- Conversely, suppose Q∘g ≠ Q∘g'. By Lemma 1 the two are not
  proportional. Write Q1 = Q∘g and Q2 = Q∘g'. Both are squarefree, so
  Q1·Q2 = D^2 · (Q1/D)(Q2/D) with D = gcd, and the cofactor product is
  squarefree and nonconstant.
- By (W), lambda(Q1) and lambda(Q2) agree on at most a rho fraction of
  F_p^n. The zero sets have density at most d/p.
- With w the number of such pairs, the union bound gives failure at most
  w · rho^t <= |U|^2 rho^t.
- (a) is the case g' = identity, applied to every point of F_p^n.

**Lemma 3 (structure) [computed].** The exact checks are
`legendre_unipotent_check.py/.out`, with p = 5 and 7, d = 3 and 4. Q is
chosen as R∘g0, with R an absolutely irreducible invariant of a
non-central one-parameter subgroup.

- In all nine cases, including the random and square controls,
  Stab(lambda∘Q) = Stab(Q).
- H = g0^{-1} H_R g0.
- |H| is 5, 49 and 7.
- H is non-normal, does not contain [G,G] and is not inside the
  translation subgroup.
- The worst agreement outside H is 0.49–0.56 for the planted keys and
  0.53–0.65 for random keys.
- 17–22 random points separate all 3125 / 2401 / 16807 cosets (up to 27
  for the trivial-H controls).
- These checks falsify nothing. They are not evidence for all p.

**Lemma 4 (Frobenius-root filter, circuit model) [proved; computed].**
Suppose Q is squarefree and F = Q^((p-1)/2) can be evaluated at points of
E = F_{p^K}^n, as an arithmetic circuit allows. Then the coefficient
vector of Q is the unique solution, up to an E-scalar, of the linear
system

    Σ_a c_a ( z^a F(z)^2 − z^{p a} ) = 0,  for random z in E^n.

*Proof.*

- Q itself solves it: Q F^2 = Q^p = Σ q_a z^{pa}, since q_a ∈ F_p.
- Let Q′ be any solution, and set R = Q′^{σ^{-1}}, where σ is
  coefficient Frobenius. Then Σ c_a z^{pa} = R^p, so
  Q′ Q^{p−1} = R^p, that is R^σ Q^{p−1} = R^p.
- Each irreducible factor π of Q has π^{p−1} | R^p, so π | R. Hence
  Q | R. Since deg R = deg Q′ <= d, R = cQ and Q′ = c^p Q.
- By Schwartz–Zippel over E, with p^K much larger than the formal
  degree, O(binom(n+d,d)) random rows give full rank minus one.
- Checks: `frobenius_root_filter_check.sage/.out`. For (p,n,d,K) =
  (7,2,3,6), (11,3,3,4), (13,3,4,4), (101,2,5,3), the kernel has
  dimension 1 and recovers Q.

Consequence: chi∘Q given as a circuit is not an S1 residual instance.
Lemma 4 is presentation-independent, like Theorem W. It uses the
Frobenius twist of F^2·Q rather than a Weil restriction.

### 3.3 Competitors

- **Classical, F_p-oracle.**
  - Russell–Shparlinski (quant-ph/0212016, abstract and Section 1):
    O(d^2 p^{d+ε}) classical for univariate keys.
  - Beullens et al. 2020 and KKK 2020 (Section 4): exponential in log p
    for fixed degree. KKK §4F treats degree 2 in O(p).
  - The repo's elementary full-data baseline needs p queries
    (`QUADRATIC_LEGENDRE_RECOVERY.md`).
  - Restricting to lines makes the multivariate case at least as hard as
    univariate key recovery. That is not hardness for computing
    Stab_U(Q).
  - Membership g ∈ H is classically easy to test, with O(log 1/eps)
    random point pairs by (W). But membership alone does not find h: H
    can have codimension at least 1 in a fixed-dimension Lie algebra, so
    random search costs p^{codim}, a Grover-type barrier for membership
    queries alone.
  - No poly(log p) classical algorithm is known; the reviewer found none.
    No lower bound is claimed.
- **Quantum, without Rees.**
  - van Dam–Hallgren–Ip covers d = 1.
  - Russell–Shparlinski Thm 6 (local text, line 341): O(d) queries
    suffice for a POVM to exist. No efficient POVM is given.
  - Repo learners (unpublished, AI-reviewed, see the STATE rows):
    quadratic, univariate and affine (`QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md`,
    `AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT.md`), fixed d
    (`LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md`, cost C_d poly(log p)
    with C_d "factorial or worse"), and uniform
    exp(O(d log d)) poly(log p) (`LEGENDRE_HANKEL_RESULTANT_READOUT.md`).
  - Multivariate Q follows from line restrictions, with scalars stitched
    through a common point a: q_b(0) = Q(a)/lc_b.
  - DISW (arXiv 1107.2189v2, Definition 2): their HSSP needs
    f(x) = f(y) ⟺ Hx = Hy. lambda∘Q has three level sets, which are not
    H-orbits. So their Proposition 2 and Theorem 1 do not apply. Lemma 2
    is the same idea as their strong base (Lemma 1), for a general
    symmetry problem.
  - Known published nonabelian HSP families (class 2; F_p ⋉ F_p^m;
    Imran–Ivanyos for bounded primes) do not contain UT_{n+1}(F_p) with
    arbitrary H. This is the paper's scope claim (`main.tex`, Related
    work), pending priority review.
  - Repo-internal, unreviewed: `CLASS_THREE_HSP_THEOREM_DRAFT.md` and
    `BOUNDED_CLASS_METABELIAN_HSP.md` propose arbitrary-H HSP in
    metabelian groups of fixed class. UT_4 is metabelian: its derived
    subgroup, supported on (1,3), (1,4) and (2,4), is abelian. UT_5 is
    not, since [E13, E35] = E15. So the "only route" claim is made for
    n >= 4.
  - Decomposition (reviewer). H ∩ T comes from the abelian HSP on the
    translations T. Given the linear part A of an element of H, its
    translation lift comes from Ivanyos–Santha Cor 8 on
    (T/(H∩T)) ⋊ ⟨A⟩, where the hidden subgroup has order p and is not
    inside T. Normal H is handled because h is an ideal. The open piece
    is π(H) ≤ UT_n. Instances with π(H) public, H ≤ T, or H normal are
    therefore already solved without Rees. In the checks, H ⊄ T and H is
    not normal, but nothing was tested about how hard π(H) is to find.
- **Regime where Rees is the only polynomial route known here.**
  d log d = ω(log log p), so that exp(O(d log d)) is superpolynomial in
  the input size; n >= 4 fixed (class n must stay fixed); p
  superpolynomial; p >= 64 d^2. The cost is Rees on a group of dimension
  n(n+1)/2, with t = O(n^2 log p) oracle calls per label.

### 3.4 Motivation (why it is not an application)

1. The ingredients are published. The oracle family is the higher-degree
   Legendre PRF (RS 2002; Beullens et al. 2020; KKK 2020). Affine
   substitution symmetries of keys are used by KKK (§3B–3D: the orbit of a
   key under Möbius maps, "good / bad / ugly" keys).
2. The target is not used anywhere.
   - KKK's stabilizers live in PGL_2(F_p), and they are cyclic of order
     r′ | r with r′ | p^2−1 (KKK Lemma 3.1, local text line 280). So they
     are not p-groups.
   - Univariate keys of degree below p have trivial unipotent stabilizer,
     because translations are the only unipotent maps of F_p.
   - Multivariate Legendre PRFs with secret polynomial keys are not a
     published primitive. The published "Legendre MQ" has public diagonal
     quadrics (STATE line 1123).
   - Random keys have trivial H (checked).
3. A nontrivial non-normal H needs a planted symmetry, as in L1′. Its
   cryptanalytic use is that it detects "bad" keys and recovers g0 modulo
   N_U(K). Neither is an existing problem.

So L1 is the best constructed survivor. It shows that the Rees regime
contains natural-looking problems where Rees is the only known
polynomial route, but it is not an application. Paper wording, if the
owner wants it: "a constructed problem built from Legendre-PRF
ingredients", never "application".

## 4. A1 in detail (arithmetization-oriented permutations)

The open branch of S1 restored by the 11-05 check is "D fixed, p
superpolynomial". Arithmetization-oriented (AO) hash permutations fit it:

- state F_p^t with t = 3 to 12;
- p about 2^64 or 2^255, given in binary;
- the inverse power maps x^(1/alpha) of Rescue have degree about p.
  Aly et al., ToSC 2020(3): "low-degree power map in even steps and its
  high-degree inverse in odd ones" [abstract].

The natural symmetry object is the self-equivalence group
{(A,B) : E∘A = B∘E}. Baudrin, Felke, Leander, Neumann, Perrin and Stennes
(ToSC 2023(4) 299–329) develop exactly this "commutative cryptanalysis",
for affine A and B [abstract].

Reasons for the kill:

- (i) Designs make H trivial. Exact check (`ao_self_equivalence_check.py/.out`):
  p = 11, cube and inverse-cube layers, random invertible linear layers.
  Over all 1,771,561 A in UT_4(F_11), only A = I makes E A E^{-1}
  affine. The same holds for the bare S-box layer and for trivial linear
  layers. (Power maps commute with scalings, a torus, not with unipotent
  maps.)
- (ii) The published examples are over F_2 (Midori, Scream), where
  p = 2 <= class.
- (iii) For maps of degree >= p, distinct cosets can give functions that
  agree on most points. No injectivity promise holds for the labels
  without extension-field evaluation, and extension-field evaluation
  changes the group (finite non-reduced stabilizers).
- (iv) The permutations are public circuits, so the classical analyst
  sees their structure.

The classical complexity of the general self-equivalence problem in this
branch remains UNKNOWN. The kill is about motivation and promise, not
hardness.

## 5. Notes on the other rows

- **G1.** Grochow–Qiao (arXiv 1907.00309 [abstract]) show that tensor,
  p-group, cubic-form and algebra isomorphism are polynomially
  equivalent. They also reduce isomorphism of exponent-p groups of class
  c < p to class 2. So isomorphism questions do not single out class >= 3
  even in Rees's own family. In any case they are orbit problems under
  GL (11-02 Remark C).
- **G2.** Stab_U(β), with β ∈ Λ²L*⊗L the bracket and U ≤ GL(L) unipotent
  and explicit, is the stabilizer of a vector under a linear p-group action
  on a space of dimension poly(dim L). That is Luks or 11-02 Lemma A. The
  same holds for semifield autotopisms restricted to a unipotent group.
  Eick–Leedham-Green–O'Brien (Comm. Algebra 30 (2002) 2271–2295) is
  bibliographically confirmed only.
- **Q1.** Webster, Quintavalle and Bartlett (arXiv 2303.15615; NJP 25
  103018) give efficient algorithms for all diagonal Clifford-hierarchy
  logical operators of qubit CSS codes [abstract]. The qudit analogue is
  linear in the coefficients of the phase polynomial for explicit codes
  [argued]. The qubit case has p = 2, outside the Lazard range.
- **Survey ePrint 2026/2678** (Di Concilio et al.) is still unread. The
  search found no such listing. Kahrobaei–Flores–Noce (arXiv 2202.05917,
  Notices AMS 2023) and arXiv 2102.04120 are the reachable surveys; their
  nilpotent constructions are in the 11-05 table.

## 6. Independent check

One Claude subagent was briefed with the code and the repo's Legendre
notes, and told to attack (a)–(d). Its report is advisory. Each item was
checked against its scripts (`review_lie_linearization_check.sage/.out`,
`review_line_stitch_check.sage/.out`) and the cited files.

- **(a) Fixed-d kill: CONFIRMED after repair. Adopted.**
  - Use the squarefree or Hankel readouts. Line restrictions are
    irreducible only about 1/d of the time (measured 0.12–0.26) and
    squarefree with probability at least 1 − d/p − d(d−1)/p (measured
    0.98–1.00).
  - Handle lambda of the leading coefficient Q_d(b) by trying both
    padding conventions.
  - Stitching recovered Q/Q(a) in 4 of 4 exact cases.
  - **Correction adopted:** "d < p makes X·Q = 0 the stabilizer
    condition" is false. Exact witnesses at p = 5, n = 3, d = 3, 4 and at
    p = 7, n = 3, d = 6 have Q∘g = Q but X·Q ≠ 0. The right condition is
    p > nd, since D_X^{nd+1} = 0 on degree <= d.
  - This does not affect Lemma 3, whose stabilizers were computed by
    brute force. It does affect the "then linear algebra" step, which now
    assumes p > nd (automatic for p >= 64 d^2 when d >= n/64).
- **(b) "Only known route": GAP. Adopted as three corrections.**
  - The window is d log d = ω(log log p), not d = ω(1).
  - n >= 4 is needed, because the repo's unreviewed metabelian drafts
    cover UT_4.
  - The fingerprint is DISW's base idea. DISW's own promise (level sets
    = H-orbits) does not hold for lambda∘Q. L1 is the "more general
    setting" DISW mention after their Definition 2, and here
    correctness comes from (W). The decomposition attack is recorded in
    Section 3.3.
- **(c) Lemma 4: CONFIRMED.** Squarefreeness is not even needed: a
  multiplicity e < p forces v_π(R) >= e. The evaluation field needs
  p^K > (unknowns)·dp. The checks covered irreducible Q only.
- **(d) Weil constants: CONFIRMED** and inserted in Lemma 2.

## 7. Proposed STATE sharpening and next step

Proposed reason text for the row "Rees applications: none survived":
"second deep search (11-09): best survivor L1, the unipotent symmetry
group of a hidden multivariate Legendre function, natural ingredients
but constructed target; fixed degree killed by the repo's quantum
Legendre learners, circuit input killed by a Frobenius-root identity;
Rees is the only known polynomial route only for d log d = ω(log log p),
n >= 4, with F_p-point access."

Next hard question: can the linear-part image π(H) = HT/T be found
without Rees? That needs a translation-invariant fingerprint of
lambda∘Q, which is a Legendre hidden shift in degree >= 2. Equally, is
there a poly(d) quantum learner of Q? A positive answer to either kills
L1. A negative answer would still not make L1 an application. The
decisive missing item is external: a natural source of keys with
nontrivial unipotent symmetry.

Literature verified in this pass:

- [cited] DISW arXiv 1107.2189v2: Definition 2, Lemma 1, Proposition 2,
  Theorems 1–3, Proposition 1 (Ω(q^{1/2}) queries for HSSP(Aff_q)).
- [cited] Russell–Shparlinski quant-ph/0212016: abstract; M_d squarefree
  monic; Thm 6.
- [cited] KKK 2020: §3B–3D, Lemma 3.1, §4F.
- [cited] Beullens et al. 2020: introduction, quantum degree-one remark.
- [abstract] Grochow–Qiao 1907.00309; Baudrin et al. ToSC 2023(4);
  Aly et al. ToSC 2020(3) / ePrint 2019/426; Webster et al. 2303.15615.
- [bibliographic] Eick–Leedham-Green–O'Brien 2002.
