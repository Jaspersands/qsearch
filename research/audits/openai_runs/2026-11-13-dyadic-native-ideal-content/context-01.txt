## Verdict

**A nonspecial, high-degree compiler exists over \(\mathbf Q_2\), with fixed, known ranks and without splitting the support.** It can produce a source-compatible Stoll input of degree exactly \(2g+1\). Below is an explicit construction, including a finite successful-run certificate.

**This does not yet establish a uniform polynomial BIT clock.** Minimum-valuation pivoting gives integral coordinates for the relevant subspaces, but does not, by itself, bound the precision needed to find those coordinates. The remaining obligation is a **native determinantal-content and reset bound**, including the subsequent halving matrices—not an existence theorem for general-position divisors.

No supplied result gives that bound. Conversely, I find no native counterfamily defeating *all selectable representatives* in the permitted coset.

I use only the supplied material; no computations or source checks were performed.

---

## 1. Cheapest native conditioning test

A small example already rejects a naive inference from support poles to interpolation conditioning.

Take
\[
g=1,\qquad f=x^3+x+1,\qquad v_2(\operatorname{disc}f)=0.
\]
For \(M\ge3\), put
\[
t=2^M,\qquad
P_0=(0,1),\qquad P_M=(t,\eta_M),
\]
where
\[
\eta_M^2=1+t+t^3,\qquad \eta_M\equiv1\pmod4.
\]
Then
\[
v_2(\eta_M-1)=M-1.
\]

The actual point
\[
h_M=[P_0+P_M-2\infty]
\]
is divisible by \(2\). Indeed, in \(L=\mathbf Q_2[\theta]/(f)\),
\[
a(\theta)=\theta(\theta-t)
=\theta^2(1-t/\theta)
\]
is a square: \(\theta\) is an integral unit and \(1-t/\theta\in1+8\mathcal O_L\).

For the degree-three RR compiler, the ambient space is \(L(5\infty)\), with basis
\[
1,x,y,x^2,xy.
\]
Direct evaluation at \(\iota P_0,\iota P_M\) gives
\[
\begin{pmatrix}
1&0&-1&0&0\\
1&t&-\eta_M&t^2&-t\eta_M
\end{pmatrix}.
\]
Its rank is two, but the minimum valuation of a nonzero maximal minor is exactly \(M-1\). All support coordinates are integral; \(g,B\), and \(v_2\operatorname{disc}f\) are fixed.

Thus:

> Bounded support poles, known rank, and selection of a minimum-valuation maximal minor do not alone bound raw evaluation losses.

This is **not** a counterexample to the proposed high-degree strategy. In fact,
\[
\frac{\eta_M-1}{t}
=\frac{1+t^2}{\eta_M+1},
\]
and the denominator on the right has valuation only \(1\). A confluent or ideal-based construction can avoid the large loss. Nor does this example establish reachability in the prescribed saturation loop. Its role is only to falsify the raw pole-to-minor inference.

The compiler below avoids direct-sum evaluation at possibly colliding points.

---

## 2. Representation invariant

Write \(K=\mathbf Q_2\), \(d=2g+1\), and
\[
R_C=K[x,y]/(y^2-f).
\]

Use graph-divisor blocks
\[
D_i=(a_i,b_i),\qquad
a_i\text{ monic},\quad
\deg b_i<e_i:=\deg a_i,\quad
a_i\mid f-b_i^2.
\]
Neither \(a_i\) nor the sum of the blocks needs to be squarefree. A block is stored without factoring \(a_i\).

Negation replaces \(b_i\) by \(-b_i\), because
\[
-[D_i-e_i\infty]=[\iota D_i-e_i\infty].
\]
Consequently, a signed input becomes
\[
h_z=[D-m\infty],\qquad D=\sum_iD_i,\qquad m=\sum_i e_i.
\]

The relevant size is **total closed-divisor degree \(m\)**, not merely the number of written summands. In the proposed invariant, \(m=O(g)\):

* store each maintained point using a degree-\(d\) representative;
* compress after each binary group addition;
* append \(2\sigma(z)\) using its \(4g\) point occurrences;
* after halving, reset the degree-\(\le g\) output to degree \(d\).

Large presentation exponents must be processed by binary additions with intervening compression, not expanded into divisor multiplicities.

