# Independent Review Accepted

Date: 2026-10-26. This supersedes the pending-review status in the frozen
`FOUR_LIST.md`; its theorem and code did not need mathematical correction.
Read `../auxiliary-four-list-review-2026-10-26/REVIEW.md` for the audit,
source hashes, independent controls and explicit access qualifications.

The reviewer accepted the small-bias success bound, arbitrary target,
unequal distributions, all rank residues, bounded sorted joins and fresh
retries. They also proved the overlap inequality analytically: each low
constraint is a graph edge. If c is the number of components, c_A the
number meeting support A and d the rank of the high columns outside A,
the exponent reduces to(c-c_A)-2d. For d=0,1,2 there can be at most0,2,4
whole omitted components, respectively. Thus the exponent is always<=0;
the1296-case computation is now a regression control, not the only proof.

Independent controls covered5184 Walsh coefficients,20736 confined-support
identities, adverse Fourier signs,7104 exhaustive matcher comparisons,
cap boundaries, and worst-rank levels through e1024. The reviewer also
replayed all36 parent tests. Repeated unbiased entries within one list
give a concrete failure if independence is dropped; do not weaken that
premise or infer it from empirical list balance.

Retain expected-cost wording: the pair cap bounds join work and storage,
not the wall-clock cost of Las Vegas prime generation or divisor arithmetic.
For L=2^ceil(r_2/3), a precise conditional time ledger is

```text
T_pre + (L sum_i T_prime_class_label(n_i)+O(L poly(r_2)))/p_* + T_finish,
p_* =1/8000.
```

T_finish includes rational halving, moving, RR/differential/residue work,
common-basis solving and exact native verification. Backend workspace and
represented divisor sizes are also charged. The original relation and all
its coordinates remain unchanged. No native divisor was constructed here.

For r_2<=2 the helper deliberately has no implementation branch; a constant
search draws one prime of each degree and checks the total label. With
epsilon<=1/4 its success is at least253/1024 for ranks1,2, and automatic
for rank0. This closes the abstract small-rank case, not a missing native
implementation. No polynomial claim follows when r_2 is linear in genus.

The separate sampler-contract follow-on may relax uniform Jacobian access;
it must be read with its own review. This frozen four-list review assumed
the earlier access contract and did not audit that relaxation.
