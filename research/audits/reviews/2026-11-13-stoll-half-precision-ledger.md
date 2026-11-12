# ONE-HALF: an explicit additive arithmetic precision ledger

2026-11-13. Independent arithmetic review of the UPDATED native candidate,
the paid Stoll root-interface report, and the checked geometric Smith
bridge. No API, network, Git or rerun of the extraction counterexample.
This pays the pencil/root/Stoll/extraction/label edge. It does not pay
the preceding canonical materializer or the whole saturation DAG.

## 1. Parameters and the explicit guard

Let `n=2g+1`, `g>=1`, and `D=v_2 Disc(f)`, with `f` monic integral.
The exact canonical input is `[a0,b0]`, `deg a0=e<=g`, `deg b0<e`,
and `S0=S_store>=1` bounds its coefficient poles. Its monic leading
coefficient and degree are exact data. The scalar `u in Z_2` is the
already selected finite integer and is frozen during refinement.
Set `d=n-e=deg A`, and use the following nonnegative, already paid caps:

    K_af   >= v Res(f,A),        K_disc >= v Disc(A),
    K_aw   >= v Res(W,A),        K_wr   >= v Res(W,R),
    K_lab  >= v Res(W,f).

The first two are visibly tested on the pencil. The middle two are
success-event bounds used to set the matrix/inverse clocks; they are
not assumed to have been measured on an unknown half. The last is
visibly tested on the extracted output (`2gns` in the candidate).

Here is one entirely numerical sufficient ledger. All quantities are
integers; use ceilings where indicated.

    S_A   = (n+3) S0
    S_hat = S_A + D + 1
    C_pen = (2n+6) S0
    K_src = 1 + max((2d-1) S_A + K_disc, n S_A + K_af)

    V_src  = n (K_af+n S_A+S_A+1)
    C_root = 20(n+1)^2 (D+V_src+1)

    S_M = (n+2) S_hat + 2 K_wr
    q   = n+d+1
    D_B = 2g+K_aw+K_wr+ceil(K_af/2)
          +[g(5g+12)+d+g] S_hat
    K_B = q S_M + D_B
    C_M = (2n+1) S_hat

    K_inv = 2g+K_aw+2K_wr+g(5g+12) S_hat
    T     = ceil(3 S_hat/2)
    H_X   = T+(g+1) S_hat
    C_X   = T+2(g+1) S_hat
    K_X   = g H_X+K_inv

    K_L   = n S0+K_lab
    V_lab = n (K_lab+n S0+S0+1)
    C_lab = 20(n+1)^2 (D+V_lab+1)
    C_out = K_L+C_lab+2

    C_half = C_pen+K_src+C_root+C_M+2K_B+C_X+2K_X+C_out.   (1)

Given `P_out>=1`, canonical input coefficients and fixed local-field
data to `P_out+C_half` absolute binary digits suffice for `P_out` digits
of the accepted half AND its exact squareclass label. All underlying
exact inputs, scalar choices, root balls and numerical solve choices are
retained. Formula (1) is polynomial in the displayed native caps and
independent of `P_out`. There is no unspecified multiplier `c`.

The following proof also gives smaller stage-by-stage requests. The
coarse additions in (1) intentionally ignore precision gains from
multiplication by known powers of 2.

## 2. Monic division and the pencil

Use this elementary coefficient lemma. Suppose `h` is monic of degree
`k`, its coefficient poles are at most `S`, and `Q` has degree at most
`t` and coefficient poles at most `H`. Put
`L=max(t-k+1,0)`. Monic long division gives quotient/remainder poles at
most `H+LS`. If both inputs change by coefficients divisible by `2^P`,
while retaining their degree/monicity and pole bounds, their quotient
and remainder change by coefficients divisible by

    2^(P-H-2LS).                                      (2)

For (2), write `Q=q h+r` and the perturbed division similarly. Divide
`delta Q-q_tilde delta h` by `h`; its poles/errors cost at most
`H+LS` before a further `LS` reduction. This proves a uniform bound
for BOTH numerator and divisor variation. Division by the constant
monic polynomial 1 has no loss and satisfies the same coarse bound.

