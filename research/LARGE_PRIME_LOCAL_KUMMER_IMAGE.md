# Growing-genus local Kummer images at large primes

Date: 2026-11-06. Status: REVIEWED WRITTEN CLASSICAL COMPOSITION. Independent
core, full-source/arithmetic and final integrated actual-text reviews are
complete. The distinct Claude coordinate audit produced verified repairs.
No novelty, separation, general Selmer or full-algorithm execution claim.

Written theorem: for every native input below and 0<eta<1, a classical
algorithm uses polynomial bit time in d, coefficient input bits, log p and
log(1/eta), and returns a complete local-image basis with probability at
least1-eta. It otherwise returns ABORT. Every returned basis is exact and
uses a returned, fixed coordinate frame. This is a composition of cited
arithmetic algorithms and the deductions below, not implemented software.

## 1. Question, selection and native contract

Can the full local two-descent image of a growing-genus hyperelliptic
Jacobian be computed in randomized polynomial BIT time at every prime
p>2g+1, including arbitrary bad reduction?

Input: explicit monic separable f in Z[X], d=2g+1>=3, a binary prime p>d,
and error bound eta. Coefficient bit size and numerical d are charged.
Let C:y^2=f, J=Jac(C), L=Q_p[X]/f. Output: a complete F2 basis of
delta(J(Q_p)) inside L*/L*^2, in explicit local valuation-parity and
residue-square coordinates. No supplied local points, extensions, factor
decomposition, cluster picture, squareclass basis or source distribution.
The target is poly(d, input bits, log p, log(1/eta)).

External role: this would remove the large-prime local-source obstruction
in growing-genus two-descent. The local operation is classical. A global
quantum composition still needs small/wild/dyadic places and the growing-
degree global class/unit obligations. None is silently supplied here.

Independent comparison considered curve zeta (known Kedlaya route), modular
factorials (already composed locally; Tal and classical literature), the
unresolved weighted-character receiver, and general sparse characteristic-
zero relation specialization. The latter still lacks a polynomial NUMERICAL
degree good cyclotomic specialization for norm circuits. The actual bounded
CIT theorem tests a supplied order, not existence of a small good order.
Two distinct Claude calls exhausted 64000 output tokens without a report:
small-cyclotomic-fable USD3.30837 estimated; general-constant-map-opus
USD1.382444 estimated. No findings or retry. The local-image question won
admission because a concrete replacement for the rare-point source emerged.

Corpus been-tried and baselines were checked before source work (and the
precise candidate rechecked). The returned LLL baseline has no applicable
hypothesis here. The relevant classical comparator is Stoll's complete
extension/disc algorithm, whose generic step scans the residue field, and
his random polynomial-divisor variant, explicitly subject to tiny generator
regions. Our fixed-cubic note already replaces the field scan by bounded
character-pattern sampling. Growing d cannot enumerate all 2^d patterns;
the proposed change is to recover their SPAN using one functional at a time
in the proof, without ever enumerating functionals in the algorithm.

## 2. Primary-source scope

Snapshots and hashes: audits/sources/local_kummer_cluster/source.json.

- Stoll, Implementing 2-descent for Jacobians of hyperelliptic curves,
  https://www.impan.pl/shop/en/publication/transaction/download/product/83397 .
  Actual Lemma4.4 gives dim J(Q_p)/2J(Q_p)=r-1 at odd p, where r is the
  number of Q_p-irreducible factors of f. Lemma6.1, the trace/norm diagram
  and the paragraph preceding delta_rec require ALL extensions of degree
  <=g. Lemma6.3 gives local stability, rational-root tails and trivial
  nonintegral x for monic odd degree at odd p. The last paragraph of §6
  warns about tiny generator sets in unstratified random sampling.
- Poteaux--Vaccon--Weimann, On OM Algorithms and Cluster Pictures (2025),
  https://weimann.users.lmno.cnrs.fr/clusters.pdf . Actual Theorem1.1 and
  Remark1.3 give the tame cluster computation in polynomial residual-field
  operations and discriminant-bounded precision, plus residual factoring.
  This is an algebraic operation theorem; BIT, local-coordinate, norm and
  output precision costs must still be supplied. No whole-paper validation.
- The additional Dokchitser et al. local-arithmetic PDF is retained but
  is not needed to justify the operation below. A failed UCL download is
  recorded, with a successful primary arXiv fallback. No theorem is inferred
  from the failed download or an abstract.

## 3. Tame-extension coverage

