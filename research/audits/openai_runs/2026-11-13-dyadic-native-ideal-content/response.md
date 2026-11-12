## Result: the native \(C_i\) and \(M_D\) content bounds hold

There is a direct saturation argument using the trace ideal of each graph ideal. Combined with an elementary pole-semigroup argument, it gives:

* **For integral blocks**, every nonzero Smith exponent of \(C_i\) is at most \(D+1\). Consequently,
  \[
  \boxed{\tau(C_i)\le r_i(D+1),\qquad
  r_i=2m-\sum_{j\le i}e_j,}
  \]
  where \(\tau\) denotes the minimum valuation of a nonzero maximal minor.
* For the final, saturated quotient and the specified high-degree RR matrix,
  \[
  \boxed{\tau(M_D)=0\qquad(S=0).}
  \]
* The projection of the integral RR kernel onto its coefficient of pole order \(N=m+2g+1\) is also surjective over \(\mathbf Z_2\). Thus there is **no additional infinity content in this high-degree projection** for integral inputs.
* Explicit diagonal scaling gives polynomial bounds for the **original matrices with coefficient poles \(S\)**. These bounds are stated below.

These are bounds for the actual product-ideal compiler, not for raw point evaluation. They do not require support separation, étale divisors, splitting fields, or a regular model.

They do **not** bound the later discriminant/resultant rejection tests or the halving matrices.

---

## 1. First test: individual flatness does not imply product flatness

Let
\[
f=x^3+1,\qquad D=v_2(-27)=0,
\]
and take the two actual integral graph ideals
\[
I_-=(x,y-1),\qquad I_+=(x,y+1).
\]
Both quotients are \(\mathbf Z_2\)-free. Nevertheless,
\[
I_-I_+
=(x^2,x(y-1),x(y+1),x^3)
=x(x,y-1,2).
\]
Its \(2\)-saturation is \((x)\), and
\[
(x)/(I_-I_+)\simeq
R_0/(x,y-1,2)\simeq\mathbf F_2.
\]
Thus the product quotient is not flat.

This also appears in the **actual compiler matrix**. In
\[
T_0=R_0/(x^2),
\]
use the saturated basis \(x,y-1,xy\) for the first ideal. At the second stage the nonzero columns span
\[
xy-x,\qquad xy+x.
\]
Their determinant in the rows \(x,xy\) is \(-2\). Therefore
\[
\tau(C_2)=1.
\]

This is an exact falsifier of the flatness shortcut. It is not a growing-loss counterexample; the loss is precisely of the bounded type proved next.

---

## 2. The trace-ideal saturation lemma

Write
\[
\mathcal O=\mathbf Z_2,\qquad
B=\mathcal O[x,y]/(y^2-f).
\]
For an integral graph ideal
\[
I=(a,y+b),\qquad
c=\frac{f-b^2}{a}\in\mathcal O[x],
\]
put
\[
w=\frac{y-b}{a}
\]
in the fraction field of \(B\). Then
\[
wa=y-b,\qquad w(y+b)=c.
\]
In particular, \(1,w\in I^{-1}\), and
\[
II^{-1}\supseteq(a,y+b,y-b,c).
\]