To specify actual points rather than exact \(2\)-adic advice, store:

1. finite approximations;
2. a shared arithmetic DAG starting from the native coefficients and seeds;
3. root selections certified by finite Hensel data;
4. nonzero-denominator certificates for subsequent arithmetic.

This is a specification of actual points, **not a free evaluation oracle**. Its evaluation precision and total size remain part of the BIT ledger.

---

## 3. Collision-safe, fixed-rank RR matrices

### 3.1 The desired RR space

Set
\[
A=\prod_i a_i,\qquad N=m+d.
\]
Then
\[
\operatorname{div}(A)=D+\iota D-2m\infty.
\]
A section of
\[
\mathcal O_C\bigl(D+(d-m)\infty\bigr)
\]
can therefore be written \(F/A\), where
\[
F\in L(N\infty-\iota D).
\]

The ambient basis is explicit:
\[
\mathcal B_N=
\{x^j:2j\le N\}
\;\cup\;
\{x^jy:2j+d\le N\}.
\]
It has \(m+g+2\) elements. Since \(N-m=d=2g+1\),
\[
\dim L(N\infty-\iota D)=g+2
\]
for **every** input divisor \(D\), including collision and multiplicity cases.

### 3.2 A finite algebra that does not split the support

Work in
\[
T=R_C/(A),
\]
of dimension \(2m\), with basis
\[
1,x,\ldots,x^{m-1},\quad
y,xy,\ldots,x^{m-1}y.
\]

Let \(X\) be multiplication by \(x\) on \(K[x]/A\). Multiplication by \(y\) on \(T\) is
\[
Y=
\begin{pmatrix}
0&f(X)\\
I&0
\end{pmatrix}.
\]

The ideal of \(\iota D_i\) is
\[
J_i=(a_i,y+b_i).
\]
Its two multiplication matrices on \(T\) are
\[
G_i=
\begin{pmatrix}
a_i(X)&0\\
0&a_i(X)
\end{pmatrix},
\qquad
H_i=
\begin{pmatrix}
b_i(X)&f(X)\\
I&b_i(X)
\end{pmatrix}.
\]

Start with \(V_0=I_{2m}\). Given a column basis \(V_{i-1}\), form
\[
C_i=[\,G_iV_{i-1}\mid H_iV_{i-1}\,].
\]
Its column space is the image of \(J_1\cdots J_i\) in \(T\).

Crucially, its rank is known in advance:
\[
r_i=2m-\sum_{j\le i}e_j.
\]
This follows from additivity of effective-divisor lengths on the smooth characteristic-zero curve. It remains valid when blocks coincide or contain conjugate pairs.

Thus the construction does not need to decide whether support points are equal, or to enumerate support fields.

### 3.3 Fraction-free basis selection

For a known-rank matrix \(C\), choose row and column sets \(I,J\) with
\[
\Delta=\det C_{I,J}\ne0.
\]
A normalized column basis is
\[
V=C_J(C_{I,J})^{-1}
  =\frac{C_J\operatorname{adj}(C_{I,J})}{\Delta}.
\]
This is the requested fraction-free numerator/denominator description.

If \(\Delta\) has minimum valuation among nonzero maximal minors, every entry of \(V\) is integral: its entries are ratios of maximal minors, and \(V_I=I\). It is a basis of the saturated lattice in the same \(K\)-subspace.

There is no need to enumerate maximal minors. Once adequate precision is available, valuation-pivoted DVR elimination can find such a chart. **Adequate precision is the unresolved qualification.**

At the final stage, \(V\) has \(m\) columns. If its pivot rows are \(I\), membership in its column space is expressed by
\[
v_{I^c}-V_{I^c}v_I=0.
\]
Let \(\Lambda_D\) denote this \(m\)-row matrix.

### 3.4 The RR interpolation matrix

Let \(E_N\) send a coefficient vector in the basis \(\mathcal B_N\) to its remainder in \(T\). Form
\[
M_D=\Lambda_D E_N.
\]
Then
\[
\ker M_D=L(N\infty-\iota D),\qquad
\operatorname{rank}M_D=m.
\]

