# Native sparse-source damped lattice Helmholtz field sampling

13November2026. Selected after STATE/TRAPS, corpus been-tried and baseline
lookups, then actual primary2609.10282 Eq20,23-28,31,A18-A21. No close corpus
endpoint or catalog match was returned; that is NOT classical hardness.
Previous static Macdonald full-output question is parked after exact moment
classical samplers and a finite-time Poisson approximation. Do NOT extend it.
Independent comparison also considered qutrit partial-assignment gauge search
2611.01983: actual source has an easy classical XOR case and finite SAT tests,
not a newly paid general search route. General Selmer's global class/unit
bypass has no new operation; do not reopen it merely because it is open.

SINGLE scientific question: is there a completely paid quantum polynomial
algorithm for this physically motivated FULL spatial Born law, and does a
classical algorithm match it? No source normalizer, inverse, Green kernel,
annulus sampler, QRAM, eigenstate, or material oracle is supplied.

INPUT: n>=2, L=2^n; torus (Z/LZ)^2, fixed grid spacing1. Standard positive
nearest-neighbor Laplacian K=4I-Tx-Tx^-1-Ty-Ty^-1. Set eta=1/L and
A=I-K+i*eta*I (fixed squared wave number1, below the van Hove value4).
Explicit list of m DISTINCT sites x_j in the torus and nonzero rational
complex weights w_j of total bit length B; combine duplicates beforehand.
f=sum_j w_j |x_j>. Arbitrary phases/signs allowed, f!=0. Input epsilon>0.
OUTPUT: one lattice site x with TV<=epsilon from
P_f(x)=|u(x)|^2/||u||^2, u=A^-1 f.
Target BOTH total bit/gate work poly(n,m,B,1/epsilon) with a finite clock.
No general relative exponentially-small output precision is required.
The discrete Fourier symbol is lambda(k)=4-2cos(2pi*kx/L)-2cos(2pi*ky/L),
a(k)=1-lambda(k)+i/L, so |a|>=1/L. Generic QLSS pays kappa~L; explicit
full-grid FFT/solve costs L^2 poly(n,B,b). Geometric resonant prep is a
proposed route around that cost, not an admitted primitive or theorem.
We do not import the continuum-circle ring into this lattice symbol.

Expected advantage target: poly(log L) at polynomial m and fixed/error
inverse-polynomial n, versus full-grid work. A same-output sublinear
classical algorithm is the first falsifier; no classical lower bound,
novelty or speedup is asserted. State preparation only is not an advantage
for the requested classical sample. Any changed source/precision/geometry
promise must be labelled a RESTRICTED endpoint, never universal.

CHEAP parent attacks, exact but not yet an independent full proof:
1. Source-register LCU success is a Gram quadratic form. If G=A^-1 delta0,
Z0=||G||^2,Z=||sum w_j T_xj G||^2, then usual ell1-weight LCU succeeds
with Z/(||w||_1^2 Z0). It is NOT generally1/m; uncompute of the SAME
weighted source ket produces |alpha_j|^2 coefficients, not arbitrary w_j.
Use separate left/right preparations and phases if repairing that detail.
2. Matched classical mixture: if the SINGLE G spatial probability and
values are efficiently available, sample j proportional|w_j|^2 then
x from |G(x-x_j)|^2/Z0. Envelope is m*sum|w_j G(x-x_j)|^2. Rejection
success Z/(m*sum|w_j|^2*Z0). This is within a polynomial factor of LCU.
Do not grant the missing single-source sampler/evaluator or normalizers.
3. Five-source cancellation: f=(I-K)delta0 = -3delta0+delta_(1,0)
+delta_(-1,0)+delta_(0,1)+delta_(0,-1). Exactly u=delta0-i*eta*G.
FourierF=1-lambda vanishes ON the actual resonant curve. A shell with
|1-lambda|<=C/L may therefore lose almost all normalized full-field mass,
and source LCU may be exponentially small in n. Prove bounds or refute;
finite plots cannot establish asymptotics. This family is classically easy,
so it is a source-interface falsifier, not a difficult quantum application.

Resources/proof obligations: actual spectrum and lattice shell sampling,
normalization/conditioning for all allowed sources, all off-shell tails,
finite-bit trigonometry with n extra bits, coherent uncomputation, quantum
state-to-classical readout, cap success/failure and total clock. Standard
classical competitors: Fourier solve, Green superposition, sparse sampling
mixture, oscillatory quadrature/stationary phase, direct localized quotient
when f=A0 h, and exact small-grid controls. No implementation is requested.
Stop at the exact missing operation if blocked. Your report is advisory;
all material claims will be independently verified by parent.

