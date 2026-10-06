# Native Ring-LWE: Covariance, A Failed Projection, And Two-Block Decoding

Date: 2026-09-29. LOCAL DERIVATION / REVIEW PENDING.

No novelty, independently checked theorem, efficient Gaussian preimage
sampler, cryptographic security estimate, or quantum speedup is claimed.
This is theory work and an implementation contract, not a live source change.
Routine integration, full tests and attack sweeps are assigned to Gemini.

Prerequisites: `NATIVE_RLWE_PHASE_DECODER_TARGET.md`,
`NATIVE_RLWE_SAMPLE_ACCESS_AUDIT.md` and
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md`. All errors below refer to their
exact reference distributions; original rounding/anchor losses remain due.

`NATIVE_RLWE_GAUSSIAN_SAMPLER_AUDIT.md` tests implementations of the target:
exact NTRU-form isoduality, native Klein rejection costs, frozen finite-box
basis walks, their infinite-coset gap bound, and the applicability limits
of published quantum sampling/lattice Fourier methods. It does not supply
the missing sampler or rule out arbitrary coherent algorithms.

`NATIVE_RLWE_COHERENT_READOUT_AUDIT.md` (2026-10-04) tests a concrete
entangled-resource/Bell/QFT readout. Its full actual-input transcript has
a classical product sampler in the audited modulus regime. The same note
shows why positive-Wigner intuition cannot dismiss arbitrary Clifford
circuits on the finite Gaussian source.

TARGET RELAXATION (2026-10-04): `NATIVE_RLWE_CHOSEN_PREIMAGE_REDUCTION.md`
gives a DIFFERENT decoder requiring measured preimages at chosen syndromes
with a shortness/moment certificate. Clean erasure and phase consistency
remain required for the inverse in Section 5, but not for that correlation
decoder. Its efficient primitive remains unresolved.

## 1. Correcting The Research Priority

One native record is INFORMATION-sufficient for the actual small-secret
prior. It does not follow that a one-record quantum decoder is the easiest
computational target. Its successful decoder must exploit that prior and
break full translation covariance. Section 2 proves a sharp obstruction for
decoders that do not. Section 3 tests an explicit prior-aware coherent
operation and shows why this particular attempt still has exponential cost.

Keep TWO distinct research tracks:

- A genuinely prior-aware, noncovariant one-record decoder, always compared
  against original-data classical decoding. A box-membership projector plus
  amplitude amplification is not enough.
- A two-INDEPENDENT-record, translation-covariant decoder with wider native
  Gaussian coefficients. Section 4 certifies sufficient information even
  for a uniform secret. Its concrete missing operation is a coherent,
  phase-aligned Gaussian preimage sampler on a rank-two R-module in its
  natural product metric. Specifying this operation does not implement it.

The second track does not contradict one-record sufficiency and does not
restore the old scalar Q=q^d+1 construction. Neither track is an algorithm
result. Repeated preparation of one record is not the second track.

## 2. A One-Record Covariant Decoder Cannot Use The Small Prior

Fix a unit a in R_q, where R=Z[X]/(X^d+1), d is a power of two, and q is
an odd prime. The ACTUAL normal-form record is b=C_a*s+e mod q. Write a
decoder's output as a center estimate y_hat=C_a*s_hat. Suppose its COMPLETE
classical input/output kernel satisfies

    K_a(y+t | b+t)=K_a(y | b), for all t in Z_q^d.             (1)

The kernel may include arbitrary quantum computation, extra preparations
of the SAME record, and an abort output. Fixed ancillary data/randomness
must not supply another correlated training record or hidden error. This
is a premise about the whole decoder, not just its final Fourier transform.

Taking t=-b shows K_a(y|b)=nu_a(y-b), with sum_z nu_a(z)<=1. Therefore
for ANY secret prior, when noise is independent of the secret,

    Pr[s_hat=s]=sum_e Pr[e] nu_a(-e)
               <=max_z Pr[e=z mod q].                        (2)

The same proof holds conditional on the hidden elliptical shape H, after
which we average H. It needs no uniform-secret assumption. Ancillary
randomness independent of secret/noise conditional on H may be averaged
too. A prior-aware operation generally violates (1), as it must to escape
this result. Multiple independent training records are outside (2).
Postselection does not evade the bound on UNCONDITIONAL success.

For D_(Z^d,H), with density proportional to exp(-pi*e^T*H^(-1)*e), the
wrapped mass is maximal at zero. Its finite Fourier coefficients are
nonnegative by Poisson summation. If H>=h_0*I, then another use of Poisson
summation gives, with Theta(t)=sum_(k in Z) exp(-pi*k^2/t^2),

    p_0=Pr[e=0 mod q]
       =q^(-d) [sum_k exp(-pi*k^T*H*k/q^2)]
                 /[sum_k exp(-pi*k^T*H*k)]
       <=[Theta(q/sqrt(h_0))/q]^d
       <=(1/q+1/sqrt(h_0))^d.                                (3)

The last inequality uses Theta(t)<=1+t. In the spherical lane h_0=rho^2.
In the actual hidden elliptical lane a UNIFORM lower eigenvalue is

    h_0=(log d)^2+d*(log d)^4/2.                              (4)

This follows by dropping the nonnegative latent squared variables, not by
giving H to the decoder or replacing H with its mean. Conditioning on a
unit label does not change these noise laws. Charge label rejection.

At the native q-near-d^4 references, the base-10 logarithms of the upper
bound (3) are:

| d | Spherical | Hidden elliptical |
| --- | ---: | ---: |
| 64 | -126.338109 | -127.418743 |
| 256 | -652.837989 | -650.621699 |
| 1024 | -3172.922424 | -3109.165803 |

These are scoped analytic success bounds, not estimates of all quantum
or classical decoders. In particular they do not apply to small-prior MAP.

## 3. Explicit Coherent Projection: Available Operations, Exponential Cost

Prepare a one-record source with a known normalized envelope g_a(c),
independent of b and e, and public phase exp(2*pi*i*<b,c>/q). It may be a
complex, nonproduct envelope for this argument. Fourier transformation gives

    |psi_(a,b)>=sum_y g_hat_a(y-b)|y>.                        (5)

For a unit a, reversibly mark membership of C_a^(-1)*y in a specified small
secret set S, using a projector Pi. Reflection about (5) is available from
its ACTUAL state-preparation circuit, not an assumed ideal-state oracle.
Try alternating phase rotations on Pi and on |psi><psi|.

Let p=||Pi*psi||^2. If the true s belongs to S, its marked basis point
y_star=C_a*s has initial probability w=|g_hat_a(-e)|^2. Otherwise correct
marked output has probability zero. The rotations preserve the two-dimensional
span of the normalized good and bad projections of psi. They NEVER change
the direction of the normalized good projection.

After T source-state phase rotations, the good amplitude is at most
(2*T+1)*sqrt(p). Indeed each such rotation has off-diagonal entry of
magnitude at most 2*sqrt(p), and good-subspace phase rotations do not mix
the two components. Thus even phase-matched choices satisfy

    Pr[correct marked output | a,b,s] <=(2*T+1)^2*w,
    E Pr[correct marked output] <=(2*T+1)^2*max_z Pr[e=z].     (6)

In the last step drop the indicator s in S, then use
sum_z |g_hat_a(z)|^2=1. For the elliptical lane first condition on H.
An input-dependent schedule with at most T rotations has the same bound.
Separate repeated trials pay for their summed costs. This is not a bound
for arbitrary operations that alter the good direction, or a decoder that
already solves the problem in classical preprocessing.

Equation (3) makes polynomially many rotations useless for constant success
in these families. The fixed-input accepted distribution is just the
classical Fourier-readout law conditioned on the same membership test.
For the native envelope this law has a classical sampler with the already
specified precision/alias errors. Amplification changes the acceptance
overhead quadratically; it does not create a new decoding distribution.

This uses the standard amplitude-amplification framework of
[Brassard--Hoyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055),
not a new search primitive. The source-specific averaged bound is a local
derivation. More general prior-aware interference remains open.

## 4. Two Independent Labels Give A Uniform-Secret Information Certificate

Use L independent uniform labels a_1,...,a_L in R_q and the linear map

    F_A(c)=sum_l C_(a_l)^T*c_l mod q,  N=q^d.                 (7)

For this section take an UNWRAPPED integer reference source

    |Psi_s> proportional to sum_(c in Z^(L*d))
        exp(-pi*||c||^2/sigma^2) exp(2*pi*i*<s,F_A(c)>/q)|c>.

Coefficient probabilities are discrete Gaussian with width s_G=sigma/sqrt(2).
Their residue law is

    mu_q(r)=[sum_k exp(-2*pi*(r+q*k)^2/sigma^2)]/Theta(s_G).

This is a PERIODIZATION OF PROBABILITIES, not the square of a periodized
amplitude. The two conventions have different conditional states. Both
will have useful bounds, but they must not be silently interchanged.

Poisson summation gives nonnegative characteristic coefficients and maximum
residue mass at zero. For q>=2*sigma and sigma>=1,

    m=max_r mu_q(r) <=Theta(s_G/q)/Theta(s_G)
                    <=10/(7*sigma).                         (8)

To check the rational constant, Theta(s_G)>=s_G, and
Theta(s_G/q)<=1+2*exp(-8*pi)/(1-exp(-24*pi)); its product with sqrt(2)
is less than 10/7. Cap the mass bound at one when necessary.

Let f=ord_(2*d)(q), J=d/f. CRT decomposes R_q into J fields of size q^f.
Exactly binomial(J,j)*(q^f-1)^j elements Delta have multiplication rank
r=j*f. For any such nonzero Delta, averaging one uniform label gives

    b_Delta=E_a <Psi_0|Psi_Delta>
           =Pr_(c from mu_q^d)[C_Delta^T*c=0]
           <=m^r.                                           (9)

The pivot-coordinate argument proves the last inequality even though the
negacyclic matrix has highly dependent entries. L independent labels give
b_Delta^L, not b_Delta for L repeated copies of the same label. Summing the
EXACT rank counts, define

    A(A)=sum_(Delta!=0) <Psi_0|Psi_Delta>,
    E_A A(A) <= B_L=[1+(q^f-1)*m^(L*f)]^J-1.                (10)

All terms in A(A) are nonnegative. For r_A(u)=Pr[F_A(c)=u], character
inversion gives, simultaneously for EVERY u,

    A(A)=N*r_A(0)-1,
    |N*r_A(u)-1|<=A(A),
    Pr_A[A(A)>eta]<=B_L/eta.                                (11)

This is all-frequency relative flatness on good labels, not merely a
collision-entropy bound. There is no prior box, small-difference assumption,
or omission of zero divisors. At high residue degree f=d/2, J=2, L=2,

    x=(q^(d/2)-1)*(10/(7*sigma))^d,
    B_2=2*x+x^2.                                            (12)

If a construction conditions a_1 to be a unit, its probability is
p_U=(1-q^(-f))^J. Replace the mean bound by B_L/p_U and charge 1-p_U;
do not pretend conditioning preserves the original label average.

### Optimal Measurement Does Not Mean Efficient Measurement

For nonempty fibers define the normalized Gaussian states

    |chi_u> proportional to sum_(F_A(c)=u)
                            exp(-pi*||c||^2/sigma^2)|c>

These states are orthogonal, and the source decomposes as

    |Psi_s>=sum_u sqrt(r_A(u))*exp(2*pi*i*<s,u>/q)|chi_u>.

Empty fibers have r_A(u)=0 and are omitted. On a unit-first-label branch
every fiber is nonempty; the sampler contract below uses that branch.

The optimal uniform-prior discrimination probability is

    P_opt=(sum_u sqrt(r_A(u)))^2/N.                          (13)

Locally, twirling an optimal POVM makes it covariant; its seed in the chi
basis has diagonal 1/N and off-diagonal magnitude at most 1/N. The
all-positive rank-one seed attains (13). This is the established
geometrically uniform square-root measurement, not a novel POVM; see
[Eldar--Forney](https://arxiv.org/abs/quant-ph/0005132).

From (11), P_opt>=1-min(1,A(A)), hence mean ideal failure <=B_L. Every
secret has the SAME conditional success for this covariant measurement,
so the bound also applies to the actual small prior. An explicit matrix
for the POVM or a simulation at tiny d does not compile it efficiently.

There is ALSO a classical information comparator. For the separate finite
PERIODIZED-AMPLITUDE reference in NATIVE_RLWE_PHASE_DECODER_TARGET, its
squared coefficient mass obeys the same 10/(7*sigma) bound when q>=2*sigma:
use sqrt(2)*(1+2*exp(-4*pi)/(1-exp(-12*pi)))^2<10/7.
Positive Fourier amplitudes make each classical readout Bhattacharyya
overlap equal the corresponding state overlap. The same CRT sum bounds
exhaustive uniform-secret ML failure by B_L. This establishes no efficient
classical algorithm, but rules out interpreting (10) as quantum-only
information. Use that reference's OWN finite-to-periodized error ledger.

## 5. The Missing Primitive, Precisely Stated

CLASSICAL FOLLOW-UP: NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE gives a direct
ONE-record original-data decoder on two d64 labels at the same q-near-d^4
row, with source-specific reference-law failure certificates for both lanes.
It need not implement (14), find Gaussian preimages or obey their internal
radius. Compare endpoints, not which internal quantum primitive it simulates.

On a unit-first-label branch, set

    K_A={c in Z^(L*d): F_A(c)=0 mod q}, det K_A=q^d.

For L=2 this is a rank-two R-module, ambient integer dimension 2d. Its
Gaussian metric is the ordinary PRODUCT coefficient metric; the product
canonical embedding changes this by only the common factor sqrt(d).
Do not embed it into a larger number field and assume that field's
canonical Gaussian retains this metric. The old metric audits explain
why that substitution can fail.

The constructive target is a coherent, phase-aligned operation

    V_A: |u>|0> -> |u>|chi_u>,                               (14)

with clean workspace, consistent positive relative phases, charged tails
and polynomial resources, at sigma=O(sqrt(q)). An acceptable weaker
approximation may be specified directly on the weighted superpositions
used here, but per-u probability distributions alone are insufficient for
THIS inverse/erasure construction. The chosen-preimage follow-up gives an
alternative decoder where distribution access can suffice without erasure.

If (14) is implemented, compute u=F_A(c) on the source, apply V_A^(-1)
to erase c, then use the inverse finite-group QFT on u. Its success is
(13). This is a reduction to an UNSOLVED operation, not a free preimage
oracle. A classical Gaussian sampler may leave irreversible random bits
or branch-dependent garbage; running it reversibly does not by itself
produce (14). Unknown u-dependent phases can also destroy the decoder.

Naively preparing the ambient Gaussian and postselecting F_A(c)=u has
probability r_A(u) approximately 1/N. Amplitude amplification costs
approximately sqrt(N)=q^(d/2). Near-flatness improves a CONDITION NUMBER,
not that absolute normalization. A generic polar-inverse wrapper has the
same missing cost. A supplied short basis/trapdoor is not part of the input.

### Finite Physical Support And The Error Ledger

The implemented signed source has each coordinate in [-R_c,R_c], with
1<=R_c<q/2. Embed it into the integer reference before applying a common
decoder. A scalar Gaussian tail bound gives

    eta_1<=sigma/(sqrt(2)*pi*R_c)*exp(-2*pi*R_c^2/sigma^2),
    delta_integer<=min(1,sqrt(L*d*eta_1)).                   (15)

Indeed Theta(s_G)>=s_G, the unnormalized two-sided tail is at most
sigma^2/(2*pi*R_c)*exp(-2*pi*R_c^2/sigma^2), and the squared overlap of
the truncated product state with the reference is its retained mass.

For L=2, R_c=sigma*sqrt(d), (15) is
(2*d)^(1/4)/sqrt(pi)*exp(-pi*d). The independent native records also pay

    delta_phase<=sqrt(2*pi)*sigma*sqrt(E2)/q.                (16)

Thus a hypothetical decoder has mean actual success at least
1-B_2-delta_integer-delta_phase-delta_implementation, before the separately
required normal-form/rounding/held-out verification ledger. Unit conditioning
changes B_2 as described above and adds its own rejection cost.

These are GLOBAL source-to-reference distances. Do not divide by a rare
fiber probability and assume the same conditional error. Section 4 proves
the unwrapped reference's relative flatness directly, avoiding that trap.

## 6. Finite References And Scaling

These are DISTINCT two-block reference widths, approximately 2*sqrt(q),
not replacements silently applied to the old one-block records.

| d | q | sigma | log10 B_2 | Spherical phase bound | Elliptical phase bound |
| --- | ---: | ---: | ---: | ---: | ---: |
| 64 | 16777259 | 8192 | -9.051128669 | 0.367954667 | 0.384294987 |
| 256 | 4294967357 | 131072 | -37.107746348 | 0.173307945 | 0.170326352 |
| 1024 | 1099511627803 | 2097152 | -149.334078533 | 0.076583836 | 0.066464983 |

Take R_c=sigma*sqrt(d). Width and support inequalities hold. B_2<=1e-8
was checked by EXACT integer arithmetic: n=(q^(d/2)-1)*10^d,
D=(7*sigma)^d, and (2*n*D+n^2)*10^8<=D^2. The primes and residue-degree
family were previously checked in the native note. Transcendental numbers
above are 100-digit numerical references, not interval-arithmetic proofs.

The phase upper bounds at d=64 are substantial, not negligible. They are
still consistent with a constant-success transfer IF the ideal decoder
is implemented and the other losses are paid. No such decoder is supplied.
The integer-tail bounds are below 1e-87 in all rows. Neither comparison
proves these finite Ring-LWE instances classically difficult.

For q of order d^a in the same residue-degree family and
sigma=c*sqrt(q), c>10/7 fixed, B_2 decays exponentially in d. The audited
moments give source errors of orders

    spherical: d^(5/4-a/2)*log d,
    elliptical: d^(1-a/2)*(log d)^2.                         (17)

At a=4 both vanish polynomially. This is a plausible source/measurement
parameter window, not an efficient algorithm or a separation.

## 7. Falsifiers And Work Allocation

Main-model work: construct or rule out specific implementations of (14),
or construct a genuinely noncovariant one-block decoder. Do not spend more
effort rederiving generic PGM optimality, generating apparent signals from
the wrong access model, or adding scalar-source infrastructure to this route.

Before treating a proposal as useful, try to falsify it by these checks:

- Does it only rotate the same two good/bad directions? Then (6) applies.
- Does it assume a Gaussian preimage/trapdoor as input? Then it assumes the
  central computational task rather than solves it.
- Does an ostensibly coherent sampler retain randomness, u-dependent phases,
  or inaccessible hidden shape? Distributional correctness is not enough.
- Does it use many copies of one record as independent labels? Then (10)
  is unavailable, and SAMPLE_ACCESS_AUDIT also constrains ideal transfer.
- Does a basis finder or classical sampler already decode ORIGINAL data?
  Then benchmark that algorithm before claiming a quantum opportunity.
- Are the finite parameters broken by serious classical lattice/hybrid
  attacks? Record that negative result; do not call failed Babai hardness.
- Are conclusions based only on averaged ideal states while discarding
  input/secret references needed to score recovery? Reject that transfer.

Gemini contract: add separate prior-aware-L1 and covariant-L2 source IDs;
record the actual number of independent training samples and preparations,
label conditioning, exact CRT rank counts, rational B witnesses, source
convention, cutoffs, precision, all error terms and proof status. No default
change to production widths, no promotion to a speedup candidate. Implement
original-data attacks before extensive ideal-state numerical experiments.

Regression checks should distinguish folded probabilities from squared
folded amplitudes, repeated from independent labels, ideal from actual noise,
conditional from global source errors, and inverse-state preparation from
an inverse of a CLASSICAL sampler. Tiny explicit inverses are algebra
controls only. Expose separate information, compilation, source, classical
baseline and reduction blockers rather than a single optimistic pass flag.

## 8. Checks Actually Run

Targeted derivation controls, not the routine repository test suite:

- Seed 290934: all nonzero Delta at (d,q,sigma)=(2,3,1.4),(2,5,2),
  (2,7,3),(4,3,1.4), totaling 160 kernel/rank checks. Exact rank counts
  were respectively {2:8}, {2:16,1:8}, {2:48}, {4:64,2:16}.
- All independent label pairs at the three d=2 cases (81,625,2401 pairs),
  and 40 seeded pairs at d=4. Checked (9)-(11), including all-u relative
  deviations. Maximum discrepancy between the two exact mean-A formulas
  was 4.45e-15. The small-parameter bounds are often vacuous; no advantage
  is inferred from these controls.
- Forty explicit finite coherent-frame controls checked orthonormal fiber
  columns and inverse-frame-plus-QFT success (13), tolerance 2e-12.
- Seed 290935: 48 correlated two-dimensional Gaussian shapes, eigenvalues
  between 3 and 18, q in {3,5,11,17}, integer cutoff 22. Checked folded
  maxima at zero and the conservative bound (3). Finite truncation makes
  these numerical algebra controls, not exact infinite-Gaussian proofs.
- Sixty covariant POVMs with random complex correlation seeds, arbitrary
  complex sources and nonuniform priors at q=3,5,7. Checked kernel
  covariance and (2); maximum identity discrepancy 1.12e-16.
- Forty-eight unit-label source cases at d=2, q=5,7, sigma=1.3 and box
  [-1,1]^2. Checked 336 ordinary-amplification and 336 phase-matched
  branches, T=0,...,6, against (6). The accepted normalized law stayed
  unchanged, maximum discrepancy 2.81e-15.
- Three growing reference rows: exact rational B, support and width checks;
  100-digit source errors and noise-atom references. The parameter checks
  were rerun after the context transition before saving this note.

These can expose algebra/implementation errors, not establish novelty or
independent proof verification. No CLI/registry wiring, full test-suite
run, large attack sweep, commit or proof promotion was performed here.
