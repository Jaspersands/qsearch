\[
\boxed{
0\longrightarrow \operatorname{Sel}_2(J)
\longrightarrow E
\xrightarrow[\operatorname{rank}=r]{\,\pi_{\mathcal C}\lambda\,}
V/\mathcal C
\xrightarrow[\operatorname{rank}=s]{\,\beta\,}
\operatorname{Sel}_2(J)^\vee
\longrightarrow 0
}
\]
Here
\[
\dim E=\dim(V/\mathcal C)=D,\qquad
s=\dim\operatorname{Sel}_2(J)=D-r.
\]
The first injection has rank \(s\). The localization map \(\lambda\) itself has rank \(D\), and the quotient map \(\pi_{\mathcal C}\) has rank \(D\); their **composition rank \(r\) remains unknown**.

This is the exact self-dual comparison sequence on the promised odd-class-number branch fields. It exposes the issue: Poitou–Tate identifies the missing cokernel with the dual of the desired Selmer group; it does not independently determine its dimension.

Below I derive the sequence, examine the extra information supplied by genus theory and norms, give an exact arithmetic control in a cyclic quartic field, and isolate one unit-basis-free operation that would finish the attack. I obtain no polynomial-time implementation of that operation and no pair of genuinely native indistinguishable instances.

## 1. Definitions and all rank terms

Put
\[
P=\{p:p\mid 2\operatorname{disc}(f)\},\qquad \Sigma=P\cup\{\infty\},
\]
and write the branch algebra as \(A=\prod_i K_i\). For this review, every nonrational \(K_i\) is in the promised Galois \(2\)-power, one-finite-prime family. Let \(S_i\) contain all primes above \(P\), and define
\[
E_i=K_i(S_i,2),\quad
e_i=r_1(K_i)+r_2(K_i)+|S_i|,\quad
m=\sum_i e_i,\quad q=|P|+1,\quad D=m-q.
\]

The standard source sequence is
\[
0\longrightarrow
\mathcal O_{K_i,S_i}^{\times}/\mathcal O_{K_i,S_i}^{\times2}
\longrightarrow E_i
\longrightarrow \operatorname{Cl}(\mathcal O_{K_i,S_i})[2]
\longrightarrow0.
\]
The supplied odd ordinary class-number proof makes the last term zero. Thus \(\dim E_i=e_i\), but supplies no localization matrix.

Define
\[
E_A=\bigoplus_i E_i,\qquad
E=\ker\!\left(N:E_A\longrightarrow \mathbf Q(P,2)\right).
\]
The diagonal rational inclusion splits \(N\), since the total degree is odd. Hence
\[
\operatorname{rank}N=q,\qquad \dim E=D.
\]
These are actual field norms: finite valuation rows include residue degrees. No quotient by diagonal rational squareclasses is being substituted for the norm kernel.

For the local spaces set
\[
V_A=\bigoplus_{v\in\Sigma}A_v^\times/A_v^{\times2},\qquad
V_{\mathbf Q}=\bigoplus_{v\in\Sigma}\mathbf Q_v^\times/\mathbf Q_v^{\times2},
\]
and
\[
V=\ker(N:V_A\to V_{\mathbf Q}).
\]
Local squareclass dimensions give
\[
\dim V_A=2m,\quad \dim V_{\mathbf Q}=2q,\quad
\operatorname{rank}N_{\rm loc}=2q,\quad \dim V=2D.
\]

Write Hilbert symbols additively in \(\mathbf F_2\). The sum of local Hilbert pairings gives a perfect symmetric form \(b_A\) on \(V_A\). Norm is adjoint to diagonal restriction:
\[
b_A(x,\operatorname{res}a)=b_{\mathbf Q}(Nx,a).
\]
The restriction \(b\) to \(V\) is perfect and alternating, because
\[
b_A(x,x)=b_A(x,-1_A)=b_{\mathbf Q}(Nx,-1)=0.
\]
This is the local Tate pairing in the odd-degree descent identification.

