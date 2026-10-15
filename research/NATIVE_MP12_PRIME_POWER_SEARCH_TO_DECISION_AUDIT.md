# Micciancio-Peikert Prime-Power Search-to-Decision Adapter, Hensel Subgroup Probes, and Sample Expansion Audit

## 1. Scope and Dishonesty Guardrails

`NATIVE_WORD_SPAN_DECISION.md` noted that [Micciancio and Peikert (2012), Section 3 Theorem 3.1](https://eprint.iacr.org/2011/501) provides a width-changing prime-power search-to-decision reduction for $q = 3^r$, while leaving the explicit Hensel subgroup-shift probe algebra, certified dither-widening sampler coupling, false-prefix propagation, and disjoint sample expansion unaudited.

This note and `theorems/native_mp12_prime_power_search_to_decision_audit.py` complete that audit:
- **No decision oracle supplied**: Auditing the search-to-decision adapter and its sample/widening costs does not construct the missing decision distinguisher (`actual_decision_algorithm_supplied = false`, `accepted_speedup_candidate = false`).
- **No fixed-bank sufficiency claim**: A single word-span cohort of $m_{\mathrm{dec}} = 2(nr + 12)$ original samples is one decision query input, not the disjoint sample bank required across all $2nr R_{\mathrm{rep}}$ adaptive Hensel queries (`fixed_single_query_bank_suffices = false`).

## 2. Theorem 1: Exact Hensel Subgroup-Shift Probe Identity for $q = 3^r$

Let $q = 3^r$ ($r \ge 1$) and $s \in \mathbb{Z}_q^n$. Write $s = s_{\mathrm{low}} + 3^\ell s_{\mathrm{upper}}$ at level $\ell \in \{0, \dots, r-1\}$, where $s_{\mathrm{low}} = s \bmod 3^\ell \in [0, 3^\ell)^n$. Given an original record $(a, y) \in \mathbb{Z}_q^n \times \mathbb{Z}_q$ with $y \equiv \langle a, s \rangle + e \pmod q$, a coordinate index $j \in \{0, \dots, n-1\}$, a candidate ternary digit $d \in \{0, 1, 2\}$ for $s_{\mathrm{upper}, j} \bmod 3$, a probe multiplier $u \in \{0, 1, 2\}$, and an integer widening dither $e_{\mathrm{widen}} \in \mathbb{Z}$, define the probed record $(a', y')$ by
$$a' = \left(a + u \cdot 3^{r - 1 - \ell} e_j\right) \bmod 3^r, \qquad y' = \left(y - \langle a, s_{\mathrm{low}} \rangle + u \cdot 3^{r - 1} d + e_{\mathrm{widen}}\right) \bmod 3^r.$$

### Proposition 2.1 (Exact Residual Dichotomy Under True vs False Digit Hypotheses)
Assuming $s_{\mathrm{low}} = s \bmod 3^\ell$, the residual of $(a', y')$ with respect to the remaining secret $s - s_{\mathrm{low}} = 3^\ell s_{\mathrm{upper}}$ satisfies
$$r'(u, d) := \left(y' - \langle a',\, 3^\ell s_{\mathrm{upper}} \rangle\right) \bmod 3^r = \left(e + e_{\mathrm{widen}} + u \cdot 3^{r - 1}\,(d - s_{\mathrm{upper}, j})\right) \bmod 3^r.$$
Consequently:
1. **True digit hypothesis ($d \equiv s_{\mathrm{upper}, j} \pmod 3$)**: For every $u \in \{0, 1, 2\}$,
   $$r'(u, d) = (e + e_{\mathrm{widen}}) \bmod 3^r,$$
   preserving the widened LWE error law identically.
2. **False digit hypothesis ($d \not\equiv s_{\mathrm{upper}, j} \pmod 3$)**: Since $\Delta d = (d - s_{\mathrm{upper}, j}) \bmod 3 \in \{1, 2\}$ is a unit in $\mathbb{Z}_3$, as $u$ ranges over $\{0, 1, 2\}$ the additive offset $u \cdot 3^{r - 1} \Delta d \bmod 3^r$ bijects onto the order-3 subgroup
   $$3^{r-1}\mathbb{Z}_{3^r} = \{0,\, 3^{r-1},\, 2 \cdot 3^{r-1}\},$$
   randomizing the top ternary digit of the residual uniformly over $\{0, 1, 2\}$.
3. **False lower-prefix countercontrol ($s_{\mathrm{low}} \ne s \bmod 3^\ell$)**: If an earlier level $\ell' < \ell$ committed to a wrong digit so that $\Delta s_{\mathrm{low}} = (s \bmod 3^\ell) - s_{\mathrm{low}} \not\equiv 0 \pmod{3^\ell}$, then
   $$y' - \langle a',\, s - s_{\mathrm{low}} \rangle \equiv e + e_{\mathrm{widen}} + u \cdot 3^{r - 1 - \ell}\!\left(3^\ell d - (s_j - s_{\mathrm{low}, j})\right) \pmod{3^r}.$$
   Because $s_j - s_{\mathrm{low}, j} \not\equiv 0 \pmod{3^\ell}$, $3^\ell d - (s_j - s_{\mathrm{low}, j})$ is never divisible by $3^\ell$ for any $d \in \{0, 1, 2\}$, so **all three** digit hypotheses $d \in \{0, 1, 2\}$ incur non-zero $u$-dependent shifts when $\ell \ge 1$.

## 3. Theorem 2: Coupled Rounded-Widening, Certified Dither Sampling, and Disjoint Sample Expansion

Let $\alpha_{\mathrm{decision}} \in (0, 1)$, $h = \lceil \log_2(n + 2) \rceil$, and $\alpha_{\mathrm{search}} = \alpha_{\mathrm{decision}} / h^2$. Each decision query consumes $m_{\mathrm{dec}}$ records widened by fresh Gaussian noise of continuous width
$$\sigma_{\mathrm{widen}} = q \sqrt{\alpha_{\mathrm{decision}}^2 - \alpha_{\mathrm{search}}^2} \ge \sigma_{\mathrm{widen, floor}} := q\,\alpha_{\mathrm{decision}}\!\left(1 - \frac{1}{h^4}\right).$$
When original search records are already rounded to $\mathbb{Z}_q$ and widened by $m_{\mathrm{dec}}$ independent draws from the certified adaptive-threshold rounded-Gaussian sampler (`native_gaussian_dither_sampler.py`) at per-batch dither failure target $2^{-\lambda_{\mathrm{dither}}}$:
1. **Rounded-input widening TV bound**:
   $$\delta_{\mathrm{round\text{-}widen}}^2 \le \frac{11\,m_{\mathrm{dec}}}{28\,q^2(\alpha_{\mathrm{decision}}^2 - \alpha_{\mathrm{search}}^2)} \implies \delta_{\mathrm{round\text{-}widen}} \le \frac{\lceil \sqrt{11 \cdot 28 \cdot m_{\mathrm{dec}} \cdot h^4 \cdot \alpha_{\mathrm{decision}}^{-2}} \rceil}{28\,q\,\sqrt{h^4 - 1}}.$$
2. **Certified dither-sampler coupling loss**: Using `dither_draw_parameters(sigma_widen_floor, f_draw)` with $f_{\mathrm{draw}} = \lambda_{\mathrm{dither}} + \lceil \log_2 m_{\mathrm{dec}} \rceil$, the $m_{\mathrm{dec}}$-draw union abort/TV loss is bounded by
   $$\delta_{\mathrm{sampler}} = \min\!\left(1,\, m_{\mathrm{dec}}\,\delta_{\mathrm{draw}}\right) \le 2^{-\lambda_{\mathrm{dither}}}.$$
3. **Effective decision advantage and disjoint sample expansion**: An average-case decision distinguisher with ideal advantage $\gamma_{\mathrm{ideal}} \in (0, 1]$ on continuous-widened instances has effective advantage on rounded-then-dither-widened instances at least
   $$\gamma_{\mathrm{eff}} = \max\!\left(0,\; \gamma_{\mathrm{ideal}} - 2\delta_{\mathrm{round\text{-}widen}} - 2\delta_{\mathrm{sampler}}\right).$$
   Testing $d \in \{0, 1\}$ (2 hypotheses per coordinate-level step across $n r$ steps, so $N_{\mathrm{tests}} = 2 n r$) with per-test majority-vote failure $\le \delta_{\mathrm{total}} / (2 n r)$ requires
   $$R_{\mathrm{rep}} \ge \left\lceil \frac{2\,\lceil \ln(4 n r / \delta_{\mathrm{total}}) \rceil}{\gamma_{\mathrm{eff}}^2} \right\rceil \quad (\text{using } \ln 2 < 1 \implies \lceil \log_2(4 n r / \delta_{\mathrm{total}}) \rceil \ge \ln(4 n r / \delta_{\mathrm{total}}))$$
   independent decision queries per test, consuming
   $$Q_{\mathrm{decision}} = 2 n r\,R_{\mathrm{rep}}, \qquad M_{\mathrm{disjoint\_samples}} = 2 n r\,R_{\mathrm{rep}}\,m_{\mathrm{dec}}$$
   disjoint original search samples.
