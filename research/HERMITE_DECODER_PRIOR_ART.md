# Hermite Decoder: Exact Prior-Art Boundary

2026-10-21. Literature and proof-interface audit. This supersedes optimistic
novelty readings of the preceding Hermite notes, without retracting their
algebraic controls. No new quantum algorithm or independently reviewed
theorem is claimed.

## Verdict

**Polynomial-time decoding with polynomial workspace is not a credible
novelty claim here, even when multiplicity grows.** The relevant affine-space
and noiseless-pinning ingredients already exist. The only surviving possible
addition in this line is their tightly space-accounted coherent streaming
composition. That might be useful, but it is not a new decoding mechanism
or a plausible Shor-level result by itself.

Do not spend another pass expanding Hermite examples or parameter sweeps.
Keep the compact implementation as a candidate implementation of known
ideas, pending independent review. Compare a genuinely new constructive
direction before extending it.

## Correct Source Version

[Kopparty, Ron-Zewi, Saraf and Wootters, ECCC Revision 2, February 22,
2023](https://eccc.weizmann.ac.il/report/2018/091/revision/2/download/):
Theorem 3.7, page 21, gives a deterministically computable low-dimensional
space for multiplicity decoding, including degrees exceeding the
characteristic. Theorem 3.8 also gives a randomized list-recovery algorithm.
Lemma 3.1 and PRUNE appear on pages 17-20; Appendix A on pages 44-47 supplies
the differential construction. The older arXiv version is not this revision.

[Guruswami and Wang, arXiv:1106.3951v1](https://arxiv.org/pdf/1106.3951),
Section 4.2, Theorem 9 and Remark 3, already avoid list enumeration using
noiseless derivative information. Their large-characteristic assumptions
must not be silently transferred to our high-degree setting.

[Wu and Yang, arXiv:2610.01902v1](https://arxiv.org/html/2610.01902v1),
Section 1.4, asks for polynomial postprocessing with similar space and pass
bounds. Their Theorem 1.6 covers every multiplicity. Our proposed decoder
only covers sufficiently large multiplicity relative to the target accuracy.

Downloaded revision SHA256:
`9b0f51d2547724f60df87aeccd00129ccf2723e4da2cb2c880cc144d9d5fff33`.
This is provenance, not a proof checker.

## What Already Follows From The Known Interface?

Translate source multiplicity `s` to our `ell`, source list size to one,
and source message degree to `K-1`. Its derivative count corresponds to
our differential order plus one. The ambient solution space has dimension
`O((1+(K-1)/q)/epsilon)` over a prime field.

Given a syndrome, our explicit dual map and right inverse convert its
error fiber into a received word. Apply the known differential-space
construction to that word. Retained error coordinates supply true jets of
the fiber polynomial at the pin locations, via the same public linear
maps. Solve those pin equations inside the affine space.

This is NOT free advice about the answer: those coordinates must be kept
in the augmented quantum label, and their score loss and storage are
charged. Their values are not obtained from a hidden solution oracle.

For half-rate polynomials, every nonzero difference has nonzero jets at
at least half the evaluation points. While the unresolved subspace is
nonzero, a fresh uniformly sampled pin therefore drops its dimension
with probability at least one half. Without replacement, previously
selected points are already common zeros, so this lower bound does not
decrease. A binomial lower-tail estimate gives
`O(dimension + log(1/eta))` pins for failure at most `eta`.

Consequently, with polynomial workspace, there is no need to enumerate
the output list at all. Construct the affine space, add true pin
equations, and accept only a unique solution that passes the guarded
radius checks. Reversible simulation gives polynomial time and space.
The precise source-loader, score and error analysis still have to be
composed; a list-decoding theorem alone is not a quantum algorithm.

For fixed `ell` and fixed gap, the published list bound is independent of
`q`. For growing `ell`, that enumeration bound is not uniformly polynomial
in `ell`. **This does not rescue a time-only novelty claim:** the affine
construction plus retained pins avoids enumeration in both regimes.

The coarse source condition `ell >= 16/epsilon^2` need not match our
smaller explicit constants. Better constants in a sufficient region
would not constitute a new algorithmic mechanism.

### Avoid A Puncturing Assumption

The theorem statement permits fewer than `q` evaluation points, but the
printed Appendix A calculation uses the full field. One can avoid relying
on that adaptation: append an arbitrary jet at zero to our `q-1` received
blocks. A nearby polynomial then has at most `h+1` discrepancies, not `h`.
For `K=ell*(q-1)/2`, the available gap is

    1 - (K-1)/(ell*q) - (h+1)/q
      = 1/2 - (h+1/2)/q + 1/(ell*q).

Use an epsilon strictly below this gap and check the multiplicity
condition. For a fixed positive gap, sufficiently large `q` pays this
one-coordinate loss. This is an explicit transfer argument, not a claim
that the paper's appendix verbatim proves the punctured case.

## A Printed Proof Step Needs Repair

Appendix A, page 46, selects a field point where the highest derivative
coefficient is nonzero using a degree-below-field-size premise. That
premise does not follow in the high-message-degree regime.

Concrete example: `q=17`, multiplicity `8`, message degree at most `63`,
derivative count `2`, radius fraction `1/4`. The appendix's strict
interpolation inequality holds and its integer degree budget can be `88`.
For the all-zero received word, choose

    A=0, B_0=0, B_1=X^17-X.

These satisfy the degree budgets and local interpolation equations, yet
`B_1(a)=0` at every base-field point. Thus that choice-of-point argument
cannot be used unchanged. **This is not a counterexample to the dimension
theorem.** The resulting operator still has exactly the expected
Frobenius-type kernel.

### Independent Highest-Degree Repair

For prime `q` and any nonzero operator `L(f)=sum_{j=0}^s B_j f^[j]`,
with `s<q`, set

    H = max_j(deg(B_j)-j),
    R(T) = sum_{deg(B_j)-j=H} lc(B_j) * binom(T,j).

The binomial polynomials of degrees at most `s` are linearly independent
over `F_q`, so `R` is nonzero of degree at most `s`. For a coefficient
`f_t`, the coefficient of degree `t+H` in `L(f)` is `R(t)*f_t` plus
terms involving higher-index coefficients. Solve downward. Only indices
where `R(t)=0` can be free; there are at most
`s*ceil(K/q)` of them below `K`.

This argument uses polynomial coefficients, not evaluation at a regular
field point, and imposes no degree-below-`q` bound on the `B_j`. It is the
argument already implemented by `operator_matrix`; we do not claim it is
new. The added controls independently compare its bound against exact
linear algebra when every coefficient value test would be uninformative.

In particular, `(X^q-X)*f^[1]` is a zero polynomial exactly when `f^[1]`
is zero. Evaluating that residual at all points of `F_q` loses this fact.
Do not replace coefficient identities with a full table of value tests.

## Why A Short Random List Is Not A Uniqueness Certificate

A randomized list decoder can omit a nearby word on a failure outcome.
Finding a singleton in that list does not certify uniqueness in the
entire guarded ball. Our exact moment-transfer interface requires that
stronger guarantee, or a separate quantitative treatment of bad outcomes.

The new test uses `0` and `(X-1)^2` over `F_5` with length-two jets. Both
fit the same guarded received word and the same zero pin at `1`; a list
containing only `0` falsely appears unique. The affine-space check retains
the ambiguity until another informative pin arrives.

This does not rule out randomized coherent decoders. It rules out
silently replacing the exact guard certificate by an incomplete list.

## What Remains Open Here?

- Our proposed `O(((s+2)^2*q*ell+s^2*ell^2*log(q*ell))*log q)`
  coherent workspace schedule needs independent verification. A generic
  dense affine solve and blanket reversible simulation do not imply it.
- Fixing `ell` can hide an extra factor of `ell`. The source's unscripted
  big-O has absolute constants; `O_ell(q log q)` is not automatically its
  uniform `O(q*ell*log q)` guarantee.
- Our bound has target-dependent `s^2` overhead, a multiplicity threshold,
  and a logarithm-absorption condition. It does not resolve every fixed
  multiplicity, especially ordinary OPI (`ell=1`), or exact optimization.
- The original explicitly presented stream has `N=(q-1)*q^ell` entries.
  Polynomial postprocessing in `q,ell` does not remove the cost of reading
  `N`. No succinct-input reduction or practical optimization advantage
  follows from this audit.

No theorem is admitted centrally. Next research should target a concrete
gap outside this already-known decoding interface, not manufacture novelty
by renaming its ingredients.

## Verification

Eight new controls and 112 connected tests pass with RuntimeWarnings
fatal. Python compilation, site JavaScript syntax, site checks and
`python qsearch.py validate` pass. The full repository suite was not run.
All six existing Hermite producer/report pairs retain their preceding
SHA256 fingerprints. No CLI/UI wiring, central admission or commit.
