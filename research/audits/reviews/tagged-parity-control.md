# Tagged-parity descent: one exact nontrivial control

2026-11-13. EXACT FINITE CONTROL ONLY. The proposed tagged map passes this
fixture, including its nontrivial obstruction and its one-dimensional kernel.
No general descent theorem, recursive clock, or tower implementation follows.
No paid report, API, network, Git action, or family scan was used.

Artifacts, relative to research/audits/:

- `controls/tower_recurrence/tagged_parity_control.py`
- `controls/tower_recurrence/tagged_parity_control.json`

The script runs under the Sage Python in TOOLBOX. It uses proof=True class
and squareclass arithmetic as an independent reference, not as an oracle in
the proposed algorithm. Its 26 exact checks all pass.

## Input and the first lower pair space

Use F=Q(a), a^2=−14, L=F(b), b^2=2, S_Q={2,7}. As in the retained
untagged control, Cl(O_F,S)=(2), L/F is unramified, and
dim F(S,2)=4, dim L(S_L,2)=6. Let

    P_1=(3,a+1),   P_2=(3,a+2).

Both are inert in L/F. Write Q_i for the unique L-prime above P_i, and
take the UPPER target J=Q_2 modulo 2. Its norm parity is zero because
the relative residue degree is 2. Therefore the first lower generalized
space is F(S,2) x F_2, with the following independent pair basis:

    (−1,0), (2,0), (a,0), ((a−2)/9,0), (1,1).

All five pairs are norm-compatible. Use the exact norm-class lifts

    beta_1=3(b−1),
    beta_2=b+2,
    beta_3=(a/4−1)b−1/2,
    beta_4=[2(a+7)−(a+10)b]/12,
    beta_5=1.

Their norms are respectively −9,2,a,(a−2)/9,1. The first lower pair space
has dimension 5, although its projection onto element squareclasses has
rank only 4. The pure tag (1,1) is therefore retained as an actual generator.

## Residuals, second lower space, and the exact map

The script computes the upstairs valuations at Q_1,Q_2 directly, then
adds the target parity when the first pair's tag is 1. Pulling these residual
columns to F gives

    R = [1 0 0 0 0]
        [1 0 0 1 1].

For T=S union {P_1,P_2}, the independent base computation gives
dim F(T,2)=5, with basis [3,(a−2)/9,(a+7)/9,2a−5,−1]. Its valuation matrix is

    W = [1 0 0 0 0]
        [1 0 0 0 0].

Thus the obstruction row is exactly [0 0 0 1 1]. The second lower pair
space is ker[W R] in F(T,2) x F_2^5, of dimension 8. The tested map is

    (gamma,u) |-> (gamma prod_k beta_k^(u_k), u_5).

The output tag is kept as a coordinate throughout the linear algebra.
Its image has dimension 7. Its kernel has dimension 1 and, in the recorded
ambient coordinates, equals exactly

    ([2],0,0,0,0,0),

where the last five entries are the second lower tags. In the displayed
F(T,2) basis the full vector is (0,0,0,1,0; 0,0,0,0,0).
It is nonzero downstairs, becomes zero upstairs because b^2=2, and no
additional tag-bearing kernel vector occurs.

## Independent upper reference and the surviving tagged class

Independently compute the complete L(S_L union {Q_1,Q_2},2), of dimension 8,
using Sage/PARI class and S-unit arithmetic. Impose its actual valuation
constraints v_(Q_i)(alpha)=c J(Q_i), retaining c as a ninth coordinate.
The resulting full upper generalized space has dimension 7. The descent
image equals this entire space as an exact binary subspace, not merely by
matching dimensions.

The combination u=(0,0,0,1,1), gamma=1, has zero residual and maps to
(beta_4,1). It survives and has nonzero tag. In contrast (beta_4,0) fails
the upper parity constraint. If the tag is discarded by restricting u_5=0,
the image rank drops to 6. This is a concrete falsifier of forgetting the
pure first-level tag just because its element representative is 1.

The saved JSON records both reference and image matrices, the kernel in
ambient coordinates, field embeddings, generator lists, and every check.
Final run: `EXACT_TAGGED_PARITY_CONTROL_PASS`, 26/26 checks. All norms use
`relative_norm()` explicitly. This control addresses the proposed algebraic
map on one field; it does not address support/height growth or recursive cost.