The rank is fixed by RR, not guessed numerically. If \(J\) is a pivot-column set and
\[
\Delta_D=\det(M_D)_J\ne0,
\]
then for each nonpivot column \(\ell\), a fraction-free kernel vector is
\[
k_\ell=
\Delta_D e_\ell-
\sum_{j\in J}
\bigl(\operatorname{adj}((M_D)_J)(M_D)_\ell\bigr)_j e_j.
\]
Dividing these vectors by \(\Delta_D\) gives a kernel basis with identity free coordinates. Minimum-valuation pivoting again makes this basis integral.

This completes an explicit, collision-safe field-operation compiler using \(O(g)\)-dimensional matrices when \(m=O(g)\).

---

## 4. Random section and divisor extraction

Choose integer coefficients \(c_1,\ldots,c_{g+2}\), and form
\[
F=p(x)+q(x)y\in\ker M_D.
\]

Let \(\alpha\) be the coefficient of the unique basis monomial of pole order \(N\). Require \(\alpha\ne0\), so \(F\) has exact pole order \(N\). Set
\[
H=p^2-fq^2,\qquad R=H/A.
\]
The division is exact. Moreover,
\[
\deg R=d,\qquad
\operatorname{lc}(R)=
\begin{cases}
\alpha^2,&N\text{ even},\\
-\alpha^2,&N\text{ odd}.
\end{cases}
\]

Accept the section when
\[
\operatorname{disc}(R)\ne0,\qquad
\operatorname{Res}(R,Af)\ne0,\qquad
\operatorname{Res}(R,q)\ne0.
\]
Define
\[
a=R/\operatorname{lc}(R),\qquad
b=-p\,q^{-1}\pmod a.
\]

Then:

* \(a\) is monic, squarefree, and has degree \(d=2g+1\);
* \(\gcd(a,f)=1\);
* \(a\mid f-b^2\);
* \([a,b]=h_z\).

The last assertion has the explicit divisor certificate
\[
D'=\operatorname{div}(F)+N\infty-\iota D,
\]
and
\[
D'-d\infty
=\operatorname{div}(F/A)+D-m\infty.
\]

All extraction can remain unsplit. For example, \(q^{-1}\bmod a\) is obtained by inverting the multiplication matrix \(q(X_a)\); its determinant is \(\operatorname{Res}(a,q)\).

### Why acceptable sections exist

The line bundle has degree \(2g+1\), hence is very ample. A general section has reduced zero divisor, avoids any prescribed finite set, and contains no hyperelliptic conjugate pair. For the last condition, vanishing at \(P+\iota P\) imposes two independent conditions; allowing \(P\) to vary still leaves a proper bad locus.

After clearing fixed denominators, the displayed rejection tests form a nonzero polynomial in the \(c_i\), of degree \(O(g+m)\).

That proves exact generic existence—not a finite-precision clock.

### What random finite-grid sampling would need

There is a useful elementary conditional bound. If an integral polynomial \(P\) in \(r\) variables has coefficient content
\[
\gamma=\min_\nu v_2(P_\nu),
\]
and degree at most \(e_i\) in variable \(i\), then
\[
\mathbb E_{c\in\mathbf Z_2^r}v_2(P(c))
\le \gamma+\sum_i e_i.
\]
One proves this first in one variable using its roots for analysis only, then inducts on the variables.

Consequently, if \(\gamma\) has a polynomial numerical cap, sampling each coefficient from
\[
\{0,\ldots,2^m-1\},\qquad
m\ge 2\bigl(\gamma+\sum_i e_i+1\bigr),
\]
gives a bounded-valuation acceptance probability at least \(1/2\). Polynomially many **draws**, not grid enumeration, then suffice.

For this application, each test polynomial must first be individually cleared to an integral polynomial. Otherwise signed resultant valuations could cancel and fail to bound individual losses.

**The required uniform content bound is not supplied.**

---

## 5. A source-compatible halving input and acceptance certificate

The compiler’s accepted output satisfies the hypotheses of Stoll Proposition 5.1 with
\[
\deg a=2g+1,\qquad \gcd(a,f)=1,\qquad c=1.
\]
Find one
\[
s\in K[x]/f,\qquad s^2\equiv-a\pmod f.
\]
This is one square-root choice, not enumeration of all choices.

