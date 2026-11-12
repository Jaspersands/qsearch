# Independent upside selection: forced lattice Helmholtz sampling

2026-11-13. SELECTION AND SCOPED ALGEBRAIC CHECKS, not an algorithm admission,
novelty assessment, hardness claim, or source-theorem certification. Only this
file was edited. No network, Git, paid API, numerical sweep, or implementation.

## Decision and exact next question

Select **full spatial Born sampling for a damped, forced lattice Helmholtz
equation with explicit sparse sources**. This is a new endpoint in the corpus,
has a direct wave-interference interpretation, and contains a sharply exposed
operation that could support a substantial algorithmic gain. The operation is
not preparation of a resonant shell: it is normalization and coherent assembly
of the ENTIRE forced field, including its off-resonant part, for arbitrary
signed/complex sources.

Let L=2^n, n>=3, on the periodic two-dimensional grid Z_L^2. Define the positive
nearest-neighbour Laplacian Delta with Fourier eigenvalue

    lambda(k)=4-2 cos(2 pi k_x/L)-2 cos(2 pi k_y/L),
    B=I-Delta,  A=B+i/L.

Native input is n and m explicitly listed grid points with rational complex
weights of total bit length B_in. Combine duplicate points exactly and reject
the zero forcing. Let f=sum_j c_j delta_(x_j), u=A^(-1)f. Output a grid point
within TV epsilon of |u(x)|^2/||u||^2. The proposed quantum target is
poly(n,m,B_in,1/epsilon) BIT/gate cost, with no supplied Green-state, ring
sampler, normalization, source-success promise, or spectral oracle. This is
a periodic damped problem; no identification with a continuum outgoing
boundary condition is assumed.

The precise paid question is: **can a native multiscale resolvent compiler
achieve that bound uniformly over these sources, or does a classical full
spatial sampler achieve the same bound first?** A source-dependent condition
number or postselection probability must be shown polynomial on this input
class, not silently made an extra promise. Generic linear-system machinery
pays a condition number of order L here and therefore does not answer it.

The small damping is intentional. Replacing 1/L by an inverse polynomial in
n can make locality/truncation a powerful classical attack in fixed physical
dimension; that easier regime is not evidence for this target.

## Three independent directions compared

1. **Forced wave-field sampling -- selected.** Input/output are fixed above.
   The constructive quantum route is sparse-source preparation, a native QFT,
   dyadic treatment of the multiplier (1-lambda+i/L)^(-1), coherent assembly
   of resonant and off-resonant bands, and inverse QFT with every normalization
   and success cost paid. Expected upside would be polynomial in log grid size
   rather than numerical grid size. The bottleneck is the complete-field
   preparation, not sparse-source loading or a Fourier eigenvalue formula.
   Strong classical competitors are explicit FFT solving and, more seriously,
   direct Green-function evaluation/sampling plus a source-mixture rejection
   scheme that handles interference. Their exact finite-lattice, spatial-TV
   clocks require checking; spectral sampling alone is a different output.
   The fresh proof obligation is uniform source-safe assembly at damping 1/L.
   The five-source control below already falsifies one natural assembly law.

2. **DQI for native sparse parity optimization -- keep as a lower-priority
   comparator.** Take an explicit full-row-rank binary matrix H with m columns
   and n_0 rows, and an explicit target b in F_2^m. Output x maximizing, or
   reaching a proved threshold for, the fraction of satisfied native clauses
   (H^T x)_j=b_j. A concrete family would use parity checks of a certified
   constant-degree expander code, so clauses have bounded width. Prepare a
   phased low-weight error source (-1)^(b.e), compute He, coherently erase e
   using the code decoder, and Fourier transform the syndrome. This is an
   end-to-end DQI mechanism once its error source and decoder are paid.
   The hoped-for advantage is polynomial-time attainment of a strictly better
   approximation regime on an explicit family, not an oracle query separation.
   Decoder radius/failure mass, coherent erasure, and the attainable objective
   threshold are charged. Classical competitors are bit-flip/BP decoding,
   local optimization, relaxation methods, and information-set search.
   A NEW useful obligation would be a source-aware decoding/score theorem for
   a specific certified expander family together with a matched classical
   threshold; merely writing another reversible decoder is not sufficient.
   The present corpus does not supply that winning family. Paired/cubic RS
   residual constructions deliberately change the objective to obtain their
   algebra, and the prime-character capacity route already uses an enormous
   known general list-decoding backend. I would not spend the next batch on
   those same operations without a natural application or a new threshold.

