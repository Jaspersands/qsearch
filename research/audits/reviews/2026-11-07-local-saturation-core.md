# Local halving saturation: formal rank and abstract group audit

2026-11-07. CLOSED component review. The formal-seed determinant and abstract
one-half saturation argument are accepted with the precise conventions below.
This does **not** establish a polynomial-BIT algorithm for the complete local
Kummer image. Uniform index and stable finite-precision implementation remain
separate gates. No finite controls were run for this review.

Read: current STATE/TRAPS, LOCAL_HALVING_SATURATION.md,
WILD_LOCAL_SELMER_ADMISSION.md, and actual Stoll Section 3 formal-log statements
and Section 5 Proposition 5.1, its proof and its p-adic warning in
`audits/sources/local_halving_saturation/stoll.txt`.

## 1. Native input and the integral guard

Take monic squarefree f in Z_2[x], degree 2g+1, g>=1. This includes the
candidate's native monic integer input, without good-reduction assumptions.
The uniform choice N>=2 below is not justified for arbitrary nonintegral monic
Q_2 coefficients. Such an input must first be rescaled or use a
coefficient-dependent N. For example, with d=2g+1 the substitution
x=2^(-2h)X, y=2^(-dh)Y gives the monic integral polynomial
2^(2dh)f(2^(-2h)X) once 2h(d-i)+v_2(a_i)>=0 for every lower coefficient a_i.
For rational expanded coefficients, an adequate h has polynomial bit size.
The genus-zero Jacobian is trivial and can be handled separately.

Write F(z)=z^(2g+1)f(1/z)=1+a_1 z+...+a_(2g+1)z^(2g+1).
For t in 4 Z_2, F(t^2) belongs to 1+16 Z_2 and has its distinguished square
root congruent to 1 modulo 8. Hence

    P(t)=(t^(-2), t^(-(2g+1))*sqrt(F(t^2)))

is an actual rational point. No supplied local point is needed.

## 2. Exact determinant, for every genus

Put F(t^2)^(-1/2)=sum_(m>=0) c_m t^(2m). Then c_0=1 and
v_2(c_m)>=-2m. Indeed the binomial coefficient at order j is
(-1)^j binom(2j,j)/4^j, and only j<=m contributes to the coefficient at
t^(2m); the coefficients of F are integral.

For omega_k=x^(g-1-k) dx/(2y), 0<=k<g, pullback to this disk gives

    omega_k = -t^(2k) F(t^2)^(-1/2) dt,
    ell_k(t) = -sum_(m>=0) c_m t^(2(k+m)+1)/(2(k+m)+1).

All displayed integration denominators are odd. Set t_i=2^N i for
1<=i<=g, N>=2, and M_(k,i)=ell_k(t_i). Cauchy--Binet expands det M over
strictly increasing indices l_0<...<l_(g-1), using the two matrices

    A_(k,l)=c_(l-k)/(2l+1) for l>=k, and 0 otherwise,
    V_(l,i)=t_i^(2l+1).

Let Delta=sum_j l_j-g(g-1)/2. It is nonnegative. Every nonzero term of
the A-minor has valuation at least -2 Delta. For l_j=j the minor is
triangular with diagonal 1/(2j+1), hence is a 2-adic unit. The alternant
identity gives

    det(t_i^(2l_j+1))
      = (product_i t_i) product_(i<j)(t_j^2-t_i^2)
        * s_lambda(t_1^2,...,t_g^2),

where s_lambda is an integral Schur polynomial homogeneous of degree Delta.
After substitution t_i=2^N i, its valuation is at least 2N Delta.
Consequently, after factoring out the leading term, every nonleading
summand has valuation at least 2(N-1)Delta>=2. This also justifies the
infinite Cauchy--Binet limit: finitely many partitions occur at each Delta,
and these valuation lower bounds tend to infinity.

It follows that

    det M = (-1)^g
      (product_i t_i) product_(i<j)(t_j^2-t_i^2)
      / product_(k=0)^(g-1)(2k+1) * (1+4 Z_2).

