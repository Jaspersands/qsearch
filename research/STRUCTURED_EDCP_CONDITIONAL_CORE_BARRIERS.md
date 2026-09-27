# Structured EDCP: Conditional Cores And Representation Barriers

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

## 1. Decision And Scope

The classical-readout simulation removes one potential source of advantage,
but not a genuine coherent joint-fiber operation. This pass sharpens the
specification of that remaining operation:

- A small-bond tensor state across a whole coefficient-block cut cannot
  represent the required source-weighted fibers with high fidelity.
- Preparing most blocks with a target-INDEPENDENT frequency marginal and
  repairing only a small block group fails even if that marginal is optimized.
  This generalizes the native-prior obstruction in the Klein audit.
- Conversely, if an informative conditional core is already available, other
  blocks can be attached using their unconditional prior, with a charged error.
  This does not construct the core or make it free.

These statements constrain representations and particular preparations, not
all quantum algorithms, tensor layouts, samplers or prior-specific decoders.
Large Schmidt rank does NOT imply exponential quantum circuit size. Section 7
includes a direct counterexample to that invalid inference.

No production wiring, candidate promotion, independent proof review or novelty
claim. Schmidt truncation, fidelity monotonicity, Young's inequality and
Gaussian collision bounds are established tools; the specialization is derived
explicitly below.

## 2. The Exact Bipartite Fiber

Fix the public scalar labels, n=1, and partition the coefficient blocks into
S and R. Let p(x) and v(y) be their respective total-frequency distributions
on Z_Q, including their actual multipliers. Their normalized conditional
coefficient states |S_x> and |R_y> have disjoint supports for distinct x,y.
The full frequency law is r=p*v. For r(u)>0, its weighted fiber is

    |zeta_u> = sum_x sqrt(p(x)*v(u-x)/r(u)) |S_x>|R_(u-x)>.  (1)

This is already a Schmidt decomposition across S|R: both families are
orthonormal. Empty terms are omitted. It holds with finite digit truncation,
noninjective within-block evaluation, and nonuniform public frequency laws.

The source-weighted squared fidelity of prepared states rho_u is

    F_bar=sum_u r(u)*<zeta_u|rho_u|zeta_u>.

This weights the actual fibers, not a uniform list of all residues. Their
weights do not depend on the secret phase. For frequency-controlled coherent
preparation/erasure, source-weighted VECTOR error bounds every phase as in
`STRUCTURED_EDCP_INTERVAL_TRANSFER_AUDIT.md`, section 10. High squared
fidelity alone does not supply a missing coherent global-phase convention.

## 3. Tensor Bond-Dimension Lower Bound

The greatest squared overlap of a Schmidt-rank-at-most-chi vector with (1)
is the sum of its chi largest squared Schmidt coefficients. Convex mixtures
of such vectors obey the same upper bound. Therefore any such representation
satisfies

    F_bar <= G_chi(p,v),
    G_chi = sum_u Top_chi {p(x)*v(u-x): x in Z_Q}.           (2)

Here Top_chi denotes the sum of the largest chi entries. Cauchy--Schwarz
first within a row and then over u gives

    G_chi <= sqrt(chi*Q*(sum_x p(x)^2)*(sum_y v(y)^2))
           = sqrt(chi*c2(p)*(1+chi2(v))),                   (3)
    chi2(v)=Q*sum_y v(y)^2-1.

Always cap probability upper bounds at one. No pointwise-flatness assumption
is needed. A useful independent check is

    G_chi <= Top_chi(p) + TV(v,uniform).                     (4)

Indeed G_chi is the largest mass of a set selecting at most chi entries in
each row of the joint law p(x)*v(u-x). Replacing v by uniform changes the
mass of every such event by at most TV(v,uniform). At uniform v equality
holds: G_chi=Top_chi(p). This proves the source-weighted statement without
silently discarding unusual u or replacing an average by a worst case.

### Native Gaussian Consequence

For S consisting of one block with a UNIT label, finite radius R0 satisfying
2R0<=q-1 makes evaluation injective. With amplitude width sigma, put

    Z=sum_(j=-R0)^R0 exp(-2*pi*j^2/sigma^2),
    c_digit=sum_(j=-R0)^R0 exp(-4*pi*j^2/sigma^2)/Z^2.

Then c2(p)=c_digit^d exactly. If E[chi2(v)]<=delta_R over the other labels,
(3) and Jensen imply

    E F_bar <= sqrt(chi*c_digit^d*(1+delta_R)),
    chi >= F_target^2/(c_digit^d*(1+delta_R))                (5)

