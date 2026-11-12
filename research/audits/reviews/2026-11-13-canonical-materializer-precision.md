# An additive precision ledger for one canonical materializer call

2026-11-13. Focused proof after current STATE,
`LOCAL_KUMMER_NATIVE_END_TO_END.md`, the independently proved ideal-saturation
bound, and `2026-11-13-reduced-rr-unit-basis.md`. No Git, network, API,
implementation or numerical sweep. Commands used `/opt/anaconda3/bin/python`.
Parent owns shared notes.

## Exact conclusion and input contract

Let d=2g+1. The input consists of actual graph blocks [a_i,b_i], with
monic a_i of known degree `1<=e_i<=g`, `deg b_i<e_i`, and
`a_i | f-b_i^2`. Signed blocks are first changed by b_i -> -b_i as needed.
Their total degree satisfies `g<=m=sum e_i<=6g`; there are k<=m blocks.
Their coefficient valuations are at least -S_in. The native f is an exact
monic squarefree integer polynomial, with D=v2(disc f).

The true canonical output is assumed to have degree g and coefficient
valuations at least -S_out. This is the coordinate-good success premise;
the unknown coefficients themselves are NOT algorithmic inputs.
The given caps S_in,S_out are nonnegative integers.

Use ABSOLUTE precision: an approximation to c at precision P means its
error has valuation at least P, even when c has a pole. For any P_out>=1,
put

    L=max(S_in,S_out),
    H=D+2L d(d-1)+2,
    C_mat(m)=dL+2m^2 H+2.

Then one canonical materializer call can request only

    P_in=P_out+C_mat(m)                                (1)

absolute digits of each input coefficient. In the native m<=6g interface,
the single bound

    C_mat(g,D,S_in,S_out)=dL+72g^2 H+2                  (2)

suffices. It is a fixed polynomial independent of the input DAG's ancestry.
The numerical algorithm uses finitely visible pivots and defines a rational
arithmetic chart at the ACTUAL input. The same chart can be refined later.

The result is a materializer ledger, not a ledger for the sampler, local
field backend, scalar pencil, Stoll half, or the entire outer DAG.

## 1. Integral scaling and matrix formation cost no digits

Use

    X=2^(2L)x,       Y=2^(dL)y,
    f_L(X)=2^(2dL)f(2^(-2L)X),
    A_i(X)=2^(2e_iL)a_i(2^(-2L)X),
    B_i(X)=2^(dL)b_i(2^(-2L)X).

All these polynomials are integral. Every multiplication applied to an input
coefficient is by a nonnegative power of 2; for B_i the exponent d-2j is
at least three. Monic leading coefficients are structural exact ones.
Thus scaling loses no absolute input precision. The exact discriminant
exponent of f_L is `D_L=D+2L d(d-1)`, and H=D_L+2 is the proved safe
per-stage Smith-exponent bound.

Form `A=product A_i`, and let `T=O[X,Y]/(Y^2-f_L,A)`, O=Z2, with its
standard rank-2m monomial lattice. The companion matrix X_T, the matrix

    Y_T = [[0,f_L(X_T)],[I,0]],

and the block operators A_i(X_T), Y_T+B_i(X_T) are all integral.
Polynomial multiplication, evaluation, and reduction by a MONIC integral
polynomial are 1-Lipschitz in absolute coefficient precision. Each is a
finite sequence of additions and multiplications of integral quantities;
monic division introduces no nonunit division. Consequently their errors
remain in `2^P O` when the input errors do.

The number of terms costs no extra digits: a nonarchimedean sum preserves
the minimum error valuation. Polynomially many such operations affect time,
not this precision bound.

## 2. Finite pivot selection for a known-rank matrix

The following concrete algorithm is used at each product stage. Let C be
an integral u-by-v matrix of KNOWN rank r, and assume every nonzero Smith
exponent is at most H. Here u=2m, v<=4m and r<=2m. It is enough to know C
modulo 2^Q with `Q>rH`; our schedule always provides two extra guard digits.

Perform full-pivot DVR elimination. In the current remaining block choose
the lexicographically first entry of minimum VISIBLE valuation. A residue
zero modulo 2^Q is treated as valuation >=Q, not as an exact zero. If the
selected entry p has valuation a, all entries of the block are divisible
by 2^a. After row/column swaps, write the block as

    [[p,b],[c,E]].

