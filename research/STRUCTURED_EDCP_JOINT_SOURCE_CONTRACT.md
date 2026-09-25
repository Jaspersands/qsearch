# Structured EDCP: A Joint Source Contract With Unheralded Contamination

Date: 2026-09-25
Status: LOCAL DERIVATION / REVIEW PENDING. Not an independent verification of
Wen--Zheng, a novelty claim, an implemented state factory, or a lattice attack.

## 1. What This Pass Changes

The previous decoder notes assume known-amplitude structured EDCP states with
independent uniform public Fourier labels. This note audits the LAST quantum
stage of the proposed source reduction. It does not assume that individual
success probabilities, normalized postselection, or a shortest nonzero lattice
vector automatically provide the required joint guarantee.

For a separated classical instance (A,b=A*s+e mod Q), the construction below
gives, after discarding grid records and Fourier measuring the second registers,

    rho_out = p0 * Sigma_s(F)^(tensor L) + (1-p0) * tau,             (1)
    p0 = (1-2*C_grid*E0/Q)^(M*L).

Here F is the deliberately prepared, normalized finite coefficient amplitude,
E0 bounds ALL shifted errors, and Sigma_s(F) includes a uniform public label
and its pure phase state. The arbitrary contamination tau need not be close
to ideal. The clean event is NOT efficiently heralded by this argument.
Nevertheless, any solver with ideal success P succeeds with probability at
least p0*P, before charged preparation and truncation errors. A residual test
can verify an output using the original classical instance.

A factorization-free random-matrix bound supplies the separation premise over
COMPOSITE Q. A computable grid replaces any call for an unknown shortest-vector
length. The parameter regime already examined in the information note has
asymptotic room for this stronger, explicitly joint contract.

FOLLOW-UP: `research/STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md` now gives a
scoped local repair of the preceding classical stage. It replaces two invalid
intermediate claims and provides a smaller, explicitly certified error budget.
That new budget changes which finite points pass; the old-budget results in
section 8 remain valid as stated. Independent review and the reverse reduction
are still outstanding.

An important correction to our earlier audit: accurate PURE marginals do imply
an accurate joint product, with a square-root accumulation bound. Independence
is not an additional premise in that situation. The real source obligations
are a COMMON success event and justified error bounds. Section 2 fixes this
overstatement; sections 3-8 establish a direct route without it.

## 2. Correcting The Marginal Objection

Suppose a joint state rho has marginal trace distances

    T(rho_i, |psi_i><psi_i|) <= epsilon_i.

Writing P_i=|psi_i><psi_i| and using commuting projectors on distinct registers,

    1 - tensor_i P_i <= sum_i (I-P_i),
    <tensor psi_i|rho|tensor psi_i> >= 1-sum_i epsilon_i,
    T(rho, tensor_i P_i) <= min(1, sqrt(sum_i epsilon_i)).          (2)

Thus a polynomial number of negligible pure-marginal errors remains negligible
jointly. This applies on a COMMON classical branch with the stated pure target
for every register. It does not prove that such a branch has sufficient weight.
Separate statements that each register is good with constant probability are
not enough. Likewise, close mixed marginals alone do not imply a product.

The state sqrt(1-delta)|00>+sqrt(delta)|11> has each marginal delta-close to
|0>, but joint distance sqrt(delta) from |00>. This explains why the square
root cannot simply be removed. Conversely, a correlated classical mixture of
ordinary coset states with arbitrary centers causes no phase-label correlation
after the specified local Fourier measurements: the centers contribute only
global phases. Do not confuse classical center uncertainty with entanglement
or unknown coefficient amplitudes.

## 3. An Actual Coefficient Lift, Not An Assumed Inverse

Fix odd q>=3, d>=1, Q=q^d+1, and

    E(c) = sum_(i=0)^(d-1) c_i*q^i mod Q,
    S_q = (q^d-1)/(q-1),       h=(q-1)/2.

