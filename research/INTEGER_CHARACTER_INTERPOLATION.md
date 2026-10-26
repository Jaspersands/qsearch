# Public Integer Character Interpolation

## Status And Reason To Test It

**A constructive public-input candidate, not an established new algorithm
or quantum speedup.** This changes the mathematical family, not merely a
pilot parameter. The cyclic group can be exponentially large in the
description parameters, while public-instance generation and bounded
signed decoding remain classical polynomial-time procedures.

The integer prime-product lattice and rational-decoding idea are known from
[Ducas and Pierrot, 2018](https://doi.org/10.1007/s10623-018-0573-3).
The score-readout/source application below is a local derivation requiring
independent proof and novelty review. It is not attributed to that paper,
nor claimed as our invention of the decoder or discrete-log primitive.

The prior finite-field MPI implementation required a polynomial-size
logarithm table and allowed full cyclic-line enumeration in polynomial
time. Here full-group enumeration is exponential in input bit length.
That removes one particular baseline, not all classical algorithms.

## Explicit Problem And Access

Let p_1,...,p_m be distinct primes other than 3, including p_1=2. Choose
M=3^k and N=2*3^(k-1), k>=2. The generator 2 has multiplicative order N
modulo M. The public instance includes the actual integer labels

```
a_i = log_2(p_i) mod N,
2^a_i = p_i mod M.
```

Given public centers c_i in Z_N, output an integer x in Z_N with large

```
S(x) = (1/m)*sum_i cos(2*pi*(a_i*x-c_i)/N).
```

Equivalently, find a multiplicative character modulo 3^k that approximately
matches specified phases on the given small primes. This is a precise
number-theoretic search task, not a black-box oracle separation.
Both solvers receive the same primes, modulus, labels and centers.
All labels can be verified classically by modular exponentiation.

The output has log(N) bits even though it is ONE cyclic coordinate.
Do not substitute dimension one for its bit complexity, or compare this
new instance to an unchanged finite-field MPI benchmark.

## Classical Generation Without An Exponential Table

Since 4=1+3, binomial expansion gives

```
4^(3^j) = 1+3^(j+1) mod 3^(j+2).
```

For a unit u, first remove its sign modulo 3 using u*2^(-epsilon), where
epsilon=0 or 1. The remainder lies in 1+3Z. Suppose its base-4 logarithm
is already known modulo 3^j, and divide away that known power.
The next ternary digit is

```
digit_j = ((remainder-1)/3^(j+1)) mod 3.
```

Remove 4^(digit_j*3^j) and continue. After k-1 digits, return epsilon
plus twice the recovered base-4 logarithm. Every returned label is checked
by exponentiation. The proof of the generator order follows from the same
valuation identity, and the implementation checks its two prime divisors.

The implementation charges m*(k-1) digit steps, shared inverse-power
construction, residual modular updates and m final exponentiations on
O(k)-bit integers. There is no Shor subroutine, hidden logarithm oracle,
or table with N entries. This is a specialized classical
Pohlig--Hellman/lifting calculation, not a new discrete-log algorithm.

## Source, Decoder And Readout

Use the same full signed box E={y in {0,+1,-1}^m: P(y)<=a,Q(y)<=b}.
For a word y let U_y be the product of primes with positive exponents and
V_y the product with negative exponents. Its syndrome is s=sum_i a_i*y_i
mod N, and

```
2^s = U_y/V_y mod M.
```

Let B=max_i p_i. Comparing two source words bounds both integer cross
products by B^(a+b). If M>2*B^(a+b), modular equality forces ordinary
integer equality. Unique factorization identifies the signed exponents.
The factor 2 is conservative and also supplies the standard symmetric
rational-reconstruction guarantee when a=b.

For a score frequency, replace y by y+e_i or y-e_i. Each cross product
against a source word is at most B^(a+b+1). Thus

```
M > 2*B^(a+b+1)
```

certifies both the source and exact mean readout. Repeated prime powers
from a magnitude-two coordinate and numerator/denominator cancellation
are included. An observable of integer l1 frequency at most j uses the
corresponding B^(a+b+j) bound.

For a=b=cap, reconstruct U/V from 2^s modulo M using the Euclidean
algorithm and the exact bound floor(sqrt((M-1)/2)). Factor numerator and
denominator by trial division over the PUBLIC prime list. Reject leftovers,
negative ratios, excessive counts, or source coordinates outside {0,+1,-1}.
No hidden error pattern or unknown factorization is supplied to decoding.
Native tests explicitly decode from s alone.

The source amplitudes are the conditioned product
sqrt(1-t),sqrt(t/2),sqrt(t/2), with the known center phases. Reversible
syndrome computation and decoding erase y; a QFT on Z_N gives x.
Finite abelian character orthogonality does not require N prime.
N>4 excludes local frequency wraparound.

If Z=Pr_m[P,Q<=cap] and R=Pr_(m-1)[P<=cap-1,Q<=cap], the exact ideal mean is

```
sqrt(2*t*(1-t))*R/Z.
```

The source can use conditional count weights and ternary unranking.
Any heralded version must pay its 1/Z cost. Full reversible compilation
and a complete finite-precision budget remain unimplemented; no quantum
optimizer execution is claimed.

Follow-up: INTEGER_CHARACTER_UNIFORM.md now supplies a review-pending
uniform polynomial resource and precision ARGUMENT, using paid local
product preparation and heralding instead of a count-weight table.
It does not supply a compiled circuit or fault-tolerant gate estimate.

## Native And Adversarial Checks

The fixed native constructor uses m=1024, cap=35 and t=1/20. It produces
a 924-bit cyclic order, with all 1024 labels stored and independently
verified. A predeclared word with 35 positive and 35 negative positions
is recovered exactly from its syndrome. A 36-positive-word control is
rejected. The exact ideal mean lower bound is above 0.30404.

This is a public-construction/decoder control, not an optimization run.
No centers or classical optimizer successes are implied by that mean.
Small m=3,4 controls exhaust source words, signed readout transitions and
the output distribution solely to verify identities.

The guard is substantive. Modulo M=27, primes(2,5,7) have labels(1,5,16).
Their cap-one source is syndrome-injective, but shifting(-1,0,0) by
another negative unit aliases(0,0,1), because 4*7=1 mod27.
Norm injectivity alone does not license a score claim.

## Attempts To Kill It

- **The known construction is not new.** Check existing quantum
  decoding/transference applications before making any novelty claim.
- **Smooth group order is not hardness.** It makes public labels easy
  and also provides p-adic, CRT and digitwise attack directions.
- **Large order alone proves nothing.** Binary/ternary digit updates
  need not enumerate the cyclic group. Full-group FFT becoming expensive
  is not a lower bound on optimization.
- **Lattice attacks remain central.** The optimizer lattice is
  a*Z+N*Z^m. Because a_1=1, it has an explicit full-rank basis with first
  row a and remaining rows N*e_i for i>1. Its determinant is N^(m-1).
  Both algorithms know this basis and the prime-product decoder.
- **Generic lattice hardness does not transfer automatically.**
  These are highly structured labels. Neither their size nor failure
  of a bounded portfolio supplies a reduction from generic CVP or LWE.
- **Do not make the problem Shor-hard by hiding labels.** The labels
  are explicit and classically generated here; hiding them would change
  verification and the access model.
- **Do not advertise prime powers as prime fields.** Z_N is a composite
  cyclic ring. Nonzero scalars need not be invertible.
- **No inherited native comparison.** The finite-field MPI portfolio
  and its fixed-state trap are not results for this new family.

## Next Decisive Experiment

Gemini should freeze a native center vector and compare p-adic digit/block
search, bounded subgroup moves, tempering and precision-safe lattice
nearest-plane/BKZ portfolios on exactly this public instance. Store full
integer x values and verify every score with exact modular residues before
floating trigonometry. Charge label generation, lattice construction,
precision and all failed starts. Never pass 924-bit labels through int64.

The main-model question is whether the publicly computable p-adic logarithm
structure supplies a polynomial-time optimizer or a useful reduction, not
whether more source-density curves can be plotted.

## Reproduction

```
python theorems/integer_character_interpolation.py
python -m pytest -q tests/test_integer_character_interpolation.py -W error::RuntimeWarning
```

The artifact is `research/phase_workbench/integer_character_interpolation.json`.
Its native mean uses exact rational interval arithmetic. Small target
amplitudes are floating numerical controls, not advantage evidence.
