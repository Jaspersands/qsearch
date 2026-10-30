# Balanced Partial-Norm Completion: Exact Filter

2026-10-29. An exact computational countercertificate for one restricted
completion family, not native infeasibility, classical hardness, a general
solver, a uniform sampler, or a universal collapse theorem. No novelty is
claimed. Arithmetic replay uses two different implementations; that is not
independent human review or proof-assistant verification.

## Fixed Native Input

Keep the [native Mersenne relation](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md):

```
q=2^n, N=n^2, K=floor(N/8), s=floor((n-3)/4), r=n-4s,
d=2^s-1, sigma(z)=z^(2^s), inv0(0)=0,
sum_i alpha_i^j*x_i=0 for 0<=j<K,
Tr(inv0(x_i)^d)=b_i for every i.
```

The principal certificate uses exactly n=17, s=3, r=5, N=289, K=36,
modulus Z^17+Z^3+1 (encoded 0x20009), the polynomial-basis points
0,...,288, and 289 target bits equal to one. Its full instance is retained
in the JSON, not replaced by a seed or a regenerated favorable input.

The bounded implementation accepts canonical n=17 or n=19 instances with
arbitrary supplied distinct points and aligned target bits. It uses the
existing strict native schema and backend-modulus validation, then builds
its arithmetic context from the exact supplied modulus. Unsupported field
degrees and malformed inputs raise ValueError, not an exclusion verdict.
The mathematical description is broader than these reference limits.

## Precisely Restricted Construction

Put

```
A(T)=product_i(T-alpha_i), h_i=A'(alpha_i),
D=floor((N-K-1)/4),
Psi(z)=z*sigma(z)*sigma^2(z)*sigma^3(z), Phi(z)=Psi(z)^(2^r).
```

Choose polynomials P_0,...,P_3, EACH of degree at most D, satisfying

```
P_j(alpha_i)=sigma^j(P_0(alpha_i)) for all i and j=1,2,3.
x_i=product_(j=0)^3 P_j(alpha_i)/h_i.
```

This uses the original points and parity matrix. The product polynomial
has degree at most 4D<=N-K-1. Lagrange interpolation therefore gives
sum_i alpha_i^j*x_i=0 for every j<K: the coefficient of T^(N-1) in the
interpolation of T^j*product P_j is zero.

It is a genuine restriction of the given quartic reparameterization.
Choose kappa_i with Phi(kappa_i)=1/h_i and put
t_i=kappa_i*P_0(alpha_i)^(2^(n-r)). Multiplicativity and Frobenius
commutation give Phi(t_i)=x_i. Phi is a permutation, so these public
scalings exist and are computable by O(n) field operations each. The
trace conditions remain Tr(t_i^(2^r-1))=b_i. Nothing changes the exponent
or grants a solver for these residual conditions.

The equal individual degree bounds are essential. Unequal degree
allocations, other coordinate multipliers, target-adaptive families,
unrestricted quartic equations and native witnesses outside this family
are NOT excluded.

## Linear Conjugacy Certificate

Write P_0(T)=sum_(k=0)^D c_k*T^k. Because all points are distinct, the
conjugate values have a degree-at-most-D interpolant exactly when the
coefficients of degrees D+1,...,N-1 in P_0(T)^(2^(a*s)) mod A vanish.
Applying inverse Frobenius to each scalar equation gives an F_q-linear
system in c_1,...,c_D with entries

```
M[(a,ell),k] = sigma^(-a)([T^ell](T^(k*2^(a*s)) mod A)),
1<=a<=3, D+1<=ell<N, 1<=k<=D.
```

The constant coefficient contributes nothing to these rows. This is
pointwise Frobenius including the variable powers, NOT coefficientwise
conjugation of P while fixing the evaluation points.

At the principal fixture D=63. The ranks after adding conjugates 1, 2
and 3 are respectively 56, 63 and 63. The following square minor, with
columns 1,...,63 in order, has nonzero determinant 44208 (0xacb0):

```
a=1: ell=64,...,94 and 96,104,...,288
a=2: ell=64,65,66,67,128,192,256
```

Thus every c_k with k>0 vanishes. All four polynomials must be constant,
and the entire restricted output family is x_i=lambda/h_i. Since Psi
is a permutation, lambda ranges over F_q; there is no missing nonzero
scalar branch. Lambda=0 gives the zero word and fails all-one targets.

## Odd Trace-Dependency Certificate

For lambda!=0 the original predicate is

```
f_s(lambda/h_i)=Tr(lambda^(-7)*h_i^7).
```

Let I={0,1,3,5,6,7,8,9,12,14,18}. The values h_i^7 in this order are

```
73587,19714,22427,29421,23183,82085,
36680,121879,23810,88157,15149.
```

