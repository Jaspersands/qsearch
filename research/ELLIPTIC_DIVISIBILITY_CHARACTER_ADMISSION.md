# Elliptic divisibility characters: native-source admission

6 November 2026. SOURCE DISTINCTION AND IDENTIFIABILITY CHECK,
independently reviewed. No efficient reconstruction algorithm, novelty,
separation or quantum execution is claimed. The Section4 exact reduction also passed independent actual-text review;
it is a candidate mechanism, not an admitted end-to-end solver.
Sections5--7 and the all-index collision examples also passed independent
core and actual-text review. No efficient decoder was inferred.

## 1. The published native question

Actual [Shparlinski--Stange, Character Sums with Division Polynomials,
Canad.Math.Bull.55(2012),850--857, Section6](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6D1DC44634CB19BEF784CE153323C084/S0008439500021871a.pdf/character-sums-with-division-polynomials.pdf)
asks to recover a hidden elliptic-curve point P from a black box returning
chi(Psi_n(P)) for integer n. The parent read Section6 and Lemmas3.1--3.3,
not just an abstract. Here Psi_n is the standard division polynomial and
chi(0)=0. Take the explicit known-curve, known-prime-field variant first,
E/Fp, p>=5; P is not supplied. A quantum version must explicitly supply
coherent XOR access to these ternary values, including zero, at the paid
bit length of n. Classical and coherent access must not be interchanged.

This is externally posed reconstruction work, distinct from the recent
class-group applications and from generic lattice-cooling conjectures.
Corpus queries for elliptic-character shift and then elliptic-divisibility
hidden-point reconstruction preceded the focused literature check. No
matching local reconstruction theorem was returned; this is not a novelty
certificate. The broad baselines lookup returned an irrelevant Siegel
reverse-transport row, not a valid attack on this oracle. A specialized
classical baseline is still required before any quantum implementation.

## 2. First exact falsifier: the requested point need not be unique

For all n, standard division polynomials obey

    Psi_n(-P) = (-1)^(n-1) Psi_n(P).                          (1)

Odd n uses a polynomial in x; even n has one factor2y times a polynomial
in x. Zero values remain zero. Therefore if p=1mod4,

    chi(Psi_n(-P)) = chi(Psi_n(P))       for EVERY n.         (2)

For order(P)>=3 these are distinct points. Exact recovery of the original
P is not identifiable in this input model. Returning the sign orbit is
necessary, but has NOT been proved sufficient: exceptional automorphisms
or further sequence collisions may enlarge the equivalence class. For
p=3mod4, n=2 separates P and-P because Psi_2(P)=2y(P) is nonzero for
order>=3. This does not establish full identifiability in that case.
The independent reviewer checked that the cited Section6 and Lemmas3.1--3.3
do not resolve this ambiguity; a period dividing2*ord(P) is not uniqueness.

## 3. A tempting different source must not be substituted

A separate trial idea assumed chosen POINT queries

    F_S(Q)=chi(x(Q+S))

for an unknown additive shift S. For Q=(x,y), S=(z,v) on
E:y²=x³+a x+b, with x!=z, the exact group-law identity is

    x(Q+S)x(-Q+S) = Q_z(x)/(x-z)²,
    Q_z(x)=(xz-a)²-4b(x+z),
    disc_x Q_z =16b(z³+a z+b)=16b v².                       (3)

Both identities were checked symbolically over QQ[a,b,x,z], by reducing
y² and v² using the curve equation; both remainders were exactly0. For
b nonsquare and v!=0, Q_z is irreducible (z=0 is then impossible).
This suggests masked quadratic-character reconstruction from a known
curve's x-coordinates. But the native INTEGER oracle in Section1 does
NOT provide F_S(Q), nor arbitrary translates of the hidden point. Lemma3.2
only composes scalar multiples of the SAME hidden P. No paid reduction
between the sources has been supplied. Thus no translated-coordinate
receiver, simulated elliptic oracle or implementation is admitted here.
Exceptional x=z, infinity padding and masking would also need payment.