A particularly clean successful chart avoids every unknown-rank branch in the Stoll step. Use unknowns
\[
\deg u\le g,\qquad
\deg v\le2g,\qquad
\deg w\le g,
\]
and the congruences
\[
v\equiv ws\pmod f,\qquad
v\equiv ub\pmod a.
\]
Their matrix \(M_{\rm half}\) has \(4g+2\) rows and \(4g+3\) columns. Append the row selecting the coefficient \(w_g\):
\[
\mathcal B=
\begin{pmatrix}
M_{\rm half}\\
[w_g]
\end{pmatrix}.
\]

Require
\[
\det\mathcal B\ne0.
\]
Then define the exact solution by
\[
(u,v,w)=\mathcal B^{-1}(0,\ldots,0,1)^t.
\]
It has \(w\) monic of degree \(g\), and no bounded solution can have smaller \(w\)-degree: such a solution would lie in \(\ker\mathcal B\).

Next require
\[
\operatorname{Res}(w,u)\ne0,
\qquad
r=-vu^{-1}\pmod w.
\]
The supplied proposition gives
\[
Q=[w,r],\qquad 2Q=[a,b]=h+2\sigma(z).
\]
Hence the original-error-subgroup certificate is exactly
\[
\boxed{\,2Q-h=2\sigma(z)\in E\,}.
\]
No replacement of \(E\), and no numerical E-membership oracle, is involved.

This accepting chart is intentionally restrictive. If its determinant or resultant is not visible within the budget, the attempt is rejected; it must not be declared an exact rank drop. Bounded success probability after permitted perturbation remains to be proved.

### Finite realization of the square root

A root declaration must be more than “choose an exact \(s\).” One possible certificate uses the order
\[
\mathcal O=\mathbf Z_2[\theta].
\]
After a paid scaling \(s=2^{-T_s}t\), certify an integral approximate solution of
\[
t^2=-2^{2T_s}a(\theta)
\]
with residual precision exceeding twice the determinant valuation of multiplication by \(2t\). The multivariate Hensel criterion then names an actual root in a specified ball.

Finding this initial certificate, including any local factorization and square-root computations, must be charged. Independent component roots do not require a compositum or a \(4^g\) sign search.

---

## 6. Precision ledger

The construction removes several unknown-rank decisions. It does **not** remove denominator losses.

Suppose the coefficients of \(a_i,b_i\) have valuation at least \(-S_i\), and put
\[
T_A=\sum_i S_i.
\]
Then coefficients of \(A\) have valuation at least \(-T_A\). Explicit conservative entry bounds include
\[
v_2(X)\ge-T_A,\qquad
v_2(f(X))\ge-dT_A,
\]
\[
v_2(a_i(X))\ge-S_i-e_iT_A,\qquad
v_2(b_i(X))\ge-S_i-(e_i-1)T_A.
\]
Once \(V_{i-1}\) is normalized integral, these give polynomial numerical denominator-clearing bounds for \(C_i\). Likewise,
\[
v_2(E_N)\ge-\lfloor N/2\rfloor T_A.
\]

The separate requirements are:

| Operation | Required certificate and charged loss |
|---|---|
| Product-ideal basis \(C_i\) | A visible nonzero \(r_i\)-minor; prescribed rank \(r_i\). Charge denominator clearing and its determinantal valuation. |
| RR kernel \(M_D\) | A visible nonzero \(m\)-minor; prescribed rank \(m\). Charge its valuation before constructing a saturated kernel basis. |
| Section at infinity | \(\alpha\ne0\), with a bounded visible valuation. Basepoint freeness proves nonvanishing is possible, not its numerical size. |
| Norm division \(H/A\) | Monic division; no uncertain leading-coefficient inverse, but nonintegral coefficients of \(A\) amplify errors. A conservative coefficient pole bound is \((d+1)T_A\). |
| Monic normalization of \(R\) | Divide by \(\pm\alpha^2\). Both numerator and denominator uncertainty must be propagated; the denominator valuation cannot be charged only once without an integrality argument. |
| General-position tests | Visibility of individually scaled discriminants/resultants. |
| \(q^{-1}\bmod a\) | Invertible multiplication matrix \(q(X_a)\), including its entry-construction and inverse losses. |
| Square root in \(L\) | A certified root ball and a bound for the inverse derivative \(2s\), in a paid basis/order. |
| Stoll solution | A bound for the **augmented** matrix \(\mathcal B\), not merely \(M_{\rm half}\). |
| \(u^{-1}\bmod w\) | A visible nonzero determinant and paid inverse/remainder arithmetic. |
| Output reset | A further high-degree compiler call, with its own losses and actual-point certificate. |

