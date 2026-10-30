# A Real Prime-Field Tower, Then A Persistent Classical Attack

## Decision

Do not promote this family as a quantum-speedup candidate. The source gap
has a concrete mathematical solution, but the resulting near-canonical
codes have a deterministic polynomial-time classical full-support solver.
The attack persists at unbounded genus and high rational gonality; it is
not just the earlier large-alphabet rejection-sampling control.

Status: written deductions plus exact finite-field controls. Independent
review accepted the scoped source and classical attack, with546 separately
checked native witnesses. See VERIFICATION.md for the review's limits.
No novelty, Shor-level result, quantum execution, uniform output sampler,
or dequantization of all AG codes is claimed. The source uses standard
class-field-tower theory, not a new tower construction method.

The problem remains the original one: given explicit full-row-rank B over
F_p and arbitrary s, find z with Bz=s and EVERY z_i nonzero. No oracle,
planted solution, altered syndrome, or partial-support output is substituted.

## 1. Explicit Source Certificate

Fix p=100003 and the smooth projective model of

    X0: y^2 = product_(a=0..12)(x-a).

The polynomial is squarefree, monic and odd degree13, so X0 has genus6
and one rational point at infinity. The following eleven distinct x values
have every x-a a nonzero square:

    18501,29631,37154,37155,40763,48611,
    48612,48613,48614,48615,51887.

The certificate contains all143 square roots and both y values for each x.
The splitting set S consists of these22 points plus infinity. A deterministic
consecutive-quadratic-residue scan finds them after51887 Legendre tests.
The scan is source discovery, not an algorithm benchmark or hardness test.

Let K=F_p(X0) and

    L=K(sqrt(x),sqrt(x-1),...,sqrt(x-12)).

Over F_p(x), the13 square classes x-a are independent by their valuations
at the13 distinct branch points. Passing to K kills exactly the class of
their full product. Indeed a base-field element square in a quadratic
extension is either a base square or the defining radicand times a square.
Consequently [L:K]=2^12 and the extension is elementary abelian.

Each div_K(x-a)=2P_a-2infinity. In odd characteristic its Kummer extension
is therefore unramified at every place. At infinity, taking the local
parameter t=y/x^7 gives (x-a)t^2 with residue1; each quadratic extension
splits there. At each selected finite point its radicand is a checked
nonzero square. Thus all23 places split in L/K. A split rational place
also excludes a constant-field extension.

Class-field theory gives d_2 Cl_S(K)>=12. Schoof's sufficient criterion is
d_2 Cl_S >= 2+2 sqrt(d_2 O_S^*+1). Here d_2 O_S^*=|S|=23, since the unit
rank is22 and F_p^* contributes one2-rank. Its integer check is

    (12-2)^2 - 4*(23+1) = 4 > 0.

