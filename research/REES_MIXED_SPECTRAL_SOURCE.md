# Low-Rank Mixed Conjugation Through Spectral Flags

29 October 2026. Written source-reduction argument with finite controls and
independent automated mathematical/primary-source review. Not a formal
proof, human review, novelty certification or end-to-end quantum execution.

## 1. Result And Access Model

The [flat-state construction](REES_SUBSPACE_SYMMETRY_SOURCE.md) loses
eigenvalue information. Taking the top wedge of an arbitrary mixed state's
entire support therefore does NOT learn its conjugation stabilizer.
This note replaces that one support with a bounded spectral flag.

Proposed reduction: given fresh IID copies of an arbitrary density rho on
q qubits, a correct supplied upper bound rank(rho)<=R, a controlled LINEAR
unitary representation U_g of a finite group G, and the global promise

    H = {g: U_g rho U_g^dagger = rho},
    TD(rho,U_g rho U_g^dagger) >= delta > 0 for every g outside H,
    TD(A,B) = ||A-B||_1/2,

one can prepare approximate copies of a pure ray-symmetry source with
stabilizer EXACTLY H and overlap gap at least delta^2/8, at polynomial cost
in R,q,1/delta, the requested number of copies and inverse error. No
minimum nonzero eigenvalue, pairwise eigenvalue gap, flatness, known rank,
known eigenbasis, conjugate copies or preparation inverse is assumed.

The source is a fixed product of at most R exterior states. Its original
register count is at most min(R(R+1)/2,16R/delta). Its controlled action
costs that many original controlled-U calls. The ideal source depends on
a public random grid chosen ONCE per run, not afresh at every receiver leaf.

The reduction can feed any applicable pure-ray learner. In this repository
the nonabelian consequence remains CONDITIONAL on the proposed Rees
receiver, with its explicit Lazard-group and fixed-class restrictions.
This does not extend that receiver to arbitrary groups. It also does not
establish a hard classical-input application or efficient behavior for
exponential R or inverse delta.

## 2. Spectral Compression Without Resolving Tiny Gaps

Set w=delta/(16R), J=ceil(1/w), and choose an integer a uniformly from
0,...,M-1, where M is a power of two at least 8R/beta. Use exactly log2 M
random bits. Define

    t_j = w(1+a/M+j),  j=0,...,J-1,
    P_j = 1_[rho>=t_j],
    B = w sum_j P_j.

For every eigenvalue lambda of rho, the corresponding eigenvalue of B is

    b(lambda) = w max(0,floor(lambda/w-a/M)).

The finite upper end of the grid loses no positive contribution because
lambda<=1. Hence 0<=lambda-b(lambda)<2w for every positive eigenvalue,
and zero stays zero. Consequently, for EVERY offset, including bad ones,

    0 <= B <= rho,  e := Tr(rho-B) < 2Rw = delta/8.

Every symmetry of rho fixes each P_j. Conversely, if g fixes all P_j,
it fixes B, and the triangle inequality gives

    TD(rho,U_g rho U_g^dagger) <= Tr(rho-B) = e < delta.

The supplied GLOBAL gap forces g in H. Thus the intersection of these
projector stabilizers is H exactly. This is not a generic claim that
approximation preserves exact symmetries: the global promise is essential.
A permutation of nearly equal eigenvalues would violate that promise.

There need not be any useful uniform orbit gap for an individual P_j.
Do NOT run a separate symmetry learner on each component and assume its
gap. Instead form one joint source as below.

## 3. Product Flag, Exact Subgroup, Uniform Gap

The P_j are nested. Equal positive ranks imply identical projectors, so
after learning their ranks we can remove duplicates without learning any
basis. Retain distinct positive-rank projectors Q_l of ranks r_l. There
are at most R, with distinct decreasing integer ranks. Also

    sum_l r_l <= sum_j rank(P_j) = Tr(B)/w <= 1/w.

