# Native Parity: Sparse Measurements Fail Under The Stated Noise, Not All Circuits

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This is a scoped measurement-class
bound with explicit positive controls, not a general DCP lower bound, new
algorithm, novelty claim or new active negative result.

Run `python theorems/dcp_native_parity_observables.py --write`. The live artifact
is `phase_workbench/dcp_native_parity_observables.json`, with matching hypothesis
contract and physics tests. It extends the original-input useful-bit model in
DCP_NATIVE_PARITY_BRIDGE.md rather than introducing a new oracle problem.

## Research Decision

The conditional cyclic-DCP reduction needs the FIRST secret bit, not merely
large total information. Enough original copies are necessary but not a
decoder. For the exact independent benchmark noise, simply finding disjoint
full-modulus frequency pairs is also insufficient at K=2*n*t: native target
edges are long, so their individual coherences are exponentially attenuated.

The next constructive target is a structured DENSE observable or a different
noise-tolerant collective procedure on the original input. Sparse effective
observables and small circuits are NOT the same class. An explicit polynomial
circuit counterexample below prevents that dangerous inference. Clean sources
and other noise models must be evaluated separately.
Dense observables can also arise from PRODUCT measurements followed by an
efficient nonlinear classical decision. A collective quantum readout is not
therefore mandatory; the required object is the complete decision observable.

## 1. Actual Effective Observable, Not Gate Count

Any final binary guess on original input density rho_S has POVM effects
E_0,E_1, E_0+E_1=I. Set O=E_0-E_1, so O is Hermitian and ||O||<=1. For a
uniform secret and target bit S_1 mod2, prediction advantage is

```text
adv = Tr[O*(rho_even-rho_odd)]/4.
```

All intermediate ancillas, adaptive feedback and measurements can be included
in this effective observable. It is independent of the unknown secret but may
depend arbitrarily on ALL public full labels. Rejected outcomes must be paid:
assigning a fair random guess on rejection measures acceptance times its
conditional advantage. The result does not bound a normalized postselected
success rate without its acceptance cost.

Let L=2^K, f_x=A*x modq and h=(q/2,0,...,0). For ORIGINAL INDEPENDENT Z faults
with common visibility v,

```text
Delta[x,y] = (rho_even-rho_odd)[x,y]
           = 2/L * v^Hamming(x,y) * 1[f_x-f_y=h].
```

Define D as a certified bound on the number of nonzero entries O[x,y] per
row that ALSO satisfy f_x-f_y=h. Other observable entries do not enter this
bit advantage. A numeric threshold on tiny floating entries is NOT a support
certificate. If every target edge has Hamming distance>=w, then

```text
|adv| <= (1/(2L))*v^w*sum_x sum_(target y)|O[x,y]|
      <= (1/2)*sqrt(D)*v^w.
```

The last step uses row l2 norm<=||O||<=1 and Cauchy-Schwarz. The implementation
uses ceil(sqrt(D)), caps at the physical1/2, and uses exact integer powers for
its outward power-of-two bound. No floating underflow produces zero evidence.

## 2. Native Short-Edge Exclusion

Every target edge gives a signed vector d=x-y in{-1,0,1}^K with A*d=h. A
nonzero d has a unit coefficient, so its image is uniform over Z_q^n even
though q is a power of two, not a field. At support weight j there are
binom(K,j)*2^j signed vectors; d and -d represent the same event because
h=-h. The union bound is therefore

```text
Pr_A[there is a target edge of weight<=r]
 <= q^(-n)*sum_(j=1..r) binom(K,j)*2^(j-1).
```

The producer finds the LARGEST r whose exact union count is at most
q^n*2^-b. It records the integer count in hexadecimal and charges the label
exceptions by1/2*2^-b. There is no full-rank filter or selected-label admission.
The K budget includes ALL original draws, not just retained samples. Chosen
labels, accessible preparation environments and secret-dependent label laws
are not covered. Pad bounded adaptive sampling to K pre-drawn IID samples.

For n64,t72,K9216,b64 it certifies minimum target distance762 outside probability
<=2^-64. At independent v63/64, disjoint pairing (D1) has unconditional average
advantage<=2^-18. Even target degree<=n^4 has average advantage<=2^-6, below
the1/16 predictor contract. At n128 the corresponding exponents are33 and19.
These are conservative upper bounds, not measured native decoder performance.

### An Asymptotic Check Independent Of The Numerical Frontier

For N=n*t, K=2N, choose r=floor(N/16). At z=1/16, positivity of generating
function coefficients gives

```text
sum_(j=1..r) binom(2N,j)*2^(j-1)
 <= (1/2)*16^r*(1+1/8)^(2N)
 < (1/2)*2^(3N/4),
```

because (81/64)^2<2 and4r<=N/4. The exception probability is<2^(-N/4-1),
which is<=2^-n for the native t=n+8. Hence w=r+1>N/16 and

```text
adv_good <= (sqrt(D)/2)*exp(-(n+8)/16),
```