Its remaining Schur block is `E-c b/p`. Compute the quotient as

    c b/p = 2^a (c/2^a)(b/2^a)/(p/2^a).               (3)

The parenthesized quantities are integral, the denominator is a unit, and
they are known modulo `2^(Q-a)`. Multiplication by 2^a restores absolute
precision Q. Hence this Schur update costs ZERO absolute digits.

Equivalently, the Schur map is 1-Lipschitz on this fixed valuation chart:
perturbing p,b,c,E by 2^Q changes c b/p by 2^Q, because b,c both have
valuation at least a. This observation is needed; separately carrying
low-precision row multipliers without restoring their powers of 2 would
obscure the precision bound.

The row and column clearings are unimodular over O. Greedy minimum pivots
have nondecreasing valuations, so their first r values are the nonzero
Smith exponents, all <=H. Therefore each required pivot is visible. Stop
after EXACTLY r pivots, using the mathematical rank theorem. Do not infer
an exact rank from a small or vanishing numerical remainder.

Record the selected ORIGINAL row and column sets I,J. Their r-by-r minor
M=C_(I,J) satisfies

    delta=v2(det M)=sum_(j=1)^r v2(p_j) <= rH.          (4)

It is a minimum-valuation maximal minor: the unimodular elimination
identifies the determinantal ideal with the product of its r pivots, and
the selected original minor has exactly that product as determinant, up
to sign. This inspects only polynomially many entries during r eliminations;
there is NO enumeration of maximal minors.

All selected pivot valuations and ties are decided from visible digits.
Once recorded, I,J are retained on refinement. The determinant remains
nonzero with valuation delta, certified by its finite digits. Higher
precision does not redefine the actual chart or its represented point.

## 3. Normalizing the saturated basis loses at most delta digits

For the indices just selected, define the exact rational chart

    V=C_J adj(M)/det M.                               (5)

Every entry is integral. Its numerator is a maximal minor of C (or an
integer combination giving the same replaced-row minor), and no such
minor has valuation below delta. Also `V_I=I_r` exactly. It follows that

    V O^r = span_K(C) intersect O^u.                   (6)

Indeed an integral vector in the K-span has coordinate vector given by
its I-rows, which are integral. Thus (5) is the required saturated lattice
basis, not just a generating set of the raw image.

Determinants, adjugates and matrix products are integral polynomial maps
in the entries, hence preserve absolute precision Q. Write

    Z=C_J adj(M),       Delta=det M,       Z=Delta V.

Since V is integral, knowing Z,Delta modulo 2^Q gives V modulo
`2^(Q-delta)`. Divide both numerator and denominator by the VISIBLE power
2^delta, then invert the resulting unit. The normalization loses delta
digits, not two delta digits. A useful direct error identity is

    V_tilde-V = ((Z_tilde-Z)-V(Delta_tilde-Delta))
                         /Delta_tilde.                (7)

Its numerator has valuation at least Q and its denominator has valuation
delta. Approximate inputs need not themselves have exact rank r; (7)
compares their rational-chart evaluation with the actual promised matrix.
Enforce the identity pivot rows structurally when storing the result.

This gives an explicit finite BIT evaluation too. Lift matrix entries to
integers modulo 2^Q. Compute the one selected determinant and its polynomially
many cofactors by exact integer determinant algorithms, and reduce modulo
2^Q. Fraction-free integer elimination is permissible here: its exact
integer divisions compute a polynomial value on a finite lift, not an
uncertified p-adic inversion. Hadamard bounds give intermediate bit lengths
O(r(Q+log r)); polynomially many such computations are polynomial BIT.
After the power-of-two division, unit inversion modulo `2^(Q-delta)` is
ordinary finite integer arithmetic.

## 4. The product-stage losses add

Start with V_0=I_(2m). At stage i form

    C_i=[ A_i(X_T)V_(i-1) | (Y_T+B_i(X_T))V_(i-1) ].

Its exact rank is `r_i=2m-sum_(j<=i)e_j`, including coincident blocks and
repeated support. The proved graph-ideal lemma says its image saturation
quotient is killed by 2^H when V_(i-1) is the normalized saturated basis.
Thus the preceding algorithm applies with the SAME H at every stage.

The block operators and V_(i-1) are integral, so formation of C_i loses
no digits. Normalization loses at most `delta_i<=r_i H`. Therefore after
all k stages V_k is available at absolute precision at least

    P_in-sum_i r_i H >= P_in-2m^2 H.                   (8)

