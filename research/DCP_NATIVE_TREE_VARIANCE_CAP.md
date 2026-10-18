# Centered Native List-Overflow Bound

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty or speedup claim.
Run `python qsearch.py dcp-native-tree-variance-cap`.

## Result And Why It Matters

The original native tree charged cap256*ceil(M)*k*L by Markov's inequality.
That is sufficient but unnecessarily large. The SAME native moment recurrence
also gives exact variances of intermediate lists. Centered Chebyshev bounds
give a substantially smaller cap while preserving the previously derived
overflow-incident edge bound. This is not an assumption of IID list entries.

Let k=2^a,L=4^b,n=b(a+1), with the previous fixed disjoint physical leaf
families and IID uniform coarse labels. Let Z_r be the size of a FULL,
UNTRUNCATED list at level r before the extra root chunk. Define

    f_0=1, f_r=f_(r-1)^2+(L-1)/L^2.

Then exactly

    E[Z_r]=L, Var(Z_r)=L^2*(f_r-1).

The root graph degree D includes one extra chunk; its second moment remains
M=f_a+1-1/L. Do NOT substitute Var(D) for Var(Z_r).

## Native Proof, Not A Random-List Heuristic

Condition on ALL earlier component chunks and a fixed original assignment x.
The two child lists use disjoint physical columns, so their sizes are
independent under this native source. Every surviving pair of child records
names a distinct physical support. Its signed sum on the next fresh component
chunk is uniform. Two distinct supports give jointly uniform sums because
their signed indicator vectors have a2x2 unit minor modulo4. This statement
uses fresh independent native label components, not independence between
all entries of a list.

If N=Z_left*Z_right candidate tuples survive earlier filters, the next-chunk
indicators are pairwise independent with probability1/L. Consequently

    E[Z_r | earlier chunks]=N/L,
    E[Z_r^2 | earlier chunks]=N/L + N*(N-1)/L^2.

Taking expectations and using E[Z_left]=E[Z_right]=L and
E[Z_left^2]=E[Z_right^2]=L^2*f_(r-1) gives
E[Z_r^2]=L^2*f_(r-1)^2+L-1. This proves the recurrence.
Two-wise uniformity is sufficient. The finite control uses overlapping
weight-two supports whose first, second and fourth sums have an always-even
sum: their entries are demonstrably NOT jointly IID, yet the exact variance
is3 at L4 across all65536 native two-leaf label assignments.

## Centered Overflow And Correlation With Degree

Sum variances over every nonroot node:

    S = L^2 * sum_(r=1)^(a-1) (k/2^r)*(f_r-1).

For public integer C>=L, integer list size gives

    delta=P[ANY overflow] <= S/(C+1-L)^2.

This is Chebyshev plus a union bound; node events need NOT be independent.
Although the executable program truncates intermediate records after flagging
overflow, the first overflowing level is computed from complete lower lists.
Thus its whole-attempt overflow event equals the event that some FULL list
overflows. It is invalid to apply this reasoning while accepting a truncated
attempt or while selecting labels on success.

Let D0=ceil(sqrt(256*ceil(M)*ceil(S))) and C=L+D0-1 for S>0; use C=L when
there are no nonroot nodes. Then M*delta<=1/256. Independently marked
overflow-incident endpoints still cost at most

    2*theta^2*E[D*1_overflow]
        <=2*theta^2*sqrt(M*delta)<=theta^2/8.

The original mutual-isolation mass is at leasttheta^2/2, so accepted coarse
mass is at least3*theta^2/8. Overflow is NOT assumed independent of graph
degree; the Cauchy-Schwarz term is retained. Source noise and higher-label
zero rejection remain separate factors. This is an unconditional native-mean
bound, not a guarantee for each public matrix, seed or conditioned syndrome.

## Scaling And How To Try To Falsify It

For L>=2(k-1), the earlier bound gives M<=3. Also

    f_r <= (1+1/L)^(2^r-1),
    f_r-1 <= (2^r-1)/(L-(2^r-1)) <= 2*(2^r-1)/L.

The middle bound follows by dominating binomial coefficients by a geometric
series, so no floating exponential estimate is needed. Hence

    S < 2*(a-1)*k*L,
    sufficient cap C=O(L+sqrt(a*k*L)).

When k and L are comparable and L>=2(k-1), this cap is only a polynomial
factor above L, not k*L. Combined with a separately verified oblivious join,
the native tree could retain Wagner-like k*L record scaling up to polynomial
factors. This is NOT yet an integrated backend, a quantum/classical separation
or a solution to the physical-width and repeated-descent bottlenecks.

The independent equality-pattern controls explicitly remove the extra root
chunk and recompute exact modulo4 unit ranks. Confusing the graph degree with
an intermediate list would fail these controls. The following invalidate the
proof and must fail admission: label-adaptive leaf families, overlapping
physical leaf blocks, nonuniform/dependent fresh chunks, filters inspecting
future chunks or hash seeds, silent acceptance after overflow, and transfer
to a previously postselected source without its own law. Other constructions
may still work; this bound cannot be borrowed for them without a new proof.

## Integration Boundary

The current full-tree default cap and its existing independent certificate
are intentionally unchanged. This module supplies an exact alternate cap
certificate, not an unreviewed automatic replacement. Gemini can add an
explicit cap-proof selector and an independent rational replay, then compare
both cap recipes with the Cartesian reference and the oblivious backend.
Do not just lower the cap and retain the old proof receipt. The raw partial-
list moment and centered threshold must be attached to the selected cap.
