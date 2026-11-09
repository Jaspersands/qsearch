# Function-field relations by finite specialization and short-lattice recovery

2026-11-06. Written bounded-error quantum composition; independent core and
full resource and classical-comparison reviews accepted.
No novelty, separation or full quantum execution claim.

## Native problem and selection

Input: binary prime p; indeterminates T=(T_1,...,T_s); a MONIC irreducible
f(Y) of numerical degree delta>=1 over F_p(T); and k>=1 NONZERO elements
u_i of F=F_p(T)[Y]/f, each represented in the basis1,...,Y^(delta-1).
Coefficients are explicit rational functions: numerator and nonzero denominator
polynomials are given as sparse lists of monomials with BINARY exponents.
The f coefficient list charges numerical delta; s,delta,k may ALL grow.
Only parameters actually occurring in the input are retained; unused named
parameters can be dropped, so their count is bounded by the input length.
No inverses, factorization, constants, divisors or relation lattice are given.
Irreducibility and nonzero elements are promises, not claimed to be certified.
Output a Z-basis of Lambda={e in Z^k:product u_i^e_i=1}, with failure<=eta.
Desired clock is polynomial in actual input BIT length and log(1/eta), even
when the numerical degrees in T are exponential in that input length.

This is an explicit symbolic-algebra input, not a hidden character oracle.
Extension-field evaluations are computed from the supplied formulas; they
are not supplied for free by an unknown function. It is not an algorithm
converting an arbitrary affine-ideal presentation into this field format.

Corpus been-tried and baseline lookups preceded this proposal. Earlier
independent comparisons rejected explicit-form Hessian/QFT under its generic
conditions, inaccessible torsion alignment, and Galois factor-degree readout
as new operations. The actual Miasnikov--Ushakov2610.27250v1 fixed-m,fixed-k
relation primitive is a constructive lead, but enumerating exponent vectors
or computing growing-variable Groebner bases is not affordable here.
The proposed new operation uses ONE large finite specialization and LLL,
with a uniform short-relation bound. It bypasses divisor computation and
the characteristic-p failure of logarithmic derivatives.

Strong classical comparators include Kreuzer--Walsh2307.09394 Algorithms2.6
and2.10 (valuation methods) and the SAME finite-specialization algorithm if
its finite-algebra relation step is supplied classically. The corpus names
LLL: it is used as a classical part of the algorithm, not claimed difficult.
Finite-field DLog is already a special case via constant inputs. No classical
lower bound follows. Quasipolynomial fixed-characteristic DLog must be
included in any parameter comparison; no general exponential separation.

## 1. A polynomial-bit bound on a full true relation basis

Let beta>=1 bound the numerical total T-degrees of all numerator/denominator
polynomials. Let L be the number of coefficient denominators (repetitions
may be retained). Form a PROOF-ONLY affine presentation by adjoining one
inverse variable for each denominator, Y satisfying the cleared monic f,
and one inverse variable for each u_i. This is a DOMAIN: localize F_p[T],
use monicity and irreducibility of f, then localize the nonzero u_i. Its
fraction field is F. No expanded inverse polynomial is needed.

The presentation has

 m=s+1+L+k,       D=max(2,beta+delta+2)

as valid variable/degree bounds; the u_i and their inverse variables have
degree<=D in it. Proposition3.1's proof in2610.27250v1 gives a basis of
Alg={e:u^e algebraic over F_p} with infinity norm<=B0, where

                         B0=k!*D^((m+1)k).                    (1)

This NUMERICAL bound is uniform in m,k: the proof bounds divisor valuations
by D^(m+1), then uses determinant/HNF bounds. Only the paper's ENUMERATION
algorithm needs fixed m,k. No valuation or normalization is computed here.

