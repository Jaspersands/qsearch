# Rees HSP: Specialist Review Assessment for Codex

Date: 27 October 2026.
Reviewer: External AI-assisted review pass (primary auditor + two independent read-only subagents: Mathematical Proof Auditor and Prior-Art/Impact Analyst).
Status: **Automated technical review, NOT human specialist validation, peer review, formal compiler verification, or a novelty certificate.** No external network, Git, or outreach action was performed.

## Reviewed Snapshot Fingerprints

```
dc92967068ef507c48fc5dc9ea8d9e5685d13219920b51df3fc01ba6ad4bb31f  research/manuscripts/rees_hsp_review.tex
74a46bd40517fc648c70c48b696b28fdeccd4b67576a7f7133338e6ccb056f24  research/manuscripts/review_evidence/2026-10-23-correctness-review.md
9a9e9d484d091c7a90e88b313d8774f050ca9dc7b9a82d0d63f2d45fe17e2f31  research/manuscripts/review_evidence/2026-10-27-prior-art-scope.md
```

Also inspected: `research/manuscripts/REES_REVIEW_BRIEF.md`, `research/manuscripts/REES_REVIEW_VERIFICATION.md`, `theorems/rees_hsp_reduction.py`, `theorems/uniform_bch_rees.py`, `theorems/central_character_descent.py`, `theorems/rees_complete_instrument.py`, `theorems/prime_power_rees_descent.py`, `formal/Formal/CentralCharacterDescent.lean`, `formal/drafts/ReesHomogenization.lean`, and the supporting audit notes in `research/`.

---

## Executive Summary Across the Three Questions

1. **Question 1 — Does the homogenization or recursive state-conversion argument have a mathematical flaw?**
   **No mathematical flaw was found.** The positive lower-central Rees cover, non-ideal Vandermonde interpolation in the vector-space quotient $L/\mathfrak{h}$, copy-only lift, coset-bank left-twirl refresh, non-transverse central character projection ($K = H \cap Z \neq 1$), pointwise quotient state conversion over non-homomorphic sections $\sigma: G/Z \to G$, complete-instrument diamond-norm error hybrid, uniform ODE-based BCH evaluation, prime-power Hensel lifting, and outer black-box reductions are all algebraically sound under their stated hypotheses. Notice that the previously identified `F1` actual-class normalization is properly reconciled in `research/manuscripts/rees_hsp_review.tex` (lines 374–384). Three minor, non-fatal exposition clarifications in Sections 6–8 are listed in Section 1.4 below.

2. **Question 2 — Does an existing result already cover this precise growing-prime regime?**
   **No inspected published theorem or short composition of published reductions covers this regime** (fixed nilpotency class $c < p$, growing dimension $n$ and growing prime $p$, arbitrary hidden subgroup $H \le \exp(L)$, total bounded-error time $\mathrm{poly}_c(n, \log p, \text{label width}, \log(1/\varepsilon))$). Every constituent primitive is prior art, but each existing framework encounters a sharp structural or complexity barrier at class $c \ge 3$ with growing $p$ that is specifically bridged by the positive Rees cover $A = \bigoplus_{r=1}^c t^r \gamma_r(L)$ and its $c$-point tuple evaluator.

3. **Question 3 — Does the result, if correct and additional, warrant further development?**
   **Yes, as a focused theoretical quantum complexity contribution and formal-verification target; no, as a practical quantum receiver or applied/cryptanalytic speedup.** Concrete, high-leverage next steps for the repository (including finishing the Lean 4 proof in `formal/drafts/ReesHomogenization.lean` and connecting it to `formal/Formal/CentralCharacterDescent.lean`) are detailed in Section 3.3.

---

## 1. Detailed Mathematical Audit (Question 1)

### 1.1 Positive Rees Homogenization (`rees_hsp_review.tex`, Section 2, Lemmas 2 & 4, Proposition 5)

- **Un-truncated Lie closure and class bound of $A = \bigoplus_{r=1}^c t^r \gamma_r(L) \subset L[t]$:**
  - By the Jacobi identity and induction on $s$, the lower-central series of any Lie algebra $L$ satisfies $[\gamma_r(L), \gamma_s(L)] \subseteq \gamma_{r+s}(L)$.
  - In $L[t] = L \otimes_{\mathbb{F}_p} \mathbb{F}_p[t]$, the polynomial bracket of $x t^r \in A_r$ ($x \in \gamma_r(L)$) and $y t^s \in A_s$ ($y \in \gamma_s(L)$) is $[x, y]_L t^{r+s}$.
    - When $r + s \le c$, $[x, y]_L \in \gamma_{r+s}(L)$, so $[x, y]_L t^{r+s} \in A_{r+s} \subset A$.
    - When $r + s > c$, $\gamma_{r+s}(L) \subseteq \gamma_{c+1}(L) = 0$ because $L$ has nilpotency class at most $c$, so $[x, y]_L = 0$ in $L$ already.
  - Thus $A$ is closed under the **exact** polynomial bracket of $L[t]$ without dropping any nonzero terms, and any $(c+1)$-fold bracket in $A$ has $t$-degree $\ge c + 1 > c$ and vanishes, so $A$ has class at most $c$ (matching `make_rees_cover` in `theorems/rees_hsp_reduction.py`, lines 168–170).
