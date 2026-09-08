# Signed-Tensor Access Audit

## Question and Decision

Can the known signed-tensor centralizer algebra provide a usable basis for
the K_m=C2 wr S_m types required by a typical Specht restriction?

Not by staying in its faithful even-diagram range. The necessary K-type
coverage of tensor degrees at most m vanishes exponentially under the
project's exact h-even source marginal. This is not a lower bound against
physical signed-tensor circuits, nonfaithful quotients, other tensor
alphabets, or implicit multiplicity registers.

## Literature Contract

[Orellana, Theorem 2.1 and Section 3](https://math.dartmouth.edu/~orellana/hcentpart.pdf)
studies tensor powers of the m-dimensional **signed permutation** module.
Tensoring moves one box from either bipartition component to the other.
The centralizer has an orbital basis indexed by even set partitions,
omitting those with too many blocks. This is not a theorem identifying
that centralizer with End_K(Res_K V_lambda), nor a quantum embedding.

The source-coverage derivation below is the project's calculation. It needs
independent review; finite exact regression checks are not formal proofs.

## Exact Tensor Degree

Write a=|alpha|, b=|beta| and a_1=alpha_1 (zero for empty alpha). Define

    w(alpha,beta) = b + 2(a-a_1).

The trivial representation starts at ((m),()) with w=0. Every cross-component
box move changes w by exactly +1 or -1. Reaching (alpha,beta) therefore
requires at least w steps. This is stronger than counting just the boxes
outside the initial first row.

The bound is achievable. First move b boxes from the initial alpha row into
beta in a Young-tableau order. For each desired alpha box below its first
row, move one box from that row to a temporary addable beta corner, then move
it back into the desired alpha corner. All intermediate shapes are
partitions, and the total number of moves is b+2(a-a_1). Thus the shortest
tensor degree equals w. Its parity is b mod 2, as required by the central
involution. The implementation cross-checks this against the entire
bipartition Bratteli graph and sum of dimension times multiplicity at each
degree on finite ranks.

## Faithful Diagram Range

An orbital even partition of 2k positions has at most k blocks. Its matrix
is nonzero precisely when its blocks can receive distinct labels in [m].
For k<=m, every such matrix is nonzero, and their disjoint supports imply
linear independence. For k>m, the orbital partition with k pair blocks is
zero, producing a nontrivial relation in the abstract diagram algebra.
The usual equality-only diagram basis is related to the orbital basis by
invertible triangular inclusion-exclusion over even coarsenings.

Consequently the faithful range is k<=m. We deliberately do not treat the
paper's stronger sufficient n>=2k condition for a convenient stable label
description as a necessary faithfulness condition. That would overstate
the obstruction.

## Natural Source Coverage

The existing branching source law has K-marginal

    q(alpha,beta) = 2 d_(alpha,beta)^2 / (2^m m!),  b even.

Equivalently A=a is Binomial(m,1/2) conditioned on m-a being even; conditional
alpha follows Plancherel measure on S_a. To occur in some tensor degree <=k,
the degree formula requires

    alpha_1 >= ceil((m+a-k)/2) = L_a.

Under RSK, alpha_1 is the longest increasing subsequence of a uniform
permutation on a letters. The expected number of increasing subsequences of
length L is binom(a,L)/L!. A union/Markov bound gives

    q{w<=k} <= sum_(m-a even) binom(m,a)/2^(m-1)
                 * min(1, binom(a,L_a)/L_a!).

Use probability one when L_a<=0 and zero when L_a>a. The implementation uses
exact rational arithmetic, including the parity conditioning. At k=m the
upper bounds are approximately 2^-10.52 for m=64, 2^-37.56 for m=128 and
2^-105.48 for m=256. These are upper bounds, not estimates of actual mass.

For the asymptotic conclusion, split at a=m/4. The binomial lower tail is
exponentially small. On the remaining event, L_a=ceil(a/2), and the
increasing-subsequence bound decreases as exp(-Omega(m log m)). Their sum
is exp(-Omega(m)), including the factor of two for even parity.

This counts only which K-types can appear. It is optimistic: a useful
embedding must also preserve each required multiplicity space and have an
efficiently implementable normalized intertwiner.

## Attempts to Refute It

- **The small controls cover nearly all source mass.** True at some ranks;
  the exact rank-six coverage is 3743/3840. This is precisely why asymptotic
  source accounting matters. The finite controls do not justify a limit.
- **Use degrees greater than m.** Allowed, but then the abstract even-diagram
  representation has a kernel. The physical tensor space is still valid.
  A source-aware quotient transform is the unresolved task, not an impossibility.
- **Use the unsigned permutation module or a mixed tensor alphabet.** This
  changes the branching graph. Recompute the degree and coverage bounds;
  do not transfer this signed-only result.
- **Avoid explicit tensor embedding.** Also allowed. Bounded-support orbit
  averages can be studied on an implicit copy register without first
  constructing a signed-tensor basis. A decoder still needs a target effect
  and end-to-end access and normalization accounting.
- **Postselect convenient K-types.** This changes the source law and pays
  the probability cost unless an additional preparation reduction is supplied.

## Next Experiment

Compare two precise contracts: a multiplicity-preserving Specht-to-signed-
tensor intertwiner in the k>m physical quotient, and a task-specific effect
on implicit copy registers. Charge the source preparation and normalization
before considering finite numerical spectra. Neither a diagram presentation
nor algebra generation alone is a coherent compiler.
