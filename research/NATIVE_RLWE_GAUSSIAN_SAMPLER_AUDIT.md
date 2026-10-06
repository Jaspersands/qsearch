# Native Two-Block Gaussian Sampling: Structure And Failed Implementations

Date: 2026-09-29. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to `NATIVE_RLWE_COVARIANT_DECODER_TARGET.md`. No novelty, general
lattice-sampling lower bound, efficient sampler, or quantum advantage is
claimed. This pass tests actual ways of implementing that note's missing
coherent Gaussian preimage operation. Routine implementation is for Gemini.

FOLLOW-UP (2026-10-04): NATIVE_RLWE_COHERENT_READOUT_AUDIT supplies a
classical transcript sampler for a concrete Bell/resource/QFT attempt at
the inverse. Its Wigner analysis also prevents an overly broad Gaussian-
input Clifford dequantization claim. Neither result closes all coherent
sampler constructions.

TARGET RELAXATION (2026-10-04): NATIVE_RLWE_CHOSEN_PREIMAGE_REDUCTION
requires only measured short preimages at chosen syndromes for a different
correlation decoder. Neither clean erasure nor exact Gaussianity is needed
when an adequate norm/moment certificate holds. Existing native-walk and
rejection failures still matter, but coherence is no longer an entry
requirement for that alternative target.

FINITE CLASSICAL FOLLOW-UP (2026-10-04):
`NATIVE_RLWE_CLASSICAL_COVER_CERTIFICATE.md` gives a saved native d64
all-coset Babai certificate passing both d^12 decoder lanes. Finite point
finding can use a full-rank nonsaturated sublattice; the sampling index
requirement below is not necessary for that endpoint. See
`NATIVE_RLWE_BALANCED_NTRU_TARGET.md` for exact classical controlled-index
completion and native-row norm-gcd false negatives. No asymptotic attack.

## 1. The Lattice Is Already In A Known Structured Class

Condition on a_1 being a unit and charge that event. Multiplying the OUTPUT
equation by C_(a_1)^(-T) does not change the coefficient metric. With

    m=a_2*a_1^(-1) in R_q, M=C_m^T,
    F(x,y)=x+M*y mod q,
    K={ (x,y) in Z^(2*d): x+M*y=0 mod q },
    B=[ qI -M ], det B=q^d,                                 (1)
      [  0  I ]

choose the centered integer coefficient lift of m. Conditional on a_1,
m is uniform in R_q, even if a_2 is not a unit. This is a public module
lattice of NTRU form, NOT a generated NTRU secret/trapdoor distribution.
The ideal phase secret in these normalized output coordinates is C_(a_1)*s;
invert C_(a_1) after decoding. A small-secret prior is pushed forward, not
unchanged. The L2 covariant decoder does not require a small-prior assumption.

There is an exact, inexpensive duality. Let P implement the coefficient
involution f(X)->f(X^(-1)): P*e_0=e_0 and P*e_j=-e_(d-j) for j>0.
Then P=P^T=P^(-1), P*M*P=M^T. For

    U=[ 0  P ], U^T*U=I, U^2=-I,
      [-P  0 ]

direct block multiplication gives

    B^T*U*B=q*U,
    U*B=q*B^(-T)*U,
    U*K=q*K^*.                                              (2)

