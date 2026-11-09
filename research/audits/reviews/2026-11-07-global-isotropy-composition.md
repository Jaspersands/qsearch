# Global compact isotropy: integrated composition review

7 November 2026. **ACCEPT the written bounded-error quantum polynomial-BIT
composition under the stated GRH and explicit-input contracts.** No remaining
mathematical/resource blocker was found in this review. This is acceptance of a
composition of the cited arithmetic interfaces and the written reductions, not
novelty, separation, an implemented solver, or an expanded-point theorem.

Read current STATE/TRAPS, the actual main note, the descent/source/local reviews,
and the relevant primary Amitsur and Voight statements. In particular, actual
Kutas--Montessinos Theorems4.12--4.13 give the promised-split GRH interface;
Voight Proposition5.8/Theorem6.1 give local Hilbert decisions, Remark5.3 the
unramified norm group, and Theorem7.2/Lemma7.16 the factored arithmetic interfaces.
Acceptance below does not follow from reviewers' ACCEPT labels or finite controls.
No Git, network/API, solver implementation, or new experiment was used.

## Contract and branch structure

The input pays the growing number field K, its defining polynomial and compatible
expanded maximal-order basis/table, and an expanded nondegenerate symmetric
d-by-d form. The result is NO or a polynomial-size K arithmetic-circuit vector
which is nonzero and isotropic, with the stated bounded overall error. An exhausted
internal clock may return ABORT within the failure budget. Compact inputs, short
or integral points, and recursively expanded Witt decompositions are not covered.

Congruence diagonalization is polynomial-bit expanded linear algebra. A zero
diagonal pivot does not imply degeneracy: use a sum of two coordinate vectors
when an off-diagonal entry is nonzero. Fraction-free/minor bounds pay coefficient
growth. Dimensions1/2 reduce respectively to NO and the square test for -b/a.
Dimensions3/4 use the written quaternion constructions. For their source promise,
decide splitting over the constructed field by Hilbert symbols at real places
and primes supporting2uv; all other finite places split. Those parameters are
still expanded and polynomial-height. A nonsplit algebra gives NO; a split one
is a legal source input. This is a finite polynomial support, not an unbounded
search for a favorable prime.

## One five-plane really suffices

For d>=5, finite completions have u-invariant4 and complex places cause no
obstruction. Consequently the exact decision is indefiniteness at every real
embedding. If there are no real embeddings, choose any five diagonal coordinates.

Otherwise choose, separately at each real embedding, five distinct coordinate
vectors containing both signs. The selected diagonal restriction has nonzero
eigenvalues. Polynomial-height algebraic inputs bound every selected absolute
coefficient below by exp(-poly(input)) and above by exp(poly(input)). Hence a
uniform polynomial-bit approximation to all d-by-5 entries preserves inertia and
nondegeneracy. The written weak-approximation routine supplies ONE K-matrix M
simultaneously close to these possibly incompatible coordinate choices. Its
restricted form M^t Q M is nondegenerate at each real place and therefore over K;
M has full column rank. It is isotropic globally. There is no requirement that
one coordinate five-subset work at all embeddings, and no recursive height bound
is being assumed. A subsequent single diagonalization remains polynomial-bit.

## Five to four: supports and signs

For q1=<a1,a2,a3>, an anisotropic finite-local ternary form represents exactly
the nonzero squareclasses other than -det(q1). Thus q1+<c> is isotropic if c is
outside det(q1) times local squares. The sign in the note is correct. One can also
see the excluded class from four-dimensional local classification: an anisotropic
4-form has square determinant, while an isotropic 4-form with square determinant
is hyperbolic and cannot contain an anisotropic 3-subform.

Take S above2 and the numerator/denominator supports of a1,a2,a3. Outside S the
ternary form is odd-residue unimodular, and finite-field isotropy lifts by Hensel.
This remains true at NEW primes introduced by the subsequently constructed c.
Those primes do not require enlarging S. At primes in S the revised local chooser
provides a nonzero binary value a4*s_p^2+a5*t_p^2 outside the forbidden class.
It is harmless to impose this stronger condition where q1 is already isotropic.

At a real place where q1 is definite, one of a4,a5 has the opposite sign. Taking
the corresponding real target coordinate1 and the other0 already gives the
desired sign; a polynomial-bit accuracy suffices by coefficient separation.
Where q1 is indefinite there is no real constraint. The finite precision
inequalities in the note ensure c/c_p is a local square at each p in S, including
fractional target coordinates. Since S contains a dyadic prime, these conditions
also ensure c is globally nonzero. Hasse--Minkowski now makes q4 isotropic.

