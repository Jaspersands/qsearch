## Findings

I do **not** obtain the requested \(C^r\operatorname{poly}(B,n,r)\) second-moment bound.

I obtain two concrete results:

1. **A common heat-tree collapse is biased already at \(r=1\), on a two-bit native circuit—even when its expansion includes every mixed-scale term.**
2. **An exact antithetic repair cancels constants before multiplying weights, but retains an \(H^{2(r+1)}\) second-moment obstruction on that same native circuit.** This obstruction holds for every full-support joint distribution of the scale tuple within the repaired sampler class.

These are statements about specified estimators, not hardness or a classical–quantum separation.

## 1. Cheapest native counterexample to sharing the heat tree

Take \(j=1\), \(n\ge2\), and
\[
\sigma(x,1)=s(x_1):=
\begin{cases}
-1,&x_1\bmod4=3,\\
+1,&\text{otherwise},
\end{cases}
\qquad \sigma(x,2)=+1.
\]
This is a constant-size phase circuit using two coordinate bits and the direction bit.

On direction-1 fields independent of \(x_2\),
\[
\Pi=P:=I-P_{\rm mean}.
\]
Write \(\mu=\mathbb E s=1/2\), \(b=s-\mu\). Then
\[
P\Sigma P\,b=-\mu b,\qquad \|b\|_2^2=1-\mu^2=\frac34.
\]
Consequently, for this entire native family,
\[
\boxed{T_r=\frac34\left(-\frac12\right)^r.}
\]
In particular, \(T_1=-3/8\). Spatial norms here use uniform spatial measure.

### A concrete common-tree operation

Let \(H_t\) be the one-dimensional free heat semigroup on this invariant subspace. Here the truncated projection is exactly
\[
\Pi_T=I-H_T.
\]
For dyadic breakpoints \(0=t_0<\cdots<t_H=T\), generate **one** Poisson heat path \(Y_t\), and put
\[
\widehat Q_\ell=S_{Y_{t_\ell}}-S_{Y_{t_{\ell+1}}}.
\]
Each band has the correct mean:
\[
\mathbb E\widehat Q_\ell=H_{t_\ell}-H_{t_{\ell+1}}.
\]

The proposed cancellation before multiplication is
\[
\widehat A=\sum_\ell\widehat Q_\ell=I-S_{Y_T}.
\]
Reusing this same \(\widehat A\) in every factor gives
\[
Z_{\rm shared}(x)
 =[\Sigma\widehat A(\Sigma\widehat A)^r\Sigma1](x).
\]

**This does not select a common scale.** Expanding its sums includes every tuple
\((\ell_1,\ldots,\ell_{r+1})\). Its apparent advantages are real:

- constants are annihilated pointwise;
- expansion costs at most \(O(2^{r+1})\) material evaluations;
- \(\mathbb E|Z_{\rm shared}|^2\le4^{r+1}\).

But its mean is wrong.

For \(r=1\), direct expansion gives
\[
Z_{\rm shared}(x,Y)
=-s(x+Y)+s(x)s(x+Y)s(x+2Y).
\]
Averaging over \(x\bmod4\) gives \(0\) when \(Y\) is even and \(-1\) when \(Y\) is odd. Thus
\[
\mathbb E Z_{\rm shared}
=-\frac{1-e^{-4T}}2.
\]

For comparison, writing
\[
a_T=1-e^{-2T},\qquad b_T=1-e^{-4T},
\]
the correct moment with both projections truncated at the **same** \(T\) is
\[
T_1^{(T)}=\frac{b_T^2}{8}-\frac{a_Tb_T}{2}.
\]
Therefore
\[
\boxed{
\mathbb E Z_{\rm shared}-T_1^{(T)}
=-\frac{b_Te^{-2T}}2-\frac{b_T^2}{8}.
}
\]
The discrepancy tends to \(-1/8\), rather than disappearing with the cutoff error.

