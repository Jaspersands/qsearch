# Planted $q$-Ary Classical Attack Threshold Bridge: Free-Support Lower Bounds, LLL $\lambda_2$ Isolation Guarantee, and $O(1)$-Space Free-Coordinate Kernel Search

## 1. Motivation and Scope

In `theorems/planted_qary_usvp_source.py`, each generated $q$-ary modular kernel instance $\Lambda_q^\perp(H) = \ker(H \bmod q) \subset \mathbb{Z}^n$ ($1 \le m < n - 1$) is benchmarked against three public-data classical attacks:
1. `sparse_column_attack(problem)` (checking unit vectors and signed column pairs of $H \bmod q$),
2. `public_LLL_attack(problem)` (exact-Gram FLINT LLL on the public centered-RREF row basis $B$), and
3. `ternary_MITM_attack(problem)` (meet-in-the-middle syndrome collision over $\{-1, 0, 1\}^{\lfloor n/2 \rfloor}$ and $\{-1, 0, 1\}^{n - \lfloor n/2 \rfloor}$ using $3^{\lfloor n/2 \rfloor} + 3^{n - \lfloor n/2 \rfloor}$ states and $O(3^{\lfloor n/2 \rfloor})$ hash-table storage).

This note proves three exact theorems connecting the centered-RREF structure of $H \bmod q$ to these classical attacks, establishing:
- the sharp free-column support lower bound $s_F \ge \max(1, s - m)$,
- the exact LLL isolation threshold $\lambda_2(\Lambda_q^\perp(H)) > \alpha^{(n-1)/2}\sqrt{s}$ and why increasing $q$ at fixed $(n, m, s)$ makes $u$ **easier** (not harder) for LLL to recover, and
- an $O(1)$-memory RREF free-coordinate kernel search that uses at most $3^{n-m}$ states (and $\frac{3^{n-m} - 1}{2}$ projectively oriented states), strictly beating $O(3^{n/2})$-space full-ambient MITM whenever $m \ge \lceil n/2 \rceil$.

## 2. Theorem 1 — Sharp Free-Support Lower Bound and Column-Pair Immunity

Let $u \in \{-1, 0, 1\}^n \setminus \{0\}$ be a planted ternary vector in $\Lambda_q^\perp(H)$ with total Hamming support $s = \|u\|_1 = \|u\|_2^2$, and let $(P, F)$ ($|P| = m, |F| = n - m$) be the pivot and free column partition of $\operatorname{RREF}(H \bmod q)$.

**Theorem 1 (Free-Column Support Lower Bound and Sparse-Column Immunity).**
1. **Sharp free-support lower bound**: Since $s_P = |\operatorname{supp}(u) \cap P| \le |P| = m$ and $u \ne 0 \implies s_F \ge 1$ (for $q \ge 3$), the free-column support $s_F = |\operatorname{supp}(u) \cap F|$ satisfies
   $$
   \max(1,\; s - m) \;\le\; s_F \;\le\; \min(s,\; n - m).
   $$
   In particular, for dense plants with $s = n$, every free column is active: $s_F = n - m$.
2. **Immunity to `sparse_column_attack` for unique plants of support $s \ge 3$**: Whenever $s \ge 3$ and $\Lambda_q^\perp(H)$ contains no nonzero non-parallel vector of Euclidean norm $\le \sqrt{2}$, `sparse_column_attack(problem)` returns `NO_UNIT_OR_COLUMN_PAIR_RELATION`, because every unit vector has $\|e_j\|_2^2 = 1 < 3 \le \|u\|_2^2$ and every signed column pair has $\|e_i \pm e_j\|_2^2 = 2 < 3 \le \|u\|_2^2$.

## 3. Theorem 2 — Exact LLL $\lambda_2$-Isolation Guarantee and Large-$q$ Monotonicity

Let $\delta \in (1/4, 1]$ be the LLL reduction parameter and $\alpha = \frac{1}{\delta - 1/4}$ be the Lovász factor ($\alpha = 4/3$ at $\delta = 3/4$).

