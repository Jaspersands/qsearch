# Planted $q$-Ary Kernel Basis Coordinate Bounds, $q$-Independent Cube Shifts, and Deterministic Prime/Residue Selection

## 1. Motivation and Scope

In `theorems/planted_qary_usvp_source.py`, a public $q$-ary lattice instance is specified by a full-row-rank parity-check matrix $H \in \mathbb{Z}_q^{m \times n}$ ($1 \le m < n$) and its modular kernel lattice
$$
\Lambda_q^\perp(H) \;=\; \{\, x \in \mathbb{Z}^n : H x \equiv 0 \pmod q \,\},
\qquad \det(\Lambda_q^\perp(H)) = q^m.
$$
The public row basis $B \in \mathbb{Z}^{n \times n}$ of $\Lambda_q^\perp(H)$ is constructed directly from the modular row-reduced echelon form (RREF) of $H \bmod q$ with centered non-pivot residues in $[-(q-1)/2, (q-1)/2]$ — without running LLL or BKZ reduction.

When this public basis $B$ is fed into the Regev-style cube-coset quantum source `CubeCosetSource` (`theorems/lattice_cube_coset_source.py`), any short planted vector $u \in \Lambda_q^\perp(H)$ induces a basis-coefficient shift vector
$$
d \;=\; u B^{-1} \;\in\; \mathbb{Z}^n \qquad \left(\text{so that } u = \sum_{k=0}^{n-1} d_k B_{k,\bullet}\right).
$$
Three structural questions govern the source quality and outer-loop overhead of this bridge:
1. **Modulus-independence of $\|d\|_1$ and $p_{\text{bad}}$**: Since $B$ has entries of magnitude up to $q$ (with $q$ reaching $2^{80}$ in the control suite), can the basis coordinates $d = u B^{-1}$ grow with $q$, or are they bounded purely in terms of $n, m$, and $\|u\|_\infty$?
2. **Nonzero free-column support**: Can a nonzero short kernel vector $u \in (-q/2, q/2)^n \cap \Lambda_q^\perp(H)$ ever be supported purely on the $m$ pivot columns?
3. **Colinear-multiple cube separation and outer-guessing collapse**: In `CubeCosetSource` with cube width $W$, how must the splitting prime $p_{\text{split}}$ and residue guess $g_{\text{res}}$ be chosen so that multiples $k u$ ($|k| \ge 2$) never collide inside a cube of width $W$, and how many outer trials are required?

This note proves four exact theorems answering all three questions.

## 2. Theorem 1 — Centered-RREF Basis-Coordinate Decomposition

