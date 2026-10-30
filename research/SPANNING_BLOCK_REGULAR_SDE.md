# Spanning-Block Preconditioning For Prime-Power Descent

**Later 29 October follow-up:** [pilot coordinates](PILOT_SUBMODULE_COORDINATES.md)
now implement the public-label frame compiler, fresh-episode controller and
original ambient verification. Physical measurement/source acquisition and
the quantum receiver remain unimplemented; the historical scope below
describes this preceding arithmetic-only pass.

29 October 2026. A conditional arithmetic/source improvement, independently
AI-reviewed. Not a novelty certificate, a complete HSP implementation, or
evidence of a quantum speedup.

## Research Decision

The remaining restriction in [random-kernel regularity](RANDOM_KERNEL_REGULAR_SDE.md)
was its dependence on a special nonzero symmetric contraction and the
associated degree-only large-prime guard. A simpler construction avoids
that dependence entirely: replace each input to ANY arbitrary-input field
SDE solver by the sum of a spanning block of original labels.

Every nonzero atom coefficient activates a whole spanning raw block.
Consequently the original-degree raw Jacobian has full rank, even if the
atom matrix has rank zero. The existing simultaneous Hensel lift then
works. There is no reason to pursue the more complicated proposed
all-power-coset random-kernel construction merely to obtain regularity.

Combined with the published polynomial-arity field solver, this gives a
conditional direct polynomial-source route for arbitrary central cyclic
rank and additive exponents at fixed class c<p. This improves a sufficient
bound and removes a restriction on the DIRECT route; it does not expand
the earlier claimed HSP complexity via the outer reduction, prove that
claim novel, or supply a hard native application.

## 1. Exact Algebraic Lemma

Work in supplied intrinsic coordinates
`C = direct_sum_(j=1..r) Z/p^e_j`, r>0, p odd, 1<=d<p.
Let M_d(r) be a sufficient monotone arity for an arbitrary-input field
solver returning a nonzero vector mu satisfying
`sum_i mu_i^d v_i = 0` over F_p. Its guarantee must apply to zero and
rank-deficient input matrices too, not just independent random inputs.

For each i=1..M_d(r), take r+1 raw labels lambda_(i,k), whose reductions
span F_p^r. Define the PUBLIC arithmetic summary

```
v_i = sum_(k=1..r+1) lambda_(i,k) mod p.
u_(i,k) = mu_i.
```

Then `sum_(i,k) lambda_(i,k) u_(i,k)^d = 0 mod p`.
Choose any i with mu_i != 0. The Jacobian columns on that entire block
are `d * mu_i^(d-1) * lambda_(i,k)`. Their common scalar is nonzero, and
their raw reductions span rank r. Thus the active Jacobian has rank r.
Keep every zero variable exactly zero, choose r active pivots, and apply
the [existing simultaneous lift](PRIME_POWER_REGULAR_SDE.md) to precision
p^max(e_j). Verify all original mixed-modulus equations afterwards.

Crucially, blockwise equality is only a starting mod-p witness. The lift
adjusts individual raw variables independently. Nonzero variables remain
units and hence legal dilation parameters. The original degree d, not
just g=gcd(d,p-1), is used for lifting and final verification.

No quantum aggregation operation occurs here. Retain the raw source
registers until the final controlled contraction. Atoms are not substitute
source states and do not save quantum storage or source copies. All
selection is a function of measured public labels and private randomness.
The existing central-descent statement must be applied to the final RAW
labels and scales. Its hidden-subgroup dilation invariance and independent
source promises remain substantive assumptions.

## 2. Availability And Paid Source Bounds

Conditional on a correct intrinsic frame, fresh IID uniform C labels
reduce to IID uniform columns in F_p^r. For m=r+1,

```
Pr[raw block spans] = product_(i=0..r-1) (1-p^(i-r-1)).
q_r = Pr[raw block fails] < 1/[p*(p-1)] <= 1/6.
```

The inequality follows by bounding failure by the sum of p^(-j) for
j=2..r+1. Use h=M_d(r) accepted blocks, at most
`K=b+ceil(log2 h)` attempts per block, b>=4. Fresh trials and a union
bound give `Pr[any block exhausts] <= h*q_r^K <= 2^-b`.
Store all attempted labels and charge rejected blocks too.

Use fresh R+2 pilot labels on EVERY whole episode, where R is a fixed
ambient cyclic-rank upper bound. Compute the intrinsic module generated
by those pilots, with coordinate/membership maps and embedding into the
original ambient label module. This compiler is NOT implemented here.
Pilot incompleteness has probability less than 1/[p^2*(p-1)]<=1/16.
On complete pilots the bank law above applies. On incomplete pilots,
abort on nonmembership and verify final cancellation back in the original
ambient module before touching the quantum sources. Correctness must not
depend on pilots being complete. Refresh pilots on the next episode.

