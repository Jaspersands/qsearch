# Constructive Polar Gibbs Falsifier: No Free Source Table

2026-10-17. Known polarization, SC shaping and channel-duality mechanisms.
Local application and finite information-order certificates require review.
No novel quantum algorithm, all-code no-go or matched runtime advantage.

## Question And Decision

The preceding [polar sampler](POLAR_CONDITIONAL_SAMPLER.md) left an explicit
blocker: its average-case error criterion did not construct an appropriate
public code without an exponential source table. This pass removes that
blocker for concrete non-prefix families.

The signs model is not optional bookkeeping. [Zhou et al., Theorem 2.4 and
Theorem 3.1](https://arxiv.org/html/2609.40345v1#S2) use uniform random clause
signs and bound expected total variation. Their theorem does not supply
an arbitrary-sign guarantee. Thus the classical average-sign bound addresses
the actual proposed reduction, not an artificially weakened comparison.
It does NOT refute their random-hypergraph results: our code family is polar.

## Input, Mechanisms And Costs

Public input: power-of-two length N, rational overlap c, explicit polar
coordinate set F, and uniform public signs J. Set p=(1-c)/2 and let H_F
extract the selected polar coordinates. The task is sampling the kernel
word y with

```
H_F y=0,
weight(y) = product_j (1+c*(-1)^(y_j+J_j)).
```

Free polar coordinates of G(y) give the independent Ising spins in another
O(N log N) binary transform. The number of spins is N-|F|. A dense parity
matrix is polynomially expandable from N,F; no coherent access oracle or
unknown coefficient is provided. These interactions need not be sparse or
bounded-locality, and no random-LDPC/ER hardness claim is transferred to them.

Quantum proposal: known polar CQ successive cancellation, coherently used
inside the known DQI Gibbs reduction. Its synthesized message graphs avoid
the enormous LDPC extrinsic-tree issue. Good fidelity-based information sets
are a constructive decoding route, not a new algorithm or established
speedup. Reversible reliability arithmetic, retained workspace and the whole
Gibbs readout would still need to be charged.

Classical competitor: SC source shaping from the existing producer. It needs
only N,F,c,J, exact rational prefix probabilities and ordinary random bits.
It uses O(N^2) rational operations in this reference, not an exponential
source table. Rational numerator/denominator lengths are polynomial in N
and the input probability precision. Matrix/check generation and binary
transforms are additional charged work, not part of the rational counter.
Construction below costs O(N G^2) support-pair operations for G grid intervals,
plus polynomial-bit integer arithmetic. This is NOT a fine-grained matched
quantum/classical gate comparison or a claim of the best classical runtime.

## The Direct Decoder-Sampler Link

For source U=G(E), E_i IID Bernoulli(p), put

```
m_i = E |P(U_i=0 | U_<i) - P(U_i=1 | U_<i)|.
epsilon_F = (1/2) sum_(i in F) m_i.
```

The preceding hybrid argument gives average uniform-sign Gibbs TV at most
2 epsilon_F = sum_F m_i. There is no factor 2^|F| in this AVERAGE guarantee;
that factor arises only when trying to infer an arbitrary-syndrome bound.

The full posterior-magnitude laws have an exact recursion. For independent
child magnitudes a,b, an even source bit has magnitude ab. The odd source
bit has magnitudes (a+b)/(1+ab) and |a-b|/(1-ab), with branch weights
(1+ab)/2 and (1-ab)/2. The zero-probability a=b=1 branch is omitted.
Independence follows from the two disjoint source halves, not cloned data.

These are the same flagged pure-state channel combinations as BPQM, with
source/CQ indices reversed. In particular m_i equals the UNSQUARED root
Uhlmann fidelity of the reversed synthesized CQ bit-channel. Independent
small density matrices now verify this stronger identity, not just entropy:
root fidelity is computed from a purification-Gram nuclear norm, avoiding
spurious square roots of tiny numerical eigenvalues. Native N2/N4 errors
are below 3e-16; numerical checks are not formal theorem proofs.

Consequently, any polar Gibbs proposal whose justification is a vanishing
SUM OF THESE ROOT FIDELITIES also supplies this polynomial classical
average-sign sampler. A claim of a Shor-like separation cannot rest solely
on that criterion. This does not cover arbitrary joint receivers or every
weaker/different decoding-error criterion. No new channel-duality theorem
is claimed; see [Renes](https://arxiv.org/abs/1701.05583) and the
[BSC/PSC treatment](https://arxiv.org/abs/2103.09225).

## Certified Finite Construction

Use overlaps m_j=j^r/G^r, j=0,...,G, and exact normalized dyadic herald
masses with denominator 2^b. The nonuniform mesh is important: a uniform
overlap mesh rounds every tiny nonzero magnitude up to at least 1/G,
which can make sum_F m_i vacuous at useful block lengths.

Each independent parent pair is combined EXACTLY in integer arithmetic.
Round resulting overlaps UP on the mesh. Round each herald mass down to
the dyadic lattice, replacing the discarded mass with overlap-one states.
All discarded mass is retained in the accounting; no renormalization hides it.
The computed mean overlaps are therefore upper bounds on the true m_i.

Why the bound survives repeated combinations: this is PHYSICAL PSC
degradation, not first-order stochastic ordering of posterior magnitudes.
If 0<=a<=d<=1, the two-state Gram identity permits the map

```
|psi_x(a)> -> |psi_x(d)> tensor |psi_x(a/d)>,
```

followed by discarding the environment (with the zero endpoint treated
separately). Removing herald mass to an uninformative overlap-one flag is
also a degrading channel. Product and averaged channel combinations preserve
this order, and root fidelity cannot decrease under degradation. The lower
comparison uses the reverse information order. This is a mathematical
comparison, NOT permission to erase environments inside a coherent receiver.

An explicit test shows why a scalar shortcut would be wrong: plus-combining
(a,b)=(0.1,0.9) versus (0.5,0.9) gives crossing posterior-magnitude CDFs.
Neither ordinary stochastic ordering nor mean-only rounding proves the
recursive certificate. Native exhaustive source controls and the previous
uniform-grid integer implementation independently check the nonuniform code.
Bounded-alphabet construction has substantial prior art, including
[Tal and Vardy](https://arxiv.org/abs/1105.6164); this is not claimed to be
their exact merge algorithm or a better construction theorem.

Select F by the smallest certified means. The report retains ALL N upper
bounds, F itself, the grid, exact masses' precision, pair/rounding work and
producer/helper hashes. It also retains failed target designs. The reported
maximum set size is maximum for THIS bound vector and TV budget, not the
optimal polar code or a capacity upper bound.

## Live Outcomes

At c=13/20, p=7/40, coarse G=64,r=4,b=96:

| N | Largest set certified at average TV<=0.1 | Rate |
| --- | --- | --- |
| 64 | 16 | 0.25 |
| 256 | 78 | 0.304688 |
| 1024 | 361 | 0.352539 |
| 4096 | 1614 | 0.394043 |

The half-rate targets in these coarse controls all FAIL certification.
Their status is UNKNOWN at this resolution, not hardness or impossibility.
A clearly labelled post-exploration rate3/8 follow-up at N4096 has certified
average TV<=0.023431. It is non-prefix and exceeds the product-USD code-rate
ceiling 1-c=0.35. That ceiling is only for the specified full-rank product
USD/Prange mechanism, not all classical algorithms; this sampler is itself
a stronger classical algorithm. The certificate is not a quantum advantage.

The larger G=256,r=3,b=96 calculation succeeds at N32768, |F|=16384:

```
average uniform-sign Gibbs TV
 <= 424553765284920852120940002337825
    /41538374868278621028243970633760768
 < 0.010221.
```

It uses 65,534 channel combinations and 1,008,335,816 active support-pair
visits. The expensive setup is disclosed, not treated as free advice. The
initial exploratory run was repeated to save the full reproducible artifact.
This finite result removes the missing public-set construction premise for
the stated half-rate family. It does NOT prove a fixed-grid asymptotic
convergence theorem, a general Gibbs sampler, or an all-sign result.

An actual N1024,361-constraint non-prefix Gibbs sample is executed and its
native kernel checks are verified. The reference accepts lengths through
32768, but a 32768-bit Gibbs draw has NOT been executed; its polynomial
O(N^2) exact-arithmetic sampler can be expensive. Large-bound verification
checks provenance, all upper-bound arithmetic and selected-set sums, not
another billion-pair replay inside each unit-test run. That distinction
must remain explicit. Full-law TV is independently checked only on small
native sources; general validity rests on the stated review-pending proof.

## Execute And Falsify

```
python theorems/polar_conditional_sampler.py --write
python theorems/polar_source_design.py --write
python theorems/polar_source_design.py --length 32768 --grid 256 --power 3 --write
python -m pytest tests/test_polar_conditional_sampler.py tests/test_polar_source_design.py -q -W error::RuntimeWarning
```

The parameterized command writes a separate parameter-labelled artifact;
it does not overwrite the coarse failures. Reject this certificate if an
independent exact source calculation exceeds an upper bound, if physical
degradation/duality does not apply, if the source uses the coherent flip
probability gamma instead of p, or if future frozen information is uncharged.
An adversarial sign regime requires a different proof, not this average bound.

## Research Decision

Do not compile another natural SC-fidelity polar receiver to argue a
random-sign Gibbs advantage: the matching classical route is now constructive.
Do not extend mesh/block-size scans as the next research project. A next
pass must identify a genuinely different efficient quantum receiver/code
mechanism that escapes this classical sampler, or pivot independently.
Random LDPC/cyclic composition, arbitrary-sign sampling and non-SC joint
measurements remain unresolved; no barrier for those is established here.
No accepted candidate, broad negative entry, proof promotion or Git operation.
