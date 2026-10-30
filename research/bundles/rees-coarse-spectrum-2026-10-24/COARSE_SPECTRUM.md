# Low-Rank Mixed Conjugation Without Spectral Separation Advice

2026-10-24. LOCAL CONSTRUCTIVE REDUCTION / INDEPENDENT REVIEW PENDING.
No new antisymmetrization or density-matrix simulation primitive, no novelty
certification, no quantum execution, and no classical-input speedup claim.

## Decision: The Exact Task Is Unchanged

The preceding simple-spectrum source cannot preserve rotations inside a
degenerate eigenspace. The support-only source forgets distinct eigenvalues.
Neither solves the general low-rank mixed conjugation task. The construction
here removes the simple-spectrum, minimum-positive-weight, known-rank and
minimum-eigenvalue-separation assumptions, not the task's global orbit gap.

Input:

- Independent copies of an unknown density matrix rho on q qubits.
- A supplied upper bound R on rank(rho), not the exact rank or eigenbasis.
- The same public explicit exponent-p Lazard group, fixed class c<p, and
  costed controlled LINEAR representation U(g) used by the existing Rees
  theorem and zero-moment source. No new hidden-function oracle is supplied.
- A promised delta in (0,1] such that TD(rho,U(g)rho U(g)^*)>=delta for
  EVERY g outside H={g:U(g)rho U(g)^*=rho}.

Output generators of this SAME H. The conditional algorithm is polynomial
in R, 1/delta, q, the existing fixed-class receiver/design costs, and inverse
error. Rank exponential in q is excluded. The global gap is a genuine input
promise; it is not certified by observing a few overlaps. Arbitrarily tiny
positive eigenvalues, arbitrarily small eigenvalue differences and exact
degeneracies are permitted under the remaining promises.

## 1. Coarsening Preserves The Entire Hidden Group

Let h=delta/(32R) and choose an offset u in [0,h). Discard eigenvalues below
c=h+u. Partition the rest into intervals [c+jh,c+(j+1)h), j>=0. Let P_j be
the corresponding nonempty spectral projectors and a_j=c+jh their distinct
positive LEFT endpoints. Define only for the proof

    A = sum_j a_j P_j.

No classical matrix A or spectral projector is given to the algorithm.
We have 0<=A<=rho, tr(A)<=1, and ||rho-A||_1<=2Rh. Every symmetry of rho
preserves its spectral bins, so H is contained in Stab(A). Conversely, if
g fixes A, then

    TD(rho,U(g)rho U(g)^*) <= ||rho-A||_1 <=2Rh=delta/16<delta.

The global promise forces g in H. Therefore Stab(A)=H, EXACTLY, even
though rho and A may have different ranks and eigenvalue multiplicities.
No assumption that the individual eigenspaces are identifiable is needed.

For g outside H, the triangle inequality gives

    TD(A,U(g)A U(g)^*) >= delta-2Rh.

Writing eta_j=||P_j-U(g)P_j U(g)^*||_op and r_j=rank(P_j), equal-rank
projector principal angles give

    TD(A,U(g)A U(g)^*) <= sum_j a_j r_j eta_j
                      <= max_j eta_j,

because sum_j a_j r_j=tr(A)<=1. Thus some eta_j>=delta-2Rh>=delta/2.
This is a global, all-g argument; no union bound over group elements or
small measured subset of them is used.

## 2. A Pure Source Keeping All Retained Eigenspaces

For each nonempty bin prepare its top exterior state omega_j, the normalized
wedge of ANY orthonormal basis of im(P_j). A change of that basis changes
only a phase. Set Psi=tensor_j omega_j, ordered by increasing bin index.
Act on every physical factor with U(g); there are sum_j r_j<=R factors.
Pad unused registers with a fixed state acted on by identity if a fixed
register layout is required.

For a frame V_j of the bin (used only in the proof),

    <omega_j|U(g)^tensor(r_j)|omega_j> = det(V_j^* U(g) V_j).

On H this has modulus one, including arbitrary internal eigenspace
rotations. The product phase is a character of H. Off H, Section 1 and
the principal-angle identity imply

    |<Psi|U(g)^tensor(sum r_j)|Psi>|
       <= sqrt(1-delta^2/4) <= 1-delta^2/8.

Apply the EXISTING zero-moment Rees evaluation design to independent Psi
copies to cancel that character. Use the existing source amplification and
fixed-class receiver. This is the original Rees lift, not a second cover.
The ray gap gamma=delta^2/8 replaces the preceding sources' constants.
No internal logical action, unknown basis, or conjugate state is computed.

The source is a tensor of separate bin wedges, NOT the wedge of the whole
support. The latter would again forget eigenvalues and can falsely retain
symmetries of a nonuniform full-rank state.

## 3. Finite Random Grid Instead Of A Spectral-Gap Promise

