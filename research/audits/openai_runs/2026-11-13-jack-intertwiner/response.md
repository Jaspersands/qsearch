## Verdict: the identity is true in every degree

At \(\alpha=3\), with the conventions and normalization in the contract,
\[
\boxed{\quad
\forall d\ge0,\ \forall\lambda\vdash d,\ \forall s\in A_\lambda:
\qquad A_d\psi_{\lambda,s}=J_{\lambda+s}.
\quad}
\]

The proof below uses the supplied paper’s **full hierarchy theorem, Theorem 2.2**, as well as Theorem 1.4. It does **not** assume a Pieri rule, simplicity of the global Lax spectrum, or simplicity of the Jack Hamiltonian spectrum. No additional source theorem is needed.

The essential additional algebraic lemma is a commuting lift of the content-sum Hamiltonian; it is proved below. The degree-three control is not used.

All operator calculations take place in finite homogeneous components, so the resolvent identities are identities of rational matrices.

---

## 1. A Hamiltonian supplied by the hierarchy

Write \(p_k=V_k\), \(V_{-k}=3k\partial_{p_k}\), and
\[
\mathcal H_d=\mathcal F[w]_d,\qquad
E=\sum_{k\ge1}k p_k\partial_{p_k},\qquad
C_\lambda=\sum_{t\in\lambda}c(t).
\]

Define, on \(\mathcal F\),
\[
H=\frac16\,\pi_0L^3\big|_{\mathcal F}-E.
\]
Equation (2.1) of the supplied paper gives
\[
H=
\frac12\sum_{a,b\ge1}(a+b)p_ap_b\partial_{p_{a+b}}
+\frac32\sum_{a,b\ge1}ab\,p_{a+b}\partial_{p_a}\partial_{p_b}
+\sum_{k\ge1}k(k-1)p_k\partial_{p_k}.
\tag{1}
\]

Theorem 2.2 gives
\[
T_\lambda(u)=
\frac1u\prod_{t\in\lambda}
\frac{(u-c(t))(u-c(t)-2)}
     {(u-c(t)-3)(u-c(t)+1)}.
\tag{2}
\]
Expanding each factor at infinity yields
\[
T_\lambda(u)
=u^{-1}+3|\lambda|u^{-3}
 +6(C_\lambda+|\lambda|)u^{-4}+O(u^{-5}).
\]
Consequently,
\[
HJ_\lambda=C_\lambda J_\lambda.
\tag{3}
\]
Also, \(H\) is self-adjoint: \(\pi_0L^3|_{\mathcal F}\) is an orthogonal compression of a self-adjoint operator, and \(E\) is self-adjoint.

No simplicity assertion about the numbers \(C_\lambda\) is being made.

---

## 2. The missing commuting lift

Let \(N=w\partial_w\), and extend \(H\) coefficientwise to \(\mathcal F[w]\). Define
\[
\widehat H
=
H+N(N-1)
+\sum_{k\ge1}
\left(
V_{-k}w^kN+
p_kN\pi w^{-k}
\right).
\tag{4}
\]
The two summands inside each parenthesis are adjoints. Thus \(\widehat H\) is self-adjoint on every \(\mathcal H_d\), and
\[
\widehat H\big|_{\mathcal F}=H.
\]

### Lemma 1: the raising intertwiner

For every \(d\ge0\),
\[
\boxed{\quad H_{d+1}A_d=A_d(\widehat H_d+L_d).\quad}
\tag{5}
\]

**Proof.** Directly from (1),
\[
[H,p_m]
=
\frac m2\sum_{\substack{a,b\ge1\\a+b=m}}p_ap_b
+m\sum_{k\ge1}p_{m+k}V_{-k}
+m(m-1)p_m.
\tag{6}
\]

Apply \(A(\widehat H+L)\) to \(fw^\ell\), and put \(m=\ell+1\). Its diagonal contribution is
\[
p_mHf+\ell(\ell+1)p_mf.
\]
Its raising contribution is
\[
(\ell+1)\sum_{k\ge1}p_{\ell+k+1}V_{-k}f,
\]
and its lowering contribution is
\[
\sum_{k=1}^{\ell}(\ell-k+1)p_kp_{\ell-k+1}f
=\frac{\ell+1}{2}\sum_{a+b=\ell+1}p_ap_bf.
\]
Together these equal \(p_mHf+[H,p_m]f=H(p_mf)\), proving (5). ∎

### Lemma 2: the lift commutes with \(L\)

For every \(d\ge0\),
\[
\boxed{\quad[\widehat H_d,L_d]=0.\quad}
\tag{7}
\]

