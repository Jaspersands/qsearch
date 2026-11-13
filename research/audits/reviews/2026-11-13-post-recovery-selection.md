# Post-recovery selection: positive Gram-defect boson simulation

Select ONE independent constructive question: can an arbitrary-complex
partial-distinguishability Gram matrix be peeled into an EXACT positive
private-flag mixture, then sampled with an exp(O(R))*poly(input,1/epsilon)
finite-bit clock, where R is an explicitly computed spectral defect?
The concrete operations below remove signed interference truncation and
factorial subset enumeration. First check whether actual noise-simulation
literature already supplies this SAME theorem; if it does, stop rather than
rename it. No novelty, advantage or general boson-sampling claim is made.

This is a classical noisy-photonics endpoint, not an extension of the closed
folded/Kerr samplers or arithmetic/HSP compilers. Its external value is a
certifiable full-distribution simulator/benchmark for imperfect many-photon
interference, with a device-input criterion and no fitted coherence oracle.

## 1. Selected native problem and explicit operation

Input: an explicit rational-complex m-by-N isometry U, one photon in each
of N distinct input modes, and an explicit rational-complex PSD Hermitian
Gram G with G_ii=1 for a PRODUCT of PURE internal photon states. Internal
states themselves, a convenient decomposition, or hidden labels are not
supplied. Output the full collision-allowing spatial occupation vector,
within TV epsilon, with a fixed finite clock and stated failure cap.
Mixed/correlated internal inputs are excluded: a pairwise Gram matrix need
not specify their full distinguishability law. Dense input length B, N,m,
output length and precision are all charged. No heralded detection or
loss-postselection law is substituted for this N-photon law.

Compute a certified rational

    0<=d<=lambda_min(G), lambda_min(G)-d<=1/N,
    H=G-dI>=0, rho=1-d, R=N*rho.

Inertia/root isolation or exact rational LDL with dyadic bisection can pay
this scalar certificate polynomially; no eigenvector/spectral-gap oracle is
needed. R is within1 of N*(1-lambda_min(G)). Treat rho=0 separately.
The candidate useful promise is R=O(log(B+2)); the general clock may be
exponential in R. It does not classify constant-overlap photonic devices as
easy, nor evade ideal boson-sampling complexity at R~N.

**New operation to audit: positive private-flag peeling.** Every G=dI+H
has a pure-state realization

    |phi_i> = sqrt(d)|private_i> + |h_i>,
    <h_i|h_j>=H_ij,

where private_i are mutually orthogonal and orthogonal to the whole shared
space. Measuring total INTERNAL private occupations commutes with every
spatial linear-optical U. Each outcome identifies a shared subset S with
independent inclusion probability rho. Conditional on S, the other photons
are mutually distinguishable and independent of that subset; S has pure
internal Gram Gamma=H_(S,S)/rho. This gives a positive mixture, not a signed
probability approximation. The algorithm uses G,H,Gamma directly; it never
constructs an internal optical state or queries a purification.

The exact law of this decomposition is the first nonnegotiable proof gate.
It is not licensed by a small off-diagonal entry, low Gram rank, loss, or
an assertion that internal colors can all be measured independently.
Private occupations are special because they identify disjoint orthogonal
sectors; measuring arbitrary shared input colors would destroy interference.

**Second operation: exact arbitrary-Gram prefix contraction.** For s=|S|
shared photons and an ordered j-output prefix o1,...,oj, propose

    p_j(o) = (s-j)!/s! * sum_{T subset S, |T|=j} C_T(o),

where C_T is the coefficient of product_(i in T) x_i*y_i in

    product_(r=1..j) sum_(i,l in T)
       U_(o_r,i)*conj(U_(o_r,l))*Gamma_(l,i)*x_i*y_l.

This is obtained by tracing unobserved spatial outputs in the exact double-
permutation formula: unobserved bra/ket input indices must match, leaving
the same selected input subset T. The internal Gram orientation above uses
Gamma_li=<phi_l|phi_i>. Repeated OUTPUT modes are allowed. Sampling ordered
outputs and then counting multiplicities pays the Fock collision factorials.

Because each coefficient polynomial has bidegree(j,j), inclusion-exclusion
over its 2j Boolean variables extracts that coefficient in poly(j)*4^j
arithmetic. Summing over T costs at most poly(s)*5^s across all subset sizes,
not s! or m^s. Evaluate all m possible next outputs and sample by exact
rational p_j/p_(j-1). The polynomial's final coefficients are nonnegative
REAL rationals despite its complex intermediate arithmetic. Exact zero
prefixes must never be divided by. Common denominators and bit lengths
must be bounded explicitly; tiny prefix mass does not authorize inverse-
probability work or a heuristic floating cutoff.

The distinguishable N-s photons are independent categorical draws from
|U_(.,i)|^2; their occupation histogram is added to the shared histogram.
The law must retain all complex Gram cycles, including three-photon triad
phase. Replacing Gamma by entry magnitudes would invalidate the problem.

For a fixed cap, take s_max=ceil(8R+2log2(2/epsilon)) (or a tighter proved
integer bound). A Bernoulli-tail bound gives Pr(|S|>s_max)<=epsilon/2;
use a legal fallback there. Then the suggested worst-branch clock is

    exp(O(R))*poly(B,N,m,1/epsilon,log(1/eta)),

with every bit operation and random-coin cap paid. Without truncating S,
E[5^|S|]=(1+4rho)^N<=exp(4R), suggesting an exact expected-time version;
that is not automatically a worst-branch finite-clock theorem. State the
TV/abort/random-bit convention separately. For R=O(log B), the finite TV
sampler is polynomial jointly in input and inverse accuracy.

