# Fixed-Input OPI: A Smaller Classical Field-Size Guarantee

2026-10-18. LOCAL APPLICATION REVIEW PENDING. No novelty, quantum algorithm,
all-field dequantization or independently accepted proof is claimed.

## Scientific Question And Outcome

Can the verified Morse norm solver avoid a factorial-genus error when
counting irreducible fibers? YES under the local trace argument below.
For degree76, modulus degree58, the sufficient field threshold falls from
756 bits to169 bits. The same fixed shifts/orientations in a declared
192-bit prime field now give a strict perfect127/127 witness after24 fibers.
The old twist bound is zero in that field. This is a genuinely enlarged
fixed-input guarantee, not an empirical seed-success estimate.

The original61-bit large source still has ZERO lower bound under both
methods. A lift to a different field does not solve or give a probability
guarantee for that original input. No field-descent claim is made.

## Problem And Mechanism

Use the explicit prime-field quadratic-coset OPI model in
[the Morse solver](PRIME_CHARACTER_MORSE_ATTACK.md): N distinct points,
public shifts, two orientations, verified nonsquare, degree<K, optional
strict exclusion of zero. The stored implementation uses points1,...,N.
Choose majority group A, minority B of size b, even n=2*floor((K-1)/2).
Require |A|<K, n>=4, n-b>=3 and p>max(n+b-1,2N).

Reuse the public unit-residue arithmetic progression and two-parameter
Morse perturbation. CHECK coprimality, simple poles, simple critical points
AND distinct critical values over the algebraic closure. The existing local
tame inertia argument gives geometric/arithmetic S_n, not merely A_n.
Then f-vg irreducible implies an actual polynomial norm, which yields the
native OPI witness; strict Cayley rotations exclude all forbidden zeros.
Nothing changes in the norm construction, source model or final verifier.

The classical baseline is the existing norm/twist solver. The prospective
quantum opening was efficient perfect intersection on these explicit lists;
an expected-polynomial classical solver removes that opening in this promised
regime. This does NOT address arbitrary oracle lists or low-rate instances.

## Exact Cycle Indicator

Let V be the (n-1)-dimensional characteristic-zero standard representation
of S_n and sigma have cycle lengths ell_1,...,ell_c. Then

    det(1-t*sigma | V) = product_i(1-t^ell_i)/(1-t).

At t=1 this equals n for an n-cycle and0 when there are at least two cycles.
The determinant/exterior-power identity therefore gives the EXACT identity

    n*1_(n-cycle)(sigma)
       = sum_(j=0)^(n-1) (-1)^j chi_j(sigma),
    chi_j(sigma) = Tr(sigma | exterior^j V).

The implementation computes chi_j from the integer polynomial
product_i(1-(-z)^ell_i)/(1+z), without a character-table library. This is used
only for small independent controls, not by the large-input solver.

No nontrivial exterior power has S_n-invariants. An elementary check avoids
assuming a full irreducible-character classification: in the basis
e_i-e_n, the subgroup S_(n-1) permutes the basis. For j>=2, any exterior
basis element contains two indices; swapping those indices fixes its support
and negates its coefficient, so every invariant coefficient is zero. For
j=1 the S_(n-1)-invariant vector is a multiple of sum_(i<n)(e_i-e_n), which
is not fixed by swapping1 with n. Only exterior^0 has an invariant line.

This argument FAILS on A_n: the top exterior power is sign and becomes
trivial. The tests explicitly reproduce that failure. Dropping the full
geometric S_n premise would silently lose the leading-term calculation.

## Trace Bound And Its Dependencies

Let U=P1 minus the geometric branch set, R=n+b branch values including
infinity. The local system attached to exterior^j V has rank C(n-1,j),
finite monodromy and weight0. It is tame because p>n implies p does not
divide n!. For j>=1 its geometric coinvariants vanish by the preceding
argument and characteristic-zero semisimplicity.

