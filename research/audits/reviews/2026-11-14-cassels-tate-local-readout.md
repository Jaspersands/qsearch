# Native Cassels--Tate local readout: the remaining descent operation

2026-11-14. STATE/TRAPS, CASSELS_TATE_NATIVE_ADMISSION and the retained
all-prime Kummer interfaces read. Actual Shukla thesis LF4832--4940,
5331--5420,5720--5775 and the necessary adjacent definitions were checked;
actual Stoll Prop5.1/proof, LF763--897, was also read. No tests, implementation,
network/API/Git or shared-status edits. The global cochain construction is
CONDITIONAL throughout; this review does not duplicate its separate audit.

**Disposition:** the native local image pays the first local-point step;
there is an algebraic replacement for the printed 4^g torsion search.
The final root-orbit Hilbert-symbol computation is polynomial once its
base-field arguments are available. However, polynomial EVALUATION of the
global cochain alone does not establish a polynomial local compiler:
Proposition4.3.15 still requires a compressed semilinear descent/norm-obstruction
operation. Even granting efficient evaluation of the resulting local cocycle
is insufficient to apply the retained expanded-field Hilbert90 algorithm.
This is a precise unpaid interface, not a complexity lower bound or no-go.

## 1. What the retained local data really provide

Put n=2g+1 and A_p=Q_p[T]/f. Its factor fields have total degree n; the
native OM/factor identifiers and squareclass frames are constructed without
a normal closure. LOCAL_KUMMER_ALL_PRIMES and its precision reviews return
basis labels WITH exact actual-point/root-chart DAGs and finite digits.
To realize a specified local Selmer label d, solve an F2 linear system and
add the selected O(g) point representatives. The retained materializer may
add 2sigma; this preserves precisely the Kummer label needed here.
Thus one obtains an ACTUAL Q in J(Q_p), not merely a formal squareclass.
The same finite conditioning/reset argument supplies generic Mumford data
[a,b] coprime to f, with paid coefficient and resultant guards.

Use representatives d consistent with the supplied global cochain. For
clarity, one may grant even polynomial-size expanded representatives here;
the descent issue below persists under this stronger input. Replacing a
compact representative by a square-equivalent one must also change the
cochain convention or record its square-root gauge; it is not a free edit.
For mu(Q)=(-1)^deg(a) a(T), compute in A_p one root

                       r^2=mu(Q)/d.

Existence follows from equality of the native labels. This is precisely the
retained componentwise square-root interface; it does not adjoin all roots
of f. Its required precision is paid by the input/resultant bounds, with
consistent selectors. The rational point Q need NOT itself have a rational
half: d is generally nontrivial.

## 2. The torsion-adjustment loop is not an intrinsic obstruction

Let theta_i be formal labelled roots and choose the same sqrt(d_i) used to
define the source cocycle alpha. Set s_i=r(theta_i)sqrt(d_i). Interpolate
s modulo f, and apply Stoll's congruences to obtain P with 2P=Q.
Stoll Prop5.1 gives a bijection between roots s modulo common sign and the
halves of Q, with a uniquely normalized minimal solution; hence this map
commutes with Galois action. Its torsor action is the standard one:
changing s_i by e_2(T,T_i) translates P by T. This follows by evaluating
the functions with divisors 2(T_i-infinity) in the Weil-pairing definition;
the common sign is the kernel of the root-sign-to-J[2] map. Equivalently,
these are the usual square-root coordinates on the [2]-torsor.
Because r is an element of A_p, its conjugate coordinates permute without
an extra sign. Consequently

                 sigma(P)-P = pi( sigma(sqrt d)/sqrt d ) = alpha(sigma).

Thus the desired half can be selected algebraically WITHOUT enumerating
J[2] or checking 4^g candidates. Alternatively, with explicit generators
of a Galois action, an already chosen half's correction is a linear system
(sigma-1)T=alpha(sigma)-[sigma(P)-P] on the 2g-dimensional torsion module.
That alternative does not make a splitting-field action oracle free.

