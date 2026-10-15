# Multi-Round Interleaved Syndrome-Work Circuits and Response-Call Degree Audit

## 1. Scope and Dishonesty Guardrails

`NATIVE_SYNDROME_DILATION.md` proved that a single application of the reversible word-to-syndrome shift $T_f|w,z\rangle = |w, z + f_A(w)\rangle$ with any label-only syndrome ancilla produces a compressed word effect $E_p = \sum_t p_t |\Phi_t\rangle\langle \Phi_t|$ whose uniform-secret average overlap equals the raw Gram collision value $\langle \psi_{s,e}, K \psi_{s,e}\rangle \le C_A = \sum_\sigma (m_\sigma / D)^2$. That audit explicitly left open:
1. Multi-round noncommuting interleaving of $T_f^{\pm 1}$, syndrome-register unitaries $W_\ell$, and word-register mixers $U_\ell$ after preparing the original-data word state $|\psi_{s,e}\rangle$; and
2. Multi-call circuits that re-apply the response-dependent phase gate $D_y = \operatorname{diag}(\omega_q^{\eta_y(w)})$ $r \ge 2$ times interleaved with label-only word/syndrome unitaries.

This note and `theorems/native_interleaved_syndrome_work_audit.py` provide exact cyclotomic and rational theorems auditing both mechanisms on actual original-data banks:
- **No universal quantum lower bound**: Bounding the fibre-pinched trace and $r$-call collision degree of these circuit families does not prove a universal lower bound against all quantum algorithms (`universal_quantum_lower_bound_claimed = false`, `new_active_negative_result_created = false`).
- **No speedup candidate**: Exhibiting noncommuting multi-round effects $[E_{\mathrm{eff}}, K] \ne 0$ and 2-call additive path collisions does not yield a polynomial-time receiver (`accepted_speedup_candidate = false`, `scalable_quantum_speedup_supplied = false`).

## 2. Theorem 1: Exact Fibre-Pinching Identity for Arbitrary Label-Only Interleaved Circuits

Let $q = 3^r$, $N = q^n$, and $D = 3^M$ for $M$ original record pairs. For secret $s \in \mathbb{Z}_q^n$ and original error vector $e$, the single-preparation native word state is
$$\psi_{s,e}(w) = \frac{1}{\sqrt{D}}\, \omega_q^{\langle s, f_A(w)\rangle + \theta_e(w)} = \Phi_s(w)\, \omega_q^{\theta_e(w)}, \qquad \omega_q = e^{2\pi i / q}.$$
Consider an arbitrary $L$-round interleaved unitary on $\mathcal{H}_{\mathrm{word}} \otimes \mathcal{H}_{\mathrm{synd}}$,
$$\mathcal{U}_L = \prod_{\ell=1}^L (U_\ell \otimes W_\ell)\, T_f^{\sigma_\ell}, \qquad \sigma_\ell \in \{-1, 0, +1\},$$
where $U_\ell \in \mathrm{U}(D)$, $W_\ell \in \mathrm{U}(N)$, the initial ancilla density $\rho_{\mathrm{anc}}$, and the final joint measurement effect $0 \le M_{\mathrm{joint}} \le I_{DN}$ depend only on the public labels $A$ (not on $s$ or the responses $y$). Define the reduced word effect
$$E_{\mathrm{eff}} = \operatorname{Tr}_{\mathrm{synd}}\!\left((I_D \otimes \rho_{\mathrm{anc}}^{1/2})\, \mathcal{U}_L^\dagger M_{\mathrm{joint}} \mathcal{U}_L\, (I_D \otimes \rho_{\mathrm{anc}}^{1/2})\right), \qquad 0 \le E_{\mathrm{eff}} \le I_D.$$

