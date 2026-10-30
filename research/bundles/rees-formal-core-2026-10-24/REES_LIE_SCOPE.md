# A Concrete Checked Rees Lie Cover

2026-10-24. This advances the formal proof from an interpolation interface
to a genuine Lie algebra construction. It does not establish a quantum
algorithm, novelty, gate complexity, or an application.

## Construction And Proof

Let L be a Lie algebra over any field F. Use mathlib's zero-based series
C_i = gamma_(i+1)(L), so C_0=L. Fix n with C_n=0. The coefficient space is

    V = { (v_0,...,v_(n-1)) : v_j in C_j }.

Choose n distinct nonzero field points s_i. Their existence is an explicit
premise, not silently inferred for every finite field. In the manuscript's
prime-field setting p>n provides enough such points. Define

    E(v)_i = sum_j s_i^(j+1) v_j.

The ambient space L^n has the pointwise Lie bracket. The cover is the image
E(V), with its inherited bracket. This construction is not the associated
graded algebra and does not quotient away derived directions in grade one.

The checked lower-central lemma is [C_i,C_j] <= C_(i+j+1). Its proof uses
induction on i, the linear-span description of the bracket ideal, and the
Jacobi identity. It is proved for the actual lower central series, not
introduced as an assumed filtration law.

For two coefficient monomials, their pointwise bracket is

    [s^r x, s^q y] = s^(r+q) [x,y].

If r+q<=n, the coefficient belongs to the required lower-central term.
If r+q>n, it is ZERO by C_n=0 and the antitone series. Thus closure does
not truncate any nonzero bracket. Finite bilinearity proves that E(V) is
a Lie subalgebra. Jacobi is inherited from the pointwise Lie algebra.

Each coordinate projection E(V)->L is constructed as a LieHom. Applying
the standard lower-central image bound to every coordinate proves that
the cover's own nth lower-central term vanishes. No separate assumption
of nilpotency of the constructed cover is used.

The evaluation matrix has powers1 throughn, and determinant
prod_i s_i * prod_(i<j)(s_j-s_i). The preceding checked interpolation
lemmas give injectivity. `recover` is explicitly multiplication by the
inverse evaluation matrix, not hidden advice or existentially supplied
coefficients. Both compositions are checked on their stated domains.
This also identifies the evaluation realization with the intended direct
sum as a vector space; no dimension formula is separately formalized.

For ANY original submodule h, all constructed evaluations lie in h iff
all recovered coefficients lie in h. With n>0, the first monomial accepts
x exactly when x belongs to h. Hence the original hidden subspace can be
read in grade one; it has not been replaced by an abelianization. The
grade-one inclusion is linear and is deliberately NOT called a Lie
homomorphism: the bracket of two degree-one elements has degree two.

## Precise Boundary

The formal constructors require C_n=0. Simply deleting this premise or
replacing it with an arbitrary truncation would change the polynomial
bracket; the proof does not authorize that change. Likewise, zero or
repeated evaluation points do not support coefficient recovery, as the
older universal counterexamples demonstrate.

The subsequent ReesDilation.lean pass constructs the concrete dilation
Lie automorphism, including its inverse, bracket law and hidden-membership
invariance. See REES_DILATION_SCOPE.md. The older coefficientwise lemma
alone was not an automorphism proof. BCH/Lazard functoriality and its
characteristic restriction are also not formalized. In particular, the
new LieHom maps must not be advertised as checked group homomorphisms.

Neither the complete normalized central quantum instrument, fresh-copy
adaptive composition, SDE algorithm/runtime, final Fourier recovery nor
resource/precision bounds are in this formal scope. Noncomputable Lean
definitions and kernel checks are not compiled quantum circuits or a
formal bit-complexity analysis. Imported mathlib proof binaries and the
Lean toolchain remain trusted.

The original sixteen theorems plus fifteen cover theorems, thirteen
dilation theorems and fifteen total definitions/instances are audited. Only the standard
propext/Classical.choice/Quot.sound axioms are allowed. Passing this
check cannot change the manuscript's novelty or natural-application
status. The one authorized independent reviewer did not review this
new formalization; no further reviewer was spawned.

## Bounded Integration Handoff

After verified migration, Gemini should integrate ReesLie.lean and
ReesDilation.lean with the
existing formal project, adjust module imports/pointwise-instance ownership
if needed, and run the full declared axiom audit. Preserve the source
snapshot and written-versus-checked scope distinctions. Do not create a
new candidate, restore circuit search, or change algorithm admission flags.
Record this as removal of the Lie-cover/evaluation and graded
Lie-automorphism proof debt only.
