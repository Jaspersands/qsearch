# Sparse Inverse Trace: Complete Affine Singleton Filter

29 October 2026. Deterministic classification of one restricted family,
with replayable moment certificates and original native-word verification.
The mathematics and implementation received independent automated review
by Nash; this is not human peer review or proof-assistant verification.
Not a general sparse-target solver, native infeasibility test, hardness
claim, uniform sampler, or novelty claim.

## Contract And Implementation

`theorems/inverse_trace_sparse_polynomial.py` exports
`classify_affine_singleton(instance)` and
`verify_moment_certificate(instance, certificate)`.

The supplied instance uses the existing `inverse_trace_smt.validate_instance`
contract: `bits`, distinct encoded `points`, aligned binary `targets`,
`checks`, and the exact `field_modulus_coefficients` of the production FLINT
backend. This module additionally requires odd field degree, odd length N,
4 <= K < N, and exactly one actual target-one coordinate. It supports all
such inputs within the existing validator's bounds; primality, N=n^2 and
K=floor(N/8) are not additional requirements. Those native parameters are
included when they meet this contract. In particular, native n5 has K=3
and is outside this theorem, not an excluded affine instance.

Let a be the supplied one-point and B the supplied zero-points. The family
being classified is exactly

    x_a = 1,
    x_b = g(b) + 1/g(b),  b in B,
    deg(g) <= 1 and g(b) != 0 for every b in B.

No separate support is selected, and zero output symbols are legal. The
condition g(b)!=0 concerns the parameter, not x_b. This is a restriction
on a common polynomial in the public coordinate, not on arbitrary local
parameters. Constant polynomials are included in the exclusion theorem.

Malformed or unsupported input raises ValueError, never an exclusion
status. There is no target coercion, point resampling, field conversion,
prefix sampling, parameter search, or change to the original checks.
Reports retain a deep copy of the complete supplied instance, including
metadata and coordinate order. The input is not mutated.

The only returned statuses are:

- `VERIFIED_NATIVE_WITNESS`: the unique affine candidate has passed the
  existing `inverse_trace_smt.verify_word` on the original public input.
- `AFFINE_ANSATZ_EXCLUDED`: an exact moment certificate excludes every
  polynomial in this affine family, not every native word.

Reports carry the positive centered moments mu_1 through mu_K, the inverse
moment mu_-1, the actual one-index and point, and either the first nonzero
positive moment or the zero-inverse-moment obstruction. The certificate
verifier recomputes powers directly, separately from the classifier's
iterative accumulation. It returns False on malformed certificates and
unsupported instances. A positive moment certificate does not itself
verify a word; `verify_word` is the separate required replay. Internal
certificate or native-verifier failure raises ArithmeticError.

## Exact Affine Classification

Define mu_j=sum_(b in B)(b-a)^j, including j=-1. Distinct points make all
inverse terms legal. Odd N gives mu_0=0.

**Theorem.** In the stated contract, an affine g yields a completion if
and only if

    mu_1 = ... = mu_K = 0,    mu_-1 != 0.

The sole candidate is g(X)=mu_-1*(X-a). Coefficients in the report are
`[constant, slope]` in the original polynomial-basis field encoding.

**Proof.** The parity equations may be tested against any polynomial of
degree less than K. Test against g, square that equation, then add the
equation tested against g^3+g. At a zero-point both contributions are
g(b)^4+1 and cancel. The remaining condition is

    g(a)*(g(a)^2+g(a)+1) = 0.

These tests are legitimate because K>=4 and deg(g)<=1. Odd field degree
implies T^2+T+1 has no field root, so g(a)=0. Constants are impossible:
the zero polynomial violates parameter nonvanishing, and a nonzero
constant gives zeroth syndrome zero on the even-sized set B instead of
the required one. Thus g=c*(X-a) with c!=0.

The shifted monomials (X-a)^j form another basis of polynomials of degree
less than K, so they preserve exactly the original parity equations.
They reduce those equations to

    c*mu_(j+1) + c^-1*mu_(j-1) = delta_(j,0),  0<=j<K.

The j=1 equation and mu_0=0 force mu_2=mu_1^2=0, hence mu_1=0. Induction
through the remaining equations forces mu_3 through mu_K to vanish.
The j=0 equation then fixes c=mu_-1, which must be nonzero. Conversely
these conditions satisfy every shifted moment and hence every original
check.

The trace predicates are automatic but still replayed. For nonzero z,
x=z+z^-1 is zero exactly at z=1. Otherwise

    1/x = z/(z+1)^2 = 1/(z+1) + 1/(z+1)^2,

so its absolute trace is zero. At the actual one-point, x_a=1 has inverse
trace one because the extension degree is odd. This proves necessity and
sufficiency for the declared family, including legal zero coordinates.

The classifier uses O(NK) field operations and O(N+K) report/storage space,
plus O(N) inversions. Direct-power certificate replay uses
O(NK log(K+1)) field multiplications with ordinary powering; native
verification has its existing polynomial cost. There is no scan over q
field elements. Completeness and polynomial cost apply to this family
only, not to unrestricted search or a hard wall-clock guarantee.

## Controls And Scope Boundaries

For polynomial-basis points 0,...,N-1 with N=n^2 and singleton a=0,
odd n implies N=1 mod8. Their first centered sum is the binary XOR of
1,...,N-1, equal to the nonzero encoded element N-1. Thus every such
instance with K>=4 excludes the whole affine family. Tests cover native
n7, n11 and n17 without changing their public inputs.

