# Sparse characteristic-zero function-field relations

Update13November: EVERY fixed extensiondegree delta now has a REVIEWED
WRITTEN classical polynomial sparse-BIT FULL Rel algorithm, uniformly in
growing variables/atoms/binaryexponents; see SPARSE_CYCLOTOMIC_FIXED_DEGREE.md.
No integerfactoring needed. General growingdelta remains OPEN.

2026-11-06. WRITTEN bounded-error quantum polynomial-bit composition, with
independent core/source/resource and actual-text reviews complete. Full
classical sparse-bit counterparts for degrees1 and2 are also reviewed.
No novelty, separation or full algorithm execution claim.

## Native question and independent selection

Input: F=Q(T_1,...,T_s)[Y]/f, with f monic irreducible of charged numerical
degree delta>=1, and k>=1 nonzero elements u_i in its Y-power basis. Every
rational-function coefficient is an explicit quotient of sparse polynomials
with binary rational coefficients and BINARY T exponents. s,delta,k all grow;
unused variables are dropped. Irreducibility and nonzeroness are promises.
No inverses, factorization, constants, valuations, points or relations are
supplied. Output the full lattice Rel={e in Z^k:u^e=1}, with error<=eta,
in time polynomial in the sparse input BIT length and log1/eta.

Question: does random large-prime specialization preserve all short false-
relation witnesses well enough for a paid finite-ring relation algorithm and
LLL to recover the exact lattice, including algebraic constant units?
Unlike characteristic p, constants need not be torsion. Bounds on their
relation basis and on bad primes must be proved, not supplied as advice.

Selection followed current STATE/TRAPS, corpus been-tried then literature,
and corpus baselines (which returned no precise sparse-relation entry).
Independent alternatives were checked first. Actual Kedlaya0411623v3
Theorem1 and Sections6--8 already supply growing-genus curve zeta via
canonical Jacobian groups; no new operation was identified there. Actual
Ding--Zhan--Preskill--Lin2508.05703v3 Theorems1--3 give mixing promises for
free systems and high-temperature local commuting systems, not the missing
low-temperature lattice transfer. The syndrome-driver alternative repeats
the scoped sqrt(overlap) two-projector gap in NATIVE_SYNDROME_DILATION.md;
no general annealing no-go follows. Growing-degree Legendre reconstruction
still lacks a paid replacement for its factorial split-mask cost. None
justified building a new subsystem. This explicit symbolic-algebra problem
has an end-to-end candidate and a decisive classical attack, so it won this
pass's comparison; it is not selected merely as an arithmetic continuation.

Classical comparators: Lenstra--Silverberg1509.08843 Thm1.11 for explicit
finite Q-algebras (s=0); the earlier fixed-variable/numerical-degree affine
composition; Kreuzer--Walsh2307.09394 valuation algorithms; and Giesbrecht--
Roche0901.1848v2 lacunary perfect-power tests under their actual scope.
Dense factorization or expansion is not polynomial in binary sparse degrees.
Section4 gives a full classical sparse-bit algorithm for delta=1. No
classical lower bound is asserted for delta>1. The quantum candidate reduces
to standard finite abelian HSP/DLog and is not a new quantum primitive.

## 1. Uniform bound including algebraic constant relations

First clear rational scalar coefficients with a COMMON multiplier for each
numerator/denominator polynomial pair, preserving their ratio and retaining
integer polynomials. Let beta>=1 bound numerical total T degree,
L count coefficient denominators, and b>=1 satisfy
prod_P max(2,||P||_1)<=2^b, with occurrences retained. These are computable
bounds of polynomial binary length. Set
m=s+1+L+k, D=max(2,beta+delta+2), B0=k!*D^((m+1)*k).
The proof-only affine domain obtained by adjoining denominator inverses and
unit inverses has these variable/degree bounds. Actual2610.27250v1 Prop3.1
proof gives an Alg basis with infinity norm<=B0, where
Alg={e:u^e algebraic over Q}. Its uniform size proof, not its fixed-parameter
enumeration clock, is used. No presentation or basis power is expanded.

