# Simon dimensions four and six: repaired polynomial-bit composition

2026-11-13. Independent assembly review. Integer factorization of any
polynomial-bit integer is an explicitly charged oracle resource.

**Result.** For a nonsingular soluble rational quadratic form of dimension
4 or 6, the repaired construction returns a nonzero rational zero in
polynomial bit time, or `ABORT` with probability at most `eta`. Every
accepted vector is checked exactly and has polynomial coordinate length.
The dimension is fixed. The large fixed constants in the unimodular
majorant routine remain part of this written algorithm.

Inputs checked in this review:

- Simon, `audits/sources/selmer_classical_two/simon_dim4.txt`, Algorithms
  4--7 and their proofs, physical lines 345--767; printed PDF pp.12--13
  also read visually where a sign mattered.
- `audits/reviews/2026-11-13-simon-minimization-majorant-clock.md`: the
  repaired minimization L1 and full unimodular isotropic-basis routine L2.
- `audits/reviews/2026-11-13-bosma-stevenhagen-conic-clock-repair.md`:
  complete represented STRICT two-Sylow generators for either sign and
  nonfundamental discriminants, with polynomial-bit composition/reduction
  and a bounded randomized clock.

This proof uses neither Simon's original indefinite reducer nor its
unpublished dimension-nine termination assertion. It does not re-audit
the separately checked Kutas interface.

## 1. Shared operations and the binary genus map

Clear rational denominators by a positive integer, obtaining an integral
Gram matrix of polynomial bit length. Compute signature and determinant
by exact rational linear algebra and factor the determinant. A zero
diagonal pivot causes no problem: congruence pivoting uses a nonzero
off-diagonal entry, or an already available isotropic vector.

L1 stores every minimized form as `c A^t Q A`, with positive rational
`c` and a polynomial-size rational backmap `A`. In every subsequent
intersection, first pull the isotropic basis back through `A`. Intersecting
an untransported coordinate subspace with a basis in the new coordinates
would be incorrect.

For a primitive binary form `g=(a,b,c)` of nonsquare discriminant `delta`,
the local Hasse invariant is

\[
 \epsilon_p(g)=(a,\delta)_p.                             \tag{1}
\]

Here `a!=0`, and diagonalization gives (1) even when `a` is not coprime
to `delta`. These invariants are genus characters of the proper/strict
class group: they multiply under composition and take values in
`{+1,-1}`. The odd-order subgroup is therefore in their kernel.

For any realizable target genus, the complete represented two-Sylow
generators supplied by the repaired B--S backend suffice. Compute their
character columns and solve a binary linear system. A solution uses
exponents 0 or 1; compose that subset, weakly reducing after every
composition. No enumeration of the class group, class equality test, or
Pell/fundamental-unit computation enters this operation. Strict classes
are retained in the real-discriminant case.

Hilbert symbols at a specified prime are computed from valuations and
unit residues, including the usual dyadic unit residues. Rational
diagonalization has polynomial-height coefficients in these fixed
dimensions. One does not need to factor every diagonal numerator merely
to evaluate a symbol at a known prime.

## 2. Dimension four

After a possible global sign change, the indefinite signature is `(3,1)`
or `(2,2)`. Apply L1.

If the absolute initial determinant is a square, every determinant
valuation stays even under the dimension-four minimization rules. At a
terminal prime the valuation is at most 2, and at 2 it is at most 1.
Thus the dyadic valuation vanishes. A remaining odd-prime valuation 2 is
the local obstruction of Simon Proposition 10. On a soluble input it
cannot occur, so the determinant becomes `+/-1`; L2 supplies a zero.
This pays Algorithm 4's exceptional branch.

Otherwise the terminal determinant `Delta` has nonsquare absolute value.
For a soluble input, Proposition 10 again excludes every valuation 2;
hence `Delta` is squarefree. Proposition 11 gives the remaining dyadic
test: insolubility occurs exactly when
`Delta = 1 mod 8` and `epsilon_2(Q)=+1`. All odd places are soluble in
this squarefree situation. Consequently, passing these tests and the
signature test implies rational solubility by Hasse--Minkowski, as used
in the source's existence proof below. The tests do not consume an
unknown rational point.

Set `delta=4 Delta`, a nonsquare quadratic-order discriminant. Simon
Proposition 12 implies existence of an integral decomposition

\[
 Q\simeq H\perp T,\quad
 \det T=-\Delta,\quad
 \operatorname{sign}T=(r-1,s-1),\quad
 \epsilon_p(T)=\epsilon_p(Q)(-1,-\Delta)_p.              \tag{2}
\]

