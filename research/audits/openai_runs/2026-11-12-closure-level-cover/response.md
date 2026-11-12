## Disposition

**The polynomial-degree and polynomial logarithmic-height bound is obtainable from a uniformly bounded supplied atlas for the requested plane-cover/base-map/deck-map output.** A useful simplification is to avoid Weil-pairing equations entirely: construct all ordered torsion bases and take any connected component. Under the stated monodromy hypothesis, every such component has the function field of the full symplectic level cover.

There is an important output distinction:

- This constructs the cover, actual torsion coordinates on it, and actual deck transformations.
- It does **not** automatically produce a tautological frame normalized by
  \[
  e_\ell(P_i,P_j)=\zeta_\ell^{J_{ij}}.
  \]
  If that normalized frame is part of “presentation,” an additional pairing obligation remains. Below, I reduce it to **one pairing evaluation**, rather than assuming a polynomial-size Weil-pairing circuit.

Neither result constructs a bounded Jacobian/addition atlas from arbitrary native curves. Nor does either produce arithmetic Frobenius or resolve its scalar-linearization issue.

---

## 1. Exact supplied-atlas contract

Fix \(a\geq1\), put \(n=2a\), and fix an atlas type
\[
\tau=(N,S,d_0,R,D).
\]
The type must be bounded by specified functions of \(a\), not chosen separately for each family.

Input consists of:

1. \(A/\mathbf Q(t)\subset\mathbf P^N\), with at most \(S\) equations of projective degree at most \(d_0\).
2. On every standard affine patch, those equations generate the actual radical ideal of the patch. Merely defining its geometric point set is insufficient for the argument below.
3. A **complete geometric atlas** for addition, with at most \(R\) charts of bidegree at most \((D,D)\), and the identity point.
4. Dense rational-function coefficients whose numerator and denominator \(t\)-degrees are at most \(T\), and whose integer coefficient logarithmic heights are at most \(B\).
5. The promises that \(A\) is the Jacobian of the given genus-\(a\) generic curve, and that its geometric mod-\(\ell\) monodromy is the full symplectic group.

Here \(\ell\) is an odd prime. The Jacobian and monodromy promises are hypotheses, not conclusions inferred from finite computations.

Set
\[
k=\mathbf Q(\zeta_\ell),\qquad K=k(t).
\]
Represent \(k\) by
\[
\Phi_\ell(Z)=1+Z+\cdots+Z^{\ell-1}.
\]
Thus its degree is \(\ell-1\), its defining polynomial has constant coefficient height, and all arithmetic in this degree-\((\ell-1)\) field is charged.

### Claimed output

A polynomial
\[
q(t,Y)\in k[t,Y],
\]
monic in \(Y\), irreducible over \(K\), with
\[
\deg_Yq=s_\ell
 :=|\operatorname{Sp}_{2a}(\mathbf F_\ell)|
 =\ell^{a^2}\prod_{i=1}^{a}(\ell^{2i}-1),
\]
together with:

- the base map \(t\);
- coordinates of an actual ordered basis of \(A[\ell]\) in \(K[Y]/(q)\);
- rational-function formulas for deck generators, represented as
  \[
  Y\longmapsto \frac{u_g(t,Y)}{v_g(t)},\qquad \deg_Yu_g<s_\ell;
  \]
- explicit denominators and a nonzero discriminant polynomial specifying an open set on which the displayed plane model is finite étale.

For a constant \(C_\tau\) depending only on the fixed atlas type and \(a\), all displayed degrees, logarithmic coefficient heights, total output length, and deterministic bit costs are bounded by
\[
(2+\ell+B+T)^{C_\tau}.
\]

Consequently the requested \(\operatorname{poly}_a(\ell,B)\) statement follows **only if** the input contract also bounds \(T\) polynomially in \(B\), with genus-uniform exponent. A bound independent of an uncharged \(t\)-degree would be false.

The construction below supplies the arithmetic argument missing from a direct appeal to Pila.

---

## 2. Multiplication atlases: expansion is polynomial, but the branching matters

Construct multiplication by \(m\) using its binary expansion.

