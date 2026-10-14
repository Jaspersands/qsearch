# Next Target: Conditional Source Refresh, Not Same-Bank Coin Repetition

The algebra, entropy censuses and common-energy ledgers below are now
implemented in [the source-refresh audit](NATIVE_SOURCE_REFRESH.md). This
working note is superseded for those parts. A law-correct Gaussian refresh,
sampler, multiple producer or complete reduction is still NOT supplied.
External proof and prior-art review are required. This targets the source-average coverage debt exposed by
NATIVE_RECURSIVE_QUOTIENT_AUDIT.md. It does NOT clear coefficient ambiguity.

## Fixed-Input Transform To Investigate

For a true original quotient at g, compute records directly from ORIGINALS
using its cumulative original prefix. Do not recurse on previously flooded
records: otherwise noise inflation compounds at each level. Write these
records as y=A*h+e modg, with m originals. Draw a fresh k-by-m sign matrix
T, a fresh uniform secret mask z, and fresh IID rounded continuous Gaussian
dithers G of width sigma=alpha_target*g. Produce

    A' = T*A modg,
    y' = T*y + G - A'*z modg.

The effective secret is h-z, uniform conditional on the entire fixed parent.
It is not disclosed to the decision mechanism. The reduction keeps z only
to unmask each candidate: for a tested coefficient c, w+c*z is a candidate
multiple of h. Unknown c still requires paid coefficient enumeration.
Signs and Gaussian dithers must be generated from independent fresh coins.
Original observations are reused, not created. No sample oracle is assumed.

## Conditional Statistical Bounds

For an m-by-n matrix A over an ODD root g, let P_A be the distribution of
t*A for a fresh uniform sign row t. For IID uniform ORIGINAL label rows,
the exact expected chi-square divergence from uniform is

    E_A[chi2(P_A || U(Z_g^n))] = (g^n-1)/2^m.

Proof: equal signs have probability2^-m. Distinct sign rows differ in at
least one coefficient +/-2, a UNIT at every ternary prime-power root.
Their label sums collide with probability g^-n. Expanding collision
probability gives the stated identity. No prime-field assumption is needed.
Conditional on a fixed A, independent sign rows give a k-row label distance
at most (k/2)*sqrt(chi2). Thus a label-quality failure budget is

    P_A[k*TV(P_A,U)>eta_label]
        <= k^2*(g^n-1)/(4*eta_label^2*2^m).

For ANY fixed integer error vector e, signs satisfy E_T||T*e||^2=k||e||^2.
Pinsker and data processing for rounding reduce a continuous Gaussian
translation to a conservative rounded-Gaussian distance

    TV(actual batch, same-label batch with independent ideal dithers)
        <= 2*sqrt(k)*||e||/sigma.

This comparison averages over T, retaining its correlation with A'. It
does not assume T*e and T*A are independent. Conditional on good parent
labels and error energy, total batch distance is at most eta_label+eta_noise.
Fresh masking then supplies the uniform-secret premise for an average-case
producer. Any producer's success probability changes by at most that TV.

For true original rounded-Gaussian quotients, e_g=nearest(g*X). Uniformly
over all g>=g_min,

    ||e_g||^2/g^2 <= 2*sum_i X_i^2 + m/(2*g_min^2).

One COMMON original energy event can therefore cover all reachable roots.
If H=(eta_noise^2*alpha_target^2/(4k)-m/(2g_min^2))/2>0, require
sum X_i^2<=H. Since Var(X)=alpha_original^2/(2*pi)<alpha_original^2/6,
its failure is at most min(1,m*alpha_original^2/(6H)) by Markov.
This moment union needs no independence of original errors. Label failures
must separately cover EVERY reachable fixed root, not just a chosen path.
Bounds are conditional premises, not runtime estimates from observed values.

## Why This May Fail

- Gaussian flooding may require alpha_target>=1 or otherwise destroy useful
  distinguishability. Never reuse the old narrow-source advantage at this width.
- The m/(2*g_min^2) rounding term can make H nonpositive. Smaller roots need a
  different argument or an independently justified terminal decoder.
- A parent matrix may have bad sign-sum entropy despite full rank. Hashes and
  distinct IDs do not establish its conditional output distribution.
- Exposing T or z to a producer changes its input promise. The proposed ideal
  distribution comparison is for the declared producer input, not all metadata.
- An implementable certified Gaussian sampler and paid precision/tail/abort
  bounds are missing. Floats or an uncharged exact-Gaussian oracle do not suffice.
- Repeating refreshed calls can improve list COVERAGE on good fixed sources,
  but concatenated lists increase branching. B^D ambiguity is still unresolved.
- False prefix branches remain outside this true-source comparison. They must
  not be treated as standard full-uniform null inputs.
- This is likely related to established leftover hashing, noise flooding and
  LWE rerandomization. No novelty or full search-to-decision theorem is claimed.

## Required Next Implementation And Falsifiers

1. Exact root/entropy/energy bounds with symbolic dyadic failure budgets.
2. Complete finite original-matrix/sign-row censuses verifying chi-square
   identity, plus zero-matrix/insufficient-entropy countercontrols.
3. Actual sign/mask transform with parent receipts and complete work accounting.
4. Certified public Gaussian-dither generation, or explicit externally proved
   sampler interface with charged total variation and abort loss.
5. Width sweeps comparing the refresh budget with real decision-source promises.
6. Recompute every true quotient from originals; certify canonical path sharing.
7. Independent rational/algebra replay and source/claim tamper tests.
8. Only then analyze conditional producer amplification. Keep ambiguity and
   false-prefix pruning as separate open obligations, not silently resolved.

The BTV primary interface was rechecked in the recursive audit. A preliminary
search also located the author discussion of [Hollow LWE](https://martinralbrecht.wordpress.com/2025/03/01/rerandomising-lwe/),
which concerns a DIFFERENT rerandomization setting. Its full theorem is not
an applicability certificate for this proposal. Follow its primary-paper link
and compare existing flooding/rerandomization lemmas before asserting novelty.
