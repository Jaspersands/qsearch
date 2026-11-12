## Finding and scope

**The displayed \(Z,W,F,\Delta,\Theta,\mathrm{Support}\), jet, and confluent-interpolation majorants admit a proof under the stated positive-genus native geometry. No semistable extension, split-support field, or complex atlas has to be constructed to evaluate them.**

The final reconstruction bound needs a precise output-signature qualification. The printed \(K\) is valid for unary and binary operation tables. It also covers ternary and quaternary tables taking values in the encoded set, by a sharper joint-height argument below. An unspecified “fixed arity,” however, is not itself a numerical arity bound. I give a computable replacement for arbitrary specified maximum arity.

The resulting theorem is a **conditional-input, unconditional-height-and-reconstruction theorem**: once the stated native geometric objects and compatible residues are supplied by the independently charged algorithms, no additional unknown height constant remains. It is not a construction of those objects or a complete classical comparator.

The substantive hypotheses are:

* \(g\geq1\); the source Arakelov arguments do not permit substituting \(g=0\) into the displayed formulas.
* The actual positive integer \(a\) is outside the branch locus, and the canonical degree-\(g\) divisors are unique and avoid poles and the excluded plane-chart points.
* The known plane equation and all coordinate transformations are charged input data.
* The actual integer \(c\) makes \(z=x+cy\) separating and a local parameter on every support in question.
* At the auxiliary prime, the supplied native geometry gives compatible integral, finite-flat encodings and the asserted residue separation.
* The all-pair set and its output tables are globally Galois-equivariant.

I use the mathematical source statements reproduced in the packet, not their review verdict labels.

## 1. Analytic constant and the nonminimal point-height bound

Write \(N_{\mathrm{atl}}\) for the atlas size, to distinguish it from the eventual all-pair cardinality.

At inner radius \(7/8\), the supplied Merkl theorem gives
\[
330N_{\mathrm{atl}}8^{3/2}\log8
 +13.2N_{\mathrm{atl}}d^2
 +(N_{\mathrm{atl}}-1)\log M.
\]
Using \(\log M\leq9d\), this is at most
\[
2^{16}N_{\mathrm{atl}}d^2.
\]
There is ample numerical slack: even replacing \(8^{3/2}\) by \(24\) and \(\log8\) by \(3\) leaves the coefficient below \(2^{16}\).

Consequently, the supplied atlas cardinality gives the embedding-wise bound
\[
2^{58}(r+1)d^3(d+L).
\]
The product-formula estimate
\[
\overline L\leq 1+r(r-1)(2h_B+\log2)\leq L_0
\]
therefore makes the printed
\[
\Lambda=2^{60}(r+1)d^3(d+L_0)
\]
a valid, deliberately enlarged average bound.

Both parts of Merkl’s theorem matter. Its local two-sided regularization implies
\[
|\log\|dz\|_{\mathrm{Ar}}|\leq\Lambda_\sigma;
\]
a global upper bound on \(G\) alone would not imply this.

### Why the bound is genuinely for \(h_Z\)

On the **specific normalization-resolution** \(Z\) supplied by the cover-model theorem, the metric-degree identity is
\[
[L:\mathbf Q]h_Z(b)
 =
 (b,\operatorname{div}_Z(d\pi))_{\mathrm{fin}}
 +\sum_\sigma-\log\|d\pi\|_{\mathrm{Ar}}(b_\sigma).
\]
Here \(d\pi\) denotes the differential, not multiplication of \(\pi\) by its degree.

The finite intersection proposition bounds the finite term on this same \(Z\):
\[
\frac{(b,\operatorname{div}_Z(d\pi))_{\mathrm{fin}}}{[L:\mathbf Q]}
 \leq
 d\sum_{\beta\in B}\frac{I_{\mathrm{fin}}(v,\beta)}{[L:\mathbf Q]}
 +2d^2\log d.
\]
The differential estimate \(1/800\), combined with the product formula, gives
\[
h_Z(b)\leq
\Lambda+(d+1)\sum_{\beta\in B}
 \bigl(h(\beta)+h(v)+\log2\bigr)
 +2d^2\log d+\log800.
\]
For a positive integer \(v\) outside the branch set,
\[
h(v)=\log v\leq\log(1+v),\qquad
\log2<1,\qquad \log800<7.
\]
Thus the displayed \(Z(v)\) is valid.

