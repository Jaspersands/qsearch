# Amitsur Arithmetic: Existing Algorithm And Output Interface

Date: 2026-10-30. Source audit and a constructive conversion lemma. No new
quantum algorithm, general splitting implementation, or broad no-go claim.

## Versioned Prior Art

Kutas--Montessinos, arXiv:2307.00261v3, already treats a split central
simple algebra A isomorphic to Mat_n(k), given by structure constants over
a number field k. Theorem3.10 builds an Amitsur presentation classically;
Theorem4.13 states quantum polynomial-time splitting under GRH. A separable
maximal commutative ETALE algebra suffices. It need not be an irreducible
field extension. The algorithm uses F, F tensor F and F tensor F tensor F,
not a potentially factorial-degree normal closure. This is existing prior
art, not a missing quantum primitive found by this project.
[Versioned full paper](https://arxiv.org/pdf/2307.00261v3).

The arXiv abstract metadata checked on 2026-10-30 still described a random
irreducibility heuristic and 24 pages. The actual v3 PDF and v3 HTML instead
contain the etale construction and GRH theorem above; the PDF has 28 pages.
Do not derive research tasks solely from that stale abstract description.
The cached PDF is `literature_cache/kutas_montessinos_2024_amitsur_v3.pdf`,
arXiv margin date 2024-07-28, title date 2024-07-30, SHA-256
`12bf7b76415bfa96fbfda52c9eec236fb639da103afaf0623e77e7ac0296f5db`.

The proof's arithmetic inputs include S-unit computation and a
class-group-generating prime set; GRH supplies the polynomial-size set.
Do not silently remove that assumption. The etale presentation is the
useful reusable idea: descent can remain in bounded tensor powers even
when the normal closure is enormous.

## A Compact Splitting Map

Let F/k be etale of dimension n and B=F tensor_k F. For an invertible
alpha in B, define the Amitsur coboundary by

```
c_ijk = alpha_jk * alpha_ik^(-1) * alpha_ij
```

in split coordinates. These coordinates explain the identities; the
implementation can use tensor algebras over k, without constructing the
splitting field. The product in A(F,c), on the vector space B, is

```
(x *_c y)_ij = sum_k x_ik * c_ikj * y_kj.
```

Multiplication by alpha sends this product to the untwisted one:

```
alpha_ij * (x *_c y)_ij
  = sum_k (alpha_ik*x_ik) * (alpha_kj*y_kj).
```

The map

```
rho(r tensor s)(z) = r*Tr_(F/k)(s*z)
T_alpha(x) = rho(alpha*x)
```

is consequently an algebra isomorphism A(F,c) to End_k(F). The trace
pairing is nondegenerate because F is etale. This proves the conversion
and its orientation, rather than assuming a cochain is already a matrix
representation. It is the content behind the paper's Corollary3.7 and
Remark3.5.

The preimage of the trace-column left ideal is

```
I_alpha = alpha^(-1)*(F tensor 1).
```

Indeed rho(F tensor 1) consists of maps z -> r*Tr(z), a dimension-n
minimal left ideal in End_k(F). A compact power-product alpha therefore
gives arithmetic circuits for the splitting and a basis of this ideal:
use repeated squaring in the dimension-n^2 algebra, then the trace map.
For polynomial-size factors and binary exponents, the number of circuit
gates is polynomial. This is a representation statement, NOT a bit bound
on evaluating or printing every coordinate. Equality testing and later
operations on arbitrary circuits also need justification.

## A Bad Gauge Can Produce A Huge Minimal Ideal

The following example refutes the shortcut "extracting a minimal ideal
automatically makes the compact answer small." It does not refute the
existence of another small splitting or the cited splitting theorem.

Fix k=Q, F=Q(sqrt(2)), and the constant algebra A(F,1). Put N=2^m and

```
gamma=(3+2*sqrt(2))^N=a+b*sqrt(2),
alpha=gamma^(-1) tensor gamma.
```

Then alpha is a 1-coboundary and delta(alpha)=1. Both gamma and alpha
have O(m)-size arithmetic circuits, and are units with no nonzero finite
divisor support. But the selected ideal is

```
I_alpha=F tensor gamma^(-1)=F tensor (a-b*sqrt(2)).
```

In the fixed tensor basis (1 tensor 1,1 tensor sqrt(2),sqrt(2) tensor 1,
sqrt(2) tensor sqrt(2)), its elements have coordinates
(r*a,-r*b,t*a,-t*b), with r,t rational. Every nonzero vector exposes
the ratio -b/a in one nonzero pair. The Pell identity a^2-2*b^2=1 gives
gcd(a,b)=1, and both a,b have Theta(N) bits. Forming the reduced quotient
of two polynomial-bit rationals could not yield this ratio. Thus ANY
expanded rational-coordinate basis of this particular ideal requires
Omega(N) bits; rescaling basis vectors cannot remove its projective
height. Also T_alpha(1 tensor 1) has entry 2*a^2.

Crucially, alpha=1 is a tiny alternative trivialization of the SAME
constant input cocycle c=1. Algorithm2 is not forced to select the bad
alpha. The example establishes a bad-output-choice obstruction, unlike
INTEGRAL_SIMILARITY_OUTPUT_SIZE.md, which proves a minimum-output bound
over ALL integral witnesses of its explicit input family.

## Interface Still To Check

The S-unit routines cited by the paper return compact outputs; its
Algorithm2 solves in exponent coordinates, then Theorem4.13 invokes the
cochain-to-splitting conversion. The finite-dimensional algebra formulas
alone do not bound expanded output height. We have not certified a general
compact-to-small-ideal normalization or ruled one out. Treat expanded
splittings as an unverified interface in any new reduction until it is
proved, not as a refuted published theorem.

Use the corrected 2025v2 number-field cost analysis when auditing the
S-unit primitive; see ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md.
Do not infer a general lattice solver, division-order PIP solver, or
metric-preserving isomorphism from a split-algebra isomorphism.

The exact algebra controls in `tests/test_amitsur_compact_output.py`
exercise the conversion and the bad-gauge example. They are not an S-unit
solver or quantum execution. A next constructive extension must remove a
specific native obstruction beyond this known arithmetic machinery, and
must specify how it consumes the returned representation.

## Simultaneous Integral Conjugacy Is Not A Free Extension

For explicit tuples A_i,B_i in Mat_n(Z), first test rational simultaneous
conjugacy and, on success, obtain T with T*A_i=B_i*T. This is existing
classical module-isomorphism machinery. Define

```
H = {X in Mat_n(Z): X*A_i=B_i*X for all i},
Omega = {Y in Mat_n(Z): Y*B_i=B_i*Y for all i},
E=Q*Omega,       I=H*T^(-1) subset E.
```

The exact criterion is `I=Omega*alpha` with `det(alpha*T)=+/-1`.
If C is a unimodular intertwiner, H=Omega*C. Conversely a free generator
gives an integral intertwiner but still needs the determinant check.
Generators differ by units of Omega, whose determinants are +/-1.
The linear systems, integer kernels and structure constants have polynomial
bit size: dim_Q(E)<=n^2, with at most n^6 structure constants. This is
an application of the existing Hom-to-principality reduction, not a new
quantum mechanism. See BHJ Proposition8.1 and Sections3,8.
[BHJ full text](https://arxiv.org/html/2202.03526v3#S8).

The safe split-component promise must hold for **E/rad(E)**, the
endomorphism algebra used by the reduction. It must not simply be assumed
from the algebra generated by the input tuple. Even mutually commuting
input matrices do not suffice, as the following exact example shows.

Let D=(-1,-1)_Q be the Hamilton division algebra and let U,V represent
left multiplication by i,j in its basis (1,i,j,ij):

```
U=[[0,-1, 0, 0],       V=[[ 0, 0,-1,0],
   [1, 0, 0, 0],          [ 0, 0, 0,1],
   [0, 0, 0,-1],          [ 1, 0, 0,0],
   [0, 0, 1, 0]],         [ 0,-1, 0,0]].
N(X)=[[0,X],[0,0]],       B=(N(I4),N(U),N(V)).
```

All pairwise products B_i*B_j vanish. Their generated algebra is the
four-dimensional span of I8 and the three B_i, with square-zero radical
spanned by the B_i and quotient Q. Nevertheless, commuting with N(I4)
forces an endomorphism to have the block form `[[P,Q],[0,P]]`.
Commuting with the other two matrices forces P to commute with U and V.
Such P are precisely right multiplications on D, whereas Q is arbitrary.
Therefore

```
E = {[[P,Q],[0,P]]: P in D^op, Q in Mat_4(Q)},
rad(E) = {[[0,Q],[0,0]]: Q in Mat_4(Q)},
dim(E)=20,       dim(rad(E))=16,       E/rad(E)=D^op.
```

The indicated ideal is the entire radical: it is square-zero and the
quotient is a division algebra. The latter fact is not inferred from its
dimension or center. For a nonzero rational quaternion q, its reduced norm
is the strictly positive sum of its four squared coordinates, so
q^(-1)=conjugate(q)/norm(q). The quotient is noncommutative and cannot be
Mat_2(Q), which has nonzero zero divisors.

Thus splitness of the generated-algebra quotient is not preserved on
passing to an arbitrary module's endomorphism algebra. If the generated
algebra is itself semisimple and split into matrix algebras over fields,
its modules decompose into simple summands and the endomorphism algebra
does have split components. That stronger sufficient assumption must not
be confused with a split quotient of a nonsemisimple algebra.

An independent adversarial review checked the example against the actual
BHJ definitions. In that paper a Lambda-lattice need not lie in the
regular module A: `Lambda=Z*I8+sum_i Z*B_i`, `Y=Z^8` satisfy the stated
definition. Proposition8.1 correctly moves the problem to End_A(QY),
and Proposition8.2 must remove the radical of THAT algebra, leaving D^op
here. Algorithm8.3's split-component promise then fails. Thus Remark8.8's
stated derivation needs a qualification for arbitrary modules: hypothesis
(H) on the original nonsemisimple A alone does not justify this chain.
This is a counterexample to preservation of a precondition, not a proof
that no different algorithm with the stated complexity can exist.

Besides semisimple split A, another sufficient case is a rationally free
module QY isomorphic to A^r: its endomorphism algebra is Mat_r(A^op),
which inherits (H). Full lattices in the regular module are covered by
this condition. The single-matrix application separately proves the
needed centralizer property in Corollary9.9/Proposition9.11, so this
tuple counterexample does not invalidate that application through this
particular precondition issue. The separate expanded-output qualification
in INTEGRAL_SIMILARITY_OUTPUT_SIZE.md still applies.

No representation-safe BQP algorithm for arbitrary tuples is established
here. Even under the correct split-centralizer promise, a compact Amitsur
splitting does not automatically supply the expanded lattice-coordinate
maps used by a subsequent algorithm. Noncommutative division components
require further principality machinery. Exact scope controls are in
`tests/test_tuple_centralizer_scope.py`.

2026-10-30 follow-up: [QUATERNION_NORM_SLICE_AND_LOCAL_FLAGS.md](QUATERNION_NORM_SLICE_AND_LOCAL_FLAGS.md)
settles the immediate rational-definite distraction: explicit ordinary PIP
there is classical fixed-dimensional SVP. A division component alone is
not a hard native target. Growing-center exact-norm principalization has
a meaningful weighted approximation interface, but no new solver is
supplied. The [HSVP source audit](QUATERNION_HSVP_PREPRINT_AUDIT.md) must be
read before importing recent quaternion approximation guarantees.
