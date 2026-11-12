# NEW proof obligation: low-degree RR cokernel from a good OUTPUT divisor

The attached exact compiler constructs a product ideal and RR matrix. The
new question is NOT the prior broad high-degree compiler request: prove the
specific LAST low-degree matrix-content implication below, or give a native
counterexample. Highest-effort mathematical work; no tools available.

Work first integrally: R0=Z2[x,y]/(y²-f), f monic squarefree degree2g+1,
D=v2disc f. Input a_i monic integral, b_i integral, a_i|f-b_i²; totaldegree
m polynomial. Let A=prod a_i, I_Q=prod(a_i,y+b_i) overQ2 and J=I_Q intersectR0.
T=R0/(A) is free rank2m; J/(A) is saturated free rankm. Use a primitive
integral basis and an integral membership map Lambda:T->Z2^m. Its pivot
coordinates form an identity, so the quotient lattice is specified, not advice.
The actual point class h=[D_input-m infinity] has a GENERIC reduced degree-g
Mumford pair [a_out,b_out], not supplied algorithmically. For the proof it
obeys polynomial caps v(x_j)>=-2s, |v(y_j)|<=(2g+1)s and
v(x_i-x_j)<=2s for distinct geometric support points. Thus coefficient poles,
Disc(a_out), Res(a_out,f) and inverse Abel differential have polynomial caps.
These good caps arise from a separate native Haar+finite-grid randomization,
not from arbitrary precision advice. All supports are finite/distinct/nonbranch.

Set N*=m+g (assume m>=g so usual basis dimension is m+1). Let E_N* send the
explicit monomial basis of L(N* infinity), x^j and x^j y at their poleweights,
to T. Then M*=Lambda E_N* is an integral m-by-(m+1) matrix of EXACT rankm;
its kernel is L(N* infinity-iota D_input), one-dimensional on the good chart.
Question: bound EVERY nonzero Smith exponent, or the minimum valuation of a
nonzero maximalminor, by poly(g,m,D,s) uniformly in input support collisions
and arbitrarily high input p-adic digits. No arbitrary-matrix example counts.

NEW paid structural facts/proposals to build on (verify if used):
1. For I=(a,y+b), c=(f-b²)/a, I Ibar/a=(a,y+b,y-b,c). This contains(2y,f')
and hence delta=4disc(f), since Af+Bf'=disc(f). Therefore with M=Ibar/a,
delta R0 subset I M subset R0. If I,J are2-saturated ideals, delta*(IJ)^sat
subset IJ: z in(IJ)^sat lies inI; t z for t inM lies inR0 andJ[1/2], henceJ;
multiply a delta decomposition. This pays the product stage with lossD+2,
independently of support separation. Do NOT infer low-degree RR from this alone.
2. At HIGH degree N0=m+2g+1, the proper odd-degree hyperelliptic model has
geometrically integral Gorenstein specialfibre, arithmeticgenusg, smoothinfinity.
J defines a flat finite quotient lengthm. J(N0 infinity) has degree2g+1,
so H1=0 on the specialfibre, and highdegree RR membership is UNIT-surjective.
This remains true at N0-1, paying the top-pole functional. The theorem at
N*=m+g is the missing step; nonspeciality overQ2 alone is not enough.
3. Parent new normalization bound: take the primitive kernel section
F=p+qy, coefficient Gauss valuation0, and let alpha be its top-pole coefficient.
NormF=p²-fq²=A*(+/-alpha² a_out). Because f mod2 has odd degree, it is NOT a
rational square; hence v_G(p²-fq²)=2min(v_Gp,v_Gq)=0. SinceAmonicintegral,
2v(alpha)=-v_G(a_out)<=S_out. Thus GOOD OUTPUT coordinates bound monic
normalization. This does NOT by itself bound the nonzero Smith exponents.

Constructive possible route: arithmetic Serre duality identifies the torsion
cokernel at N* with an evaluation/differential matrix on the OUTPUT divisor.
The latter is a Vandermonde times 1/(2y_j) and embedding matrices; all inverse
losses are bounded by the good geometry and local discriminants. Need an
EXPLICIT lattice comparison to the native Lambda/E_N* matrices, paying delta
and F rather than importing a Neron basis or a model-resolution oracle.
Alternatively derive a polynomial Bezout/syzygy splitting from the norm
identity, or a direct determinant factorization. Do not bury an exponential
Nullstellensatz bound under the wordeffective or assume integral invertibility
from a generic rank. If a different low-degree solver avoids the problematic
minor, give its actual operations/precision and certificate.

Nonintegral inputs can be treated later by explicit polynomial scaling; a
complete integral theorem already changes the next scientific action. Report
precisely whether it bounds M*, only alpha, or merely gives an existential
coordinate chart. Goal is native materialization of the ACTUAL reduced pair,
not a new infrastructure layer or a conditional restatement. No full local
Kummer algorithm, novelty or quantum separation should be inferred from it.
