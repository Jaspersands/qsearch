## Verdict

**The full uniform RR/Stoll conditioning RESET remains unresolved.** I do not obtain either a native counterfamily against selectable representatives or the required whole-loop precision bound.

There is, however, a useful distinction:

- A **specific fraction-free RR evaluation block** admits an explicit, \(h\)-independent low-jet, tail, and finite-grid bound once its section lattice is supplied in primitive integral form.
- This does **not** yet bound the actual Stoll leading-coordinate augmented determinant, nor pay for obtaining and maintaining that primitive representation from the saturation data.

The latter gap is essential. Nonspecialness and bounded field-operation counts do not close it.

All calculations below are symbolic; no tools or additional sources are used.

## 1. Cheapest native test: divisible branch torsion in genus one

Consider
\[
f=x(x+1)(x+4)=x^3+5x^2+4x,\qquad v_2(\operatorname{disc}f)=4.
\]
Let
\[
T=(0,0),\qquad Q=(2,6).
\]
The identity
\[
f-9x^2=x(x-2)^2
\]
shows that \(2Q=T\). Thus \(T\) is an admissible initial saturation candidate: it is rational \(2\)-torsion with zero Kummer label, not an arbitrary advised \(2\)-adic point.

For \(g=1\), write \(n_s\ge2\), \(D_0=n_s\), and \(R=n_s+1\). Use exactly the supplied perturbation
\[
\sigma(z)=P(2^{n_s}+2^Rz)-P(2^{n_s}).
\]
Put
\[
h_z=T+2\sigma(z),\qquad q_z=Q+\sigma(z).
\]

For odd \(z\), the supplied logarithmic description gives
\[
v_2(\log\sigma(z))=R.
\]
If \(V=P(t)\) is sufficiently near infinity, addition by \(T\) gives
\[
x(T+V)=\frac4{x(V)},\qquad
y(T+V)=-\frac{4y(V)}{x(V)^2}.
\]
Since the infinity parameter of \(2\sigma(z)\) has valuation \(R+1\), writing \(h_z=(X,Y)\) gives
\[
v_2(Y)=R+3.
\]

Also, \(q_z=(\xi,\eta)\) remains integral with \(v_2(\eta)=1\). This follows directly from the addition formulas. With
\[
S(t)=\sqrt{1+5t^2+4t^4},
\]
they give, for \(v_2(t)\ge3\),
\[
x(Q+P(t))
=\frac{2-12S(t)t+28t^2+8t^4}{(1-2t^2)^2}
\in 2+8\mathbf Z_2,
\]
and
\[
y(Q+P(t))
=-6+12\frac{(S(t)-6t^3)(S(t)-3t)}{(1-2t^2)^3}
\in 6+8\mathbf Z_2.
\]

Now use the degree-one Stoll input \(a=x-X,\ b=Y\). For odd \(z\), it is squarefree and coprime to \(f\). Let
\[
s=s_0+s_1x+s_2x^2
\]
be the square root corresponding to the explicitly identified half \(q_z\). The tangent-line identity gives
\[
s_2=\frac1\eta.
\]

With columns \((u,v_0,v_1,w_0,w_1)\), appending the \(w_1\)-coordinate row to the four Stoll equations gives a matrix \(B_1\) with
\[
\det B_1=\pm Ys_2=\pm\frac{Y}{\eta}.
\]
Here all coefficients of \(s\) have valuation at least \(-1\). Multiplying the first three congruence rows by \(2\) therefore gives an integral augmented matrix \(\mathcal B_1\), and
\[
\boxed{v_2(\det\mathcal B_1)=R+5\quad\text{for every odd }z.}
\]

There is also a paid first jet. The \(d=1\) matrix family has an analytic extension at \(z=0\), although the actual gcd branch changes there. Its determinant satisfies
\[
v_2\!\left([z]\det\mathcal B_1(z)\right)=R+5.
\]
Indeed,
\[
Y'(0)=-\frac{2^{R+3}}{S(2^{n_s})},\qquad \eta(0)=6.
\]

Thus a finite integer grid containing equally many even and odd integers succeeds with probability at least \(1/2\). No Haar point source or sign enumeration is involved.

**Disposition:** this native branch-torsion example is not a counterexample to RESET. It shows explicitly why “the starting representative meets the branch locus” is insufficient as a falsifier. It is only a fixed-curve control, not an all-genus result.

