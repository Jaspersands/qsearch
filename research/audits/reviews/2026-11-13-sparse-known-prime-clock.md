# 2026-11-13 — Supplied-prime aligned Gauss valuations: clock review

Scope: independently checked §2 of the completed sparse-vertical advisory
report and SPARSE_VERTICAL_VALUATION_COMPILER. ACCEPT the supplied-prime
compiler after the explicit repairs below. No constant field, maximal order,
local factorization, or aligned-place list is supplied. Complete prime support
remains UNPAID. This is a bounded-error algorithm: successful local certificates
do not certify that specialization preserved the original Gauss valuations.
A bad specialization can return incorrect Gauss rows, with the stated small
probability. That exact-Gauss claim is not unconditional correct-or-ABORT.
Section 7 proves a stronger SOUND CONSTANT-RESTRICTION interface: on a correct
Alg basis, every accepted regular specialization gives all required constant
valuations, and randomness affects completion only.

The main repairs are: compute radical actions using TWO digits before a
residue-field solve; prove the socle representative is integral; carry a
two-digit loss per strict order enlargement; lift residue idempotents through
the nilradical before treating them as component projectors. All original
atoms use the same projectors. No implementation or parameter sweep was run.

## 1. Explicit native bounds and the good specialization

Use the original native model F=Q(T)[Y]/f, monic irreducible degree n=delta>=1,
and nonzero original atoms u_i of Y-degree<n. Retain §1's common denominator
D, numerator coefficient bound H=2^b, d0, e0=(n+1)d0, U and V=n!U^n. In
particular M(u_i)=A_i/D^n and M(f_Y)=J/D^(n-1). The supplied prime p is part
of the input; every cost below charges log p.

Define the following computable INTEGER bounds (logarithms are base 2):

    U0=max(H^n,U),
    B=2+ceil(log2(max(H,V,n![(k+1)U0]^n))),
    Delta=n e0,
    S=binom(k+n,n).

The proof-only polynomial

    C(T,Z)=det(D^n Z0 I + sum_i Zi A_i)

has at most S coefficient polynomials in T. Each has degree<=Delta and
l1 norm<=n![(k+1)U0]^n<=2^B. The same degree/norm bounds cover D, det J and
all det A_i. These last polynomials are nonzero; some coefficients of C may
be zero. All bounds have polynomial BIT length and are computed without
expanding C, its coefficient list, or any sparse product in T.

Let the requested failure parameter satisfy 0<eta<=1/2, and put eps=eta/8.
Choose the least r>=1 with q=p^r satisfying

    q > max(16(n+1)^2, (S+k+2)(Delta+1)/eps).

Thus r log p is polynomial in native bits, log p and log(1/eta). Construct
F_q=F_p[theta]/hbar and use a monic integer coefficient lift h of hbar.
Then R=Z_p[theta]/h is the unramified complete DVR with residue field F_q;
its uniformizer is p. All actual calculations use R/(p^K), represented by
r coefficients and the monic relation h. Let L=Frac(R).

Choose t uniformly in F_q^s and lift each coordinate to its degree<r
representative with coefficients in {0,...,p-1}. This defines an exact
integral point in R^s, without constructing its enormous rational heights.
For each nonzero coefficient polynomial G of C, and for D,det J,det A_i,
divide G by its maximal coefficientwise power of p FOR THE PROOF ONLY.
The result has nonzero reduction. Schwartz–Zippel gives

    Pr(BAD) <= (S+k+2)Delta/q < eps.

On GOOD all these polynomial values have exactly their p-Gauss valuations.
Each such valuation is an integer between 0 and B: a nonzero integer
coefficient bounded by 2^B cannot be divisible by more than p^B.
Constant protected polynomials cause no exception; s=0 is deterministic.
No coefficient extraction, content computation, or exponential union-list
enumeration occurs in the algorithm.

## 2. Preservation is of the full JOINT multiset