This is stronger than merely bounding the minimal-model height. It is exactly the strengthening needed for contraction losses. Conversely, it **does not** hold for arbitrary additional blowups: repeatedly blowing up the image of \(b\) increases its canonical intersection by the corresponding finite-place contributions without changing the generic cover.

The finite extension is only a proof device. Every term above is normalized by its degree, and the wild contribution is already bounded in that normalization. No discriminant or presentation of that extension enters the formula.

### Wronskian and intrinsic invariants

In a full chart,
\[
\sum_k|f_k|^2\leq2gd^2.
\]
For a point in its \(3/4\)-disk, Cauchy on a radius-\(1/4\) disk bounds the factorial-normalized derivatives by
\[
|f_k^{(j)}/j!|\leq4^j\sqrt{2gd^2}.
\]
Hadamard therefore gives
\[
\log|W_z|
 \leq \frac{g(g-1)}2\log4+
       \frac g2\log(2g^2d^2).
\]
Adding \(A_g\log\|dz\|_{\mathrm{Ar}}\) proves the printed \(W\).

At most \(g^3-g+r\) base values are excluded by Weierstrass images and branch values. Hence some integer \(v\leq v_0=g^3+r+1\) is suitable. Monotonicity of \(Z\) suffices; neither finding this point nor testing \(v_0\) itself is required.

Substitution into the supplied Theorem 2.4.1 gives exactly
\[
h_{\mathrm{Fal}}\leq F,\qquad
\Delta_{\mathrm{st}}\leq\Delta
\]
with the printed coefficient \(2g(g+1)(4g+1)\), the factor \(12W\), and \(93g^3\).

The node sum here is that of the **relatively minimal regular semistable model**. It is not a budget for the nodes of \(Z\).

Finally, the stated theta lemma and monotonicity of \(\log\max(1,x)\) give the printed \(\Theta\). This does not require \(h_{\mathrm{Fal}}\geq0\), and it supplies an embedding average, which is exactly what the subsequent arithmetic intersection uses.

## 2. Vertical poles, the Green moment, and `Support`

### Contraction and the vertical negative part

Let \(Y\) be the relatively minimal regular semistable model. The contraction \(Z\to Y\) factors through smooth-point blowups: a blowup at a node would create a multiplicity-two component, incompatible with the reduced final fibre.

For a section \(b\), let \(L_s(b)\) count the encountered centers. The exact formulas give
\[
\sum_s\frac{L_s(b)\log\operatorname{Norm}(s)}{[L:\mathbf Q]}
 =h_Z(b)-h_Y(b).
\]
The supplied nonnegativity of the stable Arakelov point height is used here; it must not be confused with nonnegativity of Faltings height.

Since \(a\) is integral and \(\pi\) is a morphism on \(Z\), \(b\) is disjoint there from the pole divisor. For each pole section \(P\),
\[
I_{Y,s}(b,P)\leq L_s(b).
\]

On \(Y\), intersecting the principal divisor of \(\pi\) with fibre components produces a graph-Laplacian equation. Its total positive current is at most \(d\). Summing over a superlevel cut bounds every edge voltage drop by \(d\); connecting extrema by a simple path gives
\[
\max v_C-\min v_C\leq d\delta_s.
\]
Loops cause no difficulty.

The anchor at \(b\) gives
\[
v_{C_b}\geq-dL_s(b).
\]
Equivalently, translating to \(\pi-(a-1)\), which takes value \(1\) at \(b\), gives the same negative vertical part and avoids any ambiguity about primes dividing \(a\). Therefore
\[
m_s(\pi)\leq d(L_s(b)+\delta_s)
\]
and
\[
V_\pi\leq d(h_Z(b)-h_Y(b)+\Delta_{\mathrm{st}})
       \leq d(Z+\Delta).
\]
This proves the printed \(V_\pi\) without bounding the nonminimal node count.

Compatible extension and node resolution preserve these normalized statements. That is not permission to introduce arbitrary additional smooth blowups.

### The same \(\Lambda\) pays the global lower Green bound

There is no need for an unnamed new analytic constant here.

