# Small-Diagonal Bounds For Factors And Automorphisms

2026-10-26. Status: new written deduction, not independently reviewed.
Exact supplied-order certificate controls accompany the proof. No native
geometric decomposition, unknown endomorphism or quantum algorithm ran.

## Decision

The one-endomorphism polarization lead had a real scope gap: its previous
small-a competitor covered only factors isomorphic to the ORIGINAL E.
The following argument covers ALL elliptic factors, including nonfree
rank-one modules. It closes that loophole without enumerating more forms.

If a useful factor exists for a binary principal Hermitian form H with
diagonal coefficients a,d, there is an actual noncommuting endomorphism
of E of degree at most floor(min(a,d)^2/4). Consequently small min(a,d)
has a classical polynomial-in-value baseline even if the other diagonal
and off-diagonal coefficient are enormous. Stabilization does not evade
this bound. A second lemma bounds every useful automorphism of the binary
form or its product powers by degree min(a,d)^2. No assertion is made for
superpolynomial reduced diagonals or unrelated higher-dimensional sources.

## 1. Native Input And Candidate Mechanism

E is supersingular in characteristic p>3. The native input gives its curve
model and an efficiently evaluable nonscalar alpha in End(E), with paid
degree bounds, evaluator length and definition field. Put K=Q(alpha).
The unknown full order O=End(E) is NOT input. Choose a,d positive integers
and beta in the known integral quadratic algebra, such that

    H = [[a,beta],[beta^dagger,d]],  a*d-Norm(beta)=1.

H is a positive principal polarization on E^2. The earlier construction
models an eightfold stabilization through smooth quotients and then invokes
polarized decomposition. Its intended new information is a primitive
projector P outside M2(K). Such a projector gives a noncommuting map and
therefore a full-rank generated order for the downstream source.

