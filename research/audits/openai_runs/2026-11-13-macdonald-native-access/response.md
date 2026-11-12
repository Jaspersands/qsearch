## Verdict

**The mode-deletion construction works, and it gives the requested native interfaces conditionally on the stated algebraic and conditioning promises.** Two bookkeeping points are essential:

1. At degree \(n<D\), the preparation’s failure mass is \(D-\sum_k km_k\), not merely the marker value.
2. In powers of the inverse-square-root block, a marker used as temporary workspace must be fresh for each factor. Conversely, a unitary and its inverse must use the **same** banks.

The construction below uses fixed normalizations
\[
\alpha_C=32,\qquad S=2^{64},\qquad \Gamma=16S^2=2^{132}.
\]
They are independent of \(D,b\). No postselection, eigenbasis, \(\chi_\lambda\) oracle, real-rotation oracle, or QSVT phase oracle is used.

### Explicit interfaces—not deductions from generic specialization

Fix \(D\), \(N=D+1\), \(t=D/N\), and \(q=t^3\) throughout.

The conditional parts require:

* **Spectral interface:** on every valid degree sector \(d\le D\), the supplied specialized identities hold, and
  \[
  \operatorname{spec}(L_d)\subseteq\{t^k:-3D\le k\le D,\ k\in\mathbb Z\}.
  \]
* **Conditioning interface:** for \(n\ge1\), with \(A_n=QI\), an explicitly computable rational bound satisfies
  \[
  A_nA_n^\dagger\succeq \underline\chi(D,n)I,\qquad
  \underline\chi(D,n)^{-1}=\operatorname{poly}(D).
  \]
  Its computation and bit length must be polynomial. An existential “inverse-polynomial” assertion without a usable bound is not an executable interface.

No transition-overlap bound is assumed or proved here. In particular, this is not a proof of the complete shape-to-Macdonald transform.

---

## 1. Constant-normalization native \(C\): the deletion idea survives

Use registers
\[
|\ell,m_1,\ldots,m_D\rangle,\qquad
\ell+\sum_{k=1}^D km_k\le D,
\]
representing the normalized Hall occupation/marker basis. Their size is \(O(D\log(D+1))\) qubits.

Directly converting multiplication by \((1-t^k)p_kz^k/k\) into this normalized basis gives
\[
C=\sum_{k=1}^D w_k a_k^\dagger T_{-k},
\qquad
w_k^2=\frac{(1-t^k)(1-t^{3k})}{k\,t^{3k}}.
\]
Here \(T_{-k}\) vanishes when \(\ell<k\).

For \(k\le D\),
\[
1-t^k\le \frac{k}{N},\qquad
1-t^{3k}\le \frac{3k}{N},\qquad
t^{-3k}\le (1+1/D)^{3D}<27.
\]
Consequently
\[
w_k\le \frac{9\sqrt{k}}N,\qquad
\gamma_k:=\frac{Nw_k}{\sqrt{k}}\le9<16.
\]

Let \(M\) be a power of two with \(D\le M<2D\), and put \(F=\sum_k km_k\). A coherent, positive-amplitude preparation produces
\[
\sum_{k=1}^D\sqrt{\frac{km_k}{D}}\,
 |f=0,k\rangle
+\sqrt{\frac{D-F}{D}}\,|f=1,0\rangle .
\]
Unused labels have zero weight. This preparation is native: binary-prefix subtree weights are integer sums of the \(km_k\), calculated by loops over the \(D\) occupation registers. Each rotation’s arithmetic is uncomputed **before** changing the occupations. Zero-weight prefixes receive a specified identity branch.

On a good mode label:

1. Rotate a success flag with success amplitude \(\gamma_k/16\).
2. On success, remove one \(k\)-boson and increase the marker by \(k\).
3. Retain \(k\).
4. Apply Hadamards to its \(\log_2M\)-qubit register, so its zero outcome represents projection onto the uniform \(M\)-label state.

Step 2 has a polynomial-time unitary extension. For fixed \(k\), let
\[
u=\ell+km_k,\qquad L_k=\lfloor u/k\rfloor+1.
\]
Use the cycle
\[
m_k'=m_k-1\pmod{L_k},\qquad \ell'=u-km_k'.
\]
Whenever \(m_k>0\), this is precisely the required deletion. The invariant \(u\) permits its arithmetic to be uncomputed after the update. The wrap branch is harmless because its good preparation amplitude is zero when \(m_k=0\). Invalid encodings receive specified safe branches.

