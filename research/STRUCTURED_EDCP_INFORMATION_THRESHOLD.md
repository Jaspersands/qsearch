# Structured EDCP: Information Before Implementation

Date: 2026-09-24. LOCAL DERIVATION / REVIEW PENDING.

This note proves a scoped sufficient-information bound for the ideal native
coefficient-state ensemble. It does NOT provide an efficient joint measurement,
verify an entire lattice reduction, establish novelty, or claim a speedup.
Finite checks below test the identities, not an asymptotic algorithm.

## 1. Research Decision

Do not treat two blocks as an adequate full-secret decoder by default. The
necessary block count depends on coefficient entropy relative to the modulus.
For q=d^(a+o(1)), Gaussian amplitude width sigma=d^(b+o(1)), and constant
module rank n, any fixed L with b*L<a*n has vanishing optimal success for
a UNIFORM secret in Z_(q^d+1)^n. This converse also holds without truncation.

Conversely, under explicit conditions below, a larger CONSTANT L suffices for
inverse-polynomial mean error at any fixed chosen exponent. Odd q requires a
detectable binary-rank selection event, with its sampling cost included.
This changes the next target from an unexplained two-block success experiment
to a naturally distributed, information-sufficient joint-fiber measurement.
Two-block fibers remain useful structural prototypes, not guaranteed decoders.

The full-secret converse does not apply unchanged to a narrow secret prior.
The sufficient measurement has equal success for every secret and thus works
for any prior, if that measurement can actually be implemented.

