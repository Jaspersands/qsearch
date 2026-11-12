# Report: an exact ideal-class bypass, but not yet a polynomial BIT ONE-HALF

**Verdict.** There is a genuine algebraic bypass of Stoll’s minimum-degree and monic-output steps: a three-generator ideal constructed from **any nonzero bounded Stoll solution** represents an actual half. Polynomial common factors become principal ideal factors, so they are harmless.

This does **not** yet establish the requested native polynomial BIT clock. In particular, the obvious coefficientwise presentation of this ideal is not automatically a stable finite-precision representation—even on valid Stoll inputs. A paid fixed-degree/flat reset, kernel-selection procedure, and label interface remain necessary.

All deductions below use the supplied excerpts and symbolic arguments; no controls were executed.

## 1. Cheapest check: a nonminimal \(w\) need not represent any divisor

Take the native genus-two input
\[
f=x^5+x+1,\qquad
a=x^3-\tfrac14,\qquad
b=-1-\tfrac x2,\qquad
s=x^4+\tfrac12 .
\]
Here \(a\) is monic and squarefree, \(\gcd(a,f)=1\), and
\[
f-b^2=ax^2,\qquad xs\equiv b\pmod f,\qquad s^2\equiv-a\pmod f.
\]
The point \(h=[a,b]\) is the nonzero point
\[
h=2[(0,1)-\infty].
\]

The bounded triple \(t_0=(1,b,x)\) is valid. So is
\[
t=(x-1)t_0,
\qquad w=x(x-1).
\]
But no Mumford pair \([w,r]\) over \(\mathbf Q_2\) exists: at \(x=1\) it would require
\[
r(1)^2=f(1)=3,
\]
which is impossible in \(\mathbf Q_2\).

Thus even a valid bounded kernel vector on a small native input cannot simply be read as a high-degree half divisor through its \(w\)-component. This refutes that particular shortcut, not selection of better representatives.

## 2. A proved algebraic bypass using ideals

Retain all hypotheses of Stoll Proposition 5.1. Put
\[
k=\mathbf Q_2,\quad
R=k[x,y]/(y^2-f),\quad
n=\deg a,\quad
\epsilon=(-1)^n,
\]
and retain \(d=\gcd(a,f)\), \(f=df_1\), \(a=da_1\).

Let \((u,v,w)\) be **any nonzero bounded solution** of Stoll’s congruences. No minimum-degree condition or normalization of \(w\) is imposed. Stoll gives \(w\ne0\) and
\[
u^2f_1=dv^2-\epsilon a_1w^2.
\]
Define
\[
\Phi=uy-vd
\]
and the integral ideal
\[
\boxed{\quad
K=(aw,\;w(y-b),\;\Phi)\subset R.
\quad}                                                     \tag{1}
\]

### Proposition

The ideal class of \(K\), interpreted in \(J(k)\) using the rational point \(\infty\), represents a point \(q\) satisfying
\[
2q=[a,b].
\]

### Proof

Because \(f\) is squarefree and \(\operatorname{char}k=0\), the affine curve is smooth and \(R\) is a Dedekind domain. Every nonzero fractional ideal therefore defines a divisor class.

For a fractional ideal \(I\), write
\[
c(I)=[D_I-\deg(D_I)\infty]\in J(k),
\]
where \(D_I\) is its affine valuation divisor. Then
\[
c(IJ)=c(I)+c(J),\qquad c((r))=0.
\]
The hyperelliptic involution, denoted by a bar, satisfies
\[
c(\overline I)=-c(I).
\]

Let
\[
A=(a,y-b).
\]
Its divisor is the supplied effective divisor defining \([a,b]\), so
\[
c(A)=[a,b],\qquad A\overline A=(a).
\]
The latter identity includes ramification points with their correct multiplicities.

Now set, for the proof only,
\[
\beta=\frac{\Phi}{w}.
\]
The norm identity is
\[
\beta\overline\beta
=\frac{d^2v^2-fu^2}{w^2}
=\epsilon a.
\]
For the fractional ideal \(I=A+(\beta)\), this gives
\[
(\beta)\overline I
=(\beta)\overline A+(a)
=\overline A\,I.
\]
Taking divisor classes,
\[
-c(I)=-[a,b]+c(I),
\]
hence \(2c(I)=[a,b]\).

Finally, \(K=wI\), so \(c(K)=c(I)\). ∎

### Why common factors are handled correctly

For any nonzero polynomial multiplier \(m\),
\[
K(mu,mv,mw)=mK(u,v,w).
\]
Multiplication by \(m\) changes the ideal only by a principal factor. Consequently its Jacobian class is unchanged.

