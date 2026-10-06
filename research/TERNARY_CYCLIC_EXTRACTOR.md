# Exact Native Cyclic Extractor

LOCAL SOURCE DERIVATIONS / INDEPENDENT REVIEW PENDING. This is an implemented
source-valid primitive, not an accepted candidate, new speedup, or novelty claim.

## What Changed

The pointed-triple cover is no longer needed for this extractor. A single
curvature-only zero-sum support defines an invertible partition of EVERY source
word into three-cycles. There is no corner1 inverse, incoming-edge oracle,
unknown state preparation, cloning, or favorable-outcome postselection.

The support finder is KNOWN mathematics: the two Gaussian-elimination layers
in [Ivanyos and Santha, Proposition 9](https://arxiv.org/pdf/1503.09016),
specialized to F3. Among `(n+1)^2` vectors, each inner relation splits into two
equal-sum disjoint supports. A relation among their common vectors either gives
a zero sum directly or gives four disjoint equal-sum supports. Three of these
sum to zero in F3. At most `n+2` kernel calls suffice. This is one homogeneous
nonzero witness, not an algorithm for listing all affine pointed-cover inverses.

The new contribution here is a local exact-source derivation and implementation
of the native cyclic instrument, conditional source law, and resource gates.
Novelty has NOT been established.

## Original Source

At even level `L=2r`, the ORIGINAL modulus is `q=3^r`. Each supplied qutrit is

```text
(|0> + chi_q(a_i.s)|1> + chi_q(c_i.s)|2>) / sqrt(3).
```

For the fresh native source, `a_i,c_i` are independently uniform in `Z_q^n`.
Let `B_i=(a_i+c_i) mod3`. Conditional on all curvatures, each `a_i mod3`
remains uniform, and the higher lifts of `a_i,c_i` remain jointly uniform and
independent across sites. No secret is used to select a support.

Choose a nonempty binary mask `b` with `sum_i b_i B_i=0`. The translation
`x -> x+b mod3` has order three and no fixed points. Its orbits partition the
ENTIRE original word space. For the original frequency map `F`,

```text
F(x)+F(x+b)+F(x+2b)
 = sum_active(a_i+c_i) + 3*sum_inactive F_i(x_i) = 0 mod3.
```

Consequently, relative frequencies `A=F(x+b)-F(x)` and
`C=F(x+2b)-F(x)` obey `C=2A mod3`. This is the EXACT native odd level `L-1`
promise at the SAME modulus `q`; it is not a small-field shadow.

## Physical Instrument

Take the first active site `p` as pivot and set

```text
j=x_p; z_i=x_i-b_i*j mod3 for i != p.
```

One inverse SUM_F3 from pivot to each other active site implements this
coordinate change. Its inverse is explicit: `x_i=z_i+b_i*j mod3`.
Measure only the active complements. The pivot is the output qutrit;
inactive originals are untouched. ALL outcomes are retained. Each branch has
probability `3^(1-t)` for support size `t`, independent of the secret and labels.
Total acceptance is exactly one. No endpoint tags need erasure.

In a branch, the output has the original anchor phase
`chi_q(F(anchor).s)` multiplying it. That scalar may be ignored after measuring
the pointer, but it is NOT globally constant across a coherent pointer. If
the pointer is retained, its phases are part of the joint unknown state.

## Exact Source Law And Recycling

Fix all curvatures, the curvature-only selected support, and all active pointer
outcomes. The pivot is at digit zero in the anchor. Its first relative
frequency contains `a_p` with coefficient one, its second contains `c_p` with
coefficient one; other sites supply fixed offsets. Varying its conditional
tangent and two high lifts gives EVERY allowed odd pair exactly once.
This proves the uniform native odd chart INCLUDING zero tangent, without
primitive-only conditioning, approximate invariance, or rejection bias.

It is a distributional theorem over the supplied source labels. Conditional
on the FULL parent label transcript, output labels are deterministic. Do not
promise fresh-child IID inputs to a learner that also receives that transcript.
The low-level `cyclic_output` verifies the odd pair constraint but cannot
certify an external caller's curvature-only mask selection policy.

Repeated support selection uses only surviving public curvatures and consumes
only active registers. Untouched quantum originals remain live. Conditional
on all initial curvatures, disjoint child pivots have independent uniform
tangent/high data, hence the extracted odd children are jointly IID native.
The retained EVEN curvature law itself is generally NOT fresh IID. It must
not be advertised as such. Its conditional tangent/high independence is enough
for the next support extraction.

## The Serious Remaining Failure

Perfect acceptance does NOT make root depth polynomial. A one-output
odd-to-lower-even `first_kernel_line` consumes `n+1` odd inputs. If even-to-odd
supports are disjoint and each creates at most one child, any such chain needs
at least `(n+1)^(r-1)` original qutrits for one final field qutrit, even allowing
all inactive recycling. A straight fresh-batch realization consumes
`(n+1)^(3*(r-1))`. These are protocol-specific statements, NOT general quantum
lower bounds. Multi-output or retained-coherent-pointer transducers are
outside this lower-bound scope. Final incidence decoding and full-secret
bootstrapping cost additional inputs.

The new `n=4,L=16,M=100` control extracts 13 odd children; the worst-case
guarantee is four. This single instance is not an asymptotic yield guarantee.
Both depth ledgers are still exponential even at fixed `n=1`.

The primary paper's field algorithms do not automatically solve the original
higher-root native problem: its field source, polynomial degree, access model,
and reduction assumptions must be supplied, not inferred from this specialization.

## Verification And Falsifiers

- 25 focused tests cover scaled support dimensions through n32, all 81 n1
  curvature configurations, every cyclic basis word, arbitrary complex inputs,
  all physical full-root branches, 145 pointer strata / 3,915 exact q9 pairs,
  and the 729 joint-pair law of two disjoint children.
- Independent JavaScript uses separate GF3 elimination and original-root
  normalization/basis replay: 70 kernel certificates, six full-root branches,
  all 145 conditional pointer strata, and all recycled original IDs.
- Reject the source law if support selection reads tangents/high labels or the
  secret, if low-zero pairs are removed, or if any branch is discarded.
- Reject any coherent compiler that drops anchor phases or claims child IID
  conditional on full parent labels.
- Reject a full-depth speedup claim based only on acceptance or local runtime.
- Natural-problem source acquisition and qutrit-to-qubit hardware compilation
  with aggregate error remain separate obligations, not free capabilities.

```sh
python theorems/ternary_cyclic_extractor.py --write
python -m pytest -q tests/test_ternary_cyclic_extractor.py
node research/certificates/ternary_cyclic_extractor_crosscheck.js
```

## Next Research Decision

Stop spending theory effort on improving single-output pointed covers or
acceptance. Develop a costed coherent multi-output phase representation that
keeps unknown anchor phases and mixed terms. Determine how many useful logical
directions survive simultaneous curvature constraints, and whether subsequent
root lowering actually preserves information without multiplicative input loss.
An exact density/state law and end-to-end resource recurrence are mandatory.

Gemini/Antigravity owns routine CLI, registry, site and full production-suite
wiring. This pass changes no accepted-candidate registry and claims no speedup.