- **Commutation of $E_s$ and $\Delta_s$ with $\exp$ and $\log$:**
  - For every $s \in \mathbb{F}_p$, evaluation $E_s: a(t) \mapsto a(s)$ is the restriction to $A$ of the Lie algebra homomorphism $\operatorname{id}_L \otimes (t \mapsto s): L[t] \to L$. For $s \in \mathbb{F}_p^\times$, $\Delta_s: a(t) \mapsto a(st)$ is a Lie algebra automorphism of $A$ scaling grade $r$ by $s^r$.
  - Because $c < p$, all rational coefficients in the degree-$c$ Baker–Campbell–Hausdorff polynomial $\operatorname{BCH}_c(X, Y)$ have denominators dividing $c!$, which are invertible in $\mathbb{F}_p$. Since $\operatorname{BCH}_c(X, Y)$ is an $\mathbb{F}_p$-linear combination of nested Lie brackets of weight $\le c$, any Lie homomorphism $\phi: M_1 \to M_2$ between class-$\le c$ Lie algebras over $\mathbb{F}_p$ satisfies $\phi(\operatorname{BCH}_c(X, Y)) = \operatorname{BCH}_c(\phi(X), \phi(Y))$ and $\phi(-X) = -\phi(X)$. Therefore $\Phi_s := \exp \circ E_s \circ \log: \exp(A) \to \exp(L)$ is an exact group homomorphism, and $\exp \circ \Delta_s \circ \log$ is an exact group automorphism of $\exp(A)$.
