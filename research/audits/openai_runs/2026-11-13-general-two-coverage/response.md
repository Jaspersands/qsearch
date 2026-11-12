## Conclusion

I do **not** obtain a polynomial-bit source for arbitrary growing-degree fields. Restricting to quadratic unramified class characters does not, by itself, remove the harmful **principal** exceptional zero.

There is, however, a constructive two-primary gain:

> **If \(K/\mathbf Q\) is Galois of \(2\)-power degree and only one finite rational prime ramifies, then \(\mathrm{Cl}(K)\) has odd order.**  
> Thus the extra generator set can be empty: \(T=S\).

This includes the cyclic \(2^s\)-degree prime-conductor fields discussed in the retained admission note. It removes their **two-primary source requirement**, not their full class-group/L0 requirement.

Below I give the proof, a paid finite-error reduction for the weighted sampler, and a concrete obstruction to the proposed ramified-ideal supplement. All source-theorem use is limited to the supplied statements; I have not independently reopened the linked papers.

## 1. The exact smaller target—and its sampling cost

Put \(C=\mathrm{Cl}(K)\) and \(J=\langle[T]\rangle\). For a finite abelian group,
\[
|C/J|\text{ odd}
\quad\Longleftrightarrow\quad
J+2C=C.
\]
Equivalently, no nontrivial quadratic class character is trivial on \(J\).

This is weaker than full class generation, but stronger than containing \(C[2]\). For example, the order-two subgroup of \(C_4\) contains all its two-torsion but has even index.

For a nontrivial quadratic class character \(\psi\), write
\[
H=\ker\psi,\qquad
W_\psi(s)=\sum_{\psi(\mathfrak p)=-1}N\mathfrak p^{-s}.
\]
The retained ideal sampler gives exactly
\[
q_\psi
=1-\prod_{\psi(\mathfrak p)=-1}(1-N\mathfrak p^{-s})
\ge 1-e^{-W_\psi(s)}
\]
in the idealized law. This concerns **returned prime supports**, not the class of a sampled principal ideal.

The normalization is also explicit. If \(M/K\) is the corresponding ordinary unramified quadratic extension, then
\[
\frac{\zeta_K(s)}{L_K(s,\psi)}
=\frac{\zeta_K(s)^2}{\zeta_M(s)}
=\prod_{\psi(\mathfrak p)=-1}
 \frac{1+N\mathfrak p^{-s}}{1-N\mathfrak p^{-s}}.
\]
There is no uniform-class assumption here.

### Finite sampling error

Suppose a numerical \(B\) and a uniform bound \(q_\psi\ge\rho\) have been proved for every nontrivial quadratic \(\psi\). Set
\[
r=\left\lceil\log_2(8^nD)\right\rceil,
\qquad
m=\left\lceil \frac{8}{\rho}
 \left(r+\log\frac4\eta\right)\right\rceil.
\]
Run the retained sampler \(m\) times, each to total-variation error
\[
\epsilon=\frac{\eta}{4m},
\]
and retain every prime factor returned.

Until the collected classes span \(C/2C\), their span lies in some hyperplane \(\ker\psi\). A fresh idealized sample increases that span with probability at least \(\rho\). At most \(r\) increases are needed. The usual adaptive Bernoulli domination and Chernoff bound give idealized failure at most \(\eta/4\); coupling the finite samplers adds at most \(m\epsilon=\eta/4\).

No character, subgroup-membership oracle, or class coordinates are constructed.

The retained sampler’s clock is polynomial in the field input, **numerical \(B\)**, and \(\log(m/\eta)\). Its norm-bit cap bounds both the number of output prime factors and their representations. Consequently the later complete \(T\)-unit call pays \(|T|\) and \(\max_{\mathfrak p\in T}\log N\mathfrak p\). This establishes a finite-clock reduction, but not the missing general escape bound.

## 2. Why quadratic unramified characters do not remove the principal term

In the retained Chebotarev calculation, let \(\omega\) denote the exceptional class character, when present. For \(H=\ker\psi\) of index two, the aggregate main term outside \(H\) is:

\[
\begin{array}{c|c}
\text{exceptional character} & \text{main term outside }H\\ \hline
\omega=1&
\tfrac12\bigl(\operatorname{Li}(x)-\operatorname{Li}(x^\beta)\bigr)\\
\omega=\psi&
\tfrac12\bigl(\operatorname{Li}(x)+\operatorname{Li}(x^\beta)\bigr)\\
\omega\ne1,\psi&
\tfrac12\operatorname{Li}(x).
\end{array}
\]

Thus a nonprincipal exceptional character is harmless for the required escape. The principal one remains harmful **even though \(\psi\) is quadratic and unramified**.

The factorization
\[
\zeta_M(s)=\zeta_K(s)L_K(s,\psi)
\]
does not force a second copy of a principal exceptional zero: \(\zeta_M\) can inherit the simple zero of \(\zeta_K\). Unramifiedness does not give the odd-Galois multiplicity argument.

