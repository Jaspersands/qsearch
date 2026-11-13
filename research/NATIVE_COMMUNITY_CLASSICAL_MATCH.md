# Native community classical attack: log-free detection

2026-11-13. CLOSED WRITTEN native log-free classical detection theorem.
The earlier proposed route is retained below as derivation context; the direct
trace proof and terminal disposition at the end supersede its pending labels.
Start STATE/TRAPS; prior corpus been-tried/baselines then actual 2026 primary
sources checked. This is the single decisive classical comparison before
extending the repaired quantum detector. No quantum implementation.

## Problem, mechanism, resources and falsifiers

SAME explicit input as NATIVE_COMMUNITY_SOURCE_REPAIR.md: fixed even p>=4,
k>=3, fixed rational q bounded away from0 (q=1/4), one observed bit for every
p-subset, conditional means q+epsilon*f_x(E), known rational epsilon, hidden
uniform community labels. Null iid Bern(q). No labels or extra planted data.
Goal: strong classical detection with beta=epsilon/sqrt(q(1-q)) at
beta>=C_pk*n^(-p/4)*ell^((2-p)/4), ell->infinity, ell=o(sqrt n), in
n^(ell+O_p(1))*poly(B) BIT time. This removes the sqrt(logn) in the repaired
quantum threshold. At p4,beta~1/(n sqrtlogn), it would use ell=O(logn),
beating that quantum upper bound's ell=Theta(log²n).
This is a comparison of actual upper bounds, not a lower bound on quantum
algorithms or any claim about the best possible speedup.

Mechanism: add fresh NULL noise to obtain symmetric ternary observations,
use a sharp Kikuchi trace bound on the slice, and detect a positive signal
with repeated classical matrix powers. All n^p source bits, fresh randomness,
slice-vector storage and arithmetic are charged. Existing baselines include
unnormalized Kikuchi, the normalized 2026 method, and HCE; their actual model
transfer is being checked. Source: Schmidhuber--Hastings2607.29672v1,
Theorem5.3 and sections4--6, in audits/sources/2026-11-13-community-baselines/.

## Actual randomized classical operation

For every edge generate independent Z_E~Bern(q), and set X_E=Y_E-Z_E.
Under NULL the support {E:X_E!=0} is an iid Bern(2q(1-q)) subset; conditional
on this support, all nonzero signs are independent unbiased Rademachers.
Under PLANTING the X_E remain independent conditional on labels, with mean
epsilon*f_x(E) and variance<=1. There is no second planted graph.
Fixed-bit Bernoulli sampling with O(log(M/eta)) bits per draw gives total
TV<=eta; q=1/4 can be generated exactly in two bits per edge.

Write d=p/2, N=binom(n,ell), and
D=binom(ell,d)*binom(n-ell,d). On ell-subsets let A_E(S,T)=1[S triangle T=E].
Let P_E=A_E² and A=sum_E X_E A_E. For every row sum_E P_E=D, exactly.
Algorithmically A is a sparse INTEGER matrix with at most D neighbors.

## Crucial trace extension being independently checked

Condition under NULL on m nonzero observations. Their supports form a uniform
m-subset, which can be ordered by an independent random permutation of its
members. Signs stay independent. The primary Theorem5.3 has iid uniform
supports or a Poisson family, so its theorem statement is NOT directly
applicable. Its branchwise proof may extend as follows.

After a exposed distinct supports, the remaining supports are uniformly
sampled without replacement. Their expected fresh mass legal at the current
row is at most (m-a)/(M-a) times the number of legal remaining supports,
which is <=D. Supports recycling h exposed exterior vertices have mass at
most C_p*D*(C_p*t/n)^h by the same elementary slot count. Exposed sets have
O_p(t) vertices. Choose deterministic floor d_floor=D. Every denominator in
Gamma=sum_E |X_E|P_E+D*I is between D and2D, on EVERY input. The primary
chronology and active-label bounds then appear to apply unchanged, yielding

 ||Gamma^(-1/2) A Gamma^(-1/2)||<=C_p sqrt(ell/D)

with probability1-o(1) for t_trace=Theta(ell logn), ell logn<=n^(1-delta).
Consequently ||A||<=2C_p sqrt(D*ell). NO normalization needs to be computed
by the algorithm. An unproved dependence/chronology identity at this step
would block the claimed classical theorem; a printed ACCEPT label cannot
replace checking it. Conditional sampling never reveals absent observations
or makes unsupported claims about one common filtration for all branches.

## Planted witness avoids the Boolean-gauge assumption

