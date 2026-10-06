# Gaussian Endpoint Drive: Construction And Falsifiers

LOCAL DERIVATIONS / REVIEW PENDING. No accepted candidate, efficient decoder,
novelty claim or general quantum lower bound. This continues
[pointed native triples](TERNARY_POINTED_TRIPLES.md), but is NOT their
three-corner extraction instrument. It uses only the linearly invertible
second endpoint and retains the original full-root phase state.

## What Is Constructive

For native even level L=2r, q=3^r, dimension n and block width m=n+2, the
public frequencies a_i,c_i are IID uniform vectors in Z_q^n. The input is

    |psi_s> = 3^(-m/2) sum_x exp(2*pi*i*<F(x),s>/q)|x>.

The pointed constructor chooses a canonical GF3 difference kernel word w
with its first two free coefficients equal to1. Its second endpoint is
z=x+v, with v_i=1 when w_i=2 or when w_i=1 except at its first1.
The three-corner incoming problem remains unresolved. Here ONLY corner2 is
used, and anchors with difference rank below n are explicitly discarded.

For each polynomially enumerated inverse case at vertex z, unknown pivot
coefficients satisfy A*u=target over GF3, with domain restrictions before
the first1. Column i of A is f_i(z_i)-f_i(z_i-1); coefficient2 contributes
minus that column. This is genuine linear algebra, not a three-choice
witness oracle. RREF yields all affine-kernel solutions, followed by domain
filtering and canonical forward verification.

Set b=ceil(log_3(m)). EXCLUDE any case with nullity>b, regardless of whether
it is consistent. The outgoing predicate imposes the SAME cutoff on its
actual inverse case. Remaining cases enumerate at most3^b<=3m vectors.
There are at most C=m*binom(m,2) cases. Thus incoming access is complete for
this explicitly cut graph and pointwise polynomial, even on atypical labels.
This does not silently truncate an enumerator while claiming completeness.

## Retained Native Mass

At a fixed vertex and fixed case, the unfiltered n-by-k matrix A is IID
uniform and k<=n. The target contains an independent free-coordinate
frequency with unit coefficient, so is uniform independently of A.
Conditional on A, the mean affine solution count is3^(k-n), including
inconsistent targets. This remains true when conditioning on bad nullity.
For d=b+1, a union over d-dimensional kernel subspaces gives

    Pr(nullity(A)>=d) <= [n choose d]_3 * 3^(-n*d) = U.

Worst-case k=n dominates smaller k. Each discarded actual full-rank arc is
counted by one such inverse case. Translation to average uniform vertices
therefore bounds removed anchor fraction by C*U. Native average full-rank
anchor mass is at least17/18, so retained arc fraction is at least

    max(0,17/18-C*U).

This is a SOURCE-AVERAGE bound, not a guarantee for each frequency matrix.
No independence between different vertices or cases is assumed.

## Actual Collective Operator And Access

For every retained directed arc x->z, add the term

    (|x>-|z>)(<x|-<z|)

to a Laplacian L_G. Duplicate undirected arcs, if present, are counted with
multiplicity. The sparse row combines ALL retained predecessors and the
outgoing arc. Weighted degree<=1+C*3^b, row nonzeros<=2+C*3^b,
largest entry<=1+C*3^b, and norm<=2*(1+C*3^b). The uniform state is exactly
stationary. A nonzero native phase state generally is not:

    <psi_s|L_G|psi_s> = 3^(-m) sum_(x->z) |chi_s(F(x))-chi_s(F(z))|^2.

For primitive s (at least one coordinate nonzero mod3) and r>=2, conditional
high lifts make each nonempty changed-coordinate frequency difference
uniform at the higher modulus. The native-average energy is twice the
retained arc mass. Distinguishing s=0 from nonzero is NOT a new hard problem
or a secret-recovery algorithm.

