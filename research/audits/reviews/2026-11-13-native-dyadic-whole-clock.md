# Native dyadic complete image: current fixed-clock composition

2026-11-13. Independent, bounded whole-clock review of the current 350-line
`LOCAL_KUMMER_NATIVE_END_TO_END.md`. The STATE/TRAPS protocol was followed.
No Git, network, external API, implementation, or numerical experiment was used.
This review leaves shared notes untouched.

## Decision and scope

**ACCEPT the current written composition.** For every monic squarefree
`f in Z[x]` of odd degree `2g+1`, at the fixed prime 2 and for `0<eta<1`,
the assembled algorithm has a polynomial bit-time clock, returns a basis of
the COMPLETE local Kummer image or ABORT, and has ABORT probability below
eta. An accepted execution has the asserted exact image; correctness does
not require that its samples belonged to the sufficient geometric event.
The degree-one case is handled separately as the trivial Jacobian.

This is a proof-level conclusion using the independently established
geometric/grid, algebraic, and native-backend lemmas, with their actual
premises checked at the interfaces below. It is not an implementation test,
a new claim of novelty, an all-primes local theorem, or a global algorithm
or quantum-advantage conclusion. No additional unpaid input was found in
this current composition.

The operation ledgers checked for this review are
`2026-11-13-canonical-materializer-precision.md`,
`2026-11-13-stoll-half-precision-ledger.md`,
`2026-11-13-native-local-squareclass-backend.md`, and
`2026-11-13-dyadic-finite-group-stopping.md`. The ideal-saturation/weighted-RR
proof was also consulted for its off-event acceptance and sign statements.
The paid whole-DAG report's earlier objections are not treated as evidence
against the updated candidate without checking whether they remain present.

## 1. Fixed native parameters and source leaves

The discriminant valuation `D` is computable and is polynomial in the
native degree/coefficient bit length. The displayed `D0,R,H,K_index,T0`,
followed by `k,s,Q,m_grid,S_store`, are computable before sampling. In
particular `K_index` replaces the unknown exact saturation index kappa;
there is no circular choice of the clock from a discovered group order.
Set `S0=L=S_store` throughout.

Every accepted canonical materialization has degree g. Consequently the
half ledger's source degree is fixed here at `d=n-g=g+1`, where `n=2g+1`.
Its optional notation `e<=g` need not make `C_half` adaptive. Equivalently
one could take the maximum of its explicit polynomial over `0<=e<=g`.
The candidate's final instruction to use the exact half ledger also means
using `S_hat`, not the original input coefficient cap, in its determinant
and extraction estimates.

Initial points and newly drawn sigma points are native leaves, not long
expressions to be expanded. For `t_i=4i`, and also for
`t_i+2^R z_i`, the valuation of t is exactly `2+v_2(i)`: R is larger.
Thus the latter parameter never vanishes. The values `x=t^-2` and
`y=t^-n sqrt(F(t^2))` have the fixed pole bounds asserted in the candidate.
The near-one root is in its certified Hensel ball; fixed additive guard
`10(n+1)(2+ceil(log_2 g))+10` safely pays the divisions and that root.
The sampled parameter integers have polynomial bit length even though the
grid cardinality is exponential; no grid is enumerated.

Initial labels have their own nonzero representatives. A branch divisor
uses `(-1)^deg(a)(a-f/a)`, not a zero evaluation of a factor of f; its
norm valuation is at most D. A seed's representative is a signed
`x-t^-2`, whose norm valuation is negative, hence also at most D.
Their coefficient poles are at most S0. Therefore the displayed

    V_init=n(D+n*S0+S0+1),
    C_init=20(n+1)^2(D+V_init+1)+n*S0+D+10