as a necessary condition for E F_bar>=F_target, with one common upper bound
chi on every prepared state's Schmidt rank. Since c_digit=(1+o(1))/sigma,
constant target fidelity at sigma=sqrt(d) needs chi of order at least
d^(d/2), up to the displayed Gaussian/tail factors.

This rules out polynomial bond dimension for an MPS ordering with this
whole block on one side of a bond, or a tree tensor edge separating it.
It does NOT rule out a different variable ordering, a network with many
crossing edges, a succinct arithmetic tensor, or a polynomial-size quantum
circuit. Cost the product of crossing bond dimensions for a general cut.
Nonunit labels must not be silently inverted or assigned the injective c2.

## 4. Target-Independent Marginals Cannot Repair A Small Core

Now consider a proposal whose measured R-frequency distribution h(y) is
independent of u. It can depend on all PUBLIC labels and be arbitrarily
expensive to compute. The state may otherwise be mixed, coherent, and
target-dependent. Measuring the R frequency and using fidelity monotonicity
bounds its overlap by

    <zeta_u|rho_u|zeta_u>
       <= [sum_y sqrt(h(y)*v(y)*p(u-y)/r(u))]^2.

Define the nonnegative matrix

    T_(u,y)=sqrt(v(y))*sqrt(p(u-y)).

The best resulting weighted bound over EVERY h is

    F_bar <= F_fixed = ||T||_op^2.                          (6)

The Perron eigenvector of T^T*T can be chosen nonnegative, so optimizing
over normalized sqrt(h) gives this spectral norm, not a restricted search
over selected priors. With everywhere-positive p and suitable conditional
states on S, the fidelity bound is attainable in principle. No efficient
construction is inferred. For laws with zeros, (6) remains an upper bound.

Let

    P_S=(sum_x sqrt(p(x)))^2/Q.

For exactly uniform v, T is a scaled circular convolution matrix and
F_fixed=P_S. For general v there is the useful stronger perturbation bound

    F_fixed <= min(1, P_S+sqrt(chi2(v)*P_S)).                (7)

Proof: write C_(u,y)=sqrt(p(u-y)), so T*T^T=C*diag(v)*C^T.
The uniform part has operator norm P_S. For the difference B, let
delta=v-1/Q and c(t)=sum_x sqrt(p(x)*p(x+t)). Then

    ||B||_F^2=sum_(y,z) delta(y)*delta(z)*c(y-z)^2.

The matrix with entries c(y-z)^2 is positive semidefinite, circulant and
entrywise nonnegative. Its largest eigenvalue is its common row sum
sum_t c(t)^2 <= sum_t c(t) = Q*P_S, since 0<=c(t)<=1.
As ||delta||_2^2=chi2(v)/Q, ||B||_op<=||B||_F<=sqrt(chi2(v)*P_S).
Triangle inequality proves (7). This retains a meaningful bound when the
rest distribution has bounded chi-square, rather than requiring negligible
pointwise deviations from uniform.

If S contains k Gaussian blocks, grouping frequencies cannot increase the
sum of square-root probabilities, giving the prior-free parameter bound

    P_S <= min(1, kappa^(k*d)/Q),
    kappa=(sum_j exp(-pi*j^2/sigma^2))^2
                /sum_j exp(-2*pi*j^2/sigma^2).              (8)

Use the actual finite support or the convergent infinite sums consistently.
For q=d^(a+o(1)), sigma=d^(b+o(1)), fixed k with b*k<a has exponentially
small P_S in d*log d. If E chi2(v) is bounded, (7) remains exponentially
small after averaging: E F_bar<=P_bound+sqrt(delta_R*P_bound).

Thus preparing the other blocks from ANY fixed frequency marginal and
repairing only one or a few insufficient blocks cannot implement a faithful
joint fiber. This is stronger than the previous calculation for the specific
unconditional-prior proposal. It is not a prohibition on iterative methods
that genuinely change that marginal with u.

For q approximately d^12 and sigma approximately sqrt(d), the necessary
information threshold from this bound approaches k>=24. Equality is not
sufficiency, and finite constants shift where (8) becomes vacuous. This does
not require every useful circuit gate to touch 24 blocks: successive gates
can build target-dependent correlations. The condition is on the final
unconditioned marginal, not a circuit locality lower bound.

