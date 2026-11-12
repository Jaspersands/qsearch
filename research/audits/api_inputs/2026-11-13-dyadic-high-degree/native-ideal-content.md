# New hard lemma: native ideal-product saturation, not raw interpolation

The attached completed RR compiler gives a specific exact-field operation.
Your task is a NEW quantitative algebra question on that operation, using the
new parent structural observation below. Earlier questions asked for a broad
compiler or uniform RR reset; do not repeat their conditional conclusions.
Try to prove this native content bound or find an actual graph-ideal family
that defeats it. No arbitrary-matrix counterexample, no source claims from
memory. Exact constructive replacement is welcome if it evades a counterexample.

Native curve f monic squarefreeZ2[x], degree2g+1, D=v2disc f. Input graph
blocks I_i=(a_i,y+b_i) in R=Q2[x,y]/(y²-f), a_i monic, a_i divides f-b_i²,
deg b_i<e_i=deg a_i, totaldegree m=sum e_i=O(g). Each block is ACTUAL finite
closed-divisor data, not merely approximate equations; repeated/colliding
supports and opposite sheets are allowed. Coefficient poles at most S, with
S polynomial. The question must be uniform in ALL higher p-adic digits and
support collisions. No splitting fields or pairwise separation is advice.

Exact compiler: A=prod a_i, T=R/(A), dimension2m overQ2. X companion ofA,
Y=[[0,f(X)],[I,0]]. For J_i=(a_i,y+b_i), multiplication generators are
G_i=diag(a_i(X),a_i(X)) and H_i=[[b_i(X),f(X)],[I,b_i(X)]]. StartingV0=I,
C_i=[G_i V_(i-1) | H_i V_(i-1)] has knownrank2m-sum_(j<=i)e_j. Select a
saturated integral column basis V_i via minimum-valuation maximalminor.
The output entries then become integral, but exposing the minor has UNPAID
precision. At finalstage membership Lambda_D gives RR matrix M_D=Lambda_D E_N,
N=m+2g+1, rankm, kernel dimensiong+2. The attached report specifies everymatrix.

Parent proposed new algebraic mechanism: first assume blocks integralS=0.
R0=Z2[x,y]/(y²-f). Every R0/I_i=Z2[x]/a_i is Z2-free. Although the special
fiber can be singular, the Jacobian ideal (2y,f') contains4disc(f): if
A_f f+B_f f'=disc(f), then (2A_f y)(2y)+4B_f f'=4disc(f).
Thus the failure of smoothness is annihilated by2^(D+2), uniformly over the
curve. Can one use this to bound the torsion/saturation defect of the product
ideal I_1...I_i in R0/(A), e.g. annihilation by2^poly(m,D)? If so, pay the
knownrank C_i minors without dividing by a support-collision difference.
Maybe use matrix factorizations of graph ideals, conductor/trace pairing,
Fitting ideals, Tor, or an explicit fraction-free Bezout splitting. A valid
proof must handle multiplicities and opposite sheets, not assume etale divisors.
The raw distinct-point evaluation counterexample in the report is NOT a
counterexample to this product-ideal construction; its divided-difference
repair shows why. Conversely, do not assume flat individual quotients make
the product quotient flat. Test that inference first.

Then extend to input poleS by explicit integral scaling with polynomialloss,
and to the fixed high-degree RR kernel M_D. The projection at infinity may
have its own theta content: identify it rather than silently asserting that
nonspeciality gives an integral rank bound. If good final reduced Mumford
coordinates/discriminant could bound that last minor, state the exact bridge.
A uniform cap for only C_i is still a valuable result; do not inflate it.

Desired theorem: after specified denominator clearing, every needed maximal
minor minimum has valuation <=poly(g,m,D,S), independently of arbitrary
support proximity. Or a native family at fixedg,D,S with growing loss in the
ACTUAL C_i/M_D matrices; explain whether this defeats representation selection
or only this implementation. No regular/Neron model construction, global
field height advice, exponential enumeration or exact-zero oracle is allowed.
Known ranks may permit rejection with finite certificates, but a positive
success rate/cap must be proved. If complete, give a polynomial precision
schedule including input approximation, output coefficient recovery and
actual-point verification. Use highest reasoning, focused proof report.
