# Structured EDCP: Upstream Mixing, Exact Carries, And A Forward Repair

Date: 2026-09-25
Status: LOCAL DERIVATION / REVIEW PENDING. This is a scoped replacement argument
for the forward source construction, not independent peer review, a novelty
claim, a production implementation, or an algorithm solving lattice problems.

## 1. Outcome And Scope

The preceding joint-source note starts with an integer instance whose matrix
is nearly uniform and whose error has a small coefficient lift. This note
examines how Wen--Zheng Lemma 28 proposes to obtain that instance from
short-secret, coefficient-Gaussian P-MLWE.

Three parts need correction or qualification:

1. Surjectivity over a product ring does not imply an invertible row minor.
2. The stated dimension-independent carry bound in Lemma 46 has an exact
   counterexample, even with coefficient secret bound one.
3. The matrix-uniformity argument must retain the bad-original-matrix term
   and the number of amplified rows. It is not uniformly exponentially small
   in ring degree for every allowed splitting pattern.

None of these observations alone refutes the forward reduction. A replacement
uses disjoint potential anchor minors in the PROOF, a finite regularity bound
from the primary LPR argument, and an elementary exact carry identity. It also
uses the actual power-of-two canonical embedding to control Gaussian mixing
noise. Combining the resulting contract with the preceding finite-grid source
gives a conditional forward reduction for the specified P-MLWE family.

The scope is NOT the whole paper: the reverse reduction and its use of Lemma
46 are not repaired here. Neither a worst-case lattice hardness theorem for
the exact numerical parameters nor an efficient EDCP decoder is supplied.

## 2. Distributions And Widths Must Be Explicit

Let R=Z[X]/(X^d+1), with d a power of two, q an odd prime, and R_q=R/qR.
Use m>=n>=1 original rows and module-secret coordinates, respectively,
M>=1 amplified rows, and Q=q^d+1. For polynomial-time/asymptotic claims,
m and M are polynomially bounded in d. Sample independently

    A uniform in R_q^(m by n),
    s_raw with nd integer coefficients from D_(Z,r_s),
    e with md integer coefficients from D_(Z,r_e),
    b=A*s_raw+e mod qR.

Here D_(Z,r)(z) is proportional to exp(-pi*z^2/r^2), a PROBABILITY-width
convention. Let s be the centered coefficient representative of s_raw mod q.
The eventual phase amplitude width sigma is a different parameter.

Take W in R^(M by m) with independent entries from the canonical-embedding
Gaussian D_(R,r_mix). The full complex embedding satisfies V^*V=d*I, so

    ||V*v||_2^2=d*||v||_2^2,
    W coefficient law = independent D_(Z,tau), tau=r_mix/sqrt(d).  (1)

The algorithm computes A'=W*A mod q and b'=W*b mod q, both centered, then
evaluates their polynomials at q modulo Q. It never needs s, e, or a carry
witness to perform these operations.

This does NOT create ordinary independent LWE error samples. The amplified
errors share the original error vector and are correlated with the new matrix.
Only a JOINT matrix-uniformity bound and an unconditional error-smallness
bound are required by the next stage. They must not be strengthened silently.

## 3. A Counterexample To The Minor Step, And Its Repair

In F_5[X]/(X^2+1), take the two-row, one-column matrix with entries

    u=3+4X,       v=3+X.

They satisfy u+v=1, u^2=u, v^2=v and u*v=0. The matrix is surjective as a
map R_q^2 -> R_q but neither entry is a unit. There is no invertible one-row
minor. This directly falsifies the general inference in Corollary 6's proof.

For our RANDOM input matrix, a different argument is enough. Partition the
first n*floor(m/n) rows into t=floor(m/n) disjoint n-by-n blocks. If q has
residue fields of orders N_j=q^(f_j), the failure probability of ONE block is

    p_badminor = 1 - product_j product_(r=1)^n (1-N_j^(-r))
               <= min(1,n*d/q).                                (2)

The blocks are independent. The probability that none is invertible is at
most p_badminor^t. For a fixed block I, conditioned only on that block's
invertibility and value, right multiplication by A_I^(-1) makes its rows an
identity, while all remaining normalized rows are independent uniform.