For every ef<=g construct the unramified K_f/Q_p of degree f. For each
unit class u in k_f*/(k_f*)^e construct K=K_f[pi]/(pi^e-pu). There are
gcd(e,p^f-1)<=e classes. The number of fields is polynomial in g (O(g^2)
suffices); each has degree at most g. Duplicates are harmless.

Completeness: every extension of degree<=g is tame since p>g. It contains
its maximal unramified subfield. If pi_0 is a uniformizer of its totally
ramified degree-e part, pi_0^e/p is a unit. Choose its residue representative
u in the unramified field. The quotient differs from 1 by a principal unit;
the e-th power map on principal units is bijective since p does not divide e.
Adjusting pi_0 gives pi^e=pu. Changing u by an e-th power does not change
the field presentation. Thus the list covers all isomorphism classes.

Constructing a generator of the small quotient needs factoring only e<=g.
For every prime ell dividing gcd(e,q-1), test a random a by
a^((q-1)/ell)!=1. A successful a generates the quotient; its powers give
the at-most-e representatives. Do not factor q-1 or enumerate k_f.

Stoll's degree<=g prime-divisor generation and norm compatibility imply
that the images of C(K) over this list span the desired base-field image.
Using only Q_p-points or only odd-degree extensions would be incomplete.

## 4. Bounded disc traversal

Fix K, normalize v_K(pi)=1, put Delta=v_p(disc f) and D=e_K*Delta. Factor f over K into
fields E_i with distinguished alpha_i, without a full splitting field.
At D(xi,t)={x:v_K(x-xi)>=t}, compare v_K(alpha_i-xi) to t. When the
scaled beta_i=(alpha_i-xi)/pi^t is integral, compute its residue in k_i.
Exceptional z in k are precisely those residues beta_i that lie in k.
They are computable by residue-field membership; there are at most d.
Recurse into these children only. All other residues are generic.

Important fractional-distance guard: an exceptional child has an associated
root at distance >t, which need not be >=t+1. Such a child may contain NO
root in the closed disc. In that case every x-alpha_i squareclass is
constant on the child, and one local square test handles it. A literal
assertion that every generated closed child contains a root is false.

At a fixed positive depth, the associated strict root neighborhoods for
distinct centers are disjoint, so there are at most d generated nodes.
All roots are integral and every pairwise root distance has valuation<=D/2.
At depth D+1, an associated root is closer to the K-rational center than
to any other root. Krasner makes it K-rational; its distance is then an
integer and the whole disc lies in its Stoll6.3(2) tail. Its image was
already included as a Weierstrass-point image. Thus at most
1+d(D+1) nodes suffice. Nonintegral x gives the trivial class by6.3(3).

At a generic residue all valuations and squareclasses are constant on its
whole child. Compute the Gauss valuation c of f(xi+pi^t Z) and its nonzero
residual polynomial F. Its degree is <=d. Every k-root of F is exceptional.
Generic points exist precisely when c is even and chi(F(z))=1. If c is
odd there are no generic points, but exceptional children must still be
processed. Never divide away c parity.

## 5. Character-functional span lemma

Each E_i*/E_i*^2 has two coordinates at odd p: valuation parity and the
quadratic character of its normalized residue. In generic children the
former is constant. The latter is constant or a fixed sign times
chi_{k_i}(z-beta_i)=chi_k(N_{k_i/k}(z-beta_i)). The degree of this norm
polynomial is [k_i:k], with multiplicities retained. The sum over i is
<=sum_i[E_i:K]=d.

Norm to the base L induces a homomorphism of squareclass groups. Thus
EVERY base linear functional lambda has

    (-1)^lambda(v(z)) = epsilon chi_k(R(z)),  deg R<=d,       (1)

on generic residues, for an epsilon in {+1,-1}. Valuation bits and fixed
uniformizer factors are absorbed in epsilon. The exceptional set B has
size <=d and contains all k-roots of F and the relevant norm polynomials.

Lemma: if q>=256d^2 and lambda is nonzero on the span of the ACTUAL valid
generic vectors, then at least q/8 residues z in k are valid and have
lambda(v(z))=1. Invalid/exceptional residues count as failed samples.

Proof: work with polynomial square
classes modulo CONSTANTS as well as squares. If F is a constant times a
square, it has either no valid generic residues, or all of them are valid.
In the latter case (1) is either constant or has the ordinary one-character
Weil distribution. If F has nonconstant square class and R has either
constant class or the same class as F, the functional is constant on the
valid set. If it is nonzero there, all valid residues count, and the
one-character bound gives at least q/2-O(d sqrt(q))-d.

