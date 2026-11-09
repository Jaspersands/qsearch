# Modular subset sum: half-center geometry and Gaussian admission

2026-11-06. Written correction and a concrete sampler test. Sections1--6 passed independent derivation AND actual-text core review.
The reviewer rechecked equations (1)--(9), source laws, and the specific-herald
scope; this is automated review, not human validation. No
polynomial subset-sum/DCP algorithm, classical hardness, novelty, quantum
execution, or general lattice exclusion is claimed.

## 1. Question, input and proposed operation

The externally motivated problem is the average-case modular subset-sum
finder used in DCP measurement/reduction work: given explicit
`a in (Z/DZ)^n` and target T, output x in {0,1}^n with a.x=T mod D, or FAIL.
Verification uses the original modular relation. This note distinguishes:

- U: coefficients IID uniform, T independently uniform;
- P: coefficients IID uniform, a fixed or independent uniform binary X is
  used to form T=a.X. For the density-ratio statements below X is UNIFORM.
  X is not supplied to the finder.

At density one D=2^n, the proposed operation is an arbitrary-center discrete
Gaussian sampler on the GIVEN affine integer coset, centered at the Boolean
cube midpoint. It would have to run in poly(n,logD,log1/epsilon) time, include
its basis/preparation/normalization costs, and have TV error at most epsilon.
It is not enough to generate a fresh random target together with its witness.
An efficient finder would be a serious candidate for existing DCP reductions;
this note does not reprove or claim their coherent composition.

This proposal was checked against the corpus, the existing coordinate-rounding
controls, the standard LLL/Babai baseline, and current Gaussian-sampling
literature before any quantum implementation. The actual half-integer
observation already appears in the October16 correction in
`DCP_BABAI_LATTICE_ROUNDING_WITNESS_OBSTRUCTION.md`; it is reused here.
Its native finite coordinate-rounding failures do not prove a lower bound
for Gram--Schmidt nearest plane, exact CVP, or all Gaussian algorithms.

The hoped asymptotic result is a polynomial-time average-case finder, not
merely a quadratic improvement over an exponential rejection sampler.
Decisive falsifiers are poor Boolean mass under the ORIGINAL source law,
exponential normalization, uncharged basis reduction or selected targets,
and failure to preserve the supplied target. Sections2--4 pay the first
gate. Section5 rejects the straightforward conservative rejection envelope.

An independent portfolio check also rejected a tempting character-row
sampler. For lambda=(2,1), size-biased rim-hook removal followed by classical
recursion yields probabilities (1/3,1/3,1/3) on (1^3,21,3), whereas the true
chi_lambda(nu)^2/z_nu law is (2/3,0,1/3). The conditional sum
b_1|21>=|2>+|11> must remain coherent. This only rejects that recursion;
the general joint sampler remains open. No new CFT implementation was admitted.

## 2. Exact geometry, with parity retained

For any modulus D>=2 and any explicit coefficient vector, let

    g=gcd(D,a_1,...,a_n),
    L={z in Z^n:a.z=0 mod D},       h=(1/2,...,1/2).

The integer target coset exists iff g divides T. Extended gcd constructs
one integer solution z0 when it exists, without a binary witness. The image
of the homomorphism has size D/g, hence det L=D/g. All integer solutions
are z0+L; a public integer basis follows by standard kernel/HNF arithmetic.

For EVERY integer x,

    ||x-h||^2 >= n/4,
    equality iff x in {0,1}^n,
    x nonbinary implies ||x-h||^2 >= n/4+2.                 (1)

Each coordinate is a half-integer, so these assertions are immediate term
by term. Thus binary solutions are EXACTLY the points of z0+L in the closed
ball B(h,sqrt(n)/2), all on its boundary. If a binary solution exists,
every exact closest vector is binary. This is a standard exact-CVP
reduction, not an efficient CVP solver or a BDD-radius guarantee. Even an
approximate solver with factor gamma satisfying gamma^2<1+8/n would return
a binary solution on every binary-feasible instance; no such efficient solver is
supplied here.

In signed coordinates e=2x-1 the feasible set is

    2(z0+L)-1,
    e_i odd for EVERY i,
    a.e = 2T-sum_i a_i mod 2D.

Its difference lattice is 2L, with determinant 2^n D/g. The single displayed
congruence without the coordinate parities generally defines a larger set.
For n=2,D=4,a=(1,1),T=1, the relaxed congruence admits e=(0,0), but the
true signed witnesses are (-1,1),(1,-1). The corresponding determinants
are det L=4 and det(2L)=16.

