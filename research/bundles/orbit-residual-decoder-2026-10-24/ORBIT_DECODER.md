# One Polynomial, Three Orbit Rows, And A Perfect-Search Candidate

2026-10-24. LOCAL UNREVIEWED DERIVATION. This uses the existing cubic-orbit
relation, not a speedup for the earlier paired/chain problem, and not a
claimed new general DQI framework. No quantum circuit or native output
polynomial was produced. No classical separation or novelty is established.

## Decision And Candidate Contract

The prior binary local-filter avenue now has an exact classical comparator.
The resident paired-residual note instead offers a constructive source and
decoder. IMPORTANT AUDIT CORRECTION: a late filename search located
`research/CUBIC_ORBIT_DECODER.md` and `theorems/cubic_orbit_decoder.py`.
They ALREADY supply the three-point source, general projective rank formula,
whole-cap guard, coherent Gauss-phase control and native classical portfolio.
Those are reproduced ingredients, NOT new contributions of this pass.
The actual addition is the all-satisfying truncated-source construction,
perfect-search consequence at R>2/3, and exact finite two-herald failure
ledger. The external decoder is a bounded replay/reference; integration
should reuse the existing decoder rather than introduce a duplicate
registry subsystem. The earlier audit missed this existing file.

Input: an odd prime p, m dividing p-1, an order-m root zeta, M disjoint
nonzero orbits (a_i, zeta*a_i, ..., zeta^(m-1)*a_i), and n=mK <= mM.
Each explicit public F_i subset F_p has size (p-1)/2. Public b_i,l are
nonzero for l<m-1. An output is ONE polynomial P of degree <n. Its score is

    S(P) = sum_i 1_F_i(P(zeta^(m-1)*a_i)
                        + sum_(l<m-1) b_i,l*P(zeta^l*a_i)^2).

The target here is S(P)=M. No extra output polynomial or quantum source
copy is supplied. Tables may be read classically and coherently, with their
O(Mp) input/preprocessing cost paid. There is no oracle-hardness claim.
Checking an output requires actual evaluation at all mM public points and
membership in the original tables, not a reduced or predicted score.

The prioritized case is m=3 with Q_i(x,y)=b_i*(x^2-nu*y^2), where nu is a
public nonsquare. It avoids the local affine-flat control described below.
This is still a designed problem. A natural-problem reduction is a major
missing obligation; without it, even an eventual advantage may be narrow.

## Local Source Law For Every Fixed Halfset

Use normalized Fourier coefficients, so sum_e |fhat(e)|^2=E_x|f(x)|^2.
Let rho=(p-1)/(2p) and h_i=(1_F_i-rho)/sqrt(rho(1-rho)). The states with
amplitudes 1 and h_i(x_last+Q_i(x_free)) in the uniform basis are orthonormal.
At frequencies (u_0,...,u_(m-2),v), the latter has coefficient

    hhat_i(v) * product_(l<m-1)
        [p^(-1) sum_x exp(2*pi*i*(v*b_i,l*x^2-u_l*x)/p)].

The v=0 branch vanishes since hhat_i(0)=0. At every v!=0 each quadratic
Gauss sum has magnitude sqrt(p), so

    |fhat_i(u,v)|^2 = |hhat_i(v)|^2 / p^(m-1).

Thus conditional on any allowed v, all m-1 free frequencies are independent
uniform field elements. This holds for EVERY fixed halfset. The v law is
not assumed uniform. A zero quadratic coefficient destroys the argument;
the tests include that countercontrol. Selected blocks have nonzero labels,
so different selected supports are disjoint in Fourier space.

## Source Preparation Without A Block-Alphabet Table

Prepare M logical qubits, each sqrt(rho)|0>+sqrt(1-rho)|1>. Coherently count
their Hamming weight, herald weight <=D, and uncompute the count. This
retains coherence between all permitted supports. The initial failure is

    tau = Pr[Bin(M,1-rho)>D].

