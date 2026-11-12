## Verdict

**Conditionally, both the clean decoder and the full-transform consequence can be constructed.** The missing coherent-preparation operation is a deterministic rotation between two rank-one projector ranges. Here those rotations can be implemented using the native projectors \(\pi_0,E_c,P_A\), with **no inverse of a recursively prepared Jack state**.

This conclusion uses the expressly positive identity
\[
A_d\psi_{\lambda,s}=+J_{\lambda+s}
\tag{H+}
\]
and the stated overlap bounds as assumptions. I do not establish their all-degree validity here. The cyclic decomposition and orthogonality used below are those in the supplied primary text.

The two-corner-set reconstruction is correct. By contrast, actual measurement/discarding of histories, basis-state error bounds alone, and “state preparation therefore full transform” are invalid shortcuts.

Throughout, \(D\) is charged numerically, \(\alpha=3\), and
\[
|j_\lambda\rangle=\frac{J_\lambda}{\|J_\lambda\|},\qquad
|\phi_{\lambda,s}\rangle=\frac{\psi_{\lambda,s}}{\|\psi_{\lambda,s}\|}.
\]

---

## 1. Exact two-corner-set reconstruction

### Proposition 1

Let the distinct positive row lengths of a nonempty partition be
\[
L_1>\cdots>L_m>0,
\]
with multiplicities \(h_1,\ldots,h_m\), and put
\[
H_i=\sum_{j\le i}h_j,\qquad H_0=0,\qquad L_{m+1}=0.
\]

Its addable contents, in decreasing order, are
\[
a_i=3L_i-H_{i-1}\quad(1\le i\le m),\qquad a_{m+1}=-H_m.
\]
Its removable contents, in decreasing order, are
\[
r_i=3L_i-H_i-2.
\]
Consequently, with \(b_i=r_i+2\),
\[
a_i>b_i>a_{i+1},
\]
and
\[
h_i=a_i-b_i,\qquad
w_i:=L_i-L_{i+1}=\frac{b_i-a_{i+1}}3.
\]
Thus
\[
L_i=\sum_{j\ge i}w_j,
\]
repeated \(h_i\) times, reconstructs the partition uniquely.

### Proof

The addable corner associated with the \(i\)-th row block is
\((L_i,H_{i-1})\). Its removable corner is
\((L_i-1,H_i-1)\). Applying \(c(x,y)=3x-y\) gives the displayed formulas. Their differences give \(h_i\) and \(3w_i\), both positive. This also proves that sorting the two sets produces the required pairing. ∎

For the empty partition the sets are \(\{0\}\) and \(\varnothing\).

**Validation detail.** For sampled, potentially incomplete sets, positivity, divisibility by \(3\), and total size \(D\) are not by themselves complete validation: simultaneously translating both content sets leaves all these differences unchanged. The decoder should regenerate the candidate’s corner sets and compare them with the observed sets. This is polynomial-time reversible arithmetic. Completeness is still a probabilistic event, not something the decoder may assume.

---

## 2. The native invariant spaces, including degeneracy

Write
\[
\mathcal H_d=(F[w])_d,\qquad
V_d=\frac{A_d^\dagger}{\sqrt{3(d+1)}},\qquad
P_A=V_dV_d^\dagger,
\]
and let \(E_c^{(d)}\) denote the **entire**, possibly degenerate, content-\(c\) spectral projector of \(L_d\).

The weighted adjoint calculation gives
\[
A_dA_d^\dagger
 =\sum_{k\ge1}3kV_k\partial_{V_k}
 =3(d+1)I
\]
on \(F_{d+1}\). Hence \(V_d\) is an isometry.

### Proposition 2: the two required rank-one pairs

Under (H+):

1. On \(Z_\lambda\),
   \[
   \pi_0=|j_\lambda\rangle\langle j_\lambda|,
   \qquad
   E_{c(s)}^{(d)}
   =|\phi_{\lambda,s}\rangle\langle\phi_{\lambda,s}|.
   \]
   Their positive overlap is
   \[
   \langle\phi_{\lambda,s}|j_\lambda\rangle
   =\sqrt{\tau_{\lambda,s}}.
   \]

