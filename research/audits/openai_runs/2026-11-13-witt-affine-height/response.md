## Result and scope

**The fixed-rank height compiler closes, conditional on the norm and C1/C2 interfaces stipulated in the question.** The essential additional ingredient is a local binary-value construction with a **bounded valuation**, followed by CRT reduction modulo \(\gamma O_K\). Merely knowing that the local representatives have polynomial expanded size is not enough.

A deliberately generous bound obtainable below is
\[
\boxed{
H_{\rm out}\le 2^{512}H_{\rm in}
       +2^{520}(B_{\rm fld}+1)^4 ,
}
\]
where \(B_{\rm fld}\) is the bit length of the original, compatible expanded field data. The output contains the full expanded basis, not merely an abstract anisotropic form.

This is a conditional compiler theorem, not an independent certification of the scalar norm backend. In particular, the packet does not reproduce that backend’s precise GRH statement. I use its stipulated uniform quantum-bit contract, including input preparation and output costs; I introduce no additional GRH assumption.

I do not construct or analyze the growing-rank balanced tree.

---

## 1. First attempt at a falsifier: rational denominator clearing really fails

There is an exact obstruction to one tempting normalization, although not to the requested rational-coordinate output.

Let \(N\) be even, let \(p\ge3\) be prime, and let
\[
f(T)=T^N+T+p,\qquad K=\mathbf Q(\alpha),\quad f(\alpha)=0.
\]
This gives a totally imaginary field of degree \(N\):

* \(f\) has no real zero: for \(t\ge0\), \(t^N-t+p>0\).
* Every complex root has modulus \(>1\), since \(|z^N+z|\le2<p\) when \(|z|\le1\).
* The monic polynomial is irreducible. Otherwise one integral factor would have constant term \(\pm1\), contradicting that all its roots have modulus \(>1\).

Consequently,
\[
H_K(\alpha)=\log p.
\]
The principal ideal \((\alpha)\) has norm \(p\), hence is a prime \(\mathfrak p\). Moreover
\[
p=-\alpha(\alpha^{N-1}+1)
\]
shows \(v_{\mathfrak p}(p)=1\). Thus the least positive rational integer clearing the denominators of \(\alpha^{-k}\) is \(p^k\).

The tuple \((\alpha^{-k},1)\) has height \(k\log p\), while rational-integer clearing produces a tuple containing \(p^k\), whose height is
\[
H_K(p^k)=Nk\log p.
\]
For fixed \(K\), letting \(k\to\infty\) prevents an additive field term from repairing this factor \(N\).

**Conclusion:** a compiler that propagates rational-integer-cleared witnesses can fail the required slope. This is not an impossibility result for rational Witt reduction: multiplying the same projective tuple by \(\alpha^k\), for example, gives \((1,\alpha^k)\) without the loss.

The construction below never performs that dangerous normalization on an output witness or basis.

---

## 2. Exact hypotheses and accounting convention

