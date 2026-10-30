# Norm Sampler Clock And Deterministic Counting

27 October 2026. A scoped classical-proposal falsifier and a conditional
classical counting scheme, not classical hardness, a new quantum algorithm,
or a novelty claim. Finite controls check formulas; the arguments below
are what supply the asymptotic conclusions.

## Scientific Question And Input

Can a better auxiliary code, sparser multiplier, or improved incidence
proposal turn the exact rank-weighted norm sampler into a polynomial-time
native algorithm at fixed field size?

The original input is a full-row-rank `k by m` matrix B, `k>=1`, over an odd finite
field F_q and an arbitrary syndrome s. The native set is

    Y_s = {y in (F_q^*)^m : B y = s},       N_s = |Y_s|.

Assume a proved lower bound d on the minimum weight of rowspace(B).
This is an input-family promise, NOT inferred from a few sampled rows.
The complete-AG promise uses `q>=1019, e>=8, k=5e+3, m=22e,
d>=12e-3`. Existing source-construction and matrix-only adapter obligations
are not discharged by this note. The executable uses arbitrary-precision
prime-field arithmetic, with a 127-bit prime control. The written character argument also covers odd
prime powers with effective field arithmetic.
For k=0 the count is simply `(q-1)^m`; the implemented matrix interface
requires at least one row instead of using an undefined precision threshold.

The proposed improvement being tested is CLASSICAL: retain the verified
quadratic norm linearization but optimize its auxiliary choices. No new
expected quantum speedup is asserted. The strongest available comparator
remains the existing exact classical sampler on `q^2>=44e`, and the
matrix-only classical decoder supplies the ordinary-DQI quantum comparator.
Fixed-q full-support search outside the classical guarantee is not known
hard merely because this proposal fails.

## Exact Native Count

For any nontrivial additive character psi, orthogonality gives

    N_s = (q-1)^m / q^k * (1 + theta_s),
    theta_s = sum_(lambda != 0) psi(-lambda.s)
                  * (-1/(q-1))^wt(lambda B).

The sum is real and

    |theta_s| <= a := (q^k-1)/(q-1)^d.                         (1)

This is the same elementary Fourier identity already used in the
systematic-full-support baseline, not a new counting identity.

## Which Norm Proposals Are Covered

Let T=support(h), t=|T|, and A_T have r independent rows. The verified
mixed annihilation identities imply, for every lambda,

    U_lambda = A_T diag(h_T * (B_T^transpose lambda)),
    U_lambda A_T^transpose = 0.

Consequently, with r_lambda=rank(U_lambda),

    r_lambda <= min(r,t-r),       2 r_lambda <= t.            (2)

Remove dependent auxiliary rows before applying this statement. It does
not assume generic ranks, geometry, or dense h.

The covered trial draws fresh uniform nonzero values outside T, then draws
an offset coset of `row(A_T) direct_sum row(A_T)`, using rank-size bias.
If the adjusted syndrome is reachable, it takes ONE uniform solution in
the FULL affine fiber, retains reachable rank-deficient fibers, and
rejects the WHOLE trial if any norm is zero. Each new trial redraws all
outside values. A value fixed across failed trials is a different process.

For a coset C put `D(C)=k-rank(M_C)` and `N_cosets=q^(2t-2r)`.
The exact base/incident/thinning implementation has subprobability

    Pr(C accepted at offset stage) = q^D(C)/(N_cosets Z),
    Z = 1 + (q^k-1)q^(-2R),

where R is a PROVED lower bound for all r_lambda with lambda nonzero.
The stronger ideal version grants unit-cost sampling from the normalized
size-biased law, with

    Z_star = E_C q^D(C) = 1 + sum_(lambda != 0) q^(-2 r_lambda).

This identity counts ALL nonzero coefficient vectors, not projective
lines. It follows by counting the kernel of M_C^transpose and using the
independence of the two uniform offsets. Hence both normalizers Z_0 obey

    Z_0 >= 1 + (q^k-1)q^(-t).                               (3)

Granting the ideal source does not grant target-conditioned cosets or free
rejection of unreachable targets. Such a source would be a new algorithmic
obligation and is outside the result.

## Whole-Trial Acceptance And Uniform Auxiliary Bound

For a reachable coset the affine fiber has `q^(2r-k+D(C))` points.
Dividing its proposal mass by that size cancels D(C). A nonzero value has
exactly q+1 quadratic-norm lifts at each position in T. Therefore, putting
`rho=1-q^(-2)`, the exact success probability is

    P_s = N_s (q+1)^t / [(q-1)^(m-t) q^(2t-k) Z_0]
        = (1+theta_s) rho^t / Z_0.                          (4)

This needs no full-rank-M or rank-two-marginal hypothesis. Omitting
deficient reachable systems changes the algorithm and the equality.

If t>=k, `rho^t/Z_0 <= rho^k`. If t<k, (3) gives

    rho^t/Z_0 <= rho^k/(1-q^(-k)) * (q rho)^(-(k-t))
              <= rho^k/(1-q^(-k)),

