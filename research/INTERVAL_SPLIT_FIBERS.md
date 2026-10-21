# Divisor-Free Public Moment Frames From Split Fibers

Status: explicit constructive derivation and executed classical algorithm;
independent research review pending. No novelty or quantum speedup claim.
This attacks the same full-prime interval SEARCH problem, not its prescribed
sampling distribution or the earlier punctured large-field instance.

## Scientific Question

Can a bounded, near-minimum-support native moment row be constructed without
requiring its order to divide p-1 or p+1? A public short row is enough to build
the prime translation-frame attack; it must not be supplied as hidden advice.

The answer here is constructive in a RESTRICTED degree regime, and instance-
certifying outside it. It does not solve the general sparse moment problem.

Input remains prime p, explicit block length N=p, parity H_d[j,x]=x^j on all
x0..p-1, arbitrary public y or syndrome, and interval[-u,u]. Choose a power
of two ell>=d with ell<=floor(p/2). Public setup constructs two fully split
fibers of a degree-ell quadratic composition. Only AFTER setup succeeds is
its waveform used for affine rounding. No target influences setup.

## Mathematical Representation

Suppose A and B are disjoint size-ell root sets, with monic polynomials

```text
F_A(X) = product_(a in A)(X-a)
F_B(X) = product_(b in B)(X-b)
F_A-F_B = 1.
```

Newton identities imply their power sums agree for every j<ell, while the
ell-th power sums differ by -ell modulo p. Since ell<p, this is nonzero.
Thus w=1_A-1_B has integer sum0, entries0,+/-1, support2ell and native kernel
moments of exactly the required order. For ell=d, this is an ideal finite-field
equal-power-sum construction. It is NOT assumed to exist efficiently in general.

The earlier split power-map and nonsplit Dickson/trace examples are special
ways to obtain completely split fibers. This representation exposes a different
search space: PUBLIC polynomial maps and their split fibers, not circuits or
arbitrary free short-vector advice.

## Executed Public Setup

Start A={0}, B={1}, with identity polynomial F(X)=X. At each layer search b
in0..p-1 until EVERY v in A union B has v-b a NONZERO quadratic residue.
Replace each v by the two exact square roots of v-b. The new map is
`F_new(X)=F_old(X^2+b)`, so A remains the full zero fiber and B the full one
fiber. Distinct targets and nonzero roots preserve cardinality, distinctness
and disjointness. After k layers ell=2^k and the monic fiber polynomials differ
by1. The producer multiplies them and independently verifies that identity,
the native moments, support and first excluded moment.

Every candidate shift and modular character test is charged. Exact modular
square roots use the existing SymPy routine, and are checked by substitution.
If no shift works at a layer, the FULL failed scan and achieved degree are
retained. A degree8 prefix is NEVER promoted as a requested degree16 frame.
No automatic previous-layer restart or hidden target reroll occurs.

## Uniform Setup Criterion

Let v_1,...,v_M be distinct current values. Expand

```text
A_M = 2^-M sum_b product_i(1+chi(v_i-b)).
```

For b outside the M forbidden zeros this is exactly the indicator that all
differences are nonzero squares. Each forbidden point contributes at most1/2,
so the number of legal shifts is at least A_M-M/2. For a nonempty subset of
r indices, the product polynomial has r distinct roots. The multiplicative
Weil bound gives absolute character sum <=(r-1)*sqrt(p). The subset sum of
those constants, divided by2^M, is

```text
K_M = 2^-M sum_(r=1..M) binom(M,r)*(r-1)
    = M/2 - 1 + 2^-M.

N_legal >= p/2^M - K_M*sqrt(p) - M/2.
```

Use an INTEGER UPPER bound ceil(sqrt(p)) to obtain a rational LOWER bound.
If it is strictly positive, every set of M distinct values has a legal shift.
The expression decreases as M increases; since every stage has M<=ell,
positivity at ell guarantees that every greedy setup stage succeeds, independent
of its earlier choices. The software computes all constants exactly. In
particular, M1 gives the exact count (p-1)/2; the zero-value correction is not
silently dropped.

