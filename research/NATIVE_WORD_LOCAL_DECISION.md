# Actual Paired-Word Local Ground Test

Local mechanism audit and classical counterpart; external review pending.
No scalable ground-space measurement or new speedup is supplied.

## Correct Source Adapter

The existing native block heat bath operates on F(w)=sum(0,u,v)[w]. Our
actual original pair a,c gives site values(a,c-a,-c). Subtracting the known
base a gives(0,c-2a,-c-a). The change-of-label matrix has determinant3,
so these two offset columns are NOT jointly IID uniform. Reuse the existing
transition and signature enumeration routines, not their unverified source
law. Every nonzero directed site difference still has a unit coefficient
in the ORIGINAL a,c labels: +/- (2,-1),(1,1),(-1,2). Thus a fixed nonzero
signature is uniform in(Z_q)^n under actual IID original labels.

The same unoriented vocabulary count is therefore valid with a fresh proof:

    Pr[any exact full-root collision at support<=k]
      <= min(1, sum_(j=1..k) C(M,j)*6^j/(2*q^n)).

Policies can depend on all labels and words: the union is before policy
selection. Correlated signatures need not be independent. Do not transfer
this bound to structured/non-IID original labels without proof.

## Components, Not Just Fibres

For each block B enumerate its3^k assignments and average within equal
local-frequency classes. Each P_B is an orthogonal projection. The averaged
heat bath P is symmetric, stochastic and PSD. H=I-P is frustration free.
Its kernel is constant on connected COMPONENTS of the actual walk. The
ground effect therefore has null acceptance #components/3^M, not the
optimistic #frequencies/3^M unless all fibres really connect.

Exact full-root moves keep every ideal source state in the kernel. For a
nontrivial connected component of size C and minimum positive edge weight w,
a conservative gap lower bound is2w/[C(C-1)]. One proof compares each
vertex-pair difference with a spanning-tree path of at most C-1 edges and
uses sum_(i<j)|f_i-f_j|^2=C*sum_i|f_i-mean(f)|^2. Singleton components
have no positive eigenvalue; H=0 when every component is a singleton. They
do NOT provide a useful test just because no small nonzero eigenvalue exists.
Finite gap values are instance certificates, not growing-instance estimates.
The complete-block projection has exact positive gap1, but enumerates3^M
local assignments. Its favorable gap does not erase its transition cost.

Prefix-only moves are dangerous: equality mod3 need not be equality modq.
Their ideal source need not lie in the ground space. The report keeps this
failure and disables the full-root moment guarantee when a transition changes
the actual frequency. Never inherit the source bound by calling it descent.
Null trace values in the local report hold the known mask fixed while
averaging IID original values. Full-root component effects commute with
the mask phases, but a prefix-only effect need not: a data-adaptive mask
requires a separate null-model proof for such an effect.

## Paid Classical Comparator

Our input is an explicitly known product-word state. For ONE selected block,
group its local phase numerators phi by their actual frequency. Then

    <P_B> = sum_classes |sum_x chi_q(phi_x)|^2 / (3^k*class_size).

This can be computed classically from original values and the known mask.
The implemented rational interval uses the existing certified cosine helper,
charges every local assignment and unordered phase pair, and works at large
root bit lengths without a q-sized phase table. Cost is at most9^k times
polynomial bit arithmetic. Logarithmic k gives polynomial work. Uniform
block selection itself does not enumerate the binomial block menu.

The complete average local-energy statistic consequently has a classical
bounded-variable Monte Carlo estimator. This does NOT simulate long-time
coherent walks, their ground projector, arbitrary entangled operations, or
unknown quantum-only phases. Nor does it prove that every ground-space
decision advantage appears with the same gap in one-step energy.

At the current IID growing-root profile q=3^n,M=n^2+12, exact logarithmic
support moves are overwhelmingly absent. On that no-collision event P=I,
H=0 and the ground test accepts the null with probability1. More quantum
walk machinery cannot repair this particular frozen transition family.
Temporary syndrome violations, nonlocal polynomial-description macros,
different encodings, non-IID families and other ensemble effects remain open.

## Live Workflow

| Same-source control | Ground rank | Full-fibre rank | IID null acceptance | Ideal full-root membership |
| --- | --- | --- | --- | --- |
| One-site frozen | 81 | 9 | 1 | 1 |
| Two-site partial | 13 | 9 | 13/81 | 1 |
| Complete-block reference | 9 | 9 | 1/9 | 1 |
| Two-site mod3 prefix only | 3 | 9 | 1/27 | 2/27 |

The two-site actual noisy calibration has ground acceptance about0.233;
its declared source bound is retained, not replaced by ideal membership.
All bounded-error controls have applicable classical baselines and are NOT
hard-source advantage evidence. The four growing-root ledgers use exact
factored signature counts and conservative dyadic probability bounds,
rounded UP and capped at128 certificate bits to avoid huge decimal output.
These bounds are population statements conditional on IID original labels,
not measurements of how often a small finite seed succeeded.

    python theorems/native_word_local_decision.py --write
    node research/certificates/native_word_local_decision_crosscheck.js
    python -m pytest -q tests/test_native_word_local_decision.py

The four bounded controls retain every original, transition weight, connected
component, exact cyclotomic statistic, gap bound and prefix failure. They are
calibration/countercontrols, not newly invented hard oracle problems.
