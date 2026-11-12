# Native growing-boson condensate: a concrete qRSt classical attack

Use the full native real-time contract attached. Restrict ONLY the initial
occupation to mu=(1^D), i.e. D bosons in mode1. D grows; binary time2pi*a/c,
q=t^3,t=D/(D+1) fixed globally, full occupation output nu at TV2^-b remains
primary target. No eigenstate/coefficients advice. This input is not covered
by the fixed-k few-boson route. Quantum full transform and diagonal phases
are an admitted WRITTEN poly(D,L,b) interface; do not re-review them.

New source: Aigner--Frieden qRSt2009.03526v2 gives a positive randomized
permutation-to-pair-of-SYT growth diagram (Theorem4.25/proof), with exact
finite rational corner probabilities on0<q,t<1 (Proposition4.17). This is
the ordinary permutation qRSt, not the later dualqtRSK* or t=0 q-Whittaker.
Uniform permutation input produces shape weight
 (r_1^D/D!)*(sum_T psi_T)*(sum_T phi_T).
Parent proposed identification: if kappa_lambda=[p_1^D]P_lambda,
then sum psi_T=D!*kappa_lambda, sum phi_T=b_lambda*D!*kappa_lambda,
where Q_lambda=b_lambda P_lambda and h_lambda=1/b_lambda. Thus shape law
is D!*r_1^D*kappa_lambda^2/h_lambda, EXACTLY
|<Jhat_lambda,p_1^D/sqrt(D!*r_1^D)>|^2. Verify normalization/conventions!
These positive shape weights are a classical SPECTRAL measure, not yet the
real-time occupation law. A return amplitude is the bounded average
A(tau)=E_shape exp(-2pi*i*tau*E_lambda), with exact rational phase modulo1.
So if the source sampler has polynomial finite BIT/TV clock, return
amplitude and |A|^2 have classical additive-epsilon estimates in
poly(D,L,epsilon^-1,log(delta^-1)). No relative exponentially-small-probability
or full-output sampling follows automatically.

Primary question remains full occupation output from this simple growing-k
input. Try to use the NEW positive qRSt path representation constructively,
not just explain generic interference. Charge any pair-path weights, norms,
conditional probabilities, inverse map, rejection and variance. Generic
p(D) enumeration already supplies exp(O(sqrt D))*poly(D,L,b). Finite examples
can only falsify. No novelty, general hardness, or quantum speedup assumed.

## Source and task status

Corpus been-tried and baselines ran before selection. Parent read actual
qRSt Theorem4.25 proof, finite positive probability formula Proposition4.17/
Remark4.18, growth diagram Definition4.24 and squarefree Cauchy identity.
The proposed spectral measure identification uses only squarefree monomials
and orthogonality. Two distinct paid obligations are prepared under
audits/api_inputs/2026-11-13-condensate/dispatch.json (ceilings11USD, not
charges): finite native spectral/return clock, and full coherent sampler.
No general classical sampler or advantage inferred from a source citation.

## Terminal reports and new paired-growth deduction

Both reports completed and fully parent-read (Claude252LF/OAI492LF).
Core spectral identity verified; actual full Theorem4.25/Lemma4.26 and
Proposition4.17 proof checked. Use exact rational local factors and a
bounded-bit CDF for poly(D,b), not the unverified tight fixed-point exponent.
Claude's unnormalized k-annihilation correlator has prefactor sqrt((D)_k);
only its NORMALIZED version has uniform bounded additive-estimation cost.

OAI adds a constructive conditional-pair source missing in Claude: qRSt's
joint tableau law (r1^n/n!)*psi_P*phi_Q, with phi_Q=b_eta*psi_Q, makes P,Q
independent given common shape eta, with the same psi-normalized law.
Independently extend each tableau by uniform-rank insertion, using actual
primary Definition4.28 and its following equivalence to growth diagrams
(LF1894–1945 parent-read). The shape kernel is
 K(eta,lambda)=r1*phi_(lambda/eta)*kappa_lambda/kappa_eta,
but no ratio is evaluated. Sample n=D-j initial qRSt and extend both to D;
all auxiliary degrees retain ORIGINAL q=t^3,t=D/(D+1).
Then s_j=< (N1)_j>/(D)_j is the expectation of
 exp[-2pi*i*tau*(E_lambda-E_rho)], modulus1. This pays additive estimates
in poly(D,L,epsilon^-1,log1/delta) for every j, including <N1>/D.
CLOSED WRITTEN after parent checked the complete323LF independent audit
audits/reviews/2026-11-13-condensate-spectral-independent.md. The averaged
pair law is paid; conditioning on an arbitrary externally supplied shape is
NOT supplied. No speedup, novelty or whole-distribution claim.

