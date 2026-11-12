PDF extraction note: nonprinting control characters were replaced by spaces; source line references and wording retained.
Primary source https://arxiv.org/pdf/2609.40088v1; manifest {
  "url": "https://arxiv.org/pdf/2609.40088v1",
  "sha256": "6811ae8eaa9727db490653abc2f16c58eb8fa4dda9a8605d4349a163605c620b",
  "status": 200,
  "date": "2026-11-07"
}


Actual pdftotext lines 1008-1067
Definition 3.2 (Pseudo-Lipschitzness). We say that G is pseudo-Lipschitz with constant L ∈ [0, 1] if

                            ( PG )( x ) ≥ (1 − L) G ( x )             for every x ∈ X .           (60)

Lemma 3.3 (Regularity after normalization). Let f satisfy Condition 3.1, and let G be defined by (50).
Assume that the optimum of f is extensive:

                                      Hmax := max f ( x ) = Θ(n).                                 (61)
                                                       x ∈X

Define
                                          L2 ( f )                                  L2 ( f )
                           L2 ( G ) : =            ,          L : = 2L2 ( G ) =              .    (62)
                                           2Rc                                       Rc
Then L2 ( G ) = O(1/n) is an upper bound on the one-step quadratic variation of G, and G is pseudo-
Lipschitz with constant L = O(1/n).

Proof. For the affine normalization in (50), the extensive optimum implies

                                          Rc = Hmax + Ac = Θ(n).                                  (63)

Since
                                                                f ( x ) − f (y)
                                      G ( x ) − G (y) =                         ,                 (64)
                                                                       2Rc
the stated bound on L2 ( G ) follows directly from Condition 3.1 and Rc = Θ(n). For every x ∈ X ,
Cauchy–Schwarz gives
                                                                                           !1/2
                        G ( x ) − ( PG )( x ) ≤        ∑ P(x, y)(G(x) − G(y))2                    (65)
                                                       y

                                              ≤ L2 ( G ).                                         (66)


                                                           20

Since G ( x ) ≥ 1/2, it follows that
                               ( PG )( x ) ≥ G ( x ) − L2 ( G ) ≥ (1 − L) G ( x ).                    (67)
Finally, Condition 3.1 and Rc = Θ(n) give L2 ( G ) = O(1/n) and L = O(1/n).
    Section 7.3 discusses the unknown optimum and normalization parameters. We will show that
the problems we consider satisfies this condition when D is chosen to be Pauli mixer.
Condition 3.4 (Log-Sobolev Inequality). We assume that D ( P) satisfies the following log-Sobolev in-
equality with constant ω > 0: for every unit vector |ψ⟩, if
                                                                  µψ
                                    µψ (z) := |ψ(z)|2 ,     rψ :=    ,                           (68)
                                                                  π
then
                                      ⟨ψ| D |ψ⟩ ≤ 1 − ω Entπ (rψ ),                              (69)
where π is the stationary distribution of P.
   This assumption is used to control the maximum eigenvalue Eb in the denominator. While this
can be seen as an assumption for general walk operators, for the hypercube walk this assumption
holds true with ω = n1 . We make the following assumption on the access model.
Assumption 3.5 (Access model). The algorithm has coherent access to an exact binary-value oracle for
f and to the quantum update oracle of P. More precisely, controlled versions of the following unitaries and
their adjoints are available:
                                  O f | x ⟩|0 p ⟩ = | x ⟩| f ( x )⟩,
                                                           q
                                                                                                       (70)
                                   UP | x ⟩|0⟩ = ∑ P( x, y) | x ⟩|y⟩,
                                                    y∈X


Actual pdftotext lines 1404-1455

Theorem 4.6. Assume that G is pseudo-Lipschitz with constant L ∈ (0, 1], let L2 ( G ) > 0 be an upper
bound on the one-step quadratic variation of G, and assume that Condition 3.4 is satisfied. Let T ⊆ X be
nonempty, and let η, ρ ∈ (0, 1) = Θ(1) satisfy η − ρ − L > 0, 1 − ρ − Eπ [ G ] − L > 0, and Tη ⊆ T.
Suppose there exists a nonempty subset S such that G ( x ) ≥ 1 − ρ for all x ∈ S. Choose

                                                log( G ( x )/(1 − η ))
                                                                        
                                  M := max                               .                          (118)
                                         x ∈S               L