A proof-only finite specialization bounds heights of the constants. Use
Hdeg=L*beta, J=delta^2*(Hdeg+beta), W=Hdeg+k*J. The polynomial formed by
input denominators and generic multiplication-matrix determinants is nonzero
and has degree<=W. Hence some integer t in{0,...,W}^s avoids it. Specialize
to the full nonzero degree-delta Q-algebra and choose ANY residue number
field E, of degree<=delta. Let C_A be the algebraic-over-Q elements in the localized affine domain A.
It is a FIELD: the inverse of any nonzero algebraic element is a polynomial
in that element. It contains every Alg-basis product and maps injectively
into E. The entire constant field of Frac(A) need not be contained in A
(e.g. sqrt2=Y/T in Q[T,Y]/(Y²-2T²)); no such containment is assumed. The point and E are PROOF
objects only, not inputs or computed by the algorithm.

Let Hc=b+beta*ceil(log2(W+1))+1 and H=(delta+1)^4*(Hc+1).
Evaluated coefficient numerators/denominators have bit height<=Hc.
Clearing the at most delta rational coefficients of f_t bounds a root's
logarithmic Weil height by (delta+1)Hc+delta. The elementary height sum and
product inequalities then bound h(u_i(t))<=H in E. Therefore the r<=k
constant products c_j arising from an Alg basis satisfy h(c_j)<=k*B0*H.
Both H and this bound can be huge numerically, but their BINARY lengths
are polynomial. No actual value or expanded product is constructed.

Here is a self-contained sufficient lower height bound. Put
Tdelta=2^(delta+2), Kdelta=delta*(2*Tdelta+1)^(delta+1)+1,
epsilon0=1/(delta*Kdelta).
Every algebraic number of degree<=delta and height<=1/delta has a primitive
integer minimal polynomial whose coefficients have absolute value<Tdelta,
by the Mahler-measure/coefficient bound. There are fewer than Kdelta such
numbers, counting all roots of all padded degree<=delta polynomials. If a
nonzero alpha had h(alpha)<epsilon0, its first Kdelta powers would all lie
in that finite set; two would coincide, forcing alpha to be a root of unity.
Thus every non-torsion element of E has height>=epsilon0. No analytic
unproved assumption or computed constant field is used.

Embed the subgroup generated by the c_j modulo roots of unity into weighted
logs at ALL relevant finite AND archimedean places of E. Its l1 norm is
exactly2h, not merely the archimedean norm. Northcott finiteness implies this
finitely generated image is a discrete lattice. Its real rank is<=k;
nonzero vectors have norm>=epsilon0 and generators norm<=G=2*k*B0*H.
An outer John ellipsoid gives a Euclidean norm between l1/sqrt(k) and l1.
For an abstract3/4-LLL basis of this lattice, Gram--Schmidt lengths are
>=2^(-(k-1)/2)*epsilon0/sqrt(k). Back substitution using |mu_ij|<=1/2
bounds the INTEGER coordinates of every original generator by
M=ceil(2^(3k)*k*G/epsilon0).
The ellipsoid, log lattice and basis are only existence arguments. If the
real rank is0, skip them and use the whole exponent lattice as the coordinate
kernel; the same final bound remains valid.

The integer coordinate matrix therefore has kernel basis bounded by k!*M^k
(the determinant/HNF kernel argument from Prop3.1). This is the lattice of
constant products that are roots of unity. Its exact-relation sublattice has
index at most |mu(E)|<=2*delta^2: phi(w)<=delta and phi(w)^2>=w/2. HNF
and lifting through the Alg basis give a FULL Rel basis bounded by

                   B=2*k^2*delta^2*B0*k!*M^k.                  (1)

This retains nonsaturation. logB is polynomial in the original sparse input.
Independent Codex core and complete algorithm/source/resource reviews
accept this bound and its use. No geometric or logarithmic object above is advice.

## 2. Content and degree bounds for random prime specialization

Set R=2^k*k*B, Fbox=(2R+1)^k, Cdeg=(k+2)*J. Use the formal product Gden
of coefficient denominators. As in the characteristic-p note, multiplication
M_i=A_i/Gden^delta has polynomial matrix numerator degree
<=delta*(Hdeg+beta), and detA_i is nonzero with degree<=J.
The common denominator h=Gden^delta*prod_i detA_i pays M_i and its inverse;
all numerator/denominator degrees<=Cdeg. Unit/denominator bad polynomial
D0=Gden*prod_i detA_i has degree<=W.

