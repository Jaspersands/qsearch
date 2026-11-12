## Verdict

**The binomial-LCU principal-half-phase compiler works under the stated spectral promise.** In particular, its clean-isometry error is linear in the binomial cutoff defect—not merely the square root of a projected-block error.

Below is a finite-circuit proof, including a phase-sensitive native-\(W\) interface, explicit precision budgets, and charged composition costs. No QSVT phase-sequence oracle is used.

The conclusion is specifically about this half-phase compiler. A polynomial-precision-cost implementation of native \(W\) remains an independent input to the end-to-end resource bound; substituting the old first-order simulator would not establish the full proposed upgrade.

---

# 1. Statement and native-circuit interface

Let \(N=D+1\), and let \(W\) be a unitary on a finite padded system space \(\mathcal H\). Let \(\mathcal S\) be a reducing spectral subspace on which every eigenphase, represented in \((-\pi,\pi)\), satisfies
\[
|\phi|\le \pi-g_0,\qquad g_0=\frac1{2N}.
\]
On this subspace define
\[
f(W)|\omega_\phi\rangle=e^{i\phi/2}|\omega_\phi\rangle.
\]

For any \(0<\eta<1\), the construction below gives a finite unitary circuit \(\widetilde F\) such that
\[
\left\|
\left(\widetilde FJ-Jf(W)\right)P_{\mathcal S}
\right\|<\eta,                                      \tag{1}
\]
where \(J\) appends **all** signal and work registers in their prescribed zero states. Thus (1) includes workspace cleanup and is uniform on superpositions and reference-entangled inputs.

### Required native-\(W\) contract

The supplied controlled-\(W\) circuit must have a **phase-sensitive** norm guarantee.

If native implementation uses private workspace \(Z\), an adequate formulation is:

* There is a specified ideal global unitary \(\mathcal W\) satisfying
  \[
  \mathcal W(|\psi\rangle|0_Z\rangle)
     =W|\psi\rangle|0_Z\rangle
  \]
  for every logical system state.
* The supplied controlled circuit satisfies
  \[
  \|\widetilde{\mathrm C\mathcal W}
       -\mathrm C\mathcal W\|\le \rho.               \tag{2}
  \]
* Inverse calls use the **actual circuit inverse**.

This does **not** require \(\mathcal W=W\otimes I_Z\) on nonzero workspace. It compares two specified global circuits, while identifying their clean logical action.

Unitarity implies that \(\mathcal W^\dagger\) preserves the clean native-workspace subspace and implements \(W^\dagger\) there. Also,
\[
\|\widetilde{\mathrm C\mathcal W}^{\,\dagger}
       -(\mathrm C\mathcal W)^\dagger\|
=\|\widetilde{\mathrm C\mathcal W}
       -\mathrm C\mathcal W\|
\le\rho.                                            \tag{3}
\]

All native workspace is retained. Its gate, bit-generation, and qubit costs are charged below.

---

# 2. The polynomial and its cutoff error

Set
\[
H=\frac{2I+W+W^\dagger}{4},
\qquad
R=I-H=\frac{2I-W-W^\dagger}{4},
\qquad
T=\frac{I+W}{2}.
\]
For a \(W\)-eigenvector with eigenvalue \(e^{i\phi}\),
\[
H\longmapsto x=\cos^2(\phi/2),\qquad
R\longmapsto 1-x.
\]
Consequently \(0\le H,R\le I\) globally.

## 2.1 The gap implies the proposed lower bound

On the promised phase support,
\[
x\ge \sin^2(g_0/2)=\sin^2\!\left(\frac1{4N}\right).
\]
For \(0\le u\le 1/4\),
\[
\sin u\ge u-\frac{u^3}{6}\ge \frac u2.
\]
For example, the first inequality follows by integrating
\(1-\cos u\le u^2/2\). Hence
\[
x\ge \frac1{64N^2}=:a.                              \tag{4}
\]

## 2.2 Binomial identity

