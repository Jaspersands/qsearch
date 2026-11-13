## Outcome

I do **not** obtain an unrestricted polynomial rank–purity bound. The direct calculation does give:

1. a dimension-independent proof that **every state of stabilizer rank at most two satisfies \(\Pi\ge 1/16\)**, with arbitrary coefficients and phases;
2. a phase-modified six-qubit example that slightly strengthens the supplied exponent obstruction;
3. one concrete, cancellation-sensitive **Pauli visibility lemma** that would imply \(C=7\), together with its sharp rank-two version and explicit obstructions to simpler arguments.

None of this improves the supplied subexponential baseline for unrestricted \(k\).

## 1. Arbitrary-coefficient rank-two calculation

Two distinct, nonorthogonal stabilizer states can be Clifford-transformed, with phases absorbed into their coefficients, to
\[
|0^m\rangle,\quad |+^m\rangle
\]
tensored with common stabilizer ancillas. Indeed, after sending the first state to \(|0^n\rangle\), the second has support on a linear subspace containing zero; a linear reversible circuit and diagonal Clifford remove its support geometry and quadratic phase.

Clifford invariance and multiplicativity of \(\Pi\) remove the common ancillas. Write
\[
|\psi\rangle=\frac{\alpha|0^m\rangle+\beta|+^m\rangle}{\sqrt N},
\]
where
\[
d=2^m,\quad q=d^{-1/2},\quad
A=|\alpha|^2,\quad B=|\beta|^2,\quad A+B=1,
\]
\[
u=2\operatorname{Re}(\bar\alpha\beta),\qquad
v=2\operatorname{Im}(\bar\alpha\beta),\qquad
u^2+v^2=4AB,\qquad N=1+qu.
\]

Direct expansion gives the following magnitudes:

| Pauli indices | Multiplicity | Expectation magnitude |
|---|---:|---:|
| \(a=b=0\) | \(1\) | \(1\) |
| \(a=0,\ b\ne0\) | \(d-1\) | \(|A+qu|/N\) |
| \(b=0,\ a\ne0\) | \(d-1\) | \(|B+qu|/N\) |
| \(a,b\ne0,\ a\cdot b=0\) | \((d-1)(d/2-1)\) | \(|qu|/N\) |
| \(a\cdot b=1\) | \((d-1)d/2\) | \(|qv|/N\) |

Consequently,
\[
\boxed{
\Pi(\psi)=\frac1d+
\frac{
(d-1)\big((A+qu)^4+(B+qu)^4\big)
+\frac{(d-1)(d-2)}2(qu)^4
+\frac{(d-1)d}2(qv)^4
}{dN^4}.}
\tag{1}
\]
This retains all interference terms; no coefficient-norm assumption is used.

### An exact phase attack strengthens the supplied obstruction

Set
\[
\zeta=\frac{-31+3i\sqrt7}{32},\qquad
|\omega\rangle=
\frac{|0^6\rangle+\zeta|+^6\rangle}{\sqrt{225/128}}.
\]
Here \(q=1/8\), \(A=B=1/2\), \(u=-31/32\), and \(v=3\sqrt7/32\). The nonidentity magnitudes in the table become
\[
\frac{97}{225},\qquad \frac{31}{225},\qquad
\frac{3\sqrt7}{225}.
\]
Thus
\[
\begin{aligned}
\Pi(\omega)
&=\frac1{64}\left[
1+126\left(\frac{97}{225}\right)^4
+1953\left(\frac{31}{225}\right)^4
+2016\left(\frac{3\sqrt7}{225}\right)^4
\right]\\
&=\boxed{\frac{8\,986\,816}{94\,921\,875}}
<\frac{65}{686}.
\end{aligned}
\tag{2}
\]
The strict comparison is the integer calculation
\[
65(94\,921\,875)-686(8\,986\,816)=4\,966\,099>0.
\]

The state has exact rank two: \(97/225\) is a nonzero Pauli expectation magnitude other than one. Tensor powers therefore give the exact obstruction
\[
\boxed{
C\ge
\log_2\!\left(\frac{94\,921\,875}{8\,986\,816}\right)
\approx 3.4009.}
\tag{3}
\]
This excludes every fixed prefactor \(c>0\) below that exponent, since
\(\chi(\omega^{\otimes r})\le2^r\) and \(\Pi\) tensor-multiplies.

It does **not** refute \(C=4\).

### Rank two cannot falsify \(C=4\)

For any stabilizer \(\phi\), its stabilizer-projector expansion and Hölder give
\[
|\langle\phi|\psi\rangle|^8\le \Pi(\psi).
\tag{4}
\]
If the two supplied stabilizers are orthogonal, one has squared overlap at least \(1/2\), proving \(\Pi\ge1/16\).