Suppose \(H\) is one chart for \([r]\). To double, use
\[
G(H(X),H(X)).
\]
The same parent chart is used twice. For \(2r+1\), subsequently add \(X\).

At a given point, choose a parent chart nonzero there; completeness of the addition atlas supplies a nonzero child chart. Thus this construction remains a complete atlas.

If \(L=\lceil\log_2m\rceil\), one obtains the explicit bounds
\[
|\mathcal M_m|\le R^{2L+2},
\]
and, writing \(d_j\) for projective degree after a binary step,
\[
d_{j+1}\le (2D^2+D)d_j.
\]
Both are polynomial in numerical \(m\), with atlas-type-dependent exponents.

The first formula is important. Recursively allowing two independently selected parent charts produces an unnecessary squaring recurrence for chart count. That is not the construction being used.

Clear the input rational-function denominators chart by chart. For a polynomial \(F\), use the logarithm of its coefficient \(\ell^1\)-norm as a height majorant. Submultiplicativity gives a recurrence of the form
\[
h_{j+1}\le (2D^2+D)h_j+
 O_\tau(B+\log(T+2)).
\]
The \(t\)-degree satisfies the corresponding recurrence with \(T\) in place of height. Hence the **expanded** multiplication atlas has:

- polynomially many charts;
- polynomial projective degree;
- polynomial \(t\)-degree;
- polynomial logarithmic coefficient height.

It is expanded in the original, fixed projective variables. No elimination in \(O(\log\ell)\) new straight-line-program variables is being asserted.

### Torsion equations and extraneous components

For every multiplication chart, impose its projective cross-products with the identity:
\[
H_iE_j-H_jE_i=0.
\]
All charts are included.

Locally, a chart nonzero at the point identifies these equations with the pullback of the identity ideal under \([\ell]\). Because characteristic is zero, \([\ell]\) is finite étale, of degree
\[
L_\ell=\ell^{2a}.
\]
Thus the resulting torsion scheme is finite and reduced.

Use the disjoint patch partition
\[
X_i=1,\qquad X_j=0\quad(j<i).
\]
This prevents counting projective points repeatedly. Its components have total degree \(L_\ell\).

There is no compactification step here that introduces additional components. The completeness and radical-ideal premises are doing actual work.

---

## 3. Fixed-variable finite-algebra extraction, including heights

The needed elimination can be performed without invoking an unspecified Gröbner-basis or arithmetic-elimination theorem.

### Finite-algebra lemma

Let a reduced finite scheme of at most \(L\) points be defined by \(s\) polynomials of degree at most \(d\) in a fixed number \(r\) of variables over \(k(t)\). Suppose coefficient \(t\)-degrees and logarithmic heights are bounded.

Its coordinate algebra, multiplication tables, and coordinate functions can be constructed with polynomial bit cost and polynomial degree/height bounds in
\[
s,d,L,[k:\mathbf Q],T,B,
\]
with exponent depending only on \(r\).

Here is a constructive justification.

At every point, the gradients of the generators span the cotangent space. Choose \(r\) linear combinations
\[
g_i=\sum_{j=1}^{s}u_i^{\,j-1}f_j.
\]
The product, over the at most \(L\) points, of the relevant Jacobian determinants is a nonzero polynomial in the \(r\) parameters \(u_i\), of degree at most \(r(s-1)L\). Searching a grid of that size in each parameter therefore finds combinations nonsingular at every original point. Since \(r\) is fixed, this search is polynomial.

Put \(D=d+1\) and deform:
\[
g_i(X)+\varepsilon X_i^D.
\]
Over \(k(t,\varepsilon)\), the leading monomials are the pairwise coprime \(X_i^D\). Reduction therefore gives the explicit box basis
\[
X_1^{e_1}\cdots X_r^{e_r},\qquad 0\le e_i<D,
\]
of size \(M=D^r\).