Normalize C by D^(n^2). Over an algebraic closure of the p-Gauss completion,
it factors as

    product_(l=1..n) [Z0 + sum_i Zi u_i^(l)].

Put a_li=w(u_i^(l)), with w(p)=1. Weighted Gauss valuation on a polynomial
ring is multiplicative, including arbitrary real weights: this follows from
the product of nonzero initial forms in the associated graded domain.
Consequently the coefficient valuations determine the entire function

    F(x0,...,xk)=sum_l min(x0,x1+a_l1,...,xk+a_lk).

GOOD preserves every coefficient valuation of C and the valuation of D, so
it preserves this function after normalization. At x0=0, xi=-t_i, with no
t_i equal to an occurring a_li, the derivative in x0 counts exactly those
rows satisfying a_li>t_i for EVERY i. Upper-orthant counts determine a finite
joint multiset: inclusion-exclusion recovers counts in every box with
endpoints off the finitely many coordinate values. Thus the specialized
algebra has exactly the original n valuation tuples, with multiplicities.
This is a proof of alignment, not an exponential reconstruction procedure.
Preservation of separate atom norms would not suffice.

## 3. Native p-adic access, scaling and preliminary checks

The following conservative precision allocation suffices:

    Ccap=(n^2+1)(B+1),
    P0=2 Ccap+20,
    Qfin=Ccap+4,
    Kraw=P0+2B+4 = 2 Ccap+2B+24.

Digits are BASE-p digits; bit precision is Kraw log p. Every native sparse
monomial is evaluated in R/(p^Kraw) by binary powering. Original numerator
and denominator values and their common-denominator products are integral,
so these ring operations lose no precision. The cost depends on exponent
bit length, not numerical degree; no exact huge-height specialization is
formed. Common products can be evaluated with polynomially many ring
multiplications without expanding their sparse expressions.

ABORT unless the evaluated D has a visible valuation d_D<=B. When this passes,
D=p^d_D times a unit, and exact unit inversion followed by the known p-power
division gives every rational coefficient to at least P0 digits. Indeed
numerator/denominator perturbations of valuation Kraw change their quotient
by valuation at least Kraw-2d_D>=P0+4. No unidentified p-adic zero is inverted.

Set X=p^B Y and form

    g(X)=p^(nB) f(X/p^B),
    z_i(X)=p^(nB) u_i(X/p^B).

These are integral polynomials whenever d_D<=B: a coefficient of X^h is
scaled by p^(B(n-h)), and h<n. The polynomial g is monic. Form the integral
monogenic order A0=R[X]/g and its multiplication table to P0 digits.
Compute disc(g) and the algebra norms of z_i over L by DIVISION-FREE
matrix determinant algorithms, e.g. Berkowitz; integral circuits lose no
digits. ABORT unless all these quantities have visible valuations <=Ccap.
The nonzero discriminant certifies an actual finite etale L-algebra E.

GOOD always passes these checks, because

    v(disc(g))=n(n-1)B+v(det J(t))-n(n-1)v(D(t)) <= (n(n-1)+1)B,
    v(N(z_i))=n^2 B+v(det A_i(t))-n^2 v(D(t)) <= (n^2+1)B.

All these valuations are nonnegative by integrality. Their upper bounds
are <=Ccap. The global atom norm bound will later bound EVERY component
norm, since all component norm valuations are nonnegative. The preliminary
checks are also useful on BAD points: any point that passes has all the
local-algebra premises and bounds needed for the remaining fixed clock.

## 4. Elementary order normalization, including the missing digits

Let A be an integral R-order in E, with an R-basis and integral multiplication
table known modulo p^P. Initially A=A0 and P=P0. Compute the nilradical N of
A/pA as the kernel of x -> x^(q^n). This map is F_q-linear; the nilpotence
index of an element is <=n and the reduced quotient is a product of finite
fields. Binary powering uses O(n log q) exponent bits, not q^n operations.
Let I be the inverse image of N in A. Thus pA subset I subset A.

