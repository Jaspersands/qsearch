# A Multimode Information Escape, Not An Efficient Decoder

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No algorithm, novelty, accepted
candidate or general negative result. Run
`python theorems/dcp_conditional_error_frames.py --write`; the live artifact is
`phase_workbench/dcp_conditional_error_frames.json`, with contract and tests.

The single-SWAP noise limitation does NOT prove that the native source has
lost its useful bit. This workbench tests a concrete multimode alternative:
conditional phase-error frames, and a mathematical correcting transform whose
implementation is still exponentially expensive.

## 1. The Actual Error Modes

Let q=2^t, G=q^n, L=2^K and F_f={x in{0,1}^K:A*x=f}, d_f=|F_f|. On a
nonempty FULL-frequency fiber define

```text
|F_(f,e)> = d_f^(-1/2) sum_(x in F_f) (-1)^(e.x)|x>.
```

e is a possible original Z-error pattern, NOT an accessible hidden-error tag.
The decoder's possible-pattern library E must be fixed independently of A,
the secret and the realized error. A single public transform is used for all
actual errors in E. Its Gram matrix has exact entries

```text
Gram_f[e,e'] = B_f(e XOR e')/d_f,
B_f(d) = sum_(x in F_f) (-1)^(d.x).
```

Two distinct Boolean words have an original signed label difference with a
unit coefficient. Native full labels therefore give A(x-y)=0 with probability
1/G, even over a power-of-two ring. For any FIXED nonzero binary d,

```text
E_A sum_f B_f(d)^2 = L*(1-1/G).                         (1)
```

The diagonal word pairs contribute L; the off-diagonal signed sum is -L,
since sum_x(-1)^(d.x)=0. No field-rank assumption is used.

## 2. Born Weighting, Including Small Fibers

The frequency law is p_f=d_f/L, not a uniform distribution over nonempty
fibers. Write mu=L/G. On d_f>=mu/2,

```text
sum_good p_f*(B_f(d)/d_f)^2 <= (2G/L^2)*sum_f B_f(d)^2.
```

On0<d_f<mu/2 use |B_f|<=d_f and
d_f<=(2/mu)*(d_f-mu)^2. Expected occupancy squared deviation is
E sum_f(d_f-mu)^2=L*(1-1/G). Both good and small-fiber contributions are
therefore at most2*(G-1)/L. Empty fibers carry no Born mass. For M distinct
fixed possible errors, summing all M*(M-1) nonzero pair differences gives

```text
E_A sum_f p_f*||Gram_f-I||_F^2 <=4*M*(M-1)*(G-1)/L.     (2)
```

This is an original-source mean, NOT a guarantee on every matrix, frequency
or label-adaptively chosen error dictionary. Full small-source censuses test
both (1) and the NORMALIZED/Born statement (2), not just an unweighted proxy.

## 3. A Public Correcting Unitary Exists On Good Frames

Let Phi_f have columns |F_(f,e)>, e in E. If
eta_f=||Gram_f-I||_F^2<1, every Gram eigenvalue is positive, so d_f>=M.
Its polar frame W_f=Phi_f*(Phi_f^dagger Phi_f)^(-1/2) has orthonormal columns.
The singular-value identity gives

```text
||Phi_f-W_f||_F^2 = sum_i(sqrt(lambda_i)-1)^2 <= eta_f.
```

Extend W_f to a complete orthonormal basis of the ORIGINAL K-qubit word
space. A public unitary U_f sends those M columns to the SAME known basis
states |e>, for all f. On eta_f>=1 use identity; do NOT reject the branch.
No actual fault or secret is passed to this transform.

Compute the full frequency into a blank register, retain it coherently, and
apply U_f to the original word. For each error e in E the resulting state is
close to

```text
|e> tensor sum_f sqrt(d_f/L)*chi_S(f)|f>.
```

Good branches contribute squared distance<=sum_f p_f*eta_f. Bad branches
have squared distance<=4 and Born mass<=sum_f p_f*eta_f. A convenient loose
total bound is5*sum_f p_f*eta_f, uniform for EVERY fixed secret and each
error in E. The explicit finite matrices implement the actual controlled
unitary and frequency-bit readout; they do not erase an unknown vector by fiat.

Measuring X on the high bit of the first frequency coordinate reads the
original S_1 mod2. The ideal correct probability is the clean occupancy overlap
from DCP_NATIVE_PARITY_BRIDGE.md. Averaging (2), then applying Cauchy to the
state distance, gives a source-average loss at most

```text
sqrt(20*M*(M-1)*(G-1)/L).                               (3)
```

This is NOT arbitrary encoded quantum-state correction or an operator-norm
bound on all possible superpositions. The stated original phase family has
the actual Born frequency weights, which are essential to the proof.

Alignment must include relative PHASES, not just per-fiber fidelities. Multiplying
each U_f by(-1)^(high_bit(f_1)) changes none of its individual output densities,
but it reverses the target X outcome after coherent recombination. An actual
controlled-unitary test changes perfect parity readout to a perfectly wrong bit.
Known gauges can be repaired explicitly; unknown/unproven gauges are not free.

