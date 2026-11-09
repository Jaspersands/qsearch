# Reduced norm witnesses through a prescribed splitting field

7 November 2026. Reviewed WRITTEN constructive composition; field, actual
compact-source and final integrated reviews complete. No human/formal
verification, novelty, separation, integral/short/expanded solution or quantum
execution is claimed.

## Selection, native question and baselines

Start from STATE/TRAPS after Relative Norm Tensor Support. Corpus been-tried
and baselines checked. Integral matrix similarity is already covered by BHJ
Cor9.16, with the repository's expanded-output counterfamily and compact
residue interface retained. Curve zeta computation is already covered by
Kedlaya's growing-genus theorem. Neither is admitted as a new candidate.
Arbitrary CSA minimal modules remain unpaid; splitting A tensor A-op alone
returns a regular module. The route below requires only a regular module for
a different native output, whose search problem has independent arithmetic
value. It does not extend the previous relative norm solver or use that solver.

Input: growing-degree number field K, explicit compatible field/maximal-order
coordinates; a central simple K-algebra A of dimension n^2 by structure
constants and identity, n growing; expanded a in K; failure target eta.
Output NO or x in A with Nrd(x)=a. Positive coordinates are compact
arithmetic circuits in the explicit canonical format below, with a deterministic
classical construction certificate. Expanded coordinates and arbitrary circuit
identity checking are not part of this output contract. All input and circuit sizes are charged.
No splitting field, maximal subfield, division presentation, maximal A-order,
unit/class group, local invariant list or target element is supplied.

Target: bounded-error quantum polynomial BIT time under explicit GRH, using
known Kutas--Montessinos split-algebra computation and ordinary arithmetic.
This is a search target, not a claimed new quantum decision algorithm.
Hasse--Maass--Schilling ALREADY gives a classical existence criterion: a!=0
must be positive at every real place where A is nonsplit. Zero returns0;
n=1 returns a. Classical splitting, class/unit arithmetic and, for n=2,
quadratic-form/conic algorithms and the known KLPT methods under their actual
promises are the baselines. The intended asymptotic gain is polynomial quantum
BIT search by replacing the class/unit and split-algebra bottlenecks with their
known quantum algorithms; no uniform polynomial classical counterpart for
this full growing-degree contract was established here. This is not a proven
separation or a novelty statement. No classical lower bound follows from the
costs of the tested or cited competitors.

Actual Goldstein--Schacher1707.02498 Lemma1 gives the local-degree splitting
criterion, Theorem2 gives HMS, and the discussion on page3 gives embedding of
a degree-n splitting field and restriction of reduced norm to its field norm.
The proof below needs a quantitative construction, not that existence theorem
alone. Integral outlier results are not imported. Actual KM2307.00261v3
Fact2.1 pays maximal orders using factoring; Theorem4.13 applies to PROMISED
SPLIT algebras over growing number fields under GRH. Its stale abstract is
not the source authority. AMITSUR_ARITHMETIC_REUSE_AUDIT.md supplies the
reviewed compact cochain-to-matrix-map interface.

## 1. A polynomial set containing finite ramification

Construct any explicit Z-order Lambda in A: choose a rational basis starting
with1 and clear multiplication denominators by an integer M; the basis
1,M b_2,...,M b_R is closed under multiplication, R=[K:Q]n^2. Its ordinary
regular-trace discriminant delta is a nonzero integer of polynomial bit
length. Factor delta (charged quantum factoring), add rational prime2, and
decompose every selected prime in K using the supplied maximal order.

Justification: if p does not divide delta, the trace form of
Lambda/p Lambda is nondegenerate. Its Jacobson radical is in the trace
radical (every radical element times another element is nilpotent), so the
reduction is semisimple over F_p. Lift matrix units and finite-field primitive
elements over Z_p: the lifted corner has the same rank as the unramified
field order, and Nakayama gives equality. Thus the generic algebra is a
product of matrices over unramified local fields. In particular A is split
over every K-place above p. The full idempotent/corner/Hensel lifting proof
is in audits/reviews/2026-11-07-reduced-norm-field.md, Section1, and has been
checked independently. These lifts are proof objects; the algorithm computes
only the trace discriminant, not a noncommutative maximal order.