Let
\[
\lambda:E\to V,\qquad L=\lambda(E),
\]
and let
\[
\mathcal C=\bigoplus_{v\in\Sigma}\mathcal C_v
\]
be the already computed complete local Kummer images, in these common frames. Local duality gives
\[
\mathcal C=\mathcal C^\perp,\qquad \dim\mathcal C=D.
\]

Two global facts now suffice:

* **Injectivity.** A class in \(\ker\lambda\) defines, in each branch field, an ordinary everywhere-unramified quadratic extension, split at the specified places. Odd ordinary class number excludes it. Thus \(\operatorname{rank}\lambda=D\).
* **Reciprocity.** \(L\) is isotropic. Outside \(\Sigma\), admissible classes have even valuations and the relevant odd-prime unit–unit Hilbert symbols vanish. Since \(\dim L=D\), this gives \(L=L^\perp\).

Using the supplied good-prime descent statement outside \(P\),
\[
\operatorname{Sel}_2(J)=\lambda^{-1}(\mathcal C)
\cong L\cap\mathcal C.
\]
Consequently
\[
\boxed{\dim\operatorname{Sel}_2(J)
=D-\operatorname{rank}(\pi_{\mathcal C}\lambda).}
\]

The last map in the opening sequence is explicitly
\[
\beta([v])(s)=b(v,\lambda(s)).
\]
It is well-defined because \(\lambda(s)\in\mathcal C=\mathcal C^\perp\). Its kernel is
\[
(L+\mathcal C)/\mathcal C=\operatorname{im}(\pi_{\mathcal C}\lambda),
\]
and it is surjective by perfectness of \(b\). This proves the sequence, including its ranks.

For comparison, if
\[
h=\sum_i\dim\operatorname{Cl}(\mathcal O_{K_i,S_i})[2]
\]
were nonzero, then \(\dim E=D+h\), \(\dim\ker\lambda=h\), and
\[
\dim\operatorname{Sel}_2(J)=h+D-r.
\]
The comparison sequence would end
\[
V/\mathcal C\longrightarrow\operatorname{Sel}_2(J)^\vee
\longrightarrow(\ker\lambda)^\vee\longrightarrow0,
\]
with those two map ranks \(D-r\) and \(h\). The odd-class proof removes this \(h\)-term—not the intersection rank \(r\).

## 2. What genus theory and norms do—and do not—supply

### A slightly stronger rank deduction is available

For a totally real promised field, the same inertia argument can be applied to its canonical maximal elementary \(2\)-extension unramified at all **finite** primes, allowing ramification at infinity. It again rules out a nontrivial extension. Thus its narrow class group also has odd order.

The narrow/ordinary class sequence then implies that unit signatures have full rank. In particular, for totally real \(K\),
\[
K(S,2)\longrightarrow
\mathbf F_2^{r_1(K)}\oplus\mathbf F_2^{S},
\]
given by signatures and valuation parities, is an isomorphism.

This is useful additional **proof-only rank information**. It still does not compute the finite local squareclass associated with a prescribed signature/valuation vector. A rigidity or constructive theorem supplying that inverse localization remains necessary.

### The cyclic quartic branch \(\mathbf Q\times K\)

Let \([K:\mathbf Q]=4\). The global norm kernel is
\[
E\cong K(S,2),\qquad
a\longmapsto (N_{K/\mathbf Q}a,a).
\]
Thus the rational factor absorbs the norm. Imposing \(N_{K/\mathbf Q}a=1\) on the \(K\)-component would incorrectly discard classes.

Under this identification, the local pairing is
\[
\widetilde b(x,y)
=b_K(x,y)+b_{\mathbf Q}(Nx,Ny).
\]
It is symplectic, and the global image remains Lagrangian.

