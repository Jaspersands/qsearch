## Hardest falsifier first: an exactly compact solution

Take, for every \(L=2^n\),
\[
f=(B_{\rm op}+i/L)\delta _0.
\]
This is a five-site source in a radius-one square, with rational complex weights, and
\[
u=\delta _0
\]
**exactly**. Nevertheless, its source transform restricted to the real characteristic curve is
\[
F|_{\{b=0\}}=i/L.
\]

Thus:

* the exact exterior field vanishes;
* a leading radiative approximation is not identically zero;
* charging inverse radiative power would be fatal;
* sampling periodic images as independent output components would be incorrect.

More generally, \(f=(B_{\rm op}+i/L)h\) gives \(u=h\) for every compact rational \(h\).

This symbolic counterfamily does **not** falsify the endpoint below. The construction charges approximation error to \(\|f\|\), uses a proposal floor costing only \(O(\operatorname{poly}(n)\|f\|^2)\), and performs rejection against the **coherent** periodized field.

## Verdict

**The compact-source endpoint is provable.** A tangential Markov inequality for Laurent functions is unnecessary.

The replacement for that missing inequality is:

1. construct a rational, piecewise-constant upper envelope for the angular intensity by certified algebraic level-set isolation;
2. sample its lattice realization using explicit rational-wedge counts;
3. allow a polynomial additive proposal cost for lattice-boundary discrepancies.

That additive cost is affordable because
\[
\|u\|\ge \|f\|/8.
\]

Below is a construction and proof, including the two analytic estimates needed for its correctness.

---

# 1. Statement and conventions

There are absolute, effectively computable constants \(C,c\) and a randomized classical algorithm with worst-case bit clock
\[
C(1+n+D+m+B+E)^c
\]
which, given the promised compact source and an integer accuracy parameter \(E\ge2\), outputs one point of \(\mathbb Z_L^2\) with total-variation error at most \(1/E\).

Taking \(E=\lceil1/\epsilon\rceil\) gives the requested
\[
\operatorname{poly}(n,D,m,B,1/\epsilon)
\]
bound. This accuracy convention makes its input-access cost explicit; if an arbitrary rational \(\epsilon\) is supplied instead, its actual encoding length must also be read and charged.

The supplied translation is removed first. If \(L>4(D+1)\), every source site has a unique relevant integer lift
\[
s_j\in[-D,D]^2.
\]
Otherwise, \(L^2=O((D+1)^2)\), and a full-grid computation is already allowed by the claimed bound. Rounding \(D\) upward only changes constants.

Normalize the rational weights by
\[
Q=\sum_j\bigl(|\Re w_j|+|\Im w_j|\bigr).
\]
This is an exact rational computation and does not change the Born law. Henceforth \(Q=1\), and put
\[
S=\sum_j|w_j|^2.
\]
Distinct source sites imply
\[
\frac1{2m}\le S\le1,\qquad
\sum_j|w_j|\le\sqrt{mS}.
\]

Write \(\eta=1/L\). Since the spectrum of \(B_{\rm op}\) lies in \([-7,1]\),
\[
\|B_{\rm op}+i\eta\|<8,
\qquad
\boxed{\ \|u\|^2\ge S/64.\ }                                      \tag{1}
\]
This is a deduction, not a norm promise.

---

# 2. A uniform, actual-lattice far-field estimate

The following estimate is the analytic foundation of the construction.

## Lemma 1: uniform kernel expansion

For \(a\ge d\ge0\), \(a\ge1\), and \(0<\eta\le1/4\), put \(t=d/a\). Let \(p(t),q(t)\) be the unique solution
\[
\cos p+\cos q=\frac32,\qquad
\sin q=t\sin p,
\]
with
\[
0\le q\le p\le\pi/3.
\]
Define
\[
\beta(t)=\frac{\cos q+\cos p\,t^2}{\sin p},
\qquad
c(t)=\frac{-i\,e^{-i\pi/4}}
 {\sqrt{8\pi}\,\sin p\,\sqrt{\beta(t)}} .
\]
Then
\[
g_\eta(a,d)=
\frac{c(t)}{\sqrt a}
 \exp\!\left(i(ap+dq)-\frac{\eta a}{2\sin p}\right)
 +E_\eta(a,d),
\]
where
\[
\boxed{\ |E_\eta(a,d)|\le C a^{-3/2}\ }                            \tag{2}
\]
with one absolute constant, independent of \(a,d,\eta\). Also \(|c(t)|\le1\).

