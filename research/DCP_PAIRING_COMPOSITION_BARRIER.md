# Pair Compression Or Retained Correlated Blocks?

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty, general DHSP lower
bound, actual natural-source certificate or new central negative is claimed.

Run `python qsearch.py dcp-pairing-composition-barrier` and
`python qsearch.py dcp-correlated-phase-block`.

## Research Decision

Faster list merging does not by itself fix repeated many-input/one-qubit
compression. Under independent original visibility1-1/n, two fresh native
pair-compression levels with polynomial pool/attempt budgets already give
superpolynomially small unconditional output signal. This applies to ANY
pairing rule in the stated architecture, not just the new tree.

This is an argument to investigate retained correlated phase blocks, NOT to
abandon hidden shifts. A separate actual polynomial CX/CCX gate construction
retains such a block and its information. Useful accessible observables and
efficient decoding remain unknown. The information is not proved lost from
the original source; the one-pair output interface discards most of it.

## 1. Exact Scope

Inputs have n vector components and full phase modulus2^t, t>=5, with IID
uniform coarse labels in Z4^n. Their diagonals are flat, and original
dephasing is an INDEPENDENT product channel with visibility<=1-1/n.
No noise environment or latent error flags are available.

Every successful classical outcome identifies exactly one unordered pair of
ORIGINAL computational basis assignments x,y with A(y-x)=0 mod4, keeping
their two-dimensional phase state. This includes arbitrary efficient or
inefficient pairing/proposal programs and the existing reciprocal compiler.
The retained channel is the basis-pair ISOMETRY with its balanced phase
density, not an arbitrary postselected map on that subspace. A secret-erasing
reset is not a new phase source with greater useful visibility; informative
filter flags or nonisometric purification require their own source analysis.
It excludes coherent superpositions of many different pairs under one retained
outcome, collective purification between levels, and other output interfaces.

Parent pools use independent fresh batches. Their descended labels are IID
uniform conditional on retained visibility/coarse records, after discarding
higher parent-label transcripts and correctly visibility-matching zero
replacement. These are strict source-transfer ASSUMPTIONS, not inferred from
finite histograms or certified for the lattice reduction. Pooling based on
public tags is allowed but all raw attempts must be charged. The complete
second-level available pool, not only a favorable chosen subset, is counted.

Only final phase qubits are retained as secret-bearing outputs. Unused parent
qubits are discarded; earlier quantum/classical secret information is not
smuggled into an uncharged transcript. All retained classical records are
secret-independent. Final outputs may subsequently be measured collectively.

## 2. Short Masks Are A Native Rare Event

Fix x and a nonzero mask u of weight w. Each component of
sum_i A_i*(1-2x_i)*u_i is uniform modulo4, since some coefficient is a unit.
Thus its n components vanish with probability4^-n. With m source qubits,
the unconditional endpoint probability admitting ANY pair of weight<r is

    epsilon(n,m,r) <= sum_(w=1)^(r-1) binom(m,w)/4^n.       (1)

No independence among masks and no bound on computation time is needed.
Measuring an unordered-pair outcome on a flat diagonal gives its two original
endpoints exactly their original Born mass. Choosing a clever matching cannot
increase total accepted short-endpoint mass beyond (1).

Let ell=ceil(log2 m) and r=min(m,ceil(n/ell)). Since m>=2,

    sum_(w=1)^(r-1) binom(m,w)
      <=sum_(w=0)^(r-1) m^w <=2*m^(r-1),
    ell*(r-1)<=n-1,

so epsilon<=2^-n. This is a NATIVE MEAN, not a pointwise matrix guarantee.
The selected matrix with columns(4,0),(1,1) has a legal one-bit useful pairing
on EVERY endpoint, despite the native short union bound1/8 at n2,m2,r2.
It is a required scope counterexample, not a contradiction or candidate.

## 3. Two Levels And Paid Tag Selection

Allow at most R first-level raw attempts to supply one second-level pool.
By a union bound, chance that ANY produced parent used a mask shorter than
r1 is at most R*epsilon1. No independence between these events is needed.
On its complement every parent's public visibility is at mostv0^r1.
Tag-biased selection cannot find a missing clean parent for free.

The second pool has native uniform labels conditional on the retained tags
and coarse history. Its short-endpoint mass is at mostepsilon2. Every long
second pair uses at leastr2 parents, with product visibility at mostv0^(r1*r2).
Therefore the UNCONDITIONAL Born-weighted useful phase visibility S obeys

    S <= min(1,R*epsilon1+epsilon2+v0^(r1*r2)).             (2)

This is not a conditional visibility bound with free rare postselection.
An accepted output ensemble with probabilityp may have conditional mean
visibility up to min(1,S/p). Failures and selected clean tags must be paid.

At v0<=1-1/n, the elementary binomial inequality
(1+1/(n-1))^(n-1)>=2 gives

    v0^(r1*r2)<=2^-floor(r1*r2/(n-1)).                   (3)

For polynomial pool widths and R, r1,r2=Omega(n/log n), so (2) is
2^-Omega(n/log^2 n), independent of the pairing program's runtime.

