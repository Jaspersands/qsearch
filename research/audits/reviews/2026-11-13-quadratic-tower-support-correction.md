# Quadratic towers: constructive correction of outside-support parities

2026-11-13. Independent algebraic and bit-interface review. No external
source claim about relative conic solving is admitted here.

**Disposition: the proposed support correction is sound.** It gives the
full norm sequence below when the ordinary `S`-ideal class group has odd
order. It is constructive without computing that class group or
principalizing an ideal. The resources are the proved quadratic
squareclass compiler, an explicitly charged integer-factorization oracle
on additional polynomial-size integers, and polynomial-size outputs from
the separately supplied relative conic solver.

## Exact hypotheses and sequence

Let `F=Q(sqrt(D))` be quadratic and `L=F(sqrt(d))` a quadratic field
extension, with native exact coordinates for `d`. Let `S_Q` contain 2,
the primes dividing `disc(F)`, and all rational primes below finite primes
ramified in `L/F`. Let `S` contain **all** primes of `F` above `S_Q`, and
`S_L` all primes of `L` above `S`. No sign condition is imposed in the
definition of an `S`-squareclass.

Assume

\[
 \operatorname{Cl}(\mathcal O_{F,S})/2=0.                 \tag{1}
\]

Odd ordinary class number of `F` is sufficient, and is stronger than (1).
No narrow-class-group hypothesis is needed. Put

\[
 V=\{[a]\in F(S,2):a\in N_{L/F}(L^*)\}.
\]

Being a norm is well defined on squareclasses since every `F`-square is
the relative norm of an element of `F`. Then the exact sequence is

\[
 0\longrightarrow F(S,2)/\langle[d]\rangle
 \xrightarrow{\mathrm{res}}L(S_L,2)
 \xrightarrow{N_{L/F}}V\longrightarrow0.                \tag{2}
\]

For the constructive assertion, assume the relative solver supplies, for
each chosen norm-basis representative `a`, exact `x,y,c in F`, `c!=0`, with

\[
 \beta=x+y\sqrt d\ne0,\qquad N_{L/F}(\beta)=a c^2,       \tag{3}
\]

and expanded coordinate bit lengths polynomial in its inputs. An exact
solver with no output-height or running-time bound would not by itself
supply the claimed polynomial algorithm.

## Kernel and ramification checks

For a prime `P` outside `S`, the extension is unramified, so
`v_Q(d)=v_P(d)=2v_Q(sqrt(d))` at any `Q|P`. Hence `v_P(d)` is even, and
`[d] in F(S,2)`. The kernel of restriction on all squareclasses is exactly
`<d>`: expanding `(u+v sqrt(d))^2 in F` gives `2uv=0`. Thus the first map
in (2) is injective.

Norm maps `L(S_L,2)` into `F(S,2)` because
`v_P(N beta)=sum_{Q|P} f(Q/P)v_Q(beta)` is even outside `S`. If a class in
this domain has square norm, write `N beta=c^2`. Unless `beta=-c`,

\[
 (\beta+c)^2=(\operatorname{Tr}_{L/F}\beta+2c)\beta.      \tag{4}
\]

The nonzero factor on the right belongs to `F`; (4) identifies its
restriction squareclass with `[beta]`. If `beta=-c`, use that element of
`F` directly. For the resulting `u in F*`, equality of squareclasses gives
`v_Q(beta)=v_P(u) mod 2` outside `S`, since the ramification index is 1.
Therefore `[u] in F(S,2)`. This proves exactness at the middle term without
any class-group hypothesis or integral-coordinate primitivity assertion.

## Outside-support parity is pulled back from the base

For (3) and `P` outside `S`, a split prime has two valuations satisfying

\[
 v_{Q_1}(\beta)+v_{Q_2}(\beta)
   =v_P(a)+2v_P(c)\equiv0\pmod2.
\]