In particular the proposed equality is exact:

    D0 := v_2(det M)
        = N g^2 + sum_i v_2(i) + sum_(i<j) v_2(j^2-i^2).

This is nonzero determinant for all g, with
D0=O(N g^2+g^2 log(g+1)). It is not by itself an index bound relative to
the full local Jacobian's integral differential lattice.

The antiderivatives here are the coordinates of the intrinsic abelian
logarithm, not a newly supplied logarithm oracle. Near infinity the integral
chart u=1/x, w=y/x^(g+1) satisfies

    w^2=u(1+a_1 u+...+a_(2g+1)u^(2g+1)).

It is smooth at (u,w)=(0,0), and w is an integral local parameter. Its
Abel--Jacobi morphism extends to the Neron model on this smooth
neighborhood. Since w(P(t))=t sqrt(F(t^2)) is in 4 Z_2, the point
[P(t)-infinity] belongs to K2, the Neron kernel modulo 4. The formal
logarithm identifies K2 with 4 Z_2^g in a Neron differential basis; this is
the m>e/(p-1) range explicitly stated in Stoll Section 3. Pullback of the
invariant differentials gives precisely the antiderivatives above. Thus
the g seed classes have independent Q_2 logarithms. This argument uses
the Neron model for a proof, and does not construct it or charge its
coordinates as free computational input.

## 3. Rational 2-torsion and the correct subgroup convention

If f has r irreducible factors over Q_p, then
dim_F2 J(Q_p)[2]=t=r-1. The factor divisors
sum_(f_i(alpha)=0)(alpha,0)-deg(f_i)*infinity give all these classes,
with their one total-sum relation. Because deg f is odd, the usual
branch-divisor augmentation quotient has an equivariant splitting; no
extra invariant classes are lost by using the local factors. These
divisors can be reduced, or complemented, to degree at most g.
Computing certified finite local factors remains a computational task.

Let G=J(Q_p), and let G_(2) be its maximal pro-2 subgroup. For p=2 it is
isomorphic to Z_2^g plus a finite 2-group. For odd p it is the finite
2-primary torsion subgroup. In both cases

    G_(2)/2G_(2) -> G/2G

is an isomorphism. Its dimension is g+t at 2 and t at odd p.

Maintain actual points generating an abstract finitely generated group H,
with a free basis and the complete finite 2-primary torsion presentation.
At p=2 start with the g formal seeds and all G[2]; at odd p start with
all G[2] and no free generators. Write Hbar for its closure. At 2 the
independent logarithms give

    H = Z^g plus T_H,    Hbar = Z_2^g plus T_H,
    H/2H = Hbar/2Hbar.

One cannot instead call the abstract Z-span a finite-index subgroup of
the uncountable group G. The finite-index argument belongs to Hbar.
The displayed description follows from the continuous Z_2-exponent map
on G_(2): logarithmic independence makes its free-coordinate map
injective, so closure introduces no additional torsion. Initially Hbar
is open in G_(2). At odd p H is already finite and closed.

## 4. One half is enough, and each step really has index two

At every stage T_H[2]=G[2], since all rational 2-torsion was seeded and
retained. Thus dim H/2H remains g+t at 2, or t at odd p. Compute the
linear Kummer-label map on this basis. If its rank is below that target,
choose a nonzero class h in its kernel. Since ker(delta)=2G, a rational
Q with 2Q=h exists.

