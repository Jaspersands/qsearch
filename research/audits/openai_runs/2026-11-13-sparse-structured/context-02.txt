# General sparse function-field constants: classical attack

7 November2026. Reviewed pass complete. General Alg recovery is established;
the FULL classical Rel counterpart remains open. No new constant-map
subsystem or nearby refinement is queued. Full native question: can a classical
polynomial sparse-BIT algorithm replace the quantum relation step for EVERY
F=Q(T_1,...,T_s)[Y]/f with monic irreducible f of charged degree delta,
nonzero u_i in Y basis, sparse rational coefficients and binary T exponents?
Return FULL Rel={e:u^e=1}; s,delta,k grow, error<=eta. No place, constant
field, inverse or relation advice. Native contract and the reviewed quantum
upper bound are in SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md.

## Selection, mechanism and falsifiers

Fresh STATE/TRAPS, corpus been-tried and baselines preceded selection.
Independent directions were compared: inverse-trace search is already
classically matched on its native odd-degree sequence; bare supersingular
walk amplification leaves a square-root success cost; bilinear tensor-graph
Fourier outcomes have an exact classical Gaussian-elimination sampler.
No new end-to-end operation emerged there. The present attack instead tries
to remove the quantum step from an existing FULL native algorithm. It is
not a new restricted easy-face promise or a new quantum primitive.

Mechanism: compute Alg={e:u^e algebraic overQ} by all extended logarithmic
derivatives; compute a multiplicative leading-coefficient map to a small
number field, injective on constants, retaining ORIGINAL small atoms and
binary exponents; apply existing classical Lenstra--Silverberg relations
and integer intersection. Expected result if ALL gates close: polynomial
classical sparse-BIT fullRel, matching the known polynomial quantum upper
bound. The full constant-map gate is currently UNPAID. No speedup, novelty,
full classical solver or quantum execution claim.

Baseline: existing delta1/2 and monomialKummer classical algorithms;
finite-Q-algebra LS1509.08843 Thm1.11; numerical-degree valuation/factorization
algorithms. Dense factorization, giant characteristic-zero evaluation,
unstated sparse Puiseux clocks, or noncommutative determinant results after
commutative specialization are not valid substitutes. Actual Oki ICALP2020
Remark12 distinguishes numerical-degree clocks from sparse determinant-degree:
https://drops.dagstuhl.de/opus/volltexte/2020/12496/pdf/LIPIcs-ICALP-2020-89.pdf.
This source does not prove hardness of our map or exclude randomized algorithms.

## 1. Independently reviewed general-Alg algorithm

Clear rational scalar coefficients within each numerator/denominator pair.
Let D=product of ALL coefficient denominator polynomials, L their number,
b>=1 satisfy product_P max(2,||P||_1)<=2^b over input numerators/denominators,
H=2^b, and beta>=1 bound totalT degree. Put d0=(L+1)beta. Every coefficient
of f or u_i can be written p/D with ||p||_1,||D||_1<=H and degree<=d0.
These expressions are formal bounds, not expanded products. Zero numerators
are permitted. No cancellation of huge sparse exponents is required.

For multiplication byY let C=A/D be the delta-dimensional companion matrix.
Every entry of A has norm<=H and degree<=d0. The following matrices have
explicit formal numerator presentations with the indicated common powers:
    M(u_i)=A_i/D^delta,
    M(f_Y)=J/D^(delta-1),
    M((u_i)_Tj)=T_ji/D^(delta+1),
    M(f_Tj)=F_j/D^(delta+1),
    M((u_i)_Y)=Y_i/D^(delta-1).
Here T derivatives keep Y FORMALLY FIXED; later extend by
partial_j Y= -f_Tj/f_Y. The numerators use sums of powers of A, denominator
powers and ordinary numerator derivatives. Set
    U=[2(delta+1)(d0+1)H]^(2delta+4), e0=(delta+1)d0,
    V=delta! U^delta.
Every displayed numerator entry has l1norm<=U and degree<=e0: rational
coefficient derivatives have numerator p'D-pD', norm<=2d0H², and powers
of A contribute at most delta^(h-1)H^h per entry. Determinants and adjugate
entries have norm<=V. All logarithms of these bounds are polynomial in
native inputbits, including log(beta); none is a numerical-degree runtime.

Since char0 and f irreducible, f_Y is nonzero and invertible. Each u_i is
nonzero and invertible. After combining the extended derivative and u_i^-1,
    dlog_j u_i = [T_ji detJ - Y_i adjJ F_j] adjA_i
                / [D detJ detA_i],
as multiplication matrices applied to the vector1. A common denominator is
    h=D detJ product_i detA_i.
