# Homogeneous folded-chain quench: projected-Gaussian classical challenge

13 November2026. New pass after STATE/TRAPS and full197LF independent selection
`audits/reviews/2026-11-13-post-balanced-selection.md`. Full Born sampler and charged coherent amplitude compiler CLOSED WRITTEN
after full independent composition review; see closure below.

## Native question, prior work and candidate

Use EXACT native open Hamiltonian from FOLDED_CHAIN_COHERENT_TRANSFORM.md:
H_N=-(1/8) sum_(j=0)^(N-2) (1+Z_j Z_(j+3))(X_(j+1)X_(j+2)+Y_(j+1)Y_(j+2)).
For N>=2, rational p in[0,1], binary rational time t and epsilonTV, input
(sqrt(1-p)|0>+exp(i phi)sqrt(p)|1>)^(N+2), output one full physical spin word
from its evolved Born law. Charge N, all input/time/error and output bits.
The shared phase phi is irrelevant to this basis law because H preserves
magnetization. No arbitrary unknown quantum state or sector advice is supplied.

Known quantum endpoint: the already written all-sector clean transform gives
poly(N,timebits,log1epsilon) gates. Direct time stepping is not a matched
classical lower bound. Strong classical baselines include the existing
basis/Slater input match, free-fermion diagonalization, Gaussian/Pfaffian
sampling, and tensor-network contraction under its actual bond-size cost.
Target new classical match: poly(N,input/timebits,log1epsilon) BIT. If proved,
this would remove this homogeneous-product quench as a separation candidate;
it would not match the arbitrary-quantum-input unitary task.

The comparison also considered expanded CSA minimal-module output and growing
Gaussian-mixture learning; neither currently supplies as concrete a new
operation. All three corpus been-tried then baselines were checked. Negative
lexical matches were not adopted as no-gos. Parent independently checked
actual retained Ruiz2411.15132v3 passages1432-1454/1480-1503 (Dicke preparation,
fragment superpositions/correlation applications) and actual Bravyi0404180v2
Theorem1/corollaries371-420, Eq45-47666-695, projectors845-906. Bravyi pays
Gaussian closure and measurement algebra, not a hidden numeric-stability or
all-branch BIT promise. New source is retained under sources/2026-11-13-folded-gaussian/.
No novelty/priority claim is made.

## Exact new state operation

The established label lambda=(s0,w,d,m), ell=m+|w|, encodes all effective
weight-m words q. Every native move swaps physical01 and10, and adjacent
exclusion moves connect the full effective weight-m graph. Hence physical
magnetization Mphys is constant throughout each fragment. All homogeneous
product amplitudes in that fragment equal the same complex c_lambda.

Sample an ORIGINAL IID Bernoulli(p) physical word solely to obtain lambda,
then discard its effective positions and use the conditional UNIFORM Dicke
state |D_ell,m>. This samples the correct fragment weight including binomial
multiplicity. Dephasing labels is legitimate only because evolution and final
physical basis measurement are block diagonal. Within-fragment coherence is
retained; this is not a mixture of effective basis trajectories.

Let J_ij=1 for i<j and skew extend. Every even principal Pfaffian is1:
expand the first row, apply induction, and sum an odd alternating list of
ones. On ell physical modes plus one LAST spectator, the Gaussian pairing
Z=zJ therefore has Fock coefficients Pf(Z_S)=z^(|S|/2) for even S.
For 0<m<ell take z=m/(ell-m). The normalized Gaussian's squared law is
Bernoulli(q) conditioned on even total parity, q=z/(1+z)=m/ell.
Condition spectator s=m mod2 and physical particle count m. The remaining
state is exactly |D_ell,m>. Its success probability is at least

    min(q,1-q) Pr[Bin(ell,q)=m] >= 1/[ell(ell+1)].

Here m is a binomial mode, so its probability is >=1/(ell+1). m=0,ell are
fixed Slater/vacuum/full cases. Physical number-preserving free evolution
Gamma(U) with identity spectator commutes with both conditioning tests.
Thus evolve one known Gaussian, sample, accept the tests, and decode.
This identity and acceptance bound are exact deductions; complete finite-BIT
sampling still requires the following compiler.

## Parent finite-BIT construction to prove

