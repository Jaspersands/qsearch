## Verdict

**The erasure composition is sound as a theorem-relative algorithm in the stated native oracle model.** IS Theorem 3 applies to arbitrary coefficient matrices, including adaptively generated ones; no random-column promise is needed.

There is one certification limitation: the supplied excerpt does not give the numerical bit-time exponent of its SDE implementation. Below I expose that dependency explicitly. Thus the argument establishes polynomial-time existence and a total-clock formula, **not an already instantiated numerical circuit certificate**. Inventing an exponent for the published implementation would not complete the audit.

### 1. Required oracle interface and initial failure checks

Require the clean, deterministic evaluation oracle
\[
O_f:|g,z\rangle\longmapsto |g,z\oplus f(g)\rangle,
\]
where \(g\) uses the supplied BCH coordinates and \(f(g)\) is a \(b\)-bit label.

Charge \(b\), the \(D\log p\)-bit argument, public-table access, reversible lifts, and each oracle call. The stated native BIT bound requires \(b\) to be polynomially bounded in the native input size; otherwise the bound must include \(b\). If an oracle implementation costs \(T_f\) gates, add \(T_f\) times the query count below.

For a computable restriction or the single normalizer quotient, prepare a fresh uniform coordinate state and evaluate \(f\) through its public lift. No controlled phase oracle, hidden basis, or restriction of a frozen state bank is required.

Three potential failures must be excluded explicitly:

* Oracle-label registers must be **traced out**, not retained as conditioning records for the mixed-state invariant.
* Every erasure node must have a nonempty set of nonzero scales.
* Different descent charts must never contribute packets to the same tree.

These are implementation requirements, not consequences of finite controls.

### 2. One common potential and the actual oracle source

After learning \(K\), taking its normalizer, and quotienting there, consider a transverse instance:
\[
N=[L,L],\qquad V=L/N,\qquad H\cap\exp N=1.
\]
Transversality and metabelianness imply that \(H\) is abelian. Write
\[
\log H=\{u+a(u):u\in U\}
\]
for an unknown subspace \(U\le V\) and unknown linear \(a:U\to N\).

Fix, **for the proof only**, a linear projection \(\pi:V\to U\). Put
\[
u=\pi(q),\quad r=q-u,\qquad
Q(q)=\log\!\left(\exp(r)\exp(u+a(u))\exp(-q)\right).
\]
This lies in \(N\). Expanding in Lie words, every surviving word has length at most \(c\), and its arguments are linear in \(q\). Hence
\[
\deg Q\le c.
\]
This is a structural BCH deduction, not interpolation; nested written expressions do not create surviving degree-\(c^2\) terms. Their denominators are invertible because \(p>c\).

Since \(\exp(Q(q))\exp(q)=\exp(r)h(u)\), for \(v\in U\),
\[
\exp(q)h(v)=\exp(Q(q+v)-Q(q))\exp(q+v).
\]
Here the subtraction is justified by abelianness of \(N\), not by commuting quotient lifts.