In the supplied charts, the cover has the form
\[
u\circ\pi=\rho z
 \quad\text{or}\quad
u\circ\pi=h z^e,\qquad e\leq d,
\]
with unitary base coordinate and bounded base radius. Their spherical derivatives are bounded by a constant no larger than \(2d\).

Choose a \(3/4\)-chart containing \(b\), and the coordinate disk of radius \(1/8\) centered at \(z(b)\). Inside it, local regularization and the derivative bound give
\[
G(b,R)\geq
\log\operatorname{dist}_{\mathrm{ch}}(\pi(b),\pi(R))
-\log(2d)-\Lambda_\sigma.
\]
On its boundary,
\[
G(b,R)\geq-\log8-\Lambda_\sigma.
\]
Outside that disk, \(G(b,\cdot)\) is superharmonic because
\(dd^cG=\delta_b-\mu\); the minimum principle retains this boundary lower bound. Since chordal distance is at most one, the printed constant \(1000d\) comfortably covers both regions:
\[
G(b,R)\geq
\log\operatorname{dist}_{\mathrm{ch}}(a,\pi(R))
-\log(1000d)-\Lambda_\sigma.
\]

At a pole, the chordal distance is \(1/\sqrt{1+a^2}\). Combining this with the finite contraction bound proves
\[
\frac{(b,P)_{\mathrm{Ar}}}{[L:\mathbf Q]}
 \leq Z+\Lambda+\log(1000d)+\tfrac12\log(1+a^2)
 =C_{\mathrm{cross}}.
\]

### The moment has the claimed sign and multiplicity

Put
\[
\ell(Q)=\tfrac12\log(1+|\pi(Q)|^2),\qquad
u(Q)=\ell(Q)+G(P_\infty,Q).
\]
The polar logarithms cancel, including ramification multiplicities, and
\[
dd^cu=\pi^*\mathrm{FS}-d\mu.
\]
Normalization of \(G\) consequently gives
\[
u(Q)=\int_CG(Q,R)\pi^*\mathrm{FS}(R)+H_\pi,
\qquad H_\pi=\int_C\ell\,\mu.
\]
The Green integral has a **plus** sign.

The spherical identity is
\[
\int_C\log\operatorname{dist}_{\mathrm{ch}}(a,\pi(R))
                  \pi^*\mathrm{FS}(R)=-d/2.
\]
Evaluating the preceding representation at \(b\), and bounding the subtracted integral from below, yields
\[
\overline H_\pi
 \leq d\Lambda+\tfrac12\log(1+a^2)
       +d\bigl[\log(1000d)+\Lambda+\tfrac12\bigr].
\]
This is precisely the ledger’s \(H_\pi\).

There really are two distinct contributions in the subsequent coordinate-height estimate: the \(d\sup G\) term from bounding \(u(Q)\), and the moment \(H_\pi\). Neither may be silently removed.

For a section outside the generic poles, principal-divisor restriction gives
\[
\max(0,-v_s(\pi(Q)))\leq I_s(Q,P_\infty)+m_s(\pi).
\]
If \(\pi(Q)=0\), use the trivial zero finite-height contribution instead of restricting an identically zero function. Combining finite and archimedean terms gives
\[
h(\pi(Q))
 \leq \frac{(Q,P_\infty)_{\mathrm{Ar}}}{[L:\mathbf Q]}
       +V_\pi+d\Lambda+H_\pi.
\]

### Book 9.2.5 and the final factors

Use the supplied mathematical form of 9.2.5 on \(Y\), with its minus sign:
\[
-\frac{(D,D-\omega)}{2[L:\mathbf Q]}.
\]
For \(D=gb\), adjunction gives
\[
b^2=-[L:\mathbf Q]h_Y(b),
\]
so this term equals
\[
A_g h_Y(b).
\]
The remaining normalized terms are
\[
2g^2\Delta_{\mathrm{st}}+\Theta_{\mathrm{av}}
+\frac g2\log(2\pi)+\frac12h_{\mathrm{Fal}}
+\frac{(gb,P)}{[L:\mathbf Q]}.
\]
The nonnegative cohomology-cardinality term may be dropped.