Reuse the old exact unitary approximation U'=S diag(d_j) S^T. All d_j are
rational points on the unit circle approximating exp(-it lambda_j); S is the
exact sine matrix over ONE cyclotomic field of degreeO(ell), with at most one
common normalization root that cancels from U'. Binary time costs precision
O(timebits+log1eta+logell), not numerical t iterations. The approximation is
exactly unitary algebraically. On the m-particle sector its state error is
at most m||U-U'||, so approximation need not be amplified by conditioning.

Put W=diag(U',1), Z'=W Z W^T. In GROUPED Majoranas
c_odd=a+a†, c_even=i(a-a†), annihilators have coefficient matrix

    A=(I-Z', -i(I+Z'))/2,
    AA†=(I+Z'Z'†)/2 >=I/2,
    M=-i(I-2 A†(AA†)^(-1) A).

Reorder M to INTERLEAVED Majoranas. Vacuum has M_(2j-1,2j)=+1. This proposed
formula is being checked independently and in exact finite algebra.
For a k-bit occupation prefix let s_j=+1 for empty,-1 for occupied. Wick plus
the block-Pfaffian expansion proposes the JOINT probability

    P(prefix)=2^-k (prod_j s_j) Pf(M_prefix + directsum_j s_j J2),
    J2=[[0,1],[-1,0]].

Compute this directly for each prefix; do not accumulate unstable rounded
covariance updates or expand 2^k subsets. Entries, inverses, and Pfaffians
remain in one polynomial-degree field. Determinant/minor height bounds should
pay polynomial coordinate bits and nonzero algebraic separation; exact zero
and sign tests then pay conditional ratios, even for tiny prefixes. Approximate
coins at requested absolute error, cap every loop, and allocate proposal error
before O(ell^2 log1epsilon) rejection. No extra condition-number or nonzero-
probability promise is permitted. These are proof obligations, not a theorem
from an arithmetic-operation count.

## Possible coherent amplitude consequence, not yet admitted

