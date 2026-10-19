# Constructive Classical Interval Search By Character Rounding

Status: explicit local mathematical derivation and executed classical algorithm;
independent research review pending. No novelty, quantum execution or general
OPI dequantization is claimed. This supersedes the lack of an asymptotic
classical interval bound in the earlier finite LLL calibration, within the
scope below. Do not substitute successful seeded runs for the proof.

## Scientific Question And Decision

Can the prime-field, full-support interval problem remain a credible quantum
advantage target when its RS lattice has an explicit bounded-entry basis?

Here the answer is negative in a substantial parameter regime: classical
randomized polynomial-time search works for EVERY syndrome when
`d <= (p-1)/2` and `u >= certified_radius(p) = O(sqrt(p log p))`.
This is a local derivation, not an attribution to a published theorem.
There is no reason to build an expensive quantum interval SEARCH compiler
inside that regime before this comparator is independently reviewed.

The proposed quantum mechanism had been soft RS decoding followed by a Fourier
dual reduction. Its obligations included efficient coherent decoding, paid
source preparation/failures, native affine equations and a matched classical
baseline. The construction below attacks the last obligation directly; it
does not repair the quantum decoder or dequantize its prescribed distribution.

## Input And Access Model

`p` is an odd PRIME, block length `N=p`, evaluation points `0,...,p-1`.
`H_d[j,x]=x^j mod p`, `0<=j<d`, and `1<=d<=(p-1)/2`.
Given any public syndrome `s`, find an integer vector `e` with
`H_d e=s mod p` and every `|e_x|<=u`.

Gaussian elimination gives a public particular word `y` with `H_d y=s`.
Equivalently, given any canonical public word `y`, find a polynomial `P`
of degree `<p-d` with `y_x-P(x)` in the centered interval modulo p.
Coordinate-dependent translated intervals reduce to this same formulation
by subtracting their known centers from y. The software accepts centered
intervals and a public y; it does not accept arbitrary acceptance sets.

The entire length-p input/output is explicit. Polynomial time here means
polynomial in N and log p, NOT polynomial in log p alone. This is NOT an attack
on the earlier `p=2^61-1,N=127` punctured character input. Implementation has
a declared full-field cap4096; the mathematical argument has no such cap.

## Explicit Lattice Basis

Put `h=(p-1)/2`, with Legendre character `chi(0)=0` and `chi(x)=+/-1`.
Use p integer rows:

```text
b_0(x) = 1
b_(t+1)(x) = chi(x-t),   t=0,...,p-2.
```

Euler's criterion gives `chi(x-t)=(x-t)^h mod p`. For every `j<h`,
the product `x^j*(x-t)^h` has degree at most `p-2`, so its full-field
sum is zero modulo p. The constant row also has zero moments.
Thus every row is in `Lambda_d={z in Z^p : H_d z=0 mod p}` for d<=h.
At the first excluded moment j=h, every character row has sum -1 modulo p:
the leading monomial has degree p-1. The half-rate boundary is sharp for
THIS construction and is rejected by the API.

Character autocorrelation gives

```text
sum_x chi(x-t) = 0
sum_x chi(x-t) chi(x-v) = p-1 if t=v, else -1
B B^T = diag(p, p I_(p-1) - J_(p-1)).
```

For completeness, the off-diagonal sum reduces to `sum chi(a(a-1))=-1`.
The number of `(a,b)` with `b^2=a(a-1)` is p-1: the invertible change
`(2a-1-2b)(2a-1+2b)=1` parametrizes it by a nonzero field element.
That count also equals `p+sum chi(a(a-1))`.

The displayed Gram matrix has eigenvalues p (p-1 times) and1, so
`|det B|=p^h`. H_h has rank h by Vandermonde, hence its Construction-A
lattice also has determinant p^h. These rows form an exact basis of
Lambda_h, and a full-rank sublattice of Lambda_d for d<h. A sublattice
is enough: subtracting its elements preserves every original syndrome.
The proof works for primes in BOTH residue classes modulo4.

## Exact Coordinates And Constructive Rounding

Let `beta_t=sum_x y_x chi(x-t)` for all p shifts. The inverse coordinates
`alpha B=y` are

```text
alpha_0 = sum_x y_x / p
alpha_(t+1) = (beta_t-beta_(p-1)) / p,  t=0,...,p-2.
```

To derive them, the character Gram block inverse is `(I+J)/p`, and all p
character shifts sum to zero. The coefficient of the constant row is its
orthogonal projection. The producer separately verifies `a B=p y` with
integers, where a contains these numerators; no nearest-vector oracle,
short-solution advice, numerical inverse or LLL is used.

For each numerator a_i write `a_i=p*q_i+r_i`, `0<=r_i<p`. Independently set
`z_i=q_i+Bernoulli(r_i/p)` using the exact integer coin
`rng.randrange(p)<r_i`. This also handles negative a_i correctly.
Output the centered residues of `e_raw=y-z B`.

Every attempt satisfies the original modular equations, including failed
attempts. On success the producer independently interpolates `P=y-e` from
h+1 points, verifies it at ALL p points, and retains its coefficients.
Indeed P has degree <=h, stricter than the allowed degree `<p-d`.
Failed rounds remain in the transcript, including rounded coefficients and
raw/centered norms; the target is never rerolled.

