# Balanced Global Constraints Without A New Entangled Decoder

Status: constructive transfer argument pending independent review. Exact
character-count controls are implemented. No native quantum circuit, new
separation, or hard calibration family is claimed.

## Selection

The protected-MIS optimization lead now has a polynomial classical competitor.
The corpus also already contains the composite-modulus MPI extension; rebuilding
it would not advance the project. A different unresolved question is whether
two-fold code multiplication can support genuinely global constraints.

[*Quantum Algorithms for OPI Variants Beyond Locality and Classical
Decodability*, Sections 1.4 and 2.1](https://arxiv.org/html/2610.00502v1#S1.SS4)
asks about combining quantum decoding with global constraints. Its product
decoder uses independent unambiguous pair measurements and a Schur-square
linear system. We test one concrete case: require exactly half of a ternary
full-support kernel word to be +1 and half -1.

**Outcome:** this balanced case has a charged reduction to the existing
product decoder under explicit distance and precision margins. It does not
by itself justify developing an entangled decoder or claiming a new advantage.
Conversely, directly feeding a fixed-type state into the old local decoder is
incorrect. Both statements are tested below.

## Task And Promises

Let D be a k-dimensional explicit linear code in F3^m, with m even, and
`D intersect span{1} = {0}`. Given its public generator matrix, find

```
y in {-1,+1}^m,
sum_i y_i = 0 over the INTEGERS,
d.y = 0 mod 3 for all d in D.
```

Equivalently, append an all-ones row to the public constraints and ask for
a balanced full-support kernel word. If an existing matrix already has
that row in its span, first choose a complementary rowspace D by ordinary
finite-field elimination. Balance makes the dropped row redundant for the
OUTPUT task, not for arbitrary inputs to the original decoding problem.

Define

```
L = 3^k,
s2 = dim span{u coordinatewise-multiplied by v : u,v in D},
d_star <= min_(0 != d in D, a in F3) wt(d-a*1).
```

Computing s2 is polynomial linear algebra. Certifying d_star is NOT generally
efficient; it must come from an actual structural proof or an explicitly
charged census. Passing numerical parameters to the bound routine is not a
distance certificate. No oracle access or hidden code data is assumed.

## Why The Naive Decoder Fails

Write the Fourier-side signal as

```
|psi_d,h> = 1/sqrt(binomial(m,h))
            sum_(y in {+1,-1}^m, #plus=h) omega^(d.y) |y>,
omega^3=1, omega!=1.
```

Replacing d by `d+a*1` multiplies this entire state by
`omega^(a*(2h-m))`, a global phase. Thus three codewords in one constant
coset are physically indistinguishable. A decoder asked for the full
codeword has success at most 1/3 within that coset. Balanced states make
even the displayed phase equal to one.

There are no other exact aliases at an interior type: exchanging a +1 and
a -1 between any two coordinates changes their inner product by twice
the difference of the two labels. Invariance under every such exchange
forces all labels to be equal. This identifies the correct quotient, but
does not implement a decoder on it.

Furthermore, at exact balance every single-coordinate reduced state is
`I/2` on the +/- support. The local measurement that excludes the true
symbol with probability ZERO on a product signal now excludes it with
probability 1/3. Marginal uniformity does not restore the pair constraints.
The old local proof cannot simply be reused on this entangled input.

## Exact Count Bound

For the product signed set `S={+1,-1}^m`, character orthogonality gives

```
L * Pr_(y uniform S)[y in D^perp]
  = 1 + sum_(0 != d in D) (-1/2)^wt(d).
```

Consequently its deviation from 1 is at most
`e_full=(L-1)*2^(-d_star)`.

For the balanced subset T, put `p=binomial(m,m/2)/2^m`. A codeword with
symbol multiplicities `(n0,n1,n2)` contributes the coefficient of `z^(m/2)`
in

```
product_(a=0,1,2) (omega^(-a) + z*omega^a)^n_a.
```

We evaluate this coefficient exactly in Z[omega], represented by integer
pairs `(A,B)` for `A+B*omega`; no floating cancellation is used.

For a UNIFORM bound, divide each factor by two and put `z=exp(it)`.
Its magnitude is `|cos(t/2+2*pi*a/3)|`. Two unequal symbols have product
magnitude at most 3/4. A multiset of m symbols can be paired into
`min(floor(m/2), m-max(n_a))` unequal pairs. The distance-to-constants
promise therefore supplies at least `r=min(m/2,d_star)` pairs.
Fourier coefficient extraction, bounded by the maximum integrand, yields

```
|L * Pr_(y uniform S)[y in T intersect D^perp] - p|
    <= e_type = (L-1)*(3/4)^r.
```

If `p>e_type`, the intersection is nonempty and its conditional fraction
within the full-support solutions obeys

```
p_accept >= (p-e_type)/(1+e_full) =: p0 > 0.
```

This is a worst-case bound for every matrix satisfying the promises,
not an average over random matrices or a heuristic independence assumption.
Since `p=Theta(m^(-1/2))`, exponentially small e_type leaves polynomial
rejection overhead.

## A Search Algorithm Is Not Automatically A Uniform Sampler

The previous step is useful only with a distributional guarantee. Merely
finding some full-support codeword does NOT justify rejection on its type.
For example, a negation-symmetric distribution on the two constant words
has fair one-coordinate marginals but never has balanced counts.

Here is the charged conversion from a coherent product-state decoder.
Let

```
|phi_d> = X^d QFT^(-1)|S>,
|S> = uniform signed product state.
```

Assume a public uniform decoder U identifies d from this state with average
failure delta over uniform d in D. All measurements and randomness are
retained coherently. Prepare

```
1/sqrt(L) sum_d |d>|phi_d>.
```

Apply U, subtract its decoded label from the first register, then apply
U inverse. For each label d the result differs in Euclidean norm from
`|0>|phi_d>` by at most `2*sqrt(delta_d)`. Cauchy-Schwarz bounds the
uniform-superposition error by `2*sqrt(L*delta)`. The ideal sum need not
have unit norm; normalizing it costs another factor at most two.

After the final Fourier transform, character orthogonality makes that
normalized ideal state exactly uniform on `S intersect D^perp`. Thus

```
TV(actual unconditional output, uniform full-support solutions)
    <= eta = min(1, 4*sqrt(L*delta) + epsilon_circuit).
```

No failure branch is silently discarded. The factor L is essential:
average decoding success alone does not prevent coherent error accumulation.
This is a sufficient bound, not a tight characterization.

The published two-fold decoder's loose bound, specialized to F3, is
`delta <= min(1, 3^(k+s2)*2^(-dist(D)))`.
Using `dist(D)>=d_star` gives an explicit conservative eta. This invokes
the existing decoder theorem, not a new implementation of that decoder.
The argument and the application of that theorem require independent review.

## End-To-End Procedure And Cost

1. Compute the public quotient basis and Schur-square basis. Supply and
   check the relevant distance proof, not an unchecked minimum-distance
   oracle.
2. Run the coherent product-decoder conversion above, including preparation,
   both U and U inverse, Fourier operations, and precision costs.
3. Measure y. Verify all coordinates are +/-1, every public linear equation,
   and integer balance. Reject any failure.
4. Repeat from a fresh state at most
   `ceil(b/(p0-eta))` times, provided `p0>eta`.

Each trial accepts with probability at least `p0-eta`. The cap fails with
probability at most `exp(-b) <= 2^(-b)`. Costs are the FULL base sampler
cost times the cap, not just the final verifier. Choose circuit precision
so epsilon_circuit fits inside this margin. Conditional distribution errors
can grow under acceptance and are not identified with unconditional eta.

When `e_type=o(p)` and `eta=o(p)`, this is polynomial with O(sqrt(m))
expected base calls. Known amplitude amplification can improve the dependence
when the coherent base unitary and its inverse are available; that is an
existing generic technique, not a new entangled decoder or a new separation.

## Explicit Calibration, Not A Hard Instance

Use all nonzero points of F3^6, so m=728. D consists of evaluations of
linear forms at those points, with k=6. The full requested constraint
matrix appends an all-ones row.

- The explicit Schur-square matrix has rank 21.
- Each nonzero linear form takes values with counts `(242,243,243)`.
  Hence `d_star=485`, with a direct proof, not a hidden distance oracle.
- The complete balanced and full-support counts are computed as integers.
  Their exact ratio is approximately `0.0295614159482646`.
- With per-sampler circuit TV budget `2^-64`, the conservative cap is
  1,354 complete base calls for failure at most `2^-40`.
- Full matrices, exact counts, outward rational square-root bounds, and
  the resource ledger are stored in `reductions/ternary_type_transfer.json`.

This family is classically easy: `3^k=m+1`, so dynamic programming over
the syndrome states computes completion counts and samples uniformly in
polynomial time. A count coordinate also permits direct balanced sampling.
No quantum execution or classical-hardness evidence is claimed. The
calibration tests a general proof and must not be promoted into a candidate.

### Executed Coherent-Erasure Control

A separate fixed 3-label, 16-basis-state control executes preparation,
coherent label subtraction, and decoder reversal, retaining every branch.
Its dense PGM receiver is an identity-test instrument, NOT the published
scalable Schur-square decoder.

The decoder error is approximately 0.001898. The unnormalized ideal vector
has squared norm 9/8, making normalization accounting nontrivial. The final
output matches the uniform solution law to floating tolerance; its balanced
acceptance is 2/3. A decoder that always returns zero instead gives a uniform
law over all 16 signed words, TV 5/8 from the solution law and verified
balanced acceptance only 1/4. No branch is discarded to manufacture success.
Neither finite receiver supplies a native quantum implementation.

## Attempts To Break The Claim

- **Keep the constant direction:** fixed-type Gram matrices lose a factor
  of three in rank. The implemented eight-coordinate control has rank 9,
  not 27; the quotient Gram matrix has full rank 9.
- **Reuse local independent lists:** the exact two-coordinate state violates
  their zero-error property. Quotienting does not alone repair this decoder.
- **Ignore the output distribution:** fair marginals or a search guarantee
  do not imply balanced acceptance. The uniform-output proof is necessary.
- **Ignore coherent error accumulation:** dropping the factor `3^k` can
  make the worst-case transfer invalid. The ledger charges it.
- **Ignore circuit error:** a budget above the acceptance mass blocks the
  certificate; smaller errors increase the charged cap.
- **Use rare types:** an extreme type can have product mass `2^-m`;
  the O(sqrt(m)) argument does not apply. This is not a solution to the
  paper's general growing-alphabet or rare-histogram question.
- **Call a numeric bound a code certificate:** arbitrary parameters are
  marked non-admitting; only the calibration's actual algebraic family is
  certified here.

## Research Decision

Do not build a new entangled-decoder subsystem solely for central balanced
ternary counts. First compare it with this uniform-product-sampler plus
rejection baseline, with the stated code and error margins.

This does not dequantize the underlying two-fold problem. For a new
breakthrough candidate, the missing step remains a genuinely useful,
classically unresolved instance family, or a global constraint outside this
polynomial-mass regime with an end-to-end decoder. Surviving the local
independence objection is not sufficient. No claim about the general open
question, novelty, or all histogram constraints is made.

## Reproduce

```text
python theorems/ternary_type_transfer.py
python -m pytest -q tests/test_ternary_type_transfer.py \
  tests/test_ternary_decoder_filter.py tests/test_ternary_quotient_decoder.py \
  -W error::RuntimeWarning
```

The finite exhaustive checks are identity controls, not the scalable
algorithm. No central registry admission, CLI/UI wiring, old producer
rewrite, commit, push, or new agent.

Verification: 32 new tests and 67 connected tests pass (3.43s, RuntimeWarning
fatal). Python compilation, site JavaScript syntax, site checks and
`qsearch.py validate` pass; registry validation reports no issues. The full
repository test suite was not run. No jobs remain running.
