Source: https://arxiv.org/pdf/quant-ph/0212016
Local text SHA256 e28379bfb5e0e60fb3c54bd67b6020d284f96f4c3138b89cea93ece9a4d9d013

Physical lines 1-200:
                                       Classical and Quantum Polynomial
                                      Reconstruction via Legendre Symbol




arXiv:quant-ph/0212016v1 2 Dec 2002
                                                   Evaluation
                                                        Alexander Russell
                                          Department of Computer Science and Engineering
                                          University of Connecticut, Storrs, CT 06269 USA
                                                         acr@cse.uconn.edu
                                                     Igor E. Shparlinski
                                                   Department of Computing
                                        Macquarie University, Sydney, NSW 2109, Australia
                                                      igor@ics.mq.edu.au

                                                                  July 10, 2018


                                                                     Abstract

                                            We consider the problem of recovering a hidden monic polynomial
                                        f (X) of degree d ≥ 1 over a finite field Fp of p elements given a
                                        black box which, for any x ∈ Fp , evaluates the quadratic character of
                                        f (x). We design a classical algorithm of complexity O(d2 pd+ε ) and
                                        also show that the quantum query complexity of this problem is O(d).
                                        Some of our results extend those of Wim van Dam, Sean Hallgren and
                                        Lawrence Ip obtained in the case of a linear polynomial f (X) = X + s
                                        (with unknown s); some are new even in this case.




                                                                          1
1     Introduction
Let p ≥ 3 be a prime number and let Fp denote a finite field of p elements. We
let χ denote the quadratic character of Fp , or the Legendre symbol modulo
p; see [17].
    Wim van Dam, Sean Hallgren and Lawrence Ip, in the series of papers [4,
5, 6, 14] have considered the shifted Legendre symbol problem of finding an
unknown shift s ∈ Fp given an oracle O which for each x ∈ Fp computes
χ(x + s). They have designed efficient quantum algorithms for the above
problem and its generalisation to characters in residue rings.
    The problem is of intrinsic interest and also has strong cryptographic
motivation; sequences of values of quadratic characters have been considered
as sources of cryptographically strong pseudorandom bits [2, 3, 7, 10, 13, 18,
19, 21, 22].
    Here we consider a generalisation of the above problem to polynomials.
    For an integer d we let Md denote the set of square-free monic polynomials
f (X) ∈ Fp [X] of degree d,
             ∆ 
        Md = f (X) = X d + sd−1 X d−1 + . . . + s1 X + s0 | si ∈ Fp .
We study the problem of finding f ∈ Md , given an oracle Of which returns
χ(f (x)) for any x ∈ Fp :
                            Of : x 7→ χ(f (x)).
It is obvious that the square-freeness condition is essential because polyno-
mials of the form f1 (X) = F (X)G1 (X)2 and f1 (X) = F (X)G2(X)2 with
F (X), G1(X), G2 (X) ∈ Fp [X] cannot be distinguished by this oracle.
    We remark that for the approach of [4, 5, 6, 14] the orthogonality condi-
tion
       X                        
                                  p − 1,     if a = b,
           χ ((x + a)(x + b)) =                              a, b ∈ Fp ,
                                  −1,        if a 6= b,
        x∈Fp

appears to be crucial, however, this condition fails for nonlinear polynomials.
On the other hand, the Weil bound , see [17], provides a certain approximate
analogue of the above identity:
       X                   
                              p + O(d),      if g = h,
           χ (g(x)h(x)) =         1/2                        g, h ∈ Md .   (1)
                              O(p ),         if g 6= h,
       x∈Fp


                                      2
Hereafter the implied constants in symbols ‘O’ may depend on d and also,
where obvious, on the small positive parameter ε.
    Using this property we demonstrate that the quantum query complexity
of recovering f , given the oracle Of , is O(d). In contrast, we observe that
the classical query complexity is Ω(d log p). Furthermore, we give a classical
algorithm for reconstructing f from Of , which appears to be new even in the
case of linear polynomials. In fact this algorithm is also based on the Weil
bound.
    It is clear that the brute force approach leads to a (classical) algorithm