Choose K a power of two with K>=128R/epsilon and u=jh/K for a uniformly
random integer 0<=j<K. Set a=epsilon*h/(128R). For any fixed positive
eigenvalue, at most 2Ka/h+2 offsets put it within distance a of a boundary.
A union bound over at most R positive eigenvalues gives

    Pr[bad grid] <= 2Ra/h +2R/K <= epsilon/32.

Zero is always strictly below the cutoff c>=h and is not a near-boundary
retained eigenvalue. At most J=ceil(1/h)+1 bins need to be inspected.
All numbers are rational and the offset needs finitely many random bits.
The grid is chosen ONCE, before source construction, and reused throughout.

On a good grid, estimating an eigenvalue to error <=a/2 classifies it
correctly. Use the existing copy-based controlled density-matrix evolution
and binary phase-estimation construction, with all program copies fresh and
separate from retained targets. A QPE grid P>=256/(a*zeta) suffices for
per-target eigenvalue error failure <=zeta using the earlier conservative
tail bound. Estimate phases of exp(i*pi*rho/2) in [-1/2,1/2), as before.
Discard the detailed estimate and keep only the bin index.

The spectral classification comparison is on fresh rho targets, which are
mixtures of eigenstates. It is NOT a diamond-norm approximation to a coarse
projector instrument on arbitrary superpositions: fine QPE can dephase
within a bin. Fresh independent targets make the mixture-level error bound
sufficient here. DME and physical gate errors, in contrast, are charged as
complete-instrument errors on arbitrary references. These are distinct
claims; do not interchange them.

Every occupied retained bin has probability w_j=tr(P_j rho)>=h. The ideal
filtered density sigma_j=P_j rho P_j/w_j has every positive eigenvalue at
least h. It need not be flat. Therefore neither arbitrarily small original
weights nor tiny within-bin separations enter the subsequent copy cost.

## 4. Nonflat Antisymmetrization And Rank Discovery

Use the published corrected antisymmetric growth measurement. If k retained
systems lie in wedge^k(V) and a fresh density sigma on V is appended, let
Gamma be the retained state's one-particle density, normalized so tr(Gamma)=k.
Fermionic exclusion gives 0<=Gamma<=I_V: occupancy of any unit vector has
eigenvalues zero and one on the antisymmetric subspace. The success mass is

    p_k = [1-tr(Gamma*sigma)]/(k+1)
        = tr[(I-Gamma)*sigma]/(k+1).

For dim(V)=r and sigma>=h I_V, this implies

    p_k >= h*(r-k)/(k+1) >= h/(R+1)       when k<r.

At k=r, success is identically zero. The corrected failure instrument
retains antisymmetry and support, so the lower bound holds after EVERY
failure history, not only on average. Detailed ancilla indices must not
be measured before correction; the existing countercontrol still applies.

Preprocess every bin as follows. Try to obtain one filtered target using a
capped rejection sampler. If none is obtained, mark the bin empty. Otherwise
grow its wedge. After L_g consecutive growth failures at a fixed size,
record that size as its rank. Reset the failure counter after each success.
Attempting to grow beyond R is ABORT. False early stops are bounded below;
their probability is not declared zero. Discard these preprocessing targets.
Reject metadata with total recorded rank zero or exceeding R.

For subsequent packets use the recorded bins/ranks and fresh originals.
Grow each bin to its recorded rank with the same stage caps. A fetch or
growth timeout here is ABORT, not a smaller-rank packet. On correct metadata
and successful ideal extraction each output is the SAME pure Psi for every
record. No acceptance-dependent eigenbasis or mixture weight survives.
The full failure mass remains charged. Unknown rank is learned, not advice.

## 5. One Explicit Polynomial Resource Schedule

Let B cap receiver leaves, M be the existing public zero-moment design
size, and ell>=log2 of the Rees-cover order. These are paid external
parameters, not computed from a small fixture. Define ceil_log2 as a
nonnegative integer ceiling; it upper-bounds the natural logarithms below.

    gamma = delta^2/8
    k = ceil((ell + ceil_log2(8B/epsilon))/gamma)
    W = B*k*M                                independent Psi packets
    V = J*(R+1) + W*R                        growth-stage cap
    L_g = ceil((R+1)/h * ceil_log2(32V/epsilon))
    F = J + W*R + V*L_g                      filtered-target request cap
    L_c = ceil(ceil_log2(32F/epsilon)/h)
    S = F*L_c                               spectral-attempt cap

Every occupied-bin fetch fails with probability <=exp(-h L_c), so the
union of erroneous empty declarations and fetch aborts is <=epsilon/32.
Every prematurely stopped preprocessing stage or timed-out packet stage
has probability <=exp[-h L_g/(R+1)]; their union is <=epsilon/32.
The same clocks apply on erroneous histories. Empty bins cost time but
are not successes and must not be repeatedly resampled without a cap.

