**Status: the polynomial bound is not closed here, and no superpolynomial counterfamily is established.** The Taylor-coefficient mechanism is conditionally sound. The strongest deductions below identify its exact missing zero estimate and show that the multivariate native irreducibility promise does not remove the general-resultant case.

## 1. A size-preserving native lift exists

Let \(K=\mathbb Q(T)\), introduce one additional transcendental \(Z\), and set
\[
f(T,Z,Y)=p(T,Y)-Zq(T,Y),\qquad u=q(T,Z,y)=q(T,y).
\]

Then:

* \(f\) is monic of \(Y\)-degree \(\delta\), with sparse size polynomial in the original input.
* Since \(R\ne0\), \(\gcd_{K[Y]}(p,q)=1\).
* Any factorization of \(p-Zq\) in \(K[Y,Z]\), which has \(Z\)-degree one, would have a factor independent of \(Z\). That factor would divide both \(p\) and \(q\). Thus \(f\) is irreducible; monicity then gives irreducibility in \(K(Z)[Y]\).
* The original-basis atom \(u=q(y)\) is nonzero because \(\deg_Yq<\delta\).
* Exactly,
  \[
  N_{K(Z)[Y]/f\,/\,K(Z)}(u)
  =\operatorname{Res}_Y(p-Zq,q)
  =\operatorname{Res}_Y(p,q)=R(T).
  \]

Thus **every resultant in the question is already a norm on a promised native multivariate input**, with no denominator clearing or support explosion.

Consequently, any future general-resultant counterfamily automatically has a native lift for this norm-content operation. This does **not** establish hardness of fullRel. Nor does it establish a lift to an irreducible polynomial over a *univariate* base: substituting \(Z=T^w\) need not preserve irreducibility.

## 2. Exact local form of the unpaid statement

Write \(X=T-1\) and
\[
A=\mathbb C[[X]][Y]/p(1+X,Y).
\]
Monicity makes \(A\) free of rank \(\delta\). Multiplication by \(q\) has determinant \(R(1+X)\). Smith normal form over the DVR \(\mathbb C[[X]]\) gives
\[
\operatorname{ord}_{1}R
=\operatorname{length}_{\mathbb C[[X]]} A/qA
=\sum_{\substack{a\in\mathbb C\\p(1,a)=q(1,a)=0}}
 I_{(1,a)}(p,q).                                      \tag{1}
\]
Here
\[
I_{(1,a)}(p,q)=
\dim_{\mathbb C}
\frac{\mathbb C[[X,V]]}
     {(p(1+X,a+V),q(1+X,a+V))}.
\]
All these lengths are finite because \(R\ne0\). There are at most \(\delta\) contributing points. Monicity prevents an additional contribution from roots escaping to \(Y=\infty\).

Therefore the exact missing lemma is:

> **Mixed-degree sparse local zero estimate.** Bound these local intersection multiplicities polynomially in the numerical \(Y\)-degree and the original sparse bit size, while charging \(T\)-degrees only through their binary lengths.

A polynomial pointwise bound and the requested resultant bound are equivalent up to polynomial factors and the polynomial-size translation below.

### Coordinate-axis contributions are not being discarded

Write \(p=Y^a p_0\), \(q=Y^bq_0\), stripping maximal global powers of \(Y\). Nonzero resultant implies \(ab=0\).

If \(a>0\), then
\[
R=q(T,0)^a\operatorname{Res}_Y(p_0,q).
\]
If \(b>0\), then
\[
R=\bigl((-1)^\delta p(T,0)\bigr)^b
       \operatorname{Res}_Y(p,q_0).
\]
A nonzero \(t\)-term univariate polynomial has multiplicity at \(1\) at most \(t-1\), so these displayed factors contribute at most \(a(s-1)\) or \(b(s-1)\).

Stripping global powers does **not** remove every possible intersection at \((1,0)\). Those remaining intersections can be moved into the torus at polynomial cost: choose
\[
c\in\{1,\ldots,\delta+1\},\qquad p(1,c)\ne0,
\]
and replace \(Y\) by \(V+c\). Such a \(c\) exists and can be found by exact polynomial-bit evaluation. The resultant is unchanged; every point above \(T=1\) now has \(V\ne0\). The term count grows by at most \(\delta+1\), and coefficient bits increase by \(O(\delta\log(\delta+1))\).

Hence the axis issue is controllable, but **the torus mixed-degree estimate remains unpaid**. The supplied \(52d^2t^2\) theorem uses *total* degree \(d\), potentially \(2^{\Theta(E)}\), not numerical \(Y\)-degree. The supplied trinomial theorem does not cover the resulting general inputs.

