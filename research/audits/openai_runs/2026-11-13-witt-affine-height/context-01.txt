# Balanced expanded Witt decomposition

2026-11-13. New candidate, NOT admitted. Start STATE/TRAPS, then corpus
been-tried/baselines for balanced Witt decomposition and actual primary
sources. The previous ternary INTEGRAL-isometry seed remains open; this is
a different native output over a field, not a claim that its gate disappeared.

## Problem, mechanism, and reason to test it

Native input: a totally imaginary number field K of growing degree N,
explicit compatible defining polynomial/maximal-order basis/table, and a
nonsingular symmetric d-by-d matrix Q over K, expanded binary coordinates.
Output a FULL EXPANDED basis W with W^T Q W equal to a sum of canonical
hyperbolic planes and an anisotropic form of rank <=4. Both N,d grow. A
subsequent exact rational isometry of two such forms is a possible endpoint;
integral isometry, real-field extension, short lattice witnesses, novelty,
hardness, implementation and quantum execution are not claimed.

Target quantum polynomial(native bits,log(1/eta)) BIT/gates/output under
the explicit GRH of the admitted scalar norm backend. The expected benefit
is replacing the same classical class/unit/norm arithmetic by known quantum
arithmetic. No proven classical lower bound or asymptotic separation follows.
Supplied quadratic towers retain the stronger existing ERH factoring baseline.

The new norm-residue operation first upgrades the existing single-five-plane
isotropic-vector construction to expanded output: only one constant-rank
quaternion splitting and its fixed-size descent follow the expanded front end.
This is a direct consequence, not a reason to spend another paid confirmation.
The NEW operation to test is height-controlled composition of many such calls.

Diagonalize once. Each leaf is a one-dimensional form. At each node merge
the two surviving anisotropic cores, of total rank <=8, and split off all
hyperbolic planes. Carry only the new core of rank <=4. A balanced tree has
depth ceil(log2 d). The bound on anisotropic rank uses the totally imaginary
number-field Hasse principle and finite u-invariant4; it fails over real fields.

The decisive unproved lemma is a native fixed-rank <=8 reduction whose
coefficients AND change-of-basis have extensive absolute height

    H_out <= C H_in + P(charged field data),

with an ABSOLUTE constant C, independent of N,d and coefficient heights.
Here H_K(x)=N h(x), summed only over bounded-rank tuples. A factor N in C
would leave N^O(log d), and a nonlinear power of H would be worse. Neither
is acceptable. The expanded norm solver alone guarantees only a polynomial
output bound and does not prove this affine lemma.

Candidate height repair: the reviewed C1 ideal reset/C2 weighted squareclass
compression gives absolute-slope conic shortening of an ALREADY EXPANDED
witness. Its former tower root extraction can now be replaced by actual
Lenstra polynomial factoring over the original K. For q5 local gluing, take
a short nonzero gamma in the CRT ideal I by Minkowski LLL and reduce a CRT
representative modulo gamma*O_K, a SUBLATTICE of I. The basis gamma*omega_i
may yield a coefficient-height slope independent of N. These details, local
integrality, auxiliary discriminants and all fixed-rank maps need proof.

## Classical and source checks

Corpus returns existing compact isotropy, class/unit and LLL baselines;
lexical nonmatches are not novelty or hardness evidence. Actual primary
Fukshansky Theorem1.3 gives small-height Witt components by an existence
argument, starting with an existential maximal isotropic subspace. It does
not by itself supply this native polynomial compiler. Actual Koprowski–
Rothkegel assumes principal generators, S-class/S-unit computations and
Algorithm8 enlarges support until an F2 system solves. Its stated output is
an abstract anisotropic form, not a full embedded basis with this clock.
Retained PDFs/text/metadata: audits/sources/2026-11-13-balanced-witt/.
No exhaustive literature priority claim or claim their algorithms are slow.

Cheapest falsifiers: trace every height recurrence symbolically before any
quantum implementation; expose N-dependent slopes, nonlinear input-height
dependence, uncharged compact expansion, growing field towers, supplied
starting witnesses, unbounded support searches or basis reconstruction costs.
No backend or new research infrastructure is proposed. If the height lemma
fails, retain the single-vector corollary but do not promote full decomposition.

