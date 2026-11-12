# 2026-11-13 — Independent native Macdonald real-time composition

**Closed written endpoint, under the reviewed transform interface.** For every
numerical D>=1, explicit occupation partition mu of D, signed binary integer a,
positive binary integer c, and accuracy b>=0, the native Hamiltonian below has
a uniform clean circuit for time T=2pi a/c with BIT, gate and workspace cost
poly(D,L,b), where L is the combined binary length of a,c. Its restricted
operator error is <=2^-b, including workspace and any reference. Measuring
occupations gives the requested full joint law within TV 2^-b.

This is a written construction, not an implementation, novelty, hardness, or
useful-speedup claim. The matched exhaustive classical sampler also has cost
exp(O(sqrt(D))) poly(D,L,b); it is already polynomial in the binary time length.
The unrestricted polynomial-in-D classical question is not decided here.

Read STATE/TRAPS and checked the newest handoff title; read the dynamics note,
the reviewed clean transform interface, actual Nazarov–Sklyanin2015 Eq. 1.6,
1.15–1.18 (retained text LF 108–145 and 224–267), and Gu–Somma–Sahinoglu
Definitions 2.1–2.2 / Theorem 3.1 and its proof (LF 166–218, 437–527).
No in-flight reports, network, API, Git, implementation, or sweeps were used.

## 1. Source identity, normalization, and specialization

Fix N=D+1, t=D/N, q=t^3 globally. Define V_n by

    sum_(n>=0) V_n z^n
      =exp(sum_(k>=1) (1-t^k)p_k z^k/k).

This is precisely the source's Q(z), Eq. 1.6; its Q_n are NOT normalized
Macdonald polynomials. Star is adjoint for the Hall(q,t) metric. On degree D,

    H = (1-t)^-1 sum_(n=1)^D q^-n V_n V_n^*.                 (1)

The sum truncates because V_n^* lowers degree by n. Actual Eq. 1.17 has this
factor 1/(1-t), and Eq. 1.18 gives

    E_lambda=sum_(i=1)^D (q^(-lambda_i)-1)t^(i-1)
      =(q^-1-1)sum_(boxes (i,j) in lambda) t^i q^-j.          (2)

The second identity is the finite geometric sum in each row; box indices are
zero-based. H is a finite self-adjoint positive operator. This is the NS first
Hamiltonian on Fock degree D, not the auxiliary-marker Lax operator used to
construct the transform.

Although the source first treats independent q,t and generically distinct
energies, no energy-gap assumption is needed here. The previously reviewed
positive Hall Gram argument makes the monic triangular orthogonal P_lambda
analytic throughout 0<q,t<1. Multiplication by the nonzero positive hook
product gives J_lambda. Each finite-degree entry of H and each E_lambda is
also analytic there. Thus the generic identity H J_lambda=E_lambda J_lambda
extends to q=t^3. The complete orthogonal J basis survives any coincident
energies. No division by E_lambda-E_mu is performed.

Let U send the shape label lambda to Jhat_lambda in the canonical occupation
basis p_nu/sqrt(R_nu), with

    R_nu=z_nu product_k (1+t^k+t^(2k))^m_k.

The transform interface is a clean poly(D,log(1/delta)) finite-gate circuit,
uniform in shape superpositions/reference, with restricted error delta.
Its ACTUAL reversed word implements U^dagger on the entire occupation sector
with the same bound, because that sector is the full clean range of U.
All coefficients of U are real. Equations (1)–(2) therefore prove

    exp(-i T H) = U diag_lambda(exp(-2pi i a E_lambda/c)) U^dagger,       (3)

including the sign and the target occupation amplitudes in the parent note.

## 2. Exact rational phase arithmetic, without a long-time precision gap

Use the following explicit, not necessarily reduced, common denominator:

    Q_D=D^(3D) N^D.

For every lambda put

    e_lambda = sum_(i=1)^D
       (N^(3lambda_i)-D^(3lambda_i))
       D^(3D-3lambda_i+i-1) N^(D-i+1).                       (4)

All exponents are nonnegative and E_lambda=e_lambda/Q_D. Padded zero rows
give zero terms. Powers only up to O(D) occur. Their computation, summation,
and reversible implementation have a fixed polynomial bit clock; an O(D)-size
constant-power table or direct exponentiation suffices, with no partition table.