Thus K/sqrt(q) is isodual with a symplectic isometry. The general connection
between NTRU-form lattices, isoduality and symplectic reduction is established
prior art: [Gama--Howgrave-Graham--Nguyen, Sections 2-3](https://www.iacr.org/archive/eurocrypt2006/40040234/40040234.pdf).
Equation (2) fixes our negacyclic, COLUMN-basis convention explicitly.

For rho_s(K)=sum_(x in K) exp(-pi*||x||^2/s^2), Poisson summation yields

    rho_s(K)=(s^2/q)^d*rho_(q/s)(K).                        (3)

The self-dual scale is sqrt(q). This identity relates partition functions;
it does not prepare a Gaussian, find short vectors, or implement a transform
between arbitrary shifted Gaussian states. The public signed permutation U
does not shorten a bad basis. An ordinary QFT on a finite linear code is
also not the same operation as preparing its nonuniform Gaussian weights.

## 2. The Native Klein Proposal Still Pays Exponential Rejection

Set s=sigma/sqrt(2), the PROBABILITY width. In the column order (1), the
Gram--Schmidt lengths are EXACTLY d copies of q followed by d copies of 1.
For a frequency coset K+t_u write

    Z_u=rho_s(K+t_u), Z_all=Theta(s)^(2*d), r(u)=Z_u/Z_all,
    C_B=Theta(s/q)^d*Theta(s)^d,
    H_B=q^d*C_B/Z_all=[q*Theta(s/q)/Theta(s)]^d.              (4)

The ideal universal-envelope correction of the sequential Klein proposal
has acceptance Z_u/C_B. This is an EXACT statement about that specific
proposal/filter. On the all-frequency event |q^d*r(u)-1|<=eta<1,

    acceptance <=(1+eta)/H_B,
    T_proxy=sqrt(C_B/Z_u)
       >=[q/(1+s)]^(d/2)/sqrt(1+eta),                        (5)

using Theta(s/q)>=1 and Theta(s)<=1+s. Standard amplification of this
accepted branch has the corresponding inverse-square-root scale. This is
not a lower bound for a different proposal or arbitrary state preparation.

At the three L2 reference rows from COVARIANT_DECODER_TARGET and eta=.01,
the base-2 logarithms of the lower bound in (5) are respectively

    d=64: 367.9849715; d=256: 1983.9908325; d=1024: 9983.9923243.

These are analytic repetition proxies, not executed circuits. Extra gates,
basis construction, tails and coherent normalization do not disappear.

### A Recent Quantum-Sampling Paper Does Not Remove This Cost

[Ling--Yan--Zhao, Theorem 5 and Definition 9](https://arxiv.org/pdf/2605.24798)
give quantum rejection from a COHERENT TRUNCATED Klein proposal oracle.
Their acceptance parameter is p_R=Delta_R/Q(X_R); the query count omits
implementation of that supplied oracle. This is useful conditional machinery,
not a polynomial-cost oracle for arbitrary public module lattices.

In particular, do not mistake their O(1/sqrt(Delta_R)) upper bound for a
lower bound. Equation (5) follows instead from OUR specified full-proposal
filter's exact acceptance. If conditioning on X_R makes p_R much larger,
charge preparation of that conditioned proposal. An independently efficient
implementation of it would itself be substantive new progress.

A supplied better basis changes the calculation. Recompute its WHOLE
Gram--Schmidt profile and charge construction. The matched reversed-dual
Babai/list-decoders in STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT and
STRUCTURED_EDCP_PROFILE_LIST_DECODER must then be compared using the native
matrix and modulus, not the old scalar source.

For example, q*K^* modulo q is the image of the stacked native label matrix.
Reversed-dual Babai with GS lengths g_i has ideal discrete-Gaussian Fourier
noise failure bound 2*sum_i exp(-pi*(s/g_i)^2). The proof is the same
discrete MGF/nearest-plane argument, with q in place of scalar Q and the
secret recovered using a_1^(-1) from the first output block. Charge the
native readout's own alias/source errors. A good basis may be valuable,
but using it quantumly is not automatically a superpolynomial advantage.

## 3. At The Physical Cutoff, Native-Basis Local Walks Can Be Frozen

Consider a walk on (K+t_u) intersect [-R_c,R_c]^(2*d), proposing only
single steps plus or minus a column of (1), and rejecting steps outside
the box. Suppose

    2*R_c<q and ||m||_infinity>2*R_c.                        (6)

Every q*e_i step exits the first-block interval. Every other basis column
is (-M*e_j,e_j); its first block contains a signed permutation of all
coefficients of m, including one with absolute value above 2*R_c. That
step also exits the box from EVERY possible starting point. Hence the
transition matrix is the identity on each nonempty fiber, including fibers
with many points. This is an exact disconnectedness result, not slow mixing
in a numerical experiment.

For uniform centered m, if 4*R_c+1<q the exception probability is exactly

    Pr[||m||_infinity<=2*R_c]=[(4*R_c+1)/q]^d.               (7)

At R_c=sigma*sqrt(d) in the three L2 rows, log10 of this exception is
-115.595484, -693.573098 and -3699.056585. These probabilities concern
the specified NATURAL label distribution, conditional on the first unit.

This rules out implementing the target by that local walk, including a
quantization whose only position transitions are those same disconnected
edges. It does NOT rule out reduced-basis moves, nonlocal combinations,
different encodings or more general coherent operations. A small control
below explicitly restores edges with a reduced basis.

## 4. Removing The Cutoff Does Not Make Those Moves Mix Well

There is also an obstruction for the corresponding infinite-coset lazy
Metropolis chain with a fixed symmetric proposal distribution over the
same signed basis columns. This avoids blaming finite truncation alone.
Let pi_u(x)=exp(-pi*||x||^2/s^2)/Z_u on K+t_u.

Assume ||m||_2>=q. Every proposed vector v then has norm at least q.
For ||x||<=q/4,

    ||x+v||^2-||x||^2 >=||v||^2-(q/2)*||v|| >=q^2/2.

Thus the probability of making ANY move from such x is at most

    epsilon_move=exp(-pi*q^2/(2*s^2)).                      (8)

The uniform label failure probability has the elementary lattice-point bound

    Pr[||m||_2<q]
       <=pi^(d/2)*(1+sqrt(d)/(2*q))^d/Gamma(d/2+1).           (9)

Proof: disjoint unit cubes centered at the relevant coefficient vectors lie
inside a ball of radius q+sqrt(d)/2. Divide that volume by q^d. At the
three reference rows the logarithms of (9) are about -19.51,-151.95,-912.00.

This is not merely a rare-state or rare-coset bottleneck. On the same
all-frequency event as (5), Poisson summation and shifted-Gaussian maximality
give, for EVERY coset,

    max_x pi_u(x) <=q^d/[(1-eta)*s^(2*d)],
    E_(pi_u) exp(pi*||x||^2/(2*s^2))
        =rho_(sqrt(2)*s)(K+t_u)/rho_s(K+t_u)
        <=2^d*(1+eta)/(1-eta),
    Pr_(pi_u)[||x||>q/4]
        <=2^d*(1+eta)/(1-eta)*exp(-pi*q^2/(32*s^2)).         (10)

For the middle inequality, a shifted Gaussian sum is at most the unshifted
one; Poisson gives rho_(sqrt(2)*s)(K)<=2^d*rho_s(K); and relative flatness
compares the unshifted and shifted width-s normalizers. There is no hidden
covariance oracle or continuous replacement of the discrete target.

At all three reference rows with eta=.01, the atom bound is below 1/6 and
the outside-ball bound below 1/3. Greedily select a set S inside the ball
with pi_u(S) between 1/3 and 1/2. Its stationary exit flow is at most
pi_u(S)*epsilon_move. The variational bound for the indicator of S yields

    spectral_gap <=epsilon_move/(1-pi_u(S))
                 <=2*exp(-pi*q^2/(2*s^2)).                 (11)

The argument is uniform in u on good labels. Conditional on a_1 being a
unit, the probability of a label exception is bounded by
B_2/(eta*p_U) plus (9), using the prior note's exact CRT certificate.
No independence between those two exceptional events is assumed.

The resulting classical relaxation time is exponential. A claimed polynomial
quantum-walk preparation cannot cite a polynomial gap for this chain; the
usual square-root gap dependence does not fix an exponentially small gap.
This is NOT a lower bound on every quantum sampler, every annealing schedule,
or every algorithm with a warm start. A method that avoids the offending
eigenspaces or supplies different moves needs its own actual analysis.

## 5. A Lattice Fourier Transform Is Not A Missing Decoder For Free

[Eldar--Shor, Theorem 4 and its sampling algorithm](https://arxiv.org/pdf/1703.02515)
require Fourier concentration within a radius of order
lambda_1(K^*)/2^(n/2), n the ambient lattice dimension, and use nearest-plane
decoding in the construction. Here n=2*d. An amplitude-width-sigma Gaussian
has characteristic Fourier radius of order sqrt(n)/sigma, whereas
Minkowski's bound gives lambda_1(K^*)<=sqrt(n/q). Thus the stated generic
guarantee calls for widths on an exponential 2^d*sqrt(q) scale, not our
sigma=O(sqrt(q)). This is an applicability check, not a criticism of the
paper's theorem or a lower bound for specialized lattice transforms.

Nor is our quotient Z^(2*d)/K, isomorphic to (Z_q)^d, already a single
cyclic-index SysNF quotient under a unimodular integer change of basis.
Approximate lattice replacement requires its metric/coset/error analysis;
an easily implemented finite-group QFT alone does not do that replacement.

## 6. What Remains Worth Trying

The target should now be specific enough to reject superficial proposals:

- Search for quantum constructions of useful short module relations/bases
  from the NATURAL public m, with explicit resource bounds. If the output
  is classical, immediately run the matched classical decoder on it.
- Explore nonlocal coherent moves or a parent-Hamiltonian construction that
  does not use the frozen basis graph. Exhibit its transition support,
  initialization, stationary state, relevant gaps and relative phases.
- An annealing proposal must account for every reflection/preparation cost.
  Repeatedly calling the previous stage's full preparation can multiply
  costs; constant overlap of adjacent states is not a runtime proof.
- Exploit the actual isodual rank-two module, if possible, while preserving
  its discrete cosets and metric. Replacing it by an easy continuous
  Gaussian or a supplied short-trapdoor ensemble changes the problem.
- Keep the separate noncovariant one-record prior-aware track alive. These
  local-move and proposal bounds do not close it or all two-block decoders.

Gemini: implement exact basis/involution/cutoff checks and log-domain
certificate fields before running a sampler. Reject a claimed mixing result
if (6) makes its graph disconnected. Store the actual proposal support,
cutoff, basis, profile, all normalization/oracle costs and label event.
Do not create a speedup candidate from a small spectral gap, an oracle-model
query count, or a dense tiny inverse. Scope every negative result to the
algorithm family that was actually tested.

## 7. Checks Actually Run

- Seed 290936: 72 exact integer/symbolic basis cases at d=2,4,8 and
  q=3,5,17,101 verified determinant, (2), signed orthogonality and native
  GS lengths. No floating determinant was used for those identities.
- Twenty-four complete finite-box controls at (q,R_c,d)=(17,2,2),
  (23,3,2),(11,1,4), eight natural-label draws satisfying (6) each.
  Every signed native-basis step was forbidden. There were 10,264
  multi-point fibers across these cases; isolatedness is not vacuous.
- Twenty-seven centered theta-duality comparisons at d=2, q=3,5,7,
  s/sqrt(q)=.75,1,1.4 and integer cutoff 18. Maximum relative discrepancy
  8.80e-16. These truncated numerical controls do not replace Poisson's proof.
- Seed 290937: 16,128 move-energy inequalities for d=16,32,64,
  q=31,101,1009, random labels with ||m||>=q, and starting points of norm
  at most q/4. Every increment met the lower bound preceding (8).
- 332 all-frequency controls and 1,328 conditional-tail controls at d=2,
  q=3,5,7, s=sqrt(2*q), coordinate cutoff ceil(5*s). These check the
  algebra of (10), not physical source parameters at those tiny q.
- A necessary scope control: d=2,q=17,m=(6,7),R_c=2 had zero positive
  native-basis edges but 328 after exact integer LLL basis reduction.
- Three growing parameter rows checked support, atom/tail premises and
  the log-domain references at 80-digit precision. Large numbers are
  analytic bounds, not large-d simulations or timing measurements.

No routine CLI/UI/registry wiring, full repository test suite, large attack
sweep, commit, or proof-status promotion was performed.
