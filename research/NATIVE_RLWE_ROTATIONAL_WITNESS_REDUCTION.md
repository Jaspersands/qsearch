# Native Ring-LWE: One Rotational Certificate, Not d Searches

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to NATIVE_RLWE_SINGLE_WITNESS_TARGET. No novelty, efficient finder,
independent verification, security estimate or quantum algorithm is claimed.
This is a structural simplification of a conditional dual-style decoder.
Classical LLL solves every small identity control below; none is a quantum
separation or a test at the actual source's noise/prior parameters.

FINDER FOLLOW-UP: NATIVE_RLWE_SPARSE_WITNESS_AUDIT rules out the original-
coefficient sparse-inversion output class on typical native labels at the
specified radius. Dense/reduced-basis finders and nonunit-h constructions
are not excluded. It does not supply an efficient generator.

SEPARATE NONUNIT FOLLOW-UP: NATIVE_RLWE_NONUNIT_WITNESS_AUDIT rules out
that output certificate class, even with adaptive h, under the high-degree
source and this norm/box decoder. It does not invalidate rational inversion
in other regimes or exclude moment-based sampling/dense unit-h generators.

CLASSICAL FOLLOW-UP: `NATIVE_RLWE_CLASSICAL_COVER_CERTIFICATE.md` verifies
an actual native d64 kernel's all-coset Babai profile and original-coordinate
controls for both d^12 lanes. Classical competitors may use longer
witnesses than an internal Gaussian benchmark if the ORIGINAL decoder
gate passes. Full-rank sublattices suffice. Read the controlled-index
completion in `NATIVE_RLWE_BALANCED_NTRU_TARGET.md` before requiring a
primitive full basis. These finite results do not solve growing dimensions.

## 1. Decision

For the ORIGINAL negacyclic ring input, one coordinate-neutral witness
already supplies all d coordinate witnesses by signed monomial rotation.
Do not budget d independent searches, insist on independent rotated noise,
or demand a full short basis when this finite decoder needs only one vector.

There is also a broader sufficient target: a short pair with syndrome
t*h, where h is a short known integer polynomial. All rotated measurements
give a noisy known convolution of the original secret. Decode that integer
convolution and invert it over the rationals. Modular invertibility of h
is unnecessary. This enlarges the admissible output class, not the set of
available polynomial-time operations.

A chosen scalar label has an exact optimal spacing rule. Consequently an
alternative target is ONE short preimage at ONE predetermined syndrome,
not chosen access on every syndrome, Gaussian sampling, coherent erasure,
or a quantum example oracle. Finding that preimage remains unsolved.

## 2. Signed Rotations And The Exact Transpose Convention

Let S be the integer signed cyclic shift

    S*e_j=e_(j+1) for j<d-1, S*e_(d-1)=-e_0.

Then S^d=-I, S^T=S^(-1), and S is orthogonal. The multiplication matrix
of a coefficient polynomial a is

    C_a=[a, S*a, ..., S^(d-1)*a].

Both C_a and C_a^T commute with S. Retain the ORIGINAL actual input

    F=[C_(a_1)^T,C_(a_2)^T], b=F^T*s+e mod q,
    T=diag(S,S), F*T=S*F.                                 (1)

For c=(c_0,c_1) with F*c=t*e_0, set c_j=T^j*c. Exactly

    F*c_j=t*e_j mod q, ||c_j||=||c||,
    w_j=b dot c_j=t*s_j+e dot c_j mod q.                   (2)

One checked witness with the original single-witness spacing certificate
therefore decodes ALL coordinates. The same global ||e||<=E_max event
bounds every error |e dot c_j|<=E_max*R. No independent-noise assumption or
union factor d is needed. The small prior is the ORIGINAL secret box.

The entire vector can be computed classically as

    w=C_(c_0)^T*b_0+C_(c_1)^T*b_1 mod q.                  (3)

Straight quadratic integer convolution suffices for polynomial cost; a
faster exact convolution is optional. This is d correlated equations from
the SAME two retained records, not d additional source samples. Ordinary
unsigned cyclic shifts are WRONG for X^d+1. A general noncirculant public
matrix does not satisfy (1), even when its first witness is valid.

The orbit of c need not be a saturated lattice basis and spans at most d
of 2d dimensions. That does NOT invalidate (2): this decoder does not need
a full basis, uniform lattice samples or Gaussian label diversity. Earlier
basis/sampler index warnings still apply to those stronger tasks.

