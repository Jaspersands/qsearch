# DCP Adaptive Quadrature Tree-Sieve Audit: Bitwise Dyadic Demodulation, Deterministic Valuation Advancement on Both CNOT Branches, and Visibility Thresholds

## Corrected Research Decision

This is an algebraic audit, NOT an end-to-end O(ell) decoder. The removed
"recovery simulation" evaluated exact secret-dependent expectations at
prescribed labels. The physical source supplies neither primitive. Raw
labels hit the first parity stratum with probability 1/2^ell; zero labels
contain no secret phase. Both costs must be retained.

See DCP_PAID_TREE_RECEIVER.md for the implemented paid adaptive benchmark
on actual source registers. Its bounded Bellman optimization is exponential,
targets one parity bit only, and makes no general optimality/speedup claim.

## 1. Motivation and Scope

In `theorems/dcp_noisy_fourier_likelihood_decoder_audit.py`, full matched-filter / log-likelihood quadrature decoding evaluates all $N - 1 = (2 M_{\text{box}})^n - 1$ candidate shifts $s' \in \mathbb{Z}_N \setminus \{0\}$, costing $O(N)$ classical time. To decode in polynomial classical time $O(\ell) = O(\log N)$ when $\ell = \log_2 N$ is large, a receiver must recover the hidden shift
$$
s \;=\; \sum_{r=0}^{\ell-1} s_r 2^r \;\in\; \{0, \dots, 2^\ell - 1\} \qquad (s_r \in \{0, 1\})
$$
bit-by-bit from least significant bit $s_0$ to most significant bit $s_{\ell-1}$ using labels $k \in \mathbb{Z}_{2^\ell}$ of prescribed 2-adic valuation $v_2(k) = \ell - 1 - r$.

This note proves three exact theorems establishing:
1. the bitwise dyadic quadrature demodulation identity on every valuation stratum $v_2(k) = \ell - 1 - r$,
2. the deterministic $+1$ (or $\ge +2$) 2-adic valuation advancement on **both** CNOT measurement branches $b \in \{0, 1\}$ whenever two receipts of equal 2-adic valuation $v_2(k_1) = v_2(k_2) = h$ are merged, and
3. the exact visibility-squaring crossover threshold $v_d = (1 - p_{\text{bad}})^{2^d}$ across sieve depth $d$.

## 2. Theorem 1 — Exact Bitwise Dyadic Quadrature Demodulation Identity

For any nonzero label $k \in \{1, \dots, 2^\ell - 1\}$, write $k = 2^h (2 u + 1)$ where $h = v_2(k) \in \{0, \dots, \ell - 1\}$ is the 2-adic valuation of $k$ and $2u + 1$ is odd. Set $r = \ell - 1 - h \in \{0, \dots, \ell - 1\}$, and decompose $s = s_{<r} + s_r 2^r + 2^{r+1} s_{>r}$ where $s_{<r} = \sum_{j=0}^{r-1} s_j 2^j \in \{0, \dots, 2^r - 1\}$.

**Theorem 1 (Prefix-Demodulated Binary Sign Law on Stratum $v_2(k) = \ell - 1 - r$).**
1. **Exact modular phase reduction**: For every label $k = 2^{\ell - 1 - r}(2 u + 1)$ of 2-adic valuation $v_2(k) = \ell - 1 - r$,
   $$
   \frac{2\pi k s}{2^\ell}
   \;\equiv\; \frac{2\pi k s_{<r}}{2^\ell} \;+\; \pi (2 u + 1) s_r
   \;\equiv\; \frac{2\pi k s_{<r}}{2^\ell} \;+\; \pi s_r \pmod{2\pi},
   $$
   independently of both the higher bits $s_{>r}$ and the odd factor $2u + 1$.
2. **Demodulated quadrature observable**: For a receipt at label $k$ with visibility $v$ measured in Pauli axis $A \in \{X, Y\}$ with spin $z = 1 - 2y \in \{+1, -1\}$, define the prefix-demodulated score
   $$
   D_r(k, A, z; s_{<r}) \;:=\; z\,\phi_A\!\left(\frac{k s_{<r}}{2^\ell}\right),
   \qquad \phi_X(\theta) = \cos(2\pi\theta), \quad \phi_Y(\theta) = \sin(2\pi\theta).
   $$
   Under balanced $A \sim \{X, Y\}$, for **every** individual label $k$ with $v_2(k) = \ell - 1 - r$ (not merely averaged over $k$!),
   $$
   \mathbb{E}_{A \sim \{X, Y\}, z}\bigl[D_r(k, A, z; s_{<r}) \mid k\bigr]
   \;=\; \frac{v}{2} \cos(\pi s_r)
   \;=\; (-1)^{s_r}\,\frac{v}{2},
   $$
   and $\mathbb{E}[D_r^2 \mid k] = \frac{1}{2}\bigl(\cos^2(2\pi k s_{<r}/2^\ell) + \sin^2(2\pi k s_{<r}/2^\ell)\bigr) = \frac{1}{2}$ with exact variance $\operatorname{Var}(D_r \mid k) = \frac{1}{2} - \frac{v^2}{4}$.