The constant field is F_(p^c), where c<=delta: F_(p^c)(T) embeds into F and
has degree c over F_p(T), which is linearly disjoint from the finite constant
extension. This remains valid for inseparable f. The image of Alg under
u^e therefore has size h<=p^delta-1. The kernel Lambda has index h in Alg.
A triangular HNF basis of the corresponding index-h sublattice of Z^rankAlg
has entries<=h; lifting it through an Alg basis yields a Lambda basis with

                         ||b_i||_infinity <= B=k*B0*p^delta.  (2)

Lambda need NOT be saturated. Bound (2), including torsion, is essential.
Although beta,B0,B can be huge numerically, their binary lengths are
polynomial in the actual sparse input. Neither the affine presentation nor
any large basis power is expanded by the algorithm.

## 2. The precise finite specialization and failure bound

Set the integer Euclidean cutoff

                         R=2^k*k*B.                           (3)

Let G(T) be the FORMAL product of the L coefficient denominators and set

 H=L*beta,  J=delta^2*(H+beta),  C=(k+2)*J,
 W=H+k*J,  Z=W+(2R+1)^k*delta*C*k*R.

G is not expanded. Choose a>=1 with Q=p^a >= 8*Z/eta, and construct F_Q.
Every quantity has polynomial binary length, so a and logQ are polynomial
in input size and log1/eta. Choose t uniformly from F_Q^s. Evaluate every
input numerator/denominator using binary powering. ABORT on a zero input
denominator. Form the explicit finite ring

                         B_t=F_Q[Y]/f_t(Y).

It has dimension delta and canonical coefficient encodings, even if f_t is
reducible or inseparable. Evaluate all u_i; check gcd(u_i(t),f_t)=1, ABORT
otherwise, and compute their inverses by finite polynomial Euclid. No
factorization of f_t or rational-function inverse advice is required.

Here is a simultaneous proof against ALL false relations of size<=R.
In the generic field F, the multiplication matrix M_i of u_i in the Y-basis
can be written A_i/G^delta, where A_i has polynomial entries of degree
<=delta*(H+beta). This follows by expressing M_i as a degree<delta polynomial
in the companion matrix of f and clearing denominators. Thus det(A_i) is a
NONZERO polynomial of degree<=J, since u_i is nonzero in a field. The bad
input/finite-unit event lies in G*product_i det(A_i)=0, of degree<=W.

Use the common formal denominator G^delta*product_i det(A_i) for every M_i
AND M_i^(-1). The adjugate formula bounds every numerator and this denominator
by degree<=C. For e with ||e||_infinity<=R, product M_i^e_i-I has a common
numerator matrix of degree<=C*k*R. If e is NOT a true relation, multiplication
by u^e-1 is invertible in the GENERIC field, so its numerator determinant is
a NONZERO polynomial of degree<=delta*C*k*R. At a specialization where this
polynomial is nonzero, e cannot become a false relation (indeed its difference
from1 is invertible). This proof constructs no exponent-sized products.

There are at most(2R+1)^k integer vectors to consider. Schwartz--Zippel and
a union bound give

 Pr[bad denominator/unit OR some false relation ||e||_infinity<=R]
       <= Z/Q <= eta/8.                                       (4)

No independence between the events is used. This includes all coefficient
specializations, not merely closed points of the original affine variety.
The ring B_t keeps the full degree-delta quotient, so no rational-point
search, root selection or normalization advice occurs. True relations are
preserved by the localization homomorphism on every accepted specialization.
Equation (4) is an algorithmic bound, not a theorem inferred from controls.

## 3. Pay the finite relation lattice coherently

The unit group B_t^* acts faithfully by multiplication on its delta-dimensional
F_Q vector space, hence embeds in GL_delta(F_Q). A known common period is

 N=|GL_delta(F_Q)|=Q^(delta*(delta-1)/2)*product_{j=1}^delta(Q^j-1).

Its binary length is O(delta^2 logQ). For EVERY accepted input the map

 phi:(Z/NZ)^k -> B_t^*,   e -> product_i u_i(t)^e_i

