# An Explicit Two-State Receiver For The Surface Source

2026-10-23. Proposed proof with exact arithmetic and Qiskit interference
controls. Independent review pending. This specializes known quadratic
hidden-polynomial learning, not a claimed new general quantum primitive.

## Decision And Scope

The surface receiver no longer needs to leave its quantum learning step
as an unspecified HPGP call. It can use a direct two-state cancellation
measurement, two linear equations per row, and four public graph charts.
For an exact coherent LEFT-coset oracle

    f(g)=f(h) iff gW=hW,       g,h in Sp_4(F_p),

it recovers the hidden Lagrangian W using at most 32h coherent source
queries plus nine classical verification queries, with ideal failure
probability at most 4*(23/27)^h. Classical field arithmetic has expected
polynomial bit cost. Quantum arithmetic and approximate F_p Fourier
transforms have polynomial bit cost with a separately paid precision.

Here p is the receiver's ODD PRIME, equal to the isogeny prime ell in
the proposed geometric application. It is NOT that application's curve
characteristic. This pass is for rank two over a prime field, not arbitrary
rank, extension fields, rings or DCP.

The essential unimplemented dependency remains the REAL geometric source.
The small Qiskit controls enumerate oracle fibers exponentially and use
dense gates; their timings are not the claimed scalable algorithm.

## 1. Legal Source Queries And Fourier Signs

Use paired coordinates (x1,y1,x2,y2). On a good chart the hidden plane has
basis [[a,b],[1,0],[b,c],[0,1]], corresponding to S=[[a,b],[b,c]]. For the
row direction E_12 (indices 1,2 here), query the original group on

    U_X * D(I+t E_12),       t in F_p, X in Sym_2(F_p).

The public matrix builders and elementary-lift source already support
these queries. They are symplectic; no query leaves the promised domain.
After the group label is measured, the remaining state is

    p^(-1/2) sum_t |t>|z-P(t)>,
    P(t) = (2bt+ct^2, ct, 0)

in the three independent symmetric coordinates (11,12,22). The unknown
fiber label z is not read. Apply the INVERSE Fourier transform on those
three registers and measure their frequencies (r,v,w). Up to a global
phase, the remaining register is

    p^(-1/2) sum_t omega^[r c t^2 + (2br+cv)t] |t>.

All three frequencies are uniform and independent, conditional even on
the fiber label. Discard r=0. Apply the public translation

    t_new = t_old + v/(2r).

The resulting state is, up to a global phase,

    |chi_r(b,c)> = p^(-1/2) sum_t omega^[r(c t^2+2bt)] |t>.

For E_21, the same procedure uses r=w and yields |chi_r(b,a)>. In neither
case is b, c or a supplied to a gate. The cross-frequency v is removed
using only the measured frequency and field arithmetic.

One original coherent f query prepares each raw state. Original source
workspace and the public query matrix must be uncomputed before this
measurement. Uniform F_p preparation, Fourier precision and f's full
output width are charged, not declared free.

## 2. Two Fresh States Yield One Linear Equation

Take two independent packets with nonzero public weights r1,r2. If
-r1/r2 is a nonsquare, discard BOTH states. Otherwise find a root gamma
such that

    r1+r2*gamma^2=0,       gamma != 1.

Such a root always exists when the ratio is a square: if one root is 1,
choose -1, using odd characteristic. This avoids losing the b coefficient.
Apply the reversible shear

    (t1,t2) -> (t=t1, s=t2-gamma*t1).

The combined phase becomes

    2[(r1+r2*gamma)b + r2*gamma*s*c] t
       + r2(c*s^2+2b*s).

The t^2 term is exactly zero. Measure s, then inverse-Fourier-measure t,
or equivalently measure them jointly after the latter transform. The
resulting frequency k satisfies

    k = 2[(r1+r2*gamma)b + r2*gamma*s*c].

Define e=r1+r2*gamma=r2*gamma*(1-gamma), which is nonzero. Obtain

    b + lambda*c = value,
    lambda = s/(1-gamma),       value=k/(2e).

s and hence lambda are uniform in F_p, independent of the unknowns. Two
equations with distinct slopes determine b,c. The second row similarly
determines b,a; reject an inconsistent shared b.

This uses fresh copies, not cloning, time reversal of an unknown state,
a supplied stabilizer tableau or coherent access to secret coefficients.
The measurement circuit itself depends only on p and gamma.

## 3. Four Deterministic Charts And A Global Certificate

The four public frames independently rotate either coordinate plane by
[[0,-1],[1,0]], or leave it unchanged. At least one makes the bottom
projection of C^(-1)W invertible. The proof is the Plucker identity from
the classical baseline: isotropy gives P12+P34=0; if all four cross
minors vanished, P12*P34-P13*P24+P14*P23=0 would force every minor to
vanish, contradicting rank two. Unlike that baseline, no c->c+1 shift
is needed; the chirp learner also handles c=0.