pay these labels without a new success assumption or an unbounded zero
test. Fixed local-factor identifiers, integral bases, residue coordinates,
uniformizers, and root selectors refer to the ORIGINAL f. The index/CRT
loss is bounded by D/2. Their refinements use the proved fixed setup guards;
no approximate factor field is substituted for the selected actual field.
The one-time Las Vegas preprocessing has a known polynomial expected bound;
constant-probability capped attempts and logarithmically many independent
restarts give the separately allocated eta/10 timeout probability.
Subsequent refinement and the finite-ring backend are deterministic.

## 2. What each accepted group node actually proves

A binary node has at most 2g degrees from its two stored canonical blocks
and 4g from the signed point occurrences in `2 sigma`, hence `m<=6g`.
Source and retained blocks have degree at most g and coefficient poles at
most S0. Negation only changes b's sign. Common scaling by L therefore
makes all required graph blocks integral on the monic odd-degree model;
its discriminant exponent is exactly `D+2L*n*(n-1)`.

The materializer uses the conjugate graph ideals `(a,Y+b)` for points
represented with `Y=b`. The RR divisor identity is consequently
`div(F)=iota(D_input)+D_output-(m+g) infinity`, so its extracted point has
the INPUT SUM class, with the correct sign. Its known-rank saturation
charts have bounded nonzero Smith exponents. Minimum-entry elimination
and identity-pivot normalization are finite rational charts selected from
visible valuations, not enumeration of maximal minors. The accumulated
loss is at most

    C_mat=nL+72g^2*(D+2L*n*(n-1)+2)+2.

Successful unit quotient/RR checks imply the exact determinant and norm
identities even off the sufficient good-coordinate event. Monic extraction
then gives an actual degree-g graph divisor of the required class. The
stored pole test is mandatory. Arbitrarily close or repeated supports and
input/output overlap do not require an inverse of the RR coefficient q.

A half node first materializes the ACTUAL `h+2 sigma`, with no second,
unrecorded shift inside that materializer. Its input has zero exact
Kummer label, so it is divisible by 2 in the actual local group. The
visible input discriminant and branch-resultant caps supply the premises
of the scalar-pencil probability estimates. The pencil preserves the
class and uses the sign `(-1)^deg(A_u)` in its root equation.

The half ledger pays the source-resultant tests, exact selected square
root, augmented Stoll determinant, extraction determinant, and output
label. Two acceptance guards are essential:

* Invertibility of the augmented Stoll matrix does NOT imply that U is
  invertible modulo W. The candidate now separately requires visible
  nonzero `Res(W,U)` within the scaled cap `K_X` before division.
* W's stored pole cap is checked BEFORE extraction. The exact odd-degree
  norm identity then bounds U and V even on accepted off-event samples.

After those tests, the exact congruences and their degree bounds imply
`V^2-f U^2=epsilon A_u W^2`. The extracted `[W,-V/U mod W]` is an actual
half. Its stored coefficient cap and visible `Res(W,f)` bound precede
label evaluation. A failed or unresolved bounded visibility test gives
ABORT, not a claim of exact zero or a guessed label. These facts rule out
an accepted erroneous path arising merely from a failed good-event bound.

## 3. Additive precision really composes with the fixed clock

Use the exact explicit `C_half` of the half ledger with the fixed caps in
the candidate. Its successive costs are

    C_pen+K_src+C_root+C_M+2K_B+C_X+2K_X+C_out.

They cover INPUT perturbations and field-data precision, not only sizes
of the exact answers. The square-root selector and the finite pivot
choices are retained. Thus they identify one actual arithmetic chart and
one exact selected root throughout; there is no sign switch on refinement.

Set, exactly as in the candidate,

    C_max=C_mat+C_half+1,
    P_cert=2+C_mat+C_half+C_init+K_B+K_X+K_src,
    P_star=P_cert+T0*C_max.

All quantities are fixed polynomials before any group sample. Source
leaves are supplied at P_star, with their already bounded setup guards.
For a group node of depth j write `P_j=P_star-j*C_max`. Each parent has
precision at least `P_j+C_max`. A binary node needs only `P_j+C_mat`.
For a half node, compute its canonical shifted input to `P_j+C_half`;
this needs parent precision `P_j+C_half+C_mat<P_j+C_max`. The half then
returns its point and label at the required P_j. The largest field-data
request inside it is covered by that same parent allowance, so fixed
field data at P_star with its setup guard suffices.

