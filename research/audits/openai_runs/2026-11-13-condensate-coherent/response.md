The spectral-measure identification is correct. I can also obtain a **coefficient-free paired-qRSt representation for every normalized factorial moment of the output mode-1 occupation**. That is more than a return-amplitude calculation.

I do **not** obtain the requested polynomial full-output sampler. The first unpaid contraction can be reduced to an explicit alternating sum of \(D+1\) efficiently samplable phase correlations. Its natural importance-sampling implementation has an exactly calculable exponential second moment. Below I distinguish that failure from any claim about other algorithms.

## 1. Normalization and the spectral law

Keep the original degree-\(D\) parameters \(q=t^3,\ t=D/(D+1)\) fixed throughout, including at auxiliary degrees \(n<D\). Write
\[
C_n=n!r_1^n,\qquad
\kappa_\lambda=[p_1^n]P_\lambda,\qquad
h_\lambda=\langle P_\lambda,P_\lambda\rangle=\frac1{b_\lambda},
\quad |\lambda|=n.
\]

The supplied Cauchy identity has logarithm
\[
\exp\!\left(\sum_{k\ge1}\frac{p_k(X)p_k(Y)}{k r_k}\right)
 =\sum_\lambda P_\lambda(X)Q_\lambda(Y).
\]
Together with \(Q_\lambda=b_\lambda P_\lambda\), this gives the stated Hall-form normalization.

For any homogeneous degree-\(n\) symmetric function,
\[
[x_1\cdots x_n]f=n![p_1^n]f:
\]
among power sums, only \(p_1^n\) contributes to that squarefree monomial. The supplied Theorem 3.3 therefore gives
\[
\sum_{T\in\operatorname{SYT}(\lambda)}\psi_T=n!\kappa_\lambda,
\qquad
\sum_T\phi_T=b_\lambda n!\kappa_\lambda.
\]

Theorem 4.25, applied to a uniform permutation, gives the **tableau-pair law**
\[
\Pr(P,Q)=\frac{r_1^n}{n!}\psi_P\phi_Q.
\tag{1}
\]
Consequently its shape law is
\[
\boxed{\pi_n(\lambda)=C_n\frac{\kappa_\lambda^2}{h_\lambda}.}
\tag{2}
\]
This is normalized because (1) is a probability distribution.

With the positive normalization of the Macdonald eigenvectors,
\[
v_n(\lambda):=
\left\langle \frac{P_\lambda}{\sqrt{h_\lambda}},
                \frac{p_1^n}{\sqrt{C_n}}\right\rangle
=\sqrt{\pi_n(\lambda)}.
\]
Thus the target state is
\[
|\Psi_\tau\rangle
=\sum_{\lambda\vdash D}v_D(\lambda)\zeta_\lambda|\lambda\rangle,
\qquad
\zeta_\lambda=e^{-2\pi i\tau E_\lambda}.
\tag{3}
\]

In particular,
\[
A(\tau)=\mathbb E_{\pi_D}\zeta_\lambda
\]
is the return amplitude. This does not yet address occupation sampling.

### A useful consequence of the full tableau-pair law

Equation (3.2) in the extract telescopes along a tableau:
\[
\phi_T=b_\lambda\psi_T.
\]
Hence, conditional on the common shape \(\eta\), the two tableaux in (1) are independent and have the same distribution:
\[
\boxed{
\Pr(P,Q\mid\eta)=
 \frac{\psi_P}{n!\kappa_\eta}
 \frac{\psi_Q}{n!\kappa_\eta}.
}
\tag{4}
\]
This conditional independence is what makes the paired-growth construction below possible without evaluating \(\kappa_\eta\).

## 2. A paid paired-growth contraction

Let
\[
a_1=\sqrt{r_1}\,\partial_{p_1},
\qquad
a_1^\dagger=\frac{p_1}{\sqrt{r_1}},
\qquad N_1=a_1^\dagger a_1.
\]
These are the normalized mode-1 annihilation, creation and occupation operators.

### 2.1 Positive one-box lowering

