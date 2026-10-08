# Native Prefix Modular Shadows

LOCAL DERIVATION / REVIEW PENDING. This is an exact discrete falsification
baseline on the actual native-prefix distribution, not a quantum algorithm,
native integer decoder or general modular-cut no-go.

## Why Test This

The preceding audit found 16 genuinely false native prefixes with exact
fractional continuations even after integral winding. Integer coefficients
have information that real LPs erase. A natural cheap proposal is to require
prefix-lattice membership modulo two before doing harder integer decoding.
This pass implements and tries to falsify that proposal, rather than assuming
that a discrete constraint must help.

## Exact Binary-Domain Elimination

Let `K` be the actual unassigned integer kernel rows and `z_anchor` the actual
prefix anchor. A necessary condition for an original native word is

```text
z_native-z_anchor in row_span(K mod2).
```

Keep EVERY retained digit domain from the source projector. Choose its first
digit as the baseline. A singleton contributes no variable. A two-choice block
has image `{0,difference}` over F2, which is exactly a whole binary line.
The independent choices across those blocks therefore cover their entire
span `W`, with no probabilistic or relaxation step.

Compute the FULL annihilator `H` of `row_span(K mod2)+W`, not a convenient
low-rank subset. The remaining full native triangles have quotient images
`{0,H*e_u,H*e_v}`. Their sum must contain
`H*(z_anchor-z_baseline)`. This is EQUIVALENT to modulo-two native feasibility,
because any needed binary-domain correction in W has actual digit choices.
It is NOT equivalent to original integer prefix membership. The same binary
elimination is invalid over F3: a two-element set is not a ternary line.

FLINT computes exact ranks and nullspaces. Original Python integer entries
are reduced modulo two before entering bounded-word arithmetic; packed
syndrome records use decimal strings to avoid JavaScript integer loss.

## Three Independent Evidence Modes

1. Complete XOR support DP, guarded by the ENTIRE ambient `2^rank` size. A full
   support at an intermediate block stays full under subsequent nonempty
   convolutions. No truncated support is called an obstruction.
2. Exact Fourier sufficient condition. For a full ternary block `{0,u,v}`,
   every nontrivial binary-character factor has magnitude 1 or 1/3. Let
   `w(h)` count nonconstant blocks and `B=sum_(h!=0)3^(-w(h))`. If `B<1`,
   Fourier inversion gives every syndrome probability at least
   `(1-B)/2^rank`. Integer weight histograms prove the comparison exactly.
   Failure of this bound does NOT prove missing support.
3. A concrete native modular word. Uniformly sample the exact affine binary
   solution space for the remaining full blocks, rejecting every forbidden
   `(1,1)`. Recover the eliminated binary choices by another exact field solve.
   Retain `z_native` and binary prefix coefficients c satisfying
   `z_native-z_anchor=sum_i c_i K_i (mod2)` in ORIGINAL coordinates. This
   proof does not trust the quotient, proposal RNG, support table or Fourier bound.

Uniform affine rejection may have exponentially small acceptance as the number
of full triangles grows. A fixed proposal budget is not a polynomial-runtime
or source-law guarantee. Failed proposals remain unknown unless a different
exact certificate resolves them. Modular words are never candidate algorithm
outputs or integer-continuation witnesses.

## Live Outcome

All 26 exact LP-feasible parent prefixes from the preceding audit were tested:
9 at root16, 8 at root24 and 9 at root32, with the SAME conditional fixtures.

- All 26 have independently checkable original-coordinate native modulo-two
  words, including all 16 exact fixed-winding integrality gaps.
- NONE of these 26 modular words matches the original high-modulus target.
  They certify a relaxation's limitation, not even first-witness recovery.
- Those proofs required 3,163 affine proposals in total; all rejected proposals,
  native-digit checks, random nullspace XORs and recovery solves are charged.
- Complete support DP resolves 11 cases, with 28,189 XOR transitions. All 11
  targets are reachable; three have full quotient support. Their exact Fourier
  bounds independently certify the same three full-support cases.
- Fifteen full support tables are guarded out. Their target membership is STILL
  resolved by concrete modular words; arbitrary other syndromes remain unknown.
- Effective quotient dimensions are 2..12 at root16, 13..20 at root24 and
  26..33 at root32. No growing-rank DP is presented as polynomial work.

Therefore modulo-two PREFIX-FEASIBILITY checks alone cannot prune any of these
26 branches. In the three full-support cases they cannot prune ANY anchor
syndrome within that same domain-restricted modular model. Neither statement
rules out cuts that use original high-precision equations, modular powers of
three, interacting moduli, higher-degree moments or other representations.
The root32 INTEGER native truth remains unknown; a modular word does not resolve it.

## How To Prove This Conclusion Wrong

A wrong retained domain, incomplete annihilator, invalid binary elimination,
lossy syndrome, false word/coefficient identity or bad support/Fourier count
would invalidate the corresponding certificate. Unit tests cover all original
small-source words, all seven possible nonempty domains, nonunit/zero labels,
huge integer entries, forbidden fourth corners, guards, positive/negative
modular controls and an inconclusive Fourier bound on genuinely full support.
The independent JavaScript checker reconstructs the original geometry/domains,
verifies complete rank/annihilation, replays DP and exact weight enumerators,
and checks every word against the ORIGINAL integer prefix modulo two.

These 26 observations do not prove a population statement or say that residue
cuts never help elsewhere. Adding more primes without a precision/cost model
could simply hide exponential integer decoding. The next target instead asks
whether polynomial-size block-coupled moments capture a missing discrete feature;
see `NATIVE_TERNARY_COUPLED_MOMENTS_TARGET.md`.

```sh
python theorems/ternary_prefix_modular.py --write
python -m pytest -q tests/test_ternary_prefix_modular.py
node research/certificates/ternary_prefix_integrality_crosscheck.js
```

No decoder runtime integration is justified: the new mechanism pruned ZERO
audited feasible branches. Gemini/Antigravity may expose the report through
qsearch/registry/UI without promoting a candidate or quantum signal.
