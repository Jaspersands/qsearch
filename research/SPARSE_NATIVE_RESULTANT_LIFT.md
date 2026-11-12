# Native sparse norm-leading-coefficient boundary

2026-11-13. The completed OpenAI report
`audits/openai_runs/2026-11-13-sparse-structured/response.md` and complete
independent proof `audits/reviews/2026-11-13-sparse-structured-resultant-lift.md`
were parent-read. This is a reduction for a proposed intermediate
operation, NOT a classical hardness result or a full relation obstruction.

Given explicitly sparse p,q in Z[T,Y], p monic of charged Y-degree d>=2,
0<=m=deg_Y q<d, and R=Res_Y(p,q)!=0, take beta>=1 bounding T-degrees,
D=(d+m)beta, H=d(D+1)+1, qhat=q+T^-H, and

 f=p^3-p*qhat^2-qhat^3,
 u=p(T,y), v=qhat(T,y), w=p(T,y)^2-qhat(T,y)^2.

This is native monic irreducible f of degree3d, with three ORIGINAL
nonconstant Y-basis atoms. Let c in(1,2) satisfy c^3-c-1=0. Over Q(c)(T),
p-c*qhat has every root of T-adic valuation -H/d. Since gcd(H,d)=1,
a proper monic factor would have a nonintegral constant-term valuation;
it is irreducible. Also c=p(y)/qhat(y) lies in Q(T,y), proving degree3d
and irreducibility of f without supplying its constant field as advice.

Here u=cv and w=c^-1*v^2, with v of T-adic valuation -H and c nontorsion.
Consequently

 Alg={(a,b,z):a+b+2z=0},   Rel=Z(1,-3,1).

Put R_H=Res_Y(p,qhat). Tower norms give Nu=Nv=R_H^3, Nw=R_H^6.
In Res(p,q+Z)=sum r_j(T)Z^j, deg r_j<=D, r_0=R and r_d=1.
Because H>D, R_H has the same leading coefficient and degree at infinity
as R; its lowest term T^-dH makes it nonconstant. Thus a norm-LC-at-infinity
routine on these valid native inputs computes (lc R)^3, from which exact
signed cube root recovers arbitrary input resultant LC in this class.
Norm relations alone return Alg, not Rel.

All size costs are paid: with A=1+||p||_1+||q||_1, S=input term count+1,
P=T^H p, Q=T^H q+1, the cleared defining polynomial P^3-PQ^2-Q^3 has
O(S^3) terms and norm<=A^3. Exponent bits are polynomial in log beta
and log d, with numerical Y-degree3d charged. The norm coefficient bound
((d+m)! A^(d+m))^3 has polynomial logarithm; this does not pay extraction
of the first surviving coefficient of its potentially huge expansion.

Exact symbolic control: p=(Y-T^M)^d+T, q=Y-T^M, d,M>=2 with binary M,
gives R=(-1)^d T and R_H=T^-dH+(-1)^d T. The norm has actual infinity
degree3 despite cancellation of the uncombined scale3dM. In normalized
Puiseux coordinates t=T^-1/d, x=y-T^M=t^-1 X, the branch equation is
X^d+1-c*t^(d-1)X-c*t^(d(H+1))=0. Simple roots lambda^d=-1 give aligned
LC tuple(c*lambda,lambda,c^-1*lambda^2). For odd d, lambda=-1 uses Q(c).
Under an arbitrary uniformizer the correct identity is
LC(v)^d=-LC(T), not an invariant assertion LC(v)^d=-1.

The full relation lattice of this family is already explicit above;
the normalized T-adic LC tuple(c,1,c^-1) is easy too. Therefore this
does not force arbitrary places or all LC methods through resultant LC,
nor prove the full native relation problem difficult. Park this particular
norm-LC route pending a genuine extraction algorithm; no further
cancellation fixtures or quantum implementation are justified.

The alternative torus-logarithm plus finite-valuation construction is
being tested against the SAME growing-degree full native problem.