Write \(r\le8\), and use
\[
H_K(x)=N h(x),\qquad H_K(0)=0,
\]
summed over matrix or vector entries. Canonical hyperbolic planes will have Gram matrix
\[
J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

The required computational interfaces are:

1. **Expanded arithmetic.** Uniform polynomial-bit field and ideal arithmetic, compatible quadratic-extension construction, number-field polynomial factoring, and maximal-order construction from a charged order and the full discriminant radical. Integer and finite-field factoring are charged.
2. **Complete quadratic norm backend.** For every expanded quadratic extension \(M/F\) encountered here, it decides relative norm solubility and, on a positive instance, supplies the stipulated power-product output. The given residue postprocessor produces a first expanded fractional norm witness in polynomial bit time. This interface must apply to the totally imaginary auxiliary bases used below, not only to totally real fields or supplied towers.
3. **Given-witness conic shortening.** For an expanded nonsingular diagonal conic over an expanded field \(F\), an expanded nonzero witness can be replaced by one satisfying the stated bound
   \[
   H_F(x)+H_F(y)+H_F(z)
   \le64\bigl(H_F(A)+H_F(B)+H_F(C)
                +\log|\Delta_F|+[F:\mathbf Q]^2\bigr).
   \]
   Its output bound is independent of the incoming witness height. Its runtime still charges that witness.

The supplied shortening proof uses the tower only for root extraction. Replacing that step by the stipulated uniform factoring interface permits its application with an expanded auxiliary field as its base. This does **not** discard its maximal-order, metric-precision, or LLL obligations.

For field-only terms define
\[
F_K=1+\log|\Delta_K|+4N^2+\sum_{i=1}^N H_K(\omega_i),
\]
where \(\omega_i\) is the original integral basis.

This is polynomially bounded by the charged field encoding. Elementary root bounds for the defining polynomial, followed by bounds on the embedding matrix of the supplied basis, give, generously,
\[
F_K\le256(B_{\rm fld}+1)^4.                         \tag{1}
\]

The height inequalities used throughout are
\[
\begin{aligned}
H(xy)&\le H(x)+H(y),\\
H(x+y)&\le H(x)+H(y)+N\log2,\\
H(x^{-1})&=H(x),\\
\sum_{\mathfrak p}|v_{\mathfrak p}(x)|\log N\mathfrak p
&\le2H_K(x).
\end{aligned}                                                   \tag{2}
\]
For \(x\in K\subset E\), \(H_E(x)=[E:K]H_K(x)\).

---

## 3. Short-\(\gamma\) CRT reduction: the absolute-slope lemma

### Lemma

For an integral ideal \(I\subset O_K\), an expanded integral representative \(a\) can be replaced, in polynomial bit time, by \(a'\equiv a\pmod I\) satisfying
\[
\boxed{H_K(a')\le \log N(I)+F_K.}                    \tag{3}
\]
The bound is independent of the height of \(a\).

### Construction and proof

Use LLL in the scaled Minkowski metric to find \(0\ne\gamma\in I\) with
\[
\max_\sigma|\sigma(\gamma)|
 \le
 \Gamma:=3\,2^{N/2}|\Delta_K|^{1/(2N)}N(I)^{1/N}.     \tag{4}
\]
The slack accommodates a certified rational approximation to the metric. This is an ideal-lattice calculation, not a principalization of \(I\).

Write, exactly,
\[
a/\gamma=\sum_i c_i\omega_i,\qquad c_i\in\mathbf Q,
\]
choose nearest integers \(n_i\), and set
\[
a'=a-\gamma\sum_i n_i\omega_i.
\]
Then
\[
a'-a\in\gamma O_K\subset I,
\]
and
\[
|\sigma(a')|
 \le \tfrac12|\sigma(\gamma)|\sum_i|\sigma(\omega_i)|.
\]
Because \(a'\) is integral, it has no finite height contribution. Also
\[
\sum_\sigma\log\max\!\left(1,\sum_i|\sigma(\omega_i)|\right)
\le N\log N+\sum_iH_K(\omega_i).
\]
Combining this with (4) proves (3).

### Paid implementation

The initial HNF representative may have a poor intrinsic-height bound; it is temporary. The final reduction uses exact rational coordinates of \(a/\gamma\), not an archimedean closest-vector oracle.

For the LLL metric, the ideal embedding determinant is
\[
\sqrt{|\Delta_K|}\,N(I)
\]
in the scaled convention. Upper bounds on embedding entries and this determinant give an inverse-conditioning bound of \(\exp(\operatorname{poly}(\text{input bits}))\). Certified root refinement and rational-Gram LLL therefore require polynomial precision. This is the same kind of paid metric calculation used by C1, not free exact-real arithmetic.

The crucial point is the coefficient \(1\) on \(\log N(I)\). Coordinate HNF reduction alone would not prove it.

---

## 4. A bounded-valuation local binary chooser

This is the missing normalization needed before applying the preceding CRT lemma.

### Local lemma

Let \(\mathfrak p\) be a finite prime, and let \(a,b,d\in K^\times\). Put
\[
e=v_{\mathfrak p}(2),\qquad
\alpha=v_{\mathfrak p}(a),\quad
\beta=v_{\mathfrak p}(b),\quad
m=\max(\alpha,\beta).
\]
One can construct polynomial-bit expanded \(s_0,t_0\in K\), integral at \(\mathfrak p\), such that
\[
c_0=a s_0^2+b t_0^2\notin dK_{\mathfrak p}^{\times2},
\]
and
\[
\boxed{v_{\mathfrak p}(c_0)=m+2e+\nu,\qquad \nu\in\{0,1\}.}       \tag{5}
\]

It follows that it suffices to preserve \(s_0,t_0\) modulo
\[
\boxed{M_{\mathfrak p}=|\alpha-\beta|+4e+2.}          \tag{6}
\]

### 4.1 Local normalization without principal-generator advice

Choose a global integral element
\[
\pi\in\mathfrak p\setminus\mathfrak p^2.
\]
An ideal basis contains such an element; ideal membership finds one. It is not required to generate \(\mathfrak p\).

Set
\[
k_a=\left\lceil\frac{m-\alpha}{2}\right\rceil,\qquad
k_b=\left\lceil\frac{m-\beta}{2}\right\rceil,
\]
and
\[
a_0=a\pi^{\,2k_a-m},\qquad b_0=b\pi^{\,2k_b-m}.
\]
Both normalized valuations lie in \(\{0,1\}\), and at least one is zero. Interchange the two coordinates locally if necessary so that \(a_0\) is a unit. Put
\[
\delta=-b_0/a_0,\qquad v_{\mathfrak p}(\delta)\in\{0,1\}.
\]

If \(\pi^m a_0/d\) is already locally nonsquare, use the norm value \(1\). Otherwise find a locally nonsquare norm value
\[
n=r^2-\delta w^2
\]
with \(v_{\mathfrak p}(n)\in\{0,1\}\).

### 4.2 Finding that norm value with polynomially many tests

Here are explicit finite constructions.

* **\(\delta\) globally square.** For an expanded root \(\rho^2=\delta\), use
  \[
  r=(\pi+1)/2,\qquad w=(\pi-1)/(2\rho).
  \]
  Its norm is \(\pi\).

* **Globally nonsquare, locally split.** In \(L=K(\sqrt\delta)\), choose an integral \(z\) satisfying
  \[
  z\equiv\pi_1\pmod{\mathfrak P_1^2},\qquad
  z\equiv1\pmod{\mathfrak P_2},
  \]
  where \(\pi_1\in\mathfrak P_1\setminus\mathfrak P_1^2\).
  Its norm has valuation \(1\).

* **Locally ramified.** Choose an integral
  \(z\in\mathfrak P\setminus\mathfrak P^2\). Its norm again has valuation \(1\).

* **Unramified quadratic, odd residue characteristic.** Lift a nonsquare residue unit in the quadratic residue field. Its norm is a nonsquare residue unit.

* **Unramified quadratic, dyadic.** Use the unit list
  \[
  1+b_j\pi_L^i,\qquad 1\le i\le2e_L,
  \]
  where the \(b_j\) lift an \(\mathbf F_2\)-basis of the residue field. This list has at most \(4N\) elements. It generates the unit squareclasses: the successive unit quotients are additive residue fields, residue units have odd order, and \(U_{2e_L+1}\) consists of squares. Unramified unit norms are surjective, so some listed unit has nonsquare norm. Test the list; do not enumerate squareclasses.

A local square test is paid by global root factoring or by constructing the expanded quadratic field and decomposing \(\mathfrak p\). No local square root is supplied.

For the nonsquare-global cases, write the integral \(z\) as
\[
z=r+w\sqrt\delta.
\]
Trace and conjugation give
\[
v_{\mathfrak p}(r)\ge-e,\qquad
v_{\mathfrak p}(w)\ge-e.                              \tag{7}
\]
For the second inequality, division by \(\sqrt\delta\) loses at most \(1/2\) in the normalized base valuation; \(w\in K_{\mathfrak p}\) has integral valuation, so rounding restores the stated bound.

Now take, with the local swap undone,
\[
s_0=\pi^{k_a+e}r,\qquad t_0=\pi^{k_b+e}w.
\]
They are integral at \(\mathfrak p\), and
\[
a s_0^2+b t_0^2
 =\pi^{m+2e}a_0n.
\]
This proves (5), including its squareclass assertion.

### 4.3 Why the precision in (6) suffices

If \(s,t\) approximate \(s_0,t_0\) to valuation at least \(M_{\mathfrak p}\), all four coordinates are locally integral, and
\[
v_{\mathfrak p}(c-c_0)
\ge\min(\alpha,\beta)+M_{\mathfrak p}
=m+4e+2.
\]
By (5),
\[
m+4e+2>v_{\mathfrak p}(c_0)+2e.
\]
Thus \(c/c_0\) is a local square unit by Hensel’s criterion. In particular \(c\ne0\), and the forbidden squareclass remains avoided.

### 4.4 Fractional representatives do not require a global integer denominator

Although \(s_0,t_0\) are integral at \(\mathfrak p\), they can be fractional elsewhere.

For a locally integral \(x\), compute its denominator ideal
\[
\mathfrak D(x)=\{u\in O_K:ux\in O_K\}.
\]
It has \(\mathfrak p\)-valuation zero. Choose an ideal-basis element \(u\notin\mathfrak p\), and reduce
\[
(ux)\,u^{-1}\pmod{\mathfrak p^{M_{\mathfrak p}}}.
\]
The inverse and reduction are finite ideal-ring/HNF calculations.

This avoids the degree loss exhibited in §1. Temporary local representatives and their auxiliary fields need only have polynomial bit size; their potentially poor global heights are discarded before the final CRT output.

---

## 5. Quaternary descent with an absolute height slope

Consider
\[
q_4=\langle a,b,c,e\rangle,\qquad
A_4=H_K(a)+H_K(b)+H_K(c)+H_K(e).
\]
Put
\[
D=abce,\qquad u=-b/a,\qquad v=-c/a,\qquad g=bc.
\]
If \(D\) is nonsquare, construct \(E=K(t)\), \(t^2=D\); otherwise take \(E=K\).

### 5.1 Auxiliary discriminants that enter the output bound

Using the fractional square-part ideal of \((D)\), the order construction in the supplied shortening argument gives
\[
\log|\Delta_E|
 \le2\log|\Delta_K|+2N\log2+2H_K(D)
 \le2\log|\Delta_K|+2N\log2+2A_4.                    \tag{8}
\]
This uses an actual order and its full discriminant radical. It does not use a monogenic discriminant as a substitute, nor principalize the square-part ideal.

The quadratic norm field \(E(\sqrt u)\) satisfies the analogous bound over \(E\). All front-end degrees are at most \(4N\).

Compatible expanded fields and coordinate maps are computed. For example, a primitive element can be found among \(\theta+j t\) for polynomially many small integers \(j\), using exact degree tests. No large primitive generator is supplied as advice.

### 5.2 A short exact norm solution over \(E\)

Solve
\[
X^2-uY^2=v.                                        \tag{9}
\]
If \(u\) is square in \(E\), an expanded root \(\rho\) gives
\[
X=(v+1)/2,\qquad Y=(v-1)/(2\rho).
\]
Otherwise, call the norm backend on the expanded quadratic extension, expand its first witness using the stipulated residue postprocessor, and apply conic shortening to
\[
x^2-u y^2-v z^2=0.
\]
Since \(u\) is nonsquare, \(z\ne0\); put \(X=x/z,\ Y=y/z\).

Writing
\[
S_4=A_4+\log|\Delta_K|+N^2,
\]
the shortening contract and (8) give
\[
H_E(X)+H_E(Y)\le768S_4.                             \tag{10}
\]
This is independent of the first norm witness’s height.

Norm solubility is the correct decision criterion here. Indeed, with \(h=t/g\),
\[
q_4/a=x_1^2-u x_2^2-v x_3^2+uvh^2x_4^2.
\]
When \(u\) is nonsquare in \(E\), a nonzero isotropic point gives
\[
N(x_1+x_2\sqrt u)
   =v\,N(x_3+h x_4\sqrt u).
\]
The denominator norm cannot vanish, so \(v\) is a norm. The converse is the explicit descent next.

### 5.3 Explicit descent—valid for every solution of (9)

If \(D\) is square, \((-X,-Y,1,0)\) is already a \(K\)-point.

Otherwise write
\[
X=X_0+tX_1,\qquad Y=Y_0+tY_1.
\]
The coefficient of \(t\) in (9) gives
\[
X_0X_1=uY_0Y_1.                                    \tag{11}
\]

If \((X_1,Y_0)\ne(0,0)\), return
\[
\boxed{
\begin{aligned}
w_1&=u(DX_1Y_1-X_0Y_0),\\
w_2&=DX_1^2-uY_0^2,\\
w_3&=uY_0,\\
w_4&=-gX_1.
\end{aligned}}                                                   \tag{12}
\]
Otherwise return
\[
\boxed{
w=(-X_0^2+DuY_1^2,\ 0,\ X_0,\ -gY_1).
}                                                               \tag{13}
\]
Each vector is nonzero by its branch condition and (9).

For verification, these choices satisfy
\[
w_1+Xw_3+h\,uYw_4=0,\qquad
w_2+Yw_3+h\,Xw_4=0.
\]
Expanding these two identities using (9) proves \(q_4(w)=0\). Thus there is no special splitting, ruling, or Hilbert–90 advice hidden in the descent.

### 5.4 Height of the descent maps

The components are computed exactly through
\[
X_0=(X+\sigma X)/2,\qquad X_1=(X-\sigma X)/(2t),
\]
and similarly for \(Y\). Conjugacy invariance of height gives
\[
H_K(X_0)+H_K(X_1)+H_K(Y_0)+H_K(Y_1)
\le2\bigl(H_E(X)+H_E(Y)\bigr)+H_K(D)+8N\log2
\le2^{11}S_4.
\]
Applying (2) to (12)–(13) yields
\[
\boxed{H_K(w)\le2^{14}S_4.}                         \tag{14}
\]

The exact expanded basis conversions can have polynomial degree factors in their bit costs. They do not change this intrinsic-height calculation.

The ternary case is simpler: solve its quadratic norm equation, then apply the same conic shortening directly. Binary isotropy is a square test. All these cases fit within (14), with the appropriate coefficient tuple.

---

## 6. Five-to-four gluing with an affine slope

Let
\[
q_5=\langle a_1,a_2,a_3,a_4,a_5\rangle,\qquad
A_5=\sum_{i=1}^5H_K(a_i).
\]
Let \(S\) contain all dyadic primes and all numerator/denominator prime supports of \(a_1,a_2,a_3\). Then
\[
\sum_{\mathfrak p\in S}\log N\mathfrak p
 \le N\log2+2\sum_{i=1}^3H_K(a_i).                  \tag{15}
\]

At each \(\mathfrak p\in S\), apply §4 with
\[
a=a_4,\quad b=a_5,\quad d=a_1a_2a_3.
\]
Use exactly the precision
\[
M_{\mathfrak p}
 =|v_{\mathfrak p}(a_4)-v_{\mathfrak p}(a_5)|
      +4v_{\mathfrak p}(2)+2,
\]
and set
\[
I=\prod_{\mathfrak p\in S}\mathfrak p^{M_{\mathfrak p}}.
\]

The modulus mass is affine:
\[
\begin{aligned}
\log N(I)
&\le
 2H_K(a_4)+2H_K(a_5)
 +4N\log2
 +2\sum_{\mathfrak p\in S}\log N\mathfrak p\\
&\le \boxed{4A_5+6N\log2}.                         \tag{16}
\end{aligned}
\]

Construct integral CRT representatives for both coordinates, then apply the **same** short-\(\gamma\) reduction of §3 to each. Its congruences are preserved because \(\gamma O_K\subset I\). The resulting integral \(s,t\) satisfy
\[
\boxed{H_K(s)+H_K(t)\le8A_5+5F_K.}                  \tag{17}
\]

Set
\[
c=a_4s^2+a_5t^2.
\]
The local lemma ensures \(c\ne0\) and
\[
c\notin \det(\langle a_1,a_2,a_3\rangle)
                    K_{\mathfrak p}^{\times2}
\quad(\mathfrak p\in S).
\]

At a finite place where the ternary is anisotropic, this is precisely the excluded-class condition making
\[
\langle a_1,a_2,a_3,c\rangle
\]
isotropic. Outside \(S\), the odd-residue unimodular ternary is already isotropic. Complex places impose no restriction. Hasse–Minkowski therefore makes this quaternary globally isotropic.

Its coefficient height satisfies
\[
\boxed{
H_K(a_1)+H_K(a_2)+H_K(a_3)+H_K(c)
 \le17A_5+16F_K.
}                                                               \tag{18}
\]
This is where using bounded local valuations, rather than polynomial-height local representatives, matters.

Apply §5 to obtain \(w\), and lift it to
\[
(w_1,w_2,w_3,sw_4,tw_4).
\]
Equations (14), (17), and (18) give the convenient uniform bound
\[
\boxed{
H_K(\text{five-variable point})
 \le2^{20}(A_5+F_K).
}                                                               \tag{19}
\]

For a diagonal form of rank \(5,\ldots,8\), use its first five coordinates and pad the point with zeros. Thus every positive fixed-rank isotropy call has the bound (19).

---

## 7. Full embedded Witt reduction

It remains to pay diagonalization, hyperbolic normalization, orthogonal complements, and accumulated basis maps.

### 7.1 Constant-rank diagonalization with an explicit height bound

For matrices of dimensions at most eight,
\[
H(AB)\le8H(A)+8H(B)+64N\log8.                       \tag{20}
\]
For a minor \(M\) of order at most eight,
\[
H(\det M)\le H(M)+N\log(8!).                         \tag{21}
\]
The latter follows by bounding every determinant term by the product of the local maxima of all entries; no degree-\(N\) determinant bound is being propagated.

One convenient fully constructive diagonalization is:

1. Choose successive integer columns from \(\{0,1,2\}^r\) so that each leading restricted Gram determinant is nonzero.
2. Apply Gram–Schmidt using Cramer minors.

The next determinant is a nonzero quadratic polynomial in the candidate column, so it cannot vanish on the entire grid \(\{0,1,2\}^r\). This is a proved finite search of constant size because \(r\le8\), not an empirical control.

The resulting integer matrix \(S\) has
\[
H(S)\le64N\log2.
\]
Equations (20)–(21), with at most 28 Gram–Schmidt coefficients, give a diagonalizing matrix \(T\) and diagonal \(D=T^TQT\) with
\[
\boxed{H(T)+H(D)\le2^{24}(H(Q)+F_K).}               \tag{22}
\]
For example, the direct calculation bounds this by
\(29696H(Q)+2{,}945{,}712N\), already below the displayed allowance.

### 7.2 Canonical hyperbolic plane and embedded complement

Given an expanded isotropic \(v\ne0\), choose a coordinate vector \(e_j\) with
\[
\beta=v^TQe_j\ne0.
\]
Put
\[
e=v,\qquad u=e_j/\beta,\qquad
f=u-\frac{q(u)}2e.
\]
Then
\[
q(e)=q(f)=0,\qquad e^TQf=1.
\]

Project each coordinate vector into the orthogonal complement:
\[
z_k=e_k-(e_k^TQf)e-(e_k^TQe)f.
\]
Select \(r-2\) independent projected vectors by exact rank tests. If
\[
A=[e,f,Z],
\]
then
\[
A^TQA=J\perp Q_\perp.
\]
All entries are expanded rational \(K\)-coordinates; no common integer denominator is imposed.

Applying (2) and (20) to these displayed formulas gives, generously,
\[
\boxed{
H(A)+H(Q_\perp)
 \le2^{24}\bigl(H(Q)+H(v)+F_K\bigr).
}                                                               \tag{23}
\]
The coordinate projections themselves admit a substantially smaller constant; (23) leaves ample slack.

### 7.3 Accumulated basis

Maintain a full matrix \(W\), initially the identity. Every diagonalizing or hyperbolic-splitting change is embedded into the active block and multiplied into \(W\). Identity padding has zero height, and (20) pays every multiplication.

Using (19), (22), and (23), one complete positive iteration—diagonalize, find a point, split a plane, update \(W\)—increases
\[
H(W)+H(Q_{\rm active})+F_K
\]
by a factor at most \(2^{96}\). At most four planes can be split. Allowing one additional diagonalization for the terminating anisotropy decision costs at most \(2^{32}\). Hence
\[
H(W)+H(Q_{\rm an})
 \le2^{416}(H_{\rm in}+F_K).                         \tag{24}
\]

Ranks \(1\) and \(2\) use the direct decisions; ranks \(3\) and \(4\) use the complete norm decisions proved equivalent above. Rank at least five cannot be the terminating anisotropic rank. Thus \(Q_{\rm an}\) has rank at most four, and
\[
W^TQW=J^{\perp w}\perp Q_{\rm an}.
\]

Combining (1) and (24) proves the bound stated at the beginning with
\[
C=2^{512},\qquad
P(B_{\rm fld})=2^{520}(B_{\rm fld}+1)^4.
\]
These constants are intentionally very loose, but neither contains \(N\).

---

## 8. Bit costs, preparation, precision, and output

Let \(B\) be the full native expanded input length.

* **Input access:** all field tables, compatible conversions, and coefficient coordinates are read and charged. No class group, unit basis, principal generator, local root, or starting isotropic vector is advice.
* **Local work:** the support has polynomial size. All valuation exponents used above have polynomial numerical size in \(B\). The dyadic generator lists have \(O(N)\) entries. Odd-characteristic nonsquare selection uses bounded, certified sampling, not residue enumeration.
* **Temporary local fields:** their defining elements can have merely polynomial—not affine—height. Their expanded maximal orders, discriminants, and coordinate maps have polynomial bit size. They are discarded after residue extraction; their heights do not enter (16)–(19).
* **Fields affecting output height:** the q4 fields have degree at most \(4N\), and their discriminants satisfy the affine bounds in §5. A fresh call starts over the original \(K\); auxiliary fields are not accumulated into a growing tower.
* **First norm witnesses:** every norm-backend input is expanded. The residue postprocessor gives a polynomial-bit expanded witness before shortening. Reading and processing that witness is charged. Only the shortened witness enters the affine output estimate.
* **Precision:** Minkowski metrics use certified polynomial-bit approximations with explicit conditioning bounds. Root factoring is exact over the charged expanded base field. No infinitesimal comparisons or exact-real operations are free.
* **Quantum preparation and readout:** the stipulated norm/factoring clocks must include preparation from their explicit polynomial-bit inputs and classical output extraction. There is no QRAM assumption or coherent input oracle.
* **Output:** for an element expressed in the original integral basis, the supplied trace-dual/cofactor argument gives a maximum coordinate bit bound
  \[
  \ell_K(x)\le 2H_K(x)/\log2+\kappa_K+O(1),
  \]
  with \(\kappa_K\) polynomial in the original field encoding. The extra factor \(N\) in total expanded encoding length is an output/runtime cost, not a propagated height slope.

Assign separate bounded failure budgets to the polynomially many factoring and local-selection operations and to the at most four global norm calls. The total clock is polynomial in \(B\) and \(\log(1/\eta)\), under the stipulated backend contract.

---

## 9. Audit boundary and exact falsifiers

The new mathematical deductions are the bounded-valuation local lemma, the short-\(\gamma\) CRT height bound, the explicit q4 descent, and their fixed-rank basis composition. They do not follow from an “ACCEPT” label.

The decisive obligations are:

1. **Conic shortening must retain its intrinsic bound** involving \(\log|\Delta_F|+[F:\mathbf Q]^2\), not a coefficient-dependent polynomial in an auxiliary basis encoding.
2. **The local construction must satisfy (5) and (7).** Losing those bounds invalidates the modulus mass (16), even if all local objects remain polynomial-bit.
3. **The short vector must be short in the Minkowski metric.** Ordinary coefficient-lattice LLL does not establish (4).
4. **Residue extraction must not introduce a global rational-integer normalization.** Section 1 is an exact falsifier of that replacement.
5. **The norm interface must really be uniform and complete**, with expanded input, paid preparation/readout, and the stipulated polynomial-size first-witness contract.

Exact checks of the returned norm identities, local squareclasses, \(q(v)=0\), \(\det W\ne0\), and the final Gram identity are useful finite controls. They do not independently prove the height or bit-complexity theorem.

**Relative to the stipulated arithmetic interfaces, there is no remaining unpaid q4 or q5 height operation in this construction.** Independent source certification of the norm backend’s precise GRH and quantum-bit contract remains outside what the supplied text establishes. No classical hardness, quantum separation, or practical-performance conclusion follows.