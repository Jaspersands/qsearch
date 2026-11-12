## Verdict and quantifiers

**Uniqueness of the effective representative is not, by itself, a height bound.** In particular, a bound involving only the displayed curve and field parameters cannot hold uniformly over basepoints satisfying the stated uniqueness condition: the height of \(b\) must be controlled.

There are two different statements:

1. **Uniform-basepoint statement:** for every \(b\) for which all representatives are unique, their heights are bounded polynomially in the listed parameters, without charging \(h(b)\). This statement is false. An explicit counterfamily is given below; even its nonzero torsion representative has unbounded rational coefficients.

2. **Controlled-choice statement:** one can choose a suitably bounded-height \(b\), charge its construction and field, and then prove the requested growing-genus bound. The counterfamily does **not** refute this statement. I give a quantitative existence argument for a small \(b\), but the subsequent uniform arithmetic Abel-inverse estimate is not established by the supplied assumptions or by Theorem B.4.

Thus I cannot certify removal of the height blocker under the controlled-choice interpretation. The exact outstanding inequality is identified below.

Throughout, I accept the question’s uniform Merkl/Green bound and polynomial stable Faltings bound **as assumptions**. I do not treat the provisional atlas file as a proved theorem or re-audit that separate obligation.

---

## 1. An explicit obstruction to omitting the basepoint height

Take the fixed elliptic curve
\[
E:\quad y^2=x^3-2x
\]
over \(\mathbf Q\), with origin \(O\). Its projective equation is
\[
Y^2Z=X^3-2XZ^2.
\]
It is smooth, with discriminant \(512\). Consequently all of the following are fixed:

- genus \(g=1\);
- plane degree \(D=3\);
- degree \(d=2\) of \(x:E\to\mathbf P^1\);
- logarithmic model height \(B=\log 2\);
- base-field degree \(1\), discriminant \(1\), and field-presentation size.

Set
\[
\ell=2,\qquad T=\{O,Q\},\qquad Q=(0,0).
\]
Here \(Q=-Q\), so \(Q\) has order two. Thus \(m=1\). This subgroup requires no supplied torsion oracle: its description and verification have constant cost.

Let \(P=(2,2)\), and define
\[
b_N=[2^N]P,\qquad N\geq1.
\]
The duplication formula is
\[
x(2R)=\frac{(x(R)^2+2)^2}{4x(R)(x(R)^2-2)}.
\]
Since \(x(b_1)=9/4\), induction gives
\[
v_2(x(b_N))=-2N.                                      \tag{1}
\]
Indeed, if \(v_2(x)=-2N\), then both \(x^2+2\) and \(x^2-2\) have valuation \(-4N\). The displayed formula therefore has valuation
\[
-8N-(2-6N)=-2N-2.
\]
In particular, all these points exist, are affine, and have distinct \(x\)-coordinates.

On a genus-one curve every degree-one divisor class has a unique effective representative. In this case the representatives are explicitly
\[
D_O=(b_N),\qquad D_Q=(b_N+Q).
\]
Uniqueness can also be checked directly: two distinct linearly equivalent points would give a rational function of degree one, hence an isomorphism \(E\simeq\mathbf P^1\), which is impossible.

Addition by \(Q\) gives
\[
x(R+Q)=-\frac{2}{x(R)}.
\]
Therefore
\[
v_2(x(b_N+Q))=2N+1.                                  \tag{2}
\]
Write \(x(b_N+Q)=a_N/c_N\) in lowest terms. Then \(c_N\) is odd and \(2^{2N+1}\mid a_N\). The primitive closed-support eliminant is
\[
F_N(U,V)=c_NU-a_NV,
\]
and its logarithmic coefficient height satisfies
\[
h(F_N)=\log\max(|a_N|,|c_N|)
       \geq(2N+1)\log 2.                              \tag{3}
\]

All listed curve, torsion-rank, map, and field charges remain constant, while the requested coefficient height tends to infinity. Every support point is rational, so no divisor splitting or extension-field issue is involved. The complex curve, its Green estimates, and its stable Faltings height are unchanged.

This also avoids relying only on the zero torsion class: **the representative of the nonzero element \(Q\) already falsifies the bound.**

### Precisely what this falsifies

It falsifies any assertion that uniqueness alone permits the omission of the basepoint height.

It does **not** falsify a theorem whose model-height parameter explicitly includes \(b_N\). Nor does it falsify an algorithm that deliberately chooses a different, small basepoint. Reading or producing the coordinates of \(b_N\) already incurs a growing bit cost; that cost cannot be hidden in a constant-size description of \(\mathbf Q\).

