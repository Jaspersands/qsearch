# Native Source And Research Priority Audit

Checked against primary literature on 2026-10-07. This is a research decision
and a local resource derivation, not a new reduction or algorithm.

## The Source Is Connected, But Not Free

[Boucher, Fouque and Shen, Proposition5](https://arxiv.org/html/2609.34996v1#S5.SS2)
already convert DCP and CCP samples while retaining the integer-embedded secret.
For p=3, two fresh binary inputs give a native qutrit with success3/4; the
reverse projection succeeds2/3. Sections3-4 provide native phase states and
a sieve with time/sample bound2^O_p(log n log q) for fixed p. Their Section6.2
explicitly warns that the sample supply from standard LWE reductions does not
meet the sieve's needs. Thus the sample model is relevant, but this does not
establish an LWE attack.

The repo already implements the coordinate bijection and one-hot phase-space
conversion in `theorems/cyclotomic_fiber_receiver.py`. Do not describe the
native source as wholly disconnected from DCP. Conversely, do not describe
fresh samples as a reusable preparation unitary or its inverse. Integer
embedding, approximate-input errors and available source counts remain binding.

[Imran and Ivanyos](https://arxiv.org/abs/2304.08376) treat bounded nilpotency
class with bounded prime factors. The CCP paper explains why growing class
and its sample-only access prevent simply importing that exact algorithm.

Access correction, checked 2026-10-08: their non-exact Proposition3 does NOT
call the source-creation inverse. The bounded-class/class-dependent resource
issue remains. The [native orbit-source audit](NATIVE_ORBIT_SOURCE_ACCESS.md)
also supplies ordinary coset-state copies by a known relative unitary and its
inverse; that inverse returns the original unknown seed, not a known blank.
Whole-irrep filters commute with the available orbit-subspace reflection.
Keep the exact stronger oracle, non-exact source-copy route and growing-class
cost as separate questions, not one blanket access rejection.

## Compare Resource Profiles, Not Just Receiver Existence

Our full-label edge construction uses M=nr-2 native inputs and exponential
time O(3^(nr/2)*poly(n,r)), with polynomial workspace. At q=poly(n) with
growing n, its runtime is much worse than the cited quasipolynomial sieve.
That does NOT imply Pareto domination: the sieve consumes more than polynomial
samples, whereas the edge construction uses a linear batch. For n=1, compare
against the cyclic DHSP sieves as well; never substitute log1=0 into an
asymptotic vector-sieve formula and claim constant time.

The edge construction is an access/low-copy reference, not an algorithmic
speedup. A polynomial-time, polynomial-input replacement would change both
resource axes. A slightly faster exponential enumeration would not meet the
project objective. The useful target must specify its sample budget and the
upstream reduction, not just its receiver time.

## Local Bounded-Supply Conversion Derivation

The post-Fourier one-hot converter accepts with probability3/4 independently
of the secret AND both public frequency rows: all four input-word amplitudes
have squared modulus1/4. Accepted labels remain IID full native rows. This
uses fresh inputs and charges every failure, without conditioning on labels.

To acquire M>0 qutrits, allow K=4*(M+kappa) conversion attempts, each consuming
two fresh DCP inputs. Stop after M successes. If the cap expires, return a
uniform trit rather than repeat with an uncharged source pool. Let X~Bin(K,3/4).

    delta_supply = Pr(X<M)
                 = sum_(j=0..M-1) binom(K,j)*3^j / 4^K.

Since M<=K/4, Hoeffding gives delta_supply<=exp(-K/2)<=2^-kappa.
The uncapped mean input consumption is8M/3; the cap's worst-case consumption
is2K. Those are distinct ledgers. At M=0, allocate no attempts and no inputs.
Conditioning only on acceptance statuses preserves the accepted label law.
If a receiver has ideal population advantage epsilon, the capped supply plus
chance guesses has advantage at least(1-delta_supply)*epsilon. This does not
make epsilon inverse-polynomial or implement the receiver.

For imperfect input states, use the COMPLETE capped supply-and-readout channel,
including aborts. If its joint input trace-distance error is eta, final raw
correctness differs by at most eta, by contraction. Product inputs with
individual error<=e give eta<=2K*e by telescoping. Marginal error bounds alone
do not establish this when errors are correlated. Do not claim the ideal
Bernoulli/accepted-IID law for noisy inputs; compare whole channels instead.

This bound includes neither acquisition of DCP inputs from classical data nor
their error guarantees. Those must come from the actual upstream reduction.
The formula is a local specification for integration, not an executed source
factory or a claim that one-hot projection is new.

## Revised Priority

1. Seek a polynomial-copy AND polynomial-time weak native receiver, rather
   than more information-only plots or blind basis changes. At M=nr-2 the
   newly derived blind-product gate directs attention to label-sensitive,
   adaptive or collective observables. Allowing additional polynomial copies
   is legitimate if the upstream source budget permits it.
2. Treat decoder and sample supply as separate obligations. A poly-copy
   construction may have more impact than a time-only sieve refinement when
   source supply is limited; it still needs efficient decoding and precision.
3. Compare any proposal against the published native/DCP methods under the
   SAME dimension, modulus, copy, error and workspace regime. Do not silently
   compare an unlimited-sample solver with a bounded-supply cryptographic input.
4. Delegate the bounded-supply ledger and CLI wiring to Gemini. GPT effort
   should go into a genuinely new measurement/reduction mechanism, not another
   implementation of known constant-overhead conversion.

Falsifiers: source selection depends on labels; converter success varies with
the ideal input phase; accepted rows lose their IID law; the cap's probability
or counts disagree with exact binomial replay; a supposedly applicable source
reduction supplies too few states or unbudgeted joint error. No candidate may
be promoted solely because source conversion exists.

## Receiver Priority Correction, 2026-10-08

The [noncentral-filter audit](NATIVE_NONCENTRAL_FILTER_TRADEOFF.md) rejects
label-BLIND low-rank amplification, while explicitly preserving a constant
success label-adaptive counterexample that only relocates the original seed.
Do not suppress that counterexample by averaging away the observed labels.

The [word-orbit channel audit](NATIVE_DIAGONAL_ORBIT_CHANNEL.md) then shows
that preserving synchronized readouts can be simulated by ONE real native
sample while retaining the full original IID public-label distribution.
This is a scoped channel simulation and information bound, not classical
dequantization or unrestricted impossibility. Independent per-copy actions,
seed mixing and cross-orbit observables remain legal. The constructive priority
is now to couple actual original word orbits before discarding their phases,
with an informative costed output; more synchronized orbit-register processing
does not exploit the additional copies. External proof/novelty review remains.
