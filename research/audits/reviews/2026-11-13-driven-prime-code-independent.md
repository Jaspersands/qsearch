# 2026-11-13 — Independent prime code and global-control gate audit

**The prime supply, uniform mode-triple isolation, and encoded gate algebra
close for every n.** There is an explicit deterministic polynomial construction
of the code using only primes in one dyadic interval. The (1,pq) alias is absent.
The entangler is an exact two-level pi cycle, not a commutator approximation.
The isolated generators are obtainable to any inverse-polynomial error by
polynomially many actual signed S,N pulses, with polynomial total duration.

This is the narrow code/control result. It does not invoke controllability,
arbitrary addressed gates, postselection, or a general binary-time Schur
fast-forwarding interface. It does not assert novelty or a practical protocol.
The parent owns the final BQP reduction and complete end-to-end error ledger.
The construction below is suitable for that reduction's polynomial-duration
subfamily; arbitrary binary-time driven evolution is not being admitted here.

Read STATE, the candidate note and its actual MM Eq. 2.1 excerpt. The retained
Rosser--Schoenfeld1962 Corollary 3, Eq. 3.8 (LF 231–258), independently supplies
a stronger dyadic prime bound. The elementary proof below avoids relying on
its OCR threshold or any additional prime-distribution premise. No live paid
reports, network, API, Git, implementation, or finite controls were used.

## 1. An elementary uniform supply of primes in (R,2R]

Let theta(x)=sum_(p<=x) log p, with natural logarithms. First

    theta(x)<=x log 4.                                      (1)

For completeness, write P(m)=product_(p<=m)p. Induction gives P(m)<4^m.
For m=2h, primes in (h,2h] divide binom(2h,h)<4^h. For m=2h+1, primes in
(h+1,2h+1] divide binom(2h+1,h)<4^h; the latter bound follows because its
two equal central terms have sum strictly less than 2^(2h+1). Multiply by
the induction bound for P(h), respectively P(h+1). The cases m<=2 are direct.
Taking m=floor(x) proves (1).

For integer R, the central binomial coefficient satisfies

    binom(2R,R)>=4^R/(2R+1).

For p<=sqrt(2R), its p-power contribution to this binomial is at most 2R:
each term floor(2R/p^j)-2floor(R/p^j) is 0 or 1. For p>sqrt(2R) the
exponent is at most one. The interval (2R/3,R] contributes no such prime,
and the remaining primes below R have product at most exp(theta(2R/3)).
Consequently

    theta(2R)-theta(R)
      >=(2R/3)log 2-sqrt(2R)log(2R)-log(2R+1).               (2)

For R>=R0=2^20, the last two terms in magnitude sum to less than R/16.
Indeed their ratio to R is decreasing there; at R0 it is bounded by
(2^11*21+22)/2^20<1/16, using log 2<1. Since log 2>1/2, (2) gives

    theta(2R)-theta(R)>R/4,
    pi(2R)-pi(R)>R/[4 log(2R)].                             (3)

Monotonicity used here is elementary: log(2R)/sqrt(R) is decreasing when
log(2R)>2, and log(2R+1)/R is decreasing because
log x>1-1/x for x>1. Thus (3) holds for ALL integer R>=2^20, not just a
checked finite range. No PNT, prime-gap conjecture, or oracle is used.

## 2. Deterministic polynomial Sidon primes and the cutoff

For n>=1 put m=2n and choose

    R=2^20(m+1)^4.

Since log(2R)<21+4m<=25(m+1), (3) supplies more than
2^20(m+1)^3/100>(m+1)^3 primes in (R,2R]. List them by a deterministic
sieve up to 2R. Its numerical range is O(n^4), so its BIT time and storage
are polynomial in n; no factoring or primality advice is supplied.

Greedily choose m DISTINCT primes, maintaining unique unordered two-sums
INCLUDING repeated pairs. If k primes have been chosen, a new x can fail
only by

    x=a,
    x+a=b+c,
    2x=b+c,                                                 (4)

with old a,b,c and unordered old pairs b,c. Equality between x+a and x+b
forces a=b; equality 2x=x+a is already x=a. Thus at most

    k + k^2(k+1)/2 + k(k+1)/2
       = k+k(k+1)^2/2 < (k+1)^3

candidate values are forbidden. For k<m, the prime supply exceeds this
bound. Exact integer pair-sum tests therefore find the next prime by a
deterministic polynomial search. This proves the whole greedy construction,
not merely existence of a sparse set with uncharged discovery cost.

