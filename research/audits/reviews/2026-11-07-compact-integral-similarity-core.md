# Compact integral similarity: closed core composition review

2026-11-07. Read STATE/TRAPS, the output-size note, and actual frozen BHJ
2202.03526v3 text: Theorem3.4, Lemma4.2, Lemmas6.2--6.3, Propositions6.4,
6.8,7.8,9.11--9.12, Theorem7.9, Algorithms8.3/9.13, and AppendixA.
Interpreter /opt/anaconda3/bin/python. No network, API, Git, control or
implementation. The proof below audits the proposed compact adaptation;
Corollary9.16 alone is not used to settle output representation.

**Disposition: CLOSED mathematical/resource composition, with the explicit
guards and representation below.** For arbitrary growing A,B in Mat_n(Z),
the existing complete compact number-field unit/PIP primitives yield the
requested GRH-conditional bounded-error polynomial-BIT algorithm
returning NO or a polynomial-size rational arithmetic DAG for an integer
unimodular C satisfying BC=CA. The construction also admits a deterministic
positive transcript check using the described small-atom ideal certificates.
NO/completeness retain the bounded-error guarantees of the primitives. The
GRH umbrella is conservative: the cited complete S-unit theorem itself is
not labelled GRH, and this implementation need not import a class-group call.
No polynomial expanded-witness, general arithmetic-circuit identity testing,
tuple-conjugacy, novelty, classical separation or execution claim is made.

## 1. Expanded input reduction and the section

First compute an expanded polynomial-height rational D with BD=DA, or
return NO. Let S=C_Q(B), Lambda=C_Z(B), H={C in Mat_n(Z):BC=CA}, and
I=H D^-1. Integer kernel computations give expanded bases of Lambda,H,I.
BHJ Proposition9.11, via rational module canonical form, constructs the
expanded quotient homomorphism

    rho:S -> S/J(S) = product_(i,j) Mat_(d_ij)(K_i),
    K_i=Q[x]/(f_i),   sum_j j*d_ij = multiplicity(f_i).

All these field, matrix and coordinate data have polynomial BIT size. This
specific centralizer construction supplies the Wedderburn coordinates; no
general CSA splitting map or supplied centralizer is assumed. Write
barLambda=rho(Lambda), barI=rho(I). Their expanded lattice bases are obtained
by integer normal forms after clearing the known rational denominators.

The surjective map of free abelian groups I->barI has a computable Z-linear
section. Find a preimage in I of each chosen Z-basis element of barI using
HNF/SNF, retaining the integer transformation matrices. For a compact E in
barI, its coordinates in this basis are fixed rational LINEAR forms in the
coordinates of E. Applying the stored preimages therefore gives a compact
alpha in I, without expanding those integer coordinates or testing a compact
sum. Integrality is the structural consequence E in barI, not a floating-point
rounding step. C=alpha D belongs to H exactly.

## 2. The only large values in maximal-order principalization

Work in a semisimple matrix component Mat_m(K) with expanded maximal order
M. Actual Lemma6.2 and CorollaryA.3 provide expanded polynomial-height S_0
with S_0 M S_0^-1=M_a,m and a Steinitz decomposition. In nice coordinates

    e11 M has row module O^(m-1) direct-sum a^-1.

For a full left M-lattice J compute

    e11 J = O w1 direct-sum ... direct-sum O w_(m-1)
            direct-sum b w_m,

where the row matrix W=(w_i) is expanded and invertible. The field ideal
b*a is principal precisely in the required Steinitz-class case. If a compact
gamma satisfies (gamma)=b*a, then

    beta_nice = diag(1,...,1,gamma) W,
    beta = S_0^-1 beta_nice S_0

satisfies M beta=J. This follows directly from the displayed row modules;
the full-idempotent/Morita correspondence for the nice order recovers the
whole left lattice. It also covers m=1. Thus beta is a short expression
P diag(gamma,1,...) Q after permuting the distinguished coordinate, with
expanded P,Q. The large principal generator is never expanded.

