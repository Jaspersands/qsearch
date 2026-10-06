# Native Ring-LWE: Chosen Short Preimages Suffice

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

This relaxes the operation target in NATIVE_RLWE_COVARIANT_DECODER_TARGET.
No polynomial-time finder, novelty, independent verification, quantum
speedup or security estimate is claimed. Small enumerations are identity
controls, not scalable solvers. Gemini owns routine implementation.

FOLLOW-UP: NATIVE_RLWE_HOMOGENEOUS_DGS_REDUCTION gives a still weaker
alternative on existing d^4 rows: centered coordinate-neutral Gaussian
sampling, with no chosen cosets or pair queries. Its entropy/moment
certificate is essential; poorly spread small controls genuinely fail.

## 1. Decision And Access Contract

A clean phase-aligned Gaussian-fiber inverse is sufficient for the older
decoder, but is NOT necessary for a different decoder. A chosen-syndrome
interface returning MEASURED short preimages can suffice. Garbage, output
phases and lack of a coherent inverse are irrelevant to that interface.
An exact Gaussian law is unnecessary if a moment or radius certificate
is available. If the primitive is classical, the decoder is classical too.
Classical postprocessing does not simulate an unavailable quantum primitive.

Let F:Z_q^n -> Z_q^k be public and surjective. For native L2 use

    n=2*d, k=d, F=[C_(a_1)^T C_(a_2)^T], b=F^T*s+e mod q.

b contains TWO independent ORIGINAL training records. Integer error lifts
e appear only in the proof; neither e nor an ideal phase is supplied.
For classically chosen u, a fresh invocation outputs c from nu_u with
F*c=u mod q, or ABORT. Invalid outputs count as aborts. Calls have fresh
independent randomness/reset workspaces, including two calls at the same u.
Hidden coins/garbage are not read. All preprocessing, failures and retries
are charged. Runtime must hold on the queried syndrome law.

Define, with abort contributing zero,

    h_b(u)=E_[c from nu_u,success] omega^(b dot c), |h_b(u)|<=1,
    omega=exp(2*pi*i/q),
    f=Pr_[uniform u,sampler][ABORT],
    M=E_[uniform u,sampler][1_success*c*c^T].                (1)

Every individual query below has a UNIFORM marginal. Average-uniform
accuracy is sufficient; pair outputs nevertheless need independence.
Drawing an ambient Gaussian c and returning u=F*c gives RANDOM syndrome
access, not chosen access, even when u is nearly uniform. Filtering for
a chosen u costs about q^k. Subtracting an arbitrary representative to
force u can destroy shortness. The interface is UNSOLVED, not a free oracle.

## 2. Heavy Character From Moments

Let h_hat(r)=E_u h_b(u)*omega^(-r dot u). Syndrome validity gives exactly

    h_hat(s)=E_[uniform u,c,success] omega^(e dot c),
    Re h_hat(s)>=1-f-gamma_M,
    gamma_M=(2*pi^2/q^2)*e^T*M*e.                           (2)

The bound uses 1-cos(t)<=t^2/2. Set a=max(0,1-f-gamma_M). Parseval gives

    |h_hat(s)|^2>=a^2, sum_r |h_hat(r)|^2<=1.              (3)

No Gaussianity, flatness, prior or clean workspace is required here.
If M<=v*I then gamma_M<=2*pi^2*v*||e||^2/q^2. Successful norm <=R implies
the weaker M<=R^2*I. Uniform-average norm control also gives that weaker
operator bound. Small total norm does NOT imply a sharp isotropic moment
bound. Certificates must not be inferred from a few observed points.
Original uncentered error lifts avoid the invalid modular-centering
covariance shortcut. Hidden elliptical shape is not given to the solver.

## 3. Explicit Classical Correlation Decoder

For coordinate j choose uniform u in Z_q^k and uniform t in Z_q.
Independently query c at u and c' at u+t*e_j. Set Z=omega^(b dot (c'-c))
when both succeed, and Z=0 otherwise. For a proposed coordinate r,

    S_j(r)=E Re[Z*omega^(-r*t)]
          =sum_[w:w_j=r] |h_hat(w)|^2.                    (4)

Proof: E[Z|u,t]=h_b(u+t*e_j)*conj(h_b(u)). Expand both functions in
characters; averaging u cancels unequal full frequencies, and t selects
w_j=r. The scores are real nonnegative Fourier-POWER marginals.

    S_j(s_j)>=a^2, S_j(r)<=1-a^2 for r!=s_j,
    score_gap>=G=2*a^2-1.                                 (5)