Compute the multiplication matrices and
\[
C(\varepsilon,U,Z)
 =\det\!\left(ZI-\sum_iU_iM_{X_i}\right).
\]
Remove its common lowest power of \(\varepsilon\), then set \(\varepsilon=0\). The resulting polynomial has the form
\[
c(U)\prod_v(Z-U\!\cdot v)^{m_v},
\]
where \(v\) runs over finite limiting points; divergent branches contribute only to \(c(U)\).

Every nonsingular original point occurs: its formal power-series lift is obtained recursively by solving with its invertible Jacobian.

Choose small integral \(U\) avoiding collisions and \(c(U)=0\). A moment-curve search
\[
U=(1,u,\ldots,u^{r-1})
\]
has only polynomially many bad values.

Let \(p(Z)\) be the specialized polynomial, \(d_1=\gcd(p,p')\), and \(p_{\rm sf}=p/d_1\). On the squarefree algebra, the coordinates are
\[
X_i=
-\frac{(\partial C/\partial U_i)/d_1}{p'/d_1}
 \pmod {p_{\rm sf}}.
\]
Filter by all the original equations, and also by \(Z-\sum U_iX_i\), using univariate gcds. The result is a reduced subset of the original scheme. Taking the largest resulting subset over the bounded search gives the whole scheme.

All matrices have polynomial size. They involve only the fixed collection of variables \(t,\varepsilon,U,Z\). Their degrees are polynomially bounded. Determinant bounds give polynomial logarithmic heights: an \(m\times m\) determinant formed from entries of height \(h\) has logarithmic height bounded by
\[
O\!\left(m(h+\log m+\log(\text{support size}))\right),
\]
after common denominators are charged. Fraction-free linear algebra and subresultants implement the operations with polynomial bit cost.

This proves the lemma’s relevant degree, height, and construction claims; it does not merely count field operations.

Apply it to the torsion patches. We obtain
\[
T_\ell=K[A[\ell]]
\]
as an explicit finite étale algebra of dimension \(\ell^{2a}\).

---

## 4. All frames, rather than pairing equations

Form the fixed tensor power
\[
R_0=T_\ell^{\otimes n},\qquad n=2a.
\]
Its dimension is
\[
\ell^{n^2},
\]
still polynomial in numerical \(\ell\) at fixed genus.

For every nonzero \(v\in\mathbf F_\ell^n\), exclude the locus
\[
\sum_i v_iP_i=0.
\]
There are only \(\ell^n-1\) tests. Scalar multiplication and the fixed number of additions use the already bounded atlases.

These exclusions require no geometric support splitting. In a finite étale algebra \(R\), an equality locus is represented by an ideal, and its complementary support by an idempotent. Compute these using kernels, images, and linear systems over \(K\).

For height control, compute every exclusion idempotent in the **same original tensor basis**, multiply them, and change basis only once. Do not repeatedly replace the algebra by a newly presented quotient with an uncontrolled sequence of rational basis changes.

The resulting algebra \(R\) represents all ordered bases of \(A[\ell]\), and has dimension
\[
D_\ell=|\operatorname{GL}_{n}(\mathbf F_\ell)|
      =\prod_{i=0}^{n-1}(\ell^n-\ell^i)
      <\ell^{n^2}.
\]

### Primitive element

For a \(K\)-basis \(b_0,\ldots,b_{D_\ell-1}\), try
\[
w(s)=\sum_j s^jb_j.
\]
For each pair of distinct geometric points, equality of their \(w(s)\)-values excludes at most \(D_\ell-1\) integers. Thus fewer than \(D_\ell^3\) trials suffice.

The characteristic polynomial of multiplication by \(w\) is squarefree precisely when it separates all points. Once this occurs, powers of \(w\) are a basis. Recover every torsion coordinate by linear algebra.

Multiply \(w\) by an explicit common denominator \(\delta(t)\), obtaining \(Y=\delta w\) and a monic polynomial
\[
f(t,Y)\in \mathbf Z[\zeta_\ell][t,Y].
\]
The denominator product contains polynomially many factors of already bounded size; its degree and logarithmic height are therefore polynomial. So are those of \(f\) and all coordinate formulas.

---

## 5. Connected-component extraction is charged, not assumed

Factor \(f\) over \(k(t)\).

For completeness, polynomial-time factorization in this particular setting can be reduced to bounded exact linear algebra and integer lattice reduction.

1. Choose an integer \(t_0\) avoiding the leading coefficient and discriminant. A search bounded by their degrees suffices.
2. Factor \(f(t_0,Y)\) over \(k\). To reduce this to rational factorization, shift \(Y\) by a small integer multiple of \(\zeta_\ell\) and take the norm to \(\mathbf Q\). A polynomially bounded search makes the norm squarefree: collisions between roots belonging to different embeddings exclude at most quadratically many shifts. Rational factors are pulled back by gcds.
3. Lift a specialized factor modulo \((t-t_0)^k\). If \(d=\deg_Yf\) and \(T_f=\deg_tf\), take
   \[
   k>2dT_f.
   \]
   Search, by linear algebra, for polynomials \(h(t,Y)\) with \(\deg_t h\le T_f\), bounded \(Y\)-degree, divisible by the lifted factor. A genuine monic global factor satisfies these bounds. Conversely, the resultant of that genuine factor with \(h\) has \(t\)-degree at most \(2dT_f\) and is divisible by \((t-t_0)^k\), so it vanishes. Gcds recover a global factor.

Hensel lifting uses fixed Sylvester inverses; denominator exponents and coefficient heights grow polynomially in the lifting order.

The rational factorization step also has a bounded implementation. Choose a good small prime, factor modulo it, and Hensel-lift to modulus \(p^k\). A lattice of coefficient vectors encodes divisibility by one lifted factor. Integer factors have coefficient height bounded by the input height plus \(O(d)\), by the elementary root-product/Mahler bound. Choose \(k\log p\) larger than the resulting resultant bound. A sufficiently short lattice vector must then share an exact rational factor, because its integral resultant is divisible by \(p^k\) but has absolute value below \(p^k\).

The required lattice reduction is the usual size-reduction/swap algorithm with parameter \(3/4\): the product of prefix Gram determinants is a positive integer, decreases by a fixed factor at each swap, and has polynomial initial logarithm. Reduced Gram–Schmidt lengths give the approximation bound \(2^{(r-1)/2}\) in rank \(r\). These observations give polynomial iteration count, coefficient bit size, and the short-vector guarantee needed above.

Thus factorization is not an uncharged irreducibility oracle.

### Why any factor is correct

Let \(F\) be the splitting field of \(A[\ell]\) over \(K\).

An ordered basis generates \(F\): every torsion point is an \(\mathbf F_\ell\)-linear combination of its entries. Therefore **every connected component of the all-frame scheme has function field \(F\)**.

The canonical Jacobian pairing is Galois-equivariant. Since \(K\) contains \(\mu_\ell\), the arithmetic image lies in \(\operatorname{Sp}_n(\mathbf F_\ell)\). It contains the promised full geometric image, so arithmetic and geometric images are both that group.

Consequently:

- every irreducible factor has degree \(s_\ell\);
- each component is geometrically connected;
- its constant field is exactly \(k\);
- its function field is the function field of the full symplectic level cover.

No pairing evaluation or “correct component” oracle is needed for this conclusion.

Choose any factor \(q\). Its degree and logarithmic height are polynomially bounded by the charged factorization construction. The equation \(q(t,Y)=0\) is an actual finite separable plane model. Its normalization is the compact cover. The displayed plane model may be singular; zeros of its discriminant must not all be called genuine branch points.

---

## 6. Actual deck maps and the symplectic marking boundary

Enumerate
\[
M\in\operatorname{GL}_n(\mathbf F_\ell).
\]
There are fewer than \(\ell^{n^2}\) matrices. Transform the frame by
\[
P'_i=\sum_jP_jM_{ji}.
\]
Evaluate the primitive-element expression on this transformed frame.

Projective chart selection and division are done inside the finite étale algebra. For an element \(h\), its zero and nonzero supports are obtained from the kernel and image of multiplication by \(h\); inversion on its nonzero support is a linear-system computation. No individual torsion points are supplied or split.

A transformed primitive element \(Y_M\) preserves the chosen component exactly when
\[
q(t,Y_M)=0\quad\text{in }K[Y]/(q).
\]
The preserving matrices form the actual Galois image \(H\), and
\[
Y\longmapsto Y_M
\]
gives its deck maps.

Each map is computed directly from bounded scalar/addition charts, not by repeatedly composing previously enlarged rational maps.

### Obtaining a fixed-size generating set

Solve over \(\mathbf F_\ell\)
\[
M^{\mathsf T}BM=B\qquad(M\in H)
\]
for alternating matrices \(B\).

Because \(H\) is conjugate to the full symplectic group, this solution space is one-dimensional and every nonzero solution is nondegenerate. One quick proof of uniqueness is that the ratio of two invariant forms commutes with every symplectic transvection; it therefore preserves every line and is scalar.

Symplectic Gram–Schmidt produces \(S\) with
\[
S^{\mathsf T}BS=J.
\]
The standard transvections associated to
\[
e_i,\ f_i,\ e_i+e_j,\ f_i+f_j,\ e_i+f_j\quad(i\ne j)
\]
give \(O(a^2)\) generators. Their powers provide arbitrary prime-field parameters; their products give elementary symplectic row operations. Conjugate them by \(S\) and output the corresponding already constructed deck maps. Their generated subgroup can also be checked against the explicitly enumerated \(H\).

### What remains if a normalized universal frame is required

Let \(E\) be the matrix of actual Weil-pairing exponents relative to the constructed frame and the specified \(\zeta_\ell\). The preceding computation proves
\[
E=cB,\qquad c\in\mathbf F_\ell^\times.
\]
It does **not** compute \(c\).

Thus a normalized tautological frame requires one certified evaluation
\[
e_\ell(P_i,P_j),\qquad B_{ij}\ne0.
\]
A table of the \(\ell\) powers of \(\zeta_\ell\) then recovers \(c\), at polynomial cost. Obtaining that pairing value is the residual obligation; a circuit for it has not been assumed.

This scalar is a polarization-marking scalar, not permission to choose a scalar Frobenius. No Frobenius matrix is output here.

---

## 7. Uniform bounds and falsifiers

All operations above consist of:

- expanded polynomials in fixed geometric variables;
- fixed tensor powers of polynomial-dimensional finite algebras;
- polynomially many products of bounded elements;
- polynomial-size exact linear systems, determinants, gcds and the described factorization.

Thus one obtains the stated envelope
\[
\deg,\ h_{\log},\ \text{output bits},\ \text{bit operations}
 \le (2+\ell+B+T)^{C_\tau}.
\]
The exponent is computable from the displayed chart recurrences, the box size \((d+1)^N\), the fixed-dimensional parameter grids, and the algebra dimension \(\ell^{n^2}\). It contains no family-dependent or fixed-\(X\) constant. Cyclotomic arithmetic, common denominators and dense output are included.

Useful exact falsifiers are:

- a point at which all alleged multiplication charts vanish;
- torsion-algebra dimension different from \(\ell^{2a}\);
- frame-algebra dimension different from \(|\mathrm{GL}_n(\mathbf F_\ell)|\);
- a selected component of degree different from \(s_\ell\);
- a claimed deck map failing \(q(t,Y_M)=0\);
- a denominator or coefficient-height recurrence exceeding the stated polynomial envelope.

Passing these finite algebraic checks does not independently prove the geometric-monodromy promise.

## Final boundary

Pila’s retained supplied-atlas machinery supports the multiplication-chart and torsion-algebra strategy. **Its finite-field operation count alone does not prove the characteristic-zero height statement.** The arithmetic arguments above are necessary additions.

For the requested **plane model, base map and deck generators**, the supplied-atlas blocker is removable without a Weil-pairing circuit. For a **specified \(\zeta_\ell\)-normalized universal level structure**, one pairing evaluation remains explicitly unpaid.

The construction of the uniformly bounded, radical, complete Jacobian/addition atlas from native genus-\(a\) curves remains separate. Nothing here closes native surface point counting, characteristic-zero lifting, CRT height recovery, or genuine arithmetic coefficient-module linearization.