**Proof.** Under the orthogonal decomposition
\[
\mathcal H_{d+1}=\mathcal F_{d+1}\oplus w\mathcal H_d,
\]
the native block identity is
\[
L_{d+1}=
\begin{pmatrix}
0&A_d\\
A_d^\dagger&L_d+2
\end{pmatrix}.
\tag{8}
\]
Definition (4) also gives
\[
\widehat H_{d+1}=
\begin{pmatrix}
H_{d+1}&0\\
0&\widehat H_d+L_d
\end{pmatrix}.
\tag{9}
\]
For example, shifting \(fw^\ell\) to \(fw^{\ell+1}\) changes the diagonal term by \(2\ell\), the raising coefficient from \(\ell\) to \(\ell+1\), and each surviving lowering coefficient from \(\ell-k\) to \(\ell-k+1\). These changes are exactly \(L_d\); the lowering term reaching \(w^0\) has coefficient zero.

By (5) and its adjoint, the off-diagonal blocks of the commutator vanish. Hence
\[
[\widehat H_{d+1},L_{d+1}]
=
\begin{pmatrix}
0&0\\
0&[\widehat H_d,L_d]
\end{pmatrix}.
\]
The degree-zero commutator is zero, proving the assertion by induction. ∎

Since \(\widehat HJ_\lambda=HJ_\lambda=C_\lambda J_\lambda\) and \(\widehat H\) commutes with \(L\), it acts as \(C_\lambda I\) on the entire cyclic space \(Z_\lambda\). Therefore (5) implies
\[
H A_d\psi_{\lambda,s}
=(C_\lambda+c(s))A_d\psi_{\lambda,s}.
\tag{10}
\]

This is useful but **not yet sufficient**: \(H\) itself has degeneracies—for example,
\[
C_{(4,1,1)}=C_{(3,3)}=15.
\]

---

## 3. A resolvent identity forces the full child label

Let \(i_d:\mathcal F_d\hookrightarrow\mathcal H_d\) be inclusion, and write
\[
T_d(u)=\pi_0(u-L_d)^{-1}i_d.
\]
Let \(M\) denote multiplication by \(p_1\), and \(S\) multiplication by \(w\). Directly from the native \(L\),
\[
L_{d+1}M-ML_d=3S.
\tag{11}
\]
The resolvent commutator consequently gives
\[
(u-L_{d+1})^{-1}M-M(u-L_d)^{-1}
=3(u-L_{d+1})^{-1}S(u-L_d)^{-1}.
\]
The upper-right block of the inverse of (8) is
\[
\pi_0(u-L_{d+1})^{-1}S
=T_{d+1}(u)A_d(u-L_d-2)^{-1}.
\]
Thus
\[
T_{d+1}(u)p_1-p_1T_d(u)
=
3T_{d+1}(u)A_d
(u-L_d-2)^{-1}(u-L_d)^{-1}i_d.
\tag{12}
\]

Fix \(\lambda\vdash d\). Expand over **all** \(\mu\vdash d+1\):
\[
A_d\psi_{\lambda,s}=\sum_\mu a_{\mu s}J_\mu,
\qquad
p_1J_\lambda=\sum_\mu b_\mu J_\mu.
\tag{13}
\]
No Pieri support is assumed.

Theorem 1.4 gives
\[
J_\lambda=\sum_{s\in A_\lambda}\tau_{\lambda s}\psi_{\lambda,s},
\qquad \tau_{\lambda s}>0.
\]
Since \(A_di_d=p_1\),
\[
b_\mu=\sum_s\tau_{\lambda s}a_{\mu s}.
\tag{14}
\]
Applying (12) to \(J_\lambda\) and taking its \(J_\mu\)-coefficient gives
\[
b_\mu\bigl(T_\mu(u)-T_\lambda(u)\bigr)
=
3T_\mu(u)\sum_s
\frac{\tau_{\lambda s}a_{\mu s}}
     {(u-c(s))(u-c(s)-2)}.
\tag{15}
\]

Now (10) implies
\[
a_{\mu s}\ne0
\quad\Longrightarrow\quad
C_\mu-C_\lambda=c(s).
\tag{16}
\]
For fixed \(\lambda,\mu\), **at most one** \(s\in A_\lambda\) can satisfy this, because addable-corner contents within \(\lambda\) are distinct.

Suppose \(a_{\mu s}\ne0\). Equations (14)–(16) give
\(b_\mu=\tau_{\lambda s}a_{\mu s}\ne0\). Dividing (15), as a rational-function identity, yields
\[
1-\frac{T_\lambda(u)}{T_\mu(u)}
=\frac{3}{(u-c(s))(u-c(s)-2)}.
\]
Therefore
\[
T_\mu(u)
=
T_\lambda(u)
\frac{(u-c(s))(u-c(s)-2)}
     {(u-c(s)-3)(u-c(s)+1)}
=
T_{\lambda+s}(u),
\tag{17}
\]
where the final equality is exactly the box-product formula (2).

