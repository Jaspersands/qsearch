# Audit: SC randomized source encoder as a classical sampler for polar-code DQI targets

## Verdict

**The parent bound holds.** The cheapest attack was to look for a frozen value or offset weighting that breaks the "divide by $2^{-|F|}$" step. It fails, because the gauge symmetry is exact.

For every explicit $F$, every $s$ and every $\alpha\in(0,1/2)$, the candidate sampler satisfies

$$\mathbb E_{b\sim \mathrm{Unif}(\mathbb F_2^N)}\ \mathrm{TV}(\mathrm{out}_b,\pi_b)\ \le\ 2d_F .$$

The proof needs only that $G$ is invertible over $\mathbb F_2$. Polar structure is used only for efficiency, through the SC recursion, and for the hope that $d_F$ is small.

**Two corrections to the quantum-side chain:**

1. The index on the Helstrom error must be $J(i)$, not $i$.
2. The relevant $e$'s are genie-aided synthesized-channel errors with uniform future bits. They are not the block or PGM error of decoding $C$ with frozen bits fixed. An $N=2$ control shows that these two quantities genuinely differ.

The guarantee is averaged over offsets only. It gives nothing for the worst offset, and nothing for arbitrary codes.

---

## 1. Setup and exact target identification

**Conventions.**
- $G=F_2^{\otimes s}$ with $F_2=\begin{psmallmatrix}1&0\\1&1\end{psmallmatrix}$. Over $\mathbb F_2$, $F_2^2=I$, so $G^{-1}=G$.
- $W=\mathrm{BSC}(\alpha)$.
- The ideal joint law is $P(u,y)=2^{-N}\prod_j W(y_j\mid (uG)_j)$.

Under $P$, $U$ is uniform, $X=UG$ is uniform, and $E:=Y+X\sim\mathrm{Ber}(\alpha)^{\otimes N}$ is independent of $X$. Hence $Y$ is uniform and independent of $E$.

**Lemma A (proved).** Let
$$Z_b:=\sum_{x\in b+K}\alpha^{|x|}(1-\alpha)^{N-|x|}=\Pr[E\in b+K].$$
For $u$ with $u_F=0$:
$$P(U=u\mid Y=b,\,U_F=0)\ \propto\ \alpha^{|b+uG|}(1-\alpha)^{N-|b+uG|}.$$
The map $u\mapsto x=b+uG$ is a bijection from $\{u_F=0\}$ onto $b+K$. So $x$ has exactly the law $\pi_b$. Call the corresponding $u$-law $\Pi_b$. Also:
- $P(U_F=0)=2^{-|F|}$;
- $P(Y=b\mid U_F=0)=2^{|F|-N}Z_b=:p(b)$;
- $\sum_b Z_b=|K|=2^{N-|F|}$.

**Algorithm law.** The sampler draws $u$ with
$$A_b(u)=\mathbf 1[u_F=0]\prod_{i\notin F}P(u_i\mid u_{<i},b).$$

**Korada's $Q$.**
$$Q(u,y)=2^{-N}\,2^{-|F|}\prod_{i\notin F}P(u_i\mid u_{<i},y).$$
Therefore $Q(U_F=\tilde u\mid y)=2^{-|F|}$ for every $y$, so $Q(U_F=\tilde u)=2^{-|F|}$, and
$$Q(u,y\mid U_F=0)=2^{-N}A_y(u).$$

## 2. Chain-rule TV bound (Korada Lemma 2, reproved)

The extracted Lemma 2 states $\sum|Q-P|\le 2\sum_{i\in F}\mathbb E_P|{\tfrac12}-P(U_i=0\mid\cdot)|$. I reprove it rather than rely on the garbled text.

Define hybrids $H_k$: $Y$ is uniform, coordinates $i<k$ use $P$-conditionals, and coordinates $i\ge k$ use $Q$-conditionals. Then $H_N=P$ and $H_0=Q$. Consecutive hybrids differ only at coordinate $k$, and the suffix kernels sum to 1, so

$$\|H_{k+1}-H_k\|_1=\mathbb E_{(U_{<k},Y)\sim P}\big\|P_k(\cdot\mid U_{<k},Y)-Q_k(\cdot\mid U_{<k},Y)\big\|_1 .$$

This is $0$ for $k\notin F$, and $2\,\mathbb E_P|P(U_k=0\mid U_{<k},Y)-\tfrac12|$ for $k\in F$. Hence

