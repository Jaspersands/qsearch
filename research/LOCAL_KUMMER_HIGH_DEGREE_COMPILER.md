# Native dyadic ONE-HALF: high-degree divisor compiler

2026-11-13. Selected constructive question, OPEN. Start STATE/TRAPS; selection
compares three independent endpoints in audits/selection/2026-11-12/
post-conductivity-native-selection.md. Prior-work/baseline outputs are in
selection/2026-11-13/high_degree_half_*.txt. Actual Stoll Prop5.1/proof and
Khuri--Makdisi selected primary text were read; excerpts/hashes in
api_inputs/2026-11-13-dyadic-high-degree/primary-excerpts.md. No new quantum
implementation or generic precision infrastructure.

## Native problem, mechanism and resources

Input: monic squarefree f in Z[x], degree2g+1, coefficient bit sizeB, p=2,
with arbitrary bad reduction. Output a basis of the COMPLETE local Kummer
image J(Q2)/2J(Q2) in computed local squareclass coordinates, bounded erroreta.
Target BITpoly(g,B,log1/eta); no supplied local model/generators, exact-zero
oracle, conditioning bound or field closure. This is useful arithmetic descent
data and a specific blocker for the proposed global two-Selmer dimension
composition; it does not by itself pay the other primes/global interfaces.
No established asymptotic advantage over the strongest classical algorithms.
A successful local operation would itself be CLASSICAL; the global quantum
proposal uses known global arithmetic primitives under its retained promises.

Mechanism: retain a bounded-degree closed/signed divisor; add the explicit
actual-point perturbation h+2sigma(z), U subset E=2L, then use one fraction-free
RR or projective divisor computation to obtain an admissible half modulo E.
Stoll's exact-field Prop5.1 permits degree(a)<=2g+1; degree-g canonical
reduction need not precede every operation. High degree/nonspeciality is a
possible algebraic interface, not a finite-precision theorem. The explicit
seed, polynomial saturation countkappa, sigma finite-grid sampler and branch-
resultant repair are proved in the three prior LOCAL_* notes supplied to APIs.

Strongest baseline: Stoll classical congruence/gcd/CRT half from one square
root in Q2[x]/f, with O(g)-size equations and no exponential sign enumeration.
Khuri--Makdisi supplies field-operation divisor arithmetic, not an arbitrary
bad-reduction dyadic BIT bound. Known good-reduction/prime-to-p interfaces
cannot silently pay p=2 halving. Native supplied geometry/precision stays absent.

Proof obligations: materialize an actual class with paid precision; find a
usable RR/normalization chart; compute square roots and minimal-degree Stoll
kernel with certified rank; pay BOTH nonzero Smith losses K_M and augmented
monic loss K_B (schedule includes K_M+2K_B); certify 2q-h in ORIGINAL E;
maintain polynomial cost over all kappa steps. A bound S_next=poly(S_previous)
can exponentiate under iteration. Need a uniform reset or additive whole-loop
loss. Exact algebraic validity, high degree, primitive projective normalization,
and passing finite controls separately establish none of these precision gates.

Cheapest falsifiers: native translated-coset minor content with superpolynomial
loss; actual degeneration despite bounded input/output support; incorrect
rank/monic normalization under finite precision; representation requiring
exponential field/sign/grid enumeration; or a recurrence exceeding polynomial
total precision. An arbitrary ill-conditioned matrix is not a native example.

## Parallel obligations, not agreement votes

Six explicit-context jobs: nonspecial RR compiler; projective half certificate;
uniform translation reset; source/high-degree gate check; native-content attack;
whole-loop invariant. Exact prompts/models/ceilings/sessions in the dispatch.
Three OpenAI/max plus three Claude calls have local ceilings32USD total, not
actual spend. No API response is a theorem before material claims are checked.

## Parent's new coordinate-tail route (UNPROVED)

The proof-only Abel trace cover of LOCAL_HALVING_SATURATION has at most
2^poly(g,B) analytic charts, each pullback Haar density <=1 after paid scaling.
For generic P, its unique reduced degree-g divisor lies in one such chart.
Try bounding the GLOBAL Haar mass of reduced-coordinate pole loss >=K by
2^poly(g,B) * 2^(-K/poly(g)). Infinity w controls x poles. Interpolation for b
introduces x_i-x_j denominators; their collision tubes need an actual estimate,
including DEPENDENT conjugates within the SAME closed point. Distinct independent
support variables alone do not prove it. Ramification, trace bases and all
chart scaling are charged to g and v2(disc f), never enumerated algorithmically.