This is substantially different from declaring \(mw\) to be a Mumford polynomial: the latter attempts to choose one sheet over the extra roots of \(m\), while the ideal construction retains the principal contribution correctly.

The construction also does not need the post-kernel gcd \(\gcd(u,w)\). It may return a different half from Stoll’s minimum-degree construction, but the difference is rational \(2\)-torsion, which is permitted by ONE-HALF.

**Important:** its Kummer label must be the label of \(c(K)\). Neither \(\widetilde\mu(w)\) for a nonminimal vector nor the minimum-degree corollary can be substituted without further justification.

### Compatibility with the original error subgroup

If the construction is applied to
\[
h_z=h+2\sigma(z),
\]
then its exact output satisfies
\[
2q-h=2\sigma(z)\in E.
\]
No subtraction of \(\sigma(z)\), and no replacement of the original \(E\), is required.

## 3. Polynomial algebraic size is proved; a maintained finite chart is not

After replacing \(b\) by its remainder modulo \(a\), all generators in (1) have degree \(O(g)\). This replacement does not change the ideal.

As a \(k[x]\)-module, \(K\) can be stored using its three generators and their products by \(y\), in the basis \(1,y\). Thus a constant-size polynomial matrix with \(O(g)\) coefficients suffices. No support-field compositum is involved.

Moreover,
\[
(aw)\subseteq K,
\]
so
\[
\dim_k(R/K)\le \dim_k R/(aw)
=2\deg(aw)\le 6g+2.
\]
Therefore \(K\) defines an effective affine divisor \(D_K\) of uniformly bounded degree.

Mathematically, one can pad \(D_K\) with copies of \(\infty\) to fixed degree \(d_*=6g+2\), and then use
\[
H^0\!\left(\mathcal O((d_*+2g)\infty)
          -D_K-(d_*-\deg D_K)\infty\right)
\]
as nonspecial RR data of dimensions \(O(g)\).

These are **existence and algebraic-size bounds**. Computing the degree, a suitable subspace basis, a fixed-degree reset, and later group operations at bounded precision is not supplied by this argument. Keeping an unevaluated ideal-expression DAG merely postpones those costs.

Also, this construction does not remove the costs of obtaining the actual \(a,b,s,d\), or of constructing and solving the Stoll system.

## 4. A native obstruction to treating the raw generators as a finite chart

There is a stronger warning than an arbitrary perturbed matrix: the ideal-defined half can be discontinuous in the raw generator coefficients **along valid Stoll inputs**.

Take
\[
f=x^3-x,\qquad
a_0=f-1,\qquad b_0=1,\qquad s_0=2x^2-1.
\]
The valid bounded triple is
\[
(u_0,v_0,w_0)=(x,x,x).
\]
Its minimum-degree Stoll half is \(T=(0,0)-\infty\). But (1) gives
\[
K_0=(a_0x,\;x(y-1),\;x(y-1))
   =(x(y-1)),
\]
which is principal. The ideal construction therefore returns \(q_0=0\).

Now choose a small nonzero dyadic number \(\eta\), for example \(2^M\), and let \(\alpha\) be the unique root near zero of
\[
\alpha^3-\alpha=\eta^2.
\]
This is a finite Hensel specification, not exact-real advice. Put
\[
e=3\alpha^2-1,\qquad
A=-\frac{2\eta(1+\eta)}{e},
\]
and
\[
w=x-\alpha,\qquad u=w+A,\qquad v=w-A\eta.
\]
The polynomial \(fu^2-v^2\) has a double zero at \(\alpha\): its value vanishes, and its derivative there is
\[
A\bigl(eA+2\eta(1+\eta)\bigr)=0.
\]
Thus
\[
a_\eta=\frac{fu^2-v^2}{w^2}
\]
is a monic cubic. Define
\[
b_\eta\equiv v/u\pmod {a_\eta},\qquad
s_\eta\equiv v/w\pmod f.
\]
For sufficiently small nonzero \(\eta\), all these operations are defined, \(a_\eta\) is squarefree and coprime to \(f\), and these are valid Stoll data.

They converge coefficientwise to the displayed data at \(\eta=0\). In particular, \(s_\eta\) tends to the polynomial taking values \(-1,1,1\) at \(0,1,-1\), namely \(s_0\).

For \(\eta\ne0\), \(u(\alpha)=A\ne0\), and the Stoll half is
\[
P_\eta=(\alpha,\eta)-\infty.
\]
The ideal in (1) has divisor
\[
D_{a_\eta}+\iota(P_\eta),
\]
and hence represents \(P_\eta\). Therefore
\[
c(K_\eta)\longrightarrow T,
\qquad\text{whereas}\qquad c(K_0)=0.
\]
The affine ideal-divisor degree jumps from \(4\) to \(5\) at the limit.

