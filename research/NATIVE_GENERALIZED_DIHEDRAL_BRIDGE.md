# Native Inputs Have A Generalized-Dihedral Baseline

LOCAL REDUCTION / EXTERNAL REVIEW PENDING. This is a costed bridge to a known
algorithmic input family, not a new quantum algorithm, a polynomial receiver,
an executed Kuperberg sieve or a noisy classical-problem speedup.

## Why This Changes The Research Baseline

The earlier common-index native receiver has copy upper bound
K*(1+W+...+W^(L-1)), W=(n+1)^2. This is a useful constructive calibration, but
it is not the best conceivable or known upper bound for ideal native data.
A constant-probability local projection converts each paid native qutrit into
the exact uniformly labelled qubit input used by generalized-dihedral sieves.

[Kuperberg, Theorem7.1 and Section7](https://arxiv.org/abs/quant-ph/0302112)
gives an ideal abelian-hidden-shift algorithm of time/query form
2^{O(sqrt(log|A|))}, explicitly operating on labelled phase qubits. Here
|A|=3^(nL), so the literature-backed baseline form is
2^{O(sqrt(nL*log2(3)))}. This is an applicability reduction, not an executable
runtime prediction: constants, memory and approximation costs are not hidden
behind fabricated finite benchmarks. The original sieve has large quantum
memory. Later cyclic improvements must not be imported to arbitrary products
without checking their precise source and memory interfaces.

For L=Theta(n), this known ideal bound has exponent scale O(n), whereas the
stipulated native descent upper ledger has log-copy scale O(n logn). Neither
is a Shor-level polynomial algorithm or a proved classical separation. For
fixed L, the existing native polynomial receiver can be preferable: the
baseline is the minimum of legitimate applicable algorithms, not one slogan.

## Exact Mixed-Characteristic Additive Coordinates

Let R_L=Z[zeta3]/(pi^L), pi=zeta3-1, and write elements in the canonical
power basis(a,b) with its ACTUAL ideal carries. Put q=3^floor(L/2).

- At even L=2r, the additive group is Z_q x Z_q, with basis(1,zeta3).
- At odd L=2r+1, it is Z_(3q) x Z_q, with basis(1,pi); the coordinates
  of(a,b) are(U,V)=(a+b mod3q,b modq).

At odd L the inverse is(a,b)=(U-V,V), reduced in the true ideal chart.
For n ring coordinates take their n-fold direct product. Factor1 at L1 is
kept explicitly and carries no information. This is not F3^L substituted for
the native mixed-characteristic group.

Let beta_L=(u/Q,v/Q) be the native trace-pairing row, Q=3^ceil(L/2).
For each public ring label, its dual cyclic coordinates k are obtained from
its additive coordinates x by the following integer matrix, reduced modulo
the respective cyclic orders:

    even L: T=[[u,v],[v,-u-v]],
    odd  L: T=[[u,v-u],[(v-u)/3,-v]].

For odd L, v-u is divisible by3. The upper cross entry is divisible by3,
making the map well-defined from Z_(3q) x Z_q into its dual. At even levels
u^2+u*v+v^2=1; at odd levels it is3. Thus det(T)=-1 in either case. The
integer inverse preserves the same cyclic periods, so this is an actual
bijection on the dual group, not just invertibility in a misleading field.

For secret additive coordinates s_j and cyclic orders m_j, the exact phase is

    pairing_L(a,s) = sum_j k_j*s_j/m_j mod1.

The source label law transfers to uniform independent dual labels. The
chart/gate functions never take unknown secret coordinates; they occur only
in the forward verification fixtures. Small complete censuses illustrate the
bijective chart and arbitrary full-ring-secret phase identities. Scalable
closed-form chart checks do not enumerate the exponentially large group.

If an EXTERNAL reduction actually promises an integer-embedded secret(a,0),
its second additive coordinate is zero in either chart. Only the first dual
coordinate of each ring component then enters the phase. Its marginal label
is still uniform in Z_(3^ceil(L/2)), giving the smaller conditional baseline
group of order3^(n*ceil(L/2)). This includes the existing even-native noisy
classical-pair preparation's secret promise, but not arbitrary full-ring data.
The tests check the exact phase restriction and uniform marginal; no source
promise is learned from a few labels, and no full sieve is implemented here.

## Paid Local Projection

Original native samples have amplitudes

    1/sqrt3*(1,chi_L(a*s),chi_L((1+zeta3)*a*s)).

Measure the TWO-OUTCOME projector P=|0><0|+|1><1| versus |2><2|.
Success has probability2/3, independent of a and s. Retain the two-level
register and map its known basis to a qubit. The result is exactly

    1/sqrt2*(|0>+exp(2*pi*i*sum_j k_j*s_j/m_j)|1>).

Rejected registers are destroyed and charged. Unknown preparation/inverse,
cloning, coherent classical-value queries and favorable label filtering are
not supplied. The measured projection loses part of the native qutrit's
information; it is a baseline interface, not an information-preserving claim.

To request M accepted qubits, the finite extraction cap is C=3*(M+b) original
qutrits. With X~Bin(C,2/3), the exponential-moment bound gives

    Pr[X<M] <=2^(M-1)*(2/3)^C <=2^(-b-1).

The implementation returns no complete batch on finite-source exhaustion.
Declaring a cap does not physically establish an unlimited IID source. The
probability bound is conditional on that source promise, not inferred from
the retained finite labels or numerical amplitudes.

## Actual Sign-Combining Instrument

Given two paid qubits with labels k,l, apply CNOT(control=left,target=right),
measure the right qubit with actual outcome b and retain the left. Its label
is k+l for b0 or k-l for b1, with probability1/2 each on the uniform-diagonal
phase-source family. For supplied densities the retained matrix is

    rho_out[t,u] proportional to rho_left[t,u]*rho_right[t xor b,u xor b].

This computes actual supplied quantum data, including noisy densities. The
code cannot deterministically choose the minus branch. Both branches recorded
in a gate control are ALTERNATIVE counterfactual replays, never two physical
outputs from the same unknown inputs. Every physical execution retains one
child with the union of distinct paid original lineages. Using both as a
sieve population would be cloning and invalidates the source/copy ledger.

True signs are therefore available in this DIFFERENT encoding, unlike the
full-ring ternary index-permutation/Galois obstruction. This does not turn
arbitrary Gaussian dependence coefficients into free quantum gates: which
signs appear is measured, not selected by solving a classical kernel.

## Noise And Classical Scope

Uniform-diagonal averaged noisy native inputs retain projection probability
2/3. For the existing independent symmetric-error kernel, the projected
qubit has contrast gamma from its(0,1) entry, not the qutrit's average contrast
(2*gamma+gamma^2)/3. A binary merge multiplies real contrasts. Therefore ideal
sieve complexity does NOT establish a useful noisy recovery guarantee.
General approximate-source contraction must charge all ORIGINAL inputs,
including rejects, and every sieve gate. This pass does not supply that
complete robust sieve or an error-correcting decoder.

Copy-only quantum data remains distinct from the original classical noisy
records used to prepare it. Classical algorithms can retain those records.
No classical speedup separation or LWE hardness follows from this conversion.
It deliberately strengthens the quantum baseline against which new native
receivers must be judged, rather than manufacturing an oracle separation.

## Falsifiers And Next Experiments

- Dual coordinates fail the carried additive group law or the exact pairing.
- Conditioning on projection success biases native/dual labels.
- Rejected originals or desired measurement branches are obtained for free.
- A branch density differs from literal projector/CNOT measurement replay.
- Two alternative merge branches are counted as two reusable physical outputs.
- A literature bound is labelled as an implemented full solver or noisy result.

NEXT: a costed streaming generalized-abelian sieve consuming this finite
phase-source interface, with actual measured signs and all rejected/wasted
copies. Compare its source/noise exposure against native measured descent
and original-data classical attacks. Family-specific improvements must beat
this known ideal baseline, not the older n^{O(L)} upper ledger alone.

```
python theorems/native_generalized_dihedral_bridge.py --write
node research/certificates/native_generalized_dihedral_crosscheck.js
python -m pytest -q tests/test_native_generalized_dihedral_bridge.py
```
