# Coupled Inverse-Trace Search: Exact SAT Falsifier

28 October 2026. Implemented classical experiment, not a polynomial-time
solver, uniform sampler, hardness claim or quantum result.

## Scientific Question And Decision

Later 28 October result: the [polynomial-norm attack](INVERSE_TRACE_NORM_ATTACK.md)
solves the SAME n17 full instance and supplies an independently AI-reviewed
expected-polynomial search argument on an explicitly certified dense-target
regime. These historical SAT timeouts remain UNKNOWN, but are no longer
the strongest classical evidence. Uniform sampling is still a separate task.

Can a classical solver exploit actual inverse products together with the
dual-Reed-Solomon checks to solve the explicit native search problem?
Earlier local linearizations were provably too weak. This implementation
enforces the products instead of treating their monomials as independent.

The first n5 control returns a verified original-instance witness. Both
n17 runs, with and without an accepted-prefix restriction, return UNKNOWN
at their stated solver limits. This does not strengthen a quantum-advantage
claim. Stop increasing SAT budgets by inertia: the next useful attack must
exploit global algebraic structure, with full native verification.

## Input And Competing Mechanisms

The public input is the polynomial basis of F_(2^n), arbitrary distinct
points alpha_i, and arbitrary bits b_i. Set N=n^2, K=floor(N/8). Find x with

    sum_i alpha_i^j*x_i = 0,  0 <= j < K,
    Tr(inv0(x_i)) = b_i,      inv0(0)=0.

The input contains neither a witness nor a hidden oracle. The seeded
campaign chooses public points before targets; all-one targets are allowed
inputs but do not represent every target distribution. JSON records retain
the complete instance, its modulus and SHA-256 digest. A different backend
modulus is rejected rather than silently reinterpreting the input.

The existing conditional quantum route is coherent codeword filtering and
decoding, not a new mechanism introduced here. Its proposed polynomial
construction still carries its source, reversible decoder, cleanup and
resource obligations; see [the filter audit](BALANCED_CODEWORD_FILTER.md).
A superpolynomial comparison would require a credible classical lower bound
or hardness assumption for THIS explicit problem. Neither is established.

The strongest existing constructive controls include subfield attacks on
their allowed degree/target regimes and accepted-flat attacks on selected
prime-degree instances. Their successful witnesses remain valid; the new
SAT failures do not supersede them. Prime degrees and one-heavy targets are
tested to avoid automatically invoking those known subfield guarantees.

## Exact Encoding And Costs

`theorems/inverse_trace_smt.py` introduces field variables x_i,y_i and uses

    (x_i=0 AND y_i=0) OR x_i*y_i=1,
    Tr(y_i)=b_i,
    Hx=0.