Define
\[
b_k=\frac{\binom{2k}{k}}{4^k}.
\]
Then \(b_0=1\), \(0<b_k\le1\), and
\[
b_{k+1}=\frac{2k+1}{2k+2}b_k.
\]
For \(0\le z<1\), the series \(B(z)=\sum_{k\ge0}b_kz^k\) and its derivative converge locally uniformly. The recurrence gives
\[
(1-z)B'(z)=\frac12B(z).
\]
Therefore \(\sqrt{1-z}\,B(z)\) has derivative zero and value one at zero:
\[
\sum_{k=0}^\infty b_kz^k=(1-z)^{-1/2}.              \tag{5}
\]

Put
\[
q_K(x)=\sum_{k=0}^K b_k(1-x)^k,\qquad
t_K(x)=\sqrt{x}\,q_K(x).
\]
For \(0<x\le1\), positivity and (5) imply
\[
0<t_K(x)\le1.
\]
Moreover,
\[
\begin{aligned}
1-t_K(x)
&=\sqrt{x}\sum_{k=K+1}^\infty b_k(1-x)^k\\
&\le \frac{(1-x)^{K+1}}{\sqrt{x}}\\
&\le \frac{e^{-x(K+1)}}{\sqrt{x}}.
\end{aligned}
\]
Thus for \(x\ge a\),
\[
1-t_K(x)\le \frac{e^{-a(K+1)}}a.                    \tag{6}
\]

The proposed
\[
K=\left\lceil a^{-1}\log\frac1{a\delta}\right\rceil
\]
therefore suffices for \(1-t_K\le\delta\).

For an entirely integer-computable cutoff without evaluating a logarithm near an integer boundary, one may instead use
\[
p=\left\lceil\log_2\frac1{a\delta}\right\rceil,
\qquad
K=64N^2p.                                          \tag{7}
\]
The value \(p\) is found by exact comparisons of integers. Since
\(\log u\le\log_2u\) for \(u\ge1\), (7) also satisfies (6). This is merely conservative cutoff rounding, not a change to the construction.

## 2.3 Correct branch and phase

Define
\[
P_K(W)=Tq_K(H).
\]
For \(-\pi<\phi<\pi\),
\[
\frac{1+e^{i\phi}}2
=e^{i\phi/2}\cos(\phi/2),
\]
and the cosine is positive. Hence
\[
P_K(W)|\omega_\phi\rangle
=e^{i\phi/2}t_K(x)|\omega_\phi\rangle.               \tag{8}
\]

Thus the polar phase of this polynomial is exactly the principal half phase. There is no undetermined sign. At \(W=-1\), \(T=0\) and therefore \(P_K=0\).

---

# 3. An explicit global unitary dilation

Every circuit in this section is defined on all padded registers. Correctness of its selected block does not substitute for existence of a global unitary: the global unitary is explicitly the following product of gates.

## 3.1 One \(R\) block encoding

Use a two-qubit label prepared uniformly by \(H\otimes H\). Define
\[
\mathrm{SELECT}_R
=\operatorname{diag}(I,I,-W,-W^\dagger).
\]
Then
\[
B_R=(H\otimes H\otimes I)\,
       \mathrm{SELECT}_R\,
       (H\otimes H\otimes I)
\]
is unitary and
\[
(\langle00|\otimes I)B_R(|00\rangle\otimes I)
=\frac{I+I-W-W^\dagger}{4}=R.                       \tag{9}
\]

The minus signs are implemented as known conditional phases. A selector uses one controlled-\(W\) call and one controlled-\(W^\dagger\) call.

## 3.2 Why fresh signals give powers

Give the \(j\)-th \(B_R\) a fresh two-qubit signal register \(A_j\). Then
\[
\langle0_{A_1}\cdots0_{A_k}|
 B_{R,k}\cdots B_{R,1}
|0_{A_1}\cdots0_{A_k}\rangle
=R^k.                                               \tag{10}
\]
Indeed, later gadgets never touch earlier signal registers. Contracting those registers successively therefore multiplies their system matrix elements in order.