### Proof of the uniformity needed here

Start from the supplied exact residue identity
\[
g_\eta(a,d)=
-\frac{i}{4\pi}\int_{-\pi}^{\pi}
 \frac{e^{ia p_\eta(q)+idq}}{\sin p_\eta(q)}\,dq,
\quad
p_\eta(q)=\arccos\!\left(\frac32-\cos q-i\eta/2\right),
\]
on the branch \(\Im p_\eta>0\).

At \(\eta=0\), the propagating interval is \(|q|<q_0=\pi/3\). Its real phase
\[
\phi_t(q)=p_0(q)+tq
\]
has exactly one stationary point \(q(t)\). All these stationary points lie in
\[
[0,\arccos(3/4)],
\]
a fixed positive distance from the branch points \(\pm q_0\), and
\[
-\phi_t''(q(t))=\beta(t)
\]
is bounded above and below by positive absolute constants.

Choose a fixed-width smooth cutoff around \(q(t)\), with derivatives bounded uniformly in \(t\). In this neighborhood,
\[
p_\eta-p_0=\frac{i\eta}{2\sin p_0}+O(\eta^2),
\]
with the same statement for any fixed finite number of derivatives. Moreover,
\(\Im p_\eta\ge c\eta\). Consequently the amplitude
\[
A_{a,\eta}(q)=
\frac{\exp(ia(p_\eta(q)-p_0(q)))}{\sin p_\eta(q)}
\]
has uniformly bounded derivatives through any fixed order: differentiation produces factors polynomial in \(a\eta\), multiplied by \(e^{-ca\eta}\).

The one-dimensional stationary-phase remainder is therefore \(O(a^{-3/2})\), uniformly in \(\eta\). This version follows directly by the local Morse change of variable
\[
\phi_t(q)=\phi_t(q(t))-z^2/2,
\]
Taylor expansion of the transformed amplitude, and integration by parts outside the stationary neighborhood. All coordinate and derivative bounds are uniform on this fixed compact family.

Replacing the stationary amplitude by
\[
\frac{e^{-\eta a/(2\sin p(t))}}{\sin p(t)}
\]
introduces an error bounded by
\[
C a^{-1/2}(\eta+a\eta^2)e^{-ca\eta}
\le C a^{-3/2}.
\]

It remains important not to invent an endpoint error at \(q=\pm q_0\). Here is the cancellation explicitly. Write
\[
v=\sin p_\eta(q),\qquad
z=\cos p_\eta(q),\qquad
h=tv-\sin q.
\]
Outside the stationary neighborhood, but before a fixed evanescent cutoff, \(|h|\ge c>0\). If an integration-by-parts amplitude has the form \(R(q,v)/v\), division by the phase derivative gives \(R/h\). Since
\[
v'=-\frac{z\sin q}{v},
\]
differentiation returns an amplitude of the same form:
\[
\frac1v\left[
v\,\partial_q(R/h)-z\sin q\,\partial_v(R/h)
\right].
\]
Its numerator is uniformly bounded. Also
\[
\int\frac{dq}{|v|}\le C
\]
uniformly in \(\eta\), because the two limiting singularities are integrable square-root singularities. Two integrations by parts therefore bound this entire nonstationary contribution by \(Ca^{-2}\), with no branch-endpoint term.

Beyond the fixed evanescent cutoff, \(\Im p_\eta\ge c>0\), giving \(O(e^{-ca})\). For \(\eta\) above a fixed small constant, the whole integral is exponentially small in \(a\), so it is covered by the same bound. This proves (2).

The constants are effective: only fixed-order derivatives on explicit compact charts and fixed cutoff derivatives enter. No uniform estimate is being inferred from the Martin excerpt’s asymptotic formula.

---

## Lemma 2: the compact-source expansion

Define the infinite-lattice source field
\[
H(y)=\sum_j w_j g_\eta(y-s_j).
\]
For \(y\ne0\), let \(k(y)\) be the point on \(b=0\) whose outward propagation direction is \(y\), and set
\[
F(k)=\sum_j w_j e^{-ik\cdot s_j}.
\]

