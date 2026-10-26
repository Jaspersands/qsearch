# Exact pattern-channel identity and relative norm bound

**Status: proved deduction in this review, not a novelty certification.**
This gives a simpler proof of native success for the paid full-list variant.
It also strengthens the absolute support-mask estimate to a relative one.
All algorithms below retain the original native input and its paid decoder.
Subsequent literature checking found the full-list operation in Jo,
Theorem 5.2, and a generic theorem already implying native quantum success
in Horinaga–Yamakawa, Theorem 5.1. See LITERATURE.md for links and the exact
substitution. This independent calculation must not be advertised as a
new interference or list-erasure primitive.

## Two orthogonal states per coordinate

Let f_i be balanced and chi_i(x)=(-1)^f_i(x). Write F for the normalized
additive field Fourier transform. Define

    phi_i,0 = F(q^(-1/2) * 1) = |0>,
    phi_i,1 = F(q^(-1/2) * chi_i).

Balance gives phi_i,1(0)=0. These are orthonormal states, and the Fourier
transform a_i,b of the uniform root state f_i=b is

    a_i,b = (phi_i,0 + (-1)^b phi_i,1)/sqrt(2).

For sigma in {0,1}^N let phi_sigma be the tensor product of these states.
Different sigma have disjoint zero/nonzero Fourier support patterns, so
they form an orthonormal basis of a 2^N-dimensional subspace W. Every
support-only mask of a balanced product source lies in W. This statement
does not hold for a general label-dependent mask.

Let R_c be the product uniform root state for the pattern c. The R_c form
an orthonormal basis of F^(-1)W, since their supports partition F_q^N.
Let C=D^perp, M=|D|, and A=M^(-1/2) sum_(d in D) T_d. Then

    F^(-1) A F = sqrt(M) Pi_C.

No claim is made that A is itself a free physical operation.

## Exact spectrum of the compressed Gram operator

Define A_c={x in C : f_i(x_i)=c_i for every i} and

    lambda_c = M * |A_c|/(q/2)^N.

Because the R_c have disjoint supports, compression of M*Pi_C to their
span is diagonal with diagonal entries lambda_c. Equivalently, the
compression of A^*A to W has exactly these eigenvalues, with eigenvectors
the Fourier transforms of R_c. Thus

    max_c |lambda_c-1| <= eta

implies, for EVERY v in W,

    (1-eta)||v||² <= ||A v||² <= (1+eta)||v||².       (1)

This is stronger than an additive eta bound for masks of a unit source.
It is an exact equivalence between uniform relative fiber counts and
near-isometry on this particular subspace, not an assertion on the entire
q^N-dimensional Hilbert space.

For the native inverse-trace problem the already reconstructed character
calculation supplies |lambda_c-1|<=E_D(beta) for every c, where
E_D(beta)=sum_(d!=0) beta^wt(d). The positive MDS enumerator bounds this
uniformly. Hence a tail of source mass delta has coherent squared norm
at most (1+eta)*delta, rather than delta+eta. No separate sign-stripping
or random-label hypothesis has been inserted.

## Exact full-list output, including all probabilities

Let m(sigma) be a support mask and define its normalized Boolean Fourier
coefficients

    k_m(t) = 2^(-N) sum_sigma m(sigma)*(-1)^(sigma dot t).

For the source targeting b, changing between the phi_sigma and R_c bases
is exactly an N-bit Hadamard transform. Therefore

    F^(-1) A(m a_b)
       = sqrt(M) Pi_C sum_c k_m(b+c) R_c.             (2)

This is an amplitude identity. In particular, after the paid fixed-P
complete-list projection described in QUANTUM_AUDIT.md,

    Pr[output pattern c AND list herald]
       = lambda_c * |k_m(b+c)|²/P.                  (3)

The formula includes the probability of the weight projection and the
list projection. It is not conditioned on either herald.

For the Hamming ball m(sigma)=1_(|sigma|<=w), put

    tau=2^(-N) sum_(j=0)^w binom(N,j)=1-delta.

Then k_m(0)=tau, giving the exact native success identity

    Pr[fully native-valid AND list herald]
       = lambda_b * tau²/P.                         (4)

Consequently the sufficient bound is (1-eta)*(1-delta)²/P when eta<1.
The total herald probability is sum_c lambda_c*k_m(b+c)²/P and lies
between (1-eta)*tau/P and (1+eta)*tau/P by Parseval and (1).
Subtracting (4) gives an exact invalid-output mass, not an uncharged
normalization error.

Conditional on native success, every x in A_b has the SAME amplitude
and hence the output is EXACTLY uniform over A_b in the ideal model.
Verification followed by independent restarts is thus an exact uniform
native witness sampler in expected polynomial time whenever the success
lower bound is inverse polynomial. A finite restart cap keeps ABORT as an
outcome; conditional on a non-aborted answer it remains exactly uniform.

## What assumptions are actually necessary