Evaluation on Z[X]/(X^d+1) is a ring homomorphism into Z_Q. Evaluation of
CENTERED representatives of Z_q[X]/(X^d+1) is not a homomorphism of that
quotient ring. This distinction matters for the paper's Phi_q^(f) map.

The q^d balanced coefficient vectors in [-h,h]^d evaluate bijectively to the
integers [-(q^d-1)/2, (q^d-1)/2]. Of the Q centered residues, only Q/2 lies
outside that interval. Its centered q-ary expansion is

    X^d - h*(1+X+...+X^(d-1)).

After reduction by (q,X^d+1), Phi(Q/2) has coefficients (h,-h,...,-h).
Its evaluation is Q/2+q mod Q, NOT Q/2. For example, q=5,d=2 sends
13 to coefficients (2,-2), whose evaluation is 18 mod 26.

Consequently, the explicit premise ||Phi(e_j)||_infty<=B<h excludes the
exceptional residue and DOES supply a lift v_j with

    e_j = E(v_j) mod Q,      ||v_j||_infty<=B.

The same lift can instead be provided directly as a mathematical premise;
the algorithm need not know it. Do not assert this for arbitrary B, even q,
or a general polynomial without a separate proof.

For any coefficient box ||c||_infty<=R, negacyclic multiplication has
coefficient norm at most d*R*B. Therefore

    ||E(c)*e mod Q||_(torus,infty) <= E0,
    E0 = d*R*B*S_q,                                              (3)
    ||e||_(torus,infty) <= E_orig = B*S_q.

Use integer ceilings for R,B if necessary. Each coefficient of a negacyclic
product is a signed sum of exactly d products, proving (3). No modular-q
carry estimate or unproved inverse-map identity is needed. A smaller certified
uniform shifted-error bound can replace E0. The source specialization uses
d a power of two; the arithmetic here does not require that restriction.

## 4. Separation For Random Matrices Over Composite Q

Let M denote the integer-instance row count (m_prime in the paper), n its
secret dimension, and A be uniform in Z_Q^(M by n). Define separation by

    ||A*v mod Q||_(torus,infty) > Delta for EVERY nonzero v in Z_Q^n. (4)

This includes injectivity. A lower bound on the shortest NONZERO image vector
alone does not: it can overlook a nonzero vector in ker A.

For a vector v of additive order t dividing Q, each independent row product
is uniform on (Q/t)*Z_Q. For 0<=Delta<Q/2, its probability of lying within
torus distance Delta of zero is

    (2*floor(Delta*t/Q)+1)/t.

There are J_n(t)=t^n*product_(p|t)(1-p^(-n)) vectors of exact order t. Hence

    Pr[(4) fails] <= sum_(t|Q,t>1) J_n(t)
                       *((2*floor(Delta*t/Q)+1)/t)^M.             (5)

This is a union bound, not an equality for the failure probability. It counts
kernel events as well as short nonzero images. Prime-only formulas are invalid.

For M>n+1 a useful bound requiring NO factorization is

    Pr[failure] <= 2^(-(M-n))*(1+2/(M-n-1))
                   + Q^n*(3*Delta/Q)^M.                          (6)

Proof: for t<Q/Delta the floor is zero, so its contribution is at most
t^(n-M). Bound their sum by sum_(t>=2)t^(-(M-n)), then by the first term
plus the integral from 2 to infinity. For t>=Q/Delta the row probability
is at most 3*Delta/Q; there are at most Q^n such vectors in total.
For Delta=0 use only the small-order sum.

Set a=ceil(Q^(n/M)), computed by an integer M-th-root operation, and

    Delta = Q/(6*a),
    delta_sep = 2^(-(M-n))*(1+2/(M-n-1)) + 2^(-M).                 (7)

Then (6) is at most delta_sep. Computing this certificate is polynomial in
the input bit length; it does not enumerate Z_Q or factor Q. It certifies a
distributional failure bound, NOT separation of an arbitrary supplied matrix.
If the marginal distribution of A is delta_A-close to uniform, its failure
probability increases by at most delta_A. Correlation with e or s does not
invalidate this MATRIX-ONLY probability statement.

