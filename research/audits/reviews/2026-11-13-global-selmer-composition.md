# Conditional global GRH Selmer-dimension composition

2026-11-13. Independent negative audit of the completed 798-line OpenAI
global-composition report, after current STATE and the supplied
`global-primary.md` / `descent-primary.md` packets. The retained full
Poteaux--Weimann text was additionally checked at physical lines 50--104
and 773--850, and Biasse--Song at 895--945, 1573--1644 and 1710--1781.
No Git, network, API, implementation or numerical sweep. Commands used
`/opt/anaconda3/bin/python`. Parent owns shared notes.

## Verdict and exact conditional statement

ACCEPT the conditional composition. No further global obstruction was found.
For native monic squarefree f in Z[x] of odd degree 2g+1, the cited complete
compact-unit theorem and the cited GRH class-generator bound, together with
a UNIFORM complete local-image algorithm at every p dividing 2 disc(f),
give a bounded-error quantum polynomial-BIT algorithm for the integer

    dim_F2 Sel^(2)(Jac(y^2=f)/Q).

Individual field factors may have even degree, complex embeddings and
non-Galois normal closures; none of those closures is constructed.

The local premise includes all bad primes, polynomial dependence on log p,
and polynomial-time comparison with elements of the native algebra in
explicit common squareclass frames. Bare binary image vectors or merely
mathematical, inefficient frame identifications do not suffice. Ordinary
polynomial-bit frame representatives, or the native evaluation/translation
maps intended in the report, satisfy this interface.

The local premise is CONDITIONAL here. This review does not promote the
fixed-dyadic candidate or establish all-prime local images. It also does not
assert a complete classical algorithm, necessity of computing full units,
Mordell--Weil rank, novelty, hardness, separation or quantum advantage.
Global unit completeness is probabilistic, so the global result is bounded
error; it is not a claim that every possible incorrect run is detectable.

## 1. Native orders and the word-to-bit charge

Put n=deg f and h=ceil(log2(2|disc f|)). The integer resultant determinant
gives h=O(n(B+log n)) for maximum coefficient bit length B. Classical
rational polynomial factorization gives monic integral factors f_i of
polynomial encoding length. Quantum integer factorization of |disc f|,
with multiplication/primality checks, supplies all primes needed for the
factor discriminants, since

    disc f = product_i disc(f_i) * product_(i<j) Res(f_i,f_j)^2.

The actual number-field Poteaux--Weimann Theorem 1 requires the index or
discriminant factorization. That premise is now supplied. Its A=Z bound
is stated in WORD operations; the report correctly does not relabel that
displayed estimate as a sharp bit bound.

The full source proof supports the weaker polynomial-bit consequence:
its OM work is at precision sigma controlled by local index/discriminant
valuations; its coefficients are reduced modulo p^sigma; MaxMin stores
bounded valuations; and the local bases are glued by finite CRT. Here
`sigma log p=poly(h)` and log p<=h. Reading and reducing the original
polynomial separately costs poly(n,B,h). Triangular basis denominators
divide the index, and numerator coefficients can be reduced modulo those
denominators (source lines 69--72). Thus all exact basis data have
polynomial bit length. MaxMin/CRT and residue arithmetic have polynomial-
bit operands. The case of index one still pays input/output and arithmetic
costs; a zero displayed h_index term is not a free native-input shortcut.

Multiplication tables and native-coordinate conversion matrices then have
polynomial encoding size. Cauchy bounds for the native roots bound all
embeddings of these basis elements by exp(poly(n,B,h)); the nonzero trace
discriminant bounds inverse conditioning. Certified embedding approximation
and ordinary lattice reduction therefore prepare the controlled integral
basis needed by the compact-unit algorithm, with polynomial bit precision.

Prime decomposition must be in these maximal orders, including at primes
dividing the power-basis index. Factoring f_i modulo such a prime alone
would be invalid. Finite-algebra decomposition and verified randomized
finite-field factoring have the required polynomial dependence on log p.