## All-Target Probability And Complexity Proof

Fix ANY public y and its exact alpha. For each column x,

```text
e_raw[x] = sum_i (alpha_i-z_i) B[i,x].
```

The summands are independent, mean zero, and each has range length at most1.
There are p summands. Hoeffding's bound and a union bound therefore give

```text
Pr[max_x |e_raw[x]| >= u+1] <= 2p exp(-2(u+1)^2/p).
```

Raw residuals are INTEGERS. Centering modulo p can only decrease their absolute
values, so the same expression bounds failure of the returned interval word.
No independence BETWEEN columns is required.

For machine-checkable rational certificates use `e>2`:

```text
E = floor(2(u+1)^2/p)
delta = min(1, 2p / 2^E).
```

The full interval u=h has failure0 trivially. Probability enclosures are
rounded UP to128-bit dyadics; tiny positive tails are never rounded to zero.
With fresh independent coins on the SAME fixed target, r failed attempts have
probability <=delta^r, and expected attempts <=1/(1-delta) if delta<1.
Seeded `random.Random` runs are reproducible controls, NOT a source of a
confidence claim or proof of ideal probabilistic independence.

Choose `E_req=ceil(log2(4p))`, and the smallest integer r with
`2*r^2>=p*E_req`; set `u=min(h,r-1)`. Then delta<=1/2.
The implementation computes this with integer bit lengths and isqrt.
Consequently every target has expected <=2 attempts and, after t attempts,
failure <=2^-t. A verified-witness repeat-until-success variant is Las Vegas
under the ideal coin premise; the shipped bounded variant reports exhaustion.

Character evaluation costs O(p log p) small modular operations. Closed-form
coordinates, streamed basis multiplication, and native moment verification
cost O(p^2) arithmetic operations on O(log p)-bit integers. Working storage
is O(p), apart from retained transcripts. Optional syndrome elimination costs
O(d^3) field operations/O(d^2) storage; independent polynomial verification is
also polynomial and is not silently free. Expected complexity is polynomial
in the EXPLICIT block length. No assumption that a random syndrome has a
planted short witness is needed: the positive probability proof gives existence.

## Executed Controls

Run `python theorems/interval_character_rounding.py --write`.
The saved report keeps all24 exact public targets from the previous LLL report,
including its previously inconclusive p127 covering certificates; all24 have
native witnesses from this new algorithm. Their smaller-width finite successes
must NOT be called all-target certificates when the tail bound is vacuous.

Nine additional controls use public ramp, spike, and seeded uniform words:

|p|d|u|one-attempt all-target failure bound|uniform-word witness norm|
|---:|---:|---:|---:|---:|
|257|128|37|257/1024|23|
|509|254|52|509/1024|29|
|1021|510|78|1021/2048|63|

All nine succeed on the first declared round, but it is the proof, not that
frequency, that licenses a uniform bound. Ramp and spike are easy controls;
they are not advertised as hard instances. A zero-width nonzero-syndrome
control keeps all3 failed attempts and correctly returns no witness.

Tests independently construct characters from nonzero squares, compute full
Gram/determinants and rational inverses, exhaust small rounding distributions,
verify unbiasedness for signed numerators, enumerate every small syndrome,
and replay saved witnesses with direct moments and Horner evaluation.

## Why This Could Fail Or Be Overinterpreted

- A wrong full-support, dual-code or exponent convention would invalidate the
  kernel. Native moments, the sharp next-moment countercontrol and independent
  polynomial replay test this; none can justify a different support.
- An invalid Gram inverse or rounding bias would invalidate the tail proof.
  Exact reconstruction, a separate matrix inverse and exhaustive coin laws
  test these independently. The tail theorem still requires independent coins.
- Finite PRNG success cannot certify an asymptotic theorem. The derivation above
  is the reason for the bound and still requires independent expert review.
- For u near sqrt(p) without a growing factor, the union bound can be vacuous.
  No hardness OR success theorem is inferred there. Smaller d may admit much
  stronger attacks; failure of THIS bound does not favor a quantum algorithm.
- It is a SEARCH algorithm, not an ideal uniform or weighted coset sampler.
  At y=0 it returns e=0 deterministically, whereas the full-interval target
  distribution has many other words. Do not claim the quantum sampling
  distribution or all of the soft-decoder reduction has been reproduced.
- An arbitrary set of allowed residues need not contain a sufficiently long
  interval, and this argument does not address it. Extension fields with an
  integer interval encoding and punctured exponential fields are excluded.
- The construction uses classical Paley/character identities and standard
  randomized rounding. Absence of a matching search hit is NOT novelty evidence.

## Executed Deterministic Derandomization

