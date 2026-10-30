# CFI: A Scoped Classical Baseline, Not A Quantum No-Go

**Corrected 2026-10-30.** The previous universal trilemma is withdrawn.
The complete original negative record is preserved, hash-bound, in
`research/registry/quarantined_campaign_negatives.json`. It must not be
reintroduced by a report generator. This correction retains the useful
classical baseline instead of treating the erroneous quantum argument as
evidence that this family is classically hard.

Retained result: isomorphism of these **explicit graphs with a fixed base
degree bound** has a deterministic polynomial-time classical algorithm.
Consequently this task cannot witness superpolynomial classical complexity
versus a polynomial-time quantum algorithm. This says nothing against
polynomial quantum improvements, other computational tasks, or access
models that do not supply the explicit graphs.

No new quantum algorithm or quantum circuit lower bound is established.
The historical command and filenames are retained solely for traceability:

```sh
python qsearch.py cfi-graph-coset-luks-subsumption-barrier
node research/certificates/cfi_graph_coset_luks_subsumption_barrier_crosscheck.js
```

The first command writes the corrected report and applies the reviewed
quarantine. `--no-registry` skips registry mutation. It never registers
the old negative. The bounded executable controls do not run Luks' algorithm.

## 1. The Construction Actually Implemented

Let the base be a finite simple undirected graph with V vertices, E edges,
c connected components and degrees d(v). The constructor
`theorems/cfi_base_family_search.py:cfi_parity_graph_from_base` uses:

- One middle vertex (v,s) for each even binary mask on the edges incident
  to v. There are a(d)=2^(d-1) such masks for d>=1, and a(0)=1.
- Two shared edge vertices (e,0),(e,1) for every base edge e.
- An edge from (v,s) to (e,s_e) for each edge e incident to v.

There are **no** middle-middle edges or edges joining the two members of
a shared pair. The previous proof described both, reversed the degree
assignments, and contained an inconsistent degree sum. Its final cubic
counts happened to agree with the implementation; the argument did not.
The optional twist changes the incidence bit at ONE endpoint of ONE edge.
Changing it at both endpoints is a different operation.

Counting the actual construction gives

    N = sum_v a(d(v)) + 2E,
    M = sum_v d(v) a(d(v)).

Each middle vertex has degree d(v). If the endpoints u,v of an edge have
degrees at least two, each shared edge vertex has degree
2^(d(u)-2)+2^(d(v)-2). At a degree-one endpoint only the zero mask exists,
so that endpoint contributes one to bit zero and zero to bit one in the
untwisted graph. Isolated vertices contribute a single isolated middle.

For a cubic base, E=3V/2, so **N=7V, M=12V**. Middle vertices have degree
three; shared edge vertices have degree four. Their degree sum is
4V*3 + 3V*4 = 24V = 2M. This proof, not finite sample extrapolation,
establishes the identities for every cubic base. Scaling rows require
an even integer V>=4, the possible orders of connected simple cubic bases.

For the degree-four K5 control the correct counts are N=60, M=160 and
maximum degree eight. The previous `degree_bounded_by_four` field silently
meant "at most eight" on that row; it is now a literal four-bound.

## 2. A Faithful Cycle Subgroup

Let B be the vertex-edge incidence matrix over F_2. For x in ker(B), swap
the two shared vertices of edge e when x_e=1 and translate every middle
mask s by the restriction of x to its incident edges. Because Bx=0,
the translated mask is still even. Each incidence edge maps to an
incidence edge. Composition corresponds to binary addition, and any
nonzero x swaps a visible edge pair, so this action is faithful.

Thus the automorphism group contains an elementary abelian subgroup of
order 2^(E-V+c). For a connected cubic base its dimension is V/2+1.
The verifier computes a binary incidence nullspace and checks each
generator's full vertex permutation against the actual adjacency matrix.
This verifies the construction and action on the finite inputs; the
preceding argument proves faithfulness and closure for general inputs.

**No normality in the entire uncolored automorphism group is asserted.**
In fact the universal normality assertion is false. For the untwisted K4
base, use the constructor's zero-based ordering. The automorphism

    p = (1 12)(2 8)(3 4)(5 9)(6 13)(10 14)(17 26)(19 24)(21 22)

conjugates the cycle flip on base edges {01,02,12} to an automorphism
sending vertex 16 to vertex 26. Every original edge-flip subgroup element
preserves the shared pair {16,17} setwise. Thus this conjugate lies outside
the subgroup. The live report records all three adjacency-preserving
permutations as a reproducible counterexample. Normality within a
decomposition-preserving group is a different statement. Nor is the
displayed cycle subgroup asserted to be the full automorphism group.