2. For \(\mu\vdash d+1\), define
   \[
   S_\mu=\operatorname{span}
   \{\,\phi_{\mu-r,r}:r\in R_\mu\,\}.
   \]
   The \(S_\mu\) form an orthogonal decomposition of \(\mathcal H_d\). On \(S_\mu\),
   \[
   P_A=|V_dj_\mu\rangle\langle V_dj_\mu|,
   \]
   and \(E_{c(r)}^{(d)}\) has rank one. Moreover,
   \[
   \langle V_dj_\mu|\phi_{\mu-r,r}\rangle
   =\frac{\|J_\mu\|}
          {\sqrt{3(d+1)}\,\|\psi_{\mu-r,r}\|}
   =\sqrt{q_{\mu,r}}>0.
   \tag{1}
   \]

### Proof

The first assertion follows from the supplied cyclic-space theorem, its projection normalization, and orthogonality.

For the second, the \(\psi_{\lambda,s}\) constitute an orthogonal basis. Group that basis by \(\mu=\lambda+s\). Equation (H+) and orthogonality of the \(J_\mu\) imply
\[
A_d^\dagger J_\mu\in S_\mu,
\]
and \(A_d\) maps every basis vector of \(S_\mu\) into \(\mathbb C J_\mu\). Therefore \(P_A|_{S_\mu}\) is the rank-one projector onto \(V_dj_\mu\). Equation (1) follows directly from the positive identity.

Removable contents within one partition are distinct by Proposition 1, so the restriction of \(E_{c(r)}\) to \(S_\mu\) has rank one. ∎

**Global content degeneracy is therefore harmless here.** Neither construction resolves a degenerate eigenspace into an unspecified eigenbasis. It uses the global \(E_c\), which preserves every relevant \(Z_\lambda\) and \(S_\mu\).

### Computing \(q\) without Jack coefficients or norms

The proposed residue formula also follows conditionally. The native block identity is
\[
L_n=
\begin{pmatrix}
0&A_{n-1}\\
A_{n-1}^\dagger&L_{n-1}+2I
\end{pmatrix}.
\]
Under (H+), \(\mathbb Cj_\mu\oplus wS_\mu=Z_\mu\). Its scalar Schur complement gives
\[
\frac1{m_\mu(u)}
 =u-3n\sum_{r\in R_\mu}
       \frac{q_{\mu,r}}{u-(c(r)+2)}.
\]
Thus, at \(b_r=c(r)+2\),
\[
q_{\mu,r}
 =\frac{-\operatorname{Res}_{u=b_r}1/m_\mu(u)}{3n}.
\tag{2}
\]
This verifies the \(+2\) shift and the identification of the overlap used in the coherent preparation.

Both \(\tau\) and \(q\) are computable from corner lists using products and quotients of integers of magnitude \(O(D)\). Exact numerators and denominators need only \(O(D\log D)\) bits. No Jack-coefficient oracle is required.

---

## 3. A finite-clock decoder with no supplied partition label

Assume the proposed uniform bounds:
\[
\tau_{\lambda,s}\ge\frac1{16d^2}\quad(d\ge1),
\qquad
q_{\mu,r}\ge\frac1{3|\mu|}.
\tag{Hov}
\]

### 3.1 Exact rewind tail

Consider either sampling operation after content \(c\) has been obtained. Let \(Q\) be the observed-content projector and \(P\) the return projector:

- UP: \(P=\pi_0\);
- DOWN: \(P=P_A\).

Inside the relevant invariant space, let their normalized range vectors be \(x,y\), with
\[
|\langle x,y\rangle|^2=p.
\]

Use this clocked procedure:

1. Test \(P\). On success, stop.
2. Otherwise, repeat: test \(Q\), then test \(P\), stopping on \(P\)-success.
3. Allow at most \(T\) repetitions of step 2.

After a failed \(P\)-test, the state is the unique \(P\)-orthogonal vector in \(\operatorname{span}\{x,y\}\). Each subsequent \(Q,P\) round succeeds with probability \(2p(1-p)\). Therefore
\[
\Pr[\text{timeout}]
 =(1-p)\bigl(1-2p(1-p)\bigr)^T.
\tag{3}
\]

This calculation includes **both outcomes of every failed test**; it is not postselection.

For a degree-\(D\) decoder, set
\[
\gamma=\frac1{16D^2}.
\]
Every relevant \(p\) either equals \(1\), or lies in
\[
[\gamma,1-\gamma].
\]
The upper bound follows because, when there is another corner, that corner also has mass at least \(\gamma\). The one-removable-corner case has \(p=1\) and returns immediately. Hence
\[
\Pr[\text{timeout}]\le e^{-\gamma T}.
\tag{4}
\]