The [Farashahi--Shparlinski elliptic-bit paper](https://arxiv.org/abs/1005.4771)
was read for its actual input definitions: it studies characters of
x(nP) and related sequences, not this arbitrary translated-point access.
Its pseudorandomness results are not a source converter or hardness proof.

## 4. A source-correct operation for the next pass

Actual Lemma3.2 gives Psi_(nm)(P)=Psi_n(mP) Psi_m(P)^(n²).
Hence, whenever mP!=O,

    chi(Psi_(2m)(P)) = chi(2y(mP)).                          (4)

This uses a LEGAL integer query and removes the fourth-power factor.
The independent actual-text review accepted this reduction: query the
INTEGER2m, not its residue modulo r. Coherent value/XOR access is required
for the one-query wrapper; classical evaluations or phase copies do not
automatically provide it.
On the explicit additional promise P belongs to a PUBLIC subgroup of odd
prime order r with generator G, write P=[k]G, k!=0. Choose a public
primitive element g of F_r* (factor r-1 with charged Shor if needed).
For j in Z_(r-1), put m=g^j modr and define the public reference

    h(j)=chi(2y([g^j]G)).

Then the native query2m returns h(j+s), where k=g^s modr. Public scalar
multiplication computes h in polynomial(logp,logr) time; the query index
has O(logr) bits. No discrete logarithm of the UNKNOWN point is used.
This is an exact reduction to a BOOLEAN cyclic hidden shift, not an
injective hiding oracle and not yet a Kuperberg or polynomial algorithm.
The quantum XOR wrapper, if the native source is coherent, uses only
public reversible arithmetic and one native query. The theorem's subgroup
promise is extra explicit input, not a conclusion for arbitrary P.

Single most important next question: does this reference family permit
a paid informative receiver and point decoder under a correct output
ambiguity, after the strongest classical attacks? Start by testing exact
sequence collisions and legal algebraic character identities, not by
assuming injectivity or a Fourier-phase oracle. For p=3mod4, h(j+(r-1)/2)
=-h(j), but balanced signs do not prove separation of OTHER shifts.
Expected target is polynomial(logp); even a subexponential composition
needs a paid noninjective-to-injective step or another appropriate receiver.
Resources include public subgroup construction if not supplied, factoring,
index lengths, source calls, Fourier/decoder precision and verification.
No quantum advantage, absence of a classical polynomial attack, or
all-input identifiability is assumed.

Next command: specialized corpus baselines for EDS character reconstruction,
then the actual primary literature on normalized EDS/hidden-point attacks.
Expected artifact: a source-correct classical attack, an exact collision
falsifier, or an explicit receiver contract with all separation assumptions
proved. Acceptance forbids replacing(4) with the stronger oracle in(3).


## 5. Exact normal form: odd indices add no information

For ANY hidden point P of known odd order r>=3, not only prime order,
put f_P(n)=chi(Psi_n(P)), u=(r+1)/2, and

    e_P(m)=chi(2y([m]P)) for m modr !=0; e_P(0)=0,
    a_P=e_P(u)=f_P(r+1) in {+1,-1}.

Then, for every positive integer n,

    f_P(n)=e_P(u*n modr) * a_P^n.                           (5)

Proof: [(r+1)]P=P and the published multiplication identity give
Psi_(n(r+1))(P)=Psi_n(P) Psi_(r+1)(P)^(n²).
The character of the left side is e_P(un), by(4), and a_P^(n²)=a_P^n.
Multiply by a_P^n, its own inverse. If r divides n, both sides vanish;
no division by a zero value is used. This proof does not require a
perfect-periodic normalizer or gcd(r,p-1)=1.

Consequently the complete integer oracle and the even-coordinate oracle
have EXACTLY the same point-collision classes. One initial legal query
r+1 obtains a_P; each subsequent full answer uses public reduction
un modr and one even query2(un modr), with a zero output handled locally.
All queried integers have O(logr) bits after the original n is read;
parity is taken from the original INTEGER n. Conversely(4) uses one full
query. A coherent VALUE wrapper has the same reduction with public
reversible arithmetic and the retained classical anchor. It does not
upgrade a classical source or a supply of phase states.

In the prime-order public subgroup case put b(m)=chi(2y([m]G)), m!=0.
Its multiplicative stabilizer

    H={t in F_r*: b(tm)=b(m) for every m in F_r*}

is a subgroup. Hidden P=[k]G and P'=[k']G have identical FULL sources
iff k'/k belongs to H. Thus kH is the correct information-theoretic
output class; efficient computation/certification of H has NOT been paid.
For p3mod4, b(-m)=-b(m), so -1 is not in H, but H can still be nontrivial.
This is an exact source characterization, not a recovery algorithm.

