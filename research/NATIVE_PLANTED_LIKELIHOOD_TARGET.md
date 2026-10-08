# Next Positive Target: Planted Likelihood Inference

SUPERSEDED AS AN IDENTIFIABILITY TASK / LOCAL DERIVATION REVIEW PENDING.
Inspection found `ternary_covariant_noise.py` already implements the exact
paired noise law, polynomial-sample identifiability and signed-noise gates.
Do NOT spend another pass rebuilding these capabilities. The original draft
below is historical context, not a demand for redundant modules.

NEXT IMPLEMENTED REPRESENTATION: `TERNARY_CHARACTER_SYNCHRONIZATION.md` and
`theorems/ternary_character_synchronization.py` now supply an actual fixed-
vocabulary rank-one fake, a public global-character validator, a polynomial
label-adaptive moment-circuit lift with rank-one soundness, and a rational
all-rank gap to impossible perfect fit. NEXT EXPERIMENT is convex tightness
and costed native-secret inference, not another sample identifiability proof.
Do not add another generic search service. The missing capability is a
tractable optimizer for a concrete planted periodic objective, or evidence
that a proposed optimizer does not exploit the planted structure.

## Use A Source Family With An Exact Law

At width1, the first ridge stage is trivial and known. One selected full-rank
physical trit takes all three values. Its independent alpha/delta variables
map to the two output frequencies through a2-by-2 unit-determinant matrix:
the three local coefficient vectors are(0,0),(1,0),(2,1), in some permutation.
Thus, under the original IID premise, an actual width1 output has TWO
independent uniform public frequencies a,c in Z_q^n. Other physical inputs
add known-to-the-lab random offsets without changing this law. Fresh original
cohorts are required for fresh outputs. This is a known native source class,
not a new algorithm or free state-preparation oracle.

Ordinary ternary Fourier readout gives one t in F3 with likelihood

    p_t(u)=|1+chi_q(a.u)*chi_3(-t)+chi_q(c.u)*chi_3(-2t)|^2/9.

This is an efficient quantum measurement and an efficient CLASSICAL
likelihood evaluator for one proposed u. It does not recover u efficiently.

## A Positive Identifiability Argument To Formalize And Falsify

For independent uniform a,c, Fourier orthogonality yields

    E_labels[sum_t p_t(s)^2]=5/9 for every nonzero s,
    E_labels[sum_t p_t(s)*p_t(u)]=1/3 whenever s!=u,
    sum_t p_t(0)^2=1.

These formulas include nonzero divisible secrets. Expand each probability
into its six off-diagonal characters. The three independent frequency
directions are a,c,a-c. Distinct directions have unit2-by-2 coefficient
minors, so cancellation would force both secret vectors to be zero. Equal
directions cancel only at equal secrets; opposite-secret terms use a doubled
nonzero word-Fourier displacement and vanish after summing t over F3.
Verify every special zero/divisible/opposite-secret case; do not infer them
from a primitive-secret histogram.

A complete q9/n1 arithmetic calibration in this session found every nonzero
self moment5/9, every distinct-secret cross moment1/3 and zero self moment1.
This is a finite check, not a proof or a physical source-supply certificate.

For observations t_i from the true secret s, maximize the bounded score

    Score(u)=sum_i p_(t_i)(u).

The planted secret has mean per-sample advantage at least2/9 over EVERY
fixed wrong secret. Each score difference lies in[-1,1]. Hoeffding and a
union bound would give

    Pr[any wrong secret has score>=true score]
        <=(q^n-1)*exp(-2B/81),

conditional on establishing the moments and independent source law. Hence
B=O(n*log q+log(1/eta)) outputs suffice statistically. Exhaustive score
maximization costs q^n and is NOT the requested algorithm. This positive
sample theorem is compatible with the Fourier information lower bound.

## The Actual Computational Search Space

Each measured term is a sparse trigonometric polynomial:

    p_t(u)=1/3+(2/9)*Re[
      chi_q(a.u)*chi_3(-t)
      +chi_q(c.u)*chi_3(-2t)
      +chi_q((a-c).u)*chi_3(t)].

The objective has only O(B) explicitly known harmonics, but its domain has
q^n points and dense modular frequencies. Its Fourier coefficients being
known does not reveal its maximizer. A full group FFT, enumeration or
Grover maximum finding is still exponential. Ordinary Euclidean gradient
descent has no justified basin of attraction for these random modular phases.
Goldreich--Levin finds large coefficients, which are ALREADY known here;
it must not be presented as a maximizer without an additional reduction.

Promising targets to investigate skeptically:
- Reduce the planted objective to a costed noisy modular learning problem;
  determine its noise distribution and compare lattice/BKW baselines.
- Find a structured lifting or phase-synchronization formulation with a
  provable planted solution and a tight relaxation, not a fractional signal.
- Exploit known a,c,a-c triangle relations without building the exponential
  graph on every frequency vector in Z_q^n.
- Use the objective as a falsification baseline for proposed coherent
  receivers, and ask whether the full ridge family offers extra computational
  structure beyond this simplest statistically identifiable source.

Each optimizer must be secret-blind: no initialization near the true secret,
no true-secret proposal ranking or training labels supplied by the producer.
Use held-out physically new samples, prespecified growing n/q regimes,
root/sample/error/source costs, and exact exhaustive controls only where
their cost is explicitly capped. Wrong-secret likelihood peaks, modular
aliases, overfit and failed starts must be retained. Do not call polynomial
sample complexity a polynomial-time quantum algorithm or LWE attack.

HISTORICAL GPT NEXT: the source/cross-moment work was deprioritized after
the repository capability check. Use the character-lift tightness target above.
Gemini owns routine
CLI/registry/UI wiring, integrated full validation and Git backups. The
receiver and source-information modules already provide the finite baselines.