## Dispatch and initial disposition

Six distinct paid obligations run, three each provider, request ceilings33USD
not charges: audits/api_inputs/2026-11-13-sparse-wave/dispatch.json.
Full resolvent deflation, classical cancellation-aware superposition,
single-source classical Green sampling, exact source cancellation falsifier,
discrete quantum spectral shell preparation, positive separated-source Gram
bound. No paid report is yet accepted; no quantum implementation.
Parent actual primary source includes BOTH principal-value and resonant
parts via q(k), so an initial homogeneous-only suspicion was discarded.
The unresolved claims are uniform normalized ring accuracy and source
interference/normalization. The source's numerical curves do not pay them.

The five-source identity u=delta-i*eta*G is exact for this explicitly new
finite-difference target. It is not silently attributed to the source's
continuum-circle algorithm. Standard classical Green-mixture rejection is
exact conditional on paid single-kernel access and noncancellation; neither
interface is granted. Corpus lookup of geometric Helmholtz/resonant source
returned no close endpoint and no named catalog baseline; no inference of
hardness/novelty follows. QPF actual Eq14-30 has a connected feasible
partial-assignment manifold; that alone supplies no complete-solution
success bound, and XOR Gaussian elimination is the first baseline.

## Hard deductions and first paid dispositions

Two Claude reports completed, fully parent-read and reaped: cancellation-
falsifier and positive-source-frame. Four other distinct tasks remain active.
Their results are advisory; the following algebra/counting was checked by
parent. Independent scoped proofs are being completed separately.

FIVE-SOURCE result: Z0=L^-2 sum_k (b(k)^2+L^-2)^-1, with
b=2cos(theta_x)+2cos(theta_y)-3. Elementary nearest-grid crossings give
Z0>=L/486. The paid report's strip count N(t)<=tL²+3L fort<=1/2
follows by partitioning into cos(theta_x)<=7/8 orcos(theta_y)<=7/8,
where the relevant sine is >=sqrt15/8; global N(t)<=2tL²+3L.
Dyadic shells give Z0<=16L. Exact identities are
Z=||A^-1(I-K)delta||²=1-Z0/L² and Re u(0)=Z, hence P_f(0)>=Z.
Correct LCU success is Z/(49Z0)=Theta(1/L), despite FIVEsources.
Any normalized state supported in |b|<=C/L has spatial origin probability
<=N(C/L)/L²<=(C+3)/L whenC<=L/2. Therefore its actual SPATIAL output
TV from the native law is >=1-(C+19)/L. This is a full-output falsifier,
not merely loss of quantum-state fidelity. The native family itself has
classical point-mass approximation TV<=16/L; for finer epsilon, L<16/epsilon
makes the full-grid baseline polynomial in1/epsilon. No hardness follows.

Source-register issue independently checked against actual supplied primary:
V prepares sum alpha_j|j>,controlledphase,then SAMEV^dag and postselect0
implements sum|alpha_j|² phase_j, not arbitrary complexweights. Separate
left/right LCU preparation repairs this but pays the exact Gram norm.
Do not silently transfer our finite-difference counterexample to the source's
continuum-circle target. Their principal-value component is retained inq(k).
Report's finiteL4 last sentence is WRONG: the |b|<=eta shell is EMPTY,
not b=+/-1, sinceeta1/4. Its optional small control has no asymptotic force.
Final 'missing ring operation for arbitrary sources' wording is also rejected:
the needed target is FULL source-aware resolvent, not a constant-width ring.

POSITIVE-SEPARATED sources also fail as a generic repair. For every fixedR0,
choose fixed dyadic spacingd>=max(2,R0). No reciprocal-lattice Bragg point
lies onb0: modulo(1-zeta_d), the four roots sum0 inF2 whereas3=1. A norm
bound gives a positive explicit constantdelta_d. The paid construction uses
coefficients of(1+z+...+z^(M-1))^(2n) in each coordinate, withfixedM large
enough dependingd/delta_d, at sitesd(j1,j2). Allweightspositive integers,
m=O_R0(n²),totalbitsO_R0(n³), and normalizedGram
 Z/(sum_j w_j²*Z0)<=C_R0/L.