**Theorem 2 (LLL Unique-SVP Isolation Criterion and Large-$q$ Scaling).**
1. **Unconditional LLL isolation above the $\alpha^{(n-1)/2}$ gap**: Let $(b_1, \dots, b_n)$ be any $\delta$-LLL-reduced basis of $\Lambda_q^\perp(H)$. For any nonzero primitive lattice vector $u \in \Lambda_q^\perp(H)$,
   $$
   \|b_1\|_2 \;\le\; \alpha^{(n-1)/2}\,\|u\|_2 \;=\; \alpha^{(n-1)/2}\,\sqrt{s}.
   $$
   Consequently, if the second successive minimum satisfies
   $$
   \lambda_2\bigl(\Lambda_q^\perp(H)\bigr) \;>\; \alpha^{(n-1)/2}\,\sqrt{s},
   $$
   then $b_1$ cannot be non-parallel to $u$, so the shortest reduced basis vector of `public_LLL_attack` is **guaranteed** to equal $\pm u$.
2. **Large-$q$ monotonicity at fixed $(n, m, s)$**: Because $\|u\|_2 = \sqrt{s}$ is independent of $q$ while $\det(\Lambda_q^\perp(H)) = q^m$ grows with $q$, increasing the modulus $q$ at fixed $(n, m, s)$ increases the determinant-normalized gap $q^{m/n} / \sqrt{s}$ without increasing $\|u\|_2$, making `public_LLL_attack` strictly more effective as $q \to \infty$ (explaining why the $q > 2^{80}$ control in `planted_qary_usvp_source.py` is recovered immediately by LLL).

## 4. Theorem 3 — $O(1)$-Space Projective Free-Coordinate RREF Search vs Ambient MITM

In `PublicQaryLattice`, the centered RREF matrix $C \in [-(q-1)/2, (q-1)/2]^{m \times (n-m)}$ expresses the $m$ pivot coordinates uniquely modulo $q$ in terms of the $n - m$ free coordinates:
$$
u_{P_i} \;\equiv\; -\sum_{j=0}^{n-m-1} C_{i,j} u_{F_j} \pmod q \qquad (0 \le i < m).
$$

**Theorem 3 (Projective Free-Coordinate Enumeration).**
1. **Bijection with valid free-coordinate assignments**: A nonzero vector $u \in \{-1, 0, 1\}^n \setminus \{0\}$ belongs to $\ker(H \bmod q)$ if and only if $u_F \in \{-1, 0, 1\}^{n-m} \setminus \{0\}$ and for every pivot row $0 \le i < m$,
   $$
   u_{P_i} \;=\; \operatorname{centered\_mod}\!\left(-\sum_{j=0}^{n-m-1} C_{i,j} u_{F_j},\; q\right) \;\in\; \{-1, 0, 1\}.
   $$
2. **Projective sign-canonical search in $\frac{3^{n-m} - 1}{2}$ states and $O(1)$ space**: Restricting $u_F \in \{-1, 0, 1\}^{n-m} \setminus \{0\}$ to have its first nonzero coordinate equal to $+1$ checks exactly
   $$
   N_{\text{free,proj}}(n, m) \;=\; \frac{3^{n-m} - 1}{2}
   $$
   states in $O(1)$ auxiliary memory, compared to $N_{\text{MITM}}(n) = 3^{\lfloor n/2 \rfloor} + 3^{n - \lfloor n/2 \rfloor}$ states and $O(3^{\lfloor n/2 \rfloor})$ table entries for ambient `ternary_MITM_attack`. Whenever $m \ge \lceil n/2 \rceil$,
   $$
   \frac{3^{n-m} - 1}{2} \;<\; \frac{1}{4}\bigl(3^{\lfloor n/2 \rfloor} + 3^{n - \lfloor n/2 \rfloor}\bigr),
   $$
   so projective RREF free-coordinate search strictly dominates ambient MITM in **both** state count and memory.
