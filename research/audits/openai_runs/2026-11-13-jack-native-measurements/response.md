# Conditional resource audit

## Verdict

**Yes, conditional on the two stated mathematical assumptions, the mechanism admits an end-to-end polynomial BIT/circuit implementation.** No reflection about a Jack state, and no inverse of an earlier Jack-preparation routine, is needed.

This conclusion requires a specific completion of the shorthand algorithm:

1. every test is a **binary Lüders measurement**, not a finer measurement with its outcome subsequently forgotten;
2. after a failed recovery measurement, continue alternating—do not repeatedly measure the same projector;
3. implement the native isometry coherently, with its mode-selection label incorporated into the output rather than discarded;
4. use a predetermined abort clock and a global, unconditioned error budget.

A deliberately loose constructive bound proved below is
\[
 O\!\left((D+1)^{11}
 \left[\log\frac{D+1}{\epsilon}\right]^{21}\right)
\]
finite-set quantum gates and classical bit operations, apart from polynomial input-parsing cost. Thus the precision dependence can be polynomial in \(\log(1/\epsilon)\), not merely polynomial in \(1/\epsilon\).

**Scientific action:** the resource step can be stated as a conditional theorem, with the implementations and recovery rule below. The all-degree intertwining and uniform overlap claims remain **OPEN without the assumptions**. Neither the finite control nor this conditional resource theorem establishes an advantage, novelty, or classical hardness.

---

## 1. Exact assumptions and quantified conclusion

Write
\[
\mathcal H_d=\mathcal F[w]_d,\qquad \mathcal K_n=\mathcal F_n,
\]
with the supplied Hall inner product. Use hats for normalized vectors:
\[
f_\lambda=\frac{J_\lambda}{\|J_\lambda\|},\qquad
e_{\lambda,s}=\frac{\psi_{\lambda,s}}{\|\psi_{\lambda,s}\|}.
\]

The supplied Theorem 1.4 and Lemmas 3.3–3.5 provide the following source facts:

- \(\mathcal H_d=\bigoplus_{\lambda\vdash d} Z_\lambda\), orthogonally;
- \(L_d\) is self-adjoint;
- \(L_d|_{Z_\lambda}\) has simple spectrum indexed by \(A_\lambda\);
- \(\pi_0 Z_\lambda=\mathbb C J_\lambda\);
- \(\pi_0\psi_{\lambda,s}=J_\lambda\);
- all contents are integers in \([-d,3d]\).

These are used as supplied, not independently reverified through external access.

The **two additional mathematical assumptions** are:

**H1 — all-degree intertwining.**
For every \(d\ge0\), every \(\lambda\vdash d\), and every \(s\in A_\lambda\),
\[
A_d\psi_{\lambda,s}=J_{\lambda+s}.
\]

**H2 — both uniform overlap bounds.**
For the same quantifiers, putting \(n=d+1\) and
\[
\beta_d=\frac1{100n^4},
\]
assume
\[
p_{\lambda,s}:=|\langle f_\lambda,e_{\lambda,s}\rangle|^2\ge\beta_d,
\]
and
\[
q_{\lambda,s}:=
|\langle e_{\lambda,s},V_df_{\lambda+s}\rangle|^2\ge\beta_d,
\qquad
V_d=\frac{A_d^\dagger}{\sqrt{3n}}.
\]

Here “overlap” means squared overlap, consistent with the transition weight \(\tau\). If the promised bound instead concerns the unsquared modulus, replace \(\beta_d\) by \(\beta_d^2\) throughout; the conclusion remains polynomial.

### Conditional theorem

Under H1–H2, for every explicit partition \(\Lambda\vdash D\) and every rational \(0<\epsilon\le1/2\), there is a uniform finite-clock quantum circuit which:

- starts from computational-basis zero states;
- outputs an abort flag and a state in the occupation encoding;
- has abort probability at most \(\epsilon\);
- conditioned on no abort, has trace distance at most \(\epsilon\) from \(f_\Lambda\);
- also has unconditional trace distance at most \(\epsilon\) if abort is replaced by a fixed valid fallback state;
- has the polynomial bit/gate bound above.

Only H1–H2 for degrees \(0,\ldots,D-1\) are needed for a particular input size \(D\).

---

## 2. Native isometry and the two invariant decompositions

### 2.1 The isometry identity is exact

The weighted adjoint is
\[
A_d^\dagger g
 =\sum_{k=1}^{n}3k\,\partial_{V_k}g\,w^{k-1}.
\]
Consequently, for homogeneous \(g\in\mathcal K_n\),
\[
A_dA_d^\dagger g
 =3\sum_{k=1}^{n}kV_k\partial_{V_k}g
 =3n\,g.
\]
The last equality is the weighted Euler identity. Therefore
\[
V_d^\dagger V_d=I_{\mathcal K_n},
\qquad
P_A:=V_dV_d^\dagger
\]
is an orthogonal projector.

For an occupation vector \(m=(m_1,\ldots,m_n)\) satisfying
\(\sum k m_k=n\), this gives
\[
V_d|m\rangle
 =\sum_{k:m_k>0}
 \sqrt{\frac{k m_k}{n}}\,
 |m-e_k,\ell=k-1\rangle.                 \tag{1}
\]
No Jack coefficient or Jack norm is needed to implement (1).

### 2.2 Stage 1: source cyclic space

Let \(Q_c=\mathbf1_{\{c\}}(L_d)\), where \(c=c(s)\). On \(Z_\lambda\),
\[
\pi_0=|f_\lambda\rangle\langle f_\lambda|,
\qquad
Q_c=|e_{\lambda,s}\rangle\langle e_{\lambda,s}|.       \tag{2}
\]

For the first equality, \(\pi_0\) is orthogonal, its image on \(Z_\lambda\) is
\(\mathbb C f_\lambda\), and \(f_\lambda\in Z_\lambda\). The second follows from the simple corner spectrum in that cyclic space.

Both projectors, and both complements, preserve \(Z_\lambda\). More strongly, they preserve
\[
S^{(1)}_{\lambda,s}
 =\operatorname{span}\{f_\lambda,e_{\lambda,s}\}.
\]
Thus **every exact failure branch remains in this two-dimensional space**.

The normalization condition gives
\[
p_{\lambda,s}
 =\frac{\|J_\lambda\|^2}{\|\psi_{\lambda,s}\|^2}.
                                                        \tag{3}
\]

### 2.3 Stage 2: successor spaces

For every \(\mu\vdash n\), define
\[
W_\mu=
\operatorname{span}\{e_{\mu-r,r}:r\in R_\mu\}.
\]
The corner-pair eigenvectors form an orthonormal basis of \(\mathcal H_d\); grouping them by successor gives
\[
\mathcal H_d=\bigoplus_{\mu\vdash n}W_\mu
\]
orthogonally.

H1 implies
\[
V_d^\dagger e_{\lambda,s}
 =\frac{\|J_{\lambda+s}\|}
        {\sqrt{3n}\,\|\psi_{\lambda,s}\|}
   f_{\lambda+s}.
\]
Hence, writing \(b_\mu=V_df_\mu\),
\[
b_\mu=
\sum_{r\in R_\mu}
\sqrt{q_{\mu-r,r}}\,e_{\mu-r,r},                 \tag{4}
\]
where
\[
q_{\lambda,s}
 =\frac{\|J_{\lambda+s}\|^2}
        {3n\,\|\psi_{\lambda,s}\|^2},
\qquad
\sum_{r\in R_\mu}q_{\mu-r,r}=1.                  \tag{5}
\]
Completeness of the corner-pair basis proves that (4) has no omitted component.

It follows that
\[
P_A|_{W_\mu}=|b_\mu\rangle\langle b_\mu|.         \tag{6}
\]

