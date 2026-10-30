# Nonlinear Decoding Does Not By Itself Protect Pauli Readouts

2026-10-24. LOCAL UNREVIEWED deductions, exact finite algebra controls, and
conditional resource plans. No production FPRAS, quantum circuit, novelty,
independent proof, or speedup claim.

## Research Question And Decision

The preceding line-graph flux-gap pass supplies a locally derived ideal
polynomial pilot-preparation route at small beta^2(d+1). The next important
question is what useful task that makes difficult classically. Full output
sampling remains unresolved. Earlier Pauli-readout comparators covered
linear decoders, or arbitrary decoders only with polynomial sign overhead.
Could an efficient NONLINEAR decoder evade those readout comparators?

Not merely by being nonlinear. A uniform error-correction margin transfers
actual decoded Pauli readouts to the existing degree-scale canonical Pauli
comparator. This holds even when the earlier certified sign envelope is
superpolynomial. It covers energy terms with a small margin, and arbitrary
specified Paulis with a stronger margin. The result is about the actual
decoder output, with fixed input coupling signs, not an assumed Gibbs state.

The quantum mechanism being tested is now fully specified: prepare the
canonical pilot, apply the public physical Pauli word map, reversibly decode
the relation syndrome, and measure a specified physical Pauli. Both sides
receive the same explicit Hamiltonian and decoder. No source, matrix element,
decoder-success oracle, restricted classical access, or unknown advice is
granted. Quantum preparation may still have other uses; this result does
not rule out full sampling or subsequent quantum processing.

## Native Input And Exact Channel

Let P_i be explicit Hermitian physical Paulis, B their binary-label matrix,
and Dec a total deterministic classical function returning an m-bit mask.
The canonical generators O_i have the same commutation matrix as P_i and
are independent. For real |J_i|<=1, the pilot is

    |psi>=exp(-beta sum_i J_i O_i/2)|0>/sqrt(Z_hat).

For an ordered physical product P(y), use the normalized Bell vector
|P(y)>=(P(y) tensor I)|Bell>. The actual decoding isometry is

    V|y>=|y xor Dec(By)> |P(y)>.

