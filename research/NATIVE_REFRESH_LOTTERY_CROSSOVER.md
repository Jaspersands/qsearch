# Refresh-To-Clean-Basis Crossover And Composed Canonical DAG Pipeline

CURRENT REVIEW: the [scope and baseline audit](NATIVE_REFRESH_CROSSOVER_SCOPE_AUDIT.md)
retains the algebra below but rejects the proposed composition. Both scaling
profiles have unreachable refresh windows outside their pruning scope. Both
calibration recoveries are already matched by completion from the FIRST
supplied candidate list. The Python producer currently imports nonexistent
source-refresh functions, and its stored independent replay is stale.
The crossover width inequality does not imply dimension-free lottery success.
This note describes a proposal, not a verified composed recovery guarantee.

This is a conditional source-crossover and composed classical/reduction audit,
not an implemented quantum decision oracle or multiple producer. The small-root
rounding floor $m / (2 g^2)$ can make source refresh vacuous and bound the
unflooded noise width at a smaller quotient. High-probability completion
additionally requires dimension-dependent clean-basis and disjoint-trial
bounds (`native_basis_lottery`).

## The Refresh-To-Clean-Basis Crossover Inequality

At original modulus $q_0 = 3^{r_0}$ with continuous Gaussian noise width
$\alpha_{\text{orig}}$, let $g_{\min} = 3^{d_{\min}}$ be a root where the common
refresh energy threshold

    H(g_min) = (eta_noise^2 * alpha_target^2 / (4 * k) - m / (2 * g_min^2)) / 2 > 0

is positive, and let

    delta_energy = m * alpha_original^2 / (6 * H(g_min))

be the Markov failure bound of the common original energy event at $g_{\min}$.
Since $m / (2 g_{\min}^2) > 0$, we have $H(g_{\min}) < \eta_{\text{noise}}^2 \alpha_{\text{target}}^2 / (8 k)$
and

    m * alpha_original^2 = 6 * delta_energy * H(g_min)
                        < 3 * delta_energy * eta_noise^2 * alpha_target^2 / (4 * k).

Now consider any smaller terminal root $g_{\text{term}} = 3^{d_{\text{term}}}$ at
which the rounding floor makes $H(g_{\text{term}}) \le 0$, i.e.

    m / (2 * g_term^2) >= eta_noise^2 * alpha_target^2 / (4 * k)
    <=> g_term^2 / m <= 2 * k / (eta_noise^2 * alpha_target^2).

On the unflooded canonical quotient node at $g_{\text{term}}$ (extracted
directly from the $m$ original records), the derived error is
$e_{g_{\text{term}}, i} = \operatorname{nearest}(g_{\text{term}} X_i)$ with
continuous Gaussian width $\beta(g_{\text{term}}) = \alpha_{\text{orig}} g_{\text{term}}$.
Multiplying the two inequalities cancels $m, k, \eta_{\text{noise}}$ and
$\alpha_{\text{target}}$ identically:

    beta(g_term)^2 = (alpha_original * g_term)^2
                   = 6 * delta_energy * H(g_min) * (g_term^2 / m)
                   < (3 / 2) * delta_energy.

More generally, at any root $g_{\text{term}}$ where the rounding floor consumes
at least half of the target refresh energy ($m / (2 g_{\text{term}}^2) \ge \eta_{\text{noise}}^2 \alpha_{\text{target}}^2 / (8 k)$),

    beta(g_term)^2 < 3 * delta_energy.

Thus whenever the high-root refresh energy bound is nonvacuous ($\delta_{\text{energy}} \ll 1$),
every root at or below the refresh rounding-floor horizon automatically has
narrow unflooded Gaussian noise $\beta(g_{\text{term}}) < \sqrt{3 \delta_{\text{energy}}}$,
suggesting `native_basis_lottery.complete` as a comparator for the remaining
upper secret $h \in \mathbb{Z}_{g_{\text{term}}}^n$. The inequality alone does
NOT prove recovery: the ring-zero probability must be raised to the basis
dimension and the number of disjoint trials charged. See the analytical
counterprofile in the scope audit.

## Canonical Node To Clean-Basis Equivalence And Composed Ledger

A surviving canonical node $(g_{\text{term}}, L_{\text{term}} = q_0 / g_{\text{term}}, P_{\text{term}} \in \mathbb{Z}_{L_{\text{term}}}^n)$
is algebraically equivalent to the single original-modulus multiple equation

    g_term * s == (g_term * P_term) mod q_0,

because $\gcd(g_{\text{term}}, q_0) = g_{\text{term}}$ has unit part $1$ and
remaining modulus $Q = q_0 / g_{\text{term}} = L_{\text{term}}$. Invoking
`native_basis_lottery.complete(original_records, g_term, g_term * P_term mod q_0, R_orig)`
inverts a cached $n \times n$ unit minor modulo $g_{\text{term}}$ on disjoint
original blocks, rounds $(y_i - a_i \cdot P_{\text{term}}) / L_{\text{term}} \bmod g_{\text{term}}$,
lifts $s = P_{\text{term}} + L_{\text{term}} h$, and checks all $m$ original
circular distances.

The composed source ledger unions:
1. Whole-bank original Gaussian radius tail (`gaussian_radius_box`),
2. All-scale modulo-$L$ and full-modulus code separation (`separation_ledger`),
3. Reachable-root sign-sum label entropy above $g_{\min}$ (`label_entropy_budget`),
4. Common original error energy at $g_{\min}$ (`common_energy_budget`),
5. Disjoint clean-basis lottery failure at $g_{\text{term}}$ (`basis_probability_ledger`).

## Live Workflows

    python theorems/native_refresh_lottery_crossover.py --write
    node research/certificates/native_refresh_lottery_crossover_crosscheck.js
    python theorems/native_refresh_lottery_crossover.py --check-probabilities
    python -m pytest -q tests/test_native_refresh_lottery_crossover.py
