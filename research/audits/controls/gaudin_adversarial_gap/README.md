# Bounded native Gaudin joint-gap attack

2026-11-07. **FINITE_NONFALSIFICATION_ONLY.** One classical numerical attack,
fixed N=6, M=3, dimension20. No old control was imported, rerun or overwritten.

The objective is the minimum squared Euclidean distance between distinct
physical simultaneous-eigenvalue vectors of all six charges

    Q_i=n_i+(g/2) sum_{j!=i}(SWAP_ij-I)/(eps_i-eps_j).

This is not a scalar-combination eigenvalue gap or a Jacobian condition
number. Allowed parameters have eps_0=0, eps_5=5, adjacent spacing>=1/64,
and 0<=g<=16. Four stick-breaking coordinates cover the complete allowed
spacing simplex. Seed20261107 fixes a 60-member population; named starts
include equal spacing and three cluster patterns at g=0,0.1,1,16.

One differential-evolution run used3600 evaluations (59 generations,
iteration limit, no convergence assertion); a bounded Powell refinement
used414; selected-best recomputation used1. Total4015<=4096. Every objective
evaluation checks all charge eigenvector residuals. When the initial scalar
combination yields a mixed joint basis, the other fixed combinations from
the old control are tried. This was needed at14 evaluations. An unresolved
basis raises an error rather than returning a penalty or apparent small gap.

The smallest observed squared joint gap was **0.3531733000706801**, above
the conjectured1/6 threshold, at sites numerically near
(0,1/64,1/32,159/32,319/64,5) and g=1.01639424413733. The selected closest
charge vectors and full precision parameters are in `result.json`.
Selected-best all-charge residual:2.1234208849929104e-11; worst accepted
residual:1.2514267356216514e-9. Selected-best sum-charge error:7.11e-15;
maximum commutator entry:4.55e-13. These are floating diagnostics only.

No numerical violation triggered the immediate-stop rule
gap²<1/6-1e-6. Rationalized best parameters in the result are for possible
parent analysis only; they have no exact certificate and do not constitute
a counterexample. The experiment establishes no all-parameter lower bound,
all-N scaling, algorithm, hardness, novelty or quantum-execution claim.

Recorded command (do not repeat to extend the evaluation budget):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python research/audits/controls/gaudin_adversarial_gap/attack.py

The decisive unresolved question remains a bulk-sector polynomial joint-gap
derivation or a certified counterexample; no extension of this finite search
is queued.

## Distinct exact compressed control

`fused_control.py`/`fused_result.json` implement a later, distinct test of the
parent's two-cluster lead, with **one** fixed n=64, S=32, g=1/128 and matrix
dimension65. The real symmetric tridiagonal matrix on m=-32,...,32 has
diagonal m+g*m² and adjacent entry
-g/2*(S*(S+1)-m*(m+1)). This control does not rerun the optimization above.

Sage exact rational leading-principal-determinant recurrences give Sturm
counts0,1 at -24.173,-24.172, and1,2 at -23.904,-23.903. Full endpoint
determinants are nonzero; all adjacent entries are nonzero. Thus the two
smallest eigenvalues lie in these disjoint open width1/1000 intervals,
and their gap lies strictly in **(67/250,27/100)**, below1/2. Each endpoint's
complete exact sign sequence is retained in the result. Numerical first
eigenvalues are diagnostics, not used for the exact count assertion.

Conditional on the parent's physical fusion and finite-distinct-site proof,
the proposed squared charge-gap formula2*(Delta h)²/n is below729/320000,
which is below1/128. This file establishes only the compressed-matrix
inequality. Full native physical counterexample, distinct-site realization,
and asymptotic claims remain false in its claim gates pending that proof.