In the remaining case F,R,FR have nonconstant square classes. The indicator
is (1+chi(F))(1-epsilon chi(R))/4 off B. Their degree bounds d,d,2d and
Weil give at least q/4-d sqrt(q)-d >= q/8. Repeated factors and nonsquare
constant multiples are handled by the preceding cases, not incorrectly
fed into a nonsquare-over-the-algebraic-closure bound.

There are at most 2^(2r)<=2^(2d) base functionals, but NONE is enumerated.
After N>=8(2d log 2+log(2M/eta)) independent uniform residues at each of M
nodes, the union bound makes every node's valid sampled vectors span its
entire generic image with probability at least1-eta/2. Take the computable
bound M=(number of enumerated fields)*(1+d*(g*Delta+2)). This uses polynomial
sampling of a span; it does not realize every one of 2^d sign patterns.
When q<256d^2, exact residue enumeration is polynomial in d instead.

## 6. Actual vectors, certification and precision interface

For every valid generic representative x, norm x-theta to the base L.
Equivalently use (-1)^[K:Q_p] charpoly_x(theta). Existence of y follows
from the even valuation/square-unit test; explicitly constructing y is
unnecessary. For a rational root alpha of f over K, use the UNIT

    alpha-theta + (f/(X-alpha))(theta)

before the norm. Directly norming alpha-theta would contain a zero factor
and is wrong. These are actual point/divisor images, never arbitrary
norm-square vectors. Combine by F2 linear algebra. Actual Stoll4.4 supplies
the target rank r-1. Reaching it certifies completeness; a capped run that
does not reach it returns ABORT, not a purported complete subspace.

Section8 pays uniform local factorization, integral coordinates, norm maps
and precision at growing d. D=e_K*Delta is polynomial in input bits;
t<=D+1, monicity bounds the Gauss valuation by dt, and discriminants bound
root/derivative valuations. The explicit finite-ring procedure and P,S,W
budgets close the conversion; the OM operation count alone would not.

## 7. Independent reviews and verified API findings

Review ledger: audits/reviews/2026-11-06-local-kummer-image.md. Independent
Codex core, actual full-source/precision and final integrated reviews are
complete. The final review accepts the entire WRITTEN classical polynomial-
BIT composition, including logarithmic-error amplification and ABORT.

The narrow Opus coordinate audit completed: 10345 input/12621 output tokens,
estimated USD0.2938. Accepted repairs are explicit component bases, a
Frobenius-fixed-dimension decomposition stopping certificate, and a fixed
returned coordinate frame. Its d1,p2 counterexample is outside the native
d>=3,p>d contract; section8 now repeats this scope because its isolated
packet omitted it. Its source-proof packet omission was repaired by
reading and retaining the actual full section3/5 proof, independently.

Three other calls exhausted their output limits with NO reports:
small-cyclotomic-fable USD3.30837, general-constant-map-opus USD1.382444,
and local-kummer-fable USD1.78261, all estimates. No findings or retries.
Total four-call estimate USD6.767224, not an invoice or account balance.
The successful coordinate audit was a distinct narrow arithmetic question.

Cheapest falsifiers examined: omitted tame extensions, excessive character
degree after norms, square-degeneracy rare bits, fractional-root disc count,
uncharged p-adic precision, and incomplete Q_p-point-only generation. The
scope and precise resolutions are above and in the ledger.

## 8. Paid local arithmetic and polynomial BIT precision

Two additional actual primary sources were obtained and hashed in the same
source directory: Poteaux--Weimann, Fast Integral Bases Computation,
https://weimann.users.lmno.cnrs.fr/integral_bases.pdf ; and Local Polynomial
Factorisation, https://weimann.users.lmno.cnrs.fr/issac.pdf . The former's
model explicitly includes the Boolean RAM for A=Z. The paragraph on local
p-integral bases states the local version of Theorem1 with the local index
contribution, and explicitly says no discriminant factorization is needed.
This is the source route below; an alternative round-2 argument is not used.

### 8.1 Base maximal order and squareclass coordinates

Throughout this section retain the native d=2g+1>=3 and p>d; in
particular p is ODD. This is not a lemma for d=1,p=2.