Let \(A_{\rm rad}(y)\) be the leading expression in Lemma 1, with the appropriate coordinate signs and interchange, multiplied by \(F(k(y))\). For
\[
a=\|y\|_\infty\ge C(D+1),
\]
\[
\boxed{
|H(y)-A_{\rm rad}(y)|
 \le C\sqrt{mS}\,(D+1)^2a^{-3/2}.
}                                                                  \tag{3}
\]
In particular,
\[
\boxed{
\sum_{\|y\|_\infty>R}|H(y)-A_{\rm rad}(y)|^2
 \le \frac{C m(D+1)^4 S}{R}.
}                                                                  \tag{4}
\]

### Proof

The characteristic oval lies in \([-\pi/3,\pi/3]^2\); its curvature and group speed are bounded above and below by positive constants.

The leading kernel can be written invariantly as
\[
K_\eta(y)=
\frac{e^{-3\pi i/4}}
 {\sqrt{2\pi}\,|\nabla b(k(y))|\sqrt{\kappa(k(y))\,|y|}}
 \exp\!\left(
 i\,k(y)\cdot y-\frac{\eta |y|}{|\nabla b(k(y))|}
 \right).
\]
Its real phase \(S_0(y)=k(y)\cdot y\) satisfies
\[
\nabla S_0(y)=k(y),\qquad
\|\nabla^2 S_0(y)\|\le C/|y|.
\]
The gradient of its nonoscillatory amplitude is bounded by
\[
C\bigl(|y|^{-3/2}+\eta|y|^{-1/2}\bigr)e^{-c\eta|y|}
 \le C|y|^{-3/2}.
\]
Taylor expansion for \(|s|\le\sqrt2D\) therefore gives
\[
K_\eta(y-s)=K_\eta(y)e^{-ik(y)\cdot s}
 +O\!\left((D+1)^2a^{-3/2}\right).
\]
Combine this with (2), sum using \(\sum|w_j|\le\sqrt{mS}\), and use that the max-norm shell of radius \(a\) has \(8a\) lattice points. This proves (3)–(4).

This is an absolute, cancellation-safe estimate. It does not divide by \(F(k)\).

---

# 3. Computing the near field without inverse-\(\eta\) work

Only polynomial-radius kernel values will be evaluated by quadrature.

For \(|q-q_0|\) near either branch point, put
\[
h=|q-q_0|+\eta.
\]
The residue integrand and its derivative obey
\[
\left|\frac{e^{iap_\eta(q)+idq}}{\sin p_\eta(q)}\right|
 \le C h^{-1/2},
\]
\[
\left|\frac{d}{dq}
 \frac{e^{iap_\eta(q)+idq}}{\sin p_\eta(q)}\right|
 \le C\left(a h^{-1}+d h^{-1/2}+h^{-3/2}\right).                   \tag{5}
\]
Away from the two branch neighborhoods, ordinary bounded-denominator estimates apply.

Partition those neighborhoods into dyadic intervals down to scale \(\eta=2^{-n}\), with one central interval at that scale. On a length-\(h\) interval, a uniform \(N_q\)-panel rule has error at most
\[
\frac{C}{N_q}\left(ah+dh^{3/2}+h^{1/2}\right).
\]
Summing over the dyadic scales is bounded geometrically. Thus absolute error \(\delta\) is obtained with
\[
O\!\left(n\,\frac{a+d+1}{\delta}\right)
\]
elementary-function evaluations, up to an inessential polynomial overhead.

Although values near a branch point can be \(O(L^{1/2})\), representing and evaluating them requires only
\[
\operatorname{poly}\bigl(n,\log(a+2),\log(1/\delta)\bigr)
\]
bits. Complex square roots, logarithms/arccosines, and exponentials are evaluated with guard bits for the distance \(O(\eta)\) from the branch point.

Hence:

\[
\boxed{
\text{For }a,d,\delta^{-1}\text{ polynomial, near-field evaluation has a polynomial bit clock.}
}                                                                  \tag{6}
\]

No logarithmic-in-accuracy Green evaluator is assumed. Later high-precision rejection evaluations use the **stored rational near-field table**, not new Green evaluations.

---

# 4. A finite coherent approximation to the torus field

Choose
\[
M=C_0\!\left(1+n+\left\lceil\log_2\frac{m+1}{\epsilon}\right\rceil\right),
\qquad
N=(2M+3)^2,
\]
and
\[
R\ge
C_1 N m(D+1)^4\epsilon^{-2}+C_1(D+1).                              \tag{7}
\]
The fixed constants are chosen from the estimates above with sufficient error-budget slack.

