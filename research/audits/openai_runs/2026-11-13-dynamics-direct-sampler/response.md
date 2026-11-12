## Status

I do **not** close the unrestricted \(\operatorname{poly}(D,L,b)\) obligation. I do obtain a complete native sampler for a substantial growing family:

> **Proved here:** if \(h=\ell(\mu)\) is the number of bosons in the input, the full real-time occupation law can be sampled within TV \(2^{-b}\) in
> \[
> (D+1)^{O(h)}\operatorname{poly}(D,L,b)
> \]
> BIT time, without coefficient advice or an eigenstate sampler.
>
> In particular, this is polynomial for every fixed \(h\), at arbitrary rational time. The output occupation is unrestricted; its length need not be bounded.

The exact remaining growing parameter is \(h\). The construction retains the entire square of the coherent sum. Its ingredients are the supplied diagonalization, Cauchy/Pieri identities, and principal-specialization formula; no unchecked literature input is needed.

## 1. First falsification: diagonalizing the probability kernel is wrong

A direct degree-two calculation rules out replacing the coherent law by the dephased spectral mixture.

Write \(r_k=1+t^k+t^{2k}\). In degree two, eigenvectors are proportional to
\[
g_2=\frac{p_1^2}{2r_1^2}+\frac{p_2}{2r_2},
\qquad
e_2=\frac{p_1^2-p_2}{2}.
\]
Their Hall inner product is zero. Consequently,
\[
P_{(2),\tau}(1,1)
=
\frac{4r_1^2r_2}{(r_1^2+r_2)^2}
\sin^2\!\bigl(\pi\tau(E_{(2)}-E_{(1,1)})\bigr).
\]

At the contract parameters for \(D=2\),
\[
r_1=\frac{19}{9},\quad r_2=\frac{133}{81},\quad
E_{(2)}=\frac{665}{64},\quad E_{(1,1)}=\frac{95}{24}.
\]
Thus
\[
\boxed{
P_{(2),\tau}(1,1)
=\frac{133}{169}
\sin^2\!\left(\frac{1235\pi}{192}\tau\right).
}
\]
At the nonzero rational time \(\tau=192/1235\), this probability is exactly zero. The dephased mixture instead gives the constant \(133/338\).

This falsifies the proposed diagonal-kernel shortcut, not the existence of an unrestricted classical sampler. Global Cauchy orthogonality cannot be reused after restricting the output occupation.

---

## 2. A bounded-hook invariant space for few-boson inputs

All objects below use the **same global** \(t=D/(D+1)\), \(q=t^3\), including objects of degree less than \(D\).

Define the row and column generators
\[
G(x)=\sum_{n\ge0}g_nx^n
=\exp\!\left(\sum_{k\ge1}\frac{p_kx^k}{kr_k}\right),
\]
\[
E(y)=\sum_{n\ge0}e_ny^n
=\exp\!\left(\sum_{k\ge1}\frac{(-1)^{k-1}p_ky^k}{k}\right).
\]
For nonnegative \(r,s\), let
\[
\mathcal S_{r,s}^{(n)}
=
\operatorname{span}\left\{
g_{a_1}\cdots g_{a_r}e_{b_1}\cdots e_{b_s}:
\sum_i a_i+\sum_j b_j=n
\right\}.
\]

### Lemma: exact bounded-hook span

For \(0<q,t<1\),
\[
\boxed{
\mathcal S_{r,s}^{(n)}
=
\operatorname{span}\{P_\lambda:|\lambda|=n,\ \lambda_{r+1}\le s\}.
}
\tag{1}
\]

**Forward inclusion.** Repeated horizontal-strip Pieri multiplication by \(r\) row generators produces only shapes of length at most \(r\). Each subsequent elementary generator adds a vertical strip, increasing any row length by at most one. After \(s\) such factors, every row below row \(r\) has length at most \(s\).

**Reverse inclusion.** First, the Cauchy identity in \(r\) finite variables shows that the products of \(r\) row generators span all \(P_\alpha\) with \(\ell(\alpha)\le r\).

