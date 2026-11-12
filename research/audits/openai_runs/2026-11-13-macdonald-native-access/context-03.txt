# 2026-11-13 — Independent composition of the logarithmic-precision Jack compiler

**Verdict: the proposed replacements compose, with the workspace and precision
rules below.** For fixed alpha=3 and numerical degree D, the clean shape-to-Jack
transform has a uniform circuit-generation, BIT and gate bound
poly(D,log(1/epsilon)). Its restricted operator-norm error is at most epsilon,
including all retained workspace and an arbitrary reference. This is a written
construction, not an implementation, novelty or classical-separation claim.
The older inverse-accuracy theorem does not need to be changed to justify this
review. Claim promotion remains the parent's decision after reading it.

Inputs: current STATE/TRAPS/GOAL; JACK_LOG_PRECISION_COMPILER; the complete
300-line branching review; the native-measurements report §§4.3 and 5; actual
BCCKS 1412.4687, retained taylor_lcu.txt, physical LF 125–187 and 190–242.
The source really proves the cubic OAA identity and compact Taylor selector;
it also explicitly DISCARDS signals at LF 172–184. We do not import that last
step: the clean bound is proved below with squared internal tolerance.
No network, API, Git, implementation or sweep was used.

## 1. What must be preserved from the existing construction

Write N=D+1. The proved native maps B_n and C_n have identical positive
removal-path amplitudes sqrt(q), with their corresponding Fock/shape vacuum.
The desired transform is B_down^dagger C_down after the fixed vacuum recoding.
The exact polar operation in B_n is the principal square root of

    W_c=(2P0-I)(2P_c-I),

where c is a RETAINED logical content register, P_c is the full spectral
projector of L_(n-1), and P0 is the marker-zero projector. On every required
Jordan plane, W_c has phases ±2theta, cos(theta)=sqrt(tau)>0, and its principal
square root sends the Lax vector to its Jack vector with positive phase.
Thus x=cos^2(phi/2)=tau >= a:=1/(64N^2). The tau=1 case has phi=0.
All these statements hold on orthogonal direct sums, including degeneracies.
No procedure here learns lambda or tau. There is no factor equal to the number
of shapes, contents or paths in any norm estimate.

A necessary stronger interface for the INNER simulations is available:
W_c must be approximated on the WHOLE valid degree sector, for every logical
c, with its lower-level workspace zero. Merely approximating W_c on the
polar promise would not pay a block encoding or its inverse. Native simulation
and integer-grid content extraction give exactly this stronger interface.

## 2. Binomial polar filter and its actual clean amplification

Let b_k=binom(2k,k)/4^k, q_K(x)=sum_(k=0)^K b_k(1-x)^k, and

    H=(2I+W+W^dagger)/4,
    P_K(W)=(I+W)q_K(H)/2.

For the principal phase -pi<phi<pi, put f=exp(i phi/2). Then
P_K=f t, where t=sqrt(x)q_K(x). The binomial series gives 0<=t<=1 and

    1-t <= (1-x)^(K+1)/x <= exp(-a(K+1))/a       (x>=a).

At W=-1 the polynomial is zero; no approximation claim is made there.
Define s=sum b_k, so 1<=s<=K+1. Uniformly selecting I,I,-W,-W^dagger
block-encodes R=I-H. Use DISTINCT block-signal registers for its first,
second, ..., K-th occurrence. Conditional application for indices j<=k
then has all-zero block R^k. Preparing k with weights b_k/s, applying these
K conditional blocks, and reversing that preparation gives q_K(H)/s.
A separate (I+W)/2 block gives P_K/s. This is a compact circuit, not a
list of exponentially many expanded words. Each R uses at most two
controlled W/W^dagger calls; the complete block uses at most 2K+1.

Set m=4(K+1), theta*=pi/(4m+2), and dilute with the known amplitude

    d=s sin(theta*) < pi/16 < 1.

The resulting unitary V has block B=sin(theta*)P_K. Let P project onto
ALL its zero signal registers and R0=I-2P. Apply

    A_m=(-V R0 V^dagger R0)^m V.

