# Source-Adaptive Missing-Sign Query Bound

Status: DERIVED / REVIEW-PENDING, with exact finite arithmetic and physical
channel controls. No independent proof review, formal verification, novelty,
new algorithm, classical sampler, or general circuit lower bound is claimed.

This extends the [selector-only query bound](MISSING_HARMONIC_DETECTOR.md)
to full central irrep source information. It does not silently remove that
earlier theorem's independent-ancilla premise; it uses a different conditional
argument and explicitly charges the source information already available.

## Model And Conclusion

G=S_n, D=n!, and C is a class of M odd-transposition involutions. There are K
standard mixed coset registers with one common h. First obtain the full
central irrep labels lambda_1,...,lambda_K. These labels may control arbitrary
ancillary preparation, coherent subset selection, ancillary quantum memory,
and deferred classical feed-forward. The only subsequent carrier interactions
are q controlled phases on subset SIGN projectors. Final output includes
source labels and ancillas, but no further carrier measurement. Every query
and postselection probability is charged; no postselection is free.

Then the proposed derivation, now implemented and checked, gives

    T(output_null, output_h)
      <= min(1, K/(2 sqrt(M)) + 2q sqrt(K p(n)/D)),                 (1)

where p(n) counts ALL S_n irreps, not source categories retained by a chosen
coarsening. This holds for every h in C and consequently its class mixture.
It is negligible for polynomial K,q in the fixed-point-free family
n=2 mod 4. It need not be negligible for a small conjugacy class or
exponentially many copies. Arbitrary noncentral carrier operations, phases
on other target sectors, correlated non-coset input promises, and implemented
terminal carrier POVMs are not covered.

