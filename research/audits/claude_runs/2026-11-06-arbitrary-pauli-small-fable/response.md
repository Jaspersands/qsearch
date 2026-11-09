# Audit report: small-$w$ Bell-support anti-concentration constant

**Verdict up front.** No flaw found. Every step of the proposed bound checks out as a proof (not an assumption), with two cosmetic over-statements that do not affect validity. The lemma delivers an absolute constant $\gamma \ge 2^{-2368}$ (tightenable to $2^{-1186}$ with no new ideas), uniform in $n$, $w\le 24$, $P$, $C$. It is a fully paid $n$-independent constant for the single purpose stated (support-testing degree-$\le 2$ Bell relations). What it does *not* pay is listed at the end.

---

## 1. Arithmetic placement (proved)

$K=\mathbb{Q}(\zeta_{16})$, $\zeta=e^{i\pi/8}$, $[K:\mathbb{Q}]=\varphi(16)=8$. ✓

- $\cos(\pi/8)=(\zeta+\zeta^{-1})/2$, $\sin(\pi/8)=(\zeta-\zeta^{-1})/(2\zeta^4)$, $-i\sin(\pi/8)=-(\zeta-\zeta^{-1})/2$: all in $\tfrac12\mathcal{O}_K$. ✓ (They are not in $\mathcal{O}_K$: $\cos(\pi/8)$ has minimal polynomial $8x^4-8x^2+1$, so the factor $\tfrac12$ is genuinely needed and correctly carried.)
- $\sqrt2=\zeta^2+\zeta^{-2}\in\mathcal{O}_K$, so $2^{-w/2}=(\sqrt2)^w 2^{-w}\in 2^{-w}\mathcal{O}_K$ for every parity of $w$. ✓
- $(H^{\otimes w})_x\in 2^{-w}\mathcal{O}_K$; $P$ has entries in $\{0,\pm1,\pm i\}\subset\mathcal{O}_K$; so $\phi=\cos(\tfrac\pi8)H^{\otimes w}-i\sin(\tfrac\pi8)PH^{\otimes w}\in 2^{-(w+1)}\mathcal{O}_K$. ✓
- $W_v=i^{x\cdot z}X^xZ^z$ has entries in $\{0,\pm1,\pm i\}$, so $\phi^TW_v\phi\in 2^{-2(w+1)}\mathcal{O}_K$ and $\beta_v\in 2^{-(3w+2)}\mathcal{O}_K$. ✓

## 2. Transpose / conjugation (proved, and the proposal is right to use the transpose)

With $|\Phi_v\rangle=(W_v\otimes I)|\Phi^+\rangle$, $|\Phi^+\rangle=2^{-w/2}\sum_x|x\rangle|x\rangle$:
$$\langle\Phi_v|\phi\otimes\phi\rangle = 2^{-w/2}\sum_x (W_v^\dagger\phi)_x\phi_x = 2^{-w/2}\,\phi^T W_v\phi$$
(using $W_v^\dagger=W_v$). The amplitude is **bilinear**, not sesquilinear, in the copy entries, hence a polynomial over $K$ in the entries of $\phi$ with no complex conjugation. Therefore for every embedding $\sigma$ of $K$, $\sigma(\beta_v)=\sigma(2^{-w/2})\,\sigma(\phi)^T\sigma(W_v)\sigma(\phi)$ with $\sigma$ applied entrywise. This is the step that makes the Galois argument legitimate.

(Remark: even if one had written $\beta_v$ with a bar, $K/\mathbb{Q}$ is abelian, so complex conjugation $\sigma_{-1}$ commutes with every $\sigma_k$; the argument would still go through. Not needed here.)

## 3. Field-embedding assertions (proved, slightly over-stated)

Embeddings are $\sigma_k:\zeta\mapsto\zeta^k$, $k\in\{1,3,\dots,15\}$. Direct computation:

