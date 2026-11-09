# Canonical Quarter-Factorial Through Quartic Arithmetic

2026-11-06. Independently actual-note reviewed WRITTEN bounded-error
quantum composition under GRH, using published primitives. Two certified
classical controls are complete and parent-inspected. The later classical
phase simplification in Section5.1 also passed actual-text review. No novelty,
separation, executed quantum algorithm or polynomial classical output
certificate is claimed. The precise source/algorithm obligations are below.

## 1. Native Question And Direction Selection

Input: a binary prime p=5 mod8 and error tolerance 0<eta<1/2. Output the
canonical residue G=((p-1)/4)! modp in [0,p). No character oracle, class
group, unit, Galois-action matrix or sign advice is supplied. Handle p=5
directly, G=1; below p>5 and k=(p-1)/4 is odd and greater than one.

The target cost is polynomial(logp,log1eta) bounded-error quantum time.
The mechanism combines an exact quartic class module, its Fitting ideal,
a constant-accuracy Gauss phase, and classical congruences. Section5.1
reuses the required half-factorial to compute that phase classically.
This differs from estimating an exponential sum to inverse-sqrtp accuracy.
All number fields have degree at most four and logarithmic discriminant
O(logp); no growing cyclotomic-degree input is hidden.

The corpus been-tried/baselines queries on canonical quarter-factorial,
class-number and compact arithmetic led to HALF_FACTORIAL_COMPACT_ARITHMETIC.md,
COMPACT_RESIDUE_CONDUCTOR_DECISION.md and JACOBI_GROUP_RING_RECOVERY.md.
They are reused. Independent comparison rejected a binary-exponent
isogeny-action shortcut: an ell^e kernel/residue still has Theta(e logell)
bits, and a short evaluable ideal word was not supplied. The current
cubic/RS paper2509.07276v1 and the existing cubic-flat/degree-reduction
notes leave a fixed-rate problem open but supply no new paid operation.
This arithmetic target has a concrete end-to-end mechanism to audit first.

Strongest comparator: the SAME arithmetic identities with classical
class-group/relation and analytic Gauss-sum algorithms, and direct fast
modular-factorial algorithms. Subexponential class-group methods must be
charged under their actual GRH/heuristic hypotheses. Tal's September2026
exact Jacobi-sum algorithm is already classical polynomial(q,logp); its
q=4 part is classical preprocessing here. Its modular-factorial tradeoff
does not make a fixed-q canonical factorial polynomial(logp). No classical
lower bound, optimal exponent, or superiority over every classical method
has been proved. Input/output size alone does not certify the answer:
checking the canonical factorial by multiplication takes Theta(p) factors.

## 2. Public Character, Field And Integral Basis

Choose i_p=min(2^k modp, -2^k modp) in [0,p). Since (2/p)=-1,
i_p^2=-1. Define chi(a)=i^j when a^k=i_p^j; chi(0)=0. This four-case
comparison is polynomial(logp), coherently as well as classically.
There is no discrete-log oracle. chi(-1)=-1 and c=chi(2) is +/-i.

Compute J=J(chi,chi)=a+ib exactly using the already audited classical
Jacobi algorithm (JACOBI_GROUP_RING_RECOVERY.md). Its negative-exponent
character convention requires eta=i_p^-1, not eta=i_p; otherwise the
returned sum is conjugated. Thus a^2+b^2=p, a is odd and b is even,
both nonzero. Parity follows by pairing x with1-x in the Jacobi sum;
the fixed term at1/2 is chi(1/2)^2=-1, so J=-1 mod2Z[i].

Construct K=Q(theta) by

    theta^4+p theta^2+p b^2/4=0,
    r=(2theta^2+p)/a,
    sigma(r)=-r,             sigma(theta)=b r/(2theta).       (1)