The legacy volume note divides the radius-sqrt(n) signed ball by D and
asserts exponentially many shorter nonbinary candidates. Both its encoding
and that conclusion are wrong. Even correcting the determinant leaves,
for D=2^n,g=1, the continuous ratio

    Vol(B_n(sqrt(n)))/(2^n D)
      ~ (sqrt(2*pi*e)/4)^n/sqrt(pi*n).

This mildly exponential continuous ratio still does NOT count lattice
points in this boundary-aligned ensemble. Section3 gives the exact mean.
The Gaussian heuristic is not a theorem about every translated lattice.

## 3. Exact native counting laws

Write N(a,T)=|{x in {0,1}^n:a.x=T mod D}|. Under U, for EVERY D>=2,

    E_U N = 2^n/D,
    E_U N^2 = 2^n/D + 2^n(2^n-1)/D^2.                    (2)

For distinct binary x,y, the vector x-y has a coordinate equal to +1 or
-1, a unit modulo any D. Thus a.(x-y) is uniform; the additional independent
T gives joint probability D^-2. Diagonal pairs give D^-1. No primality or
conditioning on gcd=1 is used.

For every FIXED planted X, with a IID uniform and T=a.X,

    E N(a,a.X) = 1+(2^n-1)/D.                             (3)

At D=2^n, (2) gives EN=1 and EN^2=2-2^-n, so

    Pr_U[N>0] >= 1/(2-2^-n) > 1/2.                       (4)

When X is uniform, dP/dU=N at D=2^n. In particular, the target obtained by
computing and measuring a subset-sum register from a uniform Boolean
superposition has P(T|a)=N(a,T)/2^n, the planted law. A DCP phase depending
only on the measured sum changes no such probabilities. This statement
does not extend to correlated/sieved labels or other input amplitudes.

Consequently an exponential number of closest Boolean candidates is not
typical in either law: Markov bounds its probability using means 1 and
2-2^-n. Small output-list cardinality does not make finding that list easy.
No list-decoder success bound follows by dividing a list size by a
continuous volume heuristic, and no polynomial finder follows from (2).

## 4. A useful Gaussian target, conditional on a supplied sampler

Define, on the original integer target coset,

    w(x)=exp(-pi*||x-h||^2/sigma^2),
    w0=exp(-pi*n/(4*sigma^2)),
    r=sum_(j>=0) exp(-pi*j*(j+1)/sigma^2),
    Ubad(a,T)=sum_(x nonbinary, a.x=T) w(x)/w0.

The entire Z^n Gaussian mass is exactly 2^n w0 r^n. By Tonelli and uniform
T, at D=2^n,

    E_U Ubad = r^n-1,
    Z(a,T)=sum_(a.x=T) w(x)=w0*(N+Ubad).                   (5)

If g does not divide T, set Z=0 and return FAIL before asking a sampler.
Otherwise Z>0. An exact target-coset DGS sample is binary with probability
p_bin=N/(N+Ubad); define this as zero on the nonexistent coset.

Choose

    exp(-2*pi/sigma^2) <= 1/(32n),
    equivalently sigma^2 <= 2*pi/log(32n).                 (6)

Putting alpha=exp(-2*pi/sigma^2), j(j+1)/2>=j gives
r<=1/(1-alpha). Hence r^n<=exp(1/31)<17/16. Since
p_bin>=1[N>0]-Ubad, (4)--(5) imply

    E_U p_bin >= 1/(2-2^-n) - (r^n-1) > 7/16.            (7)

For the UNIFORM-X planted law the guarantee is stronger. By its density N
and Cauchy--Schwarz, with 0/0 interpreted as zero,

    E_P p_bin = E_U [N^2/(N+Ubad)]
              >= (E_U N)^2/E_U(N+Ubad)
              = r^(-n) > 16/17.                          (8)

These are source-AVERAGE guarantees, not all-instance promises. A sampler
within TV epsilon on every given feasible coset loses at most epsilon
in the corresponding average success. Preparing a state or a sample for
a freshly generated target does not supply the given-target operation.
No efficiently preparable coset state is assumed as part of the native input.

## 5. First paid-source test: the conservative rejection envelope fails