Multiply the numerator for i by product_(l!=i)detA_l. Every integer
coefficient of every resulting basis-coordinate polynomial is bounded by
    C0=2(delta+1)^3 U² V^(k+1),
and its totaldegree is at most (k+1)delta e0. The denominator h is nonzero,
has norm<=C0 and degree<=Dstar=d0+(k+1)delta e0. These are polynomial-BIT
bounds on an implicit matrix with k columns; its potentially huge number
of coefficient rows is never constructed.

In characteristic0 the common kernel of all s extended derivations is
exactly the algebraic constants. Hence the integer kernel of this implicit
coefficient matrix is Alg, a SATURATED lattice. The standard minor/HNF
kernel estimate gives a basis bound <=k!C0^k; conservatively use
    Balg=(2kC0)^(2k), R=2^k k Balg.
Choose a random prime p in[X,2X], where X exceeds 2kR C0 and
16(1+(2R+1)^k)Dstar/eta, and use capped prime generation as in the priornote.
All nonzero bounded-exponent numerator coefficients survive reduction;
h survives too. For uniform t in F_p^s, union-bound Schwartz--Zippel over h
and ONE nonzero coordinate polynomial for EACH false exponent in[-R,R]^k
bounds the bad point probability by eta/8. Exponent-box enumeration is
PROOF-ONLY. Reject bad denominators, nonunit f_Y and u_i.

Evaluate the logarithmic derivative matrix in the FULL finite algebra
F_p[Y]/f_t, retaining every Y-basis coefficient and every partial derivative.
It may be reducible; the f_Y unit test forces f_t to be squarefree.
No factorization is required.
Finite-field linear algebra computes its complete integer CONGRUENCE kernel
M (full rankk). On the good event Alg is contained in M and every vector
of M with infinitynorm<=R lies in Alg. Apply exact3/4-LLL in Z^k.

For rankr=rank Alg, lambda_r(M)<=sqrt(k)Balg, so the first r LLL vectors
have norm<=2^((k-1)/2)sqrt(k)Balg<R and belong to Alg. They span its real
space. Every later LLL vector lies outside that space and therefore has
infinitynorm>R. LLL size/Lovasz bounds give ||b_j||<=2^((k-1)/2)||b_j*||,
so all later Gram--Schmidt lengths exceed sqrt(k)Balg. Expanding any of the
short TRUE Alg basis vectors in the full M basis, its largest nonzero index
cannot be later thanr. Thus the first r vectors generate the WHOLE Alg,
not a finite-index sublattice. Select the prefix of norm<=R. Rank0/fullrank
are included. This gives a randomized polynomial sparse-BIT algorithm for
Alg only; algebraic constants and roots of unity are not thereby removed.

## 2. Independently reviewed direct-specialization falsifier

Let delta>=5 and even binary M>=2. Put
    A=2+T^M, B=T^M(T^M-1)A,
    f(T,Y)=product_(j=1)^delta(Y-jA)-B,
    u_j=Y-jA.
This is a promised native family with O(delta²) sparse monomials after
expanding the Y coefficients and polynomial coefficient BITlength.
A is irreducible by Eisenstein at2. Every nonleading Y coefficient of f
is divisible by A, and its constant coefficient divided by A is congruent
to -6 modulo A, because B/A is6 modulo A. Thus f is Eisenstein at prime
polynomial A, hence irreducible in Q(T)[Y]. All u_j are nonzero.

AtT=0, the delta branches have distinct constant terms2j. On branchj the
unit u_j cancels this first term and begins at orderM with coefficient
    -2^(2-delta)/product_(l!=j)(j-l).
At infinity the branches have distinct leading terms jT^M, but unit u_j
on branchj first has exponent M(4-delta); the relative cancellation depth
is M(delta-3). Therefore picking a simple branch does not make every
original unit's naive LC nonzero, and ordinary truncation through numerical
order costs exponentially in logM. Norm(u_j)=+/-B repairs this displayed cancellation by combining the known
other-branch leading coefficients. It does NOT identify constants alone:
u_i/u_j has norm1 and is nonconstant. At branchj overT=0, only u_j has
valuationM; all other u_i have valuation0. These valuations show Alg=0 for
THIS tuple, so its full relation problem is actually easy. The obstruction
is to the proposed operation, not the native problem. No general Puiseux
or norm-repair impossibility follows.

More strongly, for EVERY rational specialization a where all u_j can remain
units, expanded monic f_a has exponential coefficient height. At a=0,1,-1,
B(a)=0, f_a splits as product(Y-jA(a)), and localizing ALL u_j yields the
zero algebra. Those are not permissible good points. Every other rational a
has h(a)>=log2. Standard rational height inequalities give
    h(A(a))>=M h(a)-log4.
