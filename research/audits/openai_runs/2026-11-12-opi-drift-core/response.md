## Counterexamples to broader readings

These do **not** refute the note with its explicit fixed-margin assumptions, but they delimit the claim.

1. **\(\eta=\Theta(1)\) alone is insufficient.** Fix admissible parameters with \(G_{\max}=1\), put a maximizer in \(S\), and take
   \[
   \eta_B=1-2^{-B}.
   \]
   Then \(b_*\) is unchanged while
   \[
   M=\left\lceil\frac{B\log 2}{L}\right\rceil.
   \]
   Thus no bound uniform in all such \(\eta\) follows. The note’s stronger requirement \(1-\eta=\Omega(1)\) is essential. The increased precision and degree are, of course, paid costs.

2. **A raw-variance interpretation of the paper’s \(L_2(G)\) would break the lazy claim.** For example, let every halfset contain \(0\), so the native score has \(G_{\max}=1,\mu=3/4\). Under laziness, take \(L=sr/4\), \(\omega=s\omega_0\), and—incorrectly—\(L_2(G)=sQ_0\), where \(Q_0\) is the maximum raw second moment. With fixed suitable \(\rho,\eta\), (119) gives \(b_*\to b_0>0\), whereas \(M=\Theta(1/s)\).  
   Equations (65)–(66) instead require the **RMS convention**
   \[
   L_2(G)^2\ge \max_x\sum_yP(x,y)(G(x)-G(y))^2.
   \]
   That convention resolves the problem; the excerpt’s terminology “quadratic variation” is imprecise.

3. **The Prange binomial law is not a fixed-input law.** With \(q=4,k=1\) and all three halfsets equal to \(\{0,1\}\), every accepted constant completion scores \(3\), not \(1+\operatorname{Bin}(2,1/2)\). The claimed law is valid over the random-table ensemble, conditioning only on the selected rows and choices.

**Verdict:** Under the note’s fixed-\(R\), fixed-spread, fixed-\(1-\eta\) assumptions and the RMS convention forced by the excerpt, the \(b_*M=O(\log(D)^{-2})\) calculation is correct, uniformly over arbitrarily small \(s>0\). For the native slope, the spread assumption can actually be proved for **every halfset input**, not merely with high probability.

---

## 1. Native update and coherent address erasure

Assume \(1\le k\le m\); fixed \(0<R<1\) gives \(k\ge2\) eventually. Write
\[
N=\binom{m}{k-1},\qquad h=1-\frac1q.
\]
For a nonzero transition,
\[
y-x=zD_A,\qquad z\ne0,
\]
the difference has degree exactly \(k-1\), leading coefficient \(z\), and precisely the roots \(A\) among the supplied evaluation points. Hence the nonzero address \((A,z)\) is unique and recoverable by a reversible scan of those points.

The diagonal is different:
\[
P_0(x,x)=\frac1q,\qquad
P_s(x,x)=1-sh.
\]
The correct coherent construction must pool **both** the lazy identity and the active \(z=0\) event into one diagonal branch:
\[
\sqrt{1-sh}\,|\mathrm{diag}\rangle+
\sqrt{sh}\,\frac1{\sqrt{N(q-1)}}\sum_{A,z\ne0}|A,z\rangle.
\]
After computing \(y\), recover and XOR away \(A,z\) from \(y-x\), and erase the branch flag using \(y\ne x\).

Thus the address-erasure argument works. Keeping distinct lazy/active-zero labels and merely “erasing” them would not: several orthogonal coin states would have the same output.

Symmetry follows from averaging translations; a fixed \(k\)-row information set supplies \(k\) independent Lagrange directions, proving irreducibility. Uniform stationarity follows. These are mathematical oracle constructions, not yet an exact finite-gate implementation: uniform subset preparation and the generally non-dyadic branch amplitudes need an explicit precision budget.

## 2. Exact drift and conditional lazy variance

To avoid overloading the polynomial variable, write
\[
G=a+\beta H,\qquad \beta>0,\qquad
\mu=a+\beta m/2,\qquad
r=\frac{m-k+1}{m}.
\]