It is an isometry even if the decoder is bad: identical physical labels
and identical residual labels force identical y. For a physical Hermitian
Pauli Q, the pullback A=V^*(I tensor Q_left)V is Hermitian with norm <=1.
The target expectation is <psi|A|psi>. A Gibbs interpretation needs its own
proof and is not used here. The published construction and thermal error
inclusion bound are in [Hastings--Schmidhuber, Section II and Appendix A](https://arxiv.org/html/2610.03697v1).

All claims below require the UNIFORM decoder contract

    Dec(By)=y for every y with |y|<=t.                       (1)

An observed success rate, successful sampled labels, code dimension, or a
declared radius does not prove (1). `verify_ball` is exhaustive but capped;
it proves only its finite instance. For large instances a structural code
and decoder proof must supply (1). The planner deliberately does not certify
the contract from an input integer.

## 1. Short-Word Transfer

Suppose a public word h represents Q's binary label. There is a computable
phase alpha in Z/4 with Q=i^alpha P(h). Define the Hermitian coefficient
Pauli L_h=i^alpha O(h), preserving ordered-product phases. In binary form,

    L_h = i^alpha X^h Z^ell(h),
    ell(h)_j = sum_{i>j, i~j} h_i mod 2.

Take k=t-|h|>=0. If |y|<=k then both y and y+h are decoded correctly.
Consequently A|y>=L_h|y>: the sole physical label with residual zero and
syndrome By+Bh is the correctly decoded y+h, and its phase is precisely
the ordered-word multiplication phase. This is agreement of ENTIRE COLUMNS,
not just agreement of diagonal or low-weight block entries.

Let Pi_k project onto labels of weight <=k, and
delta=||(I-Pi_k)psi||^2. Since ||A-L_h||<=2,

    |<psi|A|psi>-<psi|L_h|psi>| <= 2 sqrt(delta).          (2)

No linearity or average-case analysis of Dec was used. In particular each
Hamiltonian term has |h|=1, so an error-correction margin of one bit beyond
a high-probability pilot weight cutoff suffices. Products of a fixed number
of terms have the analogous constant margin. Physical Pauli support size
and GENERATOR-word length are different quantities and must not be confused.

## 2. Arbitrary Specified Pauli Transfer

Now suppose t>=2k; the observable Q need not arrive with a short word.
Let q be its binary label and compute h=Dec(q). Retain h only if Bh=q and
|h|<=2k. If no such checked h is returned, put L=0; otherwise put L=L_h.
This uses one call to the original decoder, not a new coset-leader oracle.

For y,y' of weight <=k, their residual labels both vanish. A nonzero
matrix element A_(y',y) requires B(y+y')=q, and |y+y'|<=2k<=t. Contract
(1) forces Dec(q)=y+y'. Thus there is at most one relevant difference h,
and its phases match the lift above. Therefore

    Pi_k A Pi_k = Pi_k L Pi_k.                            (3)

This is BLOCK agreement, not column agreement. Comparing psi with its
normalized projected state gives a pure-state trace distance sqrt(delta).
The two norm-one observables each change expectation by <=2sqrt(delta),
so

    |<psi|A|psi>-<psi|L|psi>| <= 4 sqrt(delta).            (4)

If L=0, 2sqrt(delta) is sufficient; the implementation uses the conservative
common bound. No claim is made that a decoder correct to k also identifies
differences of two weight-k words. The doubled margin is essential to this
particular one-lift reduction.

## 3. Explicit Thermal Tail And Classical Complexity

The published inclusion bound gives, with q_i=(beta J_i/2)^2,

    Pr[S subset supp(Y)] <= product_{i in S} q_i.

For threshold l=k+1 and every 1<=j<=l, apply Markov's inequality to
binom(|Y|,j):

    Pr[|Y|>=l] <= e_j(q_1,...,q_m)/binom(l,j).              (5)

The implementation computes the elementary symmetric polynomials by exact
rational dynamic programming in O(ml) arithmetic operations, takes the
minimum with one, and handles k<0 or k>=m explicitly. It never treats the
pilot bits as independent Bernoulli variables.

A simple all-size choice avoids an optimization oracle. Let mu=sum_i q_i.
Set l=max(1,ceil(6mu),ceil(log2(256/epsilon^2))) and k=min(m,l-1). Since
l!>=(l/3)^l, mu^l/l!<=(3mu/l)^l<=2^-l. Thus delta<=epsilon^2/256 (or zero
when k=m). The recommended cutoff is sufficient, not minimal. Work remains
polynomial and does not require a statevector, a Gibbs sampler, or a sign
envelope. The code may use a sharper explicitly requested cutoff via (5).

Once the transfer error is <=epsilon/2, invoke the earlier canonical Pauli
comparator at additive epsilon/2. Its local theorem applies at

    (d+1)(beta J_max)^2 <= 1/64.

It is conditional on the unreviewed proof in the predecessor
DEFECT_OBSERVABLES.md / CLUSTER_BASELINE.md, not an external established
FPRAS. Its code implements capped reference controls and resource plans,
not a production end-to-end estimator. This pass calls that existing
planner and preserves `production_estimator_executed: false`.

Large lift words do not cause an exponential runtime in that theorem:
|<L_h>|<=product_{i in h} beta|J_i|. Outside the deterministic zero branch,
only |h|=O(log(1/epsilon)) is relevant; the signed marked-cluster estimator
has polynomial cost independent of d in its exponent. Exact imaginary-
Pauli zeros of the real canonical state are also retained. These facts
cannot be substituted for a full output distribution or rare-event oracle.

For O=sum_a c_a Q_a, let W=sum_a |c_a|. Estimate terms to accuracy
epsilon/W and allocate failure probabilities, or sample terms with
probability |c_a|/W. Complexity depends polynomially on W/epsilon. For
total energy W=sum|J_i|, whereas normalized energy density divides by W.
Do not quote density precision as total-energy precision. Decoder running
time and the input Pauli bit lengths are charged separately.

## 4. An Explicit Nonlinear Native Family Outside The Old Sign Guarantees

This is a control/application family, not a proposed hard sampling problem.
Take any even-degree anticommutation graph G on m>=3 vertices. On n=m-1
physical qubits use the first m-1 canonical generators and let the last
physical generator be their ordered product, multiplied by the known
phase making it Hermitian. Even vertex degree ensures that this last
generator has exactly the required commutations. The first m-1 X labels
are independent, while the last X label is their sum. Therefore

    ker B = span{(1,...,1)}.

Given By, binary elimination finds one of the two preimages, y and its
complement. Choosing the smaller Hamming weight is a polynomial classical
decoder correct on every word of weight <=floor((m-1)/2). It is nonlinear:
two disjoint low-weight representatives can sum to a high-weight word whose
decoder is its complement. All physical Paulis and their phases are public;
there is no hidden function or oracle problem.

For direct compatibility with the new preparation theorem choose G=L(K_v).
Its degree is d=2(v-2), which is even. Put v=2s^2 and beta=1/(32s). Then

    m=s^2(2s^2-1), d+1=4s^2-3,
    beta^2(d+1)<1/256,
    beta*d=s/8-1/(8s) -> infinity,
    beta^2*m=(2s^2-1)/1024 >> log m.

The usual mass-bound and existing cluster-bound log sign envelopes both
grow as Theta(s^2); those particular guarantees do NOT give polynomial
sign-sampler cost. This is not a lower bound on the true optimal sign cost.
Meanwhile mu=Theta(s^2) and the guaranteed decoding radius is Theta(s^4).
For inverse-polynomial epsilon, the required k is O(s^2+log m), so the
arbitrary-Pauli margin holds for sufficiently large s. The physical input
and reversible decoder are explicit and polynomially sized. Canonical
pilot preparation, nonlinear decoding, and arbitrary specified Pauli
readout therefore fail to supply a superpolynomial advantage for this
family under the local classical comparator theorem.

The live input uses v=32, m=496, n=495 with no Hilbert-space allocation.
Its requested readout precision is 1/4096, below the 1/128 single-flip
bound; the resulting plan needs the marked estimator, not a coarse zero.
The sufficient pilot cutoff is 31. Its radius-247 guarantee is justified
by the two-preimage algebra, not an
exhaustive 2^m check. The large-s asymptotic ledger is symbolic, not an
executed enormous instance. Small actual Majorana-cycle models separately
test the channel identities against physical Bell matrices, including
negative couplings, Y phases, and out-of-image observables.

## 5. A Native Counterexample To Removing The Margin

Use the four-cycle Majorana bilinears with unit couplings. The relation
code is repetition of length four; its minimum-weight decoder is correct
on every weight-one input. Take the degree-one native filter pilot

    H_hat|0>/||H_hat|0>|| = (|e_0>+|e_1>+|e_2>+|e_3>)/2.

This has NO weight tail beyond k=1, and decoding succeeds on its entire
support. The observable Q=P_0 P_2 also has representative P_1 P_3. In
the explicit Pauli convention it is Z_0 Z_1. Its actual decoded expectation
is 1, while choosing only the canonical lift O_0 O_2 gives 1/2. Hence
perfect average decoding success, even on the full weight-k ball, does
not permit the arbitrary-readout one-lift reduction without the stronger
difference-decoding margin. This is an exact finite algebra counterexample,
not evidence that the small system is difficult classically.

Separately, at beta=0 the decoder that always returns zero has perfect
pilot-average success but fails the radius-one contract. The planner must
not promote an average success statistic into (1).

## Research Consequence And Remaining Risk

The result changes what should count as a promising continuation of the
new preparation route. A nonlinear classical decoder is not, by itself,
an escape from additive Pauli/energy dequantization. A proposed advantage
must state the actual observable and show why these contracts fail or why
the task goes beyond them: full sampling, non-Pauli measurement, subsequent
quantum processing, insufficient decoding margin, or a different regime.

The strongest unresolved cases include average-case decoders correcting
extensive structured errors without a comparable worst-case ball radius,
and joint output sampling. This result neither solves nor rules out those
tasks. It also does not establish independent correctness or novelty of
the predecessor cluster or flux-gap proofs. Do not create another family
of readout benchmarks; the next constructive pass must identify a useful
task that survives the actual comparators, or pivot away from this input
class. No new circuit-search, UI, registry, or CLI work is justified here.
