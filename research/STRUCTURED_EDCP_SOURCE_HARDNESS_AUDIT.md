# Structured EDCP: Connecting The Source To Ring-LWE Hardness

Date: 2026-09-27. LOCAL DERIVATION / REVIEW PENDING.

This audits a missing implication, not an algorithm or a security estimate.
No novelty, independent proof verification, efficient decoder, or quantum
speedup is claimed. Production integration is assigned to Gemini.

## 1. Decision

The existing coefficient-noise reference r_e=r_s=sqrt(d) is NOT justified by
the spherical Ring-LWE hardness theorem checked here. Keep its source and
information calculations as a separate reference. Do not promote them into
a worst-case lattice consequence merely because the source is called RLWE.
Failure to meet this sufficient theorem does not establish an easy problem.

Two replacement source contracts appear compatible with the existing forward
construction. The spherical one retains independent coefficient Gaussians.
The elliptical one follows the theorem's distribution over error shapes and
needs the generalized moment proof below. Both keep the actual cyclotomic
input ring, natural labels, and all source-preparation costs. Neither uses
the much larger principal-ideal order from MODULE_GLUING_AUDIT as its input
hardness assumption.

The target remains an efficient decoder. This pass makes its potential
implication precise; it does not make the decoder easier.

## 2. Literature Contract And Normalization

Primary sources checked:

