# Groups with an abelian subgroup of index p: is the HSP known for arbitrary H? (2026-11-12)

**Status: AI-checked, pending human review.** One AI session read the primary sources
listed below and ran one exact finite check. The check only falsifies (TRAPS 7). No `.tex` file was
edited. There was no network access, so Decker–Ivanyos–Santha–Wocjan (arXiv:1107.2189) was not read.

**Claim checked** (`2026-11-12-rees-direct-twist-class3.md` §4 and its candidate paragraph).
p-groups of class < p with an abelian normal subgroup of index p (filiform, F_p ⋉ F_p^m) are
solved for an arbitrary hidden subgroup, with no Rees cover, by composing ISS 2012 Thm 2 with
IS 2015 Cor 8.

**Verdict: CORRECT WITH CONDITIONS.** The mathematics holds once the conditions C1–C5 at the end
are added. As worded, the claim overclaims in three places: "filiform", the missing constant-class
hypothesis, and the credit to ISS Thm 2. It also leaves one step implicit: H = 1 and H ≤ F_p^m.

Sources (local copies in the session scratchpad `lit-quantum/`):
- ISS: arXiv:0707.1260 §3 (Thm 2, Lemmas 1–3).
- IS: arXiv:1503.09016 §1 (Def. 4, Thm 5, Cor 6, Prop 7, Cor 8) and §4.1 (proof of Prop 7).
- BCvD: Bacon–Childs–van Dam, quant-ph/0504083 §3 Lemma 1, §4.2, §6 Thm 6.
- DHIS: arXiv:1305.1543 §1.
- Morales, arXiv:2608.05321 §1.1.
- Imran–Ivanyos, arXiv:2304.08376 §1.
- The citation lists `cit_1503.09016.json` and `cit_0707.1260.json`.

## 1. ISS 2012, Theorem 2: exact hypotheses

- **Input model.** In §3 the groups are given by *refined polycyclic presentations*, with elements
  stored as normal words and a polynomial-time collection procedure. ISS note that such a procedure
  exists for constant class. They also note that a presentation of a solvable *black-box* group
  can be computed by the quantum Beals–Babai method of IMS. Normalizers, subgroups and quotients
  are computed in this model.
- **Class of groups.** C must have *constant nilpotency class* and be *closed under taking
  subgroups and factor groups*.
- **Reduced instances.** Lemma 2 (Algorithm 1) calls a procedure P on the terms G_i of a refined
  polycyclic series of N_G(H̃)/H̃. These terms are sections of G, so they lie in C. The calls
  start at the bottom term, so the promise |hidden ∩ G_i| ≤ p holds automatically. There are
  O(log_p² |G|) calls. Lemma 3 then replaces a section by G* = {x : x^p = 1}, which is a subgroup
  when p > class (for p ≤ class, ISS use FIMSS). The result is a group in C of exponent p, with a
  hidden subgroup of order 1 or p.
- **Oracle form.** P receives the restriction of f to lifts of the section's elements. Nothing
  beyond the standard hiding function is needed. P must also handle H = 1 (Algorithm 1 branches
  on "P returns ⟨h⟩").

## 2. IS 2015, Proposition 7 and Corollary 8: exact hypotheses

- **Groups.** G_B = F_p ⋉ F_p^m for *any* B ∈ GL_m(F_p) with B^p = I. A single Jordan block is not
  required. The group is given concretely as the matrices [[B^x, v],[0,1]] with quantum encoding
  |x⟩|v⟩, so B is explicit. The class d is the least d with (B − I)^d = 0.
- **Hidden subgroups.** Cor 8 is stated for HSP(G, ℋ) only, where ℋ is the family of subgroups of
  order p *not contained in* N = 0 × F_p^m (Def. 4 makes ℋ part of the problem). The proof of
  Prop 7 says ℋ = {H_v : v ∈ F_p^m}. This needs every (1, v) to have order p, i.e.
  (B − I)^{p−1} = 0, i.e. d ≤ p − 1. That holds in our regime c < p.
- **Constants.** Cor 6 needs d constant, and so Cor 8 says "if the nilpotency class is constant".
  m is unrestricted. The proof of Thm 5 assumes p > d; the constant-p case goes through DIS-W and
  FIMSS. The algorithm is quantum polynomial time with bounded error. It depends on IS Thm 3 (the
  SDE solver), which is the same import as our Thm is-import.
