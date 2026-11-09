# Kernel lemma with sharp precision loss, and why the Stoll Prop. 5.1 systems are not yet covered

## Verdict

The kernel lemma below is proved and sharp. It uses only Smith normal form over $\mathbb Z_p$.

Applying it to Stoll's Prop. 5.1 systems is **not** justified by $g$, $B$, $\operatorname{disc} f$ and quotient accuracy alone. One quantitative bound is missing; it is stated in §4. I make no claim of a full algorithm, a speedup or novelty.

## 1. Overstrong versions disproved (1×2 examples)

**(a) Known rank alone, without $k$, determines nothing.** Take $A=(p^N\ \ 0)$ and $A'=(0\ \ p^N)$.
- Both have exact rank 1 and $A\equiv A'\equiv 0 \pmod{p^N}$.
- Their saturated kernels are $\langle(0,1)\rangle$ and $\langle(1,0)\rangle$, which differ modulo $p$.
- The same pair with $p^k$ in place of $p^N$ shows that $N>k$ is necessary even when $k$ is known.

**(b) Recovery modulo $p^N$ is false; the loss is exactly $k$.** Take $A=(p^k\ \ 0)$ and $A'=(p^k\ \ p^N)$ with $N>k$.
- Both have rank 1, a single Smith valuation $k$, and $A\equiv A' \pmod{p^N}$.
- Their saturated kernels are spanned by $(0,1)$ and $(-p^{N-k},1)$.
- These agree modulo $p^{N-k}$ and differ modulo $p^{N-k+1}$. So no algorithm can beat $N-k$.

**(c) "Kernel modulo $p^N$ is the saturated kernel" is also false.** For $A=\operatorname{diag}(p^k,0)$:
- the kernel modulo $p^N$ contains $(p^{N-k},0)$, which is not in the saturated kernel modulo $p^N$;
- it vanishes modulo $p^{N-k}$, consistent with the lemma.

Mascot Thm 2.23 is the case $k=0$, and his Remark 2.24 is this phenomenon.

## 2. Kernel lemma (proved)

**Setup.**
- $A\in M_{m\times n}(\mathbb Z_p)$ has exact rank $r$.
- Smith form: $A=UDV$ with $U\in GL_m(\mathbb Z_p)$, $V\in GL_n(\mathbb Z_p)$, and $D=\operatorname{diag}(p^{e_1},\dots,p^{e_r},0,\dots)$.
- Assume $\max_i e_i\le k<N$.
- Let $K=\ker_{\mathbb Q_p}A\cap\mathbb Z_p^n=V^{-1}(0^r\oplus\mathbb Z_p^{\,n-r})$, a saturated direct summand of rank $n-r$.
- Let $K_N=\{x\in(\mathbb Z/p^N)^n : Ax\equiv0 \pmod{p^N}\}$. This set depends only on $A \bmod p^N$.

**Lemma.** The image of $K_N$ in $(\mathbb Z/p^{N-k})^n$ equals $K \bmod p^{N-k}$.

**Corollary.** Any two exact matrices satisfying the hypotheses and congruent modulo $p^N$ have saturated kernels congruent modulo $p^{N-k}$.

**Proof.**
1. Put $y=Vx$. Then $Ax\equiv0 \pmod{p^N}$ iff $p^{e_i}y_i\equiv0 \pmod{p^N}$ for $i\le r$, with $y_j$ free for $j>r$.
2. Hence $y_i\in p^{N-e_i}\mathbb Z_p\subseteq p^{N-k}\mathbb Z_p$ for $i\le r$, using $e_i\le k$.
3. So the reduction of $y$ modulo $p^{N-k}$ lies in $0^r\oplus(\mathbb Z/p^{N-k})^{n-r}$.
4. Conversely, every vector of that form lifts to $y$ with $y_i=0$ for $i\le r$, and this lift lies in $V(K)$.
5. Apply $V^{-1}$. Sharpness is example 1(b). ∎

**Algorithm.**
1. Compute a Smith decomposition of the known residue: $A\equiv U'D'V' \pmod{p^N}$, with $U'$ and $V'$ invertible modulo $p^N$. This costs $O(mn\min(m,n))$ ring operations in $\mathbb Z/p^N$, each $\tilde O(N\log p)$ bits.
2. **Consistency check** (a necessary condition only). The residue's invariants must be exactly $r$ entries of valuation $\le k$, with the rest $\equiv0 \pmod{p^N}$. This holds because $D' \equiv D$ up to units. Failure falsifies the hypotheses.
3. **Output.** Return the last $n-r$ columns of $V'^{-1}$, reduced modulo $p^{N-k}$.