Use ONE community vector w_c(i)=1[x_i=c]-1/k. Its tensor power w_c^tensor ell
is fully symmetric, unlike the earlier block certificate. The PSD lift
from the repaired source proof has expectation
binom(ell,d)*sum_a <w_c,w_a>^p/||w_c||^p
>=binom(ell,d)*||w_c||^p>=c_pk*n^d*ell^d.
Collision projection has normalized error O_pk(ell/sqrt n), because every
coordinate weight w_c(i)^2/||w_c||² is O_pk(1/n).
The ordered mean differs from the projected PSD lift by O(n^(d-1)ell^d).
The fully symmetric ordered subspace compresses ordered K to d!*A. Thus
there is a unit SLICE witness v, depending only on labels in this analysis,
with E[v^T A v|x]>=c_pk*epsilon*D, uniformly over label vectors.
No algorithm receives the witness or labels.

For a_E=v^T A_E v, |a_E|<=v^T P_E v<=1. Therefore
Var(v^T A v|x)<=sum_E a_E²<=sum_E v^T P_E v=D.
At epsilon²D>=C_pk*ell and growing ell, Chebyshev yields planted Rayleigh
>=c_pk*epsilon*D/2 with failure O(1/ell). Choose C_pk so the proposed null
norm bound is at most one quarter of this planted signal s. This gives a
constant multiplicative detection gap, conditional on the trace extension.

## Explicit finite BIT spectral test

Use random Rademacher vectors r in {+1,-1}^N. For a fixed unit top eigenvector
v_top, E(v_top dot r)²=1 and E(v_top dot r)^4<=3; Paley--Zygmund gives
Pr(|v_top dot r|>=1/sqrt2)>=1/12. Under planting with eigenvalue>=s,
||A^j r||>=s^j/sqrt2 with that probability. Under the null bound s/4,
||A^j r||<=(s/4)^j sqrtN. Choose j=O(logN) to separate these, repeat O(logn)
times and compare exact squared integer norms against a rational threshold.
Sparse integer matrix-vector multiplication costs N*poly(n^p,ell) operations;
bit lengths grow by at most O(j logD) plus input threshold bits. No spectral
oracle, eigenvector loading, QRAM, free inverse or approximate-real arithmetic
is needed. The output is one bit. Statistical/input-rounding errors add.

## Status and next command

The positive mean and scalar variance arguments are parent derivations.
The indispensable without-replacement trace extension is under independent
review in audits/reviews/2026-11-13-community-native-classical-match.md.
Two paid independent attacks run via
api_inputs/2026-11-13-community-baseline-attack/dispatch.json (normalized
trace adaptation; HCE cycle contractions). Read only terminal/stable reports.
Acceptance requires the full branchwise proof and correct growing-order
quantifiers; any failed adaptation is only a scoped failure, never hardness.
If the theorem closes, record this actual classical upper bound and retire
the repaired quantum parameter window before selecting a different direction.


## Subsequent stronger parent/independent derivation

The proposed randomized X=Y-Z algorithm is unnecessary. For ANY deterministic
support subset and bounded coefficients u_E, independent Rademacher signs
leave only even-edge trace words. Each such length2t word has exactly t
openings and t closings. At a fixed chronology: old openings have <=D
choices; a first-use opening recycling h exterior vertices has at most
C_p D(C_p t/n)^h choices; each closing has <=(ell+2chi)/d choices by the
exact active-label parity-incidence bound (primary Lemma5.1). Chronologies
cost C_p^t2^chi (Lemma5.2). Hence the UNNORMALIZED moment satisfies

 E_sigma Tr(sum_E sigma_E u_E A_E)^(2t)
 <= N*(C_p D ell)^t*sum_chi(C_p t/n)^chi*(1+2chi/ell)^t.

At t=c ell logn with small fixed c and ell=o(sqrt n), the sum is bounded by2.
Markov gives norm<=C_p sqrt(Dell) with probability1-o(1). This is a direct
deterministic combinatorial count, with NO random-support/normalizer transfer.
For independent Bernoulli coordinates at arbitrary conditional biases,
analysis-only copies Y' give (Y-Y')=sigma*u with u in{0,1} independent of
sigma. Convexity of Tr(H^(2t)) (Schatten norm power) then transfers the bound
to the centered original matrix, uniformly conditional on ANY labels.
The algorithm therefore uses ORIGINAL Y-q, with no extra observed sample.

The paid Claude sharp-classical report completed, was fully parent-read
(12473 bytes) and reaped. Its independent deterministic-support trace and
symmetrization agree with this derivation. Its explicit small finite-n
Rayleigh constants are not imported; the independently checked all-label
pure-community certificate supplies the signal. Its asymptotic comparison
applies to the previously recorded log²n quantum clock only.

There is an immediate ordered-matrix extension: each set transition has d!
ordered lifts. Pay (d!)^(2t) per trace and the initial ordered row count,
which only changes the fixed-p norm constant. The same log-free bound can
therefore REPLACE Bernstein in the already paid native quantum compiler.
At beta threshold without sqrtlog, t_clone=1/L, h=t_clone*beta, source exponent
M*t_clone²*beta^4=O(ell^(2-p)/L²), and covariance parameter
lambda²/(h²M)=O(ell^(d+1)*L²/n^d), both vanish for polylog ell. All loading,
filter, inverse, and precision charges are unchanged. Thus the quantum
construction can also use ell~logn at beta~1/(n sqrtlogn). The older clock
is obsolete; no dominance over all quantum algorithms follows. This is
proof reuse, not a new subsystem or a claim of a new quantum advantage.
Full independent writeup pending stable-file signal; no tests or API retries.


