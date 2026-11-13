## Decisive outcome: the uniform full-sector GAP promise is false

There is an explicit **rank-two collective deformation** satisfying the contract whose parent gap is exponentially small. The proof uses an exact ground-orthogonal trial vector, not just a permanent asymptotic.

For an absolute constant \(C\), and
\[
c=\frac12\log\frac{128}{125}>0,
\]
the construction below gives, for all sufficiently large \(N\),
\[
\boxed{\qquad
2\,4^{-N}\ \le\ \Delta(H_{P_N})
\ \le\ C N^5e^{-cN}.
\qquad}
\]
The matrices have rational complex entries requiring only \(O(\log N)\) bits each. Bounded padding gives a family for every \(N\), not merely a fixed-mode auxiliary model.

This falsifies the stated **full spectral-gap assertion**. It does not establish hardness of normalized sampling or a lower bound on every possible preparation algorithm.

---

## 1. Legal, explicitly encoded input family

First take \(N=4M\). Index modes by \((g,h)\), where \(g\in\{0,1,2,3\}\) and \(1\le h\le M\). Define
\[
u_{g,h}=\frac1{\sqrt N},\qquad
v_{g,h}=\frac{i^g}{\sqrt N}.
\]
These are orthonormal. Set
\[
\Pi=uu^\dagger+vv^\dagger,\qquad
P=\frac{I+\Pi}{2}.
\]
Thus
\[
\operatorname{spec}(P)=
\{1,1,\underbrace{\tfrac12,\ldots,\tfrac12}_{N-2}\},
\qquad
P^{-1}=2I-\Pi.
\]