- **Cosets.** Def. 4 uses right cosets (Hx) while the proof of Prop 7 uses left cosets. Inversion
  converts between the two.
- **Cases outside ℋ.** H = 1, H ≤ N, and |H| > p are *not* covered by Cor 8. They are easy, by the
  standard reduction of BCvD Lemma 1 (valid for every A ⋊ Z_p):
  1. Find H₁ = H ∩ N by abelian HSP on N.
  2. If H₁ is not B-invariant, then H = H₁, and we are done.
  3. Otherwise pass to G/H₁ ≅ G_{B'} with B' induced on F_p^m/H₁; the class does not increase.
     The residual hidden subgroup there is trivial or lies in ℋ.
  4. Run Cor 8 (with a time cap) and test the output generator with one query, f(g) = f(1).
     This is BCvD §4.2's test for the trivial subgroup.
  The error is one-sided: if H/H₁ = 1, the test always fails, so we output H₁.

## 3. Closure, and the exponent-p members

Let C_c be the p-groups of class ≤ c (c fixed, c < p) that have an abelian subgroup of index ≤ p.
Such a subgroup is maximal, hence normal.

- **Subgroups.** For K ≤ G, K ∩ A is abelian and normal in K, of index [KA : A] ≤ p.
- **Quotients.** AM/M is abelian and normal in G/M, of index ≤ p.

So C_c is closed under the operations that ISS Thm 2 uses. The class must be stated with "index
≤ p": a quotient can be abelian.

**Exponent-p members.** Let G ∈ C_c have exponent p. Then either G is abelian, or G = A ⋊ ⟨g⟩
with A ≅ F_p^m elementary abelian and g ∉ A of order p, so G ≅ G_B with B = conjugation by g.
Conversely, G_B has exponent p iff d ≤ p − 1. So after the reduction to exponent p, every instance
is abelian or an IS group G_B.

**The filiform caveat.** "Filiform" is not the right description. Example: L_{5,6}, with
[x1,x2] = x3, [x1,x3] = x4, [x1,x4] = x5 and [x2,x3] = x5. It is filiform of class 4, and it has
*no* abelian ideal of codimension 1, because [a x1 + b x2, x3] = a x4 + b x5. This was checked
exactly at p = 5 and 7 (below). Only the model filiform algebra L_n qualifies. At fixed class it
has fixed dimension c + 1, so it is already a case of BCvD Thm 6, with m fixed and arbitrary H.
IS Cor 8 adds groups of bounded class with *m unbounded*, e.g. B with many Jordan blocks of
size ≤ c.

## 4. Cost in our input model (structure constants of the Lazard algebra, exponent p, fixed c < p)

- **Finding A.** If [L,L] is central (class ≤ 2), ISS Thm 1 applies directly. If class ≥ 3, the
  abelian ideal of codimension 1 is *unique*: two of them, A₁ ≠ A₂, would make A₁ ∩ A₂ central of
  codimension 2, forcing class ≤ 2. It equals C_L([L,L]): for x ∉ A, x centralizes [L,L] = N(A)
  iff N² = 0, where N = ad_x|_A. Finding it is linear algebra.
- **The isomorphism to G_B.** Pick x ∉ A and set B = exp(ad_x)|_A. Then exp(a)·exp(x)^t ↦ (t, a)
  is an isomorphism onto G_B, because (v₁k^{t₁})(v₂k^{t₂}) = (v₁ + B^{t₁}v₂)k^{t₁+t₂}. Both
  directions are BCH polynomials of degree < c, so they cost poly(m, log p) for fixed c. The
  oracle f is composed with the inverse map.
- **Reductions.** The BCvD Lemma 1 reduction stays inside the same group family, so ISS Thm 2
  (and its polycyclic-presentation model) is **not needed** in our exponent-p setting. ISS Thm 2
  is needed only for groups of higher exponent in C_c, i.e. in the setting of cor:black-box-pe.
  There ISS's own model applies: black-box groups via quantum Beals–Babai. Converting a Lazard
  chart to Mal'cev normal words is also polynomial for fixed c.

So the composition runs in quantum polynomial time with bounded error, conditional on the same
import (IS Thm 3), in our model. It is not exact.

## 5. Is the composition stated anywhere?

- IS §1 says Cor 6 and Prop 7 together "get rid of the assumption that m is constant in the result
  of [5]" (BCvD). But IS describe [5] as being for the family ℋ, and Cor 8 is stated for ℋ only.
- BCvD Thm 6 *is* for arbitrary H, for fixed r = m. §6 works out a single Jordan block and says
  the extension to other Jordan types "will be clear". Its Lemma 1 is rigorous.
- DHIS §1 says only that "the HSP in Z_p^m ⋊ Z_p" reduces to multidimensional HPGP (via DISW,
  not read).
- Morales (2608.05321) treats scalar actions with bounded rank, a different family, and does not
  cite IS.
- Imran–Ivanyos has p bounded.
- The six works that cite IS (`cit_1503.09016.json`) contain no other HSP paper.

**Result: the composition (BCvD Lemma 1 + IS Cor 8, arbitrary H, m unbounded, constant class) is
NOT FOUND stated.** It is routine and close to IS's remark. This was not an exhaustive search.

**Side finding (existing text).** Core main-core.tex line 210 says that BCvD solve F_p ⋉ F_p^m
"for hidden subgroups of order p not contained in F_p^m". That understates BCvD Thm 6, which
covers arbitrary H for constant m. It follows IS's framing. It should be corrected.

## Conditions (verdict CORRECT WITH CONDITIONS)

- **C1.** The class c is *constant* and c < p. Both ISS Thm 2 and IS Cor 8 require constant class.
  "class < p" alone is not enough.
- **C2.** The family is "groups with an abelian subgroup of index p" (exponent p: exactly
  F_p ⋉_B F_p^m). It is not "the filiform algebras". L_{5,6} is filiform with no such subgroup.
  The model filiform group at fixed class is already a case of BCvD Thm 6.
- **C3.** H = 1, H ≤ F_p^m and |H| > p are handled by BCvD Lemma 1 plus a one-query check, not by
  Cor 8. ISS Thm 2 alone leaves these cases to the subroutine.
- **C4.** In the exponent-p Lazard setting the right citation is BCvD Lemma 1. ISS Thm 2 is valid
  there but unnecessary, and it is stated in the refined-polycyclic model. It is needed only above
  exponent p.
- **C5.** The result is bounded error and conditional on IS Thm 3, like ours. The composition is
  unstated in the literature we read, so the paper should present it as an observation, not as a
  citation.

## Proposed Related Work sentence (for the integrator; not inserted)

> Bacon, Childs and van Dam reduce an arbitrary hidden subgroup of $\Fp \ltimes \Fp^m$ to the
> trivial subgroup or a subgroup of order $p$ not contained in $\Fp^m$, which one query
> distinguishes~\cite[Lemma~1 and Section~4.2]{BaconChildsVanDam2005}, and solve the problem for
> constant $m$~\cite[Theorem~6]{BaconChildsVanDam2005}; composing this reduction with
> \cite[Corollary~8]{IvanyosSantha2015} solves the HSP for an arbitrary hidden subgroup in these
> groups whenever the class is constant, with $m$ unbounded (a routine composition that we have
> not found stated), so the Lazard groups of fixed class $c<p$ that have an abelian subgroup of
> index $p$ need no cover.

This sentence replaces the current BCvD sentence on line 210, including its "for hidden subgroups
of order p not contained in F_p^m" clause. The final sentence of the candidate paragraph in
`-direct-twist-class3.md` ("handled by combining [ISS, Thm 2] with [IS, Cor 8]") should cite BCvD
Lemma 1 in place of ISS Thm 2.

## Finite check (exact, falsifier only)

Files: `2026-11-12-rees-index-p-family/index_p_check.py` and `.out`.

```
cd research/audits/reviews/2026-11-12-rees-index-p-family
nice -n 19 /opt/anaconda3/bin/python index_p_check.py > index_p_check.out   # ~2.5 min
```

Output:
- L_{5,6} at p = 5 and 7: Jacobi holds, class 4, abelian codimension-1 ideals = 0.
- Model L_5: 1 such ideal.
- 5 random G_B of class ≥ 3: abelian hyperplane unique and equal to C_L([L,L]), 0 failures.
- Filiform L_4 at p = 5: all 220 subalgebras satisfy the BCvD Lemma 1 shape (dim drop ≤ 1;
  S ∩ A is an ideal when S ⊄ A), 0 failures.

Acceptance: `failures=0` on both check lines, and `abelian_codim1_ideals=0` for L_{5,6}.