If a>1/sqrt(2), each coordinate has the unique true winner. This prevents
assembling coordinates from unrelated frequencies. Below that threshold
there is no unique-decoding certificate; apparent peaks are not proof.

Collect m independent pairs per coordinate. Reuse their t,Z to test ALL
K coordinate hypotheses, rather than requesting K separate sample sets.
Hoeffding and a union bound on summands in [-1,1] give

    m>=ceil[(2/tau^2)*log(2*k*K/delta_est)],
    Pr[max_(j,r)|S_empirical-S_j|>tau]<=delta_est.          (6)

With score bias beta from implementation/arithmetic, require

    2*(tau+beta)<G.                                       (7)

There are 2*k*m primitive invocations. Full q scoring can use an FFT of
the sparse t histogram, O(k*q*log q) arithmetic with charged precision
and storage. This is polynomial in q, not necessarily in log q; q=poly(d)
suffices for asymptotic rank-polynomial cost.

For the ACTUAL small secret, score only centered integers [-R_s,R_s] mod q,
with a proved prior-tail loss delta_s and 2*R_s<q. Then K=2*R_s+1 and
direct scoring is O(k*K*m) phase operations, polynomial in d and log q
for the existing polynomial R_s. Uniform t still spans the full modulus.
Charge delta_s once. Previous spherical/hidden-shape prior bounds apply.

Keep ORIGINAL output coordinates: normalizing a_1 to one pushes the secret
prior forward and invalidates the old box. An internal solver for
F'=C_(a_1)^(-T)*F can translate requested u to C_(a_1)^(-T)*u, return the
same c, and use ORIGINAL b in (4). Verify the final full guess against an
independent original held-out record. Existing source/anchor/rounding and
verification losses remain due; verification does not provide the primitive.

For an approximate reference oracle with average-uniform TV error epsilon
per fresh call, pair-score bias is <=4*epsilon. Charge arithmetic separately.
Correlated hidden coins invalidate the marginal-TV argument. Alternatively
certify the implemented oracle's own f,M and use (2)-(7) directly; do not
double-charge these two routes. All queries use the same actual b/function
h_b: no many-copy comparison to independent ideal phase states is asserted.
The repeated-copy barrier in NATIVE_RLWE_SAMPLE_ACCESS_AUDIT is not evaded
by free copies; the new power is the UNSOLVED chosen-syndrome interface.

## 4. Conditional Gaussian Sampling Is Sufficient, Not Necessary

Use the UNWRAPPED product probability law

    mu_sigma(c) proportional to exp(-2*pi*||c||^2/sigma^2),
    r_sigma(u)=Pr_[mu_sigma][F*c=u].

If |q^k*r_sigma(u)-1|<=eta<1 for all u, a conditional probability sampler
has uniform-syndrome coefficient law mu_sigma(c)/(q^k*r_sigma(Fc)). The
ordinary integer Gaussian has per-coordinate second moment <=sigma^2/(4*pi)
(by Poisson summation). A PSD comparison therefore gives

    M<=sigma^2/[4*pi*(1-eta)]*I,
    gamma_M<=pi*sigma^2*||e||^2/[2*q^2*(1-eta)].            (8)

No square-root state, coherent coins or consistent phases are required.
Alternatively Re h_hat(s)>=1-gamma_0-eta, with
gamma_0=pi*sigma^2*||e||^2/(2*q^2): compare to the ordinary mu_sigma
characteristic function. Use the stronger bound, not their sum.

At existing L2 rows E gamma_0=delta_phase^2/2, so

    Pr[gamma_M>.2]<=E gamma_0/[.2*(1-eta)].                (9)

This is a weaker operation target on the EXISTING d^4 family, not an
implemented sampler. Finite cutoffs need no uncontrolled rare-fiber
division: if T is omitted ambient probability, AVERAGE-uniform conditional
omitted mass is <=T/(1-eta). Empty truncated fibers contribute full failure.
Both queried syndromes have uniform marginals; this is not a per-u bound.

## 5. Distinct Norm-Only References Near q=d^6