- **Non-normal $H$ and non-ideal Vandermonde interpolation in Lemma 2 (lines 104–121):**
  - The oracle contract (line 50) is left-coset hiding: $f(g) = f(g') \iff g^{-1}g' \in H$.
  - Since $\Phi_i(a) = \exp E_{s_i}(\log a)$ is a group homomorphism,
    $$\bigl(\exp E_{s_i}(\log a)\bigr)^{-1}\bigl(\exp E_{s_i}(\log b)\bigr) = \Phi_i(a)^{-1}\Phi_i(b) = \Phi_i(a^{-1}b) = \exp E_{s_i}(\log(a^{-1}b)).$$
  - Writing $\log(a^{-1}b) = \sum_{r=1}^c C_r t^r$ with $C_r \in \gamma_r(L)$, we have $\widehat{f}(a) = \widehat{f}(b) \iff \forall i \in \{1,\dots,c\},\; \sum_{r=1}^c s_i^r C_r \in \mathfrak{h} = \log H$.
  - By Lazard correspondence over the prime field $\mathbb{F}_p$, for *any* subgroup $H \le G$ (normal or not), $\mathfrak{h} = \log H$ is a Lie subalgebra of $L$, hence in particular an $\mathbb{F}_p$-linear subspace of $L$. Thus the vector-space quotient $\pi_{\mathfrak{h}}: L \to L/\mathfrak{h}$ is well-defined and $\mathbb{F}_p$-linear even when $\mathfrak{h}$ is not an ideal.
  - Since $s_1, \dots, s_c \in \mathbb{F}_p^\times$ are distinct ($c \le p - 1$), the matrix $V = (s_i^r)_{i,r=1}^c \in \mathrm{GL}_c(\mathbb{F}_p)$ has determinant $\prod_{i=1}^c s_i \prod_{1 \le i < j \le c} (s_j - s_i) \not\equiv 0 \pmod p$. Applying $V^{-1}$ takes only $\mathbb{F}_p$-linear combinations (no Lie brackets with ambient elements), establishing $\sum_{r=1}^c s_i^r C_r \in \mathfrak{h}\ (\forall i) \iff C_r \in \mathfrak{h}\ (\forall r) \iff C_r \in \mathfrak{h} \cap \gamma_r(L)\ (\forall r)$.
  - For $x t^r \in t^r(\mathfrak{h} \cap \gamma_r(L))$ and $y t^s \in t^s(\mathfrak{h} \cap \gamma_s(L))$, $[x, y]_L \in [\mathfrak{h}, \mathfrak{h}] \subseteq \mathfrak{h}$ (using only that $\mathfrak{h}$ is a Lie subalgebra) and $[x, y]_L \in [\gamma_r(L), \gamma_s(L)] \subseteq \gamma_{r+s}(L)$, so $\widetilde{\mathfrak{h}} = \bigoplus_{r=1}^c t^r(\mathfrak{h} \cap \gamma_r(L))$ is a Lie subalgebra of $A$ preserved by every $\Delta_s$ ($s \in \mathbb{F}_p^\times$).
- **Copy-only lift (Lemma 4) and coset-bank refresh (Proposition 5):**
  - With $R_g|x\rangle = |xg^{-1}\rangle$, $R_{g_1} R_{g_2} = R_{g_1 g_2}$, $R_g^\dagger = R_{g^{-1}}$, and $\operatorname{Tr}(R_u) = |G|\delta_{u,1}$. For $\rho_H = \frac{1}{|G|} \sum_{h \in H} R_h = \frac{1}{|G|}\sum_{a \in G} |aH\rangle\langle aH|$,
    $$\operatorname{Tr}(\rho_H R_g) = \frac{1}{|G|} \sum_{h \in H} \operatorname{Tr}(R_{hg}) = \sum_{h \in H} \delta_{hg, 1} = 1_H(g^{-1}) = 1_H(g)$$
    for arbitrary (non-normal) $H \le G$.
  - On uniform address $|\exp A\rangle$, applying controlled-$R_{\Phi_i(a)}$ to $c$ fresh copies of $\rho_H$, uncomputing the public evaluation workspace, and tracing out all $c$ targets leaves the $(a,b)$ matrix entry
    $$\rho_{\text{out}}[a,b] = \frac{1}{|\exp A|} \prod_{i=1}^c \operatorname{Tr}\!\left(R_{\Phi_i(a)} \rho_H R_{\Phi_i(b)}^\dagger\right) = \frac{1}{|\exp A|} \prod_{i=1}^c \operatorname{Tr}\!\left(\rho_H R_{\Phi_i(b)^{-1}\Phi_i(a)}\right) = \frac{1_{\widetilde{H}}(b^{-1}a)}{|\exp A|} = \langle a | \rho_{\widetilde{H}} | b \rangle.$$
  - In Proposition 5 (lines 160–187), independent left translations $\mathcal{T}(S) = |G|^{-1}\sum_{g \in G} L_g S L_g^\dagger$ ($L_g|x\rangle = |gx\rangle$) map every pure left-coset projector $P_a = |aH\rangle\langle aH|$ to $\rho_H$, and $\mathcal{T}(S)_{q,r} = |G|^{-1}\sum_{z \in G} S_{zq, zr} = |G|^{-1}\operatorname{Tr}(S R_{r^{-1}q})$. The opposite-character separable bank counterexample in Remark 6 (lines 193–200) is also exact ($k a + 2(-k/2)a = 0 \pmod p$).

### 1.2 Complete Central Instrument & Pointwise Quotient Conversion (`rees_hsp_review.tex`, Section 3, Lemma 7, Proposition 8)

- **Spectral projectors $\Pi_\lambda$ (lines 213–220):**
  - For $Z \le Z(G)$ elementary abelian over $\mathbb{F}_p$ (written additively inside $\chi_\lambda$), $\Pi_\lambda = |Z|^{-1}\sum_{z \in Z} \chi_\lambda(-z) R_z$ satisfies $\Pi_\lambda^\dagger = \Pi_\lambda$, $\Pi_\lambda \Pi_\mu = \delta_{\lambda,\mu}\Pi_\lambda$, $\sum_\lambda \Pi_\lambda = I$, and $[\Pi_\lambda, \rho_H] = 0$ because $Z \le Z(G)$ implies $R_z R_h = R_{zh} = R_{hz} = R_h R_z$ even when $H$ is non-normal.
- **Normalized branch law for nontrivial $K = H \cap Z$ (Lemma 7, lines 222–245):**
  - Outcome probability: $\operatorname{Tr}(\rho_H \Pi_\lambda) = \frac{1}{|G||Z|}\sum_{h \in H, z \in Z} \chi_\lambda(-z)\operatorname{Tr}(R_{hz}) = \frac{1}{|Z|}\sum_{z \in K} \chi_\lambda(-z) = \frac{|K|}{|Z|} 1_{K^\perp}(\lambda)$.
  - Normalized state on $\lambda \in K^\perp$: $\rho_\lambda = \frac{\rho_H \Pi_\lambda}{|K|/|Z|} = \frac{1}{|G||K|} \sum_{h \in H, z \in Z} \chi_\lambda(-z) R_{hz}$.
  - Trace against $R_g$:
    $$\operatorname{Tr}(\rho_\lambda R_g) = \frac{1}{|K|}\sum_{h \in H, z \in Z} \chi_\lambda(-z)\delta_{hzg, 1}.$$
    Because $z \in Z(G)$, $hzg = 1 \iff g = (hz)^{-1} = h^{-1}z^{-1} \in HZ$. If $g \notin HZ$, the sum is $0$. If $g = h_0 z_0 \in HZ$ ($h_0 \in H, z_0 \in Z$), then $hzg = 1 \iff (hh_0)(zz_0) = 1 \iff hh_0 = k \in H \cap Z = K$ and $z = -z_0 - k$ (in additive notation on $Z$, so $-z = z_0 + k$). Since $\lambda \in K^\perp$, $\chi_\lambda(-z) = \chi_\lambda(z_0 + k) = \chi_\lambda(z_0)$ for each of the $|K|$ choices of $k \in K$. The $|K|$ equal contributions cancel $|K|^{-1}$, giving $\operatorname{Tr}(\rho_\lambda R_g) = \chi_\lambda(z_0)$ independently of the decomposition $g = h_0 z_0$.
- **Pointwise quotient conversion and non-homomorphic sections $\sigma: Q \to G$ (Proposition 8, lines 259–276):**
  - Let $\pi: G \to Q = G/Z$ be the canonical quotient homomorphism and $\sigma: Q \to G$ any public section ($\pi(\sigma(q)) = q$).
  - For active targets $I = \{i : s_i \ne 0\} \ne \emptyset$ and $g := \sigma(r)^{-1}\sigma(q) \in G$, the $(q,r)$ matrix entry of the reduced control register is:
    $$\rho_{\text{out}}[q,r] = \frac{1}{|Q|} \prod_{i \in I} \operatorname{Tr}\!\left(R_{\Delta_{s_i}(\sigma(q))} \rho_{\lambda_i} R_{\Delta_{s_i}(\sigma(r))}^\dagger\right) = \frac{1}{|Q|} \prod_{i \in I} \operatorname{Tr}\!\left(\rho_{\lambda_i} R_{\Delta_{s_i}(g)}\right).$$
  - Even when $\sigma$ is **not** a homomorphism (so $\sigma(r)^{-1}\sigma(q) \ne \sigma(r^{-1}q)$), $\pi: G \to G/Z$ *is* a homomorphism with $\ker\pi = Z \le HZ$, so:
    $$g = \sigma(r)^{-1}\sigma(q) \in HZ \iff \pi(g) = \pi(\sigma(r))^{-1}\pi(\sigma(q)) = r^{-1}q \in HZ/Z.$$
  - When $r^{-1}q \notin HZ/Z$, $g \notin HZ$, and since $\Delta_{s_i}$ ($s_i \ne 0$) preserves $H$ and $Z$, $\Delta_{s_i}(g) \notin HZ$; because $I \ne \emptyset$, the product is $0$.
  - When $r^{-1}q \in HZ/Z$, $g = hz \in HZ$, $\Delta_{s_i}(g) = \Delta_{s_i}(h)(s_i^d z)$ with $\Delta_{s_i}(h) \in H$, and Lemma 7 gives $\prod_{i \in I} \chi_{\lambda_i}(s_i^d z) = \chi_{\sum_{i=1}^M s_i^d \lambda_i}(z) = 1$ by $\sum_{i=1}^M s_i^d \lambda_i = 0$. Any central coboundary factor $\sigma(r)^{-1}\sigma(q)\sigma(r^{-1}q)^{-1} \in Z$ from a non-homomorphic $\sigma$ is absorbed into $z$ and annihilated by $\sum_{i=1}^M s_i^d \lambda_i = 0$.
- **Record independence and zero scales:**
  - Because $\rho_{\text{out}} = \rho_{HZ/Z}$ holds **pointwise** on every positive-probability branch $\boldsymbol{\lambda} \in (K^\perp)^M$ and every valid nonzero witness $\mathbf{s}$, the classical record $(\boldsymbol{\lambda}, \mathbf{s})$ is in a tensor product with $\rho_{HZ/Z}$. Disjoint fresh preparation trees therefore supply exact IID inputs to the next stage without postselection or conditioning bias. Zero-scale targets ($s_i = 0$) are simply traced out ($\operatorname{Tr}(\rho_{\lambda_i}) = 1$) without calling $\Delta_0$, while still being charged as consumed inputs.

### 1.3 Recursive Descent, SDE Interface, Clocks, and Extensions (`rees_hsp_review.tex`, Sections 4–8)

- **Retention of all of $\mathfrak{h}$ in grade 1 (Section 4, lines 284–305):**
  - Quotienting $A$ successively by $A_c, A_{c-1}, \dots, A_2$ leaves $A / \bigoplus_{r=2}^c A_r \cong A_1 = tL$ as an additive group, with hidden subgroup image $t(\mathfrak{h} \cap \gamma_1(L)) = t\mathfrak{h}$. Because $A_1 = tL$ (and not $L/[L,L]$) is linearly independent in $L[t]$ from $\bigoplus_{r=2}^c t^r \gamma_r(L)$, even directions of $\mathfrak{h}$ contained in $[L,L]$ survive intact in grade 1.
- **Exponent reduction $\delta_d = \gcd(d, p-1)$ including the $u=0$ edge case (Sections 4 & 6, lines 302–303, 433–436):**
  - Since $\gcd(d/\delta_d, (p-1)/\delta_d) = 1$, choosing $u \equiv (d/\delta_d)^{-1} \pmod{(p-1)/\delta_d}$ gives $du = \delta_d + k(p-1)$. Setting $s_i = x_i^u$ for $x_i \ne 0$ and $s_i = 0$ for $x_i = 0$ gives $s_i^d = x_i^{du} = x_i^{\delta_d}$ in $\mathbb{F}_p$. When $\delta_d = p - 1$ (so $(p-1)/\delta_d = 1$ and $u = 0$), keeping $s_i = 0$ on zero entries (explicitly guarded on line 436 of `rees_hsp_review.tex` and line 111 of `theorems/uniform_bch_rees.py`) avoids turning $0^0$ into $1$, while nonzero entries map to $1$ with $1^{p-1} = 1 = x_i^{p-1} \pmod p$.
- **Clocks, diamond-norm hybrid, and classical retries (Section 5, Lemma 9, lines 306–368):**
  - Rank failure for $m = n + t$ samples ($t = \lceil \log_p(3/\varepsilon) \rceil$) from $\mathfrak{h}^\perp \cong \mathbb{F}_p^k$ ($k \le n$) is at most $\frac{p^k-1}{p-1} p^{-(n+t)} < \frac{1}{(p-1)p^t} < \frac{\varepsilon}{3}$.
  - Complete-instrument error allocation $\varepsilon / (3 N_{\rm inst})$ across $N_{\rm inst} = N_{\rm leaf} + N_{\rm merge} + N_{\rm read}$ uses unconditional trace/diamond-norm contractivity without dividing by branch probabilities.
  - In Lemma 9, central labels $\boldsymbol{\lambda}$ are already measured and stored classically before controlled dilations are applied, so Las Vegas SDE retries with fresh classical seeds do not re-measure or consume additional quantum states.
- **Derived-dimension FPT and uniform BCH (Section 6, Lemma 10, Corollary 11, lines 370–473):**
  - The actual nilpotency class $c$ is computed first by public linear algebra in $\le n$ strict decreases (resolving `F1`).
  - Lemma 10 solves $Z'(t) = \sum_{k=0}^{c-1} b_k \operatorname{ad}_{Z(t)}^k(Y)$, $Z(0)=X$ through $t$-degree $c$ using $(c-1)\sum_{j=0}^{c-1}\frac{(j+1)(j+2)}{2} = \frac{(c-1)c(c+1)(c+2)}{6}$ Lie brackets and denominators dividing $c!$.
  - In $A_{\le d} = A / \bigoplus_{r>d} A_r$, grade $A_d$ is central and $\Delta_s|_{A_d} = s^d \operatorname{id}_{A_d}$ is scalar, so *every* subspace in a public complete flag of $A_d$ is a $\Delta_s$-invariant Lie ideal without needing alignment to $\widetilde{\mathfrak{h}} \cap A_d$.
- **Direct prime-power Lie rings (Section 7, Proposition 12, lines 475–572):**
  - Vandermonde points $1, \dots, c$ ($c < p$) have unit determinant in $\mathbb{Z}/p^E\mathbb{Z}$.
  - At a cyclic central summand $Z \cong \mathbb{Z}/p^a\mathbb{Z}$ with $|H \cap Z| = p^b$, fresh labels are uniform on $p^b\mathbb{Z}/p^a\mathbb{Z}$. For $b < a$ and batch size $B = \gcd(d, p-1) + 1 \le p$, all $B$ labels have minimal valuation $b$ with probability $(1 - 1/p)^B \ge (1 - 1/p)^p \ge 8/27 > 1/4$ for $p \ge 3$ (and probability $1$ if $b=a$).
  - On an equal-valuation batch $\lambda_i = p^v A_i$ ($p \nmid A_i$), any nonzero mod-$p$ witness has a unit coordinate $s_j \not\equiv 0 \pmod p$ with unit derivative $d A_j s_j^{d-1} \not\equiv 0 \pmod p$ ($d < p$), so univariate Hensel lifting to modulus $p^{a-v}$ produces unit active scales and exact zero inactive scales.
- **Black-box extension, free Lie pullback $F_{s,c}$, and torsion preimage $A[p]$ (Section 8, Corollary 13, lines 574–694):**
  - Both the acquired-chart route and the free class-$c$ nilpotent pullback $\Phi: \exp(F_{s,c}) \twoheadrightarrow G$ are algebraically sound.
  - For $A = K/B = \mathbb{Z}^k / \operatorname{row}_{\mathbb{Z}}(R)$ ($B = K'H_0$, $\det R \ne 0$), $C = \{a \in \mathbb{F}_p^k : aR \equiv 0 \pmod p\} \to A[p]$ via $a \mapsto \widetilde{a}R/p \bmod \operatorname{row}_{\mathbb{Z}}(R)$ is an isomorphism, and adjoining all generators of $B = \ker\pi$ ensures $L = \pi^{-1}(A[p])$ retains a nontrivial order-$p$ element of $(H \cap K)/H_0$ even when that element lies inside $B$.

### 1.4 Minor Non-Fatal Exposition Suggestions for `rees_hsp_review.tex`

1. **Explicitly note determinism of `[Fact 2]{is}` in Proposition 12 (`rees_hsp_review.tex`, line 517):**
   In Proposition 12, the base-run error budget sums $1/16$ (Markov leaf cap at $16MQ$) $+ 1/16$ (channel error) $+ 1/16$ (terminal rank failure) $= 3/16$, without a classical solver failure term. Since Fact 2 of Ivanyos–Santha (quoting van de Woestijne) is a *deterministic* $\mathrm{poly}(\delta_d, \log p)$ algorithm (as already noted in Section 6, line 431), adding the word "deterministic" before "scalar degree-$d$ equation modulo $p$ via \cite[Fact 2]{is}" on line 517 makes it immediately clear why no Lemma 9 retry allowance is needed in the $3/16$ sum.
2. **Slack logarithm base in Section 5 vs. Section 6 (`rees_hsp_review.tex`, line 308 vs. line 448):**
   Line 308 uses $t = \lceil \log_p(3/\varepsilon) \rceil$, whereas Corollary 11 (line 448) writes $M = n + \lceil \log_2(3/\varepsilon) \rceil$. Since $p \ge 3 > 2$, $\lceil \log_2(3/\varepsilon) \rceil \ge \lceil \log_p(3/\varepsilon) \rceil$ is valid and conservative; optionally note that $\log_2$ is a prime-independent upper bound on $\log_p$.
3. **Bridging sentence between semi-elementary descent and $\Omega_1$ in Corollary 13 (`rees_hsp_review.tex`, lines 649–651 & 661–685):**
   In Corollary 13, lines 661–685 descend via $L = \pi^{-1}(A[p])$ until $A = K/(K'H_0)$ is elementary abelian. Because a class-$c < p$ group $K/H_0$ with elementary abelian abelianization is *semi-elementary* (all lower-central factors have exponent $p$) but can still have exponent $p^2$ (e.g., $\langle a,b \mid a^{p^2}=b^p=1, [a,b]=a^p \rangle$), adding a single sentence noting that line 650's restriction to the exponent-$p$ subgroup $\Omega_1(K/H_0)$ is performed after semi-elementary descent via the same relation-lattice torsion construction in Lazard additive coordinates will make the connection between the two paragraphs completely seamless.

---

## 2. Prior-Art Subsumption Analysis in the Growing-Prime Regime (Question 2)

### 2.1 Why Ivanyos–Sanselme–Santha (2007/2012) + $|H| \le p$ Reduction Does Not Solve Class $c \ge 3$
- **What ISS (`arXiv:0707.1260`) provides:** Theorem 1 solves nil-2 HSP ($c \le 2$) for arbitrary $H$ in $\mathrm{poly}(n, \log p)$ time. Section 3 (Theorem 2) reduces HSP in any subgroup- and quotient-closed fixed-class nilpotent family (for $p > c$) to exponent-$p$ groups where $|H| \in \{1, p\}$ ($\mathfrak{h} = \mathbb{F}_p v$).
- **Why nil-2 scaling fails at $c \ge 3$:** In class 2, $[L,L] \le Z(L)$ is central, so when a non-homogeneous line $\mathfrak{h} = \mathbb{F}_p(x + z_0)$ fails to be invariant under $(x, z) \mapsto (ux, u^2 z)$, the discrepancy $(u^2 - u)tz_0$ is already central and produces an extra linear character phase alongside $u^2$. At class $c \ge 3$:
  1. $L$ need not admit any positive grading at all (e.g., the 8D class-3 Dixmier–Lister algebra in Remark 3).
  2. Even when $L = \bigoplus_{r=1}^c V_r$ is graded, dilating a non-homogeneous line $\mathfrak{h} = \mathbb{F}_p(v_1 + v_2 + \dots + v_c)$ with $v_2 \ne 0$ maps $\mathfrak{h}$ outside $\mathfrak{h} + \gamma_c(L)$, violating $\Delta_s(HZ) = HZ$.
- **Why $|H| = p$ does not reduce to the Hidden Polynomial Graph Problem (HPGP):**
  - *Attempt A (Codimension-1 normal subgroup $G = N \rtimes C_p$):* In class $c \ge 3$, any codimension-1 normal subgroup $N$ is generally **non-abelian**. Left multiplication by the random coset representative $n \in N$ introduces non-abelian cross-terms between $n$ and the hidden generator $v$, so different cosets of $H_v$ have *different* polynomials whose lower-degree coefficients depend on the unobserved offset $n$. As proved in `research/HPGP_COSET_INTERFACE_AUDIT.md` (Sections 3–5), any single public fiber-preserving chart covers only a single abelian coset of subgroup parameters ($\le p^{-m}$ of transverse order-$p$ subgroups in $G_m = N^m \rtimes C_p \le \mathrm{UT}_4(\mathbb{F}_p)^m$, with average trace distance $\ge \frac{1}{8}(1 - 1/p)(1 - \mathrm{cp}(N)) \to 1/8$ from any valid HPGP state).
  - *Attempt B (Abelian normal subgroup $N$):* First, at class $c \ge 4$, $[G,G]$ need not be abelian at all (e.g., $\mathrm{UT}_9(\mathbb{F}_p)$ in Section 9). Second, even when an abelian normal $N$ exists with $V = G/N \cong \mathbb{F}_p^m$ ($m \ge 2$), the projection of a 1D hidden subgroup $\mathfrak{h} = \mathbb{F}_p v$ to $V = \mathbb{F}_p^m$ is an *unknown* 1D line $U = \mathbb{F}_p \bar{v} \subset \mathbb{F}_p^m$. The state on $V$ after QFT on $N$ is an incoherent mixture over all $p^{m-1}$ affine cosets of $U$, carrying phase coherence only along the unknown line $U$, rather than a univariate HPGP state or a full-domain multivariate graph state.

### 2.2 Why Imran–Ivanyos (2023/2024) Incurs Exponential Cost in $\log p$ and How Rees Fixes It
- **What Imran–Ivanyos (`arXiv:2304.08376`, QIP 2024) provides:** Lemma 2 and Propositions 2–3 introduce iterative central subgroup state conversion for arbitrary $H$.
- **Why it is bounded-prime only:** Working on the unhomogenized group $G$ without $H$-preserving degree-$d$ dilations, Imran–Ivanyos uses untwisted translations and requires a **non-empty binary zero-sum subsequence** $\sum_{i \in I} \lambda_i = 0$ ($w_i \in \{0,1\}$) for $\lambda_i \in \mathbb{F}_p^r$. Even existentially, the Davenport/Olson threshold is $(p-1)r + 1 = \Omega(p)$ (exponential in $\log p$), and their Theorem 2 requires $S(p,r) = p^{O(p \log^2 p)} r^{O(p \log p)}$. Moreover, their Remark after Theorem 2 explicitly notes that encoding binary weights via Fermat's Little Theorem as $w_i = x_i^{p-1} \in \{0,1\}$ and invoking the Ivanyos–Santha SDE solver uses degree $d = p - 1$, which still costs $p^{\Omega(p^2 \log p)} r^{\Omega(p \log p)}$.
- **What the Rees cover changes:** Lifting $(G, H)$ via $c$ oracle evaluations to $(\exp(A), \widetilde{H})$ makes $\widetilde{H}$ invariant under $\Delta_s$ while scaling grade $d$ by $s^d$. This replaces the degree-$(p-1)$ binary zero-sum equation with the **homogeneous degree-$d$ ($d \le c$) diagonal equation** $\sum_{i=1}^M s_i^d \lambda_i = 0$, reducing the degree from $p - 1$ to $d \le c$ and unlocking the deterministic $\mathrm{poly}_c(n, \log p)$ regime of Ivanyos–Santha Theorem 3.

### 2.3 Why $\operatorname{gr}(L)$, Carnot Dilations, or Free Nilpotent Pullbacks $F_{s,c}$ Alone Fail
- **Associated graded $\operatorname{gr}(L) = \bigoplus_{r=1}^c \gamma_r(L)/\gamma_{r+1}(L)$:** Has no evaluation homomorphism $\operatorname{gr}(L) \to L$ in general, and its grade-1 space is $\operatorname{gr}_1(L) = L/[L,L]$, which erases all derived directions of $\mathfrak{h}$ (returning $0$ whenever $\mathfrak{h} \subseteq [L,L]$). In the positive Rees cover $A$, grade 1 is $A_1 = tL$, retaining all of $\mathfrak{h}$. Moreover, $A$ achieves the minimum possible dimension $\sum_{r=1}^c \dim \gamma_r(L)$ among all positively graded covers $\pi: B \to L$ with $\pi(B_1) = L$ (`research/REES_HSP_REDUCTION.md`, lines 76–84).
- **Free class-$c$ nilpotent pullback $F_{s,c} \twoheadrightarrow L$ (`research/FREE_LAZARD_PULLBACK.md`):** Eliminates target Lie-chart learning in black-box groups, but neither $\ker(\pi: F_{s,c} \twoheadrightarrow L)$ nor $\pi^{-1}(\mathfrak{h})$ is homogeneous under the natural bracket-weight grading of $F_{s,c}$ (e.g., $[a,d] + [b,[a,c]] \in \ker\pi$ in the Dixmier–Lister algebra mixes weights 2 and 3). Positive Rees homogenization is still required on top of $F_{s,c}$.

---

## 3. Assessment of Further Development & Actionable Next Steps (Question 3)

### 3.1 Theoretical Value vs. Practical/Applied Boundaries
- **Theoretical value:** High. If confirmed by human specialists, the manuscript closes the bounded-prime gap for fixed-class nilpotent HSP and unifies the ISS nil-2 scaling trick, Imran–Ivanyos central character conversion, and Ivanyos–Santha fixed-degree SDE solving in a self-contained ~10-page proof, plus a clean $2^{O(r^2 \log(r+2))}\mathrm{poly}(n, \log p)$ FPT bound in $r = \dim[L,L]$.
- **Practical/applied limits:** The worst-case Ivanyos–Santha collision-tree arity $B_d(r_d) = [d^{d(d-1)/2}(r_d+1)^d]^{\lceil \log_2(d+1) \rceil}$ produces query degree $1 + \sum_{d=2}^c d\lceil \log_2(d+1) \rceil$ in $n$ ($11$ at $c=3$; $145$ at $c=9$). Furthermore, explicit matrix, code, and succinct polynomial-circuit stabilizer problems in characteristic-$p$ matrix $p$-groups collapse to classical polynomial time via Luks's solvable matrix-group stabilizer, infinitesimal reverse-gradient PIT, adaptive extension-field orbit-module learning (`research/POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md`), and semantic Moore-gradient recognition (`research/MOORE_GRADIENT_CLASSICAL_FILTER.md`).

### 3.2 Technical Note: Does Pre-Reducing to $|H| = p$ via ISS Section 3 Lower the Rees Arity?
- **No for worst-case asymptotic arity:** At grade $d$, central character labels $\lambda_i$ are uniform on $K_d^\perp \subseteq A_d^\vee \cong \mathbb{F}_p^{r_d}$, where $K_d = \widetilde{\mathfrak{h}} \cap A_d = t^d(\mathfrak{h} \cap \gamma_d(L))$. When $|H| \le p$ ($\dim \mathfrak{h} \le 1$), $\dim K_d \in \{0, 1\}$, so $\dim K_d^\perp \in \{r_d, r_d - 1\}$. Thus the observed character vectors $\lambda_i$ still span an $(r_d - 1)$- or $r_d$-dimensional space and still require the full rank-$r_d$ SDE arity $B_d(r_d)$ (while outer normalizer recursion adds a $b(b+1)$ call factor).
- **Special-case adaptive shortcut when $\mathfrak{h} \subseteq \gamma_k(L)$:** Because $\gamma_c(L) \le Z(L)$ is already central in $L$, running ordinary abelian HSP on $\exp(\gamma_c(L))$ directly learns $\mathfrak{h} \cap \gamma_c(L)$ with $O(r_c)$ queries before forming any Rees cover; more generally, if $|H|=p$ and $\mathfrak{h} \subseteq \gamma_k(L)$ for $k \ge 2$, restricting the ambient algebra to $\gamma_k(L)$ reduces the effective class from $c$ to $\lfloor c/k \rfloor$.

### 3.3 Actionable Next Steps for Codex

1. **Promote and Compile `formal/drafts/ReesHomogenization.lean` into `formal/Formal/`:**
   - `formal/drafts/ReesHomogenization.lean` already contains the Lean 4 proofs of `evaluation_det_ne_zero`, `coefficientwise_iff`, `tuple_hides` (Lemma 2), and `coefficient_translate` / `coefficient_allowed` (Lemma 7's non-transverse $|K|$ multiplicity cancellation).
   - Move/integrate it into `formal/Formal/ReesHomogenization.lean`, connect `coefficient_allowed` to `descent_output` in `formal/Formal/CentralCharacterDescent.lean` (lines 180–198, upgrading the `transverse` hypothesis on lines 31–94 to arbitrary $K = H \cap Z$), and add `#guard_msgs in #print axioms` checks so the core algebraic/channel reduction is kernel-verified.
2. **Apply the Three Minor Exposition Clarifications in `research/manuscripts/rees_hsp_review.tex`:**
   - Line 517: note that `\cite[Fact 2]{is}` is deterministic (explaining why Proposition 12's $3/16$ error budget needs no solver-abort term).
   - Line 448: optionally note that $\lceil \log_2(3/\varepsilon) \rceil$ is a conservative prime-independent upper bound on $\lceil \log_p(3/\varepsilon) \rceil$.
   - Lines 649–651 / 661–685: add one sentence clarifying that in the $p > c$ branch of Corollary 13, once semi-elementary descent on $A = K/(K'H_0)$ terminates with elementary abelian $K/(K'H_0)$, the restriction to $\Omega_1(K/H_0)$ (line 650) is computed via the same relation-lattice torsion construction in Lazard additive coordinates.
3. **Investigate Random-Column Degree-$d$ SDE Arity Reductions (Theoretical Open Problem):**
   - Because Lemma 7 guarantees that the measured central character labels $\lambda_1, \dots, \lambda_M$ are **i.i.d. uniform over the subspace $K_d^\perp \subseteq \mathbb{F}_p^{r_d}$** (rather than worst-case adversarial columns), investigate whether a nonzero solution to $\sum_{i=1}^M s_i^d \lambda_i = 0$ for i.i.d. uniform $\lambda_i \sim \mathrm{Unif}(K_d^\perp)$ can be found in $\mathrm{poly}(r_d, \log p)$ time with $M = O_d(r_d)$ or $O_d(r_d^2)$ columns instead of the worst-case collision bound $B_d(r_d) = \Theta_d(r_d^{d\lceil \log_2(d+1) \rceil})$.
