# Symmetric determinant characters: a rank-one receiver

2026-11-06. WRITTEN algorithm, independently reviewed Sections1--4.
No novelty, separation, cryptographic application or quantum execution.

## Question, input and admission

Can a structured growing-degree character family have a receiver polynomial
in degree and logp without supplied hidden coordinate blocks? Let n>=3,
N=n(n+1)/2, V=Sym_n(F_p), p odd, and L:V->V an unknown invertible linear map.
The native input is fresh exact global copies of

    p^(-N/2) sum_(A in V) lambda(det(LA)) |A>,
    lambda(0)=1; lambda(a)=chi(a) otherwise.

Output a polynomial-size circuit for det(LA) up to a nonzero scalar. The
receiver below outputs a symmetric determinant representation. L itself
is not identifiable: congruences and scalar changes preserve this target.
No full-value oracle, selected slice, inverse source or hidden decomposition
is supplied. BIT/Q2 access can prepare these copies, with its cost charged.

This is a bounded constructive test of a growing-degree receiver, not a
reduction of arbitrary univariate character reconstruction. Symmetric
determinants are an established algebraic family, but an external native
character-source application remains unestablished. Do not create a new
variant program on that basis. Ordinary full-matrix determinant characters
have the different, nearly uniform Fourier law recorded in
CHARACTER_DETERMINANT_FOURIER_ADMISSION.md; that rejection is unchanged.

Corpus lookup: `been-tried "symmetric determinant quadratic character Gauss
sums rank one Veronese Fourier reconstruction"`. It returned the ordinary
matrix rejection and older quadratic/shift notes, not this receiver.
Baseline lookup had no matching catalog entry; this is not hardness.
Primary literature was then searched. Taniguchi--Thorne, *Orbital
exponential sums for prehomogeneous vector spaces* (2016), Sections4--5,
gives explicit binary/ternary quadratic-form Fourier tables; it is relevant
prior art, not an all-n algorithm citation. The all-n identity below is
proved directly from scalar quadratic Gauss sums. The general polynomial
equivalence motivation does not authorize importing the ordinary-matrix
GGKS19 full-value algorithm into this different sign/copy model.

## 1. Exact auxiliary function and charged source error

Use the trace pairing <A,B>=tr(AB). On ordinary upper-triangle coordinates,
the QFT label y corresponds to Bii=yii, Bij=yij/2. This public conversion
is essential. Write gamma=p^(-1/2) sum_z exp(2pi i z^2/p), |gamma|=1,
and choose a public nonsquare nu. Define for analysis only

    G_t(A)=p^(-n/2) sum_u exp(2pi i t*u^T A u/p),
    H(A)=(G_1(A)+(-1)^n G_nu(A))/(2 gamma^n).

Diagonalizing A shows H=chi(det A) at full rank, H=0 at odd corank,
and |H|=p^(corank/2) at even corank. In particular corank-one contributions
cancel. Neither this diagonalization nor the unknown H state is an
operation in the algorithm.

The Fourier transform of H(A)/sqrt(p^N) has amplitude of absolute value
p^(-n/2) at EVERY nonzero rank-one symmetric matrix. These matrices split
into the square and nonsquare scalar classes; each nonzero preimage of
u->u*u^T has size2. At zero the amplitude has this magnitude for even n,
and is zero for odd n. All other Fourier coefficients vanish. Consequently

    ||H||^2 = 1 (n even), or 1-p^(-n) (n odd),

where the function norm averages over uniform A. The rank-one label set
has p^n-1 elements. Their projective underlying vectors are uniform.

Let s=Pr[det A=0]. For every u!=0 the linear map A->Au from Sym_n onto
F_p^n is surjective. Hence E[|ker A|-1]=1-p^(-n)<1; a singular matrix has
at least p-1 nonzero kernel vectors, proving s<1/(p-1), uniformly in n.
Let f0=chi(det A), zero on singular matrices, and f=lambda(det A).
H=f0+e with e supported on singular matrices. Orthogonality gives
||e||^2=||H||^2-(1-s)<=s, whereas ||f-f0||^2=s. Therefore

    ||H-f||^2 <= 4s < 4/(p-1) <= 6/p.                 (1)

This pays all padding and lower-rank contributions without postselection.
For any measurement event E,

    sqrt(Pr_actual[E]) <= ||Pi_E Fourier(H)|| + sqrt(6/p). (2)

