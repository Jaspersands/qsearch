## Decisive result

**The single-source primitive has a classical finite-clock algorithm with total bit work \(\operatorname{poly}(n,1/\epsilon)\).** No Green-function, normalization, or sampling oracle is needed.

The construction below uses:

1. an exact one-dimensional integral for the **lattice** Green function;
2. a uniform stationary-phase estimate, with its error proved independently of \(L\);
3. a rigorously truncated periodization containing only \(O((n+\log(1/\epsilon))^2)\) images;
4. rejection sampling from an explicitly samplable spatial proposal.

The constants and polynomial exponents are deliberately loose. This is a bit-complexity result, not a practical-runtime estimate. It makes no claim about novelty, quantum advantage, or the normalization of arbitrary multisource superpositions.

---

# 1. Theorem and normalization bounds

Write
\[
h(p,q)=-3+2\cos p+2\cos q,\qquad \eta=L^{-1},
\]
and
\[
G_L(x)=\frac1{L^2}\sum_{k\in(\mathbb Z/L\mathbb Z)^2}
 \frac{e^{2\pi i k\cdot x/L}}
 {h(2\pi k_x/L,2\pi k_y/L)+i/L}.
\]

### Theorem

There is a classical randomized algorithm which, given \(n\ge2\), \(L=2^n\), and a positive rational tolerance \(\epsilon\), outputs a site whose law is within \(\epsilon\) in total variation of
\[
P_L(x)=\frac{|G_L(x)|^2}{Z_L},
\qquad
Z_L=\sum_x|G_L(x)|^2.
\]

Its worst-case clock, including input processing, finite-precision arithmetic, random-bit generation, rejection caps, and the \(2n\)-bit output, is polynomial in \(n,1/\epsilon\) and the explicit input length. For the usual dyadic error specification this is \(\operatorname{poly}(n,1/\epsilon)\).

Moreover, uniformly for all allowed \(L\),
\[
\boxed{\frac{L}{512}\le Z_L\le64L.} \tag{1}
\]

The algorithm does not evaluate \(Z_L\); these bounds suffice.

### Proof of (1): exact lattice counting

Parseval gives
\[
Z_L=\frac1{L^2}\sum_k\frac1{h(k)^2+L^{-2}}, \tag{2}
\]
where \(h(k)\) denotes the sampled symbol.

For the lower bound, take
\[
k_x=0,\ldots,\lfloor L/12\rfloor,\qquad
p=2\pi k_x/L.
\]
Then \(0\le p\le\pi/6\), and the exact resonant ordinate
\[
q_*(p)=\arccos\!\left(\frac32-\cos p\right)
\]
exists. Choose the nearest Fourier-grid ordinate \(q\). Since
\[
|q-q_*|\le\pi/L,\qquad |\partial_q h|\le2,
\]
we have \(|h(p,q)|\le2\pi/L\). Each chosen mode contributes at least
\[
\frac1{1+4\pi^2}
\]
to (2). There are at least \(L/12\) such modes, proving
\[
Z_L\ge \frac{L}{12(1+4\pi^2)}\ge\frac L{512}.
\]

For the upper bound, let
\[
N(s)=\#\{k:|h(k)|\le s\},\qquad 0<s\le1/4.
\]
On this strip,
\[
\cos p+\cos q\in[11/8,13/8].
\]
Both cosines are positive, and at least one of \(|\sin p|,|\sin q|\) is at least \(1/2\). Cover by the two corresponding coordinate charts. On either signed monotone chart the relevant derivative of \(h\) has magnitude at least one. Counting grid points in intervals of length at most \(2s\) gives
\[
N(s)\le4L+\frac4\pi L^2s. \tag{3}
\]
Use (3) on \(|h|\le L^{-1}\) and successive dyadic bands up to \(|h|=1/4\). Their contributions form convergent geometric sums of order \(L\). The remaining modes contribute at most \(16\). The loose upper bound \(64L\) follows.

No continuum density-of-states approximation is used.

