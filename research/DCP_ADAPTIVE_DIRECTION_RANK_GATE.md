# Full-Label Pre-Complement Single-Direction Descent Gate

Local derivation, external review pending. No novelty claim. No new algorithm,
general DCP lower bound, or quantum speedup admission.

Run `python qsearch.py dcp-adaptive-direction-rank-gate` and replay
`node research/certificates/dcp_adaptive_direction_rank_gate_crosscheck.js`.
The artifact is `research/phase_workbench/dcp_adaptive_direction_rank_gate.json`.

## Research Question

The higher-modulus carry-source compiler requires directions selected without
using higher label bits. Can arbitrary computation on ALL public labels avoid
the supply penalty? For ONE retained direction fixed before complement-Z
measurement, the answer is constrained by a different source of randomness:
the later complement outcomes. We never assume higher labels remain uniform
after selecting a direction from them.

Here n is the number of secret-vector components, NOT log of a cyclic group
order. The asymptotic result uses m=3n and n growing. It says nothing like
an exponential-in-log(q) lower bound for ordinary scalar DHSP (n=1).

## Exact Fixed-Label Posterior Law

Let q=2^t, t>=3, and A be an n by m matrix of public labels. The pure native
input has flat amplitudes with phase

    exp(2 pi i <s, A x>/q),  x in F_2^m.

Set B=A mod 2 and D=ker(B). Measuring the public parity chart leaves a
uniform-amplitude affine packet x0+D. Choose ANY nonzero u in D using A
and the initial syndrome. Extend u to a basis of D and measure the other
coordinates in Z, retaining a single phase qubit. The choice and chart must
be fixed BEFORE these complement outcomes. No source-preparation inverse
or secret-dependent computation is available to the selector.

Every complement outcome is equally likely, for every secret. For background
x, the new label modulo Q=q/2 is the integer vector

    a'(x) = sum_i (-1)^x_i A_i u_i / 2 mod Q.

The numerator is even because Bu=0. Reducing the label modulo 2 gives

    a'(x) mod 2 = c(A,u) - B diag(u) x,
    c(A,u) = sum_i A_i u_i / 2 mod 2.

On x=x0+w, w in D, this is a uniform affine image of

    T_u = B diag(u)|_D.

The physical outcome is a quotient D/<u>, not D itself. But T_u u=Bu=0,
so the pushforward has exactly the same law. Reversing the retained qubit's
orientation negates a', which also preserves its low bit.

Consequently, the probability that ALL output components are even is either
ZERO (an inconsistent affine target) or exactly 2^-rank(T_u). This event
allows ONE further phase-level descent to q/4. It includes the useless zero
label and does not imply any secret recovery.

The compiler exports the affine offset, image basis, dual parity equations,
kernel basis, target consistency, rank and exact binary probability. It
accepts arbitrary fixed A, not just typical or independent A.

## Connectivity Rank Identity

For S=supp(u),

    rank(T_u) = rank(B_S) + rank(B_(E-S)) - rank(B).

Indeed, ker(T_u) inside D is the direct product of the kernels on S and its
complement: both restricted column sums must vanish. Subtract their total
dimension from dim(D)=m-rank(B).

