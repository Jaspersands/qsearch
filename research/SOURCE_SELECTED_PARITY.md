# Source-Selected Parity

Status: **exact finite-degree certificate, independent finite cross-checks,
review pending; no novelty or scalable advantage established**.

The fixed-parity argument in [Coherent Terminal Readouts](COHERENT_TERMINAL_READOUTS.md)
does not cover positions selected from the observed source labels. This pass
tests that exception by implementing an actual rule, not an ideal Bayes table:

    B(lambda) = {i : chi_lambda_i(h) < 0},
    z_i = y_i xor 1[chi_lambda_i(h)<0],
    accept iff sum_(i in B(lambda)) z_i is odd.

An empty selection rejects. The hidden element h is NOT supplied to the
classifier: its cycle type is the promised fixed-point-free involution class,
so these character values are computable from each measured irrep label.
The existing two-quotient arithmetic computes this in polynomial bit time;
the bit operations cost O(k). The quantum source-label and subset-phase
front end is still required and retains its previous resource accounting.

## Result

For S6 and this corrected negative-character rule, **every k>=2 loses to
even one disjoint-pair measurement**, including if the final answer is
complemented. This is an exact finite-degree, unbounded-copy statement.
It is NOT a growing-degree obstruction or a theorem about all source-aware
classifiers. Selecting positive or zero characters and omitting correction
are separate controls, not covered by this all-copy certificate.

| Copies k | Declared Signed Gap | Pair-Event Count Baseline Gap |
| --- | ---: | ---: |
| 2 | -0.015625 | 0.176528 |
| 8 | -0.033844 | 0.266943 |
| 32 | -0.001436 | 0.523943 |
| 128 | -1.220725e-9 | 0.846834 |

The gap means P(accept|hidden class)-P(accept|null); equal-prior success is
(1+gap)/2. Negative gaps are not silently reversed. Even their absolute
values lose. The right column thresholds each known pair likelihood and
then uses the exact binomial event-count law. It is weaker than keeping
every pair likelihood, and it is NOT an end-to-end classical HSP solver.
The all-copy proof only needs the still weaker baseline that uses one pair
and discards all remaining inputs, with gap 1271/7200.

## Exact Character Contraction

Let G=S_n, D=|G|, phi_lambda=-1 when chi_lambda(h)<0 and +1 otherwise.
The central phase has real group-algebra coefficients

    a_g = (1/D) sum_lambda d_lambda phi_lambda chi_lambda(g).

For null inputs put v_lambda,0(g)=chi_lambda(g). For an alternative with
one shared h put v_lambda,h(g)=chi_lambda(g)+chi_lambda(hg). The naturally
source-weighted local factor for observed bit b and group pair (u,v) is

    L_(lambda,b,h)(u,v) = d_lambda/(4D) * [
        v_lambda,h(e) + v_lambda,h(u^-1 v)
        + (-1)^b (v_lambda,h(u^-1)+v_lambda,h(v)) ].

This follows by summing the four local selector-mask choices before the
Walsh measurement. The complete probability for a source/bit string is
sum_(u,v) conjugate(a_u) a_v product_i L_(lambda_i,b_i,h)(u,v).
The factors already contain the source mass. There is no division by a
zero-probability alternative source and no conditional renormalization.

For any fixed source-local predicate p(lambda) and declared correction
c(lambda), define integer-character sums

    R_h(g) = sum_(lambda:p(lambda)=0) d_lambda v_lambda,h(g),
    P_h(g) = sum_(lambda:p(lambda)=1) (-1)^c(lambda)
                 d_lambda v_lambda,h(g).
    C_h(u,v) = [R_h(e)+R_h(u^-1 v)+P_h(u^-1)+P_h(v)]/(2D).

Summing the selected parity's sign over each local source/bit factor gives
C_h. Because the copies share h but are independent conditional on it,

    mu_h(k) = E_h (-1)^(selected parity)
            = sum_(u,v) conjugate(a_u) a_v C_h(u,v)^k.

Sum over source labels BEFORE taking the power, but do NOT average different
h values before the power. That would change the input to independently
hidden subgroups on different copies. A regression test explicitly shows
that wrong operation changes the answer.

Simultaneous conjugation of (u,v,h) leaves every character and coefficient
unchanged. Therefore the complete contraction is constant on the hidden
conjugacy class; one representative suffices after this argument. The
verifier also checks the ENTIRE exact moment spectrum on all three hidden
members of S3, all three of S4, and all fifteen of S6.

