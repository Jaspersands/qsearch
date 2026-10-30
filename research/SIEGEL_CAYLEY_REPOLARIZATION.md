# Genus-Two Repolarization Through An Explicit Polarized Quotient

30 October 2026. A constructive mathematical deduction, independently
checked by an automated reviewer. NOT a uniform efficient geometric
converter, implemented quantum source, novelty certificate or speedup.
Exact controls: `tests/test_siegel_cayley_repolarization.py`.

## 1. Preserve The Original Weak Input

Use exactly `SIEGEL_ELEMENTARY_REPOLARIZATION.md`: A=E^2 with a known,
evaluable source quaternion order O, original encoded principally polarized
(B,lambda_B), and a weak ell-polarized isogeny phi:A->B. Here ell and
the characteristic p are distinct odd primes. On a full auxiliary torsion
basis P_R the weak evaluator supplies Q_R=a_R phi(P_R), with ONE unknown
unit a_R common to that basis. All torsion fields, pairings, coordinate
recovery and model operations are charged. No full End(B)/Hom(A,B) lattice
or geometric ell-torsion is added.

For a known degree-one lift sigma of M in Sp_4(F_ell), with known inverse,

    S = sigma^dagger sigma = I+ell T,
    psi = phi sigma^-1,
    H = phi S phi^-1 = I+phi T phi^dagger.

The previous proof gives an integral positive unit H, a principal
polarization lambda_B H, and psi^dagger H psi=[ell]. The dagger uses the
ORIGINAL polarizations. H is known on accessible torsion, not supplied as
a geometric rational-map formula or a complete target order.

The older direct stabilization has the wrong polarization. The construction
below uses a DIFFERENT map and does not contradict that obstruction.

## 2. The Plus Construction

Write S=[[a,b],[b^dagger,d]], where a,d are positive integers and
ad-Nrd(b)=1. Its Moore determinant is one because sigma is a degree-one
automorphism. Put t=a+d. Direct quaternion multiplication gives

    S^2-tS+I=0,       H^2-tH+I=0,       H+H^-1=tI.

Rational conjugacy transfers the identity to H; no presentation of
End(B) as standard quaternion matrices is assumed. Define

    N=t+2,       eta=H+I,       mu=I+H^-1=H^-1 eta.

These are integral, with

    eta^2=NH,       eta mu=mu eta=[N],       mu^dagger H mu=[N].

Assume p does not divide N. Then mu is an N-polarized separable isogeny
from the ORIGINAL (B,lambda_B) to B_H=(B,lambda_B H), of geometric degree
N^2. Its kernel satisfies

    K_N=ker(mu)=ker(eta)=eta(B[N]).