## 3. The Classical Baseline That Survives

[Luks (1982)](https://ix.cs.uoregon.edu/~luks/iso.pdf) proves that explicit
graph isomorphism is polynomial-time for each fixed valence bound.
Section 3 covers bounded valence. The Introduction, printed page 44,
explicitly declines to justify precise polynomial exponents. We therefore
retain **polynomial time for fixed degree**, not the old unsupported
`O(N^4)` attribution. The group-theoretic method is not merely generic
linear algebra for arbitrary solvable groups.

For cubic bases the expanded valence is at most four; for any other fixed
base degree there is also a fixed expanded bound. The degree must remain
fixed in this statement. If it grows with the input, the theorem supplies
no uniform polynomial with a constant exponent from this argument alone.
Additionally, expanding a degree-d parity gadget already uses 2^(d-1)
middle vertices. Succinct-input variants require a separate access analysis.

Failure of a particular Weisfeiler-Lehman test does not invalidate this
stronger classical comparator. The verifier invokes the published theorem;
its graph enumeration is not an implementation or timing benchmark of Luks.

## 4. Withdrawn Quantum Claims

1. **No factorial single-copy MI formula.** The old report gave a rate
   without a properly specified prior, hidden subgroup ensemble or POVM.
   A small Hilbert-Schmidt overlap is not itself a mutual-information bound.
   For regular coset states rho_H=|G|^-1 sum_(h in H) R_h, the exact overlap
   is Tr(rho_H rho_K)=|H intersect K|/|G|, not the inverse size of an
   involution conjugacy class. Dimensions and normalization matter.
2. **No dimension-to-runtime implication.** A factorial carrier or large
   commutant does not prove an exponential circuit cost, and an optimal
   measurement need not be compiled by dense diagonalization. The prior
   runtime curves were unsupported proxies, not measurements or bounds.
3. **No exhaustive receiver trilemma.** The corrected
   [multiplicity-carrier analysis](COSET_MULTIPLICITY_CARRIER_TRILEMMA.md)
   only proves blindness of specified invariant FINAL effects within one
   conjugacy orbit. Blind intermediate labels can retain informative
   carrier states. This is not intractability of all collective receivers.
4. **No claim that quantum computation is strictly harder.** A quantum
   computer can execute the classical algorithm. Whether a particular
   proposed receiver has additional overhead is a separate cost analysis.

Known hard-ensemble Fourier-sampling and multiregister lower bounds remain
relevant only with their hypotheses verified. They are not a universal
claim about CFI inputs or all quantum algorithms. In particular, these
graphs have nontrivial internal automorphisms; the automorphism subgroup
of a disjoint union must not silently be replaced by a rigid order-two
hidden subgroup.

More explicitly, for two connected graphs X0,X1 with automorphism groups
A0,A1, the union group is A0 x A1 when they are not isomorphic, and
(A x A) semidirect C2 when they are. For equal-sized connected cubic bases,
the subgroup orders are at least 2^(2 beta) and 2^(2 beta+1), respectively,
where beta=V/2+1. The rigid trivial-versus-order-two promise therefore fails.
The [MRS single-copy result](https://arxiv.org/pdf/quant-ph/0501056) and
[HRS multiregister result](https://arxiv.org/pdf/quant-ph/0511148) cannot be
transferred here without a valid reduction of the source and decision task.
Quotienting internal automorphisms is not free: normality within the hidden
union group is not normality within the ambient symmetric group.

The corrected report contains graph counts and actual cycle-generator
checks, not numerical quantum MI estimates or invented time comparisons.
Its false `speedup_claim_allowed` flag means this report establishes no
speedup; it does **not** mean every quantum speedup is disproved.

## 5. Research Decision And Falsifiers

Keep fixed-degree CFI as a control against weak classical baselines. Do
not make its explicit GI decision problem a Shor-level separation target.
For a new nonabelian proposal, specify the exact source ensemble and input
access, normalized states, complete receiver instrument, resource costs,
and a matched classical comparator. Charge conditioning probability and
all basis transformations. Efficient access to a class sum is not yet a
useful decoder, especially when its final measurement is orbit-invariant.

Falsify the scoped conclusions by exhibiting a counting/action mismatch
in this exact construction, a violation of the fixed-valence explicit-input
promise, or an incorrect application of the cited classical theorem.
Success of a carrier-sensitive receiver would not contradict this note:
no general quantum lower bound is claimed.