Thus the all-zero compression of this unitary is
\[
\sum_k
 \sqrt{\frac{km_k}{D}}\frac{\gamma_k}{16\sqrt M}
 |\ell+k,m-e_k\rangle
=
\frac{N}{16\sqrt{DM}}C^\dagger .
\]
Set
\[
\alpha_D=\frac{16\sqrt{DM}}N<32.
\]
An additional known dilution amplitude \(\alpha_D/32\) gives exactly the ideal block \(C^\dagger/32\).

This is a block encoding, not a successful-outcome operation. All failure flags and mode-label registers remain present. Reversing the **entire same circuit on the same banks** gives a block of \(C/32\). In that inverse, the deletion is undone before the input-dependent preparation is reversed.

In particular, this proves—not assumes—the uniform bound \(\|C\|\le32\).

---

## 2. Native \(\mathcal Q\), \(L\), and the rectangular row block

All terms of \(C\) lower the marker. Hence, on the valid sector,
\[
C^{D+1}=0,\qquad
\mathcal Q=e^C=\sum_{j=0}^{D}\frac{C^j}{j!}.
\]
The equality with the truncated multiplication operator follows because marker truncation is monotone: an intermediate term that crosses the boundary cannot later return.

Use the coefficients
\[
a_j=\frac{32^j}{j!},\qquad
\sum_{j=0}^D a_j\le e^{32}<3^{32}<S.
\]
Prepare selector probabilities \(a_j/S\). Split the remaining probability equally between \(+I\) and \(-I\), whose blocks cancel.

For a selected \(j\), apply \(j\) copies of the \(C/32\) block, using **distinct signal banks**. This is implemented compactly by \(D\) conditional block calls, with call \(h\) enabled when \(h\le j\). It does not enumerate mode words. Reversing the selector preparation gives
\[
\langle0|U_{\mathcal Q}|0\rangle=\mathcal Q/S .
\]

Taking all \(D\) terms makes this identity exact in the ideal-real circuit. A shorter, precision-dependent Taylor truncation is optional; it is unnecessary for polynomial cost in \(D,b\).

The diagonal operator satisfies
\[
D_{t/q}|\ell,m\rangle=t^{-2\ell}|\ell,m\rangle,
\qquad t^{-2\ell}<9.
\]
A calculated rotation therefore block-encodes it with normalization \(16\). Multiplying three blocks with separate factor banks gives
\[
\langle0|U_L|0\rangle
=\frac{\mathcal Q^\dagger D_{t/q}\mathcal Q}{16S^2}
=\frac L\Gamma .
\]
The adjoint factor uses the actual reversed \(U_{\mathcal Q}\) word. It is not an implementation of \(\mathcal Q^{-1}\).

For the row map, let \(P_0\) and \(P_+\) denote zero and positive marker. In normalized coordinates,
\[
I|\ell,m\rangle=|\ell+1,m\rangle .
\]
Thus
\[
A=P_0\mathcal QP_+I
\]
has a rectangular block of normalization \(S\). Marker tests and the shift are native reversible arithmetic. Equivalently, work first with the positive-marker embedding of the domain and undo the marker shift at the endpoint.

All coefficient lists here have polynomial length and polynomial-bit rational entries. Their preparation uses the same prefix-sum construction as above, not a state-preparation oracle.

---

## 3. Native inverse square root and rectangular polar isometry

Identify the input space \(Y=\Lambda_n\) with marker zero, and the output space \(X=\Lambda[w]_{n-1}\) with the positive-marker sector using \(I\). Write
\[
B=A^\dagger/S,\qquad H=B^\dagger B=AA^\dagger/S^2.
\]
Choose the known bound
\[
a=\min\!\left\{\frac12,\frac{\underline\chi(D,n)}{S^2}\right\}.
\]
Then \(aI\preceq H\preceq I\). For one circuit covering all \(n\ge1\), use the minimum of the supplied bounds over those degrees.

### The normalization-one complement block

Let \(U=U_{\mathcal Q}^\dagger\), and on its full registers define
\[
\mathsf P=|0_{\rm sig}\rangle\langle0_{\rm sig}|\otimes P_0,
\qquad
\mathsf Q=|0_{\rm sig}\rangle\langle0_{\rm sig}|\otimes P_+.
\]
Then \(\mathsf Q U\mathsf P\) is the embedded \(B\).

Add a flag \(z\), and implement
\[
F_{\mathsf Q}=(I-\mathsf Q)\otimes I_z+\mathsf Q\otimes X_z.
\]
Its zero-flag block is \(I-\mathsf Q\). Therefore
\[
\mathsf P U^\dagger(I-\mathsf Q)U\mathsf P
=I_Y-B^\dagger B=I_Y-H. \tag{1}
\]