Unlike in fixed characteristic, we must pay the chance that reduction
modulo a prime annihilates a NONZERO integer polynomial. Put K=2^b and
U=((delta+1)*K)^(delta+1), V=(delta*U)^delta, S=U*V^k.
Polynomial coefficient l1 norms are submultiplicative. Companion-matrix
expansion bounds every A_i entry and Gden^delta by U; determinants and
adjugates are bounded by V. Every common-denominator matrix numerator,
and h itself, has coefficient l1 norm<=S. For inverse numerators this
uses the sharper estimate
||Gden^(2delta)*adj(A_i)*prod_(j!=i)det(A_j)||_1
<=U^2*(delta-1)!*U^(delta-1)*(delta!*U^delta)^(k-1)<=U*V^k.
Merely substituting the looser adjugate bound V would not prove this line.
D0 has norm<=S.

For a nonrelation e with ||e||infinity<=R, the cleared numerator determinant
N_e of product M_i^e_i-I is a NONZERO integer polynomial: u^e-1 is invertible
in the generic characteristic-zero field. Its degree is<=delta*Cdeg*k*R,
and its coefficient norm is at most

                 (2*delta)^delta*(delta*S)^(delta*k*R).

Let acoef=ceil(log2 S), hcoef=delta*ceil(log2(2*delta))+
delta*k*R*ceil(log2(delta*S)), Zprime=acoef+Fbox*hcoef, and
Zdegree=W+Fbox*delta*Cdeg*k*R. These integers have polynomial BIT lengths;
no determinant, exponent-sized polynomial or product is actually expanded.
Choose integer X>=max(21,16*Zprime/eta,16*Zdegree/eta) and a uniform random
prime p in[X,2X]. For each nonzero polynomial choose one nonzero coefficient
for the PROOF only. A coefficient c has at most log|c|/logX prime divisors
in that interval. Actual Rosser--Schoenfeld Cor3 gives more than
3X/(5 logX) primes for X>=20.5. Thus the chance any selected coefficient
vanishes modulo p is <=2*Zprime/X<=eta/8.

Conditional on surviving coefficients, uniformly choose t in F_p^s.
Schwartz--Zippel plus union bound gives probability<=Zdegree/p<=eta/16
that D0 or any false-relation N_e vanishes. No independence is assumed.
ABORT on an input denominator zero or any specialized nonunit. Keep the
FULL ring B_t=F_p[Y]/f_t with canonical degree<delta labels, including
nilpotents/reducible factors. True relations survive through the INTEGRAL
model R=(Z[T,1/Gden][Y]/f)[u_i^(-1)] contained in F. Monicity gives its
injection into F and pays the coefficient denominators. No homomorphism
from the whole Q-algebra into characteristic p is asserted. True relations
are integer polynomial identities in this model and survive accepted maps;
on the good event every vector in its relation lattice of norm<=R is true.
Irreducibility modulo p is neither needed nor asserted.

## 3. Paid finite relations and exact extraction

For the finite ring use the known period |GL_delta(F_p)| and the explicit
unit multiplication homomorphism from(Z/NZ)^k. Its finite abelian HSP
source, complete kernel extraction, approximate QFT and binary arithmetic
are paid exactly as in FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION.md.
That note's exact LLL prefix proof applies with bound(1): it recovers the
full original Rel, even when nonsaturated. No new quantum subsystem is
implemented. Alternatively the whole finite-ring step reduces classically
to finite-field DLogs with polynomial overhead, including primitive-base
challenge tests and nilpotent lifts proved in that note.

Uniform prime generation uses capped uniform integer trials and exact
polynomial-time primality tests; the interval density above gives a
polynomial(logX,log1/eta) cap. Capped uniform field sampling, HSP generation
and total compiled-QFT errors receive separate confidence budgets, leaving
total error<eta. All bit sizes, including logp, logN, LLL bases, sample counts
and binary powering, are polynomial in native input size and log1/eta.
Unlike the previous fixed-p result there is no fixed-characteristic
quasipolynomial conclusion: this reduction CHOOSES a large growing prime.
No reverse reduction from finite-field DLog is supplied for characteristic0.

## 4. Cheapest classical attack: the entire rational-function case

For delta=1 write u_i=P_i/Q_i with explicit integer sparse polynomials,
retaining scalar ratios, and let A=prod_i ||P_i||_1||Q_i||_1. Set
C0=2*beta*A, Balg=k!*C0^k, Ralg=2^k*k*Balg.
The logarithmic derivative condition
sum_i e_i[(partial_j P_i)/P_i-(partial_j Q_i)/Q_i]=0 for ALL j
holds exactly when u^e is a nonzero RATIONAL constant. Clear the formal
G=prod_i P_i Q_i. The implicit integer coefficient matrix has entries of
absolute value<=C0 and degree<=2k*beta-1. Its kernel has a basis<=Balg by
the same minor/HNF argument, without constructing that coefficient matrix.

