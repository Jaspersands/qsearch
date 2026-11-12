# Factored quadratic norm conics: native backend admission

Date: 2026-11-13. Independent primary-source audit and proof repair.

**Admitted interface.** Given nonzero squarefree integers `d,t`, their
verified prime factorizations, and an error allowance `0 < eta < 1`, there is
a bounded-clock randomized classical algorithm that either correctly reports
that

\[
 x^2-dy^2=t z^2                                             \tag{1}
\]

has no nonzero rational solution, returns a nonzero integral solution, or
returns `ABORT`. Its bit cost is polynomial in the input bit length and
`log(1/eta)`; its abort probability is at most `eta`. Accepted answers are
exact. For nonsquare `d`, every returned solution has `z != 0`, and therefore
gives the explicit element `(x+y sqrt(d))/z` of norm `t`. No unit, class-group,
Pell, additional factorization, or selected-square-root oracle is used.

This is a factored-input classical backend. It does not remove the initial
factoring resource, and does not itself prove generation of `K(S,2)` or the
primitive-lift statement assigned to the separate descent review.

## Primary source and two necessary qualifications

Source: Cremona--Rusin, *Efficient solution of rational conics*, retained at
`research/audits/sources/quadratic_norm/cremona_rusin.pdf`. The original
numbered pages 3--4, 10, 16--17 were read visually; page 15 and the surrounding
text were also checked in the retained OCR.

- Sections 2.1--2.2, pp. 3--4: factored reduced diagonal coefficients,
  certificate criterion, and the certificate lattice (7).
- Lemma 2.3, p. 10: the Gaussian-integer gcd for the exceptional positive
  coefficients `a=b=1`.
- Section 2.6, pp. 15--17: the index-two lattice, weighted LLL, and the
  thirteen-vector lemma. The proof below supplies the strictness argument
  that is not printed there in detail.

There is a sign mismatch in the printed p. 17 basis: its positive
`gamma=v a' c k2` does not satisfy the p. 4 congruence `c z = k2 x (mod b)`.
Use negative `gamma`, as below, or compute the congruence kernel by integer
HNF. For example, `(a,b,c)=(1,5,-1), k2=1` makes the printed third vector
`(1,0,1)` violate that congruence. It belongs to the lattice with `-k2`
instead; hence this typo is harmless to conic solubility but should not be
copied into a certificate-preserving implementation.

Also, a shortest vector need not itself be isotropic in the exceptional
case: for `(a,b,c)=(1,1,-1)`, the index-two lattice is `D3`, and `(1,1,0)` is
shortest with quadratic value 2. The p. 16 sentence about shortest vectors
therefore requires the exceptional preprocessing explicitly mentioned on
that page. No unqualified shortest-vector assertion is used here.

## 1. Native reduction and certificate cost

Put `h=gcd(|d|,|t|)`. Since both inputs are squarefree, (1) is equivalent to

\[
 hX^2-(d/h)Y^2-(t/h)Z^2=0,
 \qquad (x,y,z)=(hX,Y,Z).                                  \tag{2}
\]

The three coefficients are pairwise coprime and squarefree. Conversely,
clearing denominators in (1) gives `h|x`, so (2) loses no rational point.
All its prime factors are inherited from the supplied lists. This single
gcd reduction is sufficient for the present interface; no recursive
squarefree factorization is needed. If all coefficients have one sign,
return `NO`. Otherwise permute and, if necessary, negate the equation to
obtain

\[
 Q(X,Y,Z)=aX^2+bY^2+cZ^2,
 \quad a,b>0>c,\quad T=|abc|,
 \quad abc\text{ squarefree}.                              \tag{3}
\]

As on pp. 3--4, solubility is equivalent to the existence of

\[
 k_1^2\equiv-bc\pmod a,\quad
 k_2^2\equiv-ca\pmod b,\quad
 k_3^2\equiv-ab\pmod {|c|}.                                \tag{4}
\]

At odd prime factors, compute Legendre symbols and square roots by
Tonelli--Shanks, then use CRT. The inputs to each symbol are units because
the diagonal coefficients are pairwise coprime. At 2 the required square
root modulo 2 is immediate. There is no missing 2-adic condition: the
source's real-plus-odd-prime criterion uses Hilbert reciprocity to account
for the remaining place. A failed Legendre test is an exact `NO`.

