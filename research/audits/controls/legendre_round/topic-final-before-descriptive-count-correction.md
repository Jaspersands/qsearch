# Native Gauss-Legendre coherent transform

2026-11-13. REVIEWED WRITTEN construction closed. For every binary N>=1,
the exact orthogonal Gauss-Legendre matrix has a uniform clean circuit of
operator error <=epsilon, using gates and workspace polynomial in log N and
p=ceil(log2(1/epsilon)). Classical generation also charges B_epsilon for
reading an arbitrary rational accuracy encoding. This covers arbitrary
reference-entangled input on the N valid labels. Full 186-line scalar and
337-line coherent proofs were independently reviewed and then fully checked
by the parent. This is AI mathematical review, not human/formal verification,
implementation, practical resource certification, novelty or a speedup claim.
No Hahn/CG, general Jacobi, or differential-equation transfer is asserted.

The complete proof is in audits/reviews/2026-11-13-legendre-scalar-source.md
and audits/reviews/2026-11-13-legendre-coherent-blocks.md. Historical admission
and intermediate open-gate text below records the construction's provenance;
the closure statement and these complete proofs supersede those gate statuses.

Problem/input: binary N>=1, rational0<epsilon<1/4, and an arbitrary reference-entangled quantum state supported on N basis labels. Implement with clean ancillas and operator error<=epsilon the EXACT orthogonal matrix U_jk=sqrt(w_j*(k+1/2))*P_k(cos theta_j), 0<=j,k<N. theta_j are increasing angular roots of P_N, w_j=2/[(1-x_j^2)P_N'(x_j)^2]. No supplied node table, coefficients, QRAM, preparation oracle, dense preprocessing or postselection. Target gate/classical uniform-generation/workspace poly(logN,log1epsilon). This is a native coherent spectral-transform endpoint, not a Shor-level algorithm, Hahn/CG transfer or classical-input speedup. Classical full-vector baselines cost near-linearN with preprocessing; succinct input/output instances can be easier and remain separate. Expected advantage only a compact coherent transform if proved.

Prior gate: exact corpus been-tried/baselines then actual primary source checks completed. No direct baseline keyword match, replaced by classicalfastJacobi. Prakash2610.03581v1 Thm3.15 gives Hahn O(N polylog), notlogN; Krawtchouk beam splitter already known and closedrepo. Duong-Hosters2611.06651v1 Thm1 gives clean QUT for FIXED INTEGER Gegenbauer m>=2 and N+m power2, with polynomial uniform generation. It explicitly excludes Legendre alpha=beta0; finiteDarboux map onlyhalf-integerJacobi. Its endpoint-divergent coefficient costsO(N). Bremer fastJacobi usesdenseNxrfactors and explicitlydoesNOT proveuniformrank bound. Do notimportfreebutterflycoefficients.

NEW OPERATION: partition angular index j (reflecttheta>pi/2 using parity(-1)^k) and degree k into O(log²N) dyadic rectangles. For j~J,k+.5~K, theta~J/N and phase p=JK/N. ChooseL=C log(N/epsilon) with explicitC to prove. Lowphasep<=L usesanalyticseparatedChebyshevapproximation; highphasep>=L usesactualuniformStieltjes expansion localized BEFORE block normalization. Sum rectangle block encodings and amplify full nearly-orthogonal matrix, not individual unitaries.

Lowphase: Mehler-Dirichlet after t=theta*sin(phi) is
 P_nu(cos theta)=(2/pi) int_0^(pi/2) cos((nu+.5)theta sinphi)/sqrt(sinc(theta(1+sinphi)/2)*sinc(theta(1-sinphi)/2)) dphi.
For realtheta<=pi/2 amplitudeuniformbounded; choose u=(k+.5)/K in[1,2], v=theta/Theta in[1,2], Theta~J/N. OscillationKTheta uv<=O(L). Proposedfixedcomplexellipsebound exp(O(L)) yields tensorChebdegreeO(L+log1delta), coefficientsl1polydegree because realfunctionbounded. Evaluatingcoefficientsvia quadrature usespoly(L,log1delta), noNtable. Weightsand sqrt(k+.5)areseparateddiagonals. EntryboundO(sqrt(p)/sqrtN), uniformrectangle outerproductnormsqrt(JK), hence blocknormalizationO(p), NOTsqrtp. This ispolylogforp<=L. Need certifycomplexanalyticdomain, coefficientcomputation and globalentry/operror.

Highphase: use ACTUAL Johansson-Mezzarobba1802.03948v2 Eq17-21:
 P_n(cosθ)=sqrt(2/(pi sinθ)) sum_(r=0..R-1) C_nr cos((n+r+.5)θ−(r+.5)pi/2)/sin^rθ + ξ;
 C_nr=Gamma(r+.5)^2 Gamma(n+1)/(pi 2^r Gamma(n+r+1.5) Gamma(r+1));
 |ξ|<2sqrt(2/(pi sinθ))*C_nR/sin^Rθ;
 C_nr<=r!/[pi sqrt(n)(2n)^r] (n,r>=1).
Thus onrectangle n sinθ>=c p withp>=CL, R=O(log(N/epsilon)) shouldyieldtinyentryerror and summablecoefficientnormalizations. Phasefactorsseparate intocommonexp(i nθ_j) and rowexp(i(r+.5)θ_j). sqrt(n+.5)C_n0bounded. Fourierbase normalizationN^-1/2 paid byrow sqrt(N wj/sinθj). Needboundsanduniformbitgammaratio, not numericalclaim.

NonuniformFourier core: θ_j=(j+.75)pi/(N+.5)+Δ_j withNΔ_j=O1 is a proposedpaidrootlemma. Then Taylor exp(i kΔ_j) hasconstantl1normalization via (k/N)^r(NΔ)^r/r!, whilebase is restricted QFT_(2N+1) with diagonalphase andconstantnormalization. AlternativeavoidnonpowerQFT: M=power2>=cN, a_j=nearest Mθ_j/(2pi) usingfiniteapproxtheta; angularrootgap>=c0/N givesinjectiveordered a_j. Coherentinjection/inversebinarysearch costs polylogN ifperindexnodeaccesspaid. Δ_j=θ_j−2pi a_j/M boundedO1/N. Need proveallfiniteprecision/injectivity, noassumedrootoracle.

The main native gate: certifiedperindexGaussnode/weightalgorithm polynomial(logN,p) forpbitaccuracy, noexpectediterations andallj includingendpoints. Johansson-Mezzarobba Eq17-21 andProp8 near1 providefastscalarevaluation; Sec7.2 hasperrootintervalNewton but citesPetrasinitialenclosure. Its globalTheorem1 is NOTthe neededbinaryN theorem. Mustderivecertifiedbrackets/gap/weightbounds and a cappedclock or leaveOPEN. SourceFLINTwebdocs markedpartLLMgenerated has a suspectprefactor; useACTUALpaperformulaabove, notthatdoc. HaleTownsendURL404 givesnoevidence.

Classical cheapest attack already applied analytically: blanketcoefficients needO(N)subnormalization; lowphase localizedFrobenius/outerproductcost isO(p), notsqrtp. Nofinitechecksorquantumcode justifyasymptotics. Decisivefalsifiers: an O(N)node/coefftable, endpointnonanalyticityrequiringdegreeN, coefficientl1superpolylog, tinybranchmass, or globalnormlossN survivingprecisionbudget. Finalblocknormalizationmustbeexplicitpoly(logN,log1epsilon), withallpreparation/reflections/precision paid. No algorithm admitteduntilalltheseareproved.

## Status
One bounded constructive admission, not a theorem. Independent source and analytic reviews underway. Two distinct Anthropic obligations prepared; OpenAI exhausted, no paidcalls. PriorGram endpoint frozen47uniquehashes.

## Parent native-node derivation (independent check underway)

Setnu=N+1/2. Forone-basedj=1,...,floor(N/2), define
I_j=[(j-1/2)pi/nu,j*pi/nu]. ActualJM Eq17 withR=1 hasrelative
error2*C_N1/(C_N0*sinθ)=1/[2(2N+3)sinθ]<1/4 at bothendpoints,
because sinθ>=2θ/pi>=(2j-1)/nu. Theleadingcosinesareopposite
+/-1/sqrt2. HenceeachdisjointI_jcontainsaroot. Reflectionandthe
oddNcenterθ=pi/2accountforallNroots, soeachindexiscertifiedwithout
Petras, scanningNroots, oradvice. Adjacentangularrootgap>=pi/(2nu).
Withtheta0_j=(j-1/4)pi/nu, |N(theta_j-theta0_j)|<=pi/4.
N1istrivial; endpointsneversitatzero.

Forweightbounds,u(θ)=sqrt(sinθ)P_N(cosθ) solves
u''+q(θ)u=0, q=nu²+1/(4sin²θ). E=u'²+q*u² obeysE'=q'*u².
On(0,pi/2),q'<=0 andq'/q<=E'/E<=0. Therefore
Ecenter<=Eroot<=Ecenter*qroot/qcenter<=1.25Ecenter, since
nu*sin(theta_root)>=1. Exactcentralbinomialvaluesatpi/2andWallis
giveN/2<=Ecenter<=4N, includingN1. Ataroot,w=2sinθ/Eroot, so
(2/5)sinθ/N<=w<=4sinθ/N. No asymptotic unknownconstant isneeded.

Onaninitialbracket,q<=1.25nu². Startingfromitsroot, comparethe
zerosolutionwithsin(sqrt(1.25)nu*d)/(sqrt(1.25)nu). Since
|d|<=pi/(2nu), positiveVolterrakernel/Sturmcomparisonkeepsa
constantfractionofinitialslope: |u(θ)|>=c sqrtN |θ-theta_root|.
Thus sufficientlysmallcertified|P_N| impliesa smallrootdistance;
a sign-ambiguousbisectionmidpointcanterminatewithacertifiedinterval
ratherthantriggeringuncappedprecision. Characterreviewindependently
hasanequivalentPrueferbound. Exactconstants/finiteprecisionarebeing
writteninthatreview.

IntegerdegreeP_n evaluationhasafixedpoly(logn,p)-BITalgorithmfrom
actualJM scalarformulas: whenn*sinθ>=C(p+logn), takeO(p+logn)
StieltjestermsusingEq19/21; otherwiseonreflectedθ<=pi/2 onehas
nθ=O(p+logn), soEq27endpointseriestruncatesinpoly(p+logn)terms.
CancellationusesO(p+logn)extrabits, notexponentialtime; derivative
Eq30/31 similarlypaid. Whennislesspoly(p), directrecurrenceiswithin
thatbound. Needexplicittailcaps, gammabaseevaluationandallbranch
precisionbeforecallingthenativegateclosed. Thesearewrittenproof
obligations, notassumptionslicensedbyFLINT'sword-sizedimplementation.

PaidClaudeFablemaxcalls: nativeanalyticprocess8399 andblockattack67507,
both64000maxoutput, localceilings5USDeach(notcharges/billingcaps),
explicitpackets/snapshots. OpenAInotcalled. TheseareNEWhypotheses, not
retriesoftheemptyGramreport. Noalgorithmclaimfrompendingreports.

## Parent coherent-kernel details for the independent audit

Lowphase interpolation can use normalizedvariablesu=(k+.5)/Kmax and
v=theta/ThetaMax in[0,1]. OnarectangleKmax*ThetaMax<=O(L), theMehler
integrand isanalytic onfixedBernsteinellipsesinu,v andafixedstripinphi: 
sincargumentsstayuniformlyawayfromnonzeromultiplesofpi when
ThetaMax<=pi/2. Itsgrowththereisexp(O(L)). TensorChebinterpolation
degreeO(L+log1delta)thereforehasuniformerror delta; coefficientl1 is
O(degree²), usingboundedrealvaluesandtheDCTcoefficientformula. The
integrandisevenandpi-periodicinphi (thetwosincfactorsexchangeunder
sinphi->-sinphi), soP_nu equalsitsaverageover[0,2pi]. Uniformperiodic
trapezoidalquadraturewithO(L+log1delta)nodescomputesentriesandthen
thepoly-sizeDCTtable. ThisisaPOLYLOGtableofkernelcoefficients,not
anN-by-r factor table. Needcertifyexplicitfixedellipse/stripconstants.
The lowphaseblock isdiagonal-sqrtweight timesa sumofrankone
Cheb(u)Cheb(v)outerproducts timesdiagonal-sqrt(k+.5); eachnormalized
outerproductofuniformrectangleintervalvectorscostspolylogN. The
normalizationboundisO(p*degree²), p=JK/N.

Highphase JMcoefficients satisfy sqrt(k+.5)*C_kr/sin^rθ <=
C*r!/[2k sinθ]^r forr>=1, withboundedr0term. Onadyadicrectangle
with min(k sinθ)>=C0R theR=O(log(N/epsilon))terms have summable
individual diagonal-normalizationproducts. Eachcosineusesrestricted
nonuniformFourierandrowphaseexp(i(r+.5)θ). Theprefactor
sqrt(N*w_j/sinθ_j)isuniformlyboundedbytheprovedweightlemma.
Choosingentryerror<=epsilon/(polylog*N)paysthefulloperatorerror
bytheFrobeniusbound, not byassumingpointwiseerrorisoperatorerror.

A power-of-two QFT avoids a non-power Fourier oracle AND avoidscomputing
Gaussnodesforgridinjection. LetM beapoweroftwowith8N<=M<16N.
Forzero-basedj, definea_j=nearestinteger M*(4j+3)/[4*(2N+1)].
These aredistinct orderedindicesin[0,M), evaluatedbyexactbinary
arithmetic. Theinversecandidate isnearestinteger (2N+1)*a/M-3/4,
followedbychecking a=a_j. Itsroundingerroris<(2N+1)/(2M)<1/2.
Thus reversibleinjection/uncomputationcostspolylogN. With
theta0_j=(j+.75)pi/(N+.5), theprovedrootbracketimplies
|N*(theta_j-2pi*a_j/M)|<=pi/4+pi/8<2.
The matrix exp(i*k*theta_j)/sqrtN is a restrictedQFT_M, normalization
sqrt(M/N)<4, multipliedentrywisebyexp(i*(k/N)*(N*Delta_j)).
TaylorLCUofthislastfactorhasl1<=exp(2), withpolylogprecisiondegree.
Allrow/colrestrictionsareexplicitbinaryintervalpredicates; right-half
reflectioncontributesonlyknownparity(-1)^k. NoN-entrypermutationtable.

ThereareO(log²N)rectangles; sumsnotproductskeepoverallLCUnormalization
polynomiallog. TheassembledAapproximatesorthogonalU, soallitsvalid
singularvaluesareclose1. Itsblockencodingnormalization alpha isknown
polylog. Standardcleanpolar/obliviousamplification mustbecosted; an
explicitboundedoddpolynomialavailableforQSVT is
 P_m(x)=[integral_0^x(1-t²)^m dt]/[integral_0^1(1-t²)^m dt].
Itsdegree2m+1, rationalcoefficients havepoly(m)bits, |P_m|<=1, and
it approaches sign(x) exponentially in m*x² awayfromzero. Taking
m=poly(alpha,log1epsilon)keepsdegreepolylog; phase-compilationand
ancillaleakageepsilon²stillrequireexplicitstandardprimitivecitation/
verification. This is an avenue for the remaining fullcompiler proof,
not yet an admitted quantum algorithm.

## Scalar gate closed written after full independent review

Parent fully read and checked all186LF of
audits/reviews/2026-11-13-legendre-scalar-source.md. Accepted: actualJM
normalization; explicitendpoint/asymptoticO(p+logN)termcaps; polynomial
logGammaevaluationwithoutdegreeNbinomials; indexedone-termrootbrackets;
Pruefervalue-to-distancebound |P_N(cosθ)|>=sqrtN*|θ-theta_j|/4;
zero-safe cappedbisection; relativeweightprecisionwithonlyO(logN)guards.
The sharperenergyestimate N/2<=Ecenter<=2N yields
(4/5)sinθ/N<=w<=4sinθ/N (parent'searlier2/5lowerboundremainsvalid).
Allj,N,p and allbranches are covered, no sourceapproximateNewtonseed.
This closesONLYscalaraccess, notthecoherenttransform.

ActualretainedQSVTprimarysource checked: periodic_conduction/qsvt.txt,
arXiv1806.01838, Cor10LF744-760 polynomialclassicalphasecompilation,
Cor18LF1150-1187 realoddpolynomialSVT, Lemma19adjacentU/Udagger/
projectorcontrolimplementation. Parent'sboundedoddintegralpolynomial
hasdegreepolyalpha/logepsilon andrationalcoefficientbitspolydegree.
Withalpha andkernelapproximationproved, this standardprimitivecanpay
thecleanpolarstep. Itdoesnotpaytheunprovedkerneloritsnormalization.

Paid terminal checkpoint: BOTH Fablemax64000 requests exhaustedoutput
budgetwithEMPTYresponse andwerereapedexit1. Native8399estimate3.322940,
block67507estimate3.323240, total6.646180USD. No mathematicalevidence,
no retry. Independent local proofs, not these calls, support the scalar
result. Three consecutive maxeffort requests acrossGram/Legendre returned
empty; futureDISTINCTtasksneedmuchsmallerscope toavoidbuyingnoanswer.
Thisdoesnotauthorize retryingtheseproofobligations. OwnerAnth20.59anchor
remainsseparatefromestimates; do notclaimameasuredremainingbalance.

## Parent clean-completion error lemma

This is a conditional composition lemma while the independent kernel review
is being finalized; it does not by itself close the transform. Pad the target
to U0 = U_N direct-sum identity on the unused labels of the next power-of-two
register. The extra identity block has an exact binary predicate and constant
normalization cost. Suppose the constructed ideal block is A/alpha, with
alpha >= 1 a computed polynomial bound and ||A-U0|| <= eta < 1/2.
Every singular value of A lies in [1-eta,1+eta]. If V is its polar unitary,
then ||V-A|| <= eta and consequently ||V-U0|| <= 2 eta. No condition number
of an unrelated padded zero block is being assumed.

For the odd polynomial P_m displayed above, its denominator is at least
1/(2 sqrt(2m+2)): integrate only up to 1/sqrt(2m+2) and use Bernoulli's
inequality. Therefore, for 0<x<=1,

    0 <= 1-P_m(x) <= 2 sqrt(2m+2) exp(-m x^2).

Put zeta=epsilon^2/1024, eta=epsilon^2/4096,
k=ceil(log2(16(alpha+2)/zeta)), and m=ceil(64 alpha^2 k^2).
For x >= 1/(2 alpha), the displayed bound is below zeta (the loose
quadratic choice of k dominates the logarithmic prefactor uniformly).
Thus odd singular-value transformation of A/alpha has successful block C
with ||C-V||<=zeta, before phase approximation. This construction uses
degree 2m+1 and rational polynomial coefficients of polynomial bitlength;
alpha is polynomial in the logarithmic input parameters, so this degree
and its classical phase-compilation cost are polynomial as well.

The clean-ancilla guarantee follows directly from unitarity, without
postselection. If J embeds the logical register with all ancillas clean,
and an ideal unitary word T has J^dagger T J=C, then

    ||T J-J U0||^2
      = ||2I-U0^dagger C-C^dagger U0||
      <= 2 ||C-U0|| <= 2(zeta+2 eta).

Allocate the phase-compilation error another zeta in successful-block norm;
the same identity then gives a clean-isometry error strictly below epsilon/8.
Compile the resulting entire ideal word, including controlled scalar phases,
to finite gates with total operator error at most epsilon/4 by a gate hybrid.
Its adjoint calls must reverse the ACTUAL same compiled word and workspace.
The whole error remains below epsilon on arbitrary entangled input. No
measurement, ancilla reset, successful-branch conditioning or finite-size
inference enters this lemma. The full kernel still must supply A, alpha,
its scalar/coefficient clocks, and the stated eta approximation.

## Final proof disposition and scope

Parent fully read all 337 lines of the independent coherent review, checking
its rho=2 analytic domains, finite quadrature/DCT coefficients, full-interval
preparations with clipping masks, high-phase gamma ratios, exact Fourier-grid
injection, and padded polar/QSVT construction. No blocker was found. With
H=32+ceil(log2(N/epsilon)), the proof gives O(H^4) coefficient terms,
normalization alpha=O(H^5), and an explicit QSVT degree O(H^11). These are
upper bounds on parts of the construction, not optimized total gate counts.
All scalar precision guards and fixed-gate programs have polynomial(H) caps.
The proof charges the full matrix error, epsilon-squared ancilla leakage,
controlled scalar phases, and reversed ACTUAL circuit words on the same banks.

The high-phase matrix need only approximate the target to O(epsilon): its
polar unitary differs by O(epsilon), while the separate O(epsilon^2) QSVT
error pays leakage. This sharper separation in the independent proof
supersedes the sufficient O(epsilon^2) input-block error in the parent lemma.
Both are valid composition arguments. The target is exact; approximations
refer to its finite circuit realization, not a changed grid or matrix.

The strongest retained classical comparator is the near-linear full-vector
fast-Jacobi algorithm with dense factors. It has a different input/output
model from an arbitrary amplitude state; no matched classical-input
separation is concluded. The actual integer-parameter QUT theorem and the
linear-in-N Hahn compiler remain prior art, with their scope boundaries intact.
No quantum implementation or additional finite tests were needed for this
written proof closure. The two paid EMPTY outputs were not used as evidence.

Next scientific action: finish the independent cross-direction selection;
do not extend Legendre to another family merely because this pass closed.
A new paid task needs a new concrete mechanism or decisive falsifier.