For the nonorthogonal case, (1) and
\[
x^4+y^4\ge \frac{(x+y)^4}{8}
\]
give, when \(q\le1/2\),
\[
\Pi(\psi)\ge
q^2+\frac{1-q^2}{8}
\left(\frac{1-2q}{1-q}\right)^4.
\tag{5}
\]
Here \((1+2qu)/(1+qu)\) is nonnegative and increasing in \(u\), so its minimum occurs at \(u=-1\).

The remaining cases require only:
\[
\begin{array}{c|c}
m & \text{lower bound}\\ \hline
m\le4 & \Pi\ge 2^{-m}\ge1/16\\[2mm]
m=5 &
\displaystyle \Pi\ge\frac1{32}+\frac{31}{256}\left(\frac34\right)^4
=\frac{4559}{65536}>\frac1{16}\\[3mm]
m\ge6 &
\displaystyle \Pi\ge\frac{63}{512}\left(\frac67\right)^4
=\frac{729}{10976}>\frac1{16}.
\end{array}
\]
Therefore
\[
\boxed{\chi(\psi)\le2\quad\Longrightarrow\quad \Pi(\psi)\ge2^{-4}.}
\tag{6}
\]

This is an analytic, all-dimension rank-two theorem—not evidence establishing the general-\(k\) inequality. It also does not cover arbitrary nonfactorizing coefficients in a \(2^r\)-term tensor-product span.

## 2. A single concrete general-\(k\) proof obligation

Let \(D=2^n\). For supplied stabilizer rays \(s_1,\ldots,s_k\), let \(L_i\) be their unsigned Pauli stabilizer groups and set
\[
U=\bigcup_{i=1}^k L_i.
\]
Define their **visible Pauli energy**
\[
V_U(\psi)=\frac1D\sum_{P\in U}
|\langle\psi|P|\psi\rangle|^2.
\]

Since \(|U|\le kD\), Cauchy–Schwarz gives the unconditional inequality
\[
\boxed{\Pi(\psi)\ge \frac{V_U(\psi)^2}{k}.}
\tag{7}
\]

A concrete sufficient lemma is:

> **Pauli visibility lemma, proposed exponent \(3\) — UNPROVED.**  
> For every collection of \(k\) stabilizer states and every normalized vector in their span,
> \[
> \boxed{V_U(\psi)\ge k^{-3}.}
> \tag{V3}
> \]

This would imply \(\Pi(\psi)\ge k^{-7}\). It is stronger than the requested conclusion and is not asserted to be necessary.

### Exact cancellation obligation

Put
\[
G_{ij}=\langle s_i|s_j\rangle,\qquad
(M_P)_{ij}=\langle s_i|P|s_j\rangle.
\]
Then (V3) is exactly the assertion
\[
\boxed{
\frac1D\sum_{P\in U}|c^\dagger M_Pc|^2
\ \ge\
k^{-3}(c^\dagger Gc)^2
\quad\text{for every }c\in\mathbb C^k.}
\tag{8}
\]
There is **no restriction** on \(c\), on \(\|c\|\), or on the conditioning of \(G\). The normalization on the right is essential.

Equation (8) isolates a degree-four positivity problem in the stabilizer dyads. It is not a termwise estimate on individual dyads.

**Falsifier:** any stabilizer list and coefficient vector with \(V_U<k^{-3}\) refutes (V3). Tensoring that same list makes \(U\) and \(V_U\) multiplicative, so such an example also refutes every version \(V_U\ge a k^{-3}\) with fixed \(a>0\). It would refute this route, **not** the original polynomial purity conjecture.

## 3. Strongest visibility controls proved here

### Sharp rank-two visibility bound

For the nonorthogonal normal form above, put \(x=A-B\). Directly from the first three rows of the table,
\[
V_U=
q^2+
\frac{1-q^2}{2(1+qu)^2}
\big((1+2qu)^2+x^2\big).
\tag{9}
\]

For \(q\le1/2\), its minimum is attained at \(x=0,u=-1\):
\[
V_{\min}(q)
=
q^2+\frac{1-q^2}{2}
\left(\frac{1-2q}{1-q}\right)^2
=
\frac{1-3q+2q^2+2q^3}{2(1-q)}.
\tag{10}
\]
For \(q\le1/4\),
\[
V_{\min}'(q)=
\frac{-1+2q+2q^2-2q^3}{(1-q)^2}<0.
\]
The discrete possibilities therefore give
\[
\begin{array}{c|c}
m & \min V_U\\ \hline
1 & 1/2\\
2 & 1/4\\
3 & (29-12\sqrt2)/56\\
m\ge4 & \ge13/48.
\end{array}
\]
For orthogonal stabilizers, the cross dyad has zero expectation on \(U\), and Pauli orthogonality gives
\[
V_U=A^2+B^2\ge1/2.
\]
Hence the exact all-dimension, two-summand minimum is
\[
\boxed{
V_U\ge \nu_2:=\frac{29-12\sqrt2}{56}\approx0.21481.}
\tag{11}
\]
Equality is attained by the balanced three-qubit minus pair.

