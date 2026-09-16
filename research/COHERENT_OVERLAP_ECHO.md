# Coherent Overlapping Nonmissing-Sector Echo

Status: IMPLEMENTED RESOURCE SCHEMA AND FINITE CONTROLS. Growing-degree
signal, useful repetition cost, natural-input reduction, independent review,
novelty and quantum speedup are NOT established.

## Constructive Target

The preceding sign-only query bounds do not cover arbitrary nonmissing-sector
operations. Instead of changing a sign-query schedule, this experiment keeps
all physical data across a sequence of different, overlapping pair operations.
No intermediate irrep label is measured or discarded. The final measurement
is specified, rather than replaced by an optimal unimplemented POVM.

Inputs are K standard mixed registers with the SAME hidden involution h:

    rho_0 = I/D, rho_h = (I+R_h)/D, D=n!.

The hidden alternative is E_h rho_h^tensor K, NOT (E_h rho_h)^tensor K.
Use the full fixed-point-free conjugacy class for the scalable proposal.
Small transposition and S5 controls are calibration, not invented new problems.

Define the known-label predicate and unitary

    phase(lambda) = -1 if chi_lambda(h)<0, otherwise +1,
    U_S = sum_lambda phase(lambda) P_lambda^S.

Zero characters MUST map to +1. The predicate depends only on the promised
conjugacy class, never the unknown h. At S6 it includes four nonmissing
negative-character irreps, unlike the sign-only interface. At S4 fixed-point-
free h, it nevertheless has commuting coefficient support. Nonmissing alone
is not enough.

On a path of K data registers let A be the product of U_(i,i+1) on odd bonds,
and B the product on even bonds. Each layer consists of disjoint gates.
Apply A, B, A^dagger, B^dagger in chronological order, controlled by one |+>
ancilla. The word is W=B^dagger A^dagger B A. The reflections are self-adjoint.
This is NOT reverse-order uncomputation, which would give identity.
Repeat this word r times on the SAME data and measure X on the ancilla:

    p_minus(rho) = (1 - Re Tr[W^r rho])/2.

The fixed decision is minus -> NULL, plus -> hidden alternative. Its equal-
prior success is (1+p_minus(null)-p_minus(alternative))/2. A reversed sign
would falsify this decision rule; absolute total variation is separately
reported as a finite diagnostic. No optimal lookup-table decoder is granted.

The chosen growing family is K=n^2, r=n. These parameters are a concrete
testable proposal, not optimized values or a theorem about useful bias.