**Why the output is correct.**
- $V'$ defines the same set $K_N$, so the proof above applies verbatim with $V'$ in place of $V$.
- The returned columns are part of a unimodular matrix, so they form a basis of a free direct summand. That summand equals $K \bmod p^{N-k}$.
- **Any integral lift is valid.** Let $c_j$ be lifts and $b_i$ a basis of $K$. Write $c_j\equiv\sum_i M_{ji}b_i$ with $M$ invertible modulo $p^{N-k}$. Lift $M$ to $GL(\mathbb Z_p)$. Then $b'_j=\sum_i M_{ji}b_i$ is a basis of $K$ with $c_j\equiv b'_j \pmod{p^{N-k}}$.

**Corollary (rank comes for free).** If only the Smith bound $k<N$ is known, the exact rank is determined by the residue: $r$ equals the number of residue invariants that are nonzero modulo $p^N$. Nonzero exact invariants are visible because $e_i\le k<N$. So one bound $k$ replaces "known $r$ and known $k$".

**Useful sufficient condition.** Since $\sum_i e_i=v(\text{gcd of } r\times r\text{ minors})$, we have $k\le v_p(\mu)$ for any single nonzero $r\times r$ minor $\mu$.

## 3. Precision ledger

1. **Output precision.** To get $K \bmod p^M$ you need $N\ge M+k$. This is sharp.
2. **Matrix perturbations.** The lemma needs only $A_{\rm exact}\equiv A_{\rm comp} \pmod{p^N}$.
   - In Stoll's setting, $N$ is the minimum accuracy over the entries coming from $s$, $b$, $d$, $a_1$, $f_1$ and $f$, after the integral rescaling below.
   - The precision lost in computing $s=\sqrt{\cdot}$ in $L=\mathbb Q_p[x]/f$ (Hensel, especially at $p=2$) and in factoring $d=\gcd(a,f)$ must be charged before $N$ is defined. That cost is not bounded here.
3. **Integrality.** Rescaling rows by $p^{c}$ to clear denominators of nonintegral Mumford inputs does not change the kernel. It does change the Smith valuations and the required accuracy. The packet's $f=x^3+4x-1$, $P=(1/4,1/8)$ example shows denominators are not controlled by $f$ alone.
4. **Unverifiable hypotheses.** Finite data can confirm $r\ge$ (observed) but can never certify that a residue-zero invariant is exactly zero.
   - Example: the true $A=(p^N\ \ 0)$ with claimed $r=0$ passes the consistency check, yet the output is silently wrong.
   - So $k$ (or $r$) must come from an external proof.
5. **Monic normalization.** Making $w$ monic divides by its leading coefficient. That costs precision $\lambda=v(\mathrm{lc}\,w)$ on the primitive kernel vector. $\lambda$ is observable whenever $\lambda<M$. A priori it is bounded by the Smith bound of the augmented system in §4. Sketch: a primitive $x$ with $Bx=(0,p^\lambda u)$ forces $e_{\max}(B)\ge\lambda$.

## 4. The actual Stoll systems

**Shape.** The unknowns are $(u,v,w)$ under the degree bounds (5.2), subject to the three congruences (5.1).
- Number of variables: $2g+\deg a-\deg d+2$.
- Number of constraints: $2g+1+\deg a_1$, which is one fewer than the number of variables.
- So $r\le$ #constraints, and the kernel is at least 1-dimensional.

**Requirements beyond "find the kernel".**
1. **Shape detection.** $\deg d$ must be known before the matrix exists. It equals $\deg a+\deg f-\operatorname{rank}\operatorname{Syl}(a,f)$, so it is itself an exact-rank question.
2. **Minimal $w$.** Stoll needs the unique $w$ that is monic of *minimal degree*. Finding it means deciding exact vanishing in the augmented systems $M_j$: $M$ plus the rows $w_{j+1}=\dots=w_g=0$, for $j=0,\dots,g$.