Heralding needs care. If the normalized successful output has a
target-dependent marginal, it is not covered by a premise claiming that
marginal is fixed. If the full output before selection has the fixed marginal,
the bound applies to SUCCESS-WEIGHTED fidelity; discarding failures cannot
promote a tiny success probability into an efficient preparation.

## 5. A Constructive Core Extension, With Its Remaining Cost

There is an important opposite case. Let R now be an informative core with
an AVAILABLE controlled conditional preparation |R_t>. Prepare S from its
unconditional prior and compute t=u-x from its frequency x:

    |phi_u> = sum_x sqrt(p(x)) |S_x>|R_(u-x)>.

Unsupported t may use an arbitrary normalized filler; its target amplitude
is zero. The controlling register u is retained throughout. The positive
overlap is

    BC_u=(p*sqrt(v))(u)/sqrt(r(u)),
    F_extension=||p*sqrt(v)||_2^2 >= (sum_y sqrt(v(y)))^2/Q
                                      >= 1/(1+chi2(v)).     (9)

The first inequality retains the constant Fourier component of the
convolution; the second is the collision/Hellinger inequality from the
information note. In particular, if v is uniform, this construction is EXACT
for arbitrary p. Source-weighted squared VECTOR error is at most

    Delta_extension^2 <= 2*(1-F_extension)
                         <= 2*chi2(v)/(1+chi2(v)).          (10)

The first step uses 0<=BC_u<=1, hence BC_u>=BC_u^2. The controlled inverse
has the same vector error and therefore the same phase-uniform guarantee.

This is an extension lemma, NOT a recursive solution of the hard core. It
says that excess blocks need not all be jointly sampled from scratch once
the actual informative core has been solved. Solving only the last single
block instead of an informative core falls under (7), not (9)'s good regime.

### Approximate Core Errors Change Their Weighting

Suppose the core preparation has pointwise vector error e(t). The residue
fed to it in this extension is distributed as

    w(t)=sum_x p(x)*r(t+x) = v*p*reverse(p),

NOT necessarily v(t). Its contribution to squared vector error is
sum_t w(t)*e(t)^2. If the available core guarantee is
sum_t v(t)*e(t)^2<=Delta_core^2, one conservative repair is

    sum_t w(t)*e(t)^2 <= Delta_core^2 + 8*TV(v,uniform),      (11)

because e(t)^2<=4 and TV(w,v)<=2*TV(v,uniform). Alternatively, a proven
pointwise (1-epsilon)/Q<=v(t)<=(1+epsilon)/Q gives a multiplicative factor
(1+epsilon)/(1-epsilon). The total vector error adds by triangle inequality.
Do not reuse a source-weighted core error unchanged after altering its input
distribution. Computing good core fibers and their coherent phases remains
the unsolved algorithmic task.

## 6. Source-Compatible Analytic References

Use the finite coefficient source sigma=sqrt(d), R0=d, L=288,
q=nextprime(d^12), n=1. For the rank bound, condition the FIRST label to be
a unit; all other labels remain independent uniform. This event and its
resource cost must be charged in an actual source workflow. No postselection
on the OTHER 287 labels is needed here.

The earlier information theorem gives an unconditional bound for those labels:

    beta=287*h2/(2*ln(q))-1,       h2=-ln(c_digit),
    T_tail=(2d)^(1-beta)/(beta-1),
    delta_R <= [(1+b_digit^(2d))/2]^287 + 2*T_tail.          (12)

The first term retains the binary obstruction; it is not set to zero. Bound
the truncated digit parity via Poisson summation plus twice its probability
tail. For the following points beta is about 4.97917 and the bound is finite.
This uses the SAME finite conditions R0<=d and 2R0<=q-1 from that theorem.

110-digit reference arithmetic, not interval-certified decimal enclosures or
executed high-dimensional state preparation:

| d | Mean chi2(v) Upper Bound | log10 Necessary Bond For Mean F>=0.9 | log10 Fixed-Marginal Fidelity Upper, k=1 |
|---:|---:|---:|---:|
| 64 | 2.07156e-9 | 57.7062 | -664.1996 |
| 256 | 8.32916e-12 | 308.1632 | -3531.2030 |
| 1024 | 3.34891e-14 | 1541.1821 | -17654.3200 |

The third column is (5); the fourth is the averaged (7)-(8). These are
different constraints on different proposal classes, not two costs of one
algorithm. All refer to the IDEAL finite clean source. Source contamination,
truncation comparisons to an untruncated source, numerical errors and label
selection are still separate. No current cryptographic security claim follows.

