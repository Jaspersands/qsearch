# Inverse-Trace Alphabets Do Not Admit Short Error-Free Local Lists

Status: written deduction from the standard Kloosterman bound, with bounded
exact controls. Not independently reviewed or proof-assistant checked. No
new quantum algorithm, native search experiment, or classical hardness claim.

## Research Decision

Do not import the unambiguous pair measurement from
[Ragavan and Shutty, Section 2.1](https://arxiv.org/html/2610.00502v1#S2.SS1)
into the native inverse-trace problem. Their full-support alphabet admits
two-element lists, enabling quadratic relinearization and a Schur-square
decoder. Our alphabet does not: every nonzero error-free single-symbol
measurement outcome needs an exponentially large list. This is a different
alphabet, not a refutation of their algorithm. Their fixed-field complexity
guarantees also must not be transferred to our exponentially growing field.

The relevant general tools are standard Fourier concentration and Gram-matrix
bounds. No novelty for those tools, or literature-wide novelty for this
application, is asserted. The project contribution is a concrete admission
test for this proposed algorithmic import, including its approximate version.

## Unchanged Native Relation And Local Access

The native task has odd n>=5, q=2^n, N=n^2, K=floor(N/8), an explicit binary
field and N original distinct public points alpha_i. Find x with

    sum_i alpha_i^j x_i = 0  (0<=j<K),
    Tr(inv0(x_i)) = 1        (all i),

where inv0(0)=0. Do not replace the predicate by x_i!=0, change the points,
plant a solution, or discard parity checks. The local alphabet is

    A = {a in F_q : Tr(inv0(a))=1},   |A|=q/2,   0 not in A.

For chi(t)=(-1)^Tr(t), the local decoder states, in Fourier coordinates, are

    |phi_c> = sqrt(2/q) sum_(a in A) chi(c*a)|a>,  c in F_q.

They are unitarily equivalent to the shifted Fourier-set states in the
Regev/DQI decoder interface. Preparing the set state is not a new obstacle:
prepare a uniform trace-one element and reversibly invert it. This does not
provide extra copies of an unknown decoder symbol for free.

The theorem concerns ONE such register and label-independent ancillas. Its
posterior claim requires a uniform classical c. A uniform codeword in the
native dual code has uniform coordinates, but conditioning on measurements
of other coordinates can change that prior. Global coherent codewords and
joint measurements are not reduced to independent symbols by this note.

## Fourier Input To The Proof

Write W(b)=sum_a chi(inv0(a)+b*a). Inversion permutes F_q, so W(0)=0. For b!=0,

    W(b) = 1 + sum_(a!=0) chi(1/a + b*a) = 1 + Kl(b),
    S(b) := sum_(a in A) chi(b*a) = -W(b)/2.

Changing variables t=b*a gives the usual Kloosterman sum chi(t+b/t).
The Weil bound gives |Kl(b)|<=2*sqrt(q), also in characteristic two; see
[Keith Conrad, On Weil's proof of the bound for Kloosterman sums](https://doi.org/10.1016/S0022-314X(02)00011-2)
and the [author's manuscript](https://kconrad.math.uconn.edu/articles/kloosterman.pdf).
Thus |W(b)|<=B:=min(q,1+floor(sqrt(4q))). This integer upper envelope is
deliberately conservative; no floating-point rounding or full-field table
is needed to compute it. S(0)=q/2. Exact small-field spectra can sharpen B
only for those fields and are not a scalable attack or hardness certificate.

## Theorem: A Bound For Every Positive-Mass Outcome

Let a one-copy measurement outcome have effect M and output a set L of ell
labels. Restrict M to the coordinate space H_A and require Tr(M)>0 there.
It may be mixed, complex, noncovariant and part of a postselected instrument.
For uniform c and nonempty L,

    Pr[c in L | outcome] <= min(1, 1/2 + (ell-1)*B/(2q)).       (1)

For an empty list the probability is zero.

Proof. Let F be the normalized additive Fourier transform and P_A,P_L the
coordinate projections. The ensemble average is P_A/|A|. Consequently the
posterior is exactly

    Tr(M P_A F^dagger P_L F P_A) / Tr(M).

It is bounded by the largest eigenvalue of that positive contraction. Its
nonzero eigenvalues equal those of G_L=P_L F P_A F^dagger P_L. The diagonal
entries of G_L are 1/2. Every off-diagonal entry has magnitude at most B/(2q)
by the preceding Fourier bound. The maximum absolute row sum bounds its
operator norm by 1/2+(ell-1)B/(2q). This proves (1). Scaling M or allowing
arbitrarily rare postselection cannot improve the conditional bound. QED.

An error-free outcome must have zero probability for every c outside L.
Since the uniform prior has full support, its posterior is one. Hence

    ell >= 1 + ceil(q/B) = Omega(sqrt(q)) = Omega(2^(n/2)).     (2)

More generally confidence eta>1/2 requires

    ell >= 1 + ceil((2*eta-1)*q/B).                            (3)

Thus even a constant reliability above one half cannot be obtained from
polynomial(n)-sized local lists. The unambiguous statement does not need a
uniform operating prior, provided error-freedom is required for ALL labels.
If side information eliminates labels from the promise, that is a new model.

An equivalent exact falsifier is useful for small controls: an error-free
effect exists for a given L iff the matrix (chi(c*a))_(c outside L,a in A)
has a nonzero nullspace over the complex numbers. This matrix is integral,
so rational rank is sufficient. Any nonzero null vector can be rescaled to
give one legal rank-one effect. This does not by itself construct a full
measurement with a desired total success probability.

## Attempts To Break The Conclusion

1. **Wrong normalization.** The posterior denominator is q*||v||^2 for
   an unnormalized rank-one vector v in H_A. The implementation checks
   posterior mass one on all labels, and independently checks Fourier noise.
2. **It rejects every alphabet.** False: an affine halfspace has a valid
   pair outcome. The n=2 inverse-trace alphabet is also such an exception.
   For native n>=5, and indeed n>=3, the bound excludes pairs.
3. **A rare herald fixes it.** Equation (1) is outcome-wise, not an average
   success estimate, so rare heralds without label advice do not fix it.
4. **The local symbol is completely inaccessible.** False: Fourier
   readout guesses c correctly with probability EXACTLY 1/2. For a pair
   {c,d}, the best posterior is exactly 1/2+|W(c+d)|/(2q), attained by the
   larger eigenvector of its two-column Gram matrix. Both are controls.
5. **Other coordinates give advice.** Possible and OUTSIDE (1). A prior
   concentrated on a known c permits a singleton with certainty. Global
   decoding, adaptive code correlations and joint POVMs remain open here.
6. **Two copies or a different source fix it.** Not excluded. Neither
   extra copies of the same unknown symbol nor a changed state family
   follow for free from the native decoder input. Charge and analyze them.
7. **A large set has a succinct equation.** Possible. Large cardinality
   does not imply large circuit-description complexity. Equation (2)
   excludes a low-degree nonzero UNIVARIATE field polynomial that vanishes
   on every label of an error-free outcome: degree>=ell. It does not exclude
   low-description Boolean constraints, Frobenius structure, or a different
   global solver. Degree growth alone is not a runtime lower bound.

## Scope, Verification And Next Scientific Step

This does not refute the existing conditional global inverse-trace/DQI
construction, prove native classical hardness, provide a sampler, or solve
the public-carry acquisition problem. The supplied-carry norm solver and
its independently verified native witness remain unchanged.

The finite verifier uses the existing BinaryField arithmetic authority and
exact FLINT rational ranks. It enumerates q^2 characters only for q<=128.
Symbolic scaling at large n uses integer arithmetic only; it is a theorem
calculation, not large-field numerical evidence. Tests cannot establish
asymptotic correctness independently of the proof above.

Reject the direct pair/relinearization transplant. Do not spend another
pass optimizing local pair measurements or extending nearby barriers. A
useful replacement must exhibit a GLOBAL decoder or a charged new source,
and must survive the existing matched classical attacks. Before building
one, compare it against the repository's already-known complete-list
decoder and source-normalization proof; do not repackage those as novelty.