Now `f-b0^2` has degree `n` and poles at most `2S0`. There are at most
`n+1` division steps by `a0`, so

    c=(f-b0^2)/a0

has poles at most `S_A=(n+3)S0`. Consequently

    A=c-2u b0-u^2 a0,       B=-b0-u a0

have poles at most `S_A` and `S0`, respectively; `A` is monic of
degree `d`, and `deg B<=g`. Squaring `b0` loses at most `S0` input
digits. Applying (2) with `H=2S0`, `S=S0`, `L<=n+1` loses at most
another `(2n+4)S0`. Thus `C_pen=(2n+6)S0` is sufficient.

In particular, pencil coefficient/content scaling must use at least
`S_A`, not the unchanged stored cap `S0`. The existing pencil tail
proof remains applicable with this corrected numerical charge.

For visible source tests, use the integral matrices
`2^S_A Sylv(A,A')`, of size `2d-1`, and `2^S_A mult_f(A)`, of size
`n`. Their determinants have valuations at most
`(2d-1)S_A+K_disc` and `nS_A+K_af`. A determinant of an integral matrix
is 1-Lipschitz in its entries. Therefore `K_src` input digits more
than suffice for both tests. A determinant not visible within its
specified cap causes ABORT, never a claim that it is exactly zero.

## 3. Root coefficient bounds and Stoll matrix construction

The root is the selected ACTUAL root of `epsilon A mod f`, with
`epsilon=(-1)^d`; its ball is frozen. The proved local-field backend
supplies `C_root` above from the visible `K_af` and pole cap `S_A`.

There is also an unconditional native coefficient bound for this root,
which avoids using an unknown good half to justify matrix arithmetic.
Every component of `A(theta)` has normalized valuation at least
`-S_A`, so every component of `s` has valuation at least `-S_A/2`.
The total integral-order index is at most `D/2`. Hence the polynomial
representative `deg s<n` has coefficient poles at most

    ceil(S_A/2)+ceil(D/2) <= S_hat.                    (3)

This uses `2^I O_L subset Z_2[theta]`, not interpolation at selected
roots. It applies to every choice of the square root.

Construct the Stoll coefficient matrix for

    V-sW mod f,             V-BU mod A,
    deg U<d/2, deg V<=g+floor(d/2), deg W<=g,

and append `W_g=1`. Its size is `q=n+d+1`. Here `deg U<=g`,
`deg V<=2g=n-1`, and `deg B<=g`. Remainder modulo integral monic `f`
loses no coefficient digits. For reduction modulo `A`, every numerator
has degree at most `n-1`, so (2) with `L<=n`, `H=S_hat` proves that
input accuracy `P+C_M` gives matrix-entry accuracy `P`.

All entries have poles at most `S_M` as displayed in Section 1. Indeed
`(n+1)S_hat` already covers the nonintegral remainders, while (3)
covers the root block; the larger reviewed `S_M` is retained so its
published determinant/Smith formulas apply unchanged with `S=S_hat`.
Set `B'=2^S_M B_g`. It is integral on every sample satisfying the
already checked input caps, not just on the success event.

## 4. Normalized solve and the mandatory early pole check

The geometric bridge proves `v det B'<=K_B` on the good event. In the
algorithm this is a visible test. On acceptance `B'` is genuinely
invertible, and the exact normalized solution is

    (U,V,W)=B'^(-1) (2^S_M e_last).

For any integral matrix with determinant valuation `delta<=K`, its
adjugate is integral. Its inverse has poles at most `K`, and perturbing
its entries and an integral right-hand side by `2^L` perturbs the
solution by at worst `2^(L-2K)`, provided `L>K`. This follows either
from the inverse difference identity or directly from Cramer's rule.
Thus matrix-entry precision `P+2K_B` suffices for solution precision
`P`, including off-event accepted matrices.

No arbitrary tiny Gaussian pivot is permitted. One may compute the
integral adjugate/determinants by division-free polynomial-time matrix
arithmetic and divide only by the certified determinant. Equivalently,
complete valuation pivoting on the integral matrix has integral
elimination multipliers and total pivot valuation `delta`; freeze those
certified pivots for refinement. A previously chosen unrelated leading
minor is not covered by this bound.

