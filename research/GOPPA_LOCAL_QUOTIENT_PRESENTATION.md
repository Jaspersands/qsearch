# Public Exterior Presentation Of Local Jet Relations

Date: 2026-10-30. Status: exact algebraic presentation and bounded regression
controls. This note supplies neither a new quotient algorithm nor an
asymptotic lower bound. It makes no candidate or quantum-advantage claim.

## Source, Scope, And Conventions

The source is Stephen A. Weis, *Improving GIJS Key Recovery for Classic
McEliece*, ePrint 2026/1984, version 0.5, October 2026. The local snapshot is
[the full paper](literature_cache/eprint_2026_1984_v05.pdf), SHA-256
`822d2cd3cc515143072a543f1bb743ea9b29651d5be03dd56f948e157d196652`.
Page references below are printed page numbers, which equal one-based PDF
page numbers in this 37-page snapshot. No later version is assumed.

Relevant source statements:

- Section 2, pp. 4-5: the full jet matrix and its two kernels.
- Section 5.1, p. 9, and Appendix A, pp. 23-24: canonical interpolation
  relations and their support-dependent lift.
- Section 5.2, pp. 9-10, and Appendix A, p. 24: Proposition 6's local
  relations; Assumption 3 is an additional exhaustion/dimension hypothesis.
- Section 5.3, p. 11: blockwise removal of relations and locator readout.
- Section 6, p. 12, and Table 7, p. 21: matrix-free products are not a
  small quotient algorithm; the estimated sparse Step-2 solver is untested.

The algebraic deductions below are derived here from the full public jet
operator. They do not assume the dimension heuristics or a known Goppa key.
The public point coordinates remain in the supplied systematic basis; no
unannounced change of basis of the multilinear forms is made.

Write `k = k_ell` for the shortened public dimension, and let `P` be the
number of constraint blocks, including the public sum point `w` when used.
Fix `1 <= s_j < d <= k` for each block. Unlike the distinguisher's omitted
point, Section 5's held-out points DO carry jets of multiplicity `s'`.
All vector spaces and products below are over `F_2` until explicitly extended.

## 1. Square-Zero Algebra And The Exact Block Map

Let

\[
A=\mathbf F_2[x_1,\ldots,x_k]/(x_1^2,\ldots,x_k^2),\qquad
x_S=\prod_{i\in S}x_i.
\]

The monomials `x_S` form a basis. Multiplication is disjoint union of index
sets, with zero for an overlap and XOR for repeated terms. In characteristic
two this is an exterior algebra: commutation has no minus sign, but squares
of linear forms are still zero. It is NOT the Boolean function algebra
`F_2[x]/(x_i^2-x_i)`. We use it to encode condition coefficient vectors, not
to evaluate the original polynomial at Boolean points.

For a public point `y_j`, define

\[
g_{j,r}=[z^r]\prod_{i=1}^k(1+y_j[i]x_i z),\qquad
g_{j,0}=1,\qquad e_j=d-s_j+1.
\]

Put `g_{j,r}=0` outside `0 <= r <= k`. The coefficient space of the full
block and its map to condition vectors are

\[
C_j=\bigoplus_{u=0}^{s_j-1}A_u,\qquad
\mu_j((f_u)_u)=\sum_{u=0}^{s_j-1}g_{j,d-u}f_u\in A_d.
\tag{1}
\]

For a derivative label `S` of size `u`, the coefficient of `x_B` in
`mu_j(x_S)` is

\[
[x_B](x_Sg_{j,d-u})
=\mathbf1_{S\subseteq B}\prod_{i\in B\setminus S}y_j[i].
\tag{2}
\]

This is exactly the full jet column in Weis, p. 4. Thus the map
`E: direct_sum_j C_j -> A_d` is `sum_j mu_j`, with no transpose ambiguity:
its kernel consists of relations among conditions, not vanishing forms.
In particular, internal relations at `j` are exactly `ker(mu_j)`.

For the homogeneous ideal

\[
I_j=(g_{j,e_j},g_{j,e_j+1},\ldots,g_{j,d})\subseteq A,
\]

equation (1) gives `im(mu_j)=(I_j)_d`, hence

\[
C_j/\ker\mu_j\simeq(I_j)_d.
\tag{3}
\]

This includes degenerate public points. A unit point contributes zero when
`s_j<d`, since all its `g_{j,r}` with `r>=2` vanish. Including zero blocks
does not invalidate the identities. No general-position promise is needed.

## 2. Pair Relations Are Ideal Products

Fix distinct blocks `a,b`, integers `i>=e_a`, `i'>=e_b` with `i+i'<=d`,
and a monomial `x_C` of degree `d-i-i'`. In `C_a` take

