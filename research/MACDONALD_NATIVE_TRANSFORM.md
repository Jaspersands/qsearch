# Native Macdonald transform at mesoscopic deformation

## Selection and exact contract

After starting from STATE/TRAPS, corpus been-tried and baselines were run
for Macdonald/Jack eigenbasis transforms (saved /tmp/qsearch_macdonald_*).
No exact catalog baseline matched; that is not absence evidence. Actual
primary2610.12326v1, Sections2-4 through Cor4.9, and1411.1315v3 definitions
were then read. The October2026 paper supplies a full Lax spectral theorem
AND an all-degree creation identity, making a complete q-deformed transform
plausible. This beats another local Selmer arithmetic subclass (general
classical comparator still open) or conductivity-window barrier (no full
joint-poly candidate) for current constructive expected value. It does not
supersede the independent BO work-law classical question. No novelty claim.

Input: numerical D>=1, explicit partition lambda of D or arbitrary supplied
shape-label superposition (its loading charged), integer accuracy b. Fix
N=D+1, t=D/(D+1), q=t^3, for ALL degree stages in this D-instance; do not
change q,t as degree decreases. Hall occupation metric is
 <p_mu,p_nu>=delta_mu,nu z_mu prod_k r_k^m_k, r_k=(1-q^k)/(1-t^k)
 =1+t^k+t^(2k) in[1,3]. Target full clean transform
 |lambda>|0> -> |Jhat_lambda(q,t)>|0>
in normalized power-sum occupation coordinates, with restricted operator
error<=2^-b. The corresponding classical sample has probability
 theta_lambda,mu^2 z_mu prod r_k^m_k/H_lambda.
No coefficient table, state source, Lax oracle, spectral basis or hidden
advice is supplied. Candidate resource poly(D,b); strongest unrestricted
baseline is explicit symmetric-function expansion on p(D)=exp(O(sqrtD))
partitions. No established asymptotic advantage: a polynomial classical
sampler may exist. A full transform is useful for native discrete-BO/Macdonald
spectral dynamics, not automatically a physical position wavefunction.

## Actual source facts and specialization obligation

Use w=z^-1, auxiliary norm ||w^ell p_mu||^2=q^ell||p_mu||^2. Full Lax
L=Qcal^dagger D_(t/q) Qcal, Qcal=pi_nonpositive Q(z),
Q(z)=exp sum_(k>=1)(1-t^k)p_k z^k/k. Source Eq8/Props3.11-3.13:
L Psi_(lambda,s)=[s]Psi, pi0Psi=J_lambda, and ||Psi||²=H_lambda/tau.
Contents [s]=t^i q^-j=t^(i-3j) at row i,column j. The source is initially
generic q,t. At q=t^3, globally coincident contents and zero varpi_lambda
MUST be handled using regular un-hatted cyclic projectors; do not use a
hatted basis with zero principal specialization. Within each partition,
addable and shifted-removable corner contents strictly interlace.

The row Q: w Lambda[w] -> Lambda extracts pi0 Q(z). Source Lemma4.7(ii)
and Proposition4.8 give Q w Psi_(lambda,s)=q^-j J_(lambda+s).
The shift I:w-polynomials degree n-1 -> positive-marker degree n is
I(f)=w f/sqrtq, an isometry. Hence A=Q I and
A Psi_(lambda,s)=q^(-j-1/2) J_(lambda+s), with POSITIVE scalar.
From the full block form, AA^dagger=Q Q^dagger =T2-I on Lambda_n.
Source product resolvent gives eigenvalue
 chi_lambda=(1-t)(q^-1-1) sum_boxes [box].
Parent predicts chi=Theta(n/N²) uniformly n<=D, so its inverse square root
is polynomially conditioned. This prediction and all scalars need proof.

Let V=A^dagger(AA^dagger)^(-1/2). Then on Jhat_mu it should produce
normalized Lax corner vectors with positive removal weights
 p_(mu,r)=q^(-2j(r)-1) tau_(mu-r,r) H_mu/(chi_mu H_(mu-r)).
