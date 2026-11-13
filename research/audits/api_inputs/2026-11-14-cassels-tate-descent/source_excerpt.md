# Source: Himanshu Shukla, On computation of the Cassels-Tate pairing, thesis2024
URL https://epub.uni-bayreuth.de/8348/1/thesis.pdf
Raw pdftotext sha256 6d2e33b99e9755673caf826fa0bf331d0799721c056ba5789a874f15ab549199
LF-indexed excerpts below; control characters replaced with spaces, no mathematical edits.


## Original LF lines 4348-4831
4.3.1    Global computation
Since α is a 1-cocycle that takes values in J[2], α always factors through a ﬁnite
extension. Therefore, one can choose a lift a of α such that a also factors through a
ﬁnite extension. Let a be such a lift of α factoring through a ﬁnite extension K/k.
Assume a01 to be as follows:
                                (
                                  0,             if χ01 (σ) = 1,
                      a01 (σ) =
                                  (T1 ) − (T0 ), if χ01 (σ) = −1,
                   √      √                                         √
where χ01 (σ) := σ( √d0 )/ d0 for some d0 ∈ k × , and let K 0 = k( d0 ). Here we have
ﬁxed a square root d0 of d0 . We have ∂a01 (σ, τ ) = 0, if χ01 (σ) = 1 or χ01 (τ ) = 1. Let
F := KK 0 and let χ(σ) denote the restriction σ K of σ ∈ Gk .

Remark 4.3.1. For σ, τ, ρ ∈ Gk , (∂a ∪1 a01 )(σ, τ, ρ) = h∂a(σ, τ ), στ a0 (ρ)i1 , and (a ∪2
∂a0 )(σ, τ, ρ) = ha(σ), σ∂a01 (τ, ρ)i2 , where h·, ·i1 , h·, ·i2 are the bilinear pairings which
induce the cup products. Note that η1 := ∂a ∪1 a01 − a ∪2 ∂a01 is independent of σ K ′
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                 91

as the values of a01 , ∂a01 are deﬁned over k. Therefore, η1 (σ, τ, ρ) depends only on
χ(σ), χ(τ ), χ01 (τ ), and χ01 (ρ) (using Gal(F /k) ⊂ Gal(K/k) × Gal(K 0 /k)), and takes
values in K × ; hence, η1 can be viewed as image of an element in Z3 (F /k) under the
inﬂation map. Therefore, we will interchangeably use η1 (χ(σ), χ(τ ), χ01 (τ ), χ01 (ρ)) and
η1 (σ, τ, ρ). If we choose α to be a normalized 1-cocycle, then we can assume that a is
also a normalized 1-cochain. Hence, ∂a(σ, τ ) = 0, if χ(σ) or χ(τ ) is the identity on
K.

     In what follows, the aim is to show that F is a splitting ﬁeld for [η1 ] and ﬁnd a
2-cochain ε1 such that ∂ε1 = η1 . In order to solve for ε1 , we will ﬁrst extract two
2-cocycles E1 and E1,g representing the trivial class in Br(K 0 ), where {id , g} is a
set of right coset representatives of GK ′ in Gk . Then we use 1-cochains e1 and e1,g
satisfying ∂e1 = E1 and ∂e1,g = E1,g , respectively, to obtain a 3-cocycle η10 that is
cohomologically equivalent to η1 but has many nice properties. At last, we trivialize
η10 using a variant of Hilbert’s Theorem 90 (see Proposition 4.3.8).
     Consider the following 2-cochain

                        E1 (σ, τ ) := η1 σ,τ ∈G ′ ,χ′ (ρ)=−1 ∈ C2 (K 0 ).
                                                   K    1


Note that E1 is the inﬂation of an element in C2 (F /K 0 ). The following proposition
shows that E1 ∈ Z2 (K 0 ).

Proposition 4.3.2. The 2-cochain E1 is a 2-cocycle with values in K × .

Proof. Since η1 is a 3-cocycle

                          ση1 (τ, ρ, θ)η1 (σ, τ ρ, θ)η1 (σ, τ, ρ)
                                                                  = 1.              (4.3.1)
                               η1 (στ, ρ, θ)η1 (σ, τ, ρθ)

Specializing to the case when χ01 (θ) = −1, and σ, τ, ρ ∈ GK ′ , we have η1 (σ, τ, ρ) = 1,
and χ01 (ρθ) = −1. This gives

                                    σE1 (τ, ρ)E1 (σ, τ ρ)
                                                          = 1,
                                    E1 (στ, ρ)E1 (σ, τ )

and therefore, E1 ∈ Z2 (K 0 ).

   The 2-cocycle E1 is constructed from η1 , and if ε01 ∈ C2 (k) is such that η1 = ∂ε01 ,
then for σ, τ ∈ GK ′ and ρ such that χ01 (ρ) = −1,

                                                σε01 (τ, ρ)ε01 (σ, τ ρ)
                                 E1 (σ, τ ) =                           .           (4.3.2)
                                                ε01 (στ, ρ)ε01 (σ, τ )

We now make the following assumption.
 92CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Assumption 4.3.3. Assume that, in the second argument ρ, ε01 (τ, ρ) only depends
on the value of χ01 (ρ) for a ﬁxed τ , and ε01 (τ, ρ) = 1, if χ01 (ρ) = 1. It can be shown
that this indeed is the case for odd-degree hyperelliptic curves. For details, see section
4.3.2 below.
    In view of the above assumption, E1 is trivialized by the 1-cochain

                                      e01 := ε01 τ ∈G ′ ,χ′ (ρ)=−1 .
                                                     K    1


This is because, if σ, τ ∈ GK ′ and χ01 (ρ) = −1, then χ01 (τ ρ) = −1 and χ01 (τ ) = 1, and
using assumption 4.3.3, Equation (4.3.2) becomes
                               σε01 (τ, ρ)ε01 (σ, τ ρ)   σe01 (τ )e01 (σ)
                E1 (σ, τ ) =          0
                                                       =      0
                                                                          = ∂e01 (σ, τ ).
                                     ε1 (στ, ρ)             e1 (στ )
    Hilbert’s Theorem 90 implies the existence of the inﬂation-restriction exact se-
quence for Brauer groups. Hence, one can view E1 as inﬂation of an element of
H2 (F /K 0 ). Therefore, we have an e1 ∈ C1 (K 0 ) such that ∂e1 = E1 , and e1 can be
viewed as inﬂation of a 1-cochain in C1 (F /K 0 ). Note that e1 only depends on σ F .
    Let {id , g} be the right coset representatives of GK ′ in Gk . Denote by {id , ḡ} the
right coset representatives of Gal(F /K 0 ) in Gal(F /k) corresponding to {id , g}. For
σ ∈ GK ′ deﬁne
                                  f1,g (σ) := η1 (σ, g, −1).
Then f1,g ∈ C1 (K 0 ), and it can be viewed as inﬂation of an element in C1 (F /K 0 ).
Deﬁne
                         E1,g (σ, τ ) := η(σ, τ g, −1)/η(σ, g, −1),
for σ, τ ∈ GK ′ . We show that E1,g is a 2-coboundary and therefore is a 2-cocycle.
Proposition 4.3.4. Let ε01 be as in assumption 4.3.3. Then

                                 e01,g (τ ) := ε01 (τ g, −1)/ε01 (g, −1)

satisﬁes ∂e01,g = E1,g .
Proof.
                                σe01,g (τ )e01,g (σ)
                 ∂e01,g (σ, τ ) =
                                    e01,g (στ )
                                σε0 (τ g, −1)ε01 (σg, −1)ε01 (g, −1)
                               = 01
                                σε1 (g, −1)ε01 (g, −1)ε01 (στ g, −1)
                                      σε01 (τ g, −1)     ε01 (σg, −1)ε01 (σ, −1)
                               = 0
                                ε1 (σ, −1)ε01 (στ g, −1)       σε01 (g, −1)
                               = η1 (σ, τ g, −1)/η1 (σ, g, −1) = E1,g (σ, τ ).
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                         93

    Once again (similar to E1 ), one can view E1,g as inﬂation of an element of
Z (F /K 0 ). We can choose e1,g ∈ C1 (K 0 ) such that ∂e1,g = E1,g to be inﬂation of
 2

an element in ∈ C1 (F /K 0 ). Hence, e1,g takes values in F × (more precisely K × ), and
factors through Gal(F /K 0 ). Deﬁne φ1,g ∈ C1 (GK ′ ) by

                                φ1,g (σ) := (f1,g + e1,g + e1 )(σ).

The following proposition shows that φ1,g is a 1-cocycle.

Proposition 4.3.5. The 1-cochain φ1,g is a 1-cocycle, and factors through Gal(F /K 0 ),
and has values in F × .

Proof. Since e1 , e1,g , f1,g are inﬂations of elements in C1 (F /K 0 ), so is φ1,g . Now using
that η1 is a 3-cocycle, for σ, τ ∈ GK ′ ,

                            ση1 (τ, g, g)η1 (σ, τ g, g)η1 (σ, τ, g)
     1 = ∂η1 (σ, τ, g, g) =
                                  η1 (στ, g, g)η1 (σ, τ, g 2 )
                            σf1,g (τ )f1,g (σ)
                          =                    E1,g (σ, τ )E1 (σ, τ )    (deﬁnition of f1,g , E1,g )
                               f1,g (στ )
                          = ∂(f1,g )(σ, τ )∂(e1,g )(σ, τ )∂(e1 )(σ, τ ) = ∂(φ1,g )(σ, τ ).



    By Hilbert’s Theorem 90, there is a t1,g ∈ F × such that ∂t1,g = φ1,g . For σ ∈ GK ′
let σg = gσg −1 ∈ GK ′ . We have gσ = σg g.
    Deﬁne a 2-cochain ε1 as follows:
                           
                           
                                                           χ01 (ρ) = 1,
                           1,             if
                 ε1 (τ, ρ) :=     e1 (τ ),        if   χ01 (τ ) = 1, χ01 (ρ) = −1,           (4.3.3)
                                
                                
                                t e (τ 0 ),      if χ01 (τ ) = −1, χ01 (ρ) = −1,
                                  1,g 1,g


where τ 0 is such that τ = τ 0 g. Deﬁne η10 := η1 − ∂ε1 . Note that for ﬁxed σ, τ ∈ Gk ,
η10 (σ, τ, ρ) depends only on χ01 (ρ). In regards to η10 we have the following proposition.

Proposition 4.3.6. η10 (σ, τ, ρ) = 1 on GK ′ × Gk × Gk ∪ Gk × Gk × GK ′ .

Proof. If σ, τ ∈ Gk and χ01 (ρ) = 1, then

                                    σε1 (τ, 1)ε1 (σ, χ01 (τ ))
                  ∂ε1 (σ, τ, ρ) =                              = 1 = η1 (σ, τ, ρ).
                                    ε1 (στ, 1)ε1 (σ, χ01 (τ ))

If σ, τ ∈ GK ′ and χ01 (ρ) = −1, then

                       σε1 (τ, −1)ε1 (σ, −1)   σe1 (τ )e1 (σ)
     ∂ε1 (σ, τ, ρ) =                         =                = E1 (σ, τ ) = η1 (σ, τ, −1).
                        ε1 (στ, −1)ε1 (σ, 1)     e1 (στ )
 94CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

If σ, τ ∈ GK ′ and χ01 (ρ) = −1, then

                           σε1 (τ g, −1)ε1 (σ, 1)
         ∂ε1 (σ, τ g, ρ) =
                          ε1 (στ g, −1)ε1 (σ, −1)
                             σt1,g σe1,g (τ )                                σe1,g (τ )
                        =                       = f1,g (σ)e1,g (σ)e1 (σ)
                          t1,g e1,g (στ )e1 (σ)                           e1,g (στ )e1 (σ)
                                                                      η1 (σ, τ g, ρ)
                        = η1 (g, σ, −1)E1,g (σ, τ ) = η1 (σ, g, −1)
                                                                      η1 (σ, g, −1)
                        = η1 (σ, τ g, ρ).



    From now on, we assume σ, τ, ρ ∈ Gk satisfy σ, τ ∈ GK ′ and χ01 (ρ) = −1. The
following corollary is a consequence of the above proposition.

Corollary 4.3.7. If σ, τ ∈ GK ′ and ρ ∈ Gk is such that χ01 (ρ) = −1, then

             η10 (σg, τ, ρ) = ση10 (g, τ, ρ) and η10 (σg, τ g, ρ) = ση10 (g, τ g, ρ).

Proof. Let σ, τ , ρ be as above. Using that η10 is a 3-cocycle we have

                              ση10 (g, τ, ρ)η10 (σ, gτ, ρ)η10 (σ, g, τ )
                                                                         = 1,
                                    η10 (σg, τ, ρ)η10 (σ, g, τ ρ)
                                                         ση10 (g, τ, ρ)
                 which by Proposition 4.3.6 gives                        = 1.
                                                         η10 (σg, τ, ρ)

Similarly,

                           ση10 (g, τ g, ρ)η10 (σ, gτ g, ρ)η10 (σ, g, τ g)
                                                                           = 1,
                                  η10 (σg, τ g, ρ)η10 (σ, g, τ gρ)
                                                          ση10 (g, τ g, ρ)
                which by Proposition 4.3.6 gives                           = 1.
                                                          η10 (σg, τ g, ρ)



    The above corollary implies that the values η10 (g, τ, −1) and η10 (g, τ g, −1) deter-
mine η10 completely. Note that the above proof uses only that η10 satisﬁes Proposition
4.3.6 and that it is a 3-cocycle. We will need the following variant of Hilbert’s Theo-
rem 90 in order to trivialize η10 .

Proposition 4.3.8. Recall that the set {id , ḡ} is the set of chosen right coset rep-
resentatives of Gal(F /K 0 ) in Gal(F /k). If x ∈ C1 (F /k) is such that for σ, τ ∈
Gal(F /K 0 ),

  1. x(στ ) = σḡ x(τ )x(σ),
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                                                95

   2. x(στ ḡ)x(σ) = σḡ x(τ ḡ),

   3. ḡ(x(σ))x(ḡσ) = x(ḡ),

   4. ḡ(x(σḡ))x(ḡ)x(ḡσḡ) = 1,
then there is a c ∈ F × satisfying
   1. x(σ) = σḡc(c) ,

   2. x(σḡ) = ḡσ(c)
                  c
                      .
Proof. Let H := Gal(F /K 0 ) and consider the endomorphism φ of F given by
                                 X               X τḡ ḡ
                            φ :=      x(τ )τḡ +              .
                                 τ ∈H            τ ∈H
                                                      x(τ ḡ)

Since x takes values in F × , division by x(τ ḡ) is justiﬁed in the above expression. By
linear independence of automorphisms, there exists a b ∈ F (one of the basis elements
of F over K 0 could be chosen as b; see Remark 4.3.12), such that φ(b) 6= 0. Therefore,
                     X                                X σḡ τḡ ḡ(b)
        σḡ φ(b) =          σḡ x(τ )σḡ τḡ (b) +                                  (by properties 1 and 2 of x)
                     τ ∈H                             τ ∈H
                                                           σḡ x(τ ḡ)
                                                                                       
                       X                        X (στ )ḡ ḡ(b) 
                   1  
                                                                  
                                                                  .
                =           x(στ )(στ )ḡ (b) +                  
                  x(σ) τ ∈H                     τ ∈H
                                                      x(στ  ḡ)   
                         |                  {z                  }
                                                         ϕ(b)


This gives x(σ) = σḡϕ(b)
                     (ϕ(b))
                            . Similarly,
                      X                           X ḡτḡ ḡ(b)
           ḡφ(b) =          ḡx(τ )ḡτḡ (b) +                                     (by properties 3 and 4 of x)
                      τ ∈H                        τ ∈H
                                                       ḡx(τ ḡ)
                                                                                    !
                                 X ḡτḡ (b)          X
                  = x(ḡ)                         +          x(ḡτ ḡ)ḡτḡ ḡ(b)
                                 τ ∈H
                                        x(ḡτ )       τ ∈H
                                                                       (by ḡτḡ ḡ = (τḡ ḡ 2 )ḡ and ḡτḡ = (τḡ )ḡ ḡ)
                                                                                      
                          X                      X                              
                              (τ    )    ḡ(b)                                  
                  = x(ḡ)                             x(τḡ ḡ )(τḡ ḡ )ḡ (b)
                                  ḡ   ḡ                      2        2
                                               +                                .
                          τ ∈H x(τḡ ḡ)         τ ∈H                           
                            |                       {z                         }
                                                             ϕ(b)


This gives x(ḡ) = ḡϕ(b)
                    ϕ(b)
                          . By property 4, for σ ∈ GK ′ ,
                                                                                                            
                         φ(b)(ḡσḡ)ḡ (φ(b))   ḡσḡ ḡ(φ(b))                              σḡ ḡ(φ(b))
              ḡx(σḡ) =                      =                = ḡ                                            .
                            φ(b)ḡφ(b)             ḡφ(b)                                        φ(b)
 96CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

This implies that x(σḡ) = ḡσ(φ(b))/φ(b). Now choose the c in the proposition to be
φ(b).
           0
    Deﬁne f1,g ∈ C1 (k) by
                                          0
                                         f1,g (σ) := η10 (g, σ, −1).
                 0
First note that f1,g can be viewed as inﬂation of an element in C1 (F /k). We have the
                                  0
following proposition regarding f1,g .
                                  0
Proposition 4.3.9. The 1-cochain f1,g satisﬁes the hypothesis of Proposition 4.3.8.

Proof. Assume that ρ ∈ Gk is such that χ01 (ρ) = −1. If σ, τ ∈ GK ′ , then
                                                                         0
               gη10 (σ, τ, ρ)η10 (g, στ, ρ)η10 (g, σ, τ )             f1,g  (στ )
                       0              0
                                                          = 1, so     0        0
                                                                                       = 1.
                      η1 (gσ, τ, ρ)η1 (g, σ, τ ρ)                 σg f1,g (τ )f1,g (σ)

Similarly, the properties η10 (g, σ, τ g) = η10 (g, σ, ρ) and
                            gη10 (σ, τ g, ρ)η10 (g, στ g, ρ)η10 (g, σ, τ g)
                                                                            =1
                                   η10 (gσ, τ g, ρ)η10 (g, σ, τ gρ)
        ′ (στ g)f ′ (σ)
       f1,g       1,g
give          ′ (τ g)
          σg f1,g
                        = 1. Furthermore,

        gη10 (g, τ g, ρ)η10 (g, gτ g, ρ)η10 (g, g, τ g)           0         0       0
                 0    2          0
                                                        = 1, so gf1,g (τ g)f1,g (g)f1,g (gτ g) = 1.
               η1 (g , τ g, ρ)η1 (g, g, τ gρ)
Similarly,
                                                                    0         0
               gη10 (g, τ, ρ)η10 (g, gτ, ρ)η10 (g, g, τ )         gf1,g (τ )f1,g (gτ )
                      0                0
                                                          = 1, so        0
                                                                                       = 1.
                     η1 (g 2 , τ g, ρ)η1 (g, g, τ ρ)                    f1,g (g)



     The above computation implies that there exists a c1,g ∈ F × such that f1,g    0
                                                                                      (σ) =
                      0
c1,g /σg (c1,g ) and f1,g (σg) = gσ(c1,g )/c1,g , for σ ∈ GK ′ . Deﬁne
                                    (
                                      1,           if χ01 (τ ) = 1 or χ01 (ρ) = 1,
                     ε001 (τ, ρ) :=
                                      τ 0 (c1,g ), if      χ01 (τ ) = χ01 (ρ) = −1,

where τ 0 ∈ GK ′ is such that τ = τ 0 g.

Proposition 4.3.10. We have ∂ε001 = η10 .

Proof. One can check that η10 matches ∂ε001 on GK ′ × GK ′ × Gk and Gk × Gk × GK ′ .
In what follows we assume ρ ∈ Gk is such that χ01 (ρ) = −1. For σ, τ ∈ GK ′ we have
                                  σε001 (τ g, −1)ε001 (σ, 1)   στ (c1,g )
           ∂ε001 (σ, τ g, ρ) =    00             00
                                                             =            = 1 = η10 (σ, τ g, ρ).
                                 ε1 (στ g, −1)ε1 (σ, −1)       στ (c1,g )
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                        97

Similarly,
    ∂ε001 (σg, τ, ρ) = σ(∂ε001 (g, τ, ρ))    (∵ ∂ε001 is 3-cocycle satisfying Proposition 4.3.6)
                          00                                             
                          gε1 (τ, −1)ε001 (g, −1)              c1,g            0
                                                                                         
                     =σ        00         00
                                                       =σ                 = σ f1,g (τ )
                           ε1 (gτ, −1)ε1 (g, 1)              τg (c1,g )
                  = σ(η10 (g, τ, ρ)) = η10 (σg, τ, ρ).                        (deﬁnition of c1,g )
Computing ∂ε001 (σg, τ g, ρ) we have
  ∂ε001 (σg, τ g, ρ) = σ(∂ε001 (g, τ g, ρ)) (∵ ∂ε001 is 3-cocycle satisfying Proposition 4.3.6)
                          00                                              
                           gε1 (τ g, −1)ε001 (g, 1)           gτ (c1,g )        0
                     = σ 00                            =σ                  = σf1,g (τ g)
                          ε1 (gτ g, −1)ε001 (g, −1)             c1,g
                                                                               (deﬁnition of c1,g )
                  = σ(η10 (g, τ g, ρ)) = η10 (σg, τ g, ρ).


   As a consequence of the above, we get the following corollary.
Corollary 4.3.11. ∂(ε1 + ε001 ) = η1 .
   Therefore, computationally the global part boils down to trivializing E1 , E1,g and
ﬁnding t1,g , c1,g . One can use following remark in order to ﬁnd t1,g , c1,g :
Remark 4.3.12. Let L be a ﬁnite Galois extension of k, α ∈ C1 (L/k), and {b1 , . . . , bn }
be a set of basis elements of L as a vector space over k. The map
                                          X
                                 Tα :=          α(g)g
                                            g∈Gal(L/k)

                                                            Pn         Pn
is a k-linear map, and if for all i, Tα (bi ) = 0, then Tα ( ai bi ) =     ai Tα (bi ) = 0.
                         P                                  i=1        i=1
Hence, at least one of          α(g)g(bi ) 6= 0.
                          g∈Gal(L/k)

    Finding e1 such that ∂e1 = E1 and e1,g such that ∂e1,g = E1,g are the bottleneck
steps of this algorithm in terms of time complexity. There are algorithms which can
be used for this purpose for example [Fie09] for local ﬁelds and [Pre13] in general, if
an eﬀective version of Hilbert’s Theorem 90 exists.

4.3.2   Removing Assumption 4.3.3
We now will show that Assumption 4.3.3 is always satisﬁed for odd-degree hyperel-
liptic curves. We have the following commutative diagram of Gk -modules
                                                         [2]
                      0          J[2]          J[4]            J[2]      0
                                                                                           (4.3.4)
                                                         [2]
                      0          J[2]           J               J        0.
 98CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Taking Galois cohomology we have

                                   [2]∗
    ···         H1 (Gk , J[4])            H1 (Gk , J[2])         δ
                                                                         H2 (Gk , J[2])             ···

                                   [2]∗
    ···             H1 (Gk , J)               H1 (Gk , J)        δ
                                                                         H2 (Gk , J[2])             ···
                                                                                loc2 (J[2])
                Q                  [2]∗   Q                          Q
    ···             H1 (Gkv , J)              H1 (Gkv , J)       δ
                                                                          H2 (Gkv , J[2])           ···
                v                         v                          v
                                                                                   (4.3.5)
    If X (J[2]) = 0, then loc (J[2]) is injective, and for an element a ∈ S (J/k) we
          2                        2                                                          (2)

have δ(a) = 0. Hence, there is a b ∈ H1 (Gk , J[4]) such that [2]∗ (b) = a. In particular,
using the construction of the map δ, given a 1-cocycle α representing a, one can
choose a 1-cocycle β ∈ Z1 (Gk , J[4]), such that [2]∗ β = α. The following proposition
shows that loc2 (J[2]) is injective. The case when all the 2-torsion points are deﬁned
over k is present in [Yan21b, Lemma 1.8.6].

Proposition 4.3.13. Let C, J, f and ∆ be as before. Then the map
                                                Y
                 loc2 (J[2]) : H2 (Gk , J[2]) →   H2 (Gkv , J[2]),
                                                             v

is injective.

Proof. By Proposition 4.1.1, J[2] ⊕ µ2 ≃ µ∆ 2 as Gk -modules, where ∆ is the Gk -set
of roots of f . Therefore, X (J[2]) = 0 ⇐⇒ X2 (µ∆
                              2                                    2
                                                     2 ) = 0 (∵ X (µ2 ) = 0). Note
           ∨      ∨ ∆
that (µ∆2 ) = (µ2 ) ≃ µ2 as Gk modules. Finiteness of µ2 implies that X (µ2 ) is
                          ∆                                ∆                i ∆

ﬁnite for all i. By Poitou-Tate duality (Theorem 1.3.43), there is a non-degenerate
and perfect pairing
                                     2 ) × X (µ2 ) → Q/Z,
                           pt : X1 (µ∆       2 ∆


                                   ∆ 0                                     ∆ 0
                         2 ) ≃ X (µ2 ) . We have X (µ2 ) = 0 ⇐⇒ X (µ2 ) =
                                                   1  ∆                 2
which implies that X1 (µ∆        2

0 ⇐⇒ X2 (µ∆                                    1  ∆                     2
             2 ) = 0. By [BPS16, Lemma 8.2], X (µ2 ) = 0. Therefore, loc (J[2]) is
injective.

    One can also prove the above proposition using Proposition 1.3.25 and Corollary
1.3.29 and the Albert-Brauer-Hasse-Noether sequence, but the above proof is neat and
possibly easy to generalize to other cases. The following corollary removes Assumption
4.3.3:

Corollary 4.3.14. There exists an ε01 ∈ C2 (k) such that ∂ε01 = η1 and such that for
a ﬁxed σ, ε01 (σ, τ ) depends only on χ01 (τ ), and ε01 (σ, τ ) = 1, if χ01 (τ ) = 1. Concretely,
one such ε01 is given by s ∪ 2a01 + f ∪ a01 , where s, f are as in Proposition 2.5.1.
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                       99

Proof. By Proposition 4.3.13, one can choose the lift β of α to C1 (Gk , J[4]) to be in
Z1 (Gk , J[4]). Hence, εw can be chosen to be the trivial 2-cochain (constant map to
1). By Proposition 2.5.1, ε01 = s ∪ 2a01 + f ∪ a01 which clearly satisﬁes ε01 (σ, τ ) = 1, if
χ01 (τ ) = 1, and for a ﬁxed σ, ε01 (σ, τ ) only depends on χ01 (τ ).


## Original LF lines 4832-5257
4.3.3   Local computation
Let v be a place of k. Following the proof of Theorem 4.2.1, we can restrict the base
ﬁeld to the ﬁeld over which one of the representative points of a local orbit of ∆ is
deﬁned. Therefore, without loss of generality, we assume that θ1 ∈ kv . Let w be the
place of F above v under the ﬁxed embedding k ,→ kv . Let Fw be the completion of
F with respect to w, and kv , Kw and Kw0 be the completions of the images of k, K,
and K 0 inside Fw , respectively. Let Pv ∈ J(kv ) and bv be as in the deﬁnition of the
CTP. We want to ﬁnd the class associated to γ1,v in Br(kv ).

                        γ1,v := (av − ∂bv ) ∪ a01,v − bv ∪ ∂a01,v − ε1,v .

     In order to avoid dealing with the cases Kw0 ⊂ Kw and Kw0 6⊂ Kw separately, we
abuse notation slightly and let χ(σ) denote the restriction of σ ∈ Gkv to Fw (instead
                                p 0   p 0                                   √ 0
of σ Kw ) and χ01 (τ ) := τ       d1,w / d1,w , where d01,w is the image of d1 in Kw0 .
     Note that γ1,v takes values in Kw× and factors through Gal(Fw /kv ). For a ﬁxed
σ ∈ Gkv , γ1,v (σ, τ ) depends only on χ01 (τ ); hence, we once again interchangeably use
γ1,v (χ(σ), χ01 (τ )) and γ1,v (σ, τ ). The following proposition implies that γ1,v encodes a
                            ×
1-cocycle in Z1 (GKw′ , kv ).

Proposition 4.3.15. One can view γ1,v as image of an element of Z2 (Fw /kv ) under
inﬂation. Deﬁne Γ1,v (h) := γ1,v (h, −1), for h ∈ GKw′ . Γ1,v deﬁned above is a 1-cocycle
in Z1 (Kw0 ), and can be viewed as inﬂation of an element in Z1 (Fw /Kw0 ).

Proof. Since γ1,v is a 2-cocycle,

                   g1 γ1,v (g2 , g3 )γ1,v (g1 , g2 g3 ) = γ1,v (g1 g2 , g3 )γ1,v (g1 , g2 ).

Assuming that g1 , g2 ∈ GKw′ , and g3 ∈
                                      / GKw′ , we have

        g1 γ1,v (χ(g2 ), −1)γ1,v (χ(g1 ), −1) = γ1,v (χ(g1 g2 ), −1), so ∂Γ1,v (σ, τ ) = 1.



     Hilbert’s Theorem 90 implies the existence of a ω1,v ∈ L× such that Γ1,v (h) =
h(ω1,v )/ω1,v . In fact, by Proposition 4.3.12, one can explicitly compute ω1,v , given
γ1,v . Choose representatives {id , g} of left cosets of GKw′ in Gkv . For h ∈ GKw′ and
g0 ∈
   / GKw′ , the equation

                        gγ1,v (h, g 0 )γ1,v (g, hg 0 ) = γ1,v (gh, g 0 )γ1,v (g, h)
 100CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

combined with χ0 (h) = 1 gives

                              γ1,v (gh, −1) = gγ1,v (h, −1)γ1,v (g, −1)
                                              ghω1,v
                                            =         γ1,v (g, −1).                                        (4.3.6)
                                               gω1,v

    By Proposition 4.3.12, one can assume that the ω1,v , which trivializes Γ1,v , is
in Kw ⊆ Fw , because γ1,v (and therefore, Γ1,v ) takes values in Kw× . Therefore, the
action of GKw′ on ω1,v can be described in terms of σ Kw× (this is true whether or not
Kw ∩ Kw0 = kv ). Now consider the 1-cochain ξ1,v ∈ C1 (Gkv , Fw× ) given by
                                                (
                                                    1,        if    χ01 (τ ) = 1,
                                ξ1,v (τ ) :=
                                                    ω1,v ,    if χ01 (τ ) = −1.

We have
                            
                            
                                                                                        χ01 (ρ) = 1,
                            1,                                    if
         ∂ξ1,v (τ, ρ) :=      τ ω1,v /ω1,v = Γ1,v (τ ),            if   χ01 (τ ) = 1, χ01 (ρ) = −1,
                            
                            
                            τ ω · ω ,                             if χ01 (τ ) = −1, χ01 (ρ) = −1.
                                  1,v     1,v

     0                                                               0
Let γ1,v := γ1,v − ∂ξ1,v . Then for τ ∈ GKw′ , ρ ∈ Gkv we have γ1,v     (τ, ρ) = 1, and if
τ∈/ GKw′ , then τ = gτ 0 , for some τ 0 ∈ GKw′ . Using Equation (4.3.6)

              0                γ1,v (gτ 0 , ρ)   gτ 0 ω1,v γ1,v (g, −1)    γ1,v (g, −1)
             γ1,v (τ, ρ) =                     =                         =              .
                              gτ 0 (ω1,v )ω1,v    gω1,v gτ 0 (ω1,v )ω1,v   g(ω1,v )ω1,v
           0
Note that γ1,v (τ, ρ) is independent of χ(τ ) and depends only on χ01 (τ ) and χ01 (ρ), and

                                                         γ1,v (g, −1)
                                            δ1,v :=                                                        (4.3.7)
                                                         g(ω1,v )ω1,v
depends only on the choice of coset representative g and ω1,v . Hence, by the condition
      0
that γ1,v is a 2-cocycle we have δ1,v ∈ kv× . To see this, let g1 , g2 , g3 ∈
                                                                            / GKw′ . Then

              0               0                    0                 0
         g1 (γ1,v (g2 , g3 ))γ1,v (g1 , g2 g3 ) = γ1,v (g1 g2 , g3 )γ1,v (g1 , g2 ), so g1 δ1,v = δ1,v .

On the other hand, assuming g1 ∈ GKw′ and g2 , g3 ∈
                                                  / GKw′ gives

              0               0                    0                 0
         g1 (γ1,v (g2 , g3 ))γ1,v (g1 , g2 g3 ) = γ1,v (g1 g2 , g3 )γ1,v (g1 , g2 ), so g1 δ1,v = δ1,v ,

therefore, δ1,v ∈ kv× . Now the class c1,v represented by γ1,v
                                                           0
                                                               (therefore, by γ1,v ) in Br(kv )
is the class of quaternion algebra (δ1,v , d1 ). We have (−1)2invv (c1,v ) = (δ1,v , d01 )v , where
                                             0

(·, ·)v denotes the Hilbert symbol over kv .
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                               101

4.3.4    An explicit η1
We assume θ1 ∈ k. We continue to use the notation from the previous section except
for χ. We ﬁx an order of the roots θ1 , . . . , θl of f , and correspondingly of T1 , . . . , Tl
in ∆. A lot of this section is a natural generalization of the deﬁnitions made in §3.1
and §3.2.1.
    If a ∈ S(2) (J/k), then a maps to an element of H1 (Gk , µ∆      2 ) via w∗ (deﬁned in
section 4.1). Therefore, we choose the cocycle α representing w∗ (a) as follows. Using
                                        ×      × 2
the identiﬁcation H1 (Gk , µ∆  2 ) ≃ A /(A ) , where recall that A is the étale algebra
associated to the deﬁning polynomial f , we choose a 1-cocycle χa ∈ Z1 (Gk , µ∆             2 ),
              P√
              l                P√
                                l
χa (σ) := σ(       di (Ti ))/(      di (Ti )) and di ∈ k(θi )× are as in Proposition 1.5.2
              i=1                   i=1
                                   Q
                                   l
with the property that                   di ∈ (k × )2 . Since π∗ ◦ w∗ is the identity morphism on
                                   i=1
cohomology classes, we will represent a by π∗ (χa ). As in §3.1, for each element
m of µ∆                                          l
             2 , we associate an element in µ2 with ith entry being m(Ti ). Under this
association, the values of χa will map to the l-tuples having exactly an odd number
of 1’s. Denote the tuple with 1 at i1 , . . . , it and −1 at other places by i1\     , . . . , it ,
              b
and by 0 the tuple with 1 everywhere. There is a natural action of Gk on these
l-tuples, coming from the action on ∆. Under π the element of µ∆           2 represented by
                           Pt
i1\
  , . . . , it will map to    [(Tin ) − (T0 )]. However, from the proof of Proposition 4.1.1,
                           n=1
                              \
the element represented by i1 , . . . , it is in the image of the point P ∈ J[2] represented
                 P                                                          P
                                                                            t
by the divisor         ((Tin ) − (T0 )) which is the same as the point        [(Tin ) − (T0 )].
                 ∈{i1 ,...,it }
                n/                                                                               n=1
Therefore, we can choose α ∈ Z (Gk , J[2]) representing a to be
                                              1


                                    X
                                    t
                      α(σ) =               [(Tin ) − (T0 )],                   \
                                                                 if χa (σ) = i1 , . . . , it ,
                                    n=1

and the lift a of α as
                                  X
                                  t
                    a(σ) =              ((Tin ) − (T0 )),                    , . . . , it 6= b
                                                               if χa (σ) = i1\               0.
                                  n=1

We deﬁne a(σ) = 0, for χa (σ) = b  0. Recall the deﬁnition of a01 from §4.3.1. We note
                                         √         √
that a factors through the ﬁeld K = k( d1 , . . . , dl ) with Gal(K/k) ⊂ C2l−1 o Sl−1 ,
where Sl−1 is the symmetric group acting on the set {T2 . . . Tl }, and
                                                                     p C2 is thepcyclic
group of order 2. Here for 1 ≤ i ≤ l − 1, the ith copy of C2 acts by di+1 7→ − di+1 .
Since we are going to compute symbolically, we assume that Gal(K/k) ≃ C2l−1 o Sl−1 .
If σ ∈ Gal(K/k), then σ = σs σp , where σp ∈ Sl−1 and σs ∈ C2l−1 ; hence, χa (σp ) = b
                                                                                     0.
Since χa is a 1-cocycle, χa (σs ) = χa (σ). For simplicity of notation we set χ = χa .
The subscripts s and p denote the sign part and the permutation part of an element
 102CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

σ ∈ Gal(K/k) considered as an element in C2l−1 o Sl−1 . Recall the action of Gk on µl2 -
tuples. For σ, τ ∈ Gal(F /k), σ · χ(τ ) = σp · χ(τ ), and σa(τ ) = σp a(τ ) = a(σ · χ(τ )) =
a(σp · χ(τ )). We have

                  ∂a(σ, τ ) = σa(τ ) + a(σ) − a(στ )
                                = σa(χ(τ )) + a(χ(σ)) − a(χ(σ)σp · χ(τ ))
                                = a(σp · χ(τ )) + a(χ(σ)) − a(χ(σ)σp · χ(τ )).

Clearly ∂a(σ, τ ) depends only on χ(σ) and σp · χ(τ ). Let {χ(σ)} be the set associ-
ated to the tuple χ(σ) and with b    0 associate the set {1, . . . , l}. Then {χ(σ)χ(τ )} =
({χ(σ)} ∩ {χ(τ )}) ∪ ({χ(σ)} ∪ {χ(τ )})c , where ∗c is the complement of a subset ∗ of
                                         P
{1, . . . , l}. Noting that a(χ(σ)) =        ((Ti ) − (T0 )) when χ(σ) 6= b  0, we treat the
                                             i∈{χ(σ)}
cases of χ(σ) = b 0 or χ(τ ) = b
                               0 or χ(σ) = σp · χ(τ ) separately. If χ(σ) or χ(τ ) is b0,
                                                                   Q
then ∂a(σ, τ ) = 0 and if χ(σ) = σp · χ(τ ), then ∂a(σ, τ ) = div(    (x − θi )). In case
                                                                                 i∈{χ(σ)}
                               b 6= σp χ(τ ),
χ(σ) 6= σp · χ(τ ) and χ(σ) 6= 0
                                                                                                       
                        X
                        l                           X                                                   
                                                                                           Q
                                                                                              y          
∂a(χ(σ), σp ·χ(τ )) =          ((Ti )−(T0 ))−2                 ((Ti )−(T0 )) = div                      .
                                                                                              (x − θi ) 
                         i=1                       ∈{χ(σ)}
                                                  i/
                                                                                           ∈{χ(σ)}
                                                                                          i/
                                                  ∈{σ·χ(τ )}
                                                 i/
                                                                                          ∈{σ·χ(τ )}
                                                                                         i/


Summarizing the above, we obtain
                     
                     
                      div(1),                                   if    χ(σ) = b
                                                                              0 or χ(τ ) = b
                                                                                           0,
                     
                                              !
                     
                              Q
                     
                      div           (x − θi ) ,                           χ(σ) = σ · χ(τ ) 6= b
                     
                                                                if                            0,
                     
                           i∈{χ(σ)}
         ∂a(σ, τ ) =                          
                     
                     
                     
                                             
                     
                      div  Q y               ,                if b
                                                                    0 6= χ(σ) 6= σ · χ(τ ) 6= b
                     
                                     (x−θi ) 
                                                                                              0.
                     
                     
                     
                     
                               ∈{χ(σ)}
                              i/
                                    ∈{σ·χ(τ )}
                                   i/



Similar to the elliptic curve case,
                      
                      0 = div(1),                                    if χ01 (τ ) = 1 or χ01 (ρ) = 1,
      ∂a01 (τ, ρ) =
                      2(T1 ) − 2(T0 ) = div(x − θi ),                if     χ01 (ρ) = χ01 (τ ) = −1.


     Choose the uniformizers tP at a non-Weierstrass point P on C as x−x(P ), as (x−
θi )/y at a Weierstrass point Ti with i 6= 0, and xg /y at T0 . Then, (∂a∪1 a01 )(σ, τ, ρ) = 1
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                                103

if χ0 (ρ) = 1. If χ0 (ρ) = −1, then
                        
                        
                         1,                                if                            b or χ(τ ) = b
                                                                                   χ(σ) = 0            0,
                        
                            Q
                        
                                                                          χ(σ) = σ · χ(τ ), 1 ∈
                                                                                               / {χ(σ)},
                        
                                  s1i ,                    if
                        
                        
                        
                        
                          i∈{χ(σ)}
                        
                              Q
                        
                                                                          χ(σ) = σ · χ(τ ), 1 ∈ {χ(σ)},
                        
                        
                          s1          s1i ,                 if
                        
                              i6=1
                        
                         i∈{χ(σ)}
 ∂a ∪ a01 (σ, τ, ρ) =
                        
                                 Q1        ,               if χ(σ) 6= σ · χ(τ ), 1 ∈
                                                                                    / {χ(σ)} ∪ {σ · χ(τ )},
                        
                                       s1i
                        
                            i/∈{χ(σ)}
                        
                          ∈{σ·χ(τ )}
                        
                        
                          i/
                        
                        
                                 i6=1
                        
                        
                        
                                 Qs1                       if χ(σ) 6= σ · χ(τ ), 1 ∈ {χ(σ)} ∪ {σ · χ(τ )},
                        
                                           ,
                        
                        
                                        s1i
                            i ∈{χ(σ)}
                               /
                         i /∈{σ·χ(τ )}

                                           Q
where sij := θi − θj , and si :=                  sij . In the above expression for ∂a ∪1 a0 (σ, τ, ρ), we
                                           j6=i
                                   b except for the ﬁrst case. Similarly,
assume that χ(σ) and χ(τ ) are not 0
                       
                       
                        1,                            if               b or χ01 (τ ) = 1 or χ01 (ρ) = 1,
                                                                 χ(σ) = 0
                       
                            Q
                       
                                                           / {χ(σ)}, χ(σ) 6= b
                                                       if 1 ∈                 0, χ01 (τ ) = χ01 (ρ) = −1,
                       
                       i /∈{χ(σ)} si1 ,
a ∪ ∂a01 (σ, τ, ρ) =
                       
                              Q
                       
                        s1          si1 ,             if 1 ∈ {χ(σ)}, χ(σ) 6= b
                                                                              0, χ01 (τ ) = χ01 (ρ) = −1.
                       
                       
                       
                       
                            i∈{χ(σ)}
                              i6=1



    We have the following useful lemma for ﬁnding a 1-cochain that trivializes a 2-
cocycle representing the trivial class in the Brauer group of a number ﬁeld, given that
it factors through a nice extension.

Lemma 4.3.16. Let L/k be a ﬁnite extension of ﬁelds with G := Gal(L/k). Let
H, N be subgroups of G with N normal in G. Assume that G ≃ N o H, and write
g = nh for each element g ∈ G with n ∈ N and h ∈ H. Let E ∈ Z2 (L) represent
                                                                        0          0
the trivial class in Br(L/k) with the property that resH
                                                       G (E) = 0, E(g, g ) = E(n, nh ),
where n0h = hn0 h−1 , and E restricted to G × H ∪ H × G is trivial. Then there is
e ∈ C1 (L) such that

   1. e(g) = e(n), for g = nh ∈ G,

   2. he(n0 ) = e(n0h ) for each n0 ∈ N and h ∈ H,

and ∂e = E.
 104CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Proof. If there is an e ∈ C1 (N, L× ) satisfying only the second property above, and
                                                                               ×
∂e = resN                                                                1
        G (E), then we extend e to deﬁne a 1-cochain (also called e) in C (G, L ) by
e(nh) = e(n). Now

                        nhe(n0 )e(n)   ne(n0h )e0 (n)
    ∂e(nh, n0 h0 ) =            0
                                     =    0     0
                                                      = ∂e(n, n0h ) = E(n, n0h ) = E(g, g 0 ).
                          e(nnh )        e (nnh )

Therefore, the rest of the proof is trying to prove the existence of such an e.
    Let e : G → L× be a 1-cochain such that ∂e = E. Then E(h, n0 ) = 1 is
equivalent to e(hn0 ) = he(n)e(h), and E(h, h0 ) = 1 is equivalent to saying that
e(hh0 ) = he(h0 )e(h0 ). Then resH G (e) is a 1-cocycle. Hence, by Hilbert’s Theorem
                    ×
90, there is a b ∈ L such that e(h) = h(b)/b.
    Using E(nh, n0 ) = E(n, n0h ),
                                   
                        he(n0 )           e(nhn0 )e(n)      e(nhn0 )      nnh0 e(h)
                n                     =                 =               =           .
                        e(n0h )           e(nn0h )e(nh)   e(nn0h )ne(h)    ne(h)

This implies that
                                                                              
              he(n0 )   n0h e(h)   hn0 (b)b                        e(n0 )          e(n0h )
                      =          = 0         =⇒ h                                = 0       .
              e(n0h )    e(h)     nh (b)h(b)                      n0 (b)/b        nh (b)/b

Now e0 (n) := e(n)b/n(b) is an element of C1 (N, L× ) such that ∂e0 = resN
                                                                         G (E) and
 0
e satisﬁes the second property in the statement of the proposition. Hence, by the
ﬁrst part of the proof, e0 can be extended to give a 1-cochain e00 ∈ C1 (L× ) such
that ∂e00 = E. We can choose our e in the proposition to be e00 which proves the
proposition.

Remark 4.3.17. In the general setup E1 and E1,g deﬁned in §4.3.1 satisfy the above
property as Gal(F /K 0 ) ≃ C2l−1 o Sl−1 . Hence, one can reduce the case of computing
e1 and e1,g such that ∂e1 = E1 and ∂e1,g = E1,g , to only computing e1 and e1,g
                   G
such that ∂e∗ = resGkk(J[2]) E∗ . This can be done by symbolically deﬁning the algebras
corresponding to the general symbolically deﬁned cocycles E1 and E1,g and then
specializing them.

   Recall the conjugation homomorphism on n-cochains from §1.3.3. The following
remark is regarding σ∗ on the 2-cochain ∂a ∪ a01 (∗, ∗, −1).

Remark 4.3.18. Let E := ∂a∪a01 (∗, ∗, −1) and σ ∈ Gal(F /k) be such that χ(σ) = b          0.
                                                                    0
Then E is invariant under σ∗ . This is because σ∗ (E) = σ∗ (∂a ∪ a1 ) ∪ σ∗ ((T1 ) − (T0 )) =
∂σ∗ (a)∪((T1 )−(T0 )). Now, σ∗ (a)(τ ) = σa(σ −1 τ σ) = σa(σ −1 ·χ(τ )) = a(χ(τ )) = a(τ ).
 4.3. THE CTP ON S(2) (J/k) × H1 (Gk , h[(T1 ) − (T0 )]i)                                      105


## Original LF lines 5331-5420
4.3.6   Algorithm

The following is pseudocode that states the key steps of an algorithm to compute the
CTP, based on the above computations. Here we have identiﬁed S(2) (J/k), where J is
the Jacobian of an odd-degree hyperelliptic curve C : y 2 = f (x), with a subgroup of
A× /(A× )2 , where A is the étale algebra A = k[x]/hf i. The input elements d, d0 ∈ A×
represent the 2-Selmer elements a, a0 , respectively.

Algorithm 1 Compute the CTP between a, a0 ∈ S(2) (J/k) represented by d, d0 ∈
A× .
Require: d, d0 ∈ A× .
                           ′
Ensure: Value of (−1)ha,a iCT in variable CT.
 1: CT ← 1                                                             . Value of CT.
 2: LocalPoints ← [ ].                            . List storing Pv indexed by Sa,a′ .
 3: for v ∈ Sa,a′ do
 4:    Find Qv ∈√J(kv ) such that δ(Qv ) = αv .    . α ∈ C1 (Gk , J[2]) is as in §4.3.4.
 5:    Kv ← kv ( dv ) and Pv ← 2 Qv ∈ J(Kv ). . Computed using Stoll’s algorithm.
                                   1

 6:    for T ∈ J[2] and T ∈  / J(kv )[2] do                               . Adjust Pv .
 7:        if ∂(Pv + T ) = αv then
 8:            Pv ← Pv + T, and exit the inner loop.
 9:        end if
10:    end for
11:    LocalPoints[v] ← Pv .
12: end for
 4.4. A CONDITIONAL BUT SIMPLER ALGORITHM                                                107

             √                     √                       √       √
13: K ← k(      d). . Adjoining d means adjoining d1 , . . . , dl , where (d1 , . . . , dl )
    is as in §4.3.4.
14: for θ ∈ {Factors of f } do
15:     kθ ← k[x]/hθi and θ1 ← a p   root of θ.
16:     d01 ← d0 (θ1 ) and K 0 ← kθ ( d01 ).
17:     Compute 2-cocycles E1 , E1,g ∈ Z2 (KK 0 /K 0 ), using §4.3.4.
18:     Solve for e1 , e1,g ∈ C1 (KK 0 /K 0 ) such that ∂e1 = E1 and ∂e1,g = E1,g . . One
    can use generic algorithms available in Magma to obtain e1 and e1,g . Lemma
    4.3.16 can be used to obtain e1 and e1,g with nicer properties.
19:     Compute 1-cocycle φ1,g and solve for a Hilbert’s Theorem 90 element t1,g .
                                 0
20:     Compute 1-cochain f1,g     and solve for c1,g , using Remark 4.3.12.
21:     for v ∈ Sa,a′ do
22:          for w ∈ {Places of k(θ) above v} do
23:             θ1,w ← Image of θ1 under the embedding kθ ,→ (kθ )w and d01,w ←
      0
    d (θ1,w ).
24:             Compute ε1,w and γ1,w .                            . By Equation (4.2.1).
25:             Compute Γ1,w , ω1,w , and δ1,w . . By Proposition 4.3.15 and Equation
    (4.3.7).
26:             CT ← CT · (δ1,w , d1,w )(kθ )w )
27:          end for
28:     end for
29: end for
30: return CT.



                   4.4    A conditional but simpler algorithm

In this section we give a simpler algorithm to compute the CTP for odd-degree hy-
perelliptic curves, conditioned on the existence of global solutions to certain ternary
quadratic forms. Since checking if a ternary quadratic form has a global solution is
equivalent to computing a ﬁnite number of local Hilbert symbols, it is not an expen-
sive check. The simplicity of the algorithm lies in reducing the time complexity for
the global step and being able to explicitly write down ε1 such that ∂ε1 = η1 (as
deﬁned in the previous section) using the solutions to these quadratic forms. The
motivation for doing so clearly comes from the case of elliptic curves in the previ-
ous chapter. However, unlike the case of elliptic curves, where the twisted curve is
given by the vanishing of a pencil of ternary quadratic forms (§3.1.1), the equations
describing a twist (corresponding to a 2-Selmer element) of the Jacobian of a genus
g ≥ 2 hyperelliptic curve are not necessarily ternary quadratic forms. Before moving
ahead, we prove the following important lemma.

Lemma 4.4.1. Let L/k be a ﬁnite extension with G := Gal(L/k) ≃ C2n with gen-
erators g1 , · · · , gn . Let E ∈ Z2 (L/k) be a 2-cocycle representing the trivial class in
 108CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Br(L/k) such that E takes values in k × and E(g, h) = E(h, g) for all g, h ∈ G. Let
bi ∈ L× be such that E(gi , gi ) = gi (bi )bi and gj (bi ) = −bi for j 6= i. Then the 1-cochain
e : G → L× given by
                                                                       Q
                                                                       t
                                                                            bi m
                                                  t(t−1)
                                                                      m=1
                      e(gi1 · · · git ) := (−1)      2                                       ,
                                                           Q
                                                           t−1
                                                                 E(gim , gim+1 · · · git )

## Original LF lines 5494-5775

   We begin with the assumption that K ∩K 0 = k and Gal(F /k) ≃ (C2l−1 oSl−1 )×C2 ,
and compute symbolically and explicitly. The general case will just be restriction of
the generic output of the following computations to a subgroup of (C2l−1 o Sl−1 ) × C2 .
Further, for σ ∈ Gal(F /K 0 ) we have σ = σs σp with σs ∈ Cl−1  2    and σp ∈ Sl−1 ,
                                                      0
considering Sl−1 and C2 as subgroups of Gal(F /K ) ≃ C2 o Sl−1 . In this case
                        l−1                                 l−1

note that χ(σ) = χ(σs ) and χ(σ) = b 0 if σ ∈ Sl−1 .
   Deﬁne the aﬃne plane curve

                                   C1j : dj u2j − d1 vj2 + θj − θ1 = 0,

where uj and vj are coordinates, for 2 ≤ j ≤ l. Note that ∆ \ {T1 } forms a Gk -set.
Fix representatives of orbits of ∆ \ {T1 }. If C1j has a k(θj )-rational point (uj , vj ),
and Tk 6= Tj is in the orbit of Tj , then for all σ ∈ Gk such that σ(Tj ) = Tk the point
(σ(u2 ), σ(v2 )) is a point satisfying the conic C1k (note that (σ(uj ), σ(vj )) ∈ k(θk ) is
the same point for all σ ∈ Gk such that σ(Tj ) = Tk ). Hence, for each Tk in the orbit
of Tj , let (uk , vk ) := (σ(uj ), σ(vj )) for some σ ∈ Gk with σ(T2 ) = Tk . In this way we
deﬁne uj , vj ∈ k(θj ) for all j 6= 1 (assuming that each C1j has a solution over k(θj )).
Deﬁne                                         p       p
                                       p1j = d1 uj + dj vj ,
                             Q
for all j 6= 1, and p1 :=        p1j .
                            j6=1
   In view of the above discussion, we have the following useful observation.
 110CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Remark 4.4.2. Let σ ∈ Gk be such that σ(Tj ) = Tk . Then σ(p1j ) = σs (p1k ), and
                                           !
                                   Y
                       σ(p1 ) = σs    p1σ·l = σs (p1 ).
                                                    l6=1

Assumption 4.4.3. We assume that for all j 6= 1, the curves C1j have solutions
(uj , vj ) with the property that if σθj = θk , then (uk , vk ) = (σuj , σvj ).

    Let gj 6= id be the element of hg2 , . . . , gl i = Gal(K/k(J[2])) ≃ C2l−1 such that
    p         p              √             √
gj ( dj ) = dj and gj ( dk ) = − dk for k 6= j, in other words χ(gj ) = b                 j. Note
                              0                    0       0
that η1 (σ, τ, ρ) = ∂a ∪1 a1 (σ, τ, ρ) when χ1 (σ) = χ1 (τ ) = −χ1 (ρ) = 1. Therefore, for
σ, τ, θ ∈ GK ′ , ∂(∂a ∪1 a01 (−1))(σ, τ, θ) = 1, i.e., ∂a ∪1 a01 (−1) is a 2-cocycle factoring
through Gal(K/k) ≃ C2l−1 o Sl−1 . One can check that this is E1 from §4.3.1, and that
E1 = E1,g , with g such that g K = id and χ01 (g) = −1. Lemma 4.3.16 implies that
                                                                                  Gal(K/k(J[2]))
there is a 1-cochain e1 ∈ C1 (Gal(K/k(J[2])), K × ) such that ∂e1 = resGal(K/k)                  E1 ,
e1 (σs σp ) = e(σs ) and σp e1 (τs ) = e1 (σp · τs ). We have E1 (gj , gj ) = s1j = gj (p1j )p1j for
each j 6= 1. Furthermore, gk (p1j ) = −p1j for j 6= k and E1 takes values in k(J[2])×
and E1 (σ, τ ) = E1 (τ, σ) for σ, τ ∈ Gal(K, k(J[2])). Lemma 4.4.1 implies that there
exists e1 ∈ C1 (K/k(J[2])) such that e1 (gi ) = p1i , and
                                                                       Q
                                                                       t
                                                                            p1im
                                                   t(t−1)
                                                                      m=1
                      e1 (gi1 . . . git ) = (−1)      2                                       .
                                                            Q
                                                            t
                                                                  E(gim , gim+1 . . . git )
                                                            m=1


Since g2 , . . . , gl generate a subgroup Gal(K/k(J[2])) and χ(gi ) = bi for 2 ≤ i ≤ l,
                                                                   Q
for any σ there is a subset Sσ ⊂ {2, . . . , l} such that χ(σ) =      bi. The following
                                                                                        i∈Sσ
proposition gives an ε1 such that ∂ε1 = η1 .

Proposition 4.4.4. Let ε1 be as follows:
             
                                                                   χ(τ )=b
                                                                         0, χ′1 (τ )χ′1 (ρ)=−1
             
             
             
              1                      if                          or χ(τ )=b 1, χ′1 (τ )χ′1 (ρ)=1,
             
                                                                         or  χ′1 (ρ)=1
             
                                                   Q
                                                   t
               e(gi1 · · · git )      if χ(τ ) =        ic     0                 0
                                                         m , χ1 (τ ) = 1, χ1 (ρ) = −1,
 ε1 (τ, ρ) =                                                                                       (4.4.1)
             
             
                                                   m=1
             
                                                Q
             
             
                                                  t
             
              e(g   · · · g    )/p   if χ(τ ) =      ic     0                   0
                                                       m , χ1 (τ ) = −1, χ1 (ρ) = −1.
              i1            it     1
                                                 m=1


Then we have ∂ε1 = η1 .

Proof. The proof will proceed similar to the proof of Proposition 3.2.2. Note that
ε1 (τ, ρ) only depends on χ(τ ), χ01 (τ ) and χ01 (ρ); hence, we will interchangeably use
ε1 (χ(τ ), χ01 (τ ), χ01 (ρ)) for ε1 (τ, ρ). We ﬁrst check that the 1-cochain ∂ε1 (∗, 1, −1) =
 4.4. A CONDITIONAL BUT SIMPLER ALGORITHM                                                                                          111

E1 . All we need to check is that e1 (∗) = ε1 (∗, 1, −1) satisﬁes σp · e1 (τ ) = e1 (σp · χ(τ )).
This follows form the fact that σp E1 (τ, ρ) = E1 (σp · χ(τ ), σp τp ρs ) (Remark 4.3.18),
and that e1 (gi1 . . . git ) is independent of the ordering of gi1 , . . . , git . Hence, ∂e1 =
E1 = ∂a ∪1 ((T1 ) − (T0 )) (Lemma 4.3.16). Noting that ε1 (σ, −1, −1)/ε1 (σ, 1, −1) =
ε1 (b0, −1, −1) = 1/p1 , the proof of Proposition 3.2.2 implies that it is enough to prove
(∂ε1 − η1 )(σ, τ, ρ) = 1 assuming χ01 (σ) = 1. Let σ, τ, ρ be such that χ01 (σ) = 1 and
χ01 (τ ) = χ01 (ρ) = −1 (the case when χ01 (τ ) = 1 is equivalent to ∂e1 = E1 ). Then
                                        σ(ε1 (χ(τ ), −1, −1))ε1 (χ(σ), 1, 1)
                  ∂ε1 (σ, τ, ρ) =
                                    ε1 (χ(σ)σp · χ(τ ), −1, −1)ε1 (χ(σ), 1, −1)
                                            p1 σε1 (χ(τ ), 1, −1)ε1 (χ(σ), 1, −1)
                                  =
                                    σs (p1 )ε1 (χ(σ)σp · χ(τ ), 1, −1)ε1 (χ(σ), 1, −1)2
                                                                        p1
                                  = E1 (χ(σ), σs · χ(τ ))                            .
                                                           σs (p1 )e1 (χ(σ), 1, −1)2
If χ(σ) = gc
           i1 · · · g
                    c it , then σs = gi1 · · · git and
                                                          t                                     2
                                                           Q
                                                                 E1 (gim , gim+1 . . . git )
                           p1                    lt−2t    m=1
                                         = (−1)                                                      .
              σs p1 e1 (gi1 . . . git )2               p1i1 . . . p1it gi1 (p1i1 ) . . . git (p1it )
Note that whether 1 ∈ {χ(σ)} or not depends on whether t is even or odd, respectively.
Assume that t is odd. Then the expression of ∂a ∪ a01 implies
                                                                                   s1                1
                E1 (gi1 , gi2 · · · git )E1 (gi2 , gi3 · · · git ) =                                Q                  = 1.
                                                                               Q
                                                                               t                                 s1j
                                                                                        s1im j /∈{i2 ,...,it }
                                                                               m=2

Therefore,
                              p1                          1                        1
                                                =                     =       0
                                                                                               .
                  σs (p1 )e1 (gi1 · · · git ) 2   si 1 1 · · · si t 1   a ∪ ∂a1 (χ(σ), −1, −1)
When t is even,
                     p1                            1                       1                                     1
                                      =           Q                                      =                                    .
         σs (p1 )e1 (gi1 · · · git )2                          s21j si1 1 · · · sit 1         a ∪ ∂a01 (χ(σ), −1, −1)
                                              ∈{i1 ,...,it }
                                             j/

                           ∂a∪a1 (σ,τ,ρ)
Therefore, ∂ε1 (σ, τ, ρ) = a∪∂a ′ (σ,τ,ρ) = η1 (σ, τ, ρ).
                                         1




4.4.1      Assumption 4.4.3 is not very strict
In this section, we discuss empirical evidence for the fact that assumption 4.4.3 is
good enough to compute the kernel of the CTP on X[2] × X[2] in most cases. For
this purpose, we say that a ∈ S(2) (J/k) is good, if the tuple (d1 , . . . , dl ) corresponding
to a satisﬁes Assumption 4.4.3.
 112CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS

Deﬁnition 4.4.5. An odd-degree hyperelliptic curve C is said to be a good curve if the
subgroup of S(2) (J/k) generated by the good elements and the image of J(k)/2J(k)
is of index at most 2.
    In [PS99] the authors show that h·, ·iCT is an alternating pairing if C has a k-
rational point. In our case C always has a k-rational point T0 . Therefore, it is
enough to compute the CTP on H × S(2) (J), for an index 2 subgroup H of S(2) (J).
LMFDB [LMF24] mentions 1207 genus 2 curves with analytic rank 0 that admit an
odd degree model, with at least 2 extra 2-Selmer group generators. All these curves
are good. Furthermore, there are only the following 2 curves
                       y 2 = 8x5 − 72x4 + 64x3 + 17x2 − 16x − 4,
                       y 2 = 8x5 + 72x4 + 140x3 − 103x2 − 4x,
where the subgroup generated by good elements is of index 2, and for every other
curve the extra part of the 2-Selmer group is generated by good elements.
   Furthermore, in the family of curves y 2 = x5 + A (which will be the focus in the
next chapter), every curve is a good curve for |A| ≤ 2000. The following theorem
proves that every curve is good in a certain family.
Theorem 4.4.6. Let p be a prime, let Cp := y 2 = x(x2 − p2 )(x2 − 4p2 ), let Jp be its
Jacobian variety, and let Tp be the image of Jp [2] inside S(2) (Jp /Q). Then S(2) (Jp )/Tp
is generated by good elements.
    This theorem will be discussed in a work (joint with Tim Evink), where we com-
pute the CTP explicitly for this family, and show that the rank bounds are equivalent
to the ones obtained via visualization. We will not discuss this here in this thesis.
    Naturally, every element of the 2-Selmer group of an elliptic curve is good, and
therefore every 2-Selmer element of a curve in the family of elliptic curves, Ep : y 2 =
x(x2 − p2 ), for p an odd prime, is good. Note that this is a subfamily of the famous
congruent number family. Let p be a prime number, and let g ≥ 2. Deﬁne the
                                  Q
                                  g
hyperelliptic curve Cp,g : y 2 = x (x2 − i2 p2 ). Then in view of the previous theorem
                                  i=1
and the case of elliptic curves, it is a natural question to ask whether, for a ﬁxed
g ≥ 3 and varying primes p, the curves Cp,g are good? Unfortunately, experiments
show that as the genus increases, the good curves in this family seem to become scarce
very fast. For example, if p < 2000, then for g = 3 there are around 74% good curves.
For g = 4, there are around 30% good curves, and for g = 5, we could not ﬁnd any
good curve. Genus 2 seems to be the sweet spot in this regard.

                4.5   Algorithm, implementation and examples

All the computations in the following section and later were performed using the
Magma computer algebra system. For computing half of a point, we used the algo-
 4.5. ALGORITHM, IMPLEMENTATION AND EXAMPLES                                                 113

rithm in [Sto17b, §5]. I thank Michael Stoll for providing me with an implementation
of this algorithm over global ﬁelds, that was later modiﬁed to incorporate the com-
putation over local ﬁelds. I also thank him for providing me with a more eﬃcient
program for checking whether a given odd-degree hyperelliptic curves is good. This
was used in the previous section to get the empirical data.

Remark 4.5.1. The current implementation works over any number ﬁeld under
the assumption that at least one of the elements being paired is good. Apart from
the global bottle-neck of solving norm equations, the current implementation uses a
non-sophisticated mechanism for ﬁnding local points corresponding to the 2-Selmer
elements. Hence, sometimes it is a bit slow and may fail in ﬁnding them. One idea
will be to extract the image of J(kv )/2J(kv ) from the 2-Selmer group computation,
which we anyway have to perform, and feed it inside the algorithm directly.


4.5.1    Algorithm for good elements

Here we provide pseudocode for an algorithm assuming that a ∈ S(2) (J/k) is a good
element. The code mimics Algorithm 1 for most parts.

Algorithm 2 Compute the CTP between a, a0 ∈ S(2) (J/k) represented by d, d0 ∈
A× .
Require: d, d0 ∈ A× such that d represents a good 2-Selmer element.
                                ′
Ensure: Value of (−1)ha,a iCT in variable CT.
 1: M ← 2-dimensional list of size l × l indexed by roots of f with entries as (0, 0).
 2: . M [θ1 , θ2 ] will store solutions to the conic (d(θ1 )u2 − d(θ2 )v 2 )/(θ1 − θ2 ) + 1 = 0.
 3: for θ ∈ {Factors of f } do
 4:     kθ ← k[x]/hθi and θ1 ← a root of θ in kθ .
 5:     for θ0 ∈ {Factors of f over kθ } and θ0 (θ1 ) 6= 0 do
 6:        kθ′ ← kθ [x]/hθ0 i and θ2 ← a root of θ0 in kθ′ .
 7:        if M [θ1 , θ2 ] 6= (0, 0) then
 8:              Compute (u, v) such that d(θ1 )u2 − d(θ2 )v 2 = θ2 − θ1 and uv 6= 0.
 9:              M [θ1 , θ2 ] ← (u, v).
10:              Assign to M at Galois conjugates of the pairs (θ1 , θ2 ), the corre-
     sponding Galois conjugate of (u, v).
11:        end if
12:     end for
13: end for
14: CT ← 1                                                                     . Value of CT.
15: LocalPoints ← [ ].                                  . List storing Pv indexed by Sa,a′ .
16: for v ∈ Sa,a′ do
17:     Find Qv ∈√J(kv ), such that δ(Qv ) = αv .        . α ∈ C1 (Gk , J[2]) is as in §4.3.4.
18:     Kv ← kv ( dv ), Pv ← 12 Qv ∈ J(Kv ).          . Computed using Stoll’s algorithm.
 114CHAPTER 4. THE CTP FOR ODD DEGREE HYPERELLIPTIC JACOBIANS


19:    for T ∈ J[2] and T ∈ / J(kv )[2] do                            . Adjust Pv .
20:        if ∂(Pv + T ) = αv then
21:            Pv ← Pv + T, and exit the inner loop.
22:        end if
23:    end for
24:    LocalPoints[v] ← Pv .
25: end for
26: for θ ∈ {Factors of f } do
27:    kθ ← k[x]/hθi and θ1 ← a root of θ, d01 ← d0 (θ1 ).
28:    for v ∈ Sa,a′ do
29:        for w ∈ {Places of k(θ) above v} do
30:            θ1,w ← Image of θ1 under the embedding kθ ,→ (kθ )w and d01,w ←
      d0 (θ1,w ).
31:            Compute ε1,w and γ1,w as in Equation (4.2.1) using the row in M cor-
    responding to θ1,w .
32:            Compute Γ1,w , ω1,w , and δ1,w . . By Proposition 4.3.15 and Equation
    (4.3.7).
33:            CT ← CT · (δ1,w , d1,w )(kθ )w .
34:         end for
35:     end for
36: end for
37: return CT.

