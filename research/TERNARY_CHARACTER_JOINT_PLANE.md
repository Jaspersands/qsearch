# Exact Joint Laws Missing From The Cyclic Repair

LOCAL DERIVATION / REVIEW PENDING. Scoped finite counterexamples, not a new
decoder, growing-sample impossibility or source dequantization.

## Necessary Joint Probability

For G=Z_q^n, q=3^r, let a,b have additive order3 and be independent in G[3].
They generate a nine-element subgroup. Any genuine secret distribution has

    P(u,v) = (1/9) sum_(x,y=0)^2 chi_3(-xu-yv) f(xa+yb) >= 0.

The sectors are (a.s/(q/3), b.s/(q/3)) mod3. For a single secret this is a
delta distribution; a mixture preserves nonnegativity. Conjugate powers
prove exact reality, and f(0)=1 proves normalization. Each of the four
one-dimensional line marginals may be nonnegative even when the joint law
is negative. Separate cyclic positivity is not joint realizability.

The compiler hashes the EXISTING represented differences V-V, retains all
nonzero order-three lines, and scans every pair. It deduplicates their full
nine-element spans, chooses a canonical ordered basis, and retains a plane
ONLY when all nine moments are represented. Missing moments are neither
zero-filled nor supplied by a hidden oracle. Compiler input is public nodes
and q, never outcomes, planted truth or an optimizer witness.

There are at most K^2 represented differences and O(K^4) line pairs. Each
plane has nine laws with nine terms. This is a polynomial-description
family in K,n and the bit length of q, although K's upstream root dependence
still matters. It is NOT a complete global-character polytope description.
Whole-scan caps fail closed; incomplete planes and skipped moments remain
explicit. This does not enumerate q^n secrets.

## Decision Experiment

Audit the EXACT strengthened native gap points, rather than rerunning SCS.
Use rational interval UPPER bounds to certify negative joint probabilities.
Do not use floating FFT signs as proofs. Recheck the complete parent PSD,
cyclic and all-character gap certificates independently.

The public-coordinate full-root plane probe was insufficient: no coordinate
pair has all81 moments represented in either cohort. Restricting to chosen
coordinate axes would also miss the real obstruction. The exhaustive
represented order-three line scan tests all lawful complete planes,
including oblique ones; it does not tailor a basis to a negative optimizer
entry. A failure of these cuts to reject the points would be retained.

The original strengthened points fail2/1 joint laws on243/227 complete
represented planes. Exactly4,230 nine-sector laws are checked, with826/2,888
incomplete spanned planes retained. The negative probability upper bounds
are approximately-0.02661360277 and-0.01420415115.

## All Joint Cuts Also Admit Exact False Solutions

No expensive new optimizer is needed. For either certified parent point X,
construct X'=(3/4)X+(1/4)I with EXACT integer moments at scale4S. Distinct
nodes make I the moment matrix of the uniform full-secret distribution:
f_I(0)=1 and f_I(d)=0 for every nonzero represented d. It is not an invented
completion oracle. Its score is computed explicitly, never assumed zero.

PSD follows from the independently certified parent and convexity. EVERY
equal-difference equation and unit diagonal holds exactly. Cyclic and plane
laws satisfy

    p'_cycle = (3/4)p_cycle + (1/4)/m,
    p'_plane = (3/4)p_plane + (1/4)/9.

The producer rechecks every law with rational lower bounds, rather than
assuming the chosen mixture is sufficient. The mixed points have positive
joint laws yet STILL score strictly above every genuine secret. The all-secret
upper is reused only from the independently replayed same-record parent.
No all-secret census, truth or holdout enters the mixed-point construction.
The independent verifier checks every mixed integer,25,764 cyclic/joint
probability laws, and both exact objective gaps at the new common denominator.

This disproves universal tightness EVEN AFTER ALL compiled order-three plane
cuts. There is no reason to run another expensive SDP solely to rediscover
this finite gap. Such cuts might still help rounding or larger-sample regimes;
neither is disproved here. Any recovery test needs new fresh data, compilation
cost and matched classical baselines. A larger generic moment hierarchy is
not the default next research direction.

The surviving score gaps per training record are approximately0.1971680855
and0.6975217237, with exact positive numerators over denominator2^74. This is
not just a potential new false optimum: explicit exact feasible points exist.

More generally, if all joint probabilities are at least -delta, identity has
probability1/9, and parent/uniform/character scores are L,B,U, then positivity
needs lambda >= 9delta/(1+9delta). The score gap survives whenever
lambda < (L-U)/(L-B). For L>U>=B these intervals overlap precisely when

    9delta*(U-B) < L-U.

Use certified lower/upper endpoints conservatively for an interval proof.
This exposes why a few slightly negative local probabilities need not rescue
a large relaxation gap. It is a scoped convex-repair argument, not a lower
bound against higher-order constraints or arbitrary quantum algorithms.

## Falsifiers And Scope

- A true character or valid mixture fails an honest plane law.
- A claimed negative upper is nonnegative on exact independent replay.
- A dependent basis, missing vector or wrong Fourier sign invalidates a law.
- A retained plane depends on the witness or measurement outcomes.
- New feasible false solutions survive all these cuts.
- Larger sample regimes escape the finite obstruction.

These points are classical moment relaxations of quantum-produced records.
Neither their failure nor classical postprocessing proves classical simulation
of the unknown quantum input. External theorem review remains owed.

```
python theorems/ternary_character_joint_plane.py --write
node research/certificates/ternary_character_joint_plane_crosscheck.js
python -m pytest -q tests/test_ternary_character_joint_plane.py
```

Gemini owns CLI/registry/UI wiring and full production validation. Import the
negative joint probabilities as exact scoped evidence, never a speedup.