- $\sigma_k(\cos\tfrac\pi8)=\cos\tfrac{k\pi}8$; $\sigma_k(\sin\tfrac\pi8)=i^{\,1-k}\sin\tfrac{k\pi}8=\pm\sin\tfrac{k\pi}8$ ($k$ odd). So $\sigma_k(H)$ is a **real unit vector**. ✓
- $\sigma_k(i)=i^k=\pm i$, so $\sigma_k(P)\in\{P,\bar P\}$; $\bar P$ is $P$ with every $Y$ factor sign-flipped, still a signed Hermitian Pauli, $\sigma_k(P)^2=I$. $\sigma_k(-i\sin\tfrac\pi8)=-(\zeta^k-\zeta^{-k})/2=-i\sin\tfrac{k\pi}8$. Hence
$$\sigma_k\!\big(e^{-i\pi P/8}\big)=\cos\tfrac{k\pi}8\,I-i\sin\tfrac{k\pi}8\,\sigma_k(P)=e^{-ik\pi\sigma_k(P)/8},$$
a unitary. ✓ ("Pauli phases" in the proposal should be read as "possibly $P\mapsto\bar P$"; harmless.)
- $\sigma_k(\sqrt2)=2\cos\tfrac{k\pi}4=\pm\sqrt2$, so $|\sigma_k(2^{-w/2})|=2^{-w/2}$; $\sigma_k(W_v)\in\{W_v,\bar W_v\}$ is unitary.

Hence $\sigma_k(\phi)=\sigma_k(R)\,\sigma_k(H)^{\otimes w}$ is a unit vector and, by Cauchy–Schwarz ($|\psi^TU\psi|=|\langle\bar\psi,U\psi\rangle|\le1$),
$$|\sigma_k(\beta_v)|\le 2^{-w/2}\le 1 .$$
The proposal's "$\le1$" is therefore correct (and loose by $2^{-w/2}$ per conjugate).

## 4. Norm inequality (proved)

Let $\alpha=2^{3w+2}\beta_v\in\mathcal{O}_K$, $\alpha\neq0$. Then $N_{K/\mathbb{Q}}(\alpha)=\prod_{k}\sigma_k(\alpha)\in\mathbb{Z}\setminus\{0\}$, so
$$1\le|\alpha|\prod_{k\neq1}|\sigma_k(\alpha)|\le|\alpha|\,2^{7(3w+2)}\ \Rightarrow\ |\beta_v|=2^{-(3w+2)}|\alpha|\ge 2^{-8(3w+2)},$$
$$\nu_\phi(v)=|\beta_v|^2\ge 2^{-16(3w+2)}\ge 2^{-1184}\quad(w\le24).\ ✓$$
(Using $|\sigma_k(\alpha)|\le 2^{3w+2-w/2}$ instead gives $\nu_\phi(v)\ge 2^{-16(3w+2)+7w}\ge2^{-1016}$; not needed.)

Sanity control: $w=1,P=Z$ gives $\nu(I)=3/8$, consistent.

## 5. Inactive factor (proved)

$\nu_H=(\tfrac12,\tfrac14,\tfrac14,0)$ on $(I,X,Z,Y)$ since $H^TXH=\sin\tfrac\pi4$, $H^TZH=\cos\tfrac\pi4$, $H^TYH=0$. Minimum nonzero probability $1/4$. ✓

## 6. Clifford invariance and degree (proved)

$C^{\otimes2}$ permutes the Bell basis up to phase: Bell states are the nondegenerate joint eigenbasis of $\{W_a\otimes W_a\}$ with eigenvalue $(-1)^{[a,v]+y(a)}$, $y(a)=x_a\!\cdot\! z_a$; $C$ acts by a symplectic $S$ on labels, and $y\circ S^{-1}+y$ has vanishing polar form (both polar forms equal $[\cdot,\cdot]$), hence is linear and absorbable into a translation. So $v\mapsto Sv+c$ is an invertible affine map of $\mathbb{F}_2^{2n}$: support probabilities are transported exactly and Boolean degree is preserved under affine substitution. ✓ The global Bell distribution of $(\phi\otimes H^{\otimes(n-w)})^{\otimes2}$ factorizes as $\nu_\phi\otimes\nu_H^{\otimes(n-w)}$. ✓ A degree-$\le2$ polynomial in the $2n$ bits touches at most two bits per monomial, hence at most two blocks under the regrouping. ✓