---

# 2. Exact infinite-lattice kernel and periodization

Define the infinite-lattice kernel
\[
g_\eta(y)=\frac1{(2\pi)^2}
 \int_{[-\pi,\pi]^2}
 \frac{e^{i(p y_1+q y_2)}}{h(p,q)+i\eta}\,dp\,dq.
 \tag{4}
\]

Two different bounds will be useful:

* a coarse exponential bound, for the periodization tail;
* an oscillatory \(r^{-1/2}\) bound, for efficient spatial rejection sampling.

## 2.1 Coarse exponential bound

Shift each Fourier contour by
\[
p_j\longmapsto p_j+i\frac{\eta}{16}\operatorname{sgn}(y_j).
\]
For \(0<\eta\le1/4\),
\[
|\operatorname{Im}h(p+i s_1,q+i s_2)|
 \le4\sinh(\eta/16)\le\eta/2.
\]
The denominator therefore stays at least \(\eta/2\) in magnitude throughout the deformation. Consequently,
\[
\boxed{
 |g_\eta(y)|\le \frac2\eta
 e^{-\eta\|y\|_1/16}.
} \tag{5}
\]

This proves absolute summability and justifies the exact identity
\[
\boxed{
G_L(x)=\sum_{z\in\mathbb Z^2}g_{1/L}(x+Lz).
} \tag{6}
\]

Thus periodization is not being assumed on the basis of a free-space asymptotic formula.

## 2.2 A uniform image-tail bound

Represent \(x\) in
\[
[-L/2,L/2-1]^2.
\]
From (5), grouping images by \(\|z\|_\infty=s\),
\[
\left|
 \sum_{\|z\|_\infty>M}g_{1/L}(x+Lz)
\right|
 \le 16Le^{1/16}\sum_{s>M}s e^{-s/16}.
\]
In particular, the following convenient rational bound holds:
\[
\boxed{
\sup_x |\text{image tail}|
 \le 2^{15}L(M+1)(31/32)^M.
} \tag{7}
\]

For any \(0<\epsilon\le1/4\), put
\[
s=\left\lceil\log_2(1/\epsilon)\right\rceil.
\]
For example,
\[
M=128(n+s+20) \tag{8}
\]
makes the right side of (7) at most
\[
\frac{\epsilon}{2^{14}L}. \tag{9}
\]
The generous constants in (8) merely avoid a search for the smallest cutoff.

There are only \(O(M^2)\) retained images.

---

# 3. The needed lattice-kernel evaluator is constructible

The central analytic ingredient is the following.

### Kernel lemma

There is an effective absolute constant \(C_g\) such that, for \(0<\eta\le1/4\),
\[
\boxed{
|g_\eta(y)|\le \frac{C_g}{\sqrt{1+\|y\|_\infty}}.
} \tag{10}
\]

Further, given \(y\), \(\eta=1/L\), and \(0<\delta\le1\), a deterministic finite-bit algorithm returns a rational complex number \(\widetilde g_\eta(y)\) satisfying
\[
\boxed{
|\widetilde g_\eta(y)-g_\eta(y)|
 \le \frac{\delta}{\sqrt{1+\|y\|_\infty}}
} \tag{11}
\]
in
\[
\operatorname{poly}\bigl(n,\log(2+\|y\|_\infty),1/\delta\bigr)
\]
bit work.

Here is a proof and the actual evaluation formula.

## 3.1 Exact one-dimensional residue formula

By coordinate reflections and interchange, reduce to
\[
a=\max(|y_1|,|y_2|),\qquad
b=\min(|y_1|,|y_2|),\qquad 0\le b\le a.
\]

Define
\[
p_\eta(q)=\arccos\!\left(\frac32-\cos q-\frac{i\eta}{2}\right),
\]
on the branch with \(\operatorname{Im}p_\eta>0\). Integrating the first momentum variable by residues gives the exact formula
\[
\boxed{
g_\eta(a,b)=
-\frac{i}{4\pi}\int_{-\pi}^{\pi}
 \frac{e^{\,i a p_\eta(q)+i bq}}{\sin p_\eta(q)}\,dq.
} \tag{12}
\]

