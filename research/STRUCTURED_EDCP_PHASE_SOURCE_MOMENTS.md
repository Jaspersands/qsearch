# Structured EDCP: Distribution-Averaged Phase Source Certificate

Date: 2026-09-26. LOCAL DERIVATION / REVIEW PENDING.

This refines `STRUCTURED_EDCP_DIRECT_PHASE_SOURCE.md` for the SPECIFIC upstream
Gaussian source. It does not replace that note's more general bounded-lift
contract. The refinement is averaged over the stipulated secret/source law,
not uniform over all fixed secrets or adversarial errors.

FOLLOW-UP: `STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md` tightens the information
certificate to three blocks at the current finite reference dimensions. The
12,9,8 table below is the earlier, looser valid certificate, not a lower bound.

HARDNESS FOLLOW-UP (2026-09-27):
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md` distinguishes this stipulated prior
from a theorem-linked RLWE source. Its spherical lane changes r_e,r_s and
recomputes the finite counts; its elliptical lane uses a DIFFERENT,
correlation-tolerant moment proof. Neither may inherit this table unchanged.

## 1. Research Decision

The direct phase-tag construction permits a second-moment proof. We can bound
the actual phase energy without replacing every error coefficient by a joint
high-probability worst-case cap. This removes the separate lift-failure charge
ON THIS DISTRIBUTIONAL ROUTE and increases the certified amplitude width.
The upstream matrix-uniformity and implementation errors remain.

Nothing here solves a lattice problem, finds a good basis or supplies an
efficient quantum decoder. The relevant constructive progress is a simpler,
wider source with a transparent joint error budget.

## 2. Rotation Energy Is Controlled By Coefficient Energy

For v in Z^d, define z_i=E_integer(X^i*v mod (X^d+1)), i=0,...,d-1, where
E_integer evaluates at q without modular reduction. Write Jv for a signed
negacyclic rotation. Since q^d+1=Q,

    q*z_i-z_(i+1)=Q*(J^i v)_(d-1),
    z_d=-z_0.

Let T be the orthogonal signed shift on the z vector. The right-hand vector
is Q times a signed permutation of v. Therefore

    (q-1)*||z||_2 <= ||(q*I-T)z||_2 = Q*||v||_2,
    ||z||_2 <= Q/(q-1)*||v||_2.                              (1)

The ordinary triangle inequality also gives the useful control
||z||_2>=Q/(q+1)*||v||_2. These are exact finite norm bounds and require
no factorization or Gaussian assumption.

The direct source proof, before substituting a lift cap, consequently gives

    delta_phase <= min(1, sqrt(pi)*sigma/(q-1)
                    *sqrt(L*v_K*sum_j E||v_j||_2^2)).        (2)

The expectation includes the source distribution, followed by fresh selectors.
Correlations between source rows do not matter: independent zero-mean selector
entries eliminate the cross terms. Equation (2) does not require selecting a
good-lift event first.

## 3. Exact Upstream Law And Carry Moments

Use `STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md` without changing conventions:

    R=Z[X]/(X^d+1), q an odd prime, h=(q-1)/2,
    A uniform in R_q^(m x n),
    s_raw: independent D_(Z,r_s) coefficients,
    e: independent D_(Z,r_e) coefficients,
    W: independent D_(Z,r_mix/sqrt(d)) coefficients,
    A'=center_q(W*A), b'=center_q(W*b).

Original A,s_raw,e,W are mutually independent; amplified A' and u=W*e are
NOT asserted independent. The actual secret s is the centered modular image
of s_raw. Its coefficients remain independent, symmetric, mean zero, and have
variance at most r_s^2/(2*pi). Centering modulo odd q cannot increase their
absolute values. The bound applies to this PRIOR, not arbitrary fixed s.

For one amplified row, negacyclic convolution and independent zero-mean input
coefficients give

    E||u_j||_2^2 <= U2,
    U2 = d*m*r_mix^2*r_e^2/(4*pi^2).                         (3)

For clarity: each output coefficient is a sum of m*d products. Distinct
W-coefficient cross terms vanish; shared original errors do not invalidate
this one-row second moment. Summing over d output coefficients gives (3).

Let p_j=sum_k A'_jk*s_k+u_j as an INTEGER negacyclic polynomial. Conditional
on A',u, the independent centered secret kills the cross term with u. Each
output coefficient of A'*s has at most n*d coefficients of A', all bounded
by h. Thus

    E||p_j||_2^2 <= P2,
    P2 = n*d^2*h^2*r_s^2/(2*pi)+U2.                          (4)

Write b'_j=p_j-q*k_j, where k_j is the coefficientwise centered quotient.
Since ||b'_j/q||_2<=sqrt(d)/2, Minkowski's inequality on random vectors gives

    sqrt(E||k_j||_2^2) <= sqrt(P2)/q+sqrt(d)/2.

The exact lift is v_j=u_j-X*k_j modulo X^d+1, as proved in the upstream note.
Multiplication by X preserves Euclidean coefficient norm, so another Minkowski
inequality yields

    sqrt(E||v_j||_2^2) <= C_mom,
    C_mom = sqrt(U2)+sqrt(P2)/q+sqrt(d)/2.                    (5)

No wrapping event, independence of k and u, or small-error conditioning was
assumed. The inequalities deliberately allow all such correlations.

Equations (2)-(5) prove

    delta_mom = min(1, sqrt(pi)*sigma*C_mom/(q-1)
                                      *sqrt(v_K*L*M)).       (6)

Combining with the SAME composite-modulus label hash gives

    D(rho_actual,rho_ideal_R)
       <= delta_amp+delta_eval+L*delta_hash+delta_mom
          +delta_implementation.                            (7)

This is averaged over the complete stipulated source, including its secret
prior, while retaining pre-existing classical records. There is NO additional
delta_err or delta_lift in (7): the tail contribution is already integrated
into the phase-energy bound. Conversely, arbitrary bounded-lift sources that
do not satisfy these Gaussian/independence premises must use the original
ledger; they do not inherit this improvement.

Approximate upstream Gaussian sampling should be compared with its exact law
in total variation BEFORE the subsequent quantum channel. Charge that joint
sampling error in delta_implementation. Small TV alone does not prove that the
approximate sampler has the same unbounded second moments.

As before, requesting the infinite coefficient target adds its explicit
truncation distance. No final grid p0 or delta_sep appears on this direct route.

## 4. Width And Finite Information Consequences

For a chosen phase budget epsilon, require

    sigma <= epsilon*(q-1) /
                   (sqrt(pi*v_K*L*M)*C_mom).                 (8)

For the fixed-rank recipe q=d^(12+o(1)), m=Theta(log d), M=Theta(d*log d),
r_e=r_s=sqrt(d), r_mix=Theta(d), one has

    C_mom=Theta(d^2*sqrt(log d)),
    sigma=Theta(epsilon*d^(19/2)/log d),      fixed L,K.

This gains a factor of order sqrt(d) over the high-probability lift-cap
certificate. It does not mean an arbitrary secret's error is that small.

Using the finite all-divisor information calculation from
`STRUCTURED_EDCP_WIDE_PHASE_INFORMATION.md`, n=1,K=4,epsilon=0.001 and
R_phase=ceil(sigma*sqrt(d)), gives the following references. Here m=ceil(log d),
M=ceil(d*log q), q=nextprime(d^12), and the exact mixing width is

    r_mix=2*d*(floor((q^(d+2))^(1/(d*m)))+1).

| d | r_mix | C_mom reference | L | sigma reference | delta_info reference |
|---:|---:|---:|---:|---:|---:|
| 64 | 3780224 | 86100005.2949 | 12 | 129035702.185 | 4.66934756e-11 |
| 256 | 36591616 | 3651887666.27 | 9 | 2.55240322e13 | 1.71733030e-5 |
| 1024 | 303337472 | 130796220001.791 | 8 | 5.67133375e18 | 5.85660663e-6 |

L is the first integer >=3 for which that sufficient information certificate
is below 0.001 at its corresponding width (8). It is not a necessary sample
count. The support radii 1032285618,408384515563435,181482679945412544673
all satisfy 2R_phase<=q-1 by integer comparison.

The direct phase error is 0.001 by design; the COMPLETE source error is (7),
not 0.001 alone. The information measurement is still not implemented. Use a
single batch with a possible binary-rank failure as described in the wide
information note, not an unproved average-to-fixed-instance retry argument.

Even here the native profile has log10 H lower bounds approximately
877.6937466,4004.465996,17940.91957. The improved width does not make the
existing native universal-envelope sampler efficient. Asymptotically this
lower bound is exp((5/2+o(1))*d*log d). It is scoped to that basis/method.
This comparison uses the native basis under the unit-first-label condition
specified in the wide-information note; that event is not free for a decoder.

The classical readout proof admits the SAME moment substitution in its KL
energy calculation. Its Gaussian flooding loss is therefore also bounded by
(6). Quantum and classical proposals must be compared at matched improved
widths, not by leaving the classical baseline at the obsolete narrow width.
This substitutes into the flooding term only; the physical-readout and
classical finite-sampling ledger must still be charged.

These are 120-digit formula evaluations, not directed-rounding enclosures or
large-dimensional experiments. Exact mixing-root inequalities and integer
support constraints were checked; primality is not independently certified.
Approximate formula outputs must not be relabeled as proof certificates.

## 5. Falsification Checks And Integration Contract

- Six hundred exact integer rotation/norm controls used d=2,4,8, q=2,3,5,17,
  50 vectors per pair, with coefficients in [-8,8]. Both sides of the norm
  sandwich and every recurrence preceding (1) passed.
- Three exhaustive source controls used d=2,n=1 and (q,m)=(3,1),(5,1),(3,2),
  totaling 85,120 cases. A was uniform; W,e,s had independent sign coefficients.
  These are algebra/moment controls, NOT Gaussian-source distribution tests.
  Substituting their actual unit coefficient variances gives U2=d^2*m and
  P2=n*d^2*h^2+U2. The mixed cross term was EXACTLY zero in every ensemble.
  Mean ||u||^2 was exactly 4,4,8; mean ||v||^2 was 44/9,116/25,28/3,
  below the corresponding bounds 13.3218855,12.9710470,21.9982991.
- Three growing reports checked the source recipe, (3)-(8), wide-information
  terms and native-profile lower bounds. No decoder was executed.

The independent-source and centered-secret premises are essential. Do not
apply (4) to a secret chosen after seeing A', to a correlated secret prior,
or to arbitrary nonzero-mean mixing coefficients. The older bounded-lift
proof remains available when its different hypotheses are met.

Gemini should expose `bounded_lift` and `upstream_gaussian_moment` as DISTINCT
proof contracts. The latter must record its exact distributional premises,
U2,P2,C_mom and source-averaged status. Do not double-charge delta_lift, and
do not remove it from the former contract. Update the classical flooding
comparator with the same energy bound. Keep all results REVIEW PENDING and
repair the upstream numerical certificate before emitting certified artifacts.

Next main-model work: explicit nonlocal conditional arithmetic or a
prior-specific measurement in this wider regime, followed immediately by a
matched classical attempt. Source preparation is substantially less entangled
with the old grid argument; efficient decoding remains the central obstacle.