$$\mathrm{TV}(P,Q)=\tfrac12\|P-Q\|_1\le d_F. \tag{1}$$

(Proved.) The factor is correct for TV defined as half the $\ell_1$ distance.

## 3. Gauge lemma: all frozen values covered (proved)

For $v\in\mathbb F_2^N$ let $T_v(u,y)=(u+vG,\;y+v)$. Since $G^2=I$, we have $(u+vG)G=uG+v$. Hence $y+uG$ is invariant, so $P\circ T_v=P$.

Because $T_v$ is a translation, the $P$-conditionals are equivariant:
$$P(u_i+(vG)_i\mid u_{<i}+(vG)_{<i},\,y+v)=P(u_i\mid u_{<i},y).$$
This is Korada Lemma 6 in our convention. Consequently $Q\circ T_v=Q$.

$T_v$ maps the slice $\{U_F=\tilde u\}$ bijectively onto $\{U_F=\tilde u+(vG)_F\}$. Since $G$ is invertible, $(vG)_F$ ranges over all of $\mathbb F_2^{|F|}$. Therefore the slice $\ell_1$ distance $\sum_{u_F=\tilde u,\,y}|P-Q|$ is independent of $\tilde u$, and equals $2^{-|F|}\|P-Q\|_1$.

Both slice masses equal $2^{-|F|}$: for $P$ because $U$ is uniform, for $Q$ by construction. Normalizing:

$$\mathrm{TV}\big(P(\cdot\mid U_F=\tilde u),\,Q(\cdot\mid U_F=\tilde u)\big)=\mathrm{TV}(P,Q)\le d_F\quad\forall\tilde u. \tag{2}$$

So the division by $2^{-|F|}$ is justified by exact equality of slice masses and slice distances. It does not come from Lemma 9.

Lemma 9 bounds only the source-averaged law of the quantization error against $\mathrm{Ber}(\alpha)^{\otimes N}$. That is the unconditional $P(E)$. It mixes cosets and cannot yield a coset-conditional statement. The parent was right not to use it.

## 4. Main theorem (proved)

**Theorem 1.** For any explicit $F\subseteq\{0,\dots,N-1\}$, $s\ge1$, $\alpha\in(0,1/2)$, and any invertible $G$ (in particular $F_2^{\otimes s}$):

$$\mathbb E_{b}\,\mathrm{TV}(\mathrm{out}_b,\pi_b)\le 2d_F,\qquad d_F=\sum_{i\in F}\mathbb E_P\big|P(U_i=0\mid U_{<i},Y)-\tfrac12\big|.$$

The same bound holds for running with any frozen value $\tilde u$, with target $\pi$ on the shifted coset $b+\tilde u G_F+K$.

**Proof.** Set
- $Q_0(u,y)=2^{-N}A_y(u)$,
- $P_0(u,y)=p(y)\Pi_y(u)$,
- $R(u,y)=2^{-N}\Pi_y(u)$.

Then:
- $\mathrm{TV}(Q_0,R)=\sum_y 2^{-N}\mathrm{TV}(A_y,\Pi_y)=\mathbb E_b\mathrm{TV}(A_b,\Pi_b)$. The bijection $u\mapsto b+uG$ preserves TV.
- $\mathrm{TV}(P_0,R)=\mathrm{TV}(p,\mathrm{Unif})$.
- $\mathrm{TV}(p,\mathrm{Unif})\le \mathrm{TV}(P_0,Q_0)$, because $p$ and $\mathrm{Unif}$ are the $Y$-marginals of $P_0$ and $Q_0$, and marginalization contracts TV.

By the triangle inequality and (2):
$$\mathbb E_b\mathrm{TV}\le \mathrm{TV}(Q_0,P_0)+\mathrm{TV}(p,\mathrm{Unif})\le 2\,\mathrm{TV}(Q_0,P_0)\le 2d_F.\qquad\square$$

## 5. Scope and finite controls

