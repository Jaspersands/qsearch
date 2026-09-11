# Coherent Subset-Phase Query

Status: explicit measurement-family reduction and finite verification;
scalable classification and novelty remain unresolved. The bounds
below are derived and review-pending, not machine-checked theorems.

Follow-up: [Coherent terminal readouts](COHERENT_TERMINAL_READOUTS.md) now
implements parity/threshold rules and derives a random two-subset reduction
for fixed parities of any degree. A source-uniform Fourier-envelope bound
also excludes scalable corrected-all-zero success, but not arbitrary
source-aware majority decisions. Earlier next-work notes below are historical.

## Actual Program

Let G=S_n, let C be the class of fixed-point-free involutions, M=|C|, and
rho_h=(I+R_h)/|G|. The binary inputs are rho_0^(tensor k), rho_0=I/|G|,
and E_(h in C) rho_h^(tensor k). The SAME hidden h appears in every copy.

Extract and retain every individual source irrep label lambda_i. Prepare
k mask qubits in |+>^k. For mask S, apply

    U_S = sum_g a_g R_g^S = sum_nu z_nu P_nu^S,
    a_g = (1/|G|) sum_nu d_nu z_nu conjugate(chi_nu(g)).

Use one common phase rule on all subsets. The primary rule is z_nu=-1 when
chi_nu(h)<0 and +1 otherwise. ZERO characters map to +1, not zero. For
each single subset, Schur's lemma gives

    C_S = E_h R_h^S = sum_nu (chi_nu(h)/d_nu) P_nu^S.

Thus U_S is sign_+(C_S). This is NOT the sign of the sum of the noncommuting
C_S appearing in the full many-copy likelihood. Finite controls also use a
zero-character reflection and the fixed phase exp(1.3 i chi_nu(h)/d_nu).
These are specified predicates, not fitted spectral separators.

Discard the physical inputs, keep source labels and selector, apply mask
Hadamards, and measure. The resulting outcomes are a concrete readout, but
the evaluator's optimal finite Bayes table is NOT an efficient decision rule.
The alternative uniform-selector test is only a two-outcome mask readout.

## Primitive and Cost Contract

For clean GPE W, the existing intertwining identity Pi_nu W|0> =
W|0>P_nu implies

    W^dagger D_z W (|0> tensor psi) = |0> tensor U_S psi.

The full-unitary regression checks this identity, including complex phases,
on all input basis columns. By linearity it also preserves coherence between
mask addresses. No Fourier workspace is discarded before uncomputation.

On physical regular registers, each initial source extraction uses QFT,
copy/measure the label, and inverse QFT. Total costs per mask query are:

- 2k source QFT/inverse calls and 2 reference QFT/inverse calls;
- 2k controlled single-copy group actions, not 2^k calls;
- k mask qubits, two layers of k Hadamards;
- one uniform group preparation and its inverse;
- exact irrep-character phase computation and its uncomputation.

The fixed-point-free character-sign arithmetic is already implemented using
two-quotients and hook lengths; it does not enumerate every partition or
resolve an exponentially small eigenvalue by generic phase estimation/QSVT.
This exploits explicit irrep-label access, an additional structural primitive.
It does not contradict a lower bound for a generic block-encoding oracle.
With source-QFT operator error delta_s and forward-GPE operator error delta_g,
the composed channel diamond error is at most min(2,4k delta_s+4 delta_g).
This presumes an exact phase predicate and adjoint uncomputation.