Equation (1) uses a full unitary and its actual inverse on the **same** signal and marker banks. It is not multiplication of two independently allocated block encodings. The success predicate is just zero-signal and positive-marker testing.

For powers of \(R:=I-H\), use fresh complete banks for each factor. In particular, because this block acts on Fock input \(Y\), its temporary marker belongs to its signal bank. **Reusing that marker across factors would allow rejected paths to return and would not encode \(R^j\).**

This supplies \(R\) with normalization one, avoiding the \(2^j\) normalization from a naïve two-term LCU.

### Binomial filter

Let
\[
c_j=\frac{\binom{2j}{j}}{4^j},\qquad
q_K(x)=\sum_{j=0}^K c_j(1-x)^j,\qquad
s_K=\sum_{j=0}^K c_j\le K+1.
\]
For \(a\le x\le1\),
\[
0\le1-\sqrt{x}\,q_K(x)
\le \frac{(1-x)^{K+1}}x
\le \frac{e^{-a(K+1)}}a. \tag{2}
\]
Choose
\[
K=O\!\left(a^{-1}\log\frac1{a\delta}\right)
\]
using an explicit integer upper bound, so the last expression is at most \(\delta\).

A compact LCU over powers of the normalization-one block (1), followed by \(B\), gives
\[
\frac{Bq_K(H)}{s_K}.
\]
The inverse-root approximation is \(S^{-1}q_K(H)\), and
\[
Bq_K(H)=V\,t_K(H),\qquad
V=A^\dagger(AA^\dagger)^{-1/2},
\]
where \(1-\delta\le t_K(x)=\sqrt{x}q_K(x)\le1\).

The temporary LCU normalization \(s_K\) is **not** treated as a constant. It is paid and removed next. A fixed normalization for the bare inverse square root would generally be impossible as \(\chi_{\min}\to0\).

### Known-angle rectangular amplification

Set
\[
m=4(K+1),\qquad
\theta_*=\frac{\pi}{4m+2},\qquad
d=s_K\sin\theta_*<\frac{\pi}{16}.
\]
Dilution by the calculated amplitude \(d\) gives a unitary \(W\) whose rectangular block is
\[
\sin\theta_*\,Vt_K(H).
\]

Let \(\Pi_i,\Pi_o\) be its known input and output success projectors: all private banks zero, with the distinguished marker respectively zero and positive. Put \(R_i=I-2\Pi_i\), \(R_o=I-2\Pi_o\), and apply
\[
\mathcal A_m=(-W R_i W^\dagger R_o)^mW. \tag{3}
\]
All inverses in (3) reverse the same compiled word and banks.

Two-projector algebra gives, in a singular channel \(x\),
\[
\Pi_o\mathcal A_m
=
V\sin\!\left((2m+1)
 \arcsin(t_K(x)\sin\theta_*)\right).
\]
Writing the sine as \(\cos\Delta_x\),
\[
0\le\Delta_x
\le(2m+1)\tan\theta_*\,\delta
\le\pi\delta.
\]
Unitarity now bounds the **entire output**, including rejected banks:
\[
\|\mathcal A_m|\psi,0\rangle-|V\psi,0\rangle\|
\le\pi\delta. \tag{4}
\]
This is an operator-norm bound, not a success-conditioned estimate. It also fixes the positive phase. No singular value, eigenvector, or \(\chi_\lambda\) is supplied to the circuit.

Finally decrement the distinguished positive marker by one to undo the embedding \(I\). The circuit uses \(O(K^2)\) calls to \(U_{\mathcal Q}\) or its inverse. Since \(a^{-1}=\operatorname{poly}(D)\), this is polynomial in \(D,\log(1/\delta)\).

Its actual inverse implements \(V^\dagger\) on the ideal range with the same clean error: this follows directly by applying the circuit’s inverse to both sides of (4). No stronger off-range promise is needed.

---

## 4. Paid native simulation of \(L\)

Here is an elementary simulator from the \(L/\Gamma\) block, without QSVT.

For a requested time \(\tau\), choose a known integer
\[
R_{\rm seg}\ge 8\Gamma|\tau|,
\]
using a rational upper bound on \(|\tau|\), and let \(\Delta=\tau/R_{\rm seg}\). For \(x=\Gamma|\Delta|\le1/8\), a compact Taylor LCU has block
\[
\frac{T_J}{2},\qquad
T_J=\sum_{j=0}^J\frac{(i\Delta L)^j}{j!}.
\]
Use probabilities \(x^j/(2j!)\), phases \((i\,\mathrm{sign}\Delta)^j\), fresh block signals for powers, and equal \(+I,-I\) padding. The tail obeys
\[
\|T_J-e^{i\Delta L}\|\le8^{-J}.
\]