The actual matrix entries are
\[
P_{(g,h),(g',h')}
=
\frac12\delta_{gg'}\delta_{hh'}
+\frac{1+i^{g-g'}}{2N}.
\]
They are exact rational complex numbers. Supplying the required dense list costs \(O(N^2\log N)\) bits; no succinct-input or precision loophole is used.

Let
\[
|\Omega\rangle=|1,\ldots,1\rangle,\qquad
n_u=a_u^\dagger a_u,\quad n_v=a_v^\dagger a_v,
\]
and define
\[
L=n_u+n_v,\qquad D=n_u-n_v.
\]
Since \(\Gamma(P)=2^{-N}2^L\) on the \(N\)-particle sector, the normalized ground state is
\[
|\psi\rangle=\frac{2^L|\Omega\rangle}{\sqrt Z},
\qquad
Z=\langle\Omega|4^L|\Omega\rangle
  =\operatorname{per}(I+3\Pi).
\]
Here \(I+3\Pi=4P^2\); the promised contraction is \(P\), not this rescaled Gram matrix.

---

## 2. Exact orthogonal trial vector and its Rayleigh quotient

Set
\[
F=\operatorname{sgn}(D),\qquad \operatorname{sgn}(0)=0.
\]

There is an exact exchange symmetry. Let \(R\) permute \(g\mapsto-g\pmod4\), and let
\[
T=\operatorname{diag}(i^g)R.
\]
Then \(Tu=v\), \(Tv=u\), and \(T\) commutes with \(P\). Also,
\[
\Gamma(T)|\Omega\rangle=(-1)^M|\Omega\rangle.
\]
Consequently the distribution of \(D\) in \(\psi\) is symmetric, so
\[
\langle\psi|F|\psi\rangle=0.
\]
Therefore
\[
|\phi\rangle
=\frac{F|\psi\rangle}
       {\sqrt{1-\Pr_\psi(D=0)}}
\]
is an **exactly ground-orthogonal trial vector**.

Every \(K_j\) is a number-conserving quadratic operator. In a mode basis containing \(u,v\), it changes \(D\) by at most \(2\). Hence, writing
\[
B_D=\mathbf 1_{\{|D|\le2\}},\qquad
p_N=\Pr_\psi(|D|\le2),
\]
we have the exact support identity
\[
[K_j,F]=[K_j,F]B_D.
\]
Because \(K_j\psi=0\),
\[
\|K_jF\psi\|
=\|[K_j,F]\psi\|
\le 2\|K_j\|\sqrt{p_N}.
\]
Using \(\|K_j\|\le2N+1\),
\[
\boxed{\quad
\Delta(H_P)
\le
\frac{4N(2N+1)^2p_N}{1-p_N}.
\quad}                                                    \tag{1}
\]

The remaining obligation is thus concrete: prove exponentially small **physical occupation probability** near \(D=0\).

---

## 3. An exact bridge from the Gaussian integral to physical occupations

The following coupling is what prevents this from being merely a norm/free-energy argument.

Let \(z,w\) be standard independent complex Gaussians. Gaussian moment expansion gives
\[
Z=
\frac1{\pi^2}\int_{\mathbb C^2}
e^{-|z|^2-|w|^2}
\prod_{j=1}^N
\left(1+\frac3N|z+i^{g_j}w|^2\right)
\,d^2z\,d^2w.                                             \tag{2}
\]
Let \(\mu_N\) denote this integrand normalized by \(Z\).

Let \(p_0(n,m)\) be the joint distribution of \(n_u,n_v\) in \(\Omega\). Their distribution in \(\psi\) is exactly
\[
p_\psi(n,m)=\frac{4^{n+m}p_0(n,m)}{Z}.                      \tag{3}
\]

### Exact auxiliary coupling

Draw \((n,m)\) from (3), then independently draw
\[
R_u\sim\operatorname{Bin}(n,3/4),\qquad
R_v\sim\operatorname{Bin}(m,3/4),
\]
followed by
\[
X\sim\operatorname{Gamma}(R_u+1,1),\qquad
Y\sim\operatorname{Gamma}(R_v+1,1).
\]
Then \((X,Y)\) has exactly the same law as
\[
(|z|^2,|w|^2)
\]
under \(\mu_N\).

To verify this, define
\[
C_{rs}=\mathbb E_0\!\left[
\binom{n_u}{r}\binom{n_v}{s}\right].
\]
The identity
\[
\operatorname{per}(I+b_1uu^\dagger+b_2vv^\dagger)
=
\mathbb E_0[(1+b_1)^{n_u}(1+b_2)^{n_v}]
\]
shows that its \(b_1^rb_2^s\) coefficient is \(C_{rs}\). Angular averaging in the Gaussian representation therefore gives radial density
\[
\frac{e^{-X-Y}}Z
\sum_{r,s}
\frac{3^{r+s}C_{rs}}{r!\,s!}X^rY^s.
\]
This is precisely a mixture of the stated Gamma distributions, with weights
\[
\frac{3^{r+s}C_{rs}}Z.
\]
The binomial draws from (3) produce those same weights.

These binomials are an exact algebraic coupling—not an approximation by an unconditional physical loss channel.

Conditioned on \(n,m\),
\[
\mathbb E[X-Y\mid n,m]=\frac34(n-m),
\]
and
\[
\operatorname{Var}(X-Y\mid n,m)
=\frac{15}{16}(n+m)+2\le N
\]
for \(N\ge32\).

If \(|n-m|\le N/9\), the conditional mean has magnitude at most \(N/12\). Chebyshev therefore gives, for \(N\ge288\),
\[
\Pr\!\left(|X-Y|\le N/6\mid n,m\right)
\ge 1-\frac{144}{N}\ge\frac12.
\]
Consequently,
\[
\boxed{\quad
\Pr_\psi(|D|\le N/9)
\le 2\,\mu_N\!\left(\big||z|^2-|w|^2\big|\le N/6\right).
\quad}                                                    \tag{4}
\]

This converts a Gaussian-integral bottleneck into a bottleneck in an actual bosonic number observable.

---

## 4. A finite-\(N\), exponentially small bottleneck bound

Rescale \(z=\sqrt N\,x,\ w=\sqrt N\,y\). Equation (2) becomes
\[
Z=\frac{N^2}{\pi^2}\int e^{N\Phi(x,y)}\,d^2x\,d^2y,
\]
where
\[
\Phi(x,y)=
-|x|^2-|y|^2+
\frac14\sum_{g=0}^3
\log\!\left(1+3|x+i^g y|^2\right).
\]

Write
\[
s=|x|^2+|y|^2,\qquad d=|x|^2-|y|^2.
\]
By arithmetic–geometric mean,
\[
\Phi(x,y)\le h(s):=-s+\log(1+3s).
\]
The maximum is
\[
\Phi_*=\log3-\frac23,
\qquad s_*=\frac23.
\]
Equality requires \(xy=0\). Thus the maximizers form two separate components: one with \(y=0\), the other with \(x=0\).

A quantitative bound is needed, rather than this saddle observation alone.

Let \(a=1+3s\), and write \(\bar xy=r+it\). The product inside the logarithm is
\[
(a^2-36r^2)(a^2-36t^2).
\]
Since
\[
r^2+t^2=\frac{s^2-d^2}{4},
\]
this product is at most
\[
\left[a^2-\frac92(s^2-d^2)\right]^2.
\]
Therefore, when \(1/3\le s\le1\) and \(|d|\le1/6\),
\[
\Phi(x,y)
\le h(s)+\frac12\log\!\left(1-\frac3{128}\right)
\le\Phi_*-c,
\]
with \(c=\tfrac12\log(128/125)\).

Outside that \(s\)-interval, the same bound follows from
\[
h(s)\le h(1/3)\quad(s\le1/3),\qquad
h(s)\le h(1)\quad(s\ge1),
\]
because both deficits from \(\Phi_*\) exceed \(c\). Hence
\[
\sup_{|d|\le1/6}\Phi(x,y)\le\Phi_*-c.                       \tag{5}
\]

### Controlling the integrals, including their tails

There is no unproved Laplace approximation here. First,
\[
\frac1{\pi^2}\int e^{\Phi(x,y)}\,d^2x\,d^2y
\le
\frac1{\pi^2}\int e^{-s}(1+3s)\,d^2x\,d^2y
=7.
\]
Thus the unnormalized mass of the strip in (5) is at most
\[
7N^2e^{(N-1)(\Phi_*-c)}.                                  \tag{6}
\]

For the denominator, discard the enhancement of mode \(v\):
\[
Z\ge\langle\Omega|4^{n_u}|\Omega\rangle
=N\int_0^\infty e^{Nh(s)}\,ds.
\]
Integrating just over \(s\in[2/3,\,2/3+1/N]\), where \(h''(s)\ge-1\), gives
\[
Z\ge e^{N\Phi_*-1/(2N)}.
\]
Combining this with (6), for \(N\ge2\),
\[
\mu_N\!\left(\big||z|^2-|w|^2\big|\le N/6\right)
\le 7N^2e^{-c(N-1)}.
\]
Equation (4) now proves the physical, macroscopic bottleneck:
\[
\boxed{\quad
\Pr_\psi(|D|\le N/9)
\le14N^2e^{-c(N-1)}
\qquad(N\ge288).
\quad}                                                    \tag{7}
\]

In particular, (7) bounds \(p_N=\Pr_\psi(|D|\le2)\).

---

## 5. Exponential parent-gap upper bound

For sufficiently large \(N\), the right side of (7) is at most \(1/2\). Substitution into the actual Rayleigh quotient (1) yields
\[
\boxed{\quad
\Delta(H_P)
\le
112N^3(2N+1)^2e^{-c(N-1)}
=O(N^5e^{-cN}).
\quad}                                                    \tag{8}
\]

All estimates above are finite-\(N\) inequalities. No finite-size fit is used.

For completeness, the generic similarity argument supplies the opposite exponential bound
\[
\Delta(H_P)\ge2\,\kappa(\Gamma(P))^{-2}\ge2\,4^{-N}.
\]
Indeed, writing \(S=\Gamma(P)\), decompose
\(S^{-1}\chi=\alpha\Omega+z\), \(z\perp\Omega\), for \(\chi\perp S\Omega\).
The gap \(2\) of \(H_I\) bounds the energy below by
\(2\sigma_{\min}(S)^2\|z\|^2\), while
\(\|\chi\|\le\|S\|\|z\|\).

### All-\(N\) extension

For arbitrary \(N\), put \(n=4\lfloor N/4\rfloor\) and use
\[
P_N=P_n\oplus I_{N-n}.
\]
Use the above trial state on the \(n\)-boson active block and one photon in each spectator mode. Spectator parent terms vanish, and the Rayleigh quotient is unchanged. Since \(N-n\le3\), (8) remains \(O(N^5e^{-cN})\).

This is a legal embedding with exactly one input photon per physical mode—not an embedding of a high-filling few-mode input.

---

## 6. Exact exchange symmetry is not essential to the spectral counterexample

The symmetric construction suffices to falsify the promised gap, but its trial vector lies in the opposite exchange sector. A simple rational perturbation removes that exact exchange symmetry while retaining the exponentially small gap.

For \(N=4M\), set
\[
\widetilde P=P-\frac1{4N}uu^\dagger.
\]
Its eigenvalues are
\[
1,\quad 1-\frac1{4N},\quad \frac12,\ldots,\frac12,
\]
and its entries still require \(O(\log N)\) bits.

Let
\[
\mathcal R=\left(1-\frac1{4N}\right)^{n_u}.
\]
Then
\[
\Gamma(\widetilde P)=\mathcal R\Gamma(P),\qquad
\widetilde K_j=\mathcal R K_j\mathcal R^{-1},
\]
and Bernoulli’s inequality gives
\[
\frac34 I\le\mathcal R\le I.
\]

Take the normalized trial vector \(\phi\) above and orthogonally project
\(\mathcal R\phi\) away from \(\mathcal R\psi\). Its norm is at least \(3/4\), while its parent-energy numerator is at most the original numerator. Therefore its Rayleigh quotient increases by at most \(16/9\).

Thus the asymmetric family also has gap \(O(N^5e^{-cN})\). This requires neither exponentially fine input precision nor an exact exchange-sector decomposition.

The projection here is a mathematical variational construction, not a supplied reflection or overlap oracle.

---

## What this establishes—and what it does not

**Proved deductions**

- The contract’s uniform inverse-polynomial **full-sector** gap assertion is false.
- The near-zero vector is genuinely ground-orthogonal, with an explicit Rayleigh bound.
- The Gaussian free-energy barrier is connected to a physical occupation bottleneck by an exact positive coupling.
- The resulting small joint residuals of the \(K_j\) are an actual nonnormal near-kernel phenomenon; integer eigenvalues of individual \(K_j\) do not prevent it.
- The input and inverse matrices have polynomial-size, logarithmic-precision encodings.

**Limits**

- The uniform rank-one family alone is not resolved by this proof. Its radial condensation saddle does not provide the two-component bottleneck used here.
- An exponentially small full gap is not, by itself, a preparation-time or sampling-hardness lower bound. In particular, symmetry-restricted evolution matters for the symmetric version.
- No classical same-output sampler is established. No unconditional loss approximation is substituted for the normalized all-\(N\)-particle law.

**Cost accounting**

The witness is analytically specified, not supplied as a cheaply prepared state. Since \(D\) has integer spectrum in \([-N,N]\), \(\operatorname{sgn}(D)\) also has an exact degree-at-most-\(2N\) interpolation-polynomial description; this does not make preparation of \(\psi\) free. No preparation, reflection, precision, or sampling-output cost is waived. An eventual sampler would still owe the dense-input access, its \(\eta\)-dependent preparation/precision costs, and occupation-output costs.

The remaining algorithmic questions are unresolved. **The stated all-\(P\), full spectral-gap promise is not: the family above falsifies it.**