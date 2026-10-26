# A Constructive Classical Sampler And Its Rare-Event Failure

2026-10-22. Local derivation, external mathematical review pending.
This incorporates the separate review's CLASSICAL_SAMPLING.md and checks
its mixture directly. It strengthens the normalization bound, gives direct
truncated sampling without rare rejection, and identifies a precise window
where excellent TV accuracy does not preserve the full-witness event.
No full classical solver or quantum separation is established.

The latent-constraint approach is prior art: see
[Zhou et al., Appendix B](https://arxiv.org/html/2609.40345v1). Their random
XORSAT theorem is not an assumption here. The native specialization uses
the explicit inverse-trace root sampler and deterministic MDS projections.
The repository's LINEAR_ERASURE_PRANGE_DUALITY.md already audits related
mixtures. This is a concrete attack on the current relation, not a new
general sampler framework.

## Same Input, No Markov Chain

Let C_y={x:Hx=y} for the public scalar or odd-folded relation, and let f_i
be its balanced inverse-trace predicates with arbitrary target bits b_i.
The scalar relation has K field checks on N coordinates. The folded relation
has K scalar checks on sN scalar coordinates, grouped into N blocks. Put

    m = K                         (scalar),
    m = ceil(K/s)                 (folded),
    r0 = N-m.

Every set S of at most r0 predicate coordinates has uniform full-alphabet
projection from C_y. This follows by solving K Vandermonde pivot columns
outside the selected coordinates/blocks. In the folded case the unused
scalar columns number s(N-|S|)>=K; no E-linear code premise is used.
Consequently, with A_S={x in C_y:f_i(x_i)=b_i for all i in S},

    |A_S|/|C_y|=2^-|S|                       when |S|<=r0.       (1)

To sample A_S uniformly, draw independent uniform accepted values at S,
draw unrestricted values on the other free coordinates, and solve the
pivot system. Inverse trace has an explicit uniform root sampler: choose
a uniform trace-b hyperplane element u and return inv0(u). In a public
binary basis, fix one coordinate with nonzero trace to satisfy the trace
equation, using all other bits freely. This includes the zero value.
For folded blocks use the public extension-field hyperplane and the stated
primal coordinate basis. This is polynomial arithmetic, not a field table.

For arbitrary S, write |A_S|/|C_y|=2^-|S| lambda_S. The existing every-target
fiber bound |lambda_c-1|<=eta implies |lambda_S-1|<=eta by averaging over
the unspecified predicate bits. This avoids a new independence assumption.

## Exact Mixture And Better Normalization

For rational M>=1, the Gibbs weight is M^a(x), where a(x) is the number of
satisfied predicates. Expand it as

    M^a(x) = sum_S (M-1)^|S| 1[x in A_S].

Set p=(M-1)/(M+1), nu(S)=p^|S|(1-p)^(N-|S|), and

    t=Pr[Bin(N,p)<=r0], tau=1-t,
    Zbar = E_(S~nu) lambda_S.

The TRUE Gibbs joint mixture weights are nu(S)*lambda_S/Zbar, not nu(S).
On the tractable sets, lambda_S=1 exactly. Thus

    1-eta*tau <= Zbar <= 1+eta*tau,
    Zbar >= t > 0.

Draw nu conditioned on |S|<=r0 and then draw uniformly from A_S. Its output
law Q is exactly the true Gibbs joint law conditioned on the tractable event.
Marginalization cannot increase TV, so

    TV(Q,pi_M) <= (1+eta)*tau/(1+eta*tau).                    (2)

This is stronger than dividing by 1-eta, and remains valid for eta>=1.
The expression follows by bounding discarded joint mass by (1+eta)*tau
and using the EXACT tractable joint mass t. This is not an equality claim
for marginal TV; the finite audit checks the actual marginal distance.

## Rare Rejection Is Not Required

If M=a/b>=1 in lowest terms, the unnormalized truncated size probabilities
are the INTEGERS

    w_j=binom(N,j)*(a-b)^j*(2b)^(N-j),  0<=j<=r0.

Use one exact integer categorical draw, followed by a uniform subset of the
chosen size. These integers have O(N log(a+b)+N) bits. Computing the table
and drawing from it is polynomial in the input and temperature bit lengths,
even when t is exponentially small. It does not cost 1/t trials.

This corrects a possible misleading reading of the separate review: only
the OPTIONAL reject-untruncated-subsets implementation costs 1/t. The direct
truncated sampler stays efficient at M>=N; what fails there is fidelity to
the desired Gibbs law, not the ability to sample the truncated law.

Exact integer draws from fair bits have expected fewer than two rejection
rounds. Capping their elementary rejection loops adds an explicit ABORT
probability, bounded by a union bound; choose O(log(N/epsilon)) rounds for
total clock error <=epsilon and add epsilon to (2). Do not condition away
that error. A deterministic pseudorandom seed is a reproducibility control,
not the mathematical source of uniform random bits.

## Exact Native Success And A Witness-Blind Window

Let lambda_b=2^N |A_b|/|C_y| for the full target. Conditional on an active
set of size j<=r0, the full-witness probability is lambda_b*2^(j-N).
For ANY distribution on such sets followed by UNIFORM conditional draws,

    Pr[native witness] <= lambda_b*2^-m.                      (3)

This is attained by systematic accepted completion with j=r0. It is not a
bound on adaptive/nonuniform solvers, general Gibbs samplers, or all classical
algorithms. The truncated mixture does not outperform this known comparator.

More precisely let theta=(M-1)/M, h=Pr[Bin(N,theta)<=r0]. Then

    Q(A_b) = lambda_b*(M/(M+1))^N * h/t,
    pi_M(A_b) = lambda_b*(M/(M+1))^N / Zbar,
    Q(A_b)/pi_M(A_b) = Zbar*h/t                 if A_b nonempty. (4)

The tilt from p to theta is essential: active sets conditioned on a full
witness have different statistics from the unconditioned proposal. Exact
pointwise likelihood ratios also follow. For a point with a satisfied bits,

    Q(x)/pi_M(x) = (Zbar/t)*Pr[Bin(a,theta)<=r0].              (5)

Equivalently Q(x) is proportional to sum_(j<=r0) binom(a,j)(M-1)^j,
not M^a. The finite audit compares this polynomial directly with the actual
latent mixture and with the true Gibbs normalization.

At fixed effective rate R=m/N, tau is exponentially small whenever
M<(2-R)/R by a fixed margin. But h is exponentially small whenever M>1/R
by a fixed margin. There is therefore a nonempty witness-blind window:

    scalar R1/8:       8 < M < 15,
    folded R3/8:       8/3 < M < 13/3.

Throughout that window the classical sampler has exponentially small TV
error yet captures an exponentially vanishing FRACTION of the Gibbs native
event. Both native probabilities are themselves exponentially small, so
this is no contradiction. Polynomially many moderate-temperature samples
do not turn into a constant-success search algorithm.

The live rational certificates make this visible without native sampling.
At n61, scalar M10 has TV<=2^-68 but relative native-event capture<=2^-20;
folded M3 has TV<=2^-174 but capture<=2^-24. These are outward-rounded
mathematical upper bounds, not empirical failure rates or lower bounds
against other algorithms. Rounding of K and ceil(K/s) is included.

At M=N the ideal native probability is near exp(-1) when eta is negligible,
whereas (3) stays exponentially small. The event A_b alone gives a constant
TV lower bound. Direct truncated sampling does not solve the search task.

## Executable Scope And Falsifiers

theorems/native_latent_sampler.py supplies:

- Exact rational binomial/TV/success certificates at the scalar and folded
  n17/31/61 parameters, without enumerating native fields or solution fibers.
- Direct integer truncated-set sampling and scalar conditional completion
  using a caller-supplied public FLINT field, arbitrary public points/targets/
  syndrome, and fair random-bit access. It does not call a search oracle.
- A separate capped enumeration of actual native codewords for all target
  and syndrome choices of a small relation, comparing every probability,
  partition tilt, exact native event and the claimed TV envelope.

The scalar completion tests exhaust the random free choices and check each
conditional word appears exactly once, rather than accepting a noisy frequency
plot. They cover all target bits and all field syndromes in the fixture.
No native-size classical sampler or folded completion implementation ran.
The folded result here is an analytical specialization of its proven scalar-
projection property; a mechanical native pilot can be delegated separately.

Falsifiers: a native input violating a stated fiber envelope; a nonuniform
conditional root/pivot sampler; a hidden active-set normalization cost; or
a polynomial classical procedure for the near-complete active sets typical
at M>=N. The latter would be major constructive progress and would defeat
the present quantum-versus-specified-baseline comparison. Neither this
mixture's failure nor the earlier worst-start heat-bath obstruction excludes
such a procedure.

NEXT: attack near-complete conditioning or find a meaningful natural reduction.
Do not mistake another temperature or mask constant for a new algorithmic
direction. The full-list quantum primitive also has direct prior art, as
recorded in EXACT_PREDICATE_CHANNEL.md.