Let \(F\) be the quadratic subfield, and grant its complete squareclass source and localization using the retained quadratic algorithm. Its restriction gives a known subspace
\[
W=\operatorname{res}_{F}^{K}F(S_F,2)\subset L.
\]
If \(K=F(\sqrt{\delta})\), restriction has kernel \(\langle\delta\rangle\), so
\[
\dim W=e_F-1.
\]
Moreover,
\[
\ker\!\left(N_{K/F}:K(S,2)\to F(S_F,2)\right)=W.
\]
For the kernel assertion, the field-level norm-square kernel is the restriction of \(F^\times/F^{\times2}\); outside \(S_F\), the extension is unramified, so an admissible restricted class has even valuations already in \(F\). Hence the relative norm rank is exactly
\[
e_K-e_F+1.
\]

But knowing this rank is not knowing a local lift of each norm class.

Indeed, by norm–restriction adjunction,
\[
\widetilde b(x,\operatorname{res}a)=b_F(N_{K/F}x,a).
\]
Therefore the condition that relative norms lie in the global localization image of \(F(S_F,2)\) is precisely orthogonality to \(W\). For a self-dual \(L\), that duplicates the condition \(W\subset L\). An exact smaller norm-image subspace can add constraints, but still need not specify its lifts.

### Exact reduction after all known global classes

For any explicitly known \(W\subset L\), put
\[
\overline V=W^\perp/W,\qquad
\overline L=L/W,\qquad
\overline{\mathcal C}=
\big((\mathcal C\cap W^\perp)+W\big)/W.
\]
Writing \(w=\dim W\) and \(t=\dim(W\cap\mathcal C)\), both barred subspaces are Lagrangian in a space of dimension \(2(D-w)\), and
\[
\boxed{
\dim\operatorname{Sel}_2(J)
=t+\dim(\overline L\cap\overline{\mathcal C}).
}
\]
Thus known rational classes, proper-subfield classes and native torsion classes can be paid and removed exactly. Unless they span \(L\), a residual orientation problem remains in this derivation.

### Formal counterexample—not native realizability

Even a quadratic refinement and a full-rank prescribed projection do not settle the abstract intersection problem.

