# Bunched binary-Fock coherent-branch sampler: classical review

2026-11-07. CLOSED independent mathematical/BIT review of
BINARY_FOCK_KERR_SAMPLING.md Sections3,3a,3b, including their updated finite
clocks. Read current STATE/TRAPS, the prior core review, and the returned
binary-binomial report; checked its material algebra rather than relying on
its verdict. No controls, sampler implementation, network/API or Git actions.

**Accepted scope:** the written classical sampler runs in bounded time
polynomial in the native input length, numerical chi, and log(1/epsilon),
for bunched input and the specified explicit finite passive/Kerr circuit.
It samples counts to TV error epsilon even when K is binary-large.
Dependence on chi is NOT dependence merely on log chi. No arbitrary-Fock,
exponentially-many-branches, novelty, hardness or executed-sampler claim.
No counterexample or unresolved mathematical resource gate was found.

## 1. Exact proposal and interference

Using period q_j=2b_j is valid because the phase change under n->n+2b_j
is an integer multiple of2pi. Fourier Parseval gives sum_r|c_jr|^2=1.
Indexed products of these coefficients therefore have squared norm1,
whether or not distinct indices give identical passive interferometers.
Every branch from a bunched input is the normalized condensate associated
with the one-particle column alpha_r. Its count amplitudes have the stated
multinomial magnitude and product phase. No permanent oracle is required.

Write S(x)=sum_r|psi_r(x)|^2. Uniform branch choice followed by its count
sample has law S/chi. Cauchy--Schwarz yields

    |sum_r c_r psi_r(x)|^2 <= S(x).

The acceptance ratio in the note is consequently in[0,1]. Its accepted
unnormalized law is |Phi(x)|^2/chi, so the exact acceptance probability is
1/chi, since the original expanded circuit is unitary. Coincident branches
and destructive interference do not alter this identity. The process
retains cross terms, in contrast to an incoherent Fourier-branch mixture.

## 2. Finite normalized vectors are well-conditioned

Store rational-complex approximations beta_r to the exact one-particle
columns and define alpha_tilde_r=beta_r/||beta_r||. The components need not
be rational, but their squared magnitudes are exact rational numbers. All
beta_r have norm bounded away from0 because the true columns have norm1.
Apply the same normalization to a rational-complex approximation of c.
It is essential to retain vector phases, not approximate columns merely
up to arbitrary scalar phase: the condensate raises that phase to K.

For normalized vectors alpha,alpha_tilde, the tensor telescoping bound is

    ||alpha^tensorK-alpha_tilde^tensorK|| <= K||alpha-alpha_tilde||.

The symmetric tensor is exactly the normalized K-boson condensate. The
branch-state column operator has norm at most sqrt(chi). Hence

    ||Phi-Phi_tilde||
      <= sqrt(chi)||c-c_tilde||_2
         + sqrt(chi)K max_r||alpha_r-alpha_tilde_r||.

The note's tolerances make this at most epsilon/256 (in fact smaller).
Thus nu=||Phi_tilde||^2 lies in[3/4,5/4]. Normalizing Phi_tilde changes its
distance from the original unit vector by at most twice the preceding
error. Its count law is within epsilon/128. No computation of nu is needed:
exact coherent rejection on these finite inputs succeeds with nu/chi.

All coefficient/vector approximations are constructible by enumerating
the chi branches and propagating m-dimensional one-particle vectors.
Fourier sums, trigonometric evaluations, and normalization use polynomial
precision and polynomial time in chi and native length. An exponential
numeric chi is an exponential charged cost, not a hidden compression.

## 3. Binary binomial subroutine

For nontrivial N>=1 and 0<p=a/b<1, all parameters of the note are rational
or integer. Bernstein gives the stated tail bound for the outward-rounded
interval I. The characteristic-function integral gives

    max_k Pr(X=k) <= sqrt(pi)/(2sqrt(2v)) < 1/sqrt(v),
    v=Np(1-p).

For d=floor(sqrt(Na(b-a)))>=1, M=min(1,b/d) is a genuine upper envelope,
not merely an approximation to one. Also M<=min(1,2/sqrt(v)), so the
written interval-size inequality implies J M<=16t. These statements are
uniform in numerical N, including v<1 and probabilities near0 or1.

The single-clock proposal samples h=ceil(log2 J) bits and discards out-of-
range indices. The exact round acceptance is P(I)/(2^h M)>=3/(128t).
Pointwise acceptance error e=delta/(64t), delta<=1/4, decreases this by at
most e, leaving at least1/(64t). The stated R_bin therefore pays timeout
<=delta/4. Conditional on acceptance, the normalized law has TV error
at most J M e/P(I)<=delta/3 from the exact interval-conditioned binomial.
Together with truncation <=delta/4 the total is <delta. This argument
handles normalization explicitly; no unbounded rejection is invoked.

