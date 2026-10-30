# Independent Review: One Correlated Rees Source

Date: 2026-10-27. Mathematical review only; no implementation or literature audit.

## Verdict And Corrections

**The proposed failure of this concrete shortcut survives.** I found no error
in the source isometry, native two-query realization, anti-representation
ordering, conditional sectors, genuine Rees examples, or nonzero-sector
kernel equality. The capped distinguishing bound follows for arbitrary
adaptive/joint control processing, including repeated right-action access,
under the precise algebraic interface below. This is not an HSP lower bound.
The subsequently added weak-Fourier characterization also survives: the
restricted statistical experiment is exactly the native irrep-weight
experiment, without an efficiency claim. Section 5 checks both directions.

The initial review of [RESULT.md](/Users/jaspersands/Developer/qsearch-research-work/rees-correlated-source-2026-10-27/RESULT.md)
identified these focused qualifications. The parent subsequently reported
them addressed; see the final addendum for current status.

1. **[P2] Do not turn this source-specific failure into a restriction on every
   future correlated source.** The final research-decision requirement for an
   observable outside the right-translation compression is necessary to
   distinguish the all-nonzero sectors of this source. A different native
   correlated source could have an informative restriction to the same
   right-action algebra. Its preparation cost and joint kernel must be
   analyzed; this example does not rule it out. The hypothetical opposite-label
   conditional-product bank illustrates the distinction but supplies no cheap
   preparation theorem.
2. **[P3] Distinguish padded and actually observed labels.** In the resource bound,
   equality with `1-(1-1/p)^T` is for the T potential, padded acquisitions.
   An early-stopping protocol's actual probability of observing a zero label
   is at most this quantity. The stated success upper bound remains correct.
3. **[P3] Make two conventions explicit.** "Central label" here means the
   character of the selected grade `Z = exp(<t^2 W>)`, not of the full center.
   The maximally mixed quotient-control conclusion assumes a uniformly
   initialized quotient control. For arbitrary initial controls the same
   kernel gives complete dephasing, not necessarily a maximally mixed state.

The new algebra section supplies the previously missing complete-protocol
justification. Keep the source contract explicit: initial controls/advice are
H-independent, hiding outputs/purifications are inaccessible, target
interactions are confined to the stated algebra, and targets are ultimately
discarded. Section 6 proves the adaptive/joint bound under that contract.
Holding targets for repeated allowed interactions does not evade it;
arbitrary measurements of those targets do.

The parent's reported 39 new plus 40 source-tree controls are not independent
evidence supplied by this review. I did not inspect or rerun their code, and
the reasoning below does not depend on those finite checks.

## 1. Source And Native Cost