**Offset scope (proved).**
- For $v\in K$ (that is, $v=wG$ with $w_F=0$), $T_v$ preserves $\{u_F=0\}$ and leaves the output $x=y+uG$ unchanged. Also $\pi_{b+v}=\pi_b$. So $\mathrm{TV}(\mathrm{out}_b,\pi_b)$ depends only on the coset $b+K$.
- Uniform $b$ is therefore the uniform average over the $2^{|F|}$ cosets.
- By Markov's inequality, a fraction at least $1-\gamma$ of offsets has $\mathrm{TV}\le 2d_F/\gamma$.
- **No worst-coset guarantee follows.** The $N=2$ control below has per-coset TVs $\alpha(1-2\alpha)$ and $(1-\alpha)(1-2\alpha)$, which are unequal.

**Finite control 1** ($N=2$, $F=\{1\}$; $K=\{00,10\}$). Let $r=(1-\alpha)^2+\alpha^2$.
- Coset $\{00,10\}$: the output is $00$ with probability $r$, while the target gives it probability $1-\alpha$. TV $=\alpha(1-2\alpha)$.
- Coset $\{01,11\}$: TV $=(1-\alpha)(1-2\alpha)$.
- Average: $\mathbb E_b\mathrm{TV}=(1-2\alpha)/2$.

Direct computation gives $d_1=r\cdot\frac{1-2\alpha}{2r}=\frac{1-2\alpha}2$. So $\mathbb E_b\mathrm{TV}=d_F\le 2d_F$. Theorem 1 is consistent here, and the factor 2 is not attained.

**Finite control 2 (exactness / non-tightness, proved).** If $F=\{0,\dots,k-1\}$ is a prefix, then every free index conditions on all frozen bits. The chain rule gives $A_b=\Pi_b$ for every $b$, so TV $=0$, even though $d_F>0$.

Example: $N=2$, $F=\{0\}$, $d_F=(1-2\alpha)^2/2$, sampler exact. In general, error comes only from free indices that precede frozen ones, because SC ignores future frozen constraints. So $d_F$ is sufficient but not necessary.

## 6. Exact bit-level implementation (proved, standard)

Take $\alpha=a/2^r$. Run SC on integer-scaled likelihood pairs, keeping homogeneous coordinates and dropping common normalizations, using:
- the check update $(a_0b_0+a_1b_1,\;a_0b_1+a_1b_0)$;
- the variable update conditioned on known $u$-partial sums.

At block length $n$, entries are integers of $O(n(r+1))$ bits. There are $O(N\log N)$ arithmetic operations, for $O(N\log N\cdot\mathsf M(N(r+1)))$ bit operations in total, where $\mathsf M$ is the multiplication cost. This is polynomial in the explicit input size $\Theta(N)$ and in $r$.

At free index $i$ with exact integer pair $(L_0,L_1)$:
- compute $\lfloor 2^t L_0/(L_0+L_1)\rfloor$;
- compare it with $t$ fresh fair bits.

The per-step conditional TV is at most $2^{-t}$ given any history. A hybrid argument gives a joint error of at most $N2^{-t}$. Choosing $t=\lceil\log_2(N/\eta)\rceil$ yields

$$\mathbb E_b\mathrm{TV}(\widehat{\mathrm{out}}_b,\pi_b)\le 2d_F+\eta,$$

in deterministic polynomial time with $O(N\log(N/\eta))$ random bits. A Las Vegas exact sampler (rejection on $[0,L_0+L_1)$) gives TV contribution 0 in expected polynomial time.

The ingredients are fully charged: $G$ is implicit from $s$; $F$, $b$ and $\alpha$ are read explicitly. No oracle, exact Gibbs sampler or quantum state is used. Floating-point SC would require a separate error analysis, which is not done here.

## 7. Does generation require computing or certifying $F$?

**No.** The sampler consumes the given $F$ and is always well-defined, whatever its quality. The bound is conditional on $d_F$.

**Optional certification (proved).** $d_F$ is an expectation of $\sum_{i\in F}|P(U_i=0\mid U_{<i},Y)-\tfrac12|\in[0,|F|/2]$ under $P$. $P$ is exactly samplable: draw $U$ uniform and $E\sim\mathrm{Ber}(\alpha)^{\otimes N}$. The SC posteriors are computed exactly. Hoeffding's inequality gives additive-$\tau$ estimates with $O(|F|^2\tau^{-2}\log\delta^{-1})$ samples.

This certifies $d_F\le\epsilon$ only to inverse-polynomial resolution. Certifying exponentially small $d_F$, for instance via Bhattacharyya computations on the exponentially large synthesized output alphabets, needs constructions not present in the supplied sources. **No uniform efficient good-code constructor is claimed.**