**Where $k$ comes from.**
- **Bounded by $f$.** The CRT identification $k[x]/(f_1a_1d)\cong\prod$ has distortion controlled partly by $v\operatorname{Res}(d,f_1)\le v(\operatorname{disc}f)$. This part is poly$(g,B)$.
- **Bounded by nothing in the packet.**
  - The distortion from $v\operatorname{Res}(a_1,f_1)$. This is Stoll's warning that roots of $a$ can be close to roots of $f$.
  - The rank and Smith valuations of $M_j$, which depend on $\deg w_{\min}$ — that is, on the half $Q=[w,r]$ itself. This is Stoll's warning about a lower-degree output or points near infinity.
  - Whether $\dim\ker M=1$ generically, and whether kernels are $h$-multiples when $\deg w_{\min}<g$. The source asserts neither. **Unverified.**

**Proved obstruction (semicontinuity).** Suppose a family of exact inputs has a uniform bound $k\le K$. Then $v(d_r)\le rK$, where $d_r$ is the $r$-th determinantal divisor. Now let inputs $A_n\to A_\infty$ $p$-adically with $\operatorname{rank}A_\infty<r=\operatorname{rank}A_n$. Every $r\times r$ minor tends to $0$, so $v(d_r(A_n))\to\infty$, contradicting the bound. Hence:

> A uniform Smith bound on a family of route inputs forces the rank of every $M_j$ to be locally constant on the family's closure.

$2J(\mathbb Q_p)$ is open, and $W_{g-1}(\mathbb Q_p)$-type loci (where $\deg w$ drops) have nearby points with $\deg w=g$. So if route inputs can accumulate at a rank-change point, no bound in terms of $g$, $B$, $\operatorname{disc}f$ and accuracy exists.

That such a rank change actually occurs for $M_j$ near the lower-degree locus is **plausible from Stoll's warning but unverified**. Whether the halving tree's inputs actually accumulate there is likewise open.

**Answer to the question.** No. Without knowing the half or assuming genericity, neither $r$ nor $k$ follows from the stated data. By the corollary in §2, a single bound suffices for both.

**The exactly one missing bound** (stated in the route's own freedom):

> **Missing bound K.** There is an explicit $K(g,B,\log p)$ such that every class $h\in A=G/E$ has a representative $h'\in h+E$ (or $h+E'$ with $E'$ a paid subgroup), findable in poly$(g,B,\log p)$ trials, with the following property. For the integrally normalized exact data $(a',b',s')$ of $h'$, every nonzero Smith valuation of $\operatorname{Syl}(a',f)$ and of $M_j(a',b',s')$, $j=0,\dots,g$, is at most $K$.

Granting K, the lemma gives at accuracy $N\ge M+K$:
- the exact $\deg d$;
- the exact ranks of all $M_j$, hence $\deg w_{\min}$;
- $w_{\min}$ modulo $p^{M-K}$, the extra $K$ covering monic normalization.

The remaining steps — computing $r$ via the second congruence, then $s$ and square-root precision — still have to be charged separately.

**Why K is plausible but unproved.**
- The coset $h+E$ corresponds to halves ranging over $q_0+L$, an open set. A proper analytic bad locus cannot contain it, so a good representative exists qualitatively.
- A quantitative version needs:
  - a bad-locus equation $F$ of bounded degree and height in coordinates where $L$ is a box;
  - a nonvanishing lemma on a box with grid spacing $p^{-j}$, $p^j>\deg F$. This matters at $p=2$, where Schwartz–Zippel over the residue field fails.
- Neither is supplied. This is speculation, not a proof.

## 5. Proof obligations and falsifiers

**Proof obligations.**
1. Prove K, or prove its variant with $E'$ and charge $[E:E']$.
2. Bound the square-root and gcd precision losses that define $N$ for the entries.
3. Settle $\dim\ker M_j$ as a function of $\deg w_{\min}$. Stoll asserts only that the minimal monic $w$ is unique.

**Falsifiers.**
1. **For K.** An explicit $f$ (any $g$) and a class $h$ such that every representative in $h+E$ has $M_{g-1}$ with Smith valuation exceeding any proposed $K$. A natural candidate is a family of halves $q_0+L$ meeting $W_{g-1}$ through their center to infinite order.
2. **For the lemma.** None possible: it is proved, and sharp by 1(b).
3. **Route-specific.** Exhibit $A_n\to A_\infty$ inside the actual halving tree with a rank drop. By semicontinuity this kills any bound uniform in $g$, $B$ and $\operatorname{disc}f$.

**Gates.** Full algorithm, speedup, novelty, hardness and execution all remain **false**. No asymptotic claim is drawn from the 1×2 examples beyond the proved sharpness.