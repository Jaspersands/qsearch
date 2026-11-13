# Small-height leading atoms for sparse constant relations

2026-11-13. Parent derivation and independent review checked. This is a
PROOF-ONLY representation lemma for the full native sparse characteristic-zero
relation problem. It constructs no leading-coefficient algorithm and closes
neither the growing-degree classical fullRel problem nor a p-adic precision
bound. No hidden leading atoms, residue field, embedding or valuation may be
supplied to an algorithm as advice.

## Question, prior work and proposed use

The native input is the one in SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md:
F=Q(T_1,...,T_s)[Y]/f, monic irreducible f of charged degree delta, and k
nonzero atoms u_i in the Y basis, with sparse rational-function coefficients
and binary T exponents. All parameters grow. Return the full integer lattice
Rel={e:product u_i^e=1}, including torsion. General Alg={e:product u_i^e is
algebraic over Q} is already computable classically in polynomial sparse BIT
time. The reviewed quantum algorithm supplies fullRel. The actual
Lenstra-Silverberg finite-Q-algebra theorem gives a classical full solver
ONLY after its explicit algebra and atoms have been constructed; the existing
cyclotomic specialization pays that operation for each fixed delta.

Corpus been-tried and baselines were checked before this pass. They return
the general constants and fixed-degree cyclotomic notes; the ordinary LLL
baseline does not supply a finite-place separation bound. The earlier
constant-map paid call was EMPTY; it is not repeated. The newer one-place
p-adic proposal would evaluate constants through original atoms at a modular
specialization, retaining Alg exponents. Its missing obligation is a uniform
polynomial precision/complete-lattice theorem, not just injectivity of a
local embedding. Ordinary growing-generator p-adic Baker estimates have not
been shown to meet that bound. Ge's theorem for explicitly supplied number
fields cannot be imported as an oracle for this compact input.

This lemma removes a different, specific uncertainty: the ORIGINAL atoms
admit simultaneous leading coefficients of small height and small common
field degree, even when the valuation orders are exponentially large. A new
classical operation extracting or using them could directly complete the
known end-to-end relation algorithm. No such operation is claimed here.

## 1. Uniform norm-polynomial bounds without expansion

Use the common-denominator construction already paid in
GENERAL_SPARSE_CONSTANTS_ATTACK.md. Write every coefficient of f and every
Y-basis coefficient of u_i as an integer polynomial divided by the SAME
nonzero integer polynomial D. Their l1 norms and that of D are at most
H=2^b, and their total T degrees are at most d0. Both b and log(d0+1) have
polynomial native bitlength; forming all expanded products is unnecessary.

The companion matrix for Y is C=A/D, where entries of A have l1 norm<=H
and degree<=d0. Put

    u_i(C)=B_i / D^delta,
    B_i=sum_(j=0)^(delta-1) b_ij A^j D^(delta-1-j),
    W=delta^delta H^delta,
    P_i(T,Z)=det(D^delta Z I-B_i),
    C0=delta! (2W)^delta.

Every entry of B_i has l1 norm<=W and degree<=delta*d0: matrix products
contribute at most delta^(j-1) terms per entry, and the displayed sum has
at most delta terms. Thus P_i has Z degree delta, total T degree at most
delta^2*d0, and total coefficient l1 norm at most C0. Its leading Z
coefficient is D^(delta^2), and P_i(T,0) is nonzero because u_i is nonzero
in the field F. In particular

    log2 C0 <= 2 delta^2 (b+log2(delta+1)+1).

These are bounds on an implicit determinant, not an algorithm enumerating
its potentially exponential support. In particular they do not give a
polynomial-order cyclotomic hitting set.

## 2. A proof-only common one-variable place

Protect D, each P_i(T,0), and a nonzero cleared discriminant numerator of
f. Their degrees are bounded by

    Dstar=10 delta^3 (d0+1).

The standard Sylvester discriminant formula has O(delta) factors, each of
degree O(delta*d0), so this deliberately loose bound suffices. Substitute
T_j=t^((Dstar+1)^(j-1)). The exponent encoding has polynomial bitlength.
On polynomials whose separate coordinate degrees are <=Dstar this map is
injective on monomials. Therefore all protected polynomials remain nonzero,
and coefficient l1 bounds are preserved. No determinant is expanded to
perform this proof step.

The specialized finite Q(t)-algebra is separable and nonzero. Every u_i is
a unit in it. Choose ANY field component E of degree m<=delta, and a place
of E above t=0. The localized original algebra

    A0=Q[T,D^-1,Y]/(f)[u_1^-1,...,u_k^-1]

