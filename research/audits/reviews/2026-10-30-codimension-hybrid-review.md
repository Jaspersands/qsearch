# Bounded-Codimension Hybrid: Independent Review

Date: 2026-10-30. Automated, read-only mathematical review apart from this
authorized record. No descendants, source edits, receiver execution, formal
verification, novelty claim, or new application claim.

## Reviewed Snapshot

- `research/BOUNDED_CODIMENSION_HYBRID_BOUND.md`, SHA-256
  `cd9cad5b0b302f573bfe4fc690b4aa1dccb0ce90e0c54c3a20b6e62f85585b8d`.
- Supporting planner read: `theorems/codimension_hybrid_budget.py`, SHA-256
  `f98cda81bc9c0d93f7df875549a728b46ddcc749f2bcc2e80b2216d7f6116153`.
- Checked the terminal allocation against
  `theorems/uniform_bch_rees.py:symmetric_recovery_budget` and inspected the
  corresponding budget tests without running the repository test suite.

Line references below identify the reviewed note snapshot, not future edits.
At final readback the note hash was unchanged, while the planner had changed
concurrently to `6509eb16e781436133face84c2306ca3a7ba6fc1ec06d681abc3bad280464ba7`.
A limited reread saw explicit oracle-runtime and uniformity metadata added;
this record does not claim a full audit of that later planner snapshot.

## Remaining Clarifications

1. Lines 164-174 need the scope qualifier already present at lines 121-122:
   the profile envelope bounds size-bounded Rees terminals, not every early
   abelian exit. For example, an abelian input of dimension 10 with k=1 and
   p>=P_1 has profile `(10,)`, not one dominated by `(1,)`. Solve any such
   abelian remainder within the at-most-n abelian-call allowance; do not
   send it to the size-bounded terminal envelope. This allowance suffices:
   each earlier intersection call strictly lowers dimension, so a final
   nonzero abelian solve still leaves at most n calls in total. Explicitly
   including that solve in "preliminary abelian calls" resolves the wording
   issue without changing any displayed cap or asymptotic bound.
2. The standalone time expression at line 109 omits label width. Read it
   subject to lines 15-28, or write the non-oracle bound with label width w
   and separately add Q*T_f. This is a local presentation mismatch, not an
   objection to the qualified main statement.

No additional mathematical obstruction to the reviewed composition was found.

## Error Allocations

For 0<epsilon<1, the classical epsilon/3 allocation is valid. With the
note's B, t, a, Q and L, B*(B-1)>=2*p^k. Thus each ideal uniform batch has
collision failure below 1/2 for every unknown actual index J<=p^k, including
the certain-collision case B>J. Slot exhaustion is at most t*2^-a. Conditional
on all ideal slots succeeding, their outputs are independent uniform H
elements. The span-failure bound p^(dim(h)-t)<=2^(n-t) is conservative and
valid. The first-error coupling contributes at most n*Q*2^-L for coordinate
sampling. Each of these three terms is at most epsilon/3. This does not
assert independent uniform draws conditional on the entire capped adaptive
run avoiding all sampling aborts.

The large-branch split is also valid. Put u=ceil_log2(4*n/epsilon).
At most n abelian calls, each using n+u ideal Fourier samples, have combined
rank failure at most n*2^-u<=epsilon/4. Their complete-sampler approximation
gets another epsilon/4. Passing epsilon/2 to symmetric_recovery_budget
assigns at most epsilon/6 each to terminal rank failure, all SDE aborts and
complete-instrument approximation. In particular its terminal slack is
ceil_log2(6/epsilon), not ceil_log2(3/epsilon). Total failure is at most
epsilon. These are complete-process budgets, not success-postselected ones.

Independent standard-library arithmetic checks, executed in memory in this
follow-up, verified five classical allocations and four large-branch
allocations using exact Fraction arithmetic. They did not invoke the planner,
draw source samples, or execute either HSP algorithm. The cases were:

- Classical `(n,k,p,epsilon)`: `(3,3,7,1/3)`, `(10,3,7,1/101)`,
  `(1,1,3,7/8)`, `(32,12,7,1/3)`, `(16,8,101,1/3)`.
- Large branch: `(10,3,2^127-1,1/3)`, `(1,1,1031,1/11)`,
  `(7,2,2^61-1,2^-30)`, `(12,5,2^127-1,7/8)`.

## Profile Envelope And Resource Scope

For a nonabelian nilpotent m-dimensional Lie algebra, r_2<=m-2 and positive
lower-central dimensions strictly decrease. Hence r_d<=m-d for d>=2 and
c_*<=m-1. Together with m<=m_bar and c_*<=2k-1 this proves domination by
the stated envelope, with omitted grades padded by zero. For k=1 there is
no nonabelian terminal; `(1,)` is only the conservative size-bounded
abelian placeholder. The envelope need not be realizable and can exceed
the original input dimension without invalidating its role as an upper cap.

At fixed prime and grade, arities increase with rank. Increasing terminal
sample count, rank, or the number of positive grades therefore only enlarges
the source forest. The bounded classical SDE caps are likewise nondecreasing
in rank and allocated failure bits. Extra envelope grades satisfy the same
field guard because their degrees remain below 2k. Thus the envelope is
usable for conservative source/randomness counts, with the early-abelian-exit
qualification above; it does not supply an actual Lie input or class proof.

The initially inspected planner's quadratic label-comparison cap is a loose upper count, not the
sorting clock establishing the sharper p^(k/2) classical time bound. The
note correctly requires sorting or an appropriately bounded dictionary;
sorting gives the deterministic comparison clock without hashing assumptions.

## Prior Nonnormal Control

The preceding review executed an exact in-memory control on UT_3(F_3), in
coordinates with product `(a,b,c)*(u,v,w)=(a+u,b+v,c+w+a*v)` modulo 3.
The hidden subgroup was the nonnormal H=`{(a,0,0)}`, with left-coset label
`(b,c)`. All 27^3=19,683 ordered three-sample batches were enumerated with
replacement. Selecting the lexicographically first equal-label index pair
gave equal counts for all three H elements for each of the 225 successful
complete label transcripts. Filtering equal selected coordinates instead
removed the identity and left counts 2,025 for each nonidentity element.

This finite diagnostic checks nonnormality, orientation, label-only choice
and retention of identity differences. It is not an asymptotic proof, an
arbitrary-group census, an end-to-end learner, or a quantum receiver test.
The general uniformity argument is conditional on the full labels:
X_i=t_label*U_i with independent uniform U_i in H, so an equal-label selected
pair gives X_i^-1*X_j=U_i^-1*U_j, uniform on H. This control is recorded from
the preceding review execution, not claimed as rerun in this follow-up.

## Final Judgment

The new epsilon/3 classical and epsilon/4, epsilon/4, epsilon/2 large-branch
allocations preserve the reviewed claim. The profile envelope is correct
for its size-bounded terminal role; qualify its wording and explicitly
include early abelian termination in the abelian-call budget as above.
The universal 2^O(k^2 log(k+2)) conditional resource bound, and the large-field
2^O(k log(k+2)) factor, remain supported. The note now explicitly retains
both essential qualifications: uniform growing-class complete-instrument
correctness/efficiency, and the separate Q*T_f oracle evaluation charge.

This judgment does not validate the underlying unverified receiver, prove
its physical gate clock, certify library behavior or primality, extend to
copy-only input, establish classical hardness, or establish priority. No
literature search was expanded in this follow-up. This reviewer wrote only
this review file and changed no generated certificate or source file.