The right side is the standard column-matroid connectivity function, using
the convention WITHOUT +1. See P. D. Seymour,
[On the connectivity function of a matroid (1988)](https://collaborate.princeton.edu/en/publications/on-the-connectivity-function-of-a-matroid/).
That reference supplies mathematical background, not this DCP source claim.

## Uniform Native Random-Matrix Bound

Let B be IID fair binary, m=3n. Choose 1<=r<=w<=n/2. A good B has full row
rank, no nonzero kernel direction with support or complement smaller than
w, and connectivity at least r across EVERY cut with both sides at least w.
This is a simultaneous event on B, not a union bound over a particular
algorithm's menu. On a good B, EVERY full-label-dependent pre-complement
selector has extra-descent probability <=2^-r, uniformly over initial syndrome.

Three elementary union bounds give its failure probability epsilon:

    e_rank = (2^n-1) / 2^(3n),
    e_support = [2 sum_(j=0)^(w-1) binom(3n,j) - 1] / 2^n,
    E_min = (n-r+1)(w-r+1),
    e_cut = min(1, 16(n+1)^2 2^(3n-E_min)),
    epsilon = min(1, e_rank + e_support + e_cut).

For each nonzero u, Bu=0 has probability 2^-n. Count the low-weight masks
excluding zero and the near-full masks INCLUDING the all-one direction.
The latter can have connectivity zero and must not be silently excluded.
For full-rank failure, union over the nonzero left-kernel vectors.

For completeness, an n by s uniform binary matrix has

    P(rank<=a) <= 4 * 2^[-(n-a)(s-a)].

Count matrices whose columns lie in an a-dimensional subspace. The binary
Gaussian-binomial count of such subspaces is at most 4*2^[a(n-a)]: the
denominator product of (1-2^-j) is >1/4. Its first factor is 1/2 and its
remaining product is >=1-sum_(j>=2)2^-j >=1/2, with strictness at finite a.
The two column blocks are independent. Thus a fixed rank pair a,b costs at
most 16*2^-E, where

    E=(n-a)(s-a)+(n-b)(3n-s-b).

When rank(B)=n and connectivity<r, write a+b=n+k, 0<=k<r.
By complement symmetry w<=s<=3n/2. As a quadratic in a,

    E=2a^2+a(n-2s-2k)+(n+k)s-2nk+k^2,  a>=k.

Its unconstrained minimizer is a*=s/2+k/2-n/4. If s<=n/2+k, the
constrained minimum is (n-k)(s-k), attained at a=k. Otherwise its relaxed
minimum is

    (n-k)(2n-k)/2 - (3n/2-s)^2/2.

Both are nondecreasing in s up to 3n/2. Since w<=n/2, E is at least
(n-k)(w-k), which decreases with k for k<=r-1. Hence E>=E_min.
Equality is feasible at s=w,a=r-1,b=n. Restricting to integer ranks cannot
lower this continuous bound. Union over <=2^(3n) cuts and <=(n+1)^2
rank pairs yields e_cut. Small integer minimizations are independently replayed;
they check the algebra but do not replace this all-n proof.

The native-source mean extra-descent probability is therefore at most

    epsilon + (1-epsilon)*2^-r.

The default w=floor(3n/32), r=floor(w/2) gives exponential decay in n, with
an exponentially small support exception and a quadratically decaying cut
exponent. This uses H_2(1/32)<1/3 for the support term. The small-n union
bound can be VACUOUS; the artifact records this rather than inferring hardness.
Scaling rows are exact theorem arithmetic, not executed large source trials.

The native mean is BEFORE source or syndrome postselection. Although the
good-B statement holds for every initial syndrome, conditioning the entire
source on a syndrome can reweight bad B. Such conditioning must be charged
separately. Selecting exceptional B and quoting the unconditional bound
would also be invalid.

## Attempts To Falsify It

- All-one kernel direction: rank zero, and deterministic descent can occur.
  Its native rarity is explicitly included in e_support, not ignored.
- Zero matrix: every direction has rank zero. The fixed-label compiler accepts
  this exception and reports its true law; it does not claim every B is hard.
- Higher-label selection makes the ZERO-background label even. The live
  controls choose u by this criterion. Random complement backgrounds still
  produce the nontrivial affine image, so this does not force descent.
- A target outside the affine image gives probability zero even if rank is
  small. The certificate checks consistency, not just 2^-rank.
- Direct enumeration evaluates the ORIGINAL signed phase labels on physical
  complement pairs, not the same affine-map formula in different syntax.
- Python tests check the actual two-amplitude conditional density matrices,
  arbitrary small secrets and all parity-chart syndromes.
- The independent JS checker recomputes kernels, ranks, affine output counts,
  every stored pair label, all scaling bounds and rank-pair integer minima.
  Tampered image bases, probabilities, labels, scope and exponents must fail.

## What This Does Not Eliminate

This does NOT cover direction choices after complement outcomes, retaining
correlated multi-qubit packets, non-Z or coherent collective instruments,
correlated/non-native sources, mixed-state noise, or decoders that recover
information without making every label component even. It does not prove
an optimal Kuperberg/Regev cost or a general query lower bound. No physical
quantum source is executed by the deterministic certificate workflow.

Next useful search: retain a correlated packet and identify a paid collective
observable, or derive a genuinely outcome-adaptive instrument with its own
source/noise law. Repeating high-label direction search before the SAME
single-output complement instrument cannot remove this rank penalty on good B.
Central registry promotion is deliberately deferred pending external review;
the report contains a scoped provisional negative record only.
