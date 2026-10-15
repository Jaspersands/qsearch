# Planted q-Ary Partner-Survival Frontier and Conditional Source Geometry

## Corrected Scope

This report bounds the failure of an intended partner event. It does NOT
certify a DCP bad-register rate without the at-most-two/common-partner
geometry promise. Previous wording conflated these events. Every occurrence
of `p_bad` in the product calculations below means **partner failure**, and
becomes a DCP bad-register bound only under that independent promise.

The live audit uses the private planted vector to select a hitting coordinate
and support-sensitive parameters. This is calibration, not a public selector.
A public implementation can schedule conservatively with `s=n, s_F=n-m`
and pay for all `n-m` coordinate trials; that still does not prove geometry.

## 1. Motivation and Scope

In `theorems/lattice_cube_coset_source.py`, `offset_average_pair_mass(box, width, delta, displacement)` computes the exact probability that a random input $(t, a) \in \{0, 1\} \times \{0, \dots, M_{\text{box}}-1\}^n$ and a uniformly random offset vector $\text{offsets} \in \{1, \dots, W\}^n$ place $(t, a)$ and its shifted partner $(1-t, a + (-1)^t \delta)$ inside the same cube of width $W$:
$$
P_{\text{good}}(M_{\text{box}}, W; \delta, u)
\;=\; P_{\text{box}}(M_{\text{box}}, \delta) \cdot P_{\text{cube}}(W, u),
$$
where
$$
P_{\text{box}}(M_{\text{box}}, \delta) \;:=\; \prod_{k=0}^{n-1} \frac{\max(0, M_{\text{box}} - |\delta_k|)}{M_{\text{box}}},
\qquad
P_{\text{cube}}(W, u) \;:=\; \prod_{i=0}^{n-1} \frac{\max(0, W - |u_i|)}{W}.
$$
Meanwhile, `theorems/lattice_cube_dcp_readout.py` evaluates the Regev $f_1$ bad-register budget
$$
p_{\text{bad}} \;=\; 1 - P_{\text{good}}(M_{\text{box}}, W; \delta, u) \;\le\; \frac{1}{\ell},
\qquad
\ell \;=\; \log_2 N \;=\; n \log_2(2 M_{\text{box}}) \;=\; n(b + 1),
$$
where $M_{\text{box}} = 2^b$ and $W = 2^w$.

This note proves three exact theorems giving the closed-form product factorization of $P_{\text{good}}$ for planted ternary $q$-ary instances and an explicit $q$-independent dyadic schedule $(M_{\text{box}} = 2^b, W = 2^w)$ that certifies $p_{\text{bad}} \le 1/\ell$ without LLL or BKZ basis reduction.

## 2. Theorem 1 — Exact Cube-Displacement Survival Factor for Ternary Vectors

**Theorem 1 (Support-Only Cube Survival Law).**
For any planted ternary vector $u \in \{-1, 0, 1\}^n \setminus \{0\}$ with Hamming support $s = \operatorname{supp}(u) = \|u\|_1 = \|u\|_2^2 \in \{1, \dots, n\}$ and any dyadic cube width $W \ge 2$, the cube-boundary survival factor depends solely on $W$ and $s$:
$$
P_{\text{cube}}(W, u)
\;=\; \left(1 - \frac{1}{W}\right)^s,
$$
and satisfies the two-sided rational enclosure
$$
1 - \frac{s}{W} \;\le\; P_{\text{cube}}(W, u) \;\le\; \frac{1}{1 + s / W}.
$$

*Proof.*
Each of the $s$ coordinates $i \in \operatorname{supp}(u)$ has $|u_i| = 1$ and contributes $(W - 1)/W = 1 - 1/W$, while each of the $n - s$ coordinates $i \notin \operatorname{supp}(u)$ has $|u_i| = 0$ and contributes $W/W = 1$. Bernoulli's inequality on $(1 - 1/W)^s$ gives the lower bound $1 - s/W$, and Bernoulli's inequality on $(1 - 1/W)^{-s} \ge (1 + 1/W)^s \ge 1 + s/W$ gives the upper bound. $\square$

## 3. Theorem 2 — Exact Worst-Case Multiplicative Box Survival Bound

Let $B \in \mathbb{Z}^{n \times n}$ be the public centered-RREF kernel basis of `PublicQaryLattice` (`theorems/planted_qary_usvp_source.py`), and let $s_F = \operatorname{supp}_F(u) \in [1, \min(s, n - m)]$ be the free-column support of $u$. By Theorems 3 and 4 of `planted_qary_cube_basis_coordinate_bridge`, on any hitting free coordinate $j_{\text{coord}} = m + j_0$ with $u_{F_{j_0}} = +1$ and deterministic $(p_{\text{split}} = \operatorname{nextprime}(W), g_{\text{res}} = 1)$, the partner box shift $\delta = (\delta_{\text{piv}}, \delta_{\text{free}})$ satisfies:
- $\delta_{j_{\text{coord}}} = 0$,
- $|\delta_{m+j}| = |u_{F_j}| \in \{0, 1\}$ with $\sum_{j \ne j_0} |\delta_{m+j}| = s_F - 1$, and
- $|\delta_{\text{piv}, i}| \le B_{\text{tern}}(s_F)$ for all $0 \le i < m$.

