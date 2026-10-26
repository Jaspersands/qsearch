# A Graph-Only Classical Falsifier For Protected Planted MIS

Status: constructive classical algorithm and a Lean-checked recovery lemma.
Application to the intended external instance family still requires independent
source-scope review. No quantum simulation, general MIS algorithm, original
author-data reproduction, or novelty claim for seed enumeration.

Follow-up: [source scope and disjoint-star certificate](PLANTED_MIS_SOURCE_SCOPE.md)
removes the synthetic control's extra preserved-cover restriction and proves
unique optimality for a directly checked deletion class with `|S|>b+1`.
It also explicitly excludes the older, broader GIC definition. The original
control and its historical results below are unchanged.

## Why This Pass

The prime-character route supplied a concrete algorithm argument but no useful
external reduction or native advantage. The independent mechanism considered
here is non-stoquastic optimization: can a proposed structured MIS family supply
a meaningful exponential separation through an XX driver? A direct solver for
the measured optimization task is a stronger falsifier than attempting to
simulate the proposed quantum path.

The construction in [Choi, arXiv:2601.17686v1, Section 2.1](https://arxiv.org/html/2601.17686v1#S2.SS1)
starts with clique blocks, joins different blocks completely, and plants an
independent set S by deleting cross-block edges between selected representatives.
Its subsequent thinning removes edges only between non-planted vertices.
This last restriction preserves every edge from an outside vertex to a planted
vertex in a different block. The following proof uses exactly that invariant,
not degree distributions, quantum spectral assumptions, or the number of local
minima.

## Recovery Lemma

Let G be a finite simple graph, S an independent set, and suppose that there
exist a,b in S such that every v outside S is adjacent to a or to b. Define

```
C(a,b) = V \ (N_G(a) union N_G(b)),
```

where N_G is the OPEN neighborhood. Then `C(a,b)=S`.

Proof: independence gives `S subset C(a,b)`, including a and b themselves.
Every vertex outside S is excluded by at least one of the two neighborhoods,
giving the reverse inclusion. No probabilistic assumption is needed.

For protected block planting, take a,b in distinct blocks. An outside vertex
v is either in a's block, in b's block, or in neither. In the first case it
remains adjacent to b, in the second to a, and in the last to both. Thus the
lemma applies. Arbitrary modifications of edges BETWEEN outside vertices do
not change the argument. The blocks need not have equal sizes, and the
algorithm need not know their partition.

If the planted S is maximum, as required by the proposed instance promise,
this gives a maximum independent set. If planting accidentally fails to make
S maximum, the same method still finds an independent set at least as large
as S, but this argument alone does not find the new optimum. These claims
must not be conflated.

### Formal Check

`formal/Formal/PlantedMISPairClosure.lean` proves:

- `recover_from_separating_pair`: the neighborhood identity from independence
  and outside domination by two seeds.
- `recover_from_protected_blocks`: the protected cross-block edge condition
  supplies that domination.

Both compiled under the pinned Lean/Mathlib toolchain. Printed dependencies
are only `propext`, `Classical.choice`, and `Quot.sound`; no `sorry`.
This is a standalone check, not an addition to the central formal audit.
It does NOT formalize Python, complexity, optimality of a planted set, or
the match between an author's prose and unpublished graph files.

## Actual Public Algorithm

The solver accepts ONLY the explicit adjacency bit masks.

1. Enumerate every unordered nonedge {u,v}.
2. Compute C(u,v) from the two public adjacency rows.
3. If C(u,v) is independent, retain it when it is the largest candidate.
4. Return the largest retained set, with a singleton/nonedge fallback.

All pairs are examined; the procedure is not given the successful pair,
planted labels, blocks, clique partition, optimum size, or generator seed.
There are at most n squared pairs. Each closure and independence check takes
at most O(n squared) Boolean adjacency operations, giving O(n^4) time and
O(n squared) graph storage. Bit masks accelerate this straightforward
implementation but are not treated as unbounded unit-cost words in the bound.

Since the true separating pair occurs among the enumerated nonedges, the
solver returns an optimum under the stated promise. It neither needs nor
reproduces the quantum state. Seed/common-neighborhood methods are established
in planted-clique algorithms; see, for example,
[Feige and Grinberg, *How to Hide a Clique?*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol168-icalp2020/LIPIcs.ICALP.2020.44/LIPIcs.ICALP.2020.44.pdf).
The contribution here is the matched structural application and its checks,
not a claim to have invented this general technique.

## Decisive Controls

The saved control is a NEW generated graph, not an author-supplied benchmark.
It uses the Table 1 sizes at k=7: 572 vertices and 38 planted vertices.
The generator performs 15 anchored degree-thinning operations deleting 332
edges, then randomly permutes all vertex labels. The solver receives only
the resulting adjacency tuple.

An additional generator restriction preserves a partition into 38 cliques.
This is an independent, public optimality certificate, not solver input.
For the returned set I, the verifier proves

```
38 = |I| <= alpha(G) <= number of cover cliques = 38.
```

This restriction means the control is not a reproduction of the authors'
unspecified thinning choices. It does not limit the recovery lemma, which
covers arbitrary outside-outside thinning when the maximum-set promise holds.
Uniqueness of the optimum is not needed or claimed.

Saved results, seed 2026102047:

- Setup, graph relabeling and premise checks: 0.20650 seconds.
- Graph-only solver: 0.07847 seconds.
- Separate public-certificate verification: 0.03344 seconds.
- All 65,756 nonedge pairs examined; 437 independent closures.
- Returned set equals the planted set, checked AFTER solving.

These are local Python timings, not a speedup ratio against another
implementation, machine or graph. No quantum execution was performed.
The report retains complete adjacency, output, certificate, and thinning
records rather than only a planted-match flag.

Tests cover all 4,096 outside-edge patterns in a nine-vertex control, shuffled
instances, independent exhaustive MIS checks, corrupt graph/certificate
rejection, and native artifact replay. A ten-cycle supplies an essential
negative control: its optimum is five, but this restricted solver returns
two. Thus passing these tests cannot silently turn the method into general MIS.

## Trying To Disprove The Conclusion

1. **Could thinning hide the planted set?** Not when it changes only edges
   between outside vertices. It leaves the exact separating-pair identity
   intact, even when single-vertex degree information is unhelpful.
2. **Does the solver receive hidden advice?** No. Its single argument is the
   graph. Planting metadata and clique cover are used only for separate
   premise and output checks, and every seed pair is charged.
3. **Could the published instance files differ?** Yes. They were not available
   in the sources inspected. Application to such files is conditional on the
   stated planting rule. Deleting planted-outside edges can break the lemma;
   the tests retain a countercontrol to that extension.
4. **Could another hard family retain the quantum mechanism?** Possibly.
   This result does not prove an annealing no-go, simulate non-stoquastic
   dynamics, or bound any spectral gap. Altered graph families need fresh
   classical analysis AND a justified quantum path.
5. **Does the numeric run prove an asymptotic statement?** No. The recovery
   proof and exhaustive polynomial enumeration give the asymptotic result.
   The run checks implementation and the stated finite certificate only.

## Decision

Do not invest in quantum compilation of the protected planted family as a
candidate exponential optimization separation. Under its written promise,
the graph-only algorithm already solves the requested search task in
polynomial time. This conclusion is much narrower than the repository's
quarantined broad annealing no-go and does not reinstate it.

The substantive follow-up is independent checking of the source interpretation,
or replay on original author files if they become available. No author contact,
external claim, central-registry admission, or benchmark campaign is authorized
by this note. Do not replace the current result with a nearby graph sweep.
To revisit non-stoquastic optimization, specify a useful family whose quantum
path is justified and whose solution is not exposed by constant-size seeds.

## Reproduce

```text
python theorems/planted_mis_pair_closure.py
python -m pytest -q tests/test_planted_mis_pair_closure.py
cd formal
/Users/jaspersands/.elan/bin/lake env lean Formal/PlantedMISPairClosure.lean
```

Verification: 38 focused tests and 114 focused/scope-audit tests pass; the
two Lean statements compile. Full repository tests and the full Lean library
build were not run for this isolated pass.