is an explicitly computable homomorphism hiding its exact kernel. Canonical
finite-polynomial coefficient labels distinguish group elements. The circuit
precomputes powers u_i(t)^(2^j) and their inverses classically, and implements
controlled multiplication by known units, an invertible linear map on B_t.
This pays coherent evaluation with polynomial gates/workspace; no QRAM,
hidden inverse or source-state reflection is supplied.

Apply the standard finite abelian HSP algorithm, with approximation and
failure budget paid, and pull its kernel back to Z^k. Equivalently take
O(k logN+log1/eta) uniform annihilator samples and solve their congruences by
integer linear algebra. Proper subgroup enlargement has conditional chance
>=1/2 and at most log2|G| enlargements are needed; a bounded sampling budget
pays completeness, not just validity of a returned generator list.
The result is the FULL-RANK lattice

                         M=Rel_(B_t)(u_1(t),...,u_k(t)).

Actual2610.27250v1 Lemma4.2 supplies the same finite-ring HSP principle with
individual order finding; the known GL period above avoids that preliminary
step. The finite ring may have nilpotents. The subgroup operates on units;
nonunits elsewhere in its coefficient representation cause no oracle issue.

## 4. LLL recovers the exact, possibly nonsaturated relation lattice

On event(4)'s complement, Lambda is contained in M and every vector of M
with Euclidean norm<=R lies in Lambda. A basis of Lambda has Euclidean norms
<=sqrt(k)B by(2). Let r=rankLambda and run3/4-LLL on a full basis of M.
For i<=r, the successive-minimum/LLL bound gives

 ||b_i|| <=2^((k-1)/2)*lambda_i(M)
          <=2^((k-1)/2)*sqrt(k)*B < R.

Thus the first r vectors lie in Lambda and span its rational span. Because
they are the first vectors of a FULL Z-basis of M, they generate
M intersect span_Q(Lambda). This lattice contains Lambda, while those
vectors already lie in Lambda; equality follows. Every later LLL vector
has norm>R, or it would be an independent vector in Lambda. Output the
short prefix and put it in HNF if a canonical basis is desired. Do NOT
saturate it. This also handles r=0 and r=k.

The lattice M contains N Z^k, so it has a polynomial-bit basis obtainable
from the HSP congruences. LLL is polynomial in that bit length and k.
This is a separation by CHOSEN field size, not an assumed LLL heuristic.

## 5. Whole-input clock, classical comparison and falsifiers

Field construction uses bounded randomized irreducible-polynomial search
with deterministic finite-field irreducibility testing: for a>1 a uniform
monic degree-a polynomial is irreducible with probability>=1/(2a), so
O(a*log(1/eta)) trials suffice; a=1 is immediate. Testing uses polynomial
modular powering and the prime divisors of the NUMERICAL polynomial-size a.
Uniform base-field samples use capped rejection of binary integers >=p;
each trial accepts with probability>=1/2. Charge the total number of
coefficient samples and all their failure probabilities. Allocate at mosteta/8 each to
field construction, uniform sampling, specialization, HSP sampling and total
compiled-QFT error. All arithmetic, extension degree a, finite labels,
periodN, sample counts, HNF/LLL sizes and binary powering are polynomial in
the ORIGINAL bit input and log1/eta. No loop scales with numerical beta orR.
On all good events the returned lattice is EXACT. This is a bounded-error
claim; the final completeness event is not certified by checking a few rows.

Classical source-first attack: for delta1 rational functions, direct polynomial
factor valuations give all nonconstant constraints, and only finite constant
relations remain. Existing Kreuzer--Walsh Algorithms2.6/2.10 are retained
under their actual costs; explicit sparse input does not make dense high-degree
factorization automatically polynomial in bit length. A classical finite relation step can use residue-field relations and
nilpotent lifts; its exact order/primitive-generator requirements must also
be paid. A finite-field DLog theorem alone is not automatically a runtime
bound for the whole finite-ring relation algorithm.
Actual Kleinjung--Wesolowski1906.10668v2 Theorem1.1 gives finite-field DLog
expected time(p*n)^(2log2(n)+O(1)); fixed p is quasipolynomial in n. A general
classical polytime relation algorithm would in particular solve finite-field
DLog, but that is not a hardness proof, nor a claim beyond Shor's primitive.