The disjunction is exactly the zero-extended inverse graph. It admits the
legal zero only when b_i=0. Products are carryless polynomial products
reduced modulo the recorded irreducible polynomial. They are NOT ordinary
integer products modulo 2^n; [Z3's bit-vector semantics](https://microsoft.github.io/z3guide/docs/theories/Bitvectors/)
requires this distinction. FLINT independently checks every returned word
against all original equations, including the fixed prefix.

For m active positions there are 2mn primary Boolean variables, m inverse
graph constraints, m trace constraints and Kn binary parity constraints.
The field multiplication circuit has O(n^2) Boolean size per block; the
parity encoding has O(K*m*n^2) size with schoolbook constant multiplication.
These are encoding bounds, NOT solver-time bounds or independence claims.
The solver may need exponential time. The requested timeout applies to
`check()` and is interruptible rather than a strict wall-clock bound; the
recorded check can overrun it. Setup and independent verification are
separately timed and not covered by a whole-workflow wall-clock guarantee.
No field truth table is generated.

The default `--pipeline direct` is `simplify; bit-blast; sat`.
`--pipeline qfbv` retains Z3's standard QF_BV preprocessing as a comparator.
The native constraints are identical. Both backends are checked against
exhaustive small-field truth and full native-witness verification. Reports
retain raw solver statistics and a positive `sat_search_observed` flag when
SAT decisions/conflicts are reported. Absent counters do not prove solver
hardness or a lower bound. Some Z3 counters are process-wide snapshots;
the saved CLI campaign uses a fresh process for every run.

Two modes are intentionally distinct:

- Default: fix the first m=K+ceil(4K/n) positions as residual, sample an
  accepted prefix on the rest, and solve H_U*x_U=H_T*x_T. Trace-hyperplane
  sampling followed by inv0 includes legal zeros. No successful-prefix
  resampling or planted syndrome is used.
- `--full`: solve all original positions, with no prefix and zero syndrome.
  A useful restriction is not necessarily the easiest classical search.
  At n17, restricting leaves 9 free field coordinates after parity checks;
  the full problem leaves 253. Neither number is a Boolean variable count.

The [completion transfer](INVERSE_TRACE_COMPLETION_TRANSFER.md) is a
sufficient route to a solver, not a lower-bound-preserving reduction in the
other direction. Seeded PRNG controls do not prove the independent-randomness
assumptions of that mathematical transfer theorem.

## Executed Initial Campaign

All three records use input seed1028 and solver seed0. No inputs were
discarded based on their outcomes. Times are measurements on this machine,
not scaling estimates.

| n | N,K | Active m | Requested timeout | Resource cap | Setup/check seconds | Outcome |
|---|---|---|---|---|---|---|
| 5 | 25,3 | 6 | 5 seconds | 50,000,000 | 0.054/0.027 | Verified original witness |
| 17 | 289,36 | 45 | 30 seconds | 50,000,000 | 0.429/12.389 | UNKNOWN, reason `canceled` |
| 17 | 289,36 | 289 | 30 seconds | 50,000,000 | 2.659/13.353 | UNKNOWN, resource limit |

Artifacts: `classical_baselines/inverse_trace_smt_n5.json`,
`inverse_trace_smt_n17.json`, and `inverse_trace_smt_n17_full.json`.
These initial three runs used the QF_BV pipeline. The last two retain
identical original-instance digests. UNKNOWN is not a
negative result against classical search. Residual UNSAT would concern
only that prefix, not the full problem. Even full UNSAT is reported as a
solver result, not an independently checked UNSAT proof. A deterministic
witness routine does not satisfy the uniform-sampling contract.

### Preprocessing Falsifier And Corrected Baseline

A diagnostic QF_BV full-instance replay exhausted its 50-million resource
budget with `sat mk var=1` and no SAT decisions/conflicts reported. That is
evidence of a frontend bottleneck, not a substantial search experiment.
The persisted `inverse_trace_smt_n17_full_qfbv.json` repeats this finding
with 2.551 seconds setup and 15.253 seconds check, on the same input.
The direct pipeline bypasses that preprocessing and demonstrably reaches
SAT search on both forms of the SAME n17 input. It still finds no witness.

| Direct run | Setup/check seconds | SAT decisions/conflicts | Outcome |
|---|---|---|---|
| n5 restricted | 0.052/0.024 | 240/158 | Verified original witness |
| n17 restricted | 0.726/22.988 | 5693/3618 | UNKNOWN, resource budget exhausted |
| n17 full | 4.813/32.145 | 4580/1 | UNKNOWN, timeout |

These are `inverse_trace_smt_n5_direct.json`,
`inverse_trace_smt_n17_direct.json`, and
`inverse_trace_smt_n17_full_direct.json` in `classical_baselines/`.
They retain the initial public inputs AND the same accepted prefix for the
restricted runs. Jobs overlapped on this machine; timings are not a
controlled pipeline speed comparison. The full direct run creates about
1.66 million SAT variables and 6.33 million nonbinary clauses, despite just
578 primary field variables. It remains encoding-heavy. The observed
conflicts are not an exhaustive search or an asymptotic lower bound.

Replay from the repository root:

```text
python qsearch.py inverse-trace-smt --bits 5 --timeout-ms 5000 --write --output research/classical_baselines/inverse_trace_smt_n5_direct.json
python qsearch.py inverse-trace-smt --bits 17 --write --output research/classical_baselines/inverse_trace_smt_n17_direct.json
python qsearch.py inverse-trace-smt --bits 17 --full --write --output research/classical_baselines/inverse_trace_smt_n17_full_direct.json
python qsearch.py inverse-trace-smt --bits 17 --full --pipeline qfbv --write --output research/classical_baselines/inverse_trace_smt_n17_full_qfbv.json
```

`--input PATH` accepts a public-instance JSON object with `bits`, `points`,
`targets`, `checks`, and `field_modulus_coefficients`; these fields are also
retained under `instance` in each run record. A saved record is evidence for
one run, not a replacement for replaying verification.

## Independent Review: Why Rational Interpolation Is Not Yet An Attack

A prior read-only automated reviewer examined the algebraic route, before
the SAT implementation. This is not an independent review of this code or
a human specialist review.

Write P(X)=product_i(X-alpha_i). Lagrange interpolation gives

    Hx=0 iff x_i=f(alpha_i)/P'(alpha_i), deg(f)<N-K.

For a full-support word, setting y_i=A(alpha_i)/B(alpha_i) requires
nonzero A and B at all supplied points. Once B is fixed, the trace equations
are binary linear in A. But the code constraint still requires

    A*f = P'*B mod P.

Let T_B=P'*B mod P. If deg(A)<=K, deg(A*f)<N, so A*f=T_B exactly.
One must solve the target-dependent divisibility condition A|T_B AND the
quotient degree bound. Factoring T_B or solving trace interpolation alone
does not complete this step. When deg(A)=d>K, the residual equation is
A*f=T_B+P*Q with deg(Q)<=d-K-1: product consistency is still present.

For B=1, N odd and deg(A)<K, there is an immediate obstruction:
deg(P')=N-1 but deg(A*f)<=N-2. All-one targets force full support, so legal
zeros cannot bypass this contradiction. A=1 fits all their trace equations
at odd n, yet x_i=1 fails the first parity check because N is odd.

There is also a genuine positive control. In characteristic two P'=V^2,
and x_i=1/V(alpha_i) is a codeword, since it corresponds to f=V of degree
(N-1)/2<N-K. Its trace targets are induced, not arbitrary supplied targets.
Even the scaled family y_i=c*V(alpha_i) has target rank at most n over F_2;
it cannot represent every one of the 2^N target strings. This rules out only
that shortcut, not all rational, adaptive or code-based attacks.

## Follow-On Review: Affine Artin-Schreier Identities Collapse

A second independent read-only automated reviewer looked for a constructive
attack using the full instance's extra freedom. No general solver emerged.
The parent checked the following narrower pole-cancellation argument; it is
not a formal compiler proof, novelty claim or obstruction to nonlinear
parametrizations.

For any number of parameters t, assign varying coordinates

    x_i(t) = 1/(L_i(t)^2 + L_i(t) + b_i),

with nonconstant affine F_q-linear L_i. Other positions may have fixed
accepted constants c_i. Regular evaluations satisfy the trace targets at
odd n. Suppose Hx(t)=0 is a RATIONAL-FUNCTION IDENTITY, not merely an equation
one hopes to solve at a chosen t. Then replacing each varying position by
b_i, and retaining every fixed c_i, gives an already explicit native witness.

Proof: for b_i=1, D_i=L_i^2+L_i+1 is irreducible over F_q[t]. Extend L_i to
an affine coordinate change and use irreducibility of T^2+T+1 at odd n.
For b_i=0 the denominator splits as L_i(L_i+1), so it cannot share a
one-target factor. Two one-target denominators are associates only when
equal: comparison of quadratic and linear terms forces the scaling to be
one, after which L_j=L_i or L_i+1. Clear denominators, retaining each distinct
irreducible factor once, and reduce each syndrome numerator modulo D_i.
It follows that the sum of H columns in every equal-denominator one-target
group is zero. Each group's binary indicator is therefore a codeword.

Over a generic formal direction toward infinity all varying reciprocals
vanish, so the vector of fixed constants, extended by zeros, also has zero
syndrome. Add the indicator codewords just obtained. The result has x_i=b_i
on varying positions and x_i=c_i elsewhere. Both its syndrome and predicates
are correct, since inv0(0)=0 and Tr(1)=1 at odd n. A generic formal direction
is sufficient; no finite rational point or denominator nonvanishing is
being granted for free.

If every coordinate varies, the necessary condition is Hb=0. For all-one
targets the zeroth check is N mod2=1, so such an identity cannot exist.
More quantitatively, that zeroth syndrome has a NONZERO numerator of total
degree at most 2N-2. Fresh uniform parameters therefore succeed with
probability at most min(1,(2N-2)/q) by the polynomial root bound. The resulting
Omega(2^n/n^2) independent-rejection cost concerns ONLY this affine-AS
sampling strategy. It says nothing about choosing parameters with a solver,
adaptive nonlinear forms, general classical search or full native hardness.

The affine condition is essential. With Q=t^2+t+1, the three functions

    1/Q, t^2/Q, (t+1)^2/Q

sum to zero and each has inverse trace one at every t not in {0,1}. Their
AS parameters are t, 1/t and 1/(t+1), hence not all affine. This is a scope
counterexample, NOT a native solution to all K parity checks. Exact controls
retain this escape instead of suggesting all rational constructions fail.

## Falsifiers And Next Decision

- Any incorrect finite-field encoding or returned invalid native word
  falsifies the experiment. Exhaustive small-field crosschecks use FLINT,
  not the SMT circuit as their reference.
- Zero omission, replacing the public points, target induction from a
  planted word, or suppressing a solver limit invalidates the comparison.
- A scalable classical construction on arbitrary prime-degree inputs
  would falsify the proposed search advantage. A successful finite solver
  run would refute hardness for that instance, not prove dequantization.
- Full-instance attacks deserve comparison before interpreting restricted
  search behavior. No extra SAT sweep is warranted without a new algebraic
  representation, elimination strategy or target-specific construction.

The broader polynomial-system mechanism and classical specialization
comparators are prior art; see [Briaud et al., Sections 3 and 5](https://arxiv.org/html/2509.07276v1).
Their random low-degree predicates are not this fixed inverse-trace family.
Their conjectured hardness cannot be imported here.