Distinct removable corners have distinct contents. Indeed, if two removable corners satisfy \(y_1<y_2\), their row lengths satisfy \(x_1>x_2\), so
\[
(3x_1-y_1)-(3x_2-y_2)
 =3(x_1-x_2)+(y_2-y_1)>0.
\]
Therefore, for \(\mu=\lambda+s\),
\[
Q_{c(s)}|_{W_\mu}
 =|e_{\lambda,s}\rangle\langle e_{\lambda,s}|.    \tag{7}
\]

Equations (6)–(7) prove that Stage 2 and every exact failure branch preserve
\[
S^{(2)}_{\lambda,s}
 =\operatorname{span}\{e_{\lambda,s},b_\mu\}.
\]

**Global content degeneracy is harmless only because of these invariant restrictions.** No global rank-one assertion is being made.

---

## 3. Recovery rule and a uniform finite clock

Consider rank-one projectors onto unit vectors \(a,b\), and set
\[
p=|\langle a,b\rangle|^2>0.
\]
Use this procedure:

1. start in \(a\);
2. measure the projector onto \(b\); stop on success;
3. following failure, measure the projector onto \(a\), then the projector onto \(b\);
4. repeat step 3 regardless of the intermediate \(a\)-measurement outcome.

No previously prepared state is reconstructed.

For \(0<p<1\), after every failed \(b\)-test the state is the same vector \(b^\perp\) in \(\operatorname{span}\{a,b\}\), up to phase. From that vector, one recovery pair succeeds with probability
\[
(1-p)p+p(1-p)=2p(1-p).
\]
Thus after the initial test and \(K\) recovery pairs,
\[
\Pr(\text{no success})=
(1-p)\,[1-2p(1-p)]^K.                           \tag{8}
\]
For \(p=1\), the initial test succeeds certainly.

This calculation also identifies a forbidden reset interpretation: after an \(a\)-test fails, repeatedly testing \(a\) cannot recover—the state is already in its orthogonal complement.

### Why a lower bound alone is not the whole clock proof

Equation (8) involves \(1-p\) as well as \(p\). Here the required complementary bound follows from the **all-corner quantifiers** in H2:

- Stage 1 has \(\sum_{s\in A_\lambda}p_{\lambda,s}=1\).
- Stage 2 has the sum rule (5).

If the relevant corner set contains at least two elements, every nontrivial overlap satisfies
\[
\beta_d\le p\le1-\beta_d,
\]
and therefore
\[
2p(1-p)\ge2\beta_d(1-\beta_d)\ge\beta_d.         \tag{9}
\]
If the corner set is a singleton, its overlap is exactly one.

Set
\[
H=\left\lceil\log_2\frac{64(D+1)}{\epsilon}\right\rceil,
\qquad
K_d=100(d+1)^4H.
\]
Abort a stage if its initial target test and its \(K_d\) recovery pairs all fail. Equations (8)–(9) give stage-abort probability at most \(2^{-H}\). Across the \(2D\) stages,
\[
a_{\rm ideal}\le2D\,2^{-H}\le\epsilon/32.        \tag{10}
\]

The number of binary measurements plus final native inverses is at most
\[
3D+400H\sum_{n=1}^{D}n^4
 \le N_0:=500(D+1)^5H.                          \tag{11}
\]

At \(d=0\), both spaces are singletons and both overlaps are one; there is no division by \(1-p\).

For a legal classical growth path, Stage 1 uses
\[
a=f_\lambda,\quad b=e_{\lambda,s},
\]
and Stage 2 uses
\[
a=e_{\lambda,s},\quad b=V_df_{\lambda+s}.
\]
After Stage 2 succeeds, the native inverse maps the latter state to \(f_{\lambda+s}\). Induction proves exact correctness of every ideal non-aborting history.

---

## 4. Native circuits, including clean workspace

### 4.1 Encoding and input access

