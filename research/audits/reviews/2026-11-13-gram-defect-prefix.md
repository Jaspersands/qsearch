# 2026-11-13 Positive Gram peeling and arbitrary-Gram prefix DP

## Disposition and native scope

Both proposed mathematical operations are valid for the stated native input:
an explicit rational-complex m-by-N isometry U, one photon in each of N
DISTINCT input modes, and a rational-complex Hermitian PSD Gram G with diagonal
one describing a PRODUCT of pure internal states. All output collisions are
allowed. The positive private-flag mixture is exact, and the shared-subset
prefix DP has at most binom(2s,s)<=4^s states, not factorial complexity.

Exact rational arithmetic and finite-bit CDF coins give a worst-branch
TV-epsilon sampler in exp(O(R))*poly(B,N,m,1/epsilon), where
R=N(1-d) and 0<=d<=lambda_min(G) is the certified rational peel. Here B is
the dense input bit length, including d if supplied. There is no unbounded
random-bit/rejection loop or inverse-prefix-probability runtime.

This proof does not assert novelty, priority over the retained simulation
literature, quantum advantage, or implementation. Pairwise G alone does not
specify general mixed/correlated internal inputs. Repeated input modes and
loss/postselection are not silently included. STATE/TRAPS and the assigned
selection were read; no network/API/Git, archive, or numerical experiment was used.

## 1. Positive private sectors, including all coherent terms

Put H=G-dI, rho=1-d. Since H>=0, choose abstract vectors h_i with Gram H,
and mutually orthonormal private vectors p_i orthogonal to their whole span.
The vectors

    phi_i=sqrt(d)*p_i+h_i

have exactly Gram G and norm one. They need not be computed. If rho>0 write
eta_i=h_i/sqrt(rho); their Gram is Gamma=H/rho, with diagonal one.

Before the interferometer the one-particle spatial/internal vectors
|i> tensor |phi_i> are orthonormal because the input modes i are distinct.
Their normalized bosonic first-quantized state is the symmetrized sum with
coefficient 1/sqrt(N!), irrespective of the internal overlaps. Expanding
each phi_i in its private/shared components gives one term per subset S of
shared photons. Each normalized term has coefficient

    rho^(|S|/2)*d^((N-|S|)/2).

The terms lie in orthogonal sectors specified by every TOTAL private
occupation: private mode p_i has occupation zero if i belongs to S and one
otherwise. These number projectors commute with spatial U and with every
spatial occupation measurement. Consequently deleting coherences between
these sectors changes NONE of the desired output probabilities, and their
exact weights are

    Pr(S)=rho^|S| * d^(N-|S|).                                    (1)

Thus shared membership is independent Bernoulli(rho). No binomial or
symmetrization factorial multiplies an individual subset weight.

Within a sector, the orthogonal internal decomposition into the shared space
and the one-dimensional private spaces factorizes the bosonic Fock space.
The branch input and the spatial evolution factor across these species.
Each private species contains one photon, producing an independent categorical
output with probabilities |U_(y,i)|^2. The shared species contains the s=|S|
photons with Gram Gamma_(S,S). Its histogram is independent of the private
histograms, and the observed histogram is their sum. Orthogonality of the
private species proves this independence; arbitrarily measuring different
shared internal colors would not be justified and would destroy interference.

Equivalently the first-quantized expansion below depends only on the Gram,
so this abstract realization gives the original law for ANY realization of G.
If rho=0, PSD and zero diagonal force H=0: G=I and every photon is private.
If d=0 every photon is shared. Empty shared subsets require no DP.

## 2. Exact first-quantized prefix normalization

Relabel the selected shared inputs 1,...,s and let Gamma_ki=<eta_k|eta_i>.
For an ordered string y=(y_1,...,y_s), the spatial measurement probability is

    p_s(y)=1/s! * sum_(pi,tau in S_s)
       product_(j=1..s) U_(y_j,pi(j))*conj(U_(y_j,tau(j)))
                        *Gamma_(tau(j),pi(j)).                    (2)