For every fixed table, polynomial \(x\), and row \(i\),
\[
(P_0 1_{F_i})(x)
 =\frac{k-1}{m}1_{F_i}(x(a_i))+\frac r2.
\]
Indeed, an anchored coordinate stays fixed; otherwise uniform \(z\in\mathbb F_q\), **including zero**, makes the updated evaluation uniform. Therefore
\[
P_sG=(1-sr)G+sr\mu. \tag{1}
\]
No independence assumption on the halfsets is used.

Let
\[
g=\max G,\qquad \Delta=g-\mu\ge\gamma>0.
\]
Because \(G>0\), the smallest pseudo-Lipschitz constant is exactly
\[
L_{\min}=sr\,\frac{\Delta}{g}.
\]
Consequently every admissible \(L\) satisfies
\[
L\ge sr\gamma, \tag{2}
\]
using \(g\le1\).

Define the raw second moment \(Q_s(x)\). At a maximizer \(x_*\),
\[
\begin{aligned}
Q_s(x_*)
 &=s\,\mathbb E_{P_0(x_*,\cdot)}
       (G(x_*)-G(Y))^2\\
 &\ge s\bigl(G(x_*)-P_0G(x_*)\bigr)^2\\
 &=sr^2\Delta^2.
\end{aligned}
\]
Thus, putting **\(V:=L_2(G)^2\)**,
\[
V\ge sr^2\gamma^2. \tag{3}
\]
The note correctly applies Jensen after conditioning on the active \(P_0\) step. Jensen over the entire lazy transition gives only the weaker \(s^2r^2\Delta^2\).

A stationary-average variation bound cannot replace this worst-case bound.

## 3. Log-Sobolev pointmass test

Here the discriminant is \(D(P_s)=P_s\), since the chain is symmetric and uniform-stationary. With natural-log entropy, a computational basis state has
\[
\operatorname{Ent}_\pi(r_\psi)=\log D=\Lambda=k\log q.
\]
Condition (69), in its actual expectation convention, therefore gives
\[
1-sh\le1-\omega\Lambda,
\qquad
\boxed{\omega\le \frac{sh}{\Lambda}}. \tag{4}
\]
There is no extra Dirichlet-form factor of two in this calculation.

Indeed, the optimal constant scales exactly linearly with \(s\), because
\[
1-\langle\psi,P_s\psi\rangle
=s\bigl(1-\langle\psi,P_0\psi\rangle\bigr).
\]
Equation (4) is an **upper bound on every valid constant**, not a usable positive certificate for applying the theorem.

## 4. Exact source prescription and rounding

Set
\[
A_0=1-\rho-L,\qquad d=A_0-\mu>0.
\]
With the RMS convention, the supplied (119) is
\[
b_*=\min\left\{1,
 \frac{\sqrt{1+8\omega^2A_0d/V}-1}{A_0}\right\}.
\]
Rationalizing, or using \(\sqrt{1+u}-1\le u/2\), gives
\[
b_*\le\frac{4\omega^2d}{V}
 \le\frac{4s h^2}{\Lambda^2r^2\gamma^2}, \tag{5}
\]
where \(0<d<1\).

For the note’s ceiling convention in (118), put
\[
C_\eta=\log\frac1{1-\eta}.
\]
Then
\[
M=\max_{x\in S}\left\lceil
  \frac{\log(G(x)/(1-\eta))}{L}\right\rceil
 \le\frac{C_\eta}{L}+1
 \le\frac{C_\eta}{sr\gamma}+1. \tag{6}
\]
The extracted excerpt does not visibly retain the rounding delimiters. A floor interpretation also satisfies this upper bound; rounding upward costs at most one degree.

Combining (5)–(6),
\[
\boxed{
b_*M\le
\frac{4h^2}{\Lambda^2}
\left(
 \frac{C_\eta}{r^3\gamma^3}
 +\frac{s}{r^2\gamma^2}
\right).
} \tag{7}
\]
This proves the claimed uniformity in \(s\). No lower bound on \(s\), and no tightness assumption on \(L,V,\omega\), was used.

