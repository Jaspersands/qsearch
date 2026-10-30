# Random-Column Rees: Review And Prior-Art Disposition

30 October 2026. Independent automated reviews, not human peer review,
formal verification, priority certification or a quantum execution report.

## Question And Roles

Does replacing worst-case diagonal-equation solving by bounded kernel
sampling on the ACTUAL IID central-character labels improve the complete
parameter bound, after bank failures, recursive source laws, arithmetic
retries, oracle calls and quantum approximation are charged?

- Parent derived the projective second-moment lemma, fixed-width tree,
  whole-tree restart and all-prime compositions; implemented the resource
  planner and integrated the CLI.
- Bohr (`01a188b6-a42b-7c93-a3af-bc7fff021a28`) first audited the nearby
  literature, then independently attacked the complete new derivation,
  including its codimension corollary and arithmetic/controller accounting.
- Confucius (`01a188b6-a4a7-7321-8182-29f23c714947`) separately audited
  codimension transport, intrinsic character rank and accepted-source laws.
- Newton (`01a188be-0660-7b51-8504-5cbeb0a91ef4`) implemented the bounded
  classical sampler and independent exhaustive arithmetic tests. This
  implementation assignment is not counted as an independent proof review.

All three agents were closed after completion. The source derivation is
[Random-Column Rees Parameter Bound](../../RANDOM_COLUMN_REES_PARAMETER_BOUND.md).

## Mathematical Disposition

Bohr found no fatal mathematical error in either proposed all-prime bound:
`2^O(r log(r+2))*poly(input)` for derived dimension r, and
`2^O(k log(k+2))*poly(input)` for hidden codimension at most k. Both retain
the existing Rees pointwise-source and uniform-compilation dependencies.
The review does not certify those inherited theorems.

The main adversarial checks were:

- Count projective directions, not all raw power vectors as independent
  events. Charge row-rank deficiency separately from the second moment.
- Use an unknown intrinsic basis only in the analysis; ordinary ambient
  nullspace computation supplies the same kernel. A measured rank is not
  an IID certificate or a replacement for the intrinsic-rank promise.
- Keep every classical retry on the SAME measured bank. Fresh whole-tree
  attempts, not repeated kernel sampling, repair random bad-bank failures.
- Successful child states must decouple from their complete records
  POINTWISE. An averaged correctness statement would not suffice. A bank's
  own accepted labels are not asserted to remain IID after its acceptance.
- Bound each grade's character rank by k. The entire Rees cover's hidden
  codimension can be the sum of these ranks and is NOT at most k.
- Use a confidence parameter depending on the fixed parameter, not n,
  inside the recursive arity. All 4m attempted trees are paid; their
  flagged aborts are charged through insufficient successes, not silently
  discarded or double-counted as quantum approximation errors.
- The ambient O(k^2) terminal dimension and O(k^3) cover dimension contribute
  polynomial factors. Classical rejection work and tree size multiply once;
  their exponents add rather than recursively multiplying.

Confucius additionally confirmed that complete recovery of h intersect A
is essential in the abelian-ideal reduction. For K=h intersect A and
S=N_L(K), codim in S/K cannot increase. An incomplete K can lose h, not
merely worsen a resource bound. No normality of h is needed for the vector
space injection of each grade quotient into L/h.

## Controller Finding And Correction

Bohr identified a nonfatal integration gap: the sampler initially raised
ValueError for a canonical bank whose observed rank exceeded the supplied
rank promise. Such a record has zero ideal probability but can occur after
quantum approximation. Parent changed this to bounded explicit
`ABORT / OBSERVED_RANK_EXCEEDS_PROMISE` and updated the regression test.

Malformed Python arguments still raise. A future complete compiled
controller must reject noncanonical binary records before invoking this
arithmetic helper. No claim of a complete emitted instrument is made.
Backend corruption remains a distinct error, never a statistical abort.

Bohr could not replay the tests with its default Python because that
environment lacked flint; it installed nothing. Parent and Newton used the
existing `/opt/anaconda3/bin/python` environment. Final test commands and
counts are recorded in the latest [handoff](../../AGENT_HANDOFF.md).

## Bounded Prior-Art Search

This is a checked comparison, NOT an exhaustive novelty determination.
The audit found no direct subsumption of the complete r/k statements in the
following results. Their regimes must remain visible:

- [Ivanyos--Magniez--Santha, Theorem 11](https://arxiv.org/html/quant-ph/0102014v1#S5)
  gives a quantum HSP algorithm polynomial in input size plus the order of
  the commutator subgroup. Here that order is p^r. It supplies exactly the
  small-prime branch when p=O(r^2); alone it is not uniform polynomial in
  log p for growing p. Their normal-hidden-subgroup results do not cover
  an arbitrary nonnormal H.
- [Ivanyos--Sanselme--Santha](https://arxiv.org/html/0707.1260v1)
  solve nilpotency class two. Their reduction to exponent-p instances with
  trivial or order-p hidden subgroup does not itself solve the higher-class
  problem or reduce the ambient central-character rank to one.
- [Imran--Ivanyos](https://arxiv.org/abs/2304.08376)
  establish polynomial time for fixed class and bounded primes. Their
  displayed zero-sum dependence does not supply this uniform growing-prime
  parameter statement. Their access premises must not be silently imported
  as free source preparation or inverse access.
- [Friedl--Ivanyos--Magniez--Santha--Sen](https://arxiv.org/html/quant-ph/0211091v4#S4.SS4)
  provide the smoothly solvable regime and more general bounds. Small
  F_p-dimension alone does not give uniform smoothness as p grows.
- [Ivanyos--Santha diagonal equations](https://arxiv.org/html/1503.09016v2)
  and [Decker et al. semidirect products](https://arxiv.org/html/1107.2189v2#S5.SS2)
  remain relevant to fixed-degree and special semidirect families. A
  reduction of arbitrary subgroups WITHIN those families is already prior
  art, not a novelty of this repository.
- [Morales, v2](https://arxiv.org/html/2608.05321v2)
  concerns structured scalar-action/quasi-Hamiltonian inputs. The checked
  scalar p-power-order action on an exponent-p vector group is trivial;
  this does not subsume the general nonabelian Lie-coordinate setting here.
- [Te'eni--Oz--Cohen, v2](https://arxiv.org/html/2510.10538v2)
  concerns abelian HSP with specified index/output structure. Its one-query
  index distinction is not arbitrary exact recovery of nonnormal H, and
  its stronger recovery conditions cannot be discarded.

The projective second-moment method, root routines and published fallback
are not individually claimed as new. Priority of their composition remains
an external research question. No people were contacted and nothing was
submitted or published during this pass.

## Remaining Decisive Work

1. Check the complete growing-class Rees source/pointwise theorem with a
   quantum algorithms specialist, including its exact input/access model.
2. Assess novelty of the combined all-prime parameter theorem, not isolated
   elementary lemmas or finite controls.
3. Identify an explicit useful classical input with an affordable hiding
   oracle and a serious matched classical baseline. Current application
   negatives remain in force; this bound alone establishes no hardness.
4. Only implement a full circuit backend when it answers a concrete
   correctness or resource question beyond these existing arguments.
