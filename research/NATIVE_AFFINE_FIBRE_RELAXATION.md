# Native Affine-Fibre Relaxation And Its Endpoint

Local constructive derivation / external review pending. This supplies exact
public coordinate parametrizations and bounded replay, not a physical gate
compiler or a general lower bound on quantum fibre preparation.

## A Real Uniform Relaxation Recipe

For cohort b, assemble the n-by-2M matrix A_b from the actual original label
pairs a,c. Suppose it has full row rank modulo3. RREF over F3 selects an
invertible pivot minor S. Its inverse is lifted to q=3^r by

```
X <- X*(2I-SX) mod 3^(min(2t,r)), starting from S^(-1) mod3.
```

Both inverse identities are checked at every lift. No matrix inverse that
assumes a prime is used at a composite root. A rank-deficient matrix returns
UNSUPPORTED, not a false assertion that its native fibres are empty.

The map z <-> (A_b*z,z_free) is an exact bijection over Z_q^(2M). For target
sigma, uniform free coordinates therefore parameterize ALL q^(2M-n)
solutions of A_b*z=sigma, at polynomial public arithmetic cost. A reversible
implementation can initialize the target and uniform free registers then
apply this invertible affine coordinate map. The repository supplies that
coordinate recipe, not a physical modular-QFT/adder compiler. Its arithmetic,
original label access, precision and all outcome branches must be charged.

## Filtering Into The Actual Native Words

A valid word has one coefficient pair from

```
(1,0), (-1,1), (0,-1)
```

at every site. This membership predicate is exact and reversible in
principle. Each accepted coefficient vector names exactly one native word.
Uniform cohort plus uniform unrestricted fibre, followed by membership
filtering, has target acceptance

```
p_sigma = eta_sigma / [B*q^(2M-n)].
```

eta_sigma counts actual words ACROSS all B cohorts. Conditional on acceptance,
all valid cohort/word preimages have equal amplitude: this is a legitimate
normalized-fibre reference, but its acceptance is not free. No failure branch
may be thrown away in the runtime ledger. On accepted branches, compute the
word, then uncompute z from its known coefficient pairs; retaining and then
discarding an unresolved pointer is not that coherent cleanup. A physical
implementation of this cleanup remains a compiler obligation.

Deterministically eta_sigma<=B*3^M, so

```
p_sigma <= min(1,3^M/q^(2M-n)).
```

For ANY fixed full-rank label family, the uniform-target mean is exactly
(3/q^2)^M; it does not need random labels or balanced fibres. This mean does
not prove that prescribed coordinate targets have typical counts. The
per-target bound is separate and holds for every target of this relaxation.
Ordinary amplitude amplification obeys p_after<=(2j+1)^2*p_sigma, so half
success requires (2j+1)^2>=1/(2*p_upper). This is necessary, not sufficient,
and is not a lower bound on other circuits or preparations.

At q=3^n,M=n^2+24, the per-target bound is 3^(-E),
E=n*(2M-n)-M=Theta(n^3). The simple uniform unrestricted relaxation is
therefore worse than the earlier comparison route. Scaling ledgers retain
exponents rather than expanding million-digit denominators.

## The F3 Counterexample To An Overbroad Cut

At q=3, the selector pairs ARE the affine line

```
beta_t = (1,0) + t*(-2,1) mod3, t in F3.
sigma(word) = sum_j a_j + sum_j t_j*(a_j+c_j).
```

If the n-by-M slope matrix is full rank, direct F3 elimination parameterizes
native word fibres without the unrestricted 2M-variable membership filter.
The module implements this known linear endpoint and a label-only polynomial
short-word helper. Applied to actual original responses, the preceding
classical reduction recovers the ideal endpoint secret. This is an explicit
classical countercontrol, NOT a new quantum algorithm or growing-root helper.

For higher roots, extrapolating the third selector produces defect(3,-3),
and slope cyclic closure produces(-6,3), modulo q. Neither vanishes at
q=9 or beyond. Thus promoting F3 elimination to Z_(3^r) ignores actual
carries. Some individual labels may cancel an extrapolation defect; that
alone does not prove F3 cyclic closure or an arbitrary-pair linearization.
Carry-aware structured algorithms are still allowed and deserve investigation.

## Verification And Falsifiers

Bounded controls enumerate every public affine coordinate, every target,
and accepted native word under a preflight cap. Exact membership counts,
uniform conditional laws, missing targets and complete failure probabilities
are retained. Tests cover unit pivots not initially on the diagonal, nonunit
rank, high-root inverse lifting, actual word/coordinate cleanup and the
endpoint classical counterpart. No original values, mask, secret or errors
enter the affine relaxation or endpoint helper.

Falsifiers: composite-field inversion without its unit premise; nonfree rank
called no solutions; word membership filters treated as certain; uniform-
target averages used as selected-target guarantees; ordinary-amplification
bounds declared universal; or F3 carries discarded at higher roots.

Run `python theorems/native_affine_fibre_relaxation.py --write` and its tests.