For clarity, this proposition does not require an algorithm for finding
the unknown point. A primitive isotropic vector has pairing divisor `a`
with `a^2|Delta`; squarefreeness forces `a=1`. Integral hyperbolic-plane
splitting then proves (2). It is an existence argument ensuring that the
following character systems are consistent.

Find a primitive class of discriminant `delta` with character target

\[
 \epsilon_p(g)=\epsilon_p(Q)(-1,-\delta)_p
 \quad\text{or}\quad
 \epsilon_p(g)=\epsilon_p(Q)(-1,-\delta)_p(2,\delta)_p,
 \qquad p\mid2\Delta.                                  \tag{3}
\]

At least one target is realizable. If the binary polynomial of `T` is
primitive, it gives the first target. Otherwise its content is exactly
2, necessarily `Delta=1 mod4`, and `T=2R` with `R` primitive of
discriminant `Delta`. A proper change of variables makes the leading
coefficient of `R=(a,b,c)` odd; then `(a,2b,4c)` is primitive of
discriminant `4 Delta`, has the invariants of `R`, and gives the second
target. This also explains why replacing the order by its maximal order
would not be legitimate.

The B--S output and the linear systems in (3) construct `g=(a,2b,c)`.
For the first target take `T'=[[a,b],[b,c]]`. For the second, one of the
three proper equivalents

\[
 (a,2b,c),\quad(c,-2b,a),\quad(a+2b+c,2b+2c,c)
\]

has even leading coefficient. Write it as `(2a',2b,c)` and put
`T'=[[a',b],[b,2c]]`. This is the rational congruence of `2g` obtained
by scaling its first variable by `1/2`. Consequently both constructions
satisfy exactly (2). Their coefficients remain polynomially bounded in
bit length. For negative `delta`, the backend's positive-form convention
gives signature `(2,0)`; for positive `delta`, the signature is `(1,1)`.

Now `Q6=Q perpendicular (-T')` has determinant `-Delta^2` and signature
`(3,3)`. At every `p|Delta`, its radical dimension and determinant valuation
are both 2. Simon Proposition 13's calculation gives an isotropic binary
radical form, so Lemma 8 removes the entire valuation. At odd `p`, equality
of the two binary Hasse invariants implies the relevant product of radical
unit coefficients is a square modulo `p`; at 2 all odd residues are squares
modulo 2. Thus the augmented form becomes integral unimodular.

L2 returns a three-dimensional totally isotropic subspace. Pull it back
to `Q6` and intersect with the original four-dimensional summand. The
intersection has dimension at least `3+4-6=1`. Pull a nonzero vector back
through the first minimization map to obtain the required zero of the
original rational form.

## 3. The seven-dimensional operation needed by dimension six

Only signatures `(5,2)` and `(4,3)` are needed after orientation. Apply
L1 to the seven-dimensional form. Its determinant `Delta` is odd and
squarefree. If it is a unit, L2 gives respectively 2 or 3 independent
isotropic vectors, which already suffices for the outer intersection.

Otherwise write `D=|Delta|` and set `delta=-8D`. This is a fundamental
negative discriminant. Use the B--S backend to find a positive primitive
binary form `T'=(a,2b,c)` with