`laplacian_row` and `sparse_row_locations` are actual bounded classical oracle
programs. The latter supplies a fixed-width sorted DISTINCT index list with
zero-entry padding; its inverse is a bounded search on the same list.
Padding inspects at most the polynomial row bound, not a hidden cube table.
For binary-register embedding, unused basis words are zero rows, with their
own distinct zero-entry padding. Extend the sorted row-index injection to a
permutation by mapping remaining indices to the ordered complement of its
image. Complement selection and its inverse use the same polynomial list
and integer rank/select, so do not require a full dimension-sized table.
Gate-level reversible compilation is NOT
supplied; bounded loops, comparisons and GF3 arithmetic must be compiled
and workspace uncomputed. Use the conservative row bound, not an uncharged
global degree maximum.

[Berry, Childs and Kothari](https://arxiv.org/abs/1501.01715) provide the
standard sparse-Hamiltonian simulation route. Their
[primary conference text, pp.1-2](https://qipconference.org/2015/talks/78-Berry.pdf)
specifies entry and index oracles and explicitly charges reverse-index
access for in-place indexing. Here those programs are bounded; oracle cost,
entry precision and reversible compilation still count. Polynomial-time
evolution requires polynomial t and precision costs. A small spectral gap,
mixing, cooling or a decoder does NOT follow from simulation access.
For one block the conservative simulation parameter d*max_entry*t is
O(n^8*t), before oracle-program costs and logarithmic precision factors.
For K blocks the corresponding conservative bound is O(K^2*n^8*t).

## Falsifier One: Arbitrary Collective Low-Label Control

Allow ANY collective POVM depending on all LOW labels, arbitrary ancillas,
and unlimited classical postprocessing using all full labels. High labels
may NOT influence quantum control before the final classical record.
Secrets are uniform on the primitive set, of size N=q^n-(q/3)^n, and r>=2.
Conditional on lows and fixed primitive s, the two high phases per input
are independent uniform roots of order q/3>=3, with fixed low rotations.

For a onehot phase polynomial a+z*b+w*c,

    E|a+z*b+w*c|^4
      = |a|^4+|b|^4+|c|^4+4*(|a*b|^2+|a*c|^2+|b*c|^2).

Applying this coordinate by coordinate, Cauchy on cross terms, and
sum(X^2)+4*sum(XY)<=(5/3)*(X+Y+Z)^2 proves, for ANY entangled coefficient f,

    E|p_f|^4 <= (5/3)^M * ||f||_2^4.

There are no root aliases: each high-phase exponent difference lies in
[-2,2], while the root order is at least3. For a positive effect E, its
spectral decomposition and Minkowski give

    E_high[p_E^2] <= (5/3)^M * (Tr(E)/3^M)^2.

Use reference weights Q_y=Tr(E_y)/3^M, not uniform outcome weights. Decision
regions may depend on ALL full labels. Cauchy across secret, high labels and
outcomes, followed by POVM completeness, yields

    native-average correctness <= min(1,sqrt((5/3)^M/N)).

At entropy width M=nr, its square is (5/9)^(nr)/(1-3^(-n)). This screens
arbitrary low-controlled collective dynamics, not just a product readout.
The squared expression bounds the SQUARE OF MEAN success; no claim about
the mean of squared per-label success is made by this argument.
It is NOT a per-fixed-label bound or a general quantum lower bound. More
charged samples, high-label quantum control, different sources or access
fall outside. Bounded exact character controls are not independent theorem
review. Outcome feedback is included only while quantum control remains
independent of high labels.

## Full-Label Dressing And Its Own Ceiling

An actual public full-modulus control is

    h(F)=2^(-1)*sum_l F_l^2 mod q,
    D_h|x>=exp(2*pi*i*h(F(x))/q)|x>,
    L_h=D_h L_G D_h^dagger.

`chirp_exponent` and `sparse_entry_spec` use exact integer modular arithmetic;
floating complex evaluation is calibration only. Computing F and h is
polynomial in physical inputs, dimension and log(q). Known controlled phase
rotations need charged approximation precision and uncomputation, but no
unknown secret, state copying, state inverse or QRAM. The complete-square
identity motivates this test; it does not implement a group Fourier transform
or erase frequency-fiber garbage.

K independent blocks use sum_b L_b. A chirp of the GLOBAL F=sum_b F_b
contains cross terms and entangles blocks. It escapes the preceding low-only
premise. It does NOT change the graph spectrum or connect its components.

Let C run over graph components (Cartesian products for K blocks), and
eta_(C,f) count words in C of full frequency f. ALL component-preserving
receivers, including arbitrary full-label-dependent controls, have optimal
uniform full-secret success

    sum_C (sum_f sqrt(eta_(C,f)))^2 / (N_full * 3^M).

Proof: measuring the component has secret-independent weight |C|/3^M.
Within C the states are group-covariant. Averaging a POVM over the group
fixes its diagonal entries in the orthogonal frequency-fiber basis to1/N_full.
Positivity bounds every off-diagonal by1/N_full; a rank-one covariant seed
attains the stated square-root expression on the state span. This is an
optimal REFERENCE, not an efficient normalization or decoder.

More simply, success<=sum_C |C|^2/(N_full*3^M); for uniform primitive secrets
replace N_full by N. Complete enumeration of all729 one-dimensional LOW
sources and19,683 anchors gives mean uniform-word component size

    lambda_1=7357/729.

Independent three-input blocks therefore satisfy native-average full-secret
success<=min(1,lambda_1^K/3^r). At entropy width3K=r this is
(7357/19683)^K. This includes high-label-controlled operations preserving
product components. It is NOT a no-go for cross-component quantum operations
or larger sample budgets; a constant-factor sample surplus can make it
vacuous. Do not extrapolate the n=1 census to growing n.

## What The Actual Replay Says

All controls use canonical original native labels, full roots and charged
physical inputs. No generated oracle problem or field-shadow source.
At n=2,q=9,M=4,t=1.3, uniform full-secret ML success is about0.04567 without
dressing and0.04460 with it; unrestricted PGM reference is about0.63616.
At n=1,q=81,two blocks,M=6,t=1.3, the corresponding figures are0.10111 and
0.05895, versus unrestricted PGM about0.96704. ML here enumerates ALL secrets
and is explicitly not an efficient classical decoder. These fixed-source
calibrations do not estimate source-average scaling or violate either bound.

There is no positive algorithmic signal. A naive quadratic dressing is
deprioritized. The useful contribution is complete polynomial row access
plus two sharp scope gates. Before more parameter searches, supply a
high-label-controlled, cross-component mechanism and a computable outcome
estimator with a correctness argument. Otherwise this is a simulated
collective dynamics experiment, not progress toward full secret recovery.

## Next Work And Falsifiers

- Independently review affine inversion, nullity-tail counting and both
  measurement bounds. A missing retained predecessor falsifies row access.
- Any valid low-controlled POVM exceeding the NATIVE-AVERAGE L4 bound under
  its exact sample/access assumptions falsifies that proof, not a single
  selected source above its ensemble bound.
- A component-preserving receiver exceeding the fixed-source component PGM
  ceiling falsifies the ceiling or the claimed component-preservation.
- Construct additional high-label-dependent OFF-DIAGONAL moves that connect
  components and retain bounded reversible incoming access. A diagonal
  phase alone cannot fix this obstruction.
- Require an explicit polynomial outcome estimator and growing-root source
  correctness before optimizing quantum dynamics. Compare legal raw-sample
  inference, known sieves, and all batch-selection costs.
- Do not transfer this graph's arc mass to an odd-qutrit extraction source
  law. No three-corner instrument or throughput recursion is compiled here.

## Reproduce

    python theorems/ternary_gaussian_drive.py --write
    python -m pytest -q tests/test_ternary_gaussian_drive.py
    node research/certificates/ternary_gaussian_drive_crosscheck.js

GPT owns the mathematics and targeted verification. Gemini owns routine
registry/CLI integration and full production validation. No UI work or
accepted candidate is justified by this pass.
