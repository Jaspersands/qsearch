# Selected Toric-Code Magic States: A One-Copy Obstruction

30 October 2026. Focused source/application audit. Only this note was written.
No subagents, commits, installations, network writes, or outreach.

## Result

**No surviving Rees application is established.** The concrete family below
has efficient non-oracle preparation, rank one inside an exponentially
degenerate local ground space, a faithful controlled class-four odd-p group,
nonnormal stabilizers, and the GLOBAL gap

    delta = sqrt(1-1/p),       gamma = 1-1/sqrt(p).

Nevertheless, ONE input copy, a public decoder, logical Fourier measurements,
and finite-field linear algebra recover its entire stabilizer. This is a
decisive same-input obstruction for this family, not an impossibility theorem
for arbitrary selected ground states or unknown deep encoders. The competitor
is quantum-assisted, not a classical simulation or a classical lower bound.

The deductions below do not depend on the proposed Rees receiver, the local
growing-prime phase-learning adaptation, or an unimplemented SDE solver.
Status: preparation is an explicit ideal-circuit construction; Sections 3--5
are written proofs under that source contract, not formal verification.
Using Rees on these inputs would remain conditional on its receiver theorem
and implementation. Section 6 reports finite experiments separately. No
hardness or advantage conjecture is advanced.

## 1. Concrete Preparation And Input

Take a supplied prime p >= 5 with p = 2 mod 3, n=4m logical p-level systems
(m>=1),
and a nonzero UNKNOWN row ell in F_p^n. Allow unknown alpha in F_p^* as well.
The logical state is

    |psi_(ell,alpha)> = p^(-n/2) sum_x omega^(alpha*(ell*x)^3) |x>,
    omega = exp(2*pi*i/p).

This is a single cubic magic resource spread across an unknown linear
logical mode. It is obtained by preparing |+>^n, reversibly computing
t=ell*x, applying phase omega^(alpha*t^3), and uncomputing t. This is an
explicit polynomial-size circuit, with O(n) field multiply-adds and a
constant number of field multiplications for the cube. It does not evaluate
a hiding function or prepare a subgroup/coset state. The full-support cubic
phase is nonstabilizer for p>3; the state is not an encoded additive coset
state. A change of linear coordinates exposes one cubic magic state and
n-1 |+> factors, which is precisely the weakness exploited below.

For a physical ground-space realization, use n/2 disjoint square L-by-L
qudit toric codes, L>=3. There are N=n*L^2 physical qudits and n logical
qudits. With consistently oriented star/plaquette Weyl checks S_j, use

    P_j = (1/p) sum_(a=0)^(p-1) S_j^a,
    H_0 = sum_j (I-P_j).

These are commuting four-local projectors, with a gap at least one above
their common kernel. The ground-space dimension is p^n and code distance
is L. Supply a fixed Clifford encoding UNITARY E, including its circuit and
logical coordinates, with

    |Psi_(ell,alpha)> = E (|psi_(ell,alpha)> tensor |0>^(N-n)).

The standard CSS row-reduction encoder has polynomial gate count in N and
log p. No constant-depth preparation is assumed. Increasing L can require
growing geometric depth; routing costs must be charged. These are exact
ideal qudit circuits. A finite universal qubit implementation pays for
field arithmetic, Fourier transforms, and phase synthesis to the requested
total accuracy, polynomially in log p and log(1/error).

The learner receives fresh IID copies, the PUBLIC E and group compiler,
not ell, alpha, the source's mode-computing circuit, its inverse, conjugate
copies, or a state projector. Reversing public E is NOT reversing the unknown
full preparation. It is available to both algorithms. If ell were supplied
as a classical circuit constant, the task would already be classically easy.

