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

