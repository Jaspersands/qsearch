# Structured EDCP: Ideal-Norm Collisions And The Small Conditional Core

Date: 2026-09-27. LOCAL DERIVATION / REVIEW PENDING.

## 1. Research Decision

The wide-support information bound can be substantially sharpened by using
the cyclotomic IDEAL behind each evaluation divisor. This is established
Gaussian/ideal geometry specialized to our source, not a claim of a new
general technique. The resulting finite certificate needs only THREE wide
blocks at each current reference dimension, rather than the earlier 12,9,8.
Two blocks suffice asymptotically in the stated regime, conditional on the
binary-rank event, but the present finite two-block certificates are vacuous.

DECODER FOLLOW-UP: `STRUCTURED_EDCP_SHEAR_ALIAS_DECODER.md` examines a
concrete global shear. Its measured linear-correction branch is exactly a
classical readout postprocessor; coherent integer-alias processing remains
open. The information certificate here does not discharge that operation.

ALGEBRAIC FOLLOW-UP: `STRUCTURED_EDCP_MODULE_GLUING_AUDIT.md` checks the
principal-ideal route. Orthogonal field lines leave index Q^(L-1) in the
native kernel; discarding their integral coupling fails a source-weighted
fidelity test. The known ideal generator q-X does not supply the core map.

This identifies a smaller, concrete algorithmic target: coherent Gaussian
conditioning for a few naturally labeled blocks. It does not solve that
problem. Information sufficiency, smoothing and the existence of many short
preimages do not supply an efficient algorithm to prepare those preimages.

Dependencies: `STRUCTURED_EDCP_DIRECT_PHASE_SOURCE.md`,
`STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS.md` and
`STRUCTURED_EDCP_WIDE_PHASE_INFORMATION.md`. The earlier bounds remain valid
under their premises; this one is tighter, not a retroactive experiment success.

## 2. The Evaluation Kernel And Its Euclidean Dual

Let d>=2 be a power of two, q>=3, Q=q^d+1 and t|Q. In the coefficient
Euclidean space of R=Z[X]/(X^d+1), define

    I_t={v in R: v(q)=0 mod t}, Gamma_t=I_t^*.

Evaluation is a surjective ring homomorphism R -> Z_t, so I_t is an ideal
of index t and its coefficient lattice has determinant t. Its Euclidean
dual has determinant 1/t. Do not confuse this COEFFICIENT dual with the
canonical trace dual without accounting for conjugation and the codifferent.

Here is a direct proof of the needed norm bound. If w is in Gamma_t and
v is in I_t, every coefficient of w*conjugate(v) is an integer: it is the
inner product of w with a signed rotation of v, which is still in I_t.
Consequently w*conjugate(I_t) is contained in R. The rational multiplication
matrix M_w, applied to an integral basis of conjugate(I_t), is an integral
matrix of determinant t*N(w). For w!=0 that determinant is NONZERO, since
X^d+1 is irreducible. Therefore

    |N(w)| >= 1/t.

If zeta ranges over the d complex roots of X^d+1, Parseval and AM-GM give

    sum_zeta |w(zeta)|^2 = d*||w||_2^2,
    |N(w)|^(2/d) <= ||w||_2^2.

Thus the coefficient-norm statement, with its precise normalization, is

    lambda_1(Gamma_t) >= t^(-1/d).                           (1)

It requires no factorization of t and no assumption that I_t is principal.
Power-of-two d is important. At d=3,q=17,t=18, the vector (1,-1,1)/18 is
in the evaluation dual but has squared norm 1/108, violating (1). Its
multiplication norm is zero in the reducible algebra. That countercontrol
prevents importing the argument to arbitrary polynomial quotient rings.

## 3. A Gaussian Collision Bound At Every Divisor

Write s=s_G=sigma/sqrt(2), and initially use the untruncated product
D_(Z,s)^d coefficient law. The standard smoothing inequality

    eta_(2^(-2d))(Lambda) <= sqrt(d)/lambda_1(Lambda^*)

and Gaussian scaling under Poisson summation imply

    rho_(1/s)(Gamma_t)
      <= (1+epsilon_d)*max(1,(sqrt(d)*t^(1/d)/s)^d),
    epsilon_d=2^(-2d).                                      (2)

For s above the smoothing threshold this is the definition of smoothing;
below it, rho_(1/s)(Gamma_t) grows by at most the d-th power of the width
ratio, using Poisson summation on Gamma_t. Equations (1)-(2) specify which
lattice and which width are involved; canonical and coefficient widths must
not be interchanged.