## 6. A prime-order collision beyond the sign ambiguity

On E/F7:y²=x³+3, #E=13 and G=(1,2) has order13. The automorphism
rho(x,y)=(2x,y) has order3, commutes with scalar multiplication and
preserves y. Therefore e_(rho P)(m)=e_P(m) for every m, and(5) implies

    f_G(n)=f_[3]G(n)=f_[9]G(n) for EVERY n,
    [3]G=(2,2), [9]G=(4,2).                                (6)

These are three distinct points, not sign pairs, even though p3mod4 and
the ENTIRE group has odd prime order. It refutes unconditional original-
point recovery under the Section4 subgroup promise, and refutes the claim
that excluding the p1mod4 sign ambiguity suffices. The analytic proof
comes from the explicit automorphism; it is not extrapolated from data.
Parent Sage verification independently confirmed the group order,
multiples, all26 native values for this triple, and(5) for all12 nonzero
points and n=1..26, using standard Psi2=2y conventions.

One separate, prespecified generic-j control was run by the helper:
E/F43:y²=x³+x+3 has #E=47, j=1, G=(2,20). Its b has23 signs of each
kind, stabilizer{1}, and minimum multiplicative-shift distance16/46.
The46 full sources on n=1..94 have no collisions, minimum distance32/94.
Psi2/Psi3 conventions, all2116 even-query identities and a second period
were checked exactly. This is FINITE SEPARATION ONLY, not asymptotic
identifiability, hardness or evidence for a quantum algorithm. No larger
scan is queued.

Excluding exceptional j-invariants alone also FAILS. On
E/F13:y²=x³+4x+8, P=(4,6) has order5, with

    2P=(5,7), 3P=(5,6)=-2P, 4P=(4,7).

The doubling slope is0 and the next addition slope is1. All four points
have2y in{1,12}, both squares modulo13. Thus e_Q(m)=1 for5 not dividingm,
and(5) gives f_Q(n)=1 for5 not dividingn, zero otherwise, for ALL four
nonzero Q in the subgroup. The curve has discriminant2 and j=7,
where1728=12mod13. Parent Sage and independent algebra review confirmed
these coordinates, orders and invariants. This is another exact all-index
counterexample, not a numerical conjecture. It does NOT refute the narrower
SIMULTANEOUS p3mod4/generic-j/whole-group-prime promise. One targeted
F11 control with E:y²=x³+5x+1, whole order11 and j=6 had trivial stabilizer;
that supplies no theorem for the narrower promise. No more cases queued.


The generic-j plus p3mod4 repair fails in an INFINITE fixed-order family.
Start with the rational Tate curve

    C: y²-xy-4y=x³-4x², P=(0,0),
    2P=(4,8), 3P=(2,2), 4P=(2,4)=-3P.

Thus P has order7. The change X=x-5/4, Y=y-x/2-2 gives

    E: Y²=X³-(43/16)X+83/32,
    Delta=-1664=-2^7*13, j=-2146689/1664,
    2Y(P),2Y(2P),2Y(4P) = -4,8,2.                         (7)

