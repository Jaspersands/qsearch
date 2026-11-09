# Classical sparse-bit relations in monomial Kummer fields

2026-11-06. Written constructive classical algorithm; independent core and
combined actual-text/resource reviews complete. One exact control passed.
No novelty, general-function-field counterpart, speedup or full execution claim.

## Native question and selection

Compute the FULL integer multiplicative relation lattice of nonzero supplied
elements in

    F = Q(T_1,...,T_s)[Y]/(Y^delta - a*T^v),

where a is a nonzero binary rational, v in N^s is binary, delta is a charged
NUMERICAL positive degree, and the binomial is promised irreducible. Each
u_i is supplied as sum_(0<=h<delta) r_ih(T)Y^h, with r_ih explicit quotients
of sparse rational-coefficient polynomials with binary nonnegative exponents.
s,delta,k all grow. Nonzero inputs and denominator polynomials are promises;
combine repeated sparse monomials and skip zero coefficient functions first.
No inverse, factorization, constants, valuation, point or relation advice.

Take k>=1 and rational 0<eta<1/2. The charged input size is the encoded
bit length PLUS delta: a binary abbreviation for the field degree does not
turn this into a polynomial-in-log(delta) claim. The output is a Z-basis
of Rel={e in Z^k:prod_i u_i^e_i=1}. The algorithm
below is classical bounded-error polynomial in this sparse input BIT length
and log(1/eta). It computes all constant and torsion relations exactly on
its good event; it does not saturate the final lattice. s=0 is included.

This family is a strong classical attack on the recent sparse arithmetic
quantum composition, not a proposed new quantum primitive. The broader
question is whether large sparse exponents and growing algebraic degree
actually require its quantum finite-group relation step. Its strongest
existing classical counterparts were all degree1/2 inputs and explicit
finite Q-algebras. Here an explicit monomial coordinate operation removes
the constant-field/leading-place blocker for ALL degrees in this family.

Selection began with STATE/TRAPS and corpus been-tried/baselines, then the
actual Laurent-binomial and finite-Q-algebra sources. Independent alternatives
were reconsidered: the original-character learner still has no paid nonsplit
source, and the actual superlattice source still has exponential conditional
records rather than a clean polynomial inverse. Neither new operation was
identified. The monomial operation below provides a complete classical
algorithm and directly tests the quantum candidate's claimed domain; it is
not selected merely because general growing-degree arithmetic remained open.

Standard attacks are integer unimodular reduction, rational logarithmic
derivatives, modular evaluation, exact LLL and number-field relations.
Dense expansion/factorization is not a sparse-bit comparator. All these
classical operations are paid below before any quantum construction.
Falsifiers are cancellation of tied leading terms, huge coefficients from
reducing alpha^c, a missing denominator/content bound, a finite-index LLL
answer, or loss of torsion in the final intersection.

## 1. Pay the constant field by exponent coordinates

Put q=(-v,delta), g=gcd(q_1,...,q_(s+1)), w=q/g. Since w is primitive,
extended-gcd unimodular operations produce C in GL_(s+1)(Z) with Cw=e_0.
Both C and its inverse have polynomial bit length and computation cost;
one-vector reduction suffices. View a monomial exponent e as new coordinates

    Ce=(c,n_1,...,n_s).

Let alpha=(T,Y)^w and let Z_j=(T,Y)^(C^-1 e_j). The actual Laurent-ring
isomorphism sends the single relation to alpha^g=a. Irreducibility of the
original field presentation implies X^g-a irreducible over Q. Therefore

    F = K(Z_1,...,Z_s),       K=Q[alpha]/(alpha^g-a),           (1)

and K is the entire algebraic constant field. Its degree g<=delta and
power-basis multiplication table have polynomial bit size. This is an
explicit computation, not a supplied constant-field oracle. Localization
at T_j and Y is legal since these are nonzero in F.

This normal-form mechanism is established Laurent-binomial theory: actual
Eisenbud--Sturmfels, Theorem2.1(b) and its diagonalization proof. No new
classification theorem is claimed. We use the one-relation construction
directly, retaining Q rather than silently imposing algebraic closure.

## 2. Leading coefficients stay compact, even after huge exponent changes

Use lexicographic order on the FREE exponent vectors n in Z^s. This is a
translation-invariant total order; finite Laurent supports have maxima and
leading coefficients multiply. Leading coefficient extends to K(Z)^* by
ratios and is the identity on K^*.

For each nonzero r_h=P_h/Q_h in one u, scan the sparse supports of P_h and
Q_h and maximize their transformed free exponents. These maxima are unique:
two T-only monomial exponents with the same free image differ by an integer
multiple of w, whose Y-coordinate is delta/g>0. Their difference has
Y-coordinate0, so that multiple is0.