The apparent turning-point singularities of this representation are handled by a fixed contour deformation, not by resolving a width-\(\eta\) feature with \(O(1/\eta)\) nodes.

## 3.2 A fixed, nonsingular contour

Take \(\tau=10^{-6}\). Let \(\chi(s)\) be an even fixed \(C^8\) function satisfying
\[
\chi(s)=0\quad(|s|\le4/5),\qquad
\chi(s)=1\quad(|s|\ge9/10),
\]
and increasing between these intervals. It can be an explicitly evaluable piecewise polynomial. For example, use the normalized integral of \(u^8(1-u)^8\) as the transition polynomial.

Deform to
\[
q(s)=s-i\tau\chi(s)\sin s,\qquad -\pi\le s\le\pi. \tag{13}
\]

This deformation is valid for every \(\eta>0\). Indeed, throughout its homotopy,
\[
\operatorname{Im}\!\left(\frac32-\cos q-\frac{i\eta}{2}\right)<0,
\]
so the chosen branch is never crossed.

There are uniform, effective bounds
\[
|\sin p_\eta(q(s))|\ge c>0, \tag{14}
\]
and, for every \(0\le\theta\le1\),
\[
\operatorname{Im}\bigl(p_\eta(q(s))+\theta q(s)\bigr)\ge0. \tag{15}
\]

For completeness, the useful part of (15) can be checked directly. For \(s\ge4/5\), write
\[
q=s-it,\qquad p_\eta(q)=u+iv,\qquad 0\le t\le\tau.
\]
The dispersion equation gives
\[
\cos u\cosh v=\frac32-\cos s\cosh t,
\]
\[
\sin u\sinh v=\sin s\sinh t+\eta/2.
\]
For \(4/5\le s\le\pi/2\), assuming \(v\le1.1t\) makes the first equation imply \(\sin u<0.601\); the second requires a value exceeding \(0.71\sinh t\), whereas its left side is less than \(0.662\sinh t\). This is impossible. For \(s\ge\pi/2\), the first equation gives \(v\ge\operatorname{arcosh}(3/2)>\tau\). Negative \(s\) follows by symmetry.

Thus \(v\ge1.1t\) where a deformation is needed. Away from the central patch, the phase has a fixed positive imaginary part. A conservative bound in (14), uniform for \(0<\eta\le1/4\), is obtainable with \(c=1/2000\).

All contour and derivative constants below are therefore computable from fixed polynomial coefficients and explicit nonzero-denominator bounds.

## 3.3 Uniform stationary phase, using the exact dispersion curve

For small fixed \(\eta\), say \(0<\eta\le\eta_*=10^{-6}\), define
\[
p_0(q)=\arccos\!\left(\frac32-\cos q\right)
\]
on the central real patch.