Downward rational rounding \(0\le b\le b_*\) preserves (7). Fixed-absolute-precision upward rounding does not uniformly preserve it: an error \(\varepsilon\) can contribute \(\varepsilon M=\Theta(\varepsilon/s)\). Preserving the paper’s success guarantee after rounding is a separate robustness obligation; preserving this upper bound alone is immediate.

## 5. Prange law—and a stronger deterministic spread certificate

Fix the \(k\) interpolation rows independently of the other tables. Conditional on their tables and accepted-value choices, the resulting polynomial is fixed, while the other tables remain independent uniform halfsets. Hence exactly
\[
H(x)=k+\operatorname{Bin}(m-k,1/2),
\]
and Hoeffding gives
\[
\Pr\!\left[H(x)<m/2+k/4\right]
 \le \exp\!\left[-\frac{k^2}{8(m-k)}\right].
\]
Uniform accepted-value choices are not necessary for this law; dependence only on the selected rows suffices. Adaptive selection using untouched tables, or conditioning on the full input, invalidates this argument.

For \(\beta=1/(2m)\), a verified completion above that threshold certifies
\[
\Delta\ge k/(8m).
\]

**Stronger repair: randomness is unnecessary for the spread bound.** Choose \(k-1\) rows, choose accepted values on them, and interpolate a polynomial \(x_0\) satisfying those anchors. On the line
\[
x_z=x_0+zD_A,\qquad z\in\mathbb F_q,
\]
all anchors remain accepted and every other evaluation runs through the whole field. Therefore, for every halfset input,
\[
\frac1q\sum_z H(x_z)
 =k-1+\frac{m-k+1}{2}
 =\frac{m+k-1}{2}.
\]
Thus
\[
H_{\max}-m/2\ge (k-1)/2,
\qquad
\Delta\ge\frac{k-1}{4m}
\]
for the native slope, including any intercept shift preserving that slope. This is \(\Omega(1)\) at fixed positive rate. Enumerating the \(q\) line members yields a paid, polynomial-native-input certificate; it does not require a maximizing oracle or authorize an uncharged conditioned quantum start.

## 6. Costs, remaining obligations, and scope

- **Explicit input and output:** membership-table encoding uses \(mq\) bits; accepted-value lists use \(\Theta(mq\log q)\) bits. Prange must scan/preprocess selected rows or pay actual indexed accesses. Verification evaluates **all \(m\) rows**. Output costs \(k\log_2q\) bits.
- **Coherent access:** no free QRAM is supplied. A conservative reversible score circuit can use \(O((mk+mq)\operatorname{poly}(\log q))\) work per evaluation via field arithmetic and explicit table multiplexing. The mixer additionally pays subset preparation and root-address recovery. The uniform coefficient state itself costs \(k\log_2q\) Hadamards.
- **Precision and powers:** charge rational parameter descriptions, rotation synthesis, accumulated oracle error, and heralding/amplification precision. Tiny \(s\) does not provide free iterations; the source implementation explicitly requires a paid polynomial \(M_{\max}\).
- **Source admission remains conditional:** a certified positive \(\omega\), valid worst-case regularity bounds, all target-set hypotheses, and any standing max-normalization requirement remain necessary. Unknown \(H_{\max}\) and normalization trials are not free. Equation (343) uses paid bounds in
  \[
  E_b^{\rm ub}=1+b\mu_{\rm ub}+\frac{b^2V_{\rm ub}}{8\omega^2},
  \]
  not an automatically available top eigenvalue.

The sharp falsifiers are (2)–(4): violating any of them invalidates a claimed native admission.

**Scope:** this is a proved constraint on the prescribed mixer, affine score and source parameter family. It establishes neither OPI hardness nor a no-go for other tilted walks, larger tilts, longer powers, or separately prepared nonstationary starts. The product bound itself is a parameter fact; conclusions about stationary-start filtering must not be transferred to other starts without a separate paid analysis.