The displayed schedule guarantees the incoming precision at stage i is
larger than r_i H, so every pivot and determinant used there is visible.
No multiplicative precision recurrence is being hidden in (8).

The true ranks and graph identities are premises about the actual DAG
inputs, not conclusions drawn from their truncated digits. Finite input
approximations may violate those identities at high order and may have a
larger formal rank if treated as unrelated exact matrices. The algorithm
does not do that: it stops at the proved r_i and evaluates the rational
chart (5), whose error is controlled by (7).

## 5. Membership map, unit RR solves and extraction

At the final stage r_k=m. Let I be V_k's identity-row set. The exact
membership/quotient map is

    Lambda(z)=z_(I^c)-(V_k)_(I^c) z_I.

It has integral coefficients, is surjective onto O^m, and has kernel the
ACTUAL saturated image in T. Constructing it loses no digits. This is
the quotient lattice used in the RR theorem; no evaluated-point or
maximal-order lattice is substituted.

Set N=m+g. There are exactly m monomials of pole weight <N. Let E_<N be
their remainder columns in T, and let e_N,e_(N+1) be the remainder columns
of the unique monomials of weights N and N+1. Monic reduction modulo A
preserves precision. On the coordinate-good event the fixed matrix

    M_0=Lambda E_<N

is invertible over O by the proved weighted-basis theorem. Test its
determinant modulo 2; otherwise ABORT. This fixed set of columns removes
the need for an additional RR chart search.

Solve the two unit systems

    M_0 c=Lambda e_N,       M_0 dvec=Lambda e_(N+1).

Subtract their combinations of the lower monomials from the respective
top monomials. The resulting sections F=p+qY and G=r+sY have top
coefficients one; G also has coefficient zero at weight N. Unit inversion
and all the remaining integral arithmetic preserve the available absolute
precision. The fixed monomial degrees and exact leading ones are retained
structurally, without searching for leading numerical nonzero coefficients.

With epsilon=(-1)^N, compute

    a_*=(p^2-f_L q^2)/(epsilon A),
    b_tilde=(p r-f_L q s)/(epsilon A),
    b_*=remainder of b_tilde modulo a_*.

The exact theorem proves `p s-q r=epsilon A` and these polynomial divisions.
Both divisors have unit leading coefficients; the numerator operations and
monic divisions preserve absolute precision. No inverse of q, resultant,
support separation, or exact zero decision is required. A tiny numerical
remainder is not being used to prove exact divisibility: exact divisibility
comes from the certified ideal/RR construction on the actual inputs.

Reverse the weighted scaling. This loses at most dL digits. Combining
this with (8), while retaining the two guard digits, proves (1)--(2).
A final coefficient-pole-cap check is finite as well: P_out>=1 makes every
violation of a nonnegative prescribed pole cap visible; an invisible error
cannot turn an accepted bounded coefficient into one violating that cap.

## 6. Compact ledger and refinement contract

| Operation | Worst additional absolute precision loss |
|---|---:|
| Signed blocks; positive weighted scaling | 0 |
| A, companion/operator matrices, integral evaluations | 0 |
| Minimum-entry pivot selection via (3) | 0 |
| Product-stage saturated normalization i | delta_i <= r_i H |
| Quotient map and monomial remainder columns | 0 |
| Fixed unit RR matrix; normalized F and G | 0 |
| Norm products and monic extraction | 0 |
| Return to the original curve coordinates | <=dL |

The saved chart consists of the product-stage row/column choices and their
visible determinant valuations, followed by the fixed unit RR system and
the fixed polynomial formulas. There are polynomially many choices and
arithmetic nodes. Determinant expressions are evaluated as matrix operations,
not expanded symbolically into exponentially many monomials.

On later refinement, request P_out+C_mat digits from each actual input DAG,
reevaluate these same rational charts, and retain the same exact objects.
Formula (7) bounds changes in bases; the polynomial/unit maps then bound
changes in membership matrices, RR coefficients and output coordinates.
Discrete pivot choices need no new oracle and cannot introduce an ancestry-
dependent precision cost. The absolute input format needs P_in+S_in unit
bits when poles are present, still polynomial in the charged parameters.

Outside the good-output premise, failure of the unit RR test or final cap
test returns ABORT within this same clock. The conditional success event
and the soundness of an accepted actual-point identity remain those proved
in the materializer/weighted-basis reviews. This note pays the missing
operation-by-operation additive precision interface only.