Their parities agree. At an inert prime there is only one parity. Because
the extension is unramified, pullback of `P` has exponent 1 at every
`Q|P`; in both cases there is a well-defined common parity `r_P`.
Only finitely many `r_P` are nonzero. Thus the outside-`S` parity divisor
of `beta` is the pullback of

\[
 J=\prod_{P\notin S}P^{r_P}.                             \tag{5}
\]

Ramification would invalidate this argument: pullback would have exponent
2, so multiplication by a base element could not change an odd valuation
above that prime. Such primes are explicitly in `S`.

There is an economical native formula requiring no arithmetic in local
fields of `L`. Set `k=v_P(d)/2`. With `v_P(0)=+infinity`,

\[
 r_P=\min\{v_P(x),v_P(y)+k\}\pmod2.                     \tag{6}
\]

Indeed, normalize `d` by a uniformizer to obtain a unit `delta`, and
write `beta=pi^r(X+Y sqrt(delta))`, where `r` is the minimum in (6) and
at least one of `X,Y` is a unit. At an inert unramified prime, reduction
of `1,sqrt(delta)` is a residue-field basis, so the valuation is exactly
`r`. At a split prime the two factors are `X+Y s` and `X-Y s`; at least
one is a unit because 2 is a unit. Their norm has even valuation by (3),
so the other factor has even valuation. Both valuations consequently
have parity `r`. This covers negative valuations and zero coefficients.
Here the rational prime below `P` is itself a local uniformizer, because
all primes ramified in `F/Q` belong to `S`.

## Exact surjectivity and construction of the correction

For any finite `T superset S`, define

\[
 v_{T\setminus S}:F(T,2)\longrightarrow
       \mathbf F_2^{T\setminus S}
\]

by valuation parities at the individual prime ideals. The obstruction for
a vector `r` to lie in this image is precisely

\[
 [\prod_{P\in T\setminus S}P^{r_P}]
       \quad\text{in }\operatorname{Cl}(\mathcal O_{F,S})/2. \tag{7}
\]

For necessity, a principal divisor with this parity equals that divisor
plus twice a divisor outside `S`. Conversely, if `[J]=2[H]` in the
ordinary `S`-class group, then `J H^{-2}` is principal modulo an ideal
supported in `S`. Its generator has the required parities and has even
valuations outside `T`, so represents a member of `F(T,2)`. This is an
existence proof, not a principalization subroutine. Assumption (1) makes
the valuation map **surjective**.

Now let `T_Q` be the rational-prime enlargement described below, and take
`T` to contain all primes of `F` above it. Compute the complete basis
`xi_1,...,xi_m` of `F(T,2)` using
`QUADRATIC_NATIVE_SQUARECLASSES.md`. Form the binary matrix

\[
 M_{Pj}=v_P(\xi_j)\bmod2\quad(P\in T\setminus S).
\]

It has full row rank by (7). Solve `M e=r` over `F_2` and set
`gamma=product_j xi_j^{e_j}`, with exponents 0 or 1. Then

\[
 \widetilde\beta=\beta\gamma\in L(S_L,2),\qquad
 N\widetilde\beta=a(c\gamma)^2.                          \tag{8}
\]

At primes outside `T` both factors have even valuations; at primes of
`T\S` the two matching parities cancel. At primes in `S` there is no
condition. This proves surjectivity in (2) constructively. It uses neither
the order of the class group nor a generator of `J H^{-2}`.

Every prime above a selected rational prime must be a row of `M`.
In particular, if one of two split `F/Q` primes is not in the support of
`beta`, its required target is zero; it must not be omitted from the
linear system.

## Native support discovery, exact valuations, and bit accounting

Use the explicit integral basis `1,omega` of the quadratic field `F`.
Choose a positive integer `M0` with `M0 d in O_F`. Then
`theta=M0 sqrt(d)` is integral, and
`O_F[theta]` is an explicit rank-four order contained in `O_L`; no maximal
order of `L` is needed. Write `beta=x+(y/M0)theta`, and choose a positive
integer `R` clearing these four rational coordinates. Thus `R beta` is
integral. Factor the nonzero integer

