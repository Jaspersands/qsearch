# Exponent p^e for the black-box corollary (9 Nov 2026, AI only)

AI-written and AI-checked only; no human has checked any of it. No claim gate was changed
and the paper was NOT edited. Question (from the session that started this one): can the
exponent-p restriction (i) of Remark rem:black-box-scope in
`2026-11-08-rees-blackbox-corollary-draft.tex` be removed with nothing assumed beyond
Theorem thm:is-import?

## Verdict: (a), with one wording fix and no new mathematics

Yes. Corollary E below is proved from Theorem thm:main (hence conditional only on Theorem
thm:is-import) and lemmas the full version already proves (AI-checked): tb-words,
tb-evaluation, tb-correspondence, tb-kernel, (M1)-(M3), tb-quotient-oracle, tb-section-rank
and Proposition tb-recursion. Nothing in the route uses Corollary cor:fpt-r, the
free-coordinate theorem, the i.i.d. label law or Schedule 2.

The "conditional" status quoted in the scope remark is a mislabel, not a gap:

- Theorem thm:ring-to-field (main.tex:1152) is titled "conditional" because its part (ii)
  uses Corollary cor:fpt-r ("Conditional on the Rees composition, as in Corollary
  cor:fpt-r"). Corollary cor:fpt-r is conditional on Theorem free-coordinate(iii) and the
  i.i.d. label law of Lemma s3-law (main.tex:1105-1145).
- The exponent-p^e route uses only part (iii), the outer recursion. Its full proof is
  Proposition tb-recursion (appendix-torsion-blackbox.tex:406-515), stated for an arbitrary
  field solver. With Solve = Theorem thm:main it needs nothing more. The appendix itself says
  so (l.832-835: routes R1 and R2 "do not use Corollary cor:fpt-r").
- The phrase "conditional on Theorem ring-to-field(iii)" in Prop black-box(ii)
  (main.tex:1188) comes from the 2 Nov check. That check found (iii) correct only "given two
  unstated stop rules" (handoff, 2026-11-02 entry). Those stop rules are now Proposition
  tb-recursion's stop rules 1 and 2, with a proof. So the phrase is stale. "Conditional,
  like Theorem thm:main, only on Theorem thm:is-import" is the accurate status.

It is not new as a mechanism. Ivanyos, Sanselme and Santha already reduce the HSP in any
subgroup- and quotient-closed class of constant-class groups to p-groups of exponent p, with
hidden subgroup trivial or of order p (arXiv:0707.1260, Section 3, Theorem 2 by Lemmas 1-3).
Their model is refined polycyclic presentations with polynomial-time collection. Their
Lemma 3 handles p > class by passing to G* = Omega_1, which is a subgroup by regularity. So
"the exponent-p case implies the exponent-p^e case" is known in their model. What is added
here is the direct black-box route through the acquired Lazard chart, with explicit counts.
It needs no pc presentation, no constructive membership and no collection. Imran and
Ivanyos (arXiv:2304.08376, Prop. 1) reduce instead to semi-elementary sections, which need
not have exponent p, so their reduction is not the comparator here. Both sources were read
from the arXiv PDFs by an AI session only.

## Corollary E (exact statement)

Fix c >= 1 and assume Theorem thm:is-import. Let G = <g_1,...,g_s> be a black-box group with
unique l-bit encodings and a coherent multiplication oracle |x,y,z> -> |x,y,z XOR xy>. G is
promised to be a p-group of class at most c < p, of any exponent, and p is given. Let f be a
coherent hiding function of label width w for an arbitrary H <= G, with f(x) = f(y) iff
x^{-1}y in H, and let eps in (0,1). Put L = floor(l / log2 p),
tau' = ceil(log_p(6L/eps)) and B_d as in (eq:Bd).

A quantum algorithm returns generators of H with probability at least 1 - eps. It makes no
query to f before it has an explicit chart. On every branch it makes at most L field calls
and at most

    Q_worst = L * c (L + tau') * prod_{d=2}^{c} B_d(L)

queries to f. That is polynomial in l and independent of s and of the exponent. Write
b = log_p|G|, n = d(log G), the number of cyclic factors, which equals log_p|Omega_1(G)|,
and R = d([log G, log G]). On the event, of probability at least 1 - eps/4, that the kernel
step returns ker Phi, the queries number at most

    sum over the <= b calls j of c (k_j + tau_j) prod_d B_d(g_{d,j}),

with k_j <= n, g_{d,j} <= min(k_j, R) and tau_j = ceil(log_p(6b/eps)). This is at most
b * c (n + tau) * prod_d B_d(min(n,R)). Its other cost is poly_c(s, l, w, log p, log(1/eps))
gates and black-box multiplications. For exponent p (b = n, a single call) this is the count
of Corollary cor:black-box. The price of exponent p^e is at most a factor b <= e*n in
queries.

## Proof

Throughout, M = p^e is the exponent of G, F = F_{s,c}(Z/M) is the free nilpotent Lie ring
in its Lyndon basis w_1..w_d, and Phi = exp o phi : F -> G, where phi is the unique Lie
ring map with x_i -> log g_i.

1. **Exponent.** Class < p makes G regular. Lazard gives a stronger statement:
   p^j log g_i = 0 for all i implies p^j log G = 0, since p^j kills every bracket monomial
   in the log g_i, and they generate log G. So exp G = max_i ord(g_i). Compute
   g_i^{p^j} by repeated p-th powers, j <= e <= L, at O(s L log p) multiplications. Identity
   test: unique encoding, x*x = x. Any known p^E >= exp G would also do, for example
   E = L; it costs only log M.
2. **Phi is computable and is a surjective additive map.** log G is a Lie ring of class
   <= c with M log G = 0, and F is relatively free in that variety (the free Lie ring of
   class c over Z is a free module; base change). So phi exists, and it is onto by the
   subgroup form of Lazard (Cor tb-correspondence(a)). Its values are computed by Lemma
   tb-evaluation at modulus M: the programs Pi_+ and Pi_[] with powers z^{a/b} taken as
   z^{ab^{-1} mod M}, at Prop black-box(i)'s multiplication counts. Inverses are z^{M-1}.
3. **Kernel.** u -> enc Phi(u) hides ker phi in (Z/M)^d (additive, unique encodings).
   Lemma tb-kernel at delta = eps/4 uses t = min(d, L) + ceil(log_p(8/eps)) samples. The
   rank of (ker phi)^perp is n <= b <= L. The public checks are Phi(v) = 1 on a generating
   set of K' (Phi is additive, so this checks K' <= ker phi) and the ideal test (dim-K'
   generators times d brackets). Abort if a check fails or if log_p|F/K'| > L. With exact
   transforms every sample lies in (ker phi)^perp, so K' >= ker phi and every
   sampling failure is caught. An undetected K' that is not equal to ker phi comes only from
   the approximation error (TV <= eps/8). If it passes both checks, then K' < ker phi and
   K' is an ideal. Then F/K' is a finite Lazard ring of class <= c, and
   E' : F/K' -> G is a surjective Lie ring map, hence a group map. f o E' hides
   E'^{-1}(H), which contains ker phi / K', and everything below runs on F/K' unchanged,
   with b' = log_p|F/K'| <= L. Correctness is unaffected; only the count changes, and the
   worst-case bound covers it. This is referee finding 2 of the e = 1 corollary, verbatim.
4. **Chart.** (M1) with S = F and the ideal K' (Smith or Howell form over Z/M,
   poly(d, log M)) presents L' = F/K' as (+)_i Z/p^{e_i}. It gives basis lifts u_i in F,
   the coordinate map, and structure constants from F's integer bracket table. The map
   E(t) = Phi(sum t_i u_i) is a Lazard combination of the precomputed Phi(u_i), at
   O_c(n(log M + A_c)) multiplications. This is the "setting" of the appendix Section
   app:tb-ring with b' <= L and B <= poly(l, w).
