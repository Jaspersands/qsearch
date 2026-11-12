## Outcome

I can construct a valid **coupled-all-\(j\)** source with a polynomial finite bit clock. Its alternating-binomial projection can also be computed before averaging.

However, the natural common-stream coupling **does not give a nonnegative count kernel**, even after averaging all secondary extensions. An exact native \(D=3\) falsifier establishes this. I do not obtain the remaining uniform variance bound or positive contraction needed for a sampler.

I use the supplied paired law, insertion interface, and moment identities as admitted; I do not re-prove them.

## 1. The common-stream coupling, and its concrete falsifier

Generate a genuine sequential uniform-rank qRSt history
\[
(P_n,Q_n,\eta_n)_{n=0}^{D},
\qquad \eta_n=\operatorname{shape}(P_n)=\operatorname{shape}(Q_n).
\]
Let \(\lambda=\eta_D\).

Independently generate random insertion maps \(F_k\), \(1\le k\le D\). Each \(F_k\) acts on a size-\((k-1)\) tableau using:

* a uniform rank in \(\{1,\ldots,k\}\);
* fresh local corner uniforms within that insertion.

Use the **same \(F_k\) across all secondary branches**. Thus their randomness is correlated between branches, but has the correct fresh law within each branch. Define
\[
\rho_n=\operatorname{shape}\!\left(F_D\circ\cdots\circ F_{n+1}(Q_n)\right),
\qquad 0\le n\le D.
\]
In particular, \(\rho_D=\lambda\). Also, because the size-one tableau is unique,
\[
\rho_0=\rho_1
\]
pathwise.

Set
\[
C_j=\cos\!\left(2\pi\tau(E_\lambda-E_{\rho_{D-j}})\right)
\]
and perform the complete projection on this one coupled sample:
\[
X_m=\binom Dm\sum_{r=0}^{D-m}(-1)^r
       \binom{D-m}{r}C_{m+r}.
\tag{1}
\]
The marginal-law verification is below. It gives
\[
\mathbb E X_m=P(N_1=m).
\]

This coupling already achieves a genuine cancellation:
\[
C_D=C_{D-1}
\quad\Longrightarrow\quad
X_{D-1}=0
\]
pathwise, matching the forbidden occupation \(N_1=D-1\). It is therefore materially different from independent-index sampling.

### Exact native \(D=3\) test

Keep the original global parameters
\[
t=\frac34,\qquad q=\frac{27}{64}
\]
also at auxiliary degree two. Choose the explicit rational input
\[
\tau_*=\frac{157464}{37}.
\]

Write
\[
R=(3),\qquad M=(2,1),\qquad C=(1,1,1).
\]
Direct substitution into the supplied native eigenvalue formula gives
\[
\tau_*(E_R-E_M)=28394,\qquad
\tau_*(E_M-E_C)=\frac{21087}{2}.
\]
Consequently, for \(f(\gamma)=e^{-2\pi i\tau_*E_\gamma}\),
\[
f(R)=f(M)=\zeta,\qquad f(C)=-\zeta
\tag{2}
\]
for an irrelevant common phase \(\zeta\).

Consider the event
\[
\eta_2=(2),\qquad \rho_0=C.
\tag{3}
\]
It has probability
\[
\pi_2((2))\,\pi_3(C)>0:
\]
the primary history and the secondary chain from the empty tableau are independent. No conditioning or rejection algorithm is being invoked here.

On this event:

* the primary endpoint \(\lambda\) is \(R\) or \(M\);
* the branch started from \(Q_2\) also ends at \(R\) or \(M\), since insertion adds one box to \((2)\);
* \(\rho_1=\rho_0=C\).

Therefore
\[
(C_0,C_1,C_2,C_3)=(1,1,-1,-1).
\]
Applying the projection **before averaging** gives
\[
(X_0,X_1,X_2,X_3)=(-4,6,0,-1).
\tag{4}
\]
Equivalently, the samplewise generating polynomial is
\[
\widehat G(z)=-4+6z-z^3.
\]

Thus this coupled projector is not a probability vector or a Bernoulli random-generation kernel. The failure is exact, not a numerical-precision artifact.

### Averaging all secondary extensions does not repair positivity