The underflow/exponential clipping step needs only absolute acceptance
precision. If ell=log(PMF/M)<=0 is known within e/8, clamping exp(ell)
changes the result by O(e); values below the written negative logarithmic
cutoff contribute less than e. Dyadic rounding and fixed finite coins pay
the remaining constant margin. None of these steps requires relative
precision on an arbitrarily small PMF.

For the positive-real Stirling first-omitted-term bound used in the note,
the displayed factorial estimate is algebraically correct:

    4(2r)!/((2pi)^(2r+2) x^(2r+1))
       <= (2r/(2pi x))^(2r) <= 2^(-5r),  x>=2r.

This follows from (2r)!<=(2r)^(2r) and 2log2(2pi)>5. Shifting a small
argument by2r uses only O(r) factors, each of O(log r) bits because that
branch has n+1<2r. For large arguments, O(log N) guard bits pay multiplication
by N in the leading Stirling/log-probability terms. Argument reduction of
integers of bitlength B additionally needs O(log(B+2)) guard bits for the
coefficient multiplying log2. Thus the note's precision is polynomial in
log(N+2), bitlength(p), log(1/delta), without a numeric-N loop. Exact
Bernoulli numbers through order2r have polynomial construction/bit cost.
The analytic first-omitted-term premise is the standard positive-real
Stirling bound; the parent separately checked its actual DLMF source.

Sequential multinomial sampling uses exact rational conditional probabilities.
Zero remaining probability is handled explicitly; division by a small but
nonzero rational has polynomial bit cost. Per-call TV errors add under a
sequential coupling, so m-1 binomials pay each proposal's requested TV.

## 4. Outer cutoff and bounded-process coupling

Use the note's exact finite normalized vectors. Fix

    R=ceil(16chi ceil(log2(16/epsilon))),
    D0=(K+1)^m,  tau=epsilon/(256 R D0).

Only O(m log(K+1)) bits represent D0; count vectors are never enumerated.
The ideal outer sampler succeeds with probability nu/chi>=3/(4chi), so
its R-round timeout is <epsilon/256. For the exact proposal S/chi,

    Pr(S(x)<=2tau) <= 2D0 tau/chi.

Consequently, ANY extra rejection confined to that set changes the entire
R-trial output process by at most2R D0tau/chi<=epsilon/128. This is an
unconditional coupling bound on capped processes; no target normalization
or lower bound on every probability is assumed.

The deterministic test using an approximation S_hat within tau/4 and
threshold3tau/2 has precisely the needed property: rejected outcomes have
S<=7tau/4<2tau, and retained outcomes have S>5tau/4>tau. No exact decision
at S=tau or at a transcendental equality is necessary.

On retained outcomes, with gamma=epsilon/(256R), numerator and denominator
errors <=gamma*tau/16 give ratio error <gamma/4 before the final arithmetic
margin. For example, computing EVERY amplitude and coefficient to absolute
error <=gamma*tau/(1000chi^2), and using appropriate elementary arithmetic
guard bits, is a sufficient common tolerance. It is slightly more conservative
than the illustrative amplitude tolerance in the note and makes its
"further polynomial margin" explicit. Clipping and dyadic rounding then
give a Bernoulli acceptance error <=gamma per trial.

Uniform-branch and multinomial proposal errors each <=epsilon/(256R),
ratio errors <=gamma, the small-S coupling loss, ideal timeout and initial
normalized-state perturbation sum to less than epsilon. The comparison is
to a fixed R-trial process, so no missing factor from conditioning on rare
acceptance remains. All needed log precisions contain only log R, log chi,
m log(K+1), native coefficient lengths, and log(1/epsilon).

## 5. Amplitudes and scope

A branch amplitude can be evaluated using half the log multinomial PMF
for its magnitude and the phases (beta_i/|beta_i|)^x_i. An exact zero beta_i
with x_i>0 gives zero immediately; exponent0 contributes1. Nonzero rational
entries have a lower bound paid by their finite bitlength, so extracting
their unit phases is polynomial-bit arithmetic. Binary powering costs
O(log(K+1)) multiplications and O(log(K+1)) additional precision. If the
log magnitude is below the absolute-amplitude threshold, output0; there
is no need to represent exp(-Theta(K)) probabilities explicitly.

This closes the stated bunched, polynomial-chi classical counterpart.
It does not apply to arbitrary occupied input patterns: their passive
branch amplitudes and samplers need not be condensate/multinomial objects.
It does not make chi polynomial for long Kerr circuits. In particular the
earlier dual-rail universal gadget does not contradict this bounded-branch
sampler. No conclusion is drawn from passing finite controls or from a
failure of another classical algorithm.