The probabilities and hook products have polynomial-bit rational formulas.
A shape-side C prepares these weights and removes r. A Fock-side B applies
V, coherently resolves [r], then the principal half-phase of two reflections
to send the Lax vector to its parent with positive phase. If fully paid,
B_down^dagger C_down erases the entire common path, as in the closed Jack
construction. Need uniform inverse-poly tau and paid content resolution.
Expected gap: contents lie in a fixed compact positive interval, distinct
values t^k for integer k in[-3D,D] separated by Omega(1/N). Approximate QPE
must recover k CLEANLY; no free exact irrational-eigenvalue label.

## Parent native-access proposal, unreviewed

Qcal=exp(C), because every monomial lowers the marker and truncation is
monotone. On normalized occupation/marker coordinates,
 C=sum_k w_k a_k^dagger T_(-k),
 w_k=sqrt[(1-t^k)(1-q^k)/(k q^k)].
For k<=D, w_k<=16 sqrt(k)/N. Define gamma_k=N w_k/sqrtk<=16.
A CONSTANT-normalization block for C^dagger is plausible:
prepare k with amplitude sqrt(k m_k/D), leaving leftover marker mass as
failure; multiply by gamma_k/16 using a known rotation; remove the boson,
shift marker up by k, retain k; project k onto a uniform power-of-two
M-label state with D<=M<2D. The top block is
 C^dagger * N/[16 sqrt(D M)].
Every arithmetic operation must be reversible, pair labels kept and erased
correctly; top projection is a block encoding, NOT free postselection.
Normalization<=32 is independent of D. This avoids an exponential
exp(poly(D)) Taylor normalization from a crude sparse-oracle bound.
Taylor LCU of exp(C) at this constant normalization uses degree poly(b),
constant total coefficient normalization (possibly huge), fresh signals and
no expanded word list. Qcal^dagger D_(t/q) Qcal then gives a native constant-
normalization block of L; D_(t/q) has bounded eigenvalues since ell<=D.
The Q row and A inherit constant-normalization blocks by projecting marker.

V must be compiled without an unknown lambda normalization or preparation
oracle. A generic rectangular polar compiler can use the binomial series
for (AA^dagger)^-1/2 on its inverse-poly singular interval. Crucially,
I-B^dagger B for a contraction B should be block encoded as
P U^dagger (I-P) U P using a failure-projector block and SAME inverse banks,
not as a two-term LCU whose norm2 would explode when raised to powers.
Known-normalization oblivious amplification then produces a near-isometry.
All retained work, actual inverses, controls and finite bits remain charged.

## Classical attacks before any quantum implementation

Rows and columns are exact polynomial classical controls. Orthogonality and
triangularity show the single-row polynomial is proportional to degreeD of
exp sum_k p_k/(k r_k); the single-column is proportional to e_D. Thus their
occupation laws are weighted-cycle measures prod w_k^m_k/z_mu, with
w_k=1/r_k for rows and w_k=r_k for columns. Dynamic programming
Z0=1, Z_n=(1/n)sum_(k=1)^n w_k Z_(n-k), followed by size-biased cycle
selection k with probability w_k Z_(n-k)/(n Z_n), samples the exact law.
All rational coefficient bit lengths and finite-bit TV approximation are
polynomial. This is a direct deduction, no hardness inference.

Actual Diaconis--Ram1007.4779 Eqs1.1-1.4 specifies the inverse-Hall-weight
stationary law, hence the ROW control, not arbitrary squared eigenfunctions.
Its q,t>1 domain can be reached by reciprocal parameters: on fixed degree,
Hall weight changes by the common factor(t/q)^D, leaving the Born law and
orthogonal polynomials unchanged. Actual OConnell--Pei1212.6716v2 Theorem2,
Eq11 and stochastic Eq13 specify t=0 random-word/tableau laws. They do NOT
by themselves give this fixed-labelled q=t^3 occupation law. Parent checked
actual statements; no claim to have ruled out other Macdonald-process routes.

Falsifiers: source poles at q=t^3; incorrect creation scalar/chi; exponentially
small transition overlap; constant-normalization C block fails; QPE label
workspace cannot be cleanly erased; generic polar cost hides exponential
normalization; positive classical representation gives unrestricted sampler.
No quantum implementation or finite sweep is authorized by this candidate.
Next decisive work: native access/polar proof, specialized branching proof,
and a constructive strongest-classical attack on this exact output law.