5. **RtF with Solve = Theorem thm:main.** Run Algorithm RtF (Prop tb-recursion) on L', with
   oracle f o E and per-call error eps/(2b'). Each call is a genuine instance of
   Definition def:input-contract:
   - Omega = M[p] for the current section M = S/K is an ideal of M, killed by p, hence an
     explicit F_p-Lie algebra by (M3).
   - Its class is <= c < p (Lemma tb-section-rank).
   - Its BCH group is the subgroup exp(Omega) of (M,*), since BCH_c uses only brackets
     inside Omega.
   - On every branch where earlier calls were correct (K <= h <= S),
     f o E o sigma o iota_M hides iota_M^{-1}((h/K) cap Omega) with the left-coset
     convention (Lemma tb-quotient-oracle). Each local query is one query of f and two
     evaluations of E o sigma o iota_M.

   Prop tb-recursion then gives at most b' calls on every branch and output h with
   probability >= 1 - eps/2 (first-error union bound). Round eps/(2b') down to a dyadic
   rational, since thm:main takes a rational error. Push forward the generators by E;
   they generate H (Cor tb-correspondence(a)). The total error is
   eps/4 + eps/2 < eps.
6. **Invalid branches; the time-out is not needed.** Step 2 of RtF stops a call "after
   T_Solve steps". Theorem thm:is-import gives "time polynomial in M and log p, where the
   polynomial depends on d", with no explicit polynomial, so an explicit time-out is not
   available as written. It is also not needed. Theorem thm:main's procedure has a fixed
   shape: Q_q queries, a recursion tree fixed by (p, m, g_d, eps) (main-core.tex l.506),
   and no repeat-until loop (grep: none in main-core.tex). Its Schedule-1 solver is total and
   deterministic on arbitrary label columns (Rem main-solver; Thm is-import says "given any
   lambda_1..lambda_M"). So thm:main's query and gate bounds hold for every oracle unitary,
   hiding or not. A call made after a wrong earlier answer therefore costs at most the
   valid-instance bound for its (k_j, g_{d,j}), and RtF's worst-case statement holds with the
   time-out deleted. Also, k_j <= n' <= b' <= L and g_{d,j} <= k_j, and B_d is monotone,
   which gives Q_worst.
7. **Counts.** On the good event: b' = b, n' = n, and every socle has dimension <= n. Its
   g_d (d >= 2) lies inside [M,M][p], which has dimension <= R by Lemma tb-section-rank.
   Public arithmetic: Lemma tb-howell-rounds, O((b+1) n^5) ring operations mod M per run,
   each O(log^2 M). Gates: thm:main's poly_c(k_j, log p, w, log(b/eps)) per call, plus
   O_c(n(log M + A_c)) multiplications and O(l) controlled-constant loads per local
   query. log M <= l + log p because M <= |G| <= 2^l. If G = 1, test it first
   (every g_i * g_i = g_i) and output {1}.

## Finite control (exact, finite; proves nothing for other groups)

Script `2026-11-09-rees-exponent-pe-blackbox/exponent_pe_check.py`
(`/opt/anaconda3/bin/python`, run from the repo root). GAP export:
`export_groups.g` -> `groups.txt`. Output: `run.out` and `results.jsonl`.
Groups: every non-abelian SmallGroup of order 3^4, 3^5 and 5^4 with class < p and exponent
> p, seven of order 5^5 (exponent 25 or 125, class 2-4), and UT_3(Z/9). Each is given to the
algorithm only as 40-bit opaque handles over a hidden permutation representation. For each
group it runs:

- the exponent from generator orders through the oracle;
- Phi on F_{s,c}(Z/M) with the certified words of `theorems/universal_lazard_words.py`;
- ker Phi by additive Schreier relations, a finite-check device that stands in for Fourier
  sampling;
- the kernel readout of Lemma tb-kernel from t samples of the exact-QFT law, uniform on
  (ker Phi)^perp, 20 trials;
- the chart by Smith form, with E graded bijective and a homomorphism on 400 sampled pairs;
- RtF for every exported subgroup: all subgroups at order <= 625, conjugacy class
  representatives at 3125.

Every field call is validated as an instance of Definition def:input-contract:
antisymmetry, Jacobi (sampled), class <= c, the lift being a group map (sampled), and f
hiding the true (h/K) cap M[p] (sampled pairs). The field solver is an oracle-only brute
force, a stand-in for Theorem thm:main; it is NOT Theorem thm:main.

Results (`run.out`, 710 s in all at nice 19):

| Quantity | Value |
|---|---|
| Groups | 48 |
| Primes and orders | p = 3: 3^4, 3^5, 3^6; p = 5: 5^4, 5^5 |
| Class | 2, 3, 4 |
| Exponent | 9, 25, 27, 81, 125 |
| Free-cover rank d | up to 14 |
| Hidden subgroups | 5359 |
| Recovered from handles | 5359 |
| Field instances validated | 13900, of which 2684 non-abelian |
| Kernel readout = ker Phi | 958 of 960 trials |
| Largest call count | equals the cap b (243_24 at b = 5; 81_6 and 625_6 at b = 4) |
| N1 cover-socle misses | 3518 subgroup cases |
| N2 frozen-normalizer non-ideals | 2914 subgroup runs |

The two readout failures (81_3 and 243_2, 19/20 each) are within the Lemma tb-kernel bound
p^{n-t}. In both, the sampled K' was strictly larger than ker Phi, which the Phi-check
catches. No run broke the call cap, and no assertion failed. None of the asserted
invariants failed (exponent from orders, E bijective and a homomorphism, instance validity,
the hiding of the true U, K <= h <= S, calls <= b).

This exercises the algebra of the composition: chart acquisition at e > 1, the RtF sections
and the push-forward. It does not exercise Theorem thm:main, the QFT approximation or any
cost.

Two negative controls are reported. N1 counts the subgroups with H cap Omega_1(G) not
contained in Phi(F[p]) = p^{e-1} log G, where restricting to the cover's socle and pushing
forward fails (Prop black-box(iii)). N2 counts the runs in which some K' is not an ideal of
the whole chart, where quotienting by K' without recomputing the idealizer (the
frozen-normalizer error) is undefined.

## Claim gates that stay false

The paper is unchanged: exponent p^e is still "not claimed" in main-core.tex and in the
draft's rem:black-box-scope until the owner's single paper pass. Also unchanged: no human
review; no novelty (the reduction is ISS 2012 Theorem 2 in kind); no speedup and no
separation; the black-box nilpotent composition (thm:bb-envelope) unclaimed; non-unique
encodings and coset-copy input not covered; class not fixed not covered.

## Disposition of the independent AI check

One independent AI subagent attacked Corollary E against the files above. Verdict: HOLDS
WITH FIXES, no counterexample, no dependence beyond thm:is-import. I checked each finding
against the source; they are dispositioned as follows.

1. Cite Prop tb-recursion with Solve = thm:main, never "Theorem ring-to-field(iii)". The
   proof of (iii) at appendix l.519-525 takes Solve = part (ii), which is the conditional
   part. ACCEPTED, and adopted above. The appendix wording at l.832 and l.847 should change
   in the paper pass.
2. The time-out is not effective, because thm:is-import gives no explicit polynomial. Cost
   bounds on invalid branches need thm:main's costs to hold for an arbitrary oracle; the
   time-out bounds steps, not queries. ACCEPTED. Step 6 above already uses this. Checked:
   the running-time paragraph (main-core.tex:577) never uses item (iii) of
   def:input-contract, and Schedule 1 takes "any lambda" (l.451). Paper pass: add a
   one-line remark after thm:main and cite it in place of the time-out.
3. The kernel step for e > 1 is sound. Because Phi is additive, killing additive
   generators of K' already gives K' <= ker Phi, so incomparable K' are caught. ACCEPTED
   (step 3).
4. and 5. The invariant, the error budget and the instance validity were checked.
   ACCEPTED. The coset convention is stated in Corollary E (x^{-1}y). If an f hides right
   cosets, precompose with x -> x^{M-1}.
6. tb-words and tb-evaluation hold at M = p^e. Phi on Lyndon words comes from nested
   Pi_[] along the standard factorization. ACCEPTED; this is what the control implements.
7. "Exponent = max generator order" needs its short proof, the identity encoding (z*z = z)
   and the loop bound j <= L. ACCEPTED, all three are in step 1.
8. Three minor points. thm:main needs a rational eps, so round eps/(2b') down to a
   dyadic rational. For c = 1 and p = 2 the kernel QFT is over Z/2^e, outside Lemma
   qft-mod's odd case; cite the standard transform, as the appendix does at l.1446, or
   note that c = 1 is the abelian HSP. Correctness still needs each call's instance to be
   valid on the good branch; obliviousness bounds only cost. ACCEPTED, all minor.

## Next hard question

Restrictions (ii) and (iv) of rem:black-box-scope are now the real boundary. (ii) is
non-unique encodings, the setting of Inui and Le Gall and of quotient groups G/N given by
generators of N. (iv) is coset-copy input, which needs E^{-1} coherently. The concrete next
question is whether E^{-1} : G -> L_G can be computed coherently. One way is an exact
abelian HSP on (Z/M)^n x Z/M for (t,a) -> enc(E(t) -_Lazard a log g), in the style of the
transversal computation of Imran and Ivanyos (Section 2.2). That would give coset-copy input
and quotients G/N, with N given by generators, at once. Next command: write the coherent
E^{-1} construction and its exactness argument in this folder. Acceptance: an exact
finite check that E^{-1}(E(t)) = t on all of L_G for the groups above, plus a written
error/exactness bound. For the paper pass, replace restriction (i) of rem:black-box-scope by
Corollary E, or by one sentence citing Prop tb-recursion with Solve = thm:main and ISS
Theorem 2.
