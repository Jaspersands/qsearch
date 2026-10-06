# Native Ring-LWE Phase States: A Smaller Decoder Target

Date: 2026-09-29. LOCAL DERIVATION / REVIEW PENDING.

No novelty, independently verified theorem, efficient decoder, cryptographic
security estimate, or quantum speedup is claimed. This is a mathematical
replacement target and implementation contract, not a live source change.
Routine implementation and large classical attack sweeps are assigned to Gemini.

CLASSICAL FOLLOW-UP (2026-10-05): NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE
constructs direct original-data decoders for TWO unfiltered native d64 labels
at the q-near-d^4 row, with exact rational source-specific failure bounds for
both reference laws. No auxiliary Gaussian sampler or ideal state is needed.
These fixed labels are not quantum-advantage evidence; larger dimensions,
typical-label behavior and original-source transfer remain unresolved.

`NATIVE_RLWE_COVARIANT_DECODER_TARGET.md` corrects the one-block research
priority without changing its information certificate: a one-record
translation-covariant decoder fails on actual noise, while two INDEPENDENT
records at wider widths support a uniform-secret covariant target. Keep
prior-aware L1 and covariant L2 as separate computational tracks. That note
also rules out a simple coherent small-prior projection/amplification attempt.

`NATIVE_RLWE_SAMPLE_ACCESS_AUDIT.md` checks the published quantum-amplitude
LWE route and derives an exact repeated-copy lower bound, retaining either
the original input or an inaccessible secret reference. Extra preparations
are not free ideal independent samples. A fully averaged quantum marginal
that forgets both records cannot certify secret-recovery transfer.

`KNOWN_PHASE_SIEVE_DEQUANTIZATION.md` rules out a separate apparent shortcut:
measured-witness extraction followed by known-qubit or explicitly listed
packet sieves has a classical sampler on this ACTUAL classical-tag source,
under the stated operation/access premises. General coherent decoders and
genuine unknown-phase HSP inputs are not covered.

## 1. Decision

The scalar construction through Q=q^d+1 is NOT required to pose a
hardness-linked quantum decoding problem. Prepare Gaussian phase registers
directly from an original normal-form Ring-LWE sample over R_q. This removes
the scalar evaluation, upstream mixing, selector hash, extended number field,
and their associated error terms from this DISTINCT forward construction.

One native block suffices statistically for the actual small-secret priors.
The proof below covers nonunit short differences by their multiplication
rank. A high residue-degree modulus makes every relevant difference a unit.
Sharper secret tails give concrete q near d^4 references, replacing the
earlier d^12 convenience choice without changing the two error-law contracts.

This is not new information extracted from a classical input. All state
parameters are computed from the retained sample (a,b); local Fourier readout
only ADDS noise to b. The unresolved contribution must be an efficient quantum
DECODING computation, compared against attacks on the ORIGINAL samples.
Neither constructing these states nor certifying information sufficiency
is evidence for such a computation.

## 2. Input, Preparation And Joint Error

