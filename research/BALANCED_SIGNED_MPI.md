# Balanced Signed MPI: A Constructive Readout Extension

## Status

**A substantive algorithmic proof candidate, not a demonstrated speedup.**
We extend a public signed-error construction by using separate positive
and negative degree budgets, including its score readout. The native
ideal mean-cosine lower bound is `0.3421279344361546`. Our exact upper
bound for the old radial guide at its licensed degree is `0.259029641`.
Neither quantity is a measured quantum optimizer result.

The starting problem, log-Cauchy construction and rational decoder are
known from [Mazumder and Niroula, arXiv:2610.06753v1](https://arxiv.org/abs/2610.06753),
Sections 6.2 and B.2. Their wider random-sign recovery result is explicitly
separate from their quantum readout guarantee. We use that distinction as
the research question, not as a license to assume the missing condition.
The earlier decoder is not our invention. Novelty and independent proof
review of this extension remain pending.

Files: `theorems/balanced_signed_mpi.py`,
`tests/test_balanced_signed_mpi.py`,
`research/phase_workbench/balanced_signed_mpi.json` (schema v2).

## Kernel-Checked Algebraic Core

`formal/Formal/BalancedSigned.lean` now proves rational separation over
an arbitrary field, the balanced-box guard, both signed score shifts,
and the encoding/separation of actual integer coordinate arrays.
Multiset roots handle multiplicity and cancellation without assuming
squarefree or already reduced fractions. A separate `ZMod 11`
counterexample checks why the strict readout guard matters; this is
distinct from the saved `F_16` syndrome counterexample below.

All nine audited statements use only `propext`, `Classical.choice` and
`Quot.sound`. The entire pinned Lean 4.35.0/Mathlib project builds with
`lake build --wfail`, including the axiom guards. The connected Python
regression suite passes 189+ tests; syntax, site and registry validation
also pass. These are scoped checks, not a full-repository test claim.

This closes the field-polynomial separation proof obligation only.
The log-to-syndrome bridge, quantum Fourier transfer, coherent
preparation, numerical mean certificate, Python decoder implementation
and complete gate/precision analysis are NOT Lean-verified. Neither
classical hardness nor novelty follows from kernel checking.
Independent review of the full algorithmic argument remains necessary.

## Fixed Task And Access

Let `F=F_(2^h)`, `N=2^h-1>3`, and `g` generate `F*`. Use disjoint distinct
points `t_1,...,t_m,z_1,...,z_n`. The public matrix is

```
B_ij = log_g(t_i+z_j) mod N.
```

Given public centers `c_i`, return `x in Z_N^n` with large mean of
`cos(2*pi*((Bx)_i-c_i)/N)`. All field data, points, matrix entries and
centers are public to both quantum and classical algorithms. No secret key,
sample oracle or hidden decoder is granted.

The native parameter calculation uses `h=13,m=6000,n=420,N=8191`. The decoder
control uses deterministic disjoint point ranges and a predeclared random
error pattern.

## Two Budgets Instead Of One Weight Cap

For an integer signed pattern `y in {0,+1,-1}^m`, write

```
U_y(T) = product_(y_i=+1)(T+t_i),
V_y(T) = product_(y_i=-1)(T+t_i).
```

Exponentiating its syndrome gives `U_y(z_j)/V_y(z_j)`. Consider the full
box `E_(a,b)={y: number_positive<=a, number_negative<=b}`.

**Norm and decoder.** If `n>a+b`, equal syndromes of two box elements make
`U_y V_y' - U_y' V_y` vanish at all `n` points. Its degree is at most `a+b`,
so it vanishes identically. Reduced monic fractions and unique factorization
then identify the same integer signed pattern. Rational interpolation,
polynomial gcd, and root scanning recover it from the syndrome.
The implementation performs extended Euclidean reconstruction, cancels
the common factor BEFORE checking final degrees, and verifies every root
and the supplied syndrome. Exhaustive small tests include unbalanced signs.

**Readout.** A score Fourier term replaces a box element `y` by
`u=y+e_i` or `u=y-e_i`, possibly producing a coordinate of magnitude two.
The positive degree of `u` is at most `a+1` and the negative degree at most
`b+1`. Comparing it to any `y' in E_(a,b)` gives cross-product degree at
most `a+b+1`. Therefore

```
n >= a+b+2
```

excludes every extra score alias. This argument includes repeated roots
arising from a magnitude-two coordinate. It is a worst-case box argument,
not an independent-sign or average-decoding assumption.

More generally the same counting allows an observable with integer
frequency l1 norm at most `j` when `n>a+b+j`. No full score distribution
is inferred from the mean case.

At `n=420`, set `a=b=209`. The box includes patterns of weight up to 418,
not merely 209. The actual control decodes 190 positive and 190 negative
positions from its syndrome alone. A 210-positive-error control is rejected;
it is not silently folded back into the accepted source law.

## No Mersenne-Prime Infinitude Premise And Composite Module Invariants

The proof uses the finite field for rational functions, but only the cyclic
group `Z_N` for exponent labels. `N` need not be prime. Character
orthogonality on `Z_N^n` is enough for the target-state norm and readout;
no Gaussian elimination over a fictitious field `F_N` is used.

`module_and_rank_audit` in `theorems/balanced_signed_mpi.py` checks both
prime-order field rank and composite-order $\mathbb{Z}_N$ Smith-normal-form
invariant factors:

- **Prime $N$ ($h=13, N=8191, m=6000, n=420$)**: Exact $\mathbb{F}_{8191}$
  rank of $B$ is $420$ (full column rank), and the first $420$ rows form an
  invertible $420 \times 420$ information set (`first_n_rows_invertible_over_Z_N: True`).
- **Composite $N$ ($h=4, N=15, m=8, n=4$)**: The Smith Normal Form invariant
  factors of $\begin{pmatrix} B \\ 15 I_4 \end{pmatrix}$ over $\mathbb{Z}_{15}$
  are `[1, 1, 1, 3]`. In particular, `rows 0..3` has nonzero determinant
  $\det(B_{0..3}) \equiv 6 \not\equiv 0 \pmod{15}$ with $\gcd(6, 15) = 3 > 1$,
  and **no $4 \times 4$ row subset of $B$ is invertible over $\mathbb{Z}_{15}$**
  (`invertible_n_by_n_information_set_exists: False`), even though the quantum
  state transfer and rational decoder in `small_control(4)` succeed with unit norm.

## Explicit Pilot And Exact Mean

Choose rational `0<t<1` and begin with one-coordinate amplitudes

```
sqrt(1-t) at 0, sqrt(t/2) at +1 and -1.
```

Restrict and normalize the product amplitudes to `E_(ell,ell)`.
Let `(P,Q)` count positive and negative symbols in `m` independent trials,
with probabilities `(t/2,t/2,1-t)`, and define

```
Z = Pr_m[P<=ell, Q<=ell],
R = Pr_(m-1)[P<=ell-1, Q<=ell].
```

The normalized pilot assigns amplitude proportional to
`(1-t)^((m-|y|)/2)*(t/2)^(|y|/2)` on each accepted pattern, and includes
the known center phase `exp(-2*pi*i*c.y/N)`.

After syndrome computation, reversible rational decoding erases the pattern;
the inverse Fourier transform on `Z_N^n` produces the target state.
Injectivity proves normalization. The readout guard reduces the score to
the single-coordinate transitions `0 <-> +1` and `0 <-> -1`, giving

```
mean_cosine = sqrt(2*t*(1-t)) * R/Z.
```

For the native parameters, `ell=209,t=13/200` gives:

- Mean cosine at least `0.3421279344361546`.
- Unconditioned source mass `Z` approximately `0.72788323`.
- Ideal output mean cosine at least `0.3` with probability greater than
  `0.06018`, using only the mean and the upper score bound 1.

## Matched Classical Portfolio (Schema v2)

`matched_classical_portfolio` freezes the native instance ($h=13, N=8191, m=6000, n=420$,
center seed `261006753`), crosschecks `fast_public_matvec` (`log_cauchy_product`
with zero-extension onto `evaluations` and restriction to `supports`) against
explicit matrix multiplication, and evaluates six predeclared classical methods
on the full $6{,}000$-row objective ([arXiv:2610.06753v1 Appendix D.1](https://arxiv.org/abs/2610.06753)):

| Classical Attack (`method`) | Initial $\to$ Final Mean Cosine | Candidate Shifts | Outcome & Structural Mechanism |
|---|---|---|
| `information_set_pinning_I0` | $0.074231 \to 0.074231$ | $1$ | Exact solve $B_{I_0} x \equiv c_{I_0} \pmod{8191}$; local $1.0$, outside $0.004553$ |
| `original_basis_fft_from_zero` | $-0.006702 \to 0.045787$ | $6{,}880{,}440$ | 2 sweeps ($840$ FFT scans) along raw columns of $B$ from $x=0$ |
| `original_basis_fft_from_pinned_I0` | $0.074231 \to 0.074231$ | $3{,}440{,}220$ | 1 sweep ($420$ FFT scans) from $x_{\text{info},0}$; 0 moves (raw columns break all 420 pins) |
| `systematic_basis_fft_I0` | $0.074231 \to 0.116649$ | $6{,}880{,}440$ | 2 sweeps ($840$ FFT scans) along $G_0 = B B_{I_0}^{-1} \pmod N$; escapes raw-column trap |
| `systematic_basis_fft_I1` | $0.067164 \to 0.114933$ | $6{,}880{,}440$ | Disjoint information set $I_1 = 420..839$ + 2 systematic FFT sweeps |
| `row_subset_lll_babai_rounding` | $0.074231 \to 0.074101$ ($0.116535$ polished) | $6{,}880{,}440$ | $40 \times 40$ LLL + Babai rounding (local 40-row cosine $0.999672$, global $0.074101$) |

All returned assignments are scored across all $6{,}000$ rows and replayed through
`fast_public_matvec`. The best classical portfolio mean cosine is `0.116649`
(`systematic_basis_fft_I0`), below the target threshold `0.30` and the ideal
balanced-box quantum mean lower bound `0.342128`. This does not prove classical
hardness or establish a quantum speedup.

```
python theorems/balanced_signed_mpi.py
python -m pytest -q tests/test_balanced_signed_mpi.py -W error::RuntimeWarning
```
