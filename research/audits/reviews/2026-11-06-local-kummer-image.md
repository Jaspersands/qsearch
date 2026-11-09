# Large-prime local Kummer image: review dispositions

Native contract: monic separable f in Z[X], degree d=2g+1>=3, p>d,
growing genus, arbitrary bad reduction; complete delta(J(Q_p)) basis in a
returned fixed local coordinate frame. Classical polynomial BIT target.
No full global Selmer, small/wild/dyadic, novelty or quantum claim.

## Independent core review

The growing-degree reviewer checked tame extension coverage, all square/
constant degeneracies in the character-functional lemma, norm pullback,
disc count and termination against actual Stoll text. Parent rechecked.

- ACCEPT: all degree<=g extensions are covered by unramified/Eisenstein
  binomial presentations; only factoring e<=g is needed for unit classes.
- ACCEPT: any base functional pulls back to a degree<=d character product.
  The nondegenerate count is at least
  (q-(4d-3)sqrt(q)-4d)/4, hence q/8 for q>=256d^2. Dependent cases are
  constant on valid points or a single character count. No 2^d-pattern
  enumeration or p-adic probability-mass promise is used.
- REPAIRED: count open root neighborhoods, including fractional-distance
  children that contain no root in the CLOSED disc. At most d nodes per
  depth; D+1 tail termination is justified by Krasner/Stoll6.3(2).
- ACCEPT: actual Stoll4.4 gives target rank r-1 at odd p; every retained
  vector is an actual point/divisor image, including the modified unit at
  Weierstrass roots. A full-rank result certifies completeness.

## Independent source and arithmetic review

The source reviewer read Stoll4.4,6.1,6.3 and norm diagram, the full supplied
OM source, and the actual integral-basis source. Parent read the relevant
statements/proofs. The original OM excerpt alone did NOT pay BIT costs.

- REPAIRED: explicit section8 uses p-integral bases at the GIVEN p on each
  global-Q irreducible factor. The full integral-basis §3 Prop4, Thms4--5,
  Cor3, then §5 Props8--10 and Thm7 proof supply the local construction,
  output format and cost. MaxMin uses its OM-tree-induced order. Working
  sigma=Delta+2 preserves the source's strict inequality. No integer
  discriminant factorization is assumed.
- ACCEPT: Frobenius nilradical, field decomposition and idempotent lifting
  in O/p^P. Uniformizers arise from N_i outside N_i^2, or p if unramified.
- REPAIRED: component integral bases are explicit independent columns of
  idempotent multiplication, with a unit pivot minor. Nakayama gives a
  free basis; coordinate extraction loses no p-adic precision.
- ACCEPT: generic/Weierstrass norm valuations are <V, determinant/Cramer
  losses <=dV, and P=16d^2g^2(Delta+2)+16 exceeds them. Added conservative
  W=2S+2e_K Delta+2 absorbs factor-approximation index loss.
- ACCEPT: explicit unramified/Eisenstein tower arithmetic at precision W
  compiles the relative degree-d factorization into polynomial BIT work.
  No flattened degree-dg large-characteristic theorem is invoked.
- Simplification verified: E_i/K are used only in the character PROOF.
  Runtime exceptional children are roots of the primitive reduction, and
  actual norm vectors are evaluated in the base coordinate frame.

## Claude coordinate audit and exact dispositions

Run: audits/claude_runs/2026-11-06-local-coordinates-opus/.
Opus5.5/high, completed end_turn, 10345 input/12621 output tokens,
estimated USD0.2938. Exact original packet/report retained.

1. **d=1,p=2 counterexample:** correct for the isolated broader lemma in
   its packet, outside the actual native d=2g+1>=3,p>d contract. REJECTED
   as a task counterexample; ACCEPTED packet-scope repair. Section8 now
   repeats d>=3 and odd p. No dyadic theorem is claimed.
2. **Component basis omitted:** ACCEPTED and independently repaired as
   above. The report also offers a valid full-matrix twisted-determinant
   alternative; unused, since the component-basis route is now explicit.
3. **No decomposition stopping test:** ACCEPTED. Use the dimension of
   Frobenius-fixed vectors in the reduced algebra to certify its number
   of field components, refine until that number, and cap failures.
4. **Uniformizer-dependent coordinates:** ACCEPTED clarification. Fix and
   return the coordinate frame once per run. Canonical coordinates are
   unnecessary; no cross-run equality without frame conversion is claimed.
5. **Local source only introductory in packet:** ACCEPTED packet omission.
   Parent and independent source reviewer subsequently checked the FULL
   §3/§5 proof chain above. Supplement saved as
   claude_inputs/2026-11-06-local-coordinates/integral_basis_proof_followup.md;
   it was NOT in the original call. No silent reviewer acceptance of it.
6. **Precision and Cramer logic:** ACCEPTED under the native bound V,
   established separately by the core derivation. No new lower-level
   primitive or hidden field-order factorization is required.

Three other calls ended max_tokens with empty reports: small-cyclotomic-
fable (64000 output, USD3.30837 estimated), general-constant-map-opus
(64000, USD1.382444), local-kummer-fable (32768, USD1.78261). They supply
NO scientific findings; no retry. Combined four-call estimate USD6.767224,
not an invoice or an exact update to the owner's balance.

## Exact falsifier control

audits/controls/local_kummer_span/exact_control.py and .json:

- Native split d5 generic disc at p10007: 5001 valid residues, rank4,
  16 realized sign patterns, minimum nonzero functional count2475>=p/8.
  The claimed bound for every pattern is deliberately false and rejected.
  Norm-square dependence and constant/square degeneracies are retained.
- Native d5,p7 bad reduction: (X^2-7)(X-1)(X-2)(X-3) has a fractional-root
  exceptional child 7Z_7 containing no root; primitive reduction constant
  and odd Gauss valuation give no points there. The closed-child-root
  misstatement is falsified.
- Exact Q_7(sqrt7) normalization of a^9(3+a): valuation9, determinant
  valuation9, Cramer recovers3+a with nonsquare residual unit3. Treating
  that determinant as a modular unit fails.

This control is not the full local-image algorithm, a growing-parameter
experiment, a quantum execution or evidence for an asymptotic theorem.

Final integrated actual-text review ACCEPTED the full written classical
composition after the above repairs. An additional clock specification
uses verified 2B-cost Las Vegas attempts and logarithmically many restarts,
not a B/eta timeout. Parent checked its probability argument and integrated
it. No remaining mathematical blocker was identified under the native
promises and checked source contracts; no finite-test inference was used.

Milestone verification passed: STATE/handoff full title and current Now/row,
five primary PDF hashes, all four saved request/context hashes and terminal
usage/report states, exact-control scope guards, and scoped git diff --check.
No broad repository suite or full algorithm execution was claimed.
