# Non-unique encodings for the Rees black-box corollaries (9 Nov 2026, AI only)

AI-written and AI-checked only; no human has checked any of it. No claim gate was changed
and the paper was NOT edited. Question (from the session that started this one): can
restriction (ii) of Remark rem:black-box-scope in
`2026-11-08-rees-blackbox-corollary-draft.tex` (unique encodings) be removed, for black-box
p-groups of class c < p in the Babai–Szemerédi model of Inui–Le Gall and
Ivanyos–Magniez–Santha, conditional only on Theorem thm:is-import?

## Verdict: (a) for the HSP with arbitrary H (new content: non-normal H), (b) for the chart

1. **Theorem N (proved here, conditional on thm:is-import; pending independent correctness and
   priority review).** The HSP for an arbitrary H in a
   black-box p-group of class at most c < p, of any exponent, with non-unique encodings, is
   solved with bounded error in time poly_c(s, l, w, log p, log 1/eps). It needs only the
   multiplication oracle (with its adjoint) and the hiding oracle f. It uses no identity test
   and no inverse oracle. The algorithm skips the kernel step. It runs the core directly on the
   free nilpotent Lazard ring F_{s',c}, with the pulled-back oracle f o Phi.
2. **Proposition O (proved here, elementary).** In the same model with all three standard
   oracles, the chart step of cor:black-box cannot be extended. Computing |G|, ker phi, an
   explicit chart, or a discrete logarithm needs Omega(sqrt p) identity-test queries, which is
   2^{Omega(l)}. This holds already for elementary abelian G of rank at most 2, and also when
   an f for H = G is supplied.
3. **The price.** The query count of Theorem N is that of thm:main at dimension
   m = dim F_{s',c} = O((l/log p + log_p(1/eps))^c), not at m <= L = floor(l/log2 p). For
   fixed c it is still polynomial in l and log(1/eps), and independent of s. Through s',
   log(1/eps) enters the dimension itself. In the unique-encoding count it enters only through
   the additive tau. Roughly, the exponent of L gets
   multiplied by c. For c = 2 the count grows from about 8 L^5 to about s'^10 / 4.

The mechanism is known. Pulling a hiding function back along a homomorphism from an explicit
group is the proof of Theorem 7 in IMS, and of Theorem 9 in Inui–Le Gall. **For normal H the
problem is already solved:** IMS Theorem 8 finds hidden normal subgroups of solvable black-box
groups with not necessarily unique encoding in polynomial time, unconditionally and for any
class and any primes. Inui–Le Gall's Theorem 9, Case 1 uses it. So what this note adds is
non-normal H only. It does so through the cover, the free nilpotent Lazard ring, with the
Rees core as the solver on it. Its priority is UNKNOWN. Of the sources read, none states a
result for non-normal H in nilpotent black-box groups of class at least 2 with non-unique
encodings, beyond Inui–Le Gall's P_{p,r} (see Sources). No novelty is claimed.

## The model (as in IMS Section 2 and Inui–Le Gall Section 2.3)

- Strings have l bits. Each element of G has at least one string, and each string encodes at
  most one element, so |G| <= 2^l. G = <g_1, ..., g_s> is given by strings for the g_i. The
  promises are: G is a p-group, its class is at most c < p, and p is given.
- Multiplication oracle: U_x |x,y,z> = |x, y, z XOR m(x,y)>. Here m(x,y) is some string for
  the product of the elements, and m is a fixed function of the two strings. Its behaviour on
  invalid strings is arbitrary. An in-place unitary V|x,y> = |x, m(x,y)> together with V^dagger
  gives U_x, by the appendix's construction (l.548): copy y, apply V, copy out, apply
  V^dagger, uncopy. That construction uses V^dagger, the unitary inverse of V. IMS (l.139 of
  the text) give "two oracles UG and its inverse UG−1". Read literally, that is the unitary
  inverse, so V^dagger is part of IMS's model. Inui–Le Gall's second oracle is
  V_G'|g>|h> = |g>|g^{-1}h>. With non-unique encodings that oracle need not equal V^dagger,
  because it may return a different string for h. So **access to V^dagger (or to the XOR
  form) is an explicit assumption here.** It is IMS's model and the usual convention for
  quantum oracles. Every coherent pull-back in IMS and Inui–Le Gall needs it to clean up its
  workspace. We also assume that valid inputs give valid outputs: m(x,y) is a string for the
  product.
- Hiding oracle: U_f |x,z> = |x, z XOR f(x)>, with labels of w bits and
  f(x) = f(y) iff x^{-1} y is in H for the encoded elements. In particular f is constant on the
  strings of one element.
- The identity test and the inverse oracle of the Babai–Szemerédi model are available, but
  Theorem N does not use them.

## Theorem N (exact statement)

Fix c >= 1 and assume Theorem thm:is-import. Let G, U_x, f be as in the model, with H <= G
arbitrary and eps in (0,1) rational. Put L = floor(l / log2 p), t_0 = ceil(log_p(4/eps)) and
s' = min(s, L + t_0). Let M = p^e be any known multiple of exp(G): M = p^L always works, and
M = p when the exponent-p promise is given. Let F = F_{s',c}(Z/M) be the free nilpotent Lie
ring of class c over Z/M on s' generators, in its Lyndon basis, with d = rank F
= sum_{k<=c} W(s',k) <= sum_{k<=c} s'^k. Here W(s',k) is the number of Lyndon words of
length k.

A quantum algorithm returns generators of H (as strings) with probability at least 1 - eps.
It makes no identity test and calls no inverse oracle. Its query count to f is as follows.

- (e = 1) At most Q_1 = c (d + ceil(log_p(6/eps))) prod_{k=2}^{c} B_k(g_k), with
  g_k = sum_{j=k}^{c} W(s',j) = dim gamma_k(F). That is thm:main's Q_q at m = d and error
  eps/2.
- (any e) At most b * c (d + ceil(log_p(6b/eps))) prod_{k=2}^{c} B_k(d), with b = d e <= d L.

For fixed c, both counts are polynomial in l and log(1/eps), and independent of s. Besides
the queries, it uses poly_c(s, l, w, log p, log(1/eps)) gates and multiplications. If s <= L + t_0, the
generator reduction (step 0) is skipped. The bound then holds with s in place of s', and the
error budget eps/4 of step 0 is unused.

### Proof

**Step 0 (generator reduction, only if s > L + t_0).** Put r = L + t_0. Draw r elements
y_j = g_1^{a_{j1}} ... g_s^{a_{js}}, with the a_{ji} uniform in {0, ..., p-1}, by
multiplications only. Let V = G / Phi(G) be the Frattini quotient. It is elementary abelian
of rank r_0 <= log_p|G| <= L, and the images of the g_i span it. The map a -> sum_i a_i g_i-bar
from F_p^s to V is a surjective linear map, so the y_j-bar are independent and uniform in V.
If they do not span V, they lie in some hyperplane. There are at most p^{r_0} hyperplanes,
each containing all r points with probability p^{-r}, so the failure probability is at most
p^{r_0 - r} <= p^{-t_0} <= eps/4. If the y_j-bar span V, the y_j generate G by Burnside's basis
theorem. A failure is not detected. It is charged to the error budget. The cost is
O(r s log p) multiplications. Rename the generators g_1, ..., g_{s'}.

**Step 1 (the pullback exists and is onto).** Exactly as in the draft corollary and in step 2
of the exponent-p^e note. log G is a Lie ring of class at most c with M log G = 0. F is free
in that variety. So there is a unique Lie ring map phi : F -> log G with x_i -> log g_i. Its
image is a Lie subring containing every log g_i, so phi is onto by the subgroup form of the
Lazard correspondence (Cor tb-correspondence(a)). F is a Lazard ring: it is finite of p-power
order and has class at most c < p. So Phi = exp o phi : (F, *) -> G is a surjective group
homomorphism, because the BCH product is a Lie polynomial.

**Step 2 (Phi on strings).** Lemma tb-evaluation's programs compute Phi(u) for the Lyndon
basis, and then the Lazard combination sum_j u_j Phi(w_j). They use products and powers
z^{a b^{-1} mod M} only. Every power is a positive power, by square-and-multiply. The string
one = g_1^M, computed by multiplications, serves as the identity input. No inverse, identity
test or string comparison is used (the control checks this: `theorems/universal_lazard_words.py`
branches only on classical integer coefficients). The output is a string Phi_str(u) that
encodes Phi(u). Different u in one coset of ker phi may give different strings. Phi_str and its
workspace are deterministic functions of u, computed by a fixed reversible circuit C_Phi of
U_x calls on valid strings.

**Step 3 (the key lemma: f o Phi_str hides Phi^{-1}(H)).** Put f~(u) = f(Phi_str(u)) and
H~ = Phi^{-1}(H). H~ is a subgroup of (F, *) and contains ker Phi. f depends only on the
encoded element: if x and y encode the same element, then x^{-1}y = 1 is in H. So
f~(u) = f~(v) iff Phi(u)^{-1} Phi(v) is in H, iff Phi((-u) * v) is in H, iff (-u) * v is in H~,
because Phi is a homomorphism and -u is the inverse of u in (F, *). The coherent oracle is
U_f~ = C_Phi^dagger (U_f on the Phi-string and label registers) C_Phi. U_f leaves the
Phi-string register unchanged, so C_Phi^dagger restores the workspace exactly, and
U_f~ |u,z> = |u, z XOR f~(u)>. This is one query of f and two runs of C_Phi. The pullback
works where the kernel step fails. The only register kept is the label, which is a function of
the element. The kernel step keeps the string Phi_str(u), which is not.

**Step 4 (e = 1: one call of thm:main).** F = F_{s',c}(F_p), with the Lyndon bracket table
reduced mod p, is an explicit Lazard chart of dimension d and class at most c < p. With U_f~,
it is an instance of Definition def:input-contract, case (a). Theorem thm:main at error eps/2
(rational) returns a basis b_1, ..., b_k of H~ (as a set, log H~ = H~) with probability at
least 1 - eps/2. It makes Q_1 queries, where g_k = dim gamma_k(F) = sum_{j>=k} W(s',j),
because the free nilpotent algebra is graded by length. Output the strings Phi_str(b_i). By
the subgroup form of Lazard, the group <b_1, ..., b_k> is H~. Phi is onto, so
Phi(H~) = H, and the outputs generate H. The total error is eps/4 + eps/2 < eps.

**Step 5 (any e: RtF on F itself).** F = (Z/M)^d with integer structure constants (the Lyndon
basis is a Z-basis of the free nilpotent Lie ring) and class at most c < p. This is the
"Setting" of appendix Section app:tb-ring, with m = d, every e_i = e, b = d e, and the oracle
U_f~ obeying the setting's convention (-x) * y. Run Algorithm RtF (Prop tb-recursion) from
K = 0, S = F, with Solve = Theorem thm:main at per-call error eps/(2b), rounded down to a dyadic
rational. This is the exponent-p^e note, steps 5 and 6, verbatim, with the acquired chart
F/K' replaced by F (that is, K' = 0). Each call on a correct branch is an instance of
def:input-contract (Lemma tb-quotient-oracle, (M3), Lemma tb-section-rank). There are at most
b calls on every branch. The time-out is replaced by thm:main's fixed shape, as in step 6 of
that note. Every socle met is a subquotient of (Z/M)^d, killed by p, so it has dimension at
most d, and each g_k is at most d. With B_k monotone, this gives the stated count. The output
is a generating set of H~. Push it forward by Phi_str. The error is eps/4 + eps/2.

**Costs.** Each query of f~ costs O_c(d (log M + A_c)) multiplications for the two runs of
C_Phi, plus O(l) qubits of workspace per string. The public arithmetic is that of thm:main at
m = d (poly_c(d, log p, w, log 1/eps)) and, for e > 1, of RtF (Lemma tb-howell-rounds,
O((b+1) d^5) ring operations mod M). log M <= l + log p. Every bound is polynomial because
d <= 2 s'^c and s' <= L + t_0 = O(l + log 1/eps). QED.

### Remarks on Theorem N

- *No identity test.* If the identity test is available, it can do three optional things. It
  can verify the exponent-p promise (all g_i^p = 1). It can find the exact e, using
  exp G = max_i ord g_i (step 1 of the exponent-p^e note). And it can shrink F by part of the
  kernel step: Fourier-sample u -> Phi_str(u) and keep K' = (samples)^perp only if
  Phi(K') = 1, by the identity test, and K' is an ideal. Then K' is an ideal of F contained in
  ker phi, so F/K' is still a valid cover, by the same argument as the draft's "deviation
  K' ⊊ K" paragraph. The abort rule d - dim K' > L must be dropped, because with non-unique
  strings K' is typically strictly smaller than ker phi (control part C). Proposition O shows
  that no procedure with o(sqrt p) identity tests reaches K' = ker phi in general.
- *Coset convention.* f must hide left cosets (x^{-1}y). If an f hides right cosets,
  precompose with x -> x^{M-1}, a product program.
- *What is not covered.* Coset-copy input (restriction (iv)). The nilpotent composition
  (restriction (iii)): the Sylow split needs element orders, and the small primes p <= c need
  Imran–Ivanyos, which assumes unique encoding. Class not fixed.
- *The comparison with Inui–Le Gall.* Their Proposition 10 asks for a polynomial-time
  bijection pi : G -> G' from the black box onto a group with a known HSP algorithm. They write
  that condition (iii), implementing pi^{-1} on strings, "seems very difficult" in the
  black-box framework. For Z_{p^r}^m ⋊ Z_p (Section 5, Theorem 11) they assume unique
  encoding and a given form of the generators. Theorem N replaces the bijection by a surjective
  homomorphism from an explicit group, Phi : F -> G, which needs no knowledge of G beyond
  p, c and a multiple of the exponent. That group has class 2 when r >= 2, since
  [y, x_i] = x_i^{p^{r-1}} is central. GAP confirms class 2 at (p,r,m) = (3,2,2), (3,3,2),
  (5,2,1) and (5,2,2). So for odd p, Theorem N covers its HSP with non-unique
  encodings and arbitrary generators, conditional on thm:is-import at degree 2. This is a
  consequence, not a new algorithm for that family, and it is AI-checked only.

## Proposition O (exact statement and proof)

**Statement.** Let p be prime and l = 2 ceil(log2 p). Consider black-box groups on strings
v in F_p^2 (other strings are invalid, and every oracle acts as the identity on them). The
multiplication oracle is |x,y,z> -> |x,y,z XOR (x+y)>, the inversion oracle is
|x,z> -> |x, z XOR (-x)>, and the generators are (1,0) and (0,1). The identity test is either
O_N |v,b> = |v, b XOR [v in N]> or the equality form |x,y,b> -> |x,y,b XOR [x - y in N]>. Here
N is either N_inf = 0, giving G = F_p^2, or N_a = F_p (1,a) for some a in F_p, giving G ≅ Z_p.
Every such G is a valid non-unique black box for an elementary abelian p-group (class 1,
exponent p). An oracle f for H = G (constant 0) may also be given. Then any quantum algorithm
that decides |G| = p versus |G| = p^2 with success at least 2/3 on every instance makes at
least sqrt(p)/12 identity-test queries.

**Proof (BBBV hybrid).** Only O_N depends on the instance. Multiplication, inversion and f
are fixed unitaries, and so are their controlled versions and adjoints. O_{N_a} and O_{N_inf}
differ exactly on the basis states whose query string lies in D_a = {(x, a x) : x != 0}. For
the equality form, the condition is x - y in D_a. The D_a are pairwise disjoint: a point
(x, y) with x != 0 lies on D_a only for a = y/x. Let psi_t be the state just before query t
on the instance N_inf, and q_a(t) its squared weight on D_a. Then sum_a q_a(t) <= 1, and the
standard hybrid bound gives ||psi^a_T - psi_T|| <= 2 sum_t sqrt(q_a(t)). By Cauchy–Schwarz,
sum_a ||psi^a_T - psi_T||^2 <= 4 T sum_t sum_a q_a(t) <= 4 T^2. Correctness on N_a and on
N_inf makes the acceptance probabilities differ by at least 1/3. For unit vectors,
|<psi|P|psi> - <phi|P|phi>| <= 2 ||psi - phi||, so ||psi^a_T - psi_T|| >= 1/6 for every a.
Then p/36 <= 4 T^2, so T >= sqrt(p)/12. Intermediate measurements are deferred. QED.

**Consequences.** Each of the following determines |G| on this family with no further
identity tests, so each needs Omega(sqrt p) = 2^{Omega(l)} queries: ker phi for the given
generators (|G| = p^{d - dim ker phi}); an explicit chart (its dimension is log_p|G|); and a
refined polycyclic presentation (|G| = prod r_i). Two more need a ≠ 0. On N_0 the string
(1,0) encodes the identity, and the answer there is the same as on N_inf. So restrict the
hybrid to the p - 1 instances N_a with a ≠ 0, which gives T >= sqrt(p-1)/12. Those two are
the discrete logarithm of (0,1) to base (1,0), which exists exactly when N = N_a with a ≠ 0,
and constructive membership in elementary abelian subgroups (IMS Corollary 5(b)). Three
conclusions follow.

- The chart step of cor:black-box and of Corollary E cannot be carried over.
- The route through a presentation cannot be carried over either. That route is "first
  compute a refined pc presentation by IMS's quantum Beals–Babai", which Ivanyos–Sanselme–
  Santha (arXiv:0707.1260, Section 3) use for black-box groups. It goes through IMS
  Theorem 6, which needs unique encoding, or through Corollary 5's oracles, which are
  unavailable here. A third route is IMS Theorem 7. It needs a hiding function of a normal
  subgroup to act as a secondary encoding, and none is available when H = G.
- Every subgroup in this family is normal, so IMS Theorem 8 solves its HSP, and so does
  Theorem N. This is a comparison of query counts in this model: the HSP takes polynomially
  many queries, the chart Omega(sqrt p). It is not a separation claim.

The hiding oracle does not rescue the chart in general. For H = G it is constant. (For H = 1
it is a unique encoding, and the kernel step then works through f, as in IMS Theorem 7.) The
bound is elementary and presumably folklore. Babai–Szemerédi prove the classical analogue for
constructive membership (as quoted by IMS, Section 3). We found no quantum statement to cite.

## Special case: quotients with quantum encodings (conditional sketch, NOT proved)

Suppose G = G~/N, where G~ is a unique-encoding black box and N is a normal subgroup of G~
that is solvable and given by generators. This is IMS Section 4.3 and Theorem 10, and
Watrous Section 4.2. Watrous's preparation of |N> (IMS Theorem 2: accuracy eps, time
polynomial in the input size and log 1/eps) gives quantum encodings |xN>. Then
u -> |Phi~(u) N> is a quantum hiding function of ker phi in the sense of IMS Lemma 9.
Phi~ is Phi evaluated in G~ with the same programs, and the power exponents are taken
mod M. G~ need not be a Lazard group. The programs are correct modulo N, because the
quotient map is a homomorphism and exponents mod M are valid in G. In-place multiplication
of the |N> register by the computed string, then uncomputing that string, gives
|u>|Phi~(u)N> with clean workspace. If the following error accounting is carried out, we
expect the kernel step of cor:black-box, the chart and the unique-encoding query count
c(L + tau) prod B_d(L) to return. The accounting must cover three things: one approximate
|N> per Fourier sample; the Phi-check and the ideal check, which need identity tests in
G~/N, that is, Watrous membership tests in N, with bounded error; and the abort test. None of
this is written here. The special case would be weaker than Theorem N for the HSP, since it
needs N by generators and a unique-encoding G~. It would be stronger in returning the chart
and the smaller query count.

## Finite control (exact, finite; proves nothing for other groups)

`2026-11-09-rees-nonunique-encoding-blackbox/nonunique_check.py`, run with
`/opt/anaconda3/bin/python` from the repo root at nice 19. Output is in `run.out` and
`results.jsonl`. GAP export: `export_groups_exp_p.g` -> `groups_exp_p.txt` (exponent p,
class < p, at most 3 generators, plus C3^2 and C5^2). Part B reuses
`../2026-11-09-rees-exponent-pe-blackbox/groups.txt`.

In the simulated black box, every element has 2 to 4 random 40-bit strings. The oracle
returns one of them, chosen pseudo-randomly but as a fixed function of the two input strings.
The algorithm side gets only generator strings and the oracle. The identity test count is 0
by construction: `UniversalLazardWords` branches only on classical coefficients. f is the
left-coset label of the element.

Results (`run.out`, 680 s in all at nice 19; no assertion failed):

| Quantity | Value |
|---|---|
| Part A, exponent p | 10 groups: C3^2, C5^2, 27_3, 81_12, 243_37, 125_3, 625_7, 625_12, 343_3, 2401_7 (2401_12 skipped, \|F\| = 7^6) |
| Part A, subgroups recovered | 1406 of 1406 (all subgroups; conjugacy class reps at 2401) |
| Part A, free cover | d = 2 to 6, class 1 to 3, p = 3, 5, 7 |
| Part B, exponent p^e | 14 runs on 8 groups (81_3, 81_4, 81_6, 243_2, 243_11, 243_12, 243_21, 625_3, 625_4, UT3_Z9), M = exp and M = p * exp where \|F\| <= 20000 |
| Part B, subgroups recovered | 825 of 825 |
| Part B, field instances validated | 2831, of which 226 non-abelian; largest call count 4 (cap b = 9) |
| Identity tests used | 0 |
| Part C, Fourier mass on (ker Phi)^perp of u -> string(Phi(u)) | 0.576 (81_12), 0.666 (243_37), 0.834 (625_7); 1 whenever ker Phi = 0 |
| Part C, readout = ker Phi | 0/20, 0/20, 4/20 in those three; the rest strictly inside ker Phi |

Part A checks that f o Phi hides Phi^{-1}(H) (sampled pairs), that Phi^{-1}(H) is a Lie
subalgebra containing ker Phi, and that the push-forward of its basis generates H. The field
solver is the oracle-only brute force U = {u : f~(u) = f~(0)}, a stand-in. It is NOT
Theorem thm:main. Part B validates each RtF call as in the exponent-p^e control. Part C shows
the failure mode concretely: with non-unique strings, the kernel readout of cor:black-box
returns an ideal strictly inside ker Phi. With an identity test that still gives a valid but
larger cover (Remarks). Without one it cannot even be checked. The control grades only. It
does not simulate coherence or the workspace clean-up of step 3, which is argued in the text.

## Claim gates that stay false

The paper is unchanged. Non-unique encodings stay "not covered" in the draft's
rem:black-box-scope until the owner's paper pass. Also unchanged: no human review; no novelty
(the pullback is IMS Theorem 7 and Inui–Le Gall Theorem 9 in kind); no speedup and no
separation; the nilpotent composition (iii) and coset-copy input (iv) are not covered;
class not fixed is not covered. Proposition O is a query lower bound for the chart, the order
and discrete logarithms in this model. It is not a hardness result for the HSP, which
Theorem N solves.

## Independent adversarial check

One independent AI subagent attacked the note against the files above and the five primary
texts. Verdict: HOLDS WITH FIXES. It found nothing fatal. It confirmed Step 3's exact
clean-up, Step 0, the counts of Steps 4 and 5, the BBBV constants of Proposition O, the class-2
claim and the source quotations. I checked each finding against the sources; the
dispositions follow.

1. Major: IMS Theorem 8 already solves the normal HSP with non-unique encodings
   (l.317–320 of the text; Inui–Le Gall Thm 9 Case 1 uses it). ACCEPTED, and checked in the
   IMS text. The verdict, the mechanism paragraph and Proposition O's conclusions now say that
   Theorem N adds non-normal H only.
2. The gloss on Inui–Le Gall's "open" remark was mine, and it conflicts with IMS Thm 8.
   ACCEPTED. The gloss is replaced by a note of the tension, left unresolved.
3. The discrete-log and constructive-membership consequences fail at a = 0. ACCEPTED. They
   are now restricted to a ≠ 0, with T >= sqrt(p-1)/12.
4. IMS's "its inverse" is V^dagger; the oracle that may differ is Inui–Le Gall's V_G'.
   ACCEPTED. The model paragraph is reworded, and valid inputs giving valid outputs is now
   stated.
5. Wording against TRAPS. ACCEPTED, all of it: "what this note adds"; the Rees review guard
   on Theorem N; "query-count comparison, not a separation"; "with o(sqrt p) identity tests";
   the placeholders filled; the control's grading-only scope stated.
6. The quantum-encoding sketch asserted results. ACCEPTED. It is now conditional, and it
   names the Watrous membership tests and the computation modulo N.
7. The next question assumed a known exponent multiple E. ACCEPTED. Obtaining E is now
   named as the first obstacle.
8. IMS Thm 7 as a third presentation route. ACCEPTED, one clause added.
9. "Subideal" was misused. ACCEPTED and reworded.

## Next hard question

The nilpotent composition (restriction (iii)) with non-unique encodings. The first obstacle
is obtaining a multiple E of exp(G) of polynomial bit length. Order finding is exactly what
fails with non-unique strings, so E must come from the input, for example from a matrix
group's order formula as in IMS Section 3, or be assumed. If E is given, the large primes
look reducible, but this is not checked. Given E and its factorization (Shor), the Sylow
projections g -> g^{a_p}, with the a_p from CRT, need no order
finding. Theorem N then applies to each G_p with p > c, with f restricted to G_p. The open
part is the small primes p <= c. Imran–Ivanyos (arXiv:2304.08376, Theorem 1) assume unique
encoding. Next command: write the Sylow split from a given exponent multiple in this folder,
and check whether Imran–Ivanyos's Proposition 1 reduction survives with f as a secondary
encoding (IMS Theorem 7 style). Acceptance: either a written reduction of the small-prime
part to a non-unique-encoding statement that is proved or cited, or a concrete step of
Imran–Ivanyos that needs unique strings, quoted from their text.

For the paper pass (owner's decision), the following is suggested. Replace restriction (ii)
of rem:black-box-scope by one sentence citing Theorem N and Proposition O. Add the
V^dagger assumption to the access-model paragraph of appendix-torsion-blackbox.tex (l.545).

## Sources (each read from the arXiv PDF by this AI session; pdftotext)

- Ivanyos, Magniez, Santha, quant-ph/0102014 (IJFCS 14 (2003)). Section 2: the model with
  non-unique encoding and the identity-test oracle. Theorem 8: hidden normal subgroups, with
  not necessarily unique encoding, in time polynomial in the input size + nu(G/N). Theorem 4 / Corollary 5: Beals–Babai,
  which needs oracles for element orders and for constructive membership in elementary abelian
  subgroups. Theorem 6: unique encoding. Theorem 7: f as a "secondary encoding", with
  phi(alpha) = f(h_1^{alpha_1} ... g^{-alpha}). Lemma 9: hiding by orthogonal quantum states.
  Theorem 10: G~/N with N solvable and given by generators, via Watrous's |N>.
- Watrous, quant-ph/0011023, Sections 1 and 4.2: unique encodings are assumed; abelian factor
  groups G/H are handled with copies of |H> "despite the fact that we do not have unique
  classical representations".
- Inui, Le Gall, quant-ph/0412033 (QIC 7 (2007) 559–570). Section 2.3: the model, with
  quantum multiplication and inversion oracles and an equality-test oracle, of which a
  classical one suffices. They write that the abelian HSP with non-unique encoding "is open"
  (l.170–172 of the text). That is their remark, not ours. It sits in some tension with IMS
  Theorem 8, which appears to cover abelian groups, since every subgroup of an abelian group
  is normal. We did not resolve this. Theorem 9 (P_{p,r}): uses f'(u,v) = f((X^p)^u (Y^p)^v). Proposition 10
  and Section 5, as quoted above.
- Ivanyos, Sanselme, Santha, arXiv:0707.1260, Section 3: the refined pc presentation model.
  For black boxes they compute the presentation by IMS's quantum Beals–Babai.
- Imran, Ivanyos, arXiv:2304.08376: unique encoding throughout (l.95, 153, 258 of the text).
- A web search (9 Nov) for non-unique-encoding HSP results for nilpotent groups found nothing
  beyond these sources.
