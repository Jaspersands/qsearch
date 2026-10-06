# Native Least-Trit Pair Collimation

LOCAL DERIVATIONS / REVIEW PENDING. An actual source-valid receiver and a
conditional arithmetic reduction, NOT a polynomial witness finder or speedup.

## Research Decision

Independent native product outputs, identical unknown copies, coherent witness
samplers and a three-corner incoming oracle are not universal requirements for
a weak least-trit learner. A measured-frequency fiber followed by an ordinary
two-witness computation gives a simpler interface. This avoids those particular
demands; it does NOT make the witness computation easy.

The core quantum mechanics is established collimation:
[Regev, Section 3](https://arxiv.org/pdf/quant-ph/0406151) measures a common low
sum, finds endpoints, and projects to a two-term phase state.
[Kuperberg, Algorithm 4.1](https://arxiv.org/pdf/1112.3333) develops phase-vector
collimation with explicit indexing/storage costs. This pass specializes an
ordinary two-witness interface to the ORIGINAL ternary native source, with
all-failure weak-trit accounting. No novelty is claimed.

## Original Source And Stripped Solver Input

At even level `2r`, take `M=n*r-2>=1` independently supplied native qutrits at
the FULL modulus `q=3^r`:

```text
D^(-1/2) sum_(x in F3^M) chi_q(F(x).s)|x>,
D=3^M; F(x)=sum_i (0,a_i,c_i)[x_i] modq.
```

Each `a_i,c_i` is independently uniform in `Z_q^n`; the hidden s is unknown.
To read coordinate j, compute the PUBLIC nuisance syndrome

```text
S(x)=(F_j(x) mod(q/3), all F_l(x) modq for l!=j).
H=|syndrome group|=q^n/3=3D.
```

Known controlled constant modular additions implement this reversible
evaluation. Measure ONLY the syndrome y, not x. Its probability is `C_y/D`,
where `C_y=|{x:S(x)=y}|`. Keep the original word register while a solver runs
in separate workspace. The solver sees only the nuisance-group labels and y:
all non-target components remain full-root, but the target's top frequency
trits are removed. It has no secret, retained-word input, or unknown-state
inverse. The implemented frozen solver view is deeply immutable.

The constant-addition arithmetic tape is provided and reversibly replayed.
Elementary modular-add and qubit-native gate decomposition/error accounting
remain obligations, not an executed quantum hardware implementation.

## Pair Instrument And Actual Guess

If R returns two verified DISTINCT u,v in the measured fiber, project the
retained word state onto their span. Never measure which endpoint survived.
The conditional projection probability is `2/C_y`; the implementation does
not need C_y. Solver failures, empty/singleton fibers, duplicate/invalid answers,
timeouts and projection failures are charged.

For a valid pair, all non-target frequency differences vanish modq and

```text
F_j(v)-F_j(u) = (q/3)*delta modq, delta in F3.
```

After selecting the pair using ONLY the stripped input, compute delta from the
full public labels. Reject delta0 as uninformative. Do not silently select a
new high-dependent pair under the same source theorem.

Local ADD gates first map u to zero. A pivot SCALE and controlled SUMs then
map v to a single digit1 at the pivot. This permutation is reversible on the
WHOLE original word basis. On the accepted pair every other wire is zero and
the pivot is

```text
(|0> + omega^(delta*s_j)|1> + 0*|2>) / sqrt(2).
```

Inverse F3 and computational measurement give `P(y=delta*s_j)=2/3` and
`P(other y)=1/6`. Guess `delta^(-1)*y mod3`. Uniformly guess on EVERY rejected
branch. Thus with informative acceptance p, raw success is `1/3+p/3` for every
fixed secret. This is a real measurement, unlike a known-secret purity plot.
No matched copies, cloning, fiber rank/unrank, unknown inverse, amplitude
amplification about an unknown state, or erased endpoint tags are needed.

The exceptional boundary cases n*r<=2 use M=1 instead of the underfull
formula. Their groups have at most three elements, so the ordinary reference
finder has CONSTANT cost. The generalized informative acceptance is
`(4H/(3D))*beta`, not4*beta. Entire native source censuses give raw success
13/27 at(n,r)=(1,1) and109/243 at(1,2),(2,1). Thus no unimplemented small-root
case is hidden in the conditional full-secret bootstrap.

## Exact Transfer To Ordinary Uniform-Target Arithmetic

Let `tau(labels,y)` be verified distinct-pair probability of the stripped solver
including failures and its own randomness. Set beta to its mean under IID
nuisance labels and an INDEPENDENT UNIFORM target y, including empty targets.
The physical syndrome is size-biased; never identify those distributions.

Before rejecting delta0, source-average pair projection acceptance is

```text
E_labels sum_y (C_y/D)*tau(labels,y)*(2/C_y)
  = (2H/D)*beta = 6*beta.
```

Conditional on the entire stripped input, chosen pair, and solver transcript,
target-component high frequency trits are still IID uniform. Distinct native
words give a frequency-difference coefficient with a unit entry, so delta is
uniform F3. Other full frequency components do not reveal these independent
target lifts. Informative acceptance is therefore EXACTLY `4*beta`, and raw
least-trit success is `1/3+4*beta/3`, averaged over source labels for EACH fixed
unknown secret. There is no per-label acceptance or average-secret shortcut.

For arbitrary external solvers, the stripped-input policy must be independently
certified; accepting a pair does not prove a caller avoided hidden high-label
selection. The built-in reference consumes only `LowProblem`.

## Constant Two-Element Mass And The Missing Primitive

Fix a native source word x. For any other u, the syndrome-collision event has
probability1/H. For DISTINCT u,v other than x, two simplex difference rows have
an integer two-column determinant+/-1. This follows either from three distinct
digits at one site, or from a site where supports/digits first differ. Hence
the two collision events are independent over the ENTIRE nuisance product
group, despite non-prime component moduli.

If K is the number of neighbors of x in its syndrome fiber,

```text
E K=(D-1)/H; E K(K-1)=(D-1)(D-2)/H^2.
1[K=1] >= K-K(K-1).
```

The natural Born-weighted mass of exactly two-word fibers is at least
`2/9-2/H^2`, at least `16/81` when H>=9. An ordinary pair solver with pointwise
success at least xi on every target with two witnesses therefore has

```text
beta >= xi*(2/9-2/H^2)/6;
raw least-trit advantage >= (2*xi/9)*(2/9-2/H^2).
```

This is CONDITIONAL. A pointwise polynomial-time finder is NOT supplied.
One may instead prove nonnegligible beta directly for this exact uniform-target
distribution; that does not automatically follow from single-witness coverage.
A singleton-only finder has complete one-witness success on its accepted
targets and ZERO pair success. Native exhaustive source controls demonstrate it.

A worst-case single-witness solver can be used in a first-differing-coordinate
self-reduction: find u, then test each of two alternative digits at each of M
prefix positions, fixing earlier digits. This uses at most `2M+1` calls and
changes the target/remaining-variable distribution. Pointwise guarantees and
fresh solver randomness suffice; original average-case guarantees do NOT
automatically transfer to those subinstances.

## Runtime And Classical Baseline

The physical average solver time is `3*E_uniform[C_y*T]`, not the unweighted
uniform-target mean. If the latter is bounded by A and beta>=b>0, cap every
run at `2A/b`. Markov loses at most b/2 uniform coverage, leaving informative
acceptance>=2b and raw advantage>=2b/3. Both A and b need proof, not measurements
conditioned on success. Source-register retention time and aborted calls count.

The built-in meet-in-the-middle finder stores at most TWO left words per sum;
that suffices to find a pair without counting the fiber. It enumerates
`3^floor(M/2)` left words and up to `3^ceil(M/2)` right words. Preflight budget
exhaustion returns no partial pair. All retained words and hash lookups count.
This is EXPONENTIAL in n*r and asymptotically worse than established DHSP sieve
baselines. Optimizing its constants is not the research target.

For fixed prime3, one native qutrit can be obtained by projecting two fresh
binary phase registers onto the three one-hot words, with probability3/4.
Expected binary inputs per native qutrit are8/3; forward yield is3/8.
IMPORTANT correction to an initial audit hypothesis: the older `p/2` field
was NOT a forward-yield bug. It counts native inputs per binary output in
the REVERSE two-word projection, whose success is2/p. These lossy conversions
are not mutually inverse sample-cost reciprocals. A separately named forward
yield `p/((p-1)*2^(p-1))`, actual reverse projection amplitudes, regression
coverage and independent directional cost checks now disambiguate the ledger.
For n>1, fresh vector phase access and natural-problem reduction remain
separate obligations; cyclic DHSP does not automatically supply that interface.

## Evidence And Revised Next Direction

The original q27 one-input census exhausts729 full label pairs and729 uniform
low-target instances. It gives beta25/729, informative acceptance100/729,
raw success829/2187, and exact natural two-element mass16/81. All225 selected
pair/high-lift branches split into150 informative ones. The singleton-only
finder's uniform-target coverage is64/243, but usable pair coverage is zero.

Physical controls keep ORIGINAL roots27 and81, with all nonempty syndrome
branches and uniform failure guesses. Every original q27 secret is tested;
a two-coordinate control checks cancellation of the untouched secret. An
available informative alternate pair is deliberately NOT substituted in a
high-zero rejection control. All18,060 native word triples through three
registers have exact integer unit minors. Small cases are calibration and
proof falsifiers, not an algorithmic separation or toy-oracle candidate.

The highest-impact missing capability is now an ORDINARY low-input two-witness
finder with proven nonnegligible uniform-target coverage and polynomial capped
runtime, or a genuinely different joint receiver. It need not return uniform
answers, count fibers, prepare a quantum inverse, or produce independent native
children. Attacks must respect ternary one-hot choices; replacing each register
by two unrestricted Boolean variables changes the arithmetic distribution.

The prior full-secret least-trit bootstrap remains CONDITIONAL on such a learner.
Neither this interface nor a favorable finite source fulfills that obligation.

```sh
python theorems/ternary_pair_collimation.py --write
python -m pytest -q tests/test_ternary_pair_collimation.py
node research/certificates/ternary_pair_collimation_crosscheck.js
```

Gemini/Antigravity owns routine qsearch/registry/site/full-suite integration.
No accepted candidate or speedup claim should be added.
