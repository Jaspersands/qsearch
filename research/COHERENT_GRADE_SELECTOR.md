# Coherent Grade Selection: A Normalization Obstruction

30 October 2026. Exact bounded certificate for a proposed source-saving
instrument. This is not a general receiver lower bound, an asymptotic copy
bound, a new HSP algorithm, or evidence of classical hardness.

Constructive follow-up: the [invariant-Gram receiver](INVARIANT_GRAM_REES_RECEIVER.md)
escapes this FOUR-copy obstruction using 14/16 sources, invariant Gram
measurements and an explicit bounded controller. It does not invalidate
the finite certificate below or establish a general-rank improvement.

## Scientific Question

Can one bank cancel several Rees grades coherently, avoiding the product
of the sequential grade arities? Measuring every noncentral character first
is already excluded by [the premature-measurement control](REES_PREMATURE_GRADE_MEASUREMENT.md).
Here the individual lower-grade labels remain COHERENT. The proposed
instrument computes only a simultaneous cancellation witness and exposes
that witness. It is therefore a genuinely different interface.

Finding a witness is insufficient. Its selection probabilities must also
preserve the coherences that carry the hidden subgroup. The exact example
below has a witness at EVERY label but admits no complete selector in the
specified diagonal, branchwise exact class. Aborting selectors in this class
have conditional acceptance at most 109/125. This does not require or assume
that an LP solver's infeasibility report is correct.

## Actual Rees Source And Restricted Instrument

Use the class-three filiform algebra over F5 with basis X,Y1,Y2,Y3 and
[X,Y1]=Y2, [X,Y2]=Y3. In its genuine positive Rees cover, let

    N = exp(span(t^2 Y2, t^2 Y3, t^3 Y3)),
    K = exp(F5 * tX).

This K is the actual lift of exp(F5*X), not an invented label oracle.
N is abelian and normal. Its character labels are (alpha,beta,ell).
Conjugation by exp(a*tX) changes alpha by +/- a*ell; the sign depends
only on the convention for right actions. Both beta and ell correspond
to central directions, so measuring THEM does not destroy K coherence.

Take four independent ideal mixed K-coset states. Condition on the central
record ell=(1,1,1,1), beta=(0,0,0,0), and do not measure alpha in F5^4.
This is a positive-probability record, of mass 5^-8. Its alpha diagonal is
uniform on all 625 labels. Retain all other registers; no hidden-subgroup
advice, inverse preparation, or source purification is supplied.

For s in F5^4, s!=0, define V_s(g)=tensor_i R_(Delta_si(g)), with an
identity action on zero-scale slots. A diagonal witness Kraus operator has
scalar amplitude a_s(alpha) on each alpha block; w_s=|a_s|^2. Independent
classical randomness or several diagonal Kraus operators with the same s
can be included by summing their weights. They must satisfy

    sum_s w_s(alpha) <= 1.

The missing mass is explicit abort. A complete selector has equality.
This class excludes alpha-mixing Kraus operators, hidden extra sources,
retained oracle-label purifications, and later corrective receivers.

The proposed ALL-GRADE MOMENT-SUPPORTED interface requires support only where

    sum_i s_i^3 = 0,             sum_i s_i^2 alpha_i = 0.

This support restriction is an explicit hypothesis, not a consequence of
quotient correctness for every possible instrument. The beta equation is
already zero. To contract to the correct quotient
source, a successful branch must also have unit correlation at K, not
merely zero phase on N. V_s(exp(a*tX)) shifts alpha by +/- a*s.

## Why Coherence Forces An Invariant Selector

Let rho denote the conditional four-source state. It obeys V_s(h)rho=rho
for h in K, since every dilation preserves K and the central conditioning
commutes with these actions. Its diagonal mass at every alpha is 1/625.

For the unnormalized successful branch B_s=A_s rho A_s^dagger, unit
correlation means Tr(B_s V_s(h))=Tr(B_s), not Tr(B_s V_s(h))=1.
Positivity implies

    (V_s(h)-I) A_s rho^(1/2) = 0.

Using V_s(h)rho^(1/2)=rho^(1/2), its commutator with A_s therefore
annihilates rho^(1/2). Conjugating A_s shifts its scalar diagonal blocks.
Its squared Hilbert--Schmidt norm equals
625^-1 sum_alpha |a_s(alpha+s)-a_s(alpha)|^2. Thus every difference
vanishes. In particular

    w_s(alpha+a*s) = w_s(alpha) for every a in F5.

Several Kraus operators cannot cancel a violation: the support condition
holds for each positive summand. This is a necessary condition in this
instrument class, not an assumption that every quantum receiver is diagonal.
Moment support gives V_s(n)B_s=B_s for every n in N; hence correlations at
h*n and h agree. This connects the necessary condition to the desired
quotient even when a chosen section does not represent its difference by h.
Mere conjugation invariance V_s(h)B_s V_s(h)^dagger=B_s would not suffice.