This affects the requested observable: \(T\) has nontrivial Kummer label, represented at the roots \(0,1,-1\) by
\[
(-1,-1,1).
\]
For sufficiently small \(\eta\), \(P_\eta\) has that same label, while \(c(K_0)\) has trivial label.

### What this does—and does not—refute

It refutes the claim that raw coefficient approximations to (1), without additional structural or flatness data, automatically specify the returned half and its label at finite precision.

It does **not** refute ONE-HALF. One could choose \(P_\eta-T\) instead, or use a suitable flat RR representation. Nor is this an assertion that these points are nonzero saturation triggers or that all representatives in a required coset are bad. It is a native obstruction to this particular unqualified finite-chart interpretation.

## 5. The remaining BIT theorem that would actually close the operation

The ideal construction removes minimum-degree reduction as an **algebraic correctness requirement**. The following costs still need a uniform theorem.

### A. Obtain a usable bounded kernel vector

A paid bound on the nonzero Smith valuations of the **full** homogeneous Stoll matrix would suffice to use the supplied finite-kernel lifting lemma: choose a primitive finite-ring kernel vector and certify an actual nonzero bounded lift.

That would avoid a minimum-\(j\) search and the specific \(w\)-leading-coefficient normalization bound. But:

- the full-matrix bound is not supplied;
- clearing matrix denominators must be charged;
- ordinary exact-field elimination may still determine \(j\) implicitly through rank;
- a branch-free approximate alternative would need its own actual-point certificate.

The formulas (1) genuinely contain no division by a tiny leading coefficient. That does not bound the conditioning of converting their generators into a usable Jacobian representation.

### B. Supply a stable, fixed-degree ideal/RR reset

One needs a constructive interface which handles phenomena such as §4 and returns an actual chosen point, not merely an unspecified torsor of halves.

It must support, at paid precision:

- addition and the binary-exponent combinations used to form later \(h\);
- fixed-degree moving/reset operations;
- subsequent halving input construction;
- Kummer-label evaluation;
- a certificate that every permitted replacement error lies in the **original** \(E\).

Nonspeciality over \(\mathbf Q_2\) fixes dimensions. By itself it does not bound integral Smith valuations or certify a finite approximation.

### C. Bound the entire loop, not one successful call

Let \(T\) count all arithmetic operations in the polynomially bounded saturation loop, including the operations used to assemble inputs.

A sufficient schedule would provide either:

- a uniform numerical reset cap
  \[
  S\le P(g,B,D,\text{seed parameters}),
  \qquad D=v_2(\operatorname{disc}f),
  \]
  throughout the computation; or
- an additive total precision-loss bound
  \[
  \sum_{\nu=1}^{T}\Delta_\nu\le
  \operatorname{poly}(g,B,D,\text{seed parameters}).
  \]

A recurrence merely saying \(S_{\nu+1}\le\operatorname{poly}(S_\nu,\ldots)\) is insufficient.

If selection uses \(h+2\sigma(z)\), its theorem must also supply a quantitative success probability and the required low-jet/tail bounds. Polynomially many finite-grid draws are admissible; enumeration of the grid is not.

### D. Charge access, roots, labels, and output

The ledger must include:

- reading \(f\) and refining every stored coefficient to the required precision;
- constructing high-degree squarefree input data and the square root \(s\);
- native local-factor and squareclass-coordinate setup;
- every ideal/RR linear-algebra operation;
- serialization of the returned point representation and its finite label.

An \(O(g)\)-coefficient ideal or \(O(g^2)\)-entry RR subspace is polynomial-size only when its numerical precision, pole bounds, and refinement costs are polynomially bounded.

## Disposition

| Claim | Status |
|---|---|
| Any bounded Stoll solution yields an actual half through (1) | **Proved** |
| Polynomial common factors can be retained without extracting a minimum-degree vector | **Proved algebraically** |
| One output has polynomial algebraic size | **Proved** |
| A nonminimal \(w\) can simply be treated as the half divisor | **Refuted** |
| Raw projective ideal generators automatically give a stable finite half/label certificate | **Refuted without further data** |
| Uniform native reset, selection, precision, and label bounds over the whole loop | **Open** |
| An all-representative native obstruction to polynomial ONE-HALF | **Not established** |

The useful constructive result is therefore an **ideal-class replacement for minimal Mumford extraction**, not a completed local routine. Closing the remaining interface would be classical and would remove the stated local blocker; nothing here establishes the full Selmer composition, a quantum separation, or hardness.