This last ideal contains \(2y\), \(2b\), and
\[
f'=a'c+ac'+2bb'.
\]
Hence
\[
(2y,f')\subseteq II^{-1}.
\]

Let
\[
\Delta=\operatorname{Res}(f,f')=\pm\operatorname{disc}(f).
\]
The Sylvester adjugate supplies integral polynomials \(\rho,\sigma\) with
\[
\rho f+\sigma f'=\Delta.
\]
In fact one can save one power of \(2\) from the parent observation:
\[
2\Delta=(\rho y)(2y)+2\sigma f'.
\]
Consequently,
\[
\boxed{2\Delta\in II^{-1}.} \tag{2.1}
\]

### Saturation consequence

For an \(\mathcal O\)-saturated ideal \(J\subset B\), define
\[
Z=(I_KJ_K)\cap B,\qquad K=\mathbf Q_2.
\]
Then
\[
\boxed{(2\Delta)Z\subset IJ.} \tag{2.2}
\]

To prove this, take \(z\in Z\). The graph quotient \(B/I\simeq\mathcal O[x]/a\) is free, so \(I\) is saturated and \(z\in I\). For any \(u\in I^{-1}\),
\[
uz\in B,\qquad uz\in J_K.
\]
Since \(J\) is saturated, \(uz\in J\). Expressing \(2\Delta\) as a sum of elements of \(I\) times elements of \(I^{-1}\), as in (2.1), proves (2.2).

No transversality or distinct-support hypothesis occurs here.

---

## 3. Application to the compiler’s actual \(C_i\)

Let
\[
P_i=I_1\cdots I_i,\qquad
J_i=P_{i,K}\cap B.
\]
Since \(P_i\) contains \(\prod_{j\le i}a_j\), these quotients are finite over \(\mathcal O\). Moreover, \(A=\prod_j a_j\) belongs to every \(P_i\).

The saturated lattice represented by \(V_{i-1}\) is
\[
J_{i-1}/(A)\subset T_0=B/(A).
\]
The column lattice of
\[
C_i=[G_iV_{i-1}\mid H_iV_{i-1}]
\]
is exactly
\[
I_iJ_{i-1}/(A).
\]
Applying (2.2) gives
\[
(2\Delta)\bigl(J_i/(A)\bigr)
\subseteq \operatorname{im}_{\mathcal O}C_i.
\]

Thus every nonzero Smith exponent of \(C_i\) is at most
\[
v_2(2\Delta)=D+1.
\]
For an integral rank-\(r_i\) matrix, its maximal-minor content is the sum of its nonzero Smith exponents. Therefore
\[
\boxed{\tau(C_i)\le r_i(D+1).} \tag{3.1}
\]

This is independent of the preceding choice of saturated basis: changing that basis by \(\mathrm{GL}_{r_{i-1}}(\mathcal O)\) does not change the column lattice.

There is also a bound for the **unsaturated raw product**. Induction in (2.2) gives
\[
\boxed{
2^{(i-1)(D+1)}P_i^{\mathrm{sat}}\subseteq P_i.
} \tag{3.2}
\]
The implementation benefits from saturating at each stage: its per-stage Smith bound is \(D+1\), rather than an accumulated \((i-1)(D+1)\).

---

## 4. Why the high-degree \(M_D\) has a unit maximal minor

The needed integral rank statement does not follow merely from characteristic-zero nonspeciality. Here it follows from the **monic odd-degree pole semigroup**.

### A finite-colength ideal lemma

Let \(k\) be any field and
\[
B_k=k[x,y]/(y^2-\bar f),
\]
where \(\bar f\) is monic of degree \(d=2g+1\). No smoothness assumption is needed.

Give \(x,y\) weights \(2,d\). Every nonzero \(p+qy\) has a unique leading weight, and leading weights multiply additively. The possible weights form
\[
\mathcal H=\langle2,d\rangle.
\]
There are exactly \(g\) missing nonnegative integers:
\[
1,3,\ldots,2g-1.
\]

Let \(L\subset B_k\) be an ideal of colength \(m\), and let \(\mathcal E\subset\mathcal H\) be its set of leading weights. Then
\[
\mathcal E+\mathcal H\subseteq\mathcal E,
\qquad
|\mathcal H\setminus\mathcal E|=m.
\]

If \(t\in\mathcal H\setminus\mathcal E\), every \(h\) satisfying
\[
h\in\mathcal H,\qquad t-h\in\mathcal H
\]
must also lie outside \(\mathcal E\). There are at least \(t+1-2g\) such integers: among \(0,\ldots,t\), at most \(g\) fail the first condition and at most \(g\) fail the second. Hence
\[
m\ge t+1-2g.
\]
Therefore
\[
\boxed{
B_k/L\text{ is spanned by monomials of weight }\le m+2g-1.
} \tag{4.1}
\]

This is an elementary filtered-algebra argument; it does not require constructing an integral curve model.

### Apply it to the final saturated quotient

For integral inputs,
\[
Q=B/J_k
\]
is finite free of rank \(m\). Reducing modulo \(2\) therefore gives an ideal quotient of colength exactly \(m\). By (4.1), the monomials of weight at most \(m+2g-1\) surject onto \(Q/2Q\), and hence onto \(Q\) over \(\mathcal O\).

The compiler’s \(\Lambda_D\), because its complementary block is an identity, identifies
\[
T_0/(J_k/(A))\simeq\mathcal O^m.
\]
Thus it is an integral quotient coordinate system, not a raw evaluation map. Since \(E_N\) includes all the monomials in (4.1),
\[
M_D=\Lambda_DE_N
\]
is surjective over \(\mathcal O\). Consequently,
\[
\boxed{\tau(M_D)=0.} \tag{4.2}
\]

### The infinity projection

Let \(\alpha\) be the coefficient of the unique monomial of weight
\[
N=m+2g+1.
\]
The monomials of weight at most \(N-1\) already surject onto \(Q\). Subtract an integral combination of those lower monomials from the top monomial to obtain an element of the kernel with
\[
\alpha=1.
\]
Therefore
\[
\boxed{
\alpha\bigl(\ker M_D\cap\mathcal O^{m+g+2}\bigr)=\mathcal O.
} \tag{4.3}
\]
Equivalently, the augmented matrix
\[
\begin{pmatrix}M_D\\ \alpha\end{pmatrix}
\]
also has a unit maximal minor.

Thus this particular high-degree infinity projection has no theta-content loss for integral blocks. A fixed, preselected minor can still be poor; the statement concerns the minimum over available charts.

---

## 5. Explicit extension to coefficient poles \(S\)

Assume \(m\ge1\); degree-zero blocks can be discarded. Set
\[
d=2g+1,\quad N=m+d,\quad
s=\left\lceil S/2\right\rceil.
\]
Use the monicity-preserving change
\[
X=2^{2s}x,\qquad Y=2^{ds}y,
\]
and define
\[
\widetilde f(X)=2^{2ds}f(2^{-2s}X),
\]
\[
\widetilde a_i(X)=2^{2se_i}a_i(2^{-2s}X),
\qquad
\widetilde b_i(X)=2^{ds}b_i(2^{-2s}X).
\]

Then \(\widetilde f,\widetilde a_i\) are integral and monic, and
\[
\widetilde D
=v_2\operatorname{disc}(\widetilde f)
=D+2s\,d(d-1). \tag{5.1}
\]

Importantly, this scaling need **not** make \(\widetilde b_i\) integral. Its pole bound is
\[
t_i=\max\{0,\ S+s(2e_i-2-d)\}.
\]
A uniform bound is
\[
t=\max\{0,\ S+s(2m-2-d)\}. \tag{5.2}
\]

### Denominator version of the saturation lemma

In an integral monic model, suppose \(a\) is integral monic, \(b\) has poles at most \(t\), and \(a\mid F-b^2\). If \(J\) is saturated and
\[
Z=((a,y+b)_KJ_K)\cap B,
\]
then
\[
\boxed{
2^{3t}(2\Delta_F)Z
\subseteq (a,2^t(y+b))J,
\qquad
\Delta_F=\operatorname{Res}(F,F').
} \tag{5.3}
\]

Here is the denominator bookkeeping.

Put
\[
c=(F-b^2)/a,\qquad w=(y-b)/a.
\]
Monic division gives pole bounds \(2t\) for \(c\) and \(c_x\), and \(t\) for \(b,b_x\). For \(z=u+vy\in Z\), write
\[
u-bv=aq.
\]
Again, monic division gives a pole bound \(t\) for \(q\), and
\[
wz=q(y-b)+vc.
\]
Thus
\[
2^{2t}wz\in B\cap J_K=J.
\]
Also \(z\in J\).

Choose integral \(\rho,\sigma\) with \(\rho F+\sigma F'=\Delta_F\). The exact identity
\[
\begin{aligned}
2\Delta_F={}&
a\left[2\sigma c_x+(\rho y-2\sigma b_x)w\right]\\
&+(y+b)\left[\rho y+2\sigma b_x+2\sigma a_xw\right]
\end{aligned} \tag{5.4}
\]
then proves (5.3): after multiplication by \(2^{3t}z\), the first bracket gives an element of \(J\), and the second is divisible by \(2^t\) with the remaining factor in \(J\).

This explicitly handles the nonflatness introduced by clearing \(b\).

### Compare the scaled and original coefficient lattices

Let \(L=\mathcal O^{2m}\) be the compiler’s original coordinate lattice in \(T\). The integral lattice of the scaled model is
\[
L'=\operatorname{span}_{\mathcal O}
\{X^j,X^jY:0\le j<m\}.
\]
Its basis vectors have original-coordinate scalings
\[
2^{2sj},\qquad 2^{ds+2sj}.
\]
Consequently, with
\[
W=s(d+2m-2),
\]
we have
\[
\boxed{2^WL\subseteq L'\subseteq L.} \tag{5.5}
\]
The same inclusions hold after intersection with every partial-product \(K\)-subspace.

The scaled, cleared generators map to
\[
\widetilde a_i\longmapsto 2^{2se_i}a_i,
\qquad
2^{t_i}(Y+\widetilde b_i)
\longmapsto2^{ds+t_i}(y+b_i).
\]
Their column lattice is therefore contained in the original, uncleared column lattice.

### Explicit clearing and content bounds

Put
\[
T=mS,
\]
\[
B=S+\max\{m,d\}\,T,
\qquad
E=\left\lfloor N/2\right\rfloor T.
\]
These clear the original matrices:
\[
2^BC_i\text{ is integral},\qquad
2^EM_D\text{ is integral}.
\]
Indeed, coefficients of \(A\) have poles at most \(T\), and the companion-matrix estimates give
\[
v(a_i(X))\ge-S-e_iT,\quad
v(b_i(X))\ge-S-(e_i-1)T,\quad
v(f(X))\ge-dT.
\]

Define
\[
H_C=B+W+\widetilde D+1+3t.
\]
Combining (5.3) and (5.5) gives the bound for the **original compiler matrices**:
\[
\boxed{\tau(2^BC_i)\le r_iH_C.} \tag{5.6}
\]

For the RR matrix, the scaled final quotient is finite free and the semigroup lemma applies to it, even though the scaled \(b_i\) need not be integral. Its monomials surject onto that quotient. Under (5.5), this implies
\[
2^{E+W}\mathcal O^m
\subseteq\operatorname{im}_{\mathcal O}(2^EM_D).
\]
Therefore
\[
\boxed{\tau(2^EM_D)\le m(E+W).} \tag{5.7}
\]

All these quantities are polynomial in \(g,m,D,S\). No discriminant of \(A\), pairwise resultant of the blocks, or support-separation parameter appears.

---

## 6. The precise infinity-content bridge

Let
\[
\mathcal K=\ker M_D\cap\mathcal O^{m+g+2},
\qquad
\alpha(\mathcal K)=2^{a_\infty}\mathcal O.
\]
The scaled integral RR construction has a section with top coefficient \(1\). Returning to the original coordinates gives an integral section with top coefficient \(2^{sN}\). Hence
\[
\boxed{a_\infty\le sN.} \tag{6.1}
\]

For
\[
\widehat M=2^EM_D,\qquad
\widehat B_\infty=
\begin{pmatrix}\widehat M\\ \alpha\end{pmatrix},
\]
there is an exact cokernel sequence
\[
0\longrightarrow
\mathcal O/\alpha(\mathcal K)
\longrightarrow
\operatorname{coker}\widehat B_\infty
\longrightarrow
\operatorname{coker}\widehat M
\longrightarrow0.
\]
Thus the contents satisfy the exact identity
\[
\boxed{
\tau(\widehat B_\infty)
=\tau(\widehat M)+a_\infty
\le m(E+W)+sN.
} \tag{6.2}
\]

This identifies and pays the extra projection content rather than suppressing it. For \(S=0\), both terms vanish.

No bridge from good reduced Mumford coordinates is needed for these two matrices. Such a bridge to a later low-degree or halving matrix would be a separate claim.

---

## 7. A polynomial precision schedule for these outputs

Let \(k\le m\) be the number of nontrivial blocks, and define
\[
T_C=H_C\sum_{i=1}^k r_i\le2m^2H_C,
\]
\[
T_R=m(E+W),\qquad T_\infty=sN.
\]
A deliberately conservative construction allowance is
\[
L_{\rm build}=B+E+T+S+2.
\]

To return saturated product bases, an integral RR kernel basis, and a top-normalized RR section to absolute precision \(P\), it suffices to request the input coefficients to
\[
\boxed{
P_{\rm in}
=
P+L_{\rm build}
+4(T_C+T_R+T_\infty)+4.
} \tag{7.1}
\]

The reason the losses add rather than iterate polynomially is important:

1. Form the fixed integral operators
   \[
   2^BG_i,\quad2^BH_i,\quad2^EE_N.
   \]
2. Every normalized \(V_i\) and every \(\Lambda_D\) is integral.
3. Multiplication by these cleared operators does not amplify errors in the normalized bases.
4. A rank-\(r\) pivot block of determinant valuation \(\tau\) costs at most \(2\tau\) digits for the usual uncertain inverse bound. The factor \(4\) in (7.1) also allows conservative pivot-discovery arithmetic.
5. Finally, dividing a kernel vector by a top coefficient of valuation at most \(T_\infty\) is paid explicitly.

Complete valuation-pivoted elimination finds a minimum-content chart without enumerating minors. The known rank tells it when to stop. The proved bounds ensure a visible pivot exists at each required step; no exact-zero oracle or probabilistic acceptance premise is needed.

### Coefficient recovery and exact output naming

Finite digits do not recover an entire \(2\)-adic coefficient. A suitable output is:

* \(P\)-digit coefficient approximations;
* a shared rational arithmetic DAG relative to the actual inputs;
* finite nonzero-pivot certificates.

The fraction-free basis and kernel formulas define the exact objects named by that DAG. Their exact identities follow from the algebra and prescribed ranks, not from declaring a small numerical residual to be zero.

After top normalization, the section coefficients have poles at most \(T_\infty\). One may additionally form
\[
H=p^2-fq^2,\qquad R=H/A
\]
by exact monic division. A safe coefficient-pole bound is
\[
v_2(R_j)\ge-\bigl(2T_\infty+(d+1)T\bigr).
\]
For \(P\)-digit recovery of \(R\), adding
\[
4T_\infty+4(d+1)T+4
\]
guard digits to the \(P\) used in (7.1) is sufficient.

This does **not** certify that \(R\) is squarefree or that \(q\) is invertible modulo \(R\).

### Actual-divisor certificate

Let \(Z\) be the effective divisor represented by the product of the graph ideals. The exact kernel identities prove
\[
F\in L(N\infty-Z).
\]
A nonzero top coefficient proves that \(F\) has exact pole order \(N\), so
\[
Z'=\operatorname{div}(F)+N\infty-Z
\]
is an actual finite effective divisor of degree \(d\). This gives an exact divisor-class certificate without splitting its support.

In the report’s notation \(Z=\iota D\), the certificate is
\[
D'-d\infty
=\operatorname{div}(F/A)+D-m\infty.
\]

The actualness of the **input** graph divisors remains a hypothesis, as stipulated in the question. Arbitrary finite approximations alone cannot certify the exact identities \(a_i\mid f-b_i^2\).

### Cost ledger

There are \(O(d+m)\) input coefficients and polynomially many matrix operations on dimensions \(O(d+m)\). The additional arithmetic and output cost is polynomial in
\[
d,m,P_{\rm in},S,D.
\]
The input-access cost must be added explicitly: if obtaining certified input coefficients to precision \(Q\) costs \(\mathcal A(Q)\), the total includes \(\mathcal A(P_{\rm in})\). A bound on coefficient poles does not by itself bound the evaluation cost of an arbitrary pre-existing input DAG.

The kernel output has \(O((m+g)(g+2))\) coefficients, whose writing cost must likewise be paid. This operation is classical; no quantum state-preparation or speedup claim is involved.

---

## 8. Scope and falsifiers

### Established here

* Raw product torsion is killed by \(2^{(i-1)(D+1)}\) for integral blocks.
* Each saturated compiler stage has nonzero Smith exponents at most \(D+1\).
* The integral high-degree \(M_D\), and its infinity augmentation, have unit maximal minors.
* Explicit polynomial caps hold after denominator clearing for the original matrices with poles \(S\).
* Rank discovery, RR coefficient recovery, and exact section/divisor certificates have the polynomial precision schedule above.

Thus a family with fixed \(g,m,D,S\) cannot have unbounded cleared content in these \(C_i\) or \(M_D\).

The central algebraic checkpoints are explicit:

1. \(2\Delta\in II^{-1}\) and inclusion (2.2);
2. the denominator-cleared inclusion (5.3);
3. the semigroup count (4.1);
4. the lattice comparison (5.5).

An alleged native counterexample can be checked directly against those statements.

### Not established here

The result does not yet supply bounded-content general-position discriminants/resultants, a squarefree admissible Mumford output, a halving-matrix bound, or an iterated reset theorem. Those are different quantitative questions.

**Bottom line:** the proposed Jacobian mechanism does pay the native product-ideal minors. More strongly, after saturation the fixed high-degree RR matrix has a separate, elementary integral-surjectivity argument, so its minimum-minor conditioning is not a remaining theta obstruction.