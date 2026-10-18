# Coarsen Less: Linear Accessible Information Without A Fiber Inverse

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This is a conditional positive
information result for the actual growing-modulus source/readout. It supplies
no efficient decoder, natural source reduction, classical hardness theorem,
or speedup. Run `python theorems/dcp_coarse_readout_information.py --write`.

## Precise Statement

Take q=2^(n+8) and IID uniform full public labels
A in Z_q^(n x m). The unknown original secret S is uniform in Z_q^n. Each
original qubit has visibility at least1-1/n from secret-independent Z faults.
Independent faults suffice; arbitrary correlations are also allowed if their
distribution is independent of S and all marginal visibilities meet the
promise. Do not assume this is the actual noise of a natural lattice reduction.

Measure a componentwise mod2^b syndrome, b1 or2, ignore its value if desired,
apply H to every original qubit and measure the complete Z string Z. For
residual secret C=S mod(q/2^b), n>=64, the following conditional bounds hold:

    b1, m3n: I(C;Z | A=a) >= n/4 bits,
    b2, m5n: I(C;Z | A=a) >= n/16 bits.

Each holds on EVERY A with injective full Boolean frequency map. Failure
probability is <2^(-n^2-3n) for m3n and <2^(-n^2) for m5n. Keeping the syndrome
can only increase mutual information.
These are not pointwise guarantees for every possible measured syndrome y.
This is ACTUAL classical readout information, not merely a Holevo lower bound.
It is one-block, uniform-prior information; it is NOT a full-secret recovery
probability, a sample-complexity upper bound, or a computational algorithm.
The real readout's C versus-C alias remains. No contradiction arises: the
target is mutual information, not an impossible full-identification guarantee.

## Proof: First Bound The Simpler Original-Source Baseline

Before syndrome pinching, measuring each phase qubit in X gives

    Pr(Z_i=z_i|S)= [1+(-1)^z_i v_i cos(2*pi*<A_i,S>/q)]/2.

Correlated Z noise need not factor the FULL outcome distribution. Nevertheless
its single-wire marginals have this form, and conditional entropy is at most
the sum of marginal entropies. If x->A*x modq is injective, averaging the full
original phase density over S gives I/2^m by character orthogonality. Any
secret-independent Z channel is unital, so the average X-output string is
exactly uniform. Hence H(Z)=m, even for correlated faults.

For fixed A_i, <A_i,S> is uniform on a dyadic subgroup of Z_q. Let theta
denote its phase and v any common marginal visibility lower bound. Binary
entropy has the convergent expansion

    h2((1+x)/2)=1-(1/ln2) sum_(k>=1) x^(2k)/(2k(2k-1)).

The finite subgroup average of cos(theta)^(2k) is at least
binom(2k,k)/4^k: its Fourier coefficients are nonnegative, and averaging keeps
the constant coefficient plus possibly additional nonnegative harmonics.
This includes zero/order-two columns; no primitive-column condition is needed.

Since exp(7/10)>1+7/10+(7/10)^2/2+(7/10)^3/6=12013/6000>2,
ln2<7/10. Define the EXACT RATIONAL lower rate

    alpha_L(v)=(10/7) sum_(k=1)^L
                  v^(2k) binom(2k,k)/(4^k*2k*(2k-1)).

Dropping only positive terms yields

    I(S;Z)_raw >= m*alpha_L(v).

This is an information lower bound for a SIMPLE ORIGINAL-PHASE MEASUREMENT,
not proof of an advantage from syndrome projection or collective processing.

## Charge Exactly What The Coarse Projection Removes

Decompose S=C+Q*H, Q=q/2^b, C uniform in Z_Q^n, H uniform in Z_(2^b)^n independent
of C. The syndrome pinching channel is the uniform diagonal twirl

    E( rho_S ) = 2^(-bn) sum_(u in Z_(2^b)^n) rho_(S+Q*u).

Secret-independent Z faults commute with this twirl. Therefore the discarded-
syndrome X-output channel at C is EXACTLY the original product-measurement
channel averaged over H. Classical information chain rule gives

    I(C;Z)_pinched = I(S;Z)_raw - I(H;Z|C)_raw
                  >= m*alpha_L(v)-bn.

No fiber enumeration, inverse, PGM, postselection or normalization oracle enters
this argument. The lossbn is the entropy of the hidden secret coset label, not
a claim that an arbitrary channel of small output dimension cannot lock data.
This EXACT twirling identity is essential; do not replace it by such a general
and false information-loss intuition.

With L16, alpha_16(63/64)>.4177. Exact rational arithmetic gives
3*alpha_16(63/64)-1>1/4 and5*alpha_16(63/64)-2>1/16. Alpha is increasing in v,
so the two bounds follow for every n>=64 and v>=1-1/n. At n64, the mod2/m3n
bound is16.2037 bits; the mod4/m5n bound is5.6729 bits. The native n256
mod2/m3n bound is75.4454 bits, not a finite known-secret measurement plot.

