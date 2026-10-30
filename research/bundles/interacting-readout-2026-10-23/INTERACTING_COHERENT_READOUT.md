# Interacting Conditional Chains: A Matched Classical Pauli Estimator

2026-10-23. LOCAL DERIVATION, INDEPENDENT REVIEW PENDING. No quantum speedup,
novelty admission, kernel-checked theorem, or general TFD simulation claim.

## Decision

The interacting chain in `research/RELATIVE_GIBBS_WORLDLINE.md` does not
escape the existing conditional-product Pauli-readout attack merely by
adding nearest-neighbor quantum-spin interactions. The paired estimator
never required a product state: only its efficient evaluation did.
Constructive 1D half-Gibbs MPO approximations supply that evaluation.

This closes a specific written gap in `research/COHERENT_GIBBS_READOUT.md`,
subject to the proof and numerical contracts below. It does not make an
arbitrary coherent quantum task classically easy. No large simulation or
new candidate search is justified by this observation.

Subsequent same-day review: `../bell-readout-2026-10-23/BELL_READOUT_DECISION.md`
gives a broader prior-art CT-state baseline when an efficient classical
relative decoder and source amplitude evaluation are available. That route
does not need the worldline sampler or conditional target-chain structure.
The present result retains a distinct decoder-free scope, but building its
full thermal backend is lower priority than resolving the actual useful
output task. The same follow-up gives decoder-free Bell-label sampling.

## Inputs, Output, And Dependencies

The public input is a binary r-by-N matrix F, explicit rational coefficients
of magnitude at most J0, and beta. Define

```
c_i(z) = (-1)^(F[:,i] . z)
H = sum_i [a_i X_i + (b_i + h_i c_i(Z_R)) Z_i + e_i c_i(Z_R) I]
    + sum_i j_i Z_i Z_(i+1).
F_z = exp(-beta H_z/2),  w_z = ||F_z||_F^2,  p(z) = w_z / sum_u w_u.
```

The letter F denotes the binary input matrix; F_z denotes a thermal filter,
not a submatrix. The target is the canonical TFD, vectorizing the FULL
block-diagonal filter, and one supplied Hermitian Pauli product on its two
copies. We estimate its expectation to ADDITIVE error. Coefficients, beta,
and binary labels have polynomial input bit lengths; beta J0 is fixed.

Three separate ingredients are required:

1. The correlated worldline source-to-target sampler already derived in
   `RELATIVE_GIBBS_WORLDLINE.md`, including its mixing, Trotter, arithmetic,
   code-distance, and ABSTAIN allowances. Discarding its local-spin output
   leaves a central label drawn within the same TV allowance of p.
2. A relative Frobenius approximation M_z for each requested half-Gibbs
   filter, with `||M_z-F_z||_F <= eta ||F_z||_F`, uniformly over input z.
3. Contractions evaluated with a charged additive arithmetic error.

