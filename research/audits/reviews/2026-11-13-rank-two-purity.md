# 2026-11-13 Exact rank-two stabilizer purity

## Result

For every normalized pure state of stabilizer rank at most two, in every
dimension, define

    Pi(psi)=2^-n sum_(a,b in F_2^n) |<psi|X^a Z^b|psi>|^4.

Then

    Pi(psi) >= 1801/21952 > 1/16.                                      (1)

Thus rank two does NOT falsify Pi>=k^-4. The exact global minimum is attained
on six qubits (with arbitrary stabilizer spectators) by

    psi=(|0^6>+exp(i theta)|+^6>)/sqrt(2+cos(theta)/4),
    t=cos(theta),  16t^3+4t^2+4t+15=0,  -1<t<0.                       (2)

The cubic has exactly one root in this interval. The exact minimum is

    [128t^4+64t^3+264t^2+1072t+1199] / [2(t+8)^4].                    (3)

In particular it is strictly smaller than the real-minus value 65/686, and
strictly smaller than 19/200. No result for growing stabilizer rank follows.
The proof is analytic; the finite rational Bernstein certificate below was
checked by symbolic polynomial arithmetic, not numerical minimization.

## All pair types reduce to two forms

Purity is Clifford invariant and multiplicative under tensor products; a
stabilizer factor has purity one. Send the first stabilizer to |0^n>.
The second has uniform-magnitude amplitudes on an affine binary space A,
with a quadratic stabilizer phase. A diagonal Clifford removes that phase
on A and fixes |0^n> up to a harmless global phase. This follows by extending
affine coordinates on A to the ambient binary space and extending the
linear mod4/quadratic mod2 phase polynomial in those coordinates.

If the overlap is nonzero, 0 belongs to A. A linear reversible binary map
therefore gives the pair |0^m>,|+^m>, with common |0> spectators; the overlap
is s=2^(-m/2). If the overlap is zero, 0 is outside A, and such a map gives
|0>|0^m>,|1>|+^m>, again with common spectators. These arguments include
all quadratic phases and signed common-stabilizer types. A coincident pair
is already rank one. The zero vector produced by cancellation is excluded.

Write coefficients alpha,beta with |alpha|^2+|beta|^2=1, and put

    z=|alpha|^2-|beta|^2, t=2 Re(conj(alpha) beta),
    u=2 Im(conj(alpha) beta),       z^2+t^2+u^2=1.                     (4)

This parametrizes every coefficient ratio and phase, including a zero
coefficient. In the nonorthogonal case the squared norm is N=1+s*t>0.

## Exact Pauli moment formulas

For the nonorthogonal pair let d=2^m=s^-2 and m>=1. Among its d^2 Paulis:

- The identity expectation after normalization is one.
- For a=0,b!=0, the expectation is ((1+z)/2+s*t)/N; there are d-1.
- For a!=0,b=0, it is ((1-z)/2+s*t)/N; there are d-1.
- For a,b!=0 and a.b=0, its magnitude is |s*t|/N; there are
  (d-1)(d/2-1).
- For a.b=1, its magnitude is |s*u|/N; there are d(d-1)/2.

Unsigned X^a Z^b may be anti-Hermitian; the absolute fourth power removes
this convention. Consequently, with X=z^2 and c=1/2+s*t,

    Pi = s^2 + (1-s^2)/(1+s*t)^4 * {
           2c^4+3c^2 X+X^2/8
           +(s^2/2-s^4)t^4+(s^2/2)(1-t^2-X)^2 }.                    (5)

This is an exact cancellation-sensitive formula, not a triangle bound.

For the orthogonal pair, normalization is already one. The flag-I/Z
expectations give 1+z^4+2(d-1)(|alpha|^8+|beta|^8). Summing the flag-X/Y
fourth powers over the d^2 physical Paulis gives exactly t^4+u^4, since each
cross amplitude has magnitude d^-1/2. Thus

    Pi=[1+z^4+2(d-1)(|alpha|^8+|beta|^8)+t^4+u^4]/(2d).              (6)

At fixed X=z^2, t^4+u^4 is minimized by t^2=u^2=(1-X)/2. Substitution gives

    Pi >= [(d+5)/4 +(3d-5)X/2 +(d+5)X^2/4]/(2d).                   (7)

For d>=2 the minimum is X=0 and equals (d+5)/(8d)>1/8. For d=1 the
minimum is 2/3 at X=1/3. Orthogonal pairs therefore cannot be global minimizers.

## Coefficient and phase minimization

For m<=3 the identity term alone gives Pi>=1/d>=1/8. For m>=3, differentiate
the braces in (5) with respect to X. The derivative is

    3(1/2+s*t)^2-s^2(1-t^2)+(1/4+s^2)X.

Its first two terms, minimized over all real t, are at least 3/16-s^2>=1/16.
Therefore X=0 is the unique minimum for each t: equal coefficient magnitudes
are optimal, and u^2=1-t^2. Formula (5) becomes

    P_s(t)=s^2+(1-s^2)F_s(t)/(1+s*t)^4,
    F_s(t)=1/8+s^2/2+s*t+2s^2*t^2+4s^3*t^3+(s^4+s^2)t^4.           (8)

