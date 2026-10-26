# A classical sampler for the coalesced Fourier-side branch

**Status: proved algorithmic deduction, using the known polynomial-time
binary elliptic-curve point-counting algorithm.** No scalable point counter
is implemented or executed in this review. The algorithm below retains the
actual native field, points, target bits, source signs and complete decoder.
It samples the intermediate branch, not native witnesses.

## Exact rejection construction

Use the notation of EXACT_PATTERN_CHANNEL.md. Let a_m(e)=a_b(e) for
wt(e)<=w and zero otherwise; its squared norm is tau. Let M=|D| and

    Z = ||A a_m||².

The desired Fourier-side distribution, conditional on the full-list
herald, is

    Q(z) = |sum_(d in D) a_m(z-d)|²/(M Z).

Classically draw e from |a_b(e)|² conditioned on the ball and draw d
uniformly from D. Output the proposal z=d+e. Its distribution is

    R(z) = sum_(d in D) |a_m(z-d)|²/(M tau).

Run the complete radius-w decoder on z. It returns exactly those d with
nonzero possible a_m(z-d), possibly also some zero-amplitude terms. There
are at most P entries. Evaluate their SIGNED amplitudes and accept z with

    r(z) = |sum_d a_m(z-d)|² / [P sum_d |a_m(z-d)|²].       (1)

Cauchy–Schwarz proves 0<=r<=1. The denominator is nonzero on any proposal
of positive mass. Multiplying R by (1) gives

    R(z) r(z) = |sum_d a_m(z-d)|²/(M tau P).

Thus the acceptance probability is Z/(tau P), and the accepted z is
EXACTLY distributed as Q. By the relative norm theorem,

    Z/(tau P) >= (1-eta)/P.

This is polynomially bounded below in the audited native regime. The
source-ball conditioning costs 1/tau expected draws; tau is near one at
rate 1/8, and at least 1/2 in the boundary construction. All uniforms and
rejection clocks are charged. Independent finite caps retain ABORT and
have exponentially decreasing failure when scaled by these lower bounds.

The nonzero local source draw has a particularly simple exact clock.
Propose u uniformly in F_q and accept with probability W(u)^2/(8q), taking
W(0)=0. The Hasse bound gives W(u)^2<=8q, while Parseval gives
sum_u W(u)^2=q², so acceptance is exactly 1/8. Conditional on acceptance,
the law is W(u)^2/q², as required. Since 8q is a power of two, this local
Bernoulli comparison uses a fixed number n+3 of random bits and an integer
comparison. Signed point counts are still charged per proposal. The
separate rational rejection in (1) has the clock qualifications below.

## Amplitudes can be compared exactly without irrational arithmetic

For u!=0 let W(u) be the integer inverse-trace Walsh sum. The source has

    a_b(0)=1/sqrt(2),
    a_b(u)=(-1)^b W(u)/(sqrt(2) q).

For each decoded error e of weight k<=w define the integer

    T_e = (-1)^(sum_(i:e_i!=0) b_i)
          * q^(w-k) * product_(i:e_i!=0) W(e_i).

Then a_b(e)=2^(-N/2)*q^(-w)*T_e. The common factor cancels in (1), leaving

    r(z)=(sum_e T_e)²/[P sum_e T_e²].

The numerator and denominator have polynomial bit length O(nN+log P).
Exact integer rejection therefore suffices. The given-field elliptic-curve
identity W(u)=#E_u(F_q)-q supplies each signed integer in polynomial time;
u=0 is handled explicitly. Computing at most P*N such values per proposal,
the complete RS decoder, codeword generation, and integer arithmetic all
remain polynomial in the explicit input length. This uses the known
point-counting result already identified in the resident
RECIPROCAL_TRACE_SOURCE_ACCESS.md, not an exponential Walsh table.

A primary reference is [Ahmadi–Granger, An efficient deterministic test
for Kloosterman sum zeros](https://arxiv.org/pdf/1104.3882), Section 1
and Lemma 2.1. Their convention includes the extra 1: the curve
`y²+xy=x³+u` has `#E_u=q+W(u)` for nonzero u. Their discussion explicitly
identifies polynomial-time point counting; searching for a special Walsh
value is a different problem and is not required by this sampler.

Clock self-audit: exactness above is for the expected-time algorithm.
A generic runtime cap can bias the conditional output and must not be
silently discarded. In particular, running the nonzero source sampler
only after the nonzero coin flip favors zero when its clock aborts. One
can avoid that particular bias by always preparing the nonzero draw first
and only then flipping the zero/nonzero coin; its fixed-cap success event
is independent of the eventual symbol. The final rational rejection
still uses expected-time integer generation. A bounded implementation
can instead use a uniform binary fraction and compare it to r(z), aborting
if its fixed-precision interval straddles r(z). At precision B its abort
mass is at most 2^-B per comparison. Union bounds, followed by division
by the inverse-polynomial acceptance lower bound, give a prescribed TV
error. That bounded version is approximate conditional sampling with an
explicit ABORT outcome, not an exact fixed-time sampler.

## What this changes, and what it does not

It is too strong to say that classical source samples plus the decoder
cannot account for the probability law of coherent erasure. They CAN
sample that intermediate law by the signed rejection calculation above,
paying the same polynomial list-size overhead. A remaining quantum
sampling claim must include the final inverse Fourier readout.

This does NOT provide that readout. Fourier-transforming a classical
probability law is not Fourier-transforming the signed amplitude vector.
The native distribution after readout is concentrated on solutions and
has the exact pattern-channel form proved separately. Efficient samples
and point queries for Q do not themselves construct samples from it.
As a useful control, in the singleton protocol the entire Fourier-side
measurement law is exactly independent of b: the singleton mask and
|a_b|² are both independent of b. The final native fibers for different b
are disjoint. Sampling that intermediate law therefore cannot be confused
with simulating the later phase-sensitive quantum measurement. This is
not an oracle lower bound: a classical algorithm also has the explicit b
and may exploit the efficiently computable phases in some other way.

Self-attack: omitting negative Walsh signs makes (1) the wrong law;
using an incomplete list loses interference terms; assuming Z=1 silently
changes normalization. None of those shortcuts is used. A finite algebraic
control is the F_8,N=4,K=1,w=2 fixture: tau=11/16 and total list herald
25/64 imply rejection acceptance (25/64)/(11/16)=25/44. The formula pays
this probability, rather than treating the intermediate law as a free
sample. This arithmetic consistency check is not the general proof.

**Next decisive question:** can this explicit signed sample/query access,
together with the public RS structure, sample the final Fourier outputs
in polynomial time? The theorem above narrows that question but neither
answers it nor proves it hard. It is a concrete additional classical
capability, not a dequantization claim or a new generic sampling primitive.
