# Known-Preparation Coherent Reflection Audit

Local derivation / external review pending. This is a costed access component
and a set of falsifiers, not a new receiver or a hardness reduction.

## Access and phase gauge

The original noisy-linear records and the reduction's mask give the ACTUAL
phase values in `native_noisy_phase_input.prepare_inputs`. This is legitimate
same-original-data access; an opaque quantum-only HSP source does not supply
these values or its preparation inverse. The existing indexed-access module
already implements the fixed-bank diagonal and inverse. The refinement here
is the complete pure-seed preparation/reflection composite, not new oracle
access inferred from copies.

Arrange 2*B*M distinct classical originals into B cohorts of M qutrits. B is
a power of two in the explicit Hadamard index preparation. Define

```
Phi_y = B^(-1/2) sum_b |b> tensor product_j psi_bj(y)
psi_bj(y) = (1, omega^value_bj1, omega^value_bj2)/sqrt(3)
U_y = D_y (H_index tensor F3^tensor_M)
R_y = U_y (I - 2|0><0|) U_y^dagger = I - 2|Phi_y><Phi_y|
```

Every phase in D_y is a known integer numerator modulo q=3^r. Multiplexing
uses explicit reversible index comparisons, not free QRAM. Each preparation
has at most 2*B*M controlled diagonal branches and B index comparison pairs.
The tensor F3 layer has M qutrit Fourier gates, and the index has log2(B)
Hadamards. A reflection invokes a preparation and its inverse, plus a
multi-register zero test/phase gate; its synthesis cost remains an obligation.
The inverse is F3^dagger D_y^dagger (with index inverse in the Fourier layer),
not D_y^dagger F3^dagger. No ideal secret-dependent gate is supplied.

The displayed gauge fixes the zero component of EACH source qutrit positive.
Relative phases between cohorts are physical. Independently removing the
global phase of every cohort changes this coherent seed and is not allowed.
Repeated preparation/reflection uses the SAME frozen bank: no fresh labels,
independent errors, or independent classical originals are generated.

## Exact IID error law and moment budget

Condition on all labels and the common mask. Errors are externally promised
independent across all 2*B*M originals, independent of labels, with a shared
symmetric law. Let gamma=E exp(2*pi*i*e/q), which is real. For one qutrit,

```
r = (1 + exp(i theta_1) + exp(i theta_2))/3
a = E r = (1+2 gamma)/3
A = |a|^2
C = E |r|^2 = (3+4 gamma+2 gamma^2)/9
E |<Phi_s,Phi_y>|^2 = A^M + (C^M-A^M)/B
E D(Phi_s,Phi_y)^2 = 1 - that expression
||R_y-R_s|| = 2 D(Phi_s,Phi_y)
```

The last identity follows from the two nonzero eigenvalues of the difference
of two rank-one projectors. It also holds when extended by identity on ANY
work register. The law is for the actual fixed seed, not averaged input
densities substituted inside an oracle. The exact finite controls enumerate
error signs only to verify this identity; the scalable budget never does.

For the true integer second moment E e^2 <= V, symmetry gives
1-gamma <= 2*pi^2 V/q^2. For B=1,

```
E D^2 <= (16*pi^2/9) M V/q^2.
```

Indeed 1-C = [4(1-gamma)+2(1-gamma^2)]/9 <= 8(1-gamma)/9,
then 1-C^M <= M(1-C). For arbitrary B, the gauge-aware vector bound is

```
E ||Phi_y-Phi_s||^2 = 2(1-a^M)
E D^2 <= (8*pi^2/3) M V/q^2.
```

For -1<=a<=1, 1-a^M <= M(1-a); this works also for negative a.
Both D^2 bounds are clipped at one. Crucially B does not multiply either
bound. This is a composite-reflection improvement over bounding the worst
individual diagonal branch of a B*M-sized indexed bank. It does NOT improve
the operator error of arbitrary uses of D_y or fast-forwarded phase powers.

Let e2 be the applicable mean squared D bound. For a receiver using K
initial seed copies and at most T reflections on arbitrary coherent work,
the averaged complete-output total variation loss is at most

```
min(1, sqrt(K*e2) + 2*T*sqrt(e2)).
```

For each frozen bank, K copies have squared trace distance
1-fidelity^K <= K*(1-fidelity). A hybrid argument charges the reflection
operator norm on every call, even if later controls adapt to measurements.
Average only AFTER that argument; Jensen bounds the two square roots. K
copies are tensor copies of the SAME point seed, not IID new source draws.
If the implemented unitary preparation is delta_U-close in operator norm
and the zero-phase gate delta_S-close, add sqrt(K)*delta_U plus
T*(2*delta_U+delta_S). These are promised complete implementation bounds,
not angle descriptions masquerading as a hardware compiler. Public source
rounding loss and the receiver's OTHER gates/instruments are separately
additive; zero values assert ideal implementations, not measured accuracy.
Precision refinements use exact
rational pi/square-root enclosures; finite controls do not prove promises.