The current primary comparator is Chevignard--Shen--Schrottenloher,
[arXiv:2605.20133v1](https://arxiv.org/abs/2605.20133), Section3.3 and its
final sampling theorem. Its quantum sampler starts from the Klein proposal
and uses amplitude transduction/rejection with a basis-dependent envelope.
The application there is explicitly ZERO-centered. The following is a
local calculation for a straightforward arbitrary-center extension, not
a theorem attributed to that paper about our affine target.

For a public basis B of L, let b_i^* be its Gram--Schmidt vectors and
sigma_i=sigma/||b_i^*||. In ideal untruncated Klein sampling the proposal
probability of y in L at center h-z0 is its Gaussian weight divided by a
product of one-dimensional Gaussian masses at conditional centers. Each
such mass is bounded above by the zero-centered theta mass. Therefore the
usual conservative envelope is

    A_B=product_i rho_(sigma_i)(Z) >= 1.

Accepting with the conditional-mass product divided by A_B converts the
proposal to the desired Gaussian and has EXACT herald probability

    p_acc=Z(a,T)/A_B.

Even granting ideal exact arithmetic and free proposal preparation, (5)--(6)
give the POINTWISE bound, for every instance and every choice of basis,

    p_acc <= total Z^n mass = 2^n w0 r^n
          < (17/16)*2^n*(32n)^(-n/8)
          = (17/16)*(8/n)^(n/8).                         (9)

This is exp(-Omega(n log n)) as n grows. With Q ordinary amplitude-
amplification iterations, success THROUGH THIS HERALD is at most
(2Q+1)^2 p_acc. Polynomial iterations/repetitions therefore do not give
inverse-polynomial success. The ideal calculation already grants away
finite-precision, truncation and basis-preprocessing costs; they cannot
serve as missing efficiency proofs for this same envelope.

This rejection is strictly specific to that conservative normalization.
It is NOT a lower bound for all DGS algorithms, tighter shifted-mass bounds,
other uses of the proposal/failure states, or all lattice bases and receivers.
Indeed, for L=Z^n and center h a product DGS sampler is trivial while the
same zero-centered envelope can waste an exponentially small herald.
Known minimum distance (1) may help a different normalization; no paid
polynomial construction exploiting it is supplied here. A large sufficient
cost expression alone would not be a lower bound; (9) instead concerns the
actual acceptance probability of the specified ideal rejection procedure.

The paid classical controls here are LLL with actual Gram--Schmidt nearest
plane and exact CVP at small size. They are NOT claimed to be the strongest
full subset-sum portfolio: representation algorithms must also enter any
future performance comparison. No speedup is inferred from these controls. The threshold 0.9408 in
[Coster et al., Theorem3.1](https://d-nb.info/1156214629/34)
uses a SHORTEST-VECTOR ORACLE; it is not an unconditional polynomial-time
guarantee for LLL/BKZ. Its ordinary integer/planted source is also not the
same as our modular U source. The legacy note misstates both this premise
and its own low-density volume arithmetic.

## 6. Decision and remaining gates

Withdraw the universal volume/multiplicity/list exclusion in
`DCP_SUBSET_SUM_EUCLIDEAN_VOLUME_INFLATION_BARRIER.md`. Preserve its historical
text behind an explicit warning and queue only its exact registry record
for mechanical quarantine. Do not broaden this to unrelated DCP records.

The proposed arbitrary-center Gaussian target has useful Boolean mass on
both explicitly stated source laws. The direct conservative-envelope
construction does not pay it. No Gaussian wrapper, enlarged lattice scan,
or new quantum implementation is warranted. A future candidate needs an
actual normalization/preparation algorithm for the given target, then its
native average coverage and coherent-use costs. Removing the false legacy
exclusion does not promote that missing algorithm into existence.

Primary PDFs/text are cached as audits/sources/quantum_dgs_2605_20133.* and
audits/sources/coster_low_density_1992.*. Focused controls are COMPLETE in
`classical_baselines/dcp_half_center_control.py` and `.json`. The parent
inspected the script and artifact and independently verified the returned
native congruences; the solver was not rerun.

- Exhaustive n3,D8 census: EN=1, EN²=15/8, planted EN=15/8, and the complete
  histogram obeys the exact size-bias identity.
- The n2,D4 parity control checks the relaxed zero, true signed witnesses,
  and determinants 4 and16.
- ONE native seeded n8,D256 draw used a=[24,45,68,120,3,166,207,142], T=5.
  Both exact-Gram--Schmidt nearest plane after LLL and fpylll proved CVP
  return binary witnesses at squared scaled distance8. Enumeration AFTER
  both solvers finds three solutions. The producer uses only (a,T,D);
  the enumerated witnesses are validator-only. No draw was rejected or
  resampled; the solver phase took about0.013 seconds at this tiny size.

These are finite classical controls, not a performance extrapolation or a
quantum/Gaussian execution. No numerical Gaussian experiment is needed for
(1)--(9). The source-scope helper also checked the PDF text: DGS Theorem7
has c=0 and its mass-ratio factor; Coster Theorem3.1 uses its lattice oracle.