On each block map the logical basis to the orthonormal uniform/h states:
prepare the last coordinate with amplitudes 1 or h_i; put the other m-1
coordinates in uniform states; apply the invertible triangular change
last -> last-Q_i(free). The logical flag must be consumed by this isometry,
not left as which-support garbage. Two explicit known columns can be
extended using a constant number of Householder/state-preparation routines.
Their classical table and rotation synthesis costs are polynomial in p and
precision. This uses scalar tables of size p, not a stored p^m block table.

Without the degree herald, the source amplitudes factor as

    sqrt(rho) + sqrt(1-rho)*h_i = 1_F_i / sqrt(rho).

It is exactly the normalized uniform-amplitude state on all ambient
satisfying assignments. The normalized truncated state has overlap
sqrt(1-tau) with that state and trace distance sqrt(tau). The support
weight law and discarded mass are exact, not a Monte Carlo estimate.

## Folding Is Only A Syndrome Permutation

Let e_i,l be an ambient Fourier label. The original single-polynomial
syndrome has n entries

    s_j = sum_(i,l) e_i,l*(a_i*zeta^l)^j,   0<=j<n.

Put z_i=a_i^m and

    e_tilde[h,i] = a_i^h * sum_l e_i,l*zeta^(lh).

Then s_(mj+h)=sum_i e_tilde[h,i]*z_i^j. These are m rows of K syndromes
with common block support. No extra measurement, state, or sample created
those rows. The inverse local fold is an invertible m-point Fourier map.

## Fixed-Last-Frequency Rank Bound

Choose a whole-ball decoder cap C>=D, with C<K. Write s=n-mC and assume
s>=D. At actual support size j<=D the stacked cap recurrence matrix factors
as W times a j-by-C Vandermonde matrix. After row permutation, column i is

    W_i = sum_(l<m-1) u_i,l V_s(a_i*zeta^l)
                            + v_i V_s(a_i*zeta^(m-1)),

where V_s(x)=(1,x,...,x^(s-1)). Fix the support and every v_i!=0. For a
nonzero kernel vector w with support T of size t, the free-node span has
rank r_t=min(s,(m-1)t); including the t last nodes gives rank min(s,mt).
Consequently the space of compatible last coefficients has dimension

    d_t = t-min(s,mt)+r_t.

Multiplication by the fixed nonzero v_i is invertible on the w coordinates.
There are at most (p^d_t-1)/(p-1) compatible projective full-support vectors.
For each, the free variables hit its specified right side with probability
p^(-r_t). Counting vectors with smaller support here only overcounts.
A union bound, then j<=D, gives the exact rational bound

    epsilon <= sum_(t=1)^D binom(D,t)
                     * (p^d_t-1)/((p-1)*p^r_t).

Every nonzero summand is at most binom(D,t)*p^(t-s)/(p-1), yielding

    epsilon <= min(1, (p+1)^D / ((p-1)*p^s)).

The same bound controls the coherent source's rejected Born mass: condition
on each support and v tuple, apply this uniform bound, then average. No
measurement of those tuples is needed. Allowing v_i=0 on a selected branch
is invalid; an exhaustive countercontrol demonstrates the failure.

At p=19,m=3,n=12,D=2,C=3, all 19^4 free assignments have failure fraction
18/19^3 for either tested nonzero v tuple, below the bound 20/19^3. This
finite check is not the proof of the general formula above.

## A Syndrome-Only Whole-Cap Uniqueness Certificate

`decode` receives only public geometry, cap, and syndrome rows. It computes
the cap-matrix rank d, solves the degree-d recurrence, requires exactly d
roots among the PUBLIC orbit nodes, solves the Vandermonde values, inverts
the fold, and replays every supplied syndrome. Inconsistency causes abstention.

Why this certifies uniqueness against the ENTIRE block ball <=C:
the verified degree-d locator has all monic degree-C multiples as solutions
to the cap recurrence. They form an affine space of dimension C-d, exactly
the solution-space dimension because the cap rank is d. Any competing
locator of degree <=C, padded by powers of X to degree C, also solves that
recurrence, so must contain the d verified nonzero roots. The union of its
support with the verified support therefore has size <=C<K. The public-node
Vandermonde is injective on that union; all additional values are zero.
The zero syndrome is handled separately by the same Vandermonde fact.