The minus signs are part of the unitary, including controlled uses. Standard
two-projector algebra, or iteration of the source identity
P(-V R0 V^dagger R0 V)P=3B-4BB^dagger B, gives on each promised eigenvector

    P A_m |0,omega> = |0> f sin((2m+1)arcsin(t sin(theta*))) |omega>.

If 1-delta<=t<=1, let
Delta=(2m+1)[theta*-arcsin(t sin(theta*))]. Then

    0<=Delta <= (2m+1)tan(theta*) delta <= pi delta,

using theta*<pi/4 and tan(theta*)<=2theta*. The displayed clean amplitude
is f cos(Delta). Unitarity, including the rejected signal space, now gives

    ||A_m|0,omega>-|0>f|omega>||^2 = 2(1-cos(Delta)),

so the FULL clean-isometry error is <=pi delta<4delta. This is stronger
than bounding only the projected block. Orthogonal spectral blocks make it
an operator-norm estimate, also after tensoring with a reference. The same
constants apply coherently to all c. The query cap

    Q=32(K+1)^2

covers (2m+1)(2K+1) calls. The normalization and amplification angle are
known globally; no unknown overlap is inserted into Grover amplification.

## 3. Native Taylor simulation with all signals kept

For L_d use the already proved 2d mode/parity matchings and diagonal 2l.
Their canonical endpoint and weight are unchanged by the matching swap.
Consequently the endpoint arithmetic really uncomputes, even on a
superposition of endpoints. With B0=4N and a power-of-two term count
M>=2d+1, each term has a native signal block H_j/B0 and a uniform selector
gives L_d/Gamma, Gamma=M B0<=16N^2. Zero or invalid terms have zero blocks.
The construction defines a full unitary on its logical block signals; all
arithmetic scratch is clean. No sparse oracle is supplied.

More generally suppose this native block represents a Hermitian H/Gamma,
with known Gamma<=Gamma_bar. For |t|<=8 choose Rseg=64 Gamma_bar (an integer)
and Delta=t/Rseg. Thus x=Gamma|Delta|<=1/8. Fresh block signals give powers
(H/Gamma)^k. With weights x^k/(2k!), phases (i sign(t))^k, and the remaining
probability split equally between I and -I, a compact Taylor selector has
block T_J/2, where

    T_J=sum_(k=0)^J (i Delta H)^k/k!,
    ||T_J-exp(i Delta H)|| <= 8^(-J).

The Taylor weight sum is <=exp(1/8)/2<1; the cancelling padding is positive.
It uses J block calls, not an expanded word table. At t=0 use identity.

For ANY unitary block V with ||PVP-U/2||<=beta and unitary U, the same
cubic identity gives clean-block error <=15beta. Since the entire OAA word
is unitary, its clean-isometry error is <=sqrt(30beta): indeed the squared
error operator is 2I-U^dagger A-A^dagger U, where A is its clean block.
Here beta<=8^(-J)/2. For a requested whole-simulation error rho, take

    J=ceil(log2(2^14 Rseg^2/rho^2)).

The segment's clean error is <rho/(32 Rseg). Keeping its signal registers
and composing Rseg segments therefore gives error <rho/32, in particular
<=rho. Distinct segment banks are convenient and still polynomial-size.
Nothing is discarded, measured, reset, or postselected. Exact inverse
calls reverse the same circuit and the same register layout.

For content extraction, M0=2^ceil(log2(8N)) suffices, with ell=log2 M0.
Ideal QPE on exp(2pi i L_d/M0) returns the signed integer content exactly,
with amplitude +1. Each of its ell controlled evolutions has |t|<2pi.
Using simulators of clean error rho gives extraction error <=ell rho before
bottom gate rounding. Reflection about content c is extraction, the exact
signed equality phase, and ACTUAL inverse extraction. It has error
<=2ell rho. This estimate holds on the whole valid sector, not only one
cyclic space. Global spectral degeneracy is harmless. The outer content
label is logical data; the INNER content-test register is a separate bank.

## 4. Fixed gates and the nested-workspace rule

There is an elementary finite-gate compiler, so no QSP phase-list compiler
or unit-cost real rotation is required. Fix, for example, the finite palette
H,S,X,Z,CNOT,Toffoli, controlled-H and controlled-S (and their finite words).
Higher Boolean controls are computed into an AND flag with Toffoli and
uncomputed. This avoids assuming every controlled gate is already exact in
an unspecified palette. Known scalar phases are implemented on that flag.