**Theorem 2 (Multiplicative and Additive Box Survival Bounds).**
For any $M_{\text{box}} > B_{\text{tern}}(s_F)$, the exact box survival factor satisfies
$$
P_{\text{box}}(M_{\text{box}}, \delta)
\;=\; \left(1 - \frac{1}{M_{\text{box}}}\right)^{s_F - 1} \prod_{i=0}^{m-1} \left(1 - \frac{|\delta_{\text{piv}, i}|}{M_{\text{box}}}\right)
\;\ge\; P_{\text{box}}^{\min}(M_{\text{box}}, m, s_F)
\;:=\; \left(1 - \frac{1}{M_{\text{box}}}\right)^{s_F - 1}\left(1 - \frac{B_{\text{tern}}(s_F)}{M_{\text{box}}}\right)^m,
$$
and the additive union bound
$$
1 - P_{\text{box}}(M_{\text{box}}, \delta)
\;\le\; 1 - P_{\text{box}}^{\min}(M_{\text{box}}, m, s_F)
\;\le\; \frac{(s_F - 1) + m\, B_{\text{tern}}(s_F)}{M_{\text{box}}}.
$$

## 4. Theorem 3 — Explicit $q$-Independent Dyadic $(M_{\text{box}}, W)$ Schedule for the $1/\ell$ Budget

**Theorem 3 (Modulus-Independent $1/\ell$ Bad-Register Schedule).**
For any dimension $n$, constraint count $m$, total support $s \in [1, n]$, and free-column support $s_F \in [1, \min(s, n - m)]$, define the worst-case box L1 ceiling
$$
L_{\text{box}}(m, s_F) \;:=\; (s_F - 1) + m\, B_{\text{tern}}(s_F).
$$
For any dyadic box size $M_{\text{box}} = 2^b$ ($b \ge 1$) and dyadic cube width $W = 2^w$ ($w \ge 1$), the offset-averaged bad-register rate $p_{\text{bad}} = 1 - P_{\text{box}}(M_{\text{box}}, \delta) P_{\text{cube}}(W, u)$ satisfies
$$
p_{\text{bad}}
\;\le\; 1 - P_{\text{box}}^{\min}(2^b, m, s_F)\left(1 - \frac{1}{2^w}\right)^s
\;\le\; \frac{L_{\text{box}}(m, s_F)}{2^b} + \frac{s}{2^w}.
$$
In particular, selecting the smallest integer $b \ge 1$ such that
$$
2^b \;\ge\; \max\bigl(2,\, 2 n (b + 1) L_{\text{box}}(m, s_F)\bigr)
$$
and setting
$$
w \;=\; \left\lceil \log_2\bigl(2 n (b + 1) s\bigr) \right\rceil
$$
guarantees both $\frac{L_{\text{box}}(m, s_F)}{2^b} \le \frac{1}{2\ell}$ and $\frac{s}{2^w} \le \frac{1}{2\ell}$, certifying
$$
p_{\text{bad}} \;\le\; \frac{1}{\ell} \;=\; \frac{1}{n(b + 1)}
$$
for **every** prime modulus $q \ge 3$ without LLL or BKZ reduction.

## 5. Geometry Obligation and Falsifier

For integer points in one width-`W` cell, each coordinate difference is at
most `W-1`, so its squared norm is at most `n*(W-1)^2`. Thus a separately
verified strict lower bound `L>n*(W-1)^2` on all nonparallel lattice vectors
excludes them from a cell. For a primitive ternary vector and a hitting
free-coordinate trial, prime splitting with `p-1>=W` excludes unwanted
collinear multiples. These are conditional sufficient inequalities, not a
method for certifying the lattice's successive minima. A generator's
distributional gap ledger is not individual-instance certification.

The existing frontier controls were generated with relative gap parameter
two. That promise alone does not meet the new geometry inequality at their
scheduled widths; the report now records this failure rather than granting
source validity.

An explicit counterexample uses `q=3`, `H=(1,1,1)`, and public row basis
`((3,0,0),(-1,1,0),(-1,0,1))`. The ternary vector `(1,1,1)` is in this
kernel. Its schedule is `M=128, W=256`, with splitting prime `257` and
coordinate one. At offsets `(1,1,1)`, the distinct same-colour inputs
`(0,0,2)` and `(0,0,3)` map to points `(-2,0,2)` and `(-3,0,3)`, both in
cell `(-1,-1,0)`. Partner failure is below `1/24`, but the two-point source
promise is false. This falsifies the unconditional transfer, not the
partner-survival product identity or a correctly promised lattice reduction.

The independent BigInt checker replays this collision and rejects promotion
of unresolved source geometry into a certified bad-register budget.
