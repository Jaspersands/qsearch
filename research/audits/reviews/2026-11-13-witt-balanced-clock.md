# Balanced expanded Witt decomposition: conditional native clock

2026-11-13. Independent composition audit of BALANCED_WITT_EXPANDED_DECOMPOSITION.md.
No API, network, Git, tests, implementation, or archives used. This is a
composition-only proof: (W) is a theorem input, not re-proved here. The
separate stable affine review supplies the constants instantiated below;
its correctness is a separate proof gate. An empty report supplies no evidence.

**Finding.** A constructive, uniform, absolute-affine version of (W) suffices.
Explicit caps below are polynomial jointly in field degree, form rank, and
native bit length. They include all embedded columns and the final isometry.
An existential small-height theorem, or a coefficient-height slope depending
on the field degree, would NOT supply this conditional result.

## 1. Exact required interface for (W)

Fix the ORIGINAL totally imaginary field K, degree N, with the supplied
compatible defining polynomial, integral basis Omega, and arithmetic tables.
Write H(x)=N*h(x), the extensive logarithmic absolute height, H(0)=0.
For every nonsingular symmetric form of rank <=8 over K, (W) must return
an EXPANDED matrix V and core C with

    V^T Q V = HYP^w directsum C,  HYP=[[0,1],[1,0]],
    C anisotropic, rank(C)<=4,
    sum H(entries of V and C) <= C0*sum H(entries of Q)+P0.

Here C0>=1 is a known ABSOLUTE integer, and P0>=1 is a computable polynomial
bound depending only on the original charged field data. In particular P0
cannot be reinterpreted as an uncontrolled function of a coefficient-dependent
auxiliary field at the next tree level. The routine must be uniform in K,
with a supplied computable polynomial all-branch BIT/gate/workspace bound
R_W(L,k) on inputs of bit length <=L and error <=2^-k. Exact arithmetic
identities and output sizes can be checked; anisotropy correctness is part
of its error contract. Its norm/order/auxiliary-field work is charged, with
front-end auxiliary degrees <=4N and EXPANDED return values in K. Internal
fields of the imported scalar-norm backend have its own polynomial bound;
they are NOT all asserted to have degree <=4N.
This spells out the needed assumption; it does not prove any of these gates.

All height bounds below are integer upper bounds. Rounding C or P upward
to C0,P0 is harmless. Constants/functions in (W) must be effective to obtain
the requested explicit caps; a bare statement that such constants exist is
not an effective cap specification. The stable
2026-11-13-witt-affine-height.md supplies the following instance. Let ell(m)
be positive-integer binary bit length, Delta=|disc K|, and let M_K be the
largest absolute integral multiplication-table entry. Put

    W_K=N*max(1,M_K), F_K=10+ell(Delta)+4N^2+N*ell(2N W_K),
    C0=128*(43000000*3^12288)^4,       P0=C0*F_K.

Its bound is exactly C0*(H_in+F_K), in natural extensive logarithmic height.
C0 is an enormous but absolute integer; F_K is polynomial in the ORIGINAL
field input, since only bit lengths of Delta and W_K occur.

## 2. Intrinsic heights give computable ORIGINAL-basis bit caps

The integral multiplication matrices have all conjugate eigenvalues bounded
by W_K. Hence B_O=N*ell(W_K) bounds max H(omega_i). Let Omega* be the
trace-dual basis, obtained by inverting T=(Tr(omega_i omega_j)). Its integer
entries satisfy |T_ij|<=N W_K^2 and |det T|=Delta. Minor bounds therefore
bound each entry of T^-1 in rational height by

    R_T=ell(Delta)+4N*ell(2N W_K),
    B_*=N^2*(R_T+1)+N*B_O >= max H(omega_i*).

These are explicit polynomial field-only bounds, requiring no embeddings,
exact Weil-height oracle, or supplied dual-basis advice.

If x=sum r_i omega_i, then r_i=Tr(x omega_i*) is rational and

    h(r_i) <= H(x)+H(omega_i*)+log N.

Indeed the trace is a sum of N conjugates, each of height h(x omega_i*).
Consequently each reduced numerator AND denominator has bit length at most

    b(H0)=4+2(H0+B_*+N)       whenever H(x)<=H0.

This is an explicit polynomial original-coordinate cap. It is NOT applied
as an N-dependent coefficient-height multiplier inside the tree recurrence.
Conversely, if the input coordinates have numerator/denominator lengths <=B,
the computable bound H_Q=N^2(B+1)+N B_O bounds every original Gram entry.

## 3. One growing-rank diagonalization with polynomial caps