\[
 \det T'=2D,\qquad
 \epsilon_p(T')=-((-1)^{(n-1)/2+s}2,p)_p
 \quad(p|D),\qquad n=7.                                \tag{4}
\]

Every choice of the odd-prime signs here is realizable (Simon Proposition
14). The dyadic sign is left free and set by the product formula. Its
local realizability can be checked explicitly. With `delta=-8D`, a
dyadic sign `+1` is supplied by `X^2-(delta/4)Y^2`; sign `-1` is supplied
by

\[
 -X^2+(\delta/4)Y^2\quad(D=1\bmod4),\qquad
 3X^2-(\delta/12)Y^2\quad(D=3\bmod4).                   \tag{5}
\]

All coefficients are integral over `Z_2`, all discriminants are `delta`,
and the respective negative signs are `(-1,delta)_2=-1` and
`(3,delta)_2=-1`. The **minus** sign in the last form corrects the printed
plus sign, confirmed on the original PDF p.13. At an odd `p|D`, a
nonsquare unit leading coefficient realizes the negative character;
the unit-leading diagonal form realizes the positive one. Gauss genus
theory supplies the global positive class, and its two-primary component
has the same characters. Thus (4) is obtained by one binary linear system.

Here is a direct check of the odd-prime cancellation in Proposition 15.
At `p|D`, write the local form of `Q` as `<p a> perpendicular U`, with
`a` a unit, and put `D'=D/p`, `k=(n-1)/2`. The terminal condition of L1
says that `U` has Witt index `(n-3)/2`, hence

\[
 \chi_p(a)=-\chi_p((-1)^{k+s}D').                       \tag{6}
\]

Write `T'` locally as `<p b> perpendicular <c>`, where
`bc=2D'` up to a unit square. Since its Hasse invariant is `chi_p(c)`,
target (4) gives the same formula for `chi_p(b)` as (6). Thus
`chi_p(ab)=1`. The radical binary form of `Q perpendicular (-T')` is
`diag(a,-b)`, so Lemma 8 removes the valuation 2 at `p`.
Use these Lemma-8 steps directly, as in the source's specialized
augmentation step, rather than first applying the generic odd-dimensional
Lemma-6 priority. They satisfy the same L1 lattice/HNF height bounds.

The augmented nine-dimensional determinant has absolute value `2D^2`.
After removing the odd primes, its dyadic valuation is 1 and its radical
dimension is 1. The nondegenerate quotient over `F_2` has even dimension
8 and admits a bilinear-isotropic subspace of dimension 4. Lemma 9
therefore removes the remaining factor 2, including its recorded scalar
division by 2. The resulting form is integral unimodular.

Its signature is `(5,4)` or `(4,5)`. L2 supplies an isotropic subspace of
dimension 4. Pull it back and intersect with the seven-dimensional
summand: the dimension is at least `4+7-9=2`. Keep a basis of this
intersection, not merely one vector, and pull it back through L1.
The source's stronger assertion of an exact/maximal intersection dimension
is unnecessary here; the lower bound is enough.

## 4. Dimension six and all signatures

Orient the input so `r>=s`. If its first minimization is unimodular, L2
already supplies a zero. Otherwise append the coefficient `-1` and use
the preceding seven-dimensional operation:

| Oriented six-dimensional signature | Seven-dimensional signature after orientation | Nine-dimensional signature if needed |
|---|---|---|
| `(5,1)` | `(5,2)` | `(5,4)` |
| `(4,2)` | `(4,3)` | `(4,5)` |
| `(3,3)` | `(4,3)`, after negating the appended form | `(4,5)` |

Each branch returns an isotropic subspace of the appended form of
dimension at least 2. After all backmaps, intersection with the original
six-dimensional summand has dimension at least `2+6-7=1`. Negating the
form does not change its zero set. A nonzero intersection vector, followed
by the initial backmap, solves the original six-dimensional equation.

There is no recursion cycle: dimension four uses a unimodular dimension-six
routine; the general dimension-six operation uses dimensions seven and
nine. All terminal unimodular operations are L2, including its full
isotropic-basis construction. No Algorithm 6 call in dimension five or
unproved indefinite-reduction subroutine is needed.

## 5. Polynomial bit clock and finite failure budget

All rational linear algebra, intersections, and backmaps have dimension
at most 9. L1 gives polynomial bit heights for its forms and maps. Each
binary discriminant therefore has polynomial bit length in the original
input. The repaired B--S backend returns polynomially many represented
generators with `O(log|delta|)`-bit reduced coefficients. The genus solve
uses exponents 0 or 1 and polynomially many compositions, reducing after
each. The augmented Gram matrices consequently have polynomial height.
There are only a constant number of such stages, so height bounds remain
polynomial after the final backmap and clearing denominators.

At most three L1 calls and one B--S call occur. The latter already includes
its polynomially many conic, modular-root, and extra factoring operations.
The initial determinant factorizations and any backend factorizations are
on polynomial-bit integers, and their number is polynomial. No claim that
only the original determinant is factored is required or made.

Give each L1 call abort allowance `eta/8` and the one B--S call allowance
`eta/4`. L2 and all remaining operations are deterministic. The union
bound is at most `5 eta/8 < eta`; the subroutines' finite clocks are
polynomial in the input size and `log(1/eta)`. The integer-factorization
oracle is exact in this statement. Finally check nonzeroness and the
original rational quadratic equation exactly before returning a vector.
An exhausted randomized search is `ABORT`, not a local obstruction.

The source also contains minor display errors: `disc(g)=delta`, not
`4 delta`, in Algorithm 5's step-8 explanation; Proposition 15's output
matrix has dimension `n+2`, not 4. Neither is used literally. With these
repairs and the explicit coordinate transports, no further assembly gap
remains for the stated dimension-four/six solver. This is a written
factoring-oracle classical algorithm, not an implementation or a claim of
classical polynomial integer factorization.
