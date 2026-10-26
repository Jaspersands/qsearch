# Integer-Character Near-Vector Reduction

## What This Adds

The cosine task now has a concrete geometric consequence: a review-pending
quantum procedure for **absolute-distance near-vector search in a specified
family of public rational lattices**. This is not a relative approximation
algorithm for CVP, a reduction from arbitrary lattice hardness, or a
demonstrated quantum speedup.

The stronger conclusion requires a stronger input modulus. It cannot be
retroactively attached to the previous 924-bit native cosine instance.
The new report freezes a separate native modulus, labels and independently
uniform centers. No serious classical optimizer or quantum optimizer has
been run on that new instance.

The integer lattice/decoder is known from
[Ducas--Pierrot](https://doi.org/10.1007/s10623-018-0573-3).
Decoding-to-Fourier duality has a substantial prior literature, including
[Regev's reduction](https://cims.nyu.edu/~regev/papers/qcrypto.pdf) and
[Debris-Alazard, Remaud and Tillich](https://arxiv.org/abs/2106.02747).
This specific source, readout and parameter composition still needs an
independent comparison against that literature. Do not claim to have
invented quantum transference, integer lattices or rational decoding.
In particular, Regev's Section 3.2 already recovers an auxiliary register
from its reduction modulo a lattice and then Fourier-samples. That is the
same central mechanism used here. The local addition is a parameterized
prime-product source and a guarded distance calculation, not a new
quantum primitive. Its research value depends on the unresolved classical
and application questions below.

## Why The Old Score Is Insufficient

Take 50 residuals, 33 equal to zero and 17 equal to half a period.
The mean cosine is 8/25=0.32, but mean normalized squared distance is
17/200=0.085, worse than the continuous uniform value 1/12.
Thus a cosine score above 0.3 does not itself imply the desired
Euclidean improvement. This is a residual-vector counterexample, not a
claim about the quantum output distribution.

One must also not assume higher moments vanish from a first-moment
license. With primes (2,5,7), cap1 and M=729, the original first-moment
height guard holds. But the third harmonic sends the source (0,0,1)
to (0,3,1), which aliases (0,-1,0):

```
5^4*7 = 1 + 6*729.
```

Both controls are retained in the producer and tests.

## The Public Lattice

Let a_1=1 and a_i=log_2(p_i) modulo N=2*3^(k-1), as in the previous
construction. Define

```
L = { y in Z^m : a dot y = 0 mod N },
Gamma = L* = Z^m + (a/N) Z.
```

An integer basis for L has rows N*e_1 and e_i-a_i*e_1 for i>1.
A numerator basis for Gamma has rows a and N*e_i for i>1; divide it by N.
The product of the numerator basis with the transpose of the L basis is
exactly N*I. Thus these really are dual bases, with determinants
det(L)=N and det(Gamma)=1/N. This is valid for composite N and nonunit
individual labels; the distinguished a_1=1 supplies the surjection.

For target c/N and output x, center each exact residue

```
r_i = a_i*x-c_i mod N,  -N/2 <= r_i < N/2,
v_i = c_i+r_i.
```

Then v/N belongs to Gamma and

```
D(x) = ||v/N-c/N||_2^2/m = sum_i r_i^2/(m*N^2).
```

Membership, distance and acceptance are checked with integer/rational
arithmetic. Conversely a supplied numerator vector in Gamma determines
x=v_1 modN and must satisfy v_i=a_i*x modN on EVERY coordinate.
There is no floating reconstruction of a large integer assignment.

## Stronger Readout License

Set J=16 and choose M=3^k satisfying

```
M > 2*B^(2cap+J).
```

This is the old integer cross-product argument with an observable
frequency j<=J. It handles an arbitrary source word plus j*e_i, not only
the signed source alphabet. The classical public-label generation and
syndrome-only decoder remain polynomial; at fixed J, increasing the
height exponent adds O(log B) bits relative to the first-moment instance.
The native costs and actual changed modulus are recorded, not hidden.

For the conditioned signed product source with active probability t,
let Z=Pr_m[P,Q<=cap] and

```
R = Pr_(m-1)[P<=cap-1,Q<=cap],
A = Pr_(m-1)[P<=cap-1,Q<=cap-1].
```

The average coordinate cosine moments in the IDEAL output distribution are

```
mu_1 = sqrt(2t(1-t))*R/Z,
mu_2 = (t/2)*A/Z,
mu_j = 0 for 3<=j<=J.
```

For j=2, the only source transition is -1 to +1, which forces both
remaining sign counts below cap. For j>=3 no integer source transition
exists, and the stronger guard excludes modular aliases. Center phases
cancel in these licensed expectations, so the formulas hold for every c.

## Squared-Distance Bound

For a centered fractional residual u in [-1/2,1/2], its absolutely
convergent periodic Fourier series is

```
u^2 = 1/12 + (1/pi^2)*sum_(j>=1) (-1)^j cos(2*pi*j*u)/j^2.
```

Apply the licensed moment identities only through J. Bound the rest by
sum_(j>J) 1/j^2 <= 1/J, without claiming anything about those harmonics.
This gives

```
E D <= 1/12 + (-mu_1 + mu_2/4 + 1/J)/pi^2.
```

For the uniform family m>=20000, cap=floor(7m/200), t=1/20, the previous
source proof gives mu_1>601/2000 and Z>=1561/1600. Since A<=1,
mu_2<=40/1561. Using J16 and pi^2<484/49 with the NEGATIVE coefficient,
the exact rational upper bound is below 3/50=0.06.
The producer checks the rational comparison and an Arb enclosure of pi.
It does not replace the written proof with a finite test sweep.

As D is nonnegative, Markov gives

```
Pr[D <= 13/200] >= 1 - (3/50)/(13/200) = 1/13.
```

Use the previous source/QFT error budget with total variation <=1/10000.
Distance verification itself is exact, so there is no trigonometric
threshold margin. The approximate conditional success is at least
1/13-1/10000. Multiplying by the paid herald probability >1/8 gives
success >1/128 per full trial. Therefore 128*b charged trials suffice
for failure <=2^-b. The circuit is still an uncompiled, review-pending
algorithmic construction, not an executed quantum optimizer.

## Arbitrary Rational Targets

The geometric input need not already be on the c/N grid. Given a rational
target t, round each N*t_i to the nearest integer b_i and write
b_i=c_i+N*z_i with c_i canonical. The exact coordinate error satisfies
|b_i/N-t_i|<=1/(2N). Solve the grid task and add the integer vector z.
Minkowski's inequality gives the output RMS distance bound

```
sqrt(13/200) + 1/(2N).
```

For N>=100 this is at most 13/50=0.26, since
(13/50-1/200)^2>13/200. Every licensed uniform instance satisfies this
small modulus guard. Input target bit lengths and rounding are charged.

This is an absolute radius of 0.26*sqrt(m), measured in the displayed
normalization. It is NOT a factor times the optimal distance. In
particular, for a target already in Gamma, the optimum is zero and the
statement supplies no multiplicative approximation guarantee.

## Attempts To Disprove Its Significance

- The reduction supplies a conventional geometric objective but still
  only on a highly structured lattice family. General CVP/LWE hardness
  cannot be imported from the notation.
- The lattice is very dense. An absolute radius proportional to sqrt(m)
  could be much larger than the true typical closest distance. A small
  improvement over coordinate rounding is not by itself significant.
- The smooth modulus and public integer-prime representation may make
  the dual near-vector problem classically easy. LLL/BKZ with Babai or
  randomized rounding, p-adic block moves and nonlocal searches remain
  mandatory. Give them ALL the same public data and charge preprocessing.
- A coordinate-rounding control in the artifact is not a competitive
  classical baseline. Its failure cannot be cited as quantum advantage.
- The Fourier-to-lattice step may be a specialization of known quantum
  transference. Novelty is explicitly unresolved.
- The first-moment native comparator cannot be reused: J16 changes the
  modulus, all labels and centers. Matched runs must use the newly frozen
  instance, and every proposed lattice vector must pass exact membership
  and full-dimensional distance verification.
- The algebra, infinite-series tail and resource composition still need
  independent review. Small distributions test signs and constants, not
  the asymptotic theorem or classical hardness.

## Decisive Next Experiment

Run precision-safe lattice and p-adic attacks on the saved J16 native
instance, optimizing squared distance on ALL rows. Save complete x and
vector numerators and verify using witness/recover_assignment. A
polynomial classical mechanism meeting the same absolute radius would
remove the proposed advantage. Failure of a finite portfolio would not
establish hardness. An external reduction or application beyond this
family remains a separate unmet obligation.

```
python theorems/integer_character_near_vector.py
python -m pytest -q tests/test_integer_character_near_vector.py -W error::RuntimeWarning
```