Summing over \(P_\infty\) multiplies **every per-pole term by \(d\)**. Summing the coordinate-height inequality over \(D_t\) multiplies its additive error by **\(g\)**. Thus
\[
\begin{aligned}
\sum_{Q\in D_t}h(\pi(Q))
\leq{}&
d\left[A_gZ+2g^2\Delta+\Theta+
 \frac g2\log(2\pi)+\frac F2+gC_{\mathrm{cross}}\right]\\
&+g[d\Lambda+H_\pi+V_\pi].
\end{aligned}
\]
This is the printed `Support`.

It overcounts some canonical-height/contraction terms but does not undercount them. Genus one is included; no division by \(g-1\) occurs.

For fixed \(r\), \(g=O_r(d)\). The dominant term is \(2dg^2\Delta\), giving the claimed loose \(d^9\) envelope. The actual \(\log(1+a)\) remains charged.

## 3. A fully explicit coordinate-height input

The ledger’s root-height step can be made concrete without any unnamed constant.

Let \(f=F_{\mathrm{plane}}\), let \(M_f\) be its number of nonzero monomials, and put
\[
A_f=h([1,\operatorname{coeff}(f)])
\]
for the chosen known representative. Define
\[
C_f=A_f+\log\max(1,M_f)+\log2.
\]
Polynomial specialization and the elementary Cauchy root bound give
\[
h(y(Q))\leq D\,h(x(Q))+C_f.
\]
Monicity ensures that the specialized polynomial is nonzero. More generally, the same argument works with the actual nonzero specialized polynomial.

Therefore a concrete choice is
\[
\boxed{H=(D+1)\mathrm{Support}+gC_f.}
\]
It bounds the multiplicity-weighted sum of the coordinate heights and, since heights are nonnegative, every individual coordinate-height sum.

This calculation can use the known **global** equation. It need not construct an equation for an individual geometric component, provided the supplied equation and residue tests give the stipulated smooth locus and nonzero \(\eta\).

The fibre point has the explicit bound
\[
\boxed{H_{\mathrm{fib}}=(D+1)\log a+C_f.}
\]

Any additional rational coordinate transformation must still be charged. A residue-unit check proves invertibility, not a zero height cost. One valid effective procedure is to evaluate its known numerator and denominator in the closed divisor algebra and invert the denominator’s multiplication matrix by Cramer’s rule. Matrix dimension, polynomial degrees, coefficient heights, and determinant factors then give explicit bounds. No geometric existence theorem is needed for that calculation.

## 4. Jets and confluent interpolation

### The recurrence is correct and polynomially constructible

On the curve,
\[
D_z=\frac{V}{\eta},\qquad
V=f_y\partial_x-f_x\partial_y,\qquad
\eta=f_y-cf_x.
\]
Induction gives
\[
D_z^nf=\frac{P_n}{\eta^{2n-1}}
\]
for each coordinate function \(f=x,y\), because
\[
D_z\left(\frac{P_n}{\eta^{2n-1}}\right)
=
\frac{\eta V(P_n)-(2n-1)P_nV(\eta)}{\eta^{2n+1}}.
\]
Thus the displayed recurrence and the exponent \(2n-1\) are correct.

Each recurrence step increases degree by at most \(2D-3\), giving
\[
\deg P_n\leq2nD.
\]
It multiplies the previous numerator by fixed equation/derivative factors; it does not square it. Coefficient bit lengths consequently grow polynomially in
\[
g,\ D,\ \text{input coefficient bits},\ \log(1+|c|).
\]
There are only \(O((gD)^2)\) possible bivariate monomials at these degrees. Constructing the recurrence is therefore polynomial in these charged numerical degree parameters—not necessarily in a hypothetical compressed \(\log D\)-only input.

For every evaluated polynomial,
\[
h(P(Q))\leq h_{\mathrm{aff}}(P)+(\deg P)H+\log\max(1,M_P).
\]
The normalized Taylor coefficient is
\[
\frac{P_n(Q)}{n!\,\eta(Q)^{2n-1}}.
\]
Using \(h(\eta(Q)^{-1})=h(\eta(Q))\) proves exactly the ledger’s `Jet_n`. This pays small nonzero tangent denominators.

There are only \(2g\) required jet entries across both coordinates and all multiplicities. Hence
\[
J=2g^2\max\mathrm{Jet}_n
\]
is more than sufficient.

### The shared-denominator interpolation bound is valid