For output y in fragment lambda and effective occupied set S, with s=m mod2,

    psi_y = c_lambda z^(-(m+s)/2) Pf(Z'_(S union spectator_if_s)).

The exponent is integer. This follows formally because projecting the original
unnormalized Gaussian gives z^((m+s)/2) times the uniform effective superposition,
and second quantization maps pairing Z to Z' with vacuum phase fixed. The
spectator is last. Cross-fragment phases c_lambda MUST be retained here; label
dephasing used for sampling is not a rule for evaluating coherent observables.
If polynomial precision and signs are proved, this may also give the existing
computationally-tractable-state additive sparse-observable interface. Do not
admit it merely because the sampler works.

## Current decisive checks and false gates

One exact Sage control, controls/folded_product/gaussian_conventions.py,
checks principal Pfaffians, covariance against direct Fock Majoranas, and every
small prefix probability for complex evolved pairing matrices. It only detects
convention mistakes. Native all-sector controls from the old pass are reused.
Independent full composition proof is underway. Claude58521 attacks native
fragment/projection/coherent-amplitude signs; OpenAI79565 attacks algebraic
height/zero/clock. Explicit packets api_inputs/2026-11-13-folded-product/;
ceilings3/4USD notcharges. PDF control characters caused local preflight
rejections BEFORE any API request; sanitized excerpts were submitted once.

Falsifiers: nonconstant physical magnetization in a label, a basis-map phase,
wrong principal Pfaffian or spectator sign, missing total-probability factor,
field-degree/coordinate growth beyond polynomial, a tiny-prefix runtime, or
an uncharged rare conditioning. No sampler/CT closure, quantum advantage,
novelty, hardness, implementation, practical runtime, arbitrary input,
inhomogeneous product, perturbation, periodic-chain or generic XXZ transfer.

## Parent exact prefix and height derivation

The finite Sage control completed/reaped90775 exit0:120principalPfaffians,
308covarianceentries,472prefixprobabilities, all exactQ(i). The first local
run84395 exited on Sage's absent matrix.copy method before prefix comparisons;
standard-library copy repaired the harness. It was not a mathematical failure.
No all-size claim follows from the finite control.

Here is the proposed all-size arithmetic proof, independently under review.
For even Gaussian covariance convention M_ab=i< c_a c_b > (a!=b), Wick gives
<prod_(j inT) i c_(2j-1)c_(2j)>=Pf(M_T). A prefix projector is the product
of(1+s_j i c_(2j-1)c_(2j))/2. Expanding the Pfaffian of M+diag(s_j J2)
groups terms by the modes paired within their own block; every such block
uses consecutive indices, so no extra cross-block sign appears. Multiplying
by prod s_j recovers the projector expansion. This proves the displayed
prefix formula without an algorithm that enumerates the expansion.

A sign-safe polynomial Pfaffian algorithm is available directly. For a2k
skew matrix B let J0=diag(J2,...,J2), so Pf(J0)=1. Compute the polynomial
D(x)=det(J0+xB) by determinant evaluation/interpolation at0,...,2k. The
polynomial q(x)=Pf(J0+xB) has degree<=k, q0=1, and q(x)^2=D(x). Hence
q_j=(D_j-sum_(i=1)^(j-1) q_i*q_(j-i))/2 constructs its coefficients and
q_k=Pf(B). The ONLY formal square root has prescribed constant1; no sign
of an ordinary complex square root is guessed. Polynomial exact determinant
arithmetic and interpolation have polynomial dimension/bit cost.

For clarity, the field does not grow with the number of modes measured.
Let d=[K:Q]=O(ell), with K=Q(zeta_(4(ell+1))). Write elements in its power
basis; coefficients of its cyclotomic polynomial are bounded by2^d because
all roots have modulus1. Reduction of products incurs at mostO(d^2) extra
coefficient bits. Each rational d_j phase uses a polynomial-bit denominator;
a common denominator for U' is their product times polynomial factors inell.
The ONE normalization root in S cancels from S diag(d_j) S^T. Forming Z', A
and AA† only multiplies/adds polynomially many such coordinates.

Inverting an L byL matrix over K can be represented as a rational linear
system of dimension Ld. Clear one common integer denominator. Cramer's rule
and the integer Hadamard bound give numerator/denominator bit bounds
O(Ld*(H+log(Ld))) for integer-entry heightH, plus the charged multiplication-
table bits. This is a constructive bound on coordinates, not an assumed
small compact expression. Standard exact rational elimination computes the
same solution in polynomial time. AA†>=I/2 ensures invertibility at the
physical embedding, hence its determinant is nonzero in the field.

For any prefix matrix, the determinant-interpolation/formal-Pfaffian route
above keeps coefficients within polynomial bit bounds. This can be seen
independently of the recurrence: each coefficient of Pf(J0+xB) is a sum of
at most(2k)! products of at mostk entries. A common denominator D_B^k works;
its coordinate height is polynomial in k,d and the input heights. Reducing
fractions after each recurrence step therefore never constructs an uncharged
expanded object. All bounds are computed from dimensions/input coordinate
bit lengths using integer arithmetic before sampling.

In particular choose an explicit positive integer D clearing each prefix
probability's coordinate denominators and an integer A>=1 bounding every
conjugate |sigma(D*P)| by the sum of its absolute integer power-basis
coefficients. Both logD and logA are polynomial. If P!=0, the algebraic
integer DP has nonzero integer norm, so

    |P| >= 1/[D*A^(d-1)].

Exact zero means all power-basis coordinates vanish. For a nonzero native
prefix, positivity follows from its projector identity; the same separation
bound pays a certified sign calculation if needed. To approximate
P(child)/P(parent) within2^-q, evaluate the two fixed-embedding field elements
to q+O(logD+dlogA) bits, divide with interval guards and clip to[0,1]. No
lower-bound promise on observed probabilities is supplied. Computing roots
of unity via certified trigonometry at these precisions is polynomial BIT.
This completes the parent's proposed tiny-prefix arithmetic argument, subject
to the independent review of its identities/field and uniform bounds.

## Paid native report and coherent amplitude simplification

Claude58521 completed, full311LF report parent-read and process reaped exit0;
usage estimate0.768200USD, notinvoice. Native moves/magnetization/connectivity,
projectedGaussian/spectator/order, normalization and prefixPfaffian derivations
were independently checked. The spectator condition is redundant given even
total parity and physicalcount=m; keeping the joint test does NOT incur a
second independent acceptance factor. Our displayed bound already uses the
correct singlejoint event.

REJECTED material source statement: report3c says Bravyi's Majorana convention
differs in sign. Actual retained PDF textLF90-110 Eq2 explicitly has
c_(2j)=(-i)(a†-a)=i(a-a†), exactly our convention. No re-signing is required.
The report's generic warning about mixing conventions is valid, but not that
source-specific assertion. The vacuum+1 control and exactQ(i) checks agree.

Accepted algebraic simplification for coherent amplitudes: use z=1, independently
of the sampler's tilted z=m/(ell-m). Let W=diag(U',1), spectatorLAST, and
R=S union{spectator} whenm isodd, elseR=S. Pfaffian minor summation gives

    Pf((W J W^T)_R)=sum_(|T|=m) det(U'_(S,T)),
    psi_y=c_lambda Pf((W J W^T)_R).

The spectator row/column forces the same spectator occupancy in every term;
its position last gives no extra sign. Every even principalPfJ=1. This is an
exact polynomial identity for every U', not an assumption of Gaussianity of
the projected Dicke state. It also covers m0 viaemptyPf1 andmell viadetU'.
Keep detU' even when the exact native full-sectorphase is1: separately rounded
one-bodyphases need not have product1. It lies in the same global error ledger.
Using a NORMALIZED Gaussian would insert a wrong label-dependent magnitude;
the formula is explicitly unnormalized. Moving the spectator's index in only
one formula would change odd-m relative signs, invisible to Born tests.

Coherent claims require the extra charged input theta=phi/(2pi) rational;
phi was irrelevant ONLY for the Born-law task. Compute
c_lambda=e(theta*Mphys)*sqrt(p^Mphys*(1-p)^(N+2-Mphys)). The squared magnitude
is an exactly computable rational ofO(N*bits(p)) bits. With U' unitary,
|sumdet|<=sqrt(binomial(ell,m))<=2^(ell/2). Therefore O(N) additional absolute
precision bits pay scalar multiplication, even when c_lambda is tiny. A
uniform per-length one-body approximation eta yields global block-diagonal
state error<=Neta: take a maximum over labels, never multiply by their number.
This gives a concrete candidate polynomial-BIT amplitude compiler and hence
possible CT readouts once the remaining finite-BIT sampler/height proof closes.
Sparse-observable estimation still costs polynomial1/error, notpolylogerror.
No general coherent-input or inhomogeneous-product transfer is admitted.

## Complete written closure and paid finite-BIT disposition

Full276LF `audits/reviews/2026-11-13-folded-product-composition.md` parent-read
and checked. It proves the native sampler AND separate amplitude compiler.
All matrix coordinate heights are charged in ONE cyclotomic field per queried
length, never an exponential compositum over all labels. A computed common
covariance denominator Q_M yields a uniform prefix denominator Q=(2Q_M)^d;
a coefficient bound gives an explicit conjugate bound A, so every nonzero
prefix exceeds1/[Q*A^(D-1)]. This pays fixed precision and exact zero tests.
Exact child-zero guards prevent rounded coins entering impossible prefixes.
Each coin uses bounded dyadic random bits; literal exact bounded sampling of
p=1/3 is impossible and is NOT claimed. Keep the original label throughout
all Gaussian retries, otherwise acceptance would bias the fragment weights.

The independent proof takes delta_U=epsilon/[64(N+2)], label coinerror
samebound, R=(N+2)^2 ceil(log2(64/epsilon)), and proposalTVnu=epsilon/(64R).
Coupling all R proposals, ideal timeout, label error and conditionalunitary
error each cost<=epsilon/64. All loops and operand lengths are polynomial
in N, input/time bits and log1epsilon. Direct m0/ell branch is exact for
Born output. The coherent compiler retains detU' in those full sectors and
uses a separately charged rational common phase theta=phi/(2pi).

OpenAI79565 completed; full302LF report parentchecked/reaped exit0,
usageestimate1.567230. Its explicit alternative bounds were checked: with
n=ell+1,c=4n,D=phi(c),kappa=8c^2, rationalphaseheight b,
h0=10n(b+kappa+ceil(log2(2n))+1), W=h0+kappa+ceil(log2(2nD))+1,
H=1000n^2DW bounds covariance and every prefix coordinate numerator/denominator.
The covariance inverse uses the common norm denominator ofdet(CC†), avoiding
an arithmetic-DAG size assumption. Polynomial determinant/Newton/formalPfaffian
calculations preserve those bounds. Its norm separation Delta=2^-L with
L=DH+(D-1)ceil(log2D)+2 is valid. This is a second checked quantitative route,
not a replacement of source assumptions with its approval label.
The report's alternative rejection error budget (proposalTVa_*epsilon/8,
conditionederror<=epsilon/4) is also valid; the independent proof's conservative
Rnu coupling already suffices. Its exactcoin and fixedlabel warnings are now
explicitly incorporated. No material finite-BIT gap remains at stated scope.

