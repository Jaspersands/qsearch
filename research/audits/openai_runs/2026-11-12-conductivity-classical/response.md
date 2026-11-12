# Classical attack: paid accelerated contrast sampling

## Result and scope

I can establish a **fully paid, all-circuit classical upper bound**, including a kernel sampler, but not the requested joint polynomial bound.

For fixed \(\rho>1\), the resulting bit complexity is
\[
\boxed{
\operatorname{poly}\!\left(B,n,\log(1/\epsilon),\log(1/\delta),
\text{input bit lengths}\right)
\,\epsilon^{-2}
\exp\!\left[
O_\rho\!\bigl(\log(1/\epsilon)\log(n+1)\bigr)
\right].
}
\]
No \(N\)-entry materialization, solution samples, or stochastic assumptions on the material are used.

Thus this is polynomial in \(n\) for fixed accuracy, and quasipolynomial when \(1/\epsilon=\operatorname{poly}(n)\). It does **not** establish \(\operatorname{poly}(B,n,1/\epsilon)\). The remaining nonpolynomial factor is an explicitly bounded signed-path variance—not an unpaid Riesz-kernel evaluation lemma.

The construction below also improves the usual contrast-series convergence factor. I make no claim that this is the optimal classical algorithm.

---

## 1. An accelerated contrast series through the same projection

Write
\[
\Pi=D(D^*D)^+D^*,\qquad \mathcal R=2\Pi-I.
\]
Then \(\mathcal R\) is an orthogonal reflection, \(\|\mathcal R\|=1\), and
\[
\mathcal R\eta_j=-\eta_j.
\]

The arithmetic-center Neumann series has contrast factor
\[
h=\frac{\rho-1}{\rho+1}.
\]
A directly derived reflection formulation improves this to
\[
a_*=\sqrt{\rho},\qquad
r=\frac{\sqrt{\rho}-1}{\sqrt{\rho}+1}<h.
\]
Let \(F=\operatorname{diag}(\sigma_e)\), where \(\sigma_e=+1\) on conductivity-\(\rho\) edges and \(-1\) otherwise. Then
\[
\frac{A/a_*-I}{A/a_*+I}=rF,
\qquad
A=a_*(I+rF)(I-rF)^{-1}.
\]

Here is the derivation, including normalization. Let the minimizing normalized electric field be
\[
E=\eta_j+D\psi,\qquad J=AE.
\]
Its Euler equation is \(\Pi J=0\), while \((I-\Pi)E=\eta_j\). Set
\[
w=(I-rF)^{-1}E.
\]
Adding these two projected equations gives
\[
(I+r\mathcal RF)w=\eta_j.
\]
Moreover, \(K_j=\langle\eta_j,J\rangle\), and taking the inner product of this equation with \(\eta_j\) yields
\[
\boxed{
K_j=a_*\left[
1+2\sum_{m=0}^{\infty}(-1)^m r^{m+1}\nu_m
\right],
\quad
\nu_m=\langle\eta_j,F(\mathcal RF)^m\eta_j\rangle .
}
\]
Since \(|\nu_m|\le1\), truncation after \(m=M\) has error at most
\[
\frac{2a_*r^{M+2}}{1-r}.
\]
Choose the least nonnegative \(M\) making this at most \(\epsilon/4\). Thus
\[
M=\frac{\log(1/\epsilon)}{\log(1/r)}+O_\rho(1).
\]

This argument uses no normalized corrector or source vector. The square root of fixed rational \(\rho\) is an algebraic constant whose arithmetic is charged below.

---

## 2. A kernel sampler without evaluating a large Fourier sum

The following construction supplies the missing sampling mechanism.

Put
\[
K_0=D^*D,\qquad H_t=e^{-tK_0},\qquad T=L^2.
\]
Fourier diagonalization gives
\[
\Pi=\int_0^T DH_tD^*\,dt+Q_\infty,
\]
where, for nonzero canonical frequency \(k\),
\[
\widehat Q_\infty(k)
=e^{-T\lambda(k)}\frac{d(k)d(k)^*}{\lambda(k)},\quad
d_i(k)=e^{2\pi i k_i/L}-1,\quad
\lambda(k)=\sum_i|d_i(k)|^2.
\]
The zero-frequency value is zero.

Consequently, \(\mathcal R\) is a sum of
\[
s=2n+3
\]
components:

* \(-I\);
* \(2\int_0^1DH_tD^*dt\);
* \(2\int_{2^\ell}^{2^{\ell+1}}DH_tD^*dt\), for \(0\le\ell<2n\);
* \(2Q_\infty\).