### Lemma 2.1 (Cross-Fibre Annihilation Under Uniform-Secret Twirl)
Even when $\mathcal{U}_L$ interleaves word mixers $U_\ell$ and noncommuting syndrome gates $W_\ell$ so that $(E_{\mathrm{eff}})_{w,v} \ne 0$ between distinct fibres $f_A(w) \ne f_A(v)$, averaging over $s \sim \operatorname{Uniform}(\mathbb{Z}_q^n)$ annihilates every cross-fibre entry of $E_{\mathrm{eff}}$:
$$\mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[\langle \psi_{s,e} | E_{\mathrm{eff}} | \psi_{s,e} \rangle\right] = \frac{1}{D} \sum_{w, v \in [D]} (E_{\mathrm{eff}})_{w,v}\, \omega_q^{\theta_e(v) - \theta_e(w)}\, \mathbb{E}_{s}\!\left[\omega_q^{\langle s, f_A(v) - f_A(w)\rangle}\right] = \langle \psi_{0,e} | \mathcal{C}_A(E_{\mathrm{eff}}) | \psi_{0,e} \rangle,$$
where $\mathcal{C}_A(E_{\mathrm{eff}}) = \sum_{\sigma \in \mathbb{Z}_q^n} \Pi_\sigma E_{\mathrm{eff}} \Pi_\sigma$ is the orthogonal pinching onto the frequency fibres $\Pi_\sigma = \sum_{w : f_A(w) = \sigma} |w\rangle\langle w|$ of size $m_\sigma = \operatorname{Tr}(\Pi_\sigma)$.

### Corollary 2.2 (Fibre-Trace Envelope Bound)
Since $\Pi_\sigma |\psi_{0,e}\rangle$ has squared $\ell_2$-norm $\|\Pi_\sigma |\psi_{0,e}\rangle\|_2^2 = m_\sigma / D$ and $\Pi_\sigma E_{\mathrm{eff}} \Pi_\sigma \ge 0$,
$$\mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[\langle \psi_{s,e} | E_{\mathrm{eff}} | \psi_{s,e} \rangle\right] \le \sum_{\sigma \in \mathbb{Z}_q^n} \frac{m_\sigma}{D}\, \lambda_{\max}(\Pi_\sigma E_{\mathrm{eff}} \Pi_\sigma) \le \sum_{\sigma \in \mathbb{Z}_q^n} \frac{m_\sigma}{D}\, \operatorname{Tr}(\Pi_\sigma E_{\mathrm{eff}} \Pi_\sigma) \le \frac{m_{\max}(A)}{D}\, \operatorname{Tr}(E_{\mathrm{eff}}).$$

## 3. Theorem 2: Exact Sum-Rule Conservation Across Multi-Round Interleaved Syndrome Sectors

Suppose $\mathcal{U}_L$ applies noncommuting unitaries $W_1, \dots, W_L \in \mathrm{U}(N)$ on the syndrome register interleaved with $T_f^{\pm 1}$, followed by the constructive ground-space readout $(F_3^\dagger)^{\otimes M} T_f$ on the word register and an orthonormal basis measurement $\{|\chi_t\rangle\}_{t \in \mathbb{Z}_q^n}$ on the syndrome register.
- Because $T_f$ acts identically on all words $w$ in the same frequency fibre $f_A(w) = \sigma$, for each syndrome outcome $t \in \mathbb{Z}_q^n$ the reduced word effect has sector weight $w_t(\sigma) = |\beta_t(\sigma)|^2 \in [0, 1]$ satisfying Parseval's identity $\sum_{t \in \mathbb{Z}_q^n} w_t(\sigma) = 1$ for every $\sigma \in \mathbb{Z}_q^n$.
- Even when noncommuting syndrome phase gates $P_{Q_2}$ make $w_t(\sigma)$ vary across $\sigma$ and $t$, summing across all $N$ syndrome readout sectors yields the **exact multi-round Parseval conservation law**:
  $$\sum_{t \in \mathbb{Z}_q^n} \mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[P_t(s, e)\right] = \frac{1}{D^2} \sum_{\sigma \in \mathbb{Z}_q^n} \left(\sum_{t \in \mathbb{Z}_q^n} |\beta_t(\sigma)|^2\right) \left|\sum_{w \in f_A^{-1}(\sigma)} \omega_q^{\theta_e(w)}\right|^2 = \langle \psi_{0,e} | K | \psi_{0,e} \rangle \le C_A.$$