There is a related batch saving for the HOMOGENEOUS Gaussian route. The
map T^j sends K_0 isometrically onto K_j, so it pushes a centered Gaussian
on K_0 to the required Gaussian on K_j. One batch of m INDEPENDENT K_0
samples can be reused for all d coordinate scores, with correlated columns
but independent sample rows. Apply concentration separately per coordinate
and union bound; coordinate independence is unnecessary. This reduces
primitive calls from d*m to m, not the unresolved cost per sample. It does
not provide chosen-coset access or make rotations of ONE vector an IID
batch. Approximation and failed-call losses still need their own ledger.

## 3. Short Polynomial Syndromes Also Suffice

Let d be a power of two, h a nonzero integer polynomial of degree <d,
and H=C_h^T. The polynomial X^d+1 is irreducible over Q, so h is a nonzero
element of a FIELD over Q and H is invertible over Q. Alternatively verify
the integer matrix's nonzero determinant directly for other rings.

Require a finite public certificate

    ||c||^2<=R^2, F*c=t*h mod q,
    U=R_s*||h||_1 integer, 2*U<q,
    min_(1<=Delta<=2*U) ||Delta*t||_q>2*B,
    B=E_max*R, det(H)!=0.                                 (4)

There is no requirement that det(H) be a unit modulo q. For R_s>=1 the
box condition also excludes a nonzero h that is zero modulo q.

The commutative ring identities, INCLUDING the adjoints, give

    [C_(c_0)^T,C_(c_1)^T]*F^T=C_(F*c)^T=t*H mod q,
    w=t*H*s+epsilon mod q,
    epsilon_j=e dot T^j*c, |epsilon_j|<=B.                 (5)

The INTEGER z=H*s has every coordinate in [-U,U]. For each coordinate
choose the unique r in that interval satisfying ||w_j-t*r||_q<=B.
Its uniqueness follows from (4), and the true z_j always passes on the
global good-noise/prior event. Then solve H*s=z OVER Q and require an
integral solution in the ORIGINAL secret box. A nonintegral/out-of-box
answer is a rejected output, not a rounded secret guess.

Exact rational elimination is polynomial in d and input bit length. With
polynomial ||h||_1, Hadamard bounds give polynomial determinant/adjugate
bit lengths. Poor real conditioning is not permission to lose arithmetic
precision, but no approximate inverse is needed after exact z recovery.
Brute-force coordinate scoring costs O(d*(2*U+1)) torus comparisons,
polynomial here; do not enumerate every full secret or coefficient tuple.

For h=2+X, ||h||_1=3, det(C_h)=2^d+1 and its singular values are >=1.
It is a simple nonmonomial output control, not a claimed hard family.
At d=4,q=17 it is NONUNIT modulo q, yet every secret in [-1,1]^4 can be
recovered from exact z modulo q since z is in [-3,3]^4. This illustrates
why substituting a modular inverse for the rational solve would falsely
reject valid certificates. This particular no-noise case is only an
identity control with an easy planted input, not a source attack.

Allowing bounded h might help a future finder avoid exact coordinate
neutrality. It also gives stronger classical dual/hybrid solvers more
freedom. Test both effects. No claim that this enlargement helps quantum
methods more than classical methods is supported.

## 4. A Predetermined Scalar Can Be Optimally Spaced

For ANY integer q and U>=1 with 2*U<q, define D=2*U+1. Then

    max_t min_(1<=Delta<=2*U) ||Delta*t||_q=floor(q/D),
    t_star=floor(q/D) attains the optimum.                 (6)

Proof of upper bound: the D residues 0,t,...,(D-1)*t are either not all
distinct, giving zero separation, or have D positive cyclic gaps summing
to q. Some gap is <=floor(q/D), and its endpoint difference is one of the
allowed Delta*t. For t_star, the residues 0,t_star,...,(D-1)*t_star have
D-1 gaps equal to t_star and a final gap q-(D-1)*t_star>=t_star. Thus the
minimum equals t_star. Neither primality nor inversion of t is used.

The best possible scalar spacing certificate at radius R is consequently

    floor[q/(2*U+1)]>2*E_max*R.                            (7)

This is a necessary and sufficient condition for SOME scalar label to
pass this uniform interval separation test, not a necessary condition for
every possible secret decoder. It does not say an arbitrary short vector's
label is good or that it can be scaled to t_star without becoming long.
Multiplying a witness by t_star/t mod q generally destroys the norm bound.

