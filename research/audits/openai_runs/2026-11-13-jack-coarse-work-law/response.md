**I cannot supply a complete polynomial classical sampler for unrestricted \(\lambda\).** Two concrete closures fail exact tests below. What survives is a polynomial computation of the first moment and the two extreme-bin probabilities—not the full law. I do not have a materially narrower conditional reduction that closes the remaining gap.

All calculations below use the explicit partition and the stated normalization, without a state-preparation, coefficient-table, or moment oracle.

## 1. The eigenstate equation supplies two moments, not a moment recurrence

Write
\[
t=\frac{2}{\sqrt3},\qquad
|\psi\rangle=|\widehat J_\lambda^{(3)}\rangle,\qquad
A=E_i-tN.
\]
The initial eigenstate equation gives
\[
S|\psi\rangle=A|\psi\rangle.
\]
Consequently,
\[
\langle S\rangle=\langle A\rangle,\qquad
\langle S^2\rangle=\langle A^2\rangle.
\]
These are genuine deductions. If an occupation sampler is available for an input, it can estimate these two moments from the diagonal random variable \(A(\mu)\).

But \(S^k|\psi\rangle=A^k|\psi\rangle\) does **not** follow: already
\[
S^2|\psi\rangle=A^2|\psi\rangle+[S,A]|\psi\rangle.
\]

### Cheapest falsifier: \(D=2,\lambda=(2)\)

In the ordered occupation basis \((|1,1\rangle,|2\rangle)\),
\[
S=\begin{pmatrix}0&2\\2&0\end{pmatrix},\quad
N=\begin{pmatrix}2&0\\0&4\end{pmatrix},\quad
|\psi\rangle=\begin{pmatrix}1/2\\ \sqrt3/2\end{pmatrix},
\quad E_i=\frac{10}{\sqrt3}.
\]
Thus \(A\) takes values \(2\sqrt3\) and \(2/\sqrt3\), with occupation probabilities \(1/4\) and \(3/4\). Nevertheless,
\[
\langle S^3\rangle=4\sqrt3,
\qquad
\langle A^3\rangle=\frac{20}{\sqrt3}.
\]

So pushing the occupation law through \(E_i-tN\) fails even on an already-classically-tractable row input. This falsifies that closure, not classical tractability.

## 2. Even the complete dispersion eigenvalue curve does not determine the work law