Splitting off the largest alphabet variable in Theorem 3.3 gives the branching identity
\[
P_\lambda(X+x)
=\sum_{\eta:\lambda/\eta\text{ horizontal strip}}
 \psi_{\lambda/\eta}P_\eta(X)x^{|\lambda/\eta|}.
\]
Taking the coefficient of \(x\),
\[
\partial_{p_1}P_\lambda
=\sum_{\eta\lessdot\lambda}\psi_{\lambda/\eta}P_\eta.
\]
Therefore the normalized matrix of \(a_1\) is positive:
\[
B_{\eta\lambda}
=\langle\eta|a_1|\lambda\rangle
=\sqrt{r_1}\,\psi_{\lambda/\eta}
  \sqrt{\frac{h_\eta}{h_\lambda}}.
\tag{5}
\]

Define an upward shape kernel, for \(|\eta|=n\), by
\[
K_n^\uparrow(\eta,\lambda)
=\frac{B_{\eta\lambda}v_{n+1}(\lambda)}
       {\sqrt{n+1}\,v_n(\eta)}
=r_1\phi_{\lambda/\eta}\frac{\kappa_\lambda}{\kappa_\eta}.
\tag{6}
\]
It is stochastic: this follows directly from
\[
a_1|\Omega_{n+1}\rangle=\sqrt{n+1}|\Omega_n\rangle,
\qquad
|\Omega_n\rangle=\frac{p_1^n}{\sqrt{C_n}}.
\]

**Equation (6) is not being offered as a coefficient oracle.** Its samples can be generated without computing either \(\kappa\).

### 2.2 Sampling the upward kernel without its normalizer

Under uniform-permutation qRSt, the recording-tableau marginal is
\[
\Pr(Q=T)=r_1^n\kappa_\eta\phi_T,
\qquad \operatorname{shape}(T)=\eta.
\]
If \(T^+\) extends \(T\) by one box to \(\lambda\), the ratio of these recording-path probabilities is exactly (6).

A uniform permutation can be grown by inserting a new uniformly chosen rank at each step. The supplied local growth rules implement that insertion by extending the growth diagram with a strip. Thus:

* start with an insertion tableau distributed as
  \(\psi_T/(n!\kappa_\eta)\);
* choose each subsequent insertion rank uniformly;
* perform qRSt insertion with fresh local randomness.

After averaging over the initial tableau, its shape evolves according to \(K_n^\uparrow\). This uses the insertion/growth construction in the supplied Theorem 4.25 proof, not a new eigenvector interface.

Now apply (4): qRSt at degree \(n\) supplies **two independent copies of the required initial tableau conditional on \(\eta\)**.

### 2.3 Explicit paired sampler

For \(j\in\{0,\ldots,D\}\), set \(n=D-j\).

1. Run uniform-permutation qRSt at degree \(n\), using the original global \(q,t\), obtaining \(P,Q\) of common shape \(\eta\).
2. Independently extend \(P\) and \(Q\) to size \(D\), using uniform-rank qRSt insertions and independent local randomness.
3. Let the final shapes be \(\lambda,\rho\).
4. Return
   \[
   W_j=\exp[-2\pi i\tau(E_\lambda-E_\rho)].
   \]

Its joint endpoint law is exactly
\[
\pi_n(\eta)
K^\uparrow_{n:D}(\eta,\lambda)
K^\uparrow_{n:D}(\eta,\rho).
\tag{7}
\]

No conditional tableau normalizer is evaluated. Nor are path labels deleted and then mistaken for a coherent inverse transform: equation (7) explicitly specifies the sum over those paths.

### 2.4 What this contraction computes

Telescoping (6) along \(j\) upward steps gives
\[
(a_1^j\Psi_\tau)_\eta
=\sqrt{(D)_j}\,v_n(\eta)
 \sum_{\lambda\vdash D}
 K^\uparrow_{n:D}(\eta,\lambda)\zeta_\lambda.
\]
Taking its squared norm proves
\[
\boxed{
s_j(\tau):=
\frac{\mathbb E_{\Psi_\tau}(N_1)_j}{(D)_j}
=
\mathbb E W_j
=
\sum_{\eta\vdash D-j}\pi_{D-j}(\eta)
\left|
 \mathbb E[\zeta_\lambda\mid\eta]
\right|^2 .
}
\tag{8}
\]
Here \(s_0=1\). At \(j=D\), the two growths start from the empty tableau independently, giving
\[
s_D=|A(\tau)|^2.
\]