Let $P = (P_0, \dots, P_{m-1})$ and $F = (F_0, \dots, F_{n-m-1})$ be the pivot and free column indices of $\operatorname{RREF}(H \bmod q)$, and let $C \in [-(q-1)/2, (q-1)/2]^{m \times (n-m)}$ be the centered non-pivot block so that $(H_{\text{rref}})_{i, P_{i'}} = \delta_{i, i'}$ and $(H_{\text{rref}})_{i, F_j} \equiv C_{i,j} \pmod q$.

The public kernel row basis $B \in \mathbb{Z}^{n \times n}$ in `PublicQaryLattice` consists of:
- $m$ pivot rows $B_{i,\bullet} = q e_{P_i}^T$ for $i \in \{0, \dots, m-1\}$, and
- $n - m$ free rows $B_{m+j,\bullet} = e_{F_j}^T - \sum_{i=0}^{m-1} C_{i,j} e_{P_i}^T$ for $j \in \{0, \dots, n-m-1\}$.

**Theorem 1 (Exact Basis-Coordinate Formula).**
For every lattice vector $u \in \Lambda_q^\perp(H)$, its unique integer row-basis coordinate vector $d = (d_{\text{piv}}, d_{\text{free}}) \in \mathbb{Z}^m \times \mathbb{Z}^{n-m}$ satisfying $u = d B$ is given by
$$
d_{\text{free}, j} \;=\; u_{F_j} \qquad (0 \le j < n - m)
$$
and
$$
d_{\text{piv}, i} \;=\; \frac{u_{P_i} + \sum_{j=0}^{n-m-1} C_{i,j} u_{F_j}}{q} \;\in\; \mathbb{Z} \qquad (0 \le i < m).
$$

*Proof.* Examining the free coordinates $F_j$ of $\sum_{i=0}^{m-1} d_{\text{piv}, i} B_{i,\bullet} + \sum_{j=0}^{n-m-1} d_{\text{free}, j} B_{m+j,\bullet} = u$ immediately yields $d_{\text{free}, j} = u_{F_j}$ because $B_{m+j,\bullet}$ is the only row of $B$ with a nonzero entry in column $F_j$ (namely $1$). Substituting $d_{\text{free}, j} = u_{F_j}$ into the pivot coordinate $P_i$ gives
$$
q\, d_{\text{piv}, i} - \sum_{j=0}^{n-m-1} C_{i,j} u_{F_j} \;=\; u_{P_i},
$$
which rearranges to the stated formula. Since $u \in \ker(H \bmod q) = \ker(H_{\text{rref}} \bmod q)$, the numerator $u_{P_i} + \sum_j C_{i,j} u_{F_j}$ is divisible by $q$, so $d_{\text{piv}, i} \in \mathbb{Z}$. $\square$

## 3. Theorem 2 — Nonzero Free-Column Support Invariant

**Theorem 2 (Positive Free Support for Short Kernel Vectors).**
Let $u \in (-q/2, q/2)^n \cap \Lambda_q^\perp(H)$ be any nonzero short kernel vector. Then its free-column support
$$
s_F \;=\; \operatorname{supp}_F(u) \;=\; \bigl|\{\, j \in \{0, \dots, n-m-1\} : u_{F_j} \ne 0 \,\}\bigr| \;\ge\; 1.
$$

*Proof.* Suppose for contradiction that $u_{F_j} = 0$ for all $0 \le j < n - m$. Then for every pivot row $0 \le i < m$, the RREF parity-check equation reads $u_{P_i} + \sum_j C_{i,j} u_{F_j} = u_{P_i} \equiv 0 \pmod q$. Since $|u_{P_i}| < q/2$, the only multiple of $q$ in $(-q/2, q/2)$ is $0$, forcing $u_{P_i} = 0$ for all $i$ and hence $u = 0$, a contradiction. $\square$

## 4. Theorem 3 — Modulus-Independent Pivot-Coordinate and Cube-Shift Bounds

**Theorem 3 (Modulus-Independent Coordinate Bounds).**
Let $u \in [-U, U]^n \cap \Lambda_q^\perp(H)$ be a short kernel vector with $1 \le U < q/2$ and free-column support $s_F = \operatorname{supp}_F(u) \ge 1$.
1. **General short vector bound**: For every pivot index $0 \le i < m$,
   $$
   |d_{\text{piv}, i}| \;\le\; \left\lfloor \frac{U \, s_F}{2} \right\rfloor \;\le\; \left\lfloor \frac{U (n - m)}{2} \right\rfloor,
   $$
   independently of the prime modulus $q$.
2. **Modulus-uniform ternary envelope ($U = 1$, $u \in \{-1, 0, 1\}^n \setminus \{0\}$)**: For any odd prime $q \ge 3$,
   $$
   |d_{\text{piv}, i}| \;\le\; B_{\text{tern}}(s_F) \;:=\;
   \begin{cases}
   0, & s_F = 1,\\[2pt]
   1, & s_F = 2,\\[2pt]
   \bigl\lfloor (s_F - 1)/2 \bigr\rfloor, & s_F \ge 3,
   \end{cases}
   \qquad \text{and} \qquad
   \|d\|_1 \;\le\; s_F + m\, B_{\text{tern}}(s_F).
   $$
   This envelope need not be attainable at a specified modulus. The exact
   fixed-modulus maximum is
   `B_q(s_F) = floor((1 + s_F*(q-1)/2)/q)`.

*Proof.*
For part 1, $|u_{P_i}| \le U$ and $|C_{i,j}| \le (q-1)/2$ for each of the $s_F$ nonzero free coordinates $u_{F_j}$ (which satisfy $|u_{F_j}| \le U$). Hence
$$
\bigl|u_{P_i} + \sum_{j=0}^{n-m-1} C_{i,j} u_{F_j}\bigr|
\;\le\; U + s_F U \frac{q-1}{2}
\;=\; q \frac{U s_F}{2} - \frac{U (s_F - 2)}{2}.
$$
For $s_F \ge 2$, dividing by $q$ gives $|d_{\text{piv}, i}| \le \lfloor U s_F / 2 \rfloor$. For $s_F = 1$, the numerator is at most $U + U(q-1)/2 = U(q+1)/2$; since $d_{\text{piv}, i} \in \mathbb{Z}$ and $U < q/2$, $|d_{\text{piv}, i}| \le \lfloor U/2 + U/(2q) \rfloor = \lfloor U/2 \rfloor = \lfloor U s_F / 2 \rfloor$.

For part 2 ($U = 1$), dividing $1 + s_F(q-1)/2$ by $q$ yields
$$
|d_{\text{piv}, i}| \;\le\; \left\lfloor \frac{s_F}{2} - \frac{s_F - 2}{2q} \right\rfloor.
$$
When $s_F = 1$, the bound is zero; when $s_F = 2$, it is one.
For $s_F\ge3$, the positive subtraction makes the floor at most
`floor((s_F-1)/2)`, but equality does NOT hold for every `q`. For example,
`q=3, s_F=9` gives `B_q=3`, not the uniform envelope `4`.

The fixed-modulus bound is attained as follows. Set all free entries of `u`
to one. If `k=B_q(s_F)>0`, set the first pivot entry to one and choose
`s_F` centered residues in `[0,(q-1)/2]` summing to `k*q-1`. Such residues
exist because every integer in `[0,s_F*(q-1)/2]` is representable this way.
If `k=0`, take that pivot entry and all residues zero. Other rows have zero
residues and pivot entries zero; the systematic pivot identity gives full
row rank. This supplies a nonzero ternary kernel vector attaining `k`.
The uniform envelope is sharp over moduli: sufficiently large odd prime `q`
attains it. It is not fixed-modulus sharpness. $\square$

The old `build_extremal_pivot_coordinate_witness` diagnostic was removed:
it bounded free coordinates by U but allowed larger pivot coordinates, so
some examples violated the claimed full-vector norm premise. The exact
ternary witnesses above replace it and check EVERY vector coordinate.

### Source-Validity Boundary

These coordinate bounds and the splitting rule exclude unwanted collinear
multiples, not unrelated short lattice vectors. A hitting coordinate selected
using the private planted vector is an audit calibration; a public algorithm
must execute or otherwise pay for its coordinate trials. Cube source validity
still requires an independent nonparallel-vector separation promise. See
`PLANTED_QARY_OFFSET_PAIR_MASS_FRONTIER_AUDIT.md` for an explicit counterexample
to promoting partner survival into unconditional DCP source quality.

## 5. Theorem 4 — Colinear-Multiple Cube Separation and Deterministic $(p_{\text{split}}, g_{\text{res}})$

In `CubeCosetSource` (`theorems/lattice_cube_coset_source.py`), the input domain $\{0, 1\} \times \{0, \dots, M_{\text{box}}-1\}^n$ maps $(t, a)$ to the lattice point
$$
x(t, a) \;=\; \sum_{k \ne j_{\text{piv}}} a_k B_{k,\bullet} \;+\; (p_{\text{split}} a_{j_{\text{piv}}} + t\, g_{\text{res}}) B_{j_{\text{piv}},\bullet},
$$
and partitions $\mathbb{R}^n$ into cubes of width $W$.

**Theorem 4 (Colinear-Multiple Separation and Deterministic Free-Coordinate Splitting).**
Let $u \in \{-1, 0, 1\}^n \setminus \{0\}$ be a planted ternary kernel vector in $\Lambda_q^\perp(H)$.
1. **Colinear-multiple obstruction for $p_{\text{split}} \le W$**: Because $\|u\|_\infty = 1$, every integer multiple $k u$ has $\|k u\|_\infty = |k|$. If $p_{\text{split}} < W$ (for instance $p_{\text{split}} = 3$ with $W \ge 4$), then two same-colour inputs $(0, a)$ and $(0, a')$ differing by $p_{\text{split}} u$ have $\|x(0, a') - x(0, a)\|_\infty = p_{\text{split}} < W$ and collide inside the same cube of width $W$ with positive probability, violating the two-point cube promise.
2. **Deterministic prime and residue choice ($p_{\text{split}} = \operatorname{nextprime}(W)$, $g_{\text{res}} = 1$)**: By Theorem 2, at least one free basis coordinate $j_{\text{piv}} = m + j_0 \in \{m, \dots, n-1\}$ satisfies $d_{j_{\text{piv}}} = u_{F_{j_0}} \in \{-1, +1\}$. Orienting $\pm u$ so that $d_{j_{\text{piv}}} = +1$, for **every** prime $p_{\text{split}} \ge W + 1$:
   - $d_{j_{\text{piv}}} = 1 \equiv 1 \pmod{p_{\text{split}}}$, so the residue guess $g_{\text{res}} = 1$ succeeds deterministically;
   - the partner box-coordinate difference $\delta = a' - a$ satisfies
     $$
     \delta_{j_{\text{piv}}} \;=\; \frac{d_{j_{\text{piv}}} - g_{\text{res}}}{p_{\text{split}}} \;=\; \frac{1 - 1}{p_{\text{split}}} \;=\; 0,
     \qquad
     \delta_k \;=\; d_k \quad (k \ne j_{\text{piv}}),
     $$
     so $\|\delta\|_1 = \|d\|_1 - 1 \le (s_F - 1) + m\, B_{\text{tern}}(s_F)$;
   - compatible multipliers satisfy `k=0 mod p` within one colour,
     `k=1 mod p` from colour zero to one, and `k=-1 mod p` in reverse.
     Apart from the desired `0`, `+1` or `-1` respectively, all have
     `|k|>=p-1>=W` and cannot share a width-W cube. The reverse partner
     `-u` is desired, not an excluded alias.
   Thus outer parameter guessing collapses to at most $n - m$ free-coordinate trials $j_{\text{piv}} \in \{m, \dots, n-1\}$ at fixed public $(p_{\text{split}} = \operatorname{nextprime}(W), g_{\text{res}} = 1)$.
