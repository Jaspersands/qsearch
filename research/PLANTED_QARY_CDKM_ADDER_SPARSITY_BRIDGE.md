# Planted $q$-Ary CDKM Adder Sparsity Bridge: Modulus-Independent Free-Column Cell Widths and Quadratic-to-Bipartite Gate Compression

## 1. Motivation and Scope

In `theorems/lattice_cube_source_circuit.py`, `compile_cube_evaluator` compiles a public `CubeCosetSource` (`theorems/lattice_cube_coset_source.py`) into a clean reversible quantum circuit using Qiskit's Cuccaro-Draper-Kutin-Moulton (CDKM) ripple-carry adder `adder_ripple_c04(w, kind="fixed")`. For a general dense $n \times n$ integer basis $B$, computing and uncomputing the $n$ lattice coordinates costs $2 b n^2$ controlled constant additions (where $b = \log_2 M_{\text{box}}$), and every coordinate cell output register scales with the full matrix norm $\max_i \sum_k |B_{k,i}|$.

When the basis $B \in \mathbb{Z}^{n \times n}$ comes from a public $q$-ary modular kernel `PublicQaryLattice` (`theorems/planted_qary_usvp_source.py`), $B$ has a highly structured sparse centered-RREF form:
- $m$ pivot rows $B_{i,\bullet} = q e_{P_i}^T$ ($0 \le i < m$), each having **only $1$ nonzero entry**;
- $n - m$ free rows $B_{m+j,\bullet} = e_{F_j}^T - \sum_{i=0}^{m-1} C_{i,j} e_{P_i}^T$ ($0 \le j < n - m$), where $C_{i,j} \in [-(q-1)/2, (q-1)/2]$.

This note proves three exact theorems showing how this centered-RREF structure compresses both the cell-output qubit widths and the CDKM constant-addition count in `compile_cube_evaluator`.

## 2. Theorem 1 — Exact Nonzero Entry Census and Bipartite Addition Compression

Let $\operatorname{nnz}(C) = |\{(i, j) \in \{0, \dots, m-1\} \times \{0, \dots, n-m-1\} : C_{i,j} \ne 0\}|$ denote the number of nonzero centered RREF residues.

**Theorem 1 (Centered-RREF Sparsity and Exact CDKM Addition Count).**
For any `PublicQaryLattice` with dimension $n$, constraint rows $m$ ($1 \le m < n - 1$), and prime $q \ge 3$, let $B \in \mathbb{Z}^{n \times n}$ be its public row basis, and let $\mathcal{S} = \operatorname{CubeCosetSource}(B, p_{\text{split}}, g_{\text{res}}, j_{\text{coord}}, M_{\text{box}}, W, \text{offsets})$ with $b = \log_2 M_{\text{box}}$ and free splitting coordinate $j_{\text{coord}} = m + j_0 \in \{m, \dots, n-1\}$.
1. **Column-wise nonzero structure**:
   - Every free column $F_j$ ($0 \le j < n - m$) has **exactly $1$ nonzero entry** in $B$, namely $B_{m+j, F_j} = +1$.
   - Every pivot column $P_i$ ($0 \le i < m$) has $1 + \operatorname{nnz}(C_{i,\bullet}) \le 1 + (n - m)$ nonzero entries in $B$.
   - The total number of nonzero entries of $B$ is
     $$
     \operatorname{nnz}(B) \;=\; n + \operatorname{nnz}(C) \;\le\; n + m(n - m) \;\le\; n + \left\lfloor \frac{n^2}{4} \right\rfloor.
     $$
