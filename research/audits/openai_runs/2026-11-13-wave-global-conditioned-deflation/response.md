## Decision: stop at a falsified cluster-compression operation

I do **not** obtain a universal compiler. The following operation, suggested by combining local deflation with the supplied angular-subspace result, is false:

> An arbitrary binary-radius cluster can be replaced by polynomial-size local polynomial fields and a polynomial-angular-bandwidth radiative field at one cluster center, with polynomial total preparation scale relative to \(\|A^{-1}f\|\).

The obstruction below is on the **exact finite torus**, includes \(\eta=1/L\), and allows arbitrary local corrections—not merely exact Laurent quotients.

This is a mechanism-specific rejection. It is **not** an impossibility theorem for every source-dependent cluster algorithm, nor a lower bound for direct Born-law sampling.

## 1. The operation being tested

Use the unitary Fourier convention
\[
\widehat z(k,\ell)=\frac1L\sum_x z(x)e^{-2\pi i(kx_1+\ell x_2)/L},
\qquad
a(p,q)=b(p,q)+i/L.
\]

At a merged cluster, suppose the proposed interface produces
\[
\widetilde u=h+v,
\]
where:

* \(h=\sum_\alpha h_\alpha\) consists of explicitly supported local polynomial fields, with total support size at most \(s\);
* the radiative components, after summation, have a common-center angular representation. On a regular resonant chart, their canonical numerator is
  \[
  L\,a(p_k,q_k)\widehat v(k,\ell_k)
  =e^{-ic\cdot(p_k,q_k)}\,g(\theta_k),
  \qquad
  g(\theta)=\sum_{|\nu|\le N}g_\nu e^{i\nu\theta};
  \]
* the total preparation scale is \(\Lambda\). In particular,
  \[
  \Lambda\ge \sum_\alpha\|h_\alpha\|\ge\|h\|;
  \]
* \(\|\widetilde u-u\|\le\delta\|u\|\).

This is a precise, restricted model of the proposed merged-node operation. It allows arbitrary coefficients and cancellation. The local supports can be anywhere on the torus; they are not assumed to have small numerical diameter.

The exact sufficient interface requested in the question is the case \(\delta=0\).

## 2. An exact native counterfamily

For \(n\ge8\), set
\[
L=2^n,\qquad R=L/8,
\qquad
f=\delta_{(R,0)}+\delta_{(-R,0)}.
\]
Here \(m=2\), the weights have constant bit length, and the complete source description uses \(O(n)\) bits.

Let
\[
M=L/8,\qquad
p_k=\frac{2\pi k}{L},\quad 0\le k<M.
\]
On this interval, define
\[
q^*(p)=\arccos(3/2-\cos p).
\]
Choose \(q_k=2\pi\ell_k/L\) nearest to \(q^*(p_k)\). Since \(b(p_k,q^*(p_k))=0\),
\[
|b(p_k,q_k)|\le 2|q_k-q^*(p_k)|\le \frac{2\pi}{L}.
\]
Consequently, with the convenient constant \(C=7\),
\[
1\le |L\,a(p_k,q_k)|\le C. \tag{1}
\]

Thus these are actual discrete torus modes carrying a resonant denominator of order \(L\), not a zero-measure continuum shell.

The source numerator on this chart is exactly
\[
F_k=e^{-iRp_k}+e^{iRp_k}
    =2\cos(\pi k/4).
\]
Its squared norm is
\[
\sum_{k=0}^{M-1}|F_k|^2=2M.
\]
Equation (1) therefore gives
\[
\|u\|^2\ge \frac{2M}{C^2}=\frac{L}{4C^2}.
\]
The supplied bound on \(Z_0\) gives the complementary estimate
\[
\|u\|^2
=\|G(\cdot-(R,0))+G(\cdot+(R,0))\|^2
\le 4Z_0\le512L. \tag{2}
\]

These bounds use the exact finite damping and exact discrete frequencies. There is no periodization truncation, continuum replacement, or uncharged aliasing approximation.

### Angular bandwidth cannot be reduced by recentering

