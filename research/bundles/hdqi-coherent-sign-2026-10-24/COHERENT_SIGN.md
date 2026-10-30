# Coherent Pilot Preparation From Conditional Signed Words

Date: 2026-10-24. LOCAL, UNREVIEWED construction. This is a proof and finite
algebra checker, not a compiled quantum circuit, hardware execution, new
generic primitive or certified novelty claim.

## 1. What This Removes

The preceding classical sampler does not itself prepare a coherent pilot.
Its conditional signed-word representation nevertheless gives a NEW,
explicitly specified coherent procedure. It preserves signs and erases
word histories by applying their preparation inverse. This supplies pilot
preparation whenever a polynomial bound on the sign ratio C is established,
WITHOUT needing the filtered-parent gap. It does not prove that gap.

In particular, the cluster-derived bound covers the growing-degree family
from the preceding pass, outside the older logarithmic-mass and beta*d-small
comparator regimes. Classical computational-basis sampling is also efficient
there. A useful quantum advantage still needs a physical HDQI decoder/output
that uses interference and defeats the corresponding classical approaches.

The mechanism is a controlled prepare/select/unprepare application of
standard LCU ideas, not a new algorithmic framework. Primary references:
[Childs--Wiebe](https://arxiv.org/abs/1202.5822) for linear combinations of
unitaries, [Ozols--Roetteler--Roland](https://arxiv.org/abs/1103.2774) for
quantum rejection sampling. The derivation and precision bounds below are
supplied for this specific public-input model, not asserted to be theorems
of those papers.

## 2. Same Explicit Input, Not A State Or Amplitude Oracle

Input is the public simple graph G with m vertices, rational |J_i|<=1 and
0<=beta<=1. The canonical independent Pauli operators and target are

    O_i=X_i prod_{j<i,j~i} Z_j, H=sum_i J_i O_i,
    |pi>=exp(-beta H/2)|0>/sqrt(Z), Z=tau(exp(-beta H)).

As proved in ../hdqi-sign-sampler-2026-10-24/SIGN_SAMPLER.md, set
x_i=beta|J_i|/2, b_y=prod_i f_{y_i}(x_i), f_0=cosh, f_1=sinh,
Z_c=prod cosh(beta J_i), q(y)=b_y^2/Z_c, C=Z_c/Z>=1. Then

    a_y=<y|exp(-beta H/2)|0>=s_y b_y r_y,
    s_y=(-1)^|y| prod_i sign(J_i)^y_i,
    r_y=E[sigma(W)|y], |r_y|<=1.                           (1)

W is a uniformly shuffled multiset of independent parity-conditioned
Poisson counts with weights x_i^k/k!, and sigma(W) is the canonical word
sign on vacuum. No oracle returning a_y or r_y is available. Zero-coupling
bits have zero proposal probability of one and are handled separately.

## 3. The Coherent Procedure

First prepare |q>=sum_y sqrt(q(y))|y>, using independent single-qubit
rotations from the explicit cosh/sinh probabilities. Define a controlled
word-history preparation U by

    U|y>|0>=|y> sum_h sqrt(P_y(h)) |h,word(h)>.

Histories h include the count choices and ALL shuffle choices. Repeated
labels can have several histories giving the same word: their probabilities
must add, not their amplitudes. Retaining the histories makes the computation
reversible. Let D_sigma be the diagonal sign phase of the computed word.
Compute its sign with reversible bit-mask arithmetic, apply the phase and
uncompute the sign computation. Now apply U^dagger. Exactly,

    <0| U_y^dagger D_sigma U_y |0>=sum_h P_y(h)sigma(h)=r_y. (2)

Apply s_y (a known product of Z gates). Project ALL work registers onto zero.
The successful, unnormalized label state is

    v=sum_y s_y sqrt(q(y)) r_y |y>
      =exp(-beta H/2)|0>/sqrt(Z_c), ||v||^2=1/C.           (3)

This preserves relative amplitude signs, not their absolute values. Failure
is a genuine heralded failure, never an all-zero pilot. Neither the target
state nor its reflection is used as an input operation.

Equation (3) is first an ideal identity. Infinite count support and exact
transcendental rotations are NOT treated as free gates; the finite version
below is the algorithm.

## 4. Finite Reversible Realization, Without Exponential Tables

For each site and parity, use the preceding sampler's rational truncated
weights x_i^(2j) p!/(p+2j)!, with omitted weight at most eta. Each local
table has O(log(1/eta)) entries, since x_i<=1/2. Its exact probabilities are
rational. The proposal bit probabilities use retained sums E_i,O_i:

    q'_i(1)=O_i^2/(E_i^2+O_i^2).

Only two small tables per site are needed; no table over 2^m labels exists.
Conditional local state preparation uses rotations with angles computed to
the allotted precision. Very small rational x_i raises precision bit costs,
not an inverse-x_i count-rejection loop.

Let L_max be the sum of the largest retained local counts. Reversibly write
the multiset into L_max padded label slots and compute its active length L.
For j=L_max,...,2, controlled on L>=j, prepare a fresh uniform integer in
[0,j), retain that integer, and swap word positions j-1 and that integer.
This is Fisher--Yates with retained choices, not an irreversible PRNG call.
It is uniform on permutations of labeled copies. Each distinct repeated-label
word occurs prod_i N_i! times, so its induced distribution is correct.

All counts, lengths, inactive slots, shuffle indices and arithmetic scratch
are included in U and its inverse. Uniform-range preparations can use O(j)
explicit small-table rotations; summing j gives O(L_max^2), still polynomial.
Controlled routing and graph lookup can use direct reversible scans, with
polynomial overhead in m, |E| and L_max. No QRAM assumption is needed.
Sign evaluation scans a word of length at most L_max against public lower
neighbor masks. Such scans and their inverses must be charged.

The code reports local-table sizes, word slots, retained shuffle bits and
a deliberately loose count of ABSTRACT controlled rotations. These are
not a compiled elementary gate count or a complete physical qubit estimate.
Decomposing each abstract rotation and its controls to operator error nu is
polynomial in the register size and log(1/nu). Reversible Boolean operations
can use exact Toffoli/Clifford gates. Input rational bit length is charged.

## 5. Precision, Postselection And Failure Budget

Let eps,delta in (0,1/4] and let C_bar>=C be the integer analytic bound from
the preceding sampler. Use the entirely rational choices

    eta=eps^2/(16384 m C_bar^2),
    circuit_error=eps/(16 C_bar).                         (4)

The latter is a whole-trial operator-norm budget, apportioned among all
approximate rotations in q', U and U^dagger. Inverses use the same compiled
unitaries in reverse, not newly sampled approximations.

The ideal product proposal and its truncated version obey
TV(q,q')<=5m eta. Hence

    ||sqrt(q)-sqrt(q')||_2<=sqrt(10m eta).

Uniformly on supported y, truncating the independent counts changes the
word law by TV<=m eta, so |r'_y-r_y|<=2m eta. The finite ideal success vector
v' therefore differs from v by at most

    ||v'-v||<=sqrt(10m eta)+2m eta<=eps/(16 C_bar).         (5)

For the last inequality, sqrt(10)<4, eps<=1 and C_bar>=1 suffice.
Add the whole-trial circuit budget to obtain for the compiled success vector u

    ||u-v||<=eps/(8 C_bar).

Since ||v||=1/sqrt(C)>=1/sqrt(C_bar), normalizing changes the state by
Euclidean distance at most 2||u-v||/||v||<=eps/4. Pure-state trace distance
is no larger. This is a CONDITIONAL successful-state guarantee, not a claim
that postselection preserves an unscaled absolute error.

Moreover ||u||>=(1-eps/8)/sqrt(C_bar), so actual success probability is
at least 1/(2 C_bar). Put r=ceil(log_2(1/delta)). Reinitialize after a failed
herald and make at most

    T=2 C_bar r                                               (6)

independent preparations. Failure is at most exp(-r)<=2^-r<=delta. Every
success has the same compiled conditional state; repeated attempts do not
increase its conditional state error. Expected attempts are at most 2C_bar.
This simple version already proves polynomial time when C_bar is polynomial.

Fixed-point amplitude amplification can improve the number of preparation
calls using the lower bound on success, the trial unitary, its inverse and
known zero-work tests; see [Yoder--Low--Chuang](https://arxiv.org/abs/1409.3305).
That refinement is NOT implemented or needed for this theorem. Its phase
synthesis and inverse-call precision must be budgeted before use. The
present ledger makes NO square-root-call or deterministic-preparation claim.

The mathematical gate model assumes the compiled gates operate as specified.
Hardware noise, error correction and physical runtimes are not included.

## 6. Regime, Classical Comparator And Remaining Question

The computable C_bar comes from the same two inequalities as the classical
sampler: log C<=beta^2 sum J_i^2/2 and, under (d+1)lambda<=1/64,

    log C<=128m(d+1)lambda^2/[1-16(d+1)lambda],
    lambda=(beta Jmax)^2.

The second depends on the preceding local UNREVIEWED cluster proof; it
must not be laundered into an independently established theorem here.
Edgeless graphs have C=1 and a direct product preparation anyway.

For even N>=2, the connected m=N^8,d=N^4 circulant with J_i=1,
beta=1/(16N^3) has C_bar=3. The previous mass exponent grows as N^2/512,
while beta*d=N/16 diverges. The construction thus supplies a coherent
preparation comparator outside both previously priced regimes, subject to
the local proof. Huge-family ledger rows are NOT constructed inputs or
quantum executions. The explicit edge list is part of the input cost.

At fixed small (d+1)beta^2, the cluster exponent remains O(m/(d+1)). It does
NOT make the full large-connected-mass degree regime polynomial. A large
bound is not a lower bound on C and not evidence of quantum hardness.

Both this procedure and the previous classical bit-string sampler are
polynomial in the stated C_bar regime. Their outputs differ: the classical
sampler cannot execute an interfering decoder. A credible advantage claim
must specify such a physical output and attack it classically. Proving a
parent gap only within this already-preparable regime is now lower priority.

## 7. Falsifiers And Evidence Limits

- Dropping the word phase gives the envelope, not the pilot.
- Dropping s_y changes relative phases even on a commuting two-site input.
- Measuring/discarding histories instead of applying U^dagger generally
  leaves a mixed state; basis histograms cannot establish coherent fidelity.
- Overwriting a shuffle history is not reversible. Repeated labels do not
  license merging orthogonal histories coherently.
- Fixed absolute rotation errors without the C_bar factor can be magnified
  by postselection. The bound in (4) prices that amplification.
- Exhaustive word/statevector controls are exponential and are not the
  proposed implementation. They are capped and marked as finite references.
- This result does not transfer to redundant Pauli inputs, inaccessible
  graphs, complex couplings, or an arbitrary externally supplied pilot.
- No decoder, preparation-gap theorem, classical hardness or Shor-level
  algorithm is established by these controls.

