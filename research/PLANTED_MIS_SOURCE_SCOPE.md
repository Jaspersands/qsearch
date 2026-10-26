# Protected Planted MIS: Optimality Without A Preserved Cover

Status: exact structural certificate and written uniqueness proof, pending
independent mathematical/source review. The new uniqueness argument is NOT
Lean-formalized. The earlier two recovery lemmas are. No author-data
reproduction, general MIS algorithm, or quantum execution.

## Question And Answer

The previous [pair-closure pass](PLANTED_MIS_PAIR_CLOSURE.md) recovered the
planted set from the graph alone, but assumed that set was maximum. Its
synthetic control preserved an additional clique cover to certify that
assumption. Does the optimum remain certifiable without this extra restriction?

**Yes, under a checkable disjoint-star deletion condition and a strict
cardinality margin.** The new control deletes 11 edges of the old cover.
It still has a uniquely optimal planted set, certified independently of the
graph-only solver. This closes the extra-control-restriction gap; it does not
extend the result to unrestricted planted graphs.

## Exact Theorem

The task is unweighted maximum independent set on an explicit finite graph.
No extension to arbitrary vertex weights is asserted.

Partition V into blocks, each partitioned into cliques. Initially, every
within-clique pair and every cross-block pair is an edge, with no other edges.
Choose S with at most one vertex per clique. Remove cross-block edges within S.
Then remove some cross-block edges between vertices outside S. Let F be the
graph consisting of these latter deletions.

Suppose F is a vertex-disjoint union of stars and isolated vertices. Set

```
b = maximum number of cliques in any one block,
K = |S|.
```

If `K > b+1`, then S is the unique maximum independent set.

Proof: consider any independent set I.

1. If I meets S in two distinct blocks, every outside vertex is adjacent
   to at least one of those two planted vertices. Hence `I subset S`.
2. If I meets S in exactly one block, I cannot contain vertices from any
   other block. Unchanged within-clique edges imply `|I| <= b`.
3. If I avoids S and occupies three blocks, one chosen vertex from each
   yields a triangle in F. This is impossible in a star forest.
4. If I avoids S and occupies two blocks with at least two vertices in
   each, those four vertices yield a four-cycle in F. Also impossible.
   Thus one occupied block has at most one vertex, and the other at most b.
   A single-block I is already bounded by b.

Every I not contained in S consequently has size at most `b+1 < K`.
Proper subsets of S have size less than K as well. This proves uniqueness.

The proof needs neither equal vertex degrees, a preserved global clique
cover, nor the additional condition on adjacency among a star's leaves.
Those conditions can be used by a generator, but are not proof premises.
Disjoint stars are sufficient, not necessary. Rejecting a certificate
outside that class does not prove that the planted set is suboptimal.

### Recovery And Advice

The earlier graph-only algorithm enumerates all nonedges {a,b}, computes
`V \ (N(a) union N(b))` using open neighborhoods, and retains the largest
independent result. Two planted vertices in different blocks recover S.
The strict margin forces S to occupy more than one block.

Thus, on this promised family, recovery takes O(n^4) Boolean operations and
O(n^2) graph storage, with no block, clique, planting, or optimum-size advice.
The NEW verifier receives the returned set and a structural witness AFTER
solving. It checks all graph edges against the declared construction, then
reconstructs F and checks its components. The witness does not accelerate
the search. This is not a claim that the witness can be recovered efficiently
for every arbitrary graph, nor is it required by the promised-family solver.

## Source Audit And Scope