## 7. Product anti-concentration (proved explicitly)

**Lemma.** Let $\mu=\mu_1\otimes\cdots\otimes\mu_m$ on $S=S_1\times\cdots\times S_m$, $p=\min_i\min_{s\in S_i}\mu_i(s)$. If $f:S\to\mathbb{F}_2$ is a sum of functions each depending on $\le d$ blocks and $f\not\equiv0$ on $S$, then $\mu(f=1)\ge p^d$.

*Proof.* Induct on $(d,m)$; $d=0$ or $m=0$: $f\equiv1$. Pick a block $B$ on which $f$ depends; write $f_b=f(b,\cdot)$ for $b\in S_B$. For $a,b\in S_B$, $f_a-f_b$ is a sum of functions of $\le d-1$ blocks (terms not involving $B$ cancel). Let $f(a,y^*)=1$. If every $f_b\not\equiv0$: $\mu(f=1)=\sum_b\mu_B(b)\mu(f_b=1)\ge p^d$ by induction on $m$. Otherwise some $f_b\equiv0$, so $f_a=f_a-f_b\not\equiv0$ has degree $\le d-1$, and $\mu(f=1)\ge\mu_B(a)\mu(f_a=1)\ge p\cdot p^{d-1}$. $\square$

With $d=2$, $p=\min(2^{-1184},\tfrac14)$: $\gamma\ge2^{-2368}$ as claimed. Peeling the core block first gives the sharper $\gamma\ge\min(\tfrac1{16},\,2^{-1184}\cdot\tfrac14)=2^{-1186}$.

---

## 8. Is this a fully paid polynomial-in-$n$ resource bound?

**For the lemma itself: yes.** $\gamma$ is an absolute constant. Testing whether a given degree-$\le2$ polynomial vanishes on the global Bell support to failure probability $\delta$ costs $\lceil\gamma^{-1}\ln(1/\delta)\rceil\le 2^{2368}\ln(1/\delta)$ Bell samples, i.e. $2\times$ that many copies, each sample $O(n)$ Clifford gates plus $O(n)$ classical bits. No $n$-dependence, no uncharged catalog, no dependence on $P$ or $C$. Astronomical constant; no practical efficiency is claimed and none should be inferred.

**Not paid by this lemma (proof obligations elsewhere):**
1. How many such tests the learner performs and how it chooses polynomials (e.g. Gaussian elimination over the $O(n^2)$ degree-$\le2$ monomials needs a union bound over $O(n^2)$ hypotheses or a sequential-elimination argument; still $\mathrm{poly}(n)$ but must be written).
2. The claim that learned support relations suffice for *exact* Clifford-product block recovery when the core has stabilizers — this lemma only supplies $\gamma$; the structural identifiability statement is separate.
3. The $w\ge25$ cubic-gap argument (not assigned).
4. Exactness assumptions: two **identical, noiseless** copies and an exactly Clifford $C$. The Galois argument does not degrade gracefully: any perturbation of $\phi$ off $K$ voids §4.

**Falsifiers** (any one would break the lemma, none is expected given the proof): a nonzero $\nu_\phi(v)<2^{-1184}$ for some $w\le24$; a degree-$\le2$ polynomial nonzero on the global support with $\Pr[f=1]<2^{-1186}$; a Clifford $C$ for which $C^{\otimes2}$ fails to map Bell states to Bell states up to phase; a global state not of the form $C(\phi\otimes H^{\otimes(n-w)})$.