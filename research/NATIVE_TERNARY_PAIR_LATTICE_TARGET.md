# Exact A2 Deep-Hole Target For Native Pairs

LOCAL GEOMETRY DERIVATION / REVIEW PENDING. This target is NOW IMPLEMENTED in
`theorems/ternary_pair_lattice.py`; see `TERNARY_PAIR_LATTICE.md`. It is not an
exact closest-vector solver, polynomial coverage theorem, or novelty claim.

## Why This Representation

For n1 the stripped pair problem has Q=3^(r-1), M=r-2 and independent paired
labels(a_i,c_i). A ternary word contributes either0,a_i,c_i. Encoding this as
two unrestricted Boolean choices is WRONG: selecting both changes the source.
An ordinary Euclidean barycenter also biases the zero choice. The exact A2
metric makes all three allowed choices equidistant and certifies validity.

Put z_i=(u_i,v_i) in Z^2 with allowed values(0,0),(1,0),(0,1). Let the row
A=(a_1,c_1,...,a_M,c_M), target t, and lattice/coset

```text
Lambda={l in Z^(2M): A.l=0 modQ}; z0+Lambda={z:A.z=t modQ}.
G=diag([[2,1],[1,2]],...); center=(1/3,...,1/3).
```

An equivalent integer Euclidean embedding is

```text
E(a,b)=(a+b,-a,-b), applied blockwise.
||E(3u-1,3v-1)||^2
 = 18*(u^2+u*v+v^2-u-v)+6.
```

The integer expression in parentheses is nonnegative: after centering it is
a positive quadratic form minus1/3, so an integer value cannot be negative.
Equality occurs EXACTLY for the three allowed points. The next possible value
is at least one. Thus for ANY integer modular witness vector z,

```text
||E(3z-1)||^2 >= 6M;
equality iff z is a valid original ternary word;
an invalid word has squared distance >= 6M+18.
```

This is an EXACT norm certificate, not a floating Babai score or Gaussian
heuristic. It does not assert that a closest vector is easy to find.

## Explicit Scalar Congruence Basis

If some A_p is a unit modQ, put

```text
z0_p=t*A_p^(-1) modQ; z0_j=0 for j!=p;
B_p=Q*e_p;
B_j=e_j-(A_j*A_p^(-1) modQ)*e_p for j!=p.
```

Rows B generate the FULL integer kernel and detB has absolute value Q.
Any kernel vector is reduced using its nonpivot coordinates; the remaining
pivot multiple is divisible by Q. The resulting embedded CVP problem has

```text
row lattice basis L_j=3*E(B_j), rank2M inside R^(3M);
target T=E(1,...,1)-3*E(z0);
distance ||3*E(l)-T||^2 = ||E(3*(z0+l)-1)||^2.
```

With no unit, abort and charge the failure in an initial average-case baseline
or implement a complete exact congruence/SNF treatment. Unit absence has
probability3^(-2M) for scalar IID labels; it is not a pointwise guarantee.
Do not extend this scalar basis to vector targets without a new construction.

IMPLEMENTATION UPDATE: the complete scalar treatment needs only the common
gcd g=gcd(Q,A), not SNF. Reject targets not divisible by g as provably empty;
otherwise divide A,Q,t by g and use the unit basis in modulus Q/g. All-zero
labels reduce to modulus1. The implementation no longer discards nonunit labels.

## Next Implementation / Falsification

- Implement exact basis, coset, inverse-word extraction, Gram/norm checks and
  full bounded witness bijection tests before interpreting LLL output.
- Try capped FLINT LLL plus exact nearest-plane, multiple public randomized
  bases/centers, and strictly verified two DISTINCT outputs. Same canonical
  closest vector twice does not satisfy the quantum interface.
- Require the original norm6M AND exact original modular congruence, not a
  plausible Euclidean residual. Decode both one-hot bits at every register.
- Benchmark IID stripped labels with independent UNIFORM targets, including
  empty/singleton targets, all timeouts, failures and all lattice work. Use
  the exponential MITM only where its full preflight budget is affordable.
- Count one-witness and two-witness coverage separately. A variable-time solver
  must satisfy the source runtime cap/occupancy-weighting contract.
- LLL/Babai is neither a CVP certificate nor a polynomial coverage theorem.
  Exact shell geometry alone proves no quantum algorithm or classical hardness.
- Treat favorable r<=8 cases as controls. Seek stable polynomial resource and
  inverse-polynomial pair-coverage bounds before claiming a breakthrough route.

Any such arithmetic solver reads ONLY the stripped labels and target; it has
no phase state or target high trits. If its real two-witness coverage and costs
meet the contract, the already implemented receiver converts that into a
source-valid quantum least-trit learner without recursive native-product loss.
The solver guarantee, classical dequantization comparison, native reduction,
hardware errors and full-secret amplification still need proof.
