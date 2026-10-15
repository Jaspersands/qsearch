# Global Affine Mod-4 Fibre Rigidity

Local derivation, external review pending. No novelty, speedup, scalar DHSP
lower bound, or general quantum lower bound is claimed.

## Research Decision

The nonlinear fibre workbench establishes near-unit mean existence of useful
coarse pairings, but its reference construction is exponential. This pass tests
one tempting efficient replacement: a single globally Boolean-affine
permutation that preserves every coarse subset sum.

That replacement is impossible whenever the low column signatures are nonzero
and pairwise distinct. This condition is overwhelmingly likely for native IID
labels when vector dimension grows and m is polynomial in that dimension.
This is NOT a barrier to partial affine proposals, outcome-adaptive measurement
trees, or efficiently computable nonlinear pairings. Do not prune those classes.

Run `python qsearch.py dcp-affine-fiber-rigidity`, then
`node research/certificates/dcp_affine_fiber_rigidity_crosscheck.js`.

## Exact Coefficient Criterion

Let A be an integer n-by-m matrix, B=A mod2, and
P(x)=Lx XOR c with x,c in F2^m and invertible L. All binary x are interpreted
as ORIGINAL Boolean assignments, not coordinates after conditioning on a
syndrome. Require A P(x)=A x mod4 for EVERY x.

Parity expansion modulo4 gives

```text
P_i(x) = c_i + (-1)^c_i [sum_j L_ij x_j
                         - 2 sum_{j<k} L_ij L_ik x_j x_k] mod4.
```

Higher-degree terms have coefficient divisible by4. Uniqueness of multilinear
coefficients on the Boolean cube over Z4 follows by triangular evaluation on
indicator vectors (no division is needed). Therefore global preservation is
equivalent to vanishing of all three lists:

```text
constant:       sum_i A_i c_i                         = 0 mod4
linear j:       sum_i (-1)^c_i A_i L_ij - A_j          = 0 mod4
quadratic j<k:  -2 sum_i (-1)^c_i A_i L_ij L_ik        = 0 mod4.
```

The validator exports the actual coefficient lists, not just a pass boolean.

## Simultaneous Form Rigidity

For each label component l, the linear equations modulo2 give BL=B, and the
quadratic equations give all off-diagonal entries of
L^T diag(B_l) L equal to zero. Its diagonal equals B_l by BL=B. Thus

```text
L^T D_l L = D_l,        D_l = diag(B_l).
```

Crucially this holds for EVERY binary linear combination D_u=sum_l u_l D_l,
not just the original coordinate forms. Invertibility gives
D_u L = L^(-T) D_u, so L preserves ker(D_u).

Write p_i=B_i in F2^n for column i. If L_ij=1 and p_i is nonzero, then for
every u with u.p_j=0 we must have u.p_i=0. Over F2 this implies
p_i=p_j: the annihilator inclusion forces p_i in span(p_j).

An explicit separating covector verifies the contrapositive. If p_i has a bit
outside p_j, use that coordinate. Otherwise p_i is a strict nonzero subset of
p_j; use one coordinate inside p_i and one in p_j outside p_i. This second
case is why pairwise INCOMPARABILITY is unnecessary. Merely distinct nonzero
signatures suffice.

With all signatures distinct and nonzero, L must be diagonal and invertible,
hence L=I. The linear equations then read -2 A_i c_i=0 mod4. Since each
A_i has an odd component, c_i=0. The only automorphism is the identity.

Full higher labels may choose L,c arbitrarily: the good-B certificate excludes
ALL such choices pointwise. For descent modulo2^h with h>=2, mod4 preservation
is a necessary condition, so the same restriction applies. One-bit descent
modulo2 is NOT covered and admits nonzero kernel translations.

## Native Probability

For IID uniform public labels in Z_(2^t)^n, columns p_i are IID uniform in F2^n.
For any fixed coordinate P[p_i=0]=2^-n; for any pair
P[p_i=p_j]=2^-n. Hence

```text
P[signature gate fails] <= min(1, (m + binom(m,2))/2^n).
```

The exact probability of passing the gate is
product_{j=0}^{m-1}(2^n-1-j)/2^(n*m) when m<=2^n-1, otherwise zero. The
implementation stores normalized exact dyadics, omitting the large exact
product beyond its explicit work cap while retaining the union bound.
At n64,m192 the failure union bound is18528/2^64 (<2^-49).

This is the probability of a SUFFICIENT certificate. Gate failure does not
imply a nontrivial affine symmetry. It is not the probability of algorithm
success, cannot be transferred to postselected low-label sources, and is not
about n=log(q) for a scalar DHSP. For n1 and m>1 the signature gate cannot pass.
Finite seeded matrices are unfiltered controls, not estimates of this theorem.

## Attempts To Falsify It

- Exhaust ALL affine bijections for six original-label controls (width<=3),
  checking the coefficients against direct evaluation on ALL original x.
- Distinct but comparable signatures (1,2,3) still force global identity.
  Nevertheless translation by111 succeeds on two of eight original inputs
  for A=((1,0,5),(0,1,1)) modulo8: a useful PARTIAL proposal of mass1/4.
  This directly refutes any attempt to extend the result to partial proposals.
- Repeated low signatures with different high labels admit a useful swap on
  half the cube for A=((1,5),(2,2)). Fixed points do not receive output credit.
- A coarse-zero column with full label4 modulo8 permits a fixed-point-free
  useful translation on EVERY input. The no-zero premise is essential.
- Repeated signatures need not yield any nontrivial symmetry: A=((1,1),(0,2))
  has only identity. Do not turn an UNKNOWN certificate into acceptance.
- Binary parity preservation alone admits translations in ker(B), even when
  signatures are nonzero and distinct. The mod4 premise is essential.
- Independent JS replay recomputes original-label global automorphisms and
  partial pair labels. It does not assume Python coefficient/pass booleans.
- Tests exhaust small matrices and affine maps, compare exact probabilities
  against complete low-label tables, and mutate certificates to test rejection.

## What Still Could Fail

The coefficient/form argument is locally derived, not externally reviewed.
Its main risk is scope misuse, not a growing-family empirical extrapolation.
Any actual counterexample consisting of good signatures plus a nonidentity
globally affine preserving map falsifies it immediately; the exact validator
and finite census make that check executable.

It may be irrelevant to the best algorithm: adaptive affine measurement trees
already induce piecewise/nonlinear maps, and partial programs can succeed.
An efficient nonlinear coarse-only receiver remains the priority. Neither
classical reconstruction, physical source supply/noise, recursive label laws,
nor final decoding is resolved here. Central registry admission remains
mechanical follow-up; this certificate is NOT a new active general no-go.
