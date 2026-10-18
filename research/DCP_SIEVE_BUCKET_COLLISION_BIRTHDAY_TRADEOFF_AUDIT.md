# DCP Sieve Bucket Collision Birthday Tradeoff Audit

## 1. Exact Results
1. **Closed-Form Finite-Sample Disjoint Pairing Identity**:
   For $M$ independent uniform headers placed into $B$ buckets with occupancies $(N_1, \dots, N_B) \sim \mathrm{Multinomial}(M; 1/B, \dots, 1/B)$,
   $$\mathbb{E}\!\left[\sum_{b=1}^B \left\lfloor \frac{N_b}{2} \right\rfloor\right] = \frac{M}{2} - \frac{B}{4}\left(1 - \left(1 - \frac{2}{B}\right)^M\right).$$
2. **Birthday vs. Saturation Regimes & Multi-Layer Coherence**:
   - Sub-saturation ($M \ll B$): $\mathbb{E}[M_{\mathrm{pairs}}] = \frac{M(M-1)}{2B}(1 - O(M/B))$.
   - Saturation ($M \gg B$, $B\ge2$): $\mathbb{E}[M_{\mathrm{pairs}}]$ approaches $\frac{M}{2} - \frac{B}{4}$. At $B=1$ use $\lfloor M/2\rfloor$.
   - With independent, label-independent phase noise on disjoint binary source trees, Fourier survival is $\gamma_L = \gamma_0^{2^L}$, CONDITIONAL on an output existing. Shared phase errors can instead cancel in a difference merge.

## 2. V1 Mean Recurrence Retracted

The previous multilayer routine incorrectly used $f(\mathbb E[M])$ in place
of $\mathbb E[f(M)]$. For initial $M=2$, buckets $[2,2]$, it reported final
expected pairs $-1/4$. The first-layer law is $\Pr[M_1=0]=\Pr[M_1=1]=1/2$,
so the true second-layer output is identically zero.

V2 computes exact rational transitions via the odd-bucket count $o$. For
each new ball there are $B-o$ bucket choices taking $o$ to $o+1$, and $o$
choices taking it to $o-1$. Count integer paths, divide by $B^M$, and map
$o$ to pair count $(M-o)/2$. Propagating the ENTIRE pool-size distribution
between layers gives exact expectations, extinction probabilities and saved
rational laws, not a continuous mean-field approximation. Exhaustive small
joint assignments and a separate JavaScript enumerator cross-check this.
Single-layer sparse-bucket means are also evaluated rationally to avoid
cancellation. The reference caps $M\le512$, $B\le65536$ are implementation
limits, not evidence of hardness or an efficient asymptotic sieve.

## 3. Scope And Remaining Blocker

Every layer assumes fresh independent uniform bucket assignments conditional
on its pool size. Actual DCP merged headers are NOT proved to satisfy this.
These are candidate pairs BEFORE any additional successful-merge branch
selection; no branch probability is charged or silently assumed to be one.
No DCP sample exponent, optimal-sieve lower bound or end-to-end decoder is
established. Generic Kuperberg sieving is existing prior art, not a discovery
from this occupancy model; see
[Kuperberg's original algorithm](https://www.math.ucdavis.edu/research/infovault/greg/SIAM_JC-35-05.pdf).
The local transition derivation remains review pending; do not promote it
to central proof status or a broad negative result.
