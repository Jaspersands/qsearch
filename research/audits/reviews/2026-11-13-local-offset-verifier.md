# Local ternary transport: counterfamily, certificate, and spinor verifier

2026-11-13. Independent review of EXPANDED_NORM_TERNARY_TRANSPORT.md and
the complete terminal OpenAI local-offset report. No tests, CAS, network,
API, Git, or archives used. The report's mathematical conclusions check
with the series proof and precision implementation specified below.

**Scope.** This proves an exact counterexample to the stated independent
component matcher/irreversible residue lift, and an all-input finite seed
verifier plus offset extractor. It does NOT construct a seed, certify NO
when one seed fails, or close native integral isometry decision. Stabilizer
spinor groups and local squareclass arithmetic retain their charged inputs.

## 1. The dyadic counterfamily is exact for every m>=2

Over Q_2 let

    A=diag(1,4,-25*2^(2m)),  B=diag(5,20,-2^(2m)),
    U=[[1,-4,0],[1,1,0],[0,0,1/5]].

The two first-column norms are 5 and 20 with zero cross term; the last
coordinate contributes -2^(2m). Thus U^T A U=B and det(U)=1. Its entries
are 2-integral. Both determinants are -100*2^(2m), and both forms are
nonsingular and real indefinite. Their displayed rank-one Jordan scales
are distinct, with valuations (0,2,2m), and unit squareclasses respectively
(1,1,-1) and (5,5,-1). The diagonal bases also satisfy the usual good-BONG
valuation condition; no BONG classification theorem is needed here.
Since 5 is not a Q_2 square, independent matching of these displayed lines
rejects an actually isometric pair. Cross-scale mixing is essential.

Although A=B mod 4, no isometry Y=I mod 2 exists. Its first column would
have x odd and y,z even, whence x^2+4y^2-25*2^(2m)z^2=1 mod 8, not 5.
For X=I the relative error is diag(-4/5,-4/5,24), of minimum valuation 2.
It lies exactly at the excluded threshold 2v_2(2); this does not contradict
the strict lifting lemma. Increasing precision while retaining this residue
class cannot fix it. The successful U has its (2,1) entry odd.

The supplied global identification need not make the answer immediate.
Set a=5*2^m and let R act on coordinates 1,3 by
[[5/4,3a/4],[3/(4a),5/4]], fixing coordinate 2. The identity 25-9=16 gives
R^T A R=A and det(R)=1. Hence F=RU satisfies F^T A F=B, det(F)=1, but
F_(3,1)=3/(4a) is nonintegral. All coefficient lengths are O(m).
This refutes only the specified uncoupled/greedy construction, not a coupled
algorithm or a uniform existence theorem for local transport.

## 2. A finite seed certifies an actual integral isometry

Let E=K_p be any characteristic-zero nonarchimedean completion, v(pi)=1,
e=v(2), and let A,B be nonsingular symmetric integral 3-by-3 matrices.
An exact global identification F in GL_3(K) with F^T A F=B is assumed
verified. Choose s_B>=0 bounding the pole orders of B^-1; v(det B) is safe.
For M=s_B+2e+3, the finite certificate is

    X in GL_3(O_E/pi^M),     X^T A X=B mod pi^M.

Choose integral representatives, still denoted X. Their determinant is a
unit. Put T=B^-1(X^T A X-B) and use the known bound r=M-s_B>2e on v(T),
where matrix valuation is the minimum entry valuation. Since BT is symmetric,
T is B-self-adjoint. Let C=sum_(j>=0) binom(-1/2,j) T^j.

For j>=1, binom(-1/2,j)=(-1)^j binom(2j,j)/4^j. The central binomial
coefficient is even, so at dyadic places its valuation is at least e.
At odd places the denominator is a unit. Uniformly,

    v(binom(-1/2,j)) >= -(2j-1)e,
    v(binom(-1/2,j)T^j) >= j(r-2e)+e.

Therefore C converges, C-I has valuation >=r-e, and the tail starting
at j=J>=1 has valuation >=J(r-2e)+e. This sharper coefficient estimate
is necessary to justify the report's displayed r-e bound. The identity
C^2(I+T)=I is a convergent power-series identity, and C^T B=BC. Consequently

    Y=XC in GL_3(O_E),       Y^T A Y=C^T B(I+T)C=B.

Conversely every integral isometry reduces to such a certificate. This is
an exact finite existence criterion, not permission to enumerate residues.

To obtain Y modulo pi^P, take J=max(1,ceil((P-e)/(r-2e))) and use
Y_J=X sum_(j=0)^(J-1) binom(-1/2,j)T^j. One may evaluate this FINITE
polynomial exactly over K: O_K/p^M representatives from ideal HNF have
polynomial bit length, J is polynomial in P,e, and products/powers of
polynomially many expanded fixed-size matrices have polynomial heights.
Thus no hidden floating/local precision guard is needed. In a truncated
implementation the binomial denominators must instead be explicitly paid.
T=0 is harmless, with C=I; the same conservative lower bound r still works.

Properness is relative to F, not to the raw determinant of Y. Set g=YF^-1;
then g^T A g=A and det(g)=det(Y)/det(F) is exactly +1 or -1. The valid
seed implies v(det B)=v(det A), so det(F) is a unit, as is det(Y).
Compute the ratio from det(Y_J)/det(F): Y,Y_J are integral, so absolute
precision e+1 suffices to distinguish the signs. This avoids extra losses
from taking a determinant of pole-bearing entries of g. Replace Y by -Y
when necessary. Odd rank makes this an integral orientation correction.