Take a monotone angular coordinate on this regular chart—for example
\[
\theta_k=\arg(\sin p_k+i\sin q_k).
\]
The \(q_k\) can be chosen nonincreasing, so these angles traverse an arc monotonically.

For any trigonometric polynomial \(g\) of degree
\[
N\le M/32=L/256
\]
and any unit-modulus sequence \(D_k\),
\[
\left\|F-Dg(\theta)\right\|_{\ell^2}
\ge \frac{\sqrt M}{8}. \tag{3}
\]
Allowing arbitrary \(D_k\) is stronger than allowing a different cluster center.

Here is an elementary proof. At the even samples \(k=2j\), \(|F_{2j}|\) alternates between \(2\) and \(0\). Call a sample bad if
\[
|F_{2j}-D_{2j}g(\theta_{2j})|\ge1/2.
\]
At good samples, the sign of
\[
|g(\theta)|^2-1
\]
must alternate. This is a real trigonometric polynomial of degree at most \(2N\), hence has at most \(4N\) zeros on the angular arc unless identically zero. The identically-zero case makes every sample bad.

Writing \(E\) for the number of bad samples, the remaining case gives
\[
M/2-1-2E\le4N,
\]
and hence \(E\ge M/8\). Therefore the squared approximation error is at least \(E/4\ge M/32\), proving the weaker constant in (3).

This is a bandwidth obstruction for the usual angular-polynomial representation, not merely for a particular choice of cluster center.

## 3. Local polynomial deflation cannot repair this at polynomial scale

Define the exact chart restriction operator
\[
(Tz)_k=L\,a(p_k,q_k)\widehat z(k,\ell_k).
\]
By (1) and unitarity of the Fourier transform,
\[
\|T\|\le C,\qquad Tu=F.
\]

For an \(s\)-supported local field,
\[
H_k=L\widehat h(k,\ell_k)
=\sum_xh(x)e^{-i(p_kx_1+q_kx_2)}
\]
satisfies
\[
|H_k|\le\|h\|_1\le\sqrt s\,\|h\|
\le\sqrt s\,\Lambda.
\]
It follows that
\[
\|Th\|_{\ell^2}
\le \frac{C\sqrt M\sqrt s}{L}\Lambda. \tag{4}
\]

Now write \(e=u-h-v\). Applying (3)–(4),
\[
\frac{\sqrt M}{8}
\le \|Th\|+\|Te\|
\le \frac{C\sqrt M\sqrt s}{L}\Lambda+C\delta\|u\|.
\]
Equation (2) implies \(\|u\|/\sqrt M\le64\). Thus
\[
\frac18\le\frac{C\sqrt s}{L}\Lambda+64C\delta.
\]

For the fixed constant
\[
\delta\le\delta_0:=\frac1{1024C},
\]
we obtain
\[
\boxed{\Lambda\ge\frac{L}{16C\sqrt s}}
\]
and therefore
\[
\boxed{\frac{\Lambda}{\|u\|}
\ge \frac1{16C\sqrt{512}}\sqrt{\frac Ls}.} \tag{5}
\]

### Quantified consequence

For every polynomial \(p\), all sufficiently large \(n\) rule out an interface on this family satisfying simultaneously
\[
N\le p(n),\qquad s\le p(n),\qquad
\Lambda\le p(n)\|u\|,\qquad
\|u-h-v\|\le\delta_0\|u\|.
\]

A directly checkable falsifier is:
\[
N\le L/256,\qquad
s\left(\frac{\Lambda}{\|u\|}\right)^2
<\frac{L}{131072C^2}.
\]
These conditions are incompatible with the claimed approximation.

This is not an unpaid coherence argument. Equation (5) explicitly charges cancellation between local and radiative parts. If those pieces are combined by the usual scale-based coherent preparation, its success is at most \(O(s/L)\); amplifying that particular preparation pays \(\Omega(\sqrt{L/s})\).

### Exact and near deflation are both covered

The ordinary Laurent source is
\[
F(X,Y)=X^R+X^{-R}.
\]
Its \(Y\)-width is zero, while \(P\) has \(Y\)-width two. Widths add under multiplication of nonzero Laurent polynomials, so \(P\nmid F\). Thus the paid exact-divisibility shortcut does not dispose of this family.

