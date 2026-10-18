# Native Higher-Call Word-Permutation Covariance Audit: Involutive Dilation Invariance, $m^2 \not\equiv 1$ Bilinear Symmetry Breaking at $k \ge 2$, and Alternating Intertwining Rescue

## 1. Motivation and Scope

In a $k$-call interleaved Fourier-response circuit $|\Psi_{\epsilon, \sigma}(y)\rangle = F_D^{\sigma_k} D_y^{\epsilon_k} \cdots F_D^{\sigma_1} D_y^{\epsilon_1} |+_D\rangle$ on a word table of size $D$, re-indexing the public word table by a permutation $\pi \in S_D$ replaces $y_w$ with $(\pi^* y)_w := y_{\pi(w)}$. While unweighted collision counts $|\mathcal{V}_\epsilon(f \circ \pi)| = |\mathcal{V}_\epsilon(f)|$ are invariant under **all** $D!$ permutations $\pi \in S_D$, the unitary Fourier transforms $F_D^{\pm 1}$ couple consecutive trajectory indices via the bilinear phase $\Phi_\sigma(w; x) = \sum_{\ell=1}^{k-1} \sigma_\ell w_{\ell+1} w_\ell + \sigma_k x w_k \bmod D$.

This note proves three exact theorems determining which affine permutations of $\mathbb{Z}_D$ preserve the $k$-call quantum dynamics:
1. Every **involutive multiplicative unit** $m \in \mathbb{Z}_D^\times$ ($m^2 \equiv 1 \pmod D$) commutes with $F_D^{\pm 1}$ and preserves the $k$-call physics for all $k \ge 1$.
2. At $k = 1$, the full affine group $\mathrm{Aff}(\mathbb{Z}_D) = \mathbb{Z}_D \rtimes \mathbb{Z}_D^\times$ preserves the unordered Born distribution, whereas at $k \ge 2$ both non-involutive units ($m^2 \not\equiv 1 \pmod D$, e.g. $m = 2 \bmod 5$) and non-zero translations ($b \not\equiv 0 \pmod D$) break unitary equivalence while preserving $|\mathcal{V}_\epsilon(f)|$.
3. Alternating the dilation between $y^{(m)}$ on odd calls and $y^{(m^{-1})}$ on even calls restores exact unitary intertwining for every unit $m \in \mathbb{Z}_D^\times$ at all call depths $k \ge 1$.

## 2. Theorem 1 — Exact Intertwining Relation $F_D^{\pm 1} \Pi_m = \Pi_{m^{-1}} F_D^{\pm 1}$ and Involutive Covariance

For any unit $m \in \mathbb{Z}_D^\times$ ($\gcd(m, D) = 1$), define the dilation permutation matrix $\Pi_m \in O(D)$ by $\Pi_m |w\rangle := |(m w) \bmod D\rangle$ (so $\Pi_m^\dagger = \Pi_m^{-1} = \Pi_{m^{-1}}$), and let $y^{(m)}_w := y_{(m w) \bmod D}$ so that $D_{y^{(m)}}^{\epsilon_\ell} = \Pi_{m^{-1}} D_y^{\epsilon_\ell} \Pi_m$.

**Theorem 1 (Exact Dilation Intertwining and Involutive Covariance $m^2 \equiv 1 \pmod D$).**
1. **Fourier-Dilation Intertwining**: For every $m \in \mathbb{Z}_D^\times$ and $\sigma_\ell \in \{-1, +1\}$,
   $$
   F_D^{\sigma_\ell}\,\Pi_m \;=\; \Pi_{m^{-1}}\,F_D^{\sigma_\ell}, \qquad \Pi_m\,F_D^{\sigma_\ell} \;=\; F_D^{\sigma_\ell}\,\Pi_{m^{-1}}.
   $$
2. **All-Call Covariance for Involutive Units ($m^2 \equiv 1 \pmod D$)**: Whenever $m^2 \equiv 1 \pmod D$ ($m^{-1} \equiv m \pmod D$), $\Pi_m$ commutes with $F_D^{\pm 1}$ ($F_D^{\sigma_\ell} \Pi_m = \Pi_m F_D^{\sigma_\ell}$) and fixes $|+_D\rangle$, so for **every** call depth $k \ge 1$:
   $$
   |\Psi_{\epsilon, \sigma}(y^{(m)})\rangle \;=\; \Pi_m\,|\Psi_{\epsilon, \sigma}(y)\rangle, \qquad
   P_{\epsilon, \sigma}\bigl(x \;\big|\; y^{(m)}\bigr) \;=\; P_{\epsilon, \sigma}\bigl((m^{-1} x) \bmod D \;\big|\; y\bigr),
   $$
   and $\mathcal{E}_{\epsilon, \sigma}(f^{(m)}, e^{(m)}) = \mathcal{E}_{\epsilon, \sigma}(f, e)$ and $\mathcal{V}_{\text{HS}}(\epsilon, \sigma; f^{(m)}, e^{(m)}) = \mathcal{V}_{\text{HS}}(\epsilon, \sigma; f, e)$.

