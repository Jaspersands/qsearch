# Native Schur Expansion And Low-Variation Pivot Barriers

LOCAL DERIVATION / REVIEW PENDING. No independent theorem review, new decoder,
accepted candidate, novelty or speedup. This is a source-distribution obstruction
to a SPECIFIC structural shortcut, not an impossibility theorem for DCP.

## Why This Pass Matters

The previous varying nonsingular pencil is a real positive control. The next
question was whether native packets could supply that structure without rare
binary signatures. Code-product geometry now gives a bound covering EVERY
physical pivot subcode, not just an enumerated menu or one isotropic chart.
Higher-label-adaptive choice of that subcode does not evade a source-wide bound.

For native dense packets with k=4n^2+16 logical coordinates, this argument
forces variation rank at least floor(n/2), except on a source event bounded by
(k+1)/2^n for n>=16. At n32, the exception upper bound is about9.58e-7.
At n64 it is about8.89e-16. These are local mathematical source bounds, NOT
empirical estimates from a handful of seeds or independently reviewed results.

This excludes constant-size/logarithmic-rank pencil enumeration as a native
fixed-packet shortcut. It does NOT exclude polynomial Gaussian inversion of
large structured matrices, all-background nonsingular pencils with larger
variation, adaptive pivots, richer nonlinear graphs or quantum branch mixing.
An exponential number of matrices is not a proof that each matrix is hard
to invert. The earlier higher-carry quartic failure still matters separately.

## From A Pivot Subcode To A Product Algebra

Let B have full row rank n, C=ker(B), and R=rowspace(B)=C_perp. For a physical
t-dimensional subcode W subset C, put

    X = span(1,W),   S = R*X = R + R*W,   r = dim(S)-n.

The symbol * denotes coordinatewise binary multiplication. For a common-isotropic
pivot W, r is exactly the actual first-plane background variation rank, by the
previous Schur-product identity. The code-product calculation itself requires
no isotropic chart and applies to every W in C.

