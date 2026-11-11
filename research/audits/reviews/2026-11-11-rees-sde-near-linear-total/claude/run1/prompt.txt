You are an adversarial referee. The attached file states six claims (with proofs) about the
diagonal SDE problem over F_p (find nonzero x in P0^n, P0 = kappa-th powers with 0, with
sum x_i lambda_i = 0 for given columns lambda_i in F_p^d).

Task, in this order, being concrete and brief:
1. For Claims 1, 2, 3, 4, 5, 6 separately: is the proof correct as written? Give a verdict
   CORRECT / CORRECT WITH REPAIR (state the repair) / WRONG (give the failing step and, if possible,
   an explicit small counterexample with kappa, p, d and columns). Check especially: the
   character-sum identity and the inclusion-exclusion step in Claim 1 (including the T' with
   rk T' < D restriction and the use of the densest sub-bank), the flat grouping in Claim 2, the
   case split in Claim 4 (is every bank covered? does the quotient argument need anything about
   columns of B \ D lying in U? does the induction use the hypothesis only at smaller or equal
   dimensions?), the detection procedure in Claim 4's algorithmic version, and the edge cases
   (zero columns, repeated columns, kappa = 2, -1 in P or not) everywhere.
2. Is the data line "N(3,3,13) >= 8 while N(3,2,13) = 5" consistent with Claims 1, 2 and 4? Say
   whether it contradicts anything.
3. From memory only (no browsing is available to you; say so), is any of Claims 1-4 a known
   result (e.g. on systems of diagonal or additive forms over finite fields, or Davenport-type
   constants with weights in a subgroup)? Name the result only if you are confident; otherwise say
   unknown. Do not guess citations.

Do not restate the claims. Keep the report under 1200 words.
