# Binary-Fock Kerr circuits: prior-art endpoint and classical branch attack

7 November2026. CLOSED written quantum/classical composition with three
independent reviews read by the parent. Quantum endpoint is known prior art.
The bounded-branch bunched-input classical sampler is a written theorem,
not an implemented or executed sampler; exact finite controls are separate.

## Question, selection and native model

The question is whether binary-large occupation and a few non-Gaussian Kerr
phases give a sampling advantage after all access, cutoff and classical
baselines are charged. This is an end-to-end count-sampling problem, not a
new optical backend or a quantum-state preparation oracle.

Take0<epsilon<=1/4 without loss of generality. Input: m modes, binary nonnegative occupations n_i with total K, an explicit
list of L gates, and requested TV error epsilon. A gate is a two-mode passive
beam splitter B(theta)=exp(theta(a†b-b†a)), a number phase, or local Kerr
K_{a/b}=exp(2pi i (a/b) binom(n,2)), with rational angles in turns, binary
numerators/positive denominators. The desired output is one photon-count
vector distributed within epsilon of the ideal circuit. All input/angle
bits, list length, m and output m log(K+1) bits are charged. A stronger
unitary statement concerns arbitrary reference-entangled input of total K.
No squeezed/displaced input, loss, preparation oracle or binary-compressed
repeat count is included. L is the ACTUAL listed gate count.

The mechanism is common-grid quantum Hermite transforms around passive
optical operations, plus reversible modular arithmetic for Kerr phases.
Expected quantum target: poly(native bits, log(K+1), log(L/epsilon)) gates.
That target is already claimed by Prakash etal2610.03581v1 Corollary2.3:
this is PRIOR ART, not a new algorithm. The narrower number-conserving proof
below makes its native cutoff and coherent phase contract concrete.
No novelty, quantum/classical separation, practicality or execution claimed.

Before selection, corpus been-tried/baselines and actual primary literature
were checked for binary-spin/Krawtchouk, binary-Fock Kerr and bunched revival
sampling. The baseline catalog's irrelevant SDP hit is not a scientific
comparator. Current sparse-constant relations, growing-rank surface readout
and Gaudin-gap routes were independently compared: no paid constant map,
succinct cover readout or quantitative physical gap operation emerged.
A fixed-spectrum Cauchy Lax matrix admits spurious non-Bethe vectors and
therefore does not supply the Gaudin gap; no physical gap counterexample.

Strong classical comparators: explicit Fock evolution/permanent sampling,
small tensor width, Gaussian-positive-Wigner methods only on their genuine
state/measurement domain, bunched passive multinomial sampling, terminal
number-diagonal phases, and the coherent finite-branch sampler proved below.
A large bosonic Hilbert space is not evidence of hardness. Kerr Fourier
branches are coherent and cannot simply be classically mixed.

## 1. Paid known quantum endpoint

Actual sources retained under audits/sources/binary_fock_kerr/:
Iyer2602.15180v1 Lemma3.1, Theorem4.2 and its phase/label-erasure proof;
Prakash2610.03581v1 Theorems2.1/2.2 and Corollary2.3. Their PDFs, text and
SHA256 manifests are separate. This is a source-based written construction,
not independent execution of QHT or an independently implemented circuit.

Use one two-mode product QHT and operational grid for all local pair totals
at most K. Iyer Lemma3.1 uses the same discrete quadratic-chirp unitary on
each Fock input, with exponentially small grid error. Its proof accounts
for the high-energy intermediate SHEARS: only the complete beam splitter
conserves number, so a naive K truncation of every shear is invalid.
Theorem4.2 explicitly maps arbitrary superpositions and fixes Hermite phase
+1, then erases the occupation workspace coherently. Thus there is no
measurement or arbitrary fixed-spin-dependent phase. Source sign convention
requires exp(-2i theta A_12); Prakash BSY has the opposite sign.

There are d=(K+1)(K+2)/2 triangular two-mode input basis states. A common
per-column grid error delta gives restricted operator error<=sqrt(d)delta,
so delta=O(eta/(K+1)) pays all superpositions and references. Uniform QHT
operator errors telescope separately. The required grid size is polynomial
in K and1/eta, so its qubit count and the source gate cost remain polynomial
in log(K+1),log(1/eta). Choose one sufficiently padded cutoff/grid per gate.
If using the WHOLE rectangle n_a,n_b<=K, the inverse needs cutoff2K+1;
the native fixed-global-K proof only needs the triangle and cutoffK+1.