There is no need to estimate d successive dense change-of-basis products.
Choose original-coordinate vectors v_i from {e_j,e_j+e_k}. Having chosen a
nonsingular span of v_1,...,v_(i-1), use its exact Gram inverse to test the
orthogonal projection of these candidates. Some projected norm is nonzero:
otherwise all diagonal and off-diagonal entries of the residual quadratic
form vanish, contradicting its nonsingularity. This also proves v_i is
independent of its predecessors. Each search tests at most d(d+1)/2 vectors.

Let G_i=(v_j^T Q v_k)_(j,k<=i). Its entries are sums of <=4 original Gram
entries, so put H_G=4H_Q+2N and

    mu=d^2(H_G+N+1),       H_S=4(d+1)mu.

Every minor of size <=d of these Gram matrices or their Cramer replacements
has height <=mu: for a k-by-k determinant, the bound is sum of the k^2
entry heights plus N log(k!), rather than an erroneous factorial sum bound.
Define

    u_i=v_i-V_(i-1) G_(i-1)^-1 V_(i-1)^T Q v_i.

Cramer's coefficients have height <=2mu. Thus each entry of S=(u_1,...,u_d)
has height <=H_S, and its diagonal coefficient is det(G_i)/det(G_(i-1)),
of height <=2mu (det(G_0)=1). All computations are ordinary exact field
linear algebra with polynomial minor bounds. This handles zero initial
diagonal pivots and uses no isotropic-vector oracle or prescribed permutation.

## 4. Balanced merging: explicit joint-polynomial recurrence

Each nonzero diagonal line is an anisotropic leaf. Work first in these
diagonal coordinates; leaf embedding columns have height zero. Let h_j bound
the SUM of core coefficient heights at level j, and g_j the MAXIMUM height
of ONE coordinate in an embedded active core column. Two children supply
a block-diagonal form of rank <=8 and coefficient height <=2h_j. By (W),

    h_(j+1) <=2C0 h_j+P0,
    H(each merge coefficient) <=2C0 h_j+P0,
    g_(j+1) <=8g_j+8(2C0 h_j+P0)+N log 8.

The last inequality is a sum of at most eight products; no d-coordinate
height sum is fed back. Set

    U0=max(2mu,P0,N,1), a=16C0+32, k=ceil(log_2 a),
    ell=ceil(log_2 max(1,d)), Gcap=a*d^k*U0       (d>=1).

Induction gives h_j,g_j<=a^j U0. Indeed the third right side is at most
(16C0+19) times max(h_j,g_j,P0,N,1), and the first is smaller. Since
a^ell<=a*d^k, Gcap bounds every core and every emitted column coordinate.
The exponent k is ABSOLUTE. Replacing C0 by a function of N would invalidate
the asserted joint-polynomial inference.

Use pairwise balanced levels, passing an unmatched child through unchanged.
There are <=d-1 merges and depth <=ell, with no zero-form padding. An empty
core is skipped, and two empty cores need no call. Previously emitted
hyperbolic pairs are orthogonal to all surviving cores and to the other
child's whole space; keep those columns unchanged forever. At a merge,
transform only the <=8 active core columns. New hyperbolic and core columns
both satisfy the displayed bound. No packet of old hyperbolic columns is
repeatedly multiplied by later changes of basis.

Storing the full emitted basis uses d^2 field entries; even retaining every
historical core embedding uses O(d^2) entries. Sparse embedding updates use
O(d) field operations per merge. Final ordering of hyperbolic pairs is only
a column permutation. Multiply by S ONCE to return to original coordinates;
the resulting decomposition matrix P has entry heights at most

    H_F=d(H_S+Gcap)+Nd.

The factor d appears once, outside the depth recurrence. The final identity
P^T Q P=HYP^w directsum C is checked exactly. The d=0 form has the empty
basis; d=1 already has its anisotropic diagonal leaf.

## 5. Core matching uses (W) alone

For two forms, first reject unequal dimensions and then unequal Witt indices.
Their correct anisotropic cores C_A,C_B have common rank r<=4. If r=0,
use the empty core map. Otherwise call (W) ONCE on C_A directsum (-C_B),
of rank <=8. If it is not hyperbolic, the cores are not isometric; Witt
cancellation therefore certifies NO for the original forms.

If hyperbolic, take one isotropic column from each canonical hyperbolic
pair of its returned basis and write the resulting 2r-by-r matrix as [X;Y].
Both projections are injective: a vector in ker(Y) would give an isotropic
vector in C_A, hence Xv=0 and then v=0; similarly for X. Therefore

    X^T C_A X=Y^T C_B Y,   T=X Y^-1,   T^T C_A T=C_B.