This argument would generally fail if the same signal register were reused. The fresh-register requirement is substantive.

## 3.3 Coherent selection of \(k\), without word enumeration

Let
\[
s=\sum_{k=0}^K b_k.
\]
Prepare
\[
Q|0\rangle=\sum_{k=0}^K\sqrt{\frac{b_k}{s}}\,|k\rangle. \tag{11}
\]
Here “weights \(b_k/s\)” means probabilities, not unnormalized amplitudes.

For \(j=1,\ldots,K\), apply \(B_{R,j}\) if \(k\ge j\). The threshold is computed reversibly from the binary \(k\) register; no enumeration of \(4^k\) selector words occurs. Define
\[
V_q=(Q^\dagger\otimes I)
       \left(\prod_{j=1}^K \mathrm C_{k\ge j}B_{R,j}\right)
       (Q\otimes I).
\]
Its all-zero signal block is
\[
\sum_{k=0}^K\frac{b_k}{s}R^k=\frac{q_K(H)}s.          \tag{12}
\]

Unused padded \(k\)-labels can use the same threshold rule. The resulting circuit is still a global unitary.

## 3.4 Append the \(T\) block

On another fresh qubit use
\[
B_T=(H\otimes I)\operatorname{diag}(I,W)(H\otimes I),
\]
whose zero block is \(T=(I+W)/2\).

Appending \(B_T\) to \(V_q\) gives a unitary \(V\) with
\[
\langle0|V|0\rangle=\frac{P_K(W)}s.                  \tag{13}
\]
It uses exactly
\[
2K+1
\]
controlled native-\(W\) or native-\(W^\dagger\) calls.

The logical signal count so far is
\[
2K+\left\lceil\log_2(K+1)\right\rceil+1.
\]
Comparator work is computed and uncomputed. All work remains part of the global circuit.

---

# 4. Known-normalization dilution

Choose exactly as proposed:
\[
m=4(K+1),\qquad
\theta_*=\frac{\pi}{4m+2},\qquad
\alpha=\sin\theta_*,
\qquad
d=s\alpha.
\]
Since \(s\le K+1\),
\[
0<d\le (K+1)\theta_*
=\frac{\pi(K+1)}{16(K+1)+2}
<\frac{\pi}{16}<1.                                 \tag{14}
\]
Thus \(d\) is a legitimate clean amplitude.

On a fresh qubit define the real unitary
\[
D_d=
\begin{pmatrix}
d&-\sqrt{1-d^2}\\
\sqrt{1-d^2}&d
\end{pmatrix}.
\]
Let \(U=D_d\otimes V\), with the obvious register ordering. Its all-zero signal block is
\[
A:=\langle0|U|0\rangle
=\frac dsP_K(W)
=\alpha P_K(W).                                    \tag{15}
\]

This is the entire normalization argument. Both \(s\) and \(d\) depend only on the chosen cutoff. No eigenvalue, \(\lambda\), \(\tau\), or unknown overlap enters the dilution or iteration count.

The ideal definition uses exact real rotations. Section 7 pays their finite implementation error.

---

# 5. The exact \(m\)-step oblivious-amplification identity

Let
\[
\Pi=|0_{\rm sig}\rangle\langle0_{\rm sig}|\otimes I,
\qquad
S=I-2\Pi.
\]
This reflection tests only known zero signal registers.

Define
\[
G=-USU^\dagger S,
\qquad
F=G^mU.                                            \tag{16}
\]
The leading minus sign is part of the definition. It is a known phase and must not be silently dropped in a controlled implementation.

We now prove the identity, including its phase.