maps unitally into E. Its algebraic-over-Q subring C_A is a field: the inverse
of a nonzero algebraic element is a rational polynomial in that element.
Consequently the specialization is INJECTIVE on C_A. It need not be
injective on the entire function field; no such assertion is used.

Let the place have ramification e and residue degree f0, with e*f0<=m.
In equal characteristic zero its completion is kappa((pi)), where
[kappa:Q]=f0, and

    t=c*pi^e*(1+O(pi)), c in kappa^*.

Choose a with a^e=c. The compatible Puiseux parameter s=t^(1/e) is
pi*a*(1+O(pi))^(1/e). Formal inversion has coefficients in
K0=kappa(a), whose degree is at most e*f0<=delta. Hence ALL the original
atoms have expansions

    u_i=alpha_i t^(r_i/e)+higher terms,
    alpha_i in K0^*, r_i in Z.

This is the fixed compatible parameter t^(1/e). Arbitrary rescaling of a
uniformizer could introduce arbitrary heights and is NOT permitted.
Neither the place nor K0, r_i or alpha_i has been computed or supplied.

## 3. Height of every original leading atom

Write the specialized P_i as sum c_ab t^a Z^b. Substituting the expansion
of u_i, the terms of minimal weight a+b*r_i/e must cancel. Thus alpha_i
is a nonzero root of the edge polynomial

    Q_i(Z)=sum_(a+b*r_i/e minimal) c_ab Z^b.

For each b at most one a occurs at the minimal weight. This is a nonzero
integer polynomial of degree<=delta and l1 norm<=C0; remove a power of Z
if necessary. Its primitive minimal-polynomial factor has Mahler measure
at most that of Q_i, which is at most C0. Therefore the absolute logarithmic
Weil height obeys

    h(alpha_i)<=log C0.

The bound is polynomial in the native sparse input parameters and contains
no numerical T-degree factor. It is simultaneous: all alpha_i lie in the
SAME degree<=delta field K0, so their embedding alignment is retained.
Individual characteristic polynomials alone would not supply that alignment.

For any evec in Alg, gamma=product u_i^evec_i is an original algebraic
constant. At the chosen place it has valuation zero, and its leading
coefficient is its faithful embedded value. Multiplicativity of leading
coefficients therefore proves the exact identity of lattices

    Rel_F = Alg intersect {evec: product alpha_i^evec_i=1}.

This is an existential reduction. Applying Lenstra-Silverberg to unspecified
alpha_i would be hidden advice. Raising atoms to an Alg basis may create
exponentially large expanded heights; the bound is for ORIGINAL alpha_i,
not for those basis power products.

## 4. What remains unproved and the next decisive gate

A classical replacement must COMPUTE one consistent leading tuple and its
field in polynomial sparse BIT time, or give a complete relation-extraction
algorithm using only native evaluations and a proved polynomial precision.
Naive Puiseux truncation is still falsified by the existing order-M family
with binary M. A small height bound is not a fast leading-coefficient oracle.
One-place logarithms have a torsion kernel only after retaining valuation;
that qualitative fact does not bound short approximate integer relations.
The all-bounded-exponent large-prime union bound is already the QUANTUM
algorithm and does not replace finite-field discrete logarithms classically.

Cheapest next test of a proposed extraction method: apply its ACTUAL native
operations and clock to the prior f=product_j(Y-j(2+T^M))-
T^M(T^M-1)(2+T^M), u_j=Y-j(2+T^M), with growing delta and binary M.
It must skip the order-M cancellation and retain one common embedding,
without expanding a degree-M series or an exponential determinant support.
This is a falsifier for the operation; the displayed tuple itself has Alg=0
and is not a hard fullRel instance. No parameter sweep or quantum code is
queued merely to reconfirm that fact.


## 5. Independent review and exact controls

The complete 192-line review
`audits/reviews/2026-11-13-fresh-native-operation-selection.md` was read and
its simultaneous-place argument checked. It uses a looser determinant norm
bound with the same polynomial logarithmic height. Its original LC-field
claim is accepted in the proof-only sense above. Its one-place fullRel
proposal remains OPEN: an injective embedding and torsion characterization
do not supply a uniform finite-precision relation algorithm. The elementary
principal-log calculation is restricted to odd primes p and p-adic units.
For good primes p>2*delta^2, torsion in a degree-delta number field has order
at most 2*delta^2 and reduces injectively; once the relation lattice modulo
torsion is actually supplied, its finite image can be enumerated in polynomial
time. This does not supply that lattice.

