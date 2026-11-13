# Homogeneous open folded-chain quench: full classical composition

13 November 2026. Independent proof audit of the native map, selection, and
finite-bit obligation. Read actual Bravyi quant-ph/0404180v2, including its
Majoranas (physical LF92), covariance/Wick formula (249–254), vacuum convention
(273–300), Gaussian closure (402–414), and measurement discussion (871–914).
No API, network, Git, tests, archives, live paid reports, or status edits used.

**Finding.** The proposed sampler closes at the stated WRITTEN native scope.
Its covariance sign and prefix-Pfaffian prefactor are correct. The proof below
pays polynomial BIT time, exact zeros, tiny prefixes, and capped randomness;
an arithmetic-operation Gaussian simulation statement alone would not do so.
The optional coherent amplitude also has a polynomial-bit formula, provided
the common input phase is supplied in rational turns. Pairing z=1 is simplest
for that separate computation. No classical hardness, novelty, implementation,
practicality, arbitrary-input, inhomogeneous-input, or perturbed-model claim.

## 1. Native input and exact sector reduction

Use exactly the N+2-spin open Hamiltonian and bond/word bijection in
FOLDED_CHAIN_COHERENT_TRANSFORM.md, N>=2. Input is numerical N, binary rational
time t, rational p in [0,1], and rational 0<epsilon<=1/4. The physical initial
state is (sqrt(1-p)|0>+exp(i*phi)sqrt(p)|1>)^(tensor N+2). The full output
Born law is independent of the common phi; it need not be supplied to sample.

For a label lambda=(s0,w,d_terminal,m), the encoded occupations are ALL
weight-m strings of length ell. Their nearest-neighbor exclusion graph is
connected (move particles successively to any desired ordered positions).
Every corresponding physical move exchanges 01 and 10 and preserves physical
magnetization. Therefore its value M_phys is constant in this whole block,
and every initial physical amplitude in the block equals the SAME number

    c_lambda=(1-p)^((N+2-M_phys)/2)*p^(M_phys/2)*exp(i*M_phys*phi).

The conditional input is exactly the uniform Dicke vector D_(ell,m).
Sampling a physical IID Bernoulli(p) word and encoding it samples the label
with its exact weight binom(ell,m)*|c_lambda|^2. Discard the sampled effective
positions; do NOT evolve that basis input instead of D_(ell,m).
Measuring/dephasing labels is legitimate for this task because the native
evolution and final computational-basis measurement are block diagonal in
these disjoint basis spans. No cross-block interference is discarded by the
classical sampler. This does not justify dephasing for other observables.

For m=0 or m=ell, the unique effective occupation is stationary and can be
decoded directly. Otherwise 1<=m<=ell-1. The native block Hamiltonian is
the number-preserving fermion lift of the path matrix with off-diagonal -1/2;
its exact one-body evolution is

    U=S diag(exp(i*t*cos(pi*j/(ell+1)))) S^T,
    S_rj=sqrt(2/(ell+1))*sin(pi*r*j/(ell+1)).

Use the exterior-power lift Gamma(U) with vacuum amplitude ONE. No scalar
phase from a different fermionic/spin lift may be silently substituted.

## 2. A known Gaussian with a polynomial-probability projection

Adjoin one spectator LAST, so the total number of modes is d=ell+1. Let J be
skew with J_ij=1 for i<j, and z=m/(ell-m)>0. Use the unnormalized state

    G_Z=exp((1/2)*sum_ij Z_ij a_i^dagger a_j^dagger)|vac>, Z=zJ.

For every even principal subset I, Pf(J_I)=1: expansion in the first row is
the alternating sum of an odd number of ones. Induction starts with the empty
Pfaffian 1. Thus the amplitude on every even occupation set I is z^(|I|/2).
Its squared norm is W=((1+z)^d+(1-z)^d)/2. The normalized occupation law is
IID Bernoulli(q), q=z/(1+z)=m/ell, conditioned on even total parity.