This complementary-overlap argument matters. A lower bound on \(p\) alone would not justify the exponential tail uniformly as \(p\to1\).

### 3.2 Explicit clocks and sample counts

For \(0<\eta<1\), choose
\[
N=
\left\lceil
  16D^2\log\frac{2(2D+1)}{\eta}
\right\rceil
\tag{5}
\]
UP samples and the same number of DOWN samples, and
\[
T=
\left\lceil
  16D^2\log\frac{4N}{\eta}
\right\rceil.
\tag{6}
\]

There are at most \(2D+1\) corners in total. Comparing with the unlimited, exactly returning sampler gives
\[
\Pr[\text{some corner missed}]
 \le(2D+1)e^{-\gamma N}\le\eta/2.
\]
A union bound over the \(2N\) rewind clocks gives
\[
\Pr[\text{some timeout}]
 \le2Ne^{-\gamma T}\le\eta/2.
\]
Thus the reconstructed label is correct with probability at least \(1-\eta\), uniformly over all \(\lambda\vdash D\).

No \(\lambda\), corner count, or overlap value is supplied to this procedure.

### 3.3 Coherent implementation and the missing operator-norm argument

Defer every measurement into a fresh outcome register. Keep the entire finite history. On timeout:

- set an abort flag reversibly;
- freeze that branch;
- retain its data-space tag and all history.

In particular, do not attempt to apply \(V^\dagger\) to a failed DOWN branch as though it were in \(\operatorname{ran}V\).

Let \(H\) be this finite-history unitary, including reversible reconstruction of a candidate \(f(h)\). On input workspace zero, write
\[
H|j_\lambda,0\rangle
 =\sum_h K_h|j_\lambda\rangle\,|h\rangle .
\]

The essential structural fact is stronger than basis-state success:

\[
\boxed{\quad
\langle K_hj_\lambda,K_hj_\nu\rangle=0
\quad\text{for every }h,\ \lambda\ne\nu.
\quad}
\tag{7}
\]

For successful histories, the data is a scalar multiple of the original Jack vector. For a timeout history, all preceding samples returned successfully, and the frozen data lies in \(Z_\lambda\) or \(S_\lambda\); those spaces are orthogonal across input partitions. A fixed history specifies the same timeout stage for all inputs compatible with it. This proves (7), including failure branches.

Now use **XOR**, not merely copying into an assumed blank register:
\[
C=H^\dagger\,\operatorname{XOR}_{f(h)}\,H.
\tag{8}
\]
Define the ideal label-XOR unitary
\[
X_D=\sum_{\lambda\vdash D}
 |j_\lambda\rangle\langle j_\lambda|
 \otimes X_{\operatorname{enc}(\lambda)}.
\]

### Proposition 3: clean coherent decoder

If the classical reconstruction error is at most \(\eta\) for every \(\lambda\), then
\[
\|CI_0-I_0X_D\|_{\rm op}\le2\sqrt{\eta},
\tag{9}
\]
where \(I_0\) appends zero workspace. This bound holds for an arbitrary label-register input, and remains valid with an arbitrary reference system.

### Proof

For an input \(\sum_\lambda |j_\lambda\rangle|v_\lambda\rangle\), compare the two operations immediately before \(H^\dagger\). The difference is
\[
\sum_{\lambda,h}
 K_h|j_\lambda\rangle|h\rangle
 (X_{f(h)}-X_{\operatorname{enc}(\lambda)})|v_\lambda\rangle.
\]
Equation (7) removes all cross terms between distinct \(\lambda\), and histories remove cross terms between distinct \(h\). Correct-label terms vanish; each incorrect-label term has operator norm at most \(2\). The squared norm is therefore at most
\[
4\eta\sum_\lambda\|v_\lambda\|^2.
\]
Applying \(H^\dagger\) preserves the norm. ∎

There is **no factor \(p(D)\)**.

For decoder error \(\epsilon\), take \(\eta=\epsilon^2/16\). Equation (9) contributes at most \(\epsilon/2\); allocate the remaining \(\epsilon/2\) to uniform operator-norm implementation errors.

A conservative bound for the complete compute–XOR–uncompute circuit is
\[
K_{\rm dec}\le32N(T+2)
 =O\!\left(D^4\log^2\frac{D+1}{\epsilon}\right)
\tag{10}
\]
native readout/isometry/projector-test calls.