The external ingredient is [Mirandola and Zemor, Theorem3.3](https://arxiv.org/pdf/1501.06419):

    dim(S) >= dim(R) + dim(X) - dim(St(S)).

Their proof explicitly includes finite fields through base-field extension and
stabilizer descent. Lemmas2.7 and2.10 give a disjoint-component decomposition
with component count dim(St(S)). We checked these hypotheses and proof sections;
this is coding-algebra stabilization, not a quantum Clifford stabilizer.
No MDS assumption or unjustified large-field transfer is used here.

Puncture z ZERO binary columns before using full-support geometry. The active
projection of W has dimension at least t-z. If the active all-one vector is
not in C, adjoining it increases that dimension. Thus a universally valid
lower bound p for the active X dimension is

    p >= max(1,t-z + indicator(B*1 != 0)).

This support/unit correction is essential. Subcodes supported on zero columns
can have r=0. The all-one vector can genuinely belong to W when all rows of B
have even weight. The tests preserve both countercontrols.

## A Per-Instance Signature Certificate

Kneser gives at least c=max(1,p-r) product components. Let a_j be the rank of B
restricted to the j-th component. R is contained in S, so

    a_j>=1,   sum_j a_j <= n+r.

A rank-a_j binary column space has at most 2^a_j-1 distinct nonzero signatures.
Convexity maximizes the sum by assigning all spare rank to one component:

    D <= 2^(n+r-c+1) + c - 2,                     (1)

where D is the distinct nonzero-column count of B. If c>n+r, the proposed
rank is impossible outright. The certificate uses actual z, row parity and D,
and rules out EVERY t-dimensional W with extension rank at most the budget.
It needs no physical-assignment, secret, chart or subcode enumeration.
Passing this necessary gate is not an existence or nonsingularity proof.

For z0, t=n and B*1!=0, r1 permits at most n+2 signatures. Typical large native
matrices have far more. This already kills the naive one-generator field-like
extension as a scalable native family. The next argument is substantially
stronger than merely counting arbitrary small signature sets.

## Count Subspace Envelopes, Not Arbitrary Signatures

Assume only z0; allow B*1=0. Then p>=n, c>=max(1,n-r), and the component
column spaces U_j subset F2^n have total dimension h<=n+r. Their union contains
every binary column. Ordered bases for these spaces can be specified with
h binary n-vectors and cuts into nonempty consecutive groups. Counting ALL
such descriptions gives at most

    (n+r) * 2^((n+1)(n+r))                         (2)

possible envelopes. This deliberately overcounts. It includes the restrictions
that may result from any selected W; no claim that W itself is random is needed.
Every eligible envelope has cardinality bounded by the parity-free version of
(1). For r<n, that version is

    L = min(2^n-1, 2^(2r+1) + n-r-2).

After the proved low-only prefix normalization, the k binary tail columns are
IID uniform. For any FIXED envelope, the chance all tails lie inside is at
most (L/2^n)^k. Union with (2), then charge the zero-column event once:

    Pr[exists n-dimensional W with dim(R+R*W)-n <= r]
       <= k/2^n + (n+r) 2^((n+1)(n+r)) (L/2^n)^k, capped at1.  (3)

No even-row exception is needed in (3). The old signature-count/odd-parity and
pair-collision bounds remain separate valid controls; the report takes the
minimum of the independent upper bounds, not their product.

For k=4n^2+16 and r=floor(n/2)-1, (3) is already exponentially small. For even
n, L<=3*2^n/4 and (3/4)^5<1/4 supplies an entirely integer dyadic bound.
The envelope overhead is about1.5n^2 bits while the tail exponent exceeds1.6n^2.
For odd n, the envelope fits within half the signature universe, giving an
even stronger bound. The inequalities give an envelope exponent at least n
for n>=16 (the two smallest even cases are checked directly).
The saved ledger conservatively rounds that mass UP to2^-n. This yields the
stated (k+1)/2^n exception, without writing exponential-size probability strings.

This is distributional: it does not certify that one PARTICULAR packet has
no low-rank subcode unless its per-instance gate also proves it. A rare filtered
packet needs its actual selection cost. Repeated fixed-packet trials do not
turn an exponentially rare structural family into a polynomial supply.

## Adaptive Regrouping From A Source Pool Is Charged

An adaptive selection from M IID ORIGINAL registers need not have the original
packet law. It cannot simply borrow (3). For each ordered selection of m=n+k
DISTINCT registers, a full-rank binary prefix can be put first and low-only
normalized. There are at most M^m ordered selections, including every possible
column ordering and selected prefix. Apply the envelope event bound before its
conservative rounding, and multiply by that entire menu.

The probability of ANY zero binary label in the entire pool is at most M/2^n.
Charge that once globally, not once per packet menu. Consequently

    pool exception <= M/2^n
       + M^m * (n+r) 2^((n+1)(n+r)) (L/2^n)^k, capped at1.    (4)

This allows arbitrary public-label-adaptive regrouping, including higher-label
choices. It grants no same-label copies or nonnative source. Rank-deficient
output protocols and different/variable packet sizes need their own argument.

Examples with M=n^4: at n64, any selected dense packet with r<=16 has existence
upper bound about9.09e-13; at n128, r<=32 has bound about7.89e-31.
The n32,r15 pool bound is1, correctly INCONCLUSIVE. Regrouping is not dismissed
by reusing a fixed-packet bound when the menu defeats it.

## Prove The Wrong Negative Story Wrong

The structured low signature B=[I_n|I_n|1] really gives an n-dimensional W with
r1. The product decomposition has n+1 components, and the signature gate
preserves it at growing n. Its specified IID systematic TAIL signature has
mass2^(-n(n+1)); adding many structured columns does not remove that selection
obligation. The obstruction is a native low-source supply problem.

It would be WRONG to assert that the middle labels necessarily become
exponentially rare. For a low-selected independent W with variation span{I_n},
M0 is a uniform n-by-n binary matrix. The two matrices M0 and M0+I are both
invertible with probability

    p_n * sum_(j=0)^n (-1)^j / product_(h=1)^j(2^h-1),
    p_n = product_(h=1)^n(1-2^-h).

This follows by subspace-lattice inclusion-exclusion for fixed vectors inside
GL_n. The sum is at least2/7 for n>=2, and p_n>=9/32, so the product is at
least9/112. Exact n2 and n3 controls give1/8 and3/32. Constant middle acceptance
is compatible with an exponentially rare native low signature. Keep those
costs separate, and do not borrow the uniform M0 law after choosing W from M0.

## Revised Direction And Remaining Risk

Cut the constant-generator or enumerable-low-image pencil route as a native
dense-decoder proposal unless a NEW source model/reduction changes these costs.
Do not reject larger correlated pencils merely because their image is large.
Focus on compact large-rank algebraic inversion, background-adaptive pivots
with a source-correct higher-carry invariant, or genuinely quantum branch-mixing
readout. Each must still meet classical arithmetic and full-secret completion
baselines. This argument does not supply any of them.

Falsifiers for this pass: a full-rank binary code and kernel W violating the
Kneser/signature calculation; a missed zero-support or all-one exception; an
under-counted signature-space envelope or ordered pool menu; a false finite-field
theorem transfer; or an actual source that is not IID native labels. The tests
exhaust448 two-plane controls and512 three-dimensional source codes, and check
992 four-dimensional hyperplanes across adversarial support/parity profiles.
Independently recomputed product stabilizers and
exact scaling formulas remain implementation evidence, not theorem peer review.
Independent mathematical review of the envelope proof is still required.