of complexity O(pd+1+ε ) which is based on computation and comparison of
the p-dimensional vectors of the values of χ(f (x)) and χ(g(x)) for all x ∈ Fp
and all g ∈ Md . A naive use of the Weil bound shows that it is enough
to compute and compare χ(f (x)) and χ(g(x)) only for 1 ≤ x ≤ dp1/2 log2 p
which leads to an algorithm of complexity O(pd+1/2+ε ). We show that using
the Weil bound in a less obvious way one can obtain an O(pd+ε ) algorithm.
   It could be relevant to recall the work of Dima Grigoriev [12] where a
somewhat related question is considered for multivariate polynomials (al-
though the field characteristic is assumed to be small).
   It is easy to see that our method applies to multiplicative characters of
other orders and to multivariate polynomials as well.
    Finally, it is also easy to see that we can allow oracles which return the
right value of χ(f (x)) only with some fixed probability γ > 1/2. We do not
pursue this issue in this work, though.

    Acknowledgement.         We thank Asma Harcharras for several useful
discussions.


2    Preparation
First of all we recall the Weil bound in its classical form given in Exam-
ple 12 of Appendix 5 of [24]; see also Theorem 3 of Chapter 6 in [16] and
Theorem 5.41 and comments to Chapter 5 of [17].

Lemma 1. For any F ∈ Md which is not a perfect square of another poly-



                                      3
nomial, the bound
                                        X
                                               χ (F (x)) ≤ dp1/2
                                        x∈Fp

holds.

    The following statement is also implied by the Weil bound and is essen-
tially Theorem 2 of [19].

Lemma 2. For any integers M < p and any F ∈ Md which is not a perfect
square of another polynomial, the bound
                                 M
                                 X                                             
                                        χ(F (x)) = O dp1/2 log p
                                  x=1

holds.

   We also need a similar statement for multivariate polynomials.

Lemma 3. For any collection of ℓ pairwise distinct linear forms

 Lν (S0 , . . . , Sd−1 ) = S0 + S1 c1ν + . . . + Sd−1 cd−1,ν + cd,ν ,                           ν = 1, . . . , ℓ,

over Fp the bound

                                          ℓ
                                                                          !
                      X                   Y
                                    χ           Lν (s0 , . . . , sd−1 )       ≤ 2ℓpd−1/2
                 s0 ,...,sd−1 ∈Fp         ν=1


holds.

Proof. We have

                                      ℓ
                                                                      !
                  X                   Y
                                χ           Lν (s0 , . . . , sd−1 )
             s0 ,...,sd−1 ∈Fp         ν=1

                                                              ℓ
                                                                                                !
                                    X             X           Y
                         ≤                                χ           Lν (s0 , . . . , sd−1 )       .
                                s1 ,...,sd−1 ∈Fp s0 ∈Fp       ν=1



                                                       4
Clearly, there are at most
                              (ℓ − 1)(ℓ − 2) d−2
                                            p    ≤ ℓ2pd−2
                                    2
d − 1-tuples (s1 . . . , sd−1 ) ∈ Fp for which the values of
                 s1 c1ν + . . . + sd−1 cd−1,ν + cd,ν ,              ν = 1, . . . , ℓ,
are pairwise distinct. In this case we estimate the sum over s0 by p. Otherwise
we see from Lemma 1 that the sum over s0 does not exceed ℓp1/2 . Therefore
                            ℓ
                                                      !
               X           Y
                       χ       Lν (s0 , . . . , sd−1 ) ≤ ℓpd−1/2 + ℓ2pd−1 .
           s0 ,...,sd−1 ∈Fp     ν=1

The claimed bound is trivial for ℓ ≥ p1/2 , otherwise we have ℓpd−1/2 ≥ ℓ2pd−1
and the result follows.

   We remark that one can also use stronger bounds based on the famous
results of Pierre Deligne [8, 9], however they do improve our final results.
   Our next statement gives an upper bound “on average” for weighted
character sums with polynomials.
Lemma 4. For any integers N ≤ p, r ≥ 1 and any sequence of real numbers
αx with |αx | ≤ 1, x = 1, . . . , N, the bound
                                            2r
               X X                                                         (2r)! r d
                              αx χ (g(x))        ≤ 4rN 2r pd−1/2 +              N p
              g∈Md x∈Fp
                                                                            r!

holds.

