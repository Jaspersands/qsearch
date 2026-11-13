# Native real quadratic palette in an indefinite division quaternion algebra

Independent review, 2026-11-14. **Proved under the actual rational
five-variable isotropy algorithm's GRH hypothesis.** For a promised
indefinite division quaternion algebra A/Q given by expanded rational
structure constants, one can construct, in randomized polynomial BIT time,
three separately embedded real quadratic fields Q(sqrt(a)), Q(sqrt(b)),
Q(sqrt(ab)), with a,b independent squareclasses, whose abstract biquadratic
compositum has a local degree-four place. All embeddings are expanded in
THE ORIGINAL A. No prime-density or new quaternary-conic claim is needed.
This is a frontend theorem, not an integral principal-generator theorem.

## 1. Source guarantee and expanded norm minus one

Actual Kutas, arXiv:1606.01053v2, retained
`audits/sources/global_isotropy/quadratic_base.txt`, physical LF196–215,
states Fact 2 (Castel): under GRH a randomized polynomial-time algorithm
finds a nontrivial zero of an indefinite rational quadratic form in at least
five variables. LF209–212 explicitly distinguishes this result from the
factoring-oracle algorithms in four variables. This is the already admitted
rational comparator in GLOBAL_COMPACT_ISOTROPY.md, not a consequence of the
separate totally imaginary Witt construction.

The source problem and output are ordinary expanded rational coefficients
and a rational zero; no compact arithmetic-circuit output convention is
introduced. Thus the polynomial BIT guarantee pays the zero's coordinate
lengths. For an expected-time interpretation, cap a run at a constant
multiple of its polynomial expectation and repeat O(log(1/eta)) times.
Check nonzero and the quadratic identity exactly before acceptance; this
gives a fixed polynomial clock with ABORT probability at most eta.

Reduced trace and norm in dimension four are computable with polynomial
bit sizes from the multiplication table: trd(v)=Tr(L_v)/2 and
nrd(v)=(trd(v)^2−trd(v^2))/2. The unit, if not supplied, is found by linear
algebra. Clear denominators in the five-form

    q_5(v,t)=nrd(v)+t².

Since A is indefinite, A tensor R is M_2(R); determinant has signature
(2,2), so q_5 has signature (3,2) and is nondegenerate. Fact 2 applies.
Let (v,t) be its returned nonzero rational zero. In a division algebra,
nrd(v)=0 implies v=0; hence t!=0. Put r=v/t. Then nrd(r)=−1.
All these coordinates are expanded and polynomial in the native input bits.

## 2. Three explicit quadratic embeddings

Set T=trd(r), i=2r−T and a=T²+4. Cayley–Hamilton gives

    r²−Tr−1=0,    trd(i)=0,    i²=a>0.

The element r is not scalar, since no rational scalar has norm −1.
Thus i is nonzero and nonscalar. If a were a rational square, the identity
(i−sqrt(a))(i+sqrt(a))=0 in the division algebra would make i scalar, a
contradiction. Also a=T²+2² is a norm from Q(sqrt(−1)), giving

    (a,−1)_v=+1 for every place v.                       (1)

Find any nonzero rational solution j of trd(j)=0 and ij+ji=0 by exact
linear algebra. The pure subspace has dimension three; anticommutation
with the nonsingular pure vector i is one nonzero linear orthogonality
condition there. Its solution space therefore has dimension two.
For pure j, j²=b is rational. Division ensures b!=0. If b<0, replace j
by ij; its square becomes −ab>0 and it remains pure and anticommuting.
Henceforth b>0. The four elements 1,i,j,ij are linearly independent:
j is outside Q(i), since it anticommutes with the invertible i. They give
an explicit quaternion presentation A=(a,b), without an isomorphism oracle.

Finally define the pure element

    z=(a/2)j+(T/2)ij.

Since j and ij anticommute and (ij)²=−ab,

    z²=(a²b−T²ab)/4=ab(a−T²)/4=ab>0.

It is nonzero because j,ij are independent and a!=0. Each of i,j,z is a
nonscalar pure element of the division algebra; consequently a,b,ab are
all nonsquares. Thus a,b are independent squareclasses and the maps
sqrt(a)->i, sqrt(b)->j, sqrt(ab)->z are the desired embeddings.
They are THREE SEPARATE field embeddings; their images are not asserted
to form a commutative biquadratic subalgebra of the division algebra.

## 3. A full local place is automatic

A division quaternion algebra over Q is ramified somewhere; because A is
indefinite, at least one such place is finite. At every division place v,

    (a,b)_v=−1.

Neither local class can be zero. If they were equal, bilinearity and (1)
would give (a,b)_v=(a,a)_v=(a,−1)_v=+1, contradiction. They are therefore
independent in Q_v*/Q_v*², so Q_v(sqrt(a),sqrt(b)) has degree four.
The independently proved review `2026-11-14-biquadratic-multinorm.md`
then supplies the rational three-norm-product surjectivity over Q.
No ramified prime has to be guessed to construct these embeddings.

## 4. Bit sizes, support, and limits

After Fact 2, only a constant number of rational products, divisions and
fixed-dimensional linear systems occur. If its zero has P(B) bits, the
new coordinates and a,b have O(P(B)+B) bits up to absolute constant
factors; kernel vectors can be chosen by constant-size minors. The inverse
basis matrix for 1,i,j,ij also has polynomial bit length. For a rational
c=u/v, the quadratic field's discriminant has O(log|uv|+1) bits, since
its squarefree radicand divides uv. Thus all three field discriminants,
embedding denominators and index determinants have polynomial bit size.
Computing their prime factors/maximal orders is charged to the separately
retained arithmetic backend; this proof supplies no factorization advice.

Any required finite S can include the primes of these explicit denominator,
index and discriminant integers in addition to the original input support.
Their total encoded bit mass is polynomial in the ENTIRE native input;
it is not asserted to be O(log discr(A)) for an arbitrarily presented order.
The element r, the three generators, and subsequent norm factors have no
integrality or prescribed ideal-alignment guarantee. Compact valuation
magnitudes, evaluation of noncommuting power words on ideals, unit-image
generation and the Page neighbor-table clock remain separate blockers.

Indeed the same Fact 2 directly finds an expanded rational element of any
prescribed nonzero reduced norm c by solving nrd(v)−c t²=0. This is a
strong classical rational-output baseline, but does not control the new
denominators/support or make the element a generator of a prescribed
integral ideal. No example or finite scan is needed for the identities.