2. **Exact CDKM constant-addition count**: Including compute and uncompute in `compile_cube_evaluator`, the exact number of constant-addition stages is
   $$
   N_{\text{add}}(\mathcal{S})
   \;=\; 2 \Bigl(b \cdot \operatorname{nnz}(B) \;+\; \bigl(1 + \operatorname{nnz}(C_{\bullet, j_0})\bigr) \;+\; n\Bigr),
   $$
   where:
   - $b \cdot \operatorname{nnz}(B)$ is the number of bit-shifted basis additions across all $n$ coordinates,
   - $1 + \operatorname{nnz}(C_{\bullet, j_0}) \le 1 + m$ is the number of colour-bit additions $t \cdot g_{\text{res}} B_{m+j_0, i}$, and
   - $n$ is the number of offset subtractions $-\text{offsets}_i$.
   Compared to a dense $n \times n$ basis with $N_{\text{add}}^{\text{dense}} = 2(b n^2 + 2n)$, the centered-RREF basis saves at least $2 b (n - m)(n - m - 1) + 2 b m(m - 1) + 2(n - m - 1)$ constant additions.

## 3. Theorem 2 — Modulus-Independent Cell Widths on All $n - m$ Free Coordinates

In `CubeCosetSource.clean_arithmetic_plan()`, each ambient coordinate $0 \le col < n$ is assigned a signed point bound $\text{bound}_{col} = \sum_{k=0}^{n-1} |B_{k, col}| c_{k,\max} + W$, bit-width $w_{col} = \max(\lfloor\log_2 \text{bound}_{col}\rfloor + 2, \text{shift} + 1)$ (where $\text{shift} = \log_2 W$), and cell output width $w_{col}^{\text{cell}} = w_{col} - \text{shift}$.

**Theorem 2 (Modulus-Independence of Free-Column Cell Output Widths).**
For every free column $F_j$ ($0 \le j < n - m$), since $B_{k, F_j} = \delta_{k, m+j}$, the signed point bound in `clean_arithmetic_plan()` is
$$
\text{bound}_{F_j} \;=\;
\begin{cases}
p_{\text{split}}(M_{\text{box}} - 1) + g_{\text{res}} + W, & j = j_0 \quad (\text{split free column}),\\[4pt]
(M_{\text{box}} - 1) + W, & j \ne j_0 \quad (\text{non-split free column}),
\end{cases}
$$
which is **completely independent of the prime modulus $q$ and dimension $n$**.
Meanwhile, for every pivot column $P_i$ ($0 \le i < m$),
$$
\text{bound}_{P_i}
\;=\; q(M_{\text{box}} - 1) + \sum_{j \ne j_0} |C_{i,j}|(M_{\text{box}} - 1) + |C_{i, j_0}|\bigl(p_{\text{split}}(M_{\text{box}} - 1) + g_{\text{res}}\bigr) + W
\;\le\; q(M_{\text{box}} - 1) + \frac{q - 1}{2}\Bigl((n - m - 1 + p_{\text{split}})(M_{\text{box}} - 1) + g_{\text{res}}\Bigr) + W.
$$
Consequently, as $q \to \infty$ at fixed $(n, m, M_{\text{box}}, W, p_{\text{split}}, g_{\text{res}})$, the $n - m$ free-column cell registers remain $O(\log(p_{\text{split}} M_{\text{box}} / W))$ qubits wide regardless of $q$, while only the $m$ pivot-column cell registers and the shared $2w + 1$ adder workspace scale as $O(\log q)$.

## 4. Theorem 3 — Exact Non-Split Free-Column Popcount Formula

**Theorem 3 (Closed-Form Gate Count on Every Non-Split Free Column).**
For every non-split free column $F_j$ ($j \ne j_0$), every bit-shifted basis coefficient in `cube_resource_estimate` is $+2^h > 0$ ($0 \le h < b$), which has binary popcount $\operatorname{popcount}(2^h) = 1$. Therefore, each non-split free column $F_j$ contributes exactly
$$
\text{adds}(F_j) \;=\; b + 1,
\qquad
\text{popcount\_sum}(F_j) \;=\; b + w - \operatorname{popcount}(\text{offsets}_{F_j} - 1)
$$
to the forward CDKM resource accumulator, independently of the matrix $H \bmod q$.