There is also an entirely finite, fair-bit version of the falsifier. Replace the stationary heat endpoint by an exactly uniform translation \(U\). Then
\[
\mathbb E[I-S_U]=P,
\]
but the shared-translation estimator has mean \(-1/2\), whereas \(T_1=-3/8\). No Poisson backend or numerical precision is involved in this test.

**Falsified operation:** replacing products of mean heat-band operators by products constructed from a shared empirical heat tree. Correct marginals and inclusion of all mixed scales do not eliminate the covariance
\[
\mathbb E[\widehat A\Sigma\widehat A]
-(\mathbb E\widehat A)\Sigma(\mathbb E\widehat A).
\]

### Genuine martingale differences do not automatically fix this

The preceding heat differences are not Doob martingale differences. But genuine martingale orthogonality also fails after inserting arbitrary \(\Sigma\).

Let \(A,B\) be the Rademacher variables given by the most and least significant bits of \(x_1\), and use the native phase
\[
s_n=\frac{1+A+B-AB}{2}.
\]
For the dyadic filtration revealing coordinate bits from coarse to fine, the only nonzero differences are
\[
u=\frac A2,\qquad v=\frac{B(1-A)}2.
\]
They can be separated by \(n-1\) levels. Although \(\mathbb E[uv]=0\),
\[
\boxed{\mathbb E[u\,s_n\,v]=-\frac14.}
\]
Indeed,
\[
\mathbb E[u\,s_n\,u]=\frac18,\qquad
\mathbb E[v\,s_n\,v]=0,
\]
so the two mixed terms supply \(-1/2\) of the correct \(T_1=-3/8\).

Thus neither martingale orthogonality nor large scale separation permits deleting these mixed terms under the native input contract.

## 2. An exact repair that cancels before multiplying weights

Here is a general-circuit antithetic construction. It is exact at the ideal truncated-integral level, but its proved second moment is not decisive.

Consider a large interval \([w,2w]\), with \(t\) uniform in that interval. For component \(ij\), duplicate the two marked Poisson counts:
\[
N,N'\sim{\rm Pois}(t)\quad\text{for }(i,+),\qquad
M,M'\sim{\rm Pois}(t)\quad\text{for }(j,-).
\]
Keep the other two counts shared. Let \(Y^{ab}\), \(a,b\in\{0,1\}\), denote the four displacements obtained by choosing the corresponding copies. Define
\[
\begin{split}
(\widehat Q_{ij,w}f)(x)
={}&\frac{w(N-N')(M-M')}{4t^2}\\
&\quad{}\times
\big[f(x+Y^{00})-f(x+Y^{10})
-f(x+Y^{01})+f(x+Y^{11})\big].
\end{split}
\tag{1}
\]
This annihilates constant \(f\) **in every realization**, before operator weights are multiplied.

The elementary identity
\[
\mathbb E[(N-N')(F(N)-F(N'))]
=2\mathbb E[(N-t)F(N)]
\]
applied twice proves
\[
\mathbb E\widehat Q_{ij,w}
=\int_w^{2w}D_i e^{-tK_0}D_j^*\,dt.
\]
For \([0,1]\), use the four local shifts
\[
S_{e_i-e_j}-S_{e_i}-S_{-e_j}+I
\]
after a sampled heat displacement, evaluating all four terms rather than selecting one.

Let \(m=r+1\), and let \(H\) be the number of intervals. For a scale tuple
\(\boldsymbol\ell=(\ell_1,\ldots,\ell_m)\), draw independent factor innovations conditional on that tuple. Their shifts are reused throughout all branches belonging to the same factor.

For any full-support tuple law \(p(\boldsymbol\ell)\),
\[
Z=
\frac{
[\Sigma\widehat Q_{\ell_1}\Sigma\cdots
 \widehat Q_{\ell_m}\Sigma1_j](X,j)
}{p(\boldsymbol\ell)},
\qquad X\ \text{uniform}.
\tag{2}
\]
Then
\[
\mathbb EZ
=\langle\eta_j,\Sigma\Pi_T(\Sigma\Pi_T)^r\Sigma\eta_j\rangle.
\]
Every mixed-scale tuple is included.

