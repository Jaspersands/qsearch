# Public Odd-Prime Clifford Realization

2026-10-21. Constructive implementation of a KNOWN modular Clifford
dependency, with independent exact-tableau and dense finite controls.
Not a new quantum algorithm, circuit search, fault-tolerant backend or
Lean-certified compiler. Its purpose is to remove the unspecified
alignment realization in CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md.

## Interface And Conventions

Input: an odd prime p and a public S in Sp(2R,F_p), with displacement
coordinates ordered `(x_1,...,x_R,z_1,...,z_R)` and pairing
`Omega(v,v')=z.x'-x.z'`. No subgroup, hidden potential, coefficient
assignment or quantum source is an input. The source convention is

```
D(x,z)|t> = omega^(x.z/2+z.t)|t+x>,    omega=exp(2*pi*i/p).
```

`theorems/prime_clifford_realization.py` exports `compile_symplectic`,
`compile_alignment` and `symplectic_action`. The first returns a
`PrimeCliffordPlan`; the second first verifies the existing jet-alignment
certificate. Gates are in chronological application order. Their product
C_S satisfies, in the exact arithmetic-qudit gate model,

```
C_S D(v) C_S^dagger = D(Sv)                 for EVERY v.
```

There is no v-dependent phase or Pauli displacement. A global phase of
C_S is immaterial. Known Clifford decomposition and modular arithmetic
are prior art; see [Hostens--Dehaene--De Moor](https://arxiv.org/abs/quant-ph/0408190),
especially Sections III-IV and the odd-dimensional conventions. The local
proof below fixes OUR symmetric-Weyl convention rather than silently
importing a phase convention from a qubit or composite-dimension library.

## Primitive Covariance

All arithmetic in exponents and basis addresses is modulo p; 1/2 is the
inverse of 2 in F_p, not a floating-point division.

| Primitive | Action on computational basis | Action on displacement |
|---|---|---|
| `fourier(i,epsilon)` | `p^-1/2 sum_u omega^(epsilon*u*t_i) |u>` at i; epsilon=+1 or -1 | `(x_i,z_i) -> (-epsilon*z_i,epsilon*x_i)` |
| `scale(i,a)` | `t_i -> a*t_i`, a nonzero | `x_i -> a*x_i`, `z_i -> a^-1*z_i` |
| `add(i,j,a)` | `t_j -> t_j+a*t_i` | `x_j -> x_j+a*x_i`, `z_i -> z_i-a*z_j` |
| `swap(i,j)` | Exchange t_i,t_j | Exchange both corresponding X and Z slots |
| `phase(i,b)` | Multiply by `omega^(b*t_i^2/2)` | `z_i -> z_i+b*x_i` |
| `cz(i,j,b)` | Multiply by `omega^(b*t_i*t_j)` | `z_i -> z_i+b*x_j`, `z_j -> z_j+b*x_i` |

Each row has exact, not merely projective, Weyl covariance. For a linear
basis permutation L_A, the inverse address is A^-1*t, giving
`D(x,z) -> D(Ax,A^-T*z)` and preserving x.z. For a symmetric quadratic
phase Q_B(t)=t^T B t/2,

```
Q_B(t+x)-Q_B(t) = x^T B t + x^T B x/2,
```

which changes z to z+Bx with precisely the symmetric-Weyl half-phase.
This covers both diagonal phase and controlled phase. Finally,
`F_epsilon X(x) F_epsilon^dagger=Z(epsilon*x)` and
`F_epsilon Z(z) F_epsilon^dagger=X(-epsilon*z)`; reordering X and Z
converts the original +x.z/2 into -x.z/2, exactly the output half-phase.
These identities prove covariance for all products of the primitives.

The common gate `omega^(b*t_i*(t_i-1)/2)` has the SAME symplectic action
as `phase(i,b)` but contributes `omega^(-b*x_i/2)` in the conjugation.
It is NOT a drop-in replacement. Likewise a Pauli displacement after
C_S preserves its symplectic tableau but adds a v-dependent character.
The scalar compiler currently assumes these characters are absent.

## Elimination Proof And Bound

Reduce S to identity by LEFT multiplication with primitive symplectic
matrices E_1,...,E_m. At stage j, all earlier X/Z column pairs are fixed.
Symplecticity forces the current pair's earlier coordinate rows to vanish,
so operations confined to sites j,...,R-1 preserve previous work.

1. The current X column is nonzero. If its X part is zero, Fourier a
   nonzero Z site. Swap a nonzero X pivot to j and scale it to one.
2. Controlled additions clear its other X entries. Controlled quadratic
   phases clear its other Z entries, and a single quadratic phase clears
   Z_j. The column is now e_j.
3. Pairing with e_j forces the partner Z column to have Z_j=1. Additions
   from other sites into j clear its remaining Z entries while fixing e_j.
4. Upper symmetric shears `x -> x+Bz` clear its other X entries, then X_j.
   On the affected one/two sites such a shear is `F^-1 L_(-B) F`, where
   L is the lower quadratic-phase shear. It needs three or five primitive
   gates and fixes e_j. The partner is now e_(R+j).

This proves the loop can always proceed, without an invertible A-block
promise, random restarts, a scan over field elements or state enumeration.
At the end `E_m ... E_1 S=I`. Therefore the output chronological list is
the REVERSED reduction list with every gate inverted; its product is S.
The implementation checks the reduced columns, final identity and exact
replay of the returned primitive list.

Stage j uses at most `8*(R-j-1)+7` primitives, hence

```
number of primitives <= 4*R^2+3*R.
```

Each primitive updates at most two length-2R rows. Elimination and replay
use O(R^3) field operations and O(R^2) field-element storage; the initial
symplectic check is also polynomial. All field values are arbitrary-size
integers. Bit complexity is polynomial in R and log p. The gate bound
counts modular qudit primitives, NOT native qubit gates or hardware depth.

An eventual qubit backend must implement modular permutations, quadratic
phase evaluation and approximate cyclic F_p transforms in polynomial
time in log p and log(1/delta). Across L primitives and bounded receiver
calls, allocate errors to the COMPLETE channel, including measurement
labels and ABORT. No exact arbitrary rotation is assumed free. No such
fault-tolerant gate synthesis or precision scheduler is implemented here.

## Consequence For The Source

The existing public alignment produces S satisfying its K/J identities.
The compiler now gives an explicit arithmetic gate list implementing the
required covariance. Consequently, for the tensor gauge

```
W_Y(q)=omega^psi(q) D(v(q)),
C_S W_Y(q) C_S^dagger = omega^psi(q) D(S*v(q)),
```

with NO new q-dependent phase. The existing symbolic expression
`P(q,t)=-psi(q)-A(q).B(q)/2-B(q).t` therefore needs no extra compiler
phase coefficients. Global circuit phases cancel, even when S depends on
the recorded branch. Only the public C_S gates are applied; the unknown
W_Y, T and potential coefficients are proof witnesses, never evaluated.

This is a written constructive discharge of the Clifford-existence and
phase convention dependency at the arithmetic gate level, not a proof
that the whole receiver executes. Carrier layout/padding, shared hidden
parameter provenance, diagonal solvers and adaptive costs still need
their own interfaces. The plan and its universal synthesis proof have
not been translated into Lean. The existing formal alignment theorem
still records exact gauge covariance as a premise.

## Falsifiers And Replay

`tests/test_prime_clifford_realization.py` checks every displacement for
each primitive, every one-qudit symplectic matrix at p=3,5, and independent
two-qudit Darboux frames. Dense gate matrices are constructed separately
from the tableau updates. It rejects the right-tableau/wrong-phase gate.
Actual variable-radical alignments at p=7 and a 127-bit prime compile
without enumerating their eight-qudit carriers; a 16-qudit transvection
also passes exact replay and the gate bound. Invalid fields, tableaux
and primitive descriptions are rejected. Small dense cases are controls
for the universal argument, not complexity evidence or algorithm candidates.

```text
python -m pytest -q tests/test_prime_clifford_realization.py
```
