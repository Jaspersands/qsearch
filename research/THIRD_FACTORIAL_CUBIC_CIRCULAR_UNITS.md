# One-third factorial through cubic circular units

6 November 2026. Written unconditional bounded-error quantum composition;
independent core and integrated actual-text review ACCEPTED. The exact
circular-unit/Fitting source, embeddings, compact arithmetic, local residue
and full error budget are included. No novelty, classical separation or
quantum execution claim.

Preferred implementation update (2026-11-06):
PRIME_INDEX_FACTORIAL_RESIDUE_NORMALIZATION.md Section10 proves that ANY
consistent algebraic embedding suffices, including ell3. Its covariance
argument removes the quantum Gauss-phase calls used in the original
construction below. The original phase-based version remains valid but
is no longer required; quantum factoring and compact S-units remain.

## 1. Native question and scientific selection

Input a binary prime p=1mod3, p>=7. Output the exact residue
k! modp, k=(p-1)/3, with bounded error0<eta<1/2. A primitive root g can be
found after charged Shor factorization of p-1; choose rho=exp(2pi*i/3)
and chi(g)=rho. Changing this auxiliary g must not change the factorial.
No units, class module, circular generator, cyclotomic product, chosen
complex branch or principal-ideal generator is supplied.

The written clock is polynomial(logp,log1/eta). The mechanism recovers
one SPECIFIC circular unit from a complete cubic class/unit computation,
uses an existing quantum Gauss-phase algorithm to select its embedding
and one of six generators, solves an integer unit-exponent equation,
and reduces a local unit. All implemented number fields have degree3
or6. The degree-(p-1) cyclotomic field appears only in the proof and a
small exact control. Expanded circular units can have large height and
must remain in compact representation.

Corpus been-tried and baselines queries preceded the source check.
Alternatives considered were a larger-annihilator character decoder
(no proved success probability), and common-slice reconstruction from
global copies (repeated copies of a selected slice are not free).
This route is selected because it supplies a concrete operation from
paid arithmetic to a canonical binary-input output, beyond the closed
CM full-kernel-product proposal. It uses, rather than replaces, the
known quantum Gauss-phase algorithm.

