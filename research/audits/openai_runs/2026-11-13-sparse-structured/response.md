## Verdict

I cannot close the proposed all-input sparse-bit LC algorithm from the supplied results. Nor can I prove that such an algorithm is impossible.

I can isolate the unpaid step more sharply: **leading coefficients of native companion-matrix norms already encode arbitrary sparse Sylvester-resultant leading coefficients**, even for monic irreducible native inputs whose **original, nonconstant atoms have nontrivial Alg and nontrivial Rel**. This is not the old Alg \(=0\) family, nor a generic-matrix substitution.

The construction below also supplies an exact growing-degree cancellation test. Its coefficient heights are polynomially bounded in bits; locating the surviving coefficient—not its eventual size—is the unsupported operation.

## 1. Native structured-resultant lift

Let
\[
p(T,Y),q(T,Y)\in\mathbb Z[T,Y],
\]
where \(p\) is monic of \(Y\)-degree \(d\ge2\), \(q\ne0\) has \(Y\)-degree \(m<d\), and
\[
R(T)=\operatorname{Res}_Y(p,q)\ne0.
\]
Both polynomials are explicitly sparse, with binary \(T\)-exponents. Let \(\beta\ge1\) bound their \(T\)-degrees, and put
\[
D=(d+m)\beta,\qquad H=d(D+1)+1.
\]
Thus \(H>D\), \(\gcd(H,d)=1\), and \(\log H\) is polynomially bounded in the input length.

Define
\[
\widehat q=q+T^{-H},
\qquad
f=p^3-p\widehat q^{\,2}-\widehat q^{\,3}.
\]
The negative exponent is represented natively as
\[
\widehat q=\frac{T^Hq+1}{T^H};
\]
no Laurent-polynomial input extension is needed.

In
\[
F=\mathbb Q(T)[y]/f,
\]
supply the following **original atoms**:
\[
u=p(T,y),\qquad
v=\widehat q(T,y),\qquad
w=p(T,y)^2-\widehat q(T,y)^2.
\tag{1}
\]

### Theorem

This construction has all the following properties.

1. \(f\) is monic irreducible of charged degree \(\delta=3d\).
2. All three atoms in (1) are nonzero and nonconstant, and are explicit in the original \(Y\)-basis.
3. Their lattices are exactly
   \[
   \operatorname{Alg}
   =\{(a,b,z)\in\mathbb Z^3:a+b+2z=0\},
   \tag{2}
   \]
   \[
   \operatorname{Rel}
   =\mathbb Z(1,-3,1).
   \tag{3}
   \]
4. Writing
   \[
   R_H(T)=\operatorname{Res}_Y(p,\widehat q),
   \]
   their native field norms are
   \[
   N(u)=N(v)=R_H^3,\qquad N(w)=R_H^6.
   \tag{4}
   \]
5. At \(T=\infty\),
   \[
   \deg R_H=\deg R,\qquad \operatorname{lc}(R_H)=\operatorname{lc}(R).
   \tag{5}
   \]

Consequently, a polynomial sparse-bit operation computing
\[
\operatorname{lc}_\infty N_{F/\mathbb Q(T)}(v)
\]
on these native inputs would compute \(\operatorname{lc}R\) for arbitrary \(p,q\) above, by an exact signed integer cube root. If it also returns the degree, division by \(3\) recovers \(\deg R\).

This is a reduction for the proposed **norm-leading-coefficient step**. It is not a claim that every possible single-place LC algorithm must compute a norm.

### Proof: irreducibility and genuine constants

Let \(c\) be the real root greater than \(1\) of
\[
h(X)=X^3-X-1,
\]
and \(K=\mathbb Q(c)\). The cubic is irreducible by the rational-root test. Moreover,
\[
N_{K/\mathbb Q}(c)=1,\qquad c^{-1}=c^2-1,
\]
and \(c\) is not a root of unity.

Over \(K(T)\), consider
\[
g=p-c\widehat q.
\]
For the \(T\)-adic valuation normalized by \(\nu(T)=1\), its constant coefficient has valuation \(-H\), its other nonleading coefficients have valuation at least \(0\), and its leading coefficient is \(1\).

Every root of \(g\) therefore has valuation \(-H/d\): any other valuation would leave a unique term of least valuation in the defining equation. If \(g\) had a monic factor of degree \(r\), its constant coefficient would have valuation \(-Hr/d\), an integer. Since \(\gcd(H,d)=1\), necessarily \(d\mid r\). Thus \(g\) is irreducible.