## 5. A Finite, Computable Grid And A Uniform Good Event

More generally take an integer C_grid>=2 and width z=Q/C_grid. Assume (4),

    z+2*E0 < Delta,       2*C_grid*E0 < Q.                         (8)

For every preparation draw fresh independent offsets U_j uniform in Z_Q and
compute on integer torus inputs

    g_U(y)_j = floor((C_grid*y_j-U_j)/Q) mod C_grid.               (9)

All arithmetic is exact, including negative floor division. No continuous
random offset or finite-bit approximation to a boundary decision is required.
Uniform integers modulo Q can be generated by rejection from binary strings.

For a fixed center A*x, the residue r_j=(C_grid*(A*x)_j-U_j) mod Q is
uniform on {0,...,Q-1}. Define the margin event

    C_grid*E0 <= r_j < Q-C_grid*E0   for all j.                   (10)

Its exact probability is p_margin=(1-2*C_grid*E0/Q)^M, the SAME for every x.
On this event all points A*x-E(c)*e, simultaneously for every c in the
coefficient support, map to the same cell. This is a BOX-MARGIN argument;
it does not union-bound exponentially many pairwise events.

Furthermore, if two error-cloud points occupy the same cell, their centers
are within torus infinity distance <z+2*E0. By (8) and (4), the centers have
the same x. Thus every measured cell identifies at most one x, whether or
not it retains the full coefficient support. This logical identification
does not require the algorithm to invert A or recover x.

For the random-matrix certificate (7), a particularly simple grid is

    C_grid=12*a,        z=Delta/2.

The integer inequality

    48*a*M*L*E0 <= Q                                             (11)

implies (8) and p_margin^L >= 1-2*C_grid*M*L*E0/Q >= 1/2.
Parameters failing (11) can still use the exact p_margin^L when (8) holds,
but must report it rather than promise a constant clean weight.

## 6. The Quantum Construction And Its Joint Meaning

Let F(c) be any normalized, known finite amplitude supported in [-R,R]^d.
The intended implementation is a product truncated Gaussian. With classical
input (A,b), prepare

    sum_c F(c)|c> * Q^(-n/2)*sum_x |x> * |0>.

Compute A*x-E(c)*b into the third register. Relabeling the uniform x SUM,
only for analysis, gives

    Q^(-n/2)*sum_(c,x) F(c)|c>|x+E(c)*s>|A*x-E(c)*e>.

Compute g_U in a fourth register and measure it. By separation, each occupied
cell leaves one x and a subset of coefficients. On the margin event it leaves
ALL coefficients. Uncompute the third register by the PUBLIC reversible map

    third <- third - A*(second) + E(c)*b mod Q.

This is zero identically. No secret or hidden error is used in the circuit.
The good branch is exactly sum_c F(c)|c>|x+E(c)*s>.

For each good center its measurement probability is 1/Q^n. Averaging over
all centers and offsets gives clean weight exactly p_margin for the margin
event defined in (10). It is independent of A,e,s under the premises.
There may be additional clean branches outside this sufficient event; they
remain in the residual component of the decomposition.

Fourier measure the second register. Every a in Z_Q^n has probability 1/Q^n,
and the first register becomes, up to the global phase omega^(<a,x>),

    |phi_(a,s;F)> = sum_c F(c)*omega^(E(c)*<a,s>)|c>.

Define Sigma_s(F)=Q^(-n)*sum_a |a><a| tensor |phi_(a,s;F)><phi_(a,s;F)|.
Discard grid records; do not condition the solver on an unknown good flag.
With fresh preparation and offsets in all L repetitions, expansion of the
resulting mixture proves (1) with p0=p_margin^L. Shared classical A,e,s are
held FIXED in this statement. They do not create phase-label correlations
on its clean component. Even classically correlated good centers would be
harmless after the Fourier measurements.

This is not negligible trace-distance proximity of the whole output to the
ideal product. Bad batches are real. A clean-component guarantee is sufficient
for a success lower bound because the success POVM is positive and linear;
the residual component cannot destructively cancel its probability.