Factor f over Q by the classical polynomial-bit integer-polynomial algorithm.
Its monic integral factors have polynomial coefficient height. On each
factor apply the source's p-INTEGRAL basis algorithm at the GIVEN p. The
product gives an explicit order O whose p-adic completion is the maximal
order of L. If Delta=v_p(disc f), each basis denominator is a power of p
of exponent<=Delta/2; the total index exponent is also<=Delta/2. Reduced
triangular numerators have polynomial bits. Exact rational arithmetic in
these bases computes the p-integral multiplication table with polynomial
bits; reducing it mod p^P loses no precision. Global maximal orders and
factoring the integer discriminant are unnecessary. Use sigma=Delta+2
for the integral-basis source's Theorem3, whose stated inequality is
STRICTLY sigma>2 ind_p(f)+1.
The actual local construction is supported beyond the introductory
paragraph: section3 Proposition4, Theorems4--5 and Corollary3 supply the
triangular-basis/MaxMin construction with its OM-tree-induced well-order.
Section5 Propositions8--10 (original text lines779--834), with I=B, give
the precision, comparisons, finite numerator expansion and local p-basis
cost. Theorem7's proof (lines847--854) composes these steps; its subsequent
global CRT step is unnecessary at a single given p. No claim rests on the
intro alone. Factor accuracy exceeds alpha_max since floor(alpha_max)<=
index<=Delta/2 and sigma-index>alpha_max.

Let R=O/pO, a d-dimensional F_p algebra. Its nilradical N is the kernel of
the F_p-linear Frobenius power a->a^(p^s), p^s>=d. Linear algebra and modular
powering compute it. Decompose the reduced algebra R/N into finite fields
by polynomial factoring and linear algebra. One need not find a primitive
element for the entire product in one random trial: successive random
elements and their minimal-polynomial factors refine components. Conditional
on a value in one field component, matching its minimal polynomial in
another F_{p^f} component allows at most f values, with probability
<=f/p^f<=1/p. A logarithmic number of independent trials and a union bound
over at most d^2 component pairs therefore separate all field components.
For a verifiable stopping test, compute
r=dim_Fp ker(Frobenius-identity) on the reduced algebra. Each finite field
factor contributes exactly one fixed dimension, so r is the true number
of components. Refine by the irreducible factors of the minimal polynomial
of a random algebra element, using CRT idempotents, until r components are
present. A capped failure returns ABORT. All residual degrees are <=d;
capped randomized finite-field routines are charged.

Lift the resulting orthogonal idempotents from R/N to R and then O/p^P O
by idempotent Newton lifting. Over the nilpotent ideal, the polynomial
3u^2-2u^3 squares the idempotence error; O(log(dP)) iterations suffice.
For each idempotent multiplication matrix over Z/p^P, choose n_i columns
independent mod p and n_i pivot rows with a unit minor. The columns form a
free basis of its component by Nakayama; the unit minor gives coordinate
extraction with NO precision loss. Each component O_i is a DVR integer
ring. Its residue map rho_i and residue
degree f_i are now explicit. Its rank is n_i and ramification e_i=n_i/f_i.
For e_i=1 take uniformizer p. Otherwise choose by linear algebra a class
in the component nilradical N_i outside N_i^2; any lift has valuation1.
This is possible because N_i/N_i^2 is one-dimensional over its residue
field. Thus no search over p elements or supplied uniformizer is needed.
Fix this decomposition, component ordering and the chosen uniformizers
ONCE per run and use them for every vector. Return the frame (idempotents,
uniformizers and residue maps) with the basis. The coordinates depend on
that frame; no canonical or cross-run identical coordinate claim is made.

For an integral nonzero a in a component, compute its multiplication
determinant in an integral basis, giving

    m_i = v_p(N_{L_i/Q_p}(a))/f_i = v_i(a).

Normalize by the chosen uniformizer pi_i^m_i and reduce via rho_i; its
quadratic character is a power with O(f_i log p) exponent bits. Together
with m_i mod2 this gives the desired two squareclass bits. Matrix inversion
by adjugate/Cramer to divide by pi_i^m_i loses at most f_i*m_i p-digits.
The determinant and finite-ring calculations are polynomial matrix work.

### 8.2 Avoid unnecessary composita in the actual algorithm

The fields E_i/K in §§4--5 are needed for the PROOF of the character bound,
not for runtime coordinate calculations. At a node compute the content and
primitive reduction F of f(xi+pi^t Z); factor F over k to find its k-roots.
These are exactly the exceptional residues. This performs the entire tree
without constructing E_i or their integral bases. Find the K-rational
roots of f once by the degree-d local factorization over the explicit K;
the linear factors provide the Weierstrass representatives to finite
precision. No full splitting field is built.