\[
x_Cg_{b,i'}\quad\text{in its degree }d-i\text{ summand},
\]

and in `C_b` take `x_Cg_{a,i}` in its degree `d-i'` summand. These are valid
derivative orders. Both block images equal

\[
x_Cg_{a,i}g_{b,i'}\in A_d.
\tag{4}
\]

Their sum is therefore in `ker(E)`. Expanding the first expression gives
exactly `g_{a<-b}(C)` of Proposition 6, p. 10: the terms are derivative
labels `C union U` for `U` in the support of `b`, `|U|=i'`, disjoint from
`C`. Appendix A, p. 24, proves the same relation using commuting Hasse
operators.

As all degrees and `C` vary, (4) spans precisely `(I_a I_b)_d`. Indeed,
every degree-`d` element of the product ideal is a sum of these products
with homogeneous multipliers, and those multipliers expand in monomials.
Thus the projected pair relations at block `a`, after internal relations
are removed, have image `(I_a I_b)_d`.

Always `I_a I_b subseteq I_a intersection I_b`, but equality of their
degree-`d` parts has NOT been assumed. In particular, we do not silently
replace Proposition 6's generated relations by all possible two-block
relations. Weis reports finite-size failures of exhaustion on p. 10.

## 3. The Exact Step-2 Block Quotient

Let `T_j` be the span in `C_j` of the unit coordinate vectors for derivative
orders `0 <= u <= s_j-s'`. If the upper bound is negative, `T_j=0`.
For a held-out block `s_j=s'`, this is exactly its value coordinate. This
matches the discarded support-free conditions of Section 5.3, Step 2,
p. 11. For the usual `s'>=1`, define

\[
J_j=(g_{j,r}:d-s_j+s'\le r\le d),
\tag{5}
\]

with an empty generating range giving the zero ideal. Equation (1) gives
`mu_j(T_j)=(J_j)_d`. Also `J_j subseteq I_j`, since its lower index is
`e_j+s'-1`.

Let `L_j` be the sum of the internal relations, projections of all
Proposition 6 relations involving `j`, and `T_j`. By (3)-(5), the first
isomorphism theorem gives

\[
\boxed{
Q_j:=C_j/L_j\simeq
\frac{(I_j)_d}
{\left(I_j\sum_{b\ne j}I_b+J_j\right)_d}.
}
\tag{6}
\]

This is an exact finite-dimensional quotient presentation over public data.
It does not assert that all cosets can be reduced or represented efficiently.
The denominator is homogeneous and contained in the numerator. Crucially,
`T_j` need not consist of kernel vectors; it is a blockwise readout quotient,
not an additional subspace one may automatically divide out of `ker(E)`.

## 4. A Short Complex And Which Dimension Is Small

Define `K_loc^gen` to mean exactly the span of internal relations and
Proposition 6's pair relations, without any extra exhaustion assertion.
After the internal quotient, consider

\[
D_2=\bigoplus_{a<b}(I_a I_b)_d
\xrightarrow{\delta_2}
D_1=\bigoplus_j(I_j)_d
\xrightarrow{\delta_1}D_0=A_d.
\tag{7}
\]

On the `(a,b)` summand, `delta_2(x)` has `x` at both endpoints and zero
elsewhere; `delta_1` sums all entries. Characteristic two gives
`delta_1 delta_2=0`. Equation (3) identifies the global kernel modulo
internal relations with `ker(delta_1)`; equation (4) identifies the remaining
generated local relations with `im(delta_2)`. Therefore

\[
H_1(D_\bullet)=\ker\delta_1/\operatorname{im}\delta_2
\simeq\ker(E)/K_{\mathrm{loc}}^{\mathrm{gen}}.
\tag{8}
\]

No exactness at the middle term, nor at either endpoint, is claimed.
The terms in (7) are ideal subspaces, not free modules with an already
computed small basis. Naming the ideals does not construct such bases.

Restriction to a block followed by (6) gives a well-defined map

\[
\theta_j:H_1(D_\bullet)\longrightarrow Q_j.
\tag{9}
\]

Under the applicable single-run hypotheses, Assumption 3 (p. 10) predicts
`dim H_1 = ms'`. Step 2 (p. 11) predicts dimension `(s'-1)m` for the
projected kernel image used at the locator blocks, namely `im(theta_j)`.
It does NOT assert `dim Q_j=(s'-1)m`. A finite sample of kernel vectors
must also span the needed image before its observed dimension equals that
of the full image. General position, the no-slack setup, and the other
stated hypotheses must not be dropped. Extra small-`t` or short-dual-word
relations are explicitly discussed on p. 10 and pp. 27-28.

In particular, Theorem 5 uses `s'-1>=2` a power of two and the exact count
`sum_j s_j+s_infinity = d D_ell+1-t+s'`, with
`D_ell=n_ell-2t-1`; its useful canonical relations require good held-out
columns. Assumption 3 applies to its stated parameter regime and excludes
dual codewords of weight at most `2d-2`. Its discussion additionally relates
the univariate count to a good held-out column and `R_d=D_d`. None of these
conditions follows from the ideal presentation itself. The source's
`R_d,D_d` here are univariate spaces, not the complex terms in (7).

## 5. Exterior Divided Powers, Not Ordinary Powers

Set `ell_j=g_{j,1}` and `omega_j=g_{j,2}`. For any quadratic exterior form
`omega=sum_{a<b} w_ab x_a x_b`, define `gamma_r(omega)` by taking the
Pfaffian of the alternating coefficient matrix on each `2r`-element subset.
Equivalently, its coefficient is the sum over perfect matchings of that
subset of the products of the matched `w_ab`. This definition uses no
division by `r!`; all matching signs are `+` in characteristic two.

For `omega_j`, each perfect matching on `B` contributes the same product
`product_{i in B} y_j[i]`. There are `(2r-1)!!` perfect matchings, an odd
number. Consequently

\[
g_{j,2r}=\gamma_r(\omega_j),\qquad
g_{j,2r+1}=\ell_j\gamma_r(\omega_j).
\tag{10}
\]

The odd identity follows because each odd-sized subset is produced `2r+1`
times. More generally, counting disjoint choices proves

\[
g_{j,a}g_{j,b}=\binom{a+b}{a}g_{j,a+b}
\quad\text{with the binomial coefficient reduced modulo two}.
\tag{11}
\]

At degree seven, (10)-(11) reduce the ideal generators to

\[
I_j=(\omega_j,\gamma_2(\omega_j))\quad(s_j=6),\qquad
I_j=(\ell_j\omega_j,\gamma_2(\omega_j))\quad(s_j=5).
\tag{12}
\]

For example, `g_3=ell*g_2`, `g_5=ell*g_4`, `g_6=g_2*g_4`, and
`g_7=ell*g_2*g_4`. These are finite-generator identities for the ideals
defined above, not a computed quotient normal form.

### Counterexample To A Quadratic-Only Replacement

Take `k=13`, `y=(1,...,1)`, and `f=x_1 x_2 x_3`. In the full square-zero
algebra, not an algebra truncated at degree seven, equation (11) gives

\[
g_2^2=0,\qquad g_2g_4=g_6,\qquad
g_2(g_4f)=g_6f\ne0.
\tag{13}
\]

The last polynomial has one term for each six-element subset of the other
ten variables, so it has 210 distinct degree-nine monomials. An even number
of distinct monomials is not the zero polynomial over `F_2`.
If `g_4f=g_2u` for some `u in A_5`, multiplication by `g_2` would make
the left side of (13) zero. Hence

\[
g_4f\notin g_2A_5,
\]

although `g_4f` is in the actual degree-seven block ideal for `s=6`.
The witness uses higher-degree multiplication to disprove a degree-seven
equality; no degree-seven coefficient matrix is necessary.

This disproves only the stated quadratic-only replacement. It is not a
Goppa key fixture or a counterexample to Assumption 3. Moreover, every
positive-degree element of `A` squares to zero, so an ordinary nonzero
regular sequence in `A` is unavailable. This does not rule out useful
truncated complexes, divided-power resolutions, or other compressions.

## 6. Public Input And Computational Obligations

All of (1)-(13) use only the explicit binary public points and the integers
`d,s_j,s'`. The original public matrix, shortening procedure, and public
sum point can supply those points without secret support. The relations
hold whether or not they arise from a Goppa code.

The generating polynomial for `g_{j,r}` has an `O(kd)` truncated coefficient
recurrence per point. This counts arithmetic-circuit description gates for
formal polynomials. It does not charge an arbitrary element of `A_d` as a
unit-cost machine word: expanded, that element has `binom(k,d)` bits.
Likewise, a polynomial-size description of (7) is not a polynomial-size
effective homology computation. Multiplication on descriptions, coefficient
contraction, ideal membership, and quotient reduction are distinct tasks.

One sufficient unresolved public primitive is a uniform construction of
polynomial-size descriptions of maps

\[
F_j:Q_j\longrightarrow\mathbf F_2^{O(ms')}
\]

that are injective on `im(theta_j)`, together with an algorithm evaluating
these maps on the compressed kernel representatives actually produced.
For block coefficients `v_{j,S}`, that evaluation means computing

\[
\sum_{|S|<s_j}v_{j,S}
F_j([x_Sg_{j,d-|S|}])
\tag{14}
\]

without enumerating all derivative coordinates. It must preserve the linear
relations needed by the branch-selection and locator-ratio steps. Supplying
only a circuit for one summand in (14) does not supply the contraction.
Producing the compressed kernel representatives is a separate obligation.
This is a sufficient specification, not a necessity theorem for every route.

An alternative small-complex construction would need computable maps
inducing the required homology isomorphism and block readouts. Equal
dimensions alone would not identify those maps. All complexity bounds must
be uniform in the original public-input bit length and `m`, with the
dependence on `d,s_j,s'` stated. Treating `d` as a fixed constant hides that
dependence when it grows with `m` (see Weis, p. 22).

The small univariate space in the source is not a public implementation
of this primitive. Appendix A, p. 24, writes the lift using coefficients
`c_{j,u,S}` that depend on the hidden curve `p` and has
`c_{j,0,empty}=lambda_j^{-d}`. The proof establishes the existence of
relations; using those coefficients computationally without recovering or
otherwise publicly realizing them would assume missing key-dependent data.

Thus this note establishes a public symbolic presentation, not a new
classical or quantum algorithm, or a universal computational barrier.

## 7. A Characteristic-Preserving CSS Encoding And Its Costs

This section is an elementary consequence of the public binary maps, not
an algorithm asserted by Weis. Write `E:F_2^J -> F_2^N`, `R=rank(E)`,
`K=ker(E)`, and `L=K_loc^gen subseteq K`. Set `r_log=dim(K/L)`; this
symbol is distinct from the locator order `s'-1`. The induced surjection
`[v] -> Ev` gives the exact sequence

\[
0\longrightarrow K/L\longrightarrow\mathbf F_2^J/L
\longrightarrow\operatorname{im}E\longrightarrow0,
\qquad
\dim(\mathbf F_2^J/L)=R+r_{\mathrm{log}}.
\tag{15}
\]

Only under the applicable Assumption 3 is `r_log=ms'`. Quotienting local
relations alone leaves the rank-`R` syndrome directions as well as the
logical quotient. In particular, the ambient quotient is not automatically
an `ms'`-dimensional space. The extra blockwise `T_j` in (6) cannot simply
be included in `L`, since it need not lie in `K`.

For `v in K`, the normalized binary coset states are

\[
|[v]\rangle_L=|L|^{-1/2}\sum_{\ell\in L}|v+\ell\rangle.
\tag{16}
\]

They are stabilized by `X^ell` for `ell in L` and by `Z^z` for
`z in row(E)`. These operators commute because `z dot ell=0`. There are
`2^r_log` orthogonal logical basis states on **J physical qubits** in this
coefficient-register construction. The code preserves binary parity; it
does not replace XOR linear algebra by complex matrix multiplication.
Equation (16) alone provides neither preparation circuits nor a compressed
physical encoding, and this register count is not a lower bound on other
encodings.

Starting from the uniform state `|+>^J` already satisfies all `X` checks.
Measuring the independent `Z` checks and postselecting the zero syndrome
succeeds with probability

\[
|K|/2^J=2^{-R}.
\tag{17}
\]

For an observed syndrome `s in im(E)`, an `X^c` correction to the zero
syndrome requires a solution of `Ec=s`. Public binary Gaussian elimination
can supply correction and encoding data at its explicit cost. Preparation
after that elimination is not, by itself, a new advantage over doing the
binary algebra classically. Equation (17) describes this particular
postselection procedure, not every possible preparation method.

A public binary linear map `F` with `F(L)=0` permits a coherent readout
`|v>|0> -> |v>|Fv>`. It is constant on each coset in (16), so it can reveal
logical information without full state tomography; to distinguish all
logical basis cosets its restriction to `K/L` must be injective. But
constructing a suitable `F`, implementing it on the represented input,
and ensuring the required locator readout are not free. This is the same
kind of construction/evaluation obligation as (14). None of (15)-(17)
is a universal quantum no-go result.

## 8. Held-Out Readout And A Native Rank Certificate

The direct CSS construction can answer one held-out membership question
without learning a full logical locator map. For a value column b, set
`A=[E|b]` and `Delta=rank(A)-R in {0,1}`. Start with uniform coefficients
`(v,t) in F_2^(J+1)`, compute `Ev+t*b`, and postselect zero. Exactly

```text
Pr[zero syndrome]=2^(-(R+Delta)),
Pr[t=1 | zero syndrome]=1/2 if b in im(E), otherwise 0.
```

In the first case the t=0 and t=1 fibers each have size |ker(E)|;
in the second only the first exists. Observing t=1 certifies membership,
and q independent accepted copies give false-negative probability 2^-q
on a member. Thus full state tomography is not the missing operation.
But ordinary postselection costs 2^(R+Delta) trials on average; amplitude
amplification of THIS preparation costs order 2^((R+Delta)/2), multiplied
by the circuit cost for E and its inverse. An explicit CNOT implementation
uses nnz(E)+wt(b) XOR gates and J+N+1 qubits. Streaming the syndrome can
reduce workspace but does not remove the expanded J-bit coefficient state.
A short formal polynomial description does not supply this circuit for free.

Known local relations L subset ker(E) do not lower the syndrome rank:
the induced map on F_2^J/L has exactly the same image. Conversely, starting
only from |L>|+> makes the syndrome t*b, excluding every t=1 branch when
b is nonzero, even if b belongs to im(E). Accepting arbitrary syndromes
without correction leaves t fair in both membership cases; correcting
requires solving `A*c=syndrome`. None of these observations is a lower
bound on different preparations or other quantum algorithms.

The rank in this cost has a deterministic lower bound from ONE actual
public jet block. Suppose its point has weight w, multiplicity s, and
e=d-s+1, with w>=e and k-w>=s-1. Fix an e-subset W of its support. For
each (s-1)-subset S of the zero coordinates choose derivative column S
and row W union S. Formula (2) shows

```text
E[row(W union S), column(S')] = 1 if S=S', else 0,
rank(E) >= binom(k-w,s-1).
```

Indeed S' lies outside the support, so S' subset W union S is equivalent
to S' subset S, hence equality; the remaining W coordinates all equal 1.
This certificate needs no hidden key, dimension heuristic or matrix
expansion. For k=150,d=7,s=6,w=75 it already gives rank at least
17,259,390. This is a parameter illustration, not a claim that every
instance has such a public point. Weis's classical matrix-free methods
are polynomial in the expanded dimensions, not exponential in this rank;
the direct zero-syndrome route is therefore not a competitive default.

There is also an easy boundary case. If one training point has weight
exactly e, its nonzero columns are distinct coordinate vectors at rows
W union S, |S|=s-1, S outside W. A held-out VALUE column then belongs to
this block image exactly when its weight is below d (the zero column),
or its weight equals d and its support contains W. This has a direct
classical test, without kernel preparation. It is not the general
multi-block recovery problem or a falsification of Weis's assumptions.

Decision: deprioritize this direct CSS postselection method. Reopen it
only with a preparation/readout that avoids its charged syndrome cost,
preserves characteristic two, and beats the matched matrix-free baseline.
The compact quaternion source is the more concrete constructive next
receiver target, not a demonstrated speedup.

## 9. Bounded Regression Coverage

The companion test file is
`tests/test_holdout_jet_exterior_presentation.py`. It imports the existing
`theorems.holdout_jet_audit.analyze` producer and compares its returned full
packed columns with independent sparse square-zero multiplication. It also
checks Proposition 6 relations, even/odd divided-power identities using an
independent matching recurrence, a tiny instance of (6), and (13).

All fixtures are deterministic public bit vectors, not hidden-support
fixtures. They test identities, not the key-recovery dimension assumptions.

Explicit caps are checked before expansion:

| Operation | Cap |
| --- | --- |
| Sparse polynomial variables / terms | 13 / 2048 |
| Term pairs in one multiplication | 100,000 |
| Producer variables / monomial rows / training columns | 7 / 64 / 256 |
| Producer entries, including held-out target | 8192 |
| Pair generators in one fixture | 128 |
| Pfaffian variables / divided-power order | 8 / 4 |
| Perfect matchings per Pfaffian coefficient | at most 105 |

The quotient regression uses a 21-row producer and one 64-coordinate block,
with exact packed-bit elimination. Its quotient dimension is eight on that
fixture, not a general prediction. The `k=13,d=7` counterexample calls no
jet producer or rank routine and constructs no quotient matrix. The tests
also check rejection of over-budget requests before the producer is invoked.

The Section 8 controls additionally inspect native identity minors,
exhaustively count the augmented kernel on at most 15 nonzero-block
coefficient coordinates, check explicit local-quotient rank preservation,
and test every held-out value point in the bounded weight-e example.
They do not expand the illustrative k=150 operator or simulate a quantum
state. Its rank bound is evaluated from the combinatorial certificate.

Run without bytecode or pytest cache writes:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B -m pytest -q -p no:cacheprovider tests/test_holdout_jet_exterior_presentation.py
```