3. **Class-group-free relative squareclass computation -- a concrete cheap
   arithmetic comparator, not the next quantum batch.** Input is a native
   quartic field L with a quadratic subfield F and a rational support set S_Q
   containing 2 and all ramification; output a complete L(S_L,2) basis, hence
   a useful global input to the existing Selmer computation. The existing
   quantum composition can use Shor factoring and the already paid arithmetic
   backends. Its strongest classical competitor is exactly that composition
   with an integer-factorization oracle, not a generic class-group heuristic.
   The genuinely new operation below replaces per-vector support correction
   by a quotient-kernel calculation and appears to remove the odd S-class
   promise. All calls are polynomial-bit fixed-degree conics, quadratic
   squareclasses, factoring, and binary linear algebra. If sound, this enlarges
   the classical match and leaves only factoring as the quantum resource; it
   does not offer a new superpolynomial mechanism beyond Shor. Its external
   value is arithmetic completeness, but it needs a short proof check rather
   than six new exploratory calls. It therefore does not displace (1).

## Immediate Helmholtz falsifier: source count does not pay combination

Put g=A^(-1)delta_0 and K^2=||g||^2. Under the unitary Fourier convention,

    K^2=L^(-2) sum_k 1/((1-lambda(k))^2+L^(-2)).

There is an elementary K^2>=c L bound with an absolute c>0. For every k_y
with angle in [0,pi/6], choose k_x nearest to a solution of
cos(theta_x)=3/2-cos(theta_y). Such a solution exists, and cosine is
1-Lipschitz, so |1-lambda(k)|<=2 pi/L. There are at least L/12 such k_y.
Consequently one may take c=1/[12(1+4 pi^2)]. No lattice-shell asymptotic or
equidistribution theorem is used.

Now use the FIVE explicit sources

    f=B delta_0=-3 delta_0+delta_(1,0)+delta_(-1,0)
                          +delta_(0,1)+delta_(0,-1).

Their exact solution is

    u=delta_0-(i/L)g.

Also ||u||<=1, since its Fourier multiplier on delta_0 is
(1-lambda)/(1-lambda+i/L), of modulus at most one. A standard LCU of the
individually normalized shifted Green states, using coefficient 1-norm
sum|c_j|=7, therefore has success probability

    P_success=||u||^2/(49 K^2)<=12(1+4 pi^2)/(49 L).

Thus a source-count-only constant success claim is false for this exact
native input, and amplitude amplification of this particular LCU can cost
exponentially in n. The source Fourier polynomial also vanishes on the
undamped resonant level 1-lambda=0. These are falsifiers of the stated
combination/shell mechanisms, not of every complete-field algorithm.
Preprocessing f=B delta_0 can escape this example; it must then cover general
explicit source polynomials, rather than quietly assume noncancellation.

The parent reports having read the new Helmholtz primary's principal-value
formula. Accordingly the earlier suggestion that the paper only constructs
a homogeneous on-shell field is WITHDRAWN. I have not independently admitted
that source's ring approximation, precision, or source-success theorem. Its
actual equations and a current classical literature check remain the parent's
primary-source obligations before any theorem claim.

## Fresh arithmetic operation exposed by the comparison

This is an independent proposed completion of the retained quartic interface,
for parent checking; it is not a new source admission. Let

    V=F(S,2) intersect N_(L/F)(L*).

Use the paid relative conic backend for a basis a_i of V, obtaining beta_i
with N(beta_i)=a_i c_i^2. Factor their polynomial-bit denominators/norms and
collect ALL base primes over the resulting rational primes into E, disjoint
from S. Outside S the parity divisor of each beta_i is the pullback of an
F-ideal parity vector J_i. This follows from even norm valuations at split
primes and unramifiedness at inert primes, as in the retained proof.

Compute the complete quadratic F(S union E,2), and let W be the image of its
valuation-parity map to F_2^E. Instead of requiring every J_i to belong to W,
compute

    C=ker(F_2^dim(V) -> F_2^E/W),  c |-> sum_i c_i J_i.

For c in C, a correcting gamma supplied by this image calculation makes
beta=prod_i beta_i^(c_i) have even outside-S valuations after multiplication
by gamma, without changing its norm squareclass. Conversely, if a product
a=prod_i a_i^(c_i) has an even-supported lift alpha, then beta/alpha has
square norm. The usual trace identity gives beta/alpha=gamma delta^2 for
some gamma in F* (including the scalar exceptional case separately).
Unramifiedness outside S makes gamma's parity vector exactly sum_i c_i J_i,
and zero outside S union E. Hence gamma belongs to F(S union E,2), proving
c in C. This establishes the needed converse without assuming class-group
surjectivity. Append F(S,2)/<d> for the norm kernel, with L=F(sqrt(d)).

The finite union E has polynomial size because the conic outputs have
polynomial bit height and there are polynomially many basis vectors.
Multiplying the selected beta_i and correction representatives preserves
polynomial height in this fixed-degree setting. The proposed new proof
obligation is precisely this quotient-kernel completeness and its recorded
coordinate bookkeeping; no principalization or new class-generator source
is being postulated. The old odd-class proof already computes the relevant
quadratic parity matrix, so this is a small actionable change if verified.

## Paid batch and stopping rule

The six proposed Helmholtz obligations are genuinely distinct: complete
multiscale quantum assembly; strongest classical spatial mixture; exact
single-source Green sampling; cancellation-safe source loading/combination;
finite-bit lattice-shell preparation; and Gram conditioning for the explicitly
restricted positive/separated-source subclass. The last subclass cannot be
silently substituted for arbitrary complex weights in the main task.