This matches the LPR regularity ensemble. Permuting rows of A only permutes
i.i.d. entries of W; right multiplication of the OUTPUT by a unit matrix
preserves uniformity. No nonorthogonal transformation of a Gaussian vector
is being assumed distribution-preserving.

Do not condition on a data-dependent chosen first invertible minor and then
assert that every other row stayed uniform. Instead sum over the FIXED
disjoint blocks as in section 4. The construction need not search for a minor
at all; this is a proof device for the unchanged multiplication W*A.

For constant n, m=Theta(log d), and q>=d^(1+c) for fixed c>0,
p_badminor^t is negligible in d. It need not be exp(-Omega(d)). LPR itself
points out the common-prime-factor obstruction when there is no fixed unit
column. In the completely split, n=1 case, a fixed CRT component of all m
original rows is zero with probability q^(-m). On that event all M amplified
rows vanish in that component, giving joint-distance lower bound

    q^(-m)*(1-q^(-M)).                                          (3)

For polynomial q and logarithmic m this is larger than exp(-c*d) for every
fixed c>0 asymptotically. Retaining this term is essential, not cosmetic.

The primary LPR theorem also resolves a notation mismatch in the 2026 paper:
its polynomial size bound is in the RING DEGREE d, not the constant module
rank n. Its parameters (degree n, rank k, length ell) correspond here to
(d,n,m). The allowed m<=poly(d) includes our logarithmic sample count.

## 4. An Explicit Joint Regularity Certificate

For an identity-normalized n-by-m map F=[I|F_bar] over R_q, let Lambda be its
kernel in the canonically embedded R^m. Write

    X(F)=rho_(1/r_mix)(Lambda^*)-1 >= 0.

Poisson summation gives the mass of every output coset. If
Y=rho_(1/r_mix)((R^m)^*)-1, then 0<=Y<=X(F), and every output probability p_z
satisfies

    q^(nd)*p_z = (1+eta_z)/(1+Y),       |eta_z|<=X(F).

It follows directly that TV(law(W_row*F^T),uniform)<=X(F). No Markov square
root or uncharged conditioning is needed when we only want average distance.

The following explicit bound is extracted from LPR Corollary 7.2 and equation
(7.2), keeping constants instead of replacing them with Omega notation. Define

    a0=(1+2^(-2d))^m,
    beta=(a0-1)*(1+q^(-(m-n)))^d
          + a0*(d/r_mix)^(d*m)*q^(d*n)*(1+q^(-n))^d.             (4)

Then E_(F_bar) X(F)<=beta. To see this, let J range between q*R^* and R^*,
and let N_J=|J/qR^*|. LPR's ideal sum bounds E X by

    sum_J N_J^(-(m-n)) * [rho_(1/r_mix)((1/q)*J)^m-1].

The ideal Gaussian bound is at most

    rho_(1/r_mix)((1/q)*J)^m
      <= a0*max(1,(N_J*d^d*r_mix^(-d))^m),

using the power-of-two cyclotomic discriminant d^d. Since q is unramified,
the ideal divisors are subsets of its distinct prime factors, so

    sum_J N_J^(-(m-n)) <= (1+q^(-(m-n)))^d,
    sum_J N_J^n <= q^(dn)*(1+q^(-n))^d.

Using max(1,x)-1<=x proves (4). These bounds require no factorization of qR.
The value beta can be large at small widths; report a vacuous bound honestly.
For r_mix>2*d*q^(n/m+2/(d*m)), it is exponentially small in d when m is
polynomially bounded, as in the primary theorem. The formula itself retains
the finite parameters and does not use that asymptotic simplification.

Let f(A) be one-row TV distance for fixed original A. On any invertible fixed
block I, the above average bound applies. For M rows, conditional independence
of the ROWS OF W gives TV<=M*f(A). Splitting off the no-anchor event and
summing over the fixed blocks proves the full joint statement

    TV(law(A,W*A), law(A,U)) <= delta_amp,
    delta_amp=min(1,p_badminor^t + M*t*beta),                     (5)

where U is independent uniform in R_q^(M by n). This argument never asserts
conditional independence of amplified errors. Approximate Gaussian sampling
adds the actual joint sampling TV error to (5).