For a fixed clock, let `q` be the number of distinct odd prime factors.
For each such prime `p`, draw `b=ceil(log2 p)` independent bits and regard
them as a trial integer. Accept a trial only if it is in `[1,p-1]` and its
Euler criterion is `-1`. At least one quarter of the `2^b` strings pass.
Allow

\[
 R=4\left\lceil\log_2\frac{4(q+1)}{\eta}\right\rceil
\]

trials per prime. Exhaustion means `ABORT`, not `NO`; the union abort
probability is at most `q(3/4)^R < eta`. Once the nonresidue is found,
Tonelli--Shanks is deterministic. Verify every returned root and the CRT
congruences exactly. A cached nonresidue can be reused for every conic using
the same prime. Thus the only randomness has a paid finite clock and
cannot produce a false answer.

## 2. Explicit integral lattices

Use exactly the source's lattice

\[
 L=\{(X,Y,Z)\in\mathbf Z^3:
 bY=k_1Z\ (a),\ cZ=k_2X\ (b),\ aX=k_3Y\ (c)\}.
\]

Its index is `T`, and `T|Q(v)` for `v in L`. A corrected explicit basis is
obtained from extended gcds

\[
 ub+vc=1,\qquad aa'+bc b'=1,
\]
\[
 \alpha\equiv b'c k_1\pmod a,\qquad
 \beta\equiv ua'b k_3\pmod {bc},\qquad
 \gamma\equiv- va'c k_2\pmod {bc},
\]
\[
 v_1=(bc,0,0),\quad v_2=(a\beta,a,0),\quad
 v_3=(\alpha\beta+\gamma,\alpha,1).                         \tag{5}
\]

For example, `gamma=-a^{-1}k2 (mod b)` gives
`k2 gamma=c (mod b)`, the sign needed by (7). The other congruences follow
directly, and the determinant is `abc`. Least absolute or nonnegative
residues give basis entries of magnitude at most `2T`.

The map `epsilon(v)=Q(v)/(abc) mod 2` is additive on `L`. Indeed, the
bilinear form `aXX'+bYY'+cZZ'` is divisible by each of `a,b,c`, using (4)
and the defining congruences. It is therefore divisible by `abc`, including
its possible factor 2. The vectors `(bc,0,0),(0,ac,0),(0,0,ab)` show that
`epsilon` is onto: their images are `bc,ac,ab mod 2`, at least one odd.
Thus

\[
 L'=\ker\epsilon,\qquad [\mathbf Z^3:L']=2T,
 \qquad Q(L')\subseteq 2T\mathbf Z.                        \tag{6}
\]

Choose a basis vector `v_i` with odd epsilon; replace it by `2v_i`, and
replace each other odd-epsilon vector by `v_j-v_i`. This is an explicit
basis of `L'`, with entries bounded by `4T`.

## 3. Gauss equality, exceptional case, and exactly thirteen tests

Give `L'` the positive norm

\[
 \|v\|_+^2=aX^2+bY^2+|c|Z^2.
\]

Its Euclidean covolume in these weighted coordinates is `2T^(3/2)`.
The three-dimensional Gauss--Hermite inequality used by Section 2.6,
`lambda_1^2 <= 2^(1/3) covolume^(2/3)`, gives

\[
 \lambda_1^2\le 2T.                                      \tag{7}
\]

Here is an elementary treatment of equality, requiring no classification
of extremal lattices. At equality the minimal vectors span the ambient
three-dimensional real space: otherwise stretch their span slightly and
shrink its orthogonal complement at fixed determinant. The gap to the
next length and discreteness ensure that this increases the minimum,
contradicting (7).

If no minimal vector had `Q=0`, (6) and `|Q(v)|<=||v||_+^2=2T` would force
every minimal vector into either the positive plane `Z=0` or the negative
axis `X=Y=0`. Spanning then supplies two independent planar minima `u,v`
and an axial minimum `w`. Since `u+v,u-v` cannot be shorter,
`|cos(theta)|<=1/2`. The index of their sublattice would be

\[
 \frac{(2T)^{3/2}|\sin\theta|}{2T^{3/2}}
 =\sqrt2|\sin\theta|
 \in[\sqrt{3/2},\sqrt2],
\]

which contains no integer. This contradiction gives an isotropic minimum.
For that vector, equality implies `2|c|Z^2=2T`, hence `Z^2=ab`. Because
`a,b` are positive, coprime, and squarefree, this is possible only when
`a=b=1`. Consequently, for every other reduced input,