When W has full column rank j, cap rank is j and the procedure recovers the
true error. Neither the true support nor an oracle for uniqueness is used.
Competitor labels need not obey the source's v!=0 promise.

## The One-Extra-Block Guard And Perfect Search

Set C=D+1. Let G be accepted source labels (weight <=D) which the decoder
certifies unique throughout the whole ball <=C. Syndrome compression U is
an isometry on G. A single score term has Fourier support on one block.
For e in G and such a shift z, weight(e+z)<=D+1=C. If

    syndrome(e+z)=syndrome(e'),  e' in G,

whole-cap uniqueness forces e+z=e'. The local evaluation map has rank m,
so distinct within-block shifts do not introduce additional multiplicities.
Hence the normalized score operators have the exact compressed identity

    U^* O_target U = Pi_G O_source Pi_G.

Choose the Fourier/inverse-Fourier signs consistently with the displayed
syndrome; output negation can otherwise change the original predicates.
This identity transfers the first moment, NOT the full filter law or full
output distribution. A stored 13-point Vandermonde alias at p=19 shows why
uniqueness only within the source radius cannot be substituted for the guard.

Let b<=epsilon be rejected mass conditioned on source preparation. The
accepted source is within sqrt(b) of the truncated source. Both normalized
score operators lie in [0,1]. The target conditional mean is therefore at
least 1-sqrt(tau)-sqrt(epsilon). Since S is integer and <=M,

    Pr[S<M | both heralds succeed] <= M*(sqrt(tau)+sqrt(epsilon)).

Pay both failed heralds as failed attempts, with NO free rerolls. A
conservative bound on total one-attempt perfect-search failure is

    L = min(1, tau + M*(epsilon+sqrt(tau)+sqrt(epsilon))).

For any separately established full-circuit trace/TV error eta, replace
this by min(1,L+eta). Approximate rare-branch conditioning is not free.

For fixed m and R=n/(mM)>(m+1)/(2m), choose a constant delta with
1/2<delta<mR/(m+1), and D=floor(delta*M). Along the public orbit family,
tau decays exponentially in M and s-D grows linearly. The rank failure
decays as exp(-Omega(M log p)). Thus the ideal algorithm has perfect-search
success 1-o(1), for every promised fixed input, in time polynomial in the
explicit input size. For m=3 the sufficient rate is R>2/3.

The finite ledger uses p=12289, M=4096, n=9828, R=819/1024, D=2375,
C=2376 and s=2700. Exact integer/rational computation, with upward dyadic
rounding, gives tau<5.858e-25 and L<3.135e-9. The displayed epsilon ceiling
2^-256 is a reporting precision ceiling, not the actual much smaller
coarse rank bound. Neither this ledger nor the basis decoder run executes
the quantum algorithm or verifies a native polynomial witness.

## Adversarial Classical Checks And Why This May Fail

1. **Anisotropy is necessary but insufficient.** With m=3 and nonsquare nu,
   x^2-nu*y^2 has no nonzero zero. On a nonconstant affine line the residual
   is either nonconstant quadratic (image size (p+1)/2) or nonconstant
   linear (image size p). Neither fits inside a halfset of size (p-1)/2.
   This excludes a local flat, NOT a nonlinear or code-aware algorithm.
2. **Split and wider forms admit flats.** x^2-y^2 vanishes on (t,t).
   Every nondegenerate diagonal ternary form over F_p has a nonzero zero:
   the sets {a*x^2} and {-c-b*y^2} each have size (p+1)/2 and intersect.
   This constructs an isotropic vector with last coordinate 1 in O(p).
   Thus m>=4 admits local accepted lines. That is not itself a full global
   solver, but it makes an unqualified width sweep unjustified.
3. **Norm structure is public.** The chosen binary quadratic is the norm
   from F_(p^2). Norm-conic parametrization, polynomial identities, and
   nonlinear moves preserving existing predicates must be attacked. The
   absence of affine lines does not block these methods. The EXISTING
   cubic-orbit module already inverts a supplied polynomial norm by
   rescaling its coefficients and taking a polynomial square root. That
   does not find a norm satisfying the input halfsets. Do not repeat
   unrestricted norm factoring as if it were an untested attack.
4. **There is a cheap exact MQ reformulation.** Let H be a public parity
   check for the length-3M evaluation code, with r=3M-n rows. Pick t_i in
   F_i. Set the last value to t_i-b_i*(x_i^2-nu*y_i^2), and solve

       H*(x_1,y_1,t_1-b_1*(x_1^2-nu*y_1^2), ...,
          x_M,y_M,t_M-b_M*(x_M^2-nu*y_M^2))=0.

   This is r equations in 2M variables with diagonal quadratic parts plus
   linear terms, NOT a generic unknown MQ instance. Every solution gives
   the same required polynomial by interpolation and degree verification.
   Allowing t_i to move in F_i adds further freedom. General massively
   underdetermined MQ algorithms do not, from their stated thresholds
   alone, solve this constant variable/equation ratio. Their failure to
   apply is NOT hardness evidence. Structured MQ is a high-priority attack.
5. **A common quadratic radical survives.** Setting the first two orbit
   evaluations to zero leaves an n-2M dimensional linear polynomial
   subspace when n>2M. On it, all predicates become scalar linear
   membership constraints. This is another concrete baseline/reduction,
   not a proof it solves all original inputs. Affine cosets add more options.
6. **Information-set attacks remain.** Interpolate accepted triples on K
   blocks, then optimize the rest. Random-table remaining scores do not
   imply worst-case input hardness. The prior paired witnesses and its
   best score concern a DIFFERENT relation and cannot be reused here.
   The existing CUBIC portfolio, however, already reaches438/684 on THIS
   relation at p2053,n204. Reuse its intrinsic moves; that low-rate result
   does not test the high-rate perfect-search regime. At high rate many
   constraints can be pinned, so classical search may be much easier.
7. **Proof/implementation/novelty remain distinct.** The Gauss-sum law,
   collaborative decoding, DQI and truncated sources are known ideas.
   An error in the guarded identity, coherent flag cleanup, or rank union
   bound kills this derivation. A published specialization may subsume it.
   A polynomial classical perfect solver kills its advantage motivation
   even if the quantum proof is correct. No independent review of THIS
   result has occurred; the authorized Rees review concerns another proof.

## Resource Ledger And Literature Limits

The explicit table input is O(Mp) bits plus public field/code data.
Constructing roots/orbits can cost O(p) reference operations. Source tables,
rotation computation, and reversible lookup are paid, not hidden advice.
Syndrome computation, cap elimination, public root scans, Vandermonde solves,
replay and their reversible adjoints are polynomial in M,p,log p. A clean
implementation must reversibly record branch choices, compare decoded and
source labels, herald, erase the accepted source, and uncompute all work.
Prime-field QFTs, rotations and arithmetic need a total error budget eta.
This note supplies no optimized gate count, fault-tolerant estimate or
compiled reversible decoder. The reference caps are implementation limits,
not an asymptotic uniformity argument or a quantum execution claim.

Related primary sources checked:

- [Schmidt, Sidorenko and Bossert](https://arxiv.org/abs/cs/0610074):
  collaborative RS decoding is an established ingredient.
- [Yu and Loeliger](https://arxiv.org/abs/1612.07854): simultaneous partial
  inverses give established conditional beyond-half-distance decoding.
- [Shang and Stilck Franca](https://arxiv.org/html/2609.35101v1): the
  relative-decoding/nonlinear-source framework is prior work.
- [Kramer et al.](https://arxiv.org/html/2610.02145v1): stronger typical
  membership-oracle folded-DQI and exact-search results already exist.
  Their random block-oracle lower bound is not a hardness result for these
  public scalar halfsets or small-order structured blocks. The truncated
  source itself should not be advertised as a new paradigm.
- [Hashimoto](https://eprint.iacr.org/2009/154.pdf): general underdefined-MQ
  polynomial regimes involve many more variables than the constant-ratio
  formulation above. This comparison does not exclude specialized attacks.

Priority after this pass: first attack the exact structured MQ/norm problem,
then seek a natural-problem reduction or independent proof/novelty review.
Do not spend another pass adding family dashboards or optimizing a rank
benchmark while these scientific gaps remain unresolved.