## Parent hard deductions after dispatch

The following algebra is now established independently of the pending
native circuit reports. Independent helper also verified the specialization
argument; full algorithm remains conditional on native access/composition.

1. Specialization: use unhatted cyclic vectors
Psi_(lambda,s)=tau_s^-1 prod_(a!=s)(L-[a])/([s]-[a]) J_lambda.
For 0<q,t<1, within each diagram addable/shifted-removable contents strictly
interlace; all these denominators and tau are nonzero. Hook norms are
positive, L entries and J are regular. Generic source identities therefore
extend continuously to q=t^3. Orthogonality and positive H/tau imply this
remains a basis even with global eigenvalue coincidences. Proposition4.8
has only same-diagram addable versus outer-corner denominators after using
Lemma4.7's unhatted phi. It too is regular. Zero varpi is never divided by.
Thus A Psi=q^(-j-1/2)J_successor with positive scalar is retained exactly.

2. chi and tau: source top-left L block is I, so pi0 L² pi0=I+QQdag.
Expanding T_lambda=1+S_lambda/(u-1) to order u^-2 gives
chi=(1-t)(q^-1-1)sum_boxes[box]. For degree n>=1, global N=D+1,

 3n/(4N²) <=chi<=300n/N².

Indeed [box] in[1/4,e^3] with e^3<21, q^-1-1>=3/N and
N(q^-1-1)<=14. For each hook exponent a and increment r>0,
(1-t^a)/(1-t^(a+r))>=a/(a+r), because (1-exp(-h x))/x decreases.
Source hook formula for tau consequently gives
 tau_Mac>=q^j tau_Jack3>=exp(-3)tau_Jack3.
For parent degree d>0, the reviewed Jack bound3/(16d) gives safe tau>=
1/(144d) (e^3<27); at d0 tau=1. No exponentially many constant factors.