Equation (8) holds for growing \(D\), not a fixed-boson subcase. It gives a bounded estimator for every normalized factorial moment of the actual coherent output:
\[
|W_j|=1,\qquad
s_j=\mathbb E\cos[2\pi\tau(E_\lambda-E_\rho)].
\]

## 3. Finite bit clocks and precision

The positive formulas in Proposition 4.17 are sufficient for polynomial finite-bit sampling.

At the prescribed specialization, their factors have the form
\[
1-q^i t^j=1-t^{3i+j},
\]
with nonnegative exponents of size \(O(D)\). Each factor has numerator and denominator of \(O(D\log(D+1))\) bits. Conservatively:

* one corner probability uses \(O(D)\) factors and has \(O(D^2\log(D+1))\) bits;
* exact cumulative probabilities over all corners need at most \(O(D^3\log(D+1))\) bits;
* a growth diagram, or the paired construction above, uses \(O(D^2)\) local choices.

Sampling each categorical choice using an \(s\)-bit uniform threshold introduces at most \(O(D2^{-s})\) TV error per choice. Including uniform permutation/rank generation, the total error is bounded by
\[
C D^3 2^{-s}
\]
for an absolute implementation constant \(C\). Thus joint-path TV error \(\eta\) requires only
\[
s=\left\lceil\log_2(CD^3/\eta)\right\rceil.
\tag{9}
\]
A coarse implementation uses \(O(D^4)\) rational arithmetic operations on
\(O(D^3\log(D+1)+s)\)-bit integers. This is a worst-case finite clock, not an uncharged exact rational coin.

For the phases, all degree-\(D\) eigenvalues have a common denominator dividing
\[
D^{3D}(D+1)^{D-1}.
\]
Their exact rational descriptions therefore have \(O(D\log(D+1))\) bits. Compute
\[
\tau(E_\lambda-E_\rho)\pmod 1
\]
exactly, using \(O(L+D\log(D+1))\)-bit integers, before approximating the exponential.

Consequently an additive-\(\gamma\), failure-probability-\(\delta\) estimate of one \(s_j\) costs
\[
O\!\left(\gamma^{-2}\log\frac1\delta\right)
\operatorname{poly}\!\left(D,L,\log\frac1\gamma\right).
\tag{10}
\]
The same accounting applies to \(A(\tau)\). This is polynomial in inverse additive error, **not polynomial in \(b\) when \(\gamma=2^{-b}\)**.

No coefficient table, eigenstate preparation, or hidden state-loading step occurs in this construction.

## 4. The first unpaid contraction

The mode-1 probability-generating function is exactly
\[
G_1(z)=\mathbb E z^{N_1}
=\sum_{j=0}^D\binom Dj s_j(\tau)(z-1)^j.
\tag{11}
\]
Thus
\[
\Pr(N_1=m)
=\binom Dm
 \sum_{r=0}^{D-m}(-1)^r
 \binom{D-m}{r}s_{m+r}(\tau).
\tag{12}
\]

Already the binary event “no mode-1 bosons” requires
\[
\boxed{
B_D(\tau):=\Pr(N_1=0)
=\sum_{j=0}^D(-1)^j\binom Dj
 \mathbb E_{\mathrm{PairGrow}(D-j\to D)}
 e^{-2\pi i\tau(E_\lambda-E_\rho)}.
}
\tag{13}
\]

This is the smallest concrete unpaid contraction in this route. Equivalently, it is the expectation of the exact vacuum projector
\[
\mathbf 1_{\{N_1=0\}}
=\sum_{j=0}^D\frac{(-1)^j}{j!}
 (a_1^\dagger)^j a_1^j.
\tag{14}
\]

Every expectation in (13) now has a polynomial-clock, coefficient-free sampler. What is missing is a polynomial-cost contraction or nonnegative random-generation representation of their alternating combination.

