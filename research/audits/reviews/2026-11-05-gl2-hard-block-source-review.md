# Independent source audit: the GL2 hard Fourier block

2026-11-05. Scope: the actual construction of the q-dimensional A_gamma
block in *Quantum Fourier transform toolbox*, arXiv:2608.28573,
Sections 6.5 and B.2, especially Theorems 6.26 and 6.33. This audits a
critical source dependency of QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md.
It is not a reproof of the entire generic Mackey induction theorem, a
compiled whole GL2 QFT, or a new algorithm/priority claim.

## Verdict and dependencies

No correctness, normalization, coherence, cleanup or circular-preparation
blocker was found in the hard-block construction. Its stated formulas
(129)-(130) have a uniform implementation polynomial in log(q) and
log(1/epsilon), using the source's clean finite-field arithmetic,
cyclic/additive Fourier transforms, coherent discrete logarithms and
normalized Gauss-phase primitive. The latter are explicit dependencies;
this audit does not substitute a pointwise-success classical logarithm
routine for an operator-norm coherent circuit.

The statement holds coherently in gamma, without iterating over its q-1
values. Only a constant number of block types, exceptional roots, and
controlled approximate subroutines occur. Public compatible generators
h of F_(q^2)^* and g=h^(q+1) of F_q^* are required and can be supplied by
the already charged public preprocessing. No unknown input polynomial or
oracle extension enters this Fourier primitive.

## Original-PDF convention checks

The local primary PDF and text are
`../sources/legendre_prf/qft_toolbox_2608_28573.pdf` and its `.txt`.
Original PDF pages 39, 40, 43 and 84 were rendered and inspected; text
extraction drops overbars elsewhere in the paper.

- Equation (114) is zeta_(alpha,beta)=chi_beta(-1)
  g_q(alpha^-1 beta)/sqrt(q), with NO conjugation. D_gamma in (134)
  uses this unbarred phase. Equation (122), outside the hard block, does
  have a conjugated zeta and must not be copied from the extracted text.
- Equation (129) has positive coefficients. Every Gauss term in (130)
  and its common chi_b(-1) factor is unbarred. The cuspidal denominator
  is sqrt(q(q^2-1)); the principal denominator is (q-1)sqrt(q); the
  Steinberg denominator is (q-1)sqrt(q+1).
- In norm-torus exponent coordinates, put n=h^(q-1),
  nu_j(n)=exp(2 pi i j/(q+1)), and gamma(g)=exp(2 pi i k/(q-1)).
  Pullback along z -> z/z^q sends the output label theta_0 nu_j to
  full-field character exponent k-(q-1)j modulo q^2-1. Frobenius sends
  j to -k-j modulo q+1. For gamma=1 the sign is hidden by the folded
  pair {j,-j}; a nontrivial-gamma test must preserve this convention.

## Torus branching and exact coefficients

Write T_gamma=R_fix (F_split direct-sum F_norm) B_gamma F_mult^dagger.
The branching map B_gamma is an isometry: distinct nonboundary t have
disjoint root-ratio support, and each has two terms of magnitude 1/sqrt(2).
For odd q, the two boundary inputs t=0,1/4 map to orthogonal combinations
of |split,1> and |nonsplit,1>. For even q only the first boundary occurs.

For nonboundary roots u+v=1 and ratio r=u/v, the output reconstructs

    u=r/(1+r), v=1/(1+r), t=r/(1+r)^2.

The denominator is nonzero. These equations recover the oriented roots,
input t and canonical ordering bit, allowing all root-finding work to be
uncomputed. The two-dimensional boundary map is handled separately.
Neither branch identification nor root selection is a measurement.

For odd q, the public discrete logarithm e of 1-4t selects the branch;
g^(e/2) gives a split square root when e is even, and
h^((q+1)e/2) gives a nonsplit root when e is odd. For even q, solving
u^2+u=t is a fixed F2-linear computation, with absolute trace selecting
the branch and a fixed extension-field section on the nonsplit branch.
All are coherent polynomial-size operations.

Expanding the split Fourier sum gives the COMPLETE Jacobi sum
J(alpha^-1 delta,alpha^-1 eta)/(q-1). The repeated root at t=1/4 supplies
the missing x=1/2 summand. Expanding the nonsplit branch similarly gives
the trace-one sum over F_(q^2); the same boundary supplies its rational
trace-one point. Frobenius invariance and symmetry of the Jacobi sum make
both nonfixed label pairs symmetric, so antisymmetric output amplitudes
vanish exactly after folding.