3. Native coefficient bound: q^-k<27 and
(1-t^k)(1-q^k)<=3k²/N² give gamma_k=N w_k/sqrtk<9 (the brief's16 is safe).
At an intermediate degree n<=D, use denominator GLOBAL D in mode sampling.
The leftover failure probability is [D-(n-ell)]/D, not merely ell/D.
This corrects the informal phrase in the frozen brief without changing
the block formula or its normalization<=32. Keeping k makes boson deletion
and marker shift reversible; the output-label uniform overlap is a block
matrix element, not a sampled event or a probability that can be omitted.

4. Coherent noninteger content readout: [s]=t^k, -3D<=k<=D, lies in[1/4,27]
and adjacent values differ by>=1/(4N). Use U=exp(2pi i L/64), coarse QPE
with O(logN) bits and controlled times O(N). Nearest k is computed by exact
rational comparisons with t^k. A constant-error trial is repeated O(b+logD)
times coherently; majority of the recovered binary labels is correct except
exp(-Omega(repetitions)). Copy the majority to the retained label, reverse
temporary labels and ALL phase-estimation circuits. On each exact eigenvector
the full clean-vector error is at most2sqrt(p_wrong), by comparison before
uncomputation. Spectral orthogonality makes this uniform on superpositions.
Thus repetition, not inverse-accuracy single-QPE tails, pays logprecision.
Controlled simulation times O(N) must be charged; old bounded-time claim
alone is insufficient. Approximate simulations enter by clean unitary hybrid.

5. Still-open composition hazard: a Taylor block close to Qcal is not a
known GLOBAL-unitary approximation to an exact-Qcal dilation. Do not invoke
an unproved global hybrid there. Form the polar filter from the ACTUAL
contraction Btilde, with normalized failure block I-Btilde†Btilde. Compare
its logical polynomial/polar output to the ideal one using contraction
polynomial bounds or a proved singular-value stability bound. For example,
||q_K(Htilde)-q_K(H)||<=sum_k b_k k ||Htilde-H|| when both remainders are
contractions. Square internal tolerance if the final clean bound uses a
square root. Native L from the same actual Q block as Bdag D B stays
Hermitian, so its logical error can be charged by Duhamel. Actual inverse
banks and input/output sector projectors remain explicit obligations.


## Nilpotency removes the native-Q approximation blocker

C lowers the nonnegative marker by at least one. Therefore on EVERY valid
sector of total degree n<=D, C^(D+1)=0 exactly, and

 Qcal=exp(C)=sum_(k=0)^D C^k/k!.

Use the constant-normalization C block (Gamma_C<=32), D fresh power signals,
and coefficient weights32^k/(G k!), with fixed power-of-two G>exp(32).
Their sum is<1, so cancelling I/-I padding is nonnegative. Factorials and
coefficients have polynomial(D) bit length. This is an EXACT real-arithmetic
finite unitary block for Qcal/G; no infinite series, truncation error or
exponential-in-D normalization. It also supplies exact-real L and A blocks.
All coefficient rotations are still compiled at the final finite-gate
milestone, with polynomial-bit costs and clean whole-logical hybrid bounds.
Thus the earlier ACTUAL-block stability warning remains valid in general,
but can be avoided here by exact nilpotence BEFORE gate rounding. Native
polar powers still need private marker/projector signals per factor, and
rectangular OAA still distinguishes input/output sectors. Full algorithm
awaits the independent composition proof; nilpotence alone is no speedup.


## Reviewed WRITTEN complete native transform

Parent fully read and independently checked the408line composition proof
`audits/reviews/2026-11-13-macdonald-composition-independent.md`. The exact
numericalD/fixed-global-t=D/(D+1),q=t³ contract is now CLOSED as a written
poly(D,log1/epsilon) BIT/gate/workspace clean transform. Input state loading
is charged; error is uniform on arbitrary superpositions and reference.
D0 is identity. No algorithm is inferred from a finite test or report label.

Checked interfaces include positive-Gram regular continuation of J (no
unchecked integrality citation), un-hatted source specialization, complete
cyclic basis despite global degeneracy, exact positive A scalar/common
paths, chi/tau bounds, constant-normalization native C block, exact finite
nilpotent Qcal, PRIVATE marker per rectangular polar power, distinct input
and output OAA projectors, known-normalization amplification, repeated
coherent content readout with timesO(D), native Hermitian L simulation,
same-bank actual inverses, finite palette and noncircular error allocation.
G=2^48 and Gamma=8G² are huge FIXED constants; no practicality claim.
The final bottom compiler pays every real rotation with clean error and
polynomial-bit arithmetic. It never assumes arbitrary block dilations close.

Both Claude reports completed and are fully parent-read. The branching
algebra is accepted with the parent's stronger hook-ratio tau bound and
positive-Gram repair of its unchecked citation. Its claimed exact bit
exponents or O(b+logD)-only working precision are not required; retain
polynomial(D,b) precision with exact rational operand lengths charged.
The classical report has no unrestricted sampler. Parent corrected/proved
several claims in MACDONALD_CLASSICAL_BASELINES.md; independent review of
near-row sampling and elementary uniform Jack-law separation is pending.
The native OpenAI report is still advisory/in-flight, to be fully checked
when terminal, not an unpaid step in this independently checked theorem.
No implementation, novelty, classical hardness, useful/Shor-level advantage,
physical position-state, fixed-away-from-one q,t or other parameter claim.

## Terminal native API report disposition

OpenAI macdonald-native-access completed; parent read all451 LF lines.
Its explicit deletion permutation, correct low-degree failure mass, exact
nilpotent Qcal, PRIVATE-marker complement powers, rectangular OAA, repeated
coherent QPE and finite palette agree with the checked construction. Its
S=2^64/Gamma=16S^2 constants are alternatives, not imported over the existing
G=2^48 construction. It explicitly assumes algebra/spectrum/conditioning;
these are discharged separately by the parent/source and408line proof. It
does NOT itself prove full branching or a speedup. Its clean readout bound
for initially-zero labels need not replace our safe2*sqrt(p_bad) uniform
XOR-label bound. All three paid reports are terminal and parent-checked.
The272line classical independent proof is also fully parent-checked.