The interferometric primitive is standard, not a discovery: compare
[Knill/Laflamme's mixed-state computation](https://arxiv.org/abs/quant-ph/9802037)
and [Swingle et al.'s echo-based correlator measurements](https://arxiv.org/abs/1602.06271).
For one round, the identity

    p_minus(rho) = Tr([A,B]^dagger [A,B] rho)/4

shows precisely why a large raw commutator norm is insufficient: the question
is the DIFFERENCE of its expectations under the two physical hypotheses.
No novelty is inferred from naming the word an echo or a correlator.

## Cost And Access

The program uses q=2r(K-1) pair phase calls, each reduced to clean GPE,
exact label phase and inverse GPE. Counts per trial:

- K coset preparations, retained until the final readout;
- 2q group QFT/inverse calls and 2q uniform preparation/inverse calls;
- 4q controlled single-register group actions/inverses;
- 2q exact character arithmetic/uncomputation calls;
- one readout qubit plus reusable GPE workspace, with no postselection.

For fixed-point-free involutions the existing exact two-quotient character
arithmetic supplies the polynomial label predicate. The finite controls use
independent character tables; table enumeration is not the proposed algorithm.
Given forward GPE operator error delta, composed channel diamond error is at
most min(2,4q delta). Actual reversible arithmetic and group-QFT gate exports
are not supplied by this pass. Preparation and natural reduction still cost
resources. A polynomial ideal query count does NOT prove a polynomial useful
repetition count when the bias is unknown or exponentially small.

Every path vertex has a distinct nonempty subset-incidence signature. Thus
the fixed palette has K effective cells, not a constant number. This avoids
the specific constant-palette compression failure, not every possible bound.
The known raw-copy bound T^2<=min(1,(2^K-1)/(4|C|)) still limits EVERY output
of this program, independent of round count. Exact outward caps are recorded
for K=3 as n grows: reusing the finite calibration with more rounds cannot
create a fixed-copy asymptotic algorithm. The K=n^2 cap is vacuous, not positive
evidence for the proposed readout.
The source-adaptive missing-sign bound does not apply to these other target
sectors. The one-common-query/discarded-data bounds do not cover this retained
sequence. None of these scope differences is evidence of speedup.

The published [Moore/Russell/Sniady sieve model, Section 3](https://arxiv.org/html/quant-ph/0612089v3)
measures and combines states into a labeled forest. Do not simply transfer its
lower bound to this unmeasured, overlapping circuit. Conversely, a measured-
tree replacement must confront that result. We have not proved that the echo
cannot be rewritten as an already bounded model.

## Exact Three-Copy Contraction

Let a(g) be the real central coefficients of U=sum_g a(g)R_g. They are exact
integers divided by D, obtained from complete characters. Both Parseval and
the full convolution identity U^2=I are checked with integer arithmetic.

For one echo on three registers, the chronological variables a,b,c,d give
word factors ca, dcba, db on the three sites, using a homomorphic group-action
convention. A raw regular trace is zero unless each factor is identity; a
coset trace is the indicator that each factor belongs to {e,h}. Eliminate
the two endpoint constraints by setting c=x a^-1 and d=z b^-1:

    m_h = sum_(a,b in G) sum_(x,z in {e,h})
          a(a) a(b) a(x a^-1) a(z b^-1)
          1[z b^-1 x a^-1 b a in {e,h}].

For the null, use x=z=e and require the remaining word equal e. This reduces
four group variables to two; it does not make group enumeration polynomial
in n. Evaluate EVERY hidden member and check class covariance exactly.
Integer accumulation is bounded before evaluation; n>6 is refused by the
finite backend, rather than accidentally allocating factorial tables.

An independent source-block calculation uses irrep matrices and unnormalized
blocks. For a source tuple with dimension d_total, the row factor is
d_total/D^K, multiplying I under null or tensor(I+rho_lambda(h)) under the
alternative. This retains zero-alternative branches and their null mass.
It constructs the actual controlled-word Kraus operator (I-W)/2 and compares
its probability with the trace formula. It never substitutes Helstrom.
An S3 raw regular-matrix control bypasses all source formulas. Averaging h
independently on each copy produces a different law, an explicit falsifier.

## Results And Baselines

Exact one-echo output TV at K=3:

| Group / hidden class | Echo TV | Pair-plus-single TV |
| --- | --- | --- |
| S3 / transposition | 1/9 | 37/72 |
| S4 / two transpositions | 0 | 27/64 |
| S6 / three transpositions | 16843/303750 ~= 0.05545 | 38684413/186624000 ~= 0.20728 |

S4/transposition gives 31/432 and S5/two-transpositions gives 21/250. These are
additional exact controls, not growing fixed-point-free evidence. S3 is a
sign-only calibration and is already inside the previous asymptotic bound.
At S3,K=4, repeating the echo twice DECREASES the TV from 4/27 to 2/27:
iterations cannot be called amplification without analyzing their response.

The pair baseline uses a quantum measurement front end followed by a known
classical score. It is NOT an end-to-end classical algorithm. The factorial
contraction knows the two promised distributions; it is NOT a classical
solver for an unknown natural instance. Legal graph/code solvers and coherent
hiding-function search need their respective input interfaces, not free
access attached to a coset-only experiment.
Both K=3 comparisons use eight group-QFT/inverse calls under the existing
physical-register schemas: four phase calls for the echo, versus three source
label extractions and one pair label for the baseline. Other costs still differ.

No finite tested case beats the implemented pair baseline. Noncommutator norm
is recorded only to check that the new operation is genuinely different.
It is not a discovery metric.

## Next Decision

The valuable next task is a transfer-network representation or analytic
bound for the ACTUAL growing path word. At fixed layer count, horizontal
contraction can still have a group-sized/exponential-layer boundary; its
dimension and approximation error must be charged. A polynomial-in-K
classical calculation at fixed n is not dequantization in n.

Likely failures: both hypotheses' moments decay toward zero, giving the same
fair-coin output; depth yields oscillation rather than amplification; a
classical tensor contraction defeats the proposal; or the needed accuracy
and repetitions consume the apparent saving. Useful evidence would be a
proved inverse-polynomial gap of the fixed readout with polynomial total
cost, followed by an access-matched baseline and natural binary reduction.

Do not spend a long series of passes tuning this finite echo if no scalable
mechanism emerges. A broad obstruction or an explicit change of interface
can justify a pivot; repeated small-group gains cannot.

## Reproduce

    python qsearch.py coset-overlap-echo
    python qsearch.py run EXP-COSET-COHERENT-OVERLAP-ECHO
    python qsearch.py dequantize
    python qsearch.py proofs

CLI and runner share one result ID. `--no-registry` writes only the report.
Negative records retain the finite limitations; proof tracking explicitly
keeps the growing-bias/reduction obligation blocked. No candidate is promoted.
