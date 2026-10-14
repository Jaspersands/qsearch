# Modulo-Scale Original-Prefix Pruning And Canonical DAG Collapse

This is a conditional reduction and ambiguity-pruning audit, not an implemented
quantum decision oracle or multiple producer. It resolves the $(R B)^D$
list-branching question from `NATIVE_RECURSIVE_QUOTIENT_AUDIT.md` and
`NATIVE_SOURCE_REFRESH.md` in the non-wrapping scale regime $4 R_{\text{orig}} < L$,
under original-radius and all-scale code-separation events. The condition
$4R<L$ is the sufficient scope of this source-wide proof, not a necessary
condition for uniqueness on every fixed instance. External review is pending.

## Ring-Projection Elimination Of The Missing Upper Quotient

At original modulus $q_0 = 3^{r_0}$, any node at child modulus $g = 3^d$ has
cumulative scale $L = q_0 / g = 3^{r_0 - d}$ and decomposes the original secret
as $s = P_{\text{true}} + L h_{\text{true}}$ with $P_{\text{true}} = s \bmod L$
and $h_{\text{true}} = \lfloor s / L \rfloor \in \mathbb{Z}_g^n$.

For every original record $(a_i, y_i)$ with $y_i \equiv a_i \cdot s + e_i \pmod{q_0}$,
reducing modulo $L$ annihilates the unknown upper term $L (a_i \cdot h_{\text{true}})$:

    (y_i - a_i . P) mod L = (a_i . (P_true - P) + e_i) mod L.

This residual depends ONLY on the candidate prefix $P \in \mathbb{Z}_L^n$ and
the original bank $(a_i, y_i)$. It requires no upper-quotient solver, no child
decision oracle, and no assumption that false child branches look like a
full-uniform decision null.

## Soundness, Completeness And Canonical DAG Width Collapse

Define the modulo-$L$ circular residual distance on the $m$ original records:

    d_L(P)_i = min((y_i - a_i . P) mod L, (a_i . P - y_i) mod L).

1. **Completeness**: If $\max_i |e_i| \le R_{\text{orig}}$, the true prefix
   $P_{\text{true}} = s \bmod L$ satisfies $\max_i d_L(P_{\text{true}})_i \le R_{\text{orig}}$
   at every scale $L \mid q_0$.
2. **Soundness in the non-wrapping regime ($4 R_{\text{orig}} < L$)**: Because
   $L = 3^{r_0 - d}$ is a ternary prime power and $a_i \bmod L$ is IID uniform
   on $\mathbb{Z}_L^n$ when $a_i \sim U(\mathbb{Z}_{q_0}^n)$, the global code
   separation event over $\mathbb{Z}_L^n$ (`separation_ledger(L, n, m, R_orig)`)
   ensures that no wrong prefix $P \neq P_{\text{true}}$ in $\mathbb{Z}_L^n$ has
   $\max_i d_L(P)_i \le R_{\text{orig}}$, with failure probability bounded by
   the modulo-$L$ small-ball union over all 3-adic difference strata.