For observed rank r=0, use the earlier separate branch: one fresh label,
accept only if it is zero. The positive-rank arithmetic API deliberately
does not pretend to execute that pilot branch.

Allow a field-solver abort at most 2^-b for each fixed atom input. Its
randomness is independent of source measurements. Then episode failure
is at most 3/16; no independence between different failure events is
required. With h_R=M_d(R), K_R=b+ceil(log2 h_R), define

```
B_R = R+2 + h_R*(R+1)*K_R.
E[predecessor sources per successful episode] <= 16*B_R/13 < 2*B_R.
```

This uses a uniform cap and a success lower bound conditional on every
prior transcript, not independent identical retry costs. Each source
must itself be legally producible; recursive expected costs multiply
across grades. At fixed class the resulting product is polynomial in
the explicit input size. Bit complexity still pays for every exponent
and log p. This is not polynomial uniformly in growing class/degree.

## 3. Published Import Versus Local Execution

For g=gcd(d,p-1)>1 use the sufficient arity

```
G(g,r) = g^(g*(g-1)/2) * (r+1)^g,
M_d(r) = G(g,r)^ceil(log2(g+1)).
```

This follows from the disjoint-representation construction and collision
accumulation in [Ivanyos--Santha, Theorem 11 and Section 3.3](https://arxiv.org/html/1503.09016v2).
Their field algorithm handles arbitrary inputs; the exponent reduction
converts its g-th-power witness to degree d. For g=1 use r+1 columns;
rank zero needs one. These are sufficient bounds, never lower bounds.

`published_sde_arity` computes that bound but does NOT implement its
general solver. `span_grade_plan(..., published_bound=True)` marks the
import explicitly and reports no implemented backend. The wrapper imposes
no extra prime-size guard beyond p>d, but actual execution still rejects
unsupported local field regimes before acquiring any raw sources.

Polynomial does not mean usable: the imported p5/d4/r2 example alone has
36,520,347,436,056,576 atoms and a bank cap above 7e18 raw sources. This
bound establishes a fixed-degree asymptotic route, not practical leverage
at those parameters. Improving such constants is not the next priority
without a hard native application and a complete source/receiver contract.

Current execution uses the existing linear, p=3 mod4 quadratic, cubic,
guarded odd-degree, or large-field symmetric backend as applicable.
Examples p5/d2 and p5/d4 remain unsupported locally. Large-field mode
uses the complete bounded-randomness backend. Small-field nonlinear
backends cap their declared conic/nonresidue/curve sampling, but retain
expected-time internal root/bit routines; no total clock is claimed.

The small-field caps are b+2 conic trials, g*(b+2) generator trials,
and 9*(b+2) cubic or 2*g*(b+2) odd-degree curve trials. Existing
per-call bounds imply a combined declared sampler abort <=2^-b:
the two terms are at most exp(-(b+2)) each (the conic bound is smaller).
Backend defects and contract violations propagate as errors, not as
statistical ABORTs. Only known stochastic exhaustion is recorded as ABORT.
Validate the RNG interface BEFORE consuming sources: nonlinear capped
backends require callable getrandbits, small-field ones require callable
randrange, and g=1 needs neither. This fixes the independent review's
reproduced late AttributeError after 12 consumed labels at p7/d3/r1.

## 4. Attempts To Falsify The Construction

- **Zero atom rank:** p7, raw columns (1,0),(0,1),(6,6) have zero sum
  mod7 but rank two. A single active atom must retain a rank-two raw
  Jacobian. Compressing the original module to atom rank would be wrong.
- **Tied-scale failure:** p3, d2, raw labels 1,2 modulo9. Their sum is
  zero mod3, but every tied unit pair gives 3*s^2 !=0 mod9. Independent
  lifting gives (4,1), which works. The regression asserts both facts.
- **Biased accepted sums:** exhaustive p3/r2/m3 counting finds 624 of
  729 blocks span, but their sums are not uniformly distributed. An
  average-case-only atom solver would not justify this theorem.
- **Fixed-source contrast:** blocks [I|0] always defeat the earlier
  random-kernel active-support test, yet the spanning-sum method works.
  This validates correctness on those inputs, not an IID source promise.
- **Singular source:** repeated rank-one columns in rank two must exhaust
  the explicit cap, charge every attempted label and return ABORT.
- **Missing backend:** reject an unsupported field before drawing labels;
  a theorem-bound report must never be executed as though a solver exists.
- **Hidden source assumptions:** seeded arithmetic fixtures cannot certify
  independent quantum inputs, a physical error bound, efficient pilots,
  valid Rees coordinates or hidden-subgroup invariance. Violation of any
  of these prevents the end-to-end algorithmic conclusion.

The SDE and regularization are classical arithmetic. They are not a
classical/quantum separation. A classical attack on a proposed native
application must use the SAME input relation and paid access. No failed
classical baseline is interpreted as evidence of hardness here.

## 5. Implementation And Replay

- `theorems/span_regular_sde.py`: arity imports, paid plans, capped block
  selection, arbitrary-input backend dispatch, expansion and raw lifting.
- `tests/test_span_regular_sde.py`: exact controls above, mixed orders,
  original-degree12/reduced-degree4, caps, backend boundaries and errors.
- `qsearch_cli/commands/sde.py`: mutually exclusive `--span-blocks` and
  `--random-kernel` report modes; default historical report unchanged.
- `research/reductions/span_regular_sde.json`: complete raw trial records,
  accepted indices, atom/expanded/final witnesses and scoped cost bounds.

Run `python qsearch.py prime-power-sde --span-blocks --write`.
No new candidate evidence status is promoted. This pass does not change
the reviewed manuscript or claim new Lean formalization.

## 6. Next Decisive Work

The small-field general backend is an implementation dependency, not the
central theoretical gap. Higher-value next work is to compile pilot
submodule coordinates with transformation maps and an ambient verification
boundary, then prove the complete label-conditioned receiver composition.
In particular test p*Z/p^2, non-coordinate embedded submodules and incomplete
pilot frames. This targets the gap between an intrinsic arithmetic witness
and a legal HSP converter. A later native application must survive matched
classical attacks before any speedup claim is entertained.

## 7. Completed Verification

Independent reviewer Dalton checked the argument, then the code. The RNG
preflight issue above was reproduced, fixed and independently confirmed
resolved. No further defect was reported. The review included 609 exact
sampler-budget checks and seven biased rank-one atom-bank controls; the
final focused module suite passed all 23 tests. This is automated review,
not human peer review or formal verification.

Live artifact controls:

| p | d | r | Raw labels consumed | Bank cap | Conditional expected predecessor bound |
| --- | --- | --- | --- | --- | --- |
| 3 | 2 | 4 | 160 | 1625 | 3262 |
| 7 | 3 | 3 | 112 | 1456 | 2922 |
| 13 | 3 | 3 | 112 | 1456 | 2922 |
| 1031 | 2 | 4 | 125 | 1625 | 3262 |

The saved zero-atom control has atom rank zero, raw Jacobian rank two,
and 45 consumed labels. All five saved controls were independently
replayed using separate modular elimination, raw trial/cost checks,
atom equations, support preservation and original mixed-modulus equations.
The final CLI regeneration preserved the artifact's hash.

Final connected regression run: **541 tests passed in 208.82 seconds**.
An earlier version passed 536; the final RNG fix adds five controls.
The final module+CLI subset passed all 29 tests. Commands used Python
3.13.5 at `/opt/anaconda3/bin/python`, with plugin autoload disabled,
`-q -p no:cacheprovider -W error`, and cache prefix `/tmp/qsearch-span-pycache`.
The 20 selected test files were:

```text
tests/test_span_regular_sde.py
tests/test_random_regular_sde.py
tests/test_prime_power_rees_descent.py
tests/test_rees_hsp_reduction.py
tests/test_uniform_bch_rees.py
tests/test_rees_complete_instrument.py
tests/test_rees_copy_only_outer.py
tests/test_central_character_descent.py
tests/test_rees_review_controls.py
tests/test_power_sde.py
tests/test_power_sde_budget.py
tests/test_bounded_power_roots.py
tests/test_weighted_two_erasure_cascade.py
tests/test_odd_power_sde.py
tests/test_cli_parser_integrity.py
tests/tools/test_split_cli.py
tests/test_polynomial_phase_copy_learning.py
tests/test_phase_copy_controller_boundaries.py
tests/test_ut5_matrix_phase_alignment.py
tests/test_symbolic_scalar_phase_erasure.py
```

Five Python syntax checks (the new module/test, CLI command/parser and CLI
test), 12 `node --check` calls under `site/js`, `python qsearch.py validate`
(`valid:true`, `issues:[]`) and `git diff --check` passed. The registry
remains at eight candidates; no evidence status was promoted. No full
repository-suite or new Lean-build claim is made. No Git writes or outreach.
