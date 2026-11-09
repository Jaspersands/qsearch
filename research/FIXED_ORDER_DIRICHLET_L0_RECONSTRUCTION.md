# Fixed-Order Dirichlet L0 Reconstruction

Date: 2026-11-06. Status: WRITTEN bounded-error fixed-q composition under
GRH, with independent actual-note integration review accepted. One bounded
certified classical control is complete and parent-inspected.
Its valuation, field construction, non-PID Fitting reconstruction, fixed-field
generator reduction and unit/phase normalization have focused independent
review. No quantum execution, novelty, separation, or unrestricted polynomial-in-growing-q
claim.

## 1. Scientific Contract And Classical Admission

For EACH FIXED q=2^s>=4, input a binary prime p=1+qk with k odd, and
a public eta in F_p of exact order q. Define chi(a)=zeta_q^j iff
a^k=eta^j, where zeta_q=exp(2pi*i/q). Output the exact coefficients of
z=L(0,chi) in the power basis of F=Q(zeta_q). Character evaluation uses
modular powering and q comparisons, not an oracle. The target cost is
bounded-error quantum C(q)*polynomial(logp,log(1/error)) under GRH, with
a finite COMPUTABLE C(q), no q-dependent advice, and NO polynomial-in-q
claim. If k=1, compute the q-term rational sum directly; all integrality
statements below require k>1. The exact output has O_q(logp) bits.

The mechanism uses the class group WITH paid Galois action of the cyclic
degree-q subfield K of Q(zeta_p), a Fitting ideal identity, fixed-field
unit normalization from classical L1 estimates, and one quantum Gauss-phase
estimate to choose a root of unity. This would turn complete class-module
data into a concrete exact character sum of conductor p. It composes
existing primitives and proposes no new hidden-subgroup algorithm.