Full N1 law still needs alternating binomial contractions:
 P(N1=m)=binom(D,m)*sum_r (-1)^r binom(D-m,r)*s_(m+r).
Single-index raw complex phase importance sampling of P(N1=0) has second
moment sum_j binom(D,j)^2/w_j>=4^D. This is an exact failure of THAT raw
estimator, not a general lower bound, and variance alone does not prove a
necessary number of samples for every alternative estimator. At zero time
cancellation is analytically trivial. Moment inversion's l1 sensitivity
bound3^D gives only a sufficient precision requirement for naive inversion.
No full-mode sampler or generic hardness follows. D2 coherence falsifier
matches already retained formula133/169*sin²(1235*pi*tau/192); no new sweep.

## Reviewed precise clock and claim boundary

Independent323LF audit parent-checked in full. At most3D²+3D categorical
choices (growth plus rank insertion) have<=D+1 alternatives; exact CDFs
have O(D³log(D+1)) bits. A fresh B=b+ceil(log2(64(D+1)^4)) bit threshold
at each choice bounds the complete adaptive joint-law TV by2^-b. No
relative conditioning on rare shapes or coefficient oracle is used.
Eigenphase differences are reduced modulo1 exactly; additive epsilon
estimation uses O(epsilon^-2 log(1/delta)) independent bounded trials.
The qRSt pair's factorization and insertion locality close all normalized
mode1 factorial moments, including growing j, at SAME global parameters.
Full mode1 distribution and full occupation sampling remain OPEN.

## Next decisive constructive tests (13 November)

One final paired-projector/Gaussian round runs under
api_inputs/2026-11-13-condensate-projector/dispatch.json: TWO new obligations,
11USD ceilings notcharges. Coupled-all-j qRSt projection targets a FULL
mode1 count sampler with paid conditionals/variance/precision. Separate
Gaussian/pump hypothesis targets the SAME full occupation law at tau=uD:
Poisson mode2 mean54*pi²*u², n1=D-2n2, with explicit finite-D TV/error clock.
This is a conjecture, not a consequence of spectral moments or finite fits.
Do not import finite-particle BEC theorems into Hall-Fock. If no uniform
sampler follows, park this line rather than requesting nearby variants.

Parent exact first-column deduction (independent check requested): write
v=q^-1-1,sigma=(1-t)v, and define L_(D-M)^(M)(-sigma) explicitly by
sum_(l=0)^(D-M) binom(D,M+l)*sigma^l/l!. For output occupation with
m_k for k>=2 and excitation massM=sum k*m_k, the native matrix element
from the condensate is
 v^M L_(D-M)^(M)(-sigma)/(1-t)
 *prod_(k>=2) (1-t^k)^m_k/(k^m_k*m_k!)
 *sqrt(prod_(k>=2)k^m_k*m_k!*r_k^m_k / ((D)_M*r1^M)).
The M0 diagonal instead excludes n0: h_D=[L_D(-sigma)-1]/(1-t).
This follows directly from V_n^*p1^D=binom(D,n)(1-q)^n p1^(D-n),
then the actual positive vertex exponential. The mode2one amplitude obeys
D*A_D ->(3/2)sqrt6 and h_D=3+21/(4D)+O(D^-2); these are initial-generator
checks, NOT finite-time convergence or a sampler. Higher-mode grouped
squared coefficients use [z^M]exp(sum_(k>=2)(1-t^k)^2*r_k*z^k/k).
A full dynamical tail/Duhamel bound is unpaid. No quantum implementation.

## Finite-time Gaussian proof proposal: under independent audit

Parent hard derivation,13November; NOT yet promoted. Define c_k=(1-t^k)
*sqrt(r_k/k)*q^(-k/2)<=8sqrt(k)/D for1<=k<=D. Then H=(1-t)^-1
[CT_z exp(sum c_k a_k^dag z^k) exp(sum c_k a_k z^-k)-I]. On input
|D-2r,r_2>, grade pump terms by xi and all k>=2 terms by xi^2.
Take |z|=1/2, |xi|=sqrt(D)/(r+1)^(1/4). Creation norm estimate
||exp(x a^dag)|n>||<=exp(|x|^2/2+|x|sqrt(n)), plus the annihilation
triangle bound, gives proposed uniform vector bound exp(84). ForD>=16,
Cauchy's grade>=5 remainder is <=2exp(84)(r+1)^(5/4)D^(-5/2).
Multiplication byD/(1-t) makes it O((r+1)^(5/4)/sqrt(D)).