## 8. Connection to quantum polar decoding of $C$

**8a. Dual code structure (proved).**
$$C=K^\perp=\{c:(cG^T)_i=0\ \forall i\notin F\}=\{vG^{-T}:v_{F^c}=0\}.$$
Since $G^{-1}=G$, we have $G^{-T}=G^T$.

Let $J$ be the index-complement permutation $i\mapsto N-1-i$, which is bitwise complement. For the $2\times2$ kernel, $F_2^T=\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}=J_2F_2J_2$. Taking tensor powers, $G^T=JGJ$. Hence

$$C=\{wG\,J:\ w_{J(F)^c}=0\}.$$

So $C$ is the coordinate-reversed polar code with **information set $J(F)$**. The reversal permutes i.i.d. channel uses and is harmless.

**8b. Channel duality (source-dependent; independently checked at $N=2$).**
- The DQI channel is $y\mapsto\sqrt{1-\alpha}|0\rangle+(-1)^y\sqrt\alpha|1\rangle$, with overlap $1-2\alpha$. By Renes eq. (23), this overlap equals $|P(0\mid y)-P(1\mid y)|$ for $\mathrm{BSC}(\alpha)$. So the DQI channel is $W^\perp$ up to unitary equivalence; binary pure-state channels are fixed by their overlap.
- Renes Corollary 2 says $(W^{\langle b\rangle})^\perp\simeq(W^\perp)^{\langle\bar b\rangle}$, with all signs complemented. Complement is $J$, independent of bit ordering, provided both families are synthesized by the same recursion. This is a proof obligation for $G=F_2^{\otimes s}$ without bit reversal.
- Corollary 3 (with $H_{\min}/H_{\max}$ duality, Theorem 2) gives $P_{\rm guess}(W^\perp)=2^{H_{\max}(W)-1}=(1+Z(W))/2$. This uses $H_{\max}(Z\mid Y)=\log(1+Z)$ for uniform binary input.

Define:
- $Z_i:=\mathbb E_P\,2\sqrt{p_0p_1}$, the Bhattacharyya parameter of the $i$-th synthesized $\mathrm{BSC}(\alpha)$ channel, with all of $U$ uniform;
- $e_j$ := the Helstrom error for uniform $U_j$ given $(U_{<j},B^N)$, where $B^N=(W^\perp)^{\otimes N}(UG)$ and all of $U$ is uniform.

Then

$$e_{J(i)}=\tfrac12(1-Z_i).$$

**Independent $N=2$ checks**, with $c=1-2\alpha$ and $a=\alpha(1-\alpha)$:
- $i=1$: $Z(W^+)=4a$. Directly, $\rho_0-\rho_1=\tfrac12(\psi_0-\psi_1)^{\otimes2}$, so $e_0=c^2/2=(1-4a)/2$. ✓
- $i=0$: $Z(W^-)^2=8a(1-2a)$. Directly, $e_1=\tfrac12(1-\sqrt{1-c^4})$ with $1-c^4=8a(1-2a)$. ✓

**8c. Factors (proved).** Write $\delta=|p_0-\tfrac12|$, so $2\sqrt{p_0p_1}=\sqrt{1-4\delta^2}$. By Jensen:
$$\mathbb E\delta^2\le\tfrac14(1-Z_i^2),\qquad d_i\le\tfrac12\sqrt{1-Z_i^2}.$$
Substituting $Z_i=1-2e$ and $1+Z_i=2-2e$:

$$d_i\le\sqrt{e_{J(i)}(1-e_{J(i)})}\le\sqrt{e_{J(i)}},\qquad d_F\le\sum_{j\in J(F)}\sqrt{e_j}. \tag{3}$$

The parent's $\sum_{i\in F}\sqrt{e_i}$ has the wrong index; it should be $\sum_{i\in F}\sqrt{e_{J(i)}}$. Also, $Z_i\ge1-2\delta^2\Rightarrow d_i\le\delta$ is recovered, matching Korada Lemma 5.