No permanent of Gamma divides the input normalization: distinct spatial
input modes make the original one-particle vectors orthonormal.

Sum over the unobserved outputs j>r. Isometry gives
sum_y U_(y,i)conj(U_(y,k))=delta_ik, forcing pi(j)=tau(j) there, and
Gamma_ii=1. Hence the r observed ket and bra inputs use the SAME subset A;
the common complementary ordered assignment has exactly (s-r)! choices.
For c_y(i,k)=U_(y,i)conj(U_(y,k))*Gamma_ki, define D_r(A,B) as the
coefficient of x_A z_B in

    product_(j=1..r) sum_(i,k=1..s) c_(y_j)(i,k)*x_i*z_k,
    x_A=product_(i in A)x_i, z_B=product_(k in B)z_k.

Then, exactly,

    p_r(y_1,...,y_r)=(s-r)!/s! * sum_(|A|=r) D_r(A,A).              (3)

For fixed A the diagonal coefficient is r! times a legitimate r-photon
ordered output probability, so it is nonnegative and real. Off-diagonal
D_r(A,B) need NOT be real or nonnegative. Complex phases must be retained.

Repeated OUTPUT labels y_j cause no restriction in this calculation. The
distinctness constraints concern only input indices in A and B. The law
(2) is permutation-invariant in its output slots. An occupation vector with
counts n_y has probability s!/product_y n_y! times any ordered-string
probability with those counts. Sampling the ordered string and counting it
therefore supplies all collision factorials automatically.

## 3. The 4^s subset-pair recurrence

Initialize D_0(empty,empty)=1. For |A|=|B|=r,

    D_r(A,B)=sum_(i in A,k in B)
                c_(y_r)(i,k)*D_(r-1)(A\{i},B\{k}).                (4)

Only squarefree states are needed: once a variable repeats, multiplication
cannot turn it into a squarefree target. Across all r the number of states is
sum_r binom(s,r)^2=binom(2s,s)<=4^s. To evaluate every possible next output,
apply (4) to the stored actual-prefix table for each y in [m], compute (3),
and retain/recompute only the selected next table. This costs
O(m*s^2*4^s) arithmetic operations across the full s-step sample, with
O(4^s+poly(m,s)) storage. There is no enumeration over m^s output strings.

Normalization can also be verified directly: sum_y c_y(i,k)=delta_ik, so
summing (4) over y and diagonal A counts each previous diagonal state
s-r+1 times. Together with (3), this proves

    sum_y p_r(prefix,y)=p_(r-1)(prefix),       p_0=1.                (5)

## 4. Exact common denominators and tiny prefixes

Take common positive integer denominators U=A/Q_U and Gamma=C/Q_Gamma,
with A,C Gaussian-integer matrices. Products/lcms of the input denominators
give log Q_U,log Q_Gamma=poly(B,N). More explicitly, if G=C0/Q_G and
d=a/b<1, the full Gamma has denominator Q_G*(b-a) and numerator
b*C0-a*Q_G*I; small rho introduces only its encoded bit length.

Set Q=Q_U^2*Q_Gamma. Every c_y(i,k) is a Gaussian integer divided by Q.
Its absolute value is at most one: U is an isometry and Gamma is a unit-
diagonal PSD Gram. For fixed A,B, D_r has (r!)^2 expanded terms, hence
|D_r(A,B)|<=(r!)^2. Store the scaled table

    E_r(A,B)=Q^r D_r(A,B) in Z[i].

Recurrence (4) uses Gaussian-integer multiplication/addition only. Its bit
lengths are O(r log Q+r log(r+1)); even before cancellations the same bound
controls partial sums. Define the nonnegative INTEGER

    P_r=(s-r)! * sum_(|A|=r) E_r(A,A).

The imaginary part vanishes exactly, and

    p_r=P_r/(s!*Q^r),
    Pr(next=y|prefix)=P_r(y)/(Q*P_(r-1)).                           (6)