## 7. Verification And Falsifiers

Seed 20260925; bounded mathematical interpreter references, not production
tests or a full-suite claim.

- Eighty distribution pairs over Q in {5,10,17,26} used five random p laws
  and four mixtures of a uniform and a nonuniform v law per modulus. All
  80 optimized fixed-marginal spectral values agreed with their nonnegative
  eigenvector witnesses. All 240 directly computed Schmidt spectra agreed
  with (1), and 320 top-rank checks passed (2) and (4).
- The same 80 pairs checked the extension overlap identity, its lower bound,
  its positive vector-error bound, and exact extension when v is uniform.
- Another 96 cases used p support sizes 1,2,4,Q and several rest mixtures.
  They checked the Frobenius perturbation proof of (7) directly, including
  narrow-support cases with useful nonvacuous bounds. Another 384 checks
  tested the collision rank bound (3).
- Three growing analytic reports evaluated (5), (7)-(8), and (12) with
  finite Gaussian sums and nonzero parity/tail terms. These are bounds,
  not executions of a conditional-core algorithm.

Countercontrols are essential:

1. If BOTH frequency laws are point masses, the only fiber is a product state
   and rank one is exact. Dropping the chi2(v) dependence would falsely exclude
   it; the stated bounds are vacuous as they should be.
2. If both laws are uniform, the fiber is
   Q^(-1/2)*sum_x |x>|u-x>, with Schmidt rank Q and rank-chi fidelity chi/Q.
   Nevertheless uniform x preparation and reversible modular subtraction
   prepare it with polynomial bit-complexity. High rank is NOT gate hardness.
3. If v is uniform and p is arbitrary, the extension in section 5 is exact.
   Reversing the roles and leaving the uniform side target-independent instead
   limits fidelity to P_S. A blanket ban on all unconditional block sampling
   would therefore be false.
4. Iterative walks that change the rest marginal with u, alternative tensor
   orderings, narrow-prior discrimination without coherent fiber recovery,
   and genuinely succinct high-rank arithmetic circuits are not excluded.

## 8. Implementation Contract And Next Research

FOLLOW-UP: `STRUCTURED_EDCP_LOCAL_MOVE_OBSTRUCTION.md` now answers the
native local-walk question below. Sparse block updates have no within-box
fiber edges with high probability; extending to Gaussian tails gives a small
reversible-chain gap on most source-weighted fibers. Nonlocal arithmetic and
off-fiber preparation remain outside that result.

Gemini should record these as SCOPED representation/proposal diagnostics:

- Validate each public law and label access model, the physical bipartition,
  probability normalization, and whether a rank or fixed-marginal premise
  actually holds. Do not use a generic "tensor method rejected" status.
- Keep F_bar, vector error, conditional fidelity and success-weighted fidelity
  distinct. Include both positive countercontrols above and mixed-state tests.
- Tiny Q-sized SVD/eigenvalue checks are mathematical references only. The
  scalable checks use digit collisions, source bounds and logarithms.
- Preserve the changed core-residue weighting in (11). An average core
  preparation guarantee is not automatically composable.
- Do not implement an "available core" stub that silently supplies the
  missing operation, or promote the candidate based on that assumption.

MAIN MODEL: investigate actual controlled preparation of an informative core
using arithmetic or target-dependent dynamics. Require an explicit map, gate
cost, source-weighted coherent error and classical comparator. The immediate
questions are whether local carry updates connect the native fibers, whether
their mixing/conductance survives random public labels, and whether there is
a compact arithmetic circuit despite the tensor-cut obstruction. A formal
conditioning equation or a near-flat output frequency law is not a solution.

## Sources And Local Dependencies

- Verstraete and Cirac, *Matrix product states represent ground states
  faithfully*, [arXiv:cond-mat/0505140](https://arxiv.org/abs/cond-mat/0505140).
  General context for MPS/Schmidt approximation, not a theorem about this EDCP
  family. The rank and spectral bounds used here are derived directly above.
- `STRUCTURED_EDCP_INFORMATION_THRESHOLD.md`: exact composite-modulus
  collisions, all-divisor bound and Gaussian entropy converse.
- `STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md`: the earlier special case with an
  unconditional PRIOR marginal and only one repaired block.
- `STRUCTURED_EDCP_INTERVAL_TRANSFER_AUDIT.md`, section 10: coherent fiber
  erasure and the correct source-weighted vector error criterion.
- `STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md`: source-specific
  dequantization of local Fourier readout, not of these coherent operations.