Each component has a constant-second-moment row sampler.

### 2.1 Dyadic heat blocks

The homogeneous heat semigroup has the exact representation
\[
(H_tf)(x)=\mathbb E f(x+Z),
\]
where each coordinate of \(Z\) is the difference of two independent \(\operatorname{Poisson}(t)\) variables, reduced modulo \(L\).

Consider a block \([U,2U]\), \(U\ge1\), and a starting edge \((x,i)\).

1. Choose output direction \(\ell\) uniformly from \(\{1,2\}\).
2. Choose \(t\) uniformly in \([U,2U]\), and put \(\tau=t/2\).
3. Generate two independent heat increments \(Z_1,Z_2\), each at time \(\tau\), retaining their Poisson counts.
4. Define
   \[
   A_i=\frac{P^{(1)}_{i,+}}{\tau}-1,\qquad
   B_\ell=\frac{P^{(2)}_{\ell,-}}{\tau}-1.
   \]
5. Return edge \((x+Z_1+Z_2,\ell)\) with weight
   \[
   w=4U A_iB_\ell.
   \]

The Poisson identity
\[
\mathbb E[P\,g(P)]=\tau\,\mathbb E[g(P+1)]
\]
shows that this represents the row of
\[
2\int_U^{2U}DH_tD^*\,dt.
\]
The plus count implements the forward difference; the minus count implements the adjoint difference.

Crucially, the two groups are independent even when \(i=\ell\), so
\[
\mathbb E[A_i^2B_\ell^2]=\tau^{-2}=\frac4{t^2},
\qquad
\mathbb E[w^2]\le64.
\]
This is an exact moment calculation, not an independence assumption about conductivities.

### 2.2 The short-time block

For \(0\le t\le1\), expand the two differences directly.

Choose \(\ell\) uniformly, \(b,c\in\{0,1\}\) independently uniformly, and a heat increment \(Z\) at time \(t\). Return
\[
(x+Z+b e_i-c e_\ell,\ell)
\]
with weight
\[
w=16(2b-1)(2c-1).
\]
Averaging over \(t\in[0,1]\) represents the short-time component. Its second moment is \(256\).

### 2.3 The long-time Fourier remainder

Sample \(k\in\mathbb Z^2\) from
\[
q(k)=\frac19\,2^{-|k_1|-|k_2|}.
\]
This is normalized and can be sampled using geometric random variables.

If \(k=0\) or lies outside the canonical frequency square, return weight zero. Otherwise choose \(y\) uniformly from the torus and \(\ell\) uniformly from the two directions. Return \((y,\ell)\) with weight
\[
w=
\frac{4e^{-T\lambda(k)}}{q(k)}
\operatorname{Re}\!\left[
\frac{d_i(k)\overline{d_\ell(k)}}{\lambda(k)}
e^{2\pi i k\cdot(x-y)/L}
\right].
\]
The factors \(4\), \(1/N\), and the direction probability give exactly \(2Q_\infty\).

For canonical \(k\),
\[
T\lambda(k)\ge16|k|^2.
\]
Therefore, for nonzero integer \(k\),
\[
|w|
\le36e^{-16|k|^2+(\log2)|k|_1}
\le36e^{-(16-\log2)|k|^2}<1.
\]
Only one frequency is evaluated—not an \(N\)-term Fourier sum.

### 2.4 Combining components

Choose one of the \(s\) components uniformly and multiply its returned weight by \(s\). The identity component simply returns the starting edge with weight \(-1\).