Write geometrically \(E=\sum_i m_iP_i\), and \(z_i=z(P_i)\). Then
\[
\sum_i m_i h(z_i)
 \leq g[H+\log(1+|c|)+\log2]=H_z.
\]
The monic polynomial
\[
A(T)=\prod_i(T-z_i)^{m_i}
\]
has coefficient-vector height at most \(H_z+g\log2\).

In normalized Taylor coordinates, the confluent matrix is
\[
W_{(i,n),j}=\binom jn z_i^{j-n}.
\]
Its determinant is
\[
\det W=\pm\prod_{i<j}(z_j-z_i)^{m_im_j}.
\]
There are no extra factorial factors in this normalization.

The sum of its row heights is at most
\[
gH_z+g^2\log2.
\]
Enlarging rows by the two jet right-hand sides costs at most \(J\). Cramer’s rule bounds the common homogeneous vector consisting of \(\det W\) and all numerator determinants by
\[
gH_z+g^2\log2+J+\log(g!).
\]
The product formula pays the common denominator. Combining with the bound for \(A\) proves the printed \(H_{\mathrm{closed}}\).

This is a joint affine coefficient-height bound, not merely a collection of independently chosen denominator bounds. It includes nonreduced divisors. The splitting field used to display the proof does not multiply the normalized absolute height.

Actual construction can use multiplication matrices and cyclicity, without factoring the support. Nothing here substitutes an intersection of RR subspaces for DivAdd or DivSub.

## 5. All-pair encoding, rationality, and the numerical \(K\)

If the tuple consists of the fibre coordinates, the closed-divisor coefficients, and cyclotomic entries, then
\[
H_{\mathrm{enc}}=H_{\mathrm{closed}}+H_{\mathrm{fib}}
\]
is sufficient. Add any explicitly required coordinate-transformation or metadata bounds. Roots of unity contribute zero absolute height, but their local representation and arithmetic are not free computational resources.

Put \(N=N_S\). For the usual integer separator
\[
\alpha_s=\sum_{j=0}^{q-1}u^j e_j(s),\qquad u\geq0,
\]
height subadditivity gives
\[
h(\alpha_s)
 \leq qH_{\mathrm{enc}}
   +\frac{q(q-1)}2\log\max(1,u)+\log q
 \leq H_\alpha.
\]
If signed separators are allowed, replace \(\log(u+2)\) by \(\log(|u|+2)\).

For
\[
\lambda_s(T)=
\frac{\prod_{t\ne s}(T-\alpha_t)}
     {\prod_{t\ne s}(\alpha_s-\alpha_t)},
\]
the numerator coefficient height is at most
\[
(N-1)(H_\alpha+\log2),
\]
and the denominator height is at most
\[
(N-1)(2H_\alpha+\log2).
\]
Their sum is exactly the stated \(H_\lambda\).

The product polynomial has coefficient height at most
\[
N(H_\alpha+\log2).
\]

For a binary operation table with output labels \(v_{st}\) of height at most \(H_\alpha\),
\[
R(X,Y)=\sum_{s,t}v_{st}\lambda_s(X)\lambda_t(Y).
\]
Each coefficient satisfies
\[
h(R_{ij})
 \leq N^2(H_\alpha+2H_\lambda)+2\log N.
\]
Boolean tables have output height zero and obey the same upper bound. Unary tables are smaller. Adding the product-polynomial budget and \(1\) proves the printed \(K\).

### Arity qualification

For tables taking values in the encoded set, a sharper joint bound is
\[
h(\text{coefficient})
 \leq NH_\alpha+kNH_\lambda+k\log N.
\]
Indeed, the joint height of all \(\alpha_s\) is at most \(NH_\alpha\), and that of all Lagrange coefficient vectors is at most \(NH_\lambda\). At an archimedean place the \(N^k\) summands cost only \(k\log N\).

This shows that the printed \(K\) also covers arities three and four, including Boolean relations. For \(N=1\), all such tables are constant.

Nevertheless, “fixed arity” without a stated maximum should not be used to certify this particular numerical formula. A universally safe explicit replacement, for maximum arity \(k\geq2\), is
\[
\boxed{
K_k=
N^k(H_\alpha+kH_\lambda)+k\log N
+N(H_\alpha+\log2)+1.
}
\]
For \(k=2\), this is the printed expression. Fixed \(k\) preserves polynomiality. No new height theorem is needed; the output signature determines \(k\).