## 7. Gaussian Width, Error Accounting, And Verification

Use the explicit AMPLITUDE convention

    F_infty(c) proportional to exp(-pi*||c||^2/sigma^2).

Its coefficient probabilities have Gaussian width sigma/sqrt(2). If eta is
their one-block probability outside [-R,R]^d, the normalized truncated
product differs from the infinite product in trace distance

    sqrt(1-(1-eta)^L) <= sqrt(L*eta).                             (12)

For a positive integer R, an elementary tail certificate is

    eta <= min(1, d*sigma^2/(2*pi*R)*exp(-2*pi*R^2/sigma^2)).

The normalization is at least one; compare the positive tail sum with its
integral. If each finite preparation is within trace distance gamma of its
intended state, ordinary CPTP contractivity and a hybrid bound charge L*gamma
to the UNCONDITIONAL output. For a solver with ideal infinite-state success P,

    actual success >= p0*(P-sqrt(L*eta)) - L*gamma.                (13)

This avoids claiming that normalized postselection is contractive. For bad
source-instance probability delta_inst and a source-secret prior within
delta_prior of the intended prior, the conservative averaged bound is

    p0*P - delta_inst - delta_prior - p0*sqrt(L*eta) - L*gamma.

Here delta_inst can include delta_sep+delta_A+delta_e by a union bound.
No independence of matrix uniformity, error smallness, and the secret is
needed for that bound. P must refer to a solver using the stipulated ideal
ensemble; extra source side information cannot silently change this reference.

The source paper's displayed rho_r state has sigma=r. Its Definition 22 uses
sqrt(D_r), which instead has sigma=sqrt(2)*r. To meet that definition, prepare
the correspondingly wider amplitude and enlarge R in the grid/error budget.
Alternatively name the output problem parameter sigma/sqrt(2). This is a
constant-width conversion to track, not evidence that no reduction can exist.

If 2*E_orig<Delta, verify a proposed secret s_hat by computing

    ||b-A*s_hat mod Q||_(torus,infty) <= E_orig.                  (14)

The true secret passes. Two passing secrets would violate (4) by the triangle
inequality, so no incorrect secret passes on a good classical instance. This
requires no closest-vector oracle. Our default E0=d*R*B*S_q with d*R>=1,
together with (11), gives the needed inequality.

Consequences for the decoder notes: on THIS reduction, a classical post-readout
list decoder can test its candidates directly against (A,b); truth coverage
suffices and exhaustive marginal-likelihood ranking is unnecessary. This is
an additional SOURCE-SPECIFIC baseline, not a free verifier for standalone
EDCP. Public (A,b) contains information absent from the standalone ensemble;
using it does not contradict an EDCP information bound. Repeat independently
prepared batches to amplify a pointwise solver success guarantee. An averaged
guarantee over secrets alone does not justify a pointwise amplification claim.
Bad classical instances remain outside the uniqueness certificate.

## 8. What Is Repaired, And What Is Not

Wen--Zheng's Lemma 30 and Theorem 4 use a randomized grid for the final stage.
This note supplies a direct uniform-support event, a joint contamination
statement, explicit injectivity, finite offsets and charged Gaussian errors.
It does not certify their preceding Lemma 28 or every general-polynomial case.

There is also a small constant error in the stated all-batch success estimate:
with k=M*L, the displayed per-state reasoning gives (1-1/k)^k, which is BELOW
1/e, not above. It is at least 1/4 for integers k>=2 and vanishes at k=1.
This alone does not refute a polynomial reduction. Our stronger margin budget
(11) supplies at least 1/2 without that calculation.

The existing information note's asymptotic source regime survives these
stronger sufficient conditions. Set d=kappa_sec through powers of two,
n constant, L constant, q a prime between d^12 and 2*d^12,

    m=ceil(log d), M=ceil(d*log q), R=d, sigma=sqrt(d),
    r1=r1_prime=ceil(sqrt(d)),
    r2 >= 2*d*q^((n*d+2)/(d*m)),
    B >= 2+c_max+2*m*r1*r2*d^2*sqrt(d).