## 2. Strong classical comparison and first falsifier

Strong baselines: Clifford--Clifford exact chain-rule simulation; exact
partial-distinguishability double-permutation/subset algorithms; Renema
interference-order truncation; Moylett/Renema/Shchesnovich noisy/lossy
simulation; particle-separable/positive-state methods. Some may already
subsume this parameter or offer a stronger device regime. Compare COMPLETE
TV samplers with arbitrary complex G and joint epsilon dependence, not only
single-outcome probability estimators or average-random-U error statements.
The current proposal is a classical comparator, not quantum advantage.

Decisive first experiment only AFTER the primary-source gate: N=m=3,
rational Householder U=I-2vv^T/9 for v=(1,2,2), and two PSD Gram matrices
with diagonal1 and off-diagonal magnitude1/8, but triangle phase0 versus
pi/2. Compare every one of the ten spatial occupation probabilities from
the exact double-permutation law against the private-flag mixture and the
prefix formula. Both Grams are PSD by diagonal dominance. The different
triad phases must be retained; collision outputs and s=0 branches must
normalize. Any mismatch kills this proposed operation before a large sweep,
implementation or a complexity claim. Passing that fixed test proves no
all-N theorem; the exact expansion and bit clock still require proof.

## 3. Two independent alternatives, compared by external value

**Binary-spin recoupling compiler (not selected now).** Native input is
binary angular-momentum/anyon labels and coupling trees; output a coherent
Racah/recoupling transformation on arbitrary superpositions, with all
rotation and precision costs charged. A poly(labelbits,log1/epsilon) target
would help large-color fusion/spin simulation, rather than another scalar
special-function estimate. Classical competitors are exact recurrences,
semiclassical kernels, sparse/treewidth tensor contraction and explicit
state-vector computation. Numerical-spin polynomial cost is exponential in
this binary input. No concrete operation removing that cost is currently in
hand; a tridiagonal recurrence or coefficient oracle is not the transform.
First falsifier is a claimed uniform compiler whose actual block-size,
spacing or overlap cost remains polynomial in numerical spin. Near-caustic
and exact-zero cases must be paid. Corpus identifies old receiver/Hahn
interfaces, not a new binary-spin theorem. Fetch actual Bacon--Chuang--Harrow,
*Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms*, and the
quoted2610.03581 block-construction theorem before importing its gate clock.
No compact-Lie-HSP or general Kronecker implication is asserted.

**Native Gibbs Hamiltonian learning (not selected).** Input fresh copies
of exp(-beta H)/Z for unknown bounded local coefficients on a known graph;
output all coefficients to additive epsilon. It has clear metrology/device-
identification value, but a generic poly(n,beta,1/epsilon) copy target is
already false without an identifiability parameter. For one qubit,
H1=Z,H2=2Z have coefficient separation1 while their Gibbs trace distance is
at most exp(-2beta); tensor-product trace distance is at most r times this,
so constant-success discrimination needs r=Omega(exp(2beta)) copies.
No quantum measurement fixes that copy-model obstruction. At high temperature
or with a paid response/covariance condition, local statistical/tomographic
and convex-learning methods are strong baselines; a free inverse covariance
is not a native construction. Fetch the actual high-temperature theorem of
Haah--Kothari--Tang, *Optimal learning of quantum Hamiltonians from high-
temperature Gibbs states*, if a restricted contract is later proposed. This
is a conditioning problem with no fresh operation yet, unlike the explicit
positive peeling/prefix route above.

## 4. Retained-primary gate and precise parent fetches

Actually read local Brod--Oszmaniec
`audits/sources/2026-11-13-bosonic-selection/brod_oszmaniec.txt`:
formal Corollary1 LF654--664 is about bunched Fock inputs; Theorem3
LF713--735 is about nonuniform LOSS with O(log N) lossless modes and an
explicit TV bound. LF239--280 explains their positive-state/input argument.
These are real classical priors, but neither statement is an arbitrary
internal-Gram spectral-defect theorem. Their ordered-output marginal method
LF578--605 is relevant prior art. It must not be renamed as our invention.

The actual bibliography supplies precise missing comparators, not theorem
content to assume:

- Renema et al., PRL120,220502, DOI10.1103/PhysRevLett.120.220502,
  *Efficient algorithm for boson sampling with partially distinguishable
  photons* (Brod LF969--971).
- Moylett et al., QST5,015001, DOI10.1088/2058-9565/ab5555,
  *Classically simulating near-term partially-distinguishable and lossy
  boson sampling* (LF959--961).
- Renema--Shchesnovich--Garcia-Patron, *Classical simulability of noisy
  boson sampling*, arXiv1809.01953 (LF957--958).

Parent was sent these fetch targets during selection. Read actual model,
Gram assumptions, U-averaging, TV normalization, complete sampler and accuracy
clock before declaring a surviving question. If any already gives the same
or stronger positive arbitrary-Gram exp(O(R)) sampler, mark this candidate
superseded and select a different operation. A new name/parameter does not
make a published simulator new.

Corpus been-tried --no-refresh preceded baselines for all three precise
candidates. Returned boson-loss barrier prose is overbroad as a scientific
verdict; only its source leads were used. Baseline keyword retrieval returned
mostly irrelevant SDP/USD entries, so the explicit primary comparisons above
replace that result. No catalog miss is evidence of novelty or hardness.
No network/API/Git, archive sweep, numerical test, status edit or new paid
call was performed. All novelty/advantage/implementation gates remain false.