For clarity, the energies are also uniformly bounded. Every box content lies
in (1/4,21), and

    N(q^-1-1)=3+6/D+4/D^2+1/D^3<=14.

Thus 0<E_lambda<300 and 0<e_lambda<300 Q_D. In particular

    bit(Q_D), bit(e_lambda)=O(D log(D+1)).                    (5)

Compute, EXACTLY with Euclidean signed remainder,

    d=c Q_D,  r_lambda=(a e_lambda) mod d,  0<=r_lambda<d.    (6)

Then the desired phase is exp(-2pi i r_lambda/d). Products, division and
remainder use O(L+D log(D+1)) input bits. No integer factoring, period finding,
approximate eigenvalue, or numerical argument reduction is needed.

Given m fractional bits, compute the integer

    z_lambda=floor(2^m r_lambda/d).

Its exact reversible arithmetic has bit cost polynomial in
L+D log(D+1)+m. The phase exp(-2pi i z_lambda/2^m) differs by at most
2pi 2^-m in complex modulus, uniformly in lambda,a,c. The actual magnitude
|a/c| no longer appears in that error bound, because (6) was exact.

This does NOT license an eigenvalue approximation of b bits before multiplying
by an arbitrary large time. Such an approximation would require the additional
log(1+|a/c|) precision. Here that issue is paid by exact rational arithmetic.
The contract specifies an exact rational multiple of 2pi, not an unspecified
real time or free absolute-time precision. Also poly(L) is not a claim of
poly(log(1+|T|)) for rational inputs with arbitrarily long denominators.

As a harmless consequence of the explicit denominator, 2pi Q_D is a common
period of H on this sector. No minimal-period claim is made, and this fact
is not needed as an oracle or an algorithmic assumption.

## 3. Controlled phases, actual inverses, and the clean error ledger

Set epsilon=2^-b, take each transform with delta=epsilon/16, and choose
m=b+8. Reversibly compute (4), (6), and z_lambda into fresh registers. If
z_lambda/2^m=sum_(j=1)^m z_j/2^j, apply on its j-th bit the diagonal gate

    P_j=diag(1,exp(-2pi i/2^j)),

then reverse the SAME arithmetic computation to erase e,r,z and its scratch.
There are m phase gates, not a selector over all partitions. In particular
P_j is the actual diagonal phase, including its scalar phase; replacing it by
an R_z gate while dropping a phase is not the stated clean operator circuit.
An additional coherent control can be included with the same finite compiler.

The earlier finite-palette compiler gives full clean error <16*2^(-b_0/2)
per such gate, using only exact reversible arithmetic and fixed gates. Choose

    b_0=max(8,ceil(2 log2(512(m+1)/epsilon))).

The m compiled phase-gate errors sum to <epsilon/32. The fractional truncation
contributes 2pi 2^-m<epsilon/32. Computing pi/sines/cosines for these bounded
constant angles to the stated precision has polynomial bit cost. Their lower
scratch is retained; it is not measured, discarded, or reset. All arithmetic
in (4)–(6), including the floor defining z, remains exact.

Use the physical word

    U_tilde  Phi_tilde  U_tilde^dagger                       (7)

with the SAME transform banks and its actual inverse, and separate phase
scratch. Input occupation registers encode a basis partition directly and
cost polynomially many bits/gates to load. No amplitude-loading task is hidden.
Invalid label encodings have safe defined arithmetic branches so every word
is a unitary on its ambient registers.

For any occupation state psi (also entangled with a reference), the inverse-
on-range identity gives error <=delta for U_tilde^dagger on psi with clean
transform workspace. The phase step has the uniform clean bound just proved.
The final U_tilde contributes delta on the ideal clean shape state. Unitary
hybrid bounds carry the actual leakage through all subsequent operations;
the argument never assumes leaked workspace reset itself. Therefore

    || (7)|psi,0> - (exp(-iTH)|psi>)|0> ||
       <=2delta+epsilon/32+epsilon/32
       =3epsilon/16 <epsilon.                              (8)

This is a restricted operator bound. Measuring occupations and tracing all
other registers gives TV error at most the same vector bound. In particular
it proves the promised sampler for EVERY explicit mu, not only a row, column,
few-mode state, or a distribution of starting occupations.