Efficient finite-group QFT constructions are established background, not a
new result here: [Moore, Rockmore and Russell, Generic Quantum Fourier
Transforms](https://arxiv.org/abs/quant-ph/0304064). The repository supplies
a reduction to these primitives, not a gate-level S_n QFT or reversible
arithmetic backend. Charge coset preparation and the natural-problem reduction
separately. Logarithmic-copy information availability is already known:
[Hayashi, Kawachi and Kobayashi](https://arxiv.org/abs/quant-ph/0604174).
An efficient measurement/classifier is the missing algorithmic component.

## Source-Conditioned Kernel

For a positive-mass source lambda, let

    pi_lambda = d_lambda^2/|G|,
    p_lambda = d_lambda(d_lambda+chi_lambda(h))/|G|,
    f_lambda(g,h) = [chi_lambda(g)+chi_lambda(hg)] /
                     [d_lambda+chi_lambda(h)].

Under the null f_lambda(g,0)=chi_lambda(g)/d_lambda. For masks S,T,

    K_h(S,T | lambda_1,...,lambda_k)
      = sum_(u,v) conjugate(a_u) a_v
        product_(i in T\S) f_lambda_i(u^-1,h)
        product_(i in S\T) f_lambda_i(v,h)
        product_(i in S intersect T) f_lambda_i(u^-1 v,h).

Divide by mask count for the uniform selector state. Weight source blocks
by product pi or product p, and average alternative blocks over the SAME h.
Zero alternative source weights are omitted only in that hypothesis; their
null blocks remain. No successful branch is renormalized. Direct controlled
tensor-product unitaries independently check every conditional Gram matrix.

## Discarded-Label Bound: Strictly Separate Scope

ONLY if all source labels and physical inputs are discarded, group moments
Tr(rho_h R_g)=1[g in {e,h}] give diagonal selector kernel entries 1. For ANY
two distinct nonempty masks the off-diagonal entry is c_h=|a_e+a_h|^2.
Disjoint, overlapping and nested masks all force both coefficient indices
into {e,h}. In the null c_0=|a_e|^2.

For r nonempty masks, rho_sel=c J/r+(1-c)I/r and

    T = (1-1/r) |Delta c|,    Delta c = E_h c_h-c_0.

Delta c is the expectation difference of the norm-one two-copy observable
U tensor U^dagger. The class-mixture chi-squared calculation gives
|Delta c| <= sqrt(3/M), hence T^2 <= min(1,3/M), NOT 3/(4M).

Including the empty mask gives q=2^k, r=q-1, Delta m=E_h a_h, and

    T = [sqrt((r-1)^2 Delta c^2 + 4r |Delta m|^2)
         + (r-1)|Delta c|] / (2q).

The formula follows from a two-dimensional empty/uniform-nonempty block and
r-1 equal perpendicular eigenvalues. Parseval sum_g |a_g|^2=1 implies
|Delta m|<=1/sqrt(M). Since sqrt(r)/q<=1/2,
T <= (sqrt(3)+1/2)/sqrt(M), whose squared constant is less than 5.
Exact outward dyadic bounds are reported through n=4096 without underflow.

This argument does NOT cover retained labels, retained physical inputs,
source-dependent or mask-dependent phases, multiple queries, or arbitrary
coherent algorithms. It is an information obstruction, not dequantization.

## Attempts to Falsify the Analysis

- Complex phases and the empty mask check orientation/conjugation errors.
- All natural sources and every hidden class member check postselection
  and accidental independent-hidden averaging. S3 includes zero-mass sectors.
- Keeping source labels exposes a real product-of-marginals counterexample:
  S4, k=3, negative-character phase and nonempty masks have joint T=0.605655,
  while the sum of marginal distances is only 0.558036. The unlabeled bound
  cannot be transferred to this joint output.
- Dephasing masks removes all information beyond the original source labels.
- S4's zero-character reflection is the IDENTITY, since none of its class
  characters vanish. Its lack of gain is not evidence about harder families.
- Full-mask S4 negative-character Walsh T=33/64 beats the one-pair T=27/64.
  However, even the optimal source-plus-selector T=0.593220 is below the
  existing pair-plus-total T=59/96, which uses two label queries. Neither
  optimal finite table is a growing-degree classifier or a classical solver.

## Factorized Readout and Stronger Baseline

For the full-mask experiment, direct Hadamard expansion gives the physical
outcome operator

    A_y = sum_g a_g tensor_i [(I+(-1)^y_i R_g)/2].

Define b_lambda(g,h)=chi_lambda(g)+chi_lambda(hg), or chi_lambda(g) under
the null. The UNNORMALIZED source-and-bit probability has the exact form

    Pr(lambda_1,...,lambda_k,y | h)
      = sum_(u,v) conjugate(a_u) a_v product_i B_(lambda_i,y_i)(u,v,h),
    B_(lambda,b)(u,v,h) = d_lambda/(4|G|) *
      [b_lambda(e,h) + (-1)^b (b_lambda(u^-1,h)+b_lambda(v,h))
       + b_lambda(u^-1 v,h)].

Source weights are already included, so no division by a potentially zero
source probability occurs. The alternative averages complete products over
the same h. This formula is independently compared against EVERY grouped
probability from the direct controlled-unitary calculation, for all three
phase rules in S3/S4. Both complex phases and zero-weight sectors are checked.

Copy exchangeability makes the histogram of (source label, output bit)
sufficient for the finite likelihood. Multiply the probability of a canonical
ordering by k!/product_j c_j!, retaining normalization. With p irreps this
has binomial(k+2p-1,2p-1) outcomes, not (2p)^k. At S4,k=8 this replaces
100 million ordered outcomes with 24,310 histograms. At S3,k=12, 2.18 billion
ordered outcomes become 6,188 histograms.

This is a SIGNED |G|^2 contraction, not a nonnegative latent-variable model.
It does not give a legal classical sampler from unknown quantum coset inputs.
Neither enumeration of group pairs nor the histogram count is polynomial in
growing symmetric-group degree. It does not compile the desired classifier.

The stronger comparison uses disjoint two-copy isotypic measurements. A legal
pair outcome (lambda,mu,nu) has null mass

    g(lambda,mu,nu) d_lambda d_mu d_nu / |G|^2

and likelihood ratio 1+r_lambda+r_mu+r_nu, r=chi(h)/d. An unused source
has ratio 1+r_lambda. Pair laws are class-invariant, so their ratios multiply
across disjoint pairs despite sharing h. The implemented terminal score
`independent_pair_label_likelihood` uses exact polynomial-bit character
arithmetic for fixed-point-free involutions; it assumes actual quantum
labels and does not verify or sample Kronecker targets. It does NOT apply to
overlapping sequential pairs. Finite baseline-law enumeration is separate
from the efficient scoring of actual observed labels.

| Fixed Group | Copies | Coherent Walsh T | Disjoint-Pair T | Source-Only T |
| --- | ---: | ---: | ---: | ---: |
| S3 | 12 | 0.949747 | 0.960600 | 0.887843 |
| S4 | 8 | 0.919075 | 0.847412 | 0.534012 |

S3's apparent gain over source labels loses to a stronger known measurement.
S4 retains a finite gain over disjoint pairs, but exact character arithmetic
identifies its origin as an abelian-support control: a_e=-1/2, a_h=1/2 for
the three perfect matchings, and a_g=0 elsewhere. These four elements form
V4, so U_S=(3 C_S-I)/2 and even overlapping subset phase actions commute.
Initial source-label projectors commute with those group actions as well.
Thus this is not evidence that noncommuting operations solve a hard growing
nonabelian problem. S3's negative-character phase has nonabelian support,
but that fact alone implies no advantage either. This exact reflection audit
does not certify support for the complex rotation phase.

The coherent program uses one additional phase query versus
floor(k/2) pair-label queries; both pay initial source extraction. None of
these fixed-group numbers tests the required growing-degree advantage.

## Low-Order Selector Readout: Retained Sources

This separate argument keeps ALL classical source labels. Suppose only d
fixed mask positions are retained after the one-query full-mask program;
the other mask qubits are traced without joint processing. Observed positions
must be chosen BEFORE the input. Physical input registers are discarded.

Tracing unobserved masks forces their bra and ket addresses to agree, giving
an input-independent uniform mixture over background subsets B of the other
k-d copies. Each conditional branch coherently addresses B union A, with A
inside the observed d positions. Every such operation lies in the algebra
generated by d singleton cells and the one background cell B. No enumeration
of the 2^d addresses is needed to state this algebra inclusion.

Conditional on original source labels and h, the background moment is
product_(i in B) f_lambda_i(g,h). The finite verifier compares the direct
partial trace against an independent kernel built from this collapsed moment
for every background, source and hidden member. It includes the empty
background as a trivial representation and keeps the factor 2^-k.

For background width b>=a=2n, apply the earlier
[source-conditioned cell bound](SOURCE_CONDITIONED_PALETTE.md), retaining
the d singleton cells as FULL raw inputs and lifting just B. For n>=10,
both lifting-error bounds decrease with b; using width a is conservative.
At n=8 the implemented bound is vacuous. The comparison still retains all
k original source labels, including labels of untouched copies.

Let delta_a denote this bound at width a. Since b is Binomial(k-d,1/2),

    T_fixed_marginal <= Pr[b<a] + delta_a.

The implementation sums the binomial tail with exact integers and rounds
outward dyadically. Small backgrounds are charged at distance at most one,
not postselected away. It also takes the minimum with the raw-copy bound
T<=min(1,sqrt((2^k-1)/(4M))). For d=O(log n) and polynomial k this yields
asymptotically vanishing signal: when k<8n use the raw-copy bound; otherwise
the binomial tail decays exponentially in n, large-cell errors vanish, and
the source-label prior term k/(2 sqrt(M)) vanishes.

At S1024, k=17528, d=11, exact rounding gives T<=2^-2174. This is an upper
bound derived from an earlier review-pending argument, not a numerical
simulation at that degree, a formally verified proof, or established novelty.

It does NOT cover a general full-bit classifier, source-selected positions,
multiple queries or joint processing of discarded mask bits. In particular,
THRESHOLDING a low-degree score need not give a low-degree decision function.
A regression countercontrol has identical two-bit marginals but different
probabilities for a threshold of the sum of three bits. Thus this result
does not justify discarding arbitrary efficiently computed thresholds.
A bounded Fourier expansion with controlled coefficient l1 norm can be
bounded termwise; no such approximation to the desired classifier is yet
supplied. The next useful target is genuinely collective output structure.

## Decision and Next Falsifier

No candidate is promoted. The specified coherent primitive escapes the
small fixed-palette assumption but has no established scalable signal.
Increasing only small-group copy counts cannot establish n-scaling.

The contraction above is now derived, implemented and independently checked.
Next exploit representation structure at GROWING degree without granting an
enumerated |G|^2 sum as an efficient classifier. Fixed low-order marginals are
now obstructed under the stated contract; efficient collective full-output
decisions, including thresholds, remain open. Kill the proposal if the implemented
readout has vanishing source-weighted signal, needs exponential classical
scoring, or loses to a legal stronger baseline. A growing-degree analysis,
not another uncompiled optimal table, is the target.

## Reproduce

    python qsearch.py run EXP-COSET-BINARY-CARRIER-INSTRUMENTS
    python qsearch.py dequantize
    python qsearch.py proofs
    python qsearch.py validate

The existing experiment writes `research/representation/coset_binary_carrier_instruments.json`,
four scoped negative records, and review-pending proof obligations. Tests live
in `tests/test_isotypic_instruments.py` and
`tests/test_coset_binary_carrier_instruments.py`.
