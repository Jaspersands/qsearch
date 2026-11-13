## Result

For the **written contract, with both Durfee bounds fixed**, the proposed specialization yields a deterministic exact algorithm. A conservative bound is
\[
\boxed{\;
O_{d,e}\!\left((n+1)^{\,8(d+e)+2\max(d,e)+10}\right)
\quad\text{bit operations}.
\;}
\]
This deliberately loose bound includes constructing every required polynomial, handling length-\(n\) Jacobi–Trudi determinants, extracting the coefficient, and writing the answer. No character-table input, advice, or supermodule semisimplicity is used.

### 1. The specialization preserves ordinary Kronecker coefficients

All variables below are **commuting indeterminates**; “odd” specifies the symmetric-function specialization, not Grassmann multiplication.

Write \(\epsilon_r=(-1)^{r-1}\). For the stated tensor alphabet \(T=X\mathbin{\mathrm{tensor}}Z\),
\[
\begin{aligned}
p_r(T)
&=\sum_{i,j}(x_i u_j)^r+\sum_{i,j}(y_i v_j)^r\\
&\quad+\epsilon_r\left(\sum_{i,j}(x_i v_j)^r+\sum_{i,j}(y_i u_j)^r\right)\\
&=\left(\sum_i x_i^r+\epsilon_r\sum_i y_i^r\right)
  \left(\sum_j u_j^r+\epsilon_r\sum_j v_j^r\right).
\end{aligned}
\]
The positive sign on the \(y_i v_j\) terms is essential and follows from \(\epsilon_r^2=1\).

Here is an ordinary symmetric-function proof of the coefficient identity. Define
\[
\Delta_*p_r=p_r\otimes p_r
\]
and extend multiplicatively over \(\mathbb Q\). Frobenius’s character formula gives
\[
s_\nu=\sum_{\rho\vdash n}\frac{\chi^\nu(\rho)}{z_\rho}p_\rho.
\]
Using \(p_\rho=\sum_{\alpha\vdash n}\chi^\alpha(\rho)s_\alpha\), the coefficient of \(s_\alpha\otimes s_\beta\) in \(\Delta_*s_\nu\) is
\[
\sum_{\rho\vdash n}
\frac{\chi^\alpha(\rho)\chi^\beta(\rho)\chi^\nu(\rho)}{z_\rho}
=g(\alpha,\beta,\nu).
\]
Consequently,
\[
hs_\nu(T)=
\sum_{\alpha,\beta\vdash n}
g(\alpha,\beta,\nu)\,hs_\alpha(X)hs_\beta(Z).
\tag{1}
\]

These character sums establish correctness only: **the algorithm never evaluates them or enumerates their indexing partitions**.

The specialization also gives
\[
\sum_{r\ge0}h_r(X)t^r
=\exp\!\left(\sum_{r\ge1}p_r(X)t^r/r\right)
=\frac{\prod_i(1+y_i t)}{\prod_i(1-x_i t)},
\]
so its Schur images are precisely the proposed Jacobi–Trudi polynomials. Everything follows from identities in ordinary symmetric functions. No decomposition of a supermodule is assumed.

### 2. Hook vanishing and the proposed leading monomial

For an alphabet \((x_1,\ldots,x_a\mid y_1,\ldots,y_b)\), the Jacobi–Trudi polynomial has the supertableau expansion: entries are ordered
\[
x_1<\cdots<x_a<y_1<\cdots<y_b;
\]
rows and columns are weakly increasing, even entries cannot repeat in a column, and odd entries cannot repeat in a row.

This expansion follows algebraically from the convolution of the complete-function sequences:
\[
hs_\alpha(x\mid y)
=\sum_{\tau\subseteq\alpha}s_\tau(x)s_{\alpha'/\tau'}(y).
\tag{2}
\]
Indeed, Cauchy–Binet applied to the Jacobi–Trudi convolution matrices gives (2); the ordinary skew-tableau expansion, transposed for the second factor, gives the stated filling rules. The usual determinant cancellation exchanges tails of intersecting paths, leaving the tableaux. Formula (2) is not an enumeration step in the algorithm.

An even entry \(x_i\) can occur only in rows \(1,\ldots,i\): all entries above it must be distinct, smaller even entries. Thus every cell below row \(a\) is odd. Such a row has length at most \(b\). Therefore
\[
hs_\alpha(x\mid y)=0\qquad\text{if }\alpha_{a+1}>b.
\tag{3}
\]

