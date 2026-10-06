# The Implicit PGM Normalization Trap

LOCAL DERIVATION / REVIEW PENDING. No novelty, independent review, accepted
candidate, efficient native decoder or speedup. This is one explicit route's
resource gate, NOT a lower bound for arbitrary DHSP algorithms or all QSVT.

## The Actual Accessible Circuit

Use G=q^n, N=2^m, Boolean map F(x)=A*x modq and the supplied unknown state

    |psi_u> = N^(-1/2) sum_x chi_u(F(x)) |x>.

The entire family |psi_s> for KNOWN trial s can be prepared by public arithmetic:
Hadamards on x followed by its known phase. This does not prepare the unknown
u or its inverse. Prepare a candidate register uniformly over s; conditionally
apply the inverse known trial phase on x, then Hadamards on x. The known
unitary U and its inverse are accessible without fresh unknown input copies.
Public phase precision still needs a gate ledger in any scalable construction.

Input projector: candidate register zero, arbitrary x. Output projector: x zero,
arbitrary candidate. These are DIFFERENT projector subspaces of the same space.
Their rectangular projected-unitary block is exactly

    T = G^(-1/2) sum_s |s><psi_s|.

Do not advertise a differently normalized ordinary block without proving its
implementation. Materializing the bounded U in this module costs G*N space and
is EXPONENTIAL calibration; its public symbolic gate structure is not a decoder.

## Why It Looks Better After Discarding Failure

Let eta_t count Boolean preimages and |F_t> denote normalized nonempty fibers.
The right singular vectors of T are |F_t>; the left vectors are the public
group characters |chi_t^*> on the candidate register; singular values are

    sigma_t = sqrt(eta_t/N), sum_t sigma_t^2=1.

For EVERY A and EVERY actual u, measuring candidate u in the output block
has unconditional probability exactly 1/G. The total herald is

    h_A = sum_t eta_t^2/N^2.

The complete IID native source moments from the preceding adaptive audit give

    E_A h_A = (N+G-1)/(N*G).

In the POOLED source experiment, correctness GIVEN a herald is therefore
N/(N+G-1). At +16 this exceeds 65536/65537, yet unconditional correctness
is STILL 1/G. The fraction of accepted runs can be exponentially tiny.
This is not the mean of per-matrix conditional probabilities; do not confuse
these sampling protocols. No herald is normalized away in the physical tests.

Even condition number 1 does not solve this. On a bijective Boolean map with
N=G, all sigma_t are 1/sqrt(G). Their ratio is 1, but their absolute scale
is tiny. A polynomial-time state-preparation unitary and a high conditional
confidence are not a polynomial-time inverse/measurement implementation.

## A Pointwise Gate For Bounded Odd Spectral Polynomials

Consider an odd polynomial p of degree at most d, bounded in magnitude by 1
on the ENTIRE interval [-1,1]. It can depend on ALL public A. A QSVT-style
transformation of this projected T preserves its singular vectors and sends
|F_t> to p(sigma_t)|chi_t^*> in its successful output block. Decode the
candidate basis label directly. Its correct probability for each u is

    P_correct = (1/G) |sum_t sigma_t*p(sigma_t)|^2.

Bernstein's polynomial derivative inequality gives
|p'(z)|<=d/sqrt(1-z^2). Since p(0)=0,

    |p(z)| <= d*arcsin(z) <= (pi*d/2)*z, 0<=z<=1.

Triangle inequality and sum sigma_t^2=1 now give

    P_correct <= min(1, pi^2*d^2/(4*G)) < min(1, 5*d^2/(2*G)),

where the strict inequality is only for the unclamped constants. The exact
artifact uses the conservative rational 5/2 coefficient. Thus success >=tau
requires d>=sqrt(2*G*tau/5). This is an exponential degree for inverse-
polynomial tau when log2(G)=nL grows. It holds for EVERY A; no random spectral
tail, minimum-eigenvalue promise or worst-mode approximation is needed.