The strongest retained applicable comparators include classical class/unit
arithmetic with its ERH subexponential algorithms, and the following
actual statements in [Tal TR26-211](https://eccc.weizmann.ac.il/report/2026/211/).
The69-page cached source `audits/sources/jacobi_classical_eccc_2026_211.pdf`
ALREADY includes these; the earlier audit of Theorem1.1 alone was not
an exhaustive comparison.

* Theorem1.1: deterministic soft-O(q^c+sqrt(p/q)) for supplied q|(p-1).
* Theorem1.3: for EACH FIXED odd prime power r and supplied q|Phi_r(p),
  soft-O_r(q^c_r+(Phi_r(p)/q)^(1/(2phi(r)))) at modulus p. This is
  deterministic with a compatible field/character supplied; Las Vegas
  construction pays them in the same expected bound. For r3 it is
  soft-O(q^c_3+sqrtp/q^(1/4)). The constants/exponents depend on r;
  there is no growing-r polynomial guarantee.
* Proposition4.2: expected soft-O(q^C+sqrt(p/q)) for q>=4 dividing p+1,
  with (p+1)/q ODD; it pays the quadratic field and order2q character.
* Proposition4.3: deterministic O(sqrtp*(logp)^(3/2)*sqrt(loglogp))
  without a divisor promise.

Proposition1.7 gives a density bound for suitable divisors at finitely many
fixed indices, not a uniform all-prime result. The optimal applicable
divisor and its discovery cost matter; choosing q3 alone is not a fair
comparison. None of these stated clocks is uniformly polynomial in logp
for every input here; this does not exclude a stronger classical method.
Exact Jacobi sums are already classically polynomial at fixed order
(actual Theorem1.5). Tal's July2026 quantum paper, actual Theorems1.1/1.3,
already uses quantum arithmetic to reconstruct Jacobi sums for a general
factorial algorithm; the classical theorem matches that imported Jacobi
operation. No classical lower bound, speedup or novelty claim follows.

## 2. Paid degree-three and degree-six field presentation

Let J=J(chi,chi) in Z[rho], computed by the already audited exact-Jacobi
method. Write J=a+b*rho, with J*bar(J)=p. For ANALYSIS define

    tau=sum_x chi(x) zeta_p^x,      tau³=pJ,
    bar(tau)=tau(bar(chi))=p/tau.                            (1)

Let L=Q(rho,tau). It has degree6: the valuations of pJ at the two primes
above p in Z[rho] are1 and2, so pJ is not a cube. Complex conjugation
sends rho to rho^-1 and tau to p/tau. Its real cubic fixed field is
K=Q(theta), where

    theta=tau+p/tau,
    theta³-3p theta-p(2a-b)=0.                              (2)

In the cyclotomic interpretation theta=3 eta_0+1, where eta_0 is the
sum over cubic residues. Thus K is the real cyclic cubic field of
conductor p and discriminant p². The physical automorphism sigma induced
by zeta_p->zeta_p^g obeys

    sigma(tau)=rho^-1 tau,
    sigma(theta)=-theta/2+3pb/[2(theta²-p)].                 (3)

The denominator is invertible in K; all calculations reduce modulo(2).
The integral maximal order is paid by fixed-degree order algorithms after
Shor factorization of the polynomial discriminant, as in the retained
cubic Selmer composition. The full field L can use O_K tensor Z[rho],
since their discriminants p² and-3 are coprime.

Constant-accuracy quantum estimation of tau/sqrtp selects the intended
real embedding of K: for each real embedding iota form

    tau_iota=[iota(sigma theta)-rho*iota(theta)]/(rho²-rho).

These three candidates have phases separated by2pi/3, even if two real
theta roots are close. Fixed-degree root separation pays O(poly(logp))
precision. No constant separation of the real theta roots is assumed.
Actual van Dam--Seroussi Algorithm3/Theorem1 is the Gauss-phase primitive;
its source has already been audited in CUBIC_GAUSS_ELLIPTIC_PRODUCT_ADMISSION.md.

## 3. Recovering the exact circular-unit submodule

Let U=O_K^*/{+1,-1}. It is a free rank-one module over
R=Z[rho], with rho acting by sigma. Indeed U has Z-rank2, the norm
operator1+sigma+sigma² vanishes modulo signs, and R is a Euclidean PID.
The same norm operator kills Cl(K): the product of all conjugates of an
ideal is generated by its rational ideal norm. Thus Cl(K) is a finite
R-module. These are the SAME actions, not a contragredient convention.

For analysis only, define the positive ramified-prime generator and a
real circular unit

    alpha=Norm_(Q(zeta_p)/K)(1-zeta_p),
    c=Norm_(Q(zeta_p)^+/K)
      [zeta_p^((1-g)/2)(1-zeta_p^g)/(1-zeta_p)],
    c²=sigma(alpha)/alpha,       C=R*c in U.                (4)

The half exponent is modulo p. No long cyclotomic product is computed.
With the selected embedding and

    T(v)=sum_(j=0)^2 rho^j log|sigma^j(v)|,

Fourier expansion of log|1-zeta_p^a| gives

    T(alpha)=-tau(chi)L(1,bar(chi)),
    T(c)=(1-rho^-1)tau(chi)L(1,bar(chi))/2.                 (5)

If log c=(l0,l1,l2), then sum l_j=0 and the regulator of c,sigma c is

    R_C=l0²+l0*l1+l1²=|T(c)|²/3=p|L(1,chi)|²/4.

The real cubic analytic class-number formula gives
h_K R_U=p|L(1,chi)|²/4. Hence

    [U:C]=h_K.                                            (6)

This scalar identity ALONE would not identify C inside U.

The needed exact identity is

    C=I U,       I=Fitt_R(Cl(K)).                          (7)

Here is its all-prime source proof. The SMALL totally positive circular
units in All's convention are exactly 2C modulo signs. Prime-conductor
cyclotomic norm distribution shows that their ambient multiplicative
group is generated by positive rational primes and alpha,sigma alpha,
sigma²alpha. Its intersection with units is the augmentation subgroup,
generated by sigma alpha/alpha and sigma²alpha/sigma alpha, namely c²
and(sigma c)². Extra prime powers in the cyclotomic conductor add no
new generator; rational prime factors cannot cancel non-p valuations.

For every rational prime ell that splits in R, ell=1mod3 and ell>=7.
Actual [Timothy All, Gauss Sums, Stickelberger's Theorem and the Gras
Conjecture for Ray Class Groups, v2, Theorem1.2, d=1](https://arxiv.org/abs/1502.01578)
gives equality of the SAME character-component orders of units modulo
small circular units and the class group. Its hypotheses ell not
 dividing2[K:Q] and e_K(ell)<ell-1 hold: e=1 unless ell=p, when e=3<p-1.
Both split characters are Q_ell-valued, so the theorem controls them
separately. The factor2 in 2C disappears at odd ell. Component lengths
therefore determine the two local Fitting valuations separately.

For every inert ell=2mod3 (INCLUDING2), and at the unique prime above3,
there is only ONE prime of R above ell. Equal total cardinalities in(6)
already determine its Fitting valuation. No 3-class exclusion, unramified-
at-p transfer, or identification of a larger circular-unit convention
is needed. Over each DVR a finite module's Fitting valuation is its
length; thus the local equalities prove(7) globally. They do NOT assert
an isomorphism of the two finite modules. Same-action orientation matters.
Greither1992 corroborates the convention, but is not a required import.

## 4. Paying the arithmetic and selecting one of six generators

Use the retained unconditional ODD_GALOIS_CLASS_GROUP_COMPOSITION.md
source for K. Close its random class-generating prime list under sigma
and adjoin the unique ramified prime P. One complete compact S-unit
basis and its valuation matrix V supply, on ONE success event:

* Cl(K)=Z^S/im(V), with sigma as a known permutation of S;
* all ordinary units from the integer valuation kernel;
* a compact beta with (beta)=P, by solving Vx=e_P.

The last equation is solvable because alpha proves that P is principal;
alpha is not an algorithmic input. Orient Norm(beta)=p by its sign.
No new principal-ideal-generator oracle is assumed. Class and unit
sigma coordinates, integer kernels and R-presentations use retained
compact arithmetic and finite-rank exact linear algebra. Add the relations
rho*e_i-e_(sigma i) to the class presentation; Euclidean R-Smith/gcd
arithmetic computes I without enumerating presentation minors.

An R-generator of U is also paid. For a nonzero integral unit-coordinate
vector v, the pair(v,S_U*v) is a Q-basis, since Phi_3 is irreducible.
The inverse of the map1->v,rho->S_U*v identifies the full unit lattice
with a fractional Eisenstein ideal. Clear its denominators, take the
Euclidean gcd of its two generators, and map back to w. Check
det(w,S_U*w)=+1 or-1. A generator of I acting on w gives c0. These are
binary-integer lattice operations, not enumeration over the class number.

Every R-generator of C is one of

    c0, sigma c0, sigma²c0, c0^-1, (sigma c0)^-1, (sigma²c0)^-1

modulo the irrelevant field sign. Their T-values differ by the six
phases of the units of R. Formula(5), constant Gauss-phase accuracy and
constant relative L(1,bar chi) accuracy therefore choose c modulo sign.
Evaluate the ACTUAL candidate T-values; do not confuse T(sigma v)=
rho^-1 T(v) with the R-action rho->sigma.

The dyadic nonreal-L1 estimator from
FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md Section9 applies here by its
proof: cubic chi is also primitive and nonquadratic, evaluated by modular
powering and three comparisons. The earlier displayed theorem was scoped
to power-of-two order, so this explicit reuse of its proof is required.
Its effective nonquadratic lower bound1/(C logp) pays inverse-polynomial
additive accuracy and constant relative phase accuracy unconditionally.
It does not require enumerating p terms or estimating L to exponential
relative precision. Compact-unit logarithms and all interval errors must
be charged; no expanded c is constructed.

## 5. Exact unit-exponent Hilbert 90

Let delta=c² and u=delta/(sigma beta/beta), an ordinary norm-one unit.
In the complete unit basis solve the INTEGER equation

    (S_U-I)v=coord_U(u),                                   (8)

where S_U is the actual sigma matrix, not a class-group matrix. Correct
selection of c guarantees an integer solution; det(S_U-I)=3. If it fails,
ABORT this attempt. Choose the sign of the resulting compact epsilon so
Norm(epsilon)=1 and put alpha_hat=beta*epsilon. Then

    sigma(alpha_hat)/alpha_hat=delta,   Norm(alpha_hat)=p.

These two conditions uniquely specify alpha: their ratio is rational
and has cube norm1, so is1. Working modulo signs in(8) causes no lost
minus sign, since both sides of the lifted ratio have norm1 and a
nontrivial rational sign would have norm-1 in degree3.

## 6. The factorial is one local residue

Use the prime of L above P specified by

    rho -> r=g^k modp,        k=(p-1)/3.

For proof ONLY put Z=zeta_p-1 in the full cyclotomic field. As chi_bar(a)
reduces to a^(2k), expansion of sum_a chi_bar(a)(1+Z)^a shows that every
coefficient below k is0 modp and the coefficient of Z^k is-1/k!:
only degree3k=p-1 in a survives the finite-field sum. Terms divisible
by p have Z-valuation at least p-1>k. Therefore

    tau(bar chi)/Z^k = -1/k! modulo the cyclotomic prime.

The cubic-residue subgroup H has even order k and product-1; hence

    alpha/Z^k = product_(a in H) a = -1 modulo that prime.

It follows that

    alpha_hat/tau(bar chi) = k! modulo P_L.                (9)

Both numerator and denominator have valuation1 at this degree-six prime,
so their ratio is a LOCAL UNIT. It is not valid to reduce them separately
to0 and divide. In degree6 use local normalization, with tau(bar chi)
itself as a uniformizer, and compact unit residues. The other prime over
p has a different valuation; its embedding must not be substituted.
The residue field is Fp, so the output is a canonical integer0..p-1.

## 7. Resource accounting and bounded error

Input/discriminant/prime-list lengths are polynomial in logp. Degree is
fixed3 or6; random class-generator norms are polynomial-BIT, not assumed
numerically small. No real-class-number upper bound polynomial in logp
is needed: h and the R-ideal generator have polynomial BIT length, and
integer exponents in compact units are charged in binary. Unlike earlier
approximate circular-basis decoding, (7) recovers the exact lattice without
an inverse-h analytic accuracy requirement.

The actual [Biasse--Song v2](https://arxiv.org/abs/2510.02280) Section8.1,
Definition8 and Proposition7 compact
representation has polynomially many exact leaves of polynomial bit size,
with binary exponents l^j for polynomially bounded j. Rational leaves are
allowed. Integer kernels, module operations and(8) preserve polynomial-
length power products with polynomial-bit exponents. They need not
preserve small EXPANDED heights. The coarse class bound h<=512p² suffices
for logh=O(logp); it is not a numerical polynomial-in-logp bound on h.

Here is an explicit logarithm and exact-coordinate budget. In degree at
most6, suppose the chosen integral basis has all embedding magnitudes
at most2^B0 and a nonzero rational leaf has coefficient height at most H
bits. Norm bounds give |log|sigma(leaf)||<=50(H+B0+1). For a compact
product u=product gamma_j^e_j, the bound

    C(u)=max(1,sum_j |e_j|*50(H_j+B0+1))

has polynomial BIT length even when numerically large. To evaluate its
logs to absolute error epsilon, leaf precision adds log(sum_j|e_j|),
not sum_j|e_j|. Certified fixed-degree root isolation and interval
arithmetic therefore have polynomial bit cost.

There is a uniform regulator lower bound sufficient for rounding. If
all three logs of a nontrivial cubic unit had absolute value<=1/4, each
conjugate of epsilon²-1 would have absolute value<1. Its nonzero integral
norm would then be<1, impossible. With the third log minus the sum of
the first two, the two-coordinate log lattice has minimum sup norm>1/8.
Minkowski's square bound gives R_U>=1/64. If full-unit basis log entries
are bounded by C>=1 and target entries by D>=1, put

    K_bound=128C,   X=max(1,K_bound*D),
    epsilon_log <= 1/[16 K_bound(1+2X)].                  (10)

The inverse log matrix has row-sum norm<=K_bound; elementary inverse
perturbation bounds give coordinate error<=1/8 at(10). Rounding recovers
the exact integers for a unit target. Required bits are O(logC+logD),
not C,D or h. This pays the sigma action and the coordinates in(8).
Also |T(c0)|²=3R_C>=3/64, so constant absolute T-error pays a constant
phase error. Allocate at most pi/48 each to the Gauss, L1 and candidate
phase approximations; the six phases are pi/3 apart. No inverse-h
accuracy is hidden in the branch choice.

Local normalization is explicit. Put pi=tau(bar chi), a uniformizer at
the SELECTED P_L, where v(p)=3. For each small rational leaf a=A/D with
A in O_L, D>0, set t=v_p(D), k_A=v_(P_L)(A). These valuations are bounded
by polynomial leaf-height bits. In the one-dimensional Fp-space
P_L^k_A/P_L^(k_A+1), compute the coordinate lc(A) of A relative to
pi^k_A using ideal HNF/SNF. Similarly compute c_p=p/pi³ modP_L from
P_L³/P_L⁴. The normalized nonzero leaf residue is

    lc(A) / [(D/p^t modp)*c_p^t],     v_(P_L)(a)=k_A-3t.  (11)

Multiply these residues to the binary exponents modulo p. Add the
valuations exactly and check total valuation0 for alpha_hat/pi. Only
leaf-height-sized ideal powers and pi^k_A are used; no huge compact
exponent is expanded. A p-divisible denominator is never reduced and
inverted globally. This pays(9) with polynomial-bit local arithmetic.

For one capped run, budget at most1/100 total failure for factoring,
primitive-root finding, complete class generators and randomized finite
arithmetic. A complete compact S-unit basis succeeds with probability
at least2/3 on the retained source theorem; the SAME full-basis event
pays all class/unit/beta outputs. Budget at most1/50 for the Gauss and
L1 estimates together. All other interval and exact arithmetic on this
event is certified. A verified factorization of N=p-1 pays primitive-
root testing: if s is the number of distinct prime factors, then
N/phi(N)<=s+1<=1+log2(N), by q_i>=i+1 and the telescoping product
product_i q_i/(q_i-1). O(logp*log1/delta) independent candidates thus
meet any fixed failure budget delta within a polynomial cap.

Malformed outputs, failed integer equations, nonzero final valuation
or exhausted caps give ABORT. The correct canonical integer has per-run
probability at least2/3-3/100>3/5. Repeat the ENTIRE run independently
R=ceil(50 ln(2/eta)) times and return the strict majority integer, or
ABORT if none exists. Hoeffding bounds failure by eta/2<eta. Arbitrary
unit bases are never majority-voted. Thus the written composition has
bounded-error quantum clock polynomial(logp,log1/eta), with no GRH or
supplied arithmetic advice. Independent actual-text review of this
integration ACCEPTED; finite controls are not its asymptotic justification.

## 8. Exact falsifier control and scope

The first decisive exact control is p313, g10. It uses a degree312
cyclotomic field ONLY as finite truth to test the cubic arithmetic:

    K: t³+t²-104t+371=0,   disc K=313²,  bnfcertify=1,
    Cl(K)=C7,             sigma(t)=t²+6t-68,
    units=(-1,-t²-6t+73,t-5),
    S_U=[[-1,1],[-1,0]],  c=21t²+128t-1531.

The c and sigma c free-unit vectors are(-1,-3),(-2,1). The class generator
(5,t+1) maps to(5,t+2), giving sigma action4 mod7. The circular lattice
and the SAME-action Fitting image both have row HNF[[1,3],[0,7]].
Reversing to action2 produces[[1,5],[0,7]], DIFFERENT despite equal index7.
This is an exact orientation falsifier.

The SAME p313 control completes the bridge. The ramified-prime generator
beta=t²+5t-68 has norm313. The correction u has free-unit coordinates
(-1,-5), and(8) gives v=(2,3). The raw epsilon=u1²*u2³ has norm-1,
so alpha_hat=-beta*epsilon, exactly the cyclotomic truth
327t²-3635t+10020. This catches a lost norm sign.

At rho=g^104=214 mod313, valuations of(alpha,tau,bar tau) are(1,2,1).
Using t-104 as a local uniformizer, alpha and bar tau have linear
coefficients216 and3; the residue216/3=72 equals104! mod313. Using tau
instead has ratio valuation-1, a pole. At the conjugate rho98 the
valuations swap. Changing both character and local prime preserves the
answer; changing only one does not. The local residue214 is distinct
from the class-module action4 above.

Durable source scripts, exact JSON and logs are in
`audits/controls/cubic_third_factorial_p313/`. The bridge was rerun from
that durable path; the source script was syntax-checked after only its
output paths changed. These are finite classical controls. No quantum
Gauss-phase, S-unit routine or end-to-end quantum algorithm was executed.

Independent core/source and final integrated-text reviews are complete.
The next scientific selection must compare a new paid mechanism on a
growing-parameter native problem against independent directions, rather
than extending this fixed-degree composition by inertia. Classical matching
for the exact factorial remains open here, not hard. No broader prime
sweep, quantum simulator, novelty/separation claim or publication is queued.