Use explicit occupation registers \(m_1,\ldots,m_D\), each with
\(O(\log(D+1))\) bits, and a register for \(\ell\). This uses
\(O(D\log(D+1))\) output/data qubits.

The normalized computational basis represents
\[
\frac{p_\mu w^\ell}{\sqrt{z_\mu3^{\ell(\mu)}}}.
\]
There is no partition-space enumeration and no qRAM assumption.

Read and validate the supplied partition. A legal path is obtained by filling its rows in order, left to right. All \(D\) boxes and their contents are computed explicitly. Input access and this preprocessing cost polynomial time in the explicit input length and numerical \(D\).

### 4.2 A clean unitary extension of \(V_d\)

Let \(U_d\) act on occupation and index registers as follows.

1. From index \(0\), coherently prepare
   \[
   \sum_{k=1}^{n}\sqrt{k m_k/n}\,|k\rangle.
   \]
   A binary prefix tree implements this: at each node compute the total integer weight in its left and right subtrees, rotate the next index bit accordingly, and uncompute the arithmetic.
2. Decrement \(m_k\), controlled on the selected \(k\).
3. Reuse the index register as \(\ell=k-1\).

All arithmetic scratch is uncomputed. In particular, there is **no discarded copy of \(k\)** or of the original occupation vector. The output itself reconstructs the input by adding one particle in mode \(\ell+1\).

Let
\[
R_n=\mathbf1\{\ell=0,\ \sum_k k m_k=n\}
\]
on the complete register encoding. Extend the above reversible operations arbitrarily but unitarily to invalid encodings. Then
\[
U_d R_n U_d^\dagger=P_A.                        \tag{12}
\]

A binary \(P_A\)-measurement is therefore:

- apply \(U_d^\dagger\);
- coherently compute the single predicate defining \(R_n\);
- measure only that predicate;
- apply \(U_d\).

On Stage 2 success, a further \(U_d^\dagger\) produces \(f_{\lambda+s}\) with index zero.

This inverse is a fixed native arithmetic circuit. It is **not** the inverse of a Jack-preparation circuit.

Similarly, the \(\pi_0\)-test computes and measures only the predicate \(\ell=0\); it does not measure \(\ell\) itself.

### 4.3 Finite-set gates: no unit-cost real rotations

The following elementary construction supplies the needed rotation compiler and will also be used for Hamiltonian simulation.

**Half-block lemma.** Suppose a unitary \(W\), with clean signal ancillas projected by \(P\), has block
\[
B=PWP,\qquad \|B-U/2\|\le\rho
\]
for a desired logical unitary \(U\). Put \(R=I-2P\). Then
\[
\mathcal O=-WRW^\dagger RW
\]
has clean block
\[
P\mathcal OP=3B-4BB^\dagger B.
\]
Expanding around \(U/2\) gives
\[
\|P\mathcal OP-U\|\le15\rho.
\]
Because \(\mathcal O\) is unitary, its off-clean block has norm
\(O(\sqrt\rho)\). Consequently,
\[
\|\mathcal O(|0\rangle\otimes I)-|0\rangle\otimes U\|
 =O(\sqrt\rho).                                 \tag{13}
\]
This is uniform over inputs and reference systems.

For a rotation \(U=cI+sJ\), where \(J^\dagger=-J\), \(J^2=-I\), and
\(c^2+s^2=1\), construct a half-block using a uniform \(b\)-bit seed:

- allocate approximately \(|c|/2\) of its labels to \(\operatorname{sgn}(c)I\);
- allocate approximately \(|s|/2\) to \(\operatorname{sgn}(s)J\);
- split the remaining labels equally between \(I\) and \(-I\).

Prepare the seed with Hadamards, apply this selection using integer threshold comparisons, and undo the Hadamards. Its clean block differs from \(U/2\) by \(O(2^{-b})\). Equation (13) gives error \(O(2^{-b/2})\).