## Falsifiers

1. **Averaged density is not a frozen-bank oracle.** For a qubit with phase
   theta=+/-2*pi/q, its averaged copy differs from |+> by
   delta_copy=(1-cos(theta))/2. Yet (R_theta R_0)^T on |+> yields outcome
   minus with probability sin^2(T*theta). At q=81,T=20 this is near one,
   while T*delta_copy is small. This is an operational budget counterexample,
   not a candidate algorithm or invented oracle problem.
2. **Distinct IDs do not prove IID.** Give every qutrit in a cohort the same
   error pair, and the second cohort the negative pair. Each marginal is
   symmetric with the same moment; the coherent relative phase accumulates
   across M sites. The actual fidelity can violate the proposed IID moment
   bound. Source independence must remain an explicit proof obligation.
3. **A single central sector is insufficient.** At native level L>=2,
   center vectors are pi^(L-1)*u with u in F3^n. A product cohort has central
   character c_b=sum_j c_bj. The coherent seed's vector stabilizer contains
   ker(C), where C has rows c_b. Its ray stabilizer contains the kernel of
   rows c_b-c_0. One cohort has all the center in its ray stabilizer, and
   for n>=2 a nonzero center kernel even as a vector. Thus the mixed-source
   gap-one contract does not transfer to one fixed product cohort.
4. **Polynomial dimension is a classical baseline.** M=1 and polynomial B
   give dimension3*B. Explicit state-vector simulation costs polynomial work
   per seed-only operation; wide group/work registers and their coupling are
   NOT included in that statement. Known preparation is not a general
   classical-simulation theorem. A target Hamiltonian gap is not a proved
   preparation path or decoder.

## Conditional finite-bank overlap gap

There is a constructive alternative to silently importing the mixed-source
gap. Use B IID cohorts of M IID full native labels and IDEAL supplied states.
Under the controlled tensor induced representation, for a fixed group
element g the cohort overlap Z_b(g) is bounded in absolute value by one.
The known original-source identity is E Z_b(g)=1_H(g): each individual
expectation is 1_H and independent products preserve it. For g in H, each
individual state is fixed exactly. For g outside H, real/imaginary Hoeffding
and a union bound over |G|=3^(nL+1) give

```
Pr[exists g outside H: |B^(-1) sum_b Z_b(g)| >= epsilon]
 <= 4 * 3^(nL+1) * exp(-B*epsilon^2/4).
```

For failure <=2^-h, the conservative sufficient threshold
B >= 4*(2*(nL+1)+2+h)/epsilon^2 uses ln3<2, ln4<2, ln2<1.
Round UP to a power of two for the explicit index preparation. This gives
a conditional finite-bank absolute overlap gap >=1-epsilon, for arbitrary
M>=1. It does not certify a particular observed bank, nor determine the full
subgroup from that bank. It assumes original IID full native labels, not
labels selected after looking at the phases. Noise reflection approximation
and this high-probability ideal-bank event are separate error ledgers.

At M=1 this honest gap still gives only a polynomial-dimension seed and no
efficient hidden-subgroup decoder. At growing M the seed Hilbert space is
wide, but rank-one access does not by itself establish useful interference,
efficient group search, robustness, or classical separation.
Scalable profiles are formal resource/error ledgers, not executed banks.
Profiles beyond native level512 explicitly exceed the current ring backend's
implementation cap; the analytic inequalities do not remove that limitation.

## Research decision

Keep coherent multi-cohort access as a CONDITIONAL research interface, not
an accepted algorithm. Deprioritize seed-only low-dimension proposals and
single-sector product-seed proposals that claim the original mixed gap.
The next meaningful experiment must specify the retained coherent group/work
register, all coupling gates, resource cap, decoder, and same-original-data
classical/tensor baseline. Try to simulate the proposed reflection program
before expanding its search. Outside the measured-packet simulation cut is
necessary for this route, not sufficient evidence of quantum advantage.

Run `python theorems/known_preparation_coherent_reflection.py --write`, then
`node research/certificates/known_preparation_coherent_reflection_crosscheck.js`.
Finite exact cyclotomic controls are certificate checks, not scalable quantum
execution. No hardware, full receiver, hardness transfer, or speedup is claimed.
