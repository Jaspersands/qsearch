# Structured EDCP: Polynomial Phase Lifting And Linearization

Date: 2026-09-28. LOCAL DERIVATION / REVIEW PENDING.

This tests a concrete route: use native Gaussian phase states as reusable
programs to create quadratic probes, then apply polynomial phase linearization.
Approximate kickback is legitimate; transferring the published decoder misses
its amplitude promise. No new algorithm, novelty, independent verification,
or speedup is claimed. Gemini owns production implementation and full tests.

## 1. Candidate And Published Interface

Use actual direct-phase registers

    |R_k> = sum_z g_sigma(z)*exp(2*pi*i*k dot z/Q)|z>

and fresh workspace h_tau(x). Reversibly add a quadratic F(x), such as
negacyclic squaring, to the source register. If this barely changes its
Gaussian envelope, the intended workspace phase is
exp(-2*pi*i*k dot F(x)/Q). Combine probes, cancel quadratic terms, and
try to Fourier-read exact linear equations for the hidden secret.

[Decker--Hoyer--Ivanyos--Santha, Section 2.1 and Theorem 1](https://arxiv.org/pdf/1305.1543)
provide real precedent using uniform finite-field polynomial graph states.
Their quadratic construction finds an isotropic direction, adds a uniform
register, shifts input coordinates, measures them, and Fourier-reads a
remaining linear phase. Uniform amplitudes matter. Our Gaussian inputs,
composite modulus and growing coefficient dimension do not meet that
theorem's input promise. This audit concerns the attempted transfer, not
the published theorem, and assumes no stronger oracle.

## 2. Read-Only Phase Programs Reduce To One Reused Fourier Sample

With the negative Fourier convention, controlled translation
|x>|z> -> |x>|z+F(x)> is diagonal in the program's Fourier basis. At label
y its workspace action is exp(-2*pi*i*y dot F(x)/Q).

Allow many such calls, arbitrary intervening workspace gates, workspace
measurements and classical feed-forward. Initially program and workspace
are independent, or a specified classical mixture of products. No program
gate mixes its Fourier labels. Finally discard or Fourier-measure it.
The exact workspace channel is then

    sample Y ONCE from the program's local Fourier law;
    replace every call by the known Y-dependent workspace phase;
    reuse that SAME Y for the entire computation.                        (1)

Each branch Kraus operator is block diagonal in Y. Tracing or Fourier-
measuring the program removes off-diagonal Y,Y' entries irrespective of
when they were dephased. This is deferred measurement with an explicit
source contract, not a new simulation theorem. Several programs require
their JOINT Fourier law; independence needs the actual product premise.
Common-secret/input conditioning cannot be discarded.

The workspace algorithm remains QUANTUM. Arbitrary processing on known Y
is not classically simulated. The missing breakthrough becomes an efficient
quantum decoder on classical local-readout data. Other secret-bearing
workspace states remain resources; unspecified initial quantum correlations
are outside this contract.

For retained input, use the lawful local-readout sampler and full ledger in
`STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md`. Do not give a simulator
ideal k=s*v or apply that sampler to standalone phase-state access.

Many probes from one program share a latent Y, not independent noisy phase
coefficients. They can reveal Y, already obtainable by one measurement.
Resampling per call is wrong: F followed by -F must cancel exactly.
Keeping the program coherent is insufficient unless a later operation
actually uses interference between Fourier labels in a secret-relevant output.

## 3. Legitimate Kickback With A Disturbance Budget

For normalized nonnegative program envelope g, compare exact translation
with [sum_x h(x)*exp(-2*pi*i*k dot F(x)/Q)|x>] tensor |R_k>. Define
C_g(f)=sum_z g(z)*g(z-f). Their inner product is real and equals

    c_bar=E_(X~|h|^2) C_g(F(X)),
    D_trace(exact,ideal product)=sqrt(1-c_bar^2).                          (2)

The earlier measured-target identity does not prohibit approximate hidden-
phase kickback with a coherent target. It identifies the noise/correlations
that an exact-oracle substitution omits.

For identical product scalar envelopes, put C1=C_gscalar(1). Telescoping
integer translations gives 1-C_gscalar(f)<=f^2*(1-C1). Overlaps are in
[0,1], so 1-product_i C_i<=sum_i(1-C_i). For any integer translation lifts,

    D_trace(exact,ideal product)
      <= min(1,sqrt(2*(1-C1)*E||F(X)||^2)).                               (3)

These are finite-modulus bounds; poor lifts weaken them. Add truncation and
preparation errors. Repeated-use approximation must concern the joint state,
not independently idealized probes. Equation (1) holds even if (3) is poor.
Ignoring lattice/wrap corrections, Gaussian widths give
1-C1 approximately pi/(2*sigma^2) and E[X^4] approximately
3*tau^4/(16*pi^2). Gentle scalar squaring needs tau^2/sigma small.

For native R=Z[X]/(X^d+1), d>=2 a power of two, Q=q^d+1,
E_q(x*x)=E_q(x)^2 mod Q. This creates a structured phase without a new
oracle. For independent symmetric integer coefficients with variance v2
and fourth moment m4, the exact negacyclic identity is

    E||X*X||^2=2*d^2*v2^2+d*(m4-3*v2^2).                                (4)

In the scaled-isometric embedding, squared root powers sum to zero, giving
this fourth moment at each root; Parseval gives (4). At d=1 use m4 instead.
Gaussian probes suggest disturbance of order d*tau^2/sigma. Use exact
moments for symmetric truncated integer priors: centering an even-modulus
periodic law can break exact zero mean at its boundary. This is a valid
construction budget, not a decoder or an efficient hidden-polynomial oracle.

## 4. Weighted Phase Linearization Has A Readout Penalty

Grant quadratic cancellation and its direction free. Let m input registers
over Z_Q have ANY density matrix rho with diagonal G(c)^2, where
G(c)=product_i g_i(c_i), g_i>=0 and sum_x g_i(x)^2=1.

Append Q^(-1/2)*sum_x |x>. Choose delta BEFORE measurement, subtract
delta_i*x from source coordinate i, and measure those coordinates to z.
Fourier-measure the appended register to P. Fix a target lambda(z) before
seeing P; it may depend on hidden parameters when defining correctness.
Then

    Pr[P=lambda(z)] <= B(delta),
    B(delta)=(1/Q)*sum_(r in Z_Q) product_i C_i(r*delta_i),
    C_i(a)=sum_u g_i(u+a)*g_i(u).                                         (5)

No purity, Gaussianity or quadratic cancellation is assumed. Equality holds
for a pure input whose phase becomes linear in x, at that linear coefficient.

Proof: post-z density is rho(z+delta*x,z+delta*x')/Q. Positivity bounds its
absolute value by G(z+delta*x)*G(z+delta*x')/Q. Fourier expansion and the
triangle inequality bound success by Q^(-2) times the sum of these envelope
products over z,x,x'. Set r=x-x', translate z, and sum the Q choices of x'
to obtain (5).

ACTUAL reduced probes from controlled addition retain their coordinate
probabilities even when kickback is not gentle. Thus (5) applies without
adding a constant approximation error to a tiny ideal bound. Preprocessing
that changes the specified diagonal needs a new calculation.

If delta_j is a unit, its multiples permute Z_Q and C_i<=1 gives

    B(delta)<=sum_r C_j(r*delta_j)/Q=||g_j||_1^2/Q.                       (6)

For a nonunit, use gcd(delta_j,Q)*||g_j||_1^2/Q, capped at 1; it may be
vacuous. A nonzero field direction has a unit coordinate, but that fact
cannot be assumed at the native composite modulus.

A list of at most J frequencies has success <=min(1,J*B(delta)). Selecting
some z does not raise UNCONDITIONAL success: acceptance times conditional
list success obeys the same bound. This is not an arbitrary amplification
lower bound. Coherent amplification or a different measurement needs its
own implementation and correctness test; a wide noisy constraint could
contain exponentially many Fourier bins.

For a nonuniform appended amplitude h, the bound gains C_|h|(r)<=1 inside
(5). Narrowing this register cannot fix exact modular-frequency readout.
Choosing directions after z or applying arbitrary later residual operations
is outside this specified stage.

### Explicit Gaussian Bound

For the normalized periodized amplitude of width tau, put

    theta(tau)=sum_(n in Z) exp(-pi*n^2/tau^2),
    Z_period=sum_(x mod Q) [sum_n exp(-pi*(x+nQ)^2/tau^2)]^2.

Then ||g||_1^2=theta(tau)^2/Z_period. Positivity and Poisson summation give
Z_period>=max(1,tau/sqrt(2)); monotone integration gives theta(tau)<=1+tau.
The unit-coordinate success bound is therefore

    min(1,(1+tau)^2/[Q*max(1,tau/sqrt(2))]).                              (7)

For tau>=1 this is <=4*sqrt(2)*tau/Q. Even granting 1<=tau<=d^10 and
q>=d^12, Q=q^d+1, it is <=4*sqrt(2)*d^(10-12*d). Analytic log10 upper
references at d=64,256,1024 are -1368.33184529063, -7373.27819879572,
-36959.7102926345. Polynomial lists or attempts cannot remove this stage's
exponential penalty. These are NOT general EDCP bounds. A non-affine
noise-tolerant decoder might still exploit the broad Fourier output.

Uniform g_i give C_i=1 and B=1, recovering the published amplitude behavior.
At delta=0, B=1 even for narrow Gaussians, showing why (6)'s premise matters.

## 5. A Coherence Signal With No Secret Information

Use controlled +F(x), the known program gate exp(2*pi*i*b*z^2/Q), then
controlled -F(x), with fresh workspace h. The final joint amplitude is

    h(x)*g(z)*exp(2*pi*i*k*z/Q)*exp(2*pi*i*b*(z+F(x))^2/Q).

The program gate mixes Fourier labels, escaping (1). Dephasing the program
first can change the workspace substantially. Yet discarding it leaves

    rho_S(x,x')=h(x)*conj(h(x'))*sum_z g(z)^2
       *exp(2*pi*i*b*((z+F(x))^2-(z+F(x'))^2)/Q),                         (8)

EXACTLY INDEPENDENT OF k. This detects a known envelope's coherence, not
hidden-phase information. Its conditional phases can be generated from
classical z~g^2, although arbitrary workspace quantum processing is not
thereby classical. The zero-information claim requires this closed loop,
secret-independent workspace and discarded program. Open loops, retaining
the program, or extra secret-bearing inputs are outside scope. A proposal
needs secret sensitivity as well as failure of a classical comparator.

### Open Loop: A Genuine Boundary To The Readout Comparison

Replace the final -F(x) translation by G(x), and put H(x)=F(x)+G(x).
For program phase coefficient b, the exact final amplitude is

    h(x)*g(z-H(x))*exp(2*pi*i*k*(z-H(x))/Q)
                    *exp(2*pi*i*b*(z-G(x))^2/Q).

After discarding the program, rho_k=V_k*rho_0*V_k^dagger with
V_k(x,x)=exp(-2*pi*i*k*H(x)/Q). This generally retains secret dependence.
It need not admit a classical-to-quantum preparation from one local Fourier
sample. The following exact test establishes that boundary, not a speedup.

Let Y=k+N mod Q be ONE original Fourier sample, nu(n)=|hat_g(n)|^2.
Put C_g(r)=sum_z g(z)*g(z-r) and assume its relevant values are positive,
as for our strictly positive periodized envelope. A channel can prepare
rho_k from Y for EVERY k in Z_Q if and only if

    Gamma(x,x')=rho_0(x,x')/C_g(H(x)-H(x'))                              (9)

is positive semidefinite; its trace is already 1. Covariantly averaging any
putative channel makes its output for y equal to V_y*Gamma*V_y^dagger.
Averaging over nu multiplies each entry by the characteristic function
C_g(H(x)-H(x')), proving necessity. Positive Gamma gives the channel,
proving sufficiency. Reproduction for all k is essential to this twirl;
a restricted prior is a different comparison.

A finite countercontrol has Q=26, sigma=4, b=1, three equal-amplitude
workspace states, and F=(0,1,4), G=(0,1,2), H=(0,2,6). The determinant
of Gamma has the outward-widened interval enclosure

    [-0.002377200934697911894, -0.002377200934697911893].

This contains the 65-digit mpmath interval result. The periodized envelope
was summed for image indices -4,...,4, adding the omitted-tail enclosure
[0,1e-900] to EACH amplitude before normalization. A Gaussian tail integral
from 104 bounds the omitted mass. Normalization, overlaps and the Hermitian
three-by-three determinant all used interval arithmetic. This is a scoped
computational sign certificate, not independent verification of the theorem.

Numerical references give minimum eigenvalue -0.01579383 and
D_trace(rho_0,rho_1)=0.1098247357. The loop therefore retains secret
dependence and escapes the one-Fourier-sample preparation class. This
refutes an OVERBROAD negative claim. It does not establish hard sampling,
a multi-sample lower bound, or an advantage over access to the full original
retained classical input.

### Still No Single-Program Recovery Improvement

For uniform k over ALL Q scalar phases, local Fourier measurement is
already optimal for the original positive-envelope pure states. Covariantly
average a recovery POVM to seed M_0. Completeness gives M_0(z,z)=1/Q;
positivity gives |M_0(z,z')|<=1/Q. Consequently success is at most
(sum_z g(z))^2/Q, attained by the Fourier POVM. Processing the source
cannot improve that optimum, which is 0.2175713173 in this countercontrol.
Failure of the stronger state-preparation comparison does not imply a gain
in this particular decision task.

The native multi-block problem has k_l=s*v_l, not independent uniform
scalar secrets. Single-program optimality does NOT settle its collective
decoding. A useful next construction must exploit the shared secret and
degenerate frequency fibers with an efficient final measurement and natural
labels. Equation (9) is a boundary test, not candidate acceptance evidence.

## 6. Targeted Checks

These finite arrays verify algebra, not new oracle problems or speedups.

- Sixteen reused-program controls at Q=5,6,7,11 with quadratic, cubic and
  arbitrary translations and Fourier/nonlinear workspace gates. Maximum
  trace-distance residual against (1): 4.40e-16. Independent Y resampling
  changes a cancelling two-call control by 0.765698900757.
- Twelve kickback controls at (Q,sigma,tau)=(17,4,1.2),(31,7,2),(101,12,2),
  (257,40,2), three frequencies each. Overlap residual <=1.12e-15. The final
  joint distance is 0.0256295198679 against bound 0.0256435501752.
- Twelve negacyclic moment controls at d=2,4,8 for four symmetric integer
  laws, residual <=5.69e-14. Finite Gaussian moments are not assumed normal.
- Twenty-seven cancellation controls at Q=11,17,31, tau=1.25,2,4 and
  delta=(1,1),(1,2),(2,3), each also checking arbitrary phases/targets.
  Equality (5) residual <=5.28e-16. At tau=2,delta=(1,1), success is
  0.1805878980,0.1168509928,0.0640795767, below unit bounds
  0.2561765354,0.1657612876,0.0909013513. Three uniform controls give 1.
- Zero direction gives 1 while wrongly applying (6) gives 0.1657612876.
  At Q=11 the mixed-basis loop changes the dephased-program comparison by
  0.625924746914, yet all eleven secret-conditioned workspace states agree
  within 5.56e-17.
- Three 80-digit growing references evaluate the bound after (7).
  Numerical residuals are controls, not interval-certified proofs.
- Six open-loop seed/secret-sensitivity controls, including even Q=26,82.
  The Q=26 determinant additionally has the interval sign certificate above;
  other numerical eigenvalues are not certificates. These deliberately test
  OUTSIDE the read-only result instead of extending its scope silently.

## 7. Decision And Gemini Contract

Do not create an alleged polynomial oracle by reusing a Gaussian phase
state, or import uniform linearization without its amplitude contract.
Retain (2)-(4) as a legitimate scoped state-construction primitive.
Extend existing source/decoder checks with:

1. Stable program identities and one latent Fourier label per reused
   program, joint laws and branch/acceptance records where needed.
2. Exact catalytic overlaps and translation-step moment budgets, keeping
   correlations rather than fabricating independent phase copies.
3. Actual diagonal envelopes, chosen directions, unit/gcd premises, list
   sizes and UNCONDITIONAL success bounds (5)-(7).
4. Uniform, zero-direction, fresh-label-resampling and mixed-basis-loop
   countercontrols. Comparator failure and secret sensitivity are separate;
   neither alone establishes an efficient algorithm.
5. Preserve the open-loop countercontrol and PSD preparation test (9).
   Do not infer a universal simulator from (1), or a speedup from a negative
   seed eigenvalue. Separate single-program uniform-secret optimality from
   the native shared-secret multi-block problem.

Next: a joint operation that uses program Fourier coherence to improve
SECRET decoding, or a concrete quantum solver on matched classical noisy
arithmetic data. Finding isotropic vectors or generating nonlinear phases
is not that solver. Source errors, composite-modulus algebra and independent
review remain mandatory. No wiring, full suite, commit, or proof promotion.
