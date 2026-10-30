# Sampling Relaxation Accepted, Order Debt Retained

Date: 2026-10-26. This supersedes the pending status in the frozen
`SAMPLING.md`. Independent review:
`../matrix-lift-access-review-2026-10-26/SAMPLER_REVIEW.md`.

Accepted: the mod-two character bound suffices for exact verified relations,
full two-primary-group generation and rational halving. Highly nonuniform
laws inside the two-primary group are allowed. Exact uniform Jacobian
sampling and its full-zeta input are unnecessary for THIS sampling role.
The true exact group order h, normalized perfect pairings, bounded exact
arithmetic and charged representations remain external premises.

Keep these qualifications with any use of the result:

- Every draw must be fresh conditional on the entire adaptive history.
  A frozen bank or success-conditioned generation samples cannot silently
  replace fresh relation-test rows. Exact verification does not repair the
  runtime of a sampler trapped in a subgroup.
- The bound4s is for OUTER proposals only. With at most st strict stages
  plus a terminal stage per saturation on t generators, the review gives
  a loose O(s^4) bound on internal sample rows during generation and O(s)
  pairings per row. Multiply by prime/class/pairing costs.
- Incorrect h can invalidate projection, the starting relation lattice
  and the completeness test; subgroup-order verification is not an
  independent certificate that a supplied Jacobian order is correct.
- Bruin's prime sampler includes its component-count rejection correction.
  Uniformly choosing an uncorrected factor of a random section is not the
  required uniform law on closed primes.

The reviewer closed the internal class-normalization gap constructively.
Let ell=2g+2, R_j=H^0(L^j) and W_D=H^0(L^2(-D)). From the sampled W_P
and the point O, repeatedly use

```text
W_(D+E) = {z in R_2 : z R_2 subset span(W_D W_E)}
```

when deg(D+E)<=ell. This supplies A=P+(ell-n)O and B=ell O. In Bruin's
medium convention c_D=[L(-D)], the desired [P-nO] is c_B-c_A, not the
opposite sign. Products through degree4 and medium subtraction through5
fit the available degree7 algebra. Repeated O or P=O causes no problem.
No canonical divisor, torsion basis, labels or half is needed to prepare
these samples. This proves a polynomial construction under the algebra
contract, not that the native backend has been implemented.

Independent controls include exact subgroup-state generation times,
adaptive relation verification, and correlated-sample failures. In C8xC4
the allowed four-point-support law is at total variation7/8 from uniform,
yet has expected generation20/3 outer proposals and minimum escape1/4.
All19 parent tests also passed independently. These remain finite controls
of the theorem, not evidence of a quantum speedup or a curve sampler.
