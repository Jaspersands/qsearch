# DCP Anchor-Conditioned Adaptive Syndrome Routing and Coset-Gauge Invariance Bridge

## 1. Coset-Gauge Equivariance and Mod-$4$ Coset Invariance
For any $A \in \mathbb{Z}_{2^t}^{n \times K}$ and disjoint-support $\bmod 2$ kernel witness matrix $V = [v^{(1)}, \dots, v^{(m)}] \in \{0,1\}^{K \times m}$ with $A v^{(j)} \equiv 0 \pmod 2$, let $\tilde{y}_{\mathrm{syn}} \in \{0,1\}^K$ be the canonical zero-pivot lift of the classically measured CNOT syndrome $y_{\mathrm{syn}} \in \{0,1\}^{K-m}$. Any coset representative $x_0 = \tilde{y}_{\mathrm{syn}} \oplus V w$ ($w \in \{0,1\}^m$) satisfies:
$$\tilde{A}_j(\tilde{y}_{\mathrm{syn}} \oplus V w) \equiv (-1)^{w_j} \tilde{A}_j(\tilde{y}_{\mathrm{syn}}) \pmod{2^t}.$$
Since $\tilde{A}_j \in (2\mathbb{Z}_{2^t})^n$ and $-z \equiv z \pmod 4$ for all even $z \in \{0, 2\} \pmod 4$, the level-$k=2$ residue $\tilde{A}_j(x_0) \bmod 4$ is strictly constant across all $2^m$ coset representatives $x_0 \in y_{\mathrm{syn}} + \mathrm{span}_{\mathbb{F}_2}(V)$.

## 2. Single-Wire ($m=1$) Unitary Invariance vs. Multi-Wire ($m = n + 1$) Adaptive Stage-2 Routing
- **Single-Wire ($m=1$) Obstruction**: On a single retained wire, secret-independent unitaries $U(y_{\mathrm{syn}})$ preserve the conditional Helstrom trace distance $D_{\mathrm{tr}}(s, s' \mid y_{\mathrm{syn}})$ and cannot repair zero-phase-difference syndrome branches.
- **Multi-Wire ($m = n + 1$) Constructive Routing**: With $m = n + 1$ disjoint $\bmod 2$-kernel wires, the halved $\bmod 4$ residue matrix $B_{\bmod 2}(y_{\mathrm{syn}}) = (\tilde{A}(y_{\mathrm{syn}}) \bmod 4)/2 \in \mathbb{F}_2^{n \times (n+1)}$ is known classically from $y_{\mathrm{syn}}$ and always has a non-zero kernel vector $w(y_{\mathrm{syn}}) \in \ker_{\mathbb{F}_2}(B_{\bmod 2}(y_{\mathrm{syn}}))$, achieving $\tilde{\tilde{A}}(y_{\mathrm{syn}}) \equiv 0 \pmod 4$ across $100\%$ of syndromes (vs. $50\%$ for blind fixed CNOT pairing at $n=1, m=2$ and $25\%$ at $n=2, m=3$).