Use residue linear algebra and an integral UNIT basis change so that

    I has basis p^eps_j b_j,  eps_j in {0,1}.

If b_i b_j=sum_l c_ij^l b_l, multiplication by b_i on I has entries

    p^(eps_j-eps_l) c_ij^l.

These are integral because I is an A-ideal. A negative exponent requires
one known division by p. Therefore its residue requires c_ij^l MODULO p^2,
not just modulo p. Compute the n action matrices on I/pI and find the joint
kernel of their linear combination with coefficients a_i. Equivalently,

    K={a mod pA : a I subset p I} subset A/pA.

This is one finite-field linear solve AFTER the charged p-divisions.
Let J be K's inverse image in A. Since pA subset I, any x with xI subset I
satisfies px in A (apply x to p*1). It follows exactly that

    (I:I)=p^-1 J.

Thus this kernel gives the whole multiplier ring, not a partial enlargement.
Choose a residue basis of K, extend it to a full basis, and lift the resulting
matrix V to an integral unit matrix. If d=dim K, a basis change to the new
order is

    F=V diag(p^-1 I_d, I_(n-d)).

Each input basis vector loses at most one digit in a product, so the new
structure table is known to P-2 digits. The inverse

    F^-1=diag(p I_d,I_(n-d)) V^-1

is integral. Thus conversion of the original z_i coordinate vectors (and 1)
loses NO additional digits. Unit changes and unit inversions lose none.
Retain the old table at full precision when doing the basis recoding: the
one-digit division used to choose K does not consume another digit of it.
The per-enlargement loss is at most TWO, not an unbounded accumulated
conditioning factor. All pivots are residue-field unit pivots, and all
choices are determined at visible finite precision.

Here is the full stopping proof. The multiplier ring is an order: it acts
on the finite free module I, so Cayley–Hamilton makes its elements integral.
Let O be the integral closure of A in E, a product of DVRs. Then

    I=rad(pA)=A intersect rad(pO).

If O/A is nonzero, it has an element annihilated by I: a power of I kills
this finite module, so take a nonzero element in its last nonzero I-power.
Choose a representative x IN O, not in A. Its socle property gives xI subset A.
Its integrality gives xI subset rad(pO), hence xI subset I. Thus (I:I)>A.
The assertion xI subset A alone would not justify that conclusion.
Conversely, when A=O, the radical is a product of invertible DVR ideals,
so (I:I)=O. Therefore K=0 is an exact maximality certificate.

A strict enlargement has R-length d>=1 and lowers the discriminant valuation
by 2d. Initial discriminant valuation is <=Ccap and the final discriminant
is integral. There are at most floor(Ccap/2) strict steps; cap the loop there
plus its final stability test. At every stage

    P >= P0-2 floor(Ccap/2) >= Ccap+20 > Qfin.

This proves the entire precision ledger, including repeated denominator
changes. Actual coefficient bases need not be expanded as huge-height global
numbers: retain their unit/power-of-p change matrices or compute directly in
the indicated finite rings. The exact corresponding R-lattices exist by the
proof, while their stored tables carry the displayed precision invariant.

## 5. Residue decomposition, idempotents and the output rows

For the resulting O, compute O/I, a reduced finite F_q-algebra of dimension
m<=n. Choose a random element and test whether 1,a,...,a^(m-1) is a basis.
The at most m conjugate evaluation maps are distinct; a collision of any
pair has probability at most 1/q. Since q>16(n+1)^2, a primitive element
exists with success probability greater than 1/2 per trial. On success its
squarefree minimal polynomial has degree m. Factor this ordinary dense
finite-field polynomial and use polynomial CRT to obtain its primitive
idempotents in O/I. No p-adic polynomial factorization oracle is invoked.