**Corollary 2.** For the given instance,
$$\mathbb E_b\mathrm{TV}(\mathrm{out}_b,\pi_b)\le 2\sum_{j\in J(F)}\sqrt{e_j}\ \le\ 2\sqrt{|F|\textstyle\sum_{j\in J(F)}e_j}.$$
In particular, Korada's choice $F=\{i:Z_i\ge1-2\delta^2\}$ means $J(F)=\{j:e_j\le\delta^2\}$, which is exactly the polar good-channel set for $W^\perp$. That gives $\mathbb E_b\mathrm{TV}\le 2|F|\delta$. By Renes Corollary 4, $I(W^\perp)=h(\alpha)$, matching the size of $J(F)$ in the polarized regime.

## 9. What this eliminates, and what it does not

**Eliminated (conditionally proved).** Any claimed averaged-offset sampling advantage on the same instance $(G,F,b)$ whose quantum side is certified via small genie-aided synthesized-channel errors $\{e_j\}_{j\in J(F)}$, in the regime $\sum_{j\in J(F)}\sqrt{e_j}=o(1)$. This is the standard polar good-set criterion. The classical sampler matches it in polynomial time, with no need to construct or certify $F$.

**Not eliminated (gaps):**

1. **Genie channel versus the actual code.** The $e_j$ use uniform future bits $U_{>j}$, including frozen ones. Decoding $C$ fixes those frozen bits, which yields a strictly better channel in general.
   - Counterpoint ($N=2$, $F=\{1\}$, $C=\{00,01\}$): the true block or Helstrom error of $C$ is $\tfrac12(1-2\sqrt a)$, about $0.2$ at $\alpha=0.1$. The genie $e_0=c^2/2=0.32$.
   - So "small PGM / block error of $C$" or "some efficient quantum decoder of $C$" does **not** imply small $\sum\sqrt{e_j}$, and no implication to small $d_F$ is proved.
   - In this tiny case $d_F=\sqrt{\varepsilon_{\rm blk}(1-\varepsilon_{\rm blk})}$ coincidentally. That is a finite control, not a lemma.
2. **Square-root and $|F|$ loss.** A quantum analysis with $\sum e_j=\varepsilon$ gives only $2\sqrt{|F|\varepsilon}$ classically. In regimes where $\sum e_j$ is small but $|F|\sum e_j$ is not, the classical bound is vacuous. This is not evidence of quantum advantage.
3. **Worst-offset or per-coset guarantees** are not covered (§5).
4. **Arbitrary codes or random regular codes.** Theorem 1 holds for any invertible $G$, but efficient exact posteriors are polar-specific. For general $G$, computing $P(U_i\mid U_{<i},Y)$ is not claimed to be efficient.
5. **Non-polar frozen sets inside polar $G$** (for example RM-like $F$). Theorem 1 still applies, but $d_F$ may be $\Theta(1)$. Then nothing follows in either direction.

## 10. Proof obligations and falsifiers

**Obligations:**
- **(O1) Recursion order.** Confirm that Renes Corollary 2's recursion, stated with $\circledast/\oplus$ convolutions and with $\oplus\simeq$ variable convolution requiring channel symmetry, generates the same synthesized channels as SC under $G=F_2^{\otimes s}$ without bit reversal, for both $W$ and $W^\perp$. Verified only at $N=2$. Theorem 1 does not depend on this.
- **(O2) Normalization.** Confirm Renes's normalization of $Q(W)$ in Corollary 3, i.e. $P_{\rm guess}(W^\perp)=(1+Z(W))/2$ for uniform input on cq channels with a classical register $U_{<j}$. Single-letter and $N=2$ cases check out.
- **(O3) Target identification.** The DQI product-amplitude output on coset $b+K$ is exactly $\pi_b$ (task-supplied identification, with $\alpha=1/(1+e^\beta)$). Its averaged-offset guarantee is $\sqrt\varepsilon$ in block error, per the 2611.12718 excerpt citing [SMR+26]. Not independently verified here.

**Falsifiers:**
- **Theorem 1:** any $(s,F,\alpha)$ with exact enumeration showing $\mathbb E_b\mathrm{TV}>2d_F$. Small-$N$ brute force over all $F$ at $N\le 8$ is cheap.
- **(3):** an index $i$ with $e_{J(i)}\ne(1-Z_i)/2$ at $N=4$ or $N=8$.
- **The elimination's relevance:** a polar-$G$ instance where an efficient quantum decoder of $C$ has small block error while $d_F$ stays $\Theta(1)$. This would show the classical counterpart misses that candidate. It would **not** by itself show a separation.

No novelty, hardness or separation claims are made.