Cheapest prespecified control: F_5(T), u=(T,2*T^2,2). True Lambda is
{e1+2e2=0, e2+e3=0 mod4}, a NONSATURATED rank2 lattice. Evaluate at a
primitive element of F_(5^5), compute the small finite relation lattice
CLASSICALLY, and run LLL. For a tight independently proved B=4, cutoff96
is below every false-relation norm, since a false relation has
|e1+2e2| >=(5^5-1)/4=781. A legal bad specialization T=1 must expose a
short false relation. This finite control does not use the large theorem
field-size bound, simulate HSP, or prove the asymptotic result.

Separate source guards: dlog(T^p)=0 does not imply algebraicity. Also
f=Y^p-T specializes to a nonreduced ring; its finite unit computation cannot
silently assume a field. No broad scan or receiver infrastructure is queued.
## 6. Executed controls and review status

The exact Sage control in
`audits/controls/function_field_specialization/native_controls.py` passed;
its JSON records the following outcomes. Direct polynomial valuation and
constant-log baselines ran first. At the primitive F3125 point, the short
LLL prefix is(-2,1,-1),(-2,1,3), generating EXACTLY the true lattice with
basis(-2,1,-1),(0,0,4), without ambient saturation. The remaining LLL vector
is(157,312,-1), above cutoff96. The legal point T=1 instead produces the
false short vector(1,0,0), whose generic product is T, not1.

In F3[Y]/(Y^3-1), the class of Y has order3 and Y-1 is a nonzero nilpotent;
projection to the only root1 would incorrectly erase that constraint.
The full quotient and known GL3(F3) period11232 preserve it. The controls
use small CLASSICAL discrete logs, no quantum HSP, and a control-only tight
bound. They do not execute the theorem-sized algorithm or prove its clock.

Independent Codex reviews accepted the source-uniform basis bound, exact
LLL recovery, and FULL finite-source/resource proof at the native scope. Parent checked
the matrix/adjugate bounds and source proof directly. Claude Opus/high run
`audits/claude_runs/2026-11-06-function-field-specialization-opus/` ended
`empty_response`, stop reason `refusal`, without a research report. It has
no findings or acceptance weight, and was not retried. Estimated usage is
$0.047964, not an invoice or account balance.

## 7. Classical counterpart: pay generators and nilpotents

The finite-ring relation operation reduces, with randomized polynomial
overhead, to finite-field DLog even if the DLog routine promises only a
PRIMITIVE base. Integer factorization of field group orders is unnecessary.
Here is the missing generator test, independently checked by Codex.

For a finite field E with M=|E|-1, sample g uniformly in E^*. For each of t
independent challenges, privately choose r uniformly from[0,M), give the
DLog routine ONLY(g,g^r), and require its returned exponent x to equal r
modulo M. Reject the candidate on timeout, invalid output or mismatch.
The DLog routine cannot see r or share its random seed. If g is primitive,
a correct DLog answer is uniquely r. If g has order d<M, conditional on
g^r and ALL routine randomness, r has M/d equiprobable preimages; each
challenge passes with probability at most d/M<=1/2, even if the routine
behaves arbitrarily outside its promise. No successful-call postselection
is used: every failed challenge rejects the candidate.

An elementary bound suffices for generator density. If M has v distinct
prime factors, the j-th is >=j+1, so phi(M)/M>=1/(v+1)>=1/(1+log2 M).
The case M=1 is trivial. If T_D is the expected clock to a correct answer on promised primitive-base
DLog inputs, cap
each challenge at4*t*T_D. A primitive candidate survives all challenges
with probability>=3/4 by Markov and a union bound. Try
L=O((1+logM)*log(1/epsilon)) candidates and take
t>=ceil(log2(2L/epsilon)). The probability of accepting any nonprimitive
g is <=L*2^(-t), and exhaustion is <=epsilon/2 for a sufficient constant.
Thus a correct primitive generator is obtained with polynomial overhead
in logM and log1/epsilon, using the promised DLog clock. This is a
bounded-error construction; it does not deterministically certify primitivity.