Use the normalization, discretization and normal-form reduction in
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md`. Set

    R=Z[X]/(X^d+1), d>=2 a power of two, q an odd prime,
    b_l=C_(a_l)*s+e_l mod q,  a_l uniform in R_q,

where C_a is the d by d INTEGER negacyclic multiplication matrix. The secret
s is error-distributed after the anchor step. Labels are independent of s
and the latent error shape. For the elliptical source, secret and errors are
independent only CONDITIONALLY on that shape. No solver is given the shape,
secret, noise, or witnesses for any of them.

For sigma>0 and integer 1<=R_c<q/2, prepare

    |Psi_(b_l,R_c)> = sum_(c in [-R_c,R_c]^d)
        g_R(c) * exp(2*pi*i*<b_l,c>/q) |c mod q>,              (1)
    g_R(c) proportional to exp(-pi*||c||^2/sigma^2).

Prepare coordinates separately, apply the PUBLIC phase from b_l, and
uncompute workspace. The coordinate preparation and reversible arithmetic
are the same ordinary primitives as in DIRECT_PHASE_SOURCE, now modulo q.
There is no enumeration of q^d entries or use of an unknown secret.
Arithmetic/state preparation precision and capped preparation retries must
still be charged. This note does not provide a compiled fault-tolerant circuit.

Let the ideal truncated state replace b_l by C_(a_l)*s. For actual integer
noise lifts, symmetry and the variance bound for a centrally truncated
discrete Gaussian give

    Var(c_i)<=sigma^2/(4*pi),
    ||Psi_actual-Psi_ideal||_2^2
        <=pi*sigma^2/q^2 * sum_l ||e_l||^2.                  (2)

This is a JOINT-state bound: use |exp(i*x)-1|<=|x| and independent,
zero-mean coefficient registers. Independence of the e_l is not needed.
Pure-state trace distance is at most vector distance. Thus, if
sum_l E||e_l||^2<=L*E2,

    delta_phase <= min(1,sqrt(pi)*sigma*sqrt(L*E2)/q).         (3)

The comparison may retain all original classical samples, including b_l.
It changes the prepared states, not those samples. Repeated preparations of
one sample repeat its label and error; they do NOT create independent a_l.
The L in (3) counts prepared blocks, including repeats. Only the original
training samples supply fresh independent labels. State closeness does not
give an ideal phase oracle on arbitrary inputs or free controlled queries.

### A Positive-Fourier Reference, With Its Own Error Charge

On Z_q define

    t_sigma(r)=sum_(k in Z) exp(-pi*(r+q*k)^2/sigma^2),
    Z=sum_(r mod q) t_sigma(r)^2,
    g_q(r)=t_sigma(r)/sqrt(Z).

The ideal reference replaces each scalar truncated amplitude by g_q. Both
g_q and its discrete Fourier transform are strictly positive real functions.
For R_c<q/2, folding the omitted amplitudes and using their l1 tail gives

    ||g_R-g_q||_2 <= 2*sigma^2/(pi*R_c)
                              *exp(-pi*R_c^2/sigma^2).
    delta_shape <= min(1,2*sqrt(L*d)*sigma^2/(pi*R_c)
                              *exp(-pi*R_c^2/sigma^2)).       (4)

The first bound uses ||unscaled g_R||_2>=1 and
2*sum_(n>R_c) exp(-pi*n^2/sigma^2)
<=sigma^2/(pi*R_c)*exp(-pi*R_c^2/sigma^2). The product bound follows from
nonnegative scalar overlaps, not a multiplication of unnormalized vectors.

The source ledger for this route is delta_phase+delta_shape+implementation
errors, plus the separately charged discretization and anchor losses in the
original reduction. It has NO delta_amp, delta_eval, selector-hash error,
or scalar-modulus Q. Old scalar-source ledgers are not silently modified.
The held-out verification sample remains excluded from all tuning.

## 3. One-Block Information Certificate

Suppose Pr[s not in S]<=delta_s for S=[-R_s,R_s]^d, with integer R_s>=1
and 2*R_s<q. Put H=(2*R_s+1)^d. The following argument works for ANY
prior with this box-tail bound, independently of the uniform label a.

For a nonzero difference Delta=s-t of two box points, multiplication in the
cyclotomic FIELD over Q has nonzero integer determinant. Parseval and
arithmetic-geometric mean imply

    0<|det C_Delta|=|Norm(Delta)|
      <=||Delta||_2^d <=G=(4*R_s^2*d)^(d/2).                 (5)

Let r_Delta=rank_(F_q)(C_Delta), h_Delta=d-r_Delta. Integer Smith normal
form gives q^h_Delta dividing det C_Delta. Since X^d+1 is square-free
modulo q and all its irreducible factors have degree

    f=ord_(2*d)(q),

the CRT also says h_Delta is a multiple of f. The strict coefficient bound
makes Delta nonzero mod q, hence h_Delta<=d-f. Therefore a uniform rank bound is

    h_max=min(d-f, f*floor(log_(q^f)(G))),
    r_min=d-h_max.                                           (6)

Compute the floor by EXACT integer power comparisons, not floating logarithms.
If G<q^f, every relevant difference is a unit and r_min=d. Neither every
nonzero ring element nor every public label is assumed invertible.

Let mu(r)=g_q(r)^2 and m=max_r mu(r). The label-averaged overlap of a pair
of ideal states has the exact character identity

    E_a <Psi_(C_a*s)|Psi_(C_a*t)>
      =Pr_(c from mu^d)[C_Delta^T*c=0 mod q]
      <=m^(r_Delta) <=m^(r_min).                             (7)

Indeed C_a*Delta=C_Delta*a; averaging over uniform a enforces the kernel
condition. A rank-r homogeneous constraint determines r pivot coordinates
after the others are fixed. Coordinate independence bounds its probability
by m^r. This does not replace a negacyclic matrix by independent random rows.

The Fourier transforms of the envelopes are positive, so the classical
Bhattacharyya overlap of the two local Fourier-readout laws equals their
pure-state overlap. For fixed true s in S, an ML error toward t requires
p_t(Y)>=p_s(Y); its probability is at most their Bhattacharyya overlap.
Union bound, then average over a and any prior on S:

    E_a Pr[ML_S(Y)!=s] <=delta_s+min(1,(H-1)*m^(r_min)).       (8)

ML_S here enumerates S. This is an INFORMATION certificate, not a polynomial
decoder, a sample-complexity separation, or a performance guarantee for Babai.
Physical-source and sampler errors are additional terms, not included in (8).

### An Elementary Maximum-Mass Bound

Poisson summation makes t_sigma maximal at zero and gives

    Z>=sum_(n in Z) exp(-2*pi*n^2/sigma^2)>=sigma/sqrt(2),
    eta=2*exp(-pi*q^2/sigma^2)/(1-exp(-3*pi*q^2/sigma^2)),
    m<=min(1,(sqrt(2)/sigma)*(1+eta)^2).

For q>=2*sigma this is <=min(1,2/sigma). Thus a particularly simple,
conservative, EXACT rational certificate at integer sigma is

    (H-1)*2^(r_min) <= epsilon_ML*sigma^(r_min).               (9)

No tiny wrapping error is multiplied by H in this version; m bounds the
actual periodized amplitude-squared law directly. The finite implemented
source is connected to that reference by the additive state error (4).

## 4. Sharper Secret Tails, Including The Hidden Shape

The old exponentially small spherical tail and elliptical energy/Markov box
are valid but unnecessarily wide for this target.

For the spherical law D_(Z^d,rho), the scalar MGF implies

    Pr[||s||_infinity>R_s]<=2*d*exp(-pi*R_s^2/rho^2).          (10)

It suffices to take R_s>=rho*sqrt(log(2*d/delta_s)/pi).
Coefficient independence is not required for this union bound once the
scalar MGF is known.

For the elliptical lane, retain its ACTUAL hidden shared shape. Set
g=f_0=t=log d as in SOURCE_HARDNESS_AUDIT. Let x_j,y_j be independent
continuous D_(1/sqrt(2)) variables for j=1,...,d/2. Define

    Z_lat=sum_j (x_j^2+y_j^2),
    H_ii=t^2+g^2*(d*f_0^2/2+Z_lat), for EVERY coefficient i.  (11)

The identical diagonal follows from the flat absolute values of the
cyclotomic Fourier embedding, pairing conjugate eigenvalues. This does NOT
make H diagonal or replace H by its expectation. Conditional on H, the exact
discrete Gaussian MGF from the source audit bounds every coefficient by
2*exp(-pi*R_s^2/H_ii).

Since Var(x_j)=Var(y_j)=1/(4*pi), E exp(pi*Z_lat)=2^(d/2).
For u>0, Chernoff therefore gives

    Pr[Z_lat>z_star]<=exp(-u),
    z_star=(d*log(2)/2+u)/pi,
    h_star=t^2+g^2*(d*f_0^2/2+z_star),
    Pr[||s||_infinity>R_s]
        <=exp(-u)+2*d*exp(-pi*R_s^2/h_star).                  (12)

Choose u=log(2/delta_s) and
R_s>=sqrt(h_star*log(4*d/delta_s)/pi). This is an averaged-prior guarantee
with the hidden shape integrated out. It does not give the decoder that
shape. Do NOT condition the separate phase moment calculation on the shape
event without recomputing it; (3) uses the original unconditional E2.

## 5. Lower-Modulus References And Asymptotics

For d>=4 a power of two and q congruent to 3 or 5 modulo 8,
ord_(2*d)(q)=d/2. The sufficient all-differences-unit condition simplifies to

    4*R_s^2*d<q.                                             (13)

This is a PUBLIC choice of modulus, not postselection on a favorable secret
or label. The Ring-LWE theorem used in the source audit allows this modulus
class. Preserve its worst-case ideal-DGS scope and approximation factors;
this does not assert hardness of ordinary unstructured LWE or exact SVP.

The following distinct source uses the first prime above d^4 that is 3 or
5 mod 8, keeping the source audit's absolute error parameters:

    rho^2=d^(3/2)*(log d)^2+(log d)^2,
    E2_spherical=d*rho^2/(2*pi),
    E2_elliptical=[d^2*(log d)^2*((log d)^2+1/(2*pi))/2
                    +d*(log d)^2]/(2*pi).

Use delta_s=0.001, the ceilings from (10)/(12), R_c=sigma*sqrt(d), and the
smallest power-of-two sigma satisfying (9) for epsilon_ML=1e-8.
All three reference dimensions have integer sqrt(d).

| d | q | factor degree f | spherical R_s | elliptical R_s |
|---:|---:|---:|---:|---:|
| 64 | 16777259 | 32 | 183 | 197 |
| 256 | 4294967357 | 128 | 727 | 734 |
| 1024 | 1099511627803 | 512 | 2699 | 2399 |

| lane | d | sigma | log10 main ML bound | prior-tail bound | phase-error bound |
|---|---:|---:|---:|---:|---:|
| spherical | 64 | 1024 | -9.25464939 | 0.000907202 | 0.032522906 |
| elliptical | 64 | 2048 | -26.47698310 | 0.000977434 | 0.067934398 |
| spherical | 256 | 4096 | -38.00754150 | 0.000966461 | 0.003829601 |
| elliptical | 256 | 4096 | -36.94288807 | 0.000983083 | 0.003763717 |
| spherical | 1024 | 16384 | -185.42245495 | 0.000996494 | 0.000423070 |
| elliptical | 1024 | 16384 | -237.81293435 | 0.000999712 | 0.000367171 |

The q values were verified by trial division through their integer square
roots. Conditions (9), (13), 2*R_c<q and 2*sigma<=q passed exact integer
checks. Transcendental entries are 100-digit numerical references, rounded
up for displayed prior/phase bounds, NOT interval certificates. The shape
error (4) is below 1e-84 in all six rows. Include it positively in a production
certificate, along with discretization, anchor, precision and verification
losses. In particular, the d=64 physical source error is NOT negligible.

The same argument also works with the old q=nextprime(d^12). Even with the
old wide boxes, its multiplication-rank lower bounds are 56,256,1024 at
d=64,256,1024 for both lanes; d=64 has f=8, NOT d/2. Thus the lower-q variant
is not needed to rescue information sufficiency. It removes an unnecessary
large-modulus choice and yields a more useful classical attack target.

For fixed or inverse-polynomial delta_s, the sharper boxes scale as

    R_s,spherical=Theta(d^(3/4)*(log d)^(3/2)),
    R_s,elliptical=Theta(d^(1/2)*(log d)^(5/2)).

With sigma a sufficiently large constant multiple of R_s, the main ML error
is exponentially small when r_min=d. Public high-factor-degree prime families
q=Theta(d^a) satisfy the norm criterion for a>5/2 (spherical) or a>2
(elliptical). The associated sufficient phase bounds scale as

    O(d^(2-a)*(log d)^(5/2)), spherical;
    O(d^(3/2-a)*(log d)^(9/2)), elliptical.

These are sufficient asymptotic regimes, not necessary thresholds or finite
security estimates. q near d^3 is asymptotically enough for both lanes under
these conditions, but is NOT substituted into the displayed finite table.

## 6. Classical Baselines And Failed Shortcuts

**The original data is the baseline.** For the periodized actual state,
local Fourier measurement gives Y=b+nu mod q, with known independent scalar
noise nu. Under the ideal comparison it gives Y=C_a*s+nu. The two are not
interchangeable without (3). A classical sampler uses observed b, never the
hidden ideal frequency. The Gaussian probability surrogate has width
q/(sqrt(2)*sigma), with per-coordinate TV bounded by

    z/(1+z), z=2*exp(-pi*sigma^2/2)/(1-exp(-3*pi*sigma^2/2)).

This is the same positive-cross-term proof as PRIOR_CVP_BASELINE, valid also
for odd q. Add d*L times this error and the relevant shape/precision terms.
Adding independent noise cannot improve the information in b. No claim that
arbitrary later quantum computation is classically simulable follows.

For the spherical ORIGINAL one-block sample, secret and noise both have
width rho. Its joint-lift MAP baseline is the 2d-dimensional lattice

    B=[ I  0 ], target=(0,b), residual=(-s,e).
      [ C_a qI]

For ideal Fourier data use the same graph with top block w*I, where
w=[q/(sqrt(2)*sigma)]/rho, and charge the surrogate-noise approximation.
On physical Fourier data there is ALSO the original e; do not label the
ideal-noise MAP objective exact. Preserve all modular lift variables.
Marginal MAP sums over lifts and is not joint-lift CVP. The elliptical prior
has a hidden covariance: giving it to a benchmark is an oracle-assisted
control, not a legal baseline on the original problem. Euclidean CVP remains
a legal heuristic there, without an exact MAP claim.

**Inverting the public multiplier is not a decoder.** If a is a unit, the
coordinate permutation x=C_a^T*c makes the ideal phase <s,x>, but transforms
the envelope into g(C_a^(-T)*x mod q). For any invertible T,

    F_q U_T=U_(T^(-T)) F_q.

Consequently this operation followed by Fourier measurement returns exactly
C_a^(-1)*Y, a relabeling of the existing noisy readout. It does not turn the
envelope into an isotropic Gaussian. This statement covers this linear
permutation/readout, NOT arbitrary subsequent quantum operations.

**Uniformizing the coefficients destroys the source approximation.** With
uniform coefficients, any nonzero noise vector mod q makes the actual and
ideal phase states orthogonal. A tiny error in each original coefficient
therefore does not give a useful ideal oracle on the full coefficient cube.
The Gaussian code's overlap with the corresponding flat phase state is

    [ (sum_r g_q(r))^2/q ]^d,

independent of the phase, and tiny at these widths. Neither that overlap nor
the failure of diagonal filtering is a lower bound on every quantum decoder.

**Published quantum-example algorithms do not supply the missing access.**
Our coherent coefficient c produces effective label C_a^T*c and error
<e,c>, a correlated linear function of c which grows with the coefficient
range. It is not a uniform-label quantum example with separately bounded
errors over all labels. Supplying that stronger input would change the problem.

**The finite instances may be classically easy.** Large modulus and small
absolute error can make lattice attacks effective. A failed Babai run is
not hardness evidence; LLL/BKZ, enumeration and hybrid attacks must be
budgeted on the same original data. A finite attack success falsifies that
parameter claim, not every asymptotic quantum decoding possibility.

## 7. Checks Actually Run

Targeted mathematical controls only, not production validation:

- 3,072 exact norm/rank cases: d=2,4 with all nonzero coefficient vectors
  in [-2,2]^d, plus 120 seeded d=8 vectors, at q=3,5,7,17. Checked nonzero
  norm, norm bound, q-nullity divisibility, CRT degree and the rank bound.
  A necessary nonunit-difference control is d=2,q=5,Delta=(-2,-1), norm 5,
  rank 1. Treating all short differences as units without (13) would fail.
- 36 exhaustive image/kernel/character checks with arbitrary product laws
  at (d,q)=(2,3),(2,5),(4,3); maximum identity error 3.60e-16.
- Six complete d=2 local-readout ensembles, all labels, outcomes and nine
  box secrets, at (q,sigma)=(3,.8),(5,1.4),(7,2.2),(11,3),(17,5),(17,7).
  Maximum classical/quantum overlap discrepancy 1.78e-15; label-average
  discrepancy 1.93e-16. All per-secret ML union bounds held. The last two
  Gaussian-prior ML success references were 0.89652537 and 0.94727728;
  these are finite algebra controls, not candidate algorithms.
- 72 joint source-moment checks, including repeated/correlated errors;
  maximum squared-distance/bound ratio 0.860483.
- 36 complex public-inverse/Fourier identities; maximum error 2.23e-16.
- 108 finite-to-periodized shape controls, 36 maximum-mass controls and
  36 Gaussian readout-alias controls. A uniform-coefficient q=17 noise-one
  countercontrol had exactly zero numerical overlap with the ideal state.
- 120 conjugate-paired elliptical embedding diagonals and 24 exact-gamma
  tail comparisons checked (11)-(12). Hidden covariance was never treated
  as observed input.
- Six old-modulus integer width/rank references; six lower-modulus rows
  with exact width/norm/support checks and three trial-division prime checks.

These checks can falsify algebra or an implementation; they do not replace
independent proof review, establish novelty, or prove a scaling advantage.
No routine full test suite, registry run, CLI wiring or commit was performed.

## 8. Gemini Contract And Next Mathematical Work

Implement a DISTINCT native-RLWE phase source and certificate. Do not
overwrite scalar EDCP records, and do not import their error ledgers.
Record the exact input ring, prime certificate, factor degree, prior lane,
hidden-shape policy, original sample count, repeated-copy count, actual
sigma/cutoffs, (3)-(4), prior tail, and exact (6)/(9)/(13) witnesses.
Mark this derivation REVIEW PENDING; no automatic theorem promotion.

First implement attacks on original samples, then on their derived readout.
Compare d^4 and d^12 variants using separate IDs. Include spherical and
hidden-shape lanes, dimension/bit costs, LLL/BKZ and bounded enumeration,
residual verification, all failures and bounded negative-result records.
The held-out sample must never select the attack settings. Treat success
only on ideal data, or with a supplied hidden covariance, as a different result.

Regression controls must reject non-prime moduli for this certificate,
non-two-power degrees, incorrect multiplication ranks, uncharged support
folding, free fresh labels from repeated samples, and shape-aware attacks
presented as ordinary attacks. Include the nonunit Delta and public-inverse
controls above. Export complete machine-readable inequality witnesses,
not a single optimistic pass flag. Running full tests and live CLI workflows
belongs to that implementation pass.

Main-model work should seek an EXPLICIT efficient inverse/measurement
for either this prior-aware native Gaussian Fourier code or the distinct
covariant L2 target in NATIVE_RLWE_COVARIANT_DECODER_TARGET, or a strong
classical attack that falsifies their relevance. A generic PGM, uncompiled inverse
isometry, Gaussian-to-flat substitution, or Grover search over all small
secrets does not resolve the computational bottleneck. An eligible proposal
must state its actual coherent operations and expose modular carry/error
decoding rather than assume it as a subroutine.

## 9. Primary Literature Checked

- [Lyubashevsky--Peikert--Regev toolkit, Section 2.5.5 and Lemma 2.24](https://sites.cc.gatech.edu/fac/cpeikert/pubs/toolkit.pdf):
  cyclotomic prime residue degrees and normal-form Ring-LWE. The rank,
  maximum-mass and finite-source arguments above are local derivations.
- [Peikert--Regev--Stephens-Davidowitz, Theorem 6.2 and Corollary 7.3](https://eprint.iacr.org/2017/258.pdf):
  the previously audited elliptical/spherical hardness routes allow general
  moduli. Their normalization and approximation losses remain required.
- [Grilo--Kerenidis--Zijlstra, Learning with Errors is easy with quantum samples](https://arxiv.org/pdf/1702.08255):
  its quantum-example input is stronger than the classical samples used here.
  It does not supply a decoder for (1) or a classical-to-quantum conversion
  meeting that input promise.