For a root \(y\) of \(g\), \(\widehat q(y)\ne0\), because its \(Y\)-degree is less than \(d\). Hence
\[
c=\frac{p(y)}{\widehat q(y)}\in\mathbb Q(T)(y).
\]
It follows that \([\mathbb Q(T)(y):\mathbb Q(T)]=3d\), proving irreducibility of the displayed monic \(f\).

Inside \(F\),
\[
u=cv,\qquad w=c^{-1}v^2.
\tag{6}
\]
Also \(\nu(v)=-H\): all terms of \(q(T,y)\) have valuation strictly greater than \(-H\). Thus
\[
u^a v^b w^z=c^{a-z}v^{a+b+2z}.
\]
Algebraic constants have valuation zero, so this product is algebraic precisely when \(a+b+2z=0\). It equals \(1\) precisely when also \(a=z\), since \(c\) is non-torsion. This proves (2)–(3).

In particular, the constant obstruction is intrinsic to the same nonconstant atoms:
\[
u/v=c\ne1,\qquad uw/v^3=1.
\]
No independent constant atom was appended.

### Proof: the structured norm identity

Resultant invariance under subtracting a multiple of the second polynomial gives
\[
N_{F/K(T)}(v)
=\operatorname{Res}_Y(p-c\widehat q,\widehat q)
=\operatorname{Res}_Y(p,\widehat q)
=R_H.
\]
Since \(R_H\in\mathbb Q(T)\), the absolute norm is \(R_H^3\). Equation (6) and \(N_{K/\mathbb Q}(c)=1\) give the other identities in (4).

Now write
\[
\operatorname{Res}_Y(p,q+Z)=\sum_{j=0}^{d}r_j(T)Z^j.
\]
Here \(r_0=R\), and every \(r_j\) has \(T\)-degree at most \(D\). Therefore
\[
R_H=R+\sum_{j\ge1}r_j(T)T^{-jH}.
\]
Every added term has degree at most \(D-H<0\), whereas the nonzero polynomial \(R\) has degree at least zero. This proves (5).

These are actual native structured matrices: \(N(v)\) has the \(3d\)-dimensional companion presentation, or the Sylvester presentation for \(f,\widehat q\), of size \(3d+m<4d\).

## 2. Heights, representation costs, and factoring

Let
\[
A=1+\|p\|_1+\|q\|_1,
\]
and let \(S\) count their supplied monomials, plus one.

Set \(P=T^Hp\), \(Q=T^Hq+1\). Clearing denominators gives
\[
T^{3H}f=P^3-PQ^2-Q^3.
\]
Consequently:

- constructing the native input uses at most \(O(S^3)\) monomials;
- its cleared numerator has coefficient \(\ell_1\)-norm at most \(A^3\);
- its \(T\)-degree is at most \(3(H+\beta)\);
- its coefficient bit heights are \(O(\log A)\);
- all exponents have \(O(\log H+\log\beta)\) bits.

The atoms require only constant-power sparse products; \(w\) has \(Y\)-degree \(2d<3d\). No inverse in the function field, Alg-basis power, or expanded high-degree specialization is constructed.

For the resultant, put \(n=d+m\) and
\[
C=n!\,A^n.
\]
The Sylvester determinant bound gives
\[
\left\|\operatorname{Res}_Y(p,q+Z)\right\|_1\le C.
\]
After substituting \(Z=T^{-H}\) and clearing a monomial denominator,
\[
\|T^{dH}R_H\|_1\le C.
\]
Thus a cleared numerator of \(N(v)=R_H^3\) has norm at most \(C^3\), and
\[
\log C=O(d\log d+d\log A).
\]

**The norm’s coefficients, including its leading coefficient, have polynomial bit height. Its expanded support need not have polynomial size.** A height bound therefore does not pay leading-coefficient extraction.

No factorization algorithm is used in this construction or proof. The only number field explicitly introduced is the fixed cubic \(K\). In a general proposed LC algorithm, factoring explicitly written residual polynomials of polynomial degree and height could be granted separately; that would not grant factorization or leading-coefficient extraction for huge-degree sparse \(T\)-polynomials or implicit resultants.

## 3. What the attempted algorithm has not paid

