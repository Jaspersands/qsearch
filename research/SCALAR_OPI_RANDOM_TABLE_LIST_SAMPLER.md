# Native Random-Table OPI: Paid List-Erasure Normalization

2026-11-05. Local derivation, independently reviewed. This composes
known DQI/list-sampling machinery; it is not a novelty or separation claim.
No quantum implementation or new classical experiment is supplied.
Review: audits/reviews/2026-11-05-scalar-opi-random-table-list-review.md.
It accepted the second moment, source quantifier, all-field Fourier/list
composition, score and perfect-witness corollary after making the Fourier
convention and global retry/precision budget explicit. No numerical
control is being represented as a proof of the asymptotic statements.

## Question, source, and prior work

Can the known complete-list DQI sampler be justified on the EXACT binary
random-table source, without importing a prime-field score theorem?

The input is q=2^t, m=q-1 distinct nonzero field evaluation points,
k=floor(Rm), fixed R in (0,1), an effective public field presentation, and
independent uniformly random q/2-element sets S_i, supplied as FULL tables.
Output a polynomial P of degree <k maximizing the fraction of accepted
evaluations; verification is ordinary field Horner evaluation and lookup.
Let C be this [m,k] Reed-Solomon code. Put h_i=2*1_{S_i}-1 and
h(c)=(h_i(c_i))_i. This note does not change any saved input or comparator.

