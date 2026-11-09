# Quadratic Legendre character-only classical scope review

Date: 2026-11-05. This is a bounded audit of local primary full texts, plus an
independently checked elementary baseline. It is not an exhaustive current
literature claim, hardness evidence, a quantum decoder, or a deployment claim.

## Native contract

Public growing odd prime p, hidden monic irreducible quadratic
f(x)=x^2+b*x+c over F_p. Access is ONLY chi(f(x)) at chosen base-field inputs;
no full field-value oracle or extension-field queries. Output b,c, then compare
with independent random oracle queries. Classical and coherent access must
remain separately charged. The attack below uses ordinary classical queries.

## Proved full-data baseline

For every p>=5 and every monic quadratic over F_p, let
S_j=sum_{x in F_p} x^j*chi(f(x)) mod p, for j=0,1,2. Euler's criterion gives
chi(f(x))=f(x)^h in F_p, h=(p-1)/2, including zeros. Since
p-1+j<2(p-1), summing monomials isolates the coefficient of x^(p-1):

- S_0=-1.
- S_1=-h*b=b/2.
- S_2=-(h*c+binomial(h,2)*b^2)=c/2-3*b^2/8.

Thus b=2*S_1 and c=2*S_2+3*b^2/4. There are exactly p character queries,
O(p) field operations and O(log p) working bits with streaming access; the
input/table source is not counted as attack workspace. This is exponential
in log p. It does not bound the best algorithm with fewer queries.

The same formula deliberately FAILS at p=3: the x^2*f(x) sum also includes
the x^4 term, and returns c+1 instead of c. This is an excluded boundary,
not repaired by quietly changing the contract.

For distinct irreducible monic quadratic candidates f,g, fg is squarefree of
degree four. Weil gives |sum chi(fg)|<=3*sqrt(p), so an independent uniform
verification query agrees with probability at most 1/2+3/(2*sqrt(p)). A
fixed wrong irreducible candidate passes v independent tests with probability
at most that bound to the power v (or the trivial bound 1 when smaller p
makes the displayed bound exceed 1). Reject reducible candidates first.

## Primary-source algorithm audit

Sources are the locally saved full texts under
research/audits/sources/legendre_prf/. Page references below are printed pages.

1. Kaluđerović, Kleinjung, Kostić, *Cryptanalysis of the generalised Legendre
   pseudorandom function*, ANTS XIV (2020), DOI 10.2140/obs.2020.4.267:
   - Section 4F, p.277, specifically addresses degree two. Precompute all p
     translations of f; at least one is centered x^2-u. Test all p centered
     candidates. The paper calls this deterministic O(p). Section 4, p.272,
     first queries all p inputs and precomputes base-field character values.
     Restoring length-L fingerprints gives soft-O(p) work and storage.
   - Section 2B, p.270, equation (2-2), explicitly ASSUMES uniqueness of the
     short fingerprint at L=2*r*log p. Thus the paper's word deterministic
     must not be mistaken for a proved short-pattern uniqueness theorem.
     The moment baseline above removes this assumption for full p-query data.
   - Section 5A, pp.277-278, applies the affine subgroup to general degree r:
     M consecutive queries yield Theta(M^2/L) sequence entries and expected
     O(p^r*L/M^2) trials. For r=2, a direct trial costs L Legendre evaluations,
     giving O(p^2*L^2/M^2) search evaluations, plus table construction and
     storage. The balanced exponent is soft-O(p) time with soft-O(sqrt(p))
     queries. Section 5A3 discusses amortized extractions/trials; its detailed
     external implementation discussion concerns the linear challenge, so do
     not silently import sharper linear implementation costs into r=2.
   - Lemma 3.1, p.272, and Section 4B, pp.272-275, explicitly require r>=3.
     The proof that the stabilizer injects into the Galois group uses at least
     three roots. Substituting r=2 into those bad-key exponents is invalid.
     Section 4F says all quadratics are bad or ugly, and still enumerates p
     possibilities: symmetry is not a poly(log p) classical decoder.
   - Section 4E, p.277, recommends good irreducible polynomials and avoiding
     stabilizers. Quadratics are outside that recommendation.

