# Parent odd-prime bridge notes, pending whole extension audit

2026-11-13. These are new constructive calculations for the already-dispatched
odd-prime task, not its API input and not an admitted all-prime algorithm.
No new source or numerical evidence is inferred. Native p is odd, f monic
integral squarefree degree n=2g+1. v_p(p)=1 throughout.

## Formal subgroup with an explicit polynomial R

Use the proved formal seed exponent N=4g^2 and t_i=p^N i. Let V be the
matrix of logarithms of P(t_i). Its determinant valuation D_p is recorded
in LOCAL_HALVING_SATURATION, including the nonunit odd denominators2k+1.
Let W be the derivative matrix (columns omega_k(P(t_i))/dt); the odd-p
inverse-square-root series has integral coefficients. The same alternant
expansion gives
 H=N*g*(g-1)+sum_(i<j) v_p(j^2-i^2).
Higher terms have positive p-adic valuation relative to this Vandermonde,
so this is exact. W andV have integral entries.

Choose R=D_p+H+2. In the Taylor expansion of
log(P(t_i+p^R z)-P(t_i)), the degree-r coefficient, r>=2, has valuation
at least R*r-v_p(r): write binom(l,r)/l=binom(l-1,r-1)/r and use
integrality of the square-root coefficients and nonnegative powers of t_i.
The finitely many low terms and the convergent infinite tail obey the same
bound. Thus after factoring p^R W, each nonlinear coefficient has valuation
at least R*(r-1)-v_p(r)-H>=1. The nonlinear correction is a strict integral
contraction of Zp^g. It follows that actual
 sigma(z)=sum_i(P(t_i+p^R z_i)-P(t_i))
parametrizes U with logU=p^R W Zp^g. Moreover V^-1 has poles at mostD_p,
so R>=D_p implies logU subset logL_p. Actual formal log injectivity gives
U subset L_p=E. Its standard-Haar volume is p^(-gR-H).

Since multiplicationby2 is an automorphism of E, A=J(Qp)/E has
A[2]=J(Qp)[2]. Work in its2primary subgroup; actual representatives may
have arbitrary E-components, and MUST NOT be required to be literal
2primary torsion points. All shifts2sigma lie in ORIGINAL E. This pays
exact quotient bookkeeping once the numerical operations are available.

## Explicit changes in the finite-grid proof

The dyadic collision/branch tube proof remains applicable with conservative
p-exponents, but its constants and source fieldtypecount need rechecked in
the independent odd-prime report. We do not call it already proved here.
The local chart v+2v^2=F(z)/8 is still integral because2 is now aunit;
its branch through0 is smooth/etale and y_new=y(1+4v). However z=4t no
longer forces an actual small formal difference. Replace it by z=p^2 t.
The determinant now contains p^(g(A_local+2))/(2^g prod y_i); the factor2
has valuationZERO. Hence the analogous safe K bound uses g(A_local+2),
not g(A_local+1). The target inverse radius stays Q=2K+1 by the same
adjugate/contraction proof if its coefficient hypotheses are checked.
For all rational halves plus the input, p^(2g+1) is a safe union multiplier.
Exact finite-grid sampling of {0,...,p^m-1} requires bounded rejection from
ceil(log2(p^m)) uniformbits, acceptance>=1/2 perattempt. Allocate its
ABORT probability; never charge a loop of lengthp or p^m.

The pencil discriminant top coefficient N'^N' is NOT aunit in general:
N'=2g+1-2e may be divisible byp. Pay N'v_p(N')<=n log_p n plus the
known inputdiscriminant cap. This only changes the polynomial contentbound,
but must be stated. GenericStoll extraction still requires the newly added
visible Res(U,W) guard; a nonzero augmented determinant alone is insufficient.

Remaining: independent full p-uniform Haar/grid constants, all changed
matrix/field precision guards, and their global bounded clock. No allprime
local, globalSelmer or quantum speedup follows from these bridge calculations.
