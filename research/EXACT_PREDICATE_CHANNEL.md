# Exact Predicate Channel And Uniform Native Sampling

2026-10-22. Incorporates the separate repository review in
`independent_review_2026_10_22/EXACT_PATTERN_CHANNEL.md`. That note supplied
the stronger identity; this pass independently reconstructs it and checks it
against the actual register-level implementation. No claim of novelty,
formal verification, classical hardness or quantum speedup is made.

## Why This Changes The Research Question

The full-list protocol does more than produce approximately valid witnesses:
conditional on successful native verification, its IDEAL output is exactly
uniform over the target fiber. Its exact success probability only needs a
lower bound on that fiber's size, not a separate coherent-tail estimate.
This applies to both the scalar and the new folded relation, without making
the folded code linear over the larger block field.

The scientific bottleneck is consequently not an unproved output-distribution
assumption. It is classical search/sampling difficulty or a meaningful natural
reduction. Reversible decoder engineering is not a substitute for either.

## Input And Charged Operations

Retain the existing public field, parity space C, and balanced local predicates
f_i. Write D=C^perp under the binary trace pairing, M=|D| and V for the size
of the full product alphabet. No field-sized table or hidden oracle is added.
Let A=M^(-1/2) sum_(d in D) T_d. This notation does NOT make A freely available.

An actual full-list receiver prepares the root-product source for target b,
filters its Fourier support pattern, computes z=d+e, and performs the fixed-P
padded-list projection. Complete lists, distinct padding, full uncomputation
and rejected outcomes are essential. Its accepted unnormalized state is
A(m a_b)/sqrt(P). P is the same on every input branch. The chosen support
mask must stay within the domain where that complete list cap applies.

Our native protocol uses the Boolean radius mask. Other masks below are
identities on a small subspace, not uncharged state-preparation promises.

## Orthogonal Pattern Basis

For a local alphabet of size q_i, put

    phi_i,0 = F_i(q_i^(-1/2) * 1) = |0>,
    phi_i,1 = F_i(q_i^(-1/2) * (-1)^f_i).

Balance makes phi_i,1(0)=0. These normalized states have disjoint zero/nonzero
Fourier support. Their N-fold tensor products phi_sigma are orthonormal.
They span a 2^N-dimensional subspace W, not the entire V-dimensional space.
Every support-only mask of the balanced source lies in W.

Let R_c be the product uniform root state for predicate pattern c. Then

    F R_c = 2^(-N/2) sum_sigma (-1)^(c dot sigma) phi_sigma.

The R_c are orthonormal and have disjoint supports. Set

    A_c = {x in C : (f_1(x_1),...,f_N(x_N))=c},
    lambda_c = M*2^N*|A_c|/V.

Fourier conjugation turns A into sqrt(M)*Pi_C. Therefore the compressed Gram
operator on W is exactly H_N diag(lambda_c) H_N, where H_N is the NORMALIZED
N-bit Hadamard matrix. Its eigenvalues are the relative fiber counts lambda_c.
This does not assert that W is invariant under A or that A is a physical
isometry on arbitrary inputs.

If |lambda_c-1|<=eta for every pattern, then for EVERY v in W,

    (1-eta)||v||^2 <= ||Av||^2 <= (1+eta)||v||^2.

In particular, a support tail of ordinary mass delta has coherent mass at
most (1+eta)*delta. The older additive delta+eta estimate remains valid but
is weaker. No random-label assumption is used. A label-dependent mask may
leave W and is NOT covered; the singleton mask is a relevant example.

## Exact Paid Output Law

For an arbitrary support mask m define

    k_m(t) = 2^-N sum_sigma m(sigma) (-1)^(sigma dot t).

Changing between the two orthogonal bases gives

    F^-1 A(m a_b) = sqrt(M) Pi_C sum_c k_m(b+c) R_c.

Thus the paid protocol obeys

    Pr[pattern c AND herald] = lambda_c*|k_m(b+c)|^2/P.

Every point of A_c has the same signed/complex amplitude. Conditioning on a
nonzero-probability pattern therefore gives a uniform sample from that fiber.
For the radius mask, tau=2^-N sum_(j<=w) binom(N,j)=1-delta and k_m(0)=tau:

    Pr[native valid AND herald] = lambda_b*tau^2/P.

This is exact, including all projection probabilities. It is NOT a conditional
success rate. For native inverse trace, the already justified character/MDS
bound gives |lambda_c-1|<=eta and hence

    native success >= max(0,1-eta)*tau^2/P,
    invalid projected mass <= (1+eta)*tau*(1-tau)/P,
    total herald in [(1-eta)*tau/P, (1+eta)*tau/P].

Clip lower bounds at zero and probability upper bounds at one. The native
success assertion itself requires only a lower bound on lambda_b; bounds on
all other fibers are needed for the total/invalid-output estimates.

Verification and independent restarts give an exact uniform native sampler
in the ideal model. A finite trial cap retains ABORT with probability (1-p)^T.
Conditioned on returning an answer before that cap, its law stays uniform.
This does not turn approximate hardware gates into an exact physical sampler:
any implemented gate/source/decoder errors still need their own paid budget.

## Fixed Nonzero Syndromes

The construction is not restricted to Hx=0. Given ANY public syndrome y,
solve Hx0=y by the public full-rank linear system and set C_y=x0+C. Translate
each accepted root by -x0_i BEFORE its Fourier transform. This multiplies
the error amplitude a_b(e) by the known character chi(<e,x0>), without
changing its zero/nonzero support distribution or requiring advice.