More generally, uniqueness forces
\[
D_0=gb.
\]
For the binary eliminant of its \(x\)-coordinate,
\[
h(F_{D_0})\geq g\,h(x(b))-\tfrac12\log(g+1).           \tag{4}
\]
Thus some basepoint-height charge is structurally necessary, not an artefact of this example.

---

## 2. A small basepoint can exist: this is a separate, provable repair

The existential interpretation deserves more than the preceding counterexample. There is a useful quantitative argument showing that bad basepoints form a polynomially bounded finite set.

Work geometrically in characteristic zero. Suppose \(g\geq2\), and write
\[
L_t=\omega_C\otimes t^{-1}.
\]
Riemann–Roch gives
\[
h^0(\mathcal O_C(gb)\otimes t)
 =1+h^0(L_t(-gb)).
\]
Thus failure of uniqueness means that a section of \(L_t\) vanishes to order at least \(g\) at \(b\).

For \(t=0\), \(h^0(L_t)=g\). For nonzero degree-zero \(t\),
\[
h^0(L_t)=g-1,
\]
because a nontrivial degree-zero line bundle has no nonzero section.

For a line bundle \(L\) with \(n\) independent sections, their Wronskian is a nonzero section of
\[
L^{\otimes n}\otimes
\omega_C^{\otimes n(n-1)/2}.
\]
Nonvanishing follows in characteristic zero from the usual Wronskian criterion for linearly independent meromorphic functions. Its zero divisor has degree
\[
n\deg L+n(n-1)(g-1).
\]
A section vanishing to order at least \(g\) forces this Wronskian to vanish, since here \(n\leq g\). Consequently the number of bad geometric basepoints for a fixed \(t\) is at most
\[
\begin{cases}
g^3-g,&t=0,\\
g(g-1)^2,&t\ne0.
\end{cases}
\]
For the entire subgroup, there are at most
\[
|T|g^3=\ell^m g^3                                      \tag{5}
\]
bad basepoints. For \(g=1\), there are none.

Now let \(x:C\to\mathbf P^1\) be the supplied finite coordinate map, of degree \(d_x\). Charge its actual degree and coefficients; if the notation \(d\) refers to a different plane map, \(d_x\) must not silently be identified with \(d\).

The images of the bad points occupy at most \(\ell^m g^3\) values of \(x\). Add the finitely many values excluded by the chosen affine model, its singularities, or the desired unramified-fibre condition. Let the resulting count be \(M\). Among
\[
0,1,\ldots,M
\]
some value \(a\) is not excluded. Every point \(b\) over that value is good, and
\[
[K(b):K]\leq d_x.
\]

For the usual normalization-of-a-plane-model presentation
\[
F(X,Y)=0,\qquad \deg F\leq D,\qquad h(F)\leq B,
\]
choose a fibre avoiding singular image points. Specialization gives
\[
h(F(a,Y))\leq B+D\log(M+1)+\log(D+1).
\]
The elementary root-height estimate then yields
\[
h([1:a:y(b)])
 \leq B+(D+1)\log(M+1)+\tfrac32\log(D+1).              \tag{6}
\]
Thus the height of a good basepoint can be polynomially controlled—in fact, the dependence on the number of torsion classes in this existence argument is logarithmic.

Important limitations:

- This proves **existence**, not a native procedure for identifying the good candidate without access to \(T\).
- Testing the conditions requires charged representations of the torsion classes and charged Riemann–Roch computations.
- The field \(K(b)\), its presentation, denominators, and discriminant must be recorded. They are not supplied by the word “choose.”
- If \(C\) is presented by a non-birational plane map, the equations and heights needed to lift the plane point to \(C\) must also be charged.

Accordingly, the missing \(h(b)\) can plausibly be repaired. Doing so does **not** prove the desired height bound for \(D_t\), \(t\ne0\).

---

## 3. Exactly which heights and field degrees are involved

### Class height is not representative height

The equality
\[
\widehat h_\Theta(t)=0
\]
concerns a point of the Jacobian with its canonical polarized height. It does not directly concern:

- the effective divisor \(D_t\);
- the individual points in its support;
- a polynomial encoding their coordinates;
- the bit length of coefficients over a specified number field.

The counterfamily separates these notions with a fixed Jacobian and fixed nonzero torsion class.

### Divisor height versus coordinate eliminant

Write
\[
D=\sum_i n_iP_i,\qquad \sum_i n_i=g,
\]
and \(x(P_i)=[\alpha_i:\beta_i]\). Define the projective binary form
\[
F_D(U,V)=\prod_i(\beta_iU-\alpha_iV)^{n_i}.
\]
It accommodates points at infinity and repeated coordinates.