The corpus lookup recovered the earlier Jo list-erasure audit in
SCALAR_OPI_SOFT_DECODING.md. Its refusal to import the prime-field theorem
was appropriate. The missing source-specific normalization can instead be
proved directly below. The mechanism itself is already in
[Jo, Sections 3-6](https://arxiv.org/html/2607.16541): complete syndrome
lists, canonical indexing, a GLOBAL padded length L, and a uniform-index
projection with probability Z/(L Z0). Its Fourier and indexing identities
extend by the trace character to binary extension fields; we give the
needed preparation and source argument rather than invoke its prime-field
main theorem.

[Sun--Wootters, Theorem 1.9 and Section 6](https://arxiv.org/html/2610.12357)
give stronger capacity-based prime-field results. Their Theorems 2.2-2.3
are explicitly prime-field statements. That is not a capacity decoder for
the present binary-field code. Here only the all-finite-field Johnson
decoder and its explicit list bound are used (Jo Theorem 4.2/Lemma 4.4).
The primary decoder source is
[Chatterjee--Harsha--Kumar, Theorem 1.1 and Section 3](https://arxiv.org/html/2511.05176).
Its theorem covers every finite field. Section 3 explicitly uses
deterministic factorization with sqrt(characteristic) dependence in small
characteristic; characteristic two does not need the large-characteristic
Hensel-lifting argument. The input-size convention here would also permit
polynomial q dependence. Thus this dependency is not an unverified
prime-to-extension-field transfer.
The standard soft-decoding predecessor is
[Chailloux--Tillich](https://arxiv.org/html/2411.12553); its perfect-search
results are not evidence of a new primitive here.
More specifically, [Chailloux, OPI x Soft Decoders, Theorem 3](https://arxiv.org/html/2511.22691)
already gives the same Johnson score curve via soft decoding. Its Section
4.2 states a prime/full-support setting, and Definition 3 measures success
averaged over the supplied random syndrome. Neither the curve nor the
decoding-to-search mechanism is new. The present proof certifies the
original binary IID full-table source with a high-probability INSTANCE
event and paid success on each good instance. It does not convert a bare
average inverse-polynomial success assertion into a per-instance guarantee.

Local source PDFs and extracted text are in audits/sources/opi_random_tables/:
jo_2607_16541.pdf SHA256
bf815612f36916d97f6a342f88ef7a81a11ce7b291250428ed038139ff368293;
sun_wootters_2610_12357.pdf SHA256
ea9daf6590afcc3b0e253d5ff607aa6fca88155862c6980abf018f67b4499364.
chk_2511_05176.pdf SHA256
b572a354132d9678da0f8951d67e41f44e8c2b7f90e913fdf8fb189cf4859e31.
chailloux_2511_22691.pdf SHA256
82c99a08575dd5342ec62c3af7adb43550a5ae6f800ba663d3fc25cbe50e1465.
Retrieved 2026-11-05. These are source snapshots, not independently verified
implementations of their algorithms.

## Exact second moment for ALL bit-pattern counts

For b in {+1,-1}^m, let N_b=|{c in C:h(c)=b}|, mu=q^k/2^m,
and p_b=N_b/q^k. Write chi2=2^m sum_b p_b^2-1. For q>2 set
r=(q-2)/(q-1), a=q/(q-1). Then EXACTLY

    E_S chi2 = sum_{j=k+1}^m binom(m,j) r^(m-j) a^j (q^(-k)-q^(-j))
             <= 2^m/q^k.                                      (1)

Proof. For two symbols at a fixed row, the random balanced table gives the
same bit with probability 1 if equal and r/2 if distinct. Average over
uniform c,c' in C. Their difference D is uniform in C, so if z(D) counts
zero coordinates,

    E_S(chi2+1)=E_D 2^z(D) r^(m-z(D))
               =sum_{J subset [m]} r^(m-|J|) a^|J| Pr[D_J=0].

The MDS evaluation map has rank min(|J|,k), hence that probability is
q^(-min(|J|,k)). Replacing it by q^(-|J|) gives
(r+a/q)^m=1. Subtract this identity; only |J|>k remains, proving equality
in (1). Every remaining summand is nonnegative, and their sum is bounded
by q^(-k)(r+a)^m=2^m/q^k. No independence of all codeword evaluations was
assumed.

Since chi2=2^(-m) sum_b(N_b/mu-1)^2, Markov gives, for every delta>0,

    Pr_S[exists b: |N_b/mu-1|>delta] <= 4^m/(delta^2 q^k).       (2)

Thus with q=m+1 and fixed positive R, choose
delta_m=(4^m/q^k)^(1/4). Eventually delta_m<1, and with probability at least
1-delta_m^2, EVERY bit pattern has relative count error <=delta_m.
Both errors decay exp(-Omega(m log m)). The event concerns the one supplied
table instance. Repeated coherent runs reuse that same instance; no fresh
table law is introduced between queries or attempts.

This is a count statement, not an efficient classical conditional-count
oracle, inverse sampler, or finder. In particular it does not provide the
number of witnesses extending a partially assigned coefficient vector.

## A known sampler with this normalization paid

Choose 0<alpha<min(1/2,1-sqrt(1-R)), a fixed margin. Set ell=floor(alpha*m)
and w=floor(log m), eventually w<ell. Define the orthonormal Boolean shells

    phi_j(b)=binom(m,j)^(-1/2) sum_{|T|=j} product_{i in T} b_i,
    F(b)=(w+1)^(-1/2) sum_{j=ell-w}^ell phi_j(b).

Under uniform b, E F^2=1. On the event (2),

    Z:=E_{c in C} F(h(c))^2 is in [1-delta_m,1+delta_m].       (3)

Indeed the all-pattern bound applies to every nonnegative weight F(b)^2.
It also implies that the law of h(c), when c is weighted by F(h(c))^2,
has total variation distance at most delta_m/(1-delta_m) from the uniform
Boolean law weighted by F(b)^2. This implication remains true for any
chosen nonzero weighting; it does not supply a way to implement it.

Here implementation is the existing complete-list construction. Define
hat(h_i)(y)=q^(-1) sum_x h_i(x)*(-1)^Tr(x*y), where Tr is the absolute
field trace. These are the Fourier coefficients of h_i, equivalently the
quantum Fourier amplitudes of h_i/sqrt(q), not the unitary transform of
the unnormalized function. Write

    A_y = product_{i:y_i!=0} hat(h_i)(y_i)
          /sqrt((w+1)*binom(m,wt(y)))

on weights ell-w,...,ell, and zero otherwise. Balancedness gives
hat(h_i)(0)=0 and sum_x |hat(h_i)(x)|^2=1, hence sum_y |A_y|^2=Z0=1.
Let B generate C and H=B^T. Prepare sum_y A_y |y>|Hy>.

For each syndrome s, choose a PUBLIC linear right inverse r_s of H, and
list decode the generalized RS code C^perp centered at r_s. Its dimension
is m-k and distance k+1. The finite sufficient condition is

    u:=m-ell > sqrt(m*(m-k-1)).                              (4)

After shell filtering, this gives exactly all y with Hy=s and A_y!=0
(including possible zero-amplitude members harmlessly). The number of
all radius-ell candidates is bounded uniformly over s by

    J=(u-(m-k-1))/(u^2/m-(m-k-1)) <= m^2.                    (5)

Use L=2^ceil(log2(max(1,ceil(J)))), computed from public parameters, for
every syndrome, including empty lists. Canonical indexing is reversible;
project its globally padded index onto |+_L>. The unnormalized syndrome
amplitude is L^(-1/2) sum_{Hy=s} A_y. Field-character orthogonality gives
flagged success Z/L, and the inverse trace Fourier transform gives exactly
the distribution proportional to F(h(Bz))^2 on z in Fq^k in the ideal
circuit. No per-list normalization, hidden inverse, or omitted failure
branch occurs. At a fixed Johnson margin J=O_R,alpha(1), so the success
probability is bounded below by a positive constant on (2).

All data access is charged. A known full table compiles into a reversible
membership/phase circuit with polynomial mq log q cost; this conservative
bound needs no QRAM. Uniform field states and the trace QFT use Hadamards
and a computable basis change. The phase h_i produces its local Fourier
state exactly before gate-synthesis issues. Controlled versions exist
because the entire public table circuit is known. Uniform shell/subset
preparation, syndrome arithmetic, deterministic complete GS decoding,
sorting/indexing and their inverses have polynomial cost and workspace in
the full input length. The all-finite-field deterministic decoder stated
in Jo Theorem 4.2 suffices; even polynomial dependence on q is legal here.
For S requested flagged draws and delta_m<=1/2, cap attempts per draw at
A=ceil(2L*log(4S/eta)). Each attempt succeeds with probability at least
1/(2L), so the union of all draw-aborts has probability <=eta/4. Synthesize
all approximate operations so the sum of operator errors over the ENTIRE
bounded S*A-attempt circuit is <=eta/4. The unconditioned hybrid bound then
controls the final output law, including aborts; no conditional-error or
per-sample failure budget is silently reused. This gives bounded-clock
polynomial time, not an unbounded expected retry assertion. Native output
verification is retained.

## Score and end-to-end consequence

Let s(b)=(m+sum_i b_i)/(2m). The identity

    (sum_i b_i) phi_j = sqrt((j+1)(m-j))*phi_(j+1)
                       +sqrt(j(m-j+1))*phi_(j-1)

gives the EXACT ambient weighted mean

    beta_m=1/2 + [1/(m*(w+1))]
                    sum_{j=ell-w}^{ell-1} sqrt((j+1)*(m-j)).   (6)

On (2), the sampler mean differs by at most delta_m/(1-delta_m).
Since w tends to infinity and w/m tends to zero, the limiting mean is
1/2+sqrt(alpha*(1-alpha)). For every fixed R in (0,1) and epsilon>0,
choose a fixed alpha below the Johnson cutoff (and below 1/2) sufficiently
close to it. Repetition, verification, and keeping the best sample gives
with high probability a score at least

    beta_J(R)-epsilon,
    beta_J(R)=1/2+sqrt(a_J*(1-a_J)),
    a_J=min(1/2,1-sqrt(1-R)).                                (7)

To justify the success quantifier, if a [0,1]-valued score has mean at least
beta_J-epsilon/2, its probability of exceeding beta_J-epsilon is at least
epsilon/2. S=ceil((2/epsilon)*log(4/eta)) successfully flagged samples give
score-failure probability <=eta/4. Together with the global abort and
precision budgets above, total algorithmic failure is <eta. Epsilon is
fixed, and the decoder's fixed margin may depend on it. This
holds for all sufficiently large m on a set of original source instances
of probability 1-exp(-Omega(m log m)); it is not a worst-case table theorem.

At R=1/4, (7) is about 0.840625, compared with the old unique-decoding
limit 0.830719 and one-shot Prange 0.625. This is a stronger asymptotic
quantum benchmark, not a recomputation of the finite saved DQI scores.
Published systematic line search/annealing and the retained Algorithm H
remain the actual classical competitors. No classical upper bound follows
from Prange's expectation or the failed q512 Algorithm H persistence test.

For fixed R>3/4 one may instead take ell=floor(m/2). Condition (4) still
has a fixed margin. On the all-positive Boolean pattern,
F(1)^2=(sum_{j=ell-w}^ell sqrt(binom(m,j)))^2/(w+1), so
2^(-m) F(1)^2=Theta((w+1)/sqrt(m)). Equation (2) transfers this probability
up to a 1+o(1) factor. Polynomially many flagged samples therefore FIND
an exactly perfect native witness with high probability. This is a
source-specific composition of existing mechanisms, not a claim of a new
perfect-search algorithm or an improvement over all prior literature.

## Falsifiers, remaining question, and stop rule

The decisive checks are (1)'s balanced-pair probability and MDS ranks,
the GLOBAL nature of (2), the trace-pairing convention, complete rather
than single-output decoding, and the L^{-1/2} projection normalization.
An explicit worst-case falsifier chooses a full-support y in C^perp
(the generalized RS multiplier vector suffices) and sets
S_i={x:Tr(y_i*x)=0}. These are balanced, but product_i h_i(c_i)=1 for
every c in C, so every odd-parity pattern has zero preimages. Thus a
worst-case extension of the all-pattern count theorem is false.
Correlated/nonuniform tables, fixed worst-case sets, compact predicates,
and a capacity decoder in characteristic two are outside the proof.
Counts, finite controls, and this quantum upper bound prove no classical
hardness, speedup, novelty, or advantage at a particular finite size.

The single substantive unresolved comparison remains a polynomial-time
classical algorithm for the full random tables versus the achievable
quantum score, now with (7) as a stronger source-correct comparator.
No new classical operation was found in this pass's independent review;
constant-block/tie-rule variants and more Algorithm H sizes are not
justified. Do not build a decoder scaffold or simulator for known list
erasure. A new operation or a new source-correct theorem is required.