If a finder can return ONE c with

    F*c=t_star*e_0 mod q, ||c||<=R,                        (8)

then (2)-(3) decode the original secret. The broader version replaces
e_0 with a fixed h and uses U=R_s*||h||_1. This is a single affine short-
preimage task on actual public F, not a full chosen-syndrome oracle.

The existing d^12-modulus references satisfy (7) for h=1 and h=2+X in
both noise lanes. Ratios t_star/(2*B), NUMERICAL REFERENCES, are:

| d | spherical h=1 | elliptical h=1 | spherical h=2+X | elliptical h=2+X |
| ---: | ---: | ---: | ---: | ---: |
| 64 | 1344.8527 | 1196.1865 | 449.1000 | 399.4029 |
| 256 | 92189.5931 | 92897.6370 | 30743.9509 | 30979.9384 |
| 1024 | 7196631.8753 | 9328251.6024 | 2399173.5409 | 3109849.2143 |

Every >1 comparison was separately checked by EXACT integers against
the saved prime/energy/radius artifact. These enormous margins are also
a warning: run strong original-data primal attacks before spending on
quantum witness generation. They do not establish classical hardness.

For the family R=2*sqrt(d*q), a sufficient unrounded modulus threshold is

    q>16*d*E_max^2*(2*U+1)^2,                             (9)

plus a strict margin for floor(q/D). The exact test (7) is authoritative;
(9) alone without that margin is not. Increasing q improves a decoder's
noise margin, not its quantum speedup. The source theorem and all prior/
normal-form/anchor/rounding/held-out losses remain separate obligations.

## 5. Existence At A Fixed Syndrome, Not A Finder

For analysis only, define the unwrapped integer Gaussian partition

    Z_sigma(u)=sum_[F*c=u] exp(-2*pi*||c||^2/sigma^2),
    Theta(s)=sum_(z in Z) exp(-pi*z^2/s^2).

Suppose the FULL syndrome laws at BOTH amplitude widths sigma and
sqrt(2)*sigma are eta-relatively flat, with eta<1. For the conditional
law at any fixed u, exponential tilting gives

    Pr[||c||>sigma*sqrt(d) | F*c=u]
      <=exp(-pi*d)*Z_(sqrt(2)*sigma)(u)/Z_sigma(u)
      <=(1+eta)/(1-eta)*2^d*(1+delta_theta)^(2*d)*exp(-pi*d),
    delta_theta=2*exp(-pi*sigma^2)/(1-exp(-3*pi*sigma^2)). (10)

Here n=2d. Poisson summation bounds
Theta(sigma)/Theta(sigma/sqrt(2))<=sqrt(2)*(1+delta_theta).
The positive theta correction is retained, not numerically set to zero.
When (10)<1, EVERY fixed syndrome, including t_star*h, has an admissible
short preimage. This uses a two-width ALL-syndrome flatness event, not an
unsupported centered-lattice covariance theorem on an affine coset.

The earlier CRT Fourier-sum method can certify each width separately;
charge the union of its exceptional-label bounds. Flatness at one width
alone is not here asserted to imply the other event. The current d^12
arithmetic artifact certifies the earlier single-width bound, not a new
production two-width certificate. That extension belongs in Gemini's
verification ledger. Any implemented approximate finder needs its OWN
output validity/failure bound; an analytical Gaussian is not supplied.

For a free label on the line span(h), the neutral lattice has determinant
q^(d-1), assuming prime q, F surjective and h nonzero modulo q. Fixing t
instead gives an affine coset of ker(F), whose determinant is q^d. That
one extra factor q must not be hidden. Neither determinant nor existence
specifies how to find a short point in the natural coefficient metric.

## 6. Try To Kill The Quantum Shortcut

Preparing an ambient product Gaussian and checking a FIXED syndrome has
acceptance in [(1-eta)/q^d,(1+eta)/q^d] on its flatness event. Generic
amplitude amplification costs order q^(d/2), before precision/tail costs.
Checking only membership in the line span(h) instead accepts about
q^(-(d-1)); generic amplification remains order q^((d-1)/2), before
norm/spacing rejection. These are costs of these specific constructions,
NOT lower bounds on every algorithm that can exploit public F.

A uniform superposition over the public finite-field kernel is easy to
prepare by known linear algebra. It does not supply the narrow Gaussian
weights or useful short representatives. Its subgroup is already known;
ordinary abelian HSP Fourier sampling reveals no missing hidden group.