Project the physical count onto m and the spectator onto s=m mod 2. Because
the spectator is last in the ordered Fock basis, no subset-dependent sign
appears: the physical conditional vector is exactly D_(ell,m). Its success is

    sigma=Pr[Bin(ell,q)=m]*q^s*(1-q)^(1-s)/Pr[even total parity]
         >=1/[ell*(ell+1)].                                      (1)

Indeed m is a binomial mode at q=m/ell, so its probability is >=1/(ell+1),
and both q and 1-q are >=1/ell. The even-parity denominator is <=1 and nonzero.
Evolve by T=diag(U,1). Both projectors commute with Gamma(T), so (1) is
unchanged and the accepted physical state is Gamma(U)D_(ell,m). This is
ordinary charged classical rejection, not free postselection or an incoherent
mixture of effective basis states.

## 3. Exact algebraic unitary approximation at binary time

Let h=4(ell+1), F=Q(zeta_h), D=[F:Q]<=h. Compute its cyclotomic polynomial
and power-basis arithmetic in polynomial(N) time; h is numerical O(N), and
even trial division of h is polynomial here. This is computed field data.
The normalization square root in S cancels in U. In fact

    U'_rs=2/(ell+1)*sum_j sin(pi*r*j/(ell+1))*sin(pi*s*j/(ell+1))*d_j

lies in F when each d_j is an exact rational point on the unit circle in Q(i).
Choose d_j within delta_U of its true time phase. A bounded stereographic
chart among the centers 1,-1,i,-i, followed by dyadic approximation of its
parameter, produces such d_j EXACTLY on the circle with polynomial bits.
Choosing a chart from a coarse approximation has fixed overlap margins;
no exact comparison with a transcendental chart boundary is required.

Computing energies to O(delta_U/max(1,|t|)) and reducing the resulting phase
uses O(bitlength(t)+log N+log(1/delta_U)) working bits, plus ordinary input
bits. No loop of length |t| occurs. S is real orthogonal, hence U' is EXACTLY
unitary, and ||U'-U||<=delta_U. Exterior powers obey

    ||Gamma_m(U')-Gamma_m(U)||<=m*delta_U.                         (2)

This follows by telescoping the m-fold tensor product and restricting to its
antisymmetric subspace. Since projection commutes with BOTH lifts, its success
bound does not amplify (2). Label weights form a probability distribution, so
the conditional-state error is bounded uniformly, not multiplied by the number
of labels. The pairing used by the proposal becomes Z'=diag(U',1)Z diag(U'^T,1).

## 4. Covariance and prefix Pfaffian: the exact signs

Use Bravyi's Majoranas x=a+a^dagger, y=i(a-a^dagger), initially GROUPED.
The operators a-Z'a^dagger annihilate G_(Z'). Their coefficient matrix is

    A=(I-Z', -i*(I+Z'))/2,
    AA^T=0,  G=AA^dagger=(I+Z'Z'^dagger)/2 >=I/2.

Put P=A^dagger G^(-1)A. P is a rank-d orthogonal projector. Isotropy AA^T=0
implies P*conj(P)=0, so P+conj(P)=I. Normalizing the annihilators to satisfy
the canonical anticommutation relations gives <c c^T>=2P. Therefore

    M=-i*(I-2P)=i*(<c c^T>-I).                                  (3)

It is real skew and M^2=-I. Reorder it to INTERLEAVED x1,y1,x2,y2,... .
For Z'=0, (3) gives M_(2j-1,2j)=+1, exactly the source vacuum convention.
There is no sign repair to the parent's covariance formula.

For a prefix of k occupation bits let s_j=+1 for empty and -1 for occupied,
J2=[[0,1],[-1,0]], and D_s=directsum_j s_j J2. Its exact joint probability is

    P_s=2^(-k)*(product_j s_j)*Pf(M_prefix+D_s).                   (4)