The leading term of r_h Y^h consequently has free exponent n_h, a rational
coefficient b_h (the ratio of two ORIGINAL small coefficients), and alpha
exponent c_h, all computed with polynomial-bit integer operations. Retain
the h attaining the largest n_h. If h,h' tie then their ORIGINAL net
exponent difference satisfies

    E_h-E_h'=(c_h-c_h')w,
    c_h-c_h'=(h-h')/(delta/g).                               (2)

Thus distinct tied h have distinct alpha exponents in an interval of length
at most g-1. With c=min_tied c_h, define

    beta=sum_tied b_h alpha^(c_h-c),
    LC(u)=alpha^c beta.                                     (3)

The polynomial defining beta has degree<g and is nonzero. Irreducibility
of X^g-a rules out cancellation. No later Puiseux term or hidden place
calculation is required. This is where the monomial presentation matters.

Each beta has at most delta terms with polynomial-size rational coefficients.
c can have a huge numerical value but has polynomial binary length. NEVER
first reduce alpha^c using alpha^g=a: doing so could write a rational number
with exponentially many bits. Retain (beta,c), and use the small original
tuple in Section5. This is the necessary compactness repair to a naive
toric reparameterization argument.

## 3. Recover Alg from the original representation

Let D_j=T_j partial/partial T_j, extended to F. The binomial identity gives
delta D_jY=v_jY. Hence

    delta D_ju_i=sum_h(delta T_j partial_j r_ih+h v_j r_ih)Y^h.

The common kernel of these derivations in characteristic zero is K. Thus

    Alg={e:prod u_i^e_i in K^*}
       ={e:sum_i e_i delta D_ju_i/u_i=0 for every j}.          (4)

Here is an explicit polynomial BIT bound for the implicit coefficient
matrix, without expanding polynomials or constructing basis powers.
Normalize each coefficient numerator/denominator with a COMMON scalar so
both are integral and their ratio is unchanged. Write a=a_num/a_den with
nonzero integers and a_den>0. Let G be the product of all r_ih denominator
polynomials and L their count. Let beta_degree>=1 bound their and all
numerator numerical total degrees, V=sum v_j, and choose integer b>=1
with the product of max(2,l1norm(P)) over all numerator/denominator
occurrences, and max(2,|a_num|), max(2,a_den), at most2^b. Set

    mu=(L+1)*beta_degree+V+1, U=2^(2b), J=delta!*U^delta,
    A=3*delta*mu*2^b*J^k, D=(k*delta+2)*mu.                  (5)

These integers have polynomial bit length, even when degrees are enormous.
Let A_ih=P_ih*(G/Q_ih), so u_i=sum A_ihY^h/G. Its multiplication matrix
has the form N_i/(a_den*G). Each entry of N_i is either a_den*A_ih or
a_num*A_ih*T^v: at most one wrap of Y^delta is needed. Each has l1norm<=U
and degree<=mu. det N_i is nonzero because u_i is a nonzero field element.

The numerator vector V_ij of delta D_ju_i over denominator G^2 has entries

    delta*(T_j partial_j A_ih*G-A_ih*T_j partial_jG)
       +h*v_j*A_ih*G.

Their l1norms are <=3*delta*mu*U and degrees<=2mu. Consequently

    delta D_ju_i/u_i
       =a_den*adj(N_i)*V_ij/(G*det N_i).

Clear the COMMON nonzero denominator H=G*prod_i det N_i. Every resulting
coordinate R_ij is an integer polynomial. The determinant/adjugate bounds
give ||R_ij||_1<=A and ||H||_1<=A, with degrees<=D. The factor delta in
matrix-vector multiplication is included in the delta! bound.

All evaluations use the original sparse polynomials, binary powering,
field matrices and determinant/adjugate computations. Formula(5) bounds
these FIXED determinant/product expressions; it is not a claim that
arbitrary arithmetic circuits have polynomial log-coefficient bounds.

The implicit integer matrix of all coefficients of every R_ij has k
columns, entries bounded by A, and integer kernel exactly Alg. It is never
constructed. Its kernel has a full basis with infinity norm at most

    B=k!*A^k.                                                (6)

For rank q in(0,k), pick q independent rows and a nonsingular q-by-q minor
C_0, with d_0=|det C_0|<=q!A^q. The projected integer kernel in the other
k-q coordinates contains d_0 Z^(k-q); an HNF basis there has entries<=d_0.
Cramer's rule lifts pivot coordinates with absolute value at most
(k-q)q!A^q<=B. Rank0 gives Z^k, and rank k gives the zero lattice.

## 4. One modular evaluation and exact LLL

Set R=2^k*k*B, F_box=(2R+1)^k and C_cut=2^(k-1)*k*B. Choose a prime p with

    p>max(delta, a_den, k*R*A, 4*(F_box+1)*D/eta).             (7)

For each false integer e in the infinity-norm R box, some nonzero
coordinate polynomial sum e_i R_ij has coefficient magnitude<=kRA;
at least one coefficient therefore survives modulo p. H also survives.
A uniform t in F_p^s simultaneously avoids H=0 and every selected false
witness with probability >=1-eta/4, by Schwartz--Zippel and the union
bound. The proof enumerates witnesses conceptually; the algorithm never does.