There is a positive native control in the production GF(128) encoding
with modulus X^7+X+1: N=49, K=6, points {0} union {16,...,63}, and singleton
at 0. All six required positive moments vanish, mu_-1=47, and g(X)=47X
returns a native-verified word. It has 47 nonzero zero-site coordinates;
the remaining zero symbol is accepted, not discarded. Shift, nonzero
scaling, and permutation controls retain the actual supplied one-site
and original ordering. A further native control using six eight-element
cosets has all six positive moments zero but inverse moment zero, so the
second exclusion branch is independently exercised.

The positive example has a structural explanation, not just a finite
success. Its zero-points are three cosets of W={0,...,15}, a binary
four-dimensional subspace. For the additive polynomial
L(X)=prod_(w in W)(X-w), each coset has vanishing power sums through
degree14. Put u=L(16), v=L(32); the three coset values are u,v,u+v.
Then mu_-1=L'*(u^2+u*v+v^2)/(u*v*(u+v)) is nonzero, because u,v,u+v
are nonzero and T^2+T+1 has no root in an odd-degree binary field.
The reviewer independently reproduced c=47 using binary arithmetic and
exhausted all 16,256 nonconstant affine candidates, finding only 47X.
This explains this structured input; it supplies no typical-input success
claim for arbitrary supplied points.

Tests also exhaust every affine polynomial on two small GF(32) instances,
including a positive one, and check the K>=4 boundary, the necessity of
testing mu_K, input immutability, malformed contracts, certificate
tampering, and failure of the existing native verifier.

The parent's disjoint-pole/MDS boundary remains separate: at minimum
linear support the weights can still fail the trace predicates. Neither
that failure nor affine exclusion implies native infeasibility. This
module neither solves minimum predicate-constrained support nor changes
the dense-target norm route in `INVERSE_TRACE_NORM_ATTACK.md`. It does not
replace the full inverse-graph baseline in `INVERSE_TRACE_SMT_BASELINE.md`.

## General Polynomial Result: Proof Only

No degree-d solver or linear prefilter is implemented here. The following
deduction records the broader algebra without expanding the software API.

Let A be m>=1 actual one-points, all fixed to x_a=1, and let
x_b=g(b)+g(b)^-1 at the zero-points, with g nonzero there and degree d.
If 3d+2m-2<K, then P_A divides g; in particular d>=m is necessary.

To prove this, test parity against X^j*g and square, then add the test
against X^(2j)*(g^3+g), for 0<=j<m. Both degrees are below K. Cancellation
at the zero-points leaves

    sum_(a in A) a^(2j)*g(a)*(g(a)^2+g(a)+1) = 0.

The Vandermonde matrix on the distinct a^2 is invertible, and the same
odd-degree irreducibility forces g(a)=0 for every a.

For completeness, let p_j=sum_(b in B)b^j and
s_j=sum_(a in A)a^j. For d<K, multiplication of the original moment
equations by g gives the necessary binary-linear system

    sum_(k=0)^d g_k*s_(j+k) + sum_(k=0)^d g_k^2*p_(j+2k) + p_j = 0,
    0<=j<K-d.

Given g_d!=0 and zero-freeness on B, this system plus the first d original
moment equations is sufficient: discrepancies obey the recurrence with
coefficients g_k, so their initial d zeros propagate. This statement does
not solve those residual reciprocal equations or the zero-freeness test.
In the divisibility regime the s term vanishes, and square roots give
the ordinary field-linear equations

    sum_(k=0)^d g_k*sqrt(p_(j+2k)) = sqrt(p_j),   g(a)=0 for a in A.

Even-indexed rows are Hankel rows since sqrt(p_(2r+2k))=p_(r+k).
Consistency is only a necessary filter without the residual equations.
The special syndrome simplifies this restricted system; it does not
establish a complexity equivalence with arbitrary-syndrome completion
or a general native solver.

## Targeted Replay

The parent-generated [saved controls](classical_baselines/inverse_trace_sparse_polynomial.json)
retain both complete public inputs and classifier records: the native n7
positive case with c=47, and the native n17 polynomial-basis affine
exclusion. Both records, moment certificates, and the positive native word
were replayed successfully here. Their `instance_sha256` values hash the
UTF-8 encoding of sorted-key compact JSON, with no trailing newline.

From the repository root, this read-only replay also checks those digests:

```sh
python -B - <<'PY'
import hashlib
import json
from pathlib import Path
from theorems.inverse_trace_sparse_polynomial import (
    classify_affine_singleton, verify_moment_certificate,
)
from theorems.inverse_trace_smt import verify_word

report = json.loads(Path(
    "research/classical_baselines/inverse_trace_sparse_polynomial.json"
).read_text())
for saved in report["cases"]:
    instance = saved["instance"]
    canonical = json.dumps(instance, sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(canonical.encode("utf-8")).hexdigest() == saved["instance_sha256"]
    replay = classify_affine_singleton(instance)
    assert all(saved[key] == value for key, value in replay.items())
    assert verify_moment_certificate(instance, saved["certificate"])
    if saved["status"] == "VERIFIED_NATIVE_WITNESS":
        assert verify_word(instance, saved["witness"])
    print(instance["bits"], saved["status"])
PY
```

Use the existing research Python environment containing FLINT and pytest:

```text
python -B -m pytest -p no:cacheprovider -q tests/test_inverse_trace_sparse_polynomial.py
```

The dedicated suite passed all 56 tests here. The parent additionally
reported 456 passing tests in a combined nine-file suite in 29.01 seconds,
including these tests and 17 route controls. That larger run was not
re-executed here; no result from the pending independent review is assumed.

The module has no CLI, UI, registry, report-writing, or installation hook.