Lift each residue idempotent to an arbitrary integral representative e0 in O,
and iterate e -> 3e^2-2e^3 modulo p^Qfin. The unique actual component idempotent
e* has e0-e* in I; each iteration squares this error ideal. Since I^n subset pO,
ceil(log2(n Qfin)) iterations give e-e* in p^Qfin O. This pays the initial
nilradical: a lift from O/I is not automatically an idempotent modulo p.
All operations here are integral and lose no digits.

The multiplication projectors for these SAME idempotents are used for every
z_i. Select independent projector columns modulo p and assemble a joint
unit basis for their direct sum. If the j-th block has dimension d_j, it is
the lattice of one field factor E_j of E, with [E_j:L]=d_j. Unit basis inversion
and block restriction are stable to Qfin digits. The block multiplication
determinant for z_i is its component norm modulo p^Qfin. As z_i is integral,

    0 <= v_p(N_(E_j/L)(z_i)) <= v_p(N_(E/L)(z_i)) <= Ccap.

Since Qfin=Ccap+4, each integer valuation nu_ji is determined exactly.
Output the rational row

    a_ji=nu_ji/d_j - nB,

with multiplicity d_j (or explicitly repeat it d_j times). For a finite
extension of a complete p-adic field, v_p Norm(z)/[E_j:L] is the valuation
normalized by w(p)=1. Thus these are exactly the specialized ORIGINAL-atom
rows. They form n entries with multiplicities, all aligned; subtraction of
nB undoes the atom scaling. Their rational bit lengths are polynomial.
On GOOD, §2 proves these are the original Gauss-extension rows as well.

## 6. Remaining finite clocks and exact error classification

For completeness, finite-field randomness can be capped explicitly. A random
monic degree-r polynomial over F_p is irreducible with probability at least
1/(2r); test it by the usual exact Frobenius/gcd irreducibility criterion.
At most ceil(4r log2(2/eps)) trials give failure <=eps. Degree-one construction
is immediate. The primitive-element search above can use
ceil(log2(2/eps)) trials, with visible rank certificates.

Dense squarefree factorization needs no unbounded retry: distinct-degree
factorization uses gcds with powers X^(q^d)-X. In an equal-degree block with
at least two factors, a random element splits with probability at least 1/2.
For odd q, first take its gcd and then use its (q^d-1)/2 power to split the
nonzero signs. For even q, its absolute trace from F_(q^d) to F_2 splits the
components. Binary powering/trace uses polynomially many operations in
n and log q. Cap each of the at most n splitting searches at
ceil(log2(2n/eps)) trials. The total failure is <=eps; multiplication and
irreducibility checks certify the returned complete factorization.

Uniform field sampling also has a fixed clock. There is a known polynomial
bound M on the number of scalar F_p draws: for example r times the sum of
r times the field-construction trial cap, s, n times the primitive-element
trial cap, and n^2 times the factorization trial cap suffices. For each draw,
cap binary rejection sampling at ceil(log2(M/eps)) attempts; the union failure
is <=eps and accepted draws are uniform. This removes an implicit unbounded
sampling loop. Every other loop above has its explicit algebraic cap.

The ring size is r*Kraw*log p bits; matrix dimensions are polynomial in n,k,
and every exponentiation uses binary exponents. The normalization iteration
count is O(n^2 B), with two digits charged per step. Thus the complete bit
cost is polynomial in native input size, log p and log(1/eta), with a fixed
exponent independent of n and numerical sparse degree.

On GOOD, and absent a capped finite-field/sampling failure, every preliminary
check and later exact certificate passes and all original rows are returned.
The union of BAD and the four capped backend failures has probability at
most 5eps<eta. Wrong Gauss rows can occur only on BAD, with probability<eps.
An accepted BAD sample still computes valid rows of its specialized etale
algebra; its local certificates alone cannot certify the Gauss-alignment
premise. This distinction must remain in any downstream confidence claim.

## 7. Stronger intended interface: sound restriction to algebraic constants