Let Omega_l be the normalized top wedge of range(Q_l), and set
Psi = tensor_l Omega_l. Its ray stabilizer is exactly the intersection
above. On H the phase is the product of the determinant characters on
these subspaces; ordinary vector invariance is not promised. The existing
zero-moment Rees design handles these phases for the stated group family.

Group duplicates in B= sum_l c_l Q_l, where c_l is w times their count.
Writing sigma_l=Q_l/r_l gives sum_l c_l r_l=Tr B<=1. If g is outside H,

    TD(B,U_g B U_g^dagger) >= delta-e > 7delta/8,
    TD(B,U_g B U_g^dagger)
      <= sum_l c_l r_l TD(sigma_l,U_g sigma_l U_g^dagger).

Some normalized projector therefore moves by at least 7delta/8. The
principal-angle/determinant bound in the flat-source note implies that
its wedge has overlap at most 1-(7delta/8)^2/2. The product overlap is
no larger, so the conservative joint gap delta^2/8 is valid. The component
that witnesses this may differ with g. None is given an individual gap.

## 4. A Random Margin, Not A Spectral-Gap Promise

Set Delta=w/(4M). Across all offsets and thresholds, neighboring candidate
thresholds are w/M=4Delta apart. Each nonzero eigenvalue can be within
distance STRICTLY less than Delta of a threshold for at most one offset.
Union bounding over at most R nonzero eigenvalues gives

    Pr[some threshold has spectral distance < Delta] <= R/M <= beta/8.

Zero is harmless since t_j>=w. Degeneracy only reduces the number of bad
offsets. This good-grid event is NOT a heralded certificate and is not
tested by the planner. A bad grid is charged as an error event. All
algorithms retain finite clocks even there. Tiny internal gaps and tiny
eigenvalues are allowed; the grid avoids them rather than resolving them.

## 5. Paid Coherent Threshold Access