Near resonance at leastone coordinate stays a constant distance fromBragg;
Dirichlet-kernel sidelobes to power2n decay geometrically. Thefarband has
bounded inverse, and Plancherel pays the complete comparison. Parent checked
the actual inequalities, including polynomial input length. Use the explicit
rational lower gap from the norm, not an unexplained exact minimum oracle.
A separate parent binomial-taper variant has the same conclusion and is
under independent audit. This refutes inverse-polynomial noncancellation
from positivity plus ANYfixed separation alone. It does not prove hardness.
Paid report's proposed stronger growing separation is CONDITIONAL on a
uniform finite-torus Green decay lemma, which remains unproved/unimported.
No new paid neighboring frame request is selected.

## Single-source construction under audit; new UNKNOWN bill

Claude lattice-shell report completed/full parent-read/reaped. It proposes
actual full single-source quantum state prep using dyadic regular charts,
a deterministic approximate-label partition, windowsO(2^j), branch weights
2^-j and all far modes. Every retained Fouriermode has exactlyonepath;
the good amplitude is1/(M*a(k)),M²320L³, constant success fromZ0>=cL.
This avoids exact shell counts and continuum annuli. The remaining finite-
bit/uncomputation/capped-clock details are under independent review; no
m1 theorem is yet promoted. Parent identified local repairs: use unrounded
1.25/.57 width bound before comparingto.35; discard optionalatmostonegridpoint
argument from interval length.28+1; ensure emptywindow computations remain
valid for all inputcolumns. No general source or advantage conclusion.

OpenAI classical-superposition request terminated RemoteProtocolError with
EMPTYreport and UNKNOWNbilling. It was reaped and was NOT retried. This is
a FIFTH unknown bill, additional to the FOURhistorical ones; no known charge
or finding can be assigned. OAI fullresolvent and singleGreen remain running.

Actual classical primary Martin2006, sections4.1/4.2 andEq20/29/33 read from
sources/new_native_wave/martin2006.txt. It supplies infinite-lattice outgoing
stationary-phase asymptotics, not a uniform finite-torus1/L-damping clock or
error-certified sampler. Do not promote that asymptotic formula into our
endpoint. Parent potential route: periodize the complex-energy stationary-
phase kernel and sample a1/(1+r) envelope; uniform damping/image/error bounds
remain unpaid. This is an operation-level classical hypothesis, not a theorem.

Independent positive-array193LF proof parent-read in full: explicit dyadic
R>=R0,delta7^(-(R/2-1)),gammaR²delta²/1024,Mceil(8n/gamma),nthreshold
max(4,log2R,4Rceil(8/gamma)). Polynomial explicit binomial source has
Z/(W2Z0)<=390(16delta^-2+1)/L. This independently closes the scoped
positive/fixedseparation falsifier, with no hidden minimum-gap oracle.

## Two newly source-backed constructive lemmas

After exact corpus lookup andactual Cor2.6/section3.2 proof of Avendano--
Krick--Sombra math/0602145, a concrete sparse ordinaryquotient operation is
nowbeing checked. Gap decomposition splitsF intoatmostm smallbboxpolynomials;
ifP dividesF, noncyclotomicfactor scope forcesP todivideeachpiece. Dense
piecequotients couldgive a polynomial-explicitH despite binaryexponents.
This is the actual source-normalization deflation blocker, not a newarithmetic
subsystem. It is UNDERREVIEW; ordinaryLaurentdivision differs frommodulo
X^L-1,Y^L-1, whereinversion would merelyrestate theoriginalproblem.

The separate new Martin2006-source lemma asks for a quantified complexenergy
stationaryphase remainder andperiodicimage envelope, at enough global l2
accuracy forclassicalm1spatialsampling. The oldinfinite-latticeasymptotic is
not granted a finite-torusclock. Both are NEW selected-source proof requests,
4USDceilings notcharges, underwave-source-lemmas/dispatch.json. Neither is a
retryofthefailedbroadclassicalsuperpositionrequest. Owner nowreportsSPENT
Claude155.99USD,OpenAI101.71USD; stored separatelyfromrunnerestimates and
not treatedasremainingbalances. No newimplementation.

## Full first-batch read and new classical-match claim

All six first-batch jobs terminal; five substantive responses fully parent-read,
one EMPTY RemoteProtocolError with UNKNOWNbill, no retry. Both remaining OAI
sessions alreadyreaped. The 282line independent selection/spatialTV proof is
fully parent-read: conservative Z0<=64L and TV>=1-[64+4(C+1)]/L
for any narrowband state (L>=max(16,8C)); origin sampler error<=64/L.