The precision allocation is noncircular: epsilon fixes delta,m; m fixes the
number of phase gates; their accuracy fixes b_0. The transform's existing
compiler is invoked at the already fixed delta. Reversible arithmetic uses
O(L+D log(D+1)+m) bits and polynomially many operations. All counts are thus
poly(D,L,b), with D charged numerically. A supplied general state is also
evolved correctly, but its preparation is not granted by this theorem.

Gu–Somma–Sahinoglu Theorem 3.1 explicitly gives the known diagonalize/evolve/
undo mechanism and warns that selecting exponentially many blocks can cost
exponentially much. Here (4)–(6) give the uniform reversible selector instead.
The theorem is not used to import exact real gates, an exact transform, or an
unpaid phase oracle; those costs and approximation errors are paid above.

## 4. The exhaustive classical clock is also polynomial in binary time

Let P=p(D). The already-stated exhaustive comparator can be made a bounded-
clock TV-epsilon sampler in P^O(1) poly(D,L,b) BIT time. One explicit way is
as follows; it uses no energy-gap division or polynomial-coefficient-height
assumption in D alone.

Enumerate the partitions of D and form the power-sum/monomial transition
matrix T. Multiplication of m_nu by p_k produces at most D+1 monomial types,
with integer multiplicities at most D+1: either add k to one existing exponent
or introduce a new exponent k. Repeating at most D multiplications builds each
p_lambda column in polynomial P,D operations. A bound (D+1)^(2D) on the sum
of absolute coefficients suffices, so the initial entries have O(D log(D+1))
bits. This is computation over partition types, not enumeration of D^D labelled
monomials.

In the power-sum basis the Hall Gram matrix is diagonal with entries R_nu.
They have common denominator N^(2D), since each r_k has denominator N^(2k).
The numerator heights are O(D log(D+1)). Inverting T and multiplying matrices
gives the positive rational Gram matrix in the monomial basis. Fraction-free
elimination and Hadamard bounds on minors show polynomial P,D bit lengths
throughout: determinants of a P-by-P matrix with B-bit entries have
O(P(B+log P)) bits. Clearing common denominators preserves this polynomial
bound.

Perform exact rational Gram–Schmidt, or fraction-free LDL, in a fixed total
order extending dominance. Positive leading principal minors prevent zero
pivots. Generically this is precisely the defining triangular orthogonal
Macdonald basis, and the positive-Gram continuation proves the same at q=t^3.
Its coefficients and squared norms are ratios of the stated minors, hence
have polynomial P,D bit length. Converting back to power sums and normalizing
gives every U_(nu,lambda) as a rational coefficient times a square root of a
positive rational. Their approximation to absolute error h costs polynomial
P,D,log(1/h) bits and operations. Any large rational coefficient or small norm
is paid by its proved bit length. Square roots are evaluated separately;
no joint algebraic number field is constructed. This is NOT a polynomial-in-D Gram algorithm;
the P factors are explicitly charged.

For the given mu compute all exact rational energies by (4) and all reduced
phases by (6). Evaluate each phase and each U entry to absolute error

    h=epsilon/(1024 P^2).

Use dyadic approximations and exact arithmetic on them to form

    Atilde_nu=sum_lambda Utilde_(nu,lambda) phasetilde_lambda
                                      Utilde_(mu,lambda).

Since true U entries and phases have modulus <=1, each summand has error
<=7h. Thus ||Atilde-A||_2<=7 P^(3/2)h<=epsilon/128. This bound is independent
of |a/c| because phase reduction was exact. Compute the nonnegative rational
weights |Atilde_nu|^2 and normalize by their positive sum. The resulting law
has TV distance <=3||Atilde-A||_2 from the target. A uniform
b+ceil(log2 P)+6-bit grid and exact comparisons against its cumulative
probabilities add TV error <=epsilon/64. This is a fixed finite clock, not
an expected-time rejection or an unresolved rare conditioning event.

All steps cost P^O(1) poly(D,L,b); sums and rounding need only b+O(log P)
additional precision beyond the charged rational-coefficient heights.
Finally P=exp(O(sqrt(D))). An elementary upper bound follows by evaluating
product_(k>=1)(1-x^k)^-1 at x=exp(-1/sqrt(D)) and using
1/(exp(y)-1)<=1/y. Thus this is the claimed
exp(O(sqrt(D))) poly(D,L,b) classical baseline, already logarithmic in the
magnitude of binary integer times. No optimality claim about this baseline
or obstruction to a polynomial-in-D classical sampler follows.
