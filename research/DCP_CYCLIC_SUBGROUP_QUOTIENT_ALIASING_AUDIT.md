# DCP Cyclic-Subgroup Quotient-Aliasing Audit: $g$-Fold Coset Indistinguishability, Euler–Ramanujan Divisor-Stratum Sum, and Folded-Kernel Parseval Identity

## 1. Motivation and Scope

When the Dihedral Coset Problem (DCP) is instantiated over a composite modulus $q$ (such as $q = 2^r, 3^r$, or smooth composite $q$), a pair state $|x\rangle + \omega_q^{d(s+e)}|x+d\rangle$ with difference $d \in \{1, \dots, q-1\}$ has greatest common divisor $g := \gcd(d, q) \in \{g' : g' \mid q,\; 1 \le g' < q\}$. Writing $m := q/g$ and $d = g d'$ with $\gcd(d', m) = 1$, the phase factor $\omega_q^{d(s+e)} = \omega_m^{d'(s+e)}$ depends on $s$ and $e$ only modulo $m = q/g$.

This note proves three exact theorems governing quotient-group aliasing across all divisor strata of $\mathbb{Z}_q$: exact $g$-fold secret-coset periodicity and folded-kernel visibility invariance, the Euler totient / Ramanujan-sum stratum identity, and the quotient-subgroup Parseval purity law.

## 2. Theorem 1 — Exact $g$-Fold Secret-Coset Aliasing and Folded-Kernel Visibility Invariance

For any divisor $g \mid q$ ($1 \le g < q$), let $m := q / g$ and define the **$g$-folded noise kernel** on $\mathbb{Z}_m$:
$$
K_\eta^{(m)}(\bar{e}) \;:=\; \sum_{k=0}^{g-1} K_\eta(\bar{e} + k m), \qquad \bar{e} \in \{0, 1, \dots, m - 1\}.
$$

**Theorem 1 (Exact Coset Periodicity and Folded Visibility Identity).**
For every difference $d \in \{1, \dots, q-1\}$ with $g = \gcd(d, q)$, $m = q/g$, and $d' = d/g$:
1. **Exact $m$-Periodicity in Secret $s$**: For every secret $s \in \mathbb{Z}_q$ and every $k \in \{0, \dots, g-1\}$,
   $$
   \rho_d\bigl((s + k m) \bmod q;\; K_\eta\bigr) \;=\; \rho_d(s; K_\eta),
   $$
   so $\rho_d(s; K_\eta)$ carries zero information about the coset index $\lfloor s / m \rfloor \in \mathbb{Z}_g$.
2. **Exact Folded Visibility Identity**: The $d$-th harmonic visibility of $K_\eta$ on $\mathbb{Z}_q$ equals the $d'$-th harmonic visibility of the folded kernel $K_\eta^{(m)}$ on $\mathbb{Z}_m$:
   $$
   \lambda_d(K_\eta) \;:=\; \sum_{e=0}^{q-1} K_\eta(e)\cos\!\left(\frac{2\pi d e}{q}\right)
   \;=\; \sum_{\bar{e}=0}^{m-1} K_\eta^{(m)}(\bar{e})\cos\!\left(\frac{2\pi d' \bar{e}}{m}\right) \;=:\; \lambda_{d'}\!\bigl(K_\eta^{(m)}\bigr).
   $$

## 3. Theorem 2 — Euler Totient Partition and Ramanujan-Sum Stratum Identity

Partition $\{1, \dots, q-1\}$ into divisor strata $\mathcal{D}_g(q) := \{d \in \{1, \dots, q-1\} : \gcd(d, q) = g\}$ for proper divisors $g \mid q$ ($1 \le g < q$). For each integer $m \ge 2$ and $e \in \mathbb{Z}$, let
$$
c_m(e) \;:=\; \sum_{\substack{1 \le u \le m \\ \gcd(u, m) = 1}} \cos\!\left(\frac{2\pi u e}{m}\right)
$$
denote **Ramanujan's trigonometric sum**.

**Theorem 2 (Exact Divisor-Stratum Cardinality and Ramanujan-Sum Visibility Total).**
1. For each proper divisor $g \mid q$, $|\mathcal{D}_g(q)| = \varphi(q/g)$, and $\sum_{g \mid q,\, g < q} \varphi(q/g) = q - 1$.
2. The sum of harmonic visibilities across the divisor stratum $\mathcal{D}_g(q)$ is given exactly by the $K_\eta$-expectation of Ramanujan's sum $c_{q/g}(e)$:
   $$
   \sum_{d \in \mathcal{D}_g(q)} \lambda_d(K_\eta) \;=\; \sum_{e=0}^{q-1} K_\eta(e)\,c_{q/g}(e).
   $$

## 4. Theorem 3 — Exact Quotient-Subgroup Parseval Identity for Folded Kernel Purity

**Theorem 3 (Subgroup Parseval Identity and Monotone Purity Under Folding).**
For every divisor $g \mid q$ ($1 \le g \le q$) with $m = q/g$:
1. The $\ell_2$ collision purity of the folded kernel $K_\eta^{(m)}$ on $\mathbb{Z}_m$ equals the average of $\lambda_{k g}(K_\eta)^2$ over the $g$-divisible frequency subgroup $g\mathbb{Z}_q = \{0, g, 2g, \dots, (m-1)g\}$:
   $$
   \bigl\|K_\eta^{(m)}\bigr\|_2^2 \;:=\; \sum_{\bar{e}=0}^{m-1} \bigl(K_\eta^{(m)}(\bar{e})\bigr)^2
   \;=\; \frac{1}{m}\sum_{k=0}^{m-1} \lambda_{k g}(K_\eta)^2
   \;=\; \frac{g}{q}\sum_{k=0}^{q/g - 1} \lambda_{k g}(K_\eta)^2.
   $$
2. Because $K_\eta(e) \ge 0$, $\bigl(\sum_{k=0}^{g-1} K_\eta(\bar{e} + k m)\bigr)^2 \ge \sum_{k=0}^{g-1} K_\eta(\bar{e} + k m)^2$, so $\|K_\eta^{(q/g)}\|_2^2 \ge \|K_\eta\|_2^2$ for every divisor $g \mid q$.
