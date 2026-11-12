Source research/audits/sources/surface_module_2026/couveignes_edixhoven_book.txt; SHA256 0ae7a4befba82ce944abeb0f71f745403bcbb9c8418232d050c8e6effba83dd9
Physical newline ranges. PARENT VISUALLY CHECKED PDF printed188-189: m_s(f) is max multiplicity of NEGATIVE PART div(f)_- along vertical components. div(f)=div(f)_+ - div(f)_-. PDF text drops minus signs.

LINES 9003-9180
9003: 9.1.3 Theorem Let X be a geometrically irreducible, smooth, and com-
9004: plete curve of positive genus over a number field K, and let X be a proper
9005: semistable model of X over the ring of integers OK of K. Suppose that we
9006: have a nonconstant morphism f W X ! PK1 and a K-rational point Q of X
9007: with f .Q/ ¤ 1. Write the divisor div.f / of f as div.f /C div.f / , with
9008: div.f /C and div.f / effective and without common irreducible compo-
9009: nents. Assume that the Zariski closure of Supp.div.f /C / [ Supp.div.f / /
9010: in X is étale over OK . For any closed point s of Spec.OK /, denote by
9011: ms .f / the supremum of the multiplicities of div.f / on X along the irre-
9012:                         bookcourant     January 8, 2011
9013: 
9014: 
9015: 
9016: 
9017: APPLYING ARAKELOV THEORY                                                         189
9018: 
9019: ducible components of the fiber at s of X . Then we have the inequality
9020:                                           X
9021: .f .Q/; 1/P 1 .Q; f  1/X C deg f             sup g
9022:                                               X
9023:                      1X
9024:                          Z                      X
9025:                    C        log.jf j2 C 1/X C   ms .f / log #k.s/ :
9026:                      2  X                     s
9027: 
9028: Here the first sum runs over the embeddings of K into C, and the last sum
9029: runs over the closed points of Spec.OK /.
9030: 
9031: 
9032: Proof Note that the locus of indeterminacy of f on X consists of finitely
9033: many closed points. This implies that there exists a blow-up XQ ! X of X
9034: such that f extends to a regular map f W XQ ! PO   1
9035:                                                      K
9036:                                                        . For any such XQ we
9037: have by construction
9038: 
9039:               .f .Q/; 1/P 1 D deg f .Q/ .OP 1 .1/; k  kP 1 /
9040:                               D deg Q f  .OP 1 .1/; k  kP 1 /
9041:                               D deg Q .OXQ .f  1/; k  kP 1 / ;
9042: 
9043: where we write 1 to emphasize that f  1 is the inverse image under f of
9044: 1.Spec.OK //, and not the Zariski closure f  1 of the inverse image under
9045: f of 1.Spec.K//. If we let k  kX denote the canonical Arakelov metric on
9046: OX .f  1/ then we can write
9047: 
9048:                                                                     k  kP 1
9049:  deg Q .OXQ .f  1/; k  kP 1 / D deg Q .OXQ .f  1/; k  kX              /
9050:                                                                     k  kX
9051:                                 D deg Q .OXQ .f  1/; k  kX /
9052:                                       X         k  kP 1
9053:                                           log..          /.Q //
9054:                                        
9055:                                                 k  kX
9056:                                                    X         k  kX
9057:                                 D .Q; f  1/XQ C       log..           /.Q // :
9058:                                                     
9059:                                                              k  k P 1
9060: 
9061: 
9062: 
9063: A bound for log..k  kX =k  kP 1 /.Q // follows by testing on the tautological
9064: section 1, giving
9065: 
9066:                                                   1
9067: log k1kX .Q / log k1kP 1 .Q / D g .f  1; Q /C log.jf .Q /j2 C1/ :
9068:                                                   2
9069:                       bookcourant     January 8, 2011
9070: 
9071: 
9072: 
9073: 
9074: 190                                                                 CHAPTER 9
9075: 
9076: Applying Proposition 9.1.4 below at this point shows that
9077:                            1
9078:             g f  1; Q C log jf .Q /j2 C 1
9079:                                                   
9080:                                2
9081:                                    1
9082:                                      Z
9083:                 .deg f / sup g C      log.jf j2 C 1/ X :
9084:                           X       2 X
9085: This accounts for the second and third terms in the bound of the theorem.
9086: We are finished once we prove that .Q; f  1/XQ .Q; f  1/X is bounded
9087: by s ms .f / log #k.s/ for a particular choice of XQ . (The usual projec-
9088:     P
9089: 
9090: tion formula shows that in fact .Q; f  1/XQ is independent of the choice
9091: of XQ .) On any XQ we write f  1 as a sum f  1 D .f  1/hor C .f  1/vert
9092: of a horizontal and a vertical part. Note that .f  1/hor D f  1, with
9093: the Zariski closure now taken in XQ . Since the local intersection multiplic-
9094: ities of Q and f  1 do not go up when passing from X to XQ , we have
9095: .Q; .f  1/hor /XQ D .Q; f  1/XQ  .Q; f  1/X , and thus we are reduced
9096: to proving that, for a particular choice of XQ , .Q; .f  1/vert /XQ is bounded
9097:                  P
9098: from above by s ms .f / log #k.s/.
9099:    We exhibit a specific blow-up, and we calculate which multiplicities f
9100: acquires along the irreducible components of the vertical fibers of this blow-
9101: up. Note that the locus of indeterminacy of f on X consists precisely of
9102: the closed points of X where an irreducible component C from the zero
9103: divisor div.f /C of f on X and an irreducible component C 0 from its po-
9104: lar divisor div.f / meet. Now since by assumption the Zariski closure of
9105: Supp.div.f /C / [ Supp.div.f / / in X is étale over OK , this can only hap-
9106: pen when at least one of C , C 0 is vertical. In points where this happens we
9107: have to perform a sequence of successive blowings-up until a component
9108: arises with multiplicity 0 for f , so that the components with positive multi-
9109: plicities and the components with negative multiplicities are separated from
9110: each other.
9111:    We begin by observing that it will cause no harm if we pass to a finite
9112: extension K ! K 0 . Indeed, both the left-hand side and the right-hand side
9113: of the inequality that we wish to prove get multiplied by ŒK 0 W K if we do
9114: this. Here is why. For the terms .f .Q/; 1/P 1 and .Q; f  1/ the scaling
9115: by a factor ŒK 0 W K follows from general properties of the Arakelov inter-
9116: section product (cf. [Fal1], p. 404, for example). (Note that it is understood
9117: that over K 0 , intersection products are taken on the minimal resolution of
9118:                         bookcourant     January 8, 2011
9119: 
9120: 
9121: 
9122: 
9123: APPLYING ARAKELOV THEORY                                                   191
9124:                                                 P
9125: the pullback of the model X .) That the term  supX g scales by a fac-
9126: tor ŒK 0 W K is obvious. Finally, fix a closed point s of Spec.OK / and let
9127: s 0 be any closed point of Spec.OK 0 / above it. Denoting by es 0 the ramifica-
9128: tion index of s 0 over s and by fs 0 the degree of the residue field extension
9129: of s 0 over s, we see that for any s 0 above s, the integer ms .f / gets multi-
9130: plied by es 0 , and the number log #k.s/ gets multiplied by fs 0 . Using that
9131:                       0                                              0
9132: P
9133:     s 0 es 0 fs 0 D ŒK W K, the sum running over the closed points s above s,
9134:                                        P
9135: we see finally that also the term s ms .f / log #k.s/ gets multiplied by
9136: ŒK 0 W K.
9137:     Starting with X over OK , we first do the following. Let x be a closed
9138: point on X that is the intersection of a vertical component C and a horizon-
9139: tal component C 0 having nonzero multiplicities m and m0 for f that have
9140: different signs. After blowing up in x, we obtain an exceptional divisor E
9141: whose multiplicity for f is mCm0 . We have two distinguished points on E,
9142: one lying on the strict transform of C , and one lying on the strict transform
9143: of C 0 . At exactly one of them there is a sign change for the multiplicities,
9144: or m C m0 D 0. If a sign change happens at the double point lying on the
9145: strict transform of C 0 , then we repeat the process. If a sign change happens
9146: at the double point lying on the strict transform of C or if m C m0 D 0, we
9147: stop, and continue with a new point x 0 , if available.
9148:     We end up with a blow-up X 0 ! X such that an intersection of two ir-
9149: reducible components C , C 0 that have different signs in div.f / on X 0 only
9150: occurs for C , C 0 both vertical. For this, we did not yet need to extend the
9151: ground field K. In order to continue, we note the following. Suppose that
9152: we have a closed point x on the model X 0 of X over OK which is a double
9153: point of a vertical fiber, and two irreducible components C , C 0 of that verti-
9154: cal fiber pass through x, having nonzero multiplicities m and m0 for f that
9155: differ in sign. Assume that K ! K 0 is a Galois extension that ramifies over
9156: the image of x in Spec.OK /, with a ramification index e that is a multiple
9157: of m m0 . In passing to the minimal resolution XQ of XO0 0 , the point x gets
9158:                                                              K
9159: replaced by a chain of e 1 projective lines of self-intersection 2. The mul-
9160: tiplicities of f along these components change in e steps from e m to e m0 ,
9161: so that the steps are m m0 and a multiplicity 0 will appear somewhere,
9162: because m m0 is a divisor of e m.
9163:     Thus we see how we can reach our goal. Take a Galois extension K ! K 0
9164:                       bookcourant     January 8, 2011
9165: 
9166: 
9167: 
9168: 
9169: 192                                                                  CHAPTER 9
9170: 
9171: that ramifies as specified above over the images in Spec.OK / of the double
9172: points where components meet with a different sign for f . (This is always
9173: possible.) By our remarks above, it suffices to prove the inequality over K 0 .
9174: By construction, the morphism f extends over the model XQ that arises in
9175: this way. Moreover, it follows from the construction that for s 0 a closed point
9176: of Spec.OK 0 / and s its image in Spec.OK / we have ms 0 .f /  es 0 ms .f /.
9177: Hence the sum of the local intersection numbers .Q; .f  1/vert /s 0 for all s 0
9178: over s is bounded from above by ŒK 0 W Kms .f / log #k.s/. This is what we
9179: needed to prove.                                                              
9180: 

LINES 4449-4498
4449: nant of cohomology to theta functions on the Jacobian of X. Let Hg be
4450: the Siegel upper half-space of complex symmetric g-by-g matrices with
4451: positive definite imaginary part. Let  in Hg be the period matrix at-
4452: tached to a symplectic basis of H1 .X; Z/ and consider the analytic Jacobian
4453: J .X / D C g =.Zg C  Zg / attached to . On C g one has the Riemann
4454: theta function #.zI  / D n2Zg exp. i tn n C 2 i tnz/, giving rise to a
4455:                            P
4456: 
4457: reduced effective divisor ‚0 and a line bundle O.‚0 / on J .X /. Now con-
4458: sider on the other hand the set Picg 1 .X / of divisor classes of degree g 1
4459: on X. It comes with a canonical subset ‚ given by the classes of effective
4460: divisors. A fundamental theorem of Abel-Jacobi-Riemann says that there
4461: is a canonical bijection Picg 1 .X / Q! J .X / mapping ‚ onto ‚0 . As
4462: a result, we can equip Picg 1 .X / with the structure of a compact complex
4463: manifold, together with a divisor ‚ and a line bundle O.‚/.
4464:    The function # is not well defined on Picg 1 .X / or J .X /. We can
4465: remedy this by putting
4466: 
4467: .4:4:5/    k#k.zI  / D .det =. //1=4 exp.  ty.=. // 1 y/j#.zI  /j;
4468:                       bookcourant     January 8, 2011
4469: 
4470: 
4471: 
4472: 
4473: 92                                                                   CHAPTER 4
4474: 
4475: with y D =.z/. One can check that k#k descends to a function on J .X /.
4476: By our identification Picg 1 .X / Q! J .X / we obtain k#k as a function
4477: on Picg 1 .X /. It can be checked that this function is independent of the
4478: choice of  . Note that k#k gives a canonical way to put a metric on the line
4479: bundle O.‚/ on Picg 1 .X /. For any line bundle L of degree g 1 there is
4480: a canonical isomorphism from .L/ to O. ‚/ŒL, the fiber of O. ‚/ at
4481: the point ŒL in Picg 1 .X / determined by L. Faltings proves that when we
4482: give both sides the metrics discussed above, the norm of this isomorphism
4483: is a constant independent of L; he writes it as exp.ı.X /=8/. In more ex-
4484: plicit terms, this means that for any line bundle L of degree g 1 on X with
4485: h0 .L/ D 0 (and hence h1 .L/ D 0) we have
4486:                                     1
4487: .4:4:6/          .L/ D C;      k1k.L/ D exp.ı.X /=8/k k.ŒL/:
4488: 
4489: The invariant ı.X / of X appears in the Noether formula, see below.
4490:    We will now turn to intersections on an arithmetic surface. For us, an
4491: arithmetic surface is a proper, flat morphism pW X ! B with X a regular
4492: scheme, with B the spectrum of the ring of integers OK in a number field K,
4493: and with generic fiber a geometrically connected and smooth curve X=K.
4494: We say that X is of genus g if the generic fiber is of genus g. We will always
4495: assume that p is a semistable curve, unless explicitly stated otherwise. After
4496: we extend the base field if necessary, any geometrically connected, smooth
4497: proper curve X=K of positive genus with K a number field is the generic
4498: fiber of a unique semistable arithmetic surface.