and
                                                                8ω 2 (1−ρ− L)(1−ρ−Eπ [ G ]− L)
                                                      q                                                  
                                                          1+               L2 ( G )2
                                                                                               − 1
                      b = b∗ := min               1,                                                          ,                            (119)
                                                                      1−ρ−L                              

Then,
                                                                                      s
                                                           η−ρ−L
                                                                        
                                                                            1             π (S) κn/2
                         | ⟨S |Cb,M | T ⟩ | ≥                                                    2   .                                     (120)
                                                             η             M+1            π (T )

where
                             2b∗ (1 − ρ − Eπ [ G ] − L)
                                                                               
                                                                     G(x)
                        κ :=                            Ex∼πS log               .                                                          (121)
                                     3nL log 2                      (1 − ρ )
Proof. First, we consider a single point x ∈ S. For any x ∈ S, define

                                               log( G ( x )/(1 − ρ))
                                                                      
                                   m( x ) :=                           .                                                                   (122)
                                                           L
                                                                                                                              p
Since η − ρ − L > 0, every x ∈ S belongs to Tη ⊆ T. When m( x ) = 0, ⟨ T | Db0 | x ⟩ =                                            π ( x )/π ( T ).
For m( x ) ≥ 1, the definition of m( x ) gives
                                                                              − log(1− L)/L
                                                                      1−ρ
                                                                   
                                  m( x )
                 G ( x )(1 − L)            > (1 − L ) G ( x )                                       ≥ 1 − ρ − L.                           (123)
                                                                      G(x)

Therefore, for every 0 ≤ s ≤ m( x ), monotonicity of ḡη implies

                                                                                                   η−ρ−L
                    ḡη ((1 − L)m(x)−s G ( x )) ≥ ḡη ((1 − L)m(x) G ( x )) ≥                                                              (124)

Actual pdftotext lines 3051-3120
Replacing Eb by a known normalization. Let Mmax = poly(n) be a common upper bound on
every power used by the application algorithms, and set

                                                          1
                                          δsv :=                   .                              (342)
                                                   Mmax + 1

Let µG and L2 ( G ) be known upper bounds on Eπ [ G ] and L2 ( G ), respectively, and define

                                                              b2 L2 ( G )2
                                    Ebub := 1 + bµG +                      .                      (343)
                                                                 8ω 2
Theorem 4.5 implies Eb ≤ Ebub . Define the slack normalization

                                         bb := (1 + δsv ) Eub .
                                         E                                                        (344)
                                                           b

The implemented operators are
                                                                        M
                                   D + bG                          1
                                                                 M + 1 m∑
                          (δ )                     (δ )                       (δ )
                        Db sv :=          ,         sv
                                                 Cb,M  :=                  ( Db sv )m             (345)
                                     E
                                     bb                                 =0


                                                   54

               (δ )
and satisfy ∥ Db sv ∥ ≤ (1 + δsv )−1 .
   To compare the implemented amplitude with the analytical bound, define
                                                                       M
                                       D + bG                     1
                            Dbub :=
                                        Ebub
                                              ,       ub
                                                     Cb,M :=          ∑   ( Dub )m .
                                                                M + 1 m =0 b
                                                                                              (346)

The amplitude proof already replaces every denominator Ebm by ( Ebub )m , so it applies directly to
 ub . Moreover,
Cb,M
                                                   M
                                              1
                                                  ∑
                                   (δ )
                                    sv
                                 Cb,M  =               (1 + δsv )−m ( Dbub )m .               (347)
                                            M + 1 m =0
The matrices D + bG and ( Dbub )m are entrywise nonnegative, and the set states have nonnegative
amplitudes. Consequently,
                          D              E               D        E
                                 (δsv )
                            S Cb,M      T ≥ (1 + δsv )− M S Cb,M
                                                             ub
                                                                 T .                       (348)

For every M ≤ Mmax , the choice (342) gives

                      (1 + δsv )− M = exp(− M log(1 + δsv )) ≥ exp(− Mδsv ) ≥ e−1 .           (349)

Thus the slack normalization decreases the marked amplitude by at most a constant factor and
leaves every exponential runtime bound unchanged. More generally, any inverse-polynomial
slack satisfying Mδsv = o (n) incurs only a factor 2−o(n) .
    Finally, substituting (342) into (316) gives
                                                        
                                                     1