The imported cohomological facts are the compact-support trace formula,
Hc0 vanishing on this affine curve, the coinvariant description of Hc2,
the tame Euler-characteristic formula and the weight<=1 bound for Hc1.
See Fouvry-Kowalski-Michel's
[Trace functions over finite fields and applications](https://people.math.ethz.ch/~kowalski/elements.pdf),
Chapter4, Theorem4.1.4, Propositions4.1.5/4.1.6 and Theorems4.1.7/4.1.9
(PDF pages33-35; printed pages31-33), draft dated December3,2014. The notes
are an exposition with some proof TODOs, not an
independent review of this application. Finite monodromy supplies weight0;
no unspecified conductor constant is substituted for an explicit bound.
Retrieved PDF SHA256:
`40dfd0f77b43e5f79ac7304695efb3a6d2d7ed23c3f14a5dde8468d80a0a6e43`.

Thus for each j>=1, Hc0=Hc2=0 and the Swan conductors vanish. Consequently

    dim Hc1(U, exterior^j V) = (R-2)*C(n-1,j),
    |sum_(v in U(Fp)) chi_j(Frob_v)|
       <= (R-2)*C(n-1,j)*sqrt(p).

At unramified fibers Frobenius cycle type equals the degrees of the distinct
irreducible factors of f-vg. Summing the exact indicator, and keeping the
trivial j=0 term SEPARATE, proves

    n*I = #U(Fp) + sum_(j=1)^(n-1) (-1)^j sum_v chi_j(Frob_v),
    #U(Fp) >= p+1-R,
    A = (R-2)*(2^(n-1)-1),
    I/p >= max(0, (p+1-R-A*ceil(sqrt(p)))/(n*p)).

All geometric branch points are charged, even those not rational. Infinity
is already removed; there is no second branch-fiber subtraction by n!.
The ceil square root is intentionally pessimistic. No floating confidence
bound or fixed-degree hidden constant enters this count.

Keep the old twist bound too: for n4,p10007 it is actually stronger. Selecting
the maximum of TWO deterministic proved-under-premises bounds is legitimate;
it is not multiple-testing or selection by observed success.

## Uniform Field Regime And Cost

A sufficient condition for the new fiber success rate>=1/(2n) is

    p >= max(16*A^2, 4*(R+A)).

Indeed A*sqrt(p)<=p/4, A*ceil(sqrt(p))<=p/4+A, and R+A<=p/4.
Add p>=2*D_bad from the existing generic Morse-parameter bound to give
expected<=2 geometry trials, where D_bad=(2d-2)*(n+d+1), d=n+b-1.
Every actual geometry is still verified; the numeric field bound alone
cannot certify S_n or permit a non-Morse input to enter the norm stage.

The threshold has O(n+log(n+b)) bits instead of O(n log n). The coefficient
2^(n-1)-1 has only n bits. No exponential-rank object, cohomology complex,
cover or group enumeration is constructed. The algorithm uses expected
polynomially many exact finite-field interpolations/resultants,
irreducibility/factorization operations and norm rotations, in N and log p.
We import standard randomized finite-field factorization complexity; the
implementation does not give certified low-level bit-operation budgets.

For a VERIFIED fixed geometry, fresh independent uniform fibers can be
amplified. A seeded replay is NOT an IID confidence certificate. The live
control's1672-fiber cap at n76 has failure<=2^-10 under the uniform-coin
premise, not because this one seeded execution succeeded.

## Executed Evidence

- All conjugacy classes for n2 through12: exact cycle indicator, correct
  n-cycle count, character/rank bounds and zero nontrivial invariant averages.
- Independent standard-representation matrix determinant with cycle type3,2,1.
- A_n countermodel: the top exterior invariant reappears as predicted.
- Full charged quartic fibers over p29,101,1009,10007:8,40,264,2528
  irreducible fibers. Factorization-derived character sums independently
  obey the indicator and each proposed cohomological error bound. At10007,
  two finite branch values are rational; #U(Fp)=10005, not p or p+1.
- The DECLARED prime p=2^192-2^64-1 retains all127 original shifts and
  orientations from the strict seed29 input. FLINT verifies primality and
  the chosen coset multiplier. One Morse geometry,24 charged fiber tests,
  strict127/127 witness, positive trace bound, zero old twist bound.
- The original61-bit source remains field-guarded, not promoted to hard
  or unsatisfiable. The old quartic bound wins when it should.

## Attempts To Disprove It And Remaining Debt

1. A general class function need not have zero mean. The trivial character
   supplies #U(Fp); omitting it would destroy the calculation. The class
   averages and exact identity are checked independently.
2. Arithmetic/geometric monodromy mismatch could destroy the density. The
   preceding Morse proof must really give geometric S_n. The A_n test shows
   a concrete failure of the invariant premise, not just a warning string.
3. Wild ramification adds Swan terms. Characteristic restrictions remain
   mandatory; a nominal positive numeric bound cannot override geometry.
4. The trace theorem bounds Hc1, not just a smooth compact curve. Compact
   supports, missing branch values, Hc2 coinvariants, and weight0 input are
   stated explicitly. These applications still need independent review.
5. A finite seeded success cannot prove a fixed-input distributional claim.
   Full small-field factorizations calibrate each trace, but they are NOT
   the large-field algorithm or a replacement for the trace proof.
6. Large-field lifting changes OPI. No descent to the original61-bit input,
   all-field solver, low-rate solver or higher-character extension follows.
7. No quantum source, decoder or readout was discovered. The benefit is a
   stronger classical falsifier that narrows where research can credibly
   seek an advantage, not an assertion of a Shor-level discovery.

## Next Decision

Do not keep refining high-rate norm thresholds by inertia. The original
low-rate K39 model fails the majority-degree budget before this trace bound
is relevant. The next constructive question should attack that DIFFERENT
degree barrier or compare an independent source/code mechanism. Merely
testing another seed/prime or removing another constant is not enough.

```text
python theorems/prime_character_exterior_bound.py --write
python -m pytest -q tests/test_prime_character_exterior_bound.py
```
