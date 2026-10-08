# Nonlinear Three-Cycle Compiler: Avoid Global Fiber Ranking

LOCAL DERIVATION / REVIEW PENDING. Conditional construction, not a supplied
efficient nonlinear extractor, novelty claim or speedup. This revises the
batch target after the lexicographic counting and affine coverage audits.

## Sufficient Object

For a fixed public LOW-frequency matrix modulo H=3^d, seek a permutation
tau of the original M-trit words with

    tau^3(x)=x, F(tau(x)) mod H=F(x) mod H.

Every orbit is a fixed point or a three-cycle. Require a CLEAN COHERENT
EVALUATOR for tau of cost C, with its arithmetic scratch erased, and a proof
that the fraction alpha of nonfixed original words is at least1/poly(n,r).
The evaluator must include clean controlled forms, or an explicit circuit
from which they can be constructed and costed. Controlling an arbitrary
unknown unitary is NOT silently granted. These are real missing requirements,
not free black-box access. Labels and
the entire tau policy must depend only on LOW rows to preserve the independent
high-lift law. Full-label-dependent policies need a different output-law proof.

This object differs from finding one zero-sum witness, one equal pair, or
a pointwise successor that lacks a global order-three identity. It is also
not the existing curvature-only even-to-odd extractor: here the WHOLE native
frequency prefix is constant on each accepted orbit, giving root q/H.

## Clean Compilation With An Uncompressed Tag

Compute y=tau(x), z=tau^2(x). The canonical representative u is the
lexicographically smallest of x,y,z, obtainable with comparisons of THREE
words, not by counting all words in a fiber. If u=tau^m(x), set t=-m mod3.
For fixed points set u=x,t=0 and failure; otherwise flag success.

Coherently compute and copy u,t,flag, then reverse all scratch used to find
them. Reconstruct x=tau^t(u) into temporary clean workspace, subtract it from
the original x register, and reverse that reconstruction's scratch. The
original word register is now ALL ZERO. Only |u>|t>|flag> remains.

The forward map is injective because (u,t) reconstructs x. A computational-
basis permutation with workspace and coherent evaluations implements the
isometry; it must not attach uncontrolled relative phases. The tag has M
trits, not M-1. Its one-extra-trit redundancy is harmless and avoids the
unnecessary demand for an efficiently compressed global fiber rank. Cost is
O(C+M) using a constant number of evaluator calls; including the finite audit's
tau^3 identity check, at most10 compute/uncompute calls suffice. This is a
conditional reversible circuit recipe, NOT a hardware gate synthesis.

Measure success and then u. Each successful tag has raw Born mass3/3^M,
independently of the secret, high labels and choice of representative. Its
remaining qutrit has rows

    ((F(tau(u))-F(u)) mod q)/H,
    ((F(tau^2(u))-F(u)) mod q)/H

at root q/H, up to the common phase. The three distinct original words have
a pointed unit minor, so LOW-only orbits give the same conditional IID child
pair law as the complete batch audit. Success is alpha=nonfixed_count/3^M.
One successful batch gives ONE child; source cost is M/alpha in expectation
when batches and source laws are independently refreshed. A fixed source
instance with alpha=0 cannot be repaired by that expectation.

## Why This Is A Better Target, Not A Solved Algorithm

The high-upside target is d=r-1 with q=poly(n), costed polynomial evaluation
AND polynomial original source supply. A shallow successful transform alone
is not a breakthrough: the EXISTING even-to-odd plus kernel-line sieve already
lowers one root with acceptance1 and polynomial overhead. Its straight fresh-
batch supply is (n+1)^(3*(r-1)) for a field-root child; its scoped disjoint
one-output protocol lower bound is (n+1)^(r-1), even with inactive recycling.
Neither is a generic quantum lower bound. The new report explicitly compares
these ledgers with the conditional batch target n*(q/3-1)+1. A successful
full-depth polynomial action would have to avoid that recursive fan-in, not
rediscover the shallow baseline. See [the implemented sieve](TERNARY_CYCLIC_EXTRACTOR.md).

The [shallow invariant-kernel cycle](TERNARY_SHALLOW_KERNEL_CYCLE.md) now
implements this known step as an explicit polynomial word-dependent action.
It has acceptance1, including actual nonconstant direction controls; this
is not excluded by a polynomial explicit-menu gate. That same audit proves
that merely keeping H0-only triples and filtering them at H0*J has exact
mean survival factor J^(-2*n). Use a higher-prefix-informed action or change
the receiver architecture; unchanged-cycle postselection is not a depth fix.

A classical or quantum construction of a costed tau would remove both
global rank and unrank requirements. The exhaustive batch reference already
defines a tau, but its evaluator stores or searches3^M words. The affine
partial instrument defines a cheap tau on its good lines and identity on
the rest, but its typical alpha is blocked by the polynomial-menu audit.
Neither satisfies both efficient evaluation AND adequate coverage.

The new full-depth target is a POLYNOMIAL-DESCRIPTION nonlinear cycle action with a
costed coherent evaluator and a source-valid coverage theorem. It may use
exponentially many implicit direction values; a polynomial-size program is
not a polynomial explicit menu. The existing menu barrier does not rule
that out. It may also fail: preserving the prefix and order three could be
as difficult as the original fiber-partition problem. This construction
does not lower that problem's complexity by renaming it.

An efficient arbitrary quantum receiver need not be a basis permutation
or have such a tau. Noncommuting measurements and source-specific approximate
transforms remain independent research routes. No equivalence to all possible
receivers, worst-case hardness theorem or LWE attack is asserted.

Approximation requires a coherent whole-instrument norm/error ledger, not
success on individual basis tests. Conditioning amplifies errors when alpha
is small. A constant-call evaluator error guarantee must be propagated through
all compute/uncompute operations and the success flag before normalizing
accepted branches. The finite exact audit does not discharge those obligations.

## Executable Controls And Falsifiers

The producer builds complete native reference cycles directly from LOW rows,
including H=9 carries, and a low-only affine partial cycle. It audits EVERY
original word, the order-three identity, prefix invariance, orbit coordinates,
injectivity and erased original-word scratch. All accepted branch phases are
checked against the true original full-root source. Reference maps remain
explicitly exponential; the partial affine control retains its real success
probability. No hard instance or toy oracle is generated as a candidate.

Reject: a two-cycle, an orbit with a changed prefix, reused output samples,
uncleared original-word scratch, missing coherent evaluation costs, high-label
selection presented as low-only, or a reference atlas declared efficient.

```
python theorems/ternary_nonlinear_cycle_compiler.py --write
node research/certificates/ternary_nonlinear_cycle_compiler_crosscheck.js
python -m pytest -q tests/test_ternary_nonlinear_cycle_compiler.py
```
