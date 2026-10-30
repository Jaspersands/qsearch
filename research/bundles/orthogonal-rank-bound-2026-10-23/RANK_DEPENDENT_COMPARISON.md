# Rank-Dependent Classical Comparison For The Orthogonal HSP Proposal

2026-10-23. **Application of a published bound, with a local query-model
derivation. Independent review pending.** This strengthens the classical
comparison of the preceding three-probe proposal. It is neither a new
fixed-point theorem nor a natural-input speedup or cryptanalytic result.

## 1. The Specific Gap Being Closed

The preceding proof gave a full-group classical query lower bound growing
as sqrt(q), from one nonzero quadratic equation on an alternating chart.
At fixed q this is constant. It cannot support an exponential-in-rank
comparison. Counting one equation discarded most of the stabilizer geometry.

Keep the SAME problem: a coherent oracle f on O+(2n,q) or SO+(2n,q) hides
the FULL stabilizer P_L of an unknown maximal totally singular subspace L.
Here q is an odd prime power, n>=3, and the field is effectively presented.
The proposed quantum recovery algorithm is unchanged. Classical algorithms
may query arbitrary group elements adaptively and use unlimited computation.
They are not restricted to the three selected abelian probes.

For the lower bound, choose L uniformly from ONE known component C of the
maximal-singular Grassmannian, and randomly injectively relabel its cosets.
Giving the component to the classical algorithm is allowed. Write

    M = |C| = product_{i=1}^{n-1} (q^i+1).

For completeness, the total count T_n follows by counting incidences with
singular lines. There are `(q^n-1)(q^(n-1)+1)/(q-1)` such lines, each lies
in T_(n-1) maximal singular spaces, and each maximal space contains
`(q^n-1)/(q-1)` lines. Therefore T_n=(q^(n-1)+1)T_(n-1), with T_1=2.
A hyperbolic-pair swap interchanges the two equally sized components.

## 2. Verified Primary-Source Input