Established: for EVERY N>=2,rationalp in[0,1],binaryrationaltime t and requested
epsilonTV, this precise homogeneous-product openfolded-chain Born law has a
classical sampler inpoly(N,input/timebits,log1epsilon) BIT. With rationalturn
commonphase supplied, any requested physicaloutput amplitude has absolute
2^-p_out approximation inpoly(N,input/time/phasebits,p_out) BIT. This is a
written algorithm, not a runnable implementation or a practical resource claim.
No arbitraryquantuminput, inhomogeneousproduct, perturbation, periodicboundary,
genericXXZ, hardness, novelty, quantumadvantage or human/formal verification.
The source-based CT sparse-observable corollary is established below with an
independently checked bounded estimator retaining cross-fragment phases.

Both new paid reports terminal/fullread/reaped; roundestimated0.768200+
1.567230=2.335430USD. Nextfreeze frombalanced_kerr_round expectedcumulative
305.391228/234priced, Anth170.637018/OpenAI134.754210,7UNKNOWNexcluded;
owneractualSPENT155.99/101.71 separate. No paidretry; preflightPDFcontrolchars
made no API calls. Current proofs/source/control are now stable for freezing
after this final CT corollary disposition.

## Sparse-observable classical readout corollary

Parent read actual Van den Nest0911.1624 retained tractable_states.txt,
Definition1 LF344-365 and Theorem3/proof525-632. The new sampler and amplitude
compiler meet its CT ingredients at chargedprecision. The following direct
bounded estimator supplies an explicit finite-bit completion, independently
checked by the composition reviewer after its276LF proof.