The coefficient of Y^(delta-1) is -delta(delta+1)A(a)/2, so its height is
at least M log2-log4-log(delta(delta+1)/2). Writing that supplied monic
presentation costs Omega(M) bits (take fixed delta or M much larger than
logdelta). This refutes a direct rational-specialization/poly-expanded-height
shortcut. It does NOT exclude changing primitive element/presentation,
compact atoms, nonrational specialization, or a different full algorithm.

## 3. Remaining gate and closed admission decision

The single scientific question remains the FULL classical counterpart.
GeneralAlg is an intermediate lemma that removes a specific first blocker;
it is not the requested full result. A paid constant map or alternative
constant-relation operation must still work uniformly in growingdelta,
all sparse inputs and binary exponents. No easy-face subclass is substituted.

Another precise shortcut fails even in the already classically solved quadratic
case. In F=Q(T)[Y]/(Y²-2T²), c=3+2Y/T and c^-1=3-2Y/T have identical
individual norm1, trace6 and characteristic polynomial X²-6X+1. The tuples
(c,c) and(c,c^-1) both have Alg=Z², but their Rel lattices are respectively
Z(1,-1) and Z(1,1), since c>1 in a real embedding. Individual characteristic
polynomials therefore lose joint embedding alignment. Mixed traces can
separate this pair; no lower bound against joint algebra methods follows.
This counterexample was independently proposed and checked directly here.

A small cyclotomic specialization would finish the constants step IF its
degree and good-point search were paid; no such general operation was found.
Do not apply sparse support-count bounds to the potentially exponential
expanded support of an implicit norm/determinant. The current attack does
not prove that a classical constant operation is impossible. It does not
replace the full question by a generic easy-initial-face promise. Reopen
with a concrete operation that handles the complete native model; otherwise
compare independent directions, rather than adding more nearby barriers.

## 4. Review, exact control and terminal API outcomes

Core review: audits/reviews/2026-11-07-general-sparse-constants-core.md.
It checks all five denominator exponents, the extended derivative formula,
U/V/C0/Dstar bounds, nonzero reduction, full congruence kernel and FULL LLL
prefix, including rank0/fullrank. Its norm-scope clarification is incorporated
above: the counterfamily's displayed tuple actually has Alg=0.

One exact CLASSICAL CAS control is
    audits/controls/general_sparse_constants/control.py
and its JSON. In the original quartic basis for (Y²-T^N)²-2, N=2^40+1,
it retains all four coefficients, uses only binary modular powering, and
recovers Alg rank5 for seven original units. The finite-algebra derivative
matrix has rank2; its full integer congruence lattice has index p². Exact
LLL returns the expected integral lattice, with no finite-index loss and
later Gram--Schmidt lengths beyond the short true basis. This case has
constants Q(sqrt2); sqrt2 is not1, and -1 has order2. Three explicit true
relations verify the constant/torsion distinction. No generic LS or fullRel
algorithm was executed. Control-only Balg=1 is NOT the theorem-sized bound.

At p257 dividing N, the derivative rank drops to1 and falsely admits Y,
confirming the essential characteristic requirement. A symbolic X=T^M
counterfamily control checks Eisenstein residue-6, all f(jA)=-B and the
coefficient causing specialization growth, without expanding M. First run
stopped on Sage gram_schmidt returning two objects rather than three; fixing
that API unpacking let the complete control pass. No formula was weakened.
The control proves no all-input theorem, confidence bound or growing-degree
runtime; those are in the reviewed derivation.

Primary source Oki's actual Remark12 is retained under
    audits/sources/general_sparse_constants/oki.pdf/.txt/source.json.
Earlier LS, kernel/LLL and prime-density source contracts are reused from
the preceding sparse-function-field notes; no source scope is expanded.

Claude input packets under audits/claude_inputs/2026-11-07-general-sparse-constants/
and runner bundles under audits/claude_runs/2026-11-07-general-sparse-
{derivative,constant-map} retain exact snapshots. Both calls are TERMINAL
with EMPTY response files. Opus derivative: refusal,10515 input/8102 output,
estimated USD0.2041. Opus constant-map: max_tokens,10382 input/32768 output,
estimated USD0.696888. Total USD0.900988. No report, accepted finding, retry,
pending call or exact balance inference. All mathematical claims above were
derived and independently checked outside these empty calls.

Disposition: general Alg is a complete WRITTEN classical polynomial sparse-BIT
algorithm; only the narrow control was executed. Full native classical Rel
remains OPEN at the compact constants operation. No full classical solver,
novelty, separation, quantum execution or general map-impossibility claim.

Milestone checks passed: STATE/title/Now/boundary row, actual Oki PDF hash,
both immutable API request/context bundles and terminal usage, core review,
exact control values/false gates, and scoped diff/whitespace. No full suite,
unrelated rerun, Git commit or balance inference.