Larger modulus can remove the Gaussian/isotropy requirement. This is a
DISTINCT theoretical source family, not a live d^4 parameter change.
Choose the first prime q>d^6 with q=3 or 5 mod 8; sigma=2*d^3,
R=sigma*sqrt(d). These dimensions have integral R. Retain the previous
normal-form noise/prior laws: absolute widths q*xi or q*alpha and energy
bounds stay unchanged. Source-theorem applicability remains a review
obligation; this is not a new hardness or security claim.

For successful norm <=R, including shared hidden noise shape,

    E gamma_R<=(2*pi^2*R^2/q^2)*E||e||^2
              =4*pi^2*sigma^2*d*E2/q^2,                  (10)

since the TWO training errors have total expected energy <=2*E2.
No unconditional secret/error independence is used. Markov gives
Pr[gamma_R>.2]<=E gamma_R/.2.

| d | q | sigma | R | E gamma_R spherical | E gamma_R elliptical |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 64 | 68719476851 | 524288 | 4194304 | .0132920128 | .0144987832 |
| 256 | 281474976710677 | 33554432 | 536870912 | .0007371856 | .0007120387 |
| 1024 | 1152921504606847067 | 2147483648 | 68719476736 | .0000359877 | .0000271060 |

Bad-error upper fractions at threshold .2 are .0664601/.0724939,
.00368593/.00356019 and .000179939/.000135530. These are HYPOTHETICAL
decoder losses, not implemented-finder performance. On the good event,
f<=.01 gives a>=.79 and G>=.2482; tau=.04 with a small arithmetic budget
satisfies (7). Add prior, estimation and original reduction losses.
At the old d^4 finite rows this conservative norm-only certificate is
vacuous for R. The sharper Gaussian guarantee cannot be used for arbitrary
short points; the distinct modulus is what enables these finite bounds.

With R^2=O(d*q), mean norm-only loss is O(d*E2/q). For q=d^a it vanishes
when a>7/2 in the spherical lane and a>3 in the elliptical lane, with the
respective logarithmic factors. d^6 is convenient, not a necessary power.

### Existence Is Not A Finding Algorithm

At residue degree d/2, two independent labels and unit first label, the
previous CRT certificate gives E_A A_sigma(A)<=B_sigma=2*x+x^2, where
x=(q^(d/2)-1)*(10/(7*sigma))^d. Apply it ALSO at sqrt(2)*sigma to get
B_wide. If both syndrome laws are eta-relatively flat, Gaussian tilting
gives for EVERY u

    E_[mu_sigma|u] exp(pi*||c||^2/sigma^2)
      <=2^d*(1+eta)/(1-eta),
    Pr[||c||>R|u]<=2^d*(1+eta)/(1-eta)*exp(-pi*d).         (11)

The tilted law is the wider Gaussian; Poisson summation gives
Theta(sigma)/Theta(sigma/sqrt(2))<=sqrt(2) for the ambient ratio.
The bound is below one, proving a short point EXISTS in every coset on
this event, without an unjustified ambient-to-conditional error transfer.

At eta=.01, log10 B_sigma=-9.0511643,-37.1077471,-149.3340785;
log10 B_wide=-18.6841241,-75.6395866,-303.4614363. Conditional on first-
label unit probability p_U=(1-q^(-d/2))^2, the bad-label union bound is
(B_sigma+B_wide)/(.01*p_U). Charge unit rejection separately. Tiny positive
terms must not become machine-underflow zero. Log10 of (11)'s tail bound
is -68.0454807,-272.2079815,-1088.8579846.