## 2. The GRH factor base is a polynomial-size native object

Let P0 contain the rational primes dividing 2 disc f, and S_i contain ALL
prime ideals above them in K_i. For each non-rational field use a computable
integer cutoff at least `48(log|Delta_Ki|)^2`, for example a suitable fixed
multiple of h^2. Enumerate rational primes up to that numerical cutoff,
decompose them in the maximal order, and retain the required prime ideals.

This enumeration is polynomial: the cutoff itself is polynomial in the
native bit length, and there are at most n ideals above each rational prime.
It is not enumeration up to a large bad prime p. Under the cited GRH
assertion these ideals generate the ORDINARY class group. Put T_i=S_i
union this generating set. Then

    sum_i |T_i|=O(n(|P0|+h^2)),
    max_(P in T_i) log Norm(P)=O(nh).

These are precisely bounded parameters for Biasse--Song Theorem 1.
For K_i=Q, use Cl(Z)=0 directly, T_i=S_i, and the explicit unit-squareclass
basis consisting of -1 and the rational primes in P0. Do not apply a
log-discriminant generator formula at Delta_Q=1.

## 3. Complete compact units and a constructive torsion bit

The required source is the COMPLETE Biasse--Song Theorem 1, with Section
8.1 / Proposition 7's exact compact recovery. Theorem 5 alone supplies
approximate HSP lattice data. The retained source also has the approximate-
generator-to-basis step (Algorithm 3); independent valid units of the right
rank would not certify completeness.

Obtain lifts of a basis of U_Ti/mu(K_i), not just a finite-index subgroup.
Append a generator of mu(K_i)/mu(K_i)^2 in EVERY field factor. This quotient
has one bit, generated by a primitive root of the largest 2-power order
in K_i. Appending only -1 can fail, for example in Q(i).

Start at zeta=-1 and repeatedly decide whether z^2=zeta has a root in K_i.
If yes, either root has twice the current order. If no, the current root
generates the full 2-primary roots-of-unity subgroup. There are O(log d_i)
tests because phi(2^a)=2^(a-1)<=d_i. A root of unity that is a square in
K_i^* is already the square of a root of unity, so this bit injects into
field squareclasses.

The parent's constructive square test removes the need for a new general
number-field factoring black box. For K=Q[theta] of degree d and zeta!=0,
form the etale algebra B=K[z]/(z^2-zeta). For integers

    0<=c<=binom(2d,2),
    R_c(T)=Norm_K/Q((T-c theta)^2-zeta),

some R_c is squarefree. For two distinct embeddings of B, equal theta
values force different z values, so no c causes a collision. Otherwise
at most one c causes a collision. The displayed set has more candidates
than pairs. Squarefreeness is tested over Q.

If zeta is not a square, B is a degree-2d field, and the separating element
z+c theta has irreducible characteristic polynomial R_c. If zeta is a
square, B=K times K and R_c has exactly two distinct irreducible factors,
each of degree d. Factor the squarefree R_c over Q. In the split case,
the gcd over K[T] of either degree-d factor with
`(T-c theta)^2-zeta` is linear, giving z+c theta and hence a square root.
Both linear roots cannot belong to the same rational factor, since that
would contradict separation. Resultants, rational factorization and exact
subresultants suffice; no support/field closure is constructed.

There is no iterative height explosion. For an integral basis omega_j and
any root of unity zeta, the coordinates satisfy

    sum_j Tr(omega_i omega_j)c_j=Tr(zeta omega_i).

All conjugates of zeta have absolute value one. The controlled basis bounds
the integer right sides and trace-matrix entries by exp(poly(input size));
its determinant is the nonzero field discriminant. Cramer bounds make
every c_j polynomial-bit, uniformly over all these roots. Consequently the
quadratic tests, separating resultants and returned roots stay polynomial.