“Clean” here is an approximation in the norm of the **entire output, including workspace**. The finite sampler does not produce exactly zero garbage with zero error.

---

## 4. The coherent-preparation upgrade is constructible

Measured, label-dependent preparation histories cannot simply be discarded. The following operation replaces them completely.

### Proposition 4: clean native-projector rotation

Suppose native projectors \(P,Q\) restrict to rank-one projectors onto unit vectors \(x,y\) in an invariant space, with known positive overlap
\[
\langle y,x\rangle=\sqrt p.
\]
Let \(K\ge1\) satisfy
\[
p_*:=\sin^2\!\left(\frac{\pi}{4K+2}\right)\le p.
\]
There is a clean unitary mapping \(x\) to \(y\), using \(K\) pairs of native projector reflections and one ancillary qubit. It uses no preparation inverse for \(x\).

### Construction and proof

Put
\[
\theta=\frac{\pi}{4K+2},\qquad
|t_p\rangle=
 \sqrt{\frac{p_*}{p}}\,|0\rangle+
 \sqrt{1-\frac{p_*}{p}}\,|1\rangle.
\]
Define
\[
P'=P\otimes|0\rangle\langle0|,\qquad
Q'=Q\otimes|t_p\rangle\langle t_p|.
\]
Then
\[
\langle y,t_p|x,0\rangle=\sin\theta.
\]

On their two-dimensional span,
\[
G=(2P'-I)(I-2Q')
\]
is the usual \(2\theta\) rotation. Explicitly, if
\[
|x,0\rangle=\sin\theta\,|y,t_p\rangle+\cos\theta\,|z\rangle,
\]
then
\[
G^K|x,0\rangle
 =\sin((2K+1)\theta)|y,t_p\rangle
  +\cos((2K+1)\theta)|z\rangle
 =|y,t_p\rangle.
\]
Finally apply the inverse of the one-qubit rotation preparing \(t_p\). The output is \(y\otimes|0\rangle\), with the positive phase shown above. ∎

The extra operation is thus only a **computable, label-controlled one-qubit rotation** and native projector reflections.

### Application to each growth edge

Choose a reversible, deterministic one-box path from the input partition, for example row-by-row filling. At degree \(d\), for the edge \(\lambda\to\mu=\lambda+s\), use:

| Stage | Source projector | Target projector | Squared overlap |
|---|---|---|---|
| \(j_\lambda\to\phi_{\lambda,s}\) | \(\pi_0\) | \(E_{c(s)}^{(d)}\) | \(\tau_{\lambda,s}\) |
| \(\phi_{\lambda,s}\to V_dj_\mu\) | \(E_{c(s)}^{(d)}\) | \(P_A\) | \(q_{\mu,s}\) |

The invariant spaces are respectively \(Z_\lambda\) and \(S_\mu\). Apply \(V_d^\dagger\) after the second rotation.

Uniform iteration counts are
\[
K_\uparrow(d)=4\max(1,d),\qquad
K_\downarrow(n)=\left\lceil\sqrt{3n}\right\rceil,
\quad n=d+1.
\tag{11}
\]
They satisfy the required \(p_*\le p\) by (Hov), including the trivial degree-zero case.

The total number of projector reflections is
\[
2\sum_{d=0}^{D-1}
 \bigl(K_\uparrow(d)+K_\downarrow(d+1)\bigr),
\]
plus \(D\) applications of \(V_d^\dagger\). This is less than a loose bound
\[
20(D+1)^2
\tag{12}
\]
for reflections and final isometries.

All path prefixes, contents, rational overlaps, and rotation angles are computed **coherently from the input label** and uncomputed before that label is erased. The loop counts depend only on degree, not on \(\lambda\). Variable rotations are implemented from angle registers, not by measuring the label and generating a label-dependent classical gate program.

Consequently this gives a uniform clean controlled preparation
\[
|\lambda\rangle|0\rangle|0_W\rangle
 \longmapsto
|\lambda\rangle|j_\lambda\rangle|0_W\rangle
\tag{13}
\]
in the ideal arithmetic/rotation model, and a uniform operator-norm approximation with finite precision.

The only inverses used are:

- native \(V_d^\dagger\);
- native spectral-readout inverses;
- reversible arithmetic inverses;
- one-qubit rotation inverses.

**There is no recursive Jack-preparation inverse.**

---

## 5. Erasing the input partition and obtaining the full transform

### Proposition 5