If \(L\le 8(R+D+1)\), use a full-grid computation. Its cost is polynomial in the displayed parameters. For example, rational Gaussian elimination gives the exact rational complex solution; determinant/minor bit bounds give polynomial bit growth. Sampling its rational squared magnitudes to the requested accuracy is then elementary.

Otherwise \(R<L/8\).

Set \(T=ML\) and \(\Omega=[-T,T]^2\cap\mathbb Z^2\). Define
\[
v(y)=
\begin{cases}
\text{a stored rational approximation to }H(y),&\|y\|_\infty\le R,\\
A_{\rm rad}(y),&R<\|y\|_\infty\le T.
\end{cases}
\]
Compute the near table to per-entry error at most
\[
\frac{c\epsilon\sqrt S}{(R+1)\sqrt N}.
\]
By normalization, its inverse requested accuracy is polynomial.

Now define, coherently,
\[
V(x)=\sum_{\substack{y\in\Omega\\y\equiv x\pmod L}}v(y).           \tag{8}
\]

There are at most \(N\) summands for any \(x\).

### Periodization tail

The elementary contour shift
\[
p_j\longmapsto p_j+i\,\operatorname{sgn}(y_j)\eta/16
\]
keeps the denominator’s imaginary part at least \(\eta/2\). It gives
\[
|g_\eta(y)|\le \frac2\eta e^{-\eta\|y\|_1/16}.
\]
Absolute convergence then proves the periodization identity. Summing the omitted images gives
\[
\left\|
u-\sum_{\substack{y\in\Omega\\y\equiv x\pmod L}}H(y)
\right\|_{\ell^2(\mathbb Z_L^2)}
\le C\sqrt{mS}\,L^2(M+1)e^{-M/C}.
\]
The chosen \(M\) makes this at most \(c\epsilon\sqrt S\).

For the retained-image approximation error, Cauchy–Schwarz gives
\[
\left\|
\sum_{y\equiv x}(H(y)-v(y))
\right\|_2^2
\le N\sum_{y\in\Omega}|H(y)-v(y)|^2.
\]
Using (4), (7), and the near-table accuracy,
\[
\boxed{\ \|u-V\|_2\le c\epsilon\sqrt S.\ }                         \tag{9}
\]
By (1), the normalized spatial Born laws of \(u\) and \(V\) differ by \(O(c\epsilon)\) in TV.

This retains the off-resonant field through the near computation and the absolute remainder estimate. It does not replace the full solution by a resonant-band state.

---

# 5. A normalization bound that survives cancellation and image interference

Let
\[
I_\eta=
\frac1{(2\pi)^2}\int_{[-\pi,\pi]^2}
 \frac{|F(p,q)|^2}{b(p,q)^2+\eta^2}\,dp\,dq
=\|H\|_{\ell^2(\mathbb Z^2)}^2.
\]
Let the eight slope charts of the characteristic oval be \(k_o(t)\), \(0\le t\le1\), and define
\[
J=\sum_{o=1}^8\int_0^1|F(k_o(t))|^2\,dt.
\]

Two elementary comparisons suffice:
\[
\boxed{
I_\eta\le C(1+mD^2)\|u\|^2,
\qquad
LJ\le C(1+mD^2)\|u\|^2.
}                                                                  \tag{10}
\]

### Discrete-to-continuous comparison

On a frequency cell of width \(2\pi/L\) around a native Fourier grid point \(p_k\),
\[
b(p)^2+\eta^2\asymp b(p_k)^2+\eta^2,
\]
because \(|b(p)-b(p_k)|\le C/L=C\eta\).

Also
\[
|F(p)-F(p_k)|
 \le C D\sqrt{mS}/L.
\]
Therefore, using Parseval for the native torus and the crude bound
\((b^2+\eta^2)^{-1}\le L^2\),
\[
I_\eta\le C\|u\|^2+C mD^2S.
\]
Equation (1) proves the first comparison.

### Restriction-to-the-curve comparison

Use a fixed tubular coordinate system \((t,s)\), where \(b=s\), around the oval. For \(|s|\le\eta\le1/4\), all Jacobians and coordinate derivatives are bounded above and below by constants. Moreover,
\[
|F(k_s(t))-F(k_0(t))|
 \le C D\sqrt{mS}\,|s|.
\]
Integrating the squared inequality against \((s^2+\eta^2)^{-1}\) gives
\[
LJ\le C I_\eta+C mD^2S/L.
\]
This proves (10).

