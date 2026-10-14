# Exact Full-Root Slice And Original-Data Baseline

Local constructive derivation / external review pending. This implements
full-root search ON A RESTRICTED SLICE and a costed original-data helper.
It does not implement a polynomial decoder or uniform coherent full row.

## Original Word Map At Every Root

The verified disjoint kernel directions keep every pivot WORD trit fixed.
Each active free site depends on exactly one parameter z in{0,1,2}.
Because the original selector frequency is a sum of local contributions,

```
sigma_q(z) = base_sigma + sum_j Delta_j(z_j) (modq), q=3^r.
```

This is site-additivity of the actual original labels, not an assumption
that unrestricted higher carry equations remain cubic. Each Delta is
divisible by3 because the low prefix is fixed. Its canonical residue divided
by3 gives a vector over Z_(q/3)^n. The exact remaining target is
(target-base_sigma modq)/3. All-root matching is therefore a three-choice
vector sum over the remaining ring. The shared classical MITM engine checks
the full ring target and counts modulus bits, vector payload, assignments,
memory and preflight exhaustion. The returned native word is independently
checked at the ORIGINAL q, not only at modulus9.

The paired choice vectors must not be replaced by arbitrary independent
ring vectors. On a direction's active sites, the sum of the two nonzero
remaining choices is exactly minus the sum of ORIGINAL a labels moduloq/3.
Their difference-coefficient matrix has determinant3, not a unit. Conditional
on all low labels their mod3 sum is fixed. The derived target also includes
the actual base frequency; any claimed source independence must be proved.

## Whole-Root Population Law

Condition on all low labels, full prefix rank and a fixed low-only slice and
target chosen before higher labels. IID uniform higher ORIGINAL label
digits are uniform in Z_(q/3). Every native word has a unit original
coefficient. Two distinct words differ at a site whose two ACTUAL selector
coefficient pairs have determinant+1 or-1. Thus their remaining original
frequencies are pairwise independent uniform vectors, despite the above
dependence between the derived choices. Independence is proved using the
original coefficient map, not assumed for the convenient vector-sum model.

For t slice parameters and E=n(r-1), the whole-root zero count has

```
mu = 3^(t-E)
Var(Z) = mu*(1-3^(-E))
Pr[Z>0] <= min(1,mu)
Pr[Z>0] >= mu/(mu+1)          [conservative second-moment lower bound]
Pr[Z=0] <= min(1,3^(E-t))    [conservative Chebyshev bound].
```

These are population promises, not guarantees for a given dataset or
independence of repeated queries/slices on that dataset. Search can still
be capped even if a solution exists. Large exponents remain symbolic.
With M about n^2, t about n, and r=n, whole-root witnesses are overwhelmingly
unlikely on this slice. Good first-carry behavior alone is misleading.

## Larger Bank, Real Helper And Noise Ledger

To guarantee t=E+s directions from full n+1-sized blocks, set
M=(n+1)*(E+s)+n. At r=n this is a cubic-size bank, not the earlier quadratic
bank. Complete MITM costs about3^((E+s)/2), still exponential in n^2.
For nr prescribed nonadaptive original-data probes, a union bound gives
whole-batch absence probability at most nr*3^(-s). No independence between
those probes is needed. Choose s=ceil(log3(nr))+failure_trits for a stated
batch budget. The implemented bank budget also charges low-prefix rank
failure: IID uniform slopes give the projective-hyperplane union upper
(3^n-1)/(2*3^M). Since M-n>=s, a conservative3^(-s) rank budget suffices.
It uses s=ceil(log3(nr+1))+failure_trits and total helper-failure upper
(nr+1)*3^(-s). Thus the noisy-reconstruction ledger does not hide a full-rank
conditioning event. This does not say live runtime/memory caps are sufficient.

The implementation supplies an actual label-only full-root helper with
verified PreimageReceipt outputs. It is wired into the existing classical
original-data reduction; all helper targets are called before responses are
evaluated. Returned witnesses can therefore be used to reconstruct the
ORIGINAL secret under the stated noise obligations, not merely an auxiliary
polynomial root. Exhaustion, unsupported low rank and missing slice words
return incomplete results with reasons. Small ideal/noisy reconstructions
are calibration, not a Shor-level discovery or hardness experiment.

The growing-bank ledger separately charges2M originals, exponential search,
nr probes, true source moments and label-only original-error independence.
For V=q^2/(3n^6)+1/2 the preceding union noise loss scales about24/n at the
cubic bank. It can be vacuous at small n and is not inferred from examples.
The helper is exponential; its statistical feasibility is not polynomial
compilation, nor a coherent uniform fibre sampler. No best-classical or
general quantum lower bound is established.

## Falsifiers And Next Work

Reject: a mod9 word called a full-root preimage; division by3 before proving
divisibility; independent random choices substituted for actual original
labels; a capped search called complete; one slice's failure called no
original words; or exponential compilation counted as free quantum access.

Higher-upside work is a structured bypass of the exponential vector-sum
search or a source-correct coherent row implementation. Compare against
other actual original-data lattice/combinatorial attacks. Large-bank
statistical/noise feasibility alone is not an algorithm. Keep witness
search, coherent sampling, proof review and source-hardness transfer separate.

Run `python theorems/native_full_root_slice.py --write` and its tests.