Label the selected primes p_1,q_1,...,p_n,q_n and set

    c_i=p_i+q_i,  D=sum_i c_i.

All primes are odd, all sum modes are even, and the Sidon property makes
all local sums c_i and all distinct cross sums p_i+p_j mutually distinct.
In particular no cross sum is a local code mode or a prime mode. Moreover

    D<=4nR=O(n^5),  R>4n,
    pq>R^2>4nR>=D                                           (5)

for ANY two selected primes. Therefore the factor pair (1,pq) has sum
1+pq>D and does not occur in S. Every desired local sum is <=D; every
desired cross sum for i!=j is also <=D, because its two prime summands
are among the positive summands defining D. The n=1 case needs no entangler.

The initial all-zero code is the explicit occupation partition
mu=(c_1,...,c_n), sorted if desired. It has no unprepared ancilla population.

## 3. Exact Fourier isolation addresses a triple, not a hidden edge oracle

For distinct p,q put C_pq=a_p^dagger a_q^dagger a_(p+q), and
h_pq=2sqrt(pq(p+q)). The factor 2 is mandatory: actual S sums ordered
(p,q) and (q,p). The diagonal i=j terms have no such factor, but none can
share the product of two distinct primes.

The occupation-independent commutator is

    [N,C_ij]=-2ij C_ij.

Choose M=2D^2+1, theta_l=2pi*l/M, and
S_l=exp(i theta_l N) S exp(-i theta_l N). All these kicks have permitted
signed rational times in units of 2pi. For f=2pq, exact discrete orthogonality
gives

    F_X=(2/M)sum_(l=0)^(M-1) cos(2pi*f*l/M) S_l
         =h_pq(C_pq+C_pq^dagger),
    F_Y=(2/M)sum_(l=0)^(M-1) sin(2pi*f*l/M) S_l
         =h_pq*i(C_pq^dagger-C_pq).                          (6)

For any term of S, 0<2ij<=D^2/2. Differences and sums of the relevant
signed frequencies are therefore smaller than M, so no modular alias occurs.
The only positive integer factor pairs of pq are (p,q) and (1,pq).
Equation (5) removes the second, and reversed ordering supplies precisely
h_pq. Thus (6) holds on the ENTIRE degree-D sector, for every spectator
occupation; it is not just a matrix element at one selected Fock state.

The real cosine and sine combinations are essential: a complex Fourier
coefficient isolating C alone is not a Hermitian control. Define
X_pq=F_X/h_pq and Y_pq=F_Y/h_pq. Their coefficients are explicitly computable,
the sum of absolute coefficients is <=2/h_pq<=2. An entirely direct bound is
||S||<=D^(7/2): each weighted creation term has norm <=D^(3/2), its adjoint
has the same norm, and there are at most D^2/2 ordered pairs. For distinct
i,j, its squared matrix element is the product of i(n_i+1), j(n_j+1),
and (i+j)n_(i+j), each <=D on a nonzero input. For i=j the corresponding
factors are i(n_i+1), i(n_i+2), and 2i*n_(2i), also each <=D.
Each fixed creation map is an injective weighted shift, so this maximum
matrix element bounds its operator norm. No Schur-spectrum bound is needed.
There is
no unknown normalization or exponentially small mode-dependent coupling.

Equation (6) is an identity of generators, NOT a claim that one finite
averaging cycle exactly exponentiates their sum. Actual pulse synthesis is
paid in Section 5 below; no weighted Hamiltonian is granted for free.

## 4. Exact local gates and an exact-cycle CZ

For qubit i use the two occupation states on (p_i,q_i,c_i)

    |0_i>=|0,0,1>,   |1_i>=|1,1,0>.

All local triples are disjoint. Both states have momentum c_i. On this
two-dimensional space, C_i=|1_i><0_i|, so X_i=C_i+C_i^dagger is Pauli X.
With the convention in (6), Y_i=i(C_i^dagger-C_i) is MINUS standard Pauli Y;
the permitted sign of the pulse time corrects this harmless convention.
The charges n_(p_i)+n_(c_i)=n_(q_i)+n_(c_i)=1 make the local two-level
space exactly invariant. Matrix elements are one, not boson-number factors
that vary with the other qubits. X and Y rotations give every local SU(2)
gate, and the usual fixed universal gate set needs only a constant number
of such rotations per one-qubit gate, up to an irrelevant overall phase.