## 2. The actual Stoll certificate that needs a bound

Retain every hypothesis of Proposition 5.1, including squarefree monic \(a\) and
\[
n=\deg a\le2g+1.
\]
Let \(e=\deg d\), where \(d=\gcd(a,f)\). With the full \(w\)-bound \(\deg w\le g\), the congruence matrix \(M_g\) has
\[
m=2g+1+n-e
\]
rows and \(m+1\) columns. Its blocks are the coefficient equations for
\[
dv-sw\bmod f_1,\qquad dv-bu\bmod a_1,\qquad f_1u-sw\bmod d.
\]

After explicitly charged denominator clearing, let \(\mathcal M_g\) be integral, and define
\[
\mathcal B_g=
\begin{pmatrix}
\mathcal M_g\\
\ell_g
\end{pmatrix},
\qquad
\ell_g(u,v,w)=w_g.
\]
This is square of size at most \(4g+3\).

A particularly economical reset target is therefore
\[
\Delta_h(z)=\det\mathcal B_g(h+2\sigma(z)).
\]

If
\[
0\le v_2(\Delta_h(z))\le K,
\]
then:

1. the bounded Stoll kernel is one-dimensional;
2. its minimum \(w\)-degree is \(g\);
3. both the relevant Smith losses and the leading-coordinate normalization loss are bounded by \(K\).

Thus the supplied precision ledger gives the sufficient **matrix-level** precision
\[
N_{\mathrm{matrix}}\ge M_{\mathrm{out}}+3K+1.
\]
Entry construction, roots, gcd/CRT operations, and conversion from the maintained point representation must be added separately.

This also avoids exact zero testing: reject a sample unless the determinant is visibly nonzero below the cap. A proof of sufficiently frequent acceptance is still required.

High-degree input \(a\) does not by itself supply that proof. In particular, it does not automatically remove the reduced-output leading-coordinate problem encoded by \(\mathcal B_g\).

## 3. A genuine RR evaluation-block reset

Here is an explicit positive result for an actual RR matrix, rather than for an unspecified analytic function.

### Statement

Choose an even pole bound \(\mathcal N\ge2g+2\), and let
\[
V=H^0(C,\mathcal O_C(\mathcal N\infty))
\]
with its usual explicit monomial basis in \(x,y\).

Let \(s_1,\ldots,s_r\in V\), where \(1\le r\le g\). Assume their coefficient matrix in that basis:

- has entries in \(\mathbf Z_2\);
- has an \(r\times r\) minor that is a unit.

Equivalently, the supplied section lattice is primitive. This is a substantive input-normalization hypothesis, not something inferred from nonspecialness.

Consider the fraction-free evaluation determinant
\[
\mathcal D_W(z)=
\det\!\left(
t_i(z)^{\mathcal N}s_j(P(t_i(z)))
\right)_{i,j=1}^r,
\qquad
t_i(z)=2^{n_s}i+2^Rz_i.
\]
Multiplication by \(t_i^{\mathcal N}\) explicitly clears the infinity poles.

Restrict the permitted integer samples to
\[
z_i=2^c Z_i,\qquad c=n_s+4r.
\]
Set
\[
R'=R+c,\qquad a=R'-n_s=R+4r.
\]
Then a valid conditioning cap is
\[
\boxed{
K_{\mathrm{RR}}
=(R+n_s+12r)\,r\mathcal N+2r.
}
\]

If each \(Z_i\) is sampled independently and uniformly from
\[
\{0,\ldots,2^{K_{\mathrm{RR}}+1}-1\},
\]
then
\[
\boxed{
\Pr\!\left[v_2(\mathcal D_W(2^cZ))\le K_{\mathrm{RR}}\right]\ge\frac12.
}
\]

This uses only polynomial-bit integers and polynomially many draws. It does not enumerate the grid.

### Paid low-jet coefficient

After multiplying a standard section by \(t^{\mathcal N}\), the basis functions are
\[
t^e
\quad\text{or}\quad
t^e\sqrt{F(t^2)},
\]
with distinct exponents
\[
e\in
\{0,2,\ldots,\mathcal N\}
\;\cup\;
\{1,3,\ldots,\mathcal N-2g-1\}.
\]