## 3. Theorem 2 — Alternating $(m, m^{-1})$ Intertwining vs Uniform-Dilation Symmetry Breaking at $k \ge 2$

**Theorem 2 (Exact Alternating-Call Intertwining for General Units $m \in \mathbb{Z}_D^\times$).**
Let $m \in \mathbb{Z}_D^\times$ be any unit modulo $D$.
1. **Alternating-Call Dilation**: If the $\ell$-th oracle call ($\ell = 1, \dots, k$) queries the dilated phase table $y^{(m_\ell)}$ with alternating exponents $m_\ell := m$ for odd $\ell$ and $m_\ell := m^{-1} \bmod D$ for even $\ell$, then
   $$
   F_D^{\sigma_k} D_{y^{(m_k)}}^{\epsilon_k} \cdots F_D^{\sigma_1} D_{y^{(m_1)}}^{\epsilon_1} |+_D\rangle
   \;=\;
   \begin{cases}
   \Pi_m\,|\Psi_{\epsilon, \sigma}(y)\rangle, & k\text{ odd}, \\
   \Pi_{m^{-1}}\,|\Psi_{\epsilon, \sigma}(y)\rangle, & k\text{ even}.
   \end{cases}
   $$
2. **Uniform-Dilation Bilinear Scaling ($m^2 \not\equiv 1 \pmod D, k \ge 2$)**: Under uniform dilation $y^{(m)}$ on all $k \ge 2$ calls, substituting $w_\ell \mapsto m^{-1} w_\ell \bmod D$ maps the collision variety bijectively ($|\mathcal{V}_\epsilon(f^{(m)})| = |\mathcal{V}_\epsilon(f)|$) while scaling every internal bilinear Fourier coupling by $m^{-2} \not\equiv 1 \pmod D$:
   $$
   \Phi_\sigma\bigl(m^{-1} w; x\bigr) \;\equiv\; m^{-2}\sum_{\ell=1}^{k-1} \sigma_\ell w_{\ell+1} w_\ell \;+\; m^{-1}\sigma_k x w_k \pmod D,
   $$
   breaking permutation equivalence of the Born distribution at $k \ge 2$ whenever $m^2 \not\equiv 1 \pmod D$.

## 4. Theorem 3 — Cyclic Word-Translation $w \mapsto (w + b) \bmod D$: $k=1$ Invariance vs $k \ge 2$ Ramp-Phase Breaking

Let $y^{[+b]}_w := y_{(w + b) \bmod D}$ denote the cyclic translation of the word table by $b \in \mathbb{Z}_D$.

**Theorem 3 ($k = 1$ Translation Invariance vs $k \ge 2$ Internal Ramp Injection).**
1. At $k = 1$, $D_{y^{[+b]}}^{\epsilon_1}|+_D\rangle = X_D^{-b} D_y^{\epsilon_1}|+_D\rangle$, and $F_D^{\sigma_1} X_D^{-b} = Z_D^{-\sigma_1 b} F_D^{\sigma_1}$, so for every $b \in \mathbb{Z}_D$:
   $$
   \langle x \mid \Psi_{\epsilon_1, \sigma_1}(y^{[+b]})\rangle \;=\; \omega_D^{-\sigma_1 b x}\,\langle x \mid \Psi_{\epsilon_1, \sigma_1}(y)\rangle, \qquad
   P_{\epsilon_1, \sigma_1}\bigl(x \;\big|\; y^{[+b]}\bigr) \;=\; P_{\epsilon_1, \sigma_1}(x \mid y).
   $$
2. At $k \ge 2$, the phase gate $Z_D^{-\sigma_1 b}$ between $F_D^{\sigma_1}$ and $D_{y^{[+b]}}^{\epsilon_2}$ injects the linear phase ramp $\omega_D^{-\sigma_1 b w_2}$ before $F_D^{\sigma_2}$, breaking translation invariance for $b \not\equiv 0 \pmod D$ even though $|\mathcal{V}_\epsilon(f^{[+b]})| = |\mathcal{V}_\epsilon(f)|$.