Real ramification can be read from the regular-trace quadratic form on A.
Over R its positive-minus-negative signature is +n for M_n(R) and -n for
M_(n/2)(H), up to a positive trace scaling. Indeed a quaternion diagonal
entry contributes(1,3), and each off-diagonal pair contributes(4,4).
Diagonalize over K and evaluate signs at its real embeddings with exact
algebraic-number algorithms. If a is negative at a nonsplit real place,
return NO by HMS. Fraction-free congruence diagonalization has polynomial-bit minors; exact
real-root isolation/sign evaluation is polynomial in the growing field degree
and expanded heights. Use K-regular trace here, distinct from the Q-regular
trace in delta. For a concrete size bound choose d_a>0 with b=d_a*a integral
and U_a>=1 an integer row-sum bound on its multiplication matrix. Every
conjugate of b has absolute value<=U_a, and its nonzero norm is an integer.
Thus every |sigma(a)|>=alpha=1/(d_a*U_a^([K:Q]-1)), a polynomial-bit positive
rational <=1. No numerical embedding gap is supplied.

## 2. Classical prescribed-constant finite-field irreducibility

For every finite field F_q, degree g>=2 and c!=0, a uniform monic degree-g
polynomial with constant c is irreducible with probability >=1/(3g).
Here is an elementary bound, avoiding a finite-field norm oracle.
The norm fibre for (-1)^g c in F_(q^g)^* has size H=(q^g-1)/(q-1).
For each prime ell dividing g, its intersection with the maximal proper
subfield F_(q^(g/ell)) has size at most

    ell*(q^(g/ell)-1)/(q-1).

The bad fraction is therefore at most

    sum_(ell prime|g) ell/(1+q^(g/ell)+...+q^((ell-1)g/ell)).

If g is prime this is <=g/(2^g-1)<=2/3. For composite g>=6, sum of distinct
prime divisors is <=g, and every denominator is >=q^(g/2)+1. The bound
g/(2^(g/2)+1) is decreasing for g>=6 and equals2/3 at6. For g=4 the direct
bound is2/(q^2+1)<=2/5. Hence at least H/3 fibre elements have full degree.
Each monic irreducible accounts for g roots; H>=q^(g-1), giving1/(3g).
For g=1 the linear polynomial is automatic. Test irreducibility classically
by Frobenius modular powering. O(g log(1/eta)) capped trials suffice.

This is a quantified proof with an analytic tail, not a finite-size inference.
The independent field review checks the norm-on-subfield exponent and all
small cases; no quantum discrete log is needed for this step.

## 3. Local irreducible polynomials with exact constant

For each selected finite K-place q, let pi have valuation1 and let
v=v_q(c), c=(-1)^n a. Set k=floor(v/n), v0=v-kn in[0,n-1], c0=c/pi^(kn).
Let g=gcd(n,v0), e=n/g, h=v0/g, with g=n when v0=0. Choose over the residue
field a monic irreducible degree-g polynomial with constant c0/pi^v0 mod q.
Lift its coefficients u_j to O_(K,q), using u_0=c0/pi^v0 EXACTLY, and put

    P0(X)=sum_(j=0)^g u_j*pi^(h*(g-j))*X^(e*j),   u_g=1.

An elementary proof replaces an imported Newton theorem. Every root beta
has valuation v0/n: smaller valuation makes the leading term uniquely least,
larger makes the constant uniquely least, so neither can cancel. The reduced
denominator forces ramification index at least e. The unit beta^e/pi^h
reduces to a root of the chosen degree-g irreducible polynomial, forcing
residue degree at least g. Hence [K_q(beta):K_q]>=eg=n, proving irreducibility,
including wild characteristic and v0=0. The same proof applies to coefficient
perturbations strictly above the side's heights.
Set Pq(X)=pi^(kn)*P0(X/pi^k); it is monic with exact constant c.
All powers have polynomial NUMERICAL exponents: write c=b/d with b integral,
d a positive integer. The valuations of b and d are bounded in magnitude by
log|Norm(b)| and [K:Q]log d, each polynomial for this EXPANDED input. Successive
ideal membership gives these valuations. A basis element of q outside q^2
is a small uniformizer pi, without a principal-generator oracle.

