Source: https://arxiv.org/pdf/1904.00702v2
Local: research/audits/sources/sparse_content_multiplicity/koiran_skomra.txt
SHA256 f57fd307710c910cfb90d7f7e5f9280118a0b09776fc0efbc4f18a8cd8934634


Physical lines 24-40:

                                                                            1. Introduction
                                            In this paper we consider the following problem. Let F (x, y) ∈ C[x, y] and
                                          G(x, y) ∈ C[x, y] be two polynomials with complex coefficients such that F
                                          has degree d ⩾ 1 and G has t ⩾ 1 monomials. We want to estimate the
                                          maximal multiplicity of an isolated solution of the system
                                                                         F (x, y) = G(x, y) = 0 .                                (1)
                                          Our main result is the following theorem.
                                          Theorem 1.1. Suppose that p := (a, b) ∈ (C \ {0})2 is an isolated solution
                                          of system (1). Then, the intersection multiplicity of F (x, y) and G(x, y) at
                                          p is at most 52 d2 t2 .
                                             The assumption that a and b are nonzero is crucial, as shown by the
                                          following examples.
                                          Example 1.2. Let F (x, y) := x − y and G(x, y) := x2n − y n . Then, (0, 0) is a
                                          solution of (1) and its multiplicity is equal to n. Similarly, let F (x, y) := x−1
                                          and G(x, y) := y n +x−1. Then, (1, 0) is a solution of (1) and its multiplicity
                                          is equal to n. In Theorem 1.1 the restriction to points p with nonzero

Physical lines 65-101:
only on the number of monomials in F and G. We therefore highlight the
following question.
Question 1. Let F, G ∈ C[x, y] be two polynomials with at most t mono-
mials each. What is the maximal multiplicity of an isolated solution p =
(a, b) ∈ (C \ {0})2 of system (1)? In particular, is the multiplicity of p
polynomially bounded in t, i.e., bounded from above by tc where c is some
absolute constant?
   The first focus of fewnomial theory [Kho91, Sot11] was on the number
of real solutions of multivariate systems. In particular, a seminal result by
Khovanskii [Kho91] shows that a system of n polynomials in n variables
involving l + n + 1 distinct monomials has less than
                                 l+n
                               2( 2 ) (n + 1)l+n                           (2)
non-degenerate positive solutions. This bound was improved by Bihan and
Sottile [BS07] to
                                e2 + 3 ( l ) l
                                       2 2 n.
                                   4
These results can be viewed as far reaching generalizations of Descartes’
rule of signs, which implies that a univariate polynomial with t monomials
has at most t − 1 positive roots. As pointed out in [KPT15a], the analogue
of Question 1 for real roots is very much open: it is not known whether
the number of isolated real solutions of a system F (x, y) = G(x, y) = 0 is
polynomially bounded in the number of monomials of F and G.
   The first result on fewnomials and multiplicities seems to be an analogue
of Descartes’ rule due to Hajós (see [Haj53, Len99] and Lemma 3.9 below):
the multiplicity of any nonzero root of a univariate polynomial f ∈ C[X]
with t monomials is at most t − 1. For multivariate systems, an analogue of
Khovanskii’s bound (2) was obtained by Gabrielov [Gab95]. He showed that
for a system of n polynomials in n variables involving at most t monomials,
the multiplicity of any solution in (C \ {0})n does not exceed
                           2t(t−1)/2 [min(n, t) + 1]t .
                                   2
In particular, this provides a 2O(t ) upper bound for Question 1. Gabrielov’s
result also implies an exponential bound for the problem considered in The-
orem 1.1 instead of our polynomial bound. After [Gab95], subsequent work
has focused on multiplicity estimates for more general (“Noetherian”) mul-

Physical lines 142-192:
we recommend [Bür00]. The authors’ interest for intersection multiplicity
was sparked by the following variation on Conjecture 1.3:
Conjecture 1.4 (τ -conjecture for multiplicities). Consider a nonzero poly-
nomial of the form
                                         k
                                         XYm
                               f (X) =             fij (X),
                                         i=1 j=1
where each fij ∈ C[X] has at most t monomials. The multiplicity of any
nonzero complex root of f is bounded by a polynomial function of kmt.
  2The separation result derived in [Koi11] is actually a little weaker than VP 6= VNP; a
proof that Conjecture 1.3 implies the full separation VP 6= VNP can be found in the PhD
thesis by Sébastien Tavenas [Tav14]. In fact, a bound on the number of real roots that is
polynomial in kt2m would suffice for that purpose [Tav14, Theorems 3.25 and 3.38].
4                  PASCAL KOIRAN AND MATEUSZ SKOMRA


   The idea of looking at multiplicities in this context was introduced by