Primary physical context: [Bullock--Brennen, qudit surface codes](https://arxiv.org/abs/quant-ph/0609070)
construct local qudit ground-space memories; [Howard--Vala](https://arxiv.org/abs/1206.1598)
study qudit non-Clifford diagonal gates and associated resource states, and
[Campbell--Anwar--Browne](https://arxiv.org/abs/1205.3104) give odd-prime magic
state distillation protocols. The unknown-mode symmetry task and calculation
here are deductions, not claims that those papers propose this application.

## 2. Why The Entire-Ground-Space Filter Does Not Apply

rho=|Psi><Psi| is a SELECTED pure ground state, not the normalized projector
onto ker(H_0). For every operator O supported on fewer than L physical
qudits, error detection gives

    E_0^dagger O E_0 = c_O I,
    E_0|v> := E(|v> tensor |0>^(N-n)).

Thus all selected logical states have identical marginals on those supports.
The group action below preserves the code, so even nonsymmetries with a
constant global trace distance change NONE of these marginals. The parent
energy is zero on both states. Its gap cannot separate one selected ray
from another ground-state ray. Moreover, the supplied physical action is
not promised to be onsite or a physical-site wreath-product action.

The input rank is r=1, despite the exponential dimension p^n of the parent
ground space. Neither the flat-source rank restriction nor the mixed-source
spectral construction is an obstacle here. No spectral-flag machinery is
needed. This genuinely tests the selected-state exclusion in
../../LOW_RANK_SYMMETRY_APPLICATION_FILTER.md.

## 3. Controlled Group And Exact Stabilizer

Let G=UT_5(F_p)^m. Each factor acts on a block of four logical coordinates
by the affine permutation specified by its upper-unitriangular 5-by-5
matrix, using the fifth coordinate as the constant 1. Globally write

    g.x = M_g*x+t_g,      P_g|x> = |g.x>,
    R(g) = E (P_g tensor I_(N-n)) E^dagger.

This is a faithful LINEAR representation on the full physical Hilbert
space, not a projective label family. G has order p^(10m), exponent p,
and class exactly four < p. It is nonmetabelian: E_13 and E_35 belong to
its derived Lie algebra and [E_13,E_35]=E_15 != 0. Central E_15 acts by a
translation, not a scalar. Controlled actions use two public encoding
circuits and O(m) controlled field multiply-adds, with all arithmetic and
synthesis charged. They need not be transversal or fault-tolerant.

The ray/conjugation stabilizer is exactly

    H_ell = {g : ell*M_g=ell and ell*t_g=0}.                 (1)

This follows also from the global-overlap proof below, so there is no
unproved polynomial-identity or phase-character assumption. Here every ray
symmetry actually fixes the vector; alpha does not affect H_ell.

Nonnormal example: ell selects the first coordinate of the first block.
Then that factor's first row above the diagonal must vanish, leaving the
bottom-right UT_4. E_23 lies in its Lie algebra, but
[E_12,E_23]=E_13 does not. Hence H_ell is nonnormal and nonabelian, not just
an abelian-quotient Pauli stabilizer. Other factors are unrestricted.

The relevant research regime is already exponent p. The latest
../../UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md remains the governing comparison
for ring inputs; direct mixed-order machinery adds nothing to this example.
Its ordinary-label oracle result is not silently imported as a copy theorem.

## 4. Proved GLOBAL Orbit Gap

Because p=2 mod 3, cubing permutes F_p, so

    sum_u omega^(alpha*u^3) = 0.                           (2)

Up to complex conjugation, the physical overlap is

    z_g = E_x omega^(alpha*((ell*M_g*x+ell*t_g)^3-(ell*x)^3)).

There are exactly two cases, covering EVERY element of G:

1. If ell*M_g and ell are linearly independent, their evaluations on
   uniform x are independent uniform field elements. Equation (2), also
   after a translation, makes z_g=0.
2. Otherwise ell*M_g=s*ell. M_g is unipotent, so its only eigenvalue is
   one and s=1. Put b=ell*t_g. If b=0, z_g=1. If b!=0, the phase is
   alpha*(3*b*u^2+3*b^2*u+b^3), a nondegenerate quadratic. Its normalized
   Gauss sum has magnitude p^(-1/2).

For clarity, the last magnitude needs no uncharged exponential-sum oracle:
expand |sum_u omega^(A*u^2+B*u)|^2 and substitute u=v+h. The sum over v
vanishes unless 2*A*h=0. Since A!=0 and p is odd, only h=0 remains,
giving squared magnitude p.

Consequently |z_g| is either 0 or p^(-1/2) off H_ell, proving (1) and

    TD(rho,R(g)rho R(g)^dagger) >= sqrt(1-1/p) >= sqrt(4/5).

This is an analytic global promise, not a sampled minimum. The pure-source
overlap gap is gamma=1-p^(-1/2). It is independent of m, L, and ell.

## 5. Same-Input Competitor: One Copy And A Linear Kernel

Apply E^dagger to ONE input copy, discard the known-zero encoding ancillas,
and measure all logical registers in the Fourier basis. For outcome k,

    amplitude(k) = p^(-n) sum_x omega^(alpha*(ell*x)^3-k*x).

Summing over ker(ell) makes this zero unless k=s*ell. On that line it is

    amplitude(s*ell) = (1/p) sum_u omega^(alpha*u^3-s*u).

By (2), s=0 has zero amplitude. Thus the one measurement returns a NONZERO
multiple of ell with probability exactly one in the ideal model. The
distribution along the line need not be uniform. Normalizing the first
nonzero coordinate recovers the projective row [ell]; that is all (1) needs.
No repeated measurement of a chosen slice, postselection, tomography,
controlled R call, or recovery of alpha is required.

To return original-group generators rather than just a membership rule,
embed the affine Lie algebra of G in (n+1)-by-(n+1) matrices and put
w=(ell,0). Solve the PUBLIC linear system

    h_ell = {X in Lie(G) : w*X=0}.                         (3)

There are 10m unknowns. This kernel is a Lie subalgebra, since w*X=w*Y=0
implies w*[X,Y]=0. Also

    w*(g-I)=0 iff w*log(g)=0 iff g in exp(h_ell).

Both implications use the finite exp/log polynomials of degree at most
four, whose denominators are units for p>=5. Exponentiate an F_p basis of
(3). Its elements generate the WHOLE H_ell by the Lazard correspondence,
not just its normal core. All operations are on public matrices and exact
field coordinates, polynomial in m and log p; no enumeration of G or F_p
is used. This argument applies to all m, not merely the finite controls.

Total ideal resources: one physical input copy, one E^dagger, n single-qudit
Fourier measurements, and polynomial classical field arithmetic. Source,
decoder, and measurement errors add to the probability of a wrong sample;
allocate a total <=epsilon to obtain success >=1-epsilon. Input-model
certification is not supplied, just as the Rees source assumes its promises.

This competitor also avoids assuming that a qubit Clifford-product learner
extends to growing-prime qudits. It proves the needed special case directly.
The hidden mode can vary with n, and its stabilizer is not supplied in
advance, so this is an actual learning task, albeit an easy one.

## 6. Experiments, Falsifiers, And Next Action

**Finite experiments, not hardware or a scalable implementation:** an
in-memory Python/NumPy check at p=5 considered ell=(1,0,0,0), (1,2,3,4),
(0,1,2,3), and (0,0,0,1). It exhausted all distinct induced pairs
(ell*M_g,ell*t_g): respectively 625, 625, 125, and 5. These cover the
action of all 9,765,625 group elements for each selected row, without
enumerating all group elements. Counts of squared overlaps (0,1/5,1) were
(620,4,1), (620,4,1), (120,4,1), and (0,4,1).

The overlap test used integer phase histograms h_j and correlations
c_r=sum_j h_j*h_(j+r). All c_r for r!=0 were equal, so the exact squared
cyclotomic sum was c_0-c_1. Fourier checks were floating-point, with mass
on the nonzero ell-line within 4e-16 of one. Exact matrix checks verified
the nonnormality and nonmetabelian commutators. Earlier UT_4 subfamily
controls exhausted 62,500 group/row pairs with the same gap classification.
No physical code encoder, noisy learner, or Rees circuit was executed.

**Decisive falsifiers:** a promised input yielding a Fourier outcome outside
F_p^* ell, an off-stabilizer overlap exceeding p^(-1/2), or disagreement
between (1) and exp((3)) would refute the corresponding deduction. The
prime congruence, nonzero alpha/ell, and known decoder are essential stated
premises; do not drop them while retaining the exact one-copy claim.

**Boundary:** generic cubic polynomials, hidden quadratic scrambling,
arbitrary selected nonstabilizer code states, or an inaccessible encoder
are not solved by this line-support argument. Their absence from this
filter is not hardness evidence. Publicly dressing BOTH the state and
action with a deeper known unitary does not help: the competitor undresses
it at the same charged cost. Cooling alone also does not prepare the
specified selected state; the circuit in Section 1 is the actual source.

**Next action:** reject this single-mode encoded magic family as a reason
to build the Rees receiver. Before budgeting another selected-ground-state
candidate, test its decoded Fourier support and determine whether that
support already fixes the subgroup. Advance only a specifically prepared
family escaping that inference with its own proved global gap. No claim
that such a survivor exists, and no new candidate campaign, follows here.