Then B=O_n(d^4*log d), a=O_n(1), B<h, and the ratio of the left side of
(11) to Q is O_n(L*d^7*(log d)^2/q), tending to zero. The random-matrix
failure bound is exponentially small in M. Gaussian joint truncation is
exponentially small in d. This demonstrates compatibility of explicit
conditions, not hardness of these particular source parameters.

Finite analytic evaluations used n=1,L=288,q=nextprime(d^12). To avoid silently
rounding the source error DOWN, set

    u=ceil((q^(d+2))^(1/(d*m))), r2=2*d*u,
    B=3*d+26+2*m*r2*d^3, E0=d^2*B*S_q.

The integer root is exact; q values came from SymPy and are not accompanied
by primality certificates. The margin inequality itself was checked with
integers. Clean weights and logarithms used 90-digit floating arithmetic.

| d | M | a | (48*a*M*L*E0)/Q | Clean Weight Lower Bound | (11) Passes |
|---:|---:|---:|---:|---:|:---|
| 64 | 3195 | 3 | 1138.89466750 | 4.12676e-248 | No |
| 256 | 17035 | 3 | 4.30506979 | 0.1161892 | No |
| 1024 | 85174 | 3 | 0.01270622 | 0.9936670 | Yes |

The middle point fails the convenient one-half certificate, but its explicit
clean weight is not negligible. Log10 matrix-failure bounds at these points
are approximately -961.31, -5127.57, -25639.45. Log10 joint truncation bounds
are -85.59, -347.25, -1394.79. These are analytic certificates/reference
evaluations, NOT simulations of the quantum reduction or audited source data.

## 9. Bounded Checks And Attempts To Break The Argument

All checks below ran in temporary interpreter sessions, with no production
integration or full-suite claim. Random reference seed: 20260925.

1. Enumerated 27,204 centered residues for q in {3,5,7,9,11} and d in {1,2,3,4}.
   Each parameter pair had exactly the stated exceptional residue. Every
   strict small-Phi lift passed; accepting B=h would incorrectly admit it.
2. Exhausted 14,962 matrix/radius instances across 15 cases with Q in
   {3,4,6,8,10}, including n=2, testing (5) against ACTUAL separation failures.
   All probabilities stayed below the divisor union bounds. Another 3,996
   divisor-sum evaluations, Q=3..150, n=1..3, M=n+{2,4,8}, checked (6).
3. A=0,e=0 deliberately violates injectivity. The second register stays
   uniform and Fourier measurement yields only a=0, not uniform labels.
   The residual verifier then admits all secrets. These controls falsify
   versions of the claim that omit (4).
4. At q=53,d=2,Q=2810, A_j=2^j mod Q for j=0..11 has exact minimum
   torus infinity separation 1022. With C_grid=5, R=B=1 and E0=108,
   z+2*E0=778<1022 and the margin is nonempty. The actual e=(1,...,1)
   has shifted error at most 54, so the generic certificate is conservative.
   Across 24 independent offset vectors, 606,960 (x,c) records and 168,145
   occupied cells had no cross-center collision. All 190 sufficient-margin
   centers retained the entire coefficient support.