The selected operations are Pauli/phase operations. Thresholds are computed reversibly. Thus a fixed gate set containing Hadamard, \(S\), CNOT and Toffoli suffices. Controlled rotations are covered by allowing \(c,s\) to depend on unchanged control bits.

Square roots and divisions use finite-bit integer arithmetic. Sines and cosines can be computed by bounded-argument Taylor series; \(\pi\), where needed, can be computed from geometrically convergent arctangent series. Keeping intermediate Boolean computation and reversing it after copying the result makes these computations reversible with polynomial overhead.

Signal ancillas may be measured at the end of the gadget. A nonzero result is an **explicit abort**, not free postselection. On non-abort they are exactly clean; (13) bounds the full instrument error, including abort.

The only reflections in this construction are about **known zero ancillas**.

---

## 5. Content measurements by explicit sparse simulation

### 5.1 Native sparse decomposition

In the normalized occupation basis, \(L_d\) has diagonal \(2\ell\) and edges
\[
(m,\ell)\longleftrightarrow(m-e_k,\ell+k)
\]
of weight \(\sqrt{3k m_k}\).

For each \(k\), split its edges according to the parity of the upper endpoint’s \(m_k\). Each resulting edge set is a matching: a vertex has at most one incident edge of each parity. Therefore
\[
L_d=H_0+\sum_{k=1}^{d}\sum_{a=0}^1 H_{k,a},      \tag{14}
\]
where \(H_0\) is diagonal and every \(H_{k,a}\) is a direct sum of two-by-two off-diagonal blocks and zeros.

On valid degree-\(d\) encodings,
\[
\|H_0\|\le2d,\qquad
\|H_{k,a}\|\le\sqrt{3d}.
\]
All endpoints, weights, and matching memberships are computable by explicit occupation-register arithmetic.

A matching can be reversibly relabelled by its canonical endpoint and an orientation bit. Rotating that bit, then reversing the relabelling, implements the corresponding two-level operation with clean workspace.

### 5.2 A block encoding with polynomial normalization

Choose an integer
\[
B_0=4(d+1)
\]
and a power of two \(M_0\ge2d+1\), padding (14) with zero terms.

Each term has a native unitary block encoding of \(H_j/B_0\):

- for a diagonal term, rotate a signal qubit with clean amplitude equal to the diagonal entry divided by \(B_0\);
- for a matching, use clean amplitude \(a/B_0\), followed, on the clean branch, by the matching swap;
- for a zero term, flip the signal qubit.

Uniformly select the term using Hadamards. The resulting unitary \(U_L\) has clean block
\[
\frac{L_d}{\Gamma},\qquad
\Gamma=M_0B_0=O((d+1)^2).                        \tag{15}
\]
This construction uses no sparse-matrix oracle: the address and value computations are included in the circuit.

### 5.3 Polynomial-logarithmic precision simulation

Here is a direct simulation proof, rather than an appeal to an unspecified simulation theorem.

To simulate \(e^{itL_d}\), for the times used below \(|t|\le\pi\), take
\[
R_{\rm seg}=32\Gamma,\qquad
\Delta=t/R_{\rm seg},\qquad
x=\Gamma|\Delta|\le1/8.
\]
The degree-\(K\) Taylor polynomial
\[
T_K=\sum_{k=0}^{K}\frac{(i\Delta L_d)^k}{k!}
\]
satisfies
\[
\|T_K-e^{i\Delta L_d}\|
 \le\sum_{k>K}\frac{x^k}{k!}
 \le8^{-K}.                                    \tag{16}
\]

Using fresh block-signal registers, \(k\) applications of \(U_L\) have clean block \((L_d/\Gamma)^k\). Coherently select \(k\) with weights
\[
\frac{x^k}{2k!},
\]
and phase \((i\,\operatorname{sgn}t)^k\). Their sum is less than one. Split the remaining probability equally between \(I\) and \(-I\), whose contributions cancel. The resulting unitary has clean block exactly \(T_K/2\) in the ideal-arithmetic construction.