The original Hermite2510.04929 Theorem19 and Lemmas25--27 explicitly cover
coherent superpositions, a common amplification polynomial and degree-label
erasure. Pad its effective cutoff N_eff>=max(K+1,C log1/eta) to respect
N>log1/eta. Where the source bounds a squared tail bytau, use internal
tau=O(eta²). Both choices keep grid size polynomial and gate cost logarithmic
inK and1/eta. Its temporarily dropped(-1)^n Hermite convention must be
restored if needed; product parity commutes with a number-conserving mixer.

Reduce beam-splitter angles modulo2pi, never modulo pi while dropping
B(theta+pi)=(-1)^(n_a+n_b)B(theta). Local pair totals can be coherently
superposed even at fixed GLOBAL totalK. Number phases and Kerr phases are
computed by binary arithmetic; compute a*binom(n,2) mod b exactly, synthesize
the rational phase to eta and uncompute work. Exact modular arithmetic does
not mean arbitrary-angle synthesis is exact. All angle BIT lengths count.

Per-stage clean-isometry error O(epsilon/L) yields full errorO(epsilon) by
hybrid telescoping along the ideal total-K trajectory. Earlier digital
leakage is included in this operator error; no postselection or conditional
renormalization. Number measurement contracts trace distance. Map an invalid
padding tuple deterministically to the original valid input tuple; since
the ideal output is valid, this does not increase TV error. Initial binary
Fock preparation/output costO(m log(K+1)). K0 is trivial vacuum.

## 2. Exact interference and universality scope controls

Let K_pi(n)=exp(pi i binom(n,2)). It is1 on n0,1 and-1 on n2. For a balanced
B, the operation C=B†(K_pi tensor K_pi)B acts on the pair input states
00,10,01,11 as diag(1,1,1,-1), with zero leakage. In the two-photon sector
B|11> is a NOON state supported on20,02; both terms acquire-1. Total0/1
are unchanged. Apply this gadget between selected rails of two dual-rail
qubits. Native passive single-qubit rotations/phases plus this exact CZ
contain the usual universal gate set. Thus a general efficient classical
constant-TV sampler would simulate BQP sampling (and BQP decision with a
fixed sufficient error margin). This is a known-universality implication,
not proof BPP!=BQP, sampling hardness, novelty or an exponential separation.
It already uses small occupations and does not arise from high K alone.

For K_pi, period4 Fourier coefficients are
    c=(0,(1-i)/2,0,(1+i)/2),
    K_pi(n)=sum_r c_r exp(2pi i r n/4).
An exact two-photon witness is
    |20> -> B(pi/4) -> K_pi on modea -> B(pi/8)†.
Its output is -|11>, hence counts(0,1,0) in basis(02,11,20). The incoherent
Fourier mixture instead has probabilities(1/4,1/2,1/4), TVdistance1/2.
A spectator-mode control keeps globaltotal1 while pairtotals0,1 are
superposed; reducing B(pi) toidentity makes the two final states orthogonal.

These identities are frozen in audits/controls/binary_fock_kerr/control.py
and result.json using exact Sage algebraic arithmetic. They do not execute
QHT, prove the large-K gate bound or establish complexity separation.

## 3. Constructive classical branch sampler

Restrict only this CLASSICAL theorem to a bunched input |K,0,...,0> (the
occupied mode can be specified). Keep arbitrary passive gates and rational
Kerr gates. For Kerr j choose q_j=2b_j after fraction reduction; an identity
phase may useq_j1. The exact period dividesq_j. Fourier expansion gives

    K_j(n)=sum_(r<q_j) c_jr exp(2pi i r n/q_j),
    c_jr=q_j^-1 sum_(u<q_j) K_j(u) exp(-2pi i r u/q_j),
    sum_r |c_jr|²=1.