To prove it, expand product_j (1+s_j*i*c_(2j-1)c_(2j))/2 and apply the
source Wick formula <i^q c_a1...c_a(2q)>=Pf(M_sub). In the Pfaffian of
M_prefix+D_s, selecting an adjacent D_s pair has positive deletion sign.
Its expansion is sum_I Pf(M_pairs(I))*product_(j notin I)s_j; multiplication
by product_all s_j gives exactly the projector expansion. This expansion is
a proof, not an algorithm enumerating 2^k terms. For k=1 it gives (1+s*M12)/2;
vacuum empty prefixes have probability 1 and occupied ones 0. No square root
of a determinant, inverse of a conditional covariance, or Pfaffian sign guess
enters (4). Gaussianity/Wick remain valid for singular reduced covariances.

## 5. Polynomial BIT heights and a uniform nonzero-prefix bound

Represent F in its cyclotomic power basis, conjugating by zeta_h -> zeta_h^-1.
Cyclotomic coefficients have magnitude <=2^D, since all their roots have
modulus one. Reduction of a product of two basis elements thus has polynomial
bit height, for example <=4h^2+O(1). The exact rational-circle d_j have
polynomial coordinate bits. A common denominator for U' is obtained from
2(ell+1) times their denominators, whose logarithm is O(ell times their bit
length). Consequently Z', A and G have polynomial coordinate bits.

Compute G^(-1)A by a rational linear system of dimension r=D*d, never by
iterating analytic inverses. If b bounds the rational matrix/RHS entry bits,
clearing all denominators uses <=3r^2*b bits. Hadamard/Cramer bounds each
solution coordinate by

    r*((3r^2+1)*b+log2(r+1))+O(1)

numerator/denominator bits. Exact fraction-free linear algebra pays this
clock; G is nonsingular by its physical lower bound. Forming (3) is then a
fixed number of polynomial-size matrix operations. In particular one can
compute an integer Q_M>=1 and B with log2 Q_M<=B such that every coordinate
of Q_M*M is integral of magnitude <=2^B, with B polynomial in native bits.
There is no height recurrence through a sequence of measurements.

All prefix matrices have the SAME bound. Set

    Q=(2Q_M)^d,
    C=(2d)^(2d)*[(D+1)*2^(B+1)]^d,  A_bound=Q*C.

For every prefix probability P_s, Q*P_s is an algebraic integer. At every
embedding of F its absolute value is <=A_bound: each Pfaffian has <=(2d)!
terms, degree <=d, and conjugates of its cleared entries are bounded by the
sum of their power-basis coefficient magnitudes. These term counts are used
only for a height estimate. If P_s is nonzero, its integral field norm gives

    |P_s| >= mu :=1/[Q*A_bound^(D-1)].                            (5)

The logarithm of 1/mu is an explicit polynomial bound. It is uniform over
ALL exponentially many possible prefixes without enumerating them. A prefix
probability is nonnegative by (4)'s physical derivation, so nonzero means
positive; an arbitrary algebraic sign oracle is not needed.

For a sign-safe polynomial Pfaffian algorithm on any 2k-square skew B0, compute
det(J0+tB0) by exact interpolation at t=0,...,2k, where Pf(J0)=1. Recover its
formal square root q(t), q0=1, by

    q_j=(D_j-sum_(i=1)^(j-1) q_i*q_(j-i))/2, j=1,...,k.

The identity det(J0+tB0)=Pf(J0+tB0)^2 proves q_k=Pf(B0), including zero.
No numerical root choice occurs. Intermediate coefficients have polynomial
height because they are coefficients of this degree-k Pfaffian polynomial;
determinants/interpolation also have the displayed polynomial minor bounds.
This is a polynomial number of field/rational operations with polynomial bits.

Exact zero testing means checking the rational power-basis coordinate vector.
At a positive prefix compute both child joint probabilities from (4). Force
the positive child if the other is zero. Otherwise approximate their ratio
to additive nu/(4d), and use a dyadic coin with an additional <=nu/(4d) error.
For example, evaluate each joint probability to nu*mu^2/(64d); (5) pays the
division and requires only polynomially many bits. Evaluation at the specified
root of unity uses elementary sine/cosine with coefficient-height guard bits.
Clipping the ratio to [0,1] cannot increase its error. Every reached prefix
has positive exact probability; define a bounded failure return for an
unreachable zero prefix as well. Coupling the d coin steps gives TV <=nu.
All bit coins have fixed length. No repeated precision search or tiny-prefix
postselection appears inside this Gaussian sampler.