For any evaluation residue x, Poisson summation on I_t gives

    Pr[E(C)=x mod t]
      <= s^d/(t*theta(s)^d)*rho_(1/s)(Gamma_t)
      <= (1+epsilon_d)*max(1/t,beta),
    beta=(sqrt(d)/s)^d.                                     (3)

Collision probability is at most maximum point mass. Now truncate EACH digit
to [-R,R], with retained scalar mass zeta. Conditioning two FULL d-coordinate
vectors costs zeta^(-2d), not the zeta^(-2) of the older single-digit argument.
Define alpha=(1+epsilon_d)*zeta^(-2d). For the truncated law,

    C_t=Pr[E(C)=E(C') mod t] <= alpha*max(1/t,beta).           (4)

Cap the right side at one when useful. This proof imposes no R<=d or
2R<=q-1 restriction; unlike the prefix proof it does not require digit
injectivity. Efficient preparation, source error and any coefficient-register
conversion still have their own contracts.

## 4. Summing Actual Divisors Through Their Prime Structure

For independent uniform rank-n labels and L blocks, the exact identity is

    E chi2 = sum_(t|Q,t>1) J_n(t)*C_t^L.

Let h=L-n>0. On ODD divisors, max(x,y)^L<=x^L+y^L and
sum_(t|Q) J_n(t)=Q^n give

    odd contribution <= alpha^L*(S_h+Q^n*beta^L),
    S_h=sum_(t|Q,t>1,t odd) J_n(t)/t^L.                      (5)

The Euler product bounds

    1+S_h <= product_(odd p|Q) (1-p^(-h))^(-1).

Every such prime p has order 2d for q modulo p, so p=1 mod 2d. Listing
distinct primes increasingly, p_j>=2d*j+1. These restrictions supply a
much sharper sum than counting every integer as a possible divisor.

For h=1, let r_max be any certified upper bound on their number. Then

    S_1 <= exp(H_(r_max)/(2d))-1,
    H_r=sum_(j=1)^r 1/j.                                    (6)

Indeed -log(1-1/p)<=1/(p-1), and the distinct-prime product is at most Q.
One entirely integer computable choice is

    r_max=floor(floor(log2 Q)/floor(log2(2d+1))).

Bit lengths give both inner floors; no modulus factorization is needed.
For h>=2, summing over all j>=1 gives the simpler bound

    S_h <= exp((1+1/(h-1))/(2d)^h)-1.                        (7)

Here 1/(p^h-1)<=1/(p-1)^h and sum j^(-h)<=1+1/(h-1).
Repeated prime powers were already included in the Euler product; there is
no hidden square-free assumption.

For even q, Q is odd and (5) bounds the whole expected chi-square. For odd
q, impose the public event G of full binary row rank. With the notation of
the preceding information note,

    p_G=prod_(i=0)^(n-1)(1-2^(i-L)),
    b=sum_c (-1)^c*mu(c),
    delta_info=(2^n-1)*|b|^(2d)
                 +(2^n/p_G)*alpha^L*(S_h+Q^n*beta^L).        (8)

Then E[chi2 | G]<=delta_info, and the ideal optimal measurement has average
success at least 1/(1+delta_info), equally for every secret. This is NOT an
efficient measurement. Use the existing source ledger and charge p_G; binary
full rank does not mean all labels are units modulo Q.

## 5. Two Asymptotic Blocks, Three At The Current Parameters

The finite table in this section is for the original coefficient-width
sqrt(d) source, not a hardness certificate. The separate theorem-linked
sources in `STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md` require recomputed
widths and have sufficient finite counts 4,3,3 at these reference dimensions.

Let q=d^(a+o(1)), sigma=d^(b0+o(1)), and use truncation with negligible
joint coefficient loss. For fixed n,L with L>n, the large-divisor term is

    Q^n*beta^L = exp((a*n-L*(b0-1/2)+o(1))*d*log d).

Thus it vanishes when L*(b0-1/2)>a*n. For L=n+1, (6) gives
S_1=O(log d/d), since log Q=Theta(d*log d) and r_max=O(d).
For L>=n+2, (7) is O(d^(-(L-n))).

At n=1,a=12,b0=9.5, TWO blocks suffice asymptotically conditional on G.
One cannot suffice for a uniform secret: the existing kappa-entropy converse
has log P_opt<=-(2.5+o(1))*d*log d. This identifies the asymptotically minimal
constant block count in this regime, NOT an efficient two-block decoder.
If the source's phase-error budget is d^(-c), its moment width becomes
d^(9.5-c+o(1)); two blocks still meet the sufficient bound for every fixed
0<c<3. A fixed 0.001 source error is therefore not essential to the statement.

Finite constants matter. Using the exact upstream recipe and moment source
with total L=3, n=1,K=4 and phase budget 0.001 gives:

| d | sigma reference | delta_info reference | log10(Q*beta^3) |
|---:|---:|---:|---:|
| 64 | 258071404.370480 | 2.79034888e-4 | -25.61568085 |
| 256 | 4.42089206e13 | 1.74386826e-5 | -2041.278774 |
| 1024 | 9.26124923e18 | 1.08991376e-6 | -16188.84025 |

For L=2, with the corresponding wider source budget, log10(Q*beta^2) is
434.0351,1060.1058,1357.3110: those certificates are VACUOUS. Do not report
finite two-block success or infer finite two-block impossibility from them.

Here p_G=7/8 for the three-block case. If the ideal measurement were efficient,
one-batch success would be at least p_G/(1+delta_info) minus the COMPLETE
source and measurement errors. The phase term alone is 0.001; it is not the
whole source ledger. Bounded repetition must use its TOTAL number of prepared
blocks in the source budget. The one-batch information calculation is not a
free unlimited-sample or fixed-instance retry guarantee.

The native unit-first-label basis still has log10 H lower bounds about
858.4278271,3943.394476,17722.82358 at these widths. The known generic native
sampler remains exponentially expensive. Its unit-label event is separate
from G. Improving information sufficiency did not implement the sampler.

These are 120-digit analytic references, not interval certificates or
executed high-dimensional quantum states. The near-one zeta/alpha factors
must be bounded with directed precision in production. Gaussian tails are
not exact zero. Earlier source primality/review qualifications remain.

## 6. Checks, Failure Modes And Next Work

- 306 exact rational dual-vector controls at (q,d)=(3,2),(5,2),(17,2),
  (3,4),(5,4),(3,8). For sampled vectors in Gamma_t across divisors t,
  t*N(w) was a nonzero integer and the norm bound held using integer powers.
  The d=3 counterexample above failed the norm bound as intended.
- 25 direct finite Gaussian collision controls covered seven ensembles,
  including R>q and divisors of Q with repeated-prime possibilities. All
  respected (4). Finite sums were cut at R=ceil(4*sigma); the uncharged
  normalization tail in these floating references was below 1e-40, beneath
  the 2e-12 check tolerance. They are not exact infinite-sum verifications.
- 306 exact rational Euler-sum controls covered d=2,4,8, q=3,...,19,
  n=1,2 and h=1,2,3. Exact divisor sums respected (6)-(7), including repeated
  prime powers. Production evaluation of the bound itself needs no factoring.
- Three finite three-block source reports and three vacuous two-block reports
  retained every term of (8). No efficient decoder or growing quantum run.

Likely failure of the research direction: sampling a dense modular Gaussian
fiber can remain computationally difficult even when its residue law is
nearly uniform. The generic polar normalization and native-basis profile
obstructions do not disappear. A claim of progress must exhibit the arithmetic
map, its bit complexity, coherent precision and matched classical alternative.

Highest-impact next question: for two or three random scalar labels, can the
weighted kernel fiber be prepared/erased by exploiting the negacyclic
multiplication structure, without a Gaussian-preimage oracle, a trapdoor-chosen
label matrix, a Q-sized table or a short lattice basis assumed for free?
The earlier conditional-core extension can then append other blocks, but it
does not supply this core. Start with the naturally distributed three-block
regime above, not a favorable hand-selected instance.

Gemini should add `ideal_norm` as an independently checked information
certificate with fields lambda_dual_lower,epsilon_d,alpha,beta,S_h,p_G and all
applicability premises. Retain the older prefix bound as a comparison, not
as the default wide-source bottleneck. Exact small-divisor references should
catch a missing zeta^(-2d), a dropped prime-power contribution or a canonical
embedding scale error. Keep two-block finite failures visible and all status
REVIEW PENDING. Source construction, information and efficient decoding must
remain different proof obligations.

## Primary Source

[Lyubashevsky, Peikert and Regev, A Toolkit for Ring-LWE Cryptography,
full version dated 2013-05-16](https://sites.cc.gatech.edu/fac/cpeikert/pubs/toolkit.pdf),
Lemma 2.6 and Claim 7.1, provide the smoothing and Gaussian scaling bounds used
in (2). Their ideal-norm and embedding discussion is relevant context. The
coefficient-dual normalization, arithmetic-progression divisor sum and source
specialization are derived explicitly above; no independent novelty claim.