The report uses exact integer rounding, including vacuous small-size bounds;
it does not substitute a floating exponential fit or claim finite practical
failure where the bound is1. Example profiles charge R=n^8 and Q=n^4.

## 4. Arbitrary Readout Does Not Recover Missing Signal

For each final accepted record with visibilityv, replace its phase qubit by
I/2 while leaving the same secret-independent classical record distribution.
Its trace distance from the actual qubit isv/2. On rejected records it is0.
Thus the whole one-attempt CQ output is within S/2 of a secret-independent
reference, pointwise in the secret. For Q independent final attempts, tensor
hybrids and contractivity give distance at mostQ*S/2. Any joint quantum
decoder's advantage for a uniform secret bit is at most that distance.

The exclusion of additional secret-bearing outputs is essential: retaining
unconsumed parent qubits, measuring earlier outputs and saving informative
classical records, or retaining a many-pair correlated block changes the
input to this decoder. Those are valid research directions, not covered cases.

## 5. Attempts To Break This Argument

1. Correlated faults with the SAME single-register visibility evade the product
   rule: all-register dephasing with probability1/2 gives every nonempty-pair
   visibility1/2, whereas independent noise gives1/16 at width4. Marginal
   fault rates alone cannot justify this upper bound. No general adversarial-
   noise or natural-lattice-source impossibility follows.
2. Stronger original noise quality, such asv0=1-1/n^2, removes the stated
   inverse-n conclusion. Exact-noise and clean inputs remain legitimate.
3. A true many-pair coherent filter can purify degenerate frequency sectors;
   see the prior DCP_NOISE_SECTOR_PURIFICATION.md. That source/instrument class
   is deliberately excluded. Do not extend (2) to arbitrary quantum channels.
4. Superpolynomial charged pooling can make the rare-short-parent term large.
   This is not a bound on every subexponential sieve. Known clean-input
   [Kuperberg algorithms](https://arxiv.org/abs/quant-ph/0302112) remain outside
   the noisy polynomial-budget conclusion. Its
   [low-quantum-space successor](https://arxiv.org/abs/1112.3333) also makes
   memory access an explicit tradeoff; a classical join is not its replacement.
5. The [lattice connection](https://arxiv.org/abs/cs/0304005) requires its own
   source-transfer analysis. The present stress model is NOT such a proof.
6. Retaining the correlated phase block below preserves linear information.
   Therefore this is an interface restriction, not destruction of information
   in the raw source and not a reason to stop pursuing collective measurements.

The most valuable falsifier is an actual source/instrument that violates one
specifically named premise and has a competitive end-to-end cost. Another
favorable finite matrix or a faster merge alone is not that falsifier.

## 6. Physical Retained-Block Escape

The companion module exports an actual reversible gate list for

    |x>|z> -> |x>|z+A*x mod4>,

componentwise. Each syndrome component has two wireslo,hi. Controlled add1
is CCX(x_i,lo,hi) followed byCX(x_i,lo); add2 isCX(x_i,hi); add3 is the
opposite orderCX thenCCX. No arithmetic scratch is needed. Public coefficients
choose the gate sequence, never the unknown x. The inverse reverses the list.
At most2nm gates and m+2n wires are used. The arbitrary-syndrome action is
MODULAR ADDITION, not bitwise XOR. Initial syndrome zero computes A*x mod4.

Measure the2n syndrome wires and RETAIN ALL m original phase qubits. Every
outcome is retained with its exact Born probability, with an implicit fiber
predicate. Neither a uniform fiber oracle nor a compact index/inverse is
granted by this gate construction. Source preparation is not performed by
the module, nor is hardware transpilation/execution.

For full-frequency injective A, uniform-secret averaging gives the maximally
mixed state on each measured fiber. The outcome-weighted Holevo quantity is
at least m-H(Y)-m*h2((1-v)/2), as in the prior scalar local derivation
DCP_MULTI_OUTPUT_FREQUENCY_BOUND.md. Here H(Y)<=2n. The entropy decrease under
an efficient projective measurement follows by purifying the input and using
concavity on the unchanged average reference marginal.

For m4n,t=n+8,v=1-1/n, full-map noninjectivity has probability

    <=(3^m-1)/2^(n*t) <2^(2m-n*t)=2^(-n^2).

For e=ceil(log2 n), h2(1/(2n))<=(e+3)/(2n), since
-(1-p)log2(1-p)<=p/ln2<2p. Hence on the injective event

    chi >= max(0,2n-2e-6).                               (4)

This is linear retained Holevo quantity in the SAME inverse-n noise model.
Holevo is an upper bound on accessible information, NOT a lower bound and
NOT an efficient decoding theorem. The finite controls directly simulate all
secrets, densities and outcomes, including a noninjective exception where the
injective entropy bound is explicitly UNKNOWN.

## Next Research Task

Operate on the implicit correlated block without measuring or erasing its
original Boolean address. Search for a polynomially accessible collective
observable, quotient transition or source-aware measurement that reveals
secret structure, and compare its entire outcome distribution to an explicit
classical simulation. Enumerating and diagonalizing fiber tables is a bounded
control, not an implementation. Do not replace the block by its one-qubit
marginals or claim that computing A*x into another register erases x.