Let \(\mathcal H\) denote the complete primary history and put
\[
r=\pi_3(C),\qquad 0<r<1.
\]
For every primary history with \(\eta_2=(2)\), equation (2) implies
\[
C_1=1,\qquad
\mathbb E[C_2\mid\mathcal H]
=\mathbb E[C_3\mid\mathcal H]=1-2r.
\]
Hence
\[
\boxed{\mathbb E[X_0\mid\mathcal H]=-4r<0.}
\tag{5}
\]

This is a stronger scoped falsifier: **an exact contraction confined to the secondary randomness, while preserving this conditional expectation, cannot produce nonnegative probabilities at each fixed primary history.** A positive repair would have to cancel across different primary histories or change the representation.

Even the idealized “square conditional amplitudes first” repair fails this control. Define, analytically,
\[
g_n(\eta)=\sum_\gamma K_{n:D}(\eta,\gamma)f(\gamma).
\]
Using \(|g_{D-j}(\eta_{D-j})|^2\) gives another unbiased coupling of the moments. On \(\eta_2=(2)\), its four entries are
\[
\bigl(1,1,(1-2r)^2,(1-2r)^2\bigr),
\]
whose projected zero-count entry is
\[
-8r(1-r)<0.
\tag{6}
\]
This grants conditional-amplitude access only for the analytic test; it is **not** a paid arbitrary-shape conditioner.

Equations (4)–(6) reject these positivity mechanisms. They do **not** reject a polynomial-variance signed contraction.

## 2. The actual all-\(j\) joint law is valid

For each fixed \(n\), the supplied paired law says that, conditional on \(\eta_n\), \(P_n\) and \(Q_n\) are independent identically \(\psi\)-weighted tableaux.

The primary continuation after degree \(n\):

* starts from \(P_n\);
* uses fresh primary ranks and corner coins.

The secondary continuation:

* starts from \(Q_n\);
* uses an independent secondary stream.

Therefore, conditional on \(\eta_n\), their endpoints are independent, and after averaging their respective starting tableaux each follows the admitted upward kernel. Thus
\[
\Pr(\eta_n=\eta,\lambda=\alpha,\rho_n=\beta)
=
\pi_n(\eta)\,
K_{n:D}(\eta,\alpha)\,
K_{n:D}(\eta,\beta).
\tag{7}
\]
Sharing secondary maps between different \(n\)'s does not change any of these marginals. No independence between different \(j\)'s is claimed or needed.

Equation (7), together with the admitted moment identity, proves \(\mathbb E C_j=s_j\).

Crucially, \(P_n\) is the **actual insertion tableau at time \(n\)**. This construction does not truncate both final tableaux. \(Q_n\) may be recovered as the recording-tableau restriction, but the corresponding \(P_n\) must come from the genuine sequential history.

Neither the construction nor its implementation evaluates a \(\kappa\)-ratio or conditions on an externally supplied shape.

### Finite bit clock

At insertion degree \(k\), there are at most \(k\) active secondary branches, each using at most \(k\) local choices. Consequently,
\[
\sum_{k=1}^{D}O(k^2)=O(D^3)
\]
local-choice evaluations suffice for all branches, in addition to the primary history.

Use the supplied exact rational local CDFs. Couple each shared continuous uniform to its \(B\)-bit truncation. A union bound over the ideal local decisions gives
\[
\operatorname{TV}(\text{ideal joint source},\text{finite-bit source})
\le O(D^4\,2^{-B}).
\tag{8}
\]
This bound uses marginal uniformity within each branch, not conditional independence between branches after other branches have been exposed.

The supplied rational bit-length bounds therefore give a deterministic
\[
\operatorname{poly}\!\left(D,\log(1/\delta_{\rm path})\right)
\]
clock for joint-path error \(\delta_{\rm path}\). All streams start from the empty tableau and fair bits. There is no uncharged source preparation, rare-event rejection, or conditional normalizer.

For the \(D+1\) phases, compute
\[
\tau(E_\lambda-E_{\rho_n})\pmod 1
\]
exactly before approximating the cosine. This costs polynomial time in \(D,L\) and the requested phase bits.

Finally, all entries of (1) can be computed with polynomially many arithmetic operations. The binomial coefficients have only \(O(D)\) bits.

**What this pays is one coupled signed vector \(X\), not a count sample.**

## 3. Precision is payable; the uniform variance is not yet paid

For every ideal coupled sample,
\[
\sum_{m=0}^{D}X_m=1.
\tag{9}
\]
However, positivity fails as above.