3. **Canonical DAG collapse**: When $4 R_{\text{orig}} < L' = q_0 / g'$ holds for
   every reachable nonunit child modulus $g' \le g_{\max}$ (equivalently
   $4 g_{\max} R_{\text{orig}} < q_0$), every false prefix is pruned at the
   parent before child expansion, and all surviving candidates at child modulus
   $g'$ share the unique prefix $P' = s \bmod (q_0 / g')$ and merge into ONE
   canonical node $(g', q_0 / g', P')$.
   Across $d_{\max} = \log_3 g_{\max}$ reachable valuations there are at most
   $d_{\max}$ DISTINCT nonroot nodes. The IMPLEMENTED level traversal can
   expand a node again at another depth, using a different supplied list.
   Without a globally memoized producer/list contract, its expansion bound is
   $1+d_{\max}(d_{\max}+1)/2$, including the root. Candidate work is at most
   that quantity times $B_{\text{level}}$. Thus the conditional bound is
   quadratic in root length, not the previously claimed linear work bound.
   A true global DAG cache could reduce it, but must not silently discard
   different-depth candidate lists. Actual expansion/revisit work is recorded.

## Wrap-Around Horizon And Coarse-Radius Falsifiers

1. **Coarse-scale wrap-around ($L \le 2 R_{\text{orig}}$)**: Since
   $d_L(P)_i \le \lfloor L / 2 \rfloor$ for every residue modulo $L$, whenever
   $L \le 2 R_{\text{orig}}$ (i.e. $g = q_0 / L \ge q_0 / (2 R_{\text{orig}})$),
   every wrong prefix $P \in \mathbb{Z}_L^n$ trivially satisfies
   $\max_i d_L(P)_i \le R_{\text{orig}}$ and modulo-$L$ pruning has zero power.
2. **Half-modulus collision zone ($2 R_{\text{orig}} < L \le 4 R_{\text{orig}}$)**:
   When $2 R_{\text{orig}} \ge L / 2$, balls of radius $R_{\text{orig}}$ around
   $0$ and nonzero codewords in $\mathbb{Z}_L$ overlap, so $4 R_{\text{orig}} < L$
   is a strict gate for THIS global-separation proof. It does not imply all
   fixed instances outside the gate have multiple fitting prefixes. An
   explicit noiseless scale27,radius7 census has exactly one fitting prefix
   despite $4R=28\ge27$. Complete wrap at $L\le2R$ still has zero pruning
   power for every prefix; the intermediate regime is not a universal no-go.
3. **Tight Gaussian radius vs crude Markov radius**: Setting $R = q_0 / n$
   restricts non-wrapping child moduli to $g < n / 4$. Using the certified
   continuous-Gaussian tail enclosure `gaussian_radius_box(alpha_orig * q_0, R_gauss, 128)`
   with $R_{\text{gauss}} = \lceil 8 \alpha_{\text{orig}} q_0 \rceil$ at
   $\alpha_{\text{orig}} = 1 / n^3$ extends the non-wrapping pruning horizon to
   $g < q_0 / (4 R_{\text{gauss}}) \approx n^3 / 32$, which covers all child
   moduli $g \le C = n^2$ for $n \ge 32$.
   These are DECLARED coefficient budgets, not bounds supplied by a real or
   published producer. The BTV small-multiple bound can be substantially
   larger. Do not infer usable-valuation coverage from these selected profiles.

## New Countercontrols And Remaining Debt

### Classical Domination In This Proof Scope

For any true ORIGINAL-root multiple with missing factor g, the known quotient
is x=s modL, where L=q0/g. On the audit's original-radius event,
|e_i|<=R<L/4 implies nearest(e_i/L)=0 for EVERY original row. Thus the
existing one-pass rounded quotient system is EXACT, with no child producer,
recursive source refresh or Gaussian flooding.

The modulo-L code-separation event also implies full label rank modulo3:
otherwise a nonzero mod3 kernel vector z gives the zero codeword
(L/3)*z moduloL, contradicting separation. A label-only unit minor therefore
exists and its verified ring inverse recovers the missing quotient in one
classical solve. On the same source events, full original verification
recovers the planted secret. This argument needs neither paired originals
nor a clean disjoint block; parity is only a limitation of the existing
reference API used by these EVEN-count calibration controls.

All supplied root pairs in both live controls are evaluated by that existing
classical algorithm, with paid label RREF, cached inverses, all response
roundings and all original distances. It finds the same fitted secret with
ZERO additional multiple/decision calls and ZERO flooded Gaussian samples.
No correct pair is selected from truth for this comparison.

Therefore prefix-DAG pruning does NOT open a new completion regime under its
stated successful source events. Keep it as a verification/reduction audit,
and deprioritize it as a new algorithm search direction. The actual high-upside
missing operation is still a source-compatible producer, or a stronger
completion/pruning mechanism OUTSIDE the one-pass safe-valuation regime.

A one-row unit-label, zero-error original instance has unique radius0 fits
at every scale. Two depth-dependent candidate paths revisit the same canonical
mod3 node. The actual traversal performs eight candidate checks, exceeding
the old six-check claim, while recovering the correct original secret.
This falsifies the old work bound, not the useful modular projection identity.

The API's successful terminal fits do NOT certify observed-bank source events
or general tree elimination. Actual radius/code events, complete candidate
coverage, supported scales and a real producer remain separate requirements.
Unexpanded wrapping branches are incomplete work, not evidence of no secret.

## Live Workflows

    python theorems/native_prefix_ambiguity_pruning.py --write
    node research/certificates/native_prefix_ambiguity_pruning_crosscheck.js
    python theorems/native_prefix_ambiguity_pruning.py --check-probabilities
    python -m pytest -q tests/test_native_prefix_ambiguity_pruning.py
