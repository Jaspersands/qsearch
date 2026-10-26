# Original Chain: Support Geometry Does Not Justify Another Tuning Campaign

## Decision

**Deprioritize this guide optimization.** On the original nonlinear-chain
problem, using shared vertices between adjacent tests gives only a small
same-decoder improvement. More importantly, an exact local-operator
certificate bounds the whole specified guide class, not just the fitted
ansatz. This is a finite structural diagnosis, not a Shor-level result.

The source problem and relative-decoding framework are from
[Shang and Stilck Franca, arXiv:2609.35101v1](https://arxiv.org/abs/2609.35101).
We do not claim novelty for that framework or for preparing arbitrary
source polynomials. This pass changes the guide on the **same** adjacent
nonlinear residual task; it does not change to paired or triple orbits.

Implementation: `theorems/chain_support_budget.py`. Exact replay artifact:
`research/reductions/chain_support_budget.json`. Independent mathematical
review remains pending. No central claim admission, quantum execution,
coherent gate count, or classical speedup claim.

## Input And Mechanism

There are `M+1` distinct evaluation points over an odd prime field. Return
one polynomial `P` of degree `<n` with many passing tests

```
r_i = P(alpha_(i+1)) + b_i P(alpha_i)^2 in F_i.
```

The sets are explicit equal-density tables, `rho=|F_i|/p`; all `b_i` are
known and nonzero. The native parameters remain `p=2053, M=2051, n=205`,
`rho=1026/2053`. No native input is resampled. The calculation holds for
any such tables and multipliers, rather than depending on one frozen seed.

Dropping the code constraint leaves independent uniform residuals, since
`(x_0,...,x_M) -> (x_0,r_0,...,r_(M-1))` is a triangular bijection.
Let `u_i=1[r_i in F_i]-rho` and `v=rho(1-rho)`. The products `u_S` are
orthogonal, with squared norm `v^|S|`.

A subset of path edges with `d` selected edges and `r` nonempty runs touches
exactly `c=d+r` vertices. Its Fourier transform therefore has Hamming support
at most `c`. Use the entire space

```
V_K = span {u_S : covered_vertices(S) <= K}.
```

The old degree-`D` space is contained in `V_(2D)`, but adjacent selections
allow degrees larger than `D`. Source terms with different edge selections
can overlap in Fourier space and interfere. They are NOT an incoherent
distribution of independent edge errors; the FFT regression checks this.

Two guide terms depend on at most `2K` evaluations. Inserting `j` objective
factors adds at most `2j` evaluations. RS interpolation therefore proves
exact normalization and moment transfer when

```
2K + 2j <= n.
```

The existing syndrome-only whole-cap Hamming Prony decoder needs `2K`
syndrome coordinates. No new structured burst decoder is assumed.
`K=100` permits two moments at `n=205`; `K=101` permits the mean only.
This pass computes no new second-moment certificate.

## Constructive Lower Witness

We compress multiplication by the score to functions uniform within each
`(d,r)` class. The number of subsets in a class is exactly

```
N(d,r) = binom(d-1,r-1) binom(M-d+1,r),       d,r >= 1,
N(0,0) = 1.
```

In the normalized product basis the score operator is

```
A = M*rho*I + (1-2*rho) sum_i n_i + sqrt(v) sum_i X_i,
```

where `n_i` records whether `i` is selected. Adding an edge either bridges
two runs, extends a run, or creates a run. For `z=M-d`, the respective
TOTAL directed flip counts from class `(d,r)` are

```
B = binom(d-1,r-1) (r-1) binom(z,r-1),
I = binom(d-1,r-1) (r+1) binom(z,r+1),
E = z*N(d,r) - B - I.
```

Targets are `(d+1,r-1)`, `(d+1,r+1)`, and `(d+1,r)`. The empty class has
`M` additions to `(1,1)`. Tests enumerate every bit string through `M=8`
to check both these counts and the covered-vertex formula.

The compressed matrix has polynomial dimension `O(K^2)` and is sparse.
Its eigenvector only proposes coefficients. The stored guide is

```
g = sum_(d,r) a_(d,r) sum_(S in class(d,r)) u_S,
```

with explicit rational `a_(d,r)`. Its norm and mean are recomputed as exact
rational numbers. A floating eigenvalue is never used as a certificate.
The old radial guide is independently embedded and recovers its exact
norm/mean. The compressed matrix is NOT an invariant subspace: squaring it
does not give the second moment. A leakage regression enforces this limit.

This ansatz has an efficient ideal source-preparation route: prepare the
polynomial-size `(d,r)` register with weights proportional to
`a_(d,r)*sqrt(N(d,r)*v^d)`; prepare uniformly selected positive run lengths
and admissible gaps by combinatorial unranking; map the resulting selection
bits isometrically to the local orthonormal pair `(1,u_i/sqrt(v))`, after
uncomputing `(d,r)` from the selection string; add a
uniform root, invert the residual bijection, and Fourier transform.
Explicit table access and reversible arithmetic must be paid for. Their
cost is polynomial in the explicit input size, not necessarily in `log p`.
Finite-precision synthesis and a full gate/error budget are still absent.

The source also admits classical transfer-matrix sampling. That does not
sample a code-constrained polynomial; efficient source sampling alone is
not a dequantization argument.

## Upper Certificate For The Whole Specified Space

The lower witness above is only a Ritz ansatz. The following upper bound
holds for EVERY complex-amplitude vector in `V_K`.

Write the path cost operator as
`C_path=2 sum n_i - sum_(i=1)^(M-1) n_i n_(i+1)`.
Close the chain into a cycle:

```
C_cyc = C_path - n_M*n_1 <= C_path.
```

For any feasible unit vector, `<C_cyc> <= K`. For `lambda >= 0`,

```
<A>/M <= rho + lambda*K/M
          + lambda_max((1-2rho) sum n_i + sqrt(v) sum X_i
                       - lambda*C_cyc)/M.
```

On a cycle of `M >= ell` sites, sum all translated length-`ell` windows of

```
h_ell = (1-2rho)/ell * sum n_i + sqrt(v)/ell * sum X_i
         - lambda * (2/ell * sum n_i
                     - 1/(ell-1) * sum_(internal bonds) n_i*n_(i+1)).
```

Each site occurs `ell` times and each bond `ell-1` times, so the sum is
exactly the operator above. Subadditivity of the largest eigenvalue gives
an upper bound of `M*lambda_max(h_ell)`. No translation invariance of the
guide or independence of occupancies is required.

Replace `sqrt(v)` by `1/2`. These real symmetric matrices have nonnegative
off-diagonal entries; after a scalar identity shift, Perron-Frobenius
monotonicity proves that this replacement upper-bounds the largest
eigenvalue. It is NOT an assertion of an operator PSD ordering.

Use `ell=4`, `lambda=8/5`, and `mu=7761/100000`. The code clears rational
denominators of `mu*I-h_ell` and computes all 16 leading principal minors
with exact FLINT integer determinants. Every minor is strictly positive,
so Sylvester's criterion proves `lambda_max(h_ell)<mu`. The resulting
universal class bound is

```
mean_fraction < rho + (8/5)*K/M + 7761/100000.
```

The artifact stores all minors and parameters. Its verifier recomputes
them; it rejects a changed score bound or an insufficient eigenvalue cap.
The periodic-window identity is also checked exactly on all 7-site words.

## Findings And Falsifiers

At `K=100`, the exact rational guide has mean fraction
`0.6439395549989568`, compared with `0.6431342271562736` for the degree-50
guide. The increase is only **0.0805328 percentage points**. The whole
`V_100` class has certified mean fraction below `0.655377181`.

The artifact also evaluates the full mean-only support allowance `K=101`,
giving `0.6447097820946768`; its entire class is below `0.656157288`.
This prevents an artificial stopping
point at `K=100`, but does not support a new tuning campaign.

These bounds do not exclude an asymptotic advantage below that ceiling.
They do not establish any classical lower bound. They do not constrain
all decodable sources, other local basis functions, high-cost terms whose
Fourier components cancel, stronger decoders, different codes, or arbitrary
quantum algorithms. They apply only to the explicitly defined `V_K`.

Falsifiers for the derivation are an incorrect local predicate matrix, a
wrong flip count, a failed principal-minor certificate, a violation of
the periodic-window identity, or Fourier support beyond the vertex budget.
Current exact/enumerative controls pass. Independent proof review could
still invalidate the conclusion.

**Next scientific work must change a real bottleneck:** a constructive
decoder/source mechanism outside this class, a meaningful reduction to a
natural task, or a genuinely independent direction. Neither more shell
tuning nor a larger finite seed campaign meets that criterion.

## Reproduction

```
python theorems/chain_support_budget.py
python -m pytest -q tests/test_chain_support_budget.py -W error::RuntimeWarning
```

No CLI/UI wiring or central registry promotion is requested. Mechanical
reruns must preserve both the exact proof scope and the original problem.

Validation: 15 new / 152 connected tests passed with runtime warnings fatal;
Python syntax, all 12 site JavaScript syntax checks, site checks, and
`qsearch.py validate` passed. This was not a full-repository test run.
