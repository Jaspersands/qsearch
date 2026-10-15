# Certified Rounded-Gaussian Dither Sampler and Adaptive-Threshold Coupling Ledger

## 1. Scope and Dishonesty Guardrails

This note specifies and proves the public rounded-Gaussian dither and sign/mask batch sampler (`theorems/native_gaussian_dither_sampler.py`) for conditional source refresh (`theorems/native_source_refresh.py`).

- **No unproved quantum producer**: Certifying the public dither and sign/mask sampler supplies the $\delta_{\mathrm{sampler}}$ term in `native_source_refresh.source_ledger`, but does **not** supply the missing target-width multiple or decision producer (`actual_quantum_decision_or_multiple_producer = false`, `accepted_speedup_candidate = false`).
- **No independent transcendental certificate**: Directed dyadic enclosures of the Gaussian CDF use FLINT/Arb (`erf`/`erfc`) on exact rational inputs. Replaying the same Arb calls in `--check-probabilities` verifies deterministic enclosure generation, not an independent transcendental proof (`independent_transcendental_certificate_supplied = false`).
- **No fresh-sample fabrication**: Public sign bits, mask bits, and Gaussian dither bits are reduction-side randomness paid in full; they never increase the count of independent original oracle observations (`fresh_public_randomness_is_a_fresh_original_sample = false`).

## 2. Continuous-to-Rounded Gaussian CDF and Directed Arb Enclosures

For a positive exact rational width $\sigma \in \mathbb{Q}_{>0}$, let $W \sim \sigma^{-1} \exp(-\pi w^2 / \sigma^2)$ and define the nearest-integer rounded Gaussian random variable
$$E = \operatorname{nearest}(W) \in \mathbb{Z}, \qquad E = t \iff W \in \left[t - \tfrac{1}{2},\, t + \tfrac{1}{2}\right).$$
For any integer threshold $t \in \mathbb{Z}$, the exact cumulative distribution function is
$$F(t) = \mathbb{P}[E \le t] = \mathbb{P}\!\left[W \le t + \tfrac{1}{2}\right] = \frac{1 + \operatorname{erf}\!\left(\sqrt{\pi}\,(t + 1/2)/\sigma\right)}{2}.$$
Recall the existing tail primitive `gaussian_radius_box(sigma, r, bits)` from `native_gaussian_quotient_completion.py`, which encloses
$$\operatorname{tail}(r) = \mathbb{P}[|E| > r] = \operatorname{erfc}\!\left(\frac{\sqrt{\pi}\,(r + 1/2)}{\sigma}\right) \in [\operatorname{tail}_{\mathrm{lo}}(r),\, \operatorname{tail}_{\mathrm{hi}}(r)]$$
using directed $2^{-\text{bits}}$-dyadic endpoints. By symmetry of $\operatorname{erf}$:
1. For $t \ge 0$:
   $$F(t) = 1 - \frac{\operatorname{tail}(t)}{2} \in \left[1 - \frac{\operatorname{tail}_{\mathrm{hi}}(t)}{2},\; 1 - \frac{\operatorname{tail}_{\mathrm{lo}}(t)}{2}\right].$$
2. For $t \le -1$, writing $r = -t - 1 \ge 0$ so that $t + 1/2 = -(r + 1/2)$:
   $$F(t) = \frac{\operatorname{tail}(-t - 1)}{2} \in \left[\frac{\operatorname{tail}_{\mathrm{lo}}(-t - 1)}{2},\; \frac{\operatorname{tail}_{\mathrm{hi}}(-t - 1)}{2}\right].$$

Every comparison between the latent uniform variable $U \sim \operatorname{Uniform}[0, 1)$ and $F(t)$ is decided exclusively by comparing the dyadic prefix interval of $U$ against the directed rational enclosure $[F_{\mathrm{lo}}(t), F_{\mathrm{hi}}(t)]$.

## 3. Tail Truncation and the Adaptive-Threshold Precision Union

Let $f \ge 1$ be the declared per-draw failure-bit target and set the integer truncation bound
$$B = \lceil f \sigma \rceil \ge 1.$$
Then $(B + 1/2)/\sigma > f$, and the probability that $|E| > B$ satisfies
$$\mathbb{P}[|E| > B] = \operatorname{erfc}\!\left(\frac{\sqrt{\pi}\,(B + 1/2)}{\sigma}\right) \le \exp\!\left(-\pi f^2\right) \le \exp(-3 f^2) \le 2^{-3 f^2} \le 2^{-f - 1}.$$
The sampler checks $U < F(-B - 1)$ (left tail $E \le -B - 1$) and $U \ge F(B)$ (right tail $E > B$) explicitly before binary searching $t \in [-B, B]$ for the smallest integer $t$ with $U < F(t)$.

