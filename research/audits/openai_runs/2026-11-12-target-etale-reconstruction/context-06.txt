## Verdict

**The proposed orbit reconstruction followed by direct reduction is not justified by the stated interfaces.** There is an interface-level counterexample: a polynomial-bit-size, Galois-equivariant change of the canonical encoding can preserve every characteristic-zero and small-\(P\) promise while making **every integer linear functional collide at the original prime \(p\)**.

This falsifies the proposed **direct-reduction plus candidate-search mechanism**, not the existence of another classical completion. The smallest missing statement exhibited here is a **bounded target-faithful encoding selector**, or a separately proved, polynomial-cost \(p\)-integral normalization step.

I retain the following as conditional inputs, not established native closure:

- **[Frame]** The genuine full constant-\(\Gamma\) frame cover and evaluation maps, where \(\Gamma=\operatorname{GSp}_n(\mathbf F_\ell)\).
- **[Good-\(p\)]** Good reduction at the target, with \(p\ne\ell\).
- **[Aux]** The constructible auxiliary \(P\), faithful presentation and RR interface.
- **[Socle]** The genuinely Galois-stable natural socle \(E\), of rank \(R=nm\), \(m=(r-2)n\).
- **[Lift]** Complete small-\(P\) torsion, exact operations, and numerical lifts at charged precision.
- **[Height]** The admitted polynomial logarithmic-height bound for admissible canonical closed-divisor encodings.

The counterexample persists even if one additionally grants a successful \(P\)-admissible basepoint choice and **exact** characteristic-zero reconstruction.

## 1. The first cheap falsifiers can be repaired

Put
\[
s=|\Gamma|,\qquad M=\ell^R,\qquad N=sM.
\]
These are polynomial in numerical \(\ell\), with the stipulated fixed \(n,r,R\).

For a rational unbranched \(a\), let \(T_a\) be the full frame fibre. After choosing a geometric point \(b_0\), write
\[
\sigma(b_0)=b_0c_\sigma .
\]
Since the right deck action is constant, \(c_{\sigma\tau}=c_\sigma c_\tau\). Consequently the splitting field of \(T_a\) has degree at most \(s\), not \(s!\). By **[Socle]**, the field trivializing \(E\) has degree at most
\[
|\operatorname{GL}_R(\mathbf F_\ell)|.
\]
Their compositum therefore has degree at most
\[
D=s\,|\operatorname{GL}_R(\mathbf F_\ell)|.
\]

Encoding **all** \((b,t)\in T_a\times E\), with the component/origin data indexed by every \(g\in\Gamma\), repairs the non-rational-basepoint problem. Uniqueness of each canonical divisor and constant deck maps give
\[
\sigma\bigl(\operatorname{enc}(b,t)\bigr)
 =\operatorname{enc}(\sigma b,\sigma t).
\]
Thus the product polynomial and uniquely interpolated tables for **Galois-equivariant operations** have rational coefficients.

This does not require splitting geometric divisor supports. The coefficients of a unique closed divisor lie in its field of definition.

At an auxiliary prime where these fibres are étale, one common residue extension also suffices: the fibre Frobenius orders divide \(s\), while the order on \(E\) divides \(|\operatorname{GL}_R(\mathbf F_\ell)|\). A common extension of degree dividing their product accommodates both. Any additional field used by the admitted lifting implementation remains separately charged.

### The dimension and action conventions

For right deck maps \(R_g\),
\[
A(g)=R_g^*,\qquad P(g)=(R_g)_*=A(g^{-1}).
\]
Here \(A\) is a left representation and \(P\) is a right action. With
\[
S=(\mathbf F_\ell^n)^\vee,\qquad
W=\operatorname{Hom}_\Gamma(S,E),
\]
the admitted natural-socle statement is
\[
\dim W=m,\qquad E\simeq S\otimes W,\qquad \dim E=nm=R.
\]
It is **not** an identification of \(W\) with a collection of actual torsion classes.

The pair set has \(N=s\ell^R\) elements and is not itself the torsion group. For example, legitimate equivariant tables include
\[
((b,t),(c,u))\longmapsto(b,t+u),\qquad
(b,t)\longmapsto(b,0),\qquad
(b,t)\longmapsto(bg,t).
\]
One must subsequently remove the torsor factor, rather than regard all \(N\) labels as \(E\).