[Choi, 2601.17686v1, Section 2.1](https://arxiv.org/html/2601.17686v1#S2.SS1)
specifies complete cross-block edges before planting and outside-only
anchored thinning. Its one-participation restriction naturally gives
disjoint stars when it includes both centers and removed neighbors.
The implementation checks that graph property directly, without assuming
that unseen benchmark files obey this interpretation.

Table 1 has

```
(clique_count, clique_size, planted_count):
(4+4k, 9, 2+2k), (8+4k, 6, 6+2k), (3+2k, 4, 2).
```

For every integer `k >= 0`, `b=8+4k`, `K=10+4k=b+2`; the strict margin holds.
These are an asymptotic family calculation, not an inference from timing.

The [official source archive](https://arxiv.org/src/2601.17686v1) contains
30 members. No machine-readable benchmark graphs or generator were found.
In `Results0123.tex`, construction lines 38-42, thinning lines 70-84, and
parameter line 129 support the mapping above.

- Archive SHA256:
  `ade4650cd0b2dac01c4a8a14f2421afc3e2cb7acbcca67379594ef3ed46729c3`
- Member SHA256:
  `6491a5f8c1672d7a8e43f0ded116d7defd3aaa9889f730024acb5e45079018db`

The [older supplement's GIC definition](https://arxiv.org/html/2509.16263v1#S3.SS3)
is broader, describing local-minimum clique structures that may overlap.
It does NOT supply the protected cross-block premise. This proof therefore
does not solve all graphs called GIC there, or settle its general quantum
mechanism. Independent external review remains pending; no author was
contacted and no original graph file was tested.

## New Native Control

`theorems/planted_mis_star_certificate.py` adds a verifier and a new thinning
generator. The recovery algorithm is unchanged. The generator does not
protect the old clique cover.

Saved in `classical_baselines/planted_mis_star_certificate.json`:

- k=7, seed 2026102051; 572 vertices, 38 planted vertices.
- 15 disjoint-star thinning operations, 332 deleted edges.
- 11 edges belonging to the old control's cover were deleted.
- All 65,756 nonedge pairs examined; 465 independent closures.
- Recovered set equals S; block-only bound 36, outside-only bound 37.
- Consequently the returned 38-vertex set is the unique optimum.
- Generation 0.13664s; graph-only recovery 0.08137s; posthoc checking 0.05731s.

Full adjacency, structural witness, thinning operations, solver output,
and certificate are saved. These are local implementation timings on a new
synthetic graph, not a ratio against the paper's different instances/solvers.

## Falsification Controls

- Joining a three-vertex independent planted set to a ten-cycle gives
  perfect separating planted pairs, but the solver returns three while
  an independent set and clique cover certify the true optimum is five.
  Recovery by itself does not imply optimization.
- A deleted triangle across three blocks breaks the star condition and
  permits an outside set tying the planted set.
- A deleted four-cycle across two blocks gives another tie.
- With `K=b+1`, even a valid deleted star can permit a tie. The strict
  margin matters for uniqueness.
- Exhaustive independent-set enumeration checks ten small generated
  controls; all proper subgraphs of the three-outside-vertex deletion
  triangle are also checked. Corrupt graph/partition/target witnesses fail.
- Native replay rechecks the graph, recovery, certificate, single-use
  thinning, final degrees, neighbor restrictions, and broken old cover.

21 new tests and 135 combined focused/scope-audit tests pass. These checks
are implementation/identity controls, not evidence of quantum advantage.
The new cardinality argument is written but not machine-formalized.

## Decision And Remaining Gates

Do not compile a quantum optimization demonstration for this protected
family as an exponential separation. An exact graph-only polynomial
competitor exists under the stated premises.

Do not convert this result into a general non-stoquastic or annealing no-go.
No dynamical simulation, spectral-gap bound, or reduction for the older
broad GIC definition has been proved. The quarantined broad negative stays
quarantined.

Further work here must provide independent review or actual author-file
replay, not another size/seed campaign. A different optimization candidate
must both remove the constant-seed exposure and justify its quantum path;
changing edges until this attack fails is not a quantum algorithm.

## Reproduce

```text
python theorems/planted_mis_star_certificate.py
python -m pytest -q tests/test_planted_mis_star_certificate.py \
  tests/test_planted_mis_pair_closure.py \
  tests/test_campaign_negative_claim_audit.py \
  tests/test_nonabelian_barrier_scope_audit.py -W error::RuntimeWarning
```

No central registry admission, CLI/UI integration, commit, push, or new
agent. The full repository test suite and full Lean build were not run.
Python compilation, site JavaScript syntax, `tools/check_site.py`,
`qsearch.py validate` (valid, no issues), and `git diff --check` pass.
All owned jobs completed.