A real rotation is U=cI+sJ0 with J0=XZ, J0^dagger=-J0, J0^2=-I. A diagonal
phase is handled by J0=iI with c,s depending on the unchanged logical bits.
Thus controlled phases, including their scalar phases, are also covered.
Approximate c,s to 2^(-b-10). With a uniform 2^b-label Hadamard seed, allocate
even integer counts approximating 2^(b-1)|c| and 2^(b-1)|s| to signed I,J0.
Split the remaining, even, count between I and -I. For b>=8 the count fits,
and the all-zero block differs from U/2 by at most 8*2^(-b). Signs near zero
can be decided from the approximation: a wrong sign then has only that small
absolute error. The half-block OAA gives full clean error <16*2^(-b/2).
Selection, thresholds, signs and reflections use only the fixed palette and
reversible integer arithmetic. No further approximate rotation is needed
inside THIS compiler. The 2^b labels use b qubits and binary comparisons;
they are not enumerated. Its actual inverse is its reversed gate word.

Coefficient computations have a uniform polynomial bit clock. The b_k/s
are exact rationals with O(K) bits; their nonzero weights are at least
1/[(2K+1)(K+1)]. The dilution is bounded away from one and is computable
from pi and sine to any requested bits. Taylor coefficients involve only
known dyadic multiples of pi. In the QPE uses, a positive x is at least an
inverse polynomial in N. Hence the logarithm of the inverse smallest
positive Taylor weight is O(J(log N+log(J+1))). Prefix divisions and square
roots therefore cost polynomial bits, even for tiny terminal weights.
Branching/V weights have the previously proved polynomial-bit arithmetic.
Bounded-argument Taylor series and geometrically convergent arctangent
series compute sine/cosine and pi; square roots use integer algorithms.
Absolute square-root precision can be secured by twice as many input bits.
Invalid encodings receive specified identity/zero-weight branches and safe
denominators. They do not cause an unbounded numerical branch.

The crucial register rule is this:

* Different factors in a POWER block have different block-signal registers.
* A selected unitary V, every occurrence of V^dagger in its OAA, and its
  eventual circuit inverse use the SAME register banks and reversed word.
  Allocating unrelated fresh banks for V^dagger is not that inverse.
* Every lower-level approximate gate has a clean-isometry guarantee for
  ALL its logical inputs, including arbitrary upper signal/control states.
  Its own lower-level scratch is zero in the ideal reference circuit.

Consequently upper OAA may act on dirty upper signals without invoking an
unproved lower-level promise. At each circuit-word occurrence, compare with
the ideal logical gate while its lower scratch is zero. A unitary hybrid
bound handles the actual accumulated leakage; no assumption says the actual
scratch has magically reset. For inverses, if T approximates U on a clean
subspace S, then

    ||(T^dagger-U^dagger)U|_S||=||(U-T)|_S||.

Here U is a full logical unitary on the required inner sector, so its clean
range is again the whole logical sector. This pays all inner inverse calls.
All-zero reflections may include lower scratch: on the ideal clean lower
bank they are exactly the required upper reflection. Scratch is retained to
the endpoint. The error statements are joint-vector/operator bounds, not
success-conditioned bounds. Repeated uses of one bank are legitimate by
this hybrid argument; fresh complete segment banks are an optional simplifier.

## 5. An explicit noncircular allocation and the final transform

For D>=1 and 0<epsilon<1/2 choose, in THIS order,

    N=D+1,  zeta=epsilon/(128N),  delta=zeta/16,  a=1/(64N^2),
    K=ceil(a^(-1)*(1+ceil(log2(1/(a delta))))),
    m=4(K+1),  Q=32(K+1)^2,
    ell=ceil(log2(8N)),
    rho=zeta/[64(Q+1)(ell+1)].