Set zeta=epsilon/(32S), eta=epsilon/(32S), and allocate epsilon/(32S)
to each spectral experiment's public gates. For QPE with t bits, controlled
time (pi/2)*2^b is less than 2*2^b. The already derived bound
half_diamond <=2*time^2/N for controlled DME permits

    N_b = ceil(8*t*4^b/eta),        b=0,...,t-1

fresh PROGRAM copies per bit. The raw-copy cap is

    S * (1 + sum_b N_b).

The leading 1 is a fresh target, not reused as program data. Spectral-tail,
DME and spectral-gate errors each total <=epsilon/32. Growth instruments
number at most V*L_g, requiring half-diamond error <=epsilon/(32 V L_g)
each. Controlled original U(g) calls number at most R*W, requiring error
<=epsilon/(32 R W) each. Register-SWAP count is at most 2R V L_g, before
charging their q-qubit implementation cost. Uniform-grid arithmetic and
the public receiver/address operations are included in the reserved budget.

Amplification costs <=epsilon/8; the eight other categories (grid, fetch,
growth stopping, spectral tails, DME, spectral gates, growth gates, U gates)
cost <=epsilon/32 each. Reserve epsilon/2 for the remaining Rees/public
operations. Total <=7epsilon/8, leaving epsilon/8 slack. Source impurities,
if present, need an ADDITIONAL raw-copy telescoping budget; the theorem as
stated supplies exact IID copies. Do not divide errors by rare branch mass.

The planner is deliberately loose. It certifies polynomial dependence,
not practical feasibility or optimal sample complexity. It executes none
of the spectral measurements, quantum growth protocol, or Rees receiver.

## 6. Adversarial Tests And What Remains Open

- If delta is false, coarsening CAN enlarge the stabilizer. A tiny unequal
  pair inside one bin exchanged by a public involution is a counterexample.
  The promise is never certified by the rounding code.
- If the rank cap is false, discarded mass need not be small. Many tiny
  weights can contain the relevant symmetry information. Polynomial rank
  remains substantive and the previous Omega(rank) copy obstruction stands.
- Coarsening may merge unequal eigenvalues; the global-gap proof, not a
  claim that those values are truly equal, is what preserves H.
- A boundary eigenvalue requires the bad-grid budget. A deterministic grid
  chosen without the margin argument is not covered by the QPE analysis.
- Failure correction is required even for nonflat sources. Rank discovery
  has a bounded error; it is not a finite-shot certificate of exact rank.
- The whole-support wedge and a chosen eigenbasis both solve the wrong
  task. Separate bin wedges preserve internal rotations without forgetting
  differences between bins.
- Generic mixed StateHSP hardness is not contradicted: no polynomial rank
  bound for those hard inputs was supplied. The group/controlled-action
  model and global promise also remain explicit. In addition, the cited
  Section 5.3 uses exponentially close states as APPROXIMATE symmetries.
  Our task concerns an EXACT subgroup with a uniform gap outside it; these
  contracts are not interchangeable. No general mixed-state isomorphism
  algorithm or QSZK-to-BQP collapse is claimed.
- Explicit density tables, low-width tensor networks, stabilizer descriptions
  and exposed preparation circuits retain their classical baselines. A
  quantum-copy input theorem is not a Shor-like classical-input separation.

This is a constructive removal of spectral advice from the same mixed
conjugation source, not a new natural hard application. Next consequential
work is independent scrutiny of this assembled result and a genuine
application/prior-art comparison. Do not launch larger planted spectra or
reinterpret passing controls as an efficient executed state learner.

## Literature And Verification Scope

Known primitives: [Kimmel et al., Appendix C](https://arxiv.org/html/1608.00281#A3)
for controlled copy-based evolution; [Bene Watts et al., Algorithms 1-2 and
Theorems 3,5](https://arxiv.org/html/2610.06737v1) for corrected streaming
antisymmetrization of nonflat states. The latter already handles unknown
support and unknown rank in Algorithm 2; even the growth probability used
here appears in its proof. Our capped stopping schedule is not claimed as
a new primitive. The new local argument is
the gap-preserving coarsening and its composition with the existing Rees
source, with ranks discovered and all failures paid. Novelty is unverified.
[Gheorghiu et al., Section 5.3](https://arxiv.org/html/2605.12615v2#S5.SS3)
is the relevant generic mixed-StateHSP hardness comparison, not a theorem
under our low-rank promise.

The implementation contains exact rational spectrum/grid/resource checks,
finite projector/determinant controls, and literal corrected-growth channel
checks imported from the already tested primitive. Spectra/frames supplied
to controls are diagnostics only, not inputs to the proposed algorithm.
All files remain outside the moving checkout. No central admission follows.