### 4.1 Exact variance accounting

Choose an index \(j\) with probabilities \(w_j>0\), then run the corresponding paired sampler. The unbiased estimator
\[
Y=\frac{(-1)^j\binom Dj}{w_j}W_j
\]
has
\[
\mathbb E|Y|^2
=\sum_{j=0}^D\frac{\binom Dj^2}{w_j}
\ge \left(\sum_{j=0}^D\binom Dj\right)^2
=4^D.
\tag{15}
\]
The optimum is attained by \(w_j=\binom Dj/2^D\), giving
\[
Y=2^D(-1)^jW_j,\qquad
\mathbb E|Y-B_D|^2=4^D-B_D^2.
\tag{16}
\]

So **even optimal single-index importance sampling of this uncollapsed unit-phase representation has exponential second moment**. Taking real parts does not establish a uniform remedy: at \(\tau=0\), \(W_j=1\), \(B_D=0\), and the real estimator has variance exactly \(4^D\).

The zero-time cancellation can of course be performed analytically. That observation does not supply a contraction valid for arbitrary binary \(\tau\).

For this sample-mean scheme, additive error \(\epsilon\) requires order
\[
4^D\epsilon^{-2}
\]
samples. Its phase and local-probability precision need only \(b+O(D+\log D)\) bits when \(\epsilon=2^{-b}\); **the bad cost is sample count, not the bit length of individual phases**.

Likewise, if every \(s_j\) is estimated within \(\eta\), (12) gives
\[
\sum_m|\widehat{\Pr}(N_1=m)-\Pr(N_1=m)|
\le 3^D\eta.
\tag{17}
\]
The straightforward moment-table route to mode-1 TV error \(2^{-b}\) therefore uses \(\eta=O(2^{-b}3^{-D})\), with an exponential statistical cost.

These are failures of specified estimators. They are not lower bounds against coupled estimators, analytic contractions, or another sampler.

### Is (13) simpler than the original problem?

It is simpler in representation:

* one scalar marginal rather than \(p(D)\) output probabilities;
* only \(D+1\) explicitly samplable correlations;
* no general power-sum coefficient or character evaluation.

But there is no proved polynomial contraction. The implementation above is asymptotically worse than the supplied partition-enumeration baseline.

Also, evaluating \(B_D\) to exponentially small additive error is not something every full sampler must explicitly do. Equation (13) is an unpaid step of this conditional-norm approach, not a complexity equivalence.

## 5. Exact obligations for continuing to full occupation output

For all modes define
\[
a_k=\sqrt{k r_k}\,\partial_{p_k}.
\]
The full generating functional has the finite exact expansion
\[
\boxed{
G_\tau(\mathbf z)
=\sum_{\mathbf j:\,\sum k j_k\le D}
 \left[\prod_k\frac{(z_k-1)^{j_k}}{j_k!}\right]
 \left\|\prod_k a_k^{j_k}\Psi_\tau\right\|^2.
}
\tag{18}
\]

More specifically, the joint weight of an occupation prefix
\(N_1=m_1,\ldots,N_s=m_s\) is
\[
\boxed{
W(m_1,\ldots,m_s)
=
\sum_{\substack{\mathbf j\ge0\\
 \sum_{k\le s}k(m_k+j_k)\le D}}
 \frac{(-1)^{\sum j_k}}{\prod_{k\le s}m_k!j_k!}
 \left\|
   \prod_{k\le s}a_k^{m_k+j_k}\Psi_\tau
 \right\|^2 .
}
\tag{19}
\]
Thus the remaining conditional probabilities are precisely ratios of these weights.