If established for coordinate loss on all G, then division by
mu(U)=2^(-gR-H) gives a uniform conditional tail on EVERY h+U, independent
of incoming coordinate height. The same would apply to every shifted half
q+sigma(z); a proof-only union bound over rational two-torsion can cost O(g)
additional digits without enumeration. This avoids the earlier invalid tail
for successful halving on all G (outside2G a half does not exist).

Even that coordinate theorem would not yet bound Stoll matrix losses, select
constructively a good RR chart, or transfer Haar probability to the exact
finite integer sigma grid. Local stability at a paid depth is necessary; mere
E-coset preservation is too weak. Two narrow independent internal reviews
attack the coordinate-tail and matrix-conditioning implications separately.
Next experiment is those explicit proofs/native counterexamples and checking
the six paid reports. No further fixture or sweep until a falsifier is fixed.

## New mixed-resultant pencil proof proposal

The matrix audit now identifies a specific mixed resultant between input a
and half supportW. Separate coordinate tails do not automatically control it.
Parent proposes the already permitted SAME-CLASS pencil A_u=c-2ub-u²a:
its mixed resultant has coefficient content <=g+vRes(W,f)/2, by Gauss norms
and b²+ac=f at each Wroot. The discriminant's top ucoefficient is conjectured
+/- (2g+1-2e)^(2g+1-2e) Disc(a), at degree4g. These exact identities, paid
scaling and exponential one-variable sublevel estimates would permit a union
bound over all rational halves WITHOUT enumeration. A new64K Claude proof
attack is dispatched; full concrete proposal in mixed-pencil-proposal.md.
This is a new operation/lemma, not a retry of any empty task. Until checked,
these claims are proposals and do not close Stoll conditioning or ONE-HALF.

## Coordinate Haar reset: parent-checked theorem

The full283line independent proof in audits/reviews/2026-11-13-kummer-
coordinate-haar-tail.md has been read and checked. For D=v2disc f,
Nc=4D+12, M=2ceil(log2g)+4, a_free=3D+10, Delta=g(1+ceil log2g), set

 A_tail=3g+gM+2gNc+a_free+Delta+3+2ceil(log2g), c_g=6g-3.

For EVERY native f and integer s>=0,
mu_omega{beta_coord>c_g*s}<=2^(A_tail-s). This is about the ACTUAL generic
reduced Mumford coefficients on allJ(Q2), not existence of a favorable chart.
Dependent same-closed-point conjugates are paid by the embedding-matrix
row-difference lemma and field discriminant <=Delta, not assumed independent.
Infinity x=w^-2 is only true up to a unit; the proof uses exact valuations.
The exceptional nongeneric divisor locus has Haar measurezero, not a finite-
grid exclusion by fiat. No local field/chart is enumerated computationally.

Divide by mu(U)=2^(-gR-H) for every h+U; s=A_tail+gR+H+k gives failure<=2^-k.
For h+2U addg. This closes the coordinate-only HAAR reset, independently of
incoming height. It does not yet transfer to finite sigma grids, produce the
pair, or bound any actual halving matrix. The new finite-grid API proof is
active with64K output limit and only the needed context/primary excerpts.

Parent branch extension (explicit derivation, under further audit): add the
events v2(y_i)>n*s, n=2g+1. On an integral x-free chart, monicity of f and
root balls give mass <=n*2^(a_free-2s); on a y-free chart <=2^(a_free-ns);
infinity y has negative valuation. After the <=g supports and same chart
cover, A_good=A_tail+1 safely pays the combined coordinate/collision/branch
events. On this good set vDisc(a)<=2g(g-1)s and vRes(a,f)<=2gns. The same
holds for each half's supportW, and |vRes(W,R_half)|<=gns. A proof-only
union bound over <=4^g halves costs O(g) extra s, not enumeration. This is
a new branch-safe Haar claim, not yet a finite sampler or full algorithm.

## Three completed OpenAI reports: individual parent dispositions

All408/541/328line reports fully read; the following deductions were checked
independently, not accepted from the report labels.