Use the SAME complete D-list decoder, fixed padding, erasure and inverse
Fourier transform, then translate the output by x0. Apply the proof above
to the balanced predicates g_i(z_i)=f_i(z_i+x0_i) on C. It gives

    lambda_c(y) = M*2^N*|{x in C_y:f(x)=c}|/V,
    Pr[pattern c AND herald | public y] = lambda_c(y)*|k_m(b+c)|^2/P.

Native verified outputs are exactly uniform on the specified fiber of C_y.
The MDS/character bound is unchanged: translation only multiplies nontrivial
local Fourier coefficients by unit-modulus characters. This is a fixed-input
bound, NOT an average over y. A different representative x0 in the same coset
gives the same final law. Solve/translation costs are polynomial in the public
input size and remain part of the algorithm; no native witness is supplied.
For the folded relation, H and the solve are over F_q, with the same primal
and trace-dual bases as before, not a fictitious E-linear parity system.

The small register reference checks all16 syndromes and all8 target patterns
of F4,N3,K2, including empty fibers. It checks every signed amplitude after
the offset-source phase and before the final output relabeling. Separate
equivalent-offset controls check invariance of the paid pattern law. These
finite checks validate the algebraic extension, not its asymptotic complexity
or any classical-hardness assertion.

## Revised Native Certificates

The scalar n17/31/61, N=n^2, K=floor(N/8), w=floor(.6N) budgets retain P8.
Their success lower bounds exceed1/9 and approach1/8, instead of the older
triangle-bound floor near1/16. At the small F8,N4,K1,w2,b0101 fixture,
lambda_b=5/4, tau=11/16, P2 gives605/2048, matching the REGISTER operations.

For the CHANGED folded s67,r8,rate3/8 relation, n17/31/61 success floors are
approximately .0508646/.0685570/.0984480. The existing weaker floors are not
counterexamples; the artifact now uses the sharper formula. These are ideal
mathematical certificates, not native circuits or runtime comparisons.

The systematic classical accepted-completion baseline remains important.
With m=K for the scalar case, or m=ceil(K/s) for the folded case, it succeeds
with probability lambda_b*2^-m. Consequently the ratio of the TWO SPECIFIED
per-attempt success probabilities is exactly2^m*tau^2/P when lambda_b>0.
This is not an all-classical lower bound, and the different per-attempt work
must still be compared. Empty fibers or zero native amplitude cannot be
conditioned into a successful sampler.

## Adversarial Checks

The actual full-list register audit now compares EVERY final signed amplitude
against the pattern law for all32 target inputs, rather than checking only
total success. The folded trace-dual reference does the same for all10 of
its target inputs. Both preserve the paid projection ledger and empty fibers.

Additional independent tests check:

- All signed masks with entries -1,0,1 on the radius-one support patterns of
  a bounded input, against direct Fourier/coalescence arithmetic.
- A mask whose signed average is zero: native success vanishes even if other
  patterns have nonzero probability. Dropping signs would create false success.
- Every entry of the compressed Gram matrix, computed directly from the
  phi_sigma states, versus the Hadamard transform of exact native counts.
- A label-dependent mask that produces different amplitudes within one
  predicate fiber. The support-only premise cannot simply be removed.
- A physically paid, complete-list projection with BRANCH-DEPENDENT padding.
  Its output need not be uniform within a native fiber. Completeness and
  a legal probability ledger do not replace the fixed-P premise.

The last countercontrol uses P(z)=2 on singleton cosets and8 otherwise in
the F8 reference. Both paddings are feasible; their square-root ratio is2,
so it is checked in exact integer amplitudes with common denominator sqrt(8).
No invalid arbitrary nonunitary reset is used to manufacture the failure.

These are proof falsifiers, not toy-oracle algorithms or performance evidence.
The 2^N pattern calculation is an explicitly capped reference. Native bounds
use the character estimate without enumerating native fibers or patterns.

## Prior Art And Scope

[DQI](https://arxiv.org/html/2408.08292v5), Sections8 and14, already uses
Boolean Fourier/polynomial filters and covers folded/extension-field settings.
[Soft-decoder reductions](https://arxiv.org/html/2411.12553v2) connect decoding
to dual-coset sampling with explicit access and fidelity requirements. The
exact pattern formulation narrows, rather than establishes, a novelty claim.
The separate review's derivation is credited above; no new decoder or general
quantum-advantage theorem is being announced.

PRIOR-ART CORRECTION (primary sources checked 2026-10-22):
[Jo, Theorem5.2 and Remark5.3](https://arxiv.org/html/2607.16541v2) already
gives the fixed-length complete-list projection, its probability cost and
the warning about branch-dependent normalization. That primitive is NOT
new here. [Horinaga--Yamakawa, Theorem5.1](https://arxiv.org/pdf/2607.14650)
gives a generic prime-power-field quantum theorem from ordinary/coherent
tail and target-normalization bounds. The scalar inverse-trace estimates
provide those hypotheses; their separate growing-characteristic OPI result
must not be imported wholesale. The present per-instance predicate analysis
is at most a candidate specialization/simplification, not certified novelty.
For the folded F_q-linear, E-block code, check the appropriate code/alphabet
contract separately rather than silently treating it as E-linear.

The result is an IDEAL uniform sampler for a specifically constructed relation
under the explicit source, list and fiber-count conditions. It supplies no
reduction from factoring, lattices, arbitrary MQ, code equivalence or another
standard hard problem. Failed classical baselines and near-uniform fiber
counts are not hardness proofs.

NEXT: constructive classical completion/sampling or a meaningful application.
Do not build a new mask-optimization framework or continue improving constants
as a proxy for that question. The independent review files remain untouched.
