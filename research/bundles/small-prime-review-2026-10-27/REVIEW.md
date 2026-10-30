# Independent Small-Prime Review

## Verdict

**ACCEPT the scoped new-seed, degree-eight geometry, native matrix, and
fixed-p parameter transfer. No fatal theorem error or required mathematical
fix was found.** This includes the late `dimension_L_G_minus_K` addition and
the clarification that the extra fiber does not split in the full Kummer
extension.

The constructed object really is a complete genus-41 AG code over F_1019,
with `(k,m,dim V^2,dim V^3)=(43,176,126,176)`. The basis-completeness and
normalization arguments below are essential; this verdict is not just a
replay of the parent's ranks. The finite native problem is classically
solved. Full cube rank is not hardness evidence.

Higher-degree curves, matrices, prime-divisor sampling, and quantum circuits
were NOT generated. The higher-level verdict is a transfer of the stated
mathematical bounds and arithmetic contracts, not certification of an
implemented source constructor. No speedup, novelty, uniform-Picard law,
or general classical lower bound is certified.

## Reviewed State

Read `small_prime.py`, `seed_search.py`, the subsequently supplied
`RESULT.md` and `avoidance.py`, and the six requested prior proof documents.
Also checked the fixed-field assumptions in the prior `SOURCE.md`,
`ARITHMETIC.md`, and `REVIEW_RESOLUTION.md`. Source SHA-256 digests are in
[evidence.json](/Users/jaspersands/Developer/qsearch-research-work/small-prime-review-2026-10-27/evidence.json).
The final control run includes the `L(I-E)=0` addition; its
`small_prime.py` digest is
`8ffe074188c704579ec73ff6c2587460dd0b42fad56fcf76126236838eea28a1`.

All authored files and generated evidence are confined to this review
directory. No parent/original source, Git, UI, registry, or migration state
was changed. The parent test suite was not run. Later parent test counts
and main-registry results are not independent evidence in this review.

## 1. Seed And Tower

Trial division verifies that 1019 is prime. The thirteen branches are
distinct, and all 143 prescribed differences are nonzero squares, checked
by exhaustive square-table lookup rather than the parent's exponentiation
routine. Scanning this fixed field confirms that the eleven listed x values
are exactly the x values with all thirteen differences nonzero squares for
this particular branch set. This is not a smallest-prime result.

Let F=F_1019(x), f=product(x-a), and K=F(y), y^2=f. The monic squarefree
degree-13 equation has a smooth projective model of genus 6 and one rational
infinity O. Finite-branch valuations make the thirteen square classes x-a
independent in F*/F*2. The kernel of F*/F*2 -> K*/K*2 is exactly the class
of f: if (u+vy)^2 lies in F, then 2uv=0. Consequently their rank over K is
exactly 12. No consecutiveness of the branch values enters this proof.

Each divisor is `div_K(x-a)=2P_a-2O`. In odd residue characteristic, even
valuation gives an unramified quadratic extension; it does NOT by itself
give splitting. Splitting at the marked finite places follows from their
checked nonzero-square residues. At infinity, t=y/x^7 has valuation 1 and

    (x-a)t^2 = (x-a)f(x)/x^14 -> 1.

Hensel lifting makes this unit a square in the completion. Thus all thirteen
quadratic extensions split at O, as well as at the 22 finite marked points.
A rational split place rules out enlargement of the constant field.

The resulting S-split unramified elementary extension has rank 12. Hence
`d_2 Cl_S >= 12`. The S-unit group has free rank 22, and F_1019* contributes
one further 2-rank, giving `d_2 O_S* = 23`. The strict squared margin is

    (12-2)^2 - 4*(23+1) = 4.