Put \(t=2^{n_s}u\), and remove the known factor \(2^{n_se}\) from each basis function. The resulting functions are
\[
u^e
\quad\text{or}\quad
u^e S(u),
\qquad
S(u)=\sqrt{F(2^{2n_s}u^2)}.
\]
The integral-coefficient hypothesis on \(f\) and \(n_s\ge2\) imply
\[
S(u)\in1+4\mathbf Z_2\langle u\rangle.
\]

At any integer center \(i\), take Taylor coefficients of orders belonging to the displayed exponent set. The resulting square jet matrix is upper triangular with diagonal \(1\), modulo \(4\). It is consequently invertible over \(\mathbf Z_2\).

These are Taylor coefficients—Hasse jets—not ordinary derivatives with omitted factorial costs.

Primitivity of the section matrix implies that the alternating coefficient tensor of the evaluation determinant has a coefficient of valuation at most
\[
n_s r\mathcal N.
\]
Applying the integral invertible jet matrices preserves this minimum-content bound. Hence some jet with
\[
\alpha_i\le\mathcal N,\qquad |\alpha|\le r\mathcal N
\]
has valuation at most \(n_s r\mathcal N\).

Substituting \(u_i=i+2^aZ_i\) proves that some coefficient satisfies
\[
\boxed{
v_2\!\left([Z^\alpha]\mathcal D_W(2^cZ)\right)
\le C:=R'r\mathcal N.
}
\]
This bound is independent of the higher digits or hidden height of the sections.

The tensor argument proves existence of a bounded-content jet; the algorithm does **not** construct that tensor or enumerate its coefficients.

### Restricted-series tail

Before the substitution \(u_i=i+2^aZ_i\), all Taylor coefficients are integral. Therefore
\[
v_2\!\left([Z^\alpha]\mathcal D_W(2^cZ)\right)\ge a|\alpha|.
\]

Truncate at total degree
\[
d_{\mathrm{tr}}=4r\mathcal N+1.
\]
The omitted tail is divisible, coefficientwise, by
\[
2^{a(d_{\mathrm{tr}}+1)}.
\]
Since \(n_s\le R\) and \(a=R+4r\),
\[
a(d_{\mathrm{tr}}+1)>
C+2r\,d_{\mathrm{tr}}
=K_{\mathrm{RR}}.
\]
Thus the tail cannot change any valuation at or below the claimed cap.

Again, the multivariate truncation is for analysis. Evaluating the original \(r\times r\) determinant requires only individual section evaluations and polynomial-size linear algebra.

### Finite-grid anti-concentration

The elementary counting fact needed here is:

> If \(P\in\mathbf Z_2[Z_1,\ldots,Z_r]\) has coefficient content \(c_P\) and coordinate degrees \(d_i\), then
> \[
> \mathbb E\,v_2(P(X))\le c_P+\sum_i d_i
> \]
> for independent uniform \(2\)-adic parameters \(X_i\).

For one variable, factor over an algebraic closure and use the Gauss norm. Each integral root contributes at most \(1\) to the expected valuation. Induction on the variables gives the stated bound.

Consequently, if \(c_P\le C\) and \(\sum d_i\le r d_{\mathrm{tr}}\),
\[
\Pr[v_2(P(X))>C+2r d_{\mathrm{tr}}]\le\frac12.
\]

The event below this valuation cap depends only on the parameters modulo \(2^{K_{\mathrm{RR}}+1}\). Hence exactly the same bound holds for the finite grid above. The Haar variables are only a proof device for this finite-residue counting statement; they are not a source of Jacobian points.

### What is charged

Given the primitive section basis to the required precision:

- its coefficient access and storage cost is polynomial in \(r,\mathcal N,K_{\mathrm{RR}}\);
- the principal square roots are computed from the explicit equations and residue choice, with the dyadic square-root precision charged;
- the determinant is evaluated modulo \(2^{K_{\mathrm{RR}}+1}\);
- \(O(\log(1/\varepsilon))\) independent draws suffice for failure probability \(\varepsilon\).

No support-field compositum, Plücker-coordinate enumeration, or multivariate-series enumeration is needed.

For a prospective degree-\((2g+1)\) KM representation, \(\mathcal N=4g+2\) meets the supplied RR degree requirements. The displayed cap is then polynomial in \(g,R\).

**Status:** the matrix lemma is proved. Its applicability throughout the point-arithmetic pipeline remains conditional on obtaining the stated primitive section basis with an actual-point certificate and paid precision.