Nonspecial RR compiler: ACCEPT exact graph-ideal product in R/(A), known
rank2m-sum e_i, collision-safe multiplication matrices, high-degree RRkernel
of dimensiong+2, and generic section/norm extraction of a degree2g+1 input.
Minimum-valuation pivots normalize a lattice but do not themselves expose it
at bounded precision. The integral near-colliding elliptic points example
has raw evaluation minor lossM-1 at fixedcurve; its divided-difference repair
is explicit. It is not a selectable-representative or loop counterfamily.
The finite acceptance certificate from augmented B and Res(w,u) is exact
provided actual root/point data; all conditioning remained unpaid in thatreport.

Uniform-reset report: ACCEPT the specific primitive RR evaluation-block lemma.
After t^N pole clearing, the Hasse-jet basis is triangularunit mod4; primitive
section wedges retain a low jet of valuation<=R' rN. Restricted-series tail
and elementary polynomial sublevel bound pay K_RR=(R+n_s+12r)rN+2r.
The polynomial-bit finite grid succeeds with probability>=1/2. This requires
an ALREADY PAID primitive section lattice and simple independent evaluations;
it does not apply by name to confluent/quotient/Stoll matrices. The genusone
branch-torsion example has augmented determinant valuationR+5 after row scaling;
parent checked the tangent identity and first derivative algebraically. It is
one native control, not an all-genus proof or a new numerical experiment.

Projective-half report: ACCEPT the exact ideal-class bypass. For ANY nonzero
bounded Stoll vector, Phi=uy-vd and K=(aw,w(y-b),Phi). With A=(a,y-b),
beta=Phi/w and beta*barbeta=epsilon*a, (beta)*bar(A+(beta))=barA*(A+(beta));
therefore2c(K)=c(A). Polynomial common factors are principal. Algebraic size
is O(g), without a minimal w or a support-field compositum. But K's raw
coefficients are NOT a stable finite chart. Parent checked the f=x³-x family:
valid triples tend to(x,x,x), K_eta representsP_eta->T=(0,0), whileK0 is
principal. The Kummer label jumps from(-1,-1,1) totrivial. This refutes only
that raw-chart interpretation. Also f=x5+x+1 yields a nonminimalw=x(x-1)
requiringr(1)²=3, so w alone cannot name a half. No full-HALF claim follows.

## Generic Stoll matrix conditioning and pencil: parent-checked bridge

Full345line review audits/reviews/2026-11-13-stoll-geometric-smith-bridge.md
was read and every factorization/valuation step checked. For a squarefree
coprimef input and degree-g squarefree half[W,R] disjoint from input,

 2v(det B_g)=2vRes(U,W)-vRes(a,U)+vRes(f,a)-2vRes(W,R).

The proof evaluates the polar norm map by CRT and confluent interpolation;
the apparent RR determinant cancels to Res(U,V), with only UNIT leading
padding factors. There is no hidden powerof2. Gauss valuation of V²-fU²
is exactly2min(v_GU,v_GV), since odd-degree monic f mod2 is not a rational
square. Thus U,V coefficient poles are paid from a,W. An explicit Bezout
identity U(4R²Z-C²U)=-4epsilon*aR² modW pays the remaining inverse using
mixed Res(a,W). The review gives explicit polynomialD_B,S_M,K_B bounds
for augmentedB and ALL testedM_k, including rank discovery and normalization.
This is conditional on the named good coordinate/branch/separation event,
not a generic conditioning assertion.

The parent's same-class pencil PENCIL lemma is now CHECKED, including the
full completed Claude report. A_u=c-2ub-u²a0, B_u=-b0-u a0 preservesclass,
with monicdegree2g+1-e. Mixed resultant content<=g+vRes(W,f)/2; exact
Disc(A_u) topcoefficient atdegree4g is
(-1)^(N(N-1)/2) N^N Disc(a0), N=2g+1-2e odd. Monic finite and large
Puiseux root groups prove this all-g identity; no finite-size inference.
Integral scaling includes n*S_W+g*S_A for mixed resultants, not just A.
Univariate exponential root-ball tails pay ALL <=4^g rational halves with
O(g+log(g/delta)) samplingbits (or the conservative larger integral capgrid).
No half/support-field enumeration. Visible branch/discriminant checks and
later B determinant certify acceptance; unobservable mixed bounds are in
probability only. The set of halves is fixed BEFOREu, so no branch circularity.
Derivative fallback for Weierstrass halves is NOT used. Provider Fable declined
the separate finite-grid request (empty/refusal,USD0.133840), no result/retry.

These lemmas remove the MIXED-resultant and generic Stoll Smith blockers,
provided actual bounded input/half charts have been reached. Full ONE-HALF is
still open. Active new tasks target ideal-product materialization and the
low-degree RR cokernel; internal work targets finite sigma-grid stability.

