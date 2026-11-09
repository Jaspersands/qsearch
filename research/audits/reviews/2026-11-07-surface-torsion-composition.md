# Quartic P2: integrated written-algorithm review

2026-11-07. CLOSED after the explicit joins/guards below. Read the complete
surface-torsion geometry review, the current main note, and the earlier cyclic-
induction/readout review; checked the cited Kedlaya input protocol, pencil
statement, reduced-divisor lemma and KM5.5 parameter interface directly. No
network, API, implementation or control was run.

**Disposition:** the geometry plus corrected readout gives a WRITTEN bounded-
error quantum algorithm for the exact degree22 P2 of every promised smooth
quartic over F_p, in polynomial(log p, log(1/eta)) BIT/gate time at FIXED degree.
The following implementation guards are part of the theorem, rather than
optional checks. No GRH, supplied torsion, cohomology oracle, short output
certificate or Tate-conjecture assumption is used. This is not a novelty,
classical separation, practical-cost or execution claim. The Kuga--Satake
classical comparator remains viable/open as recorded separately.

The determinant convention is P2(T)=det(1-FT). Thus the derived point count
is #X(F_p)=1+p^2-[T]P2. In the direct-count branch the Newton power traces
are s_j=#X(F_(p^j))-1-p^(2j). A plus sign before [T]P2 in the main-note
contract is a transcription error and must be changed; the Leray proof
already uses the correct convention.

## 1. Native geometry and arithmetic source join

Use the source-paid CUBIC-Veronese pencil, not an unproved genus3 plane-pencil
promise. Its fibers have class3H, genus19, a reduced degree36 base scheme and
132 geometric nodal bad fibers. The irreducibility argument in the geometry
review covers every such singular fiber: if D=A+B with one node, then A.B=1;
choosing 1<=H.A<=6 contradicts A^2=3(H.A)-1 and the Hodge-index inequality.
Nonreduced components would not have only an ordinary node.

The pointed-pencil search is native. For large p the K3 Weil bound and the
bounded number of contained lines give constant success for random line
intersection/root extraction. The distribution on surface points has bounded
bias relative to the uniform distribution. The good pointed-pencil locus is
a nonempty open subset of an irreducible fixed-degree incidence bundle, so
the source's bounded-degree avoidance/verification pays the joint search.
Its rational basepoint is a rational point of the generic fiber; other base
points need not be rational. No extension changes the surface Frobenius here.

The fixed g=19, d0=39, deg L=117 section data and canonical reduced-divisor
atlas are compatible with KM5.5: the relevant degrees lie in [39,78]. A minimal
effective representative E-mP0 has h0(E)=1 and omits P0, and is unique. These
constructions commute with field extension. In particular, evaluating them on
a separable Jacobian ell-torsion point produces coordinates over that same
separable field; they do not introduce a hidden purely inseparable coordinate
extension. Conversely the represented divisor determines its class over the
coordinate field. This justifies using the etale residue fields of J[ell],
not merely counting geometric points in a potentially unrelated algebra.

All coordinate, pivot and rank charts have fixed variable count and initial
degree. Flattened O(log ell) addition chains have polynomially many paths and
polynomial degrees/t-heights. The fixed-variable elimination and finite-algebra
linear solves therefore have polynomial size in ell and log p. The stated
trace-pairing radical removal is valid under its characteristic bound: over
each separable residue field the trace form is its nondegenerate field trace
multiplied by the local Artin length, which is nonzero when that length<p.
Its kernel is exactly the nilradical.

The rank-ell^38 torsion algebra and its 38-fold tensor product remain polynomial
in numerical ell. Canonical addition/equality tests on the universal points
retain exactly the frames. The output is a possibly disconnected full GL38
torsor, with explicit deck actions and FULL arithmetic action. It is not a
supplied torsion basis or merely a geometric monodromy cover. Flattening before
finite-algebra inversion is essential to the claimed polynomial t-height.

## 2. One safe characteristic envelope, with an exact fallback

Define one explicit fixed polynomial Q(ell) dominating:

- 2*M_cell(ell)^2 for radical removal;
- all frame/twist algebra ranks and primitive-element discriminant sampling
  degrees used by the chosen construction;
- |GL38(F_ell)| and the fixed pointed-pencil/field-size thresholds.

The polynomial is obtained by composing the displayed fixed-size/elimination
bounds; it must not silently mean an unknown input-dependent complexity bound.
Require p>Q(ell) for the geometric branch. This repairs the possible mistake
of using the cell-rank guard as if it automatically dominated frame rank.
Alternatively infinite-field sampling from low-t-degree polynomials would
pay primitive elements, but the enlarged envelope is simpler.

If this guard fails for ANY ell reached by the CRT procedure below, count
X(F_(p^j)) directly for 1<=j<=22, then use integer Newton identities. Since
ell=O(log p), the failure gives p<=Q(O(log p)). Enumerating projective points
in these FIXED extension degrees takes p^O(1), hence polynomial(log p) on
this branch. Finite-field construction and arithmetic are included. The bound
has enormous fixed exponents but is a genuine bit-complexity bound. It does
not extend to variable surface degree or an unbounded number of point counts.

## 3. Actual curve inputs, twists and local Frobenius

The generic algebra is normalized to the genuine finite etale cover over U;
poles of a divisor chart are not additional geometric ramification. In the
safe branch the frame degree is prime to p, so the Riemann--Hurwitz bound is
tame. With 132 branch points, every component and the sum of its genera are
polynomial in |GL38|. Constant-field twist descent uses a constant extension
of degree ord(h)<=|GL38| and semilinear fixed-space linear algebra. It does
not divide by |H| in characteristic ell or require an unknown function-field
Frobenius oracle.

The normalizations and full constant fields must be computed BEFORE a curve
zeta call. Rebase each arithmetic component over its full constant field so
the supplied curve is geometrically irreducible, as Kedlaya requires. Zeta
factors of such a component over its smaller field are recovered with the
corresponding substitution T->T^a. For first point counts, a component with
constant degree a>1 simply contributes no base-field points.

An original plane model can have genus much smaller than its degree. Charge
normalization and Riemann--Roch by that supplied degree, which is polynomial
in ell; do not charge it only by genus. Then use a paid low-degree plane-model
conversion if needed for Kedlaya's stated protocol. Genus-zero geometric
components have zeta 1/((1-T)(1-qT)) and need no Jacobian computation. The
source's polynomial resolution/RR interface avoids a common field rationalizing
arbitrary singularities.

For the boundary, the stronger common-extension bound is justified by the
torsor structure, not by an arbitrary splitting-field assertion: a connected
arithmetic component is Galois of degree dividing |GL38|. Constant degrees
and local residue degrees divide the stated torsor bounds. Deck maps commute
with Frobenius; their twists have polynomial extension bounds as well.
Kozen's local parameters, bounded zero/pole orders and finite-algebra identity
tests pay the local evaluations and permutations.

The inertia group at a geometric boundary point is its deck stabilizer.
Arithmetic Frobenius sends that point to another in the same deck orbit;
finding a deck element realizing this movement gives its decomposition-group
representative modulo inertia. Its action on the invariant subspace is thus
well-defined. For raw J[ell] arithmetic matrix A, the coefficient sheaf V is
the dual, with arithmetic action A^(-T); its geometric Frobenius action is
A^T. These conventions must also be used for the twist sector, rather than
discarding an arithmetic cyclotomic twist.

## 4. Readout and Leray: the exact joins

There is ONE necessary correction to the current main-note wording:

    H_c(U,V) = (H_c(Z) tensor V)^Gamma

is NOT valid for arbitrary V when ell divides |Gamma|. General descent is
derived. The ordinary-invariant formula used here is only for
P=Ind_H chi with |H| prime to ell: Shapiro and exact H-invariants give the
chi^-1 sector. For the natural dual V, first use the proven G0 identity and
Euler-L multiplicativity. No full-Gamma semisimplicity or invalid invariant
functor is needed. With this restriction the readout review applies unchanged.

