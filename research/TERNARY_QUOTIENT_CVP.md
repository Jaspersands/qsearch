# Exact Orthogonal Dead-Direction Elimination

## Claim And Its Limit

The full-record lattice attack has many basis directions that cannot change
the secret class through either their own code image or Gram-Schmidt
feedforward. This does NOT alone license deleting those dimensions from CVP:
code-zero directions may be coupled to one another. The new compiler requires
their mutual Gram-Schmidt coefficients to be EXACTLY zero. It fails closed
with `UNKNOWN_COUPLED_DEAD_DIRECTIONS` otherwise.

For a certified full square basis R, write its exact orthogonalization as
R_i=R_i*+sum_(j<i) mu_ij R_j*, with D_i=||R_i*||^2>0 and
alpha_i=<y,R_i*>/D_i. For any integer coefficient vector c,

    ||y-sum_i c_i R_i||^2
      =sum_j D_j (alpha_j-c_j-sum_(i>j) mu_ij c_i)^2.

Let L be the live influence closure and Z its complement. By construction a
dead coefficient cannot influence a live one; its own public code secret
is zero. Under the additional diagonal-dead test, no dead coefficient
influences another dead coefficient either. Fixing c_L therefore gives the
EXACT global conditional minimum over ALL c_Z, by independent nearest-integer
rounding (ties to floor(x+1/2)):

    Phi(c_L) = sum_(j in L) D_j
        (alpha_j-c_j-sum_(i in L,i>j) mu_ij c_i)^2
      +sum_(j in Z) D_j dist(alpha_j-sum_(i in L,i>j) mu_ij c_i, Z)^2.

The secret is sum_(i in L) c_i s_i mod q, where s_i is the public code image
of R_i. This is an exact elimination theorem for the represented lattice,
not a claim that the number of live directions stays small as n,r grow.
The periodic second term is essential. It couples the remaining coefficients
and preserves a potentially difficult nonconvex search; Phi is NOT an
ordinary lower-dimensional Euclidean CVP. Conditional optimality is NOT
global optimality over c_L and does not grant the required9/8 factor.

## Critical Countercheck: The Original Problem Already Has n Coordinates

The observed1024-to59 LLL-coordinate compression is NOT a reduction of the
original number of unknowns. The secret already has n=8 coordinates. In fact
EVERY full-unit-rank systematic code lattice here admits an exact n-coordinate
form: put the m-n nonpivot q-axis rows FIRST and the n systematic code-generator
rows LAST. The q-axes are mutually orthogonal, code-zero and GS-dead. Projecting
the code generators off them leaves exactly the orthonormal pivot axes, so
there are n live coefficients with D_i=1 and no live-live GS coupling.

The remaining periodic cost is

    sum_i (y_(pivot_i)-c_i)^2
      +sum_(j nonpivot) q^2 dist((y_j-sum_i G_ij*c_i)/q, Z)^2.

For each c mod q, choosing its nearest lift to the pivot outcomes gives the
canonical wrapped cost of the corresponding secret. The pivot inverse is a
bijection to ALL q^n secret classes. Thus this n-coordinate formulation is
the original hard inference objective in different coordinates, not a new
dimension-reduction breakthrough. LLL can still help the geometry of local
proposals, but having59 active directions instead of1024 is NOT evidence of
a lower intrinsic dimension or better asymptotic complexity. The report and
independent checker retain this systematic-basis countercheck explicitly.

This revision also changes the next research question: prove useful geometric
conditioning or search-cost bounds, not just a small active-coordinate count.

## Bounded Attack And Falsifiers

The implemented public policy uses beam width32 and branch radius1, processing
live indices in descending order. Each retained state branches at the nearest
coefficient and its two adjacent integers. Partial scores include exact live
costs plus dead costs once ALL their live dependencies have been assigned.
These scores are lower bounds on completions. They are exact rationals.
Ties are broken by the descending coefficient tuple. Beam pruning and the
finite local coefficient menu do NOT preserve a guarantee of finding CVP.

Every final state is reconstructed in the ORIGINAL full lattice. Exact
Gram-Schmidt and coordinate distances must agree. Its secret satisfies EVERY
original full-root congruence. Training evaluates canonical wrapped Euclidean
cost and the stable native likelihood, both on ALL original records. Previous
public proposals are retained so either objective cannot worsen merely
because beam pruning discards an old candidate. Their costs and source
lineage are not charged as new experiments.

The posthoc valid point from the parent report supplies a falsifier:
64*C-81*W>0 proves THIS new proposal pool also misses norm9/8, where C is its
best canonical distance and W is a public valid comparison point's distance.
No exact global optimum or optimality of the planted secret is assumed.
If the margin disappears, the result is INCONCLUSIVE, not proof of9/8.
Fresh failure does not prove classical hardness or exclude quantum receivers.

## Prospective Validation Policy

The eight existing training cohorts and label-only LLL bases are reused.
Their old holdout results influenced this design and are NEVER reused for
the new attack's validation. Both new selections are frozen before512
new simulated native records, with seed120200+parent_seed and new source IDs.
Multiplicity counts DISTINCT frozen candidates, not all training proposals.
The original source simulation is not physical quantum-state preparation.
All these training cohorts remain below the population CVP reduction's
conservative copy budget; no confidence is inherited from that theorem.

The report pins the complete parent bytes and this derivation. The parent
supplies exact basis transformations and all training records, so they are
not duplicated. New evidence contains full coefficient paths, stage costs,
new validation data, comparison margins and honest cumulative copy counts:
M training +512 old validation +512 new validation originals. New LLL calls
are zero, but the inherited THREE reductions per cohort remain charged.

An independent BigInt/rational JS implementation replays the parent
certificate, checks the elimination premise, regenerates the ENTIRE bounded
beam policy, and verifies final lattice points, objectives, fresh gates,
factor falsifiers and the resource ledger. Exact arithmetic does not certify
floating native-likelihood ordering when scores are arbitrarily close;
bounded represented-root likelihood checks are numerical crosschecks only.
`--replay-saved --write` updates mathematical certificates and derivation
hashes without generating new training, validation or decoder outputs.

## Next Decision

If the bounded attack fails, first distinguish missed branches from weak
partial bounds. A complete radius-bounded search with an explicit node cap
could certify small-instance CVP or return UNKNOWN; cap exhaustion cannot
be relabeled as optimality. Other possible advances are sharper admissible
periodic lower bounds and source-aware coefficient proposals. Merely deleting
the periodic objective, granting Gaussian noise or treating a small observed
active rank as an asymptotic theorem would invalidate this direction.

No production CLI, UI, registry or Git wiring is part of this scientific pass;
those remain delegated to Gemini/Antigravity under the operating contract.
