# One native bosonic normalization question

Input N-by-N explicit rational complex contraction A, singular values in[1/2,1]; N modes and exactlyN bosons, initial Fockstate |1,...,1>. Output occupation sample toTV eta from normalized Gamma(A)|1^N>. A ispublic, all N² entries/inputprecision charged. No normalized-state/reflection oracle, hiddenoverlap, suppliedgap orpostselection. Unitarysubcase isKNOWNbosonsampling, notanewShor-levelalgorithm. Directpassivedilation allsurvival canbe2^-N evencondition2 (diagonalhalf-loss example), butthat example'snormalizedstateiseasy; thisonlykillsdirectpostselectionclock. Columnscalarscancelafterstate normalization: doNOTcallthatdiagonalexampleahardinstance.

Actual prior check: Brod--Oszmaniec1906.06696v4 Theorems3/4 approximate UNCONDITIONED loss-channel output; theirTV error doesnotautomatically control exponentiallyrareall-N-survivorconditional law. Theorem2 isexactgeneralFocksampler withexponential product ofoccupancyfactors forN singlephotons, efficientcorollaryonlyfewoccupiedmodes/highlyunbalancedinputs. Noalgorithm forourfullconditionalmodel imported. Corpuslookupfoundonlyoverbroad/quarantinedloss/gapbarriers; theyareNOTusedasno-go.

NEW explicit parent proposal (parentderived, notliteraturetheorem): bosonic creationvector a†, annihilationa. b_j†=sum_u A_uj a_u†; c_j=sum_v(A^-1)_jv a_v, so[c_i,b_j†]=deltaij. Let K_j=b_j† c_j−1, H_A=sum_j K_j†K_j restrictedtofixedN-particle sector. Gamma(A) n_j Gamma(A)^-1=b_j†c_j. Henceuniquecommonzero vector ispsi_A∝product_j b_j†|0>, thedesiredstate. A nonunitarysimilarity isNOTunitary; no gapboundfollowsfromtheinteger eigenvalues oftheK_j. ||K_j||≤2N+1, so||H_A||≤N(2N+1)². Itisnumberconservingandquartic, withO(N^5)explicitterms andpoly-bitcoefficients. No FockcutoffbeyondfixedparticleN.

Polar A=U P. Preparepsi_P thenapplyknownGamma(U). Path P(s)=(1−s)I+sP stays[1/2,1], beginswithH_I=sum(n_j−1)² whosefixedN groundis|1^N>, gap2. H(s), firsttwoderivatives havepolyNnorm andexplicitpolybitcoefficients. Uniformgap≥N^-C forEVERYsuchP,s wouldpayadiabaticpreparationandnormalizedoutput withpoly(N,B,1/eta)gates; fullpromise isexactlythisGAP, notassumed. Genericsimilarityconditioningonlygivesexponential κ(Gamma(P))≤2^N anddoesnotresolveit. Noadvantage/hardness/noveltyclaim fromfiniteexamplesorfailedattacks.

Cheapest adversarial families: blockdiagonalP (onlytestsproductstates), rank-one P=(I+a uu*)/normalization withu=ones/sqrtN andκ(P)≤2, orboundedconditiondense/bandedP. Norm ofthetargetis per(A†A); forG=I+b J/N theexactpermanentis sum_r (N)_r (b/N)^r, witha changeofextensive saddleatb=1. ThiscanlocateapotentialcollectivebarrierbutisNOTaHamiltoniangaptheorem. Matrix P ratherthanG mustsatisfyspectralpromise. No finite-sizegapfitprovesanything.

Strongestclassicalbaseline: exactoccupation/amplitudesvia permanentsequentialmethods, scalar/unitary/orthogonal-column cases, lowrank/lowphotoncases, positive/small-offdiagonalGram clusterexpansions ifhypothesesproved. Needchecksameconditionaloutput, notunnormalizedweightalone. Thissingleproof/falsifierquestiondirectlyremoves thefullalgorithm'snormalizationblocker; no newinfrastructure/quantumimplementationwillbe built first.


Status: NEW unproved parent-gap candidate, no quantum implementation.
Two distinct paid proof/attack obligations prepared in
`audits/api_inputs/2026-11-13-bosonic-parent/dispatch.json`.
Prior community endpoint and all stronger classical baselines stay closed.
Independent171LF opportunity comparison was fully parent-read. Its other
GI low-coordinate-discard and local-fragment-gap compilers fail scoped exact
tests; none is promoted to a broad no-go. The native bosonic operation here
is a NEW parent-Hamiltonian proposal, beyond the rejected direct dilation.


## Explicit rank-two counterfamily: global-gap conjecture refuted

The parent has now read and checked all 274 lines of the stable independent
proof, `audits/reviews/2026-11-13-bosonic-parent-native-audit.md`, and the
complete independently obtained OpenAI counterfamily report. This is an
analytic asymptotic upper bound, with no finite-size fit.
For N divisible by4 take u=ones/sqrtN and v with phases1,i,-1,-i repeated,
normalized bysqrtN, and

 P=(I+uu*+vv*)/2.