- [Crockett--Peikert, Challenges for Ring-LWE, Section 2.2, pp. 9-10](https://eprint.iacr.org/2016/782.pdf):
  in degree d two-power cyclotomics, R^vee=R/d and the power-basis embedding
  is a sqrt(d)-scaled isometry. Multiplying dual-ring coordinates by d
  converts canonical error width r to primal coefficient width sqrt(d)*r.
- [Peikert--Regev--Stephens-Davidowitz, June 2020 revision, Corollary 7.3](https://eprint.iacr.org/2017/258.pdf):
  decision spherical RLWE with ell samples has a quantum worst-case ideal-DGS
  reduction when xi*q >= omega(sqrt(log d))*(d*ell/log(d*ell))^(1/4).
  Theorem 6.2 instead uses the elliptical mixture in Definition 6.1 and
  alpha*q >= 2*omega(1). Both allow any modulus; the older splitting
  restriction is not necessary here. The DGS scale and approximation losses
  in those statements must be retained, not relabeled exact SVP hardness.
- [Lyubashevsky--Peikert--Regev toolkit, Lemmas 2.23-2.24](https://sites.cc.gatech.edu/fac/cpeikert/pubs/toolkit.pdf):
  discretization must respect lattice translations; an invertible anchor
  changes a uniform secret into an error-distributed secret.

Here is the normalization in our coordinates. Set

    R=Z[X]/(X^d+1), d>=2 a power of two, V^*V=d*I,
    standard sample: b=a*s/q+e mod R^vee,
    s in R^vee/qR^vee, canonical continuous e of width xi.

Multiplying the sample by q*d gives

    b_primal=a*(d*s)+q*d*e mod qR,
    continuous coefficient width w=sqrt(d)*q*xi.              (1)

Conversely, the CURRENT discrete primal coefficient width sqrt(d), pulled
back to the dual lattice, has absolute canonical width 1. Embedding the
primal error first gives width d, but that is NOT q*xi in the dual theorem.
Neither interpretation removes the separate continuous/discrete bridge.

For ell=ceil(log d)+2 the sufficient spherical threshold grows roughly as
d^(1/4)*omega(sqrt(log d)). Width 1 does not meet it. This is a checked
theorem mismatch, not a claim that every possible reduction is ruled out.

## 3. A Translation-Equivariant Discretization

Ordinary nearest-integer rounding of a continuous Gaussian is not an exact
discrete Gaussian. We use a randomized rounding kernel instead. For observed
x in R and public t>0, output k in Z with conditional probability

    K_t(k|x)=exp(-pi*(k-x)^2/t^2)/Theta_t(x),
    Theta_t(x)=sum_(j in Z) exp(-pi*(j-x)^2/t^2).

It satisfies K_t(k+z|x+z)=K_t(k|x) for integer z. It can therefore be applied
to the OBSERVED b_primal, without knowing its integer signal or its noise.
Choice of representative modulo q only translates the integer output by q.
Uniform continuous b modulo q becomes exactly uniform integer b modulo q
by translation symmetry, when this kernel is sampled exactly.

Put

    epsilon_t=2*exp(-pi*t^2)/(1-exp(-3*pi*t^2)) < 1.

Poisson summation bounds Theta_t(x)/t between 1-epsilon_t and 1+epsilon_t,
uniformly in x. For X with continuous probability density
exp(-pi*x^2/w^2)/w, removing that denominator's fluctuation gives exactly

    integral density_X(x)*exp(-pi*(k-x)^2/t^2)/t dx
      = exp(-pi*k^2/(w^2+t^2))/sqrt(w^2+t^2).

Its discrete normalizer is between 1 and 1+epsilon_t. Comparing the two
normalized laws consequently gives the conservative bound

    TV(round_t(X), D_(Z,rho)) <= min(1,2*epsilon_t/(1-epsilon_t)),
    rho^2=w^2+t^2.                                           (2)

For d*ell independent scalar noises, sum their bounds. Add finite-precision
input and sampler errors separately. Do not infer second moments of an
approximate implementation from TV closeness; first couple to the exact
reference law, then apply the moment proof there.

This is an explicitly charged approximation, not an exact rounding identity.
A numerical countercontrol at w=1 gives nearest-rounded zero mass
0.789908594556, versus 0.920441787836 for D_(Z,1).

### Multivariate Extension

Let the continuous coefficient density be proportional to
exp(-pi*x^T*C^(-1)*x), with C positive definite. Apply K_t independently
given its coordinates. Completing the multivariate Gaussian square gives
the unnormalized discrete law with width matrix H=C+t^2*I. Its Poisson
normalizer is between 1 and (1+epsilon_t)^d, since H>=t^2*I. Hence

    TV(round_t(X), D_(Z^d,H))
      <= min(1,exp(d*(log(1+epsilon_t)-log(1-epsilon_t)))-1).   (3)

The bound is UNIFORM in C. It therefore also applies conditionally on an
unknown shared error shape, and sums over ell samples after averaging over
that shape. Compute it with log1p/expm1, not cancellation at 1.

For this exact centered discrete law, completing the square and using that
a shifted lattice Gaussian sum is at most its centered sum gives

    E exp(v^T Z) <= exp(v^T*H*v/(4*pi)),
    E Z=0, Cov(Z)<=H/(2*pi), E||Z||^2<=Tr(H)/(2*pi).           (4)

Coefficient independence is not asserted when H is not scalar.

## 4. Normal Form And A Decision Reduction

Use rank n=1. Take ell=m+2 original samples: an anchor, m training samples,
and an independent held-out verification sample. After discretization, on
the exact discrete reference law write

    b_i=a_i*s+e_i mod qR.

If a_0 is a unit, compute

    a'_i=-a_i*a_0^(-1),
    b'_i=b_i-a_i*a_0^(-1)*b_0=a'_i*e_0+e_i.                 (5)

The new secret is e_0, and training labels are independent uniform elements.
For a shared latent error shape, the secret and errors are independent
CONDITIONALLY on that shape, not necessarily after it is averaged out.
The original uniform secret also makes b_0 independent of e_0. None of
these statements allows a decoder to see the shape or the original errors.

For odd prime q, X^d+1 is square-free modulo q. Its CRT components have
sizes q^f; a union bound gives Pr[a_0 nonunit]<=d/q. Abort on a nonunit;
do not condition it away without charging it. No splitting congruence is
needed. A recovered e_0 mod q gives s=a_0^(-1)*(b_0-e_0).

A search decoder becomes a distinguisher using the held-out sample, which
must not enter preparation, decoder tuning, or candidate selection. Accept
when all centered coefficients of b_*-a_*s_hat have absolute value <=B.
If a public bound E||e_*||^2<=E2 is available, choose an integer
B>=sqrt(E2/delta_ver). Markov bounds honest verification failure by delta_ver.
For a uniform input, conditional on every training computation and s_hat,
the held-out residual is uniform; when 2B+1<=q its acceptance probability is

    rho_false=((2B+1)/q)^d.                                 (6)

For an ideal decoder with source-averaged success p and a complete forward
source/measurement error bound delta_src, the distinguishing advantage is
at least

    (1-d/q)*(p-delta_src)-delta_round-delta_ver-rho_false.     (7)

Include implementation errors in the appropriate delta. A nonpositive lower
bound proves nothing. Constant source error does not preserve an arbitrarily
small inverse-polynomial decoder advantage: shrink the budgets when needed.
No per-fixed-input success amplification is inferred from average success.

Evaluation E_q of a centered q-ary polynomial is injective into Z_(q^d+1).
Reject a decoder output outside that image; otherwise balanced-base-q
decoding recovers e_0 mod q. Thus a hypothetical adequate phase decoder would
give the required RLWE distinguisher, without the unaudited reverse EDCP
reduction. It would NOT establish hardness of every EDCP instance, ordinary
unstructured LWE, or a proven classical-versus-quantum separation.

## 5. Spherical Source Lane

For growing d, take the existing q=nextprime(d^12), m=ceil(log d), ell=m+2,
M=ceil(d*log q), and the unchanged upstream mixing width. Choose

    t=log d,
    q*xi=d^(1/4)*log d,
    w=d^(3/4)*log d,
    r_e=r_s=rho=sqrt(w^2+t^2).                               (8)

Then (q*xi)/[(d*ell/log(d*ell))^(1/4)*sqrt(log d)] tends to infinity.
This is an ASYMPTOTIC match to the spherical theorem, not a numerical
security certificate at any particular d. The rounding bound is negligible.
After (2) and (5), the exact independent-coefficient prior in
`STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS.md` applies with the new rho.

For fixed selector K and block count L, the earlier moment proof now gives

    C_mom=Theta(d^(9/4)*(log d)^(3/2)),
    sigma=Theta(epsilon*d^(37/4)/(log d)^2).                  (9)

The ideal-collision criterion is L*(b-1/2)>12 for sigma=d^(b+o(1)).
Two blocks still suffice asymptotically for constant epsilon, and for
epsilon=d^(-c) with 0<c<11/4. This is information sufficiency, not efficient
decoding. One block remains information-insufficient for a uniform secret.

Using K=4, phase budget 0.001, s_G=sigma/sqrt(2), and R=ceil(sigma*sqrt(d)):

| d | rho | sufficient L | sigma reference | delta_info reference |
|---:|---:|---:|---:|---:|
| 64 | 94.1966361450 | 4 | 18981263.9451211 | 1.52587945e-6 |
| 256 | 354.934675502 | 3 | 1.99288145195e12 | 1.74386826e-5 |
| 1024 | 1254.74956916 | 3 | 2.36190537670e17 | 1.08991376e-6 |

At d=64,L=3, log10(Q*beta^L)=180.005833752: that sufficient certificate is
VACUOUS. At L=4 it is -206.382136718. All three finite L=2 references are
also vacuous. Do not reuse the previous three-block d=64 claim after changing
the error law. The displayed sufficient counts are not necessary counts.

The joint rounding-TV log10 upper references for ell samples are
-20.3453363223, -38.0398088610, -60.9852706748. These are additional reduction
losses, not replacements for upstream/source/measurement errors.

## 6. Elliptical Source Lane Without Coefficient Independence

This avoids paying the spherical conversion's dimension factor, but changes
the prior. It must be a DISTINCT contract, never a silent substitution into
the iid coefficient proof. The cyclotomic field is totally complex. Set

    g=q*alpha=log d, f=log d, t=log d.

For each conjugate pair j, draw x_j,y_j independently from continuous
D_(1/sqrt(2)); give both embeddings the squared absolute dual width

    (q*r_j)^2=g^2*(x_j^2+y_j^2+f^2)/2.                      (10)

This specifies the PRS error-shape distribution for our parameter choice.
The shape is sampled ONCE for the RLWE instance, hidden from the solver.
Samples are independent conditioned on it. We do not replace it by its mean.
The choices f=log d and g=log d meet the theorem's asymptotic growth premises.

In a real orthonormal coefficient representation, the continuous width
matrix C has eigenvalues d*(q*r_j)^2, with the paired multiplicities.
After (3), the exact reference noise is D_(Z^d,H), H=C+t^2*I. Its expected
energy, and that of an independently sampled secret conditional on H, obey

    E2=S2=[d^2*g^2*(f^2+1/(2*pi))/2+d*t^2]/(2*pi).           (11)

Indeed each x_j,y_j has variance 1/(4*pi), and apply (4), then average.
There is no hidden high-probability cutoff of the shape. Coordinatewise
centering modulo q cannot increase a vector's norm and preserves its zero
mean by global sign symmetry. It need NOT preserve its covariance matrix.

For an explicit control, a symmetric signed vector +/- (1,2) has zero
variance in direction (2,-1). Centering modulo 3 gives +/- (1,-1), with
variance 9 in that direction, despite decreasing total squared norm from
5 to 2. Thus a pre-centering covariance bound cannot simply be reused.

Here is a replacement rank-one moment proof that uses only energy bounds.
W remains independent with iid coefficient variance <=r_mix^2/(2*pi*d).
Independence and zero mean of W coefficients give

    U2=m*r_mix^2*E2/(2*pi).

Every centered A' row has coefficients bounded by h=(q-1)/2. Its negacyclic
multiplication operator has norm <=sum_i |A'_i|<=d*h. The secret is
independent of A',W,e conditional on H, with conditional mean zero. Hence
the mixed term between A'*s and W*e vanishes, and

    P2=d^2*h^2*S2+U2,
    C_corr=sqrt(U2)+sqrt(P2)/q+sqrt(d)/2,
    delta_phase<=sqrt(pi)*sigma*C_corr/(q-1)*sqrt(v_K*L*M).   (12)

This intentionally uses a weaker operator bound for the secret term; no
unjustified independence of its coefficients is needed. The exact carry
identity and Minkowski argument from the moment note complete the proof.
The amplified errors are still correlated with each other and their labels.

With the existing r_mix=Theta(d), equations (11)-(12) give

    C_corr=Theta(d^2*(log d)^(5/2)),
    sigma=Theta(epsilon*d^(19/2)/(log d)^3).

The two-block sufficient asymptotic exponent is retained for epsilon=d^(-c)
with 0<c<3. The phase coefficient Gaussian is still the original product
Gaussian; only the UPSTREAM RLWE secret/error prior changed. Consequently
the ideal-collision calculation is unchanged at the revised phase width.

| d | E2 upper reference | sufficient L | sigma reference | delta_info reference |
|---:|---:|---:|---:|---:|
| 64 | 98585.1950651 | 4 | 18174024.9168294 | 1.52587945e-6 |
| 256 | 4957739.50769 | 3 | 2.02776038424e12 | 1.74386826e-5 |
| 1024 | 193261682.738 | 3 | 2.72148561475e17 | 1.08991376e-6 |

The d=64,L=3 bound is again vacuous (log10(Q*beta^3)=183.629643516).
Spherical and elliptical finite widths are comparable here; the latter's
advantage is asymptotic and does not justify ignoring the extra proof scope.
The matched classical flooding/readout argument must receive the SAME (12).

## 7. Verification, Falsifiers, And Handoff

Targeted checks performed, not a routine production test run:

- Four exact codifferent trace-pairing determinants and numerical embedding
  identities at d=2,4,8,16.
- Sixteen scalar rounded-Gaussian laws at w=0.25,0.5,1,3 and t=0.75,1,1.5,2;
  maximum observed TV 0.0333037231, below (2). Forty-five uniform-output
  residue checks for q=3,5,7. Default quadrature tolerances initially failed
  a tighter assertion; explicit absolute/relative tolerances resolved it.
- 170,368 exact normal-form identities and original-secret recoveries in
  Z_q[X]/(X^2+1), q=3,5, across every unit anchor and small signed errors.
  These verify algebra, not Gaussian hardness or growing decoder performance.
- Twenty-four correlated discrete-Gaussian width matrices checked (4), with
  72 MGF controls. Finite lattice sums are numerical checks, not proofs.
- Four genuinely correlated continuous-Gaussian rounding laws checked (3).
  Maximum observed TV was 0.007701683. Refining 64 to 96 Gauss--Hermite nodes
  per direction changed the joint law by at most 2.56e-12 in TV. The explicit
  centering countercontrol above rules out an unjustified covariance shortcut.
- 5,120 exact rank-one correlated-source cases across 80 conditional-shape
  ensembles checked the zero mixed term, U2,P2 and carry-energy inequality.
  Shared signed-vector priors are countercontrols, not the PRS distribution.
- Nine spherical and six elliptical 120-digit analytic references. Scalar
  truncation loss was bounded by 2*exp(-2*pi*d), retaining the full-vector
  exponent. Exact integer checks gave 2R<=q-1 in each case. nextprime values
  are not independently primality-certified; decimals are not interval
  enclosures. Information error is conditional on binary full rank G, whose
  probability 1-2^(-L) remains in the one-batch success ledger.

The main ways this direction can fail are still an exponentially expensive
decoder, a quantum operation that is classically reproducible, or an error
budget larger than its success advantage. A correct normalization and a
hardness-linked prior do not repair any of those. A polynomial ideal-lattice
approximation result would require reporting its actual factor and input
class; do not describe it automatically as solving general lattices or
achieving Shor-level significance.

Gemini integration contract:

1. Preserve the old source as `coefficient_gaussian_reference`, explicitly
   without a checked worst-case-hardness implication. Add separate
   `prs_spherical_rounded` and `prs_elliptical_rounded` contracts.
2. Record dual/primal normalization, original ell=m+2 versus amplified M,
   hidden shape semantics, width/moment bounds, rounding error, anchor loss,
   verification threshold and false-acceptance bound. Never expose the
   sampled shape, secret, noise, or held-out sample to the research decoder.
3. Use the iid moment proof only for the spherical lane; use (11)-(12) for
   the elliptical lane. Recompute information and matched classical bounds.
4. Reject: width-1 certification by Corollary 7.3; uncharged deterministic
   rounding; per-sample resampling of the shared shape; independent-secret
   assumptions after marginalizing H; held-out leakage; old d=64,L=3
   certification; zeroing tiny positive error terms; finite security claims
   inferred from asymptotic omega conditions.
5. Implement reproducible independent checks before changing registry proof
   status. Keep LOCAL DERIVATION / REVIEW PENDING. The upstream production
   numerical repair in `STRUCTURED_EDCP_UPSTREAM_NUMERICAL_REVIEW.md` remains
   required. No candidate is promoted by this note.

Next main-model work should return to an explicit genuinely quantum
cross-block decoder or basis operation under one of these source contracts,
not further source-only optimization. Independent review of the bridge,
especially shared-shape conditioning and reduction advantage, is valuable.