*Proof.*
Since $k 2^{r+1} = 2^\ell (2u + 1)$ is a multiple of $2^\ell$, the higher bits $2^{r+1} s_{>r}$ contribute an integer multiple of $2\pi$. For the $r$-th bit $s_r 2^r$, $2\pi k s_r 2^r / 2^\ell = \pi (2u + 1) s_r \equiv \pi s_r \pmod{2\pi}$ because $2u + 1$ is odd and $s_r \in \{0, 1\}$. Using $\cos(\alpha + \pi s_r)\cos\alpha + \sin(\alpha + \pi s_r)\sin\alpha = \cos(\pi s_r) = (-1)^{s_r}$ at $\alpha = 2\pi k s_{<r}/2^\ell$ yields the pointwise expectation $(-1)^{s_r} v / 2$ and second moment $1/2$. $\square$

## 3. Theorem 2 — Deterministic Valuation Advancement on Both CNOT Branches

**Theorem 2 (Equal-Valuation CNOT Pairing Dichotomy).**
Let $k_1, k_2 \in \{1, \dots, 2^\ell - 1\}$ be two nonzero labels with identical 2-adic valuation $v_2(k_1) = v_2(k_2) = h < \ell - 1$, so that $k_1 = 2^h u_1$ and $k_2 = 2^h u_2$ with $u_1, u_2$ odd. Under the CNOT merge (`OpaquePhaseBackend.merge`), the two branch output labels are $k_+ = (k_1 + k_2) \bmod 2^\ell$ ($b = 0$) and $k_- = (k_1 - k_2) \bmod 2^\ell$ ($b = 1$).
1. **Unconditional $+1$ advancement on both branches**: Both $k_+$ and $k_-$ satisfy $2^{h+1} \mid k_\pm$, so **every** branch outcome $b \in \{0, 1\}$ advances the 2-adic valuation by at least $+1$ ($v_2(k_{\text{out}}) \ge h + 1$, with $k_{\text{out}} = 0$ treated as valuation $\ell$).
2. **Exact mod-4 branch dichotomy**: Because $u_1, u_2 \in \{1, 3\} \pmod 4$ are odd, one of $u_1 \pm u_2$ is congruent to $2 \pmod 4$ and the other is congruent to $0 \pmod 4$. Specifically:
   - On the branch $b \in \{0, 1\}$ where $u_1 + (-1)^b u_2 \equiv 2 \pmod 4$, the output label has **exact** valuation $v_2(k_{\text{out}}) = h + 1$.
   - On the complementary branch $1 - b$ where $u_1 + (-1)^{1-b} u_2 \equiv 0 \pmod 4$, the output label jumps by at least $+2$: $v_2(k_{\text{out}}) \ge h + 2$.
3. **Uniform distribution on higher valuations**: If $u_1, u_2$ are independent and uniformly distributed on the odd residues modulo $2^{\ell - h}$, then across the two equiprobable branches $b \in \{0, 1\}$, $k_{\text{out}} / 2^{h+1}$ is uniformly distributed on $\mathbb{Z}_{2^{\ell - h - 1}}$, so $\Pr[v_2(k_{\text{out}}) = h + 1] = 1/2$ and $\Pr[v_2(k_{\text{out}}) \ge h + 2] = 1/2$.

## 4. Theorem 3 — Balanced-Tree Visibility, Not End-to-End Decoding

**Theorem 3 (Sieve-Depth Visibility Law).**
After d FULL BALANCED stages, each output has exactly 2^d original leaves
and visibility v_0^(2^d). General equal-valuation feedback trees need not be
balanced: their visibility is v_0^L for their ACTUAL leaf count L. Valuation
jumps can be large with two leaves, and zero-label outputs are uninformative.
For the full balanced case, maintaining v_d>=v_min requires
$$
p_{\text{bad}} \;\le\; 1 - v_{\min}^{2^{-d}},
$$
For the stated score D in [-1,1] with signed mean v_d/2, Hoeffding gives
error at most exp(-m*v_d^2/8), so
`m >= ceil(8*v_d^-2*ln(ell/delta))` is SUFFICIENT at a stage. It is not a
lower bound or a proof of optimality. The previous factor-two expression
did not account for the score's half-visibility mean. The implementation
uses an exact dyadic logarithm upper bound for a conservative quota.

The former factor-two guarantee is also EXACTLY falsified, not merely
unproved: ell3, stage2, k1, correct prefix1, bit0, visibility4/5 and35 shots
give D=z/sqrt(2). At total delta=1/10000,35 shots meet the old quota, yet
the single event of17 positive spins has probability greater than
8.15e-5, exceeding the allowed per-stage1/30000. Rational sqrt(2) and a
positive exponential Taylor sum certify BOTH inequalities independently.
This example has bad rate1/5<=1/ell, inside the inverse-log noise promise.

Without a sieve, stage r has label probability 2^r/2^ell, requiring expected
`m*2^(ell-r)` original preparations. These symbolic profiles are not executed
quantum experiments. A useful sieve needs a separate paid source/cost law;
neither the expectation identity nor increasing valuation proves one.