Likewise a central unit epsilon is lifted by Lemma6.3 as
S_0^-1 diag(epsilon,1,...) S_0. Complete unit generators need not be changed
into a numerically conditioned logarithm basis. The finite-group exponent
solution specifies epsilon as a binary power product of them. Roots of unity
must be included. All later entry expressions are polynomial-size sums of
known gamma/unit monomials with expanded coefficients, not unrestricted
compact matrices on which a new elimination algorithm is invoked.

## 3. Proper conductor, local adjustment and finite lifting

BHJ Section4/Proposition6.8 assume a proper full ideal f contained in
barLambda. If barLambda is already maximal, the literal central conductor
is the whole center and the quoted CRT construction has an empty prime set.
Handle that case directly, OR uniformly take

    g = 2 * central_conductor(barLambda,M),   f=g M.

The latter is proper in every component and still contained in barLambda.
Factoring the extra rational prime2 is harmless. This explicit guard also
avoids silently treating unit-ideal components as nontrivial finite rings.

Using Proposition6.8, compute expanded xi with

    X=barI xi subset barLambda,   X+f=barLambda.

These lattice equalities are themselves exactly checkable with expanded
HNF data. The beta used from this point MUST generate M X. One may recompute
it from expanded X or replace a previous generator beta_old by beta_old xi.
Keeping the old beta without this update is incorrect notation/logic.

The finite groups and the reduced-norm image in BHJ Steps8--10 are computed
from the explicit quotient rings, not enumerated element by element. Their
orders have polynomial BIT length. Actual Theorem8.4 reduces the operations
to the charged integer factorization, finite-field primitive-element/DLog,
unit-group and principal-ideal primitives. The finite exponents are binary.

After solving the finite norm equation, let a in (barLambda/f)^x and
u in M^x satisfy nr(beta*a)=nr(u) modulo g. Compute the residue
beta*a*u^-1 of reduced norm1. Actual Theorem7.9 lifts it to v in SL(M).
Sections7.1--7.3 give polynomially many elementary factors, with expanded
small representatives and the nice-order ideal corrections. Their product v
and inverse have polynomial expanded height: there are polynomially many
factors of polynomial height. No unit-group expansion occurs in this lift.

Put alpha_bar=(v*u)^-1 beta = u^-1 v^-1 beta. Then
alpha_bar mod f=a^-1, so alpha_bar belongs to M, its residue belongs to
(barLambda/f)^x, and barLambda*alpha_bar+f=barLambda. Also
M*alpha_bar=M*beta=M*X. Applying Lemma4.2 to X and to barLambda*alpha_bar
gives

    barLambda*alpha_bar = M*alpha_bar intersect barLambda
                        = M*X intersect barLambda = X.

Consequently

    E = (v*u)^-1 beta xi^-1

belongs to and generates the ORIGINAL barI. This proves the compact
membership/generation join without testing an equality of compact sums.

## 4. Local residue computation with nonunit compact leaves

Final-unit status does not make every compact leaf invertible modulo g.
Here is a complete local operation sufficient for this composition.
The power-product interface is already proved in
COMPACT_RESIDUE_CONDUCTOR_DECISION.md, Sections "Local Evaluation Without
Expanding Exponents" and "Division By A Nonunit Denominator". The
denominator-ideal formulation below is an equivalent formulation of that
reused result, not a newly discovered residue theorem.

For P|g choose expanded pi in P but not P^2 from a basis of P. For each
small expanded nonzero atom a, clear a small rational denominator d with
d*a in O. Norm(d*a) and d bound |v_P(a)| polynomially in the input bits;
Norm(a) alone is not sufficient because valuations can cancel there. Thus
u=a*pi^(-v) is an expanded polynomial-height P-unit, even at wild primes.
Compute the denominator ideal

    D(u)={b in O : b*u in O}

by lattice arithmetic. Since u belongs to O_P, D(u) is not contained in P;
a basis element b outside P therefore exists. Both b and b*u have
polynomial expanded height. Reduce u modulo P^A as (b*u)*b^-1, computing
the inverse with the Bezout identity bO+P^A=O.

For a compact monomial eta=product a_l^(e_l), compute the integer
V=sum e_l*v_P(a_l) in binary and exponentiate the unit residues in binary.
If V>=A the integral residue is0; if 0<=V<A multiply by pi^V. Neither a
large exponent nor a large total positive valuation becomes a loop bound.