A useful conservative bound is
\[
\begin{aligned}
\|X\|_1
&\le
\sum_{j=0}^{D}\binom Dj
       \sum_{m=0}^{j}\binom jm\\
&=3^D.
\end{aligned}
\tag{10}
\]
This is an upper bound, not a necessary sensitivity or sample-complexity lower bound.

If each cosine has absolute error at most \(\alpha\), and the complete source has TV error at most \(\delta_{\rm path}\), then
\[
\left\|\mathbb E\widetilde X-P\right\|_1
\le 3^D\alpha+2\,3^D\delta_{\rm path}.
\tag{11}
\]
Thus exponentially small tolerances here require only **linearly more precision bits**. For example,
\[
\alpha=O(\epsilon\,3^{-D}),\qquad
\delta_{\rm path}=O(\epsilon^2\,9^{-D})
\tag{12}
\]
control the bias and also make the finite implementation's second moment close enough to the ideal one. Both require
\[
O(D+\log(1/\epsilon))
\]
precision bits, plus the polynomial-size exact rational data.

The missing quantity is
\[
\boxed{
V(D,\tau)=\sum_{m=0}^{D}\operatorname{Var}_{\mathcal H,F}(X_m).
}
\tag{13}
\]
The construction completely specifies this variance, including all cross-\(j\) correlations. The admitted separate moment laws do not determine it.

I have no uniform polynomial bound for (13). The immediately available bound is only
\[
V(D,\tau)\le \mathbb E\|X\|_2^2\le 9^D.
\tag{14}
\]
Neither (14) nor the finite positivity falsifier establishes that exponential variance is necessary.

## 4. An explicit variance bound would finish the TV-\(\epsilon\) sampler

This identifies a precise remaining sufficient obligation, rather than treating the signed sum as a sampler.

Suppose one proved an **explicit, uniform**
\[
V(D,a/c)\le V_0(D,L),
\qquad V_0=\operatorname{poly}(D,L).
\tag{15}
\]
Then the following conversion would be complete:

1. Generate
   \[
   M=O\!\left(\frac{(D+1)(V_0+1)}{\epsilon^2}\right)
   \]
   independent coupled vectors, using the finite precision in (12).
2. Average them to obtain \(x\), retaining \(C_0=1\) exactly, hence \(\sum_m x_m=1\).
3. Set
   \[
   v_m=\max(x_m,0),\qquad Z=\sum_m v_m,\qquad q_m=v_m/Z.
   \]
   Here \(Z\ge1\), so this normalization has no rare-event denominator.
4. Sample \(q\) by an exact-rational CDF and a bounded uniform grid, allocating the remaining TV budget to that categorical draw.

The standard estimates are
\[
\mathbb E\|x-P\|_1
\le
\text{bias}+
\sqrt{\frac{(D+1)\sum_m\operatorname{Var}(\widetilde X_m)}{M}},
\]
and
\[
\operatorname{TV}(q,P)\le \|x-P\|_1.
\]
Averaging over the algorithm's internal randomness therefore bounds the unconditional output TV distance. No high-probability conditioning or unbounded retry loop is needed.

All arithmetic, the normalization \(Z\), and the final categorical sampling would have polynomial bit cost. The output is one \(O(\log D)\)-bit count.

This would give
\[
\operatorname{poly}(D,L,1/\epsilon)
\]
time. It would **not** give polynomial time in \(b\) when \(\epsilon=2^{-b}\).

Clipping and normalizing a **single** signed vector is not justified: it generally changes its expectation. The averaging step becomes valid only after paying a uniform variance bound such as (15).

## Exact final unsolved operation

The source access, all-\(j\) coupling, phase evaluation, and samplewise alternating projection are paid.

What remains unpaid is a **uniform cross-primary-history contraction of that projected vector** yielding either:

* a nonnegative normalized count kernel, with its conditional generation costs paid; or
* an unbiased contracted vector with an explicit polynomial total variance bound.

For the concrete common-stream construction above, the precise sufficient unresolved obligation is **(15)**. The fixed-primary-history positive contraction is already falsified by (5); simply squaring conditional amplitudes is falsified by (6).

I have not supplied the required involution, positive random-generation law, uniform generating-kernel evaluator, or variance proof. Thus this round stops without a new uniform full-\(N_1\) sampler. The supplied exhaustive baseline remains complete, and none of these scoped failures implies classical hardness or a quantum speedup.