OAI full-resolvent report: ACCEPT exact F=PH+R, S=R-i*eta*H and
u=h+A^-1s; fullshell geometric covers need no cardinality oracle. Its
universal theorem (D), (||h||+beta)^2<=poly(input)||u||², is explicitly
UNPROVED. Nondivisibility is not noncancellation: F=P+L^-2. Generic monic
normal-form division has exponential output: F=1+X^D+Y^D,D=L/4,
Q=YP gives quotient sum_j t_j(X+X^-1-3)Y^(D-1-j), with coefficient
(-1)^j on X^j. This concerns nonzero-remainder division; it does NOT
refute polynomial sparse EXACT-divisible quotient recovery.

ACCEPT restricted classical match from that report: if an exact quotientH
has polynomial explicit support s, then u=h-i*eta*A^-1h,
||u||²=||h||²-eta²||A^-1h||² and
TV(P_u,P_h)<=sqrt(128s/L). For L>=512s/epsilon² sample the explicit
h coefficients to error epsilon/2; otherwise L²=O(s²/epsilon^4) and
exact rational full-grid elimination plus capped finite-bit CDF is polynomial.
Polynomial coordinate span makes ordinary quotient recovery polynomial by
dense division; a new source-backed gap lemma is testing binary-exponent
exact-divisible recovery. No hardness or quantum advantage in this family.

OAI single-green report is FULL parent-read. It proposes a complete classical
m=1 finiteclock sampler: exact residue integral, fixed nonsingular contour,
uniform stationary phase remainder O(r^-3/2), O((n+log1/epsilon)^2)
periodicimages, radial-plus-uniform rejection with polynomial acceptance.
The central claimed C4 bound uses exp(-c*r*eta)(1+(r*eta)^4), paying
noncommuting limits. Parent checked algebra and sampling reduction; independent
full contour/constant/clock review is ACTIVE. This claim stays UNDERREVIEW,
not a classical theorem merely because the report calls it proved.
The existing separately dispatched Claude uniform-envelope source lemma is
independent and stilllive; it was not launched as a retry or after seeing
this report. Two new sourcelemmas use 4USDceilings, not charges.

## Exact-divisible source lemma: source correction and closure

Both new Claude lemmas terminal/reaped. Sparse-deflation report FULLread;
uniform-green-envelope truncated EMPTY, no findings and no retry. Exact
ordinary quotient recovery is CLOSED WRITTEN with the following repair.
Actual PDFpage12, retained sparse_bivariate_cor25.png, shows Cor2.5 uses
5^6=15625, NOT56 (pdftotext loses the superscript). The report's Delta288000B
and its numerical coefficient/support constants are REJECTED. Replace by
Delta=2^27 B: 5^6*2*3*(log2(96))^3*3B < 2^27B. Asymptotic bounds survive.
Source definition h1 on physicalLF306-358 agrees with archimedean l1 and
nonarchimedean max; after common Gaussian integer scaling, h1<=3B for
B the total binary rational coefficient encoding, B>=m. Monomialshifts and
subsum coefficients obey the same bound. Actual Cor1.2,totaldegree3 and
Cor2.5 proof/section3.2 have been read; this invokes their published theorem,
not an unverified abstract.

Parent independent irreducibility check: XY*P is quadratic inY overC(X),
discriminant (X²-5X+1)(X²-X+1) has four distinct nonzero roots and is not
a square. Gauss lemma gives absoluteirreducibility; five terms exclude a
binomial/cyclotomic factor. Gap split firstY thenX gives atmostm shifted
boxes of sides atmost(m-1)(Delta-1). Cor2.5 implies P|F iff eachsmall
piece is divisible byXY*P. Dense lex triangular quotient recurrence and
exact product verification give explicitH with atmost(m-1)²(Delta-1)²
terms, coefficientbitsO(mB), exponentbitsO(n), and polynomialBITcost.
Huge fixed constants, no practicality claim. The report's recurrence and
assembly were independently checked; repeated division is not being claimed.

Torus qualification is essential: the[0,L) lift can reject Bop*delta0
because it wraps. For a supplied polynomial boundS on support of an
undamped torus quotienth, test(2S+1)² shifted coordinatewindows when
L>=2S+2. At least onecut avoids two adjacent occupiedrows andcolumns;
then h and Bop*h lift without wrap. Every acceptedordinary quotient
reduces to a validtorus quotient. SmallerL uses fullgrid polynomialinS.
The earlier sharper Z0<=64L or128L estimate implies the same-output
classical sampler TV<=sqrt(128s/L), with polynomial1/epsilon fullgrid
fallback. Thus exact-divisible small-support quotient sources are classically
matched, with quotient RECOVERED rather than suppliedadvice. General
approximate/source-conditioned deflation remains OPEN. No genericdivision,
classicalhardness, quantumadvantage or new algorithm novelty follows.