## Finite sigma-grid good charts: parent-checked theorem

The full299line review audits/reviews/2026-11-13-kummer-finite-grid-stability.md
was read and checked. Set n=2g+1, A_good=A_tail+1 and

 s=A_good+gR+H_seed+2g+1+k,
 A=4ns+4,
 K=g(A+1)+s*g(g-1)+gns+ceil(Delta_*/2), Q=2K+1,
 m_grid=max(0,Q-R).

For EVERY actual h in2J(Q2), exact uniform z0 in{0,...,2^m_grid-1}^g makes
h+2sigma(z0) AND EVERY rational half q+sigma(z0) have degreeg, distinct finite
x, v(x)>=-2s, -ns<=v(y)<=ns, and v(x_i-x_j)<=2s, with failure<=2^-k.
This is uniform in h and costs polynomial samplingbits; no field/half/grid
enumeration. The theorem establishes an actual finite source, not only Haar
existence. It still does NOT compute the canonical Mumford pair.

The paid domain proof uses F(z)=(f(x+2^A z)-y²)/y² and the smooth etale chart
v+2v²=F(z)/8, y_new=y(1+4v). Weil restriction along OE/Z2 is smooth even
for ramifiedfields. The generic trace-Abel map extends by Neron mapping;
parameters congruentmod4 lie in ACTUAL K2. No model or differential basis is
computed. Pullback differential coefficients and every integration denominator
are bounded explicitly. Its derivative is the scaled Vandermonde/embedding
matrix divided by prod2y; inverse loss<=K. Hensel gives the logball2^Q Z2g
inside the actual chart. Hence this subgroup preserves the SAME good caps.
Coupling Haarz with its integerresidue z0 changes sigma by2^m_grid U, so
finite-grid success follows without claiming finite samples are Haar points.

Combined with the checked pencil/Smith theorem this pays the probabilistic
and generic-matrix conditioning interfaces. Remaining critical operation is
constructive materialization from the maintained signed divisor. An independent
product-ideal argument now bounds singularity defects by4disc f; highdegree
RR unit-surjectivity is under full audit. The LOWdegree RR cokernel at m+g
is separate: primitive-kernel norm identity bounds top normalization via
outputa, but does not alone bound all nonzero Smith losses. Two paid tasks
and two internal derivations focus on those exact operations. Full HALF OPEN.

## Native canonical materialization: parent-checked theorem

Full503line review dyadic-ideal-saturation-bound.md was read and checked,
including the lowdegree section6; a second independent negative audit agrees.
The completed native-ideal-content OpenAI report was fully read too. Its
sharper integral trace-ideal identity uses2disc(f) rather than4disc(f), giving
per-stage Smith exponent<=D+1. The conservative independentD+2 bound remains
valid. The exact f=x³+1 opposite-sheet example has product torsion2 and
minorloss1 atD0, refuting flat-products inference but matching the bound.
An elementary pole-semigroup argument independently pays highdegreeRR unit
surjectivity. The general nonintegral bounds are paid, though the selected
loop needs only reduced inputblocks of degree<=g.

Most importantly, canonical materialization now has a direct construction.
Let m>=g be total signed-sum degree after converting negative blocks by
hyperelliptic conjugation; append sigma points first. Choose weighted scaling
L=max(S_input,S_good_output). ALL input reduced blocks and the unknown good
output pair become integral on the monic odddegree scaled curve. Its discriminant
inflates by2L(2g+1)2g, still polynomial. Saturate the actual graph-ideal products
in R/(A) using the proved rank/Smith caps, with no support-separation assumption.

At N=m+g, a primitive RRkernel section F=p+qY has
NormF=epsilon alpha² A a_out, epsilon=(-1)^N. Since odd-degree f mod2 cannot
be a rational square, NormF is primitive; A and truea_out are monicintegral,
so alpha is UNIT. Normalize it to1. The proof-only section
G_true=F(Y+b_out)/a_out is integral by monicdivision and belongs to the same
input ideal even when supports overlap. Its topweightN+1 is1 and
Det(F,G_true)=epsilon A. Thus F,G_true generate the saturated input ideal;
opposite leading parities give a monic weighted reductionbasis. The m
monomials of weight<N are an integral quotient basis. BOTH lowdegreeRR
restriction maps atN andN+1 are unit-surjective on the good-output event.