For the supplied six-qubit pair, arbitrary coefficients and phases give
\[
V_U\ge \frac{169}{448},
\]
with equality at the original balanced minus state. Thus (V3) survives the complete two-summand audit, but this does not establish it for larger \(k\).

### A tensor obstruction to stronger visibility claims

Tensoring the three-qubit minimizer gives \(k=2^r\) supplied terms and
\[
V_U=\nu_2^r.
\]
Therefore any uniform visibility exponent must satisfy
\[
\boxed{
A\ge\log_2\!\left(\frac{56}{29-12\sqrt2}\right)
\approx2.219.}
\tag{12}
\]
In particular, \(V_U\ge a k^{-2}\) is false for every fixed \(a>0\).

This also blocks obtaining \(C=4\) merely by combining (7) with a uniform visibility bound: that argument would require \(A\le3/2\), already ruled out. Exponent \(3\) in (V3) is a concrete remaining proof target, not an extrapolation from passing controls.

### Orthogonal-list control, not an allowed native promise

Let \(E_i\) be the collision probability obtained by measuring in the joint stabilizer eigenbasis of \(L_i\). Then
\[
E_i=\frac1D\sum_{P\in L_i}|\langle P\rangle|^2,
\qquad
V_U\le\sum_iE_i\le kV_U.
\]
If the supplied \(s_i\) are orthogonal and \(\psi=\sum_i c_i s_i\), then
\[
\sum_iE_i\ge\sum_i|c_i|^4\ge1/k,
\]
so \(V_U\ge k^{-2}\). This restricted theorem cannot be imported as a conditioning promise into the native task.

I have no nontrivial unrestricted-\(k\) proof of (V3).

## 4. Explicit failures of tempting proof steps

**Dropping cross dyads is not monotone.**  
In the supplied six-qubit minus state, a nonidentity \(Z\)-type Pauli receives \(4/7\) from the diagonal dyads and \(-1/7\) from the cross dyads, leaving \(3/7\). Fourth powers do not turn this destructive interference into a positive contribution that may be discarded.

**A lower frame bound on the whole dyad span is impossible.**  
Take \(s_1=|0\rangle,s_2=|1\rangle\). Then \(U=\{I,Z\}\), but
\[
X_0=|0\rangle\langle1|
\]
has zero Pauli coefficients on \(U\). Thus the visible-Pauli map has a kernel even for two orthogonal stabilizers. Any proof of (8) must exploit the positive rank-one form \(\rho=|\psi\rangle\langle\psi|\), not invert a Gram matrix on all dyads.

These are genuine counterexamples to proof steps, not counterexamples to the requested purity bound.

## 5. Conditional consequence and costs

No algorithm follows from the established controls alone. In particular, \(U\) is only a mathematical witness: the native input supplies neither its generating tableaux nor the decomposition, and enumerating \(U\), potentially of size \(k2^n\), is not a polynomial-time operation.

If (V3) were proved, it would also imply stabilizer fidelity at least \(k^{-4}\). Indeed,
\[
V_U\le\sum_iE_i\le kF_S(\psi),
\]
because each collision probability is at most the largest outcome probability in that stabilizer basis. The **supplied** self-corrector and Corollary 8.6 could then be applied with \(\tau=k^{-4}\). That is a conditional composition of existing results, not a new learner.

Its resources must include:

- all fresh input copies used for discovery and verification;
- the quoted polynomial discovery gate/time cost;
- an \(O(n^2)\)-bit output tableau and its writing cost;
- verification at overlap scale \(\gamma\): distinguishing \(p\ge\gamma\) from \(p\le\gamma/2\) takes \(O(\gamma^{-1}\log(1/\eta))\) fresh-copy Clifford measurements;
- inverse-polynomial threshold precision, requiring \(O(\log(1/\gamma)+\log(1/\eta))\) bits for the verification parameters. Verification Clifford gates can be exact.

No preparation/reflection oracle, conjugated copies, or amplitude access is introduced. If copy production has an external preparation cost, that cost multiplies the number of copies consumed.

Finally, (V3) would imply
\[
\chi(T^{\otimes m})\ge (4/3)^{m/7},
\]
confirming that the unresolved lemma carries substantial content. Polynomial extent, residual-rank preservation, and full tomography do not follow from the argument above. **The outstanding step is the unrestricted positivity inequality (8); no polynomial-cost inductive operation proving it has been established.**