Use this rare-event bound, not a total-variation estimate of order p^-1/2.
With hidden L, the transformed argument is (L*)^-1 B, so observed rank-one
labels lie on L*(rank-one cone), where * is the trace adjoint. They do NOT
lie on L^-T(rank-one cone). This transpose direction controls the decoder.

## 2. Learn the quadratic ideal from raw copies

Put h=binom(n+3,4), M=h+n+1. Take h independent raw Fourier labels and
evaluate all N(N+1)/2 degree-two monomials in each. The pullback of a
quadratic under u->L*(u*u^T) is a quartic in n variables. This pullback
is onto the h-dimensional quartic space: every degree-four monomial is
a product of two degree-two monomials, and 2 is invertible.

Until the evaluation rows have rank h, a missing row direction corresponds
to a nonzero quartic. Schwartz--Zippel bounds its vanishing probability on
uniform nonzero u by at most4/p (the homogeneous zero at0 only improves
this bound). Adding the possible ideal zero label costs at mostp^-n.
By (2), the probability that a raw label is invalid OR fails this rank
increment is less than (sqrt5+sqrt6)^2/p <24/p. The argument is uniform
in the adaptive previously observed span. With probability at least
1-24h/p, all h rows are valid and their kernel is EXACTLY the degree-two
ideal I2 of the transformed rank-one symmetric cone.

These quadrics cut out the cone: in standard coordinates they are the
2x2 minors. At a nonzero point u*u^T their common differential kernel
is T_u={u*v^T+v*u^T:v in F_p^n}, of dimension n. All these operations
are public linear algebra on the learned quadrics and measured labels.

## 3. Public coordinate reconstruction without square-root advice

Take n more raw labels v_i. On the good event they have underlying vectors
u_i forming a basis. Form their tangent spaces T_i from I2. For i!=j,
T_i intersect T_j is one-dimensional; choose any nonzero w_ij in it.
The N vectors v_i and w_ij form a basis of the observed ambient space.
These dimension and independence tests are public.

Take one more raw point v0 and expand

    v0=sum_i c_ii v_i + sum_(i<j) c_ij w_ij.

Require every coefficient nonzero. Define a public linear map U on Sym_n by

    U(Eii)=c_ii v_i,
    U(Eij+Eji)=c_ij w_ij, i<j.

Indeed write v_i=L*(beta_i u_i*u_i^T),
w_ij=L*(beta_ij(u_i*u_j^T+u_j*u_i^T)), and
v0=L*(alpha u*u^T), u=sum_i a_i u_i. The displayed coefficients imply
U=L* C, where C(A)=alpha S A S^T and S has columns a_i u_i. Thus

    det(U* A)=alpha^n det(S)^2 det(LA).                (3)

This is the desired projective output. No individual beta, alpha, a_i,
square root or hidden original u_i is computed. In coordinate matrices,
the trace adjoint is D^-1 U^T D, D=diag(1 diagonal,2 off-diagonal).

The n basis samples each have ideal bad mass at most2/p (a proper
linear subspace plus zero), giving actual failure less than15/p by(2).
The last point avoids n coordinate hyperplanes; actual failure is at
most(2n+14)/p<=7n/p. Including training, total attempt failure is at most
24M/p. For p>=256M a complete attempt succeeds with probability >7/8.
Failed public dimension checks return ABORT. A bad attempt may return a
wrong candidate; no unproved deterministic certification is claimed.

## 4. Finite caps and amplification

Use an odd R>=8 ln(4/eta) independent attempts. Correct candidates form a
strict majority except with probability eta/4, using even the weaker
success bound3/4. Compare two output determinant circuits projectively by
testing F(x)G(z)-G(x)F(z)=0 at K independent random pairs x,z. For
nonproportional polynomials this is nonzero, of total degree2n, so one
false match has probability <=2n/p<=1/4. Take
K=ceil(ln(4R^2/eta)/ln4) and union-bound all pair comparisons by eta/4.
Select any candidate matching more than R/2 candidates, counting itself;
otherwise ABORT. This is bounded O(R^2) comparison work even when erroneous
PIT answers are nontransitive; no largest-clique computation is hidden.