## 6. Complete native clock and error allocation

Let d_max=N+2 and choose delta_U=epsilon/(64*d_max). Sample the initial
physical label using Bernoulli(p) coins rounded to error epsilon/(64*d_max)
per bit, handling p=0,1 exactly. This changes the label law by <=epsilon/64.
All later guarantees hold uniformly for every valid label, including tiny ones.

For a nontrivial label, form the exact algebraic U', Z', and M above. Put

    R=d_max^2*ceil(log2(64/epsilon)),  nu=epsilon/(64R).

Keep this originally sampled label FIXED through all R attempts; resampling it
after a failed projection would incorrectly reweight labels by their success.
In each attempt sample a fresh Gaussian occupation word to TV error nu,
and accept exactly when its physical count is m and its spectator equals
m mod 2. On success discard the spectator and decode with the sampled label.
On timeout output any fixed valid decoded weight-m word of that label.
The ideal attempt success is >=1/d_max^2, so timeout probability <=epsilon/64.
Coupling all approximate attempts costs <=R*nu=epsilon/64. Equation (2)
contributes <=epsilon/64 to the native conditional Born law. Together with
label rounding these errors are <epsilon; the generous margin also permits
fixed rational upper bounds when forming clocks and precisions.

The number of attempts is polynomial in N and log(1/epsilon), and all field
degrees, coordinates, precisions, time-phase computations, and Pfaffian calls
are polynomial in N, the input/time bits and log(1/epsilon). No numerical-time
loop, exponentially many labels, expanded Born table, or inverse-success
oracle is used. This proves the advertised full finite-BIT sampler.

## 7. Optional coherent physical amplitude: use pairing J without tilt

For this separate computation set z=1, T=diag(U',1), and Z'=T J T^T.
Given an output physical word y, compute its label and effective occupied
set S, and let I=S with the last spectator appended iff m is odd. Then

    psi'_y=c_lambda*Pf(Z'_I).                                   (6)

The Pfaffian minor-summation identity follows by applying the exterior power
of T to exp(sum_(i<j) J_ij e_i wedge e_j). Since Pf(J_A)=1 for every even A,
and T has an untouched LAST spectator, the minor is exactly

    Pf(Z'_I)=sum_(physical |A|=m) det(U'_(S,A)).

Only input sets with the same spectator bit contribute; their ordering gives
no extra sign. This is the amplitude obtained by evolving the unnormalized
uniform weight-m vector. It covers m=0 (empty Pfaffian 1) and m=ell, where
the answer is det(U'), whose phase MUST be retained. The true U has determinant
one because the path matrix has trace zero, but a generic U' need not.

To output a complex amplitude, phi/(2pi) must be charged rational input (or
an explicitly charged computable-phase interface). The Born sampler did not
need it. Compute |c_lambda| from the exact rational
p^M_phys*(1-p)^(N+2-M_phys), then its positive square root, and compute its
phase by rational-turn multiplication. The Pfaffian has modulus
<=sqrt(binom(ell,m))<=2^(ell/2), by the norm of a row of the exterior-power unitary.
Thus O(N) additional absolute-precision guard bits pay multiplication by an
approximated scalar. All field heights are as above, and an arbitrary requested
additive amplitude precision 2^-p_out costs polynomially in p_out as well.
Choose delta_U=O(2^-p_out/N): the full initial norm in any block is <=1, so
(2) bounds the amplitude approximation error without dividing by label weight.

The original tilted expression z^(-(m+s)/2)*Pf((T zJ T^T)_I) is also correct,
but unnecessary; z=1 removes that rational inverse factor. Neither formula
extends the uniform-within-block input premise. The precise physical scope
remains homogeneous product input, the stated OPEN folded Hamiltonian, and
the charged full computational-basis Born/amplitude outputs.