For fixed s satisfying the cubic equation, the hyperplane
H_s={alpha:sum s_i^2 alpha_i=0} is invariant under alpha -> alpha+a*s.
Hence w_s is a nonnegative combination of indicators of affine lines
alpha+F5*s contained in H_s. Scaling s by any nonzero field element changes
neither H_s nor these lines. It suffices to retain first-nonzero-entry-one
representatives: exactly 31 directions, each with 25 lines, or 775 lines.
Every one of the 625 points belongs to at least one such line.

## Integer Certificate

For alpha, define its canonical key as the lexicographically smallest
sorted tuple among t*alpha for t=1,2,3,4. Define a nonnegative integer z
by the following twenty keys; omitted keys do not occur.

| Key | z | Key | z |
| --- | ---: | --- | ---: |
| 0000 | 30 | 1111 | 30 |
| 0001 | 10 | 1112 | 5 |
| 0011 | 20 | 1113 | 0 |
| 0012 | 0 | 1114 | 0 |
| 0014 | 10 | 1122 | 0 |
| 0111 | 0 | 1123 | 10 |
| 0112 | 0 | 1124 | 5 |
| 0113 | 5 | 1134 | 10 |
| 0114 | 10 | 1144 | 0 |
| 0123 | 0 | 1234 | 10 |

Exact enumeration verifies BOTH

    sum_(alpha in line) z(alpha) >= 30 on every legal line,
    sum_(alpha in F5^4) z(alpha) = 3270.

Write q_line>=0 for the constant selection weight on a line. Completeness
with abort requires a(alpha)=sum_(line containing alpha) q_line<=1. Then

    5 sum_line q_line
      <= (1/6) sum_alpha z(alpha) a(alpha)
      <= 3270/6 = 545.

The left side is total accepted mass summed over the 625 labels. Thus
average acceptance is at most 545/625=109/125, and abort is at least
16/125 in this conditioned sector. A complete exact selector is impossible.
The test verifies the integer inequalities directly; there is no solver,
floating-point tolerance, asymptotic extrapolation, or stored LP status in
the certificate. Numerical optimization suggested this certificate and
attained 0.872, but no exact primal solution is retained, so no optimality
claim is made.

## Uniform-Over-Witness Selection Also Fails

A second exact control illustrates the normalization error. Use four
sources with ell=(1,1,1,0), beta=0 and alpha_4=0. At alpha=0 there are
124 nonzero simultaneous witnesses. For s=(0,1,4,0), the valid hidden
action changes alpha to (0,1,4,0), which has only 44 witnesses. The same s
is valid at both points, but its uniform selection weights are 1/124 and
1/44. They violate the coherence condition. The zero-character fourth
slot guarantees existence of a witness everywhere on this slice; failure
is not explained by an empty solution set. This does not rule out a
different, nonuniform selector on that slice.

## Scope And Next Constructive Gate

The 16/125 bound is CONDITIONAL on a fixed finite central record; it is
not a global constant-loss bound or an obstruction for growing bank size.
Even for this record an aborting selector is allowed, and bounded retries
remain possible. No necessity of the sequential product bound follows.
The sources are mathematical controls, not proposed toy-oracle candidates.

In particular, the moment-support restriction cannot be dropped. For this
specific K, the usual second-kind section and the unchanged centrally
conditioned source, with s=(1,0,0,0), already contract to the correct quotient
source without cubic cancellation. Differences of section representatives
whose quotient lies in the X line are pure X elements. This does not solve
unknown arbitrary H, but excludes a broader interpretation of our certificate.

The useful next task is a constructive, coherently implementable selector
or receiver that escapes this interface: for example, a larger-bank
aborting instrument with proved uniform acceptance and paid implementation,
or a genuinely basis-mixing collective instrument. An existential SDE
theorem, a uniform sampler over its solutions, or a new source-count
calculator alone does not supply that missing instrument. First verify its
COMPLETE quotient channel, including abort and every auxiliary record.

## Replay

    env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error tests/test_coherent_grade_selector.py

Four tests pass. The 625 points, 31 directions and 775 lines are bounded
finite arithmetic controls, not a scalable receiver implementation. Related
agent review and the wider application comparison are recorded separately.
Gibbs independently checked the source conditioning, necessary operator
identity, and integer certificate. Its line-price histogram is
30:667, 40:48, 50:48, 70:12; the witness-count histogram is
1:64, 6:476, 11:84, 31:1. This is automated review, not human peer review
or formal verification. The operator identities are analytical arguments;
the tests check the finite combinatorics, not a quantum implementation.