Hence the S-split unramified2-class tower is infinite. This application uses
[Schoof, Theorem2.3](https://www.mat.uniroma2.it/~schoof/f2.pdf).
The general use of such towers for asymptotically many rational points is
established literature, also discussed in
[Elkies et al., Section3.2](https://arxiv.org/html/math/0208060).

This is an existence certificate with an explicit first elementary cover,
NOT an implemented efficient generator for all subsequent class fields.
Adding a twelfth x pair makes this particular sufficient GS test fail;
the code records absence of that certificate, not finiteness of the tower.

## 2. The Refined Quantum Window Is Genuinely Populated

Take an unramified cover pi:X->X0 of degree e in this tower. Intermediate
2-power degrees are available from finite2-group extensions. Requiring
that covers contain a specified intermediate cover is an explicit extra
condition used below, not something inferred just from their degree.

Write I=pi^*(infinity), let D be the sum of all lifts of the22 finite
splitting points, and choose R over infinity. Put G=10I+3R. Then

    g=5e+1, d=deg G=10e+3=2g+1, m=deg D=22e,
    k=ell(G)=5e+3, w=ell(2G)=15e+6.

For e>=4 evaluation is injective on L(2G), and standard AG multiplication
identifies V^2 with ev_D L(2G). The theorem used for multiplication is
[Couvreur et al., Theorem5 and Corollary6](https://arxiv.org/html/1401.6025v3).
The preceding proposed USD refinement would give

    E <= (p^(5e+3)-1) p^(15e+6)/(p-1)^(22e)
      < p^9 * (2/p^2)^e.

The last inequality follows from (1-1/p)^22 >= 1-22/p >1/2.
At e=8 the last bound is256/p^7<1; it decreases geometrically. The usual
length-only classical guarantee m>3d-g+1 fails, since22e<25e+9.

These are parameters of an actual mathematically certified tower, not
unrealizable numerical tuples. Nevertheless the quantum conclusion still
depends on the independently checked status of the USD argument and on
charged source, decoder and compilation costs. The known local pair
implementation costs polynomial in p, not merely log p.

The tower has at least23e rational points. Every F_p-defined map to P1
therefore has degree at least23e/(p+1). With fixed p, rational gonality
grows linearly in e. Also m/p eventually exceeds every constant multiple
of log m. Thus the previous sufficient low-gonality/large-alphabet rejection
argument does not by itself dispose of this asymptotic family.

## 3. The Classical Attack That Does Dispose Of It

Inside L take the degree-eight cover X8 of X0 obtained by adjoining

    w1=sqrt(x(x-1)), w2=sqrt(x(x-2)), w3=sqrt(x(x-3)).

Their independent square classes are the even subsets of {0,1,2,3}, modulo
the unrelated13-factor base relation. All infinity points split. At the
distinguished R0 where w_i/x has residue+1, define

    f=-66+62x-36w1+18w2-45*w1*w2/x+w3.             (1)

The quotient w1*w2/x is the integral function sqrt((x-1)(x-2)); it has no
finite poles. Every term in (1) has poles of order at most2 at infinity.
For the formal parameter u with x=u^-2 and positive leading radicals,
expansion over Q, hence over F_p, gives

    f = -(27/32) u^8 + O(u^10).

The exact series check is independent of a numerical tolerance. In
particular f is nonzero and ord_R0(f)=8, with the weaker bound7 sufficient.

Let H(x) be the product of the eleven x-x_j. On any unramified cover,

    omega=dx/(y H(x)),   div(omega)=32I-D.

This uses div(dx/y)=10infinity on X0 and div(H)=D-22I.
On X8, f belongs to L(2I-9R0). On every higher unramified cover containing
X8, its pullback belongs to L(2I-9R) for any R above R0. Therefore

    div(f omega) >= 30I+9R-D = 3G-D.

The residues h_P=f(P)/(y(P) H'(x(P))) give an annihilator of ev_D L(3G),
hence of the Schur cube. It is nonzero: a regular differential vanishing
on3G cannot exist, because3d>2g-2. In the exact degree-eight control all176
residues are nonzero; that stronger property also pulls back unchanged.

One does not need curve coordinates or this special h in the classical
solver. Compute U=V^3 from the ORIGINAL parity matrix and take any nonzero
vector in U^perp. Normal generation at d>=2g+1 gives EQUALITY
U=ev_D L(3G), not merely inclusion. This equality is essential when using
an arbitrary matrix-computed annihilator. Complete AG duality then gives

    wt(h) >= 3d-2g+2 = 20e+9 > d.

Every nonzero row-space word has at most d evaluation zeros. Consequently
B restricted to supp(h) has full row rank. This is precisely the condition
needed by the known cubic/nonsquare norm solver, for every target syndrome.
The implementation reuses that solver from the preceding bundle; it is
the construction of
[Ragavan-Shutty, Section6](https://arxiv.org/html/2610.00502v1), not a new
classical algorithm. All multiplication spaces, nullspaces and rank tests
cost polynomially many field operations in the explicit matrix size.
The nonsquare2 is verified in F_100003. No random successful annihilator,
exponential codeword enumeration or hidden curve advice is required.

Thus the specified cofinal tower family is classically solved even where
the proposed quantum bound is extremely strong. This argument does not
depend on the USD lemma being correct. It gives witnesses, NOT uniform
sampling of the full-support fiber.

## 4. Bounded Divisor Repairs Also Fail

On the full elementary cover L, the following93 functions are independent
and have poles at most2I:

    1,x; the13 sqrt(x-a); the78 pairwise products.

Independence follows from the distinct Kummer characters, except1,x which
are independent in the trivial character. Their pullbacks remain independent
on every cover containing L. In particular ell(2I)>=93 on those covers.

Now let G=K_X+E, where E is EFFECTIVE of degree r>=3, and remove an effective
puncture divisor P of degree u from the full evaluation set, to ensure
disjointness. Since K_X~10I and D_full~22I,

    K_X-3G+(D_full-P) ~ 2I-3E-P,
    ell(2I-3E-P) >= 93-3r-u.                     (2)

Imposing zeros along an effective divisor removes at most its degree in
dimension. For r=3 and u<=83, (2) forces a nonzero cube annihilator. The
same support-rank argument yields a classical solver, for all sufficiently
large degrees where the stated evaluation conditions hold.

This rules out simply moving the three extra divisor points, distributing
their multiplicities differently, or making a bounded small puncture.
It does NOT cover arbitrary degree-(2g+1) divisor classes: G-K_X need not
have an effective degree-three representative. A bare degree or genus
cannot establish the required inclusion of the full Kummer cover either.
The arithmetic helper explicitly does not verify those geometric premises.

## 5. Exact Native Controls And A Failed Escape Attempt

The actual degree-eight curve has genus41. Its full L(10I+3R0) evaluation
matrix is43-by-176, not the smaller pullback of the base curve's code.

To construct it, decompose the function field into its16 Kummer characters
over F_p(x). The masks are the eight even subsets of {0,1,2,3} and their
13-element complements. The integral functions are x^j z_T, with
z_T^2=product_(a in T)(x-a). Character projection and valuations at each
branch show that any function regular at finite places has polynomial
coefficients in this basis. At infinity, fixed pole parity gives independent
characters on the eight points. Thus the pole-filtered list is complete.

There are64 monomials of pole order<=13. Cancelling coefficients of orders
11,12,13 at the seven other infinity points gives21 independent constraints,
leaving43 basis functions. Evaluation at the176 explicit distinct points
has rank43. Direct Schur computation gives square126, cube173, nullity3.
The analytic residue vector annihilates the computed cube exactly.

The solver verifies the ORIGINAL relation on54 targets in tests: zero,
ones, a nonconstant target,43 coordinate targets, and eight seeded targets.
These are controls, not an empirical all-target proof. The all-target
statement follows from the algebraic construction and rank argument.

A second actual control replaces G by the one-point divisor83R0. It starts
with624 monomials and581 independent jet constraints and again produces
the full43-dimensional code. Its square/cube dimensions are again126/173,
and the matrix-only classical solver works. This finite mutation therefore
does not escape either. Its result is NOT extrapolated into a theorem about
all one-point divisors on every tower level.

## 6. Adversarial Assessment And Next Decision

- A tower seed is not a polynomial-time tower generator. No higher native
  matrices have been generated; parameter records cannot be labeled runs.
- Large prime constants and explicit input size matter. Even the full first
  elementary cover has a20,483-by90,112 parity matrix; we did not build it.
- All-field AG existence is not enough. This source is genuinely prime-field,
  but that does not make it classically hard.
- A failed sufficient cubic length bound is not a failed cubic algorithm.
  This pass supplies a family-wide counterexample to that shortcut.
- The annihilator proof is specific to the indicated divisor/evaluation
  geometry and cover inclusions. It is not a universal AG no-go result.
- Conditional USD success is not an established speedup, independent novelty,
  or a practical coherent circuit. The classical result stands either way.

Stop scaling this family as advantage evidence. A new AG proposal must
first demonstrate that its actual divisor class/evaluation set removes
sections of K_X-3G+D, without destroying the square-decoder guarantee or
reintroducing cheap uniform sampling. The native input construction and
useful-problem reduction must be supplied too. A generic divisor class is
an avenue to investigate, not a claim that those checks will succeed.

The literature audit also found relevant matrix-choosability/additive-basis
existence theorems, e.g.
[Nagy-Pach-Tomon, Theorem1.1(ii)](https://arxiv.org/html/2111.13658).
They must not be mislabeled efficient constructive algorithms: this pass
has not extracted a polynomial search routine from their group-ring proof.
