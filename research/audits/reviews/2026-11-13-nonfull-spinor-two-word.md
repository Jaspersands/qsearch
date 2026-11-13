# Proper ternary stabilizer spinor image pays a two-move transporter

13 November 2026. Independent local proof. STATE/TRAPS, the reviewed binary
norm compiler, four-word proof, actual Beli thesis/classification and Kirschmer
source were read. Critical OCR inequalities were checked against rendered PDF
pages. No network, API, Git, new finite controls, or shared-status edits.

## 1. The exact conclusion

Let F/Q_2 be ANY finite extension, with v(pi)=1 and e=v(2). Let L and L'
be isometric nonsingular ternary O_F-lattices. Choose good BONGs with norms
a_1,a_2,a_3 and b_1,b_2,b_3, respectively. Their valuation invariants agree;
write R_i=v(a_i)=v(b_i), with R_1<=R_3. Define

    W=F^*/F^*2, V=O_F^*F^*2/F^*2,
    Theta_L=theta(O^+(L)) subset W,
    x=b1/a1, z=b3/a3.

**Theorem.** If Theta_L != W, the adjacent binary word

    12(x), 23(z)                                      (1)

is legal. It changes the norms to (b1,a2*x*z,b3); a unit-square rescaling
of the middle BONG vector gives exactly the target tuple. The previously
proved quadratic-order norm construction therefore produces an actual local
coordinate transporter with polynomial bit cost in the expanded local input,
e,f and requested precision. The same orientation works in every case;
trying a reversed word is unnecessary for this theorem.

No claim is made that every full-image lattice admits two or four moves.
The theorem concerns actual integral lattices and their good BONGs, not
merely isometric rational quadratic spaces.

## 2. Source contracts and the important boundary signs

Primary thesis: `sources/spinor_genus_admission/beli_thesis.pdf`/`.txt`.
Physical PDF page numbers are printed page numbers plus 11.

* Lemma1.4.3(i)--(ii), printed56/PDF67, gives property A iff R_i<R_(i+2)
  for a BONG, and good iff the corresponding inequalities are non-strict.
  Thus rank three has property A precisely when R_1<R_3.
* Corollary1.4.10(ii)--(iii), printed67/PDF78, embeds the adjacent binary
  proper spinor groups G(a_(i+1)/a_i), including their changes after an
  adjacent binary move, inside Theta_L.
* Definition9 and Lemma1.4.11, printed67--69/PDF78--80, say that property A
  but not property B forces Theta_L=W. The triggering conditions for B are
  a gap <=2e+1 that is odd, OR an even gap R with

      d(-epsilon_i*epsilon_(i+1)) <= e-R/2.           (2)

  Each existing neighboring gap must then be >=2e+1. The inequality in (2)
  is INCLUSIVE; OCR turns it into a strict inequality. The proof includes
  equality and explicitly uses the unramified class Delta to produce two
  distinct norm hyperplanes. No unproved equality repair is required.
* Section1.7, printed105/PDF116, states that without property A, Theta_L is
  either W or V. Lemma1.7.1(i), printed105--106/PDF116--117, gives the exact
  binary criterion, for an admissible ratio a=pi^R*epsilon:

      G(a) subset V iff R is even and either
      a in -(Delta/4)*O_F^*2 or d(-epsilon)>e-R/2.     (3)

  Here Delta is the nonsquare unramified quadratic class, d(Delta)=2e.
  The exceptional alternative has R=-2e and defect2e. The hyperbolic
  a in -(1/4)*O_F^*2 has infinite defect and satisfies the second alternative;
  its special G=V rule is explicit in Definition3, printed29/PDF40.
* Theorem3, printed112/PDF123, additionally characterizes Theta_L subset V
  by the binary containments and (R_(i+1)-R_i)/2=e mod2 when endpoints agree.
  This parity condition is correct but is NOT needed in the argument below.

These facts match `sources/dyadic_seed_selection/kirschmer_code/genus.m`
LF260--298 and LF648--683. That code's OnePlusPowerOfP, LF242--248, literally
enumerates all squareclasses: its implementation clock is NOT imported.
Use the already reviewed polynomial filtration/symbol compiler instead.

## 3. Binary thresholds and classification information

Write Hilbert symbols as F2 bits and put

    C=-a1*a2, D=-a2*a3, m=R2-R1, n=R3-R2,
    h(q)=min(e+m/2, m+d(C*q)),
    k(p)=min(e+n/2, n+d(D*p)).                       (4)

Let U_t be the unit-squareclass defect filtration. Beli's binary criterion
is eta in U_alpha intersect N(-a_i*a_(i+1)); see classification LF980--997.
Thus (1) requires

    d(x)>=h(1), <C,x>=0,
    d(z)>=k(x), <D*x,z>=0.                           (5)

Good-BONG admissibility gives m,n>=-2e, m+d(C)>=0, n+d(D)>=0 and m+n>=0;
in particular h(1),k(1)>=0. See classification LF90--97.
The rank-three alpha invariants are

    alpha1=min(h(1),m+k(1)),
    alpha2=min(k(1),n+h(1)).                         (6)

