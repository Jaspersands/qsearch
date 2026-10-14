# Recursive Quotients: Exact Composition, Unresolved Producer Coverage

This is a conditional reduction audit, not a multiple producer or algorithm
discovery. The scientific target is to remove an unnecessary terminal
valuation restriction IF a usable mechanism exists at smaller roots.

## Canonical Same-Original Nodes

At current q=3^r a compatible external hypothesis (c,w) yields g=gcd(c,q),
Q=q/g and a prefix x IF w=c*s. Nonzero c modulo q ensures g<q; a unit
coefficient already supplies a full algebraic preimage. No nonunit inverse
or zero-modulus coefficient is accepted. Original records need not be paired.

Let the original modulus be q0, cumulative scale L=q0/q and original prefix
P<L coordinatewise. A nonunit step updates

    P' = P + L*x, L' = L*Q, q' = g.

For odd L,Q and any integer z, write k_D=(D-1)/2. Then
k_L+L*k_Q=k_(LQ), so

    nearest_Q(nearest_L(z)) = nearest_(LQ)(z).

Subtracting integral label contributions and reducing modulo the odd roots
preserves this identity. Every sequential derived response therefore equals
the direct ORIGINAL-record response

    nearest_(L')((y_original - a_original.P') modq0) modg.

This holds for ANY compatible supplied path, not just true paths. Nodes with
the same original-bank hash, g and P' contain exactly the same data and can
be merged. They are not fresh observations or separate IID trials. Different
prefixes must not be merged merely because their roots match. The module
verifies every sequential/direct equation and retains parent/original hashes.

If a unit step terminates the supplied path, the complete original preimage
is lifted, every supplied multiple equation is checked, and every original
circular distance is evaluated. An original-radius fit is not uniqueness or
planted truth. Actual producers and ambiguity search are NOT supplied here.

## Source Law And Recursion Traps

For a TRUE fixed quotient, Gaussian originals have exact derived error
nearest(gX). Normalized width alpha is preserved, but the same X is used at
every root. The high secret quotient of a uniform original secret is uniform
at each fixed root. It may be nonprimitive even when the original is primitive.
For q0=3^r and dimension n, a union over all proper fixed-root quotients
bounds nonprimitive failure by min(1,(r-1)/3^n). This premise is not inferred
from a chosen secret or from successful calibration paths.

An adaptive root does not automatically retain the unconditioned source law.
One can instead prove simultaneous good events at every fixed TRUE root,
then use a union. But an inverse-polynomial source-average coverage guarantee
does NOT imply high simultaneous success. Two source-good events can each
have probability1/2 and have empty intersection. Repeating random coins on
the same bad source does not automatically increase its good-instance mass.
Only a proved conditional-on-previous-success bound permits multiplying
per-level coverage. No such bound is supplied by this audit.
The Frechet ledger applies to a DECLARED set of fixed true roots. An adaptive
path with at most D visited roots does not justify unioning only D arbitrary
fixed-root failures: cover every reachable true root or prove a stronger
conditional selection theorem. The source contract does not certify that.

If each level has at most B list/coefficient branches and depth D, the
complete-tree work upper is sum_(j=0..D) B^j. Randomly following one branch
has success lower1/B^D IF every visited true list covers. B=poly(n) and
D=O(log n) generally gives quasipolynomial, not polynomial work. These
are costs of the stated traversal, not lower bounds on better reductions.
Node canonicalization may share repeated paths; no polynomial DAG bound
is asserted without counting distinct prefixes.

For a centered coefficient bound C, the first nonunit child satisfies
g<=min(C,q0/3), hence its root length is at most floor(log_3 C). Later
nonunit steps decrease that length. This is a possible leverage point,
not an efficient recovery theorem: source-compatible decision access,
terminal decoding, joint coverage and ambiguity control remain missing.

## Wrong-Prefix Falsifier

The complete noiseless original-label population at q81 with s5 and a WRONG
supplied prefix2 yields child value nearest(a/3) mod9 and child label a mod9.
Conditional on each child label, only THREE of nine values occur, each with
probability1/3. Total variation from full uniform is2/3. Thus wrong branches
need not be the standard full-uniform null presented to a decision algorithm.
This is a finite mathematical countercontrol, not a generated toy oracle
candidate. Gaussian applicability on false paths is deliberately uncertified.

## Literature Interface

[Bogdanov, Tan and Vasudevan, Theorem3.1 and Section4.1](https://arxiv.org/html/2610.12913v1)
provide a list containing a small multiple with source-average success.
Their coefficient is explicitly nonzero in Z_q. The list does not certify
which pair is true or give uniform conditional recursive success. The
general-noise theorem is the relevant interface for rounded continuous
Gaussian errors; do not import its discrete-Gaussian corollary automatically.
The recursive composition and counters above are local derivations, not
claims that the cited authors proved this recursive route. Novelty review
and the full recursive reduction remain open.

## Live Workflows And Next Proof

    python theorems/native_recursive_quotient_audit.py --write
    node research/certificates/native_recursive_quotient_crosscheck.js
    python -m pytest -q tests/test_native_recursive_quotient_audit.py

Two actual original-record chains, including root3^64, verify all ancestry
and full original fits. Their multiples come from truth ONLY in calibration.
Next: obtain a real source-compatible mechanism with JOINT root coverage,
or a verification/pruning theorem that bounds distinct surviving prefixes.
Absent that, stop claiming bounded per-level work solves the producer debt.