using (1-1/n)^w<=exp(-w/n). Every fixed polynomial D gives exponentially
small advantage, plus the charged exponentially small label exceptions.
The bound also excludes subexponential-in-n target degree from giving an
inverse-polynomial advantage asymptotically. It does NOT exclude dense
observables implemented by polynomial circuits.

## 3. Physical Pairing And Dense Positive Controls

For each public label matrix, the bounded reference constructs the weighted
kernel B[x,y]=v^Hamming(x,y)*1[f_x-f_y=h]. Unordered frequency pairs{f,f+h}
give bipartite blocks

```text
[[0, C_f], [C_f^dagger, 0]],
C_f[x,y]=v^Hamming(x,y), x in F_f, y in F_(f+h).
```

The physical Helstrom advantage is exactly sum_f||C_f||_*/L, with each pair
counted ONCE. For clean inputs each C_f has rank one, recovering the subset-sum
occupancy overlap. Independent noise can increase block rank; replacing it by
a clean overlap with an unexplained average visibility is not valid.

A public greedy disjoint pairing defines O[x,y]=O[y,x]=1 on paired target
vertices, zero elsewhere. It is a valid observable: perform a two-level
Hadamard on each pair, distinguish its plus/minus basis outcomes, and guess
fairly on unmatched vertices. No favorable-branch renormalization is used.
For EVERY fixed secret it achieves advantage sum_pairs v^distance/L.
The finite tests execute this basis change on actual original density matrices,
not a simulator's sampled secret/error tags.

Dense diagonalization supplies a second valid POVM, the spectral sign of B.
On labels(2,2,2,2) mod8 with v3/4, actual pairing success is.7109375 while
the collective reference reaches approximately.79317154. These small matrices
are algebraic calibration, NOT a proposed new oracle family or a native scaling
claim. Allocation of L^2 entries and L-dimensional eigendecomposition is
explicitly charged as exponential reference work. No finite-gate implementation
or efficient method of obtaining the required singular vectors is supplied.

## 4. Two Essential Countercontrols

**Gate sparsity is not observable sparsity.** The circuit

```text
H^K * (I-2|1^K><1^K|) * H^K = I-2|minus^K><minus^K|
```

uses2K Hadamards and a multi-controlled Z with a polynomial clean-ancilla
decomposition. Its effective observable has2^K-1 nonzero off-diagonal entries
per row. On the structured label fixture a_i=h, half the entries per row are
target couplings. This is not native typicality or an algorithm; it falsifies
the inference that polynomial gate count forces small D.
Even simpler, perform K Hadamards, measure all wires, and output minus exactly
when all outcomes are one. This product-X readout plus a polynomial classical
AND has EXACTLY the same effective observable. The sparse-class bound does not
exclude efficient nonlinear processing of many local measurement outcomes.

**Marginal visibility is insufficient.** With labels(2,2) mod8, shared all-Z
faults can have zero single-qubit marginal visibility while preserving the
weight-two target coherence and giving pairing success3/4. Independent
zero-visibility noise gives success1/2. The stronger independent-noise bound
must not migrate to the earlier correlated-noise information theorem.

Finally, merely computing f_x into a fresh register leaves orthogonal x
garbage. Applying H to its target bit then ignoring x gives an exactly fair
bit, even on a source with high optimal success. The earlier
DCP_SUBSET_SUM_MEASUREMENT_AUDIT.md already establishes the general retained-
input problem. Fast classical modular arithmetic does not solve coherent
fiber processing or the noisy block singular-vector problem.

## What Would Change The Research Decision

Rank and noise must not silently define the wrong search space. At the SAME
modulus2^t and per-qubit visibility1-1/(t-8), K=2*(t-8)*t growing-rank samples
have t expected injected Z faults, whereas2*t scalar samples have only
t/(t-8). The artifact includes both, plus the clean growing-rank case.
For scalar rank1 with K=2*t, even a maximum-weight target edge has attenuation
at least(1-1/(t-8))^(2*t), approaching a nonzero constant. The growing-rank
exponential attenuation argument therefore does NOT transfer to scalar DCP.
This lower attenuation bound does not prove target edges or a receiver exist.
Expected fault count is not decoder failure probability. The conditional
scalar-to-native lift need not inject noise when a CLEAN native predictor is
available. A noisy high-rank obstruction must not suppress clean or fixed-rank
algorithm ideas, which may be easier and still scientifically important.

Construct and cost a polynomial circuit for a dense target-coupling observable
with inverse-polynomial native average advantage; prove a stronger exploitable
structure of the weighted frequency blocks; or exhibit a different physical
protocol outside this sparse class. Attempt to falsify every proposed circuit
against the exact original-source kernel, including all rejected draws and
noise. No general negative belongs in the registry from this scoped bound.

The bit-measurement/subset-sum connection is prior art:
[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
The scoped calculations here remain review-pending, not independently certified
new theorems. A known identity plus a new filename is not a research breakthrough.