For ||e||infinity<=Ralg, the combined numerator has coefficient l1 norm
<=2*k*Ralg*beta*A. Choose a prime larger than this bound so EVERY nonzero
bounded-exponent derivative polynomial survives reduction. Choose it also
large enough for the simultaneous Schwartz--Zippel bound over the exponent
box and the degree of G. Evaluate the s-by-k logarithmic derivative matrix
at one random point where all P_i,Q_i are nonzero. Its integer congruence
kernel M contains Alg. With high probability it contains no false vector
of norm<=Ralg. Classical finite-field linear algebra and LLL therefore
recover Alg exactly in polynomial SPARSE BIT time, without factoring the
polynomials or constructing huge coefficients/powers.

For any fixed monomial order, leading coefficient defines a multiplicative
map Q(T)^* -> Q^*. On Alg, the constant u^e equals
prod_i (lc(P_i)/lc(Q_i))^e_i. Hence

      Rel = Alg intersect Rel_Q(lc(P_1)/lc(Q_1),...,lc(P_k)/lc(Q_k)).

The latter is classical polynomial time via gcd-free integer bases and a
sign congruence, or the actual finite-Q-algebra relation theorem. Intersect
relations of the ORIGINAL small rational numbers; never expand powers of
an Alg basis. This supplies a polynomial classical bound for ALL delta=1 inputs of this
model. It does not solve the general algebraic-extension case or exclude
polynomial quantum improvements.

## 5. A stronger classical attack: EVERY quadratic extension

Let delta=2. Complete the square: z=2Y+b_f for f=Y²+b_f*Y+c_f,
so z²=D=b_f²-4c_f,
and write each u_i=U_i+V_i*z with rational functions U_i,V_i. Irreducibility
means D is not a square in Q(T). All these expressions, and each
N_i=U_i²-V_i²*D, require only a CONSTANT number of sparse additions and
multiplications per unit. Their sparse sizes and coefficient/exponent bit
lengths are polynomial in the original input, even when degrees are huge.
No univariate perfect-square root or dense expansion is computed.

Fix lex monomial order and let v(R),lc(R) denote the leading exponent vector
and coefficient of a nonzero rational function. Put a=lc(D), choose a formal
omega with omega²=a, and let K0=Q(omega) (Q itself when a is a rational
square, tested by exact integer square roots). There is a field embedding
of F into an iterated Laurent series field over K0 with half-integer
exponents, taking z to a square root with leading term
omega*T^(v(D)/2). Here is a proof that avoids an analytic convergence claim:
put x_i=T_i^(-1), with x1 outermost; factor the first leading power of x1,
recursively square-root its leading coefficient in the inner Laurent field,
then use the ordinary x1-adic binomial square root of1+x1*H. Continue
recursively inward. The coefficient at the final leading term is omega.
Every series is PROOF-ONLY, never constructed or truncated by the algorithm.

Its leading-coefficient map LC:F^* -> K0^* is multiplicative. Computing
LC(U+Vz) is inexpensive. If U or V vanishes, or v(U) and v(V)+v(D)/2 differ,
take the evident dominant term. If exponents agree and
lc(U)+lc(V)*omega is nonzero, return that sum. If it is zero, omega is
rational and the conjugate U-Vz has leading coefficient2lc(U), which is
nonzero. Therefore the cancellation branch is EXACTLY

               LC(U+Vz)=lc(U²-V²D)/(2lc(U)).                  (2)

This uses one sparse norm, not a long Puiseux series. Generic irreducibility
ensures that the norm is nonzero for every nonzero input. Fix one branch for all units. Either branch gives a multiplicative map
whose restriction to constants is injective; hence either yields the same
final relation lattice, although individual NONCONSTANT leading coefficients
may change even when both maps restrict to the identity on Q.

Every nonzero element algebraic over Q has valuation0: otherwise its
minimal polynomial has a unique extremal-valuation term. Consequently LC
restricts to an INJECTIVE Q-field map on the algebraic constants. Even sums
are preserved there: a cancellation increasing valuation of a nonzero
algebraic sum would contradict valuation0. Thus

             Rel_F(u)=Alg intersect Rel_K0(LC(u_1),...,LC(u_k)).