For EVERY prime p3mod8 with p>3, the curve has good reduction and P still
has order7. All three listed values are nonsquares: chi(2)=-1 and
chi(-1)=-1. Their negatives are squares. Consequently, on F7*,

    e_P(m) = -(m|7),       H={1,2,4},
    f_P(n)=f_[2]P(n)=f_[4]P(n) for EVERY n.                 (8)

Here (m|7) is the Legendre character modulo7, not modulo p. Reduction
preserves these nonzero points and their order; p7 is outside this prime
progression. Removing p43 and83 also ensures j is neither0 nor1728:
c4=129, c6=-2241, so the only relevant extra prime divisors are43,83.
Dirichlet's theorem gives infinitely many remaining primes. Parent Sage
checked the rational model and the p11 instance, and independent algebra
review accepted the entire family. At p11 the short model is
Y²=X³+9X+5, G=(7,9), j=9, #E=14 and ordG=7; the multiplier stabilizer
is exactly{1,2,4}. This strengthens the identifiability falsifier without
a larger scan. It is a FIXED-order7 family, not a growing-order complexity
result, and it does not satisfy the whole-group-prime promise. That
remaining simultaneous promise is still unresolved.

## 7. Actual classical-source comparison and remaining obligation

The specialized corpus baseline query found no catalogued match; this
absence is not evidence of hardness. The parent read actual Sections3,
4,7,8 of [Lauter--Stange, The elliptic curve discrete logarithm problem
and equivalent hard problems for elliptic divisibility sequences](https://arxiv.org/abs/0803.0728).
Their Theorem6 supplies a perfectly periodic normalization when the point
order is greater than3 and coprime to q-1. Theorem8 computes its VALUE
from a SUPPLIED point in polynomial time; Theorem9 recovers a point from
three FULL normalized field values. Neither converts a single character
bit into those values. The EDS-Residue parity reduction in Proposition3
and Corollary2 starts with SUPPLIED base P and Q=[k]P and an oracle for
the unknown-index residue Psi_k(P), under its stated normalizer promise.
Our source instead hides P and accepts KNOWN integer indices. That
reduction is neither a classical attack on this source nor a hardness
reduction for it. Proposition4 also requires the supplied point Q.

Actual [Jao--Jetchev--Venkatesan, On the Bits of Elliptic Curve
Diffie-Hellman Keys, INDOCRYPT2007, Sections2.1 and4.1--4.2](https://djao.math.uwaterloo.ca/wiki/images/8/82/Indocrypt-2007.pdf)
already formulate the multiplier hidden-number problem with analytic
extractor chi(x([m]P)). They separate uniqueness from reconstruction:
their analytic separation is conjectural and efficient decoding is not
supplied. Their proved fixed-extension algebraic-coordinate reconstruction
has DIFFERENT outputs. Neither result converts the present chi(2y) source
into its stronger algebraic data, and no new broad hidden-number framing
is claimed here. The actual source text, not only its abstract, was read
and independently checked.

Exhaustive point/sequence matching is a legal classical comparator.
Computing all b values and cyclic correlation after choosing a primitive
root gives a complete shift-class list in polynomial(r,logp) time; even
paying classical factorization/primitive-root enumeration stays polynomial
in numerical r. It is exponential in logp when r is of order p.
Polynomial QUERY counts do not remove this classical time. A stronger
classical reconstruction algorithm on the exact source remains UNKNOWN.

The proposed quantum mechanism remains the Boolean cyclic shift(4),
with target polynomial(logp,logr) time and paid coherent native queries.
It has no proved phase inversion, informative receiver or decoder.
Generic injective hidden-shift algorithms cannot simply be invoked.
An injectivization using random translated tuples would need a proved
minimum shift-disagreement bound outside H and a paid treatment of H;
nonconstant/balanced b does not provide such a bound. For arbitrary Boolean
references even a KNOWN trivial stabilizer is insufficient: a public
singleton indicator shifted on Z_N is unstructured search and needs
Omega(sqrt(N)) quantum queries. That generic counterexample is NOT a
lower bound for this elliptic family. Weil bounds on
chi(y(Q)y([t]Q)) charge the DEGREE of [t], ordinarily t², and do not give
a uniform constant just because scalar multiplication runs in logt time.
The F7 collision is the first decisive falsifier of all-point recovery.
The F43 test does not repair the missing asymptotic obligation.

Next scientific decision: compare this generic-j/stabilizer-quotient
reconstruction question with independent high-upside native mechanisms
before extending it. Returning here requires a concrete source-correct
operation beyond relabeling it a hidden shift, or a decisive classical
attack. No receiver implementation, simulation, broad sweep, novelty,
separation, all-input uniqueness or quantum execution is admitted.


## 8. Independent direction comparison and disposition

Two externally motivated alternatives were compared after corpus lookups,
then parent primary-source checks. Neither examined operation removes its
specific end-to-end blocker, so neither receives implementation work.

* Explicit graph isomorphism: input two adjacency matrices promised
  isomorphic; output a directly verified permutation. Proposed operation:
  coherently sample paired anchors, individualize/refine, and amplify only
  branches that construct and verify a full permutation. Preparation,
  verification and reversal are polynomial in graph size and anchor count.
  If a trial succeeds with probability alpha, classical repetition costs
  O(1/alpha), while this quantum wrapper costs O(1/sqrt(alpha)). Therefore
  a polynomial quantum clock for THIS wrapper already gives a polynomial
  classical clock. Marking mere extendability would require the unpaid
  isomorphism oracle. The independent corpus review also retained actual
  classical individualization successes; Babai's actual Theorem1.1.1 and
  Corollary1.1.2 give the broader quasipolynomial classical baseline
  ([primary manuscript](https://arxiv.org/abs/1512.03547), with the
  [author's restored-bound correction](https://people.cs.uchicago.edu/~laci/update.html)).
  The target polynomial improvement needs a different interference/decoder
  mechanism. This does not rule out quantum graph-isomorphism algorithms.
* Supersingular isogeny: input explicit supersingular curves over F_(p²);
  output an efficiently evaluable connecting isogeny. Proposed operation:
  prepare short small-degree paths, retain histories, mark an endpoint
  isomorphic to the target, and amplify. Field arithmetic, neighbor steps,
  history storage, inverse preparation and map verification are charged.
  The same alpha argument rejects a polynomial-time claim for this
  wrapper. In a near-uniform N-vertex regime it costs order sqrt(N) calls;
  erasing histories is an additional unpaid operation. Classical
  bidirectional path matching is already relevant, and a current primary
  preprint states a stronger unrestricted-degree comparator:
  [Delgado2026](https://arxiv.org/abs/2609.22018), actual Theorems1.1/5.3
  and Corollaries1.2/5.4, claim classical expected p^(1/3+o(1)) time AND
  memory without a smoothness heuristic. Parent read these statements
  and the final reduction, not the full proof; this is an ATTRIBUTED
  preprint baseline, not a new verified repository theorem. Its corollary
  explicitly excludes a prescribed prime-degree path. No constant-degree
  path claim or quantum bound is inferred from it. Even without relying
  on that new preprint, the same-sampler alpha comparison rejects the
  examined route to polynomial time. Other coherent mechanisms remain open.

Decision: park the EDS decoder proposal after the exact source and
collision results. Neither independent search-amplification alternative
is promoted, and neither justifies a subsystem. The most important next
scientific question is a CONSTRUCTIVE one: which motivated native input
admits a new paid operation giving poly(input bits) recovery beyond these
search wrappers? Admission requires a concrete operation and a decisive
classical/source falsifier before any new implementation. This is a
selection obligation, not a claim that any open problem is hard or that
the repository has exhausted possible directions.