None of these repairs supplies target-faithful coordinates.

## 2. Height bounds solve certification—not reduction quality

Grant that every scalar tuple coordinate has absolute logarithmic height at most \(H_0\), including the separately bounded basepoint coordinates.

For a linear functional with \(L\) coordinates and coefficients of absolute value at most \(A\), a safe bound is
\[
h(\gamma(z))\le L(H_0+\log\max(1,A))+\log L=:H_\gamma.
\]
Then, for instance,
\[
h(Q_\gamma)\le N(H_\gamma+\log 2).
\]

Writing
\[
L_i(X)=
\frac{\prod_{j\ne i}(X-\alpha_j)}
     {\prod_{j\ne i}(\alpha_i-\alpha_j)},
\qquad \alpha_i=\gamma(z_i),
\]
gives polynomial height bounds for every coefficient of \(L_i\). Unary tables use \(N\) such terms; binary tables use \(N^2\). Their coefficient heights consequently remain polynomial in \(N,L,H_0,\log A\).

The degree bound \(D\) also bounds local valuations of nonzero algebraic differences. Together these bounds support certified precision propagation and rational reconstruction, rather than an integer-relation guess. All lifting, interpolation, rational arithmetic and output sizes must still be charged.

But
\[
\text{a polynomial bound on }h(Q_\gamma)
\quad\not\Rightarrow\quad
p\nmid\operatorname{disc}(Q_\gamma).
\]
A height bound pays for a denominator or discriminant; it does not make it a \(p\)-adic unit.

## 3. Counterexample: all candidate functionals fail at \(p\)

Start with an admissible canonical encoding. Denote its torsion-dependent scalar entries by
\[
u_1(b,t),\ldots,u_L(b,t).
\]
They determine the same actual closed divisors as before. Suppose their heights are bounded by \(H_0\).

Every such entry has algebraic degree at most \(D\). For every place above \(p\), using \(v_p(p)=1\),
\[
v_p(u_j)\ge-\frac{D H_0}{\log p}
\]
when \(u_j\ne0\).

Choose the explicitly bounded integer
\[
k=1+\left\lceil\frac{D H_0}{\log p}\right\rceil
\]
and replace the encoding by
\[
u'_j(b,t)=p^k u_j(b,t).
\]
Leave any torsion-independent basepoint entries unchanged. Any torsion-dependent chart tags can be encoded with the same scaling.

This is an invertible, explicitly known rational reencoding. Its inverse divides by the known integer \(p^k\); no number field or Galois advice is needed.

### It preserves the admitted promises

