# Scalar Fermat Backend For Rees State Sources

2026-10-22. Implements a missing PUBLIC arithmetic prerequisite, not a
new quantum algorithm. The full Rees receiver, novelty and a natural hard
application remain under review. No central-registry admission is made.

## Why This Pass

The whole-proof review rechecked the nonnormal-coset orientation, normalized
central branches and pointwise witness cancellation. No fatal error was
identified in those steps; this is not independent verification. The
literature checked still distinguishes the growing-prime proposal from
the bounded-prime result of Imran--Ivanyos. Absence of a search hit does
not certify novelty. No new hard natural application was established.

The proposed copy-only group-action conversion was already present in
REES_PROJECTIVE_STATE_SOURCE.md. Do not relabel its rediscovery as progress.
It needs public nonzero rows solving sum x_i^d=0, with at most d+1 entries,
to cancel unknown stabilizer characters without conjugate-state access.
The implementation previously rejected some valid even degrees and primes.
This pass removes that specific limitation.

## Scalar Algorithm And Proof

Known odd prime p, integer 1<=d<p. Odd d uses (1,-1). For even d>=2,
let N be the number of zeros of sum_(i=1..d+1) x_i^d over F_p. The standard
additive-character bound |sum_x e_p(t*x^d)|<=(d-1)*sqrt(p), t nonzero,
is stated in [Moment subset sums, Theorem 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC10941333/).
Character orthogonality gives

```
|N-p^d| <= (d-1)^(d+1) * p^((d+1)/2).
```

Use the exact integer large-field test

```
p^(d-1) >= 16*(d-1)^(2*d+2).
```

Then N>=3*p^d/4 and N-1>=p^d/2. Each d-coordinate prefix has at most d
completions. Therefore a uniformly random prefix admits a NONZERO solution
with probability at least 1/(2d). The zero prefix has only the all-zero
completion and is rejected. For the other prefixes set value=-sum x_i^d.
Zero value gives final coordinate zero. For nonzero value, the exact test
value^((p-1)/gcd(d,p-1))=1 decides whether a root exists. Find one root of
X^d-value with FLINT and verify the entire resulting row exactly.

This is not a search over p field elements at large primes. It uses d
random residues per attempt and at most one root-finding call before a
successful return. The random-prefix argument is unconditional for the
stated field/degree assumptions; reproducible seeds alone do not prove it.

If the large-field inequality fails, necessarily p<16*(d-1)^4. Enumerating
the field is now explicitly bounded by a polynomial in d. Build one root
per d-th-power value, and use a d-step residue dynamic program to represent
-1 as a sum of d such values. Prepend 1. Existence follows from the usual
homogeneous equation existence theorem: a nonzero solution on d+1 variables
can be permuted and scaled to put 1 first, because all coefficients equal
one. The dynamic program costs O(d*p^2) transitions and O(d*p) stored
predecessors. It is never used outside the proved small-field regime.

This solves only the equal-coefficient SCALAR Fermat problem. The stronger
published scalar diagonal algorithms remain prior art, as does the
many-equation Ivanyos--Santha theorem. Neither a replacement for that
general SDE solver nor a new arithmetic speedup is claimed.

## Failure And Runtime Accounting

After T independent uniform trials, sampling ABORT probability is at most
(1-1/(2d))^T. ABORT never returns an invalid witness. `fermat_trial_cap`
chooses an exact conservative cap from a rational error allowance: take
T=2*d*ceil(log2(1/eta)). This controls SAMPLING, not the internal wall clock
of the FLINT polynomial-root backend. Root finding remains an expected-time
arithmetic dependency, as in the existing cubic SDE module.

For a class-c design, give each of at most c scalar rows allowance eta/c
and use the class-c cap. A union bound pays for all rows; the existing
quadratic sampler has a stronger per-trial guarantee. A failed small-root-
of-unity fast path merely falls back and adds no extra failure event.
All this public preparation occurs BEFORE acquiring unknown state copies.

`projective_source_budget` takes an already certified design; it does not
include a design-generation failure. For an end-to-end error epsilon, one
valid composition allocates epsilon/2 to design preprocessing and calls
that budget with error epsilon/2. A separately capped root implementation
would need its own runtime/failure allowance. Do not describe the current
library calls as a fully clocked quantum receiver.

## Changes And Verification Surface

- `theorems/scalar_fermat_solver.py`: exact witnesses, regime guard,
  sampling-cap calculation, degree-bounded DP, root verification and report.
- `theorems/rees_projective_source.py`: retains cheaper existing paths,
  invokes the new scalar backend for previously unsupported degrees,
  and generates explicit forced-fallback artifacts.
- Tests include the former p=13 quartic failure; a128-bit prime p=2^128-275
  with p=5 mod8, where -1 is NOT a fourth power; exact bounded success
  counts; all-zero sampling ABORT; malformed RNG/root rejection; and a guard
  preventing large primes from entering the enumerating path.
- Existing source tests retain mixed-state scope, fresh-copy, phase,
  workspace and nonnormal-subgroup falsifiers. No generic noisy-state
  correction or mixed-state conjugation-symmetry claim is added.

Standalone workflow: `python -m theorems.scalar_fermat_solver --write`.
Integrated workflow: `python -m theorems.rees_projective_source --write`.
The receiver's GENERAL MANY-EQUATION SDE backend is still incomplete.
Further public-arithmetic work should be justified by a concrete receiver
obstruction, not by a desire to accumulate implemented modules.