Compute Alg classically as in Section4, now retaining BOTH coefficients
in the basis1,z of every logarithmic derivative. The formula

 dlog(U+Vz) = [(U' + (V'+V*D'/(2D))*z)*(U-Vz)]/(U²-V²D)

uses only a constant number of sparse rational operations for each partial
derivative; reduce z²=D. Clear their formal common denominator, bound
coefficient l1 norms by products of the explicit sparse norms, and apply
the same bounded-kernel, large-PRIME, random-evaluation and full-congruence
LLL proof. There are2s rows and polynomially many factors. No inverse oracle/advice or expanded common-denominator product is used;
the displayed rational inverses are computed from their small explicit
expressions. No small-characteristic derivative assumption or specialized
irreducibility is used. Char0 constants are
exactly the simultaneous kernel of these extended derivations.

The ORIGINAL LC(u_i) are explicit elements of a number field of degree<=2
with polynomial coefficient bit size. Actual Lenstra--Silverberg Thm1.11
computes their complete relations classically in polynomial time for growing
k; intersect integer lattices without saturation. No Alg-basis powers are
expanded, and norms alone are NOT substituted for exact constant relations.
This proves a bounded-error CLASSICAL polynomial sparse-bit algorithm for
EVERY promised quadratic input here, including growing s and k. It is a
cheapest classical attack on the quantum proposal, not a general growing-
delta dequantization or novelty claim. Independent mechanism and final actual-text review accepted; one exact
cancellation/binary-exponent control passed.

## 6. Exact control, review dispositions and remaining scope

The sole new Sage control is
`audits/controls/sparse_charzero_relations/binary_quadratic.py` and its JSON.
Native N=2^40+1 stays a41-bit exponent; no T^N polynomial is expanded.
For F=Q(T)[Y]/(Y²-T^(2N)-2) and units(Y-T^N,Y+T^N,2,T), the exact
classical derivative matrix over the full quadratic basis recovers Alg of
rank2 at p=2^61-1. With control-only B_alg=1 and cutoff64, later exact
Gram--Schmidt lengths prove no short vector outside the true Alg span.
The plus branch gives LC tuple(1,2,2,1); the minus branch(-2,-1,2,1).
Both give exactly Rel=Z(1,1,-1,0). The cancellation0 in the naive first
leading coefficient is repaired to1 by the norm formula. Derivative-only
accepts constant2; LC-only accepts nonconstant T. At p=257 dividing N,
the derivative filter falsely accepts(1,0,0,0), catching the essential
large-CHARACTERISTIC condition. All controls passed in one execution.

This is a CLASSICAL source-first falsifier/control, not a quantum HSP run,
generic LS execution, theorem-sized prime experiment, numerical confidence
estimate or asymptotic proof. The existing nontrivial Q(sqrt2) constant-unit
control from the earlier affine pass is reused as context, not rerun.
No broader suite or parameter sweep is claimed.

Parent and independent reviews checked the full quantum argument and both
classical cases against actual sources. Three material wording/representation
repairs are retained in the review record: use C_A rather than assuming all
fraction-field constants lie in A; reduce the integral model rather than a
Q-algebra modulo p; use the sharper adjugate norm for S=UV^k. Final quadratic
review also corrected the branch statement: nonconstant LCs can change even
if the constant embedding is unchanged. Its explicitly computed rational
inverses are paid, not claimed absent. Source snippets, URLs and PDF hashes
are in `audits/sources/sparse_charzero_relations/`; earlier Prop3.1 source
packet is reused. No Claude API call was made in this pass.

Remaining high-value classical question: can an efficiently computed leading-
coefficient map at a place of the algebraic field replace the finite DLog
step, with sparse-bit cost and no hidden constant-field advice? The quadratic
radical/norm construction closes degree2; its constant-depth sparse arithmetic
does not extend automatically to growing degree. General classical complexity
and novelty remain UNKNOWN. No finite-field DLog reverse reduction in
characteristic0, general ideal-presentation conversion, or new quantum
primitive is asserted. Passing controls/reviews never proves a separation.

Next pass must compare this remaining question with independent externally
valuable mechanisms before admitting another extension. No full algorithm
implementation, larger sweep, registry, CLI, website or paper is queued.