For full-list native success, equation (4) needs balanced root preparation,
complete bounded list decoding, the fixed paid projection, and a lower bound
on lambda_b. It does NOT need a separate coherent-tail estimate, a uniform
bound on every lambda_c, or a rare-ambiguity/point-mass premise. The broader
fiber estimate is useful for (1) and total-channel bounds, but a lower bound
on the target fiber already establishes native success via (4).

In this repository, inverse-trace character sums establish lambda_b=1+o(1)
for every target, and ordinary RS at fixed R<1/4 gives tau=1-o(1) and
constant P. All arithmetic and list work remain polynomial in log(q),N.
Thus this supplies an alternative unconditional ideal quantum proof for
the SAME relation, not an easier supplied-density-oracle problem.

The matched systematic-root sampler has success lambda_b*2^-K.
The ratio of these two success probabilities per attempt is exactly
2^K*tau²/P. This compares two specified proposals only; it does not bound
all classical algorithms or pay away their different per-attempt costs.

## Self-attack and a targeted finite falsifier

For F_8,N=4,K=1,w=2,b=(0,1,0,1), our separate native count gives |A_b|=40,
so lambda_b=5/4. Here tau=11/16 and P=2. Equation (4) predicts

    (5/4)*(11/16)^2/2 = 605/2048,

exactly the register-level channel fixture in the newly reviewed shared
note. This one check is a falsifier for normalization mistakes, not the
proof of (1)–(4), which is the orthogonal-basis calculation above.

The strongest falsifier is an accepted full-list branch whose amplitudes
depend on more than the final Boolean predicate pattern. This occurs if
the list normalization varies with z, the decoder is incomplete, or a
message/index record survives. None is allowed in the audited protocol.
A label-dependent singleton mask need not satisfy (2); the older singleton
analysis still uses its distinct ambiguity argument. There is no extension
from finite tests to arbitrary masks or arbitrary dirty implementations.

The identity makes the claimed incremental novelty narrower: it connects
the balanced-mask argument directly to the known fiber-count calculation
and the usual DQI Boolean Fourier filter. Prior-art comparison must check
this formulation and the paid full-list operation; absence of the exact
notation in a selected paper is not a novelty result.

## Direct truncated-source preparation and the exact coefficient optimum

**Later proved refinement, not a correction to (4).** Formula (4) counts
starting from the untruncated product state and measuring its weight flag.
If the normalized truncated state is prepared directly, the native success
per prepared source is instead lambda_b*tau/P. The original tau^2 formula
remains correct for its specified protocol.

This normalization need not cost 1/tau retries. Let
B_w=sum_(j=0)^w binom(N,j), so tau=B_w/2^N. Prepare a uniform integer
in {0,...,B_w-1} by Hadamards on ceil(log2 B_w) bits and rejection of
out-of-range integers. Acceptance is at least 1/2. Reversibly unrank the
integer to a binary string sigma of weight at most w, then erase the
integer by computing its rank. Binomial coefficients have O(N) bits and
ranking/unranking uses polynomially many bit operations. Thus this gives
an exact uniform superposition on the Hamming ball in expected polynomial
time, with failure at most 2^(-R) after R capped preparation attempts.

Apply phase (-1)^(b dot sigma). Controlled on each sigma_i, prepare
phi_i,0=|0> or phi_i,1=F(q^(-1/2)*(-1)^f_i). The latter uses uniform
field Hadamards, reversible predicate phase evaluation, and the additive
field Fourier transform, all exact in the binary ideal circuit model.
Balance makes its zero-frequency amplitude exactly zero. Therefore sigma
is recoverable as the zero/nonzero support of the error registers and can
be uncomputed cleanly. The resulting source is

    v_b = B_w^(-1/2) sum_(|sigma|<=w) (-1)^(b dot sigma) phi_sigma.

The same fixed-P list operation now gives lambda_b*tau/P native success,
exact conditional uniformity, and no residual support-label register.
This is a standard DQI-style support-state preparation; Jo's Proposition
6.2 already gives the general controlled support/Fourier-state approach.
No novel source-preparation primitive is claimed.

There is also an exact coefficient bound within this specified family.
For any normalized v=sum_(sigma in S) c_sigma*phi_sigma, the native
probability after the same paid list map is

    lambda_b/(P*2^N) * |sum_(sigma in S) c_sigma*(-1)^(b dot sigma)|^2
       <= lambda_b*|S|/(P*2^N).

Cauchy--Schwarz proves the inequality. The equal-magnitude, phase-aligned
coefficients above attain it when S is the Hamming ball. Thus optimizing
only these support coefficients cannot remove the remaining ball-mass
factor tau. This is not a lower bound on other quantum algorithms, on
label-dependent sources, or on different decoding/projection mechanisms.

Self-attack: keeping sigma after source preparation would destroy the
required interference; erasing it relies on the exact zero-frequency
cancellation, not an approximate support assertion. Treating a uniform
integer in an exponentially large range as a table would also be wrong:
its binary length is O(N), and the ranking computations above are explicit.
At native rate 1/8, tau=1-o(1), so this refinement changes neither the
polynomial conclusion nor the classical-advantage assessment.