Its derivative has the sign of

    G_s(t)=1/2-2s^2+s*t+8s^2*t^2+4s*t^3,
    G_s'(t)=s(1+16s*t+12t^2)>=s(1-16s^2/3)>0.                    (9)

For m>=7, s<=1/(8sqrt(2))<9/100, and G_s(-1)=1/2-5s+6s^2>0.
Hence real subtraction t=-1 minimizes the phase. There

    P_s(-1)=(28s^3-28s^2+7s-1)/(8(s-1)^3),
    d/ds P_s(-1)=-(28s^2-21s+2)/(4(s-1)^4)<0                     (10)

on 0<=s<=9/100. In particular every m>=7 satisfies

    Pi>P_(9/100)(-1)=19/200+91851/150714200>19/200.                 (11)

For m=6, s=1/8, (9) gives precisely the cubic in (2). It is negative at
t=-1 and positive at t=0, so its unique root is the strict phase minimum.
Substitution gives (3). Real subtraction is not optimal here, and

    min_t P_(1/8)(t)<P_(1/8)(-1)=65/686<19/200.                    (12)

For completeness, the following small exact positivity certificate excludes
m=4,5; it avoids any optimization over a numerical phase grid. Define

    R_s(t)=200(1+s*t)^4 [P_s(t)-19/200].

For s=1/4, 256 R_s(t) is

    A(t)=3181t^4+2896t^3+5376t^2+10336t+5836.

For s=sqrt(2)/8,

    1024 R_s(t)=6381t^4+2896sqrt(2)t^3+9952t^2
                +18272sqrt(2)t+14844.

Both expressions are positive for t>=0. For -1<=t<=0 use sqrt(2)<17/12,
noting the negative odd powers, to obtain 3072 R_s(t)>B(t), where

    B(t)=19143t^4+12308t^3+29856t^2+77656t+44532.

The entries below are 48 times the five degree-four Bernstein coefficients
after linearly mapping the displayed interval to [0,1]. All are positive:

| Polynomial | Interval | Scaled Bernstein coefficients |
|---|---|---|
| A | [-1,-1/2] | 55728, 29016, 33852, 55494, 88743 |
| A | [-1/2,0] | 88743, 121992, 166848, 218112, 280128 |
| B | [-1,-1/2] | 171216, 40992, 126348, 330888, 615645 |
| B | [-1/2,0] | 615645, 900402, 1265376, 1671600, 2137536 |

Bernstein basis functions are nonnegative and sum to one, so this proves
P_s(t)>19/200 for every phase at m=4,5. Together with (7), (11), (12), and
the identity bound for m<=3, it proves the global minimum claim.

## Explicit lower bound and reusable scope

For m=6 the two one-zero Pauli families alone give, by convexity in z,

    Pi >= 1/64 +(126/64)*[(1/2+s*t)/(1+s*t)]^4
        >= 1/64 +(126/64)*(3/7)^4
         = 1801/21952 > 1/16,

because the displayed ratio is positive and increasing in t on [-1,1].
All other pair types have the stronger lower bounds just proved. This proves
(1) without needing to evaluate the algebraic minimum numerically.

Tensoring the minimizing state strengthens the necessary exponent in any
uniform c*k^-C conjecture to C>=-log_2(Pi_min), as rank is at most 2^r and
purity is Pi_min^r. It gives a fixed exponent restriction, not a refutation
of all polynomial bounds. In particular neither this tensor construction
nor any other rank-two pair falsifies exponent four. The reusable ingredients
are the exact Pauli-support counting in (5),(6) and the coefficient-imbalance
convexity; they do not supply an analogous cancellation inequality for k>2.

## 2026-11-13 Addendum: shorter proof of the exponent-four gate

The global phase minimization and the m=4,5 certificates above are NOT needed
to prove Pi>1/16. Here is a separate short proof from the exact Pauli counts.
The pair normal forms and the orthogonal-pair calculation (6),(7) still apply;
orthogonal pairs have Pi>=1/8, as do nonorthogonal pairs with m<=3.

For m>=4 put s=2^(-m/2)<=1/4. Keep only the identity and the two one-zero
Pauli families. Convexity of the fourth power in the coefficient imbalance z
gives

    Pi >= s^2+2(1-s^2)*[(1/2+s*t)/(1+s*t)]^4.

On -1<=t<=1 the ratio is positive and has derivative
s/[2(1+s*t)^2]>=0. Therefore

    Pi >= L(s):=s^2+2(1-s^2)*[(1/2-s)/(1-s)]^4.

Exact polynomial division gives

    L(s)-1/16 = Q(s)/[16(1-s)^3],
    Q(s)=1-11s+45s^2-63s^3+16s^4+16s^5.

Under s=x/4, Q has degree-five Bernstein coefficients on 0<=x<=1

    [1, 9/20, 29/160, 61/640, 17/160, 5/32].

These coefficients and the rational identity were independently verified by
exact symbolic arithmetic. Every coefficient is positive, so Q(s)>0 throughout
0<=s<=1/4. More explicitly Q(s)>=61/640 and 16(1-s)^3<=16 give the uniform bound

    Pi >= 1/16+61/10240 = 701/10240 > 1/16.

This weaker numerical constant already settles the requested rank-two C4 gate
without optimizing the phase, separating discrete overlap sizes, or evaluating
the algebraic minimum. The stronger bound and exact minimum above are optional
refinements, not premises of that decision.