For any unitary block \(W\) with compression \(B\), the cubic amplification word has compression
\[
3B-4BB^\dagger B.
\]
If \(\|B-U/2\|\le\beta\) for unitary \(U\), its projected error is at most \(15\beta\), and its full clean-isometry error is at most \(\sqrt{30\beta}\). Thus taking, for example,
\[
J=\left\lceil\log_2\frac{64R_{\rm seg}^2}{\rho^2}\right\rceil
\]
makes the ideal-real complete simulation error less than \(\rho/2\). Finite-gate rounding receives the remaining budget.

Different segments may use fresh complete banks; all are retained. Each segment’s internal inverse uses its original banks. The inverse of the whole simulator is its literal reversed word. Controlled versions retain all scalar phases, including the minus signs in amplification.

This guarantee holds on the **whole valid degree sector**, with arbitrary logical controls—not merely on a selected eigenspace.

---

## 5. Clean readout of the integer \(k\), without exact-grid QPE

The spectral interface and the specialization give explicit bounds:
\[
\frac13<t^D\le t^k\le t^{-3D}<27.
\]
For adjacent exponents in the allowed range,
\[
t^k-t^{k+1}=\frac{t^k}{N}>\frac1{3N}. \tag{5}
\]
Thus the distinct spectral values have a known inverse-polynomial gap.

Use QPE on
\[
U=e^{2\pi iL/128},
\]
with \(Q=2^h\) the least power of two satisfying \(Q\ge2^{17}N\).

For an ideal QPE outcome \(y\), let \(d_y\) be its cyclic distance, in grid bins, from \(Q\lambda/128\). The geometric-sum formula gives
\[
\Pr(y)\le\frac1{4d_y^2}.
\]
Summing this tail shows that \(d_y<16\) with probability at least \(15/16\). On that event,
\[
\left|\frac{128y}{Q}-\lambda\right|
<\frac{128\cdot16}{Q}
\le\frac1{64N},
\]
which is less than one quarter of the gap (5). The spectral interval is also far enough from phase wraparound for this good event.

Reversibly classify \(128y/Q\) by the nearest member of
\[
\{t^k:-3D\le k\le D\}.
\]
These are explicit rationals of \(O(D\log(D+1))\) bits. A charged linear scan or reversible binary search computes the nearest value and its integer \(k\); no logarithm oracle or eigenvalue table is supplied.

Run an odd number \(r\) of independent coherent QPE estimators and compute their majority label. Conditional on each eigenspace, the ideal outcome distributions are independent. A simple union bound gives
\[
\Pr(\text{wrong majority})
\le 2^r(1/16)^{r/2}\le2^{-r}.
\]

Let \(E\) denote this coherent estimation and majority computation. Perform
\[
E,\quad \text{copy the majority label to the output},\quad E^\dagger.
\]
The last operation is the **actual reverse circuit**, including all simulation banks.

For an eigenvector with correct label \(k\), before the reverse computation the bad component has squared norm at most \(2^{-r}\). Comparing the copied label with a fixed copy of \(k\) gives
\[
\bigl\|E^\dagger\mathrm{COPY}\,E|\psi,0,0\rangle
      -|\psi,0,k\rangle\bigr\|
\le \sqrt{2\,2^{-r}}. \tag{6}
\]
Orthogonality of spectral subspaces makes (6) uniform on superpositions, degeneracies, and reference systems. There is no dimension factor.

For \(\epsilon=2^{-b}\), \(r=2b+9\) makes this ideal estimation error at most \(\epsilon/16\). Allocate \(O(\epsilon/[r(h+1)])\) to each controlled simulation and charge the QFT rotations in the finite-gate budget below.

Crucially:

* \(h=O(\log D)\);
* the largest simulated time \(2\pi2^{h-1}/128\) is \(O(D)\);
* confidence is increased by \(O(b)\) repetitions, **not** by an exponentially fine grid.

The result is an \(\epsilon\)-clean integer-label readout with polynomial cost in \(D,b\). “Clean” is approximate in joint norm; finite approximate QPE does not erase erroneous components exactly. A content reflection is then readout, integer equality phase, and actual inverse readout, with the same workspace accounting.

---