Writing \(\delta=1-\beta\), the relevant dyadic calculation is
\[
\frac{d}{dx}\left(\operatorname{Li}(x)-\operatorname{Li}(x^\beta)\right)
=\frac{1-x^{-\delta}}{\log x}.
\]
At a polynomial-bit scale \(X\), this supplies a constant fraction of the ordinary main term only when \(\delta\log X\) is bounded below.

This is a limitation of this proof, **not** an upper bound on the actual weighted support escape: small primes could already supply sufficient escape.

### An explicit \(B\) when the prime-count bound is paid

Suppose the retained argument supplies \(X=2^L\) and, simultaneously for all relevant \(H\),
\[
\#\{\mathfrak p\notin H:X\le N\mathfrak p<2X\}
\ge \frac{X}{4\log(2X)}.
\]
Then take the integer
\[
\boxed{B=L+1.}
\]
For \(s=1+1/B\), one has \((2X)^{1/B}=2\), so
\[
W_\psi(s)
\ge \frac{X}{4\log(2X)}(2X)^{-s}
=\frac{1}{16\log(2X)}.
\]
Hence the conservative escape bound
\[
\boxed{\rho=\frac{1}{32(L+1)}}
\]
is valid.

This pays numerical \(B\), not merely \(\log B\). For example, the supplied Stark statement gives such a polynomial scale for **Galois fields with no quadratic subfield**, using
\[
L=\left\lceil A\log_2(Dn^n)\right\rceil
\]
with the retained effective absolute constant \(A\). I have not evaluated that constant numerically here.

For arbitrary nonnormal fields, substituting the retained \(n!\)-dependent bound does **not** meet the growing-degree contract. No general polynomial \(B\) follows.

## 3. A concrete genus family defeats the raw ramified-ideal supplement

There is an exact family showing that “include the ramified ideals, then use only quadratic unramified characters” does not automatically evade the principal exceptional factor.

Let
\[
p,q\equiv1\pmod8,\qquad p\ne q,\qquad \left(\frac pq\right)=1,
\]
and set
\[
K=\mathbf Q(\sqrt{pq}),\qquad
M=\mathbf Q(\sqrt p,\sqrt q).
\]

Then:

* \(D_K=pq\) and \(D_M=(pq)^2\), so \(M/K\) is unramified at finite primes.
* Both fields are totally real, so \(M/K\) also satisfies the ordinary-class-field condition at real places.
* Every prime of \(K\) above \(p\) or \(q\) splits in \(M/K\), by the mutual quadratic-residue condition.
* Every prime above \(2\) splits, since \(p,q\equiv1\pmod8\).

Therefore the nontrivial unramified quadratic character \(\psi\) of \(M/K\) is trivial on **all primes above \(2pq\)**.

This is directly relevant to native Selmer input:
\[
f(x)=x(x^2-pq),\qquad \operatorname{disc}(f)=4(pq)^3.
\]
Its bad-prime set is supported on \(2,p,q\). The classes of those bad primes—and all ramified prime ideals—remain inside \(\ker\psi\).

For instance, \(p=17,q=89\) satisfies the conditions because
\[
\left(\frac{17}{89}\right)
=\left(\frac{89}{17}\right)
=\left(\frac4{17}\right)=1.
\]
This is an exact structural witness, not an exceptional-zero example or an asymptotic experiment. It requires no Pell decision or assumption about relations among real ambiguous forms.

### The surviving analytic problem is completely explicit

Let \(\chi_p,\chi_q,\chi_{pq}\) be the associated primitive quadratic Dirichlet characters. Then
\[
L_K(s,\psi)=L(s,\chi_p)L(s,\chi_q),
\qquad
\zeta_K(s)=\zeta(s)L(s,\chi_{pq}).
\]

For an unramified rational prime \(\ell\):

* mixed signs \((\chi_p(\ell),\chi_q(\ell))\) give an inert prime of \(K\), which is principal;
* signs \((+1,+1)\) give primes inside \(\ker\psi\);
* signs \((-1,-1)\) give two norm-\(\ell\) primes outside \(\ker\psi\).

Consequently,
\[
\boxed{
W_\psi(s)=
2\sum_{\substack{\ell\ \mathrm{prime}\\
\chi_p(\ell)=\chi_q(\ell)=-1}}\ell^{-s}.
}
\]
The support escape is exactly
\[
1-\prod_{\chi_p(\ell)=\chi_q(\ell)=-1}(1-\ell^{-s})^2.
\]

A possible exceptional zero of \(L(s,\chi_{pq})\) is **principal over \(K\)** and has the harmful sign for precisely this double-nonresidue prime set. Quadratic unramifiedness and the raw ramified-ideal supplement have not removed it.

This does not reopen the already-treated quadratic algorithm: constructive quadratic class halving can bypass this analytic route. It shows why that algebraic work cannot be replaced by merely adjoining ramified primes.

## 4. A genuine constructive extension: one-prime Galois \(2\)-extensions

