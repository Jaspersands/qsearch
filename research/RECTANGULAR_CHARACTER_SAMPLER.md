# A Classical Sampler For Rectangular Cycle-Class QCT Columns

Status: an executable application of known combinatorics to a specified
quantum output distribution. Not a new Schensted algorithm, new quantum
algorithm, general character-transform simulator, or HSP dequantization.
The application and scope should still receive independent review.

## Question And Selection

After the arithmetic-resonance and conditional-product Gibbs falsifiers,
reconsidered an independent representation-theoretic mechanism: could
character-transform readout supply a new difficult sampling primitive on
large permutation classes?

The [QCT paper, Eq. (4)](https://arxiv.org/html/2610.16827v1) defines
class-to-irrep amplitudes by the normalized character table. It also
discusses central-information limitations for HSP. Its full coherent
transform is NOT the same computational task as sampling one column.
The repository previously had polynomial involution-character scoring,
but correctly did not infer a sampler from that scoring routine.

The concrete hypothesis tested here is narrower: basis-column readout on
the public class `k^m` of `S_n`, `n=k*m`. This includes fixed-point-free
involutions (`k=2`), not just classes moving a constant number of points.

Result: its ENTIRE irrep-label distribution has an exact classical
sampler in polynomial time in n, using known quotient and Schensted
constructions. The class size being enormous does not make this sampling
task difficult.

## Prior Art, Not A New Algorithm

[Stanton and White (1985)](https://doi.org/10.1016/0097-3165(85)90088-3)
give the rim-hook Schensted correspondence and its decomposition into
k ordinary Schensted correspondences. The
[Shimozono--White account](https://fpsac-archive.github.io/FPSAC99/ARTICLES/55Shimozono.pdf)
explicitly describes the colored-permutation and empty-core quotient
interpretation. The equal-cycle character magnitude formula is also
recorded in [Swanson, Theorem 8](https://arxiv.org/html/1701.04963).
We apply these established results, rather than claim a new correspondence
or an independent discovery of its counting formulas.

## Input, Output And Full Law

Input: public positive integers k,m and the ordinary degree-n symmetric
group representation model. Output: a partition lambda of n.
The target is measurement of the irrep register immediately after the
QCT acts on the normalized class-basis state `|k^m>`.

Since the centralizer has size `z_(k^m)=k^m m!`, the output law is

```
P(lambda) = chi_lambda(k^m)^2 / (k^m m!).
```

It is zero unless lambda has empty k-core. For empty core, write its
k-quotient as `(alpha_0,...,alpha_(k-1))`, with `m_j=|alpha_j|` and
`sum_j m_j=m`. The standard character magnitude formula gives

```
|chi_lambda(k^m)| = [m! / product_j m_j!] product_j f^(alpha_j),
```

where `f^alpha` counts standard Young tableaux. Substitution yields

```
P(lambda)
 = [m! / (k^m product_j m_j!)]
   product_j [(f^(alpha_j))^2 / m_j!].
```

The first factor is the multinomial law for m independent uniform colors.
The other factors are independent Plancherel laws at the resulting sizes.
This proves normalization and provides a sampler; it is not merely a
cheap point-probability evaluator.

## Public Sampling Algorithm

1. Draw one uniform permutation of m symbols and m independent uniform
   colors in `{0,...,k-1}`.
2. Split the permutation word by its position colors. Conditional on the
   color counts, the relative orders of these subwords are independent
   uniform permutations of their respective lengths.
3. Apply ordinary row insertion to each subword and retain its shape
   alpha_j. These shapes have exactly the required Plancherel laws.
4. Assemble the k-quotient with empty core by the abacus map.

For step 4 choose `L=max_j length(alpha_j)`, pad each alpha_j to L rows,
and form beta numbers `k*(alpha_(j,i)+L-i)+j`, using one-based i.
Sort all kL beta numbers decreasingly and subtract the staircase of
length kL. Remove zero rows. The result is the unique empty-core
partition with the specified ordered quotient.

The implementation checks the inverse abacus map and total size on every
draw. It does not calculate a character, enumerate partitions, enumerate
permutations, or perform rejection over irrep labels during sampling.
Uniform integer generation may of course reject random BIT strings;
that is ordinary exact discrete random generation, not postselection of
favorable group or representation outcomes.

Naive row insertion already uses polynomial time, conservatively
`O(m^2 log(m+1) + n log(n+1))` comparisons and `O(n)` stored integers of
`O(log(n+1))` bits. No optimal RSK implementation is needed for the claim.
The comparison is polynomial in n, NOT polynomial in the bit length of a
succinct `(k,m)` descriptor. Neither do standard degree-n group QFT
implementations promise polynomial cost in log n alone.

The mathematical law assumes ideal uniform discrete randomness. A seeded
Python PRNG is used for reproducible records, not claimed to be a
certified source of independent fair bits.

## Independent Checks

- Enumerate the ACTUAL colored-permutation map for five small parameter
  pairs, including `(k,m)=(3,4)`. Every output multiplicity equals
  `chi_lambda(k^m)^2`; every source object, not a selected seed, is counted.
- Across all 50 rectangular cycle-type columns through degree 16,
  compare all 3,635 partition/column pairs with the existing independent
  Murnaghan--Nakayama recursion. Exact agreement and exact normalization.
- Check ordinary RSK against the hook-length Plancherel law, quotient
  round trips, nonempty-core zeros, and the existing involution-character
  arithmetic through degree 18.
- Disable character evaluation and all-partition enumeration during
  large-sampler tests, so a hidden table cannot satisfy the test.

The live artifact records all 64 samples for each predeclared case:

| Degree | Cycle type | Class-size bit length | 64-sample time |
|---|---|---|---|
| 4096 | `2^2048` | 21622 | 0.21548 seconds |
| 4095 | `3^1365` | 28822 | 0.10994 seconds |

Timing includes source draws, RSK, assembly, and inverse checks. It excludes
process startup and the separate first-sample point-mass certificate.
The first mass is stored exactly in hexadecimal numerator/denominator
form. These large outputs are executions of the classical sampler, not
quantum runs or evidence of a new quantum advantage.

## Attempts To Break The Scope

**HSP law is different.** For a single involution coset state, weak Fourier
sampling has probabilities `d_lambda(d_lambda+chi_lambda(h))/n!`, not
`chi_lambda(h)^2/z_h`. At degree four their total variation distance is
exactly `1/4`. The test preserves this mismatch. This sampler does not
replace the quantum front end of the existing binary carrier instruments,
nor sample their joint Kronecker labels or learn a hidden matching.

**Coherent inputs are different.** In S2 the character transform is a
Hadamard. The equal coherent superposition of its two class inputs gives
one certain output, whereas a mixture of their column samples is uniform.
The total variation discrepancy is `1/2`. Thus column simulation does not
license arbitrary input states, interference, or repeated coherent QCTs.

**Mixed cycle lengths can cancel.** Shape `(2,2)` and cycle type `(2,1,1)`
have two unsigned rim-hook paths but character zero. The positive
equal-cycle quotient formula cannot simply be applied by replacing m with
the total number of cycles. No polynomial sampler for every mixed column
is claimed here.

**An enormous state space is not the resource.** All-class or all-irrep
enumeration would be expensive; this sampler does neither. Conversely,
sampling these labels does not classically prepare the corresponding
coherent superposition or implement spectral filtering.

## Research Decision

Do not use rectangular-cycle class-state sampling, including fixed-point-
free involutions, as a new hard quantum primitive. Use this exact baseline
in any future experiment with THAT output contract.

This does not refute the character-transform paper or solve GI/HSP.
The new repository capability is the matched full-law sampler, where the
older routine supplied only character scores. No central claim admission,
CLI/UI wiring, or unrelated registry reclassification is warranted.

A successor needs a useful explicitly encoded computational task and an
operation whose interference or output law is absent from this classical
construction, with all preparation and measurement costs paid. Mixed
cycle types or a surviving coherent state are not, by themselves, such
an algorithm. Do not automatically start a mixed-type parameter campaign.

## Reproduce

```
python theorems/rectangular_character_sampler.py
python -m pytest -q tests/test_rectangular_character_sampler.py -W error::RuntimeWarning
```

Artifact: `research/classical_baselines/rectangular_character_sampler.json`.
Existing character producers and all earlier artifacts are unchanged.

Verification: 35 new/202 connected tests pass in 100.61 seconds with
RuntimeWarning fatal. Python/site syntax, site checks and registry
validation pass (`valid:true`, no issues). Full repository suite not run.
All owned jobs are terminal.
