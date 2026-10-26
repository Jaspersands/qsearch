# Canonical-TFD Pauli Readout Is Classical For Conditional-Product Blocks

Status: written argument and executable interval controls; independent
mathematical review still required. Not a kernel-checked theorem, new quantum
algorithm, general TFD simulator, or claim of algorithmic novelty.

## Scientific Question

`RELATIVE_GIBBS_WORLDLINE.md` dequantized computational-basis Gibbs sampling,
but explicitly did not settle coherent observables on the canonical
thermofield double. Does that distinction rescue a concrete noncommuting,
code-coupled Hamiltonian family?

For the conditional-product subfamily below, no: an explicit classical
sampler plus a bounded paired estimator reproduces any specified two-sided
Pauli expectation to additive accuracy. This is a matched readout attack,
not an inference that diagonal samples contain all quantum coherence.

This uses the established sampling-based classical-simulation perspective,
not a new general simulation principle. See
[Van den Nest, 0911.1624](https://arxiv.org/abs/0911.1624) and
[Schwarz and Van den Nest, 1310.6749](https://arxiv.org/abs/1310.6749).
Their computationally tractable-state framework is relevant prior art.
Here the normalizing partition sum is not assumed computable: it cancels
from the actual estimator.

## Explicit Input And Task

Public binary columns `f_i` have width `r`. There are `r` central qubits
and `N` local qubits. All coefficients and beta are explicit rationals:

```
c_i(z) = (-1)^(f_i . z)
H = sum_i [a_i X_i + (b_i + h_i c_i(Z_R)) Z_i + e_i c_i(Z_R) I_i].
```

The `X_i` and `Z_i` terms genuinely need not commute. Conditional on the
central assignment `z`, however, different local blocks are independent.
There is NO local-spin interaction `Z_i Z_j` in this model.

Define `F_z = exp(-beta H_z/2)`, `w_z = ||F_z||_F^2`, and

```
|TFD> = vec(exp(-beta H/2)) / sqrt(Z),  Z = sum_z w_z.
```

The task is the expectation of ONE supplied Hermitian Pauli product
`P_L tensor P_R` on this canonical purification. It is not sampling the
entire output of an arbitrary quantum circuit acting on that state.
Polynomially many such expectations are handled by a union bound.

For asymptotic polynomial bit complexity, coefficient bit lengths and
`beta sum_i (|a_i|+|b_i|+|h_i|+|e_i|)` must be polynomially bounded.
The numerical implementation uses explicit finite precision and fails
closed on a nonfinite enclosure. Mere rational input does not grant
unit-cost operations on arbitrarily large exponents.

## Bounded Coherent Estimator

The local square roots are explicit 2 by 2 matrices:

```
F_i(c) = exp(-beta e_i c/2) *
 [cosh(beta R_i(c)/2) I
  - sinh(beta R_i(c)/2)/R_i(c) * (a_i X + (b_i+h_i c) Z)]
R_i(c)^2 = a_i^2 + (b_i+h_i c)^2
Z_i(c) = 2 exp(-beta e_i c) cosh(beta R_i(c)).
```

Use the continuous limit at `R_i(c)=0`. Then
`F_z = tensor_i F_i(c_i(z))` and `w_z = product_i Z_i(c_i(z))`.

If the central X masks of `P_L` and `P_R` differ, the expectation is
exactly zero: both copies of the canonical TFD have the same central
assignment. Otherwise let their common flip be `v` and `z'=z xor v`.
Write `A,B` for their local-spin Pauli products. Define

```
G(z) = phase(z) Tr[F_z^dagger A F_z' B^T].
```

For central Pauli notation `P = i^(#Y) X^x Z^t`,
`phase(z) = i^(#Y_L+#Y_R) (-1)^((t_L xor t_R).z')`.
The transpose `B^T` is essential, especially for Y operators.
The trace factorizes into `N` local contractions, so no Hilbert-space
table or partition-function oracle is required.

The unpaired importance ratio `Re G(z)/w_z` can be exponentially large.
Do NOT claim a bounded-variable concentration result for that ratio.
Instead draw `z` from `p(z)=w_z/Z` and use

```
Y(z) = 2 Re G(z)/(w_z+w_z').
```

Hermiticity gives `G(z')=conjugate(G(z))`. Pairing the two terms of the
involution `z -> z'` proves

```
E_p Y = sum_z Re G(z)/Z = <TFD|P_L tensor P_R|TFD>.
```

Cauchy-Schwarz and unitarity of the Pauli factors give
`|G(z)| <= sqrt(w_z w_z')`. Therefore
`|Y(z)| <= 2 sqrt(w_z w_z')/(w_z+w_z') <= 1`.
This also covers `v=0`; there is no special division by an orbit size.

## Actual Classical Central Sampler

Write `Z_i(c)=D_i(1+u_i c)`, where
`u_i=(Z_i(+)-Z_i(-))/(Z_i(+)+Z_i(-))` and `p_i=|u_i|`.
Independently pin equation `f_i.z = int(u_i<0)` with probability `p_i`.
If the selected columns are independent, solve by binary elimination
and draw all free coordinates uniformly. Otherwise emit ABSTAIN.
Do not retry until success or condition away the abstentions.

For `F` the matrix of columns, define

```
A = sum_(0 != y in ker F) product_(i:y_i=1) p_i.
```

The probability of a dependent selected set is at most A, by a union
bound over supported nonzero kernel words.
The unnormalized target pin extension weights a consistent selected set
by `2^(|T|-rank F_T)`. On a dependent set this is at most one plus
the number of nonzero kernel words supported in T. Its total bad mass
is consequently at most `2A`. The target normalization is in
`[1-A,1+A]`, by expanding the product of binary factors.
On independent sets the target and proposal have the same conditional
law. Thus, including the ABSTAIN symbol, a conservative bound is

```
TV <= min(1, A + 2A/(1-A))       when A < 1.
```

No division by `1-A` is used when `A>=1`; the bound is then one.

The implementation computes outward Arb intervals for the signed biases
and rounds them to explicit signed dyadics. It samples each pin with
`coin_bits` fair bits and integer comparison. If the rounded bias is
`u_i*`, the three-outcome pin law changes by at most `|u_i-u_i*|`, even
when the sign changes. Sum these certified errors into the TV ledger.
The rest of the affine sampler is exact.

The executable certificate enumerates kernel words only under a declared
nullity cap (default 12). This cost is charged as `2^nullity`; exceeding
the cap is an error, not permission to assume a distance certificate.

For a separate, independently established distance guarantee `d`,
`A <= sum_(j=d)^N binom(N,j) p_max^j`. In the prior high-temperature
window `d>2 tau N`, `|a|,|b|,|h|,|e|<=J0` and `beta<tau/(5J0)`,

```
p_i <= tanh(beta (|e_i|+|h_i|)) < 2 tau/5
A <= (5/4) (e/5)^d.
```

The first bound uses the Lipschitz bound for `log cosh` and the reverse
triangle inequality for `R_i(+) - R_i(-)`. For the second, bound the first
binomial term by `(e N p_max/d)^d` and subsequent ratios by `<1/5`.
This is a written conditional distance argument. The current executable
does NOT accept an unchecked user-supplied `d`.

## Finite Error Ledger

Set the estimator to zero on ABSTAIN. If the implemented sampler has
TV error at most delta from p, its observable bias is at most `2 delta`,
because `Y` lies in `[-1,1]`. For m independent samples, Hoeffding gives

```
Pr[|sample mean - E_implemented Y| > t] <= 2 exp(-m t^2/2).
```

The live report stores rational interval endpoints for every accumulated
mean and an outward upper bound for
`sqrt(2 log(2/failure_probability)/m)`. Its confidence interval also
includes `2 delta`. Arithmetic uncertainty is carried by the mean
enclosure, not silently discarded.

A seeded Python PRNG enables replay but is not a certified source of
independent fair coins. The stated probability theorem explicitly assumes
fair coins. The deterministic reference below is independent of that
statistical assumption.

## Controls And Native Calibration

The tests check all 256 two-copy Pauli products on a one-central,
one-local-qubit model against the actual dense canonical TFD, plus
dependent-label multi-block controls. They cover Y transposes, unmatched
central flips, zero local fields, extreme unpaired ratios, exact small
pin laws including abstentions, and kernel enumeration.

The live calibration uses 128 local blocks and 127 central bits:
`F=[I | all-ones]`, whose kernel is the length-128 repetition code.
Coefficients are `a=1, b=1/3, h=1/2, e=1/5, beta=1/8`.
This would be a 510-qubit canonical purification. No such state is
allocated. Estimate the X product on all central bits in BOTH copies,
with identity on the local spins, using 4096 samples and seed 2026102031.

An independent O(N) even-parity contraction computes the exact reference
to interval accuracy. That easy reference is deliberately retained:
the calibration is an identity and numerical-scaling control, NOT a hard
instance or evidence for quantum advantage.

Live result: mean `0.755255556042035`, reference
`0.7558247604973607`, fair-coin 99% confidence enclosure
`[0.7043923175820747, 0.8061187945019953]`. There were zero abstentions.
Certified sampler TV is at most `2.907e-18`, dominated by pin rounding.
Tables, kernel certificate and 4096 samples took `0.91453` seconds on this
machine, excluding the independent reference and process startup.
The calibration uses its explicitly enumerated one-word kernel
certificate, NOT an assertion that beta lies in the distance-based
high-temperature window.

Verification: 30 new tests and 533 connected tests pass, RuntimeWarning
fatal. The connected suite emits 111 existing Qiskit/IBM dependency
deprecation warnings. Python/site syntax, site checks and `qsearch.py
validate` pass (`valid:true`, no issues). The full repository suite was
not run.

## Scope And Decision

When `b=e=0`, an additional elementary falsifier exists: CNOTs from the
central bits to the local spins conjugate the model to uncoupled spins.
The native calibration uses nonzero b and e, but is still not a hardness
candidate. Dependence of Pauli labels and noncommutation alone are not
enough.

Adding an actual quantum-block interaction changes the dense answer;
the tests exhibit this counterexample. General interacting TFDs,
nonstoquastic source preparation, full coherent-output sampling, and
arbitrary circuit readouts remain outside the result.

Do not grow this into a temperature or observable sweep. This resolves
one concrete loophole in the conditional-product route. A constructive
successor must identify a useful output task that escapes efficiently
contractible classical readout, and also provide a paid quantum source,
decoder, and measurement. Simply replacing a Pauli with another sparse
observable is not sufficient in light of the classical-simulation prior
art. No claim admission, CLI/UI wiring, or quantum breakthrough follows.

## Files And Reproduction

- `theorems/coherent_gibbs_readout.py`
- `tests/test_coherent_gibbs_readout.py`
- `research/classical_baselines/coherent_gibbs_readout.json`

```
python theorems/coherent_gibbs_readout.py
python -m pytest -q tests/test_coherent_gibbs_readout.py -W error::RuntimeWarning
```