The resulting basis of U_Ti/U_Ti^2 has dimension
`rho_i+|T_i|`, where rho_i=r1_i+r2_i. A generator in one factor is embedded
with value ONE in all other factors. Value zero would not be in L^*.

## 4. Exact virtual-squareclass identification

For each field let K_i(S_i,2) be the squareclasses with even valuations
outside S_i. Let V_i record valuation parity at T_i minus S_i. Then

    ker(V_i: U_Ti/U_Ti^2 -> F2^(T_i minus S_i))
          ~= K_i(S_i,2).                              (3)

Injection: if a T_i-unit u=x^2 in K_i, every valuation of x outside T_i
is zero, so x is itself a T_i-unit.

Surjection: for alpha in K_i(S_i,2), form the fractional ideal a from
half its valuations outside T_i. Since T_i generates the class group,
choose a T_i-supported fractional ideal b with [b]=[a]. If
`(x)=a b^-1`, then u=alpha/x^2 is a T_i-unit and has even valuations at
T_i minus S_i. These ideals and x are proof-only witnesses; the algorithm
uses the complete unit basis and a binary kernel and never computes them.

Thus the construction includes the S_i-class-group 2-torsion contribution.
Replacing (3) by genuine S_i-units would in general lose classes. The exact
sequence with Cl(O_Ki,Si)[2] gives the report's dimension check, but that
check is not a completeness certificate for probabilistically found units.

## 5. Norms, compact localization and common finite frames

Prime-ideal valuations use their integer normalization. The correct norm
formula is

    v_p(Norm_K/Q u)=sum_(P|p) f_P v_P(u),

with RESIDUE degrees f_P, not ramification indices. Add the rational-sign
row, computed from all real embeddings; complex pairs contribute positive
norm. Rows for rational primes below T_i outside P0 become zero after (3).

There is no quotient by diagonal rational squareclasses. In fact the norm
from product_i K_i(S_i,2) onto Q(P0,2) is surjective: diagonal rational a
has norm a^n, and n is odd. The norm constraint therefore has rank |P0|+1.
This matches the actual odd-degree norm-kernel model in Stoll Lemma 4.1.

Represent each compact unit by its polynomially many exact small atoms and
binary exponents. Evaluate squareclasses using exponent PARITIES only.
For base 2, all positive-level powers in an integral compact representation
are squares; fractional corrections still contribute their parity atoms.
Store later basis changes as binary matrices. No huge unit is expanded.

The original full-unit valuations supply exact support bookkeeping (or can
be computed as binary-weighted sums of atom valuations). A small parity
representative can have EXTRA EVEN valuations outside T_i. Its actual
support must not be confused with the original unit's support. This does
not affect any squareclass map or parity constraint.

For local evaluation of an atom gamma, choose a polynomial-bit positive
integer b clearing its basis denominators and set alpha=b^2 gamma. This
is integral and has the same squareclass. Its nonzero integer norm is a
polynomial-size determinant. Therefore

    0<=v_P(alpha)<=ceil(log2|Norm(alpha)|)+1

at EVERY finite prime ideal. This is a polynomial NUMERICAL valuation bound
for these atoms, independent of geometric bounds for local Jacobian points.
No factorization of the atom norm is needed for this upper bound.

The native order and maximal product order satisfy

    disc f=[product O_Ki : Z[x]/f]^2 product Delta_Ki.

Consequently all native-to-integral and CRT denominator exponents are
bounded by v_p(disc f). Local maximal-order components can be obtained by
finite-algebra decomposition modulo p and unit-derivative idempotent
lifting. This uses the same theta, not an abstract local-field isomorphism
oracle. Uniformizers and residue bases are finite local arithmetic data.

Odd-prime squareclasses use valuation parity and residue quadratic character;
Euler powering has a polynomial-bit exponent. Dyadic frames can use the
triangular principal-unit presentation through U_(2e+1), since that final
subgroup consists of squares. The presentation has 2[E:Q2] generators and
is exact by its diagonal-2 determinant and the filtration order. Removing
the residue part by the odd exponent 2^f-1 preserves the squareclass.