A polynomial native full-field compiler would justify completing a written
quantum endpoint. A matching polynomial classical spatial sampler would close
this target. If both remain open but every proposed quantum construction
exposes a numerical L cost or an unproved source condition, stop that batch;
do not turn a shell-state lemma into a solver or keep buying nearby barriers.
The five-source calculation should be in the initial packet, not discovered
after implementation.

## Corpus and baseline provenance

Started from current STATE.md and TRAPS.md. Local `been-tried` searches covered
DQI/RS/LDPC decoding, hidden-shift/class-group operations, unconditional class
generators, the quartic support correction, and sparse-source Helmholtz.
The Helmholtz query found no close native endpoint; its leading spatial-walk
barrier was quarantined and was not used as evidence. Local `baselines`
queries returned BP/polar/tensor methods for decoding and index calculus/KLPT
for arithmetic. The Helmholtz baseline index had no relevant entry, so the
explicit FFT and kernel-mixture competitors above are proof obligations,
not claimed source-verified bounds.

Pertinent topic files read: PAIRED_RESIDUAL_DECODER.md,
CUBIC_ORBIT_DECODER.md, PRIME_CHARACTER_CAPACITY_SOURCE.md,
UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md,
NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT.md, and
QUARTIC_RELATIVE_NORM_CLASSICAL.md. The quaternion note rules out merely
rebranding its already classical public-dihedral class label as a new hidden
shift. The unconditional class-generator note already formulates norm-box
support and inverse-norm escape questions, so neither was selected again.
Historical inverse-trace decoder memory was checked against the parent's
current closure and was not used to reopen the solved native search.

## Independent extension: actual spatial-TV falsifier for five sources

The stronger same-output claim is valid with the parent's conservative
constants. Write b(k)=1-lambda(k)=-3+2 cos(theta_x)+2 cos(theta_y),
eta=1/L, and N_delta=#{k: |b(k)|<=delta}. For 0<=delta<=1/8,

    N_delta <= 4 L (L delta+1).                              (1)

Indeed, on this set cos(theta_x)+cos(theta_y) lies in
[23/16,25/16]. If both sine magnitudes were less than 1/2, both cosine
magnitudes would exceed sqrt(3)/2. Their sum would then be at least sqrt(3),
at most -sqrt(3), or have magnitude at most 1-sqrt(3)/2, all impossible.
Thus at least one sine magnitude is >=1/2. For fixed other coordinate,
the corresponding variable has two monotone sine-large arcs, and |db/dtheta|
is >=1 on each. Each arc's intersection with |b|<=delta has length <=2delta
and contains at most L delta/pi+1 <= L delta+1 grid points. Union over the
two arcs, L other-coordinate values, and the two coordinate choices proves
(1), allowing overlap and endpoints conservatively.

Consequently, for every integer L>=4,

    Z_0=L^(-2) sum_k 1/(b(k)^2+eta^2)=||g||^2 <=64 L.       (2)

For L>=16, the region |b|<=1/L contributes at most N_(1/L)<=8L.
Each shell 2^j/L<|b|<=2^(j+1)/L with j>=0 and upper endpoint <=1/8
contributes at most

    4 L (2^(j+1)+1)/4^j <=12 L 2^(-j).

These shell bounds sum to at most 24L. The largest included endpoint is
greater than 1/16, so the remainder contributes at most 256. Altogether
Z_0<=32L+256<=48L<=64L. For 4<=L<16 the trivial Z_0<=L^2 suffices.
This covers the entire spectrum; no uncounted intermediate annulus remains.

For the exact five-source solution, Parseval and the value at the origin give

    Z=||A^(-1)B delta_0||^2=1-eta^2 Z_0>0,
    Re u(0)=L^(-2) sum_k b(k)^2/(b(k)^2+eta^2)=Z.

Hence its normalized spatial law P_f satisfies

    P_f(0)=|u(0)|^2/Z >= Z >=1-64/L.                        (3)

In particular the deterministic classical sampler returning the origin has
TV error at most 64/L for THIS family. This is not a general sparse-source
classical sampler.

Now fix C>=0 and any normalized state psi whose Fourier support is contained
in |b|<=C/L. Cauchy--Schwarz and the unitary Fourier normalization imply
|psi(0)|^2 <=N_(C/L)/L^2 <=4(C+1)/L whenever L>=8C. The same bound holds
for mixtures supported in that Fourier subspace. Therefore, for
L>=max(16,8C), its spatial law P_psi obeys the actual output-distance bound

    TV(P_f,P_psi) >=1-[64+4(C+1)]/L.                        (4)

For fixed C this tends to one. This directly refutes substitution of ANY
such narrow-ring state for the full forced field on the five-source input,
even if that ring state is prepared perfectly. It does not refute a compiler
that retains the principal-value/off-resonant contribution. No paid reports,
numerics, or primary-source claim were used in this extension.