For i!=j put r=p_i+p_j and C=a_(p_i)^dagger a_(p_j)^dagger a_r.
Sidon distinctness ensures r is empty on EVERY code word. If the logical
bits are 00,01 or 10, both C and C^dagger annihilate the state: r is empty
and the two prime modes are not both occupied. For 11 the only connected
states, with all other occupations fixed, are

    |1_(p_i),1_(p_j),0_r>  <-->  |0_(p_i),0_(p_j),1_r>.

The amplitude of C+C^dagger on this block is exactly one. The conserved
charges n_(p_i)+n_r=n_(p_j)+n_r=1 rule out a second pump quantum or higher
occupation states. Spectators q_i,q_j and all remaining qubits are unchanged.
It follows EXACTLY that

    exp(-i*pi*X_(p_i,p_j)) |_code = CZ_(i,j),                (7)

and r returns to vacuum. No commutator simulation is needed. Sequential
entanglers begin with their ancillas empty; distinct cross sums also avoid
accidental identification with another entangler's or qubit's mode.

Therefore local SU(2) and (7) give an explicit gate algebra on n qubits.
This is not an inference from the size of a dynamical Lie algebra. The
occupation decoder checks each triple for the two code patterns and checks
other modes empty. Any invalid outcome receives a specified default output;
it is never rejected or postselected. Ideal gates have zero bad-code mass.

## 5. The isolation has a uniform polynomial native-pulse clock

Here is a sufficient bound establishing that (6) is an actual two-control
construction; optimizing it is unnecessary. Let B=(D+1)^4>=||S||, and write a chosen
normalized X or Y as sum_l gamma_l S_l, with sum_l |gamma_l|<=2. For a gate
angle |u|<=pi, first-order unitary product formulas give

    ||exp(-iu sum_l gamma_l S_l)
         - (product_l exp(-i(u/r)gamma_l S_l))^r||
       <=u^2 (sum_l ||gamma_l S_l||)^2/(2r)
       <=2pi^2 B^2/r.                                      (8)

This bound follows from the pairwise commutator estimate and unitary Duhamel
integrals; there is no exp(B) loss. For G intended primitive rotations/CZ
cycles, r=ceil(64 B^2 G/epsilon) gives less than epsilon/(2G) error per
gate. Each exponential in (8) is exactly the conjugated native word

    exp(i theta_l N) exp(-i(u/r)gamma_l S) exp(-i theta_l N).

These are operator products, with the rightmost pulse applied first: the
chronological native times are N(+theta_l), S((u/r)gamma_l), N(-theta_l).
No optional adjacent-kick merge is used.

Thus there are at most 3GMr native pulses. The N times are exact rational
multiples of 2pi. The S times can be rounded to signed rational multiples
of 2pi: compute f*l modulo M before evaluating sine/cosine, and use the
explicit positive square root h_pq. Bounded-argument elementary evaluation
gives absolute time error <=epsilon/[12GMr(B+1)] with polynomial bit cost.
The total extra operator error is then <=epsilon/12. No relative precision
at a nearly zero cosine or sine is requested. The detailed parent budget
may allocate smaller tolerances without changing polynomiality.

This pulse word has POLYNOMIAL TOTAL ABSOLUTE DURATION as well as polynomial
length. Ideal S durations sum to at most 2pi G; rounding adds a bounded
amount. N durations sum to at most 4pi GMr. Each pulse descriptor uses
O(log D+log G+log(1/epsilon)) bits with the displayed choices. Since D=O(n^5),
all construction, pulse-count, duration and bit costs are polynomial in
n,G,1/epsilon. Signed times are an essential part of the stated access model.

Consequently this reduction needs only ordinary polynomial-duration sparse
simulation of S and diagonal simulation of N for its quantum upper bound.
S has O(D^2) explicitly computable row neighbors and polynomial-bit square-root
weights in occupation coordinates. No unreviewed Schur-transform interface,
arbitrary binary-time fast forwarding, or exponentially deep BCH construction
is needed. Approximate pulse errors are bounded on the full degree sector, so
leakage during compilation is carried by unitary norm bounds and the final
decoder, not silently reset at logical gate boundaries.

The addressed three-wave encoding and pi-cycle interaction are not asserted
new. The material result here is their explicit polynomial extraction from
the TWO globally specified S,N controls with a native polynomial-size code.
Any final complexity consequence must retain this exact pulse/input contract
and the separately checked overall error and sampling reduction.