## 3. Four charts cover EVERY proper ternary isometry

Take an expanded diagonalization D=W^T A W=diag(a_1,a_2,a_3), and
h=W^-1 g W in SO(D). Such W is obtainable by fixed-rank symmetric
elimination, using an off-diagonal pair if a diagonal pivot is zero.
For b(u,v)=u^T Dv and q(u)=b(u,u), reflection in an anisotropic vector is
r_u=I-2u(u^T D)/q(u). Direct matrix multiplication gives

    1+tr(r_u r_v)=4 b(u,v)^2/(q(u)q(v)).

Every proper ternary isometry is a product of two such reflections,
including identity as r_u r_u. Here is an all-input justification.
For h!=I, the polynomial q((h-I)x) is nonzero: otherwise im(h-I) is
totally isotropic and has dimension <=1. A nonzero rank-one orthogonal
map h-I=u*l satisfies 2b(u,x)+q(u)l(x)=0; nondegeneracy forces q(u)!=0,
making h a reflection of determinant -1, a contradiction. Over the
infinite field E choose x with both q(x) and q(hx-x) nonzero. Reflection
in hx-x composed with h fixes x and has determinant -1. Its restriction
to the nonsingular binary complement is a reflection: its eigenvalues
are +1,-1, with orthogonal anisotropic eigenlines. This proves the claim
even for nonsemisimple h; no reflection decomposition must be computed.

Whenever t=1+tr(h)!=0, the identity above therefore gives theta(h)=[t]
in E*/E*2, using theta(r_u)=[q(u)]. The excluded trace-zero case is real.
Use S_0=I and S_1,S_2,S_3 the diagonal sign matrices with respectively
coordinates (2,3), (1,3), (1,2) negated. All are proper, and sum S_j=0.
For t_j=1+tr(S_j h), sum t_j=4, so some v(t_j)<=2e. For any such chart,

    theta(g)=theta(S_j)[t_j],
    theta(S_0)=1, theta(S_1)=[a_2a_3],
    theta(S_2)=[a_1a_3], theta(S_3)=[a_1a_2].

Spinor norm is natural under the isometry W and multiplicative; squareclass
inversion is the identity. These facts justify the orientation and factors.
No trace-zero division, genericity assumption, or hidden chart oracle occurs.

## 4. Robust chart selection and offset precision

Let s(Z)=max(0,-min_ij v(Z_ij)) for a known matrix Z, and put
beta=s(W^-1)+s(F^-1)+s(W), P=beta+4e+1. An error of valuation >=P in Y
gives error >=4e+1 in all t_j. Hence computing the four residues detects
some valuation <=2e exactly. Zero or high-valuation charts may be skipped;
they need not be distinguished from one another. The chosen representative
tilde t satisfies v((tilde t-t)/t)>=2e+1, so tilde t/t is a square by
Hensel's criterion applied at 1. Thus its squareclass is certified.
The same P already exceeds e+1 for the preceding orientation test.

Multiply by the exact chart factor and use the charged local-squareclass
routine, then reduce modulo theta(SO(A,O_E)). Different proper certified
transporters Y_1,Y_2 have g_2 g_1^-1=Y_2Y_1^-1 in this integral stabilizer,
so the resulting coset is independent of the seed and its representatives.
Expanded norm-height bounds, after denominator clearing, bound all needed
nonzero valuations s_B,beta polynomially. Also e<=[K:Q], and residues have
M log|O_E/pi| information bits, with expanded order/ideal arithmetic charged.
This pays a verifier and extractor, not seed discovery or stabilizer generation.

## 5. Exact neighbor check and its location

Let s=17^4=83521, A=diag(1,289,-s), and

    F=P=[[3,0,1/3],[0,1,0],[0,0,1/3]],
    B=P^T A P=[[9,0,1],[0,289,0],[1,0,-9280]].

At the place 3 set v=(1,0,4), d=q(v)=1-16s=-3*445445, and
g=r_v r_(e_2). These reflections commute, so g is a proper involution.
The actual transporter is

    X=gP=[[3(d-2)/d,0,(-1-8s)/(3d)],
          [0,-1,0],[-24/d,0,(16s-7)/(3d)]].

Here v_3(d)=1. The last-column numerators -668169 and 1336329 are both
divisible by 9; the first-column numerators have valuation at least 1.
Thus X is 3-integral, det(X)=1, and X^T A X=B. Its self-isometry relative
to F is precisely g. The spinor norm is [289d]=[d]=[3], because
d/3=-445445=1 mod 3. Meanwhile 1+tr(g)=0. The S_3 chart gives
1+tr(S_3g)=4/d and theta(S_3)=[289], recovering the same class.

P and P^-1 have denominators supported only at 3. At every other finite
place take X=P, with relative self-isometry I and offset 1. In particular,
the offset AT 17 is 1: the nontrivial idele component is AT 3. Its given
ray character is (3/17)=-1 (3^8=-1 mod 17). This checks the reported local
data; the previously supplied global spinor-character computation is not
re-proved by this local calculation. No ordinary-class-group replacement
or full integral-isometry algorithm follows from this certificate.