This satisfies [Schoof, Theorem 2.3, printed page 11](https://reneschoof.github.io/CurvesF2.pdf).
The theorem is stated for general finite fields, not just the F_2 example
in the paper's title. Its application here is valid.

An infinite pro-2 extension supplies intermediate dyadic degrees. This is
an existence statement; it neither implements those levels nor forces an
arbitrary chosen chain to contain a preselected intermediate cover.

`seed_search.py` is a bounded discovery heuristic. Its beam truncation and
deduplication do not prove nonexistence on failure. Its `UNKNOWN` and
no-smallest-prime qualifications are appropriate. I did not rerun the beam
search or independently certify its reported discovery-operation count.

## 2. Degree Eight And Residue Fields

The three pair masks `{0,1}`, `{0,2}`, `{0,3}` are independent modulo the
full thirteen-element mask. Thus adjoining their roots gives degree 8 over
K, and degree 16 over F. It is a subextension of the above unramified
geometric extension. Riemann-Hurwitz gives

    2g_X-2 = 8*(2*6-2) = 80, so g_X=41.

There are eight rational points above O, not sixteen: infinity is already
ramified with index 2 over the x-line. Their independent residues w_i/x
are the eight sign triples. The eight even-character sign vectors have
rank 8 over F_1019 in the exact control.

Each selected finite x has sixteen distinct rational points on this
degree-eight cover, giving the 176 distinct evaluation points D. These
points are nonsingular in the displayed affine equations because all four
radicals are nonzero. Their residue fields really are F_1019.

The first additional split x is 6. The five points, in `(x,w1,w2,w3,y)`
coordinates and the parent's specified ordering, are

    0:  (6,  49, 997, 954, 147)
    3:  (6,  49, 997,  65, 872)
    5:  (6,  49,  22, 954, 872)
    9:  (6, 970, 997, 954, 872)
    14: (6, 970,  22,  65, 147).

They are distinct and disjoint from D. The nonsquare branch-difference
indices at x=6 are `0,1,2,3,4,5,7,10,11,12`. In particular the FIRST FOUR
differences are all nonsquares; their required pair products are squares.
There is no need for thirteen individual roots in F_1019 at these points.
The degree-eight rational points do not become rational split points of
the full elementary cover. The updated parent correctly distinguishes this.

## 3. Complete Basis And Evaluator

Over F, the sixteen characters are the eight even subsets of `{0,1,2,3}`
and their full complements. Write z_T^2=product_(i in T)(x-a_i), choosing
the characters compatibly with w_i and y. Their weight multiplicities are

    |T|:          0  2  4  9  11  13
    multiplicity: 1  6  1  1   6   1.

Here is a completeness proof on the normalization. The full order-16
Galois group over F preserves the finite locus and the divisor I above
infinity. Since 16 is invertible, character projection preserves L(nI).
Every projected function is h_T(x)z_T with h_T in F. At a branch in T,
z_T has valuation 1 and x-a_i valuation 2, so a denominator factor cannot
be cancelled. At other finite places z_T has valuation zero unless it is
one of these simple branch zeros. Thus finite regularity forces h_T to
be a polynomial. At every infinity point z_T has pole order |T| and x
pole order 2, so a polynomial of degree j has exact pole order 2j+|T|.
Distinct characters cannot hide higher poles from all character projections.

Therefore `x^j z_T`, `2j+|T|<=n`, is the complete L(nI) basis. At n=11
the count is `6 + 6*5 + 1*4 + 1*2 + 6*1 = 48`, also agreeing with
Riemann-Roch: `deg(11I)-g+1=88-41+1=48`.

For a low mask T, let r be the number of selected indices in `{1,2,3}`
and epsilon indicate whether 0 is selected. Even parity makes
`h=(r-epsilon)/2` a nonnegative integer, and the correct function is

    z_T = product_(selected i) w_i / (x-a_0)^h.

The apparently singular quotient is regular on the normalization: its
valuation at a_0 is `r-2h=epsilon`, and the other branch valuations are
exactly those of z_T. For the complement, `z_(full\T)=y/z_T`, again with
nonnegative finite valuations. At all D and E evaluation points the
denominators are nonzero. The parent's exponent and complementary sign
choice are correct; replacing the latter by unrelated square roots would
not be justified by square identities alone.

The independent evaluator instead lifts thirteen compatible roots to
F_1019(theta), theta^2=2, multiplies them, and verifies descent of all
sixteen characters to F_1019. This checks the case of nonsquare individual
factors at x=6 without borrowing the parent's denominator formula.

## 4. Canonical Class And Exact Native Ranks

On the base curve `div(dx/y)=10O`: finite branch zeros cancel in dx/y,
and its infinity order is 10. The cover is unramified, so its pullback has
divisor 10I. Consequently `K_X=10I` is a valid canonical representative.

For `G=11I-E`, degree 83 is `2g+1`, and negative coefficients at E are
allowed. Vanishing at these five points cuts L(11I) down to L(G).
Riemann-Roch independently forces dimension 43. The complete L(I) contains
only constants; vanishing at E forces zero. Thus

    ell(G-K_X) = ell(I-E) = 0.

There is no canonical-divisor error in the late parent addition. In
particular G is not linearly equivalent to K_X plus an effective degree-3
divisor.

I reconstructed L(tG) for t=1,2,3 by imposing t local vanishing jets at
each point of E on the COMPLETE L(11tI). Here x-6 is a uniformizer. Jets
were computed from z_T^2=product(x-a_i), not by multiplying parent rows.
Plain-Python modular elimination, independent of FLINT, gives:

| t | dim L(11tI) | Jet rank | dim L(tG) | Evaluation rank on D |
|---|---:|---:|---:|---:|
| 1 | 48 | 5 | 43 | 43 |
| 2 | 136 | 10 | 126 | 126 |
| 3 | 224 | 15 | 209 | 176 |

Separately forming Schur products of the independently constructed matrix
gives square rank 126 and cube rank 176, with exactly the same evaluated
spaces as the jet construction. Its rowspace also equals the parent's
43-by-176 matrix rowspace, in the identical point ordering.

Normal generation at degree at least 2g+1 identifies these Schur powers
with the complete evaluated RR spaces; effectiveness is not a hypothesis.
See [Couvreur, Marquez-Corbella and Pellikaan, Theorem 5 and Corollary 6](https://arxiv.org/html/1401.6025v3#S2.SS2).
Duality then gives
`ell(K_X-3G+D)=0`. Since D is linearly equivalent to 22I, this residual
class is `-I+3E`, of degree 7. The full cube really removes the SAME-code
annihilator, but not auxiliary-code or general classical attacks.

No pullback extrapolation is valid: on a further degree-r cover, the
pullback of G has degree 83r, whereas the prescribed new degree is 80r+3.
A class without sections can also acquire sections after pullback.

## 5. Fixed-Prime Bounds

For an actual tower curve of dyadic degree e>=8 and a divisor G disjoint
from D with degree d=2g+1, the dimensions are

    g=5e+1, d=10e+3, k=5e+3, m=22e, w=15e+6.

Here m>2d and normal generation applies. Every nonzero word of V has at
most d zeros. Shortening L(2G) at z of these zeros has dimension w-z,
because `2d-z>=d>2g-2`. This directly gives the stated decoder estimate

    E_dec <= (p^k-1)*p^w/(p-1)^m < p^9*(2/p^2)^e.

For p=1019, Bernoulli gives `(1-1/p)^22 >= 1-22/p > 1/2`.
The coarse e=8 bound is 256/p^7<1 and its per-integer-step ratio is
2/p^2<1. These are proofs for all e in range, not an extrapolation from
the finitely tested degrees.

The corrected USD reduction must count both branch acceptance and final
verified validity. With `alpha=(p^k-1)/(p-1)^(m-d)`, the raw success lower
bound is `(1-E_dec)^2/(1+alpha)`, as implemented. The unsquared expression
belongs to the accepted-branch analysis and is not a raw-trial guarantee.
This uses the ideal unambiguous-decoder premises in the supplied resolution;
no circuit or noise-tolerance claim was independently executed here.

For the class bound, `a=deg(K-3G+D)=2e-9` lies in `[0,g-1]` and
`g-a-1=3e+9`. [Cascudo-Cramer-Xing, Proposition 3.4](https://arxiv.org/html/1207.2936#S3)
supplies `A_a/h <= g/[p^(3e+9)(sqrt(p)-1)^2]`. Multiplication by 3
contributes at most `#J[3]<=9^g` preimages per class; it need not be onto.
Taking `L=floor(sqrt(p))-1=30` weakens this correctly to B_e.

For uniform degree-d CLOSED primes, each degree-d class contains at most
`M_d=(p^(g+2)-1)/(p-1)` primes, since this counts all its effective
representatives. With `N_d>=p^d/(2d)` and
`h< (floor(sqrt(p))+2)^(2g)=33^(2g)`, it follows that

    Pr(bad prime) <= B_e * 2dp/(p-1) * (33^2/p)^g.

This is a maximum-class-mass argument, not a uniform-Picard assumption.
The prime-count condition follows independently from the point-count
identity `d N_d = #X(F_(p^d)) - sum_(r|d,r<d) r N_r` and Weil bounds:
the total error is at most `(g+1)(d+6)p^(d/2)`. Thus
`p^d>=4(g+1)^2(d+6)^2` suffices. It holds at e=8; its right-hand side
grows by a factor <16 per integer e-step, while its left side grows by p^10.

The exact ratio of consecutive displayed bad-prime bounds is

    (9^5/p^3)*(g+5)/g*(d+10)/d*(33^2/p)^5
      < 4*9^5/p^3*(33^2/p)^5
      = 0.000311184864329546558116318... < 1.

At e=8 the independent exact arithmetic gives

    E_dec upper       = 1.04190511223771003887767e-21
    alpha upper       = 4.27510275947761065445735e-151
    bad-prime upper   = 8.24654782279747671104125e-59.

The parent's figures are consistent approximations. All bounds were also
compared exactly with `parameter_bounds` for dyadic e=8 through 1024.
Those comparisons certify arithmetic, NOT generated higher curves.

The actual prime sampler still needs the component-count acceptance
correction in [Bruin, Algorithm 3.2](https://arxiv.org/html/1003.2563).
For the stated degree-(2g+2) embedding and i=2, the section dimension is
3g+5, the prime-vanishing dimension g+4, and the component cap 2. This
gives acceptance at least `(1-p^(-g-4))/(4d)` under the prime-count bound.
The characteristic change introduces no exception to these formulas.

## 6. Costs And Classical Comparison

The prior construction contract uses odd characteristic, rational split
places, normalized local units, bounded original-field representations,
and exact 2-primary certificates. These conditions survive the new seed.
In particular its normalization argument explicitly allows characteristic
smaller than the presentation degree; growing genus past 1019 is not by
itself a counterexample. Choosing between consecutive pole orders retains
a separating coordinate. This is a check of transfer, not a fresh audit
or implementation of every arithmetic dependency.

The fixed-p conclusion is not polynomial time in log p uniformly over p.
The local quantum pair construction and fixed-characteristic order routine
have polynomial-p costs, with unspecified practical constants. Normalization,
RR construction, exact order, sampling corrections, compilation precision,
inverse decoding, failed trials, and final verification remain charged.
The dense input has Theta(e^2) field entries, not poly(log e) size.

`avoidance.py` correctly reduces disjoint column bases to affine avoidance.
Distance `m-d=12e-3 > k` ensures that deleting any k columns leaves full
row rank, so two disjoint bases exist. Finalizing a row at its last nonzero
variable forbids at most one value; including zero excludes at most k+1
values. For `p>=k+2` a legal value exists. The finite search interval in
the code is long enough by the same pigeonhole argument, without scanning
all p elements. A dead end outside the guarantee means UNKNOWN, not UNSAT.

At p=1019 this covers integer e<=202, hence dyadic e<=128. The analogous
old-prime cutoff is e<=19999, hence dyadic e<=16384. This changes a
sufficient low-dimensional range, not general solvability.

Systematic rejection has exact success
`(1-1/p)^k*(1+R_s)`, with `|R_s|<=alpha`, for EVERY syndrome. At e=8 its
certified success is approximately 0.958659856305859. Even the weaker
affine union bound is `1-176/1019 = 843/1019 > 0.827`.
The binary rejection-trial exponent per e changes from about 0.000072133
to 0.00708245, a factor of 98.186. This comparison concerns that sampler,
not a lower bound on all classical algorithms. The forecast e=1024
systematic success is still approximately 0.00653916, and its dense
matrix would have 115,410,944 entries. Neither matrix generation nor
runtime at that degree has been established by these numbers.

## 7. Independent Evidence And Limits

Reproduce from the isolated review directory:

```sh
/opt/anaconda3/bin/python -B /Users/jaspersands/Developer/qsearch-research-work/small-prime-review-2026-10-27/audit.py
```

[audit.py](/Users/jaspersands/Developer/qsearch-research-work/small-prime-review-2026-10-27/audit.py)
uses Python 3.13.5; the parent-comparison phase uses installed python-flint
0.9.0. The independent field arithmetic, jet construction, nullspaces and
row reduction use this review's code, not parent algebra helpers.

The final run passed: 319,488 exact character-product identities across
all 78 unramified split fibers; 19,968 independent radical-evaluator
comparisons; all 176 coordinate-deletion rank checks; the three jet/RR
constructions; and the independent Schur-space comparisons. Omitting the
denominator fails the mask-6 check at 1,232 of the 1,248 tested points.
The receipt retains explicit matrices, RR bases, constraints, product-basis
indices, the five E points, root certificates, and source hashes.

The parent avoidance routine produced 46 witnesses checked directly
against the ORIGINAL parent matrix and targets. Separately, this review's
all-free-coordinate greedy routine produced 46 checked witnesses for the
independently based matrix. These latter targets refer to that basis, not
an unrecorded identification with the parent's syndromes. Exhaustive
controls also passed for all 480 invertible 2-by-2 matrices over F_5 and
all 25 forbidden targets each: 12,000 cases. The F_3 dead-end control
correctly remained UNKNOWN despite an existing witness.

Evidence decimals can round extremely near-unit bounds to 1; strict
inequalities are checked with exact Fractions, and exact e=8 values are
retained. Source hashes were unchanged between start and end of the final
run. No native object beyond degree 8 was constructed.

**Required fixes: none in the scoped claims.** Preserve the distinctions
between the degree-eight and full Kummer fibers, normalized functions and
raw affine quotients, same-code escape and classical hardness, and
conditional forecasts and implemented higher-level inputs. Those are
substantive restrictions, not optional wording.