Grades1,3 vanish. Grades2,4 on this column are exactly
v*n1+d2*n2+d11*n1(n1-1)+gD*(a2^dag*a1^2+h.c.), where
v=q^-1-1,d2=(1+t)(q^-2-1)/2,d11=(1-t)*v^2/4,
gD=c1^2*c2/[2(1-t)]. Subtract exact h_D, not only its expansion.
D(d2-2v)r and the quartic-pump diagonal difference are O(r/D).
D^2*gD tends kappa=(3/2)sqrt6 with O(1/D) error; pump depletion
changes offdiagonal coefficients by O((r+1)^(3/2)/D).
Proposed all-column estimate, including upper boundary R=floor(D/2):
||D(H-h_D)J_D|r>-J_D*kappa*(b+b^dag)|r>||
 <=C(r+1)^2/sqrt(D),0<=r<=R, with explicit universalC.
J_D kills r>R and maps retained r to physical |D-2r,r_2>.

Duhamel compares exp[-isD(H-h_D)]Omega with J_D*exp[-is*kappa(b+b^dag)]|0>.
The latter coherent coefficients have Poisson mean lambda=kappa^2*s^2.
Weighted Cauchy bounds sum |c_r|(r+1)^2 by
sqrt(sum(r+1)^-2)*sqrt(E_Poisson[(r+1)^6])<=C(1+lambda)^3.
The sole omitted-source boundary r=R+1 is likewise bounded by the sixth
moment. Integration suggests state norm error <=C|s|(1+s^2)^3/sqrt(D).
The discarded coherent tail is bounded by the sixth moment; send overflow
to the legal condensate output. With s=2pi*u, proposed full occupation
TV bound <=C(1+|u|)^7/sqrt(D), Poisson n2 mean54pi^2*u^2,n1=D-2n2.
Finite-bit Poisson/CDF approximation adds its separately paid error.

Audit must verify the analytic vector bound with finite-degree projection,
low-grade identities, global column/boundary norm, explicit constants and
Duhamel clock. Even if closed, this only gives a finiteD/time/precision
window, e.g.7gamma+c<1/2 foru<=D^gamma,errorD^-c. It does NOT settle
arbitrary binary time, arbitrary precision, or general full-output sampling.
No novelty, hardness, useful quantum advantage or finite-example inference.

## Coupled-projector report: terminal, scoped falsifier under verification

OpenAI coupled-projector report completed and fully parent-read; Claude
Gaussian-clock report truncated EMPTY at64000 output tokens, no retry or
mathematical finding. Common sequential qRSt primary history plus a shared
independent secondary insertion stream pays all-j joint source in polynomial
BIT. It does NOT pay signed-vector variance. Report's exact native D3
control,t3/4,q27/64,tau157464/37, proposes phases row=mixed=-column and
sample vector(-4,6,0,-1) on the positive event eta2=row,rho0=column.
Conditioning on primary history still gives negative P(N1=0) estimator
-4*pi3(column); square-conditional-amplitude repair gives -8r(1-r).
Verify eigenphase fractions with exact Sage before accepting. This would
refute these positivity constructions only; cross-primary contractions and
polynomial variance remain OPEN. No more adjacent static paid batch selected.

## Final reviewed disposition: restricted full-output baseline CLOSED

Parent read the full339LF independent pump proof and all of the completed
coupled-projector report. Exact D3 Sage control has13 assertions: eigenphase
gaps28394,21087/2 and signed projection(-4,6,0,-1). The common-stream
joint-law, positive event and conditional negative contractions were checked
analytically, not inferred from that control. Thus the fixed-primary-history
positive projection and square-conditional-amplitude repairs are REFUTED;
no general variance bound or classical hardness follows.

Pump theorem CLOSED WRITTEN: for every integerD>=1 and realu, the original
full occupation distribution at tau=uD is within
 min(1,2^40*exp(84)*(1+abs(u))^7/sqrt(D))
of Poisson n2 with mean54*pi^2*u^2, n1=D-2n2, overflow mapped to condensate.
The exact native CT operator, Weyl-displacement norm bound, low-grade
coefficients, uniform full-output columns and both pump boundaries are paid.
The finite-bit CDF sampler adds its allocated error and has polynomial cost
in numericalD,inputbits and precisionbits in a polynomially bounded u window.
The displayed approximation bound must ALSO meet the requested error; this
is not arbitrary-b or arbitrary-binary-time sampling. Huge constants have
no practical meaning. No implementation, novelty or quantum advantage.

Terminal2job increment3.012588USD (Anth1.361168,OAI1.651420), cumulative
249.179788USD/193priced records(Anth149.085718,OAI100.094070),FOURUNKNOWN
excluded. Estimates not invoices/balances. Claude EMPTY truncation supplies
no finding and was not retried. Prepared ledger in controls/condensate_projector_round;
stable proof/report/control hashes are being frozen once. This closes this
static line's present constructive round; priority pivots to the independently
selected exact sparse-wave endpoint, not another nearby asymptotic variant.