## 3. What elementary support and Wronskian arguments actually establish

Let \(s_p,s_q\) be the two term counts, and \(m=\deg_Yq\). Multihomogeneity of the resultant gives the support bound
\[
\#\operatorname{supp}R\le
K:=
\binom{s_p+m-1}{m}
\binom{s_q+\delta-1}{\delta}.
\]
Indeed, each determinant term selects \(m\) input terms from \(p\) and \(\delta\) from \(q\).

For \(H(T)=\sum_{j=1}^{r}c_jT^{e_j}\), applying
\(D=T\,d/dT\) at \(1\) gives the Vandermonde system
\[
D^kH(1)=\sum_jc_je_j^k,\qquad 0\le k<r.
\]
Thus a nonzero \(H\) has order at most \(r-1\), proving
\[
\operatorname{ord}_{1}R\le K-1.                       \tag{2}
\]
This is a rigorous upper bound, but it is **not an admissible polynomial truncation schedule when \(\delta\) grows**.

The precise Wronskian bottleneck can also be stated. On a regular torus branch \(Y=\phi(T)\), choose \(r\) independent functions among the monomials occurring in \(q(T,\phi(T))\), and let \(W\) be their Wronskian. Replacing one basis function by their nonzero linear combination gives
\[
\operatorname{ord}_{1}q(T,\phi(T))
\le r-1+\operatorname{ord}_{1}W.
\]
Factoring out monomial units and clearing powers of \(p_Y\) leaves a numerator built from derivatives of \(p\). **Its polynomial \(Y\)-degree alone does not bound its order along the branch.** Bounding its numerical \(T\)-degree or expanded support reintroduces the forbidden exponential clock. Singular branches additionally require controlling the denominator/ramification contributions.

That residual zero estimate—not the formal Wronskian construction—is the unpaid step. Nothing here proves that a better Wronskian argument is impossible.

## 4. Conditional arithmetic costs are payable

Suppose a proved polynomial bound \(M\) were available. Put \(n=\delta+m\), let \(N\) bound the input \(T\)-exponents, and take \(D=\max(1,nN)\). A conservative coefficient-norm bound is
\[
\|R\|_1\le H:=n!\,(s2^B)^n.
\]
If \(a_j=[X^j]R(1+X)\), then
\[
|a_j|\le H D^j,
\]
so for \(j\le M\),
\[
\log_2\max(1,|a_j|)
=O\!\left(n(B+\log s+\log n)+M(E+\log n)\right).
\]

Compute each \((1+X)^e\bmod X^{M+1}\) by binary powering or binomial recurrence, then compute the truncated Sylvester determinant. No pivot inversion in a truncated ring is necessary: traces of matrix powers and Newton identities, with divisions only by \(1,\ldots,n\), suffice. Input access, intermediate precision and output length are polynomial under the hypothesized bound.

The first nonzero \(a_j\) satisfies
\[
\operatorname{content}(R)\mid a_j.
\]
Factoring \(a_j\) is a **separate charged task**, not a known classical polynomial-time consequence of this extraction.

### Multivariate nonvanishing can be paid deterministically

If every coordinate degree of the actual multivariate norm is at most \(D_0\), use
\[
T_i=U^{(D_0+1)^{i-1}}.
\]
This is injective on all exponent vectors in \([0,D_0]^r\), preserving both nonzeroness and content. Weight and substituted-exponent bit lengths are polynomial in \(r\) and \(\log(D_0+1)\). No probabilistic nonvanishing assertion is needed. Irreducibility after this substitution is not asserted.

### Denominator scope guard

Formal circuit clearing and truncated evaluation are polynomial-size operations. But that fact alone does **not** extend a multiplicity theorem parameterized by the *expanded* term count of integral \(p,q\) to the original rational presentation. For example,
\[
\prod_{j<r}(1+T^{2^j})
\]
has a small factored presentation and \(2^r\) expanded terms. The native application therefore needs either the zero estimate for the original rational/factored presentation or a size-preserving reduction to the explicitly sparse integral case.

## Disposition

The route is **unpaid, not refuted**. The missing all-input theorem is the mixed-degree local zero estimate in (1), with its rational-presentation scope justified. A valid falsifier would be an explicit family of polynomial sparse bit size with superpolynomial \(\operatorname{ord}_{1}R\); the lift in §1 would then supply genuine native multivariate norm instances automatically.

No supplied theorem, finite control, or argument above closes that estimate or implies hardness, a speedup, or a fullRel algorithm.