Gauss-norm multiplicativity at finite places, and the elementary coefficient/Mahler-measure inequalities at archimedean places, give
\[
\boxed{
\sum_i n_i h(x(P_i))-\tfrac12\log(g+1)
\ \leq\ h(F_D)\
\leq\sum_i n_i h(x(P_i))+g\log2 .
}                                                        \tag{7}
\]
For the upper bound, each coefficient is bounded by the corresponding binomial coefficient times the product of the factor norms. For the lower bound, Mahler measure is at most the Euclidean coefficient norm, hence at most \(\sqrt{g+1}\) times the maximum coefficient.

Thus a coefficient-height bound controls every individual \(x\)-coordinate height, and conversely a bound on the sum of coordinate heights controls the eliminant.

An \(x\)-eliminant need not, alone, distinguish points above the same \(x\)-value. Exact divisor encoding may additionally require \(y\)-data or a finite coordinate algebra. Those data and their recovery are not free. On a nonvertical affine plane chart, however, the equation supplies the elementary estimate
\[
h(y(P))
 \leq D\,h(x(P))+B+\tfrac32\log(D+1),
\]
provided the specialized polynomial is nonzero.

### Descent does not require splitting the support

Let \(L\) contain the fields of definition of \(b\) and the class \(t\). If \(D_t\) is unique, every \(\sigma\in\operatorname{Gal}(\overline L/L)\) fixes it: \(\sigma D_t\) is another effective representative of the same class. Hence \(D_t\) is a **closed divisor over \(L\)**.

Every closed point in its support then has residue degree at most \(g\), so for an individual geometric support point,
\[
[\mathbf Q(P):\mathbf Q]\leq g[L:\mathbf Q].            \tag{8}
\]
This conclusion does not say that \(L\) contains the point. Nor does it bound the simultaneous splitting field by \(g[L:\mathbf Q]\). A splitting field can be much larger and is unnecessary for a closed-divisor representation.

This repairs the logical shortcut in source Lemma 6.7: rationality of the class is not rationality of every support point. Uniqueness plus divisor degree gives the valid individual-degree bound.

### Fixed rank requires a Galois qualification

If \(T\) is Galois stable, its full action factors through
\[
\operatorname{GL}_m(\mathbf F_\ell),
\]
so the field making the entire module rational has degree at most
\[
|\operatorname{GL}_m(\mathbf F_\ell)|<\ell^{m^2}.
\]
For an individual \(t\), its orbit has size at most \(|T|=\ell^m\).

If \(T\) is merely an abstract rank-\(m\) subgroup of geometric torsion, these bounds do not follow: Galois can move it to other subgroups. Fixed rank alone does not provide a polynomial-degree class field. Constructing the relevant field and its action remains charged even when its degree is bounded.

### Absolute heights versus actual coefficient bits

Suppose \(F_D\) is defined over a supplied field \(L\) of degree \(q\), and normalize one nonzero coefficient to \(1\). If \(h(F_D)\leq H\), every resulting coefficient has absolute height at most \(H\).

A coefficient \(c\) of degree \(e\leq q\) has primitive minimal polynomial with
\[
\log\max|\text{coefficients}|
 \leq eH+e\log2.
\]
Thus its minimal polynomial uses \(O(e^2(H+1))\) bits. Separate minimal polynomials do not specify the joint conjugate choices, so this is not yet a complete common-field encoding.