For a hook-admissible \(\lambda\), write
\[
\alpha=(\lambda_1,\ldots,\lambda_r),\qquad
\beta=(\lambda_{r+1},\lambda_{r+2},\ldots).
\]
Consider
\[
F_\lambda=P_\alpha\prod_{j=1}^{s}e_{\beta'_j}.
\]
Every shape \(\nu\) in its Pieri expansion has at most \(|\beta|\) boxes below row \(r\). If it has exactly \(|\beta|\), its first \(r\) rows remain \(\alpha\). Its tail \(\gamma\) satisfies, for every \(k\),
\[
\sum_{i=1}^{k}\gamma_i
\le
\sum_{j=1}^{s}\min(k,\beta'_j)
=
\sum_{i=1}^{k}\beta_i.
\]
Hence \(\gamma\) is dominated by \(\beta\). The target \(\beta\) occurs by adding its columns in order; the corresponding valid-strip coefficients are strictly positive. Ordering first by tail size and then by tail dominance gives an invertible triangular system. This proves (1).

No content-gap division is involved.

### Selection rule for \(p_\mu\), without an invalid specialization inference

The supplied principal-specialization formula gives, in degree \(n\),
\[
[p_n]J_\lambda
=
\frac{1-t^n}{n}
\prod_{\substack{(i,j)\in\lambda\\(i,j)\ne(0,0)}}(t^i-q^j).
\tag{2}
\]
At \(q=t^3\), this vanishes exactly when \(\lambda_4\ge2\). Orthogonality therefore gives
\[
p_n\in\mathcal S_{3,1}^{(n)}.
\]

Now use multiplication of the actual spanning representations:
\[
\mathcal S_{r,s}\mathcal S_{r',s'}
\subseteq\mathcal S_{r+r',s+s'}.
\]
For \(\mu=(\mu_1,\ldots,\mu_h)\),
\[
\boxed{
p_\mu=\prod_{a=1}^{h}p_{\mu_a}
\in\mathcal S_{3h,h}^{(D)}.
}
\tag{3}
\]
This is a product-of-spans argument, not an inference about individual length-\(h\) coefficients from a univariate specialization zero.

By (1), this space is invariant under \(H\). Its Macdonald labels satisfy
\[
\lambda_{3h+1}\le h.
\]
For fixed \(h\), their number is polynomial in \(D\).

---

## 3. Native Gram and Hamiltonian kernels

Set \(r=3h\), \(s=h\), \(v=r+s=4h\). Introduce
\[
Z=(x_1,\ldots,x_r,y_1,\ldots,y_s),
\]
and define
\[
A_k(Z)=\frac1{r_k}\sum_{i=1}^{r}x_i^k
       +(-1)^{k-1}\sum_{j=1}^{s}y_j^k,
\]
\[
\mathcal F(Z;p)
=\exp\!\left(\sum_{k\ge1}\frac{p_kA_k(Z)}k\right).
\]
For a multi-index \(a\) of total degree \(D\), put
\[
f_a=[Z^a]\mathcal F.
\]
These are exactly the row/column products spanning \(\mathcal S_{r,s}^{(D)}\).

Define
\[
C_k(Z,W)=\frac{r_k}{k}A_k(Z)A_k(W).
\]
The full Hall contraction is
\[
\boxed{
K(Z,W)=\langle\mathcal F(Z),\mathcal F(W)\rangle
=\exp\!\left(\sum_{k\ge1}C_k(Z,W)\right).
}
\tag{4}
\]
Therefore
\[
G_{ab}=[Z^aW^b]K=\langle f_a,f_b\rangle.
\]

This kernel has an explicit factorization. If
\[
C(u)=\exp\!\left(\sum_{k\ge1}\frac{u^k}{kr_k}\right),
\]
then
\[
\begin{aligned}
K={}&
\prod_{i,i'}C(x_ix'_{i'})
\prod_{i,j}(1+x_i y'_j)
\prod_{j,i'}(1+y_jx'_{i'})\\
&\times
\prod_{j,j'}\prod_{c=0}^{2}(1-t^c y_jy'_{j'})^{-1}.
\end{aligned}
\tag{5}
\]
There is no infinite-product oracle: coefficients of \(C(u)=\sum c_nu^n\) through degree \(D\) follow from
\[
c_0=1,\qquad
n c_n=\sum_{k=1}^{n}\frac{c_{n-k}}{r_k}.
\]

### Computing the native Hamiltonian, not importing its eigenvectors

The supplied vertex definition gives
\[
V^*(u)=\exp\!\left(\sum_{k\ge1}(1-q^k)u^k\partial_{p_k}\right).
\]
Hence
\[
V^*(u)\mathcal F(Z;p)=B(u;Z)\mathcal F(Z;p),
\]
where
\[
\boxed{
B(u;Z)=
\prod_{i=1}^{r}\frac{1-tx_i u}{1-x_i u}
\prod_{j=1}^{s}\frac{1+y_j u}{1+q y_j u}.
}
\tag{6}
\]
Writing \(B_n=[u^n]B\), the Hamiltonian form matrix is
\[
\mathsf H_{ab}
=
[Z^aW^b]\,
\frac{K(Z,W)}{1-t}
\sum_{n=1}^{D}q^{-n}B_n(Z)B_n(W).
\tag{7}
\]

There is a convenient finite implementation. Every monomial of \(K\) has equal total degree in \(Z\) and \(W\). Since \(|a|=|b|=D\),
\[
\boxed{
\mathsf H_{ab}
=
[Z^aW^b]\,
\frac{K(Z,W)}{1-t}
\bigl(B(q^{-1};Z)B(1;W)-1\bigr).
}
\tag{8}
\]
Terms with different \(B\)-degrees cannot contribute. The rational factors in (6) are expanded formally only through degree \(D\).

### Paid preprocessing

1. Enumerate the degree-\(D\) product generators.
2. Compute their Gram matrix from (4).
3. Select an independent subset by exact rational elimination. Its Gram matrix \(G\) is positive definite.
4. Compute \(\mathsf H\) from (8), and form the coordinate matrix
   \[
   M=G^{-1}\mathsf H.
   \]
5. Enumerate the hook labels \(\lambda_{r+1}\le s\) and their exact rational \(E_\lambda\).
6. Group equal eigenvalues **exactly**. For each distinct \(E\), compute
   \(\ker(M-EI)\) by rational elimination. Combining these bases gives a rational eigenvector matrix.

This uses neither a Macdonald coefficient table nor normalized eigenvector advice. It also does not divide by differences of coincident eigenvalues.

The input coordinates are native and explicit:
\[
[p_\mu]\mathcal F(Z;p)
=
\prod_{k=1}^{D}\frac{A_k(Z)^{m_k}}{k^{m_k}m_k!},
\tag{9}
\]
so
\[
\langle f_a,p_\mu\rangle
=
R_\mu[Z^a]\prod_k\frac{A_k(Z)^{m_k}}{k^{m_k}m_k!}.
\]
Solving with \(G\) gives the coordinates of \(p_\mu\). Membership (3) makes this an exact representation, not an orthogonal approximation.

Apply the spectral phases in these coordinates. Below, \(w_a\) denotes the resulting coefficients, with phases replaced by certified dyadic approximations:
\[
\widetilde f=\sum_a w_a f_a.
\]

---

## 4. Full-square contraction and every sequential conditional

This is the essential sampling step.

For a prefix \(n_1,\ldots,n_j\), define
\[
\boxed{
K_{\mathbf n,j}(Z,W)
=
\left(\prod_{k=1}^{j}\frac{C_k(Z,W)^{n_k}}{n_k!}\right)
\exp\!\left(\sum_{k=j+1}^{D}C_k(Z,W)\right).
}
\tag{10}
\]
Direct expansion gives
\[
[Z^aW^b]K_{\mathbf n,j}
=
\sum_{\substack{\nu\vdash D\\m_k(\nu)=n_k,\ k\le j}}
R_\nu\,[p_\nu]f_a\,[p_\nu]f_b.
\tag{11}
\]

Thus the **unnormalized prefix probability** is
\[
\boxed{
W_{\mathbf n,j}
=
\sum_{a,b}w_a\overline{w_b}
[Z^aW^b]K_{\mathbf n,j}.
}
\tag{12}
\]
All cross terms are present. This is a positive-semidefinite Gram contraction even though intermediate polynomial coefficients can have signs.

At the root,
\[
W_{\varnothing,0}=\|\widetilde f\|^2.
\]
For each prefix,
\[
W_{\mathbf n,j-1}
=
\sum_{c=0}^{\lfloor d/j\rfloor}W_{(\mathbf n,c),j},
\tag{13}
\]
where \(d\) is the remaining weighted degree. Hence normalization is obtained internally.

### A usable recurrence

Maintain the truncated kernel for the chosen prefix before mode \(j\):
\[
Q=\left(\prod_{k<j}\frac{C_k^{n_k}}{n_k!}\right)
   \exp\!\left(\sum_{k\ge j}C_k\right).
\]
Compute
\[
T_0=\operatorname{trunc}(e^{-C_j}Q),
\qquad
T_c=\operatorname{trunc}\!\left(\frac{C_jT_{c-1}}c\right).
\tag{14}
\]
The contraction (12) applied to \(T_c\) is the weight for \(m_j=c\). Sample \(c\), retain \(T_c\), and continue.

Here truncation means total degree at most \(D\) separately in each copy. Each \(C_j\) has at most \(v^2\) monomials, and
\[
e^{-C_j}
=\sum_{m=0}^{\lfloor D/j\rfloor}\frac{(-C_j)^m}{m!}
\]
is sufficient.

This is a deterministic coefficient recurrence supplying every conditional. There is no estimator variance to bound. It sums over all occupation outputs without enumerating them.

---

## 5. Finite BIT costs and accuracy

### Exact arithmetic size

Let
\[
S=(D+1)^v,\qquad v=4h.
\]
A single-copy coefficient array has at most \(S\) entries, and a two-copy array at most \(S^2\). The number of degree-\(D\) generators is at most \(S\).

A conservative common bound on the initial rational-data bit lengths is
\[
B_0=O\!\left((D+v+1)^3\log(D+2)\right).
\tag{15}
\]
This includes Gram entries, Hamiltonian entries, input coordinates before solving, and eigenvalues.

For example, writing
\[
r_k=\frac{s_k}{(D+1)^{2k}},
\qquad \log_2 s_k=O(k\log(D+2)),
\]
the coefficients of \(C_k\) have common denominator dividing
\[
d_k=k\,s_k(D+1)^{2k}.
\]
A common denominator for all truncated exponential-kernel coefficients divides
\[
\prod_{k=1}^{D}
d_k^{\lfloor D/k\rfloor}
\bigl(\lfloor D/k\rfloor!\bigr),
\]
whose bit length is \(O(D^2\log(D+2))\). Coefficient magnitudes, and the additional rational factors in (8), fit within (15). This also controls the signed intermediate calculations in (14).

Fraction-free elimination gives:

- coordinate-matrix entries with \(O(SB_0)\) bits;
- integer bases for its rational eigenspaces with \(O(S^2B_0)\) bits;
- transformed state coefficients with
  \[
  B=O(S^3B_0+b+L+1)
  \tag{16}
  \]
  bits.

These deliberately loose bounds charge the conditioning of the chosen algebraic basis through exact integer sizes, rather than assuming well-conditioned floating-point eigenvectors.

Using schoolbook integer arithmetic, one conservative total bound is
\[
\boxed{
O\!\left(
(S^4+v^2D^2S^2)B^2
+
S(L+B_0+b+1)^4
\right)
}
\tag{17}
\]
BIT operations, plus input/output and random-bit handling. Storage is \(O(S^2B)\) bits.

The \(S^4\) term pays for all exact eigenspace calculations. The \(v^2D^2S^2\) term pays for kernel construction, prefix updates, and all candidate contractions. Thus (17) is
\[
(D+1)^{O(h)}\operatorname{poly}(D,L,b).
\]

### Time and phase precision

Every eigenvalue has denominator dividing the explicit integer
\[
Q_D=D^{3D}(D+1)^{D-1}.
\]
Its bit length is \(O(D\log(D+2))\). Compute \(\tau E\bmod1\) exactly, using integers of \(O(L+D\log(D+2))\) bits, before approximating the phase.

Choose dyadic \(\widetilde z_E\) satisfying
\[
|\widetilde z_E-e^{-2\pi i\tau E}|
\le\delta,\qquad
\delta=2^{-(b+4)}.
\]
Certified elementary series evaluation suffices in polynomial bit time. Equal eigenvalues receive the same approximate phase.

Let \(f=e^{-2\pi i\tau H}p_\mu\). Orthogonality of distinct eigenspaces gives
\[
\|\widetilde f-f\|
\le\delta\sqrt{R_\mu}.
\]
After normalization,
\[
\left\|
\frac{\widetilde f}{\|\widetilde f\|}
-\frac{f}{\sqrt{R_\mu}}
\right\|
\le2\delta.
\]
Therefore their occupation laws differ in TV by at most \(2\delta\). This bound does not depend on the number of eigenvalues or on \(|\tau|\).

As an exact consistency check, \(\tau=Q_D\) gives a full revival for every input.

### Bounded-clock conditional sampling

After phase approximation, all weights in (12) are exact nonnegative rationals. Clear their common denominators and compare integer cumulative weights.

At each of the \(D\) stages use
\[
R=b+\left\lceil\log_2\!\bigl(8D(D+1)\bigr)\right\rceil
\]
uniform random bits. There are at most \(D+1\) candidate counts, so finite-CDF rounding contributes at most
\[
D(D+1)2^{-R}\le 2^{-b}/8
\]
in TV over the whole sequential sampler. Together with phase error, the total is below \(2^{-b}\).

Rare prefixes do not demand uncharged numerical precision: their conditional weights are handled by exact rational arithmetic.

The algorithm uses \(O(D(b+\log D))\) random bits and pays \(O(D\log(D+2))\) output bits in the worst case. Input loading and the conversion (9) are included; no state or coefficient preparation is free.

---

## 6. Exact limits of the construction and the unpaid contraction

### A growing-family falsifier of a fixed-hook extension

For input \(\mu=(1^D)\), every Macdonald label has nonzero overlap.

Indeed, \(p_1=r_1g_1\), and repeated one-box Pieri multiplication has strictly positive coefficients along every valid Young-tableau chain. Thus \(p_1^D\) has a nonzero \(P_\lambda\) component for every \(\lambda\vdash D\).

Consequently, no fixed hook cutoff can cover all explicit occupation inputs. This exactly falsifies extending the above support argument with \(r,s\) bounded independently of \(\mu\). It is **not** a hardness statement: full spectral support does not preclude a compressed algorithm.

A related exact check applies to universal low-rank conditional kernels. In the normalized eigenbasis,
\[
C^{(0)}_{\lambda\kappa}
=\sum_{\nu:m_1(\nu)=0}U_{\nu\lambda}U_{\nu\kappa}
\]
satisfies
\[
C^{(0)}=U^{\mathsf T}\Pi_{m_1=0}U,\qquad
\operatorname{rank}C^{(0)}=p(D)-p(D-1).
\]
This rank is already exponentially large in \(\sqrt D\): choose arbitrary subsets of even parts up to order \(\sqrt D\), then fill the remaining even degree with \(2\)'s, reserving a \(3\) when needed for parity. Hence a universally polynomial-rank factorization is not a valid shortcut. Structured high-rank contraction remains possible.

### Smallest unpaid contraction

In the product-generator representation, even the first nontrivial marginal is the explicit contraction
\[
\boxed{
\Pr(m_1=0)
=
\frac{
\displaystyle\sum_{a,b}w_a\overline{w_b}
[Z^aW^b]\bigl(e^{-C_1(Z,W)}K(Z,W)\bigr)
}{
\displaystyle\sum_{a,b}w_a\overline{w_b}
[Z^aW^b]K(Z,W)
}.
}
\tag{18}
\]
Here \(w\) must be generated from the explicit \(\mu,\tau\), not supplied as advice. Equations (10) and (14) give the exact extensions needed for every subsequent conditional.

For bounded \(h\), the construction above pays both phase evolution and this contraction. For unbounded \(h\), it pays them with arrays of size up to \((D+1)^{8h}\), and dense algebra of corresponding size. Taking the better of this algorithm and the admitted \(\exp(O(\sqrt D))\) baseline does not establish a polynomial unrestricted bound.

**Next decisive question:** can the phase-evolved coefficient functional in (18), together with the prefix updates (14), be represented and contracted in \(\operatorname{poly}(D,L,b)\) bit time when \(h\) grows—without supplying that functional or its normalization as an oracle?

That is the unresolved contraction. The finite interference example, full-support example, and rank calculation delimit particular shortcuts; none establishes classical hardness or a quantum advantage.