Isometry implies these invariants agree at the target, and Theorem3.1(iii)
gives d(x)>=alpha1 and d(z)>=alpha2. Determinant matching makes
b2/(a2*x*z) a unit square. Rational Hasse matching gives

    <C,x> + <D,z> + <x,z> = 0.                      (7)

Consequently the final norm condition in (5) follows from the first one.
Classification Theorem3.1 is LF680--686 in the retained classification text.

## 4. A gap above 2e: one endpoint is a square

This case does not even need the proper-image assumption. If m>2e, then
h(1)=e+m/2>2e. Since k(1)>=0, both entries of the minimum for alpha1
exceed 2e, so x is a unit square. Also

    n+h(1) >= e+n/2 >= k(1),

using m+n>=0. Hence alpha2=k(1)=k(x), and (7) pays the last norm condition.
Both moves in (1) are legal; the first is only a square rescaling.
If n>2e the symmetric argument makes z a square and alpha1=h(1); (7)
then gives <C,x>=0, and the final square multiplier is automatically legal.

## 5. Strict endpoint inequality, with both gaps <=2e

Suppose R_1<R_3 and m,n<=2e. Property A holds. Since Theta_L is proper,
Lemma1.4.11 forces property B for the chosen BONG. Neither gap can be odd:
the other gap would have to be >=2e+1. Nor can the inclusive defect trigger
(2) hold. Therefore m,n are even and

    d(C)>e-m/2, d(D)>e-n/2,
    h(1)=e+m/2, k(1)=e+n/2.                         (8)

Equation (6) now gives alpha1=h(1), alpha2=k(1), since
m+k(1)-h(1)=n+h(1)-k(1)=(m+n)/2>0. In particular

    alpha1+alpha2=2e+(R3-R1)/2>2e.                  (9)

The same statements hold for the target lattice, whose spinor image is
isometry-invariant. Thus k(x)=alpha2. Theorem3.1(iv) now requires b1 to be
represented by [a1,a2], equivalently <C,x>=0. The prefix-defect bounds and
(7) give all of (5). This also reproduces the reviewed high-alpha theorem.

## 6. Equal endpoint valuations, including both boundary binary types

Suppose R_1=R_3, so n=-m and -2e<=m<=2e. Property A fails. The source
dichotomy and proper-image assumption give Theta_L=V. Each adjacent binary
G is contained in V. Apply (3) to both ratios: m is even, and on putting

    h=e+m/2, k=e-m/2,       0<=h,k<=2e, h+k=2e,

we obtain d(C)>=k and d(D)>=h. The first is STRICT unless the first ratio
is -(Delta/4) times a unit square; that exception has m=-2e, h=0,
and C is the unramified class. Likewise for the second ratio.
It follows directly from (4)--(6) that

    h(1)=alpha1=h, k(1)=alpha2=k.                    (10)

The target has the same image V. Applying (3) to its second ratio also
gives k(x)=k. Classification therefore pays both depth conditions in (5).

If h>0 then d(C)>k, and d(x)>=h implies d(C)+d(x)>2e. The Hilbert defect
rule gives <C,x>=0. If h=0, admissibility and (3) say C is a square or the
unramified class. The square character is trivial; the unramified character
is v(.) mod2, hence is trivial on the unit x. This also gives <C,x>=0.
Equation (7) proves the final norm condition. This handles h=0 and k=0,
including hyperbolic and unramified-anisotropic binary boundary lattices.
No parity rounding or presumed generic nonzero defect was used.

## 7. Native construction and the precise seed-free consequence

The native setup is already paid in `reviews/2026-11-07-spinor-genus-sources.md`:
minimum-entry block splitting and at most three Beli1.4.6 repairs construct
the good BONG in polynomial expanded height; O(ef) explicit generators and
Voight6.1 Hilbert linear algebra compute Theta_L and every required filtration.
Thus testing whether Theta_L=W is also polynomial, not an extra oracle.

The cases exhaust R_1<=R_3 and prove (1). Realize its two unit multipliers
using the reviewed rank-two ORDER norm compiler, embed each adjacent BONG
replacement, and square-rescale the middle vector. Convert the frames back
to original coordinates. The retained polynomial guards and exact checks
det X a unit and X^T A X=B mod pi^M apply, where pi^s_B*B^-1 is integral and
M=s_B+2e+3 suffices for the existing
inverse-square-root lift/spinor-offset verifier. e,f, local presentations,
coefficients and all requested digits remain charged; no residue enumeration
or indefinite number of binary moves is introduced.

Conversely, when Theta_L=W and L,L' have ALREADY passed the exact local
integral-isometry test, no seed is needed merely to determine the relative
proper spinor-image coset. That coset is d*Theta_L=W for every possible
offset d. It is nonempty: an improper transporter can be made proper by
composing with -I in odd rank. Full spinor image alone does not certify local
isometry, and this observation does not output a transporter in that branch.

The earlier Q2(sqrt2) example requiring four moves has R=(0,0,3), e=2.
Its odd gap3 and neighboring gap0 violate property B, so its image is FULL.
It is consistent with, and explains the need for, the proper-image hypothesis.
This proof pays the local seed/offset dichotomy needed by the retained global
decision composition. Global hypotheses, witness construction in full-image
cases, novelty, practicality and quantum/classical comparisons are separate.
