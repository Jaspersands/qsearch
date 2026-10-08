# Native Character SDP Decoder Attempt

IMPLEMENTED NUMERICAL EXPERIMENT / NO RECOVERY THEOREM. This is an actual
secret-blind optimizer and rounding pipeline, not another perfect-fit validator.
No candidate, novelty, cryptographic attack or speedup is admitted. The input
is CLASSICAL records of lawful quantum measurements, not classical access to
the unknown native states and not coherent LWE-example access.

## Why Test This

`TERNARY_COVARIANT_NOISE.md` already proves polynomial-sample identifiability
at a sufficient surplus. Exhaustive maximization is exponential. The
`TERNARY_CHARACTER_SYNCHRONIZATION.md` circuit supplies a polynomial-size
rank-one-sound representation but had no optimizer. This pass tests whether
that representation is computationally useful, instead of re-proving that
the samples contain information or repeating a low-copy receiver variant.

Original even-native level2r supplies q=3^r, independent uniform public
rows a,c and actual phase qutrits. The existing physical covariant readout is

    y1=a.s+e1, y2=c.s+e2 modq,
    nu(e1,e2)=|1+chi_q(e1)+chi_q(e2)|^2/(3*q^2).

Errors WITHIN one pair are correlated. Three score features below are not
three independent samples. The measurement/compiler/noise law is reused,
not replaced by Gaussian LWE, a chosen evaluator or a fabricated oracle.

## Stronger Polynomial Moment Model

Compile the existing repeated-power and public unit-basis character circuit.
Identify formal circuit nodes with EQUAL ACTUAL frequency vectors. This
identification is valid for every true group character, independent of the
observations. It can drastically reduce the matrix without dropping any
compiled relation. Nodes and the constraint operator read only public labels.

For every pair of surviving frequency nodes u,v, enforce

    X >= 0, X_uu=1,
    X_uv=X_ab whenever u-v=a-b modq.

The complete difference operator is sparse and vectorized; no selected
constraint subsample is used. All inherited addition/conjugation/target
constraints are equal-frequency-difference identities and are included.
The q-loops remain present through the actual frequency-zero identification.
Every exact rank-one feasible X is therefore a genuine shared character,
by the existing circuit proof. Conversely every true character is feasible.
Polynomial node construction does NOT prove that a higher-rank feasible
point is a distribution over true characters or that optimization is tight.

For M independent original qutrit records maximize the LINEAR score

    sum_i Re[chi_q(-y_i1)*X_(a_i,0)
             +chi_q(-y_i2)*X_(c_i,0)
             +chi_q(-(y_i1-y_i2))*X_(a_i,c_i)].

On X=chi_q(u.s)*conj(chi_q(v.s)), this is exactly M times the existing
heldout_score. It is a bounded correlation objective, NOT log likelihood.
Its relation to sample identifiability is already known; noisy optimization
and actual recovery remain the questions.

If K equals q^n, the full moment matrix is group-circulant. Fourier
diagonalization makes it a mixture of characters; a unique maximizing
character gives rank1. Such small full-group controls are calibration, NOT
evidence for an efficient growing-dimensional method. The producer marks
this saturation and never constructs the group by enumeration to reach it.

## An Actual Solver And Decoder

CVXPY/SCS solves the Hermitian PSD model. Afterward independently recompute
Hermiticity, all unit diagonals, EVERY equal-difference constraint and the
smallest eigenvalue. Missing/nonfinite/infeasible matrices are not rounded.
Iteration limits, inaccurate statuses, caps and failures remain recorded.
Even a numerically feasible matrix is NOT an exact primal/dual certificate.
No certified integrality gap or optimum is inferred from a solver's status.

Round anchored column phases, the leading eigenvector and predeclared
complex-Gaussian Gram projections. For the public unit basis, round phases
to the nearest qth roots and apply its exact composite-ring inverse. This
is secret-blind arithmetic, but rounding has NO recovery theorem. Negative
eigenvalues are clipped only when drawing proposals; that is not a repaired
feasible moment matrix. Zero/weak phase entries have no privileged truth.