### Lemma 3.1 (Why Query-Count Union Bounds Fail for Adaptive Binary Search)
During binary search over $[-B, B]$ together with the two tail endpoints, the algorithm queries at most $\lceil \log_2(2B + 1) \rceil + 2$ thresholds on any single execution path. However, **which** thresholds are queried depends adaptively on the same latent draw $U \in [0, 1)$. Across all possible $U \in [0, 1)$, the binary search decision tree visits the full set of $2B + 2$ thresholds
$$\mathcal{T}_B = \{-B - 1,\, -B,\, -B + 1,\, \dots,\, B\}.$$
A $K$-bit dyadic prefix cell $[p 2^{-K}, (p+1) 2^{-K})$ fails to resolve against an enclosure $[F_{\mathrm{lo}}(t), F_{\mathrm{hi}}(t)]$ of width $F_{\mathrm{hi}}(t) - F_{\mathrm{lo}}(t) \le 2 \cdot 2^{-K}$ only if $U$ falls within distance $2^{-K}$ of $[F_{\mathrm{lo}}(t), F_{\mathrm{hi}}(t)]$, an interval of Lebesgue measure at most
$$(F_{\mathrm{hi}}(t) - F_{\mathrm{lo}}(t)) + 2 \cdot 2^{-K} \le 4 \cdot 2^{-K}.$$
Because the bad sets of different thresholds in $\mathcal{T}_B$ can be disjoint across the binary search tree, the exact union bound over all $2B + 2$ reachable thresholds is
$$\mathbb{P}[\text{uniform-prefix precision abort}] \le 4(2B + 2)\,2^{-K} = 8(B + 1)\,2^{-K}.$$
Using the naive path-length formula $4(\lceil \log_2(2B+1)\rceil + 2)2^{-K}$ undercounts the union by a factor of $\Theta(B / \log B)$, which is exponentially small in $\log B$ when $\sigma$ is large (e.g. $\sigma \sim 3^{40}$).

### Theorem 3.2 (Per-Draw Coupling Loss Bound)
Choose the dyadic prefix bit budget by the exact integer formula
$$K = f + \lceil \log_2(16(B + 1)) \rceil = f + (16(B + 1) - 1).\mathrm{bit\_length}().$$
Then $2^K \ge 2^f \cdot 16(B + 1)$, so:
1. **Precision abort loss**:
   $$\delta_{\mathrm{prec}} = 4(2B + 2)\,2^{-K} = \frac{8(B + 1)}{2^K} \le 2^{-f - 1}.$$
2. **Tail truncation abort loss**:
   $$\delta_{\mathrm{tail}} \le 2^{-3 f^2} \le 2^{-f - 1}.$$
3. **Total per-draw coupling loss** (if every visited CDF box clears the width bound $\le 2 \cdot 2^{-K}$ within the Arb precision cap):
   $$\delta_{\mathrm{draw}} = \delta_{\mathrm{tail}} + \delta_{\mathrm{prec}} \le 2^{-f}.$$
If an implementation imposes a finite Arb working-precision cap `max_enclosure_bits`, any threshold where `enclosure_bits > max_enclosure_bits` is required triggers an explicit `NUMERICAL_PRECISION_CAP_ABORT` rather than silently using a wider box.

## 4. Complete Source-Refresh Batch Sampling and Coupling Ledger

A complete source-refresh batch at modulus $g = 3^d$, dimension $n$, parent row count $m$, and output batch size $k$ requires:
1. **Paid uniform sign matrix** $T \in \{-1, +1\}^{k \times m}$: $k m$ independent uniform bits, mapped via $b \mapsto 2b - 1 \in \{-1, +1\}$ with zero abort probability.
2. **Paid uniform secret mask** $z \in \mathbb{Z}_g^n$: for each coordinate $j \in \{0, \dots, n-1\}$, draw $L_g = \lceil \log_2 g \rceil$ uniform bits per trial for up to $R_{\mathrm{mask}}$ trials, accepting the first draw $v < g$. Since $g > 2^{L_g - 1}$, each trial rejects with probability $1 - g / 2^{L_g} < 1/2$. Choosing
   $$R_{\mathrm{mask}} = f_{\mathrm{mask}} + \lceil \log_2 n \rceil$$
   bounds the complete-mask rejection abort probability by
   $$\delta_{\mathrm{mask}} = n \left(1 - \frac{g}{2^{L_g}}\right)^{R_{\mathrm{mask}}} \le n\,2^{-R_{\mathrm{mask}}} \le 2^{-f_{\mathrm{mask}}}.$$
3. **Paid $k$-tuple of rounded-Gaussian dithers** $(e_0, \dots, e_{k-1})$ at width $\sigma = \alpha_{\mathrm{target}} g / \sqrt{2}$: setting $f = \lambda_{\mathrm{dither}} + \lceil \log_2 k \rceil$ guarantees per-draw loss $\delta_{\mathrm{draw}} \le 2^{-f}$ and $k$-draw union loss
   $$k\,\delta_{\mathrm{draw}} \le k\,2^{-f} \le 2^{-\lambda_{\mathrm{dither}}}.$$

If any single dither draw or mask coordinate aborts, the **entire** $k$-row refresh batch aborts (`status = "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY"`), emitting `producer_input = None` while retaining the partial draw receipts solely for audit diagnostics. When all draws succeed, the total sampler TV/abort loss
$$\delta_{\mathrm{sampler}} = \min\!\left(1,\; k\,\delta_{\mathrm{draw}} + \delta_{\mathrm{mask}}\right)$$
is passed directly into `native_source_refresh.source_ledger(..., sampler_TV_loss=delta_sampler)`.