If H(t)=0 abort. Otherwise evaluate the delta*s-by-k derivative matrix E,
and form the FULL congruence lattice L={e in Z^k:Ee=0 mod p}, including
p Z^k. Finite-field Gaussian elimination and integer HNF compute a basis.
On the good event it contains Alg and no false vector of Euclidean norm<=R.

If r=rank Alg, the first r vectors of a 3/4-LLL basis of L have lengths
<=2^((k-1)/2)*sqrt(k)*B<=C_cut<R, by the successive-minimum bound. They
therefore belong to Alg and span its rational span. Being a prefix of a
full L-basis, they generate L intersect that span. Since this intersection
contains Alg, equality follows. Every later vector has length>R. Keep the
prefix of lengths<=C_cut. This recovers ALL of Alg, not a finite-index
subgroup. Rank0 and rank k work with the same rule.

log p and the lattice input/output bit sizes are polynomial. Choose p in
[X,2X] above the bound using capped uniform candidates and primality tests;
the already checked prime-density estimate pays polynomially many trials.
Capped exact sampling of t and prime-search failure use at most eta/2
additional budget. All clocks are polynomial in input bits and log1/eta.
When s=0 no random point is necessary and Alg=Z^k. Large characteristic,
not only a large extension of a small characteristic, protects contents.

## 5. Full constants, torsion and nonsaturation

Compute (beta_i,c_i) from(3), and apply actual Lenstra--Silverberg1509.08843
Theorem1.11(i) to the ORIGINAL small tuple

    (beta_1,...,beta_k,alpha) in the explicit degree-g field K.

It returns generators for its full integer relation lattice L_K in
deterministic polynomial time; convert to a basis by integer normal forms.
No factorization advice, compact-power evaluation or constant-height
oracle is added. The field and every supplied algebraic number have
polynomial bit size. Define the integer map

    J_c(e)=(e_1,...,e_k,sum_i c_i e_i).

Then the complete answer is

    Rel=Alg intersect J_c^(-1)(L_K).                         (8)

Indeed on Alg, the product is in K and equals its leading coefficient.
Integer kernels/intersections compute(8) in polynomial time. Do not
saturate: roots of unity impose genuine finite-index conditions. This is
an end-to-end classical polynomial sparse-bit algorithm for the stated
family, subject only to the input promises and bounded randomized error.

## Sources, review and exact experiment

The source snapshots/hash ledger are in
audits/sources/monomial_kummer_relations/. Actual ES Theorem2.1(b) and its
proof supply the known Laurent normal form; actual LS Theorem1.11(i) is
the final number-field algorithm. The earlier rational/quadratic note and
finite-specialization LLL proof are reused, not rerun. No general sparse
factorization theorem is imported; the recently retrieved sparse-GCD paper
does not establish hardness for this relation problem.

Independent core reviewers accepted the leading/cancellation/compactness
argument and the derivative/full-lattice stage separately. Parent combined
them and made coefficient/denominator bound(5) explicit. Independent
combined actual-text/source/resource review accepted that bound, the integer
cutoff, confidence budget and full constants/torsion stage. Review record:
audits/reviews/2026-11-06-monomial-kummer-relations.md.

The single exact control used delta6, a2, v=6M+2, M=2^40+172, units
(Y,T,2,1+Y^3/T^(3M+1),Y^3/T^(3M+1)-1,-1). The expected full lattice is
generated by (6,-6M-2,-1,0,0,0), (0,0,0,1,1,0), (0,0,0,0,0,2).
All those generators were recovered exactly, with every huge exponent kept
binary. C=[[-1,-M],[3,3M+1]] gave K=Q(sqrt2), T=alpha^-1*Z^3 and
Y=alpha^-M*Z^(3M+1). The two tied coefficients 1+alpha and alpha-1 were
nonzero. One original-degree6 finite-ring evaluation at t7 and a161-bit
prime gave derivative rank1; LLL recovered full Alg rank5 using the
independently known CONTROL-ONLY basis bound3M+1. An exact small-field
valuation/unit/sign calculation, not general LS, gave full Rel rank3.

The derivative-only filter accepted constant2; the LC-only filter accepted
Y/T^M=Z, which is nonconstant. Saturating the sign relation would falsely
accept -1. The small prime257 divides6M+2 and erases the Y derivative
constraint. Artifacts: audits/controls/monomial_kummer_relations/
native_control.{py,json}. This tests identities; it is not a general LS
implementation, theorem-sized run, quantum execution, or evidence for
asymptotics beyond the proof.

No implementation, larger sweep or general-growing-degree extension is
queued. A new pass must compare externally valuable mechanisms again.
The remaining general-f constant/leading-place issue is not promoted by
continuity. Reentry needs a distinct paid operation or a decisive classical
attack on an actual quantum candidate. No Claude API call was made this pass.