The corpus been-tried query (exact Dirichlet L zero values / class Fitting
ideal / units / closest vector / fixed character order) found no matching
mechanism; that is not a priority certificate. The baselines query names
classical relation collection/index calculus for class groups and units.
Those apply to the SAME K and action and are stronger comparators than
direct p-term summation. Louboutin2001 Section3.1 Theorems5/7 uses an
explicit truncation of order sqrt(p logp) here, with the root number
assumed known in Remark8. Chocian2026 Theorems3.1/3.2 give a p-sized
Fourier identity and an odd-auxiliary-prime congruence, not a polylog
computation. Section9 of QUARTER_FACTORIAL_QUARTIC_ARITHMETIC.md records
the actual-source checks and links. Tal2026 exact Jacobi sums are ALREADY
CLASSICAL polynomial(q,logp), and are used only as paid preprocessing.
Broader searches have not established priority or absence of a faster
classical exact L0 algorithm.
The hoped-for asymptotic improvement is polynomial-logp work in place
of those identified classical exact methods; this is not a claim about
optimal classical complexity. The parent checked Biasse--Fieker2014
Section1 and Theorem6.1: the fixed-degree index-calculus comparator has
a subexponential L_Delta[1/2,O(1)] bound under GRH AND additional
smoothness/relation heuristics, not under GRH alone. Here Delta=p^(q-1).
[Actual primary theorem](https://doi.org/10.1112/S1461157014000345).
That historical scope is now superseded as the strongest cited comparator:
deBoer--PelletMary--Wesolowski, *Rigorous Methods for Computational Number
Theory*, actual Theorem1.3, gives fixed-degree subexponential L_Delta(1/2)
class-group/compact-unit computation under ERH without those additional
heuristics. The varying-degree factors and source audit are recorded in
UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md Section4. No classical polylog
algorithm or separation follows from either bound.

First falsifiers: a hidden p-sized field description; incomplete class
relations; inverse-character or plus-projection error; a missing prime
over2; an incomplete unit subgroup; excessive numerical precision; or a
classical polylog construction of the same ideal. No quantum subsystem
is warranted before those checks.

## 2. Exact Integrality And The Entire Missing 2-Part

Put r=q/2, O=Z[zeta_q], lambda=(1-zeta_q). Let M_j be 1/p times the
sum of canonical residues a with chi(a)=zeta_q^j. Each multiplicative
coset has size k>1 and sums to zero in F_p, so M_j is integral. Since
k is odd, chi(-1)=-1, and

    M_(j+r)=k-M_j,
    z=-sum_j M_j*zeta_q^j=sum_(j<r)(k-2M_j)*zeta_q^j.       (1)

All coefficients are odd and have absolute value <k<p. Further,

    sum_(j<r) zeta_q^j = 2/(1-zeta_q),    v_lambda(2)=r.

Consequently v_lambda(z)=r-1 EXACTLY: the sum has valuation r-1 and
its difference from z belongs to2O. There is just one prime above2,
of norm2. No K^+ class-number ratio or additional quantum call is needed
to recover the removed2-part. This proof has independent review.

## 3. Paying For The Maximal Order And Galois Action

Let H=ker(chi). Define formal periods

    e_j=sum_(chi(a)=zeta_q^j) zeta_p^a.

This is a mathematical definition, NOT a p-term construction. The elements
zeta_p^a, 1<=a<p, form a full integral basis of Q(zeta_p). Its H-fixed
sublattice has the orbit sums as a full integral basis of O_K. They are
linearly independent, sigma(e_j)=e_(j+1), and 1=-sum_j e_j.

Let N_uv count t in F_p with chi(t)=zeta_q^u and
chi(1-t)=zeta_q^v. Extend ALL characters, including the trivial one,
by zero at0. Fourier inversion gives

    N_uv=q^(-2)*sum_(a,b=0..q-1) zeta_q^(-au-bv) J(chi^a,chi^b).

The exceptional values are J(1,1)=p-2; J(1,psi)=J(psi,1)=-1 for
nontrivial psi; and J(psi,psi^-1)=-psi(-1). Nondegenerate binary sums
come from Tal2026's CLASSICAL exact global reconstruction. Its actual
Section2.4 factorization, Lemma2.8 and Section3.1 Step2 apply to arbitrary
binary exponents u,v, without coprimality or u+v<q restrictions. The
latter restriction is used ONLY for the distinguished-p local UNIT
evaluation in the factorial addition chain, which is not imported here.
Tal's negative-power convention requires source root eta^(-1), with
compatible roots eta^(-q/m) at divisor m. The parent checked these source
passages; the local source is audits/sources/jacobi_classical_eccc_2026_211.txt.

Convert its product representations to exact coefficients using auxiliary
small-prime CRT, avoiding every denominator and norm of an individual
nonzero compact factor. These integers have total bit length polynomial
in the product encoding; hence only polynomially many primes are bad.
Test divisibility by gcd/modular arithmetic, without factoring the norms.
Modular inverses and binary powering handle negative exponents. The
nondegenerate sums have all conjugate magnitudes sqrtp; for power-of-two
cyclotomic bases, Fourier inversion bounds each integer coefficient by
sqrtp. Accumulating good-prime product greater than2*ceil(sqrtp) suffices.
Degenerate values are handled directly. Searching sufficiently many small
primes and all modular work has polynomial(q,logp) cost in the imported
product encoding. This does not assume distinguished-p unit evaluation.

The actual multiplication table in the integral basis is

    e_i*e_j=sum_l [N_(i-l,j-l)-k*delta_(j,i+r)] e_l.        (2)

Indeed the zero sum of the two exponents contributes k exactly when
j=i+r; replacing that rational constant using 1=-sum e_l yields(2).
All structure constants have O(logp) bits. Independence of the periods
makes the q conjugates of e_0 distinct, so e_0 is primitive. Its
multiplication matrix gives its degree-q defining polynomial, and rational
linear algebra converts the known maximal integral basis to its power
basis. Coefficients and transition matrices have polynomial bit size for
fixed q. Thus field, maximal order and sigma are explicitly available
without a p-term period expansion or finding a primitive root modulo p.
The conductor-discriminant formula gives disc(K)=p^(q-1). Since k>1,
K is a proper subfield of Q(zeta_p) and has only roots of unity +/-1.
This full construction has independent source/formula review.

## 4. The Class Module Determines The Exact Principal Ideal

For k>1, K is CM of degree q and discriminant p^(q-1), with roots of
unity {+1,-1}. Only p ramifies, totally. The minus group ring is

    R=Z[C_q]/(1+sigma^r)[1/2]=O[1/2].

All odd characters of C_q are primitive because q is a power of2.
Greither2007 Section2 equations(8)-(10) give U^-=R: the total norm
and its averaged idempotent vanish on minus, and the other generator
becomes1. Corollary8.7 applies to this absolutely abelian field with
only2-power roots of unity. Its concluding cyclic-group paragraph
allows the original class module in place of its same-action dual.
With sigma mapped to zeta_q,

    Fitt_R(Cl_K^-)= (L(0,bar chi)).                         (3)

The parent checked the actual source passages; the quarter-factorial note
records the source URL and convention. Identity(3) is unconditional here;
GRH remains in complete class-group generation; Section9 gives an
unconditional classical randomized analytic approximation.

Take the Galois-stable factor base of ALL prime ideals with norm at most
48*ceil(log2|disc K|)^2. One successful COMPLETE compact S-unit call
supplies its entire valuation-relation lattice V. On that SAME event,
Cl_K=Z^d/im(V), with sigma the explicitly computed permutation of prime
ideals. Smith/Hermite transformations carry its action to the finite
abelian presentation. No coordinate oracle or separately trusted class
number accompanies incomplete relations. The complete S-unit primitive
and GRH class-group reduction are the source-audited Biasse--Song
operations used in the two preceding arithmetic notes.

The non-PID Fitting computation does not enumerate maximal minors.
Factor h_K with explicitly charged Shor factoring. For each odd ell|h_K,
extract its primary module and FIRST project to minus by
(1-sigma^r)/2 modulo ell^e, with ell^e annihilating that primary group.
Factor X^r+1 modulo ell, Hensel-lift its distinct irreducible factors
f_i modulo ell^e, and construct CRT idempotents e_i(X). The prime
P_i=(ell,f_i(zeta_q)) is unramified of residue degree d_i=deg(f_i), and

    v_(P_i)(Fitt)=log_ell |e_i(sigma) Cl_K[ell^infinity]^-| / d_i. (4)

The localization is a DVR with residue size ell^d_i; Fitting valuation
is module length. If the module is Z^t/L, the image of an action E_i
has order det(L)/det(L+E_i Z^t), computed by integer HNF. The numerator
in(4) is divisible by d_i. All group sizes, Hensel precisions, matrices
and ideal exponents have polynomial bit length in the paid relation data
and logp for fixed q. Finite-field factoring has a charged randomized
runtime/error budget. Form the odd ideal, conjugate ONCE for(3), and
restore lambda^(r-1). This is exactly I=(z).

Independent review accepted this construction with the minus projection,
factoring payment and conjugation retained. Canonical ideal HNF permits
amplification of the common complete-relation event, not a polynomial
certificate of completeness.

## 5. A Generator In The Fixed Coefficient Field

F depends only on q, not on p. Compute a CERTIFIED COMPLETE fundamental
unit basis once by finite classical arithmetic. Charge its computable
cost to C(q). Merely using cyclotomic units of unproved index one would
be invalid; no Weber-type class-number assertion is assumed.

An integral ideal I is a coefficient lattice in Z^r of determinant N(I).
Exact integer LLL produces nonzero alpha in I with

    ||alpha_coeff||_2 <= 2^((r-1)/4)*N(I)^(1/r).

Each conjugate of alpha has modulus at most sqrt(r)*||alpha_coeff||_2.
Thus |N(alpha)|<=C_F*N(I), where the explicit integer
C_F=(r*2^r)^r more than suffices. J=(alpha)*I^(-1) is integral with
norm<=C_F; because I is principal, so is J. A finite table depending only
on F supplies J=(gamma); return beta=alpha/gamma. Then (beta)=I and
beta has O_q(logp) coefficient bits. Exact ideal inversion/HNF and
division have polynomial bit cost. No quantum PIP/S-unit call in F,
factorization of N(I), or expanded huge compact generator is required.

One can construct the table without guessing which ideals are principal.
The certified unit basis gives a bounded fundamental parallelepiped in
the log-unit hyperplane. Every principal integral ideal of norm<=C_F
has a generator whose conjugate moduli are bounded by a computable
constant depending only on F: multiply any generator by units to place
its centered log vector in that parallelepiped. The inverse embedding
matrix converts that bound into a finite integral coefficient box.
Enumerate the box, retain nonzero elements with ideal norm<=C_F, and
tabulate their canonical ideals and generators. Every principal J needed
above occurs. Table cost is charged to C(q), not supplied as advice.

The fixed-field PIP reduction and explicit finite-box construction have
independent review. For example D=(1/2)*sum_i ||log|epsilon_i|||_infinity
bounds the centered fundamental parallelepiped. The generator moduli are
at most C_F^(1/r)*exp(D), and Fourier inversion in this power basis gives
the same bound on each integer coefficient. Use certified upper bounds
and an enclosing integer box; all constants depend only on q.

## 6. Unit Normalization, Phase And Error Budget

For each odd a representing a conjugate pair, the functional equation gives

    log|sigma_a(z)| = (logp)/2-log(pi)+Re log L(1,chi^(-a)). (5)

The preferred estimator for(5) is the unconditional CLASSICAL randomized
method in Section9, with simultaneous confidence included in the error
budget. The following original deterministic option remains valid.
Under GRH, the source-audited Granville--Soundararajan short-Euler-product
lemma computes(5) to any fixed accuracy delta(q)>0 in poly_q(logp)
time. No Gauss phase is needed for these magnitudes. Use the COMPLETE
fixed-field unit basis to form a square log matrix B after deleting one
CM coordinate. Certify H(q)>=max(1,||B^(-1)||_infinity) by interval refinement.
On the correct ideal event, t=log|z|-log|beta|=B*n for integer n.
Approximate t in vector infinity norm within1/(32H), and B^(-1)
in INDUCED infinity matrix norm within1/(32T). A computable bound is
an upward-rounded T>=1+r*(log(r*p)+log C_beta), where
C_beta=max(1,sum_j |beta_j|); thus T>=1+||t||_infinity by the
coefficient upper bounds and the nonzero integral norms. Since H,T>=1,
the product error is at most1/32+1/32+1/1024<1/8.
The resulting coordinates are within1/8 of n;
round them. Refining the fixed matrix to O_q(log T) bits is paid work,
not fixed-precision advice. This argument has independent review and
does not invoke a closest-vector oracle.

Here beta and z have O_q(logp)-bit algebraic coordinates and nonzero
integral norm, so all their embedding logs are O_q(logp). Hence n is
O_q(logp) numerically, and the product beta times the unit powers may
be expanded with O_q(logp)-bit intermediates. After this normalization,
the quotient by z is a unit. The omitted CM log coordinate also vanishes
because this unit has norm1, so every conjugate has modulus1 and the
quotient is a root of unity. The q torsion associates remain to be selected using
the paid Gauss-phase estimate and the complex short L1 approximation.
For q=4 the unit rank is zero and this normalization is empty.

The original deterministic analytic option uses
Granville--Soundararajan2003 Lemma2.1, actually
read in the previous source audit. Under GRH, with y=(logp)^8,

    log L(1,chi^(-a))
      =sum_(n<=y) Lambda(n)*chi(n)^(-a)/(n logn)
        +O(logp*(log y)^2/sqrt(y)).                       (6)

For any fixed required accuracy depending on q, increase the effective
constant/threshold and compute the finite initial p range directly.
The constants are computable, not hidden advice. Prime-power sieving,
character evaluation and interval summation cost poly_q(logp). The
uniformly nontrivial odd characters here all have conductor p.

The functional equation gives z=tau(chi)*L(1,bar chi)/(i*pi).
Van Dam--Seroussi Algorithm3/Theorem1 supplies arg(tau(chi)) to fixed
angular error pi/(16q) with constant success in poly(logp,q) work.
The public q-valued character prepares its state by phase kickback on a
uniform nonzero register; additive QFT and inversion give the Gauss-phase
eigenvalue. Controlled use pays the relative phase. Expected-error bounds
give constant probability via Markov after reducing the requested error;
gate/state approximation is included. Combine with the complex(6) error
at most pi/(16q). The q candidates zeta_q^j*beta*u are separated by
2pi/q, so this safely identifies the unique correct coefficient vector.
Their embedding phases are evaluated with polynomial-logp precision,
using the O_q(logp) coefficient height and nonzero integral norms.

The equality of ideals is essential: equal conjugate magnitudes alone
do NOT imply a root-of-unity ratio, e.g. (3+4i)/5. Only after recovering
I=(z), rather than (bar z), is (beta*u)/z an algebraic UNIT, so Kronecker
applies. The mandatory conjugation in Section4 cannot be validated or
replaced by log-magnitude comparisons, which lose complex conjugation.

Run the complete class-module block with sufficient internal success
probability, or amplify its canonical ideal HNF to failure below1/20,
INCLUDING its charged integer/finite-field factoring substeps. Numerical
truncation uses certified bounds under GRH. Fixed-field algebraic work is exact/certified. Reduce Gauss-phase
failure below1/20 and, when using Section9, its simultaneous sampling
failure below1/20. The resulting canonical exact output is correct with
probability greater than2/3; repeat whole blocks and take majority of the
coefficient vector to reach error eta. Fixed runtime caps and malformed
outputs count as failures. Cost is C(q)*polynomial(logp,log1eta) under
GRH. This is bounded-error, not exact-on-success and not a certificate
of the class group, GRH or the final answer.

## 7. Validation And Remaining Scientific Scope

The parts above have focused independent review and the corrected assembled
note has actual-text integration review. That review required H>=1, an
induced matrix norm and a public computable T in Section6; those fixes
are integrated. The parent inspected the closed script and JSON for the
sole prescribed case q8,p41,eta27:

    classical_baselines/fixed_order_l0_control.py
    classical_baselines/fixed_order_l0_control.json

The exact period multiplication has primitive polynomial
x^8+x^7+3x^6+11x^5+44x^4-53x^3+153x^2-160x+59. All64 products
and the cyclic action check. The period and maximal-order discriminants
are both41^7. PARI bnfcertify accepts K and F; Cl(K)=1 and the
coefficient field has complete free-unit rank1 and torsion order8.
Its certified unit is epsilon=1+zeta+zeta^2. Direct diagnostic truth is
z=1+zeta-zeta^2-zeta^3, norm8, and the recovered ideal is lambda^3;
lambda^2 fails. Since Cl(K) is trivial, this case does NOT exercise a
nontrivial non-PID class action or the general primary-length algorithm.

Coefficient LLL gives alpha=2, with J of norm2. A certified PARI principal
generator substitutes for the theorem's finite table and returns
beta=1-3zeta+3zeta^2-zeta^3. Log rounding gives epsilon^2. Deliberately
twisting beta by epsilon^7 leaves the same ideal but NONE of its eight
torsion associates equals z; correcting by epsilon^-5 restores the same
normalized generator. Phase selection chooses zeta^2 and recovers z
exactly. The direct numerical functional-equation residual is below1e-55.
This is a decisive finite failure of skipping unit normalization, not
evidence for all primes or an asymptotic advantage.

Diagnostic substitutions are explicit: O(p) period counts and Bernoulli
sums replace Tal preprocessing; exact-z embeddings replace short GRH
logs; PARI replaces fixed-table construction; direct Gauss/digamma sums
replace quantum phase and short Euler data. No quantum primitive, GRH
Euler truncation, finite-table build, arbitrary-class Fitting code or
growing-q algorithm was executed. No novelty, classical separation,
general conductor, even-character nonzero value or arbitrary factorial
consequence follows. The earlier q4,p101 control separately catches the
inverse-character and missing2-factor errors; no new scan is needed.

The next hard question is whether the conductor-p class-module input can
be obtained classically in polylogp, or whether an independently selected
problem offers more research value. Do not extend denominators or add a
generic arithmetic subsystem merely because this composition is available.

## 8. Growing Order: Index-Scaled Unit Coordinates

2026-11-06 follow-up. Core, source, precision and resource derivations have independent
review. The assembled Section8 has independent actual-text integration
review accepted. This section does
NOT remove the circular-unit index, assume Weber's conjecture, or promote
the preceding fixed-q theorem to unrestricted polynomial growing-q time.

### 8.1. Selection And Actual Classical Source

The next scientific question is whether the coefficient-field step can
be made uniform as q grows, replacing its unbounded fixed-field table by
a paid operation. This is the specific blocker removed here. An independent
portfolio review first compared native unique-SVP via the existing
localized-packet source, folded-RS/DQI substitution, and fixed-particle
graph walks. The first has no new full-label noisy-DCP decoder and its
source is already Regev cs/0304005 (local original TeX checked by reviewer);
the second reuses existing capacity-DQI, while fixed particle number gives
a polynomial-size classical simulation. Growing particle count alone did
not supply a decoder. No independent mechanism passed that bounded
admission comparison; no general impossibility or exhaustive search claim.
For the strongest alternative, the native input is an integer lattice
basis with a stated Theta(n^2.5) uniqueness gap and output its shortest
vector. Public lattice translation plus compact spatial packets supplies
noisy dihedral states in polynomial resources, but the source has paid
unflagged bad-state registers. Regev's actual theorem needs a decoder
for that law; no new one was supplied. LLL/BKZ use the SAME explicit
basis, and existing large-gap controls were already recovered by LLL.
The first test of a future receiver is whether its purported full-label
operation reduces to a coarse digest, where the scoped information-loss
falsifier applies. This is not a general DCP or unique-SVP obstruction.

Corpus been-tried and baselines queries for circular-unit log/Fourier
decoding found the prior RLWE unit-orbit audit and LLL/Babai plus index
calculus. The parent and source reviewer read ACTUAL CDPR2016, Claim2.1,
Lemma2.7, Theorems2.8/3.1 and Section4 after Theorem4.1.
[Author manuscript](https://ir.cwi.nl/pub/24685/24685B.pdf). The relevant
source facts are: canonical circular units have a well-conditioned dual
log basis; the full-unit index is the real cyclotomic class number h; and
arbitrary-unit decoding must pay that index. The paper's short-generator
distribution theorem is NOT a theorem about these deterministic L0 values.
Its coset-enumeration discussion does not make representatives free.

Put F=Q(zeta_q), m=q/4, d=m-1, E=O_F^*, and let C be its circular
units including torsion. For q>=8, let B have columns
Log((zeta_q^j-1)/(zeta_q-1)), with j in (Z/q)^*/{+/-1} except1.
Log uses the m complex-place magnitudes. CDPR's actual results give

    [Log E : Log C]=h=h(F^+),
    ||b_j^dual||_2^2=O(log^3(q)/q).                        (7)

These geometry/index statements are unconditional; no general h=1 or
polynomial h bound is established by this source. The parent searched
current literature as well but imports no new class-number bound from
abstracts. The q4 unit-rank-zero case needs no such step.

### 8.2. Paid Full-Unit Coordinates

All field/K-class-module/ideal steps in Sections2--4 have polynomial
(q,logp) descriptions and costs: Tal's imported Jacobi algorithm and
Biasse--Song's complete S-unit theorem explicitly cover growing degree.
The fixed-field table of Section5 is now replaced. Compute h(F^+) with
a paid quantum class-group block under GRH; F^+ has degree q/4 and
log discriminant O(q logq), with its explicit cyclotomic integral basis.

Use one complete compact S-unit call in F supported on the known prime
factors of I=(z). Its valuation matrix V gives a compact generator beta
by solving Vt=v(I), and the integer kernel of V supplies COMPLETE ordinary
unit generators epsilon_i. Include known torsion mu_q. Both outputs rely
on the same successful complete-generator event. The support and compact
encodings have polynomial(q,logp) size; the previously charged factorization
of the ideal supplies its support. No principal generator or unit advice.

Let D=B^+ be the real left inverse/dual-coordinate map. Since E/C has
order h, every h*D*Log(epsilon_i) is an integer vector. Evaluate these
known compact algebraic units to sufficient precision and round to form
the integer columns

    W_i=h*D*Log(epsilon_i).

Their image is EXACTLY h*D*Log(E), since the epsilon_i generate E.
No independence of the supplied generators is needed. For the target
t=Log(z)-Log(beta), the correct ideal event implies beta^-1*z is a unit,
so

    n=h*D*t lies in Z^d and in im_Z(W).                    (8)

Compute n by sufficiently accurate analytic target logs and rounding,
then solve W*x=n over the integers using Smith/Hermite arithmetic.
The compact u=product_i epsilon_i^x_i has Log(u)=t. Thus beta*u differs
from z by a root of unity, selected with the already-paid Gauss phase.
This corrects ALL units, without assuming u lies in C, listing E/C
representatives, or invoking a closest-vector oracle. The independent
review accepted this algebraic step and the growing-degree S-unit source.

Known-unit logs need accuracy inverse-polynomial in h, but their exact
compact factors make that only polynomial in log h PRECISION cost.
In contrast the unknown target approximation needs accuracy1/(h*poly(q))
and polynomial in h TIME, both for the original GRH Euler option and
for the preferred unconditional Monte Carlo estimator in Section9.
Hiding that distinction would invalidate the proposed uniform bound.
The next sections pay precision, exact CRT expansion and error budgets;
no new code or scan is needed for this lattice identity.

### 8.3. Precision And Exact Output, Uniformly In q

Certify A>=max(1,||D||_infinity), where the norm is the INDUCED matrix
norm. Equation(7) gives A=poly(q), since each dual row has l1 norm at
most sqrt(m) times its l2 norm. The circular basis and its dual are
computed with interval arithmetic at polynomial bit cost; their Gram
conditioning is polynomial in q by the same dual bound and the elementary
O(logq) entry bound for B.

Construct a PUBLIC integer bound T>=1 on the infinity norms of all
compact unit-log vectors and t. For a nonzero small factor alpha whose
rational power-basis numerator and common denominator have at most b
bits, the upper bound on all conjugates and its nonzero rational norm
give |log|sigma(alpha)||<=4r*(b+ceil(log2r)+1). Multiply by each absolute
compact exponent and sum. Add r*ceil(log(rp)+1) to cover Log z. The
result may be numerically enormous but log T is polynomial in the
compact encoding. No expanded Pell/unit coefficients are used.

For a computed h within its public cap, approximate D within
1/(100*h*T) in induced norm, and each log vector within1/(100*h*A)
in vector infinity norm. Then each scaled coordinate error in W or n
is at most1/100+1/100+1/10000<1/4, so rounding is exact on the common
correct-data event. This includes the error from multiplying a large
log vector by an approximate basis. Known compact algebraic factors allow
these accuracies with polynomial(q,logp,logh,logT) bit work.

For UNKNOWN target Log z, Section9 is the preferred unconditional
randomized method. The following deterministic alternative is retained:
use the r/2 real parts of the short-GRH series(6), together with the exact (logp)/2-logpi term. Its error bound
reaches delta=1/(poly(q)*h) at y=poly(q,h,logp). For example a sufficiently
large fixed multiple in y=(h*A*(q+logp+logh+2))^8 pays the logarithmic
error factors; finitely many threshold cases are directly computed.
The sieve and summation cost is polynomial in h ITSELF. This is the
only claimed analytic replacement for the fixed-q constant tolerance.

The integer matrices W,n, and a Smith-form integer solution x have
polynomial bit length in all compact input data and logh. Flatten
beta*product epsilon_i^x_i into a product of small algebraic factors
with binary exponents. Its encoding remains polynomial. On the correct
event it equals zeta_q^j*z. Multiplication by zeta_q is a signed
permutation of power-basis coefficients, so every final coefficient has
absolute value <p. Evaluate the compact product modulo small rational
primes avoiding ALL denominators and norms of its small nonzero factors,
with inverses for negative exponents. The number of bad primes is bounded
by the total bit length of these integers, not by exponent magnitudes.
Accumulating good-prime product >2p and symmetric coefficient CRT gives
the exact normalized element. No huge intermediate unit is expanded.
One O(1/q)-accuracy Gauss phase with the complex L1 phase selects z.
Both the precision and compact-CRT deductions have independent review.

### 8.4. Two Distinct Runtime Statements

BOUNDED CLOCK. For arbitrary growing q2power>=8, binary prime p=1+qk
with k odd>1, public character root, and public integer H>=1, there is
a WRITTEN under-GRH quantum procedure with worst-case clock
poly(q,H,logp,log1eta). Its answer is correct with probability at least
1-eta when h(F^+)<=H; a guessed h>H yields ABORT. Outside that promise
it need not produce L0. No hidden upper bound is supplied: H is an
explicit resource parameter and h is still computed, not trusted. The
q4 and k1 branches are the earlier algorithms/direct sum.

EXPECTED TIME FOR ALL q. There is also a WRITTEN under-GRH procedure
for all inputs with expected time poly(q,h(F^+),logp,log1eta) and the
same bounded-error exact output. This does NOT assert worst-case
poly(q,true h,logp) time. The necessary runtime repair is as follows.

An effective bound is U_q=(2q)^(4q). Indeed F^+ has degree m<=q and
discriminant at most q^q. Minkowski supplies an integral ideal in every
class with norm at most X<=q^(q/2). If a(n) counts ideals of norm n,
Euler factors give a(n)<=d_m(n), whence

    h<=sum_(n<=X) a(n)<=X*(1+logX)^(m-1)<=q^((5/2)q)<U_q.

The middle bound follows by summing the m-fold divisor function over
products and using harmonic sums. Thus log U_q=O(q logq). Reject h
guesses outside[1,U_q], and cap every subsequent block by its explicit
polynomial worst-case work on that cap, INCLUDING malformed downstream
outputs. If Q(q,logp)*h^a bounds the h-dependent work on ALL capped
branches for a fixed exponent a, amplify the canonical h block
to error below eta/[100*U_q^(a+2)]. Its amplification overhead remains
polynomial in q and log1eta. Even a wrong large h guess contributes at
most Q*U_q^a times that probability to EXPECTED work. Correct-h paths
cost Q*h^a. Invalid data, rank failures and exceeded clocks are failures,
not reasons for unbounded refinement or restarts.

For both statements, h and the oriented ideal I have canonical outputs
and are amplified separately. One complete F S-unit event supplies beta
and ALL ordinary unit generators; its success is not inferred from an
unrelated majority result. Take that event's probability at least2/3,
and allocate total failure below1/20 to the other canonical arithmetic,
factorization, phase/state/gate and numerical steps. The whole canonical
output is then correct with probability at least2/3-1/20>1/2.
Independent whole-output repetition/majority, with FRESH randomized
arithmetic blocks in each repetition, gives error eta and preserves
the expected-work bound. The h-block error is small enough for
the expected-time calculation above, not merely for correctness. Under
GRH the original Euler interval/truncation errors are deterministically
bounded. With the preferred Section9 estimator, its additional sampling
failure enters the same ledger and each repetition uses fresh samples.

In particular any publicly bounded family h(F^+)<=poly(q,logp) has a
polynomial-clock quantum composition. This is a FAMILY PROMISE, not a
proved bound on all power-of-two conductors. Neither a Weber class-number
claim nor a classical lower bound has been established. A polynomial
dependence on the numerical h cannot be rephrased as dependence only on
its bit length.

### 8.5. Validation, Baselines And Remaining Question

No new implementation is required for the coordinate identity. Reuse the
certified q8,p41 control: its epsilon=1+zeta+zeta^2 is exactly the
canonical circular unit b_3, and the complete unit certificate gives
index1. Its existing exponent2 correction and exponent7 wrong-unit
control therefore cover the index1 branch. They do not test h>1,
the new quantum class-number call, analytic precision, compact CRT or
any growing-q complexity claim. No new scan is admitted.

The strongest applicable classical operation, CDPR circular-coordinate
rounding, has been USED rather than overlooked. Its published
short-generator distribution is not assumed, and full units are paid
through the exact integer image W. Classical index-calculus/PIP can
replace the quantum arithmetic at their own costs. A faster direct
classical exact-L0 method remains UNKNOWN. These are parameterized
upper bounds from known primitives, with no novelty or separation claim.

The precise remaining scientific question is whether the numerical
circular-unit index can be removed, either by a paid decoder for the
known target in Log(E)/Log(C), or by a different native algorithm of
higher expected external value. A bound on h, a supplied unit coset,
or a favorable finite dimension cannot be treated as an algorithm.

Section8 final actual-text review accepted the coordinate lattice, source
scope, explicit precision, effective class-number cap, compact CRT and
both distinct runtime statements. All malformed branches retain the
public work caps, and whole-output repetitions use fresh arithmetic
blocks. The parent checked the cited source passages and the existing
control's exact b_3 identity. No additional test execution was warranted.

## 9. Unconditional Classical Approximation Of Nonreal L1

2026-11-06 follow-up. The estimator, nonquadratic source scope and
precision/resource proof have independent review. Actual integrated-text
review of Section9 and its preferred-step annotations is accepted. This replaces the analytic GRH approximation, NOT
the class-group computation. The full L0 composition remains under GRH.

### 9.1. Contract, Selection And Baselines

Input a binary prime p, public eta defining a nonprincipal character chi
of power-of-two order q>=4 as above, rational additive accuracy0<epsilon<=1
and failure allowance0<rho<1. The output approximates L(1,chi) to
additive error epsilon with probability at least1-rho in classical time
polynomial(q,logp,1/epsilon,log1/rho). A relative/log-magnitude/circular-
phase accuracy delta is also available in polynomial(q,logp,1/delta,
log1/rho) time for these NONQUADRATIC characters. This is randomized
coarse approximation, not exact L0, polynomial-in-log(1/epsilon)
computation, or a new quantum advantage. Character evaluation is paid by
modular powering and q comparisons. No character oracle is supplied.

The decisive question was whether the analytic phase/magnitude input
actually needed a short Euler product or a new quantum operation. Corpus
been-tried and baselines queries for Dirichlet L1 / dyadic importance
sampling found no matching result (the baseline catalog returned only
a weak unrelated lattice match). Literature searches found standard
deterministic evaluation routines, not a priority certificate for this
argument. The parent and reviewer checked CDPR2016 ACTUAL Theorem2.6,
which gives an effective unconditional lower bound

    |L(1,psi)| >= 1/(C logp)                              (9)

for primitive nonquadratic psi of conductor p. The cited
[author manuscript](https://ir.cwi.nl/pub/24685/24685B.pdf) attributes
this to classical Landau bounds. This, not GRH or a typical-generator
assumption, is the relevant primary import. All odd powers chi^a here
have full order q>=4, so are nonreal and primitive of conductor p.
The result does not give the same relative complexity for real quadratic
characters, where the unconditional lower bound is much smaller.

### 9.2. Exact Dyadic Sampling Law

Choose J to be the least POWER OF TWO at least
ceil(log2(8p/epsilon+1)), and put N=2^J-1. Then N>=8p/epsilon and
J=O(logp+log1/epsilon). The numeric cutoff N is never enumerated.
Draw j uniformly from{0,...,J-1}, using exactly log2J random bits, then
draw n uniformly from{2^j,...,2^(j+1)-1} using j fresh bits. Return

    X=J*2^j*chi(n)/n.

For every n in its unique dyadic block, its probability is1/(J*2^j),
so E[X]=sum_(n<=N) chi(n)/n EXACTLY and |X|<=J. This choice of J
avoids a rejection-sampling clock. It uses at most J+log2J random bits
per sample, with O(J)-bit integer arithmetic. Multiples of p have chi=0.

Nonprincipality and periodicity imply |A(t)|<=p for
A(t)=sum_(n<=t)chi(n). Abel summation therefore bounds the omitted tail
by2p/N<=epsilon/4, unconditionally. The fact that the series is only
conditionally convergent at1 does not invalidate the finite unbiased
estimator or this explicit tail bound.

For m characters (m=1 for a single value, m=q/4 for the required
conjugate pairs), use

    M >= 32*J^2*epsilon^(-2)*log(4m/rho)                  (10)

independent samples, with integer ceilings/upper bounds. Hoeffding applied
to real and imaginary parts bounds each component error by epsilon/4
except with total probability rho after a union bound. The resulting
complex sampling error is less than epsilon/2. Approximate roots of
unity and rational weights so the total numerical error is at most
epsilon/4. For example evaluate each character root within
O(epsilon/J) and average with fixed-point precision paying logM bits.
No enormous common rational denominator is formed. Sampling, tail and
numerical errors sum to at most epsilon. Shared n samples may be used
for all characters; their independence across characters is unnecessary
for the union bound. Every sample is fresh across the M trials.

### 9.3. Log-Magnitude, Phase And The Existing Unit Algorithm

Take b=ceil(log2p) and a fixed effective integer C at least the constant
in(9), enlarged if needed. Then kappa=1/(Cb) is a rational lower bound
for each required |L(1,chi^(-a))|. For0<delta<=1/4 set

    epsilon=delta*kappa/16.                              (11)

On the common good event, |Lhat/L-1|<=delta/16. The convergent
logarithm of1+(Lhat/L-1) gives errors below delta in both log|L| and
CIRCULAR phase. No global unwrapped log branch is needed. If an estimate
is too close to zero (e.g. |Lhat|<kappa/2), ABORT rather than refine
without a clock; the good event cannot trigger that condition. Numerical
log/argument evaluations have polynomial bit cost using the known lower
bound and fixed error allocation.

For fixed q this directly supplies Section6's constant target-log and
phase tolerance. For Section8 choose delta to meet its stated
1/(100*h*A) target-log error budget, allowing the additional elementary
(logp)/2-logpi and beta-log errors. Equations(10)-(11) then use polynomial
(q,h,logp,log1/rho) work; the leading sampling dependence is quadratic
in1/delta, with logarithmic cutoff factors. It is NOT polynomial only in
logh. The previous public-H clock and expected-time bad-h protection
remain valid, updating their generic polynomial work exponent if needed.

Add the simultaneous Monte Carlo failure rho to the existing aggregate
<1/20 ledger for the non-F-S-unit blocks. Whole-output repetitions use
fresh arithmetic AND fresh classical sampling. The complete F S-unit
event still pays beta and the full units together. No exact-on-success
claim or independent trust in an incomplete class group is introduced.

The preferred analytic subroutine is now this unconditional randomized
one; the earlier deterministic GRH Euler proof remains a valid option.
GRH is STILL used to generate the full conductor-p class module and, in
the uniform version, the real coefficient-field class number h. Those
Dedekind GRH assumptions can already imply relevant Dirichlet GRH, so
this does not claim a strictly weaker logical assumption for the whole
composition. It removes the analytic subroutine's dependency and supplies
a stronger classical baseline for that operation. Exact I=(L0), the
Gauss phase and their access costs are not obtained by this estimator.

### 9.4. Minimal Exact Classical Control

One Sage exact finite-distribution check used p13,q4,eta5,J4,N15. Its
character is chi(n)=i^j iff n^3=5^j mod13. Exact summation over the
finite sampling distribution gives

    E[X] = 341/315 - (5309/9240)i = sum_(n<=15)chi(n)/n,
    E[|X|^2] = 271511131/24012450 < J^2=16.

Omitting the weight2^j/n gives the NONZERO bias

    211/1260 - (233/4620)i.

The parent executed this with /opt/anaconda3/envs/qsearch-cas/bin/python
and exact QQ/CyclotomicField arithmetic. This checks the precise sampling
normalization and falsifies the unweighted substitute. It is not a Monte
Carlo confidence experiment, a general theorem inferred from finite data,
or execution of the whole L0 algorithm. No new runner or scan was added.

### 9.5. Independent Class-Generation Comparison

A separate candidate would remove class-group GRH by sampling random
rational primes of polynomial bit length, factoring their defining
polynomial, and collecting ideal classes. Its intended output is complete
class generators/action for the SAME K; the hoped-for cost is polynomial
in degree and log discriminant. Rational-prime sampling/factoring is a
paid first operation, not a class-uniform oracle. Classical prime-density
and relation-collection baselines apply; no uniform generator-coverage
theorem was supplied, so no unconditional algorithm is admitted.

There is a precise elementary failure of one proposed repair. If K/Q
is cyclic CM of2-power degree and an unramified prime ideal has residue
degree f>1, its decomposition group is even and contains complex
conjugation c. Therefore c fixes that prime ideal and its class; the
class has ZERO odd-minus projection. Accepting higher-degree prime factors
cannot replace completely split primes in this particular minus-class
generating strategy. The parent checked the independent derivation.

Do not conflate this with every exceptional class character being harmful.
If a normalized class distribution mu satisfies Re E_mu[psi]<=e<1/2
for every nontrivial class character, then every proper subgroup has
mass at most(1+e)/2 by character orthogonality. For fixed e, a rank-growth
clock gives generators after O(log|G|+log1/rho) independent draws.
Negative character bias is allowed. What is missing is a paid sampler
with those normalized guarantees, including its supply rate; factoring
random element norms supplies no coverage theorem by itself. No assertion
that an exceptional zero exists, and no general unconditional-class-group
no-go, follows. The norm-sampling bypass remains UNKNOWN.

The subsequent source audit in UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md
Section5 pays a CLASSICAL inverse-norm ideal law using independent factored
integer streams. Its class-coverage bound remains unknown; it does not
remove GRH here. That note also distinguishes Charles's fixed-field
uniform sampler from the required varying-field clock.

Section9 actual-text review accepted the sample constant32, exact bounded
sampling, numerical allocations, local-log conversion, simultaneous
confidence and existing runtime protections. The reviewer also checked
the finite expectation/bias algebraically and both Section9.5 lemmas.
The parent verified the source and ran the single exact classical control;
no full sampler, confidence experiment or quantum primitive was executed.