2. Beullens, Beyne, Udovenko, Vitto, *Cryptanalysis of the Legendre PRF and
   Generalizations* (2020):
   - Section 4.2, pp.9-10, gives M queries, O(M^2/m) sequence extractions,
     O(p^d*m^2/M^2) Legendre evaluations, and O(M^2) memory, m=d*ceil(log p).
     For d=2 this is soft-O(p) balanced time, not poly(log p).
   - Assumption 1, p.5, assumes only O(1) keys share the short sequence.
     Runtime/collision estimates using it remain conditional.
   - Section 5.1, pp.10-11, needs f=gh over F_p. For split quadratics it gives
     O(log p) queries and O(p*log p) time/memory. It DOES NOT apply to the
     irreducible quadratic promise. Section 5.2's unique k-XOR reductions
     likewise require actual lower-degree factors over the native field.
   - The p.2 polynomial-time quantum/single-query statement concerns the
     preceding L_k(x)=chi(x+k), degree one, and cites van Dam-Hallgren.
     Section 5.2's quantum k-XOR tradeoffs are exponential-in-log-p resource
     bounds for factorable keys; they are not a quadratic decoder here.

3. Russell, Shparlinski, *Classical and quantum function reconstruction via
   character evaluation*, arXiv quant-ph/0212016 (local preprint):
   - Theorem 5, Section 3 p.7, gives deterministic O(d^2*p^(d+epsilon))
     binary operations. Its proof uses O(d*sqrt(p)*log^2(p)) oracle values.
     For d=2 this is weaker than the quadratic-specific full-data baseline.
   - Theorem 6, Section 4 p.8, gives O(d) quantum queries to prepare states
     for which a successful POVM EXISTS. It gives no efficient implementation
     of that measurement. This is a query statement, not poly(log p) time.
   - Introduction p.2 attributes efficient quantum algorithms to the LINEAR
     shifted-character case and says exact orthogonality fails nonlinear.

The degree-two reconstruction problem is a published native specialization;
these sources do not supply a concrete deployment reason for choosing it.
It is a structurally weak family relative to KKK's recommendation, but not
a rare subfamily within degree two. Irreducibility blocks factor attacks,
not the affine/quadratic baseline. No classical poly(log p) attack follows
from this audit; no classical hardness follows from its absence.

## Decisive scientific control

Run `/opt/anaconda3/envs/qsearch-cas/bin/python
research/classical_baselines/quadratic_legendre_contract.py`.
The script and sibling JSON contain every irreducible monic quadratic for
predeclared p=5,7,11,13 (164 total), plus all three p=3 boundary failures.
Only the source/harness sees the coefficients. The attack receives p and a
sign iterator, uses p queries, and returns the moment formulas' coefficients.
The harness compares the truth and every native evaluation, and charges 16
independent seeded random verification queries separately. Exact integer
counts are preserved; no fitting, quantum simulation, or timing inference.
Logical operation counts describe the written arithmetic, excluding Sage
field setup, conversions, source construction, and validation. Space is an
analytic O(log p) statement, not measured Python/Sage memory consumption.

Acceptance: all 164 p>=5 instances recover exactly and match all native
outputs; each uses exactly p attack queries; all independent verification
comparisons pass; all three p=3 cases retain the predicted c+1 failure.
These controls check the proved baseline and access boundaries only.

## Final resource and error audit

Independent follow-up accepted expected O(sqrt(p)polylog p) resources and
conservative failure-or-incorrect-output bound4/64+1/4096=257/4096. True
candidates always pass; false candidates already require bad fingerprints,
so the16 checks need no extra term in this bound. Saved false-candidate
logs and verification can be O(p) worst-case. Expected false center pairs
are at most B^2/(64p^2)=O(1/p); wrong-center acceptance additionally costs
(3/4)^16. Charge its entire O(p) width branch rather than reusing the
correct-center nonzero-offset bound. Correct-center false width pairs have
expectation at most3M^2/(64p^2)=O(1/p). N>=18 ensures M<=N; public nonsquare
rejection has exactly two expected trials. No additional run was needed.