## Terminal proof disposition and admitted theorem

Parent read and checked all 334 lines of the independent proof
`audits/reviews/2026-11-13-community-native-classical-match.md`. The exact
admitted result is: for fixed even p=2d>=4, k>=3, d<=ell=o(sqrt n), and the
native explicit independent Bernoulli input, there is a classical finite-BIT
detector of cost n^(ell+O_p(1))*poly(B) whenever epsilon²D>=C_(p,k)*ell,
D=binom(ell,d)binom(n-ell,d). Its error is O(n^-4)+2n^(-2ell). The signal
statement is uniform over EVERY fixed label vector. At fixed q this is
beta>=C_(p,k,q)n^(-p/4)ell^((2-p)/4). There is no sparse-q normalized-SNR
extension. The detector uses original Y-q, not an additional statistical
sample. No label, matrix, spectral or factoring oracle is granted.

The full proof pays deterministic-support moment counting (constant18,
fresh h bound D(2d²t/n)^h), t=floor(ell ln n/64), Schatten moment Jensen,
all-label fully symmetric pure-community witness, and exact integer power
iteration. One explicit loose norm constant is2^300; all sufficient-n
conditions are scalar inequalities depending on fixed p,k. This is a
written asymptotic theorem, not a numerical/practical claim.

The independently checked ordered-lift corollary changes the norm constant
by only d!. Substitution into the existing native quantum compiler removes
its sqrtlog threshold loss too. At ell=Theta(logn), its full charged upper
bound remains n^(ell/4)exp(O_(p,k)(ell logell))poly(n^p,B); at other polylog
orders retain O(ell(logell+loglogn)) in the subleading exponent. The older
quantum ell~log²n bound is superseded at the same p4 beta~1/(n sqrtlogn).
Neither lower bounds nor matched sufficient constants were proved. No new
quantum advantage, novelty, recovery, implementation or Shor-level claim.

### Independent HCE attack also closes a scoped classical bound

Parent fully read and checked the terminal OpenAI cycle report (13451 bytes).
It gives a DIFFERENT explicit classical detector, at p4,k3,q1/4. Sum the
squarefree edge monomials over connected degree-two covers with l edges
and2l vertices. A regular-triangle fourth-moment identity expresses the
native f as1/54 times its three pairings. Therefore each cover's label
contraction is54^(-l)sum_(3^l pairings)2^(number of circuits)>=18^(-l),
rather than assuming the Boolean XOR mean. No label oracle is used.

The exact cover count is (n)_(2l) P_l/(l!24^l), with P_l the loopless
connected pairings of4l halfedges. Uniform estimates give
N_l>=c*g_l*n^(2l), g_l=(4l-1)!!/(l!24^l), g_l/g_(l-1)>=l/8.
A proper shared set of s edges has a nonempty even boundary u>=2 by
connectedness, yielding overlap-pair fraction
<=4l/(c*n)*8^s/(s!*n^(2s)). Edge-disjoint but vertex-intersecting pairs
are NOT assumed independent; their fraction is at most4l²/n.

Let D_sig=beta²n²l. The verified relative planted variance is bounded by

 16^l*[4l²/n +4l/(c*n)*(exp(324/(beta²n²))-1)]
       +(1/c)*(5184e/D_sig)^l.

For even l->infinity, l<=ln(n)/8, and D_sig>=2^15, this is
O(l²*n^(-5/8)+2^(-l)); the null variance is exactly N_l. Direct enumeration
costs (n^4+n^(2l)exp(O(l logl)))*poly(B,l,logn), with polynomial storage.
At beta=C/(n sqrtlogn), C>=1024 fixed, this is exp(O(log²n)). The input
coefficients are (4Y-1)/sqrt3; even l permits exact integer accumulation
and a rational comparison, so no precision oracle is hidden.

This independent result includes shared-label covariance and uniform
GROWING-order counting, which the printed fixed-order XOR theorem did not
supply for this input. Its narrower sufficient-C/l scope is preserved;
no claim for arbitrary labels, every positive C, or l~log²n is admitted.
It reinforces the old-clock counter-baseline, not dominance over the
trace-sharpened quantum construction. No HCE implementation is queued.

## Next scientific action

This line now has a repaired, fully paid detection mechanism and two concrete
classical baselines. It offers no Shor-level candidate. Do not spend another
pass on recovery, sparse-q variants or benchmark infrastructure by inertia.
Compare independent high-upside hypotheses by external value, with corpus
lookup then actual primary checks, before choosing a new constructive gate.
Independent post-community selection is in progress; no new family is yet
admitted. The next command is to read its STABLE selection note and inspect
only the primary statements needed to accept or kill its best operation.