Factor f_t over F_Q by standard randomized polynomial-time polynomial
factorization, retaining multiplicities. In each residue field
E_j=F_Q[Y]/h_j, compute a primitive generator as above and logs of all
u_i. Integer congruence kernels give M_0, the full lattice of exponent
vectors whose image is1 in every residue field. There are at most delta
factors, each degree<=delta. For each subsequent DLog at an accepted
primitive base, cap an independent attempt at4*T_D, check its output, and
retry O(log(number_of_calls/epsilon)) times before ABORT. A good attempt
finishes with probability>=3/4. This pays confidence logarithmically;
using a single Markov cap T_D/epsilon would NOT give the stated clock.
Polynomial factorization is likewise verified by product/multiplicity and
irreducibility tests, with bounded attempts and logarithmic amplification.
Distribute the confidence budget over the polynomially many calls.

Let J be the nilradical of B_t, generated by product_j h_j modulo f_t.
It satisfies J^delta=0. Suppose a current exponent lattice M_r maps into
1+J^r. The map w -> w-1 mod J^(r+1) is a homomorphism into the explicit
additive F_p-vector space J^r/J^(r+1), because2r>=r+1. For a basis of M_r,
compute its finite-ring unit images by binary powering, build that vector
map, and take its INTEGER congruence kernel modulo p. Lift through M_r
and HNF-reduce. Starting at r=1 with M_0, at most delta-1 steps produce
the EXACT relation lattice in B_t. Every intermediate lattice contains
the true finite relation lattice, whose index is <=|B_t^*|<=Q^delta;
HNF therefore keeps polynomial bit size. No numerical exponent expansion,
integer factorization, chosen root, or discarded nilpotent is hidden here.

Invoking the actual Kleinjung--Wesolowski1906.10668v2 Theorem1.1, the
residue fields have degree n=a*deg(h_j)<=a*delta over F_p, and DLog costs
expected(p*n)^(2log2(n)+O(1)). The reduction above supplies the formerly
missing generator/order and nilpotent steps. For FIXED p the WHOLE
function-field relation algorithm therefore has a bounded-error CLASSICAL
quasipolynomial clock in the original sparse input and log1/eta. The
quantum clock is polynomial. For variable p, keep the actual DLog bound;
there is no general classical polynomial-time claim, exponential-separation
proof, or new quantum primitive beyond finite abelian HSP.

The precise primitive-level classification is randomized polynomial-time
Turing EQUIVALENCE with finite-field DLog. The forward reduction is Sections2,
4 and7 with polynomial-size fields and polynomially many oracle calls.
Conversely set s=0, use the explicit finite-field presentation, and supply
(g,h) with h in<g>. Projection of Rel(g,h) onto its second coordinate is Z,
since some relation(x,-1) exists. Extended gcd of the second coordinates of
a complete returned basis constructs such a relation, yielding g^x=h;
reduce x modulo the known ambient field-group order if desired. This
deterministic extraction retains arbitrary-order bases and costs polynomial
bit time. The equivalence establishes neither a classical lower bound nor
a new quantum primitive beyond finite-field DLog. It also preserves fixed p.

The classical theorem's statement and descent interface were read from the
actual PDF; its full proof is invoked as published, not independently
reproved. Excerpts, URL and hash are in
`audits/claude_inputs/2026-11-06-function-field-relations/classical_dlog_*`.
Kreuzer--Walsh's additional Derksen--Jeandel--Koiran citation was located,
but an accessible full source was not obtained in this bounded pass; its
exact overlap remains unchecked. Novelty is explicitly UNKNOWN.

Section7 is closed after independent review and the explicit verified-restart
clock repair. Next hard work is independent direction selection. No new quantum implementation, parameter
sweep, CLI, registry, website or generic subsystem is queued.