Try those four frames in a fixed order, with capped pair budgets. Bad
charts need not satisfy ANY phase-state promise. From plausible row
answers form the graph plane and conjugate it back. For each of its
two independent columns v, test against the ORIGINAL oracle

    f(I+v*v^T*J) = f(I).

For a Lagrangian W, this transvection stabilizes W iff v lies in W:
if its pairing with W is zero, v belongs to W^perp=W; otherwise invariance
forces the nonzero transvection increment, a scalar multiple of v, into
W. The reverse implication is immediate. Both tests passing therefore
certifies the exact plane under the original oracle promise.

No malformed or bad-chart phase answer can bypass this certificate.
Constant-label bad charts give r=0 and exhaust their budget in the
controls; deliberately fabricated row answers also fail the certificate.

## 4. Explicit Budgets

Use two stages per row, each allowing h independent raw pairs. Stage one
seeks any compatible pair; stage two seeks one with a different slope.
Each pair consumes TWO new raw copies even when it is discarded.

The probability of two nonzero weights and a square ratio is

    alpha=((p-1)/p)^2 / 2 >= 2/9.

Conditioned on this event, a new slope differs from the first with
probability 1-1/p, so stage two succeeds with probability at least 4/27
per trial. Each stage therefore fails with probability at most
(23/27)^h. Two stages in each of two rows give failure at most
4*(23/27)^h for any fixed good chart. At least one fixed chart is good.
Earlier bad charts cannot falsely accept, so this same bound suffices
for the full procedure; no extra factor of four charts is necessary.

Each row uses at most 4h copies, giving at most 32h over four charts.
There are at most eight candidate-vector tests and one shared f(I).
Take h>=ceil(log(4/epsilon)/log(27/23)) for ideal failure <=epsilon.
Output ABORT on exhaustion, never a fabricated negative result.

Quadratic roots use standard randomized polynomial-time finite-field
arithmetic. The prototype delegates to SymPy's root routine, whose local
Tonelli--Shanks code was inspected; its nonresidue search has expected,
not hard worst-case, runtime. A uniform bounded-clock implementation must
cap and charge this classical failure separately. It can be done BEFORE
the corresponding pair measurement; these are measured public weights.

Budget approximate Fourier and other circuit errors by a hybrid bound
over the capped operation count, and add geometric-source error separately.
The 32h+9 bound is not a Toffoli, physical-qubit or fault-tolerant estimate.
Two chirp registers need O(log p) qubits; source label and arithmetic
workspace must be added. No exponentially wide field table is part of
the proposed scalable algorithm.

## 5. Dequantization, Falsifiers And Prior Art

The previously implemented classical equality-only receiver takes
O(sqrt(p)) oracle calls. This quantum procedure does not establish that
real geometric labels require that classical cost. The product-target
and mixing-endomorphism attacks remain mandatory same-input baselines.

The chirp states and decoder are stabilizer/Clifford structures over
F_p. This does not itself classically dequantize their preparation from
f: a classical stabilizer tableau would already contain the unknown
quadratic coefficients. It is additional advice, not the original input.
The explicit dephasing control reduces the probability of satisfying
the paired equation from one to 1/p. This is a coherence check, NOT
experimental evidence of computational advantage.

Decisive falsifiers include a sign error in the two Fourier transforms,
a biased/nonfresh frequency source, state reuse after measurement,
incorrect shear orientation, uncharged state selection, and any wrong
plane passing the original-oracle certificate. The tests exercise these
boundaries through exact exponent identities, Qiskit interference,
bad charts, fake answers, state counts and dephasing.

Quantum algorithms for quadratic polynomial graphs are established prior
art: [Decker--Wocjan](https://arxiv.org/abs/quant-ph/0703195), and the
[Ivanyos--Santha HPGP framework](https://arxiv.org/html/1503.09016) used by
the earlier receiver. The cancellation here is an explicit specialization
to its surface row structure, not a novelty claim. A targeted search did
not establish whether this precise Sp_4 composition was already written
down; absence of a search hit is not a novelty certificate.

## 6. What The Code Actually Executes

`chirp_receiver.py` contains public root selection, measurement-equation
postprocessing, four-chart orchestration, budgets and final certificates.
It accepts a state-preparation and measurement backend, not hidden S.

`quantum_controls.py` uses Qiskit 2.3.0 for padded-prime Fourier gates,
the two-register shear, state measurement and interference controls.
For primes 3 and 5, `NativeFiberControl` enumerates the p^4 ORIGINAL
legal queries per chart/direction to construct exact post-label states.
These classical table queries are reported separately from ideal coherent
source-copy counts. It does not read subspace coordinates out of labels.
The fixture callback alone knows the hidden plane.

Dense gates are explicitly bounded to small fields. They are exponential
in log p, not a scalable gate synthesis. The 127-bit check is classical
postprocessing only. No geometric source, quantum hardware or full
fault-tolerant prime-field circuit was executed. The remaining research
bottleneck is the source and the hardness of its actual public data,
not another opaque-label scaling benchmark.
