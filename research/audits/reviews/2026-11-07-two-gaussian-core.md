# Independent core review: two arbitrary Gaussian branches

7 November 2026. Read STATE/TRAPS, the supplied two-Gaussian contract, and
the earlier two-Fock theorem only for scope. **The exact equal-angle
pairing-form operation below is valid. A uniform copy/BIT learner is NOT
proved by this review.** No network, Git, API, implementation, or archive
work was used.

## Exact normal-form scope

In a proof-only frame taking the first even pure Gaussian branch to vacuum,
the second even pure Gaussian branch has the paired canonical form

    tensor_j (c_j |00> + s_j |11>),
    c_j,s_j>=0, c_j^2+s_j^2=1,

and unused vacuum modes. For nonzero vacuum overlap this is the skew-Takagi
form of its antisymmetric Thouless pairing matrix. Zero-overlap endpoints
are included by the occupied canonical modes; even parity makes their
number even, allowing them to be paired. This normal form is existential;
neither inverse branch preparation nor its pairing matrix is input advice.

The local covariance of each physical mode pair represents the Bloch vector
of its even logical qubit and has two equal normal singular values nu_j.
For at least three genuinely active pairs and two nonzero coefficients,
the contract's denominator-free determinant-difference identity implies
that equal nu_j occur exactly at equal c_j. Its factor
1-product_(l!=j,k)c_l^2 is then positive. Cases with at most two active pairs
are constant-size Gaussian-compressible cases. This is an exact grouping
observation, not a lower bound on gaps between approximate groups.

## Small covariance within a large equal-angle group

Consider k>=3 equal-angle pairs, c_j=c, and let R in [0,1] be the vacuum
overlap of all other branch factors. Write A=|alpha|^2, B=|beta|^2 and

    N=A+B+2 Re(conj(alpha) beta) R c^k >0.

Tracing out all but one pair gives exactly

    det(rho_1)=AB(1-c^2)(1-R^2 c^(2k-2))/N^2.

For fixed c,R, this determinant is maximized by equal coefficient
magnitudes and destructive relative phase. Indeed, setting
u=2sqrt(AB)/(A+B)<=1, the relevant factor u/(1-u R c^k) increases with u.
Thus

    nu >= c(1-R c^(k-2))/(1-R c^k)
        >= c(k-2)/k >= c/3.

The first inequality follows by subtracting the maximal 4det from one:
the numerator is the square (c-R c^(k-1))^2. For the second inequality,
the ratio decreases with R, and
(1-c^(k-2))/(k-2)>=(1-c^k)/k. The case c=R=1 is a single Gaussian branch;
an exactly vanishing normalization is excluded, rather than divided by.

This also controls a potential cancellation objection. If c<=1/2, the
global branch overlap is at most c^k<=1/8. After normalization,
(|alpha|+|beta|)/sqrt(N)<=sqrt(2/(1-R c^k))<2. Replacing this group's
second factor by full occupation has vector error O(sqrt(k)c), with no
unbounded coefficient prefactor. Hence small nu can imply a controlled
vacuum/full approximation after a quantitatively chosen threshold. It
does not by itself choose that threshold for all groups in the full run.

## Exact rank-one two-particle RDM

Suppose now the group's covariance magnitude nu is nonzero. Apply the SAME
local even Gaussian rotation to every original pair to diagonalize its
identical local logical density matrix. The group remains permutation
symmetric on its k logical qubits, and its physical covariance is nu J in
a common complex structure. Any other frame normalizing this covariance
differs by a passive U(2k) transformation.

In the symmetry frame let n_j be logical occupation, and set

    p=<n_j>, q=<n_i n_j>, z=<sigma_i^+ sigma_j^->, i!=j.

Permutation symmetry makes z real. The two-logical-qubit reduced state has
no singlet support, so z=p-q>=0. Let R2 be the physical two-particle RDM,
with entries <a_a^dagger a_b^dagger a_d a_c> indexed by increasing pairs.
Pair parity and the symmetry give

    R2=q I+z |Omega><Omega|,
    Omega=sum_(j=1)^k |2j-1,2j>,   ||Omega||^2=k.

Specifically, the k paired diagonal entries equal p=q+z, their off-diagonal
entries equal z, and every nonpaired diagonal entry equals q. All other
entries vanish. Anomalous fourth moments may exist but do not invalidate
this number-conserving RDM identity. Under a passive change of modes R2
transforms by exterior-square conjugation, preserving this form.

If z>0, its unique top eigendirection is Omega and its gap is kz. These
entries are obtained from the measured second/fourth Majorana moments by
polynomial-sized coordinate transformations. This requires no hidden
stabilizer-group generators or generic Lie-algebra decomposition.

## Explicit pair extraction from the eigendirection

Reshape sqrt(k) times a normalized top eigenvector into a complex skew
matrix Z. In exact arithmetic Z Z^dagger=I. Its overall phase is irrelevant.
The antiunitary map

    Theta(v)=Z conjugate(v)

satisfies Theta^2=-I. Choose any unit vector v and put w=Theta(v). Skewness
gives <v,w>=0, and w has norm one. Their span and its orthogonal complement
are Theta invariant. Repeating this operation gives k orthonormal pairs
using ordinary matrix multiplication and Gram--Schmidt. This is a concrete
polynomial arithmetic skew-Takagi construction, without a search over
frames or a supplied inverse.

Both original branches restricted to this equal-angle group were products
of identical two-mode Gaussian factors after the shared local rotation.
Their pair-creation form is Omega. Every symplectic basis obtained above
therefore keeps BOTH branches as products over the resulting mode pairs;
zero-overlap and full-occupation endpoints obey the same conclusion.

## Vanishing or small rank-one signal

Let Nlog=sum_j n_j. Symmetry yields

    <Nlog(k-Nlog)>=k(k-1)z.

Since Nlog(k-Nlog)>=k-1 on occupations 1,...,k-1,

    Pr(outside vacuum/full sector)<=kz.

Thus z=0 puts the entire reduced state exactly in the two-dimensional
vacuum/full sector. Any passive basis preserves that sector, so no pairing
frame is needed. Small z permits a projection with trace-distance cost at
most sqrt(kz), including when the group is entangled with the rest. Such
projection must be paid if used operationally; it is not a free conditional
source. Known-frame vacuum/full checking has a polynomial circuit.

At nu=0 and k>=3, the earlier bound forces c=0. The group is an exactly
balanced vacuum/full sector on 2k physical modes. Its degree-four connected
tensor is W(J), and the earlier two-Fock flattening has top eigenvalue
2k-1 with gap 2k-2. This identifies its complex structure up to sign without
dividing by nu. A nearby-group use requires a separately quantified
perturbation argument. Groups of k<=2 have constant physical dimension;
they must be retained as blocks in a coherent global learner, not replaced
by independently tomographed reduced states that discard relative phase.

## What remains open in this review

The exact multiplicity problem admits the explicit operation above, so an
unpaid compact-stabilizer classification is unnecessary for this gate.
However, learning an exact variance kernel or exact covariance multiplicity
from finite samples is not justified. A whole uniform learner still needs
quantitative grouping/merging of nearly equal covariance values, control
of orientation when nu is small, consistent perturbation bounds through
R2 construction and skew rounding, and a charged coherent supplied-frame
endpoint preserving long-range phase. All thresholds, failed projections,
source samples and numerical bit costs must be included there. This review
does not supply those missing global bounds or claim the full algorithm.
