# Mixed-Input Audit Of Affine Phase Erasure

**Status: exact local derivation and independent finite controls.
Independent proof review and novelty review remain open.**

The question is whether the previous pure-coset reasoning describes an
actual channel on standard mixed HSP inputs, including all measurement
outcomes and retained classical transcripts. This audit finds no missing
postselection or hidden representative in that conversion. It also makes
the independence assumption explicit and removes a prime-congruence
restriction from the WRITTEN schedule using published classical solvers.
The implemented receiver retains its original restriction.

This is not an external computational reduction or a Shor-level claim.

## Exact Input Invariant

Let `A=Fp^m`, `D=|A|`, and let `L<=A` be an unknown linear subspace.
For any phase function `P:A->Fp`, define

```
rho(L,P) = (1/D) sum_(x,x': x-x' in L)
             omega^(P(x)-P(x')) |x><x'|.
```

This has trace one. Equivalently, it is the UNIFORM mixture of normalized
phase-decorated states on all affine `L` cosets. Choosing a uniformly
random ambient representative gives the same mixture, since every coset
has the same number of representatives. No representative is available
to the receiver.

The instrument identity below does not require `P` to be polynomial.
Bounded degree and a fixed common parameter vector are needed only to
compute cancellation weights efficiently.

## The Complete Public Instrument

Take `k` independent inputs `rho(L,P_i)`, public scalars `c_i`, at least
one nonzero, and a fresh uniform register on `A`. Subtract `c_i*x` from
source register `i`, then measure those source registers. For outcome
`y=(y_1,...,y_k)` the Kraus operator is

```
K_y = D^(-1/2) sum_(x in A)
        |x><y_1+c_1*x, ..., y_k+c_k*x|.
```

This operator uses no hidden subspace, potential, coefficient or origin.
The isometry preparation, invertible coordinate shears and ordinary
measurements give a physical construction, not a requested inverse map.

**Completeness.** In `K_y^dagger K_y`, output-basis orthogonality removes
all pairs with different `x`. For each fixed input tuple and each `x`,
there is exactly one `y`. Hence

```
sum_y K_y^dagger K_y = I.
```

This even holds for all-zero scales, although those scales do NOT preserve
the desired input invariant.

**Every branch.** Set `P_y(x)=sum_i P_i(y_i+c_i*x)`. Direct multiplication
of density entries gives

```
K_y (tensor_i rho(L,P_i)) K_y^dagger
    = D^(-k) rho(L,P_y).
```

The support condition is `c_i*(x-x') in L` for every `i`. At least one
nonzero scalar makes it equivalent to `x-x' in L`. Inactive scales
contribute only a global phase, which drops out of the density matrix.
Thus EVERY `y in A^k` has probability `D^(-k)`.

The production receiver discards zero-scale source copies. The displayed
instrument instead measures them; summing over those unused outcomes
gives exactly the production instrument on the active copies. They remain
charged to the source budget in both descriptions.

This branch law is for the independent MIXED ensemble. For fixed pure
cosets, some outcomes have zero probability; that is not a contradiction.
For pure supports of dimension `l`, an allowed active-`k` branch has
probability `p^(l-m-k*l)`. Do not replace either law with the other.

## Actual HSP Source, Not A Promised Phase Oracle

Use the explicit class-three chart and common potential derived in
`NIL3_COCYCLE_RECEIVER.md`. Write `|N|=M`, and assume the cyclic hidden
subgroup has nonzero quotient line `L`. The standard mixed coset source is

```
rho_H = (1/(D*M)) sum_(g in G, h in H) |g><g*h|.
```

Apply the positive-sign QFT to the normal coordinate and measure its
label `lambda`. Two quotient coordinates are connected exactly when
their difference lies in `L`. Summing over the `M` normal coordinates
and using the common-potential identity yields

```
<q| sigma_lambda |q'>
  = (1/(D*M)) 1[q-q' in L]
      omega^(lambda.(Q(q)-Q(q'))).

Pr(lambda) = 1/M;
sigma_lambda / Pr(lambda) = rho(L, lambda.Q).
```

The Fourier label is retained. The unknown oracle output/coset name is
discarded to obtain the standard mixture; it is not additional advice.
Fresh independent oracle preparations supply independent inputs
conditioned on the fixed hidden subgroup and the observed labels.

The new diagnostic constructs `rho_H` from actual group edges
`g -> g*h^t`, Fourier-transforms their normal-coordinate differences,
and compares ALL label blocks with this formula. It does not synthesize
the source by assuming the desired polynomial-phase state.

The theorem here is not about arbitrary hidden `H`, `H<=N`, arbitrary
correlated sources, or unknown changes of subgroup between copies.

## Adaptive Induction And Error

At a merge, the public maps and chosen weights are fixed after conditioning
on earlier classical outcomes. Fresh sources and disjoint surviving
packets are independent under that conditioning. The branch identity
therefore applies again. Every surviving packet is another
`rho(L,P_transcript)`, and its public coefficient map is obtained by the
existing translation rule.

Before final Fourier readout, the Fourier-label/shear transcript is
secret-independent in this promised source model. Transcript-dependent
weights, zero-map decisions and grouping do not change that assertion.
If complete cancellation makes `P_transcript` constant, the conditional
output is exactly `rho(L,0)` for EVERY transcript. It is decoupled from
the retained CLASSICAL transcript.