Compute F and G from these two finite matrices, requiring visible unit ranks
and top coefficients; otherwise ABORT this sample. No unknown output is used.
For G=r+sY, G=G_true+lambda F with integral lambda. Recover

 a_out=NormF/(epsilon A),
 b_out=rem_aout[(p*r-f_scaled*q*s)/(epsilon A)].

These are ONLY monic polynomial divisions. No q inverse, support splitting,
ideal-degree guess or uncharged chart is needed, includingq0/repeated/overlapping
input support. Successful unit tests are sound even outside the probability
event; the event pays their success. Exact arithmetic DAG/pivot certificates
name actual points, not approximate-equation witnesses. Rescaling back loses
at most(2g+1)L digits. All dimensions/losses are polynomial in g,m,D,L.

This closes the constructive reduced-divisor materialization gate PROVIDED
its actual input DAG can be refined at the requested cost. Together with the
finitegrid and Stoll/pencil proofs, a complete dyadic local-image algorithm
is now a plausible written composition. Remaining audit: native local-field/
squareclass setup, one chosen square root without sign enumeration, additive
precision across ALL DAG steps, bounded-error stopping and exact outputlabels.
No full local-image/global-Selmer admission before that composition is checked.

Terminal ten-job checkpoint: five completed, four emptytruncated, one empty
refusal. Round estimates15.367048USD (Anth6.568088/OpenAI8.798960), cumulative
165.246856USD across141records (Anth118.367096/OpenAI46.879760). Two oldUNKNOWN
bills excluded, none new. Frozen93hashes: audits/controls/dyadic_compiler_round/.
The48USD local ceiling was not spending; estimates are not invoices/balances.
No empty or refused request was retried. The64K lowRR empty report has no
findings; the independent mathematical materializer proof above is separate.

## Whole composition dispatched (2026-11-13)

The actual end-to-end candidate is now written in
LOCAL_KUMMER_NATIVE_END_TO_END.md. Three distinct paid attacks concern the
additive precision DAG, an explicit native unit-filtration square-root backend,
and the exact Stoll root-to-half acceptance interface. The previous ten jobs
are terminal; no empty/refused job was retried. Selected contexts and13USD
local ceilings (not spending) are in the new dyadic-composition dispatch.json.
The independent217line reduced-rr-unit-basis review has also been fully read
and checked: its elementary weighted basis agrees with the already proved
materializer, including overlapping supports and q=0. No new whole-algorithm
admission follows from this corroboration.

## Exact acceptance falsifier and finite stopping (2026-11-13)

The finite quotient stage is now fully checked: immutable triangular relations
and labelkernel modulo relation rows give exact index2 enlargements and
complete-image stopping. Use computable K_index, not unknown kappa, in clocks.
See full260line dyadic-finite-group-stopping review and revised end-to-end note.

Paid Stoll review found a missing visible extraction-inverse guard. Parent
constructed and Sage-verified a NATIVE genus2 example, with actual same-class
pencil draw u=1: f=1+x(x-1)(x-2)(x-3)^2, A=x(x-1)(x-2), B=-x^2+3x-1,
U=V=x,W=x(x-3), s=(x-3)^(-1)modf. Its reduced source is
[a0,b0]=[x^2-7x+12,4x-11]. Disc(f)=2297,Disc(A)=4,Res(A,f)=1,
Det(augmented Stoll B)=1, but Res(U,W)=0 and gcd(U,W)=x.
The exact half is[W,-1], so this refutes ONLY determinant-only simpleinverse
extraction, not Stoll's general gcd formula or the guarded algorithm. Add
visible nonzero Res(U,W), capped by the proved mixed-resultant identity,
BEFORE the inverse; abort otherwise. Source signs stay exact DAG identities.
The review's alternative Res(W,fA) test is sufficient but not asserted equivalent.
Artifact: audits/controls/dyadic_extraction_guard/{counterexample.py,counterexample.json}.
The first related example had a rational pencil scalar1/3; it was strengthened
to the actual integer finite-grid draw1 and rerun. This was not a broad sweep.

The paid unit-filtration report's finite-group algebra is checked; its source
objections require the full OM algorithm/proof, not its short packet. Root
has now read Prop3.8/Cor3.10, Montes actual INPUT/OUTPUT and Theorem5.18:
faithfulness/condition12 are output guarantees, not advice. The full local
Okutsu-basis proposition evaluates numerators at the actual selected factor;
no approximate-root identification is required. Detailed backend review is
still being finalized; no Round2 theorem recalled from memory is imported.