Let \(a_0=|V|\), \(b_0=|N|\), and discard the oracle-label register after a uniform query. The resulting group state is
\[
\frac1{|G|}\sum_{g\in G,h\in H}|g\rangle\langle gh|.
\]
In normal-first coordinates its terms are
\[
\frac1{a_0b_0}\sum_{n,q,v\in U}
 |n,q\rangle
 \langle n+Q(q+v)-Q(q),q+v|.
\]
Fourier transform \(N\), using positive characters, and measure its character \(\lambda\). Summation over \(n\) kills unequal character indices. Consequently
\[
\Pr[\lambda]=b_0^{-1},\qquad
\rho_\lambda[q,q']
 =a_0^{-1}\mathbf1_{q'-q\in U}
   \omega^{\lambda(Q(q)-Q(q'))}.
\]
Thus the retained quotient state is exactly \(\rho(U,\lambda Q)\), including when \(\lambda=0\).

The controller retains \(\lambda\), not the original oracle label. Fresh preparations give independent copies conditional on the current public chart and prior controller history.

### 3. Independent reconstruction of the complete instrument

Let \(A=\mathbb F_p^m\), \(a_0=|A|\), and
\[
\rho(U,P)=a_0^{-1}
 \sum_{x'-x\in U}\omega^{P(x)-P(x')}|x\rangle\langle x'|.
\]
Take \(k\) independent such inputs with phases \(P_i\), and public scales \(s_i\), not all zero.

Append \(a_0^{-1/2}\sum_x|x\rangle\), subtract \(s_i x\) from input \(i\), and measure the old registers. For outcome \(y=(y_1,\ldots,y_k)\),
\[
K_y=a_0^{-1/2}\sum_x
 |x\rangle\langle y_1+s_1x,\ldots,y_k+s_kx|.
\]
This uses only public arithmetic and a fresh uniform register.

Output-basis orthogonality gives
\[
K_y^\dagger K_y
 =a_0^{-1}\sum_x|y+s x\rangle\langle y+s x|.
\]
For each fixed \(x\), summing over \(y\) gives the input identity. Therefore
\[
\sum_yK_y^\dagger K_y=I.
\]

Define \(P_y(x)=\sum_iP_i(y_i+s_i x)\). Direct multiplication gives
\[
\begin{aligned}
&\left[K_y\Bigl(\bigotimes_i\rho(U,P_i)\Bigr)K_y^\dagger\right]_{x,x'}\\
&\quad=a_0^{-(k+1)}
 \prod_i\mathbf1_{s_i(x'-x)\in U}\,
 \omega^{P_y(x)-P_y(x')}\\
&\quad=a_0^{-k}\rho(U,P_y)[x,x'].
\end{aligned}
\]
The last equality uses one nonzero scale and linearity of \(U\). Hence
\[
\Pr[y]=a_0^{-k}
\]
for **every** outcome tuple. There is no postselection loss.

Zero-scale inputs can instead be discarded; their constant phase contributions disappear. They are nevertheless consumed and charged. All-zero scales do not preserve the desired invariant and are rejected.

The correct retained-record invariant is a cq state
\[
\sum_r p_r|r\rangle\langle r|
 \otimes\bigotimes_i\rho(U,P_{r,i}),
\]
where \(r\) contains characters, instrument outcomes, scales, and controller randomness. Applying the preceding identity separately for each \(r\) preserves this form. Adaptive packet selection does not spoil conditional independence when trees are disjoint.

**Important falsifier:** conditioning additionally on original oracle labels generally changes the inputs to fixed pure cosets. For \(U=0\), two fixed basis inputs and scales \(1,1\) permit only outcomes satisfying one affine relation. Their outcome law is not \(a_0^{-2}\). The compiler above avoids this error by discarding those labels.

### 4. Formal cancellation, without learning \(Q\)

Use one parameter vector for the common \(N\)-valued polynomial:
\[
\theta_{a,\alpha},\qquad
1\le a\le n,\quad 1\le|\alpha|\le c,\qquad
M=n\!\left(\binom{m+c}{c}-1\right).
\]
There is one \(Q\) per fixed ambient chart, not an unrelated unknown polynomial for each packet.

Represent every packet by a public coefficient map
\[
P_i(x)\equiv
 \sum_{\theta,\beta\ne0}C_i[\theta,\beta]\theta\,x^\beta
 \pmod{\text{constants}}.
\]
Initially,
\[
C_i[(a,\alpha),\beta]=\lambda_{i,a}\mathbf1_{\alpha=\beta}.
\]
Translation, scaling, and addition update this map using only public records.

At stage \(j=c,c-1,\ldots,1\), input maps have formal degree at most \(j\). Form a row for **every parameter** and **every degree-\(j\) monomial**:
\[
\sum_{i=1}^k C_i[\theta,\beta]s_i^j=0,
\qquad |\beta|=j.
\]
There are
\[
E_j=M\binom{m+j-1}{j}
\]
rows. Translation does not affect the leading homogeneous part, so a nonzero SDE solution cancels degree \(j\) for every assignment of \(\theta\).

This is stronger than cancellation merely for realizable hidden potentials. No knowledge of \(U,\pi,a,Q\), and no statistical assumption on the columns, enters the solver.

For \(j=1\), use ordinary linear dependence with \(E_1+1\) columns.

Reading the supplied Theorem 3 bound as
\[
k>j^{\,j^2\log j}(E+1)^{j\log j},
\]
the conservative integer arities
\[
A_1(E)=E+1,\qquad
A_j(E)=1+j^{j^3}(E+1)^{j^2}\quad(j\ge2)
\]
suffice. They dominate the displayed bound for the usual logarithm conventions.

The theorem’s input is an arbitrary known coefficient matrix. Conditioning on any controller history produces another such matrix; adaptivity introduces no new applicability condition.

Verify every returned scale vector exactly: nonzero and satisfying all rows. On failure, abort or use the bounded retry policy below.

A disjoint tree uses at most
\[
L=\prod_{j=1}^c A_j(E_j)
\]
fresh oracle sources. After stage one the packet is \(\rho(U,0)\). Its Fourier measurement is uniform on \(U^\perp\), conditional on every retained pre-Fourier record.

### 5. Explicit dimension and source exponents

Set
\[
x=D+1,\quad B=\binom{D+c}{c},\quad Z=xB^2.
\]
Then
\[
M\le DB,\qquad E_j\le Z,\qquad
Z\le(c+1)^{2c}x^{2c+1}.
\]
One packet’s full coefficient map has at most \(Z\) field entries.

Define
\[
S_c=\sum_{j=1}^c j^2=\frac{c(c+1)(2c+1)}6,\quad
\beta_c=(2c+1)S_c,\quad
\nu_c=(2c+1)c^2.
\]
Explicitly,
\[
L\le K_c x^{\beta_c},\qquad
A_{\max}\le K'_c x^{\nu_c},
\]
where one valid leaf constant is
\[
K_c=[2(c+1)^{2c}]^{S_c}
       \prod_{j=2}^c(1+j^{j^3}).
\]
Thus no \(c^D\) dependence is concealed in the source arity.

There are at most \(cL\) nodes or packet incidences up to a degree-dependent constant. Expanding a degree-\(c\) monomial under \(y+s x\) produces at most \(2^c\) terms. Consequently all map updates in one tree cost at most \(C_cLZ\) field operations, including row formation.

### 6. Bounded group control and oracle count

Use fixed rank budgets. With \(t\) independent uniform samples from a subspace of \(\mathbb F_p^d\), failure to span is at most \(p^{d-t}\).

Choose
\[
h=\left\lceil\log_2\frac{16(c+2)}\eta\right\rceil+2,
\qquad t=D+h.
\]
Use at most \(t\) samples for the initial intersection, each descent level, and the terminal abelian HSP.

For the initial intersection, measuring \(q\) gives normal differences in \(\Phi(q)K\); apply the full truncated \(\Phi(-q)\), not its first-order truncation. Exact samples give \(\widehat K\supseteq K\); original-oracle membership checks then certify equality.

Use the audited normalizer and quotient only after that certification. Later groups are direct restrictions inside this one quotient.

At a nonabelian level, the erased samples give \(\widehat U\supseteq U\) in the ideal algorithm. Accept its public preimage only after a strict class decrease. Exact recovery of \(U\) is a sufficient fallback because
\[
(HN)'=[H,N]\le\gamma_3(S),\qquad
\gamma_j(HN)\le\gamma_{j+1}(S).
\]
There are at most \(c-1\) nonabelian restrictions, even with early stopping at a strict overestimate.

The raw-source count is bounded by
\[
N_{\rm src}\le(c-1)tL+2t.
\]
Including intersection and terminal membership checks,
\[
N_f\le(c+1)t(L+1)+2D+2.
\]
This is a **sum across descent levels**, not a recursive product of oracle-source costs. No packet crosses a chart change.

### 7. Finite-bit classical and quantum implementation

Read the expanded structure table, costing at least its input length \(I_{\rm in}\). Public brackets, BCH evaluation, basis changes, normalizers, quotient tables, and class tests admit a conservative \(C_cD^6\) field-operation bound per public reconstruction/test. Table access is charged; no QRAM is assumed.

Schoolbook modular arithmetic and extended Euclid give polynomial bit costs in
\(\ell=\lceil\log_2p\rceil\). Reversible straight-line arithmetic can retain and uncompute intermediates with polynomial gates and workspace.

For the SDE module, expose the required implementation contract:
\[
T_{{\rm SDE},j}(k,\ell,\zeta)
 \le a_c\bigl(k+\ell+\lceil\log_2(1/\zeta)\rceil+1\bigr)^{\kappa_c},
\]
uniformly over all its coefficient matrices; a returned answer is exact, and abort probability is at most \(\zeta\). Here \(a_c,\kappa_c\) are fixed compiler constants.

The supplied theorem states deterministic polynomial time, so its literal implementation needs no failure allowance. If power decomposition is implemented randomly instead, roots and nonresidues are not free:

* For \(e=\gcd(j,p-1)\), only prime factors of the fixed integer \(j\) are needed—not a factorization of \(p-1\).
* Sampling and testing a generator of the \(e\)-power-class quotient succeeds with probability at least \(1/e\).
* Known-power roots can then be extracted using the relevant small-prime-power components; their digitwise logarithms have \(O(\ell)\) digits, with bounded-size digit searches.
* These operations have polynomial bit cost in \(\ell\); cap rejection/nonresidue searches at \(C_c\log(R/\zeta)\) trials for \(R\) requests. Failure means ABORT.

This describes how to charge such arithmetic, not a replacement for the published SDE algorithm. Its actual implementation certificate must instantiate \(a_c,\kappa_c\).

Finite-gate uniform preparation and prime-field QFTs also need no exact-angle primitive. One explicit route is:

1. Prepare \(|\mathbb F_p\rangle\) by binary-interval rotations, computing conditional interval sizes reversibly.
2. Prepare a Fourier eigenstate using modular products and controlled phases.
3. Erase its index by coherent phase estimation of the modular shift and rounding.
4. Use \(\ell+O(\log(1/\epsilon))\) estimation bits; the wrong-rounding tail is \(O(p/2^s)\).
5. Compute angles to finite precision and synthesize rotations over a fixed universal gate set.

Schoolbook arithmetic, elementary-function approximation and standard gate synthesis allow a deliberately loose bound \(C(\ell+\log(1/\epsilon)+1)^{20}\) per coordinate primitive. All ancillas and synthesis computation are charged.

### 8. A total-clock formula and adaptive approximation proof

Let
\[
\Gamma=b+\ell+h+\lceil\log_2x\rceil+1.
\]
With the SDE contract above, a conservative overall bound is
\[
\boxed{
T\le I_{\rm in}
 +C_c\,x^{\,\beta_c+\nu_c\kappa_c+2c+12}
             \Gamma^{\,\kappa_c+25}.
}
\]
It bounds classical bit operations, non-oracle gates, fresh-register preparation, and a safe workspace bound. Retaining all public maps and transcripts is still within this clock. Output costs \(O(D^2\ell)\) bits.

The constants include the fixed BCH tables, SDE implementation, and gate compiler—not any hidden subgroup data. For \(c=1\), use the abelian algorithm directly.

Allocate solver failure \(\eta/(16(N_{\rm nodes}+1))\) per call. Allocate uniform diamond-norm error \(\eta/(32B_{\rm q})\) per quantum preparation/Fourier block, where \(B_{\rm q}\) is the explicit polynomial block cap. Required precision is
\[
O_c(\ell+h+\log(D+1)+\log(h+1)),
\]
not polynomial in \(1/\eta\).

Every controller branch has fixed caps, valid-range checks, and an ABORT exit. Pad halted branches with no-ops. For each classical history \(r\), implement the selected quantum block with the same uniform diamond-error bound. The controlled cq channel then has that bound as well.

Telescoping the padded channels gives
\[
\|\mathcal E_{\rm real}-\mathcal E_{\rm ideal}\|_\diamond
 \le \sum_{\text{blocks}}\epsilon_{\text{block}}.
\]
This comparison is **unconditioned**. It never divides by an exponentially small instrument-branch probability.

In the ideal algorithm, union bounds cover rank-cap failure and bounded classical searches; every non-aborting output is correct. The hybrid transfers its success probability to the real algorithm, yielding error at most \(\eta\).

On approximation-error branches, neither \(\widehat U\supseteq U\) nor preservation of \(H\) is asserted. A noisy class decrease and terminal membership checks can indeed accept a proper subgroup. The global hybrid—not an invalid noisy-containment argument—controls that event.

### 9. Scope and remaining certificate

The append–shear–measure operation is the known Decker–Høyer–Ivanyos–Santha phase-linearization primitive. The mixed unknown-support cq identity above is the additional argument needed here; no novelty claim follows.

The supplied HPGP theorem is univariate, and the supplied HSP application concerns the specified semidirect products and subgroup family. Neither directly proves this native arbitrary-\(H\), growing-\(D\) result. Only Theorem 3’s arbitrary-matrix SDE guarantee is imported into the controller.

**Remaining numerical proof obligation:** attach the actual finite-bit SDE implementation and its certified \(a_c,\kappa_c\), together with the oracle label-width contract. Without them, these files do not constitute a fully instantiated numerical compiler artifact. That incompleteness is not a mathematical counterexample to the composition.

A failure of arbitrary-row applicability, a nonpolynomial root routine, conditioning on discarded oracle labels, or cross-chart packet reuse would invalidate the corresponding proof step. Finite controls, internal status, and failed attacks establish none of those universal obligations and imply no hardness, novelty, or useful nonoracle application.