Under (H+) and (Hov), there is a uniform approximate clean implementation of
\[
U_J|\lambda\rangle=|j_\lambda\rangle
\]
on the \(p(D)\)-dimensional partition code space.

### Construction

First perform (13). Then apply the decoder’s label-XOR operation with the physical Jack register as its data and the original partition register as its XOR target:
\[
|\lambda\rangle|j_\lambda\rangle
 \longmapsto
|0\rangle|j_\lambda\rangle.
\tag{14}
\]
All preparation-control work must already have been uncomputed. A register swap and, if necessary, a reversible conversion between partition encodings put the output in the desired register.

For a superposition,
\[
\sum_\lambda a_\lambda|\lambda\rangle
 \longmapsto
\sum_\lambda a_\lambda|j_\lambda\rangle,
\]
with no surviving copy of \(\lambda\). Splitting the error budget between controlled preparation and decoding gives total operator-norm error at most \(\epsilon\).

Because the normalized Jacks form an orthonormal basis, the target \(U_J\) is a unitary change of basis between the two logical spaces. The compiled circuit is a unitary on its padded registers and approximates the clean logical transformation. Its inverse is simply the reverse of this polynomial-size circuit.

This consequence does **not** follow from the original measured preparation alone; it follows from Proposition 4 plus the clean decoder.

---

## 6. Fully charged implementation bounds

Here is one deliberately loose implementation avoiding free sparse-matrix, state-preparation, or QRAM oracles.

Let
\[
g=D+1,\qquad \ell=1+\log(g/\epsilon).
\]

### Native \(V\)

In the normalized occupation encoding,
\[
V_{n-1}|m_1,\ldots,m_n\rangle
 =
\sum_{k:m_k>0}
 \sqrt{\frac{k m_k}{n}}\,
 |m-e_k,\ l=k-1\rangle.
\tag{15}
\]

Construct this by a reversible tree of weighted choices over the explicit \(D\) occupation registers. Uncompute all weight arithmetic before changing the occupations; retain the chosen \(k-1\) as the actual \(w\)-register, not as garbage. The inverse adds mode \(l+1\) and reverses the choice circuit.

Thus disjoint supports are accompanied by an actual circuit construction. Reflection or testing of \(P_A\) is obtained by conjugating the computational input-code projector with this circuit.

### Native content readout

Take
\[
M=2^q>4D.
\]
Ideal phase estimation on
\[
\exp\!\left(2\pi i(L_d+dI)/M\right)
\]
reads the integer \(c+d\) **exactly** in the ideal simulation model. Only \(q=O(\log D)\) controlled evolutions are needed, each at time at most \(2\pi\). Degenerate content eigenspaces remain untouched internally.

Binary tests and reflections for \(E_c\) are readout–compare/phase–unreadout circuits. Their errors are bounded as whole unitaries, not merely on individual eigenvectors.

### Explicit polynomial Hamiltonian simulation

Split \(L_d\) into its diagonal and, for every mode \(k\), two matching Hamiltonians according to the parity of the upper occupation on that edge:
\[
L_d=H_{\rm diag}+\sum_{k=1}^d(H_{k,0}+H_{k,1}).
\]
Each matching is a disjoint union of two-level systems with coupling
\(\sqrt{3km_k}\). Reversible pair identification and a computed two-level rotation implement its exponential cleanly.

There are \(2d+1\) terms, and
\[
\sum_j\|H_j\|
 \le2d+2d\sqrt{3d}\le6g^{3/2}.
\]
For \(|t|\le2\pi\), first-order product formula with
\[
r=\left\lceil 2000g^3/\delta\right\rceil
\]
steps, together with appropriately synthesized rotations, suffices for operator-norm error \(\delta\).

Using conservative schoolbook reversible arithmetic and rotation synthesis, one matching exponential can be bounded by
\[
O(g^2 b^6)
\]
gates, where \(b\) is the required bit precision. A native spectral readout of error \(\delta\) therefore has a loose bound
\[
O\!\left(
 \frac{g^6}{\delta}
 \log^8\frac{g}{\delta}
\right).
\]

Allocate per-native-operation error \(O(\epsilon/K)\), where
\[
K=O(g^4\ell^2)
\]
includes the decoder and coherent preparation. The resulting all-inclusive loose bounds are
\[
\boxed{
\text{gates }=
O\!\left(g^{14}\epsilon^{-1}\ell^{12}\right),
\qquad
\text{qubits }=
O\!\left(g^4\ell^3\right).
}
\tag{16}
\]
Exact overlap products have \(O(D\log D)\) bits; direct arithmetic and elementary-function evaluation for the preparation angles fit below this envelope.