The interpolant is explicitly
 s(X)=sum_i r(theta_i)sqrt(d_i) f(X)/((X-theta_i)f'(theta_i)).
It and Stoll's O(g)-size determinants have polynomial-size arithmetic
CIRCUITS in labelled radicals. This is not an expanded polynomial-degree
field, nor by itself a certified finite-bit evaluator of those circuits.
In particular the retained all-rational-halves precision theorem cannot
silently be applied to a common exponential-degree radical field. Nothing
in this section claims that such an expansion is necessary.

## 3. Exactly what Proposition4.3.15 still asks us to compute

Fix a local root orbit, E=Q_p(theta), and put E'=E(sqrt(d'_theta)). If d'
is a square, this orbit's symbol is already1. Otherwise let F contain the
source's radical data and E', H=Gal(F/E'), and choose g outside H. Even
GRANT polynomial evaluation of the full local gamma of Eq4.2.1, not just
the global epsilon. Source LF4853--4869 says that

             Gamma(h)=gamma(h,-1),   h(omega)=Gamma(h)omega

is a Hilbert90 descent equation. Source LF4914--4937 then gives

 delta=gamma(g,-1)/(g(omega)omega) in E*,  local sign=(delta,d'_theta)_E.

The second Hilbert argument is d', as the derivation shows; the omitted
prime in some pseudocode is not a different pairing convention.
The solution space is an E'-line. Replacing omega by c*omega for c in E'*
changes delta by Norm(E'/E)(c)^(-1), so only its quadratic norm class is
needed. A generator of the line is sufficient, but not logically necessary.

If F/E' has an EXPANDED polynomial-degree model with action matrices and
values Gamma(h_j) for generating h_j, solve the simultaneous linear equations
 h_j(omega)-Gamma(h_j)omega=0. No enumeration of H or Hilbert90 trace sum is
needed. A nonzero kernel vector suffices, and determinants then compute
delta. A polynomial coefficient/pivot valuation bound pays finite precision.
This is a genuine linear-algebra repair of the printed group sum, BUT its
matrix dimension is [F:E']; polynomial cocycle evaluation does not bound it.
The source only places omega in K_w, its common radical field, LF4884--4887;
it gives no polynomial-degree descent model for growing genus.

The precise missing operation is therefore: from the compressed local
semilinear line specified by gamma/Gamma, compute its quadratic norm
obstruction in E*/Norm(E'/E) with polynomial bit and precision cost.
Acceptable replacements include a polynomial-size expanded descent module,
a proved compressed invariant computation, or a polynomial list of explicit
quaternion symbols representing the same class. The native Kummer labels
and point DAGs supply none of these automatically. Taking a norm out of an
even-degree splitting field is not a substitute: it can erase a 2-torsion
Brauer obstruction. A local proof must also bound cancellation/pivot losses;
a count of arithmetic-circuit gates alone does not do so.

## 4. The final readout, conditional on that missing output, is small

For delta in E* with certified valuation/unit precision, no large field is
needed. At odd p its squareclass uses valuation parity and residue squareclass;
at p=2, units modulo pi^(2e_E+1) suffice, with e_E<=n. Native finite local
arithmetic thus reads polynomially many bits, provided delta's normalization
and nonzero valuation guard are actually supplied by the descent compiler.
One explicit symbol algorithm constructs only the QUADRATIC extension E',
computes its squareclass generators, takes their degree-two determinant norms,
and tests delta's label in their span in E*/E*2. This is the norm criterion
for the Hilbert symbol; finite unit filtrations have O([E':Q_2]) generators.
No residue-field enumeration or radical compositum is involved. At real
places the symbol is negative exactly when both arguments are negative;
complex places contribute1.

There are at most n local root orbits, with total degree n. Multiply their
signs: local corestriction preserves the invariant, so no extraneous factor
[E:Q_p] is inserted. Globally the finite support set S must still be certified
from the cochain, as in source LF5258--5269; this is outside this local claim.
The sign encodes invariants0 and1/2 as +1 and-1. Until the compressed descent
operation and its guards are proved, no general native Cassels--Tate matrix
clock follows, even though local Kummer images and final Hilbert symbols
are paid. The conclusion leaves alternative pairing constructions open.
