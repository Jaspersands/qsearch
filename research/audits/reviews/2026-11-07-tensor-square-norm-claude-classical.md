# Returned classical report: bounded disposition

2026-11-07. Reviewed STATE.md, TENSOR_SQUARE_RATIONAL_NORMS.md and
`../claude_runs/2026-11-07-tensor-square-norm-classical-opus/response.md`.
No new research pass, implementation, source fetch, HNP theorem verification,
Git/network/API action or parameter sweep. Interpreter:
`/opt/anaconda3/bin/python`.

## R1: accepted with explicit representation and sign repairs

For n=[L:Q] and c in Q*, N(c)=c^n. Hence membership of a in N(L*) depends
only on its class in Q*/Q*^n. The map on representatives descends through
L*/(L*^n Q*). This is a valid algebraic simplification, not a procedure
that finds enough representatives of the norm image.

On the finite rational support S, the quotient is

    (Z/n)^|S| x (Z/2 if n is even, trivial if n is odd).

For an optional modular implementation using the KNOWN prime-valuation
coordinates, find z for x0=product_i epsilon_i^z_i such that every

    d_p = v_p N(x0)-v_p(a)

is divisible by n. If n is even, also require sign N(x0)=sign(a), and
take c=product_p p^(d_p/n)>0. If n is odd, give that same positive power
product the sign sign(N(x0)/a). Then N(x0)/a=c^n and

    x=x0/c

has EXACT norm a. The correction must be included in the output. Its
exponents are signed binary integers, so c and x remain polynomial-size
compact power products; their expanded rational/field coordinates need
not be polynomial size. Reducing the target first instead is also valid,
provided its known rational nth-power factor is restored to the witness.

Composite n requires module/congruence arithmetic, not Gaussian elimination
over a presumed field. Integer HNF/SNF on the congruences with nI columns
and the separate even-n sign row pays this exactly.

Do NOT identify arbitrary gcd-free coordinates reduced modulo n with the
full quotient Q*/Q*^n. For example, the single gcd-free base4 has exponent1
for the rational square4; reducing that exponent mod2 falsely calls its
class nontrivial. Use the known prime coordinates on S, or first replace
each gcd-free base by its maximal perfect-power root, scaling coordinates
by its extracted exponent. Exact integer root tests pay that normalization
without factoring. The existing exact gcd-free HNF solver has no such issue.

Disposition: R1 is ACCEPTED in this repaired form. It does not require any
change to the existing solver, which is already polynomial, preserves all
norm coordinates and signs, and directly produces an exact-norm witness.
The report's instruction that the draft SHOULD replace Z-HNF is rejected
as unnecessary. A representative list must still generate the required
norm-image quotient before it can justify NO; R1 supplies no cheap source
or completeness certificate for such a list.

## R2: accepted narrow observation, no new defect in the draft

Paired tensor norms have rational norm exactly+1, so by themselves they
provide no new norm value or nontrivial norm-image class modulo Q*^n.
They move support of an EXISTING solution in the proof. The draft already
uses them that way and obtains its norm-image generators independently
from complete S-units. The report's phrase about a nontrivial class in
Q*/N(L*) should not be used literally: every field norm is already trivial
in that latter quotient. This observation does not falsify the composition.

## Smooth-relation proposal: certified YES search, no proved clock

After the R1 repairs, any collected relation combination producing the
target norm class yields a compact witness, and the existing classical
gcd-free verifier certifies it exactly. That positive stopping rule does
NOT need a preceding HNP-based YES decision: the witness proves itself.

The proposal does not specify or prove a distribution of sampled small
elements/ideals whose smooth norms generate the required image. The
support theorem guarantees suitable S-units exist; multiplying by rational
denominators can make a representative integral without changing its
norm class. It does not put those representatives in the proposed sampled
small boxes or prove a positive probability of obtaining a spanning set.
Consequently neither almost-sure termination nor finite expected runtime
has been established for the sampler as written. A target outside the
currently collected span is not a certified NO.

REJECT the report's unqualified "Las Vegas" and subexponential-algorithm
labels. Retain only a heuristic relation-generation proposal with certified
positive outputs and unproved coverage/runtime. Even the displayed Dickman
model does not automatically supply the stated subexponential estimate:
at fixed n, norms of scale D^(1/2) and B=(log D)^C give heuristically

    u ~ log D/(2C log log D),
    rho(u)^(-1) = D^(1/(2C)+o(1)).

That is exponential in the logarithmic discriminant input size. This is
a conditional estimate inside the report's random-integer smoothness model,
not a proved sampling bound or a lower bound on norm algorithms. A larger
factor base changes the tradeoff and must be charged explicitly.

## HNP and final disposition

The parent separately audits the HNP primary sources. No qualitative HNP
theorem is promoted here to a polynomial algorithm: the local filtration,
precision and whole-runtime obligations in the report are expressly
unfinished. A valid S_n Frobenius certificate once witnesses are found
also does not establish the claimed polynomial search clock; a generic
closure-based Chebotarev bound can charge factorial degree/discriminant,
and the specified long-prime-cycle interval may be empty at small n.
Do not import that search-runtime assertion through this review.

Existing HNF solver: NO CHANGE REQUIRED. Accept R1 as an optional exact
quotient formulation, retain R2 as a scope clarification, and classify the
smooth search as heuristic/unbounded pending its missing source theorem.
No implementation or new control is requested. No classical polynomial
counterpart, proven subexponential construction, novelty, separation or
security conclusion follows from this returned report.