[Kuwahara, Alhambra and Anshu, Theorem 3, Eqs. 23-25](https://arxiv.org/html/2007.11174v2#S4.SS1)
construct an MPO approximation with relative Schatten-norm error. Apply
their result at half the inverse temperature, with p=2, after rescaling
the bounded local terms. At fixed beta J0, inverse-polynomial accuracy has
polynomial construction cost and bond dimension. This is a constructive
theorem, not an inference from the existence of a thermal area law. No
thermal-MPO implementation or finite-precision certificate is supplied by
this bundle.

The target family and certified temperature regime come from
[Shang, Wang and Stilck Franca, Theorem 8.1](https://arxiv.org/abs/2610.06667v2).
The paper's preparation claim is NOT contradicted by a classical estimator
for a particular readout task. We do not ascribe a hardness claim to it.

## Paired Identity Without Product Blocks

Write the central Pauli factors as `i^(#Y) X^x Z^t`. If the two central X
masks differ, the answer is zero, since both TFD copies share their label.
Otherwise their common mask v defines z' = z xor v. Let A and B be the
Pauli factors on the two local chains. Set

```
phase(z) = i^(#Y_L+#Y_R) (-1)^((t_L xor t_R).z')
G(z) = phase(z) Tr(F_z^dagger A F_z' B^T)
Y(z) = 2 Re G(z) / (w_z + w_z').
```

Hermiticity of the full observable gives G(z') = conjugate(G(z)).
Pairing the involution z -> z' therefore yields

```
E_(z~p) Y(z) = sum_z Re G(z) / sum_z w_z
             = <TFD|P_L tensor P_R|TFD>.
```

This also holds when v=0. Cauchy-Schwarz gives

```
|Y(z)| <= 2 sqrt(w_z w_z') / (w_z+w_z') <= 1.
```

No global partition sum, minimum-sector-probability bound, enumeration of
2^r labels, independent local-spin premise, or normalized-sector advice is
used. Build exactly the two requested MPOs and contract their double layer
along the chain. Runtime and memory are polynomial in N and their bonds.
The right-hand transpose is essential for Y operators.

## Uniform Perturbation Bound

Let a=||F_z||_F, b=||F_z'||_F, D=a^2+b^2, and kappa=2 eta+eta^2.
Assume 0 <= eta < 1 and both relative-error promises. Replace each F by M
to obtain G_tilde, D_tilde and Y_tilde. Direct triangle inequalities give

```
|G_tilde-G| <= kappa a b <= kappa D/2
|D_tilde-D| <= kappa D
|2 Re G_tilde| <= D_tilde.
```

The last inequality applies even to non-Hermitian approximate MPOs. Thus

```
Y_tilde-Y = 2 Re(G_tilde-G)/D
             + 2 Re(G_tilde) (1/D_tilde - 1/D)
|Y_tilde-Y| <= 2 kappa = 4 eta + 2 eta^2.
```

In particular, an exponentially small w_z or an exponentially imbalanced
pair does NOT cause an inverse-probability penalty. The bound deliberately
uses D in the first term and the Cauchy-Schwarz bound with D_tilde in the
second. Bounding both denominators separately is unnecessarily pessimistic.

The sampler still targets the TRUE p, not weights estimated from the MPOs.
No theorem about sampling the approximate weights is assumed or needed.

## Complete Error And Resource Ledger

Set the estimator to zero on ABSTAIN. If sampler TV is delta and arithmetic
adds at most epsilon_arith per value, the deterministic observable bias is

```
B <= 2 delta + 4 eta + 2 eta^2 + epsilon_arith.
```

For m independent ideal-randomness executions, the bounded estimator has
Hoeffding tail `2 exp(-m t^2/2)` at statistical error t. Charge numerical
evaluation error separately as above. Independent restarts after the
specified burn-in justify this usage. Consecutive correlated heat-bath
samples do NOT justify the same iid formula. A seeded PRNG is a replay
mechanism, not a certificate of fair independent randomness.

For the sampler, let d be a separately established minimum-distance lower
bound for ker F, and let tau be the source paper's constant decoding radius
fraction. In its window d>2 tau N and beta<tau/(5J0), the existing proof has

```
A <= (5/4) (e/5)^d
delta <= mixing + Trotter + arithmetic + A + 2A/(1-A), if A<1.
```

Consequently inverse-polynomial readout accuracy is classical for
sufficiently large N when d is linear. Do NOT silently remove this finite
pinning error floor. Requested accuracy below it is not certified by this
particular composition. Passing controls does not certify code distance.

Each sample pays a source-chain run, pinning and GF2 solving, two thermal
MPO constructions, their norms, and one paired overlap. Reusing previously
built sectors is optional; building all sectors in advance is exponential
and forbidden as a claimed polynomial implementation. For error t and
failure q, m >= 2 log(2/q)/t^2 suffices, apart from B. Polynomially many
supplied Pauli expectations are covered by a union bound. A polynomial-size
Pauli sum with polynomial coefficient l1 norm is also covered with the
corresponding precision and sampling overhead.

Sector-dependent scalar energy offsets MUST be retained. For
H_z=H_z^local+E(z)I, represent M_z with scalar log scale -beta E(z)/2.
Separately normalizing M_z destroys the relative sector weights and changes
the canonical TFD. A gauge used to make transverse coefficients negative
for sampling must either be undone for the MPO or applied to the observable.
Sampling-only gauge changes preserve w_z; they do not license changing G.

## Attempts To Falsify The Composition

- **Product assumption smuggled back in:** actual ZZ terms change the dense
  expectation. The MPO result is checked against the interacting value.
- **Density approximation substituted for its square root:** the imported
  guarantee is for exp(-beta H_z/2) in Schatten 2, not merely a trace-close
  normalized Gibbs density. Only the former is used in this derivation.
- **Exponential normalization cost:** no Z is evaluated. Norm ratios are
  logarithmically scaled; tests include sector norms differing by 100 powers
  of ten and global log scales around 10,000.
- **Wrong Pauli conjugation:** a Y/Y identity-filter control has expectation
  -1, not +1. All central Pauli pairs are checked on complex block filters.
- **Precision smuggled into NumPy:** numerical tensors are diagnostics only.
  The code does not certify relative thermal error or rounding enclosures.
  Production use needs the published constructor and certified arithmetic.
- **Kernel promise inferred from easy data:** the long-chain calibration is
  a known easy bond-two Ising transfer matrix, not a hard code or separation.
- **MPO existence mistaken for construction:** Theorem 3, not just the area
  law, is the required dependency. TEBD convergence at a chosen bond cutoff
  is not a substitute for the relative-error premise.
- **Thermal construction hides a sampling oracle:** the hard central law is
  obtained only by the separately derived worldline-pinning algorithm. This
  step fails outside its stated assumptions even if every sector is easy.

## What Is Still Open

This does not prepare the TFD, reproduce arbitrary circuit output laws,
estimate exponentially small probabilities to relative error, or prove all
HDQI tasks easy. Interactions alone, or naming an observable coherent, do
not identify a useful task outside the attack. A successor needs a concrete
input/output problem and paid quantum procedure that breaks one premise:
central sampling, conditional contraction, temperature/error window, or
efficiently representable observable. Merely appending a Clifford circuit
and measuring one output Pauli still pulls back to a Pauli and is covered.

Independent review of the existing correlated sampler and this composition
is needed. Formal bit-level thermal construction and outward contractions
are not yet implemented. Do not expand this into temperature sweeps or
claim an end-to-end scalable classical implementation from these controls.
