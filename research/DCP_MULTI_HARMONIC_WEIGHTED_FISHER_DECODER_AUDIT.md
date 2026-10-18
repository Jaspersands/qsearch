# DCP Multi-Harmonic Weighted Fisher Decoder Audit: Exact Parseval Mean-Square Visibility Law, Zero-Lag Inversion Identity, and Matched-Filter Optimality

## 1. Motivation and Scope

In `theorems/dcp_noisy_fourier_likelihood_decoder_audit.py` (Subsystem 8), noisy DCP decoding was analyzed at a single fundamental harmonic $\lambda_1 = \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos(2\pi e/q)$. However, standard DCP state preparation generates random pair differences $d \in \mathbb{Z}_q \setminus \{0\}$, where a pair state $|x\rangle + \omega_q^{d(s+e)}|x+d\rangle$ subjected to symmetric modular phase error $e \sim K_\eta$ ($K_\eta(-e) = K_\eta(e)$) exhibits the **$d$-th harmonic visibility**
$$
\lambda_d \;:=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos\!\left(\frac{2\pi d e}{q}\right), \qquad d \in \{0, 1, \dots, q-1\}.
$$
This note proves three exact theorems linking the multi-harmonic visibility spectrum $\{\lambda_d\}_{d=1}^{q-1}$ to the physical error distribution $K_\eta$ and establishing the exact SNR gain of matched-harmonic weighting over uniform difference weighting.

## 2. Theorem 1 — Exact Zero-Error Fourier Inversion and Non-Zero Difference Visibility Sum

**Theorem 1 (Exact Sum of Non-Zero Harmonic Visibilities via $K_\eta(0)$).**
For any symmetric probability distribution $K_\eta$ on $\mathbb{Z}_q$ ($K_\eta(-e) = K_\eta(e)$), $\lambda_0 = \sum_{e \in \mathbb{Z}_q} K_\eta(e) = 1$, and by discrete Fourier inversion at $e = 0$,
$$
\frac{1}{q}\sum_{d=0}^{q-1} \lambda_d \;=\; K_\eta(0).
$$
Consequently, the exact sum and mean of $\lambda_d$ over all non-zero differences $d \in \{1, \dots, q-1\}$ are given in closed form solely by the zero-error probability $K_\eta(0)$:
$$
\sum_{d=1}^{q-1} \lambda_d \;=\; q\,K_\eta(0) - 1, \qquad
\overline{\lambda}_{\text{non-zero}}(K_\eta) \;:=\; \frac{1}{q - 1}\sum_{d=1}^{q-1} \lambda_d \;=\; \frac{q\,K_\eta(0) - 1}{q - 1}.
$$

## 3. Theorem 2 — Exact Parseval Identity for Non-Zero Difference Mean-Square Visibility

**Theorem 2 (Exact Parseval Collision-Purity Law for Quadratic Visibility).**
For any symmetric probability distribution $K_\eta$ on $\mathbb{Z}_q$, Parseval's theorem on $\mathbb{Z}_q$ gives $\frac{1}{q}\sum_{d=0}^{q-1} \lambda_d^2 = \sum_{e \in \mathbb{Z}_q} K_\eta(e)^2 = \|K_\eta\|_2^2$. Subtracting $\lambda_0^2 = 1$ yields the exact closed-form identity for total and mean-square non-zero harmonic visibility:
$$
\sum_{d=1}^{q-1} \lambda_d^2 \;=\; q\,\|K_\eta\|_2^2 - 1 \;=\; q\sum_{e \in \mathbb{Z}_q} K_\eta(e)^2 - 1,
$$
$$
\overline{\lambda^2}_{\text{non-zero}}(K_\eta) \;:=\; \frac{1}{q - 1}\sum_{d=1}^{q-1} \lambda_d^2 \;=\; \frac{q\sum_{e \in \mathbb{Z}_q} K_\eta(e)^2 - 1}{q - 1}.
$$

## 4. Theorem 3 — Matched-Harmonic Weighting Optimality vs Naive Uniform Weighting

For any difference-weight profile $w = (w_1, \dots, w_{q-1}) \in \mathbb{R}^{q-1} \setminus \{0\}$, define the multi-harmonic quadrature SNR functional
$$
\mathrm{SNR}(w; K_\eta) \;:=\; \frac{\bigl(\sum_{d=1}^{q-1} w_d \lambda_d\bigr)^2}{\sum_{d=1}^{q-1} w_d^2}.
$$

**Theorem 3 (Cauchy–Schwarz Matched-Filter Optimality and Exact SNR Gap).**
1. **Matched-Filter Optimality**: By Cauchy–Schwarz, $\mathrm{SNR}(w; K_\eta)$ is maximized over all $w \in \mathbb{R}^{q-1} \setminus \{0\}$ by the matched-harmonic weights $w_d^* = \lambda_d$, achieving
   $$
   \mathrm{SNR}_{\text{matched}}(K_\eta) \;=\; \sum_{d=1}^{q-1} \lambda_d^2 \;=\; q\sum_{e \in \mathbb{Z}_q} K_\eta(e)^2 - 1.
   $$
2. **Uniform Weighting SNR**: Under uniform weights $w_d^{\text{unif}} = 1$ ($d = 1, \dots, q-1$), Theorem 1 gives
   $$
   \mathrm{SNR}_{\text{unif}}(K_\eta) \;=\; \frac{\bigl(\sum_{d=1}^{q-1} \lambda_d\bigr)^2}{q - 1} \;=\; \frac{\bigl(q\,K_\eta(0) - 1\bigr)^2}{q - 1}.
   $$
3. **Exact Physical-Space Variance Identity for the SNR Gap**: The SNR gain of matched-harmonic weighting over uniform weighting equals $q - 1$ times the spectral variance of $\{\lambda_d\}_{d=1}^{q-1}$, which by Parseval's identity on $\mathbb{Z}_q \setminus \{0\}$ equals $q$ times the sum of squared deviations of $K_\eta(e)$ on the non-zero error locus $e \in \{1, \dots, q-1\}$:
   $$
   \mathrm{SNR}_{\text{matched}}(K_\eta) - \mathrm{SNR}_{\text{unif}}(K_\eta)
   \;=\; q \sum_{e=1}^{q-1} \left(K_\eta(e) - \frac{1 - K_\eta(0)}{q - 1}\right)^2 \;\ge\; 0,
   $$
   with equality if and only if $K_\eta(e) = \frac{1 - K_\eta(0)}{q - 1}$ is constant across all non-zero errors $e \in \{1, \dots, q-1\}$ (i.e., pure depolarizing noise).