Hrubeš [Hru13]. Conjecture 1.4 implies a slightly weaker separation than
VP 6= VNP, which can be obtained under a bound on multiplicities that is
only polynomial in kt2m [Tav14, Section 2.2]. Finally we point out that there
is also a “τ -conjecture for Newton polygons,” which implies the separation
VP 6= VNP [KPTT15]. It was recently announced by Hrubeš [Hru19] that
Conjecture 1.3 implies the τ -conjecture for Newton polygons. Moreover, it
follows from [Hru13] that Conjecture 1.3 also implies Conjecture 1.4. The
real τ -conjecture is therefore the strongest of these 3 conjectures (and there
is no known implication between the other two).

1.2. Outline of the proof. In this section we present some of the ideas of
the proof of Theorem 1.1 in an informal way. The actual proof is presented
in Section 5 after some preliminaries in Sections 2 to 4.
   Like in [KPT15a] we rely heavily on the properties of Wronskian deter-
minants. Let us assume first that the relation F (x, y) = 0 can be inverted
locally in a neighborhood of (a, b) as y = φ(x), where φ is an analytic func-
tion. In this case we just have to bound the multiplicity of a as a root of
the univariate function
                                            cα xα1 φ(x)α2 ,
                                      X
                       G(x, φ(x)) =
                                      α∈Λ
where the support Λ of G is of size t. This multiplicity can be bounded with
the help of the Wronskian determinant of the t functions {xα1 φ(x)α2 : α ∈ Λ}
(see Proposition 2.6 and Remark 2.7). The entries of the Wronskian deter-
minant may be of very high degree due to the presence of the exponents
α1 , α2 , over which we have no control. Fortunately, it turns out that high
exponents can be factored out and we can reduce to the case of a deter-
minant with entries of low degree in x and φ(x). We can then conclude by
applying Bézout’s theorem (Theorem 3.8) to F (x, y) = 0 and to a low-degree
determinant.
   The above proof idea is not always applicable since it might not be possible
to invert the relation F (x, y) = 0 as y = φ(x). In particular, we must

Source: https://arxiv.org/pdf/2610.35037v1
Local: research/audits/sources/sparse_content_multiplicity/mousseau.txt
SHA256 49fce498bacd14f6da4b4eeb1d6bc15641630342ba2292de38052ddf1007443c


Physical lines 94-141:
obtaining a bound that is quadratic in N . We consider a system f (x, y) = g(x, y) = 0, where
f, g ∈ C[x, y] are polynomials with complex coefficients such that f is a trinomial and g has
N > 1 monomials. Our main result (Theorem 13) is as follows:
Theorem 13. Let f ∈ C[x, y] be a trinomial and g ∈ C[x, y] be a polynomial with N ≥ 1
monomials. If q ∈ (C∗ )2 is an isolated solution of f = g = 0, then

                                                   (N − 1)(N + 2)
                                  Multq (f, g) ≤                  .                              (5)
                                                         2
   Furthermore, for N = 2 or 3, this bound is sharp.
   Restricting to the algebraic torus (C∗ )2 is strictly necessary, as roots lying on the coordinate
axes can have arbitrarily high multiplicities independently of N . Note also the parallel with the
positive root counts: whereas the best known general bound for positive solutions of a trinomial
and an N -nomial is cubic in N [EHKT20], our upper bound for the intersection multiplicity is
quadratic in N .

                                                   2
    Setting N = 3, Theorem 13 yields a maximal intersection multiplicity of 5 for a system of two
trinomials, matching the sharp bound of Li, Rojas, and Wang for positive solutions. Moreover,
we show that this upper bound of 5 is sharp, as achieved at q = (1, 1) by the system

                              2x9 + y 9 − 3 = x16 + 2xy 6 − 3y = 0.                            (6)

This sharp bound for two trinomials provides a strong affirmative insight into Question 1.1.
    Furthermore, in the 1970s, Anatoli Kouchnirenko conjectured that a system ofQ    n polynomial
equations in n variables with m1 , . . . , mn monomials, respectively, has at most ni=1 (mi − 1)
strictly positive solutions-a conjecture refuted for m1 = m2 = 3 by Haas via the system (4).
The analogous question for intersection multiplicities  in the algebraic torus had remained open
until now. System (6) demonstrates that ni=1 (mi − 1) fails to be a valid upper bound for the
                                             Q
intersection multiplicity as well, while Theorem 13 establishes that for two trinomials, the sharp
bound is indeed 5.




                                                3
Contents
1 Introduction                                                                                         1

2 Some basic concepts                                                                                  4
  2.1 Multiplicity and invariants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        4
  2.2 Puiseux series . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       5
  2.3 Wronskian and toric operator . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           6

3 Case of a trinomial and a sparse polynomial                                                          9