Thus the inequality is additive at each edge. It does not replace a
requested precision by a polynomial of that precision. The source tests,
scaled determinant tests, initial labels and pole tests all have more
than their visibility threshold at P_cert; a further unknown exact-zero
or normalization test is not needed. No ancestor must be recomputed or
expanded. Frozen rational charts/root balls are retained as certificates
of actual points, while finite coefficients are approximations to them.

## 4. Exact quotient, stopping, node count and original E

The independent initialization gives
`A[2]=(L/E) direct_sum G[2]`, of dimension `q=g+t<=3g`, in the quotient
by the ORIGINAL `E=2L`. Initial label dependence is allowed and does not
invalidate that independent abstract presentation.

At each stage, the immutable triangular relation matrix presents the
actual generated subgroup of A. Choosing a zero-label binary vector
outside its row span modulo 2 gives a nonzero element of B/2B. A half
adjoins exactly one new order-two quotient coset. Append only the relation
`(-v,2)`; no point equality oracle or large-exponent basis recombination
is required. At full label rank q, `B+2A=A`, so the finite 2-group A/B is
zero. The returned labels therefore span the complete image.

There are exactly kappa successful enlargements mathematically, with
`kappa<=K_index`. Assembling the selected 0/1 vectors by binary operations
and then halving uses at most

    kappa*q+kappa*(kappa-1)/2 <= K_index*(q+K_index)

group nodes. Initialization and the separately named shifts/scalar draws
fit within `T0=4(K_index+3g+10)^4`. Internal field/matrix arithmetic is
charged by the polynomial per-node ledgers; it is not an extra chain of
group nodes. Hence every depth is at most T0 and `P_j>=P_cert`.

Each binary assembly and each half records its actual perturbation in
ORIGINAL E. In particular the new relation is
`2Q-sum(v_i P_i)=e_assembly+2 sigma_half in E`. No new lattice is silently
substituted after a coordinate reset. The exact point/root/pivot DAG is
sufficient for these identities; finite coefficient approximations are
never themselves declared exact points.

## 5. Conditional probabilities and polynomial bit cost

For a binary node, the geometric bound applies to every incoming h. For
a zero-label half node, h lies in 2G, and the stronger bound covers h_z
AND ALL its rational halves. These are uniform statements conditional on
the previously revealed actual points and choices. Fresh z is independent
of that history. After h_z is fixed, the set of its rational halves is
fixed before u is sampled, even though the algorithm's chosen half can
depend on u and on the backend selector.

The scalar union degree is at most `2n*4^g`. With
`t_scalar=k+2g+ceil(log_2(16n))+2`, its tail is at most `2^-k/32` on the
geometric good event. The half set and the scalar grid are not enumerated.
Clearing coefficient denominators shifts the polynomial content and value
together, so the candidate's raw caps retain that estimate. On the joint
good event all the actual acceptance tests discussed above pass.

At most T0 stages need these fresh geometric/pencil estimates. Therefore
with `k=ceil(log_2(100*T0/eta))` their total failure is at most
`2*T0*2^-k<=eta/50`. Adding the eta/10 preprocessing timeout leaves strictly
less than eta. Adaptivity does not require unconditional independence of
success events. Failure stops with ABORT; a partial image is never labeled
complete.

Finally, D, K_index, T0, all valuation caps, and all additive precision
budgets are fixed polynomials in `g,B,log(1/eta)`. Matrix and field degrees
are polynomial in g. P_star is a product/sum of those polynomials, and
each node is evaluated once using polynomial-bit arithmetic. Exponential
group orders, coordinate grids, residue fields and half sets occur only
in proofs or logarithmic sampling bounds, never as enumeration costs.
The current candidate therefore closes the written fixed-clock dyadic
composition at its stated scope.