The standard inequality is recalled as Eq(1.1) by
[Kalmykov, Nagy and Totik](https://www.math.u-szeged.hu/pot/Rational.pdf).
The local application above is not a new approximation-theory theorem.

## Keeping All Branches And Allowing Classical Re-Guessing

For a collection of successful branch polynomials p_j, each odd of degree at
most d, require sum_j |p_j(z)|^2<=1 throughout [-1,1], not a separate bound
of 1 per branch. Apply the scalar Bernstein inequality to every unit-vector
projection of the polynomial vector. This gives

    ||p(z)|| <= d*arcsin(z) <= (pi*d/2)*z.

It also holds for complex coefficients by taking real phase projections of
derivatives. Arbitrarily many jointly normalized branches therefore obey the
same unconditional bound, without multiplying it by the number of branches.

For uniform u, the output law is translation covariant. An optimal classical
guess can shift the measured label by a branch-dependent offset delta_j.
The branch amplitude vectors are sums of sigma_t*p_j(sigma_t) multiplied by
unit phases chi_(delta_j)(t). For each t these phases preserve the branch norm;
the same triangle bound applies to their vector sum. Hence arbitrary classical
guessing from the label AND successful branch is also bounded in mean over the
uniform secret. This latter claim is NOT pointwise for every secret: always
guessing one fixed secret is the standard counterexample to that overreach.
Failure registers are not granted as an extra decoder; decoding them needs a
separate analysis. Other output unitaries or altered singular vectors are open.

## Physical Controls, Not Merely A Spectral Spreadsheet

The bounded module builds the actual known U, verifies unitarity and its
rectangular block, and retains the entire unknown-input output vector.
Use input/output reflections R_in,R_out. Iterating

    Q = -U*R_in*U^dagger*R_out

r times after U gives p_(2r+1)(z)=sin((2r+1)*arcsin(z)), an odd bounded
polynomial. Degrees 1,3,5,7 are evaluated against every secret on four declared
matrices, including the zero source and the q4 adaptive parity example. All
failure probabilities remain charged. Optimal classical re-guessing is also
computed rather than assuming the raw label is optimal under overshoot.

Native 16/512/256-matrix censuses verify herald moments without favorable
sampling. At n=8/16/32,L=4n+1,m=nL+16 and degree=(nL+m)^2, rational success
upper bounds are respectively at most 2^-226,2^-994,2^-4074.

## Literature And Attempt To Falsify The Scope

[The polar-decomposition PGM algorithm](https://arxiv.org/html/2106.07634),
Lemma1, Algorithm2 and Theorem3, explicitly charges subnormalization and the
inverse smallest singular value. Its literal ordinary-block construction is
not the different-projector circuit above. Neither expression becomes cheap
merely because trial states have compact circuits. No improvement over that
paper's algorithms or optimality theorem is claimed here.

[The Petz implementation](https://arxiv.org/html/2006.16924) also tracks
state access and spectral resources. It does not grant a free ensemble inverse.

FALSIFY A UNIVERSAL CLAIM: take q=2,A=I,m=n. Independent Hadamards decode
u exactly in linear quantum gates. Our comparison T still has singular values
2^(-n/2), condition number 1, and its univariate polynomial route still obeys
the gate. Thus the obstacle belongs to this representation, NOT the problem.
For known binary-digit labels at q4, degree3 amplification already succeeds
exactly; this small control is not a scalable native-source selector.

This does not cover label-dependent fiber-wise transformations, a better
normalized encoding with a proved circuit, arbitrary interleaved quantum
algorithms, additional unknown states, direct structured decoding or usable
information in failure branches. One must construct and cost those escapes,
not invoke their names or treat them as already impossible.

## Research Action

Stop proposing compact trial-state preparation followed by generic polar
filtering as the missing breakthrough primitive. A useful replacement must
change the normalization/source geometry or implement a different decoder.
The direct verified-witness filter remains an alternative conditional interface;
it still needs its actual native polynomial finder and natural-source proof.

Module/test stem: `dcp_pgm_projected_encoding`. Artifact:
`research/classical_baselines/dcp_pgm_projected_encoding.json`.
Independent-language checker:
`research/certificates/dcp_pgm_projected_encoding_crosscheck.js`.
Production CLI/registry/full-suite wiring remains delegated to Gemini.

All-record follow-up: [failure readout audit](DCP_PGM_FAILURE_READOUT.md)
retains every computational-basis signal and auxiliary outcome. It derives a
matched local reference channel and a source-linked hybrid gate for a declared
projector/auxiliary processor class. Arbitrary terminal collective measurements
and different signal interleavings are STILL not excluded.