Take a normalized \(W\)-eigenvector \(|\omega\rangle\) with phase \(\phi\ne\pi\), and abbreviate
\[
f=e^{i\phi/2},\quad t=t_K(x),\quad
a_\omega=\alpha t,\quad
\theta_\omega=\arcsin a_\omega.
\]
Let
\[
|e\rangle=|0_{\rm sig}\rangle|\omega\rangle,
\qquad
|g\rangle=f|e\rangle,
\qquad
|y\rangle=U|e\rangle.
\]
Equation (15) gives
\[
\Pi|y\rangle=a_\omega|g\rangle,
\qquad
\Pi U^\dagger|g\rangle=a_\omega|e\rangle.             \tag{17}
\]
Because \(a_\omega\le\alpha<1\), define
\[
b_\omega=\sqrt{1-a_\omega^2},\qquad
|h\rangle=\frac{|y\rangle-a_\omega|g\rangle}{b_\omega}.
\]
Then
\[
\Pi|h\rangle=0,\qquad
|y\rangle=a_\omega|g\rangle+b_\omega|h\rangle.
\]

Put \(Q_U=U\Pi U^\dagger\). From (17),
\[
Q_U|g\rangle=a_\omega|y\rangle.
\]
Since \(Q_U|y\rangle=|y\rangle\), it also follows that
\[
Q_U|h\rangle=b_\omega|y\rangle.
\]
Thus, in the ordered orthonormal basis \((g,h)\),
\[
\Pi=
\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
Q_U=
\begin{pmatrix}
a_\omega^2&a_\omega b_\omega\\
a_\omega b_\omega&b_\omega^2
\end{pmatrix}.
\]
Consequently
\[
G=-(I-2Q_U)(I-2\Pi)
=
\begin{pmatrix}
\cos(2\theta_\omega)&\sin(2\theta_\omega)\\
-\sin(2\theta_\omega)&\cos(2\theta_\omega)
\end{pmatrix}.                                    \tag{18}
\]
Applying this rotation \(m\) times to
\((\sin\theta_\omega,\cos\theta_\omega)^T\) proves
\[
F|e\rangle
=
\sin((2m+1)\theta_\omega)|g\rangle
+
\cos((2m+1)\theta_\omega)|h\rangle.                 \tag{19}
\]

In particular, the clean amplitude is exactly
\[
f(\phi)\,
\sin\!\left((2m+1)\arcsin(\alpha t_K(x))\right).      \tag{20}
\]

This is singular-vector amplification in the signal space, proved directly from two projectors. It assumes no phase-sequence oracle and no reflection about an unknown state.

## 5.1 Calibration and clean-isometry error

Write \(n=2m+1\). By construction,
\[
n\theta_*=\frac{\pi}{2}.
\]
For \(0\le t\le1\), set
\[
\Delta=\frac{\pi}{2}-n\arcsin(\alpha t)\ge0.
\]
The derivative bound for \(\arcsin\) gives
\[
\begin{aligned}
\Delta
&\le n\frac{\alpha(1-t)}{\sqrt{1-\alpha^2}}\\
&\le \frac{\pi}{2\cos\theta_*}(1-t).
\end{aligned}
\]
Here \(m\ge4\), so \(\theta_*\le\pi/18\), and
\[
\frac{\pi}{2\cos(\pi/18)}<2.
\]
Therefore
\[
\Delta\le2(1-t).                                    \tag{21}
\]

Equation (19) now reads
\[
F|e\rangle=\cos\Delta\,|g\rangle+\sin\Delta\,|h\rangle.
\]
Its distance from the **clean target vector** is
\[
\begin{aligned}
\|F|e\rangle-|g\rangle\|
&=\sqrt{(\cos\Delta-1)^2+\sin^2\Delta}\\
&=2\sin(\Delta/2)\\
&\le\Delta.
\end{aligned}
\]
Thus, on the promise,
\[
\|F|e\rangle-f|e\rangle\|\le2\delta.                \tag{22}
\]

This is the required clean error. The projected amplitude defect is actually
\[
1-\cos\Delta\le\Delta^2/2,
\]
but the proof does not mistake that smaller quantity for the full isometry error.

## 5.2 Why the bound is uniform