This pays core matching without a new represented-value or hyperbolic-branch
primitive. Put A_match=2C0*Gcap+P0. Its small matrices have entries of height
<=A_match; determinant/minor bounds in rank <=4 and one product give the
safe cap H_T=160(A_match+N+1) for every entry of T. A zero projection
determinant on an erroneous branch causes ABORT, never an invented NO.

If P_A^T A P_A=HYP^w+C_A and P_B^T B P_B=HYP^w+C_B, return

    U=P_A*(I_(2w) directsum T)*P_B^-1.

This orientation gives U^T A U=B. Compute the growing inverse and products
only at this final step. With H_I=2d^2(H_F+N+1), inverse entries have height
<=H_I; the following loose computable cap bounds every final U entry:

    H_U=(d+1)^2*(H_F+H_T+H_I+N+1).

Check U^T A U=B exactly; nonsingularity of B then also verifies invertibility.
No integral-isometry conclusion is made.

## 6. All-branch caps, errors, auxiliary fields, and cost

The constants above also supply an explicit rejection policy. Let H_*=H_U
(the harmless matching bounds may be precomputed even for decomposition
alone), and cap every returned/recursive-state K-entry by b(H_*) rational bits
per coordinate. Check shape, rank <=8/4 as appropriate, finite denominators,
invertibility of each claimed basis, nonsingularity of every nonempty core,
and exact basis/Gram identities before feeding a return into another node.
On a correct run these caps never reject. On a wrong run they need not
imply the intrinsic height recurrence: their role is to keep every next
input bounded. An oversize, inconsistent, or malformed return causes ABORT.
These affine caps apply to SHORTENED returns and propagated caller data,
not every internal register of (W). In particular a raw first expanded norm
witness may exceed them: it is processed under that backend's separate
polynomial current-input cap, then shortened before crossing this interface.

One conservative fixed-rank request size is

    L_*=S_K+1024 N*(b(H_*)+1)+ceil(log_2(4(d+1)/eta))+1024,

where S_K includes all original field data. Cap each call at the specified
R_W(L_*,ceil(log_2(4(d+1)/eta))). Reject oversize interface streams before
expansion. For completeness, caller arithmetic admits a direct coarse cap.
Use the displayed projection algorithm with one prefix inverse per stage;
<=100(N+d+8)^6 field operations cover it, the tree, and the final checks.
An accepted erroneous return can have intrinsic height larger than H_*.
The converse bound in section 2 gives H_bad=N^2*(b(H_*)+1)+N*B_O for each
accepted coordinate-capped field entry. Fraction-free/minor bounds therefore
give the all-branch working cap B_w=b((N+d+8)^4*(H_*+H_bad+N+1)).
This also covers intermediate computations immediately before a cap rejection.
An elementary field operation
uses an N-by-N rational solve at worst. Clearing its denominators and using
fraction-free elimination gives <=100(N+1)^4 integer operations on at most
L_int=16(N+1)^4(B_w+S_K+1) bits. Schoolbook arithmetic and naive Euclidean
gcd can each be bounded by (L_int+1)^3 elementary bit steps after fixed
constant slack. For example the resulting caller cap is

    R_caller=10^4*(N+d+8)^6*(N+1)^4*(L_int+1)^3.

The important assertion is this explicit polynomial bound, not its loose
exponent. Input reading, coordinate normalization and output are included.

There are <=d-1 calls for one decomposition and <=2d-1 for two decompositions
plus comparison. Give each error budget eta/(4(d+1)). Uniform conditional
correctness on every valid expanded input permits the union bound even for
adaptive calls; total backend failure is <eta. Negative answers rely on
this correctness event; an exact positive isometry is additionally verified.
No unexpected norm NO is retried automatically. Repeated native backend
invocations may use fresh randomness rather than reuse unverified advice.

Every call has the ORIGINAL K as its base. Front-end extensions of degree
<=4N are computed and discarded inside (W), never used as the next level's
base. Internal fields of the imported complete norm backend retain its own
polynomial bound, not the number 4N. All field tables, orders, discriminants,
and GRH assumptions are paid by (W)'s native contract. No tower follows ell.
Combining the call bound, R_W, and the displayed field-coordinate caps gives
polynomial BIT/gates/workspace/output jointly in N,d,native bits,log(1/eta).
All composition obligations close under the constructive absolute-affine
(W) interface, instantiated above. Its separate proof and imported primitive
proofs are not independently re-proved by this composition audit. No integral,
real-field, practical, implementation, novelty, or speedup conclusion follows.