After expanding t Kerr gates there are chi=product_j q_j indexed branches.
Each branch is an ordinary passive interferometer U_r with coefficientc_r,
where sum_r |c_r|²=1 even if some branches coincide. The actual state is
Phi=sum_r c_r psi_r and has norm1 because the original circuit is unitary.
Here psi_r is a normalized bosonic condensate with one-particle vector
alpha_r=U_r e_input. Its count amplitude is exactly

    psi_r(x)=sqrt(K!/product_i x_i!) product_i alpha_ri^(x_i), sum_i x_i=K.

Its probabilities are multinomial, efficiently sampled by m-1 BINOMIAL
samples with binary totals. Its complex amplitude, including signs/phases,
can be evaluated to polynomial requested BIT precision with logfactorials
and binary angle multiplication; it is not a permanent of sizeK.

Choose a branch uniformly from the chi indices, then sample x from its
multinomial law. The proposal is p(x)=S(x)/chi, S=sum_r |psi_r(x)|². Accept
with probability
    A(x)=|sum_r c_r psi_r(x)|²/S(x).
Cauchy-Schwarz and sum|c|²1 imply0<=A<=1. The accepted distribution is
EXACTLY the desired count law, with acceptanceprobability1/chi. This
retains interference; it is not the incorrect Fourier mixture in section2.
Finite numerical normalization is paid below. Runtime polynomial in chi,
m,L, nativebitlength,log(K+1),log(1/epsilon); hence polynomial in nativebits
when chi is polynomial. An exponentially large chi is charged, not ignored.
Constantly many low-denominator Kerr phases are a natural covered case.
The universality gadget has chi exponential in the number of nonlinear gates,
so this classical theorem does not dequantize all native circuits.

### 3a. Binary binomial sampler with a finite clock

For N in binary, rational p=a/b in[0,1], and TV tolerance0<delta<=1/4,
treat N0 and p0,1 separately. Set mu=Np, v=Np(1-p), and integer
t=ceil(log2(8/delta)). Use w=isqrt(ceil(2vt))+1 and integer radius
r=w+ceil(2t/3). The interval I=[ceil(mu-r),floor(mu+r)] intersect[0,N]
has tail probability<=2exp(-t)<=delta/4 by Bernstein's inequality.
Its length J<=2sqrt(2vt)+4t/3+7. All endpoint arithmetic is rational/integer.

A degree-independent envelope follows directly from Fourier inversion:
|1-p+pe^(iu)|^N <=exp(-2v sin²(u/2))<=exp(-2v u²/pi²), |u|<=pi.
Thus max_k BinPMF(k)<=sqrt(pi)/(2sqrt(2v))<1/sqrt(v), and also<=1.
Let d=isqrt(N*a*(b-a))>=1, M=min(1,b/d). This is a certified rational
UPPER envelope, withinfactor2 of min(1,1/sqrt(v)); J*M<=16t. No clipping
of a genuinely excessive PMF ratio is hidden here.

Use a SINGLE clock: in each round draw h=ceil(log2J) fair bits, discard
j>=J, otherwise propose k=I_min+j and accept with probability
q(k)=BinPMF(k)/M. The exact round success probability is
P(I)/(2^h M)>=3/(8JM)>=3/(128t). Compute a clipped dyadic q_tilde with
absolute error<=e=delta/(64t). Then round success>=1/(64t).
Run R_bin=ceil(64t*ceil(log2(4/delta))) rounds, output floor(mu) on timeout.
The timeout probability<=delta/4. Conditional on success, normalized
q_tilde differs from normalizedq by TV<=JM*e/P(I)<=delta/3.
Together with interval truncation<=delta/4 this is strictly less thandelta.
The bit coin for q_tilde is exact and finite; no nested unbounded rejection.

Evaluate ell=logPMF(k)-logM using logGamma(N+1)-logGamma(k+1)
-logGamma(N-k+1)+klogp+(N-k)log(1-p)-logM. Absolute ell error<=e/8
suffices: if an approximation is below -log(16/e), set q_tilde0; otherwise
compute its exponential, clip to[0,1], and dyadically round within e/8.
Tiny probabilities need no relative precision. A fixed margin in the
cutoff and exponential error covers the uncertain cutoff band.