5. For the same reference, all 81 coefficient pairs were checked against ALL
   2810 one-coordinate offsets: 227,610 offset comparisons. Their averaged
   coherence is [1-C_grid*|E(c)-E(c')|/Q]^12. Gaussian amplitude width 1.7
   gave a positive semidefinite residual rho-p_margin*|F><F|, and its two-block
   tensor analogue also passed. The one-block trace distance from ideal was
   0.3189123: a clean-component certificate is NOT whole-state closeness.
   This finite reference has p_margin=0.00296536 and is not a scaling success.
6. Public third-register uncomputation passed 2,700 modular identities,
   including vector secrets and nonzero errors. No hidden secret was used
   in the evaluated uncomputation expression.
7. At Q=10, two identical unknown centers (maximally classically correlated)
   passed 1,000 full coefficient-amplitude checks over every Fourier label
   pair and center. Only a global phase depended on the center. Twelve GHZ
   controls checked the pure-marginal square-root bound rather than the
   invalid linear-error claim.
8. At the separated q=53 reference, 25,290 candidate checks across nine
   different true secrets found exactly one residual-verifier acceptance
   each, the true secret. The noninjective control accepted all 2810 instead.

These tests corroborate the algebra; they do not prove all-size correctness.
Independent review should attack (i) the finite-grid branch decomposition,
(ii) the distinction between a hidden event and an algorithmic flag,
(iii) the small-Phi lift premise, (iv) error accumulation through the actual
source implementation, and (v) use of averaged versus pointwise solver success.

## 10. Remaining Blockers And Division Of Work

MAIN MODEL NEXT: audit Lemma 28's transformation from polynomial/module LWE
to the classical integer instance. In particular, establish the actual JOINT
distribution of A, secret and error, the advertised error lift and norm bound,
matrix uniformity, parameter growth, and the use of Gaussian mixing. This is
now the next unverified source link; another decoder tweak does not repair it.
Then return to a genuinely conditional multi-block operation, with the strong
classical post-readout baselines already derived.

GEMINI IMPLEMENTATION, following independent review of this note:

- Add `theorems/structured_edcp_joint_source_contract.py`: explicit amplitude
  width, finite support, actual coefficient-lift premise, integer grid, matrix
  separation distributional certificate, clean-batch weight, joint tail and
  preparation errors. Distinguish a deterministic small-reference separation
  check from a distributional certificate for a random source matrix.
- Implement (5) only as a bounded factorization-assisted reference; implement
  (6)-(7) for scalable reports. Never enumerate the modulus in a scalable path.
- Add the source-specific verifier (14) and allow the profile-list decoder
  to use it only when source side information and its uniqueness premises
  are supplied. Do not expose it as an oracle in standalone EDCP experiments.
- Preserve `source_common_success`, `clean_component_weight`,
  `unheralded_contamination`, `joint_trace_error`, `width_convention`,
  `source_instance_failure`, and `upstream_reduction_review_pending` separately.
  A constant clean weight must NOT become a negligible trace-error claim.
- Reproduce the eight controls above, including exceptional Phi, noninjective
  matrices, negative floor division, torus wrap, arbitrary shared errors,
  pure-marginal square roots and the verifier's missing-premise failure.
- Wire reviewed reports to the existing source/proof audit, not a new candidate
  promotion. Run repository validation and resolve unrelated integration test
  failures before describing the production pipeline as verified.

No new quantum advantage, efficient joint decoder, efficient basis finder,
cryptographic security estimate or complete source reduction is established.

## Sources And Related Local Notes

- Wen and Zheng, *Module Learning With Errors and Structured Extrapolated
  Dihedral Cosets*, [IACR ePrint 2026/155](https://eprint.iacr.org/2026/155.pdf).
  Inspected the existing local PDF downloaded on 2026-09-24: definitions 15-19,
  Lemmas 28-30, Theorem 4 and Lemma 51. A fresh web fetch returned 403. This
  audit is tied to that inspected version, not an assertion about a newer one.
- Brakerski, Kirshanova, Stehle and Wen, *Learning With Errors and Extrapolated
  Dihedral Cosets*, [arXiv:1710.08223v2](https://arxiv.org/abs/1710.08223v2).
  The cube-separation construction is prior methodology. No novelty is claimed
  for using it; the contribution here is a scoped, explicit source contract
  for the repository's decoder assumptions.
- `research/STRUCTURED_EDCP_INFORMATION_THRESHOLD.md`, section 7: source
  parameter compatibility, width conventions and the now-refined joint issue.
- `research/EDCP_CORRELATED_CENTER_AUDIT.md`: normalized-postselection and
  square-root truncation audit; unknown-center families are a different contract.
- `research/STRUCTURED_EDCP_PROFILE_LIST_DECODER.md`: source-specific verification
  removes likelihood selection when a list contains the truth, but does not
  remove the list-generation cost or classically simulate the quantum source.