The lift (w1,w2,w3,s*w4,t*w4) preserves the form value. It cannot kill a nonzero
w because c!=0 implies (s,t)!=(0,0). The final map M also preserves nonzeroness
because M has full column rank. This checks the exact output, not just existence.

## Local construction and polynomial expanded sizes

The quadratic ideal replacement has the required uniform interface. A global
square test is not being confused with a local square promise. In the nonsquare
case, factoring p in K(sqrt(delta)) distinguishes the split, ramified and inert
local cases. A uniformizer/CRT element gives odd norm valuation in the first two;
the inert dyadic branch tests only O(n) squareclass generators, using unramified
unit-norm surjectivity. No enumeration of the exponentially large squareclass
group is present. The local review's arbitrary-fractional precision proof checks
the square-difference bound and correctly charges numerical M, not merely log M.

Ideal HNF bases, reduced CRT representatives, residue lifts, and compatible
relative-coordinate conversion all have polynomial expanded bits. Every square
test makes a quadratic extension of the ORIGINAL K; the fields are not accumulated
into an exponential tower. There are polynomially many calls of degree at most2n.
Valuations of these expanded elements are bounded by cleared denominator and norm
bit sizes. Therefore every requested ideal-power norm logarithm is polynomial.

## Weak approximation and conditioning

The formula x=u0/D+sum k_i*b_i/(D*M) is valid: M=1+kR is a unit at every prescribed
finite prime, and all corrections lie in I/(DM). The exponent
e_p=M_p+n*v_r(D) dominates M_p+v_p(D). Clearing denominators and multiplying the
polynomially many ideals therefore costs polynomial bits.

Use the FULL real Minkowski matrix, including both components of complex
embeddings, to choose the correction coefficients. Its determinant has absolute
value2^(-r2)*sqrt(|disc K|)*Norm(I). Combined with the explicit exp(poly) entry
bound, this gives an exp(poly) inverse-norm bound. The note's separate target and
matrix error tolerances imply coefficient error below1/(4M); subsequent integer
rounding contributes at most3/(4M) per coefficient. The chosen M then pays the
requested real error. Its numerical value can be enormous but its bit length,
all required precision, and every resulting expanded coefficient are polynomial.
Root isolation uses the supplied compatible power-basis encoding; no unlabelled
embedding or floating condition-number promise is imported.

## Split source, compact descent, and failure clocks

All field/form data passed to the promised-split source are expanded and of
polynomial height. GRH remains explicit. The source's compact cochain-to-matrix
interface is used; no large unit or splitting coordinate is expanded. The
source's internal etale tensor-factor fields have polynomial degree as its theorem
charges. The phrase degree<=2n applies to the local quadratic/descent fields,
not to every internal field of the imported source.

The exact descent proof is sound for an arbitrary valid splitting: reversion is
an ANTI-automorphism, so conjugate isotropic planes correspond to opposite ideal
rulings and intersect in a line. Normalizing a nonzero coordinate makes that line's
point K-rational. Only constantly many compact field operations and minors are
needed. Returning through the expanded changes of basis adds polynomially many
DAG gates. No sign comparison or real approximation of compact outputs occurs.

Use certified/capped factoring and finite-field routines with a polynomial bound
on their total calls. Allocate, for example, eta/4 each to these preparatory calls,
the compact split-source failure, compact branch tests, and final verification.
A correct splitting has an efficiently checkable set of algebra relations through
the paid bounded-error circuit interface. Independent capped source repetitions
and verification can amplify a constant-success source in O(log(1/eta)) trials;
one must not majority-vote noncanonical splitting matrices.

The modular circuit test pays its enormous expanded heights by choosing primes
with POLYNOMIAL BIT length exceeding the logarithm of the bad-prime bound. It
does not enumerate those primes or factor expanded circuit values. Evaluate in
the full finite algebra and require each denominator multiplication matrix to be
invertible. Use FRESH primes for adaptive tests and final verification. Reusing
one prime is safe only for a fixed nonadaptive expression list with a union bound.
Undefined divisions are rejected. Uniform circuit/time/size caps bound every
conditional test input, so the modular error bound remains applicable after prior
branch choices. This gives bounded-error verification, not deterministic exact
certification of arbitrary compact arithmetic circuits.

## Scope of acceptance

The original expanded growing-(n,d) input reaches NO or a compact nonzero point
without hidden local roots, class/unit advice, auxiliary-field advice, support
search, or a compact-to-expanded conversion. The finite controls are consistent
with this proof but are not its justification. Rational forms and special base
fields retain stronger classical algorithms; existing norm, S-unit, quaternion,
and isotropy literature supplies substantial overlap. No general classical
separation, new primitive, priority claim, short/expanded solution, repeated Witt
decomposition, GRH removal or quantum execution follows.