These bounds compare **unperiodized intensity** to the actual coherent torus norm. They are why coherent image cancellation cannot create an exponentially bad rejection ratio here.

---

# 6. A paid algebraic angular envelope—without a Markov theorem

The angular intensity is algebraic in the slope \(t\). Explicitly, set
\[
u(t)=\cos p(t)
 =\frac{5/2+2t^2}{3+\sqrt{4+t^2+4t^4}},
\qquad
v(t)=\frac32-u(t),
\qquad
w(t)=\sqrt{1-u(t)^2}.
\]
Then
\[
e^{\pm ip}=u\pm iw,\qquad
e^{\pm iq}=v\pm itw.
\]
Signs and coordinate interchange give all eight charts.

Since \(|s_{j,\ell}|\le D\), negative Laurent powers can be replaced by conjugate unit-circle powers. Thus \(F(k_o(t))\), and then
\[
r_o(t)=|F(k_o(t))|^2,
\]
have polynomial representations of degree \(O(D+1)\) in \(t,u,w\), subject to
\[
(1-t^2)u^2-3u+\frac54+t^2=0,
\qquad
w^2=1-u^2,
\]
on the specified real branch.

Dense expansion has polynomially many coefficients, with polynomial bit length in \(D,m,B\). This conversion is used **only for certified level-set decisions**, not for a relative norm inequality.

## Envelope construction

Put
\[
\tau=S/L,\qquad U=mS.
\]
Use the levels
\[
a_k=2^k\tau,\qquad
0\le k\le \lceil\log_2(mL)\rceil.
\]
For a scalar \(0\le r\le U\), the exact staircase
\[
\tau+\sum_k a_k\,\mathbf 1_{\{r\ge a_k\}}
\]
lies between \(r\) and \(2r+\tau\).

For each chart and level, construct a rational-interval superset
\[
E_{o,k}^+\supseteq\{t\in[0,1]:r_o(t)\ge a_k\}.
\]

Here is the charged algebraic operation:

* eliminate the fixed-degree auxiliary variables from \(r_o(t)-a_k\);
* isolate the real roots of the resulting nonzero univariate polynomial;
* decide the correct branch’s sign on each complementary interval;
* enlarge root enclosures slightly and include them;
* handle identically constant restrictions exactly.

Artificial factors or denominators arising at \(t=1\) are removed algebraically; that endpoint is handled separately. No denominator is used to compare norms.

If \(K_0\) bounds the total number of relevant polynomial roots over all charts and levels, refine enclosures to width
\[
\delta_t\le \frac{1}{C m L(K_0+1)}.
\]
This requires only \(O(n+\log m+\log(K_0+1))\) requested refinement bits, in addition to polynomial coefficient-height and root-separation bits.

Define
\[
H_o(t)=\tau+\sum_k a_k\,\mathbf 1_{E_{o,k}^+}(t).
\]
Then
\[
\boxed{
H_o(t)\ge r_o(t),\quad
H_o(t)\le4mS,\quad
\sum_o\int_0^1H_o(t)\,dt\le2J+C\tau.
}                                                                  \tag{11}
\]

The number \(K\) of positive interval components in these staircases is polynomial in \(D,m,n\); their bit lengths are polynomial in \(D,m,B,n\).

### Why root isolation is a paid operation

Resultants here have polynomial degree and coefficient bit length because the auxiliary algebraic extension has fixed degree. Square-free factorization and fraction-free Sturm/subresultant sequences have polynomial bit complexity. Root separation needs only polynomially many bits in the degree and coefficient height. Bisection retains only intervals containing roots, so at each depth there are at most the polynomial degree many surviving intervals.

There is no integration oracle, transcendental root oracle, or inverse-radiative-power parameter.

---

# 7. Sampling the discrete far-field proposal

Represent the \(H_o\) as positive interval components
\[
\omega_i\,\mathbf1_{I_i}(t),
\]
including the floor \(\tau\mathbf1_{[0,1]}\) in every chart.

Partition \(R<a\le T\) into dyadic bins
\[
A_j\le a<2A_j,
\]
truncated at \(R+1\) and \(T\). For every angular component and radial bin, use the constant proposal weight
\[
\frac{\omega_i}{A_j}
\]
on lattice points in the corresponding octant satisfying
\[
a\in\text{bin }j,\qquad d/a\in I_i,\qquad 0\le d\le a.
\]
Overlaps on axes and diagonals are allowed and counted as proposal multiplicity.