For a finite sum whose term valuations are bounded below by -K, evaluate
pi^K times every term modulo P^(A+K), sum, and divide an expanded lifted
representative by pi^K using the same denominator-ideal procedure. The result
is well-defined modulo P^A. In this application K is polynomial: global
units have valuation0, gamma's valuations are those of its EXPANDED target
ideal, and all other coefficient denominators have polynomial height.
CRT combines the local residues. Ideal exponents A and the required K are
polynomial in the input bits, including ramification; no archimedean precision
or expansion of regulator-sized units is required.

One may equivalently fix a common rational denominator BEFORE evaluating
these sums. Choose denominators for the expanded coefficient matrices and
for the expanded fractional ideals (gamma), then multiply the required
polynomial number of them. Gamma occurs only to bounded degree in the
displayed beta/u expressions, and positive or negative powers of global
units remain integral. The common denominator therefore has polynomial BIT
length independent of the numerical unit exponents. At P enlarge precision
by its valuation, evaluate the integral numerator, and divide in the local
lattice; do not invert this possibly nonunit denominator modulo g.

On faulty primitive outputs, cap valuations/precisions by the proved bounds
and ABORT on inconsistency. A binary integer valuation must never be used
as an unbounded numeric precision request. Verifying gamma's ideal and the
unit memberships first supplies the required bounds directly.

## 5. Exact determinant character, without a compact determinant

For c in S, its determinant as a rational n-dimensional operator is

    det_Q(c)=product_(i,j) Norm_(K_i/Q)(det rho_ij(c))^j.       (1)

To see this, use the decomposition into (Q[x]/f_i^j)^(d_ij) and the f_i-adic
filtration. On each graded layer, cross-length homomorphisms are triangular
when lengths are ordered; maps from a shorter block to a longer block gain
the required positive f_i power. Each size-j diagonal semisimple block
rho_ij(c) occurs in exactly j layers. Taking determinants and field norms
proves (1). Equivalently the radical contributes only a determinant-one
unipotent correction. Formula(1) is independent of the chosen radical lift.

Apply (1) to the lattice-section lift alpha of E, and multiply by det D.
The norm of every central unit has absolute value1, and det v=1 in each
matrix component. Hence

    |det C| = |det D| * product_(i,j)
       ( |Norm(det beta_ij)| / |Norm(det xi_ij)| )^j.          (2)

Every quantity on the right has polynomial-height rational representation.
In particular, for a component Mat_m(K), after the local adjustment X is
integral and J=M X is an EXPANDED sublattice of M. Right multiplication by
beta has rational determinant Norm(det beta)^m, so

    |Norm(det beta)|^m = [M:J].

Compute the index with expanded lattice determinants and take its exact
positive integer m-th root. Correct principalization guarantees that root
exists. This also gives a direct check against a Steinitz determinant-ideal
calculation, without forming det(beta) as a compact sum. In the unadjusted
fractional-lattice version the same calculation uses a positive rational
index and exact rational root. Norm(det xi) and det D are expanded quantities.
Weighted products have polynomial bit length because j<=n and the number
of components is polynomial. Sign is unnecessary for GL_n(Z); if wanted,
compact atom norm signs and binary exponent parities determine it exactly.

The section proves C is an integer intertwiner. Therefore |det C|=1 is the
complete positive test. If barI is not principal, Theorem3.4(a) and
Proposition9.12 give NO. If it is principal but (2) is not1, Algorithm9.13's
proof applies to ANY section lift: either I is not principal, or every free
generator yields the wrong lattice index. If an integral similarity existed,
Theorem3.4(b) would make every such lift a generator and Proposition9.12
would force determinant absolute value1. Thus the final NO is sound on the
primitive-success event; no additional radical freeness oracle is missing.

## 6. Bit costs, verification and confidence

The current source interface is explicitly reused from
RELATIVE_NORM_TENSOR_SUPPORT.md, the complete compact S-unit passage and
its source ledger: actual Biasse--Song2510.02280v2 Theorem1, complete-
generation Theorem5/Proposition2, compact-output Proposition7 and Section8.2.
Use S empty for units, adding full torsion as in that note. For PIP take S
to contain the prime-ideal support of the expanded fractional target ideal,
obtain complete compact S-units, and solve the integer valuation system for
that target. A solution is the desired compact generator; an infeasible
system proves nonprincipality on the completeness event. Factoring the target
support is charged. This uses no extra class-group oracle, and no GRH
requirement is attributed to the source S-unit theorem merely because the
main contract conservatively retains GRH.