The supplied general-Alg algorithm remains closed and unchanged. If the proposed operation produced an explicit polynomial-size number field \(E\) and aligned values
\[
\alpha_i=\operatorname{LC}(u_i),
\]
with injective restriction to constants, then the supplied Lenstra–Silverberg Theorem 1.11 would give
\[
\operatorname{Rel}_F(u)
=\operatorname{Alg}\cap\operatorname{Rel}_E(\alpha_1,\ldots,\alpha_k).
\]
This uses the **original** images, not expanded powers of an Alg basis. The source requires the explicit finite \(\mathbb Q\)-algebra and explicit coordinates; a compact resultant circuit is not that input.

The unsupported step in the proposed norm/subresultant derivation is now precise:

> From a polynomial-size, specialized commutative Sylvester/companion presentation with binary weights, locate its first surviving weighted coefficient—and compute that coefficient—without expanding its support or advancing through numerical-degree precision.

The theorem above shows that native irreducibility and nontrivial Alg do not automatically simplify this step: its norm presentation contains arbitrary sparse resultants of charged \(Y\)-degree.

Moreover, norms do not finish the constants step even on this family. Since \(R_H\) is nonconstant, (4) implies that the relation lattice of the three norm images is **exactly Alg**, of rank \(2\). The true Rel has rank \(1\). Thus norm relations discard the required \(c\)-versus-\(1\) distinction completely.

The supplied Oki result does not fill this gap: its stated matrix expansion depends on the numerical maximum exponent, and Remark 12 explicitly distinguishes that clock from sparse-bit SDD. Conversely, Remark 12 is not a lower bound and does not exclude a randomized sparse-bit algorithm. Replacing specialized coefficient identities by independent noncommuting symbols would change the cancellation problem.

## 4. Exact growing-degree cancellation control

Here is a concrete specialization of the theorem, not an executed experiment.

Choose any \(d\ge2\) and binary \(M\ge2\), and set
\[
p=(Y-T^M)^d+T,\qquad q=Y-T^M.
\]
Expanding the \(Y\)-coefficients costs polynomially in \(d,\log M\): there are only \(d+2\) supplied terms and binomial coefficients of \(O(d)\) bits. Form \(H,f,u,v,w\) as above.

Directly,
\[
R=(-1)^dT,
\]
and
\[
R_H
=(-1)^d p(T,T^M-T^{-H})
=T^{-dH}+(-1)^dT.
\]
Hence the exact native norm is
\[
\boxed{
N(v)=\left(T^{-dH}+(-1)^dT\right)^3,
\quad
\deg_\infty N(v)=3,
\quad
\operatorname{lc}_\infty N(v)=(-1)^d.
}
\tag{7}
\]

The uncorrected leading-scale resultant has terms of degree \(3dM\); specialized commutative cancellation removes them down to degree \(3\). Clearing denominators merely adds a known degree shift.

For a genuine place at infinity, let \(\lambda\) be the leading coefficient of \(v\). Then
\[
\lambda^d=-1,
\]
and the aligned original LC tuple must have the form
\[
\boxed{
\bigl(c\lambda,\ \lambda,\ c^{-1}\lambda^2\bigr),
\qquad c^3-c-1=0.
}
\tag{8}
\]
For odd \(d\), the branch \(\lambda=-1\) gives the explicit valid output
\[
E=\mathbb Q(c),\qquad
\bigl(\operatorname{LC}(u),\operatorname{LC}(v),\operatorname{LC}(w)\bigr)
=(-c,-1,c^2-1).
\]
Other branches are permitted, but must retain the same joint identities. In every case,
\[
\operatorname{Alg}=\{a+b+2z=0\},
\qquad
\operatorname{Rel}=\mathbb Z(1,-3,1).
\]

This control’s cancellation is jumpable by the displayed substitution; its depth is **not** an impossibility proof. It decisively rejects a routine returning the generic weighted degree or identifying norm relations with full relations.

**Final theorem-level conclusion:** the proposed norm-cancellation route still owes polynomial sparse-bit leading-coefficient extraction for arbitrary sparse Sylvester resultants. That unpaid operation occurs inside explicit monic irreducible native instances with growing \(\delta\), polynomial-bit heights, and intrinsic rank-\(2\) Alg versus rank-\(1\) Rel. No general LC algorithm, impossibility result, or classical dequantization follows yet.