Put `N = |G|`. Directly,

    <Vg'|Vg> = (1/N) sum_y 1{g'y = gy} = 1{g'=g}.
    V*|x,y> = N^(-1/2)|x y^-1>.

Thus the public reversible map `|g,y> -> |g y,y>` applied to
`rho_H tensor |+><+|` implements the source. Its inverse on the full pair is
`|x,y> -> |x y^-1,y>` and returns `rho_H tensor |+><+|`.

Alternatively, a uniform pair queried at `x y^-1`, with public argument
workspace uncomputed and only the hiding output discarded, has matrix entry

    N^(-2) 1{(x y^-1)^-1 (x' y'^-1) in H},

exactly `V rho_H V*`. Retaining or tracing dirty argument workspace would
change this density. No inverse hiding-oracle query is needed for public
arithmetic cleanup.

For the actual class-two cover, evaluation into the original Heisenberg
group in BCH coordinates is

    E_s(x,y,w,z) = (s*x, s*y, s*w + s^2*z).
    f_hat(u) = (f(E_1(u)), f(E_2(u))).

Both evaluations are group homomorphisms. For every odd p the coefficient
matrix `[[1,1],[2,4]]` has determinant 2, hence is invertible. For the native
line `<X>`, requiring both evaluations to lie in that line forces `y=w=z=0`;
for `<Y>` it forces `x=w=z=0`. Therefore the lifted hidden subgroups are
exactly the claimed `H_X` and `H_Y`, not accidental larger pullbacks.

Two ordinary evaluations of f, retaining their output labels until the final
trace, implement one lifted query. This checks the prescribed cost, not its
optimality among all reductions. Public reversible arithmetic has polynomial
bit cost in this explicit four-coordinate family; label width and ideal
uniform/Fourier primitives remain part of the access contract. No efficient
uniform sampler for an arbitrary encoded finite group is inferred.

This agrees with the local [ordinary-query lift](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/REES_HSP_REDUCTION.md:91),
but the coordinate calculation above independently checks this example.

## 2. Action Ordering And Conditional Sectors

With the RESULT convention,

    R_a R_b = R_(b a),                 R_a* = R_(a^-1).
    V*(R_a tensor R_b)V = (1/N) sum_y R_(y a b^-1 y^-1).

For `U_q = R_(a(q)) tensor R_(b(q))`, the multiplier on density entry
`(q,q')` is `Tr(Theta_lambda U_q'* U_q)`. The two right-action arguments
are `a(q)a(q')^-1` and `b(q)b(q')^-1`; their relative product is therefore

    a(q) a(q')^-1 b(q') b(q)^-1.

This is exactly the displayed ordering. Reversing the usual representation
rule without changing the kernel would be an error, but RESULT does not do
that. Also `(R_a tensor R_a)V = V` for every a, directly by reindexing y.

Fix a central subgroup Z and define the character projector consistently by

    P_lambda = |Z|^(-1) sum_(z in Z) conjugate(chi_lambda(z)) R_z.
    rho_H,lambda = P_lambda rho_H P_lambda / Tr(rho_H P_lambda).

Only positive-mass sectors may be normalized. The central intertwining
identities give opposite labels and the normalized JOINT state
`V rho_H,lambda V*`; they do not give independent target sectors. In general
the mass is `|H intersect Z|/|Z|` for characters trivial on that intersection,
and zero otherwise. Here `H_X intersect Z = H_Y intersect Z = {e}`, so every
lambda has mass `1/p`. There is no absent nonzero-label branch to discard.

Using `Tr(rho_H R_u) = 1_H(u)` in the projector formula gives

    Tr(rho_H,lambda R_u) = chi_lambda(z0)  if u = h*z0 in HZ;
                           0                otherwise.

The positive character sign is correct with the stated R convention. It
must not be imported by name from a different inverse-right-action convention.

## 3. Genuine Rees Lines And Vanishing Distinguishing Kernel

Here `gamma_1(L)=<X,Y,W>` and `gamma_2(L)=<W>`, so the cover really is
`tL + t^2<W>`. Its only nonzero basis bracket is `[tX,tY]=t^2W`; the separate
grade-one `tW` coordinate must remain. Both lines lift from native subgroups,
are graded, are nonnormal, and meet the selected Z trivially.

For `v=(alpha,beta,omega,zeta)` and `u=(x,y,w,z)`, the group law yields

    v u v^-1 = (x,y,w,z + alpha*y - beta*x).

For nonzero `(x,y)`, the last increment is uniform on F_p as v ranges over
the group. Membership in `H_X Z` or `H_Y Z` is preserved by conjugation.
If membership fails, every summand in C vanishes; if it holds and
`(x,y) != (0,0)`, the nontrivial character average vanishes. When `x=y=0`,
membership for either line additionally requires `w=0`. Hence for lambda != 0,

    C_X,lambda(u) = C_Y,lambda(u)
                  = chi_lambda(z) if x=y=w=0, and 0 otherwise.

For lambda=0 the result is instead `1_(HZ)(u)`. These are exact identities
for every odd p. "Vanishing" refers to the distinguishing/off-central
kernel, not to the probability or trace of the nonzero-sector state.

The full center is `exp(<tW,t^2W>)`, of rank two. In full-center notation
`(mu,lambda)`, labels `(mu,0)` with mu != 0 are not covered by the phrase
"nonzero lambda". Keeping the selected grade explicit prevents that false
extension.

For a uniform control on `Q=G/Z`, the section choice in RESULT gives
`I_Q/|Q|` on nonzero lambda: distinct q and q' cannot have a section difference
in Z. At lambda=0 it gives the coset density of `HZ/Z`. The quotient is
abelian here, so the displayed `q q'^-1` versus `q^-1 q'` membership
conventions agree. Without uniform initialization the nonzero channel merely
sets off-diagonal control entries to zero.

## 4. Marginals Are Not A Product Bank

The newly displayed unconditioned marginal formulas are correct. More
explicitly, let `J|g> = |g^-1>`. For either the unconditioned native density
or a normalized central sector sigma,

    Tr_second(V sigma V*) = (1/N) sum_y R_y sigma R_y*.
    Tr_first(V sigma V*)  = J sigma J*.

The second identity uses the left-translation invariance of native coset
densities and their central sectors. This also avoids ambiguity about the
names "left coset" and "right coset": the kernel in RESULT is authoritative.
The native matrix with `g^-1 g' in H` is supported on sets `gH`.

The second marginal retains a native sector up to public inversion; the
first is conjugation-twirled. Thus perfect opposite labels do not implement
the [earlier conditional-product bank](/Users/jaspersands/Developer/qsearch-research-work/rees-source-tree-review-2026-10-27/REVIEW.md:78).
The parent's computational-basis measurement of the second register and
known right-translation undoing is another valid recovery of one original
source. Neither recovery manufactures two independent sector targets.

## 5. New Weak-Fourier Corollary

Let `B=span_C{R_g}` and `A=B tensor B`. The map `Phi(E)=V* E V` is unital
and completely positive, since V is an isometry. The displayed compression
of each basis element is a conjugacy average, hence belongs to `Z(B)`.
By linearity, `Phi(A) subset Z(B)` for every finite group and every native
input density rho, not just a coset density.

The primitive central projections of B are mutually orthogonal projectors
`Pi_pi` summing to I. Consequently every effect `0<=E<=I` in A satisfies

    Phi(E) = sum_pi e_pi Pi_pi,        0<=e_pi<=1.

Positivity and the upper bound follow from `0<=Phi(E)<=Phi(I)=I` on each
nonempty block; no coefficient-positivity assumption in the group basis is
needed. For a POVM `{E_o}`, unitality gives `sum_o e_(o,pi)=1`. Therefore

    Pr(o | V rho V*) = sum_pi e_(o,pi) Tr(rho Pi_pi).

This is precisely classical stochastic postprocessing of the native weak
Fourier distribution. Conversely, twirling any central element fixes it, so

    Phi(Pi_pi tensor I) = Pi_pi.

Thus the compression range is actually ALL of `Z(B)`, and measuring these
first-target central projectors gives the native weights themselves. Use one
consistent convention for the irrep labels: changing from inverse-right
representations to this anti-representation can relabel pi by its dual, but
does not change the statistical characterization.

The converse is not merely a formal allowance of a new target observable.
It can be realized with unrestricted controls and controlled right actions.
Write `Pi_pi=sum_u c_(pi,u) R_u`. Prepare a group-indexed ancilla uniformly,
apply controlled `R_g` to the first target, and measure the ancilla projectors
`Q_pi=J Pi_pi J*`, where `J|g>=|g^-1>`. These are a public orthogonal POVM,
with `Q_pi[h,g]=c_(pi,g h^-1)`. Its induced first-target effect is

    (1/N) sum_(g,h) Q_pi[h,g] R_h* R_g
      = sum_u c_(pi,u) R_u = Pi_pi.

This only establishes existence in the unrestricted-control interface.
Implementing that ancilla measurement can be expensive; no efficient QFT,
classical simulation, or efficient sampling of the weights follows.

For T sources, compression of an induced effect in `A^(tensor T)` lies in
`Z(B)^(tensor T)`. Its coefficients in the product projectors again form
probabilities. On fresh independent native states the weights are products
of the individual irrep weights; arbitrary joint processing is a stochastic
map on the entire label tuple, not necessarily separate per-copy processing.
Central-character projectors are already sums of the appropriate `Pi_pi`
blocks, so recording them introduces no extra information.

One proof-order caution matters: Phi is generally NOT multiplicative.
Compose/adapt the receiver in A first and compress the resulting effects;
do not multiply compressed gates as if `Phi(EF)=Phi(E)Phi(F)`. The new RESULT
uses the valid effects-and-algebra argument, and Section 6 makes it explicit.

## 6. Complete Adaptive/Joint Protocol Proof

For one target pair let

    A = span_C{U_(a,b) : a,b in G},     U_(a,b)=R_a tensor R_b.

This is a unital *-algebra, since

    U_(a,b) U_(c,d) = U_(c a, d b),     U_(a,b)*=U_(a^-1,b^-1).

For fixed nonzero lambda, the source expectation functional restricted to
A is the same for X and Y:

    phi_H,lambda(U_(a,b)) = C_H,lambda(a b^-1).

Equality on this spanning set gives equality on all of A, not just on a
single advertised control kernel. For T fresh sources and a fixed all-nonzero
label vector, independence makes the expectation functionals equal on
`A^(tensor T)`.

Allow arbitrary H-independent ancillary controls, joint control unitaries,
measurements, adaptive classical choices, and controlled right actions on
any targets. Conditioned on labels and an outcome history, every circuit
Kraus operator belongs to `B(controls) tensor A^(tensor T)`: generators have
that form and products/sums/adjoints remain in it. Taking a final control
measurement and the expectation over the H-independent initial control
state produces an effect on the sources in `A^(tensor T)`. Intermediate
target discard is represented by identities on those targets in this
backwards calculation. Adaptive branches obey the same closure argument.

Consequently every retained control outcome probability agrees for X and Y
on an all-nonzero label vector. Testing with every final control POVM gives
equality of the entire retained control state and classical transcript.
This includes entangled controls, repeated use of targets before discard,
coherent sums of right-action words, and adaptive stopping. It does NOT
assert equality of the physical target states under arbitrary measurements.

Fresh acquisitions must be independent copies of the specified mixed
source, with no correlated hidden advice or accessible source purification.
The deterministic cap T counts all acquisitions, including rejected labels
and restarts. Preassign T IID uniform labels and pad unused acquisitions.
For the good event E that all padded labels are nonzero,

    Pr(E) = (1-1/p)^T,                 epsilon = 1-Pr(E).
    sigma_H = (1-epsilon) tau_good + epsilon tau_H,bad.

The normalized tau_good is common to both hypotheses by the preceding proof;
the bad states need not agree. Thus, with trace distance D,

    D(sigma_X,sigma_Y) <= epsilon <= min(1,T/p).
    P_success(equal prior) <= 1/2 + epsilon/2.

This is an unconditional decision bound. Conditioning the reported success
on a rare accepted/zero-label event is not covered. Early stopping changes
the observed-zero probability to an inequality but not this proof.

In particular, success >= 2/3 requires

    T >= ceil(log(2/3) / log(1-1/p)),

which implies the weaker stated `T >= p/3`. This is a necessary condition,
not a sufficiency or an optimal native-query theorem. If an approximate
implementation's COMPLETE output, including records/abort, is within trace
distance delta of the ideal output for each H, the success upper bound
acquires `+delta`. Branchwise renormalized error estimates alone do not
justify that extension.

## 7. Explicit Escapes And Final Recommendation

There is a particularly small excluded observable. Set `L_s|g>=|s g>`.
Reindexing the second register gives

    (I tensor L_s)V = V R_(s^-1).

Take `a=(1,0,0,0)` in H_X and use `s=a^-1`. The expectation of this public
left action is `k_X,lambda(a)=1` versus `k_Y,lambda(a)=0`, for EVERY lambda,
including nonzero ones. A Hadamard test has plus probability 1 versus 1/2;
answering X on plus and Y on minus succeeds with equal-prior probability
3/4 using one source. This is outside A, and explicitly falsifies any claim
of global all-nonzero information loss. It recovers access to one native
source's information, not an independent cancellation bank or a general
HSP solver.

There is also an exact two-original-query classical baseline for this binary
promise: compare `f(e)` and `f(exp X)` in the original Heisenberg group.
They agree exactly for the X line. Thus no unrestricted difficulty claim
can be attached to this example, even without invoking general HSP algorithms.

Retain the concrete negative result with the algebraic interface and padding
qualification above. Keep open genuinely different native correlated sources
with informative right-action functionals, left/mixed-action receivers,
and explicitly paid multi-output constructions. None is shown here to
improve source complexity. The fixed-class theorem and the earlier scoped
source-tree bound are neither strengthened nor refuted by this review.

Only this isolated REVIEW.md was written. No main repository, Git state,
UI, dependency, parent artifact, or implementation was changed.

## Final Addendum And Status

**Weak-Fourier corollary: verified, with no further mathematical correction
required.** Section 5 independently checks central compression, positivity
and completeness of the resulting stochastic coefficients, the converse
projector identity and its allowed-control realization, and the joint-copy
extension. Composition takes place in the target *-algebra before
compression; no multiplicativity of compression or efficient QFT is assumed.

The parent reports that RESULT now incorporates the earlier qualifications
on advice/purifications/extra queries, same-source versus different-source
claims, padded versus observed zero events, and selected Z/uniform controls.
Those findings are therefore recorded as addressed by the parent, rather
than outstanding mathematical objections. The added native controls were
not inspected or independently rerun, as requested.

Final conclusion: the concrete correlated-source shortcut fails in the
specified right-action interface, whose information is statistically
equivalent to native weak Fourier sampling. The capped adaptive/joint bound
survives. Different sources or excluded observables remain genuine escape
routes; no unrestricted HSP lower bound or efficient simulator follows.