The h-twist must be over F_(p^j), producing h*F^j. Component and boundary
permutations isolate the compact-curve H1 traces from point counts. Fourier
projection and Newton identities occur in characteristic ZERO, followed by
integral reduction at ell. This pays Newton indices divisible by ell.
Rational L-functions with value1 at zero have unique m-th roots; factor and
combine multiplicities in binary before dividing by m. No degree-m expansion
or division by m in characteristic ell occurs.

At an irreducible node the integral nearby-cycle sequence and primitive
nonseparating vanishing cycle give H1(special)=V^I after reduction for EVERY
ell!=p. R0 is constant and R2 is the Tate sheaf because the fibers are
geometrically irreducible. Proper base change and the Euler version of Leray
therefore yield

    zeta(tilde X)=zeta(P1,T)*zeta(P1,pT)/L(P1,j_*V),
    P2(X,T)*P_B(pT)=(1-pT)^2*L(P1,j_*V).

P_B is the degree36 base-scheme permutation polynomial, not (1-T)^36 unless
all basepoints happen to be rational. The boundary factors are exactly
det(1-F_s*T^deg(s)|V^I)^(-1). The formula uses an Euler identity; no mod-ell
Leray degeneration assumption is hidden in it. K3 cohomology is torsion-free
in the needed ell-adic degrees, with H1=H3=0 and H2 rank22, so the recovered
mod-ell polynomial is the reduction of the integral P2.

## 5. Output-size and probability clocks

The quantum curve subroutine can fail with a plausible but incorrect answer.
Before any potentially large expansion, perform the following size guards;
they protect runtime, not correctness certification. For tame rank38 V on
P1 minus132 geometric points, Grothendieck--Ogg--Shafarevich gives

    H_c^0=0,  dim H_c^2<=38,
    dim H_c^1=38*(132-2)+dim H_c^2<=4978.

After signed factor multiplicities are combined/divided by m, ABORT unless
the reduced numerator degree is <=4978 and denominator degree <=38. Also
check m-divisibility, normalization, and descent of the final coefficients
to F_ell. These degree tests are performed on BINARY exponents before
expansion. Correct readout always passes. Apply the boundary/Leray correction,
then require the fixed degree22 and normalization before storing a CRT residue.
This prevents bad quantum outputs from causing expansion by an exponential
numerical exponent. Such checks do not certify that a surviving answer is right.

Collect primes ell>22, ell!=p until their product exceeds 2^23*p^22.
The Weil bounds |c_i|<=binom(22,i)*p^i imply this exceeds twice every possible
coefficient magnitude. Effective elementary prime bounds give a largest
required ell=O(log p), even after excluding those finitely many primes and p.
Signed CRT then recovers each integer coefficient uniquely. No additional
unknown set of bad auxiliary primes is excluded.

All genera, model degrees, extension degrees, character-table dimensions and
numbers of quantum calls are polynomial in numerical ell at fixed rank38.
The cyclotomic order ell^lcm(1,...,38)-1 is included in this cost, however
impractical the resulting constant exponent is. Together with ell=O(log p),
these are polynomial bit/gate bounds in the native input length.

Give each quantum curve-zeta call an error budget summing to at most eta/2.
Independent repetitions and exact output-majority amplify its bounded success
probability with logarithmic overhead. Give classical randomized construction
and finite-field routines the remaining eta/2. For an expected Las Vegas
clock T, use independently restarted attempts capped at a constant multiple
of T, with O(log(number_of_calls/eta)) attempts; do NOT use a single cap T/eta
and call that logarithmic confidence dependence. Validate intermediate model
and factor outputs where applicable, and ABORT on an exhausted clock. Cap
all output lengths by the preceding proven degree/height bounds.

On the joint success event all residues and the exact output are correct.
On its complement the algorithm may ABORT or return an incorrect polynomial;
the total probability is at most eta. There is no independent exact-output
verifier, and Weil/functional-equation checks do not provide one.

**Final scope:** with the ordinary-invariants sentence restricted as above and
the explicit guards incorporated, no remaining composition blocker was found.
This closes the written fixed-degree quantum upper-bound reduction. It does
not close the independently viable Kuga--Satake classical comparison, establish
priority, or license a speedup/novelty/implementation claim.