The fixed-label task is an AFFINE natural-metric short-preimage problem.
The free-label task is a coordinate-neutral Euclidean lattice problem,
not a rank-two R-module just because F came from two ring elements. In
general multiplying a neutral witness by an arbitrary ring polynomial
moves its syndrome off the chosen line. Monomial rotation changes WHICH
line is used; it does not make the original neutral lattice an R-module.

Principal-ideal arithmetic does not supply bounded Bezout coefficients
for this task. Module lattice reductions must charge their actual field-
dependent CVP/SVP oracles and approximation losses. A quantum label on an
oracle-based wrapper is insufficient: [classical module-LLL work](https://eprint.iacr.org/2022/1356.pdf)
also retains a field-dependent CVP oracle. The [earlier module-LLL paper](https://eprint.iacr.org/2019/1035.pdf)
separately describes its rank-two and fixed-field-CVP subproblems.

This decoder is in the established dual/hybrid neighborhood, not a new
paradigm. [Small-secret dual attacks](https://www.iacr.org/archive/eurocrypt2017/10210169/10210169.pdf)
already exploit short relations that eliminate subsets of secret
coordinates. A real quantum contribution must lower the fully charged
cost of the original-input problem, not just exploit a familiar decoder.

Mandatory competitors are ORIGINAL-data primal CVP/BDD, ordinary and
module LLL/BKZ, free-label neutral relations, fixed-label affine short
preimages, and bounded short-polynomial syndromes. Include preprocessing,
retries, verification, bit complexity and the actual hidden-shape access
contract. Do not rank a finder against only a deliberately frozen native
walk or exponential reference enumeration.

## 7. Exact Controls Actually Run

Reproducible standalone probe:

    python research/certificates/native_rlwe_rotational_witness_probe.py

Seed 290951, exact SymPy/integer calculations:

- 16 ORIGINAL uniform-ring label inputs at d=2,4,8,16 and q=1009,5003,
  conditioned on a_1 being a unit. Prior radius ONE and total noise norm
  ONE were chosen for identity controls, NOT substituted source parameters.
- Classical LLL on the free-label line lattices found all 32 tested h=1
  or h=2+X certificates. Exact lattice determinants, syndromes and score
  spacing passed. All 240 decoded secret coordinates and all 240 signed
  orbit/norm identities passed. This is NO asymptotic solver guarantee.
- 208 unsigned-rotation equations failed as expected. All 32 deliberately
  nonring matrices retained the first witness but broke its rotation rule.
- All 32 zero-label controls failed eligibility. All 32 explicit out-of-
  noise-contract controls confidently decoded a DIFFERENT secret. Retain
  those failures: verification does not make a false noise promise true.
- Exhaustively checked optimal spacing (6) in 65 small prime/composite
  modulus/interval cases, not just prime q or unit t.
- All 81 d=4,q=17 nonunit-polynomial/no-noise controls recovered by exact
  rational inversion. Their deliberately easy inputs are not source data.
- All 12 fixed-label inequalities at the saved d^12-modulus references
  passed exact integer tests; displayed ratios are only numerical summaries.

No production CLI, live candidate/registry promotion, full test suite or
commit. Independent reduction/source review and actual-source classical
baselines are still required. The probe checks mathematical identities,
not the implementation of an unavailable quantum witness generator.

## 8. Next Theory Task And Gemini Integration Contract

Main-model task: a genuinely new, costed structural algorithm for ONE
original-coordinate short relation/preimage, or a decisive classical
falsifier. Do not return to full DGS merely because earlier wrappers used
it. Improving a conditional decoder further has diminishing value until
the finder or its stronger classical competitor advances.

Gemini: replace d independent neutral-finder calls by one exact signed
orbit where (1) is certified. Preserve a nonring fallback only as a
different model, not backward compatibility for a false ring identity.
Store base witness, label, syndrome polynomial, original prior/noise
contract, exact spacing and all source/preprocessing/failure losses.
Add the h-polynomial and predetermined-label tasks as separate backends,
not aliases that pretend free-label finding provides chosen-label access.

Port the probe's controls to the routine suite. Run actual-source primal
and lattice baselines first, report unsuccessful attempts too, and check
the two-width CRT/existence ledger without calling it a sampler. Keep
efficient generation, independent review and source applicability OPEN.