For an orthonormal eigenbasis \(\{\omega_j\}\), the corresponding \(g_j\) and \(y_j=Ue_j\) satisfy
\[
\langle g_i,y_j\rangle=a_j\delta_{ij}.
\]
It follows directly from their definitions that the corresponding \(h_j\) are orthonormal and orthogonal to every \(g_i\). Hence the two-dimensional amplification planes are mutually orthogonal.

Therefore the error on their direct sum is a **maximum** of the scalar errors, not a sum:
\[
\|(FJ-Jf(W))P_{\mathcal S}\|\le2\delta.              \tag{23}
\]
The same argument covers degeneracies and controlled direct sums over content labels. Tensoring the error operator with a reference identity leaves its operator norm unchanged.

---

# 6. Relative phase and the distinction from a full-space claim

## 6.1 Positive Jack polar phase

Using the two-projector structure supplied in the review, let
\[
v=\cos\vartheta\,u+\sin\vartheta\,u_\perp,
\qquad
\cos\vartheta=\sqrt{\tau}>0.
\]
On this plane,
\[
W=(2P_0-I)(2P_c-I)
=
\begin{pmatrix}
\cos(2\vartheta)&\sin(2\vartheta)\\
-\sin(2\vartheta)&\cos(2\vartheta)
\end{pmatrix}.
\]
Since \(0\le\vartheta<\pi/2\), its principal square root is
\[
f(W)=
\begin{pmatrix}
\cos\vartheta&\sin\vartheta\\
-\sin\vartheta&\cos\vartheta
\end{pmatrix},
\]
and therefore
\[
f(W)v=u
\]
with coefficient \(+1\).

Equations (8) and (20) preserve precisely this phase. Moreover,
\[
0\le n\arcsin(\alpha t)\le\pi/2,
\]
so the amplified scalar multiplying \(f\) never introduces an additional sign.

The assumption here is the supplied positive-overlap identification of \(u,v\) and the stated gap. The half-phase compiler itself requires no access to those vectors or their overlaps.

## 6.2 What happens at the cut

For the one-dimensional example \(W=-1\),
\[
H=0,\qquad P_K=0,\qquad a_\omega=0.
\]
The amplified clean amplitude remains zero. The output has unit norm entirely in the nonclean signal sector.

This is **not** a counterexample to the promised construction. It is the cheapest counterexample to the stronger, unclaimed assertion that this circuit is clean and approximates a square root on every logical input.

Both the ideal circuit \(F\) and the finite circuit \(\widetilde F\) are nevertheless global unitaries. A unitary circuit extension outside the promise does not mean a clean implementation of the discontinuous target function there.

---

# 7. Finite-bit coefficient preparation and finite gates

## 7.1 Exact rational data have polynomial bit length

Use the common denominator \(4^K\):
\[
w_k=\binom{2k}{k}4^{K-k},
\qquad
S_K=\sum_{k=0}^K w_k.
\]
Then
\[
s=\frac{S_K}{4^K},
\qquad
\frac{b_k}{s}=\frac{w_k}{S_K}.
\]
Each \(w_k\) has at most \(2K+1\) bits, and \(S_K\) has
\[
2K+O(\log(K+1))
\]
bits. Binomial coefficients, weights, and prefix sums can all be computed exactly by polynomially many integer operations.

In particular, a denominator of numerical size \(4^K\) costs \(O(K)\) bits, not \(4^K\) work.

## 7.2 Explicit preparation circuit

Pad to
\[
L=\lceil\log_2(K+1)\rceil
\]
label qubits. A binary prefix tree has fewer than \(2(K+1)\) internal nodes.

At a node with child weights \(W_0,W_1\), use a controlled real rotation with
\[
\cos\beta=\sqrt{\frac{W_0}{W_0+W_1}},
\qquad
\sin\beta=\sqrt{\frac{W_1}{W_0+W_1}}.
\]
Applied to the next zero qubit, this gives the required positive amplitudes. Induction down the tree proves (11).

Empty nodes and exact zero/one probabilities are decided by exact integer comparisons. The circuit contains \(O(K)\) controlled rotations, not an exponentially indexed state-preparation oracle. Prefix controls use \(O(\log(K+1))\) exact reversible gates each.