After normalization, residue precision (odd p), or a constant number of
rational 2-adic digits (dyadic), suffices for the unit class. Atomic
valuations and discriminant conversion losses give the polynomial precision
guard stated in the report. Real signs of atoms also have polynomial
separation bounds from their exact heights and nonzero norms.

Fix one frame at each p. Translate the returned local-image frame generators
into it, or evaluate atoms in the returned frame using its native maps.
Arbitrary unaligned uniformizers, nonsquares, component labels or dyadic
relation bases cannot be compared as binary vectors. This is why efficient
frame interoperability belongs explicitly to the local premise above.

## 6. The real image and omitted finite places

If the real roots are r_1<...<r_R, then R=2k+1. The positive bounded
intervals of the monic odd-degree polynomial are (r_(2j-1),r_(2j)). A real
point in the jth interval has Kummer sign vector

    w_j=e_(2j)+...+e_R.

These k vectors are independent and span the adjacent-pair vectors
`e_2+e_3, e_4+e_5, ..., e_(R-1)+e_R`.

They generate the entire real image. The rational infinity point removes
the real divisor-class obstruction, and supports can be moved off the
branch divisor. A nonreal conjugate pair contributes |x-r_a|^2>0 at
every real root. A real point contributes one of the listed vectors or
zero from the unbounded positive interval. Thus dim(image at infinity)=k.
Real-root isolation and O(g) interval choices are polynomial; no real
component enumeration is needed.

The retained Stoll Proposition 4.2 identifies the genuine Selmer group
with norm-kernel classes satisfying all local images. Corollary 4.7 allows
an even smaller prime set than P0. Outside P0, the curve has good odd
reduction and L_p is unramified; even component valuations and square norm
are exactly the unramified local image. Hence (3) and the norm condition
already impose those places. Every p in P0, including discriminant-valuation-
one primes and small bad primes, is covered by the conditional local call.

## 7. Final matrix and probability ledger

Let m be the total dimension of the initial product T-unit squareclass
basis. Its embedding into L^*/L^*2 is injective. Let V be the valuation
matrix, N the rational norm matrix, R_v the common-frame localization maps,
and A_v a binary matrix whose kernel is the COMPLETE local image. Then

    dim Sel^(2) = m - rank [ V ; N ; A_infty R_infty ;
                                      (A_p R_p)_(p in P0) ].

The number of fields, primes, atoms, columns and rows is polynomial.
There is no class-group, residue-field, Jacobian or compact-exponent
enumeration. Polynomial-size explicit inputs to quantum arithmetic are
charged as circuit input; the local routines need not be coherent oracles.

Completeness of the unit group is a probabilistic event. Use Theorem 5's
explicit logarithmic dependence on its failure parameter THROUGH the full
unit algorithm and exact recovery, allocating O(1/n) error per field.
Allocate O(1/|P0|) per local call and charge the other randomized arithmetic
separately. Verified Las Vegas steps can use constant-factor time caps and
logarithmically many independent retries. No 1/eta-time cutoff is needed.

A full run then succeeds with a fixed probability above one half. Repeat
complete runs independently O(log(1/eta)) times and majority-vote only the
final INTEGER DIMENSION, treating aborts separately. Do not majority-vote
unit bases or coordinate vectors in potentially different frames. Direct
logarithmic failure allocation is an equivalent option. Valid units alone
are not being used to certify a complete basis.

The first unresolved NONCONDITIONAL input remains the uniform complete
local-image routine at every prime in P0. The global upper bound does not
turn full-unit computation into a necessary task for every possible
classical dimension algorithm. Stoll's retained Lemma 4.10 is an upper
bound, not such an equivalence. The report's limited classical comparator
and its explicit no-advantage/no-hardness boundary are the appropriate ones.