The chosen K makes the binomial defect <=delta. Take the known polynomial
Gamma_bar, then Rseg and J from §3. All these quantities are now fixed.
The polar truncation contributes <zeta/4. Replacing its W calls contributes
at most 2Q ell rho<zeta/32. Its outer content extraction contributes at most
ell rho<zeta/64. Therefore every REAL-ARITHMETIC B_n circuit, with all Taylor
signals retained, is within zeta/2 of its ideal clean B_n. The C_n and V
coefficient rotations can at this intermediate step be treated as their
specified ideal unitaries; their finite compilation is charged next.

Unroll this finite nested circuit schedule, including the actual B inverses.
Let T>=1 be a computable upper bound on the number of elementary variable
rotations/phases in it. This count is polynomial in N,K,J,Rseg and is fixed
BEFORE selecting their accuracy: it counts coefficient-preparation, block,
QFT and dilution rotations, not unknown logical states. Choose

    b=max(8,ceil(2 log2(128T/epsilon))).

Compile those rotations by §4. Total clean error is at most
T*16*2^(-b/2)<=epsilon/8. Exact integer arithmetic gates introduce no
additional approximation. Their lengths are polynomial in the chosen bit
precision and the coefficient-bit bounds above. For an inverse occurrence,
use the already compiled forward word in reverse with the same banks.
There is no recursive request to choose accuracy from its own final gate
count. The high-level count precedes b; the bottom compiler introduces only
exact gates and has polynomial cost in b.

The real-arithmetic B_down differs from ideal B_down by <=D zeta/2. The
already established common positive path range permits its ACTUAL inverse
on C_down's ideal range, with the same error by the inverse-on-range identity.
Thus real-arithmetic B_down^dagger C_down has error <=D zeta/2. Adding the
finite-gate error gives

    D zeta/2 + epsilon/8 < epsilon.

This bound includes the entire output workspace. It is a restricted operator
bound on all valid shape inputs, so it is uniform on arbitrary superpositions
and reference systems. No partition-count factor occurs. D=0 is identity.
K is polynomial in N and log(1/epsilon); Q,Rseg are polynomial in those
parameters; J and b are polynomial in their logarithms and log(1/epsilon).
All gate, classical compilation and workspace counts are therefore
poly(D,log(1/epsilon)), with fixed exponents. No exact exponent is claimed.

## 6. The BO work sampler also needs, and has, a native S block

The L simulator alone would NOT upgrade the quench output. In the common
canonical Fock space its final Hamiltonian is

    S=sum_(i,j>=1) sqrt(i*j*(i+j))
        (a_i^dagger a_j^dagger a_(i+j)+h.c.).

For each unordered i<=j with i+j<=D, label a merge/split edge by the endpoint
with larger m_(i+j). At this canonical endpoint the weight is

    2 sqrt(i*j*(i+j)*(m_i+1)*(m_j+1)*m_(i+j))     (i<j),
    sqrt(i^2*(2i)*(m_i+1)*(m_i+2)*m_(2i))        (i=j).

The factor two belongs ONLY to i<j: the original sum has both ordered pairs.
For a fixed pair its edges form chains. Splitting by parity of the larger
m_(i+j) makes two matchings, including the i=j chain where m_i changes by two.
Each endpoint can compute the same canonical label and weight; after the
controlled swap it can reverse that computation. The matching decomposition
has O(D^2) terms. Since k m_k<=D and i,j,i+j<=D, each displayed weight is
<=8N^2. Choosing a power-of-two term selector and block scale 8N^2 gives
Gamma_S<=64N^4 safely. No number of partitions or nonnative matrix entry is
used. The construction preserves the exact momentum-D sector.

The same retained-signal Taylor compiler therefore simulates S in
poly(D,log(1/rho)) BIT/gate cost. Its eigenvalues 2C1(nu) are integers in
[-D(D-1),D(D-1)]. Integer-grid QPE with modulus >=8N^2 uses O(log N)
simulations at times <2pi and resolves the energy exactly in the ideal
circuit. Allocate, for example, eta/8 to initial Jack preparation and
eta/[8(1+ell_S)] to each final-QPE simulation, with the same finite-gate
rounding rule. This gives a poly(D,log(1/eta)) TV-eta work sampler after
measuring only the energy output. The earlier known initial-energy formula
and physical scope are unchanged. The row/column classical z-law baselines
and all other classical-separation gates also remain unchanged.