\[
 R\,|N_{L/\mathbf Q}(R\beta)|.                           \tag{9}
\]

Let `E_Q` be its prime support outside `S_Q`, and put `T_Q=S_Q union E_Q`.
For a rational prime outside this set, the integral element `R beta` has
unit norm and `R` is a unit. Hence every valuation of `beta` above it is
zero. The norm and denominators in (9) have polynomial bit length in the
explicit field and conic-output coordinates. Cancellation in the norm of
a fractional element is why denominators are cleared **before** forming
this support bound.

Integer factorization of (9) is an additional charged call. It is not
covered by the claim that the original bad-prime factorization alone
suffices for the quadratic base-field algorithm.

At any new rational prime `q`, `F/Q` is unramified and `q` is odd. Its one
or two prime ideals are computed by the quadratic residue test for `D`
and, in the split case, a modular square root. For an exact field element
`u=(A+B omega)/C`, the inert-prime valuation is
`min(v_q(A),v_q(B))-v_q(C)`. At a split prime, lift the corresponding
simple root of the minimal polynomial of `omega` modulo `q` to
`q^(e+1)`, where `e=v_q(N(A+B omega))`. Evaluating `A+B omega` there gives
the exact numerator valuation, which is at most `e`; subtract `v_q(C)`.
Zero elements are handled separately. This supplies the valuations in
(6) and every entry of `M` using only quadratic-field arithmetic.

These root lifts have polynomial precision: `(e+1)log q` is bounded by
the norm bit length plus `log q`. Norm valuations at known primes use
division, not factorization. The finite modular-root searches use the
bounded-confidence clock in the conic backend review. No prime ideals,
uniformizers, unit generators, or embeddings are supplied as advice.

For all norm-basis lifts, take the union of their sets `E_Q` and compute
one enlarged basis and one valuation matrix. There are polynomially many
primes: the sum of their logarithms is bounded by the bit lengths of the
integers (9). The quadratic compiler returns at most `2|T_Q|+1` basis
elements, each with polynomial-size coordinates. Binary linear algebra
is polynomial. A product of a subset of these elements has logarithmic
height at most the sum of their heights; in the fixed quadratic basis its
expanded rational coordinate length is polynomial as well. The same
holds for `beta gamma` in the fixed quartic basis. Thus correction does
not hide a huge unit, exponent, or expanded numerator.

## Basis output and exact remaining scope

The corrected lifts of a basis of `V`, together with a basis of
`F(S,2)/<d>`, form a basis of `L(S_L,2)`: independence follows by first
taking norms and then using the restriction kernel. In particular,

\[
 \dim L(S_L,2)=\dim F(S,2)-1+\dim V.                      \tag{10}
\]

Expressing `[d]` in the constructed quadratic basis requires no abstract
squareclass-coordinate oracle. The base algorithm records which basis
elements lift each rational norm-basis vector. Compute the rational norm
squareclass of `d`, solve for those coordinates, and divide by the indicated
lift product. The remaining element has square rational norm; take that
rational square root exactly and apply (4) for `F/Q`. Its rational factor
has squareclass supported in `S_Q`, whose sign and prime parities give the
remaining coordinates modulo `<D>`. This yields a nonzero coordinate
vector for `[d]`; ordinary binary elimination selects the quotient basis.
All products here also involve only polynomially many bounded-size
elements.

The reviewed result is the full support-correction and norm-sequence
bridge. To claim the entire quartic algorithm, separately pay computation
of the norm subspace `V` and the relative conic solver with polynomial
running time and explicit coordinate heights. The parent is auditing that
source. Without (1), the exact additional obstruction is (7), not a
generic need for the whole class group. Under (1), no such computation is
needed. Extra integer factorization remains an explicit resource.
