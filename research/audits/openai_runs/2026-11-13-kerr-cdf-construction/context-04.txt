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
