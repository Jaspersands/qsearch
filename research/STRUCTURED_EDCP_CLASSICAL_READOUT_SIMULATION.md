# Structured EDCP: Classical Simulation Of Local Fourier Readout

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

FOLLOW-UP (2026-09-26): `STRUCTURED_EDCP_DIRECT_PHASE_SOURCE.md` uses the same
classical tags in a QUANTUM phase-state preparation, not a classical simulator
of arbitrary measurements. `STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS.md` improves
the flooding energy bound for the precise upstream Gaussian prior. Its wider
quantum states and the classical comparator must use the same revised budget.

## 1. Research Decision

For the retained classical integer source (A,b), the clean structured-EDCP
LOCAL FOURIER READOUT can be approximated by a polynomial-time classical
sampler. The sampler does not know the secret or the error lifts. It uses
small random linear combinations of the public equations and independent
Gaussian flooding. Composite-modulus label hashing and the complete error
budget are derived below.

This strengthens the earlier POST-READOUT classical comparisons. A proposal
whose only quantum step is producing this readout, followed by an efficient
classical decoder, must now compete against a fully classical algorithm on
the SAME retained input. The simulation loss must be smaller than the claimed
success probability. It is not automatically negligible at every allowed
width, and it is not automatically a simulation of the contaminated source.

This does NOT simulate the phase states, coherent joint measurements, an
arbitrary quantum postprocessor, or a standalone EDCP oracle without (A,b).
It does not find a good lattice basis or solve the resulting decoding problem.
No unconditional lattice attack, independent proof review or novelty claim
is supplied. Small linear combinations and leftover hashing are established
LWE tools; see the primary-source attribution at the end.

## 2. Source And Access Contract

Let d>=2 be a power of two, q>=2 an integer, Q=q^d+1, and

    E(v)=sum_(i=0)^(d-1) q^i*v_i mod Q,
    S_q=(q^d-1)/(q-1).

The algorithm has the classical pair

    A in Z_Q^(M x n),       b=A*s+e mod Q.

The source is fixed before the sampler's fresh coins are drawn. Assume:

- The M-by-n matrix A has marginal TV distance at most delta_A from uniform.
  This is a distributional premise, not a test for one observed matrix.
- Except with joint probability delta_lift, each e_j has an ACTUAL integer
  coefficient lift v_j with E(v_j)=e_j and ||v_j||_infinity<=B.
- s, the errors, A, and other pre-existing classical side information may
  be correlated. Independence of amplified error rows is NOT assumed.
- The source's classical input is available. Unknown-secret verification or
  access to the hidden lifts is not given to the sampler.

Use the upstream and joint-source notes for the proposed source realization.
Their derivations remain review pending. In particular, the current generated
upstream numerical artifact has errors documented separately in
`STRUCTURED_EDCP_UPSTREAM_NUMERICAL_REVIEW.md`; its certification flag must
not be used to discharge delta_A.

The ideal target has fresh independent uniform a_l in Z_Q^n and

    Y_(l,i)=q^i*<a_l,s>+Z_(l,i) mod Q,
    Z_(l,i) independently distributed as D_(Z,r),
    Pr[Z=k]=exp(-pi*k^2/r^2)/theta(r),
    theta(r)=sum_(k in Z) exp(-pi*k^2/r^2),
    r=Q/(sqrt(2)*sigma).                                    (1)

sigma is the PHASE AMPLITUDE width. It is not the probability width of the
source coefficient Gaussian. Section 6 charges the difference between (1)
and the true physical Fourier noise.

## 3. An Explicit Classical Sampler

Choose an even power of two K with 2<=K<=2d; set J=K/2. Independently for
every row and block, draw

    V uniform on {-J,...,J-1},       C uniform on {0,1},
    U=V+C.