`solve_deterministic` now implements conditional expectations, not an assumed
coloring oracle. For `k=u+1`, choose the rational base `c=1+4k/p` and use
`Phi(e)=sum_x(c^e_x+c^-e_x)`. Write `alpha_i=q_i+r_i/p`, with exact floor
residual `w=y-qB`. Independently rounding each remainder defines an initial
expected potential. Replacing each coin by whichever permitted branch has
smaller conditional potential makes that expectation nonincreasing. Once all
coins are fixed, this is the ACTUAL potential of an integer residual. If the
initial value is strictly smaller than `c^k`, no coordinate can have magnitude
at least k. This supplies a deterministic, target-specific certificate.

No approximate real probabilities or numerical exponentials are needed.
For `c=a/b`, all conditional terms share the positive denominator
`D=(ab)^(2p)*p^p`. Initially the positive term for column x is

```text
a^(p+w_x) b^(p-w_x) product_i F(r_i,B[i,x])
F(r,s) = (p-r)*ab + r*ab*c^(-s),    s in {-1,0,1}.
```

Each F is an INTEGER: the last factor is a^2, ab or b^2. The negative term
reverses w and s. Fixing a bit replaces its F by `p*ab*c^(-s*bit)`, also an
integer. Exact divisions remove only the unprocessed factor. Every step checks
the weighted-branch expectation identity and monotonicity, and the final terms
are independently cross-multiplied against `D*c^(+/-e_x)`. The report saves all
floor/ceil decisions and a hash of the exact integer potential chain.

The uniform certificate is also exact. Put `t=(c-1)/(c+1)` and

```text
L = 2 sum_(j=0..7) t^(2j+1)/(2j+1)
U = L + 2*t^17 / (17*(1-t^2))
L <= log(c) <= U
M = k*L - p*U^2/8
E[Phi] / c^k <= 2p*exp(-M) <= 2p*2^(-floor M).
```

Whenever this last rational bound is <1, EVERY target is solved
deterministically. `deterministic_radius` searches from the randomized width
upward until this is certified, or reaches the trivially full interval.
For example p23 needs radius9 instead of the randomized certificate's8;
the two bounds are not silently equated. As p grows, log(c) is asymptotic to
4k/p, so the width remains O(sqrt(p log p)). This does NOT remove sqrt(log p).
It removes the need for random or PRNG coins in the implemented search.

This has larger bit complexity than randomized rounding: O(p^2) operations
on O(p log p)-bit integers and O(p^2 log p) bits of working storage. It remains
polynomial in the explicit block length; no comparison calls it free.

Eight executed controls cover seeded public words and quarter-field spikes at
p31/61/127/257. All have uniform certificates and native polynomial witnesses.
Uniform-word norms are3/6/8/11; spike norms4/5/8/12. Naive nearest-coordinate
rounding instead returns zero coefficients on y=(floor(p/4),0,...,0), leaving
norm floor(p/4): a linear-error counterexample, not a valid derandomization.
The deterministic impossible-target control is inconclusive with no witness.
Independent tests exhaust all small conditional distributions and compare
every branch choice to a separately computed rational expectation.

This is a local application of the established
[conditional-probabilities derandomization method](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1987/5986.html),
not a claim to have invented that method. The clean milestone is26 focused
tests and191 connected tests, including those26, passing in one connected
command. This is NOT full-repository coverage.

## Literature, Impact And Next Decision

[Paley1933](https://doi.org/10.1002/sapm1933121311) supplies the historical
character-matrix context, not a claim that this particular RS search attack is
new. [Hoeffding1963](https://doi.org/10.1080/01621459.1963.10500830) supplies
the bounded independent-summand inequality. Its original preprint is indexed
by the NC State repository, but direct retrieval encountered bot protection.

[Quantum advantage from soft decoders](https://arxiv.org/abs/2411.12553),
Problems6-8 and Section6.1, formulates the full-support interval search task
and compares against a Prange-style classical method. Here d is the number
of target parity checks and the polynomial dimension is p-d; keep that
distinction when comparing its rate notation. Its sufficient quantum regime
is not evidence of classical hardness. At fixed interval density rho<=1/2,
our earlier support ceiling `d/p<C<=rho` puts every certified profile within
the half-rate scope, and `u=Theta(p)` eventually exceeds our radius. Thus
THIS prime/full-support/fixed-density search window has a constructive
classical comparator. No conclusion is transferred to prescribed sampling.

[Bennett-Peikert2022](https://arxiv.org/abs/2202.07736) and
[Mook-Peikert2022](https://web.eecs.umich.edu/~cpeikert/pubs/bch-lattice-decoding.pdf)
are relevant prior art on RS/related lattice decoding. Near-lattice bounded
distance list decoding and all-target interval covering/search are different
guarantees; citing either does not automatically prove the other.

Expected research value is pruning a misleading apparent advantage rather
than finding a quantum speedup. Conditional expectation is now implemented
above, but does not remove the logarithmic factor. Published constructive
partial coloring ([Lovett-Meka2012](https://arxiv.org/abs/1203.5747), Theorem4)
is a possible stronger baseline, not software implemented in this pass.
A more structure-specific next hypothesis is to replace dense character rows
by sparse differences of multiplicative-subgroup indicators, then invert the
translation frame exactly. This could change the variance parameter itself;
rank, native moments, inverse bit complexity and parameter scope need proof.
Do not substitute another seed/width mesh or conditional oracle for that test.