Density-matrix exponentiation is established prior art, not our primitive.
[Kimmel et al., Appendix C](https://arxiv.org/pdf/1608.00281) supplies
controlled sample-based evolution. [Go et al., Theorem 2](https://arxiv.org/html/2412.02134v3#S4)
provides a nonasymptotic diamond-norm bound including entangled references.
Copies of |1><1| tensor rho also implement controlled evolution via the
enlarged-program construction. Negative time changes a known interaction
angle and consumes fresh copies; it is not an inverse state-preparation
oracle. Register interactions cost polynomial(q), not constant gates.

Derived threshold lemma: if dist(t,spec rho)>=Delta, coherent phase
estimation, a threshold bit and coherent uncomputation yield the complete
instrument

    M_t(X) = |1><1| tensor P_t X P_t
           + |0><0| tensor (I-P_t) X (I-P_t)

within half-diamond error eta using
O(Delta^-2 eta^-1 log^2(2/eta)) program copies, plus polynomial gate and
workspace overhead. This is a composition of known primitives, not a
single theorem claimed verbatim from those sources.

For completeness: use eigenvalue precision below Delta/3 and amplify the
coherent classification success so its wrong-bit probability is O(eta^2).
Copy ONLY the resulting bit, then uncompute every eigenvalue/work register
before measuring that bit. Eigenvalue estimates can be phase shifted away
from the 0/1 wraparound, e.g. phase-estimate exp(i*pi*(rho+I)/2), whose
eigenphases lie in [1/4,1/2]. The total absolute simulated evolution time,
including cleanup, is O(Delta^-1 log(2/eta)). Allocate simulation errors
proportionally to the absolute time of each controlled evolution; summing
their quadratic-copy bounds gives the displayed total cost.

For an exact eigenvector the ideal forward-estimation amplitudes have
wrong-bit norm O(eta). Orthogonality of different eigenspaces makes the
same isometry bound uniform over superpositions and entangled references.
This yields the complete-instrument error after uncomputation. Measuring
the detailed eigenvalue label first would instead dephase within a sector.

The inverse estimation circuit is synthesized using FRESH negative-time
simulations. It approximates the inverse IDEAL circuit, not the physical
inverse of a noisy consumed-copy channel. A complete-channel hybrid pays
for both directions. The finite reference tests explicitly distinguish
these facts and retain off-diagonal control/reference coherences.

## 6. Acquiring The Ranks Without Eigenbasis Advice

For the ideal spectrum, eigenvalue sampling on an input rho chooses each
eigenvector i with probability lambda_i, counting multiplicities. Thus

    E[1_[lambda_i>=t]/lambda_i] = rank(P_t).

An unweighted threshold frequency instead gives spectral MASS, not rank.
No uniform-eigenvector sampler is granted. Use independent phase-estimated
values Y, clipped to [0,1], precision

    h = min(Delta/2,w^2/128),  ideal tail probability kappa=w/128,
    implemented single-sample TV error zeta=w/128.

For each threshold form Z_j=1/Y if Y>=t_j, otherwise zero. It lies in
[0,1/w]. On a good phase estimate the threshold is correct and reciprocal
error is at most 2h/w^2. Tail and implementation errors add at most
(kappa+zeta)/w. The bias is therefore at most 1/32. With

    m = ceil(128*w^-2 * ceil(log2(2J/beta))),

Hoeffding and a union bound put every empirical mean within 1/8 of its
expectation, except with probability beta. Rounding to the nearest integer
recovers ALL ranks. The SAME m samples serve all J thresholds; no pairwise
eigenvalue gaps or eigenvector descriptions are needed. Reject impossible
rank sequences before further processing. Even a plausible sequence is
not a heralded correctness certificate.

Use exact rational classical threshold/reciprocal arithmetic or allocate
at most 1/32 additional absolute error in each final empirical mean. The
total remains below 1/4, so integer rounding is unchanged. Check the public
rank, monotonicity and register-count bounds even when training is wrong;
do not let a rare bad estimate remove the worst-case runtime cap.

A conservative training cost is
O(m h^-2 zeta^-1 log^2(2/kappa)) DME program copies plus m target copies.
These are fresh independent acquisitions. Systematic implementation error
is paid through the bias bound, not silently treated as random noise.

## 7. Ideal Component Preparation, Clocks And Physical Error

On a good grid with correct ranks, an ideal threshold measurement on rho
accepts with p_l=Tr(Q_l rho)>=w and returns

    rho_l = Q_l rho Q_l / p_l,
    rank(rho_l)=r_l,  lambda_min_nonzero(rho_l)>=w.

The published NONFLAT streaming algorithm of
[Bene Watts et al., Theorem 5](https://arxiv.org/html/2610.06737v1#S3)
prepares Omega_l; its known-rank stopping rule and rejected-copy handling
are used unchanged. We do not pretend rho_l is flat. Repeated source
requests use independent inputs, filters and program copies.

Let K<=R be the number of distinct flags, T the entire ideal receiver's
requested number of PRODUCT states, and b=ceil(log2(RKT/beta)). Each
rank-r_l component permits N_l=ceil(r_l/w)*b growth attempts, with one
initial filtered input, except rank one needs no growth. Its failure bound
is r_l exp(-N_l*w/r_l)<=r_l 2^-b. Summing all TK components gives <=beta.

Let F=T sum_l(N_l+1), counting initial inputs as well. Each filtered-input
request gets at most C=ceil(w^-1 ceil(log2(F/beta))) trials (at least one).
All failures consume their input and program copies. Since ideal acceptance
is >=w, the chance that any request times out is <=F exp(-wC)<=beta.
There are at most A=FC filter attempts. The first timeout aborts the WHOLE
receiver, including any already delivered states.

The finite cap calculator reports A TARGET copies, NOT total raw copies:
each of those A attempts also consumes its paid DME program. Giving each
filter complete error eta=beta/(2A) costs in total

    O(A^2 Delta^-2 beta^-1 log^2(2A/beta)) program copies.

Growth-gate synthesis gets the remaining preparation error beta/2 divided
over its capped calls. This compares the complete physical adaptive run
to the ideal one, including all rejected branches and ABORT. No normalized
postselection error is used for free. If one instead bounds a single
accepted output, a factor O(1/p_l) must explicitly be paid.

Only IDEAL rho_l have exact support/minimum-eigenvalue promises and exact
terminal wedges. Approximate physical filters can leak outside the support.
The complete-run hybrid, not an assertion of exact purity after noise,
justifies substitution into the receiver.

For total requested error epsilon, give the inherited pure-source/receiver
budget epsilon/2 and set beta=epsilon/16. Bad grid, rank estimation,
growth timeout, filter timeout and complete preparation approximation
together add at most 5beta. This is below epsilon with slack. The earlier
receiver allocation already charges controlled group-action precision.
Raw-source IID correctness remains an input promise. A noisy supplied
copy stream requires an additional separately charged model.

The full cost is polynomial in R,q,1/delta,1/epsilon and T; coefficients
and exponents are large. No resource advantage follows from that statement.
There is no factor d from maximally mixed ambient-state postselection.

## 8. Finite Controls And Falsifiers

`mixed_spectral_source.py` uses explicitly SUPPLIED rational spectra only
as a reference. Its C3 controls compare the entire-support wedge with the
joint spectral flag on nonflat states, including a 2^-80 internal gap and
a 2^-80 tail. They are not generated oracle candidates or recovered hidden
subgroups. A false-global-gap control shows rounding can otherwise invent
symmetries. Noncommuting dense-matrix controls check the joint overlap
bound with an unknown-to-the-hypothetical-learner eigenbasis.

`copy_spectral_reference.py` executes actual finite controlled partial-SWAP
dilations with fresh program states traced out. It checks control and
reference coherence, both evolution signs and noninvertibility of consumed
channels. Its exact unitary/eigenvalue comparisons are reference access,
not operations granted to the copies-only algorithm. It is NOT a complete
spectral filter, rank learner, flag factory or quantum receiver.

For its conservative half-diamond allowance 2t^2/n: the one-step controlled
dilation and ideal evolution have the same first derivative
-i[|1><1| tensor rho, X]. Each unitary-channel Taylor remainder has diamond
norm at most 2theta^2, since the Hamiltonian norm is <=1. Preparation and
partial trace are contractions, also with a reference. Their difference
is at most 4theta^2; telescope n steps with theta=t/n and divide by two.
This elementary bound is not an optimal-copy theorem or a fitted exponent.

Reject any claimed extension that supplies the spectrum to the actual
learner, reuses program copies, uses individual projector gaps, measures
spectral labels before cleanup, drops herald failures, calls approximate
filters exactly rank-preserving, or omits the DME program-copy factor.

## 9. Significance And Remaining Gates

[Holt--Subramanian Section 10.4](https://arxiv.org/html/2609.38085v2#S10.SS4)
formulates mixed-state conjugation symmetry. Their Hamiltonian route uses
normalized Frobenius separation: inserting H=rho does not automatically
preserve a dimension-independent trace-gap guarantee. The scalar-support
mixed-state task is different. The primary-source reviewer found no
checked theorem giving the entire bridge here, but did NOT certify novelty.

Replay `python qsearch.py subspace-source --mixed-spectrum --write`.
The output explicitly marks its known-spectrum controls and unimplemented
quantum steps. Do not promote a speedup or completed receiver status.

The application audit in `LOW_RANK_SYMMETRY_APPLICATION_FILTER.md` eliminates
several natural but easy families. Next decisive work is a source outside
those matched-access filters, with a proved global gap, or an independent
human/prior-art assessment of this general reduction. More budget profiles
alone would not strengthen either claim.
