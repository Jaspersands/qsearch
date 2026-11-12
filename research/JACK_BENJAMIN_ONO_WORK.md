# Native quantum Benjamin-Ono dispersion-quench work problem

Input: explicit partition lambda of numerical degree D, fixed alpha=3, TV tolerance0<eta<1. No quantum state, coefficient table, sampler or partition-function advice is supplied. Common canonical bosonic Fock basis is occupation |mu>, with sum k m_k=D. Define
 S=sum_(i,j>=1) sqrt(i j(i+j)) [a_i^dagger a_j^dagger a_(i+j)+a_(i+j)^dagger a_i a_j],
 N=sum_k k² n_k, H_i=S+(2/sqrt3)N, H_f=S.
This is the actual quantum Benjamin-Ono Hamiltonian in MM Eq2.1, normalized: T3(alpha)=alpha^(3/2)S+alpha(alpha-1)N. Do not identify Hall Fock with finite-particle Calogero-Sutherland position measure.

Prepare the specified initial eigenstate Jhat_lambda^(3), whose occupation amplitudes are theta_mu sqrt(z_mu 3^length(mu)/H_lambda). Parent reviewed WRITTEN full clean preparation costs poly(D,1/eta), no hidden advice, from explicit lambda. Its energy is E_i=2(C3(lambda)+D)/sqrt3, C3=sum_boxes(3x-y), zero-based column x,row y. Make a sudden quench to H_f. Required output: integer final energy e (work W=e-E_i has an exact quadratic-field description), within TV eta of its spectral Born law. Schur basis diagonalizes S with e_nu=2 C1(nu), C1=sum_boxes(x-y); |e|<=D(D-1). There are only O(D²) possible bins. Full final-shape sampling is NOT required.

Quantum candidate is already complete at WRITTEN level: existing initial Jack preparation; sparse simulation of S (O(D²) row neighbors, square roots of polynomial-bit integers, norm <=D(D-1)); ordinary coherent QPE of exp(2pi i S/M), M a power2>4(D+1)², reads integer energies without resolving degeneracies. Controlled times<2pi, precision/error paid polynomial(D,1/eta). No alpha1 transform, new quantum subsystem, giant time evolution or physical-position state conversion is needed. No novelty, speedup, hardness or implementation claim.

Classical target equivalently: in Hall-alpha1 symmetric functions f_lambda(p)=J_lambda^(3)(sqrt3 p_1,sqrt3 p_2,...)/sqrt(H_lambda), expand f=sum_nu c_nu s_nu; output e with P_lambda(e)=sum_(nu:2C1(nu)=e) |c_nu|². Existing alpha3 occupation Born sampler does NOT compute these coherent overlaps or their energy pushforward. Exhaustive p(D)=exp(O(sqrtD)) symmetric-function linear algebra supplies a rigorous subexponential baseline. Classical additive approximations of EACH energy probability to O(eta/D²), or characteristic function on O(D²) roots to suitable accuracy, would suffice. Charge bit precision, contraction and normalizers.

Cheapest strong classical attacks ALREADY verified: initial row(D) produces a Schur z-measure with real z=z'=1/sqrt3; column(1^D) produces the transpose of z=z'=sqrt3 (equivalently z=-sqrt3), so flip final energy for the transpose. At degree n, add box of ordinary content c with probability [(z+c)²/(z²+n)] * dim(nu)/[(n+1)dim(rho)]. These positive transitions normalize since Plancherel up-content moments are0,n. Path products and #paths=dim(nu) give n!/(z²)_n prod_boxes(z+c)²/hook², the actual Borodin-Olshanski Eq1.1 measure. Both row and column work laws have polynomial classical samplers with Q(sqrt3) arithmetic and finite-bit TV control. No generic hardness follows. Other bounded-Durfee inputs are NOT automatically covered by the old occupation sampler.

Actual current Tierz2509.09640v2 Eqs1-9 ties work to Loschmidt amplitude and Toeplitz determinants for specified effectively-free/Gaussian or domain-wall preparations. Our final S is free fermionic, but arbitrary initial Jack3 states do not come with that determinant/Toeplitz representation. Need derive it, not infer it from final Hamiltonian alone. Asymptotic Gaussianity without uniform finite-D TV bounds is insufficient. Conversely non-Gaussianity alone is no obstruction, since rows already have positive z-measure sampling.