- The genuine cover, evaluation, torsion classes and \(h^0=1\) assertions are unchanged.
- It remains Galois-equivariant.
- At \(P\ne p\), multiplication by \(p^k\) is a unit. Thus faithful small-\(P\) encoding and lifting are unchanged.
- The height increase is polynomial:
  \[
  h(u'_j)\le H_0+k\log p
  \le H_0+D H_0+2\log p.
  \]
- The scaling and its inverse have polynomial bit size.
- No new characteristic-zero chart exception is introduced.

Thus it satisfies the stated *type* of encoding-height interface. If “canonical” is intended to forbid this reencoding, the missing restriction must be stated as an integral normalization property; uniqueness and a height bound do not imply it.

### Every integer functional collides

For every \(j,b,t\),
\[
u'_j(b,t)\in p\mathcal O_{\overline{\mathbf Q}_p}.
\]
Hence, for a fixed \(b\) and any \(t,t'\in E\), every integer linear functional satisfies
\[
\gamma(\operatorname{enc}'(b,t))
-
\gamma(\operatorname{enc}'(b,t'))
\in p\mathcal O_{\overline{\mathbf Q}_p}.
\]

Therefore:

- either \(Q_\gamma\) is not \(p\)-integral, so direct reduction is unavailable;
- or its roots are integral and the \(M=\ell^R>1\) labels over each fixed \(b\) have the same reduction.

In the second case, over \(\overline{\mathbf F}_p\),
\[
\overline{Q_\gamma}(X)
  =\prod_{b\in T_a}(X-c_b)^M,
\]
possibly with further coincidences among the \(c_b\). It is never squarefree.

This applies to **every** integer coefficient vector, not merely a particular moment curve or a finite candidate grid. Moving \(b\) does not help: the collision occurs among the torsion labels over each \(b\). In fact, any integral polynomial functional of these entries has the same problem.

The elementary two-label illustration is
\[
Q(X)=X(X-p).
\]
It is separable over \(\mathbf Q\), has small logarithmic height, and is perfectly usable at an auxiliary \(P\ne p\). But
\[
\overline Q=X^2.
\]
Applying \(X\mapsto X^p\) to this nonreduced order is not the arithmetic permutation of the two characteristic-zero labels.

### This is not a finite-small-\(p\) issue

The construction works for arbitrarily large \(p\). Its coefficients depend on \(p\), with logarithmic size \(O(B)\), exactly as the interface permits.

Thus
\[
p>\text{every relevant fixed polynomial in }\ell
\]
does not repair it. One cannot appeal to “only finitely many bad primes for a fixed encoding” when the native instance and its encoding vary with the target prime.

## 4. The exact missing success lemma

A direct-reduction algorithm needs an effective statement of the following form.

> **Target-faithful selector.** There is a polynomial-size, polynomial-bit candidate family of fibres and encoding charts, with a computable bound, such that at least one candidate is admissible at \(P\), has an unramified target fibre, and gives a \(p\)-integral tuple encoding that separates every pair after reduction.

“Finite chart exceptions in characteristic zero” is insufficient. The selector needs a bound on the bad locus **after reduction at \(p\)** and a proof that it is not the whole parameter space.

Once a target-faithful tuple exists, the remaining functional search is elementary. For
\[
\gamma_c(z)=\sum_{j=0}^{L-1}c^jz_j,
\]
each pair excludes at most \(L-1\) values of \(c\), so at most
\[
C_\gamma=(L-1)\binom N2
\]
values are bad. If \(p>C_\gamma\), testing \(C_\gamma+1\) distinct residues guarantees success.

The missing premise is that each pair’s difference polynomial is nonzero modulo \(p\). The counterexample makes those polynomials identically zero.

### Verification is available; guaranteed success is not

For a reconstructed candidate, the following are exact, polynomial-size checks:

1. the required rational denominators are prime to \(p\);
2. \(\gcd(\overline Q_\gamma,\overline Q_\gamma')=1\);
3. the reduced operation tables satisfy the required identities;
4. the selected frame fibre has the required target étaleness.

These use division by the known prime \(p\) and finite-field arithmetic, not factorization of a target-sized integer.

They certify a successful candidate. They do **not** establish that a bounded search contains one. In the counterexample, every candidate correctly fails.

For \(p\le C_\gamma\), a complete algorithm also needs an explicitly charged alternative to a single primitive coordinate; it cannot silently discard those cases.

## 5. What a repair would have to pay

A different algorithm could avoid target-good divisor charts by:

1. reconstructing the rational finite algebra and operations;
2. taking the quotient corresponding to \(E\);
3. computing a \(p\)-maximal, finite-étale order using the promised unramified representation;
4. reducing that order and computing its Frobenius.

That is a plausible algorithmic repair, not supplied global advice. But its construction, polynomial bit bounds, operation-table transport and output extraction must be proved and charged. Merely invoking good reduction does not make the initially reconstructed monogenic order \(p\)-maximal.

If either repair succeeds, the full-frame conventions then give
\[
\phi g^T=P(g)\phi,\qquad
F_W(\phi)=F_E\circ\phi.
\]
Under the supplied arithmetic identification, the corrections are \(p^{-1}\) for \(H^1(U,L)\) and \(p^{-2}\) for the stated untwisted coefficient system; geometric Frobenius is the inverse.

**Bottom line:** all-pairs orbit encoding repairs the algebraic-basepoint and global-field problems, and **[Height]** can repair heuristic reconstruction. It does not supply a target-faithful reduction. The proposed integer-\(\gamma\)/basepoint search has a counterexample under the written interfaces. No hardness claim, classical lower bound, or quantum speedup follows.