Integer coefficients A_g=D*a_g and moments N_h=2D*C_h give

    mu_h(k) = [sum_N W_h(N) N^k] / [D^2 (2D)^k],
    W_h(N) = sum_(u,v : N_h(u,v)=N) A_u A_v.

The implementation groups equal integer moments before taking arbitrary-
precision powers. It never constructs the exponentially large output law
or a tensor-product state at S6. All probability and domination decisions
use exact rational arithmetic; floats are only display values.

The W values CAN BE NEGATIVE. These are not latent-variable probabilities,
a legal classical sampler, or a dequantization of the measurement. Enumeration
still costs |G|^2 group pairs and all irrep characters, which is factorial
in n. The implemented evaluator deliberately declares its S3/S4/S6 domain.
Fast dependence on k is not efficient dependence on n.

## Certificate for Every Copy Count

For corrected negative-character selection at S6, grouping the exact
moments yields the following radii and absolute coefficient masses:

    r0 = max |C_0| = 139/180,     L0 = sum |W_0|/D^2 = 62864/405,
    r1 = max |C_h| = 13/15,       L1 = sum |W_h|/D^2 = 48668/675.

Triangle inequality bounds the absolute acceptance gap by

    |gap(k)| <= (L0*r0^k + L1*r1^k)/2.

At k=38 this is already strictly below 1271/7200; both radii are below one,
so it decreases for every larger integer k. For k=2,...,37 the exact moment
formula verifies the same strict inequality individually. The largest
absolute prefix gap is

    391526744626649 / 10883911680000000 < 0.036,

attained at k=6. The k=1 corrected rule has gap zero. Hence no additional
copy count can repair this SPECIFIC fixed-degree rule. This certificate
does not assert that its final single bit retains all source/parity
information: an arbitrary decision based on the source labels as well as
that bit is a different readout.

## Verification and Prior Art

The moment evaluator uses integer Murnaghan-Nakayama characters. Its 96
null/alternative laws for S3/S4, k=1,2,3, four selection predicates and two
correction choices agree with the independent matrix-derived histogram
evaluator. That evaluator is itself cross-checked against direct physical
subset-phase programs. Separate tests call the executable terminal rule
on every S4 k=3 source/bit histogram. Exact hidden-member spectrum checks,
the finite prefix, and the tail inequalities have dedicated regressions.

The relevant broad context includes [Hallgren, Roetteler and Sen](https://arxiv.org/abs/quant-ph/0511148),
who prove a growing number of jointly measured coset states is necessary
for the graph-isomorphism HSP setting, and [Moore, Russell and Sniady](https://arxiv.org/abs/quant-ph/0612089),
who rule out polynomial-time algorithms in their specified adaptive sieve
model. Neither abstract alone proves this particular fixed-S6 statement
or licenses a blanket no-go for all coherent subset programs. These are
scope references, not an established novelty comparison for our certificate.

## Research Decision

Do not recycle corrected negative-source parity as an untested positive
example. It really does fall outside the earlier fixed-position bound,
but that logical gap is not a performance result. Keep its exact certificate
as a falsifier and as a check on future changes to the measurement.

The next discriminating experiment is a source-corrected Hamming threshold
at S6, using label-summed generating functions and the same natural weights.
For that rule the local generating function has coefficients

    alpha_h = [1+J_h(u^-1 v)+a_h(u^-1)+a_h(v)]/4,
    beta_h  = [1+J_h(u^-1 v)-a_h(u^-1)-a_h(v)]/4,

where J_0(g)=1[g=e], J_h(g)=1[g=e or g=h], a_0(g)=a_g and
a_h(g)=a_g+a_(hg). The proposed weight law is the coefficient of z^j in
sum_(u,v) conjugate(a_u)a_v (alpha_h+z beta_h)^k. This NEXT-work formula
needs independent verification before use; it is not implemented by the
parity certificate. Compare declared thresholds against pair detectors,
not only against the weak one-label baseline, and do not fit a favorable
orientation or threshold without labeling it exploratory.

Reproduce the current work with:

```sh
python qsearch.py run EXP-COSET-BINARY-CARRIER-INSTRUMENTS
python qsearch.py dequantize
python qsearch.py proofs
python qsearch.py validate
```