Single most important unresolved scientific question: is there a complete polynomial classical sampler for THIS coarse work law on unrestricted lambda? A full sampler decisively removes this proposed physical advantage; a failed determinant/recurrence only scopes that construction. Core reports are advisory and all material claims will be independently verified.

## Parent verification and source scope

Independent193line review in audits/reviews/2026-11-13-jack-external-value-
selection.md fully parent-read/checked. Actual source extracts and live
paid briefs are under audits/api_inputs/2026-11-13-jack-work/. The original
Jack classical round has now supplied only scoped closure falsifiers, not
a full classical sampler; these are recorded in JACK_POSITIVE_CREATION_
CLASSICAL_ATTACK.md.

Additional standard baseline checked after corpus lookup: Jiang1204.1671
actual§2/Theorem2.1 gives a Metropolis random-transposition chain with
Ewens stationary law of parameter theta^-1. At theta3 this is the already
easy initial ROW's occupation Born law. Its Jack coefficients are spectral
eigenfunctions; sampling the stationary law is not sampling the squared
components of an arbitrary labelled eigenfunction, nor the mixed-basis
quench law. Diaconis--Ram1007.4779 actualEqs1.2--1.3 analogously specifies
a Macdonald stationary partition law, not arbitrary fixed-shape Born
sampling. No generic classical conclusion is imported from rapid mixing
of those DIFFERENT stationary laws. These source checks do not rule out
a new valid intertwining or mixing construction.

## Exact work-law falsifiers, with narrow scope

A tempting whole-law shortcut is to use only the two partition statistics
A=sum_i lambda_i², B=sum_j lambda'_j². Indeed, for g=(alpha-1)/sqrt(alpha),

 E_lambda(g)=[g(A+B)+sqrt(g²+4)(A-B)]/2.

Hellmann--Feynman gives <N2>=(A+B)/2+[g/sqrt(g²+4)](A-B)/2;
at g=2/sqrt3, <S>=sqrt3*(A-B)/2. Neither identity determines the full law.
ONE exact Sage control (no sweep) compares lambda33 and411, both D6,A18,B12.
Both have <N2>=33/2 and <S>=3sqrt3, but

 shape33: <N2²>=14022/49, <S²>=2232/49;
 shape411: <N2²>=16839/49, <S²>=5988/49.

The script uses actual Sage integral Jack expansions and the exact Hall
weights. Parent checked the receipt/method and relation
<S²>=[42²-168<N2>+4<N2²>]/3. Thus knowing the entire g-dependent energy
formula of the selected eigenbranch does NOT fix its quench work law.
Artifacts: audits/controls/jack_work_energy_collision/{control.sage,result.json}.
No quantum advantage or general recurrence lower bound follows.

Claude jack-schur-positive-work ended TRUNCATED with3060bytes, fully read.
It gives the correct row/column baseline and asserts several new claims,
but ends mid-contraction before their proofs. Its claimed D^O(m) exact
algorithm, general Schur-positive-mixture obstruction and exponential
vertex-coherent rank bound are NOT ADOPTED. No retry.

One useful assertion can be proved independently here without its missing
proof. From the already exact J21=p1³+2p1p2-3p3, Hall1 Schur expansion is

 J21^(3)(sqrt3*p)/sqrt315
   =(6 s3+9sqrt3 s21-6 s111)/sqrt315.