This is an explicit rational-complex matrix, eigenvalues1 (twice) and1/2
otherwise. Its input bit length is polynomial in N; it satisfies the
ORIGINAL one-photon-per-mode and N-boson contract. Set D=n_u-n_v and
psi=normalizedGamma(P)|1^N>. A mode permutation/diagonal-phase involution
swaps u,v and fixes the input up to global phase, so the law of D is symmetric.
The trial vector sign(D)psi is orthogonal to psi. Each K_j is bilinear and
changes D by at most2. Thus its commutator with sign(D) acts only on the
input sector |D|<=2, and the trial energy is polynomial(N) times
p_boundary=Pr_psi(|D|<=2). No claim follows from an auxiliary saddle alone.

The bridge to the ACTUAL occupation law is exact. If
Z(b1,b2)=per(I+b1 uu*+b2 vv*), its coefficients c_rs are nonnegative.
At b1=b2=3, auxiliary R,S weighted by c_rs*3^(r+s)/Z are independent
Binomial(n_u,3/4),Binomial(n_v,3/4), conditional on actual occupations.
The positive Gaussian integral for Z, after angular averaging, is a
nonnegative sum of radial monomials. Conditional on R,S, its unscaled
squared radii X,Y are independent Gamma(R+1,1),Gamma(S+1,1).
For physical |D|<=2 this gives |E(X-Y)|<=3/2 and
Var(X-Y)<=15N/16+2. Therefore with constant probability |X-Y|<=N/6.
A small Gaussian central strip hence bounds physical p_boundary from above.

For scaled x=X/N,y=Y/N,t=x+y, the four equally populated phase groups give
an exponent upper bound

 F <= g(t)+(1/2)log(1-18xy/(1+3t)^2),
 g(t)=log(1+3t)-t, max g=f*=log3-2/3.

On |x-y|<=1/6, if t<=1/3 the gap from f* is at least1/15. If t>=1/3,
xy>=3t²/16, and the logarithmic correction is at most-3/64. Thus this
entire central strip has rate at most f*-3/64. The norm has an axis-region
lower bound exp(N f*-4); direct integration including the tail gives
Gaussian strip probability <=2^14 N² exp(-3N/64). The bridge then gives
p_boundary<=2^15 N² exp(-3N/64) for N>=256.

Using ||K_j||<=2N+1, the expected trial energy divided by its norm yields

 gap(H_P) <= 2^22 N^5 exp(-3N/64),

for N divisible by 4 and N>=1024. The uniform inverse-polynomial GLOBAL
gap conjecture is refuted. This removes its proposed proof of the adiabatic
compiler; it does not establish slow dynamics or sampling hardness. The
Gaussian coefficient coupling, infinite-volume tail, explicit norm lower
bound, orthogonality and commutator support were checked directly. No
numerical control or quantum implementation is needed for this deduction.


CRUCIAL parent scope correction: the low-energy sign(D) trial lies in the
OPPOSITE symmetry sector to the ground state. For this exact family the
linear path P(s)=(1-s)I+sP preserves that symmetry. Hence the exponential
GLOBAL gap falsifies the stated uniform global-gap certificate, but does
not itself establish that this family's actual adiabatic evolution is slow.
A same-sector gap could be polynomial; it is not proved here. No runtime
lower bound, all-path obstruction or sampling hardness follows. Any earlier
wording that the compiler is killed refers ONLY to its proposed global-gap
proof, not a demonstrated impossibility of its dynamics.


## Paid report dispositions and robustness

Both jobs in `audits/api_inputs/2026-11-13-bosonic-parent/dispatch.json` are
terminal, fully parent-read and reaped. Claude's 9,128-byte report correctly
left the gap unresolved. Its unique-zero, scaling and similarity observations
are retained; its small-perturbation estimate is used only for small delta.
The 12,121-byte OpenAI report independently derived the same four-phase
rank-two family and exact physical/Gaussian coupling. Its looser exponential
rate also suffices; the standalone proof above supplies the explicit bound.
The generic lower bound 2*4^(-N) is consistent with both upper bounds.

A checked corollary from the OpenAI report removes the exact exchange
symmetry without removing the spectral obstruction. Set
P_tilde=P-(1/(4N))*uu*. Then Gamma(P_tilde)=R Gamma(P),
R=(1-1/(4N))^(n_u), with (3/4)I<=R<=I. The new constraints are
R K_j R^(-1). Transport a unit ground-orthogonal low-energy vector by R and
project away from R psi. Its norm is at least 3/4, because distance to the
transported ground line is bounded below by sigma_min(R) times the original
distance; its energy is no larger than before, since the subtracted ground
component has zero energy and ||R||<=1. Hence the gap bound changes by at
most 16/9. The input still has O(log N)-bit rational entries and eigenvalues
1, 1-1/(4N), and 1/2. This is a spectral statement, not an adiabatic runtime
lower bound, and does not license a nearby perturbation campaign.

The round's saved estimates are Claude USD0.712780 and OpenAI USD1.783040,
total USD2.495820. They are not provider invoices or balance measurements.
The next scientific action is an independent comparison of end-to-end
mechanisms by external value, rather than another gap variant.