## 7.3 Angles can be computed in polynomial bit time

For completeness, a rational probability \(p\in[0,1]\) can be converted to
\[
\beta\in[0,\pi/2],\qquad \sin^2\beta=p,
\]
to absolute error \(2^{-B}\) using polynomial bit work.

A robust bisection method suffices. The useful elementary inequality is, for \(0\le u<v\le\pi/2\),
\[
\begin{aligned}
\sin^2v-\sin^2u
&=\sin(v+u)\sin(v-u)\\
&\ge \sin^2(v-u)\\
&\ge \frac4{\pi^2}(v-u)^2.                         \tag{24}
\end{aligned}
\]
Bisect the normalized interval \(\beta=(\pi/2)t\), \(0\le t\le1\). Evaluate \(\sin^2((\pi/2)t)\) within
\[
\gamma=2^{-2B-20}.
\]
If the comparison with \(p\) is decisive, keep the correct half. If it is within the evaluation uncertainty, (24) already locates the angle within \(O(\sqrt\gamma)\), well below \(2^{-B}\). Otherwise \(O(B)\) bisections suffice.

The required transcendental values need no oracle:

* \(\pi\) can be computed using
  \[
  \pi=16\arctan(1/5)-4\arctan(1/239),
  \]
  verified by the tangent addition formula and the appropriate angle interval.
* The alternating arctangent series has geometrically bounded remainder at these arguments.
* On bounded arguments, the sine Taylor series reaches \(b\)-bit accuracy using \(O(b)\) terms; factorial growth gives the remainder bound.

These procedures use polynomially many rational or fixed-point operations with polynomial-length operands.

For dilution, compute \(d=s\sin\theta_*\), then the angle \(\arccos d\). A safe transcendental working accuracy is
\[
b=2B+2\lceil\log_2(K+2)\rceil+40
\]
bits, using interval arithmetic to certify the final angle error. The factor \(s\le K+1\) is covered by the extra \(\log K\) precision. Exact coefficient integers still require \(O(K)\) bits. All these costs are polynomial in \(K+B\).

## 7.4 A finite-gate synthesis route

One may use the standard constructive Solovay–Kitaev theorem for a fixed inverse-closed gate set dense in \(SU(2)\). It provides phase-sensitive operator-norm approximation with word length and classical compilation work polynomial in \(B\) for error \(2^{-B}\).

An explicit suitable fixed one-qubit generating pair is
\[
G_z=
\begin{pmatrix}
(3+4i)/5&0\\0&(3-4i)/5
\end{pmatrix},
\qquad
G_x=
\begin{pmatrix}
3/5&4i/5\\4i/5&3/5
\end{pmatrix},
\]
together with their inverses. Include exact \(H,X,Z,\mathrm{CNOT}\), and Toffoli gates for the remaining circuit.

To check density, if \(\alpha=\arg(3+4i)\), then \(\alpha/\pi\) is irrational: otherwise \(e^{i\alpha}\) would be a root of unity, making \(2\cos\alpha=6/5\) a rational algebraic integer, which is impossible. Powers of the two generators are therefore dense in their respective one-parameter \(z\)- and \(x\)-rotation groups. Euler decomposition then gives density in \(SU(2)\).

The constructive synthesis theorem is not a phase-sequence oracle. Its usual proof uses a fixed constant-resolution net and a balanced-commutator recursion: residual error \(r\) is reduced to \(O(r^{3/2})\) while word length grows by a constant factor. Thus both word length and compilation time are polynomial in \(\log(1/r)\). All required two-by-two matrix calculations have polynomial bit algorithms.

Controlled real rotations can be implemented using two single-qubit rotations and two CNOTs, since
\[
X R_y(\gamma)X=R_y(-\gamma).
\]
All synthesized rotations are compared as actual \(SU(2)\) matrices, **not modulo global phase**. Known selector minus signs and the minus sign in (16) are retained exactly.