since `q rho = q-q^(-1)>1`. Thus EVERY admissible auxiliary choice obeys

    P_s <= u := min(1, (1+a)rho^k/(1-q^(-k))).              (5)

Sparse support cannot remove the clock: it reduces the nonzero-norm loss
but increases the incidence normalization cost. Better lambda weights
cannot evade (5) either, since the ideal Z_star version is included.

## Adaptive And Capped Policies

The bound is uniform in syndrome and in all auxiliary choices. A policy
may select new admissible A,h and R using the entire prior history BEFORE
the next trial's fresh prescribed draws. Its conditional success remains
at most u. Hence

    Pr(success by L trials) <= 1-(1-u)^L <= L u.

A policy continuing until success has `E[T]>=1/u` (infinite expectation
is allowed). For a capped or abandoning policy completing C trials, only

    Pr(success) <= u E[C]

is justified. A one-trial cap disproves the unqualified `E[C]>=1/u` claim.
This correction came from independent review and is retained in tests.

All preprocessing and ideal-source costs were set to zero for this lower
bound, strengthening it within the specified proposal family. A witness
emitted by another preprocessing algorithm is outside this trial model.

## Fixed-Field Consequence

For the complete-AG promises, a decreases exponentially in e at every
fixed q>=1019. In fact the stronger square-gap condition

    (q-1)^(12e-3) > q^(2(5e+3))                             (6)

holds. At e=8 its ratio is `q^7(1-1/q)^93`, which is at least
`q^7(1-93/q)>1` by Bernoulli. Each increment in e multiplies the ratio by
`q^2(1-1/q)^12 >= q(q-12)>1`. Thus `a<q^(-k)` and the prefactor
in (5) is less than two.

Since `(1-1/q^2)^(q^2)<1/2`, a convenient wholly integer forecast is

    P_s <= 2^(-b),       E[T] >= 2^b,
    b = max(0, floor((5e+3)/q^2)-1).                         (7)

These are conditional asymptotic forecasts, not generated matrices or
measured runtimes. At fixed q the clock is exponential in e. When q grows,
the rate changes; (7) is NOT a q-independent exponential lower bound.
There is no contradiction with the earlier `q^2>=44e` success guarantee.

## Deterministic Approximate Counting

Under the square-gap promise `(q-1)^d >= q^(2k)`, (1) gives

    a < q^(-k),
    |(q-1)^m/q^k - N_s|/N_s < 1/(q^k-1).                   (8)

For requested rational `0<epsilon<1`, use the following complete scheme:

1. If `epsilon>=1/(q^k-1)`, return the exact rational main term.
2. Otherwise compute N_s exactly by enumerating projective dual vectors.

For one representative lambda of each nonzero line, put
`w=wt(lambda B)`. Summing additive characters along its nonzero scalar
multiples gives q-1 if `lambda.s=0`, and -1 otherwise. Thus

    q^k N_s = (q-1)^m
      + sum_[lambda] (q-1 if lambda.s=0 else -1)
                     * (-1)^w * (q-1)^(m-w).               (9)

No approximate complex arithmetic is required. In branch 2 the number
of projective words is

    (q^k-1)/(q-1) < 1/((q-1)epsilon) <= 1/epsilon.

Each word uses polynomial field and integer work; all integers have
polynomial bit length in the explicit input. This is a deterministic
fully polynomial-time approximation scheme UNIFORMLY in q, under the
square-gap distance promise and effective field arithmetic. It is not
merely a fixed-q corollary or an arbitrary-epsilon claim from the main
term alone. By (6), it applies to the promised complete-AG family.

The default executable caps projective enumeration at 100000 words;
if that cap is exceeded it returns UNKNOWN, not a count. The uncapped
algorithm is the total scheme proved here. The fast branch explicitly
reports that it has NOT verified the supplied distance promise; verifying
such a promise for arbitrary matrices is not free. In the exact branch,
enumeration also checks the actual minimum distance and rejects a
contradicted promise. No capped-call performance is advertised as a total
FPTAS implementation.

No auxiliary matrix, annihilator, norm proposal, or geometric adapter is
needed for this counting scheme once the original B and its distance promise
are given. The bit-complexity proof assumes an effective valid field encoding;
the executable's FLINT primality validation is an additional implementation
check, not a new polynomial-time field-construction theorem.

This removes multiplicative approximate COUNTING at inverse-polynomial
precision as a target for superpolynomial quantum advantage on these
promises. It does not rule out improved polynomial or precision dependence,
nor close exact counting, witness search or exact uniform sampling.

## Why Count-To-Search Is Still Unjustified

After pinning j coordinates, the guaranteed residual distance can fall to
d-j, rank can drop, and some residual syndromes can be unreachable.
The count approximation promise is not self-reducible for free.