Allocate at most eta/4 total circuit approximation error over all MR
copies. The QFT and public field operations have standard polynomial
precision cost. Copies O(n^4 log(1/eta)), time/storage polynomial in
n,logp,log(1/eta). Polynomial linear algebra may have a large exponent;
no optimized exponent is asserted. No amplitude amplification or inverse
source is used. This is a WRITTEN algorithm, not a circuit execution.
For each classical uniform field draw, reject integers >=p from
ceil(log2 p) fair bits; acceptance is >1/2. The known polynomial bound B
on requested draws permits a cap ceil(log2(4B/eta)) per draw, with total
abort probability <=eta/4. The nonsquare and H are analysis only and
need not be generated. These four eta/4 budgets close the finite ledger.

## 5. Native classical complete-line and Jordan-algebra baseline

This comparator has chosen classical padded-sign access to the SAME F,
not a full-value oracle. Quantum BIT/Q2 access prepares the theorem's
global copies with one sign query each. Copy-only input and classical
chosen queries must still be distinguished; no query separation follows.
The common output is an evaluable projective polynomial circuit. The
quantum construction additionally supplies a symmetric matrix pencil;
the classical construction below need not recover its coordinates.

For p>=65536n^2, a WRITTEN classical algorithm uses
O(p*(N^3+log(1/eta))) sign queries and polynomial(n,p,log(1/eta)) time.
The p threshold is deliberately separate from the quantum threshold.
The imported full-table routine and the composed classical algorithm
have NOT been executed.

Given a base v and a direction w, query all p signs of
f(t)=F(v+tw). Run Kopparty's Algorithm A on both r=+lambda(f) and
r=-lambda(f), with degree bound n and error bound n. The ACTUAL
Theorem3.1 in Section3.1 of arXiv2601.07137 requires

    degree <= (epsilon/16)*sqrt(p), errors <= (1/8-epsilon)*p.

Use epsilon=1/16, hence n<=sqrt(p)/256. Do not replace this by the
less precise introduction threshold. Root padding contributes at most n
corruptions. Require the returned q to be monic, squarefree, degree
EXACTLY n, q(0)!=0, and Delta(chi(q),sigma*lambda(f))<=n for the selected
sigma in {+1,-1}. All these checks are public and polynomial(p,n).

This acceptance test certifies q=f/lc(f). For nonzero f, if qf is NOT a nonzero
scalar times a polynomial square,
the test implies |sum_t chi(q(t)f(t))|>=p-3n, whereas Weil gives at most
(2n-1)sqrt(p), a contradiction at the stated threshold. Otherwise qf=c*h^2
with c!=0, and
squarefreeness and deg q=n>=deg f force f to be a scalar times q. An
identically zero f is excluded by the same one-polynomial character bound.
Thus bad or repeated-root lines cannot contaminate accepted jet data,
even if the imported decoder returns arbitrary output outside its promise.
For a good line the correct leading-character choice is within the
decoder promise and is accepted.

A first accepted random (v,w) certifies A=L(v) nonsingular. Retain v.
For any fixed invertible A, the polynomial

    det(B)*disc_t(det(A+tB))

in symmetric B has total degree <=n^2 and is nonzero. Exhibit B in an
A-orthogonal basis with n distinct nonzero generalized eigenvalues;
p>n suffices. Hence a uniform direction is good with probability at
least1-n^2/p. This bound and the earlier singularity bound pay initial
base selection; finite geometric caps consume only logarithmic overhead.

For each accepted line normalize q by q(0), obtaining
1+a1*t+a2*t^2+a3*t^3+... . For X=A^-1 L(w), compute

    r1(w)=a1=tr(X),
    r2(w)=a1^2-2a2=tr(X^2),
    r3(w)=a1^3-3a1*a2+3a3=tr(X^3).

These are homogeneous polynomials of degrees1,2,3 in the PUBLIC direction
w. Recover them by ordinary interpolation on random accepted directions.
A missing degree<=3 relation vanishes on at most3/p of all directions;
raw progress probability is therefore at least1-(n^2+3)/p. Conditional
Bernoulli domination gives O(N^3+log(1/eta)) raw directions for full rank,
with finite caps. No global all-lines-good event or n^8 prime threshold
is needed. Bad lines are rejected after their fully charged p queries.

Polarize r2,r3 to obtain T(X,Y)=tr(XY) and C(X,Y,Z)=tr(XYZ). For
A-selfadjoint matrices, adjoint reversal and cyclicity make C symmetric.
T is nondegenerate: the map B->A^-1 B A^-1 is a bijection of Sym_n and
the trace pairing on Sym_n is nondegenerate in odd characteristic.
Solving the public linear equations

    T(X circle Y,Z)=C(X,Y,Z)