The known missing-harmonic construction motivating this restricted interface
is [Moore/Russell](https://arxiv.org/abs/quant-ph/0504067). The hybrid method
is standard; see [Bennett et al.](https://arxiv.org/abs/quant-ph/9701001).
The following scoped application is written out to make its assumptions
auditable, not to establish novelty by an incomplete literature search.

The [Moore/Russell/Sniady measured-sieve model, Section 3](https://arxiv.org/html/quant-ph/0612089v3)
allows intermediate isotypic measurements on adaptively combined states and
uses the resulting transcript. That is not this sign-phase-only interface.
Conversely, coherent overlapping phase queries are not automatically a
measured binary-tree sieve. Neither result may be transferred between these
models merely because both mention missing harmonics. Nonmissing intermediate
operations need their own analysis, and a measured-sieve replacement must
first confront that published limitation. No novelty inference follows from
our different exponent or access restrictions.

## Conditional Rank Lemma

For a fixed tuple of sources and nonempty subset S, put

    V_S = tensor_(i in S) V_lambda_i,
    r_S(lambda) = mult_sign(V_S) / product_(i in S) d_i.

This is the probability of the sign projector on the conditional NULL input.
In the regular representation the unused row factors are maximally mixed;
they multiply numerator and denominator equally. They are not postselected
or replaced by a pure carrier. Right group actions and the selected projectors
act only on column factors.

Fix j in S. Frobenius reciprocity identifies mult_sign(V_lambda_j tensor W)
with the multiplicity of sign tensor V_lambda_j^* in W. That irreducible has
dimension d_j, so its multiplicity is at most dim(W)/d_j. Hence

    r_S(lambda) <= 1/d_j^2,
    max_(S nonempty) r_S(lambda) <= max_i 1/d_i^2 <= sum_i 1/d_i^2.  (2)

This includes singleton subsets and one-dimensional irreps. There is no
assumption that all tensor products are multiplicity-free, no large-dimension
cutoff, and no omission of rare small-dimensional sources.

The null source law is Plancherel, p_lambda=d_lambda^2/D, so

    E_p[1/d_lambda^2] = p(n)/D,
    E_(p^K) max_S r_S <= K p(n)/D.                              (3)

This charges an arbitrarily expensive best-subset choice for FREE and still
bounds it. Implementing such optimization is not required by the proof.
No union bound over 2^K subsets, unknown character-ratio constant, or typical
diagram asymptotic is needed. Full sources dominate any fixed coarsening for
this architecture: standard inputs are already block diagonal and all allowed
carrier operations preserve those blocks.

## The Two Different Source Priors

For a hidden h in C the source law is

    q_lambda = d_lambda(d_lambda + chi_lambda(h))/D.

It is the SAME for every h in the class. Copies have product source laws p^K
or q^K even though the same hidden h is used throughout. Conditional carrier
states can still depend on h; they are not averaged independently per copy.
Character-column orthogonality gives

    E_p[(chi_lambda(h)/d_lambda)^2] = 1/M,
    TV(p,q) <= 1/(2 sqrt(M)),
    TV(p^K,q^K) <= K/(2 sqrt(M)).                               (4)

These are normalized probability laws, including zero-probability alternative
branches. Dropping those branches from the NULL distribution would falsely
remove a real signal. Source labels are not independent of the conditional
carrier state and must not be treated as an independent reference register.

## Source-Conditioned Query Hybrid

In the identity-query version of the null program, conditional on lambda,
data remains maximally mixed on its full source block and ancillas evolve
according to lambda. Before query j, a coherent weighted mixture of subset
choices has marked weight at most max_S r_S(lambda). A controlled phase has
amplitude change bounded by twice the square root of its marked probability.

One can purify the classical source distribution with an inaccessible copy
of the label, purify each maximally mixed source block, and telescope query
differences using identity prefixes and actual suffixes. Equation (3) bounds
each squared difference by 4 K p(n)/D, including arbitrary ancillary memory.
The null program's output distance from its identity-query version is thus
at most 2q sqrt(K p(n)/D).

For the alternative, every sign projector annihilates the conditional state
on every nonzero source branch. The phase queries act as identity, including
after source-conditioned ancillary operations. However, its identity-query
program has source law q^K, not p^K. The same source-to-ancilla channel applied
to these two distributions has output distance at most (4). Triangle
inequality proves (1). No step treats actual successive queries as independent.

The source term cannot be deleted at q=0. The S3, K2 physical control has
output distance 11/36 with zero queries, exactly its weak-source TV. A claimed
query-only bound of zero is therefore explicitly falsified.

The exact certificate stores the separate squared terms A=K^2/(4M) and
B=4q^2 min(1,K p(n)/D), capped where appropriate, then uses
(sqrt(A)+sqrt(B))^2<=2(A+B). At q=0 it keeps A alone. This conservative
rational bound is converted to an OUTWARD rounded dyadic distance bound;
large integers use hexadecimal certificates, not floating-point underflow.

## Verification And Scaling

Persistent exact censuses cover 1,502 conditional source/subset ranks:

| n | K | Checks | E_null max_S r_S |
|---|---|---|---|
| 3 | 3 | 189 | 119/216 |
| 4 | 2 | 75 | 23/192 |
| 4 | 3 | 875 | 2819/13824 |
| 6 | 2 | 363 | 719/172800 |

Independent regular-representation controls compare 102 conditioned projector
ranks, plus 39 per-hidden one-copy source probabilities and all null source
probabilities. Physical Young-representation controls include all 61 source
tuples across S3 K2/q0, S3 K3/q2, and S4 K2/q1, and every hidden transposition.
They prepare the best subset for each source tuple before the first controlled
pi phase, then mix coherent subset/control registers with source-dependent
complex unitaries. They verify both normalized conditional laws, annihilation,
the hybrid norm budget, and the final SOURCE-PLUS-ANCILLA output distance.
Regular rows are included in the independent rank/prior comparison, not
silently dropped from the null weighting.

Classical postprocessing of the SAME weak-label transcript is reported as a
baseline. It includes a quantum weak-label front end and is NOT end-to-end
classical dequantization. The finite ancilla trace distance is an optimal
UNCOMPILED readout diagnostic, not a supplied scalable decision circuit.
For S4 K2 one selected adaptive phase improves output trace distance by 1/144
over weak labels. This finite signal does not survive the growing-n bound.

For fixed-point-free h with K=q=n^2, the exact outward distance caps are:

| n | Certified T cap |
|---|---|
| 18 | 2^-4 |
| 34 | 2^-21 |
| 66 | 2^-64 |
| 130 | 2^-168 |
| 258 | 2^-408 |
| 514 | 2^-954 |
| 1026 | 2^-2176 |

These are theorem-bound evaluations, not large quantum simulations. n6 and
n10 are vacuous. Finite checks do not prove the all-n derivation.

## Failure Modes And Remaining Work

- The sign must really be missing: an odd transposition count. Fixed-point-free
  S4 is excluded; S4 transpositions are the physical calibration used here.
- Noncentral source/carrier measurements destroy the conditional-null model;
  extra phases on other target irreps need a new analysis.
- A final arbitrary carrier POVM can already exploit the information in the
  input states. Its compiler cannot be supplied free or ruled out by (1).
- Postselection must retain branch mass. Conditioning on a rare small irrep
  does not preserve the average bound without paying its success probability.
- This proof is ideal. If both output laws are within trace distance epsilon
  of an ideal allowed program, add 2epsilon to (1). Synthesis accuracy must
  be charged uniformly; an apparent signal from off-model operations is not
  evidence for the stated mechanism.
- The proposed uniform inequality still needs independent mathematical and
  prior-art review. No registry status substitutes for that review.

Implementation: `theorems/coset_missing_sign_source_adaptation.py`, integrated
into the existing `coset-missing-harmonic` CLI and experiment report, with
scope-gated proof/dequantization/mutation records. Further work should test
specific, costed NONMISSING-sector or noncentral carrier operations, or actual
terminal data compilers, rather than keep optimizing source-conditioned
missing-sign schedules that satisfy these premises.