\[
 \lambda_1^2<2T,\qquad Q(v_{\min})=0.                     \tag{8}
\]

If `a=b=1`, use the actual Lemma 2.3 algorithm: compute a Gaussian gcd
`x+iy=gcd(k3+i,c)`. Its norm is `|c|`. At an odd prime dividing squarefree
`c`, the two conjugate Gaussian primes cannot both divide `k3+i`; exactly
one enters the gcd. If `2|c`, `k3` is odd and `v_2(k3^2+1)=1`, giving the
single required Gaussian factor above 2. Thus `(x,y,1)` solves (3).
Nearest-integer Gaussian division decreases the squared norm by a factor
at most `1/2` at every nonterminal step, so this is polynomial bit cost,
not a Pell computation. It also preserves the chosen certificate.

Otherwise run ordinary exact LLL with `delta=3/4` on the integral weighted
Gram matrix of the basis of `L'`. No irrational square roots of weights
are represented. For its output basis `b1,b2,b3`, put `B_i=||b_i^*||^2`.
The source's Lemma 2.7 uses `|mu_ij|<=1/2` and `B1<=2B2<=4B3`.
If a vector is strictly shorter than `b1`, its third coefficient has
absolute value at most 1; its second also does, since for third coefficient
`+/-1` one has `(n2+mu32 n3)^2<3/2`. Finally
`|n1+mu21 n2+mu31 n3|<1` gives `|n1|<=1`. This last deduction completes the
omitted final line of the printed proof. If `b1` is already shortest, it
is itself in the same list.

Therefore a shortest vector occurs among the 26 nonzero coefficient
triples in `{-1,0,1}^3`, or exactly 13 up to sign. Evaluate their weighted
lengths and `Q` exactly. By (8), a shortest one is a conic solution. The
Gaussian branch removes the tie issue before this argument is used.

## 4. Bit clock, output height, and remaining scope

Let `B=2+bitlength(|d|)+bitlength(|t|)`; the inherited prime lists have
total bit length `O(B)`. All gcd, CRT, and lattice input integers have
`O(B)` bits. The `L'` basis has entries at most `4T`, and its weighted
Gram entries have absolute value at most `48T^3`, also `O(B)` bits.

In fixed rank 3, exact LLL has a polynomial bit clock, not merely a
real-arithmetic clock. More concretely, its integral prefix-Gram
determinant potential starts at `2^{O(B)}`, is at least 1, and each swap
decreases it by a factor at most `3/4`. There are `O(B)` swaps and
size-reduction stages. Gram--Schmidt lengths stay below the initial
maximum, and their positive denominators are bounded prefix determinants;
all size-reduction quotients and intermediate coordinates therefore have
`O(B)` bits. Fixed-dimensional rational operations suffice throughout.
This gives a polynomial bit bound directly for this weighted input.

For the other operations, each Tonelli--Shanks call uses `O(B^2)` modular
multiplications, there are at most `O(B)` prime factors, and every
nonresidue trial uses `O(B)` modular multiplications. All have `O(B)`-bit
operands. Gaussian gcd, extended gcd, CRT, and the thirteen tests obey
smaller polynomial bounds. For example,
`O((B+1)^8 (1+log(1/eta)))` is a deliberately loose common schoolbook-bit
upper bound for this entire backend, with the verified factorizations
provided. Its randomized portion is bounded by the explicit `R` above.

For nonsquare `d`, the chosen solution satisfies `||v||_+^2<=2T`, including
the Gaussian branch. Undoing the permutation, global sign, and (2) gives
the useful explicit bounds

\[
 |x|\le\sqrt{2|dt|},\qquad
 |y|\le\sqrt{2|t|},\qquad
 |z|\le\sqrt{2|d|}.                                      \tag{9}
\]

Dividing by the integer gcd produces a primitive triple without increasing
height. For nonsquare `d`, `z=0` would force the entire triple to vanish,
so the rational norm element is available with `O(B)`-bit numerators and
denominator. The split case `d=1`, if allowed, is handled directly by
`(x,y,z)=(t+1,t-1,2)`.

Thus the native conic call is admitted with inherited factoring, bounded
randomness, exact certificates, explicit small output, and no intermediate
factorization. The broader quadratic `S`-squareclass generation and the
ideal/class interpretation of these norm lifts remain separate proof
obligations; this source audit does not silently identify them with conic
solubility.