Here is a complete BIT justification for logfactorials. For x>=2r_s,
the r_s-term positive-real Stirling expansion for logGamma(x) has remainder
bounded by its first omitted term (NIST DLMF5.11(ii),
https://dlmf.nist.gov/5.11#ii, actual statement checked), at most
    4(2r_s)!/((2pi)^(2r_s+2) x^(2r_s+1))
    <=(2r_s/(2pi*x))^(2r_s)<=2^(-5r_s).
Take r_s>=ceil(P/5)+1. If n+1<2r_s, shift log(n!) to
log((n+2r_s)!)-log(product_(j=1)^(2r_s)(n+j)); the correction product
has O(r_s log r_s) bits. Exact Bernoulli coefficients require polynomial
bits/time inr_s. Choose P=O(log(N+2)+log1/e+log(bitlength(b)+2)) with
sufficient guard bits for the O(r_s) sums. The logN term pays multiplication
of logerrors by N, NOT a numericN loop. Standard argument reduction and
2atanh((y-1)/(y+1)),1<=y<2, compute logs with a geometrically convergent
series; the extra log(bitlength(b)+2) precision pays the exponent timeslog2.
Pi and the remaining elementary operations are computed to the same fixed
precision. The total bitlength/time is polynomial in log(N+2), bitlength(p),
and log1/delta. Multinomial sampling uses m-1 conditional binomials, with
parameter p_i/(1-sum_(j<i)p_j), residual photon count, and deterministic
zero-count/zero-probability cases. Per-call TV allocations sum to the
requested proposal error.

### 3b. Small probabilities and stable coherent rejection

First define exactly normalized FINITE inputs: approximate each one-particle
column by a rational-complex vector beta, then use alpha_tilde=beta/||beta||.
Normalization need not preserve rational coordinates. Its mode probabilities
|beta_i|²/sum_j|beta_j|² ARE exact rationals, so section3a applies. Likewise
approximate the coefficient vector by rational-complex entries and divide
by its Euclidean norm. Both input vectors being normalized are bounded away
from zero, so these operations are well-conditioned and computable.

If ||alpha-alpha_tilde||<=zeta, their K-boson condensates differ in norm
by at most K*zeta. The coefficient vector has l1 norm<=sqrt(chi), and the
matrix of normalized branch-state columns has operator norm<=sqrt(chi).
Thus choosing column error zeta<=epsilon/[1024(K+1)chi(L+1)] and
coefficient l2 error<=epsilon/(1024chi) makes the approximate coherent
vector Phi_tilde within epsilon/256 ofPhi. In particular its squared norm
nu lies in[3/4,5/4]. Its normalized state/count law is O(epsilon/128)-close
to the original. Keep each column's actual complex phase: an arbitrary
column-global phase is raised to K and changes branch interference.
Its EXACT coherent rejection probability is nu/chi,
without needing to compute nu.

Fix R=ceil(16chi*ceil(log2(16/epsilon))) outer trials. Exact rejection
would time out with probability<epsilon/256. Let D0=(K+1)^m bound the
number of countvectors and tau=epsilon/(256 R D0). Only logD0=m log(K+1)
bits are used; D0 counts are never enumerated. Write S for the approximate
branch squared-amplitude sum. If S<=2tau, its proposal mass over all such
x is<=2D0tau/chi. Rejecting these proposals changes the entire R-trial
process by at most2R D0tau/chi<=epsilon/128, by a coupling union bound.
This avoids an unproved lower bound on individual probabilities.

For other proposals evaluate S to absolute error<=tau/4; reject if its
approximation<=3tau/2. Every possible extra rejection then has S<=2tau;
otherwise S>=tau. Set gamma=epsilon/(256R). Evaluate each branch amplitude
and coefficient to enough fixed absolute precision that numerator and
S errors are<=gamma*tau/16. For example amplitude error
<=gamma*tau/(1000chi²) for BOTH amplitudes and coefficients
suffices, with a constant error margin for arithmetic. For S>=tau this pays the acceptance ratio to additive
gamma. Clip the final dyadic probability to[0,1]. Across R trials the
resulting probability error is<=Rgamma; the small-S loss was paid above.

Each condensate amplitude is computed as sqrt(multinomial PMF) times the
product of beta_i/|beta_i| to binary powers x_i. Exact zero beta_i with
x_i>0 gives zero immediately. A nonzero rational-complex entry has a paid
bitlength lower bound, so its unit phase is computable; binary powering
requires O(logK) multiplications and O(logK) extra precision. Logfactorials
and rational probabilities give the magnitude as in3a, with an absolute
amplitude underflow threshold. This costs polynomially many bits in native
input, m log(K+1), logchi and log1/epsilon, even at destructive interference.

Approximate uniform branch sampling with a finite fair-bit clock and the
multinomial proposal can each have TV error<=epsilon/(256R). All proposal,
ratio, cutoff, timeout and normalized-state errors then sum to less than
epsilon (shrink the fixed error allocation if necessary). Every loop is
capped; runtime is polynomial in chi,m,L,nativebits,log(K+1),log1/epsilon.
Uniform branch choice avoids division by small coefficient probabilities.

No full classical sampler implementation is claimed. This complete written
construction is a matched classical baseline for its explicit input and chi
regime, not a theorem for arbitrary Fock inputs or exponentially many branches.


## 4. Source scope and external review dispositions

The original Hermite proof and the Iyer/Prakash sources have been read at
actual theorem/proof level; source and core reviews are CLOSED. The source
review includes all source locators, cutoff padding, phase convention and
workspace accounting. The classical review is separate: a QHT acceptance
label cannot establish a classical bit-complexity theorem.

Devroye--Los, Mathematics and Computers in Simulation228(2025),147--155
(retained devroye.pdf, copyright2024), explicitly assumes an idealized REAL
RAM with exact real uniform draws and unit-cost exp/log/trigonometry at
text54--59. Its constant EXPECTED binomial runtime is not the finite-BIT
result in3a. The printed multinomial discussion must retain conditional
renormalization of each remaining probability. Van den Nest0911.1624
Definition1/344--365 assumes efficient Born sampling AND amplitude
evaluation. Theorem3/525--527 yields additive matrix-element estimation;
it does not automatically supply full-TV sampling of a coherent sum.
Section3 proves the needed rejection interface directly. No novelty claim.

Paid Claude run2026-11-07-binary-binomial is COMPLETED/end_turn, model
claude-opus-5-5/high, estimateUSD0.297948. Parent read the complete report.
Its certified rational envelope, single rejection clock, explicit
normalization bound and Stirling remainder suggestions were checked and
adopted. The original bounded-horizon coupling was also a valid way to pay
acceptance errors, so the report's normalization criticism does not identify
a counterexample. Its concrete bounds are used only fordelta<=1/4, and
additional log(bitlength(b)+2) guard bits pay large argument exponents in
logarithm evaluation. Positive-real remainder statement checked against
actual NIST primary text; no costly numerical sweep is needed to prove it.
The distinct native-hypothesis-selection run refused with EMPTY response,
estimateUSD0.017036, no findings and no retry. Both processes terminal and
reaped. SumUSD0.314984 is a usage estimate, not invoice or remainingbalance.

## Next decision and false gates

The quantum endpoint is PRIOR ART and needs no new backend. The bounded-chi
bunched regime is classically matched; short Fourier
expansions alone are not a remaining quantum candidate. A new direction
must specify a readout/family outside this comparator and a concrete new
operation; generic universality or a large K does not establish Shor-level
advantage. No novelty, separation, full/quantum execution, general active
Gaussian cutoff theorem, arbitrary-Fock classical sampler or exponentially
long kicked-circuit fast-forwarding may be inferred.

The next hard question must be chosen by external value, not by enlarging this
note's circuit class. No further Kerr backend or nearby low-branch variant is
queued. Re-entry requires an explicit native family/readout and a concrete
operation beyond the known full circuit simulator, together with a classical
attack outside the matched bunched/chi regime. For that proposed family,
next run `tools/corpus/cli.py been-tried "<exact family and operation>"` with
/opt/anaconda3/bin/python, then actual primary literature and the matching
baselines lookup. Expected artifact is one candidate card and a decisive
classical falsifier/proof, not another large-K plot or generic universality
claim. Accept only a paid all-parameter operation or a genuine counterfamily.