It remains to justify that equality of these transfer eigenvalues identifies the partition—even at rational \(\alpha=3\).

---

## 4. The full transfer eigenvalue separates partitions

Let a nonempty partition have distinct row lengths
\[
\ell_1>\ell_2>\cdots>\ell_m>0
\]
with multiplicities \(n_i\), and put
\(h_i=n_1+\cdots+n_i\), \(h_0=0\).

Its addable-corner contents and shifted-removable-corner contents are respectively
\[
a_i=3\ell_i-h_{i-1}\quad(1\le i\le m),
\qquad a_{m+1}=-h_m,
\]
and
\[
b_i=3\ell_i-h_i\quad(1\le i\le m).
\]
They satisfy
\[
a_i>b_i>a_{i+1}.
\]
Consequently, the corner formula in Theorem 2.2,
\[
T_\lambda(u)=
\frac{\prod_{i=1}^m(u-b_i)}
     {\prod_{i=1}^{m+1}(u-a_i)},
\]
has no cancellations. Its ordered poles and zeros recover
\[
n_i=a_i-b_i,\qquad
\ell_i-\ell_{i+1}=\frac{b_i-a_{i+1}}3,
\qquad \ell_{m+1}=0.
\]
Thus
\[
T_\mu(u)=T_\nu(u)\quad\Longrightarrow\quad\mu=\nu.
\tag{18}
\]
The empty partition is separately identified by \(T_\varnothing(u)=1/u\).

Combining (17) and (18), every nonzero coefficient in (13) has
\(\mu=\lambda+s\). Hence
\[
A_d\psi_{\lambda,s}=\gamma_{\lambda s}J_{\lambda+s}.
\]

Finally, write
\[
\psi_{\lambda,s}=\sum_{\ell\ge0}f_\ell w^\ell,
\qquad f_0=J_\lambda.
\]
In
\[
A_d\psi_{\lambda,s}=\sum_{\ell\ge0}p_{\ell+1}f_\ell,
\]
only \(\ell=0\) can contribute to \(p_1^{d+1}\). Its coefficient is therefore \(1\). The stipulated normalization gives the same coefficient \(1\) in \(J_{\lambda+s}\). Thus \(\gamma_{\lambda s}=1\), completing the proof.

As a consequence—not an input—the one-box Pieri relation follows:
\[
p_1J_\lambda
=\sum_{s\in A_\lambda}\tau_{\lambda s}J_{\lambda+s}.
\tag{19}
\]

---

## 5. Degeneracy counterexample and native-projector consequence

### Exact counterexample to content-only identification

There is no counterexample to the quantified identity above. There is, however, an explicit counterexample to the weaker shortcut “an \(L\)-eigenvector maps to a single Jack.”

In degree four, both
\[
\psi_{(2,2),(2,0)}
\quad\text{and}\quad
\psi_{(2,1,1),(2,0)}
\]
have content \(6\). Therefore their sum \(v\) satisfies
\[
L_4v=6v,
\qquad
A_4v=J_{(3,2)}+J_{(3,1,1)},
\]
which is not a single Jack. The canonical parent label matters. The proof above resolves this degeneracy through (16)–(18), not through spectral simplicity.

### The native \(P_A\) preserves the proposed child space

For every \(\mu\vdash d+1\), define exactly the contract’s space
\[
Y_\mu=\operatorname{span}
\{\psi_{\mu-r,r}:r\in R_\mu\}.
\]
The supplied orthogonality theorem and the edge-indexing bijection give an orthogonal decomposition
\[
\mathcal H_d=\bigoplus_{\mu\vdash d+1}Y_\mu.
\]
The proved identity gives \(A_dY_\mu=\mathbb C J_\mu\). By adjointness and Jack orthogonality,
\[
A_d^\dagger J_\mu\in Y_\mu.
\]
Moreover,
\[
A_dA_d^\dagger
=\sum_{k\ge1}3k p_k\partial_{p_k}
=3(d+1)I.
\]
Hence
\[
P_A\psi_{\mu-r,r}
=\frac{A_d^\dagger J_\mu}{3(d+1)}\in Y_\mu.
\]
Thus \(P_A\), every exact content projector of \(L_d\), and their complementary projectors preserve \(Y_\mu\). No additional Jack projector is needed for this **exact algebraic invariant-space issue**.

## Scientific action

**Close obligation 1 as proved.** The necessary advance beyond the elementary block identity is the commuting lift (4)–(7), followed by the full hierarchy argument—not further finite sweeps or an unsupplied Pieri theorem.

The uniform-overlap and approximate-measurement/runtime obligations remain **OPEN and unaddressed here**. This establishes the algebraic identity and exact native invariant spaces, not a preparation algorithm or efficiency claim.