Finally, evaluating an independent uniform coefficient matrix gives uniform
entries on a subset of Z_Q of size q^d=Q-1. Thus its EXACT distance from
uniform over Z_Q^(M by n) is

    delta_eval = 1-(1-1/Q)^(M*n) <= M*n/Q.                       (6)

The final integer matrix is within delta_amp+delta_eval of uniform.
It is independent of s EXACTLY, because W and A are independent of the
original secret. This also supplies a joint matrix/secret guarantee, not
merely a marginal statement with an uncontrolled secret posterior.

The guarantee does NOT reveal W as extra independent side information.
Conditioned on A and W, W*A is deterministic. A claim of independence from
both A AND the revealed mixing coins would have distance 1-q^(-d*M*n).
The solver may ignore/discard those coins. Any attack using additional retained
side information must state that access model explicitly.

## 5. The Carry Bound Counterexample And A Simpler Exact Identity

The following is an exact counterexample to the stated Lemma 46 bound, even
when all differences are reduced to centered coefficients modulo q.
Let d>=64 be a power of two, q>d an odd prime, n=1, and put

    h=(q-1)/2,  U(X)=1+X+...+X^(d-1),
    a(X)=h*U(X),     s(X)=U(X),     b=0,     phase index i=0.

The polynomial secret has infinity norm B=1. Since d is even, U(q) is even,
and a(q)=Q/2-1. Hence a(q)*s(q)=-U(q) mod Q and Phi of that product is
the all-minus-one coefficient vector. The j-th coefficient of the integer
negacyclic product a*s is h*(2*j+2-d). Their centered difference modulo q is

    c_j = j-d/2,       j=0,...,d-1,
    ||c||_infty = d/2.                                         (7)

The lemma's displayed bound, using its EF(X^d+1)<=2, is at most 26.5 when
n=B=1. Already d=64 gives 32>26.5; d=128 gives 64>26.5. Rotating to phase
index one preserves this norm, so index-set conventions do not rescue it.
Under unreduced integer subtraction the norm is larger, not smaller.
The proof's use of n*B in a polynomial coefficient one-norm estimate cannot
replace the missing dependence on polynomial degree d.

This does NOT by itself disprove Lemma 28's aggregate error bound: its much
larger mixing bound may have slack. It does invalidate importing the stated
carry lemma uncritically, including in the separately unaudited reverse path.

For the forward construction, dispense with Phi carries entirely. Let
u=W*e in R^M before reduction modulo q. For every row form the INTEGER
negacyclic polynomial

    p_i=sum_j A'_ij*s_j+u_i,
    b'_i=p_i-q*k_i,       k_i coefficientwise nearest quotient by q.

Evaluation E_q:R -> Z_Q is a ring homomorphism, and multiplication by q in
Z_Q equals evaluation after multiplying by X. Therefore the exact error lift
of the public integer instance is

    v_i = u_i-X*k_i mod (X^d+1),
    E_q(b'_i) = sum_j E_q(A'_ij)*E_q(s_j)+E_q(v_i) mod Q.          (8)

Let S=sum_j ||s_j||_1 and suppose ||u||_infty<=U0. Since A' has centered
coefficients bounded by h,

    ||k_i||_infty <= floor((h*S+U0+h)/q) = K0,
    ||v_i||_infty <= U0+K0 = B_out.                             (9)

Multiplication by X only rotates/sign-flips the coefficient vector. This
proof includes all carries, even if u wraps many times modulo q. There is
no assumption that centered evaluation on R_q is a ring homomorphism.

The final secret is defined consistently as E_q(s), with s centered modulo q.
Its distribution is EXACTLY the intended evaluated modular Gaussian prior.
Evaluation on centered coefficients is injective, so recovering that integer
secret recovers the P-MLWE secret modulo q. No approximate secret-prior claim
or negligible-wrap assumption is needed for this correspondence.

## 6. Bounding The Actual Mixed Error Without Independence Fiction

Write theta(r)=sum_(z in Z) exp(-pi*z^2/r^2). A scalar D_(Z,r) has

    E exp(t*Z) <= exp(r^2*t^2/(4*pi)),
    E exp(lambda*Z^2) <= (1-lambda*r^2/pi)^(-1/2)
       for 0<lambda<pi/r^2.                                   (10)