Let n=N+2, O have norm<=B, and computable unique rowANDcolumn neighbor lists
of size<=s. Charge listing and coefficient-evaluation costs. Handle B=0 or
zero listings directly. Pad to a power of two s' in[s,2s), so neighbor choice
uses a FIXED number of fair bits. Choose a fair row/column branch: sample a
column x from p_x=|psi_x|^2 and choose one of its s' rows y, OR sample a rowy
and choose one of its s' columnsx. Padding returns a dummy with estimator0.
A real orderededge(x,y) has proposalweight(p_x+p_y)/(2s'). Use

    Z=2s'*conj(psi_y)*O_yx*psi_x/(p_x+p_y).

Its mean is exactly <psi|O|psi>, and |Z|<=s'B. Cross-fragment phases are
computed from the charged rationalturnphi and the unnormalizedPfaffian,
never dropped by the label-sampling dephasing argument.

Set tau=epsilon/[100(s'B+1)2^n]. At mosts'2^n realedges exist, so the total
proposalweight with S=p_x+p_y<=3tau is at most3*2^(n-1)*tau; suppressing that
band costs bias<3epsilon/200. Numerically suppress S_tilde<=2tau. Amplitude
and matrix-entry absolute precision at most
eta=epsilon*tau/[1000s'(B+1)] pays the threshold uncertainty and all retained-
edge ratios; no relative-accuracy or exact transcendentalcomparison oracle.
Clip the estimator to its known bound. SamplingTV<=epsilon/[100s'(B+1)]
contributes bias<=epsilon/50. All remaining numericalerrors fit a fixed
fraction ofepsilon. Required amplitude precision is O(n+log(s'(B+1)/epsilon))
bits plus chargednative bits; numerical2^n enumeration never occurs.
Hoeffding with O(max(1,s'^2 B^2/epsilon^2) log(1/failure)) IID draws completes
the additive estimate. For complex O, handle real/imaginary parts separately.
This is polynomial in1/observableerror, NOTpolylog observableerror.

Thus additive estimation for polynomially row/column-sparse bounded observables,
including arbitrary-length Pauli strings and polynomialPauli sums with charged
bounds, is also classically matched for THIS homogeneous-input openchain.
No dense-observable, relative-error, arbitraryinput, inhomogeneousproduct or
perturbation extension follows. The native quantum transform remains a
written arbitrary-quantum-input unitary result; its scope is different.