## 6. Finite gates, precision, and complete cost accounting

### No unit-cost calculated rotations

Fix once a finite palette containing
\[
H,S,X,Z,\mathrm{CNOT},\mathrm{Toffoli},
\text{ controlled-}H,\text{ controlled-}S.
\]
Higher controls use reversible AND computation.

Every calculated real rotation has the form
\[
U_{\rm rot}=cI+sJ,\qquad J=XZ,
\]
and a calculated scalar phase uses \(J=iI\). Compute \(c,s\) to \(p\)-bit absolute accuracy. With a uniform \(p\)-qubit Hadamard seed, assign even integer counts approximating
\[
2^{p-1}|c|,\qquad 2^{p-1}|s|
\]
to the appropriately signed \(I,J\) branches. Split the remaining count equally between \(I,-I\). For sufficiently large fixed minimum \(p\), the counts fit because \(|c|+|s|\le\sqrt2\).

Binary threshold comparisons implement this selector; \(2^p\) labels are **not enumerated**. Its block differs from \(U_{\rm rot}/2\) by \(O(2^{-p})\). One cubic amplification therefore implements the rotation with full clean error
\[
O(2^{-p/2}),
\]
using only the fixed palette and reversible arithmetic. This bottom compiler invokes no further calculated rotations. Its inverse is its exact reversed gate word.

### Polynomial arithmetic

The required data have polynomial bit clocks:

* \(t^k,q^k,w_k^2,\gamma_k^2\): \(O(D\log(D+1))\)-bit rationals;
* \(32^j/j!\), \(j\le D\): polynomial-bit rationals;
* \(c_j\), \(j\le K\): \(O(K)\)-bit rationals;
* the readout comparison grid: \(O(D)\) explicit polynomial-bit rationals.

Division and square roots use finite integer algorithms. Sine, cosine, and \(\pi\) for the known amplification/QFT angles can be computed by convergent elementary series. Absolute square-root accuracy is obtained with sufficient doubled input precision. Zero denominators in empty preparation prefixes are explicitly bypassed. All table construction and controlled access are charged; no QRAM is assumed.

### Noncircular precision allocation

First choose the ideal finite schedules: \(K,m,r,h,R_{\rm seg},J\). Unroll a polynomial bound \(T\) on their calculated rotation/phase occurrences, including inverse occurrences. **Then** choose
\[
p=O\!\left(\log T+\log(1/\epsilon)\right)
\]
with a sufficient fixed constant so their total clean error is within the remaining budget. Coefficient arithmetic uses the additional polynomial guard bits described above.

The bound \(T\) is fixed before bottom precision is selected. Exact Boolean arithmetic introduces no additional approximation error.

The workspace rules are:

* Separate algebraic factors in a power receive separate complete signal banks.
* Every occurrence of a specified unitary’s inverse reverses that same compiled word on the same banks.
* Lower-level rotation guarantees hold for all logical inputs, including dirty upper signal/control states.
* A unitary hybrid argument compares against zero lower workspace in the ideal reference circuit. It never assumes actual leaked workspace has reset.

This pays amplification on dirty upper signals and all inverse calls.

For example, the polar circuit uses \(O(K^2)\) \(\mathcal Q\)-block calls, each containing \(O(D)\) \(C\)-block calls. The readout uses
\[
O\!\left(r(\Gamma N+\log N)J\right)
\]
\(L\)-block calls. Since \(\Gamma,S\) are fixed constants and \(a^{-1}\) is supplied as polynomial, classical compilation, reversible arithmetic, gates, and retained workspace are all \(\operatorname{poly}(D,b)\).

All auxiliary preparations above start from zero and are included in these counts. Preparing an arbitrary externally supplied logical input remains an additive, charged cost. The native output has occupation/marker size \(O(D\log D)\), and the content label has \(O(\log D)\) bits; no classical amplitude-list output is claimed.

---

## Scope and falsifiers

The native construction is established under the two stated interfaces. Its decisive compression identities are the deletion block and
\[
\mathsf P U^\dagger(I-\mathsf Q)U\mathsf P=I-B^\dagger B.
\]
Fresh inverse banks, or recycled auxiliary markers inside powers, invalidate these identities and are exact implementation falsifiers.

The remaining external obligations are the specialized algebraic/spectral identities and an explicit valid \(\underline\chi\). A failure of either invalidates the corresponding conditional polar/readout claim. This proof does **not** certify specialized branching, transition overlaps, the full transform, classical hardness, or a speedup. No finite examples or failed attacks are used as evidence for those claims.