The first inequality follows by completing the square and maximizing a shifted
theta sum at an integer center. The second follows from Poisson summation:
theta(r')/theta(r)<=r'/r for r'>r. These are exact discrete inequalities,
not a continuous-noise replacement.

Set c0=(pi-log 2)/2. For N independent coefficient Gaussians of width r,

    Pr[||Z||_2^2 > r^2*N] <= exp(-c0*N).                        (11)

Use lambda=pi/(2*r^2) in (10). Thus except on probabilities
delta_e=exp(-c0*m*d) and delta_s=exp(-c0*n*d), respectively,

    sum_j ||e_j||_2^2 <= r_e^2*m*d,
    S <= r_s*n*d.                                              (12)

The second uses Cauchy--Schwarz and the fact that coefficient centering modulo
q cannot increase absolute values or the Euclidean norm.

Condition on the ORIGINAL error e satisfying (12), NOT on the new matrix.
Every coefficient of W*e is a linear combination of independent width-tau
Gaussians, with squared coefficient norm exactly sum_j ||e_j||_2^2.
Consequently, for every amplified coefficient,

    Pr[|u_ij|>U0 | e] <= 2*exp(-pi*U0^2/(r_e^2*r_mix^2*m)).     (13)

All output coefficients may be dependent. A union bound, not independence,
shows that for any delta_mix>0 it suffices to take

    U0 >= r_e*r_mix*sqrt((m/pi)*log(2*M*d/delta_mix)).             (14)

Combine (9), (12) and (14). With failure at most
delta_err=delta_e+delta_s+delta_mix, the integer source has ACTUAL lifts
bounded by B_out. The finite-grid phase source can use these lifts directly;
it need not infer their existence from Phi. The lift is a proof witness,
not information handed to the algorithm.

A simple exact-integer certificate for delta_mix=exp(-d), with integer upper
bounds on r_e and r_mix, is

    T=d+ceil(log2(2*M*d)),
    3*U0^2 >= r_e^2*r_mix^2*m*T,   U0 a positive integer.         (15)

This is conservative because pi>3 and ceil(log2 N)>=log N. It avoids an
uncertified ceiling of a floating-point square root/logarithm. Use integer
square roots, and S0=ceil(r_s*n*d), in the scalable certificate.

There really IS dependence to preserve: for two scalar mixed errors
Z1=W1*e and Z2=W2*e with independent nondegenerate zero-mean Gaussians,

    Cov(Z1^2,Z2^2)=Var(e^2)*E(W1^2)*E(W2^2)>0.

Ordinary independent-error LWE tools cannot be applied to this source without
a separate distributional argument. Our subsequent grid proof only needs
the small-error event and matrix separation, so this dependence is permitted.

## 7. Composition With The Quantum Stage

Feed the evaluated (A',b') into the construction in
`research/STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md`, using coefficient support
radius R_phase and

    E0=d*R_phase*B_out*(q^d-1)/(q-1),
    a=ceil(Q^(n/M)),       C_grid=12*a,
    p0=(1-24*a*E0/Q)^(M*L).

The condition 48*a*M*L*E0<=Q certifies p0>=1/2. On good instances, the
phase output has an unheralded ideal-product component with this weight.
The downstream random-code separation failure delta_sep is charged using
the matrix TV certificate, not by assuming the evaluated matrix is exact
uniform or independent of its error.

For ideal decoder success P, finite preparation error gamma per block and
one-block Gaussian coefficient tail eta, a conservative total success bound is

    p0*P - (delta_amp+delta_eval+delta_err+delta_sep)
          - p0*sqrt(L*eta) - L*gamma - delta_sampling.            (16)

The evaluated secret-prior discrepancy is zero under the definition above.
delta_sampling is the total approximation error for the CLASSICAL discrete
Gaussian draws; it is not to be double-counted inside delta_amp as well.
The public residual verifier applies to the evaluated integer (A',b'), with
E_orig=B_out*(q^d-1)/(q-1). It does not require revealing W or the hidden lifts.

This is a conditional LOCAL forward-reduction argument using the primary LPR
ideal Gaussian inequality. It is not a formal proof artifact or a compiled
quantum circuit. It establishes neither a decoder nor the precise worst-case
hardness/security of the chosen input family.

## 8. Parameter Consequences And Finite Certificates

In the earlier regime q between d^12 and 2*d^12, n,L constant,
m=ceil(log d), M=ceil(d*log q), r_e=r_s=sqrt(d), and
r_mix just above 2*d*q^((n*d+2)/(d*m)), one has

    r_mix=Theta_n(d),
    U0=O_n(d^2*sqrt(log d)),
    K0=O_n(d^(3/2)),
    B_out=O_n(d^2*sqrt(log d)).

With amplitude sigma=sqrt(d) and R_phase=d, the grid-condition ratio is
O_n(L*d^5*(log d)^(3/2)/q), improving the previous conservative
O_n(L*d^7*(log d)^2/q). This is a real improvement to the source contract,
but not a quantum speedup. Widening sigma must also trigger stronger classical
decoding checks; a cleaner/wider source is not automatically more quantum.

The following analytic reference uses n=1,L=288,q=nextprime(d^12), and

    r_mix=2*d*(floor((q^(d+2))^(1/(d*m)))+1).

This enforces the primary theorem's STRICT width inequality. q values were
obtained with SymPy, not independently certified prime. Formula (15), the
carry ceiling, a=3, and the grid inequality were checked using integers.
Reported probabilities use 100-digit arithmetic, with log1p/expm1 to retain
tiny Gaussian-mass terms; they are not interval-certified decimal enclosures.

| d | M | U0 | B_out | Grid Ratio | Clean Weight Lower Bound |
|---:|---:|---:|---:|---:|---:|
| 64 | 3195 | 355689417 | 355689673 | 0.04087873 | 0.9797681 |
| 256 | 17035 | 13854650858 | 13854652906 | 8.09642e-6 | 0.999995952 |
| 1024 | 85174 | 480919408113 | 480919424497 | 1.34009e-9 | 0.999999999330 |

All three pass the one-half margin certificate with the NEW error budget.
The old-budget failures in the preceding note remain correct for that budget;
they are not experimental failures that this calculation has overwritten.

| d | log10 delta_amp Upper Bound | log10 delta_err Upper Bound |
|---:|---:|---:|
| 64 | -33.6294 | -27.7948 |
| 256 | -148.3397 | -111.1794 |
| 1024 | -231.7931 | -444.7175 |

The worst-case anchor bound dominates delta_amp at d=1024. Do not substitute
an exp(-Omega(d)) label for it. The evaluation TV logarithms are approximately
-1383.64, -7393.88 and -36985.64; sampling/circuit errors are still separate.
These large-dimensional values are formula evaluations, not executions of
the source or a decoder, and not classical-security estimates.

## 9. Checks Actually Run And Red Team

No production wiring or full-suite run occurred. The following bounded
mathematical checks used temporary interpreter sessions and seed 20260925.

1. Exhausted the 25 ring elements and all 625 pairs in the surjective/no-unit
   minor control. Both rows were nonunits; their image was the full ring.
2. Exact carry-bound controls at (q,d)=(257,32),(257,64),(521,128) gave norms
   16,32,64. The latter two violate the 26.5 bound. Equation (7) gives an
   all-size family, not only those numerical examples.
3. 1,800 random EXACT integer-polynomial/module cases covered q in
   {3,5,7,17,53}, d in {2,4,8}, n in {1,2,3}. Mixed errors were allowed to
   exceed q. Every case passed (8), the carry ceiling and the lift bound.
   Another 360 full classical transformations formed the ORIGINAL (A,b),
   multiplied both by W, centered A',b', and checked 1,620 amplified-row
   identities plus 540 evaluated-secret round trips. Original secrets and
   errors were allowed to wrap modulo q. These are algebra checks for arbitrary
   small W, not tests that such W has the stipulated Gaussian distribution.
   Four additional carry controls checked both phase indices zero and one.
4. Six Fourier embedding matrices, d=2..64 through powers of two, satisfied
   V^*V=d*I numerically, with maximum absolute roundoff 2.96e-13.
5. 656 identity-normalized matrices across 16 Gaussian-width ensembles checked
   TV<=X and E X<=beta. Rings were (q,d)=(3,2),(5,2),(7,2),(3,4), m=2,n=1,
   coefficient widths tau in {0.5,1,2,4}. Wrapped one-dimensional Gaussian
   reference sums were cut at ceil(10*max(1,tau)); no exact infinite-sum
   equality is inferred from this floating-point reference.
6. Eleven full joint-amplification cases exhausted 22,507 original matrices
   (counting repeats at different widths), explicitly forming conditional
   TWO-row distributions. All respected (5). Small-width bounds were vacuous.
   At q=3,d=4,tau=8, actual joint TV was 0.02423785 versus bound 0.15875381;
   at tau=16 the same limiting TV was below 0.14306801. It does not go to
   zero merely by making the Gaussian wider: bad original matrices remain.
7. Fifty-four finite Gaussian MGF/norm checks and 18 conditional mixed-error
   MGF checks passed. A shared-error reference at width 1.3 gave positive
   squared-error covariance 0.0112506, rejecting an unconditional independent-
   amplified-error model.
8. The three growing-parameter reports checked the integer root, the strict
   mixing-width choice, the integer tail ceiling and the grid certificate.

One reference initially asserted that a small-width bound would be nonvacuous;
it was not. The mathematical inequality still held. The check was corrected
to report its bound as one rather than discard the case or call it a success.

Remaining ways this could fail: an error in the LPR ideal-sum specialization,
mis-scaled canonical Gaussian, unsupported input secret/error distribution,
finite-sampling errors larger than the budget, or misuse of side information
in a decoder comparison. The ideal-sum specialization and end-to-end success
composition need independent mathematical review. No empirical check above
certifies a growing-size quantum algorithm.

## 10. Handoff And Next Research Decision

GEMINI, after reviewing the derivation:

- Add `theorems/structured_edcp_upstream_mixing.py`, with exact negacyclic
  carry lifts, the finite beta/delta_amp certificate, exact evaluation TV,
  canonical/coefficient width conversion and the integer Gaussian-error budget.
- Integrate with the joint-source contract, preserving ORIGINAL rows m,
  amplified rows M, module rank n, ring degree d and phase blocks L separately.
  Do not reduce these to a single sample-count or scalar confidence score.
- Preserve bad-minor probability, regularity mass, amplified-row hybrid loss,
  coefficient tails, evaluated-prior identity, Gaussian sampling error and
  quantum preparation error as separately inspectable obligations.
- Store the exact Lemma 46 counterexample and the surjective/no-unit-minor
  counterexample as literature-linked corrections. Do not label the entire
  paper refuted. The FORWARD repair does not validate its reverse reduction.
- Reproduce the checks above, including a vacuous-width case, a shared-error
  dependence control and a revealed-mixing-coins access-model control.
- Generate live artifacts only through the normal proof-gated registry path.
  No candidate or speedup promotion follows from source repair alone.

MAIN MODEL: the previous missing forward link now has a concrete scoped
derivation to review, rather than an unexamined citation. Next attack the
substantive decoding bottleneck using the REAL source: either a new conditional
multi-block operation, or an efficient source-specific lattice basis method.
First test whether the improved allowable phase widths and retained integer
instance make the prior-aware classical baseline tractable. Keep the reverse
equivalence and worst-case-hardness implications explicitly unaudited.

## Sources

- Wen and Zheng, *Module Learning With Errors and Structured Extrapolated
  Dihedral Cosets*, [ePrint 2026/155](https://eprint.iacr.org/2026/155.pdf).
  Version downloaded 2026-09-24; inspected Lemma 28, Lemma 46 and its proof,
  and supplementary D.1-D.3. Formula pages 39,66,67,79,80 were rendered.
  This is a version-specific audit, not a statement about later revisions.
- Lyubashevsky, Peikert and Regev, *A Toolkit for Ring-LWE Cryptography*,
  [author-hosted full version, 2013-05-16](https://sites.cc.gatech.edu/fac/cpeikert/pubs/toolkit.pdf).
  Inspected section 7, Corollary 7.2, Theorem 7.4, Corollary 7.5 and equation
  (7.2), including the explicit discussion of the common-factor obstruction.
  The Gaussian regularity machinery is prior work, not a new discovery here.