Their binary XOR is zero. The sum of the corresponding eleven predicate
bits must therefore be zero for EVERY nonzero lambda. The prescribed
eleven ones sum to one. This excludes the entire balanced-factor family,
not merely a tested list of scalars. The native fiber itself remains
nonempty by the existing native fiber-count bound.

For arbitrary supplied targets, the same test seeks a dependency of
h_i^d whose target-bit XOR is one. Its cardinality need not be odd when
the targets are not all one. A dependency for the constant family alone
does not justify exclusion unless the full-rank conjugacy minor is also
available.

## Implementation And Replay

[mersenne_partial_norm_filter.py](../theorems/mersenne_partial_norm_filter.py)
exports analyze_balanced_factors(instance), verify_exclusion_certificate,
build_report, and verify_report. It preserves the input by deep copy and
binds the certificate to its full canonical JSON SHA-256, including the
actual modulus, point order, targets, s and K.

The producer computes polynomial remainders, row rank, pivot-row selection,
the determinant, and the trace dependency using explicit polynomial-basis
FLINT arithmetic and binary elimination. Neither the row certificate nor
the dependency is hardcoded as the computed verdict.

The exclusion verifier uses separate integer bit-polynomial field and
polynomial arithmetic. It recomputes A, every selected remainder row, the
minor determinant, and h_i^d. For h_i it uses direct products over all
other original points, unlike the producer's derivative evaluation. It
checks nonzero determinant, distinct valid row labels, every stored value,
the actual target XOR, and the full instance binding. It does not call
the producer or trust its ranks. Modular repeated squaring avoids a loop
of exponential length in the exponent 2^(a*s). No full-field table or
enumeration is used.

Statuses are deliberately narrow:

- BALANCED_FAMILY_EXCLUDED: BOTH certificates independently replayed.
- NONCONSTANT_FAMILY_REMAINS: rank is below D; no exclusion certificate.
- NO_TRACE_OBSTRUCTION: only constants remain, but this filter found no
  contradictory trace dependency. No witness or sampling claim is made.

A failed independent replay raises ArithmeticError. Malformed certificates
return False. The CLI returns nonzero when saved-report replay fails.
Report replay also recomputes the complete diagnostic, including any
non-exclusion control, so altered ranks or status fields are not trusted.

From the repository root, without bytecode or pytest-cache writes:

```sh
python -B -m theorems.mersenne_partial_norm_filter --write --include-n19
python -B -m theorems.mersenne_partial_norm_filter --verify
python -B -m pytest tests/test_mersenne_partial_norm_filter.py -q -p no:cacheprovider -W error
```

Without --write, generation prints JSON only. The sole CLI write target
is [the owned report](classical_baselines/mersenne_partial_norm_filter.json).
There is no native search, parameter enumeration or alternate solver.

## Costs And Control Boundary

For this diagnostic, polynomial construction, remainders, Frobenius maps
and elimination cost O(N^3+n*N^2) field operations with O(N^2) field
storage. The independent verifier has the same conservative polynomial
bound. Schoolbook field operations give O(n^8) bit work and O(n^5) bits
of storage when N=n^2. These are asymptotic arithmetic bounds, not a hard
wall-clock guarantee. Trace-dependency elimination and O(N*n) public
scaling operations fit within these bounds. Native verification of any
separately supplied word costs O(N*K+N*n) field operations, but the filter
does not construct a word.

The optional original n19 all-one fixture has s=4, r=3, N=361, K=45,
D=78 and its recorded modulus 0x80027. Its successive ranks are
64,75,77, leaving coefficient dimension TWO. Its constant subfamily has
a trace obstruction, but that cannot exclude the surviving nonconstant
space. The report correctly returns NONCONSTANT_FAMILY_REMAINS. There
is no claim that all prime degrees, or even all supplied n17 point sets,
collapse to constants.

Focused tests cover exact certificate values, independent replay with the
producer disabled, reordered valid rows, certificate tampering, native
input preservation, point permutations and translations, zero targets,
the n19 non-collapse control, and direct original-word parity/predicate
checks for three scalar controls. They also replay the saved report and
check CLI success and failure paths.

## Executed Verification

The commands above were executed with /opt/anaconda3/bin/python, with
bytecode and pytest-cache writes disabled. The focused test file returned
46 passed in 11.72s. CLI generation with --write --include-n19 exited 0
and wrote two results with exactly one balanced-family exclusion. A
separate --verify invocation exited 0 and returned:

```json
{"verified": true, "result_count": 2, "exclusion_count": 1}
```

These are the executed tests and reference fixtures, not whole-repository
test results or a general search/sampling experiment. Only the module,
its focused test file, this note and the associated JSON report were
created for this work. No installation or Git operation was performed.