For generic alpha^2!=gamma, the two shifted principal characters have
nontrivial product. The Jacobi-to-Gauss quotient therefore gives (130),
including the case where exactly one shifted character is trivial.
For the cuspidal term the trace-zero fiber vanishes because the restricted
character is nontrivial. The fixed Steinberg row uses the quadratic
extension Gauss identity, giving the required minus sign in its trace-one
sum. Multiplying by D_gamma gives the literal A_gamma coefficients.

For alpha^2=gamma, the source obtains instead

    T_gamma|c_alpha> = -chi_alpha(-1) A_gamma|c_alpha>/sqrt(q)
                     +sqrt((q-1)/q)|det_alpha>.

This includes the extra quadratic fixed label in odd characteristic.
The two fixed-row cases are separate: the trivial shifted character has
Jacobi sum q-2, whereas the other has J(xi,xi)=-xi(-1).
No nontrivial-Gauss normalization is used for a trivial character.

## Exceptional columns are prepared without calling A_gamma

Lemma B.3 explicitly constructs the required target column. Let s be the
number of solutions to alpha^2=gamma. Its three branch probabilities are

    N_C=|C_gamma| q/((q-1)(q+1)),
    N_P=|P_gamma| q/(q-1)^2,
    N_S=(1+(s-1)q^2)/((q-1)^2(q+1)).

Using |C_gamma|=(q+1-s)/2 and |P_gamma|=(q-1-s)/2 shows that they sum
to one exactly. The principal branch can be empty (q=3,s=2); it is then
skipped rather than normalized by zero.

The uniform label states exclude at most two fixed exponents in cyclic
sets of size q-1 and q+1. Rank/unrank of that complement uses comparisons
and additions. Canonicalizing each involution pair leaves a |+> order
bit, removed with a Hadamard. No rejection or postselection is used.

On cuspidal labels the shifted character is regular and therefore
nontrivial; one normalized F_(q^2) Gauss phase gives its coefficient.
On principal labels the two shifted characters are nontrivial inverses;
their Gauss product is the explicit phase q xi(-1). The at most two
Steinberg amplitudes have relative magnitudes 1 and q. The second one's
phase uses two nontrivial Gauss-phase gates. Original PDF page 84 confirms
this q factor; dropping it would give a false normalized preparation.

Thus exceptional-column preparation invokes only public arithmetic,
uniform orbit labels, small rotations and Gauss phases. It never invokes
the unknown A_gamma circuit that it is being used to construct.

## Reflection, orthogonality and uniform errors

R_exc acts on the plane spanned by A_gamma|c_alpha> and |det_alpha> as
the reflection with matrix

    [ -a, sqrt(1-a^2); sqrt(1-a^2), a ],
    a=chi_alpha(-1)/sqrt(q).

Its normal vector is an explicitly weighted combination of the prepared
column and determinant state. Prepare-reflect-unprepare implements it
with clean ancillas. There are at most two such planes, found by solving
2a=k in exponent coordinates, so the construction is coherent in gamma.

The required orthogonality need not be assumed circularly from an
efficient A_gamma circuit. T_gamma is already an isometry. Its generic
columns equal the stated A_gamma columns up to unit phases; its
exceptional columns have the displayed physical-plus-determinant form.
Orthogonality of T_gamma columns and physical versus determinant labels
therefore forces all A_gamma columns to be orthonormal. The exceptional
planes are orthogonal; their reflections fix every other target column.

Each controlled subroutine is uniformly accurate in operator norm.
Dividing epsilon among the constant number of subroutines suffices;
there is no sum over q character labels in the error or gate count.
The construction implements the literal hard-block matrix on the clean
source subspace and returns its work registers to zero.

## Separate finite falsifier

The completed `../../classical_baselines/gl2_qft_hard_block_control.py`
and sibling JSON were inspected after the parent's run. They use exact
Sage field arithmetic and 200-bit complex matrix entries for the
predeclared q=3,5,7, gamma=1 cases. All 15 input columns are checked,
including every unused antisymmetric and determinant output. The literal
D -> F_mult^dagger -> B -> F_tori -> R_fix -> R_exc product matches
(129)-(130), with every recorded error below 2^-150. Branch isometry,
label unitarity, target isometry and unused-output leakage also pass.
Omitting R_exc gives an error greater than 0.1 at each q.

That control constructs R_exc densely from the literal target columns.
It therefore does NOT test efficient exceptional-column preparation;
the independent Lemma B.3 audit above supplies that separate obligation.
The test is a finite classical matrix falsifier, not an exact all-q
certificate or quantum execution. The remaining generic induction/QFT
theory retains its explicit source dependency; no whole QFT execution
is asserted.