The parent's proposed restriction to Alg is valid and removes the correctness
risk from specialization for that interface. It uses NO joint-characteristic
preservation premise. Let C0 be the algebraic closure of Q in F, let c=[C0:Q],
and consider ANY point that passes the denominator, discriminant and atom
norm checks above. Embed L in Cp. Write X=(X1,...,Xs) for formal variables and
substitute T=t+X into the coefficient functions. D(t)!=0 makes their expansions
well defined in Cp[[X]]. Every specialized root y_l has f_Y(t,y_l)!=0, so the
formal implicit-function theorem gives one root series y_l(X) with that
constant term. All n root series are distinct. No convergence estimate or
p-adic analytic continuation is needed: the nonzero derivative is invertible
in the coefficient FIELD Cp and the formal coefficients are solved recursively.

The fraction field of Cp[[X]] contains Q(T) injectively via T=t+X. Translation
is injective on polynomial rings even when t is algebraic. Since f is
irreducible over Q(T), the n root series give n distinct Q(T)-embeddings of F,
and exhaust them. Every element of C0 maps to a CONSTANT in Cp: its minimal
polynomial over Q splits into linear factors over Cp, and their product can
vanish in the formal fraction field only if one factor vanishes. Every
embedding sigma:C0->Cp extends to exactly n/c of the n embeddings of F.
Indeed C0(T) is a pure transcendental extension of C0, the variables remain
independent over Cp, and every root of f already lies in the target formal
field. For s=0 this is simply the ordinary number-field embedding count.

Every original u_i is regular at every root and has nonzero value, by the
accepted denominator and norm checks. Hence for EVERY e in the true Alg,
including arbitrary negative coordinates, taking constant terms gives

    product_i u_i(t,y_l)^e_i = sigma_l(product_i u_i^e_i).

Taking the normalized p-adic valuation proves

    sum_i e_i a_li = v_p(sigma_l(u^e)).

This holds simultaneously for every e, with one joint embedding sigma_l per
row. Every constant embedding occurs n/c times. Consequently these restricted
rows cover every p-adic place of C0 with the correct embedding multiplicities;
their common kernel on Alg consists exactly of constants that are units at
ALL places over the supplied p. Same-row alignment is essential here too.
The component rows in §5, repeated d_j times, are precisely the n evaluated
root rows used in this proof.

For this interface alone, omit C, S and the exponential coefficient union.
Replace B by

    B0=2+ceil(log2(max(H,V)))

throughout the scaling and precision schedule, and choose

    q > max(16(n+1)^2, (k+2)(Delta+1)/eps).

The GOOD event now protects ONLY D,det J,det A_i. It is used solely to prove
that the bounded precision and preliminary valuation caps pass with high
probability. EVERY accepted point is sound on Alg, even outside GOOD. The
same fixed-clock proof gives ABORT probability <=eta and zero mathematical
error in the restricted rows. Given a correct integer basis of Alg, restrict
the exact rational rows by integer matrix multiplication; its cost is
polynomial in that basis's bit length and needs no additional p-adic precision.
If Alg itself was obtained by a bounded-error upstream algorithm, its failure
budget remains separate; this lemma does not certify an erroneous Alg basis.

This is a complete supplied-prime CONSTANT-UNIT-KERNEL interface without a
constant-field computation. It is sufficient for intersection over a supplied
complete prime list. Finding that complete list remains a different operation.

## Disposition

The joint-characteristic alignment argument survives; the p-radical
multiplier-ring construction is constructive after the two-digit repair;
the corrected integral socle argument proves termination; and the explicit
Kraw allocation pays all successive basis and determinant losses.
Exact original Gauss rows are bounded-error. Their restriction to the true
Alg is stronger: every accepted regular point is sound, and the smaller
protected family gives a complete correct-or-ABORT compiler for the supplied
prime's constant-unit conditions. Neither conclusion discovers all primes
or supplies a full growing-degree relation algorithm on its own.