## 4. Why this does not prove the requested RESET

There are four unresolved bridges.

### A. Primitive RR input is not supplied by the native problem

Every exact subspace admits a primitive lattice basis. That existence statement does not pay for recovering one from ill-conditioned finite data.

A maintained KM-type representation would need to specify, for example:

- a degree-\((2g+1)\) effective divisor class;
- its subspace in \(H^0((4g+2)\infty)\);
- a primitive finite-precision basis;
- data certifying an actual divisor/Jacobian point behind that basis.

An arbitrary rounded Grassmannian matrix is not such a certificate.

The RR lemma does not pay the transformations needed to establish this invariant initially and after each addition or half.

### B. The required matrices are not all independent-point evaluation blocks

The perturbation of the halving input contains \(2P(t_i(z))\), not just independent simple evaluation conditions. Actual constructions can involve:

- confluent conditions;
- multiplication and division of section spaces;
- kernel computations and cancellations;
- degree and squarefree branches.

One cannot substitute their determinants into the proved evaluation-block lemma without deriving the corresponding coefficient map and its integral conditioning.

### C. The Stoll augmented determinant still lacks its paid jet

For
\[
\Delta_h(z)=\det\mathcal B_g(h+2\sigma(z)),
\]
the needed assertion is something like
\[
\exists\,|\alpha|\le d_{\rm Stoll}:
\quad
v_2([z^\alpha]\Delta_h)\le C_{\rm Stoll},
\]
with both quantities polynomial in native parameters, after a specified, charged normalization.

I have not established this.

In particular, the RR evaluation argument does not control the prescribed \(w_g\)-functional on the Stoll kernel. A bound for \(\mathcal M_g\) alone cannot replace the augmented-matrix bound. Nor does a degree bound control a common \(2\)-adic content factor.

The square-root branch \(s\) must also be selected and materialized with paid precision. An analysis of one analytic half branch is not yet an algorithm for transporting that branch without an exponential sign search.

### D. There is no whole-loop loss induction here

The established RR bound is independent of \(h\), but the missing conversions and Stoll determinant bound are not paid.

A valid completion needs either a reset invariant
\[
S_i\le P(g,B,D,D_0,R)
\]
or an additive ledger such as
\[
S_i\le S_{\rm seed}+i\,P(g,B,D,D_0,R),
\qquad i\le\kappa.
\]
I obtain neither for the complete pipeline. In particular, this report does not replace them with a per-step bound polynomial in the previous \(S_i\).

## 5. Exact acceptance and falsification obligations

A full RESET proof should supply the following, for a specified polynomial-size representation:

1. **Actual-point invariant:** finite data name an actual \(h\), and output data name an actual \(q\), with the error schedule proving \(2q-h\in E\), for the original \(E\).
2. **Native materialization bound:** obtaining each tested RR/Stoll matrix has polynomial numerical precision and denominator cost.
3. **Augmented-minor content:** explicit low-jet order and valuation bounds for enough actual minors, including the leading-coordinate augmentation.
4. **Tail bounds at the acceptance threshold:** not just convergence.
5. **Joint success probability:** if polynomially many certificates must hold simultaneously, separate constant-success statements are insufficient. A union-bound-compatible failure budget or a justified adaptive sampling argument is needed.
6. **Bounded retries and loop precision:** no exact infinite zero tests and no precision recursion capable of exponential growth.

A genuine counterfamily must instead exhibit native inputs and admissible saturation states for which the proposed selectable representation family cannot meet such a bound with inverse-polynomial probability. A bad canonical representative, or one vanishing determinant at \(z=0\), does not do this. No such counterfamily is produced here.

## Bottom line

The explicit \(\sigma\)-family is strong enough to yield a **paid finite-grid reset for primitive RR evaluation blocks**. The genus-one branch-torsion control also survives the cheapest native attack with an explicit augmented-determinant bound.

But the decisive claim remains unproved: **uniformly obtaining and conditioning the actual Stoll augmented matrix from polynomial-size maintained saturation data, across the entire loop.** Neither the supplied sources nor the partial lemma above provides that bridge.

Accordingly, ONE-HALF remains open in this report. Closing it would provide a classical local routine; it would not by itself establish a quantum separation, Mordell–Weil rank algorithm, or point-finding result.