Now take \(a=b=d\), and order monomials lexicographically with
\[
x_1>\cdots>x_d>y_1>\cdots>y_d.
\]
For \(\alpha_{d+1}\le d\), put
\[
r_i=\alpha_i,\qquad
c_j=\max(\alpha'_j-d,0).
\]
Then
\[
\operatorname{LM}(hs_\alpha(X))
=x_1^{r_1}\cdots x_d^{r_d}y_1^{c_1}\cdots y_d^{c_d},
\qquad
\operatorname{LC}=1.
\tag{4}
\]

**Proof of the greedy assertion.** Maximizing the number of \(x_1\)'s fills the entire first row, uniquely. Conditional on this, maximizing \(x_2\) fills the second row, and so on through row \(d\). The remaining cells are odd. Maximizing \(y_1\) fills their first column, maximizing \(y_2\) fills their second column, and so on. This filling is valid because the residual width is at most \(d\), and each maximizing choice is forced.

The vector \((r,c)\) recovers the shape: append the partition \(c'\) below the first \(d\) rows. Thus different hook shapes have distinct leading monomials.

The analogous statement holds for \(Z\). In the combined variable order
\[
x_1,\ldots,x_d,y_1,\ldots,y_d,
u_1,\ldots,u_e,v_1,\ldots,v_e,
\]
the products \(hs_\alpha(X)hs_\beta(Z)\) have distinct leading monomials, all with coefficient one. They are therefore integrally linearly independent. Equations (1) and (3) establish that discarding off-hook shapes causes **no folded contributions**.

Finally,
\[
\operatorname{Durfee}(\alpha)\le d
\iff \alpha_{d+1}\le d,
\]
so these are exactly the promised shapes.

### 3. Explicit finite construction

Let
\[
q=2d+2e,\qquad m=\max(d,e),\qquad C=4de.
\]
Work in \(\mathbb Z[x,y,u,v]\).

#### Enumerate only hooks

For the \((d,d)\)-hook, enumerate tuples
\[
(r_1,\ldots,r_d,c_1,\ldots,c_d)\in\{0,\ldots,n\}^{2d}.
\]
Retain precisely those satisfying:

* both \(r\) and \(c\) are nonincreasing;
* \(\sum_i r_i+\sum_j c_j=n\);
* \(r_d\ge \#\{j:c_j>0\}\).

Append the rows of \(c'\) to \(r\), deleting trailing zeros. This produces each hook partition exactly once. Reconstruction and checking take \(O_d(n\log(n+2))\) bit operations per candidate.

Hence the retained counts satisfy
\[
N_d\le(n+1)^{2d},\qquad N_e\le(n+1)^{2e}.
\]
No enumeration of all \(p(n)\) partitions occurs.

#### Construct the complete functions

For each of \(X,Z,T\), compute \(h_0,\ldots,h_{2n}\) by truncated generating-function multiplication. Start with \(h_0=1\), all other entries zero.

For each even alphabet entry \(w\), update in ascending order:
\[
h_r\leftarrow h_r+w h_{r-1},\qquad r=1,\ldots,2n.
\]
For each odd entry \(w\), use the same update in descending order. These implement multiplication by \((1-wt)^{-1}\) and \(1+wt\), respectively.

The entries \(w\) are variables for \(X,Z\) and quadratic monomials for \(T\). Formal truncation cannot affect any required coefficient.

#### Compute all Jacobi–Trudi determinants

Compute
\[
P_\alpha=hs_\alpha(X),\qquad Q_\beta=hs_\beta(Z),\qquad F=hs_\nu(T).
\]

For a shape \(\gamma\), use its \(\ell\times\ell\) Jacobi–Trudi matrix
\[
A_{ij}=h_{\gamma_i-i+j},\qquad \ell=\ell(\gamma)\le n,
\]
with \(h_0=1\) and \(h_r=0\) for \(r<0\). Indices up to \(2n\) suffice.

Here is an explicit determinant algorithm requiring no polynomial division or pivoting. Compute
\[
s_i=\operatorname{tr}(A^i),\quad 1\le i\le\ell,
\]
by repeated ordinary matrix multiplication. Then compute
\[
c_0=1,\qquad
c_k=-\frac1k\sum_{i=1}^k c_{k-i}s_i,
\quad 1\le k\le\ell,
\tag{5}
\]
and return \((-1)^\ell c_\ell\).

Every division in (5) is **coefficientwise exact integer division**. To prove this, set
\[
D(t)=\det(I-tA)=\sum_{k=0}^{\ell}c_k t^k.
\]
The formal identity
\[
D'(t)=-D(t)\sum_{i\ge1}\operatorname{tr}(A^i)t^{i-1}
\]
gives (5). Since \(D(t)\) has integer polynomial coefficients, the numerators are divisible by \(k\).

This works for singular matrices as well. It uses \(O(n^4)\) polynomial-ring operations, not \(n!\) determinant terms.

#### Extract by triangular integer subtraction

Form the list of all \(K=N_dN_e\le(n+1)^q\) pairs and sort their leading monomials in decreasing lexicographic order.

Initialize \(R=F\). For each pair \((\alpha,\beta)\), let \(M_{\alpha\beta}\) be its leading monomial and perform
\[
a_{\alpha\beta}=[M_{\alpha\beta}]R,\qquad
R\leftarrow R-a_{\alpha\beta}P_\alpha Q_\beta.
\tag{6}
\]
Record the coefficient for the input pair \((\lambda,\mu)\).

By (1) and (4), at every step \(R\) is exactly the sum of the unprocessed basis terms. A later basis polynomial cannot contain the current leading monomial. Thus
\[
a_{\alpha\beta}=g(\alpha,\beta,\nu),
\]
and the final residual is zero. This is unitriangular elimination entirely over \(\mathbb Z\).

### 4. Intermediate sizes and bit costs

#### Complete functions and determinant intermediates

For a polynomial \(P\), let \(\|P\|_1\) be the sum of absolute coefficient values.

Each relevant alphabet has at most \(C\) letters. Consequently
\[
\|h_r\|_1\le C^r.
\]
One justification is to encode each choice contributing to \(h_r\) as a sorted word of length \(r\) over at most \(C\) letters.

Every Jacobi–Trudi entry therefore has norm at most
\[
H=C^{2n}
\]
and total degree at most \(4n\).

It is important **not** to assume determinant intermediates retain the final degree \(2n\). The bounds used here are
\[
\deg(A^i_{ab}),\deg(s_i)\le4ni,\qquad
\deg(c_k)\le4nk.
\]
Thus all mathematical polynomial intermediates have total degree at most \(4n^2\). A generic multiplication buffer with coordinate bounds \(8n^2\) suffices.

For an \(\ell\times\ell\) matrix,
\[
\|(A^i)_{ab}\|_1\le \ell^{i-1}H^i,\qquad
\|s_i\|_1\le(\ell H)^i.
\]
The coefficient \(c_k\) is a signed sum of principal minors, so
\[
\|c_k\|_1
\le { \ell\choose k}k!H^k
\le(\ell H)^k.
\]
This minor expansion is a **bound**, not an implemented enumeration. Every partial numerator in (5) has norm at most
\[
k(\ell H)^k.
\]
Partial coefficient convolutions obey the same absolute-product bounds. Hence all determinant arithmetic uses
\[
B=O_{d,e}(n^2\log(n+2))
\]
bits per integer coefficient.

There are
\[
M=(8n^2+1)^q=O_{d,e}(n^{2q})
\]
available dense coefficient positions. Schoolbook convolution and schoolbook integer arithmetic cost
\[
O(M^2B^2)
\]
bit operations per polynomial multiplication. Exact division by \(k\le n\) costs no more than this bound. Carry-safe integer packing also gives a direct bit-machine implementation of the convolution bound.

One determinant therefore costs
\[
O_{d,e}(n^{4q+8}\log^2(n+2))
\]
bit operations. There are at most
\[
1+N_d+N_e=O_{d,e}((n+1)^{2m})
\]
determinants. Complete-function construction is lower-order.

#### Final polynomials and elimination

Every nonzero determinant term for a partition of \(n\) has total complete-function index \(n\). Thus \(P_\alpha,Q_\beta\) have degree \(n\), and \(F\) and the products \(P_\alpha Q_\beta\) have degree \(2n\). They can be compressed to
\[
M_0=(2n+1)^q=O_{d,e}(n^q)
\]
coefficient positions.

The tableau interpretation gives
\[
\|F\|_1\le C^n,\qquad
\|P_\alpha Q_\beta\|_1
\le(2d)^n(2e)^n=C^n.
\]
Ordinary Kronecker coefficients are nonnegative. Therefore each residual in (6), being a sum of remaining terms, has nonnegative coefficients bounded by those of \(F\). Elimination causes no coefficient growth beyond \(O_{d,e}(n)\) bits.

Even forming every product by generic dense convolution costs only
\[
O_{d,e}(n^{3q+2})
\]
bit operations. The subtractions cost \(O_{d,e}(n^{2q+2})\); sorting and enumeration are smaller. Products can be constructed one at a time.

Combining these estimates gives
\[
O_{d,e}\!\left(
(n+1)^{4q+2m+8}\log^2(n+2)
\right),
\]
and hence the boxed exponent \(4q+2m+10=8(d+e)+2m+10\). For example, \(O_{d,e}((n+1)^{2q+5})\) bits of workspace suffice with the storage scheme described above.

#### Input, precision, and output

Reading and validating three explicit partitions costs \(O(n\log(n+2))\) bits of work; unary \(n\) is charged. For \(n=0\), return \(1\).

There is no approximation, sampling, oracle access, or quantum state preparation. All integers and polynomial coefficients are constructed explicitly.

Each surviving basis polynomial evaluates to a positive integer at all variables equal to one. Equation (1) consequently implies
\[
0\le g(\lambda,\mu,\nu)\le F(1)\le C^n.
\]
The binary output therefore needs at most \(1+\lceil n\log_2 C\rceil\) bits, including the trivial zero case.

### 5. Audit obligations and scope

The decisive obligations are discharged above: the ordinary internal-coproduct identity, hook vanishing and unit leading terms, exact finite determinant evaluation, and bounded integer extraction.

Concrete exact falsifiers would be a correctly computed failure of the asserted leading term, a nondivisible Newton numerator, or a nonzero terminal residual in (6). These are implementation-checkable invariants; finite passing examples are not the basis of the proof.

This establishes only the stated **two-fixed-Durfee, numerical-\(n\)** contract. The supplied Panova excerpts do not include §7.5, so they do not authenticate that the attributed open question has precisely these two bounds. Novelty, priority, and the broader dimension-ratio comparison remain outside this conclusion.