For an integral matrix of known rank, let
\[
\tau=\min_{\Delta\ne0}v_2(\Delta)
\]
over maximal minors. Its largest nonzero Smith valuation is at most \(\tau\). Precision greater than \(\tau\) is needed even to expose the prescribed rank by such a witness.

A conservative absolute-precision allowance for uncertain inverse operations is \(P_{\rm out}+2\tau\), after entry-construction losses. Ratios known to be integral can admit sharper bounds, but this does not bound \(\tau\).

The fundamental scalar propagation rule is
\[
P_{x/y}\ge
\min\{P_x-v_2(y),\ P_y+v_2(x)-2v_2(y)\}.
\]
It prevents silently discarding the normalization loss identified in the supplied precision note.

---

## 7. The concrete missing theorem

Minimum-minor normalization establishes
\[
\text{integral coordinates for the selected subspace}.
\]
It does **not** establish
\[
\text{polynomial precision needed to discover those coordinates}.
\]
It can divide out an arbitrarily large common power of \(2\).

For this compiler, the missing quantities are now concrete:

1. the determinantal contents of the prescribed-rank product matrices \(C_i\);
2. the determinantal content of \(M_D\);
3. the content of the section acceptance polynomial, including the infinity coefficient;
4. the conditioning of \(\mathcal B\), root extraction, and output inverses after the permitted perturbation;
5. the conditioning of the output reset.

A sufficient native theorem would provide
\[
C=\operatorname{poly}(g,B,v_2\operatorname{disc}f,\text{seed parameters})
\]
such that, for every maintained native state and requested \(h\),

* bounded finite grids for \(z\) and section coefficients can be sampled in polynomial time;
* a polynomially bounded number of draws reaches certificates whose **individual** losses are at most \(C\);
* the output is reset to a polynomial-size representation with the same cap.

Alternatively, a proved additive bound on total loss along the complete computation DAG would suffice.

A recurrence such as
\[
S_{\rm new}\le \operatorname{poly}(S_{\rm old},g,B)
\]
does not suffice: it can grow exponentially over the already-polynomial saturation loop.

For the section coefficients, the bad conditions are polynomial and the conditional sampling bound above is available. For \(z\), dependence passes through the native analytic perturbation, selected kernel charts, and root choices. **Low-jet content and tail bounds, or a replacement argument, are still required.** Genericity on an open subgroup proves neither the numerical cap nor findable success probability.

---

## 8. Status and falsifiers

### Proved deductions here

* A collision-safe, unsplit RR compiler with prescribed ranks and \(O(g)\)-dimensional matrices.
* Explicit fraction-free basis and kernel formulas.
* Extraction of a degree-\(2g+1\), squarefree general-position Mumford representative.
* A source-compatible successful-halving chart.
* An exact original-\(E\) acceptance certificate, using actual points named by finite algebraic/Hensel data.

### Refuted inference

Bounded support poles plus minimum-minor selection do not, by themselves, bound raw interpolation precision. The genus-one family demonstrates that narrowly.

### Conditional

The compiler has polynomial BIT cost if the stated native conditioning/reset cap—or an additive global loss theorem—is proved. At that point matrix arithmetic, sampling, DAG evaluation, input access, and \(O(g)\)-coefficient output can all be charged at polynomial numerical precision.

### Still open

Uniform native ONE-HALF across the full saturation loop. Neither the supplied Stoll proposition nor the KM field-operation baseline supplies the missing bad-prime content bound.

A genuine falsifier would need a native, admissible family showing superpolynomial required loss or inadequate success probability **for all representatives selectable by the proposed bounded strategy**, or a failure of its actual-point invariant. One bad representative, the collision example above, or failure of a finite experiment is insufficient.

**Bottom line:** high-degree RR removes the inverse-Abel chart bottleneck at the exact-algebra level and gives a substantially cleaner certificate interface. The remaining gap is a specific quantitative content/reset theorem. No complete local-image algorithm, quantum speedup, or hardness conclusion follows yet.