After the finite-precision modifications below, this produces a random edge \(e'\) and weight \(W\) satisfying
\[
\mathbb E[Wf(e')\mid e]=(\widetilde{\mathcal R}f)(e),
\qquad
\boxed{\mathbb E[W^2\mid e]\le V:=(16s)^2.}
\]
The bound is uniform over starting edges and over all coefficient circuits.

---

## 3. Paying time sampling, Poisson generation, and precision

### Finite time meshes

Continuous random times are unnecessary. Use a \(p\)-bit uniform left-endpoint mesh in every interval.

For a dyadic block, its longitudinal Fourier multiplier is an integral of
\[
2u e^{-u(1+v)},\qquad v\in[0,1],\quad u=U\lambda.
\]
Its mesh error is at most \(2e^{-1}2^{-p}\), uniformly in \(u\). The short-time block has error at most \(16\,2^{-p}\), since \(\lambda\le8\).

Round each Fourier-remainder sample weight to absolute error at most \(2^{-p}\). Because its destination is uniform over edges, the resulting error matrix has row and column absolute sums at most \(2^{-p}\), hence operator norm at most \(2^{-p}\).

Thus
\[
\|\widetilde{\mathcal R}-\mathcal R\|\le8s\,2^{-p}.
\]

Choose
\[
\zeta=\min\left\{
1,\frac{1-r}{2r},
\frac{\epsilon(1-r)^2}{64a_*r^2}
\right\},
\qquad
p=\left\lceil\log_2\frac{8s}{\zeta}\right\rceil.
\]
Then \(\|\widetilde{\mathcal R}-\mathcal R\|\le\zeta\).

Telescoping products gives
\[
|\widetilde\nu_m-\nu_m|
\le m\zeta(1+\zeta)^{m-1}.
\]
Consequently, the total error in the truncated conductivity series is bounded by
\[
2a_*\zeta r^2
\bigl[1-r(1+\zeta)\bigr]^{-2}
\le\epsilon/8.
\]
Only \(p=O_\rho(\log((n+1)/\epsilon))\) fractional bits are required for the kernel approximation.

### Large Poisson parameters are not simulated step by step

The largest Poisson mean is \(O(L^2)\), but its binary representation has only \(O(n+p)\) bits.

Here is an implementable bit-cost route, rather than a constant-time Poisson oracle:

* For mean \(\lambda\le1\), use inverse-CDF sampling with interval arithmetic.
* For \(\lambda\ge1\), use a two-sided geometric proposal centered at \(\lfloor\lambda\rfloor\), with scale
  \[
  u=\left\lceil64\sqrt{\lambda+1}\right\rceil.
  \]
  Its mass is proportional to \(e^{-|k-\lfloor\lambda\rfloor|/u}\).
* Elementary Poisson probability-ratio bounds and the factorial bound give a constant rejection envelope; \(4096\) is a conservative admissible constant.
* A two-sided geometric draw is the difference of two geometric draws. These can be generated by inverse transforms using logarithms, without taking \(u\) individual steps.
* Acceptance probabilities are evaluated through logarithms and \(\log(k!)\). Stirling expansion with a certified remainder, using direct summation for small arguments, computes these in polynomial bit work.

Exact comparisons can be implemented by refining intervals against fresh random bits. Expected work is polynomial in parameter bit length. To obtain a bounded runtime, cap rejection attempts and interval refinements at polynomially many bits in
\[
n+p+\log(Q(M+1)/\delta),
\]
where \(Q\) is the sample count below. Couple this implementation to the exact sampler and charge all cap events to a \(\delta/2\) failure budget.

Thus no operation proportional to the Poisson mean is hidden.

### Other arithmetic

The Fourier denominator can be as small as \(\Theta(L^{-2})\). Its evaluation therefore explicitly uses \(O(n)\) additional precision bits. Exponentials, trigonometric functions, and division are computed with certified finite precision.

Frequencies with \(|k|\) exceeding \(O(\sqrt p)\) can be assigned zero weight once the displayed exponential bound certifies error below \(2^{-p}\). This also avoids constructing enormous importance-weight denominators.

Products along a path have polynomial bit length in \(M,n,p\) and the cap parameters. The constants involving \(\sqrt\rho\) have algebraic degree at most two and can be evaluated rigorously at the required precision.

---

## 4. Scalar estimator and explicit work bound

Start from a uniformly sampled node \(x_0\), with direction \(i_0=j\). This costs \(2n\) random bits, not preparation of a solution distribution.

For a length-\(m\) path, use fresh kernel-sampler randomness at each step and define
\[
Z_m=
\left(\prod_{t=0}^{m}\sigma(e_t)\right)
\left(\prod_{t=1}^{m}W_t\right)
\mathbf1_{\{i_m=j\}}.
\]
For \(m=0\), this is simply \(\sigma(x_0,j)\).

The uniform starting node supplies exactly the \(1/N\) normalization:
\[
\mathbb E Z_m=\widetilde\nu_m,
\qquad
\mathbb E Z_m^2\le V^m.
\]
The second assertion follows by conditioning successively on the path history. Conductivities along the path can be arbitrarily correlated.

Define the explicit integer and geometric sum
\[
\Gamma=\max\{1,\lceil16rs\rceil\},
\qquad
G_M=\sum_{m=0}^{M}\Gamma^m.
\]
Choose the degree with probability
\[
p_m=\Gamma^m/G_M
\]
and return
\[
Y=\frac{2a_*\,(-1)^m r^{m+1}Z_m}{p_m}.
\]
Degree sampling uses integer weights with \(O(M\log(\Gamma+1))\) bits. Since \(\Gamma\ge r\sqrt V\),
\[
\boxed{\mathbb E Y^2\le(2a_*rG_M)^2.}
\]

Median-of-means therefore requires
\[
\boxed{
Q=O_\rho\!\left(
\epsilon^{-2}
\left[\sum_{m=0}^{M}\lceil16r(2n+3)\rceil^m\right]^2
\log(2/\delta)
\right)
}
\]
independent trajectories. This is the precise nonpolynomial sampling factor.

Round each completed \(Y\) to absolute error \(\epsilon/16\), rather than repeatedly summing unrelated rational denominators. Allocate \(\epsilon/2\) to statistical error and \(\epsilon/16\) to final output rounding. Together with the truncation and kernel budgets, the total error is at most \(\epsilon\).

### Charged work

Each trajectory uses at most:

* \(M+1\) evaluations of the actual supplied Boolean circuit;
* \(M\) kernel transitions;
* polynomial-bit arithmetic and random-bit generation.

Reading the circuit and numerical inputs is charged. Circuit evaluation is not treated as a unit-cost oracle. If \(b_{\rm in}\) denotes numerical-input description length, a conservative complete form is
\[
Q(M+1)\,
\operatorname{poly}\!\left(
B,n,p,M,\log G_M,\log(Q/\delta),b_{\rm in}
\right)
\]
bit operations, with polynomial working storage and a scalar output of \(O(\log(1/\epsilon))\) bits.

Using \(G_M\le(M+1)\Gamma^M\) gives the bound stated at the beginning. One may also take the minimum with a fully paid full-grid solve when that is cheaper.

---

## 5. Explicit falsifier for a constant signed-path variance claim

The operator contraction \(\|\mathcal R\|=1\) does **not** imply constant variance for this sampler.

Take the succinct, balanced layered family
\[
\sigma(x,\ell)=
\begin{cases}
+1,&0\le x_1<L/2,\\
-1,&L/2\le x_1<L,
\end{cases}
\]
for both edge directions. The circuit only needs the most significant bit of \(x_1\).

In fact, the following calculation works for every two-phase input: all phase factors disappear when \(Z_m\) is squared.

Let \(H=2n\) be the number of dyadic heat components. On any such component,
\[
\mathbb E[w^2]\ge16
\]
even with the finite left-endpoint mesh. Restricting to paths that select heat components at every step yields
\[
\boxed{
\mathbb E Z_m^2\ge
\frac12(16sH)^m.
}
\]
The final factor \(1/2\) is the probability of ending in direction \(j\); the squared-moment transition totals are direction-independent.

For the ideal exact kernel, \(|\mathbb E Z_m|\le1\). Already \(m=1\) therefore has variance \(\Omega(n^2)\), and the higher-order second moments grow as \(n^{2m}\).

This explicitly falsifies a proposed \(C^m\), \(n\)-independent variance bound **for this independent signed-path construction**.

It is not a classical lower bound. These layered materials are easy by harmonic/arithmetic means, and preprocessing, control variates, correlated estimators, or a different construction could avoid this waste.

---

## 6. What remains open, and what would falsify the report

A sufficient route to genuine dequantization would be an all-circuit estimator for the required degree-\(m\) moments having both
\[
\text{work}=\operatorname{poly}(B,n,m),
\qquad
\text{second moment}\le \operatorname{poly}(n)\,C_\rho^m,
\]
with the polynomial degree independent of \(m\). Since \(m=O_\rho(\log(1/\epsilon))\), that would give the target joint polynomial bound. This report does not supply it.

The concrete proof obligations for independent checking are:

1. The reflection energy identity, including \(1/N\) normalization and the zero mode.
2. The Poisson score identities and their conditional second moments.
3. The uniform quadrature/operator-error bounds.
4. The rejection-envelope and capped bit implementation—not merely a library call claiming constant-time Poisson sampling.

Constant phases analytically reduce to \(K=1\) or \(\rho\). Layers must give the harmonic mean normal to layers and arithmetic mean parallel to them. A frozen \(L=4\) rational solve would be a useful transcription falsifier, but **no finite controls were executed here**, and they would not establish scaling.

Finally, the supplied Mourrat theorem remains an IID/ensemble baseline. Randomly translating an arbitrary periodic circuit does not supply independence or quantitative decorrelation. None of that theorem’s stochastic error rates has been imported here.

**Admission consequence:** the full-grid-only comparison is inadequate, because a constructive subgrid classical algorithm exists. But the requested polynomial classical endpoint remains unproved; neither that gap nor this sampler’s variance counterexample establishes hardness or quantum advantage.