Failure of full frequency injectivity requires A*d=0 modq for some nonzero
d in{-1,0,1}^m. Every d has a unit coefficient, giving probability q^-n.
A union bound gives(3^m-1)/q^n. For m3n, 3^3=27<32=2^5, giving the first
failure exponent. For m5n, 3^5=243<256=2^8 gives the second. There is no source-dependent choice of favorable
syndrome or free repeated-copy promise.

## A Cheaper Matched Measurement Baseline Is Already Available

The SAME discarded-syndrome output law needs no coherent syndrome register:
draw uniform u in Z_(2^b)^n. For b1, apply Z^(sum_l u_l A_li mod2);
for b2, apply S^(sum_l u_l A_li mod4) to original qubiti,
apply H, measure all original wires and ignore u for this comparison. The exported actual plan
uses at mostm Z gates for b1 or3m S gates for b2, plus m H gates,
no ancillas, with bn random bits. It
requires the same UNKNOWN-secret phase qubits. It is not a classical sampler
for unknown-secret data. The equality asserted is for the z MARGINAL, not
the complete recorded twirl/syndrome instruments. Twirl values may be retained;
retaining records cannot weaken the information lower bound. Do not equate
the two full recorded instruments or silently change nuisance-secret priors.

For parity-only projection there is also an exact coherent compression:
the existing affine-coordinate CNOT/X compiler clears rank(A mod2) pivot
wires, with no higher syndrome measured or imposed. Measure H only on its
remaining k=m-r wires. If V_j are the original binary kernel directions,
the full original X outcome z enters probabilities only through
w_j=<z,V_j> mod2. Every w has2^r equally probable preimages independent of
secret and syndrome. Hence the compressed free-wire readout has exactly the
same information as complete original X readout, including after ignoring y.
This requires V chosen by A mod2 independently of the syndrome, as in RREF.
No enumeration of the2^k affine domain is used by the compiler.
Unlike the mod4 case, this affine lift DOES index the complete measured
PARITY fiber; no unmeasured high-bit constraint is imposed. It is an explicit
Clifford compilation, not an assumed full-quadratic-fiber oracle. At m3n,
full binary rank gives k2n except probability<2^-2n; rank-deficient cases use
their actual k. That rank probability is SEPARATE from the stronger frequency-
injectivity event needed for the information lower bound.

Noise is not reset by compression. For independent original Z faults, free
coherences use v^weight(V*(u XOR u')). For correlated faults they use the
ORIGINAL error-character expectation E_e(-1)^<e,V*(u XOR u')>, not a product
of marginal free-wire visibilities.

Thus the bound does NOT establish the necessity or superiority of retained
coherent blocks. It establishes that a modest width change removes the
specific fixed-readout information bottleneck. The old MOD4/width3n upper bound
cannot be extrapolated to MOD2 or every polynomial packet width. Conversely,
the new lower bound does not falsify that scoped result or the bounded-SQ gates.

## Revised Research Decision

Prefer the less destructive one-bit projection when exploring actual
correlated packet inference. Do not measure an extra residue bit merely to
make the nominal phase modulus descend faster. Mod2 and mod4 produce
DIFFERENT residual-secret targets; this is not a same-target algorithmic
speedup comparison. If two successive parity layers are required, preserve
the higher carries/noise and pay their true joint source law; restarting IID
phase qubits remains unjustified. Wider packets are a separate valid escape.

## What Remains Hard

Even ordinary dihedral coset states have long-known measurement records with
sufficient information but difficult postprocessing; see
[Ettinger-Hoyer](https://arxiv.org/abs/quant-ph/9807029) and
[Kuperberg's cosine-observation discussion](https://arxiv.org/abs/quant-ph/0302112).
No novelty claim is made for the sample/inference distinction or single-qubit
readout. Our next task is a computationally efficient decoder for the actual
growing-modulus full transcript, or a better physically paid collective method.

Do not invert mutual information into a recovery guarantee. Nor may the
uniform-prior lower bound be chained through arbitrary adaptive posteriors.
Unknown-secret source preparation, its real noise, classical postprocessing,
measurement-record access and end-to-end asymptotics remain proof obligations.
Positive finite likelihood tables are EXPONENTIAL calibration only.

Nine complete controls include clean/noisy/dephased sources, a two-component
source, common-mode correlated faults, and a noninjective zero-label source
that must NOT receive the injectivity-dependent certificate. Tests replay
original density operators, both mod2/mod4 twirls, actual parity compression,
entropy-series constants and noise
correlations, rather than only asserting favorable metric flags.
