# Quaternion Splitting Leaves An Integral Hermitian Equation

Date: 2026-10-30. Status: exact algebraic reduction and bounded controls;
not a new quantum solver or a hardness theorem. This identifies the
integral descent obligation behind the compact-orbit research direction.

## Natural-Order Contract

Let L/F be a CM quadratic extension, R=O_L, and
`B=L+jL`, with `j^2=-1` and `ja=conjugate(a)j`. Use RIGHT L-coordinates
`x=a+jb`, and the natural order O_0=R+jR. Then

```text
rho(a+jb) = [[a,-bar(b)],[b,bar(a)]],
S = [[0,-1],[1,0]],       J(v)=S*bar(v),
rho(B) = {A : A*S=S*bar(A)},
rho(x)^* rho(x)=nrd(x)*I_2,    det(rho(x))=nrd(x).
```

Here rho is LEFT multiplication and J is RIGHT multiplication by j.
Splitting `B tensor_F L = M_2(L)` is rational algebra, not an assertion
that every integral order becomes M_2(R).

A locally principal RIGHT O_0-ideal I is a J-stable rank-two R-module
Lambda. If nrd(I)=q O_F, its determinant ideal is qR, so its Steinitz
class is trivial: Lambda is free even when I is not quaternion-principal.
Choose a basis P with det(P)=q. Supplying q removes an unknown determinant
generator; module/basis computation still has to be charged.

Set `H=P^*P` and `D=P^-1*S*bar(P)`. Direct calculation gives

```text
D*bar(D)=-I_2,     D^*H D=bar(H),     det(H)=q^2.
```

The exact residual task is

```text
U in SL_2(R), D*bar(U)=U*S
    iff U in SL_2(R), U^*H U=q*I_2.
```

Indeed PU then has quaternionic shape and determinant q. Conversely,
a scaled-unitary 2x2 matrix with determinant q has that shape. For one
column u in R^2, take `U=[u,D*bar(u)]`: its determinant is `u^*Hu/q`.
Therefore the missing operation is precisely finding `u^*Hu=q` over
INTEGRAL coordinates. A rational solution or an ordinary field ideal
generator does not supply this unimodular frame. Ordinary Hilbert 90
also cannot be quoted with `D*bar(D)=-I` as though it were +I.

## Exact Countercontrol

Take F=Q, L=Q(sqrt(-11)), `w=(1+sqrt(-11))/2`, so `w^2=w-3` and
`w*bar(w)=3`. The field ring R=Z[w] has class number one: Minkowski's
bound is below 3 and the only prime to check, 2, is inert. Nevertheless,
the right O_0-ideal

```text
I={a+jb : b=w*a mod 2R},
P=[[1,0],[w,2]],       q=2,
H=[[4,2*bar(w)],[2*w,4]],
D=[[-bar(w),-2],[2,w]]
```

has no norm-2 element. It is R-stable, and J-stability follows from
`1+w*bar(w)=4=0 mod 2`. Its index in O_0 is 4. All norms are even;
`1+jw` and `w+j(w-1)` have norms 4 and 6, so its norm ideal is 2Z.

The ideal is locally principal: away from 2 its index is a unit; at 2,
the norm-6 element's principal ideal is contained in I and has the same
local index 4. A norm-2 element would require a sum of two values

```text
N(a+c*w)=(a+c/2)^2+(11/4)c^2
```

to equal 2. Both w coefficients must vanish. The only remaining candidates
have entries +/-1, contradicting `b=w*a mod 2R`. Thus H/2 is positive,
unimodular and has minimum 2, not 1; it is not integrally isometric to I_2.

Rational descent still exists:

```text
U_Q=P^-1*rho(1+j)
   =[[1,-1],[(1-w)/2,(1+w)/2]].
```

It has determinant one and satisfies the two displayed descent equations,
but is not integral. This falsifies field principalization PLUS rational
descent implying an integral generator. It says nothing about the hardness
of promised-YES instances, and this rational rank-four control is itself
classically easy.

## A Genuine Easy Special Case

If the public module actually decomposes orthogonally as
`Lambda=a ideal direct_sum bar(a ideal)`, with `a*bar(a)=qR`, the rank-one
polarized ideal problem applies. [Lenstra--Silverberg, Theorem 1.3](https://arxiv.org/pdf/1706.07373)
finds t with `a=tR` and `t*bar(t)=q`, or certifies no such t, in classical
polynomial time in its stated explicit CM input model. Then t is a
quaternion generator.

This is complete for this decomposed regime: if both coordinates of a
norm-q vector were nonzero, their norm ratios would be totally positive
algebraic integers summing to 1. Their traces would each be at least d,
a contradiction. The extra promise is an INTEGRAL orthogonal decomposition,
not just a free module basis or a rational diagonalization of H.

## General Orders And Remaining Work

For an order containing R, retain its actual Steinitz module and Hermitian
form, not R^2 by fiat. If I is locally principal over O, left multiplication
by a local generator is right-L-linear with determinant its reduced norm.
Comparison at every finite prime gives
`det_R(I)=nrd(I)*R*det_R(O)`. With nrd(I)=q O_F the two Steinitz CLASSES
therefore agree. This still requires explicit module isomorphisms to a
common coefficient module E; it is not equality of the given modules or
a free basis algorithm. With correctly matched module data the equations
become `D*bar(U)=U*D_0` and `U^*H U=q*H_0`, with U an integral module
automorphism. The determinant-ideal comparison and normalization must be
proved for that input. If R is not contained in O, check R-stability first;
saturating an ideal changes its membership problem.

Completing the square does not separate the general search. For
`H=[[h,c],[bar(c),k]]`, det(H)=q^2, the first-column equation implies

```text
N(h*s+c*t)+q^2*N(t)=h*q,
h*s+c*t = c*t mod hR.
```

A field norm solver at a fixed right-hand side neither chooses t nor
enforces the coupled congruence. The matched general baseline remains
weighted SVP in dimension 4d, already used by
[Kirschmer--Voight, Algorithm 6.3](https://jvoight.github.io/articles/quatideal-fixed-errata-111614.pdf).
The full Hawk paper's Definition 2.18 and Section 4.1 use this norm-exact,
rank-two geometry. No arbitrary-degree field-PIP barrier is reinstated.

Next work must solve the integral equation or exploit the compact quantum
source without assuming its answer. Tests in
`tests/test_quaternion_integral_descent.py` check only explicit identities
and matched finite examples, not an algorithm for growing-degree descent.