Apply the half-block lemma. Taking
\[
K=O\!\left(\log\frac{R_{\rm seg}}{\zeta}\right)
\]
makes one segment’s clean-isometry error \(O(\zeta/R_{\rm seg})\). Composing all \(R_{\rm seg}\) segments gives error \(O(\zeta)\). Finite-gate compilation is allocated an additional \(O(\zeta)\) budget.

All inverses used here are inverses of native arithmetic, block-encoding, and coefficient-preparation circuits. None is a Jack-preparation inverse. Known scalar phases in the half-block construction must be retained in controlled versions.

Again, dirty signal outcomes can cause a charged abort; there is no cost-free conditioning.

### 5.4 Exact-grid content extraction

Choose a power of two \(M>4d\). With ideal controlled evolutions, the circuit
\[
|v_c\rangle|0\rangle\longmapsto
|v_c\rangle|c\bmod M\rangle                     \tag{17}
\]
is exact for every eigenvector of integer eigenvalue \(c\in[-d,3d]\).

Indeed, prepare a uniform superposition of \(y=0,\ldots,M-1\), apply
\(e^{2\pi i yL_d/M}\), and inverse Fourier transform. The required controlled times are
\[
t_j=2\pi\,2^j/M,
\]
whose sum is less than \(2\pi\), and each is at most \(\pi\).

To measure the **binary** projector \(Q_{c_*}\):

1. coherently perform (17);
2. compute the equality flag \(c=c_*\);
3. uncompute (17);
4. measure only the equality flag.

This is exactly the Lüders instrument
\[
\rho\longmapsto
Q_{c_*}\rho Q_{c_*}\otimes|1\rangle\langle1|
+(I-Q_{c_*})\rho(I-Q_{c_*})\otimes|0\rangle\langle0|.
\]

Equal global contents receive the same label, as they must. Degeneracy creates no precision problem: the argument bounds the implemented instrument, not a choice of eigenvectors inside a degenerate eigenspace.

### 5.5 Bit complexity of the simulation

For one measurement with target instrument error \(\eta\), put
\[
B=1+\left\lceil\log_2\frac{D+1}{\eta}\right\rceil.
\]
Then:

- the phase register has \(O(\log(D+1))\) qubits;
- \(\Gamma,R_{\rm seg}=O((D+1)^2)\);
- \(K=O(B)\);
- \(O(B^2)\) arithmetic precision bits suffice.

The last item includes small Taylor weights. For the nonzero phase-estimation times, \(x\ge1/[C(D+1)]\), so every positive Taylor weight is at least
\[
2^{-O(K(\log(D+1)+\log K))}.
\]
Thus resolving the prefix-state-preparation denominators needs only \(O(B^2)\) bits. There is no hidden real-number oracle or exponentially long coefficient table.

Using schoolbook arithmetic and the rotation construction above gives the conservative bound
\[
C_{\rm meas}(D,\eta)
 \le C(D+1)^6 B^{20}                            \tag{18}
\]
for gates and classical bit operations, including circuit generation and controlled operations. The native isometry and range measurements fit within the same bound. These exponents are deliberately loose.

---

## 6. Accumulated error, leakage, and final resources