Immediately after this solve, require that `W` has coefficient poles
at most `S0`; otherwise ABORT. Such a pole test is exact from any
absolute precision at least 1, since all relevant negative digits are
then known. The actual source identity is

    V^2-fU^2=epsilon A W^2.

The odd degree and monicity of `f` imply
`v_G(V^2-fU^2)=2 min(v_G(U),v_G(V))`: primitive reduction cannot make
`f mod 2` a square in F2(x). Hence, after the `W` cap check,
`U,V` have coefficient poles at most `T=ceil(3S_hat/2)`. These caps
can also be visibly checked. Thus subsequent extraction arithmetic
does not assume invisible good-output coordinates.

## 5. Selected inverse extraction with an independent determinant guard

Form the `g`-by-`g` matrix and vector

    C_U = multiplication by U on Q_2[x]/W,
    b_V = -rem_W V.

This requires no discovery of `deg U`: use the fixed monomial quotient
basis. Its determinant is exactly `Res(W,U)`, including when the leading
coefficient of `U` vanishes. In particular it is the REQUIRED separate
acceptance test; invertibility of `B_g` does not imply it.

Numerators have degree at most `2g`, so (2) gives entry/RHS poles at
most `H_X=T+(g+1)S_hat` and construction loss at most
`C_X=T+2(g+1)S_hat`. Put

    C'=2^H_X C_U,           b'=2^H_X b_V.

Both are integral. The reviewed Bezout identity gives the success cap
`K_inv` in Section 1, and therefore `v det C'<=K_X=gH_X+K_inv`.
Require this determinant to be visibly nonzero within that cap.
The exact native example with `det B_g=1` and `Res(U,W)=0` is rejected.
No polynomial involving the unknown `R` is used as an algorithmic
certificate or extraction formula.

The same integral adjugate bound now shows that `P+2K_X` digits in
`C',b'` suffice for `P` digits of

    R=C'^(-1)b' = -V/U mod W.

Consequently `P+C_X+2K_X` digits of `U,V,W` suffice. This includes
divisor variation in `W`, rather than treating it as an exact supplied
modulus. Root balls, matrix choices and the scalar pencil are retained;
refinement follows this same exact rational expression.

## 6. Stored output, labels and backward composition

Require the extracted `R` pole cap `S0`. For the output branch test use
`2^S0 mult_f(W)`, an integral `n`-by-`n` matrix. Its determinant has
valuation at most `K_L=nS0+K_lab` on the good event. Request at least
`K_L+1` coefficient digits and require visible nonzeroness within this
cap. This proves that `(-1)^g W mod f` is a valid element of `L*`.
Its component valuations are then bounded by the native norm formula;
the proved field backend needs at most `C_lab+1` input digits to compute
its exact squareclass label. No approximate gcd is taken.

The following backward requests exhibit (1):

    P1 = P_out+C_out                    # W,R and output/label tests
    P2 = P1+C_X+2K_X                    # U,V,W
    P3 = P2+C_M+2K_B                    # A,B,s
    P4 = P3+C_root                      # A and fixed field data
    P_input = P4+C_pen+K_src = P_out+C_half.

All source visibility tests fit the extra `K_src` margin. Every internal
division is monic, a unit inversion, a frozen Hensel correction already
paid by `C_root`, or an adjugate solve with one separately certified
determinant. Their precision guards are independent of the requested
precision. Matrix sizes, polynomial degrees and counts of operations
are polynomial in `g`; the bit length of the frozen grid integer `u`
is charged separately by its already proved polynomial grid bound.

These backward equations do not require re-evaluating old DAG nodes.
With a separately proved node bound `T0`, a common fixed edge guard
`C_max>=C_half`, and source precision `P_star=P_cert+T0 C_max`, a node
at depth `j` may be computed ONCE at precision `P_star-j C_max`.
Its parents provide at least the required input precision. Keep the
same exact identities and selected root/solve certificates. This
ledger presents no obstruction to that descending-precision schedule;
the bound on the number of nodes is outside this review.

On acceptance the source identities prove an actual half with the
recorded orientation. On rejection this fixed computation returns
ABORT without inferring a rank drop or a nonexistent half. The
probability that all tests accept remains the separate paid geometric
and pencil assertion. This arithmetic ledger does not replace it.