To reduce u0=c/pi^v modulo q, do not invert a possibly nonunit rational
denominator. Write the expanded u0=b'/d' with b' integral. For t=v_q(d'),
we also have v_q(b')=t. Solve d'*z=b' modulo q^(t+1), z in O_K, using HNF
with preimages. Since d'O_K+q^(t+1)=q^t this works, and z is the desired
residue. This reuses the exact division lemma in
COMPACT_RESIDUE_CONDUCTOR_DECISION.md. All t and expanded coefficients have
polynomial size. Arbitrary succinct local data with binary HUGE valuations
are not covered by this argument.

Write b_(q,i) for each free coefficient of Pq. Its Newton-line height is
v*(n-i)/n. Let ell_q=1+|v|, strictly above every such height. Clear all local
coefficient denominators by a positive integer D, set E_q=v_q(D)+ell_q and
I=product_q q^E_q. Solve N_i=D*b_(q,i) mod q^E_q by ideal CRT and choose
integral HNF-reduced N_i. Their conjugates are bounded by a polynomial-bit
integer U, using row-sum norms of their multiplication matrices.

Let M=Norm(I), so M O_K is contained in I. Choose an integer s of polynomial
NUMERICAL size with 2^s>=max(1,4n*U/alpha), and set

    T=1+M*2^s,   t_i=N_i/(D*T),
    P(X)=X^n+sum_(i=1)^(n-1) t_i X^i+c.

T is positive, congruent1 modulo I, and a unit at every selected q. Since
D*b_(q,i) is integral,
N_i-D*T*b_(q,i)=(N_i-D*b_(q,i))+(1-T)*D*b_(q,i) belongs to q^E_q.
Therefore v_q(t_i-b_(q,i))>=ell_q. Every local irreducibility certificate
survives. At every real embedding |sigma(t_i)|<=U/(D*T)<=alpha/(4n).
All D,M,T and coefficients have polynomial BIT length. There is no loop up
to T, no approximate constant term and no uncharged weak-approximation oracle.

At every real nonsplit place, n is even and a>0. For real t, the free terms
have absolute sum <=alpha/(4n)*sum_(j=1)^(n-1)|t|^j; separately |t|<=1 and |t|>=1
show P(t)>0 at this bound. Thus P has no real root there. At every
selected finite place it is irreducible of degree n, so is globally irreducible
(prime2 ensures a selected place even if delta=1). F=K[X]/P has degree n
and splits A by the actual local-degree criterion. Its generator theta has
Norm_F/K(theta)=a. No normal closure or supplied maximal subfield was used.

## 4. Recover an element using a regular module

Compute a compact split map rho:A tensor_K F -> M_n(F), using the EXISTING
KM theorem under GRH, with Fact2.1 paying the newly constructed F's maximal
order. Let V=F^n as an A-module. dim_K V=n^2=dim_K A. Since A is simple,
all its finite modules are sums of the same simple module, so V is isomorphic
to the REGULAR left A-module. This does not construct a global minimal ideal.

Choose w in V. Let B_w have columns rho(b_i)w in K coordinates, for the input
K-basis b_i of A. Its determinant is a nonzero polynomial of degree n^2 in
w's n^2 coordinates. Sample those coordinates from an integer grid of size
4n^2; Schwartz--Zippel gives success at least3/4. Use capped retries.
For invertible B_w define

    x = B_w^-1(theta*w),

interpreting this vector as coordinates in A. The scalar theta operation on
V commutes with A, so under the regular-module identification it is RIGHT
multiplication by x. Its K-characteristic polynomial is P^n, whereas regular
right multiplication has characteristic polynomial redchar_x^n. Both roots
are monic degree-n polynomials, hence redchar_x=P and Nrd(x)=a.

## 5. Exact compact construction certificate

The certificate verifies the expanded Amitsur presentation, rather than
accepting an arbitrary claimed rho. Let H be KM's auxiliary rank-n etale
algebra over the prescribed F, U=H tensor_F H and W=H tensor_F H tensor_F H.
Their absolute dimensions are [K:Q]n^2, [K:Q]n^3 and [K:Q]n^4 respectively.
The verifier checks compatible expanded F/K data, irreducibility of P (by
ordinary polynomial factoring/LS1.10), theta and its norm a. No maximal-order
claim for F need be verified classically. Its construction during search is
paid by KM Fact2.1; field arithmetic/certificate uses checked power bases.

Check expanded H is etale, and the expanded invertible map Phi:U->A tensor F
intertwines the c-twisted product with the input product on basis pairs. c
and all maps have polynomial coordinate heights. This checks the link to
A's ACTUAL structure constants, not just a Brauer-class label.

Represent alpha as a product of SMALL expanded U-unit atoms to binary
exponents. Lift a component-field atom u using 1-e+e*u, not the nonunit e*u.
Test atoms are units and precompute their SMALL expanded inverses for negative
exponents. Apply the three expanded insertion maps into W. Recompute the
FULL LS1.11 relation kernel on the mapped small atoms and c, and verify the
signed exponent relation c=delta(alpha). Do not trust an asserted relation
basis. This is deterministic polynomial BIT arithmetic in an expanded
commutative algebra, not a relation oracle on compact sums.

With c_ijk=alpha_jk*alpha_ik^-1*alpha_ij, canonically build

    rho = trace_map o multiplication_by_alpha o Phi^-1.

The exact identity alpha_ij*c_ikj=alpha_ik*alpha_kj proves multiplicativity;
the untwisted map sends r tensor s to (z -> r*Tr(s*z)). Thus the compact rho
is an algebra isomorphism by a fixed algebraic identity and the checked
expanded Phi. This closes the homomorphism gate without general circuit PIT.
An arbitrary rho perturbed by a nonmultiplicative linear map is rejected by
the required syntactic reconstruction.

From the small integer w rebuild B_w, D_w=det(B_w) and its Cramer numerators
by canonical polynomial-size DIVISION-FREE determinant DAGs, such as
Berkowitz. No factorial Leibniz list or assumed pivot inverse is permitted.
A supplied modulus with valid exact rational reductions and a NONZERO
coordinate of D_w in the FULL K-algebra modulo that modulus proves D_w!=0
in K. A nonzero coordinate suffices; unit testing is required only if an
inverse is actually evaluated in the finite algebra. The field inverse can
also be compiled into the rational adjugate/norm circuit, whose denominator
is nonzero because D_w!=0 in the promised field K.

Finally rebuild and compare the submitted output DAG syntactically with the
Cramer construction. The exact cochain identity, expanded presentation,
nonzero denominator certificate and regular-module proof imply Nrd(x)=a.
The verifier never evaluates the enormous output, solves general additive
circuit equality, or trusts arbitrary rho/output circuits. Positive-certificate
soundness is unconditional under the native field/CSA input promises.

## 6. Height, prime and aggregate failure clocks

Expand the canonical B_w/determinant computation conceptually to a rational
scalar +,-,* DAG with H0-bit constants, including field tables, small inverses
and all binary-power gates. Let T0 count ALL scalar nodes, including rational
leaves and output slots, padded if necessary to dominate their counts.
T0,H0 are polynomial in the native
input and capped source output. Every unreduced numerator/denominator has
bit length at most B0=2^(T0+2)*(H0+1). This is an EXPONENTIAL expanded size;
only log B0 is polynomial, and only that is used to choose prime sizes.
For fixed w with D_w!=0, rational denominators and a chosen nonzero coordinate
numerator have at most (T0+1)*B0 bad rational prime divisors.

For error delta, choose

    b=2*(T0+ceil(log2(H0+1))+ceil(log2(T0+1))
           +ceil(log2(1/delta))+32).

The standard explicit dyadic prime-count bound makes a uniform b-bit prime
bad with probability<delta. Uniform integers and deterministic polynomial
primality tests give a capped O(b log(1/delta_gen)) generation clock. Conditional
on success the prime is uniform. Choose a FRESH prime after atoms and w are
fixed. Modular evaluation has polynomial BIT cost and successful nonzero
output is an EXACT certificate. No modular false-positive identity claim occurs.

Cyclic w succeeds with probability>=3/4. Set delta,delta_gen<=1/8; each
combined trial succeeds with probability>1/2. Cap at ceil(log2(4/eta))
trials, giving exhaustion probability<=eta/4. All bounds are uniform over
the finite w grid; never choose a new expression adaptively from its modulus.

Allocate eta/4 to support factoring/prime decomposition, eta/4 to all capped
local residual-polynomial trials, eta/4 to KM's expanded front end/maximal-
order/complete compact S-unit calls, and eta/4 to cyclic-vector/prime trials.
The source front end is polynomial-size expanded arithmetic; all its outputs
can be checked directly. Complete S-units under GRH ensure finding alpha. Explicitly retain the
small atoms of every compact U S-unit generator, including torsion. Map these
atoms into W by the three insertion maps; append expanded c, and compute the
full LS integral relation kernel. The binary exponent matrix E describing
delta of the U generators then yields the exact integer system
E*z-e_c in that kernel. Integer HNF with preimages finds z of polynomial bit
length when solvable. This is the small-atom implementation of KM's S-unit
coordinate step, not relations on compact sums or free logarithm inversion.
An incorrect/incomplete source cannot pass a false exact coboundary certificate.
Use the published adjustable completeness guarantee and distribute its budget
among the polynomially many component-field calls. Source/output size caps
and all finite random clocks are charged. ANY failure or exhaustion is ABORT,
not mathematical NO. NO is issued only by the exact classical HMS test.

## Decisive tests and next work

Cheapest failures: trace-discriminant support missing a ramified prime;
prescribed-constant irreducibles too rare; a wild Newton counterexample;
CRT/archimedean constraints requiring superpolynomial bits; treating a regular
module as minimal; left/right orientation; source unit expansion; or an
unpaid zero-test/verification oracle. Finite controls must include an actual
classical norm solver before any quantum implementation.

All three independent reviews are complete, read and integrated. The final
review required explicitly paying the small-atom/HNF SEARCH step and counting
all scalar DAG nodes in the modulus bound; both repairs are above. The
conditional written native search theorem is accepted within that scope.
No backend, sweep, adjacent integral/PIP extension or quantum execution is
queued. Independently compare native mechanisms for the next pass.

## Review, Claude dispositions and exact classical control

Completed and fully read independent reviews:
`audits/reviews/2026-11-07-reduced-norm-field.md` (field constructor) and
`audits/reviews/2026-11-07-reduced-norm-compact.md` (actual source and exact
certificate), and
`audits/reviews/2026-11-07-reduced-norm-composition.md` (full native theorem).
Parent independently checked the trace lifting, finite-field
count, root valuation/degree argument, denominator-adjusted CRT, and the
presentation/cochain orientation and circuit/prime clock.

Both Opus reports completed and were fully read. Local report estimate
USD0.258848: its elementary root-valuation/residue-degree proof and coefficient
precision are accepted after checking. Its expected-only Las Vegas wording is
replaced by the stated capped trials/ABORT; its granted valuation/uniformizer
operations are paid by actual global ideal arithmetic above. Its finite examples
are not theorem evidence.

Module report estimateUSD0.507716: regular-module and norm derivation accepted;
its missing homomorphism-interface warning is correct and resolved by the
expanded Phi checks and canonical trace/cochain construction. Its perturbation
rho->rho o tau falsifies an UNCHECKED arbitrary rho certificate, which is not
accepted here. Its blanket claim that exact certification requires general
circuit identity testing is rejected for this explicit proof-carrying format.
Its scalar-cochain type objection concerns using the prescribed F as though it
split nonsplit A over K: our scalar cochain is for the SPLIT A tensor F and
auxiliary H over F, as the actual KM source requires. The distinction is now
explicit. Its proposed randomized rho-free verifier is not used; its possible
compact theta case is outside our expanded constructed theta contract.
No source claim is imported from its unverified citations. No retry/live call.

`audits/controls/reduced_norms/control.py/.json` is PASS: actual PARI qfsolve
solves the Hamilton norm3 baseline; one exact NONDIVISION algebra M2(H),
F=Q(zeta12), theta=2+zeta12 with norm13, uses a fully explicit classical split
map as a control of the paid primitive's interface. Its regular module has
K-dimension16, while a proper left ideal has dimension8. The cyclic-vector
construction recovers reduced characteristic polynomial
X^4-8X^3+23X^2-28X+13. Transport agrees with RIGHT multiplication, not left;
regular characteristic polynomial is its fourth power. det(B_w) is nonzero
mod101. These are finite convention/interface checks, not execution of a
native quantum solver, not hidden splitting advice in the theorem, and not
an asymptotic proof from tests. No code change or broader rerun is queued.

Milestone: current STATE/title/Now/boundary row, four primary PDF hashes,
three closed reviews, exact control values/false gates, two completed Claude
reports and aggregate usage ledger checked. Scoped diff/whitespace PASS.
No full suite, control rerun, registry promotion, Git commit or balance claim.
The broader research goal remains active; this is a completed research pass.