## 4. Theorem 3: Two-Call Response-Phase Interleaving and 3-Adic Valuation Stratification

When a circuit queries the response-dependent diagonal gate $D_y = \operatorname{diag}(\omega_q^{\eta_y(w)})$ twice ($r = 2$) with intermediate uniform word mixer, averaging over $s \sim \operatorname{Uniform}(\mathbb{Z}_q^n)$ pinches the 4-tuple path sum $(w_1, w_2, v_1, v_2) \in [D]^4$ onto the **additive 2-call relation**
$$\mathcal{R}_2(A) = \left\{(w_1, w_2, v_1, v_2) \in [D]^4 : f_A(w_1) + f_A(w_2) \equiv f_A(v_1) + f_A(v_2) \pmod q\right\}.$$
Let $e_0 = (1, 0), e_1 = (-1, 1), e_2 = (0, -1) \in \mathbb{Z}^2$ be the native pair digit vectors. Because $e_0 + e_1 + e_2 = (0, 0)$, for each site $j \in \{1, \dots, M\}$ the integer difference $\Delta_j = e_{w_{1,j}} + e_{w_{2,j}} - e_{v_{1,j}} - e_{v_{2,j}} \in \mathbb{Z}^2$ partitions the $3^4 = 81$ site 4-tuples into three exact 3-adic strata:
1. **$\Delta_j = (0, 0)$ over $\mathbb{Z}$** ($15$ tuples per site, where $\{w_{1,j}, w_{2,j}\} = \{v_{1,j}, v_{2,j}\}$ as multisets);
2. **$\Delta_j \in \{\pm 3 e_0, \pm 3 e_1, \pm 3 e_2\}$** ($12$ tuples per site, where $\{w_{1,j}, w_{2,j}\} = \{a, a\}$ and $\{v_{1,j}, v_{2,j}\} = \{a+1, a+2\}$);
3. **$\gcd(\Delta_{j,0}, \Delta_{j,1}, 3) = 1$** ($54$ tuples per site).

Across $M$ pair sites, $\Delta = (\Delta_1, \dots, \Delta_M) \in \mathbb{Z}^{2M}$ partitions the $81^M$ 4-tuples into:
- **$15^M$ identically-zero 4-tuples** ($\Delta = 0$ over $\mathbb{Z}$), which collide with probability $1$ for every bank $A$;
- **$27^M - 15^M$ order-$(q/3)$ subgroup 4-tuples** ($\Delta \in 3\mathbb{Z}^{2M} \setminus \{0\}$), whose IID uniform label combination is $0 \pmod 3$ when $d = 1$ (colliding with probability $1$) and is uniform on $3\mathbb{Z}_q^n$ when $d \ge 2$ (colliding with probability $3^n / N$);
- **$81^M - 27^M$ unit-coefficient 4-tuples** ($\Delta \notin 3\mathbb{Z}^{2M}$), whose IID uniform label combination is uniform on $\mathbb{Z}_q^n$ (colliding with probability $1/N$).

Consequently, for IID uniform original labels $A \sim \operatorname{Uniform}((\mathbb{Z}_q^n)^{2M})$ with $q = 3^d$:
$$\mathbb{E}_A\!\left[C_A^{(2)}\right] = \begin{cases}
\left(\frac{1}{3}\right)^M + \left(1 - \left(\frac{1}{3}\right)^M\right)\frac{1}{3^n}, & d = 1, \\[8pt]
\left(\frac{5}{27}\right)^M + \left(\left(\frac{1}{3}\right)^M - \left(\frac{5}{27}\right)^M\right)\frac{3^n}{N} + \left(1 - \left(\frac{1}{3}\right)^M\right)\frac{1}{N}, & d \ge 2.
\end{cases}$$