When \(a>0\), put \(\theta=b/a\). The real phase
\[
\phi_\theta(q)=p_0(q)+\theta q
\]
has a unique stationary point \(q_\theta\), determined by
\[
\sin q_\theta=\theta\sin p_0(q_\theta).
\]
It satisfies
\[
0\le q_\theta\le\arccos(3/4)<3/4.
\]
Furthermore,
\[
p_0''(q)=-
 \frac{\cos q+\cos p_0(q)\,[p_0'(q)]^2}{\sin p_0(q)}<0. \tag{16}
\]
Thus the stationary point is uniformly nondegenerate; there is no caustic in this chart.

Let
\[
H_\theta=-p_0''(q_\theta)
 =\frac{\cos q_\theta+\theta^2\cos p_0(q_\theta)}
        {\sin p_0(q_\theta)}.
\]
Then
\[
\boxed{
g_\eta(a,b)=
-\frac{i}{4\pi}
 \sqrt{\frac{2\pi}{aH_\theta}}\,
 \frac{
  \exp\!\left(i a p_\eta(q_\theta)+i bq_\theta-i\pi/4\right)}
 {\sin p_\eta(q_\theta)}
 +R_\eta(a,b),
} \tag{17}
\]
with
\[
\boxed{|R_\eta(a,b)|\le C a^{-3/2}} \tag{18}
\]
uniformly in \(a\ge1\), \(0\le b\le a\), and \(0<\eta\le\eta_*\).

### Why the remainder is uniform as \(\eta\to0\)

On a fixed central cutoff, factor the integrand as
\[
e^{ia\phi_\theta(q)} A_{a,\eta}(q),
\qquad
A_{a,\eta}(q)=
 \frac{\chi_c(q)}{\sin p_\eta(q)}
 e^{ia[p_\eta(q)-p_0(q)]}.
\]
Here \(\chi_c=1\) on \(|q|\le3/4\) and vanishes before \(|q|=4/5\).

On this patch,
\[
\operatorname{Im}p_\eta(q)\ge c\eta,\qquad
\partial_q^j[p_\eta(q)-p_0(q)]=O_j(\eta).
\]
Consequently,
\[
\|A_{a,\eta}\|_{C^4}
 \le C e^{-c a\eta}\bigl(1+(a\eta)^4\bigr)
 \le C'. \tag{19}
\]
This bound, rather than an assumption that \(a\eta\) is small, is what supplies uniformity.

A smooth Morse change of variable makes the central phase
\[
\phi_\theta(q_\theta)-t^2/2.
\]
For the resulting compactly supported amplitude \(H(t)\), Fourier inversion and the Gaussian integral give
\[
\int e^{-iat^2/2}H(t)\,dt
=
\sqrt{\frac{2\pi}{a}}e^{-i\pi/4}
\frac1{2\pi}\int \widehat H(\xi)e^{i\xi^2/(2a)}\,d\xi.
\]
Using
\[
|e^{i\xi^2/(2a)}-1|\le \frac{\xi^2}{2a},
\]
the error is bounded by
\[
C a^{-3/2}\int \xi^2|\widehat H(\xi)|\,d\xi.
\]
The integral is uniformly bounded by the compact-support and \(C^4\) bounds. This proves the central contribution to (18).

On the intervening contour patches, the phase derivative is bounded away from zero, so two integrations by parts give \(O(a^{-2})\). On the outer patch, (15) is strictly positive and gives \(O(e^{-ca})\). Both fit within (18).

For \(\eta\ge\eta_*\), (5) itself implies a uniform \(Ca^{-3/2}\) bound. Thus a zero approximation can be used for sufficiently large \(a\) in that fixed-\(\eta\) regime.

Equation (10) follows from these estimates and the bounded contour integral when \(a=0\).

## 3.4 Efficient evaluation

The stationary point requires no search over \(L\) modes. With \(t=\theta^2\),
\[
Y=\cos q_\theta
 =\frac{2+\frac52t}{3t+\sqrt{4+t+4t^2}}, \tag{20}
\]
and
\[
q_\theta=
\arctan\!\left(
 \frac{\theta\sqrt{1-(3/2-Y)^2}}{Y}
\right).
\]
These formulas are well-conditioned even at \(\theta=0,1\).

To achieve (11):

* **Large \(a\):** when \(a\ge C_1/\delta\), use (17), or zero in the fixed-large-\(\eta\) regime. Equation (18) supplies the required error.
* **Small \(a\):** evaluate the deformed exact integral (12). Its integrand has derivative bounded by \(C(1+a)\), uniformly in \(\eta\). A composite quadrature with
  \[
  N=O((1+a)^2/\delta)=O(\delta^{-3})
  \]
  nodes suffices.

The large phase \(a p_\eta+bq_\theta\) requires angle precision
\[
O(\delta/a),
\]
so the arithmetic uses
\[
O\bigl(n+\log(2+a)+\log(1/\delta)\bigr)
\]
bits, including the extra \(n\)-scale phase bits. Elementary square roots, logarithms, trigonometric functions and exponentials on the displayed domains can be evaluated by finite Taylor/Newton schemes with polynomial bit work. Exponentials below the requested absolute tolerance can be clipped.

This proves the kernel lemma. In particular, no quadrature or series of length \(\operatorname{poly}(L)\) is hidden in it.

---

# 4. A uniformly accurate torus field with only polynomial work

Let
\[
r(x)=\|x\|_\infty
\]
for the centered torus representative, and retain \(\|z\|_\infty\le M\).

For \(z\ne0\), with \(\|z\|_\infty=j\),
\[
\|x+Lz\|_\infty\ge Lj/2.
\]
Therefore
\[
\sum_{\|z\|_\infty\le M}
 \frac1{\sqrt{1+\|x+Lz\|_\infty}}
 \le
S_M(x):=
\frac1{\sqrt{1+r(x)}}+\frac{12M^{3/2}}{\sqrt L}. \tag{21}
\]

The square-shell counts give
\[
\sum_x\frac1{1+r(x)}\le4L,
\]
hence
\[
\|S_M\|_2\le18M^{3/2}\sqrt L. \tag{22}
\]

Choose
\[
\delta=\frac{\epsilon}{2^{14}(M+1)^2}
\]
and compute, only at requested candidate sites,
\[
v(x)=\sum_{\|z\|_\infty\le M}
 \widetilde g_{1/L}(x+Lz). \tag{23}
\]
Combining (9), (11), and (21),
\[
\boxed{
|v(x)-G_L(x)|
 \le \delta S_M(x)+\frac{\epsilon}{2^{14}L}
} \tag{24}
\]
for every torus point and every allowed \(L\).

Thus
\[
\|v-G_L\|_2
 \le \frac{19\epsilon}{2^{14}}\sqrt L. \tag{25}
\]

For nonzero vectors \(u,v\),
\[
\operatorname{TV}\!\left(
 \frac{|u|^2}{\|u\|^2},
 \frac{|v|^2}{\|v\|^2}
\right)
\le
\left\|\frac u{\|u\|}-\frac v{\|v\|}\right\|_2
\le \frac{2\|u-v\|_2}{\|u\|_2}. \tag{26}
\]
Using (1), equations (25)–(26) yield
\[
\operatorname{TV}(P_L,P_v)\le\epsilon/8. \tag{27}
\]

This is an additive global guarantee. It does not require relative accuracy at interference zeros or exponentially small individual probabilities.

---

# 5. Explicit spatial proposal and rejection sampler

Put \(R=L/2\). For the centered torus, the number of sites with \(r(x)=r\) is
\[
N_0=1,\qquad
N_r=8r\quad(1\le r<R),\qquad
N_R=2L-1.
\]

Define the proposal
\[
\boxed{
Q(x)=\frac12\,\frac1{(R+1)N_{r(x)}}
       +\frac12\,\frac1{L^2}.
} \tag{28}
\]

It is sampled by:

* with probability \(1/2\), choose a radius uniformly from \(0,\ldots,R\), then a site uniformly on its square shell;
* otherwise choose a uniformly random torus site.

Shell enumeration and evaluation of \(Q(x)\) use \(O(n)\)-bit integer arithmetic. No annulus oracle is supplied or needed.

The proposal obeys
\[
Q(x)\ge\frac1{16L(1+r(x))},
\qquad
Q(x)\ge\frac1{2L^2}. \tag{29}
\]

From the kernel bound and its evaluation error,
\[
|v(x)|\le(C_g+1)S_M(x).
\]
Consequently, for an effective fixed constant \(C_E\),
\[
|v(x)|^2
 \le C_E\left(\frac1{1+r(x)}+\frac{M^3}{L}\right)
 \le C_H LM^3Q(x), \tag{30}
\]
where, for example, any integer \(C_H\ge18C_E\) works.

Set
\[
H=C_H LM^3.
\]
Accept a proposal \(x\) with probability
\[
\boxed{
A(x)=\frac{|v(x)|^2}{H Q(x)}.
} \tag{31}
\]
The numerator and \(Q(x)\) are rational, so this acceptance probability is efficiently evaluable. Its accepted law is exactly \(P_v\) in the ideal arithmetic sampler.

Equation (25) ensures \(\|v\|_2\ge\|G_L\|_2/2\), so
\[
\Pr(\text{accept})
 =\frac{\|v\|_2^2}{H}
 \ge\frac1{2048C_HM^3}. \tag{32}
\]

Thus rejection loses only a polynomial factor in \(n+\log(1/\epsilon)\).

---

# 6. Finite clock, finite randomness, and total cost

Expected-time rejection is not the final algorithm.

With \(s=\lceil\log_2(1/\epsilon)\rceil\), cap the number of trials at
\[
T=2048C_HM^3(s+4). \tag{33}
\]
By (32), the probability of reaching the cap is at most \(\epsilon/16\). On a cap or any explicitly designated failure, output a fixed site.

Uniform integers used by the proposal can be generated by binary rejection, whose individual success probability is at least \(1/2\). Cap each such subroutine after
\[
J=O(\log(T/\epsilon))
\]
attempts. A union bound makes their total failure probability at most, say, \(\epsilon/16\).

For (31), use a \(b\)-bit Bernoulli probability with
\[
2^{-b}\le\epsilon/(64T).
\]
Since \(v(x)\) and \(Q(x)\) are rational, the threshold can be computed by integer division. Coupling over all trials bounds the resulting distributional error by \(T2^{-b}\).

Together with (27), these errors sum to less than \(\epsilon\).

### Work accounting

Each trial evaluates \(O(M^2)\) images. A deliberately loose bound for one kernel evaluation is
\[
O\!\left(\delta^{-3}\operatorname{poly}(n+s)\right).
\]
Since
\[
M=O(n+s),\qquad
\delta^{-1}=O((M+1)^2/\epsilon),\qquad
T=O(M^3(s+1)),
\]
the overall work is bounded by
\[
O\!\left(
 M^{11}\epsilon^{-3}(s+1)\operatorname{poly}(n+s)
\right), \tag{34}
\]
plus input reading and the \(2n\)-bit output.

All loops have prescribed finite caps. The algorithm can stream both quadrature nodes and image sums, so it also uses polynomial space.

---

# 7. Status, proof obligations, and falsifiers

**Proved deduction presented here:** the native \(m=1\) spatial Born sampler admits the requested classical polynomial bit-complexity construction.

The nontrivial verification points are explicit:

1. **Residue branch and contour:** equations (12)–(15), including nonvanishing of \(\sin p_\eta\).
2. **Uniform oscillatory error:** the \(C^4\) bound (19) and its implication (18).
3. **Periodization:** the resolvent-strip estimate (5) and the uniform image tail (7).
4. **Discrete normalization:** the exact strip count (3), not a continuum shell count.
5. **Finite-clock sampling:** the envelope (30), acceptance lower bound (32), and error budgets for all caps.

These are proof-checking obligations, not extra input promises. Their constants are effective and independent of \(L,\epsilon\).

A mathematical falsifier of the main analytic step would be a sequence with \(0<\eta\le\eta_*\), \(0\le b\le a\), for which
\[
a^{3/2}\left|g_\eta(a,b)-g_{\eta,\mathrm{lead}}(a,b)\right|
\]
is unbounded. The argument above rules this out through (19); finite numerical agreement would not establish that fact. An exact violation of any displayed tail, counting, or envelope inequality would likewise invalidate the corresponding sampler proof.

No finite numerical controls were used, and no unprovided source was imported as a theorem. In particular, the supplied primary’s continuum circular-ring formulas are not used.

**Scope:** this completes only the requested single-source primitive. It does not establish efficient interference normalization, or a universal classical algorithm, for arbitrary \(m\)-source inputs.