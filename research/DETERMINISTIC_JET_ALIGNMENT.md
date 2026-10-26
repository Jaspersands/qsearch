# Deterministic Public Jet Alignment

2026-10-21. CONSTRUCTIVE PUBLIC-ALGEBRA REPLACEMENT, not a new HSP theorem.
This removes the random transverse-Lagrangian step from the proposed
class-four receiver. The source, rank, scalar-erasure and full-algorithm
proof obligations remain. No hidden potential coefficients are inputs.

## Contract And Target Embedding

Work over F_p, p odd, with carrier V=F_p^(2R), ordered (X,Z), and form

```
[v,v'] = Z.X' - X.Z'.
```

The public maps K:F_p^w->V and J:F_p^D->V satisfy K^T Omega K=0,
rank[K|J]=w+D and R>=D+w. Let k_a and j_i be their columns. Define
C_ai=[k_a,j_i] and H_ij=[j_i,j_j]. Prescribe targets

```
k'_a = (0, sum_i C_ai e_i + e_(D+a)),
j'_i = (e_i, (1/2) sum_l H_il e_l).
```

The indices lie in the R X/Z coordinate positions. Each k' has a unique
extra Z coordinate; each j' has a unique first-D X coordinate. Hence all
w+D targets are independent. Their Gram matrix equals the original one:
[k'_a,k'_b]=0, [k'_a,j'_i]=C_ai and
[j'_i,j'_l]=(H_il-H_li)/2=H_il. Thus the map on the prescribed subspace
is an isometry. Extending it to V gives precisely

```
(SK)_X=0,  (SJ)_X=(I_D,0)^T,  S^T Omega S=Omega.
```

This is an application of classical Witt extension, not a new extension
theorem. For background on its scope, see
[Huang, introduction and alternating-form discussion](https://webhome.auburn.edu/~huanghu/paper/Witt-extension-compositio.pdf).
The explicit algorithm and proof below avoid depending on a black-box
Witt solver or on uniform sampling of a Lagrangian.

Sharper feasibility criterion (written, not used by the current uniform
padding backend): R>=D+w-rank(C) is necessary and sufficient under the
same rank/isotropy premises. Necessity follows because (SK)_Z has rank w,
its first D rows equal C^T, and only R-D other rows are available. For
sufficiency, append w-rank(C) standard-coordinate rows completing C^T
to rank w, instead of assigning every k_a a distinct extra coordinate.
The resulting targets are independent and have the same Gram matrix,
so the extension proof still applies. Thus the conservative R>=D+w
guard is not a general impossibility claim below that threshold. Tightening
padding is lower priority than verifying the remaining source/receiver.

## Extension With At Most Two Transvections Per Column

Process the independent source/target lists in order. Initially S=I.
Suppose S already maps all earlier source vectors to the prescribed
targets, whose span is E. For the next pair put u=S(source_i), v=target_i.
Both lie outside E. Gram equality implies u-v belongs to E-perp.

If u=v, do nothing. If [u,v]!=0, put d=u-v and apply

```
T(x)=x + [x,d]*d/[u,v].
```

Then T(u)=v, T fixes E pointwise, and direct bilinear expansion gives
[T(x),T(y)]=[x,y]. Update S to T*S. This is a rank-one matrix update.

If u!=v but [u,v]=0, obtain a basis of E-perp by linear elimination.
Nondegeneracy gives (E-perp)-perp=E. Since u,v are outside E, neither
functional [u,-] nor [v,-] vanishes identically on E-perp. Find a basis
vector r with [u,r]!=0. If [v,r]!=0, take d=r. Otherwise find a basis
vector s with [v,s]!=0. Take d=s if [u,s]!=0, and d=r+s otherwise.
In every case d is in E-perp and BOTH pairings are nonzero.

Set t=u+d. Its pairings with E agree with those of u and v; also
[u,t]!=0 and [t,v]!=0. Apply the preceding one-transvection construction
first from u to t, then from t to v. Both fix every earlier target.
No enumeration of p elements, search over ambient vectors, square-root
choice or random trial is involved. This proves the inductive extension
even when the prescribed subspace has a nontrivial radical.

For n prescribed vectors there are at most 2n transvections. Recomputing
orthogonal complements by elimination gives a conservative O(n R^3)
field-operation bound, hence O(R^4) here, with polynomial bit cost in
log p. The implementation uses exact arbitrary-precision finite-field
matrices. This count is NOT a quantum-gate bound. Feed the resulting S
to the existing exactly phased prime-Clifford compiler, then charge its
native arithmetic/gate synthesis separately.

## Consequences For The Receiver

The public controller now deterministically succeeds whenever its checked
rank/isotropy/dimension premises hold. A malformed design is rejected;
no random draw can turn a valid design into ABORT. The previous bound for
a random Lagrangian's intersection with im J is no longer a dependency.

For variable-rank carriers it suffices to use
R=max(R0,D+w), instead of max(R0,D+w+2). Needed padding remains a PHYSICAL
maximally mixed channel, not a pure zero ancilla. The unused extra target
coordinates are algebraic positions after S, not a claim that the original
state had pure or known values there.

The same canonical unknown Tq appears in every packet because the target
X images of J are fixed. Constant offsets, radical phases, Z displacements
and spectator outcomes remain in the existing symbolic scalar compiler.
S depends only on public K,J. No hidden coefficients are used to choose it.

The full matrix-attempt failure budget is now at most 3/100+1/p<1/4:
1/100 each for empty nonzero-label slots, capped quartic solving and
remaining exact-field random sampling, plus 1/p for jet rank failure.
There is ZERO alignment failure term. The third 1/100 is retained for
independent nonzero block multipliers, not a deleted Lagrangian sampler.
Drawing from bit strings and accepting 1,...,p-1 succeeds with probability
at least 1/2; cap each of B multipliers at ceil(log2(100B)). Conditional
accepted multipliers are exactly uniform and independent. Their complete
abort probability is at most 1/100. Solver randomness belongs in its own
budget. Approximate quantum operations remain covered by joint channel
error, not by dividing through a successful branch probability.

## Implementation And Evidence Boundary

`ut5_matrix_phase_alignment.extend_symplectic_isometry` implements the
transvection proof. The shared align_jet_maps builds the target embedding,
extends it, and verifies the final symplectic and K/J identities. Both
UT5 and variable-radical controllers use it. Randomness/retry arguments
and the random completion helper are removed, not retained as a fallback.
JetAlignment records a transvection count instead of an attempt number.

New exact controls cover every pair of nonzero F_3^2 vectors, every Sp_2
matrix over F_3 and F_5, prescribed subspaces with nonzero radicals,
full-basis uniqueness, 127-bit arithmetic and rejected nonisometries.
Existing independent quantum-channel, scalar-parameter and Clifford
covariance controls exercise the actual replacement, not just its rank.
These support implementation correctness, not novelty or the whole HSP
claim. The universal proof above is written, not newly formalized in Lean.

Failure criteria: unequal Gram matrices, dependent prescribed vectors,
insufficient target-embedding width, a transvection moving an earlier
target, a field-dependent search, or a phase-inexact Clifford realization.
The padding threshold is sufficient for THIS construction, not a lower
bound against every possible alignment. The full receiver still needs
independent review and a useful application surviving classical attacks.