Call the resulting far proposal weight \(h_{\rm far}(y)\). Since damping is at most one and \(|c(t)|\le1\),
\[
h_{\rm far}(y)\ge |A_{\rm rad}(y)|^2.
\]
The proposal may omit damping because its radius is truncated to \(ML\); this costs only a factor \(M\). **The evaluated field retains damping.**

For the near patch, use
\[
h_{\rm near}(y)=|v(y)|^2.
\]
Thus, throughout \(\Omega\),
\[
h(y)\ge |v(y)|^2.
\]

## Explicit lattice counting

For a rational interval \(I=[\ell,r]\), the number of admissible \(d\)'s at a fixed integer \(a\) is obtained from
\[
\lfloor ra\rfloor-\lceil\ell a\rceil+1,
\]
with the relevant endpoint convention.

Cumulative counts are sums of rational floor functions. They are computed by the Euclidean floor-sum recursion: remove integer quotients from numerator coefficients, then interchange the two axes of the remaining lattice triangle. Each interchange is an Euclidean step. All integers have polynomial bit length.

A uniform point in such a component is sampled by:

1. drawing a uniform rank below its exact count;
2. binary-searching the major coordinate using cumulative floor sums;
3. selecting the corresponding minor coordinate.

This takes polynomially many bit operations in the endpoint bit lengths and \(\log T\). It is not a shell-count oracle.

## Proposal mass bound

For a slope interval of length \(\ell\), a bin with \(a<2A_j\) contains at most
\[
2A_j^2\ell+2A_j
\]
lattice points. Consequently
\[
W_{\rm far}:=\sum_y h_{\rm far}(y)
 \le C\left[
 T\sum_o\int H_o
 +(1+\log T)\sum_i\omega_i
 \right].
\]
Using (11), \(\sum_i\omega_i\le C K mS\), and \(T=ML\),
\[
W_{\rm far}\le
C\left[MLJ+MS+(1+\log T)KmS\right].                               \tag{12}
\]

The term involving \(K\log T\) pays for arbitrarily narrow angular intervals and lattice-boundary discrepancies. No relative angular derivative inequality is needed.

For the near patch,
\[
W_{\rm near}\le2I_\eta+\text{the paid table-error term}.
\]
Combining this with (10)–(12),
\[
\boxed{
W:=\sum_{y\in\Omega}h(y)\le P\,\|u\|^2,
}                                                                  \tag{13}
\]
where, for an absolute effective constant,
\[
P=C\left[
(M+1)(1+mD^2)+mK(1+n+\log(M+1))+1
\right].
\]
In particular, \(P\) is polynomial.

All proposal weights and counts are rational. Therefore \(W\) is computed exactly with polynomial bit length.

---

# 8. Coherent rejection, not an image mixture output

Sample \(y\) with probability \(h(y)/W\), and fold it to \(x=y\bmod L\). Define the exactly computable rational quantity
\[
H_x=\sum_{\substack{y\in\Omega\\y\equiv x\pmod L}}h(y).
\]
The folded proposal is \(q(x)=H_x/W\).

Compute the coherent amplitude \(V(x)\) from (8), and accept with probability
\[
\alpha(x)=\frac{|V(x)|^2}{N H_x}.                                 \tag{14}
\]
Cauchy–Schwarz and \(h(y)\ge|v(y)|^2\) prove
\[
0\le\alpha(x)\le1.
\]

Conditioned on acceptance, the law is exactly the Born law of \(V\). The ideal acceptance probability is
\[
p_{\rm acc}=\frac{\|V\|^2}{NW}.
\]
Equations (9) and (13) give
\[
\boxed{\ p_{\rm acc}\ge \frac1{CNP}.\ }                            \tag{15}
\]
There is no inverse radiative power in this bound.

Near/far interference and all retained periodic-image interference are included in the numerator of (14). Images are only components of a positive **proposal**.

---

# 9. Precision, random bits, and a genuine finite clock

## Acceptance precision

The angular floor ensures that the rejection denominator is never dangerously small for bit complexity.

For every torus point, choose a congruent image with major coordinate between \(L/2\) and \(3L/2\). It is in \(\Omega\), outside the near patch, and its floor contribution gives
\[
\boxed{\ H_x\ge cS/L^2.\ }                                       \tag{16}
\]