For a sampled x or a modified Weierstrass unit, compute the norm to L as
the determinant of multiplication over the known integral tower basis of
K/Q_p. Unramified K_f and Eisenstein K_f[pi], pi^e=pu, have such a basis
explicitly. The matrix dimension is<=g and entries lie in O_L. Polynomial
operations, including synthetic division by a known root for f/(X-alpha),
are integral and do not lose p-adic precision. The result is fed into the
BASE order-coordinate algorithm above. Keep the local factorization of f
relative to K at degree d: p>d does not imply p>dg.

### 8.3 A conservative working precision

Put Delta=v_p(disc f), T=g*Delta+2 and

    V=d*g*(T+Delta+2),   P=16*d^2*g^2*(Delta+2)+16.

At every generic node t<=g*Delta+1, v_K(x-alpha)<=t for every geometric
root. This remains true under every embedding of K since the root set is
base-field invariant. Consequently every component of the transferred
norm has normalized valuation<=d*g*T<V. At a Weierstrass root, components
are root differences or f'(alpha); normalized p-valuations are bounded
by the discriminant, so their transferred valuations are also<V.

Thus all determinant valuations used for coordinate extraction are <=dV.
The choice P>dV+2 leaves at least two p-digits after the worst Cramer loss.
The earlier order construction is exact rational arithmetic, so its basis
denominators do not consume this finite-ring precision; input polynomial
evaluation in its integral table preserves precision. Idempotents and
component bases are computed in the finite ring itself. Generic inputs and
point-square tests need precision at most dT+1 in the K normalization,
which is also covered.

Compute K-rational roots and all local factor approximations to absolute
K-precision S=e_K*(P+Delta+2), using the conservative working precision
W=2S+2e_K Delta+2. This is polynomial, exceeds the source OM threshold,
and absorbs its possible index loss between working precision and factor
accuracy (index<=e_K Delta/2). A linear factor approximation
gives a root approximation to S digits directly. Evaluation of the modified
Weierstrass polynomial and its norm is stable modulo p^P because they are
integral polynomial operations. The norm determinant does not introduce
a hidden division. Root labels and output squareclasses are therefore
unchanged by the finite approximations.

Represent O_K/(pi^W) in the explicit unramified/Eisenstein tower with at
most ef*ceil(W/e) base-p digits. Its modular arithmetic and unit inversion
are polynomial in ef,W,log p. The local-factorization source operates at
finite working precision W with polynomially many residue/tower operations;
residual extension degrees are <=d. Simulating these operations in the
explicit finite tower supplies the BIT conversion, rather than assuming
an algebraic-RAM operation has unit bit cost.

All values Delta,d,g,P,S,W are polynomial in native input bits; residue-field
elements have O(g log p) bits and every field degree is charged. Assign
eta/2 to field construction/factoring and eta/2 to the span samples. For
an expected-polynomial Las Vegas subroutine with proved bound B, cap each
attempt at 2B, verify its output, and independently restart
O(log(number_of_calls/eta)) times before ABORT. Markov gives success>=1/2
per attempt. Do NOT use a single B/eta clock, which would lose the claimed
poly(log(1/eta)) dependence. Explicit random irreducibles and small unit-
quotient generators similarly use their known polynomial success bounds
and logarithmic amplification. Every returned full-rank basis
then remains exact, rather than a potentially wrong approximate image.

The independent source/precision and final integrated actual-text reviews
accepted this completion after the stated repairs. Source results, new
deductions and finite controls remain distinguished in the review ledger.

## 9. Exact control and next decision

One Sage control is retained in audits/controls/local_kummer_span/.
At d5,p10007, the generic valid image has rank4, with5001 valid residues
and minimum detectable-functional count2475. It explicitly rejects the
stronger every-pattern density claim. A native d5,p7 fractional-root child
has odd Gauss valuation and no points; exact Q_7(sqrt7) Cramer normalization
retains the determinant's valuation9. These are falsifier checks, not
proof of the theorem or execution of its complete algorithm.

The construction removes the large-prime local source/scan blocker. It
leaves small/wild/dyadic places and growing-degree global arithmetic open
for a full quantum Selmer algorithm. It does not compute Mordell-Weil rank,
rational points or covering curves, and does not establish novelty or a
quantum speedup. No larger local implementation or neighboring extension
is queued. The next pass must independently compare native high-upside
mechanisms and existing literature before selecting a theorem or test.
Next command: read STATE/TRAPS, then corpus been-tried/baselines for that
explicit mechanism. Acceptance requires a paid operation with an end-to-end
role, rather than another conditional local analysis by inertia.