---

# 8. Explicit noncircular error budget

Let
\[
n=2m+1=8K+9.
\]
The circuit \(F=(-USU^\dagger S)^mU\) contains \(m+1\) uses of \(U\) and \(m\) uses of \(U^\dagger\). Therefore its native query count is exactly
\[
Q_W=(8K+9)(2K+1)\le18(K+1)^2.                      \tag{25}
\]

A prefix preparation uses fewer than \(2(K+1)\) controlled rotations. Replacing each controlled rotation by at most two single-qubit variable rotations, each \(U\) or \(U^\dagger\) contains at most
\[
8(K+1)+1
\]
such rotations. Thus the conservative bound
\[
N_{\rm rot}=100(K+1)^2                              \tag{26}
\]
covers all variable single-qubit rotations in the amplified circuit.

Use the following explicit choices:
\[
\boxed{
\begin{aligned}
\delta&=\eta/8,\\
K&=64N^2
 \left\lceil\log_2\frac{64N^2}{\delta}\right\rceil,\\
\rho&=\frac{\eta}{8Q_W},\\
B&=\left\lceil\log_2\frac{32N_{\rm rot}}{\eta}\right\rceil.
\end{aligned}}                                                     \tag{27}
\]

Compute each elementary rotation angle within \(2^{-B}\), and synthesize its resulting matrix within \(2^{-B}\). Its total operator error is at most \(2^{1-B}\).

For products of unitaries, telescoping gives
\[
\left\|\prod_j\widetilde U_j-\prod_jU_j\right\|
\le\sum_j\|\widetilde U_j-U_j\|.                     \tag{28}
\]
The same bound applies to repeated, correlated errors; no independence assumption is needed.

Comparing the finite circuit with the exact circuit gives
\[
\|\widetilde F-F\|
\le Q_W\rho+2N_{\rm rot}2^{-B}
\le\frac{\eta}{8}+\frac{\eta}{16}.                  \tag{29}
\]
Together with (23),
\[
\left\|
(\widetilde FJ-Jf(W))P_{\mathcal S}
\right\|
\le \frac{\eta}{4}+\frac{\eta}{8}+\frac{\eta}{16}
=\frac{7\eta}{16}<\eta.                             \tag{30}
\]

Where ideal native implementations use private work, (29) compares the specified global circuit extensions. Equation (30) includes all their workspace.

### Why this budget is noncircular

The dependency order is
\[
(D,\eta)\longrightarrow K
\longrightarrow (m,Q_W,N_{\rm rot})
\longrightarrow(\rho,B).
\]
Neither \(K\) nor the number of outer calls depends on the cost of achieving \(\rho\).

There is also no need to prove that the approximate native \(W\) has the same eigenvectors or preserves the ideal spectral gap. The spectral argument applies to the exact reference circuit; the finite implementation is handled by (28).

---

# 9. Charged resources and composition

Let

* \(G_W(D,\rho)\) be the gate count of the supplied controlled native-\(W\) circuit;
* \(q_W(D,\rho)\) its workspace;
* \(\mathrm{BIT}_W(D,\rho)\) its charged classical generation/access cost.

Then one half-phase compiler has gate count
\[
G_{1/2}
\le
Q_WG_W(D,\rho)
+
O\!\left(
K^2\bigl[\log(K+2)+B^{c}\bigr]
\right),                                           \tag{31}
\]
for a fixed finite-synthesis exponent \(c\).

The additional signal and reversible-control workspace is \(O(K+\log(K+2))\), apart from the logical data and native workspace. Zero-register initialization is polynomial in this workspace size.

Classical coefficient generation, certified angle computation, and writing the finite gate sequence require
\[
\operatorname{poly}(K,B)
+
O\!\left(Q_W\,\mathrm{BIT}_W(D,\rho)\right)          \tag{32}
\]
charged bit work. The tables are compiled into explicit prefix-controlled gates; no QRAM or coefficient oracle is assumed.

## 9.1 Precision after \(O(D)\) stages