These are polynomial-bit exact algebraic data. To identify the field,
let tau=tau(chi), tau'=tau(bar chi) in Q(zeta_p,i), and use

    tau^2=J sqrtp,  tau'^2=bar J sqrtp,  tau tau'=-p,
    theta=(tau+tau')/2,       theta^2=(a sqrtp-p)/2.

The sum defining theta has rational coefficients Re chi(a), so theta
belongs to Q(zeta_p). The automorphism zeta_p->zeta_p^g with chi(g)=i
sends tau to -i tau and tau' to i tau'; hence (1), sigma^2theta=-theta.
This identifies K as the cyclic quartic subfield, with complex conjugation
sigma^2, real subfield Q(sqrtp), conductor p and discriminant p^3.
The imaginary theta and its irrational square show degree exactly four.
These exponential sums identify the field in the proof; none are expanded
to construct the input.

An explicit integral basis is available without a maximal-order oracle:

    eta0=(r-1+2theta)/4,       eta2=(r-1-2theta)/4,
    eta1=(-r-1+2sigma(theta))/4,
    eta3=(-r-1-2sigma(theta))/4.                         (2)

Indeed {zeta_p^a:1<=a<p} is an integral basis of Q(zeta_p); its H-invariant
integer combinations, H=ker chi, are exactly its four orbit sums eta_j.
These equal (2). Thus they form the full O_K integral basis, and
sigma(eta_j)=eta_(j+1). Multiplication in Q[theta] supplies its integer
multiplication table in polynomial bit time. For p>5, mu(K)={+1,-1}:
an odd root of unity would force its prime conductor to be p and degree
p-1<=4; i is excluded by the unique real quadratic subfield.

## 3. What The Class Module Determines

Set z=L(0,chi)=-(1/p)sum_(a=1)^(p-1) a chi(a). The displayed sum is a
definition/diagnostic, not the algorithm for z.

Actual source: [Greither2007, Corollary8.7 and Section2 equations8--10](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8FC72811C1D6E37F74B89EE96727F257/S0010437X07002965a.pdf/determining-fitting-ideals-of-minus-class-groups-via-the-equivariant-tamagawa-number-conjecture.pdf).
For absolutely abelian CM K with a 2-power number of roots of unity,
Fitt_R(Cl_K^(dual,minus))=S'_Ku(K/Q)^minus, with
R=Z[1/2][Gal(K/Q)]/(1+sigma^2). This corollary is unconditional for
absolutely abelian K (Theorem1.1); no unproved ETNC assumption is added.
Its dual convention is (gamma f)(x)=f(gamma x), NOT f(gamma^-1 x).
Its omega satisfies chi(omega)=L(0,chi^-1).

Here only p ramifies and its inertia group is all C4. The local module
U_p=<N_G,1-(N_G/4)F_p^-1> projects to the unit ideal in R, since N_G
vanishes there. Therefore under R=Z[i,1/2], sigma->i,

    Fitt_R(Cl_K^(dual,minus)) = (bar z).                    (3)

It is bar z, not z. With this SAME-action dual, a finite Gaussian module
and its dual have the same Fitting ideal: over the Gaussian PID decompose
into R/(pi^e); its dual has the same annihilator (pi^e) and cardinality,
so has the same cyclic summand. Thus the computed class module itself
suffices. This argument is not valid after silently replacing the dual
action by the usual inverse-action convention.

The localization at2 loses precisely a known factor. Write C_j for the
quartic residue classes and M_j=(sum_(a in C_j) a)/p. Since each C_j is a
coset of a multiplicative subgroup of odd order k>1, its sum vanishes
modp and M_j is integral. Oddness gives M_(j+2)=k-M_j. Consequently

    z=-[(2M_0-k)+i(2M_1-k)] in Z[i].

Both coordinates are odd. Thus v_(1+i)(z)=1 EXACTLY. Recover the integral
ideal (z) by taking the conjugate of the odd part in (3) and restoring
one factor1+i. No assertion that the entire class group is odd is needed.

## 4. Paying For The Class Group And Its Action

Use the published Biasse--Song complete compact S-unit primitive and its
GRH class-group reduction, with the source scope already audited in
HALF_FACTORIAL_COMPACT_ARITHMETIC.md (BS2016 Theorems1.1/1.2 and
2510.02280v2 Section8). Enumerate ALL prime ideals of norm at most
48 ceil(log2|disc K|)^2. This set is stable under sigma; the explicit
integral basis/action computes its permutation exactly. Under the GRH
generator bound its classes generate Cl_K. Enumeration/factorization over
these polynomially bounded rational primes is polynomial(logp).

ONE complete S-unit call supplies compact generators. Their valuation
matrix V has image the full class-relation lattice. Compact factor
valuations and their binary exponents have polynomial total bit size.
Thus Cl_K=Z^d/im V comes with its sigma action as a public permutation of
the d prime-ideal generators. No class-group-coordinate oracle, extra
discrete logs or principal-ideal generator is silently supplied.

Present the Gaussian module by generators e_j, relations the columns of
V and i e_j-e_(sigma j). This imposes sigma^2=-1; after inverting2 it is
exactly the minus part. Compute its Fitting ideal, strip all factors1+i,
conjugate once and restore1+i. Only successful COMPLETE relation output
justifies (3); a plausible finite quotient does not certify completeness.

A polynomial implementation of the Gaussian determinant ideal does not
enumerate all maximal minors. Convert relation columns and their i
multiples to an integer full-rank lattice in Z^(2d) and take HNF. Project
its first Gaussian coordinate: the gcd of the basis coordinates is g.
Gaussian extended Euclid gives w in the lattice with first coordinate g.
The vectors u-(u_1/g)w generate its projection kernel over Z[i]. Delete
the first coordinate and take integer HNF again. Recurse for d coordinates;
the product of the g's generates the determinant/Fitting ideal. Integer
HNF keeps the sizes polynomial in the relation data and lattice-index bit
length; Gaussian Euclidean gcd/Bezout has polynomial bit cost. This
avoids an exponential list of minors or a new arithmetic subsystem.

Canonicalize the recovered ideal as its rank-two integer HNF. A successful
S-unit call gives the same ideal regardless of generating-set choices;
repeat independent calls and take a majority of canonical ideals to
amplify success. This amplifies the common complete-relation event, not a
purported polynomial certificate of the class number.

## 5. Selecting The Gaussian Unit At Constant Phase Accuracy

The preferred L1 approximation is now the unconditional CLASSICAL
randomized dyadic estimator in Section9 of
FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md. Its effective nonquadratic
lower bound applies to this quartic character; simultaneous log/phase
confidence enters the existing error budget, with fresh samples on each
whole-output repetition. The deterministic GRH Euler argument below
remains a valid alternative. Class-group generation still uses GRH;
this substitution neither computes the ideal nor supplies a free Gauss
phase or an exact classical factorial algorithm.

The ideal determines z only up to +/-1,+/-i. The odd-character functional
equation gives

    z = tau(chi)/(i pi) * L(1,bar chi).                      (4)

For example insert s=0 into the completed equation for
Lambda(s,chi)=(p/pi)^((s+1)/2) Gamma((s+1)/2)L(s,chi).
The four candidate associates have angular separation pi/2. Therefore
a phase estimate with error less than pi/4 selects the exact z; no
inverse-sqrtp accuracy is required, even when one coordinate is small.

[van Dam--Seroussi2002, Algorithm3/Theorem1](https://sites.cs.ucsb.edu/~vandam/gausssumdlog.pdf)
provides the normalized Gauss phase in poly(logp,1/epsilon) time, with
expected angular error epsilon. Here epsilon is a fixed sufficiently
small constant. Prepare the character state using the public four-valued
chi, a uniform nonzero field register and phase kickback. An additive
QFT followed by inversion acts on it by tau(chi)/sqrtp. Controlled use
provides a relative phase. Expected-error guarantees give constant
failure probability by Markov; independent repetitions amplify it.
Approximate gates/state preparation are charged to the error budget.

For L(1,bar chi), [Granville--Soundararajan2003, Lemma2.1, pages6--7](https://dms.umontreal.ca/~andrew/PDF/L1chi2002.pdf)
gives a truncated logarithmic series in a zero-free rectangle. The actual
lemma and GRH specialization were visually read, including the error
term; its character is not restricted to quadratic characters. Under GRH
take s=1, sigma0=1/2 and y=(logp)^8, increasing by a universal constant
or treating the finitely many small p directly. The error is

    log L(1,bar chi)
      = sum_(n<=y) Lambda(n)bar chi(n)/(n log n)
        + O(logp*(log y)^2/sqrt y).                       (5)

Only prime powers contribute. Sieving through y and evaluating chi uses
polynomial(logp) work. Effective constants in the standard lemma permit
a fixed absolute error, say pi/32, for the imaginary part. Rational/
interval evaluation of the finite terms uses polynomially many precision
bits. Equivalently choose a sufficiently large universal threshold and
handle its finite initial segment by direct computation; no p-dependent
advice is used. GRH includes this Dirichlet character, not just class-group
generation. A Gauss-phase error at most pi/16 plus this log-phase error
is safely below pi/4. Choose the nearest associate of the ideal generator.

### 5.1. Stronger Classical Phase Calculation Once Half-Factorial Is Paid

The source refresh found a simpler way to supply tau's phase. Compute
F=((p-1)/2)! FIRST using the reviewed half-factorial composition, since
Section6 needs it anyway. Choose a0 from +/-a with a0=1 mod4, and b0
from +/-b so b0=-F*a0 modp. These choices are unique; no search through
representations or supplied signed Gaussian prime is needed. Put
omega=a0+i b0 and s=(-1)^((b0+2)/4) Jacobi(|b0|,|a0|).

[Buell--Hudson--Williams1984, equations1.1,3.3 and3.5](https://mathstat.carleton.ca/~williams/papers/pdf/134.pdf)
states Matthews's quartic Gauss formula with this normalization:

    tau(chi_omega)=i s p^(1/4) sqrt(omega),                (10)

where the complex square root is principal. The parent visually read
pages310 and314; equation1.1 has a MINUS sign in b0=-F*a0, which the
text extraction loses. Equation3.3 defines the character by reduction
modomega, so the residue of i is -a0/b0=-F. Consequently

    tau(chi)=tau(chi_omega)       if i_p=-F modp;
    tau(chi)=-conj(tau(chi_omega)) otherwise.

The second identity is the odd-character conjugation law. Jacobi symbols
and radicals are classical polynomial(logp) computations; only constant
phase precision is required. Equations(4)--(5) then orient the exact
Gaussian ideal without a quantum Gauss-phase call. This is the preferred
composition; the earlier independent quantum phase route remains valid.
The formula is NOT a classical polylogp solution from p alone: its signed
b0 requires the canonical F, and computing that F remains charged.

A parent-only 50-digit diagnostic at p13 and101 compared (10) with
the directly enumerated Gauss sum, using omega=-3+2i and1+10i,
respectively; absolute differences were below3e-50. The functional
equation using a diagnostic digamma evaluation of L1 matched exact L0
below2e-50. This is a sign/convention check only, not an implementation
of the truncated GRH series or the full quantum composition.

## 6. From The Exact L-Value To The Canonical Factorial

Put S=sum_(a=1)^k chi(a)=A+iB and C=sum_(a=1)^k chi(a)^2. These sums
are again identities, not enumerations in the algorithm. Multiplication
by2 in the residue-weighted sum gives halfsum H=(2-bar c)z; multiplication
by4 gives H+2S=5z. Hence

    S=(3+bar c)z/2.                                      (6)

The ordinary imaginary quadratic class-number identity gives

    C=h(Q(sqrt(-p)))/2,      disc=-4p.                    (7)

Here is the residue derivation of (7). Write eta=(./p), psi=chi_(-4).
The odd primitive character eta psi has discriminant-4p; the ordinary
imaginary quadratic class-number formula gives h(-4p)=L(0,eta psi).
Write its weighted sum over1,...,4p as b+jp, 1<=b<p, 0<=j<4.
The b term cancels because sum_j psi(b+j)=0. Also
sum_j j psi(b+j) is -2 for b=0,1 mod4 and +2 for b=2,3 mod4.
Since sum_b eta(b)=0, this gives
L(0,eta psi)=sum_(b=0,1 mod4) eta(b). The two classes are 4a and
p-4a, 1<=a<=k, respectively. Both have character eta(a), proving (7).
Compute this ordinary class number with the same published quantum
primitive; its degree is2 and discriminant bit length O(logp).
This is the original valid implementation. Section8 below removes that
extra call by reusing the already-paid real quadratic data, computing
only the residue modulo16 that equation(8) actually needs.

If N_j counts the interval values chi(a)=i^j, then
A=N0-N2, B=N1-N3, and N0+N2=(k+C)/2. Thus

    chi(G)=i^E,       E=B-A+(k+C)/2 mod4.                 (8)

Use the reviewed half-factorial composition to compute F=((p-1)/2)!
modp. The SAME compatible Jacobi sum gives its required square directly:

    G^2=-F/(2a) modp.                                    (9)

Indeed at i->i_p the Jacobi sum reduces to sum_x x^k(1-x)^k=0,
by power sums (degree2k<p-1). At i->-i_p it reduces to
sum_x x^(3k)(1-x)^(3k)=binom(3k,k): only exponent4k contributes,
and its sign is positive because k is odd and sum_x x^(4k)=-1.
The first reduction makes the second equal2a. Finally
binom(3k,k)=-binom(2k,k) modp by replacing each numerator2k+j
with -(2k+1-j). Since binom(2k,k)=F/G^2, equation(9) follows.
This pays the orientation directly, without a separately signed
sum-of-two-squares representation. It agrees with the standard Gauss
congruence displayed in the actual Chowla--Dwork--Evans1986 source.

Find the two square roots in polynomial(logp) randomized time, with
bounded clocks/error budget. Select the unique t satisfying t^k=i_p^E.
Uniqueness follows from k odd, equivalently chi(-1)=-1. Square-root
checks alone cannot identify the canonical root; (6)--(8) supply the sign.

## 7. Resources, Failure Semantics And Decisive Controls

The preferred implementation now uses only TWO number fields: the real
quadratic half-factorial field and the cyclic quartic field. Section8
amplifies the real block's JOINT finite output (F,h(-4p) mod16), rather
than selecting an arbitrary unit from a block with the right F alone.
Everything except the imported quantum arithmetic is classical
polynomial(logp) using Section5.1; the earlier route alternatively uses
a constant-accuracy quantum Gauss phase. Only a fixed number of arithmetic
fields/outputs is needed. Amplify EACH arithmetic output to failure at
most eta/10 (the joint real-block pair and canonical quartic ideal),
and use a union bound with phase/state/gate and
square-root errors. Time and space are polynomial(logp,log1eta). The
overall guarantee is BOUNDED ERROR. Root tests, integrality and norm
checks do not certify class-group completeness or the canonical answer.

The completed exact control predeclares p13,29,37,53,61,101,109,149,173,
181,197,229 for a cheap character-only scan, stopping at the first
nonunit odd ideal not associated to its conjugate. That is p101:
z=-3+i and z/(1+i)=-1+2i. Certified quartic class/action computations
were restricted to p13 and101. The latter detects reversed sigma/character
orientation; the former retains a trivial odd class module with the
nontrivial missing factor1+i. Compare endpoints with direct factorials
only as diagnostics. Finite checks never prove (3) or the complexity.

The script/artifact are classical_baselines/quarter_factorial_arithmetic_control.py
and same-stem.json. All used quartic and quadratic class groups passed
PARI bnfcertify. Atp13, L=1-i, Cl_K trivial and G=6. Atp101,
L=-3+i, J=-1-10i, Cl_K=C5 with sigma acting by2. Its Gaussian presentation
is <5,5,i-2>, Fitting ideal=(-1-2i); restoring1+i gives (bar L),
norm10. Omitting that factor fails integrally; using unconjugated L also
fails. The endpoint selects G=46; conjugating L wrongly selects55.
Omitting the division by2 in (6) leaves no matching root in either case.
The parent inspected code and exact artifact, including the equivalent
direct-J square target. The control uses directly enumerated L, not the
algorithm's canonical-unit selection, and uses a cyclic presentation at
these primes rather than implementing the general HNF recursion.

Independent actual-text reviews covered Sections1--7 and a separate
review accepted the later Section5.1 simplification; parent derivations
and actual-source checks agree. No
quantum implementation, generic compiler, larger scan or registry
promotion is authorized. Compare independent
high-upside directions before extending to further denominators; a
fixed-degree composition is not itself the repository's ultimate goal.

## 8. Output-Specific Classical Audit And Shared Quadratic Data

2026-11-06 follow-up checkpoint. The scientific question was whether
classical reciprocity already supplies the canonical sign without a full
class computation. The corpus been-tried lookup found the existing
arithmetic notes; the baselines catalog had no direct keyword match, which
does NOT imply the absence of classical algorithms. The actual classical
congruences below sharpen the comparator and remove one quantum call.
No classical polynomial-time solution from p alone follows.

### 8.1. The precise residues needed, and the mod8 substitution

Write z=x+iy, c=chi(2)=s i with s=+/-1, and H=h(-4p). Both x,y are odd.
Equation(6) gives B-A=((3-s)y-(3+s)x)/2. Therefore equation(8) reduces to

    E = y+2+(k+H/2)/2 mod4,   if s=+1;
    E = 2-x+(k+H/2)/2 mod4,   if s=-1.                   (11)

The exact outputs used here are H mod16 and one coordinate of z mod4.
[Williams--Currie1982, equations0.3 and1.8](https://people.math.carleton.ca/~williams/papers/pdf/122.pdf)
give H=-a0+b+1 mod8, with a0=1 mod4 and b=+F*a0 modp. The parent
visually read pages969--972; independent review agrees. Its PLUS sign
differs from the Matthews normalization in Section5.1.

Directly substituting this mod8 congruence does not select the root in
(11): replacing H by H+8 changes E by2 and reverses chi(G). This is a
failure of THAT substitution only. It does not establish ambiguity from
the full public input p or exclude other classical formulas. Also its
signed b already requires the canonical F; it is not free input advice.

### 8.2. The stronger source removes the imaginary class-group call

Actual source: [Kaplan--Williams1982, pages375--376, equations1.3--1.4
and Theorem1](https://people.math.carleton.ca/~williams/papers/pdf/123.pdf).
Here the paper writes h(-p) for the ordinary class number of Q(sqrt(-p)),
which is our H=h(-4p); it uses a radicand convention. Let epsilon>1 be
the positive fundamental maximal-order unit of Q(sqrtp), and h_R its
ordinary maximal-order class number. Let B=Z[sqrtp], let eta=T+U sqrtp
be its positive fundamental unit, and let kappa be its order class number.
The source gives

    eta=epsilon,  kappa=3h_R, if epsilon belongs to B;
    eta=epsilon^3,kappa=h_R,  otherwise;
    H=T*kappa mod16.                                     (12)

No fundamental Pell coefficient or class number is supplied by the native
input. They are already PAID outputs of the half-factorial construction.

There is a uniform version that avoids the branch in (12). Put

    T3=Tr(epsilon^3)/2,
    H=h_R*T3 mod16.                                      (13)

Since p=5mod8, 2 is inert and O/2O=F4. Every unit cubed is1 mod2O,
so epsilon^3 belongs to B and T3 is an integer. If epsilon is not in B,
(13) is immediate from (12). Otherwise eta=epsilon=T+U sqrtp with
T even (indeed T=2 mod4), Norm(epsilon)=-1. Hence
T3=4T^3+3T=3T mod16, while kappa=3h_R, proving (13).
Equivalently, with t=Tr(epsilon), T3=(t^3+3t)/2.

### 8.3. Compact evaluation modulo32 and shared success

Use O=Z[omega], omega=(1+sqrtp)/2. Evaluate the compact epsilon modulo
32O; no coefficient of the expanded unit is computed. More explicitly,
for each small exact factor gamma=A+B omega, its 2-adic valuation is
min(v2(A),v2(B)), since reduction in the integral basis is over the field
F4. Strip that power of2. The resulting coefficients have odd denominators,
and the factor is a unit modulo32O; its inverse is its conjugate divided
by its odd norm. Binary modular powering handles positive or negative
compact exponents. The total valuation is zero for epsilon, so the product
of normalized factors gives its actual residue. Individual nonunit factors
are permitted. All factor/exponent data have polynomial bit length.

Cube this residue. If epsilon^3=A+B omega mod32O, then B is even and

    T3=A+B/2 mod16

is well-defined. A different representative B+32 changes B/2 by16.
The multiplication table depends only on (p-1)/4 mod32, and the residue
ring has1024 elements. The work is polynomial in the compact encoding and
logp. This is the previously proved compact-residue interface specialized
to a particularly simple inert prime, not a new subsystem.

Retain the primitive positive epsilon and h_R INSIDE the same successful
real S-unit block used for half-factorial. Return the finite canonical
pair (F,H mod16) from that block. A complete-generator success event
proves BOTH coordinates simultaneously. Independent repetitions and
majority of the PAIR amplify that common event. Do not take a majority
of F alone and then trust an arbitrary accompanying unit/class number.
The quartic ideal is amplified separately as before. The guarantee stays
bounded error with polynomial(logp,log1eta) resource bounds under GRH.

The existing certified controls already cover both cases of (12).
Atp13 epsilon=1+omega, h_R=1; epsilon^3=13+10omega, so T3=18 and
H=2 mod16, matching certified H=2. Atp101 epsilon=9+2omega, h_R=1;
epsilon^3=3629+802omega, so T3=4030 and H=14 mod16, matching
certified H=14. These are direct exact checks from the saved artifact;
they do not execute compact quantum arithmetic or require a new scan.

### 8.4. Independent direction comparison

An independently proposed alternative was to compute the volume of a
hyperbolic knot from its explicit braid/diagram by a unitary colored-Jones
circuit followed by the volume-conjecture limit. Its intended cost was
polynomial in diagram length and inverse additive volume error; it would
require a color parameter N bounded polynomially in those inputs and a
paid logarithmic estimate. The relevant classical baseline is geometric
triangulation/gluing-equation computation, not enumeration of Jones
coefficients; supplied well-conditioned shape data would already make
volume evaluation classical.

The first proposed circuit operation fails an exact representation test.
[AJL, Claim2.6 and Definition3.2](https://arxiv.org/pdf/quant-ph/0511096)
uses path labels1,...,N-1 and weights sin(pi*j/N). The N-dimensional color
needed by [Murakami--Murakami, Theorem2.1 and Conjecture5.1](https://arxiv.org/pdf/math/9905075)
has quantum dimension [N]=sin(pi)/sin(pi/N)=0 and is absent in that
unitary quotient. The reduced colored-Jones value is defined before
specialization; dividing a zero trace by zero is not the required circuit.
The parent checked these actual source definitions after the independent
derivation. No alternative polynomial-normalization representation or
uniform effective convergence bound was supplied. This rejects only the
direct AJL/volume-limit composition, not topological quantum algorithms
or the volume conjecture. No code or follow-up subsystem is admitted.

Section8 core/source review, uniform simplification and actual-text
integration review accepted. The independent topology comparison also
passed actual-text scope review. The parent verified the derivations,
primary source statements and the two exact arithmetic substitutions.
The classical status of the necessary z-coordinate mod4 remains UNKNOWN;
absence of an attack is not hardness. Any further arithmetic pass needs
a concrete operation for that residue or another externally valuable
output, compared with an independent candidate before work begins.

## 9. Residue Restatement And A Scoped Classical Shortcut Failure

Given the ALREADY PAID pair (Fhalf,Hmod16), put Q=(2k+H)/4 mod4.
The previously proved sign formula reduces, for z=x+iy and c=chi(2), to

    c=i:  E=y+2+Q mod4;       c=-i: E=2-x+Q mod4.

Thus the required coordinate R=y mod4 or x mod4 is polynomial-time
equivalent to the canonical quarter-factorial G RELATIVE TO those supplied
quadratic outputs. R gives E and selects the correct square root of
-Fhalf/(2Re J). Conversely G gives i^E=chi(G) by modular powering and
four comparisons, then the displayed formula gives R. For p5mod8 the
square root is deterministic: for the known square u use t=u^((p+3)/8);
t^2 is u or -u, corrected with i_p when needed. No discrete-log oracle.
This is an auxiliary-input equivalence, not a classical algorithm from p.
Merely renaming the missing sign as a Bernoulli residue makes no progress.

After stripping its unique1+i factor, the odd ideal I=(alpha) of Z[i]
satisfies I+(4)=Z[i]: Norm(alpha) is odd, so alpha is invertible modulo4
with inverse bar(alpha)/Norm(alpha). Its reduced ideal is the unit ideal,
and the corresponding odd module tensor Z[i]/4 vanishes. This defeats
only recovery from that REDUCED IDEAL or ABSTRACT MODULE. A raw
presentation matrix can retain information (the1x1 matrix [alpha] still
displays alpha mod4); arbitrary processing of its entries is not ruled
out. Greither's ring already inverts2 and has no unital map to Z[i]/4,
so the reduction statement concerns the integral odd ideal first.
Both scoped deductions received independent review; no hardness follows.

The parent checked actual primary classical comparisons before the next
direction. Louboutin2001, Section3.1 Theorems5/7, uses the explicit
truncation M>=A_chi(lambda log A_chi)^(m/2); for L=Q this is of order
sqrt(p logp). Remark8 assumes the root number known in that bound.
[Original paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C0DC557393DB837B785975F56308DF3A/S0027763000022170a.pdf/computation-of-l0-x-and-of-relative-class-numbers-of-cm-fields.pdf).
Chocian2026 Theorem3.1 is an exact character Fourier identity with p-1
terms at conductor p, not a paid polylog algorithm; Theorem3.2 uses an
ODD auxiliary prime and does not supply this modulo4 computation.
[Actual theorem body](https://arxiv.org/html/2607.27503). These source
scopes do not establish the absence of a faster classical algorithm.
The stronger general class/unit comparator is now actual
deBoer--PelletMary--Wesolowski Theorem1.3: fixed-degree L_Delta(1/2)
under ERH without additional smoothness heuristics; see
UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md Section4 for its full scope.
An independent curve-zeta/Jacobian-order proposal is already Kedlaya's
algorithm, recorded in INVERSE_TRACE_RAY_CLASS_SCOPE.md; no new candidate
or implementation was admitted from that rediscovery.

The next candidate has a different exact output: all coefficients of
L(0,chi) for any FIXED power-of-two character order. Its specific blocker
is unit ambiguity in the coefficient field, and its construction/limits
belong in FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md.