Every geometric operation in this proposed completion is CLASSICAL. There
is no intrinsic quantum speedup in it. The endpoint with one given map
already has substantial classical and quantum baselines, including the
discriminant-dependent algorithms of
[Herledan Le Merdy--Wesolowski](https://arxiv.org/html/2309.11912v4).
This pass tests whether geometric decomposition can improve input access;
it does not presume that improvement or promote a CandidateRecord.

## 2. Factor-Independent Extraction Lemma

Let F be ANY geometric elliptic factor of (E^2,H), with its principal
polarization. Write its projection as the row f=(u,v):E^2->F, where
u,v:E->F are actual homomorphisms. This does not identify F with E.
The polarized section is H^-1 f^dagger, so

    f H^-1 f^dagger = 1_F,
    P = H^-1 f^dagger f in M2(O).

Put m=deg(u), n=deg(v), and z=a*v-u*beta:E->F. Completing the square gives

    deg(z)+deg(u)=a.

Indeed, multiply the first identity by a and use a*d=Norm(beta)+1.
Its terms are a*d*deg(u), -a times the reduced trace of u*beta*v^dagger,
and a^2*deg(v); these are exactly deg(z)+deg(u). This argument is valid
for inseparable maps as well, using degree norms and canonical duals.

Now define the actual endomorphism of the ORIGINAL E

    w = u^dagger*z,
    deg(w) = m*(a-m) <= floor(a^2/4).

To check that it carries precisely the useful information, set

    S = H P = f^dagger f
      = [[m,h],[h^dagger,n]],  h=u^dagger*v.

Then w=a*h-m*beta. Since H,H^-1 and beta lie in M2(K), and m,n are
scalars,

    P in M2(K) iff S in M2(K) iff h in K iff w in K.

The centralizer of nonscalar alpha in the quaternion algebra is exactly K.
Thus P outside M2(K) forces [alpha,w]!=0. Neither a free module basis nor
a unit vector in O^2 was used. This is the missing nonfree-factor case.

If m=0 or m=a, w=0 and P is uninformative. The proof never divides by m;
these endpoints are handled, not dropped as exceptional numerical cases.

## 3. An Algebraic Certificate Without Finding F

The same deduction can be checked directly from an integral nonzero proper
H-self-adjoint idempotent P in M2(O). S=HP is Hermitian positive semidefinite
of rank one; H-S has the same positivity. Therefore 0<=m<=a, 0<=n<=d,
Norm(h)=m*n, and the quaternionic rank-one trace identity is

    d*m+a*n-Trd(beta^dagger*h)=1.

Expanding Norm(a*h-m*beta) using these two equations and
Norm(beta)=a*d-1 gives exactly m*(a-m). The off-diagonal h is the only
possible nonscalar-algebra obstruction in S. This proves the same
commutant equivalence without selecting any coordinates on the factor F.

nonfree_factor_bound.py checks this certificate from a SUPPLIED ambient
order and projector. That access is only for tests. It rejects rational
nonintegral idempotents, non-orthogonal idempotents, nonprincipal forms,
scalar orientations and beta that already supplies outside-K advice.

## 4. Native Extraction And Its Costs

If the geometric pipeline actually produces a factor, it need not reveal
the unknown comparison isomorphism to extract P. In the notation of the
existing converter, with Q=D^2,

    F*C=C*F=Q I,
    L=q^dagger e q=Q F^-1 P F,
    F L C=Q^2 P.

All numerator maps are native. Divide its individual E->E corner maps by
Q^2 using the published isogeny-division interface. Zero maps are handled
separately; for a nonzero integral quotient the numerator degree is at
least Q^4, satisfying the interface's size condition when Q>1. Charge
degree bounds, representation size, finite fields and native zero tests.
No hidden full order is needed.

For the eight-copy stabilization, polarized decomposition uniqueness
places each primitive factor in one original surface copy. The other
blocks of P vanish. This follows from the same unique-decomposition
dependency already used by the previous report, not from unpolarized
matrix factorization. See
[Ibukiyama--Karemaker--Yu, Theorem 4.20](https://arxiv.org/html/2205.13180v3#S4.SS5).

Compute S=HP by native operations. Its diagonal map [m] can be identified
by exact trace reconstruction, and w=a*S12-m*beta is then evaluable.
The degree ceiling is small even if the expression producing w is long;
charge compression when reusing it. This describes a conditional native
extractor. The local certificate code does NOT perform these steps.

## 5. The Matched Classical Competitors

### Bounded-Degree Endomorphism Search

On the SAME original E and alpha, enumerate all endomorphisms of degree
at most B=floor(a^2/4), and test their commutators with alpha. If the
geometric factor attack can succeed, this enumeration can succeed too.
It does not need to construct H, any PPAV, or the factor F.

This is polynomial in the VALUE of B and the paid native input length,
not in log(B). One elementary realization enumerates finite subgroup
schemes of elliptic isogeny degree at most B, computes quotient curves,
and tests their isomorphisms back to E. For prime-to-p degree the torsion
and subgroup counts and extension degrees are polynomial in B. If p<=B,
include the bounded number of Frobenius factors; the value bound still
pays for them. Test the native commutator by exact degree-bounded equality,
charging alpha evaluation and the auxiliary fields. No maximal-order oracle
or hardness assumption enters this baseline.

### Complete Factor Search Without The High-Dimensional Converter

There is also a direct exhaustive description of all elliptic factors,
not just a witness implication. Enumerate nonzero u,z:E->F into a common
codomain, up to computed codomain isomorphisms, with

    deg(u)+deg(z)=a.

For each pair test native divisibility of z+u*beta by [a], and, if integral,
set v=(z+u*beta)/a. Then f=(u,v) satisfies f H^-1 f^dagger=1 and produces
an actual factor projector. Conversely EVERY useful factor supplies just
such a pair by Section 2. Endpoint zero cases can be treated separately;
they never supply a noncommuting witness.

Enumerating the two low-degree maps and aligning their codomains costs a
polynomial in the VALUE a. The possibly huge beta only enters evaluation,
degree accounting and efficient scalar division. If a numerator is nonzero
but has degree less than a^2 it cannot have a nonzero integral quotient;
reject it before calling the division theorem. A zero numerator gives the
zero quotient. The number of candidates and field extensions are charged.

Thus a polynomially small a cannot hide an exponential improvement merely
by moving from free E-factors to nonfree factors. The exhaustive native
enumerators above are written baselines, not executed by the supplied-order
tests. Finding an informative factor is not proof of classical hardness.

## 6. All Binary Automorphisms Also Have A Small-Diagonal Ceiling

Let W=[[x,u],[y,v]] be an integral automorphism with W^dagger H W=H.
Suppose W is outside M2(K). The first-column equation gives

    Norm(a*x+beta*y)+Norm(y)=a^2.

If y or z=a*x+beta*y fails to commute with alpha, that native map is the
required witness of degree at most a^2. The difficult-looking case is
when both commute, so x,y are in K but the second column is not.

In that case, put c=(x,y)^T and, inside the COMMUTATIVE field K, set

    c_perp = (-beta*bar(x)-d*bar(y), a*bar(x)+bar(beta)*bar(y))^T,
    U = [c, (beta*c+c_perp)/a].

The first-column norm equation gives c^dagger H c=a, orthogonality to
c_perp, Norm_H(c_perp)=a, and det[c,c_perp]=a. Hence det(U)=1 and
U^dagger H U=H. U need not be integral; it is a comparison matrix only.
The H-unitary D=U^-1 W has first column (1,0)^T and therefore the form

    D = [[1, beta*(1-eta)/a], [0,eta]],  Norm(eta)=1.

Crucially the last row of U^-1 is (-y,x), with NO denominator. Thus

    eta=x*v-y*u

is an actual INTEGRAL endomorphism of E. If eta belonged to K, D and W
would also belong to M2(K), a contradiction. It is a noncommuting elliptic
unit, degree one, which the mandatory native unit baseline already finds.
There is no hidden norm-one rational map or uncharged division in this
case. automorphism_certificate checks both branches directly.

### Product Powers Do Not Evade The Ceiling

For A_H^s, use unique polarized decomposition. If A_H is indecomposable,
an automorphism permutes the s copies with H-unitary binary maps between
them. A block outside K invokes the preceding lemma.

If A_H decomposes into elliptic factors F1,F2 and one of its primitive
projectors is outside K, Section 2 already gives the stronger a^2/4 bound.
Otherwise both projectors commute with alpha, so alpha restricts to
endomorphisms alpha_i on Fi. Write u_i:E->Fi for restriction of the factor
projection to the first E coordinate. If a>=2, each u_i is nonzero: u_i=0
would force a*deg(v_i)=1. Its degree m_i lies between 1 and a-1.

Automorphisms of a product of principally polarized elliptic curves are
monomial in the elliptic factors, with degree-one isomorphism entries.
An automorphism outside the known quadratic algebra therefore has some
entry psi:Fi->Fj with alpha_j*psi != psi*alpha_i. The native composition

    gamma = u_j^dagger * psi * u_i

then fails to commute with alpha, since the nonzero u_i,u_j are invertible
in Hom^0. Its degree is m_i*m_j<=a^2. This is an existence argument for
the matched low-degree competitor; none of the unknown factors is given
to that competitor as advice.

When a=1, H is integrally equivalent over K to the standard product via
the known shear [[1,beta],[0,1]]. Every automorphism of its powers is thus
a conjugated monomial map. Any outside-K entry requires a noncommuting
elliptic unit, again of degree one. This handles the zero-projection edge
case rather than assuming all u_i are nonzero.

Consequently EVERY useful automorphism of A_H^s implies a noncommuting
endomorphism of E of degree <=a^2, independent of s. This does not cover
the dimension-16 additive-source polarization Z_beta, nor arbitrary
intermediate interpolation quotients: those are different objects, not
powers of this binary H. It is not a general no-go for geometric methods.

## 7. Basis Choice And The Actual Surviving Regime

Swap the two coordinates to get the analogous bound floor(d^2/4). More
generally, for any KNOWN integral invertible T in GL2(K intersect O), with
known integral inverse, replace H by T^dagger H T and P by T^-1 P T.
Membership in M2(K) is unchanged. Every small diagonal exposed this way
gives the same bounded-degree competitor. Constructing such a basis is
not assumed free; a certificate for one already found is enough.
For automorphisms of any product power, the corresponding ceiling is
min(a,d)^2, without the factor of four improvement specific to factors.

Consequences:

- H=[[2,pi],[-pi,(p+1)/2]] can yield useful elliptic projectors only if a
  noncommuting degree-one unit already exists. Native unit enumeration is
  the immediate baseline, regardless of the size of p.
- H=[[4,pi],[-pi,(p+1)/4]], when integral, requires a noncommuting map of
  degree at most four. Searching nonfree factors does not remove that cost.
- The previous a<=8 or a<=16 supplied form boxes cannot provide evidence
  of a major speedup even after all nonfree factors are added: degrees16
  or64, respectively, are already covered by native low-degree search.
- Automorphism enumeration of the same stabilized small-a forms does not
  repair the input-access problem: degree<=a^2 is a matched competitor.
- Large trace alone is not the right research parameter. Both diagonals,
  and the diagonals after any known cheap K-basis change, must evade the
  matched low-degree ceiling before this lead merits further effort.

This is NOT a no-go theorem for high-height families with large reduced
diagonals. It does not prove that they contain useful factors with any
particular probability. It does not cover different higher-dimensional
source constructions. No new successful family is
identified here, and no quantum receiver is justified by the deduction.

## 8. Adversarial Checks And Literature Scope

The proof was attacked at its former weakest point: a factor F not
isomorphic to E. All key expressions are correctly typed through
Hom(E,F), and the second proof uses the projector alone. A full-order
certificate does not authenticate native provenance; a geometrically
produced P and the native division checks remain separate requirements.

Exact controls include saturation of the bound at (a,m,degree)=(2,1,1)
and (7,4,12), an enormous off-diagonal coefficient with fixed a=2,
complementary projectors, coordinate swapping, zero m, rational false
projectors and compatibility with the earlier free-factor implementation.
Automorphism controls test both noncommuting first-column branches, the
integral unit phase when the first column is known, and bad unitary inputs.
Positive fixtures have a SUPPLIED factor basis and known noncommuting maps.
They are algebra checks, not a newly found native family. No nonfree
geometric factor was computed; coverage of nonfree factors is deductive.

A fresh primary-source search also found
[Viehmann's generic-automorphism theorem](https://arxiv.org/html/2603.06033v2).
It does not establish useful-symmetry probabilities for this project.
Our prime-to-p quotients of E^g preserve the p-divisible group and have
a-number g, while generic supersingular statements concern a different
moduli regime. The previous forced-Q8 family already shows why one cannot
substitute a generic +/-1 assertion for analysis of these specific queries.

Next substantive work must exhibit a legal family with LARGE relevant
diagonals, a reason for noncommuting factors, and a matched native cost
analysis, or pivot to a different input-access mechanism. Merely adding
nonfree enumeration to the old tiny form boxes is now explicitly cut.