Therefore evaluating \(\alpha(x)\) to additive error \(\gamma\) requires only polynomially many bits in
\[
n+B+\log(D+2)+\log(N+2)+\log(1/\gamma).
\]
The far amplitudes use algebraic operations, square roots, inverse trigonometric functions, and exponentials. Their phases have magnitude \(O(ML)\), so argument reduction and phase accuracy require \(O(n+\log M)\) additional bits, not \(O(L)\) work.

The near values are stored rationals. They are **not recomputed by quadrature to \(L^{-1}\) accuracy** during rejection.

## Finite rejection cap

Use
\[
T_{\rm acc}=
\left\lceil CNP\log(C/\epsilon)\right\rceil
\]
trials, then return a fixed point if all trials fail. By (15), the ideal failure probability is at most the allocated \(O(\epsilon)\) budget.

In each trial:

* sample the rational component distribution to TV error \(O(\epsilon/T_{\rm acc})\);
* sample its uniform lattice rank to the same accuracy;
* compute and implement (14) to additive error \(O(\epsilon/T_{\rm acc})\).

All three operations have a fixed random-bit budget. For example, drawing a uniform integer below \(C_{\rm count}\) by mapping a \(b\)-bit uniform integer through a scaled floor incurs TV error at most \(C_{\rm count}/2^b\); here
\[
\log C_{\rm count}=O(n+\log M).
\]
No unbounded random-bit rejection loop is required.

A trial-by-trial coupling bounds the accumulated implementation error by \(O(\epsilon)\). Together with (9), the chosen constant allocations give total error at most \(\epsilon\).

## Resource accounting

| Operation | Charged resource |
|---|---|
| Read sites, translation, weights | \(O(nm+B)\) bits, plus parameter encodings |
| Rational normalization and \(S\) | Polynomial rational arithmetic |
| Near patch | \(O(R^2m)\) kernel terms |
| Each near kernel evaluation | Dyadic quadrature with polynomial inverse absolute accuracy, as in (5)–(6) |
| Angular algebra | Polynomial degree and coefficient bit length in \(D,m,B,n\) |
| Angular level sets | Resultants, subresultants/Sturm counts, certified rational root enclosures |
| Proposal normalization | Exact rational weights times exact lattice counts |
| Each proposal point | Euclidean floor sums and binary search on \(O(n+\log M)\)-bit coordinates |
| Coherent field evaluation | At most \(N\) image amplitudes, each explicitly evaluated |
| Acceptance | At least \(1/(CNP)\), with a deterministic trial cap |
| Randomness | Polynomially many explicitly bounded random bits |
| Output | Two \(n\)-bit coordinates and the supplied translation added modulo \(L\) |

Since \(M,N,R,K,P,T_{\rm acc}\) are all polynomial in the requested parameters, every row has a polynomial worst-case bit bound.

---

# 10. What is proved, and what would falsify this construction

The construction covers **every** compact source in the supplied square. It does not first require exact divisibility, a nonzero radiation certificate, a lower bound on radiative power, separated sites, or a conditional norm-ratio promise.

Its central proof obligations are:

1. **Uniform lattice remainder:** (2), including cancellation of the apparent branch-endpoint contributions. The integration-by-parts argument above supplies that obligation.
2. **Cancellation-safe source remainder:** (3)–(4), obtained by translating the actual lattice phase and amplitude.
3. **Coherent norm control:** (10), obtained from native Fourier cells and a fixed tubular coordinate system.
4. **Paid angular proposal:** (11), using algebraic level sets and explicit coefficient/root bit bounds—not a Laurent Markov theorem.
5. **Discrete proposal mass and finite rejection:** (12)–(16), including lattice-boundary costs, image coherence, and the probability floor.

A counterexample to any displayed uniform inequality would invalidate this particular proof. A failure of an implementation of root isolation or stationary phase would not, by itself, establish hardness.

The initial exact-compact-solution falsifier illustrates the intended behavior: for \(f=(B_{\rm op}+i/L)\delta_0\), the angular power is \(O(L^{-2})\), but the proposal floor costs only \(O(MS)\), and the local field supplies the actual mass. No inverse radiative power is paid.

**Scope:** this proves the endpoint with numerical diameter parameter \(D\). It does not supply a polynomial-diameter clustering theorem for arbitrary sparse sources, and it makes no hardness or quantum-speedup claim outside this compact-source promise.