Exact Sage control (one run, not an asymptotic experiment):
`audits/controls/sparse_constant_local_logs/control.py`, with saved
`result.json`, uses E=Q(t)[z]/(z^2-2*t^(2M+1)), M=3, and original atoms
(z,t,2,z/t^M). The compatible leading tuple is (sqrt(2),1,2,sqrt(2));
its common field has degree 2 while the residue field has degree 1.
Alg has rank 3; fullRel has rank 2 with basis
(1,0,3,-7), (0,1,1,-2). Both products were checked exactly in the original
function field and in Q(sqrt(2)). The original constant 2 is in Alg and
is not a full relation. This illustrates the distinction; the proof does
not rely on this finite example.

The same control computes 2^(p-1) modulo p^2 and p^3 exactly. For p=1093
and 3511 it is 1 modulo p^2 but not modulo p^3 (residues 581794064 and
628683172 respectively). Thus the p-adic principal logarithm of 2 has
valuation exactly 2. A test using only vanishing modulo p^2 can falsely
classify this non-torsion constant as torsion. This REFUTES only the
unqualified two-digit test, not polynomial precision, all single-place
algorithms, or classical tractability. No quantum speedup follows.

No paid call or implementation expansion was made in this pass. The second
candidate in the independent review, Davenport-Hasse lifting for phase
powers, fails its stated register-cost target: a degree-2^j extension
requires Omega(2^j log q) bits merely to represent a general field element.
This refutes the direct extension-register operation, not every method of
Gauss phase powering. No source theorem is inferred from an abstract.


## 6. Actual primary-source precision check and pass disposition

Kunrui Yu, *Linear forms in p-adic logarithms III*, Compositio Mathematica
91 (1994), 241-276, was downloaded from
https://www.numdam.org/article/CM_1994__91_3_241_0.pdf and retained with
SHA256/URL metadata in `audits/sources/sparse_constant_local_logs/`.
Displayed mathematics was visually inspected on journal pages 241, 242 and
246 because text extraction omits formulas. Section 0.1 bounds the valuation
of a nonzero product-minus-one by Phi*log(d*B). Phi includes a factor
proportional to ((n+1)*d/sqrt(log(p)))^(2*(n+1)), the product of the n
height parameters, and p^f-1. Theorem 1' on page 246 likewise retains
(n+1)^(2*n+4), a product V_1*...*V_n, and an exponential-in-n constant.
Consequently substituting polynomial height and degree bounds into THIS
published estimate does not yield polynomial digit precision in growing n.
This is a scope audit of that bound, not a claim that no stronger bound or
algorithm exists. It supplies no lower bound on required precision.

The pass therefore closes the proof-only simultaneous leading-height lemma
and the specific two-digit counterexample. General growing-degree classical
fullRel remains OPEN. No full solver, novelty, speedup or hardness is inferred.
The previously checked Lenstra-Silverberg Theorem 1.11 still requires an
EXPLICIT finite Q-algebra and its elements; a proof-only leading tuple does
not meet that interface. No general constant-map prompt, paid retry, series
expansion or determinant enumeration is queued. Compare independent native
operations before deciding whether this residual deserves another pass.


## 7. Bounded determinant-degree baseline screen

A separate corpus been-tried/baselines query for sparse polynomial matrix
determinant degree and combinatorial relaxation found no exact catalogued
transfer. That is not an absence-of-baselines result. The actual primary
Hirai-Ikeda arXiv:2008.11388v2 Theorem 1.2 and its defining equation (1.2)
were then read; the PDF/text/hash metadata are retained beside Yu1994.
Their log-cost algorithm concerns a symbolic matrix sum A_k*x_k*t^c_k
with noncommuting independent x_k. The rational-field implementation is
also discussed immediately after Theorem 1.2. Our native determinant has
fixed numerical coefficient matrices and no such independent symbols.
This input distinction prevents importing that theorem directly.

A direct algebraic falsifier for adding independent symbols and later
specializing them away is, for every integer M>=1,

    A(t)=[[1,t^M],[t^M,1+t^(2M)]], det A(t)=1.

Giving its three coefficient matrices independent COMMUTING labels yields

    det(x0*I+x1*t^M*[[0,1],[1,0]]+x2*t^(2M)*[[0,0],[0,1]])
       =x0^2+(x0*x2-x1^2)*t^(2M).

Generic degree is 2M, while the native specialization x0=x1=x2=1 has
degree zero. Thus even the commutative generic determinant is the wrong
invariant; no noncommutative theorem repairs this transfer automatically.
This does not refute every sparse determinant-degree algorithm, nor give a
reduction from the native norm matrices to a hard general determinant task.
The Murota1995 abstract was located but its full complexity theorem was not
inspected; applicability in sparse binary degree remains UNKNOWN here.
No implementation or paid request is justified by this source screen.