Gaussian preimages/short bases are established concepts, not novel primitives:
[Gentry--Peikert--Vaikuntanathan](https://www.mit.edu/~vinodv/papers/trapcvp.pdf)
does not supply our random module's short basis at the requested width.
Chosen-query character learning has established precedents too; see
[Akavia's noisy-character framework](https://people.csail.mit.edu/akavia/AkaviaPhDThesis.pdf).
The equations here give an explicit elementary interface-specific argument,
not a novelty claim or an assumed general-purpose learner.

## 6. Generic Grover Search Still Fails

Uniform residue preimages are easy linear algebra, but each fiber has q^d
residues. Because R<q/2, a short integer point has a unique residue.
For ANY surjective F, the mean marked fraction over uniform u is exactly

    p_mean=|Z^(2d) intersect Ball(R)|/q^(2d)
      <=pi^d*(R+sqrt(d/2))^(2d)/(d!*q^(2d)).               (12)

Cover integer points by their unit cubes to obtain the bound. A strategy
only alternating uniform-fiber source reflections and shortness phases
has mean success <=(2*T+1)^2*p_mean after at most T amplification rotations,
including input-dependent bounded schedules. Log10 upper p_mean at the
three references is -596.7315024,-3308.0828208,-16926.8787583.
This rules out generic polynomial-cost amplification for this target,
not structured operations, nonlocal walks, better starts or all algorithms.

## 7. Attempts To Break The Reduction

- Easy affine c=(F_1^(-1)*u,0) has the correct syndrome but is long. Its
  h is a PERFECT character at WRONG secret s+F_1^(-T)*e_1. Peaks alone
  are not evidence; the moment/norm and held-out checks are indispensable.
- Random syndrome samples do not provide paired chosen queries; matching
  independent labels in the other k-1 coordinates is exponentially costly.
- Shared private samples replace the t=0 correlation |h(u)|^2 by 1.
  One-call marginals cannot certify pair independence.
- Flatness alone is insufficient: broad coefficients lose noise robustness.
- Existence, a supplied trapdoor or q^d enumeration is not a scalable finder.
- Average-error bounds do not certify every fixed input; Markov losses stay.
- Reversible classical sampling is not automatically coherent erasure,
  but this decoder does not ask for erasure in the first place.

## 8. Checks Actually Run

No production CLI, full suite, registry promotion or commit:

- Seed 290941: 72 arbitrary bounded complex functions on Z_q^k, q=3,5,7,
  k=1,2,3. All 144 coordinate identities matched, max error 5.56e-16;
  empirical scores at 3,000 pairs per coordinate recovered all true modes.
- Seed 290942: 14 COMPLETE native L2 d=2 cases at q=11,17,31, with
  14,641/83,521/923,521 coefficient residues per case. Actual noisy b,
  exhaustive conditional Gaussian reference laws. All 28 empirical
  coordinates recovered at 3,000 pairs each; identity error <=3.34e-16.
  Checked Gaussian variance, heavy-character and average cutoff bounds,
  including empty branches. Some small cases FAIL flatness; successful
  decoding must not automatically certify those cases. Enumeration is
  exponential and supplies no algorithmic primitive.
- Shared-coin control: replacing independent calls at t=0 gives score 1
  instead of .6545084972, an error of .3454915028.
- Seed 290943: 12 NON-Gaussian minimum-norm native preimage tables,
  5,484 exact syndrome witnesses and moment checks. True Fourier power
  >=.6514472764; all coordinate marginals recovered. Twelve long-affine
  controls instead had unit power at a wrong secret. Tables are controls,
  not scalable finders.
- Seed 290944: 20 complete small uniform-fiber counts verified (12),
  its volume bound and independence of the count identity from labels.
- Checked three new primes with SymPy isprime, residue-degree classes,
  integer radii and 2*R<q; recomputed CRT bounds, noise losses, all-coset
  tails and unstructured-search masses.

Independent proof review, source applicability and the efficient primitive
remain open. These checks support algebra and scope, not a breakthrough.

## 9. Gemini Contract And Next Theory Target

Implement the interface and correlation decoder as a CONDITIONAL reduction
test, with no default efficient-preimage certificate. Reference enumeration
must be marked EXPONENTIAL. Record original F,b/source IDs, chosen access,
independent resets, preprocessing/query costs, abort/syndrome validity,
norm/moment certificates, score gap, prior, numerical/error terms and held-
out residuals. Unknown moments remain UNKNOWN, not assumed isotropic.
Keep d^4 Gaussian and d^6 norm-only records separate. Exact modular integers
are essential: d^6 labels exceed exact float precision and matrix products
overflow int64 even where q fits int64.

Regression controls: aborts/average failures, truncation, wrong long affine
representatives, invalid syndromes, shared coins, normalized-prior errors,
small-prior scoring and generic-Grover cost. Full suite/live integration
belongs to Gemini. Do not resolve the efficient-primitive proof obligation
from this note or its small reference backend.

Main-model target is now an EXPLICIT structured quantum chosen short-
preimage finder at O(sqrt(d*q)) radius, or a conditional distribution
sampler with the sharper moment guarantee. Clean erasure is an optional
stronger route, not an entry condition. Benchmark relation generation,
basis construction, optimization and walks against their full classical
counterparts. Native local moves and generic amplification already fail;
a new operation needs a proved useful effect and cost, not just membership
in an unexcluded circuit family.