recovers the Jordan multiplication X circle Y=(XY+YX)/2 in PUBLIC input
coordinates. Use Jordan powers of x and r1 to calculate tr((A^-1Lx)^k)
for k<=n. Newton identities, with all k invertible since p>n, output

    det(A^-1Lx)=F(x)/F(v).

The resulting polynomial-size arithmetic circuit is an exact projective
reconstruction on the successful interpolation event. No hidden matrix,
eigenbasis, inverse source, determinant-value oracle, or imported GGKS19
equivalence theorem enters this algorithm. Its p dependence is charged;
it does not prove classical polynomial-logp recovery or hardness.

A separate classical implication illustrates the sign-model boundary.
Let L_s shear A11 to A11+s*A22, leaving every other coordinate fixed.
It is invertible for every s, and

    F_s(A)=det(A)+s*A22*det(A_hat1,hat1)=b(A)+s*a(A).

A shifted-Legendre TRIT oracle chi(s+t) simulates one padded determinant
query exactly: for a!=0 use t=b/a, multiply the nonzero answer by chi(a),
and restore +1 at a zero trit; a=0 is public. A projective output G recovers
s from G(diag(0,1,...,1))/(G(I)-G(diag(0,1,...,1))). The denominator is
the nonzero projective scale. This is an implication only, not classical
hardness, a copy-only reduction, or a silently identical padded-bit model.

## 6. Falsifiers, review and current evidence

Decisive first falsifiers were a wrong Gauss normalization, hidden factor2,
large lower-rank norm, nonexistent rank escape, or unpaid tangent-frame
alignment. Independent ACTUAL-TEXT core review accepted Sections1--4,
including source error, adaptive rank escape, scalar frames, the adjoint,
bounded majority selection even on bad PIT outcomes, and all four eta/4
budgets. A separate reviewer checked the native complete-line/Jordan
baseline and actual Kopparty theorem threshold. Its polynomial-p cost is
not a classical lower bound. Novelty and external source application remain
unestablished; no asymptotic separation is asserted.

Two classical finite FFT controls used exhaustive symmetric matrices and
RAW quadratic exponential sums (not the claimed rank formula): n3p5 and
n4p3. Actual rank-one masses .63995904 and .4070442438577388; singular
masses .2064 and .358024691358. The respective ||H-f||^2 are .4048 and
.636488340192044, below4s. Ideal norms .992 and1; rank-one ideal masses
.992 and .987654320987655, zero masses0 and3^-4. Off-support ideal mass
<7e-31 and full-rank/corank-one identities error<4e-15. Exact modular
determinants agreed with independent Leibniz determinants in every case.
These primes are BELOW the theorem threshold. They are normalization
falsifiers, not evidence of asymptotic efficiency or a quantum run.
Durable producer/evidence: classical_baselines/symmetric_det_fft_control.py
and .json. Its six assertion types pass on exactly these two cases.

One exact Sage IDEAL-label decoder control uses n3,p65537,seed20261106.
The public decoder receives ONLY19 labels and n; no L, original vectors
or inverse. It obtains training rank15, ideal dimension6, tangent
dimensions3, frame rank6 and exact symbolic projective equality with
scale18838. Ignoring the trace factor2 or using the inverse-transpose
instead produces a nonproportional polynomial in both negative controls.
Truth enters only AFTER decoding. Producer/evidence:
classical_baselines/symmetric_det_ideal_decoder_control.py and .json.
This checks the ideal decoder, not the actual contaminated-source run.
No repeated sweeps or registry promotion is authorized.

The known-column full-matrix alternative is not a separate admitted
program: measuring all but one supplied block gives exact conormal
incidences and a polynomial decoder, but that supplied decomposition
does not solve general L or univariate reconstruction. Its native classical
competitor reduces each linear form to shifted-Legendre line recovery.
The symmetric mechanism above genuinely removes the supplied blocks in
its own different, explicitly stated family. It supplies no conversion
between those families or from a univariate companion pencil.

Sources: https://thornef.github.io/gauss-ff-submit.pdf;
https://arxiv.org/abs/2601.07137 (Algorithm A/Theorem3.1, actual text in
audits/sources/legendre_prf/kopparty_noisy_2601_07137.txt). Prior ordinary-
matrix source scope is in the admission note. Priority search found relevant
quadratic-form Fourier tables, not a verified all-n reconstruction citation;
absence of a search hit does NOT establish novelty.