Prior art: structured coefficient states are from Definition 22 of
[Wen and Zheng](https://eprint.iacr.org/2026/155.pdf). The distinction between
optimal discrimination and efficient implementation is established in
[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
This is a direct moment/regularity argument, not a new conceptual framework;
compare the composite-modulus Gaussian leftover-hash work of
[Jin, Liu, Wang and Gu](https://eprint.iacr.org/2024/1695.pdf).
An independent novelty and proof review remains necessary.

## 2. Exact Ensemble And Two Information Bounds

Let d>=2 be a power of two, q>=3, Q=q^d+1, and n,L positive integers. Let
mu be a known probability distribution on integer digits [-R,R], with

    1 <= R <= d,             2R <= q-1,
    c2 = sum_j mu(j)^2 < 1,  h2 = -log(c2) > 0.

All logarithms are natural. The collision identity in section 3 does not need
these support or cyclotomic restrictions; the all-divisor bound does.

Use independent coefficient vectors C_l whose d coordinates have law mu.
Write E(c)=sum_i q^i c_i mod Q, U_l=E(C_l). Public labels a_l are independent
uniform vectors in Z_Q^n, independent of the coefficients and secret. Let
A have these labels as its columns. The supplied joint pure state is

    |Psi_(A,s)> = sum_(c_1,...,c_L) sqrt(prod_(l,i) mu(c_(l,i)))
                    * omega_Q^(<s, sum_l a_l E(c_l)>) |c_1,...,c_L>.

No unknown centers, unknown phases, retained garbage, or correlated blocks
are silently identified with this state. Fourier measurement of the offset
registers of ideal independent structured-EDCP samples produces these uniform
labels: conditional phase states are normalized, and each label has probability
Q^(-n). An offset contributes only an irrelevant global phase.

Define the weighted fiber distribution

    P_A(v) = Pr[sum_l a_l U_l = v],  v in Z_Q^n.

Collecting equal-v terms into orthonormal normalized fiber states gives

    P_opt(A) = (sum_v sqrt(P_A(v)))^2 / Q^n.

This is the optimal success for the uniform-secret ensemble. Averaging a POVM
over the secret's phase action fixes its seed diagonal to 1/Q^n on occupied
fibers; positivity bounds every seed entry by 1/Q^n. A Fourier seed attains
the displayed bound. Its success is the SAME for every s, not just on average.
Implementing that seed in coefficient registers requires a joint-fiber
isometry that is not supplied by the formula.

Let chi2(A)=Q^n*sum_v P_A(v)^2-1. Holder's inequality yields

    1 = (sum_v P_A(v))^3
      <= (sum_v sqrt(P_A(v)))^2 * sum_v P_A(v)^2,
    P_opt(A) >= 1/(1+chi2(A)).

Thus E[chi2]<=delta implies E[P_opt]>=1/(1+delta)>=1-delta.
The same argument works for a conditioned label ensemble. Markov gives,
for any tau>0, Pr[P_opt<1-tau] <= delta/tau. A mean guarantee is not
a pointwise guarantee for every label matrix.

There is also a useful converse. Set kappa=(sum_j sqrt(mu(j)))^2. Using
sqrt(sum_x w_x)<=sum_x sqrt(w_x) separately in each fiber gives

    P_opt(A) <= min(1, kappa^(d*L)/Q^n) <= min(1,(2R+1)^(d*L)/Q^n).

This holds for EVERY A, and the first bound holds for infinite digit support
whenever sum_j sqrt(mu(j)) is finite. No injectivity assumption is needed.
For untruncated Gaussian amplitudes exp(-pi*j^2/sigma^2),

    mu(j) proportional to exp(-2*pi*j^2/sigma^2),
    kappa = (sum_j exp(-pi*j^2/sigma^2))^2
                  / sum_j exp(-2*pi*j^2/sigma^2)
          = sqrt(2)*sigma*(1+o(1)) as sigma grows.

Consequently, for fixed L with b*L<a*n in the regime of section 1,
log P_opt <= -(a*n-b*L+o(1))*d*log(d). This is a uniform-prior bound;
it must not be used to exclude a decoder exploiting a smaller secret set.

## 3. Exact Composite-Modulus Collision Identity

For each t dividing Q, define

    C_t = Pr[U=U' mod t],
    J_n(t) = t^n * prod_(prime p dividing t) (1-p^(-n)).

Here U,U' are independent digit evaluations and J_n is the Jordan totient.
The exact identity is

    E_A[chi2(A)] = sum_(t|Q, t>1) J_n(t) * C_t^L.                (1)

Proof by collisions: condition on Delta_l=U_l-U'_l and put
g=gcd(Q,Delta_1,...,Delta_L). A uniform row of A maps this difference to
zero with probability g/Q. Independent rows give (g/Q)^n. Finally use
g^n=sum_(t|g) J_n(t) and Pr[t divides every Delta_l]=C_t^L. The t=1 term
cancels the minus one in chi2.

Independent Fourier proof: chi2(A) is the sum of squared nontrivial Fourier
coefficients of P_A. There are J_n(t) characters of exact order t in Z_Q^n.
For such a character, a uniform column label has a uniform scalar image in
Z_t. Averaging its squared characteristic function gives C_t. Independent
columns give C_t^L, proving (1).

The prime-only expression (Q^n-1)*C_Q^L is FALSE at composite Q. Nor does
large total entropy alone imply sufficient entropy modulo every divisor.

## 4. A Factorization-Free Bound For All Odd Divisors

If an odd prime p divides q^d+1, then q has order exactly 2d modulo p:
its order divides 2d but not d, and d is a power of two. Therefore p>=2d+1.
Every odd divisor t>1 of Q is consequently at least 2d+1.

For t>=q, let k=floor(log_q t). The first k digits evaluate injectively
modulo t. Indeed their difference has integer magnitude at most
2R*(q^k-1)/(q-1)<=q^k-1<t, and base-q digit differences with magnitude
at most q-1 cannot cancel unless all are zero. Their collision probability
is c2^k. Adding the independent remaining digits is convolution, which
cannot increase the squared L2 norm.

For odd t<q, a single digit is injective modulo t because t>=2d+1>2R.
Convolving with the remaining digits again only decreases collision. Thus

    C_t <= c2^max(1,floor(log_q t)) <= t^(-h2/(2*log(q))).       (2)

The last, deliberately conservative step uses max(1,floor x)>=x/2.
No factorization of Q is required to evaluate this bound.

Put

    beta = L*h2/(2*log(q)) - n > 1,
    T = (2d)^(1-beta)/(beta-1).

Since J_n(t)<=t^n, summing (2) over odd divisors t>1 gives at most
sum_(m=2d+1)^infinity m^(-beta)<=T. Summing over all these integers is
intentional: there is no unjustified omission of the number of divisors.

## 5. Odd Moduli And The Binary Obstruction

When q is EVEN, Q is odd and (1)-(2) immediately give

    E_A[chi2(A)] <= T,    E_A[P_opt(A)] >= 1/(1+T).             (3)

When q is ODD, d is even and Q=2 mod 8. Write Q=2M with M odd. Let G be
the public, efficiently testable event that A mod 2 has row rank n. For L>=n,

    p_G = Pr[G] = prod_(i=0)^(n-1) (1-2^(i-L)).

For L<n it is zero. Repeatedly sampling batches until G consumes L/p_G
blocks on average, before charging other preparation losses.

Let b=sum_j (-1)^j mu(j). Since q is odd, U has parity bias b^d.
For A in G, each nonzero binary secret character has at least one active
column, so its squared Fourier coefficient is at most |b|^(2d). All order-2
characters together contribute at most (2^n-1)*|b|^(2d), pointwise on G.

Other character orders are u and 2u with u>1 odd. C_(2u)<=C_u and
J_n(2u)=(2^n-1)*J_n(u). Their total UNCONDITIONAL expected contribution
is at most 2^n*T. Conditioning this nonnegative quantity on G costs at
most 1/p_G. Therefore

    E[chi2(A) | G] <= delta_even,
    delta_even = (2^n-1)*|b|^(2d) + (2^n/p_G)*T,
    E[P_opt(A) | G] >= 1/(1+delta_even).                        (4)

Both qualifications are necessary. For n=1, all labels are even with
probability 2^(-L); then s and s+Q/2 give identical states, and uniform-secret
success is at most 1/2. Fixed L cannot yield unconditional success tending
to one. More generally a binary rank deficiency n-r gives 2^(n-r) aliases.
If all supported digits are even, |b|=1 and these aliases remain even when
the public matrix has full binary rank. Rank selection alone is not enough.

## 6. Gaussian Scaling And Charged Errors

Take amplitude width sigma and truncate to [-R,R]. For growing sigma with
negligible relative Gaussian tails, c2=(1+o(1))/sigma and h2=log(sigma)+o(1).
Let q=d^(a+o(1)), sigma=d^(b0+o(1)), with fixed a>b0>0 and b0<1. Choose
R=O(sigma*sqrt(log d)) large enough for the desired tail accuracy. Eventually
R<=d and 2R<=q-1, and log(q)/h2 tends to a/b0.

For any fixed r>0, the finite condition

    L >= 2*(n+r+1)*log(q)/h2

ensures beta>=r+1 and T<=(2d)^(-r)/r. A constant integer L with strict
asymptotic margin therefore suffices. For odd q, also impose G. Gaussian
digit parity is bounded away from one, giving exponential decay in the
parity term; negligible truncation preserves that fact. n is constant here.

A FIXED L gives a chosen inverse-polynomial exponent, not negligible error
at every exponent. The gap between the converse threshold L>=a*n/b0 and
this conservative sufficient count is not a sharp threshold theorem.

ADVERSARIAL FOLLOW-UP: `research/STRUCTURED_EDCP_LOCAL_READOUT_BASELINE.md`
shows that local Fourier readout plus unrestricted CLASSICAL decoding is
also constant-block information-sufficient when a>b0+1/2. Thus this bound
is not evidence that collective entangling measurement is necessary. Both
efficient classical decoding and efficient joint quantum decoding remain open.

For the original untruncated product amplitudes, a per-block tail bound is

    eta <= d*sigma^2/(2*pi*R) * exp(-2*pi*R^2/sigma^2).

With independent blocks, all L truncate with probability at least 1-L*eta;
their untruncated and normalized truncated states have trace distance at most
sqrt(L*eta). A physical support projection followed by the ideal measurement
loses at most L*eta in unconditional success. A comparison of full and
truncated OPTIMAL successes instead uses the trace-distance bound. These
are different error statements; do not equate probability mass and distance.
Add joint source error and measurement implementation error separately.
If only an unconditional source-distance bound is known, conditioning on a
selection event can amplify it; a per-accepted-batch bound is required.

The following are evaluations of analytic bounds using 80-digit arithmetic,
NOT quantum simulations. n=1, L=40, sigma=sqrt(d), and the chosen tail target
is d^(-8). The last column bounds mean ideal failure after G when q is odd.

| d | q | R | Mean Failure Bound |
|---:|---:|---:|---:|
| 64 | 4096 | 21 | 1.58946e-7 |
| 64 | 4097 | 21 | 3.18134e-7 |
| 256 | 65536 | 48 | 2.48353e-9 |
| 256 | 65537 | 48 | 4.96728e-9 |
| 1024 | 1048576 | 107 | 3.88052e-11 |
| 1024 | 1048577 | 107 | 7.76105e-11 |

The corresponding per-block tail bounds are 4.88821e-18, 6.00185e-23 and
4.82802e-28. These q choices are ensemble examples, not asserted valid
cryptographic reduction parameters. In the same q=d^2 regime, the untruncated
two-block converse has log10 success upper bounds approximately -96.33,
-539.45 and -2774.29 at those three d values. Adding blocks is essential
for this full uniform-secret task, not a cosmetic parameter sweep.

## 7. Source Parameter Audit: Compatible Exponents, Not A Verified Reduction

Theorem 4 of Wen-Zheng, pages 44-45, has an explicit width/sample inequality.
Writing its Gaussian amplitude parameter as r_src, the displayed inequality is

    (3+r_src*sqrt(kappa_sec)*c_prime*d*(sqrt(2)+2/q))
       * (q^d-1)/(q-1) <= Q^(1-n/m_prime)/(4*m_prime*ell*C),
    c_prime = 2+c_max+2*m*r1*r2*d^2*sqrt(kappa_sec),
    c_max = 3*r1_prime*sqrt(kappa_sec)*n^2+18*n+11/2,
    r2 >= 2*d*q^(n/m+2/(d*m)).

These formulas were checked visually against the PDF, not inferred from
garbled text extraction. The local compatibility calculation is as follows.
Let kappa_sec=d tend through powers of two, n fixed, C=8, ell=L fixed,
m=ceil(log d), m_prime=ceil(d*log q), r1=r1_prime=ceil(sqrt(d)), and
r_src=sqrt(d). Take a prime q between d^12 and 2*d^12 and r2 at its lower
bound. Such primes exist; the resulting odd primes are unramified in this
power-of-two cyclotomic field. Their prime-ideal norms are at least q, so
the theorem's stated norm-growth condition is satisfied asymptotically.
The smoothing condition also holds, for example with error exp(-sqrt(d)).

Our calculation gives

    r2=Theta_n(d),     c_prime=O_n(d^4*log d),
    (left side)/(right side)=O_n(L*d^7*(log d)^2/q)=o(1).

Here Q^(n/m_prime)=O_n(1). Thus the DISPLAYED parameter conditions have
room for a polynomially growing coefficient width and constant block count;
there is no exponent-level incompatibility with the information theorem.
This deliberately large polynomial modulus is not a standardized parameter
set and has not been assigned a classical security estimate.

Width convention still needs resolution: Definition 10 on page 19 defines
D_r proportional to rho_r=exp(-pi*||c||^2/r^2). Definition 22 on page 28
uses sqrt(D_r), so its amplitude width in THIS note is sigma=sqrt(2)*r.
Equation (26) on page 45 instead displays amplitude rho_r, giving sigma=r.
Both scalings fit our information theorem, but their exact distributions are
different. Do not silently identify them or claim this discrepancy refutes
the reduction; track the rescaling through the source construction.

As a finite check of the DISPLAYED inequality alone, set n=1,L=288 and
q=nextprime(d^12), as returned by SymPy, at d=64,256,1024. An upper bound
on the ratio of its sides was 972.603, 3.67764 and 0.0108546, respectively.
The first two do NOT pass. The last does, but this is not a certified
primality transcript or full verification of the source theorem. The ratio
was evaluated in log space without constructing Q-sized objects; omitted
log(1-q^(-d))-(1-n/m_prime)*log(1+q^(-d)) terms are strictly negative.

The theorem also supplies a nonuniform secret prior. The covariant sufficient
measurement succeeds equally for that prior, but our uniform-prior converse
need not constrain a prior-adapted algorithm. CORRECTION from the later source
audit: on a COMMON success event, marginal errors epsilon_i against specified
PURE targets imply joint product trace error <=sqrt(sum_i epsilon_i).
Independence is not a further premise there. Mixed marginal closeness or
separate constant-probability success events do not suffice.

`research/STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md` now gives a scoped repair
of the LAST source stage: a finite randomized grid, composite-modulus matrix
separation, and an unheralded clean product component of explicit weight.
It tracks joint truncation and preparation errors without assuming normalized
postselection is contractive. Its stronger margin condition is asymptotically
compatible with this regime. The subsequent
`research/STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md` gives a scoped local repair
of the upstream stage, with explicit mixing and carry bounds. Independent
review, the reverse reduction and precise hardness implications remain open;
these local derivations are not an independently verified source theorem.

## 8. Exact Checks And Premise Counterexamples

Integer weights on digits (-1,0,1) tested (1) with rational arithmetic by
enumerating EVERY label matrix in the following ensembles. These weights
are verification controls, not new oracle-problem proposals.

| q,d,n,L | Digit Weights | Label Matrices | Exact Mean chi2 |
|---|---|---:|---:|
| 3,2,1,1 | 1,2,1 | 10 | 15/8 |
| 3,2,1,2 | 1,2,1 | 100 | 253/512 |
| 3,2,1,3 | 1,2,1 | 1000 | 5559/32768 |
| 3,2,2,1 | 1,2,1 | 100 | 33/2 |
| 3,2,2,2 | 1,2,1 | 10000 | 405/128 |
| 5,2,1,2 | 1,4,1 | 676 | 23045/13122 |
| 8,2,1,2 | 1,2,1 | 4225 | 173/128 |
| 4,2,1,2 | 1,2,1 | 289 | 81/256 |

All 16400 matrices passed the identity. Exact binary-rank proportions matched
p_G; every conditional moment satisfied (4), with the exact odd-divisor sum
in place of T. For example, at q=3,d=2,n=1,L=3 the conditional chi2 is
9507/229376, below 2197/28672. Its mean optimal-reference success is
0.9905798567. The all-zero label matrix prevents a pointwise near-one claim.

At Q=65,n=1,L=2, the false prime-only formula gives 81/64 instead of
173/128. The proper divisor terms are genuinely needed.

Gaussian collision checks covered 108 parameter points: q in
{3,4,5,8,9,13,16,17}, d in {2,4,8}, R in {1,2}, and sigma in
{1.1,1.8,3.0}, retaining the support premises and (2R+1)^d<=7000.
All 210 odd-divisor checks satisfied (2); maximum rounding excess was
1.12e-16. This is floating-point corroboration, not the all-size proof.

Three exact uniform-digit controls deliberately broke a premise. Each
violated C_t<=c2^max(1,floor(log_q t)):

| Broken Premise | q,d,R,t | Actual C_t | Invalid Bound |
|---|---|---:|---:|
| d is a power of two | 24,3,3,5 | 23537/117649 | 1/7 |
| R<=d | 17,2,3,5 | 481/2401 | 1/7 |
| 2R<=q-1 | 4,2,2,17 | 41/625 | 1/25 |

An even-digit control at q=5,d=2, digits (-2,0,2), weights (1,2,1), and
full-rank label a=1 retained the exact s versus s+13 alias. A separate
exponential-identity check confirmed rho_r^2 is proportional to D_(r/sqrt(2)),
not D_r. No production tests, CLI runs, registry promotion, or compiled
joint quantum measurement were performed in this pass.

## 9. What This Does Not Solve

1. Flat output fibers are not efficient inverse fibers. Drawing coefficients
   from mu is easy, but rejection sampling a specified near-uniform v still
   costs about Q^n draws. The collision bound does not supply a sampler.
2. A dense table for P_A or its PGM is an exponential reference, not a decoder.
   The one-block carry chain does not survive arbitrary independent labels
   without a new mathematical argument.
3. Real Gaussian diagonalization does not preserve the integer coefficient
   lattice. A continuous Gaussian sampler is not the required quantum state.
4. No lower bound against all efficient joint measurements or classical
   attacks has been proved. Lattice decoding and local quantum measurements
   followed by classical inference remain required baselines.
5. A prior-adapted measurement may use fewer blocks than this uniform-secret
   analysis. That is a separate, source-relevant research direction.
6. The bounds and checks are local work awaiting independent scrutiny. They
   do not establish a discovery, formal verification, or literature novelty.

## 10. Division Of Work And Decisive Next Tests

MAIN MODEL: seek an actual joint-fiber operation or a different collective
measurement on natural labels, at an information-sufficient block count.
Keep two-block constructions only when they expose a composable operation
or exploit an explicitly specified prior. Audit whether ordinary local
Fourier readout reduces the same source to an already tractable classical
inference problem. Resolve source width and joint-state contracts before
making a lattice consequence. Tightening constants alone is low priority.

GEMINI: add a bounded-reference checker and analytic resource report; no
Q-sized tables in the scalable reporting path. Preserve equation (1), exact
rank probabilities, digit-parity bias, all three premise counterexamples,
and the prime-only failure as regression tests. Compute h2 and kappa from
one-dimensional digit weights, retain distinct probability-tail and
trace-distance fields, and mark all measurement-runtime fields unresolved.
Do not accept a speedup candidate from an information certificate.

Expose separate statuses for information sufficiency, decoder implementation,
classical baselines, source-parameter compatibility and verified reduction.
These are mathematical handoff requirements, not completed integration.