More importantly, the proof allowed **any** local \(h\). It therefore also covers attempted near-deflation. For a decomposition \(f=B_{\rm op}h+r\), the exact identity is
\[
u=h+A^{-1}(r-i\eta h).
\]
The correction \(-i\eta A^{-1}h\) must be included in the paid radiative components or represented by further paid components. It cannot be silently dropped.

The scale bound also applies to a purported sparse torus correction, independently of Laurent cuts.

## 4. What this falsifies—and what it does not

### Falsified operation

Local polynomial deflation cannot, in general, turn a cluster of binary-described radius \(R\) into a common-center radiative field whose ordinary angular bandwidth is polynomial in \(\log R\), while maintaining polynomial support and preparation scale.

Here \(R=L/8\), and a bandwidth of order \(L\) is required by the tested representation. The large oscillatory radiative numerator cannot be reassigned to a short local polynomial without paying the scale in (5).

The supplied continuum theorem does not remove this obstruction. Its bounded \(L^2\) sources, circular far-field transform, and angular subspaces are not the native lattice problem. No lattice nearorthogonality theorem was assumed in this proof.

### Not falsified

**This example does not force a correct tree algorithm to make the offending merge.** It can retain the two source centers. Indeed, its raw source-LCU success obeys the proved control
\[
\frac{\|u\|^2}{4Z_0}\ge\frac1{2048C^2}.
\]
Thus this is a noncancelling control family, not a hardness family.

Also, large bandwidth is not by itself a quantum circuit-size lower bound. A high-frequency character has a short binary description and can be implemented by phase arithmetic. The paid \(m=1\) primitive already handles translated Green states. What fails is replacing numerical bandwidth by bit length in the **angular compression and separation argument**.

A source-dependent radiative representation could escape the theorem. But then its inverse-output state preparation, clean uncomputation, cancellation-sensitive scale, and finite clock must be constructed. A small source-space Gram matrix does not supply that construction.

Finally, (5) obstructs the requested full-mode decomposition interface. It is not a TV-distance lower bound against an unrelated direct spatial sampler.

## 5. Resource accounting and remaining proof obligations

* **Input:** this counterfamily is generated and read in \(O(n)\) bit work. No hidden support or oracle is used.
* **Precision:** the obstruction survives fixed relative vector error \(\delta_0\). It does not rely on exponentially accurate numerical tests.
* **Chart access:** the \(M=L/8\) chart modes are an analytic witness, not a free enumerated data structure. An implementation that enumerates them pays \(\Omega(L)\) work.
* **Large local fields:** escaping (5) through support \(s=\Omega(L/\operatorname{poly}(n))\) is incompatible with an explicit polynomial-size local polynomial. An implicit dense field would require another constructive preparation theorem.
* **Classical control:** a charged full-grid FFT remains available in
  \[
  O\!\left(L^2\operatorname{poly}(n,B,\log(1/\epsilon))\right)
  \]
  bit work, followed by a \(2n\)-bit spatial sample. This is not polynomial in \(n\). The proposed classical \(m=1\) match is not a supplied verified primitive, so I do not grant a free classical Green evaluator or sampler.
* **No speedup inference:** neither this counterfamily nor failure of the compression operation establishes hardness or a quantum advantage.

To continue this mechanism, one would need one of two genuinely constructive results:

1. **An avoidance theorem:** a polynomial-bit-clock tree construction that never requires the failed compression and proves the total preparation-scale bound for every native input, including near-divisible sources. A failed separation certificate does not prove actual nonorthogonality or justify unrestricted merging.
2. **A replacement operation:** source-dependent, possibly high-bandwidth radiative components with explicit full-mode preparations, all corrections and uncomputations, known success bounds, and a polynomial finite clock.

Neither result follows from the supplied continuum nearorthogonality bounds. Retaining their numerical bandwidth in a separation condition also does not resolve the diameter-squaring issue.

**Stop point:** stable, radius-free common-center angular compression after local polynomial deflation is false. No complete universal compiler, smaller-promise endpoint, or new speedup is established by this cluster continuation.