Then Q is not in H, because h is not in 2H, and
H'=H+Z Q has [H':H]=2. Every rational half differs from Q by an element
of G[2] already in H; hence all choices give the same H'. There is no
need to enumerate the 2^t different halves. Also Q lies in G_(2):
multiplication by 2 is invertible on the complementary prime-to-2
quotient. The identity H intersect 2Hbar=2H shows Q is not in Hbar, so
[Hbar':Hbar]=2 as well.

The maintained presentation can be updated without an unknown relation
oracle. Choose the representative h with free coefficients 0 or 1.
If any free coefficient is 1, replace that free generator by Q; the old
generator equals twice Q minus the other free terms and the torsion
term. The logarithm determinant is divided by 2, and the old finite
torsion subgroup is unchanged. If h is pure torsion, Q is torsion;
adjoin Q with the relation 2Q=h and use integer Smith normal form on
the finite presentation. The fact Q is not in H proves this presentation
is exact. This preserves the free/finite decomposition and the closure
description. Keeping only a redundant list of points and its label
kernel would be insufficient: an internal generator relation need not
produce strict enlargement.

Each step halves the finite index [G_(2):Hbar], so the process terminates
abstractly. A nontrivial remaining finite 2-group quotient has nonzero
2-torsion. The multiplication-by-2 exact sequence, together with
G_(2)[2] contained in Hbar, injects this quotient's 2-torsion into the
kernel of Hbar/2Hbar -> G_(2)/2G_(2). Thus the stated rank stopping rule
is equivalent to Hbar=G_(2), and returns the complete local image.
This is a finite-termination theorem, not a polynomial iteration theorem.

## 5. Exact symbolic index ledger

Let eta=R omega be a Neron invariant differential basis at 2, and let L
be the closed span of the free seeds. Then L is contained in K2,
log_eta(K2)=4 Z_2^g, and

    log_2[K2:L] = D0+v_2(det R)-2g.

K2 is torsion-free, so for the initial Hbar0=L+G[2] one has
[Hbar0:L]=2^t. Consequently the exact number of successful index-two
enlargements is

    kappa = v_2 |G/K2| + D0+v_2(det R)-2g-t.

This identity already includes all finite 2-primary torsion; no extra
torsion-exponent parameter is needed. The connected special fiber has
size at most 2^(3g): its unipotent, toric and abelian factors contribute
2^u, at most 3^b, and at most (1+sqrt(2))^(2a)<8^a, with a+b+u=g.
Since |K1/K2|=2^g,

    v_2 |G/K2| <= v_2 |Phi(F_2)| + 4g,
    kappa <= v_2 |Phi(F_2)| + D0+v_2(det R)+2g-t.

At odd p the analogous exact starting index is
v_2 |J(Q_p)[2^infinity]|-t. It is at most
v_2 |Phi(F_p)|+O(g log p)-t, because the pro-p kernel contributes no
2-part and the connected special fiber has size at most (4p)^g.

These are accounting identities and inequalities. The native bounds on
the positive differential correction and component-group 2-part are
not proved by this review. Neither R nor Phi is supplied as advice.

## 6. What the actual halving source pays, and what remains open

Stoll Proposition 5.1 pays one half over an exact characteristic-not-2
field once a square root of the Kummer representative in k[x]/f is
known. It handles a common factor of the Mumford polynomial and f.
Repeated factors of the Mumford polynomial can first be extracted as
the explicitly divisible summand described immediately before the
proposition. Its congruences are linear in O(g) coefficients; the least
degree monic w can be found by at most g+1 such linear systems, followed
by polynomial gcd/CRT. This is a classical algebraic operation and
does not require enumeration of all square-root signs.

The source explicitly warns that p-adic precision can fail near branch
points, lower-degree output divisors and infinity. Its suggested changes
of representation, practical rarity and possible Laurent-series route
do not give a uniform BIT bound. In particular this review does not
establish:

* a polynomial bound for kappa in the native coefficient bits and genus;
* stable finite-precision factoring, Kummer coordinates, square roots,
  point addition, degree/rank decisions and minimal-w halving throughout
  all saturation steps;
* a certified polynomial precision schedule that handles the source's
  exceptional divisor charts without an uncharged genericity promise.

Replacing these p-adic points by successively larger exact global
algebraic-number fields does not close the last gates: repeated halves
can increase global representation degree. No such expansion is included
in the native resource claim. The accepted formal/group components
therefore support the proposed route but do not yet remove the full
wild-local-image blocker or establish a quantum speedup.
