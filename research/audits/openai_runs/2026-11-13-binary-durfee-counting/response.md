## Verdict

**The compiler is valid for fixed \(d,e\).** The proposed single-coefficient identity is correct in its stated chamber. Moreover, the cap **\(n\)** already works: off-diagonal **Frobenius Giambelli** hooks cannot exceed \(n\).

An explicit bound on the number of lattice variables is
\[
\boxed{D_{d,e}=8d^{2}e^{2}+2de+d^{2}+e^{2}}.
\]
Below is a uniform reduction to bounded integer-point problems, followed by the required binary-complexity accounting.

### 1. Input and algebraic conventions

Write the inputs as
\[
\lambda=(\alpha\mid\beta),\qquad
\mu=(\gamma\mid\delta),\qquad
\nu=(r\mid s),
\]
with respective Frobenius lengths \(a,b,c\).

Read and validate every coordinate: the two lists for each partition have equal length and are strictly decreasing nonnegative integer lists. Compute
\[
|\lambda|=a+\sum_i(\alpha_i+\beta_i),
\]
and similarly for \(\mu,\nu\), using binary arithmetic. Reject inconsistent sizes or inputs outside \(a\le d,b\le e\). No ordinary row-list expansion is needed. These operations take polynomial bit time in the supplied length \(L\).

For common size \(n=0\), return \(1\). Henceforth \(n>0\), so \(a,b,c\ge1\).

All supersymmetric identities use
\[
p_k(x\mid y)=p_k(x)+(-1)^{k-1}p_k(y).
\]
In particular, the rectangular factor is \(\prod(x_i+y_j)\), with no additional sign.

## 2. The single coefficient is a genuine projector

For the extractor alone, work in
\[
\mathbb Z[x^{\pm1},u^{\pm1}][[y,v]].
\]
The stipulated expansions of \(Q_X^{-1},Q_Z^{-1}\) are well-defined there: each geometric factor increases a \(y\)- or \(v\)-degree.

Consider a surviving \((a,a)\)-hook partition \(\rho\).

