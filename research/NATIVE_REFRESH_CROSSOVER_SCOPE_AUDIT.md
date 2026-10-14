# Crossover Scope, Classical Dominance And Dimension Debt

This audit keeps the refresh-to-clean-basis algebra but rejects the CURRENT
composed recovery claim. It does not assert that all source refresh, all
search-to-decision reductions or all quantum measurements fail. The reviewed
report is untrusted input; its broken producer is not imported.

## Scope Cannot Be Added Like Failure Probabilities

For an original nonzero centered coefficient with |c| <= C, its nonunit
factor g = gcd(c, 3^r) is at most C. Every subsequent child root strictly
decreases. A refresh window entirely above this first-child bound therefore
cannot describe the same declared recursive path.

The n=32 profile has C=512, so its largest first child is 3^5=243, but
claims refresh at 3^9 and 3^10. The n=128 profile has C=16384, so the
largest first child is 3^8=6561, but claims refresh at 3^12 and 3^13.
Moreover, EVERY root in both refresh windows fails the pruning proof's
own sufficient gate 4*R < q/g, with R=ceil(8*alpha_original*q).

The small union of failure bounds on different, incompatible scopes is
not a recovery guarantee. This audit returns NULL for the composed bound.
Increasing C alone would not fix the failed radius gate. Restricting to
the safe pruning roots must also confront the existing classical completion
baseline; the first supplied usable multiple already suffices there under
the radius and separation events described in NATIVE_PREFIX_AMBIGUITY_PRUNING.

## Matched Controls, Without Another Producer Call

Both supplied recovery controls are replayed from all their original records
and ALL three first-stage candidate pairs. Mask removal is checked exactly.
The existing basis lottery is run on these pairs with label-only cached bases,
paid rank/inverse/rounding work and full original distance verification.
Neither the secret nor later-stage candidates enter the algorithm.

In each control the false pair fails and the two true pairs recover the same
secret as the proposed multi-stage pipeline. No second refresh, recursive
producer or Gaussian dither is used. The large 3^64/odd-original-count control
is included, so this comparison is not contingent on the older even-bank API.
Fixture truth is used only AFTER solving. These controls establish matched
classical dominance on the controls, not source-wide correctness or a global
no-go. The candidate lists remain supplied calibration data.

## The Valid Inequality Is Not A Dimension-Free Success Theorem

Write H_min=(eta^2*alpha_target^2/(4*k)-m/(2*g_min^2))/2 > 0 and
delta=m*alpha_original^2/(6*H_min). At a smaller root where H_term <= 0,

    beta_term^2 < 3*delta/2.

This follows by substituting the two thresholds; it is retained. But for
IID errors a chosen n-row invertible basis recovers the true remaining
secret only when ALL its rounded errors vanish MODULO g_term. The upper
bound per basis is p_ring_zero^n, not p_ring_zero. Nonzero ring wraps are
included in the probability enclosure; no clean-event necessity is falsely
imposed in place of ring-zero necessity.

A deliberately astronomical analytical counterprofile takes
n=3^80, m=128*n, k=n, g_term=3^85, g_min=3^86,
alpha_original=1/(10*g_term), and eta=alpha_target=1/4.
It has beta=1/10, delta<1/100 and satisfies the crossover inequality, yet
the probability that ANY of 128 disjoint bases recovers the secret is tiny.
This is a logical scaling counterexample, NOT an executed source bank and
NOT a refutation of the existing n=32 or n=128 lottery probability boxes.

No astronomical exact probability power is evaluated. For certified ring
escape floor p>0, reciprocal Bernoulli gives

    (1-p)^ceil(1/p) <= 1/2,
    P(any correct basis) <= T * 2^-floor(n/ceil(1/p)).

The reported exponent is safely capped at 192. Gaussian enclosures use
trusted FLINT/Arb and can be replayed separately; the JS arithmetic checker
does NOT independently certify transcendental functions. No bound against
other classical decoders or quantum strategies is inferred.

## Workflows And Decision

    python theorems/native_refresh_crossover_scope_audit.py --write
    python theorems/native_refresh_crossover_scope_audit.py --check-probabilities
    node research/certificates/native_refresh_crossover_scope_audit_crosscheck.js
    python -m pytest -q tests/test_native_refresh_crossover_scope_audit.py

Keep the lemma as a conditional reduction tool. Do not repair the missing
quantum mechanism by writing another traversal wrapper. Integration repair
of the older producer remains Gemini's task, with this scope audit required
before promoting its recorded composition claims.