Let b be the total native matrix input length. All expanded algebras,
fields, orders, ideals, sections, local representatives and finite rings
above have dimension and coefficient bit length polynomial in b by the
specific cited constructions. Compact atoms have polynomial height and
exponents have polynomial binary length. Arithmetic in fixed explicit field
bases, followed by repeated squaring, gives a shared rational arithmetic DAG
of polynomial size for E, alpha and C. No expanded compact value, arbitrary
compact zero test, compact matrix pivot or logarithmic condition-number
assumption is used.

A positive transcript can verify compact ideal/unit assertions as follows.
Factor the integer norms and denominators of the SMALL expanded atoms
during construction, using the charged factorization primitive. Decompose
their principal ideals in the explicit maximal orders and retain checkable
prime-ideal factorizations. Atom norm/denominator bit lengths and the total
number of factors are polynomial. Complete rational-prime factorizations,
prime-ideal residue fields, ideal products and valuations are verified by
expanded arithmetic. For a prime ideal P, verify its rational residue
characteristic p is prime and O/P is an explicit field of order p^f; Norm(P)
need not be prime when f>1. For two local presentations a/b=a'/b', the
denominator-independence identity is a*b'=a'*b. The identity
(gamma)=target ideal and epsilon being a
unit are then exact binary valuation-vector equalities, never huge ideal
powers. These certificates establish membership, not completeness of a unit
generating list. Standard explicit maximal-order construction/certification
is charged; no maximal-order advice is input.

Expanded normal-form witnesses check the section and the original Hom
module. The finite congruence, elementary lift factors and verified
Steinitz/principal-ideal data prove E generates barI by Section3. Formula(2)
then proves unimodularity. The verifier checks this prescribed transcript
and its associated DAG, not an arbitrary externally supplied arithmetic
circuit. Positive soundness uses exact identities, independently of GRH;
completeness and negative decisions use the stated quantum primitives.

For confidence amplification, do NOT majority-vote noncanonical unit bases.
Independently repeat the unit primitive, verify individual unit memberships,
and take the UNION of valid generator lists. One complete successful run
makes this union complete, and valid additional units cannot enlarge the
group beyond O^x. The enlarged list has polynomial size with logarithmic
repetitions. For PIP accept any verified principal generator; a correct YES
instance supplies one on a successful run, and none exists on a NO instance.
Use the source success bound and logarithmic independent repetitions to
budget missed generators/completeness across the polynomial number of calls.

Factorization, finite-group logs and primitive-element candidates have
checkable outputs; apply bounded retries. Classical expected-polynomial
construction routines are independently restarted at constant-multiple caps,
with logarithmic repetitions and ABORT on exhausted clocks. Bound all output
sizes in advance and allocate the total failure budget eta across calls.
This yields a polynomial BIT clock with logarithmic confidence dependence;
no numerical finite-group exponent, regulator or expanded witness size is
charged as if it were small.

NO and ABORT are different outputs. A mathematically infeasible ideal/unit
valuation system, rational-similarity failure, local-module obstruction, or
the exact final determinant test gives NO on the source-completeness event.
A malformed primitive result, failed certificate, failed exact-root consistency
check or exhausted sampling clock gives ABORT (or a bounded retry), not a
mathematical NO. A valid but incomplete unit list cannot be detected merely
by checking its members; the union amplification bounds precisely that residual
source failure. Both ABORT and an incorrect NO count against the total eta.

## Final scope

The three substantive repairs are compact Steinitz/unit transport, normalized
local residue evaluation, and a structural section/determinant test. Together
they close the proposed single-matrix compact-output composition under the
stated existing arithmetic primitives. The source's Corollary9.16 is retained
as prior art; it is not read as permission to print exponentially large
conjugators. The repository's explicit 2x2 conductor family remains a decisive
counterexample to polynomial expanded output and is consistent with this DAG
endpoint. No broader simultaneous-conjugacy or arbitrary-CSA output claim
has been established here.