Use trace distance
\[
T(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1
\]
and half-diamond distance for instruments.

Set
\[
\eta=\frac{\epsilon}{64N_0}.
\]
Implement every counted native operation to half-diamond error at most \(\eta\), including all simulation, arithmetic, rotation, and clean-workspace abort errors.

A clean-isometry operator-norm error \(\delta\) bounds the induced channel’s half-diamond error by \(\delta\): apply the isometries to a purification, bound the vector difference, then use contractivity under measurement and discarding. Hence the preceding construction supplies the required instrument bounds.

Pad stopped branches with idle operations. The channel hybrid bound for the entire adaptive, clocked computation is
\[
T(\rho_{\rm actual}^{\rm flagged},
  \rho_{\rm ideal}^{\rm flagged})
 \le N_0\eta=\epsilon/64.                       \tag{19}
\]
This is an **unconditioned** bound. It remains valid even when an approximate failure branch leaves its ideal invariant space.

Combining (10) and (19),
\[
\Pr(\text{actual abort})\le3\epsilon/64.         \tag{20}
\]
Replacing abort by a fixed valid occupation state gives unconditional output error at most \(3\epsilon/64\). Conditioned on success,
\[
T(\rho_{\rm success},|f_\Lambda\rangle\langle f_\Lambda|)
 \le
 \frac{2(\epsilon/64)}{1-3\epsilon/64}
 <\epsilon.                                   \tag{21}
\]

There is **no claim** that every normalized approximate failure branch stays close to its ideal counterpart. That claim would be false for sufficiently rare histories. The bounded full instrument is what prevents postselection from concealing accumulated error.

Since \(\log((D+1)/\eta)=O(H)\), equations (11) and (18) yield
\[
\boxed{\quad
G,\ C_{\rm bit}
 =O\!\left((D+1)^{11}H^{21}\right).
\quad}                                        \tag{22}
\]
One conservative reusable workspace bound is
\[
O((D+1)^2H^{14})\ \text{qubits},
\]
including finite-arithmetic scratch and simulation signals. No workspace from earlier degrees must remain coherently stored.

The explicit input length is charged separately for parsing; \(D\) is charged **numerically**. The output is the coefficient state on \(O(D\log(D+1))\) data qubits. Producing a classical list of its amplitudes is not included or claimed.

---

## 7. Strongest native counterexample and implementation falsifiers

### Global rank-one content claims are false, with maximal possible output error

At \(d=4\), both
\[
(\lambda,s)=((2,2),(2,0))
\quad\text{and}\quad
(\lambda',s)=((2,1,1),(2,0))
\]
have content \(6\). Their eigenvectors are orthogonal because they lie in different cyclic spaces. Thus the global \(Q_6\) has rank at least two.

The intended successors are respectively
\[
(3,2)\quad\text{and}\quad(3,1,1).
\]
If the second eigenvector is supplied to a Stage 2 intended for the first, the native \(P_A,Q_6\) procedure operates in \(W_{(3,1,1)}\) and, on success, outputs
\(f_{(3,1,1)}\), not \(f_{(3,2)}\). These outputs are orthogonal: the error is trace distance **one**.

Therefore content tests do not certify the partition label, and leaked weight in another successor block is not automatically corrected. The invariant-space proof and the unconditioned error bound are essential.

### Measuring the entire \(w\)-register breaks the stated Stage 1 invariance

The supplied degree-two formulas give
\[
Z_{(2)}
 =\operatorname{span}\{J_{(2)},\,V_1w+3w^2\}.
\]
A binary \(\pi_0\)-failure can leave the second vector. Measuring the complete value of \(\ell\) can then produce \(w^2\), but
\[
w^2\notin Z_{(2)}.
\]
So “measure \(\ell\), then report whether it was zero” is **not** an acceptable implementation of the required binary Lüders measurement.

Likewise, classically sampling the mode in (1) and discarding the choice implements a mixture, not the native isometry.

These are exact falsifiers of particular universal implementation claims—not evidence for a complexity lower bound.

---

## Final assessment

**PROVED CONDITIONAL ON H1–H2:** both invariant-space constructions, rank-one restrictions despite global degeneracy, all exact failure branches, a coherent native isometry, finite-precision content measurements, a deterministic abort clock, and polynomial accumulated bit/circuit cost.

**OPEN without the assumptions:** H1 and H2 themselves.

The useful next action is to record the mechanism as this explicit conditional theorem and require binary-instrument and clean-workspace implementations. Additional low-degree controls cannot replace either remaining all-degree assumption. No speedup, novelty, or matched classical-sampling separation follows.