Proof of the last equality: mu eta=[N] puts the image in ker(mu).
Also deg(eta)=N^2 by eta^2=NH and deg(H)=1. Both kernels have N^2
geometric points inside B[N], so the image has N^4/N^2=N^2 points.
The identity mu^*lambda_H=N lambda_B makes K_N maximal isotropic for the
ORIGINAL N-Weil pairing. Polarization descent is the standard theorem,
e.g. [Moonen, Proposition 11.25](https://www.math.ru.nl/~bmoonen/BookAV/PolWp.pdf).

If a charged geometric quotient algorithm constructs

    q_geom:(B,lambda_B)->(C,lambda_C)=B/K_N,
    q_geom^*lambda_C=N lambda_B,

then there is a unique polarized isomorphism u:B_H->C with

    q_geom=u mu,       q_geom eta=u[N].

This is quotient uniqueness and equality of pullback polarizations, not
an assumed algorithm for finding a target End/Hom lattice. It supplies
the desired changed polarized MODEL via a quotient of the original model.

### Why This Is Genus Two

The scalar identity H+H^-1=tI is essential. A general higher-dimensional
positive determinant-one H does not satisfy it. The tests include a
three-dimensional counterexample. No general-g converter follows.

### Why Use Plus, Not Minus

Since S=I+ell T, its determinant-one identity gives

    t-2=-ell^2 det_M(T),       N=t+2=4 mod ell^2.

Thus N is automatically coprime to odd ell. The analogous minus
multiplier t-2 contains ell and is unsuitable for the original access
model. N=4 forces H=I by positivity; that case needs no repolarization.

## 3. Kernel And Marks Without Synchronizing Weak Signs

For each full primary order R=s^e exactly dividing N, supply the accessible
source basis P_R and its weak image Q_R. Then

    K_R = image(Q_R (S_R+I)).

Indeed phi(S+I)=(H+I)phi, and phi is invertible on R-torsion because
gcd(R,ell)=1. The common unit a_R changes generators, NOT this subgroup.
No pairing normalization or cross-prime choice of signs is required.
If access is only promised at prime orders, the higher-primary basis and
evaluation is an additional charged requirement, not an implicit grant.

For a FIXED marking order r coprime to N, the desired marked image is

    u psi(P_r)
      = q_geom(phi([N^-1 mod r](S+I)sigma^-1 P_r)).

Known source matrix action and linear combinations of the existing weak
image basis produce this tuple up to the SAME common unit a_r. The source
operator (S+I)sigma^-1=sigma^dagger+sigma^-1 has adjoint product [N], so
it is invertible on this marking torsion. The formula requires no
arbitrary-point division by N, no sqrt(N), and no recovery of a_r.

For r sharing factors with N, one can instead choose [N]Q=P and use
u(P)=q_geom eta(Q). This is independent of the division choice because
eta(B[N])=K_N, but computing Q may require larger primary torsion.
Do NOT count this as free. Section 4 avoids overlap for fixed odd marks.

The quotient kernel need not be free over Z/N. A real integral fixture is

    ell=5, phi=[[1,2],[-2,1]], sigma=[[1,10],[0,1]],
    H=[[89,34],[34,13]], N=104,
    U=[[5,2],[8,3]], q=[[2,10],[10,-2]],
    U^T U=H, q^T q=104 I, q(H+I)=104 U.

The Smith invariants of H+I on the two real factor coordinates are 2,52.
Its 2-primary geometric kernel has type (Z/2)^2 x (Z/4)^2, NOT (Z/8)^2.
A backend limited to free full-level kernels cannot silently accept it.
These matrices act on E^2 in characteristic 11; the tests verify exact
arithmetic and pairing coordinates, not an emitted geometric quotient.

## 4. A Constructive Fixed-Mark Avoidance Lemma

Choose fixed ODD marking primes before evaluating M, as required by the
joint marked rigidity theorem. For a known q in O, change the lift by

    C(q)=I+ell E_12(q),       sigma'=sigma C(q).

C(q) is a degree-one unit with explicit inverse and C(q)=I mod ell.
With S'=C^dagger S C and N(q)=tr_diag(S')+2, exact multiplication gives

    N(q)=t+2+ell Trd(q^dagger b)+a ell^2 Nrd(q),
    a N(q)=Nrd(a ell q+b)+(a+1)^2.

The conjugate orientation matters. For ell=5,a=1,b=5i,d=26,q=i the
correct N is 104; using Trd(qb) would incorrectly return 4.

For each odd r dividing p*M_marks, with r!=ell:

- If a!=0 mod r, take q=z*1. The polynomial in z has nonzero quadratic
  coefficient a ell^2, so one of z=0,1,2 gives N(q)!=0 mod r.
- If a=0 mod r, Nrd(b)=-1 mod r. Take q=zb; the polynomial is
  t+2-2ell z mod r, so one of z=0,1 works.

Coordinatewise CRT in the known integral O-basis gives q_0 satisfying
all these choices. Every q in q_0+R O, R=rad(p*M_marks), retains

    gcd(N(q),p*M_marks*ell)=1.

This uses only arithmetic modulo p, NOT p-torsion. Representatives have
polynomial bit length in the charged source data and marking product.
It does not give powersmooth N or a polynomial torsion-field degree.

The change preserves the whole jointly marked polarized class. In fact

    v=phi C^-1 phi^-1=I-phi E_12(q) phi^dagger

is an integral automorphism, with the plus-sign expression as inverse.
Writing psi'=phi sigma'^-1 and H'=phi S'phi^-1 gives

    v psi=psi',       v^dagger H'v=H.

Use the UPDATED S', sigma', H', N in every quotient/mark formula. This
permits optimizing the lift without changing the queried kernel class.
It does not permit independently canonicalizing individual marking levels.

## 5. The Remaining Arithmetic Problem Is Now Explicit

After fixed-mark avoidance, the upper-shear route asks for

    Nrd(x)=aN-(a+1)^2,
    x in b+a ell q_0+a ell R O,

where N has an AFFORDABLE torsion and polarized-quotient cost, not merely
polynomial bit length. Also N >= (a+1)^2/a; this one-sided shear cannot
make the fixed first diagonal a disappear.