## 4. Native Independent Noise Is Information-Theoretically Tolerable

At t=n+8,K=2*n*t, independent original Z probability1/(2n) gives mean error
weight t. Choose the FIXED set of all errors of weight<=2t:

```text
M=sum_(j=0..2t) binom(K,j)=2^(O(n log n)).
```

The standard threshold2mu Chernoff estimate bounds its omitted probability
by(e/4)^t<(11/16)^t. The rational outward constant follows from
e<=sum_(j=0..4)1/j!+1/100<11/4. The implementation uses exact rational powers.

Combining the clean occupancy loss, (3) and this paid error tail yields a
suitable arbitrary controlled-frame-unitary parity failure bound

```text
0.5*sqrt((G-1)/L)
 + sqrt(20*M*(M-1)*(G-1)/L)
 + (11/16)^t, capped1.                                 (4)
```

Since L/G=2^(n*t), the multimode term eventually decays despite the large
pattern library. Current conservative analytical failure bounds are<=2^-21
at n32,<=2^-38 at n64 and<=2^-73 at n128. The n8/n16 bounds are VACUOUS.
These are existence/information statements under original independent Z noise,
NOT large native circuit executions or polynomial algorithms. The sampler/
single-SWAP upper bound and this information escape are compatible: the
controlled frame transport can preserve MULTIPLE error modes rather than one.

## 5. Why This Still Does Not Solve DCP

The prototype enumerates2^K words, groups full arithmetic fibers, constructs
M frame columns, takes SVD/QR and stores dense2^K-dimensional U_f matrices.
Its time, advice and memory are exponential. The analytical M itself is already
2^(O(n log n)); enumerating it is NOT polynomial. Near-orthogonality does not
provide an efficient discrimination or basis-change circuit.

That memory refers to the CLASSICAL dense reference, not a quantum-width lower
bound. The original word plus full-frequency register uses K+n*t qubits before
arithmetic scratch; an arbitrary long gate decomposition need not store a dense
matrix coherently. Uniform description, gate count and efficient synthesis are
still missing. Exponential simulator memory is not itself physical impossibility.

The research target is now explicit: a UNIFORM physical transform exploiting
the public modular arithmetic and phase-error structure, coherently aligned
across paired frequency branches, without enumerating errors/fibers or using
free QRAM, preparation inverses or private fault labels. Prove every access,
finite-gate precision and source cost. A generic search over M error modes
would still have prohibitive scaling; merely invoking a matrix function is
not an algorithm.

There is an additional normalization trap. A column-preparation circuit
|j>|0> -> |j>|F_(f,e_j)> still retains j. Projecting that label onto a uniform
padded P=2^ceil(log2 M) state gives the raw frame map Phi_f/sqrt(P), not Phi_f.
Even an exactly orthogonal frame then has success1/P in the adjoint erasure
step; generic amplification has characteristic sqrt(P) overhead. At n64 the
recorded mode count needs1066 binary bits, so this generic route is grossly
exponential. This is a cost of that construction, NOT a lower bound on every
structured transform. Tests verify the penalty on an exactly orthogonal frame
where a different explicit structured transform is in fact easy.

## 6. Essential Counterexamples And Scope

If d=(A mod2)^T*u then (-1)^(d.x)=(-1)^(u.f mod2) is constant on F_f. Such
label-adaptive aliases have Gram magnitude1, so (1) cannot be reused with a
d chosen after observing A. Tests show this failure over a complete source.

However the resulting error shifts S by(q/2)*u, which PRESERVES its low parity
for t>=2. A known dense clean parity observable still reads that bit despite
these aliases. Thus Gram-near-identity is SUFFICIENT, not necessary: do not
demand that every error mode be distinguishable or declare all bad frames
fatal. The prototype's identity fallback can fail even where another valid
measurement succeeds. A separate positive alias control demonstrates this.

The physical controls include exactly orthogonal known modes, nonzero Gram
overlaps with actual approximate polar transport, bad frames retained without
filtering, and all finite secrets/possible errors using the same public
unitaries. Small dyadic/repeated-label controls are algebraic calibration, not
new toy oracle candidates or native performance evidence. Float circuit checks
are numerical, not exact algebraic certificates; the Gram gates/moments use
exact integer and rational arithmetic.

Independent/label-independent noise is crucial. Correlated secret-dependent
faults, actual lattice preparation, accessible purification and source precision
remain separate obligations. There is no general fault-tolerance result here.

Prior-art context: [Knill and Laflamme](https://arxiv.org/abs/quant-ph/9604034),
[Beny and Oreshkov](https://arxiv.org/abs/0907.5391), and the subset-sum measurement
connection of [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
They are context, not attribution of this local bound or proof of its novelty.
External theorem review remains necessary before relying on these estimates.