There is also an explicit source-based lowering representation beyond mode 1. Define
\[
\mathcal B(z)f(\mathbf p)
=f(p_1+z,p_2+z^2,\ldots)
=\sum_{r\ge0}z^r\mathcal B_r f.
\]
By Theorem 3.3, \(\mathcal B_r\) is the positive horizontal-strip lowering matrix with weights \(\psi_{\lambda/\eta}\). But
\[
\log\mathcal B(z)=\sum_{k\ge1}z^k\partial_{p_k},
\]
so, already,
\[
\partial_{p_2}=\mathcal B_2-\frac12\mathcal B_1^2.
\tag{20}
\]
More generally,
\[
\partial_{p_k}
=\sum_{\ell=1}^k\frac{(-1)^{\ell-1}}{\ell}
 \sum_{\substack{r_1+\cdots+r_\ell=k\\r_i\ge1}}
 \mathcal B_{r_1}\cdots\mathcal B_{r_\ell}.
\tag{21}
\]
This identifies the higher-mode signed contraction without importing a character oracle.

A complete polynomial sampler still needs all of the following concrete payments:

1. **Contract (13), then the relevant prefix weights (19), or sample their branches directly**, with polynomial representation size and a uniform cost bound for arbitrary allowed \(\tau\).
2. **Handle conditioning.** The current paired construction uses the unconditioned condensate vector \(v_D\). After an occupation prefix is imposed, one cannot restart it as a fresh condensate at a smaller degree.
3. **Prove the sampling clock and TV bound.** For a sequential occupation sampler, conditional TV errors can be budgeted to sum to \(2^{-b}\), but small prefix weights must be handled rather than divided by without a cost analysis. A variance bound alone normally gives inverse-error estimation cost; a polynomial-\(b\) sampler additionally needs a justified random-generation mechanism.
4. **Charge output.** An explicit occupation vector or partition takes \(O(D\log(D+1))\) bits. Nothing in the preceding construction removes that cost.

No such completion is established here.

## 6. Cheapest exact coherence falsifier

\(D=1\) is one-dimensional. The first nontrivial exact test is \(D=2\), at the required native parameters
\[
t=\frac23,\qquad q=\frac8{27}.
\]
The supplied tableau formulas give
\[
P_{(2)}=\frac{7p_1^2+19p_2}{26},
\qquad
P_{(1,1)}=\frac{p_1^2-p_2}{2},
\]
and
\[
r_1=\frac{19}{9},\qquad r_2=\frac{133}{81}.
\]
Consequently
\[
\pi_2((2))=\frac7{26},\qquad
\pi_2((1,1))=\frac{19}{26}.
\]

With occupation rows \((1,1),(2)\) and eigenvector columns \((2),(1,1)\),
\[
U=
\begin{pmatrix}
\sqrt{7/26}&\sqrt{19/26}\\
\sqrt{19/26}&-\sqrt{7/26}
\end{pmatrix}.
\]
The energies are
\[
E_{(2)}=\frac{665}{64},\qquad
E_{(1,1)}=\frac{95}{24},\qquad
\Delta E=\frac{1235}{192}.
\]
Therefore
\[
\boxed{
P_{\,(1,1),\tau}((2))
=\frac{133}{169}
 \sin^2\!\left(\pi\tau\frac{1235}{192}\right).
}
\tag{22}
\]

Two exact tests are:

| \(\tau\) | \(P((1,1))\) | \(P((2))\) |
|---|---:|---:|
| \(0\) | \(1\) | \(0\) |
| \(96/1235\) | \(36/169\) | \(133/169\) |

A spectral-shape draw followed by a phase-blind eigenstate mixture instead gives the time-independent value
\[
P((2))=\frac{133}{338}.
\]
It therefore fails already at this instance.

Moreover, the eigenbasis projector onto occupation \((2)\) has off-diagonal entry
\[
U_{(2),(2)}U_{(2),(1,1)}
=-\frac{\sqrt{133}}{26}.
\]
Thus substituting nonnegative qRSt transition weights for this occupation projector is not an identity. This falsifies that shortcut, not the possibility of a different positive representation.

---

**Established:** the spectral identity, a polynomial finite-TV qRSt clock, and the coefficient-free paired-growth formula (8) for all mode-1 factorial moments.

**Unpaid:** the explicit projector contraction (13), followed by the conditional higher-mode contractions (19).

The guaranteed complete full-output algorithm remains the supplied
\[
\exp(O(\sqrt D))\,\operatorname{poly}(D,L,b)
\]
enumeration baseline. The calculations above establish neither classical hardness nor a quantum speedup.