Here the smaller output changes the answer decisively.

### Proposition

If \(K/\mathbf Q\) is Galois of degree \(2^a\), and at most one finite rational prime ramifies in \(K\), then
\[
\mathrm{Cl}(K)/2\mathrm{Cl}(K)=0.
\]
In particular, \(\mathrm{Cl}(K)\) has odd order.

### Proof

For analysis only, let \(M/K\) be the maximal ordinary unramified elementary-abelian \(2\)-extension. Thus
\[
A=\operatorname{Gal}(M/K)\simeq\mathrm{Cl}(K)/2\mathrm{Cl}(K).
\]

This extension is canonical, so \(M/\mathbf Q\) is Galois. Its Galois group \(G\) is a finite \(2\)-group. If \(p\) is the sole possible finite ramified prime, then \(M/\mathbf Q\) is also unramified outside \(p\).

Let \(I\le G\) be inertia at a prime above \(p\). If \(I\ne G\), it is contained in a maximal subgroup \(N\) of the finite \(2\)-group \(G\). Such \(N\) is normal of index two. All conjugates of \(I\) lie in \(N\), so the quadratic field \(M^N/\mathbf Q\) is unramified at \(p\), and also at every other finite prime.

No nontrivial quadratic extension of \(\mathbf Q\) is unramified at all finite primes. Hence \(I=G\).

But \(M/K\) is unramified, so
\[
I\cap A=1.
\]
Together with \(I=G\), this gives \(A=1\). ∎

The Hilbert class field is used only in this proof; it is neither supplied nor constructed by the algorithm.

### Native source and application

On this family, the source simply returns
\[
R=\varnothing,\qquad T=S.
\]
There are no sampling, precision, or generator-confidence costs. The ordinary bad-prime decomposition and the complete compact \(T\)-unit computation remain paid operations.

A recognizable growing-genus native family is
\[
f_k(x)=x\bigl(x^{2^k}+1\bigr),\qquad k\ge1.
\]
Its branch algebra is
\[
\mathbf Q\times\mathbf Q(\zeta_{2^{k+1}}).
\]
The nontrivial factor has degree \(2^k\), is Galois, and ramifies only at \(2\). Thus \(T=S\) suffices. Its discriminant has \(O(2^k k)\) bits, and the input, maximal-order arithmetic, ideal representations, and complete \(T\)-unit call all remain polynomial in the native degree-and-coefficient input—not in \(k\) alone.

The same algebraic argument applies to the retained cyclic \(2^s\)-degree prime-conductor fields. Their possibly nontrivial **odd** class groups are irrelevant to this source objective.

The \(2\)-group hypothesis is essential. The supplied cyclic-cubic example, ramified at only \(163\) but with class group \(C_2^2\), already falsifies a one-ramified-prime claim without that hypothesis.

Under the stipulated local-image premises, this removes the global generator-GRH premise for these Selmer families. It makes no quantum-speedup claim; specialist classical unit methods must also be considered.

## 5. The precise unpaid statement for the analytic attack

The weighted-sampler-plus-ramified-ideal route already requires the following concrete statement.

> **Double-nonresidue harmonic bound.**  
> Find effective absolute constants \(A,c>0\) such that, for every pair of primes
> \[
> p,q\equiv1\pmod8,\qquad (p/q)=1,
> \]
> with
> \[
> B=\left\lceil A(1+\log(pq))^c\right\rceil,
> \]
> one has
> \[
> \sum_{\substack{\ell\ \mathrm{prime}\\
> (\ell/p)=(\ell/q)=-1}}
> \ell^{-1-1/B}
> \ge \frac{1}{A(1+\log(pq))^c},
> \]
> including the case of a possible exceptional zero of \(L(s,\chi_{pq})\).

This is a specific Dirichlet-prime statement for an explicit ordinary unramified genus extension, rather than the prior all-class-characters coverage barrier. A proof would pay this genus case of the sampler, with the finite-error procedure in §1. It would **not alone** prove the arbitrary-degree theorem.

The supplied statements do not establish it. Fixed-field convergence supplies no numerical polynomial \(B\), and a least-prime existence result supplies no such harmonic mass. No exceptional zero is asserted to exist.

Finally, complete \(T\)-units do not themselves implement the missing halving operation. Their valuation lattice presents the subgroup already generated by \(T\). In an equation
\[
\mathfrak b^2=(\alpha)\mathfrak a,
\]
with \(\mathfrak a\) supported on \(T\), restricting \(\alpha\) to \(U_T\) forces \(\mathfrak b\) to be supported on \(T\) as well. It therefore cannot produce an outside class needed for saturation. I have no native arbitrary-degree implementation of that additional operation to substitute here.

**Disposition:** the general source remains unproved. The one-prime Galois \(2\)-extension result is a genuine constructive two-primary extension; the explicit genus family isolates why the proposed general analytic/ramified supplement is still unpaid. Neither failure establishes hardness or impossibility.