This does not prove decoupling from an arbitrary external QUANTUM
reference. Independence is a statement about the receiver's source
marginals, not permission to erase correlations in a purification.
Complete-instrument diamond-norm errors and source trace-distance errors
can be accumulated by contractivity and a hybrid argument. Renormalizing
a rare branch and dividing by its probability is neither necessary nor
justified. This audit is ideal-state algebra, not a fault-tolerance proof.

## Failure Controls

1. **All-zero scales.** The operation is still CPTP but outputs the pure
   ambient uniform state, not `rho(L,0)` for a proper subspace. Rejecting
   all-zero cancellation vectors is mathematically necessary.
2. **Dephased sources.** Each source becomes `I/D`; every conditional
   output remains `I/D`. Final Fourier samples are uniform and lose the
   line. A classical basis-sample simulator is not a dequantization.
3. **Different subspaces.** For phase-free independent inputs, the output
   is the mixture for the intersection of active subspaces. Two distinct
   lines can collapse to `I/D`. The common-hidden-subgroup promise matters.
4. **Correlated coset origins.** Sharing one randomly chosen coset between
   two inputs is not the product mixed ensemble. At `p=3,m=2`, the checked
   two-copy example has 54 impossible outcomes among 81, instead of a
   uniform law. A supplier cannot silently substitute correlated copies.
5. **External-reference claim.** Marginal correctness is not a claim that
   all purifications give a product state with their environment.
6. **Uncharged descriptions.** Knowing stabilizer or phase descriptions
   of the unknown source would change the classical input model. The
   fixture's potential and hidden line are not receiver inputs.

## All-Prime Written Schedule

The existing code uses cube inversion for `p=2 mod3` and a convenient
quadratic solver for `p=3 mod4`. Neither congruence is intrinsic to the
instrument or the class-three potential.

[Ivanyos and Santha, arXiv:1503.09016v2, Propositions 9 and 10](https://arxiv.org/pdf/1503.09016)
give randomized polynomial-time diagonal-equation solvers with
`(R+1)^2` quadratic columns and `(9R+1)(3R+1)(R+1)` cubic columns.
Their polynomial bit complexity is in `R` and `log p`, not `p`.
These are prior-art subroutines, not new algorithms from this repository.

The common-potential public rank bounds from the previous derivation are

```
R3 = n
R2 = n*(m+1)
R1 = n*binom(m+2,2).
```

They remain valid after adaptive translations: degree-`d` coefficients
factor through moments `sum_i lambda_ij*b_i^d*a_i^gamma`,
`|gamma|<=3-d`. This bounds the equation rank, regardless of the number
of original copies absorbed in a packet.

Substituting the published solvers gives a conservative schedule

```
B3 = (9*n+1)*(3*n+1)*(n+1)
B2 = (n*(m+1)+1)^2
B1 = n*binom(m+2,2)+1
S_general(m,n) = B3*B2*B1 = O(n^6*m^4).
```

Thus the WRITTEN construction extends to every prime `p>3` in the same
explicit Lie-presentation/cyclic-transverse-H promise, with polynomial
cost. For `m,n<=d`, this is `O(d^10)` copies per quotient state, NOT a gate
complexity exponent. The known final quadratic HPGP stage likewise uses
the general quadratic solver. The smaller implemented schedule remains
`O(n^4*m^4)` for its restricted primes.

The published solver is valid for arbitrary input coefficient columns;
it does not require independent random later labels. Its randomness is
classical, and a proposed solution is checked before physical use.
Expected polynomial subroutine cost plus constant-error stopping budgets
is sufficient for a bounded-error polynomial algorithm in the written
model. The local fixed-attempt simulator is not its uniform compiler.

**Not implemented:** general-prime SDE backend, arbitrary-precision
quantum arithmetic/QFT compiler, or a verified public black-box-to-Lie
conversion. No interface flags or accepted claims have been promoted.

## Prior-Art And Decision

The SDE machinery and the univariate full-graph HPGP learner are known.
The point requiring independent overlap review is the global
common-potential reduction with UNKNOWN affine support of higher
quotient dimension, including the non-split extension.

The bounded-prime nilpotent HSP theorem in
[Imran and Ivanyos](https://arxiv.org/abs/2304.08376) already covers
constant-prime examples; the finite `p=5` audit is only a consistency
check. It cannot establish novelty. Searches did not identify an exact
match for the proposed all-prime explicit-presentation statement, but
failure to find a paper is not evidence of priority.

Next scientific gate: independently verify or refute the complete
explicit-presentation theorem, then audit the published reduction's
presentation requirements. A classical oracle-query separation for
opaque coset names does not establish relevance to lattices, code
equivalence, graph isomorphism, or cryptography. Do not expand group
families or add parameter campaigns until those questions are answered.

## Reproduction

```
python -m theorems.affine_phase_channel_audit --write
python -m pytest -q tests/test_affine_phase_channel_audit.py -W error::RuntimeWarning
```

The finite control checks Kraus completeness, all 81 branches, explicit
matrix multiplication versus address selection, adaptive composition,
phase-free transcript independence, the failure controls above, and all
125 partial-QFT labels for the non-split order-3125 group. The simulation
cost is deliberately finite and is NOT charged as proposed quantum cost.