Take
\[
\overline V=X\oplus X^\vee,\qquad X=\mathbf F_2^2,
\]
with
\[
b((x,y),(x',y'))=x\cdot y'+x'\cdot y,\qquad Q(x,y)=x\cdot y.
\]
Let
\[
\overline{\mathcal C}=X\oplus0,\qquad
L_0=X\oplus0,\qquad
L_1=\{(x,Hx):x\in X\},
\quad
H=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
Both \(L_i\) are totally singular Lagrangians, both project isomorphically onto \(X\), but
\[
\dim(L_0\cap\overline{\mathcal C})=2,\qquad
\dim(L_1\cap\overline{\mathcal C})=0.
\]
Even the intersection parities agree.

This refutes a deduction from those abstract rank/duality axioms alone. It is **not** a construction of two promised branch fields realizing the two orientations.

## 3. An exact cyclic-quartic arithmetic control

A small native example demonstrates that norm-compatible local data really can fail to glue globally.

Take
\[
f=x^5-1=(x-1)\Phi_5(x),\qquad
K=\mathbf Q(\zeta_5),\qquad F=\mathbf Q(\sqrt5),
\]
with \(P=\{2,5\}\). The prime \(2\) is inert in \(K\), and \(5\) is totally ramified. Put
\[
\epsilon=\frac{1+\sqrt5}{2},\qquad \varpi=1-\zeta_5.
\]
The known dimension is \(e_K=4\).

In \(F(S_F,2)\), the four classes
\[
-1,\ \epsilon,\ \sqrt5,\ 2
\]
are independent by signatures and the two valuation parities, hence form a complete basis. Since
\[
(\zeta_5-\zeta_5^{-1})^2=-\sqrt5\,\epsilon,
\]
their restriction has image
\[
W=\langle -1,\epsilon,2\rangle,\qquad \dim W=3.
\]
The class \(\varpi\) has odd valuation at the prime above \(5\), whereas restricted \(F\)-classes have even valuation there. Therefore
\[
K(S,2)=\langle-1,\epsilon,2,\varpi\rangle.
\]
These labels have been derived here; they are not supplied unit advice.

Now define a local tuple \(z\) by
\[
z_{5}=[2]\in K_{5}^{\times}/K_{5}^{\times2},
\qquad z_{2}=0.
\]
There are no real \(K\)-components. It has:

* trivial relative norm to \(F\), since locally \(N_{K/F}(2)=4\);
* trivial absolute norm squareclass;
* zero valuation parity everywhere;
* zero Hilbert pairing with every element of \(W\).

Nevertheless,
\[
b_K(z,\lambda(\varpi))
=(2,\varpi)_{K_5}=1
\]
in additive notation: \(\varpi\) is a uniformizer and \(2\) is nonsquare in the residue field \(\mathbf F_5\). Global reciprocity therefore proves
\[
\boxed{z\notin\lambda K(S,2).}
\]
So local norm compatibility, including compatibility with every quadratic-subfield class, is not a gluing criterion.

There is also a useful formal completion inside this **native ambient space**. Write \(\ell=\lambda(\varpi)\), and compare
\[
L=W+\langle\ell\rangle,\qquad
L'=W+\langle\ell+z\rangle.
\]
Both are bilinear self-dual isotropic spaces of dimension four. They have the same valuation maps and the same relative and absolute norm images, because \(Nz=0\). In particular,
\[
N_{K/F}(\varpi)=\frac{\sqrt5}{\epsilon},\qquad
N_{K/\mathbf Q}(\varpi)=5
\]
are unchanged. They are also Galois-stable: conjugates of \(\varpi\) differ from it by units, whose squareclasses lie in \(W\).

For the native curve, the rational two-torsion divisor
\[
D=(1,0)-\infty
\]
has descent class \((5,\varpi)\). Hence \(\ell\in\mathcal C\). Since \(b(z,\ell)=1\), any vector \(\ell+z+w\), \(w\in W\), pairs nontrivially with \(\ell\) and cannot belong to \(\mathcal C\). Thus
\[
\dim(L'\cap\mathcal C)
=\dim(L\cap\mathcal C)-1.
\]

**Boundary of this control.** \(L'\) is not a second native global image. Native two-torsion immediately rejects it. Indeed, \(W\) together with that torsion class already spans the true image on this example. Nor have I verified that \(L'\) passes additional quadratic-refinement constraints. The example precisely falsifies sufficiency of the listed **bilinear, dimension and norm tests**; it is not an indistinguishable native pair or evidence of computational hardness.

## 4. A surviving basis-free candidate: constrained ray-class rank

There is an exact alternative endpoint that does not require a global unit or \(K(S,2)\) basis as output.

Continue with \(\mathbf Q\times K\). Choose a ray modulus containing all real places and finite exponents
\[
m_w=
\begin{cases}
1,&w\nmid2,\\
2e_w+1,&w\mid2.
\end{cases}
\]
These exponents ensure that the corresponding principal local congruence groups are squares. Consequently every quadratic extension represented by \(K(S,2)\) has conductor dividing this modulus.

Let
\[
R=\operatorname{Cl}_{\mathfrak m}(K),\qquad \overline R=R/2R.
\]
Class field theory gives, as an existence statement,
\[
\overline R^\vee\cong K(S,2),\qquad \dim\overline R=e_K.
\]
This does **not** supply character labels computationally.

A local tuple defines an idele and hence a map
\[
j:V_K\longrightarrow\overline R.
\]
Its pairing with the character defined by \(a\in K(S,2)\) is
\[
\chi_a(j(x))=b_K(\lambda(a),x).
\]

Define
\[
T=1+\operatorname{res}_{\mathbf Q}^{K}N_{K/\mathbf Q}
\]
on local squareclasses. Since \([K:\mathbf Q]=4\), \(T^2=1\), and
\[
b_K(x,Ty)=\widetilde b(x,y).
\]
It follows that
\[
\boxed{
\operatorname{Sel}_2(J)
\cong
\left(\overline R/j(T\mathcal C)\right)^\vee.
}
\]
Indeed, a global quadratic character annihilates \(j(T\mathcal C)\) exactly when its localization is orthogonal to \(\mathcal C\) under \(\widetilde b\), hence lies in \(\mathcal C\).

This gives the following precise unresolved operation.

### Required operation

**Input**

1. The native defining polynomial for \(K\), with the integral/local representations constructed at their charged costs.
2. \(S\) and the compact ray-modulus descriptor above.
3. A matrix \(P_*\) of local idele classes in the computed squareclass frames.

**Output**
\[
\operatorname{rank}_{\mathbf F_2}j(P_*),
\]
or equivalently \(\dim(\overline R/j(P_*))\).

For the Selmer problem, take \(P_*=T\mathcal C\). A polynomial-bit implementation on the promised fields would finish the cyclic-quartic attack without requiring a global basis as output.

This is an exact interface, **not an algorithm already obtained**. In the usual ray-class sequence,
\[
\mathcal O_K^\times
\longrightarrow
(\mathcal O_K/\mathfrak m_f)^\times\times\{\pm1\}^{r_1}
\longrightarrow R
\longrightarrow\operatorname{Cl}(K)
\longrightarrow0,
\]
odd ordinary class number removes the ordinary \(2\)-class contribution. It does not supply the unit residue image. Translating local uniformizer ideles into ray-class coordinates is also not free. A proposed implementation must avoid or pay these operations rather than hide them in “reciprocity.”

Testing whether each supplied basis vector glues is insufficient: combinations may glue. The interface needs an obstruction **rank**, or explicit linear obstruction coordinates.

### Cheapest exact falsifier for this operation

Use the preceding \(K=\mathbf Q(\zeta_5)\), with modulus
\[
\mathfrak m=\mathfrak P_2^3\mathfrak P_5,
\]
and give the operation the one-column matrix \(P_*=\langle z\rangle\).

The single explicit \(S\)-unit \(\varpi=1-\zeta_5\), of norm \(5\), certifies
\[
\chi_\varpi(j(z))=(\varpi,2)_{K_5}=1.
\]
Thus
\[
\boxed{\operatorname{rank}j(\langle z\rangle)=1,\qquad
\dim(\overline R/j(\langle z\rangle))=3.}
\]
This is a constant-degree, exact symbolic test requiring one nontrivial Hilbert-symbol evaluation. It falsifies an implementation returning zero obstruction for \(z\). Passing it establishes nothing asymptotic.

## 5. Costs and remaining proof obligations

After the inherited integer factorization and the accepted native local construction:

* \(D\), all local-frame dimensions and the relevant matrix sizes are polynomial in native \(n,B\).
* Constructing and reading the matrices, computing \(T\), and all subsequent binary linear algebra have polynomial bit cost.
* The modulus has a polynomial-size prime-power description:
  \(\log N\mathfrak m\) is polynomial in the native parameters. Enumerating residue classes up to \(N\mathfrak m\), however, is not permitted.
* Ray-class coordinates, global characters, principal-ideal generators and unit residue images are not input advice.
* No quantum state preparation is used in this classical route. The output integer requires \(O(\log(D+1))\) bits.

A successful direct-dimension shortcut still needs one of the following:

1. **A native rigidity theorem:** the computable local, norm and genus data force the same \(\dim(L\cap\mathcal C)\) for every genuinely realizable remaining global image.
2. **A constructive rank algorithm:** for example, the constrained ray-class operation above, with polynomial bit bounds and no unpaid globalization or search.
3. **A genuine native counterexample to a proposed invariant formula:** two native instances with matching claimed sufficient data but different exact dimensions. The formal completions above do not establish this.

**Conclusion.** Reciprocity gives a self-dual global image, and genus theory supplies substantial rank information. Neither the exact duality sequence nor norm compatibility supplies its remaining orientation. The direct attack survives as a constrained ray-class rank problem, with a concrete input/output specification and an exact small falsifier. Its polynomial classical complexity remains unresolved; no hardness or quantum speedup follows.