The work probabilities at e=(6,0,-6) are(4,27,4)/35. For EVERY admissible
Borodin--Olshanski z,z' measure at D3, the probability of middle shape21
(and hence energy0) is

 (2/3)*(z²-1)(z'²-1)/[(zz'+1)(zz'+2)] <= 2/3.

Proof: if z'=conjugate(z), put t=|z|²; numerator<= (t+1)², giving
a ratio at most (2/3)(t+1)/(t+2). If real z,z' have t=zz'>0 (including admissible degenerate limits),
the numerator=t²-z²-z'²+1 <=(t-1)² <=(t+1)(t+2).
The admissibility conditions are from the actual primary Eq1.1 discussion.
Limits retain the inequality. Positive mixtures retain it too. Target
27/35 exceeds2/3 by11/105, so no such mixture approximates this work law
in TV less than11/105. This refutes exactly a positive mixture of these
z-measure laws. It does NOT refute other Schur processes, positive integral
samplers, signed constructive methods, or general classical algorithms.


## Completed coarse-law attack: exact identities and limits

OpenAI jack-coarse-work-law completed with8139bytes/233lines, fully parent
read and checked. It supplies no unrestricted polynomial classical sampler.
Its actionable deductions below are accepted only at their exact scope.

The initial eigen-equation S psi=(E_i-t N)psi gives the same first and
second moments of S and A=E_i-t N, but NOT their whole distributions.
Already for D2,row input, in the occupation basis S=[[0,2],[2,0]],
N=diag(2,4), psi=(1/2,sqrt3/2), E_i=10/sqrt3,t=2/sqrt3. Direct algebra
gives <S^3>=4sqrt3 whereas <A^3>=20/sqrt3. Thus an occupation sample
pushed through E_i-t N is not the work sample, even in this easy family.

Some actual work probabilities are nevertheless polynomially computable.
For D>=2, the extreme energies +/-L, L=D(D-1), each have one Schur shape.
The coefficients of h_D and e_D, and actual primary Theorem2.2 in
Bendali--Dolega2305.07966v1 (J_lambda(u)=prod_boxes(u+3x-y)), imply

 P_lambda(+L)=prod_boxes(sqrt3+3x-y)^2/H_lambda,
 P_lambda(-L)=prod_boxes(-sqrt3+3x-y)^2/H_lambda.

Both use polynomial-bit Q(sqrt3) products. Parent checked actual source
lines440-463 and the products. The independent report finds the SAME
33/411 energy-curve collision as the exact parent control, now at a bin:

 P_411(30)=(386-207sqrt3)/28224,
 P_33(30)=(3146+1815sqrt3)/470400.

H_411=18289152,H_33=101606400. Thus the whole initial eigenenergy curve
also cannot determine the extreme-bin probabilities. Exact means are
<N>=D+(3 n(lambda')+n(lambda))/2 and <e>=sqrt3(n(lambda')-n(lambda));
these and two endpoint bins do not give a sampler for the remaining bins.

The small energy alphabet alone also does not justify Monte-Carlo moment
reconstruction at inverse-polynomial accuracy. The actual hook Schur
energies are e_j=2D j-D(D-1),0<=j<=n=D-1. On X=(S+L)/(2L), these are
j/n. Binomial(n,1/2) conditioned on even versus odd j has TV1, while
EVERY kth power-moment difference is

 2^(1-n) n! {k brace n}/n^k <=2^(1-n),

and vanishes for k<n. This is the finite-difference identity, with the
upper bound from surjections among n^k maps. These distributions are NOT
asserted to be Jack work laws. This only falsifies the generic inference
from O(D^2) bins and inverse-polynomial moment accuracy to TV accuracy.
Exact or exponentially accurate moments can still have polynomial bit
length; no classical lower bound or new nearby barrier is inferred.

Both paid work jobs are terminal and reaped. Frozen35hash usage/source
checkpoint: audits/controls/jack_work_round/. Round estimate3.721176USD;
cumulative224.954806USD/177priced records (Anth139.512426,OAI85.442380),
FOUR unknown bills excluded. Estimates are not invoices or balances.
The labelled parent-note snapshot there predates this final disposition;
it is preserved unchanged. No log-precision request is included.


Constructive resource upgrade (Nov13): JACK_LOG_PRECISION_COMPILER.md pays
both initial Jack preparation and the native final S simulation with
poly(D,log1/eta) BIT/gates. Full300line independent proof checked, including
S's unordered-pair factor two and canonical parity matchings. This upgrades
the SAME written TV sampler, without changing its input/output or classical
comparison. No implementation or advantage claim.
