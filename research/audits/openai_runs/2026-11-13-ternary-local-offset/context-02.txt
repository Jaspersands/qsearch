# Checked primitive contracts, 13November2026

The admitted relative norm endpoint returns NO or a signed power product
of polynomially many polynomial-size EXPANDED L-atoms, binary exponents,
exact norm equal to expanded a inK. Its bounded-error polynomial quantum
BIT clock assumes explicit GRH and charges expanded maximal-order tables,
embedding and field degrees. No arbitrary compact arithmetic circuit or
compact target is allowed. Parent read the original exact contract,
RELATIVE_NORM_TENSOR_SUPPORT.md lines42-53. Complete S-unit/relation and
tensor-support proofs were already independently checked; not re-proved here.

Actual A.K.Lenstra IW213/82, Factoring Polynomials over Algebraic Number
Fields, field encoding in section1 and Theorem3.7 with preceding scalar
normalization proof were read. It factors univariate polynomials over
Q(alpha), represented by a monic integral minimal polynomial, in polynomial
arithmetic count AND polynomial integer bit lengths depending on field
degree, polynomial degree and coefficient bits. Thus it supplies classical
polynomial BIT extraction of a known dth power's root without computing
a splitting field. Rational coefficients are cleared/normalized first.
Retained source: audits/sources/2026-11-13-expanded-norm/lenstra_factor.pdf.
Parent encoding deduction: from a charged field structure table one can
build a primitive element incrementally. For each next basis element b,
try alpha+t*b for 0<=t<=n(n-1)/2 and take maximal minimal-polynomial degree.
The finitely many pairwise embedding collisions are the only bad t; hence
the maximum generates Q(alpha,b). At mostn stages, polynomial-bit t and
coordinates; compute minimal polynomials and basis conversions by exact
linear algebra. This deduction is part of the requested audit.

Actual Magma quaternion-isomorphism documentation text1082 describes
matching one standard generator then a perpendicular second generator
using quadratic conic/norm operations. It does NOT assert a uniform BIT
clock. Parent's explicit division-algebra construction is separate algebra
to be checked, not a theorem inferred from this documentation.

Actual Fan-Li2026 Constructive and stable Cartan-Dieudonne Theorem1.1 is
BINARY local orthogonal decomposition/stability, given an existing matrix.
It is not a ternary native transporter algorithm or a polynomial search
clock; do not import it as one. Existing Beli/Voight spinor/Hilbert source
contracts are described in the attached prior local admission note.
