# DCP Multi-Packet Product-Twirl SQ Dimension and Sign-Ambiguity Audit

## 1. Exact Results
1. **Global Sign Indistinguishability**:
   Under product-twirled single-coordinate measurements $P_\gamma(y \mid a, s) = \frac{1}{2} + \frac{1}{2}(1-2y)\gamma\cos(\frac{2\pi}{q}\langle a, s \rangle)$, $s$ and $-s \bmod q$ induce identical $T$-packet distributions for all $T \ge 1$.
2. **Cosine Character Orthogonality & SQ Dimension**:
   Over $a \sim \mathrm{Unif}(\mathbb{Z}_q^n)$, the profiles $\phi_s(a) = \cos(\frac{2\pi}{q}\langle a, s \rangle)$ are mutually orthogonal across all distinct unordered pairs $\{s, -s\}$ ($\mathbb{E}_a[\phi_s \phi_{s'}] = 0$ for $s \not\equiv \pm s'$), with $\chi^2(P_s \| P_0) = \gamma^2$ on $2$-torsion shifts ($2s \equiv 0$) and $\gamma^2/2$ on non-$2$-torsion shifts.
3. **Chosen-Header Constructive Control**:
   If headers are chosen along standard basis vectors $a^{(i)} = e_i$, $\mathbb{E}[1-2y \mid a=e_i] = \gamma\cos(2\pi s_i / q)$ directly reads out the coordinate cosines in $O(n/\gamma^2)$ samples.
