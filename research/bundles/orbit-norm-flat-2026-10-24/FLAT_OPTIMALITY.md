# All Base-Field Linear Norm Flats Have The Same Sharp Bound

2026-10-24. LOCAL UNREVIEWED DEDUCTION. This addendum supersedes the
suggestion in RESULT.md to look for larger non-extension-linear flats.
It does not change that file's classical algorithm, input, or receipt.
It is not a classical hardness theorem or a quantum speedup result.

## Statement

Keep the original cubic-orbit input and its notation. Let c_i be the last
point of orbit i, a_i=h_(c_i)*b_i != 0, and 1<=r<M. On F_p^(2M) define

    q_j(x,y) = sum_i a_i*c_i^j*(x_i^2-nu*y_i^2),  0<=j<r.

For ANY F_p-linear subspace U on which every q_j vanishes identically,

    dim_Fp U <= 2*floor((M-r+1)/2).

No closure under multiplication by theta, GRS form of U, or randomness
assumption is required. The norm-scaled polynomial construction in
RESULT.md attains this bound. Hence the bound is sharp for all such U,
not just the earlier extension-linear ansatz.

## Elementary Proof

**Support lemma.** For u=(x,y) in U, put
v_i=a_i*(x_i^2-nu*y_i^2). The r moment equations say V v=0, where
V_(j,i)=c_i^j. Every set of at most r columns of V is independent, by the
Vandermonde determinant. Thus any nonzero v has support at least r+1.
Anisotropy is essential: since nu is a nonsquare, v_i=0 if and only if
(x_i,y_i)=(0,0). Every nonzero u therefore has block support at least r+1.

**Choose one dual form.** Choose ANY r-1 coordinate indices T, and set
f(X)=product_(i in T)(X-c_i). Its degree is r-1, so

    q_f = sum_j f_j*q_j = sum_i a_i*f(c_i)*(x_i^2-nu*y_i^2)

also vanishes on U. Its active coordinates S are exactly the complement
of T; write s=|S|=M-r+1. Projection U -> F_p^(2S) is injective: a vector
in its kernel would be supported on only r-1 blocks, violating the
support lemma. The projected space is totally isotropic for the
NONDEGENERATE form q_f restricted to S. Polarization is valid since p
is odd. These assertions include all basis-pair cross terms.

**Dimension and determinant.** Nondegeneracy first gives dim U<=s.
If s is odd, dim U=s is impossible. Indeed, an s-dimensional totally
isotropic subspace in a nondegenerate 2s-dimensional symmetric form
extends to a basis in which the Gram matrix is

    [ 0  C ]
    [ C' D ],   C invertible.

Its determinant is (-1)^s*det(C)^2. On the other hand the diagonal norm
form has determinant

    (-nu)^s * product_(i in S)(a_i*f(c_i))^2.

Equality of square classes would make nu^s a square, contradicting odd s
and nonsquare nu. Thus dim U<=s-1 for odd s and <=s for even s, exactly
2*floor(s/2). The construction in RESULT.md has that dimension, proving
sharpness. There is no genericity assumption or unproved rank heuristic.

The usual interpretation is the Witt index of a sum of scaled anisotropic
norm planes. The proof above spells out the needed upper bound rather
than relying on a classification black box. For background on totally
isotropic subspaces and Witt theory see
[Pete L. Clark's notes](https://people.reed.edu/~ormsbyk/kgroup/resources/Pete_Clark_Quadratic_Forms.pdf).
No novelty is claimed for these ingredients or the resulting application.

## Consequence For The Actual Remaining Question

At p12289,M4096,n9828, r2460 and s1637. EVERY such flat has dimension
at most1636. A linearized r-by-D system therefore cannot have full row
rank on any of them. Dropping extension-linearity cannot repair the
current all-right-hand-sides completion method. This conclusion does not
depend on a failed search, field size, random seed, or the choice of U.

This does NOT rule out a consistent particular right-hand side in a
rank-deficient slice. It does not rule out nonlinear parameterizations,
adaptive halfset targets, multiple coupled slices, or other classical
algorithms. It also does not prove a complexity separation. The original
rate0.8 input remains unresolved, not hard or unsatisfiable. The quantum
proposal still needs its complete implementation/resource proof and a
meaningful natural-problem reduction.

## Attempts To Break The Argument

- A non-extension-linear restriction of the known flat still satisfies
  the bound and projection test. The proof does not silently reintroduce
  theta-closure.
- Replacing nu by a square destroys the support lemma: x_i=y_i, nu=1
  yields an M-dimensional common flat. This exceeds the claimed bound
  in the p19,M6,r3 control. Such inputs must be rejected.
- Zero weights or repeated c_i destroy nondegeneracy or the Vandermonde
  distance step. The certificate rejects both. They are not present in
  the original task.
- Checking only individual basis vectors would miss mixed quadratic
  terms. The certificate checks the entire restricted Gram matrices.
- The parity of s matters. Using only half the ambient dimension would
  incorrectly permit an extra dimension when s is odd.
- The proof concerns simultaneous quadratic-zero DIRECTIONS after fixing
  target values. It is not a restriction on every affine or nonlinear
  representation of the original solution relation.

## Bounded Handoff

Integrate this as a scoped mechanism limitation beside the earlier
high-rate classical falsifier, after verified migration. Do not enqueue
larger-F_p-flat search as the next task. Do not turn the bound into a
hardness label or automatically promote the quantum candidate.

The next useful classical question is whether target flexibility removes
the residual consistency equations when D<r. For a given center, a left
annihilator L of its r-by-D derivative matrix gives the exact remaining
condition L*Hz*t = L*(b_norm_syndrome-Hx*x0-Hy*y0), with t_i in F_i.
Analyze that SAME explicit halfset/linear-system problem, its access
model, and its structure before invoking a generic solver or timeout.
This equation is a reformulation, not a new efficient solver. Compare its
constraints with existing OPI, moment-masking and norm-pencil work to avoid
repeating those passes. A natural-problem reduction remains an independent
high-value alternative if this line supplies only barriers.