Refine the proposals by complete coordinate scans, choosing only TRAINING
score improvements. The same number of nominal phase starts is supplied to
a matched non-SDP baseline: zero, public noisy-basis interpolation and random
full-root secrets, with the same coordinate sweeps. The baseline pays no SDP
cost. It has at least as many distinct starting points if SDP proposals
collapse. All complete score evaluations are charged. Candidate selection
and starts cannot see the latent secret or held-out labels/outcomes.

A stronger256-start non-SDP baseline is also retained, including when the
SDP itself exhausts its matrix cap. Equal start counts alone are NOT equal
total compute: a tiny classical portfolio cannot justify an advantage over
classical decoding when the SDP costs much more. The stronger baseline does
not exhaust all classical algorithms either. Refinement batches q trial
values with checked int64 modular arithmetic and the same score; this is
an implementation efficiency, not an extra query or independent sample.

One final candidate per method is frozen before fresh held-out measurements.
Use the existing score threshold1/2 and error bounds exp(-2H/81) for H fresh
native qutrits. Each method gets the same counterfactual classical holdout
records; this is legal copying of CLASSICAL observations, not quantum cloning.
Their errors are not declared independent. A simultaneous three-method
false-acceptance bound can union their three individual bounds. Do not keep
selecting candidates or hyperparameters on that holdout.

Exhaustive reference maximization is capped separately and is NEVER an input
to the decoder. Its floating score comparisons are numerical calibration,
not a certified exact optimizer. Calibrated recovery compares against truth
only AFTER the pipeline returns. Original ring labels and every simulated
measurement are saved. PRNG seeds and distinct record IDs are not proof of
physical IID source availability.

## Costs And Falsifiers

The inherited formal node count is polynomial in M,n,logq. After quotienting,
K is no larger. Dense Hermitian storage and the complete constraint scan cost
O(K^2); a numerical PSD/eigenvalue step can cost O(K^3). Solver iteration
and conditioning costs must still be justified before a complexity theorem.
Coordinate refinement costs at most S*(1+q*n*C) complete score evaluations
for S starts and C sweeps, with O(M*n) modular work per score. This is
polynomial in q, NOT logq. A q=poly(n) upstream regime may admit that cost;
arbitrary growing roots do not. All source conversion/supply/error obligations
remain separate. Measurement precision is owed in addition to numerical
solver precision. The finite implementation limits q<=2^20 and caps complete
coordinate scans at4096; it never calls a partial scan complete.

Kill this proposal if:

- Numerical feasibility fails or large rank persists as native data grows.
- The SDP score exceeds realizable character scores while rounding fails;
  this requires an exact certificate before becoming a proved gap.
- Recovery is explained by full-group saturation or capped enumeration.
- Equal-work classical multi-start refinement recovers as well or better.
- Training score improves but fresh native prediction/recovery does not.
- Practical node counts, iterations, root scans or source supply conceal
  an exponential dependence. A matrix cap is a FAILED attempt, not an
  omitted experiment or evidence of mathematical impossibility.

Do not promote a handful of successes to a population theorem. These fixed
cohorts are a mechanism test, not a confidence-certified scaling study.
If the relaxation is useful, derive an error/tightness theorem or identify
which label-adaptive relations matter before expanding numerical sweeps.
If it fails, inspect feasible non-character directions rather than simply
trying more starts or a cosmetic alternative optimizer.

Primary context: [Singer's synchronization method](https://arxiv.org/abs/0905.3174)
motivates spectral/SDP rounding but does not prove this character model tight.
[CVXPY's complex/semidefinite constraints](https://www.cvxpy.org/tutorial/constraints/index.html)
describe the numerical interface. This pass claims no novelty for SDP or rounding.

```
python -m pip install -r requirements-research-optimization.txt
python theorems/ternary_character_sdp_decoder.py --write
node research/certificates/ternary_character_sdp_decoder_crosscheck.js
python -m pytest -q tests/test_ternary_character_sdp_decoder.py
```

Gemini/Antigravity owns qsearch/registry/UI wiring, full production validation
and Git backups. Import as a numerical research attempt with explicit failed
controls and exact-proof debt, not an accepted algorithm candidate.