All these integers have polynomial bit length in s,B,N; (5) says their
conditional numerators sum exactly to Q*P_(r-1). A positive prefix has
p_(r-1)>=1/(s!*Q^(r-1)). Its possibly tiny value costs only polynomial bits,
not probability-dependent repetitions or approximate cancellation tests.

For any categorical distribution computed this way, form its exact rational
cumulatives F_j and thresholds floor(2^b_rng F_j). Draw one uniform b_rng-bit
integer and use the resulting half-open integer intervals. Total variation
from the exact conditional is at most m*2^-b_rng. A zero-probability outcome
has identical consecutive thresholds, so it is NEVER chosen. Starting from
p_0=1, the sampler thus never divides by an exact zero prefix. Truncation of
tiny positive conditional probabilities is charged by this uniform TV bound.

## 5. Finite mixture cap and total BIT clock

For 0<epsilon<=1 let b_eps=ceil(log2(2/epsilon)) and

    K=min(N,ceil(8R)+2b_eps),          R=N*rho.

For exact Bernoulli flags, E[2^|S|]=(1+rho)^N<=exp(R). If K<N, Markov gives
Pr(|S|>K)<=exp(R)*2^-K<=epsilon^2/4<=epsilon/4. If K=N the tail is zero.
On the capped tail output a fixed LEGAL N-photon histogram; this changes the
distribution by at most that tail probability and gives a finite clock.

Use b_rng=ceil(log2(8N(m+1)/epsilon)) bits for each flag and categorical draw.
Round Bernoulli inclusion rho downward, and use the exact-CDF thresholds
above for shared/private spatial draws. Flag-law TV changes by at most
N*2^-b_rng; conditional spatial sampling by at most N*m*2^-b_rng. Coupling
sequential conditionals and then applying the histogram map bounds the total
additional TV by epsilon/8. Together with the tail this is below epsilon.
All branches return a legal histogram; there is no hidden Monte Carlo
estimation failure or unbounded exact-coin loop.

The worst arithmetic count is O(m*K^2*4^K+poly(N,m)), and every operation
has polynomial bit cost by section 4. Since 4^K=exp(O(R))*poly(1/epsilon),
the advertised finite BIT bound follows, including input reading and output.
The scalar d can itself be chosen by O(log N) dyadic bisection tests of
G-dI>=0 on [0,1], using exact rational Hermitian Schur complements; take
the lower feasible endpoint within 1/N of lambda_min. If G=I take d=1.
This needs no eigenvector, gap, factoring, or internal-state realization.
It gives N*(1-lambda_min(G))<=R<=N*(1-lambda_min(G))+1.

TV error is not an algorithmic failure probability: the fallback above is
part of the approximate output law. If instead one demands an explicitly
flagged tail ABORT of probability eta, changing the cap to O(R+log(1/eta))
generally adds a power of 1/eta to the worst-branch clock. A polylog(1/eta)
bound for that different convention is not inferred. The all-legal-output
TV sampler here has no internal failure event on promised inputs.

## 6. Exact phase-sensitive falsifier for an invalid simplification

Replacing complex Gamma by entry magnitudes is false already for three
photons. Let U=I-2vv^T/9, v=(1,2,2). Its first row is (7,-4,-4)/9.
Take two Gram matrices with diagonal one and off-diagonal magnitudes 1/8,
whose triangle products have phases zero and pi/2. Both are PSD by strict
diagonal dominance. For all three photons exiting mode 1, (2) gives

    probability=perm(G)*product_i |U_(1,i)|^2,
    perm(G)=1+3/64+2*(1/8)^3*cos(triangle phase).

The two probabilities differ by exactly 49/531441. Both the positive
mixture and (4) retain this term. This analytical counterexample rejects
magnitude-only/private-shared dephasing shortcuts; it does not contradict
the proved sector measurement or require a numerical control.