These bounds are intentionally not optimized. In particular, (16) claims only polynomial dependence on \(1/\epsilon\), not an uncharged polylogarithmic-precision implementation.

### Input and output charges

- The decoder acts on **one already supplied quantum state** in \(F_D\); it does not obtain that state from classical coefficients for free.
- Explicit occupation/partition registers use \(O(D\log D)\) bits. Their loading, scanning, and reversible conversion are charged.
- The full transform acts on an already supplied computational-basis state or superposition. Preparing an arbitrary input superposition is a separate cost.
- The output is a quantum state. Reading one partition costs its explicit output length. Extracting all coefficients is not included.

---

## 7. Exact counterexamples to the tempting shortcuts

### A. Perfect basis-state nondemolition can still destroy coherence

At \(D=2\),
\[
A_{(2)}=\{6,-1\},\qquad
A_{(1,1)}=\{3,-2\}.
\]
The UP content records have disjoint supports. Reading or discarding that record distinguishes the two Jack labels perfectly.

Even if an ideal rewind subsequently restores each individual Jack state, the input
\[
\frac{|j_{(2)}\rangle+|j_{(1,1)}\rangle}{\sqrt2}
\]
becomes the equal incoherent mixture when the record is discarded. Its trace distance from the intended pure superposition is \(1/2\).

Thus classical-label preparation can be perfect on every basis input and still fail the coherent task by a constant.

More generally, basis-vector error does not control operator error: for
\[
|u\rangle=M^{-1/2}\sum_{i=1}^M|i\rangle,\qquad
R=I-2|u\rangle\langle u|,
\]
every basis-vector error is \(2/\sqrt M\), while
\[
\|R-I\|_{\rm op}=2.
\]
Equation (7), not a dimension-dependent union bound, is what prevents this failure in the decoder proof.

### B. The complete UP support and \(D\) do not determine the partition

The distinct degree-28 partitions
\[
\lambda=(5^4,4,1^4),\qquad
\nu=(5,3^7,2)
\]
have the same addable-content set
\[
\{15,8,-2,-9\}.
\]
Their removable-content sets are respectively
\[
\{9,5,-8\},\qquad
\{12,-1,-5\}.
\]
So collecting UP supports alone, without estimating weights, is insufficient. This does not refute Proposition 1; it illustrates why the second corner set is substantive.

### C. Finite sampling does not give an exactly clean, zero-error decoder

For
\[
\lambda=(3,2),\qquad \nu=(3,1,1),
\]
both UP supports contain \(9\), and both DOWN supports contain \(6\). The relevant probabilities are
\[
\tau_{\lambda,9}=\frac5{44},\quad q_{\lambda,6}=\frac12,
\qquad
\tau_{\nu,9}=\frac3{28},\quad q_{\nu,6}=\frac{11}{20}.
\]
The finite history “always UP \(9\), always DOWN \(6\), every initial return test succeeds” has positive probability for both inputs. No deterministic history-label function can label that history correctly for both.

With \(N\) samples in each direction, this alone gives the compute–copy–uncompute scheme a nonzero worst-case norm error of at least
\[
\sqrt2\,(5/88)^N.
\]
It does **not** obstruct arbitrary prescribed \(\epsilon>0\); it rules out silently replacing bounded error by exact cleanliness.

---

## 8. Remaining proof obligations and falsifiers

The conditional result is invalidated by any of the following:

1. An exact all-degree counterexample to the **positive** identity (H+).
2. A required overlap violating (Hov).
3. A native implementation whose guarantee is only basis-state accuracy, rather than the uniform operator-norm bounds used above.
4. Unremoved label-dependent work in controlled preparation before step (14).
5. Use of a finer, unspecified eigenbasis measurement inside globally degenerate content eigenspaces instead of \(E_c\).

The reconstruction, invariant-space deductions, finite-clock analysis, coherent-history norm bound, and native-projector rotation are analytic deductions, not extrapolations from finite controls.

**Bottom line:** under the allowed assumptions, there is no remaining coherent-preparation obstruction: it is resolved by the explicit projector-rotation construction. The conditional full transform follows, with charged polynomial resources and uniformly small total-workspace error. This establishes neither a classical hardness result nor a speedup or novelty claim.