**Case \(\operatorname{Durfee}(\rho)=a\).** Rectangular factorization gives
\[
hs_\rho(X)=Q_X
s_{(\rho_1-a,\ldots,\rho_a-a)}(x)
s_{(\rho'_1-a,\ldots,\rho'_a-a)}(y).
\]
Consequently,
\[
\frac{\Delta(x)\Delta(y)}{Q_X}hs_\rho(X)
=
\det(x_i^{\rho_j-j})_{i,j\le a}
\det(y_i^{\rho'_j-j})_{i,j\le a}.
\]
Both exponent lists are strictly decreasing. The coefficient of
\(x^\alpha y^\beta\) therefore equals \(1\) exactly when both Frobenius lists equal those of \(\lambda\), and otherwise equals \(0\). The matching permutations are identities, so the sign is \(+1\).

**Case \(\operatorname{Durfee}(\rho)<a\).** Use the skew-Schur identity
\[
hs_\rho(X)=
\sum_{\substack{\kappa\subseteq\rho\\\ell(\kappa)\le a}}
s_\kappa(x)s_{\rho'/\kappa'}(y).
\]
Pad \(\kappa\) to length \(a\). Since \(\rho_a<a\), one has \(\kappa_a<a\). Every monomial of
\[
\Delta(x)s_\kappa(x)=\det(x_i^{\kappa_j+a-j})
\]
has some \(x\)-coordinate with exponent \(\kappa_a<a\). Multiplication by
\[
Q_X^{-1}
=\prod_i x_i^{-a}
 \prod_{i,j}\sum_{q\ge0}(-y_j/x_i)^q
\]
subtracts at least \(a\) from **every** \(x\)-exponent and never increases one. That coordinate becomes negative. Multiplication by the remaining \(y\)-polynomials cannot repair it.

Thus no such term reaches the all-nonnegative target \(\alpha\). This argument includes zero arms and legs and does not assume a generic shape. The skew-Schur sum is a proof device, not an algorithmic enumeration.

The same argument applies to \(Z\).

Now \(p_k(T)=p_k(X)p_k(Z)\), so the usual symmetric-function Kronecker identity specializes to
\[
hs_\nu(T)=\sum_{\rho,\sigma\vdash n}
g(\rho,\sigma,\nu)hs_\rho(X)hs_\sigma(Z).
\]
Applying the two proved projectors establishes exactly
\[
\boxed{
g(\lambda,\mu,\nu)=
[x^\alpha y^\beta u^\gamma v^\delta]\,
hs_\nu(T)
\frac{\Delta(x)\Delta(y)\Delta(u)\Delta(v)}{Q_XQ_Z}.
}
\]
This proof does not require enumerating the Schur basis.

There are \(2ab\) even and \(2ab\) odd tensor letters. Hook vanishing implies \(hs_\nu(T)=0\) if \(c>2ab\); the projector then proves \(g=0\). After that shortcut,
\[
c\le2ab
\]
is fixed.

## 3. Explicit finite rational terms

Put
\[
\mathcal E=\{x_i u_j,\ y_i v_j: i\le a,j\le b\},\qquad
\mathcal O=\{x_i v_j,\ y_i u_j: i\le a,j\le b\}.
\]
Both have size \(2ab\).

For a hook, the prescribed chamber gives
\[
[t^r w^s]\frac{H_T(t)E_T(w)}{t+w}
=\sum_{j=0}^{s}(-1)^j h_{r+j+1}(T)e_{s-j}(T)
=hs_{(r+1,1^s)}(T).
\]
The last equality is the hook Jacobi–Trudi identity. This displayed sum is **not executed**. The omitted \(-1/(t+w)\) has only negative \(t\)-exponents.

For each Giambelli permutation \(\sigma\in S_c\), assign hook \(h\) its own \(t_h,w_h\), targeting \(r_h,s_{\sigma(h)}\). Consequently, omitted \(-1\) terms cannot acquire positive \(t_h\)-degree from another hook.

Expand only:

* the \(c!\) Giambelli permutations;
* the four Vandermonde determinants;
* the \(4abc\) binomial numerator factors.

For each resulting term, let \(m\) be its Laurent-monomial exponent vector. It is explicitly obtained from:

1. shifts \(-a\) on every \(x_i\), \(-b\) on every \(u_j\), and \(-1\) on every \(t_h\);
2. chosen Vandermonde monomials, e.g.
   \(\prod_i x_i^{a-\pi_x(i)}\);
3. an arbitrary selected subset of \(zt_h\), \(z\in\mathcal O\), and of \(zw_h\), \(z\in\mathcal E\), for each hook.

Its fixed sign \(\omega\) is the product of the Giambelli and four Vandermonde permutation signs. All binomial numerator coefficients are \(+1\).

Order the formal coordinates as
\[
(x,y,u,v,t_1,\ldots,t_c,w_1,\ldots,w_c),
\]
and define
\[
B_\sigma=(\alpha,\beta,\gamma,\delta,r_1,\ldots,r_c,
s_{\sigma(1)},\ldots,s_{\sigma(c)}).
\]

Here is the complete list of geometric occupations. Write \(\mathbf e(z)\) for a monomial’s exponent vector.

| Factor family | Matrix column | Occupation sign | Number |
|---|---|---:|---:|
| \(H_T(t_h)\) denominators, \(z\in\mathcal E\) | \(\mathbf e(z)+\mathbf e_{t_h}\) | \(+1\) | \(2abc\) |
| \(E_T(w_h)\) denominators, \(z\in\mathcal O\) | \(\mathbf e(z)+\mathbf e_{w_h}\) | \(+1\) | \(2abc\) |
| \(1/(1+w_h/t_h)\) | \(\mathbf e_{w_h}-\mathbf e_{t_h}\) | \((-1)^{k}\) | \(c\) |
| \(1/(1+y_j/x_i)\) | \(\mathbf e_{y_j}-\mathbf e_{x_i}\) | \((-1)^{k}\) | \(a^2\) |
| \(1/(1+v_j/u_i)\) | \(\mathbf e_{v_j}-\mathbf e_{u_i}\) | \((-1)^{k}\) | \(b^2\) |

Let \(A\) be the matrix of these columns. It has
\[
R=2a+2b+2c
\quad\text{rows and}\quad
D=a^2+b^2+c(4ab+1)
\]
columns, all entries in \(\{-1,0,1\}\).

The term contributes
\[
\omega
\sum_{\substack{k\in\mathbb Z_{\ge0}^{D}\\Ak=B_\sigma-m}}
(-1)^{\sum_{\ell\in S}k_\ell},
\]
where \(S\) consists exactly of the last three table families.

**Formal-series justification.** Assign weights
\[
\operatorname{wt}(x_i)=\operatorname{wt}(u_j)=0,\quad
\operatorname{wt}(y_i)=\operatorname{wt}(v_j)=1,\quad
\operatorname{wt}(t_h)=1,\quad
\operatorname{wt}(w_h)=2.
\]
Every geometric direction in the table has strictly positive weight. Therefore these expansions lie in a common Laurent-series completion and have locally finite coefficients. Negative \(x,u,t\) shifts cause no ambiguity or infinite cancellation. The auxiliary and base-variable coefficient extractions may be interchanged.

## 4. The explicit cap is \(n\)

First, the off-diagonal warning does **not** invalidate this construction:
\[
n=c+\sum_i r_i+\sum_i s_i
\quad\Longrightarrow\quad
r_i+s_j+1\le n-c+1\le n.
\]
This holds for every Frobenius Giambelli cell, diagonal or not.

Fix one expanded numerator term. For hook \(h\), let \(p_h,q_h\ge0\) be its numerator \(t_h,w_h\)-degrees. Let \(j_h\) be its \(w_h/t_h\) occupation, and let \(H_h,E_h\) be the sums of its respective \(H\)- and \(E\)-denominator occupations. Matching auxiliary exponents gives
\[
E_h+q_h+j_h=s_{\sigma(h)},\qquad
H_h+p_h-1-j_h=r_h.
\]
Thus
\[
j_h,E_h\le s_{\sigma(h)}\le n,\qquad
H_h\le r_h+s_{\sigma(h)}+1\le n.
\]
Every individual hook occupation is therefore at most \(n\).

Each \(Q_X\) occupation increases some \(y_j\). All other contributions to that \(y_j\)-exponent are nonnegative, including Vandermonde monomials. Hence each such occupation is at most \(\beta_j\le n\). Likewise each \(Q_Z\) occupation is at most the corresponding \(\delta_j\le n\).

Therefore, **term by term, before cancellation**,
\[
\boxed{0\le k_\ell\le n\quad\text{for every contributing occupation}.}
\]
Impossible degree equations simply produce empty problems.

## 5. Explicit bounded integer-point problems, including signs

There are
\[
s_0=|S|=a^2+b^2+c
\]
signed indices. Enumerate \(\eta\in\{0,1\}^{S}\), extending it by zero on unsigned indices. Substitute
\[
k=Cz+\eta,
\]
where \(C\) is diagonal, with entry \(2\) on signed indices and \(1\) elsewhere.

Define
\[
U_\ell=
\begin{cases}
\lfloor(n-\eta_\ell)/2\rfloor,&\ell\in S,\\
n,&\ell\notin S.
\end{cases}
\]
The explicit polytope for this branch is
\[
\boxed{
P=\left\{
z\in\mathbb R^D:
ACz=B_\sigma-m-A\eta,\quad
0\le z_\ell\le U_\ell
\right\}.
}
\]
Its contribution is
\[
\omega(-1)^{\sum_{\ell\in S}\eta_\ell}
\,|P\cap\mathbb Z^D|.
\]

This is a bijection between integer points and occupations of the specified parity, not merely a congruence relaxation. Equality constraints can be supplied as two inequalities. Negative upper bounds, inconsistent equalities, and zero rows are checked directly.

The total number of problems is at most
\[
N_{a,b,c}
=
c!(a!)^2(b!)^2\,2^{\,4abc+a^2+b^2+c},
\]
a constant for fixed \(d,e\). Their dimension satisfies
\[
D\le a^2+b^2+2ab(4ab+1)
\le \boxed{D_{d,e}}.
\]

Their inequality coefficients are in \(\{-2,-1,0,1,2\}\); right-hand sides and bounds have \(O_{d,e}(\log(n+1))=O_{d,e}(L)\) bits. The box is encoded in binary, **not enumerated**.

All permutations, subsets, columns, signs, and parity branches are generated by this algorithm. There is no preprocessing advice.

## 6. Barvinok–Pommersheim: applicable hypotheses and paid counting

The supplied source text establishes the relevant chain:

* LF 155–174 defines inequality-description size by **binary encoding**.
* Theorem 4.4, LF 934–955, gives a polynomial-time short generating-function algorithm for rational polyhedra in fixed ambient dimension.
* Algorithm 5.2, LF 1056–1105, gives exact polynomial-time counting for rational **polytopes** in fixed dimension.

Our problems satisfy these hypotheses: dimension at most \(D_{d,e}\), integer normals, integer—hence rational—right-hand sides, and explicit boundedness. The theorem’s subsequent statement about fixed normals and unchanged combinatorial structure is an **additional parametric assertion**, not a hypothesis for running the algorithm. We do not use it.

I can audit these supplied excerpts; without tools I cannot independently authenticate the PDF hashes or physical line locations.

**Empty and lower-dimensional cases can also be handled explicitly before invocation.** There are constantly many inequalities. Enumerate their \(D\)-element subsets, solve full-rank intersections exactly, and retain feasible vertices. Since the polytope is bounded, no feasible vertex means it is empty. This works even when the polytope is lower-dimensional.

From the vertices compute its rational affine hull. Clear denominators and use polynomial-bit Smith/Hermite normal form to determine whether that hull contains an integer point and, if so, parameterize its integer lattice as
\[
z=z_0+Uy,\qquad y\in\mathbb Z^k.
\]
These are exact rational linear-algebra and integer Euclidean-algorithm computations in bounded dimension, with polynomial-bit data. If the affine hull has no integer point, return zero. For \(k=0\), count the single point directly. Otherwise substitute into the inequalities, obtaining a bounded full-dimensional rational polytope in dimension \(k\le D\). Thus no nondegeneracy assumption is hidden.

Nor is the generating-function-to-count step a free oracle or numerical limit. Following Algorithm 5.2, choose an integer moment-curve vector nonorthogonal to every returned denominator direction. Polynomially many candidates suffice. Substitution \(x_j=\exp(\tau\ell_j)\) reduces each summand to
\[
\varepsilon_i
\frac{\exp(\eta_i\tau)}
{\prod_{j=1}^{k}(1-\exp(\xi_{ij}\tau))},
\qquad \xi_{ij}\ne0.
\]
Compute the degree-\(k\) Taylor coefficient after multiplication by \(\tau^k\), using exact truncated rational series. Since \(k\) is fixed, only fixed-order expansions are required. The short representation has polynomially many terms and polynomial-bit exponents; exact rational evaluation and summation therefore cost polynomial bit time. No floating-point precision promise or unit-cost large-integer arithmetic is used.

## 7. End-to-end bit bound and scope

Every branch count satisfies
\[
|P\cap\mathbb Z^D|\le(n+1)^D.
\]
Consequently the final output and the compiler’s signed partial sums have
\[
O_{d,e}(\log(n+1))
\]
bits. Internal counting-algorithm data need only satisfy—and do satisfy—the polynomial-bit bounds of that algorithm; a stronger linear-bit claim about all its intermediates is unnecessary.

Reading and validating the input costs polynomial time in \(L\). Generating the constant number of descriptions costs polynomial bit time. Each fixed-dimensional counting call costs polynomial bit time in its \(O_{d,e}(L)\)-bit description. Signed addition and writing the output are polynomial as well. Hence
\[
\boxed{\text{deterministic running time } \operatorname{poly}_{d,e}(L),
\text{ including output}.}
\]

There is no numerical-\(n\) loop, character oracle, count oracle, advice, approximate arithmetic, or quantum state-preparation step.

**Explicit falsifiers addressed:** a legal lower-Durfee term reaching an all-nonnegative target would invalidate the projector; a legal exponent solution with an occupation exceeding \(n\) would invalidate the bounded reduction; failure of the parity bijection would invalidate its signs. The arguments above exclude all three universally, rather than by finite examples.

This establishes only the fixed-\(d,e\), compact-Frobenius **classical** compiler. It makes no claim for growing Durfee, novelty or priority, hardness, or quantum advantage.