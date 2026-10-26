# Simultaneous Prime-Character Alignment From A Sine-Box Source

Status: constructive quantum algorithm argument, pending independent
mathematical and novelty review. Implemented classical arithmetic,
bounded whole-law Fourier controls, and a matched classical attack.
No scalable quantum circuit execution, classical hardness, or speedup
claim.

## What Is Different

The earlier uniform algorithm guaranteed a constant AVERAGE cosine on
a signed-trit source with a count herald. This variant instead targets
EVERY coordinate to a requested inverse-polynomial phase tolerance.
It uses a product sine source on a full box of integer exponents and
needs no source postselection.

This changes the modulus and input family. It is not a better score on
the old saved benchmark. Increasing the modulus also helps classical
algorithms, so a stronger quantum output guarantee is not evidence of
advantage.

The discrete-logarithm lattice and rational decoder are established
[Ducas--Pierrot constructions](https://doi.org/10.1007/s10623-018-0573-3).
Decoder erasure followed by Fourier readout is the established
[DQI/reduction paradigm](https://arxiv.org/abs/2408.08292).
This application is not presumed novel merely because the repository
did not previously implement its larger alphabet.

## Proposed Uniform Statement

Let `p_1,...,p_m` be distinct public primes different from 3, `B=max p_i`,
and let `0<epsilon<1/2` be rational. Choose

```
w = ceil(sqrt(m)/epsilon)
P = (product_i p_i)^w
M = 3^k > 2 P^2 B,       k >= 2
N = 2*3^(k-1)
a_i = log_2(p_i) mod N.
```

The logarithms are public and classically computable by ternary lifting.
For EVERY public center vector `c in Z_N^m`, the proposed bounded-error
quantum procedure outputs x such that

```
max_i dist((a_i*x-c_i)/N, Z) <= epsilon.
```

One approximate full trial succeeds with probability greater than
`13/16`. Verify the output with exact integer arithmetic. With b fresh
trials the failure probability is at most `(3/16)^b < 2^-b`.

The cost is polynomial in `m, 1/epsilon, log B, b` and the public
description length. It is NOT polynomial in `log(1/epsilon)` under
a succinct input convention. Inverse-polynomial epsilon gives polynomial
cost; exponentially small epsilon does not.

## Source And Actual Decoder

For integer `-w <= y <= w`, define

```
g_w(y) = sin(pi*(y+w+1)/(2w+2)) / sqrt(w+1).
```

Prepare the product of local states

```
sum_(y=-w)^w g_w(y) exp(-2*pi*i*c_i*y/N) |y>.
```

The vector g_w has norm one and is the positive top eigenvector of
the length-`2w+1` path adjacency matrix divided by two. Hence

```
sum_(y=-w)^(w-1) g_w(y) g_w(y+1) = cos(pi/(2w+2)).
```

Each local state has only `2w+1` explicitly computable amplitudes.
Known [uniformly controlled rotation constructions](https://arxiv.org/abs/quant-ph/0407010)
prepare it with O(w) rotation/CNOT blocks after padding to a binary
register. This is a polynomial-size table PER COORDINATE, not a table of
all `(2w+1)^m` words or all N syndromes. Charge table computation and
finite-precision rotation synthesis.

Coherently compute `s=sum_i a_i y_i mod N`. For any box word,

```
2^s = U/V mod M,
U = product_(y_i>0) p_i^y_i <= P,
V = product_(y_i<0) p_i^(-y_i) <= P.
```

The rational fraction is reduced by unique prime factorization.
Since `M>2P^2`, bounded rational reconstruction recovers U/V from
the SYNDROME ALONE. Divide numerator and denominator by the public
primes, recovering all exponents, and reject a remaining factor or an
exponent outside the box. No arbitrary integer-factorization oracle is
used. This decoder accepts exponents beyond +/-1; the old signed-trit
decoder must not be silently reused.

Two box words with the same syndrome have cross-product difference
smaller than M, so they give the same rational number and the same word.
Reversibly evaluate the total decoder function, XOR its fixed-width
word encoding into the original word register, and uncompute workspace.
Define an arbitrary fixed default on invalid syndromes. The ideal word
register is erased; no measurement of the individual exponents is made.

The tests also retain the failure control: tracing out the un-erased word
instead leaves a mixture of syndrome basis states, whose Fourier output
is uniform and has zero coordinate cosine bias.

## Whole-Law Readout Identity

Apply the cyclic Fourier transform to the erased syndrome register.
The ideal output law is

```
Pr[x] = (1/N) |
  sum_(y in [-w,w]^m) product_i g_w(y_i)
           exp(2*pi*i*sum_i(a_i*x-c_i)*y_i/N)
|^2.
```

It is normalized because the source is normalized and the syndrome
map is injective. The sum factorizes as a product of local trigonometric
polynomials, but the coordinate phases of a common output x are NOT
independent.

For its first moment at coordinate i, character orthogonality restricts
to congruences between two box words differing in syndrome by `a_i`.
The corresponding cross-product terms are bounded by `P^2 p_i <= P^2 B`.
The stronger guard `M>2P^2 B` makes every such modular relation an
ordinary prime-factor equality. Only the actual neighbor
`y' = y+e_i` contributes. The center phases cancel. Therefore, for all c,

```
E cos(2*pi*(a_i*x-c_i)/N) = cos(pi/(2w+2)).
```

This argument licenses only the required norm and first moments.
It does not assume independence or license every higher Fourier moment.
The bounded controls compare the entire FFT distribution with the
independent product-amplitude formula, not just one aggregate score.

## From Mean Cosine To Simultaneous Accuracy

Let `d_i=dist((a_i*x-c_i)/N,Z) in [0,1/2]`.
Concavity of sine on `[0,pi/2]` gives `sin(pi*d_i)>=2*d_i`, hence

```
8 d_i^2 <= 1-cos(2*pi*d_i).
```

Also `1-cos u <= u^2/2`. Summing expectations yields

```
E sum_i d_i^2
 <= m*pi^2/[64*(w+1)^2]
 < 5m/[32*(w+1)^2].
```

If any coordinate violates epsilon, the sum of squares exceeds
epsilon squared. Markov's inequality and the width definition imply

```
Pr[max_i d_i > epsilon]
 < 5m/[32*(w+1)^2*epsilon^2] < 5/32.
```

No coordinate independence, fitted distribution, or numerical
concentration assumption enters this proof. The ideal success is
therefore greater than `27/32`.

## Paid Precision And Bit Complexity

Allocate source-unitary operator error at most `1/64` and complete QFT
operator error at most `1/64`. Exact logical arithmetic and unitary
contractivity then give output TV at most `1/32`, leaving success
greater than `13/16`. There is no herald normalization penalty.
Invalid binary encodings in an approximate implementation are rejected
at readout and included in this TV budget, not renormalized away.

The score verifier uses signed modular residues and the exact rational
epsilon. It requires no trigonometric approximation and accepts precisely
when every `|residue_i|/N <= epsilon`.

Let `L=bit_length(M)`. Minimal k gives
`L=O(w sum_i log p_i + log B)=O(m^(3/2) log B/epsilon)`.
The explicit label table has O(mL) bits.

- Classical label construction/verification is polynomial in m,L; the
  current shared lifting implementation stores O(L^2) bits of powers.
- Product preparation has O(mw) constant-dimensional blocks plus
  synthesis overhead and certified finite-precision classical angle
  computation.
- Syndrome arithmetic costs O(m L log(w+1)) bit gates using controlled
  constant additions and a fixed offset for signed encodings.
- Modular exponentiation, Euclidean reconstruction and public-prime
  division cost O(L^3+(m+L)L^2) with conservative schoolbook arithmetic.
  Saved-history reversible simulation has polynomial space and gate cost.
- The existing CRT/radix-three Fourier decomposition has O(L^2)
  constant-dimensional blocks, with finite-precision synthesis charged.
- Repeat the FULL trial b times; exact verification and failed attempts
  are charged. No concrete fault-tolerant T/qubit estimate is claimed.

These are logical complexity bounds, not an executable large circuit.
The explicit parameterization also imposes much larger arithmetic
registers than the earlier constant-average-cosine example.

For the first 20,000 primes other than 3 and epsilon=1/10, w=1415,
B=224743 and the prime product has 323536 bits. Elementary integer
bounds put L between 915604051 and 915606901 bits. A fixed-width
20,000-label table alone exceeds 18.3 trillion bits (2.28 decimal TB).
The current lifting cache's quadratic bit storage is much worse.
This is a description-size calculation, NOT a constructed instance or
quantum run. The theorem does not require m>=20000; this example exposes
the cost of the large-dimension budget previously used by this track.

## Matched Classical Falsifier And Verification

The saved native instance uses all 32 primes, epsilon=1/4, w=23, and an
8014-bit modulus. Public construction and label verification took
126.50 seconds. Twelve syndrome-only decodes, including both extreme
box corners, took 15.53 seconds and recovered every exponent exactly.
No native quantum state or output sample was produced.

For the SAME public labels and centers, one full-dimensional LLL basis
and one exact Babai call find a witness with maximum normalized error
approximately 2.86945e-76. LLL took 3.68 seconds; the exact certificate
and rounding took 0.60 seconds, in addition to public preprocessing.
The saved basis also certifies, via one quarter of the exact normalized
Gram--Schmidt trace, squared Euclidean covering radius at most
1.00975e-28. This is smaller than epsilon squared, so the classical
method meets the max-coordinate requirement for EVERY center vector
at this instance, not merely for the saved random target.

That certificate decisively removes this finite instance as evidence
of quantum advantage. It does not establish an asymptotic polynomial
classical algorithm, nor refute the constructive quantum argument.
Changing the modulus has made the classical problem strikingly easy.

Thirty focused tests and 167 connected tests pass. Controls include
actual syndrome-only decoding, the full output law rather than just
its first moment, the failure when the word register is not erased,
exact acceptance boundaries, and replay of the full saved classical
basis and all-target certificate. These checks do not replace
independent proof or novelty review. The full repository suite was
not run for this scoped pass.

## Falsifiers And Remaining Debt

### Prior-Art And Reduction Audit

[Regev, Lemma 3.14 and its proof](https://cims.nyu.edu/~regev/papers/qcrypto.pdf)
already uses bounded-distance decoding to erase a register before a
Fourier transform and thereby sample a dual lattice. Its statement is
Gaussian, not this exact finite sine-box contract. Consequently the
generic mechanism is established, while this search does not settle
whether the precise parameterized application has appeared before.
[DQI, Section 7](https://arxiv.org/html/2408.08292v3#S7) explicitly places
decoder/Fourier methods in that lineage. Changing the source envelope
does not by itself create a new algorithmic paradigm.

The arithmetic task has an exact geometric interpretation. Put

```
Lambda = {y in Z^m : a.y = 0 mod N}
Gamma = Z^m + (a/N) Z = Lambda^*
t = c/N.
```

An accepted output x specifies a lattice point
`z+a*x/N` within epsilon of t in every coordinate, after choosing the
nearest coordinatewise integers z. Conversely any such Gamma point
specifies an accepted x modulo N. This is an absolute-radius close-vector
search on one explicit family, not a multiplicative approximation to
the closest distance on arbitrary lattices. The public prime decoder
is a decoder for Lambda, whereas the search output is in its DUAL.
These are different computational tasks; an easy decoder does not
alone give an easy dual search, and a successful dual search does not
solve arbitrary lattice decoding.

For the shipped supports containing prime 2, a_1=1, so the finite
quotient Z^m/Lambda has order N. The syndrome register is precisely
this quotient, and its Fourier labels parameterize Gamma/Z^m. Without
prime 2 the image can be a proper subgroup; the implementation's QFT
on Z_N retains repeated output representatives. The norm and first
moment argument does not require a_1=1.

The exact kernel/dual interpretation explains what an external reduction
must supply: map an independently meaningful input to these SPECIFIC
prime-log labels and allowed modulus, transfer its solutions back, and
charge description length and precision. A reduction to a generic
rank-one modular lattice is not enough. Neither the saved code nor the
sources reviewed here supply this missing map. No generic CVP, LWE or
cryptographic consequence should be attached to this construction.

### Failure Conditions

1. A wrong neighbor relation or failed syndrome-only erasure invalidates
   the theorem. Exhaustive small-word controls and full-law comparisons
   are regressions, not a formal proof for every m.
2. A state-preparation or Fourier compiler exceeding the stated operator
   errors invalidates its implementation. No native compiler is supplied.
3. The enlarged modulus can make simultaneous alignment classically easy.
   A matched LLL/Babai attack is included; finite failures would not
   establish hardness, and finite successes do not disprove this quantum
   existence theorem.
4. Known quantum decoding/transference results may already subsume this
   parameterized statement. The literature search did not establish
   novelty. The lattice and the generic quantum mechanism are prior art.
5. A useful reduction from an independently motivated computational task
   is still absent. This is an explicit arithmetic relation, not a
   generic CVP, LWE, factoring, ECDSA, or hidden-shift solver.

The correct next gate is independent proof/novelty review and an
asymptotically meaningful matched classical construction, or a useful
external reduction. Do not run a width/tolerance sweep or compare a new
modulus to the old saved task as though the input had stayed fixed.

## Reproduce

```
python theorems/integer_character_sine_box.py
python -m pytest -q tests/test_integer_character_sine_box.py -W error::RuntimeWarning
```

The report is `research/phase_workbench/integer_character_sine_box.json`.
Earlier producers and artifacts are unchanged. No central claim
admission, CLI/UI wiring, commit, or push is part of this pass.
