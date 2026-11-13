# Joint norms: coprime-degree reduction and enlarged normal-field support

Independent audit, 2026-11-13. Scope: explicit number fields and embeddings,
nonzero targets, compact power-product outputs. No network, API, Git, or
finite control was used. These are elementary reductions, not novelty claims.

## 1. Two scalar calls suffice in coprime degrees

Let A,B be linearly disjoint over Q, L=A tensor_Q B a field,
d=[A:Q], e=[B:Q], and gcd(d,e)=1. Then [L:A]=e and [L:B]=d.
For a in A*, b in B*, a joint solution exists if and only if

1. N_(A/Q)(a)=N_(B/Q)(b);
2. each of N_(L/A)(y)=a and N_(L/B)(w)=b is individually soluble.

Necessity is transitivity. For sufficiency choose such y,w and put

    v=w/y,  c=N_(L/B)(v),  gamma=N_(L/A)(v).

Compatibility gives N_(B/Q)(c)=N_(A/Q)(gamma)=N_(L/Q)(v)=1.
The tensor-product hypothesis supplies the exact base-change identities

    N_(L/A)(c)=N_(B/Q)(c)=1,
    N_(L/B)(gamma)=N_(A/Q)(gamma)=1.

Also N_(L/A)(gamma)=gamma^e and N_(L/B)(c)=c^d. Consequently

    q=v^e/gamma
    N_(L/A)(q)=1,             N_(L/B)(q)=c^e.

Choose integers u,t with ud+te=1. Then

    x=y*c^u*q^t
    N_(L/A)(x)=a,
    N_(L/B)(x)=N_(L/B)(y)*c^(ud+te)=b.

There is no additional norm call on c, gamma, or a compact target.
For d=1 return x=b directly; compatibility is precisely its other norm
condition. For e=1 return x=a. This includes d=e=1, when a=b.

**BIT and oracle interface.** First compute compatibility on the original
expanded inputs by exact determinants. Then call the existing scalar
relative-norm backend on the two original expanded targets. A certified NO
from either call settles the joint problem. Otherwise use the displayed
formula. This is polynomial classical postprocessing of two scalar calls;
it inherits their hypotheses, access model, and classical/quantum costs.
It does not turn a quantum or conditional backend into a classical theorem.

Write scalar outputs as products of polynomially many expanded nonzero
L-atoms with binary exponents. Form v by concatenation and sign changes.
For each atom compute its two relative norms by multiplication-matrix
determinants over A and B; the required relative bases and conversions are
ordinary exact rational linear algebra on the supplied field tables.
Determinant degree and coefficient-height bounds are polynomial in this
expanded input. Embed the resulting norm atoms back into L, retaining the
original exponents. Thus c,gamma,q,x stay compact throughout. Extended
Euclid gives |u|<=e, |t|<=d when d,e>1; exponent lengths increase by only
O(log(de)) beyond sums of the original lengths. No power product is expanded.
Allocate failure probability eta/2 to each scalar call; their union bound
is eta without independence. The reduction adds no probabilistic step.

## 2. Enlarged support for a normal field

Let L/Q be Galois of degree N with group G, and let A,B be subfields.
Put H_A=Gal(L/A), H_B=Gal(L/B). For every cyclic subgroup D<=G set F_D=L^D.
Take a finite rational-prime set S containing all primes ramified in L,
the full prime-ideal support of a and b, and rational primes below a
class-generating set for EVERY F_D. Then every soluble joint norm equation
has an S-unit solution with the same two exact targets.

Here and below S-support in a field includes every place over a prime in S.
Fix p outside S and a prime P0 of L above p. Its decomposition group D is
cyclic because p is unramified. For F=L^D and q=P0 intersect F, the extension
L/F is Galois with group D and its decomposition group at P0 is all of D.
Thus q has a unique prime P0 above it, with e(P0/q)=1 and f(P0/q)=|D|.
Since f(P0/p)=|D|, f(q/p)=1 and, crucially,

    q O_L=P0.

Class generation in F gives beta in F* with div_F(beta)=q+E_S for an
S-supported fractional divisor E_S. Hence div_L(beta)=P0+an S-divisor.
Moreover beta is fixed by D. Primes above p are G/D, and this defines
an EXACT multiplicative G-equivariant map

    Phi: Z[G/D] -> L*,
    Phi(sum z_(gD)[gD])=product_(gD) (g beta)^z_(gD).

Fixedness by D makes it well-defined. Its outside-S divisor is precisely
the supplied vector above p, and is zero above every other outside-S prime.
No choice of conjugate generators introduces units or roots of unity.

Let x0 be any joint solution and z_p its integral valuation vector above p.
As the targets are S-units, exact Galois norm identities imply

    T_(H_A) z_p=0,  T_(H_B) z_p=0,  where T_H=sum_(h in H) h.

These equations include the local norm multiplicities: on an H-orbit each
coordinate of T_H z is |Stab_H(P)| times the sum of the orbit coordinates.
Here |Stab_H(P)| is the residue degree of L/L^H at P, since p is unramified.
They follow equally by taking div_L of N_(L/L^H)(x0)=product_h h(x0).
Equivariance now gives, as ELEMENT equalities,

    N_(L/A)(Phi(z_p))=Phi(T_(H_A)z_p)=1,
    N_(L/B)(Phi(z_p))=Phi(T_(H_B)z_p)=1.

Divide x0 by the product of these corrections over its finitely many
outside-S support primes. The result is an S-unit and has unchanged norms.
This is an existence proof: neither x0 nor these principalizations are
supplied to the eventual algorithm. It lifts the entire integral joint
kernel, rather than just the rectangle-transfer sublattice.

**Size and hypotheses.** There are at most N cyclic subgroups and their
fixed fields have total degree at most N^2. The discriminant tower formula
gives log|disc(F_D)|<=log|disc(L)|. Under the already charged GRH
class-generator bound for these fixed fields, one may conservatively take

    B0=48*max(1,2N*bit_length(|disc(L)|))^2

as in RELATIVE_NORM_TENSOR_SUPPORT.md, and include every rational prime
<=B0. Thus constructing this enlarged support needs no Galois-group list,
fixed-field construction, class-group computation, or normal-closure advice.
Normality of the supplied L remains a promise; GRH must cover the fields
whose class-generation bound is used. Prime enumeration has polynomial
cost because B0 is a numerical polynomial in the explicit input.

For target support choose an integer m>0 with ma integral and include primes
dividing m and |N_(A/Q)(ma)|; do likewise for b. This covers zeros AND poles.
Using N_(A/Q)(a) alone would miss cancellations between primes over the same
rational prime. These and the discriminant are polynomial-bit integers;
integer factoring is charged to the existing backend, not treated as a free
classical polynomial operation. All proof objects beta may remain unknown.

**Disposition.** Both reductions are sound in the stated scopes. Section 2
does NOT prove Magma's narrower assertion using arbitrary class generators
of L alone: generators of cyclic fixed fields are the additional argument.
Neither section closes the general noncoprime, nonnormal joint-norm problem
or establishes hardness. A downstream complete S-unit/relation compiler
must retain its separately charged hypotheses and finite-bit output costs.