### Rationality and \(P\)-integrality are separate proofs

Galois equivariance permutes the summands and their labels, so it proves that these coefficients are rational. A height bound alone would not prove rationality.

At the chosen local place, integral tuple entries and pairwise distinct separator residues imply
\[
\alpha_s\in\mathcal O,\qquad
\alpha_s-\alpha_t\in\mathcal O^\times.
\]
Hence the Lagrange formulas have integral coefficients locally. Since their global coefficients are rational, their reduced rational denominators are \(P\)-units.

Residue-good \(\eta\) and cyclicity support this conclusion only through the stipulated compatible finite-flat local algebra. They cannot replace that geometric premise. Likewise, factorial divisions in the analytic jet formula are not an instruction to divide by nonunits in a local implementation; the closed-algebra construction avoids that issue.

## 6. A concrete integer reconstruction rule

Let \(K_{\mathrm{int}}\geq1\) be an integer upper bound for the appropriate displayed expression: \(K\), or \(K_k\) if the output signature requires it.

All logarithms can be bounded outward rationally. Exact transcendental evaluation is unnecessary. For example, logarithms of known positive integers can be overbounded from their bit lengths, and factorials have explicitly computable polynomial-length representations.

A particularly simple rule is
\[
\boxed{
T=2^{\,2K_{\mathrm{int}}},\qquad
s=\lfloor\log_2P\rfloor,\qquad
e=\left\lfloor\frac{4K_{\mathrm{int}}+1}{s}\right\rfloor+1.
}
\]
Since \(\log2>1/2\),
\[
T\geq \exp(K_{\mathrm{int}}).
\]
Also
\[
P^e\geq2^{se}>2^{4K_{\mathrm{int}}+1}=2T^2.
\]
This rule uses only integer arithmetic once the majorants have been rounded upward.

For two reduced fractions with numerator absolute value and positive denominator bounded by \(T\), equality modulo \(P^e\), with both denominators \(P\)-units, implies
\[
P^e\mid ad-bc,\qquad |ad-bc|\leq2T^2<P^e.
\]
Thus they are equal. Standard rational reconstruction therefore uniquely recovers every coefficient from its correct residue.

## 7. Resources, falsifiers, and the admitted output

The effective statement charges:

* Reading the actual plane coefficients, transformations, integer choices, and local field presentations.
* Constructing the bivariate recurrence polynomials and their coefficient bounds.
* Enumerating the \(N\) encoded objects and constructing the specified tables—not time polynomial merely in \(\log N\).
* Every local precision digit: the modulus has \(O(K_{\mathrm{int}}+\log P)\) bits under the rule above.
* Local extension degree and basis arithmetic for producing those residues.
* Rational reconstruction and the explicit output size, potentially \(O(N^kK_{\mathrm{int}})\) bits for dense fixed-arity outputs.

Intrinsic heights do not bound coordinates in an arbitrary high-height number-field basis. That issue disappears for the final rational coefficients, but not for any additionally requested algebraic-coordinate output.

Nor does a reconstruction threshold certify that an arbitrary lifting routine delivers residues to that precision. Any nonunit divisions or precision loss in the independently paid local algorithm must already be accounted for. The theorem applies to correctly aligned residues modulo the stated modulus.

The decisive falsifiers are concrete:

* Using an arbitrary blowup model in place of the source \(Z\).
* Charging a nonminimal node count to \(\Delta_{\mathrm{st}}\).
* Losing uniqueness or allowing support at a pole or unresolved plane singularity.
* Failure of the \(\eta\), cyclicity, or separator-unit tests.
* Failure of global Galois equivariance.
* Requesting an output arity not covered by the chosen numerical \(K\).
* Supplying inaccurate or incompatibly aligned local residues.

None is repaired by a successful finite reconstruction experiment.

**Admitted conclusion:** under the specified positive-genus native geometry and charged local-computation interface, the height-to-precision bridge is effective. The printed support and closed-encoding formulas are valid, and the boxed integer rule supplies a computable certified reconstruction precision. The final arity must be stated or handled by \(K_k\). No semistable-model algorithm, global torsion splitting field, analytic-chart construction, full comparator, hardness claim, or quantum speedup follows.