# Plane Adapter Accepted Under The Reviewed Module Contract

Date: 2026-10-26. This supersedes pending-review status in `PLANE.md`.
Independent review: `../matrix-lift-access-review-2026-10-26/PLANE_REVIEW.md`.
The compact module's separate positive verdict and qualifications are in
`../compressed-graded-algebra-2026-10-26/REVIEW_RESOLUTION.md`.

Accepted: bounded product/colon preparation of exact one-point pole spaces;
the coprime-pole proof of birationality, including inseparable field degrees;
integrality and coefficient bounds; the unique weighted relation; and
descent of its monic coefficients to the original field. The total plane
degree is in fact exactly2g+2, not just at most this number.

The two reviewed results compose as follows:

```text
promised native complete AG matrix -> true quadrics, H and rational O
  -> certified compact all-degree section ring with explicit original rows
  -> original-field plane equation of degree2g+2
  -> known Lauder-Wan exact Jacobian order at fixed characteristic.
```

Thus the fixed-p EXACT-ORDER ACCESS objection is resolved at the theorem
level under this source-matched construction. It should not remain listed
as an unexplained group-order oracle. Implementation and actual measured
cost remain entirely separate. If module setup is randomized expected-
polynomial, so is the composed route; a deterministic point counter does
not derandomize setup. The result is polynomial in p, not uniformly in
log(p), and p100003 may be impractical for a direct counter implementation.

The growing-degree interface is essential: function preparation uses R_4,
but relation recovery needs true R_(4g+4). The all-degree module certificate
provides polynomial storage and arithmetic there. For the genus41 input,
the final theoretical section matrix has14,072 rows and3,571 columns.
No such matrix was built, and no native zeta polynomial or h was computed.

The independent reviewer checked a genuinely inseparable example on
v^3-v=t^5 over F3, genus4, x=t^3 and y=v^2. The unique relation is
Y^9+Y^6+Y^3-X^10, with F_Y=0 and verified rational inverse. Parent replay
is now durable in `inseparable_control()`. Do not reject a valid relation
merely because its derivative in Y vanishes. The existing small odd-prime
tests where p divides2g+1 were NOT themselves inseparable examples.

Parent also added extra-denominator-zero tests: h=t^(g+1) in the supplied
genus1,2 controls. Their colons must force cancellation away from O, not
silently assume h has no other zeros. These still use H=ell O controls,
not the actual arbitrary native divisor class; the reviewed general proof
covers arbitrary recovered H.

No full-support solve, short effective divisor, native group order or
quantum speedup follows from these control results. Canonical/differential
conversion and final evaluation frames remain obligations downstream.
Gemini's bounded implementation sequence is still the compact-algebra
handoff, followed by the plane adapter with exact kernel, substitution,
monic-leading-coefficient and base-field checks.