Define
\[
a_\lambda=\sum_{s\in\lambda}x(s)=n(\lambda'),\qquad
b_\lambda=\sum_{s\in\lambda}y(s)=n(\lambda).
\]
For the auxiliary parameterization
\[
H(t)=S+tN,\qquad t=q-q^{-1},\quad q>0,
\]
the same Jack diagonalization gives
\[
E_\lambda(q)
=q(2a_\lambda+D)-q^{-1}(2b_\lambda+D).
\]
Equivalently,
\[
E_\lambda(t)
=(a_\lambda-b_\lambda)\sqrt{t^2+4}
 +(a_\lambda+b_\lambda+D)t.
\]

Hellmann–Feynman therefore supplies the exact controls
\[
\boxed{\langle N\rangle
=D+\frac{3a_\lambda+b_\lambda}{2}},
\qquad
\boxed{\mathbb E[e]=\sqrt3(a_\lambda-b_\lambda)}
\]
at \(q=\sqrt3\). Differentiating the specified Jack eigenvector is legitimate also at persistent degeneracies; a nondegenerate eigenvalue assumption is unnecessary.

This does not initialize a full energy-moment recurrence. In fact, two inputs can have identical \(E_\lambda(t)\) for **every** dispersion parameter and different coarse work laws.

### An independently computable distinguishing bin

Put \(L=D(D-1)\). The final energy \(L\) has the unique Schur shape \((D)\), and \(-L\) has the unique shape \((1^D)\).

In the integral-Jack normalization underlying the contract,
\[
H_\lambda
=\prod_{s\in\lambda}
 (3a(s)+l(s)+1)(3a(s)+l(s)+3),
\]
and the principal-specialization identity is
\[
J_\lambda^{(3)}(p_k=u\text{ for all }k)
=\prod_{s\in\lambda}(u+3x(s)-y(s)).
\]
Because
\[
h_D=\sum_{\mu\vdash D}\frac{p_\mu}{z_\mu},
\]
Hall inner-product contraction gives
\[
\langle f_\lambda,h_D\rangle
=\frac{J_\lambda^{(3)}(p_k=\sqrt3)}{\sqrt{H_\lambda}}.
\]
The analogous elementary-symmetric-function contraction gives the other endpoint. Hence, for \(D\ge2\),
\[
\boxed{
P_\lambda(L)=
\frac{\displaystyle\prod_{s\in\lambda}
       (\sqrt3+3x(s)-y(s))^2}{H_\lambda}
}
\]
and
\[
\boxed{
P_\lambda(-L)=
\frac{\displaystyle\prod_{s\in\lambda}
       (-\sqrt3+3x(s)-y(s))^2}{H_\lambda}.
}
\]

These formulas concern the Hall-Fock state directly; no physical-position measure is substituted.

### Exact finite counterexample

Take
\[
\lambda=(4,1,1),\qquad \kappa=(3,3).
\]
Both have
\[
D=6,\qquad a=6,\qquad b=3.
\]
They therefore have the same entire dispersion eigenvalue curve, the same initial energy \(14\sqrt3\), and the same final-energy mean \(3\sqrt3\).

Their specialization products differ:
\[
\begin{aligned}
J_{(4,1,1)}(p_k=u)
 &=u(u+3)(u+6)(u+9)(u-1)(u-2),\\
J_{(3,3)}(p_k=u)
 &=u(u+3)(u+6)(u-1)(u+2)(u+5).
\end{aligned}
\]
Their norms are
\[
H_{(4,1,1)}=18\,289\,152,\qquad
H_{(3,3)}=101\,606\,400.
\]
Substitution gives
\[
P_{(4,1,1)}(30)
=\frac{386-207\sqrt3}{28224},
\]
whereas
\[
P_{(3,3)}(30)
=\frac{3146+1815\sqrt3}{470400}.
\]
These are unequal.

Thus a closure initialized only by the known dispersion eigenvalue curve—or by its derivatives—cannot produce the full law. This counterexample does **not** rule out a recurrence using additional, efficiently computable information from the full partition.

### Cost of the surviving endpoint computation

The two endpoint weights are genuinely polynomial-time computable from explicit \(\lambda\):

* Box coordinates, arms, and legs can be constructed in polynomial time, with \(O(D)\) boxes processed.
* There are \(O(D)\) product factors.
* Exact arithmetic remains in \(\mathbb Q(\sqrt3)\).
* Numerators and denominators have \(O(D\log D)\) bits: every integer factor is \(O(D)\).
* Additive error \(\delta\) can be obtained with polynomial bit cost using \(O(D\log D+\log(1/\delta))\) working precision.
* An energy label needs \(O(\log D)\) output bits.

This pays input access, normalization, arithmetic, and precision for these **two weights only**. It supplies no sampler for the residual probability mass.

## 3. Small support does not make approximate-moment inversion safe

The known energy grid does yield a computable polynomial-order annihilator. Its coefficients are not the main outstanding cost; the initial moments remain unevaluated.

Nor can their required accuracy be dismissed merely because there are polynomially many bins. The following is a conditioning control on the **actual final spectrum**.

Let \(n=D-1\). The hook shapes
\[
\nu_j=(j+1,1^{D-j-1}),\qquad 0\le j\le n,
\]
have energies
\[
e_j=2Dj-D(D-1).
\]
For the normalized spectral variable
\[
X=\frac{S+L}{2L},
\]
these eigenvalues become \(x_j=j/n\).

Consider the two probability measures on these legal energies
\[
Q_{\mathrm{even}}(j)=
\begin{cases}
2^{1-n}\binom nj,&j\text{ even},\\
0,&j\text{ odd},
\end{cases}
\]
and the complementary odd-parity measure \(Q_{\mathrm{odd}}\). Their TV distance is \(1\).

Yet their normalized power moments satisfy, for every \(k\ge1\),
\[
\begin{aligned}
\left|\mathbb E_{\mathrm{even}}X^k
-\mathbb E_{\mathrm{odd}}X^k\right|
&=2^{1-n}
 \left|\sum_{j=0}^n(-1)^j\binom nj(j/n)^k\right|\\
&=2^{1-n}\frac{n!\,{k\brace n}}{n^k}\\
&\le 2^{1-n}.
\end{aligned}
\]
Here \(n!{k\brace n}\) counts surjections from a \(k\)-element set onto an \(n\)-element set, so it is at most \(n^k\). The moment differences vanish exactly for \(k<n\).

**Scope:** these two measures are not asserted to be Jack-quench laws. They show that the actual spectrum and its small number of bins, by themselves, provide no inverse-polynomial-accuracy moment-to-TV guarantee.

This does not defeat an exact or sufficiently accurate deterministic moment algorithm: exponentially small numerical error can require only polynomially many **bits**. It does defeat the shortcut of combining ordinary inverse-polynomial-accuracy Monte Carlo moments with an allegedly well-conditioned reconstruction. A special conditioning theorem for the Jack laws would need its own proof.

## Conclusion

The surviving, fully charged classical computations are:

* the mean final energy;
* the two extreme-bin probabilities;
* the already-supplied special-input samplers.

They do not supply computable Lanczos coefficients, the missing initial moments, or an efficiently evaluable Loschmidt function for arbitrary \(\lambda\). I therefore **cannot mark the requested polynomial classical construction as complete**.

These failed closures establish neither hardness nor a quantum advantage. The unrestricted coarse-work sampling question remains unresolved here; I am not replacing it with another oracle assumption or recommending another nearby barrier pass.