Known quaternion norm/ideal-smoothing work is relevant but not an imported
solution. [KLPT](https://arxiv.org/abs/1406.0981) smooths equivalent ideal
norms. [Wesolowski, Sections 5--6](https://arxiv.org/pdf/2111.01481) gives
GRH-conditional norm and powersmooth ideal algorithms. Neither checked
statement alone proves this shifted-norm affine-coset claim. Do not replace
the missing reduction by the phrase "use KLPT". Other lift choices or
multi-stage quotients may beat this sufficient construction.

The six EXISTING ell=61 quaternion lifts give the saved exact costs in
`classical_baselines/siegel_cayley_costs.json`. Their largest individual
primary full-torsion extension degrees over F_121 are, respectively,

    311617275, 67384820994048292, 311617275,
    67384820994048292, 16337508, 430718.

Here E:y^2=x^3-x has Frobenius [-11] over F_121, and the full s^e torsion
requires extension degree ord_(s^e)(-11). Replay checks the point count,
N factorizations and exact minimality of every recorded order without
constructing those fields. These rule out cheap full-torsion evaluation
for those particular lifts, NOT all quotient representations or all lifts.

Even a fixed small prime is insufficient. N=4 mod 61^2 and
ord_(61^2)(2)=3660 force a pure 2-power N=2^e to have e=2 mod 3660.
Outside H=I this requires e>=3662; all six upper-shear fixtures have a>1.
Full 2^e torsion then requires degree 2^(e-2)>=2^3660 over F_121.
Here v_2((-11)^(2^k)-1)=k+2 for k>=0, giving that exact order for e>=2.
Any explicit generating set for a kernel of order 2^(2e) in rank-four
torsion contains a point of order >=2^ceil(e/2), requiring a field of
degree at least 2^1829. Implicit-kernel methods are not excluded.
Also ord_61(3)=10 and ord_61(4)=30, so N=3^e is impossible here.
Neither argument excludes mixed-prime smoothing.

## 6. Resource And Claim Gates

An efficient oracle still needs ALL of the following, uniformly over its
query domain:

1. A constructive lift/multiplier selector with a proved affordable bound.
   Factorization of N and any norm search are paid, not assumed free.
2. Required primary torsion and weak evaluations in charged fields, or a
   verified alternative compact-kernel interface. Higher prime powers
   cannot be obtained free from prime-only access.
3. A genuine polarized quotient implementation covering the produced
   kernel types, including nonfree/even-primary cases, and point transport.
   The [Lubicz--Robert algorithm](https://arxiv.org/abs/1402.3628) takes an
   encoded theta model and a kernel description; its degree-dependent cost
   is not polynomial in log(N) for unrestricted N.
4. Bounded model/field construction throughout the quotient chain. Working
   with separate torsion fields does not by itself bound model composita.
5. ONE geometric polarized isomorphism class for the entire weak marked
   tuple, fixed field embeddings, the existing rigidity bound, and a paid
   joint canonicalizer. Do not use per-level minima or Frobenius orbits.
6. A bounded coherent evaluation with clean discarded work and full error
   accounting. A classical formula does not by itself implement this.

Skipping expensive query-dependent multipliers and returning a common
ABORT label has no established coset-constancy/error guarantee. Finite
success or an affordable subfamily cannot replace a uniform oracle proof.

More precise checked operation contracts:

- [Lubicz--Robert, Fast change of level, Theorem 1.3 and Remark 4.6](https://antsmath.org/ANTSXV/papers/ANTS-XV_lubicz-robert.pdf):
  for odd prime s, a level-4 theta model and the required rational kernel
  data, quotient/evaluation costs O((4s)^g log s) field operations. At
  fixed g=2 this is O(s^2 log s), not polynomial in log s. The split-kernel
  hypothesis does not directly cover arbitrary nonfree composite kernels.
- [Dequay--Lubicz, Theorem 10, Corollary 14 and Algorithm 8](https://arxiv.org/pdf/2504.21058v2):
  the level-4 degree-2 step uses compatible auxiliary 8-torsion data; the
  quoted O(8^g) arithmetic excludes acquiring that data. Their working
  field convention includes the compositum of input-definition fields.
- A general N therefore needs an applicable, certified primary chain.
  Galois stability of K_N does not supply a controlled-field isotropic
  flag, all intermediate theta models, or descent algorithms for free.

Neither operation needs a target End/Hom lattice. That is useful, but
removing that requirement is not a proof of affordable weak-input access.
The separately rechecked 2026/1142 full PDF remained inaccessible via
ordinary public requests; accessible interpolation slides still start
with two already encoded PPAVs. No theorem-absence claim follows.

## 7. Next Decisive Work

First test the explicit constrained norm problem against algorithms with
matching hypotheses. A valid theorem must supply actual affordable N and
fields, preserve the original weak-input model, and work across the needed
query domain. Small sweeps can falsify a proposed selector but cannot
prove uniform efficiency. If no such route emerges, stop adding quotient
plumbing and compare another native application.

In parallel, apply `SIEGEL_REVERSE_TRANSPORT_ATTACK.md` whenever the
ORIGINAL target model exposes extra polarized automorphisms. That attack
uses the known SOURCE order and can recover easy kernels without a full
target lattice. Surviving that attack is not classical hardness. Even a
successful conversion here would use the known degree-two HPGP receiver,
not establish unique utility or novelty for the Rees theorem.