For example, take
\[
\eta=\frac{\epsilon}{16N},
\qquad
L=1+\left\lceil\log_2\frac{N}{\epsilon}\right\rceil.
\]
Then
\[
K=O(N^2L),\qquad Q_W=O(N^4L^2),
\]
and the explicit native accuracy is
\[
\rho=\frac{\epsilon}{128NQ_W}.                      \tag{33}
\]
Consequently
\[
\log\frac1\rho=O(L),\qquad B=O(L).                  \tag{34}
\]

Across \(O(D)\) polar uses, the native call count is
\[
O(N^5L^2).                                         \tag{35}
\]
In particular, if the independently supplied native implementation obeys
\[
G_W(D,\rho)\le C N^u(1+\log(1/\rho))^v
\]
with fixed exponents, the polar contribution after composition is bounded by
\[
O\!\left(N^{u+5}L^{v+2}+N^5L^{c+2}
         +N^5L^2\log(NL)\right),                   \tag{36}
\]
with polynomial bit-generation cost as well.

This explicitly charges native calls. An arbitrary supplied \(W\) circuit can have arbitrary length; no unconditional bound independent of that input length is possible.

## 9.2 Actual inverses and imperfect intermediate states

If full unitaries \(B,\widetilde B\) satisfy a restricted clean-input bound
\[
\|(\widetilde B-B)P_{\mathcal T}\|\le e,
\]
then on the ideal range \(B(\mathcal T)\),
\[
\begin{aligned}
\|(\widetilde B^\dagger-B^\dagger)BP_{\mathcal T}\|
&=\|\widetilde B^\dagger(B-\widetilde B)P_{\mathcal T}\|\\
&\le e.
\end{aligned}                                      \tag{37}
\]
Thus the use of the actual inverse polar/branching circuits is paid by the forward restricted bound.

Likewise, in a stage-by-stage hybrid argument, each local error is evaluated on the **ideal** intermediate state. Approximate states may have small components outside the promise; subsequent unitaries cannot increase the norm of those error components. No projection back into the promise, reset, measurement, or discard is needed.

The supplied branching composition budgets can therefore use this compiler in place of the old half-phase QPE compiler without changing their restricted-operator-norm reasoning.

---

# 10. Scope and falsifiability

### Proved here

* The stated binomial polynomial has the required principal phase and cutoff tail.
* The fresh-signal LCU is an explicit global unitary with block \(P_K/s\).
* Known-normalization dilution gives exactly \(\sin\theta_*\,P_K\).
* The stated \(m\)-step OAA identity, including its phase, holds.
* Its promised-subspace **clean-isometry** error is at most \(2\delta\).
* Rational coefficient preparation, angle computation, and finite-gate synthesis require polynomial bit work.
* Equations (27) and (33) give an explicit noncircular native-\(W\) accuracy budget.
* With independently logarithmic-precision-cost native \(W\), composition has polynomial \((D,\log(1/\epsilon))\) cost.

### Assumptions not re-proved by this obligation

* The supplied Jack spectral-gap and positive-overlap facts.
* The separate native simulation implementation and its claimed polynomial dependence on \(\log(1/\rho)\).
* The already reviewed nonpolar branching interfaces.

In particular, a reference to an absent native-measurement report is not itself verification of the second item.

### Concrete interface falsifiers

The proof would not apply if an implementation:

1. reused the same \(R\)-signal register when asserting (10);
2. prepared amplitudes \(b_k/s\) rather than probabilities \(b_k/s\);
3. discarded LCU or native-simulation workspace;
4. supplied controlled \(W\) only up to an untracked global phase;
5. replaced (30) by a projected-block-only guarantee;
6. asserted cleanliness at \(W=-1\).

These are specific algebraic or interface failures, not failed-attack evidence.

No numerical tests are needed for the acceptance above. No hardness, novelty, or classical speedup conclusion follows. The output is a coherent transform with its workspace close to zero; reading an exponentially long amplitude list is neither provided nor included in the claim.