For a concrete alternative, take a supplied presentation
\[
L=\mathbf Q(\theta)
\]
with \(\theta\) integral and monic minimal polynomial of logarithmic coefficient height \(H_L\). Writing
\[
c=\sum_{j=0}^{q-1}a_j\theta^j,\qquad a_j\in\mathbf Q,
\]
Lagrange interpolation over the \(q\) conjugates gives the safe bound
\[
h(a_j)\leq qH+8q^2\bigl(H_L+\log(2q)\bigr).
\]
This follows by using
\[
\sum_\sigma \sigma(c)
 \frac{f(X)}{(X-\sigma\theta)f'(\sigma\theta)}
\]
and applying the elementary sum, product, and evaluation height inequalities. It gives a polynomial-size rational-coordinate encoding **when \(q,H_L,H\) are all charged and polynomially bounded**.

Likewise, rational reconstruction of numerators and denominators bounded by \(A\), at a prime not dividing the denominators, requires modulus greater than \(2A^2\) for the standard uniqueness certificate. Precision therefore scales with coefficient bit length; it cannot be inferred merely from canonical-height zero.

---

## 4. What Theorem B.4 actually supplies

The displayed upper constant in Theorem B.3 is
\[
c_2=(2^{2g}-1)h_\Theta(A)
       +(2^{2g+1}-1/3)\,g\log2.
\]
Even granting a polynomial bound on \(h_\Theta(A)\), this gives
\[
h(P)\leq O\!\left(4^g(h_\Theta(A)+g)\right)
\]
for torsion. For \(g=\ell^{\,a}\), this is not polynomial in \(\ell\).

Theorem B.4 itself says that its constant depends on \(N,g,D\), and is polynomial only in its last three listed items: equation height, extension degree, and logarithmic field discriminant. It does not assert polynomial dependence on growing genus or degree.

There are further representation costs:

- The standard principal \(4\Theta\) linear system has \(4^g\) sections. Materializing its complete coordinate vector is already exponential in \(g\).
- Appendix D explicitly states a construction cost of \(\exp(\operatorname{poly}(g))\).
- Algorithm 10 inverts by examining \(\ell^{2g}\) divisorial representatives.
- Restricting enumeration to \(\ell^m\) known representatives would only help **after** their native construction; they cannot be assumed supplied.
- B.4 bounds the height in its specified Jacobian representation, not the height of the unique degree-\(g\) effective representative.

The supplied excerpt does not contain the detailed comparison asserted from Theorem D.2 or the cited results [PW21] and [Rém10]. I cannot audit unseen constants or use those citations as a substitute for the missing uniform estimate.

Consequently B.4 does not remove this blocker, even under the two analytic/arithmetic assumptions granted by the question.

---

## 5. The exact remaining proof obligation

There is a way to formulate the missing estimate without demanding a numerical condition-number bound for Abel inversion.

Let
\[
a_b:C^{(g)}\longrightarrow J,\qquad D\longmapsto[D-gb],
\]
and let \(\rho_b\) be the rational map sending a class with unique representative to its chosen support-encoding coefficients.

Suppose \(\rho_b\) is represented by sections \(s_0,\ldots,s_r\) of an adelically metrized line bundle \(\overline{\mathcal L}\) on \(J\). Where these sections do not vanish simultaneously, the height identity gives
\[
h(\rho_b(t))
 =
h_{\overline{\mathcal L}}(t)
+\sum_v\frac{n_v}{[L:\mathbf Q]}
       \log\max_i\|s_i(t)\|_v.
\]
Therefore
\[
\boxed{
h(\rho_b(t))
\leq h_{\overline{\mathcal L}}(t)
+\sum_v\frac{n_v}{[L:\mathbf Q]}
       \log^+\max_i\|s_i\|_{v,\sup}.
}                                                        \tag{9}
\]

This is an actual upper-bound mechanism. It does **not** need a lower bound on an individual inverse denominator: the global projective height accounts for denominators.

To close the assigned problem, one must establish, with universal polynomial dependence:

1. a suitable section representation of \(\rho_b\);
2. its line-bundle height at torsion, including all translation costs from \(b\);
3. its archimedean sup-norm budget;
4. its finite-place denominator and vertical-model budget;
5. a polynomial-size representation or certificate, without materializing an exponential Jacobian embedding.

The resulting right-hand side must be bounded by a polynomial in
\[
\ell,d,D,g,B,h(b),\text{field-presentation bits},
\]
with the admitted Green and stable Faltings bounds substituted explicitly.

The Green assumption can contribute to item 3, and stable Faltings height can contribute to metric normalizations. Neither supplied assumption establishes all five items. Uniqueness establishes that the inverse is defined at \(t\); it does not bound the adelic section budget in (9).

Model height must remain present. For example,
\[
E_N:\ y^2=N^2(x^3+1)
\]
is isomorphic over \(\mathbf Q\) to \(y^2=x^3+1\), so its stable Faltings height is unchanged. The point \((0,N)\) has order three, but its \(y\)-coordinate height is \(\log N\). The model height charges this correctly. Stable Faltings height and complex geometry alone cannot replace that charge.

---

## Audit disposition

**Proved here:**

- uniqueness alone cannot justify an uncharged basepoint;
- the constant-curve counterfamily explicitly falsifies that inference;
- good basepoints exist outside at most \(\ell^m g^3\) geometric points;
- closed-divisor descent gives individual support-degree bounds without splitting;
- eliminant heights, point-coordinate heights, and coefficient bit costs are related by explicit inequalities.

**Not proved:** the polynomial adelic section budget in (9) for growing genus after choosing and charging a small basepoint.

A counterfamily to that **corrected** theorem would have to keep the basepoint, model, coordinate map, and actual field-presentation charges controlled while forcing superpolynomial representative height. The elliptic family above does not do that once \(h(b)\) is included. Conversely, failed searches or finite examples would not establish the corrected theorem.

Accordingly, the source’s height argument cannot be promoted to native polynomial-time closure. The remaining obligation is precisely the uniform arithmetic inverse-Abel/support-encoding estimate, not canonical-height vanishing itself.