# Structured EDCP: Local Readout Is Already Information-Sufficient

Date: 2026-09-24. LOCAL DERIVATION / REVIEW PENDING.

This is an adversarial baseline for the preceding information theorem. Local
Fourier measurements followed by unrestricted CLASSICAL maximum-likelihood
decoding also suffice with a constant number of blocks in a scoped growing
Gaussian regime. The classical search is not shown to be efficient. This
does not classically simulate the original quantum source or prove a speedup.

The research consequence is substantive: an information certificate alone
cannot justify a collective-measurement advantage for this family. Any proposed
joint-fiber algorithm must be compared with decoding the classical data below.
`research/STRUCTURED_EDCP_PRIOR_CVP_BASELINE.md` supplies the next concrete
baseline: a charged noise approximation, the actual prior-aware weighted
lattice, and bounded exact-LLL/Babai checks. It does not supply a scaling
guarantee or identify joint-lift MAP with marginal-secret MAP.
The local Fourier transformation is related to the already published
structured-EDCP-to-noisy-linear-data construction in section 4 of
[Wen and Zheng](https://eprint.iacr.org/2026/155.pdf); no novelty is claimed.
Our exact overlap and divisor analysis is derived here for the stated source.

## 1. An Exact Finite Source For The Local Measurement

Use Q=q^d+1 and n-dimensional labels as in
`research/STRUCTURED_EDCP_INFORMATION_THRESHOLD.md`. Define on Z_Q

    h(j)=exp(-pi*j^2/sigma^2), j in Z,
    g(j)=sum_(k in Z) h(j+kQ), j in Z_Q,
    Zg=sum_(j in Z_Q) g(j)^2,    mu_Q(j)=g(j)^2/Zg.

One coefficient's state, at frequency theta in Z_Q, has amplitudes
g(j)*omega_Q^(j*theta)/sqrt(Zg). Its local QFT outcome is

    Y=theta+E mod Q,
    Pr[E=e]=nu(e)=hat_g(e)^2/Zg,
    hat_g(e)=Q^(-1/2)*sum_j g(j)*omega_Q^(-j*e).

Poisson summation gives the crucial property

    hat_g(e)=(sigma/sqrt(Q))*sum_(k in Z)
                 exp(-pi*sigma^2*(k+e/Q)^2) > 0.

Thus nu is an explicitly known noise distribution. No phase signs have been
discarded. The original unperiodized Gaussian source is extremely close;
section 4 charges this comparison. This is not a new assumed oracle family.

For the whole source, independent local QFTs produce the classical data

    Y_(l,i)=q^i*<a_l,s>+E_(l,i) mod Q,
    l=1,...,L, i=0,...,d-1,

with independent E_(l,i) of law nu. The public labels remain the actual
independent uniform labels. A QFT operates on O(log Q) qubits per coordinate,
not a Q-entry classical array. Gate approximation and source errors are
separate charges; no circuit compilation was performed in this pass.

## 2. Exact Classical Overlap And Error Bound

Let the Bhattacharyya overlap of two shifted noise distributions be

    B(v)=sum_e sqrt(nu(e)*nu(e-v)).

Because hat_g is real and positive, Parseval gives the EXACT equality

    B(v)=sum_j mu_Q(j)*omega_Q^(j*v) >= 0.                     (1)

The right-hand side is the pure-state inner product, not its square.
Positivity matters: arbitrary amplitude distributions need not satisfy (1).
This equality does not imply equal optimal quantum and classical success.

Consider maximum likelihood over ALL s in Z_Q^n. If a wrong s' beats the
true likelihood, then p_s(y)<=sqrt(p_s(y)*p_(s')(y)). A union bound gives,
for each secret and fixed A,

    Pr[ML error | A,s] <= sum_(Delta != 0)
                           prod_(l,i) B(q^i*<a_l,Delta>).

For t dividing Q let beta_t=Pr[sum_i q^i C_i=0 mod t], where C_i have
law mu_Q. Averaging a single uniform column against a character of order t
gives beta_t, by Fourier orthogonality. Independent columns and the Jordan
character counts from the preceding note give

    E_A[Pr[ML error | A,s]]
       <= sum_(t|Q,t>1) J_n(t)*beta_t^L.                      (2)

This is a bound for every s, not an assumption of a uniform actual source
prior. The decoder enumerating all secrets is only an existence baseline:
Q^n possibilities are exponential in d*log q. Likelihood evaluation alone
does not supply an efficient search procedure.

Note the distinction from the quantum information note: beta_t is a ZERO
probability for ONE evaluation, whereas C_t is a collision probability for
TWO evaluations. Substituting one for the other would overstate the baseline.

## 3. Bounding The Classical Divisor Terms

Here are explicit sufficient finite premises, followed by an asymptotic regime
that satisfies them. Suppose d>=2 is a power of two, q>=3, 8<=sigma<=d,
and let

    alpha=4/sigma < 1,
    Rq=floor((q-1)/2),
    tau_q = sigma^2/(2*pi*Rq)*exp(-2*pi*Rq^2/sigma^2),
    B0=floor(q^2/2),
    T0 = sigma^2/(pi*B0)*exp(-pi*B0^2/sigma^2),
    epsilon_wrap = min(1,2*T0+T0^2).

Require the scalar inequality

    d*(tau_q+epsilon_wrap) <= (1/2)*alpha^d.                  (3)

It can be checked in log space without forming a residue table. Section 4
proves the periodization error used here.

For the unwrapped coefficient probability mu(j) proportional to h(j)^2,
Poisson summation gives its normalizer at least sigma/sqrt(2). Consequently
max_j mu(j)<=sqrt(2)/sigma<2/sigma.

For an odd divisor 1<t<q, the preceding note proves t>=2d+1. The maximum
Gaussian residue mass occurs at zero, since its discrete Fourier coefficients
are nonnegative. This mass is bounded by

    (sqrt(2)/sigma)*(1+2*r/(1-r^3)),
    r=exp(-2*pi*t^2/sigma^2) <= exp(-8*pi),

and is less than 2/sigma. Convolution with further independent digits cannot
increase the maximum mass.

For t>=q set k=floor(log_q t)<=d. Restrict the first k digits to [-Rq,Rq].
Their evaluations are injective modulo t, giving maximum mass at most
(2/sigma)^k in that subdistribution. The excluded probability is at most
k*tau_q. Add the remaining independent digits, then compare to the periodized
law with error at most d*epsilon_wrap. Condition (3) implies, in both cases,

    beta_t <= alpha^max(1,floor(log_q t))
            <= t^(-h/(2*log(q))),   h=-log(alpha).             (4)

For example, in the large-t case, (2/sigma)^k=alpha^k*2^(-k), and the
additive error is at most alpha^d/2<=alpha^k/2. This is why the small tail
must be bounded BEFORE summing exponentially many secret competitors.
Merely assigning it a small inverse-polynomial value would not justify (2).

Let b_local=L*h/(2*log(q))-n>1 and

    T_local=(2d)^(1-b_local)/(b_local-1).

For q even, (2)-(4) give mean ML error at most T_local. For q odd, condition
on the same full-row-rank event G for A mod 2 as in the preceding note.
Let b_Q=sum_j (-1)^j mu_Q(j). Equation (1) makes b_Q nonnegative. The
order-2 contribution is at most (2^n-1)*b_Q^d on G. Other orders u,2u obey
beta_(2u)<=beta_u and J_n(2u)=(2^n-1)*J_n(u). Thus

    E[ML error | G,s] <= (2^n-1)*b_Q^d + (2^n/p_G)*T_local.   (5)

The parity exponent is d, NOT 2d as in the collision/PGM bound. Rank selection
still costs L/p_G blocks on average. Without it, exact secret aliases remain.

If q=d^(a+o(1)), sigma=d^(b+o(1)), with 0<b<1 and a>b+1/2, then
q^2/sigma^2 grows faster than d*log d. Condition (3) eventually holds,
h=log(sigma)-log(4), and log(q)/h tends to a/b. For any fixed desired
inverse-polynomial error exponent, a sufficiently large CONSTANT L therefore
suffices in (2) or (5). The Gaussian parity term decays faster. A constant
L does not give negligible error at all exponents simultaneously.

This covers both the q=d^2,width=sqrt(d) ensemble and the larger-modulus
formal source-parameter regime in the preceding note. It is not a sharp
sample threshold or a proof of an efficient classical decoder.

## 4. Periodization And Physical Source Error

Let I_Q=[-floor(Q/2),ceil(Q/2)-1] be canonical integer representatives, and
put B=floor((Q-1)/2). The amplitude tail outside I_Q satisfies

    T_amp <= sigma^2/(pi*B)*exp(-pi*B^2/sigma^2) <= T0,

since Q=q^d+1>=q^2+1. In the residue register, the vector of omitted
amplitudes has Euclidean norm at most T_amp. Normalizing changes the pure
state by trace distance at most 2*T_amp. The unwrapped probability folded
modulo Q differs from the normalized canonical truncation by total variation
at most T_amp^2. It follows that

    TV(mu_Q, law(C mod Q)) <= 2*T_amp+T_amp^2 <= epsilon_wrap.

This proves the comparison in section 3. It also charges the actual quantum
operation: project the supplied integer coordinates onto I_Q, map them
reversibly to residues, and perform local QFTs. Across d*L coordinates the
projection fails with probability at most d*L*T_amp^2, and its accepted state
differs from the ideal periodized product by at most 2*d*L*T_amp. These
errors are tiny in the stated regime but are not identically zero.

If a practical source instead truncates at a MUCH smaller R, include that
source's actual joint trace distance, as well as QFT implementation error.
If only preselection error is known, charge its amplification under G.
CORRECTION: on a common success event, trace errors epsilon_i against PURE
marginal targets imply joint product error <=sqrt(sum_i epsilon_i). Mixed
marginal guarantees or separate constant-probability success events do not
suffice. `research/STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md` supplies a scoped
last-stage source repair with an explicit unheralded clean-product component;
the upstream reduction remains unverified.

## 5. Verification Actually Performed

Exact finite ensemble formulas were checked numerically with periodized
Gaussian amplitudes. Complete classical outcome likelihoods and optimal
collective reference probabilities were evaluated for every label tuple:

| q,d,sigma,L | Label Tuples | Mean Local-QFT + Classical ML | Mean Collective PGM |
|---|---:|---:|---:|
| 3,2,1.4,1 | 10 | 0.2305925710 | 0.2730514459 |
| 3,2,2.0,2 | 100 | 0.6630625322 | 0.7674808181 |
| 4,2,2.0,1 | 17 | 0.3511153335 | 0.4266234775 |
| 5,2,3.0,1 | 26 | 0.4031770722 | 0.4940666376 |

Across all 153 label tuples, classical success never exceeded the quantum
optimum, and the pairwise error bound held. The overlap identity residual was
at most 4.45e-16; the averaged divisor-moment residual was at most 1.78e-15.
The union bounds are vacuous at these small parameters; the table is an
identity check, NOT evidence for asymptotic recovery or a scalable decoder.

A sign countercontrol, amplitude vector (1,0,1,0,0)/sqrt(2) modulo 5,
has classical overlap 0.7090169944 at shift one, but pure-state overlap
magnitude 0.3090169944. It correctly fails equality (1).

Separately, 60-digit evaluations checked (3) and the analytic bounds at n=1,
L=160,sigma=sqrt(d). These are IDEAL information bounds, before source and
gate error; they are not measured recovery rates:

| d | q | Mean ML Failure Bound |
|---:|---:|---:|
| 64 | 4096 | 3.14302e-11 |
| 64 | 4097 | 6.29227e-11 |
| 256 | 65536 | 2.64698e-23 |
| 256 | 65537 | 5.29442e-23 |
| 1024 | 1048576 | 7.70372e-35 |
| 1024 | 1048577 | 1.54076e-34 |

All six finite scalar criteria passed. No bulk workflows, production tests,
candidate promotions, or efficient ML/collective decoder implementations.

## 6. Revised Algorithmic Target And Handoff

The meaningful competition is now between efficient CLASSICAL decoding of
the locally measured data and efficient QUANTUM processing of the supplied
phase states. Both have enough information in the specified regime. The
present result does not show either decoding problem is easy, nor does it
rule out a runtime advantage from a coherent collective measurement.

Do not say the source has been dequantized: a classical processor receiving
these quantum-generated outcomes is not a classical sampler from the original
input/access model. Proving such a sampler is a separate obligation. Equally,
do not say statistical sufficiency requires joint entangling readout here.

MAIN MODEL: attack the noisy geometric-label classical inference problem
above, retaining modular carries and the actual secret prior. Compare lattice
decoding, hidden-number methods and structured integer inference with the
joint-fiber construction. The narrower Gaussian secret prior in the source
reduction could materially change the required L; analyze it before rejecting
all few-block routes. A better information constant is lower priority than
an actual efficient decoder or a rigorous obstruction to a specific decoder.

GEMINI: implement only the specified bounded reference and analytic report,
with positivity and parity countercontrols and an explicit exponential-search
warning on maximum likelihood. No Q-sized table belongs in a scalable path.
Keep the local-measurement runtime separate from classical decoding runtime
and from the source preparation cost. This note is a handoff, not integration.
