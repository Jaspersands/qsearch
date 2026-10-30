# Verification

2026-10-23. Final targeted suite: 24 tests passed in 8.79 seconds.
All three Python files pass py_compile. Tests cover:

- All 40 Lagrangians at ell=3 and all 156 at ell=5, with the exact split
  versus transverse corner-span classification.
- Nine full maximal quaternion-order fixtures at characteristics 7,11,19
  and kernel primes 5,17,61. Completion changes index ell^16 to one.
- Three split-kernel controls retain index 61^16 and fail fullness.
- Three mixing-involution controls complete the order; scalar maps do not.
- Actual common-scalar cancellation on auxiliary levels 3,5,7,13 in the
  arithmetic model, without supplying a kernel to that interface.
- The dimension-five source-word obstruction and rejection of rational
  nonintegral advice in the known-map control.

The replay records nine successful lattice cases, three rejected
deficient lattices and three mixing-involution checks, with source hashes.
These use REFERENCE target-order coordinates. Actual curve/product
evaluation, geometric Gram extraction and the Frobenius-conjugacy probe
remain unexecuted. No general dequantization or quantum speedup follows.

Final broader milestone: 224 tests passed across seven ISOLATED bundles:
24 classical Siegel + 22 effective output + 24 product/mixing controls +
27 prime-square flags + 56 smooth source + 47 kernel output + 24 general
smooth squares. All ten Python files in the three new bundles pass syntax
checks. No full-repository CLI/UI validation was attempted against the
moving checkout. Source/staging remain untouched; no commit or push.