Thus U has probability 1/(2K) at the two endpoints -J,J and probability
1/K at the interior integers. Its exact properties are

    E U=0,        Var(U)=v_K=(K^2+2)/12,
    Pr[U=U']=c_K=(2K-1)/(2K^2),
    Pr[U even]=Pr[U odd]=1/2.                               (2)

For each l=1,...,L, draw a fresh vector u_l of M such coefficients and return

    a_l=u_l^T*A mod Q,
    t_l=u_l^T*b mod Q,
    Y_(l,i)=q^i*t_l+Z_(l,i) mod Q,     i=0,...,d-1.          (3)

The intended output consists of a_l and the Y_(l,i), not the private selector
or Gaussian coins. The sampler uses O(L*M*n+L*d) modular arithmetic operations
up to ordinary bit-complexity and Gaussian-sampling costs. Neither Q-sized
tables nor secret-dependent steps occur. Generating q^i uses modular iteration.

The symmetric distribution matters. The older consecutive uniform selector
has mean -1/2, giving an additional squared bias term in the error energy.
The extra Bernoulli coin removes it without a parity defect.

## 4. Exact Hashing Over The Composite Modulus

Every odd prime p dividing Q has ord_p(q)=2d. Indeed, q^d=-1 mod p and 2d
is a power of two, so the order cannot divide d. Consequently p>=2d+1.
For odd q, Q=2 mod 8 and hence v_2(Q)=1; for even q, Q is odd.

For two selectors u,u', every coordinate of w=u-u' has magnitude <=K<=2d.
If w is nonzero, its common gcd with Q is therefore 1 or 2. For uniform A,

    Pr_A[w^T*A=0]=(gcd(Q,w_1,...,w_M)/Q)^n.

The zero difference occurs with probability c_K^M. All differences are even
with probability 2^(-M). Writing P_A for the conditional law of u^T*A,
the collision identity gives the EXACT mean chi-square divergence

    E_A chi2(P_A || uniform) = C_hash,

    C_hash=(Q^n-2^n)*c_K^M+(2^n-1)*2^(-M),   q odd;
    C_hash=(Q^n-1)*c_K^M,                    q even.        (4)

For example, use E chi2=Q^n*E collision-1, and separate zero differences,
nonzero even differences, and the remaining differences. This proof does not
factor Q. Cauchy--Schwarz and Jensen give

    delta_hash=min(1, sqrt(C_hash)/2).                       (5)

For L fresh selectors on the SAME A, the joint label error, retaining the
complete source and any pre-existing classical side information, is at most

    delta_A + L*delta_hash.                                 (6)

Proof: for each fixed source, conditional label distance is a function only
of A. A product hybrid bounds it by L*TV(P_A,uniform). Average over the
uniform A ensemble using (5). Replacing the actual marginal of A costs
delta_A ONCE, since the joint distance function is bounded by one. Arbitrary
source side information changes neither the fixed-A law nor this averaging.
Conditioning on a favorable subset of A would require a separate bound.

For n=1, M approximately ln Q, K=4 gives c_K=7/32 and ln(1/c_K)>1,
so the first term in (4) decays. K=2 gives c_K=3/8 and ln(1/c_K)<1;
it does NOT suffice with that row count. For fixed n choose a fixed K with
ln(1/c_K)>n, subject to K<=2d. Growing n requires explicit recalculation.
Insufficient rows do not become sufficient merely by declaring more samples.

Negative controls:

- Selectors in {-1,+1} fix a parity coset for even Q. At Q=10 and ten rows
  A=(1,...,10) mod 10, label TV is 1/2, despite a false prime-modulus
  universal-hash calculation suggesting a much smaller value.
- The support restriction cannot be dropped. For the older uniform
  consecutive selector with Q=10,d=2,K=8,M=2, exact mean chi-square is
  129/256, not the inapplicable formula's 3/8; differences divisible by 5
  occur. The new symmetric selector also requires its stated support bound.

## 5. Noise Flooding Without Independent Source Errors

Multiplication by q^i modulo Q acts on a coefficient lift by a signed
negacyclic rotation. Define an integer representative

    z_(i,j)=integer evaluation of X^i*v_j mod (X^d+1).

It satisfies z_(i,j)=q^i*e_j mod Q and |z_(i,j)|<=B*S_q. For fixed good
source data, (3) differs from the target signal only by integer shifts

    k_(l,i)=sum_j U_(l,j)*z_(i,j).

For an integer translate of the exact Gaussian in (1), symmetry gives

    KL(D_(Z,r)+k || D_(Z,r))=pi*k^2/r^2.                    (7)

The normalizer cancels and E Z=0. Product KL adds over coordinates.
Apply this to the augmented distribution including the selectors, and then
discard selectors and reduce modulo Q; relative entropy contracts. Although
the errors z_(i,j) can be arbitrarily correlated, they are FIXED before U.
The independent zero-mean selector entries imply

    E_U sum_(l,i) k_(l,i)^2
       =L*v_K*sum_(i,j) z_(i,j)^2
       <=L*v_K*d*M*(B*S_q)^2.

Pinsker's inequality therefore proves

    delta_flood <= min(1, (B*S_q/r)*sqrt(pi*v_K*d*L*M/2))
                = min(1, (B*S_q*sigma/Q)*sqrt(pi*v_K*d*L*M)). (8)

The sampler does not need z or v to run. They are proof witnesses, not oracle
inputs. A source adversarially chosen AFTER seeing the new selectors is
outside the theorem. Reusing selectors does not supply independent labels.

For comparison, a simpler shift-by-one/telescoping argument uses
TV(D_r,D_r+1)=1/theta(r)<=1/r, yielding the looser worst-case bound
d*L*J*M*B*S_q/r. Equation (8) avoids both the linear coordinate hybrid and
the worst-case row sum. It does not assume independent source errors.

First replace the shifted Gaussian, preserving the selector-derived labels;
then replace those labels using (6). For the ideal target (1), including the
unchanged source record, the final guarantee is

    delta_classical <= delta_A + delta_lift + L*delta_hash
                       + delta_flood + delta_sampler.        (9)

The conditional Gaussian channel after the first replacement depends on the
secret and label, but not on the discarded selectors. This order is essential:
uniform-looking labels alone would not justify independent error noise.

## 6. Physical Noise, Source Contamination And Precision

The exact periodized-source Fourier noise is proportional to

    [sum_(k in Z) exp(-pi*sigma^2*(e/Q+k)^2)]^2.

The earlier prior-aware baseline proves that its TV distance from (1) modulo
Q is at most rho/(1+rho), with

    rho=2*exp(-pi*sigma^2/2)/(1-exp(-3*pi*sigma^2/2)).

Charge d*L*rho/(1+rho). This is not zero at finite sigma. Also charge the
source coefficient truncation (sqrt(L*eta) for one-block probability tail
eta), finite periodization comparison, state preparation and QFT errors.

The actual grid source has a clean component of weight p0, not a promise of
being the ideal source on every run. Comparing its physical readout with the
classical sampler additionally costs at most 1-p0 on good source instances,
plus the source's bad-instance probability and the errors above. Use a uniform
lower bound for p0 when averaging instances. Separate ledgers can conservatively
double-charge a bad event; never silently drop it to obtain a better result.

For classical postprocessing with ideal-target success P, (9) implies success
at least P-delta_classical. For success measured on the actual quantum-source
workflow, subtract the additional physical/source discrepancies. An inverse-
polynomial success claim needs error SMALLER than that success probability;
an inverse-polynomial simulation error is not a negligible-error cryptographic
equivalence. Conditional experiments, such as a unit first label or full
parity rank, need their acceptance probability and conditioning loss charged.

Efficient Gaussian draws do not require enumerating r, which can be enormous.
Use a certified one-dimensional sampler with polynomial bit-complexity in
log Q and requested precision. One elementary wide-Gaussian option is to round
a continuous Gaussian of density exp(-pi*x^2/r^2)/r to the nearest integer.
Its TV distance from D_(Z,r) is <=1/r: the L1 error of the step approximation
to exp(-pi*x^2/r^2) is <=1, its integral is r, and theta(r)>=r; accounting
for both normalization and the step error gives the bound. Charge d*L/r.

Finite-bit generation must approximate the ROUNDED output distribution via
certified Gaussian bin probabilities or quantiles. A finite-bit real is not
TV-close to a continuous Gaussian before rounding. Tail and numerical errors
belong in delta_sampler. This note is not a production sampler implementation.

## 7. Source-Compatible Parameters

The forward source's sufficient margin condition is

    48*a*M*L*d*R*B*S_q <= Q,
    a=ceil(Q^(n/M)),        R>=sigma*sqrt(kappa).

Substitution in (8) gives

    delta_flood <= sqrt(pi*v_K)/(48*a*sqrt(kappa*d*L*M)).     (10)

This is a stronger consequence of the SAME source condition; no width or row
budget has been made free. With kappa=d, fixed K,n,L and M=Theta(d*log d),
this bound decreases polynomially. Taking smaller sigma improves flooding
but can worsen the information available for decoding.

The following analytic references reuse the upstream integer recipe:
n=1,L=288,q=nextprime(d^12),M=ceil(d*ln q),a=3,K=4,kappa=d.
B is the proven lift B_out, not an independent-error standard deviation.
The default sigma is sqrt(d), R=d. All numbers below use 110-digit arithmetic,
not interval-certified enclosures; primality was not independently certified.

| d | M | B | Default Flooding Upper Bound | log10(L*delta_hash) |
|---:|---:|---:|---:|---:|
| 64 | 3195 | 355689673 | 1.00379e-8 | -358.7015 |
| 256 | 17035 | 13854652906 | 2.15250e-13 | -1920.7774 |
| 1024 | 85174 | 480919424497 | 3.98330e-18 | -9612.1906 |

These are NOT total errors. delta_A, delta_lift, physical noise, source clean
weight, finite sampling and preparation must still be added. For example,
the source clean weight is only about 0.9797681 at d=64. The true physical
noise approximation contributes log10 bounds approximately -39.0934,
-169.4715 and -692.7900 at these default widths.

Let R_max=floor(Q/(48*a*M*L*d*B*S_q)) and sigma_max=R_max/sqrt(d).
These are maxima for this sufficient certificate, not necessary width limits.

| d | R_max | Flooding Bound At sigma_max | log10 Native H Lower Bound |
|---:|---:|---:|---:|
| 64 | 1565 | 2.45459e-7 | 1249.9278 |
| 256 | 31618906 | 2.65859e-8 | 5824.9133 |
| 1024 | 764126358828 | 2.97241e-9 | 26517.6057 |

The last column uses H>=Q/theta(s_G)^d>=Q/(1+s_G)^d, s_G=sigma/sqrt(2),
for the NATIVE basis. Thus merely widening the source up to the certified
limit still leaves that universal-envelope method exponentially expensive.
This is not a lower bound on every lattice sampler or quantum measurement.

## 8. Consequences For The Profile Decoder

`STRUCTURED_EDCP_PROFILE_LIST_DECODER.md` gives a classical list decoder for
the same public, noise-independent kernel basis. Its profile obeys

    J_profile=H*theta(1/s_G)^D <= e*H
    when s_G^2>=ln(4D)/pi,       D=d*L.

If the required basis is CLASSICALLY obtainable in polynomial time, the
profile and list parameters are polynomial, the input has the source contract
above, and total simulation loss is small relative to success, the complete
comparison is now classical: (3), classical list decoding, and public residual
verification against (A,b). Charge the basis construction, finite sampler,
list generation, any label conditioning, and verification.

Previously the comparison stopped after a quantum readout. That qualification
is superseded for this specified source and measurement. It remains correct
for standalone phase-state access. A polynomial universal-envelope quantum
method justified ONLY by such a classically available polynomial profile
does not demonstrate a superpolynomial separation on this source.

No efficient good-basis algorithm is supplied. A basis found by an essential
quantum computation is not classically available for free. Nor does this
argument simulate a quantum decoder merely because its input is classical.
Basis dependence on the fresh readout noise is outside the existing profile
theorem unless separately analyzed.

## 9. Checks And Attempts To Break The Claim

Bounded mathematical interpreter checks, seed 20260925; no production wiring
or full-suite run. Exact finite controls are not growing-size evidence.

1. Exhausted six symmetric-selector hashing cases (Q,n,M,K) equal to
   (10,1,2,4), (10,1,3,4), (10,2,2,4), (26,1,2,4), (65,1,2,4),
   (82,1,2,8). Across 22,725 matrix seeds and 1,044,669 weighted selector
   images, mean chi-square agreed EXACTLY with (4), using rational arithmetic.
   The respective values were 81/128,855/4096,171/32,179/128,49/16,1381/1024.
   The n=2 small example's TV bound is vacuous and was retained as such.
2. Sixty exact selector-energy identities checked (8) for d in {2,4,8},
   M in {1,2,3,4}, five arbitrary integer shift arrays each. No error-row
   independence was used. Twenty-five finite Gaussian references checked (7)
   at r in {0.5,1,2,5,20} and shifts in {0,1,2,5,9}; infinite tails in those
   floating-point references were truncated, not claimed algebraically zero.
3. Forty-eight complete output-law comparisons enumerated (a,Y_0,Y_1),
   covering q in {3,5}, M=4, eight source instances, sigma in {0.5,1,2}.
   Some errors explicitly depended on A; others used arbitrary bounded lifts
   in every row. All 445,824 compared output entries respected fixed-seed
   label TV plus the source-specific KL flooding bound. These compare with
   the WRAPPED-GAUSSIAN target only, not the uncharged physical noise.
   At q=3,sigma=1 the first case had TV 0.15351349, label TV 0.05126953,
   and flooding bound 0.68646842. Some bounds are deliberately vacuous.
4. Three growing analytic reports rechecked the exact integer root, Gaussian
   tail budget, carry budget and maximum margin radius before evaluating
   (4), (8) and the native H lower bound. These are formula evaluations, not
   executed high-dimensional decoders or evidence of classical security.

The claim can fail through missing source access, insufficient label entropy,
a selector parity obstruction, invalid lift bounds, adaptive source errors,
unaccounted contamination, a wrong physical-noise convention, a noise-dependent
basis, or a claimed success smaller than the simulation loss. Each is an
explicit premise or charged error above. None is dismissed by a green test.

## 10. Gemini Contract And Next Theory

FOLLOW-UP: `STRUCTURED_EDCP_CONDITIONAL_CORE_BARRIERS.md` quantifies two
remaining representation pitfalls and a constructive conditional-core
extension. It does not provide the missing core algorithm.

Gemini should implement the sampler and checker after reviewing this note:

- Keep source M,n,d and requested readout L distinct; record the classical
  input access requirement and the excluded coherent measurement access.
- Implement exact selector probabilities and both branches of (4), with
  log-domain bounds; reject unsupported K,d rather than silently applying
  a prime-modulus hash formula. Keep vacuous bounds visible.
- Preserve source-data-only sampling: the callable sampler takes A,b and
  public parameters, NEVER s or the error lifts. Reference evaluators may
  use secret data in clearly separated test-only code.
- Record delta_A, delta_lift, hashing, flooding, physical-noise approximation,
  clean-component contamination, conditioning and numerical sampling losses
  separately. A small flooding term is not the full certificate.
- Reproduce the exact controls, plus signed-selector parity failure,
  insufficient rows, unsupported K, dependent errors and missing-source cases.
- Compare classical synthetic readout and actual local-readout references with
  identical downstream decoders and basis costs. Do not compare one side's
  exact ML with the other side's heuristic and call it a quantum separation.
- Repair the upstream numerical certificate FIRST; the separate review lists
  exact discrepancies and safe required semantics. No candidate promotion.

Main-model effort should now target a genuine coherent conditional-fiber
operation or a quantum-specific basis construction. Before pursuing one,
identify precisely which operation is not replaced by (3). A new wrapper
around local readout is not enough. Independent proof review and the original
source's reverse/hardness implications remain outstanding.

## Sources

- Regev, *The Learning with Errors Problem*, CCC 2010 invited survey,
  [author-hosted PDF](https://cims.nyu.edu/~regev/papers/lwesurvey.pdf), section 4.
  Linear combinations and leftover-hash reasoning are established machinery.
  Equations (2)-(10) above are a local derivation for the specified composite
  modulus, correlated source and structured readout, not an attributed theorem
  from that survey or a claim of mathematical novelty.
- `STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md`: reviewed source premises,
  exact carry lifts and finite parameter recipe.
- `STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md`: unheralded clean component,
  source errors and public residual verifier.
- `STRUCTURED_EDCP_PRIOR_CVP_BASELINE.md`: physical Fourier-noise correction.
- `STRUCTURED_EDCP_PROFILE_LIST_DECODER.md`: matched classical decoder and
  fixed-basis limitations.