The analytic call `setup_bound(p,M)` does not allocate a field table or run
setup. It can certify the bound at a huge prime while the actual explicit
generator correctly rejects inputs beyond its declared implementation cap4096.
For p1021,M4 the rational lower bound is445/16>0. For p347,M8 the bound is
negative although the actual setup succeeds. This is a sufficient criterion,
not a necessary condition or evidence of hardness when it is inconclusive.

Asymptotically a sufficient condition is roughly
`sqrt(p) > 2^ell*ell/2`, with slack for lower-order terms. Thus powers of two
ell below about (1/2)log2(p)-O(log log p) admit a divisor-free, uniform setup
guarantee. For arbitrary d, rounding ell up to the next power of two may cost
a factor below2 in degree and shrink this guaranteed range. No claim is made
for ell polynomial in p or arbitrary growing codimension.

The character-sum theorem is standard: see
[Weil1948](https://doi.org/10.1073/pnas.34.5.204) and
[Katz1989, Theorem2](https://web.math.princeton.edu/~nmk/old/estcharsums.pdf)
in the split-etale case. The subset expansion, zero correction, composition
construction and RS application are local derivations, not claims attributed
to those papers. No novelty follows from a literature-search miss.

## From One Public Row To Every Affine Target

Only a VERIFIED completed setup is passed to the existing translation solver.
The common implementation now shares actual waveform validation, prime cyclic
Q-polynomial inversion, exact denominator coins, native residual checks and
full independent RS polynomial replay with the torus construction.

The constant row plus p-1 translates has squared column range at most2ell+1.
Prime cyclotomic irreducibility gives full real rank, even if the sublattice is
not the entire Construction-A lattice. Exact rational coordinates are COMPUTED
and reconstructed; no inverse or short-vector oracle is supplied. Consequently

```text
Pr[||e||inf>u] <= min(1,2p exp(-2(u+1)^2/(2ell+1))).
```

At the saved certified width O(sqrt(ell log p)), expected rounds are<=2 for
EVERY syndrome, under fresh independent exact coins. When setup satisfies the
uniform criterion this is a uniform constructive family algorithm. When the
criterion is inconclusive but a public frame is actually found and verified,
it is an all-target algorithm for those fixed public parameters, not a general
setup theorem. Neither conclusion follows merely from seeded success rates.

### Stronger Simple Baseline In The Low-Degree Regime

Do not always use the independent-rounding bound. Exact nearest rounding of
each rational row coordinate has error at most1/2. A column's L1 sum is
`1+sum(abs(w))-abs(w[x+1])`, accounting for the omitted translate. All current
split, nonsplit and fiber waveforms have sum(abs(w))=2ell and a zero entry.
The raw INTEGER residual therefore has norm at most
`floor((1+2ell)/2)=ell`, for EVERY target, without rounding coins.
This also holds for the multiplicity2 nonsplit fallback: L1 and squared norm
must not be confused. Centering can only improve the result.

The implementation computes and verifies this bound from the actual waveform.
It selects nearest rounding when ell is the better certified radius, otherwise
independent rounding. Prior torus comparisons ALSO take their better bound;
the older random-only radius is not used to inflate the improvement. Nearest
rounding's random tail certificate is explicitly marked COMPARISON ONLY, not
the active guarantee. An observed success below ell never shrinks its uniform
bound. Independent tests prohibit PRNG creation in nearest mode.

Thus a positive setup criterion gives a DETERMINISTIC all-target solver at
radius ell in the logarithmic-degree regime. The old dense nearest-rounding
spike failure does not contradict this: the dense frame's L1 bound is p/2,
whereas these frames have only O(ell) nonzero mass per column. This does NOT
show the smaller sufficient quantum radius (about3d/4 for uniform profiles)
is classically achievable, nor remove the public setup restriction.

Setup takes O(p*ell*log ell) elementary character checks as a conservative
bound, plus exact roots and polynomial checks. The tighter scan count sums
the current value counts, at most2ell-2, timesp; actual short-circuit counts
are recorded. Arithmetic and exact rational inverse bit costs are polynomial
in EXPLICIT p. It is not a log-p-only algorithm, nor a free reduction of a
punctured N127 input to an exponentially larger full support.

## Results And Decisive Failure Controls

Run `python theorems/interval_split_fibers.py --write`.

|p|ell=d|greedy public shifts|radius|best torus radius|public-word norm|denominator bits|
|---:|---:|---|---:|---:|---:|---:|
|347|8|6,43,232|8|11|3|180|
|1019|16|7,43,97,622|14|14|9|722|

Both ell values divide NEITHER p-1 nor p+1. Each parameter has two native
verified targets, a seeded public word and a quarter-field spike. All four
meet the known uniform-interval sufficient KV inequality. The p347 construction
uses deterministic nearest rounding and improves the best prior radius;
p1019 uses independent rounding and does not improve that radius but removes
the exact subgroup-order requirement. These are classical comparators, not
quantum runs or proof of a new complexity separation.

Additional setup-only controls are p1021,ell4 (positive uniform bound) and
p4093,ell8 (explicit success despite inconclusive bound). Greedy ell16 setup
FAILS at p347 andp4093: after the ell8 prefix it scans all347/4093 possible
last shifts and finds none. Those public setups remain unaccepted with no
affine target admitted to rounding. This does NOT prove that another earlier
prefix would fail, that no degree16 fiber pair exists, or that ISIS is hard.

Independent tests exhaust small character patterns including zero corrections,
replay every shift scan, rebuild fibers by enumerating quadratic preimages,
multiply root polynomials independently, check all moments and Horner witnesses,
and reject incomplete/zero/non-zero-sum/undercounted frames.

## A Local Optimality Cut: Do Not Keep Tuning Waveforms

The L1 limitation has a direct proof. Let w be any nonzero INTEGER zero-sum
waveform with all moments j<ell zero modulo p, ell<p. Its positive and negative
parts define disjoint multisets A and B with the same total multiplicity M.
Suppose M<ell. Their first M power sums agree, and p>M permits every division
in the Newton identities. Their monic degree-M root polynomials are therefore
identical, contradicting disjoint nonempty positive/negative multisets.
Hence M>=ell, so

```text
sum(abs(w)) >= 2ell
sum(w^2) >= sum(abs(w)) >= 2ell.
```

These unit-weight fibers attain BOTH minima. For sparse rows with a zero
coordinate, the nearest bound from the maximum column L1 sum is M, at least
ell; the Hoeffding squared-range parameter is at least2ell+1. There is no
smaller-mass waveform left to find at the same native moment order. Finite
exhaustive tests include multiplicity2 rows, independently of this proof.

This is a bound on THESE certificates and representations, not a lower bound
on the actual covering radius or classical algorithms. It does not rule out
coupled discrepancy rounding, overcomplete generators, saturated lattices,
different access models, or any quantum algorithm. Do not turn it into another
generic no-go result. Once setup works, further same-order waveform grids
cannot improve the present certificate; higher-value work must change the
rounding mechanism or leave this direction.

## Why This May Not Matter Enough

- The uniform setup theorem only reaches logarithmic degree; it does not
  remove the divisor condition at arbitrary rates. Greedy failures are real.
- Independent rounding retains sqrt(log p); nearest rounding instead gives
  radius ell. That still exceeds the sufficient quantum interval radius by
  a constant factor near ell=d. No complete dequantization follows.
- Setup scans the full field and inverse coordinates can have large rational
  denominators. These costs are acceptable only in the stated N=p model.
- A single verified sparse homogeneous row gives an affine solver because
  prime translations span the zero-mean space. FINDING such a row remains the
  real algorithmic issue; a generic supplied-row API is not a discovery.
- Equal power sums and split fibers are classical ideas. Independent review
  and prior-art scrutiny remain necessary before claiming new mathematics.

The concrete coupled-rounding follow-up is now IMPLEMENTED in
INTERVAL_LOCAL_LEMMA.md: fixing the constant and local resampling replace
log(p) by log(ell) in the sparse-frame bound, under explicit hypotheses. The
L1 optimality cut above remains valid; it never excluded coupled rounding.

Next high-value question is NOT another seed grid: can a proven covering-map
construction supply TWO split fibers at substantially larger degree with
polynomial public setup, or can a constructive discrepancy algorithm shrink
the radius enough to close the remaining interval window? If neither offers
a concrete mechanism, stop extending this comparator and compare independent
quantum source/code families with actual coherent decoders and matched inputs.