This repair does **not** establish the requested across-factor common-increment theorem: its unbiasedness proof uses independent innovations between factor occurrences.

### Work and upper moments

Each full edge operator has at most eight descendants per queried edge: two next directions and four antithetic corners. Hence one transcript uses

- \(O(8^m)\) material evaluations;
- at most \(24m\) Poisson draws;
- no dense spatial sum or conditional heat expectation.

Direct shift-norm bounds give, uniformly in the scale,
\[
\mathbb E\|\widehat Q_\ell f\|_2^2\le64\|f\|_2^2,
\qquad
\mathbb E\|\widehat Q_\ell f\|_4^4\le4096\|f\|_4^4.
\]
For the large intervals, these follow from
\[
\mathbb E(N-N')^2=2t,\qquad
\mathbb E(N-N')^4=12t^2+2t.
\]

Choose independent scale probabilities satisfying
\(p_\ell\ge1/(2H)\). Such probabilities are generated exactly by drawing
\(\lceil\log_2H\rceil\) bits and mapping the resulting integer modulo \(H\).
Then
\[
\boxed{
\mathbb EZ^2\le V:=(256H^2)^m,\qquad
\mathbb EZ^4\le V^2.
}
\tag{3}
\]

The work is \(C^r\) times a polynomial in the native bit parameters. The second moment still contains \(H^{2m}\).

## 3. A proved second-moment obstruction for this repair

The period-four circuit from Section 1 shows that (3) is not merely a loose treatment of constant media.

On its invariant subspace, only component \(11\) survives pointwise. For a nonzero period-four Fourier angle
\(\theta\in\{\pi/2,\pi,3\pi/2\}\), define
\[
g_t(\theta)=
\mathbb E\!\left[(N-N')^2
  |e^{i\theta N}-e^{i\theta N'}|^2\right].
\]
The Skellam characteristic function gives
\[
g_t(\pi/2)=g_t(3\pi/2)=4t(1+2te^{-2t}),
\qquad
g_t(\pi)=4t(1+e^{-4t}).
\]
Thus the squared Fourier multiplier of (1) satisfies
\[
\mathbb E|\widehat q_\ell(\theta)|^2
=\frac{w^2}{16t^4}g_t(\theta)^2
\ge\frac{w^2}{t^2}\ge\frac14.
\]
The small interval satisfies the same lower bound. Consequently,
\[
\mathbb E\|\widehat Q_\ell f\|_2^2
\ge\frac14\|Pf\|_2^2
\tag{4}
\]
on the period-four subspace.

Every realization maps into the mean-zero subspace. For mean-zero \(f\),
\[
\|P\Sigma f\|_2^2
=\|f\|_2^2-|\langle s,f\rangle|^2
\ge\mu^2\|f\|_2^2=\frac14\|f\|_2^2.
\]
Starting from \(\|Ps\|_2^2=3/4\), repeated application of (4) gives, for **every** scale tuple,
\[
\mathbb E|F_{\boldsymbol\ell}|^2\ge 3\,16^{-m},
\]
where \(F_{\boldsymbol\ell}\) is the numerator in (2). Therefore every full-support joint scale law obeys
\[
\begin{split}
\mathbb EZ^2
&=\sum_{\boldsymbol\ell}
 \frac{\mathbb E|F_{\boldsymbol\ell}|^2}
      {p(\boldsymbol\ell)}\\
&\ge 3\,16^{-m}
 \left(\#\{\boldsymbol\ell\}\right)^2
=\boxed{3\left(\frac{H^2}{16}\right)^m}.
\end{split}
\tag{5}
\]

**Scope of this theorem:** arbitrary joint scale reweighting cannot fix this antithetic, factor-replica sampler with the universal \(H\)-band cutoff. It does not cover a new across-factor coupling with explicit covariance corrections, material-aware analytic simplifications, or another end-to-end method. This layered circuit itself is easy; recognizing its period can bypass the unnecessarily long heat cutoff.

## 4. Bounded finite transcript and charged costs

The following finite-clock consequence uses the **binomial-sampling guarantee stated in the packet**, not an assumed unit-cost Poisson oracle.

For desired per-moment bias \(b\le1\), set
\[
\tau=\frac{b}{8m},\qquad
T=2^J\ge\max\!\left(1,\frac{L^2}{16}\log\frac2\tau\right),
\qquad h\le\frac{\tau}{128T},
\]
with dyadic \(h\) and midpoint time grids.

The full integrand derivative has norm at most \(64\). Thus cutoff plus quadrature operator error is at most \(\tau\), and the resulting product bias is below \(b/4\). Here
\[
H=O\!\left(n+\log\log(m/b)\right).
\]

For the ideal grid estimator, use \(V\) from (3), and:

1. **Clip the completed transcript** at
   \[
   A=\frac{4V}{b}.
   \]
   Lost first moment is at most \(V/A=b/4\).

2. With \(F=24m\), set per-count TV tolerance
   \[
   \beta\le\frac{b}{16AF}.
   \]
   Choose a power-of-two
   \[
   Q\ge\max(T,2T^2/\beta),
   \]
   replace each Poisson count by \({\rm Binomial}(Q,t/Q)\), and sample it to TV at most \(\beta/2\). Whole-transcript TV is at most \(F\beta\). Because clipping precedes this comparison, the additional mean error is at most \(b/8\), and the second moment increases by at most \(V/4\).

3. Round the completed, clipped value to a common dyadic spacing at most \(b/8\), before averaging.

The actual bounded transcript therefore has bias at most \(b\) and second moment at most \(4V\). No expectation of an unbounded weight is bounded using TV.

All count, time, weight, product, and accumulator bit lengths are polynomial in
\[
B,n,m,\log(1/b)
\]
and the native scalar-input bit lengths. A transcript costs
\[
8^m\operatorname{poly}(B,n,m,\log(1/b))
\]
bit operations, including material evaluation, coordinate arithmetic, random-bit clocks and weight arithmetic. Uniform starting positions cost \(2n\) random bits. Completed values are rounded before accumulation, avoiding denominator growth with the number of samples.

Median-of-means needs
\[
O\!\left(Va^{-2}\log(1/\delta)\right)
\]
transcripts for statistical error \(a\). This recovers a quasi-polynomial joint-precision bound, not the sought polynomial match.

The variance obstruction is not an artifact of infinite Poisson tails: clipping loses at most
\[
\mathbb EZ^4/A^2\le b^2/16
\]
of the second moment. Reducing the finite-sampler TV tolerance further preserves a constant fraction of (5), with only polynomial additional bit precision.

## 5. Exact next falsifier and remaining obligation

A new common-tree coupling should first pass these algebraic tests:

- **Two-bit circuit, \(r=1\):** return mean \(-3/8\), not \(-1/2\), for \(s=(1,1,1,-1)\).
- **Arbitrarily separated dyadic levels:** retain
  \[
  \mathbb E[u\,s_n\,v]=-\frac14
  \]
  for the top-bit/low-bit circuit above.

For a genuine Doob construction, the unresolved paid operation is evaluating or estimating the necessary **conditional expectations and their products**. Replacing each conditional expectation by one shared completion introduces precisely the covariance problem exposed here. Those conditional computations cannot be counted as single material queries.

The remaining proof obligation is an explicit correction or different representation that preserves all such mixed terms while bounding both work and second moment by \(C^r\operatorname{poly}(B,n,r)\). Nothing above rules out that possibility.