[Guralnick and Kantor, Probabilistic Generation of Finite Simple Groups,
J. Algebra 234 (2000), 743-792](https://pages.uoregon.edu/kantor/PAPERS/gkfinal.pdf),
Section 3.2 (pp753-754), defines the relevant normalizer actions and allows
both orthogonal orbits or their union. Lemma 3.14 (pp756-758) bounds the
nontrivial maximal-singular fixed-point ratio by
`2/|F|^(m*) + 1/|F|^(m#)` for m>=3. Its parameter table gives m*=n-2,
m#=n-1 for the split orthogonal group. The cited pages were read as text and
visually checked, including the exponents. This is a SUBSPACE-action result;
the non-subspace fixed-point theorems are not being substituted for it.

Thus for a noncentral g in SO+(2n,q), on either component,

    Pr_{L uniform C}[gL=L] < beta(n,q)
                          = 2/q^(n-2) + 1/q^(n-1).

This is not inferred from finite examples. The extra diagonal coset of
Omega in SO is covered by the normalizer scope, not silently discarded.

For g in O with determinant -1, the fixed-point probability is zero:
the stabilizer of any maximal singular L has determinant one. In adapted
coordinates it is block triangular with diagonal A,A^(-T). Therefore the
same beta applies to every noncentral full-O query difference as well.

The universal kernel is exactly {+I,-I}. The earlier alternating-chart
polynomial argument proves this without a center-classification lookup:
fixing every graph forces the off-diagonal blocks to vanish and both
diagonal blocks to be the same scalar. Orthogonality makes that scalar +/-1.
The chart lies in a single component. Its argument needs n>=3.

## 3. Adaptive Opaque-Label Coupling

Fix the classical algorithm's internal randomness. Run it against a dummy
oracle that assigns fresh uniformly chosen distinct labels to query classes
modulo +/-I. Queries differing by that known central kernel receive the
same label. The dummy transcript, including the adaptively chosen matrices,
is independent of L.

Couple this transcript to a genuine randomly relabeled coset oracle until
the first noncentral collision. For any pair of dummy queries g_i,g_j whose
difference is noncentral, the event of a real collision is

    g_i L = g_j L  iff  (g_j^-1 g_i)L=L,

and has probability at most beta. A union bound over the precomputed dummy
transcript gives probability at most binomial(Q,2)*beta that any such
collision happens. This remains valid for adaptivity: independence is
asserted for the DUMMY transcript, not for the posterior conditioned on no
collision. Once a collision occurs, grant the algorithm success for free.

On no collision, the output is the dummy output. Since that output is
independent of uniform L, its unconditioned guessing success is at most 1/M.
Intersecting with the no-collision event cannot increase that joint
probability. Averaging over the algorithm's randomness therefore gives

    Pr[recover L] <= min(1, 1/M + binomial(Q,2)*beta).

The coupling needs enough distinct label names for its fresh labels. For
Q up to the number of genuine cosets this holds. Above that count the
displayed bound is already at least one, so the trivial bound suffices.
The label widths are O(n^2 log q), not a hidden exponential-bit resource.
This is an average-case bound over L AND relabeling; it implies a worst-case
oracle lower bound, not hardness for every fixed labeling.

For any constant success target bounded away from zero,

    Q = Omega(q^((n-2)/2)).

At fixed odd q, this is exponential in n. The existing proposed quantum
schedule is polynomial in n, log q and log(1/epsilon). Thus, conditional
only on correctness of the proposed quantum reduction and this application,
the comparison is no longer limited to growing field size. No circuit has
been compiled or physically executed to establish that polynomial schedule.

## 4. A Root Element Explains The Exponent

This is a local incidence derivation, not a claim that we have classified
the maximum fixed-point ratio. Let

    u = [[I,D],[0,I]],    D=E_12-E_21,
    R = image(u-I) = span(e1,e2).

For maximal singular L, set t=dim(L intersect R). The image of L in the
dual of R has dimension 2-t, so (u-I)L has that dimension. If t=0, it
cannot lie in L intersect R. If t=2, it vanishes. If t=1, the alternating
rank-two map D sends the annihilator of the line L intersect R precisely
onto that line. Consequently

    uL=L  iff  dim(L intersect R)>=1.

Each of the q+1 lines in R lies in
`A=product_{i=1}^{n-2}(q^i+1)` members of a given component. Exactly
`B=product_{i=1}^{n-3}(q^i+1)` members contain all of R. Incidence counting
subtracts q extra counts for each such member. Thus the exact ratio is

    ((q+1)A-qB)/M
      = ((q+1)q^(n-2)+1)/[(q^(n-2)+1)(q^(n-1)+1)].

It lies between `(1/2)q^(-(n-2))` and beta. Therefore this uniform
fixed-point/collision method cannot improve its exponent simply by
sharpening beta's constant. This does not show a classical algorithm
achieves the lower bound or that every query strategy encounters roots.

The existing generic classical birthday algorithm on each line probe uses
`O(poly(n,log(1/epsilon))*q^((n-1)/2))` expected queries. At fixed q its
rank exponent matches the lower bound, up to the polynomial prefactor.
The extra sqrt(q) factor matters when q varies. This upper bound is a
derived baseline, not a new implementation or an assertion of optimality.

**Subsequent same-day improvement:**
`../orthogonal-isotropic-birthday-2026-10-23/CLASSICAL_ATTACK.md` supplies
a stronger classical attack using random maximal-singular restrictions of
each probe. Its proposed cost is poly(n,log(1/epsilon))*q^((n-2)/2), matching
the lower-bound exponent also when q grows. The executable controller uses
only the same opaque oracle and records all calls. The older upper bound
above remains valid but is no longer the best implemented comparator.

## 5. Attempts To Invalidate The Comparison

1. **Structured labels defeat it.** If f(g) returns a basis of gL, then
   f(I) gives L in one classical query. Random opaque relabeling is a real
   restriction, not a consequence of the HSP equality promise. An explicit
   efficient source can have much more information than its collision
   partition. The finite test includes this one-query counterexample.
2. **Center collisions are free.** +/-g always collide. Counting those
   events against beta would invalidate the proof. Dummy labels identify
   those public classes from the outset.
3. **Rank two is excluded.** An elementary SL2 Levi fixes every alternating
   graph in a component. Neither the n>=3 kernel argument nor the quoted
   lemma licenses extrapolation to n=2. Existing rank-two falsifiers remain.
4. **Two components are not interchangeable advice.** The prior is a known
   single component; SO preserves it. O queries may cross it, but a
   determinant-minus-one difference has no fixed maximal singular space.
5. **A root calculation is not a universal theorem.** Only the cited
   published lemma supplies the all-element bound. Enumerating several
   representative elements over all small hidden spaces does not do so.
6. **No quantum speedup from a classical simulator.** The preceding dense
   Fourier reference queries exponentially many values. Its actual calls
   cannot be replaced in a report by the proposed coherent query schedule.
7. **No novelty inference.** Both fixed-point estimates and opaque-label
   collision lower-bound arguments are established techniques. Whether the
   three-probe orthogonal recovery is already known remains unresolved.

## 6. What This Changes, And What It Does Not

The fixed-field classical-comparison blocker has a concrete literature-backed
resolution. The old `2/q` chart bound remains a valid simpler comparison
with a different prior; do not take their minimum without reconciling priors.
The new prior and proof replace it for the rank claim.

The next high-value work is independent review of the three-probe reduction
and a precise prior-art comparison, followed by a genuinely useful explicit
source. More opaque-label fixtures, finer constants, neighboring group
variants or dashboard wiring will not turn this into a Shor-level result.

No result is admitted to the moving repository's candidate registry. These
files are in a separate local research bundle because migration is active.

## 7. Additional Prior-Art Check

[Ivanyos (2012), Section 5](https://www.rintonpress.com/xxqic12/qic-12-78/0661-0669.pdf)
explicitly discusses extending hidden-Borel methods to orthogonal groups.
That historical question does not certify that it remains open today. Our
promise is a maximal-singular stabilizer, not an arbitrary orthogonal Borel;
the three-probe argument does NOT solve the latter by assertion.

[Ettinger, Hoyer and Knill (2004)](https://arxiv.org/abs/quant-ph/0401083)
already obtain polynomial quantum query complexity for arbitrary finite-group
HSP, with exponential computation. Thus the important proposed contribution
is efficient recovery, not merely polynomial queries versus a classical
lower bound. A query-separation headline alone would substantially overstate
what is new.

Targeted searches for orthogonal/parabolic HSP, polar-space hidden subgroups,
and unipotent-radical quantum methods did not locate a covering theorem.
This is an incomplete search, not a novelty conclusion. The prior pass also
checked the GL parabolic and finite-chain-ring results; an oracle restricted
to O cannot simply be evaluated on arbitrary GL matrices. Any reduction
through a GL theorem must explicitly construct that extra oracle access.