For example, over F_3, B is the all-ones row of length `m=3n+1`, s=0.
Root Fourier error is `2^(-3n)`, arbitrarily small. Yet the nonzero prefix
of 3n ones forces the last coordinate to zero, giving zero full-support
completions. The root main term is positive, and so is the false residual
main term 2/3. The test checks this obstruction exactly.

It rules out blindly using root promises on conditioned inputs, not all
count-to-search reductions or adaptive reconstruction algorithms.

## Falsifiers, Baselines And Next Decision

A valid counterexample is an admissible A,h and native input whose actual
whole-trial law exceeds (5), or a promised-square-gap matrix/syndrome whose
count scheme violates its relative-error guarantee. Tests check both
normalizers on all 625 offset cosets of a variable-rank control, all native
syndromes of four small explicit matrices, and the earlier exact acceptance
probabilities. They do not replace the proofs.

Cut from the optimization queue: sparse-h sweeps, alternate auxiliary-code
sweeps, and better incidence weighting as attempts to rescue THIS fresh
norm proposal at fixed q. Also do not present approximate counting at
inverse-polynomial precision on the native high-distance family as an
unresolved superpolynomial quantum advantage target.

Still potentially constructive: a paid method conditioning directly on
nonzero affine fibers, a genuinely different correlated repair kernel,
or a useful-problem reduction into a native promise with a known quantum
algorithm and no matched classical solver. Merely asserting such an access
primitive, increasing a norm degree, or testing more tiny instances is
not a candidate. The next pass must supply a concrete mechanism or compare
independent directions; these barriers are not a reason to stay here.

Literature check: [Nagy--Pach](https://arxiv.org/abs/2107.03956) supplies
nowhere-zero existence in its stated field range, not an extractor adopted
here. A [2026 permanent-rank preprint](https://www.preprints.org/manuscript/202608.1194)
states an additional finite-dimension existence boundary, not a verified
general fixed-q polynomial native search algorithm for this pass. It is
not peer-reviewed. No novelty conclusion follows from this bounded check.

## Independent Review And Verification

The independent reviewer accepted the scoped clock proof, including ideal
size-biased proposals, and supplied the capped-policy qualification above.
A separate follow-up accepted the deterministic counting scheme, the
projective formula, uniform-in-q bit complexity, and AG square gap. Parent
read both reports. These are independent AI audits, not human validation
or formal theorem verification. The reviewer did not audit this new code;
parent inspected the implementation and ran its exact controls.

Reports remain at
`/Users/jaspersands/Developer/qsearch-research-work/norm-clock-review-2026-10-27/`:

```text
df0b7ef312eda730d258709bf353088bd7a0aca3377c095cef53148cfa05395b  REVIEW.md
44f1f6916513ddc6465ce330d9896f9a2d987657f294dbbbba33522434ed2638  COUNTING_ADDENDUM.md
```

They are outside Git; those pointers are not backups. The standalone
proof, executable arithmetic, tests and generated report of THIS pass are
inside the repository. The reviewer is closed.

New implementation: `theorems/norm_sampler_clock.py`. New tests:
`tests/test_norm_sampler_clock.py`. Generated artifact:
`research/classical_baselines/norm_sampler_clock.json`. Reproduce with

```text
python -m theorems.norm_sampler_clock --write
python -m theorems.norm_sampler_clock --check
```

The final selected Python suite passed **197 tests in 17.23 seconds**:
31 new controls, the preceding 121 Rees review/source controls, and 45
existing isolated norm-sampling controls. The exact command from the root:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-clock-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_norm_sampler_clock.py tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py /Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/test_norm_sampling.py /Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/test_rank_weighting.py
```

Two-file `py_compile`, `qsearch.py validate` and `git diff --check` passed.
The full repository Python suite was not run. No Lean source changed in
this pass; the preceding pass's full Lean validation remains separate.
No UI/JavaScript changed and no Node check is claimed. No candidate or
central registry claim was promoted, and no commit/push or contact occurred.

An additional live call used the ORIGINAL 43-by-176 F_1019 matrix from
the earlier norm-completion receipt, with syndrome zero, distance promise
93 and requested error 1/10^6. It returned the exact rational main term
`1018^176/1019^43`, with 1759 numerator bits, 430 denominator bits,
and conditional relative-error upper bound `1/(1019^43-1)`. It enumerated
zero dual words. Rank and field entries were verified; distance and AG
provenance were reused promises, NOT inferred from this execution. The
existing input was already classically easy and no new native matrix was
generated. Input-receipt SHA-256:
`50f530fba419da9f68dbe088a8acad2fe392ead3e49aab977893e6b09ec48588`.

Integration handoff: a future CLI/registry wrapper must preserve the
distance-promise flag, exact rational error threshold, UNKNOWN cap outcome,
fixed-q qualification and distinction between counting and search.
Never upgrade the forecast rows into generated instances or measured
runtime. The next scientific pass is not more parameter sweeps on this
same proposal family.
